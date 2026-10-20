import os
import unicodedata

import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import dict_row

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://servidorbr:local-dev-only@localhost:5432/servidorbr")
app = Flask(__name__)


def normalize(value):
    value = unicodedata.normalize("NFKD", value)
    return " ".join("".join(ch for ch in value if not unicodedata.combining(ch)).upper().split())


def db():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row, connect_timeout=3)


@app.get("/api/health")
def health():
    try:
        with db() as conn:
            conn.execute("SELECT 1")
        return jsonify(status="ok", database="ok")
    except psycopg.Error:
        return jsonify(error={"code": "DATABASE_UNAVAILABLE", "message": "Banco de dados indisponível."}), 503
