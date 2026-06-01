---
name: development-planning
description: Use when a target project has PRD/HLD/LLD documents under docs and needs the development-planning harness workflow to produce a planning-only development task plan, source-backed task descriptions under tasks/development, an executable DAG, independently acceptable task contracts, and a final delivery acceptance task before product development begins.
---

# Development Planning

Use this runtime entry for the `development-planning` harness workflow. The harness plans development after PRD/HLD/LLD exists, reads planning documents under the target project's `docs/`, produces canonical JSON development planning under the planning output root, and emits per-task descriptions plus task-scoped execution instructions.

This is a planning task, not a coding task. The skill must not implement product code, rewrite PRD/HLD/LLD, run delivery work, or create standalone starter prompt templates. Per-task prompt files are allowed only as task execution support files under `<planning-output-root>/<TASK-ID>/`.

## Harness Type

`harness-workflow`: the value is staged source interpretation, whole-plan decomposition, task-contract formation, task logic review, whole-plan integrity review, DAG validation, and parent-consumable planning verdicts.

The portable harness contract is defined by the top-level `manifest.yaml`, `agent.md`, `workflow.md`, `rules.md`, `schemas/development-planning.schema.json`, and `validators/validate_harness.py`. This runtime entry must follow that contract.

## Inputs

- Target project root.
- PRD/HLD/LLD and related requirement, architecture, low-level design, acceptance, or delivery documents fixed under `<target>/docs`.
- Target project source files only when needed to verify stack, module boundaries, local conventions, build/test commands, existing tests, interfaces, schemas, migrations, or deployment scripts.

## Required Outputs

Write these files in the target project:

- `<planning-output-root>/development-planning.json`: canonical planning output containing the task list, DAG, execution order, task description index, and acceptance gates.
- `<planning-output-root>/<TASK-ID>/task.md`: the task description and delivery contract for one planned development task.
- `<planning-output-root>/<TASK-ID>/prompt.md`
- `<planning-output-root>/<TASK-ID>/AGENTS.md`
- `<planning-output-root>/<TASK-ID>/CLAUDE.md`

The default planning output root is `tasks/development`. If the user explicitly requests another planning or task output root, use that requested root and record it in `development-planning.json` as `output_root`. If PRD/HLD/LLD evidence is missing, contradictory, or too thin to plan safe development tasks, still write `<planning-output-root>/development-planning.json` with `planning_status=blocked`, blockers, and required fixes. Do not fabricate a ready implementation DAG, task description, or task fixture.

## References

Load only what the task needs:

- `references/methodology.md`: source reading, boundaries, task decomposition, DAG rules, blocker criteria, and acceptance task design.
- `references/output-contract.md`: target output file contracts, task description contract, and readiness gates.
- `references/planning-quality-model.md`: harness-style staged planning and review model.
- `assets/TASK_DESCRIPTION.template.md`: per-task `task.md` delivery contract template.
- `assets/TASK_PROMPT.fixture.md`: per-task prompt support template.
- `assets/AGENTS.template.md`: per-task `AGENTS.md` fixture template.
- `assets/CLAUDE.template.md`: per-task `CLAUDE.md` fixture template.

## Workflow

1. Inspect `<target>/docs` recursively and inventory PRD/HLD/LLD sources.
2. Read relevant PRD/HLD/LLD deeply enough to identify product scope, current delivery phase, architecture, low-level design obligations, interfaces, data/state model, acceptance criteria, constraints, risks, and non-goals.
   - If `docs/contract-envelope.json` or another structured contract source exists, inventory and read it directly. Do not rely only on rendered PRD/HLD prose for requirement, acceptance, verification, STOP, or technical decision IDs.
3. Inspect target source only to confirm local implementation conventions such as package layout, module boundaries, framework choices, persistence libraries, error style, CLI/API framework, build commands, test commands, and generated artifact rules.
4. Stage 1, overall planning: extract development obligations and create a source-backed whole-plan outline with product goals, scope, task families, delivery phases, acceptance surface, and likely dependency axes. Do not create final task files yet.
5. Stage 2, independent task formation: decompose the whole-plan outline into cohesive implementation tasks with inputs, exact expected output areas, acceptance criteria, verification commands, stop conditions, allowed scope, forbidden scope, and handoff expectations.
6. Stage 3, task logic and completeness review: review every task contract for cohesion, independent acceptance, source traceability, boundary clarity, verification sufficiency, stop conditions, and downstream handoff value. Block or revise weak tasks before writing ready outputs.
7. Stage 4, whole-plan integrity and dependency review: build and review the DAG, execution order, parallel groups, coverage matrix, final delivery acceptance task, and dependency reasons. Block or revise when requirements are uncovered, dependencies are cyclic/ambiguous, or parallel tasks conflict.
   - Build reverse coverage from source requirement/acceptance IDs to tasks, verification, evidence, and final acceptance. `coverage_matrix` may show task-to-source coverage, but `requirement_coverage_matrix` is required when sources contain explicit IDs such as `FR-001` or `AC-001`.
   - Treat any direct or transitive dependency path between two tasks as a blocker for putting them in the same parallel group.
