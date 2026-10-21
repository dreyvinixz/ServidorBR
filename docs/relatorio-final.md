# Relatório de estado do projeto - ServidorBR

**Atualizado em:** 20/10/2026  
**Estado:** MVP integrado; análise local de consultas, benchmark concorrente e auditoria documental das fontes concluídos; entrega acadêmica ainda não aprovada.

## 1. Escopo disponível

O MVP reúne frontend estático, API Flask/Gunicorn, PostgreSQL com índices `pg_trgm`, ETL de CSV e Compose. Uma instalação nova começa com banco vazio e recebe dados por importação local. O volume local de desenvolvimento contém 414.801 registros de aposentados da competência 08/2025; os CSVs originais não foram incluídos no repositório.

## 2. Equipe e histórico verificável

O enunciado requer de três a quatro integrantes e distribuição real de tarefas/commits. `TASK.md` registra dois nomes e um integrante como `PREENCHER`; a autoria Git desta implementação é somente `dreyvinixz`. Não atribuir autoria, datas ou trabalho a integrantes sem evidência. A composição precisa ser confirmada pelo grupo antes da submissão.

O `main` remoto contém mais de 30 commits após integração dos PRs #13 a #30. A Issue [SB-05](https://github.com/dreyvinixz/ServidorBR/issues/12) foi fechada com a entrega do ETL oficial. O diário disponível em `docs/burndown.csv` termina em 26/09/2026 e não representa o trabalho executado em outubro; não foi reconstruído retroativamente.

## 3. Prazo e sprints

O enunciado define entrega limite em 13/10/2026. Esta implementação começou em 20/10/2026, depois do prazo. O quadro original registra Sprint 1 desde 25/09 e acompanhamento somente até 26/09. Não há evidência suficiente para afirmar conclusão das duas sprints de 15 dias, histórico diário por pessoa ou burndown real de 30 dias.

## 4. Evidências técnicas

- `docker compose config -q`: passou em 20/10/2026.
- `python -m unittest discover -s backend -p 'test_*.py'`: 12 testes passaram em 20/10/2026, incluindo API, ETL, formato oficial CP1252, campo extralongo e reimportação idempotente.
- Os três serviços iniciaram; `db` e `backend` ficaram saudáveis; página e `GET /api/health` retornaram HTTP 200.
- Fontes oficiais `APOSENTADOS_082025.csv` e `APOSENTADOS_082025_FULL.csv`: 811 e 413.990 linhas inseridas, respectivamente; banco com 414.801 hashes únicos. A reimportação da extração mensal inseriu 0 e reconheceu 811 duplicatas. CPF e matrícula não existem no schema e não são enviados ao banco pelo ETL.
- Busca por cargo retornou HTTP 200 e 35 registros; similaridade retornou HTTP 200 com limite de 100. O defeito no operador `%` do `pg_trgm` foi corrigido e ganhou teste de regressão.
- `EXPLAIN (ANALYZE, BUFFERS)` sobre 414.801 linhas apontou 6.970 resultados após rechecagem e ~10,4 mil blocos de heap; o sort Top-N consumiu cerca de 2 ms. Um experimento de `COUNT` limitado a 100 levou 31,440 ms contra mediana de 207,183 ms para o `COUNT` integral. A API não foi alterada nessa investigação.
- O benchmark concorrente executou 25 requisições em cada nível (1, 2, 4 e 8), com 100 respostas HTTP 200 e nenhum erro. A vazão máxima foi 4,464 req/s em concorrência 4; em concorrência 8, o P95 foi 1,946 s e o pico observado de CPU do banco foi 610%. Uma execução curta não comprova capacidade de produção; o P99 com 25 amostras é o maior valor observado.
- Os resultados sequenciais e concorrentes, instruções de reprodução e métricas de CPU/RAM estão em `docs/testes-e-carga.md`; os planos completos da análise estão em `docs/analise-busca-similaridade.md` e o benchmark em `docs/benchmark-concorrente-2026-10-20.json`.

## 5. Branches, PRs e proteção

- PRs #13 a #30 foram integrados por Pull Requests; PR #21 integrou o formato oficial e as validações do ETL, PR #24 ampliou o parser para a fotografia completa, PR #26 documentou a análise de consulta, PR #28 fixou a regra de fonte, e PR #30 adicionou e executou o benchmark concorrente.
- A proteção de `main` exige o check `backend` e branch atualizada; administradores também estão sujeitos às regras; force push e exclusão estão bloqueados.
- A exigência de aprovação foi configurada como zero para permitir o fluxo solo. Aprovação independente pode ser adicionada quando houver outro colaborador; não foi simulada.

## 6. Limitações conhecidas

1. A base consultada cobre aposentados civis. Para uma competência com arquivo `_FULL`, a regra do ServidorBR escolhe `_FULL` como fonte canônica e não soma o arquivo mensal; o volume local mantido para reprodução ainda contém ambos e, por isso, é uma fixture exploratória mista.
2. O dicionário oficial de aposentados não documenta UF; o endpoint continua retornando `422 UF_UNAVAILABLE` para UF válida e não infere estado pelo órgão.
3. O dicionário oficial de Carreiras/Cargos declara dados de servidores ativos e `UF da UPAG de vinculação`. Essa UF é da unidade pagadora, não residência. A fonte ainda não foi integrada; registros ativos continuam fora da API.
4. Carreiras/Cargos não foi relacionado automaticamente a registros individuais de aposentados. A integração exige separar a situação funcional e descartar CPF.
5. O ETL é append-only; mudanças ou remoções entre competências não são reconciliadas automaticamente.
6. O benchmark concorrente é uma rodada local curta, limitada a uma consulta e a quatro níveis. Rate limit em memória não sincroniza instâncias, e os limites atuais de timeout não são um SLO validado.
7. A exigência de equipe mínima e a data limite do enunciado continuam não atendidas por este trabalho solo tardio.

## 7. Conclusão

O código, os testes e a documentação permitem reproduzir a execução local com uma amostra oficial. Não declarar a entrega acadêmica como concluída: faltam evidência da equipe exigida, adequação ao prazo e medições de carga sobre um conjunto representativo.
