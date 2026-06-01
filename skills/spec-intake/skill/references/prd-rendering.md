# PRD Writer And Brief Rendering

Use this reference in Stage 2 after Stage 1 has produced a validator-clean `contract-envelope.json`.

Stage 2 has two outputs:

- `prd.md`: standard PRD document produced by `prd-writer`.
- `prd-brief.md`: concise, formal Simplified Chinese review brief derived from `prd.md` and `contract-envelope.json`.

`spec-intake` does not own the canonical PRD body. If `prd-writer` is unavailable, Stage 2 must produce a blocked package instead of writing an ad hoc replacement. `human-prd.md` and `agent-prd.md` are legacy artifacts and are forbidden.

Stage 2 must record `writer_invocations.prd`. A review-ready PRD package requires `status=completed`, `writer_skill=prd-writer` or `prd-writing`, a `SRC.source_type=system_generated` source ref, canonical `input_refs`, and an `output_artifacts` entry for `prd.md` with sha256. If the writer is unavailable or fails, set `status=unavailable`, `failed`, or `blocked`, include `required_fix`, keep `render_status.prd=blocked` and `render_status.prd_brief=blocked`, and keep Stage 3 blocked.

Neither document is a new source of product truth. If a PRD needs a fact that is missing from `contract-envelope.json`, return to Stage 1 and update the requirement table first.

Use `prd-quality-reference.md` as a quality bar for depth, traceability, and review usefulness. It is a reference package, not a current-product source. Do not copy its domain facts, component names, interface details, acceptance rules, or roadmap items into the current PRD unless those facts also exist in the current `contract-envelope.json`.

## Best-Practice Basis

The Stage 2 rules combine common PRD guidance and agent-readable specification guidance:

- PRDs align teams around what is being built, who it benefits, objectives, assumptions, scope, dependencies, and release requirements.
- Strong product goals are measurable and tied to roadmap decisions.
- Useful implementation-facing PRDs preserve control flow, data flow, interfaces, acceptance, and constraints without drifting into task decomposition.
- Human review briefs need clear purpose, scope, approach, acceptance, roadmap, risks, and source evidence.
- Agent systems need explicit permissions, safety boundaries, and evaluation criteria when execution behavior is part of the product.

## `prd.md`

Audience: human product reviewers, engineering designers, and downstream agents.

Language: use the language required by `prd-writer`; when unspecified, prefer English for the canonical standard PRD so downstream agents can consume it reliably.

Purpose: define the product decision and requirements in a complete, traceable, HLD-ready PRD. It is not an implementation task list and not a loose summary.

A review-ready standard PRD must include:

- `Document Metadata`
- `Executive Summary`
- `Problem and Background`
- `Target Users and Personas`
- `Goals and Outcomes`
- `Success Metrics`
- `Scope and Non-Goals`
- `User Stories and Use Cases`
- `Functional Requirements`
- `Non-Functional Requirements and Guardrails`
- `Implementation Approach`
- `Acceptance Criteria`
- `Release Plan and Roadmap`
- `Risks, Assumptions, and Dependencies`
- `Open Questions`
- `Traceability`

Each section must cite canonical IDs from the contract where relevant. The PRD must not introduce implementation details, technologies, tools, permissions, data fields, tests, or acceptance rules that are absent from the requirement table or canonical objects. If a useful PRD fact is missing from the contract, either derive it from an explicit requirement-table row or mark it as an open question/assumption and downgrade readiness if it blocks product clarity, verification, output, safety, or execution.

When the contract contains execution or implementation-model refs, the PRD must make them visible and useful, not merely cite them. Cover non-empty `FLOW`, `DATA`, `MOD`, `TECH`, `STATE`, `DCT`, `IN`, `EXE`, `VER`, `OUT`, `STOP`, and `DONE` refs when they exist. For execution-like products, the implementation approach must identify the major loop, external components, public interface or method boundary, runtime states, evidence outputs, subjective judgment boundary, verification strategy, and mechanical delivery checks when those facts exist in the contract.

## `prd-brief.md`

Audience: human reviewer.

Language: professional, formal Simplified Chinese.

Purpose: brief the human on the product decision. It must be concise, readable, and information-dense enough for a reviewer to decide whether the PRD direction is acceptable.

A review-ready PRD brief must include:

- `修订记录`
- `产品目标`
- `建设范围`
- `实现方案`
- `验收标准与方法`
- `路线图`
- `风险与开放问题`
- `参考文献`

The brief must answer these review questions with concrete information:

- 产品目标：为什么要做，面向谁，解决什么问题。
- 建设范围：MVP 做什么，不做什么。
- 实现方案：核心组件、核心流程、核心边界如何配合交付产品。
- 验收标准与方法：验收什么，用什么方法证明通过。
- 路线图：当前阶段交付什么，后续阶段如何演进。
- 风险与开放问题：哪些风险、依赖、开放问题会影响评审或建设。

For execution-like products, the implementation approach should include enough detail for a human reviewer to understand the execution loop and boundaries without reading all of `prd.md`: external components, public interfaces or methods, monitoring or orchestration loop, subjective judgment owner, mechanical checks, evidence outputs, and final acceptance owner. Keep it concise and use tables or Mermaid diagrams when they improve readability.

Hard writing requirements:

- Use professional, formal Simplified Chinese.
- Write for human reviewers, not for runtime agents.
- Use concise prose plus structured forms such as Markdown tables and Mermaid diagrams when they improve readability.
- Do not include process markers such as `Source contract:`, `Render status:`, or `render_status`.
- State only final conclusions and review-relevant facts; do not narrate how the workflow produced the document.
- Every substantive section must cite canonical refs such as `REQ-*`, `AC-*`, `SRC-*`, or related contract IDs.
- Put the revision table first. It must include version, date, revision summary, and reviser.
- Put references last. The reference section must include `contract-envelope.json`, `prd.md`, and the canonical IDs used by the brief.

## Review Loop

Give `prd.md` and `prd-brief.md` to the user for approval.

- If approved, record a `SRC.source_type=user_confirmation` with `confirmation_kind=prd_review_approval`, `confirmation_intent=approve_prd_and_enter_stage_3`, and sha256 bindings for both artifacts.
- If revision is requested, update `contract-envelope.json.requirement_table` first, rerun `prd-writer`, regenerate `prd-brief.md`, and repeat Stage 2.
- If rejected or insufficient, set the relevant gate to `revise` or `failed` and keep Stage 3 blocked.
