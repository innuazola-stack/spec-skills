# PRD Intake 输出契约

## 修订记录

| 版本 | 日期 | 修订人 | 修订内容 | 依据 |
| --- | --- | --- | --- | --- |
| v1.0 | 2026-05-25 | Codex | 将输出契约重构为 `prd-intake` 的唯一权威事实模型，明确 canonical contract、渲染块、审计层、质量门禁和 Human/Agent PRD 渲染闭环。 | 用户确认：以 output contract 为核心推导渲染逻辑 |
| v1.1 | 2026-05-25 | Codex | 收敛 review 发现的根因问题：对象本体、状态枚举、gate 语义、STOP 状态、Human/Agent 条件阻断和追踪层级。 | 设计审计修复 |
| v1.2 | 2026-05-25 | Codex | 完成对象化迁移：统一 `objects[ID].payload`、移除事实双写、收敛 gate status、补齐 STOP 状态、用户确认来源和决策追踪。 | 收敛审计修复 |
| v1.3 | 2026-05-25 | Codex | 补齐 `Q/ASM` 闭环字段、`REF.related_refs`、per-type status 约束和 envelope ID 完整性规则。 | 收敛审计修复 |
| v1.4 | 2026-05-26 | Codex | 区分 schema shape、语义一致 envelope 示例和最小 smoke fixture；补齐主结构 `object_index`、decision traceability 类型化状态和 Agent Source Of Truth 的 `ASM` 支撑。 | 收敛审计修复 |
| v1.5 | 2026-05-26 | Codex | 将 `decision_traceability.status` 纳入统一状态语义，补强最终 envelope 示例中 open Q/ASM 的非阻断证据，并修正 TRACE relation 枚举写法。 | 收敛审计修复 |
| v1.6 | 2026-05-26 | Codex | 补强 contract version 同步门禁，并将 `decision_traceability.status` 类型约束纳入 validator 最低实现。 | 收敛审计修复 |
| v1.7 | 2026-05-26 | Codex | 将 L4 envelope 示例补齐为真正 execution-ready，并把 ready、traceability、version sync 纳入 validator 最低实现。 | 收敛审计修复 |
| v1.8 | 2026-05-26 | Codex | 收紧 validator 的 rendered `REQ` 追踪口径，并用 `META` 替代示例 gate 自引用证据。 | 收敛审计修复 |

## 1. 契约定位

`prd-intake` 的核心产物不是一份自然语言 PRD，而是一份 canonical structured contract。Human PRD 和 Agent PRD 都只是这份 contract 的同级渲染结果。

本文件是 `prd-intake` 的最高优先级输出契约。`README.md` 只能解释技能目标和工作流；`human-prd-template.md` 与 `agent-prd-template.md` 只能定义渲染规则。任何模板、样例或说明与本文件冲突时，以本文件为准。

输出必须遵守五条硬规则：

1. 先有 canonical object，后有正文事实。
2. 先有 `RB`，后有 PRD 正文块。
3. 先通过 gate，后声明 final 或 execution-ready。
4. Human PRD 与 Agent PRD 是 sibling render，不存在互相派生。
5. 无法追踪到 contract 的内容只能成为 `ASM`、`Q`，或被 gate 阻断。

## 2. 输入契约

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `raw_idea` | 是 | 用户输入的原始想法，可以是一句话、会议记录、Issue、访谈摘要、草稿或长文。 |
| `source_context` | 否 | 用户提供的背景材料、链接、文件、竞品、业务约束或现有系统说明。 |
| `requested_output` | 否 | 用户要求 Human PRD、Agent PRD、完整文档包，或只做 intake 澄清。 |
| `constraints` | 否 | 已知业务、技术、法律、时间、组织、平台或交付限制。 |
| `language_preference` | 否 | 只影响附加本地化版本。canonical Human PRD 必须使用专业简体中文；Agent PRD 与 execution-facing 交付物必须使用英文。 |

输入不足时，不得补写为事实。缺失信息必须进入 `assumptions`、`open_questions`，或触发下一轮 intake 问题。

## 3. Canonical Structured Contract

技能内部必须维护以下顶层结构。字段名使用英文，字段内容可按目标产物使用中文或英文；Agent-facing 内容必须可稳定转为英文。下方 JSON 是结构骨架：为保持契约可读性，部分对象 payload 只展示 `id`/`type` 占位；真实输出必须按第 5 节对象 schema 填充完整 payload，且不得产生悬空 canonical ID。

