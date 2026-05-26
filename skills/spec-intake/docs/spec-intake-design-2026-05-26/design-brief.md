# Spec Intake Design Brief

## Date

2026-05-26

## Mission

Create a reusable skill that turns raw product ideas into contract-backed Human PRDs, Agent PRDs, and execution task plans.

## Target Dev Root

`skills/spec-intake`

## Target Skill Source Path

`skills/spec-intake/skill`

## Dominant Skill Type

`hybrid`: thinking-dominant, script-supported.

## Prototype Paradigm

Bounded reusable skill. It produces spec artifacts, but the skill itself is not a harness workflow runtime.

## Harness Class

Not a harness workflow. It follows harness-hardening principles for contracts, gates, and evidence.

## Responsibilities

- Convert raw ideas into canonical contract-backed spec packages.
- Guide clarification, inference, assumptions, and open questions.
- Render Human PRD and Agent PRD from the contract.
- Decompose execution-ready Agent PRD into task plans.
- Provide validation guidance and a structural validator.

## Output Contract

The expected generated package contains `contract-envelope.json`, `human-prd.md`, `agent-prd.md`, `execution-task-plan.json`, and `intake-notes.md`.

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
| Task decomposition | Thinking |
| Structural validation | Script |
| Semantic quality | Thinking review |

## Input Contract

Inputs are raw idea text, optional source notes, requested output target, and optional output directory. Missing facts must become questions, assumptions, stop conditions, or blocked gates.

## Execution Contract

Run intake, build canonical contract, render PRDs, plan tasks if allowed, then validate. Never write untraced facts into PRDs or tasks.

## Lifecycle Plan

Design, implement runtime skill files, add fixtures, run validator, validate lifecycle artifacts, then optionally package for release.

## Done Criteria

Runtime files exist, references are linked, validator fixture passes, lifecycle validation passes, and semantic review has no high-severity finding.

## Self-Improving Loop Contract

Review failures become updates to references, validator checks, or fixtures. Do not bury repeated failures in final prose.

## Validator And Semantic Review Plan

Use `skill/scripts/validate_spec_intake_package.py` for structure, `tests/validator_regression.py` for known false-positive probes, and `skill/references/quality-gates.md` for semantic review.

## Trigger Design

Trigger on raw idea intake, PRD creation, Human PRD, Agent PRD, execution task planning, and spec package generation.

## Boundary With skill-creator

`harness-workflow-designer` governs architecture and lifecycle. Generic skill anatomy follows skill-creator conventions.

## Encoding Hygiene Plan

Runtime files use UTF-8. Chinese is allowed where user-facing PRD rules require it.

## Composition Notes

The skill can be composed with downstream implementation skills after it emits an execution-ready Agent PRD and ready task plan.

## Risks Or Open Questions

Full semantic quality still requires agentic evaluation on realistic ideas. The current validator is intentionally structural.
