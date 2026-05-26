# Execution Task Plan Example: Post-Meeting Action Hub

## Revision History

| Version | Date | Author | Change | Basis |
| --- | --- | --- | --- | --- |
| v1.0 | 2026-05-26 | Codex | Added a good example of decomposing the existing Agent PRD example into an execution task plan. | User request: try decomposing the generated instance into a good task breakdown example |
| v1.1 | 2026-05-26 | Codex | Aligned the example with the `execution_task_plan` schema, added closure-card verification refs, module refs, and explicit stop/defer and verification/done mappings. | Convergence review fix |
| v1.2 | 2026-05-26 | Codex | Hardened source metadata, canonical phase refs, structured field mapping, parallel groups, and gate evidence refs. | Convergence review fix |

## 1. Purpose

This reference shows how to turn `agent-prd-example-meeting-action-hub.md` into an `execution_task_plan` without adding new product facts. It demonstrates three hard principles:

1. Each task is closed: it carries its own goal, inputs, outputs, allowed boundary, forbidden boundary, acceptance, verification, stop conditions, and dependencies.
2. Each task can be accepted independently: a reviewer can judge pass/fail for the task without waiting for the whole PRD to be done.
3. All non-deferred tasks together cover the Phase 1 PRD goal: extract, review, confirm, and export post-meeting action items while preserving evidence, human confirmation, scope boundaries, and verification.

This file is a reference example. It does not replace the Agent PRD or the canonical contract.

## 2. Source And Planning Status

| Field | Value |
| --- | --- |
| `plan_id` | `ETP-MAH-001` |
| `planning_source_mode` | `contract_backed` |
| `source_artifacts.contract_ref` | Canonical Post-Meeting Action Hub contract used to render `agent-prd-example-meeting-action-hub.md`; not the minimal smoke fixture. |
| `source_artifacts.contract_version` | `1.8` |
| `source_artifacts.agent_prd_ref` | `agent-prd-example-meeting-action-hub.md` |
| `source_artifacts.agent_prd_status` | `execution_ready` |
| `source_artifacts.phase_ref` | `PHASE-001` |
| `source_artifacts.phase_label` | `Phase 1 MVP` |
| `source_artifacts.phase_ref_kind` | `canonical_id` |
| `source_artifacts.phase_ref_fallback_reason` | Empty; canonical phase ID is available from the source contract metadata. |
| `planning_status` | `ready` |
| `blocking_reasons` | Empty. |
| `missing_required_refs` | Empty. |
| `required_fixes` | Empty. |
| `task_graph` | Sections 4 and 5 together: summary rows provide task identity and refs; closure cards provide inputs, outputs, boundaries, acceptance, verification, stop conditions, and dependencies. |
| `dependency_edges` | Section 6, Dependency Edges. |
| `parallel_groups` | Section 7, Parallel Groups. |
| `stage_goal_coverage` | Section 10, Stage Goal Coverage. |
| `planning_gate_report` | Section 11, Planning Gate Report. |
| Runtime assumption | Repository file paths are unknown, so allowed boundaries use PRD module names and `MOD-*` references instead of concrete paths. |

Structured field mapping:

| `execution_task_plan` field | Rendered source in this example |
| --- | --- |
| `source_artifacts` | Section 2 source rows. |
| `task_graph[*].task_id/title/task_type/status/parallel_group` | Section 4 task graph summary. |
| `task_graph[*].contract_refs/verification_refs/done_refs/dependencies` | Section 4 summary plus Section 9 verification and done mapping. |
| `task_graph[*].inputs/outputs/allowed_files_or_modules/forbidden_scope_refs/acceptance/verification/stop_conditions` | Section 5 closure cards. |
| `dependency_edges` | Section 6 dependency edge table. |
| `parallel_groups` | Section 7 parallel group table. |
| `stage_goal_coverage` | Section 10 stage goal coverage table and reasoning. |
| `planning_gate_report[*].evidence_refs` | Section 11 `Evidence Refs`; only stable IDs. |
| `planning_gate_report[*].evidence_summary` | Section 11 `Evidence Summary`; human-readable explanation. |

