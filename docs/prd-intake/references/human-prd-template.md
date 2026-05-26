# Human PRD Delivery Specification

## Revision History

| Version | Date | Author | Change | Basis |
| --- | --- | --- | --- | --- |
| v1.0 | 2026-05-25 | Codex | Rebuilt the Human PRD delivery specification as a renderer of `output-contract.md`, with no independent field authority. | User-approved contract-first hardening |
| v1.1 | 2026-05-25 | Codex | Aligned Human PRD rendering with object payloads, `CORE`, stricter MVP requirement acceptance, and Q/ASM blocking semantics. | Design audit fix |
| v1.2 | 2026-05-25 | Codex | Objectized user confirmation through `SRC.source_type=user_confirmation` so source integrity matches the output contract. | Convergence audit fix |
| v1.3 | 2026-05-25 | Codex | Aligned Q/ASM closure wording with `status` and `resolution_refs` in the output contract. | Convergence audit fix |

## 1. Purpose

The Human PRD is the decision document for human reviewers. It must help product, design, engineering, business, operations, security, or compliance stakeholders understand:

1. What will be built.
2. What standard defines success.
3. How the product will work and be delivered.

The canonical Human PRD must be written in professional Simplified Chinese. User-requested localization may be delivered only as an additional derivative artifact and must not replace the canonical Human PRD.

## 2. Source Authority

The Human PRD must be rendered only from the canonical structured contract defined in `docs/prd-intake/output-contract.md`.

This template is a rendering specification. It may define section order, wording quality, table shape, diagram use, and readability standards. It must not define narrower support, weaker visibility, additional facts, or alternative gates beyond `output-contract.md`.

Every product fact in the Human PRD must satisfy all of the following:

1. It maps to a canonical object in `output-contract.md`.
2. It belongs to a rendered content block with an `RB`.
3. Its `RB.contract_refs` is non-empty.
4. It appears in `traceability_summary`.
5. It does not contain unsupported claims.

Document metadata such as title, author, date, version, revision history, and change basis must be supported by `META`, not by `RB`.

## 3. Required Output Shape

The Human PRD must contain these document-level blocks and three core product sections:

| Section | Role | Required Contract Support |
| --- | --- | --- |
| 修订记录 | Track document updates. | `META` |
| 要做什么 | Explain product problem, users, value, scope, and non-scope. | `CORE`, `USER`, `SCOPE`, `OOS`, `REQ`, `MOD`, `SRC`, `ASM`, `RB` |
| 标准是什么 | Define acceptance, success, risk, and quality bars. | `REQ`, `AC`, `MET`, `BAR`, `RISK`, `Q`, `ASM`, `RB` |
| 如何实现 | Explain product-system behavior, MVP, and roadmap. | `FLOW`, `DATA`, `DCT`, `STATE`, `MOD`, `TECH`, `PHASE`, `SCOPE`, `OOS`, `REQ`, `AC`, `MET`, `RISK`, `Q`, `ASM`, `RB` |
| 参考依据 | Explain how sources and assumptions support product judgment. | `SRC`, `TRACE`, `RB`, `ASM` |
| 参考文献 | List sources actually used. | `SRC`, optional `TRACE` |

HTML is only a presentation format. If HTML is requested, it must preserve the same sections and the same `RB` coverage.

## 4. Section Rules

### 4.1 要做什么

This section must let a reviewer understand the product direction in one pass.

Required content:

| Content | Rendering Rule |
| --- | --- |
| Product name | Use `CORE.product_name`; if unconfirmed, mark it as a working name. |
| One-line summary | Use `CORE.one_line_summary`; avoid marketing language. |
| Target users | Use `USER`; do not invent personas. |
| Problem statement | Use `CORE.problem_statement` and supporting `SRC` or explicit `ASM`. |
| Product solution | Summarize `SCOPE`, `REQ`, and `MOD` without implementation minutiae. |
| Scope and non-scope | Show `SCOPE` and `OOS` together. |
| Product assumptions | Render `ASM` only when it affects product judgment; label it as an assumption and include validation need, owner, and expiry condition when contract-backed. |

Recommended forms:

| Content Type | Best Form |
| --- | --- |
| Scope and non-scope | Compact table. |
| Product shape | Mermaid flowchart or concise HTML block. |
| User and value | Short prose plus table. |

### 4.2 标准是什么

This section defines acceptance, not ambition.

Required content:

| Content | Rendering Rule |
| --- | --- |
| Requirements | List only contract-backed `REQ` items. |
| Acceptance criteria | Each rendered MVP `REQ` must reference at least one `AC`; non-MVP draft requirements without `AC` must be visibly marked draft or open. |
| Success metrics | Use `MET`; do not fabricate numeric targets. |
| Quality bars | Use `BAR`; express unacceptable outcomes clearly. |
| Risks | Use `RISK`; include only risks that affect decision or execution. |
| Open questions | Use `Q` only when unresolved decisions affect acceptance, quality bars, metrics, or release readiness. |
| Assumptions | Use `ASM` only when assumptions affect acceptance, quality bars, metrics, or release readiness. |

Requirements must preserve stable IDs while being readable to humans.

