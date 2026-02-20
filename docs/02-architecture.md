# 아키텍처 설계

## 선택한 아키텍처
- Serving: FastAPI + Gunicorn(UvicornWorker)
- Packaging: Docker image에 모델 포함(빌드 시 snapshot_download)
- Observability: Prometheus/Grafana + Loki/Promtail + Tempo + OpenTelemetry
- CD: GitOps(Argo CD) 기반(설계)

## 데이터 플로우
1) Client → /v1/predict
2) API → tokenizer/model inference
3) 결과 응답 + metrics/logs/traces 기록
4) Prometheus/Grafana, Loki, Tempo로 수집/조회

## 가용성/안정성 요소
- readiness/liveness
- rollingUpdate(maxUnavailable=0)
- replicas=2 + PDB(minAvailable=1)
- resource requests/limits
