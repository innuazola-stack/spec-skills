from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


TARGET = Path(r"C:\Users\54256213\Documents\github\spec-scheduler")
PLANNING_OUTPUT_ROOT = "tasks/design"
DETAILED_DESIGN_ROOT = "docs/design"
OUT = TARGET / PLANNING_OUTPUT_ROOT
DESIGN_OUT = TARGET / DETAILED_DESIGN_ROOT
DOCS = TARGET / "docs"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def jdump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


source_inventory = [
    {
        "path": "docs/agent-prd.md",
        "kind": "Agent PRD",
        "impact": "Defines execution-ready product requirements, current Phase 1 refs, acceptance matrix, Scheduler boundaries, and agent execution appendix.",
        "key_refs": ["REQ-001..REQ-024", "AC-001..AC-024", "VER-001..VER-024", "PHASE-001..PHASE-004"],
    },
    {
        "path": "docs/human-prd.md",
        "kind": "Human PRD",
        "impact": "Human-facing PRD source that records the product intent and user-visible Scheduler boundaries; used as a parity source against agent-prd.md and contract-envelope.json.",
        "key_refs": ["human-facing Scheduler requirement narrative", "Phase 1/Phase 2 intent"],
    },
    {
        "path": "docs/intake-notes.md",
        "kind": "intake notes",
        "impact": "Initial intake context used only for source completeness and parity checks; implementation obligations must still trace through PRD/HLD/contract refs.",
        "key_refs": ["intake context"],
    },
    {
        "path": "docs/high-level-design.md",
        "kind": "HLD markdown",
        "impact": "Defines implementation-ready architecture, control flow, data flow, interface contracts, state model, technical decisions, and real acceptance plan.",
        "key_refs": ["TECH-008..TECH-015", "DCT-015..DCT-020", "FLOW-STEP-001..FLOW-STEP-011"],
    },
    {
        "path": "docs/high-level-design.json",
        "kind": "HLD structured source",
        "impact": "Structured source for components, flows, objects, interfaces, state model, implementation design, environment, and design gates.",
        "key_refs": ["HLD-SCHEDULER-001"],
    },
    {
        "path": "docs/contract-envelope.json",
        "kind": "canonical contract",
        "impact": "Canonical object graph and traceability source for requirements, data contracts, technical choices, stop conditions, and done criteria.",
        "key_refs": ["CORE-001", "SCOPE-001", "DCT-014", "BAR-003"],
    },
    {
        "path": "docs/hld-semantic-review.json",
        "kind": "semantic review",
        "impact": "Confirms HLD review_status=pass across source traceability, control flow, data/data objects, interface precision, technical implementation, acceptance, parity, and task boundary.",
        "key_refs": ["review_status=pass"],
    },
    {
        "path": "docs/acceptance/scheduler_acceptance.py",
        "kind": "acceptance runner",
        "impact": "Defines real acceptance invocation wrapper and required scheduler acceptance-run boundary.",
        "key_refs": ["DCT-014", "VER-014..VER-024"],
    },
    {
        "path": "docs/acceptance/scheduler-runtime-fixtures.json",
        "kind": "acceptance fixture",
        "impact": "Provides real runtime DAG fixtures for query-only, schedulable, pending-result, no-intervention, and exhausted scenarios.",
        "key_refs": ["SRC-012"],
    },
    {
        "path": "docs/acceptance/executor-result-samples.json",
        "kind": "acceptance fixture",
        "impact": "Provides accepted, missing-evidence, and stale-token Executor result samples.",
        "key_refs": ["SRC-013", "SRC-005"],
    },
]

