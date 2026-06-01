# Methodology

## Boundary

This skill serves target projects that already have PRD/HLD/LLD material under `docs/`. It prepares the project for future implementation by producing canonical JSON development planning, per-task descriptions, and per-task execution support files.

It does not implement product code, generate PRD/HLD/LLD, run development work, or create standalone starter prompt templates. Per-task prompt files are allowed only inside task folders. If PRD/HLD/LLD is missing or too thin, produce a blocked development planning JSON with required fixes.

The default planning output root is `tasks/development`. If the user explicitly names another planning output root, use that root consistently and record it in the planning JSON as `output_root`.

## Method

1. Inventory `docs/` sources.
2. Read PRD/HLD/LLD for product scope, current phase, architecture, detailed component design, data/state model, interfaces, constraints, acceptance, risks, and non-goals.
3. Verify local implementation conventions from project source only when needed.
4. Extract development obligations.
5. Create the overall development plan before task files exist.
6. Decompose obligations into cohesive, independently acceptable implementation tasks.
7. Review each task for logic and completeness.
8. Add one final delivery acceptance task after all non-deferred implementation tasks.
9. Build and review an acyclic DAG with explicit edge reasons and execution logic.
10. Write `<planning-output-root>/development-planning.json` containing `planning_status`, `output_root`, harness-style phase reports, DAG, task list, task description index, fixtures index, task-to-source coverage, reverse requirement coverage, dependencies, parallel groups, execution order, task logic review, plan integrity review, and gates.
11. Write per-task descriptions under `<planning-output-root>/<TASK-ID>/task.md`.
12. Write per-task fixtures under `<planning-output-root>/<TASK-ID>/`.
13. Self-review for traceability, source requirement ID coverage, no-new-facts, staged planning rigor, task logic, task completeness, DAG soundness, task description readiness, task fixture readiness, task cohesion, independent acceptance, and delivery acceptance coverage.

## Harness-Style Planning Stages

Use this four-stage quality model:

1. Overall planning: build a whole-plan outline from PRD/HLD/LLD before creating final task contracts.
2. Independent task formation: split the outline into cohesive, independently acceptable tasks with source-backed contracts.
3. Task logic and completeness review: check every task for cohesion, boundary clarity, acceptance, verification, stop conditions, and handoff value.
4. Whole-plan integrity and dependency review: check task-to-source coverage, reverse requirement coverage, DAG correctness, execution order, parallel safety, final acceptance, deferred work, and blockers.

Record each stage in `phase_reports[]`. A ready plan cannot skip a stage or leave a stage in `blocked`.

## Development Task Criteria

Each implementation task must include:

- task ID
- title
- task type
- source refs
- inputs consumed
- expected outputs
- allowed scope
- forbidden scope
- acceptance criteria
- verification commands or checks
- stop conditions
- dependencies
- impacted files, components, modules, schemas, migrations, docs, or tests
- task description path
- fixture directory
- single-task prompt path
- task `AGENTS.md` path
- task `CLAUDE.md` path

The task title, scope, outputs, acceptance, and verification must describe one cohesive implementation responsibility. Avoid mixing unrelated UI, backend, schema, deployment, and acceptance work in the same task unless the PRD/HLD/LLD proves they are inseparable.

## Independent Acceptance

Each task must be acceptable on its own. A downstream task may depend on it, but the task itself still needs:

- a clear completion state
- direct acceptance criteria
- verification commands or review checks
- explicit file/component boundaries
- explicit stop conditions for missing source facts, broken dependencies, or out-of-scope work
- a handoff that states changed areas, tests run, unresolved risks, and dependency outputs for later tasks

## Task Logic And Completeness Review

Review every task contract before declaring the plan ready. Block or revise if any task:

- mixes unrelated responsibilities
- lacks a source-backed reason to exist
- cannot be independently accepted
- has vague expected outputs or impacted areas
- lacks verification or acceptance evidence
- has weak stop conditions
- lacks clear downstream handoff outputs
- depends on an unstated or cyclic upstream output

## Final Delivery Acceptance Task

The final delivery acceptance task is still planned work. It must depend on every non-deferred implementation task and must verify:

- all planned implementation tasks are complete or explicitly deferred by source-backed rationale
- product behavior satisfies PRD/HLD/LLD requirements and acceptance criteria
- every explicit source requirement or acceptance ID such as `FR-001` or `AC-001` is covered by the reverse `requirement_coverage_matrix`
- build, tests, lint/typecheck, migrations, contract tests, integration tests, or manual verification required by source docs are executed or explicitly blocked
- user-facing flows, API/CLI contracts, data/state behavior, permissions, observability, and error paths are covered where applicable
- no future-phase or out-of-scope work was silently implemented
- unresolved risks, defects, and release blockers are recorded
- a delivery acceptance report will be written under `<planning-output-root>/`

The acceptance task is a verification task. It must not add new product scope. If it is allowed to fix defects, that allowance must be explicit in the task scope and must be constrained to issues discovered while executing acceptance.

## DAG Rules

- No cycles.
- Edge reasons must be semantic.
- Each edge must state the upstream output consumed by the downstream task.
- Parallel groups require no direct or transitive dependency path and no conflict over files, components, schemas, migrations, interfaces, state, test evidence, or acceptance artifacts.
- Future-phase PRD/HLD/LLD work must not enter current-phase implementation unless explicitly required as preparation.
- The final delivery acceptance task must be last in the DAG.

## Whole-Plan Integrity Review

Review the complete task graph before writing ready outputs. Block or revise if:

- any current-phase requirement, output, acceptance criterion, or required verification is uncovered
- source docs contain explicit requirement or acceptance IDs but `requirement_coverage_matrix` does not map them to tasks, final acceptance, verification, and evidence
- an edge lacks a consumed output or source-backed reason
- the graph has a cycle
- execution order is not a valid topological order
- a parallel group has a direct/transitive dependency path or file, schema, migration, interface, state, test evidence, or acceptance conflicts
- the final delivery acceptance task is missing, not last, or does not depend on all non-deferred implementation tasks
- deferred or future-phase work leaks into current-phase implementation

## Blockers

Block readiness when:

- PRD, HLD, or required LLD is absent.
- Current delivery phase cannot be identified.
- Technology stack, architecture, interfaces, data model, state model, permissions, schema/migration ownership, or acceptance evidence is missing or contradictory.
- Required verification commands or acceptance environment cannot be determined.
- A requested task would require inventing product facts or implementation scope.
- A task cannot be isolated into a safe single-task execution fixture.
