# Agent PRD Example: Post-Meeting Action Hub

## Revision History

| Version | Date | Author | Change | Basis |
| --- | --- | --- | --- | --- |
| v1.0 | 2026-05-25 | Codex | Created an Agent PRD example that stays consistent with the shared product contract and follows harness-consumable execution contracts. | Shared product contract; harness hardening reference |
| v1.1 | 2026-05-25 | Codex | Rewrote the Agent-facing document in English to reduce encoding risk and improve runtime portability. | Agent-facing document language rule |
| v1.2 | 2026-05-25 | Codex | Fixed Phase 1 scope, status model, implementation constraints, and open-decision traceability to match the shared product contract. | Review fixes |
| v1.3 | 2026-05-25 | Codex | Hardened invalid export target handling and completion criteria for implementation constraints and open decisions. | Review fixes |
| v1.4 | 2026-05-25 | Codex | Added explicit state transition rules so editing cannot imply confirmation or export eligibility. | Review fixes |
| v1.5 | 2026-05-25 | Codex | Reframed the example so the canonical contract is the source of truth and the Human PRD is only a sibling review artifact. | Review fix; root cause: the reference example still modeled sibling PRDs as upstream/downstream documents |
| v1.6 | 2026-05-25 | Codex | Added explicit requirement phases to align the reference example with the Agent PRD template and output contract. | Review fix; root cause: requirement phase was required by the template but absent from the example shape |
| v1.7 | 2026-05-25 | Codex | Added visible requirement-to-verification links and verification-to-requirement mappings. | Review fix; root cause: verification support was contract-backed but not visible in the reference rendering |
| v1.8 | 2026-05-25 | Codex | Converted open decisions, stop conditions, and done criteria into field-complete tables. | Review fix; root cause: required contract fields were present as prose but not visibly aligned with the template fields |
| v1.9 | 2026-05-25 | Codex | Completed field-level alignment for scope, implementation constraints, state transitions, data contract, and consistency checks. | Review fix; root cause: template required fields were still only partially visible in reference tables |
| v1.10 | 2026-05-25 | Codex | Added explicit blocking failure rules to the Verification Contract section. | Review fix; root cause: blocking failures were represented only in Done Criteria, not in the required Verification Contract shape |
| v1.11 | 2026-05-25 | Codex | Strengthened the primary positive extraction verification case so it proves all required extraction fields from `REQ-001` and `REQ-005`. | Review fix; root cause: the reference verification example covered only part of the linked acceptance criteria |
| v1.12 | 2026-05-25 | Codex | Added open-decision authority to Source Of Truth so the section visibly covers unresolved questions required by the Agent PRD template. | Review fix; root cause: open decisions were present later in the body but absent from the Source Of Truth reference shape |
| v1.13 | 2026-05-25 | Codex | Added explicit precedence and conflict handling to Source Of Truth. | Review fix; root cause: Source Of Truth listed sources and purposes but did not visibly encode source priority for harness execution |
| v1.14 | 2026-05-25 | Codex | Renamed in-scope IDs from `S-*` to `SCOPE-*` to match the output contract ID system. | Review fix; root cause: the reference example used local shorthand IDs instead of canonical contract prefixes |
| v1.15 | 2026-05-25 | Codex | Removed an unused harness reference from References. | Review fix; root cause: the reference list contained a source that was not used by the Agent PRD body |
| v1.16 | 2026-05-25 | Codex | Added `owner` and `due_date` to the Action item required fields table. | Review fix; root cause: the JSON schema, acceptance criteria, and verification cases required these fields, but the required-fields table did not |
| v1.17 | 2026-05-25 | Codex | Added canonical IDs to all object-backed rows and replaced local verification labels with `VER-*` IDs. | Review fix; root cause: object-backed rows were traceable in prose but did not expose canonical contract IDs consistently |
| v1.18 | 2026-05-25 | Codex | Replaced local `GATE-*` check rows with `VER-*` rows and preserved `GATE-*` only as global gate references. | Review fix; root cause: the example reused global gate IDs for local verification checks |
| v1.19 | 2026-05-25 | Codex | Added visible active inputs, acceptance criteria IDs, sequencing references, and blocking failure handling fields to match the authoritative field closure table. | Review fix; root cause: several contract fields were required by template and output contract but only implied by prose or section names in the reference |
| v1.20 | 2026-05-25 | Codex | Replaced range-style ID references with explicit ID lists in execution-critical rows. | Self-review fix; root cause: range wording was human-readable but less stable for Agent or validator consumption |
| v1.21 | 2026-05-26 | Codex | Merged duplicate `REF-001` Source Of Truth rows so one canonical ID has one visible source meaning. | Convergence audit fix |

