#!/usr/bin/env python3
"""Validate a spec-intake output package.

The validator is intentionally structural and semantic-light: it checks required
artifact shape, canonical reference integrity, readiness invariants, and HLD
handoff gates. It does not judge product usefulness or writing quality.
"""

from __future__ import annotations

import json
import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


CONTRACT_ID_PREFIXES = (
    "CORE",
    "USER",
    "SCOPE",
    "OOS",
    "PHASE",
    "REQ",
    "AC",
    "MET",
    "FLOW",
    "DATA",
    "MOD",
    "TECH",
    "STATE",
    "DCT",
    "IN",
    "EXE",
    "VER",
    "OUT",
    "STOP",
    "DONE",
    "RISK",
    "BAR",
    "ASM",
    "Q",
    "REF",
    "SRC",
    "TRACE",
    "RB",
    "META",
    "GATE",
)
PLAN_ID_PREFIXES = ("CHECK",)
ID_PREFIXES = CONTRACT_ID_PREFIXES + PLAN_ID_PREFIXES
ID_RE = re.compile(r"\b((?:" + "|".join(ID_PREFIXES) + r")-\d{3})\b")
CONTRACT_ID_RE = re.compile(r"^(?:" + "|".join(CONTRACT_ID_PREFIXES) + r")-\d{3}$")
CHECK_ID_RE = re.compile(r"^CHECK-\d{3}$")
PLANNING_GATE_STATUS = {"pass", "warning", "blocked"}
HLD_STATUS = {"ready", "blocked"}
HARNESS_WORKFLOW_TYPE = "review_gated_self_improving_generation"
HARNESS_STAGES = [
    "stage_1_requirements_table",
    "stage_2_prd_review",
    "stage_3_hld",
]
HARNESS_STAGE_STATUS = set(HARNESS_STAGES + ["complete", "blocked"])
PRD_REVIEW_STATUS = {"not_started", "pending", "approved", "revise", "failed"}
EXECUTION_MODES = {"live_interactive", "reference_replay"}
QUESTION_TYPES = {"boolean", "single_choice", "multi_choice"}
INTERACTION_DECISIONS = {"ask_user", "proceed_without_questions", "blocked_draft"}
REQUIREMENT_ROW_ORIGINS = {
    "explicit_fact",
    "confirmed_fact",
    "bounded_inference",
    "assumption",
    "open_question",
}
SOURCE_TYPES = {
    "user_input",
    "user_document",
    "user_confirmation",
    "external_reference",
    "local_file",
    "runtime_input",
    "system_generated",
}
DECISION_STATUSES = {"open", "resolved", "deferred", "superseded"}
TRACE_RELATIONS = {"stated_by", "confirmed_by", "inferred_from", "assumes", "resolves", "blocks", "renders"}
STATUS_BY_TYPE = {
    "CORE": {"draft", "confirmed", "blocked"},
    "REQ": {"draft", "confirmed", "blocked"},
    "Q": {"open", "resolved", "deferred", "superseded"},
    "ASM": {"open", "resolved", "deferred", "superseded"},
    "RB": {"ready", "blocked"},
    "STOP": {"defined", "triggered", "resolved"},
    "GATE": {"pass", "warning", "blocked"},
}
CONTRACT_REF_TYPES = set(CONTRACT_ID_PREFIXES) - {"SRC"}


VIEW_FIELDS_BY_TYPE = {
    "requirements": "REQ",
    "acceptance_criteria": "AC",
    "success_metrics": "MET",
    "risks": "RISK",
    "quality_bars": "BAR",
    "assumptions": "ASM",
    "open_questions": "Q",
    "references": "REF",
    "sources": "SRC",
    "traceability": "TRACE",
    "render_blocks": "RB",
    "document_metadata": "META",
    "quality_gates": "GATE",
}

SCOPE_VIEW_FIELDS_BY_TYPE = {
    "in_scope": "SCOPE",
    "out_of_scope": "OOS",
    "roadmap": "PHASE",
}

IMPLEMENTATION_VIEW_FIELDS_BY_TYPE = {
    "control_flow": "FLOW",
    "data_flow": "DATA",
    "modules": "MOD",
    "technical_decisions": "TECH",
    "state_transitions": "STATE",
    "data_contracts": "DCT",
}
EXECUTION_LIKE_TERMS = (
    "executor",
    "agent",
    "adapter",
    "automation",
    "cli",
    "orchestrator",
    "scheduler",
    "daemon",
    "workflow",
    "component",
    "tool",
)
HLD_STRUCTURED_LIST_FIELDS = {
    "control_flow_design": {
        "text": ("step_id", "name", "trigger", "actor_or_component", "failure_or_branch_behavior"),
        "lists": ("input_refs", "output_refs", "interaction_refs", "contract_refs"),
    },
    "data_flow_design": {
        "text": ("flow_id", "source", "transformation", "target", "persistence_or_retention"),
        "lists": ("data_refs", "contract_refs"),
    },
    "data_objects": {
        "text": ("object_name", "purpose", "lifecycle"),
        "lists": ("fields", "contract_refs"),
    },
    "interface_contracts": {
        "text": ("interface_name", "provider", "consumer", "invocation", "error_semantics"),
        "lists": ("inputs", "outputs", "source_refs", "contract_refs"),
    },
    "state_model": {
        "text": ("state", "owner"),
        "lists": ("transitions", "contract_refs"),
    },
    "technical_decisions": {
        "text": ("decision", "rationale", "implementation_notes"),
        "lists": ("contract_refs",),
    },
    "implementation_design": {
        "text": ("component_or_concern", "design"),
        "lists": ("contract_refs",),
    },
    "environment_requirements": {
        "text": ("requirement", "provided_by_or_source", "required_for"),
        "lists": ("contract_refs",),
    },
}
HLD_REAL_ACCEPTANCE_TEXT_FIELDS = ("environment", "real_data", "acceptance_owner", "acceptance_command")
HLD_REAL_ACCEPTANCE_LIST_FIELDS = (
    "preconditions",
    "execution_steps",
    "expected_results",
    "expected_artifact_paths",
    "mechanical_checks",
    "failure_criteria",
    "evidence_to_capture",
    "contract_refs",
)
HLD_REAL_ACCEPTANCE_SOURCE_REF_FIELDS = ("environment_source_refs", "real_data_source_refs", "acceptance_owner_source_refs")
HLD_FORBIDDEN_ACCEPTANCE_TERMS = ("mock", "stub", "fake", "simulated", "simulation", "synthetic")
HLD_LOOSE_INTERFACE_TERMS = (
    "or equivalent",
    "command-equivalent",
    "documented methods or",
    "when needed",
    "if applicable",
    "as needed",
    "tbd",
    "todo",
)
HLD_DEFERRED_ACCEPTANCE_TERMS = (
    "selected by",
    "supplied by",
    "provided by",
    "to be provided",
    "to be selected",
    "to be confirmed",
    "downstream",
    "later",
    "tbd",
    "todo",
    "placeholder",
)
HLD_REQUIRED_READY_DESIGN_GATE_KEYS = (
    "source_readiness",
    "control_flow_readiness",
    "data_flow_and_object_readiness",
    "interface_state_readiness",
    "technical_implementation_readiness",
    "real_acceptance_readiness",
    "hld_document_readiness",
    "task_boundary_readiness",
)
HLD_MARKDOWN_REQUIRED_SECTIONS = (
    "Revision History",
    "Scope And Goals",
    "Architecture Overview",
    "Control Flow",
    "Data Flow",
    "Data Objects",
    "Interface Contracts",
    "State Model",
    "Technical Decisions",
    "Implementation Design",
    "Real Acceptance Plan",
    "Risks And Guardrails",
    "References",
)
HLD_MARKDOWN_REQUIRED_READY_MARKERS = (
    "Source-backed interface precision",
    "Source Evidence",
    "Exact Invocation Boundary",
    "Executable acceptance design",
    "Acceptance Command",
    "Preconditions",
    "Expected Artifact Paths",
    "Mechanical Checks",
    "Failure Criteria",
)
HLD_SEMANTIC_REVIEW_REQUIRED_KEYS = (
    "source_traceability",
    "control_flow_completeness",
    "data_flow_and_objects",
    "interface_precision",
    "technical_implementation",
    "executable_acceptance",
    "markdown_parity",
    "no_untraced_invention",
    "task_boundary",
)
HLD_SEMANTIC_REVIEW_STATUS = {"pass", "warning", "blocked"}
WRITER_STATUSES = {"not_requested", "completed", "blocked", "unavailable", "failed"}
PRD_WRITER_SKILLS = {"prd-writer", "prd-writing"}
HLD_WRITER_SKILLS = {"hld-writer", "hld-writing"}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - message matters in CLI
        raise ValueError(f"{path.name} is not valid JSON: {exc}") from exc


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def same_items(left: Any, right: Any) -> bool:
    return sorted(as_list(left)) == sorted(as_list(right))


def is_iso_datetime(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def collect_ids(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, str):
        found.update(ID_RE.findall(value))
    elif isinstance(value, list):
        for item in value:
            found.update(collect_ids(item))
    elif isinstance(value, dict):
        for item in value.values():
            found.update(collect_ids(item))
    return found


def contract_source_text(contract: dict[str, Any]) -> str:
    chunks: list[str] = []
    source_idea = contract.get("source_idea")
    if isinstance(source_idea, dict):
        raw_idea = source_idea.get("raw_idea")
        if isinstance(raw_idea, str):
            chunks.append(raw_idea)
    objects = contract.get("objects")
    if isinstance(objects, dict):
        for object_id, value in objects.items():
            if not isinstance(object_id, str) or not object_id.startswith("SRC-"):
                continue
            payload = value.get("payload") if isinstance(value, dict) else {}
            if isinstance(payload, dict):
                for key in ("content", "label", "target"):
                    item = payload.get(key)
                    if isinstance(item, str):
                        chunks.append(item)
    return "\n".join(chunks).lower()


def is_execution_like_contract(contract: dict[str, Any]) -> bool:
    text = contract_source_text(contract)
    return any(term in text for term in EXECUTION_LIKE_TERMS)


def non_empty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def collect_text_excluding_keys(value: Any, excluded_keys: set[str]) -> list[str]:
    chunks: list[str] = []
    if isinstance(value, str):
        chunks.append(value)
    elif isinstance(value, list):
        for item in value:
            chunks.extend(collect_text_excluding_keys(item, excluded_keys))
    elif isinstance(value, dict):
        for key, item in value.items():
            if isinstance(key, str) and key in excluded_keys:
                continue
            chunks.extend(collect_text_excluding_keys(item, excluded_keys))
    return chunks


def has_markdown_heading(text: str, heading: str) -> bool:
    pattern = rf"(?m)^##+\s+{re.escape(heading)}\s*$"
    return re.search(pattern, text) is not None


def markdown_h2_headings(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"(?m)^##\s+(.+?)\s*$", text)]


def markdown_section(text: str, heading: str) -> str:
    pattern = rf"(?ms)^##\s+{re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def object_type_ids(contract: dict[str, Any], object_type: str) -> set[str]:
    objects = contract.get("objects") or {}
    return {
        object_id
        for object_id, obj in objects.items()
        if isinstance(obj, dict) and obj.get("type") == object_type
    }


def sorted_object_type_ids(contract: dict[str, Any], object_type: str) -> list[str]:
    return sorted(object_type_ids(contract, object_type))


def contract_current_phase_ref(contract: dict[str, Any]) -> str | None:
    scope = contract.get("scope")
    if isinstance(scope, dict):
        for phase_ref in as_list(scope.get("roadmap")):
            if object_type(contract, phase_ref) == "PHASE":
                return phase_ref
    phase_refs = sorted_object_type_ids(contract, "PHASE")
    if len(phase_refs) == 1:
        return phase_refs[0]
    return None


