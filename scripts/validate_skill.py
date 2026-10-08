#!/usr/bin/env python3
"""Validate this repository's skill package without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
SKILL_PROFILES = {
    "game-store-image-maker": {
        "references": [
            "references/input-brief-template.md",
            "references/store-asset-specs.md",
            "references/design-playbook.md",
            "references/project-workflow.md",
        ],
        "files": [
            "assets/project-template/materials/brief.md",
            "assets/project-template/materials/asset-inventory.md",
            "assets/project-template/working/shot-plan.md",
            "assets/project-template/working/copy-bank.md",
            "assets/project-template/working/prompt-pack.md",
            "assets/project-template/working/qa-notes.md",
            "assets/project-template/exports/manifest.md",
        ],
        "terms": ["Instagram", "1080x1350", "1080x1920", "contain-on-canvas"],
    },
    "game-raster-asset-pipeline": {
        "references": [
            "references/job-manifest.md",
            "references/imagegen-and-visual-qa.md",
            "references/registry-and-regeneration.md",
        ],
        "files": [
            "scripts/inspect_raster.py",
            "assets/project-template/raster-jobs.json",
            "assets/project-template/imagegen-assets.json",
        ],
        "json_files": [
            "assets/project-template/raster-jobs.json",
            "assets/project-template/imagegen-assets.json",
        ],
        "terms": [
            "ImageGen",
            "view_image",
            "regenerate",
            "transparent_gutter",
            "occupancy_mode",
            "background_color",
            "app_icon",
        ],
    },
}


def validate_openai_yaml(text: str) -> list[str]:
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines or lines[0] != "interface:":
        return ["agents/openai.yaml must contain only an interface mapping"]
    expected = {"display_name", "short_description", "default_prompt"}
    found: set[str] = set()
    errors: list[str] = []
    for line in lines[1:]:
        match = re.fullmatch(r'  ([a-z_]+):\s+"([^"\\]*(?:\\.[^"\\]*)*)"', line)
        if not match:
            errors.append(f"Invalid agents/openai.yaml line: {line}")
            continue
        key = match.group(1)
        if key not in expected or key in found:
            errors.append(f"Unexpected or duplicate agents/openai.yaml key: {key}")
        found.add(key)
    missing = expected - found
    if missing:
        errors.append(f"Missing agents/openai.yaml keys: {', '.join(sorted(missing))}")
    return errors


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

    profile = SKILL_PROFILES.get(name)
    if profile is None:
        errors.append(f"No repository validation profile for skill: {name}")
        profile = {"references": [], "files": [], "json_files": [], "terms": []}

    for relative_path in profile["references"]:
        if not (skill_dir / relative_path).exists():
            errors.append(f"Missing reference file: {relative_path}")
        elif relative_path not in text:
            errors.append(f"SKILL.md does not mention reference: {relative_path}")

    for relative_path in profile["files"]:
        if not (skill_dir / relative_path).exists():
            errors.append(f"Missing required skill file: {relative_path}")

    for relative_path in profile.get("json_files", []):
        json_path = skill_dir / relative_path
        if json_path.exists():
            try:
                json.loads(json_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"Invalid JSON file {relative_path}: {exc}")

    combined_text = text + "\n"
    for relative_path in profile["references"]:
        reference_file = skill_dir / relative_path
        if reference_file.exists():
            combined_text += reference_file.read_text(encoding="utf-8") + "\n"

    for term in profile["terms"]:
        if term not in combined_text:
            errors.append(f"Expected skill guidance to mention: {term}")

    if not openai_yaml.exists():
        errors.append("Missing agents/openai.yaml")
    else:
        openai_text = openai_yaml.read_text(encoding="utf-8")
        errors.extend(validate_openai_yaml(openai_text))
        if f"${name}" not in openai_text:
            errors.append(f"agents/openai.yaml default prompt should mention ${name}")

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
