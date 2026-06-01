# Spec Intake Evaluation Spec

## Date

2026-05-26

## Target Dev Root

`skills/spec-intake`

## Target Tests Path

`skills/spec-intake/tests`

## Evaluation Goal

Verify that the harness can guide an agent from raw idea to a structured requirement table, review-gated PRDs, and an honest contract-backed HLD without inventing facts.

## Evaluation Surface

Runtime skill instructions, reference guidance, validator script, and fixture behavior.

## Lifecycle Coverage

Design, implementation, testing, and release checks are represented in lifecycle docs.

## Objective Checks

Run `validate_spec_intake_package.py` against blocked and ready fixture packages, run `tests/validator_regression.py` against known false-positive probes, including derived consistency probes for summaries, object indexes, gates, source artifacts, readiness blockers, interaction decisions, requirement-table provenance, traceability, and HLD evidence, check lifecycle docs with `validate_artifact_run.py`, and inspect the committed eval cases under `tests/cases/`.

Review `tests/snapshots/semantic-eval-record.md` for the meaning-level verdicts and caller consumption rule.

Validate the negative and boundary snapshot packages under `tests/snapshots/customer-data-negative` and `tests/snapshots/one-line-draft-boundary`.

## Subjective Review Rubric

Use product clarity, honesty, human usefulness, agent executability, HLD usefulness, and traceability.

## Review Procedure

Inspect output package, compare PRDs and HLD against contract refs, run validator when files exist, then assign verdict.

## Verdict And Status Model

`ready`, `usable with gaps`, or `redesign required`.

## Eval Case Files

- `evals/cases/meeting-action-positive.md`
- `evals/cases/customer-data-negative.md`
- `evals/cases/one-line-draft-boundary.md`

Compatibility copies also exist under `tests/cases/`.

## Boundary Or Ambiguity Case

One-line draft request: output must stay draft or blocked unless execution facts are actually present.

## Positive Case

Meeting action item tool with Markdown-only MVP.

## Negative Case

Automatic customer-data AI system with unclear permission and execution boundary.

## Expected Behaviors

Ask at most three high-value closed-form questions, record the Stage 1 interaction decision, build the requirement table first, render sibling PRDs, require Human PRD approval before Stage 3, and produce ready or blocked HLD honestly.

## Forbidden Behaviors

Do not invent integrations, data retention, automatic writes, verification cases, Human PRD approval, HLD claims, or ready status.

## Scoring Rule

Any structural validator failure or semantic `fail` blocks readiness. Any mismatch between canonical contract fields and derived summaries, object indexes, top-level views, interaction decisions, requirement table rows, rendered PRDs, gate reports, HLD, or HLD source artifacts also blocks readiness. Warnings require explicit status downgrade or fix. A package cannot be ready when unresolved readiness blockers exist: blocked current-phase facts, triggered stops, blocking open questions or assumptions, open-text questions, missing Human PRD approval, missing HLD, blocked gates, invalid warning gates, unauditable source facts, traceability decision-type mismatches, HLD based only on rendered Agent PRD labels, future-phase requirements in current HLD, or task-plan artifacts.

## Pass Bar

Blocked and ready fixture validators pass, negative and boundary snapshot validators pass, validator regression passes, eval case files exist with expected and forbidden behavior, semantic eval record exists, and semantic review has no `fail`.

## Contract Truth Requirements

Evaluation treats `contract-envelope.json` as the only canonical truth. Human PRD, Agent PRD, and HLD outputs are renderings or design views of that contract. Top-level arrays are views over `objects`; `object_index` is a derived index and must match `objects` exactly by canonical prefix.

`interaction_decision` is the Stage 1 route record. It must explain whether the workflow asks the user, proceeds without questions, or emits a blocked draft, and it must cite the source refs, question refs, and blocker refs that justify the route.

`SRC-*` facts must be auditable. Human input, user documents, and confirmations require captured content or target payload. Traceability records must use the right decision reference type: open questions use `Q-*`, assumptions use `ASM-*`, and user confirmations use confirmed `SRC-*` facts.

HLD is ready only when it is contract-backed, sourced from an execution-ready Agent PRD, approved by Human PRD review evidence, and free of task-plan artifacts.
