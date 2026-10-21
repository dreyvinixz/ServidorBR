"""Restore cargo and agency fields in the August 2025 FULL source.

Read-only by default. Use --apply only after reviewing the preflight output.
The durable backup is created in the same transaction before any UPDATE.
"""
import argparse
import csv
import hashlib
import os
import tempfile
import urllib.request

import psycopg
from etl import DATABASE_URL, detect_dialect, detect_encoding, iter_search_fields, norm

SOURCE_FILE = "APOSENTADOS_082025_FULL.csv"
SOURCE_URL = f"https://repositorio.dados.gov.br/segrt/{SOURCE_FILE}"
BACKUP_TABLE = "servidores_full_fields_backup_20261020"
EXPECTED_TOTAL = 414_801
EXPECTED_FULL = 413_990
EXPECTED_CARGO = 413_920
EXPECTED_ORGAO = 413_990
EXPECTED_MONTHLY = 811


def source_rows(path):
    """Yield the stable legacy key and the four corrected field values."""
    encoding = detect_encoding(path)
    occurrences = {}
    with open(path, encoding=encoding, newline="") as source:
        sample = source.read(8192)
        source.seek(0)
        dialect = detect_dialect(sample)
        for nome, cargo, orgao in iter_search_fields(source, dialect):
            nome = nome.strip()
            if not nome:
                continue
            # The existing FULL import hashed the name while cargo and orgao
            # were blank. Preserve that key so the repair never matches by name.
            identity = "\x1f".join((SOURCE_FILE, nome, "", ""))
            occurrence = occurrences.get(identity, 0) + 1
            occurrences[identity] = occurrence
            material = identity if occurrence == 1 else f"{identity}\x1fduplicate\x1f{occurrence}"
            digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
            yield digest, cargo or None, norm(cargo), orgao or None, norm(orgao)


def db_snapshot(conn):
    return conn.execute(
        """SELECT count(*) AS total,
                  count(*) FILTER (WHERE source_file = %s) AS full_rows,
                  count(*) FILTER (WHERE source_file = 'APOSENTADOS_082025.csv') AS monthly_rows,
                  count(*) FILTER (WHERE source_file = %s AND cargo IS NOT NULL) AS full_cargo,
                  count(*) FILTER (WHERE source_file = %s AND orgao IS NOT NULL) AS full_orgao,
                  (SELECT md5(coalesce(string_agg(
                      source_hash || E'\\x1f' || coalesce(cargo, E'\\N') || E'\\x1f' || cargo_norm ||
                      E'\\x1f' || coalesce(orgao, E'\\N') || E'\\x1f' || orgao_norm,
                      E'\\x1e' ORDER BY source_hash), ''))
                   FROM servidores WHERE source_file = 'APOSENTADOS_082025.csv') AS monthly_signature
           FROM servidores""",
        (SOURCE_FILE, SOURCE_FILE, SOURCE_FILE),
    ).fetchone()


