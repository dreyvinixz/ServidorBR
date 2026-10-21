import unittest
from unittest.mock import MagicMock, patch

from app import app, normalize


class ApiTest(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_normalize_removes_accents_and_compacts_spaces(self):
        self.assertEqual(normalize("  João   da Silva "), "JOAO DA SILVA")

    def test_unknown_parameter_is_rejected(self):
        response = self.client.get("/api/servidores?cpf=123")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"]["code"], "UNKNOWN_PARAMETER")

    def test_valid_uf_exposes_source_limitation(self):
        response = self.client.get("/api/servidores?uf=SP")
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json["error"]["code"], "UF_UNAVAILABLE")

    def test_invalid_uf_is_rejected(self):
        response = self.client.get("/api/servidores?uf=XX")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"]["code"], "INVALID_UF")

    def test_bad_pagination_is_rejected(self):
        response = self.client.get("/api/servidores?page=0")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"]["code"], "INVALID_PAGINATION")

    @patch("app.db")
    def test_user_text_is_bound_as_a_parameter(self, connect):
        conn = MagicMock()
        connect.return_value.__enter__.return_value = conn
        count = MagicMock()
        count.fetchone.return_value = {"n": 0}
        records = MagicMock()
        records.fetchall.return_value = []
        conn.execute.side_effect = [count, records]

        payload = "' OR 1=1 --"
        response = self.client.get("/api/servidores", query_string={"cargo": payload})

        self.assertEqual(response.status_code, 200)
        query, params = conn.execute.call_args_list[0].args
        self.assertNotIn(payload, query)
        self.assertEqual(params["cargo"], f"%{normalize(payload)}%")

    @patch("app.db")
    def test_similarity_escapes_trigram_operator_for_psycopg(self, connect):
        conn = MagicMock()
        connect.return_value.__enter__.return_value = conn
        count = MagicMock()
        count.fetchone.return_value = {"n": 1}
        records = MagicMock()
        records.fetchall.return_value = [{"id": 1, "nome": "MARIA SILVA", "cargo": None, "orgao": None, "uf": None}]
        conn.execute.side_effect = [count, records]

        response = self.client.get("/api/servidores", query_string={"similar": "MARIA"})

        self.assertEqual(response.status_code, 200)
        query, params = conn.execute.call_args_list[0].args
        self.assertIn("nome_norm %% %(similar)s", query)
        self.assertEqual(params["similar"], "MARIA")

    @patch("app.db")
    def test_similarity_count_below_limit_is_exact(self, connect):
        conn = MagicMock()
        connect.return_value.__enter__.return_value = conn
        count = MagicMock()
        count.fetchone.return_value = {"n": 3}
        records = MagicMock()
        records.fetchall.return_value = [
            {"id": 1, "nome": "MARIA A", "cargo": None, "orgao": None, "uf": None},
            {"id": 2, "nome": "MARIA B", "cargo": None, "orgao": None, "uf": None},
        ]
        conn.execute.side_effect = [count, records]

        response = self.client.get(
            "/api/servidores", query_string={"similar": "MARIA", "limit": 5, "per_page": 2}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["pagination"], {"page": 1, "per_page": 2, "total": 3, "pages": 2})
        count_query, params = conn.execute.call_args_list[0].args
        self.assertIn("SELECT count(*) AS n FROM (SELECT 1 FROM servidores", count_query)
        self.assertIn("LIMIT %(count_limit)s) AS matched", count_query)
        self.assertEqual(params["count_limit"], 5)

    @patch("app.db")
    def test_similarity_count_above_limit_is_capped_and_drives_pages(self, connect):
        conn = MagicMock()
        connect.return_value.__enter__.return_value = conn
        count = MagicMock()
        count.fetchone.return_value = {"n": 10}
        records = MagicMock()
        records.fetchall.return_value = [
            {"id": 5, "nome": "MARIA E", "cargo": None, "orgao": None, "uf": None},
        ]
        conn.execute.side_effect = [count, records]

        response = self.client.get(
            "/api/servidores", query_string={"similar": "MARIA", "limit": 5, "per_page": 2, "page": 3}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["pagination"], {"page": 3, "per_page": 2, "total": 5, "pages": 3})
        count_query, params = conn.execute.call_args_list[0].args
        self.assertIn("LIMIT %(count_limit)s", count_query)
        self.assertEqual(params["count_limit"], 5)
        result_query, result_params = conn.execute.call_args_list[1].args
        self.assertIn("LIMIT %(limit)s OFFSET %(offset)s", result_query)
        self.assertEqual(result_params["limit"], 1)
        self.assertEqual(result_params["offset"], 4)

    @patch("app.db")
    def test_non_similarity_count_remains_exact(self, connect):
        conn = MagicMock()
        connect.return_value.__enter__.return_value = conn
        count = MagicMock()
        count.fetchone.return_value = {"n": 3}
        records = MagicMock()
        records.fetchall.return_value = []
        conn.execute.side_effect = [count, records]

        response = self.client.get("/api/servidores?cargo=ANALISTA&per_page=2")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["pagination"]["total"], 3)
        count_query, params = conn.execute.call_args_list[0].args
        self.assertEqual(count_query, "SELECT count(*) AS n FROM servidores WHERE cargo_norm LIKE %(cargo)s")
        self.assertNotIn("count_limit", params)

    @patch("app.db")
    def test_search_options_returns_values_from_database(self, connect):
        conn = MagicMock()
        connect.return_value.__enter__.return_value = conn
        cargos = MagicMock()
        cargos.fetchall.return_value = [{"cargo": "ANALISTA"}, {"cargo": "PROFESSOR"}]
        orgaos = MagicMock()
        orgaos.fetchall.return_value = [{"orgao": "MINISTERIO"}]
        conn.execute.side_effect = [cargos, orgaos]

        response = self.client.get("/api/opcoes")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"cargos": ["ANALISTA", "PROFESSOR"], "orgaos": ["MINISTERIO"]})
        self.assertIn("SELECT DISTINCT cargo", conn.execute.call_args_list[0].args[0])
        self.assertIn("SELECT DISTINCT orgao", conn.execute.call_args_list[1].args[0])


if __name__ == "__main__":
    unittest.main()
