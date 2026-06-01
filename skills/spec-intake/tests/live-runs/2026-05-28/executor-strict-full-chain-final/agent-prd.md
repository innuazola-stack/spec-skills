# Executor Agent PRD

Source contract: `contract-envelope.json`

render_status.agent_prd=execution_ready

## Document Metadata
Product: Executor (`CORE-001`). Contract: `contract-envelope.json`. Intake: `INTAKE-EXECUTOR-STRICT-FULL-CHAIN-20260528-001`. Phase: `PHASE-001`. Status: `execution_ready`. Primary sources: `SRC-001`, `SRC-002`, `SRC-003`, `SRC-004`, `SRC-005`, and `SRC-006`.

## Executive Summary
Build the Executor MVP as a local CLI program that accepts one JSON or YAML task description file. The file supplies the working directory, task description, permissions, skill configuration, delivery standards, delivery method, and a list of reference documents located under the working directory (`REQ-001`, `REQ-002`, `IN-001`). Executor must drive Claude CLI only through ClaudeTmuxAdapter CLI version 1.0.0, using that adapter for launch, state/screen observation, input sending, and output/screen reading (`REQ-003`, `TECH-001`, `SRC-003`, `SRC-004`, `SRC-005`). Subjective progress judgment must be implemented as a dedicated openclaw-callable skill that consumes Claude CLI screen evidence and task context, then returns progress and next-instruction decisions (`REQ-007`, `REQ-010`, `AC-010`, `TECH-002`, `SRC-006`). Before handoff, Executor must run mechanical delivery checks and emit structured result, logs, and evidence (`REQ-005`, `REQ-008`, `OUT-001`, `DONE-001`).

## Problem and Background
Users need a command-line executor that can turn a structured task description and local reference documents into a controlled Claude CLI execution flow (`CORE-001`, `REQ-001`). The raw idea names two existing capabilities: openclaw for subjective agent judgment and ClaudeTmuxAdapter for mechanical Claude CLI session control (`SRC-001`, `SRC-002`). Local ClaudeTmuxAdapter evidence confirms that its boundary is mechanical: launch, capture, status detection, input, output reading, and termination are structured operations, while semantic task judgment and delivery verdicts remain outside the adapter (`SRC-003`, `SRC-004`).

## Target Users and Personas
The MVP user is a command-line operator who can prepare a JSON or YAML task description file and place supporting documents in the working directory (`REQ-001`, `REQ-002`). The user expects Executor to drive one local task run, preserve permission boundaries, and produce auditable evidence for later agent or reviewer acceptance (`REQ-005`, `REQ-008`, `DONE-001`). No hosted user, remote API consumer, or multi-user workflow is in current scope.

## Goals and Outcomes
The product must provide a stable local CLI entry point, validate task-file inputs, call ClaudeTmuxAdapter CLI for Claude session operations, invoke the required openclaw progress-judgment skill when Claude is idle, and produce evidence-rich completion handoff (`REQ-001` through `REQ-010`). A successful outcome is a single local run that loads the task file, respects permissions, uses adapter evidence, records progress-skill decisions, runs mechanical checks, and emits final result plus logs (`AC-001` through `AC-010`, `VER-001`).

## Success Metrics
No separate `MET-*` KPI exists in the contract. MVP success is therefore measured by the blocking acceptance and verification objects: the CLI starts from a valid JSON/YAML task file, rejects invalid input, routes all Claude operations through ClaudeTmuxAdapter CLI 1.0.0, invokes the openclaw progress-judgment skill on idle screen evidence, sends returned next instructions through the adapter, runs mechanical delivery checks, and emits structured outputs (`AC-001` through `AC-010`, `VER-001`, `OUT-001`).

## Scope and Non-Goals
In scope: a local CLI such as `executor run <task-file>` (`REQ-004`); JSON/YAML task-description parsing (`REQ-002`, `IN-001`, `DCT-001`); ClaudeTmuxAdapter CLI integration for launch/status/capture/input/read operations (`REQ-003`, `REQ-006`, `TECH-001`, `MOD-002`); periodic monitoring and the required openclaw progress-judgment skill for idle Claude CLI screen evidence (`REQ-007`, `REQ-010`, `FLOW-001`, `MOD-003`, `TECH-002`); mechanical delivery checks (`REQ-008`); structured result and execution logs (`REQ-005`, `OUT-001`). Non-goals: direct tmux or Claude CLI control, semantic status interpretation inside the adapter, remote execution, concurrency, queueing, hosted APIs, or expanded schemas that have not been added to the requirement table (`BAR-001`, `STOP-001`).

## User Stories and Use Cases
As a CLI operator, I want to run Executor with a JSON or YAML task file so that I can start one Claude-backed task from local context (`REQ-001`, `REQ-004`). As an operator, I want reference documents listed in the task file and stored under the working directory so that the execution context is explicit and auditable (`REQ-002`, `DCT-001`). As a reviewer, I want structured result, adapter evidence, openclaw judgment records, and mechanical check output so that I can inspect whether handoff is justified (`REQ-005`, `REQ-008`, `OUT-001`, `DONE-001`).

