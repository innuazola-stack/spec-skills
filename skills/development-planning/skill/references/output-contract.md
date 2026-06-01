# Output Contract

## `<planning-output-root>/development-planning.json`

This is the canonical planning output. It must be valid JSON and include:

```json
{
  "planning_status": "ready | blocked",
  "output_root": "tasks/development | user-specified planning output root",
  "source_inventory": [],
  "prd_hld_lld_interpretation": {},
  "development_scope": {},
  "project_stack": {},
  "planning_harness_model": {
    "target_type": "harness-workflow",
    "quality_standard": "harness-style staged planning gates",
    "stages": []
  },
  "phase_reports": [],
  "tasks": [],
  "dag": {
    "nodes": [],
    "edges": [],
    "parallel_groups": [],
    "execution_order": [],
    "cycle_check": {
      "status": "pass | blocked",
      "cycles": []
    }
  },
  "task_descriptions": [],
  "fixtures": [],
  "coverage_matrix": [],
  "requirement_coverage_matrix": [],
  "delivery_acceptance": {},
  "task_logic_review": {},
  "plan_integrity_review": {},
  "planning_gate_report": [],
  "external_dependencies": [],
  "open_questions": [],
  "required_fixes": []
}
```

The default `<planning-output-root>` is `tasks/development`. If the user explicitly specifies another planning root, use that root consistently in `output_root`, task description paths, task fixture paths, and fixture file content.

Each `tasks[]` item must include:

- `task_id`
- `title`
- `task_type`
- `source_refs`
- `inputs`
- `expected_outputs`
- `impacted_areas`
- `allowed_scope`
- `forbidden_scope`
- `acceptance`
- `verification`
- `stop_conditions`
- `dependencies`
- `handoff_requirements`
- `task_description_path`
- `fixture_dir`
- `prompt_path`
- `agents_path`
- `claude_path`

Each `phase_reports[]` item must include:

- `stage_id`
- `stage_name`
- `purpose`
- `inputs`
- `outputs`
- `review_checks`
- `status`
- `blocking_findings`

Ready planning must include exactly one final delivery acceptance task. It must:

- have `task_type=delivery_acceptance`
- depend on every non-deferred implementation task
- produce a named acceptance report under `<planning-output-root>/`
- verify the complete software product against PRD/HLD/LLD delivery requirements
- include build/test/lint/typecheck/integration/manual verification expectations where source-backed
- avoid adding new product scope

Each `dag.edges[]` item must include `from`, `to`, `reason`, `consumed_output`, and `source_refs`.

Each `dag.parallel_groups[]` item must include `group_id`, `task_ids`, `rationale`, `conflict_check`, and `source_refs`.

Each ready plan should include `requirement_coverage_matrix[]` when PRD/HLD/LLD sources contain explicit requirement or acceptance IDs such as `FR-001` or `AC-001`. Each row must include:

- `coverage_id`
- `requirement_family`
- `source_requirements`
- `covered_by_tasks`
- `verified_by`
- `required_evidence`

The matrix is the reverse coverage gate: every source requirement or acceptance ID must map to one or more implementation tasks, the final delivery acceptance task, verification method, and concrete evidence artifacts. Do not rely only on task-to-source `coverage_matrix`; it cannot prove source-to-task completeness by itself.

`task_logic_review` must summarize every task-level review. It must include `status`, `reviewed_task_ids`, `checks`, `blocking_findings`, and `required_revisions`. Required checks are cohesion, independent acceptance, source traceability, boundary clarity, verification sufficiency, stop conditions, and handoff completeness.

`plan_integrity_review` must summarize the whole-plan review. It must include `status`, `checks`, `coverage_findings`, `dependency_findings`, `parallel_safety_findings`, `execution_order_findings`, `delivery_acceptance_findings`, `blocking_findings`, and `required_revisions`.

Blocked planning must set `planning_status=blocked`, keep `tasks`, `dag.nodes`, `dag.edges`, `dag.parallel_groups`, `dag.execution_order`, task descriptions, and fixtures empty unless a partial diagnostic is explicitly safe, and include non-empty `required_fixes`.

## `<planning-output-root>/<TASK-ID>/task.md`

Each ready task must have a task description and delivery contract. It must include:

- task ID and title
- task type
- source refs
- planning status
- dependencies and downstream consumers
- allowed scope
- forbidden scope
- expected outputs
- acceptance criteria
- verification commands or review checks
- stop conditions
- handoff requirements

This file is the canonical human-readable task contract. It must describe future development work only; it must not contain completed implementation claims.

## `<planning-output-root>/<TASK-ID>/prompt.md`

Each ready task must have a single-task prompt fixture. It must include:

- task ID and title
- role and mission
- source refs to read first
- exact implementation scope for that one task
- forbidden scope
- expected output areas
- acceptance criteria
- verification commands or review checks
- stop conditions
- handoff expectations

The prompt is task-scoped. It must not be a generic project starter prompt.

## `<planning-output-root>/<TASK-ID>/AGENTS.md`

Each ready task must have task-scoped Codex/general agent instructions. It should include:

- role and mission
- PRD/HLD/LLD source requirement
- planning JSON source requirement
- task fixture source requirement
- technology stack constraints
- no-new-facts rule
- task boundary rules
- verification and acceptance expectations
- handoff format

It must not include one-off prompt templates.

## `<planning-output-root>/<TASK-ID>/CLAUDE.md`

Each ready task must have task-scoped Claude instructions, not a one-line redirect. It should include:

- role
- fixed input/output paths
- task source reading method
- implementation boundary rules
- verification expectations
- hard constraints
- consistency with the fixture `AGENTS.md`

It must not include one-off prompt templates.

## Gate Report

Use these checks:

| Gate | Pass Condition |
| --- | --- |
| source_readiness | PRD/HLD/LLD sources are present and inventoried. |
| traceability | Every task and acceptance claim maps to PRD/HLD/LLD or target evidence; explicit FR/AC source IDs are covered by `requirement_coverage_matrix`. |
| scope_readiness | Current delivery phase, in-scope work, non-goals, and deferred work are explicit. |
| stack_readiness | Technology stack and local conventions are confirmed or blockers are recorded. |
| task_cohesion | Every implementation task owns one bounded responsibility. |
| independent_acceptance | Every task has clear boundaries, acceptance, verification, and stop conditions. |
| staged_planning_rigor | Phase reports cover overall planning, independent task formation, task logic review, and whole-plan integrity review. |
| task_logic_review | Every task passes cohesion, completeness, acceptance, boundary, verification, stop condition, and handoff checks. |
| dag_soundness | DAG is acyclic, execution order is valid, and edges have reasons. |
| parallel_safety | Parallel groups are dependency-free and conflict-free; no task in a parallel group may depend directly or transitively on another task in the same group. |
| plan_integrity_review | Whole-plan coverage, dependencies, execution order, parallel groups, and final acceptance are reviewed with no blockers. |
| task_description_readiness | Every ready task has task.md under its task folder. |
| task_fixture_readiness | Every ready task has prompt.md, AGENTS.md, and CLAUDE.md under its task folder. |
| delivery_acceptance_task | One final acceptance task exists after all non-deferred implementation tasks and validates delivery quality. |
| no_starter_prompt_template | No standalone starter prompt template output is created. |