## 1. Execution Objective

Implement the Phase 1 MVP capability for the Post-Meeting Action Hub: extract candidate action items from meeting text, group them by owner, show source excerpts on a review page, and allow users to confirm, edit, delete, reject, and export confirmed action items to Markdown.

This Agent PRD is rendered from the same canonical contract as `human-prd-example-meeting-action-hub.md`. The Human PRD is a sibling review artifact for consistency checks. The implementation must not introduce any scope that is absent from or excluded by the canonical contract.

## 2. Source Of Truth

| ID | Source | Authority | Purpose | Conflict Handling |
| --- | --- | --- | --- | --- |
| REF-001 | Canonical Post-Meeting Action Hub contract | Primary | Authoritative source for product goals, users, scope, requirement IDs, success metrics, risks, non-goals, implementation decisions, open decisions, phase boundaries, and the Phase 2 task-system sync roadmap boundary. | If another source disagrees with the canonical contract, stop and require a contract update before implementation; defer Phase 2 work unless the roadmap is explicitly changed in the canonical contract. |
| REF-002 | `human-prd-example-meeting-action-hub.md` | Sibling artifact | Consistency-check artifact for human-readable product intent. | Do not treat the Human PRD as upstream authority; use it to detect inconsistency with the canonical contract. |
| IN-001; IN-002; IN-003; IN-004 | Runtime input contract | Required execution boundary | Defines required transcript, participants, meeting metadata, optional Markdown export target, and entry blockers. | Missing or invalid required input stops execution according to the Input Contract. |
| DATA-001 | Meeting text input | Runtime data source | Data source for action item extraction. | Use only for extracting candidate action items; do not let runtime input change product scope, requirements, or acceptance criteria. |
| Q-001; Q-002; Q-003 | Canonical contract open decisions | Primary ambiguity boundary | Defines unresolved integration, distributed confirmation, and source-excerpt retention decisions that the Agent must not self-resolve. | Stop or defer according to Open Decisions and Stop Conditions. |

## 3. Input Contract

| ID | Input | Required | Constraints |
| --- | --- | --- | --- |
| IN-001 | `meeting_transcript` | Yes | Plain-text meeting transcript or meeting notes from an authorized meeting. |
| IN-002 | `participants` | Yes | Participant list with at least names; email or user ID is optional. |
| IN-003 | `meeting_metadata` | Yes | Meeting title, meeting time, and organizer. |
| IN-004 | `export_target` | No | Defaults to `markdown` when omitted. Only `markdown` is supported in Phase 1. Any other value is an entry blocker. |

Entry blockers:

| ID | Entry Blocker | Required Handling |
| --- | --- | --- |
| STOP-001 | `meeting_transcript` is missing. | Stop and request the missing transcript or notes. |
| STOP-002 | The meeting text cannot be confirmed as authorized input. | Stop until authorization exists. |
| STOP-003 | `participants` is empty. | Stop and request the participant list. |
| STOP-004 | `export_target` is present and is not `markdown`. | Stop or require a confirmed scope change. |
| STOP-005 | The user asks the system to process unauthorized recordings, private chats, or sensitive external data. | Stop until authorization and data handling approval exist. |

