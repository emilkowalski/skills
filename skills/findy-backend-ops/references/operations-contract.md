# FINDY Operations Contract

## 환경

- development: SQLite와 메모리 대체 구현 허용
- staging: production과 같은 종류의 PostgreSQL·Redis TLS·오브젝트 스토리지
- production: 기본 키, wildcard CORS, 자동 seed, debug 산출물 금지

## 데이터

- 마이그레이션 버전과 적용 기록을 보존
- 주요 외래키, 유일성, 조회 인덱스를 명시
- 포인트·신고·계정 삭제는 멱등성과 트랜잭션 경계 보장
- 이전 전 백업, 검증 쿼리, 실패 롤백 절차 기록

## 관측성

- 구조화 로그: request_id, route, status, latency, error class
- 지표: 인증 성공률, API 지연, 업로드 실패율, 신고 대기
- 민감정보: 토큰, OTP, 전화번호, 이메일, 쿠키, provider payload 마스킹

## 미디어

- 클라이언트는 제한된 업로드 권한만 사용
- MIME·크기 검증, EXIF 제거, 압축, 실패 재시도
- orphan 정리와 계정 삭제 상태를 감사 로그로 추적
