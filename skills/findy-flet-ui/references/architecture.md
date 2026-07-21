# FINDY Frontend Architecture

## 공식 실행 경로

```text
main.py
  -> app.runtime.main
  -> shared state and route assembly
  -> app/screens/*
```

삭제되거나 보관된 구형 FINDY/FINDY2 경로를 다시 만들지 않는다.

## 디렉터리 책임

| 경로 | 책임 |
| --- | --- |
| `app/screens/` | 화면별 Flet UI와 화면 전용 이벤트 |
| `app/ui/` | 토큰 alias, primitive, header, shell, toast, safe area |
| `app/components/` | 카드, 레이아웃, 오버레이, 리뷰 표현 |
| `app/core/` | 설정과 세션 상태 |
| `app/data/` | 표시 데이터, 카테고리, 정책 콘텐츠 |
| `app/features/` | 커뮤니티, 리뷰, 미디어, 안전 정책 로직 |
| `app/services/` | API, 인증, 사용자, 미디어, 동기화 연결 |
| `assets/` | 앱에서 실제 사용하는 로고, 아이콘, 미디어, 폰트 |
| `tests/` | 단위, 통합, 스모크 테스트 |
| `site/` | FINDY 공식 소개·정책 사이트 |
| `archive/` | 현재 앱이 참조하지 않는 보관 자료 |

## 배치 원칙

- 두 화면 이상에서 재사용되는 시각 요소는 `app/ui` 또는 `app/components`에 둔다.
- 화면 전용 조합은 `app/screens`에 둔다.
- API 호출과 저장 정책은 화면 함수 안에 직접 누적하지 않고 `app/services`로 보낸다.
- 필터링·정렬·신고·포인트 같은 도메인 규칙은 `app/features`에 둔다.
- `app/runtime.py`에는 전역 상태 조립과 화면 전환 연결을 중심으로 남긴다.
- 순환 import를 피하기 위해 하위 모듈이 runtime의 내부 함수를 직접 import하지 않게 한다. 필요한 callback과 state를 인자로 전달한다.

## 변경 판단

1. 동일한 문제가 여러 화면에서 발생하는가?
   - 예: 공통 primitive를 수정하고 모든 호출부를 검증한다.
   - 아니오: 화면 모듈에 국소 수정한다.
2. 시각 표현인가, 서비스 동작인가?
   - 시각: `app/ui`, `app/components`, `app/screens`.
   - 서비스: `app/services` 또는 `app/features`.
3. 기존 helper가 있는가?
   - 있으면 확장한다. 비슷한 helper를 새로 복제하지 않는다.

## 현재 주요 source of truth

- 디자인 수치: `app/components/layout.py`, `app/ui/tokens.py`
- 공통 칩·탭·뒤로가기: `app/ui/primitives.py`
- 상단 액션: `app/ui/header.py`
- 하단 안전영역: `app/ui/safe.py`
- 토스트: `app/ui/toast.py`
- 출시 UX 계약: `docs/FRONTEND_QA.md`
- 작업 원칙: `docs/WORK_RULES.md`