## 3. Decomposition Rationale

The plan first isolates entry blockers and data contracts, because extraction, review, and export all depend on valid meeting input and stable action item shape. It then separates extraction, grouping, review state transitions, Markdown export, residual-scope handling, and verification record production.

This produces tasks that are small enough to verify independently, but not so small that they become unreviewable implementation fragments.

## 4. Task Graph Summary

| Task ID | Status | Type | Closed Result | Key Contract Refs | Verification / Done | Dependencies | Parallel Group |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `TASK-001` | `planned` | foundation | Entry validation and stop handling boundary is implemented. | `IN-001`, `IN-002`, `IN-003`, `IN-004`, `STOP-001`, `STOP-002`, `STOP-003`, `STOP-004`, `STOP-005`, `EXE-005`, `DCT-001`, `MOD-001`, `BAR-004`, `RISK-003` | `VER-006`, `VER-016`, `DONE-002` | - | `PG-001` |
| `TASK-002` | `planned` | foundation | Action item, meeting input, and export payload contracts are stable. | `DCT-001`, `DCT-002`, `DCT-003`, `DATA-001`, `DATA-002`, `DATA-003`, `TECH-005`, `MOD-001`, `MOD-002`, `MOD-004`, `Q-003`, `STOP-010` | `VER-013`, `DONE-006` | `TASK-001` | `PG-002` |
| `TASK-003` | `planned` | implementation | Candidate action items are extracted with required fields and evidence behavior. | `REQ-001`, `REQ-005`, `AC-001`, `AC-005`, `EXE-004`, `TECH-001`, `MOD-002`, `DCT-002`, `DATA-001`, `STOP-009`, `BAR-002` | `VER-001`, `VER-005`, `VER-007`, `VER-018`, `DONE-001`, `DONE-002`, `DONE-003` | `TASK-002` | `PG-003` |
| `TASK-004` | `planned` | implementation | Candidate action items are grouped by owner, including missing-owner fallback. | `REQ-002`, `AC-002`, `MOD-002`, `DATA-002`, `DCT-002`, `STOP-003` | `VER-002`, `VER-006`, `DONE-001` | `TASK-002`, `TASK-003` | `PG-004` |
| `TASK-005` | `planned` | implementation | Review operations enforce confirm/edit/delete/reject state transitions. | `REQ-003`, `AC-003`, `EXE-003`, `DATA-003`, `STATE-001`, `STATE-002`, `STATE-003`, `STATE-004`, `STATE-005`, `TECH-002`, `MOD-003`, `STOP-006`, `BAR-001` | `VER-003`, `VER-004`, `VER-008`, `VER-014`, `VER-017`, `VER-019`, `DONE-001`, `DONE-008` | `TASK-003`, `TASK-004` | `PG-005` |
| `TASK-006` | `planned` | implementation | Markdown export includes only confirmed action items and keeps Phase 2 sync out. | `REQ-004`, `AC-004`, `OUT-003`, `DATA-004`, `DCT-003`, `TECH-003`, `MOD-004`, `OOS-001`, `OOS-002`, `OOS-005`, `STOP-006`, `STOP-007`, `BAR-001` | `VER-003`, `VER-004`, `VER-008`, `VER-010`, `VER-020`, `DONE-004`, `DONE-007` | `TASK-005` | `PG-006` |
| `TASK-007` | `planned` | documentation | Residual scope and open decisions are visible and not self-resolved. | `OUT-004`, `OOS-001`, `OOS-002`, `OOS-003`, `OOS-004`, `OOS-005`, `Q-001`, `Q-002`, `Q-003`, `EXE-001`, `EXE-002`, `TECH-004`, `MOD-005`, `STOP-007`, `STOP-010` | `VER-010`, `VER-020`, `DONE-007` | `TASK-006` | `PG-007` |
| `TASK-008` | `planned` | verification | Verification record proves requirements, negative cases, consistency, and blocking failures. | `OUT-001`, `OUT-002`, `STOP-008`, `VER-001`, `VER-002`, `VER-003`, `VER-004`, `VER-005`, `VER-006`, `VER-007`, `VER-008`, `VER-009`, `VER-010`, `VER-011`, `VER-012`, `VER-013`, `VER-014`, `VER-015`, `VER-016`, `VER-017`, `VER-018`, `VER-019`, `VER-020`, `VER-021`, `GATE-007` | `DONE-001`, `DONE-002`, `DONE-003`, `DONE-004`, `DONE-005`, `DONE-006`, `DONE-007`, `DONE-008` | `TASK-001`, `TASK-002`, `TASK-003`, `TASK-004`, `TASK-005`, `TASK-006`, `TASK-007` | `PG-008` |