def current_req_ids(contract: dict[str, Any], phase_ref: str | None = None) -> list[str]:
    phase = phase_ref or contract_current_phase_ref(contract)
    req_ids = sorted_object_type_ids(contract, "REQ")
    if phase:
        return [req_id for req_id in req_ids if payload_for(contract, req_id).get("phase") == phase]
    return req_ids


def payload_for(contract: dict[str, Any], object_id: str) -> dict[str, Any]:
    obj = (contract.get("objects") or {}).get(object_id)
    if isinstance(obj, dict) and isinstance(obj.get("payload"), dict):
        return obj["payload"]
    return {}


def object_type(contract: dict[str, Any], object_id: str) -> str | None:
    obj = (contract.get("objects") or {}).get(object_id)
    if isinstance(obj, dict):
        value = obj.get("type")
        return value if isinstance(value, str) else None
    return None


def validate_ref_type(contract: dict[str, Any], ref: Any, field_name: str, expected_type: str) -> list[str]:
    if not isinstance(ref, str):
        return [f"contract-envelope.json {field_name} must be an ID string"]
    if ref not in (contract.get("objects") or {}):
        return [f"contract-envelope.json {field_name} references missing object {ref}"]
    if object_type(contract, ref) != expected_type:
        return [f"contract-envelope.json {field_name} ref {ref} must be {expected_type}"]
    return []


def validate_ref_types(
    contract: dict[str, Any],
    ref: Any,
    field_name: str,
    expected_types: set[str],
) -> list[str]:
    if not isinstance(ref, str):
        return [f"{field_name} must be an ID string"]
    if ref not in (contract.get("objects") or {}):
        return [f"{field_name} references missing object {ref}"]
    actual = object_type(contract, ref)
    if actual not in expected_types:
        expected = "/".join(sorted(expected_types))
        return [f"{field_name} ref {ref} must be {expected}"]
    return []


def validate_ref_list_types(
    contract: dict[str, Any],
    value: Any,
    field_name: str,
    expected_types: set[str],
    *,
    require_non_empty: bool = False,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list):
        return [f"{field_name} must be a list"]
    if require_non_empty and not value:
        errors.append(f"{field_name} must be non-empty")
    for index, ref in enumerate(value):
        errors.extend(validate_ref_types(contract, ref, f"{field_name}[{index}]", expected_types))
    return errors