def download_source(path):
    request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "ServidorBR-backfill/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response, open(path, "wb") as target:
        while chunk := response.read(1024 * 1024):
            target.write(chunk)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Create the backup and update the approved fields.")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="servidorbr-full-repair-") as temp_dir:
        path = os.path.join(temp_dir, SOURCE_FILE)
        print(f"Baixando fonte oficial: {SOURCE_URL}", flush=True)
        download_source(path)

        with psycopg.connect(DATABASE_URL) as conn:
            before = db_snapshot(conn)
            if before[0] != EXPECTED_TOTAL or before[1] != EXPECTED_FULL or before[2] != EXPECTED_MONTHLY:
                raise RuntimeError(f"Totais inesperados antes da operação: {before}")
            if before[3] != 0 or before[4] != 0:
                raise RuntimeError("O estado FULL mudou desde o preflight; recusando aplicar.")
            if conn.execute("SELECT to_regclass(%s)", (f"public.{BACKUP_TABLE}",)).fetchone()[0]:
                raise RuntimeError(f"A tabela de backup {BACKUP_TABLE} já existe; nada foi alterado.")

            full_hashes = {row[0] for row in conn.execute(
                "SELECT source_hash FROM servidores WHERE source_file = %s", (SOURCE_FILE,)
            )}
            source_hashes = set()
            source_cargo = source_orgao = 0
            for digest, cargo, _cargo_norm, orgao, _orgao_norm in source_rows(path):
                if digest in source_hashes:
                    raise RuntimeError(f"Chave source_hash repetida na fonte: {digest}")
                source_hashes.add(digest)
                source_cargo += cargo is not None
                source_orgao += orgao is not None
            if (len(source_hashes), source_cargo, source_orgao) != (EXPECTED_FULL, EXPECTED_CARGO, EXPECTED_ORGAO):
                raise RuntimeError(
                    f"Contagem inesperada na fonte: linhas={len(source_hashes)}, "
                    f"cargo={source_cargo}, orgao={source_orgao}"
                )
            if source_hashes != full_hashes:
                raise RuntimeError(
                    f"As chaves não correspondem: fonte={len(source_hashes)}, "
                    f"banco={len(full_hashes)}, faltantes={len(source_hashes - full_hashes)}, "
                    f"extras={len(full_hashes - source_hashes)}"
                )

            print(
                f"Preflight OK: linhas FULL={len(source_hashes)}, cargo={source_cargo}, "
                f"orgao={source_orgao}, mensais={before[2]}, "
                f"total={before[0]}, backup={BACKUP_TABLE}",
                flush=True,
            )
            if not args.apply:
                print("Modo somente leitura; use --apply para executar a atualização aprovada.")
                return

            with conn.transaction():
                conn.execute(
                    f"""CREATE TABLE public.{BACKUP_TABLE} AS
                         SELECT id, source_file, source_hash, cargo, cargo_norm, orgao, orgao_norm
                         FROM servidores WHERE source_file = %s""",
                    (SOURCE_FILE,),
                )
                backup_count = conn.execute(f"SELECT count(*) FROM public.{BACKUP_TABLE}").fetchone()[0]
                if backup_count != EXPECTED_FULL:
                    raise RuntimeError(f"Backup incompleto: {backup_count} linhas.")

                conn.execute(
                    """CREATE TEMP TABLE full_fields_stage (
                           source_hash CHAR(64) PRIMARY KEY,
                           cargo TEXT, cargo_norm TEXT NOT NULL,
                           orgao TEXT, orgao_norm TEXT NOT NULL
                       ) ON COMMIT DROP"""
                )
                with conn.cursor().copy(
                    "COPY full_fields_stage (source_hash,cargo,cargo_norm,orgao,orgao_norm) FROM STDIN"
                ) as copy:
                    for digest, cargo, cargo_norm, orgao, orgao_norm in source_rows(path):
                        copy.write_row((digest, cargo, cargo_norm, orgao, orgao_norm))
                stage_count = conn.execute("SELECT count(*) FROM full_fields_stage").fetchone()[0]
                if stage_count != EXPECTED_FULL:
                    raise RuntimeError(f"Carga temporária incompleta: {stage_count} linhas.")

                updated = conn.execute(
                    """UPDATE servidores AS target
                       SET cargo = stage.cargo, cargo_norm = stage.cargo_norm,
                           orgao = stage.orgao, orgao_norm = stage.orgao_norm
                       FROM full_fields_stage AS stage
                       WHERE target.source_file = %s AND target.source_hash = stage.source_hash""",
                    (SOURCE_FILE,),
                ).rowcount
                if updated != EXPECTED_FULL:
                    raise RuntimeError(f"Quantidade atualizada inesperada: {updated}.")

                after = db_snapshot(conn)
                expected = (EXPECTED_TOTAL, EXPECTED_FULL, EXPECTED_MONTHLY, EXPECTED_CARGO, EXPECTED_ORGAO)
                actual = (after[0], after[1], after[2], after[3], after[4])
                if actual != expected or after[5] != before[5]:
                    raise RuntimeError(f"Readback não confere; transação será revertida: {after}")
                print(f"Validação dentro da transação OK; backup={backup_count}, atualizadas={updated}.", flush=True)

        print(
            f"Concluído. Backup permanente: public.{BACKUP_TABLE}; "
            f"total={after[0]}, FULL cargo={after[3]}, "
            f"FULL orgao={after[4]}, mensais={after[2]}."
        )


if __name__ == "__main__":
    main()
