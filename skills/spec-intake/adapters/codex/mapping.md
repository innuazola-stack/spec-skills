# Codex Adapter Mapping

The Codex adapter preserves the portable `spec-intake` harness contracts in the Codex skill runtime.

## Stage Mapping

| Portable stage | Codex behavior |
| --- | --- |
| Stage 1 requirement table | Use the local references to build `contract-envelope.json`, ask only closed-form clarification questions, and run the Stage 1 validator before claiming completion. |
| Stage 2 PRD review | Call `prd-writer` for `prd.md`, derive `prd-brief.md`, validate with `--stage stage2`, and record PRD review approval only from an explicit user confirmation. |
| Stage 3 HLD | Call `hld-writer` with the approved PRD package and contract, then validate the HLD package and semantic review. |

## Runtime Limits

Codex cannot force a user to approve a PRD in a separate UI state. The adapter records approval as `SRC.source_type=user_confirmation`; without that source ref and current artifact hash bindings, the validator blocks ready Stage 3 HLD.

If `prd-writer` or `hld-writer` is not installed or cannot be invoked, the adapter must report a blocked package rather than silently writing the artifact itself.

## Non-Negotiable Mappings

- The adapter must preserve the PRD review approval gate.
- The adapter must reject legacy `human-prd.md` and `agent-prd.md` outputs.
- The adapter must preserve closed-form Stage 1 questions.
- The adapter must preserve `contract-envelope.json` as canonical truth.
- The adapter must not output task plans.
