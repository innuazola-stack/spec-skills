# PRD Writing Skill Design Brief

## Purpose

Create a reusable writing skill that helps agents produce professional Simplified Chinese software product PRDs that are concise, source-backed, final-view only, and useful to human stakeholders.

## Design Choices

- Keep runtime instructions in `skill/SKILL.md`.
- Store the 10+ external methodology references in `skill/references/prd-methodology.md`.
- Store the output contract and quality checklist in `skill/references/prd-output-contract.md`.
- Provide one reusable PRD template in `skill/assets/PRD.template.md`.
- Provide `tools/validate_skill_static.py` for skill-package regression checks.
- Provide `tools/validate_prd_document.py` so the skill can both write PRDs and block invalid PRDs before delivery.
