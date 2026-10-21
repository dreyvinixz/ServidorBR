"""Measure concurrent local API latency and Docker resource use without printing records."""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


QUERY = {"similar": "MARIA", "limit": 100, "per_page": 1}
DOCKER_STATS_FORMAT = "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}"


def percentile(values, fraction):
    ordered = sorted(values)
    index = max(0, math.ceil(fraction * len(ordered)) - 1)
    return ordered[index]


def memory_mib(value):
    match = re.fullmatch(r"([0-9.]+)\s*([KMG]i?B)", value.strip(), re.IGNORECASE)
    if not match:
        return None
    amount = float(match.group(1))
    unit = match.group(2).lower()
    scale = {"kb": 1 / 1024, "kib": 1 / 1024, "mb": 1, "mib": 1,
             "gb": 1024, "gib": 1024}[unit]
    return amount * scale


class DockerStatsSampler:
    def __init__(self, interval_seconds):
        self.interval_seconds = interval_seconds
        self.stop_event = threading.Event()
        self.samples = defaultdict(lambda: {"cpu": [], "memory_mib": []})
        self.errors = []
        self.thread = threading.Thread(target=self._sample_loop, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *_):
        self.stop_event.set()
        self.thread.join(timeout=5)

    def _sample_loop(self):
        while not self.stop_event.is_set():
            try:
                result = subprocess.run(
                    ["docker", "stats", "--no-stream", "--format", DOCKER_STATS_FORMAT],
                    capture_output=True, text=True, check=True, timeout=5,
                )
                for line in result.stdout.splitlines():
                    parts = line.split("|", 2)
                    if len(parts) != 3:
                        continue
                    name, cpu_text, memory_text = parts
                    cpu = float(cpu_text.rstrip("%"))
                    used_memory = memory_mib(memory_text.split("/", 1)[0])
                    self.samples[name]["cpu"].append(cpu)
                    if used_memory is not None:
                        self.samples[name]["memory_mib"].append(used_memory)
            except (OSError, subprocess.SubprocessError, ValueError) as exc:
                self.errors.append(type(exc).__name__)
            self.stop_event.wait(self.interval_seconds)

    def summary(self):
        result = {}
        for name, values in sorted(self.samples.items()):
            cpu = values["cpu"]
            memory = values["memory_mib"]
            result[name] = {
                "samples": len(cpu),
                "cpu_avg_percent": round(statistics.mean(cpu), 2) if cpu else None,
                "cpu_peak_percent": round(max(cpu), 2) if cpu else None,
                "memory_peak_mib": round(max(memory), 2) if memory else None,
            }
        return {"containers": result, "sampling_errors": dict(Counter(self.errors))}


def one_request(base_url, timeout):
    url = f"{base_url.rstrip('/')}/api/servidores?{urlencode(QUERY)}"
    started = time.perf_counter()
    try:
        with urlopen(url, timeout=timeout) as response:
            body = json.load(response)
            status = response.status
        return status, (time.perf_counter() - started) * 1000, body["pagination"]["total"]
    except HTTPError as exc:
        return exc.code, (time.perf_counter() - started) * 1000, None
    except (URLError, TimeoutError, OSError) as exc:
        reason = getattr(exc, "reason", exc)
        return f"error:{type(reason).__name__}", (time.perf_counter() - started) * 1000, None


def run_level(base_url, concurrency, request_count, timeout, stats_interval):
    start = time.perf_counter()
    with DockerStatsSampler(stats_interval) as sampler:
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = [pool.submit(one_request, base_url, timeout) for _ in range(request_count)]
            responses = [future.result() for future in as_completed(futures)]
    duration = time.perf_counter() - start
    latencies = [latency for status, latency, _ in responses]
    statuses = Counter(str(status) for status, _, _ in responses)
    successful = [total for status, _, total in responses if status == 200]
    return {
        "concurrency": concurrency,
        "requests": request_count,
        "duration_seconds": round(duration, 3),
        "rps": round(request_count / duration, 3),
        "successes": len(successful),
        "errors": request_count - len(successful),
        "status_counts": dict(sorted(statuses.items())),
        "matching_rows": successful[0] if successful else None,
        "mean_ms": round(statistics.mean(latencies), 3) if latencies else None,
        "p50_ms": round(statistics.median(latencies), 3) if latencies else None,
        "p95_ms": round(percentile(latencies, 0.95), 3) if latencies else None,
        "p99_ms": round(percentile(latencies, 0.99), 3) if latencies else None,
        "max_ms": round(max(latencies), 3) if latencies else None,
        "resources": sampler.summary(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://localhost:3000")
    parser.add_argument("--levels", default="1,2,4,8", help="Níveis de concorrência separados por vírgula")
    parser.add_argument("--requests", type=int, default=20, help="Requisições em cada nível")
    parser.add_argument("--timeout", type=float, default=20)
    parser.add_argument("--stats-interval", type=float, default=1)
    parser.add_argument("--output", help="Caminho opcional para salvar o JSON sem dados pessoais")
    args = parser.parse_args()
    try:
        levels = [int(value) for value in args.levels.split(",")]
    except ValueError:
        parser.error("--levels deve conter inteiros separados por vírgula")
    if not levels or any(level < 1 or level > 32 for level in levels):
        parser.error("cada nível deve estar entre 1 e 32")
    if len(set(levels)) != len(levels):
        parser.error("--levels não pode repetir níveis")
    if not 1 <= args.requests <= 25 or len(levels) * args.requests > 100:
        parser.error("use 1-25 requisições por nível e no máximo 100 no total para respeitar o rate limit")
    if args.timeout <= 0 or args.stats_interval <= 0:
        parser.error("timeouts e intervalo de coleta devem ser positivos")

    warmup_status, _, _ = one_request(args.base_url, args.timeout)
    if warmup_status != 200:
        parser.error(f"requisição de aquecimento retornou {warmup_status}")
    results = [run_level(args.base_url, level, args.requests, args.timeout, args.stats_interval)
               for level in levels]
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "base_url": args.base_url,
        "scenario": QUERY,
        "warmup_requests": 1,
        "requests_per_level": args.requests,
        "levels": levels,
        "resource_sampling_interval_seconds": args.stats_interval,
        "measurements": results,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
