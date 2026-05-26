# PRD To Execution Tasks 工作法

## 修订记录

| 版本 | 日期 | 修订人 | 修订内容 | 依据 |
| --- | --- | --- | --- | --- |
| v1.0 | 2026-05-26 | Codex | 定义如何从 execution-ready Agent PRD 和 canonical contract 派生可执行任务图。 | 用户要求：把 PRD 执行任务拆解逻辑设计清楚 |
| v1.1 | 2026-05-26 | Codex | 将任务内敛、独立验收、阶段性目标覆盖升级为硬门禁，并补充阶段目标覆盖输出。 | 用户补充任务拆解三项基本原则 |
| v1.2 | 2026-05-26 | Codex | 基于好实例和生成过程，总结任务拆解设计流程、过程产物、评审循环和示例映射。 | 用户要求：总结如何完成任务拆解，形成设计文档 |
| v1.3 | 2026-05-26 | Codex | 收紧任务目标对象与支撑边界对象的口径，并明确 `phase_ref` 可见标签降级规则。 | 收敛 review 修复 |
| v1.4 | 2026-05-26 | Codex | 补硬 blocked planning 契约、source metadata、parallel groups、gate evidence refs、validator 最低实现和负例校准。 | 收敛 review 修复 |

## 1. 文档定位

本文定义 `prd-intake` 的执行任务拆解工作法：当 `output-contract.md` 已经产出 L4 canonical contract 和 execution-ready Agent PRD 后，如何把 PRD 拆成可执行、可验证、可停止、可并行调度的任务图。

本文不替代 `output-contract.md`、`idea-to-output-contract.md` 或 `agent-prd-template.md`。任务拆解结果不是新的事实来源，不能新增需求、范围、技术选择、数据字段、验收标准、验证用例或完成标准。它只能把已经存在的 contract-backed execution facts 转成执行计划。

如果 Agent PRD 不是 `execution_ready`，不得生成执行任务图；只能输出 blocked task planning report，说明缺哪些 `IN`、`EXE`、`VER`、`OUT`、`STOP` 或 `DONE`。

## 2. 设计目标

任务拆解设计的目标不是把 PRD 改写成待办清单，而是生成一份可被执行 agent 消费、可被 reviewer 验收、可被 gate 机械检查的 `execution_task_plan`。

一份合格设计必须回答五个问题：

| 问题 | 设计回答 |
| --- | --- |
| 从哪里来 | 只从 canonical contract、execution-ready Agent PRD、traceability summary、gate report 和受限 runtime context 派生。 |
| 拆什么 | 以 current execution phase 的 `REQ/AC/OUT/DONE` 为目标对象，同时纳入支撑执行和边界控制的 `IN/EXE/DCT/DATA/STATE/FLOW/VER/STOP/BAR/RISK/OOS/Q/ASM/TECH/MOD`。 |
| 怎么拆 | 先按 contract-backed execution units 建任务，再按内敛、独立验收和阶段目标覆盖修正粒度。 |
| 怎么证明好 | 每个任务有 closure card；整体有 dependency edges、parallel groups、stage goal coverage 和 planning gate report。 |
| 何时停止 | 任何缺事实、缺验收、缺验证、阶段越界、open decision 自答或 runtime conflict 都必须 blocked。 |

## 3. 输入与输出

### 3.1 输入

| 输入 | 必需 | 说明 |
| --- | --- | --- |
| `canonical_contract` | ready plan 必需；rendered-only diagnostic 可缺失 | 来自 `output-contract.md` envelope，必须包含完整 `objects` 和 `object_index`。缺失时只能输出 `planning_source_mode=rendered_agent_prd_only` 且 `planning_status=blocked` 的诊断报告，不得生成 ready task graph。 |
| `agent_prd` | 是 | Agent PRD render target 或文件。只有 `status=execution_ready` 且无阻断 gate 时，才能生成 `planning_status=ready` 的任务图；其他状态只能生成 blocked planning report。 |
| `traceability_summary` | 是 | 用于把任务反向追踪到 `REQ/AC/VER/OUT/DONE/STOP/EXE`。 |
| `gate_report` | 是 | 用于判断是否允许拆解；任一阻断 gate 失败时只能输出 blocked report。 |
| runtime context | 否 | 只允许提供仓库、文件、框架、工具链等执行环境信息；不得改变产品事实。 |

### 3.2 输出

执行任务拆解输出是 `execution_task_plan`，建议作为 downstream execution artifact 保存，不写回 canonical contract。

