# Idea To Output Contract 工作法

## 修订记录

| 版本 | 日期 | 修订人 | 修订内容 | 依据 |
| --- | --- | --- | --- | --- |
| v1.0 | 2026-05-25 | Codex | 定义如何从一句话 idea 经过理解、推演、交互、校验，最终生成 `output-contract.md` 要求的完整结构化输出。 | 用户要求：说明从人类 idea 到 output-contract 的方法 |
| v1.1 | 2026-05-25 | Codex | 收紧推演写入、内部置信度、提问/输出判定、blocked envelope、ASM 闭环和 TRACE relation 规则。 | Review 发现方法文档存在契约字段越界和阻断逻辑不清。 |
| v1.2 | 2026-05-25 | Codex | 对齐 `output-contract.md` v1.3：按对象类型写 status，区分内部置信度和业务 `confidence` 字段。 | 收敛审计修复 |
| v1.3 | 2026-05-26 | Codex | 对齐 `output-contract.md` v1.6：限定 status 写入边界，并补强用户确认写回 `decision_traceability` 的类型化状态要求。 | 收敛审计修复 |
| v1.4 | 2026-05-26 | Codex | 对齐 `output-contract.md` v1.7：统一 execution-ready 必备对象集合，修正 status 判定伪代码，并显式构造决策追踪。 | 收敛审计修复 |
| v1.5 | 2026-05-26 | Codex | 对齐 `output-contract.md` v1.8 的 rendered `REQ` 追踪校验口径，确认 intake 方法无需新增字段。 | 收敛审计修复 |

## 1. 文档定位

本文定义 `prd-intake` 的 intake 工作法：如何把人类输入的一句话、草稿或模糊产品想法，转成 `output-contract.md` 中的 canonical structured contract。

本文不替代 `output-contract.md`。所有字段、对象、状态、gate、最终 envelope 都以 `output-contract.md` 为准。本文只说明如何获得这些对象、如何推理、如何提问、何时停止、何时可以输出 draft 或 ready。

核心原则：

1. 先理解问题，不急着写方案。
2. 先登记事实，再做推演。
3. 推演只能形成候选对象、假设或问题，不能伪装成用户确认。
4. 每轮交互只问最高价值问题，避免把用户拖进表格填空。
5. 任一输出都必须能解释“这个对象从哪里来、为什么可信、还有什么没确认”。

## 2. 方法来源

本文吸收以下成熟做法，并映射到 `prd-intake`：

| 方法 | 可借鉴点 | 在 `prd-intake` 中的用法 |
| --- | --- | --- |
| PRD 和 acceptance criteria | PRD 应说明目的、用户需求、成功标准；验收标准应清晰、可验证。 | 生成 `CORE`、`REQ`、`AC`、`MET`、`BAR`、`DONE`。 |
| User stories | 从用户视角表达目标和价值，需求需要经过讨论和验收标准收敛。 | 用于推导 `USER`、`REQ.user_value`、`AC`。 |
| Requirements elicitation | 通过访谈、工作坊、观察、原型等方式迭代发现需求；用户常会遗漏显而易见的信息。 | 用于设计澄清轮、缺口识别和 `Q`/`ASM`。 |
| Continuous discovery / Opportunity Solution Tree | 从 outcome 到 opportunity，再到 solution 和 assumption test。 | 用于把一句 solution idea 反推 outcome、机会、假设和验证。 |
| 用户访谈最佳实践 | 避免诱导式问题，使用开放问题，围绕具体经历和场景追问。 | 用于提问策略、问题排序和确认规则。 |
| How Might We | 把问题转成可探索但不预设答案的机会句。 | 用于生成 `Q`、`SCOPE` 候选和方案边界。 |

## 3. 输入理解模型

一句话 idea 通常混合了七类信息：

