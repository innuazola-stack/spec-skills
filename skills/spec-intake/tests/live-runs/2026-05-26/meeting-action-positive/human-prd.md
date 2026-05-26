# Human PRD Review Fixture

Source contract: `contract-envelope.json`

Render status: `review_ready`

## 目标

为会议后的执行跟进提供一个第一版工具：只处理已授权的会议文字记录，提取行动项、负责人、截止时间和原文证据，并在人工确认后导出 Markdown。

## 范围

Phase 1 只覆盖 `SCOPE-001` 和 `REQ-001`。`OOS-001` 明确排除 Jira、Linear、Asana、日历或邮件等外部任务自动创建。

## 验收

`AC-001` 要求在给定已授权文字记录时，输出可确认的行动项，并且在确认前不能导出最终 Markdown。

## 状态

当前 Human PRD 可进入 review_ready。
