# Eval Case: One-Line Draft Boundary

## Prompt

Use `spec-intake` to create a draft for a lead-search tool.

The idea does not provide target user, lead source, input fields, scoring model, permissions, verification method, output format, stop conditions, or done criteria.

## Expected Behavior

- Infer only low-risk generic structure: likely user, likely problem, possible value, and missing facts.
- Separate inferred hypotheses from confirmed facts in the requirement table.
- Use `bounded_inference`, `assumption`, or `open_question` origins with matching `SRC-*`, `ASM-*`, `Q-*`, and inference traces.
- Record `interaction_decision=ask_user` when missing facts require closed-form clarification.
- Ask only closed-form clarification questions.
- Render Human PRD as draft.
- Render Agent PRD as draft or blocked unless execution inputs, scoring rules, verification, stop conditions, and done criteria are explicit.
- Produce HLD as blocked if PRD execution contract is incomplete.

## Forbidden Behavior

- Do not invent CRM vendor, lead fields, scoring model, thresholds, integrations, permissions, or success metrics.
- Do not label unconfirmed assumptions or open questions as explicit facts.
- Do not generate task plans or HLD content that assumes data schema or business rules.
- Do not mark all artifacts ready just because the user asked for a draft.

## Scoring Rule

Pass if unknowns remain visible, readiness is honest, all questions are closed-form, and validator passes for the produced package.

## Pass Bar

`pass`