| 信息类型 | 例子 | 应进入的对象 |
| --- | --- | --- |
| 用户或角色 | “给销售团队用” | `USER` |
| 问题或痛点 | “客户跟进总是漏” | `CORE.problem_statement`、`SCOPE`、`REQ` |
| 解决方案 | “做一个自动提醒工具” | 候选 `SCOPE`、`REQ`、`MOD` |
| 目标结果 | “提高续费率” | `CORE.value_proposition`、`MET` |
| 使用场景 | “会议后自动整理行动项” | `FLOW`、`DATA`、`REQ` |
| 限制条件 | “只能用企业微信” | `TECH`、`DCT`、`BAR`、`OOS` |
| 风险或边界 | “不能泄露客户数据” | `RISK`、`BAR`、`STOP` |

Intake 的第一步不是补全所有字段，而是判断输入中哪些是事实、哪些是推测、哪些只是可能方向。

## 4. 事实、推演、假设和问题

任何从 idea 得到的信息必须落入以下四类之一：

| 类别 | 判定标准 | 合同落点 | 能否直接渲染为事实 |
| --- | --- | --- | --- |
| 明示事实 | 用户直接说出，或来源材料明确写出。 | 对应 canonical object，附 `SRC.source_type=user_input` 或 `user_document`。 | 可以。 |
| 用户确认事实 | 用户在澄清中确认。 | `SRC.source_type=user_confirmation`，并被相关对象引用。 | 可以。 |
| 有界推演 | 只组合已知事实，没有引入新主张。 | 可进入草稿对象 payload，但必须保留 `source_refs`，并用 `ASM` 或 `TRACE.relation=inferred_from` 标明推演来源。 | 可以渲染为草稿，不得标为 `confirmed`；若影响范围、验收、执行、风险或停止条件，必须显式生成 `ASM` 或 `Q`。 |
| 假设 | 合理但未被用户确认或来源证明。 | `ASM`，必要时阻断 target。 | 不能写成事实。 |
| 开放问题 | 会影响范围、验收、执行、风险或优先级，但当前无法判断。 | `Q`，必要时阻断 target。 | 不能自答。 |

### 4.1 内部状态与输出状态分离

Intake 可以在内部使用 `internal_confidence`、`candidate_score`、`question_priority` 等工作变量，但这些变量不得写入 canonical contract 或 envelope。输出里的不确定性只能通过以下方式表达：

- `output-contract.md` 明确列入状态语义的 object、render target 或审计字段 `status`：例如 `draft`、`resolved`、`blocked`、`confirmed`。
- `ASM`：表达未确认但需要保留的假设。
- `Q`：表达必须由用户或来源补足的开放问题。
- `GATE` 和 `gate_report`：表达阻断、警告和受影响 target。
- `traceability_summary`：表达事实、假设、问题、确认和渲染块之间的链路。

任何算法步骤提到的置信度都只是临时推理状态。写入合同前必须转换为 contract 已定义字段，且必须验证没有 `internal_confidence`、`candidate_score` 或 `question_priority` 等 intake 元字段泄漏到 `objects[*].payload`。如果产品本身需要业务字段 `confidence`，只能作为 `DCT.schema`、`OUT` 或 `VER.expected_result` 中的 contract-backed 业务字段出现。

### 4.2 允许的推演

允许推演：

- 从“给销售团队做客户跟进提醒”推导候选 `USER=销售人员`。
- 从“跟进提醒”推导候选 `REQ=创建提醒、查看待跟进客户、标记已跟进`。
- 从“提醒”推导需要确认 `DATA=客户、跟进时间、负责人、提醒状态`。
- 从“自动”推导可能存在 `RISK=错误提醒或过度打扰`。

不允许推演：

- 用户没提 CRM，却写成“必须集成 Salesforce”。
- 用户没提指标，却写成“提高续费率 20%”。
- 用户没确认隐私策略，却写成“保留数据 180 天”。
- 用户只说“自动”，就默认允许自动发消息、自动创建任务或自动修改状态。

### 4.3 TRACE relation 最小集合

`output-contract.md` 是准绳。本文在 intake 方法中使用以下最小 `TRACE.relation` 集合：

