---
name: findy-flet-ui
description: FINDY Flet 앱의 화면, 공통 카드, 칩, 버튼, 상단 헤더, 하단 내비게이션, 토스트를 구현하거나 리팩터링할 때 사용한다. 기존 동작과 사용자 변경을 보존하면서 FINDY 디자인 토큰, 모바일 안전영역, 접근성, 화면별 모듈 구조를 일관되게 적용해야 하는 작업에 적합하다.
---

# FINDY Flet UI

FINDY의 실제 Flet 코드에 변경을 적용하는 구현 스킬이다. 새 화면을 만들거나 UI 회귀를 고칠 때 현재 앱의 공통 컴포넌트와 제품 결정을 우선한다.

## 작업 순서

1. 저장소 루트를 찾고 `AGENTS.md`, `PROJECT_RULES.md`, `docs/WORK_RULES.md`, `docs/FRONTEND_QA.md` 중 존재하는 파일을 읽는다.
2. `git status --short`로 기존 변경을 확인한다. 사용자가 만든 변경은 되돌리거나 덮어쓰지 않는다.
3. `main.py`에서 실제 실행 경로를 추적한다. FINDY의 현재 공식 경로는 `main.py -> app/runtime.py`다.
4. 대상 화면과 연결된 `app/screens`, `app/ui`, `app/components`, `app/services`를 읽는다.
5. 두 화면 이상에서 같은 요소를 고칠 때만 공통 primitive를 수정한다. 한 화면에만 해당하면 화면 모듈에 국소 적용한다.
6. [디자인 시스템](references/design-system.md)과 [코드 구조](references/architecture.md)를 기준으로 최소 변경을 구현한다.
7. 로딩, 빈 상태, 오류, 재시도, 키보드, 스크롤 복원, 하단 안전영역까지 확인한다.
8. 변경 범위에 맞는 테스트와 `git diff --check`를 실행한다.

## 구현 원칙

- Flet과 저장소에 이미 있는 helper API를 사용한다. React, CSS, 웹 전용 UI 라이브러리 관행을 그대로 옮기지 않는다.
- 사용자에게 기능 추가가 아니라 시안이나 의견만 요청받았다면 코드를 수정하지 않는다.
- 사용자가 확정한 로고, 아이콘, 사진을 임의로 다시 그리거나 형태를 바꾸지 않는다. 요청된 크롭, 여백, 선 굵기, 크기만 조정한다.
- 공통 UI를 바꾸면 실제로 그 primitive를 쓰는 모든 화면을 확인한다. 화면마다 복사된 수치를 추가하지 않는다.
- `Container.on_click`을 사용할 때도 44pt 터치 영역, tooltip, 고정 크기를 보장한다. 현재 Flet 런타임에서 안전한 접근성 API만 사용한다.
- 버튼 글자는 시각적 중앙에 맞추고 동적 콘텐츠가 부모 크기를 바꾸지 않게 한다.
- 하단 내비게이션, FAB, 토스트, 키보드가 본문과 겹치지 않도록 `app/ui/safe.py`의 계산을 재사용한다.
- 자주 쓰는 전환은 140~220ms의 짧은 ease-out 범위에서 기존 motion을 따른다. 화면 전체 깜빡임이나 스크롤 초기화를 만들지 않는다.
- 예약, 결제, 정산, 아티스트 입점 기능은 명시적으로 요청되고 제품 범위가 열리기 전까지 활성화하지 않는다.

## FINDY 고정 계약

- 홈의 여섯 분야는 2행 3열 구조를 유지한다.
- 일반 탐색 아이콘은 브라운 또는 무채색으로 두고 신뢰·상태 정보에만 의미 색을 사용한다.
- 좋아요와 저장은 선택 시 아이콘을 채우되 카드 배경은 바꾸지 않는다.
- 커뮤니티 카드에는 글 미리보기를 3~4줄 노출하고 긴 글의 `더보기`는 상세로 이동한다.
- 카드 메타 정보는 분야를 먼저 표시한다. 예: `헤어 · 커뮤니티`, `네일아트 · 스냅`.
- 글쓰기 FAB는 커뮤니티, 스냅, 비디오에서만 노출한다.
- 페이지 크기는 커뮤니티 10개, 스냅 1열 12개, 스냅 3열 36개를 유지한다.
- 스크린샷은 내부 검증에 사용할 수 있지만 사용자가 요청하지 않으면 결과 메시지에 첨부하지 않는다.

## 검증

작은 시각 수정은 최소한 컴파일, 관련 테스트, diff 검사를 수행한다. 공통 shell이나 상태 흐름을 바꾸면 전체 검증을 수행한다.

```bash
PYTHONPYCACHEPREFIX="${TMPDIR:-/tmp}/findy_pycache" python3 -m compileall -q main.py app
PYTHONPYCACHEPREFIX="${TMPDIR:-/tmp}/findy_pycache" python3 -m unittest discover -s tests -p 'test_*.py'
PYTHONPYCACHEPREFIX="${TMPDIR:-/tmp}/findy_pycache" python3 tests/smoke.py
python3 scripts/check_repo.py
(cd site && npm test && npm run lint)
git diff --check
```

실행하지 못한 검증은 성공으로 표현하지 말고 이유와 남은 위험을 보고한다.

## Git 게시 절차

커밋이나 푸시는 사용자가 요청했을 때만 한다. 커밋 전 `git status`, `git diff --cached`, `.gitignore`, 추적 중인 민감 파일을 확인한다. `.env`, DB, 키, 토큰, 개인정보 문서, 민감 PDF, 빌드·캐시 산출물이 있으면 삭제하지 말고 추적만 해제한 뒤 이유를 보고한다. 푸시 전 변경 요약을 보여주고 사용자 승인을 받는다.
