# Test Plan

## Static Checks

- `manifest.yaml` declares `kind: harness-workflow`.
- Top-level `agent.md`, `workflow.md`, `rules.md`, schema, validator, evals, and Codex adapter exist.
- Generated planning package validator exists and validates ready and blocked fixture packages.
- `SKILL.md` has valid frontmatter with `name: development-planning`.
- Description starts with `Use when`.
- Output contract mentions `tasks/development/development-planning.json`, task descriptions, `task.md`, `AGENTS.md`, and `CLAUDE.md`.
- References cover methodology, output contract, and harness-style planning quality model.
- No standalone starter prompt template file exists in the skill.
- Static text includes planning-only scope, staged planning rigor, task cohesion, independent acceptance, task logic review, plan integrity review, final delivery acceptance task, DAG, and execution order requirements.

Run:

```bash
python validators/validate_harness.py
python validators/validate_development_planning_package.py tests/fixtures/ready-package
python validators/validate_development_planning_package.py tests/fixtures/blocked-package
python tools/validate_skill_static.py
```

Negative validator fixtures must fail:

```bash
python validators/validate_development_planning_package.py tests/fixtures/invalid-duplicate-execution-order
python validators/validate_development_planning_package.py tests/fixtures/invalid-declared-path
```

The harness source validator runs these negative fixtures and fails if either invalid package is accepted.

## Manual Pressure Scenarios

1. Missing HLD/LLD pressure: verify the skill blocks readiness instead of inventing architecture, interfaces, or acceptance.
2. Starter-prompt-template pressure: verify the skill refuses to create a standalone starter prompt template while still creating per-task prompt fixtures.
3. Implementation pressure: verify the skill produces planning, task descriptions, and fixtures only, not product code.
4. Thin DAG pressure: verify each dependency edge has a semantic reason and consumed output.
5. Cohesion pressure: verify broad mixed tasks are split until each task has one responsibility.
6. Acceptance pressure: verify exactly one final delivery acceptance task depends on all non-deferred implementation tasks.
7. Harness-style review pressure: verify the plan records overall planning, independent task formation, task logic review, and whole-plan integrity review before readiness.

## Acceptance

The skill is ready when static checks pass and review confirms the body contains enough specific guidance for a future agent to perform target-project development planning without relying on this conversation.

Evaluation pass bar is defined in `docs/evaluation-spec.md`: at least 22/24, no zero dimensions, and full score on JSON planning, staged planning rigor, task logic review, plan integrity review, independent acceptance, DAG soundness, task description and fixture completeness, final acceptance, and blocked behavior.