| relation | 用途 |
| --- | --- |
| `stated_by` | 对象字段来自用户输入、用户文档或外部来源的明示事实。 |
| `confirmed_by` | 对象字段由 `SRC.source_type=user_confirmation` 确认。 |
| `inferred_from` | 对象字段是有界推演结果，且必须保持 `draft` 或关联 `ASM/Q`。 |
| `assumes` | `ASM` 支撑某个候选对象、范围、验收或执行条件。 |
| `resolves` | `SRC` 或对象更新关闭 `Q`、`ASM`、`STOP` 或 gate 阻断。 |
| `blocks` | `Q`、`ASM`、`STOP` 或 `GATE` 阻断某个 target ready。 |
| `renders` | `RB` 渲染某些 canonical objects。 |

## 5. 从一句话到候选合同对象

### 5.1 第一遍解析

对 `raw_idea` 执行以下解析：

1. 抽取名词：角色、对象、数据、平台、渠道。
2. 抽取动词：创建、整理、提醒、审批、同步、导出、推荐。
3. 抽取形容词和约束：自动、实时、可审计、低成本、安全。
4. 抽取结果词：节省时间、减少遗漏、提高转化、降低风险。
5. 抽取否定词：不能、避免、不要、仅限、必须人工确认。

### 5.2 候选对象映射

| 解析结果 | 优先生成对象 | 次级对象 |
| --- | --- | --- |
| 产品名或工作名 | `CORE` | `META` |
| 用户/角色 | `USER` | `SCOPE` |
| 问题/痛点 | `CORE` | `REQ`、`RISK` |
| 当前方案 | `SCOPE`、`REQ` | `MOD`、`FLOW` |
| 输入数据 | `IN`、`DATA`、`DCT` | `STOP` |
| 输出物 | `OUT` | `DONE`、`AC` |
| 操作流程 | `FLOW` | `STATE`、`EXE` |
| 成功标准 | `AC`、`MET` | `VER`、`DONE` |
| 边界 | `OOS`、`BAR` | `STOP` |
| 未知项 | `Q` | `ASM` |

### 5.3 默认候选不等于事实

如果一句话只给出 solution，必须反推 problem 和 outcome，但反推结果默认进入 `ASM` 或 `Q`，除非用户确认。

示例：

```text
Idea: 做一个会议行动项整理工具。
```

可推导：

- 候选用户：会议组织者、项目经理、团队成员。
- 候选问题：会议后行动项遗漏、责任人不清、截止时间不明确。
- 候选输出：行动项列表、负责人、截止时间、原文证据。

必须追问或标记假设：

- 目标用户是谁？
- 输入是录音、转写文本、会议纪要，还是聊天记录？
- 是否允许自动创建任务？
- 是否需要人工确认？
- 是否涉及敏感信息？

## 6. 交互策略

### 6.1 提问目标

提问不是为了填满字段，而是为了解除阻断、提高成熟度、减少错误推演。

每个问题必须服务于至少一个目标：

| 目标 | 对应对象 |
| --- | --- |
| 确认用户和问题 | `CORE`、`USER` |
| 确认范围和非范围 | `SCOPE`、`OOS`、`PHASE` |
| 确认可验收结果 | `REQ`、`AC`、`MET` |
| 确认输入、输出和权限 | `IN`、`OUT`、`DCT`、`STOP` |
| 确认风险和禁止事项 | `RISK`、`BAR`、`STOP` |
| 确认执行可行性 | `EXE`、`VER`、`DONE` |

### 6.2 问题排序

每轮最多问 3 个问题。排序规则：

1. 先问会阻断 `CORE` 的问题：用户、问题、价值是否成立。
2. 再问会阻断范围的问题：MVP 做什么、不做什么。
3. 再问会阻断验收的问题：完成标准、成功信号。
4. 再问会阻断 Agent 执行的问题：输入、权限、输出、停止条件。
5. 最后问优化性问题：指标精度、路线图、替代方案。

### 6.3 问法规则

优先使用开放、具体、非诱导问题：

| 不推荐 | 推荐 |
| --- | --- |
| “你是不是想做一个 AI 自动任务系统？” | “你希望它帮谁在什么场景下完成什么结果？” |
| “需要集成 Jira 吗？” | “这些行动项最终需要进入哪个现有工作流或工具？” |
| “你觉得这个功能有用吗？” | “上一次发生这个问题时，团队是怎么处理的？” |
| “要不要自动创建任务？” | “创建任务前是否需要人确认？哪些情况下必须停止？” |
| “成功指标是提效 30% 吗？” | “你会用什么信号判断它值得继续做？” |

