# Eval Case: Stage 1 PRD Support Coverage

## Prompt

Use `spec-intake` to run Stage 1 intake for a CLI executor.

The executor should run a task through an existing adapter. The idea mentions a CLI and the adapter, but does not define target users, MVP boundary, acceptance method, output contract, stop conditions, done criteria, or roadmap.

## Expected Behavior

- Produce a Stage 1 package with `contract-envelope.json` only.
- Validate the package with `validate_spec_intake_package.py <output-dir> --stage stage1`.
- Record source facts without inventing missing product or execution details.
- Set `interaction_decision=ask_user` or `blocked_draft`; do not set `proceed_without_questions` unless PRD-ready support is present.
- Ask only boolean, single-choice, or multi-choice questions.
- Questions must target the missing Stage 2 support: target-user posture, MVP boundary, acceptance/verification method, output/done contract, and stop conditions.
- For executor-like ideas, questions or blocked refs must also cover execution topology: external component boundary, source availability, control flow, state handling, judgment boundary, evidence output, and mechanical delivery check.
- If the package remains blocked, represent missing support through `Q-*`, `ASM-*`, `STOP-*`, or `GATE-*` refs and affected target blockers.

## Forbidden Behavior

- Do not proceed to Stage 2 from a requirement table that cannot support both PRDs.
- Do not fill users, roadmap, acceptance method, output, stop, or done criteria with invented facts.
- Do not produce Human PRD, Agent PRD, HLD, task plans, task graphs, dependency edges, parallel groups, or implementation task cards in the Stage 1 package.

## Scoring Rule

Pass if the Stage 1 package validator passes and semantic review confirms that `proceed_without_questions` appears only when product context, user posture, MVP scope, acceptance/verification, implementation approach, execution topology, source evidence, and `IN`/`EXE`/`VER`/`OUT`/`STOP`/`DONE` refs are all source-backed.

## Pass Bar

`pass`
