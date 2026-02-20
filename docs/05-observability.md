# 모니터링/로깅/트레이싱(Observability)

## 메트릭(예: Prometheus)
- 요청 수/에러율
- 레이턴시 p95
- 추론 시간
- 모델 로딩 상태(model_loaded)

## 로그(예: Loki)
- JSON 구조화 로그
- request_id 포함(상관관계 분석)

## 트레이스(예: Tempo)
- OTEL로 FastAPI tracing
- traces-to-logs 연결(Tempo→Loki)

## 알림(설계)
- SLO 기반(에러율/ready 실패/latency p95)
- Alertmanager로 라우팅(메일/슬랙은 사내 시스템 가정)
