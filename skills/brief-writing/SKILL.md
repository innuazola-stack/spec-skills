---
name: brief-writing
description: Use when Codex needs to write, rewrite, review, or update a professional Simplified Chinese product brief, product design brief, UX/design brief, technical brief, engineering design brief, tech spec brief, one-pager, kickoff brief, or cross-functional decision brief. Trigger when turning research, notes, ideas, PRDs, HLDs, specs, discovery material, or stakeholder input into a concise source-backed brief that aligns product, design, engineering, QA, business, and operations readers.
---

# Brief Writing

Use this skill to produce concise, source-backed Simplified Chinese briefs that help a team decide what to do next. A brief is not a full PRD, HLD, or implementation spec; it is the alignment layer that states the problem, decision context, constraints, options, success criteria, and next handoff.

## Basic Quality Requirements

Every brief must satisfy these requirements:

1. 必须使用专业、正式的简体中文。
2. 文档读者是人类。使用自然、面向人的解释，不写机器化片段、 schema 式堆砌或内部 agent 口吻。
3. 根据文档目的选择表达形式：结论用文字，结构、范围、风险、追踪关系用表格，流程、状态、依赖关系用 Mermaid，公式、指标口径用 LaTeX。
4. 使用书面用语、清晰层级和专业章节设计。
5. 只表达最终观点和结论。不得出现过程性内容、草稿说明、隐藏推理、泛泛背景或无关材料。
6. 内容必须真实、有据可循。所有重要观点、事实、指标、风险、约束和建议都要有出处标记，并在文末记录参考文献。
7. 文档最前面必须是修订表。每次更新都要严谨、诚实地记录版本、日期、作者、状态、修订内容和依据。
8. 文档必须紧扣目的和主题。任何无关内容都不得放入。
9. 文档必须简洁、清晰，禁止冗余；即使源文档很长，也只保留对决策有用的内容。

## Load References

Load only what the task needs:

- `references/brief-methodology.md`: distilled product, design, technical-spec, and documentation-writing practices from 12 external sources.
- `references/brief-output-contract.md`: required structure options, evidence rules, review gates, and scoring rubric.
- `assets/Brief.template.md`: reusable Simplified Chinese brief template.

## Workflow

1. Identify the brief type, decision to unlock, target readers, stage of work, expected length, and available sources.
2. Build a source inventory before writing. Use project evidence IDs such as `[BIZ-01]`, `[USER-01]`, `[RESEARCH-01]`, `[DESIGN-01]`, `[TECH-01]`, `[DATA-01]`, `[OPS-01]`, `[SEC-01]`, and `[STAKEHOLDER-01]`.
3. Read `references/brief-methodology.md` when selecting the writing logic, section model, and level of detail.
4. Read `references/brief-output-contract.md` before composing or reviewing the final brief.
5. Choose the brief mode:
   - Product brief: align on problem, audience, value, scope, success metrics, market/context, and release direction.
   - Design brief: align on user problem, design goal, audience, constraints, brand/design-system inputs, deliverables, review path, and handoff needs.
   - Technical brief: align on product intent, technical approach, architecture boundary, constraints, tradeoffs, risks, validation, and implementation handoff.
   - Hybrid brief: connect product intent, design requirements, and technical constraints in one concise artifact.
6. Write final-view content only. Do not include research narration, drafting commentary, hidden reasoning, or generic textbook material.
7. Select expression forms deliberately. Use text, tables, Mermaid, and LaTeX only when each form improves readability or reviewability for the brief purpose.
8. Cite every material product, user, business, design, technical, metric, timeline, dependency, or risk claim with project evidence markers. Use methodology markers only for document-structure rationale.
9. Make uncertainty visible as assumptions, open questions, risks, blockers, or decision requests.
10. If the brief is saved as a document or intended for approval, start with a revision record and end with a complete references section.
11. Remove unused template sections, placeholders, and content that does not directly serve the brief purpose.
12. Self-review against the checklist and rubric in `references/brief-output-contract.md` before claiming the brief is ready.

## Brief Logic

Use this order unless the user's requested format is stricter:

1. Decision: What decision or alignment should this brief enable?
2. Context: Why this matters now, who is affected, and what evidence exists?
3. Problem: What user, business, design, or technical problem must be solved?
4. Boundary: What is in scope, out of scope, constrained, assumed, or unknown?
5. Direction: What product/design/technical direction is recommended and why?
6. Evaluation: What success metrics, acceptance signals, or review criteria decide whether the direction worked?
7. Handoff: What deliverables, owners, milestones, decisions, and next artifacts follow?

## Hard Rules

- 除非用户明确要求其他语言，否则必须使用专业、正式的简体中文。
- 必须面向人类读者写作，语言自然、严谨、可读，不得写成解析器输入或内部 agent 记录。
- 所有保存或用于评审/审批的简报，最前面必须是修订表；每次更新都必须诚实记录变化和依据。
- 简报必须简洁，通常控制在一到三页；用户要求 one-pager 时应更短。
- 先给结论和决策，再给依据和细节。
- 使用清晰标题、合理层级和专业章节顺序。
- 根据目的使用 text、table、Mermaid、LaTeX 等表达形式；只有能提升理解或评审效率时才保留。
- 文档必须是 final-view：不得包含过程叙述、隐藏推理、草稿备注、TODO、占位符或泛泛填充。
- 发现阶段或设计探索阶段不得过早规定设计/工程解法。
- 不得隐藏约束；预算、时间、设计系统、技术、数据、安全、合规、运维等约束都要明确呈现。
- 不得编造事实、指标、日期、预算、依赖、用户、审批、风险或技术细节。
- 所有重要观点和依据必须有出处标记，并在文末列出所有被引用的参考资料。
- 范围、需求、约束、选项、风险、追踪关系优先用表格表达。
- 流程、状态机、架构边界、依赖关系和评审路径需要可视化时使用 Mermaid。
- 指标口径、覆盖率、容量、转化率等需要精确定义时使用 LaTeX。
- 产品简报聚焦 what/why；技术简报聚焦 how/tradeoffs；设计简报聚焦用户、约束、交付物和反馈路径。
- 删除任何与简报目的和主题无关的内容。
- 交付前压缩冗余表达。

## Common Mistakes

| Mistake | Correct Behavior |
| --- | --- |
| Expanding a brief into a full PRD or HLD | Keep only the alignment-critical decisions and link to deeper artifacts. |
| Starting with features instead of the problem | State the user/business/technical problem and success criteria first. |
| Treating the brief as a static artifact | Note revision status, decision owner, approval path, and open questions. |
| Writing vague deliverables | Specify exact artifact formats, handoff expectations, owners, and dates when known. |
| Mixing facts with assumptions | Mark unknowns explicitly and separate evidence from judgment. |
| Over-constraining creative work | State goals and constraints without prematurely dictating the solution. |
| Omitting technical feasibility | For product/design briefs, surface known stack, integration, accessibility, legal, data, security, and operational constraints when relevant. |
| Omitting user value | For technical briefs, retain product intent and user/business value so engineering decisions remain grounded. |
