#!/usr/bin/env python3
"""Validate a spec-intake output package.

The validator is intentionally structural and semantic-light: it checks required
artifact shape, canonical reference integrity, readiness invariants, and task
planning gates. It does not judge product usefulness or writing quality.
"""

from __future__ import annotations

import json
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
PLAN_ID_PREFIXES = (
    "TASK",
    "PG",
    "CHECK",
)
ID_PREFIXES = CONTRACT_ID_PREFIXES + PLAN_ID_PREFIXES
ID_RE = re.compile(r"\b((?:" + "|".join(ID_PREFIXES) + r")-\d{3})\b")
CONTRACT_ID_RE = re.compile(r"^(?:" + "|".join(CONTRACT_ID_PREFIXES) + r")-\d{3}$")
TASK_ID_RE = re.compile(r"^TASK-\d{3}$")
GROUP_ID_RE = re.compile(r"^PG-\d{3}$")
CHECK_ID_RE = re.compile(r"^CHECK-\d{3}$")
TASK_STATUS = {"planned", "ready", "blocked", "deferred", "in_progress", "done", "skipped"}
TASK_TYPES = {"foundation", "implementation", "integration", "verification", "documentation", "release", "cleanup"}
READY_TASK_STATUS = {"planned", "ready"}
PARALLEL_GROUP_STATUS = {"serial", "parallel_safe", "blocked"}
PLANNING_GATE_STATUS = {"pass", "warning", "blocked"}
COVERAGE_STATUS = {"covered", "partial", "blocked"}
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
    if target == "agent_prd":
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
    for target in ("human_prd", "agent_prd"):
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
            if target not in {"human_prd", "agent_prd", "task_plan"}:
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


