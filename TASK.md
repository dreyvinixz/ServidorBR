# Tasks - ServidorBR

Quadro operacional das tasks da equipe. Os requisitos, critérios de aceite e especificações ficam no [ROADMAP.md](ROADMAP.md).

## Equipe

- DEV-01 - Guilherme Estrella (`@Shaarkegas`): Dados e Banco
- DEV-02 - `@dreyvinixz`: Líder técnico, Backend e DevOps/QA
- DEV-03 - `PREENCHER`: Frontend

## Regras rápidas

- Cada task tem uma Issue `SB-XX` e branch própria a partir da branch da sprint.
- Todo Pull Request exige a aprovação de pelo menos um revisor diferente do autor.
- O PR da task aponta para a branch da sprint; somente o PR da sprint aponta para `main`.
- Uma task só é marcada como concluída após PR aprovado, mesclado e testes aplicáveis passarem.

## Sprint 1 - Fundação e API pesquisável

**Branch:** `sprint/01-fundacao-api`

- [ ] **SB-01** - Repositório, quadro ágil, Issues e modelos de PR - DEV-02 - `chore/SB-01-estrutura-agil`
- [ ] **SB-02** - Analisar dicionários dos datasets e mapear campos - DEV-01 - `docs/SB-02-dicionario-dados`
- [ ] **SB-03** - Modelar schema e scripts de inicialização PostgreSQL - DEV-01 - `feat/SB-03-schema-postgres`
- [ ] **SB-04** - Criar `pg_trgm` e índices B-Tree/GIN - DEV-01 - `perf/SB-04-indices-pesquisa`
- [ ] **SB-05** - Construir ETL, validação e normalização dos CSVs - DEV-01 - `feat/SB-05-etl-importacao`
- [ ] **SB-06** - Criar Flask, SQLAlchemy, configuração e health check - DEV-02 - `feat/SB-06-api-base-health`
- [ ] **SB-07** - Implementar busca e filtros combinados - DEV-02 - `feat/SB-07-api-filtros`
- [ ] **SB-08** - Validar parâmetros, paginação e erros JSON - DEV-02 - `feat/SB-08-validacao-paginacao`
- [ ] **SB-09** - Configurar Gunicorn, timeout e rate limiting - DEV-02 - `feat/SB-09-protecao-api`
- [ ] **SB-10** - Dockerfiles, Compose, healthchecks e `.env.example` - DEV-02 - `chore/SB-10-docker-compose`
- [ ] **SB-11** - Testes de API, validação e SQL injection - DEV-02 - `test/SB-11-api-seguranca`

## Sprint 2 - Experiência web, desempenho e entrega

**Branch:** `sprint/02-experiencia-entrega`

- [ ] **SB-12** - Busca por similaridade via `pg_trgm` - DEV-02 - `feat/SB-12-busca-similaridade`
- [ ] **SB-13** - Estrutura React, layout e responsividade - DEV-03 - `feat/SB-13-layout-react`
- [ ] **SB-14** - Formulário de filtros e consumo da API - DEV-03 - `feat/SB-14-formulario-busca`
- [ ] **SB-15** - Lista, detalhes, paginação e estados de interface - DEV-03 - `feat/SB-15-resultados-paginacao`
- [ ] **SB-16** - Proxy Nginx e integração frontend-backend - DEV-02 - `feat/SB-16-proxy-integracao`
- [ ] **SB-17** - Cenários de carga e coleta de métricas reais - DEV-02 - `test/SB-17-carga`
- [ ] **SB-18** - Otimizar consultas e registrar limitações - DEV-01 - `perf/SB-18-otimizacao-consultas`
- [ ] **SB-19** - Pipeline de CI para testes e build - DEV-02 - `ci/SB-19-pipeline`
- [ ] **SB-20** - Documentação técnica, relatório e burndown real - DEV-02 - `docs/SB-20-relatorio-final`
- [ ] **SB-21** - Checklist, regressão e preparação da entrega - DEV-02 - `chore/SB-21-entrega-final`
