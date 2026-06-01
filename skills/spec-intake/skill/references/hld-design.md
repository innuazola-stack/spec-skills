# HLD Writer Design

Use this reference after the PRD package is approved as a `SRC.source_type=user_confirmation`.

## Preconditions

Ready HLD requires:

- `harness_workflow.approval_gates.prd_review.status=approved`
- approval source ref points to `SRC.source_type=user_confirmation`
- approval source binds the current `prd.md` and `prd-brief.md` sha256 values
- `render_status.prd=review_ready`
- `render_status.prd_brief=review_ready`
- `prd.md` contains the required standard PRD sections and source-backed current refs
- Stage 1 `requirement_table` is present and provenance-valid
- `hld-writer` is available and used as the HLD generation owner
- `writer_invocations.hld.status=completed` with `writer_skill=hld-writer` or `hld-writing`, a `SRC.source_type=system_generated` source ref, canonical input refs, and sha256-bound output artifacts
- all HLD statements trace to canonical contract refs or approved PRD refs
- HLD-ready implementation context is present: control flow, data flow, data objects, source-backed interface boundaries, state model, technical decisions, environment requirements, and executable real acceptance inputs
- real acceptance can run in a concrete confirmed environment with concrete confirmed real data and no mock, stub, fake, simulated, or synthetic substitutes
- real acceptance environment, data, and owner are backed by `SRC-*` evidence refs

If any precondition fails, ask the user for the missing Stage 3 information when the user is available. Stage 3 questions may ask for concrete environment details, source paths, credentials/permissions, real data locations, deployment constraints, interface docs, or acceptance ownership. If the missing information cannot be obtained, require `hld-writer` to write a blocked HLD package with blocking reasons, missing refs, required fixes, and a blocked design gate. Do not mark the HLD ready.

## Output Shape

Stage 3 produces three mandatory files through `hld-writer`:

- `high-level-design.json`: structured source of truth for deterministic validation and downstream consumption.
- `high-level-design.md`: formal HLD document for human and agent readers. It is not optional, and a JSON-only delivery is not complete.
- `hld-semantic-review.json`: independent semantic review artifact. It is required because HLD self-reported design gates are not enough to prove implementation readiness.

`high-level-design.json` contains:

- `hld_id`
- `source_artifacts`
- `design_status`
- `blocking_reasons`
- `missing_required_refs`
- `required_fixes`
- `contract_refs`
- `architecture_summary`
- `component_boundaries`
- `data_and_state_design`
- `integration_points`
- `verification_strategy`
- `risk_controls`
- `control_flow_design`
- `data_flow_design`
- `data_objects`
- `interface_contracts`
- `state_model`
- `technical_decisions`
- `implementation_design`
- `environment_requirements`
- `real_acceptance_plan`
- `design_gate_report`

Task planning fields are forbidden: `task_graph`, `tasks`, `task_cards`, `implementation_tasks`, `work_items`, `dependency_edges`, `parallel_groups`, `stage_goal_coverage`, and `planning_gate_report`.

`high-level-design.md` must include these sections in a professional document form:

- `Revision History`
- `Scope And Goals`
- `Architecture Overview`
- `Control Flow`
- `Data Flow`
- `Data Objects`
- `Interface Contracts`
- `State Model`
- `Technical Decisions`
- `Implementation Design`
- `Real Acceptance Plan`
- `Risks And Guardrails`
- `References`

The Markdown HLD must contain concrete final design conclusions only. It must use diagrams and tables where they clarify the design, including at least one Mermaid diagram and structured tables for objects, interfaces, technical decisions, or acceptance. It must cite canonical refs for substantive claims and identify `contract-envelope.json`, `prd.md`, or `high-level-design.json` as source artifacts. A ready Markdown HLD must visibly include source-backed interface precision and executable acceptance design: source evidence, exact invocation boundary, acceptance command, preconditions, expected artifact paths, mechanical checks, and failure criteria.

`hld-semantic-review.json` must include `review_id`, `review_status`, `source_artifacts`, `dimensions`, and `overall_findings`. Ready review requires fixed passing dimensions: `source_traceability`, `control_flow_completeness`, `data_flow_and_objects`, `interface_precision`, `technical_implementation`, `executable_acceptance`, `markdown_parity`, `no_untraced_invention`, and `task_boundary`.