```json
{
  "plan_id": "string",
  "planning_source_mode": "contract_backed | rendered_agent_prd_only",
  "source_artifacts": {
    "contract_ref": "canonical contract URI, path, or envelope id",
    "contract_version": "string",
    "agent_prd_ref": "agent-prd-example-meeting-action-hub.md",
    "agent_prd_status": "not_requested | draft | execution_ready | blocked",
    "phase_ref": "PHASE-001",
    "phase_label": "Phase 1 MVP",
    "phase_ref_kind": "canonical_id | rendered_label",
    "phase_ref_fallback_reason": ""
  },
  "planning_status": "ready | blocked",
  "blocking_reasons": [],
  "missing_required_refs": [],
  "required_fixes": [],
  "task_graph": [
    {
      "task_id": "TASK-001",
      "title": "string",
      "task_type": "foundation | implementation | integration | verification | documentation | release | cleanup",
      "contract_refs": ["REQ-001", "AC-001", "EXE-001"],
      "verification_refs": ["VER-001"],
      "done_refs": ["DONE-001"],
      "stop_refs": ["STOP-001"],
      "inputs": ["IN-001"],
      "outputs": ["OUT-001"],
      "dependencies": [],
      "parallel_group": "PG-001",
      "allowed_files_or_modules": ["string"],
      "forbidden_scope_refs": ["OOS-001"],
      "acceptance": ["string"],
      "verification": ["string"],
      "stop_conditions": ["string"],
      "status": "planned"
    }
  ],
  "dependency_edges": [
    {
      "from": "TASK-001",
      "to": "TASK-002",
      "reason": "TASK-002 depends on schema from TASK-001",
      "contract_refs": ["DCT-001"]
    }
  ],
  "parallel_groups": [
    {
      "group_id": "PG-001",
      "task_refs": ["TASK-001"],
      "rationale": "string",
      "conflict_refs": [],
      "status": "serial | parallel_safe | blocked"
    }
  ],
  "stage_goal_coverage": [
    {
      "phase_ref": "PHASE-001",
      "phase_label": "Phase 1 MVP",
      "goal_refs": ["REQ-001", "OUT-001", "DONE-001"],
      "required_task_refs": ["TASK-001", "TASK-002"],
      "coverage_status": "covered | partial | blocked",
      "missing_refs": []
    }
  ],
  "planning_gate_report": [
    {
      "check_id": "CHECK-001",
      "name": "task traceability",
      "status": "pass | warning | blocked",
      "evidence_refs": ["TASK-001", "REQ-001"],
      "evidence_summary": "All task refs resolve to the source contract.",
      "required_fix": ""
    }
  ]
}
```

`TASK-*`、`PG-*` 和 `CHECK-*` 是 execution planning IDs，不是 `output-contract.md` 的 canonical IDs。它们不得替代 `REQ-*`、`AC-*`、`VER-*`、`STOP-*` 或 `DONE-*`。

正式可执行任务计划必须满足：

- `planning_source_mode=contract_backed`。
- `source_artifacts.agent_prd_status=execution_ready`。
- `source_artifacts.phase_ref_kind=canonical_id`，且 `phase_ref` 引用真实 `PHASE-*`。可同时输出 `phase_label` 方便人读。
- `planning_status=ready` 时，`blocking_reasons`、`missing_required_refs` 和 `required_fixes` 必须为空。
- `planning_status=blocked` 时，`task_graph`、`dependency_edges` 和 `parallel_groups` 必须为空；必须填充 `blocking_reasons`、`missing_required_refs` 或 `required_fixes` 中至少一项，并输出 `planning_gate_report`。

`rendered_agent_prd_only` 只允许用于诊断或迁移场景：当只能看到渲染后的 Agent PRD、无法访问 canonical contract 或无法解析 `PHASE-*` 时，可以输出 `phase_ref_kind=rendered_label` 和 `phase_ref_fallback_reason`，但不得声明 `planning_status=ready`，也不得把任务图交给执行 agent。

任务状态只描述执行计划在调度阶段的状态，不描述 canonical contract 的成熟度：

| 状态 | 含义 | 使用约束 |
| --- | --- | --- |
| `planned` | 已被拆出，但尚未检查运行环境是否可直接执行。 | 任务图初始默认值。 |
| `ready` | 依赖已满足，执行环境与输入可用。 | 只能在依赖、文件边界和 stop 条件确认后设置。 |
| `blocked` | 缺少输入、决策、环境或上游产物。 | 必须带 blocking reason 和 required fix。 |
| `deferred` | 属于未来阶段或当前范围外。 | 必须关联 `PHASE`、`OOS` 或明确的 defer reason。 |
| `in_progress` | 已交给执行 agent。 | 不应由 PRD intake 静态规划阶段设置。 |
| `done` | 执行完成且验证通过。 | 必须能回链到 `VER-*` 和 `DONE-*`。 |
| `skipped` | 有意跳过。 | 必须说明被哪个 stop/defer/范围规则允许。 |

## 4. 拆解前置条件

