from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "manifest.yaml",
    "SKILL.md",
    "agents/openai.yaml",
    "references/brief-methodology.md",
    "references/brief-output-contract.md",
    "assets/Brief.template.md",
    "releases/1.0.0.md",
]

SKILL_REQUIRED_SNIPPETS = [
    "必须使用专业、正式的简体中文",
    "文档读者是人类",
    "text、table、Mermaid、LaTeX",
    "只表达最终观点和结论",
    "所有重要观点、事实、指标、风险、约束和建议都要有出处标记",
    "文档最前面必须是修订表",
    "文档必须紧扣目的和主题",
    "禁止冗余",
]

CONTRACT_REQUIRED_SNIPPETS = [
    "必须使用专业、正式的简体中文",
    "人类决策者",
    "修订表",
    "Mermaid",
    "LaTeX",
    "Blocking Gates",
    "Scoring Rubric",
    "Review Checklist",
    "Reference round trip",
    "Topic focus",
]

TEMPLATE_REQUIRED_SNIPPETS = [
    "## 修订记录",
    "## 决策摘要",
    "## 参考资料",
    "```mermaid",
    "```latex",
    "交付前删除所有未使用的模板占位符",
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8-sig")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_required_files() -> None:
    missing = [rel for rel in REQUIRED_FILES if not (ROOT / rel).is_file()]
    require(not missing, "Missing required files: " + ", ".join(missing))


def check_manifest() -> None:
    text = read("manifest.yaml")
    require("name: brief-writing" in text, "manifest name mismatch")
    require("version: 1.0.0" in text, "manifest version mismatch")
    for rel in REQUIRED_FILES[1:]:
        require(rel in text or rel.startswith("releases/"), f"manifest missing {rel}")


def check_skill_frontmatter() -> None:
    text = read("SKILL.md")
    require(text.startswith("---\n"), "SKILL.md missing YAML frontmatter")
    match = re.match(r"---\n(?P<frontmatter>.*?)\n---\n", text, re.DOTALL)
    require(match is not None, "SKILL.md frontmatter is not closed")
    frontmatter = match.group("frontmatter")
    require("name: brief-writing" in frontmatter, "SKILL.md name mismatch")
    require("description:" in frontmatter, "SKILL.md missing description")
    require("[TODO" not in text and "TODO]" not in text, "SKILL.md contains TODO")
    for snippet in SKILL_REQUIRED_SNIPPETS:
        require(snippet in text, f"SKILL.md missing required snippet: {snippet}")


def check_references_and_template() -> None:
    methodology = read("references/brief-methodology.md")
    require(methodology.count("https://") >= 10, "methodology must include at least 10 external sources")
    require("Distilled Brief Logic" in methodology, "methodology missing brief logic")
    require("Evaluation Standards" in methodology, "methodology missing evaluation standards")

    contract = read("references/brief-output-contract.md")
    for snippet in CONTRACT_REQUIRED_SNIPPETS:
        require(snippet in contract, f"output contract missing required snippet: {snippet}")

    template = read("assets/Brief.template.md")
    for snippet in TEMPLATE_REQUIRED_SNIPPETS:
        require(snippet in template, f"template missing required snippet: {snippet}")


def check_openai_yaml() -> None:
    text = read("agents/openai.yaml")
    require('display_name: "Brief Writing"' in text, "openai.yaml display name mismatch")
    require("Use $brief-writing" in text, "openai.yaml default prompt must reference $brief-writing")


def check_zip(path: Path) -> None:
    require(path.is_file(), f"missing artifact: {path}")
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
    required = set(REQUIRED_FILES)
    required.update({"tools/validate_skill_static.py", "tools/build_release.py"})
    missing = sorted(required - names)
    require(not missing, f"{path.name} missing: " + ", ".join(missing))


def main() -> int:
    check_required_files()
    check_manifest()
    check_skill_frontmatter()
    check_references_and_template()
    check_openai_yaml()

    dist = ROOT / "dist"
    release_manifest = dist / "release-manifest.yaml"
    if release_manifest.exists():
        text = release_manifest.read_text(encoding="utf-8")
        require("name: brief-writing" in text, "release manifest name mismatch")
        require("version: 1.0.0" in text, "release manifest version mismatch")
        check_zip(dist / "brief-writing-1.0.0-source.zip")
        check_zip(dist / "brief-writing-1.0.0-codex.zip")

    print("PASS: brief-writing static validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
