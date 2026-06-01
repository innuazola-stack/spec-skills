---
name: prd-writing
description: Use when Codex should write, rewrite, review, or update a professional Simplified Chinese software product PRD with revision history, source-backed requirements, concise final conclusions, traceability, acceptance criteria, metrics, rollout, risks, and references.
---

# PRD Writing Codex Adapter

Read the portable skill package before writing:

1. `manifest.yaml`
2. `agent.md`
3. `workflow.md`
4. `rules.md`
5. `skill/SKILL.md`
6. `skill/references/prd-methodology.md`
7. `skill/references/prd-output-contract.md`

Use `skill/assets/PRD.template.md` when the user wants a new PRD or when an existing structure is weak.

Before claiming completion, verify the final PRD begins with `修订记录`, uses Simplified Chinese, contains no process narration, cites material claims, cites methodology references in the body when they are listed, and ends with `参考文献`.

If the PRD is saved as Markdown, run this from the `prd-writing` skill root before delivery:

```bash
python tools/validate_prd_document.py <prd-path>
```

If the validator fails, revise the PRD or report it as blocked. Do not claim a failed PRD is ready.