执行任务拆解必须先检查：

| 条件 | 失败处理 |
| --- | --- |
| `agent_prd.status=execution_ready` | 输出 blocked task planning report。 |
| `canonical_contract.object_index` 包含 `IN/EXE/VER/OUT/STOP/DONE` | 输出缺失对象清单，不生成任务图。 |
| `gate_report` 无阻断 gate | 输出阻断 gate 和 required fix。 |
| 每个 current-execution `REQ` 有 `AC` 和 `VER` | 不得把该 `REQ` 拆成实现任务。 |
| open `Q/ASM` 不阻断执行 | 若影响执行，生成 stop/defer 任务而不是自答。 |
| runtime context 不改变 contract | 若冲突，停止并要求 contract update。 |

## 5. 任务拆解设计流程

任务拆解按以下顺序完成。不得跳过前面的事实盘点，直接凭经验写任务。

### 5.1 冻结执行来源

先确认并记录：

| 项 | 必须确认 |
| --- | --- |
| Source Agent PRD | 文件、版本或 envelope target。 |
| Agent PRD status | 必须是 `execution_ready`。 |
| Current phase | 当前只执行哪个 canonical `PHASE-*`；可见 phase label 只能作为 `phase_label`，不能替代 ready plan 的 `phase_ref`。 |
| Source of truth | canonical contract 优先级高于 Human PRD、样例和 runtime context。 |
| Runtime context | 只能补执行环境边界，不得新增产品事实。 |

如果当前 phase 不能定位，不能继续拆任务；必须回到 contract 或 Agent PRD 修正。

### 5.2 建立来源清单

把 Agent PRD 中的执行对象先整理成 source inventory。该清单是过程产物，可以不进入最终交付，但必须用于自检。

| 来源簇 | 要收集的对象 | 用途 |
| --- | --- | --- |
| 执行目标 | `PHASE`、current `REQ`、`AC`、`OUT`、`DONE` | 决定阶段目标覆盖。 |
| 输入边界 | `IN`、entry `STOP`、authorization rules | 决定入口任务和阻断行为。 |
| 数据与结构 | `DCT`、`DATA`、`TECH`、`MOD` | 决定 foundation / data contract 任务。 |
| 行为与状态 | `EXE`、`STATE`、`FLOW`、current `REQ` | 决定实现任务和串行依赖。 |
| 输出与残余范围 | `OUT`、`OOS`、future `PHASE`、open `Q/ASM` | 决定 export、documentation、defer/stop 任务。 |
| 验证与完成 | `VER`、`DONE`、`GATE`、`BAR`、`RISK` | 决定 verification 任务和 planning gates。 |

来源清单的失败信号：

- `REQ` 没有 `AC` 或 `VER`。
- `OUT` 没有对应实现或验证路径。
- `DONE` 无法回链到任务和 `VER`。
- `STOP/BAR/RISK/OOS/Q/ASM` 没有进入任何任务或 stop/defer report。

### 5.3 派生执行单元

不要先写任务名。先把来源清单转换成 execution units：

| Execution unit | 来源 | 通常变成 |
| --- | --- | --- |
| Entry boundary unit | `IN`、entry `STOP`、authorization `BAR/RISK` | 输入校验或入口阻断任务。 |
| Data contract unit | `DCT`、`DATA`、schema-related `TECH` | foundation 任务。 |
| Requirement behavior unit | current `REQ` + `AC` + `EXE` | implementation 任务。 |
| State/control unit | `STATE`、`FLOW`、confirmation/export eligibility | implementation 或 integration 任务。 |
| Output unit | `OUT`、export format、residual-scope note | implementation 或 documentation 任务。 |
| Risk/stop unit | `STOP`、`BAR`、`RISK`、`OOS`、open `Q/ASM` | stop handling、defer 或 documentation 任务。 |
| Verification unit | `VER`、`DONE`、blocking failure cases | verification 任务或 task-level verification refs。 |

一个 execution unit 可以被多个任务引用，但每个 unit 必须至少被一个任务覆盖或被明确 deferred / blocked。

### 5.4 生成候选任务

候选任务的标题必须先写成“可观察结果”，再补类型和 refs。禁止先按技术层写“前端任务 / 后端任务 / 测试任务”。

任务通常按以下骨架生成：

1. Entry boundary。
2. Data contracts。
3. Core requirement behavior。
4. State / review / control behavior。
5. Output behavior。
6. Residual scope / open decisions。
7. Verification record。

不是每个 PRD 都必须使用同样数量的任务；数量由内敛、独立验收和阶段目标覆盖决定。

### 5.5 填写 closure card

每个任务必须写 closure card。没有 closure card 的任务不允许进入 ready task graph。