### 4.3 如何实现

This section explains product operation, not an engineering task list.

Required content:

| Content | Rendering Rule |
| --- | --- |
| Control flow | Use `FLOW`; show actors and major product actions. |
| Data flow | Use `DATA` and `DCT`; show inputs, transformations, persistence, and outputs. |
| Module design | Use `MOD`; define responsibility and boundary for each major module. |
| State model | Use `STATE` when behavior depends on status, lifecycle, approval, export eligibility, or user action. |
| Technical decisions | Use `TECH`; each decision must have one clear choice and rationale. |
| Boundary | Use `SCOPE`, `OOS`, and `PHASE`; do not imply future scope is current scope. |
| MVP definition | Use `PHASE`, `SCOPE`, `OOS`, `REQ`, `AC`, `MET`, and `RISK`; state included capabilities, excluded capabilities, validation focus, and exit criteria. |
| Open decisions | Use `Q`, `RISK`, and `PHASE`; state impact without resolving the decision. |
| Product roadmap | Use `PHASE`, `OOS`, `Q`, and `TECH`; each phase must state goal, deliverables, non-goals, and exit criteria. |
| Implementation assumptions | Use `ASM` only when assumptions affect implementation boundary, sequencing, validation, or release readiness. |

Recommended forms:

| Content Type | Best Form |
| --- | --- |
| Control flow | Mermaid sequence diagram. |
| Data flow | Mermaid flowchart. |
| Modules | Responsibility table. |
| Technical decisions | Decision table with rationale. |
| State behavior | State table or state diagram. |
| MVP and roadmap | Compact phase table. |

## 5. Reference Rules

The Human PRD must preserve two distinct reference blocks:

| Block | Purpose | Rule |
| --- | --- | --- |
| 参考依据 | Explain why cited sources or explicit assumptions support product judgment. | Must not introduce unsupported claims; any rendered `ASM` must show status, basis, validation need, owner, expiry condition, and `resolution_refs` when resolved or superseded. |
| 参考文献 | List the actual sources used by the document. | Must not list unused or invented sources. |

`参考依据` may summarize source relevance. It may not turn a weak source, assumption, or open question into a confirmed fact.

## 6. Readability Standard

The Human PRD is acceptable only when it satisfies all rules below:

| Rule | Requirement |
| --- | --- |
| Concise | Remove background that does not affect product judgment. |
| Scannable | Use tables and diagrams for comparison, flow, boundaries, risks, and phases. |
| Clear | Prefer observable wording over vague adjectives. |
| Complete enough | Do not omit scope, acceptance, risks, or open questions for brevity. |
| Decision-oriented | Preserve information needed to approve, reject, narrow, or expand the product. |
| Contract-backed | Every meaningful product statement traces to `RB.contract_refs`. |
| Canonical Chinese output | The generated canonical Human PRD uses professional Simplified Chinese. |

## 7. Prohibited Output

The Human PRD must not contain:

| Prohibited Content | Reason |
| --- | --- |
| Unsupported user claims, market claims, or metric targets. | Creates hallucination risk. |
| Agent execution steps, tool instructions, or test commands. | Belongs in Agent PRD. |
| Future roadmap scope written as MVP scope. | Breaks phase consistency. |
| Multiple technical options without a decision. | Prevents implementation alignment. |
| Long background sections required to understand the product. | Violates readability goal. |
| Requirements without acceptance criteria. | Prevents review and execution. |
| Additional peer core product sections that dilute `要做什么`, `标准是什么`, and `如何实现`. | Breaks the reference-aligned reading model. |
| HTML that hides, omits, or renames beyond recognition the required sections. | Treats presentation as a structure exemption. |

## 8. Human PRD Delivery Gate

Before delivery, verify:

| Gate | Pass Condition |
| --- | --- |
| Contract authority | Every content fact is supported by `output-contract.md`; this template did not add new facts or narrower support. |
| Coverage | Every product content section has at least one `RB`; every `RB.contract_refs` is non-empty; document metadata is supported by `META`. |
| Source integrity | External claims, source citations, and factual numbers map to `SRC`, `ASM`, or `SRC.source_type=user_confirmation` through the contract. |
| Requirement integrity | Each rendered MVP or current-acceptance `REQ` has related `AC`; non-MVP, draft, or open `REQ` items without `AC` are visibly marked and are not presented as approvable scope. |
| Scope integrity | `SCOPE`, `OOS`, `PHASE`, and MVP boundary do not conflict. |
| Reference-shape integrity | Required document blocks and exactly three core product sections are present. |
| Presentation integrity | Markdown or HTML preserves the same sections and `RB` coverage. |
| Unknowns honesty | `Q` and `ASM` remain visible when they affect decision, acceptance, implementation, or release readiness. |
| Human blocking | `Q.blocks_human_prd=true` with `Q.status=open`, or `ASM.blocks_human_prd=true` with `ASM.status=open`, prevents `review_ready` until resolved in the contract with `resolution_refs`. |
| Readability | A human reviewer can understand the product without reading the full contract. |

If any gate fails, the Human PRD must be marked draft or blocked, not final.