## 5. Closure Cards

### TASK-001: Validate Inputs And Entry Blockers

| Field | Value |
| --- | --- |
| Inputs | `meeting_transcript`, `participants`, `meeting_metadata`, optional `export_target`. |
| Outputs | Validated input object or a stop report naming the missing or invalid input. |
| Allowed boundary | Meeting input module; input validation; entry blocker reporting. |
| Forbidden boundary | Extraction, review UI, export, external sync, or inferred authorization. |
| Independent acceptance | Missing transcript, empty participants, unauthorized input, and unsupported `export_target` each produce the expected stop behavior; valid inputs pass through unchanged. |
| Verification refs | `VER-006`, `VER-016`, `DONE-002`. |
| Stop conditions | `STOP-001`, `STOP-002`, `STOP-003`, `STOP-004`, `STOP-005`. |
| Dependencies | None. |

### TASK-002: Stabilize Data Contracts

| Field | Value |
| --- | --- |
| Inputs | Validated meeting input from `TASK-001`; PRD data contract definitions. |
| Outputs | Stable internal shapes for meeting input, action item, and Markdown export payload. |
| Allowed boundary | Data model and transformation boundary for `DCT-001`, `DCT-002`, `DCT-003`. |
| Forbidden boundary | LLM prompt behavior, review actions, export rendering, retention policy invention. |
| Independent acceptance | Required fields, nullable rules, `confidence` range, `source_excerpt` behavior, and confirmed-only export payload constraints are represented in the model or validation layer. |
| Verification refs | `VER-013`, `DONE-006`. |
| Stop conditions | Stop if implementation needs a concrete source-excerpt retention policy not supplied by `Q-003` / `STOP-010`. |
| Dependencies | `TASK-001`. |

### TASK-003: Extract Candidate Action Items With Evidence

| Field | Value |
| --- | --- |
| Inputs | Valid meeting text and stable action item schema. |
| Outputs | Candidate action item array with title, owner, due date, source excerpt, confidence, and initial status. |
| Allowed boundary | Extraction logic and evidence handling. |
| Forbidden boundary | Human confirmation, export, task-system sync, or default confirmation without explicit user action. |
| Independent acceptance | `VER-001` produces a candidate with required fields and non-empty source excerpt; `VER-005` does not create a confirmed item from vague discussion; `VER-007` keeps source-less candidates in `needs_review`. |
| Verification refs | `VER-001`, `VER-005`, `VER-007`, `VER-018`, `DONE-001`, `DONE-002`, `DONE-003`. |
| Stop conditions | `STOP-009` when classification ambiguity affects export output. |
| Dependencies | `TASK-002`. |

### TASK-004: Group Candidates By Owner

| Field | Value |
| --- | --- |
| Inputs | Candidate action item array and participant list. |
| Outputs | Grouped candidate list by owner, including `Needs owner confirmation`. |
| Allowed boundary | Owner grouping and missing-owner fallback. |
| Forbidden boundary | Inventing owners beyond the participant list and meeting text; review action state changes. |
| Independent acceptance | `VER-002` groups identified owners separately and places unidentified owners in the fallback group. |
| Verification refs | `VER-002`, `VER-006`, `DONE-001`. |
| Stop conditions | `STOP-003` if participant input is missing and grouping cannot be evaluated. |
| Dependencies | `TASK-002`, `TASK-003`. |

### TASK-005: Enforce Review State Transitions

