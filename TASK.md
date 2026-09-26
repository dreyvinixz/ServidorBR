# Tasks da Equipe - ServidorBR

Este documento transforma o planejamento do [`ROADMAP.md`](ROADMAP.md) em tarefas atribuídas a uma equipe de **três desenvolvedores**. A divisão principal é fixa; colaboração e revisão cruzada não alteram a autoria real dos commits.

| Código | Integrante | GitHub | Responsabilidade principal |
| --- | --- | --- | --- |
| DEV-01 | `Guilherme` | `PREENCHER` | Dados e Banco |
| DEV-02 | `PREENCHER` | `@dreyvinixz` | Líder técnico, Backend e DevOps/QA |
| DEV-03 | `PREENCHER` | `@PREENCHER` | Frontend |

O responsável é quem executa e cria os commits principais; o apoio pode colaborar e revisar, sem substituir a autoria real.

## Regras obrigatórias de Git e Pull Request

1. Cada sprint será desenvolvida em uma branch de integração exclusiva:
   - Sprint 1: `sprint/01-fundacao-api`
   - Sprint 2: `sprint/02-experiencia-entrega`
2. Nenhuma task é iniciada diretamente em `main`. Cada task deve ter branch própria criada a partir da branch da sprint, por exemplo: `feat/SB-07-api-filtros`.
3. Todo Pull Request deve apontar para a branch da sprint correspondente. Somente ao final da sprint, a branch da sprint poderá abrir PR para `main`.
4. Cada Pull Request exige a aprovação de **pelo menos um revisor diferente do autor**. O autor não pode aprovar nem mesclar o próprio PR sem uma aprovação externa.
5. O revisor deve verificar critérios de aceite, testes, segurança, documentação e se os commits estão vinculados à Issue (`SB-XX`).
6. Não mesclar Pull Requests com testes falhando, conflitos não resolvidos ou segredos expostos.
7. Cada task possui uma Issue antes do primeiro commit. O PR deve conter `Closes #<numero-da-issue>`.
8. Commits devem seguir `tipo(escopo): resumo [SB-XX]`, por exemplo: `feat(api): add UF filter [SB-07]`.

## Fluxo de branches

```text
main
  ├─ sprint/01-fundacao-api
  │    ├─ feat/SB-03-schema-postgres
  │    ├─ feat/SB-07-api-filtros
  │    └─ test/SB-11-api-seguranca
  │
  └─ sprint/02-experiencia-entrega
       ├─ feat/SB-12-similaridade
       ├─ feat/SB-14-formulario-busca
       └─ test/SB-17-carga
```

## Sprint 1 - Fundação e API pesquisável

**Branch de integração:** `sprint/01-fundacao-api`  
**Objetivo:** preparar dados, infraestrutura e API segura com filtros e paginação.

| Task | Descrição | Responsável | Apoio / revisor preferencial | Branch | Pontos | Critério resumido |
| --- | --- | --- | --- | --- | ---: | --- |
| SB-01 | Repositório, quadro ágil, Issues e modelos de PR | DEV-02 | DEV-01 | `chore/SB-01-estrutura-agil` | 3 | Quadro e templates disponíveis; papéis registrados. |
| SB-02 | Analisar dicionários dos datasets e mapear campos | DEV-01 | DEV-02 | `docs/SB-02-dicionario-dados` | 5 | Fonte, campo, tipo e tratamento documentados. |
| SB-03 | Modelar schema e scripts de inicialização PostgreSQL | DEV-01 | DEV-03 | `feat/SB-03-schema-postgres` | 5 | Tabelas, chaves e persistência definidos. |
| SB-04 | Criar `pg_trgm` e índices B-Tree/GIN | DEV-01 | DEV-02 | `perf/SB-04-indices-pesquisa` | 3 | Índices idempotentes para todos os filtros. |
| SB-05 | Construir ETL, validação e normalização dos CSVs | DEV-01 | DEV-03 | `feat/SB-05-etl-importacao` | 8 | Importa CSV, trata inválidos e gera relatório. |
| SB-06 | Criar Flask, SQLAlchemy, configuração e health check | DEV-02 | DEV-03 | `feat/SB-06-api-base-health` | 5 | Health retorna JSON e banco é tratado com segurança. |
| SB-07 | Implementar busca e filtros combinados parametrizados | DEV-02 | DEV-01 | `feat/SB-07-api-filtros` | 8 | Nome, cargo, UF e órgão funcionam combinados. |
| SB-08 | Validar parâmetros, paginação e erros JSON | DEV-02 | DEV-03 | `feat/SB-08-validacao-paginacao` | 5 | Entradas inválidas retornam 400 padronizado. |
| SB-09 | Configurar Gunicorn, timeout e rate limiting | DEV-02 | DEV-01 | `feat/SB-09-protecao-api` | 5 | Há concorrência, 429 e tratamento seguro de timeout. |
| SB-10 | Dockerfiles, Compose, healthchecks e `.env.example` | DEV-02 | DEV-03 | `chore/SB-10-docker-compose` | 5 | Três serviços sobem com `docker compose up --build`. |
| SB-11 | Testes de API, validação e SQL injection | DEV-02 | DEV-01 | `test/SB-11-api-seguranca` | 8 | Testes de filtros e payloads maliciosos passam. |

