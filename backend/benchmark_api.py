"""Measure sequential local API search latency without printing personal records."""
import argparse
import json
import math
import statistics
import time
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen


def request_json(base_url, params):
    url = f"{base_url.rstrip('/')}/api/servidores?{urlencode(params)}"
    started = time.perf_counter()
    try:
        with urlopen(url, timeout=15) as response:
            body = json.load(response)
            status = response.status
    except HTTPError as exc:
        raise RuntimeError(f"API returned HTTP {exc.code}") from exc
    elapsed_ms = (time.perf_counter() - started) * 1000
    if status != 200:
        raise RuntimeError(f"API returned HTTP {status}")
    return body, elapsed_ms


def percentile(values, fraction):
    ordered = sorted(values)
    index = max(0, math.ceil(fraction * len(ordered)) - 1)
    return ordered[index]


def measure(base_url, runs):
    baseline, _ = request_json(base_url, {"cargo": "AGENTE ADMINISTRATIVO", "per_page": 1})
    if not baseline["data"]:
        raise RuntimeError("Benchmark precisa de pelo menos um registro importado.")
    scenarios = (
        ("nome_exato_sem_resultado", {"nome": "BENCHMARK SEM RESULTADO", "per_page": 1}),
        ("cargo_parcial", {"cargo": "AGENTE ADMINISTRATIVO", "per_page": 1}),
        ("orgao_parcial", {"orgao": "MINISTERIO", "per_page": 1}),
        ("similaridade_nome", {"similar": "MARIA", "limit": 100, "per_page": 1}),
    )
    results = []
    for label, params in scenarios:
        first, _ = request_json(base_url, params)
        samples = [request_json(base_url, params)[1] for _ in range(runs)]
        results.append({
            "scenario": label,
            "samples": runs,
            "matching_rows": first["pagination"]["total"],
            "mean_ms": round(statistics.mean(samples), 3),
            "p50_ms": round(statistics.median(samples), 3),
            "p95_ms": round(percentile(samples, 0.95), 3),
            "p99_ms": round(percentile(samples, 0.99), 3),
            "max_ms": round(max(samples), 3),
        })
    return {"base_url": base_url, "runs_per_scenario": runs, "measurements": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:3000")
    parser.add_argument("--runs", type=int, default=20)
    args = parser.parse_args()
    if not 1 <= args.runs <= 25:
        parser.error("--runs deve estar entre 1 e 25 para respeitar o rate limit local.")
    print(json.dumps(measure(args.base_url, args.runs), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