| Field | Value |
| --- | --- |
| Inputs | Grouped candidate list. |
| Outputs | Reviewable candidates with confirm, edit, delete, reject transitions and persisted state fields. |
| Allowed boundary | Review page behavior and state transition rules. |
| Forbidden boundary | Treating edit, delete, or reject as confirmation; exporting unconfirmed items. |
| Independent acceptance | `VER-003`, `VER-004`, and `VER-008` prove edit/confirm behavior; `VER-014`, `VER-017`, and `VER-019` prove state and blocking rules. |
| Verification refs | `VER-003`, `VER-004`, `VER-008`, `VER-014`, `VER-017`, `VER-019`, `DONE-001`, `DONE-008`. |
| Stop conditions | `STOP-006` when a request tries to automatically create or commit unconfirmed tasks. |
| Dependencies | `TASK-003`, `TASK-004`. |

### TASK-006: Export Confirmed Items To Markdown

| Field | Value |
| --- | --- |
| Inputs | Reviewed action items with explicit confirmation status. |
| Outputs | Markdown export containing only confirmed action items, including confirmed edited values. |
| Allowed boundary | Markdown export generation and export eligibility filtering. |
| Forbidden boundary | External task-system sync, boards, Gantt charts, auto-commit behavior. |
| Independent acceptance | Confirmed items export; unconfirmed, deleted, and rejected items do not export; edited confirmed values appear in Markdown. |
| Verification refs | `VER-003`, `VER-004`, `VER-008`, `VER-010`, `VER-020`, `DONE-004`, `DONE-007`. |
| Stop conditions | `STOP-007` when the request requires external task-system sync during Phase 1. |
| Dependencies | `TASK-005`. |

### TASK-007: Preserve Residual Scope And Open Decisions

| Field | Value |
| --- | --- |
| Inputs | Output scope and open decisions from the Agent PRD. |
| Outputs | Residual-scope note that states external task-system sync is Phase 2 and open decisions are not resolved. |
| Allowed boundary | Documentation of deferred scope and stop/defer handling. |
| Forbidden boundary | Choosing Jira, Linear, or Asana; distributed confirmation; concrete source-excerpt retention period. |
| Independent acceptance | Residual scope names Phase 2 sync as deferred, and any request touching `Q-001`, `Q-002`, or `Q-003` is either deferred or stopped according to `STOP-007` and `STOP-010`. |
| Verification refs | `VER-010`, `VER-020`, `DONE-007`. |
| Stop conditions | `STOP-007`, `STOP-010`. |
| Dependencies | `TASK-006`. |

### TASK-008: Produce Verification Record

| Field | Value |
| --- | --- |
| Inputs | Outputs from `TASK-001` through `TASK-007`. |
| Outputs | Test or verification record covering positive cases, negative cases, consistency checks, and blocking failures. |
| Allowed boundary | Verification execution, evidence capture, final consistency check. |
| Forbidden boundary | Changing requirements or weakening acceptance criteria to pass tests. |
| Independent acceptance | The record shows pass/fail evidence for `VER-001` through `VER-021`, and every blocking failure maps to the required failure handling. |
| Verification refs | `VER-001`, `VER-002`, `VER-003`, `VER-004`, `VER-005`, `VER-006`, `VER-007`, `VER-008`, `VER-009`, `VER-010`, `VER-011`, `VER-012`, `VER-013`, `VER-014`, `VER-015`, `VER-016`, `VER-017`, `VER-018`, `VER-019`, `VER-020`, `VER-021`, `DONE-001`, `DONE-002`, `DONE-003`, `DONE-004`, `DONE-005`, `DONE-006`, `DONE-007`, `DONE-008`. |
| Stop conditions | `STOP-008` if contract, Human PRD, and Agent PRD conflict during verification. |
| Dependencies | `TASK-001`, `TASK-002`, `TASK-003`, `TASK-004`, `TASK-005`, `TASK-006`, `TASK-007`. |

## 6. Dependency Edges

