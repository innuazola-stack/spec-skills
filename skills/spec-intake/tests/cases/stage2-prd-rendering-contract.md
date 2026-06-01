# Eval Case: Stage 2 PRD Rendering Contract

## Prompt

Use `spec-intake` Stage 2 to render PRDs from a validated requirement table for an executor product.

The Stage 1 contract already confirms a local CLI input, ClaudeTmuxAdapter public-boundary integration, structured JSON result plus execution log, and separate agent/reviewer completion acceptance.

## Expected Behavior

- Render both PRDs only from `contract-envelope.json.requirement_table` and canonical objects.
- Validate the PRD-only package with `validate_spec_intake_package.py <output-dir> --stage stage2`.
- Render `agent-prd.md` in English for another agent.
- Agent PRD must be an execution-ready PRD, not merely an execution note. It must include a complete product PRD body with metadata, executive summary, problem/background, target users/personas, goals/outcomes, success metrics, scope/non-goals, user stories/use cases, functional requirements, non-functional guardrails, user flow/UX notes, acceptance criteria, release plan/roadmap, risks/assumptions/dependencies, open questions, and traceability.
- Agent PRD must also include an agent execution appendix with source of truth, mission, requirement trace, input, execution, tool/integration boundaries, permissions/safety, data/state, verification, output, stop, done, and forbidden assumptions.
- Agent PRD sections must contain non-trivial body text and visibly cover current-phase requirement, acceptance, verification, input, execution, output, stop, and done refs.
- Agent PRD must visibly cover non-empty implementation-model refs such as control flow, data flow, modules, technical decisions, states, and data contracts; execution-like products must show the major loop, external component method boundary, state handling, judgment boundary, evidence output, and mechanical delivery checks when present in the contract.
- Render `human-prd.md` in professional, formal Simplified Chinese as a concise but information-dense brief, not a full execution contract.
- Human PRD must include revision record first, then product goal, construction scope, implementation approach, acceptance criteria and methods, roadmap, risks/open decisions, and references last.
- Human PRD must use concrete information from canonical refs, include source markers in substantive sections, avoid workflow process markers, and use structured forms such as tables or diagrams where they improve readability.
- Human PRD core sections must be concrete enough for review; headings plus citations are not sufficient.
- Human PRD implementation approach must summarize material execution topology from the contract at human-review depth rather than hiding it behind generic "call adapter" wording.
- Stage 2 may use the real PRD quality reference package to calibrate depth, traceability, and review usefulness, but it must not import reference-package domain facts into the current product.
- Present Human PRD for review and keep Stage 3 blocked until approval is recorded as `SRC.source_type=user_confirmation`.
- Contract summary must show Stage 1 and Stage 2 ready, must not mark Stage 3 ready, and must keep Stage 3 blocked while Human PRD review is pending.

## Forbidden Behavior

- Do not add facts absent from the requirement table or canonical objects.
- Do not make Human PRD a full English Agent PRD or include agent-only sections such as `Execution Contract` or `Tool and Integration Boundaries`.
- Do not make Human PRD a thin generic summary with no concrete goal, scope, approach, acceptance method, roadmap, or evidence.
- Do not make Human PRD a citation-only brief.
- Do not include process markers such as `Source contract:`, `Render status:`, or `render_status` in Human PRD.
- Do not make Agent PRD a short human summary.
- Do not make Agent PRD only an execution contract, contract-ref index, or instruction sheet.
- Do not copy executor-specific requirements, component names, method names, CLI names, acceptance criteria, or roadmap items from the quality reference into an unrelated Stage 2 package.
- Do not mark Agent PRD `execution_ready` while required execution objects, verification, output, stop, or done refs are absent.
- Do not mark Agent PRD `execution_ready` while product PRD essentials such as user/problem, goals, success metrics, requirements, acceptance, roadmap, risks, assumptions, dependencies, or traceability are absent.
- Do not enter Stage 3 without Human PRD approval evidence.
- Do not produce HLD, task plans, task graphs, dependency edges, parallel groups, or implementation task cards in the Stage 2 package.

## Scoring Rule

Pass if the Stage 2 validator passes, semantic review confirms Agent PRD is a complete English execution-ready PRD with both product body and agent execution appendix, non-empty implementation-model refs are rendered into concrete execution topology, Human PRD is concise, formal, information-dense, Chinese, source-marked, and useful for human approval, both are traceable to the Stage 1 contract, the quality reference was used only as a quality bar and not as current-product evidence, contract summary matches the Stage 2 gate state, and Stage 3 remains gated by Human PRD approval.

## Pass Bar

`pass`
