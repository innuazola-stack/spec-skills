---
name: development-planning
description: Use when Codex should run the development-planning harness workflow for a target project with PRD/HLD/LLD under docs, producing planning-only task contracts under tasks/development with a validated DAG and final delivery acceptance task.
---

# Development Planning Codex Adapter

This adapter maps Codex runtime behavior to the portable `development-planning` harness.

## Read First

1. `manifest.yaml`
2. `agent.md`
3. `workflow.md`
4. `rules.md`
5. `schemas/development-planning.schema.json`
6. `skill/SKILL.md`

## Runtime Contract

Use the portable harness stages exactly:

1. Overall planning
2. Independent task formation
3. Task logic and completeness review
4. Whole-plan integrity and dependency review

Write planning outputs under `tasks/development` unless the user explicitly requests another root.

Do not implement product code. This adapter only plans future development work and writes task contracts plus execution support files.

## Validation

Before claiming the harness source is ready, run:

```bash
python validators/validate_harness.py
```

Before claiming a generated target planning package is ready or honestly blocked, run:

```bash
python validators/validate_development_planning_package.py <target-root-or-output-root>
```