| From | To | Reason | Contract Refs |
| --- | --- | --- | --- |
| `TASK-001` | `TASK-002` | Data contracts depend on the accepted input boundary. | `IN-001`, `IN-002`, `IN-003`, `IN-004`, `DCT-001` |
| `TASK-002` | `TASK-003` | Extraction must emit the stable action item schema. | `DCT-002`, `DATA-001`, `TECH-001` |
| `TASK-003` | `TASK-004` | Grouping requires extracted candidates. | `REQ-001`, `REQ-002`, `DATA-002` |
| `TASK-003` | `TASK-005` | Review requires candidate action items. | `REQ-003`, `STATE-001`, `STATE-002` |
| `TASK-004` | `TASK-005` | Review page consumes grouped candidates. | `REQ-002`, `REQ-003` |
| `TASK-005` | `TASK-006` | Export eligibility depends on review state. | `REQ-004`, `STATE-002`, `DCT-003` |
| `TASK-006` | `TASK-007` | Residual scope must match actual export boundary. | `OUT-003`, `OUT-004`, `DATA-004`, `OOS-005` |
| `TASK-001` | `TASK-008` | Verification record needs entry blocker evidence. | `VER-006`, `VER-016`, `OUT-002` |
| `TASK-002` | `TASK-008` | Verification record needs data contract evidence. | `VER-013`, `DONE-006`, `OUT-002` |
| `TASK-003` | `TASK-008` | Verification record needs extraction and evidence behavior. | `VER-001`, `VER-005`, `VER-007`, `VER-018`, `OUT-002` |
| `TASK-004` | `TASK-008` | Verification record needs owner grouping evidence. | `VER-002`, `VER-006`, `OUT-002` |
| `TASK-005` | `TASK-008` | Verification record needs review state transition evidence. | `VER-003`, `VER-004`, `VER-008`, `VER-014`, `VER-017`, `VER-019`, `OUT-002` |
| `TASK-006` | `TASK-008` | Verification record needs export and Phase 2 deferral evidence. | `VER-010`, `VER-020`, `OUT-002`, `OUT-003` |
| `TASK-007` | `TASK-008` | Verification record needs residual-scope and open-decision evidence. | `OUT-004`, `DONE-007`, `OUT-002` |

## 7. Parallel Groups

| Parallel Group | Tasks | Status | Conflict Refs | Rationale |
| --- | --- | --- | --- | --- |
| `PG-001` | `TASK-001` | `serial` | - | Starts first; no parallel work should bypass input and authorization checks. |
| `PG-002` | `TASK-002` | `serial` | `TASK-001` | Follows input boundary; stabilizes shared contracts. |
| `PG-003` | `TASK-003` | `serial` | `TASK-002` | Extraction is isolated after schema stabilization. |
| `PG-004` | `TASK-004` | `serial` | `TASK-003` | Grouping depends on extraction but can be accepted without export. |
| `PG-005` | `TASK-005` | `serial` | `TASK-003`, `TASK-004` | Review state machine must be serialized with export eligibility. |
| `PG-006` | `TASK-006` | `serial` | `TASK-005` | Export must finish before the residual-scope note can truthfully describe what was not implemented. |
| `PG-007` | `TASK-007` | `serial` | `TASK-006` | Residual scope follows export boundary and remains independently acceptable as documentation. |
| `PG-008` | `TASK-008` | `serial` | `TASK-001`, `TASK-002`, `TASK-003`, `TASK-004`, `TASK-005`, `TASK-006`, `TASK-007` | Runs last as final verification evidence. |

## 8. Stop/Defer Report

