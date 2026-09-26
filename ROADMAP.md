# Roadmap de Desenvolvimento - ServidorBR

## 1. Propósito e regra de execução

Este documento é o plano de trabalho oficial do projeto **ServidorBR**. Ele organiza o desenvolvimento em duas sprints de 15 dias, com tarefas previamente atribuídas, critérios de aceite e entregáveis verificáveis.

> Importante: este plano não substitui o trabalho real. Commits, pull requests e mudanças de status devem ser registrados somente na data em que acontecerem e pela conta GitHub da pessoa responsável. Não criar commits retroativos ou simular atividade anterior.

## 2. Visão do produto

ServidorBR é uma aplicação web para consulta de dados públicos de servidores ativos e aposentados do Poder Executivo Federal. A pessoa usuária poderá pesquisar por nome, similaridade de nome, cargo/profissão, UF e órgão/instituição, combinar filtros e navegar pelos resultados paginados.

### Arquitetura prevista

```text
Navegador
    |
    v
Frontend (React + Vite + Nginx) --- /api ---> Backend (Flask + Gunicorn)
                                                    |
                                                    v
                                       PostgreSQL + pg_trgm (container db)
```

Os serviços obrigatórios serão `frontend`, `backend` e `db`, iniciados na raiz com `docker compose up --build`.

## 3. Equipe e responsabilidades

Os nomes devem ser preenchidos antes do início da Sprint 1. Os papéis não impedem colaboração ou revisão cruzada; definem a responsabilidade principal e a autoria esperada dos commits.

| Papel | Integrante | Responsabilidade principal |
| --- | --- | --- |
| Líder técnico / Backend / DevOps / QA | `@dreyvinixz` | Arquitetura, API Flask, integrações, Docker, CI, testes, carga, revisão técnica e acompanhamento diário. |
| Dados / Banco | `Guilherme` | Dicionário de dados, ETL, PostgreSQL, normalização e índices. |
| Frontend | `PREENCHER` | Interface React, experiência responsiva e consumo exclusivo da API. |

O nome e o usuário GitHub do integrante de Frontend devem ser preenchidos antes do início da Sprint 1. A colaboração e a revisão cruzada continuam permitidas, mas a autoria dos commits deve refletir o trabalho efetivamente realizado por cada pessoa.

## 4. Processo ágil e rastreabilidade

- Criar uma Issue para cada item identificado como `SB-XX` neste roadmap.
- Preencher em cada Issue: responsável, estimativa, descrição, critérios de aceite, dependências e evidências.
- Usar o fluxo `Backlog -> Todo -> In Progress -> Review -> Done`.
- Desenvolver em branch curta vinculada à Issue, por exemplo `feat/SB-06-api-filters`.
- Abrir Pull Request para mudanças significativas. Pelo menos uma revisão por outro integrante é recomendada antes de mesclar.
- Registrar diariamente no quadro o status, o impedimento e os pontos restantes; esses registros alimentam o burndown real.

### Padrão de commits

```text
tipo(escopo): resumo objetivo [SB-XX]
```

Tipos permitidos: `feat`, `fix`, `test`, `docs`, `chore`, `refactor`, `perf`.

Exemplos:

```text
feat(api): add validated UF filter [SB-06]
feat(db): create trigram index for normalized names [SB-04]
test(api): cover invalid pagination parameters [SB-08]
docs: document Docker startup flow [SB-14]
```

Um commit deve conter uma alteração coesa e funcionalmente verificável. A Issue só é concluída quando cumprir a definição de pronto.

## 5. Definição de pronto

Uma tarefa só pode ir para `Done` quando:

1. a implementação estiver integrada à branch de desenvolvimento;
2. os critérios de aceite estiverem atendidos;
3. os testes aplicáveis passarem;
4. não houver segredo ou credencial no código;
5. a documentação afetada for atualizada;
6. a Issue, o PR e os commits estiverem vinculados entre si;
7. houver evidência da validação (log, teste, captura ou relatório).

## 6. Sprint 1 - Fundação e API pesquisável

**Objetivo:** deixar a stack executável, o banco preparado e a API capaz de realizar buscas validadas, paginadas e seguras.

**Período planejado:** dias 1 a 15 do calendário da equipe (preencher datas reais ao iniciar).

