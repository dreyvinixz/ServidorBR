# Base de aposentados — agosto de 2025

As duas partes `APOSENTADOS_082025_FULL.csv.gz.part01` e `.part02` contêm o CSV oficial completo, compactado sem alterações. A competência é 08/2025; a publicação oficial está datada de 24/12/2025.

Fonte: https://repositorio.dados.gov.br/segrt/APOSENTADOS_082025_FULL.csv

CSV original: 170.844.864 bytes, 413.990 registros, separador ponto e vírgula e codificação CP1252.
SHA-256 do CSV original: `cd7aeaf871cbbe006ae7ced659bbf6bb94107aa5ff943eeb2eeded53b884bdec`.

O arquivo original contém campos que o ETL descarta, inclusive CPF mascarado e matrícula. Somente nome, cargo e órgão são importados. A inclusão compactada é uma exceção autorizada para permitir a reprodução da carga. Não some a extração mensal desta competência ao FULL.

As partes são fragmentos binários de um único gzip. Reúna e extraia com Python 3.11 ou superior na raiz do projeto (o script verifica o SHA-256):

```bash
python db/data/extract_csv.py
```

Depois importe:

```bash
docker compose up -d db backend
docker compose cp db/data/APOSENTADOS_082025_FULL.csv backend:/tmp/APOSENTADOS_082025_FULL.csv
docker compose exec backend python etl.py /tmp/APOSENTADOS_082025_FULL.csv
```

Uma base nova deve receber somente o FULL. O ETL não limpa registros de cargas anteriores. A extração descompactada continua ignorada pelo Git.