| Control Refs | Handling Task Refs | Handling |
| --- | --- | --- |
| `STOP-001`, `STOP-002`, `STOP-003`, `STOP-004`, `STOP-005`, `BAR-004`, `RISK-003` | `TASK-001`, `TASK-008` | Validate required input and authorization before extraction; record blocking evidence in verification. |
| `STOP-006`, `BAR-001`, `OOS-002` | `TASK-005`, `TASK-006`, `TASK-008` | Enforce explicit human confirmation before export or task commitment. |
| `STOP-007`, `OOS-005`, `Q-001` | `TASK-006`, `TASK-007`, `TASK-008` | Keep external task-system sync deferred to Phase 2 unless the roadmap changes. |
| `STOP-008`, `GATE-007` | `TASK-008` | Stop verification if canonical contract, Human PRD, and Agent PRD conflict. |
| `STOP-009`, `BAR-002` | `TASK-003`, `TASK-008` | Clarify or exclude ambiguous action-item candidates that affect export output. |
| `STOP-010`, `Q-003` | `TASK-002`, `TASK-007`, `TASK-008` | Do not invent a retention period; stop when a concrete policy is required. |
| `OOS-001`, `OOS-003`, `OOS-004` | `TASK-006`, `TASK-007`, `TASK-008` | Keep excluded product-management, unauthorized-data, and non-MVP language-quality scope out of Phase 1. |
| `Q-002` | `TASK-007`, `TASK-008` | Do not implement distributed per-owner confirmation in Phase 1. |

## 9. Verification And Done Mapping

| Verification / Done Refs | Covered By | Notes |
| --- | --- | --- |
| `VER-001`, `VER-005`, `VER-007`, `VER-018`, `DONE-003` | `TASK-003`, `TASK-008` | Extraction must create required fields, reject vague discussion, and keep source-less items in `needs_review`. |
| `VER-002`, `VER-006` | `TASK-001`, `TASK-004`, `TASK-008` | Owner grouping depends on participant input and missing-participant blocking behavior. |
| `VER-003`, `VER-004`, `VER-008`, `VER-014`, `VER-017`, `VER-019`, `DONE-004`, `DONE-008` | `TASK-005`, `TASK-006`, `TASK-008` | Review transitions and export eligibility prove human confirmation and edit behavior. |
| `VER-010`, `VER-020`, `DONE-007` | `TASK-006`, `TASK-007`, `TASK-008` | Phase 2 sync and open decisions remain deferred or stopped. |
| `VER-013`, `DONE-006` | `TASK-002`, `TASK-008` | Implementation decisions and data minimization are preserved. |
| `VER-009`, `VER-011`, `VER-012`, `VER-015`, `VER-016`, `VER-021`, `DONE-005` | `TASK-001`, `TASK-008` | Final verification proves consistency, input blockers, risk controls, success metrics, and blocking failures. |
| `DONE-001`, `DONE-002` | `TASK-003`, `TASK-004`, `TASK-005`, `TASK-006`, `TASK-008` | Current requirements and negative cases pass only after implementation tasks and verification evidence are complete. |

## 10. Stage Goal Coverage

| Phase Ref | Phase Label | Goal Refs | Required Task Refs | Coverage Status | Missing Refs |
| --- | --- | --- | --- | --- | --- |
| `PHASE-001` | `Phase 1 MVP` | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `REQ-005`, `OUT-001`, `OUT-002`, `OUT-003`, `OUT-004`, `DONE-001`, `DONE-002`, `DONE-003`, `DONE-004`, `DONE-005`, `DONE-006`, `DONE-007`, `DONE-008` | `TASK-001`, `TASK-002`, `TASK-003`, `TASK-004`, `TASK-005`, `TASK-006`, `TASK-007`, `TASK-008` | `covered` | - |

Coverage reasoning:

- `REQ-001` and `REQ-005` are closed by `TASK-003` and verified by `TASK-008`.
- `REQ-002` is closed by `TASK-004` and verified by `TASK-008`.
- `REQ-003` is closed by `TASK-005` and verified by `TASK-008`.
- `REQ-004` and `OUT-003` are closed by `TASK-006` and verified by `TASK-008`.
- `OUT-001` is the aggregate feature implementation output closed by `TASK-003`, `TASK-004`, `TASK-005`, and `TASK-006`, then verified by `TASK-008`.
- `OUT-004` and open-decision discipline are closed by `TASK-007`.
- `DONE-001` through `DONE-008` are accepted only after `TASK-008` records verification evidence.

## 11. Planning Gate Report

