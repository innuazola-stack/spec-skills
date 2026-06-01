# Spec Intake Workflow

## Harness Type

`spec-intake` is a review-gated, self-improving generation harness.

## Stage 1: Requirement Table Intake

Input:
- raw user idea
- optional notes, files, constraints, or prior PRD fragments
- declared execution mode: `live_interactive` for a real user-facing run, or `reference_replay` for non-interactive regression/reference validation

Actions:
- register source facts as `SRC-*`
- record `harness_workflow.execution_mode`; never mix reference replay evidence with live execution evidence
- classify extracted statements as explicit facts, confirmed facts, bounded inferences, assumptions, or open questions
- write `interaction_decision` as `ask_user`, `proceed_without_questions`, or `blocked_draft`
- ask only boolean, single-choice, or multi-choice clarification questions when readiness blockers remain and the decision is `ask_user`
- collect or block on the PRD-ready support needed by Stage 2: product context, target-user posture, MVP boundary, acceptance and verification method, implementation approach, roadmap, risks/open decisions, sources, and execution refs
- for execution-like ideas, collect or block on execution topology: external components, authoritative component sources, public interface boundary, execution loop, state handling, subjective judgment boundary, evidence chain, and mechanical delivery checks
- write `contract-envelope.json.requirement_table`

Output:
- Stage 1 package rooted at `contract-envelope.json`
- canonical contract objects
- interaction decision with source, question, and blocker refs
- structured requirement table
- PRD-ready Stage 1 support when `interaction_decision=proceed_without_questions`
- blocked/draft gates when information is incomplete

Delivery:
- Stage 1 is complete only after `contract-envelope.json` is written as a real file and `skill/scripts/validate_spec_intake_package.py <output-dir> --stage stage1` passes.
- Stage 1 must not output `prd.md`, `prd-brief.md`, `human-prd.md`, `agent-prd.md`, `high-level-design.json`, `high-level-design.md`, `hld-semantic-review.json`, or `execution-task-plan.json`.

Gate:
- pass when current-phase requirements have traceable rows, `interaction_decision` has no undeclared blockers, and `proceed_without_questions` has PRD-ready support for Stage 2
- for execution-like ideas, pass only when control flow, modules, and technical decisions are present and source-backed enough to render implementation approach without inventing component capabilities
- blocked when material product, execution, permission, verification, stop, or done facts are unknown
- blocked when a `reference_replay` run is presented as a completed live workflow

## Stage 2: PRD Writer And PRD Brief

Input:
- validator-clean Stage 1 requirement table
- canonical contract objects
- source refs, assumptions, open questions, quality bars, and execution topology refs
- `prd-writer` availability

Actions:
- call `prd-writer` with the requirement table and canonical contract packet
- require `prd-writer` to produce `prd.md` as the standard PRD document
- record `writer_invocations.prd` with writer skill, status, source ref, input refs, output artifact hashes, and required fix when blocked
- derive `prd-brief.md` from `prd.md` and `contract-envelope.json` in professional Simplified Chinese for human review
- present `prd.md` and `prd-brief.md` for user review
- for `live_interactive`, stop after presenting the PRD package until the user explicitly approves or requests revision
- when approved, record a `SRC.source_type=user_confirmation` whose payload binds the approval to `prd.md` and `prd-brief.md`, the current artifact sha256 values, `confirmation_kind=prd_review_approval`, and `confirmation_intent=approve_prd_and_enter_stage_3`

Delivery:
- `prd.md` must be a complete standard PRD. It must define product metadata, summary, problem/background, users/personas or explicit user posture, goals/outcomes, success metrics, scope/non-goals, use cases, functional and non-functional requirements, implementation approach, acceptance criteria, release plan/roadmap, risks/assumptions/dependencies, open questions, and traceability.
- `prd.md` required sections must contain non-trivial body text and visibly cover current-phase `REQ`, `AC`, `VER`, `IN`, `EXE`, `OUT`, `STOP`, and `DONE` refs when those refs are material.
- `prd.md` must visibly cover non-empty implementation-model refs such as `FLOW`, `DATA`, `MOD`, `TECH`, `STATE`, and `DCT` so execution topology does not disappear before HLD.
- `prd-brief.md` must stay concise and cover product goal, what to build, how to build it, acceptance standards and methods, roadmap, and risks/open decisions.
- `prd-brief.md` implementation path must contain concrete reviewable content, including key external components, major execution loop, judgment/check boundaries, and verification method when those are present in the PRD or contract.
- `prd-brief.md` core sections must contain concrete reviewable content, not only headings or canonical citations.
- Both documents must be derived from the Stage 1 requirement table and canonical objects; missing facts route back to Stage 1.
- Stage 2 is complete only after `skill/scripts/validate_spec_intake_package.py <output-dir> --stage stage2` passes.

