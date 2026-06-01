# Output Artifacts

Use this reference before writing `contract-envelope.json`, `prd.md`, `prd-brief.md`, `high-level-design.json`, or `high-level-design.md`.

## Package Files

Stage 1 package:

```text
contract-envelope.json
```

Stage 1 is complete only when this file is written and `validate_spec_intake_package.py <output-dir> --stage stage1` passes. Stage 1 packages must not contain `prd.md`, `prd-brief.md`, `human-prd.md`, `agent-prd.md`, `high-level-design.json`, `high-level-design.md`, `hld-semantic-review.json`, or `execution-task-plan.json`.

Stage 2 package:

```text
contract-envelope.json
prd.md
prd-brief.md
intake-notes.md
```

Stage 2 is complete only when these files are written and `validate_spec_intake_package.py <output-dir> --stage stage2` passes. Stage 2 packages must not contain `human-prd.md`, `agent-prd.md`, `high-level-design.json`, `high-level-design.md`, `hld-semantic-review.json`, or `execution-task-plan.json`. `render_status.prd` must be `review_ready`, `render_status.prd_brief` must be `review_ready`, `harness_workflow.current_stage` must be `stage_2_prd_review`, and `prd_review.status` must be `pending` or `approved`. `contract_summary.stage_ready` must include Stage 1 and Stage 2, must not include Stage 3, and pending PRD review must keep Stage 3 blocked.

Final package:

```text
contract-envelope.json
prd.md
prd-brief.md
high-level-design.json
high-level-design.md
hld-semantic-review.json
intake-notes.md
```

The package is a file-based adaptation of the harness output contract: `contract-envelope.json` is the canonical contract plus audit layer, `prd.md` is the standard PRD produced by `prd-writer`, `prd-brief.md` is the concise human review brief, `high-level-design.json` is the structured HLD source, `high-level-design.md` is the formal human-readable HLD document, and `hld-semantic-review.json` is the independent semantic review artifact.

## Contract Envelope

`contract-envelope.json` is the source of truth. It must contain:

- `contract_version`
- `intake_id`
- `harness_workflow`
- `source_idea`
- `interaction_decision`
- `requirement_table`
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
- `writer_invocations`
- `objects`
- `object_index`
- `contract_summary`
- `traceability_summary`
- `gate_report`
- `next_actions`

Use canonical IDs: `CORE`, `USER`, `SCOPE`, `OOS`, `PHASE`, `REQ`, `AC`, `MET`, `FLOW`, `DATA`, `MOD`, `TECH`, `STATE`, `DCT`, `IN`, `EXE`, `VER`, `OUT`, `STOP`, `DONE`, `RISK`, `BAR`, `ASM`, `Q`, `REF`, `SRC`, `TRACE`, `RB`, `META`, `GATE`.

Top-level arrays are indexes or views. `objects[ID].payload` owns the facts. `object_index` is derived from `objects` and must cover every object by canonical type.

## Writer Invocation Evidence

`writer_invocations` proves that `spec-intake` delegated writer-owned artifacts instead of hand-authoring them.

Required records:

- `writer_invocations.prd` for Stage 2.
- `writer_invocations.hld` for Stage 3.

Each writer record must include:

- `writer_skill`: `prd-writer` or `prd-writing` for PRD; `hld-writer` or `hld-writing` for HLD.
- `status`: `completed`, `blocked`, `unavailable`, or `failed` after the stage is attempted.
- `source_ref`: a `SRC-*` object with `source_type=system_generated` describing the writer invocation.
- `input_refs`: canonical IDs supplied to the writer.
- `output_artifacts`: for completed runs, path and sha256 for writer-owned outputs.
- `required_fix`: required when status is `blocked`, `unavailable`, or `failed`.

Ready Stage 2 requires `writer_invocations.prd.status=completed` and `output_artifacts.path=prd.md`.
Ready Stage 3 requires `writer_invocations.hld.status=completed` and output artifacts for `high-level-design.json`, `high-level-design.md`, and `hld-semantic-review.json`.

When a writer is unavailable, the package must be blocked and must include `required_fix`; do not silently handwrite the writer-owned artifact.

## Harness Workflow State

`harness_workflow.workflow_type` must be `review_gated_self_improving_generation`.

`harness_workflow.stage_order` must be:

1. `stage_1_requirements_table`
2. `stage_2_prd_review`
3. `stage_3_hld`

`harness_workflow.approval_gates.prd_review` controls the Stage 2 to Stage 3 transition. Stage 3 may run only when:

- `status=approved`
- `approved_by_ref` points to a `SRC-*` object
- that `SRC-*` has `source_type=user_confirmation`
- that `SRC-*` has `confirmation_kind=prd_review_approval`
- that `SRC-*` has `confirmation_intent=approve_prd_and_enter_stage_3`
- `approved_artifacts` binds both `prd.md` and `prd-brief.md` by current sha256 digest

When the user rejects or revises the PRD package, set the approval gate to `revise`, update the requirement table, rerun `prd-writer`, regenerate the PRD brief, and do not enter HLD.

## Interaction Decision

`interaction_decision` is the hard Stage 1 route decision. It records whether the workflow must ask the user, can proceed without questions, or can only produce a blocked draft.

Required fields:

- `stage=stage_1_requirements_table`
- `decision`: `ask_user`, `proceed_without_questions`, or `blocked_draft`
- `can_ask_user`
- `reason`
- `question_refs`
- `blocking_refs`
- `source_refs`

`decision=ask_user` requires non-empty `question_refs` backed by `Q-*` objects. `decision=proceed_without_questions` is forbidden while unresolved blocking `Q-*`, `ASM-*`, triggered `STOP-*`, or blocking `GATE-*` refs remain.

`decision=proceed_without_questions` also requires PRD-ready Stage 1 support. The contract must already contain source-backed product context, target-user posture, MVP boundary, current-phase requirement rows, acceptance/verification support, implementation approach support, and complete execution refs (`IN`, `EXE`, `VER`, `OUT`, `STOP`, `DONE`) when execution behavior is material. Missing support must route to `ask_user` or `blocked_draft`.

## Status Rules

- PRD statuses: `not_requested`, `draft`, `review_ready`, `blocked`.
- PRD brief statuses: `not_requested`, `draft`, `review_ready`, `blocked`.
- `CORE` and `REQ`: `draft`, `confirmed`, `blocked`.
- `Q` and `ASM`: `open`, `resolved`, `deferred`, `superseded`.
- `RB`: `ready`, `blocked`.
- `STOP`: `defined`, `triggered`, `resolved`.
- `GATE`: `pass`, `warning`, `blocked`.

Do not add `status` to object types that do not define it.

## Render Block Rule

Every meaningful PRD or brief section must be backed by `RB-*` with:

- target: `prd` or `prd_brief`
- section
- content type
- `contract_refs`
- `source_refs`
- allowed inference
- unsupported claims
- status

Unsupported claims must be empty for ready outputs.

Requested PRD artifacts must have at least one `RB-*` for their target. Ready artifacts require every target `RB-*` to be `ready`, with non-empty `contract_refs` and `source_refs`.
