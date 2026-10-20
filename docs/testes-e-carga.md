# Testes e carga - ServidorBR

## Testes automatizados existentes

Com Python 3.12 e dependências instaladas:

```powershell
python -m pip install -r backend/requirements.txt
python -m unittest discover -s backend -p 'test_*.py'
```

Onze casos passaram localmente em 20/10/2026. Além dos seis testes de API já existentes (normalização, parâmetros desconhecidos, UF válida indisponível, UF inválida, paginação inválida e bind parameter com payload de SQL injection), a suíte agora cobre o operador `pg_trgm`, linhas idênticas preservadas, reimportação idempotente, delimitadores `;`, `,` e tabulação, nome vazio rejeitado, formato oficial sem cabeçalho em CP1252 e exclusão de CPF/matrícula dos dados persistidos.

## Validação de configuração

`docker compose config -q` passou localmente em 20/10/2026. Os containers `db`, `backend` e `frontend` iniciaram e ficaram saudáveis; a página retornou HTTP 200 e `GET /api/health` pelo Nginx retornou `{"database":"ok","status":"ok"}`. Depois de importar a amostra, a busca por `AGENTE ADMINISTRATIVO` retornou HTTP 200 com 35 correspondências; a consulta por similaridade retornou HTTP 200 com 6 correspondências.

## Medição local de consultas

Com 811 registros importados da amostra oficial `APOSENTADOS_082025.csv`, o script `backend/benchmark_api.py --runs 20` executou 20 requisições sequenciais por cenário via Nginx em `http://localhost:3000` (sem concorrência). O cliente mede o tempo HTTP ponta a ponta no host Windows; cada busca retorna no máximo 1 registro. P99 com 20 amostras é apenas o maior valor observado e não estima cauda de produção.

Medição em 20/10/2026:

| Cenário | Linhas correspondentes | Média | P50 | P95 | P99/maior |
|---|---:|---:|---:|---:|---:|
| Nome exato sem resultado | 0 | 21,865 ms | 14,391 ms | 35,155 ms | 66,309 ms |
| Cargo parcial | 35 | 18,629 ms | 14,470 ms | 30,216 ms | 52,153 ms |
| Órgão parcial | 188 | 15,158 ms | 14,262 ms | 19,967 ms | 22,249 ms |
| Similaridade de nome | 6 | 20,490 ms | 18,722 ms | 34,198 ms | 36,183 ms |

O cenário de similaridade revelou um erro Psycopg no operador `%` do `pg_trgm`, que retornava 503. O operador foi escapado como `%%` na consulta parametrizada e passou a ser coberto por teste de regressão; após a correção, as 20 amostras responderam com HTTP 200.

Esses números validam consultas funcionais e dão uma linha de base para uma tabela pequena. Não representam teste concorrente nem permitem projetar desempenho com a base completa.

## Carga concorrente

Ainda não há medições de RPS, latência sob concorrência, erros simultâneos, CPU ou RAM. A tabela não é preenchida com estimativas; o cenário de carga precisa ser executado sobre a stack e um conjunto representativo antes de registrar conclusões.

| Concorrência | RPS | Média | P50 | P95 | P99 | Erros/timeout | CPU/RAM |
|---:|---|---|---|---|---|---|---|
| Não medido | - | - | - | - | - | - | - |

Rate limit em memória, limite de consulta de 8 s e timeout Gunicorn de 15 s são configurações iniciais, não limites validados por benchmark.