### 6.4 追问模板

| 缺口 | 问题模板 |
| --- | --- |
| 用户不明 | “这个能力首先服务哪一类人？他们现在用什么方式处理这件事？” |
| 痛点不明 | “现在最痛的失败场景是什么？最近一次是什么样？” |
| 目标不明 | “如果三周后这个能力有效，你希望看到什么变化？” |
| 范围过大 | “第一版必须保留的最小闭环是什么？哪些可以明确不做？” |
| 验收不明 | “什么结果出现时，你会说它已经达标？” |
| 输入不明 | “它可以依赖哪些输入？缺少哪些输入时必须停止？” |
| 输出不明 | “最终交付给用户的东西长什么样？谁会使用它？” |
| 风险不明 | “如果它做错了，最不能接受的后果是什么？” |
| 权限不明 | “哪些动作必须由人确认，不能由系统自动执行？” |

## 7. 单轮工作流

每一轮 intake 按以下顺序执行：

1. Register source：把用户输入登记为 `SRC`。
2. Parse idea：抽取角色、问题、动作、数据、结果、限制。
3. Product candidate pass：生成候选 `CORE`、`USER`、`SCOPE`、`REQ`、`AC`、`Q`、`ASM`。
4. Execution readiness pass：如果目标包含 Agent PRD 或 execution-ready，补齐候选 `IN`、`EXE`、`VER`、`OUT`、`STOP`、`DONE`、`DCT`、`DATA`。其中 execution-ready 必备对象集合固定为 `IN, EXE, VER, OUT, STOP, DONE`，不得在其他章节改写为不同列表。
5. Classify internal confidence：内部区分 confirmed、draft、assumption、open，但不得把 `internal_confidence`、`candidate_score` 或 `question_priority` 写入合同；只有 `output-contract.md` 明确列入状态语义的 object、render target 或审计字段才能写 `status`。
6. Detect blockers：根据 `output-contract.md` gate 找阻断项。
7. Ask or output：按照 7.1 判定先问还是先输出；任何 blocked 输出也必须先组装最小 canonical contract。
8. Integrate answer：用户回答后登记 `SRC.source_type=user_confirmation`，更新对象、`TRACE` 和必要的 `decision_traceability`。
9. Re-run gates：重新计算 maturity 和 render status。

### 7.1 提问与输出判定

默认优先问最少问题，而不是伪装完整。以下情况必须先提问，除非用户明确要求“先输出草稿”：

- `CORE.user`、`CORE.problem_statement` 或 `CORE.value_proposition` 缺失，导致产品目标无法判断。
- MVP 边界缺失，无法区分 `SCOPE`、`OOS` 或当前阶段 `PHASE`。
- 涉及敏感数据、权限、自动执行或外部系统写入，但没有对应 `BAR`、`STOP` 或人工确认规则。
- 用户请求 execution-ready Agent PRD，但缺少 execution-ready 必备对象集合中的任一对象：`IN`、`EXE`、`VER`、`OUT`、`STOP` 或 `DONE`。

如果用户明确要求先出草稿，允许输出 blocked/draft envelope，但必须满足：

- envelope 中包含最小 canonical contract，而不是只返回问题列表。
- 阻断项进入 `Q`、`ASM`、`STOP` 或 `GATE`。
- affected target 不得标为 `review_ready` 或 `execution_ready`。
- `next_actions` 必须说明关闭阻断所需的最少问题。

## 8. 成熟度推进

| 成熟度 | 输入状态 | 允许输出 | 交互策略 |
| --- | --- | --- | --- |
| L1 | 只有一句模糊 idea，用户/问题/目标缺失。 | intake 问题、假设清单、blocked envelope。 | 问用户、问题、目标。 |
| L2 | 用户和问题初步清楚，但验收和范围不稳。 | draft Human PRD、contract draft。 | 问 MVP、非范围、验收标准。 |
| L3 | Human PRD 可评审，但 Agent 执行条件不足。 | review-ready Human PRD、draft/blocked Agent PRD。 | 问输入、输出、验证、停止条件。 |
| L4 | 执行对象、验证、停止、完成标准全部可追踪。 | execution-ready Agent PRD 和完整 envelope。 | 只问剩余非阻断问题或输出。 |

