# Contract Envelope Schema

`contract-envelope.json` is the canonical Stage 1 contract and audit envelope consumed by `prd-writer`, `prd-brief.md`, and `hld-writer`.

## Harness Workflow

Required fields:

- `workflow_type`: `review_gated_self_improving_generation`
- `stage_order`: `stage_1_requirements_table`, `stage_2_prd_review`, `stage_3_hld`
- `current_stage`: one of `stage_1_requirements_table`, `stage_2_prd_review`, `stage_3_hld`, `complete`, `blocked`
- `execution_mode`: `live_interactive` or `reference_replay`
- `approval_gates.prd_review.status`: `not_started`, `pending`, `approved`, `revise`, or `failed`
- `approval_gates.prd_review.approved_by_ref`: required only when approved, and must reference a `SRC-*` user confirmation

When `approval_gates.prd_review.status=approved`, the approval source payload must include:

- `source_type`: `user_confirmation`
- `confirmation_kind`: `prd_review_approval`
- `confirmation_intent`: `approve_prd_and_enter_stage_3`
- `confirmed_stage`: `stage_2_prd_review`
- `approved_artifacts`: entries for `prd.md` and `prd-brief.md`, each with a sha256 digest that matches the rendered artifact

## Render Status

`render_status` must use the current artifact targets:

- `prd`: `not_requested`, `draft`, `review_ready`, or `blocked`
- `prd_brief`: `not_requested`, `draft`, `review_ready`, or `blocked`

Legacy `human_prd` and `agent_prd` render targets are forbidden in new packages.

## Render Blocks

Each `RB-*` payload must include:

- `target`: `prd` or `prd_brief`
- `section`
- `content_type`
- `contract_refs`
- `source_refs`
- `allowed_inference`
- `unsupported_claims`
- `status`

## HLD Source Artifacts

## Writer Invocations

`writer_invocations` must record writer-owned artifact generation:

- `writer_invocations.prd.writer_skill`: `prd-writer` or `prd-writing`
- `writer_invocations.prd.status`: `completed`, `blocked`, `unavailable`, or `failed`
- `writer_invocations.prd.source_ref`: `SRC-*` with `source_type=system_generated`
- `writer_invocations.prd.output_artifacts`: includes `prd.md` with sha256 when completed
- `writer_invocations.hld.writer_skill`: `hld-writer` or `hld-writing`
- `writer_invocations.hld.status`: `completed`, `blocked`, `unavailable`, or `failed`
- `writer_invocations.hld.source_ref`: `SRC-*` with `source_type=system_generated`
- `writer_invocations.hld.output_artifacts`: includes HLD JSON, HLD Markdown, and semantic review with sha256 when completed

Blocked or unavailable writer records must include `required_fix`.

## HLD Source Artifacts

Ready `high-level-design.json` must include `design_status=ready`, `source_artifacts.prd_ref=prd.md`, `source_artifacts.prd_status=review_ready`, `source_artifacts.prd_brief_ref=prd-brief.md`, `source_artifacts.prd_brief_status=review_ready`, non-empty `contract_refs`, all required HLD narrative fields, structured implementation sections, `real_acceptance_plan`, and `design_gate_report`.

Task planning fields are forbidden in HLD.
