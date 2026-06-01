---
name: prd-writing
description: Use when Codex needs to write, rewrite, review, or update a professional Simplified Chinese software product PRD for human readers, including source-backed requirements, revision history, structured scope, user needs, acceptance criteria, metrics, rollout, risks, and references. Trigger for requests involving PRD, 产品需求文档, product requirements document, 软件产品需求, feature requirements, or turning research/briefs into a final PRD.
---

# PRD Writing

Use this skill to produce a final, human-readable software product PRD in professional Simplified Chinese. The output must be concise, source-backed, and directly useful for product, design, engineering, QA, operations, security, and business stakeholders.

## Load References

Load only what the task needs:

- `references/prd-methodology.md`: distilled PRD best practices from 10+ external references, including source IDs.
- `references/prd-output-contract.md`: required PRD structure, evidence rules, citation rules, blocking gates, and review checklist.
- `assets/PRD.template.md`: reusable Chinese PRD template.
- `../../tools/validate_prd_document.py`: deterministic PRD gate for saved Markdown outputs.

## Workflow

1. Identify the PRD purpose, product context, intended readers, release boundary, and available sources.
2. Build a source inventory. Assign project evidence IDs before writing, such as `[BIZ-01]`, `[USER-01]`, `[TECH-01]`, `[DATA-01]`, `[DESIGN-01]`, and `[OPS-01]`.
3. Read `references/prd-methodology.md` for methodology support when deciding the structure or quality bar.
4. Read `references/prd-output-contract.md` before composing the final PRD.
5. If product evidence is too thin to support a PRD, do not fabricate a normal PRD. Produce a blocked PRD with revision record, known facts, missing evidence, open questions, and reference list.
6. Start the PRD with the revision table. If updating an existing PRD, preserve prior entries and append a new honest entry.
7. Write only final product conclusions. Do not include process notes, research narration, agent thoughts, or todo-style drafting commentary.
8. Select expression forms by purpose: prose for decisions, tables for requirements and traceability, Mermaid for flows or state, and LaTeX for formulas or metrics.
9. Cite every material claim with project evidence or methodology markers. Use methodology markers only for document-structure rationale, not as product facts.
10. Cite methodology markers in the body when the document structure, acceptance model, traceability model, metrics model, or non-functional coverage is justified by best practice. Do not list methodology references that are not cited in the body.
11. End with `参考文献`, listing every cited project source and external methodology source.
12. If the PRD is saved as Markdown, run `python tools/validate_prd_document.py <prd-path>` from the `prd-writing` skill root before delivery. If validation fails, revise or report the PRD as blocked; do not claim it is ready.
13. Self-review against the checklist in `references/prd-output-contract.md` before claiming the PRD is ready.

## Blocking Gates

Fail the PRD instead of delivering it as ready when any gate fails:

| Gate | Blocks When |
| --- | --- |
| Revision first | The first visible line is not `## 修订记录`. |
| Evidence | Any material product statement, summary row, requirement row, metric row, acceptance row, risk row, or traceability row lacks a source marker. |
| Reference round trip | A cited marker is missing from `参考文献`, or a listed reference is not cited in the body. |
| Methodology grounding | External methodology references are listed but not cited in the body, or methodology markers are used as product facts. |
| Final-view only | The document contains process narration, TODO markers, placeholders, or drafting commentary. |
| Requirements | Functional requirements are not prioritized, source-backed, and linked to acceptance criteria. |
| Acceptance | Acceptance criteria are not pass/fail verifiable. |
| Unknowns | Missing evidence is hidden instead of marked as assumption, open question, risk, blocker, or dependency. |

## Required PRD Sections

Use these sections unless the user's requested format is stricter. Omit only sections that are irrelevant to the PRD purpose.

1. 修订记录
2. 文档摘要
3. 背景与问题
4. 目标与成功指标
5. 用户与使用场景
6. 范围定义
7. 用户旅程或业务流程
8. 功能需求
9. 非功能需求与约束
10. 数据、埋点与度量方案
11. 验收标准
12. 发布、灰度与回滚
13. 依赖、风险与开放问题
14. 需求追踪矩阵
15. 参考文献

## Hard Rules

- Write in Simplified Chinese.
- Use formal written language.
- Write for human readers, not machines.
- Put the revision table at the beginning.
- Keep the document final-view only: no process narration, draft comments, or meta discussion.
- Do not fabricate facts. Mark unknowns as assumptions, open questions, risks, or blockers.
- Keep every section tied to the product purpose.
- Keep the document concise and readable.
- Use source markers for all material claims.
- Include a complete references section at the end.
- Do not list unused references.
- Do not deliver a saved PRD as ready until `validate_prd_document.py` passes.

## Common Mistakes

| Mistake | Correct Behavior |
| --- | --- |
| Writing a generic PRD template with placeholders only | Produce a purpose-specific PRD using the user's sources and mark unknowns. |
| Treating methodology sources as product evidence | Use methodology sources only for structure and quality principles. |
| Burying revision history near the end | Put revision history first. |
| Including "写作过程" or "调研过程" | Include only final conclusions and evidence. |
| Listing vague requirements | Write testable, source-backed, prioritized requirements. |
| Missing non-goals | Explicitly state out-of-scope items when they prevent scope creep. |
| Missing acceptance criteria | Define verifiable pass/fail conditions for key requirements. |
| Hiding uncertainty | Record assumptions, risks, blockers, and open questions honestly. |
