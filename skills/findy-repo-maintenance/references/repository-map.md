# FINDY Repository Map

| 경로 | 책임 |
| --- | --- |
| `app/` | Flet 사용자 앱 |
| `auth/` | 인증 gateway |
| `api/` | 사용자·관리 API |
| `security/` | 공유 보안 primitive |
| `ops/` | 컨테이너와 배포 설정 |
| `site/` | 공개 소개·정책 사이트 |
| `assets/` | 실제 앱·사이트가 참조하는 에셋 |
| `promo/` | 홍보 산출물과 생성 원본 |
| `docs/` | 제품·개발·법무·운영 문서 |
| `scripts/` | 빌드·검사·마이그레이션 명령 |
| `tests/` | 단위·통합·스모크 계약 |
| `archive/` | 현재 런타임에서 사용하지 않는 보관 자료 |

## 이름 변경 검사

- Python import와 package init
- asset path와 Flet `src`
- Docker context, compose, Kubernetes, CI
- Markdown 링크와 명령 예시
- release 설정과 사이트 public path
- 테스트 fixture와 monkeypatch target

정리 후 `rg`로 이전 경로가 호환 목적 외에 남았는지 확인한다.
