# Executor Agent PRD

Source contract: `contract-envelope.json`

render_status.agent_prd=execution_ready

## Document Metadata

- Product: Executor (`CORE-001`)
- Contract: `contract-envelope.json`
- Contract version: `1.8`
- Intake: `INTAKE-EXECUTOR-MINIMAL-001`
- Current phase: `PHASE-001`
- Status: `execution_ready`
- Primary sources: `SRC-001`, `SRC-002`, `SRC-003`, `SRC-004`, `SRC-005`, `SRC-006`

## Executive Summary

Build the Executor MVP: a local CLI program that accepts a task description, reads work environment, permission, and skill configuration context, and drives Claude CLI through the already formed `ClaudeTmuxAdapter`. The MVP entry point is local CLI only, for example `executor run <task-file>`.

During execution, Executor must use documented `ClaudeTmuxAdapter` capabilities to launch Claude CLI, retain the `ClaudeTmuxTarget`, call `detect_state`, call `capture_screen`, call `send_input`, optionally call `read_output`, and preserve adapter outputs as execution evidence (`REQ-006`, `AC-006`, `SRC-005`, `SRC-006`). When periodic monitoring finds Claude CLI idle, Executor must capture the current screen and invoke a dedicated progress-judgment skill through `opencalw`; the skill returns `next_instruction`, `deliverable_ready`, `no_action`, or `blocked` (`REQ-007`, `AC-007`, `SRC-004`). If `deliverable_ready` is returned, Executor must run a mechanical delivery check before handoff (`REQ-008`, `AC-008`). Semantic task completion remains reserved for a separate agent or reviewer (`REQ-005`, `DONE-001`).

## Problem and Background

Users need a command-driven executor that can translate a structured task description into Claude CLI execution (`CORE-001`, `REQ-001`). The executor should reuse the existing `ClaudeTmuxAdapter` instead of rebuilding Claude session control (`CORE-001`, `REQ-003`, `TECH-001`). A one-time adapter call is not enough: Executor must observe the Claude run through adapter state and screen content, delegate subjective progress judgment to a separate skill, and perform mechanical delivery checks before handoff (`REQ-006`, `REQ-007`, `REQ-008`, `SRC-004`). `ClaudeTmuxAdapter` documentation explicitly keeps state observation mechanical and separate from task completion judgment (`SRC-005`).

## Target Users and Personas

The contract does not define named user personas. The supported user for this MVP is the operator who provides a local task file and expects Executor to drive Claude CLI execution from that file (`REQ-001`, `REQ-004`). Do not invent additional personas, hosted users, or API consumers.

## Goals and Outcomes

- Provide a stable local CLI boundary for starting executor runs (`REQ-004`, `SRC-002`).
- Preserve task context by passing work environment, permissions, and skill configuration into the execution flow (`REQ-002`, `IN-001`, `DCT-001`).
- Route Claude CLI execution control through `ClaudeTmuxAdapter` (`REQ-003`, `TECH-001`, `MOD-002`).
- Monitor Claude CLI through adapter `detect_state` and `capture_screen`, preserving observations as execution evidence in the orchestration flow (`REQ-006`, `AC-006`, `EXE-001`, `FLOW-001`).
- Use a dedicated `opencalw` progress-judgment skill when adapter state is idle (`REQ-007`, `MOD-003`, `TECH-002`).
- Run mechanical delivery checks before handoff (`REQ-008`, `AC-008`, `DONE-001`).
- Produce structured JSON and execution logs for review (`REQ-005`, `OUT-001`).
- Prevent fabricated completion by requiring separate agent or reviewer acceptance (`REQ-005`, `DONE-001`).

## Success Metrics

No separate `MET-*` KPI object exists in the Stage 1 contract. For this MVP, success is measured by `AC-001` through `AC-008` and `VER-001`:

- a run starts from a provided task description
- required task context is represented in the executor input contract
- Claude CLI invocation is routed through `ClaudeTmuxAdapter`
- adapter launch/target capture, `detect_state`, `capture_screen`, `send_input`, monitoring, and evidence preservation are present
- idle-state progress judgment is routed through the `opencalw` skill and any next instruction is sent through adapter `send_input`
- delivery handoff is blocked until mechanical checks pass
- the CLI boundary is local-only
- output includes structured JSON and execution log
- completion is accepted by a separate agent or reviewer

