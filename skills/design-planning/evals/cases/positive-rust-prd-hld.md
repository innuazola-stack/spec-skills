# Positive Case: Rust PRD/HLD Ready

## Prompt

Use `design-planning` on a Rust target project whose `docs/` directory contains complete PRD and HLD sources for the current implementation phase.

## Expected Behavior

- Inventory all material PRD/HLD and related architecture sources under `docs/`.
- Write `tasks/design/design-planning.json` unless the user explicitly provides another planning output root.
- Write `docs/design/rust-implementation-design.md`.
- Record `planning_review_stages` for overall planning, task formation, single-task review, global DAG review, artifact generation, and final design acceptance.
- Produce documentation-only `detailed_design` tasks, each with one exact `docs/design/*.md` `design_doc_path`.
- Produce one `design_acceptance` task that depends on every detailed design task.
- Write per-task `prompt.md`, `AGENTS.md`, and `CLAUDE.md` fixtures under `<planning-output-root>/fixtures/<TASK-ID>/`.
- Pass `validators/validate_design_planning.py` against the generated target output.

## Forbidden Behavior

- Creating implementation/code-writing tasks.
- Writing planning JSON or fixtures under `docs/design` by default.
- Missing exact `docs/design/*.md` design document paths.
- Missing final design acceptance task.
- Creating a standalone starter prompt template.

## Scoring Rule

Score 0-2 for source inventory, staged harness output, JSON planning shape, DAG soundness, fixture completeness, documentation-only enforcement, exact design document paths, final acceptance correctness, Rust design coverage, and validator evidence.

## Pass Bar

Pass requires at least 18 of 20 points, no zero score, and full score for documentation-only enforcement, exact design document paths, final acceptance correctness, and validator evidence.
