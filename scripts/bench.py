import argparse
import asyncio
import json
import time
from statistics import mean

import httpx

DEFAULT_TEXT = "삼성전자 실적이 시장 기대치를 상회하며 주가가 상승했다."

def percentile(values, p):
    if not values:
        return None
    values = sorted(values)
    k = (len(values) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(values) - 1)
    if f == c:
        return values[f]
    return values[f] + (values[c] - values[f]) * (k - f)

async def worker(client, url, payload, n, latencies, errors):
    for _ in range(n):
        t0 = time.perf_counter()
        try:
            r = await client.post(url, json=payload, timeout=10.0)
            dt = time.perf_counter() - t0
            latencies.append(dt)
            if r.status_code != 200:
                errors.append((r.status_code, r.text[:200]))
        except Exception as e:
            dt = time.perf_counter() - t0
            latencies.append(dt)
            errors.append(("exc", str(e)))

async def run(url, concurrency, total_requests, batch_size, text):
    per_worker = total_requests // concurrency
    remainder = total_requests % concurrency

    payload = {"texts": [text] * batch_size, "return_all_scores": True}

    latencies = []
    errors = []

    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(concurrency):
            n = per_worker + (1 if i < remainder else 0)
            tasks.append(asyncio.create_task(worker(client, url, payload, n, latencies, errors)))

        t0 = time.perf_counter()
        await asyncio.gather(*tasks)
        total_time = time.perf_counter() - t0

    # Note: Each request includes batch_size texts. Effective text-inferences = total_requests * batch_size
    qps = total_requests / total_time
    ips = (total_requests * batch_size) / total_time  # inferences per second

    report = {
        "url": url,
        "concurrency": concurrency,
        "total_requests": total_requests,
        "batch_size": batch_size,
        "duration_s": total_time,
        "qps": qps,
        "inferences_per_s": ips,
        "latency_s": {
            "p50": percentile(latencies, 50),
            "p95": percentile(latencies, 95),
            "p99": percentile(latencies, 99),
            "avg": mean(latencies) if latencies else None,
            "max": max(latencies) if latencies else None,
        },
        "errors": errors[:10],
        "error_count": len(errors),
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="http://localhost:8000/v1/predict")
    p.add_argument("--concurrency", type=int, default=10)
    p.add_argument("--requests", type=int, default=200)
    p.add_argument("--batch-size", type=int, default=4)
    p.add_argument("--text", default=DEFAULT_TEXT)
    args = p.parse_args()
    asyncio.run(run(args.url, args.concurrency, args.requests, args.batch_size, args.text))

if __name__ == "__main__":
    main()
