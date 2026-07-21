# FINDY Release Gates

## 자동 확인

- FINDY 제품명과 단일 릴리스 설정
- bundle/application ID, semantic version, 증가한 build number
- debug 서명·debuggable 산출물 차단
- 공개 HTTPS URL 형식과 응답
- 민감 파일, DB, 빌드 결과물, 개인정보 문서의 공개 추적 여부
- 서버 production fail-fast와 명시적 CORS

## 외부 증빙

- Android/iOS 실기기 핵심 흐름
- 실제 release signing과 스토어 업로드
- SMS, OAuth, PASS, 복구 이메일
- APNs/FCM 권한과 실제 수신
- 운영자 정보와 고객지원 연락처
- 법률 검토된 약관, 개인정보처리방침, 만 14세 정책

외부 증빙이 하나라도 필수인데 없으면 `blocked` 또는 `unverified`로 유지한다.
