# Version

## Date

2026-05-29

## Target Dev Root

`skills/spec-intake`

## Current Version

`1.0.0`

## Summary

Production-ready release of the `spec-intake` harness workflow and Codex skill adapter.

## Notable Changes

- Added runtime skill package.
- Added intake, output, task, and quality references.
- Added structural validator script.
- Added no-dependency skill package validator because the system `quick_validate.py` requires unavailable `yaml`.
- Added blocked Agent PRD fixture.
- Hardened output-package validation for full contract sections, dangling references, render gates, Agent PRD readiness, HLD integrity, and required intake notes.
- Added positive, negative, and boundary semantic eval case files.
- Added validator regression probes for execution readiness false positives, HLD envelope gaps, non-canonical IDs, and missing render-block coverage.
- Added ready HLD fixture and hardened planning validation for canonical source readiness, current-phase coverage, dependency graph consistency, enum values, and top-level contract ref types.
- Added semantic eval record for positive, negative, and boundary cases.
- Hardened schema validation for object status enums, payload refs, render-block source refs, task typed refs, contract summary drift, and added negative/boundary snapshot packages.
- Hardened derived consistency validation for HLD source artifacts, quality gate reports, traceability summaries, decision refs, and planning gate evidence refs.
- Hardened the output contract as the unique canonical truth: required full top-level contract views, `document_metadata`, `next_actions`, and exact `object_index` derivation from `objects`.
- Added source-fact auditability checks for `SRC-*` payloads and a closed `source_type` vocabulary.
- Added readiness-blocker validation for blocked `CORE-*` facts, current-phase `REQ-*` facts, triggered `STOP-*` conditions, and blocking open or missing-status `Q-*` / `ASM-*` decisions.
- Added typed traceability validation for open questions, assumptions, and user confirmations.
- Removed task-plan ownership from the workflow and made `high-level-design.json` the only Stage 3 artifact.
- Required Agent PRD Data and State coverage.
- Hardened current-phase handling: ready plans require canonical current phase requirements, reject future-phase task refs, and no longer fall back from missing current-phase requirements to all requirements.
- Hardened derived view consistency: top-level contract views must match `objects`, and `GATE-*` payloads must match `gate_report` rows.
- Hardened task closure validation for task type, ready-plan task status, closure field non-emptiness, stage goal refs, dependency edge contract refs, and planning evidence.
- Hardened audit validation for ISO `source_idea.created_at`, resolved decision evidence, and `TRACE.relation` vocabulary.
- Converted the workflow to a harness-first, review-gated self-improving generation flow.
- Added portable harness core files: `manifest.yaml`, `agent.md`, `workflow.md`, `rules.md`, and schema notes.
- Added `harness_workflow` and `requirement_table` contract gates.
- Added `interaction_decision` as the hard Stage 1 route gate and validator-backed requirement-table origin provenance checks.
- Required clarification questions to be boolean, single-choice, or multi-choice with explicit options.
- Required Human PRD approval evidence before ready Stage 3 HLD.
- Required ready HLD to include contract-backed design sections and design gates.
- Added regression probes for missing harness state, missing requirement table, open-ended questions, missing Human PRD approval, and missing HLD.
- Added Codex adapter source files, canonical `evals/cases`, source harness validator wrapper, and source regression probes for adapter/eval/manifest/mojibake drift.
- Added harness release builder and release notes for source and Codex runtime packages.
- Hardened Stage 1 execution-like readiness: executor, agent, adapter, CLI, automation, scheduler, and tool-orchestration ideas must include source-backed execution topology before proceeding without questions.
- Hardened Stage 2 PRD rendering: execution-ready Agent PRDs must cover non-empty implementation-model refs, and Human PRDs must summarize material execution topology at human-review depth.
- Added the executor real-use-case lessons record and regression probes for missing implementation topology / missing implementation refs.
- Added a Stage 2 PRD quality reference package pointer so agents can calibrate PRD depth and traceability without hardcoding executor-specific facts.
- Hardened Stage 3 HLD into an implementation-design contract with structured control flow, data flow, data objects, interfaces, state model, technical decisions, environment requirements, and no-mock real acceptance gates.
- Hardened Stage 3 real acceptance concreteness: ready HLD now rejects deferred environment/data placeholders, requires `SRC-*` evidence refs for real environment, real data, and acceptance owner, and validates structured data-object fields.
- Hardened Stage 3 semantic design gates: ready HLD now requires fixed passing `gate_key` coverage for source readiness, control flow, data/data objects, interface/state, technical implementation, real acceptance, and task boundary, and rejects generic single-gate shortcuts.
- Hardened Stage 3 HLD document delivery: final packages now require `high-level-design.md` in addition to `high-level-design.json`, and ready HLD Markdown must include source refs, required HLD sections, diagrams, tables, current design refs, and non-thin formal design content.
- Hardened Stage 3 implementation precision: ready HLD interface contracts now require `SRC-*` source evidence and precise invocation boundaries, while real acceptance now requires an executable command, preconditions, expected artifact paths, mechanical checks, and failure criteria.
- Hardened Markdown HLD semantic parity: ready `high-level-design.md` must now render source-backed interface precision, exact acceptance command, expected artifact paths, executable acceptance design, and the required `hld_document_readiness` gate.
- Added independent HLD semantic review: final Stage 3 packages now require `hld-semantic-review.json` with fixed passing dimensions for traceability, control flow, data/object design, interface precision, implementation, executable acceptance, Markdown parity, no untraced invention, and task boundary.
- Sealed the workflow as `1.0.0` after aligning Stage 1 requirement-table intake, Stage 2 execution-ready Agent PRD and human-review Human PRD generation, Stage 3 implementation-ready HLD generation, no-task-output boundaries, fixed HLD design gates, and independent semantic review.

## Compatibility Notes

Designed for Codex skill layout. Install by copying `skills/spec-intake/skill` into the active Codex skills directory as `spec-intake`.
