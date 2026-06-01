# Development Planning Skill Brief

## Mission

Create a reusable harness workflow that guides Claude/Codex to read PRD/HLD/LLD documents from a target project's `docs/` directory and produce planning-only JSON development planning, a DAG of cohesive tasks, per-task descriptions, and per-task execution support files.

## Harness Type

Harness workflow. The main risk is staged reasoning quality and enforceability: source interpretation, development task cohesion, independent acceptance, DAG soundness, execution order, durable instruction boundaries, and validator-backed readiness.

The harness owns staged planning gates and parent-consumable verdicts. It does not own delegated multi-agent execution, approvals, release packaging, or live E2E evidence for the product being planned.

## Non-Goals

- No product implementation; this is a planning task.
- No PRD/HLD/LLD generation.
- No standalone starter prompt template.
- No multi-stage harness or runtime adapter.

## Output Contract

The target project receives:

- `tasks/development/development-planning.json`
- `tasks/development/<TASK-ID>/task.md`
- `tasks/development/<TASK-ID>/prompt.md`
- `tasks/development/<TASK-ID>/AGENTS.md`
- `tasks/development/<TASK-ID>/CLAUDE.md`

## Quality Bar

The skill is acceptable when it forces source-backed PRD/HLD/LLD reading, harness-style overall planning, independent task formation, task logic review, whole-plan integrity review, cohesive independently acceptable development task descriptions, JSON DAG/task output with dependency reasons, execution order and parallel groups, per-task execution support files, blocked output for missing evidence, and one final delivery acceptance task.