```json
{
  "contract_version": "string",
  "intake_id": "string",
  "source_idea": {
    "raw_idea": "string",
    "source_context_refs": ["SRC-001"],
    "created_at": "ISO-8601 datetime"
  },
  "core": "CORE-001",
  "scope": {
    "in_scope": ["SCOPE-001"],
    "out_of_scope": ["OOS-001"],
    "mvp_boundary": "string",
    "roadmap": ["PHASE-001"]
  },
  "requirements": ["REQ-001"],
  "acceptance_criteria": ["AC-001"],
  "success_metrics": ["MET-001"],
  "implementation_model": {
    "control_flow": ["FLOW-001"],
    "data_flow": ["DATA-001"],
    "modules": ["MOD-001"],
    "technical_decisions": ["TECH-001"],
    "state_transitions": ["STATE-001"],
    "data_contracts": ["DCT-001"]
  },
  "agent_execution": {
    "input_contracts": ["IN-001"],
    "execution_rules": ["EXE-001"],
    "verification_cases": ["VER-001"],
    "output_deliverables": ["OUT-001"],
    "stop_conditions": ["STOP-001"],
    "done_criteria": ["DONE-001"]
  },
  "risks": ["RISK-001"],
  "quality_bars": ["BAR-001"],
  "assumptions": ["ASM-001"],
  "open_questions": ["Q-001"],
  "references": ["REF-001"],
  "sources": ["SRC-001"],
  "traceability": ["TRACE-001"],
  "render_blocks": ["RB-001"],
  "document_metadata": ["META-001"],
  "quality_gates": ["GATE-001"],
  "render_status": {
    "human_prd": "not_requested | draft | review_ready | blocked",
    "agent_prd": "not_requested | draft | execution_ready | blocked"
  },
  "objects": {
    "CORE-001": {
      "type": "CORE",
      "payload": {
        "id": "CORE-001",
        "product_name": "string",
        "one_line_summary": "string",
        "target_users": ["USER-001"],
        "personas": ["USER-001"],
        "problem_statement": "string",
        "value_proposition": "string",
        "source_refs": ["SRC-001"],
        "assumption_refs": ["ASM-001"],
        "status": "draft | confirmed | blocked"
      }
    },
    "REQ-001": {
      "type": "REQ",
      "payload": {
        "id": "REQ-001",
        "title": "string",
        "description": "string",
        "user_value": "string",
        "priority": "must | should | could",
        "phase": "PHASE-001",
        "scope_ref": "SCOPE-001",
        "acceptance_criteria": ["AC-001"],
        "source_refs": ["SRC-001"],
        "status": "draft | confirmed | blocked"
      }
    },
    "AC-001": {
      "type": "AC",
      "payload": {
        "id": "AC-001",
        "requirement_id": "REQ-001",
        "criterion": "string",
        "verification_method": "manual_review | test | metric | inspection",
        "blocking": true
      }
    },
    "RB-001": {
      "type": "RB",
      "payload": {
        "id": "RB-001",
        "target": "human_prd | agent_prd",
        "section": "string",
        "content_type": "text | table | mermaid | latex | html | checklist | json_schema",
        "contract_refs": ["REQ-001", "AC-001"],
        "source_refs": ["SRC-001"],
        "allowed_inference": "none | summary | translation | formatting | bounded_synthesis",
        "unsupported_claims": [],
        "status": "ready | blocked"
      }
    },
    "ASM-001": {
      "type": "ASM",
      "payload": {"id": "ASM-001"}
    },
    "BAR-001": {
      "type": "BAR",
      "payload": {"id": "BAR-001"}
    },
    "DATA-001": {
      "type": "DATA",
      "payload": {"id": "DATA-001"}
    },
    "DCT-001": {
      "type": "DCT",
      "payload": {"id": "DCT-001"}
    },
    "DONE-001": {
      "type": "DONE",
      "payload": {"id": "DONE-001"}
    },
    "EXE-001": {
      "type": "EXE",
      "payload": {"id": "EXE-001"}
    },
    "FLOW-001": {
      "type": "FLOW",
      "payload": {"id": "FLOW-001"}
    },
    "GATE-001": {
      "type": "GATE",
      "payload": {"id": "GATE-001"}
    },
    "IN-001": {
      "type": "IN",
      "payload": {"id": "IN-001"}
    },
    "MET-001": {
      "type": "MET",
      "payload": {"id": "MET-001"}
    },
    "META-001": {
      "type": "META",
      "payload": {"id": "META-001"}
    },
    "MOD-001": {
      "type": "MOD",
      "payload": {"id": "MOD-001"}
    },
    "OOS-001": {
      "type": "OOS",
      "payload": {"id": "OOS-001"}
    },
    "OUT-001": {
      "type": "OUT",
      "payload": {"id": "OUT-001"}
    },
    "PHASE-001": {
      "type": "PHASE",
      "payload": {"id": "PHASE-001"}
    },
    "Q-001": {
      "type": "Q",
      "payload": {"id": "Q-001"}
    },
    "REF-001": {
      "type": "REF",
      "payload": {"id": "REF-001"}
    },
    "RISK-001": {
      "type": "RISK",
      "payload": {"id": "RISK-001"}
    },
    "SCOPE-001": {
      "type": "SCOPE",
      "payload": {"id": "SCOPE-001"}
    },
    "SRC-001": {
      "type": "SRC",
      "payload": {"id": "SRC-001"}
    },
    "STATE-001": {
      "type": "STATE",
      "payload": {"id": "STATE-001"}
    },
    "STOP-001": {
      "type": "STOP",
      "payload": {"id": "STOP-001"}
    },
    "TECH-001": {
      "type": "TECH",
      "payload": {"id": "TECH-001"}
    },
    "TRACE-001": {
      "type": "TRACE",
      "payload": {"id": "TRACE-001"}
    },
    "USER-001": {
      "type": "USER",
      "payload": {"id": "USER-001"}
    },
    "VER-001": {
      "type": "VER",
      "payload": {"id": "VER-001"}
    }
  },
  "object_index": {
    "CORE": ["CORE-001"],
    "REQ": ["REQ-001"],
    "AC": ["AC-001"],
    "RB": ["RB-001"],
    "ASM": ["ASM-001"],
    "BAR": ["BAR-001"],
    "DATA": ["DATA-001"],
    "DCT": ["DCT-001"],
    "DONE": ["DONE-001"],
    "EXE": ["EXE-001"],
    "FLOW": ["FLOW-001"],
    "GATE": ["GATE-001"],
    "IN": ["IN-001"],
    "MET": ["MET-001"],
    "META": ["META-001"],
    "MOD": ["MOD-001"],
    "OOS": ["OOS-001"],
    "OUT": ["OUT-001"],
    "PHASE": ["PHASE-001"],
    "Q": ["Q-001"],
    "REF": ["REF-001"],
    "RISK": ["RISK-001"],
    "SCOPE": ["SCOPE-001"],
    "SRC": ["SRC-001"],
    "STATE": ["STATE-001"],
    "STOP": ["STOP-001"],
    "TECH": ["TECH-001"],
    "TRACE": ["TRACE-001"],
    "USER": ["USER-001"],
    "VER": ["VER-001"]
  }
}
```

`objects` 是事实源本体，必须保存每个 canonical object 的完整 payload。顶层数组只是索引，不能替代对象本体。任何渲染、审计或 gate 判断都必须以 `objects` 中的 payload 为准。
`object_index` 是从 `objects` 派生的必填索引，必须覆盖 `objects` 中全部对象；不得把它当作事实 payload 的替代品。
除 `core` 这种指向主对象的 ID 字段外，顶层字段都只是索引或视图；不得在顶层和 `objects[ID].payload` 中双写同一事实。若实现需要 summary view，必须从 `objects` 派生。

## 4. ID 体系

所有可被 PRD 正文引用的对象必须有稳定 ID。

| 前缀 | 对象 | 示例 |
| --- | --- | --- |
| `SRC` | 来源材料 | `SRC-001` |
| `REF` | 结构化引用对象 | `REF-001` |
| `CORE` | 产品核心事实 | `CORE-001` |
| `USER` | 用户、角色或 persona | `USER-001` |
| `SCOPE` | 范围内事项 | `SCOPE-001` |
| `OOS` | 范围外事项 | `OOS-001` |
| `REQ` | 需求 | `REQ-001` |
| `AC` | 验收标准 | `AC-001` |
| `MET` | 成功指标 | `MET-001` |
| `FLOW` | 控制流 | `FLOW-001` |
| `DATA` | 数据流或数据来源 | `DATA-001` |
| `MOD` | 模块 | `MOD-001` |
| `TECH` | 技术或产品实现决策 | `TECH-001` |
| `STATE` | 状态转移规则 | `STATE-001` |
| `DCT` | 数据契约 | `DCT-001` |
| `IN` | Agent 输入契约 | `IN-001` |
| `EXE` | Agent 执行规则 | `EXE-001` |
| `VER` | Agent 验证用例 | `VER-001` |
| `OUT` | Agent 交付物 | `OUT-001` |
| `STOP` | Agent 停止条件 | `STOP-001` |
| `DONE` | Agent 完成标准 | `DONE-001` |
| `BAR` | 质量红线 | `BAR-001` |
| `RISK` | 风险 | `RISK-001` |
| `ASM` | 假设 | `ASM-001` |
| `Q` | 开放问题 | `Q-001` |
| `PHASE` | 路线图阶段 | `PHASE-001` |
| `RB` | 渲染块 | `RB-001` |
| `META` | 文档元信息 | `META-001` |
| `GATE` | 质量门禁 | `GATE-001` |
| `TRACE` | 追踪关系 | `TRACE-001` |

ID 一旦进入同一 contract version，不得改变含义。Agent PRD 中所有 object-backed row 必须显式展示主对象 ID。不得用局部编号替代 canonical ID。

`GATE-*` 只表示本文件第 12 节的全局质量门禁。Agent PRD 中的本地验证、阻断失败和一致性检查必须使用 `VER-*`，可以引用相关 `GATE-*`，但不得创建新的本地 `GATE-*`。

## 5. 核心对象 schema

### 5.1 `CORE`: Product Core