**Meta de aceite:** `docker compose up --build` sobe os três serviços; a API em Gunicorn responde `GET /api/health` e executa filtros por nome, cargo, UF e órgão com paginação e validação.

| ID | Tarefa | Resp. | Pontos | Dependência | Critérios de aceite |
| --- | --- | --- | ---: | --- | --- |
| SB-01 | Criar repositório, quadro ágil, templates de Issue/PR e estrutura inicial | Líder técnico | 3 | - | Estrutura versionada; Issues criadas; membros e papéis registrados. |
| SB-02 | Analisar os dicionários dos dois datasets oficiais e mapear campos | Dados / Banco | 5 | - | Documento indica origem, campo, tipo, uso e tratamento de cada dado importado. |
| SB-03 | Modelar schema PostgreSQL e scripts de inicialização | Dados / Banco | 5 | SB-02 | Tabelas, chaves, normalizados e volume persistente definidos em SQL. |
| SB-04 | Criar índices B-Tree, GIN e extensão `pg_trgm` | Dados / Banco | 3 | SB-03 | Índices para nome, cargo, UF, órgão e busca parcial; script idempotente. |
| SB-05 | Implementar ETL de CSV com validação e normalização | Dados / Banco | 8 | SB-02, SB-03 | Lê CSVs de `db/data`, remove/trata inválidos, normaliza texto e importa com relatório. |
| SB-06 | Criar API Flask, configuração SQLAlchemy e endpoint de health | Líder técnico | 5 | SB-03 | `GET /api/health` retorna JSON e identifica indisponibilidade do banco com segurança. |
| SB-07 | Implementar repositório/serviço de busca e filtros combinados | Líder técnico | 8 | SB-04, SB-06 | Nome, cargo, UF e órgão são combináveis; consultas são parametrizadas. |
| SB-08 | Implementar validações, paginação e contrato de erros | Líder técnico | 5 | SB-07 | UF, páginas, limites, strings vazias/longas e parâmetros desconhecidos retornam erro JSON 400. |
| SB-09 | Configurar Gunicorn, timeouts, rate limiting e handlers seguros | Líder técnico | 5 | SB-06 | Backend usa workers/threads, retorna 429 no excesso e não expõe stack traces. |
| SB-10 | Criar Dockerfiles, Compose, healthchecks e variáveis de ambiente | DevOps / QA | 5 | SB-03, SB-06 | Os três containers sobem pela raiz; backend usa host `db`; volume do Postgres persiste dados. |
| SB-11 | Criar testes de API, validação e segurança da Sprint 1 | DevOps / QA | 8 | SB-07, SB-08, SB-09 | Cobertura para filtros, paginação, UF inválida, parâmetros desconhecidos e payloads de SQL injection. |

**Total planejado da Sprint 1: 60 pontos.**

### Roteiro diário sugerido - Sprint 1

| Dia | Foco | Entregável esperado |
| ---: | --- | --- |
| 1 | SB-01 | Quadro, papéis, repositório e backlog disponíveis. |
| 2-3 | SB-02 | Mapeamento do dicionário de dados revisado. |
| 4-5 | SB-03 e SB-04 | Schema, extensões e índices revisados. |
| 6-8 | SB-05 | ETL executado contra arquivo de amostra e relatório gerado. |
| 6-9 | SB-06 | Esqueleto Flask, health check e conexão configurados. |
| 9-11 | SB-07 e SB-08 | Filtros, paginação e validações funcionais. |
| 12 | SB-09 | Gunicorn, rate limit e timeout configurados. |
| 13 | SB-10 | Stack inicializa via Docker Compose. |
| 14-15 | SB-11 | Testes, correções e demonstração de encerramento. |

## 7. Sprint 2 - Experiência web, desempenho e entrega

**Objetivo:** oferecer uma interface completa, implementar a similaridade, testar concorrência e concluir documentação/evidências.

**Período planejado:** dias 16 a 30 do calendário da equipe (preencher datas reais ao iniciar).

**Meta de aceite:** a pessoa usuária faz qualquer busca exigida pelo enunciado pelo frontend; a API é testada sob carga e a documentação permite reproduzir a execução.

