# API - ServidorBR

Base URL local: `http://localhost:3000/api` (através do proxy Nginx). Todas as respostas usam JSON UTF-8.

## Saúde

`GET /health` verifica a conectividade com o PostgreSQL.

Sucesso HTTP 200: `{"status":"ok","database":"ok"}`. Falha de banco: HTTP 503, `DATABASE_UNAVAILABLE`.

## Pesquisa

`GET /servidores` combina filtros informados com `AND`.

| Parâmetro | Regra |
|---|---|
| `nome` | Exato após normalização; 1-120 caracteres |
| `similar` | Trigramas + padrão parcial; 2-120 caracteres |
| `cargo` | Contém trecho; 1-120 caracteres |
| `orgao` | Contém trecho; 1-160 caracteres |
| `uf` | UF inválida -> 400; UF válida -> 422 `UF_UNAVAILABLE`, pois o arquivo de aposentados não contém UF |
| `page` | Inteiro de 1 a 1.000.000; padrão 1; página além do total retorna 400 quando há resultados |
| `per_page` | Inteiro entre 1 e 100; padrão 25 |
| `limit` | Máximo global de resultados para `similar`; inteiro entre 1 e 100; padrão 100. A última página pode conter menos de `per_page` itens para não ultrapassar esse teto. |

Exemplos:

```http
GET /api/servidores?nome=JOAO%20DA%20SILVA
GET /api/servidores?cargo=PROFESSOR&orgao=UNIVERSIDADE&per_page=25
GET /api/servidores?similar=JOAO%25SILVA&limit=100
```

Resposta:

```json
{"data":[{"id":1,"nome":"JOAO DA SILVA","cargo":"PROFESSOR","orgao":"UNIVERSIDADE FEDERAL","uf":null}],"pagination":{"page":1,"per_page":25,"total":1,"pages":1},"query_time_ms":4.2}
```

Na busca similar, `total` e páginas são limitados ao `limit`; `per_page` define o tamanho da página dentro desse teto.

## Erros

| HTTP | Códigos/situações |
|---:|---|
| 400 | `UNKNOWN_PARAMETER`, `INVALID_QUERY`, `INVALID_PAGINATION`, `INVALID_PAGE`, `INVALID_UF` |
| 404 | `NOT_FOUND` |
| 422 | `UF_UNAVAILABLE` |
| 429 | `RATE_LIMITED` |
| 503 | `DATABASE_UNAVAILABLE`, `QUERY_TIMEOUT` |
| 500 | `INTERNAL_ERROR`, sem detalhes internos |

Consultas usam parâmetros vinculados pelo Psycopg. Nomes de colunas e fragmentos de ordenação são constantes definidas no backend. CPF e matrícula não são retornados.
