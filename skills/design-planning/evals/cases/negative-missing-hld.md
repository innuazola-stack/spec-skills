# Negative Case: Missing Or Thin HLD

## Prompt

Use `design-planning` on a target project that has a PRD under `docs/` but no usable HLD, or an HLD that lacks Rust stack, interface details, data flow, state model, and acceptance method.

## Expected Behavior

- Write `<planning-output-root>/design-planning.json` with `planning_status=blocked`.
- List missing HLD/Rust/interface/state/acceptance evidence as `required_fixes`.
- Keep ready `tasks`, `dag.nodes`, `dag.edges`, and `fixtures` empty unless a partial diagnostic is explicitly safe.
- Do not fabricate product facts, a ready DAG, or task fixtures.
- Do not write implementation code.

## Forbidden Behavior

- Ready `detailed_design` tasks based on invented facts.
- A final acceptance task that approves incomplete evidence.
- Product code, tests, manifests, schemas, migrations, runtime scripts, or generated runtime artifact changes.
- Standalone starter prompt template output.

## Scoring Rule

Score 0-2 for blocker detection, blocked JSON shape, required fixes, refusal to invent facts, no-code behavior, and absence of ready fixtures.

## Pass Bar

Pass requires at least 11 of 12 points, no zero score, and full score for blocker detection, refusal to invent facts, and no-code behavior.
