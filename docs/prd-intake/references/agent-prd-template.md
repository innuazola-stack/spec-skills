# Agent PRD Delivery Specification

## Revision History

| Version | Date | Author | Change | Basis |
| --- | --- | --- | --- | --- |
| v1.0 | 2026-05-25 | Codex | Rebuilt the Agent PRD delivery specification as an execution renderer of `output-contract.md`, with explicit object ID visibility and gate dependence. | User-approved contract-first hardening |
| v1.1 | 2026-05-25 | Codex | Aligned Agent PRD rules with object payloads, `CORE`, mandatory `VER-*` for execution-ready output, fixed State section behavior, and corrected References support. | Design audit fix |
| v1.2 | 2026-05-25 | Codex | Scoped current-execution `REQ` verification, objectized user confirmation, and added STOP status and resolution rendering. | Convergence audit fix |
| v1.3 | 2026-05-25 | Codex | Aligned open decision closure with `Q.status`, `ASM.status`, and `resolution_refs` in the output contract. | Convergence audit fix |
| v1.4 | 2026-05-26 | Codex | Added execution-affecting `ASM` to Source Of Truth support and conflict handling. | Convergence audit fix |

## 1. Purpose

The Agent PRD is the execution contract for an AI Agent or harness. It must tell the Agent exactly what to build, what not to change, what inputs are valid, how to verify completion, and when to stop and ask a human.

The Agent PRD must be written in English. It must be complete, precise, logically ordered, and directly consumable by automated or semi-automated execution systems.

## 2. Source Authority

The Agent PRD must be rendered only from the canonical structured contract defined in `docs/prd-intake/output-contract.md`.

This template is a rendering specification. It may define section order, visible fields, table shapes, wording constraints, and execution readability rules. It must not define narrower support, weaker visibility, additional scope, new data fields, new verification cases, or alternative gates beyond `output-contract.md`.

Every execution fact in the Agent PRD must satisfy all of the following:

1. It maps to a canonical object in `output-contract.md`.
2. It belongs to a rendered content block with an `RB`.
3. Its `RB.contract_refs` is non-empty.
4. It appears in `traceability_summary`.
5. It exposes the canonical ID when it is an object-backed row.

Document metadata such as title, author, date, version, revision history, and change basis must be supported by `META`, not by `RB`.

## 3. Required Output Shape

The Agent PRD must use these sections in this order:

| Section | Purpose | Required Contract Support |
| --- | --- | --- |
| Revision History | Track document updates. | `META` |
| Execution Objective | Define the exact outcome for this execution. | `CORE`, `PHASE`, `SCOPE`, `REQ`, `OUT`, `RB` |
| Source Of Truth | Identify authoritative sources and precedence. | `REF`, `IN`, `DATA`, `Q`, `ASM`, conditional `SRC`, optional `TRACE`, conditional `RB` |
| Input Contract | Define inputs, constraints, entry blockers, and permissions. | `IN`, `DCT`, `SCOPE`, `STOP`, `EXE`, `BAR`, `RB` |
| Scope Contract | Define in-scope and out-of-scope work. | `SCOPE`, `OOS`, `PHASE`, `STOP`, `RB` |
| Execution Contract | Define required behavior, forbidden behavior, sequencing, and human confirmation. | `EXE`, `REQ`, `BAR`, `OOS`, `STOP`, `FLOW`, `STATE`, `TECH`, `RB` |
| Implementation Constraints | Carry product and technical decisions into execution limits. | `TECH`, `MOD`, `DATA`, `PHASE`, `RB` |
| Requirements And Acceptance Criteria | Define buildable requirements and acceptance criteria. | `REQ`, `AC`, `VER`, `PHASE`, `RB` |
| State Transition Contract | Define state changes, event rules, and eligibility behavior. | `STATE`, `REQ`, `AC`, `DATA`, `BAR`, `STOP`, `RB` |
| Data Contract | Define schemas, fields, constraints, sources, and outputs. | `DCT`, `DATA`, `REQ`, `TECH`, `BAR`, `RISK`, `Q`, `RB` |
| Verification Contract | Define positive cases, negative cases, consistency checks, and blocking failures. | `VER`, `AC`, `DONE`, `GATE`, `REQ`, `STOP`, `BAR`, `RB` |
| Output Contract | Define required deliverables and residual scope. | `OUT`, `REQ`, `AC`, `DONE`, `VER`, `OOS`, `Q`, `PHASE`, `RB` |
| Open Decisions | List unresolved decisions and execution-affecting assumptions the Agent must not self-resolve. | `Q`, `ASM`, `PHASE`, `STOP`, `RB` |
| Stop Conditions | Define when execution must stop and ask a human. | `STOP`, `Q`, `RISK`, `BAR`, `RB` |
| Done Criteria | Define all conditions required before completion can be claimed. | `DONE`, `VER`, `AC`, `GATE`, `RB` |
| References | List references used by the Agent PRD body. | `REF`, conditional `SRC`, conditional `TRACE`, conditional `RB` |