tasks = [
    {
        "task_id": "TASK-001",
        "title": "Design Rust workspace, configuration, and process entrypoints",
        "task_type": "detailed_design",
        "source_refs": ["TECH-008", "TECH-009", "DCT-015", "DCT-016", "REQ-014", "REQ-015"],
        "inputs": ["docs/agent-prd.md", "docs/human-prd.md", "docs/high-level-design.md", "docs/high-level-design.json", "docs/contract-envelope.json"],
        "outputs": [
            "Cargo workspace and crate skeleton design",
            "scheduler binary entrypoint design",
            "configuration model design for bind address, state directory, SQLite path, capacity, lease timeout, executor command",
            "module layout design matching Rust implementation design",
            "documented Rust crate selection decision design for HTTP, SQLite, CLI/config, error handling, tracing, and time",
        ],
        "allowed_scope": [
            "Specify Rust project structure and module boundaries without creating files",
            "Specify configuration loading and CLI flag behavior without implementing it",
            "Select proposed compile-time dependencies only where HLD leaves implementation-library choice open: HTTP JSON daemon, SQLite WAL, CLI/config, serialization, logging/tracing, error handling, and time",
            "Record any dependency choice with rationale and a stop condition if the choice conflicts with HLD or project owner direction",
        ],
        "forbidden_scope": [
            "Design scheduling decisions outside this task",
            "Invent route mutation endpoints",
            "Choose a different storage engine or public transport",
        ],
        "acceptance": [
            "Design document specifies the crate/module layout expected for later implementation",
            "Design document specifies configuration parsing and startup validation behavior",
            "Design document specifies rejection behavior for unsupported non-local bind address unless explicitly configured for tests",
            "Chosen Rust crates are documented as design decisions and do not change HLD technology choices",
        ],
        "verification": [
            "Review crate/module design against HLD boundaries",
            "Review proposed configuration behavior against PRD/HLD refs",
            "Record later implementation verification commands only as proposed checks",
        ],
        "stop_conditions": ["HLD technology stack conflicts with project owner direction", "Required Rust toolchain is absent"],
        "dependencies": [],
        "fixture_dir": "tasks/design/fixtures/TASK-001",
        "prompt_path": "tasks/design/fixtures/TASK-001/prompt.md",
        "agents_path": "tasks/design/fixtures/TASK-001/AGENTS.md",
        "claude_path": "tasks/design/fixtures/TASK-001/CLAUDE.md",
    },
    {
        "task_id": "TASK-002",
        "title": "Define domain types, state machines, and SQLite schema",
        "task_type": "detailed_design",
        "source_refs": ["DATA-007", "DATA-008", "DATA-009", "DATA-010", "DATA-011", "DCT-016", "DCT-020", "STATE-003", "STATE-004"],
        "inputs": ["TASK-001 module layout", "HLD data_objects", "HLD state_model", "contract objects DCT-016/DCT-020"],
        "outputs": [
            "Rust domain structs/enums design for runtime snapshots, jobs, leases, Executor results, intervention decisions, audit events",
            "SQLite table schema and migration design",
            "State transition enum and reason-code vocabulary design",
        ],
        "allowed_scope": [
            "Specify serializable domain types and DB row mappings",
            "Specify schema constraints including update_version, active scheduling_key uniqueness, foreign keys, and append-only audit fields",
        ],
        "forbidden_scope": ["Design daemon loop behavior outside this task", "Invoke Executor", "Accept results without state-transition service"],
        "acceptance": [
            "All HLD data objects have corresponding Rust types or documented DB rows",
            "Schema covers dag_runtime, node_runtime, scheduler_job, lease_record, executor_result, intervention_decision, route_exhaustion, audit_event",
            "State enum excludes business_success/project_done route outcomes",
        ],
        "verification": ["Review domain model coverage against HLD data objects", "Review schema design against required persistence and audit invariants"],
        "stop_conditions": ["A required HLD field cannot be represented without inventing semantics"],
        "dependencies": ["TASK-001"],
        "fixture_dir": "tasks/design/fixtures/TASK-002",
        "prompt_path": "tasks/design/fixtures/TASK-002/prompt.md",
        "agents_path": "tasks/design/fixtures/TASK-002/AGENTS.md",
        "claude_path": "tasks/design/fixtures/TASK-002/CLAUDE.md",
    },
    {
        "task_id": "TASK-003",
        "title": "Design RuntimeStore transaction and audit boundary",
        "task_type": "detailed_design",
        "source_refs": ["TECH-009", "TECH-010", "TECH-014", "DCT-016", "DCT-017", "DCT-020", "REQ-015", "REQ-023"],
        "inputs": ["TASK-002 schema and domain types"],
        "outputs": [
            "RuntimeStore abstraction design",
            "SQLite WAL initialization design",
            "one-DAG-runtime transaction helper design",
            "compare-and-update update_version check design",
            "append-only audit_event writer design",
        ],
        "allowed_scope": [
            "Specify SQLite connection setup, transactions, current-state reads/writes, and audit writes",
            "Specify narrow repository APIs for later implementation tasks",
        ],
        "forbidden_scope": ["Design readiness rules outside this task", "Invoke external processes", "Design HTTP endpoints outside this task"],
        "acceptance": [
            "Every state-changing repository method can insert audit_event in the same transaction",
            "Stale update_version causes rollback/conflict",
            "audit_event rows are append-only",
        ],
        "verification": ["Review transaction design against one-DAG-runtime boundary", "Review audit and stale-version behavior against PRD/HLD refs"],
        "stop_conditions": ["SQLite transaction semantics cannot support required atomicity"],
        "dependencies": ["TASK-002"],
        "fixture_dir": "tasks/design/fixtures/TASK-003",
        "prompt_path": "tasks/design/fixtures/TASK-003/prompt.md",
        "agents_path": "tasks/design/fixtures/TASK-003/AGENTS.md",
        "claude_path": "tasks/design/fixtures/TASK-003/CLAUDE.md",
    },
    {
        "task_id": "TASK-004",
        "title": "Design localhost HTTP JSON API control plane",
        "task_type": "detailed_design",
        "source_refs": ["TECH-008", "DCT-015", "REQ-014", "REQ-024", "STOP-008", "VER-014"],
        "inputs": ["TASK-001 process entrypoints", "TASK-003 RuntimeStore APIs"],
        "outputs": [
            "HTTP JSON endpoint handler design for DAG/runtime query, lifecycle, tick, result-intake routing boundary, and audit",
            "ResultIntakePort trait or equivalent service boundary design for TASK-008",
            "caller identity and authorization guard",
            "route-definition mutation rejection behavior",
        ],
        "allowed_scope": [
            "Specify endpoint shapes from DCT-015",
            "Map transport errors to 401/403/409/422 semantics",
            "Call existing RuntimeStore/service boundaries only",
            "For Executor results, specify transport-level parsing, caller guard, and delegation to a ResultIntakePort; do not design result validation or state transitions in this task",
        ],
        "forbidden_scope": ["Add route design/mutation APIs", "Run scheduler loop decisions inline without service boundary", "Design ResultIntake validation/state transitions from TASK-008"],
        "acceptance": [
            "All DCT-015 endpoints exist",
            "Executor-result endpoint delegates to ResultIntakePort and has no embedded result state-transition logic",
            "Route mutation attempts are rejected without state write",
            "Unauthorized calls are rejected and auditable",
        ],
        "verification": ["Review API surface against DCT-015", "Review handler/service boundary design against TASK-008 responsibilities"],
        "stop_conditions": ["Authentication/authorization model is not sufficiently defined for endpoint guard behavior"],
        "dependencies": ["TASK-003"],
        "fixture_dir": "tasks/design/fixtures/TASK-004",
        "prompt_path": "tasks/design/fixtures/TASK-004/prompt.md",
        "agents_path": "tasks/design/fixtures/TASK-004/AGENTS.md",
        "claude_path": "tasks/design/fixtures/TASK-004/CLAUDE.md",
    },
    {
        "task_id": "TASK-005",
        "title": "Design daemon loop, recovery reconciliation, and intervention classification",
        "task_type": "detailed_design",
        "source_refs": ["FLOW-STEP-001", "FLOW-STEP-005", "FLOW-STEP-011", "REQ-012", "REQ-013", "REQ-017", "REQ-021", "TECH-015"],
        "inputs": ["TASK-003 RuntimeStore transaction boundary", "TASK-002 state model"],
        "outputs": [
            "SchedulerDaemon loop",
            "runtime DAG iterator with fairness ordering",
            "RecoveryReconciler for expired leases and pending results",
            "InterventionClassifier with reason categories",
        ],
        "allowed_scope": [
            "Classify non-runtime DAGs as query-only/no scheduling write",
            "Record intervention decisions before readiness",
            "Reconcile expired rights before dispatch",
        ],
        "forbidden_scope": ["Create jobs before intervention classification", "Dispatch non-runtime DAGs", "Infer route business success"],
        "acceptance": [
            "Mixed runtime/non-runtime fixtures produce query-only records for non-runtime DAGs",
            "Each runtime pass records exactly one primary intervention reason before scheduling",
            "route_exhausted never emits business_success/project_done",
        ],
        "verification": ["Review daemon control flow against FLOW-STEP refs", "Review fixture coverage expectations from scheduler-runtime-fixtures.json"],
        "stop_conditions": ["Runtime DAG state categories are contradictory or incomplete"],
        "dependencies": ["TASK-003"],
        "fixture_dir": "tasks/design/fixtures/TASK-005",
        "prompt_path": "tasks/design/fixtures/TASK-005/prompt.md",
        "agents_path": "tasks/design/fixtures/TASK-005/AGENTS.md",
        "claude_path": "tasks/design/fixtures/TASK-005/CLAUDE.md",
    },
    {
        "task_id": "TASK-006",
        "title": "Design deterministic readiness, fairness, and dispatch candidate calculation",
        "task_type": "detailed_design",
        "source_refs": ["REQ-016", "REQ-022", "DCT-019", "TECH-011", "TECH-015", "VER-016", "VER-022"],
        "inputs": ["TASK-005 intervention decisions", "TASK-003 RuntimeStore reads", "TASK-002 domain types"],
        "outputs": [
            "ReadinessEngine",
            "DispatchCandidate builder",
            "capacity/backpressure decisions",
            "blocked/deferred-ready audit reason generation",
        ],
        "allowed_scope": [
            "Evaluate dependency completion, node state, permissions, active lease, retry, global capacity, per-DAG capacity",
            "Emit deterministic decision reasons",
        ],
        "forbidden_scope": ["Persist jobs or leases", "Invoke Executor", "Accept results"],
        "acceptance": [
            "Only fully ready nodes become DispatchCandidate ready",
            "Capacity denial records deferred-ready",
            "No readiness decision depends on subjective text",
        ],
        "verification": ["Review readiness rules against DCT-019 and TECH-011", "Review fixture coverage plan for dependencies, block, lease, permission, retry, capacity"],
        "stop_conditions": ["DAG topology source is unavailable or contradictory"],
        "dependencies": ["TASK-005"],
        "fixture_dir": "tasks/design/fixtures/TASK-006",
        "prompt_path": "tasks/design/fixtures/TASK-006/prompt.md",
        "agents_path": "tasks/design/fixtures/TASK-006/AGENTS.md",
        "claude_path": "tasks/design/fixtures/TASK-006/CLAUDE.md",
    },
    {
        "task_id": "TASK-007",
        "title": "Design dispatch service, job-instance.v1 mapping, leases, fencing, and Executor gateway",
        "task_type": "detailed_design",
        "source_refs": ["REQ-018", "REQ-020", "DCT-010", "DCT-017", "DCT-018", "TECH-012", "TECH-013", "STOP-007"],
        "inputs": ["TASK-006 DispatchCandidate", "TASK-003 RuntimeStore transaction boundary", "Executor job-instance.v1 contract from SRC-005"],
        "outputs": [
            "DispatchService",
            "job-instance.v1 mapper",
            "lease and monotonic fencing token creation",
            "job control directory writer",
            "ExecutorGateway for spec-executor command invocation",
        ],
        "allowed_scope": [
            "Persist job/lease/fencing/audit before external invocation",
            "Write job-instance JSON and invoke exact DCT-018 boundary when provided",
            "Capture stdout/stderr/exit code as invocation evidence",
        ],
        "forbidden_scope": [
            "Treat missing spec-executor as success",
            "Mark node delivered from command exit",
            "Bypass job-instance.v1 mapping",
        ],
        "acceptance": [
            "Generated job-instance contains required job-instance.v1 fields and DAG/node/job/lease metadata",
            "Duplicate scheduling_key cannot create a second active job",
            "Missing spec-executor fails integration precondition or marks job failed without node delivery",
        ],
        "verification": ["Review dispatch design against job-instance.v1 and lease/fencing refs", "Review golden fixture expectations for job-instance JSON"],
        "stop_conditions": ["Required spec-executor boundary is unavailable for final runtime acceptance"],
        "dependencies": ["TASK-006"],
        "fixture_dir": "tasks/design/fixtures/TASK-007",
        "prompt_path": "tasks/design/fixtures/TASK-007/prompt.md",
        "agents_path": "tasks/design/fixtures/TASK-007/AGENTS.md",
        "claude_path": "tasks/design/fixtures/TASK-007/CLAUDE.md",
    },
    {
        "task_id": "TASK-008",
        "title": "Design Executor result intake, validation, state transitions, and stale-result defense",
        "task_type": "detailed_design",
        "source_refs": ["REQ-019", "REQ-020", "DCT-011", "DCT-012", "STATE-004", "STOP-002", "STOP-003", "STOP-008", "VER-019", "VER-020"],
        "inputs": ["TASK-003 RuntimeStore transactions", "TASK-007 job/lease/fencing records", "executor-result-samples.json"],
        "outputs": [
            "ResultIntake service",
            "evidence validation rules",
            "accepted/rejected/expired result decisions",
            "state transition service for job/node/lease/result",
        ],
        "allowed_scope": [
            "Validate executor identity, job id, lease id, fencing token, node version, evidence refs, mechanical checks",
            "Advance node only after accepted result",
            "Reject stale/missing/failed evidence without node delivery",
        ],
        "forbidden_scope": [
            "Treat Executor completed as delivery",
            "Accept stale node version or fencing token",
            "Advance dependent nodes in the same transaction as acceptance unless HLD explicitly authorizes it",
        ],
        "acceptance": [
            "Accepted sample advances node through valid transition",
            "Missing evidence sample is rejected",
            "Stale token/version sample is rejected",
            "Duplicate result submission does not duplicate accepted transition",
        ],
        "verification": ["Review result intake design against executor-result samples", "Review state transition and stale-result defense coverage"],
        "stop_conditions": ["Evidence contract cannot be evaluated mechanically"],
        "dependencies": ["TASK-007"],
        "fixture_dir": "tasks/design/fixtures/TASK-008",
        "prompt_path": "tasks/design/fixtures/TASK-008/prompt.md",
        "agents_path": "tasks/design/fixtures/TASK-008/AGENTS.md",
        "claude_path": "tasks/design/fixtures/TASK-008/CLAUDE.md",
    },
    {
        "task_id": "TASK-009",
        "title": "Design acceptance-run, audit retrieval, and end-to-end fixture verification",
        "task_type": "detailed_design",
        "source_refs": ["DCT-014", "BAR-003", "MET-004", "VER-014", "VER-017", "VER-018", "VER-019", "VER-020", "VER-021", "VER-022", "VER-023", "VER-024"],
        "inputs": ["TASK-004 API", "TASK-005 loop", "TASK-006 readiness", "TASK-007 dispatch/executor", "TASK-008 result intake", "docs/acceptance/scheduler_acceptance.py"],
        "outputs": [
            "spec-scheduler acceptance-run command design",
            "acceptance artifact writer design",
            "audit retrieval coverage design",
            "end-to-end real fixture verification design",
        ],
        "allowed_scope": [
            "Specify acceptance-run command consumed by docs/acceptance/scheduler_acceptance.py",
            "Specify expected artifacts under provided output-dir",
            "Specify coverage for API, main loop, readiness, dispatch, result validation, idempotency, recovery, fairness, permissions, audit, exhaustion",
        ],
        "forbidden_scope": ["Use mock/stub/fake/simulated/synthetic acceptance inputs", "Skip expected artifact generation"],
        "acceptance": [
            "Design document defines the real-fixture acceptance runner success criteria",
            "Design document lists all expected artifact paths",
            "Design document specifies scheduler-run-report.json domain pass reporting",
            "Design document specifies audit-events.jsonl coverage for dispatch, no_intervention, accept, reject, defer, recover, route_exhausted",
        ],
        "verification": [
            "Review the proposed acceptance command and artifact contract against docs/acceptance/scheduler_acceptance.py"
        ],
        "stop_conditions": ["spec-scheduler command is not callable", "Required real fixtures are missing"],
        "dependencies": ["TASK-004", "TASK-005", "TASK-006", "TASK-007", "TASK-008"],
        "fixture_dir": "tasks/design/fixtures/TASK-009",
        "prompt_path": "tasks/design/fixtures/TASK-009/prompt.md",
        "agents_path": "tasks/design/fixtures/TASK-009/AGENTS.md",
        "claude_path": "tasks/design/fixtures/TASK-009/CLAUDE.md",
    },
    {
        "task_id": "TASK-010",
        "title": "Accept the completed detailed design document set",
        "task_type": "design_acceptance",
        "source_refs": ["REQ-001..REQ-024", "DCT-014..DCT-020", "TECH-008..TECH-015", "VER-014..VER-024"],
        "inputs": [
            "docs/design/rust-implementation-design.md",
            "docs/design/TASK-001-rust-workspace-entrypoints-design.md",
            "docs/design/TASK-002-domain-state-schema-design.md",
            "docs/design/TASK-003-runtime-store-audit-design.md",
            "docs/design/TASK-004-http-api-control-plane-design.md",
            "docs/design/TASK-005-daemon-recovery-intervention-design.md",
            "docs/design/TASK-006-readiness-fairness-design.md",
            "docs/design/TASK-007-dispatch-executor-gateway-design.md",
            "docs/design/TASK-008-result-intake-state-transition-design.md",
            "docs/design/TASK-009-acceptance-audit-e2e-design.md",
        ],
        "outputs": [
            "whole detailed design document set acceptance report",
            "coverage and traceability review",
            "cross-document consistency review",
            "quality gate result with pass/fail/blocker findings",
        ],
        "allowed_scope": [
            "Review the completed detailed design documents against PRD/HLD, contract, planning DAG, and good detailed design criteria",
            "Record findings, blockers, and required fixes in the acceptance report",
            "Confirm no implementation files were changed by design tasks",
        ],
        "forbidden_scope": [
            "Write product code",
            "Rewrite all design documents instead of reporting findings",
            "Approve missing, contradictory, untraceable, or implementation-thin design documents",
        ],
        "acceptance": [
            "Acceptance report covers every detailed design document and every current-phase obligation",
            "Acceptance report records pass/fail/blocker status and concrete required fixes",
            "Acceptance report confirms documentation-only compliance",
        ],
        "verification": [
            "Review all docs/design/*.md detailed design documents",
            "Check coverage against tasks/design/design-planning.json and PRD/HLD refs",
            "Check no implementation files changed as part of design work",
        ],
        "stop_conditions": [
            "Any required detailed design document is missing",
            "A design document cannot be accepted without inventing missing PRD/HLD facts",
        ],
        "dependencies": ["TASK-001", "TASK-002", "TASK-003", "TASK-004", "TASK-005", "TASK-006", "TASK-007", "TASK-008", "TASK-009"],
        "fixture_dir": "tasks/design/fixtures/TASK-010",
        "prompt_path": "tasks/design/fixtures/TASK-010/prompt.md",
        "agents_path": "tasks/design/fixtures/TASK-010/AGENTS.md",
        "claude_path": "tasks/design/fixtures/TASK-010/CLAUDE.md",
    },
]

