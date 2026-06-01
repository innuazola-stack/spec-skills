# File Plan

## Harness Core Files

- `manifest.yaml`: harness metadata, required files, adapters, and done criteria.
- `agent.md`: portable role, inputs, outputs, and completion criteria.
- `workflow.md`: review-gated stage graph and gate contracts.
- `rules.md`: authority, file, no-code, task, final acceptance, and validation rules.
- `schemas/design-planning.schema.json`: machine-readable planning output shape.
- `validators/validate_design_planning.py`: target output validator.
- `validators/validate_harness.py`: source harness structure validator.
- `tools/build_release.py`: source/runtime release builder.
- `releases/<version>.md`: release note for each packaged harness version.

## Adapter Files

- `adapters/codex/system-prompt.md`, `install.md`, `mapping.md`.
- `adapters/claude/CLAUDE.md`, `install.md`, `mapping.md`.
- `adapters/gemini/GEMINI.md`, `install.md`, `mapping.md`.
- `adapters/openclaw/OPENCLAW.md`, `install.md`, `mapping.md`.
- `adapters/hermas/HERMAS.md`, `install.md`, `mapping.md`.

## Runtime Skill Compatibility Files

- `skill/SKILL.md`: main skill entrypoint, workflow, hard rules, gates, mistakes.
- `skill/references/methodology.md`: method, boundaries, DAG rules, blocker criteria.
- `skill/references/rust-detailed-design.md`: Rust-specific design checklist.
- `skill/references/output-contract.md`: JSON planning, task fixtures, and gate report.
- `skill/assets/TASK_PROMPT.fixture.md`: per-task prompt fixture template.
- `skill/assets/AGENTS.template.md`: per-task Codex/general agent instruction fixture template.
- `skill/assets/CLAUDE.template.md`: per-task Claude instruction fixture template.

## Lifecycle And Eval Files

- `docs/design-brief.md`: mission, harness type, non-goals, output contract.
- `docs/file-plan.md`: this file.
- `docs/evaluation-spec.md`: positive, negative, and boundary evaluation cases.
- `docs/test-plan.md`: manual and static validation plan.
- `evals/cases/*.md`: harness eval cases with prompt, expected behavior, forbidden behavior, scoring rule, and pass bar.
- `tests/cases/*.md`: compatibility copies for older local test references.