```json
{
  "id": "CORE-001",
  "product_name": "string",
  "one_line_summary": "string",
  "target_users": ["USER-001"],
  "personas": ["USER-001"],
  "problem_statement": "string",
  "value_proposition": "string",
  "source_refs": ["SRC-001"],
  "assumption_refs": ["ASM-001"],
  "status": "draft | confirmed | blocked"
}
```

规则：

- Human PRD 中产品名称、摘要、问题、价值主张必须引用 `CORE-*` 或更具体的对象 ID。
- `CORE.status=blocked` 时，不得声明 Human PRD review-ready 或 Agent PRD execution-ready。
- `CORE` 不替代 `USER`、`SCOPE`、`REQ`、`AC` 等细粒度对象；它只承载产品核心判断。

### 5.2 `REQ`: Requirement

```json
{
  "id": "REQ-001",
  "title": "string",
  "description": "string",
  "user_value": "string",
  "priority": "must | should | could",
  "phase": "PHASE-001",
  "scope_ref": "SCOPE-001",
  "acceptance_criteria": ["AC-001"],
  "source_refs": ["SRC-001"],
  "status": "draft | confirmed | blocked"
}
```

规则：

- 每个 MVP `REQ` 必须至少关联一个 `AC`。
- `status=blocked` 的需求不得进入 final Human PRD 或 execution-ready Agent PRD。
- Human PRD 和 Agent PRD 不得新增 contract 中不存在的 `REQ`。

### 5.3 `AC`: Acceptance Criterion

```json
{
  "id": "AC-001",
  "requirement_id": "REQ-001",
  "criterion": "string",
  "verification_method": "manual_review | test | metric | inspection",
  "blocking": true
}
```

规则：

- `criterion` 必须可判断。
- `blocking=true` 且无法验证时，Agent PRD 必须 blocked。

### 5.4 `TECH`: Technical Decision

```json
{
  "id": "TECH-001",
  "decision": "string",
  "rationale": "string",
  "applies_to": ["MOD-001", "REQ-001"],
  "phase": "PHASE-001",
  "agent_constraint": "string"
}
```

规则：

- 技术选型必须是明确决策，不得列多个候选项后不做结论。
- 影响执行的 `TECH` 必须进入 Agent PRD 的 `Implementation Constraints`。
- 影响产品落地理解的 `TECH` 必须进入 Human PRD 的“如何实现”。

### 5.5 `Q`: Open Question

```json
{
  "id": "Q-001",
  "question": "string",
  "impact": "string",
  "phase": "PHASE-001",
  "owner": "human | product | engineering | legal | unknown",
  "blocks_human_prd": false,
  "blocks_agent_prd": true,
  "agent_handling": "defer | stop_and_ask | out_of_scope",
  "status": "open | resolved | deferred | superseded",
  "resolution_refs": ["SRC-002"]
}
```

规则：

- 开放问题必须说明影响和 owner。
- `blocks_human_prd=true` 且 `status=open` 时，Human PRD 不得 review-ready。
- `blocks_agent_prd=true` 且 `status=open` 时，Agent PRD 不得 execution-ready。
- `status=resolved` 必须有 `SRC.source_type=user_confirmation`、contract update 或其他可追踪 resolution evidence，并写入 `resolution_refs`。
- `status=deferred` 必须有明确 `phase` 和 `agent_handling`，且不得作为当前执行范围。
- Agent 不得自行关闭开放问题；只能通过 contract 更新或用户确认关闭。

### 5.6 `ASM`: Assumption

```json
{
  "id": "ASM-001",
  "assumption": "string",
  "basis_refs": ["SRC-001"],
  "affected_sections": ["product_judgment", "acceptance", "implementation", "roadmap"],
  "validation_need": "string",
  "owner": "product | engineering | legal | human | unknown",
  "expiry_condition": "string",
  "blocks_human_prd": false,
  "blocks_agent_prd": false,
  "status": "open | resolved | deferred | superseded",
  "resolution_refs": ["SRC-002"]
}
```

规则：

- 假设必须显式标注，不得写成事实。
- Human PRD 正文出现的 `ASM` 必须在“参考依据”中闭环说明。
- `status=open` 的阻断性假设必须阻断相应 render target。
- `status=resolved` 表示假设已被确认或被 contract 更新吸收；必须有 `resolution_refs`。
- `status=superseded` 表示假设被更新后的对象、来源或决策替代；必须通过 `resolution_refs`、`TRACE.relation=resolves` 或 `decision_traceability` 保留审计链路。

### 5.7 `RB`: Render Block

`RB` 是正文事实内容的最小审计单元。Human PRD 或 Agent PRD 中任何表达产品事实、范围、需求、验收、流程、数据、模块、技术决策、风险、开放问题、执行约束、验证或交付要求的章节、表格、图、清单或关键段落，都必须有 `RB`。

```json
{
  "id": "RB-001",
  "target": "human_prd | agent_prd",
  "section": "string",
  "content_type": "text | table | mermaid | latex | html | checklist | json_schema",
  "contract_refs": ["REQ-001", "AC-001"],
  "source_refs": ["SRC-001"],
  "allowed_inference": "none | summary | translation | formatting | bounded_synthesis",
  "unsupported_claims": [],
  "status": "ready | blocked"
}
```

规则：

- `contract_refs` 不能为空。
- `allowed_inference` 只能覆盖表达层处理，不得创造新事实；`bounded_synthesis` 必须列出所有参与的 `contract_refs`，输出只能表达这些对象的明确组合或交集。
- `unsupported_claims` 必须为空；非空时 `status=blocked`。
- Agent PRD 的 `section` 必须使用英文章节名。
- 修订记录、标题、作者、日期、版本等文档管理信息不得用 `RB` 支撑，必须使用 `META`。

### 5.8 `META`: Document Metadata

```json
{
  "id": "META-001",
  "target": "human_prd | agent_prd | audit",
  "field": "revision_history | title | author | date | version | change_basis",
  "value": "string",
  "basis": "user_request | agent_update | source_update | review_fix | system_generated"
}
```

规则：

- `META` 只能支撑文档管理信息。
- `META` 不得支撑产品事实、需求、验收、执行约束或来源主张。

### 5.9 Supporting Objects

