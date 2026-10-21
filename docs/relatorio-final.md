# Relatório de estado do projeto - ServidorBR

**Atualizado em:** 20/10/2026  
**Estado:** reparo dos campos FULL e busca com listas pesquisáveis integrados pelo PR #46; aplicativo desktop adicional em desenvolvimento na branch `feat/SB-29-desktop-app`.

## 1. Escopo disponível

O MVP reúne frontend estático, API Flask/Gunicorn, PostgreSQL com índices `pg_trgm`, ETL de CSV e Compose. Uma instalação nova começa com banco vazio e recebe dados por importação local. O volume local de desenvolvimento contém 414.801 registros de aposentados da competência 08/2025; os CSVs originais não foram incluídos no repositório.

## 2. Equipe e histórico verificável

O enunciado requer de três a quatro integrantes e distribuição real de tarefas/commits. `TASK.md` registra dois nomes e um integrante como `PREENCHER`; a autoria Git desta implementação é somente `dreyvinixz`. Não atribuir autoria, datas ou trabalho a integrantes sem evidência. A composição precisa ser confirmada pelo grupo antes da submissão.

O `main` remoto contém mais de 30 commits após integração dos PRs #13 a #30. A Issue [SB-05](https://github.com/dreyvinixz/ServidorBR/issues/12) foi fechada com a entrega do ETL oficial. O diário disponível em `docs/burndown.csv` termina em 26/09/2026 e não representa o trabalho executado em outubro; não foi reconstruído retroativamente.

## 3. Prazo e sprints

O enunciado define entrega limite em 13/10/2026. Esta implementação começou em 20/10/2026, depois do prazo. O quadro original registra Sprint 1 desde 25/09 e acompanhamento somente até 26/09. Não há evidência suficiente para afirmar conclusão das duas sprints de 15 dias, histórico diário por pessoa ou burndown real de 30 dias.

## 4. Evidências técnicas

- `docker compose config -q`: passou em 20/10/2026.
- `python -m unittest discover -s backend -p 'test_*.py'`: 15 testes passaram após a mudança do `COUNT`, incluindo API, ETL, limites da contagem, formato oficial CP1252, campo extralongo e reimportação idempotente.
- Os três serviços iniciaram; `db` e `backend` ficaram saudáveis; página e `GET /api/health` retornaram HTTP 200.
- Fontes oficiais `APOSENTADOS_082025.csv` e `APOSENTADOS_082025_FULL.csv`: 811 e 413.990 linhas inseridas, respectivamente; banco com 414.801 hashes únicos. A reimportação da extração mensal inseriu 0 e reconheceu 811 duplicatas. CPF e matrícula não existem no schema e não são enviados ao banco pelo ETL.
- Busca por cargo retornou HTTP 200 e 35 registros; similaridade retornou HTTP 200 com limite de 100. O defeito no operador `%` do `pg_trgm` foi corrigido e ganhou teste de regressão.
- `EXPLAIN (ANALYZE, BUFFERS)` sobre 414.801 linhas apontou 6.970 resultados após rechecagem e ~10,4 mil blocos de heap; o sort Top-N consumiu cerca de 2 ms. Um experimento de `COUNT` limitado a 100 levou 31,440 ms contra mediana de 207,183 ms para o `COUNT` integral. A API não foi alterada nessa investigação.
- A rota agora limita a contagem da busca por similaridade ao parâmetro `limit`, mantendo contagem exata abaixo do teto e o total capado acima dele. Três testes cobrem abaixo/acima do limite e contagem exata dos demais filtros. Duas rodadas sequenciais mostraram P50 de 305–338 ms e P95 de 413–463 ms, contra 458/509 ms antes; uma segunda rodada teve pico máximo isolado de 1,612 s. O plano limitado executou em 33 ms e 567 shared hits contra 237 ms e 10.457 hits na contagem integral.
- O benchmark concorrente foi repetido com 25 requisições por nível (1, 2, 4 e 8), 100 respostas HTTP 200 e nenhum erro. Após a mudança, a vazão foi de 3,04/4,41/6,09/6,16 req/s e o P95 de 417/557/531/1.329 ms, respectivamente. O pico observado de CPU do banco chegou a 685%. Uma execução curta não comprova capacidade de produção; o P99 com 25 amostras é o maior valor observado.
- Os resultados sequenciais e concorrentes, instruções de reprodução e métricas de CPU/RAM estão em `docs/testes-e-carga.md`; os planos e comparação estão em `docs/analise-busca-similaridade.md`, e os JSON antes/depois estão em `docs/benchmark-concorrente-2026-10-20.json` e `docs/benchmark-concorrente-depois-count-limitado-2026-10-20.json`.
- O reparo autorizado da base local criou `servidores_full_fields_backup_20261020` com 413.990 linhas e atualizou somente `cargo`, `cargo_norm`, `orgao` e `orgao_norm` por `(source_file, source_hash)`. Readback confirmou 414.801 registros totais, 413.920 linhas FULL com cargo, 413.990 com órgão e 811 linhas mensais intactas. A procedure e o SQL de reversão estão em `docs/reparo-campos-full-202508.md`.
- A API `GET /api/opcoes` fornece 1.479 cargos e 183 órgãos distintos da base; a busca aproximada `Maria Silva` retornou 100 resultados com campos de cargo/órgão preenchidos. `npm run build` e `python -m unittest discover -s backend -p 'test_*.py'` passaram (15 testes). A API também retornou 200 para uma consulta vazia.
- A interface web ainda aguarda inspeção visual no navegador: o ambiente de automação não disponibilizou navegador. A responsividade foi compilada, mas não foi declarada como visualmente aceita.

## 5. Branches, PRs e proteção

- PRs #13 a #34 foram integrados por Pull Requests; PR #21 integrou o formato oficial e as validações do ETL, PR #24 ampliou o parser para a fotografia completa, PR #26 documentou a análise de consulta, PR #28 fixou a regra de fonte, PR #30 adicionou o benchmark concorrente, PR #32 atualizou este relatório, e PR #34 limitou o `COUNT` da busca por similaridade e repetiu as medições.
- PRs #36, #37, #39, #41 e #43 integraram o frontend React/Tailwind, documentação de status, proxy Vite, opções avançadas e aliases do FULL. O PR #46 integrou o reparo de dados e listas pesquisáveis; seus checks `backend` e `frontend` passaram.
- A Issue #45 acompanha o aplicativo desktop para o ponto adicional de 1,0. O pacote Windows e sua validação ainda estão pendentes.
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

O código, os testes e a documentação permitem reproduzir a execução local com uma amostra oficial. Para fechar o repositório ainda faltam empacotar e validar o aplicativo desktop da Issue #45 e concluir uma inspeção visual no navegador quando este estiver disponível. Não declarar a entrega acadêmica como concluída: faltam evidência da equipe exigida e adequação ao prazo.
