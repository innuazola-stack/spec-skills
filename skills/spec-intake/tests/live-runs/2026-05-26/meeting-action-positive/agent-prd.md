# Agent PRD Ready Fixture

Status: execution_ready

Source contract: `contract-envelope.json`

## Source of Truth

Use `contract-envelope.json`. Current execution scope is `PHASE-001`.

## Input Contract

Use `IN-001`: authorized transcript text is required.

## Scope Contract

Implement `REQ-001` inside `SCOPE-001`. Respect `OOS-001`: do not create Jira, Linear, Asana, calendar, or email tasks.

## Execution Contract

Use `EXE-001`: extract only evidence-backed action items and require human confirmation before export.

## Data and State Contracts

No persistent state is required for this fixture. Keep transcript-derived action items reviewable before export.

## Verification Contract

Use `VER-001` and `AC-001`.

## Stop

Use `STOP-001`.

## Done

Use `DONE-001`.