## 4. Scope Contract

### 4.1 In Scope

| ID | Phase Boundary | Scope | Scope Blocker |
| --- | --- | --- | --- |
| SCOPE-001 | Phase 1 MVP | Extract candidate action items from meeting text. | Stop if the input is not authorized meeting text. |
| SCOPE-002 | Phase 1 MVP | Generate owner, due date, source excerpt, and confidence for each candidate action item. | Stop or mark `needs_review` when evidence is missing. |
| SCOPE-003 | Phase 1 MVP | Group candidate action items by owner. | Do not infer a missing owner beyond the participant list and meeting text. |
| SCOPE-004 | Phase 1 MVP | Support confirm, edit, delete, and reject operations for candidate action items. | Do not treat edit, delete, or reject as confirmation. |
| SCOPE-005 | Phase 1 MVP | Export confirmed action items to Markdown. | Stop or defer if the request requires task-system sync. |

### 4.2 Out Of Scope

| ID | Phase Boundary | Out-of-scope item | Scope Blocker |
| --- | --- | --- | --- |
| OOS-001 | Excluded from all phases | Full project management, boards, Gantt charts, or resource scheduling. | Reject as outside the product boundary. |
| OOS-002 | Excluded from all phases | Automatically creating or committing tasks without human confirmation. | Stop and ask for explicit contract change. |
| OOS-003 | Excluded from all phases | Processing unauthorized meeting recordings, private chats, or sensitive external data. | Stop until authorization and data handling approval exist. |
| OOS-004 | Excluded from Phase 1 | Quality guarantees for languages other than Chinese and English. | Mark as future evaluation rather than MVP scope. |
| OOS-005 | Phase 2 deferred scope | External task-system sync in Phase 1. | Defer to Phase 2 unless the roadmap is changed. |

## 5. Execution Contract

The Agent must follow these rules:

| ID | Type | Rule | Related Flow / State / Sequence |
| --- | --- | --- | --- |
| EXE-001 | Fact boundary | Do not change the canonical contract goals, non-goals, requirement IDs, or success metrics. | Applies across the full execution sequence. |
| EXE-002 | Implementation boundary | Do not build a full project management system or add unconfirmed integration scope. | Applies before implementation planning and output selection. |
| EXE-003 | Human confirmation | Candidate action items must be confirmed by a human before export. | `DATA-003`; `STATE-002`; extract, review, confirm, then export. |
| EXE-004 | Evidence requirement | A candidate without a source excerpt must not enter the default confirmed state. | `DATA-001`; `STATE-001`; extraction output must be checked before confirmation. |
| EXE-005 | Privacy requirement | Do not process unauthorized text. Do not expose context beyond what is needed to evaluate the action item. | `STOP-002`; input authorization check precedes extraction. |

## 6. Implementation Constraints

These constraints carry forward the implementation decisions from the canonical contract:

| ID | Area | Technical Decision | Rationale | Affected Modules | Phase Applicability | Agent Constraint |
| --- | --- | --- | --- | --- | --- | --- |
| TECH-001 | AI extraction | Use an LLM for structured extraction into fixed-field JSON. | Action item detection needs language understanding, while fixed fields make review and export deterministic. | MOD-002 Action Item Extraction Module; DCT-002 Data Contract | Phase 1 | The extractor output must be machine-readable and conform to the data contract in this document. |
| TECH-002 | Review experience | Use a web review page as the primary human confirmation surface. | Table-based review, editing, and grouping are more reliable than chat-only confirmation for post-meeting workflows. | MOD-003 Review Page Module; STATE-001; STATE-002; STATE-003; STATE-004; STATE-005 | Phase 1 | Do not replace the review page with chat-only confirmation. |
| TECH-003 | Initial output | Use Markdown export for the MVP. | Markdown is low-cost, readable, and easy to copy into existing tools while validating product value. | MOD-004 Export Module; OUT-003 | Phase 1 | Do not implement external task-system sync in Phase 1. |
| TECH-004 | Integration strategy | Add at most one primary task-system integration in Phase 2. | Integration effort should follow proof that Markdown export and human confirmation create value. | MOD-005 Sync Module; OUT-004 | Phase 2 | Treat any Jira, Linear, Asana, or similar integration request as a Phase 2 scope decision. |
| TECH-005 | Data retention | Keep only action items, review status, and necessary source excerpts by default. | Data minimization lowers privacy risk and avoids storing meeting content beyond execution needs. | MOD-001 Meeting Input Module; DCT-001; DCT-002; DCT-003 | Phase 1 | Do not persist full meeting content unless a future privacy decision explicitly allows it. |

