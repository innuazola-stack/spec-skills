# Eval Case: Stage 3 HLD Writer Implementation Design

## Prompt

Use `spec-intake` Stage 3 to produce HLD from an approved PRD package and validated requirement table.

## Expected Behavior

- Require PRD review approval evidence backed by `SRC.source_type=user_confirmation`.
- Require approval artifact bindings for current `prd.md` and `prd-brief.md`.
- Call `hld-writer` to produce `high-level-design.json`, `high-level-design.md`, and `hld-semantic-review.json`.
- HLD must make data flow, control flow, data objects, interaction interfaces, state model, technical decisions, implementation details, and real acceptance method directly readable.
- HLD must define real environment, real data, executable command, expected artifacts, mechanical checks, failure criteria, evidence capture, and acceptance owner without mock content.
- HLD must not include task decomposition.
- Final package validator must pass.

## Forbidden Behavior

- Do not write HLD without `hld-writer`.
- Do not use legacy Human/Agent PRDs as source artifacts.
- Do not mark HLD ready without PRD review approval.
- Do not use mock, stub, fake, simulated, synthetic, placeholder, or deferred acceptance inputs.
- Do not output task plans, task graphs, dependency edges, parallel groups, or implementation task cards.

## Scoring Rule

Pass if final validation passes, HLD is implementation-ready, `hld-semantic-review.json` passes every required dimension, source refs align with `contract-envelope.json` and approved PRD artifacts, and no task output is present.

## Pass Bar

`pass`
