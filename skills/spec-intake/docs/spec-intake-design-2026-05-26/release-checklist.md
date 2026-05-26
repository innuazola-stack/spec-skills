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

- `SKILL.md` frontmatter contains only `name` and `description`.
- Trigger covers idea intake, PRD creation, and task planning.
- References are linked directly from `SKILL.md`.

## Validation Checks

- No-dependency skill package validator passes.
- Blocked fixture validator passes.
- Ready fixture validator passes.
- Negative snapshot validator passes.
- Boundary snapshot validator passes.
- Validator regression probes pass.
- Derived consistency probes reject drift between contract summaries, object indexes, gate reports, source artifacts, traceability summaries, readiness blockers, and planning evidence refs.
- Top-level contract views match canonical `objects`; no canonical object may hide outside its view.
- `GATE-*` payloads match `gate_report` rows for status, blocking, affected targets, and evidence refs.
- Source facts are auditable: user input, user documents, and confirmations carry captured content or target payload.
- Human PRD, Agent PRD, and task plan readiness is blocked by blocked current-phase facts, triggered stop conditions, unresolved blocking questions or assumptions, blocked gates, invalid warning gates, or rendered-only planning.
- Agent PRD validation requires Data and State coverage.
- Task-plan phase integrity, closure fields, status vocabulary, task type vocabulary, parallel group status vocabulary, and planning source modes match `references/task-decomposition.md`.
- Lifecycle artifact validator passes.
- Eval case files cover positive, negative, and boundary prompts.
- Semantic eval record exists with verdicts, evidence, and caller consumption rule.
- No visible mojibake in runtime files.

## Packaging Or Distribution Steps

Not packaged in this turn. Future release can copy `skill/` into a skill install location or build a zip under `dist/`.

## Release Notes Status

Initial implementation; no external release notes yet.

## Ship Decision

Repository-local usable after validation passes; external release remains pending packaging.