## 7. Requirements And Acceptance Criteria

| ID | Phase | Requirement | Acceptance Criteria IDs | Agent Acceptance Criteria | Verification Link |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | Phase 1 | The system must extract candidate action items from meeting text. | AC-001 | Given meeting text with explicit commitments, output an action item array. Each item includes `title`, `owner`, `due_date`, `source_excerpt`, and `confidence`. | VER-001, VER-005 |
| REQ-002 | Phase 1 | The system must group action items by owner. | AC-002 | Items with the same owner appear in the same group. Items without an identified owner appear in the `Needs owner confirmation` group. | VER-002 |
| REQ-003 | Phase 1 | The user must be able to confirm, edit, delete, or reject candidate action items. | AC-003 | Each candidate supports `confirm`, `edit`, `delete`, and `reject` actions. The final `status`, `edited`, and `edited_fields` values are persisted. | VER-003, VER-004, VER-008 |
| REQ-004 | Phase 1 | The user must be able to export confirmed action items to Markdown. | AC-004 | Confirmed action items can be exported to Markdown. Unconfirmed, deleted, and rejected items do not appear in the default export. External task-system sync is out of scope for Phase 1. | VER-003, VER-004, VER-008 |
| REQ-005 | Phase 1 | The system must preserve the source evidence for each action item. | AC-005 | Each candidate displays `source_excerpt`. If `source_excerpt` is missing, the item status is `needs_review` and must not default to confirmed. | VER-001, VER-007 |

## 8. State Transition Contract

| ID | State | Event | Transition Rule | Export Eligibility | Negative Rule |
| --- | --- | --- | --- | --- | --- |
| STATE-001 | `needs_review` | `edit` | Keep `status=needs_review`; set `edited=true`; update `edited_fields`. | Not exportable. | Editing alone must not confirm an item. |
| STATE-002 | `needs_review` or edited candidate | `confirm` | Set `status=confirmed`; preserve `edited` and `edited_fields`. | Exportable. | Do not confirm an item without explicit user action. |
| STATE-003 | Any non-deleted candidate | `reject` | Set `status=rejected`. | Not exportable. | A rejected item must not appear in default export. |
| STATE-004 | Any candidate | `delete` | Set `status=deleted`. | Not exportable. | A deleted item must not appear in default export. |
| STATE-005 | `confirmed` | `edit` | Keep `status=confirmed`; set `edited=true`; update `edited_fields`. | Exportable with edited values. | Do not clear confirmation because of an edit. |

Rules:

- Editing alone must not confirm an item.
- Editing a `needs_review` item keeps it in `needs_review` until the user explicitly confirms it.
- A deleted or rejected item must not be exported, even if it was previously edited.

## 9. Data Contract

```json
{
  "meeting_id": "string",
  "generated_at": "ISO-8601 datetime",
  "action_items": [
    {
      "id": "string",
      "title": "string",
      "owner": "string | null",
      "due_date": "ISO-8601 date | null",
      "source_excerpt": "string | null",
      "confidence": "number",
      "status": "needs_review | confirmed | rejected | deleted",
      "edited": "boolean",
      "edited_fields": ["title", "owner", "due_date"]
    }
  ]
}
```

