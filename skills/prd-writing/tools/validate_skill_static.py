from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "manifest.yaml",
    "agent.md",
    "workflow.md",
    "rules.md",
    "skill/SKILL.md",
    "skill/references/prd-methodology.md",
    "skill/references/prd-output-contract.md",
    "skill/assets/PRD.template.md",
    "adapters/codex/SKILL.md",
    "tools/validate_prd_document.py",
    "tools/build_release.py",
    "releases/1.0.0.md",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


for rel in REQUIRED_FILES:
    if not (ROOT / rel).exists():
        fail(f"missing {rel}")

skill = (ROOT / "skill/SKILL.md").read_text(encoding="utf-8")
if not skill.startswith("---\nname: prd-writing\n"):
    fail("SKILL.md frontmatter name is missing or invalid")
if "description: Use when " not in skill:
    fail("SKILL.md description must start with Use when")

for term in [
    "Simplified Chinese",
    "修订记录",
    "source-backed",
    "参考文献",
    "Mermaid",
    "LaTeX",
    "Do not fabricate facts",
    "Blocking Gates",
    "validate_prd_document.py",
]:
    if term not in skill:
        fail(f"SKILL.md missing required term: {term}")

manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
for term in [
    "version: 1.0.0",
    "release_builder: tools/build_release.py",
    "release_artifacts_built",
]:
    if term not in manifest:
        fail(f"manifest missing release term: {term}")

methodology = (ROOT / "skill/references/prd-methodology.md").read_text(encoding="utf-8")
source_ids = set(re.findall(r"\| M\d{2} \|", methodology))
if len(source_ids) < 10:
    fail("methodology reference must include at least 10 external source IDs")
for term in ["Atlassian", "Aha!", "Productboard", "Airtable", "Product School", "Perforce", "Roman Pichler", "Non-functional Requirements"]:
    if term not in methodology:
        fail(f"methodology missing expected source or concept: {term}")

contract = (ROOT / "skill/references/prd-output-contract.md").read_text(encoding="utf-8")
for term in [
    "## 修订记录",
    "Every material claim has a source marker",
    "Reference round-trip gate",
    "Methodology grounding gate",
    "Product-fact gate",
    "Requirement Table Contract",
    "Acceptance Criteria Contract",
    "Traceability Matrix Contract",
    "Final Review Checklist",
    "validate_prd_document.py",
]:
    if term not in contract:
        fail(f"output contract missing required term: {term}")

template = (ROOT / "skill/assets/PRD.template.md").read_text(encoding="utf-8")
if not template.startswith("# <产品/功能名称> 产品需求文档（PRD）\n\n## 修订记录"):
    fail("PRD template must begin with title followed by revision record")
for term in ["```mermaid", "```latex", "需求追踪矩阵", "参考文献"]:
    if term not in template:
        fail(f"template missing required expression or section: {term}")

print("PASS: prd-writing static validation")