`System Context` is optional. Include it only when the canonical contract has concrete `MOD`, `DATA`, `DCT`, `TECH`, `SRC`, or runtime references to existing files, APIs, interfaces, modules, schemas, or platform constraints. Do not create a placeholder System Context section.

`State Transition Contract` is a fixed section. If no state transition applies, render the section with `Not applicable`, cite the contract or gate evidence, and do not omit it.

`References` belongs to the Agent PRD execution body. Full section-to-contract coverage belongs to `traceability_summary`, not to the Agent PRD body.

## 4. Section Rules

### 4.1 Execution Objective

Required visible fields:

| Field | Rule |
| --- | --- |
| Capability name | Use `CORE.product_name` or confirmed working name. |
| Execution phase | Use `PHASE`; do not collapse roadmap phases. |
| Deliverable outcome | Use `SCOPE`, `REQ`, and `OUT`. |
| Non-expansion rule | State that scope absent from the canonical contract must not be added. |

### 4.2 Source Of Truth

This section must define source precedence.

| Field | Rule |
| --- | --- |
| Source ID | Preserve `REF`, `SRC`, `IN`, `DATA`, `Q`, or execution-affecting `ASM` ID. |
| Canonical contract | Use `REF.ref_type=canonical_contract` when delivered or persisted. |
| Human PRD sibling | Use `REF.ref_type=sibling_artifact` only as consistency-check artifact when both PRDs are delivered. |
| Runtime inputs | Use active `IN` rows when inputs define execution facts. |
| Runtime data sources | Use active `DATA` rows when data sources define execution facts. |
| Open questions | Use `Q`; do not infer answers. |
| Open assumptions | Use `ASM` when an unresolved assumption affects execution scope, sequencing, validation, or stop behavior; do not present it as confirmed. |
| Conflict handling | Stop unless the contract provides explicit precedence. |

If an open `ASM` conflicts with a confirmed `SRC` or canonical object payload, the Agent must stop and require a contract update before execution continues.

### 4.3 Input Contract

| Field | Rule |
| --- | --- |
| Input ID | Preserve `IN.id`. |
| Required inputs | Use `IN.required=true`. |
| Optional inputs | State default behavior when omitted. |
| Constraints | Use `IN.constraints` and `DCT.constraints`. |
| Entry blockers | Use `IN.entry_blockers` and `STOP`. |
| Permission requirements | Use `EXE`, `BAR`, or `STOP` when relevant. |

### 4.4 Scope Contract

| Field | Rule |
| --- | --- |
| In scope | List `SCOPE` items with IDs. |
| Out of scope | List `OOS` items with IDs. |
| Phase boundary | Use `PHASE` to separate MVP, later work, and excluded work. |
| Scope blocker | State stop or defer behavior for `OOS` or future `PHASE` requests. |

### 4.5 Execution Contract

| Field | Rule |
| --- | --- |
| Rule ID | Preserve `EXE.id`. |
| Required behavior | Use `EXE` and `REQ`. |
| Forbidden behavior | Use `BAR`, `OOS`, and `STOP`. |
| Sequencing constraints | Use `FLOW`, `STATE`, or `EXE`; render as a visible table column or equivalent field. |
| Human confirmation | Use `SRC.source_type=user_confirmation` for confirmed facts; use `BAR`, `STATE`, or `STOP` when approval affects state or output. |

### 4.6 Implementation Constraints

| Field | Rule |
| --- | --- |
| Technical decision ID | Preserve `TECH.id`. |
| Decision | Use `TECH.decision`. |
| Rationale | Use `TECH.rationale`. |
| Affected modules | Use `TECH.applies_to` and `MOD`. |
| Phase | Use `TECH.phase`. |
| Agent constraint | Use `TECH.agent_constraint`. |

Do not offer implementation choices unless the contract explicitly defines them as open decisions.

### 4.7 Requirements And Acceptance Criteria

