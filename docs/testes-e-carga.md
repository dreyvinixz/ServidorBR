# Testes e Carga - ServidorBR

## Estratégia de testes

| Tipo | Escopo | Task | Status |
| --- | --- | --- | --- |
| API funcional | Nome, cargo, UF, órgão, filtros combinados, similaridade e paginação | SB-11 e SB-12 | Pendente |
| Validação | UF, limite, página, parâmetros desconhecidos, strings vazias e extensas | SB-11 | Pendente |
| Segurança | Payloads de SQL injection | SB-11 | Pendente |
| Integração | Frontend, backend, banco e Docker Compose | SB-16 e SB-21 | Pendente |
| Carga | Requisições concorrentes e proteção contra sobrecarga | SB-17 | Pendente |

## Cenários de carga previstos

| Cenário | Usuários simultâneos | RPS | Média | P50 | P95 | P99 | Erros | Timeout | CPU | RAM |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 10 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` |
| 2 | 25 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` |
| 3 | 50 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` |
| 4 | 100 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` |
| 5 | 200 | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` |

Preencher esta tabela somente com valores medidos. Informar ferramenta, configuração, data, versão testada e limitações quando a SB-17 for executada.
