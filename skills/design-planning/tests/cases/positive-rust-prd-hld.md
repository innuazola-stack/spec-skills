# Positive Case: Rust PRD/HLD Ready

## Target Shape

```text
target/
  docs/
    prd.md
    hld.md
  Cargo.toml
  src/
```

## Source Conditions

- PRD defines current-phase requirements, acceptance criteria, and non-goals.
- HLD defines Rust stack, crate/module approach, control flow, data flow, interface boundaries, state model, and acceptance method.
- Source tree confirms Rust workspace or crate conventions.

## Expected Skill Behavior

- Inventory `docs/prd.md` and `docs/hld.md`.
- Write `<planning-output-root>/design-planning.json` with `tasks`, `dag`, `planning_review_stages`, and gate report.
- Write `docs/design/rust-implementation-design.md`.
- Write `<planning-output-root>/fixtures/<TASK-ID>/prompt.md`, `AGENTS.md`, and `CLAUDE.md` for each ready task.
- Each detailed design task has `task_type=detailed_design` and one exact `docs/design/*.md` `design_doc_path`.
- One final task has `task_type=design_acceptance` and depends on every detailed design task.
- Generated planning passes `validators/validate_design_planning.py`.
- Include Rust design coverage for modules, traits, data types, errors, state, async/concurrency, persistence, tests, and acceptance where relevant.
- Do not create a standalone starter prompt template file.
