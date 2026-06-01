# Development Planning Rules

## Authority

1. Latest user instruction
2. PRD/HLD/LLD files under target `docs/`
3. Structured contract sources under target `docs/`, including `contract-envelope.json` when present
4. Existing target source files as read-only convention evidence
5. Bounded inference from cited facts
6. Assumptions, open questions, and deferred items

Lower authority may not overwrite higher authority. Assumptions and open questions never become ready facts.

## Planning-Only Boundary

- Do not implement product code.
- Do not modify product source files, tests, manifests, schemas, migrations, or runtime scripts as part of planning.
- Do not claim software delivery has happened.
- Task files describe future work only.

## Artifact Rules

- Default output root is `tasks/development`.
- `development-planning.json` is the canonical planning artifact.
- Each ready task must have `tasks/development/<TASK-ID>/task.md`.
- Each ready task must have `prompt.md`, `AGENTS.md`, and `CLAUDE.md` in the same task folder.
- Ready plans must include exactly one `delivery_acceptance` task.
- Ready plans must include `requirement_coverage_matrix` when source docs contain explicit requirement or acceptance IDs such as `FR-001` or `AC-001`.
- Blocked plans must not emit executable task contracts unless partial diagnostic output is explicitly safe.

## Stage Rules

- `phase_reports` must include exactly the canonical stages:
  - `STAGE-001`
  - `STAGE-002`
  - `STAGE-003`
  - `STAGE-004`
- Ready plans require every stage to pass.
- Ready plans require `task_logic_review.status=pass`.
- Ready plans require `plan_integrity_review.status=pass`.
- Failed stage gates must produce blockers and required fixes.

## DAG Rules

- The DAG must be acyclic.
- `dag.execution_order` must be a valid topological order.
- Every edge must include `from`, `to`, `reason`, `consumed_output`, and `source_refs`.
- Parallel groups must not contain direct/transitive dependency paths or conflicts over files, schemas, migrations, interfaces, state, test evidence, or acceptance artifacts.
- The final `delivery_acceptance` task must depend on every non-deferred implementation task and be last in execution order.

## Validation Rules

- Run `validators/validate_harness.py` before claiming the harness source package is ready.
- Run `validators/validate_development_planning_package.py <target-root-or-output-root>` before claiming any generated development planning package is ready or honestly blocked.
- A failed validator blocks ready status.
- Semantic review can downgrade a structurally valid plan when task meaning, coverage, or dependency reasoning is weak.

## Done Rule

Do not claim completion unless the final answer reports validator evidence and any remaining risks.
