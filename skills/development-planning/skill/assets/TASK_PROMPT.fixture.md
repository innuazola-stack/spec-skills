# Development Task Prompt: {{TASK_ID}} {{TASK_TITLE}}

You are working from a single planned development task from the target project's development plan.

## Mission

Complete only `{{TASK_ID}}`: `{{TASK_TITLE}}`.

## Read First

- PRD/HLD/LLD refs: `{{SOURCE_REFS}}`
- Planning JSON: `<planning-output-root>/development-planning.json`
- Task description: `<planning-output-root>/{{TASK_ID}}/task.md`
- Task fixture: `<planning-output-root>/{{TASK_ID}}/`

## Scope

Allowed scope:

{{ALLOWED_SCOPE}}

Forbidden scope:

{{FORBIDDEN_SCOPE}}

## Expected Outputs

{{EXPECTED_OUTPUTS}}

## Acceptance Criteria

{{ACCEPTANCE}}

## Verification

{{VERIFICATION}}

## Stop Conditions

{{STOP_CONDITIONS}}

## Handoff

Report the task ID, changed files or areas, verification performed, acceptance status, dependency outputs for downstream tasks, and unresolved risks or blockers. Do not perform work from other task IDs.
