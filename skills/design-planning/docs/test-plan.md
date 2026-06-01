# Test Plan

## Static Checks

- `skill/SKILL.md` has valid frontmatter with `name: design-planning`.
- Harness core files exist: `manifest.yaml`, `agent.md`, `workflow.md`, `rules.md`.
- Schema exists: `schemas/design-planning.schema.json`.
- Validator exists: `validators/validate_design_planning.py`.
- Output contract mentions `planning_review_stages`, `design_doc_path`, `design_acceptance`, `AGENTS.md`, and `CLAUDE.md`.
- No standalone starter prompt template file exists.

Run:

```bash
python skills/design-planning/tools/validate_skill_static.py
```

## Real Output Validation

Run the validator against a generated target:

```bash
python skills/design-planning/validators/validate_design_planning.py --project-root C:\Users\54256213\Documents\github\spec-scheduler --planning-json C:\Users\54256213\Documents\github\spec-scheduler\tasks\design\design-planning.json
```

Expected:

```text
PASS: design planning output validation
```

## Manual Pressure Scenarios

1. Missing HLD pressure: verify readiness blocks instead of inventing Rust architecture.
2. Starter-prompt-template pressure: verify no standalone starter prompt template is created.
3. Implementation pressure: verify fixtures require documentation-only work and exact `docs/design/*.md` deliverables.
4. Thin DAG pressure: verify each dependency edge has a semantic reason.
5. Missing acceptance pressure: verify validator fails when no `design_acceptance` task exists.
6. Stale wording pressure: verify validator fails when fixtures contain implementation-task wording.

## Acceptance

The harness is ready when:

- static checks pass
- real output validation passes
- review confirms staged gates, task formation, DAG review, artifact generation, and final design acceptance are all represented in `design-planning.json`
- semantic review has no blocker
