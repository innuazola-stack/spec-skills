from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

CORE_FILES = [
    "SKILL.md",
    "manifest.yaml",
    "agent.md",
    "workflow.md",
    "rules.md",
    "schemas/design-planning.schema.json",
    "validators/validate_design_planning.py",
    "validators/validate_harness.py",
    "tools/build_release.py",
    "skill/SKILL.md",
    "releases/0.2.0.md",
]

EVAL_CASES = [
    "evals/cases/positive-rust-prd-hld.md",
    "evals/cases/negative-missing-hld.md",
    "evals/cases/boundary-future-phase.md",
]

ADAPTERS = {
    "codex": "system-prompt.md",
    "claude": "CLAUDE.md",
    "gemini": "GEMINI.md",
    "openclaw": "OPENCLAW.md",
    "hermas": "HERMAS.md",
}

FORBIDDEN_SOURCE_TERMS = [
    "default_planning_output_root: docs/design",
    "The default planning output root is `docs/design`",
    '"output_root": "docs/design | user-specified planning output root"',
    "task_type\": \"implementation\"",
    "task_type\": \"foundation\"",
    "task_type\": \"verification\"",
    '"cargo test',
    "Project builds with empty/stub modules",
]


def fail(errors: list[str]) -> None:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> None:
    errors: list[str] = []

    for rel in CORE_FILES + EVAL_CASES:
        if not (ROOT / rel).exists():
            errors.append(f"missing required harness file: {rel}")

    for adapter, entry in ADAPTERS.items():
        base = ROOT / "adapters" / adapter
        for name in ["install.md", "mapping.md", entry]:
            if not (base / name).exists():
                errors.append(f"missing adapter file: adapters/{adapter}/{name}")
        mapping = base / "mapping.md"
        if mapping.exists() and "Unsupported behavior" not in mapping.read_text(encoding="utf-8"):
            errors.append(f"adapter mapping omits unsupported behavior: adapters/{adapter}/mapping.md")

    manifest = read("manifest.yaml") if (ROOT / "manifest.yaml").exists() else ""
    for term in [
        "version: 0.2.0",
        "type: harness-workflow",
        "paradigm: review-gated",
        "default_planning_output_root: tasks/design",
        "fixed_detailed_design_root: docs/design",
        "supported_adapters:",
    ]:
        if term not in manifest:
            errors.append(f"manifest missing term: {term}")

    release_note = ROOT / "releases" / "0.2.0.md"
    if release_note.exists():
        text = release_note.read_text(encoding="utf-8")
        for term in ["## Summary", "## Changes", "## Validation", "## Compatibility"]:
            if term not in text:
                errors.append(f"release note missing term: {term}")

    skill = read("skill/SKILL.md") if (ROOT / "skill/SKILL.md").exists() else ""
    if "The default planning output root is `tasks/design`" not in skill:
        errors.append("SKILL.md must set default planning output root to tasks/design")
    if "Detailed design document outputs are fixed under target `docs/design/`" not in skill:
        errors.append("SKILL.md must keep detailed design documents under docs/design")

    output_contract = read("skill/references/output-contract.md") if (ROOT / "skill/references/output-contract.md").exists() else ""
    if '"output_root": "tasks/design | user-specified planning output root"' not in output_contract:
        errors.append("output contract must show tasks/design as default output_root")

    for rel in EVAL_CASES:
        if not (ROOT / rel).exists():
            continue
        text = read(rel)
        for heading in ["## Prompt", "## Expected Behavior", "## Forbidden Behavior", "## Scoring Rule", "## Pass Bar"]:
            if heading not in text:
                errors.append(f"{rel} missing eval heading: {heading}")

    for rel in ["skill/SKILL.md", "skill/references/output-contract.md", "skill/references/methodology.md", "manifest.yaml", "tools/generate_spec_scheduler_design_planning.py"]:
        path = ROOT / rel if rel.startswith(("skill/", "manifest", "tools/")) else ROOT / rel
        if not path.exists() and rel.startswith("tools/"):
            path = ROOT.parents[1] / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for term in FORBIDDEN_SOURCE_TERMS:
            if term in text:
                errors.append(f"{rel} contains forbidden source term: {term}")

    if errors:
        fail(errors)
    print("PASS: design-planning harness validation")


if __name__ == "__main__":
    main()