| Field | Rule |
| --- | --- |
| Requirement ID | Preserve `REQ.id`. |
| Phase | Use `REQ.phase`. |
| Requirement statement | Use `REQ.title` and `REQ.description`. |
| Acceptance criteria IDs | Preserve linked `AC.id` values. |
| Acceptance criteria | Use linked `AC`; do not replace with unnumbered prose only. |
| Verification link | Use `VER` for execution-ready output. `AC.verification_method` may supplement draft output but cannot replace `VER-*`. |

Each current-execution `REQ` must have at least one `AC` and at least one visible `VER-*` link before the Agent PRD can be execution-ready. Deferred or future-phase `REQ` items may appear only as residual scope, roadmap, or non-executable context, and must not be presented as buildable current work.

### 4.8 State Transition Contract

Render this section in every Agent PRD. When behavior depends on lifecycle, review status, approval, deletion, export eligibility, workflow state, or user action, include concrete `STATE-*` rows. When no state behavior applies, render `Not applicable` with the supporting contract or gate evidence.

| Field | Rule |
| --- | --- |
| State rule ID | Preserve `STATE.id`. |
| States | Use `STATE.states`. |
| Events | Use `STATE.events`. |
| Transition rules | Use `STATE.transition_rules`. |
| Eligibility rules | Use `STATE.export_eligibility` or equivalent eligibility field. |
| Negative rules | State forbidden transitions when defined by `BAR`, `AC`, or `STOP`. |

### 4.9 Data Contract

| Field | Rule |
| --- | --- |
| Data contract ID | Preserve `DCT.id`; preserve `DATA.id` for data-source rows. |
| Schema | Use `DCT.schema`. |
| Required fields | Use `DCT.required_fields`. |
| Field constraints | Use `DCT.constraints`. |
| Data sources and outputs | Use `DATA.inputs` and `DATA.outputs`. |
| Privacy or retention constraints | Use `TECH`, `BAR`, `RISK`, or `Q`. |

### 4.10 Verification Contract

Verification must prove product intent, not only code execution.

| Case Type | Rule |
| --- | --- |
| Case ID | Preserve `VER.id`. |
| Positive cases | Use `VER.case_type=positive`; show related `REQ` or `AC`. |
| Negative cases | Use `VER.case_type=negative`; show related `REQ`, `AC`, `STOP`, or `BAR`. |
| Consistency checks | Use `VER.case_type=consistency_check`; reference relevant contract area and global `GATE` when applicable. |
| Blocking failures | Use `VER.case_type=blocking_failure`; render `blocking=true` and `failure_handling` as visible fields. |

Positive and negative verification cases must use `VER-*` IDs. Local `C-*`, `N-*`, or local `GATE-*` labels are forbidden.

### 4.11 Output Contract

| Field | Rule |
| --- | --- |
| Output ID | Preserve `OUT.id`. |
| Deliverable | Use `OUT.deliverable`. |
| Acceptance rule | Use `OUT.acceptance_rule`, linked `AC`, `VER`, and `DONE`. |
| Residual-scope note | Use `OOS`, `Q`, or `PHASE` when work is deferred. |

### 4.12 Open Decisions

| Field | Rule |
| --- | --- |
| Decision ID | Preserve `Q.id` or execution-affecting `ASM.id`. |
| Question or assumption | Use `Q.question` or `ASM.assumption`. |
| Impact | Use `Q.impact` or `ASM.impact`. |
| Owner | Use `Q.owner` or `ASM.owner`. |
| Phase | Use `Q.phase` or the phase affected by `ASM`. |
| Agent handling | Use `Q.agent_handling` or `ASM.agent_handling`; open assumptions must tell the Agent whether to proceed, defer, or stop. |
| Status | Use `Q.status` or `ASM.status`; `open` decisions and assumptions remain visible and must not be self-resolved. |
| Resolution references | Use `Q.resolution_refs` or `ASM.resolution_refs` when the item has been resolved, deferred, or superseded. |

The Agent must not close open decisions or execution-affecting assumptions unless the user explicitly confirms the answer and the contract is updated.

### 4.13 Stop Conditions

| Field | Rule |
| --- | --- |
| Stop ID | Preserve `STOP.id`. |
| Trigger | Use `STOP.condition`. |
| Reason | Use `STOP.reason`. |
| Status | Use `STOP.status`; only `triggered` blocks execution-ready output. |
| Required action | Use `STOP.required_human_action`. |
| Resolution references | Use `STOP.resolution_refs` when the stop condition has been resolved. |
| Related risk or quality bar | Use `RISK` or `BAR` when relevant. |

