# Scheduler Agent PRD

render_status.agent_prd=execution_ready. This document is derived from `contract-envelope.json` and must not be treated as an independent source of product facts.

## Document Metadata

Product: Scheduler. Document version: 0.1. Date: 2026-05-29. Source contract: `contract-envelope.json` with primary sources `SRC-001` and `SRC-002`. Current phase: `PHASE-001`.

## Executive Summary

Scheduler is a daemon scheduling controller and state judge that advances already-defined workflow routes into executable, recoverable, auditable job-state flows. It controls dispatch, lease authority, result acceptance, blocking, failure, and route exhaustion through deterministic rules; it does not design routes, execute tasks, or declare business success. See `CORE-001`, `SCOPE-001`, `REQ-001`, and `REQ-008`.

## Problem and Background

Existing workflow routes need a conservative runtime controller that can decide when a node is ready, when a job instance and lease may be issued, when Executor evidence is valid, and when no more scheduling is possible. Without that boundary, route mutation, duplicate execution, stale results, and unsupported success claims can corrupt route state. See `REQ-002`, `REQ-003`, `REQ-004`, `REQ-005`, `RISK-001`, and `RISK-002`.

## Target Users and Personas

Primary users are workflow platform integrators and Executor service owners who need an API-callable daemon to advance route state safely. Secondary users are operations reviewers who need audit records explaining dispatch, acceptance, rejection, blocking, expiry, and route exhaustion decisions. See `USER-001` and `CORE-001`.

## Goals and Outcomes

The MVP must deliver a mechanical Scheduler that dispatches only ready nodes, creates idempotent job instances and leases, validates Executor results with identity and evidence, records state events, and emits route_exhausted without business success inference. Outcomes map to `DONE-001`, `DONE-002`, and `DONE-003`.

## Success Metrics

Success is measured by duplicate active dispatch prevention (`MET-001`), stale result rejection (`MET-002`), and decision audit coverage (`MET-003`). These metrics must be verified with repository-local real fixtures, especially `VER-003`, `VER-004`, and `VER-007`.

## Scope and Non-Goals

In scope: daemon API boundary, persistent state and lease authority, readiness evaluation, idempotent dispatch, lease/fencing token management, Executor-result validation, job/node state transitions, state events, blocking records, acceptance/rejection records, and route exhaustion records. Out of scope: route design, new node generation, direct command execution, deliverable mutation, skipping evidence checks, completed-as-deliveried shortcuts, execution-narrative success, and project success declarations. See `SCOPE-001`, `OOS-001`, `EXE-002`, and `BAR-002`.

## User Stories and Use Cases

As a workflow platform integrator, I can call Scheduler through an API so that ready route nodes are dispatched without embedding scheduling rules in the caller (`TECH-001`, `REQ-003`). As an Executor owner, I can submit a result with lease identity, fencing token, status, and evidence so that Scheduler accepts only valid outcomes (`IN-002`, `REQ-005`). As an operations reviewer, I can inspect state events and rejection records to understand why a node advanced, failed, blocked, expired, or exhausted (`REQ-007`, `OUT-003`, `OUT-004`).

## Functional Requirements

Functional requirements are `REQ-001` through `REQ-008`: preserve Scheduler ownership boundaries, run the fixed scheduling loop, perform readiness and idempotent dispatch, manage leases and fencing tokens, validate Executor evidence, express outcomes through state machine transitions, record auditable evidence, and report route exhaustion without success inference. Acceptance is bound to `AC-001` through `AC-008` and verification is bound to `VER-001` through `VER-008`.

## Non-Functional Requirements and Guardrails

Scheduler must be mechanical, conservative, deterministic, recoverable, and auditable. Guardrails include persistent transactional state authority (`TECH-002`), deterministic state machine transitions (`TECH-003`), no route mutation (`REQ-001`), no direct task execution (`EXE-002`), no evidence bypass (`STOP-003`), and no success inference on exhaustion (`STOP-004`).

## User Flow or UX Notes

The caller interacts with Scheduler as a daemon API, not as a route authoring tool. A typical flow is: caller triggers or waits for a scheduling loop; Scheduler reads authoritative state; Scheduler dispatches eligible nodes by creating `JobInstance` and `ExecutionLease`; Executor later provides `ExecutorResult`; Scheduler validates identity and evidence; Scheduler emits `StateEvent` records and updated job/node states. See `FLOW-001`, `DCT-002`, `DCT-003`, `DCT-004`, and `DCT-005`.

## Acceptance Criteria

The product is acceptable only when all current criteria pass: no route-definition mutation (`AC-001`), correct loop order (`AC-002`), idempotent dispatch (`AC-003`), lease/fencing stale rejection (`AC-004`), evidence-gated Executor result handling (`AC-005`), valid job/node transitions (`AC-006`), audit event coverage (`AC-007`), and route exhaustion without business success (`AC-008`).

## Release Plan and Roadmap

Phase `PHASE-001` delivers PRD and HLD-ready requirements for Scheduler as a daemon API with persistent state and repository-local acceptance fixtures. Future implementation can select concrete API and storage technologies during detailed design or implementation, but this workflow must not output implementation task decomposition. See `SCOPE-001`, `BAR-002`, and `DONE-003`.

## Risks, Assumptions, and Dependencies