**Total: 60 pontos.**

### Aceite da Sprint 1

- [ ] Todos os PRs acima foram revisados e mesclados em `sprint/01-fundacao-api`.
- [ ] A branch da sprint passou por teste integrado com `docker compose up --build`.
- [ ] `GET /api/health` e os filtros nome, cargo, UF e órgão funcionam em JSON.
- [ ] Existe validação, paginação, rate limiting, timeout e teste de SQL injection.
- [ ] O PR `sprint/01-fundacao-api -> main` possui pelo menos um revisor e está aprovado.

## Sprint 2 - Experiência web, desempenho e entrega

**Branch de integração:** `sprint/02-experiencia-entrega`  
**Objetivo:** entregar busca por similaridade, interface responsiva, carga, documentação e pacote de entrega.

| Task | Descrição | Responsável | Apoio / revisor preferencial | Branch | Pontos | Critério resumido |
| --- | --- | --- | --- | --- | ---: | --- |
| SB-12 | Busca por similaridade via `pg_trgm` com limite máximo | DEV-02 | DEV-01 | `feat/SB-12-busca-similaridade` | 5 | Busca parcial retorna no máximo 100 resultados. |
| SB-13 | Estrutura React, layout e responsividade | DEV-03 | DEV-02 | `feat/SB-13-layout-react` | 8 | Tela principal funciona em celular e desktop. |
| SB-14 | Formulário de filtros e consumo exclusivo da API | DEV-03 | DEV-02 | `feat/SB-14-formulario-busca` | 8 | Todos os filtros geram chamadas HTTP corretas. |
| SB-15 | Lista, detalhes, paginação e estados de interface | DEV-03 | DEV-02 | `feat/SB-15-resultados-paginacao` | 8 | Loading, vazio, erro, timeout e 429 são exibidos. |
| SB-16 | Proxy Nginx e integração frontend-backend | DEV-02 | DEV-03 | `feat/SB-16-proxy-integracao` | 3 | Frontend acessa a API por `/api` em containers. |
| SB-17 | Cenários de carga e coleta de métricas reais | DEV-02 | DEV-01 | `test/SB-17-carga` | 5 | RPS, latências, erros, CPU e RAM documentados. |
| SB-18 | Otimizar consultas e registrar limitações | DEV-01 | DEV-02 | `perf/SB-18-otimizacao-consultas` | 5 | Decisões justificadas por resultados medidos. |
| SB-19 | Pipeline de CI para testes e build | DEV-02 | DEV-03 | `ci/SB-19-pipeline` | 3 | Pipeline executa testes e build sem falhas. |
| SB-20 | Documentação técnica, relatório e burndown real | DEV-02 | DEV-01 | `docs/SB-20-relatorio-final` | 5 | Todos os documentos e evidências reais estão completos. |
| SB-21 | Checklist, regressão e preparação da entrega | DEV-02 | DEV-03 | `chore/SB-21-entrega-final` | 3 | Build limpo e checklist de aceite concluído. |

**Total: 53 pontos.**

### Aceite da Sprint 2

- [ ] Todos os PRs foram revisados e mesclados em `sprint/02-experiencia-entrega`.
- [ ] Frontend atende a todas as buscas e estados exigidos.
- [ ] Similaridade, paginação, carga e CI foram validados com resultados reais.
- [ ] Documentação, burndown e relatório final foram atualizados.
- [ ] O PR `sprint/02-experiencia-entrega -> main` possui pelo menos um revisor e está aprovado.

## Checklist de revisão de Pull Request

O revisor registra no PR quais itens conferiu:

- [ ] A Issue `SB-XX` está vinculada e seus critérios de aceite foram cumpridos.
- [ ] O código não inclui credenciais, dados sensíveis ou arquivos gerados indevidos.
- [ ] Entradas do usuário são validadas e não há SQL montado por concatenação.
- [ ] Os testes relevantes foram adicionados/atualizados e passam.
- [ ] A implementação não quebra Docker Compose nem o contrato da API.
- [ ] A documentação foi atualizada quando necessária.
- [ ] A alteração é compreensível, coesa e está pronta para mesclagem.

## Registro diário por integrante

Cada pessoa atualiza uma linha por dia útil no quadro da sprint ou no relatório. Use somente fatos verificáveis.

| Data | Dev | Task | Status | Commit/PR | Impedimento | Próxima ação |
| --- | --- | --- | --- | --- | --- | --- |
| AAAA-MM-DD | DEV-01 | SB-02 | In Progress | `hash ou URL` | `nenhum ou descrição real` | Revisar campos de órgão. |
