# Relatório de estado do projeto - ServidorBR

**Atualizado em:** 20/10/2026  
**Estado:** MVP local implementado; entrega acadêmica ainda não aprovada.

## 1. Escopo disponível

O MVP reúne frontend estático, API Flask/Gunicorn, PostgreSQL com índices `pg_trgm`, ETL de CSV e Compose. A base não contém registros no repositório. A execução de testes unitários e a validação de configuração do Compose passaram; ainda falta confirmar a stack com banco e dados reais.

## 2. Equipe e histórico verificável

O enunciado requer de três a quatro integrantes e distribuição real de tarefas/commits. `TASK.md` registra dois nomes e um integrante como `PREENCHER`; os commits desta branch foram feitos somente pelo usuário Git configurado `dreyvinixz`. Não atribuir autoria, datas ou trabalho a integrantes sem evidência. A composição precisa ser confirmada pelo grupo antes da submissão.

Os commits locais desta implementação estão na branch `feat/SB-02-21-mvp-entrega`; consultar `git log --date=short --format="%h %ad %an %s"`. O diário disponível em `docs/burndown.csv` termina em 26/09/2026 e não representa o trabalho executado nesta branch. Não foi reconstruído retroativamente.

## 3. Prazo e sprints

O enunciado define entrega limite em 13/10/2026. Esta implementação começou em 20/10/2026, depois do prazo. O quadro original registra Sprint 1 desde 25/09 e acompanhamento somente até 26/09. Não há evidência suficiente para afirmar conclusão das duas sprints de 15 dias, histórico diário por pessoa ou burndown real de 30 dias.

## 4. Evidências técnicas

- `docker compose config -q`: passou em 20/10/2026.
- `python -m unittest discover -s backend -p 'test_*.py'`: 6 testes passaram em 20/10/2026.
- Docker Compose completo: ainda não registrado como iniciado/saudável neste relatório.
- Importação dos arquivos oficiais: não executada; nenhum CSV foi disponibilizado localmente.
- Carga e percentis: não medidos.

## 5. Limitações conhecidas

1. Fonte de aposentados não documenta UF; endpoint retorna `422 UF_UNAVAILABLE` para UF válida.
2. Base inicia vazia e cobre apenas aposentados, não servidores ativos.
3. Carreiras/Cargos não foi relacionado automaticamente a registros individuais.
4. ETL pode colapsar duas pessoas com o mesmo nome, cargo e órgão no mesmo arquivo; isso requer chave não sensível e validação do dataset.
5. Rate limit em memória não sincroniza instâncias e não foi validado sob carga.
6. A exigência de equipe mínima e a data limite do enunciado continuam não atendidas por este trabalho solo tardio.

## 6. Conclusão

O código e a documentação técnica constituem uma base executável para demonstração após importar um CSV. Não declarar a entrega acadêmica como concluída: faltam evidência da equipe exigida, adequação ao prazo, dados oficiais de teste, teste integrado dos containers e medições de carga.
