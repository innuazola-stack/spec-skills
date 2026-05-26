# Spec Intake Live Eval Run

## Date

2026-05-26

## Purpose

Close the release evidence gap in `tests/snapshots/semantic-eval-record.md` by materializing the three eval prompt outputs as file packages and validating each package with the repository validator.

## Packages

| Case | Prompt | Package | Expected readiness | Validator | Semantic verdict |
| --- | --- | --- | --- | --- | --- |
| Meeting Action Positive | `tests/cases/meeting-action-positive.md` | `tests/live-runs/2026-05-26/meeting-action-positive` | Human PRD `review_ready`; Agent PRD `execution_ready`; task plan `ready` | `ok=true` | `pass` |
| Customer Data Negative | `tests/cases/customer-data-negative.md` | `tests/live-runs/2026-05-26/customer-data-negative` | Human PRD `draft`; Agent PRD `blocked`; task plan `blocked` | `ok=true` | `pass` |
| One-Line Draft Boundary | `tests/cases/one-line-draft-boundary.md` | `tests/live-runs/2026-05-26/one-line-draft-boundary` | Human PRD `draft`; Agent PRD `blocked`; task plan `blocked` | `ok=true` | `pass` |

## Commands

```powershell
C:\Users\54256213\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe skills\spec-intake\skill\scripts\validate_spec_intake_package.py skills\spec-intake\tests\live-runs\2026-05-26\meeting-action-positive
C:\Users\54256213\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe skills\spec-intake\skill\scripts\validate_spec_intake_package.py skills\spec-intake\tests\live-runs\2026-05-26\customer-data-negative
C:\Users\54256213\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe skills\spec-intake\skill\scripts\validate_spec_intake_package.py skills\spec-intake\tests\live-runs\2026-05-26\one-line-draft-boundary
```

All three commands returned:

```json
{
  "ok": true,
  "errors": []
}
```

## Semantic Review Notes

- The positive meeting-action case keeps authorized transcript text as a required input, requires human confirmation, exports Markdown, and keeps external task-system creation out of scope.
- The customer-data negative case keeps permission, data boundary, action authority, safety, privacy, and verification unresolved instead of inventing executable authority.
- The one-line draft boundary case keeps CRM vendor, scoring inputs, scoring rules, thresholds, integrations, permissions, and success metrics unknown instead of turning hypotheses into facts.

## Reuse Rule

If the contract schema, validator, render rules, or task-decomposition rules change, this dated live-run record must be rerun or superseded by a newer dated record.
