# Spec Intake File Plan

## Date

2026-05-26

## Target Dev Root

`skills/spec-intake`

## Target Skill Source Path

`skills/spec-intake/skill`

## Planned SKILL.md Shape

Frontmatter with `name` and `description`, followed by default workflow, references, hard rules, output package shape, and completion check.

## Planned agents/openai.yaml Alignment

UI metadata mirrors the trigger: raw idea to contract-backed Human PRD, Agent PRD, and execution tasks.

## Planned references/ Files

- `intake-method.md`
- `output-artifacts.md`
- `task-decomposition.md`
- `quality-gates.md`

## Planned scripts/ Files

- `validate_spec_intake_package.py`
- `validate_skill_package.py`

## Planned assets/ Files

None for initial version.

## Planned Lifecycle Artifacts

Design brief, file plan, evaluation spec, implementation plan, test plan, release checklist, and version record.

## Planned Validators Or Reviewers

Structural output-package validator, no-dependency skill-package validator, and semantic quality-gate rubric.

## Planned Loop Artifacts

Blocked and ready fixture packages under `tests/fixtures/`, semantic eval cases under `tests/cases/`, semantic eval record under `tests/snapshots/`, validator regression probes in `tests/validator_regression.py`, and future live-run snapshots under `tests/snapshots/`.

## UTF-8 Policy

All runtime and test files must be UTF-8.

## Subproblem-To-Owner Mapping

Thinking owns meaning. Scripts own structure and parseability.

## Recommended Implementation Order

Write runtime skill, write references, add validator, add fixtures, run validation, then review lifecycle artifacts.
