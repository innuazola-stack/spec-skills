# Design Planning Workflow

## Paradigm

`review-gated harness`

The workflow is mostly linear, but each stage has a gate that can block downstream work or require revision. The final design acceptance task is a downstream review artifact consumed by the caller before implementation begins.

## Stage 1: Overall Planning

Input:

- target project root
- all files under `<target>/docs`

Actions:

- inventory PRD/HLD and related sources
- identify current phase, scope, non-goals, Rust stack, architecture, control flow, data flow, interfaces, state, risks, and acceptance obligations
- inspect target source only as evidence for local Rust conventions

Output:

- `source_inventory`
- `prd_hld_interpretation`
- `design_scope`
- `rust_stack`
- initial obligation set

Gate:

- pass when PRD/HLD sources are present and sufficient for design
- revise when evidence is thin but recoverable through explicit required fixes
- fail when ready planning would require invented product facts

## Stage 2: Task Formation

Input:

- obligation set from Stage 1
- output contract

Actions:

- decompose obligations into documentation-only detailed design tasks
- assign each task one exact `docs/design/*.md` design document path
- define source refs, inputs, outputs, allowed scope, forbidden scope, review checks, stop conditions, and handoff expectations

Output:

- `tasks[]`
- `fixtures[]`

Gate:

- pass when every task is independently executable as a design document task
- revise when a task is too broad, overlaps another task, or lacks an exact document path
- fail when a task would require implementation work or unsupported facts

## Stage 3: Single-Task Review

Input:

- every task candidate

Actions:

- review each task for logical scope, source traceability, single-document deliverability, no-code constraints, and fixture readiness

Output:

- `planning_review_stages[]` entry for `single_task_review`
- task-level fixes or blockers

Gate:

- pass when every task can produce the named design document without modifying code
- revise when task wording could be misread as implementation
- fail when task execution cannot be safely bounded

## Stage 4: Global DAG Review

Input:

- reviewed task set

Actions:

- build acyclic dependency DAG
- add edge reasons
- verify missing obligations, duplicate ownership, hidden dependencies, invalid parallelism, and dependency direction

Output:

- `dag.nodes`
- `dag.edges`
- `dag.parallel_groups`
- `coverage_matrix`

Gate:

- pass when DAG is acyclic and complete
- revise when dependencies are ambiguous or coverage is incomplete
- fail when the task set cannot satisfy PRD/HLD expectations

## Stage 5: Artifact Generation

Input:

- reviewed DAG and task set

Actions:

- write `<planning-output-root>/design-planning.json`
- write `docs/design/rust-implementation-design.md`
- write every task fixture directory with `prompt.md`, `AGENTS.md`, and `CLAUDE.md`

Output:

- planning JSON
- overall design document
- per-task fixtures

Gate:

- pass when validator confirms structure, paths, fixture files, task wording, and DAG integrity
- revise when structural errors are found
- fail when required artifacts cannot be written

## Stage 6: Final Design Acceptance

Input:

- all detailed design document tasks
- all planned `docs/design/*.md` design document paths

Actions:

- add a final `design_acceptance` task after all detailed design tasks
- require an acceptance report under `docs/design/`
- check final task depends on every detailed design task

Output:

- final acceptance task and fixture
- `planning_review_stages[]` entry for `final_design_acceptance`

Gate:

- pass when exactly one final acceptance task exists and depends on every detailed design task
- revise when acceptance scope is incomplete
- fail when no final acceptance route exists

## Handoff

The handoff must include:

- target project
- output roots
- task count, edge count, fixture count
- final acceptance task id
- validator command and verdict
- semantic review verdict
- residual warnings and external dependencies
