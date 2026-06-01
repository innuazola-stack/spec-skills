from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


REQUIRED_STAGES = {
    "overall_planning",
    "task_formation",
    "single_task_review",
    "global_dag_review",
    "artifact_generation",
    "final_design_acceptance",
}

REQUIRED_GATES = {
    "source_readiness",
    "traceability",
    "rust_stack_readiness",
    "control_flow_readiness",
    "data_flow_readiness",
    "technical_decision_readiness",
    "staged_review_readiness",
    "dag_soundness",
    "parallel_safety",
    "task_fixture_readiness",
    "design_acceptance_task",
    "no_starter_prompt_template",
}

STALE_DEV_WORDING = [
    "Implement only",
    "implementation task",
    "Report changed files",
    "implemented task",
]


def fail(errors: list[str]) -> None:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail([f"cannot read JSON {path}: {exc}"])
    raise AssertionError("unreachable")


def find_cycles(task_ids: set[str], edges: list[dict]) -> list[str]:
    graph = {task_id: [] for task_id in task_ids}
    for edge in edges:
        graph.setdefault(edge.get("from"), []).append(edge.get("to"))

    visited: set[str] = set()
    active: set[str] = set()
    cycles: list[str] = []

    def visit(node: str) -> None:
        if node in active:
            cycles.append(node)
            return
        if node in visited:
            return
        visited.add(node)
        active.add(node)
        for nxt in graph.get(node, []):
            if nxt in graph:
                visit(nxt)
        active.remove(node)

    for task_id in task_ids:
        visit(task_id)
    return cycles


def validate(project_root: Path, planning_json: Path) -> list[str]:
    errors: list[str] = []
    plan = load_json(planning_json)

    for field in [
        "planning_status",
        "output_root",
        "detailed_design_root",
        "rust_design_path",
        "source_inventory",
        "planning_review_stages",
        "tasks",
        "dag",
        "fixtures",
        "coverage_matrix",
        "planning_gate_report",
        "external_dependencies",
        "open_questions",
        "required_fixes",
    ]:
        if field not in plan:
            errors.append(f"planning missing field: {field}")

    if errors:
        return errors

    if plan["detailed_design_root"] != "docs/design":
        errors.append("detailed_design_root must be docs/design")
    if plan["rust_design_path"] != "docs/design/rust-implementation-design.md":
        errors.append("rust_design_path must be docs/design/rust-implementation-design.md")

    rust_design = project_root / plan["rust_design_path"]
    if not rust_design.exists():
        errors.append(f"missing rust design document: {plan['rust_design_path']}")

    stages = {stage.get("stage_id") for stage in plan["planning_review_stages"]}
    missing_stages = sorted(REQUIRED_STAGES - stages)
    if missing_stages:
        errors.append(f"missing planning_review_stages: {', '.join(missing_stages)}")
    for stage in plan["planning_review_stages"]:
        if stage.get("status") != "pass":
            errors.append(f"planning stage not pass: {stage.get('stage_id')}={stage.get('status')}")
        for field in ["checks", "findings", "evidence_refs"]:
            if not stage.get(field):
                errors.append(f"planning stage {stage.get('stage_id')} missing {field}")

    gates = {gate.get("gate"): gate.get("status") for gate in plan["planning_gate_report"]}
    missing_gates = sorted(REQUIRED_GATES - set(gates))
    if missing_gates:
        errors.append(f"missing planning gates: {', '.join(missing_gates)}")
    for gate, status in gates.items():
        if status not in {"pass", "warning"}:
            errors.append(f"planning gate not pass/warning: {gate}={status}")

    tasks = plan["tasks"]
    task_ids = [task.get("task_id") for task in tasks]
    task_id_set = set(task_ids)
    if len(task_ids) != len(task_id_set):
        errors.append("duplicate task_id found")

    detailed_tasks = [task for task in tasks if task.get("task_type") == "detailed_design"]
    acceptance_tasks = [task for task in tasks if task.get("task_type") == "design_acceptance"]
    if len(acceptance_tasks) != 1:
        errors.append(f"expected exactly one design_acceptance task, found {len(acceptance_tasks)}")

    for task in tasks:
        task_id = task.get("task_id", "<missing>")
        for field in [
            "title",
            "source_refs",
            "inputs",
            "outputs",
            "allowed_scope",
            "forbidden_scope",
            "acceptance",
            "verification",
            "stop_conditions",
            "dependencies",
            "design_doc_path",
            "fixture_dir",
            "prompt_path",
            "agents_path",
            "claude_path",
        ]:
            if field not in task:
                errors.append(f"{task_id} missing field {field}")
        design_doc_path = task.get("design_doc_path", "")
        if not design_doc_path.startswith("docs/design/") or not design_doc_path.endswith(".md"):
            errors.append(f"{task_id} design_doc_path must be docs/design/*.md")
        for dependency in task.get("dependencies", []):
            if dependency not in task_id_set:
                errors.append(f"{task_id} depends on unknown task {dependency}")

        for fixture_field in ["prompt_path", "agents_path", "claude_path"]:
            rel = task.get(fixture_field)
            if not rel:
                continue
            fixture_path = project_root / rel
            if not fixture_path.exists():
                errors.append(f"{task_id} missing fixture file: {rel}")
                continue
            text = fixture_path.read_text(encoding="utf-8")
            if "Do not implement code" not in text:
                errors.append(f"{rel} missing no-code rule")
            if design_doc_path and design_doc_path not in text:
                errors.append(f"{rel} missing exact design_doc_path")
            for wording in STALE_DEV_WORDING:
                if wording in text:
                    errors.append(f"{rel} contains stale development wording: {wording}")

    if acceptance_tasks:
        acceptance = acceptance_tasks[0]
        acceptance_deps = set(acceptance.get("dependencies", []))
        detailed_ids = {task["task_id"] for task in detailed_tasks}
        missing = sorted(detailed_ids - acceptance_deps)
        if missing:
            errors.append(f"design_acceptance missing dependencies: {', '.join(missing)}")

    dag = plan["dag"]
    edges = dag.get("edges", [])
    node_ids = {node.get("task_id") for node in dag.get("nodes", [])}
    if node_ids != task_id_set:
        errors.append("dag.nodes task IDs do not match tasks")
    for edge in edges:
        src = edge.get("from")
        dst = edge.get("to")
        if src not in task_id_set or dst not in task_id_set:
            errors.append(f"bad edge: {src}->{dst}")
        if not edge.get("reason"):
            errors.append(f"edge missing reason: {src}->{dst}")
        if not edge.get("source_refs"):
            errors.append(f"edge missing source_refs: {src}->{dst}")
    cycles = find_cycles(task_id_set, edges)
    if cycles:
        errors.append(f"DAG has cycles: {', '.join(cycles)}")

    fixture_index = {fixture.get("task_id") for fixture in plan["fixtures"]}
    if fixture_index != task_id_set:
        errors.append("fixtures index task IDs do not match tasks")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--planning-json", required=True)
    args = parser.parse_args()

    errors = validate(Path(args.project_root), Path(args.planning_json))
    if errors:
        fail(errors)
    print("PASS: design planning output validation")


if __name__ == "__main__":
    main()
