---
name: spec-intake
description: Run the Codex adapter for the spec-intake harness workflow.
---

# Spec Intake Codex Adapter

This adapter maps the portable `spec-intake` harness to Codex skill runtime behavior. The installable runtime copy is `skill/SKILL.md`; this file is the source adapter entry that must preserve the same workflow semantics.

Codex execution must:

- load `agent.md`, `workflow.md`, and `rules.md` as the portable core semantics when reviewing or changing the harness
- use `skill/references/intake-method.md` for Stage 1 requirement-table intake
- use `skill/references/prd-rendering.md` and `skill/references/prd-quality-reference.md` for Stage 2 `prd-writer` delegation, PRD quality calibration, and PRD brief review
- use `skill/references/output-artifacts.md` for contract, PRD, and HLD output rules
- use `skill/references/hld-design.md` only after PRD review approval; Stage 3 must delegate HLD generation to `hld-writer`, and ready HLD must be structured implementation design with real-environment, real-data acceptance and no mock substitutes
- use `skill/references/quality-gates.md` before claiming readiness
- run `skill/scripts/validate_spec_intake_package.py <output-dir>` for generated packages
- run `skill/scripts/validate_skill_package.py skill` and regression suites when changing the harness source

The adapter must not weaken the portable workflow: Stage 1 must record `contract-envelope.json.interaction_decision`, PRD review approval remains a hard Stage 3 gate, Stage 1 clarification questions remain closed-form, every generated artifact remains derived from `contract-envelope.json.requirement_table`, Stage 2 must not emit legacy `human-prd.md` or `agent-prd.md`, ready Stage 2 and Stage 3 must include `writer_invocations` evidence, ready HLD requires structured implementation design and real acceptance, and task-plan output remains forbidden.
