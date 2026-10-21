# Análise da busca por similaridade

Investigação local vinculada à issue [#25](https://github.com/dreyvinixz/ServidorBR/issues/25). O objetivo é localizar o custo da busca `similar=MARIA` antes de alterar a API ou os índices. Nenhuma consulta de produção ou índice foi modificado nesta etapa.

## Ambiente e consulta

- PostgreSQL 16 / `pg_trgm` 1.6, via Docker Compose.
- Tabela `servidores`: 414.801 linhas vivas; tabela com 81 MB e índices com 227 MB. O índice `ix_servidores_nome_trgm` ocupa 41 MB.
- A tabela tinha `n_dead_tup = 0` e `last_autoanalyze` em 20/10/2026.
- Todos os planos foram capturados com `EXPLAIN (ANALYZE, BUFFERS)`, executando as consultas na base local.
- O filtro reproduz o da API: `nome_norm % 'MARIA' AND nome_norm LIKE '%MARIA%'`. A consulta de resultados ordena por `similarity(nome_norm, 'MARIA') DESC, nome_norm`.
- O benchmark HTTP anterior usa `per_page=1`; a API sem esse parâmetro usa 25 por página. Foram inspecionados ambos os limites.

Comando-base para reproduzir o `COUNT` e a seleção limitada:

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT count(*)
FROM servidores
WHERE nome_norm % 'MARIA'
  AND nome_norm LIKE '%MARIA%';

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, nome, cargo, orgao, uf
FROM servidores
WHERE nome_norm % 'MARIA'
  AND nome_norm LIKE '%MARIA%'
ORDER BY similarity(nome_norm, 'MARIA') DESC, nome_norm
LIMIT 1 OFFSET 0;
```

Trecho capturado do plano combinado do `COUNT`:

```text
Aggregate (actual time=215.654..215.656 rows=1 loops=1)
  Buffers: shared hit=10457
  -> Bitmap Heap Scan on servidores
       (actual time=27.136..215.271 rows=6970 loops=1)
       Recheck Cond: ((nome_norm % 'MARIA') AND (nome_norm ~~ '%MARIA%'))
       Rows Removed by Index Recheck: 68986
       Heap Blocks: exact=10153
       Buffers: shared hit=10457
       -> Bitmap Index Scan on ix_servidores_nome_trgm
            (actual time=26.071..26.072 rows=75956 loops=1)
            Buffers: shared hit=304
Planning Time: 1.482 ms
Execution Time: 215.906 ms
```

Trecho do plano com `LIMIT 25`:

```text
Limit (actual time=210.959..210.963 rows=25 loops=1)
  -> Sort (actual time=210.957..210.959 rows=25 loops=1)
       Sort Key: similarity(nome_norm, 'MARIA') DESC, nome_norm
       Sort Method: top-N heapsort  Memory: 29kB
       -> Bitmap Heap Scan on servidores
            (actual time=23.243..209.272 rows=6970 loops=1)
Planning Time: 0.701 ms
Execution Time: 211.183 ms
```

## Resultados observados

| Plano | Linhas relevantes | Tempo observado | Buffers / sort |
|---|---:|---:|---|
| `COUNT` combinado (3 execuções) | estimativa 37; 6.970 reais no heap scan | mediana 207,183 ms; faixa 204,036–212,012 ms | 10.457 shared hits |
| Resultados, `LIMIT 1` (3 execuções) | 6.970 linhas candidatas visitadas; 1 retornada | mediana 228,648 ms; faixa 224,530–275,359 ms | 10.457–10.463 hits; Top-N |
| Resultados, `LIMIT 25` (3 execuções) | 6.970 candidatas; 25 retornadas | mediana 215,877 ms; faixa 211,458–222,565 ms | 10.457 hits; Top-N usou 29 kB |
| Trigram `%` isolado | estimativa 194; 7.047 reais | 371,340 ms naquela execução | 141.630 entradas no bitmap; 134.583 removidas na rechecagem; 10.369 hits e 216 reads |
| `LIKE` isolado | estimativa 79.820; 75.595 reais | 34,143 ms naquela execução | 75.956 entradas no bitmap; 10.252 hits |
| `COUNT` limitado a 100 | 100 linhas contadas | 31,440 ms naquela execução | 567 hits; bitmap trigram ainda leu 75.956 entradas |

Os planos variam com o estado do cache; as execuções repetidas da consulta combinada ocorreram com todas as páginas em shared buffers. As medições isoladas de `%` e `LIKE` foram executadas antes do bloco repetido e não devem ser comparadas como se tivessem exatamente o mesmo estado de cache.

## Leitura dos planos

1. **O acesso ao heap do filtro combinado domina.** O plano combinado visita 10.153 blocos da tabela e reexamina 68.986 entradas candidatas do índice; somente 6.970 linhas satisfazem ambos os predicados. A estimativa do planner (37 linhas) fica muito abaixo do observado (6.970).
2. **A ordenação não explica a maior parte da latência.** O plano ordenado usa `top-N heapsort` e 29 kB para o limite 25. No plano detalhado, o heap scan consumiu cerca de 209,3 ms e a execução completa cerca de 211,2 ms; a ordenação acrescentou aproximadamente 2 ms.
3. **O `COUNT` integral repete o filtro antes da busca de resultados.** A rota executa `count(*)` e, depois, a seleção ordenada. As medianas locais de `COUNT` e seleção limitada ficam próximas de 207 ms e 216–229 ms, respectivamente, compatíveis com a busca HTTP anterior de P50 464 ms.
4. **O total exposto pela API é limitado.** Para busca por similaridade, a rota retorna `min(total, limit)`, e `limit` não pode exceder 100. Um `COUNT` sobre uma subconsulta limitada ao mesmo `limit` preserva o total exposto pela API: se houver menos resultados, conta todos; se houver mais, conta até o limite. No teste exploratório com limite 100, o `COUNT` caiu para 31,440 ms e 567 blocos, embora a criação do bitmap trigram ainda tenha lido 75.956 entradas.

## Recomendação para a próxima alteração

Priorizar um `COUNT` limitado a `limit`, coberto por testes de contrato para zero, abaixo do limite e acima do limite. Medir novamente o plano e a latência HTTP antes de considerar mudanças no índice ou na ordenação. A evidência atual não justifica adicionar índice de ordenação: o `Sort` é Top-N pequeno, enquanto a varredura/rechecagem do filtro e a contagem integral concentram o custo. O experimento de contagem limitada foi apenas `EXPLAIN ANALYZE`; a API continua inalterada.

Esta análise é de uma base local e de um único termo de busca. Não é benchmark concorrente nem previsão de desempenho em produção.