| Closure field | 设计要求 |
| --- | --- |
| Inputs | 写清任务消费什么上游产物、runtime input 或 contract object。 |
| Outputs | 写清任务完成后产生什么可观察产物或状态。 |
| Allowed boundary | 写清允许修改或实现的模块、行为、文档或输出区域。 |
| Forbidden boundary | 写清不得碰的范围、future phase、open decision 和外部系统。 |
| Independent acceptance | 写成任务级 pass/fail 判断，不能只写“满足 PRD”。 |
| Verification refs | 至少一个 `VER-*`、`AC-*`、`DONE-*` 或 planning `CHECK-*`。 |
| Stop conditions | 相关 `STOP/BAR/RISK/OOS/Q/ASM` 必须可见。 |
| Dependencies | 只引用真实上游 `TASK-*`，不得使用范围写法。 |

### 5.6 推导依赖和并行

依赖先从事实推导，再从执行风险补充。判断顺序：

1. 数据结构是否先于消费它的逻辑。
2. 状态机是否先于依赖状态的导出或确认行为。
3. stop/barrier 是否先于可能触发风险的实现。
4. 输出是否先于验证该输出的 verification record。
5. residual-scope note 是否依赖实际输出边界。

并行只在没有 dependency edge 且验收互不遮挡时成立。任何有依赖边的两个任务不得放在同一个 `parallel_group`。

### 5.7 建立阶段目标覆盖

`stage_goal_coverage` 是最后的整体证明，必须覆盖当前 phase 的：

- current-execution `REQ`。
- 对应 `OUT`。
- blocking `DONE`。
- 必要的 stop/defer/residual-scope 输出。

若某个 `REQ/OUT/DONE` 只能由“最终整体完成”证明，说明任务还不够内敛，应拆出独立验收或补 verification task。

### 5.8 运行评审循环

初稿完成后，按以下顺序修：

| Review pass | 目标 | 常见修复 |
| --- | --- | --- |
| Traceability pass | 所有任务 refs 都来自 Agent PRD / contract。 | 删除新事实，补缺失 refs。 |
| Closure pass | 每个任务边界闭合。 | 补 inputs、outputs、allowed/forbidden boundary、stop conditions。 |
| Acceptance pass | 每个任务可独立验收。 | 把整体验收拆成 task-level acceptance。 |
| Dependency pass | 依赖和并行不矛盾。 | 展开范围边；拆分或串行冲突任务。 |
| Coverage pass | 全部非 deferred 任务覆盖阶段目标。 | 补任务、补 defer report，或回到 PRD 修正。 |
| Risk pass | `STOP/BAR/RISK/OOS/Q/ASM` 没有消失。 | 把风险红线挂到具体任务。 |

只有这些 review pass 全部通过，`planning_status` 才能是 `ready`。

## 6. 任务粒度

一个合格任务必须同时满足：

| 维度 | 要求 |
| --- | --- |
| 内敛 | 任务边界闭合，必须自带目标、输入、输出、允许修改范围、禁止范围、验收、验证、停止条件和依赖；不得要求执行者自行补范围。 |
| 单一结果 | 任务完成后有一个可观察产物或状态变化。 |
| 可独立验收 | 单个任务完成后，审查者可以只凭该任务的 acceptance、verification、contract refs 和实际产物判断 pass/fail；不得把“整份 PRD 最终成功”作为唯一验收标准。 |
| 可验证 | 至少关联一个 `VER-*`、`AC-*`、`DONE-*` 或 planning `CHECK-*`。 |
| 可追踪 | `contract_refs` 非空，且引用真实 canonical IDs。 |
| 可停止 | 相关 `STOP-*`、`BAR-*`、`OOS-*` 或 open decision 可见。 |
| 覆盖阶段目标 | 全部非 deferred 任务完成后，必须足以实现当前 `PHASE` 的阶段性目标、相关 `REQ`、`OUT` 和 `DONE`。 |
| 不跨阶段 | 不把 future `PHASE` 工作塞进 current execution。 |
| 不混职责 | 不把 schema、业务逻辑、UI、集成、测试、发布全部塞进一个任务。 |

“内敛”不是要求任务没有依赖，而是要求依赖被显式声明，且任务自身有封闭的验收边界。一个任务可以依赖上游产物，但不能依赖下游任务来证明自己是否合格。

任务过大时按以下顺序拆小：

1. 按 `REQ` 拆：每个 current-execution `REQ` 至少有一个实现任务或验证任务。
2. 按 `DCT/DATA` 拆：数据结构、输入解析、输出格式先稳定。
3. 按 `STATE/FLOW` 拆：状态转移和控制流单独成任务。
4. 按 `VER` 拆：正例、负例、一致性检查、阻断失败分别可见。
5. 按风险拆：涉及 `STOP/BAR/RISK` 的任务必须显式暴露 stop behavior。