DESIGN_TASK_SPECS = {
    "TASK-001": {
        "title": "Design Rust workspace, configuration, and process entrypoints",
        "design_doc_path": "docs/design/TASK-001-rust-workspace-entrypoints-design.md",
    },
    "TASK-002": {
        "title": "Design domain types, state machines, and SQLite schema",
        "design_doc_path": "docs/design/TASK-002-domain-state-schema-design.md",
    },
    "TASK-003": {
        "title": "Design RuntimeStore transaction and audit boundary",
        "design_doc_path": "docs/design/TASK-003-runtime-store-audit-design.md",
    },
    "TASK-004": {
        "title": "Design localhost HTTP JSON API control plane",
        "design_doc_path": "docs/design/TASK-004-http-api-control-plane-design.md",
    },
    "TASK-005": {
        "title": "Design daemon loop, recovery reconciliation, and intervention classification",
        "design_doc_path": "docs/design/TASK-005-daemon-recovery-intervention-design.md",
    },
    "TASK-006": {
        "title": "Design deterministic readiness, fairness, and dispatch candidate calculation",
        "design_doc_path": "docs/design/TASK-006-readiness-fairness-design.md",
    },
    "TASK-007": {
        "title": "Design dispatch service, job-instance.v1 mapping, leases, fencing, and Executor gateway",
        "design_doc_path": "docs/design/TASK-007-dispatch-executor-gateway-design.md",
    },
    "TASK-008": {
        "title": "Design Executor result intake, validation, state transitions, and stale-result defense",
        "design_doc_path": "docs/design/TASK-008-result-intake-state-transition-design.md",
    },
    "TASK-009": {
        "title": "Design acceptance-run, audit retrieval, and end-to-end fixture verification",
        "design_doc_path": "docs/design/TASK-009-acceptance-audit-e2e-design.md",
    },
    "TASK-010": {
        "title": "Accept the completed detailed design document set",
        "design_doc_path": "docs/design/TASK-010-detailed-design-acceptance-review.md",
        "task_type": "design_acceptance",
    },
}