| 对象 | 最低字段 | 用途 |
| --- | --- | --- |
| `SRC` | `id`、`source_type`、`label`、`target`、`provided_by`、`accessed_at`、`scope` | 外部来源、用户文件、链接、参考文献、事实依据。 |
| `REF` | `id`、`ref_type`、`label`、`target`、`scope`、`source_refs`、`related_refs` | canonical contract、同级产物、本地引用、harness 引用。`ref_type` 只能是 `canonical_contract`、`sibling_artifact`、`local_reference`、`harness_reference`；`related_refs` 用于说明该引用影响的执行控制、需求、验证、停止或完成对象。 |
| `USER` | `id`、`name`、`description`、`source_refs` | 目标用户和 persona。 |
| `SCOPE` | `id`、`statement`、`phase`、`source_refs` | 本期范围和允许能力。 |
| `OOS` | `id`、`statement`、`phase`、`reason`、`source_refs` | 非范围、禁止扩展、延期事项。 |
| `MET` | `id`、`metric`、`target`、`measurement_method`、`related_reqs`、`source_refs` | 成功指标和观测信号。 |
| `BAR` | `id`、`bar`、`reason`、`related_reqs`、`agent_rule_ref` | 质量红线和不可接受结果。 |
| `FLOW` | `id`、`actors`、`steps`、`related_reqs`、`source_refs` | Human 控制流和 Agent 顺序约束。 |
| `DATA` | `id`、`inputs`、`transformations`、`stores`、`outputs`、`related_reqs` | 数据流、运行数据来源、输出去向。 |
| `MOD` | `id`、`name`、`responsibility`、`interfaces`、`boundaries`、`related_reqs` | 模块职责和边界。 |
| `STATE` | `id`、`states`、`events`、`transition_rules`、`export_eligibility`、`related_reqs` | 生命周期、状态、审批、导出资格。 |
| `DCT` | `id`、`schema`、`required_fields`、`constraints`、`related_reqs` | Agent Data Contract。 |
| `PHASE` | `id`、`name`、`goal`、`deliverables`、`excluded_items`、`exit_criteria` | MVP 和路线图阶段。 |
| `IN` | `id`、`name`、`required`、`constraints`、`entry_blockers`、`permission_requirements` | Agent Input Contract。 |
| `EXE` | `id`、`rule`、`required_behavior`、`forbidden_behavior`、`sequence_refs`、`human_confirmation` | Agent Execution Contract。 |
| `VER` | `id`、`case_type`、`related_refs`、`input`、`expected_result`、`blocking`、`failure_handling` | 验证用例。`case_type` 只能是 `positive`、`negative`、`consistency_check`、`blocking_failure`。 |
| `OUT` | `id`、`deliverable`、`acceptance_rule`、`related_reqs`、`residual_scope_note` | Agent 必须交付的结果。 |
| `STOP` | `id`、`condition`、`reason`、`status`、`required_human_action`、`related_refs`、`resolution_refs` | Agent 必须停止并询问人类的条件；只有 `status=triggered` 阻断当前 execution-ready。 |
| `DONE` | `id`、`criterion`、`verification_refs`、`blocking`、`consistency_condition` | 完成标准。 |
| `RISK` | `id`、`risk`、`impact`、`mitigation`、`related_refs` | 风险与缓解。 |
| `TRACE` | `id`、`from_ref`、`to_ref`、`relation`、`claim` | 来源到需求、需求到验收、需求到验证、渲染块到合同对象的追踪。 |
| `GATE` | `id`、`name`、`blocking_condition`、`status`、`blocking`、`affected_targets`、`evidence_refs` | 质量门禁执行结果。 |

`SRC.source_type` 必须使用明确枚举：`user_input | user_document | user_confirmation | external_reference | local_file | runtime_input | system_generated`。当人类补充回答或确认某个事实时，必须登记为 `SRC.source_type=user_confirmation`，并由相关 `CORE`、`REQ`、`Q`、`ASM`、`STOP` 或 `TRACE` 引用；不得只在自然语言里写“用户确认”。

`TRACE.relation` 必须使用明确枚举：`stated_by | confirmed_by | inferred_from | assumes | resolves | blocks | renders`。其中 `inferred_from` 只能用于有界推演，相关对象不得因此变成 `confirmed`；影响范围、验收、执行、风险或停止条件的推演必须同时由 `ASM`、`Q`、`GATE` 或 `decision_traceability` 显式呈现。

### 5.10 Status Semantics

| 对象 | 字段 | 合法值 | 说明 |
| --- | --- | --- | --- |
| render target | `status` | `not_requested | draft | review_ready | execution_ready | blocked` | Human PRD 只能使用 `not_requested`、`draft`、`review_ready`、`blocked`；Agent PRD 只能使用 `not_requested`、`draft`、`execution_ready`、`blocked`。 |
| `CORE`、`REQ` | `status` | `draft | confirmed | blocked` | 只用于对象本身事实成熟度；不得写入未定义该字段的对象。 |
| `Q`、`ASM` | `status` | `open | resolved | deferred | superseded` | `open` 表示仍影响判断；`resolved` 表示已有确认或合同更新；`deferred` 表示明确延期；`superseded` 表示被更新对象或决策替代但保留审计链路。 |
| `RB` | `status` | `ready | blocked` | 只表示渲染块能否安全输出。 |
| `STOP` | `status` | `defined | triggered | resolved` | `defined` 表示停止条件存在；只有 `triggered` 会阻断当前 Agent PRD；`resolved` 必须有 `SRC.source_type=user_confirmation` 或 contract 更新。 |
| `GATE` | `status` | `pass | warning | blocked` | `warning` 表示未完全满足但不阻断当前 target ready；`blocked` 表示受影响 target 不得 ready。 |
| `GATE` | `blocking` | `true | false` | `blocking=true` 时，受影响 target 不得是 `review_ready` 或 `execution_ready`。 |
| `traceability_summary.decision_traceability` | `status` | `open | resolved | deferred | superseded | confirmed` | `open_question` 和 `assumption` 只能使用 `open | resolved | deferred | superseded`；`user_confirmation` 只能使用 `confirmed`。 |

状态转换规则：

- `status` 不是所有对象的通用字段；只有本节列出的对象、render target 和 audit fields 可以写入 `status`。其他对象的不确定性必须通过 `Q`、`ASM`、`GATE`、`STOP` 或 `TRACE` 表达。
- `not_requested` 只能转为 `draft` 或保持不变。
- `draft` 可转为 `review_ready`、`execution_ready` 或 `blocked`。
- `blocked` 只能在缺口被 contract 更新、`SRC.source_type=user_confirmation` 或 gate 证据解决后回到 `draft`。
- `review_ready` 和 `execution_ready` 不是永久状态；任一相关 object 改变后必须回到 `draft` 重新 gate。
- `GATE.status=pass` 时 `blocking` 必须为 `false`。
- `GATE.status=warning` 时 `blocking` 必须为 `false`；warning 只能表达非阻断缺口。
- `GATE.blocking=true` 时 `status` 必须为 `blocked`；不得出现 `status=warning` 且 `blocking=true` 的组合。

Validator 实现必须至少检查以下组合不变量：

```pseudo
for gate in gate_report:
  assert gate.status in ["pass", "warning", "blocked"]

  if gate.status in ["pass", "warning"]:
    assert gate.blocking == false

  if gate.status == "warning":
    assert gate.message is not empty
    assert gate.required_fix is not empty

  if gate.blocking == true:
    assert gate.status == "blocked"

  if gate.blocking == true or gate.status == "blocked":
    assert "review_ready" not in affected target statuses
    assert "execution_ready" not in affected target statuses

for decision in traceability_summary.decision_traceability:
  assert decision.decision_type in ["open_question", "assumption", "user_confirmation"]

  if decision.decision_type in ["open_question", "assumption"]:
    assert decision.status in ["open", "resolved", "deferred", "superseded"]

  if decision.decision_type == "user_confirmation":
    assert decision.status == "confirmed"

if agent_prd.status == "execution_ready":
  assert object_index contains ["IN", "EXE", "VER", "OUT", "STOP", "DONE"]
  assert no blocking gate affects agent_prd

if human_prd.status == "review_ready":
  assert no blocking gate affects human_prd

for render_block_id in human_prd.render_block_refs + agent_prd.render_block_refs:
  assert render_block_id in traceability_summary.render_traceability.render_block_id

rendered_requirement_ids = unique REQ-* IDs from traceability_summary.render_traceability[*].contract_refs
for requirement_id in rendered_requirement_ids:
  assert requirement_id in traceability_summary.requirement_traceability.requirement_id
  assert requirement_id in contract_summary.requirements

for concrete_envelope_example in reference_envelopes:
  assert concrete_envelope_example.contract_version == latest_revision_version
```

