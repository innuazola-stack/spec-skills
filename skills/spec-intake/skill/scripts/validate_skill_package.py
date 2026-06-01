#!/usr/bin/env python3
"""Validate the spec-intake skill package without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ALLOWED_FRONTMATTER_KEYS = {"name", "description"}
NAME_RE = re.compile(r"^[a-z0-9-]+$")
MOJIBAKE_PATTERNS = tuple(
    chr(codepoint)
    for codepoint in (0x8389, 0x8782, 0x9695, 0x8737, 0x7E32, 0x7ACA, 0x8B41, 0x87C6, 0xFFFD)
)
REQUIRED_EVAL_SECTIONS = (
    "## Prompt",
    "## Expected Behavior",
    "## Forbidden Behavior",
    "## Scoring Rule",
    "## Pass Bar",
)


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


def text_has_mojibake(text: str) -> bool:
    return any(pattern in text for pattern in MOJIBAKE_PATTERNS)


def validate_no_mojibake(project_root: Path) -> list[str]:
    errors: list[str] = []
    source_paths = [
        project_root / "manifest.yaml",
        project_root / "agent.md",
        project_root / "workflow.md",
        project_root / "rules.md",
        project_root / "schemas",
        project_root / "adapters",
        project_root / "evals",
        project_root / "skill" / "SKILL.md",
        project_root / "skill" / "references",
        project_root / "tests" / "cases",
    ]
    for source_path in source_paths:
        if source_path.is_file():
            paths = [source_path]
        elif source_path.is_dir():
            paths = sorted(path for path in source_path.rglob("*") if path.is_file() and path.suffix in {".md", ".yaml", ".yml"})
        else:
            continue
        for path in paths:
            if text_has_mojibake(path.read_text(encoding="utf-8")):
                errors.append(f"{path.relative_to(project_root)} contains visible mojibake")
    return errors


def validate_eval_cases(project_root: Path) -> list[str]:
    errors: list[str] = []
    cases_dir = project_root / "evals" / "cases"
    if not cases_dir.exists():
        return ["missing evals/cases"]
    case_files = sorted(cases_dir.glob("*.md"))
    if len(case_files) < 3:
        errors.append("evals/cases must contain at least three eval cases")
    for case_file in case_files:
        text = case_file.read_text(encoding="utf-8")
        for section in REQUIRED_EVAL_SECTIONS:
            if section not in text:
                errors.append(f"{case_file.relative_to(project_root)} missing {section}")
    return errors


def validate_harness_source(project_root: Path) -> list[str]:
    errors: list[str] = []
    required_files = (
        "manifest.yaml",
        "agent.md",
        "workflow.md",
        "rules.md",
        "schemas/contract-envelope.schema.md",
        "adapters/codex/SKILL.md",
        "adapters/codex/mapping.md",
        "adapters/codex/install.md",
        "validators/validate_harness.py",
        "tools/build_release.py",
    )
    for harness_file in required_files:
        if not (project_root / harness_file).exists():
            errors.append(f"missing harness source file {harness_file}")

    manifest = project_root / "manifest.yaml"
    if manifest.exists():
        text = manifest.read_text(encoding="utf-8")
        required_manifest_text = (
            "kind: harness-workflow",
            "entry: adapters/codex/SKILL.md",
            "runtime_package_entry: skill/SKILL.md",
            "cases_dir: evals/cases",
            "tests/harness_source_regression.py",
            "tools/build_release.py",
        )
        for required in required_manifest_text:
            if required not in text:
                errors.append(f"manifest.yaml missing {required}")

    codex_adapter = project_root / "adapters" / "codex" / "SKILL.md"
    if codex_adapter.exists():
        adapter_text = codex_adapter.read_text(encoding="utf-8")
        for required in (
            "Stage 1",
            "PRD review approval",
            "prd-writer",
            "hld-writer",
            "writer_invocations",
            "closed-form",
            "requirement-table",
            "validate_spec_intake_package.py",
        ):
            if required not in adapter_text:
                errors.append(f"adapters/codex/SKILL.md missing workflow semantic marker: {required}")

    errors.extend(validate_eval_cases(project_root))
    errors.extend(validate_no_mojibake(project_root))
    return errors


def validate_skill(root: Path) -> list[str]:
    errors: list[str] = []
    project_root = root.parent if root.name == "skill" else root
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
        "references/hld-design.md",
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

    errors.extend(validate_harness_source(project_root))

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
