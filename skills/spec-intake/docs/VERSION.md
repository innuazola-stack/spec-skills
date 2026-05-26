# Version

## Date

2026-05-26

## Target Dev Root

`skills/spec-intake`

## Current Version

`0.1.0`

## Summary

Initial repository-local implementation of the `spec-intake` skill.

## Notable Changes

- Added runtime skill package.
- Added intake, output, task, and quality references.
- Added structural validator script.
- Added no-dependency skill package validator because the system `quick_validate.py` requires unavailable `yaml`.
- Added blocked Agent PRD fixture.
- Hardened output-package validation for full contract sections, dangling references, render gates, Agent PRD readiness, task graph integrity, and required intake notes.
- Added positive, negative, and boundary semantic eval case files.
- Added validator regression probes for execution readiness false positives, task-plan envelope gaps, non-canonical IDs, and missing render-block coverage.
- Added ready task-plan fixture and hardened planning validation for canonical source readiness, current-phase coverage, dependency graph consistency, enum values, and top-level contract ref types.
- Added semantic eval record for positive, negative, and boundary cases.
- Hardened schema validation for object status enums, payload refs, render-block source refs, task typed refs, contract summary drift, and added negative/boundary snapshot packages.
- Hardened derived consistency validation for task-plan source artifacts, quality gate reports, traceability summaries, decision refs, and planning gate evidence refs.
- Hardened the output contract as the unique canonical truth: required full top-level contract views, `document_metadata`, `next_actions`, and exact `object_index` derivation from `objects`.
- Added source-fact auditability checks for `SRC-*` payloads and a closed `source_type` vocabulary.
- Added readiness-blocker validation for blocked `CORE-*` facts, current-phase `REQ-*` facts, triggered `STOP-*` conditions, and blocking open or missing-status `Q-*` / `ASM-*` decisions.
- Added typed traceability validation for open questions, assumptions, and user confirmations.
- Aligned task decomposition validation with design vocabulary: task statuses, `serial` parallel groups, contract-backed planning, and rendered-only blocked diagnostic plans.
- Required Agent PRD Data and State coverage.
- Hardened current-phase handling: ready plans require canonical current phase requirements, reject future-phase task refs, and no longer fall back from missing current-phase requirements to all requirements.
- Hardened derived view consistency: top-level contract views must match `objects`, and `GATE-*` payloads must match `gate_report` rows.
- Hardened task closure validation for task type, ready-plan task status, closure field non-emptiness, stage goal refs, dependency edge contract refs, and planning evidence.
- Hardened audit validation for ISO `source_idea.created_at`, resolved decision evidence, and `TRACE.relation` vocabulary.

## Compatibility Notes

Designed for Codex skill layout. External installation may require copying `skills/spec-intake/skill` into the active skills directory.