## 6. 成熟度与允许输出

| 等级 | 名称 | 最低条件 | 允许输出 |
| --- | --- | --- | --- |
| L1 | 探索态 | 用户、问题或目标不清晰。 | intake 问题、假设清单、方向摘要。 |
| L2 | Human PRD 草稿态 | 用户、问题、目标、范围初步成立，但验收、指标、风险仍有缺口。 | draft Human PRD，不得声明可评审 final。 |
| L3 | Human PRD 可评审态 | Human PRD 所需事实、范围、验收、风险、开放问题均可追踪。 | review-ready Human PRD。 |
| L4 | Agent PRD 可执行态 | Agent 输入、执行、输出、验证、停止条件、完成标准全部可追踪，且与 canonical contract 一致；若同时渲染 Human PRD，还必须通过 sibling consistency。 | execution-ready Agent PRD。 |

任一阻断 gate 失败时，只能输出 draft、blocked report 或澄清问题，不得声明 final。

缺口呈现规则：

| 成熟度 | 允许缺口 | 必须如何呈现 |
| --- | --- | --- |
| L1 | 用户、问题、目标、范围大面积缺失。 | 输出 intake 问题；缺失项进入 `Q`，必要前提进入 `ASM`；不渲染完整 PRD。 |
| L2 | 验收、指标、风险、实现细节可能缺失。 | Human PRD 必须标为 `draft`；缺口进入 `Q`、`ASM` 和 `gate_report`，不得写成事实。 |
| L3 | Agent 输入、验证、停止条件或完成标准可能不足。 | Human PRD 可 `review_ready`；Agent PRD 必须为 `not_requested`、`draft` 或 `blocked`。 |
| L4 | 不允许存在阻断 Agent 执行的缺口。 | Agent PRD 可 `execution_ready`；任何剩余非阻断未知项必须在 `Q` 或 residual-scope note 中可见。 |

## 7. Human PRD 渲染闭环

Human PRD 必须使用专业简体中文，是面向人类评审的决策文档。它只呈现人类需要判断的产品逻辑，不呈现 Agent 执行契约。

| Human PRD 章节 | 必须回答 | 合同支撑 | 可见形态 |
| --- | --- | --- | --- |
| 修订记录 | 文档如何变化。 | `META` | 版本、日期、修订人、修订内容、依据。 |
| 要做什么 | 产品解决什么问题，给谁用，本期做什么、不做什么。 | `CORE`、`USER`、`SCOPE`、`OOS`、`REQ`、`MOD`、`SRC`、`ASM`、`RB` | 简洁正文、范围表、产品形态图。 |
| 标准是什么 | 做到什么程度算成功，什么不可接受。 | `REQ`、`AC`、`MET`、`BAR`、`RISK`、`Q`、`ASM`、`RB` | 需求/标准表、指标表、质量红线、风险表。 |
| 如何实现 | 产品如何运转，如何分阶段落地。 | `FLOW`、`DATA`、`DCT`、`STATE`、`MOD`、`TECH`、`PHASE`、`SCOPE`、`OOS`、`REQ`、`AC`、`MET`、`RISK`、`Q`、`ASM`、`RB` | Mermaid 图、模块表、技术决策表、MVP 表、路线图表。 |
| 参考依据 | 来源或假设如何支撑产品判断。 | `SRC`、`TRACE`、`RB`、`ASM` | 来源说明和假设闭环说明。 |
| 参考文献 | 使用了哪些来源。 | `SRC`、可选 `TRACE` | 只列已使用来源。 |

Human PRD 的简洁表达不得删除关键合同事实。若某事实影响决策、验收、范围、风险、路线图或 MVP 边界，它必须可见。

## 8. Agent PRD 渲染闭环

Agent PRD 必须使用英文，是面向 AI Agent 或 harness 的执行契约。它必须完整、清晰、可验证、可停止、可审计。

Agent PRD 必须按以下顺序渲染：

1. Revision History
2. Execution Objective
3. Source Of Truth
4. Input Contract
5. Scope Contract
6. Execution Contract
7. Implementation Constraints
8. Requirements And Acceptance Criteria
9. State Transition Contract
10. Data Contract
11. Verification Contract
12. Output Contract
13. Open Decisions
14. Stop Conditions
15. Done Criteria
16. References

`System Context` 只能在 contract 存在具体 `MOD`、`DATA`、`DCT`、`TECH`、`SRC` 或 runtime reference 时作为条件章节出现，不能作为空占位。

| Agent PRD 章节 | 合同支撑 | 硬性可见字段 |
| --- | --- | --- |
| Revision History | `META` | version、date、author、change、basis |
| Execution Objective | `CORE`、`PHASE`、`SCOPE`、`REQ`、`OUT`、`RB` | capability、phase、deliverable outcome、non-expansion rule |
| Source Of Truth | `REF`、`IN`、`DATA`、`Q`、`ASM`、条件 `SRC`、可选 `TRACE`、条件 `RB` | source ID、authority、purpose、conflict handling |
| Input Contract | `IN`、`DCT`、`SCOPE`、`STOP`、`EXE`、`BAR`、`RB` | input ID、required/optional、constraints、entry blockers、permissions |
| Scope Contract | `SCOPE`、`OOS`、`PHASE`、`STOP`、`RB` | in scope、out of scope、phase boundary、scope blocker |
| Execution Contract | `EXE`、`REQ`、`BAR`、`OOS`、`STOP`、`FLOW`、`STATE`、`TECH`、`RB` | rule ID、required behavior、forbidden behavior、sequence、human confirmation |
| Implementation Constraints | `TECH`、`MOD`、`DATA`、`PHASE`、`RB` | technical decision ID、decision、rationale、affected modules、phase、agent constraint |
| Requirements And Acceptance Criteria | `REQ`、`AC`、`VER`、`PHASE`、`RB` | requirement ID、phase、AC IDs、acceptance criteria、verification link |
| State Transition Contract | `STATE`、`REQ`、`AC`、`DATA`、`BAR`、`STOP`、`RB` | state rule ID、states、events、transition rules、eligibility、negative rules |
| Data Contract | `DCT`、`DATA`、`REQ`、`TECH`、`BAR`、`RISK`、`Q`、`RB` | schema ID、schema、required fields、constraints、sources、outputs、privacy/retention |
| Verification Contract | `VER`、`AC`、`DONE`、`GATE`、`REQ`、`STOP`、`BAR`、`RB` | `VER-*` ID、case type、related refs、expected result、blocking、failure handling |
| Output Contract | `OUT`、`REQ`、`AC`、`DONE`、`VER`、`OOS`、`Q`、`PHASE`、`RB` | output ID、deliverable、acceptance rule、residual-scope note |
| Open Decisions | `Q`、`ASM`、`PHASE`、`STOP`、`RB` | decision/assumption ID、question or assumption、impact、owner、phase、agent handling、status、resolution refs |
| Stop Conditions | `STOP`、`Q`、`RISK`、`BAR`、`RB` | stop ID、trigger、reason、status、required human action、resolution refs、related risk/bar |
| Done Criteria | `DONE`、`VER`、`AC`、`GATE`、`RB` | done ID、completion condition、verification refs、blocking、consistency condition |
| References | `REF`、条件 `SRC`、条件 `TRACE`、条件 `RB` | actual references used by the Agent PRD body; execution controls affected by references must be linked through `TRACE` or `REF.related_refs`, not listed as reference sources. |

