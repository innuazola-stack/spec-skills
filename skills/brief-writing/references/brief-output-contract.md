# Brief Output Contract

Use this contract before drafting or reviewing a final brief. The brief can be a standalone Markdown document, a section inside another planning artifact, or a concise response in chat. Saved or approval-bound briefs must meet the stricter gates below.

## Required Behavior

- 必须使用专业、正式的简体中文，除非用户明确要求其他语言。
- 必须面向人类决策者写作，使用自然、书面、可读的解释，不得写成解析器输入或内部 agent 记录。
- 必须简洁、清晰，只表达最终观点和结论。
- 保存或用于评审/审批的简报，最前面必须是修订表；每次更新必须诚实记录版本、日期、作者、状态、修订内容和依据。
- 必须根据文档目的设计专业结构和层级。
- 必须根据目的使用 text、table、Mermaid、LaTeX 等表达形式。
- 所有重要事实、观点、指标、约束、风险、决策和建议都必须有项目证据标记。
- 方法论来源只能用于结构或质量标准，不能当作产品事实。
- 必须区分已知事实、假设、开放问题、阻塞项和风险。
- 必须明确下一步交付物和承接关系。
- 交付前必须删除无关内容、冗余细节、TODO、占位符和过程叙述。

## Structure Options

### 紧凑一页简报

Use when the user asks for a one-pager, kickoff note, executive brief, or early alignment memo.

1. 标题与状态
2. 决策摘要
3. 背景与问题
4. 目标与非目标
5. 范围与约束
6. 推荐方向
7. 成功标准
8. 风险、假设与待确认问题
9. 交付物与下一步
10. 参考资料

### 产品简报

Use when the brief should align product strategy before PRD, design, build, or launch.

1. 修订记录
2. 决策摘要
3. 背景与机会
4. 用户、场景与问题
5. 目标、非目标与成功指标
6. 范围、约束与依赖
7. 产品方向与核心能力
8. 市场、竞品或替代方案
9. 发布、资源与里程碑
10. 风险、假设与待确认问题
11. 交付物与后续文档
12. 参考资料

### 设计简报

Use when product, UX, UI, research, content, brand, or design system work needs a clear frame.

1. 修订记录
2. 决策摘要
3. 背景与设计问题
4. 目标用户与使用场景
5. 设计目标、非目标与成功标准
6. 范围、约束与设计输入
7. 品牌、内容、可访问性与设计系统要求
8. 交付物、格式与交接要求
9. 评审节奏、决策人和里程碑
10. 风险、假设与待确认问题
11. 参考资料

### 技术简报

Use when engineering needs a concise decision frame before a full tech spec, HLD, RFC, or implementation task plan.

1. 修订记录
2. 决策摘要
3. 产品意图与技术背景
4. 问题边界与系统上下文
5. 技术目标、非目标与质量属性
6. 推荐技术方向
7. 备选方案与取舍
8. 架构、数据、接口、运行时或部署影响
9. 安全、隐私、可观测性、运维与回滚影响
10. 验证计划与成功标准
11. 风险、依赖、假设与待确认问题
12. 后续交付物
13. 参考资料

### 产品-设计-技术混合简报

Use when one artifact must align product, design, and engineering at kickoff.

1. 修订记录
2. 决策摘要
3. 背景、用户问题与业务目标
4. 范围、非目标、约束与依赖
5. 产品方向
6. 设计方向与交付物
7. 技术方向与可行性判断
8. 成功指标、验收信号与验证计划
9. 方案取舍、风险与待确认问题
10. 评审、决策人与下一步
11. 参考资料

## Evidence Rules

| Claim Type | Required Evidence |
| --- | --- |
| User need, pain point, persona, scenario | User research, support ticket, interview, analytics, stakeholder source, or marked assumption |
| Business goal, budget, market, deadline | Business source, roadmap, leadership input, finance source, or marked assumption |
| Feature, scope, non-goal | Product source, stakeholder decision, PRD, issue, design input, or marked assumption |
| Design requirement | Design system, brand guide, UX research, accessibility rule, content guideline, stakeholder source, or marked assumption |
| Technical constraint | Architecture source, codebase inspection, HLD, system owner input, security/data/ops source, or marked assumption |
| Metric or success target | Analytics source, business goal, experiment plan, historical baseline, or marked assumption |
| Risk or dependency | Source-backed owner/system/team/date, or marked unknown |

