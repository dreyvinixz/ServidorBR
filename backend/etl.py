"""Importa o CSV oficial de aposentados sem persistir CPF ou matrícula."""
import argparse
import csv
import hashlib
import os
import unicodedata

import psycopg

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://servidorbr:local-dev-only@localhost:5432/servidorbr")


def norm(value):
    value = unicodedata.normalize("NFKD", value or "")
    return " ".join("".join(c for c in value if not unicodedata.combining(c)).upper().split())


def key(header):
    return norm(header).replace(" ", "")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path")
    args = parser.parse_args()
    inserted = rejected = seen = 0
    occurrences = {}
    with open(args.csv_path, encoding="utf-8-sig", newline="") as source:
        sample = source.read(8192)
        source.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=";,\t")
        except csv.Error:
            class SemicolonDialect(csv.excel):
                delimiter = ";"
            dialect = SemicolonDialect
        reader = csv.DictReader(source, dialect=dialect)
        columns = {key(name): name for name in reader.fieldnames or []}
        if "NOME" not in columns:
            raise SystemExit("CSV incompatível: coluna Nome não encontrada.")

        def get(row, *names):
            for name in names:
                original = columns.get(key(name))
                if original:
                    return (row.get(original) or "").strip()
            return ""

        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                for row in reader:
                    seen += 1
                    nome = get(row, "Nome")
                    if not nome:
                        rejected += 1
                        continue
                    cargo = get(row, "Cargo")
                    orgao = get(row, "Nome do órgão", "Nome do orgao")
                    identity = "\x1f".join((os.path.basename(args.csv_path), nome, cargo, orgao))
                    occurrence = occurrences.get(identity, 0) + 1
                    occurrences[identity] = occurrence
                    # Keep the original hash for the first row so existing imports
                    # remain idempotent. Distinct identical rows get stable ordinals.
                    material = identity if occurrence == 1 else f"{identity}\x1fduplicate\x1f{occurrence}"
                    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
                    cur.execute(
                        "INSERT INTO servidores (nome,nome_norm,cargo,cargo_norm,orgao,orgao_norm,source_hash,source_file) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (source_hash) DO NOTHING",
                        (nome, norm(nome), cargo or None, norm(cargo), orgao or None, norm(orgao), digest, os.path.basename(args.csv_path)),
                    )
                    inserted += cur.rowcount
    duplicates = max(0, seen - rejected - inserted)
    print(f"Lidos: {seen}; inseridos: {inserted}; duplicados: {duplicates}; rejeitados sem nome: {rejected}")


if __name__ == "__main__":
    main()
