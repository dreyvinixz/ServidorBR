import os
import re
import unicodedata
import time

import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import dict_row

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://servidorbr:local-dev-only@localhost:5432/servidorbr")
app = Flask(__name__)
ALLOWED = {"nome", "cargo", "orgao", "uf", "similar", "page", "per_page", "limit"}
VALID_UF = set("AC AL AP AM BA CE DF GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO ES".split())


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


@app.get("/api/servidores")
def search():
    filters, params = [], {}
    for key, column in (("nome", "nome_norm"), ("cargo", "cargo_norm"), ("orgao", "orgao_norm")):
        value = request.args.get(key)
        if value is not None:
            value = normalize(value)
            if key == "nome":
                filters.append(f"{column} = %({key})s")
                params[key] = value
            else:
                filters.append(f"{column} LIKE %({key})s")
                params[key] = f"%{value}%"
    where = " WHERE " + " AND ".join(filters) if filters else ""
    started = time.perf_counter()
    with db() as conn:
        total = conn.execute(f"SELECT count(*) AS n FROM servidores{where}", params).fetchone()["n"]
        rows = conn.execute(
            f"SELECT id,nome,cargo,orgao,uf FROM servidores{where} ORDER BY nome_norm LIMIT 25", params
        ).fetchall()
    return jsonify(data=rows, pagination={"page": 1, "per_page": 25, "total": total, "pages": (total + 24) // 25}, query_time_ms=round((time.perf_counter() - started) * 1000, 2))
