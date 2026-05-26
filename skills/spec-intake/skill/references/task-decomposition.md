# Task Decomposition

Use this reference after the Agent PRD is execution-ready and the user wants implementation tasks.

## Preconditions

Ready task planning requires:

- `planning_source_mode=contract_backed`
- Agent PRD status is `execution_ready`
- `source_artifacts.agent_prd_status` matches `contract-envelope.json.render_status.agent_prd`
- canonical phase is available as `PHASE-*`
- current phase has at least one current `REQ-*`
- source gates have no blocking failures
- every current `REQ-*` has linked `AC-*` and `VER-*`
- `IN`, `EXE`, `VER`, `OUT`, `STOP`, and `DONE` exist in the contract

If any precondition fails, output a blocked task-plan envelope with empty `task_graph`, `dependency_edges`, and `parallel_groups`.

`planning_source_mode=rendered_agent_prd_only` is allowed only for diagnostic or migration output. It must have `planning_status=blocked`, `phase_ref_kind=rendered_label`, a non-empty `phase_ref_fallback_reason`, and no executable task graph.

## Task Graph Contract

`execution-task-plan.json` contains:

- `plan_id`
- `planning_source_mode`
- `source_artifacts`
- `planning_status`
- `blocking_reasons`
- `missing_required_refs`
- `required_fixes`
- `task_graph`
- `dependency_edges`
- `parallel_groups`
- `stage_goal_coverage`
- `planning_gate_report`

Each task must include:

- `task_id`
- `title`
- `task_type`
- `contract_refs`
- `verification_refs`
- `done_refs`
- `stop_refs`
- `inputs`
- `outputs`
- `dependencies`
- `parallel_group`
- `allowed_files_or_modules`
- `forbidden_scope_refs`
- `acceptance`
- `verification`
- `stop_conditions`
- `status`

Task status vocabulary is `planned`, `ready`, `blocked`, `deferred`, `in_progress`, `done`, or `skipped`.

Ready task plans may contain only `planned` or `ready` tasks. `blocked`, `deferred`, `in_progress`, `done`, and `skipped` can appear only in non-ready planning contexts or execution state records outside this intake handoff.

Parallel group status vocabulary is `serial`, `parallel_safe`, or `blocked`.

`stage_goal_coverage` must include `phase_ref`, `phase_label`, `goal_refs`, `required_task_refs`, `coverage_status`, and `missing_refs`. A ready plan requires `coverage_status=covered` and empty `missing_refs`.

For ready plans, `stage_goal_coverage.phase_ref` must match `source_artifacts.phase_ref`, `goal_refs` must be canonical contract refs, and `required_task_refs` must be non-empty. Dependency edge `contract_refs` must be canonical contract refs, not `TASK-*`, `PG-*`, or `CHECK-*`.

## Decomposition Method

1. Freeze source artifacts and current phase.
2. Build source inventory: current `REQ/AC/OUT/DONE`, `IN`, `DCT`, `DATA`, `EXE`, `STATE`, `FLOW`, `VER`, `STOP`, `BAR`, `RISK`, `OOS`, `Q`, `ASM`, `TECH`, `MOD`.
3. Derive execution units: entry boundary, data contract, requirement behavior, state/control, output, risk/stop, verification.
4. Slice units into closed tasks.
5. Write closure cards: inputs, outputs, allowed boundary, forbidden boundary, independent acceptance, verification refs, stop conditions, dependencies.
6. Infer dependency edges from real data, state, output, safety, integration, or verification dependencies. Edge direction is `from=<dependency task>` and `to=<dependent task>`, matching each dependent task's `dependencies` list.
7. Infer parallel groups. Dependency-linked tasks must not be `parallel_safe` together.
8. Prove stage goal coverage.
9. Run planning gates.

## Hard Principles

- Tasks must be closed: no hidden context or implicit scope.
- Tasks must be independently acceptable: a reviewer can pass/fail each task without waiting for the whole PRD.
- All non-deferred tasks together must cover every current phase `REQ`, linked `AC`, execution `IN/EXE/VER/OUT/STOP/DONE`, and done criterion needed for the current phase goal.
- Closure fields must not be bypassed by stuffing refs into `contract_refs`: `inputs`, `outputs`, and `stop_refs` must carry their own `IN-*`, `OUT-*`, and `STOP-*` refs.
- Tasks do not create product facts; they only schedule contract-backed facts.
