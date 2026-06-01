# Eval Case: Stage 3 HLD Implementation Design

## Prompt

Use `spec-intake` Stage 3 to produce HLD from an approved Human PRD, execution-ready Agent PRD, and validated requirement table.

The product has enough contract support to design implementation flow, data objects, interfaces, state handling, technical decisions, and real-environment acceptance.

## Expected Behavior

- Produce `high-level-design.json` as the structured HLD source and `high-level-design.md` as the formal HLD document; do not produce task plans or task cards.
- Produce `hld-semantic-review.json` as an independent semantic review artifact.
- Require Human PRD approval evidence backed by `SRC.source_type=user_confirmation`.
- Use only approved PRDs, requirement table rows, and canonical contract objects.
- Include architecture summary, component boundaries, data/state design, integration points, verification strategy, and risk controls.
- Include structured implementation design sections: `control_flow_design`, `data_flow_design`, `data_objects`, `interface_contracts`, `state_model`, `technical_decisions`, `implementation_design`, `environment_requirements`, and `real_acceptance_plan`.
- Render `high-level-design.md` with revision history, scope/goals, architecture overview, control flow, data flow, data objects, interface contracts, state model, technical decisions, implementation design, real acceptance plan, risks/guardrails, references, at least one Mermaid diagram, structured tables, source artifacts, current design refs, source-backed interface precision, exact invocation boundaries, executable acceptance command, preconditions, expected artifact paths, mechanical checks, and failure criteria.
- Control flow must describe ordered triggers, actors/components, inputs, outputs, interactions, and branch/failure behavior.
- Data flow must describe source, transformation, target, persistence or retention, data refs, and contract refs.
- Data objects must describe fields, meaning, required/optional status where applicable, lifecycle, and contract refs. Each field must be a structured object with `name`, boolean `required`, and `meaning`.
- Interface contracts must describe provider, consumer, exact invocation, inputs, outputs, error semantics, source refs, and contract refs.
- Technical decisions must include rationale and implementation notes.
- Real acceptance plan must name a concrete confirmed real environment, concrete confirmed real data, acceptance command, preconditions, execution steps, expected results, expected artifact paths, mechanical checks, failure criteria, evidence to capture, acceptance owner, `mock_policy=forbidden`, contract refs, and `SRC-*` evidence refs for environment, real data, and acceptance owner.
- Design gates must include separate pass gates with `gate_key` values for `source_readiness`, `control_flow_readiness`, `data_flow_and_object_readiness`, `interface_state_readiness`, `technical_implementation_readiness`, `real_acceptance_readiness`, `hld_document_readiness`, and `task_boundary_readiness`.
- Semantic review must include passing dimensions for source traceability, control flow completeness, data flow and objects, interface precision, technical implementation, executable acceptance, Markdown parity, no untraced invention, and task boundary.
- If Stage 3 lacks environment, real data, permissions, interface docs, deployment constraints, or acceptance ownership, ask the user or produce a blocked HLD with concrete required fixes.

## Forbidden Behavior

- Do not pass a ready HLD with only narrative summary fields.
- Do not pass a ready HLD that is JSON-only, lacks `high-level-design.md`, or renders a thin Markdown summary instead of a formal HLD document.
- Do not omit control flow, data flow, data objects, interface contracts, state model, technical decisions, implementation design, environment requirements, or real acceptance plan.
- Do not use mock, stub, fake, simulated, or synthetic acceptance inputs.
- Do not use deferred acceptance placeholders such as "selected by downstream owner", "supplied later", "to be provided", `TBD`, or placeholders.
- Do not invent technologies, interfaces, data fields, or acceptance steps absent from the contract or unresolved user input.
- Do not hide missing environment or real data behind assumptions.
- Do not replace the fixed HLD design gate taxonomy with one generic pass gate.
- Do not let JSON carry implementation-ready facts that are missing from `high-level-design.md`.
- Do not let HLD self-reported design gates replace independent semantic review.
- Do not include task plans, task graphs, dependency edges, parallel groups, implementation task cards, or work items.

## Scoring Rule

Pass if the final package validator passes, independent semantic review confirms the HLD is implementation-ready with structured control/data/interface/state/technology design, `high-level-design.md` is a formal readable HLD with diagrams, tables, references, current design refs, source-backed interface precision, exact acceptance command, expected artifact paths, mechanical checks, and failure criteria, all material claims trace to canonical refs, the fixed design gate taxonomy and `hld-semantic-review.json` separately pass all required HLD readiness dimensions, real acceptance uses concrete confirmed real environment and real data with `SRC-*` evidence refs and no substitutes or deferred placeholders, and missing HLD-critical information is asked or blocked rather than invented.

## Pass Bar

`pass`
