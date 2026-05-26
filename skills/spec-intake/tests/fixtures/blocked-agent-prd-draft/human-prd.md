# Human PRD Draft Fixture

Source contract: `contract-envelope.json`

Render status: `draft`

## 目标

这个 fixture 用来验证当 Agent PRD 仍是 draft 时，规范包必须保持诚实的 blocked 状态。

## 范围

只验证 blocked planning 行为，不声明任何真实产品执行范围。

## 验收

任务计划必须输出 `planning_status=blocked`，并且 `task_graph`、`dependency_edges`、`parallel_groups` 为空。

## 风险和开放问题

`Q-001` 仍然 open：执行输入、验证用例、停止条件和完成标准尚未定义。
