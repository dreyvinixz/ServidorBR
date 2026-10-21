# Tasks - ServidorBR

Quadro operacional das tasks da equipe. Os requisitos, critérios de aceite e especificações ficam no [ROADMAP.md](ROADMAP.md).

## Equipe

- `@dreyvinixz`: desenvolvimento individual, incluindo dados, backend, frontend, DevOps e QA.

## Estado integrado em `main` - 20/10/2026

- A `main` está em `96dfd30`; o reparo FULL e os filtros pesquisáveis foram integrados pelo PR [#46](https://github.com/dreyvinixz/ServidorBR/pull/46), vinculado à Issue [#44](https://github.com/dreyvinixz/ServidorBR/issues/44).
- O banco local contém 414.801 registros. O reparo FULL foi validado com backup reversível de 413.990 linhas; veja [`docs/reparo-campos-full-202508.md`](docs/reparo-campos-full-202508.md).
- A interface oferece 1.479 cargos e 183 órgãos distintos por seletores pesquisáveis; o build web e os 16 testes do backend passaram. A inspeção visual automatizada pelo navegador continua pendente porque o ambiente não oferece navegador.
- O aplicativo desktop da Issue [#45](https://github.com/dreyvinixz/ServidorBR/issues/45) foi integrado pelo PR [#47](https://github.com/dreyvinixz/ServidorBR/pull/47); os checks `backend`, `frontend` e `desktop` passaram e a issue foi fechada.
- A autoria do trabalho é individual. O requisito acadêmico de três ou quatro participantes continua não atendido; não atribuir autoria ou histórico a outras pessoas.
- O prazo do enunciado era 13/10/2026; esta implementação iniciou em 20/10/2026.

## Regras rápidas

- Cada task deve ter uma Issue `SB-XX` e branch própria criada a partir de `main` no fluxo solo atual.
- Cada alteração é integrada por Pull Request para `main`; o check obrigatório `backend` precisa passar.
- Revisão independente é recomendada quando houver outro colaborador disponível; não simular aprovação em trabalho solo.
- `main` continua protegida contra force push e exclusão e exige branches atualizadas.
- Uma task só é marcada como concluída após PR mesclado e checks/testes aplicáveis passarem; aprovação independente não é simulada no fluxo solo.

## Sprint 1 - Fundação e API pesquisável

**Branch:** `sprint/01-fundacao-api`

- [x] **SB-01** - Repositório, quadro ágil, Issues e modelos de PR - estrutura registrada no histórico de Issues/PRs e neste quadro.
- [x] **SB-02** - Analisar dicionários dos datasets e mapear campos - mapeamento e limitações em [`docs/dados-e-etl.md`](docs/dados-e-etl.md).
- [x] **SB-03** - Modelar schema e scripts de inicialização PostgreSQL - schema em `db/init.sql`.
- [ ] **SB-04** - Criar `pg_trgm` e índices B-Tree/GIN - índices para campos pesquisáveis existem; UF permanece indisponível porque a fonte usada não fornece esse campo.
- [x] **SB-05** - Construir ETL, validação e normalização dos CSVs - `dreyvinixz` (solo) - PRs [#21](https://github.com/dreyvinixz/ServidorBR/pull/21) e [#24](https://github.com/dreyvinixz/ServidorBR/pull/24); evidência em [`docs/dados-e-etl.md`](docs/dados-e-etl.md)
- [ ] **SB-06** - Criar Flask, SQLAlchemy, configuração e health check - Flask, configuração e health check estão implementados; a conexão usa psycopg, não SQLAlchemy.
- [ ] **SB-07** - Implementar busca e filtros combinados - nome, cargo, órgão e similaridade estão implementados; filtro de UF depende de uma fonte que contenha UF.
- [x] **SB-08** - Validar parâmetros, paginação e erros JSON - validações e erros JSON cobertos pelos testes do backend.
- [x] **SB-09** - Configurar Gunicorn, timeout e rate limiting - configuração e limites em `backend/Dockerfile` e `backend/app.py`.
- [x] **SB-10** - Dockerfiles, Compose, healthchecks e `.env.example` - stack de três serviços e healthchecks configurados.
- [x] **SB-11** - Testes de API, validação e SQL injection - suíte automatizada do backend.

## Sprint 2 - Experiência web, desempenho e entrega

**Branch:** `sprint/02-experiencia-entrega`

- [x] **SB-12** - Busca por similaridade via `pg_trgm` - endpoint e análise documentados em [`docs/analise-busca-similaridade.md`](docs/analise-busca-similaridade.md).
- [ ] **SB-13** - Estrutura React, layout e responsividade - interface React/Tailwind implementada; inspeção visual manual ainda pendente.
- [ ] **SB-14** - Formulário de filtros e consumo da API - nome, cargo, órgão e similaridade consomem a API; UF indisponível na fonte atual.
- [ ] **SB-15** - Lista, detalhes, paginação e estados de interface - lista, paginação e estados estão implementados; painel de detalhe individual e inspeção visual continuam pendentes.
- [x] **SB-16** - Proxy Nginx e integração frontend-backend - proxy configurado em `frontend/nginx.conf`.
- [x] **SB-17** - Cenários de carga e coleta de métricas reais - medições concorrentes e limitações registradas em [`docs/testes-e-carga.md`](docs/testes-e-carga.md).
- [x] **SB-18** - Otimizar consultas e registrar limitações - plano, custo de contagem e mudança limitada documentados em [`docs/analise-busca-similaridade.md`](docs/analise-busca-similaridade.md).
- [x] **SB-19** - Pipeline de CI para testes e build - workflow executa jobs de backend, frontend e empacotamento desktop Windows.
- [ ] **SB-20** - Documentação técnica, relatório e burndown real - documentação técnica e relatório estão atualizados; burndown histórico completo não foi reconstruído.
- [ ] **SB-21** - Checklist, regressão e preparação da entrega - validações automatizadas passaram; inspeção visual e critérios acadêmicos de equipe/prazo permanecem pendentes.

## Melhorias do produto

- [x] **SB-22** - Modernizar frontend com React, Vite e Tailwind CSS 4 - `dreyvinixz` (solo) - Issue [#35](https://github.com/dreyvinixz/ServidorBR/issues/35), PR [#36](https://github.com/dreyvinixz/ServidorBR/pull/36)
- [x] **SB-24** - Melhorar usabilidade das opções avançadas de busca - `dreyvinixz` (solo) - Issue [#40](https://github.com/dreyvinixz/ServidorBR/issues/40), PR [#41](https://github.com/dreyvinixz/ServidorBR/pull/41)
- [x] **SB-25** - Corrigir mapeamento dos cabeçalhos do CSV FULL - `dreyvinixz` (solo) - Issue [#42](https://github.com/dreyvinixz/ServidorBR/issues/42), PR [#43](https://github.com/dreyvinixz/ServidorBR/pull/43)
- [x] **SB-28** - Recuperar cargo/órgão no FULL e melhorar filtros pesquisáveis - `dreyvinixz` (solo) - Issue [#44](https://github.com/dreyvinixz/ServidorBR/issues/44), PR [#46](https://github.com/dreyvinixz/ServidorBR/pull/46)
- [x] **SB-29** - Aplicativo desktop com interface gráfica (ponto adicional) - `dreyvinixz` (solo) - Issue [#45](https://github.com/dreyvinixz/ServidorBR/issues/45), PR [#47](https://github.com/dreyvinixz/ServidorBR/pull/47); CI Windows passou.