Schema ID: `DCT-002`.

Data constraints:

- `confidence` must be between 0 and 1.
- Initial `status` must not be `confirmed` unless the user explicitly confirms the item.
- If `source_excerpt` is empty, `status` must be `needs_review`.
- If `owner` is empty, the candidate must be placed in the `Needs owner confirmation` group.
- If a user edits a candidate and then confirms it, set `status` to `confirmed`, set `edited` to `true`, and record changed fields in `edited_fields`.

Required fields:

| ID | Object | Required Fields | Field Constraints |
| --- | --- | --- | --- |
| DCT-001 | Meeting input | `meeting_transcript`, `participants`, `meeting_metadata` | Input must be authorized and tied to one meeting. |
| DCT-002 | Action item | `id`, `title`, `owner`, `due_date`, `source_excerpt`, `confidence`, `status`, `edited`, `edited_fields` | `owner` and `due_date` may be null when not present in the meeting text; `source_excerpt` may be null only when `status=needs_review`; `confidence` is 0 to 1. |
| DCT-003 | Export payload | Confirmed action item `title`, `owner`, `due_date`, and source context when available | Only `status=confirmed` items appear in default Markdown export. |

Data sources and outputs:

| ID | Data Source | Transformation | Output |
| --- | --- | --- | --- |
| DATA-001 | Authorized meeting transcript or notes | Extract candidate action items and source excerpts. | Candidate action item array. |
| DATA-002 | Participant list | Match or group candidate owners. | Owner field or `Needs owner confirmation` group. |
| DATA-003 | Human review actions | Update status, edited flag, and changed fields. | Confirmed, rejected, deleted, or still-needs-review records. |
| DATA-004 | Confirmed action items | Format confirmed items into Markdown. | Markdown export. |

Privacy and retention constraints:

| ID | Constraint | Agent Handling |
| --- | --- | --- |
| BAR-004 | Do not process unauthorized meeting content. | Stop and ask for authorization. |
| TECH-005 | Keep only action items, review status, and necessary source excerpts by default. | Do not persist full meeting content. |
| Q-003 | Retention duration for source excerpts is unresolved. | Stop and ask when a concrete retention period is required. |

## 10. Verification Contract

### 10.1 Positive Cases

| ID | Related Requirements | Related AC | Input | Expected Result |
| --- | --- | --- | --- | --- |
| VER-001 | REQ-001, REQ-005 | AC-001, AC-005 | "Zhang San will submit the API draft by next Friday." | Generate one candidate action item with `title`, `owner=Zhang San`, `due_date` set to next Friday, non-empty `source_excerpt`, and `confidence` between 0 and 1. |
| VER-002 | REQ-002 | AC-002 | "Li Lei will organize user interviews, and Han Meimei will confirm the design." | Generate two action items and group them by owner. |
| VER-003 | REQ-003, REQ-004 | AC-003, AC-004 | User edits the due date and confirms the item. | Markdown export uses the edited value. |
| VER-004 | REQ-003, REQ-004 | AC-003, AC-004 | User edits an item and then confirms it. | Set `edited` to `true`, keep changed fields in `edited_fields`, set `status` to `confirmed`, and include the item in Markdown export. |

### 10.2 Negative Cases

| ID | Related Requirements Or Controls | Related AC | Input | Expected Result |
| --- | --- | --- | --- | --- |
| VER-005 | REQ-001 | AC-001 | "We can discuss this direction later." | Do not generate a confirmed action item. |
| VER-006 | STOP-003 | AC-002 | Missing participant list. | Block execution and report the missing input. |
| VER-007 | REQ-005, EXE-004 | AC-005 | Candidate item has no source excerpt. | Set status to `needs_review`; do not default to confirmed. |
| VER-008 | REQ-003, REQ-004, STATE-001 | AC-003, AC-004 | User edits an item but does not confirm it. | Set `edited` to `true`; keep `status` unchanged; do not include the item in Markdown export unless it is later confirmed. |

