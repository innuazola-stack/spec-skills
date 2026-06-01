#!/usr/bin/env python3
"""Validate the development-planning harness source package."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path


CANONICAL_STAGES = [
    "stage_1_overall_planning",
    "stage_2_independent_task_formation",
    "stage_3_task_logic_review",
    "stage_4_plan_integrity_review",
]

CANONICAL_PHASE_IDS = ["STAGE-001", "STAGE-002", "STAGE-003", "STAGE-004"]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require_files(root: Path) -> None:
    required = [
        "manifest.yaml",
        "agent.md",
        "workflow.md",
        "rules.md",
        "schemas/development-planning.schema.json",
        "validators/validate_harness.py",
        "validators/validate_development_planning_package.py",
        "adapters/codex/SKILL.md",
        "adapters/codex/mapping.md",
        "skill/SKILL.md",
        "skill/references/output-contract.md",
        "skill/references/planning-quality-model.md",
        "skill/assets/TASK_DESCRIPTION.template.md",
        "skill/assets/TASK_PROMPT.fixture.md",
        "skill/assets/AGENTS.template.md",
        "skill/assets/CLAUDE.template.md",
        "evals/cases/positive-prd-hld-lld.md",
        "evals/cases/negative-missing-lld.md",
        "evals/cases/boundary-future-phase.md",
        "evals/fixtures/positive-prd-hld-lld/docs/prd.md",
        "evals/fixtures/positive-prd-hld-lld/docs/hld.md",
        "evals/fixtures/positive-prd-hld-lld/docs/lld.md",
        "evals/fixtures/negative-missing-lld/docs/prd.md",
        "evals/fixtures/negative-missing-lld/docs/hld.md",
        "evals/fixtures/boundary-future-phase/docs/prd.md",
        "evals/fixtures/boundary-future-phase/docs/hld.md",
        "evals/fixtures/boundary-future-phase/docs/lld.md",
        "tests/fixtures/ready-package/tasks/development/development-planning.json",
        "tests/fixtures/blocked-package/tasks/development/development-planning.json",
        "tests/fixtures/invalid-duplicate-execution-order/tasks/development/development-planning.json",
        "tests/fixtures/invalid-declared-path/tasks/development/development-planning.json",
        "tests/fixtures/invalid-parallel-group-dependency/tasks/development/development-planning.json",
    ]
    for rel in required:
        if not (root / rel).exists():
            fail(f"missing {rel}")


def validate_manifest(root: Path) -> None:
    text = read(root / "manifest.yaml")
    for term in [
        "kind: harness-workflow",
        "paradigm: review-gated-branching-dag-planning",
        "stage_1_overall_planning",
        "stage_2_independent_task_formation",
        "stage_3_task_logic_review",
        "stage_4_plan_integrity_review",
        "validators/validate_harness.py",
        "validators/validate_development_planning_package.py",
        "schemas/development-planning.schema.json",
        "adapters/codex/SKILL.md",
    ]:
        if term not in text:
            fail(f"manifest.yaml missing {term}")
    stage_positions = [text.find(stage) for stage in CANONICAL_STAGES]
    if any(pos < 0 for pos in stage_positions) or stage_positions != sorted(stage_positions):
        fail("manifest canonical stage order is missing or out of order")


def validate_core_docs(root: Path) -> None:
    agent = read(root / "agent.md")
    workflow = read(root / "workflow.md")
    rules = read(root / "rules.md")

    for term in ["planning-only", "does not own", "Completion Criteria"]:
        if term not in agent:
            fail(f"agent.md missing {term}")

    for term in [
        "Stage 1: Overall Planning",
        "Stage 2: Independent Task Formation",
        "Stage 3: Task Logic And Completeness Review",
        "Stage 4: Whole-Plan Integrity And Dependency Review",
        "Blocked Planning Route",
        "Handoff",
    ]:
        if term not in workflow:
            fail(f"workflow.md missing {term}")

    for term in [
        "Planning-Only Boundary",
        "phase_reports",
        "STAGE-001",
        "STAGE-002",
        "STAGE-003",
        "STAGE-004",
        "DAG Rules",
        "Validation Rules",
    ]:
        if term not in rules:
            fail(f"rules.md missing {term}")


def validate_schema(root: Path) -> None:
    schema = json.loads(read(root / "schemas/development-planning.schema.json"))
    required = set(schema.get("required", []))
    for key in [
        "planning_status",
        "planning_harness_model",
        "phase_reports",
        "tasks",
        "dag",
        "task_logic_review",
        "plan_integrity_review",
        "required_fixes",
    ]:
        if key not in required:
            fail(f"schema required missing {key}")

    target_type = (
        schema.get("properties", {})
        .get("planning_harness_model", {})
        .get("properties", {})
        .get("target_type", {})
        .get("const")
    )
    if target_type != "harness-workflow":
        fail("schema planning_harness_model.target_type must be harness-workflow")

    phase_enum = (
        schema.get("properties", {})
        .get("phase_reports", {})
        .get("items", {})
        .get("properties", {})
        .get("stage_id", {})
        .get("enum", [])
    )
    if phase_enum != CANONICAL_PHASE_IDS:
        fail("schema phase_reports stage_id enum must match canonical phase IDs")


def validate_runtime_skill(root: Path) -> None:
    skill = read(root / "skill/SKILL.md")
    if not skill.startswith("---\nname: development-planning\n"):
        fail("skill/SKILL.md frontmatter name invalid")
    for term in [
        "harness workflow",
        "tasks/development",
        "planning-only",
        "development-planning.json",
        "phase reports",
    ]:
        if term not in skill:
            fail(f"skill/SKILL.md missing {term}")

    contract = read(root / "skill/references/output-contract.md")
    for term in [
        '"target_type": "harness-workflow"',
        '"phase_reports": []',
        '"task_logic_review": {}',
        '"plan_integrity_review": {}',
        "Blocked planning",
    ]:
        if term not in contract:
            fail(f"output-contract.md missing {term}")


def validate_evals(root: Path) -> None:
    for rel in [
        "evals/cases/positive-prd-hld-lld.md",
        "evals/cases/negative-missing-lld.md",
        "evals/cases/boundary-future-phase.md",
    ]:
        text = read(root / rel)
        for section in [
            "## Prompt",
            "## Expected Behavior",
            "## Forbidden Behavior",
            "## Scoring Rule",
            "## Pass Bar",
        ]:
            if section not in text:
                fail(f"{rel} missing {section}")
        if "Fixture:" not in text:
            fail(f"{rel} missing fixture reference")


def validate_no_mojibake(root: Path) -> None:
    bad_patterns = [chr(0xFFFD), chr(0x7AB6), chr(0x7B0F)]
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".json", ".py"}:
            text = read(path)
            if any(pattern in text for pattern in bad_patterns):
                fail(f"visible mojibake in {path.relative_to(root)}")


def validate_package_validator_fixtures(root: Path) -> None:
    validator = root / "validators" / "validate_development_planning_package.py"
    positive = [
        root / "tests" / "fixtures" / "ready-package",
        root / "tests" / "fixtures" / "blocked-package",
    ]
    negative = [
        root / "tests" / "fixtures" / "invalid-duplicate-execution-order",
        root / "tests" / "fixtures" / "invalid-declared-path",
        root / "tests" / "fixtures" / "invalid-parallel-group-dependency",
    ]
    for fixture in positive:
        result = subprocess.run([sys.executable, str(validator), str(fixture)], check=False, capture_output=True, text=True)
        if result.returncode != 0:
            fail(f"package validator should pass {fixture.relative_to(root)}: {result.stdout}{result.stderr}")
    for fixture in negative:
        result = subprocess.run([sys.executable, str(validator), str(fixture)], check=False, capture_output=True, text=True)
        if result.returncode == 0:
            fail(f"package validator should reject {fixture.relative_to(root)}")

    def minimal_ready_plan(source_inventory: list[dict[str, str]], extra: dict | None = None) -> dict:
        plan = {
            "planning_status": "ready",
            "output_root": "tasks/development",
            "source_inventory": source_inventory,
            "planning_harness_model": {
                "target_type": "harness-workflow",
                "quality_standard": "review-gated-branching-dag-planning",
                "stages": CANONICAL_PHASE_IDS,
            },
            "phase_reports": [
                {
                    "stage_id": stage_id,
                    "stage_name": stage_id,
                    "purpose": "test",
                    "inputs": [],
                    "outputs": [],
                    "review_checks": [],
                    "status": "pass",
                    "blocking_findings": [],
                }
                for stage_id in CANONICAL_PHASE_IDS
            ],
            "tasks": [
                {
                    "task_id": "TASK-001",
                    "title": "Implement",
                    "task_type": "implementation",
                    "source_refs": ["docs/prd.md"],
                    "inputs": ["input"],
                    "expected_outputs": ["output"],
                    "impacted_areas": ["src"],
                    "allowed_scope": ["scope"],
                    "forbidden_scope": ["forbidden"],
                    "acceptance": ["acceptance"],
                    "verification": ["test"],
                    "stop_conditions": ["stop"],
                    "dependencies": [],
                    "handoff_requirements": ["handoff"],
                    "task_description_path": "tasks/development/TASK-001/task.md",
                    "fixture_dir": "tasks/development/TASK-001",
                    "prompt_path": "tasks/development/TASK-001/prompt.md",
                    "agents_path": "tasks/development/TASK-001/AGENTS.md",
                    "claude_path": "tasks/development/TASK-001/CLAUDE.md",
                },
                {
                    "task_id": "TASK-002",
                    "title": "Accept",
                    "task_type": "delivery_acceptance",
                    "source_refs": ["docs/prd.md"],
                    "inputs": ["TASK-001"],
                    "expected_outputs": ["report"],
                    "impacted_areas": ["tasks/development/report.md"],
                    "allowed_scope": ["verify"],
                    "forbidden_scope": ["features"],
                    "acceptance": ["accepted"],
                    "verification": ["test"],
                    "stop_conditions": ["incomplete"],
                    "dependencies": ["TASK-001"],
                    "handoff_requirements": ["report"],
                    "task_description_path": "tasks/development/TASK-002/task.md",
                    "fixture_dir": "tasks/development/TASK-002",
                    "prompt_path": "tasks/development/TASK-002/prompt.md",
                    "agents_path": "tasks/development/TASK-002/AGENTS.md",
                    "claude_path": "tasks/development/TASK-002/CLAUDE.md",
                },
            ],
            "dag": {
                "nodes": ["TASK-001", "TASK-002"],
                "edges": [
                    {
                        "from": "TASK-001",
                        "to": "TASK-002",
                        "reason": "acceptance consumes implementation",
                        "consumed_output": "implementation evidence",
                        "source_refs": ["docs/prd.md"],
                    }
                ],
                "parallel_groups": [],
                "execution_order": ["TASK-001", "TASK-002"],
                "cycle_check": {"status": "pass", "cycles": []},
            },
            "task_descriptions": [],
            "fixtures": [],
            "coverage_matrix": [],
            "delivery_acceptance": {"task_id": "TASK-002"},
            "task_logic_review": {
                "status": "pass",
                "reviewed_task_ids": ["TASK-001", "TASK-002"],
                "checks": [],
                "blocking_findings": [],
                "required_revisions": [],
            },
            "plan_integrity_review": {
                "status": "pass",
                "checks": [],
                "coverage_findings": [],
                "dependency_findings": [],
                "parallel_safety_findings": [],
                "execution_order_findings": [],
                "delivery_acceptance_findings": [],
                "blocking_findings": [],
                "required_revisions": [],
            },
            "planning_gate_report": [],
            "required_fixes": [],
        }
        if extra:
            plan.update(extra)
        return plan

    def expect_dynamic_reject(plan: dict, docs: dict[str, str], label: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture_root = Path(tmp)
            for rel, text in docs.items():
                path = fixture_root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            output_root = fixture_root / "tasks" / "development"
            output_root.mkdir(parents=True, exist_ok=True)
            (output_root / "development-planning.json").write_text(json.dumps(plan), encoding="utf-8")
            result = subprocess.run([sys.executable, str(validator), str(fixture_root)], check=False, capture_output=True, text=True)
            if result.returncode == 0:
                fail(f"package validator should reject dynamic fixture: {label}")

    expect_dynamic_reject(
        minimal_ready_plan([{"path": "docs/prd.md", "kind": "prd"}]),
        {"docs/prd.md": "PRD", "docs/contract-envelope.json": "{}"},
        "missing contract-envelope source inventory",
    )
    expect_dynamic_reject(
        minimal_ready_plan([{"path": "docs/prd.md", "kind": "prd"}]),
        {"docs/prd.md": "Requirement FR-001 must pass AC-001."},
        "missing reverse requirement coverage",
    )


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) == 2 else Path(__file__).resolve().parents[1]
    root = root.resolve()
    require_files(root)
    validate_manifest(root)
    validate_core_docs(root)
    validate_schema(root)
    validate_runtime_skill(root)
    validate_evals(root)
    validate_no_mojibake(root)
    validate_package_validator_fixtures(root)
    print("PASS: development-planning harness validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
