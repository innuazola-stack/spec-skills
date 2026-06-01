# Negative Case: Missing Or Thin HLD

## Target Shape

```text
target/
  docs/
    prd.md
```

## Source Conditions

- PRD exists.
- HLD is missing, or the available HLD omits Rust stack, interface details, data flow, state model, and acceptance method.

## Expected Skill Behavior

- Write `<planning-output-root>/design-planning.json` with `planning_status=blocked`.
- Explain missing HLD/Rust/interface/state/acceptance evidence as required fixes.
- Do not fabricate a ready DAG.
- Do not emit ready task fixtures.
- Do not write implementation code.
- Do not create a standalone starter prompt template file.