## Scope and Non-Goals

In scope for `PHASE-001`:

- local CLI invocation such as `executor run <task-file>` (`REQ-004`)
- loading a task description (`REQ-001`, `IN-001`)
- extracting work environment, permissions, and skill configuration (`REQ-002`, `DCT-001`)
- executor orchestration that coordinates task parsing, adapter execution, progress judgment, delivery checks, and reviewer handoff (`MOD-001`, `FLOW-001`)
- using documented `ClaudeTmuxAdapter` capabilities: launch or command-equivalent launch path, `detect_state`, `capture_screen`, `send_input`, and `read_output` when needed (`REQ-006`, `TECH-001`, `SRC-005`, `SRC-006`)
- periodic monitoring that continues while adapter state is `busy`, captures screen on `idle`, and treats `blocked`, `exited`, or `unknown` through stop or recovery rules (`REQ-006`, `STOP-001`)
- `opencalw` progress-judgment skill creation and invocation for idle-state subjective assessment (`REQ-007`, `MOD-003`, `TECH-002`)
- mechanical delivery check after `deliverable_ready` and before reviewer handoff (`REQ-008`, `AC-008`)
- collecting execution evidence including adapter state observations, screen-content observations, progress skill input/output, sent instructions, and delivery-check results (`DATA-001`, `OUT-001`)
- emitting structured JSON result plus execution log (`REQ-005`, `OUT-001`)
- handing semantic completion judgment to a separate agent or reviewer (`REQ-005`, `DONE-001`)

Non-goals for the MVP:

- library/API entry point
- direct Claude process control outside `ClaudeTmuxAdapter`
- embedding semantic progress judgment inside `ClaudeTmuxAdapter`
- handing off a deliverable without mechanical delivery checks
- remote or hosted execution
- extra external services or schedulers
- detailed JSON field schema beyond the structured JSON result requirement
- durable state model beyond run evidence and logs

## User Stories and Use Cases

- As an operator, I want to run `executor run <task-file>` so that I can start a Claude-backed task from a local task description (`REQ-001`, `REQ-004`).
- As an operator, I want the task file to carry work environment, permission, and skill configuration context so that Claude execution follows the intended constraints (`REQ-002`, `IN-001`).
- As an operator, I want Executor to use `ClaudeTmuxAdapter` so that session control is delegated to the existing adapter boundary (`REQ-003`).
- As an operator, I want Executor to monitor Claude through adapter state and screen content so that a running task is observable instead of opaque (`REQ-006`, `AC-006`).
- As an operator, I want idle-state screens to be judged by a configured skill so Executor can either send a next instruction or prepare delivery (`REQ-007`, `MOD-003`).
- As a reviewer, I want structured JSON, logs, adapter evidence, progress-skill decisions, and delivery-check results so that I can inspect the run and validate completion (`REQ-005`, `REQ-008`, `OUT-001`, `VER-001`).

## Functional Requirements

- Executor must expose a local CLI entry point for the MVP (`REQ-004`, `AC-004`).
- Executor must accept a task description containing work environment, permissions, skill configuration, adapter launch/config context, and progress-judgment skill configuration (`REQ-002`, `AC-002`, `IN-001`).
- Executor must call Claude CLI through `ClaudeTmuxAdapter` (`REQ-003`, `AC-003`, `TECH-001`).
- Executor must use documented `ClaudeTmuxAdapter` methods or command-equivalent capabilities for launch, `detect_state`, `capture_screen`, `send_input`, and `read_output` when needed (`REQ-006`, `AC-006`, `TECH-001`).
- Executor orchestration module `MOD-001` must own the control flow in `FLOW-001`: periodically call adapter `detect_state`; when state is `busy`, continue monitoring; when state is `idle`, capture the current screen and invoke the `opencalw` progress-judgment skill (`REQ-007`, `AC-007`, `MOD-001`, `FLOW-001`).
- Executor must send any returned `next_instruction` through `ClaudeTmuxAdapter.send_input`; if the skill returns `deliverable_ready`, Executor must run mechanical delivery checks before handoff (`REQ-007`, `REQ-008`, `AC-008`).
- Executor must collect execution evidence during the run, including adapter monitoring observations, skill decisions, sent next instructions, and delivery-check results (`DATA-001`, `OUT-001`).
- Executor must emit a structured JSON result plus execution log (`REQ-005`, `AC-005`, `OUT-001`).
- Executor must use separate agent or reviewer acceptance for semantic completion (`REQ-005`, `DONE-001`).

