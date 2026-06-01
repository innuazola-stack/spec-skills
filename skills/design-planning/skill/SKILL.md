---
name: design-planning
description: Use when a Rust target project has PRD/HLD documents under docs and needs harness-governed JSON design planning, detailed-design document tasks, per-task execution fixtures, and final design acceptance.
---

# Design Planning

This runtime skill entrypoint delegates to the `design-planning` harness workflow in the development root:

- `manifest.yaml`
- `agent.md`
- `workflow.md`
- `rules.md`
- `schemas/design-planning.schema.json`
- `validators/validate_design_planning.py`

Use the harness core as the source of truth. This file exists so Codex can discover and invoke the workflow as a local skill.

The workflow reads PRD/HLD under the target project's `docs/`, produces canonical JSON planning under the planning output root, writes all detailed design documents under the target repository's `docs/design/`, emits per-task execution fixtures containing the single-task prompt plus task-scoped `AGENTS.md` and `CLAUDE.md`, and validates the result with the harness validator.

This skill does not implement product code, write PRD/HLD, or generate standalone starter prompt templates. Per-task prompt files are allowed only as task execution fixtures under `<planning-output-root>/fixtures/<TASK-ID>/`.

## Harness Type

`harness-workflow`: review-gated workflow.

The workflow uses staged review gates and ships portable harness adapters plus release validation.

## Inputs

- Target project root.
- PRD/HLD and related requirement or architecture documents fixed under `<target>/docs`.
- Target project source files only when needed to verify Rust stack, crate layout, local conventions, interfaces, or build/test commands.

## Required Outputs

Write these files in the target project:

- `<planning-output-root>/design-planning.json`: canonical planning output containing the DAG and task list.
- `docs/design/rust-implementation-design.md`
- `<planning-output-root>/fixtures/<TASK-ID>/prompt.md`
- `<planning-output-root>/fixtures/<TASK-ID>/AGENTS.md`
- `<planning-output-root>/fixtures/<TASK-ID>/CLAUDE.md`

The default planning output root is `tasks/design`. If the user explicitly requests another planning or task output root, use that requested root and record it in `design-planning.json` as `output_root`. Detailed design documents are different: they must always be saved under target `docs/design/`. If PRD/HLD evidence is missing or contradictory, still write `<planning-output-root>/design-planning.json` with `planning_status=blocked`, blockers, and required fixes. Do not fabricate a ready design, ready DAG, or task fixtures.

## References

Load only what the task needs:

- `../agent.md`: role, boundaries, inputs, outputs, and done criteria.
- `../workflow.md`: stage graph and gate contracts.
- `../rules.md`: authority, file, no-code, task, acceptance, and validation rules.
- `references/methodology.md`: source reading, boundaries, task decomposition, DAG rules, and blocker criteria.
- `references/rust-detailed-design.md`: Rust-specific detailed design checklist.
- `references/output-contract.md`: target output file contracts and readiness gates.
- `assets/TASK_PROMPT.fixture.md`: per-task prompt fixture template.
- `assets/AGENTS.template.md`: per-task `AGENTS.md` fixture template.
- `assets/CLAUDE.template.md`: per-task `CLAUDE.md` fixture template.
- `../schemas/design-planning.schema.json`: machine-readable planning output shape.
- `../validators/validate_design_planning.py`: structural validator for generated planning.

## Workflow

Use the harness-style staged review model defined in `workflow.md`:

