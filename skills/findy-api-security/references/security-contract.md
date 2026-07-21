# FINDY Security Contract

## 신뢰 경계

- 사용자 ID: 검증된 세션 토큰의 subject
- 관리자 권한: 별도 관리자 인증과 서버 측 역할
- 리소스 접근: 소유자, 공개 범위, 관리자 역할을 서버에서 판정
- 클라이언트 필드: 표시·필터 입력일 뿐 권한 근거가 아님

## Challenge 저장

- 필드: digest, purpose, target, expires_at, attempts, created_at
- 운영: `rediss://` 공유 저장소와 원자적 검증·소비
- 개발: 동일 repository 인터페이스를 구현하는 메모리 TTL 저장소
- 성공한 challenge는 한 번만 소비되고 재사용할 수 없음
- 발송 실패 시 challenge를 남기지 않음

## 필수 회귀

- 인증 없음, 변조·만료 토큰, 타인 리소스
- 잘못된 관리자 키와 운영 기본 키
- OTP 만료, 오입력 한도, 재전송 cooldown
- 다른 인스턴스 간 요청·검증, 동시 성공 경쟁, Redis 장애
- 계정 연결 해제, 로그아웃, 탈퇴의 멱등성과 부분 실패