for task in tasks:
    spec = DESIGN_TASK_SPECS[task["task_id"]]
    design_subjects = task["outputs"]
    implementation_forbidden_scope = task["forbidden_scope"]
    task["title"] = spec["title"]
    task["task_type"] = spec.get("task_type", "detailed_design")
    task["design_doc_path"] = spec["design_doc_path"]
    task["design_subjects"] = design_subjects
    task["outputs"] = [
        f"Detailed design document saved exactly at `{task['design_doc_path']}`",
        "Document sections: source refs, scope boundary, proposed Rust modules/traits/types, control flow, data flow, state/persistence, errors/diagnostics, security/permissions, observability, verification plan, risks, and handoff notes",
        "Document covers these design subjects: " + "; ".join(design_subjects),
    ]
    task["allowed_scope"] = [
        "Produce detailed design documentation only; do not implement, scaffold, wire, or modify product code",
        f"Write the task deliverable exactly to `{task['design_doc_path']}`",
        "Use PRD/HLD, contract, semantic review, acceptance fixtures, and existing design docs as the only sources of product facts",
        "Specify concrete Rust design decisions, interfaces, data contracts, state transitions, and verification strategy needed for later implementation",
        "Record unsupported or contradictory details as blockers/open questions instead of inventing implementation facts",
    ]
    task["forbidden_scope"] = [
        "Modify production source code, tests, build manifests, schemas, migrations, runtime scripts, or generated runtime artifacts",
        "Run implementation commands as proof of completion; commands may be listed only as a proposed verification plan in the design document",
        "Create placeholder code, stubs, scaffolding, migrations, or executable acceptance artifacts",
        *implementation_forbidden_scope,
    ]
    task["acceptance"] = [
        f"`{task['design_doc_path']}` exists and is a detailed design document, not implementation code",
        "Document traces all material claims to PRD/HLD, contract, semantic review, target evidence, or explicit open questions",
        "Document is specific enough for a later developer to implement without rediscovering control flow, data flow, interfaces, state, errors, and verification strategy",
        "No production code, tests, manifests, schemas, migrations, runtime scripts, or generated runtime artifacts are changed",
    ]
    task["verification"] = [
        f"Confirm the detailed design file path is exactly `{task['design_doc_path']}`",
        "Review the document for PRD/HLD traceability, boundary compliance, control-flow completeness, data-flow completeness, and Rust design specificity",
        "Confirm no product code, tests, build manifests, schemas, migrations, runtime scripts, or generated runtime artifacts were modified",
    ]

