# CI/CD 파이프라인 설계

## 목표
- 모델 업데이트(월 1~2회)를 **완전 자동화**로 배포
- 테스트/보안 스캔 통과 시에만 배포
- 롤백 가능(이전 이미지 태그)

## CI (예: GitHub Actions)
- 단위 테스트 → 이미지 빌드(모델 포함) → 스모크 테스트 → (옵션) 레지스트리 푸시
- 파일: `.github/workflows/ci.yml`

## CD (GitOps)
- 매니페스트 repo 변경 감지(Argo CD) → 자동 롤링 배포
- (옵션) Argo Rollouts로 카나리 + 메트릭 기반 자동 롤백

## 트레이드오프
- 직접 kubectl 배포(간단) vs GitOps(운영자 없는 팀에 적합)
