---
name: spec-intake
description: Run a harness-first intake workflow that turns a raw idea into a structured requirement table, a prd-writer PRD with review brief, and an hld-writer HLD.
---

# Spec Intake

Use this skill as the Codex adapter for the `spec-intake` harness workflow. The harness turns a raw product idea into a package that a human reviewer and downstream design consumer can inspect without guessing.

The workflow is a review-gated, self-improving generation harness. Do not treat it as a prompt-only PRD or HLD writer. Every downstream artifact must be derived from the Stage 1 structured requirement table inside `contract-envelope.json`.

## Required References

Load only what the current request needs:

- `references/intake-method.md`: use for Stage 1 requirement-table intake and clarification.
- `references/prd-rendering.md`: use for Stage 2 `prd-writer` delegation, `prd.md` acceptance, and `prd-brief.md` derivation.
- `references/prd-quality-reference.md`: use in Stage 2 only as a PRD quality bar; never use it as current-product evidence.
- `references/output-artifacts.md`: use before writing or reviewing `contract-envelope.json`, `prd.md`, `prd-brief.md`, or HLD.
- `references/hld-design.md`: use only after PRD review approval; Stage 3 delegates HLD writing to `hld-writer`.
- `references/quality-gates.md`: use before claiming any package is ready.

## Harness Stages

1. Stage 1: requirement table intake.
   - Declare the run mode in `harness_workflow.execution_mode`: use `live_interactive` for a real user-facing workflow, or `reference_replay` only for non-interactive regression/reference validation.
   - Never claim a `reference_replay` package is a completed live workflow.
   - Register the user's idea and supplied notes as source facts.
   - Separate explicit facts, confirmed facts, bounded inferences, assumptions, and open questions.
   - Ask clarification only as boolean, single-choice, or multi-choice questions.
   - Record `contract-envelope.json.interaction_decision` before ending Stage 1.
   - Collect or block on the PRD-ready support Stage 2 needs: product context, target-user posture, MVP boundary, acceptance and verification method, implementation approach, roadmap, risks/open decisions, sources, and execution refs.
   - For executor, agent, adapter, CLI, automation, scheduler, daemon, workflow, or tool-orchestration ideas, also collect execution topology: external components, authoritative component sources, public interface boundary, execution loop, state handling, subjective judgment boundary, evidence chain, and mechanical delivery checks.
   - Produce or update `contract-envelope.json.requirement_table`.
   - End Stage 1 only after a real Stage 1 package exists and `validate_spec_intake_package.py <output-dir> --stage stage1` passes.
   - If blocking information is missing, keep affected targets draft or blocked.
2. Stage 2: PRD writer and PRD brief.
   - Invoke `prd-writer` as the only owner of the standard PRD body.
   - Provide `prd-writer` the Stage 1 requirement table, canonical contract objects, source refs, constraints, open questions, assumptions, and quality bars.
   - Require `prd-writer` to output `prd.md` as the standard PRD document. `spec-intake` must not create `agent-prd.md` or `human-prd.md`.
   - Record `contract-envelope.json.writer_invocations.prd` with `writer_skill=prd-writer` or `prd-writing`, `status=completed`, `source_ref=SRC-*`, `input_refs`, and sha256-bound `output_artifacts`.
   - Derive `prd-brief.md` from `prd.md` and `contract-envelope.json` as a professional Simplified Chinese review brief for humans.
   - Use `references/prd-quality-reference.md` to calibrate specificity, structure, and review usefulness; do not copy its domain facts or treat it as evidence for the current product.
   - Validate the PRD-only package with `validate_spec_intake_package.py <output-dir> --stage stage2`; Stage 2 must not include HLD or task-plan artifacts.
   - Give `prd.md` and `prd-brief.md` to the user for approval.
   - Stop for explicit user approval before Stage 3 in `live_interactive` mode.
   - Approval evidence must be a `SRC.source_type=user_confirmation` with `confirmation_kind=prd_review_approval`, `confirmation_intent=approve_prd_and_enter_stage_3`, and `approved_artifacts` entries whose paths are `prd.md` and `prd-brief.md` with sha256 values matching the rendered files.
   - If the user requests revision, update the requirement table first, then rerun `prd-writer` and regenerate the brief.
   - Do not enter Stage 3 until `harness_workflow.approval_gates.prd_review.status=approved` with a `SRC.source_type=user_confirmation` ref.
3. Stage 3: HLD writer.
   - Invoke `hld-writer` as the only owner of HLD generation.
   - Provide `hld-writer` the approved `prd.md`, `prd-brief.md`, `contract-envelope.json`, Stage 1 requirement table, canonical objects, source refs, environment/data/permission facts, and acceptance constraints.
   - Require HLD output as `high-level-design.json`, `high-level-design.md`, and `hld-semantic-review.json`.
   - Record `contract-envelope.json.writer_invocations.hld` with `writer_skill=hld-writer` or `hld-writing`, `status=completed`, `source_ref=SRC-*`, `input_refs`, and sha256-bound `output_artifacts`.
   - Ask the user for missing Stage 3 information when real environment, real data, interface documentation, permissions, deployment constraints, acceptance owner, or other HLD-critical facts are unclear.
   - Do not produce task plans, task graphs, dependency edges, or implementation task cards.

## Output Package

When creating a final package, write this shape unless the user names another destination:

```text
<output-dir>/
  contract-envelope.json
  prd.md
  prd-brief.md
  high-level-design.json
  high-level-design.md
  hld-semantic-review.json
  intake-notes.md
```

`contract-envelope.json` is the source of truth. `prd.md` is the standard PRD produced by `prd-writer`; `prd-brief.md` is a concise human review brief derived from `prd.md` and the contract. `high-level-design.json`, `high-level-design.md`, and `hld-semantic-review.json` are produced by `hld-writer` and validated by this harness. A JSON-only HLD is incomplete.