## Non-Functional Requirements and Guardrails

- Permission guardrail: Executor must honor only the permissions supplied in the task description (`REQ-002`, `IN-001`).
- Integration guardrail: Executor must not bypass `ClaudeTmuxAdapter` for Claude CLI invocation, control, state detection, screen capture, input sending, or output reading (`REQ-003`, `REQ-006`, `TECH-001`).
- Judgment guardrail: `ClaudeTmuxAdapter` state detection remains mechanical; subjective progress judgment belongs only to the `opencalw` skill (`REQ-007`, `TECH-002`, `SRC-005`).
- Honesty guardrail: Executor must not claim completion from process state, screen state, adapter state, or the progress skill alone (`EXE-001`, `DONE-001`).
- Failure guardrail: Executor must stop when the task file is unavailable, task context is invalid, adapter launch/control/observation fails, state is `unknown` without sufficient evidence, screen content cannot be captured, `opencalw` skill invocation fails, required next instruction cannot be sent, mechanical delivery check fails, or reviewer acceptance fails (`STOP-001`).
- Scope guardrail: New invocation modes, APIs, schemas, state stores, adapter methods, judgment skills, or delivery-check criteria require a requirement-table update before inclusion (`BAR-001`).

## User Flow or UX Notes

The MVP flow is:

1. Operator runs the local CLI with a task file (`REQ-004`).
2. Executor loads the task description (`REQ-001`).
3. Executor extracts work environment, permissions, skill configuration, adapter config, and progress-judgment skill config (`REQ-002`, `IN-001`, `DCT-001`).
4. Executor launches Claude CLI through `ClaudeTmuxAdapter` and records the returned `ClaudeTmuxTarget` or equivalent session target (`REQ-006`, `SRC-006`).
5. Executor sends the initial task instruction through adapter `send_input` and stores the `InputReceipt` (`REQ-006`, `SRC-005`).
6. Executor periodically calls `detect_state` and stores each `ClaudeTmuxState` (`REQ-006`, `AC-006`).
7. If state is `busy`, Executor waits and continues polling (`EXE-001`).
8. If state is `blocked`, `exited`, or `unknown`, Executor follows `STOP-001` or a traced recovery path (`STOP-001`).
9. If state is `idle`, Executor calls `capture_screen`, sends the screen data and execution context to the `opencalw` progress-judgment skill, and stores the skill input/output (`REQ-007`, `MOD-003`).
10. If the skill returns `next_instruction`, Executor sends it through adapter `send_input` and resumes monitoring (`AC-007`).
11. If the skill returns `deliverable_ready`, Executor runs mechanical delivery checks (`REQ-008`, `AC-008`).
12. Executor emits structured JSON plus logs containing adapter evidence, progress-skill decisions, sent instructions, and delivery-check results (`OUT-001`).
13. A separate agent or reviewer validates semantic completion against task expectations and execution evidence (`DONE-001`, `VER-001`).

No UI, wireframe, or hosted UX is defined in this contract.

## Acceptance Criteria

