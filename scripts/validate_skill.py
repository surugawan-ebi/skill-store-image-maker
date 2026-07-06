#!/usr/bin/env python3
"""Validate this repository's skill package without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
REQUIRED_REFERENCES = [
    "references/input-brief-template.md",
    "references/store-asset-specs.md",
    "references/design-playbook.md",
    "references/project-workflow.md",
]
REQUIRED_TEMPLATE_FILES = [
    "assets/project-template/materials/brief.md",
    "assets/project-template/materials/asset-inventory.md",
    "assets/project-template/working/shot-plan.md",
    "assets/project-template/working/copy-bank.md",
    "assets/project-template/working/prompt-pack.md",
    "assets/project-template/working/qa-notes.md",
    "assets/project-template/exports/manifest.md",
]


def parse_simple_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")

    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("SKILL.md frontmatter is not closed")

    values: dict[str, str] = {}
    for raw_line in parts[1].strip().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {raw_line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        values[key] = value
    return values


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"

    if not skill_md.exists():
        return [f"Missing {skill_md}"]

    text = skill_md.read_text(encoding="utf-8")
    try:
        frontmatter = parse_simple_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]

    extra_keys = set(frontmatter) - ALLOWED_FRONTMATTER_KEYS
    if extra_keys:
        errors.append(f"Unexpected frontmatter keys: {', '.join(sorted(extra_keys))}")

    name = frontmatter.get("name", "")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        errors.append("Skill name must be 1-64 lowercase letters, digits, or hyphens")

    description = frontmatter.get("description", "").strip()
    if not description:
        errors.append("Skill description is required")
    if len(description) > 1024:
        errors.append("Skill description must be 1024 characters or fewer")

    if "TODO" in text or "[TODO" in text:
        errors.append("SKILL.md still contains TODO markers")

    for relative_path in REQUIRED_REFERENCES:
        if not (skill_dir / relative_path).exists():
            errors.append(f"Missing reference file: {relative_path}")
        elif relative_path not in text:
            errors.append(f"SKILL.md does not mention reference: {relative_path}")

    for relative_path in REQUIRED_TEMPLATE_FILES:
        if not (skill_dir / relative_path).exists():
            errors.append(f"Missing project template file: {relative_path}")

    if not openai_yaml.exists():
        errors.append("Missing agents/openai.yaml")
    else:
        openai_text = openai_yaml.read_text(encoding="utf-8")
        if "$game-store-image-maker" not in openai_text:
            errors.append("agents/openai.yaml default prompt should mention $game-store-image-maker")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_skill.py <skill-directory>", file=sys.stderr)
        return 2

    skill_dir = Path(sys.argv[1])
    errors = validate_skill(skill_dir)
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
