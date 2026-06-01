---
name: design-planning
description: Use when a Rust target project has PRD/HLD documents under docs and needs harness-governed JSON design planning, detailed-design document tasks, per-task execution fixtures, and final design acceptance.
---

# Design Planning

This skill is the Codex entrypoint for the `design-planning` harness workflow.

Use the harness core in this directory as the source of truth:

- `manifest.yaml`
- `agent.md`
- `workflow.md`
- `rules.md`
- `schemas/design-planning.schema.json`
- `validators/validate_design_planning.py`

The workflow reads PRD/HLD under the target project's `docs/`, produces canonical JSON planning under the planning output root, writes all detailed design documents under the target repository's `docs/design/`, emits per-task execution fixtures containing the single-task prompt plus task-scoped `AGENTS.md` and `CLAUDE.md`, and validates the result with the harness validator.

## Harness Type

`harness-workflow`: review-gated workflow.

## Required Outputs

Write these files in the target project:

- `<planning-output-root>/design-planning.json`: canonical planning output containing the DAG and task list.
- `docs/design/rust-implementation-design.md`
- `<planning-output-root>/fixtures/<TASK-ID>/prompt.md`
- `<planning-output-root>/fixtures/<TASK-ID>/AGENTS.md`
- `<planning-output-root>/fixtures/<TASK-ID>/CLAUDE.md`

The default planning output root is `tasks/design`. If the user explicitly requests another planning or task output root, use that requested root and record it in `design-planning.json` as `output_root`. Detailed design documents are fixed under target `docs/design/`.

## References

Load only what the task needs:

- `agent.md`: role, boundaries, inputs, outputs, and done criteria.
- `workflow.md`: stage graph and gate contracts.
- `rules.md`: authority, file, no-code, task, acceptance, and validation rules.
- `skill/references/methodology.md`: source reading, boundaries, task decomposition, DAG rules, and blocker criteria.
- `skill/references/rust-detailed-design.md`: Rust-specific detailed design checklist.
- `skill/references/output-contract.md`: target output file contracts and readiness gates.
- `skill/assets/TASK_PROMPT.fixture.md`: per-task prompt fixture template.
- `skill/assets/AGENTS.template.md`: per-task `AGENTS.md` fixture template.
- `skill/assets/CLAUDE.template.md`: per-task `CLAUDE.md` fixture template.
- `schemas/design-planning.schema.json`: machine-readable planning output shape.
- `validators/validate_design_planning.py`: structural validator for generated planning.

## Workflow

Follow `workflow.md`:

1. Inventory and interpret PRD/HLD sources under target `docs/`.
2. Decompose current-phase detailed design obligations into documentation-only tasks.
3. Assign each detailed design task one exact `docs/design/*.md` output path.
4. Build an acyclic DAG with semantic edge reasons.
5. Emit task-scoped fixtures under `<planning-output-root>/fixtures/<TASK-ID>/`.
6. Add one final `design_acceptance` task that depends on every detailed design task.
7. Run `validators/validate_design_planning.py` before claiming readiness.

## Hard Rules

- PRD/HLD inputs are fixed under target `docs/`.
- Planning and task fixture outputs use `tasks/design/` by default unless the user explicitly specifies another planning output root.
- Detailed design document outputs are fixed under target `docs/design/`.
- DAG and task list must be JSON, not only Markdown prose.
- No standalone starter prompt template is produced.
- Do not write implementation code unless the user explicitly changes the task.
- Per-task execution fixtures must describe documentation-only work and forbid modifying production code, tests, manifests, schemas, migrations, runtime scripts, and generated runtime artifacts.
- Every task must specify its exact detailed design document filename under `docs/design/`.
- Every ready plan must include one final documentation-only design acceptance task after all design tasks.
- Do not invent requirements, APIs, data fields, runtime components, acceptance commands, or Rust libraries.
- Follow the HLD's Rust technology stack. If it is absent or conflicting, block the affected design area.

## Ready Gates

- Every material PRD/HLD source is listed in the source inventory.
- Every current-phase requirement and acceptance criterion maps to design tasks or explicit deferred/blocking rationale.
- Control flow and data flow are described step by step.
- Rust module boundaries, traits, data types, error types, ownership/lifetime expectations, async/concurrency model, and persistence/state boundaries are explicit where relevant.
- The DAG is acyclic and every dependency has a semantic reason.
- Every ready task has `prompt.md`, `AGENTS.md`, and `CLAUDE.md`.
- A final design acceptance task exists, depends on all detailed design document tasks, and checks the completed design document set.
- The harness validator passes against the generated target output.