`high-level-design.json.source_artifacts` must include `contract_ref=contract-envelope.json`, `prd_ref=prd.md`, `prd_status=review_ready`, `prd_brief_ref=prd-brief.md`, and `prd_brief_status=review_ready`.

## Design Rules

1. HLD generation must be delegated to `hld-writer`.
2. Write architecture and component boundaries only from approved `prd.md`, `prd-brief.md`, requirement table, and canonical contract refs.
3. Do not introduce product facts, technologies, integrations, data fields, tests, or scope that are absent from the contract or approved PRD.
4. Use `contract_refs` to identify the objects that support the HLD.
5. Keep missing execution facts as blockers, not design assumptions.
6. Use `design_gate_report` to explain whether HLD is ready or blocked.
7. For ready HLD, model control flow as ordered steps with trigger, actor/component, inputs, outputs, interactions, branches, and failure behavior.
8. For ready HLD, model data flow as source, transformation, target, persistence/retention if applicable, data refs, and contract refs.
9. For ready HLD, model data objects with field-level meaning, required/optional status, lifecycle, and contract refs.
10. For ready HLD, model interfaces with provider, consumer, exact invocation style, inputs, outputs, error semantics, source refs, and contract refs.
11. For ready HLD, model state transitions and technical decisions explicitly. Key technical decisions must include rationale and implementation notes.
12. Verification must be an executable acceptance design, not a test slogan. It must name the concrete confirmed real environment, concrete confirmed real data, acceptance command, preconditions, execution steps, expected results, expected artifact paths, mechanical checks, failure criteria, evidence to capture, and acceptance owner.
13. Mock, stub, fake, simulated, and synthetic acceptance inputs are forbidden in ready HLD. Use `real_acceptance_plan.mock_policy="forbidden"`.
14. Deferred wording such as "selected by downstream owner", "supplied later", "to be provided", `TBD`, or placeholders is forbidden in ready HLD. Missing real acceptance resources must trigger Stage 3 questions or blocked HLD.
15. `real_acceptance_plan` must include `environment_source_refs`, `real_data_source_refs`, and `acceptance_owner_source_refs`, each pointing to `SRC-*` evidence.
16. Ready HLD `design_gate_report` must contain pass gates with fixed gate keys: `source_readiness`, `control_flow_readiness`, `data_flow_and_object_readiness`, `interface_state_readiness`, `technical_implementation_readiness`, `real_acceptance_readiness`, `hld_document_readiness`, and `task_boundary_readiness`.
17. Ready HLD must render the structured JSON design into `high-level-design.md`; the Markdown document must not be a JSON wrapper, thin summary, task plan, or process log.
18. The Markdown HLD must make data flow, control flow, data objects, interaction interfaces, selected technical approach, implementation details, and real acceptance method directly readable without opening JSON.

## Ready Gate

Ready HLD must have:

- `design_status=ready`
- empty `blocking_reasons`, `missing_required_refs`, and `required_fixes`
- non-empty `contract_refs`
- non-empty narrative fields
- non-empty structured implementation fields: `control_flow_design`, `data_flow_design`, `data_objects`, `interface_contracts`, `state_model`, `technical_decisions`, `implementation_design`, `environment_requirements`, and `real_acceptance_plan`
- current-phase requirement, acceptance, verification, input, execution, output, stop, done, and non-empty implementation-model refs are covered by HLD `contract_refs` or nested structured section refs
- `real_acceptance_plan` names concrete confirmed real environment, concrete confirmed real data, executable acceptance command, preconditions, execution steps, expected results, expected artifact paths, mechanical checks, failure criteria, evidence capture, acceptance owner, `mock_policy=forbidden`, and `SRC-*` refs for environment, data, and owner
- `design_gate_report` contains all required ready gate keys and each required gate passes with evidence
- `high-level-design.md` exists, cites its source artifacts, contains all required HLD sections, includes Mermaid and tables, covers current design refs, renders interface source refs, renders the exact acceptance command and expected artifact paths, and visibly includes source-backed interface precision plus executable acceptance design
- `hld-semantic-review.json` exists, has `review_status=pass`, contains every required semantic dimension, and records no warning or blocked dimension for ready HLD
- no blocked design gate
- no legacy Human/Agent PRD, `execution-task-plan.json`, task graph, task alias, dependency edge, parallel group, or implementation task artifact in the package