edges = []
for task in tasks:
    for dep in task["dependencies"]:
        reason = {
            ("TASK-001", "TASK-002"): "Domain types and SQLite schema need the crate/module layout and dependency baseline from TASK-001.",
            ("TASK-002", "TASK-003"): "RuntimeStore consumes schema, state enums, and domain row mappings from TASK-002.",
            ("TASK-003", "TASK-004"): "HTTP API handlers call RuntimeStore transaction/query APIs from TASK-003.",
            ("TASK-003", "TASK-005"): "Daemon loop and intervention classification must read/write runtime state and audit events through TASK-003.",
            ("TASK-005", "TASK-006"): "Readiness can run only after intervention classification selects schedulable_nodes or related reasons.",
            ("TASK-006", "TASK-007"): "DispatchService consumes DispatchCandidate records produced by ReadinessEngine.",
            ("TASK-007", "TASK-008"): "ResultIntake validates results against job, lease, fencing, and node-version records created by dispatch.",
            ("TASK-004", "TASK-009"): "Acceptance-run and API checks require implemented HTTP control plane.",
            ("TASK-005", "TASK-009"): "Acceptance-run covers runtime loop, no_intervention, recovery, and exhaustion behavior.",
            ("TASK-006", "TASK-009"): "Acceptance-run covers readiness, capacity, and deferred-ready behavior.",
            ("TASK-007", "TASK-009"): "Acceptance-run verifies job-instance, lease, fencing, and Executor gateway artifacts.",
            ("TASK-008", "TASK-009"): "Acceptance-run verifies accepted/rejected result decisions and state transitions.",
            ("TASK-001", "TASK-010"): "Final design acceptance must review the Rust workspace and entrypoint design document.",
            ("TASK-002", "TASK-010"): "Final design acceptance must review the domain, state, and schema design document.",
            ("TASK-003", "TASK-010"): "Final design acceptance must review the RuntimeStore and audit design document.",
            ("TASK-004", "TASK-010"): "Final design acceptance must review the HTTP API control-plane design document.",
            ("TASK-005", "TASK-010"): "Final design acceptance must review the daemon, recovery, and intervention design document.",
            ("TASK-006", "TASK-010"): "Final design acceptance must review the readiness, fairness, and dispatch-candidate design document.",
            ("TASK-007", "TASK-010"): "Final design acceptance must review the dispatch, lease, fencing, and Executor gateway design document.",
            ("TASK-008", "TASK-010"): "Final design acceptance must review the result intake and state transition design document.",
            ("TASK-009", "TASK-010"): "Final design acceptance must review the acceptance-run, audit, and E2E verification design document.",
        }[(dep, task["task_id"])]
        refs = list(dict.fromkeys([*task["source_refs"][:4], *next(t for t in tasks if t["task_id"] == dep)["source_refs"][:4]]))
        edges.append({"from": dep, "to": task["task_id"], "reason": reason, "source_refs": refs})

coverage = [
    {"obligation": "Scheduler ownership boundary and non-goals", "refs": ["REQ-001", "OOS-001", "STOP-001", "STOP-002"], "task_ids": ["TASK-001", "TASK-004", "TASK-005", "TASK-007", "TASK-008"]},
    {"obligation": "Authoritative persisted state and audit", "refs": ["REQ-015", "REQ-023", "DCT-016", "DCT-020"], "task_ids": ["TASK-002", "TASK-003", "TASK-009"]},
    {"obligation": "HTTP API control plane and permissions", "refs": ["REQ-014", "REQ-024", "DCT-015", "STOP-008"], "task_ids": ["TASK-004", "TASK-009"]},
    {"obligation": "Runtime DAG loop and intervention-first scheduling", "refs": ["REQ-012", "REQ-013", "REQ-017", "FLOW-004"], "task_ids": ["TASK-005", "TASK-009"]},
    {"obligation": "Readiness, fairness, capacity, and backpressure", "refs": ["REQ-016", "REQ-022", "DCT-019", "TECH-015"], "task_ids": ["TASK-006", "TASK-009"]},
    {"obligation": "Executor dispatch, job-instance.v1, leases, fencing", "refs": ["REQ-018", "REQ-020", "DCT-010", "DCT-018", "TECH-012", "TECH-013"], "task_ids": ["TASK-007", "TASK-009"]},
    {"obligation": "Executor result validation and state transitions", "refs": ["REQ-019", "DCT-011", "DCT-012", "STATE-004", "STOP-003"], "task_ids": ["TASK-008", "TASK-009"]},
    {"obligation": "Recovery and idempotency", "refs": ["REQ-020", "REQ-021", "TECH-006", "TECH-013"], "task_ids": ["TASK-003", "TASK-005", "TASK-007", "TASK-008", "TASK-009"]},
    {"obligation": "Real acceptance matrix and artifacts", "refs": ["DCT-014", "BAR-003", "MET-004", "VER-014..VER-024"], "task_ids": ["TASK-009"]},
    {"obligation": "Detailed design document set acceptance", "refs": ["REQ-001..REQ-024", "DCT-014..DCT-020", "TECH-008..TECH-015", "VER-014..VER-024"], "task_ids": ["TASK-010"]},
]

planning_review_stages = [
    {
        "stage_id": "overall_planning",
        "stage": "Generate source-backed overall design plan from PRD/HLD",
        "status": "pass",
        "checks": [
            "All docs/ PRD, HLD, contract, semantic review, and acceptance sources are inventoried.",
            "Current-phase scope, non-goals, Rust stack, control flow, data flow, interfaces, state, risks, and acceptance obligations are identified.",
            "Unsupported facts are recorded as warnings or external dependencies instead of invented.",
        ],
        "findings": [
            "Overall planning is ready for task decomposition.",
            "Rust source/Cargo.toml and spec-executor are not present, so implementation-specific verification remains an external dependency.",
        ],
        "evidence_refs": ["docs/agent-prd.md", "docs/human-prd.md", "docs/high-level-design.md", "docs/high-level-design.json", "docs/contract-envelope.json", "docs/hld-semantic-review.json"],
    },
    {
        "stage_id": "task_formation",
        "stage": "Form independent documentation-only detailed design tasks",
        "status": "pass",
        "checks": [
            "Each task has one exact docs/design/*.md design_doc_path.",
            "Each task is documentation-only and forbids code/test/manifest/schema/migration/runtime changes.",
            "Each task has source refs, inputs, outputs, review checks, stop conditions, and handoff expectations.",
        ],
        "findings": [
            "Nine detailed design tasks and one final design acceptance task are formed.",
            "Tasks are scoped by design ownership rather than implementation activity.",
        ],
        "evidence_refs": [t["task_id"] for t in tasks],
    },
    {
        "stage_id": "single_task_review",
        "stage": "Review each task for logic and completeness",
        "status": "pass",
        "checks": [
            "Task deliverables are detailed design documents, not code changes.",
            "Task scopes are coherent and non-overlapping enough for independent execution.",
            "Task fixtures include prompt.md, AGENTS.md, and CLAUDE.md with exact document paths and no-code constraints.",
        ],
        "findings": [
            "Every task can be executed as an isolated detailed design document task.",
            "TASK-004 and TASK-008 are separated by ResultIntakePort boundary to avoid hidden implementation coupling.",
        ],
        "evidence_refs": [t["fixture_dir"] for t in tasks],
    },
    {
        "stage_id": "global_dag_review",
        "stage": "Review overall task completeness and dependency correctness",
        "status": "pass",
        "checks": [
            "DAG is acyclic.",
            "Every edge has a semantic reason.",
            "All current-phase obligations map to at least one task or explicit warning/dependency.",
            "Parallel group claims are dependency-safe.",
        ],
        "findings": [
            "DAG has 10 nodes and 21 edges.",
            "TASK-010 depends on all nine detailed design tasks.",
        ],
        "evidence_refs": [e["from"] + "->" + e["to"] for e in edges],
    },
    {
        "stage_id": "artifact_generation",
        "stage": "Generate planning JSON, overall design document, and per-task fixtures",
        "status": "pass",
        "checks": [
            "Planning JSON is written under the requested planning output root.",
            "Overall detailed design document is written under docs/design/.",
            "Every task fixture is written under the requested planning output root.",
        ],
        "findings": [
            "Requested planning output root is tasks/design.",
            "Detailed design document root remains docs/design.",
        ],
        "evidence_refs": ["tasks/design/design-planning.json", "docs/design/rust-implementation-design.md"],
    },
    {
        "stage_id": "final_design_acceptance",
        "stage": "Add final acceptance task for the completed detailed design document set",
        "status": "pass",
        "checks": [
            "Exactly one final design acceptance task exists.",
            "Final acceptance task depends on every detailed design task.",
            "Final acceptance task writes its report under docs/design/ and forbids code changes.",
        ],
        "findings": [
            "TASK-010 is the final design acceptance task.",
            "TASK-010 writes docs/design/TASK-010-detailed-design-acceptance-review.md.",
        ],
        "evidence_refs": ["TASK-010", "docs/design/TASK-010-detailed-design-acceptance-review.md"],
    },
]

