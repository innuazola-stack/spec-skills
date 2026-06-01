# PRD Quality Reference

Use this reference during Stage 2 to calibrate PRD depth, traceability, and review usefulness after Stage 1 has produced a validator-clean `contract-envelope.json`.

This is a quality reference, not a product template and not a source of domain facts.

## Reference Package

The historical executor Stage 2 package reached the intended specificity bar, but it used the old Human/Agent PRD split. Use it only to learn depth, evidence discipline, and execution-topology visibility. In the current workflow, the same quality bar must be achieved through:

- `prd.md`: standard PRD produced by `prd-writer`.
- `prd-brief.md`: Simplified Chinese human review brief derived from `prd.md` and the contract.

Do not copy executor-specific facts, component names, method names, CLI names, or domain wording into unrelated products.

## What To Learn

### Contract-First Revision

Late user feedback becomes canonical contract facts before PRD documents are regenerated. New external sources, requirements, acceptance criteria, verification refs, risks, and traceability rows must be added to `contract-envelope.json` first.

Quality bar: no important PRD claim should exist only in prose.

### Source-Backed Implementation Detail

Do not say "call an adapter" generically when source material exists. Record the external component source, public method or command boundary, runtime states, screen/status evidence, judgment boundary, and delivery-check boundary in the contract before describing the implementation approach in `prd.md`.

Quality bar: when external component docs or source are available, method-level or interface-level claims must cite canonical source refs. When sources are missing, record a blocking question or assumption instead of inventing the interface.

### Standard PRD

`prd.md` must be a complete product requirements document. It explains the problem, target users, goals, success measures, scope, requirements, acceptance, verification posture, roadmap, risks, assumptions, dependencies, and traceability. For execution-like products, it must also preserve input, execution, integration, permission, state, output, stop, and done contracts enough for HLD writing.

Quality bar: a downstream designer or agent should be able to proceed to HLD without asking "what is the product?", "how does execution actually work?", or "how will we know it is acceptable?"

### PRD Brief With Review Value

`prd-brief.md` is short, formal, and review-oriented, but not empty. It starts with a revision table, uses Simplified Chinese, answers what the product goal is, what will be built, how it will work, how it will be accepted, what the roadmap is, and what risks remain. It uses structured forms such as tables or Mermaid diagrams when they improve readability, and ends with references.

Quality bar: a human reviewer should understand the product direction and approval risks without reading the full PRD.

### Execution Topology Visibility

For execution-like products, `prd.md` and the brief expose the material topology at the right depth: external components, public interfaces, loop or orchestration model, runtime states, evidence outputs, subjective judgment owner, mechanical checks, and final acceptance owner.

Quality bar: do not hide a material execution loop behind vague implementation phrases.

## Forbidden Uses

- Do not treat this reference as a template that every product must mimic section-by-section.
- Do not import executor-specific requirements, component names, methods, CLI names, monitoring behavior, or delivery checks into other products.
- Do not use the reference as evidence for the current product. Current-product facts must come from the current Stage 1 sources and requirement table.
- Do not use the reference to bypass user clarification when the current product lacks required facts.

## Stage 2 Self-Check

Before marking `prd.md` and `prd-brief.md` `review_ready`, compare the draft with this quality bar:

- Does every material product or implementation claim trace to the current `contract-envelope.json`?
- Was `prd.md` produced by `prd-writer` rather than hand-authored by spec-intake?
- Does `prd.md` read as a complete standard PRD?
- Does `prd.md` render non-empty `FLOW`, `DATA`, `MOD`, `TECH`, `STATE`, and `DCT` refs when present?
- Does `prd-brief.md` answer goal, scope, approach, acceptance method, roadmap, and risks with concrete information?
- Could a human approve the direction from `prd-brief.md` while consulting `prd.md` for detail?
- Could `hld-writer` begin HLD from `prd.md` without guessing key execution boundaries?
- Has revision feedback been incorporated through the requirement table before rerunning `prd-writer`?

If the draft fails these checks, return to Stage 1 or revise the contract-backed Stage 2 render before presenting it as ready.
