# Quality Gates

Use this reference before claiming any spec package is ready.

## Contract Gates

Block ready output when:

- required IDs are missing or dangling
- `harness_workflow` is missing, not the required three-stage workflow, or lacks a PRD review gate
- `harness_workflow.execution_mode` is missing, invalid, or uses `reference_replay` while claiming completed Stage 3/live workflow readiness
- PRD approval lacks explicit `prd_review_approval` intent, Stage 3 authorization, or artifact sha256 bindings to the rendered `prd.md` and `prd-brief.md`
- `requirement_table` is missing or does not cover current-phase requirements
- `interaction_decision=proceed_without_questions` but Stage 1 lacks PRD-ready support for product context, target users, MVP boundary, acceptance/verification, implementation approach, source evidence, or execution refs
- execution-like Stage 1 input proceeds without source-backed implementation topology: control flow, modules, technical decisions, external component boundary, state handling, evidence outputs, subjective judgment boundary, or mechanical delivery checks when those are material
- a clarification `Q-*` is open-text instead of boolean, single-choice, or multi-choice
- `object_index` diverges from `objects`
- `SRC` payload lacks a valid `source_type` or auditable content/target for user sources
- `RB` unsupported claims are non-empty
- `traceability_summary` diverges from `render_blocks` or `traceability`
- `quality_gates` diverges from `gate_report.gate_id`
- top-level contract views diverge from `objects` and `object_index`
- `GATE-*` payload diverges from its `gate_report` row
- `CORE.status=blocked`, current `REQ.status=blocked`, or `STOP.status=triggered` affects readiness
- `GATE.status=blocked` affects the target
- `Q` or `ASM` blocks the target and has missing or open status
- `gate_report.status=warning` lacks message or required fix
- Stage 2 does not delegate canonical PRD creation to `prd-writer`
- `prd.md` is missing, thin, unsupported, untraceable, or not a complete standard PRD
- `prd.md` omits material implementation-model refs such as `FLOW`, `DATA`, `MOD`, `TECH`, `STATE`, or `DCT`, causing the implementation approach or integration boundary to disappear before HLD
- `prd-brief.md` is not a professional, formal Simplified Chinese review brief with revision record, product goal, construction scope, implementation approach, acceptance criteria and methods, roadmap, risks/open decisions, and references
- `prd-brief.md` lacks information density: goal, what to build, how to build it, how to verify it, and roadmap are empty, generic, or unsupported by canonical refs
- `prd-brief.md` implementation approach hides material execution topology that exists in the PRD or contract
- `prd-brief.md` includes workflow process markers such as `Source contract:`, `Render status:`, or `render_status`
- `prd-brief.md` does not put revision record first or references last
- `prd-brief.md` substantive sections lack canonical source refs
- Stage 2 package contains downstream HLD, legacy Human/Agent PRD, or task-plan artifacts
- Stage 2 package does not set `prd_review.status` to `pending` or `approved` after PRD rendering
- Stage 2 `approved` review state is not backed by a PRD approval source bound to the current `prd.md` and `prd-brief.md`
- Stage 2 `contract_summary.stage_ready` or `stage_blocked` does not match the review-gated stage state
- rendered requirements cannot be traced to source `REQ-*`
- decision traceability type, ref, and status do not agree
- resolved decisions lack resolution refs or `TRACE.relation` is outside the allowed relation vocabulary

## Stage 1 Question Quality Gate

When `interaction_decision=ask_user`, the clarification set must target the highest-risk blockers in the idea, not merely ask any valid closed-form questions.

Block or revise Stage 1 semantic readiness when:

- executor, agent, adapter, CLI, automation, scheduler, daemon, or workflow ideas omit a closed-form question about the input contract while input shape is unclear
- an external component is central to the idea but no question confirms whether integration is via public CLI/API or internal implementation
- completion authority or output deliverable is unclear and no question combines or covers completion/output contract
- permission, credential, filesystem, network, external-write, or destructive-action boundaries are material and no closed-form question covers them
- questions introduce a new actor or component as the preferred path without also offering a neutral "keep blocked" or public-boundary option
- the first round uses all available questions on secondary details while a core execution boundary remains unresolved

For executor-like workflows with only three questions available, a strong first round usually covers: input contract, external component boundary, and combined completion/output contract.

## HLD Gates

Block ready HLD when:

- Stage 3 does not delegate HLD generation to `hld-writer`
- source PRD status in the HLD does not match the canonical contract
- PRD review approval is missing or not backed by `SRC.source_type=user_confirmation`
- PRD approval is generic, replay-only, not scoped to PRD review, or bound to stale `prd.md` / `prd-brief.md` digests
- `high-level-design.json` is missing
- `source_artifacts` refs, file names, version, status, or phase type diverge from the contract
- HLD refs are missing or not from source contract
- required HLD narrative fields are empty
- structured HLD implementation sections are missing, empty, or lack contract refs
- current requirement, acceptance, verification, input, execution, output, stop, done, or non-empty implementation-model refs are not covered by the HLD
- control flow lacks ordered steps, actors/components, inputs, outputs, interactions, and failure/branch behavior
- data flow lacks source, transformation, target, and data refs
- data objects lack field-level design or lifecycle
- interface contracts lack provider, consumer, invocation, inputs, outputs, or error semantics
- technical decisions lack rationale or implementation notes
- real acceptance plan lacks concrete confirmed real environment, concrete confirmed real data, execution steps, expected results, evidence capture, acceptance owner, `mock_policy=forbidden`, or `SRC-*` evidence refs for environment/data/owner
- ready HLD design gates do not include all required `gate_key` values: `source_readiness`, `control_flow_readiness`, `data_flow_and_object_readiness`, `interface_state_readiness`, `technical_implementation_readiness`, `real_acceptance_readiness`, `hld_document_readiness`, and `task_boundary_readiness`
- a required ready HLD design gate is missing, duplicated, not `pass`, lacks evidence refs, or lacks evidence summary
- ready HLD contains mock, stub, fake, simulated, or synthetic acceptance substitutes
- ready HLD defers acceptance resources with wording such as "selected by downstream owner", "supplied later", "to be provided", `TBD`, or placeholders
- stop/risk/scope controls disappear
- future phase work enters current design without contract support
- HLD adds new facts
- design gate evidence uses `CHECK-*`, non-ID values, or missing refs
- `human-prd.md`, `agent-prd.md`, `execution-task-plan.json`, task graphs, dependency edges, parallel groups, or implementation task cards appear in the package

## Subjective Review Rubric

Score each dimension `pass`, `revise`, or `fail`:

| Dimension | Pass condition |
| --- | --- |
| Product clarity | User, problem, value, MVP, non-goals, roadmap, and acceptance method are understandable and source-backed before PRD rendering. |
| Honesty | Unknowns are explicit and do not become facts. |
| PRD quality | `prd.md` is a complete standard PRD produced by `prd-writer`, preserves material execution/implementation topology, and is ready for HLD writing. |
| Human usefulness | `prd-brief.md` lets a human reviewer quickly understand the goal, scope, approach, acceptance standards and methods, roadmap, risks, and evidence without workflow-process clutter. |
| Execution topology | For execution-like ideas, the contract and PRD clearly identify external components, public interface/method boundary, execution loop, state handling, subjective judgment owner, mechanical delivery checks, and evidence outputs. |
| HLD usefulness | The HLD gives an implementation-ready design produced by `hld-writer`, with concrete control flow, data flow, data objects, interface contracts, state model, technical decisions, environment requirements, no-mock real acceptance plan, and risk controls without implementation task decomposition. |
| Traceability | Important claims link to contract refs and source refs. |
| Harness routing | Stage 3 is entered only after PRD review approval, and revise feedback routes back through the requirement table. |
| Clarification quality | Stage 1 questions are closed-form and target the highest-risk missing boundaries for the idea type. |

Any `fail` blocks ready. Any `revise` requires either patching or explicitly downgrading output status.

## Validation Script

For Stage 1 packages, run:

```bash
python <path-to-spec-intake-skill>/scripts/validate_spec_intake_package.py <output-dir> --stage stage1
```

For Stage 2 PRD packages, run:

```bash
python <path-to-spec-intake-skill>/scripts/validate_spec_intake_package.py <output-dir> --stage stage2
```

For final packages, run:

```bash
python <path-to-spec-intake-skill>/scripts/validate_spec_intake_package.py <output-dir>
```

In this repository's development layout, run `python skill/scripts/validate_spec_intake_package.py <output-dir> --stage stage1` for Stage 1 packages, `python skill/scripts/validate_spec_intake_package.py <output-dir> --stage stage2` for Stage 2 PRD packages, or `python skill/scripts/validate_spec_intake_package.py <output-dir>` for final packages, from `skills/spec-intake`.

For repository development, also run:

```bash
python tests/validator_regression.py
```

Report the exact verdict. Do not claim validation passed if the script was skipped.
