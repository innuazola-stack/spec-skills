# Eval Case: Meeting Action Positive

## Prompt

Use `spec-intake` to create a spec package for:

```text
做一个会议后自动整理行动项的工具。第一版只处理授权的会议文字记录，提取行动项、负责人、截止时间和原文证据，让人确认后导出 Markdown，不要自动创建 Jira/Linear/Asana 任务。
```

## Expected Behavior

- Produce `contract-envelope.json`, `human-prd.md`, `agent-prd.md`, `execution-task-plan.json`, and `intake-notes.md`.
- Treat authorized meeting text as a required input.
- Preserve human confirmation before export or external task creation.
- Mark task-system sync as out of scope or a future phase.
- Render Human PRD in Chinese and Agent PRD in English.
- Produce a ready task plan only if execution objects, verification, stop, and done criteria are traceable; otherwise produce a blocked task plan with required fixes.

## Forbidden Behavior

- Do not invent Jira, Linear, Asana, calendar, or email integrations.
- Do not allow automatic task creation.
- Do not export unconfirmed action items.
- Do not omit source evidence behavior.

## Scoring Rule

Pass if semantic review rubric has no `fail`, output package validator passes, and any blocked status has concrete required fixes.

## Pass Bar

`pass`
