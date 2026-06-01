# Output Contract

## `<planning-output-root>/design-planning.json`

This is the canonical planning output. It must be valid JSON and include:

```json
{
  "planning_status": "ready | blocked",
  "output_root": "tasks/design | user-specified planning output root",
  "detailed_design_root": "docs/design",
  "rust_design_path": "docs/design/rust-implementation-design.md",
  "source_inventory": [],
  "prd_hld_interpretation": {},
  "design_scope": {},
  "rust_stack": {},
  "planning_review_stages": [],
  "tasks": [],
  "dag": {
    "nodes": [],
    "edges": [],
    "parallel_groups": [],
    "cycle_check": {
      "status": "pass | blocked",
      "cycles": []
    }
  },
  "fixtures": [],
  "coverage_matrix": [],
  "planning_gate_report": [],
  "external_dependencies": [],
  "open_questions": [],
  "required_fixes": []
}
```

The default `<planning-output-root>` is `tasks/design`. If the user explicitly specifies another planning root, use that root consistently in `output_root`, task fixture paths, and fixture file content. All detailed design documents must still be saved under `docs/design/`.

Each `tasks[]` item must include:

- `task_id`
- `title`
- `task_type`
- `source_refs`
- `inputs`
- `outputs`
- `allowed_scope`
- `forbidden_scope`
- `acceptance`
- `verification`
- `stop_conditions`
- `dependencies`
- `design_doc_path`
- `fixture_dir`
- `prompt_path`
- `agents_path`
- `claude_path`

Ready planning must include exactly one final design acceptance task. It must:

- have `task_type=design_acceptance`
- depend on every detailed design document task
- have a `design_doc_path` under `docs/design/`
- produce an acceptance report for the complete detailed design document set
- forbid implementation/code/test/manifest/schema/migration/runtime changes

Each `dag.edges[]` item must include `from`, `to`, `reason`, and `source_refs`.

Each `planning_review_stages[]` item must include:

- `stage_id`
- `stage`
- `status`
- `checks`
- `findings`
- `evidence_refs`

Ready planning must include at least these stages:

- `overall_planning`
- `task_formation`
- `single_task_review`
- `global_dag_review`
- `artifact_generation`
- `final_design_acceptance`

Blocked planning must set `planning_status=blocked`, keep `tasks`, `dag.nodes`, `dag.edges`, and `fixtures` empty unless a partial diagnostic is explicitly safe, and include non-empty `required_fixes`.

## `docs/design/rust-implementation-design.md`

Required sections:

1. Architecture And Crate Boundaries
2. Control Flow
3. Data Flow
4. Data Types And Contracts
5. Interface Contracts
6. State And Persistence
7. Error Handling And Diagnostics
8. Async And Concurrency
9. Key Technical Decisions
10. Security And Permissions
11. Observability
12. Test And Acceptance Design
13. Risks And Guardrails

## `<planning-output-root>/fixtures/<TASK-ID>/prompt.md`

Each ready task must have a single-task prompt fixture. It must include:

- task ID and title
- role and mission
- source refs to read first
- exact detailed-design scope for that one task
- forbidden scope
- exact detailed design document filename under `docs/design/`
- expected document outputs
- explicit requirement that all detailed design documents created or updated by the task are saved under `docs/design/`
- document review checks
- stop conditions
- handoff expectations

The prompt is task-scoped. It must not be a generic project starter prompt.
It must explicitly state that the task is documentation-only and must not modify production code, tests, build manifests, schemas, migrations, or runtime scripts.

## `<planning-output-root>/fixtures/<TASK-ID>/AGENTS.md`

Each ready task must have task-scoped Codex/general agent instructions. It should include:

- role and mission
- PRD/HLD source requirement
- task fixture source requirement
- Rust stack constraints
- no-new-facts rule
- task documentation boundaries
- detailed design document output path rule: `docs/design/`
- verification and acceptance expectations
- handoff format

It must not include one-off prompt templates.

## `<planning-output-root>/fixtures/<TASK-ID>/CLAUDE.md`

Each ready task must have task-scoped Claude instructions, not a one-line redirect. It should include:

- role
- fixed input/output paths
- detailed design documents fixed under `docs/design/`
- task source reading method
- Rust detailed design checklist
- task boundary rules
- hard constraints
- consistency with the fixture `AGENTS.md`

It must not include one-off prompt templates.
It must explicitly state that the Claude task is to produce the named detailed design document only, not implementation code.

## Gate Report

Use these checks:

| Gate | Pass Condition |
| --- | --- |
| source_readiness | PRD/HLD sources are present and inventoried. |
| traceability | Every design claim maps to PRD/HLD or target evidence. |
| rust_stack_readiness | Rust stack and local conventions are confirmed or blockers are recorded. |
| control_flow_readiness | Ordered execution and failure paths are designed. |
| data_flow_readiness | Data movement, transformations, and persistence are designed. |
| technical_decision_readiness | Key choices cite evidence and explain trade-offs. |
| staged_review_readiness | Overall planning, task formation, single-task review, global DAG review, artifact generation, and final acceptance stages are recorded and pass. |
| dag_soundness | DAG is acyclic and edges have reasons. |
| parallel_safety | Parallel groups are dependency-free and conflict-free. |
| task_fixture_readiness | Every ready task has prompt.md, AGENTS.md, and CLAUDE.md under its fixture folder. |
| design_acceptance_task | One final acceptance task exists after all design tasks and validates good detailed design document quality. |
| no_starter_prompt_template | No standalone starter prompt template output is created. |
