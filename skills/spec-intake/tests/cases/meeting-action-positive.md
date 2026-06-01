# Eval Case: Meeting Action Positive

## Prompt

Use `spec-intake` to create a spec package for a meeting action item extractor.

The first version may consume only authorized meeting transcript text. It should extract action item, owner, due date when present, and source evidence. A human must confirm the extracted items before Markdown export. The first version must not automatically create Jira, Linear, Asana, calendar, or email tasks.

## Expected Behavior

- Produce `contract-envelope.json`, `human-prd.md`, `agent-prd.md`, `high-level-design.json`, and `intake-notes.md`.
- Build `requirement_table` before rendering PRDs.
- Record `interaction_decision=proceed_without_questions` only when no Stage 1 blockers remain.
- Treat authorized transcript text as required input.
- Preserve human confirmation before export.
- Mark external task-system sync as out of scope or future phase.
- Render Human PRD in Chinese and Agent PRD in English.
- Produce ready HLD only after Human PRD approval is represented by a user-confirmation source.
- Ready HLD must include structured control flow, data flow, data objects, interface contracts, state model, technical decisions, implementation design, environment requirements, and a no-substitute real acceptance plan.

## Forbidden Behavior

- Do not invent Jira, Linear, Asana, calendar, or email integrations.
- Do not allow automatic task creation.
- Do not export unconfirmed action items.
- Do not omit source evidence behavior.
- Do not leave `interaction_decision` missing or inconsistent with blockers.
- Do not produce task plans, task graphs, dependency edges, parallel groups, or implementation task cards.
- Do not enter Stage 3 without Human PRD approval evidence.
- Do not mark HLD ready if real environment, real data, or evidence capture are missing.

## Scoring Rule

Pass if semantic review rubric has no `fail`, the output package validator passes, and any blocked status has concrete required fixes.

## Pass Bar

`pass`
