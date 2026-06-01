# Codex Installation Notes

To install this harness as a Codex skill, copy `skill/` into the active Codex skills directory as `spec-intake`.

The portable harness source remains in the repository root:

- `manifest.yaml`
- `agent.md`
- `workflow.md`
- `rules.md`
- `schemas/`
- `adapters/codex/`
- `evals/cases/`

Before copying or packaging, run:

```powershell
C:\Users\54256213\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe skill\scripts\validate_skill_package.py skill
C:\Users\54256213\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe tests\harness_source_regression.py
C:\Users\54256213\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe tests\validator_regression.py
```
