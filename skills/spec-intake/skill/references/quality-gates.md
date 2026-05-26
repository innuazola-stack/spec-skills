# Quality Gates

Use this reference before claiming any spec package is ready.

## Contract Gates

Block ready output when:

- required IDs are missing or dangling
- `object_index` diverges from `objects`
- `SRC` payload lacks a valid `source_type` or auditable content/target for user sources
- `RB` unsupported claims are non-empty
- `traceability_summary` diverges from `render_blocks` or `traceability`
- `quality_gates` diverges from `gate_report.gate_id`
- top-level contract views diverge from `objects` and `object_index`
- `GATE-*` payload diverges from its `gate_report` row
- `CORE.status=blocked`, current `REQ.status=blocked`, or `STOP.status=triggered` affects readiness
- `GATE.status=blocked` affects the target
- `Q` or `ASM` blocks the target and has missing or open status
- `gate_report.status=warning` lacks message or required fix
- Human PRD and Agent PRD disagree on shared facts
- Agent PRD lacks execution objects, verification, stop conditions, or done criteria
- execution-ready Agent PRD text lacks required execution sections
- rendered requirements cannot be traced to source `REQ-*`
- decision traceability type, ref, and status do not agree
- resolved decisions lack resolution refs or `TRACE.relation` is outside the allowed relation vocabulary

## Task Planning Gates

Block ready task planning when:

- source Agent PRD status in the plan does not match the canonical contract
- `source_artifacts` refs, file names, version, status, or phase type diverge from the contract
- task refs are missing or not from source contract
- current `REQ` coverage is incomplete
- current phase has no current `REQ`
- future-phase `REQ` enters a ready current-phase task
- linked `AC` or execution `IN/EXE/VER/OUT/STOP/DONE` coverage is incomplete
- verification or done coverage is incomplete
- stop/risk/scope controls disappear
- dependencies are cyclic, unexplained, self-referential, or inconsistent between task cards and `dependency_edges`
- future phase work enters current execution
- tasks add new facts
- ready tasks hide `IN/OUT/STOP` refs in generic `contract_refs` instead of closure fields
- task type or ready-plan task status is outside the allowed vocabulary
- parallel groups hide conflicts
- planning gate evidence uses `CHECK-*`, non-ID values, or missing refs
- dependency edge `contract_refs` use execution-plan IDs instead of canonical contract refs
- tasks cannot be independently accepted
- stage goal coverage is partial or blocked

## Subjective Review Rubric

Score each dimension `pass`, `revise`, or `fail`:

| Dimension | Pass condition |
| --- | --- |
| Product clarity | User, problem, value, MVP, and non-goals are understandable. |
| Honesty | Unknowns are explicit and do not become facts. |
| Human usefulness | Human PRD supports decision-making without implementation clutter. |
| Agent executability | Agent PRD tells an agent what to do, avoid, verify, and stop on. |
| Task usefulness | Tasks are closed, independently acceptable, and cover the phase. |
| Traceability | Important claims link to contract refs and source refs. |

Any `fail` blocks ready. Any `revise` requires either patching or explicitly downgrading output status.

## Validation Script

When the package exists on disk, run:

```bash
python <path-to-spec-intake-skill>/scripts/validate_spec_intake_package.py <output-dir>
```

In this repository's development layout, run the same validator as `python skill/scripts/validate_spec_intake_package.py <output-dir>` from `skills/spec-intake`.

For repository development, also run:

```bash
python tests/validator_regression.py
```

The regression suite must include both blocked and ready fixtures, plus false-positive probes for source readiness, coverage, dependency, status, render-block, task typed refs, payload schema, object-index drift, summary drift, derived traceability, gate/report drift, readiness blockers, source payload auditability, planning evidence type, rendered-only blocked planning, phase source type, and ID namespace failures.

Use the bundled Python executable if `python` is unavailable. Report the exact verdict. Do not claim validation passed if the script was skipped.
