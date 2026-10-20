# Relatório de estado do projeto - ServidorBR

**Atualizado em:** 20/10/2026  
**Estado:** MVP integrado; validações locais com amostra oficial concluídas; entrega acadêmica ainda não aprovada.

## 1. Escopo disponível

O MVP reúne frontend estático, API Flask/Gunicorn, PostgreSQL com índices `pg_trgm`, ETL de CSV e Compose. Uma instalação nova começa com banco vazio e recebe dados por importação local. O volume local de desenvolvimento contém 414.801 registros de aposentados da competência 08/2025; os CSVs originais não foram incluídos no repositório.

## 2. Equipe e histórico verificável

O enunciado requer de três a quatro integrantes e distribuição real de tarefas/commits. `TASK.md` registra dois nomes e um integrante como `PREENCHER`; a autoria Git desta implementação é somente `dreyvinixz`. Não atribuir autoria, datas ou trabalho a integrantes sem evidência. A composição precisa ser confirmada pelo grupo antes da submissão.

O `main` remoto contém mais de 30 commits após integração dos PRs #13 a #22. A Issue [SB-05](https://github.com/dreyvinixz/ServidorBR/issues/12) foi fechada com a entrega do ETL oficial. O diário disponível em `docs/burndown.csv` termina em 26/09/2026 e não representa o trabalho executado em outubro; não foi reconstruído retroativamente.

## 3. Prazo e sprints

O enunciado define entrega limite em 13/10/2026. Esta implementação começou em 20/10/2026, depois do prazo. O quadro original registra Sprint 1 desde 25/09 e acompanhamento somente até 26/09. Não há evidência suficiente para afirmar conclusão das duas sprints de 15 dias, histórico diário por pessoa ou burndown real de 30 dias.

## 4. Evidências técnicas

- `docker compose config -q`: passou em 20/10/2026.
- `python -m unittest discover -s backend -p 'test_*.py'`: 12 testes passaram em 20/10/2026, incluindo API, ETL, formato oficial CP1252, campo extralongo e reimportação idempotente.
- Os três serviços iniciaram; `db` e `backend` ficaram saudáveis; página e `GET /api/health` retornaram HTTP 200.
- Fontes oficiais `APOSENTADOS_082025.csv` e `APOSENTADOS_082025_FULL.csv`: 811 e 413.990 linhas inseridas, respectivamente; banco com 414.801 hashes únicos. A reimportação da extração mensal inseriu 0 e reconheceu 811 duplicatas. CPF e matrícula não existem no schema e não são enviados ao banco pelo ETL.
- Busca por cargo retornou HTTP 200 e 35 registros; similaridade retornou HTTP 200 com limite de 100. O defeito no operador `%` do `pg_trgm` foi corrigido e ganhou teste de regressão.
- Medições sequenciais de API: 20 amostras por cenário sobre 414.801 registros, sem concorrência; P50/P95 foram registrados em `docs/testes-e-carga.md`. Não há benchmark concorrente nem métricas de CPU/RAM.

## 5. Branches, PRs e proteção

- PRs #13 a #24 foram integrados por Pull Requests; PR #18 integrou o release, PR #21 integrou o formato oficial e as validações do ETL, PRs #22/#23 atualizaram este relatório, e PR #24 ampliou o parser para a fotografia completa.
- A proteção de `main` exige o check `backend` e branch atualizada; administradores também estão sujeitos às regras; force push e exclusão estão bloqueados.
- A exigência de aprovação foi configurada como zero para permitir o fluxo solo. Aprovação independente pode ser adicionada quando houver outro colaborador; não foi simulada.

## 6. Limitações conhecidas

1. A fonte importada cobre aposentados civis; servidores ativos não estão integrados.
2. O dicionário oficial de aposentados não documenta UF; o endpoint retorna `422 UF_UNAVAILABLE` para UF válida e não infere estado pelo órgão.
3. Carreiras/Cargos não foi relacionado automaticamente a registros individuais.
4. O ETL é append-only; mudanças ou remoções entre competências não são reconciliadas automaticamente.
5. As consultas foram medidas localmente e sequencialmente; o benchmark não valida carga concorrente.
6. Rate limit em memória não sincroniza instâncias e não foi validado sob concorrência.
7. A exigência de equipe mínima e a data limite do enunciado continuam não atendidas por este trabalho solo tardio.

## 7. Conclusão

O código, os testes e a documentação permitem reproduzir a execução local com uma amostra oficial. Não declarar a entrega acadêmica como concluída: faltam evidência da equipe exigida, adequação ao prazo e medições de carga sobre um conjunto representativo.
