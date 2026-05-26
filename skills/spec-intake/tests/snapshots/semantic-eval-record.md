# Semantic Eval Record

## Date

2026-05-26

## Reviewer Role

Spec-intake quality reviewer checking whether output packages would be acceptable for downstream PRD consumption and task planning.

## Verdict Vocabulary

- `pass`: structurally valid and semantically aligned with the eval case.
- `revise`: structurally valid but meaning-level gaps must be fixed before ready use.
- `fail`: unsafe, invented, untraceable, or readiness is overstated.

## Caller Consumption Rule

`pass` may be consumed by the caller. `revise` must route back to contract or rendering fixes. `fail` blocks readiness and task execution.

## Case: Meeting Action Positive

Prompt file: `tests/cases/meeting-action-positive.md`

Representative snapshot package: `tests/fixtures/ready-agent-prd-task-plan`

Verdict: `pass`

Evidence:

- Validator passes for the ready package.
- The package keeps authorized transcript text as `IN-001`.
- The package requires human confirmation through `EXE-001`.
- The package exports Markdown through `OUT-001`.
- `OOS-001` blocks automatic external task creation.
- `TASK-001` covers `REQ-001`, `AC-001`, `IN-001`, `EXE-001`, `VER-001`, `OUT-001`, `STOP-001`, and `DONE-001`.

## Case: Customer Data Negative

Prompt file: `tests/cases/customer-data-negative.md`

Snapshot package: `tests/snapshots/customer-data-negative`

Verdict: `pass`

Evidence:

- The expected behavior preserves permission, input boundary, action authority, safety, privacy, and verification as blockers until clarified.
- A valid output must not mark Agent PRD as `execution_ready`.
- A valid output must not create tasks that modify customer records or trigger outbound contact.
- The snapshot package validates with `planning_status=blocked`.

## Case: One-Line Draft Boundary

Prompt file: `tests/cases/one-line-draft-boundary.md`

Snapshot package: `tests/snapshots/one-line-draft-boundary`

Verdict: `pass`

Evidence:

- The expected behavior separates confirmed facts from hypotheses.
- A valid output must not invent CRM vendor, fields, scoring model, thresholds, permissions, integrations, or success metrics.
- A valid task plan remains blocked unless execution inputs, scoring rules, verification, stop conditions, and done criteria are explicit.
- The snapshot package validates with `planning_status=blocked`.

## Live Eval Run

Run date: 2026-05-26

Run record: `tests/live-runs/2026-05-26/README.md`

Produced packages:

- `tests/live-runs/2026-05-26/meeting-action-positive`
- `tests/live-runs/2026-05-26/customer-data-negative`
- `tests/live-runs/2026-05-26/one-line-draft-boundary`

Validator command:

```bash
python skill/scripts/validate_spec_intake_package.py <package-dir>
```

Validator verdict:

- Meeting Action Positive: `ok=true`
- Customer Data Negative: `ok=true`
- One-Line Draft Boundary: `ok=true`

Semantic verdict:

- Meeting Action Positive: `pass`
- Customer Data Negative: `pass`
- One-Line Draft Boundary: `pass`

Residual requirement status: closed. Future changes to the skill contract, validator, task-decomposition rules, or render rules must rerun these three live packages or replace them with an equivalent dated live-run record.
