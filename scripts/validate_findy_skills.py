#!/usr/bin/env python3
"""Validate FINDY skill packaging without project-specific dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|#)([^)]+)\)")
ABSOLUTE_PATH_RE = re.compile(r"/(?:Users|home)/[^\s`\"']+")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("YAML frontmatter가 없습니다")
    try:
        raw, _body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError("YAML frontmatter 종료 구분자가 없습니다") from exc

    metadata: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"잘못된 frontmatter 행: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    agent_file = skill_dir / "agents" / "openai.yaml"

    try:
        metadata = parse_frontmatter(skill_file)
    except (OSError, ValueError) as exc:
        return [f"{skill_file}: {exc}"]

    if set(metadata) != {"name", "description"}:
        errors.append(f"{skill_file}: frontmatter는 name과 description만 허용합니다")
    if metadata.get("name") != skill_dir.name:
        errors.append(f"{skill_file}: name이 디렉터리명과 다릅니다")
    if not metadata.get("description"):
        errors.append(f"{skill_file}: description이 비어 있습니다")

    if not agent_file.is_file():
        errors.append(f"{agent_file}: agents metadata가 없습니다")
    else:
        agent_text = agent_file.read_text(encoding="utf-8")
        if f"${skill_dir.name}" not in agent_text:
            errors.append(f"{agent_file}: default_prompt에 ${skill_dir.name}이 없습니다")

    for path in skill_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if ABSOLUTE_PATH_RE.search(text):
            errors.append(f"{path}: 사용자별 절대 경로가 포함되어 있습니다")
        for target in LINK_RE.findall(text):
            clean_target = target.split("#", 1)[0]
            if clean_target and not (path.parent / clean_target).resolve().exists():
                errors.append(f"{path}: 존재하지 않는 링크 {target}")

    return errors


def main() -> int:
    skill_dirs = sorted(path for path in SKILLS_ROOT.glob("findy-*") if path.is_dir())
    if not skill_dirs:
        print("FINDY skills not found", file=sys.stderr)
        return 1

    errors = [error for skill_dir in skill_dirs for error in validate_skill(skill_dir)]
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        return 1

    print(f"Validated {len(skill_dirs)} FINDY skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
