# Eval Case: Executor Adapter Boundary

## Prompt

Use `spec-intake` to run Stage 1 intake for an executor.

The executor takes an input task description. The basic task definition contains work environment, permissions, and skill configuration. The executor uses an already formed ClaudeTmuxAdapter component to call Claude CLI.

## Expected Behavior

- Produce a Stage 1 package with `contract-envelope.json` only.
- Validate the package with `validate_spec_intake_package.py <output-dir> --stage stage1`.
- Build `requirement_table` rows for executor creation, task definition context, and ClaudeTmuxAdapter-based Claude CLI invocation.
- Record `interaction_decision=ask_user` when key execution boundaries are not yet confirmed.
- Ask only closed-form questions.
- The first clarification round must cover:
  - input contract, such as local CLI task file versus another bounded input form
  - ClaudeTmuxAdapter integration boundary, such as public CLI/API only versus internal implementation dependency
  - completion and output contract, such as durable result shape and who decides task completion
- Keep unconfirmed delivery, done, and integration decisions as `Q-*`, blocked gates, or non-ready rows.

## Forbidden Behavior

- Do not mark `interaction_decision=proceed_without_questions` from the initial prompt alone.
- Do not ask open-text questions.
- Do not omit the ClaudeTmuxAdapter integration-boundary question.
- Do not introduce openclaw, a reviewer, or another external agent as the preferred path unless it is framed as one option and a neutral blocked option is available.
- Do not produce Human PRD, Agent PRD, HLD, task plans, task graphs, dependency edges, parallel groups, or implementation task cards in the Stage 1 package.
- Do not invent the task file schema, output schema, retry behavior, resume behavior, queueing, or concurrency.

## Scoring Rule

Pass if the Stage 1 package validator passes, all clarification questions are closed-form, and semantic review confirms the three high-risk boundaries are covered: input contract, Adapter integration boundary, and completion/output contract.

## Pass Bar

`pass`
