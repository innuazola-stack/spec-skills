# Boundary Case: Future Phase Leakage

## Target Shape

```text
target/
  docs/
    prd.md
    hld.md
```

## Source Conditions

- PRD/HLD define current Phase 1 plus a future Phase 2 feature.
- User asks for detailed design readiness for current implementation.

## Expected Skill Behavior

- Keep current-phase detailed design and DAG focused on Phase 1.
- Include future-phase work only as deferred or preparatory design when PRD/HLD explicitly require it.
- Record source-backed deferral rationale in coverage matrix.
- Keep `planning_review_stages` and final design acceptance focused on the current phase.
- Do not let future-phase work create false dependencies in the current DAG.
