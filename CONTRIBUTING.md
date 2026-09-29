# Guia de contribuição

## Antes de começar

1. Consulte `TASK.md` e escolha apenas a task atribuída a você.
2. Crie/atribua a Issue correspondente (`SB-XX`) no GitHub.
3. Mova a Issue para `Todo` no quadro da sprint.
4. Crie uma branch a partir da branch de integração da sprint.

```bash
git switch sprint/01-fundacao-api
git pull origin sprint/01-fundacao-api
git switch -c feat/SB-07-api-filtros
```

## Durante o desenvolvimento

- Mova a Issue para `In Progress` somente quando começar o trabalho real.
- Faça commits coesos: `tipo(escopo): resumo [SB-XX]`.
- Registre impedimentos reais no quadro e na Issue.
- Não envie segredos, arquivo `.env`, dados sensíveis ou CSVs públicos volumosos.

## Pull Request e revisão

1. Envie a branch e abra um PR para a branch da sprint correta.
2. Use o modelo de PR e vincule a Issue com `Closes #numero`.
3. Solicite revisão de alguém que não seja o autor.
4. O revisor deve usar o checklist de PR; ao menos uma aprovação é obrigatória.
5. Após a aprovação e os checks passarem, mescle na branch da sprint.
6. Somente no encerramento da sprint abra o PR `sprint/... -> main`, também revisado por outra pessoa.

## Colunas do quadro

`Backlog` -> `Todo` -> `In Progress` -> `Review` -> `Done`

Não marque uma task como `Done` sem PR mesclado, critérios de aceite atendidos, testes aplicáveis e documentação atualizada.
