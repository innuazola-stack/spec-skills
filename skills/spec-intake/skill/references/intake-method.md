# Intake Method

Use this reference when the user gives a raw idea, one-line concept, rough notes, or an incomplete PRD request.

## Classify Source Material

Every extracted statement must become one of:

| Class | Meaning | Contract handling |
| --- | --- | --- |
| Explicit fact | The user or supplied material states it directly. | Create/update object with `SRC.source_type=user_input` or `user_document`. |
| Confirmed fact | The user confirms it during clarification. | Create `SRC.source_type=user_confirmation`; add trace relation `confirmed_by`. |
| Bounded inference | Combines known facts without adding an unsupported product claim. | Keep draft; add `TRACE.relation=inferred_from`; add `ASM` or `Q` if it affects scope, acceptance, execution, risk, or stop behavior. |
| Assumption | Plausible but unconfirmed. | Create `ASM`; block ready output if material. |
| Open question | Needs human/source decision. | Create `Q`; block affected target when it changes scope, validation, execution, risk, or priority. |

Never write internal `confidence`, `candidate_score`, or `question_priority` into the contract.

## Parse The Idea

Extract:

- roles and users
- problem or failure scenario
- intended outcome
- solution behavior
- input data
- output deliverables
- constraints, risks, permissions, or forbidden actions
- success signals

For executor, agent, adapter, CLI, automation, scheduler, or tool-orchestration ideas, also extract the execution topology before Stage 1 can be considered PRD-ready:

- external components, adapters, CLIs, APIs, SDKs, tools, or skills named by the user
- where authoritative component documentation or implementation can be found, when the user supplies or references it
- public interface boundary: command, API, skill call, adapter method, file contract, or runtime capability
- execution loop: start/attach, send input, observe status, capture output or screen, decide next action, retry/stop, and handoff
- state vocabulary and state handling, such as busy, idle, blocked, exited, unknown, success, failure, or deliverable-ready
- mechanical observation versus subjective judgment: which part is deterministic and which part needs a reviewer, agent, or skill
- evidence chain: logs, screenshots, state records, receipts, output files, validation reports, or review decisions
- mechanical delivery checks that must run before semantic completion or human approval

Map them to candidate objects:

| Signal | Primary objects |
| --- | --- |
| Product name, summary, value | `CORE`, `META` |
| User or role | `USER`, `SCOPE` |
| Problem or pain | `CORE`, `REQ`, `RISK` |
| MVP behavior | `SCOPE`, `REQ`, `EXE`, `FLOW` |
| Input | `IN`, `DATA`, `DCT`, `STOP` |
| Output | `OUT`, `DONE`, `AC` |
| Success standard | `AC`, `MET`, `VER`, `DONE` |
| Boundary | `OOS`, `BAR`, `STOP`, `PHASE` |
| Unknown | `Q`, `ASM` |

For execution-like ideas, map the topology into canonical objects:

| Signal | Primary objects |
| --- | --- |
| External component or adapter | `MOD`, `TECH`, `SRC`, `ASM`, `STOP` |
| Public methods or commands | `TECH`, `EXE`, `VER`, `OUT`, `STOP` |
| Execution loop or monitor | `FLOW`, `EXE`, `VER`, `DATA`, `DONE` |
| Runtime states | `STATE`, `EXE`, `STOP`, `DONE` |
| Subjective judgment step | `MOD`, `TECH`, `EXE`, `VER`, `OUT`, `STOP` |
| Mechanical delivery check | `REQ`, `AC`, `VER`, `OUT`, `DONE`, `STOP` |
| Evidence output | `DATA`, `DCT`, `OUT`, `VER`, `DONE` |

If the idea names an external component and the component documentation or implementation is available from a provided path, repository, URL, or supplied file, read the relevant source before finalizing Stage 1. Register it as `SRC.source_type=local_file`, `external_reference`, or `user_document` and cite it from the affected `REQ`, `EXE`, `VER`, `OUT`, `STOP`, `DONE`, `MOD`, and `TECH` objects. If the source is referenced but unavailable, ask a closed-form question or keep readiness blocked; do not invent method names, states, or capabilities.

## Ask Questions

Ask at most three questions per round. Questions must be closed form:

- `boolean`: exactly two options, normally yes/no or approve/revise.
- `single_choice`: two or more mutually exclusive options.
- `multi_choice`: two or more selectable options.

Do not ask open-text questions. When a free-form answer would be useful, convert it into bounded options and include a choice such as "none of these; keep blocked and ask a narrower follow-up" only when the workflow can safely stay blocked.

Prefer questions that unblock the highest-value target:

1. user, problem, and value
2. MVP scope and non-scope
3. acceptance and success criteria
4. input, permissions, output, stop conditions
5. execution and verification details

For executor, agent, adapter, CLI, or automation workflows, prioritize the first clarification round around the execution boundary before asking lower-level preference questions:

1. Input contract: file, inline text, API payload, existing artifact, or another bounded source.
2. External component boundary: whether the workflow calls a component only through its public CLI/API or may depend on internal implementation.
3. Completion and output contract: who or what decides completion, and what durable output is produced.
4. Permission and safety boundary: allowed filesystem, network, credentials, external writes, and destructive actions.
5. Recovery boundary: whether MVP includes retry, resume, queueing, concurrency, or only one sequential run.
6. Source availability: whether authoritative docs or implementation for central components should be read before PRD rendering.
7. Judgment boundary: whether subjective decisions are made by a human, reviewer agent, model call, skill, or deterministic rule.
8. Delivery check boundary: whether the system must run mechanical completeness/evidence checks before handoff.