1. Stage 1, overall planning: inspect `<target>/docs` recursively, read PRD/HLD deeply, inventory sources, identify scope/current phase, Rust stack expectations, architecture, control flow, data flow, interfaces, state, acceptance, risks, and non-goals.
2. Stage 1 gate: confirm the overall plan is source-backed and has enough evidence to design. If not, write blocked planning JSON.
3. Stage 2, task formation: decompose the detailed design work into source-backed documentation sub-tasks with inputs, exact `docs/design/<filename>.md` output paths, acceptance, review checks, stop conditions, allowed scope, and forbidden scope.
4. Stage 2 gate: review every task independently for logical scope, single-document deliverability, source traceability, no-code constraints, and enough detail to produce the intended design document.
5. Stage 3, DAG construction: build an acyclic DAG. Every edge must name the consumed design output, decision, interface, schema, state model, or verification result.
6. Stage 3 gate: review the whole task set for missing obligations, duplicate ownership, hidden dependencies, invalid parallelism, and incorrect dependency direction.
7. Stage 4, artifact generation: write `<planning-output-root>/design-planning.json`, write `docs/design/rust-implementation-design.md`, and create each task fixture under `<planning-output-root>/fixtures/<TASK-ID>/`.
8. Stage 4 gate: add one final design acceptance task after all detailed design document tasks. This task must depend on every detailed design task, produce a named acceptance review document under `docs/design/`, and verify the whole design set against good detailed design document requirements.
9. Record the staged review results in `design-planning.json`, run `validators/validate_design_planning.py`, and self-review against the gate report in `references/output-contract.md` before claiming readiness.

## Hard Rules

- PRD/HLD inputs are fixed under target `docs/`.
- Planning and task fixture outputs use `tasks/design/` by default unless the user explicitly specifies another planning output root.
- Detailed design document outputs are fixed under target `docs/design/`.
- DAG and task list must be JSON, not only Markdown prose.
- Per-task prompt, `AGENTS.md`, and `CLAUDE.md` belong under `<planning-output-root>/fixtures/<TASK-ID>/`.
- No standalone starter prompt template is produced.
- Do not write implementation code unless the user explicitly changes the task.
- Per-task execution fixtures must describe documentation-only work. They must forbid modifying production code, tests, manifests, schemas, migrations, runtime scripts, and generated runtime artifacts.
- Every task must specify its exact detailed design document filename under `docs/design/`.
- Every ready plan must include one final documentation-only design acceptance task after all design tasks. It must not implement code; it reviews the completed design document set and writes an acceptance report under `docs/design/`.
- Do not invent requirements, APIs, data fields, runtime components, acceptance commands, or Rust libraries.
- Follow the HLD's Rust technology stack. If it is absent or conflicting, block the affected design area.
- Treat unresolved interface docs, real acceptance environment, data source, permissions, or architectural decisions as blockers when they affect implementation readiness.

## Ready Gates

A ready design-planning result must satisfy all of these:

- Every material PRD/HLD source is listed in the source inventory.
- Every current-phase requirement and acceptance criterion maps to design tasks or explicit deferred/blocking rationale.
- Control flow and data flow are described step by step.
- Rust module boundaries, traits, data types, error types, ownership/lifetime expectations, async/concurrency model, and persistence/state boundaries are explicit where relevant.
- Key technical choices cite PRD/HLD or target-project evidence.
- The DAG is acyclic and every dependency has a semantic reason.
- Parallel groups do not share unresolved decisions, files, schemas, interfaces, state, or acceptance evidence.
- Every ready task has a fixture folder with `prompt.md`, `AGENTS.md`, and `CLAUDE.md`.
- Fixture files are task-scoped, source-backed, and not one-line redirects.
- A final design acceptance task exists, depends on all detailed design document tasks, and checks source traceability, requirement coverage, DAG consistency, control flow, data flow, interface contracts, state/persistence, errors, security, observability, verification strategy, risks, and no-code-change compliance.
- The harness validator passes against the generated target output.
- No standalone starter prompt template artifact is produced.

## Common Mistakes

| Mistake | Correct Behavior |
| --- | --- |
| Treating design planning as implementation | Produce design docs and agent instructions only. |
| Reading only file names in `docs` | Read PRD/HLD deeply enough to design control flow, data flow, and Rust boundaries. |
| Creating generic tasks | Create source-backed design tasks with concrete outputs and verification. |
| Putting all tasks in one vague prompt | Emit one fixture folder per task with task-specific prompt, AGENTS.md, and CLAUDE.md. |
| Assuming Rust libraries | Use HLD/source evidence, or block and request the decision. |
| Producing a DAG without edge reasons | Every edge names the consumed output, decision, interface, schema, state model, or verification result. |
