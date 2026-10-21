"""Importa CSVs oficiais de aposentados sem persistir CPF ou matrícula."""
import argparse
import codecs
import csv
import hashlib
import io
import os
import time
import unicodedata

import psycopg

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://servidorbr:local-dev-only@localhost:5432/servidorbr")
OFFICIAL_COLUMNS = 18
MAX_CSV_FIELD_CHARS = 1_000_000


def norm(value):
    value = unicodedata.normalize("NFKD", value or "")
    return " ".join("".join(c for c in value if not unicodedata.combining(c)).upper().split())


def key(header):
    return norm(header).replace(" ", "")


def detect_encoding(path):
    """Validate UTF-8 incrementally, falling back to the source's Windows encoding."""
    decoder = codecs.getincrementaldecoder("utf-8-sig")("strict")
    try:
        with open(path, "rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                decoder.decode(chunk)
            decoder.decode(b"", final=True)
    except UnicodeDecodeError:
        return "cp1252"
    return "utf-8-sig"


def iter_search_fields(source, dialect):
    """Yield only name, cargo, and agency from headered or official positional CSVs."""
    csv.field_size_limit(MAX_CSV_FIELD_CHARS)
    reader = csv.reader(source, dialect=dialect)
    first = next(reader, None)
    if first is None:
        raise SystemExit("CSV vazio.")

    columns = {key(name): index for index, name in enumerate(first)}
    has_header = "NOME" in columns and (
        len(first) < OFFICIAL_COLUMNS
        or bool({"CARGO", "CARGOEMPREGO", "NOMEDOORGAO", "ORGAO", "CPF", "MATRICULA", "MATRICULADOSERVIDOR"} & columns.keys())
    )
    if has_header:
        def value(row, *names):
            for name in names:
                index = columns.get(key(name))
                if index is not None and index < len(row):
                    return (row[index] or "").strip()
            return ""

        for row in reader:
            yield (
                value(row, "Nome"),
                value(row, "Cargo", "Cargo emprego"),
                value(row, "Nome do órgão", "Nome do orgao", "Orgao"),
            )
        return

    # Official APOSENTADOS_MMAAAA files have no header. The published dictionary
    # orders Nome at 0, Nome do órgão at 3, and Cargo at 6 in an 18-column row.
    if len(first) < OFFICIAL_COLUMNS:
        raise SystemExit(
            f"CSV incompatível: esperado cabeçalho com Nome ou ao menos {OFFICIAL_COLUMNS} colunas oficiais."
        )
    yield (first[0] or "").strip(), (first[6] or "").strip(), (first[3] or "").strip()
    for row in reader:
        if len(row) < OFFICIAL_COLUMNS:
            yield "", "", ""
        else:
            yield (row[0] or "").strip(), (row[6] or "").strip(), (row[3] or "").strip()


def detect_dialect(sample):
    """Choose the delimiter producing the most consistent multi-column rows."""
    candidates = []
    for priority, delimiter in enumerate((";", ",", "\t")):
        try:
            widths = [len(row) for row in csv.reader(io.StringIO(sample), delimiter=delimiter) if row]
        except csv.Error:
            continue
        if not widths:
            continue
        modal_width = max(set(widths), key=widths.count)
        consistency = widths.count(modal_width) / len(widths)
        candidates.append(((modal_width, consistency, -priority), delimiter))
    if not candidates or max(candidates)[0][0] == 1:
        class SemicolonDialect(csv.excel):
            delimiter = ";"
        return SemicolonDialect
    delimiter = max(candidates)[1]
    class DetectedDialect(csv.excel):
        pass
    DetectedDialect.delimiter = delimiter
    return DetectedDialect


def import_file(csv_path):
    started = time.perf_counter()
    encoding = detect_encoding(csv_path)
    inserted = rejected = seen = 0
    occurrences = {}
    with open(csv_path, encoding=encoding, newline="") as source:
        sample = source.read(8192)
        source.seek(0)
        dialect = detect_dialect(sample)

        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                for nome, cargo, orgao in iter_search_fields(source, dialect):
                    seen += 1
                    if not nome:
                        rejected += 1
                        continue
                    identity = "\x1f".join((os.path.basename(csv_path), nome, cargo, orgao))
                    occurrence = occurrences.get(identity, 0) + 1
                    occurrences[identity] = occurrence
                    # Keep the original hash for the first row so existing imports
                    # remain idempotent. Distinct identical rows get stable ordinals.
                    material = identity if occurrence == 1 else f"{identity}\x1fduplicate\x1f{occurrence}"
                    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
                    cur.execute(
                        "INSERT INTO servidores (nome,nome_norm,cargo,cargo_norm,orgao,orgao_norm,source_hash,source_file) "
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (source_hash) DO NOTHING",
                        (nome, norm(nome), cargo or None, norm(cargo), orgao or None, norm(orgao), digest, os.path.basename(csv_path)),
                    )
                    inserted += cur.rowcount
    duration = time.perf_counter() - started
    return {
        "seen": seen,
        "inserted": inserted,
        "duplicates": max(0, seen - rejected - inserted),
        "rejected": rejected,
        "duration_seconds": duration,
        "rows_per_second": seen / duration if duration else 0,
        "encoding": encoding,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path")
    args = parser.parse_args()
    stats = import_file(args.csv_path)
    print(
        f"Lidos: {stats['seen']}; inseridos: {stats['inserted']}; "
        f"duplicados: {stats['duplicates']}; rejeitados: {stats['rejected']}; "
        f"tempo_s: {stats['duration_seconds']:.3f}; "
        f"linhas_s: {stats['rows_per_second']:.1f}; codificacao: {stats['encoding']}"
    )


if __name__ == "__main__":
    main()
