#!/usr/bin/env python3
"""Regression probes for the spec-intake package validator.

The workflow now ends at a prd-writer PRD, a PRD brief, and an hld-writer HLD.
These probes intentionally focus on the hardened writer delegation contracts and
the legacy-artifact boundary instead of the removed Human/Agent PRD model.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


ROOT = Path(__file__).resolve().parents[1]
BASE_READY = ROOT / "tests" / "fixtures" / "ready-agent-prd-hld"
TMP = ROOT / ".tmp-validator-regression"
VALIDATOR = ROOT / "skill" / "scripts" / "validate_spec_intake_package.py"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_case(name: str, mutate: Callable[[Path], None]) -> Path:
    case_dir = TMP / name
    shutil.rmtree(case_dir, ignore_errors=True)
    shutil.copytree(BASE_READY, case_dir)
    mutate(case_dir)
    return case_dir


def run_validator(case_dir: Path, *, stage: str | None = None) -> tuple[int, dict]:
    command = [sys.executable, str(VALIDATOR), str(case_dir)]
    if stage:
        command.extend(["--stage", stage])
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(command, text=True, encoding="utf-8", capture_output=True, check=False, env=env)
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = {"ok": False, "errors": [result.stdout, result.stderr]}
    return result.returncode, payload


def remove_writer_invocations(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract.pop("writer_invocations", None)
    write_json(path, contract)


def prd_writer_not_completed(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["writer_invocations"]["prd"]["status"] = "failed"
    contract["writer_invocations"]["prd"]["required_fix"] = "Rerun prd-writer and produce prd.md."
    write_json(path, contract)


def prd_writer_source_not_system_generated(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["SRC-006"]["payload"]["source_type"] = "user_input"
    write_json(path, contract)


def hld_missing_prd_brief_source(case_dir: Path) -> None:
    path = case_dir / "high-level-design.json"
    hld = read_json(path)
    hld["source_artifacts"].pop("prd_brief_ref", None)
    hld["source_artifacts"].pop("prd_brief_status", None)
    write_json(path, hld)


def legacy_artifact_present(case_dir: Path) -> None:
    (case_dir / "agent-prd.md").write_text("# Legacy Agent PRD\n", encoding="utf-8")


def missing_prd_file(case_dir: Path) -> None:
    (case_dir / "prd.md").unlink()


def make_stage2_ready(case_dir: Path) -> None:
    for filename in ("high-level-design.json", "high-level-design.md", "hld-semantic-review.json"):
        path = case_dir / filename
        if path.exists():
            path.unlink()
    contract_path = case_dir / "contract-envelope.json"
    contract = read_json(contract_path)
    contract["harness_workflow"]["current_stage"] = "stage_2_prd_review"
    contract["harness_workflow"]["completed_stages"] = ["stage_1_requirements_table"]
    contract["harness_workflow"]["approval_gates"] = {
        "prd_review": {"status": "pending", "approved_by_ref": ""}
    }
    contract["contract_summary"]["stage_ready"] = ["stage_1_requirements_table", "stage_2_prd_review"]
    contract["contract_summary"]["stage_blocked"] = ["stage_3_hld"]
    contract["next_actions"] = ["Review prd-brief.md and approve or request revision."]
    contract.get("writer_invocations", {}).pop("hld", None)
    write_json(contract_path, contract)


def stage2_missing_prd_writer(case_dir: Path) -> None:
    make_stage2_ready(case_dir)
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["writer_invocations"].pop("prd", None)
    write_json(path, contract)


def stage2_blocked_writer(case_dir: Path) -> None:
    for filename in ("prd.md", "prd-brief.md", "high-level-design.json", "high-level-design.md", "hld-semantic-review.json"):
        path = case_dir / filename
        if path.exists():
            path.unlink()
    contract_path = case_dir / "contract-envelope.json"
    contract = read_json(contract_path)
    contract["render_status"] = {"prd_brief": "blocked", "prd": "blocked"}
    contract["writer_invocations"] = {
        "prd": {
            "writer_skill": "prd-writer",
            "status": "unavailable",
            "source_ref": "SRC-006",
            "input_refs": ["REQ-001", "AC-001"],
            "output_artifacts": [],
            "required_fix": "Install or restore prd-writer, then rerun Stage 2.",
        }
    }
    contract["contract_summary"]["ready_targets"] = []
    contract["contract_summary"]["blocked_targets"] = ["prd_brief", "prd"]
    contract["contract_summary"]["stage_ready"] = ["stage_1_requirements_table"]
    contract["contract_summary"]["stage_blocked"] = ["stage_2_prd_review", "stage_3_hld"]
    contract["harness_workflow"]["current_stage"] = "stage_2_prd_review"
    contract["harness_workflow"]["completed_stages"] = ["stage_1_requirements_table"]
    contract["harness_workflow"]["approval_gates"] = {
        "prd_review": {"status": "not_started", "approved_by_ref": ""}
    }
    contract["next_actions"] = ["Install or restore prd-writer, then rerun Stage 2."]
    write_json(contract_path, contract)


def main() -> int:
    shutil.rmtree(TMP, ignore_errors=True)
    TMP.mkdir(parents=True, exist_ok=True)
    try:
        checks: list[tuple[str, Path, bool, str | None]] = [
            ("ready final fixture passes", BASE_READY, True, None),
            ("missing writer_invocations fails", make_case("missing_writer_invocations", remove_writer_invocations), False, None),
            ("prd writer not completed fails", make_case("prd_writer_not_completed", prd_writer_not_completed), False, None),
            ("prd writer source not system_generated fails", make_case("prd_writer_source_not_system_generated", prd_writer_source_not_system_generated), False, None),
            ("HLD missing PRD brief source fails", make_case("hld_missing_prd_brief_source", hld_missing_prd_brief_source), False, None),
            ("legacy agent PRD artifact fails", make_case("legacy_artifact_present", legacy_artifact_present), False, None),
            ("missing prd.md fails", make_case("missing_prd_file", missing_prd_file), False, None),
            ("stage2 ready PRD package passes", make_case("stage2_ready", make_stage2_ready), True, "stage2"),
            ("stage2 missing prd writer fails", make_case("stage2_missing_prd_writer", stage2_missing_prd_writer), False, "stage2"),
            ("stage2 blocked writer package passes", make_case("stage2_blocked_writer", stage2_blocked_writer), True, "stage2"),
        ]

        failures: list[str] = []
        results: list[dict] = []
        for name, case_dir, should_pass, stage in checks:
            code, payload = run_validator(case_dir, stage=stage)
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