Routes:
- `approved`: record a PRD review approval `SRC.source_type=user_confirmation` with artifact binding, then proceed to Stage 3
- `revise`: update the requirement table first, rerun `prd-writer`, regenerate the brief, and repeat Stage 2
- `failed`: stop with blocked status and required fixes

Output:
- `prd.md`
- `prd-brief.md`
- PRD review gate state

Gate:
- ready when both PRD artifacts validate, `prd_review.status` is `pending` or `approved`, and no HLD or task-plan artifact exists in the Stage 2 package
- ready when `contract_summary.stage_ready` includes Stage 1 and Stage 2, Stage 3 is not ready, and pending PRD review keeps Stage 3 blocked
- approved only when the approval source has explicit PRD review intent and sha256 bindings to the rendered `prd.md` and `prd-brief.md`
- blocked when PRD or brief content is thin, unsupported, untraceable, writer dependency is unavailable, writer invocation evidence is missing, or the PRD review gate state is inconsistent

## Stage 3: HLD Writer

Input:
- approved PRD review evidence
- `prd.md`
- `prd-brief.md`
- Stage 1 requirement table
- canonical contract objects
- `hld-writer` availability

Actions:
- call `hld-writer` with the approved PRD package and canonical contract packet
- require `hld-writer` to create `high-level-design.json` as the structured HLD source, `high-level-design.md` as the formal HLD document, and `hld-semantic-review.json` as the independent semantic review artifact
- record `writer_invocations.hld` with writer skill, status, source ref, input refs, output artifact hashes, and required fix when blocked
- require architecture summary, component boundaries, data/state design, integration points, verification strategy, and risk controls
- require structured implementation design: control flow, data flow, data objects, source-backed interface contracts, state model, technical decisions, implementation design, environment requirements, and executable real acceptance plan
- require the formal HLD document to include revision history, scope/goals, architecture overview, control flow, data flow, data objects, interface contracts, state model, technical decisions, implementation design, real acceptance plan, risks/guardrails, references, diagrams, tables, and canonical refs
- when environment, real data, interface documentation, permissions, deployment constraints, acceptance owner, or other HLD-required information is missing, ask the user for that information or produce a blocked HLD with required fixes
- prove HLD readiness through fixed design gates covering source readiness, control flow, data/data objects, interface/state, technical implementation, real acceptance, HLD document readiness, and task boundary; then prove independent semantic review readiness through fixed dimensions

Output:
- ready or blocked `high-level-design.json`
- ready or blocked `high-level-design.md`
- ready or blocked `hld-semantic-review.json`
- design gate report

Gate:
- ready only when the PRD review gate is approved, `prd.md` is review-ready, all HLD files are present, HLD facts are contract-backed, required implementation design sections are structured and non-empty, interface contracts have exact invocation boundaries and `SRC-*` source evidence, `high-level-design.md` contains the required HLD sections plus diagrams/tables/current refs/source-backed interface precision/executable acceptance design, current requirement/execution/implementation refs are covered, concrete real-environment and real-data acceptance is defined with executable command, preconditions, expected artifacts, mechanical checks, failure criteria, `SRC-*` evidence refs, and no mock or deferred content, all required HLD design gate keys including `hld_document_readiness` are present and pass, `hld-semantic-review.json` has `review_status=pass` and all required dimensions pass, no task-plan artifact exists, and validator passes
- ready only when `harness_workflow.execution_mode=live_interactive`; reference replay may validate examples but must not claim a completed live workflow
- blocked when `hld-writer` is unavailable or when control flow, data flow, data objects, interface contracts, state model, technical decisions, implementation details, real environment, real data, or acceptance evidence are missing or unsupported

## Retry And Exhaustion

Revision loops route back to Stage 1 because feedback changes the requirement table before PRD or HLD are regenerated. The default maximum review loop count is 3. When the loop exhausts, produce a blocked package with unresolved questions and required fixes.

## Handoff

The final handoff must state package path, stage status, ready/blocked targets, writer dependencies used, validator command, validator verdict, semantic review verdict, and remaining risks.
