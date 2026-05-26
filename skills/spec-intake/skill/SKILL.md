---
name: spec-intake
description: Turn a raw product idea, one-line request, notes, or rough feature concept into a contract-backed specification package: canonical structured contract, Human PRD, Agent PRD, and execution task plan. Use when Codex needs to conduct PRD intake, ask clarifying questions, render human/agent PRDs, or decompose an execution-ready Agent PRD into independently acceptable implementation tasks.
---

# Spec Intake

Use this skill to turn a human idea into a spec package that another person or agent can consume without guessing.

The skill is `hybrid`: thinking-dominant, script-supported. Reasoning owns product understanding, clarification, contract modeling, PRD rendering, and task decomposition. Scripts only validate file shape and key invariants; they never decide product meaning.

## Required References

Load only what the current request needs:

- `references/intake-method.md`: use for turning a raw idea into a canonical contract and deciding what to ask.
- `references/output-artifacts.md`: use before writing or reviewing the contract envelope, Human PRD, or Agent PRD.
- `references/task-decomposition.md`: use before producing execution tasks.
- `references/quality-gates.md`: use before claiming output is ready.

## Default Workflow

1. Register the user's idea and any provided notes as source facts.
2. Separate explicit facts, bounded inferences, assumptions, and open questions.
3. Ask at most three high-value clarifying questions when blockers prevent a useful contract. If the user asks for a draft anyway, produce a blocked or draft package instead of inventing facts.
4. Build `contract-envelope.json` as the single source of truth. All PRD and task content must trace to it.
5. Render `human-prd.md` in clear professional Chinese for human product review.
6. Render `agent-prd.md` in English for implementation agents only when the contract supports execution readiness; otherwise render draft or blocked status.
7. Produce `execution-task-plan.json` only from an execution-ready Agent PRD and canonical phase. If blocked, output the blocked task-plan envelope with an empty task graph.
8. Run self-review and, when files exist locally, run `scripts/validate_spec_intake_package.py <output-dir>`.

## Output Package

When creating files, write a package with this shape unless the user names another destination:

```text
<output-dir>/
  contract-envelope.json
  human-prd.md
  agent-prd.md
  execution-task-plan.json
  intake-notes.md
```

`intake-notes.md` records questions, assumptions, blocked reasons, and source notes. It is not a substitute for the canonical contract.

## Hard Rules

- Contract first: no Human PRD, Agent PRD, or task fact may exist only in prose.
- Honest unknowns: unknown facts become `Q`, `ASM`, `STOP`, or blocked gates.
- No silent execution readiness: Agent PRD can be `execution_ready` only when execution objects, verification, stop conditions, and done criteria are traceable.
- No task invention: execution tasks must not introduce requirements, fields, technologies, tests, or scope absent from the source contract.
- No rendered-only ready plan: a rendered Agent PRD without the canonical contract can only produce `planning_status=blocked`.
- Preserve sibling consistency: Human PRD and Agent PRD are sibling renders from the contract, not sources for each other.

## Completion Check

Before finalizing, verify:

- contract envelope JSON parses and contains canonical objects plus gate report.
- Human PRD and Agent PRD state their source contract and do not add untraced facts.
- every Agent PRD current requirement has acceptance and verification.
- execution task plan is either ready with contract-backed refs, or blocked with empty executable graph and required fixes.
- validation output is reported honestly, including any skipped checks.
