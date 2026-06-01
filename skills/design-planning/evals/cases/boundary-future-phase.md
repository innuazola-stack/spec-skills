# Boundary Case: Future Phase Leakage

## Prompt

Use `design-planning` on a Rust target project whose PRD/HLD contains current Phase 1 requirements plus future Phase 2 features. The user asks for detailed design readiness for the current implementation phase.

## Expected Behavior

- Keep the current-phase detailed design DAG focused on Phase 1.
- Include future-phase work only as deferred or preparatory design when PRD/HLD explicitly require it.
- Record source-backed deferral rationale in the coverage matrix.
- Keep `planning_review_stages` and final design acceptance focused on current-phase detailed design readiness.
- Prevent dependency edges from current tasks to deferred future-phase tasks.

## Forbidden Behavior

- Future-phase task nodes in the current DAG without explicit PRD/HLD preparation evidence.
- Hidden dependency edges from current tasks to deferred future-phase work.
- Broad task prompts that invite implementation or speculative product design.

## Scoring Rule

Score 0-2 for current-phase scope fidelity, deferred-work handling, DAG dependency correctness, source traceability, and final acceptance focus.

## Pass Bar

Pass requires at least 9 of 10 points, no zero score, and full score for current-phase scope fidelity and DAG dependency correctness.
