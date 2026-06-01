# Spec Intake Design Brief

## Date

2026-05-26

## Mission

Create a reusable skill that turns raw product ideas into contract-backed Human PRDs, Agent PRDs, and HLD.

## Target Dev Root

`skills/spec-intake`

## Target Skill Source Path

`skills/spec-intake/skill`

## Workflow Type

`harness-workflow`: review-gated, self-improving generation.

## Dominant Skill Type

Harness workflow. The portable core owns staged orchestration, gates, contracts, and release validation; the Codex skill is a runtime adapter.

## Prototype Paradigm

Portable harness core with a Codex skill adapter.

## Harness Class

Review-gated self-improving generation harness.

## Responsibilities

- Convert raw ideas into a Stage 1 structured requirement table.
- Record an auditable Stage 1 interaction decision before PRD rendering.
- Guide clarification, inference, assumptions, and open questions without open-text questions.
- Render Human PRD and Agent PRD from the requirement table and contract.
- Gate Stage 3 on Human PRD approval.
- Produce HLD from an approved Human PRD and execution-ready Agent PRD.
- Provide validation guidance and a structural validator.

## Output Contract

The expected generated package contains `contract-envelope.json`, `human-prd.md`, `agent-prd.md`, `high-level-design.json`, and `intake-notes.md`. The contract must include `harness_workflow`, `interaction_decision`, and `requirement_table`; ready HLD must include required design sections and design gates.

## Non-Responsibilities

- Execute implementation tasks.
- Resolve open product decisions without the user.
- Invent scope, technologies, data fields, tests, or external integrations.
- Treat script validation as semantic approval.

## Subproblem Ownership Map

| Subproblem | Owner |
| --- | --- |
| Product understanding | Thinking |
| Contract construction | Thinking |
| PRD rendering | Thinking |
| HLD drafting | Thinking |
| Structural validation | Script |
| Semantic quality | Thinking review |

## Input Contract

Inputs are raw idea text, optional source notes, requested output target, and optional output directory. Missing facts must become closed-form questions, assumptions, stop conditions, or blocked gates, and the Stage 1 route must be recorded in `interaction_decision`.

## Execution Contract

Run Stage 1 requirement table intake, Stage 2 PRD rendering and Human PRD review, then Stage 3 HLD only after approval. Never write untraced facts into PRDs or HLD.

## Lifecycle Plan

Design portable harness files, implement runtime skill adapter files, add fixtures, run validator, validate lifecycle artifacts, then optionally package for release.

## Done Criteria

Runtime files exist, references are linked, validator fixture passes, lifecycle validation passes, and semantic review has no high-severity finding.

## Self-Improving Loop Contract

Review failures become updates to references, validator checks, or fixtures. Do not bury repeated failures in final prose.

## Validator And Semantic Review Plan

Use `skill/scripts/validate_spec_intake_package.py` for structure, `tests/validator_regression.py` for known false-positive probes, and `skill/references/quality-gates.md` for semantic review.

## Trigger Design

Trigger on raw idea intake, PRD creation, Human PRD, Agent PRD, HLD, and spec package generation.

## Boundary With skill-creator

`harness-workflow-designer` governs architecture and lifecycle. Generic skill anatomy follows skill-creator conventions.

## Encoding Hygiene Plan

Runtime files use UTF-8. Chinese is allowed where user-facing PRD rules require it.

## Composition Notes

The skill can be composed with downstream implementation planning or development skills after it emits an execution-ready Agent PRD and ready HLD.

## Risks Or Open Questions

Full semantic quality still requires agentic evaluation on realistic ideas. The current validator is intentionally structural.
