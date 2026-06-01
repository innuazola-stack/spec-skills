# Meeting Action Extractor Agent PRD

Source contract: `contract-envelope.json`

render_status.agent_prd=execution_ready

## Document Metadata

- Product: Meeting Action Extractor (`CORE-001`)
- Contract: `contract-envelope.json`
- Version: `1.8`
- Current phase: `PHASE-001`
- Status: `execution_ready`
- Primary source: `SRC-001`

## Executive Summary

Build the Phase 1 Meeting Action Extractor: a bounded tool that accepts authorized transcript text, extracts reviewable action items with evidence, requires human confirmation, and exports a confirmed Markdown action-item list. The PRD is execution-ready for the current phase because the input, execution rule, verification case, output, stop condition, and done criterion are all represented by `IN-001`, `EXE-001`, `VER-001`, `OUT-001`, `STOP-001`, and `DONE-001`.

## Problem and Background

Teams lose follow-up accountability after meetings because action items are scattered in transcripts (`CORE-001`). The product should convert authorized transcript text into a reviewable list of action items so operators can trust and edit the list before sharing it (`REQ-001`).

## Target Users and Personas

Primary users are product and project operators who review meeting outcomes and prepare follow-up lists (`CORE-001`). No additional personas are defined in the contract; do not invent roles beyond this user group.

## Goals and Outcomes

- Provide a reliable Phase 1 workflow for extracting action items from authorized transcript text (`SCOPE-001`, `REQ-001`).
- Require human confirmation before export so users can trust and edit the result (`EXE-001`, `AC-001`).
- Keep Phase 1 focused on Markdown export without external task-system creation (`OOS-001`).

## Success Metrics

No separate `MET-*` KPI is defined in the source contract. For this phase, release success is measured by the binary acceptance and verification evidence in `AC-001` and `VER-001`: a transcript with one explicit action item produces a reviewable item, waits for confirmation, and exports Markdown only after confirmation.

## Scope and Non-Goals

In scope: authorized transcript text input, evidence-backed action item extraction, human confirmation, and Markdown export (`SCOPE-001`, `REQ-001`).

Out of scope: automatic Jira, Linear, Asana, calendar, or email task creation (`OOS-001`).

## User Stories and Use Cases

- As a product or project operator, I want to submit authorized transcript text so that I can identify follow-up action items (`IN-001`, `REQ-001`).
- As a reviewer, I want each action item to include source evidence so that I can verify it before export (`AC-001`, `EXE-001`).
- As an operator, I want Markdown export only after confirmation so that unreviewed action items are not shared (`OUT-001`, `DONE-001`).

## Functional Requirements

- The product must accept authorized transcript text (`IN-001`).
- The product must identify action item, owner, due date when present, and evidence quote (`REQ-001`, `AC-001`).
- The product must require human confirmation before Markdown export (`EXE-001`, `AC-001`).
- The product must export a confirmed Markdown action-item list (`OUT-001`).

## Non-Functional Requirements and Guardrails

- Process only authorized transcript text (`IN-001`, `STOP-001`).
- Do not export unconfirmed action items (`EXE-001`, `DONE-001`).
- Do not create tasks or write to external systems in Phase 1 (`OOS-001`).
- Do not infer missing owners or due dates without transcript evidence (`EXE-001`, `AC-001`).

## User Flow or UX Notes

The Phase 1 user flow is: provide authorized transcript text, extract evidence-backed action items, present them for human confirmation, then export confirmed Markdown. No wireframes or UI artifacts are defined in the contract.

## Acceptance Criteria

`AC-001`: Given authorized transcript text with one explicit action item, the output includes action, owner, due date if present, evidence quote, and waits for confirmation before Markdown export.

## Release Plan and Roadmap

`PHASE-001` is the complete current release scope: authorized transcript input, reviewable extraction, human confirmation, and Markdown export. External task-system creation is not part of this release and must remain out of scope unless a later requirement-table revision adds it.

## Risks, Assumptions, and Dependencies

The contract defines no blocking assumptions or risks for this ready fixture. The main dependency is user-provided authorized transcript text (`IN-001`). Missing authorization triggers `STOP-001`.

## Open Questions

No blocking open questions remain for Phase 1 execution readiness.

## Traceability

- `SRC-001` states the original product idea.
- `TRACE-001` connects `SRC-001` to `REQ-001`.
- `REQ-001` is verified by `AC-001` and `VER-001`.
- Product rendering is covered by `RB-001` and agent execution rendering by `RB-002`.

## Source of Truth

Use `contract-envelope.json`. Current execution scope is `PHASE-001`. Do not use this PRD to introduce facts that are absent from the contract.

## Reader and Mission

Reader: downstream implementation or design agent. Mission: implement the Phase 1 meeting action extractor without inventing integrations or bypassing human confirmation.

## Requirement Trace

Primary requirement: `REQ-001`. Acceptance: `AC-001`. Verification: `VER-001`. Current scope: `SCOPE-001`; excluded scope: `OOS-001`.

## Input Contract

Use `IN-001`: authorized transcript text is required.

## Execution Contract

Use `EXE-001`: extract only action items supported by transcript evidence and require human confirmation before export.

## Tool and Integration Boundaries

No external task-system integration is allowed in Phase 1. Do not call Jira, Linear, Asana, calendar, or email APIs.

## Permissions and Safety

Process only authorized transcript text. Do not export unconfirmed action items and do not perform external writes.

## Data and State Contract

No persistent state is required for this fixture. Keep transcript-derived action items reviewable before export.

## Verification Contract

Use `VER-001` and `AC-001`.

## Output Contract

Use `OUT-001`: confirmed Markdown export only.

## Stop Conditions

Use `STOP-001`.

## Done Criteria

Use `DONE-001`.

## Forbidden Assumptions

Do not assume external task creation, missing authorization, unconfirmed export, hidden integrations, or inferred owners/due dates without transcript evidence.
