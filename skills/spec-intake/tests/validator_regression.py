#!/usr/bin/env python3
"""Regression probes for the spec-intake package validator.

These tests mutate the passing blocked fixture into packages that used to slip
through validation. They are intentionally local and dependency-free.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
BASE_BLOCKED = ROOT / "tests" / "fixtures" / "blocked-agent-prd-draft"
BASE_READY = ROOT / "tests" / "fixtures" / "ready-agent-prd-task-plan"
TMP = ROOT / ".tmp-validator-regression"
VALIDATOR = ROOT / "skill" / "scripts" / "validate_spec_intake_package.py"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_case(name: str, mutate: Callable[[Path], None], base: Path = BASE_BLOCKED) -> Path:
    case_dir = TMP / name
    shutil.rmtree(case_dir, ignore_errors=True)
    shutil.copytree(base, case_dir)
    mutate(case_dir)
    return case_dir


def run_validator(case_dir: Path) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), str(case_dir)],
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        payload = {"ok": False, "errors": [result.stdout, result.stderr]}
    return result.returncode, payload


def execution_ready_with_open_q_and_draft_file(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["render_status"]["agent_prd"] = "execution_ready"
    contract["gate_report"] = []
    contract["quality_gates"] = []
    contract["objects"]["GATE-001"]["payload"]["status"] = "pass"
    contract["objects"]["GATE-001"]["payload"]["blocking"] = False
    contract["objects"]["GATE-001"]["payload"]["affected_targets"] = []
    contract["objects"]["REQ-001"]["payload"]["verification_refs"] = ["VER-001"]
    for object_type in ("IN", "EXE", "VER", "OUT", "STOP", "DONE"):
        object_id = f"{object_type}-001"
        contract["objects"][object_id] = {
            "type": object_type,
            "payload": {"id": object_id, "source_refs": ["SRC-001"]},
        }
    write_json(path, contract)


def blocked_plan_missing_documented_fields(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan.pop("blocking_reasons", None)
    plan.pop("missing_required_refs", None)
    write_json(path, plan)


def noncanonical_object_namespace(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["FOO-001"] = {"type": "FOO", "payload": {"id": "FOO-001"}}
    write_json(path, contract)


def requested_agent_prd_without_render_block(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["render_blocks"] = ["RB-001"]
    contract["objects"].pop("RB-002", None)
    write_json(path, contract)


def ready_plan_missing_req_coverage(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["task_graph"][0]["contract_refs"] = ["EXE-001"]
    write_json(path, plan)


def ready_plan_from_draft_contract(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["render_status"]["agent_prd"] = "draft"
    write_json(path, contract)


def task_self_dependency_without_edge(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["task_graph"][0]["dependencies"] = ["TASK-001"]
    write_json(path, plan)


def invalid_task_and_group_status(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["task_graph"][0]["status"] = "banana"
    plan["parallel_groups"][0]["status"] = "banana"
    write_json(path, plan)


def core_wrong_type(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["core"] = "SRC-001"
    write_json(path, contract)


def invalid_object_statuses(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["REQ-001"]["payload"]["status"] = "banana"
    contract["objects"]["GATE-001"]["payload"]["status"] = "banana"
    contract["gate_report"][0]["status"] = "banana"
    write_json(path, contract)


def render_block_wrong_source_ref_type(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["RB-001"]["payload"]["source_refs"] = ["REQ-001"]
    write_json(path, contract)


def task_allowed_files_wrong_type(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["task_graph"][0]["allowed_files_or_modules"] = "src/action_items"
    write_json(path, plan)


def task_input_wrong_field_type_but_coverage_elsewhere(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["task_graph"][0]["inputs"] = ["REQ-001"]
    plan["task_graph"][0]["contract_refs"].append("IN-001")
    write_json(path, plan)


def contract_summary_drift(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["contract_summary"]["ready_targets"] = []
    contract["contract_summary"]["blocked_targets"] = ["agent_prd"]
    write_json(path, contract)


def ac_requirement_wrong_type(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["AC-001"]["payload"]["requirement_id"] = "CORE-001"
    write_json(path, contract)


def trace_wrong_endpoint_types(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["TRACE-001"]["payload"]["from_ref"] = "REQ-001"
    contract["objects"]["TRACE-001"]["payload"]["to_ref"] = "SRC-001"
    write_json(path, contract)


def gate_evidence_wrong_type_and_report_mismatch(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["GATE-001"]["payload"]["evidence_refs"] = ["REQ-001"]
    contract["gate_report"][0]["gate_id"] = "REQ-001"
    contract["gate_report"][0]["evidence_refs"] = ["REQ-001"]
    write_json(path, contract)


def source_context_wrong_type(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["source_idea"]["source_context_refs"] = ["REQ-001"]
    write_json(path, contract)


def rb_contract_refs_are_source_only(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["RB-001"]["payload"]["contract_refs"] = ["SRC-001"]
    write_json(path, contract)


def blocked_plan_wrong_phase_ref_type(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["source_artifacts"]["phase_ref"] = "REQ-001"
    write_json(path, plan)


def quality_gates_missing_gate_report_gate(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["quality_gates"] = []
    write_json(path, contract)


def traceability_summary_missing_rb(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["traceability_summary"]["render_traceability"] = []
    write_json(path, contract)


def traceability_summary_decision_wrong_type(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["traceability_summary"]["decision_traceability"] = [
        {
            "decision_type": "open_question",
            "decision_ref": "REQ-001",
            "status": "open",
            "affected_refs": ["REQ-001"],
        }
    ]
    write_json(path, contract)


def planning_gate_evidence_wrong_type(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["planning_gate_report"][0]["evidence_refs"] = ["CHECK-001"]
    write_json(path, plan)


def blocked_plan_source_status_lies_ready(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["source_artifacts"]["agent_prd_status"] = "execution_ready"
    write_json(path, plan)


def object_index_drift(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["object_index"]["REQ"] = []
    write_json(path, contract)


def core_blocked_ready(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["CORE-001"]["payload"]["status"] = "blocked"
    write_json(path, contract)


def req_blocked_ready(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["REQ-001"]["payload"]["status"] = "blocked"
    write_json(path, contract)


def stop_triggered_ready(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["STOP-001"]["payload"]["status"] = "triggered"
    write_json(path, contract)


def blocking_q_missing_status(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["Q-001"] = {
        "type": "Q",
        "payload": {
            "id": "Q-001",
            "question": "Which execution authority is confirmed?",
            "blocks_agent_prd": True,
        },
    }
    contract["open_questions"] = ["Q-001"]
    contract["object_index"]["Q"] = ["Q-001"]
    write_json(path, contract)


def gate_warning_empty_fix(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["gate_report"][0]["status"] = "warning"
    contract["gate_report"][0]["message"] = ""
    contract["gate_report"][0]["required_fix"] = ""
    contract["objects"]["GATE-001"]["payload"]["status"] = "warning"
    write_json(path, contract)


def user_confirmation_decision_ref(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["SRC-002"] = {
        "type": "SRC",
        "payload": {
            "id": "SRC-002",
            "source_type": "user_confirmation",
            "content": "User confirmed the Phase 1 execution boundary.",
        },
    }
    contract["sources"].append("SRC-002")
    contract["traceability_summary"]["decision_traceability"] = [
        {
            "decision_type": "user_confirmation",
            "decision_ref": "SRC-002",
            "status": "confirmed",
            "affected_refs": ["PHASE-001", "REQ-001"],
        }
    ]
    contract["object_index"]["SRC"].append("SRC-002")
    write_json(path, contract)


def rendered_only_blocked_plan(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["planning_source_mode"] = "rendered_agent_prd_only"
    plan["planning_status"] = "blocked"
    plan["source_artifacts"]["contract_ref"] = ""
    plan["source_artifacts"]["phase_ref"] = "Phase 1 MVP"
    plan["source_artifacts"]["phase_ref_kind"] = "rendered_label"
    plan["source_artifacts"]["phase_ref_fallback_reason"] = "Only a rendered Agent PRD label is available."
    plan["blocking_reasons"] = ["rendered_agent_prd_only"]
    plan["required_fixes"] = ["Provide contract-envelope.json with canonical PHASE refs."]
    plan["task_graph"] = []
    plan["dependency_edges"] = []
    plan["parallel_groups"] = []
    plan["stage_goal_coverage"] = []
    plan["planning_gate_report"] = [
        {
            "check_id": "CHECK-001",
            "name": "source mode",
            "status": "blocked",
            "evidence_refs": ["PHASE-001"],
            "evidence_summary": "Rendered-only source cannot produce executable tasks.",
            "required_fix": "Provide canonical contract and rerun planning.",
        }
    ]
    write_json(path, plan)


def agent_prd_missing_required_sections(case_dir: Path) -> None:
    path = case_dir / "agent-prd.md"
    path.write_text(
        "# Agent PRD\n\n"
        "Source contract: contract-envelope.json\n\n"
        "render_status.agent_prd=execution_ready\n\n"
        "REQ-001 AC-001 VER-001 IN-001 EXE-001 OUT-001 STOP-001 DONE-001\n",
        encoding="utf-8",
    )


def ready_plan_phase_has_no_current_req(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["PHASE-002"] = {
        "type": "PHASE",
        "payload": {"id": "PHASE-002", "name": "Future phase"},
    }
    contract["object_index"]["PHASE"].append("PHASE-002")
    contract["scope"]["roadmap"].append("PHASE-002")
    contract["objects"]["REQ-001"]["payload"]["phase"] = "PHASE-002"
    write_json(path, contract)


def add_future_req(contract: dict) -> None:
    contract["objects"]["PHASE-002"] = {
        "type": "PHASE",
        "payload": {"id": "PHASE-002", "name": "Future phase"},
    }
    contract["objects"]["REQ-002"] = {
        "type": "REQ",
        "payload": {
            "id": "REQ-002",
            "title": "Future requirement",
            "description": "Future requirement outside the current phase.",
            "user_value": "Future value.",
            "priority": "could",
            "phase": "PHASE-002",
            "scope_ref": "SCOPE-001",
            "acceptance_criteria": ["AC-001"],
            "verification_refs": ["VER-001"],
            "source_refs": ["SRC-001"],
            "status": "confirmed",
        },
    }
    contract["object_index"]["PHASE"].append("PHASE-002")
    contract["object_index"]["REQ"].append("REQ-002")
    contract["scope"]["roadmap"].append("PHASE-002")


def hidden_req_not_in_requirements_view(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    add_future_req(contract)
    write_json(path, contract)


def future_req_in_ready_task(case_dir: Path) -> None:
    contract_path = case_dir / "contract-envelope.json"
    contract = read_json(contract_path)
    add_future_req(contract)
    contract["requirements"].append("REQ-002")
    write_json(contract_path, contract)

    plan_path = case_dir / "execution-task-plan.json"
    plan = read_json(plan_path)
    plan["task_graph"][0]["contract_refs"].append("REQ-002")
    write_json(plan_path, plan)


def gate_object_report_drift(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["GATE-001"]["payload"]["status"] = "blocked"
    contract["objects"]["GATE-001"]["payload"]["blocking"] = True
    write_json(path, contract)


def extra_gate_object_not_in_quality_gates(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["GATE-002"] = {
        "type": "GATE",
        "payload": {
            "id": "GATE-002",
            "status": "pass",
            "blocking": False,
            "affected_targets": ["agent_prd"],
            "evidence_refs": ["REQ-001"],
        },
    }
    contract["object_index"]["GATE"].append("GATE-002")
    write_json(path, contract)


def bad_task_type(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["task_graph"][0]["task_type"] = "banana"
    write_json(path, plan)


def ready_plan_with_blocked_task(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["task_graph"][0]["status"] = "blocked"
    write_json(path, plan)


def closure_fields_empty_but_contract_refs_cover(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    task = plan["task_graph"][0]
    task["contract_refs"] = ["REQ-001", "EXE-001", "IN-001", "OUT-001", "STOP-001"]
    task["inputs"] = []
    task["outputs"] = []
    task["stop_refs"] = []
    write_json(path, plan)


def stage_goal_task_ref_goal(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["stage_goal_coverage"][0]["goal_refs"] = ["TASK-001"]
    write_json(path, plan)


def empty_required_task_refs(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["stage_goal_coverage"][0]["required_task_refs"] = []
    write_json(path, plan)


def missing_planning_gate_evidence(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    plan["planning_gate_report"][0]["evidence_refs"] = []
    write_json(path, plan)


def edge_contract_ref_task(case_dir: Path) -> None:
    path = case_dir / "execution-task-plan.json"
    plan = read_json(path)
    second = json.loads(json.dumps(plan["task_graph"][0]))
    second["task_id"] = "TASK-002"
    second["dependencies"] = ["TASK-001"]
    second["parallel_group"] = "PG-002"
    plan["task_graph"].append(second)
    plan["parallel_groups"] = [
        {"group_id": "PG-001", "task_refs": ["TASK-001"], "status": "parallel_safe"},
        {"group_id": "PG-002", "task_refs": ["TASK-002"], "status": "parallel_safe"},
    ]
    plan["dependency_edges"] = [
        {
            "from": "TASK-001",
            "to": "TASK-002",
            "reason": "Probe dependency.",
            "contract_refs": ["TASK-001"],
        }
    ]
    plan["stage_goal_coverage"][0]["required_task_refs"] = ["TASK-001", "TASK-002"]
    write_json(path, plan)


def non_iso_created_at(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["source_idea"]["created_at"] = "not-a-date"
    write_json(path, contract)


def resolved_q_without_resolution(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["Q-001"] = {
        "type": "Q",
        "payload": {
            "id": "Q-001",
            "question": "Resolved without evidence?",
            "blocks_agent_prd": False,
            "status": "resolved",
        },
    }
    contract["open_questions"] = ["Q-001"]
    contract["object_index"]["Q"] = ["Q-001"]
    write_json(path, contract)


def trace_relation_banana(case_dir: Path) -> None:
    path = case_dir / "contract-envelope.json"
    contract = read_json(path)
    contract["objects"]["TRACE-001"]["payload"]["relation"] = "banana"
    write_json(path, contract)


def main() -> int:
    shutil.rmtree(TMP, ignore_errors=True)
    TMP.mkdir(parents=True, exist_ok=True)
    try:
        checks: list[tuple[str, Path, bool]] = []
        checks.append(("blocked fixture passes", BASE_BLOCKED, True))
        checks.append(("ready fixture passes", BASE_READY, True))
        checks.append((
            "execution_ready_with_open_q_and_draft_file fails",
            make_case("execution_ready_with_open_q_and_draft_file", execution_ready_with_open_q_and_draft_file),
            False,
        ))
        checks.append((
            "blocked_plan_missing_documented_fields fails",
            make_case("blocked_plan_missing_documented_fields", blocked_plan_missing_documented_fields),
            False,
        ))
        checks.append((
            "noncanonical_object_namespace fails",
            make_case("noncanonical_object_namespace", noncanonical_object_namespace),
            False,
        ))
        checks.append((
            "requested_agent_prd_without_render_block fails",
            make_case("requested_agent_prd_without_render_block", requested_agent_prd_without_render_block),
            False,
        ))
        checks.append((
            "ready_plan_missing_req_coverage fails",
            make_case("ready_plan_missing_req_coverage", ready_plan_missing_req_coverage, BASE_READY),
            False,
        ))
        checks.append((
            "ready_plan_from_draft_contract fails",
            make_case("ready_plan_from_draft_contract", ready_plan_from_draft_contract, BASE_READY),
            False,
        ))
        checks.append((
            "task_self_dependency_without_edge fails",
            make_case("task_self_dependency_without_edge", task_self_dependency_without_edge, BASE_READY),
            False,
        ))
        checks.append((
            "invalid_task_and_group_status fails",
            make_case("invalid_task_and_group_status", invalid_task_and_group_status, BASE_READY),
            False,
        ))
        checks.append((
            "core_wrong_type fails",
            make_case("core_wrong_type", core_wrong_type, BASE_READY),
            False,
        ))
        checks.append((
            "invalid_object_statuses fails",
            make_case("invalid_object_statuses", invalid_object_statuses, BASE_READY),
            False,
        ))
        checks.append((
            "render_block_wrong_source_ref_type fails",
            make_case("render_block_wrong_source_ref_type", render_block_wrong_source_ref_type, BASE_READY),
            False,
        ))
        checks.append((
            "task_allowed_files_wrong_type fails",
            make_case("task_allowed_files_wrong_type", task_allowed_files_wrong_type, BASE_READY),
            False,
        ))
        checks.append((
            "task_input_wrong_field_type_but_coverage_elsewhere fails",
            make_case("task_input_wrong_field_type_but_coverage_elsewhere", task_input_wrong_field_type_but_coverage_elsewhere, BASE_READY),
            False,
        ))
        checks.append((
            "contract_summary_drift fails",
            make_case("contract_summary_drift", contract_summary_drift, BASE_READY),
            False,
        ))
        checks.append((
            "ac_requirement_wrong_type fails",
            make_case("ac_requirement_wrong_type", ac_requirement_wrong_type, BASE_READY),
            False,
        ))
        checks.append((
            "trace_wrong_endpoint_types fails",
            make_case("trace_wrong_endpoint_types", trace_wrong_endpoint_types, BASE_READY),
            False,
        ))
        checks.append((
            "gate_evidence_wrong_type_and_report_mismatch fails",
            make_case("gate_evidence_wrong_type_and_report_mismatch", gate_evidence_wrong_type_and_report_mismatch, BASE_READY),
            False,
        ))
        checks.append((
            "source_context_wrong_type fails",
            make_case("source_context_wrong_type", source_context_wrong_type, BASE_READY),
            False,
        ))
        checks.append((
            "rb_contract_refs_are_source_only fails",
            make_case("rb_contract_refs_are_source_only", rb_contract_refs_are_source_only, BASE_READY),
            False,
        ))
        checks.append((
            "blocked_plan_wrong_phase_ref_type fails",
            make_case("blocked_plan_wrong_phase_ref_type", blocked_plan_wrong_phase_ref_type, BASE_BLOCKED),
            False,
        ))
        checks.append((
            "quality_gates_missing_gate_report_gate fails",
            make_case("quality_gates_missing_gate_report_gate", quality_gates_missing_gate_report_gate, BASE_READY),
            False,
        ))
        checks.append((
            "traceability_summary_missing_rb fails",
            make_case("traceability_summary_missing_rb", traceability_summary_missing_rb, BASE_READY),
            False,
        ))
        checks.append((
            "traceability_summary_decision_wrong_type fails",
            make_case("traceability_summary_decision_wrong_type", traceability_summary_decision_wrong_type, BASE_READY),
            False,
        ))
        checks.append((
            "planning_gate_evidence_wrong_type fails",
            make_case("planning_gate_evidence_wrong_type", planning_gate_evidence_wrong_type, BASE_READY),
            False,
        ))
        checks.append((
            "blocked_plan_source_status_lies_ready fails",
            make_case("blocked_plan_source_status_lies_ready", blocked_plan_source_status_lies_ready, BASE_BLOCKED),
            False,
        ))
        checks.append((
            "object_index_drift fails",
            make_case("object_index_drift", object_index_drift, BASE_READY),
            False,
        ))
        checks.append((
            "core_blocked_ready fails",
            make_case("core_blocked_ready", core_blocked_ready, BASE_READY),
            False,
        ))
        checks.append((
            "req_blocked_ready fails",
            make_case("req_blocked_ready", req_blocked_ready, BASE_READY),
            False,
        ))
        checks.append((
            "stop_triggered_ready fails",
            make_case("stop_triggered_ready", stop_triggered_ready, BASE_READY),
            False,
        ))
        checks.append((
            "blocking_q_missing_status fails",
            make_case("blocking_q_missing_status", blocking_q_missing_status, BASE_READY),
            False,
        ))
        checks.append((
            "gate_warning_empty_fix fails",
            make_case("gate_warning_empty_fix", gate_warning_empty_fix, BASE_READY),
            False,
        ))
        checks.append((
            "user_confirmation_decision_ref passes",
            make_case("user_confirmation_decision_ref", user_confirmation_decision_ref, BASE_READY),
            True,
        ))
        checks.append((
            "rendered_only_blocked_plan passes",
            make_case("rendered_only_blocked_plan", rendered_only_blocked_plan, BASE_READY),
            True,
        ))
        checks.append((
            "agent_prd_missing_required_sections fails",
            make_case("agent_prd_missing_required_sections", agent_prd_missing_required_sections, BASE_READY),
            False,
        ))
        checks.append((
            "ready_plan_phase_has_no_current_req fails",
            make_case("ready_plan_phase_has_no_current_req", ready_plan_phase_has_no_current_req, BASE_READY),
            False,
        ))
        checks.append((
            "hidden_req_not_in_requirements_view fails",
            make_case("hidden_req_not_in_requirements_view", hidden_req_not_in_requirements_view, BASE_READY),
            False,
        ))
        checks.append((
            "future_req_in_ready_task fails",
            make_case("future_req_in_ready_task", future_req_in_ready_task, BASE_READY),
            False,
        ))
        checks.append((
            "gate_object_report_drift fails",
            make_case("gate_object_report_drift", gate_object_report_drift, BASE_READY),
            False,
        ))
        checks.append((
            "extra_gate_object_not_in_quality_gates fails",
            make_case("extra_gate_object_not_in_quality_gates", extra_gate_object_not_in_quality_gates, BASE_READY),
            False,
        ))
        checks.append((
            "bad_task_type fails",
            make_case("bad_task_type", bad_task_type, BASE_READY),
            False,
        ))
        checks.append((
            "ready_plan_with_blocked_task fails",
            make_case("ready_plan_with_blocked_task", ready_plan_with_blocked_task, BASE_READY),
            False,
        ))
        checks.append((
            "closure_fields_empty_but_contract_refs_cover fails",
            make_case("closure_fields_empty_but_contract_refs_cover", closure_fields_empty_but_contract_refs_cover, BASE_READY),
            False,
        ))
        checks.append((
            "stage_goal_task_ref_goal fails",
            make_case("stage_goal_task_ref_goal", stage_goal_task_ref_goal, BASE_READY),
            False,
        ))
        checks.append((
            "empty_required_task_refs fails",
            make_case("empty_required_task_refs", empty_required_task_refs, BASE_READY),
            False,
        ))
        checks.append((
            "missing_planning_gate_evidence fails",
            make_case("missing_planning_gate_evidence", missing_planning_gate_evidence, BASE_READY),
            False,
        ))
        checks.append((
            "edge_contract_ref_task fails",
            make_case("edge_contract_ref_task", edge_contract_ref_task, BASE_READY),
            False,
        ))
        checks.append((
            "non_iso_created_at fails",
            make_case("non_iso_created_at", non_iso_created_at, BASE_READY),
            False,
        ))
        checks.append((
            "resolved_q_without_resolution fails",
            make_case("resolved_q_without_resolution", resolved_q_without_resolution, BASE_READY),
            False,
        ))
        checks.append((
            "trace_relation_banana fails",
            make_case("trace_relation_banana", trace_relation_banana, BASE_READY),
            False,
        ))

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
