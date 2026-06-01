# Boundary Case

## Prompt

Use development-planning on this target project. PRD/HLD/LLD exists, but it also mentions a future-phase feature that is not part of the current delivery phase.

## Expected Behavior

- Plan only current-phase implementation tasks.
- Record future-phase work as deferred or out of scope unless source docs explicitly require preparatory work now.
- Include the future-phase decision in overall planning, task logic review, and whole-plan integrity review.
- Do not include dependency edges from current tasks to deferred future-phase tasks.
- Keep the final delivery acceptance task focused on current delivery scope.

## Forbidden Behavior

- Future-phase task nodes in the current-phase DAG without explicit PRD/HLD/LLD preparation evidence.
- Dependency edges from current tasks to deferred future-phase tasks.
- Whole-plan integrity review passing without explaining future-phase isolation.
- Any product code change.

## Scoring Rule

Score 0-2 for current-phase fidelity, deferred-work handling, DAG isolation, review-gate coverage, final acceptance focus, and planning-only behavior.

## Pass Bar

Pass requires at least 11 of 12, no zero dimensions, and full score for current-phase fidelity, DAG isolation, and review-gate coverage.