A Stage 1-only package contains `contract-envelope.json` only. Do not include PRD, PRD brief, HLD, Human/Agent PRD legacy files, or task-plan files before the proper stage runs.

## Hard Rules

- Requirement table first: no PRD, PRD brief, or HLD fact may exist only in prose.
- Writer ownership: Stage 2 must use `prd-writer` for `prd.md`; Stage 3 must use `hld-writer` for HLD. If the required writer is unavailable, produce a blocked package instead of falling back to ad hoc writing.
- Writer evidence required: ready Stage 2 and ready Stage 3 must include `writer_invocations` records and `SRC.source_type=system_generated` evidence proving the writer dependency, invocation status, inputs, and output artifact digests.
- No legacy PRDs: `human-prd.md` and `agent-prd.md` are forbidden outputs.
- Run mode first: every package must declare `live_interactive` or `reference_replay`; replay packages cannot be handed off as completed live workflows.
- Interaction decision first: Stage 1 must explicitly record whether it is asking the user, proceeding without questions, or producing a blocked draft.
- Closed questions only: clarification questions must be `boolean`, `single_choice`, or `multi_choice` with explicit options.
- PRD-ready means real support: `proceed_without_questions` is allowed only when Stage 1 can support a standard PRD and PRD brief with source-backed product context, user posture, scope, acceptance/verification, implementation approach, roadmap, risks/open decisions, and `IN`/`EXE`/`VER`/`OUT`/`STOP`/`DONE` refs when execution behavior is material.
- Execution topology required: for executor, agent, adapter, CLI, automation, scheduler, daemon, workflow, or tool-orchestration ideas, Stage 1 must capture source-backed control flow, modules, technical decisions, state handling, evidence outputs, judgment boundaries, and delivery checks, or record blocked questions/assumptions.
- Honest unknowns: unknown facts become `Q`, `ASM`, `STOP`, or blocked gates.
- No hallucinated completion: bounded inferences must cite source refs, include `TRACE.relation=inferred_from`, and material assumptions must block readiness.
- PRD review gate: Stage 3 is forbidden until PRD review approval is recorded as a user-confirmation source.
- Approval binding required: PRD approval must explicitly target PRD review, authorize Stage 3, and bind the current `prd.md` and `prd-brief.md` sha256 values. Generic "continue", "run the full chain", or reference replay authorization is not approval.
- No thin PRD: `prd.md` must be a complete standard PRD with product context, users or explicit user posture, goals, success measures, requirements, acceptance, roadmap, risks, dependencies, open questions, and traceability.
- No missing topology: when the contract contains implementation-model refs such as `FLOW`, `DATA`, `MOD`, `TECH`, `STATE`, or `DCT`, `prd.md` must preserve the implementation approach enough for HLD writing.
- No thin brief: `prd-brief.md` must answer goal, what to build, how to build it, how to verify it, roadmap, and risks/open decisions with concrete source-backed content.
- Quality reference is not evidence: the PRD quality reference may calibrate quality, but it must not contribute current-product facts, requirements, methods, components, acceptance criteria, or roadmap items.
- HLD must be implementation-ready design: ready HLD requires structured control flow, data flow, data objects, interface contracts, state model, technical decisions, implementation design, environment requirements, and real acceptance plan with contract refs.
- HLD document required: ready Stage 3 must include `high-level-design.md` with required HLD sections, diagrams/tables/current refs/source-backed interface precision/executable acceptance design, exact invocation boundaries, executable acceptance command, preconditions, expected artifact paths, mechanical checks, and failure criteria.
- Independent semantic review required: ready Stage 3 must include `hld-semantic-review.json` with all required semantic dimensions passing.
- Real acceptance only: ready HLD must define concrete confirmed real environment, concrete confirmed real data, execution steps, expected results, evidence capture, acceptance owner, `SRC-*` evidence refs for environment/data/owner, and `mock_policy=forbidden`.
- No task output: task plans, task graphs, dependency edges, parallel groups, implementation task cards, and task decomposition are outside this workflow.

## Completion Check

Before claiming Stage 1 completion, verify:

- `contract-envelope.json` parses and contains `harness_workflow`, `interaction_decision`, `requirement_table`, canonical objects, derived views, and gate report.
- `proceed_without_questions` is backed by PRD-ready Stage 1 support; otherwise `ask_user` or `blocked_draft` is recorded.
- all unresolved clarification questions are boolean or choice questions with options.
- `python skill/scripts/validate_spec_intake_package.py <output-dir> --stage stage1` passes.
- no `prd.md`, `prd-brief.md`, legacy Human/Agent PRD, HLD, or task-plan artifact exists in the Stage 1 package.

Before finalizing the full workflow, verify:

- `contract-envelope.json` parses and contains `harness_workflow`, `interaction_decision`, `requirement_table`, canonical objects, derived views, and gate report.
- all unresolved clarification questions are boolean or choice questions with options.
- `prd.md` and `prd-brief.md` are traceable to the contract and contain no untraced facts.
- Stage 2 PRD package passes `python skill/scripts/validate_spec_intake_package.py <output-dir> --stage stage2` before PRD approval is treated as reviewable.
- Stage 2 contract summary matches the review-gated stage state.
- Stage 3 ready HLD has approved PRD review evidence and contract-backed design refs.
- Stage 3 ready HLD has structured implementation design, a formal `high-level-design.md`, an independent passing `hld-semantic-review.json`, covers current requirement/execution/implementation refs, and contains a no-mock real acceptance plan.
- no legacy Human/Agent PRD, `execution-task-plan.json`, or task decomposition artifact is present.
- validation output is reported honestly, including any skipped checks.