任务过小时合并：

- 只有重命名、注释、无独立验证的碎片任务应并入相邻任务。
- 同一文件、同一 contract refs、同一验证命令的小步骤可以合并。
- 不能为了并行而制造没有独立验收价值的任务。

## 7. 任务类型

| 类型 | 何时使用 | 必须引用 |
| --- | --- | --- |
| `foundation` | 建立项目结构、配置、数据模型或 shared interfaces。 | `TECH`、`MOD`、`DCT`、`DATA`、相关 `IN/OUT`。 |
| `implementation` | 实现用户可见或系统行为。 | `REQ`、`AC`、`EXE`、相关 `STATE/FLOW`。 |
| `integration` | 连接外部系统、输入源、存储、模型或运行环境。 | `IN`、`DATA`、`TECH`、`STOP`、`BAR`。 |
| `verification` | 编写或运行验证用例。 | `VER`、`AC`、`DONE`、相关 `REQ/STOP/BAR`。 |
| `documentation` | 更新使用说明、开发说明或运维说明。 | `OUT`、`DONE`、`REF`、必要 `REQ`。 |
| `release` | 打包、迁移、部署、开关、发布检查。 | `OUT`、`DONE`、`GATE`、`STOP`。 |
| `cleanup` | 删除废弃实现或收敛技术债。 | 必须有 `TECH`、`MOD`、`VER` 或明确 `DONE` 支撑。 |

## 8. 拆解算法

```pseudo
function decompose_prd_to_tasks(envelope, runtime_context):
  source_artifacts = build_source_artifacts(envelope, runtime_context)

  if envelope.agent_prd.status != "execution_ready":
    return blocked_execution_task_plan(source_artifacts, "agent_prd_not_execution_ready")

  if has_blocking_gate(envelope.gate_report):
    return blocked_execution_task_plan(source_artifacts, "source_gate_blocked")

  contract = envelope.canonical_contract
  required_execution_types = ["IN", "EXE", "VER", "OUT", "STOP", "DONE"]
  if not object_index_contains(contract, required_execution_types):
    return blocked_execution_task_plan(source_artifacts, "missing_execution_objects")

  if source_artifacts.phase_ref_kind != "canonical_id":
    return blocked_execution_task_plan(source_artifacts, "missing_canonical_phase_ref")

  current_reqs = select_current_execution_requirements(contract)
  if not assert_every(current_reqs has linked AC and VER):
    return blocked_execution_task_plan(source_artifacts, "requirement_verification_link_missing")

  execution_units = []

  for req in current_reqs:
    unit = build_requirement_unit(req)
    unit.acceptance = linked_AC(req)
    unit.verification = linked_VER(req)
    unit.outputs = linked_OUT(req)
    unit.done = linked_DONE(req)
    unit.stops = related_STOP_BAR_RISK(req)
    execution_units.add(unit)

  data_units = derive_data_and_input_units(contract.DCT, contract.DATA, contract.IN)
  behavior_units = derive_flow_state_execution_units(contract.FLOW, contract.STATE, contract.EXE)
  verification_units = derive_verification_units(contract.VER, contract.DONE)

  tasks = slice_units_into_tasks(execution_units, data_units, behavior_units, verification_units)
  tasks = attach_contract_refs(tasks)
  tasks = attach_stop_conditions(tasks)
  tasks = attach_verification_and_done_refs(tasks)

  dependency_edges = infer_dependencies(tasks)
  parallel_groups = infer_parallel_groups(tasks, dependency_edges)
  stage_goal_coverage = map_tasks_to_current_phase_goals(tasks, contract.PHASE, contract.REQ, contract.OUT, contract.DONE)

  validation = validate_task_plan(tasks, dependency_edges, parallel_groups, stage_goal_coverage, envelope)
  if validation.has_blocking_failure:
    return blocked_execution_task_plan(source_artifacts, validation.blocking_reasons)

  return execution_task_plan(source_artifacts, tasks, dependency_edges, parallel_groups, stage_goal_coverage, validation.planning_gate_report)
```

## 9. 依赖推导

依赖只能来自可解释原因，不得按主观顺序硬排。

| 依赖来源 | 规则 |
| --- | --- |
| 数据依赖 | `DCT/DATA/IN` 任务先于消费这些结构的实现任务。 |
| 状态依赖 | `STATE` 任务先于依赖状态规则的 UI、API、导出或验证任务。 |
| 输出依赖 | 产出 `OUT` 的任务先于验证该输出的 `VER/DONE` 任务。 |
| 安全依赖 | `STOP/BAR/RISK` 控制任务先于可能触发风险的实现任务。 |
| 集成依赖 | 外部系统、授权、配置或 runtime reference 先于依赖它的功能任务。 |
| 测试依赖 | 测试设计可以早于实现；测试执行依赖实现产物。 |

