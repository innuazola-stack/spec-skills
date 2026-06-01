# Detailed Design Task Prompt: {{TASK_ID}} {{TASK_TITLE}}

You are working on a single documentation-only detailed design task from the target Rust project's design plan.

Do not implement code. Do not modify production source files, tests, build manifests, schemas, migrations, runtime scripts, or generated runtime artifacts.

## Mission

Complete only `{{TASK_ID}}`: `{{TASK_TITLE}}`.

Your only deliverable is the detailed design document named below:

- `{{DESIGN_DOC_PATH}}`

## Read First

- PRD/HLD refs: `{{SOURCE_REFS}}`
- Planning JSON: `<planning-output-root>/design-planning.json`
- Rust design: `docs/design/rust-implementation-design.md`
- Task fixture: `<planning-output-root>/fixtures/{{TASK_ID}}/`

## Scope

Allowed scope:

{{ALLOWED_SCOPE}}

Forbidden scope:

{{FORBIDDEN_SCOPE}}

## Expected Outputs

{{EXPECTED_OUTPUTS}}

The document must be saved exactly at `{{DESIGN_DOC_PATH}}`. Any additional detailed design document created or updated while completing this task must also be saved under `docs/design/`.

## Review Checks

{{VERIFICATION}}

## Stop Conditions

{{STOP_CONDITIONS}}

## Handoff

Report the detailed design document path, review checks performed, unresolved design risks, and any design mismatch that requires updating the planning output or `docs/design/`. Do not report implementation files because this task must not change them.
