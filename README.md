# Ezcaretech MLOps Assignment Starter (KR-FinBert Sentiment)

This repo is a **2-day execution-oriented** starter:
- FastAPI REST serving
- Docker + docker-compose (with OSS observability stack)
- Prometheus metrics, structured logs, OTEL traces
- Automated tests + simple load benchmark script
- Kubernetes manifests (deployment/service/hpa/pdb/netpol)
- CI pipeline example (GitHub Actions)

> Model: `snunlp/KR-FinBert-SC`

## 0) Prereqs (Ubuntu 22.04)
- Python 3.11
- Docker + Docker Compose v2

## 1) Local run (recommended first)
```bash
make venv
make install
make download-model
make run
```

Test:
```bash
curl -s http://localhost:8000/healthz
curl -s http://localhost:8000/readyz
curl -s -X POST http://localhost:8000/v1/predict \
  -H 'Content-Type: application/json' \
  -d '{"text":"실적이 개선되어 주가가 상승했다."}'
```

## 2) Tests
Fast tests:
```bash
make test
```

Real-model e2e test (requires local model):
```bash
make e2e
```

## 3) Docker image build/run
```bash
make docker-build
make docker-run
```

## 4) Full stack (API + Prometheus + Grafana + Loki + Tempo)
```bash
make compose-up
```

Open:
- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

Shutdown:
```bash
make compose-down
```

## 5) Benchmark (for throughput/latency numbers)
```bash
make bench
```

It prints JSON with p50/p95/p99 and QPS.
Use this output directly in your report.

## 6) Kubernetes manifests
See `k8s/`.

## 7) Docs
See `docs/` for the report skeleton you should fill.