禁止依赖：

- “因为习惯上先做后端”。
- “因为看起来更顺”。
- “为了让计划像瀑布模型”。
- “为了占满每个 agent”。

## 10. 并行规则

可以并行的任务必须同时满足：

1. 没有 dependency edge。
2. 修改区域不高度重叠，或有明确合并策略。
3. 不同时改变同一个 canonical decision 的解释。
4. 各自有独立验证或可组合验证。
5. 失败时不会让另一个任务的结果不可判断。

必须串行的情况：

- 数据合同尚未稳定，却要实现依赖该 schema 的逻辑。
- 状态机尚未确定，却要实现导出资格、确认、删除或审批行为。
- Stop/barrier 规则尚未实现，却要实现高风险自动动作。
- 同一个文件或模块需要跨任务大规模重写。

## 11. 阻断与降级

任务拆解过程中遇到以下情况必须 blocked：

| 阻断 | 处理 |
| --- | --- |
| Agent PRD 不是 `execution_ready` | 不生成任务图，返回缺失对象和 gate。 |
| current `REQ` 缺 `AC` 或 `VER` | 不拆实现任务，要求回到 contract/Agent PRD 修复。 |
| 任务需要回答 open `Q` | 生成 human decision task 或 stop report，不得自答。 |
| 任务需要 future `PHASE` 范围 | 标为 deferred，不进入 current task graph。 |
| runtime context 与 contract 冲突 | 停止，要求 contract update 或用户确认。 |
| 任务无法验证 | 不得进入 ready task graph。 |

blocked planning report 必须仍然使用 `execution_task_plan` envelope，而不是临时 prose：

- `planning_status=blocked`。
- `task_graph=[]`、`dependency_edges=[]`、`parallel_groups=[]`。
- `stage_goal_coverage` 可以为空；若已经能定位缺口，必须写 `coverage_status=blocked` 和 `missing_refs`。
- `blocking_reasons` 必须使用稳定原因码，例如 `agent_prd_not_execution_ready`、`source_gate_blocked`、`missing_execution_objects`、`missing_canonical_phase_ref`、`requirement_verification_link_missing`、`open_decision_blocks_execution`、`future_phase_requested`、`runtime_contract_conflict`、`task_not_independently_verifiable`。
- `missing_required_refs` 只放缺失的 canonical refs 或 object types，例如 `VER`、`PHASE-001`、`REQ-003`。
- `required_fixes` 写回到 contract、Agent PRD、runtime context 或用户决策的具体修复动作。
- `planning_gate_report` 必须包含失败 check，且 `status=blocked`、`evidence_refs` 为 ID-only 数组、`evidence_summary` 解释原因。

## 12. 任务计划门禁

| Check | 阻断条件 |
| --- | --- |
| `CHECK-001: task traceability` | 任一 `TASK` 缺 `contract_refs`，或引用不存在。 |
| `CHECK-002: requirement coverage` | current-execution `REQ` 没有实现任务或验证任务。 |
| `CHECK-003: verification coverage` | 任一 `TASK` 缺 `verification_refs`、`done_refs` 或 planning `CHECK`。 |
| `CHECK-004: stop visibility` | 涉及 `STOP/BAR/RISK/OOS/Q/ASM` 的任务没有 stop handling。 |
| `CHECK-005: dependency soundness` | dependency edge 没有原因，或存在循环依赖。 |
| `CHECK-006: phase integrity` | future `PHASE` 被放进 current execution。 |
| `CHECK-007: no new facts` | 任务新增 contract 中不存在的需求、字段、验证或技术决策。 |
| `CHECK-008: parallel safety` | parallel group 中存在未声明的文件、schema、状态或输出冲突。 |
| `CHECK-009: done alignment` | 任务完成条件无法汇总到 `DONE-*`。 |
| `CHECK-010: task closure` | 任一任务缺少输入、输出、允许修改范围、禁止范围、验收、验证、停止条件或依赖声明，导致执行者需要自行补范围。 |
| `CHECK-011: independent acceptance` | 任一任务不能被单独验收，或只能通过整份 PRD 最终完成来判断是否合格。 |
| `CHECK-012: phase goal coverage` | 全部非 deferred 任务完成后，仍无法覆盖当前 `PHASE` 的阶段目标、current-execution `REQ`、`OUT` 或 `DONE`。 |

任一 blocking check 失败时，`planning_status=blocked`，不得把任务图交给执行 agent。

### 12.1 Validator 最低实现

实现方至少要提供以下 deterministic checks；只检查文件存在不算通过：