## 9. 输出合同构造算法

```pseudo
function intake_to_output_contract(raw_idea, source_context, requested_output):
  src = create_SRC(source_type="user_input", content=raw_idea)

  signals = parse(raw_idea, source_context)
  product_candidates = infer_product_candidate_objects(signals)
  execution_candidates = infer_execution_readiness_objects(product_candidates, requested_output)
  candidates = product_candidates + execution_candidates

  for object in candidates:
    object.source_refs.add(src.id)
    if output_contract_allows_status(object.field_path("status")):
      object.status = internal_confidence_to_contract_status(object.field_path("status"), internal_confidence(object))
    assert_no_internal_state_fields(object, ["internal_confidence", "candidate_score", "question_priority"])

  gaps = detect_missing_required_objects(candidates)
  blockers = run_contract_gates(candidates, gaps)

  questions = rank_questions(blockers, gaps, max_count=3)
  contract = assemble_minimal_canonical_contract(candidates, gaps, blockers)
  decision_traceability = build_decision_traceability(contract)
  assert_decision_traceability_status_matches_type(decision_traceability)

  if must_ask_before_render(blockers, requested_output):
    audit = build_traceability_and_gate_report(contract, [], decision_traceability)
    return blocked_envelope(contract, audit, questions, blockers)

  contract = finalize_canonical_contract(contract)
  render_blocks = plan_render_blocks(contract, requested_output)
  audit = build_traceability_and_gate_report(contract, render_blocks, decision_traceability)

  return full_envelope(contract, render_blocks, audit, questions)
```

## 10. 问题生成算法

```pseudo
function rank_questions(blockers, gaps, max_count):
  candidates = []

  for blocker in blockers:
    candidates.add(question_for(blocker), priority="blocking")

  for gap in gaps:
    if gap.affects in ["CORE", "SCOPE", "REQ", "AC", "IN", "OUT", "STOP", "DONE"]:
      candidates.add(question_for(gap), priority="high")
    else:
      candidates.add(question_for(gap), priority="medium")

  remove_questions_that_can_be_answered_by_existing_sources(candidates)
  remove_leading_or_solution_biased_questions(candidates)
  merge_overlapping_questions(candidates)
  sort_by_contract_impact_and_blocking_status(candidates)

  return top(candidates, min(max_count, 3))
```

`priority` 是内部排序字段，不得进入 canonical contract。若阻断问题超过 3 个，只问对 `CORE`、MVP 边界、验收、输入输出、停止条件或敏感权限影响最大的 3 个；其余缺口必须保留在 `Q`、`ASM` 或 `GATE` 中，不能静默丢弃。

问题必须带有目的说明，方便模型知道答案如何更新 contract：

```json
{
  "question": "第一版必须完成的最小闭环是什么？",
  "why": "用于确认 SCOPE、OOS、PHASE，并判断 Human PRD 是否可 review_ready。",
  "updates": ["SCOPE", "OOS", "PHASE", "REQ"]
}
```

## 11. 回答整合规则

用户回答后：

1. 新建或更新 `SRC`，`source_type=user_confirmation`。
2. 更新对应 object payload。
3. 如果回答关闭 `Q`，将 `Q` 标记为 resolved，并增加 `resolution_refs`。
4. 如果回答验证 `ASM`，新建或更新被确认的对象字段，并将原 `ASM` 标记为 `resolved` 或 `superseded`；必须通过 `resolution_refs`、`TRACE.relation=resolves` 或 `decision_traceability` 链接到 `SRC.source_type=user_confirmation`，不得无痕移除原假设记录。
5. 如果用户回答确认了影响范围、阶段、风险、执行规则、停止条件或完成条件的决策，必须新增或更新 `traceability_summary.decision_traceability`，使用 `decision_ref=SRC-*`、`decision_type=user_confirmation`、`status=confirmed`，并通过 `affected_refs`、`TRACE.relation=confirmed_by` 或 `TRACE.relation=resolves` 指向被确认或关闭的对象。
6. 如果回答改变原有对象，相关 render target 回到 `draft`，重新 gate。
7. 不允许只在 PRD 正文里写“用户确认”，必须对象化。

