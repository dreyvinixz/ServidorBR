# Testes e carga - ServidorBR

## Testes automatizados existentes

Com Python 3.12 e dependências instaladas:

```powershell
python -m pip install -r backend/requirements.txt
python -m unittest discover -s backend -p 'test_*.py'
```

Seis casos no host passaram em 20/10/2026: normalização, parâmetros desconhecidos, UF válida indisponível, UF inválida, paginação inválida e bind parameter com payload de SQL injection. CI reproduz o comando no GitHub Actions.

## Validação de configuração

`docker compose config -q` passou localmente em 20/10/2026. Isso valida a sintaxe/resolução do Compose, não inicia containers nem comprova comunicação com PostgreSQL, API ou interface.

## Carga

Não há medições de RPS, latência, percentis, erros concorrentes, CPU ou RAM. A tabela não é preenchida com estimativas; o cenário de carga precisa ser executado sobre a stack e um conjunto representativo antes de registrar conclusões.

| Concorrência | RPS | Média | P50 | P95 | P99 | Erros/timeout | CPU/RAM |
|---:|---|---|---|---|---|---|---|
| Não medido | - | - | - | - | - | - | - |

Rate limit em memória, limite de consulta de 8 s e timeout Gunicorn de 15 s são configurações iniciais, não limites validados por benchmark.
