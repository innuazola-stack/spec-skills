# Design Planning Brief

## Mission

Create a reusable review-gated harness workflow that guides Claude/Codex to read PRD/HLD documents from a Rust target project's `docs/` directory and produce harness-governed detailed design planning.

## Target Type

`harness-workflow`

## Harness Paradigm

`review-gated`

The workflow owns staged planning, task formation, single-task review, global DAG review, artifact generation, and final design acceptance.

## Non-Goals

- Do not implement product code.
- Do not write or rewrite PRD/HLD.
- Do not create standalone starter prompt templates.
- Do not implement product-specific runtime behavior inside adapters; adapters only preserve harness instructions for each supported agent runtime.

## Canonical Outputs

- `<planning-output-root>/design-planning.json`
- `docs/design/rust-implementation-design.md`
- `<planning-output-root>/fixtures/<TASK-ID>/prompt.md`
- `<planning-output-root>/fixtures/<TASK-ID>/AGENTS.md`
- `<planning-output-root>/fixtures/<TASK-ID>/CLAUDE.md`
- `docs/design/<TASK-ID>-*-design.md` task deliverable paths
- final `docs/design/*acceptance-review.md` design acceptance report path

## Required Hardening

- Harness core files: `manifest.yaml`, `agent.md`, `workflow.md`, `rules.md`.
- Machine-readable schema: `schemas/design-planning.schema.json`.
- Structural validator: `validators/validate_design_planning.py`.
- Evaluation cases with scoring and pass bar.