planning = {
    "planning_status": "ready",
    "output_root": PLANNING_OUTPUT_ROOT,
    "detailed_design_root": DETAILED_DESIGN_ROOT,
    "rust_design_path": f"{DETAILED_DESIGN_ROOT}/rust-implementation-design.md",
    "source_inventory": source_inventory,
    "prd_hld_interpretation": {
        "product": "Scheduler daemon for runtime DAG orchestration",
        "current_phase": "PHASE-002 implementation planning from ready Phase 1 PRD/HLD artifacts",
        "hld_status": "ready",
        "semantic_review_status": "pass",
        "core_boundary": "Scheduler advances existing runtime DAGs only; it does not design routes, create nodes, run task commands directly, mutate deliverables, or infer business success.",
        "acceptance_policy": "Real fixtures only; mock, stub, fake, simulated, synthetic, placeholder, or deferred acceptance inputs are forbidden.",
    },
    "design_scope": {
        "in_scope": [
            "Rust daemon/API implementation plan",
            "SQLite WAL runtime store",
            "runtime DAG loop and intervention classification",
            "readiness, fairness, dispatch, leases, fencing",
            "spec-executor boundary integration",
            "Executor result intake and audit",
            "acceptance-run command and real fixture verification",
            "final acceptance of the detailed design document set",
        ],
        "out_of_scope": [
            "DAG route design",
            "new route node generation",
            "direct task provider command execution by Scheduler",
            "deliverable mutation",
            "business-success inference from route exhaustion",
        ],
    },
    "rust_stack": {
        "confirmed_from_hld": {
            "language": "Rust target implementation",
            "api_transport": "localhost HTTP JSON on 127.0.0.1",
            "storage": "SQLite WAL",
            "transaction_model": "one DAG-runtime transaction per control-loop decision; external Executor invocation after commit",
            "executor_boundary": "spec-executor run --job-instance <job-instance.json> --result-output <executor-result.json>",
            "audit": "append-only audit_event plus current-state tables",
            "fairness": "round-robin runtime DAG iteration with global/per-DAG capacity budgets",
        },
        "implementation_choices_to_finalize_in_task_001": [
            "HTTP server crate/framework",
            "SQLite access crate and migration approach",
            "CLI/config parsing crate",
            "error type/reporting crate pattern",
            "tracing/logging crate setup",
            "time/clock abstraction for deterministic tests",
        ],
        "not_verified_from_source": [
            "No Cargo.toml or Rust source exists in target at planning time.",
            "No spec-scheduler binary exists yet.",
            "HLD records that spec-executor executable was not found and must be provided by implementation/integration setup.",
        ],
    },
    "planning_review_stages": planning_review_stages,
    "tasks": tasks,
    "dag": {
        "nodes": [{"task_id": t["task_id"], "title": t["title"], "task_type": t["task_type"]} for t in tasks],
        "edges": edges,
        "parallel_groups": [
            {
                "group_id": "PG-001",
                "task_ids": ["TASK-004", "TASK-005"],
                "status": "parallel_safe_after_dependencies",
                "rationale": "Both consume RuntimeStore APIs from TASK-003 but work on separate API and loop/classifier surfaces. Coordinate only on shared service interfaces.",
                "conflict_refs": [],
            }
        ],
        "cycle_check": {"status": "pass", "cycles": []},
    },
    "fixtures": [
        {
            "task_id": t["task_id"],
            "fixture_dir": t["fixture_dir"],
            "prompt_path": t["prompt_path"],
            "agents_path": t["agents_path"],
            "claude_path": t["claude_path"],
        }
        for t in tasks
    ],
    "coverage_matrix": coverage,
    "planning_gate_report": [
        {"gate": "source_readiness", "status": "pass", "evidence_refs": ["docs/agent-prd.md", "docs/human-prd.md", "docs/intake-notes.md", "docs/high-level-design.md", "docs/high-level-design.json", "docs/contract-envelope.json"], "summary": "PRD, HLD, contract, semantic review, intake notes, and acceptance fixtures are present and inventoried."},
        {"gate": "traceability", "status": "pass", "evidence_refs": ["REQ-001..REQ-024", "DCT-014..DCT-020", "TECH-008..TECH-015"], "summary": "Tasks and coverage map to PRD/HLD refs."},
        {"gate": "rust_stack_readiness", "status": "warning", "evidence_refs": ["TECH-008", "TECH-009", "TECH-012"], "summary": "HLD defines Rust-oriented implementation choices, but target has no Cargo.toml/source and spec-executor binary is absent by HLD note."},
        {"gate": "control_flow_readiness", "status": "pass", "evidence_refs": ["FLOW-STEP-001..FLOW-STEP-011"], "summary": "Planning covers API/tick intake through exhaustion."},
        {"gate": "data_flow_readiness", "status": "pass", "evidence_refs": ["DATAFLOW-001..DATAFLOW-008", "DATA-007..DATA-011"], "summary": "Planning covers API input, runtime snapshot, intervention decision, readiness, dispatch, Executor invocation, result intake, and audit."},
        {"gate": "technical_decision_readiness", "status": "pass", "evidence_refs": ["TECH-008..TECH-015"], "summary": "Tasks preserve HLD technical selections."},
        {"gate": "staged_review_readiness", "status": "pass", "evidence_refs": [s["stage_id"] for s in planning_review_stages], "summary": "Harness-style overall planning, task formation, single-task review, global DAG review, artifact generation, and final acceptance stages are recorded and pass."},
        {"gate": "dag_soundness", "status": "pass", "evidence_refs": [e["from"] + "->" + e["to"] for e in edges], "summary": "DAG is acyclic and every edge has a reason."},
        {"gate": "parallel_safety", "status": "pass", "evidence_refs": ["PG-001"], "summary": "Only API and loop/classifier are marked parallel-safe after RuntimeStore dependency; no independent fixture conflicts are hidden."},
        {"gate": "task_fixture_readiness", "status": "pass", "evidence_refs": [t["fixture_dir"] for t in tasks], "summary": "Every ready task has prompt.md, AGENTS.md, and CLAUDE.md fixture paths."},
        {"gate": "design_acceptance_task", "status": "pass", "evidence_refs": ["TASK-010"], "summary": "Final design acceptance task depends on every detailed design task and writes a review report under docs/design."},
        {"gate": "no_starter_prompt_template", "status": "pass", "evidence_refs": [], "summary": "No standalone starter prompt template is produced; prompt.md files are per-task fixtures."},
    ],
    "external_dependencies": [
        {
            "dependency": "Rust toolchain and package registry access",
            "needed_by": ["TASK-001", "all cargo verification tasks"],
            "status": "not verified in target repository",
            "handling": "TASK-001 must verify the toolchain before selecting and wiring crates.",
        },
        {
            "dependency": "spec-executor command implementing DCT-018",
            "needed_by": ["TASK-007", "TASK-009"],
            "status": "absent according to HLD planning evidence",
            "handling": "TASK-007 may implement the gateway and failure/precondition behavior, but final runtime acceptance cannot pass until this executable boundary is provided.",
        },
    ],
    "open_questions": [],
    "required_fixes": [],
    "warnings": [
        "Target project currently has no Rust source files or Cargo.toml, so local Rust conventions are derived from HLD rather than existing code.",
        "Final runtime acceptance remains blocked until an implementation provides spec-scheduler and the required spec-executor boundary.",
    ],
}


