# Spec Intake Test Plan

## Date

2026-05-26

## Target Dev Root

`skills/spec-intake`

## Target Tests Path

`skills/spec-intake/tests`

## Test Goal

Prove the initial skill package has structural validation and realistic semantic review criteria.

## Eval Case Files

- `tests/cases/meeting-action-positive.md`
- `tests/cases/customer-data-negative.md`
- `tests/cases/one-line-draft-boundary.md`

## Positive Case Coverage

Meeting action item idea with Markdown-only MVP should produce contract-backed PRDs and ready HLD or explicit blockers.

## Negative Case Coverage

Automatic customer-data AI idea should not become execution-ready without permission, input, stop, and verification facts.

## Boundary Case Coverage

One-line "give me a draft" request should produce draft or blocked artifacts with unknowns preserved.

## Tooling Or Commands

Run `skill/scripts/validate_skill_package.py skill`.

Run `skill/scripts/validate_spec_intake_package.py tests/fixtures/blocked-agent-prd-draft`.

Run `skill/scripts/validate_spec_intake_package.py tests/fixtures/ready-agent-prd-hld`.

Run `python tests/validator_regression.py` to prove known false-positive probes fail, including derived consistency probes for object indexes, source artifacts, readiness blockers, quality gates, traceability summaries, HLD evidence refs, and blocked-HLD source truth.

Check `tests/cases/*.md` for prompt, expected behavior, forbidden behavior, scoring rule, and pass bar.

Run `skill/scripts/validate_spec_intake_package.py tests/snapshots/customer-data-negative`.

Run `skill/scripts/validate_spec_intake_package.py tests/snapshots/one-line-draft-boundary`.

Check `tests/snapshots/semantic-eval-record.md` for reviewer role, verdict vocabulary, evidence, and caller consumption rule.

## Pass Bar

Both fixture validators return `ok=true`; both snapshot validators return `ok=true`; skill validator returns `ok=true`; validator regression returns `ok=true` with every intentional bad mutation rejected; eval cases and semantic eval record are present and reviewable; semantic review rubric has no `fail`.

## Regression Probe Scope

The regression suite must reject all known root-cause classes that previously allowed false readiness:

- `object_index` drift from canonical `objects`.
- top-level view drift from canonical `objects`, including hidden `REQ-*` or `GATE-*` objects.
- `GATE-*` payload drift from `gate_report`.
- Missing audit payload on user-input or user-confirmation `SRC-*` facts.
- `CORE-*`, current `REQ-*`, triggered `STOP-*`, and open or missing-status blocking `Q-*` / `ASM-*` refs while any rendered artifact is marked ready.
- Quality gate contradictions, including `blocking=true` without `blocked` status and `warning` without required fix guidance.
- Traceability rows whose `decision_type` does not match their `decision_ref`, including `user_confirmation` rows that must point to confirmed `SRC-*` facts.
- invalid `TRACE.relation`, non-ISO `source_idea.created_at`, or resolved `Q-*` / `ASM-*` without resolution refs.
- Agent PRD packages missing the Data and State section.
- HLD that claims readiness from rendered labels instead of canonical contract refs.
- ready HLD with missing approval, draft Agent PRD source, empty design sections, missing design evidence, or non-contract refs.
- legacy task-plan artifacts such as `execution-task-plan.json`, task graphs, dependency edges, or parallel groups.
