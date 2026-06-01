# Optimization Plan

## Current State

The harness workflow meets the requested contract:

- PRD/HLD input under target `docs/`.
- Planning output as JSON.
- JSON includes DAG and task list.
- Each ready task has independent fixture files: `prompt.md`, `AGENTS.md`, and `CLAUDE.md`.
- Runtime adapters, eval cases, source validation, target-output validation, and release validation are present.

## Follow-Up Hardening

1. Maintain the JSON Schema for `<planning-output-root>/design-planning.json`.
2. Add fixture snapshot examples for one positive target project.
3. Add an agentic evaluation where a fresh agent consumes one task fixture and reports whether the scope is sufficient.
4. Add release CI wiring around `tools/build_release.py --check`.

## Not In Scope

- Implementing Rust product code.
- Generating standalone starter prompts.
