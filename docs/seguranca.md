# Segurança - ServidorBR

## Controles previstos

| Controle | Estratégia | Task |
| --- | --- | --- |
| SQL injection | Queries parametrizadas; nunca concatenar entrada do usuário em SQL | SB-07 e SB-11 |
| Validação | Validar campos aceitos, tamanho, tipo, UF, paginação e limites | SB-08 |
| Limite de resultados | `per_page` e `limit` com máximo de 100 | SB-08 e SB-12 |
| Rate limiting | Limitar excesso de requisições por cliente e responder 429 | SB-09 |
| Timeout | Interromper consulta demorada e responder 503 sem travar workers | SB-09 |
| Segredos | Usar `.env`; ignorar credenciais no Git | SB-10 |
| Erros | Não expor stack trace, strings de conexão ou dados internos | SB-09 |

## Casos que serão testados

```text
' OR 1=1 --
'; DROP TABLE servidores; --
```

Essas entradas devem ser tratadas como dados de busca, nunca como comandos SQL.

## Evidências pendentes

- [ ] Validações implementadas e cobertas por teste.
- [ ] Testes de SQL injection executados.
- [ ] Rate limiting e timeout verificados.
- [ ] Revisão de segredos antes da entrega.
