#!/usr/bin/env python3
"""Regression probes for spec-intake harness source validation."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / ".tmp-harness-source-regression"
VALIDATOR = ROOT / "skill" / "scripts" / "validate_skill_package.py"


def make_case(name: str, mutate: Callable[[Path], None]) -> Path:
    case_dir = TMP / name
    shutil.rmtree(case_dir, ignore_errors=True)
    shutil.copytree(ROOT, case_dir, ignore=shutil.ignore_patterns(".tmp-*", "dist", "releases"))
    mutate(case_dir)
    return case_dir


def run_validator(case_dir: Path) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, str(case_dir / "skill" / "scripts" / "validate_skill_package.py"), str(case_dir / "skill")],
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = {"ok": False, "errors": [result.stdout, result.stderr]}
    return result.returncode, payload


def remove_codex_adapter(case_dir: Path) -> None:
    shutil.rmtree(case_dir / "adapters" / "codex", ignore_errors=True)


def remove_eval_cases(case_dir: Path) -> None:
    shutil.rmtree(case_dir / "evals" / "cases", ignore_errors=True)


def remove_release_builder(case_dir: Path) -> None:
    builder = case_dir / "tools" / "build_release.py"
    if builder.exists():
        builder.unlink()


def mojibake_eval_prompt(case_dir: Path) -> None:
    eval_dir = case_dir / "evals" / "cases"
    eval_dir.mkdir(parents=True, exist_ok=True)
    corrupt = "".join(chr(codepoint) for codepoint in (0x86DB, 0x58FB, 0xFF78, 0x8353, 0x8B41))
    (eval_dir / "mojibake.md").write_text(
        "# Eval Case: Mojibake\n\n"
        "## Prompt\n\n"
        f"{corrupt} workflow\n\n"
        "## Expected Behavior\n\n"
        "Reject mojibake.\n\n"
        "## Forbidden Behavior\n\n"
        "Do not accept corrupt text.\n\n"
        "## Scoring Rule\n\n"
        "Fail when mojibake is present.\n\n"
        "## Pass Bar\n\n"
        "`pass`\n",
        encoding="utf-8",
    )


def remove_manifest_adapter_mapping(case_dir: Path) -> None:
    path = case_dir / "manifest.yaml"
    text = path.read_text(encoding="utf-8")
    text = text.replace("  codex:\n    entry: adapters/codex/SKILL.md\n", "")
    text = text.replace("  codex:\n    entry: skill/SKILL.md\n", "")
    path.write_text(text, encoding="utf-8")


def main() -> int:
    shutil.rmtree(TMP, ignore_errors=True)
    TMP.mkdir(parents=True, exist_ok=True)
    try:
        checks: list[tuple[str, Path, bool]] = [
            ("current harness source passes", ROOT, True),
            ("missing codex adapter fails", make_case("missing-codex-adapter", remove_codex_adapter), False),
            ("missing eval cases fails", make_case("missing-eval-cases", remove_eval_cases), False),
            ("missing release builder fails", make_case("missing-release-builder", remove_release_builder), False),
            ("mojibake eval prompt fails", make_case("mojibake-eval-prompt", mojibake_eval_prompt), False),
            (
                "manifest missing adapter mapping fails",
                make_case("manifest-missing-adapter-mapping", remove_manifest_adapter_mapping),
                False,
            ),
        ]

        failures: list[str] = []
        results: list[dict] = []
        for name, case_dir, should_pass in checks:
            code, payload = run_validator(case_dir)
            passed = code == 0 and payload.get("ok") is True
            results.append({"name": name, "passed": passed, "errors": payload.get("errors", [])})
            if passed != should_pass:
                failures.append(f"{name}: expected pass={should_pass}, got pass={passed}")

        print(json.dumps({"ok": not failures, "failures": failures, "results": results}, ensure_ascii=False, indent=2))
        return 0 if not failures else 1
    finally:
        shutil.rmtree(TMP, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
