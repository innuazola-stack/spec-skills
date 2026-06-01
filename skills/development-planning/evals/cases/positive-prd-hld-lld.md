# Positive Case

## Prompt

Use development-planning on this target project. Read PRD/HLD/LLD under ./docs and produce planning only. The planning must write task descriptions to tasks/development, include cohesive independently acceptable development tasks, a DAG and execution order as JSON, plus per-task support files containing prompt.md, CLAUDE.md, and AGENTS.md.

Fixture: `evals/fixtures/positive-prd-hld-lld`.

## Expected Behavior

- Read `docs/prd.md`, `docs/hld.md`, and `docs/lld.md`.
- Write `tasks/development/development-planning.json` with `planning_status=ready`.
- Include `planning_harness_model.target_type=harness-workflow`, all four `phase_reports`, `task_logic_review.status=pass`, and `plan_integrity_review.status=pass`.
- Include cohesive tasks with clear boundaries, constraints, verification, and independent acceptance.
- Include a DAG with edge reasons, consumed outputs, parallel groups, and execution order.
- Include exactly one final `delivery_acceptance` task depending on every non-deferred implementation task.
- Write `tasks/development/<TASK-ID>/task.md`, `prompt.md`, `AGENTS.md`, and `CLAUDE.md` for every ready task.
- Pass `validators/validate_development_planning_package.py` against the generated package.
- Do not implement product code.

## Forbidden Behavior

- Markdown-only task planning.
- Ready planning without the four harness stages.
- Ready planning with missing task-level or whole-plan review results.
- Generic all-task prompts instead of per-task contracts.
- Any product code change.

## Scoring Rule

Score 0-2 for source reading, staged planning, task cohesion, independent acceptance, task logic review, whole-plan integrity review, DAG quality, task contract completeness, final acceptance, and planning-only behavior.

## Pass Bar

Pass requires at least 19 of 20, no zero dimensions, and full score for staged planning, task logic review, whole-plan integrity review, DAG quality, and final acceptance.
