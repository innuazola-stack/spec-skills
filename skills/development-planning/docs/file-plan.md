# File Plan

## Runtime Skill Files

- `manifest.yaml`: harness identity, canonical stages, validators, adapters, and done requirements.
- `agent.md`: portable mission, role boundary, operating defaults, and completion criteria.
- `workflow.md`: canonical four-stage workflow and gates.
- `rules.md`: authority, artifact, stage, DAG, validation, and done rules.
- `schemas/development-planning.schema.json`: structural output contract for planning artifacts.
- `validators/validate_harness.py`: source-package validator for harness files, schema, evals, and adapter.
- `adapters/codex/SKILL.md`: Codex adapter entrypoint.
- `adapters/codex/mapping.md`: mapping from portable harness contract to Codex runtime skill files.
- `skill/SKILL.md`: main skill entrypoint, workflow, hard rules, gates, mistakes.
- `skill/references/methodology.md`: method, boundaries, DAG rules, blocker criteria, task cohesion, and final acceptance task design.
- `skill/references/output-contract.md`: JSON planning, task descriptions, task fixtures, and gate report.
- `skill/references/planning-quality-model.md`: harness-style staged planning and review model.
- `skill/assets/TASK_DESCRIPTION.template.md`: per-task `task.md` delivery contract template.
- `skill/assets/TASK_PROMPT.fixture.md`: per-task prompt support template.
- `skill/assets/AGENTS.template.md`: per-task Codex/general agent instruction fixture template.
- `skill/assets/CLAUDE.template.md`: per-task Claude instruction fixture template.

## Lifecycle Files

- `docs/design-brief.md`: mission, skill type, non-goals, output contract.
- `docs/file-plan.md`: this file.
- `docs/evaluation-spec.md`: positive, negative, and boundary evaluation cases.
- `docs/test-plan.md`: manual and static validation plan.