| Validator check | 必须验证 |
| --- | --- |
| JSON shape | `execution_task_plan` 可解析，包含 `plan_id`、`planning_source_mode`、`source_artifacts`、`planning_status`、`task_graph`、`dependency_edges`、`parallel_groups`、`stage_goal_coverage`、`planning_gate_report`。 |
| Ready invariants | `planning_status=ready` 时 source mode 必须是 `contract_backed`，Agent PRD 必须是 `execution_ready`，phase ref 必须是 canonical `PHASE-*`，且 blocking arrays 为空。 |
| Blocked invariants | `planning_status=blocked` 时不得输出可执行 `task_graph`、`dependency_edges` 或 `parallel_groups`，且必须有 blocking reason、missing refs 或 required fix。 |
| Ref existence | 所有 `contract_refs`、`verification_refs`、`done_refs`、`stop_refs`、`stage_goal_coverage.goal_refs` 和 `planning_gate_report.evidence_refs` 必须存在于 source contract 或 execution plan ID 集。 |
| Evidence refs | `planning_gate_report.evidence_refs` 只能包含稳定 ID；解释性文字只能进入 `evidence_summary`。 |
| Dependency graph | `dependency_edges` 必须引用存在的 `TASK-*`，必须无环，且 edge reason 非空。 |
| Parallel safety | `parallel_groups` 只能引用存在的任务；存在 dependency edge 的任务不得处于同一 `parallel_safe` group；冲突时必须 `status=blocked` 或拆分任务。 |
| Task closure | 每个 ready task 必须有 inputs、outputs、allowed/forbidden boundary、acceptance、verification refs、stop conditions 和 dependencies。 |
| Coverage | current phase 的 `REQ/OUT/DONE` 必须被非 deferred task 覆盖；缺口必须让 `planning_status=blocked`。 |
| No new facts | 任务不得出现 source contract / Agent PRD 中不存在的需求、字段、验收、验证、技术决策或范围。 |

## 13. 输出形态

推荐输出顺序：

1. Planning status。
2. Source contract and Agent PRD status。
3. Task graph summary。
4. Task table。
5. Dependency edges。
6. Parallel groups。
7. Stop/defer report。
8. Verification and done mapping。
9. Stage goal coverage。
10. Planning gate report。

任务表推荐字段：

| 字段 | 说明 |
| --- | --- |
| Task ID | `TASK-*`，只在 execution task plan 内稳定。 |
| Title | 动词开头，描述可观察结果。 |
| Type | 使用第 7 节枚举。 |
| Contract refs | 至少一个 canonical ID。 |
| Verification refs | `VER-*` 或 planning `CHECK-*`。 |
| Done refs | 对应 `DONE-*`。 |
| Dependencies | 上游 `TASK-*`。 |
| Stop refs | 相关 `STOP/BAR/RISK/Q/ASM/OOS`。 |
| Acceptance | 任务级完成判断。 |

`Stage goal coverage` 必须说明当前 `PHASE` 的阶段性目标由哪些任务闭合，至少包含 `phase_ref`、`phase_label`、`goal_refs`、`required_task_refs`、`coverage_status` 和 `missing_refs`。ready plan 的 `phase_ref` 必须是 canonical `PHASE-*`；若只消费 rendered Agent PRD 且没有可见 `PHASE-*`，只能输出 blocked diagnostic report，并在 `source_artifacts.phase_ref_kind=rendered_label` 与 `phase_ref_fallback_reason` 中说明。若 `coverage_status` 不是 `covered`，`planning_status` 必须是 `blocked`。

## 14. 常见失败模式

| 失败模式 | 表现 | 修正 |
| --- | --- | --- |
| 按技术层随手拆 | “前端任务、后端任务、测试任务”无法追踪 `REQ/AC`。 | 先按 contract refs 建任务，再映射技术层。 |
| 任务新增需求 | 任务里出现 Agent PRD 没有的功能或字段。 | 删除或回到 contract update。 |
| 验证后置丢失 | 实现任务有了，`VER` 没进入计划。 | 每个任务必须带 verification 或 done refs。 |
| 并行过度 | 多个任务同时修改同一状态机或 schema。 | 增加 dependency edge 或合并任务。 |
| Stop 条件消失 | Agent 执行时不知道何时问人。 | 将 `STOP/BAR/RISK/Q/ASM` 显式挂到任务。 |
| 未来阶段混入 | Phase 2 工作进入当前 execution。 | 标为 deferred，放入 stop/defer report。 |
| 用任务图替代 PRD | 执行 agent 只看任务，不看 source of truth。 | 每个任务必须引用 Agent PRD 与 contract refs。 |
| 任务不内敛 | 任务描述依赖隐含上下文，缺输入、输出、文件边界或 stop 条件。 | 补齐封闭边界；补不齐则 blocked。 |
| 不能独立验收 | 任务只能等全项目完成后才知道是否合格。 | 拆出任务级 acceptance 和 verification；没有独立验收价值则合并。 |
| 阶段目标漏项 | 所有任务做完仍不能实现当前 PRD 阶段目标。 | 补 `stage_goal_coverage` 缺口，或回到 contract/Agent PRD 修正。 |

