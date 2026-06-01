# Design Planning Rules

## Authority Order

1. Latest user instruction
2. Target PRD/HLD and contract artifacts under `<target>/docs`
3. `workflow.md`
4. `agent.md`
5. `schemas/design-planning.schema.json`
6. `skill/SKILL.md` compatibility entrypoint
7. Prior generated planning artifacts

## File Rules

- PRD/HLD inputs are fixed under `<target>/docs`.
- Planning JSON and task fixtures use `<planning-output-root>`.
- Detailed design documents always use `<target>/docs/design`.
- Task fixture directories must be `<planning-output-root>/fixtures/<TASK-ID>/`.
- Every task must have `prompt.md`, `AGENTS.md`, and `CLAUDE.md`.
- Do not create standalone starter prompt templates.

## No-Code Rule

Design planning tasks must not modify:

- product source files
- tests
- build manifests
- schemas or migrations
- runtime scripts
- generated runtime artifacts

The only allowed generated artifacts are planning JSON, design documents, fixtures, validation reports, and review notes.

## Task Rules

- Every detailed design task has `task_type=detailed_design`.
- Every detailed design task has one exact `docs/design/*.md` `design_doc_path`.
- Every task fixture must say `Do not implement code`.
- Every task fixture must name the exact design document path.
- Verification commands may be proposed inside a design document, but the design task must not run them as implementation proof.

## Final Acceptance Rule

Ready planning must include exactly one final task with `task_type=design_acceptance`.

The final acceptance task must:

- depend on every `detailed_design` task
- write an acceptance report under `docs/design/`
- check the complete design document set for good detailed design quality
- forbid code/test/manifest/schema/migration/runtime changes

## Validation Rule

Run `validators/validate_design_planning.py` against generated planning before claiming readiness.

Validation failure blocks completion.
