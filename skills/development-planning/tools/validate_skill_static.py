from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "skill/SKILL.md",
    "skill/references/methodology.md",
    "skill/references/output-contract.md",
    "skill/references/planning-quality-model.md",
    "skill/assets/TASK_DESCRIPTION.template.md",
    "skill/assets/TASK_PROMPT.fixture.md",
    "skill/assets/AGENTS.template.md",
    "skill/assets/CLAUDE.template.md",
    "docs/design-brief.md",
    "docs/file-plan.md",
    "docs/evaluation-spec.md",
    "docs/test-plan.md",
    "tests/cases/positive-prd-hld-lld.md",
    "tests/cases/negative-missing-lld.md",
    "tests/cases/boundary-future-phase.md",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


for rel in REQUIRED_FILES:
    path = ROOT / rel
    if not path.exists():
        fail(f"missing {rel}")

skill = (ROOT / "skill/SKILL.md").read_text(encoding="utf-8")
if not skill.startswith("---\nname: development-planning\n"):
    fail("SKILL.md frontmatter name is missing or invalid")
if "description: Use when " not in skill:
    fail("SKILL.md description must start with Use when")

required_terms = [
    "<planning-output-root>/development-planning.json",
    "<planning-output-root>/<TASK-ID>/task.md",
    "tasks/development",
    "planning task",
    "PRD/HLD/LLD",
    "DAG",
    "cohesive",
    "independently acceptable",
    "final delivery acceptance task",
    "Harness-style review stages",
    "execution order",
    "AGENTS.md",
    "CLAUDE.md",
    "No standalone starter prompt template",
]
for term in required_terms:
    if term not in skill:
        fail(f"SKILL.md missing required term: {term}")

for path in ROOT.rglob("*"):
    if path.is_file() and path.name.lower() in {"prompt_template.md", "starter_prompt.md", "starter-prompt.md"}:
        fail(f"standalone starter prompt template-like file should not exist: {path.relative_to(ROOT)}")

for template in [
    "skill/assets/TASK_DESCRIPTION.template.md",
    "skill/assets/TASK_PROMPT.fixture.md",
    "skill/assets/AGENTS.template.md",
    "skill/assets/CLAUDE.template.md",
]:
    text = (ROOT / template).read_text(encoding="utf-8")
    forbidden_template_markers = ["Copy this " + "prompt", "Starter " + "Prompt"]
    if any(marker in text for marker in forbidden_template_markers):
        fail(f"{template} contains prompt-template wording")

output_contract = (ROOT / "skill/references/output-contract.md").read_text(encoding="utf-8")
for term in [
    '"tasks": []',
    '"dag": {',
    '"fixtures": []',
    '"output_root":',
    '"execution_order": []',
    '"delivery_acceptance": {}',
    '"planning_harness_model":',
    '"phase_reports": []',
    '"task_logic_review": {}',
    '"plan_integrity_review": {}',
    "task_type=delivery_acceptance",
    "consumed_output",
    '"task_descriptions": []',
    "task_description_path",
    "<planning-output-root>/<TASK-ID>/task.md",
    "<planning-output-root>/<TASK-ID>/prompt.md",
    "<planning-output-root>/<TASK-ID>/AGENTS.md",
    "<planning-output-root>/<TASK-ID>/CLAUDE.md",
]:
    if term not in output_contract:
        fail(f"output contract missing required planning/fixture term: {term}")

evaluation = (ROOT / "docs/evaluation-spec.md").read_text(encoding="utf-8")
for term in [
    "Exact Review Query",
    "Scoring Rule",
    "Pass bar",
    "Final delivery acceptance task",
    "tasks/development",
    "Harness-style staged planning",
    "task_logic_review",
    "plan_integrity_review",
]:
    if term not in evaluation:
        fail(f"evaluation spec missing required review term: {term}")

for case in [
    "tests/cases/positive-prd-hld-lld.md",
    "tests/cases/negative-missing-lld.md",
    "tests/cases/boundary-future-phase.md",
]:
    text = (ROOT / case).read_text(encoding="utf-8")
    for term in ["## Prompt", "## Expected Behavior", "## Forbidden Behavior", "## Scoring Rule", "## Pass Bar"]:
        if term not in text:
            fail(f"{case} missing eval section: {term}")

print("PASS: development-planning static validation")
