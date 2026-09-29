# Dados e ETL - ServidorBR

## Fontes oficiais

| Conjunto | Fonte | Situação |
| --- | --- | --- |
| Gestão de Pessoas do Executivo Federal - Aposentados | https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal--aposentados | A analisar - SB-02 |
| Gestão de Pessoas do Executivo Federal - Carreiras/Cargos | https://dados.gov.br/dados/conjuntos-dados/gestao-de-pessoas-executivo-federal---carreiras--cargos | A analisar - SB-02 |

## Mapeamento de campos

O mapeamento será completado após a leitura dos dicionários oficiais. Não presumir nomes de colunas dos CSVs antes dessa análise.

| Campo de origem | Campo destino | Tipo | Uso | Tratamento | Situação |
| --- | --- | --- | --- | --- | --- |
| `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | `PREENCHER` | Pendente |

## Processo de ETL planejado

1. Receber os CSVs oficiais em `db/data/` sem versionar arquivos volumosos ou sensíveis.
2. Validar cabeçalhos, codificação, campos obrigatórios e tipos.
3. Tratar ou rejeitar registros inválidos, registrando a quantidade e o motivo.
4. Normalizar campos pesquisáveis.
5. Importar os dados validados para PostgreSQL.
6. Produzir relatório com totais de entrada, importação, rejeição e motivo das rejeições.

## Normalização de texto

Campos utilizados em pesquisa terão versão normalizada: sem acentos, em maiúsculas, com espaços duplicados removidos e sem espaços nas extremidades.

```text
José da Silva Júnior -> JOSE DA SILVA JUNIOR
```

## Evidências pendentes

- [ ] Dicionários oficiais analisados.
- [ ] Mapeamento de campos preenchido.
- [ ] Relatório de importação com números reais anexado.
- [ ] Schema e índices validados no PostgreSQL.
