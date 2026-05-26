#!/usr/bin/env python3
"""Validate the spec-intake skill package without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
NAME_RE = re.compile(r"^[a-z0-9-]+$")


def parse_simple_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter"]
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, ["SKILL.md frontmatter must be delimited by ---"]

    data: dict[str, str] = {}
    for lineno, line in enumerate(parts[1].strip().splitlines(), start=2):
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"frontmatter line {lineno} is not key: value")
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, errors


def validate_skill(root: Path) -> list[str]:
    errors: list[str] = []
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        return ["missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    frontmatter, fm_errors = parse_simple_frontmatter(text)
    errors.extend(fm_errors)

    unexpected = sorted(set(frontmatter) - ALLOWED_FRONTMATTER_KEYS)
    if unexpected:
        errors.append("unexpected SKILL.md frontmatter keys: " + ", ".join(unexpected))

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not name:
        errors.append("missing SKILL.md frontmatter key: name")
    if not description:
        errors.append("missing SKILL.md frontmatter key: description")

    if name and (not NAME_RE.fullmatch(name) or name.startswith("-") or name.endswith("-") or "--" in name):
        errors.append("skill name must be lower hyphen-case without edge or repeated hyphens")
    if len(name) > 64:
        errors.append("skill name must be at most 64 characters")
    if len(description) > 1024:
        errors.append("description must be at most 1024 characters")
    if "<" in description or ">" in description:
        errors.append("description must not contain angle brackets")

    for ref in (
        "references/intake-method.md",
        "references/output-artifacts.md",
        "references/task-decomposition.md",
        "references/quality-gates.md",
    ):
        if ref not in text:
            errors.append(f"SKILL.md does not link {ref}")
        if not (root / ref).exists():
            errors.append(f"missing {ref}")

    agent_yaml = root / "agents" / "openai.yaml"
    if not agent_yaml.exists():
        errors.append("missing agents/openai.yaml")
    else:
        agent_text = agent_yaml.read_text(encoding="utf-8")
        for key in ("display_name:", "short_description:", "default_prompt:"):
            if key not in agent_text:
                errors.append(f"agents/openai.yaml missing {key}")

    for script_name in ("validate_spec_intake_package.py", "validate_skill_package.py"):
        if not (root / "scripts" / script_name).exists():
            errors.append(f"missing scripts/{script_name}")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_skill_package.py <skill-dir>", file=sys.stderr)
        return 2

    errors = validate_skill(Path(argv[1]))
    ok = not errors
    print(json.dumps({"ok": ok, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