Agent PRD 不得新增范围、技术选择、数据字段、验证用例或完成条件。存在 canonical ID 的行必须展示 canonical ID。State Transition Contract 章节固定出现；当无状态规则适用时，必须写明 `Not applicable` 并引用 gate evidence，不得省略章节。

## 9. 审计层输出

最终输出必须包含展示层和审计层。

| 输出 | 类型 | 要求 |
| --- | --- | --- |
| `human_prd` | 展示层 | 给人类评审的 PRD，可为 Markdown 或 HTML。 |
| `agent_prd` | 展示层 | 给 Agent 或 harness 执行的英文 PRD。 |
| `contract_summary` | 审计层 | 摘要列出需求、范围、阶段、开放问题、阻断项和 render target 状态。 |
| `traceability_summary` | 审计层 | 分为 `render_traceability`、`requirement_traceability` 和 `decision_traceability`：前者列每个 `RB` 的 target、section、contract_refs、source_refs、status；第二类只覆盖 `SRC/ASM/Q -> REQ -> AC -> VER -> OUT/DONE` 的需求链路；第三类覆盖影响范围、阶段、风险、执行或停止条件的 `Q`、`ASM` 和 `SRC.source_type=user_confirmation` 决策链。 |
| `gate_report` | 审计层 | 真实完整输出必须列出每个全局 `GATE` 的 `pass | warning | blocked`、证据和处理建议；明确标注为最小 smoke fixture 的 reference fixture 可以只列 evaluated subset，但不得作为完整输出示例。 |

缺少审计层时，即使 PRD 文本完整，也不得声明交付完成。

## 10. 最终输出 envelope

`prd-intake` 的完整结构化输出必须使用以下 envelope。调用方可以只展示其中的 Human PRD 或 Agent PRD，但技能内部交付必须保留完整 envelope，方便审计、重渲染和失败诊断。下方是语义一致的 L4 envelope 示例：为避免重复第 5 节 schema，`payload` 仅作缩写，真实输出必须写入完整对象 payload。

```json
{
  "intake_id": "prd-intake-valid-minimal-envelope-example",
  "contract_version": "1.8",
  "maturity_level": "L4",
  "render_status": {
    "human_prd": "review_ready",
    "agent_prd": "execution_ready",
    "blocked_reasons": []
  },
  "canonical_contract": {
    "summary": "object",
    "objects": {
      "CORE-001": {
        "type": "CORE",
        "payload": {"id": "CORE-001"}
      },
      "REQ-001": {
        "type": "REQ",
        "payload": {"id": "REQ-001"}
      },
      "AC-001": {
        "type": "AC",
        "payload": {"id": "AC-001"}
      },
      "IN-001": {
        "type": "IN",
        "payload": {"id": "IN-001"}
      },
      "EXE-001": {
        "type": "EXE",
        "payload": {"id": "EXE-001"}
      },
      "ASM-001": {
        "type": "ASM",
        "payload": {
          "id": "ASM-001",
          "assumption": "This non-blocking assumption affects residual planning only.",
          "basis_refs": ["SRC-001"],
          "impact": "Does not change current execution readiness.",
          "validation_need": "Review during follow-up planning.",
          "owner": "product",
          "expiry_condition": "Superseded by a confirmed roadmap decision.",
          "blocks_human_prd": false,
          "blocks_agent_prd": false,
          "agent_handling": "defer",
          "status": "open",
          "resolution_refs": []
        }
      },
      "DONE-001": {
        "type": "DONE",
        "payload": {"id": "DONE-001"}
      },
      "GATE-001": {
        "type": "GATE",
        "payload": {"id": "GATE-001"}
      },
      "GATE-002": {
        "type": "GATE",
        "payload": {"id": "GATE-002"}
      },
      "GATE-003": {
        "type": "GATE",
        "payload": {"id": "GATE-003"}
      },
      "GATE-004": {
        "type": "GATE",
        "payload": {"id": "GATE-004"}
      },
      "GATE-005": {
        "type": "GATE",
        "payload": {"id": "GATE-005"}
      },
      "GATE-006": {
        "type": "GATE",
        "payload": {"id": "GATE-006"}
      },
      "GATE-007": {
        "type": "GATE",
        "payload": {"id": "GATE-007"}
      },
      "GATE-008": {
        "type": "GATE",
        "payload": {"id": "GATE-008"}
      },
      "GATE-009": {
        "type": "GATE",
        "payload": {"id": "GATE-009"}
      },
      "GATE-010": {
        "type": "GATE",
        "payload": {"id": "GATE-010"}
      },
      "GATE-011": {
        "type": "GATE",
        "payload": {"id": "GATE-011"}
      },
      "GATE-012": {
        "type": "GATE",
        "payload": {"id": "GATE-012"}
      },
      "GATE-013": {
        "type": "GATE",
        "payload": {"id": "GATE-013"}
      },
      "GATE-014": {
        "type": "GATE",
        "payload": {"id": "GATE-014"}
      },
      "META-001": {
        "type": "META",
        "payload": {"id": "META-001"}
      },
      "OOS-001": {
        "type": "OOS",
        "payload": {"id": "OOS-001"}
      },
      "OUT-001": {
        "type": "OUT",
        "payload": {"id": "OUT-001"}
      },
      "PHASE-001": {
        "type": "PHASE",
        "payload": {"id": "PHASE-001"}
      },
      "Q-001": {
        "type": "Q",
        "payload": {
          "id": "Q-001",
          "question": "Which future-phase option should be selected after the current execution?",
          "impact": "Affects residual scope only, not the current Agent PRD.",
          "phase": "PHASE-001",
          "owner": "human",
          "blocks_human_prd": false,
          "blocks_agent_prd": false,
          "agent_handling": "defer",
          "status": "open",
          "resolution_refs": []
        }
      },
      "RB-001": {
        "type": "RB",
        "payload": {"id": "RB-001"}
      },
      "RB-101": {
        "type": "RB",
        "payload": {"id": "RB-101"}
      },
      "SCOPE-001": {
        "type": "SCOPE",
        "payload": {"id": "SCOPE-001"}
      },
      "SRC-001": {
        "type": "SRC",
        "payload": {"id": "SRC-001"}
      },
      "SRC-002": {
        "type": "SRC",
        "payload": {"id": "SRC-002"}
      },
      "STOP-001": {
        "type": "STOP",
        "payload": {"id": "STOP-001"}
      },
      "VER-001": {
        "type": "VER",
        "payload": {"id": "VER-001"}
      }
    },
    "object_index": {
      "CORE": ["CORE-001"],
      "REQ": ["REQ-001"],
      "AC": ["AC-001"],
      "IN": ["IN-001"],
      "EXE": ["EXE-001"],
      "ASM": ["ASM-001"],
      "DONE": ["DONE-001"],
      "GATE": ["GATE-001", "GATE-002", "GATE-003", "GATE-004", "GATE-005", "GATE-006", "GATE-007", "GATE-008", "GATE-009", "GATE-010", "GATE-011", "GATE-012", "GATE-013", "GATE-014"],
      "META": ["META-001"],
      "OOS": ["OOS-001"],
      "OUT": ["OUT-001"],
      "PHASE": ["PHASE-001"],
      "Q": ["Q-001"],
      "RB": ["RB-001", "RB-101"],
      "SCOPE": ["SCOPE-001"],
      "SRC": ["SRC-001", "SRC-002"],
      "STOP": ["STOP-001"],
      "VER": ["VER-001"]
    }
  },
  "human_prd": {
    "format": "markdown",
    "content": "[example Human PRD content omitted]",
    "render_block_refs": ["RB-001"],
    "status": "review_ready"
  },
  "agent_prd": {
    "format": "markdown",
    "content": "[example Agent PRD content omitted]",
    "render_block_refs": ["RB-101"],
    "status": "execution_ready"
  },
  "contract_summary": {
    "product": "Example Product",
    "requirements": ["REQ-001"],
    "scope": ["SCOPE-001"],
    "out_of_scope": ["OOS-001"],
    "phases": ["PHASE-001"],
    "open_questions": ["Q-001"],
    "assumptions": ["ASM-001"]
  },
  "traceability_summary": {
    "render_traceability": [
      {
        "render_block_id": "RB-001",
        "target": "human_prd",
        "section": "标准是什么",
        "contract_refs": ["REQ-001"],
        "source_refs": ["SRC-001"],
        "status": "ready"
      },
      {
        "render_block_id": "RB-101",
        "target": "agent_prd",
        "section": "Verification Contract",
        "contract_refs": ["REQ-001", "AC-001", "VER-001"],
        "source_refs": ["SRC-001"],
        "status": "ready"
      }
    ],
    "requirement_traceability": [
      {
        "requirement_id": "REQ-001",
        "source_refs": ["SRC-001"],
        "assumption_refs": ["ASM-001"],
        "acceptance_criteria": ["AC-001"],
        "verification_refs": ["VER-001"],
        "output_refs": ["OUT-001"],
        "done_refs": ["DONE-001"]
      }
    ],
    "decision_traceability": [
      {
        "decision_ref": "Q-001",
        "decision_type": "open_question",
        "affected_refs": ["SCOPE-001", "PHASE-001", "STOP-001"],
        "status": "open",
        "owner": "human",
        "resolution_refs": []
      }
    ]
  },
  "gate_report": [
    {
      "gate_id": "GATE-001",
      "name": "source integrity",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd", "agent_prd"],
      "evidence_refs": ["SRC-001", "RB-001", "RB-101"],
      "message": "All rendered facts have source or contract support.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-002",
      "name": "requirement completeness",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd", "agent_prd"],
      "evidence_refs": ["REQ-001", "AC-001"],
      "message": "Rendered MVP requirements have acceptance criteria.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-003",
      "name": "scope consistency",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd", "agent_prd"],
      "evidence_refs": ["SCOPE-001", "OOS-001", "PHASE-001"],
      "message": "Scope, non-scope, and phase boundary are consistent.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-004",
      "name": "human readability",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd"],
      "evidence_refs": ["RB-001"],
      "message": "Human PRD render is review-ready.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-005",
      "name": "agent executability",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["agent_prd"],
      "evidence_refs": ["IN-001", "EXE-001", "VER-001", "OUT-001", "STOP-001", "DONE-001"],
      "message": "Agent PRD execution prerequisites are present.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-006",
      "name": "traceability",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd", "agent_prd"],
      "evidence_refs": ["RB-001", "RB-101", "REQ-001"],
      "message": "Rendered blocks and requirements are traceable.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-007",
      "name": "consistency",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd", "agent_prd"],
      "evidence_refs": ["REQ-001", "AC-001"],
      "message": "Rendered outputs are consistent with the canonical contract.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-008",
      "name": "language",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd", "agent_prd"],
      "evidence_refs": ["RB-001", "RB-101"],
      "message": "Human and Agent PRD language requirements are satisfied.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-009",
      "name": "output coverage",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd", "agent_prd"],
      "evidence_refs": ["RB-001", "RB-101"],
      "message": "Rendered output blocks are covered by RB objects.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-010",
      "name": "unsupported claim",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd", "agent_prd"],
      "evidence_refs": ["RB-001", "RB-101", "ASM-001"],
      "message": "No rendered claim is unsupported or converts assumptions into facts.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-011",
      "name": "example conformance",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd", "agent_prd"],
      "evidence_refs": ["META-001", "RB-001", "RB-101"],
      "message": "Envelope example conforms to the current output contract version.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-012",
      "name": "requirement-verification linkage",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["agent_prd"],
      "evidence_refs": ["REQ-001", "AC-001", "VER-001"],
      "message": "Current execution requirement has visible acceptance and verification links.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-013",
      "name": "closure synchronization",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["human_prd", "agent_prd"],
      "evidence_refs": ["META-001", "RB-001", "RB-101"],
      "message": "README, templates, examples, and section tables are synchronized with the output contract.",
      "required_fix": ""
    },
    {
      "gate_id": "GATE-014",
      "name": "canonical ID visibility",
      "status": "pass",
      "blocking": false,
      "affected_targets": ["agent_prd"],
      "evidence_refs": ["RB-101"],
      "message": "Agent PRD object-backed rows preserve canonical IDs.",
      "required_fix": ""
    }
  ],
  "next_actions": []
}
```

