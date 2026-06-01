# Planning Quality Model

Use harness-style quality gates to judge this planning skill without turning it into a runtime harness.

## Target Type

- target type: `harness-workflow`
- quality standard: harness-style staged planning gates
- non-goal: runtime orchestration, delegated agents, approvals, adapters, release packages, or live E2E evidence

## Required Stages

| Stage | Name | Required Output | Blocking If |
| --- | --- | --- | --- |
| `STAGE-001` | Overall planning | Whole-plan outline covering goals, scope, task families, acceptance surface, risks, and dependency axes. | PRD/HLD/LLD cannot support a whole-plan outline. |
| `STAGE-002` | Independent task formation | Cohesive task contracts with source refs, boundaries, acceptance, verification, stop conditions, and handoff. | Any task cannot be independently accepted or has unclear boundaries. |
| `STAGE-003` | Task logic and completeness review | `task_logic_review` with one reviewed result per task. | Any task fails cohesion, completeness, acceptance, verification, or handoff checks. |
| `STAGE-004` | Whole-plan integrity and dependency review | `plan_integrity_review` covering coverage, DAG, execution order, parallel safety, and final acceptance. | Coverage gaps, cyclic/ambiguous dependencies, unsafe parallelism, or weak final acceptance remain. |

## Review Dimensions

Task-level review checks:

- cohesion
- independent acceptance
- source traceability
- reverse requirement coverage
- boundary clarity
- verification sufficiency
- stop condition sufficiency
- handoff completeness
- dependency input clarity

Plan-level review checks:

- current-phase requirement coverage
- output and acceptance coverage
- source requirement ID coverage
- DAG acyclicity
- edge consumed-output quality
- execution order validity
- parallel safety, including no direct or transitive dependency path inside any parallel group
- final delivery acceptance correctness
- deferred and future-phase isolation

## Done Criteria

A ready result must include:

- all four `phase_reports[]`
- `task_logic_review.status=pass`
- `plan_integrity_review.status=pass`
- no blocking findings in task-level or plan-level reviews
- task descriptions and fixtures for every ready task
- exactly one final delivery acceptance task
- a reverse `requirement_coverage_matrix` whenever source docs contain explicit requirement or acceptance IDs such as `FR-001` or `AC-001`

If any criterion fails, output blocked planning with required fixes instead of ready task contracts.
