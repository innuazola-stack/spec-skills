# Spec Intake Rules

## Authority

1. User-provided facts and confirmations
2. Provided source documents
3. Bounded inferences from cited facts
4. Assumptions and open questions

Lower authority may not overwrite higher authority. Assumptions and open questions never become ready facts until resolved or explicitly deferred as non-blocking.

## Question Rules

- Ask at most three clarification questions per round.
- Questions must be `boolean`, `single_choice`, or `multi_choice`.
- Each question must include explicit options.
- Open-text questions are forbidden.
- If unresolved blocking `Q-*` or `ASM-*` exists, `interaction_decision` may not be `proceed_without_questions`.

## Artifact Rules

- `contract-envelope.json` is canonical.
- `harness_workflow.execution_mode` is required and must be `live_interactive` for a real user-facing run or `reference_replay` for non-interactive regression/reference validation.
- A `reference_replay` package may prove validator behavior or document quality, but it must not mark Stage 3 or the full workflow as a completed live execution.
- `interaction_decision` is the Stage 1 gate record for asking, proceeding, or blocked draft output.
- `requirement_table` is the Stage 1 table consumed by `prd-writer`, `prd-brief.md`, and `hld-writer`.
- Requirement-table row origins must match evidence: facts cite `SRC-*`, assumptions cite `ASM-*`, open questions cite `Q-*`, and bounded inference cites `SRC-*` plus `TRACE.relation=inferred_from`.
- Execution-like ideas require source-backed execution topology before ready rendering: external components, public interface boundaries, control flow, modules, technical decisions, state handling, evidence outputs, judgment boundaries, and mechanical delivery checks when material.
- Stage 2 must call `prd-writer` to create `prd.md`; spec-intake may only validate that PRD and derive `prd-brief.md`.
- Stage 2 must not create `human-prd.md` or `agent-prd.md`.
- Stage 3 must call `hld-writer` to create HLD outputs.
- HLD is the only Stage 3 output family. It consists of `high-level-design.json` as structured source, `high-level-design.md` as the formal HLD document, and `hld-semantic-review.json` as the independent semantic review artifact.
- A JSON-only HLD is incomplete. Ready Stage 3 must include a readable HLD document with scope/goals, architecture overview, control flow, data flow, data objects, interface contracts, state model, technical decisions, implementation design, real acceptance plan, risks/guardrails, references, diagrams, tables, and current design refs.
- PRD review approval must be an explicit user-confirmation source for `prd_review_approval`, must authorize entering Stage 3, and must bind to the exact `prd.md` and `prd-brief.md` sha256 values being consumed.
- Ready HLD must be an implementation design, not a summary. It must include structured control flow, data flow, data objects, interface contracts, state model, technical decisions, implementation design, environment requirements, and a real acceptance plan.
- Stage 3 may ask the user for missing HLD information such as real environment, real data, interface documentation, permissions, deployment constraints, or acceptance ownership. Unknown HLD-critical facts must become questions, blockers, or required fixes; they must not become design assumptions.
- HLD acceptance must use concrete confirmed real environment and real data with `SRC-*` evidence refs for environment, data, and acceptance owner. Mock, stub, fake, simulated, synthetic, deferred, placeholder, `TBD`, and "to be provided later" substitutes are forbidden in ready HLD.
- Ready HLD must include fixed HLD design gates with `gate_key` values for source readiness, control flow, data/data objects, interface/state, technical implementation, real acceptance, HLD document readiness, and task boundary. A generic single pass gate cannot make HLD ready. These internal design gates do not replace the independent `hld-semantic-review.json`.
- Task plan files, task graphs, dependency edges, and parallel groups are forbidden outputs.

## Validation Rules

- Run `skill/scripts/validate_spec_intake_package.py <output-dir> --stage stage1` before claiming Stage 1 is complete.
- Run `skill/scripts/validate_spec_intake_package.py <output-dir> --stage stage2` before treating the PRD package as reviewable.
- Run `skill/scripts/validate_spec_intake_package.py <output-dir>` when a final package exists.
- Run `tests/validator_regression.py` during repository development.
- A failed validator blocks ready status.
- Semantic review can downgrade a structurally valid package when product meaning is weak, invented, or not useful.
- The validator must reject legacy Human/Agent PRD artifacts, generic approval evidence, and reference replay packages that claim completed live Stage 3 readiness.

## Done Rule

Do not claim completion unless the final answer reports validator evidence, semantic status, and any skipped checks or residual risks.
