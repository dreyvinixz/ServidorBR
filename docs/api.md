# API - ServidorBR

**Base URL prevista:** `http://localhost:8000/api`  
**Formato de resposta:** JSON  
**Status:** contrato inicial; confirmar ao concluir SB-06 a SB-12.

## Health check

```http
GET /api/health
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

## Pesquisa de servidores

```http
GET /api/servidores
```

| Parâmetro | Regra prevista | Exemplo |
| --- | --- | --- |
| `nome` | Texto de 1 a 120 caracteres | `JOAO DA SILVA` |
| `similar` | Texto parcial de 2 a 120 caracteres | `JOAO%SILVA` |
| `cargo` | Texto de 1 a 120 caracteres | `PROFESSOR` |
| `uf` | UF brasileira válida | `RS` |
| `orgao` | Texto de 1 a 160 caracteres | `UNIVERSIDADE` |
| `page` | Inteiro maior ou igual a 1 | `2` |
| `per_page` | Inteiro entre 1 e 100 | `25` |
| `limit` | Inteiro entre 1 e 100 para similaridade | `100` |

Exemplo de resposta de sucesso:

```json
{
  "data": [],
  "pagination": {"page": 1, "per_page": 25, "total": 0, "pages": 0},
  "query_time_ms": 0
}
```

## Erros previstos

| Situação | HTTP | Estrutura |
| --- | ---: | --- |
| Parâmetro inválido | 400 | `{"error":{"code":"...","message":"..."}}` |
| Rota inexistente | 404 | JSON de erro |
| Rate limit excedido | 429 | JSON de erro |
| Timeout de consulta | 503 | JSON de erro |
| Falha interna | 500 | JSON seguro, sem detalhes internos |

## Evidências pendentes

- [ ] Endpoints implementados e validados.
- [ ] Exemplos atualizados com respostas reais.
- [ ] Contrato revisado após integração do frontend.
