---
name: executor-progress-judgment
description: Judge Claude CLI progress from ClaudeTmuxAdapter screen evidence for Executor runs and write a structured progress decision JSON file.
---

# Executor Progress Judgment

Use this skill only when Executor invokes OpenClaw for an idle Claude CLI screen.

## Input Contract

The OpenClaw message must name:

- `progress-judgment-request.json`: a JSON file written by Executor.
- `progress-decision.json`: the JSON file this skill must write.

Read the request file before deciding. The request must contain:

- `run_id`
- `screen_snapshot_ref`
- `screen_text`
- `adapter_state`
- `task_context`
- `prior_decisions`
- `allowed_decisions`

If any required field is missing, write a `blocked` decision with a concise rationale.

## Decision Rules

Choose exactly one decision:

- `next_instruction`: Claude is idle and needs a specific next instruction to continue.
- `deliverable_ready`: the screen evidence and task context show the deliverable is ready for mechanical delivery checks.
- `no_action`: Claude is idle, but the safest action is to wait for the next poll.
- `blocked`: progress cannot continue safely or required evidence is insufficient.

Never claim `deliverable_ready` from general confidence, elapsed time, or adapter idle state alone. It requires concrete screen evidence that the task output is complete enough for Executor's mechanical checks.

Only produce `next_instruction` when the instruction is specific, bounded by the task context, and does not request filesystem, command, or network actions outside the permission boundary.

## Output Contract

Write only the decision JSON to the requested `progress-decision.json` path. Use this shape:

```json
{
  "decision": "next_instruction|deliverable_ready|no_action|blocked",
  "next_instruction": "string; required only for next_instruction",
  "rationale": "short evidence-based reason",
  "confidence": "low|medium|high",
  "screen_evidence_ref": "same value as request.screen_snapshot_ref",
  "openclaw_evidence_path": "path to this decision file"
}
```

Omit `next_instruction` unless `decision` is `next_instruction`. A `low` confidence decision must not be `deliverable_ready`.

## Forbidden Behavior

- Do not control Claude, tmux, or ClaudeTmuxAdapter.
- Do not execute the task yourself.
- Do not read unrelated files.
- Do not invent screen evidence that is not present in the request.
- Do not return unstructured prose as the canonical decision.
