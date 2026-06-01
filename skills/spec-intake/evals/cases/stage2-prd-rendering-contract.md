# Eval Case: Stage 2 PRD Writer Contract

## Prompt

Run `spec-intake` Stage 2 from a validator-clean Stage 1 package for an execution-like product. Produce the PRD package and stop for review.

## Expected Behavior

- Call `prd-writer` to produce `prd.md`.
- Derive `prd-brief.md` from `prd.md` and `contract-envelope.json`.
- `prd.md` must be a complete standard PRD with metadata, executive summary, problem/background, target users/personas, goals/outcomes, success metrics, scope/non-goals, use cases, functional requirements, non-functional guardrails, implementation approach, acceptance criteria, release plan/roadmap, risks/assumptions/dependencies, open questions, and traceability.
- `prd.md` must visibly cover current-phase requirement, acceptance, verification, input, execution, output, stop, done, and non-empty implementation-model refs.
- `prd-brief.md` must be professional Simplified Chinese, concise, formal, source-marked, and information-dense.
- `prd-brief.md` must include revision record first, then product goal, construction scope, implementation approach, acceptance criteria and methods, roadmap, risks/open decisions, and references last.
- Present `prd.md` and `prd-brief.md` for review and keep Stage 3 blocked until approval is recorded as `SRC.source_type=user_confirmation`.
- Contract summary must show Stage 1 and Stage 2 ready, must not mark Stage 3 ready, and must keep Stage 3 blocked while PRD review is pending.
- `validate_spec_intake_package.py <output-dir> --stage stage2` must pass.

## Forbidden Behavior

- Do not create `human-prd.md` or `agent-prd.md`.
- Do not handwrite `prd.md` when `prd-writer` is required.
- Do not make `prd.md` only an execution contract, contract-ref index, or instruction sheet.
- Do not make `prd-brief.md` a thin generic summary with no concrete goal, scope, approach, acceptance method, roadmap, or evidence.
- Do not include process markers such as `Source contract:`, `Render status:`, or `render_status` in `prd-brief.md`.
- Do not enter Stage 3 without PRD review approval evidence.

## Scoring Rule

Pass if the Stage 2 validator passes, semantic review confirms `prd.md` is a complete standard PRD produced by `prd-writer`, material implementation-model refs are rendered into concrete implementation topology, `prd-brief.md` is concise, formal, information-dense, Chinese, source-marked, and useful for human approval, both artifacts trace to the Stage 1 contract, and Stage 3 remains gated by PRD review approval.

## Pass Bar

`pass`