### 4.14 Done Criteria

| Field | Rule |
| --- | --- |
| Done ID | Preserve `DONE.id`. |
| Completion condition | Use `DONE.criterion`. |
| Verification reference | Use `DONE.verification_refs`. |
| Blocking status | Use `DONE.blocking`. |
| Consistency condition | Include sibling PRD consistency when both PRDs exist. |

### 4.15 References

The References section identifies sources used by the Agent PRD body. It does not replace `traceability_summary`.

| Field | Rule |
| --- | --- |
| Reference ID | Preserve `REF.id` or `SRC.id`. |
| Canonical contract reference | Use `REF.ref_type=canonical_contract`. |
| Human PRD reference | Use `REF.ref_type=sibling_artifact`; do not present it as upstream authority. |
| Source files or links | Use `SRC` and stable names or URLs. |
| Local references | Use `REF.ref_type=local_reference` only when present and used. |
| Harness references | Use `REF.ref_type=harness_reference` or `SRC` only when present and used. |

Execution controls affected by a reference, such as `EXE`, `VER`, `STOP`, or `DONE`, must be linked through `TRACE` or `REF.related_refs`; they are not themselves reference sources.

Allowed `REF.ref_type` values are exactly those defined in `output-contract.md`.

## 5. Language And Formatting Rules

| Rule | Requirement |
| --- | --- |
| Language | English only. |
| IDs | Preserve canonical IDs exactly. |
| Tables | Use tables for contracts, scopes, requirements, verification, outputs, stops, and done criteria. |
| Code blocks | Use fenced code blocks for schemas and structured payloads. |
| Ambiguity | Do not hide ambiguity in prose; use Open Decisions or Stop Conditions. |
| No filler | Avoid background that does not affect execution. |
| Reference-aligned shape | Do not add mandatory top-level sections beyond the required sequence unless contract-backed. |

## 6. Prohibited Output

The Agent PRD must not contain:

| Prohibited Content | Reason |
| --- | --- |
| New scope absent from `SCOPE` or `REQ`. | Breaks canonical contract consistency. |
| Future phase work presented as current execution. | Breaks roadmap boundary. |
| Technical choices without `TECH` support. | Creates unsupported architecture. |
| Verification cases without `VER` support. | Creates fake confidence. |
| Data fields not present in `DCT` or `DATA`. | Causes implementation drift. |
| Open decisions resolved by the Agent. | Bypasses human authority. |
| Non-English Agent-facing text. | Violates runtime portability. |
| Placeholder System Context. | Encourages invented implementation context. |
| Full traceability report inside the Agent PRD body. | Belongs to `traceability_summary`. |
| Missing References section in an execution-ready Agent PRD. | Prevents source authority from being auditable. |

## 7. Agent PRD Delivery Gate

Before delivery, verify:

| Gate | Pass Condition |
| --- | --- |
| Contract authority | Every execution fact is supported by `output-contract.md`; this template did not add scope or facts. |
| English-only | No non-English Agent-facing prose remains. |
| Coverage | Every execution factual content block has `RB`; every `RB.contract_refs` is non-empty; metadata uses `META`. |
| Source integrity | Every fact maps to `REF`, `SRC`, `IN`, `DATA`, `SRC.source_type=user_confirmation`, or another canonical object. |
| Scope integrity | `SCOPE`, `OOS`, and `PHASE` do not conflict. |
| Executability | `IN`, `EXE`, `VER`, `OUT`, `STOP`, and `DONE` are present for execution-ready delivery. |
| Requirement integrity | Every current-execution `REQ` has linked `AC`, explicit phase, visible verification link, and canonical ID; deferred or future-phase `REQ` items are not executable requirements. |
| Canonical ID visibility | Every object-backed row exposes the canonical ID for its primary object. |
| Verification integrity | Positive, negative, consistency, and blocking cases use `VER-*` IDs and map to related refs. |
| Stop status | Only `STOP.status=triggered` blocks execution-ready output; `defined` stop conditions remain visible as rules. |
| Open-decision honesty | `Q.status=open` items are preserved and not self-resolved; closed decisions must show `resolution_refs`. |
| Reference-shape integrity | The required section sequence is complete; optional System Context appears only when contract-backed. |
| References integrity | References lists only actual `REF` or `SRC` entries used by the Agent PRD body. |
| Audit separation | Section-to-contract coverage is delivered in `traceability_summary`, not confused with the Agent PRD body. |

If any gate fails, the Agent PRD must be marked blocked or draft, not execution-ready.
