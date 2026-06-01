# Spec Intake Release Checklist

## Date

2026-05-26

## Target Dev Root

`skills/spec-intake`

## Target Docs Path

`skills/spec-intake/docs`

## Release Goal

Prepare a repository-local skill package that can later be copied or packaged for Codex skill installation.

## Public Surface Checks

- `manifest.yaml` declares `kind: harness-workflow`, the Codex adapter entry, eval case directory, and validators.
- Portable core files exist: `agent.md`, `workflow.md`, `rules.md`, and `schemas/contract-envelope.schema.md`.
- Codex adapter files exist under `adapters/codex/`.
- Canonical eval cases exist under `evals/cases/`.
- `SKILL.md` frontmatter contains only `name` and `description`.
- Trigger covers idea intake, PRD creation, and HLD.
- References are linked directly from `SKILL.md`.

## Validation Checks

- No-dependency skill package validator passes.
- Source harness validator passes.
- Source harness regression probes pass.
- Harness release builder `tools/build_release.py` passes.
- Blocked fixture validator passes.
- Ready fixture validator passes.
- Negative snapshot validator passes.
- Boundary snapshot validator passes.
- Validator regression probes pass.
- Derived consistency probes reject drift between contract summaries, object indexes, gate reports, source artifacts, traceability summaries, readiness blockers, and HLD evidence refs.
- Top-level contract views match canonical `objects`; no canonical object may hide outside its view.
- `GATE-*` payloads match `gate_report` rows for status, blocking, affected targets, and evidence refs.
- Source facts are auditable: user input, user documents, and confirmations carry captured content or target payload.
- Human PRD, Agent PRD, and HLD readiness is blocked by blocked current-phase facts, triggered stop conditions, unresolved blocking questions or assumptions, blocked gates, invalid warning gates, or missing HLD source evidence.
- Agent PRD validation requires Data and State coverage.
- HLD source artifacts, required design sections, design gates, and forbidden legacy task-plan outputs match `references/hld-design.md`.
- Lifecycle artifact validator passes.
- Eval case files under `evals/cases/` cover positive, negative, and boundary prompts with scoring rules and pass bars.
- Semantic eval record exists with verdicts, evidence, and caller consumption rule.
- No visible mojibake in runtime, adapter, source, or eval files.

## Packaging Or Distribution Steps

Run `tools/build_release.py` from `skills/spec-intake`. It emits source and Codex runtime zips under `dist/`, then writes `dist/release-manifest.yaml` with relative artifact paths and SHA-256 checksums.

## Release Notes Status

Release notes are recorded in `releases/1.0.0.md`.

## Ship Decision

Repository-local usable after validation passes; external release remains pending packaging.
