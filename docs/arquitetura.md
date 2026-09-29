# Arquitetura - ServidorBR

## Visão geral

O ServidorBR será composto por três serviços Docker:

```text
Navegador
    |
    v
frontend (React + Vite + Nginx) -- /api --> backend (Flask + Gunicorn)
                                                 |
                                                 v
                                      db (PostgreSQL + pg_trgm)
```

## Serviços

| Serviço | Responsabilidade | Tecnologia | Status |
| --- | --- | --- | --- |
| `frontend` | Interface de pesquisa e consumo da API | React, Vite, Nginx | Planejado - SB-13 a SB-16 |
| `backend` | API REST, validação, segurança e paginação | Python, Flask, Gunicorn, SQLAlchemy | Planejado - SB-06 a SB-12 |
| `db` | Persistência, índices e busca textual | PostgreSQL, `pg_trgm` | Planejado - SB-03 a SB-05 |

## Decisões técnicas

- O frontend consumirá somente endpoints HTTP do backend pelo prefixo `/api`.
- O backend acessará o banco pelo hostname interno `db`, jamais por `localhost` em ambiente Docker.
- A execução final será feita a partir da raiz: `docker compose up --build`.
- O PostgreSQL utilizará volume persistente, consultas parametrizadas e índices para campos pesquisáveis.
- O backend será iniciado por Gunicorn com workers/threads e não pelo servidor de desenvolvimento do Flask.

## Variáveis de ambiente previstas

| Variável | Uso | Valor real |
| --- | --- | --- |
| `POSTGRES_DB` | Nome do banco | Definir em `.env` |
| `POSTGRES_USER` | Usuário do banco | Definir em `.env` |
| `POSTGRES_PASSWORD` | Senha do banco | Definir em `.env`, nunca versionar |
| `DATABASE_URL` | Conexão do backend | Definir em `.env` |
| `API_PORT` | Porta da API | Definir na SB-10 |

## Evidências pendentes

- [ ] Diagrama revisado após implementação da SB-10.
- [ ] Saída de `docker compose up --build` registrada.
- [ ] Healthchecks e rede interna verificados.
