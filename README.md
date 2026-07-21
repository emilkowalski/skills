# FINDY Codex Design Skills

이 저장소는 [Emil Kowalski의 design engineering skills](https://github.com/emilkowalski/skills)를 기반으로 하며, FINDY Flet 앱에서 Codex가 일관된 구현·감사·모바일 QA를 수행하도록 전용 스킬을 추가한 포크입니다.

원본 디자인·애니메이션 스킬의 저작권과 출처는 원저작자에게 있습니다. FINDY 전용 스킬은 원본을 수정하지 않고 별도 폴더로 관리합니다.

## 설치

전체 스킬을 설치합니다.

```bash
npx skills@latest add rudals906377/skills
```

## FINDY Codex 스킬

- **[findy-flet-ui](./skills/findy-flet-ui/SKILL.md)** — FINDY Flet UI 구현, 공통 컴포넌트 정리, 안전영역과 접근성 보정.
- **[findy-frontend-audit](./skills/findy-frontend-audit/SKILL.md)** — 코드를 바꾸지 않고 공개 MVP 프론트 품질을 근거 중심으로 감사.
- **[findy-mobile-qa](./skills/findy-mobile-qa/SKILL.md)** — 360x800·390x844, 키보드, 큰 글자, safe area와 고정 UI 회귀 검증.

역할을 구현, 감사, QA로 분리해 Codex가 분석 요청에서 임의 수정하거나 한 작업에서 범위를 과도하게 넓히지 않도록 했습니다.

## Upstream 스킬

- **[emil-design-eng](./skills/emil-design-eng/SKILL.md)** — UI polish와 design engineering 원칙.
- **[review-animations](./skills/review-animations/SKILL.md)** — motion 코드를 엄격한 기준으로 리뷰.
- **[improve-animations](./skills/improve-animations/SKILL.md)** — 코드베이스 전체 애니메이션 감사와 실행 계획 작성.
- **[find-animation-opportunities](./skills/find-animation-opportunities/SKILL.md)** — 필요한 motion 기회와 피해야 할 motion 탐색.
- **[animation-vocabulary](./skills/animation-vocabulary/SKILL.md)** — 정확한 애니메이션 언어와 표현.
- **[apple-design](./skills/apple-design/SKILL.md)** — Apple 인터페이스와 fluid motion 원칙.
- **[pick-ui-library](./skills/pick-ui-library/SKILL.md)** — 검증된 웹 UI 라이브러리 선택 지원.

Upstream 스킬은 주로 웹과 motion에 강합니다. FINDY 화면을 직접 수정할 때는 Flet 구조와 제품 계약을 아는 `findy-flet-ui`를 우선 사용하고, motion의 세부 품질을 다듬을 때 upstream 스킬을 함께 사용합니다.

## 검증

```bash
for skill in skills/findy-*; do
  python3 /Users/kyoungmin/.codex/skills/.system/skill-creator/scripts/quick_validate.py "$skill"
done
git diff --check
```

## 출처와 라이선스

- Upstream: [emilkowalski/skills](https://github.com/emilkowalski/skills)
- Upstream design references: [animations.dev](https://animations.dev/)
- License: [MIT](./LICENSE)