Envelope 规则：

- `human_prd.content` 和 `agent_prd.content` 是展示层，不是事实来源。
- `canonical_contract.summary` 可摘要化，但 `canonical_contract.objects` 必须保存完整对象 payload；`object_index` 只做索引。
- `canonical_contract.object_index` 必须覆盖 `canonical_contract.objects` 中的全部对象；任何 `contract_summary`、`traceability_summary`、`gate_report`、`render_block_refs`、`blocked_reasons`、`next_actions` 或 PRD content 中引用的 canonical ID，都必须存在于 `canonical_contract.objects`，或在本 envelope 中明确标为外部 `REF/SRC`。
- `traceability_summary.render_traceability` 必须覆盖每个已渲染 `RB`。
- `traceability_summary.requirement_traceability` 必须覆盖每个已渲染 `REQ` 的来源、验收、验证和交付/完成链路。
- `traceability_summary.decision_traceability` 必须覆盖所有影响非 `REQ` 对象的 `Q`、`ASM` 和 `SRC.source_type=user_confirmation`，包括影响范围、阶段、风险、执行规则、停止条件或完成条件的决策；`decision_ref` 可以是 `Q-*`、`ASM-*` 或 `SRC-*`。
- `decision_traceability.status` 必须按 `decision_type` 解释：`open_question` 和 `assumption` 只能使用 `open | resolved | deferred | superseded`；`user_confirmation` 只能使用 `confirmed`，并通过 `affected_refs`、`TRACE.relation=confirmed_by` 或 `TRACE.relation=resolves` 指向被确认或关闭的对象。
- `gate_report.blocking=true` 或 `status=blocked` 时，`affected_targets` 不能是 `review_ready` 或 `execution_ready`。
- `gate_report.status=warning` 时必须给出 `message` 和 `required_fix`；warning 不阻断当前 ready 状态，但必须保留在审计层。
- `gate_report.status=pass` 或 `warning` 时 `blocking` 必须为 `false`；`blocking=true` 时 `status` 必须为 `blocked`。
- L1 或 blocked 输出也必须返回 envelope；此时 `content` 可为空或为 draft/blocked 文本。

## 11. 渲染算法

Human PRD 与 Agent PRD 必须按同一渲染算法生成，区别只在目标章节、语言和可见字段。

