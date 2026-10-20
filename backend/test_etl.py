import csv
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import etl


class FakeCursor:
    def __init__(self, database):
        self.database = database
        self.rowcount = 0

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute(self, query, params):
        self.database.statements.append((query, params))
        digest = params[6]
        self.rowcount = int(digest not in self.database.hashes)
        self.database.hashes.add(digest)


class FakeDatabase:
    def __init__(self):
        self.hashes = set()
        self.statements = []
        self.cursor_value = FakeCursor(self)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def cursor(self):
        return self.cursor_value


class EtlTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.path = Path(self.temp_dir.name) / "sample.csv"
        self.database = FakeDatabase()
        self.connection = patch("etl.psycopg.connect", side_effect=lambda *args, **kwargs: self.database)
        self.connection.start()
        self.addCleanup(self.connection.stop)

    def write_headered(self, delimiter, rows, encoding="utf-8-sig"):
        with self.path.open("w", encoding=encoding, newline="") as output:
            writer = csv.writer(output, delimiter=delimiter)
            writer.writerow(["Nome", "CPF", "Matrícula do Servidor", "Nome do órgão", "Cargo"])
            writer.writerows(rows)

    def test_repeated_official_records_are_preserved_and_reimport_is_idempotent(self):
        self.write_headered(
            ";",
            [
                ["João da Silva", "***123456**", "000000001", "Órgão Público", "Técnico"],
                ["João da Silva", "***123456**", "000000001", "Órgão Público", "Técnico"],
            ],
        )

        first = etl.import_file(self.path)
        second = etl.import_file(self.path)

        self.assertEqual((first["seen"], first["inserted"], first["duplicates"]), (2, 2, 0))
        self.assertEqual((second["seen"], second["inserted"], second["duplicates"]), (2, 0, 2))
        self.assertEqual(len(self.database.hashes), 2)
        identity = "\x1f".join((self.path.name, "João da Silva", "Técnico", "Órgão Público"))
        self.assertEqual(self.database.statements[0][1][6], hashlib.sha256(identity.encode()).hexdigest())
        self.assertNotIn("***123456**", repr(self.database.statements))
        self.assertNotIn("000000001", repr(self.database.statements))

    def test_headered_csv_accepts_comma_semicolon_and_tab_delimiters(self):
        for delimiter in (",", ";", "\t"):
            with self.subTest(delimiter=repr(delimiter)):
                self.database = FakeDatabase()
                self.write_headered(delimiter, [["Ana", "***000000**", "123", "Órgão", "Analista"]])

                stats = etl.import_file(self.path)

                self.assertEqual((stats["seen"], stats["inserted"], stats["rejected"]), (1, 1, 0))
                self.assertEqual(self.database.statements[0][1][0], "Ana")

    def test_blank_names_are_rejected_without_database_write(self):
        self.write_headered(",", [["", "***000000**", "123", "Órgão", "Analista"]])

        stats = etl.import_file(self.path)

        self.assertEqual((stats["seen"], stats["inserted"], stats["rejected"]), (1, 0, 1))
        self.assertEqual(self.database.statements, [])

    def test_official_headerless_cp1252_format_reads_only_search_fields(self):
        fields = [
            "João Silva", "***123456**", "000000001", "Ministério Público", "MP", "00000",
            "Técnico", "A", "001", "00", "001", "VOLUNTÁRIA", "Fundamento", "Portaria",
            "01012025", "Concurso", "01011990", "4.188,35\x00",
        ]
        with self.path.open("w", encoding="cp1252", newline="") as output:
            csv.writer(output, delimiter=";").writerow(fields)

        stats = etl.import_file(self.path)

        self.assertEqual(stats["encoding"], "cp1252")
        self.assertEqual((stats["seen"], stats["inserted"], stats["rejected"]), (1, 1, 0))
        params = self.database.statements[0][1]
        self.assertEqual((params[0], params[2], params[4]), ("João Silva", "Técnico", "Ministério Público"))
        self.assertNotIn("***123456**", repr(self.database.statements))
        self.assertNotIn("000000001", repr(self.database.statements))


if __name__ == "__main__":
    unittest.main()
