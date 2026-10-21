# Testes e carga - ServidorBR

## Testes automatizados existentes

Com Python 3.12 e dependências instaladas:

```powershell
python -m pip install -r backend/requirements.txt
python -m unittest discover -s backend -p 'test_*.py'
```

Doze casos passaram localmente em 20/10/2026. Além dos seis testes de API já existentes (normalização, parâmetros desconhecidos, UF válida indisponível, UF inválida, paginação inválida e bind parameter com payload de SQL injection), a suíte cobre o operador `pg_trgm`, linhas idênticas preservadas, reimportação idempotente, delimitadores `;`, `,` e tabulação, nome vazio rejeitado, formato oficial sem cabeçalho em CP1252, campo grande em coluna não pesquisada e exclusão de CPF/matrícula dos dados persistidos.

## Validação de configuração

`docker compose config -q` passou localmente em 20/10/2026. Os containers `db`, `backend` e `frontend` iniciaram e ficaram saudáveis; a página retornou HTTP 200 e `GET /api/health` pelo Nginx retornou `{"database":"ok","status":"ok"}`. Com as duas publicações importadas, a busca por `AGENTE ADMINISTRATIVO` retornou HTTP 200 com 35 correspondências; a consulta por similaridade retornou HTTP 200 com limite de 100 resultados.

## Medição local de consultas

Com 414.801 registros importados das duas publicações oficiais de 08/2025, o script `backend/benchmark_api.py --runs 20` executou 20 requisições sequenciais por cenário via Nginx em `http://localhost:3000` (sem concorrência). O cliente mede o tempo HTTP ponta a ponta no host Windows; cada busca retorna no máximo 1 registro. P99 com 20 amostras é apenas o maior valor observado e não estima cauda de produção. O cenário de similaridade respeita o limite da API e informa no máximo 100 resultados.

Medição em 20/10/2026:

| Cenário | Linhas correspondentes | Média | P50 | P95 | P99/maior |
|---|---:|---:|---:|---:|---:|
| Nome exato sem resultado | 0 | 214,291 ms | 27,976 ms | 294,127 ms | 2.864,741 ms |
| Cargo parcial | 35 | 21,295 ms | 15,715 ms | 32,950 ms | 81,264 ms |
| Órgão parcial | 188 | 53,991 ms | 17,573 ms | 117,539 ms | 508,722 ms |
| Similaridade de nome | 100 (limite) | 470,935 ms | 464,402 ms | 535,489 ms | 550,370 ms |

O cenário de similaridade revelou um erro Psycopg no operador `%` do `pg_trgm`, que retornava 503. O operador foi escapado como `%%` na consulta parametrizada e passou a ser coberto por teste de regressão; após a correção, as 20 amostras responderam com HTTP 200.

Esses números são uma linha de base sequencial na fotografia completa local; similaridade foi a consulta mais lenta, com P50 de 464 ms e P95 de 535 ms. Um teste observou um pico isolado de 2,865 s na busca exata sem resultado. Os resultados justificam uma etapa futura de otimização e não representam teste concorrente ou garantia de produção.

A análise detalhada de `EXPLAIN (ANALYZE, BUFFERS)` para essa busca está em [`analise-busca-similaridade.md`](analise-busca-similaridade.md). Ela separa o custo do `COUNT`, do filtro trigram e da ordenação sem mudar consulta ou índice de produção.

## Carga concorrente

Ainda não há medições de RPS, latência sob concorrência, erros simultâneos, CPU ou RAM. A tabela não é preenchida com estimativas; o cenário de carga precisa ser executado sobre a stack e um conjunto representativo antes de registrar conclusões.

| Concorrência | RPS | Média | P50 | P95 | P99 | Erros/timeout | CPU/RAM |
|---:|---|---|---|---|---|---|---|
| Não medido | - | - | - | - | - | - | - |

Rate limit em memória, limite de consulta de 8 s e timeout Gunicorn de 15 s são configurações iniciais, não limites validados por benchmark.
