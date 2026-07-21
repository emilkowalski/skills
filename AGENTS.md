# Codex Repository Rules

## Scope

- `skills/findy-*` contains FINDY-specific Codex skills.
- Other skill folders are upstream material from `emilkowalski/skills`; keep their authorship and behavior intact unless an upstream sync explicitly requires a change.

## Skill changes

- Use lowercase hyphenated directory names.
- Keep `SKILL.md` frontmatter to `name` and `description`.
- Put detailed checklists and product contracts in `references/`.
- Keep `agents/openai.yaml` prompts explicit and mention the skill as `$skill-name`.
- Do not add secrets, production URLs, databases, build artifacts, screenshots, or user documents.

## Validation

Run for each changed skill:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" skills/<skill-name>
python3 scripts/validate_findy_skills.py
git diff --check
```

Before commit or push, inspect `git status`, staged changes, `.gitignore`, and tracked files for sensitive content.