rust_design = """\
# Rust Implementation Design

## Architecture And Crate Boundaries

The implementation should be a Rust daemon/binary named `spec-scheduler` with narrow modules for configuration, HTTP API, runtime store, daemon loop, intervention classification, readiness, dispatch, Executor gateway, result intake, recovery, audit, and acceptance-run support.

Suggested crate/module surface:

| Module | Responsibility | Primary Refs |
| --- | --- | --- |
| `config` | Bind address, SQLite path, state directory, capacity, lease timeout, executor command, acceptance paths. | TECH-008, TECH-009, DCT-018 |
| `domain` | Runtime IDs, node/job/lease/result/audit types, state enums, reason codes, DTO conversions. | DATA-007..DATA-011, STATE-003, STATE-004 |
| `store` | SQLite WAL schema, transactions, compare-and-update, append-only audit. | DCT-016, DCT-017, DCT-020 |
| `api` | HTTP JSON endpoints, permission guards, and service-port delegation boundaries. | DCT-015, REQ-014, REQ-024 |
| `daemon` | Runtime DAG iteration, tick handling, shutdown-safe loop. | REQ-013, TECH-015 |
| `intervention` | pending_result, expired_lease, schedulable_nodes, blocked_recheck, recovery_reconcile, route_exhausted, no_intervention. | REQ-017, FLOW-004 |
| `readiness` | Dependency, state, permission, lease, retry, capacity decisions into DispatchCandidate. | DCT-019, TECH-011 |
| `dispatch` | Job/lease/fencing creation, job-instance.v1 writer, idempotent scheduling key. | REQ-018, REQ-020, DCT-010 |
| `executor_gateway` | File-backed `spec-executor` invocation and process evidence capture. | DCT-018, TECH-012 |
| `result_intake` | Executor result validation, accepted/rejected decisions, state advancement, and implementation of the API `ResultIntakePort`. | DCT-011, DCT-012 |
| `recovery` | Startup/loop reconciliation of expired leases, pending results, incomplete invocations. | REQ-021 |
| `acceptance` | `acceptance-run` command consumed by `docs/acceptance/scheduler_acceptance.py`. | DCT-014, VER-014..VER-024 |

## Control Flow

1. API request or daemon timer creates a causation ID.
2. RuntimeStore opens a SQLite transaction and reads a DAG runtime snapshot.
3. Non-runtime DAGs return query-only or no-op behavior without scheduling writes.
4. Recovery reconciles expired leases and pending results before new dispatch.
5. InterventionClassifier records exactly one intervention reason before readiness.
6. ReadinessEngine builds DispatchCandidate values only for fully ready nodes.
7. DispatchService commits scheduler_job, lease_record, fencing_token, job-instance.v1 path, and audit event.
8. ExecutorGateway invokes `spec-executor` after commit and records stdout/stderr/exit/result-output evidence.
9. ResultIntake validates identity, job, lease, fencing token, node version, evidence refs, and mechanical checks.
10. StateTransitionService advances nodes only after accepted evidence.
11. Scheduler records route_exhausted without business success when no active jobs and no schedulable nodes remain.

## Data Flow

HTTP JSON input and daemon ticks become transaction commands. RuntimeStore converts SQLite rows into `DagRuntimeSnapshot`. Intervention decisions are persisted before readiness. Readiness transforms snapshots into `DispatchCandidate` records. Dispatch transforms candidates into durable jobs, leases, fencing tokens, job-instance files, and dispatch audit events. Executor invocation transforms a job-instance file into process evidence and an Executor result output. Result intake transforms result output into accepted/rejected decisions and state transitions. Every state-changing decision appends audit evidence.

## Data Types And Contracts

Key Rust data types should include:

- `DagRuntimeSnapshot`
- `RuntimeState`
- `NodeRuntimeState`
- `DispatchCandidate`
- `SchedulerJob`
- `LeaseRecord`
- `FencingToken`
- `JobInstanceV1`
- `ExecutorInvocationRecord`
- `ExecutorResultEvidence`
- `ResultDecision`
- `AuditEvent`
- `InterventionDecision`

DTOs for HTTP and Executor result intake should convert into domain types at validation boundaries; internal services should avoid consuming raw unvalidated JSON.

## Interface Contracts

- HTTP JSON endpoints from DCT-015.
- API endpoint handlers must delegate result validation and state transitions through a `ResultIntakePort` or equivalent service interface implemented by `result_intake`.
- SQLite WAL store and transaction boundary from DCT-016/DCT-017.
- Required Executor command: `spec-executor run --job-instance <job-instance.json> --result-output <executor-result.json>`.
- Result intake API `POST /v1/executor-results`.
- Acceptance runner command from `docs/acceptance/scheduler_acceptance.py`.

## State And Persistence

SQLite current-state tables own `dag_runtime`, `node_runtime`, `scheduler_job`, `lease_record`, `executor_result`, `intervention_decision`, and `route_exhaustion`. `audit_event` is append-only and inserted in the same transaction as the associated decision. `update_version` protects current-state writes. A unique active `scheduling_key` prevents duplicate active dispatch.

## Error Handling And Diagnostics

Use explicit error categories for invalid caller, unauthorized runtime/node/Executor, stale update version, duplicate scheduling key, invalid transition, missing evidence, stale fencing token, stale node version, command failure, and acceptance artifact failure. User-facing diagnostics should preserve reason codes and causation IDs. Logs/tracing should record runtime ID, node ID, job ID, lease ID, intervention reason, and audit event ID where available.

## Async And Concurrency

The HLD does not mandate a specific async runtime or Rust crate set. TASK-001 must finalize the concrete crate choices for HTTP, SQLite access, CLI/config, error handling, tracing, and time while preserving HLD choices. If the HTTP framework requires async, use a single writer boundary around SQLite transactions and avoid holding DB transactions across external Executor calls. Scheduler fairness is deterministic: iterate by `last_checked_at` then `dag_runtime_id`, enforce global and per-DAG capacity, and record deferred-ready when capacity denies dispatch.

## Key Technical Decisions

- Localhost HTTP JSON API on 127.0.0.1.
- SQLite WAL durable runtime store.
- One DAG-runtime transaction per control-loop decision.
- Deterministic readiness evaluation.
- File-backed `spec-executor` command boundary.
- Monotonic fencing tokens.
- Append-only audit plus current-state tables.
- Round-robin runtime DAG fairness with capacity budgets.
- Concrete Rust library choices are not HLD-level product facts; record them in TASK-001 and keep them replaceable behind module/service boundaries.

## Security And Permissions

Permission checks happen before dispatch or result acceptance. Unauthorized API caller, DAG/runtime, node, Executor identity, lease, fencing token, or evidence access must be rejected without state advancement and must be audited. Route-definition mutation through the Scheduler API is forbidden.

## Observability

Every dispatch, no_intervention, accept, reject, expire, block, recover, defer, and route_exhausted decision must have an audit event. Process invocation evidence must capture argv, stdout, stderr, exit code, job-instance path, result-output path, and causation ID.

## Test And Acceptance Design

Unit tests cover domain conversions, state transitions, readiness, fencing, result validation, and scheduling keys. Integration tests use a temporary SQLite database. Acceptance is the real command:

```bash
python3 docs/acceptance/scheduler_acceptance.py --scheduler-command spec-scheduler --fixtures docs/acceptance/scheduler-runtime-fixtures.json --executor-results docs/acceptance/executor-result-samples.json --output-dir docs/acceptance/output/scheduler-real-acceptance-001
```

Expected artifacts:

- `scheduler-run-report.json`
- `state-transition-events.jsonl`
- `job-instances.json`
- `lease-records.json`
- `result-decisions.json`
- `audit-events.jsonl`

## Risks And Guardrails

- Guard against Scheduler becoming planner/executor through route mutation and direct command execution bans.
- Guard against Executor self-report trust by requiring evidence validation.
- Guard against duplicate dispatch through scheduling keys, leases, and fencing tokens.
- Guard against stale results through node version and current fencing token checks.
- Guard against hidden success inference by keeping route_exhausted separate from business success.
"""