### 10.3 Consistency Checks

| ID | Check | Related Contract Area | Pass Criteria |
| --- | --- | --- | --- |
| VER-009 | Requirement IDs | Requirements And Acceptance Criteria | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, and `REQ-005` exactly match the canonical contract and the sibling Human PRD. |
| VER-010 | Non-goals | Scope Contract; Stop Conditions | The implementation does not add boards, Gantt charts, automatic task commitment, unauthorized data processing, or external task-system sync in Phase 1. |
| VER-011 | Success metrics | Human PRD sibling artifact; canonical contract metrics | Implementation and instrumentation do not redefine the canonical contract success metrics. |
| VER-012 | Risk controls | Execution Contract; Data Contract; Stop Conditions | Human confirmation, source excerpts, and authorized input checks are present. |
| VER-013 | Implementation decisions | Implementation Constraints | LLM structured JSON extraction, web review page, Markdown-only MVP export, and data minimization constraints are preserved. |
| VER-014 | State transitions | State Transition Contract | Edit, confirm, reject, delete, and export eligibility follow the State Transition Contract. |

### 10.4 Blocking Failures

| ID | Blocking Failure | Related Contract Area | Blocking | Failure Handling |
| --- | --- | --- | --- | --- |
| VER-015 | Any blocking acceptance criterion for `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, or `REQ-005` fails. | Requirements And Acceptance Criteria; Done Criteria | true | Mark the implementation as not complete; do not claim execution-ready delivery. |
| VER-016 | A required input is missing, unauthorized, or outside the allowed `export_target=markdown` boundary. | Input Contract; Stop Conditions | true | Stop and ask for the missing authorized input or a confirmed scope change. |
| VER-017 | The implementation creates or commits tasks without explicit human confirmation. | Execution Contract; State Transition Contract; Stop Conditions | true | Block completion and remove or correct the behavior. |
| VER-018 | An item without `source_excerpt` defaults to confirmed or appears in the default export. | Data Contract; Verification Contract VER-007 | true | Block completion and keep the item in `needs_review`. |
| VER-019 | The implementation treats edit, delete, or reject as confirmation. | State Transition Contract; Verification Contract VER-008 | true | Block completion and require explicit confirmation for export eligibility. |
| VER-020 | The implementation adds Phase 2 task-system sync during Phase 1. | Scope Contract; Open Decisions; Stop Conditions | true | Stop, defer the request, or require a confirmed roadmap change. |
| VER-021 | The canonical contract, Human PRD, and Agent PRD disagree on facts, scope, requirement IDs, acceptance criteria, or phase boundaries. | Consistency Checks; GATE-007 global consistency gate | true | Stop until the contract conflict is resolved. |

## 11. Output Contract

The Agent must deliver:

| ID | Output | Requirement |
| --- | --- | --- |
| OUT-001 | Feature implementation | Satisfies `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, and `REQ-005`. |
| OUT-002 | Test or verification record | Covers positive cases, negative cases, consistency checks, and blocking failures. |
| OUT-003 | Markdown export output | Contains only action items with `status: confirmed`, including confirmed items that have `edited: true`. |
| OUT-004 | Residual-scope note | State that external task-system sync is Phase 2 scope and is not implemented in the MVP. |

## 12. Open Decisions

These decisions are defined by the canonical contract and must not be resolved by the Agent during Phase 1 implementation:

| ID | Decision | Impact | Owner | Phase | Agent Handling | Status | Resolution References |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q-001 | First task-system integration choice: Jira, Linear, or Asana. | Determines the first external sync adapter and task payload shape. | Product owner | Phase 2 | Do not implement. Mention as deferred scope if requested. | open | - |
| Q-002 | Per-owner distributed confirmation. | Changes the review flow, notification model, and confirmation authority. | Product owner | Phase 3 | Do not implement. Use organizer-led confirmation for MVP. | open | - |
| Q-003 | Source-excerpt retention duration. | Affects privacy handling, storage policy, and auditability. | Product owner with privacy reviewer | Phase 1 | Keep only necessary source excerpts. Stop and ask if a concrete retention policy is required. | open | - |