def validate_contract(contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "contract_version",
        "intake_id",
        "source_idea",
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

    allowed_human = {"not_requested", "draft", "review_ready", "blocked"}
    allowed_agent = {"not_requested", "draft", "execution_ready", "blocked"}
    if render_status.get("human_prd") not in allowed_human:
        errors.append("render_status.human_prd has invalid status")
    if render_status.get("agent_prd") not in allowed_agent:
        errors.append("render_status.agent_prd has invalid status")

    for target in ("human_prd", "agent_prd"):
        blockers = readiness_blockers(contract, target)
        if target_is_ready(render_status, target) and blockers:
            errors.append(f"render_status.{target} cannot be ready while blockers exist: " + ", ".join(sorted(blockers)))

    render_blocks_by_target: dict[str, list[str]] = {"human_prd": [], "agent_prd": []}
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
            if (payload.get("blocks_human_prd") is True or payload.get("blocks_agent_prd") is True) and "status" not in payload:
                errors.append(f"objects.{object_id}.payload.status is required when Q blocks a target")
            if payload.get("status") == "resolved" and not as_list(payload.get("resolution_refs")):
                errors.append(f"objects.{object_id}.payload.resolution_refs is required when Q is resolved")
            if "resolution_refs" in payload:
                errors.extend(validate_ref_list_types(contract, payload.get("resolution_refs"), f"objects.{object_id}.payload.resolution_refs", set(CONTRACT_ID_PREFIXES)))
        if object_kind == "ASM":
            if (payload.get("blocks_human_prd") is True or payload.get("blocks_agent_prd") is True) and "status" not in payload:
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
                    if target not in {"human_prd", "agent_prd", "task_plan"}:
                        errors.append(f"objects.{object_id}.payload.affected_targets has invalid target {target!r}")
            errors.extend(validate_ref_list_types(contract, payload.get("evidence_refs"), f"objects.{object_id}.payload.evidence_refs", set(CONTRACT_ID_PREFIXES)))
        if obj.get("type") == "RB":
            target = payload.get("target")
            if target not in {"human_prd", "agent_prd"}:
                errors.append(f"{object_id}.target must be human_prd or agent_prd")
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

    for target in ("human_prd", "agent_prd"):
        if render_status.get(target) != "not_requested" and not render_blocks_by_target.get(target):
            errors.append(f"render_status.{target} is requested but has no RB coverage")
        if target_is_ready(render_status, target):
            for rb_id in render_blocks_by_target.get(target, []):
                if payload_for(contract, rb_id).get("status") != "ready":
                    errors.append(f"render_status.{target} is ready but {rb_id} is not ready")

    if render_status.get("agent_prd") == "execution_ready":
        agent_execution = contract.get("agent_execution")
        if not isinstance(agent_execution, dict):
            errors.append("execution-ready Agent PRD requires agent_execution object")
            agent_execution = {}
        for field_name, required_type in execution_field_types().items():
            refs = agent_execution.get(field_name)
            if not isinstance(refs, list) or not refs:
                errors.append(f"execution-ready Agent PRD requires non-empty agent_execution.{field_name}")
            elif any(((objects.get(ref) or {}).get("type") != required_type) for ref in refs):
                errors.append(f"agent_execution.{field_name} must reference only {required_type} objects")
            if not object_type_ids(contract, required_type):
                errors.append(f"execution-ready Agent PRD requires at least one {required_type} object")
        for req_id in current_req_ids(contract):
            req = objects.get(req_id, {})
            payload = req.get("payload", {}) if isinstance(req, dict) else {}
            if not as_list(payload.get("acceptance_criteria")):
                errors.append(f"{req_id} missing acceptance_criteria for execution-ready Agent PRD")
            req_refs = collect_ids(payload)
            if not any(ref.startswith("VER-") for ref in req_refs):
                errors.append(f"{req_id} missing visible VER link for execution-ready Agent PRD")

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
    human = (root / "human-prd.md").read_text(encoding="utf-8")
    agent = (root / "agent-prd.md").read_text(encoding="utf-8")
    notes = (root / "intake-notes.md").read_text(encoding="utf-8")

    if len(human.strip()) < 20:
        errors.append("human-prd.md must be non-empty")
    if len(agent.strip()) < 20:
        errors.append("agent-prd.md must be non-empty")
    if len(notes.strip()) < 20:
        errors.append("intake-notes.md must be non-empty")

    if "contract" not in human.lower() and "合同" not in human and "契约" not in human:
        errors.append("human-prd.md should state its source contract")
    if "contract" not in agent.lower():
        errors.append("agent-prd.md should state its source contract")

    render_status = contract.get("render_status") if isinstance(contract.get("render_status"), dict) else {}
    human_status = render_status.get("human_prd")
    agent_status = render_status.get("agent_prd")
    if human_status and human_status != "not_requested" and human_status not in human.lower():
        errors.append(f"human-prd.md should state render_status.human_prd={human_status}")
    if agent_status and agent_status != "not_requested" and agent_status not in agent.lower():
        errors.append(f"agent-prd.md should state render_status.agent_prd={agent_status}")

    known = set((contract.get("objects") or {}).keys())
    for filename, text in (("human-prd.md", human), ("agent-prd.md", agent), ("intake-notes.md", notes)):
        dangling = sorted(ref for ref in collect_ids(text) if ref not in known and not ref.startswith(("TASK-", "PG-", "CHECK-")))
        if dangling:
            errors.append(f"{filename} has dangling refs: " + ", ".join(dangling))

    agent_required_sections = [
        "Source of Truth",
        "Input Contract",
        "Scope Contract",
        "Execution Contract",
        "Data and State",
        "Verification Contract",
        "Stop",
        "Done",
    ]
    if render_status.get("agent_prd") == "execution_ready":
        for section in agent_required_sections:
            if section not in agent:
                errors.append(f"execution-ready agent-prd.md missing section: {section}")

    return errors


def validate_task_plan(plan: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = [
        "plan_id",
        "planning_source_mode",
        "source_artifacts",
        "planning_status",
        "blocking_reasons",
        "missing_required_refs",
        "required_fixes",
        "task_graph",
        "dependency_edges",
        "parallel_groups",
        "stage_goal_coverage",
        "planning_gate_report",
    ]
    for key in required:
        if key not in plan:
            errors.append(f"execution-task-plan.json missing {key}")

    list_fields = [
        "blocking_reasons",
        "missing_required_refs",
        "required_fixes",
        "task_graph",
        "dependency_edges",
        "parallel_groups",
        "stage_goal_coverage",
        "planning_gate_report",
    ]
    for key in list_fields:
        if key in plan and not isinstance(plan.get(key), list):
            errors.append(f"execution-task-plan.json {key} must be a list")

    status = plan.get("planning_status")
    source_mode = plan.get("planning_source_mode")
    source = plan.get("source_artifacts", {})
    if not isinstance(source, dict):
        errors.append("execution-task-plan.json source_artifacts must be an object")
        source = {}

    render_status = contract.get("render_status") if isinstance(contract.get("render_status"), dict) else {}
    if source.get("contract_version") != contract.get("contract_version"):
        errors.append("task plan source_artifacts.contract_version must match contract_version")
    if source.get("agent_prd_ref") != "agent-prd.md":
        errors.append("task plan source_artifacts.agent_prd_ref must be agent-prd.md")
    if source.get("agent_prd_status") != render_status.get("agent_prd"):
        errors.append("task plan source_artifacts.agent_prd_status must match contract render_status.agent_prd")
    if source_mode == "contract_backed":
        if source.get("contract_ref") != "contract-envelope.json":
            errors.append("task plan source_artifacts.contract_ref must be contract-envelope.json")
        if source.get("phase_ref_kind") == "canonical_id":
            phase_ref = source.get("phase_ref")
            if object_type(contract, phase_ref) != "PHASE":
                errors.append("task plan source_artifacts.phase_ref must reference a PHASE object")
        elif source.get("phase_ref_kind"):
            errors.append("task plan source_artifacts.phase_ref_kind must be canonical_id when provided")
    elif source_mode == "rendered_agent_prd_only":
        if status != "blocked":
            errors.append("rendered_agent_prd_only task plan must be blocked")
        if source.get("phase_ref_kind") != "rendered_label":
            errors.append("rendered_agent_prd_only task plan requires phase_ref_kind=rendered_label")
        if not source.get("phase_ref_fallback_reason"):
            errors.append("rendered_agent_prd_only task plan requires phase_ref_fallback_reason")
    else:
        errors.append("execution-task-plan.json planning_source_mode must be contract_backed or rendered_agent_prd_only")

    if status == "ready":
        if source_mode != "contract_backed":
            errors.append("ready task plan must be contract_backed")
        if render_status.get("agent_prd") != "execution_ready":
            errors.append("ready task plan requires contract render_status.agent_prd=execution_ready")
        if source.get("agent_prd_status") != "execution_ready":
            errors.append("ready task plan requires source_artifacts.agent_prd_status=execution_ready")
        if source.get("phase_ref_kind") != "canonical_id":
            errors.append("ready task plan requires canonical phase_ref")
        phase_ref = source.get("phase_ref")
        if object_type(contract, phase_ref) != "PHASE":
            errors.append("ready task plan source_artifacts.phase_ref must reference a PHASE object")
        elif not current_req_ids(contract, phase_ref):
            errors.append("ready task plan requires at least one current REQ for source_artifacts.phase_ref")
        for key in ("blocking_reasons", "missing_required_refs", "required_fixes"):
            if as_list(plan.get(key)):
                errors.append(f"ready task plan must have empty {key}")
        if not as_list(plan.get("task_graph")):
            errors.append("ready task plan requires non-empty task_graph")
        if not as_list(plan.get("stage_goal_coverage")):
            errors.append("ready task plan requires stage_goal_coverage")
    elif status == "blocked":
        for key in ("task_graph", "dependency_edges", "parallel_groups"):
            if as_list(plan.get(key)):
                errors.append(f"blocked task plan must have empty {key}")
        if not any(as_list(plan.get(key)) for key in ("blocking_reasons", "missing_required_refs", "required_fixes")):
            errors.append("blocked task plan needs blocking_reasons, missing_required_refs, or required_fixes")
    else:
        errors.append("execution-task-plan.json planning_status must be ready or blocked")

    object_ids = set((contract.get("objects") or {}).keys())
    tasks = [task for task in as_list(plan.get("task_graph")) if isinstance(task, dict)]
    groups = [group for group in as_list(plan.get("parallel_groups")) if isinstance(group, dict)]
    edges = [edge for edge in as_list(plan.get("dependency_edges")) if isinstance(edge, dict)]
    task_ids = {task.get("task_id") for task in tasks}
    group_ids = {group.get("group_id") for group in groups}
    check_ids = {
        gate.get("check_id")
        for gate in as_list(plan.get("planning_gate_report"))
        if isinstance(gate, dict)
    }
    known = object_ids | task_ids | group_ids | check_ids

    for task_id in task_ids:
        if not isinstance(task_id, str) or not TASK_ID_RE.fullmatch(task_id):
            errors.append(f"task id must match TASK-###: {task_id}")
    for group_id in group_ids:
        if not isinstance(group_id, str) or not GROUP_ID_RE.fullmatch(group_id):
            errors.append(f"parallel group id must match PG-###: {group_id}")
    for check_id in check_ids:
        if not isinstance(check_id, str) or not CHECK_ID_RE.fullmatch(check_id):
            errors.append(f"planning gate check_id must match CHECK-###: {check_id}")

    plan_refs = collect_ids(plan)
    dangling = sorted(ref for ref in plan_refs if ref not in known)
    if dangling:
        errors.append("execution-task-plan.json has dangling refs: " + ", ".join(dangling))

    task_required = [
        "task_id",
        "title",
        "task_type",
        "contract_refs",
        "verification_refs",
        "done_refs",
        "stop_refs",
        "inputs",
        "outputs",
        "dependencies",
        "parallel_group",
        "allowed_files_or_modules",
        "forbidden_scope_refs",
        "acceptance",
        "verification",
        "stop_conditions",
        "status",
    ]
    for task in tasks:
        task_id = task.get("task_id", "<missing>")
        for key in task_required:
            if key not in task:
                errors.append(f"{task_id} missing {key}")
        for key in ("contract_refs", "verification_refs", "done_refs", "stop_refs", "inputs", "outputs", "acceptance", "verification", "stop_conditions"):
            if key in task and not as_list(task.get(key)):
                errors.append(f"{task_id} requires non-empty {key}")
        for key in (
            "contract_refs",
            "verification_refs",
            "done_refs",
            "stop_refs",
            "inputs",
            "outputs",
            "dependencies",
            "allowed_files_or_modules",
            "forbidden_scope_refs",
            "acceptance",
            "verification",
            "stop_conditions",
        ):
            if key in task and not isinstance(task.get(key), list):
                errors.append(f"{task_id}.{key} must be a list")
        if "allowed_files_or_modules" in task and not as_list(task.get("allowed_files_or_modules")):
            errors.append(f"{task_id}.allowed_files_or_modules must be non-empty")
        if task.get("task_type") not in TASK_TYPES:
            errors.append(f"{task_id}.task_type has invalid task_type")
        task_ref_schema = {
            "contract_refs": CONTRACT_REF_TYPES,
            "verification_refs": {"AC", "VER"},
            "done_refs": {"DONE"},
            "stop_refs": {"STOP"},
            "inputs": {"IN"},
            "outputs": {"OUT"},
            "forbidden_scope_refs": {"OOS", "BAR", "RISK"},
        }
        for key, allowed_types in task_ref_schema.items():
            if key in task:
                errors.extend(validate_ref_list_types(contract, task.get(key), f"{task_id}.{key}", allowed_types))
        if task.get("status") not in TASK_STATUS:
            errors.append(f"{task_id}.status has invalid status")
        if status == "ready" and task.get("status") not in READY_TASK_STATUS:
            errors.append(f"{task_id}.status must be planned or ready in a ready task plan")
        if status == "ready" and isinstance(source.get("phase_ref"), str):
            for req_ref in as_list(task.get("contract_refs")):
                if object_type(contract, req_ref) == "REQ" and payload_for(contract, req_ref).get("phase") != source.get("phase_ref"):
                    errors.append(f"{task_id}.contract_refs includes non-current-phase requirement {req_ref}")
        for dep in as_list(task.get("dependencies")):
            if dep not in task_ids:
                errors.append(f"{task_id} depends on missing task {dep}")
            if dep == task_id:
                errors.append(f"{task_id} cannot depend on itself")
        group = task.get("parallel_group")
        if group and group not in group_ids:
            errors.append(f"{task_id} references missing parallel_group {group}")

    adjacency: dict[str, list[str]] = {task_id: [] for task_id in task_ids if isinstance(task_id, str)}
    declared_edges: set[tuple[str, str]] = set()
    for task in tasks:
        task_id = task.get("task_id")
        if not isinstance(task_id, str):
            continue
        for dep in as_list(task.get("dependencies")):
            if isinstance(dep, str) and dep in task_ids:
                declared_edges.add((dep, task_id))
                adjacency.setdefault(dep, []).append(task_id)
    for edge in edges:
        src = edge.get("from")
        dst = edge.get("to")
        if src not in task_ids or dst not in task_ids:
            errors.append(f"dependency edge references missing task: {src}->{dst}")
        else:
            adjacency.setdefault(src, []).append(dst)
        if not edge.get("reason"):
            errors.append(f"dependency edge {src}->{dst} missing reason")
        if not as_list(edge.get("contract_refs")):
            errors.append(f"dependency edge {src}->{dst} missing contract_refs")
        if "contract_refs" in edge:
            errors.extend(validate_ref_list_types(contract, edge.get("contract_refs"), f"dependency edge {src}->{dst}.contract_refs", CONTRACT_REF_TYPES, require_non_empty=True))

    edge_pairs = {(edge.get("from"), edge.get("to")) for edge in edges}
    for edge in declared_edges:
        if edge not in edge_pairs:
            errors.append(f"task dependency {edge[0]}->{edge[1]} missing dependency_edges entry")
    for edge in edge_pairs:
        if edge[0] in task_ids and edge[1] in task_ids and edge not in declared_edges:
            errors.append(f"dependency edge {edge[0]}->{edge[1]} missing matching task.dependencies entry")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return False
        if node in visited:
            return True
        visiting.add(node)
        for nxt in adjacency.get(node, []):
            if not visit(nxt):
                return False
        visiting.remove(node)
        visited.add(node)
        return True

    for task_id in list(adjacency):
        if not visit(task_id):
            errors.append("dependency_edges contain a cycle")
            break

    for group in groups:
        refs = as_list(group.get("task_refs"))
        if group.get("status") not in PARALLEL_GROUP_STATUS:
            errors.append(f"parallel group {group.get('group_id')} has invalid status")
        if "task_refs" in group and not isinstance(group.get("task_refs"), list):
            errors.append(f"parallel group {group.get('group_id')}.task_refs must be a list")
        if group.get("status") == "parallel_safe":
            for a in refs:
                for b in refs:
                    if a != b and ((a, b) in edge_pairs or (b, a) in edge_pairs):
                        errors.append(f"parallel group {group.get('group_id')} contains dependency-linked tasks {a} and {b}")
        for ref in refs:
            if ref not in task_ids:
                errors.append(f"parallel group {group.get('group_id')} references missing task {ref}")

    for coverage in as_list(plan.get("stage_goal_coverage")):
        if not isinstance(coverage, dict):
            continue
        if coverage.get("coverage_status") not in COVERAGE_STATUS:
            errors.append("stage_goal_coverage has invalid coverage_status")
        if coverage.get("coverage_status") != "covered" and status == "ready":
            errors.append("ready task plan requires covered stage_goal_coverage")
        if "phase_ref" not in coverage:
            errors.append("stage_goal_coverage missing phase_ref")
        elif status == "ready" and object_type(contract, coverage.get("phase_ref")) != "PHASE":
            errors.append("ready stage_goal_coverage.phase_ref must reference PHASE")
        elif status == "ready" and isinstance(source.get("phase_ref"), str) and coverage.get("phase_ref") != source.get("phase_ref"):
            errors.append("ready stage_goal_coverage.phase_ref must match source_artifacts.phase_ref")
        if not coverage.get("phase_label"):
            errors.append("stage_goal_coverage missing phase_label")
        if "missing_refs" not in coverage or not isinstance(coverage.get("missing_refs"), list):
            errors.append("stage_goal_coverage.missing_refs must be a list")
        if status == "ready" and as_list(coverage.get("missing_refs")):
            errors.append("ready stage_goal_coverage must have empty missing_refs")
        if not as_list(coverage.get("goal_refs")):
            errors.append("stage_goal_coverage missing goal_refs")
        errors.extend(validate_ref_list_types(contract, coverage.get("goal_refs"), "stage_goal_coverage.goal_refs", CONTRACT_REF_TYPES, require_non_empty=True))
        if status == "ready" and not as_list(coverage.get("required_task_refs")):
            errors.append("ready stage_goal_coverage.required_task_refs must be non-empty")
        for ref in as_list(coverage.get("required_task_refs")):
            if ref not in task_ids:
                errors.append(f"stage_goal_coverage references missing task {ref}")

    for gate in as_list(plan.get("planning_gate_report")):
        if not isinstance(gate, dict):
            continue
        if gate.get("status") not in PLANNING_GATE_STATUS:
            errors.append(f"planning gate {gate.get('check_id')} has invalid status")
        if not as_list(gate.get("evidence_refs")):
            errors.append(f"planning gate {gate.get('check_id')} requires non-empty evidence_refs")
        for ref in as_list(gate.get("evidence_refs")):
            if not isinstance(ref, str) or not ID_RE.fullmatch(ref):
                errors.append(f"planning gate {gate.get('check_id')} has non-ID evidence ref {ref!r}")
            elif ref.startswith("CHECK-"):
                errors.append(f"planning gate {gate.get('check_id')} evidence_refs cannot use check ref {ref}")
        if gate.get("status") == "blocked" and status == "ready":
            errors.append(f"ready task plan cannot have blocked planning gate {gate.get('check_id')}")

    if status == "ready":
        phase_ref = source.get("phase_ref") if isinstance(source, dict) else None
        expected_refs = expected_ready_plan_refs(contract, phase_ref if isinstance(phase_ref, str) else None)
        task_covered_refs: set[str] = set()
        for task in tasks:
            for key in ("contract_refs", "verification_refs", "done_refs", "stop_refs", "inputs", "outputs"):
                task_covered_refs.update(ref for ref in as_list(task.get(key)) if isinstance(ref, str))
        missing_coverage = sorted(ref for ref in expected_refs if ref not in task_covered_refs)
        if missing_coverage:
            errors.append("ready task plan missing contract coverage: " + ", ".join(missing_coverage))

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_spec_intake_package.py <output-dir>", file=sys.stderr)
        return 2

    root = Path(argv[1])
    errors: list[str] = []
    required_files = [
        "contract-envelope.json",
        "human-prd.md",
        "agent-prd.md",
        "execution-task-plan.json",
        "intake-notes.md",
    ]
    for filename in required_files:
        if not (root / filename).exists():
            errors.append(f"missing {filename}")

    if errors:
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1

    contract = load_json(root / "contract-envelope.json")
    task_plan = load_json(root / "execution-task-plan.json")
    errors.extend(validate_contract(contract))
    errors.extend(validate_prd_files(root, contract))
    errors.extend(validate_task_plan(task_plan, contract))

    ok = not errors
    print(json.dumps({"ok": ok, "errors": errors}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