def gate_records(contract: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for gate in as_list(contract.get("gate_report")):
        if isinstance(gate, dict):
            records.append(gate)
    for obj in (contract.get("objects") or {}).values():
        if isinstance(obj, dict) and obj.get("type") == "GATE":
            payload = obj.get("payload")
            if isinstance(payload, dict):
                records.append(payload)
    return records


def target_is_ready(render_status: dict[str, Any], target: str) -> bool:
    status = render_status.get(target)
    return status in {"review_ready", "execution_ready"}


def writer_invocation(contract: dict[str, Any], target: str) -> dict[str, Any]:
    invocations = contract.get("writer_invocations")
    if not isinstance(invocations, dict):
        return {}
    value = invocations.get(target)
    return value if isinstance(value, dict) else {}


def validate_writer_invocation(
    contract: dict[str, Any],
    target: str,
    allowed_skills: set[str],
    required_outputs: tuple[str, ...],
    *,
    require_completed: bool,
) -> list[str]:
    errors: list[str] = []
    invocation = writer_invocation(contract, target)
    if not invocation:
        return [f"writer_invocations.{target} is required"]

    writer_skill = invocation.get("writer_skill")
    if writer_skill not in allowed_skills:
        errors.append(f"writer_invocations.{target}.writer_skill must be one of: " + ", ".join(sorted(allowed_skills)))
    status = invocation.get("status")
    if status not in WRITER_STATUSES:
        errors.append(f"writer_invocations.{target}.status has invalid status")
    if require_completed and status != "completed":
        errors.append(f"writer_invocations.{target}.status must be completed")
    if status == "completed":
        outputs = invocation.get("output_artifacts")
        if not isinstance(outputs, list):
            errors.append(f"writer_invocations.{target}.output_artifacts must be a list")
            outputs = []
        output_paths = {item.get("path") for item in outputs if isinstance(item, dict)}
        for output_path in required_outputs:
            if output_path not in output_paths:
                errors.append(f"writer_invocations.{target}.output_artifacts must include {output_path}")
        for item in outputs:
            if not isinstance(item, dict):
                errors.append(f"writer_invocations.{target}.output_artifacts entries must be objects")
                continue
            sha256 = item.get("sha256")
            if not isinstance(sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", sha256):
                errors.append(f"writer_invocations.{target}.output_artifacts entry for {item.get('path')} must include lowercase sha256")
    elif status in {"blocked", "unavailable", "failed"}:
        if not non_empty_text(invocation.get("required_fix")):
            errors.append(f"writer_invocations.{target}.required_fix is required when writer is not completed")
    source_ref = invocation.get("source_ref")
    errors.extend(validate_ref_type(contract, source_ref, f"writer_invocations.{target}.source_ref", "SRC"))
    if isinstance(source_ref, str):
        payload = payload_for(contract, source_ref)
        if payload.get("source_type") != "system_generated":
            errors.append(f"writer_invocations.{target}.source_ref must point to SRC.source_type=system_generated")
    input_refs = invocation.get("input_refs")
    errors.extend(validate_ref_list_types(contract, input_refs, f"writer_invocations.{target}.input_refs", set(CONTRACT_ID_PREFIXES)))
    return errors


def has_blocked_gate_for_target(contract: dict[str, Any], target: str) -> bool:
    for gate in gate_records(contract):
        status = gate.get("status")
        blocking = gate.get("blocking")
        affected = as_list(gate.get("affected_targets"))
        if (status == "blocked" or blocking is True) and (not affected or target in affected):
            return True
    return False


def blocking_decision_refs(contract: dict[str, Any], target: str) -> list[str]:
    blockers: list[str] = []
    blocker_key = f"blocks_{target}"
    for object_id, obj in (contract.get("objects") or {}).items():
        if not isinstance(obj, dict) or obj.get("type") not in {"Q", "ASM"}:
            continue
        payload = obj.get("payload")
        if not isinstance(payload, dict):
            continue
        if payload.get(blocker_key) is True and payload.get("status") in {None, "open"}:
            blockers.append(object_id)
    return blockers


def triggered_stop_refs(contract: dict[str, Any]) -> list[str]:
    return [
        object_id
        for object_id, obj in (contract.get("objects") or {}).items()
        if isinstance(obj, dict)
        and obj.get("type") == "STOP"
        and isinstance(obj.get("payload"), dict)
        and obj["payload"].get("status") == "triggered"
    ]


def object_status_refs(contract: dict[str, Any], object_type: str, status: str) -> list[str]:
    return [
        object_id
        for object_id, obj in (contract.get("objects") or {}).items()
        if isinstance(obj, dict)
        and obj.get("type") == object_type
        and isinstance(obj.get("payload"), dict)
        and obj["payload"].get("status") == status
    ]


def readiness_blockers(contract: dict[str, Any], target: str) -> list[str]:
    blockers: list[str] = []
    blockers.extend(object_status_refs(contract, "CORE", "blocked"))
    current_reqs = set(current_req_ids(contract))
    blockers.extend(ref for ref in object_status_refs(contract, "REQ", "blocked") if ref in current_reqs)
    blockers.extend(blocking_decision_refs(contract, target))
    if target == "prd":
        blockers.extend(triggered_stop_refs(contract))
    if has_blocked_gate_for_target(contract, target):
        blockers.append("GATE")
    return sorted(set(blockers))


def validate_typed_ref_list(
    contract: dict[str, Any],
    value: Any,
    field_name: str,
    expected_type: str,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list):
        return [f"contract-envelope.json {field_name} must be a list"]
    for ref in value:
        if ref not in (contract.get("objects") or {}):
            errors.append(f"contract-envelope.json {field_name} references missing object {ref}")
        elif ((contract.get("objects") or {}).get(ref) or {}).get("type") != expected_type:
            errors.append(f"contract-envelope.json {field_name} ref {ref} must be {expected_type}")
    return errors


def execution_field_types() -> dict[str, str]:
    return {
        "input_contracts": "IN",
        "execution_rules": "EXE",
        "verification_cases": "VER",
        "output_deliverables": "OUT",
        "stop_conditions": "STOP",
        "done_criteria": "DONE",
    }


def expected_summary_targets(contract: dict[str, Any]) -> tuple[set[str], set[str]]:
    render_status = contract.get("render_status") if isinstance(contract.get("render_status"), dict) else {}
    ready: set[str] = set()
    blocked: set[str] = set()
    for target in ("prd_brief", "prd"):
        status = render_status.get(target)
        if status == "blocked" or readiness_blockers(contract, target):
            blocked.add(target)
        elif target_is_ready(render_status, target):
            ready.add(target)
    return ready, blocked


def expected_ready_plan_refs(contract: dict[str, Any], phase_ref: str | None) -> set[str]:
    expected: set[str] = set()

    req_ids = current_req_ids(contract, phase_ref)
    for req_id in req_ids:
        expected.add(req_id)
        req_payload = payload_for(contract, req_id)
        for ac_ref in as_list(req_payload.get("acceptance_criteria")):
            expected.add(ac_ref)
        for ref in collect_ids(req_payload):
            if ref.startswith("VER-"):
                expected.add(ref)

    for ac_id in object_type_ids(contract, "AC"):
        if payload_for(contract, ac_id).get("requirement_id") in req_ids:
            expected.add(ac_id)

    agent_execution = contract.get("agent_execution") if isinstance(contract.get("agent_execution"), dict) else {}
    for field_name in execution_field_types():
        expected.update(ref for ref in as_list(agent_execution.get(field_name)) if isinstance(ref, str))

    implementation_model = contract.get("implementation_model") if isinstance(contract.get("implementation_model"), dict) else {}
    for field_name in IMPLEMENTATION_VIEW_FIELDS_BY_TYPE:
        expected.update(ref for ref in as_list(implementation_model.get(field_name)) if isinstance(ref, str))

    return expected


def validate_gate_record(
    contract: dict[str, Any],
    gate: dict[str, Any],
    field_name: str,
) -> list[str]:
    errors: list[str] = []
    errors.extend(validate_ref_type(contract, gate.get("gate_id"), f"{field_name}.gate_id", "GATE"))
    status = gate.get("status")
    blocking = gate.get("blocking")
    if status not in PLANNING_GATE_STATUS:
        errors.append(f"{field_name}.status has invalid status")
    if "blocking" in gate and not isinstance(blocking, bool):
        errors.append(f"{field_name}.blocking must be boolean")
    if status in {"pass", "warning"} and blocking is not False:
        errors.append(f"{field_name}.blocking must be false when status is pass or warning")
    if blocking is True and status != "blocked":
        errors.append(f"{field_name}.status must be blocked when blocking is true")
    if status == "warning" and (not gate.get("message") or not gate.get("required_fix")):
        errors.append(f"{field_name}.warning requires non-empty message and required_fix")
    if status == "blocked" and not gate.get("required_fix"):
        errors.append(f"{field_name}.blocked requires non-empty required_fix")
    affected = gate.get("affected_targets")
    if not isinstance(affected, list):
        errors.append(f"{field_name}.affected_targets must be a list")
    else:
        for target in affected:
            if target not in {"prd_brief", "prd", "hld"}:
                errors.append(f"{field_name}.affected_targets has invalid target {target!r}")
    errors.extend(validate_ref_list_types(contract, gate.get("evidence_refs"), f"{field_name}.evidence_refs", set(CONTRACT_ID_PREFIXES)))
    return errors


def validate_view_matches_objects(contract: dict[str, Any], field_name: str, value: Any, object_type_name: str) -> list[str]:
    expected = sorted_object_type_ids(contract, object_type_name)
    if not same_items(value, expected):
        return [f"contract-envelope.json {field_name} must match all {object_type_name} objects"]
    return []


def validate_gate_report_consistency(contract: dict[str, Any], gate_report: list[Any]) -> list[str]:
    errors: list[str] = []
    report_by_id = {
        gate.get("gate_id"): gate
        for gate in gate_report
        if isinstance(gate, dict) and isinstance(gate.get("gate_id"), str)
    }
    for gate_id in sorted_object_type_ids(contract, "GATE"):
        payload = payload_for(contract, gate_id)
        report = report_by_id.get(gate_id)
        if not isinstance(report, dict):
            errors.append(f"gate_report missing record for {gate_id}")
            continue
        for key in ("status", "blocking"):
            if payload.get(key) != report.get(key):
                errors.append(f"gate_report.{gate_id}.{key} must match objects.{gate_id}.payload.{key}")
        for key in ("affected_targets", "evidence_refs"):
            if not same_items(payload.get(key), report.get(key)):
                errors.append(f"gate_report.{gate_id}.{key} must match objects.{gate_id}.payload.{key}")
    return errors


def validate_traceability_summary(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    summary = contract.get("traceability_summary")
    if not isinstance(summary, dict):
        return ["contract-envelope.json traceability_summary must be an object"]

    render_traceability = set(as_list(summary.get("render_traceability")))
    expected_render = set(as_list(contract.get("render_blocks")))
    if render_traceability != expected_render:
        errors.append("traceability_summary.render_traceability must match render_blocks")

    requirement_traceability = set(as_list(summary.get("requirement_traceability")))
    expected_requirement = set(as_list(contract.get("traceability")))
    if requirement_traceability != expected_requirement:
        errors.append("traceability_summary.requirement_traceability must match traceability")

    decision_traceability = summary.get("decision_traceability")
    if not isinstance(decision_traceability, list):
        errors.append("traceability_summary.decision_traceability must be a list")
        return errors
    for index, item in enumerate(decision_traceability):
        if not isinstance(item, dict):
            errors.append(f"traceability_summary.decision_traceability[{index}] must be an object")
            continue
        decision_type = item.get("decision_type")
        decision_ref = item.get("decision_ref")
        status = item.get("status")
        if decision_type == "open_question":
            errors.extend(validate_ref_types(contract, decision_ref, f"traceability_summary.decision_traceability[{index}].decision_ref", {"Q"}))
            if status not in DECISION_STATUSES:
                errors.append(f"traceability_summary.decision_traceability[{index}].status has invalid status")
        elif decision_type == "assumption":
            errors.extend(validate_ref_types(contract, decision_ref, f"traceability_summary.decision_traceability[{index}].decision_ref", {"ASM"}))
            if status not in DECISION_STATUSES:
                errors.append(f"traceability_summary.decision_traceability[{index}].status has invalid status")
        elif decision_type == "user_confirmation":
            errors.extend(validate_ref_types(contract, decision_ref, f"traceability_summary.decision_traceability[{index}].decision_ref", {"SRC"}))
            if isinstance(decision_ref, str) and payload_for(contract, decision_ref).get("source_type") != "user_confirmation":
                errors.append(f"traceability_summary.decision_traceability[{index}].decision_ref must be SRC with source_type=user_confirmation")
            if status != "confirmed":
                errors.append(f"traceability_summary.decision_traceability[{index}].status must be confirmed for user_confirmation")
        else:
            errors.append(f"traceability_summary.decision_traceability[{index}].decision_type has invalid type")
        if not as_list(item.get("affected_refs")):
            errors.append(f"traceability_summary.decision_traceability[{index}].affected_refs must be non-empty")
        errors.extend(validate_ref_list_types(contract, item.get("affected_refs"), f"traceability_summary.decision_traceability[{index}].affected_refs", set(CONTRACT_ID_PREFIXES)))
    return errors


def expected_object_index(contract: dict[str, Any]) -> dict[str, list[str]]:
    grouped = {prefix: [] for prefix in CONTRACT_ID_PREFIXES}
    for object_id in sorted((contract.get("objects") or {}).keys()):
        prefix = object_id.split("-")[0]
        if prefix in grouped:
            grouped[prefix].append(object_id)
    return grouped


def validate_object_index(contract: dict[str, Any]) -> list[str]:
    actual = contract.get("object_index")
    if not isinstance(actual, dict):
        return ["contract-envelope.json object_index must be an object"]
    expected = expected_object_index(contract)
    errors: list[str] = []
    for prefix, expected_refs in expected.items():
        refs = actual.get(prefix)
        if refs != expected_refs:
            errors.append(f"object_index.{prefix} must match objects of type {prefix}")
    extra = sorted(set(actual) - set(expected))
    if extra:
        errors.append("object_index has non-canonical keys: " + ", ".join(extra))
    return errors


def prd_review_approval_payload_errors(contract: dict[str, Any], source_ref: Any) -> list[str]:
    errors: list[str] = []
    payload = payload_for(contract, source_ref) if isinstance(source_ref, str) else {}
    if payload.get("source_type") != "user_confirmation":
        errors.append("prd_review.approved_by_ref must reference a user_confirmation SRC")
        return errors
    if payload.get("confirmation_kind") != "prd_review_approval":
        errors.append("PRD review approval source must set confirmation_kind=prd_review_approval")
    if payload.get("confirmation_intent") != "approve_prd_and_enter_stage_3":
        errors.append("PRD review approval source must set confirmation_intent=approve_prd_and_enter_stage_3")
    if payload.get("confirmed_stage") != "stage_2_prd_review":
        errors.append("PRD review approval source must set confirmed_stage=stage_2_prd_review")
    artifacts = payload.get("approved_artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        errors.append("PRD review approval source must include approved_artifacts")
    else:
        artifact_paths = {item.get("path") for item in artifacts if isinstance(item, dict)}
        for expected_path in ("prd.md", "prd-brief.md"):
            if expected_path not in artifact_paths:
                errors.append(f"PRD review approval source approved_artifacts must include path={expected_path}")
    return errors


def validate_harness_workflow(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    workflow = contract.get("harness_workflow")
    if not isinstance(workflow, dict):
        return ["contract-envelope.json harness_workflow must be an object"]

    if workflow.get("workflow_type") != HARNESS_WORKFLOW_TYPE:
        errors.append(f"harness_workflow.workflow_type must be {HARNESS_WORKFLOW_TYPE}")
    execution_mode = workflow.get("execution_mode")
    if execution_mode not in EXECUTION_MODES:
        errors.append("harness_workflow.execution_mode must be live_interactive or reference_replay")
    if not isinstance(workflow.get("execution_mode_reason"), str) or not workflow.get("execution_mode_reason", "").strip():
        errors.append("harness_workflow.execution_mode_reason must be a non-empty string")
    if workflow.get("stage_order") != HARNESS_STAGES:
        errors.append("harness_workflow.stage_order must define the three required stages in order")
    current_stage = workflow.get("current_stage")
    if current_stage not in HARNESS_STAGE_STATUS:
        errors.append("harness_workflow.current_stage has invalid stage")
    if execution_mode == "reference_replay" and current_stage in {"stage_3_hld", "complete"}:
        errors.append("reference_replay cannot claim completed Stage 3 or full live workflow readiness")

    approvals = workflow.get("approval_gates")
    if not isinstance(approvals, dict):
        errors.append("harness_workflow.approval_gates must be an object")
        approvals = {}
    human_review = approvals.get("prd_review")
    if not isinstance(human_review, dict):
        errors.append("harness_workflow.approval_gates.prd_review must be an object")
        human_review = {}
    review_status = human_review.get("status")
    if review_status not in PRD_REVIEW_STATUS:
        errors.append("harness_workflow.approval_gates.prd_review.status has invalid status")
    approved_by = human_review.get("approved_by_ref")
    if review_status == "approved":
        errors.extend(validate_ref_types(
            contract,
            approved_by,
            "harness_workflow.approval_gates.prd_review.approved_by_ref",
            {"SRC"},
        ))
        if isinstance(approved_by, str) and payload_for(contract, approved_by).get("source_type") != "user_confirmation":
            errors.append("harness_workflow.approval_gates.prd_review.approved_by_ref must be a user_confirmation SRC")
        errors.extend(prd_review_approval_payload_errors(contract, approved_by))
        if execution_mode != "live_interactive":
            errors.append("approved prd_review requires harness_workflow.execution_mode=live_interactive")
    elif approved_by:
        errors.append("harness_workflow.approval_gates.prd_review.approved_by_ref is allowed only when status=approved")

    revision_policy = workflow.get("revision_policy")
    if not isinstance(revision_policy, dict):
        errors.append("harness_workflow.revision_policy must be an object")
    else:
        if not isinstance(revision_policy.get("max_review_rounds"), int) or revision_policy.get("max_review_rounds") < 1:
            errors.append("harness_workflow.revision_policy.max_review_rounds must be a positive integer")
        if revision_policy.get("on_revise") != "update_requirement_table_then_rerender_prds":
            errors.append("harness_workflow.revision_policy.on_revise must route back through the requirement table")

    return errors


def stage_1_blocking_refs(contract: dict[str, Any]) -> list[str]:
    blockers: set[str] = set()
    for target in ("prd_brief", "prd"):
        blockers.update(blocking_decision_refs(contract, target))
        if has_blocked_gate_for_target(contract, target):
            blockers.update(sorted_object_type_ids(contract, "GATE"))
    blockers.update(triggered_stop_refs(contract))
    return sorted(blockers)


def validate_interaction_decision(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    decision = contract.get("interaction_decision")
    if not isinstance(decision, dict):
        return ["contract-envelope.json interaction_decision must be an object"]

    if decision.get("stage") != "stage_1_requirements_table":
        errors.append("interaction_decision.stage must be stage_1_requirements_table")
    if decision.get("decision") not in INTERACTION_DECISIONS:
        errors.append("interaction_decision.decision has invalid decision")
    if not isinstance(decision.get("can_ask_user"), bool):
        errors.append("interaction_decision.can_ask_user must be boolean")
    if not isinstance(decision.get("reason"), str) or not decision.get("reason").strip():
        errors.append("interaction_decision.reason must be a non-empty string")

    errors.extend(validate_ref_list_types(
        contract,
        decision.get("source_refs"),
        "interaction_decision.source_refs",
        {"SRC"},
        require_non_empty=True,
    ))
    errors.extend(validate_ref_list_types(
        contract,
        decision.get("question_refs"),
        "interaction_decision.question_refs",
        {"Q"},
    ))
    errors.extend(validate_ref_list_types(
        contract,
        decision.get("blocking_refs"),
        "interaction_decision.blocking_refs",
        {"Q", "ASM", "STOP", "GATE"},
    ))

    blockers = set(stage_1_blocking_refs(contract))
    declared_blockers = set(ref for ref in as_list(decision.get("blocking_refs")) if isinstance(ref, str))
    missing_blockers = sorted(blockers - declared_blockers)
    if missing_blockers:
        errors.append("interaction_decision.blocking_refs missing blockers: " + ", ".join(missing_blockers))
    if blockers and decision.get("decision") == "proceed_without_questions":
        errors.append("interaction_decision.decision cannot proceed_without_questions while blockers exist")
    if not blockers and as_list(decision.get("blocking_refs")):
        errors.append("interaction_decision.blocking_refs must be empty when no blockers exist")

    question_refs = [ref for ref in as_list(decision.get("question_refs")) if isinstance(ref, str)]
    if decision.get("decision") == "ask_user":
        if decision.get("can_ask_user") is not True:
            errors.append("interaction_decision.can_ask_user must be true when decision=ask_user")
        if not question_refs:
            errors.append("interaction_decision.question_refs must be non-empty when decision=ask_user")
    if question_refs:
        for ref in question_refs:
            if ref not in declared_blockers and ref in blockers:
                errors.append(f"interaction_decision.question_refs {ref} must also appear in blocking_refs")
    if decision.get("decision") == "proceed_without_questions":
        if question_refs:
            errors.append("interaction_decision.question_refs must be empty when proceeding without questions")
        if decision.get("can_ask_user") is not True:
            errors.append("interaction_decision.can_ask_user must be true when proceeding without questions")
    if decision.get("decision") == "blocked_draft" and not blockers:
        errors.append("interaction_decision.decision=blocked_draft requires at least one blocker")

    return errors


def has_inferred_trace(contract: dict[str, Any], req_ref: str) -> bool:
    for trace_id in as_list(contract.get("traceability")):
        if object_type(contract, trace_id) != "TRACE":
            continue
        payload = payload_for(contract, trace_id)
        if payload.get("relation") == "inferred_from" and payload.get("to_ref") == req_ref:
            return True
    return False


def validate_requirement_table(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    table = contract.get("requirement_table")
    if not isinstance(table, list):
        return ["contract-envelope.json requirement_table must be a list"]
    if not table:
        errors.append("contract-envelope.json requirement_table must be non-empty")
        return errors

    seen_reqs: set[str] = set()
    for index, row in enumerate(table):
        field = f"requirement_table[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{field} must be an object")
            continue
        row_id = row.get("row_id")
        if not isinstance(row_id, str) or not re.fullmatch(r"RT-\d{3}", row_id):
            errors.append(f"{field}.row_id must use RT-###")
        req_ref = row.get("requirement_ref")
        errors.extend(validate_ref_type(contract, req_ref, f"{field}.requirement_ref", "REQ"))
        if isinstance(req_ref, str):
            seen_reqs.add(req_ref)
        origin = row.get("origin")
        if origin not in REQUIREMENT_ROW_ORIGINS:
            errors.append(f"{field}.origin has invalid origin")
        source_refs = row.get("source_refs")
        if not isinstance(source_refs, list) or not source_refs:
            errors.append(f"{field}.source_refs must be non-empty")
        else:
            errors.extend(validate_ref_list_types(contract, source_refs, f"{field}.source_refs", {"SRC", "ASM", "Q"}, require_non_empty=True))
            source_types = {object_type(contract, ref) for ref in source_refs if isinstance(ref, str)}
            if origin in {"explicit_fact", "confirmed_fact"} and "SRC" not in source_types:
                errors.append(f"{field}.source_refs must include SRC for origin={origin}")
            if origin == "assumption" and "ASM" not in source_types:
                errors.append(f"{field}.source_refs must include ASM for origin=assumption")
            if origin == "open_question" and "Q" not in source_types:
                errors.append(f"{field}.source_refs must include Q for origin=open_question")
            if origin == "bounded_inference":
                if "SRC" not in source_types:
                    errors.append(f"{field}.source_refs must include SRC for origin=bounded_inference")
                if isinstance(req_ref, str) and not has_inferred_trace(contract, req_ref):
                    errors.append(f"{field}.origin=bounded_inference requires TRACE relation inferred_from to {req_ref}")
        for key in ("problem", "user_value", "mvp_scope", "acceptance_summary"):
            if not isinstance(row.get(key), str) or not row.get(key).strip():
                errors.append(f"{field}.{key} must be a non-empty string")
        target_refs = row.get("target_artifact_refs")
        if not isinstance(target_refs, list) or not target_refs:
            errors.append(f"{field}.target_artifact_refs must be non-empty")
        else:
            allowed = {"REQ", "AC", "RB", "IN", "EXE", "VER", "OUT", "STOP", "DONE"}
            errors.extend(validate_ref_list_types(contract, target_refs, f"{field}.target_artifact_refs", allowed, require_non_empty=True))

    current_reqs = set(current_req_ids(contract))
    missing = sorted(current_reqs - seen_reqs)
    if missing:
        errors.append("requirement_table missing current requirements: " + ", ".join(missing))
    return errors


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def stage1_prd_support_gaps(contract: dict[str, Any]) -> list[str]:
    decision = contract.get("interaction_decision")
    if not isinstance(decision, dict) or decision.get("decision") != "proceed_without_questions":
        return []

    gaps: list[str] = []
    core_ref = contract.get("core")
    core_payload = payload_for(contract, core_ref) if isinstance(core_ref, str) else {}
    for key in ("product_name", "one_line_summary", "problem_statement", "value_proposition"):
        if not non_empty_string(core_payload.get(key)):
            gaps.append(f"CORE.{key}")
    if not as_list(core_payload.get("target_users")) and not as_list(core_payload.get("personas")) and not object_type_ids(contract, "USER"):
        gaps.append("CORE.target_users_or_personas")
    if not as_list(core_payload.get("source_refs")):
        gaps.append("CORE.source_refs")

    scope = contract.get("scope") if isinstance(contract.get("scope"), dict) else {}
    if not as_list(scope.get("in_scope")):
        gaps.append("scope.in_scope")
    if not non_empty_string(scope.get("mvp_boundary")):
        gaps.append("scope.mvp_boundary")
    if not as_list(scope.get("roadmap")):
        gaps.append("scope.roadmap")

    current_reqs = current_req_ids(contract)
    if not current_reqs:
        gaps.append("requirements.current_phase")
    rows = [row for row in as_list(contract.get("requirement_table")) if isinstance(row, dict)]
    if not rows:
        gaps.append("requirement_table")
    if current_reqs and not any(row.get("requirement_ref") in current_reqs for row in rows):
        gaps.append("requirement_table.current_phase_rows")

    if not as_list(contract.get("acceptance_criteria")):
        gaps.append("acceptance_criteria")
    if not as_list(contract.get("success_metrics")):
        has_verification = bool(as_list(contract.get("acceptance_criteria")) and as_list((contract.get("agent_execution") or {}).get("verification_cases")))
        if not has_verification:
            gaps.append("success_metrics_or_verification")

    implementation_model = contract.get("implementation_model") if isinstance(contract.get("implementation_model"), dict) else {}
    agent_execution = contract.get("agent_execution") if isinstance(contract.get("agent_execution"), dict) else {}
    implementation_support = any(as_list(implementation_model.get(field_name)) for field_name in IMPLEMENTATION_VIEW_FIELDS_BY_TYPE)
    implementation_support = implementation_support or bool(as_list(agent_execution.get("execution_rules")))
    if not implementation_support:
        gaps.append("implementation_model")
    if is_execution_like_contract(contract):
        if not as_list(implementation_model.get("control_flow")):
            gaps.append("implementation_model.control_flow")
        if not as_list(implementation_model.get("modules")):
            gaps.append("implementation_model.modules")
        if not as_list(implementation_model.get("technical_decisions")):
            gaps.append("implementation_model.technical_decisions")

    for field_name in execution_field_types():
        if not as_list(agent_execution.get(field_name)):
            gaps.append(f"agent_execution.{field_name}")

    if not as_list(contract.get("sources")):
        gaps.append("sources")

    return sorted(set(gaps))


def validate_stage1_prd_support(contract: dict[str, Any]) -> list[str]:
    gaps = stage1_prd_support_gaps(contract)
    if not gaps:
        return []
    return [
        "interaction_decision.decision cannot proceed_without_questions without PRD-ready Stage 1 support: "
        + ", ".join(gaps)
    ]


def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "contract_version",
        "intake_id",
        "harness_workflow",
        "source_idea",
        "interaction_decision",
        "requirement_table",
        "core",
        "scope",
        "requirements",
        "acceptance_criteria",
        "success_metrics",
        "implementation_model",
        "agent_execution",
        "risks",
        "quality_bars",
        "assumptions",
        "open_questions",
        "references",
        "sources",
        "traceability",
        "render_blocks",
        "document_metadata",
        "quality_gates",
        "render_status",
        "objects",
        "object_index",
        "contract_summary",
        "traceability_summary",
        "gate_report",
        "next_actions",
    ]
    for key in required:
        if key not in contract:
            errors.append(f"contract-envelope.json missing {key}")

    objects = contract.get("objects", {})
    if not isinstance(objects, dict):
        errors.append("contract-envelope.json objects must be an object")
        objects = {}

    known = set(objects.keys())
    all_refs = collect_ids(contract)
    dangling = sorted(ref for ref in all_refs if ref not in known and not ref.startswith(("TASK-", "PG-", "CHECK-")))
    if dangling:
        errors.append("contract-envelope.json has dangling refs: " + ", ".join(dangling))

    for field_name, expected_type in VIEW_FIELDS_BY_TYPE.items():
        errors.extend(validate_typed_ref_list(contract, contract.get(field_name), field_name, expected_type))
        errors.extend(validate_view_matches_objects(contract, field_name, contract.get(field_name), expected_type))

    if not isinstance(contract.get("next_actions"), list):
        errors.append("contract-envelope.json next_actions must be a list")
    errors.extend(validate_object_index(contract))

    source_idea = contract.get("source_idea")
    if not isinstance(source_idea, dict):
        errors.append("contract-envelope.json source_idea must be an object")
        source_idea = {}
    if not isinstance(source_idea.get("raw_idea"), str) or not source_idea.get("raw_idea"):
        errors.append("source_idea.raw_idea must be a non-empty string")
    if not isinstance(source_idea.get("created_at"), str) or not source_idea.get("created_at"):
        errors.append("source_idea.created_at must be a non-empty string")
    elif not is_iso_datetime(source_idea["created_at"]):
        errors.append("source_idea.created_at must be ISO-8601")
    errors.extend(validate_ref_list_types(contract, source_idea.get("source_context_refs"), "source_idea.source_context_refs", {"SRC"}))
    errors.extend(validate_harness_workflow(contract))
    errors.extend(validate_interaction_decision(contract))
    errors.extend(validate_requirement_table(contract))
    errors.extend(validate_stage1_prd_support(contract))

    errors.extend(validate_ref_type(contract, contract.get("core"), "core", "CORE"))
    scope = contract.get("scope")
    if not isinstance(scope, dict):
        errors.append("contract-envelope.json scope must be an object")
        scope = {}
    for field_name, expected_type in SCOPE_VIEW_FIELDS_BY_TYPE.items():
        errors.extend(validate_typed_ref_list(contract, scope.get(field_name), f"scope.{field_name}", expected_type))
        errors.extend(validate_view_matches_objects(contract, f"scope.{field_name}", scope.get(field_name), expected_type))

    implementation_model = contract.get("implementation_model")
    if not isinstance(implementation_model, dict):
        errors.append("contract-envelope.json implementation_model must be an object")
        implementation_model = {}
    for field_name, expected_type in IMPLEMENTATION_VIEW_FIELDS_BY_TYPE.items():
        errors.extend(validate_typed_ref_list(contract, implementation_model.get(field_name), f"implementation_model.{field_name}", expected_type))
        errors.extend(validate_view_matches_objects(contract, f"implementation_model.{field_name}", implementation_model.get(field_name), expected_type))

    agent_execution_for_type_check = contract.get("agent_execution")
    if not isinstance(agent_execution_for_type_check, dict):
        errors.append("contract-envelope.json agent_execution must be an object")
        agent_execution_for_type_check = {}
    for field_name, expected_type in execution_field_types().items():
        errors.extend(validate_typed_ref_list(contract, agent_execution_for_type_check.get(field_name), f"agent_execution.{field_name}", expected_type))
        errors.extend(validate_view_matches_objects(contract, f"agent_execution.{field_name}", agent_execution_for_type_check.get(field_name), expected_type))

    text = json.dumps(contract, ensure_ascii=False)
    for forbidden in ("internal_confidence", "candidate_score", "question_priority"):
        if forbidden in text:
            errors.append(f"contract-envelope.json leaks internal field {forbidden}")

    render_status = contract.get("render_status")
    if not isinstance(render_status, dict):
        errors.append("contract-envelope.json render_status must be an object")
        render_status = {}

    allowed_prd_brief = {"not_requested", "draft", "review_ready", "blocked"}
    allowed_prd = {"not_requested", "draft", "review_ready", "blocked"}
    if "human_prd" in render_status or "agent_prd" in render_status:
        errors.append("render_status must not contain legacy human_prd or agent_prd keys")
    if render_status.get("prd_brief") not in allowed_prd_brief:
        errors.append("render_status.prd_brief has invalid status")
    if render_status.get("prd") not in allowed_prd:
        errors.append("render_status.prd has invalid status")

    for target in ("prd_brief", "prd"):
        blockers = readiness_blockers(contract, target)
        if target_is_ready(render_status, target) and blockers:
            errors.append(f"render_status.{target} cannot be ready while blockers exist: " + ", ".join(sorted(blockers)))

    render_blocks_by_target: dict[str, list[str]] = {"prd_brief": [], "prd": []}
    for object_id, obj in objects.items():
        if not isinstance(obj, dict):
            errors.append(f"objects.{object_id} must be an object")
            continue
        if not CONTRACT_ID_RE.fullmatch(object_id):
            errors.append(f"objects.{object_id} uses a non-canonical contract ID prefix")
        if obj.get("type") != object_id.split("-")[0]:
            errors.append(f"objects.{object_id}.type must match ID prefix")
        if obj.get("type") not in CONTRACT_ID_PREFIXES:
            errors.append(f"objects.{object_id}.type is not a canonical contract object type")
        payload = obj.get("payload")
        if not isinstance(payload, dict):
            errors.append(f"objects.{object_id}.payload must be an object")
            continue
        if payload.get("id") != object_id:
            errors.append(f"objects.{object_id}.payload.id must equal object ID")
        object_kind = obj.get("type")
        if "status" in payload:
            allowed_status = STATUS_BY_TYPE.get(object_kind)
            if allowed_status is None:
                errors.append(f"objects.{object_id}.payload.status is not allowed for type {object_kind}")
            elif payload.get("status") not in allowed_status:
                errors.append(f"objects.{object_id}.payload.status has invalid status")
        if object_kind == "AC":
            errors.extend(validate_ref_type(contract, payload.get("requirement_id"), f"objects.{object_id}.payload.requirement_id", "REQ"))
            if not payload.get("criterion"):
                errors.append(f"objects.{object_id}.payload.criterion must be non-empty")
            if payload.get("blocking") is True and not payload.get("verification_method"):
                errors.append(f"objects.{object_id}.payload.verification_method is required when blocking=true")
            if "verification_method" in payload and isinstance(payload.get("verification_method"), str) and ID_RE.fullmatch(payload["verification_method"]):
                errors.extend(validate_ref_type(contract, payload.get("verification_method"), f"objects.{object_id}.payload.verification_method", "VER"))
        if object_kind == "REQ":
            errors.extend(validate_ref_list_types(contract, payload.get("acceptance_criteria"), f"objects.{object_id}.payload.acceptance_criteria", {"AC"}))
            if "verification_refs" in payload:
                errors.extend(validate_ref_list_types(contract, payload.get("verification_refs"), f"objects.{object_id}.payload.verification_refs", {"VER"}))
            if "phase" in payload:
                errors.extend(validate_ref_type(contract, payload.get("phase"), f"objects.{object_id}.payload.phase", "PHASE"))
            if "scope_ref" in payload:
                errors.extend(validate_ref_type(contract, payload.get("scope_ref"), f"objects.{object_id}.payload.scope_ref", "SCOPE"))
            if "source_refs" in payload:
                errors.extend(validate_ref_list_types(contract, payload.get("source_refs"), f"objects.{object_id}.payload.source_refs", {"SRC"}))
        if object_kind == "SRC":
            if payload.get("source_type") not in SOURCE_TYPES:
                errors.append(f"objects.{object_id}.payload.source_type has invalid source type")
            if payload.get("source_type") in {"user_input", "user_document", "user_confirmation"}:
                if not payload.get("content") and not payload.get("target"):
                    errors.append(f"objects.{object_id}.payload must include content or target for user source")
        if object_kind in {"CORE", "SCOPE", "OOS", "IN", "EXE", "VER", "OUT", "STOP", "DONE"} and "source_refs" in payload:
            errors.extend(validate_ref_list_types(contract, payload.get("source_refs"), f"objects.{object_id}.payload.source_refs", {"SRC"}))
        if object_kind == "SCOPE" and "phase" in payload:
            errors.extend(validate_ref_type(contract, payload.get("phase"), f"objects.{object_id}.payload.phase", "PHASE"))
        if object_kind == "Q":
            question_type = payload.get("question_type")
            options = payload.get("options")
            if question_type not in QUESTION_TYPES:
                errors.append(f"objects.{object_id}.payload.question_type must be boolean, single_choice, or multi_choice")
            if not isinstance(options, list) or len(options) < 2:
                errors.append(f"objects.{object_id}.payload.options must contain at least two choices")
            elif question_type == "boolean" and len(options) != 2:
                errors.append(f"objects.{object_id}.payload.options must contain exactly two choices for boolean questions")
            elif any(not isinstance(option, str) or not option.strip() for option in options):
                errors.append(f"objects.{object_id}.payload.options must contain non-empty strings")
            if (payload.get("blocks_prd_brief") is True or payload.get("blocks_prd") is True) and "status" not in payload:
                errors.append(f"objects.{object_id}.payload.status is required when Q blocks a target")
            if payload.get("status") == "resolved" and not as_list(payload.get("resolution_refs")):
                errors.append(f"objects.{object_id}.payload.resolution_refs is required when Q is resolved")
            if "resolution_refs" in payload:
                errors.extend(validate_ref_list_types(contract, payload.get("resolution_refs"), f"objects.{object_id}.payload.resolution_refs", set(CONTRACT_ID_PREFIXES)))
        if object_kind == "ASM":
            if (payload.get("blocks_prd_brief") is True or payload.get("blocks_prd") is True) and "status" not in payload:
                errors.append(f"objects.{object_id}.payload.status is required when ASM blocks a target")
            if payload.get("status") == "resolved" and not as_list(payload.get("resolution_refs")):
                errors.append(f"objects.{object_id}.payload.resolution_refs is required when ASM is resolved")
            if "resolution_refs" in payload:
                errors.extend(validate_ref_list_types(contract, payload.get("resolution_refs"), f"objects.{object_id}.payload.resolution_refs", set(CONTRACT_ID_PREFIXES)))
        if object_kind == "STOP":
            if payload.get("status") == "resolved" and not as_list(payload.get("resolution_refs")):
                errors.append(f"objects.{object_id}.payload.resolution_refs is required when STOP is resolved")
        if object_kind == "TRACE":
            errors.extend(validate_ref_types(contract, payload.get("from_ref"), f"objects.{object_id}.payload.from_ref", {"SRC"}))
            errors.extend(validate_ref_types(contract, payload.get("to_ref"), f"objects.{object_id}.payload.to_ref", CONTRACT_REF_TYPES))
            if payload.get("relation") not in TRACE_RELATIONS:
                errors.append(f"objects.{object_id}.payload.relation has invalid relation")
        if object_kind == "GATE":
            if payload.get("status") not in PLANNING_GATE_STATUS:
                errors.append(f"objects.{object_id}.payload.status has invalid status")
            if "blocking" in payload and not isinstance(payload.get("blocking"), bool):
                errors.append(f"objects.{object_id}.payload.blocking must be boolean")
            affected = payload.get("affected_targets")
            if not isinstance(affected, list):
                errors.append(f"objects.{object_id}.payload.affected_targets must be a list")
            else:
                for target in affected:
                    if target not in {"prd_brief", "prd", "hld"}:
                        errors.append(f"objects.{object_id}.payload.affected_targets has invalid target {target!r}")
            errors.extend(validate_ref_list_types(contract, payload.get("evidence_refs"), f"objects.{object_id}.payload.evidence_refs", set(CONTRACT_ID_PREFIXES)))
        if obj.get("type") == "RB":
            target = payload.get("target")
            if target not in {"prd_brief", "prd"}:
                errors.append(f"{object_id}.target must be prd_brief or prd")
            else:
                render_blocks_by_target.setdefault(target, []).append(object_id)
            for key in ("section", "content_type", "allowed_inference"):
                if not payload.get(key):
                    errors.append(f"{object_id} missing {key}")
            for key in ("contract_refs", "source_refs", "unsupported_claims"):
                if key not in payload or not isinstance(payload.get(key), list):
                    errors.append(f"{object_id}.{key} must be a list")
            if not as_list(payload.get("contract_refs")):
                errors.append(f"{object_id} requires non-empty contract_refs")
            if not as_list(payload.get("source_refs")):
                errors.append(f"{object_id} requires non-empty source_refs")
            errors.extend(validate_ref_list_types(contract, payload.get("contract_refs"), f"{object_id}.contract_refs", CONTRACT_REF_TYPES, require_non_empty=True))
            errors.extend(validate_ref_list_types(contract, payload.get("source_refs"), f"{object_id}.source_refs", {"SRC"}, require_non_empty=True))
            if payload.get("status") not in {"ready", "blocked"}:
                errors.append(f"{object_id}.status must be ready or blocked")
            if payload.get("status") == "ready" and as_list(payload.get("unsupported_claims")):
                errors.append(f"{object_id} is ready but has unsupported_claims")

    for target in ("prd_brief", "prd"):
        if render_status.get(target) != "not_requested" and not render_blocks_by_target.get(target):
            errors.append(f"render_status.{target} is requested but has no RB coverage")
        if target_is_ready(render_status, target):
            for rb_id in render_blocks_by_target.get(target, []):
                if payload_for(contract, rb_id).get("status") != "ready":
                    errors.append(f"render_status.{target} is ready but {rb_id} is not ready")

    if render_status.get("prd") == "review_ready":
        agent_execution = contract.get("agent_execution")
        if not isinstance(agent_execution, dict):
            errors.append("review-ready PRD requires agent_execution object")
            agent_execution = {}
        for field_name, required_type in execution_field_types().items():
            refs = agent_execution.get(field_name)
            if not isinstance(refs, list) or not refs:
                errors.append(f"review-ready PRD requires non-empty agent_execution.{field_name}")
            elif any(((objects.get(ref) or {}).get("type") != required_type) for ref in refs):
                errors.append(f"agent_execution.{field_name} must reference only {required_type} objects")
            if not object_type_ids(contract, required_type):
                errors.append(f"review-ready PRD requires at least one {required_type} object")
        for req_id in current_req_ids(contract):
            req = objects.get(req_id, {})
            payload = req.get("payload", {}) if isinstance(req, dict) else {}
            if not as_list(payload.get("acceptance_criteria")):
                errors.append(f"{req_id} missing acceptance_criteria for review-ready PRD")
            req_refs = collect_ids(payload)
            if not any(ref.startswith("VER-") for ref in req_refs):
                errors.append(f"{req_id} missing visible VER link for review-ready PRD")

    gate_report = contract.get("gate_report")
    if not isinstance(gate_report, list):
        errors.append("contract-envelope.json gate_report must be a list")
        gate_report = []
    for index, gate in enumerate(gate_report):
        if not isinstance(gate, dict):
            errors.append(f"gate_report[{index}] must be an object")
            continue
        errors.extend(validate_gate_record(contract, gate, f"gate_report[{index}]"))
    errors.extend(validate_gate_report_consistency(contract, gate_report))

    quality_gate_refs = set(as_list(contract.get("quality_gates")))
    gate_report_refs = {
        gate.get("gate_id")
        for gate in gate_report
        if isinstance(gate, dict) and isinstance(gate.get("gate_id"), str)
    }
    if quality_gate_refs != gate_report_refs:
        errors.append("contract-envelope.json quality_gates must match gate_report gate_id refs")

    contract_summary = contract.get("contract_summary")
    if not isinstance(contract_summary, dict):
        errors.append("contract-envelope.json contract_summary must be an object")
        contract_summary = {}
    ready_targets = set(as_list(contract_summary.get("ready_targets")))
    blocked_targets = set(as_list(contract_summary.get("blocked_targets")))
    expected_ready, expected_blocked = expected_summary_targets(contract)
    if ready_targets != expected_ready:
        errors.append(
            "contract_summary.ready_targets must match derived ready targets: "
            + ", ".join(sorted(expected_ready))
        )
    if blocked_targets != expected_blocked:
        errors.append(
            "contract_summary.blocked_targets must match derived blocked targets: "
            + ", ".join(sorted(expected_blocked))
        )

    errors.extend(validate_traceability_summary(contract))

    return errors



def validate_prd_files(root: Path, contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    brief = (root / "prd-brief.md").read_text(encoding="utf-8")
    prd = (root / "prd.md").read_text(encoding="utf-8")
    notes = (root / "intake-notes.md").read_text(encoding="utf-8")

    if len(brief.strip()) < 20:
        errors.append("prd-brief.md must be non-empty")
    if len(prd.strip()) < 20:
        errors.append("prd.md must be non-empty")
    if len(notes.strip()) < 20:
        errors.append("intake-notes.md must be non-empty")

    if "contract-envelope.json" not in brief and "合同" not in brief:
        errors.append("prd-brief.md should state its source contract")
    if "contract" not in prd.lower():
        errors.append("prd.md should state its source contract")

    render_status = contract.get("render_status") if isinstance(contract.get("render_status"), dict) else {}
    brief_status = render_status.get("prd_brief")
    prd_status = render_status.get("prd")
    if prd_status and prd_status != "not_requested" and prd_status not in prd.lower():
        errors.append(f"prd.md should state render_status.prd={prd_status}")

    known = set((contract.get("objects") or {}).keys())
    for filename, text_value in (("prd-brief.md", brief), ("prd.md", prd), ("intake-notes.md", notes)):
        dangling = sorted(ref for ref in collect_ids(text_value) if ref not in known and not ref.startswith(("TASK-", "PG-", "CHECK-")))
        if dangling:
            errors.append(f"{filename} has dangling refs: " + ", ".join(dangling))

    brief_sections = [
        "修订记录",
        "产品目标",
        "建设范围",
        "实现方案",
        "验收标准与方法",
        "路线图",
        "风险与开放问题",
        "参考文献",
    ]
    brief_evidence_sections = [
        "产品目标",
        "建设范围",
        "实现方案",
        "验收标准与方法",
        "路线图",
        "风险与开放问题",
    ]
    agent_only_sections = [
        "Source of Truth",
        "Reader and Mission",
        "Requirement Trace",
        "Execution Contract",
        "Tool and Integration Boundaries",
        "Permissions and Safety",
        "Stop Conditions",
        "Done Criteria",
    ]
    if brief_status in {"draft", "review_ready", "blocked"}:
        if len(brief) > 8000:
            errors.append("prd-brief.md must stay concise for human review")
        process_markers = ["Source contract:", "Render status:", "render_status", "stage_2", "Stage 2"]
        for marker in process_markers:
            if marker in brief:
                errors.append(f"prd-brief.md must not include process marker: {marker}")
        for section in agent_only_sections:
            if f"## {section}" in brief:
                errors.append(f"prd-brief.md must not include agent-only section: {section}")
    if brief_status == "review_ready":
        headings = markdown_h2_headings(brief)
        for section in brief_sections:
            if not has_markdown_heading(brief, section):
                errors.append(f"review-ready prd-brief.md missing brief section: {section}")
        if headings and headings[0] != "修订记录":
            errors.append("review-ready prd-brief.md must put revision table first")
        if headings and headings[-1] != "参考文献":
            errors.append("review-ready prd-brief.md must put references at the end")
        revision = markdown_section(brief, "修订记录")
        for column in ("版本", "日期", "修订说明", "修订人"):
            if column not in revision:
                errors.append(f"review-ready prd-brief.md revision table missing column: {column}")
        if "|" not in brief:
            errors.append("review-ready prd-brief.md must use at least one table")
        for section in brief_evidence_sections:
            body = markdown_section(brief, section)
            if not collect_ids(body):
                errors.append(f"review-ready prd-brief.md section lacks source refs: {section}")
            if len(body) < 80:
                errors.append(f"review-ready prd-brief.md section is too thin: {section}")
        references = markdown_section(brief, "参考文献")
        if "contract-envelope.json" not in references:
            errors.append("review-ready prd-brief.md references must include contract-envelope.json")
        if "prd.md" not in references:
            errors.append("review-ready prd-brief.md references must include prd.md")
        if not collect_ids(references):
            errors.append("review-ready prd-brief.md references must include canonical refs")

    prd_sections = [
        "Document Metadata",
        "Executive Summary",
        "Problem and Background",
        "Target Users and Personas",
        "Goals and Outcomes",
        "Success Metrics",
        "Scope and Non-Goals",
        "User Stories and Use Cases",
        "Functional Requirements",
        "Non-Functional Requirements and Guardrails",
        "Implementation Approach",
        "Acceptance Criteria",
        "Release Plan and Roadmap",
        "Risks, Assumptions, and Dependencies",
        "Open Questions",
        "Traceability",
    ]
    if render_status.get("prd") == "review_ready":
        for section in prd_sections:
            if not has_markdown_heading(prd, section):
                errors.append(f"review-ready prd.md missing PRD section: {section}")
            else:
                body = markdown_section(prd, section)
                min_length = 20 if section == "Open Questions" else 40
                if len(body) < min_length:
                    errors.append(f"review-ready prd.md PRD section is too thin: {section}")

        required_prd_refs = expected_ready_plan_refs(contract, contract_current_phase_ref(contract))
        missing_refs = sorted(ref for ref in required_prd_refs if ref not in collect_ids(prd))
        if missing_refs:
            errors.append("review-ready prd.md missing current execution refs: " + ", ".join(missing_refs))

    return errors

def validate_hld_structured_list_field(contract: dict[str, Any], hld: dict[str, Any], field_name: str, status: str) -> list[str]:
    errors: list[str] = []
    spec = HLD_STRUCTURED_LIST_FIELDS[field_name]
    value = hld.get(field_name)
    if status == "ready" and (not isinstance(value, list) or not value):
        return [f"ready HLD requires non-empty {field_name}"]
    if value is None:
        return errors
    if not isinstance(value, list):
        return [f"high_level_design.{field_name} must be a list"]
    for index, item in enumerate(value):
        item_name = f"high_level_design.{field_name}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_name} must be an object")
            continue
        for text_field in spec["text"]:
            text_value = item.get(text_field)
            if not non_empty_text(text_value):
                errors.append(f"{item_name}.{text_field} must be a non-empty string")
            elif field_name == "environment_requirements":
                lowered = text_value.lower()
                deferred = sorted(term for term in HLD_DEFERRED_ACCEPTANCE_TERMS if term in lowered)
                if deferred:
                    errors.append(f"{item_name}.{text_field} must name concrete confirmed resources, not deferred placeholders: " + ", ".join(deferred))
            elif field_name == "interface_contracts":
                lowered = text_value.lower()
                loose_terms = sorted(term for term in HLD_LOOSE_INTERFACE_TERMS if term in lowered)
                if loose_terms:
                    errors.append(f"{item_name}.{text_field} must be precise and must not use loose interface terms: " + ", ".join(loose_terms))
        for list_field in spec["lists"]:
            list_value = item.get(list_field)
            if not isinstance(list_value, list) or not list_value:
                errors.append(f"{item_name}.{list_field} must be a non-empty list")
                continue
            if field_name == "data_objects" and list_field == "fields":
                for field_index, field_item in enumerate(list_value):
                    field_item_name = f"{item_name}.fields[{field_index}]"
                    if not isinstance(field_item, dict):
                        errors.append(f"{field_item_name} must be an object")
                        continue
                    if not non_empty_text(field_item.get("name")):
                        errors.append(f"{field_item_name}.name must be a non-empty string")
                    if not isinstance(field_item.get("required"), bool):
                        errors.append(f"{field_item_name}.required must be boolean")
                    if not non_empty_text(field_item.get("meaning")):
                        errors.append(f"{field_item_name}.meaning must be a non-empty string")
                continue
            if field_name == "interface_contracts" and list_field == "source_refs":
                errors.extend(validate_ref_list_types(
                    contract,
                    list_value,
                    f"{item_name}.{list_field}",
                    {"SRC"},
                    require_non_empty=True,
                ))
                continue
            if list_field.endswith("_refs") or list_field == "contract_refs":
                errors.extend(validate_ref_list_types(
                    contract,
                    list_value,
                    f"{item_name}.{list_field}",
                    CONTRACT_REF_TYPES,
                    require_non_empty=True,
                ))
    return errors


def validate_hld_real_acceptance_plan(contract: dict[str, Any], hld: dict[str, Any], status: str) -> list[str]:
    errors: list[str] = []
    plan = hld.get("real_acceptance_plan")
    if status == "ready" and not isinstance(plan, dict):
        return ["ready HLD requires real_acceptance_plan object"]
    if plan is None:
        return errors
    if not isinstance(plan, dict):
        return ["high_level_design.real_acceptance_plan must be an object"]

    for field_name in HLD_REAL_ACCEPTANCE_TEXT_FIELDS:
        if not non_empty_text(plan.get(field_name)):
            errors.append(f"real_acceptance_plan.{field_name} must be a non-empty string")
    for field_name in HLD_REAL_ACCEPTANCE_LIST_FIELDS:
        value = plan.get(field_name)
        if not isinstance(value, list) or not value:
            errors.append(f"real_acceptance_plan.{field_name} must be a non-empty list")
            continue
        if field_name == "contract_refs":
            errors.extend(validate_ref_list_types(
                contract,
                value,
                "real_acceptance_plan.contract_refs",
                CONTRACT_REF_TYPES,
                require_non_empty=True,
            ))
    for field_name in HLD_REAL_ACCEPTANCE_SOURCE_REF_FIELDS:
        value = plan.get(field_name)
        errors.extend(validate_ref_list_types(
            contract,
            value,
            f"real_acceptance_plan.{field_name}",
            {"SRC"},
            require_non_empty=True,
        ))
    if plan.get("mock_policy") != "forbidden":
        errors.append("real_acceptance_plan.mock_policy must be forbidden")

    acceptance_text = "\n".join(collect_text_excluding_keys(plan, {"mock_policy"})).lower()
    forbidden = sorted(term for term in HLD_FORBIDDEN_ACCEPTANCE_TERMS if term in acceptance_text)
    if forbidden:
        errors.append("real_acceptance_plan must not use mock/stub/fake/simulated/synthetic acceptance substitutes: " + ", ".join(forbidden))
    deferred = sorted(term for term in HLD_DEFERRED_ACCEPTANCE_TERMS if term in acceptance_text)
    if deferred:
        errors.append("real_acceptance_plan must name concrete confirmed resources, not deferred placeholders: " + ", ".join(deferred))
    return errors


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_prd_review_approval_artifact_binding(root: Path, contract: dict[str, Any]) -> list[str]:
    workflow = contract.get("harness_workflow") if isinstance(contract.get("harness_workflow"), dict) else {}
    approvals = workflow.get("approval_gates") if isinstance(workflow.get("approval_gates"), dict) else {}
    human_review = approvals.get("prd_review") if isinstance(approvals.get("prd_review"), dict) else {}
    if human_review.get("status") != "approved":
        return []

    approved_by = human_review.get("approved_by_ref")
    payload = payload_for(contract, approved_by) if isinstance(approved_by, str) else {}
    artifacts = payload.get("approved_artifacts")
    if not isinstance(artifacts, list):
        return []

    errors: list[str] = []
    for expected_name in ("prd.md", "prd-brief.md"):
        expected_path = root / expected_name
        if not expected_path.exists():
            errors.append(f"PRD review approval artifact binding cannot be checked because {expected_name} is missing")
            continue
        expected_hash = file_sha256(expected_path)
        matched = False
        for item in artifacts:
            if not isinstance(item, dict) or item.get("path") != expected_name:
                continue
            matched = True
            sha256 = item.get("sha256")
            if not isinstance(sha256, str) or not re.fullmatch(r"[0-9a-f]{64}", sha256):
                errors.append(f"PRD review approval approved_artifacts {expected_name} must include a lowercase sha256 digest")
            elif sha256 != expected_hash:
                errors.append(f"PRD review approval sha256 does not match current {expected_name}")
        if not matched:
            errors.append(f"PRD review approval approved_artifacts must bind {expected_name}")
    return errors


def validate_high_level_design(hld: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(hld, dict):
        return ["high-level-design.json must be an object"]

    forbidden_task_fields = {
        "task_graph",
        "tasks",
        "task_cards",
        "implementation_tasks",
        "work_items",
        "dependency_edges",
        "parallel_groups",
        "stage_goal_coverage",
        "planning_gate_report",
    }
    for key in sorted(forbidden_task_fields):
        if key in hld:
            errors.append(f"high-level-design.json must not contain task planning field {key}")

    required = [
        "hld_id",
        "source_artifacts",
        "design_status",
        "blocking_reasons",
        "missing_required_refs",
        "required_fixes",
        "contract_refs",
        "architecture_summary",
        "component_boundaries",
        "data_and_state_design",
        "integration_points",
        "verification_strategy",
        "risk_controls",
        "control_flow_design",
        "data_flow_design",
        "data_objects",
        "interface_contracts",
        "state_model",
        "technical_decisions",
        "implementation_design",
        "environment_requirements",
        "real_acceptance_plan",
        "design_gate_report",
    ]
    for key in required:
        if key not in hld:
            errors.append(f"high-level-design.json missing {key}")

    for key in ("blocking_reasons", "missing_required_refs", "required_fixes", "contract_refs", "design_gate_report"):
        if key in hld and not isinstance(hld.get(key), list):
            errors.append(f"high-level-design.json {key} must be a list")

    if not isinstance(hld.get("hld_id"), str) or not hld.get("hld_id", "").startswith("HLD-"):
        errors.append("high-level-design.json hld_id must start with HLD-")

    status = hld.get("design_status")
    if status not in HLD_STATUS:
        errors.append("high_level_design.design_status has invalid status")

    source = hld.get("source_artifacts", {})
    if not isinstance(source, dict):
        errors.append("high-level-design.json source_artifacts must be an object")
        source = {}
    render_status = contract.get("render_status") if isinstance(contract.get("render_status"), dict) else {}
    if source.get("contract_ref") != "contract-envelope.json":
        errors.append("HLD source_artifacts.contract_ref must be contract-envelope.json")
    if source.get("contract_version") != contract.get("contract_version"):
        errors.append("HLD source_artifacts.contract_version must match contract_version")
    if source.get("prd_ref") != "prd.md":
        errors.append("HLD source_artifacts.prd_ref must be prd.md")
    if source.get("prd_status") != render_status.get("prd"):
        errors.append("HLD source_artifacts.prd_status must match contract render_status.prd")
    if source.get("prd_brief_ref") != "prd-brief.md":
        errors.append("HLD source_artifacts.prd_brief_ref must be prd-brief.md")
    if source.get("prd_brief_status") != render_status.get("prd_brief"):
        errors.append("HLD source_artifacts.prd_brief_status must match contract render_status.prd_brief")
    if source.get("phase_ref_kind") == "canonical_id":
        phase_ref = source.get("phase_ref")
        if object_type(contract, phase_ref) != "PHASE":
            errors.append("HLD source_artifacts.phase_ref must reference a PHASE object")
    elif source.get("phase_ref_kind"):
        errors.append("HLD source_artifacts.phase_ref_kind must be canonical_id when provided")

    errors.extend(validate_ref_list_types(
        contract,
        hld.get("contract_refs"),
        "high_level_design.contract_refs",
        CONTRACT_REF_TYPES,
        require_non_empty=status == "ready",
    ))

    workflow = contract.get("harness_workflow") if isinstance(contract.get("harness_workflow"), dict) else {}
    approvals = workflow.get("approval_gates") if isinstance(workflow.get("approval_gates"), dict) else {}
    human_review = approvals.get("prd_review") if isinstance(approvals.get("prd_review"), dict) else {}
    if status == "ready":
        if render_status.get("prd") != "review_ready":
            errors.append("ready HLD requires contract render_status.prd=review_ready")
        if source.get("prd_status") != "review_ready":
            errors.append("ready HLD requires source_artifacts.prd_status=review_ready")
        if render_status.get("prd_brief") != "review_ready":
            errors.append("ready HLD requires contract render_status.prd_brief=review_ready")
        if source.get("prd_brief_status") != "review_ready":
            errors.append("ready HLD requires source_artifacts.prd_brief_status=review_ready")
        if human_review.get("status") != "approved":
            errors.append("ready HLD requires approved prd_review gate")
        elif payload_for(contract, human_review.get("approved_by_ref")).get("source_type") != "user_confirmation":
            errors.append("ready HLD prd_review approval must reference user_confirmation SRC")
        for key in ("blocking_reasons", "missing_required_refs", "required_fixes"):
            if as_list(hld.get(key)):
                errors.append(f"ready HLD must have empty {key}")
        required_hld_refs = expected_ready_plan_refs(contract, source.get("phase_ref") if source.get("phase_ref_kind") == "canonical_id" else contract_current_phase_ref(contract))
        missing_hld_refs = sorted(ref for ref in required_hld_refs if ref not in collect_ids(hld))
        if missing_hld_refs:
            errors.append("ready HLD missing current design refs: " + ", ".join(missing_hld_refs))
    elif status == "blocked":
        if not any(as_list(hld.get(key)) for key in ("blocking_reasons", "missing_required_refs", "required_fixes")):
            errors.append("blocked HLD needs blocking_reasons, missing_required_refs, or required_fixes")

    for field_name in (
        "architecture_summary",
        "component_boundaries",
        "data_and_state_design",
        "integration_points",
        "verification_strategy",
        "risk_controls",
    ):
        value = hld.get(field_name)
        if status == "ready" and (not isinstance(value, str) or not value.strip()):
            errors.append(f"high_level_design.{field_name} must be a non-empty string when ready")

    for field_name in HLD_STRUCTURED_LIST_FIELDS:
        errors.extend(validate_hld_structured_list_field(contract, hld, field_name, status))
    errors.extend(validate_hld_real_acceptance_plan(contract, hld, status))

    check_ids = set()
    design_gate_keys: dict[str, str] = {}
    for index, gate in enumerate(as_list(hld.get("design_gate_report"))):
        if not isinstance(gate, dict):
            errors.append(f"design_gate_report[{index}] must be an object")
            continue
        check_id = gate.get("check_id")
        if not isinstance(check_id, str) or not CHECK_ID_RE.fullmatch(check_id):
            errors.append(f"design gate check_id must match CHECK-###: {check_id}")
        else:
            check_ids.add(check_id)
        if gate.get("status") not in PLANNING_GATE_STATUS:
            errors.append(f"design gate {check_id} has invalid status")
        if gate.get("status") == "warning" and (not gate.get("message") or not gate.get("required_fix")):
            errors.append(f"design gate {check_id}.warning requires non-empty message and required_fix")
        if gate.get("status") == "blocked" and not gate.get("required_fix"):
            errors.append(f"design gate {check_id}.blocked requires non-empty required_fix")
        if not non_empty_text(gate.get("evidence_summary")):
            errors.append(f"design gate {check_id} requires non-empty evidence_summary")
        if not as_list(gate.get("evidence_refs")):
            errors.append(f"design gate {check_id} requires non-empty evidence_refs")
        errors.extend(validate_ref_list_types(
            contract,
            gate.get("evidence_refs"),
            f"design gate {check_id}.evidence_refs",
            CONTRACT_REF_TYPES,
            require_non_empty=True,
        ))
        gate_key = gate.get("gate_key")
        if status == "ready":
            if not non_empty_text(gate_key):
                errors.append(f"ready HLD design gate {check_id} requires gate_key")
            elif gate_key not in HLD_REQUIRED_READY_DESIGN_GATE_KEYS:
                errors.append(f"ready HLD design gate {check_id} has unknown gate_key: {gate_key}")
            elif gate_key in design_gate_keys:
                errors.append(f"ready HLD has duplicate design gate key: {gate_key}")
            else:
                design_gate_keys[gate_key] = str(check_id)
                if gate.get("status") != "pass":
                    errors.append(f"ready HLD required design gate {gate_key} must be pass")
        if gate.get("status") == "blocked" and status == "ready":
            errors.append(f"ready HLD cannot have blocked design gate {check_id}")

    if status == "ready":
        missing_gate_keys = sorted(set(HLD_REQUIRED_READY_DESIGN_GATE_KEYS) - set(design_gate_keys))
        if missing_gate_keys:
            errors.append("ready HLD missing required design gate keys: " + ", ".join(missing_gate_keys))

    known = set((contract.get("objects") or {}).keys()) | check_ids
    dangling = sorted(ref for ref in collect_ids(hld) if ref not in known)
    if dangling:
        errors.append("high-level-design.json has dangling refs: " + ", ".join(dangling))

    return errors


def validate_hld_markdown(root: Path, contract: dict[str, Any], hld: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    path = root / "high-level-design.md"
    text = path.read_text(encoding="utf-8")
    if len(text.strip()) < 200:
        return ["high-level-design.md must be a non-empty HLD document"]

    status = hld.get("design_status")
    known = set((contract.get("objects") or {}).keys()) | {
        gate.get("check_id")
        for gate in as_list(hld.get("design_gate_report"))
        if isinstance(gate, dict) and isinstance(gate.get("check_id"), str)
    }
    dangling = sorted(ref for ref in collect_ids(text) if ref not in known and not ref.startswith(("TASK-", "PG-")))
    if dangling:
        errors.append("high-level-design.md has dangling refs: " + ", ".join(dangling))

    if "high-level-design.json" not in text and "contract-envelope.json" not in text:
        errors.append("high-level-design.md must identify its source contract or structured HLD source")

    if status == "ready":
        for section in HLD_MARKDOWN_REQUIRED_SECTIONS:
            if not has_markdown_heading(text, section):
                errors.append(f"ready high-level-design.md missing section: {section}")
            elif len(markdown_section(text, section)) < 40:
                errors.append(f"ready high-level-design.md section is too thin: {section}")
        if "```mermaid" not in text:
            errors.append("ready high-level-design.md must include at least one mermaid diagram")
        if "|" not in text:
            errors.append("ready high-level-design.md must include tables for structured design details")
        required_refs = expected_ready_plan_refs(
            contract,
            hld.get("source_artifacts", {}).get("phase_ref")
            if isinstance(hld.get("source_artifacts"), dict)
            and hld.get("source_artifacts", {}).get("phase_ref_kind") == "canonical_id"
            else contract_current_phase_ref(contract),
        )
        missing_refs = sorted(ref for ref in required_refs if ref not in collect_ids(text))
        if missing_refs:
            errors.append("ready high-level-design.md missing current design refs: " + ", ".join(missing_refs))
        for keyword in ("Control Flow", "Data Flow", "Data Objects", "Interface Contracts", "Real Acceptance Plan"):
            if keyword not in text:
                errors.append(f"ready high-level-design.md must cover {keyword}")
        for marker in HLD_MARKDOWN_REQUIRED_READY_MARKERS:
            if marker not in text:
                errors.append(f"ready high-level-design.md missing implementation-ready marker: {marker}")
        plan = hld.get("real_acceptance_plan") if isinstance(hld.get("real_acceptance_plan"), dict) else {}
        acceptance_command = plan.get("acceptance_command")
        if isinstance(acceptance_command, str) and acceptance_command.strip() and acceptance_command not in text:
            errors.append("ready high-level-design.md must include real_acceptance_plan.acceptance_command")
        for artifact_path in as_list(plan.get("expected_artifact_paths")):
            if isinstance(artifact_path, str) and artifact_path.strip() and artifact_path not in text:
                errors.append(f"ready high-level-design.md missing expected artifact path: {artifact_path}")
        for index, interface in enumerate(as_list(hld.get("interface_contracts"))):
            if not isinstance(interface, dict):
                continue
            for source_ref in as_list(interface.get("source_refs")):
                if isinstance(source_ref, str) and source_ref not in collect_ids(text):
                    errors.append(f"ready high-level-design.md missing interface source ref from interface_contracts[{index}]: {source_ref}")

    return errors


def validate_hld_semantic_review(review: dict[str, Any], contract: dict[str, Any], hld: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(review, dict):
        return ["hld-semantic-review.json must be an object"]

    status = hld.get("design_status")
    required_fields = ("review_id", "review_status", "source_artifacts", "dimensions", "overall_findings")
    for field_name in required_fields:
        if field_name not in review:
            errors.append(f"hld-semantic-review.json missing {field_name}")

    review_status = review.get("review_status")
    if review_status not in HLD_SEMANTIC_REVIEW_STATUS:
        errors.append("hld-semantic-review.json review_status must be pass, warning, or blocked")
    if status == "ready" and review_status != "pass":
        errors.append("ready HLD requires hld-semantic-review.review_status=pass")

    source = review.get("source_artifacts") if isinstance(review.get("source_artifacts"), dict) else {}
    if source.get("contract_ref") != "contract-envelope.json":
        errors.append("hld-semantic-review source_artifacts.contract_ref must be contract-envelope.json")
    if source.get("hld_json_ref") != "high-level-design.json":
        errors.append("hld-semantic-review source_artifacts.hld_json_ref must be high-level-design.json")
    if source.get("hld_markdown_ref") != "high-level-design.md":
        errors.append("hld-semantic-review source_artifacts.hld_markdown_ref must be high-level-design.md")

    seen_keys: set[str] = set()
    for index, dimension in enumerate(as_list(review.get("dimensions"))):
        item_name = f"hld-semantic-review.dimensions[{index}]"
        if not isinstance(dimension, dict):
            errors.append(f"{item_name} must be an object")
            continue
        key = dimension.get("dimension_key")
        if not isinstance(key, str) or not key:
            errors.append(f"{item_name}.dimension_key must be a non-empty string")
            continue
        seen_keys.add(key)
        if key not in HLD_SEMANTIC_REVIEW_REQUIRED_KEYS:
            errors.append(f"{item_name}.dimension_key is not recognized: {key}")
        dim_status = dimension.get("status")
        if dim_status not in HLD_SEMANTIC_REVIEW_STATUS:
            errors.append(f"{item_name}.status must be pass, warning, or blocked")
        if status == "ready" and dim_status != "pass":
            errors.append(f"ready HLD semantic review dimension {key} must be pass")
        if not non_empty_text(dimension.get("finding")):
            errors.append(f"{item_name}.finding must be a non-empty string")
        if dim_status in {"warning", "blocked"} and not non_empty_text(dimension.get("required_fix")):
            errors.append(f"{item_name}.{dim_status} requires required_fix")
        if dim_status == "pass" and dimension.get("required_fix"):
            errors.append(f"{item_name}.required_fix must be empty when status=pass")
        errors.extend(validate_ref_list_types(
            contract,
            dimension.get("contract_refs"),
            f"{item_name}.contract_refs",
            CONTRACT_REF_TYPES,
            require_non_empty=True,
        ))
        source_refs = dimension.get("source_refs")
        if key in {"source_traceability", "interface_precision", "executable_acceptance", "markdown_parity"}:
            errors.extend(validate_ref_list_types(
                contract,
                source_refs,
                f"{item_name}.source_refs",
                {"SRC"},
                require_non_empty=True,
            ))
        elif source_refs is not None:
            errors.extend(validate_ref_list_types(
                contract,
                source_refs,
                f"{item_name}.source_refs",
                {"SRC"},
            ))

    missing_keys = sorted(set(HLD_SEMANTIC_REVIEW_REQUIRED_KEYS) - seen_keys)
    if status == "ready" and missing_keys:
        errors.append("ready HLD semantic review missing dimensions: " + ", ".join(missing_keys))
    if status == "ready" and not non_empty_text(review.get("overall_findings")):
        errors.append("ready HLD semantic review requires overall_findings")
    return errors


def parse_cli(argv: list[str]) -> tuple[Path, str] | None:
    if len(argv) not in {2, 4}:
        return None
    root = Path(argv[1])
    stage = "final"
    if len(argv) == 4:
        if argv[2] != "--stage" or argv[3] not in {"stage1", "stage2", "final"}:
            return None
        stage = argv[3]
    return root, stage


def validate_stage1_package(root: Path) -> list[str]:
    errors: list[str] = []
    if not (root / "contract-envelope.json").exists():
        return ["missing contract-envelope.json"]
    for filename in ("prd-brief.md", "prd.md", "human-prd.md", "agent-prd.md", "high-level-design.json", "high-level-design.md", "hld-semantic-review.json", "execution-task-plan.json"):
        if (root / filename).exists():
            errors.append(f"Stage 1 package must not contain downstream artifact {filename}")
    if errors:
        return errors
    contract = load_json(root / "contract-envelope.json")
    errors.extend(validate_contract(contract))
    return errors


def validate_stage2_package(root: Path) -> list[str]:
    errors: list[str] = []
    required_files = [
        "contract-envelope.json",
        "intake-notes.md",
    ]
    for filename in required_files:
        if not (root / filename).exists():
            errors.append(f"missing {filename}")
    for filename in ("human-prd.md", "agent-prd.md", "high-level-design.json", "high-level-design.md", "hld-semantic-review.json", "execution-task-plan.json"):
        if (root / filename).exists():
            errors.append(f"Stage 2 package must not contain downstream artifact {filename}")

    if errors:
        return errors

    contract = load_json(root / "contract-envelope.json")
    render_status = contract.get("render_status") if isinstance(contract.get("render_status"), dict) else {}
    prd_writer = writer_invocation(contract, "prd")
    prd_writer_status = prd_writer.get("status")
    stage2_blocked_by_writer = prd_writer_status in {"blocked", "unavailable", "failed"} or render_status.get("prd") == "blocked" or render_status.get("prd_brief") == "blocked"

    if not stage2_blocked_by_writer:
        for filename in ("prd.md", "prd-brief.md"):
            if not (root / filename).exists():
                errors.append(f"missing {filename}")
    elif not non_empty_text(prd_writer.get("required_fix")):
        errors.append("blocked Stage 2 writer invocation must include required_fix")

    if errors:
        return errors

    errors.extend(validate_contract(contract))
    errors.extend(validate_writer_invocation(
        contract,
        "prd",
        PRD_WRITER_SKILLS,
        ("prd.md",),
        require_completed=not stage2_blocked_by_writer,
    ))
    if not stage2_blocked_by_writer:
        errors.extend(validate_prd_files(root, contract))
    errors.extend(validate_prd_review_approval_artifact_binding(root, contract))

    if stage2_blocked_by_writer:
        if render_status.get("prd") != "blocked" or render_status.get("prd_brief") != "blocked":
            errors.append("blocked Stage 2 requires render_status.prd and render_status.prd_brief to be blocked")
    elif render_status.get("prd_brief") != "review_ready":
        errors.append("Stage 2 requires render_status.prd_brief=review_ready")
    if not stage2_blocked_by_writer and render_status.get("prd") != "review_ready":
        errors.append("Stage 2 requires render_status.prd=review_ready")

    workflow = contract.get("harness_workflow") if isinstance(contract.get("harness_workflow"), dict) else {}
    if workflow.get("current_stage") != "stage_2_prd_review":
        errors.append("Stage 2 package requires harness_workflow.current_stage=stage_2_prd_review")
    approvals = workflow.get("approval_gates") if isinstance(workflow.get("approval_gates"), dict) else {}
    human_review = approvals.get("prd_review") if isinstance(approvals.get("prd_review"), dict) else {}
    if stage2_blocked_by_writer:
        if human_review.get("status") not in {"failed", "revise", "not_started"}:
            errors.append("blocked Stage 2 requires prd_review.status=failed, revise, or not_started")
    elif human_review.get("status") not in {"pending", "approved"}:
        errors.append("Stage 2 package requires prd_review.status=pending or approved")
    if human_review.get("status") == "pending" and human_review.get("approved_by_ref"):
        errors.append("Stage 2 pending prd_review must not have approved_by_ref")

    summary = contract.get("contract_summary") if isinstance(contract.get("contract_summary"), dict) else {}
    stage_ready = set(as_list(summary.get("stage_ready")))
    stage_blocked = set(as_list(summary.get("stage_blocked")))
    required_ready = {"stage_1_requirements_table", "stage_2_prd_review"}
    missing_ready = sorted(required_ready - stage_ready)
    if stage2_blocked_by_writer:
        if "stage_2_prd_review" in stage_ready:
            errors.append("blocked Stage 2 must not mark stage_2_prd_review ready")
        if "stage_2_prd_review" not in stage_blocked:
            errors.append("blocked Stage 2 requires contract_summary.stage_blocked include stage_2_prd_review")
    elif missing_ready:
        errors.append("Stage 2 contract_summary.stage_ready missing: " + ", ".join(missing_ready))
    if "stage_3_hld" in stage_ready:
        errors.append("Stage 2 contract_summary.stage_ready must not include stage_3_hld")
    if human_review.get("status") == "pending" and "stage_3_hld" not in stage_blocked:
        errors.append("Stage 2 pending review requires contract_summary.stage_blocked include stage_3_hld")
    completed = workflow.get("completed_stages")
    if isinstance(completed, list) and "stage_1_requirements_table" not in completed:
        errors.append("Stage 2 completed_stages must include stage_1_requirements_table when present")

    return errors


def validate_final_package(root: Path) -> list[str]:
    errors: list[str] = []
    required_files = [
        "contract-envelope.json",
        "prd-brief.md",
        "prd.md",
        "intake-notes.md",
    ]
    for filename in required_files:
        if not (root / filename).exists():
            errors.append(f"missing {filename}")
    if (root / "execution-task-plan.json").exists():
        errors.append("execution-task-plan.json is no longer a spec-intake output; produce high-level-design.json and high-level-design.md only")
    for filename in ("human-prd.md", "agent-prd.md"):
        if (root / filename).exists():
            errors.append(f"{filename} is a legacy spec-intake artifact and must not be present")

    if errors:
        return errors

    contract = load_json(root / "contract-envelope.json")
    hld_writer = writer_invocation(contract, "hld")
    hld_writer_status = hld_writer.get("status")
    final_blocked_by_writer = hld_writer_status in {"blocked", "unavailable", "failed"}
    if not final_blocked_by_writer:
        for filename in ("high-level-design.json", "high-level-design.md", "hld-semantic-review.json"):
            if not (root / filename).exists():
                errors.append(f"missing {filename}")
    elif not non_empty_text(hld_writer.get("required_fix")):
        errors.append("blocked final HLD writer invocation must include required_fix")
    if errors:
        return errors

    errors.extend(validate_contract(contract))
    errors.extend(validate_writer_invocation(
        contract,
        "prd",
        PRD_WRITER_SKILLS,
        ("prd.md",),
        require_completed=True,
    ))
    errors.extend(validate_writer_invocation(
        contract,
        "hld",
        HLD_WRITER_SKILLS,
        ("high-level-design.json", "high-level-design.md", "hld-semantic-review.json"),
        require_completed=not final_blocked_by_writer,
    ))
    errors.extend(validate_prd_files(root, contract))
    errors.extend(validate_prd_review_approval_artifact_binding(root, contract))
    if final_blocked_by_writer:
        return errors
    hld = load_json(root / "high-level-design.json")
    semantic_review = load_json(root / "hld-semantic-review.json")
    errors.extend(validate_high_level_design(hld, contract))
    errors.extend(validate_hld_markdown(root, contract, hld))
    errors.extend(validate_hld_semantic_review(semantic_review, contract, hld))
    return errors


def main(argv: list[str]) -> int:
    parsed = parse_cli(argv)
    if parsed is None:
        print("Usage: validate_spec_intake_package.py <output-dir> [--stage stage1|stage2|final]", file=sys.stderr)
        return 2

    root, stage = parsed
    if stage == "stage1":
        errors = validate_stage1_package(root)
    elif stage == "stage2":
        errors = validate_stage2_package(root)
    else:
        errors = validate_final_package(root)

    ok = not errors
    print(json.dumps({"ok": ok, "stage": stage, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
