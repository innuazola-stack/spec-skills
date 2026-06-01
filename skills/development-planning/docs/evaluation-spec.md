# Evaluation Spec

## Exact Review Query

Use this query when evaluating the skill:

```text
Use development-planning on this target project. Read PRD/HLD/LLD under ./docs and produce planning only. The planning must write task descriptions to tasks/development, include cohesive independently acceptable development tasks, a DAG and execution order as JSON, per-task support files containing prompt.md, CLAUDE.md, and AGENTS.md, one final delivery acceptance task, and harness-style staged planning reviews for overall planning, independent task formation, task logic, and whole-plan integrity.
```

## Positive Case

Input: A target project has `docs/prd.md`, `docs/hld.md`, and `docs/lld.md` with current-phase requirements, architecture, low-level component design, interfaces, acceptance, and stack.

Fixture: `evals/fixtures/positive-prd-hld-lld`.

Expected:

- Reads PRD, HLD, and LLD.
- Writes `tasks/development/development-planning.json` with `tasks`, `dag`, and `execution_order`.
- Includes `planning_harness_model`, four `phase_reports`, `task_logic_review`, and `plan_integrity_review`.
- Produces cohesive tasks with explicit boundaries, constraints, verification, and independent acceptance.
- Produces DAG edges with reasons and consumed outputs in JSON.
- Writes `tasks/development/<TASK-ID>/task.md`, `prompt.md`, `AGENTS.md`, and `CLAUDE.md` for every ready task.
- Includes exactly one final `delivery_acceptance` task depending on all non-deferred implementation tasks.
- Records no blocking findings in task-level or whole-plan reviews.
- Passes `validators/validate_development_planning_package.py` against the generated package.
- Does not implement product code; it only plans future development work.
- Does not create a standalone starter prompt template.

Forbidden:

- Markdown-only task planning.
- Generic all-task prompt instead of per-task `prompt.md`.
- A ready plan with no final acceptance task.
- A ready plan without all four phase reports.
- A ready plan with missing or blocked `task_logic_review` or `plan_integrity_review`.
- Tasks that mix unrelated responsibilities without source-backed rationale.

## Negative Case

Input: Target project has no HLD or lacks required LLD/interface/acceptance details.

Fixture: `evals/fixtures/negative-missing-lld`.

Expected:

- Writes blocked `tasks/development/development-planning.json`.
- Lists missing PRD/HLD/LLD, interface, stack, or acceptance decisions as required fixes.
- Does not fabricate a ready DAG.
- Does not emit ready task descriptions or task fixtures.
- Records blocked phase reports and required fixes instead of pretending reviews passed.
- Passes `validators/validate_development_planning_package.py` as an honestly blocked package.
- Does not implement product code.

Forbidden:

- Any ready task in `tasks[]`.
- Any fixture entry for a task that depends on missing design or acceptance facts.

## Boundary Case

Input: PRD/HLD/LLD exists but includes a future-phase feature request.

Fixture: `evals/fixtures/boundary-future-phase`.

Expected:

- Keeps current-phase DAG clean.
- Defers future-phase work unless explicitly required as preparation.
- Records source-backed defer rationale.

Forbidden:

- Future-phase task nodes in the current-phase DAG without explicit PRD/HLD/LLD preparation evidence.
- Dependency edges from current tasks to deferred future-phase tasks.

## Review Rubric

- Source traceability.
- Task cohesion.
- Independent acceptance.
- DAG acyclicity and edge quality.
- Execution order and parallel safety.
- Task description and fixture completeness.
- Harness-style staged planning.
- Task logic review quality.
- Whole-plan integrity review quality.
- No-new-facts compliance.
- AGENTS/CLAUDE durability.
- Final delivery acceptance task quality.
- Absence of standalone starter prompt template output.

## Scoring Rule

Score each dimension as:

- `2`: fully satisfies the requirement with source-backed evidence.
- `1`: partially satisfies the requirement but has ambiguity or weak evidence.
- `0`: missing, contradicted, or unsafe.

Dimensions:

1. PRD/HLD/LLD source inventory and reading discipline.
2. JSON planning shape with `tasks`, `dag`, and `execution_order`.
3. Task cohesion and scope boundaries.
4. Independent task acceptance.
5. Harness-style staged planning.
6. Task logic review quality.
7. Whole-plan integrity and dependency review quality.
8. DAG edge reasons and acyclicity.
9. Per-task `task.md` and fixture completeness.
10. Task prompt specificity.
11. Final delivery acceptance task.
12. Blocked behavior for missing evidence.

Pass bar:

- Total score at least 22 of 24.
- No dimension may score `0`.
- Dimensions 2, 4, 5, 6, 7, 8, 9, 11, and 12 must each score `2`.