1. Select target：根据 `requested_output` 和成熟度选择 `human_prd`、`agent_prd` 或仅审计输出。
2. Check prerequisites：根据第 7 节或第 8 节确定目标章节所需 canonical objects。
3. Build blocks：为每个正文事实章节、表格、图、清单或关键段落创建 `RB`。
4. Validate refs：确认每个 `RB.contract_refs` 非空，且 ID 存在于 canonical contract。
5. Render text：只允许 summary、translation、formatting 或 bounded_synthesis，不允许新增事实。
6. Run gates：执行第 12 节质量门禁。
7. Assemble envelope：写入 PRD content、`contract_summary`、`traceability_summary`、`gate_report` 和 `next_actions`。

渲染算法的阻断优先级：

| 优先级 | 条件 | 行为 |
| --- | --- | --- |
| P0 | contract object 缺失或 ID 不存在 | 不渲染相关正文事实块。 |
| P0 | `RB.contract_refs` 为空 | 不渲染该块，记录 gate failure。 |
| P0 | `unsupported_claims` 非空 | blocked。 |
| P1 | Human PRD 缺关键决策事实 | 降级为 draft 或 blocked。 |
| P1 | Agent PRD 缺 `IN`、`EXE`、`VER`、`OUT`、`STOP`、`DONE` | blocked，不得 execution-ready。 |
| P2 | 可读性或格式不佳但事实完整 | 可重渲染，不得改变 contract。 |

## 12. 质量门禁

| 门禁 | 阻断条件 |
| --- | --- |
| `GATE-001: source integrity` | 关键事实没有来源、合同对象、假设标注或 `SRC.source_type=user_confirmation`。 |
| `GATE-002: requirement completeness` | MVP `REQ` 缺少 `AC`，或 `AC` 不可判断。 |
| `GATE-003: scope consistency` | `SCOPE`、`OOS`、`PHASE`、MVP、路线图互相冲突。 |
| `GATE-004: human readability` | Human PRD 不能让人快速理解“要做什么、标准是什么、如何实现”。 |
| `GATE-005: agent executability` | Agent PRD 缺少 `IN`、`EXE`、`VER`、`OUT`、`STOP` 或 `DONE`。 |
| `GATE-006: traceability` | 需求、验收、技术决策、开放问题、渲染块无法回溯，或任一 envelope 内部引用的 canonical ID 缺少对应 `objects[ID].payload`。 |
| `GATE-007: consistency` | 任一 PRD 与 canonical contract 在事实、需求、范围、阶段、验收、技术决策或开放问题上不一致；若 Human PRD 与 Agent PRD 同时渲染，两者 sibling render 不一致。 |
| `GATE-008: language` | canonical Human PRD 不是专业简体中文，或 Agent PRD / execution-facing 交付物不是英文。 |
| `GATE-009: output coverage` | 正文事实内容缺少 `RB`，`RB.contract_refs` 为空，或文档元信息缺少 `META`。 |
| `GATE-010: unsupported claim` | `RB.unsupported_claims` 非空，或输出把假设写成事实。 |
| `GATE-011: example conformance` | Reference 样例没有体现模板和输出契约要求，JSON fence 不可解析，envelope 示例 `contract_version` 不等于本文件修订记录最新版本，envelope 示例存在悬空 canonical ID，gate 语义自相矛盾，样例表缺少模板要求的状态/闭环字段，或 fixture 声称覆盖完整 PRD examples 却未覆盖其中全部 canonical ID。该 gate 只阻断样例发布或文档包验收，不阻断真实用户 PRD 输出。 |
| `GATE-012: requirement-verification linkage` | Agent PRD 中任一 current-execution `REQ` 没有可见 `AC` 或 `VER`；deferred/future-phase `REQ` 未标明 phase/status 却被呈现为当前可执行工作；或任一 `VER` 没有相关合同对象。 |
| `GATE-013: closure synchronization` | README、模板、样例或章节表窄于本输出契约，造成字段、出现规则、支撑对象、可见形态或门禁不一致。 |
| `GATE-014: canonical ID visibility` | Agent PRD 中 object-backed row 缺少 canonical ID，或使用局部编号替代 canonical ID。 |

任一阻断门禁失败时：

- Human PRD 只能标为 draft 或 blocked。
- Agent PRD 不能标为 execution-ready。
- 最终输出必须包含失败门禁、缺失对象和下一步澄清项。

## 13. 渲染阻断规则

1. 正文事实块没有 `RB`：不渲染。
2. `RB.contract_refs` 为空：不渲染。
3. `RB.unsupported_claims` 非空：blocked。
4. 合同对象缺少必要 ID：blocked。
5. Human PRD 为了简洁删除关键事实：blocked。
6. Agent PRD 为了完整新增合同外事实：blocked。
7. `Q.blocks_human_prd=true` 且 `Q.status=open`：Human PRD 不得 `review_ready`。
8. `Q.blocks_agent_prd=true` 且 `Q.status=open`：Agent PRD 不得 `execution_ready`。
9. `ASM.blocks_human_prd=true` 且 `ASM.status=open`：Human PRD 不得 `review_ready`。
10. `ASM.blocks_agent_prd=true` 且 `ASM.status=open`：Agent PRD 不得 `execution_ready`。
11. `AC.blocking=true` 且不可验证：Agent PRD blocked。
12. `STOP.status=triggered`：Agent PRD blocked，除非存在 `SRC.source_type=user_confirmation` 或 contract update，并将 STOP 更新为 `resolved` 且填充 `resolution_refs`。

## 14. 最终交付约束

最终交付必须满足：

| 约束 | 要求 |
| --- | --- |
| 合同优先 | `human_prd` 与 `agent_prd` 只能渲染 canonical contract 已登记对象。 |
| 块级可追踪 | 每个正文事实块必须有 `RB`，并在 `traceability_summary` 出现。 |
| 元信息分离 | 修订记录、标题、作者、日期、版本和变更依据必须由 `META` 支撑。 |
| 一致性 | 每份 PRD 都必须与 canonical contract 一致；当 Human PRD 与 Agent PRD 同时渲染时，同一 `REQ`、`AC`、`SCOPE`、`OOS`、`TECH`、`PHASE`、`Q` 在两份 PRD 中含义一致。 |
| 未知项诚实 | 无法由合同支持的内容必须转为 `ASM` 或 `Q`，不得写入正文事实。 |
| Agent 可执行 | `agent_prd` 必须由 `IN`、`EXE`、`VER`、`OUT`、`STOP`、`DONE` 支撑，否则不得 execution-ready。 |

## 参考文献

[R1] Atlassian. “What is a Product Requirements Document (PRD)?” https://www.atlassian.com/agile/requirements

[R2] Productboard. “What is a Product Requirements Document (PRD)?” https://www.productboard.com/blog/product-requirements-document-guide/

[R3] Jama Software. “Best Practices for Writing Requirements.” https://www.jamasoftware.com/media/2024/03/Best-Practices-for-Writing-Requirements-2024.pdf

[R4] Wikipedia. “Requirements traceability.” https://en.wikipedia.org/wiki/Requirements_traceability

[R5] Wikipedia. “Traceability matrix.” https://en.wikipedia.org/wiki/Traceability_matrix

[R6] OpenAI. “Structured Outputs.” https://platform.openai.com/docs/guides/structured-outputs

[R7] OpenAI Agents SDK. “Agents.” https://openai.github.io/openai-agents-python/agents/

[R8] OpenAI. “A practical guide to building agents.” https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
