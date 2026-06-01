from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "SKILL.md",
    "manifest.yaml",
    "agent.md",
    "workflow.md",
    "rules.md",
    "schemas/design-planning.schema.json",
    "validators/validate_design_planning.py",
    "validators/validate_harness.py",
    "tools/build_release.py",
    "evals/cases/positive-rust-prd-hld.md",
    "evals/cases/negative-missing-hld.md",
    "evals/cases/boundary-future-phase.md",
    "adapters/codex/install.md",
    "adapters/codex/mapping.md",
    "adapters/codex/system-prompt.md",
    "adapters/claude/install.md",
    "adapters/claude/mapping.md",
    "adapters/claude/CLAUDE.md",
    "adapters/gemini/install.md",
    "adapters/gemini/mapping.md",
    "adapters/gemini/GEMINI.md",
    "adapters/openclaw/install.md",
    "adapters/openclaw/mapping.md",
    "adapters/openclaw/OPENCLAW.md",
    "adapters/hermas/install.md",
    "adapters/hermas/mapping.md",
    "adapters/hermas/HERMAS.md",
    "skill/SKILL.md",
    "skill/references/methodology.md",
    "skill/references/rust-detailed-design.md",
    "skill/references/output-contract.md",
    "skill/assets/TASK_PROMPT.fixture.md",
    "skill/assets/AGENTS.template.md",
    "skill/assets/CLAUDE.template.md",
    "docs/design-brief.md",
    "docs/file-plan.md",
    "docs/evaluation-spec.md",
    "docs/test-plan.md",
    "tests/cases/positive-rust-prd-hld.md",
    "tests/cases/negative-missing-hld.md",
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
if not skill.startswith("---\nname: design-planning\n"):
    fail("SKILL.md frontmatter name is missing or invalid")
if "description: Use when " not in skill:
    fail("SKILL.md description must start with Use when")
if "The default planning output root is `tasks/design`" not in skill:
    fail("SKILL.md must set default planning root to tasks/design")

required_terms = [
    "harness-workflow",
    "workflow.md",
    "<planning-output-root>/design-planning.json",
    "<planning-output-root>/fixtures/<TASK-ID>",
    "Detailed design document outputs are fixed under target `docs/design/`",
    "AGENTS.md",
    "CLAUDE.md",
    "Rust",
    "DAG",
    "No standalone starter prompt template",
]
for term in required_terms:
    if term not in skill:
        fail(f"SKILL.md missing required term: {term}")

for path in ROOT.rglob("*"):
    if path.is_file() and path.name.lower() in {"prompt_template.md", "starter_prompt.md", "starter-prompt.md"}:
        fail(f"standalone starter prompt template-like file should not exist: {path.relative_to(ROOT)}")

for template in ["skill/assets/TASK_PROMPT.fixture.md", "skill/assets/AGENTS.template.md", "skill/assets/CLAUDE.template.md"]:
    text = (ROOT / template).read_text(encoding="utf-8")
    forbidden_template_markers = ["Copy this " + "prompt", "Starter " + "Prompt"]
    if any(marker in text for marker in forbidden_template_markers):
        fail(f"{template} contains prompt-template wording")

output_contract = (ROOT / "skill/references/output-contract.md").read_text(encoding="utf-8")
if '"output_root": "tasks/design | user-specified planning output root"' not in output_contract:
    fail("output contract must show tasks/design as the default planning output root")
for term in [
    '"tasks": []',
    '"dag": {',
    '"fixtures": []',
    '"output_root":',
    '"detailed_design_root":',
    '"planning_review_stages": []',
    "design_doc_path",
    '"external_dependencies": []',
    "docs/design/rust-implementation-design.md",
    "task_type=design_acceptance",
    "staged_review_readiness",
    "design_acceptance_task",
    "<planning-output-root>/fixtures/<TASK-ID>/prompt.md",
    "<planning-output-root>/fixtures/<TASK-ID>/AGENTS.md",
    "<planning-output-root>/fixtures/<TASK-ID>/CLAUDE.md",
]:
    if term not in output_contract:
        fail(f"output contract missing required planning/fixture term: {term}")

evaluation = (ROOT / "docs/evaluation-spec.md").read_text(encoding="utf-8")
for term in ["Exact Review Query", "Scoring Rule", "Pass bar", "planning_review_stages", "design_acceptance", "Validator coverage"]:
    if term not in evaluation:
        fail(f"evaluation spec missing required review term: {term}")

manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
for term in ["type: harness-workflow", "default_planning_output_root: tasks/design", "supported_adapters:"]:
    if term not in manifest:
        fail(f"manifest missing required harness term: {term}")

for rel in [
    "evals/cases/positive-rust-prd-hld.md",
    "evals/cases/negative-missing-hld.md",
    "evals/cases/boundary-future-phase.md",
]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    for heading in ["## Prompt", "## Expected Behavior", "## Forbidden Behavior", "## Scoring Rule", "## Pass Bar"]:
        if heading not in text:
            fail(f"{rel} missing eval heading: {heading}")

repo_root = ROOT.parents[1]
generator = (repo_root / "tools/generate_spec_scheduler_design_planning.py").read_text(encoding="utf-8")
for forbidden in [
    'task_type": "foundation"',
    'task_type": "implementation"',
    'task_type": "verification"',
    "Create Rust workspace",
    "Implement RuntimeStore",
    "Project builds with empty/stub modules",
    '"cargo test',
]:
    if forbidden in generator:
        fail(f"generator contains development-task wording: {forbidden}")

for rel in ["skill/SKILL.md", "skill/references/output-contract.md", "skill/references/methodology.md", "manifest.yaml"]:
    text = (ROOT / rel).read_text(encoding="utf-8")
    for forbidden in [
        "default_planning_output_root: docs/design",
        "The default planning output root is `docs/design`",
        '"output_root": "docs/design | user-specified planning output root"',
    ]:
        if forbidden in text:
            fail(f"{rel} contains stale planning-root wording: {forbidden}")

print("PASS: design-planning static validation")
