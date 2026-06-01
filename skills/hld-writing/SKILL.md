---
name: hld-writing
description: Use when Codex needs to write, rewrite, review, or update a professional Simplified Chinese software product High-Level Design (HLD) document for human readers, including revision history, source-backed architecture context, scope, quality attributes, architectural views, decisions, tradeoffs, risks, traceability, and references. Trigger for HLD, HLDD, high-level design, 高层设计, 概要设计, 架构设计文档, 技术方案, or turning PRD/research/architecture notes into a final HLD.
---

# HLD Writing

Use this skill to produce a final, human-readable software product HLD in professional Simplified Chinese. The document must explain the selected architecture clearly enough for product, engineering, QA, operations, security, data, and business stakeholders to align on scope, quality goals, tradeoffs, and delivery risks.

## Load References

Load only what the task needs:

- `references/hld-methodology.md`: distilled HLD and architecture-documentation practices from 10+ external references, including source IDs.
- `references/hld-output-contract.md`: required HLD structure, evidence rules, citation rules, expression-form rules, and review checklist.
- `assets/HLD.template.md`: reusable Simplified Chinese HLD template.

## Workflow

1. Identify the HLD purpose, system boundary, product context, intended readers, release scope, and available sources.
2. Build a source inventory. Assign project evidence IDs before writing, such as `[BIZ-01]`, `[PRD-01]`, `[TECH-01]`, `[DATA-01]`, `[SEC-01]`, `[OPS-01]`, and `[DESIGN-01]`.
3. Read `references/hld-methodology.md` when selecting architecture-documentation principles, views, diagrams, quality attributes, and decision-record conventions.
4. Read `references/hld-output-contract.md` before composing or reviewing the final HLD.
5. Start the HLD with the revision table. If updating an existing HLD, preserve prior entries and append a new honest entry.
6. Write only final architecture conclusions. Do not include process notes, research narration, agent thoughts, drafting commentary, or "next steps" unless they are approved product/engineering follow-up decisions.
7. Select expression forms by purpose: prose for conclusions, tables for inventories and traceability, Mermaid for architecture/sequence/deployment/data-flow views, and LaTeX for formulas or capacity models.
8. Cite every material claim with project evidence or methodology markers. Use methodology markers only for document-structure rationale, not as product facts.
9. End with `参考文献`, listing every project source and external methodology source cited in the document.
10. Self-review against the checklist in `references/hld-output-contract.md` before claiming the HLD is ready.

## Required HLD Sections

Use these sections unless the user's requested format is stricter. Omit only sections that are irrelevant to the HLD purpose.

1. 修订记录
2. 文档概述
3. 背景与目标
4. 架构摘要
5. 范围边界
6. 干系人与关注点
7. 质量属性目标
8. 约束、假设与依赖
9. 架构视图
10. 数据与接口设计
11. 安全、隐私与合规设计
12. 可靠性、性能与容量设计
13. 运维、可观测性与发布设计
14. 架构决策与权衡
15. 风险、技术债与待确认事项
16. 需求追踪矩阵
17. 参考文献

## Hard Rules

- Write in Simplified Chinese.
- Use formal written language with natural, human-oriented explanations.
- Put the revision table at the beginning.
- Keep the document final-view only: no process narration, draft comments, hidden reasoning, or meta discussion.
- Do not fabricate product facts, architecture constraints, metrics, dependencies, diagrams, decisions, tradeoffs, or references.
- Mark unknowns as assumptions, risks, open questions, or blockers.
- Keep every section tied to the system purpose and HLD topic.
- Keep the document concise and readable.
- Use source markers for all material claims.
- Include a complete references section at the end.

## Common Mistakes

| Mistake | Correct Behavior |
| --- | --- |
| Writing a generic architecture essay | Produce a system-specific HLD using the user's sources and mark gaps honestly. |
| Mixing HLD with low-level implementation detail | Keep implementation detail only when needed to justify a high-level decision. |
| Treating methodology sources as product evidence | Use methodology sources only for structure and quality principles. |
| Missing revision history | Put revision history first and update it honestly. |
| Including "调研过程" or "写作过程" | Include only final conclusions and evidence. |
| Drawing diagrams without textual conclusions | Every diagram must have a short explanation of what decision or concern it clarifies. |
| Listing quality goals without measurable targets | Express key non-functional goals with measurable or testable criteria whenever evidence allows. |
| Hiding uncertainty | Record assumptions, risks, blockers, and open questions explicitly. |
