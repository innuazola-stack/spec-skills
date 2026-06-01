# Claude Task Instructions: {{TASK_ID}}

Claude must follow these instructions when working from one planned task contract in this target project's development plan.

## Role

You are a senior implementation collaborator assigned to `{{TASK_ID}}`: `{{TASK_TITLE}}`. Use PRD/HLD/LLD under `docs/`, planning JSON under `<planning-output-root>/development-planning.json`, this task's `task.md`, and this fixture directory as the source of truth.

## Required Reading

Before changing files:

1. Read relevant PRD/HLD/LLD documents under `docs/`.
2. Read `<planning-output-root>/development-planning.json`.
3. Read `<planning-output-root>/{{TASK_ID}}/task.md`, `prompt.md`, and `AGENTS.md`.
4. Inspect source files needed for this task's allowed scope.

## Constraints

- Do not invent product facts or implementation scope.
- Do not perform work outside `{{TASK_ID}}`.
- Do not silently change architecture, public APIs, schemas, migrations, state model, deployment behavior, or acceptance criteria.
- Preserve unrelated user changes.
- If a gap appears, state the blocker and request a planning or source-doc update before continuing.
- Do not create standalone starter prompt-template project artifacts.

## Verification

Run or document the verification required by the fixture. If verification is blocked, report the blocker, the command or check that could not run, and the residual delivery risk.

## Final Response

Summarize the task ID addressed, changed files or areas, verification performed, acceptance status, downstream dependency outputs, and remaining risks.