## Functional Requirements
Executor must expose local CLI invocation (`REQ-004`). It must accept one JSON/YAML task-description file and validate working directory, task description, permissions, skill configuration, delivery standards, delivery method, and reference document list (`REQ-002`, `AC-002`, `IN-001`). It must call ClaudeTmuxAdapter CLI 1.0.0 for all Claude launch, status/capture observation, input sending, and screen/output reading (`REQ-003`, `AC-003`, `REQ-006`). Its control loop must periodically observe adapter state; on busy it continues polling, on idle it captures screen and calls the required openclaw progress-judgment skill, on blocked/exited/unknown it follows stop rules (`FLOW-001`, `EXE-001`, `STOP-001`). The skill contract must accept Claude CLI screen evidence plus task context and return `next_instruction`, `deliverable_ready`, `no_action`, or `blocked`; returned next instructions are sent through adapter CLI (`REQ-007`, `REQ-010`, `AC-007`, `AC-010`).

## Non-Functional Requirements and Guardrails
Executor must preserve permission boundaries from the task file (`REQ-002`, `STOP-001`). It must not bypass ClaudeTmuxAdapter CLI for Claude session operations (`TECH-001`). It must not ask ClaudeTmuxAdapter to make semantic judgments; subjective progress decisions belong to the dedicated openclaw progress-judgment skill (`REQ-010`, `TECH-002`, `SRC-003`, `SRC-006`). It must not claim completion from adapter state, process state, or screen text alone (`DONE-001`). It must stop on invalid task files, missing reference documents, unavailable commands, adapter failures, progress-skill failures, permission violations, mechanical check failure, or inconsistent stop/done evidence (`STOP-001`).

## User Flow or UX Notes
The user runs `executor run <task-file>`. Executor parses the JSON/YAML file, verifies referenced documents under the working directory, launches Claude through ClaudeTmuxAdapter CLI, sends the initial instruction, and enters the monitor loop. The monitor records state evidence, captures screen on idle, calls the openclaw progress-judgment skill, sends returned instructions, or moves to mechanical delivery checks when deliverable readiness is indicated. The final user-visible output is a structured result plus logs and evidence paths (`FLOW-001`, `DATA-001`, `REQ-010`, `OUT-001`).

## Acceptance Criteria
`AC-001`: A run starts from a provided task description. `AC-002`: JSON/YAML task files are accepted only when required fields and reference document list are valid. `AC-003`: Claude operations are routed through ClaudeTmuxAdapter CLI 1.0.0. `AC-004`: MVP exposes local CLI invocation. `AC-005`: Executor emits structured result plus logs and requires separate acceptance for semantic completion. `AC-006`: Adapter state/screen/input evidence is included. `AC-007`: Idle state triggers screen capture and openclaw progress judgment; returned next instruction is sent through the adapter. `AC-008`: Mechanical delivery checks pass before handoff. `AC-009`: Readable logs and final execution result exist. `AC-010`: The product includes an openclaw-callable progress-judgment skill with screen-evidence input and structured progress/next-instruction output (`AC-001` through `AC-010`).

## Release Plan and Roadmap
`PHASE-001` is the current release: one local sequential task run, JSON/YAML task input, ClaudeTmuxAdapter CLI integration, openclaw progress-judgment skill, mechanical delivery checks, and evidence output (`SCOPE-001`, `PHASE-001`, `REQ-010`). Later expansion to library/API entry points, remote execution, concurrency, durable queues, richer state persistence, or changes to the progress-skill responsibility boundary requires requirement-table revision (`BAR-001`, `ASM-002`).

## Risks, Assumptions, and Dependencies
`RISK-001`: openclaw CLI flags are not supplied as local source, but the progress-judgment skill is a required feature with an explicit screen-evidence input and structured decision output contract (`REQ-010`, `AC-010`, `SRC-006`). `ASM-001`: detailed JSON/YAML schema can be hardened in HLD if it preserves required fields. `ASM-002`: exact openclaw invocation details remain deferred unless supplied. Dependencies include ClaudeTmuxAdapter README and Agent PRD (`SRC-003`, `SRC-004`) plus user confirmation of version 1.0.0 (`SRC-005`).

## Open Questions
No blocking open questions remain for PRD rendering. The monitoring interval, exact JSON/YAML schema details, and exact openclaw CLI flags may be designed in HLD only within the confirmed boundaries. The existence and responsibility of the openclaw progress-judgment skill are confirmed and must not be downgraded to a generic agent judgment step (`REQ-010`, `AC-010`, `SRC-006`, `ASM-001`, `ASM-002`, `BAR-001`).