| ID | Tarefa | Resp. | Pontos | Dependência | Critérios de aceite |
| --- | --- | --- | ---: | --- | --- |
| SB-12 | Implementar busca por similaridade com `pg_trgm` | Dados / Banco + Líder técnico | 5 | SB-04, SB-07 | Aceita padrões parciais, limita a 100 registros e usa consulta/indexação adequada. |
| SB-13 | Criar estrutura React, design system e layout responsivo | Frontend | 8 | SB-10 | Aplicação abre em desktop e celular com header, área de busca e acessibilidade básica. |
| SB-14 | Implementar formulário e consumo exclusivo da API | Frontend | 8 | SB-07, SB-13 | Campos nome, cargo, UF, órgão e similaridade enviam query strings corretas. |
| SB-15 | Implementar resultados, detalhes, paginação e estados de UI | Frontend | 8 | SB-08, SB-14 | Exibe registro único detalhado e lista múltipla; tem loading, vazio, erro, timeout e 429. |
| SB-16 | Configurar proxy Nginx e integração frontend-backend | Frontend + DevOps / QA | 3 | SB-10, SB-14 | Browser acessa `/api` pelo frontend sem dependência de URL local do backend. |
| SB-17 | Criar cenários de carga e medir resultados | DevOps / QA | 5 | SB-09, SB-12 | Cenários concorrentes documentam RPS, média, P50/P95/P99, erros, timeout, CPU e RAM. |
| SB-18 | Otimizar consultas e registrar limitações reais | Dados / Banco + Líder técnico | 5 | SB-17 | Ajustes são justificados com medições; limitações não são ocultadas. |
| SB-19 | Configurar CI para testes e build | DevOps / QA | 3 | SB-11, SB-16 | Pipeline executa testes e valida construção dos serviços. |
| SB-20 | Produzir documentação técnica e relatório final | Líder técnico + todos | 5 | SB-18, SB-19 | README, arquitetura, API, ETL, segurança, carga, tarefas, burndown e limitações completos. |
| SB-21 | Executar checklist final e preparar pacote de entrega | DevOps / QA | 3 | SB-20 | Build limpo, smoke tests e checklist de aceitação anexados à release. |

**Total planejado da Sprint 2: 53 pontos.**

### Roteiro diário sugerido - Sprint 2

| Dia | Foco | Entregável esperado |
| ---: | --- | --- |
| 16-17 | SB-12 | Endpoint de similaridade testado. |
| 16-19 | SB-13 | Shell visual responsivo concluído. |
| 19-22 | SB-14 e SB-15 | Busca, lista, detalhes, paginação e estados visuais. |
| 22 | SB-16 | Integração Nginx/API validada em containers. |
| 23-24 | SB-17 | Relatório de carga inicial com métricas medidas. |
| 25 | SB-18 | Melhorias de desempenho comprovadas. |
| 26 | SB-19 | CI funcional. |
| 27-28 | SB-20 | Documentação e evidências consolidadas. |
| 29-30 | SB-21 | Regressão, build final e entrega. |

## 8. Especificações técnicas

### 8.1 Contrato da API

`GET /api/servidores` aceitará os parâmetros opcionais abaixo. Filtros presentes serão combinados com `AND`.

| Parâmetro | Tipo/regra | Exemplo |
| --- | --- | --- |
| `nome` | texto normalizado, 1 a 120 caracteres | `JOAO DA SILVA` |
| `similar` | texto parcial, 2 a 120 caracteres | `JOAO%SILVA` |
| `cargo` | texto, 1 a 120 caracteres | `PROFESSOR` |
| `uf` | uma UF brasileira válida | `RS` |
| `orgao` | texto, 1 a 160 caracteres | `UNIVERSIDADE` |
| `page` | inteiro >= 1; padrão 1 | `2` |
| `per_page` | inteiro de 1 a 100; padrão 25 | `25` |
| `limit` | inteiro de 1 a 100, apenas na similaridade | `100` |

Resposta de sucesso:

```json
{
  "data": [{"id": 1, "nome": "JOAO DA SILVA", "cargo": "PROFESSOR", "uf": "RS", "orgao": "UNIVERSIDADE FEDERAL"}],
  "pagination": {"page": 1, "per_page": 25, "total": 1, "pages": 1},
  "query_time_ms": 12
}
```

Resposta de erro:

```json
{
  "error": {"code": "INVALID_UF", "message": "UF inválida."}
}
```

