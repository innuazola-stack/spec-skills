# Methodology

## Boundary

This skill serves target projects that already have PRD/HLD material under `docs/`. It prepares the project for development by producing canonical JSON design planning, Rust detailed design documentation, and per-task execution fixtures.

It does not implement product code, generate PRD/HLD, or create standalone starter prompt templates. Per-task prompt files are allowed only inside task fixture folders. If PRD/HLD is missing or too thin, produce a blocked design planning JSON with required fixes.

The default planning output root is `tasks/design`. If the user explicitly names another planning output root, use that root consistently and record it in the planning JSON as `output_root`. All detailed design documents are fixed under target `docs/design/`, even when planning fixtures are written elsewhere.

## Method

Use harness-style staged gates:

1. Overall planning stage:
   - Inventory `docs/` sources.
   - Read PRD/HLD for scope, current phase, Rust technology stack, architecture, control flow, data flow, interfaces, data/state model, acceptance, risks, and non-goals.
   - Verify local Rust conventions from project source only when needed.
   - Extract design obligations.
2. Overall planning gate:
   - Check source readiness, requirement coverage, current-phase boundary, non-goals, Rust stack evidence, and blockers before forming tasks.
3. Independent task formation stage:
   - Decompose obligations into independently reviewable documentation-only design sub-tasks.
   - Assign each task one exact detailed design document path under `docs/design/`.
4. Single-task review gate:
   - Check every task for single-document deliverability, source refs, inputs, allowed/forbidden scope, review checks, stop conditions, and no-code constraints.
5. DAG and global completeness stage:
   - Build an acyclic DAG with explicit edge reasons.
   - Complete Rust-oriented software engineering design for control flow, data flow, key technical choices, and implementation readiness.
6. Global DAG/completeness gate:
   - Check missing obligations, duplicate ownership, hidden dependencies, invalid parallelism, incorrect dependency direction, and final acceptance coverage.
7. Artifact generation stage:
   - Write `<planning-output-root>/design-planning.json` containing `planning_status`, `output_root`, `detailed_design_root`, staged review results, DAG, task list, fixtures index, coverage, dependencies, and gates.
   - Write Rust detailed design docs under `docs/design/`.
   - Write per-task fixtures under `<planning-output-root>/fixtures/<TASK-ID>/`, and make each fixture explicitly require any detailed design documents created or updated by the task to be saved under `docs/design/`.
8. Final design acceptance stage:
   - Add a final design acceptance task after all detailed design tasks. It reviews the completed document set against good detailed design criteria and writes a named acceptance report under `docs/design/`.
9. Final planning review gate:
   - Self-review for traceability, no-new-facts, DAG soundness, task fixture readiness, Rust readiness, final acceptance task readiness, and blocked decisions.

## Detailed Design Sub-Task Criteria

Each sub-task must be a documentation-only detailed design task and include:

- task ID
- title
- design type
- source refs
- inputs consumed
- outputs produced
- allowed scope
- forbidden scope
- acceptance criteria
- verification method
- stop conditions
- dependencies
- exact detailed design document path under `docs/design/`
- fixture directory
- single-task prompt path
- task `AGENTS.md` path
- task `CLAUDE.md` path

The task title, scope, outputs, acceptance, verification, and fixtures must use design-document language. Do not describe the task as implementation, coding, wiring, scaffolding, or running tests. Commands may be mentioned only as proposed verification in the design document, not as work the design task should execute.

## Final Design Acceptance Task

The final acceptance task must depend on every detailed design document task and must verify:

- all planned detailed design documents exist under `docs/design/`
- every document traces claims to PRD/HLD, contract, source evidence, or explicit open questions
- every current-phase requirement and acceptance criterion is covered or explicitly deferred/blocked
- control flow and data flow are complete and consistent across documents
- Rust module/trait/type boundaries, interface contracts, state/persistence, error handling, security/permissions, observability, and verification strategy are sufficiently precise for implementation
- DAG dependencies and document handoffs are consistent
- no task modified product code, tests, manifests, schemas, migrations, runtime scripts, or generated runtime artifacts
- risks, blockers, and external dependencies are explicit

## DAG Rules

- No cycles.
- Edge reasons must be semantic.
- Parallel groups require no dependency path and no conflict over files, schemas, interfaces, state, decisions, or acceptance evidence.
- Future-phase PRD/HLD work must not enter current-phase design unless explicitly required.

## Blockers

Block readiness when:

- PRD or HLD is absent.
- Rust technology stack is missing or contradictory.
- Control flow, data flow, state, interface, data object, or acceptance evidence is too thin to design.
- Interface documentation, permission model, deployment environment, or real acceptance data is required but absent.
- A requested task would require inventing product facts or implementation scope.
- A task cannot be isolated into a safe single-task execution fixture.