## 13. Stop Conditions

The Agent must stop and ask a human when:

| ID | Trigger | Reason | Status | Required Human Action | Resolution References | Related Risk Or Bar |
| --- | --- | --- | --- | --- | --- | --- |
| STOP-006 | The user asks to automatically create unconfirmed tasks. | The MVP requires human confirmation before task commitment. | defined | Confirm a scope change or reject the request. | - | BAR-001 Human confirmation bar |
| STOP-002 | The user asks to process unauthorized or sensitive meeting content. | The product must not process unauthorized or sensitive data. | defined | Provide authorization and data handling approval, or remove the content. | - | RISK-003 Privacy risk |
| STOP-007 | The user asks for external task-system sync during Phase 1 implementation. | External sync is Phase 2 scope, not MVP scope. | defined | Confirm a roadmap change or keep the request deferred. | - | OOS-005 Scope boundary |
| STOP-008 | The canonical contract, Human PRD, and Agent PRD conflict on requirement IDs, scope, or acceptance criteria. | Execution would no longer be traceable to one authoritative contract. | defined | Resolve the contract conflict before implementation continues. | - | GATE-007 global consistency gate |
| STOP-009 | The Agent cannot determine whether an item is an action item, discussion item, or decision record, and the ambiguity affects export output. | Ambiguous extraction may create incorrect commitments. | defined | Clarify the item classification or exclude it from export. | - | BAR-002 Quality bar |
| STOP-010 | The implementation requires a concrete retention period for source excerpts and no human decision exists. | Retention duration is an open privacy decision. | defined | Provide the retention policy or approve a narrower storage behavior. | - | Q-003 Privacy decision |

## 14. Done Criteria

All of the following must be true before completion:

| ID | Completion Condition | Verification Reference | Blocking |
| --- | --- | --- | --- |
| DONE-001 | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, and `REQ-005` pass acceptance. | Requirements And Acceptance Criteria; VER-001; VER-002; VER-003; VER-004; VER-005; VER-006; VER-007; VER-008 | Yes |
| DONE-002 | Negative cases do not produce incorrect confirmed items. | VER-005; VER-006; VER-007; VER-008 | Yes |
| DONE-003 | Items without source excerpts do not default to confirmed. | REQ-005; VER-007 | Yes |
| DONE-004 | Unconfirmed, deleted, and rejected items do not appear in the default export. | REQ-004; State Transition Contract; VER-008 | Yes |
| DONE-005 | The canonical contract, Human PRD, and Agent PRD remain consistent on facts, scope, requirement IDs, and acceptance criteria. | VER-009; VER-021; GATE-007 | Yes |
| DONE-006 | Implementation preserves the canonical contract decisions for LLM structured JSON extraction, web review page, Markdown-only MVP export, Phase 2 task-system sync, and data minimization. | TECH-001; TECH-002; TECH-003; TECH-004; TECH-005; VER-013 | Yes |
| DONE-007 | Open decisions are not self-resolved by the Agent, and any request touching them is deferred or escalated according to the Open Decisions and Stop Conditions sections. | Q-001; Q-002; Q-003; STOP-007; STOP-010 | Yes |
| DONE-008 | Editing does not imply confirmation, and export eligibility follows the State Transition Contract. | STATE-001; STATE-002; STATE-003; STATE-004; STATE-005; VER-004; VER-008 | Yes |

## References

[REF-001] Canonical Post-Meeting Action Hub contract: source contract used to render both reference PRDs.

[REF-002] Human PRD sibling review artifact: `human-prd-example-meeting-action-hub.md`
