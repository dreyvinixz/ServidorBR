# Arquitetura - ServidorBR

## Topologia executável

```text
Navegador -> frontend (Nginx + HTML/CSS/JS) -> /api -> backend (Flask + Gunicorn) -> db (PostgreSQL + pg_trgm)
```

`docker-compose.yml` define a rede interna, volume persistente para PostgreSQL, healthchecks e ordem de inicialização. Somente o frontend publica uma porta no host; o backend é acessado por proxy Nginx.

## Serviços

| Serviço | Função | Porta | Saúde/persistência |
|---|---|---|---|
| `frontend` | Interface e proxy `/api` | host 3000 -> 80 | Nginx |
| `backend` | API REST e ETL | interna 8000 | healthcheck HTTP |
| `db` | Persistência e índices | interna 5432 | volume `postgres_data`, `pg_isready` |

## Configuração

| Variável | Padrão local | Uso |
|---|---|---|
| `POSTGRES_DB` | `servidorbr` | Banco |
| `POSTGRES_USER` | `servidorbr` | Usuário |
| `POSTGRES_PASSWORD` | `local-dev-only` | Senha local descartável |
| `WEB_PORT` | `3000` | Porta HTTP publicada |
| `RATE_LIMIT` | `120 per minute` | Limite por IP |

## Decisões e limites

- PostgreSQL 16 com `pg_trgm`; texto normalizado também possui índices B-Tree.
- Gunicorn usa 2 workers, 4 threads e timeout de 15 segundos. O PostgreSQL cancela uma consulta após 8 segundos.
- Rate limit reside em memória. Réplicas independentes não compartilham contadores; não é controle distribuído para produção.
- CSV não é incorporado à imagem nem montado por padrão. O operador fornece o arquivo no momento da importação.
- O SQL de inicialização é executado pelo entrypoint PostgreSQL somente quando o volume é criado. Atualizações futuras exigem migração explícita.
- A base inicia vazia. Nenhum CSV ou registro foi incluído no repositório.

## Evidência

`docker compose config -q` foi validado localmente. Ainda é necessário executar a stack completa com Docker e importar um CSV oficial para comprovar a integração com dados reais.
