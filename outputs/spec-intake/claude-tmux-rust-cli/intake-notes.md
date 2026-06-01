# Intake Notes

Source contract: `REF-001` (`contract-envelope.json`)

## Source

The user requested a Rust CLI wrapper around Claude CLI with five mechanical tmux operations: launch, capture, status detection, input, and termination.

## Clarification Decision

No clarification was required before creating an execution-ready package because the user explicitly supplied the core product, target runtime shape, five required capabilities, mechanical-only constraint, 1-second input confirmation rule, and 99% idle/busy accuracy targets.

## Non-blocking Assumptions

- `ASM-001`: local Unix-like runtime with tmux and Claude CLI available.
- `ASM-002`: permission settings can be represented by CLI args, environment variables, or generated config files.
- `ASM-003`: 99% accuracy is measured on an implementation-owned labeled screen fixture corpus.

These assumptions are non-blocking because the implementation tasks include validation and stop behavior for unavailable runtime dependencies and release evidence for the accuracy target.

## Readiness

Human PRD is `review_ready`. Agent PRD is `execution_ready`. Task planning is `ready` for `PHASE-001`.

## Package References

- `REF-001`: canonical structured contract, `contract-envelope.json`.
- `REF-002`: rendered human PRD, `human-prd.md`.
- `REF-003`: rendered agent PRD, `agent-prd.md`.
- `REF-004`: rendered execution task plan, `execution-task-plan.json`.