Risk `RISK-001` covers duplicate jobs and stale writes if transaction and fencing semantics are weak. Risk `RISK-002` covers accepting Executor narration instead of mechanical evidence. Dependencies are authoritative route state, persistent state/lease storage, Executor result/evidence payloads, and repository-local real fixtures. Clarifications `Q-001`, `Q-002`, and `Q-003` are resolved by `SRC-002`.

## Open Questions

No blocking product question remains for PRD rendering. `Q-001`, `Q-002`, and `Q-003` were resolved by `SRC-002`; HLD may still ask narrower implementation questions if concrete API operations, storage transaction behavior, or acceptance command details are missing.

## Traceability

Current execution-ready refs covered by this PRD: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, AC-001, AC-002, AC-003, AC-004, AC-005, AC-006, AC-007, AC-008, VER-001, VER-002, VER-003, VER-004, VER-005, VER-006, VER-007, VER-008, IN-001, IN-002, EXE-001, EXE-002, EXE-003, OUT-001, OUT-002, OUT-003, OUT-004, OUT-005, STOP-001, STOP-002, STOP-003, STOP-004, DONE-001, DONE-002, DONE-003, FLOW-001, DATA-001, DATA-002, DATA-003, MOD-001, MOD-002, MOD-003, TECH-001, TECH-002, TECH-003, STATE-001, STATE-002, DCT-001, DCT-002, DCT-003, DCT-004, DCT-005. Product source refs: `SRC-001`, `SRC-002`, and output path ref `SRC-003`.

## Source of Truth

The only source of truth is `contract-envelope.json`. Human and Agent PRDs are sibling renders from the requirement table and canonical objects. Important source refs are `SRC-001` for the original Scheduler idea and `SRC-002` for daemon API, persistent storage, and repository-local real acceptance confirmations.

## Reader and Mission

This PRD is for another agent that must produce or review downstream design without inventing product facts. The reader must preserve Scheduler as a state-control daemon and must not turn it into a route designer, task executor, or business-success judge.

## Requirement Trace

Requirement trace: `REQ-001` -> `AC-001` -> `VER-001`; `REQ-002` -> `AC-002` -> `VER-002`; `REQ-003` -> `AC-003` -> `VER-003`; `REQ-004` -> `AC-004` -> `VER-004`; `REQ-005` -> `AC-005` -> `VER-005`; `REQ-006` -> `AC-006` -> `VER-006`; `REQ-007` -> `AC-007` -> `VER-007`; `REQ-008` -> `AC-008` -> `VER-008`.

## Input Contract

Scheduler consumes `IN-001` authoritative route and scheduler state plus `IN-002` Executor result and evidence. Data objects are `DCT-001` RouteSnapshot, `DCT-002` JobInstance, `DCT-003` ExecutionLease, `DCT-004` ExecutorResult, and `DCT-005` StateEvent.

## Execution Contract

Execution rules are `EXE-001`, `EXE-002`, and `EXE-003`. Scheduler must run the fixed loop order, refuse forbidden ownership, and use persistent idempotency plus fencing-token checks before accepting or changing state.

## Tool and Integration Boundaries

Scheduler is a daemon API service (`TECH-001`, `MOD-001`). Persistent state and leases are owned by a storage abstraction (`MOD-002`, `TECH-002`). Executor is an external result/evidence producer (`MOD-003`); Scheduler validates Executor outputs but does not run Executor tasks.

## Permissions and Safety

Scheduler may read and write only scheduling authority data: route snapshots, node states, job instances, leases, result decisions, state events, block reasons, and exhaustion records. It must not modify route definitions, create nodes, run commands, alter deliverables, or bypass evidence checks. See `REQ-001`, `EXE-002`, `STOP-001`, `STOP-003`.

## Data and State Contract

Data refs are `DATA-001`, `DATA-002`, and `DATA-003`. State refs are `STATE-001` for node states and `STATE-002` for job states. The HLD must define legal state transitions and reject invalid transitions, stale fencing tokens, expired leases, and unsupported result evidence.

## Verification Contract

Verification cases `VER-001` through `VER-008` must use repository-local real route, node, permission, lease, and Executor result examples. Acceptance must prove no duplicate active jobs, stale result rejection, evidence-gated delivery, audit event completeness, and route exhaustion without success inference.

## Output Contract

Scheduler outputs `OUT-001` job instances, `OUT-002` execution leases, `OUT-003` state events, `OUT-004` accepted/rejected/expired/blocked decision records, and `OUT-005` route exhaustion records. It does not output route definitions, new nodes, command results, modified deliverables, or business-success declarations.

## Stop Conditions

Stop and block or reject when authoritative state is missing or contradictory (`STOP-001`), lease identity or fencing token is stale (`STOP-002`), evidence is missing or undecidable (`STOP-003`), or the route is exhausted (`STOP-004`). Stop conditions must produce auditable records.

## Done Criteria

Done means `DONE-001`, `DONE-002`, and `DONE-003`: deterministic dispatch and duplicate prevention, evidence-valid result acceptance with stale/failed rejection, and auditable state transitions plus route exhaustion without route mutation or success inference.

## Forbidden Assumptions

Do not assume Scheduler can modify route definitions, create nodes, execute commands, edit deliverables, trust Executor completed, infer success from execution narration, accept stale results, skip evidence checks, or declare business completion when no schedulable node remains. Do not add implementation task plans to this PRD.
