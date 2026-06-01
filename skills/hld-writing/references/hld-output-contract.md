# HLD Output Contract

Use this contract before writing or reviewing a final HLD.

## Evidence Rules

- Assign project evidence IDs before writing. Recommended prefixes:
  - `[BIZ-xx]`: business brief, strategy, KPI, approval, contract.
  - `[PRD-xx]`: PRD, requirement table, user story, acceptance criterion.
  - `[TECH-xx]`: codebase, architecture note, engineering proposal, dependency analysis.
  - `[DATA-xx]`: schema, analytics, data contract, retention policy.
  - `[SEC-xx]`: security requirement, compliance policy, threat model.
  - `[OPS-xx]`: SLO, incident report, monitoring, deployment, runbook.
  - `[DESIGN-xx]`: UX flow, Figma, service blueprint, journey map.
- Cite every material claim about scope, architecture, quality targets, constraints, interfaces, data, security, rollout, risks, and decisions.
- Methodology markers `[Mxx]` can support document structure or writing standards. They cannot prove product facts.
- If evidence is missing, state the uncertainty as an assumption, risk, open question, or blocker. Do not invent.

## Required Opening

The HLD must begin with `修订记录`.

| Column | Requirement |
| --- | --- |
| 版本 | Use a clear version such as `v0.1`, `v1.0`, or the version already used in the document. |
| 日期 | Use the actual update date. |
| 作者 | Use the actual author when known. Use `Agent` only when the agent made the update. |
| 修订内容 | State the real change, not a vague phrase. |
| 依据 | Cite source, approval, issue, or user request marker. If no formal approval exists, say so honestly. |

## Recommended Structure

| Section | Purpose | Typical Forms |
| --- | --- | --- |
| 修订记录 | Audit the document's evolution. | Table |
| 文档概述 | State purpose, readers, status, and evidence basis. | Prose/table |
| 背景与目标 | Explain the business and product problem the architecture solves. | Prose/table |
| 架构摘要 | Present the selected high-level solution and core design principles. | Prose + context diagram |
| 范围边界 | Define in-scope, out-of-scope, system boundary, and external dependencies. | Boundary table |
| 干系人与关注点 | Map reader groups to architecture concerns. | Table |
| 质量属性目标 | State measurable or reviewable non-functional targets. | Quality attribute table |
| 约束、假设与依赖 | Separate hard constraints, assumptions, and dependencies. | Table |
| 架构视图 | Explain context, module/container, runtime, deployment, data, security, and operations views as needed. | Mermaid + prose |
| 数据与接口设计 | Describe data ownership, contracts, APIs, events, consistency, and lifecycle. | Tables/diagrams |
| 安全、隐私与合规设计 | Show identity, authorization, secrets, privacy, compliance, and trust boundaries. | Control matrix |
| 可靠性、性能与容量设计 | State availability, failure handling, scaling, latency, throughput, and capacity model. | Tables/LaTeX |
| 运维、可观测性与发布设计 | Describe monitoring, logging, alerting, deployment, rollback, and runbook expectations. | Matrix/sequence |
| 架构决策与权衡 | Record architecture-significant decisions and consequences. | ADR table |
| 风险、技术债与待确认事项 | Make unresolved risk and debt visible with ownership and mitigation. | Risk table |
| 需求追踪矩阵 | Trace requirements to architecture elements, quality goals, decisions, and validation evidence. | Traceability table |
| 参考文献 | List every cited project and methodology source. | Numbered list/table |

## Expression Forms

| Form | Use For | Avoid |
| --- | --- | --- |
| Text | Final conclusions, rationale, implications. | Long process narration or generic theory. |
| Table | Scope, evidence, decisions, risks, quality targets, interfaces, traceability. | Dense paragraphs that compare many attributes. |
| Mermaid flowchart | Context, components, deployment, data flow, dependencies. | Decorative diagrams with no review value. |
| Mermaid sequence | Critical runtime interactions, auth flow, async processing, failure handling. | Simple CRUD flows that a table explains better. |
| Mermaid state | Lifecycle, workflow, state transitions, retry/circuit-breaker states. | Linear procedures. |
| LaTeX | Availability, capacity, scoring, cost or throughput formulas. | Formulas without defined variables or evidence. |

## Final-View Rules

The HLD must not contain:

- hidden reasoning, chain-of-thought, or agent self-description;
- phrases such as "我将", "下一步我会", "调研过程", "草稿", "待我确认";
- source-gathering narration;
- unrelated product strategy, implementation task lists, or generic architecture education;
- uncited claims presented as facts.

The HLD may contain:

- assumptions, risks, blockers, and open questions when clearly labeled;
- follow-up decisions if they are part of the final architecture governance content;
- concise rationale for architecture choices.

## Review Checklist

Before delivery, verify:

- The document is written in professional Simplified Chinese.
- The first section is `修订记录`.
- The document states purpose, readers, status, scope, and evidence basis.
- The system boundary and external dependencies are explicit.
- Architecture views are mutually consistent in names, components, interfaces, and direction of data/control flow.
- Quality attributes are measurable or at least reviewable.
- Security, privacy, reliability, performance, operability, and cost concerns are addressed when relevant.
- Architecture decisions include rationale, tradeoffs, and consequences.
- Risks, technical debt, assumptions, and open questions are not hidden.
- Every material claim has a source marker.
- The `参考文献` section lists every source marker used.
- Content is concise, final, and directly tied to the HLD purpose.