8. Define execution logic: topological order, parallel groups, stage gates, blocked conditions, and the final delivery acceptance task.
9. Write `<planning-output-root>/development-planning.json` with harness-style phase reports, task list, DAG, task description index, fixture index, coverage, execution order, task logic review, plan integrity review, and gate report as JSON.
10. For each ready task, create `<planning-output-root>/<TASK-ID>/task.md` as the task description and delivery contract.
11. For each ready task, create `<planning-output-root>/<TASK-ID>/prompt.md`, `AGENTS.md`, and `CLAUDE.md` from the fixture templates, adapting task-specific source refs, scope, acceptance criteria, verification commands, and handoff requirements.
12. Add exactly one final delivery acceptance task after all implementation tasks. This task must depend on every non-deferred implementation task, specify full delivery verification, produce a named acceptance report under the planning output root, and verify the completed product against PRD/HLD/LLD delivery standards.
13. Self-review against `references/planning-quality-model.md` and the gate report in `references/output-contract.md` before claiming readiness.

## Hard Rules

- PRD/HLD/LLD inputs are fixed under target `docs/`.
- Planning and task description outputs use `tasks/development/` by default unless the user explicitly specifies another planning output root.
- DAG and task list must be JSON, not only Markdown prose.
- Per-task `task.md`, prompt, `AGENTS.md`, and `CLAUDE.md` belong under `<planning-output-root>/<TASK-ID>/`.
- No standalone starter prompt template is produced.
- This skill plans development work; it does not perform implementation, modify product code, run development tasks, or claim delivered software.
- Harness-style review stages are mandatory: overall planning, independent task formation, task logic/completeness review, and whole-plan dependency/integrity review.
- Every ready task must be cohesive: one responsibility, one bounded set of files or components, one acceptance surface.
- Every ready task must be independently acceptable: clear inputs, outputs, boundaries, constraints, verification, and stop conditions.
- Every ready plan must include exactly one final delivery acceptance task. It must depend on all non-deferred implementation tasks and verify the whole product against PRD/HLD/LLD acceptance and delivery standards.
- Do not invent requirements, APIs, data fields, runtime components, acceptance commands, libraries, services, deployment environments, or test data.
- Follow the technology stack and architecture defined by PRD/HLD/LLD and confirmed source evidence. If absent or conflicting, block the affected development area.
- Treat unresolved interface docs, real acceptance environment, data source, permission model, schema/migration ownership, or architectural decisions as blockers when they affect implementation safety.

## Ready Gates

A ready development-planning result must satisfy all of these:

- Every material PRD/HLD/LLD source is listed in the source inventory.
- Every material structured contract source under `docs`, including `contract-envelope.json`, is listed in the source inventory and read before task generation.
- The plan contains harness-style phase reports for overall planning, independent task formation, task logic review, and whole-plan integrity review.
- Every current-phase requirement, output, and acceptance criterion maps to implementation tasks, the final acceptance task, or explicit deferred/blocking rationale.
- Every explicit source requirement or acceptance ID such as `FR-001` or `AC-001` maps through `requirement_coverage_matrix` to implementation task(s), the final delivery acceptance task, verification method, and required evidence.
- Every implementation task is cohesive and independently acceptable.
- Every task has source-backed allowed scope, forbidden scope, expected outputs, acceptance criteria, verification commands or checks, stop conditions, dependencies, task description path, and fixture paths.
- The DAG is acyclic and every dependency has a semantic reason.
- The task logic review has no blocking findings for task cohesion, completeness, acceptance, boundaries, verification, stop conditions, or handoff.
- The whole-plan integrity review has no blocking findings for coverage, dependency correctness, parallel safety, execution order, or final acceptance.
- Parallel groups do not share unresolved decisions, files, schemas, interfaces, migrations, state, test evidence, acceptance artifacts, or any direct/transitive dependency path.
- Execution order is derivable from the DAG.
- Every ready task has a folder under `tasks/development` with `task.md`, `prompt.md`, `AGENTS.md`, and `CLAUDE.md`.
- Fixture files are task-scoped, source-backed, and not one-line redirects.
- Exactly one final delivery acceptance task exists after all non-deferred implementation tasks and verifies source traceability, requirement coverage, DAG completion, full test/build acceptance, integration behavior, risks, and delivery standard compliance.
- No standalone starter prompt template artifact is produced.

## Common Mistakes

| Mistake | Correct Behavior |
| --- | --- |
| Treating development planning as implementation | Produce JSON planning, task descriptions, and per-task execution instructions only. |
| Reading only file names in `docs` | Read PRD/HLD/LLD deeply enough to plan implementation boundaries and acceptance. |
| Creating broad generic tasks | Create cohesive tasks with concrete outputs, constraints, and independent verification. |
| Missing the final acceptance task | Add exactly one delivery acceptance task that depends on all non-deferred implementation tasks. |
| Skipping review gates | Complete and record the task-level and whole-plan review stages before claiming readiness. |
| Producing a DAG without edge reasons | Every edge names the consumed output, interface, schema, migration, state model, decision, or test evidence. |
| Letting parallel tasks conflict | Parallel groups must be dependency-free and conflict-free. |
| Inventing stack or commands | Use PRD/HLD/LLD/source evidence, or block and request the decision. |
