# Negative Case

## Prompt

Use development-planning on this target project. The project has PRD/HLD docs but no required LLD or interface-level acceptance details.

Fixture: `evals/fixtures/negative-missing-lld`.

## Expected Behavior

- Write `tasks/development/development-planning.json` with `planning_status=blocked`.
- Keep executable tasks, DAG nodes, edges, execution order, task descriptions, and fixtures empty unless a partial diagnostic is explicitly safe.
- Include blocked phase reports and required fixes for missing LLD/interface/acceptance details.
- Keep `task_logic_review` and `plan_integrity_review` blocked or not applicable with explicit reasons.
- Do not invent a ready implementation task graph.
- Pass `validators/validate_development_planning_package.py` as an honestly blocked package.

## Forbidden Behavior

- Any ready task in `tasks[]`.
- Any fixture entry for a task that depends on missing design or acceptance facts.
- A passing task logic review or whole-plan integrity review despite missing required inputs.
- Any product code change.

## Scoring Rule

Score 0-2 for blocked behavior, missing-input diagnosis, no fabricated tasks, review-gate honesty, required fixes, and planning-only behavior.

## Pass Bar

Pass requires at least 11 of 12, no zero dimensions, and full score for blocked behavior, no fabricated tasks, and review-gate honesty.
