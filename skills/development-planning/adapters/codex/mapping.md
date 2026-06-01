# Codex Adapter Mapping

## Portable Core To Codex Runtime

| Portable Harness Artifact | Codex Runtime Use |
| --- | --- |
| `manifest.yaml` | Declares harness identity, canonical stages, validators, adapter entry, and done requirements. |
| `agent.md` | Defines mission, role boundary, defaults, and completion criteria. |
| `workflow.md` | Defines the stage sequence and gates Codex must follow. |
| `rules.md` | Defines authority, planning-only boundary, artifact rules, stage rules, DAG rules, and done rule. |
| `schemas/development-planning.schema.json` | Defines the generated planning artifact shape. |
| `validators/validate_harness.py` | Validates the harness source package. |
| `validators/validate_development_planning_package.py` | Validates generated `tasks/development` planning packages. |
| `skill/SKILL.md` | Runtime skill entry used by Codex skill loading. |
| `skill/assets/*.md` | Templates for task contracts and task-scoped execution support files. |

## Unsupported Runtime Behavior

- This adapter does not execute planned development tasks.
- This adapter does not perform product release.
- This adapter does not provide live E2E product evidence.
- This adapter does not introduce approval gates beyond blocked/ready planning verdicts.

## Handoff

Codex final responses must report:

- planning package path
- planning status
- validator evidence when source validation was run
- generated planning package validator evidence when a package was produced
- final delivery acceptance task ID for ready plans
- blockers, required fixes, or residual risks
