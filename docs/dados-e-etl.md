# Dados e ETL - ServidorBR

## Fontes consultadas

| Conjunto | Documento/repositório | Uso |
|---|---|---|
| Gestão de Pessoas do Executivo Federal - Aposentados | [Dicionário oficial de dados](https://repositorio.dados.gov.br/segrt/1.20180829-DadosRecursos-Aposentados.pdf) | Fonte de registros de aposentados civis; contém nome, CPF mascarado, matrícula, órgão, cargo e outros atributos. |
| Gestão de Pessoas do Executivo Federal - Carreiras/Cargos | [Repositório oficial SEGRt](https://repositorio.dados.gov.br/segrt/) | Referência de nomenclatura; ainda não há integração/vínculo automático com a tabela de pessoas. |

## Amostra oficial importada

Foi usada a amostra [`APOSENTADOS_082025.csv`](https://repositorio.dados.gov.br/segrt/APOSENTADOS_082025.csv), publicada no [repositório oficial SEGRt](https://repositorio.dados.gov.br/segrt/). O índice do repositório lista o arquivo com 327 KB e data de 24/12/2025. O CSV foi baixado em 20/10/2026 para `db/data/`, diretório ignorado pelo Git, e não foi incluído no repositório.

O [dicionário oficial](https://repositorio.dados.gov.br/segrt/1.20180829-DadosRecursos-Aposentados.pdf) descreve 18 campos e a amostra não tem linha de cabeçalho. A leitura posicional usa `Nome` (coluna 1), `Nome do órgão` (coluna 4) e `Cargo` (coluna 7); CPF e matrícula são lidos apenas como parte da linha CSV e nunca entram na consulta de inserção, no hash de identidade ou no schema PostgreSQL. O arquivo usa separador `;`, codificação CP1252 e contém bytes NUL em campos não importados.

Resultado da carga local: 811 linhas lidas, 811 inseridas, 0 duplicadas e 0 rejeitadas; 334.943 bytes; 0,336 s (2.414 linhas/s), incluindo leitura, conexão e escrita no PostgreSQL local. Uma segunda execução leu 811 linhas, inseriu 0 e reconheceu 811 duplicatas (0,131 s). A tabela ficou com 811 hashes únicos. A amostra permanece no volume local do banco; o CSV original foi removido do host e do container após a validação.

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

1. Baixe o CSV oficial e mantenha-o fora do Git: `Invoke-WebRequest -Uri https://repositorio.dados.gov.br/segrt/APOSENTADOS_082025.csv -OutFile db/data/APOSENTADOS_082025.csv`.
2. Inicie os containers com `docker compose up --build -d`.
3. Copie o CSV para o container: `docker compose cp ./db/data/APOSENTADOS_082025.csv backend:/tmp/APOSENTADOS_082025.csv`.
4. Execute: `docker compose exec backend python etl.py /tmp/APOSENTADOS_082025.csv`.
5. Guarde o resumo da execução e a competência/fonte do arquivo no relatório de entrega.

ETL aceita `;`, `,` ou tabulação; cabeçalhos normalizados equivalentes a `Nome`, `Cargo` e `Nome do órgão`; e o formato oficial sem cabeçalho com 18 colunas. A detecção de UTF-8 é feita em streaming e usa CP1252 quando a validação UTF-8 falha. Registros sem nome são rejeitados; no formato oficial posicional, linhas com largura incompatível também são rejeitadas. Hash SHA-256 de nome, cargo, órgão e nome do arquivo evita reimportar linhas idênticas do mesmo arquivo. Quando a mesma combinação aparece mais de uma vez no CSV, o ETL acrescenta um ordinal de ocorrência ao hash para preservar cada linha e manter a reimportação idempotente. A primeira ocorrência mantém o hash anterior para compatibilidade com registros já importados. Não faz `TRUNCATE` e não apaga registros anteriores.

## Limitações conhecidas

- A identidade de cada linha idêntica depende da ordem de ocorrência no arquivo; mudanças no conteúdo ou na repetição de linhas podem gerar novas identidades. O ETL é append-only e não reconcilia alterações nem remove registros antigos.
- A importação é linha a linha; foi medida somente com esta amostra de 811 linhas, não com os arquivos completos.
- A importação é append-only; alterações e remoções em novas competências não são reconciliadas automaticamente.
- O vínculo entre carreiras/cargos e pessoas não foi estabelecido.
- A UF não está disponível no dataset selecionado.
