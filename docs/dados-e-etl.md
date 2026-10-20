# Dados e ETL - ServidorBR

## Fontes consultadas

| Conjunto | Documento/repositório | Uso |
|---|---|---|
| Gestão de Pessoas do Executivo Federal - Aposentados | [Dicionário oficial de dados](https://repositorio.dados.gov.br/segrt/1.20180829-DadosRecursos-Aposentados.pdf) | Fonte de registros de aposentados civis; contém nome, CPF mascarado, matrícula, órgão, cargo e outros atributos. |
| Gestão de Pessoas do Executivo Federal - Carreiras/Cargos | [Repositório oficial SEGRt](https://repositorio.dados.gov.br/segrt/) | Referência de nomenclatura; ainda não há integração/vínculo automático com a tabela de pessoas. |

Os dados CSV não estão neste workspace. Portanto, não há contagens de linhas importadas a reportar.

## Mapeamento utilizado

| Campo original | Destino | Aplicação | Tratamento |
|---|---|---|---|
| `Nome` | `nome`, `nome_norm` | Busca nominal | Remove diacríticos, maiúsculas e compactação de espaços |
| `Cargo` | `cargo`, `cargo_norm` | Busca parcial | Mesma normalização; opcional |
| `Nome do órgão` | `orgao`, `orgao_norm` | Busca parcial | Mesma normalização; opcional |
| `CPF`, `Matrícula do Servidor` | Não armazenados | Nenhum | Descartados pelo ETL |
| UF | `uf` nullable | Filtro previsto | O dicionário consultado não contém esse atributo; não é inferido |

O arquivo de aposentados documenta nome, órgão e cargo, entre outros campos. Não documenta UF. A aplicação sinaliza a limitação e não deduz estado a partir do órgão.

## Importação local

1. Baixe o CSV oficial e mantenha-o fora do Git.
2. Inicie os containers com `docker compose up --build -d`.
3. Copie o CSV para o container: `docker compose cp ./aposentados.csv backend:/tmp/aposentados.csv`.
4. Execute: `docker compose exec backend python etl.py /tmp/aposentados.csv`.
5. Guarde o resumo da execução e a competência/fonte do arquivo no relatório de entrega.

ETL aceita `;`, `,` ou tabulação e cabeçalhos normalizados equivalentes a `Nome`, `Cargo` e `Nome do órgão`. Registros sem nome são rejeitados. Hash SHA-256 de nome, cargo, órgão e nome do arquivo evita reimportar linhas idênticas do mesmo arquivo. Não faz `TRUNCATE` e não apaga registros anteriores.

## Limitações conhecidas

- Linhas distintas no mesmo arquivo com nome, cargo e órgão idênticos colidem no hash e uma delas é ignorada. Uma chave oficial não sensível ou estratégia de versionamento por competência é necessária para corrigir isso com segurança.
- A importação é linha a linha e não foi medida com os arquivos completos.
- Encoding esperado é UTF-8/UTF-8 com BOM; outros encodings precisam de conversão ou suporte adicional.
- O vínculo entre carreiras/cargos e pessoas não foi estabelecido.
- A UF não está disponível no dataset selecionado.
