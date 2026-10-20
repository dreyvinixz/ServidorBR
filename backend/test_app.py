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


if __name__ == "__main__":
    unittest.main()
