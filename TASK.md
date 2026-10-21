# Tasks - ServidorBR

Quadro operacional das tasks da equipe. Os requisitos, critérios de aceite e especificações ficam no [ROADMAP.md](ROADMAP.md).

## Equipe

- `@dreyvinixz`: desenvolvimento individual, incluindo dados, backend, frontend, DevOps e QA.

## Estado da implementação local - 20/10/2026

- A `main` está em `212ec69`; o reparo FULL e os filtros pesquisáveis foram integrados pelo PR [#46](https://github.com/dreyvinixz/ServidorBR/pull/46), vinculado à Issue [#44](https://github.com/dreyvinixz/ServidorBR/issues/44).
- O banco local contém 414.801 registros. O reparo FULL foi validado com backup reversível de 413.990 linhas; veja [`docs/reparo-campos-full-202508.md`](docs/reparo-campos-full-202508.md).
- A interface oferece 1.479 cargos e 183 órgãos distintos por seletores pesquisáveis; `npm run build` e os 15 testes do backend passaram. A inspeção visual automatizada ficou pendente porque não havia navegador disponível no ambiente.
- O app desktop para o ponto adicional está em desenvolvimento na branch `feat/SB-29-desktop-app`, Issue [#45](https://github.com/dreyvinixz/ServidorBR/issues/45); ainda não conte como concluído.
- A autoria do trabalho é individual. O requisito acadêmico de três ou quatro participantes continua não atendido; não atribuir autoria ou histórico a outras pessoas.
- O prazo do enunciado era 13/10/2026; esta implementação iniciou em 20/10/2026.

## Regras rápidas

- Cada task deve ter uma Issue `SB-XX` e branch própria criada a partir de `main` no fluxo solo atual.
- Cada alteração é integrada por Pull Request para `main`; o check obrigatório `backend` precisa passar.
- Revisão independente é recomendada quando houver outro colaborador disponível; não simular aprovação em trabalho solo.
- `main` continua protegida contra force push e exclusão e exige branches atualizadas.
- Uma task só é marcada como concluída após PR aprovado, mesclado e testes aplicáveis passarem.

## Sprint 1 - Fundação e API pesquisável

**Branch:** `sprint/01-fundacao-api`

- [ ] **SB-01** - Repositório, quadro ágil, Issues e modelos de PR - DEV-02 - `chore/SB-01-estrutura-agil`
- [ ] **SB-02** - Analisar dicionários dos datasets e mapear campos - DEV-01 - `docs/SB-02-dicionario-dados`
- [ ] **SB-03** - Modelar schema e scripts de inicialização PostgreSQL - DEV-01 - `feat/SB-03-schema-postgres`
- [ ] **SB-04** - Criar `pg_trgm` e índices B-Tree/GIN - DEV-01 - `perf/SB-04-indices-pesquisa`
- [x] **SB-05** - Construir ETL, validação e normalização dos CSVs - `dreyvinixz` (solo) - PRs [#21](https://github.com/dreyvinixz/ServidorBR/pull/21) e [#24](https://github.com/dreyvinixz/ServidorBR/pull/24); evidência em [`docs/dados-e-etl.md`](docs/dados-e-etl.md)
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

## Melhorias do produto

- [x] **SB-22** - Modernizar frontend com React, Vite e Tailwind CSS 4 - `dreyvinixz` (solo) - Issue [#35](https://github.com/dreyvinixz/ServidorBR/issues/35), PR [#36](https://github.com/dreyvinixz/ServidorBR/pull/36)
- [x] **SB-24** - Melhorar usabilidade das opções avançadas de busca - `dreyvinixz` (solo) - Issue [#40](https://github.com/dreyvinixz/ServidorBR/issues/40), PR [#41](https://github.com/dreyvinixz/ServidorBR/pull/41)
- [x] **SB-25** - Corrigir mapeamento dos cabeçalhos do CSV FULL - `dreyvinixz` (solo) - Issue [#42](https://github.com/dreyvinixz/ServidorBR/issues/42), PR [#43](https://github.com/dreyvinixz/ServidorBR/pull/43)
- [x] **SB-28** - Recuperar cargo/órgão no FULL e melhorar filtros pesquisáveis - `dreyvinixz` (solo) - Issue [#44](https://github.com/dreyvinixz/ServidorBR/issues/44), PR [#46](https://github.com/dreyvinixz/ServidorBR/pull/46)
- [ ] **SB-29** - Aplicativo desktop com interface gráfica (ponto adicional) - `dreyvinixz` (solo) - Issue [#45](https://github.com/dreyvinixz/ServidorBR/issues/45)
