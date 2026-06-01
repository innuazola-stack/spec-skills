# Claude Tmux CLI Adapter Agent PRD

Status: `execution_ready`

Source contract: `REF-001` (`contract-envelope.json`)

## Revision History

| Version | Date | Author | Change | Basis |
| --- | --- | --- | --- | --- |
| v1.0 | 2026-05-26 | Codex | Created the execution PRD from the canonical contract. | `SRC-001`; `META-001` |
| v1.1 | 2026-05-26 | Codex | Expanded the PRD to the reference minimum shape with visible contracts, acceptance, data, state, outputs, open assumptions, stops, and done criteria. | `RB-003`; `RB-004` |
| v1.2 | 2026-05-26 | Codex | Restored contract-backed references, fixed State Transition Contract shape, and rendered enriched ASM/TECH/DCT/VER/STOP/DONE payloads. | `REF-001`; `ASM-001`; `DCT-003`; `VER-006` |

## 1. Execution Objective

Implement `PHASE-001`: a Rust CLI adapter that controls Claude CLI inside tmux through mechanical launch, capture, status detection, input, and termination commands.

| Field | Value |
| --- | --- |
| Capability name | Claude Tmux CLI Adapter (`CORE-001`) |
| Execution phase | `PHASE-001` Phase 1 mechanical tmux adapter MVP |
| Current scope | `SCOPE-001` local Rust CLI commands for launch, capture, status, input, and exit/kill |
| Required outputs | `OUT-001`, `OUT-002`, `OUT-003`, `OUT-004`, `OUT-005` |
| Non-expansion rule | Do not implement semantic Claude-message understanding, remote orchestration, multi-host tmux management, or non-tmux terminal backends because `OOS-001` excludes them. |

## 2. Source of Truth

| ID | Source | Authority | Purpose | Conflict Handling |
| --- | --- | --- | --- | --- |
| `REF-001` | `contract-envelope.json` | Primary canonical contract | Authoritative source for goals, requirements, inputs, outputs, stops, verification, modules, and task planning refs. | If any PRD, task, or implementation request conflicts with `REF-001`, stop and require a contract update. |
| `SRC-001` | Original user idea | Source fact | Provides the Rust CLI, Claude CLI, tmux, five mechanical operations, 1-second confirmation, and 99%/99% accuracy requirements. | Do not infer unstated product behavior beyond contract objects derived from this source. |
| `REF-002` | `human-prd.md` | Derived artifact | Human-facing PRD for product review. | Do not use it to override `REF-001`. |
| `REF-004` | `execution-task-plan.json` | Derived artifact | Task decomposition generated from this Agent PRD and `REF-001`. | If task refs drift from `REF-001`, regenerate or patch the plan. |

## 3. Input Contract

| ID | Input | Required | Constraints | Entry Blocker |
| --- | --- | --- | --- | --- |
| `IN-001` | launch_config | Yes | Must include workspace/config values, permission settings, `CLAUDE.md` content or path, and task prompt. | `STOP-001` |
| `IN-002` | tmux_session_id | Yes | Must address an existing tmux session for capture, status, input, or termination. | `STOP-002`; `STOP-004` |
| `IN-003` | structured_screen_history | Yes | Must contain current and historical structured captures for the same session. | `STOP-002`; `STOP-003` |
| `IN-004` | instruction_text | Yes | Must be sent to Claude CLI and followed by Enter. | `STOP-004` |
| `IN-005` | termination_mode | Yes | Must select graceful `/exit` or force kill. | `STOP-005` |

Permission and environment handling must follow `EXE-001` and `ASM-002`. Missing tmux or Claude CLI must stop launch according to `STOP-001`.

## 4. Scope Contract

### 4.1 In Scope

| ID | Phase | Scope | Required Behavior |
| --- | --- | --- | --- |
| `SCOPE-001` | `PHASE-001` | Phase 1 implements local Rust CLI commands for configuring and launching Claude CLI in tmux, capturing and parsing screens, detecting idle or busy state from structured diffs, sending input, and exiting or killing a session. | Implement launch, capture, status, input, and termination commands with structured JSON results. |

### 4.2 Out Of Scope

| ID | Phase | Out-of-scope Item | Required Handling |
| --- | --- | --- | --- |
| `OOS-001` | `PHASE-001` | Phase 1 does not implement semantic understanding of Claude messages, remote orchestration, multi-host tmux management, or non-tmux terminal backends. | Reject, defer, or require a contract update before implementation. |

## 5. Execution Contract