## Blocking Gates

Fail the brief instead of marking it ready when any gate fails:

| Gate | Blocks When |
| --- | --- |
| Decision clarity | The brief does not state what decision, alignment, or handoff it enables. |
| Evidence integrity | Material claims lack evidence markers or are presented as fact when only assumed. |
| Scope boundary | In-scope and out-of-scope items are missing where scope ambiguity could affect execution. |
| Success criteria | No measurable or reviewable success standard exists. |
| Constraint visibility | Relevant budget, timeline, design, technical, legal, data, security, accessibility, or operational constraints are hidden. |
| Handoff readiness | Deliverables, owner/reviewer, decision path, or next artifact are missing for an approval-bound brief. |
| Final-view only | The output includes drafting notes, hidden reasoning, TODO placeholders, or process narration. |
| Reference round trip | Cited markers are missing from references, or listed references are never cited. |
| Revision first | A saved or approval-bound brief does not begin with a revision table. |
| Human-readable language | The brief reads like a schema, trace dump, or machine artifact rather than a professional document for people. |
| Expression fit | The brief uses only dense prose where tables, diagrams, or formulas are needed for clarity, or forces visual/formula formats that do not serve the purpose. |
| Topic focus | The brief includes content unrelated to its stated purpose, decision, or audience. |
| Concision | Redundant sections, repeated claims, or unnecessary source-document detail obscure the decision. |

## Scoring Rubric

Score each dimension from 0 to 3.

| Dimension | 0 | 1 | 2 | 3 |
| --- | --- | --- | --- | --- |
| Decision clarity | No decision stated | Decision implied | Decision stated | Decision, owner, recommendation, and approval path clear |
| Problem grounding | Solution-first | Weak problem | Evidence-backed problem | Problem tied to user/business/system impact |
| Scope control | Missing | Partial | Clear in/out scope | Scope plus constraints, dependencies, and non-goals |
| Evidence | Unsupported | Some markers | Most material claims sourced | All material claims sourced or labeled unknown |
| Success criteria | Missing | Vague | Reviewable | Measurable, owned, and linked to goals |
| Tradeoffs | Missing | One-sided | Alternatives noted | Alternatives, rationale, costs, and consequences clear |
| Handoff | Missing | Next step vague | Deliverables listed | Owners, formats, dates, reviewers, and next artifacts clear |
| Scannability | Dense | Some headings | Mostly scannable | Short, front-loaded, table-driven, easy to review |
| Professional language | Informal, mechanical, or awkward | Mostly readable but inconsistent | Formal and clear | Formal, natural, concise, and appropriate for human stakeholders |
| Expression design | One format used regardless of need | Some helpful formatting | Fit-for-purpose tables/diagrams/formulas | Multiple forms used only where they improve understanding and review |
| Topic focus | Off-topic material present | Some unnecessary detail | Mostly focused | Every section directly serves the brief purpose |

Ready threshold:

- Approval-bound brief: every blocking gate passes and average score is at least 2.5.
- Draft brief: decision, evidence, scope, and uncertainty gates pass; open gaps are labeled.
- Chat-only brief: concise answer is acceptable, but do not claim approval readiness unless gates pass.

## Review Checklist

- Does the title reveal the initiative and brief type?
- Is the first substantive section a revision table with an honest update record?
- Does the opening summary say what is being decided?
- Are readers, owner, reviewers, and status clear when approval is expected?
- Is the document written in professional Simplified Chinese for human readers?
- Is the problem evidence-backed and separated from the proposed solution?
- Are goals, non-goals, scope, constraints, and dependencies explicit?
- Are material facts cited and assumptions labeled?
- Are all cited sources listed at the end, and are all listed sources cited in the body?
- Is the recommended direction proportional to the evidence?
- Are alternatives and tradeoffs included when a technical or strategic decision is involved?
- Are success criteria measurable or reviewable?
- Are prose, tables, diagrams, and formulas used only where they improve the reader's understanding?
- Are risks and open questions actionable, with owners when known?
- Are deliverables and handoff expectations concrete?
- Is every section directly related to the brief purpose and topic?
- Is the brief short enough for the intended audience to actually read?
- Has redundant or source-document-level detail been removed?
