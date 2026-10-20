# Dados e ETL - ServidorBR

## Fontes consultadas

| Conjunto | Documento/repositório | Uso |
|---|---|---|
| Gestão de Pessoas do Executivo Federal - Aposentados | [Dicionário oficial de dados](https://repositorio.dados.gov.br/segrt/1.20180829-DadosRecursos-Aposentados.pdf) | Fonte de registros de aposentados civis; contém nome, CPF mascarado, matrícula, órgão, cargo e outros atributos. |
| Gestão de Pessoas do Executivo Federal - Carreiras/Cargos | [Repositório oficial SEGRt](https://repositorio.dados.gov.br/segrt/) | Referência de nomenclatura; ainda não há integração/vínculo automático com a tabela de pessoas. |

## Fontes oficiais importadas

Foram usadas duas publicações da competência 08/2025 no [repositório oficial SEGRt](https://repositorio.dados.gov.br/segrt/): a extração mensal [`APOSENTADOS_082025.csv`](https://repositorio.dados.gov.br/segrt/APOSENTADOS_082025.csv) e a fotografia completa [`APOSENTADOS_082025_FULL.csv`](https://repositorio.dados.gov.br/segrt/APOSENTADOS_082025_FULL.csv). O índice lista os arquivos com 327 KB e 163 MB, respectivamente, ambos datados de 24/12/2025.

O [dicionário oficial](https://repositorio.dados.gov.br/segrt/1.20180829-DadosRecursos-Aposentados.pdf) descreve 18 campos. Os CSVs não têm cabeçalho; a leitura posicional usa `Nome` (coluna 1), `Nome do órgão` (coluna 4) e `Cargo` (coluna 7). CPF e matrícula nunca entram na consulta de inserção, no hash de identidade ou no schema PostgreSQL. Os arquivos usam separador `;` e CP1252. A fotografia completa tem 127 registros com colunas adicionais e um campo de 280.630 caracteres numa coluna legal não pesquisada; o ETL lê as três colunas necessárias e tolera esses extras.

| Arquivo | Bytes locais | Linhas lidas | Inseridas | Duplicadas | Rejeitadas | Tempo | Vazão |
|---|---:|---:|---:|---:|---:|---:|---:|
| `APOSENTADOS_082025.csv` | 334.943 | 811 | 811 | 0 | 0 | 0,336 s | 2.414 linhas/s |
| `APOSENTADOS_082025_FULL.csv` | 170.844.864 | 413.990 | 413.990 | 0 | 0 | 93,680 s | 4.419 linhas/s |

A segunda execução da extração mensal inseriu 0 e reconheceu 811 duplicatas em 0,131 s. O volume local contém 414.801 registros e hashes únicos: os 811 da extração mensal e os 413.990 da fotografia completa. Os arquivos foram removidos do host e dos containers após a carga; o volume local de PostgreSQL mantém apenas as colunas pesquisáveis. Hash SHA-256 do arquivo FULL baixado: `CD7AEAF871CBBE006AE7CED659BBF6BB94107AA5FF943EEB2EEDED53B884BDEC`.

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

1. Baixe o CSV oficial e mantenha-o fora do Git: `Invoke-WebRequest -Uri https://repositorio.dados.gov.br/segrt/APOSENTADOS_082025.csv -OutFile db/data/APOSENTADOS_082025.csv` (ou use o sufixo `_FULL` para a fotografia completa).
2. Inicie os containers com `docker compose up --build -d`.
3. Copie o CSV para o container: `docker compose cp ./db/data/APOSENTADOS_082025.csv backend:/tmp/APOSENTADOS_082025.csv`.
4. Execute: `docker compose exec backend python etl.py /tmp/APOSENTADOS_082025.csv`.
5. Guarde o resumo da execução e a competência/fonte do arquivo no relatório de entrega.

ETL aceita `;`, `,` ou tabulação; cabeçalhos normalizados equivalentes a `Nome`, `Cargo` e `Nome do órgão`; e o formato oficial sem cabeçalho com ao menos 18 colunas. A detecção de UTF-8 é feita em streaming e usa CP1252 quando a validação UTF-8 falha. O limite de campo é 1.000.000 caracteres; campos acima desse limite falham a transação. Registros sem nome são rejeitados; no formato oficial posicional, linhas com menos de 18 colunas também são rejeitadas. Hash SHA-256 de nome, cargo, órgão e nome do arquivo evita reimportar linhas idênticas do mesmo arquivo. Quando a mesma combinação aparece mais de uma vez no CSV, o ETL acrescenta um ordinal de ocorrência ao hash para preservar cada linha e manter a reimportação idempotente. A primeira ocorrência mantém o hash anterior para compatibilidade com registros já importados. Não faz `TRUNCATE` e não apaga registros anteriores.

## Limitações conhecidas

- A identidade de cada linha idêntica depende da ordem de ocorrência no arquivo; mudanças no conteúdo ou na repetição de linhas podem gerar novas identidades. O ETL é append-only e não reconcilia alterações nem remove registros antigos.
- A importação é append-only; alterações e remoções em novas competências não são reconciliadas automaticamente. Não há chave oficial não sensível para reconciliar pessoas entre arquivos distintos.
- O tempo do FULL foi medido na máquina local e não representa uma carga concorrente ou uma garantia para outros ambientes.
- O vínculo entre carreiras/cargos e pessoas não foi estabelecido.
- A UF não está disponível no dataset selecionado.
