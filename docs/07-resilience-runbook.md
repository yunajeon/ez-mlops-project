# 장애 대응 및 운영 안정성(런북)

## 장애 유형별 대응
1) 모델 로드 실패(/readyz 503)
- 증상: readiness 실패로 트래픽 차단, 재시작 반복
- 원인: 모델 파일 손상/의존성 문제
- 대응: 이전 이미지 태그로 롤백, 모델 아티팩트 검증

2) 레이턴시 급증/타임아웃
- 증상: p95 상승, 5xx 증가
- 대응: HPA scale-out, worker/batch 조정, 리소스 상향

3) OOMKilled
- 대응: requests/limits 조정, max_length/batch 줄이기

## 배포 실패 대응
- 롤링 배포 중 readiness 실패 시 자동 중단
- Argo Rollouts 사용 시 메트릭 기반 자동 롤백
