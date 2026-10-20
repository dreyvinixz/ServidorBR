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


def error(code, message, status):
    return jsonify(error={"code": code, "message": message}), status


@app.get("/api/servidores")
def search():
    unknown = set(request.args) - ALLOWED
    if unknown:
        return error("UNKNOWN_PARAMETER", "Parâmetro de busca desconhecido.", 400)

    def integer(key, default, maximum):
        raw = request.args.get(key, str(default))
        if not re.fullmatch(r"[0-9]+", raw):
            raise ValueError(key)
        value = int(raw)
        if not 1 <= value <= maximum:
            raise ValueError(key)
        return value

    try:
        page = integer("page", 1, 1_000_000)
        per_page = integer("per_page", 25, 100)
        limit = integer("limit", 100, 100)
    except ValueError as exc:
        return error("INVALID_PAGINATION", f"Parâmetro inválido: {exc.args[0]}.", 400)

    filters, params = [], {}
    for key, column in (("nome", "nome_norm"), ("cargo", "cargo_norm"), ("orgao", "orgao_norm")):
        value = request.args.get(key)
        if value is not None:
            value = normalize(value)
            maximum = 160 if key == "orgao" else 120
            if not value or len(value) > maximum:
                return error("INVALID_QUERY", f"{key} deve ter entre 1 e {maximum} caracteres.", 400)
            if key == "nome":
                filters.append(f"{column} = %({key})s")
                params[key] = value
            else:
                filters.append(f"{column} LIKE %({key})s")
                params[key] = f"%{value}%"
    similar = request.args.get("similar")
    if similar is not None:
        similar = normalize(similar)
        if not 2 <= len(similar) <= 120:
            return error("INVALID_QUERY", "similar deve ter entre 2 e 120 caracteres.", 400)
        params["similar"] = similar.replace("%", "")
        params["pattern"] = f"%{similar}%"
        filters.extend(["nome_norm % %(similar)s", "nome_norm LIKE %(pattern)s"])
    where = " WHERE " + " AND ".join(filters) if filters else ""
    page_size = min(per_page, limit) if similar is not None else per_page
    params.update(limit=page_size, offset=(page - 1) * page_size)
    started = time.perf_counter()
    with db() as conn:
        total = conn.execute(f"SELECT count(*) AS n FROM servidores{where}", params).fetchone()["n"]
        order = "similarity(nome_norm, %(similar)s) DESC, nome_norm" if similar is not None else "nome_norm"
        rows = conn.execute(
            f"SELECT id,nome,cargo,orgao,uf FROM servidores{where} ORDER BY {order} LIMIT %(limit)s OFFSET %(offset)s", params
        ).fetchall()
    return jsonify(data=rows, pagination={"page": page, "per_page": page_size, "total": total, "pages": (total + page_size - 1) // page_size}, query_time_ms=round((time.perf_counter() - started) * 1000, 2))
