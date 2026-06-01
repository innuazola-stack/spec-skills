# OpenClaw Adapter Mapping

| Core requirement | Mapping | Notes |
| --- | --- | --- |
| PRD/HLD reading | prompt | Must read target `docs/` before planning. |
| Staged review gates | prompt | Follow `workflow.md` gate order and verdict vocabulary. |
| JSON/schema compliance | tool | Use validator when local execution is available. |
| Task fixtures | prompt | Fixtures must be documentation-only and task-scoped. |
| Unsupported behavior | manual | Host must provide filesystem and command execution capability. |
