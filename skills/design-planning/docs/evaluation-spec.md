# Evaluation Spec

## Exact Review Query

```text
Use design-planning on this Rust target project. Read PRD/HLD under ./docs and produce harness-governed design planning. The planning must include staged review results, a DAG and task list as JSON, per-task fixtures containing prompt.md, CLAUDE.md, and AGENTS.md, exact docs/design design_doc_path values, and one final design acceptance task.
```

## Positive Case

Input: A Rust target project has `docs/prd.md` and `docs/hld.md` with current-phase requirements, architecture, data flow, interfaces, acceptance, and Rust stack.

Expected behavior:

- Inventories PRD/HLD sources.
- Writes `<planning-output-root>/design-planning.json`.
- Writes `docs/design/rust-implementation-design.md`.
- Records `planning_review_stages` for overall planning, task formation, single-task review, global DAG review, artifact generation, and final design acceptance.
- Produces documentation-only `detailed_design` tasks, each with one exact `docs/design/*.md` `design_doc_path`.
- Produces one `design_acceptance` task that depends on every detailed design task.
- Writes per-task `prompt.md`, `AGENTS.md`, and `CLAUDE.md`.
- Passes `validators/validate_design_planning.py`.

Forbidden behavior:

- Markdown-only task planning.
- Implementation/code-writing tasks.
- Missing exact design document paths.
- Missing final design acceptance task.
- Standalone starter prompt template output.

## Negative Case

Input: Target project has no HLD or has an HLD without Rust stack or interface details.

Expected behavior:

- Writes blocked planning JSON.
- Lists missing HLD/Rust/interface decisions as required fixes.
- Does not fabricate a ready DAG.
- Does not emit ready task fixtures that depend on missing facts.
- Does not create implementation code.

Forbidden behavior:

- Ready `detailed_design` tasks based on invented facts.
- Any final acceptance task that approves incomplete design evidence.

## Boundary Case

Input: PRD/HLD exists but includes a future-phase feature request.

Expected behavior:

- Keeps current-phase DAG clean.
- Defers future-phase work unless explicitly required as preparation.
- Records source-backed defer rationale.

Forbidden behavior:

- Future-phase task nodes in the current-phase DAG without explicit PRD/HLD preparation evidence.
- Dependency edges from current tasks to deferred future-phase tasks.

## Developer-Misinterpretation Case

Input: The executor tries to treat a generated task fixture as an implementation task.

Expected behavior:

- Fixture says `Do not implement code`.
- Fixture forbids modifying source, tests, manifests, schemas, migrations, runtime scripts, and generated runtime artifacts.
- Fixture names exactly one detailed design document under `docs/design/`.

Forbidden behavior:

- Commands such as `cargo test` presented as work to execute during design.
- Handoff text asking for implementation files changed.

## Scoring Rule

Score each applicable dimension as:

- `2`: explicit, enforced, and evidenced.
- `1`: present but incomplete or weakly evidenced.
- `0`: missing, contradicted, or unsafe.

Dimensions:

1. PRD/HLD source inventory and reading discipline.
2. Harness-stage output with `planning_review_stages`.
3. JSON planning shape with `tasks`, `dag`, `fixtures`, and gates.
4. DAG edge reasons and acyclicity.
5. Per-task fixture completeness.
6. Documentation-only task enforcement.
7. Exact `docs/design/*.md` design document paths.
8. Final `design_acceptance` task correctness.
9. Rust detailed design coverage.
10. Blocked behavior for missing evidence.
11. Validator coverage and pass evidence.
12. No standalone starter prompt template.

## Pass bar

- Total score at least 22 of 24.
- No dimension may score `0`.
- Dimensions 2, 3, 4, 6, 8, and 11 must each score `2`.