| Check | Status | Evidence Refs | Evidence Summary | Required Fix |
| --- | --- | --- | --- | --- |
| `CHECK-001: task traceability` | pass | `TASK-001`, `TASK-002`, `TASK-003`, `TASK-004`, `TASK-005`, `TASK-006`, `TASK-007`, `TASK-008` | All tasks list source contract refs. | - |
| `CHECK-002: requirement coverage` | pass | `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `REQ-005`, `TASK-003`, `TASK-004`, `TASK-005`, `TASK-006`, `TASK-008` | Current requirements are covered by implementation tasks and final verification. | - |
| `CHECK-003: verification coverage` | pass | `VER-001`, `VER-002`, `VER-003`, `VER-004`, `VER-005`, `VER-006`, `VER-007`, `VER-008`, `VER-009`, `VER-010`, `VER-011`, `VER-012`, `VER-013`, `VER-014`, `VER-015`, `VER-016`, `VER-017`, `VER-018`, `VER-019`, `VER-020`, `VER-021`, `TASK-008` | Full verification set is covered by the verification record, with local verification refs on implementation tasks. | - |
| `CHECK-004: stop visibility` | pass | `STOP-001`, `STOP-002`, `STOP-003`, `STOP-004`, `STOP-005`, `STOP-006`, `STOP-007`, `STOP-008`, `STOP-009`, `STOP-010`, `TASK-001`, `TASK-003`, `TASK-005`, `TASK-006`, `TASK-007`, `TASK-008` | Stop behavior appears in concrete tasks and the stop/defer report. | - |
| `CHECK-005: dependency soundness` | pass | `TASK-001`, `TASK-002`, `TASK-003`, `TASK-004`, `TASK-005`, `TASK-006`, `TASK-007`, `TASK-008` | Dependency edges are acyclic and each edge has a reason. | - |
| `CHECK-006: phase integrity` | pass | `PHASE-001`, `OOS-005`, `Q-001`, `TASK-006`, `TASK-007` | Phase 2 sync is deferred and not implemented in the Phase 1 export task. | - |
| `CHECK-007: no new facts` | pass | `REF-001`, `PHASE-001`, `TASK-001`, `TASK-002`, `TASK-003`, `TASK-004`, `TASK-005`, `TASK-006`, `TASK-007`, `TASK-008` | Tasks only use facts and IDs from the source contract and Agent PRD example. | - |
| `CHECK-008: parallel safety` | pass | `PG-001`, `PG-002`, `PG-003`, `PG-004`, `PG-005`, `PG-006`, `PG-007`, `PG-008` | No dependency-linked tasks are marked parallel-safe; all groups are intentionally serial. | - |
| `CHECK-009: done alignment` | pass | `DONE-001`, `DONE-002`, `DONE-003`, `DONE-004`, `DONE-005`, `DONE-006`, `DONE-007`, `DONE-008`, `TASK-008` | Done criteria are covered by implementation tasks and accepted through final verification evidence. | - |
| `CHECK-010: task closure` | pass | `TASK-001`, `TASK-002`, `TASK-003`, `TASK-004`, `TASK-005`, `TASK-006`, `TASK-007`, `TASK-008` | Closure cards state inputs, outputs, boundaries, acceptance, verification refs, stop conditions, and dependencies. | - |
| `CHECK-011: independent acceptance` | pass | `TASK-001`, `TASK-002`, `TASK-003`, `TASK-004`, `TASK-005`, `TASK-006`, `TASK-007`, `TASK-008` | Each task has a task-level pass/fail criterion. | - |
| `CHECK-012: phase goal coverage` | pass | `PHASE-001`, `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `REQ-005`, `OUT-001`, `OUT-002`, `OUT-003`, `OUT-004`, `DONE-001`, `DONE-002`, `DONE-003`, `DONE-004`, `DONE-005`, `DONE-006`, `DONE-007`, `DONE-008` | Stage goal coverage is `covered` with no missing refs. | - |

## 12. Why This Is A Good Example

This decomposition avoids three common failures:

- It does not split by vague technical layers such as "frontend", "backend", and "tests"; every task is anchored to PRD objects.
- It does not hide verification in the final task only; each implementation task has local verification refs, while `TASK-008` produces the full verification record.
- It does not claim completion from implementation alone; Phase 1 is complete only when feature output, test record, Markdown export, residual-scope note, stop handling, and all done criteria are covered.
