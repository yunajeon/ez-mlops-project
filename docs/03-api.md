# 모델 서빙 API

## 엔드포인트
- POST /v1/predict
- GET /healthz
- GET /readyz
- GET /metrics
- GET /version

## 요청/응답 예시
- (curl 결과 캡처 붙여넣기)

## 의사결정 근거
- FastAPI: 생산성/타입힌트/테스트 용이
- /readyz: 모델 로딩 실패 시 트래픽 차단
