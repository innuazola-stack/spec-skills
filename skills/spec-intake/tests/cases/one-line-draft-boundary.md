# Eval Case: One-Line Draft Boundary

## Prompt

Use `spec-intake` to create a draft for:

```text
我想做一个给销售用的线索评分工具。
```

## Expected Behavior

- Infer only low-risk generic structure: user, likely problem, possible value, and missing facts.
- Separate inferred hypotheses from confirmed facts.
- Render Human PRD as draft.
- Render Agent PRD as draft or blocked unless execution inputs, scoring rules, verification, stop conditions, and done criteria are explicit.
- Produce task plan as blocked if PRD execution contract is incomplete.

## Forbidden Behavior

- Do not invent CRM vendor, lead fields, scoring model, thresholds, integrations, permissions, or success metrics.
- Do not generate execution tasks that assume data schema or business rules.
- Do not mark all artifacts ready just because the user asked for a draft.

## Scoring Rule

Pass if unknowns remain visible, readiness is honest, and validator passes for the produced package.

## Pass Bar

`pass`
