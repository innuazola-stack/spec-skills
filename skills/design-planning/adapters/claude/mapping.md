# Claude Adapter Mapping

| Core requirement | Mapping | Notes |
| --- | --- | --- |
| Read PRD/HLD under target `docs/` | prompt | Claude is instructed to inspect all source documents first. |
| Produce planning JSON and fixtures | prompt | Paths and schemas are fixed by the harness core. |
| Produce detailed design documents under `docs/design` | prompt | Documentation-only constraint is repeated in task fixtures. |
| Run structural validators | manual | Claude must ask the host/runtime to execute validator commands when tools are unavailable. |
| Semantic review gate | prompt | Claude reports pass/revise/fail with blocker taxonomy. |
| Unsupported behavior | manual | Filesystem writes and validator execution depend on host tooling. |
