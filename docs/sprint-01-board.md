# Quadro local - Sprint 1: Fundação e API pesquisável

Este arquivo é um espelho inicial do GitHub Project. O quadro oficial deve ser criado no repositório remoto usando as mesmas colunas. Atualize o status somente com o trabalho efetivamente realizado.

**Branch de integração:** `sprint/01-fundacao-api`  
**Pontos planejados:** 60  
**Início real:** `PREENCHER`  
**Término real:** `PREENCHER`

| Status | Task | Responsável | Pontos | Issue | PR | Impedimento / observação |
| --- | --- | --- | ---: | --- | --- | --- |
| In Progress | SB-01 - Repositório, quadro ágil, Issues e modelos de PR | DEV-02 | 3 | `PREENCHER` | `PREENCHER` | Templates, branches e esqueletos de documentação publicados; falta criar Issue/Project, convidar membros, abrir PR e obter revisão. |
| Todo | SB-02 - Dicionários dos datasets e mapeamento de campos | DEV-01 | 5 | `PREENCHER` | `PREENCHER` | - |
| Todo | SB-03 - Schema e scripts PostgreSQL | DEV-01 | 5 | `PREENCHER` | `PREENCHER` | Depende de SB-02. |
| Todo | SB-04 - Extensão e índices de pesquisa | DEV-01 | 3 | `PREENCHER` | `PREENCHER` | Depende de SB-03. |
| Todo | SB-05 - ETL e importação de CSV | DEV-01 | 8 | `PREENCHER` | `PREENCHER` | Depende de SB-02 e SB-03. |
| Todo | SB-06 - API base e health check | DEV-02 | 5 | `PREENCHER` | `PREENCHER` | Depende de SB-03. |
| Todo | SB-07 - Filtros combinados | DEV-02 | 8 | `PREENCHER` | `PREENCHER` | Depende de SB-04 e SB-06. |
| Todo | SB-08 - Validação e paginação | DEV-02 | 5 | `PREENCHER` | `PREENCHER` | Depende de SB-07. |
| Todo | SB-09 - Gunicorn, timeout e rate limit | DEV-02 | 5 | `PREENCHER` | `PREENCHER` | Depende de SB-06. |
| Todo | SB-10 - Docker Compose e healthchecks | DEV-02 | 5 | `PREENCHER` | `PREENCHER` | Depende de SB-03 e SB-06. |
| Todo | SB-11 - Testes de API e segurança | DEV-02 | 8 | `PREENCHER` | `PREENCHER` | Depende de SB-07, SB-08 e SB-09. |

## Configuração obrigatória no GitHub Project

Crie um projeto chamado **ServidorBR - Sprint 1** e acrescente os campos:

| Campo | Tipo | Valores |
| --- | --- | --- |
| Status | Single select | Backlog, Todo, In Progress, Review, Done |
| Sprint | Single select | Sprint 1 |
| Responsável | Assignees | integrantes reais da equipe |
| Pontos | Number | estimativa da task |
| Impedimento | Text | bloqueio real e ação necessária |

Adicione as Issues SB-01 a SB-11 ao projeto e preencha os dados conforme esta tabela. Convide os dois outros integrantes ao repositório e configure nas regras de proteção de branch a exigência de uma aprovação antes de mesclar.