Do not spend the first clarification round on cosmetic output, naming, or implementation details when input, adapter boundary, completion authority, or permissions are still unresolved. If only three questions are allowed, combine completion and output into one closed-choice question rather than dropping the adapter boundary.

Use concrete, non-leading wording with explicit options:

- Boolean: "Is the first version limited to read-only analysis with no external writes? Options: Yes / No."
- Single choice: "Which MVP boundary should Stage 1 use? Options: A. transcript-to-Markdown only; B. transcript-to-task-system export; C. keep blocked until the boundary is provided."
- Multi choice: "Which inputs are authorized for the first version? Options: uploaded transcript text; meeting title; participant list; none yet."
- Executor boundary: "Which Adapter integration boundary should Stage 1 use? Options: A. call the existing adapter only through its public CLI/API; B. allow direct internal library/API use; C. keep blocked until the adapter boundary is specified."

## Output Decision

Before Stage 1 ends, write `contract-envelope.json.interaction_decision` with:

- `stage=stage_1_requirements_table`
- `decision`: `ask_user`, `proceed_without_questions`, or `blocked_draft`
- `can_ask_user`
- `reason`
- `question_refs`
- `blocking_refs`
- `source_refs`

Ask first when:

- user/problem/value are too unclear to model `CORE`
- MVP scope cannot be separated from future scope
- target users, personas, or explicit unknown-user posture cannot be supported
- product goal, implementation approach, acceptance method, roadmap, risk/open-decision posture, or references would be empty in `prd.md` or `prd-brief.md`
- sensitive data, permissions, automation, or external writes lack stop rules
- execution behavior is material but `IN`, `EXE`, `VER`, `OUT`, `STOP`, or `DONE` cannot be traced

If the user asks for a draft anyway, produce a draft or blocked envelope with `Q`, `ASM`, `STOP`, `GATE`, and `next_actions`; do not mark affected targets ready.

Do not set `decision=proceed_without_questions` while unresolved blocking `Q`, `ASM`, triggered `STOP`, or blocking `GATE` refs remain.

## PRD Support Coverage

Stage 1 is the only source of truth for Stage 2. Before setting `decision=proceed_without_questions`, the contract must contain enough source-backed material to render:

- Standard PRD body: metadata, executive summary, problem/background, users/personas or explicit unknown-user posture, goals/outcomes, scope/non-goals, use cases, functional requirements, guardrails, implementation approach, acceptance, roadmap, risks/assumptions/dependencies, open questions, and traceability.
- Execution support in the PRD: input contract, execution rules, tool/integration boundaries, permission/safety posture, data/state contract, verification, output, stop conditions, and done criteria when those are material.
- PRD brief: product goal, what to build, how to build it, acceptance standards and methods, roadmap, risks/open decisions, and references.

For `proceed_without_questions`, the validator requires at least:

- `CORE.product_name`, `CORE.one_line_summary`, `CORE.problem_statement`, `CORE.value_proposition`, user/persona support, and `CORE.source_refs`
- `scope.in_scope`, `scope.mvp_boundary`, and `scope.roadmap`
- current-phase `REQ-*` rows with problem, user value, MVP scope, acceptance summary, and target artifact refs
- non-empty acceptance criteria plus success metrics or verification cases
- implementation support through `implementation_model` or `agent_execution.execution_rules`
- for execution-like ideas, implementation topology through `implementation_model.control_flow`, `implementation_model.modules`, and `implementation_model.technical_decisions`
- non-empty `agent_execution.input_contracts`, `execution_rules`, `verification_cases`, `output_deliverables`, `stop_conditions`, and `done_criteria`
- auditable `SRC-*` evidence

If any of these are absent and cannot be derived honestly from the idea, ask closed-form clarification questions or produce a blocked draft. Do not fill the gap with invented facts.

## Requirement Table Contract

Stage 1 ends only when a real Stage 1 package exists and `contract-envelope.json.requirement_table` is validator-clean. Each row must capture:

- `row_id`
- `requirement_ref`
- `origin`: `explicit_fact`, `confirmed_fact`, `bounded_inference`, `assumption`, or `open_question`
- `source_refs`
- `problem`
- `user_value`
- `mvp_scope`
- `acceptance_summary`
- `target_artifact_refs`

The row `origin` must match its evidence. `explicit_fact` and `confirmed_fact` require `SRC-*`; `assumption` requires `ASM-*`; `open_question` requires `Q-*`; `bounded_inference` requires `SRC-*` and `TRACE.relation=inferred_from` to the row requirement.

`prd.md`, `prd-brief.md`, and HLD must derive from these rows plus the canonical `objects` payloads. If feedback changes the PRD, update the requirement table first, then rerun `prd-writer` and regenerate the brief.

Run `python skill/scripts/validate_spec_intake_package.py <output-dir> --stage stage1` before claiming Stage 1 is complete. A Stage 1 package must not contain `prd.md`, `prd-brief.md`, `human-prd.md`, `agent-prd.md`, `high-level-design.json`, or `execution-task-plan.json`.