| ID | Required Behavior | Sequencing / Boundary | Related Output |
| --- | --- | --- | --- |
| `EXE-001` | Launch must write or select CLAUDE.md, apply config and permission settings, start Claude CLI in tmux, and return the tmux session id. | First operation in `FLOW-001`; moves state from unknown to launched. | `OUT-001` |
| `EXE-002` | Screen capture must use mechanical tmux output and deterministic parsing into messages, input, and status fields. | Requires `IN-002`; produces observed screen state. | `OUT-002` |
| `EXE-003` | Status detection must compare current and historical structured screens and classify idle or busy only by explicit diff rules. | Requires `IN-003`; must obey `STOP-003`. | `OUT-003` |
| `EXE-004` | Input must send instruction text to the tmux session, trigger execution, wait one second, and capture confirmation evidence. | Requires addressable session and capture path. | `OUT-004` |
| `EXE-005` | Termination must support graceful /exit and force tmux kill paths. | Ends session lifecycle as exiting, killed, or terminated. | `OUT-005` |

Forbidden behavior:

| Control | Rule |
| --- | --- |
| `BAR-001` | Do not classify status by LLM judgment or semantic guessing. |
| `BAR-003` | Do not return unstructured logs as the only command output. |
| `OOS-001` | Do not add non-tmux backends or remote orchestration in Phase 1. |

## 6. Implementation Constraints

| ID | Area | Technical Decision | Affected Modules | Agent Constraint |
| --- | --- | --- | --- | --- |
| `TECH-001` | CLI runtime | Implement the wrapper as a Rust CLI application. | `MOD-001`, `MOD-002` | Keep command behavior deterministic and testable through Rust unit and integration tests. |
| `TECH-002` | Session boundary | Use tmux as the session boundary and interact through tmux commands. | `MOD-003`, `MOD-006`, `MOD-007` | Use tmux commands as the only terminal session boundary in Phase 1. |
| `TECH-003` | Parsing and status | Keep capture parsing and status classification mechanical and deterministic; do not use LLM judgment. | `MOD-004`, `MOD-005` | Use explicit parser and diff rule hits; never call an LLM or infer Claude intent for status. |

| ID | Module | Responsibility |
| --- | --- | --- |
| `MOD-001` | cli_command_router | Expose launch, capture, status, input, and exit commands. |
| `MOD-002` | environment_builder | Materialize config values, permission settings, CLAUDE.md, and task prompt files. |
| `MOD-003` | tmux_controller | Create, address, send keys to, capture, and kill tmux sessions. |
| `MOD-004` | screen_parser | Parse raw tmux screen text into structured messages, input, and parser status using mechanical rules. |
| `MOD-005` | status_detector | Compute structured diffs and classify idle or busy by deterministic rules. |
| `MOD-006` | input_sender | Send instruction text and Enter, then capture confirmation after one second. |
| `MOD-007` | termination_controller | Send /exit or force kill a tmux session and report final state. |

## 7. Requirements And Acceptance Criteria

| ID | Phase | Requirement | Acceptance Criteria IDs | Agent Acceptance Criteria | Verification Link |
| --- | --- | --- | --- | --- | --- |
| `REQ-001` | `PHASE-001` | Launch Claude CLI in a configured tmux session | `AC-001` | Given config, CLAUDE.md content, task prompt, and permission settings, the launch command creates a tmux session running Claude CLI and returns a non-empty session id plus launch metadata. | `VER-001` |
| `REQ-002` | `PHASE-001` | Capture and mechanically structure the current tmux screen | `AC-002` | Given a valid session id, the capture command returns raw screen text, parsed messages, parsed input area, parser status, and capture timestamp without semantic interpretation. | `VER-002` |
| `REQ-003` | `PHASE-001` | Detect idle or busy state by structured screen diff | `AC-003` | Given current and historical structured captures, the status command returns idle or busy plus structured diff details, with idle accuracy >= 99% and busy accuracy >= 99% on the labeled corpus. | `VER-003`, `VER-006` |
| `REQ-004` | `PHASE-001` | Send command input to a Claude CLI tmux session and confirm delivery | `AC-004` | Given a valid session id and instruction, the input command sends the instruction, presses Enter, waits one second, captures the screen, and returns confirmation evidence or a structured failure. | `VER-004` |
| `REQ-005` | `PHASE-001` | Exit or kill a Claude CLI tmux session | `AC-005` | Given a valid session id, the exit command sends /exit when graceful mode is requested or kills the tmux session when force mode is requested, and reports whether the session still exists. | `VER-005` |

## 8. State Transition Contract

Data and State are intentionally separated: this section defines lifecycle transitions, while `## 9. Data Contract` defines the schemas used by those transitions. State model: `STATE-001`.

