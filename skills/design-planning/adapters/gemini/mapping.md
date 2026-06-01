# Gemini Adapter Mapping

| Core requirement | Mapping | Notes |
| --- | --- | --- |
| Source inventory | prompt | Gemini must summarize PRD/HLD evidence before task decomposition. |
| JSON planning output | prompt | Must follow `schemas/design-planning.schema.json`. |
| Fixture generation | prompt | Must emit per-task `prompt.md`, `AGENTS.md`, and `CLAUDE.md`. |
| Validator execution | manual | Requires host tooling when Gemini lacks local execution. |
| Semantic review | prompt | Use pass/revise/fail verdicts. |
| Unsupported behavior | manual | Runtime cannot guarantee filesystem or command access without host integration. |
