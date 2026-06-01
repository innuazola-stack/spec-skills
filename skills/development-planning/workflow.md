# Development Planning Workflow

## Harness Type

`development-planning` is a review-gated branching/DAG planning harness.

It is a harness workflow because success depends on ordered stages, gate artifacts, task handoffs, a validated DAG, and parent-consumable planning verdicts.

## Stage 1: Overall Planning

Input:

- target project root
- PRD/HLD/LLD and related documents under `docs/`
- optional read-only source evidence for stack, commands, and local conventions

Actions:

- inventory source documents
- inventory structured contract documents such as `docs/contract-envelope.json` when present
- identify current delivery phase, product goals, scope, non-goals, acceptance surface, risks, and dependency axes
- identify missing or contradictory facts that block planning
- create the whole-plan outline before writing task contracts

Output:

- `phase_reports[]` entry for `STAGE-001`
- `source_inventory`
- `prd_hld_lld_interpretation`
- `development_scope`
- `project_stack`
- structured contract sources under `docs` are present in `source_inventory`

Gate:

- pass when PRD/HLD/LLD evidence supports a whole-plan outline
- blocked when current phase, stack, architecture, interface, acceptance, or delivery scope is missing or contradictory

## Stage 2: Independent Task Formation

Input:

- Stage 1 whole-plan outline
- source inventory and interpretation

Actions:

- decompose future development work into cohesive tasks
- define task IDs, task types, source refs, inputs, expected outputs, impacted areas, allowed scope, forbidden scope, acceptance, verification, stop conditions, dependencies, and handoff requirements
- add exactly one final `delivery_acceptance` task after all non-deferred implementation tasks

Output:

- `phase_reports[]` entry for `STAGE-002`
- `tasks[]`
- `task_descriptions[]`
- `fixtures[]`

Gate:

- pass when every task is independently acceptable and source-backed
- blocked when any task cannot be isolated or accepted without inventing missing facts

## Stage 3: Task Logic And Completeness Review

Input:

- all task contracts from Stage 2

Actions:

- review every task for cohesion, independent acceptance, source traceability, boundary clarity, verification sufficiency, stop condition sufficiency, handoff completeness, and dependency input clarity
- revise weak tasks or block the plan

Output:

- `phase_reports[]` entry for `STAGE-003`
- `task_logic_review`

Gate:

- pass when `task_logic_review.status=pass` and there are no blocking findings
- blocked when any task is too broad, untraceable, unverifiable, boundary-weak, or unable to hand off useful outputs

## Stage 4: Whole-Plan Integrity And Dependency Review

Input:

- reviewed task contracts
- coverage matrix
- reverse requirement coverage matrix when sources contain explicit requirement or acceptance IDs
- DAG nodes, edges, parallel groups, and execution order

Actions:

- build and review the DAG
- verify current-phase requirement, output, acceptance, and verification coverage
- verify every explicit source requirement or acceptance ID maps to tasks, final delivery acceptance, verification, and evidence
- verify acyclicity and topological execution order
- verify every edge has a semantic reason and consumed output
- verify parallel groups are dependency-free and conflict-free, including no direct or transitive dependency path among group members
- verify the final delivery acceptance task is last and depends on all non-deferred implementation tasks
- verify deferred and future-phase work does not leak into current-phase implementation

Output:

- `phase_reports[]` entry for `STAGE-004`
- `dag`
- `coverage_matrix`
- `requirement_coverage_matrix`
- `delivery_acceptance`
- `plan_integrity_review`
- `planning_gate_report`

Gate:

- pass when `plan_integrity_review.status=pass`, DAG is valid, coverage is complete, final acceptance is correct, and no blocking findings remain
- blocked when coverage gaps, cyclic dependencies, unsafe parallelism, invalid execution order, or weak final acceptance remain

## Blocked Planning Route

When any stage is blocked:

- write `development-planning.json` with `planning_status=blocked`
- keep executable `tasks`, DAG nodes, edges, parallel groups, execution order, task descriptions, and fixtures empty unless partial diagnostic output is explicitly safe
- include `required_fixes`
- include phase reports and review objects that explain the blocker
- do not emit ready task folders

## Handoff

The final handoff must state:

- planning package path
- planning status
- source validator command and verdict when the harness source package was changed
- generated package validator command and verdict when a planning package was produced
- ready or blocked stage
- final delivery acceptance task ID when ready
- unresolved risks or required fixes
