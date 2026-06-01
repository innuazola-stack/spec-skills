# PRD Output Contract

## Required Language And Tone

- Use Simplified Chinese.
- Use formal written language.
- Address human readers with clear context, concise conclusions, and professional structure.
- Avoid informal filler, vague claims, decorative prose, and generic product-management lectures.

## Document-Level Contract

The PRD must begin with this section:

```markdown
## 修订记录

| 版本 | 日期 | 作者 | 修订内容 | 依据/审批 |
| --- | --- | --- | --- | --- |
| v0.1 | YYYY-MM-DD | <作者> | 初始版本。 | <来源或审批依据> |
```

Rules:

- Use the current date for the new revision entry unless the user supplies another date.
- Preserve prior revision records when updating an existing PRD.
- Never claim approval that is not evidenced.
- If the update is based only on user instruction, write `用户指令` as the basis.

## Required Sections

| Section | Required Content | Quality Bar |
| --- | --- | --- |
| 修订记录 | Version, date, author, change summary, evidence or approval basis. | First section, honest, complete. |
| 文档摘要 | Product, purpose, target readers, decision or delivery boundary. | 3-6 concise bullets or short prose. |
| 背景与问题 | User/business problem, current pain, evidence, urgency. | Source-backed; no generic market claims. |
| 目标与成功指标 | Product goals, non-goals if needed, primary metrics, guardrails. | Measurable, source-backed, with metric definitions. |
| 用户与使用场景 | Primary users, scenarios, jobs to be done, edge cases. | Tied to real evidence or explicit assumptions. |
| 范围定义 | In scope, out of scope, assumptions, constraints. | Prevents scope creep and ambiguity. |
| 用户旅程或业务流程 | Core flow, exception flow, state or dependency. | Mermaid when visual clarity helps. |
| 功能需求 | Requirement ID, priority, description, rationale, source, acceptance link. | Testable and traceable. |
| 非功能需求与约束 | Performance, security, privacy, accessibility, reliability, observability, compliance, compatibility, maintainability as relevant. | Explicit pass/fail or measurable criteria. |
| 数据、埋点与度量方案 | Events, properties, metrics, dashboards, owner, decision thresholds. | Enables post-release evaluation. |
| 验收标准 | Given/When/Then or pass/fail acceptance criteria. | QA and engineering can verify directly. |
| 发布、灰度与回滚 | Release phases, feature flags/cohorts, monitoring, support, rollback triggers. | Safe launch plan when applicable. |
| 依赖、风险与开放问题 | External dependencies, product/technical risks, unresolved questions, owner, due date. | Honest; blockers clearly marked. |
| 需求追踪矩阵 | Source to goals, requirements, acceptance, metrics. | Shows evidence coverage. |
| 参考文献 | Every project and external source cited. | Complete, stable, and at the end. |

## Citation Rules

- Use project source markers for product facts:
  - `[BIZ-01]` for business strategy, goals, or stakeholder input.
  - `[USER-01]` for user research, interviews, support tickets, or feedback.
  - `[DATA-01]` for analytics, experiment, benchmark, or operational data.
  - `[DESIGN-01]` for design files, flows, prototypes, or UX decisions.
  - `[TECH-01]` for architecture, constraints, API contracts, security, or operations.
  - `[LEGAL-01]` for compliance, policy, privacy, or contractual constraints.
- Use methodology markers `[M01]` to `[M16]` only for PRD structure and quality principles.
- A paragraph with multiple factual claims may cite multiple markers.
- If no source exists, mark the item as assumption, open question, risk, or blocker.
- Every factual row in the summary, goal, user, scope, requirement, non-functional, metric, acceptance, release, risk, dependency, open-question, and traceability tables must include at least one source marker.
- Every cited marker must appear in `参考文献`.
- Every source listed in `参考文献` must be cited in the body. Do not keep unused methodology references for decoration.
- Methodology references must appear in the body at the point where they justify document structure, acceptance rigor, traceability, non-functional coverage, measurement design, or release safety. They must not be the sole support for product facts.

## Blocking Gates

The PRD is not ready if any blocking gate fails.

| Gate | Blocking Condition | Required Response |
| --- | --- | --- |
| Revision-first gate | First visible line is not `## 修订记录`. | Move revision history to the top before any title or summary. |
| Source-backed gate | A material statement or table row lacks a source marker and is not explicitly an assumption, open question, risk, blocker, or dependency. | Add source marker or move the item to uncertainty handling. |
| Reference round-trip gate | A body marker is missing from `参考文献`, or `参考文献` lists a marker unused in the body. | Fix citations before delivery. |
| Methodology grounding gate | Methodology sources are listed but not cited in the body. | Cite methodology markers where they justify PRD structure or quality model. |
| Product-fact gate | Methodology marker is the only support for a product fact. | Replace with project evidence or mark as assumption/open question. |
| Requirement gate | Requirement rows lack ID, priority, source, or acceptance link. | Complete the row or block the PRD. |
| Acceptance gate | Acceptance criteria are not verifiable as pass/fail. | Rewrite as observable conditions. |
| Final-view gate | Process narration, TODO, placeholder, "待补充", or drafting notes appear. | Remove them or block the PRD. |
| Unknowns gate | Missing facts are hidden or smoothed over. | Add explicit assumptions, risks, blockers, or open questions. |

When blocked, write a short `PRD 质量门禁结论` section after the revision table and before the normal PRD body. State `状态：blocked`, list blocking findings, required evidence, and owner/date when known. Do not present the document as ready.

## Requirement Table Contract

```markdown
| ID | 优先级 | 需求 | 说明 | 依据 | 验收标准 |
| --- | --- | --- | --- | --- | --- |
| FR-001 | P0 | <需求结论> | <必要说明> | [SOURCE-ID] | AC-001 |
```

Priority:

- `P0`: Release blocker.
- `P1`: Core value requirement.
- `P2`: Important but can be deferred with explicit trade-off.
- `P3`: Nice-to-have or future-phase candidate.

## Acceptance Criteria Contract

Use pass/fail statements. Prefer Given/When/Then when interaction or state matters:

```markdown
| ID | 对应需求 | 验收标准 | 验证方式 | 依据 |
| --- | --- | --- | --- | --- |
| AC-001 | FR-001 | Given <前置条件>, When <动作>, Then <可观察结果>. | 测试/评审/监控 | [SOURCE-ID] |
```

## Traceability Matrix Contract

```markdown
| 来源 | 目标 | 需求 | 验收标准 | 指标/监控 |
| --- | --- | --- | --- | --- |
| [SOURCE-ID] | G-001 | FR-001 | AC-001 | MET-001 |
```

## Final Review Checklist

- The first visible section is `修订记录`.
- The PRD is written in Simplified Chinese and formal written style.
- The document contains only final conclusions, not process narration.
- Every material claim has a source marker or is labeled as assumption/open question/risk/blocker.
- Every table row containing a factual assertion has a source marker.
- Every body citation appears in `参考文献`, and every reference item is cited in the body.
- Methodology references are cited in the body for structure and quality, not used as product facts.
- Scope includes in-scope and out-of-scope items when scope ambiguity is possible.
- Requirements are testable, prioritized, and traceable.
- Acceptance criteria are verifiable.
- Non-functional requirements are present when relevant to software delivery.
- Metrics and analytics are defined when success measurement matters.
- Rollout and rollback are defined when release risk exists.
- References include all cited project and methodology sources.
- The document is concise and contains no unrelated content.
- `tools/validate_prd_document.py <prd-path>` passes when the PRD is saved as Markdown.
