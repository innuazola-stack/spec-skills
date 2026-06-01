#!/usr/bin/env python3
"""Validate a generated development-planning package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


PHASE_IDS = ["STAGE-001", "STAGE-002", "STAGE-003", "STAGE-004"]
TASK_FILES = ["task.md", "prompt.md", "AGENTS.md", "CLAUDE.md"]
REQUIREMENT_ID_RE = re.compile(r"\b(?:FR|AC)-\d{3}\b")


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def load_plan(path_arg: str | None) -> tuple[Path, dict[str, Any]]:
    root = Path(path_arg) if path_arg else Path.cwd()
    root = root.resolve()
    if root.is_file():
        plan_path = root
        output_root = root.parent
    elif (root / "development-planning.json").exists():
        output_root = root
        plan_path = root / "development-planning.json"
    else:
        output_root = root / "tasks" / "development"
        plan_path = output_root / "development-planning.json"

    if not plan_path.exists():
        fail(f"missing planning artifact: {plan_path}")
    try:
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {plan_path}: {exc}")
    if not isinstance(plan, dict):
        fail("development-planning.json must be a JSON object")
    return output_root, plan


def require_keys(obj: dict[str, Any], keys: list[str], label: str) -> None:
    for key in keys:
        if key not in obj:
            fail(f"{label} missing required key {key}")


def path_from_declared(output_root: Path, declared_path: str, expected_filename: str, task_id: str) -> Path:
    declared = Path(declared_path)
    expected_suffix = Path("tasks") / "development" / task_id / expected_filename
    short_suffix = Path(task_id) / expected_filename
    if declared.is_absolute():
        candidate = declared
    elif len(declared.parts) >= 4 and Path(*declared.parts[-4:]) == expected_suffix:
        candidate = output_root / task_id / expected_filename
    elif len(declared.parts) >= 2 and Path(*declared.parts[-2:]) == short_suffix:
        candidate = output_root / task_id / expected_filename
    else:
        fail(f"{task_id} declared path for {expected_filename} is outside the task contract path: {declared_path}")
    return candidate.resolve()


def infer_target_root(output_root: Path) -> Path:
    if output_root.name == "development" and output_root.parent.name == "tasks":
        return output_root.parent.parent
    return output_root.parent


def normalize_source_inventory_paths(plan: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    for source in plan.get("source_inventory", []):
        if isinstance(source, str):
            raw_path = source
        elif isinstance(source, dict):
            raw_path = str(source.get("path", ""))
        else:
            continue
        if raw_path:
            paths.add(raw_path.replace("\\", "/"))
    return paths


def collect_doc_requirement_ids(target_root: Path) -> set[str]:
    docs_root = target_root / "docs"
    if not docs_root.exists():
        return set()
    ids: set[str] = set()
    for path in docs_root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".json"}:
            ids.update(REQUIREMENT_ID_RE.findall(path.read_text(encoding="utf-8", errors="ignore")))
    return ids


def validate_shape(plan: dict[str, Any]) -> None:
    require_keys(
        plan,
        [
            "planning_status",
            "output_root",
            "source_inventory",
            "planning_harness_model",
            "phase_reports",
            "tasks",
            "dag",
            "task_descriptions",
            "fixtures",
            "coverage_matrix",
            "delivery_acceptance",
            "task_logic_review",
            "plan_integrity_review",
            "planning_gate_report",
            "required_fixes",
        ],
        "plan",
    )
    if plan["planning_status"] not in {"ready", "blocked"}:
        fail("planning_status must be ready or blocked")
    model = plan["planning_harness_model"]
    if not isinstance(model, dict) or model.get("target_type") != "harness-workflow":
        fail("planning_harness_model.target_type must be harness-workflow")


def validate_phase_reports(plan: dict[str, Any], ready: bool) -> None:
    phase_reports = plan.get("phase_reports")
    if not isinstance(phase_reports, list):
        fail("phase_reports must be an array")
    ids = [phase.get("stage_id") for phase in phase_reports if isinstance(phase, dict)]
    if ids != PHASE_IDS:
        fail(f"phase_reports must contain exactly {PHASE_IDS} in order")
    for phase in phase_reports:
        require_keys(
            phase,
            ["stage_id", "stage_name", "purpose", "inputs", "outputs", "review_checks", "status", "blocking_findings"],
            f"phase {phase.get('stage_id')}",
        )
        if phase["status"] not in {"pass", "blocked"}:
            fail(f"phase {phase['stage_id']} status must be pass or blocked")
        if ready and phase["status"] != "pass":
            fail(f"ready plan has non-passing phase {phase['stage_id']}")


def validate_task_shape(task: dict[str, Any]) -> None:
    require_keys(
        task,
        [
            "task_id",
            "title",
            "task_type",
            "source_refs",
            "inputs",
            "expected_outputs",
            "impacted_areas",
            "allowed_scope",
            "forbidden_scope",
            "acceptance",
            "verification",
            "stop_conditions",
            "dependencies",
            "handoff_requirements",
            "task_description_path",
            "fixture_dir",
            "prompt_path",
            "agents_path",
            "claude_path",
        ],
        f"task {task.get('task_id')}",
    )


def normalize_nodes(nodes: list[Any], tasks: list[dict[str, Any]]) -> list[str]:
    if not nodes:
        return [task["task_id"] for task in tasks]
    normalized: list[str] = []
    for node in nodes:
        if isinstance(node, str):
            normalized.append(node)
        elif isinstance(node, dict) and isinstance(node.get("task_id"), str):
            normalized.append(node["task_id"])
        elif isinstance(node, dict) and isinstance(node.get("id"), str):
            normalized.append(node["id"])
        else:
            fail(f"unsupported DAG node shape: {node!r}")
    return normalized


def validate_dag(plan: dict[str, Any], tasks: list[dict[str, Any]]) -> None:
    dag = plan["dag"]
    require_keys(dag, ["nodes", "edges", "parallel_groups", "execution_order", "cycle_check"], "dag")
    task_ids = [task["task_id"] for task in tasks]
    if len(set(task_ids)) != len(task_ids):
        fail("task IDs must be unique")
    nodes = normalize_nodes(dag["nodes"], tasks)
    if set(nodes) != set(task_ids):
        fail("dag.nodes must match task IDs")
    execution_order = dag["execution_order"]
    if not isinstance(execution_order, list):
        fail("dag.execution_order must be an array")
    if len(execution_order) != len(task_ids) or len(set(execution_order)) != len(execution_order):
        fail("dag.execution_order must contain each task ID exactly once")
    if set(execution_order) != set(task_ids):
        fail("dag.execution_order must include exactly the task IDs")

    edges = dag["edges"]
    adjacency: dict[str, list[str]] = {task_id: [] for task_id in task_ids}
    indegree: dict[str, int] = {task_id: 0 for task_id in task_ids}
    for edge in edges:
        require_keys(edge, ["from", "to", "reason", "consumed_output", "source_refs"], "dag edge")
        src = edge["from"]
        dst = edge["to"]
        if src not in indegree or dst not in indegree:
            fail(f"edge references unknown task: {src} -> {dst}")
        if not edge["reason"] or not edge["consumed_output"]:
            fail(f"edge {src} -> {dst} must include reason and consumed_output")
        adjacency[src].append(dst)
        indegree[dst] += 1

    order_index = {task_id: idx for idx, task_id in enumerate(execution_order)}
    for src, downstream in adjacency.items():
        for dst in downstream:
            if order_index[src] >= order_index[dst]:
                fail(f"execution_order is not topological for edge {src} -> {dst}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visiting:
            fail("DAG contains a cycle")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dst in adjacency[task_id]:
            visit(dst)
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in task_ids:
        visit(task_id)

    def has_path(src: str, dst: str) -> bool:
        stack = list(adjacency[src])
        seen: set[str] = set()
        while stack:
            node = stack.pop()
            if node == dst:
                return True
            if node in seen:
                continue
            seen.add(node)
            stack.extend(adjacency[node])
        return False

    parallel_groups = dag["parallel_groups"]
    if not isinstance(parallel_groups, list):
        fail("dag.parallel_groups must be an array")
    for group in parallel_groups:
        if not isinstance(group, dict):
            fail("dag.parallel_groups entries must be objects")
        require_keys(group, ["group_id", "task_ids", "rationale", "conflict_check", "source_refs"], "parallel group")
        group_ids = group["task_ids"]
        if not isinstance(group_ids, list) or len(group_ids) < 2:
            fail(f"parallel group {group.get('group_id')} must contain at least two task IDs")
        if len(set(group_ids)) != len(group_ids):
            fail(f"parallel group {group.get('group_id')} contains duplicate task IDs")
        unknown = [task_id for task_id in group_ids if task_id not in task_ids]
        if unknown:
            fail(f"parallel group {group.get('group_id')} references unknown task IDs: {unknown}")
        for src in group_ids:
            for dst in group_ids:
                if src != dst and has_path(src, dst):
                    fail(f"parallel group {group.get('group_id')} contains dependent tasks: {src} -> {dst}")

    cycle_check = dag["cycle_check"]
    if cycle_check.get("status") != "pass":
        fail("ready DAG cycle_check.status must be pass")
    if cycle_check.get("cycles"):
        fail("ready DAG cycle_check.cycles must be empty")


def validate_final_acceptance(plan: dict[str, Any], tasks: list[dict[str, Any]]) -> None:
    acceptance_tasks = [task for task in tasks if task.get("task_type") == "delivery_acceptance"]
    if len(acceptance_tasks) != 1:
        fail("ready plan must include exactly one delivery_acceptance task")
    final_task = acceptance_tasks[0]
    non_deferred = [
        task["task_id"]
        for task in tasks
        if task["task_id"] != final_task["task_id"] and task.get("task_status", "ready") != "deferred"
    ]
    dependencies = set(final_task.get("dependencies", []))
    missing = [task_id for task_id in non_deferred if task_id not in dependencies]
    if missing:
        fail(f"delivery_acceptance task missing dependencies: {missing}")
    execution_order = plan["dag"]["execution_order"]
    if execution_order[-1] != final_task["task_id"]:
        fail("delivery_acceptance task must be last in execution_order")
    delivery = plan.get("delivery_acceptance", {})
    if delivery and delivery.get("task_id") not in {None, final_task["task_id"]}:
        fail("delivery_acceptance.task_id must match final delivery acceptance task")


def validate_task_files(output_root: Path, tasks: list[dict[str, Any]]) -> None:
    for task in tasks:
        task_id = task["task_id"]
        task_dir = output_root / task_id
        declared_dir = Path(task["fixture_dir"])
        expected_dir = (output_root / task_id).resolve()
        if declared_dir.is_absolute():
            declared_resolved = declared_dir.resolve()
        elif len(declared_dir.parts) >= 3 and Path(*declared_dir.parts[-3:]) == Path("tasks") / "development" / task_id:
            declared_resolved = expected_dir
        elif len(declared_dir.parts) >= 1 and declared_dir.parts[-1] == task_id:
            declared_resolved = expected_dir
        else:
            fail(f"{task_id} fixture_dir is outside the task contract path: {task['fixture_dir']}")
        if declared_resolved != expected_dir:
            fail(f"{task_id} fixture_dir does not match expected task directory")
        if not task_dir.exists():
            fail(f"missing task directory: {task_dir}")
        path_fields = {
            "task.md": "task_description_path",
            "prompt.md": "prompt_path",
            "AGENTS.md": "agents_path",
            "CLAUDE.md": "claude_path",
        }
        for filename in TASK_FILES:
            path = path_from_declared(output_root, task[path_fields[filename]], filename, task_id)
            expected_path = (task_dir / filename).resolve()
            if path != expected_path:
                fail(f"{task_id} declared {path_fields[filename]} does not match {expected_path}")
            if not path.exists():
                fail(f"missing task file: {path}")
            text = path.read_text(encoding="utf-8").strip()
            if len(text) < 20:
                fail(f"task file is too thin: {path}")


def validate_source_inventory(output_root: Path, plan: dict[str, Any]) -> None:
    target_root = infer_target_root(output_root)
    docs_root = target_root / "docs"
    if not docs_root.exists():
        return
    source_paths = normalize_source_inventory_paths(plan)
    for contract in docs_root.rglob("contract-envelope.json"):
        rel_path = contract.relative_to(target_root).as_posix()
        if rel_path not in source_paths:
            fail(f"source_inventory missing material contract source: {rel_path}")


def validate_requirement_coverage(output_root: Path, plan: dict[str, Any], tasks: list[dict[str, Any]]) -> None:
    target_root = infer_target_root(output_root)
    expected_ids = collect_doc_requirement_ids(target_root)
    if not expected_ids:
        return

    matrix = plan.get("requirement_coverage_matrix")
    if not isinstance(matrix, list) or not matrix:
        fail("ready plan with FR/AC source IDs must include non-empty requirement_coverage_matrix")

    task_ids = {task["task_id"] for task in tasks}
    acceptance_tasks = {task["task_id"] for task in tasks if task.get("task_type") == "delivery_acceptance"}
    covered_ids: set[str] = set()
    for row in matrix:
        if not isinstance(row, dict):
            fail("requirement_coverage_matrix rows must be objects")
        require_keys(
            row,
            ["coverage_id", "source_requirements", "covered_by_tasks", "verified_by", "required_evidence"],
            "requirement coverage row",
        )
        source_requirements = row["source_requirements"]
        covered_by_tasks = row["covered_by_tasks"]
        if not isinstance(source_requirements, list) or not source_requirements:
            fail(f"requirement coverage row {row.get('coverage_id')} must list source_requirements")
        if not isinstance(covered_by_tasks, list) or not covered_by_tasks:
            fail(f"requirement coverage row {row.get('coverage_id')} must list covered_by_tasks")
        unknown_tasks = [task_id for task_id in covered_by_tasks if task_id not in task_ids]
        if unknown_tasks:
            fail(f"requirement coverage row {row.get('coverage_id')} references unknown tasks: {unknown_tasks}")
        if acceptance_tasks and not acceptance_tasks.intersection(covered_by_tasks):
            fail(f"requirement coverage row {row.get('coverage_id')} must include the final delivery acceptance task")
        if not row["verified_by"] or not row["required_evidence"]:
            fail(f"requirement coverage row {row.get('coverage_id')} must include verification and evidence")
        covered_ids.update(str(req_id) for req_id in source_requirements)

    missing = sorted(expected_ids - covered_ids)
    if missing:
        fail(f"requirement_coverage_matrix missing source requirement IDs: {missing}")


def validate_ready(output_root: Path, plan: dict[str, Any]) -> None:
    tasks = plan["tasks"]
    if not tasks:
        fail("ready plan must include tasks")
    for task in tasks:
        validate_task_shape(task)
    if plan["task_logic_review"].get("status") != "pass":
        fail("ready plan requires task_logic_review.status=pass")
    if plan["plan_integrity_review"].get("status") != "pass":
        fail("ready plan requires plan_integrity_review.status=pass")
    if plan["task_logic_review"].get("blocking_findings"):
        fail("ready plan task_logic_review.blocking_findings must be empty")
    if plan["plan_integrity_review"].get("blocking_findings"):
        fail("ready plan plan_integrity_review.blocking_findings must be empty")
    if plan["required_fixes"]:
        fail("ready plan required_fixes must be empty")
    validate_source_inventory(output_root, plan)
    validate_dag(plan, tasks)
    validate_requirement_coverage(output_root, plan, tasks)
    validate_final_acceptance(plan, tasks)
    validate_task_files(output_root, tasks)


def validate_blocked(plan: dict[str, Any]) -> None:
    if not plan["required_fixes"]:
        fail("blocked plan must include required_fixes")
    dag = plan["dag"]
    for key in ["nodes", "edges", "parallel_groups", "execution_order"]:
        if dag.get(key):
            fail(f"blocked plan must keep dag.{key} empty")
    for key in ["tasks", "task_descriptions", "fixtures"]:
        if plan.get(key):
            fail(f"blocked plan must keep {key} empty")
    if plan["task_logic_review"].get("status") == "pass":
        fail("blocked plan must not pass task_logic_review")
    if plan["plan_integrity_review"].get("status") == "pass":
        fail("blocked plan must not pass plan_integrity_review")


def main(argv: list[str]) -> int:
    output_root, plan = load_plan(argv[1] if len(argv) > 1 else None)
    validate_shape(plan)
    ready = plan["planning_status"] == "ready"
    validate_phase_reports(plan, ready=ready)
    if ready:
        validate_ready(output_root, plan)
    else:
        validate_blocked(plan)
    print("PASS: development planning package validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