| Situação | HTTP |
| --- | ---: |
| Consulta válida, inclusive sem resultado | 200 |
| Parâmetro inválido | 400 |
| Rota inexistente | 404 |
| Excesso de requisições | 429 |
| Timeout da consulta | 503 |
| Falha inesperada | 500 |

### 8.2 Dados e segurança

- Os CSVs oficiais serão tratados pelo ETL antes da importação.
- Campos pesquisáveis manterão versão normalizada: sem acentos, em maiúsculas, com espaços internos reduzidos e sem espaços nas extremidades.
- Todas as consultas terão parâmetros vinculados; valores de usuário nunca serão concatenados em SQL.
- PostgreSQL usará `pg_trgm`, índice GIN para busca textual e índices B-Tree para filtros frequentes.
- O backend limitará paginação/resultados, aplicará rate limiting e timeout de consulta.
- Credenciais existirão apenas no ambiente local/deploy e serão documentadas em `.env.example`; `.env` será ignorado pelo Git.

### 8.3 Interface

- Tela inicial com busca principal e filtros avançados: nome, cargo, UF, órgão e similaridade.
- Resultados em tabela/lista acessível com nome, cargo, UF e órgão.
- Um resultado: cartão/painel detalhado. Vários: lista paginada.
- Estados explícitos: carregando, sucesso, nenhum resultado, parâmetro inválido, limite de requisições e timeout.
- Layout responsivo para largura de celular, tablet e desktop.

## 9. Documentação e evidências exigidas

| Documento | Responsável inicial | Conteúdo mínimo | Quando atualizar |
| --- | --- | --- | --- |
| `README.md` | Líder técnico | propósito, pré-requisitos, execução, testes e URLs | a cada mudança de operação |
| `ROADMAP.md` | Líder técnico | sprints, tarefas, papéis e critérios | início e fechamento de cada sprint |
| `docs/arquitetura.md` | Líder técnico | diagrama, serviços, rede, variáveis e decisões | quando arquitetura mudar |
| `docs/dados-e-etl.md` | Dados / Banco | fontes, dicionário, mapeamento e tratamento | após SB-02/SB-05 |
| `docs/api.md` | Líder técnico | endpoints, parâmetros, erros e exemplos | após mudança de contrato |
| `docs/seguranca.md` | Líder técnico | validações, injeção SQL, rate limit e timeout | após SB-09 |
| `docs/testes-e-carga.md` | DevOps / QA | estratégia, comandos, métricas reais e conclusões | após SB-11/SB-17 |
| `docs/relatorio-final.md` | Todos | divisão real, commits, burndown, dificuldades e limitações | continuamente; concluir na SB-20 |

## 10. Burndown e acompanhamento diário

Pontos totais planejados: **113**. O burndown não deve conter valores previstos como se fossem concluídos. A pessoa líder registra diariamente apenas os pontos que continuam abertos no fim do dia.

Modelo de registro em `docs/burndown.csv`:

```csv
data,sprint,pontos_planejados_restantes,pontos_reais_restantes,observacao
AAAA-MM-DD,1,60,60,Inicio da sprint
AAAA-MM-DD,1,56,60,Impedimento: aguardando dicionario de dados
```

## 11. Checklist de aceite para a entrega

- [ ] Equipe com 3 ou 4 integrantes, cada pessoa com histórico real no GitHub.
- [ ] Duas sprints/30 dias registradas com quadro, responsáveis, estimativas e impedimentos.
- [ ] `docker compose up --build` inicia `frontend`, `backend` e `db`.
- [ ] Backend usa Flask com Gunicorn e concorrência configurada.
- [ ] PostgreSQL persiste dados em volume e usa índices/documentação de ETL.
- [ ] API JSON possui filtros, combinação, similaridade, paginação e healthcheck.
- [ ] Parâmetros inválidos, SQL injection, sobrecarga e timeout são tratados com respostas seguras.
- [ ] Frontend consome apenas a API e atende a todos os estados previstos.
- [ ] Testes funcionais, validação, segurança e carga foram executados e documentados com resultados reais.
- [ ] Relatório final tem divisão das tarefas, evidências de GitHub, burndown, pontos fortes/fracos, dificuldades, impedimentos e limitações.