## 15. 示例和校准

下表示例只展示任务图形态。真实 `execution_task_plan` 必须引用当前 envelope 中实际存在的 canonical IDs；不得照抄示例 ID 到不包含这些对象的合同中。

完整好实例见 `references/execution-task-plan-example-meeting-action-hub.md`。该文件展示如何从现有 `agent-prd-example-meeting-action-hub.md` 派生内敛、可独立验收、覆盖 Phase 1 阶段目标的任务图。

| Task ID | Type | Title | Contract refs | Verification refs | Done refs | Dependencies |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-001 | foundation | Define input schema and validation boundary. | DCT-001, IN-001, DATA-001 | VER-001 | DONE-001 | - |
| TASK-002 | implementation | Implement the current requirement behavior. | REQ-001, AC-001, EXE-001 | VER-001 | DONE-001 | TASK-001 |
| TASK-003 | integration | Connect state, flow, and output behavior. | REQ-001, STATE-001, FLOW-001, OUT-001 | VER-001 | DONE-001 | TASK-001 |
| TASK-004 | verification | Run consistency and blocking failure checks. | VER-001, GATE-007, STOP-001 | VER-001 | DONE-001 | TASK-002, TASK-003 |

验收真实任务计划时，仍必须覆盖当前 execution 的全部 `REQ/AC/VER/OUT/DONE/STOP`。

### 15.1 Blocked Fixtures

除完整好实例外，任务拆解实现至少要用以下负例和边界例校准 blocked path：

| Fixture | 输入缺陷 | 期望输出 |
| --- | --- | --- |
| Agent PRD not ready | `source_artifacts.agent_prd_status=draft` 或 `blocked`。 | `planning_status=blocked`；`task_graph=[]`；`blocking_reasons` 包含 `agent_prd_not_execution_ready`；`required_fixes` 指向 Agent PRD gate 修复。 |
| Missing verification link | current `REQ-*` 没有 `AC-*` 或 `VER-*`。 | `planning_status=blocked`；`missing_required_refs` 包含缺失的 `AC` 或 `VER`；不得生成实现任务。 |
| Future phase request | runtime context 或用户请求要求把 future `PHASE` 或 `OOS-*` 当作当前执行任务实现。 | `planning_status=blocked`；`blocking_reasons` 包含 `future_phase_requested`；不得进入 current `task_graph`。若 future scope 只作为边界说明出现，则只能进入 stop/defer report，不阻断 ready plan。 |
| Rendered-only source | 只有渲染后的 Agent PRD，无法访问 canonical contract 或 `PHASE-*`。 | `planning_source_mode=rendered_agent_prd_only`；`phase_ref_kind=rendered_label`；`planning_status=blocked`；不得交给执行 agent。 |

这些 fixtures 的验收重点不是“能输出一些文字”，而是 blocked status、空任务图、稳定 reason code、missing refs 和 required fixes 都能被 validator 机械判断。

### 15.2 Minimal Blocked Output Example

下面是 Agent PRD 尚未 execution-ready 时的最小 blocked envelope。它不是可执行任务计划，执行 agent 不得消费其中的空任务图。

```json
{
  "plan_id": "ETP-BLOCKED-001",
  "planning_source_mode": "contract_backed",
  "source_artifacts": {
    "contract_ref": "canonical contract URI, path, or envelope id",
    "contract_version": "1.8",
    "agent_prd_ref": "agent-prd.md",
    "agent_prd_status": "draft",
    "phase_ref": "PHASE-001",
    "phase_label": "Phase 1 MVP",
    "phase_ref_kind": "canonical_id",
    "phase_ref_fallback_reason": ""
  },
  "planning_status": "blocked",
  "blocking_reasons": ["agent_prd_not_execution_ready"],
  "missing_required_refs": [],
  "required_fixes": [
    "Run Agent PRD gates until source_artifacts.agent_prd_status becomes execution_ready."
  ],
  "task_graph": [],
  "dependency_edges": [],
  "parallel_groups": [],
  "stage_goal_coverage": [],
  "planning_gate_report": [
    {
      "check_id": "CHECK-000",
      "name": "source readiness",
      "status": "blocked",
      "evidence_refs": ["PHASE-001"],
      "evidence_summary": "The source Agent PRD is draft, so execution task planning cannot produce a ready task graph.",
      "required_fix": "Make the Agent PRD execution-ready and rerun task planning."
    }
  ]
}
```