- `AC-001`: The executor can start a run from a provided task description after the invocation boundary is confirmed.
- `AC-002`: The task definition exposes work environment, permissions, and skill configuration to the executor.
- `AC-003`: Claude CLI invocation is routed through `ClaudeTmuxAdapter` instead of direct Claude process control.
- `AC-004`: The MVP executor exposes a local CLI boundary such as `executor run <task-file>`.
- `AC-005`: The executor emits a structured JSON result plus execution log, and completion is accepted by a separate agent or reviewer.
- `AC-006`: During a run, executor uses documented `ClaudeTmuxAdapter` methods or command-equivalent capabilities to launch Claude CLI, detect state, capture screen content, send instructions, continue monitoring until stop or completion handoff, and include adapter outputs in execution evidence.
- `AC-007`: When a periodic adapter status check returns idle, executor captures the current screen, calls the `opencalw` progress-judgment skill with screen data and context, and sends any returned next instruction through `ClaudeTmuxAdapter.send_input`; if the skill returns `deliverable_ready`, executor moves to mechanical delivery check instead of sending more input.
- `AC-008`: Before handoff, executor performs a mechanical delivery check covering structured JSON result, execution log, adapter screen/state/input evidence, progress-judgment decision evidence, and stop/done consistency; semantic completion remains reserved for the separate agent or reviewer.

## Release Plan and Roadmap

`PHASE-001` is the current MVP release. It contains the local CLI boundary, task-description input, `ClaudeTmuxAdapter` execution and monitoring integration, idle-state `opencalw` progress judgment, mechanical delivery checks, structured JSON/log output with evidence, and separate review acceptance. Future capabilities such as library/API entry points, detailed output schema, persistent state beyond run evidence, remote execution, or broader permission models are not part of this phase and require requirement-table revision.

## Risks, Assumptions, and Dependencies

- `RISK-001`: Executor readiness could be overclaimed if CLI shape, delivery output, completion authority, adapter behavior, progress judgment, or delivery checks are invented.
- `ASM-001`: `ClaudeTmuxAdapter` is assumed to be available and already formed, as stated by the user; it is deferred and non-blocking.
- Dependency: Claude CLI invocation, control, state detection, screen capture, input sending, output reading when needed, and monitoring depend on `ClaudeTmuxAdapter` (`REQ-006`, `TECH-001`, `MOD-002`, `SRC-005`, `SRC-006`).
- Dependency: subjective progress judgment depends on a new progress-judgment skill invoked through `opencalw` (`REQ-007`, `MOD-003`, `TECH-002`).
- Dependency: completion depends on a separate agent or reviewer acceptance step (`DONE-001`).

## Open Questions

No blocking open questions remain. `Q-001`, `Q-002`, and `Q-003` were resolved by `SRC-002`. The exact monitoring interval and exact structured JSON fields are intentionally left for HLD or implementation configuration as long as they satisfy `REQ-006` through `REQ-008` and do not change product behavior.

## Traceability

- `SRC-001` states the original executor idea.
- `SRC-002` confirms local CLI only, structured JSON plus execution log, and separate agent/reviewer completion authority.
- `SRC-003` confirms the review requirement for adapter-based execution and monitoring.
- `SRC-004` confirms detailed monitoring-loop requirements: adapter methods, periodic status checks, idle screen capture, `opencalw` judgment skill, next-instruction execution, and mechanical delivery checks.
- `SRC-005` records the local `ClaudeTmuxAdapter` README interface contract.
- `SRC-006` records the local `ClaudeTmuxAdapter` Agent PRD command contract.
- `TRACE-001`, `TRACE-002`, and `TRACE-003` connect explicit source facts to `REQ-001`, `REQ-002`, and `REQ-003`.
- `TRACE-004` and `TRACE-005` record bounded inference for the invocation and delivery/completion requirements.
- `TRACE-006` connects `SRC-003` to `REQ-006`.
- `TRACE-007` connects `SRC-004` to `REQ-007`.
- `TRACE-008` connects `SRC-004` to `REQ-008`.
- `RB-001` renders the Human PRD brief; `RB-002` renders this Agent PRD.

## Source of Truth

Use only `contract-envelope.json` as the authoritative source for this PRD. Current execution scope is `PHASE-001`. Requirement table rows `RT-001` through `RT-008` are mandatory source rows for product intent, scope, acceptance, execution boundaries, adapter monitoring, progress judgment, and delivery checks.

## Reader and Mission

Reader: a downstream design or implementation agent.

Mission: build the Executor MVP defined by `REQ-001` through `REQ-008` without inventing invocation modes, output formats, completion authority, permissions, adapter behavior, progress judgment, or delivery checks outside the contract.