## Traceability
Core product refs: `CORE-001`, `SCOPE-001`, `PHASE-001`. Requirement refs: `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `REQ-005`, `REQ-006`, `REQ-007`, `REQ-008`, `REQ-009`, `REQ-010`. Acceptance refs: `AC-001`, `AC-002`, `AC-003`, `AC-004`, `AC-005`, `AC-006`, `AC-007`, `AC-008`, `AC-009`, `AC-010`. Execution and design refs: `IN-001`, `EXE-001`, `VER-001`, `OUT-001`, `STOP-001`, `DONE-001`, `FLOW-001`, `DATA-001`, `MOD-001`, `MOD-002`, `MOD-003`, `TECH-001`, `TECH-002`, `STATE-001`, `DCT-001`. Source refs: `SRC-001`, `SRC-002`, `SRC-003`, `SRC-004`, `SRC-005`, `SRC-006`.

## Source of Truth
`contract-envelope.json` is the sole source of truth. Human PRD and Agent PRD are sibling renders and cannot override the requirement table or canonical objects (`RB-001`, `RB-002`).

## Reader and Mission
Reader: downstream agent responsible for HLD or implementation design. Mission: consume this PRD without guessing, preserve the confirmed boundaries, and ask for a contract revision before adding new input modes, adapter calls, permissions, schemas, or completion rules (`BAR-001`, `STOP-001`).

## Requirement Trace
Implement and design only the current MVP refs: `REQ-001` through `REQ-010`, accepted by `AC-001` through `AC-010`, verified by `VER-001`, and executed through `IN-001`, `EXE-001`, `OUT-001`, `STOP-001`, and `DONE-001`.

## Input Contract
`IN-001` is a path to one JSON or YAML task description file. It must provide working directory, task description, permissions, skill configuration, delivery standards and method, and reference document list under the working directory. Missing fields, missing documents, or documents outside the working directory trigger `STOP-001`.

## Execution Contract
`EXE-001` requires validation, ClaudeTmuxAdapter CLI launch, periodic state observation, screen capture on idle, invocation of the required openclaw progress-judgment skill, adapter-mediated next-instruction sending, mechanical delivery checks, and final evidence output. The loop is represented by `FLOW-001`; evidence is represented by `DATA-001`; executor modules are `MOD-001`, `MOD-002`, and `MOD-003`; the skill requirement is `REQ-010`.

## Tool and Integration Boundaries
ClaudeTmuxAdapter must be called through CLI version 1.0.0 and is the only allowed boundary for Claude launch, capture/status observation, input sending, and screen/output reading (`REQ-003`, `TECH-001`, `SRC-005`). openclaw owns subjective progress judgment through the required progress-judgment skill only; it does not replace mechanical checks or reviewer acceptance (`REQ-007`, `REQ-010`, `AC-010`, `TECH-002`).

## Permissions and Safety
Permissions come from the task description file. Executor must reject actions outside the task permission boundary and must stop on destructive or external writes not authorized by the task (`REQ-002`, `STOP-001`). It must keep referenced documents under the working directory and preserve evidence for review (`DCT-001`, `OUT-001`).

## Data and State Contract
`DCT-001` represents the task file and run context. `DATA-001` covers adapter state/screen evidence, openclaw progress-judgment skill input/output records, next-instruction receipts, mechanical check results, final result, and logs. Runtime states include busy, idle, blocked, exited, and unknown as observed through adapter evidence (`STATE-001`, `FLOW-001`, `EXE-001`).

## Verification Contract
`VER-001` must cover valid JSON input, valid YAML input, invalid missing fields, invalid reference documents, adapter CLI routing, idle-state openclaw progress-judgment skill invocation, next-instruction sending, mechanical delivery checks, and permission-boundary failures. Verification must use real commands and files, not mock acceptance (`VER-001`, `AC-001` through `AC-010`).

## Output Contract
`OUT-001` requires final execution result, structured run summary, adapter state/screen evidence, openclaw progress-judgment skill input/output records, mechanical delivery-check report, and readable logs. Output must distinguish success, blocked, stopped, and failed states.

## Stop Conditions
`STOP-001` triggers on invalid task files, missing or out-of-workdir reference documents, unavailable ClaudeTmuxAdapter/openclaw commands, adapter state failure, unknown state without sufficient evidence, progress-judgment skill rejection/failure, permission-boundary violation, mechanical delivery-check failure, or unrecoverable command failure.

## Done Criteria
`DONE-001` requires one local run with acceptable adapter evidence, passing openclaw progress-judgment skill decision, passing mechanical delivery checks, emitted final result and evidence logs, and no permission-boundary violation. Semantic task acceptance remains separate from adapter state.

State transition ref: STATE-001 defines the monitored runtime states for busy, idle, blocked, exited, and unknown adapter observations.

## Forbidden Assumptions
Do not invent openclaw CLI flags beyond the confirmed boundary. Do not omit the required progress-judgment skill or replace it with generic inline executor logic. Do not add direct tmux/Claude CLI control. Do not add remote execution, queueing, concurrency, or hosted APIs. Do not treat ClaudeTmuxAdapter mechanical state as semantic task completion (`REQ-010`, `RISK-001`, `ASM-002`, `BAR-001`).
