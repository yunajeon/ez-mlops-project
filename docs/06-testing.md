# 자동화된 테스트

## 테스트 구성
- Unit/Contract: API 스키마 및 라우팅(모델 mock)
- E2E: 실제 모델 로딩 및 추론 (pytest -m e2e)

## 실행 결과
- `pytest` 로그 캡처
- `pytest -m e2e` 로그 캡처

## 부하/성능 측정
- `python scripts/bench.py ...` 결과(JSON) 첨부