## Requirement Trace

- `REQ-001`: Create the executor that runs work from an input task description. Acceptance: `AC-001`; verification: `VER-001`.
- `REQ-002`: Parse task definition context containing work environment, permissions, and skill configuration. Acceptance: `AC-002`; verification: `VER-001`.
- `REQ-003`: Use `ClaudeTmuxAdapter` to call Claude CLI. Acceptance: `AC-003`; verification: `VER-001`.
- `REQ-004`: Expose a local CLI boundary such as `executor run <task-file>`. Acceptance: `AC-004`; confirmation source: `SRC-002`.
- `REQ-005`: Produce structured JSON plus execution log, with completion accepted by a separate agent or reviewer. Acceptance: `AC-005`; confirmation source: `SRC-002`.
- `REQ-006`: Execute and monitor through documented `ClaudeTmuxAdapter` capabilities, including launch/target capture, `detect_state`, `capture_screen`, `send_input`, optional `read_output`, and evidence preservation. Acceptance: `AC-006`; sources: `SRC-003`, `SRC-004`, `SRC-005`, `SRC-006`; verification: `VER-001`.
- `REQ-007`: Create and invoke an idle-state progress-judgment skill through `opencalw`. Acceptance: `AC-007`; source: `SRC-004`; verification: `VER-001`.
- `REQ-008`: Run mechanical delivery checks before handoff. Acceptance: `AC-008`; source: `SRC-004`; verification: `VER-001`.

## Input Contract

Use `IN-001` and `DCT-001`. The input is a task description that contains work environment, permissions, skill configuration, adapter launch/config context, and progress-judgment skill configuration sufficient for `opencalw` invocation. The MVP entry point is local CLI only, represented by `REQ-004` and confirmed in `SRC-002`.

## Execution Contract

Use `EXE-001` and the orchestration flow in `FLOW-001`. `MOD-001` owns the executor orchestration; adapter operations remain under `MOD-002`; subjective progress judgment remains under `MOD-003`.

1. Run one local CLI invocation.
2. Load the task file.
3. Pass task context to Claude through `ClaudeTmuxAdapter`.
4. Launch Claude CLI through the adapter launch capability or command-equivalent launch path described by `SRC-006`, then retain `ClaudeTmuxTarget`.
5. Send the initial task instruction through `send_input` and preserve `InputReceipt`.
6. Periodically call `detect_state` and preserve `ClaudeTmuxState`.
7. If state is `busy`, continue periodic monitoring.
8. If state is `idle`, call `capture_screen`, pass `ScreenSnapshot.text` plus execution context to the `opencalw` progress-judgment skill, and preserve the skill result.
9. If the skill returns `next_instruction`, send it through `send_input` and continue monitoring.
10. If the skill returns `deliverable_ready`, run the mechanical delivery check.
11. Collect execution evidence, including adapter observations, skill decisions, sent instructions, and delivery-check results.
12. Hand the checked result to a separate agent or reviewer for acceptance.

The executor must not declare task success solely from process state, screen state, adapter state, the progress skill, or mechanical checks.

## Tool and Integration Boundaries

Use `TECH-001` and `MOD-002`: Claude CLI invocation, execution control, instruction sending, state detection, screen capture, output reading when needed, and monitoring must be routed through `ClaudeTmuxAdapter`. Use `TECH-002` and `MOD-003`: subjective progress judgment must be implemented as a dedicated `opencalw` skill. The contract does not authorize direct Claude process control, semantic judgment inside `ClaudeTmuxAdapter`, extra external services, background schedulers, remote APIs, or non-local invocation modes.

## Adapter Method Contract

Executor must align with the local `ClaudeTmuxAdapter` documentation in `SRC-005` and `SRC-006`:

| Executor need | Adapter capability | Required evidence |
| --- | --- | --- |
| Start Claude CLI | adapter launch capability or command-equivalent launch path | `ClaudeTmuxTarget` or session id plus launch metadata |
| Check Claude state | `detect_state(ClaudeTmuxTarget, DetectionPolicy)` | `ClaudeTmuxState.status`, confidence, signals, reason, observed time |
| Capture idle screen | `capture_screen(ClaudeTmuxTarget, lines?)` | `ScreenSnapshot.text`, content hash, evidence path |
| Send task or next instruction | `send_input(ClaudeTmuxTarget, content, submit)` | `InputReceipt` and post-send confirmation evidence |
| Read recent output when needed | `read_output(ClaudeTmuxTarget, ReadWindow)` | `OutputWindow` and evidence path |

Allowed adapter states are `busy`, `idle`, `blocked`, `exited`, and `unknown` as documented in `SRC-005`. Adapter state is mechanical evidence only; it never proves task completion.

## Progress Judgment Skill Contract

Create a dedicated skill invoked through `opencalw` from the executor monitoring loop (`REQ-007`, `MOD-003`, `TECH-002`). The skill input must include the latest `ScreenSnapshot.text`, relevant adapter state, task description context, prior progress decisions, and delivery criteria available from the task description. The skill output must be one of:

| Output | Meaning | Executor action |
| --- | --- | --- |
| `next_instruction` | Claude should continue with a concrete instruction | send via `ClaudeTmuxAdapter.send_input` and keep monitoring |
| `deliverable_ready` | Claude appears finished enough for delivery preparation | run mechanical delivery check |
| `no_action` | no safe next instruction is available yet | continue monitoring or stop according to policy |
| `blocked` | progress cannot be judged safely | stop or escalate under `STOP-001` |

The skill may perform subjective judgment; the adapter may not.

## Permissions and Safety

Executor must honor the permissions supplied in the task description and must not grant permissions beyond them. If required permission context is missing, treat the task context as invalid and stop under `STOP-001`.

## Data and State Contract

Use `DATA-001` and `DCT-001`. Task definition data includes work environment, permissions, skill configuration, adapter launch/config context, and progress-judgment skill configuration. Execution evidence includes `ClaudeTmuxTarget`, `ScreenSnapshot`, `ClaudeTmuxState`, `InputReceipt`, progress-judgment skill input/output, mechanical delivery-check result, structured JSON result, and execution log. No additional persistent state requirement is specified in the contract.

## Verification Contract

Use `VER-001` and acceptance criteria `AC-001` through `AC-008`. Verification must fail if any required behavior depends on an untraced assumption. In particular, verification must show adapter launch/target capture, `detect_state` polling, busy wait behavior, idle `capture_screen`, `opencalw` progress-judgment skill invocation, `next_instruction` `send_input`, `deliverable_ready` transition, mechanical delivery check, output emission, and reviewer acceptance.

## Output Contract

Use `OUT-001`. The MVP output is a structured JSON result plus execution log. The execution log must include adapter monitoring observations, progress-judgment skill decisions, sent next instructions, and mechanical delivery-check evidence sufficient for reviewer inspection. The contract does not define exact JSON fields.

## Stop Conditions

Use `STOP-001`. Stop when task file input is unavailable, task context is invalid, `ClaudeTmuxAdapter` cannot launch, address, control, or observe Claude CLI, `detect_state` is `unknown` without sufficient evidence, screen content cannot be captured, monitoring evidence is stale or unavailable, `opencalw` progress-judgment skill invocation fails, a required next instruction cannot be sent, mechanical delivery check fails, or separate agent/reviewer acceptance fails.

## Done Criteria

Use `DONE-001`. Done means the executor has completed the local CLI run, captured adapter state and screen-content evidence, recorded progress-judgment skill decisions, passed mechanical delivery checks, emitted structured JSON and logs, and received completion acceptance from a separate agent or reviewer.

## Forbidden Assumptions

Do not assume a library/API entry point, direct Claude CLI process control, hosted execution, extra external integrations, a detailed JSON schema, persistent state, self-certified task completion, adapter capabilities beyond those documented in `SRC-005`/`SRC-006`, semantic status inference inside `ClaudeTmuxAdapter`, or delivery readiness without the `opencalw` progress-judgment skill and mechanical delivery checks. Do not treat `ClaudeTmuxAdapter` availability as proven beyond the deferred non-blocking assumption in `ASM-001`.