| State | Event | Transition Rule | Output Eligibility | Negative Rule |
| --- | --- | --- | --- | --- |
| `unknown` | launch requested | Validate `IN-001`; if valid, create tmux session. | Can produce `OUT-001`. | Do not continue if `STOP-001` is triggered. |
| `launched` | capture requested | Capture tmux screen and parse into `DCT-002`. | Can produce `OUT-002`. | Do not return only raw screen text. |
| `observed` | status requested | Compare current and historical structured captures. | Can produce `OUT-003`. | Do not classify by semantic guessing; use `STOP-003`. |
| `idle` | input requested | Send `IN-004`, press Enter, wait one second, capture confirmation. | Can produce `OUT-004`. | Do not claim success without capture evidence. |
| `busy` | input requested | Caller should wait or continue observing. | No input output unless command explicitly proceeds. | Do not hide busy classification. |
| `input_sent` | confirmation capture complete | Return structured confirmation or failure. | Can produce `OUT-004`. | Do not omit evidence. |
| `exiting` / `killed` | termination requested | Send `/exit` or force kill according to `IN-005`. | Can produce `OUT-005`. | Do not force kill after graceful failure unless requested. |
| `terminated` | final existence check complete | Report final session existence state. | Completion state for `REQ-005`. | Do not claim terminated without checking session state. |

## 9. Data Contract

### 9.1 Schemas

| ID | Schema | Required Fields | Constraints | Produced By |
| --- | --- | --- | --- | --- |
| `DCT-001` | LaunchSessionResponse | `session_id`, `workspace`, `claude_md_path`, `permission_profile`, `started_at`, `status` | Do not return success without a non-empty session_id.<br>Include structured error information through DCT-004 on failure. | `OUT-001` |
| `DCT-002` | StructuredScreen | `session_id`, `captured_at`, `raw_screen`, `messages`, `input`, `status` | Keep raw_screen as evidence.<br>Record parser status when screen shape is unsupported. | `OUT-002` |
| `DCT-003` | StatusDiff | `session_id`, `state`, `current_capture`, `previous_capture_ref`, `diff`, `rule_hits`, `confidence_source` | Return unknown/failure under STOP-003 when rule hits are insufficient.<br>Expose diff details in OUT-003. | `OUT-003` |
| `DCT-004` | CommandResult | `session_id`, `operation`, `success`, `evidence`, `error` | Every command must distinguish success from failure.<br>Do not return raw logs as the only output. | `OUT-004`, `OUT-005` |

### 9.2 Data Sources And Outputs

| ID | Data Source | Transformation | Output |
| --- | --- | --- | --- |
| `DATA-001` | Session-scoped current and historical structured captures used for mechanical diff and status classification. | Mechanical screen parsing and structured diff. | `OUT-002`; `OUT-003` |

## 10. Verification Contract

| ID | Type | Related Requirement | Related AC | Expected Result | Blocking |
| --- | --- | --- | --- | --- | --- |
| `VER-001` | positive | `REQ-001` | `AC-001` | tmux session running Claude CLI exists and OUT-001 contains required launch metadata. | Yes |
| `VER-002` | fixture | `REQ-002` | `AC-002` | Raw tmux fixtures convert to DCT-002 without semantic inference. | Yes |
| `VER-003` | behavior | `REQ-003` | `AC-003` | Status detector returns idle/busy/unknown with DCT-003 diff and rule hits. | Yes |
| `VER-004` | integration | `REQ-004` | `AC-004` | Input sends text, triggers execution, waits one second, and returns confirmation evidence. | Yes |
| `VER-005` | integration | `REQ-005` | `AC-005` | Graceful /exit and force kill report operation mode and final session existence. | Yes |
| `VER-006` | accuracy_gate | `REQ-003` | `AC-003` | Idle accuracy >= 99% and busy accuracy >= 99% on the labeled status corpus. | Yes |

Consistency checks:

| Check | Related Controls | Pass Criteria |
| --- | --- | --- |
| Mechanical-only status | `BAR-001`; `EXE-003`; `STOP-003` | No status classifier path uses LLM or semantic inference. |
| Structured output | `BAR-003`; `DCT-001`; `DCT-002`; `DCT-003`; `DCT-004` | Every command returns explicit success/failure and evidence/error fields. |
| Scope boundary | `OOS-001`; `TECH-002` | Implementation does not add non-tmux terminal backends or remote orchestration. |
| Input confirmation | `REQ-004`; `EXE-004`; `RISK-003` | Input command captures screen one second after sending and exposes confirmation evidence. |

## 11. Output Contract

