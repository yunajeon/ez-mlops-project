# 보안/거버넌스 고려

## 보안
- 최소권한: serviceAccountToken 비활성화, non-root 실행
- 네트워크: NetworkPolicy로 통신 범위 제한
- 시크릿: Secret/외부 시크릿 매니저(사내) 연동 가정
- 공급망: 의존성 pinning, 이미지 스캔(Trivy), SBOM 생성(설계)

## 모델 거버넌스
- 모델 버전 추적: MODEL_VERSION / 이미지 태그
- 프로비넌스: 모델 소스(HF repo) + 해시 기록
- 배포 승인: PR 리뷰(개발자 5명 체계) + 자동 테스트 통과
