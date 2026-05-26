# Output Artifacts

Use this reference before writing `contract-envelope.json`, `human-prd.md`, or `agent-prd.md`.

## Package Files

```text
contract-envelope.json
human-prd.md
agent-prd.md
execution-task-plan.json
intake-notes.md
```

The package is a file-based adaptation of `docs/prd-intake/output-contract.md`: `contract-envelope.json` is the canonical contract plus audit layer, while `human-prd.md` and `agent-prd.md` are sibling renders from that contract.

## Contract Envelope

`contract-envelope.json` is the source of truth. It must contain:

- `contract_version`
- `intake_id`
- `source_idea`
- `core`
- `scope`
- `requirements`
- `acceptance_criteria`
- `success_metrics`
- `implementation_model`
- `agent_execution`
- `risks`
- `quality_bars`
- `assumptions`
- `open_questions`
- `references`
- `sources`
- `traceability`
- `render_blocks`
- `document_metadata`
- `quality_gates`
- `render_status`
- `objects`
- `object_index`
- `contract_summary`
- `traceability_summary`
- `gate_report`
- `next_actions`

Use canonical IDs: `CORE`, `USER`, `SCOPE`, `OOS`, `PHASE`, `REQ`, `AC`, `MET`, `FLOW`, `DATA`, `MOD`, `TECH`, `STATE`, `DCT`, `IN`, `EXE`, `VER`, `OUT`, `STOP`, `DONE`, `RISK`, `BAR`, `ASM`, `Q`, `REF`, `SRC`, `TRACE`, `RB`, `META`, `GATE`.

Top-level arrays are indexes or views. `objects[ID].payload` owns the facts. `object_index` is derived from `objects` and must cover every object by canonical type.

Every top-level view must match its object type exactly. For example, every `REQ-*` object appears in `requirements`, every `GATE-*` object appears in `quality_gates` and `gate_report`, and every `SRC-*` object appears in `sources`. Do not hide canonical objects only in `objects`.

## Source Facts

Every rendered fact must trace to `SRC-*`, `ASM-*`, `Q-*`, or another canonical object.

`SRC.source_type` must be one of:

- `user_input`
- `user_document`
- `user_confirmation`
- `external_reference`
- `local_file`
- `runtime_input`
- `system_generated`

For `user_input`, `user_document`, and `user_confirmation`, include `content` or `target`. Do not write "user confirmed" only in prose; record a `SRC.source_type=user_confirmation` object and link it through `TRACE` or `decision_traceability`.

## Status Rules

- Human PRD statuses: `not_requested`, `draft`, `review_ready`, `blocked`.
- Agent PRD statuses: `not_requested`, `draft`, `execution_ready`, `blocked`.
- `CORE` and `REQ`: `draft`, `confirmed`, `blocked`.
- `Q` and `ASM`: `open`, `resolved`, `deferred`, `superseded`.
- `RB`: `ready`, `blocked`.
- `STOP`: `defined`, `triggered`, `resolved`.
- `GATE`: `pass`, `warning`, `blocked`.

Do not add `status` to object types that do not define it.

## Readiness Blockers

Ready output is forbidden when:

- `CORE.status=blocked`
- any current `REQ.status=blocked`
- `Q` or `ASM` has `blocks_human_prd=true` or `blocks_agent_prd=true` and `status` is missing or `open`
- `STOP.status=triggered` affects Agent PRD execution
- `GATE.status=blocked` or `GATE.blocking=true` affects the target
- `gate_report.status=warning` lacks `message` or `required_fix`
- `gate_report.status=pass|warning` has `blocking=true`
- `gate_report.blocking=true` has any status other than `blocked`

`contract_summary.ready_targets` and `blocked_targets` must be derived from these blockers, not written by hand.

Current requirements are phase-aware. The current phase is the first canonical `PHASE-*` in `scope.roadmap` unless a task plan provides a more specific canonical phase. Future-phase blocked requirements must not block the current phase, and future-phase requirements must not enter a ready current-phase task plan.

## Human PRD

Render in professional simplified Chinese. It answers:

- 要做什么、给谁用
- 为什么值得做
- MVP 做什么、不做什么
- 验收标准是什么
- 风险、假设、开放问题是什么
- 分阶段如何落地

The Human PRD is for decision-making. It may be `draft` or `review_ready`; it is not an implementation task list.

## Agent PRD

Render in English. It must define:

- Source of Truth
- Input Contract
- Scope Contract
- Execution Contract
- Data and State Contract
- Verification Contract
- Stop Conditions
- Done Criteria

Agent PRD can be `execution_ready` only when current execution requirements have visible `AC` and `VER`, execution objects are traceable, blocking gates pass, and unresolved decisions are either non-blocking or deferred.

## Render Block Rule

Every meaningful PRD section must be backed by `RB-*` with:

- target: `human_prd` or `agent_prd`
- section
- content type
- `contract_refs`
- `source_refs`
- allowed inference
- unsupported claims
- status

Unsupported claims must be empty for ready outputs.

Requested PRDs must have at least one `RB-*` for their target. Ready PRDs require every target `RB-*` to be `ready`, with non-empty `contract_refs` and `source_refs`.

## Traceability Summary

`traceability_summary.render_traceability` must match `render_blocks`.

`traceability_summary.requirement_traceability` must match `traceability`.

`decision_traceability` is typed:

- `decision_type=open_question`: `decision_ref` must be `Q-*`; status is `open`, `resolved`, `deferred`, or `superseded`.
- `decision_type=assumption`: `decision_ref` must be `ASM-*`; status is `open`, `resolved`, `deferred`, or `superseded`.
- `decision_type=user_confirmation`: `decision_ref` must be `SRC-*` with `source_type=user_confirmation`; status must be `confirmed`.

Every decision trace must include non-empty `affected_refs`.

Resolved `Q-*` and `ASM-*` objects require non-empty `resolution_refs`. `TRACE.relation` must be one of `stated_by`, `confirmed_by`, `inferred_from`, `assumes`, `resolves`, `blocks`, or `renders`.