| ID | Output | Requirement | Acceptance Rule |
| --- | --- | --- | --- |
| `OUT-001` | LaunchSessionResponse containing tmux session id and launch metadata. | `REQ-001` | Satisfies `AC-001`, related `VER-*`, and `DONE-001`. |
| `OUT-002` | StructuredScreen containing messages, input, parser status, and raw screen evidence. | `REQ-002` | Satisfies `AC-002`, related `VER-*`, and `DONE-002`. |
| `OUT-003` | StatusDiff containing idle or busy state and structured diff details. | `REQ-003` | Satisfies `AC-003`, related `VER-*`, and `DONE-003`. |
| `OUT-004` | Input confirmation response containing the post-send screen capture and delivery evidence. | `REQ-004` | Satisfies `AC-004`, related `VER-*`, and `DONE-004`. |
| `OUT-005` | Termination response containing operation mode, success flag, and final session existence state. | `REQ-005` | Satisfies `AC-005`, related `VER-*`, and `DONE-005`. |

## 12. Open Decisions

There are no blocking open `Q-*` decisions. The following execution-affecting assumptions remain visible and must not be silently expanded.

| ID | Assumption | Impact | Status | Agent Handling | Resolution Refs |
| --- | --- | --- | --- | --- | --- |
| `ASM-001` | The target runtime is a local Unix-like environment where tmux and Claude CLI can be invoked by subprocess. | Affects launch, capture, input, and termination commands because all session control is delegated to tmux subprocesses. | deferred | Proceed only for local Unix-like tmux runtime; return STOP-001 or STOP-002 structured failure when tmux or Claude CLI is unavailable. | `STOP-001`, `STOP-002`, `VER-001`, `VER-002` |
| `ASM-002` | Permission settings can be represented as CLI args, environment variables, or generated config files selected by the implementation. | Affects launch_config shape, environment materialization, and reproducibility of Claude CLI permissions. | deferred | Select CLI args, environment variables, or generated config files during implementation, then make the selected profile visible in OUT-001. | `IN-001`, `OUT-001`, `TECH-001`, `VER-001` |
| `ASM-003` | The 99% accuracy target is measured on an implementation-owned labeled fixture corpus for known Claude CLI screen states. | Affects release readiness for status detection and prevents unsupported accuracy claims. | deferred | Treat VER-006 as a blocking release gate; do not mark status detection done when either accuracy metric is below 99%. | `MET-001`, `MET-002`, `VER-006`, `BAR-002` |

## 13. Stop Conditions

| ID | Trigger | Reason | Status | Required Action | Failure Output |
| --- | --- | --- | --- | --- | --- |
| `STOP-001` | launch_preflight_failed | Launch cannot satisfy REQ-001 without tmux, Claude CLI, or writable workspace. | defined | Return a structured launch failure and do not claim a session id. | `OUT-001` |
| `STOP-002` | session_capture_unavailable | Capture/status cannot satisfy REQ-002 or REQ-003 without an addressable session and observable screen. | defined | Return a structured capture/status failure. | `OUT-002` |
| `STOP-003` | classification_rules_insufficient | Semantic guessing would violate BAR-001. | defined | Return unknown or structured failure instead of idle/busy. | `OUT-003` |
| `STOP-004` | input_target_unavailable | Input cannot satisfy REQ-004 without an addressable tmux session. | defined | Return a structured input failure. | `OUT-004` |
| `STOP-005` | graceful_exit_failed_without_force | Force kill requires explicit termination authority. | defined | Report graceful failure unless the caller requested force mode. | `OUT-005` |

## 14. Done Criteria

| ID | Completion Condition | Verification Reference | Output Reference | Blocking |
| --- | --- | --- | --- | --- |
| `DONE-001` | Launch is done when a configured tmux Claude CLI session starts and returns a usable session id. | `VER-001` | `OUT-001` | Yes |
| `DONE-002` | Capture is done when raw screen, messages, input, and parser status are returned structurally. | `VER-002` | `OUT-002` | Yes |
| `DONE-003` | Status detection is done when idle/busy classification, structured diff, and 99%/99% corpus evidence are implemented. | `VER-003`, `VER-006` | `OUT-003` | Yes |
| `DONE-004` | Input is done when instruction send, execution trigger, one-second confirmation capture, and structured result work. | `VER-004` | `OUT-004` | Yes |
| `DONE-005` | Termination is done when graceful /exit and force kill modes return reliable structured outcomes. | `VER-005` | `OUT-005` | Yes |

## References

| ID | Reference | Usage |
| --- | --- | --- |
| `SRC-001` | Original user idea | Source for product scope, five operations, mechanical-only constraint, 1-second confirmation, and 99%/99% accuracy target. |
| `REF-001` | Canonical structured contract | Source of truth for all object IDs and execution facts in this Agent PRD. |
| `REF-002` | Human PRD | Sibling human-facing rendered artifact. |
| `REF-004` | Execution task plan | Sibling task decomposition artifact derived from this Agent PRD. |
