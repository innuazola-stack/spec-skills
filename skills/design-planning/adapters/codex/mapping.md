# Codex Adapter Mapping

| Core requirement | Mapping | Notes |
| --- | --- | --- |
| Read PRD/HLD under target `docs/` | native | Codex can inspect workspace files. |
| Produce planning JSON and fixtures | native | Use file editing tools with the harness file rules. |
| Produce detailed design documents under `docs/design` | native | No product code changes are allowed. |
| Run structural validators | tool | Use the local Python validator commands. |
| Semantic review gate | prompt | Codex must report verdict, blockers, and residual risks. |
| Release packaging | tool | Use `tools/build_release.py` from the harness root. |
| Unsupported behavior | manual | User approval may be needed for writes outside the current writable roots. |