def fixture_prompt(task):
    return f"""# Detailed Design Task Prompt: {task['task_id']} {task['title']}

You are working on one documentation-only detailed design task from the Scheduler design plan.

Do not implement code. Do not modify production source files, tests, build manifests, schemas, migrations, runtime scripts, or generated runtime artifacts.

## Mission

Complete only `{task['task_id']}`: {task['title']}.

Your only deliverable is the detailed design document named below:

- `{task['design_doc_path']}`

## Read First

- `docs/agent-prd.md`
- `docs/human-prd.md`
- `docs/intake-notes.md`
- `docs/high-level-design.md`
- `docs/high-level-design.json`
- `docs/contract-envelope.json`
- `{PLANNING_OUTPUT_ROOT}/design-planning.json`
- `{DETAILED_DESIGN_ROOT}/rust-implementation-design.md`
- This fixture directory: `{task['fixture_dir']}`

## Source Refs

{', '.join(task['source_refs'])}

## Allowed Scope

{chr(10).join('- ' + x for x in task['allowed_scope'])}

## Forbidden Scope

{chr(10).join('- ' + x for x in task['forbidden_scope'])}

## Required Document Output

{chr(10).join('- ' + x for x in task['outputs'])}

The document must be saved exactly at `{task['design_doc_path']}`. Any additional detailed design document created or updated while completing this task must also be saved under `{DETAILED_DESIGN_ROOT}/`.

## Review Checks

{chr(10).join('- ' + x for x in task['verification'])}

## Stop Conditions

{chr(10).join('- ' + x for x in task['stop_conditions'])}

## Handoff

Report the detailed design document path, review checks performed, unresolved design risks, and any design mismatch that requires updating `{PLANNING_OUTPUT_ROOT}` or `{DETAILED_DESIGN_ROOT}/`. Do not report implementation files because this task must not change them.
"""


def fixture_agents(task):
    return f"""# Task Agent Instructions: {task['task_id']}

## Role

You are a senior Rust design agent assigned to `{task['task_id']}`: {task['title']}. Produce only the named detailed design document for this task.

Do not implement code. Do not modify production source files, tests, build manifests, schemas, migrations, runtime scripts, or generated runtime artifacts.

## Required Reading

1. PRD/HLD under `docs/`.
2. `{PLANNING_OUTPUT_ROOT}/design-planning.json`.
3. `{DETAILED_DESIGN_ROOT}/rust-implementation-design.md`.
4. This fixture directory.

## Hard Rules

- Do not invent requirements, APIs, data fields, runtime components, or acceptance criteria.
- Stay within `{task['task_id']}` allowed scope.
- Do not perform work from other task IDs.
- Deliver exactly this task document: `{task['design_doc_path']}`.
- Preserve HLD choices: localhost HTTP JSON, SQLite WAL, single-writer transactions, deterministic readiness, spec-executor boundary, fencing tokens, append-only audit, round-robin fairness.
- Save every detailed design document created or updated by this task under `{DETAILED_DESIGN_ROOT}/`.
- If detailed design reveals a gap, record it in the design document and stop or request an update to `{PLANNING_OUTPUT_ROOT}` and `{DETAILED_DESIGN_ROOT}/` before continuing.
- Do not modify production source code, tests, build manifests, schemas, migrations, runtime scripts, or generated runtime artifacts.

## Task Scope

Allowed:

{chr(10).join('- ' + x for x in task['allowed_scope'])}

Forbidden:

{chr(10).join('- ' + x for x in task['forbidden_scope'])}

## Review Checks

{chr(10).join('- ' + x for x in task['verification'])}

## Handoff

Report the detailed design document path, task ID, review checks, and any residual risks or required design updates. Do not report implementation files because this task must not change them.
"""


def fixture_claude(task):
    return f"""# Claude Task Instructions: {task['task_id']}

Claude must follow these instructions for `{task['task_id']}`: {task['title']}.

## Role

You are a senior Rust design collaborator. Use `docs/` PRD/HLD plus `{PLANNING_OUTPUT_ROOT}` planning artifacts and `{DETAILED_DESIGN_ROOT}` detailed design documents as source of truth.

Your only deliverable is the named detailed design document: `{task['design_doc_path']}`.

## Required Reading

1. Relevant PRD/HLD refs: {', '.join(task['source_refs'])}.
2. `{PLANNING_OUTPUT_ROOT}/design-planning.json`.
3. `{DETAILED_DESIGN_ROOT}/rust-implementation-design.md`.
4. `{PLANNING_OUTPUT_ROOT}/fixtures/{task['task_id']}/prompt.md`.
5. `{PLANNING_OUTPUT_ROOT}/fixtures/{task['task_id']}/AGENTS.md`.

## Constraints

- Do not implement code.
- Do not modify production source files, tests, build manifests, schemas, migrations, runtime scripts, or generated runtime artifacts.
- Work only on `{task['task_id']}`.
- Do not silently change architecture, crate boundaries, traits, data types, state model, async/concurrency model, persistence strategy, or acceptance criteria.
- Write the task deliverable exactly to `{task['design_doc_path']}`.
- Save every detailed design document created or updated by this task under `{DETAILED_DESIGN_ROOT}/`.
- Do not create route design, route mutation, direct command execution by Scheduler, artifact mutation, or business-success inference.
- If a gap appears, state the blocker in the design document and request or make a design-document update.

## Review Checks

{chr(10).join('- ' + x for x in task['verification'])}

## Final Response

Summarize `{task['task_id']}`, detailed design document path, review checks performed, and remaining design risks. Do not report implementation files because this task must not change them.
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    DESIGN_OUT.mkdir(parents=True, exist_ok=True)
    write(OUT / "design-planning.json", jdump(planning))
    write(DESIGN_OUT / "rust-implementation-design.md", rust_design)
    stale_design = OUT / "rust-implementation-design.md"
    if stale_design.exists() and stale_design.resolve() != (DESIGN_OUT / "rust-implementation-design.md").resolve():
        stale_design.unlink()
    for task in tasks:
        fdir = TARGET / task["fixture_dir"]
        write(fdir / "prompt.md", fixture_prompt(task))
        write(fdir / "AGENTS.md", fixture_agents(task))
        write(fdir / "CLAUDE.md", fixture_claude(task))


if __name__ == "__main__":
    main()