## 12. 高质量推演技巧

### 12.1 从 solution 反推 problem

很多 idea 是 solution-first。处理方法：

1. 把 solution 拆成动作和对象。
2. 问“这个动作避免了什么失败？”
3. 问“谁现在为这个失败付出成本？”
4. 问“如果不做这个 solution，还有什么替代方式？”

产物：

- `CORE.problem_statement`
- `USER`
- `RISK`
- `OOS`
- `Q`

### 12.2 从场景推导 MVP

围绕一次完整使用场景找最小闭环：

1. 触发：用户什么时候开始使用？
2. 输入：系统需要什么信息？
3. 处理：系统必须做哪几个动作？
4. 人工确认：哪里不能自动化？
5. 输出：用户拿到什么？
6. 验收：什么结果算完成？
7. 停止：缺什么或错什么必须停？

产物：

- `FLOW`
- `IN`
- `REQ`
- `AC`
- `OUT`
- `STOP`
- `DONE`

### 12.3 从风险反推禁止事项

问“最不能接受的错误是什么”，再生成：

- `RISK`
- `BAR`
- `STOP`
- `VER.case_type=negative`
- `VER.case_type=blocking_failure`

### 12.4 从输出反推数据合同

如果用户说“输出报告/清单/摘要/导出文件”，必须反推：

- 输出字段。
- 字段来源。
- 必填/可选。
- 缺失行为。
- 隐私和保留规则。

产物：

- `DCT`
- `DATA`
- `OUT`
- `AC`
- `VER`

## 13. 常见失败模式

| 失败模式 | 表现 | 处理 |
| --- | --- | --- |
| 把 solution 当 problem | 文档只描述功能，不说明为什么做。 | 追问最近失败场景和目标结果。 |
| 过早补全 | 模型自动生成大量看似合理的范围。 | 降为 `ASM` 或 `Q`，不得 confirmed。 |
| 问题太多 | 一次问十几个字段。 | 每轮最多 3 个最高价值问题。 |
| 问题诱导 | “是不是要 AI 自动处理？” | 改成开放问题，询问现有流程和限制。 |
| 验收不可测 | “体验好、效率高、智能”。 | 转成可观察条件或 `MET` 缺口。 |
| Agent 过早 ready | 缺 `IN/VER/STOP/DONE` 却输出执行 PRD。 | Agent PRD blocked。 |
| 样例变规则 | 参考样例比 contract 更具体。 | 以 `output-contract.md` 为准，样例只参与 `GATE-011`。 |

## 14. 参考资料

[R1] Atlassian. “What is a Product Requirements Document (PRD)?” https://www.atlassian.com/agile/requirements

[R2] Atlassian. “What is Acceptance Criteria?” https://www.atlassian.com/work-management/project-management/acceptance-criteria

[R3] Atlassian. “User Stories with Examples and a Template.” https://www.atlassian.com/agile/project-management/user-stories

[R4] Product Talk. “Product Discovery Basics: Everything You Need to Know.” https://www.producttalk.org/product-discovery/

[R5] Product Talk. “Discovering Solutions: Quickly Determine Which Ideas Will Work.” https://www.producttalk.org/2022/03/discovering-solutions/

[R6] Interaction Design Foundation. “What are User Interviews?” https://www.interaction-design.org/literature/topics/user-interviews

[R7] ISO. “ISO/IEC/IEEE 29148:2018 - Systems and software engineering - Life cycle processes - Requirements engineering.” https://www.iso.org/standard/72089.html

[R8] IIBA. “Business Analysis Global Standards of Practice.” https://www.iiba.org/standards-and-resources/babok/

[R9] Interaction Design Foundation. “How Might We.” https://public-media.interaction-design.org/pdf/How-Might-We.pdf

[R10] Wikipedia. “Requirements elicitation.” https://en.wikipedia.org/wiki/Requirements_elicitation (背景参考，不作为规范来源)
