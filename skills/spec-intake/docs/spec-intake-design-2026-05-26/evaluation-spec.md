# Spec Intake Evaluation Spec

## Date

2026-05-26

## Target Dev Root

`skills/spec-intake`

## Target Tests Path

`skills/spec-intake/tests`

## Evaluation Goal

Verify that the skill can guide an agent from raw idea to honest, contract-backed spec package without inventing facts.

## Evaluation Surface

Runtime skill instructions, reference guidance, validator script, and fixture behavior.

## Lifecycle Coverage

Design, implementation, testing, and release checks are represented in lifecycle docs.

## Objective Checks

Run `validate_spec_intake_package.py` against blocked and ready fixture packages, run `tests/validator_regression.py` against known false-positive probes, including derived consistency probes for summaries, object indexes, gates, source artifacts, readiness blockers, traceability, and planning evidence, check lifecycle docs with `validate_artifact_run.py`, and inspect the committed eval cases under `tests/cases/`.

Review `tests/snapshots/semantic-eval-record.md` for the meaning-level verdicts and caller consumption rule.

Validate the negative and boundary snapshot packages under `tests/snapshots/customer-data-negative` and `tests/snapshots/one-line-draft-boundary`.

## Subjective Review Rubric

Use product clarity, honesty, human usefulness, agent executability, task usefulness, and traceability.

## Review Procedure

Inspect output package, compare PRDs and tasks against contract refs, run validator when files exist, then assign verdict.

## Verdict And Status Model

`ready`, `usable with gaps`, or `redesign required`.

## Eval Case Files

- `tests/cases/meeting-action-positive.md`
- `tests/cases/customer-data-negative.md`
- `tests/cases/one-line-draft-boundary.md`

## Boundary Or Ambiguity Case

One-line draft request: output must stay draft or blocked unless execution facts are actually present.

## Positive Case

Meeting action item tool with Markdown-only MVP.

## Negative Case

Automatic customer-data AI system with unclear permission and execution boundary.

## Expected Behaviors

Ask at most three high-value questions, build canonical contract first, render sibling PRDs, and produce ready or blocked task plan honestly.

## Forbidden Behaviors

Do not invent integrations, data retention, automatic writes, verification cases, or ready status.

## Scoring Rule

Any structural validator failure or semantic `fail` blocks readiness. Any mismatch between canonical contract fields and derived summaries, object indexes, top-level views, rendered PRDs, gate reports, or task-plan source artifacts also blocks readiness. Warnings require explicit status downgrade or fix. A package cannot be ready when unresolved readiness blockers exist: blocked current-phase facts, triggered stops, blocking open questions or assumptions, blocked gates, invalid warning gates, unauditable source facts, traceability decision-type mismatches, task plans based only on rendered Agent PRD labels, future-phase requirements in current tasks, or non-closed task cards.

## Pass Bar

Blocked and ready fixture validators pass, negative and boundary snapshot validators pass, validator regression passes, eval case files exist with expected and forbidden behavior, semantic eval record exists, and semantic review has no `fail`.

## Contract Truth Requirements

Evaluation treats `contract-envelope.json` as the only canonical truth. Human PRD, Agent PRD, and task plan outputs are renderings or execution views of that contract. Top-level arrays are views over `objects`; `object_index` is a derived index and must match `objects` exactly by canonical prefix.

`SRC-*` facts must be auditable. Human input, user documents, and confirmations require captured content or target payload. Traceability records must use the right decision reference type: open questions use `Q-*`, assumptions use `ASM-*`, and user confirmations use confirmed `SRC-*` facts.

Task planning is ready only in `contract_backed` mode with canonical contract refs. The ready phase must have current requirements, and ready task cards must keep `IN-*`, `OUT-*`, and `STOP-*` in their closure fields instead of hiding them in generic `contract_refs`. `rendered_agent_prd_only` is allowed only as a blocked diagnostic fallback.
