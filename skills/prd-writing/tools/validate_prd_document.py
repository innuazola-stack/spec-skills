from __future__ import annotations

import re
import sys
from pathlib import Path


try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REQUIRED_SECTIONS = [
    "修订记录",
    "文档摘要",
    "背景与问题",
    "目标与成功指标",
    "用户与使用场景",
    "范围定义",
    "用户旅程",
    "功能需求",
    "非功能需求",
    "数据",
    "验收标准",
    "发布",
    "依赖",
    "需求追踪矩阵",
    "参考文献",
]

PROCESS_TERMS = [
    "我会",
    "接下来",
    "下一步",
    "TODO",
    "TBD",
    "待补充",
    "待完善",
    "草稿",
    "本文将",
    "写作过程",
    "调研过程",
]

UNCERTAINTY_WORDS = ["假设", "开放问题", "风险", "阻塞", "依赖", "未知", "待确认"]
PLACEHOLDER_PATTERNS = [
    r"<产品",
    r"<功能",
    r"<作者",
    r"<来源",
    r"<需求",
    r"<目标",
    r"<指标",
    r"<角色",
    r"<场景",
    r"<日期",
    r"<URL",
    r"<前置条件",
    r"<动作",
    r"<可观察结果",
    r"<说明",
    r"<内容",
    r"<名称",
]
SOURCE_RE = re.compile(r"\[(S\d{2}|M\d{2}|BIZ-\d{2}|USER-\d{2}|DATA-\d{2}|DESIGN-\d{2}|TECH-\d{2}|LEGAL-\d{2}|SOURCE-ID)\]")
MARKER_RE = re.compile(r"\[(S\d{2}|M\d{2}|BIZ-\d{2}|USER-\d{2}|DATA-\d{2}|DESIGN-\d{2}|TECH-\d{2}|LEGAL-\d{2})\]")


def fail(errors: list[str]) -> None:
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)


def section_text(text: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}.*?$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return ""
    next_match = re.search(r"^##\s+", text[match.end() :], re.MULTILINE)
    end = match.end() + next_match.start() if next_match else len(text)
    return text[match.end() : end]


def table_rows(section: str) -> list[str]:
    rows = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if re.fullmatch(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?", stripped):
            continue
        if "---" in stripped and set(stripped.replace("|", "").replace(" ", "")) <= {"-", ":"}:
            continue
        rows.append(stripped)
    return rows


def row_has_marker_or_uncertainty(row: str) -> bool:
    return bool(SOURCE_RE.search(row)) or any(word in row for word in UNCERTAINTY_WORDS)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: validate_prd_document.py <prd.md>")
        sys.exit(2)

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []

    first_visible = next((line.strip() for line in lines if line.strip()), "")
    if first_visible != "## 修订记录":
        errors.append("first visible line must be exactly '## 修订记录'")

    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in text and not any(line.startswith("## ") and section in line for line in lines):
            errors.append(f"missing required section containing: {section}")

    for term in PROCESS_TERMS:
        if term in text:
            errors.append(f"contains process/placeholder term: {term}")

    placeholder_like = [
        line
        for line in lines
        if any(re.search(pattern, line) for pattern in PLACEHOLDER_PATTERNS)
    ]
    if placeholder_like:
        errors.append("contains unresolved template placeholder text")

    body, sep, refs = text.partition("## 参考文献")
    if not sep:
        errors.append("missing final references section")
        refs = ""

    body_markers = set(MARKER_RE.findall(body))
    ref_markers = set(MARKER_RE.findall(refs))
    missing_from_refs = sorted(body_markers - ref_markers)
    unused_refs = sorted(ref_markers - body_markers)
    if missing_from_refs:
        errors.append(f"body markers missing from references: {', '.join(missing_from_refs)}")
    if unused_refs:
        errors.append(f"references listed but not cited in body: {', '.join(unused_refs)}")

    body_methodology = sorted(marker for marker in body_markers if marker.startswith("M"))
    listed_methodology = sorted(marker for marker in ref_markers if marker.startswith("M"))
    if listed_methodology and not body_methodology:
        errors.append("methodology references are listed but not cited in the body")

    for line_no, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        next_line = lines[line_no].strip() if line_no < len(lines) else ""
        if next_line.startswith("|") and "---" in next_line and set(next_line.replace("|", "").replace(" ", "")) <= {"-", ":"}:
            continue
        if line_no <= 4:
            continue
        if "---" in stripped and set(stripped.replace("|", "").replace(" ", "")) <= {"-", ":"}:
            continue
        if any(header in stripped for header in ["版本 | 日期", "项目 | 内容", "ID |", "来源ID |"]):
            continue
        if "参考文献" in "\n".join(lines[max(0, line_no - 5) : line_no]):
            continue
        if not row_has_marker_or_uncertainty(stripped):
            errors.append(f"table row lacks source marker or uncertainty label at line {line_no}: {stripped[:120]}")

    requirements = section_text(text, "功能需求")
    for row in table_rows(requirements):
        if not re.search(r"\|\s*FR-\d{3}\s*\|", row):
            continue
        if not re.search(r"\|\s*P[0-3]\s*\|", row):
            errors.append(f"requirement row lacks P0-P3 priority: {row[:120]}")
        if not MARKER_RE.search(row):
            errors.append(f"requirement row lacks source marker: {row[:120]}")
        if not re.search(r"AC-\d{3}", row):
            errors.append(f"requirement row lacks acceptance link: {row[:120]}")

    acceptance = section_text(text, "验收标准")
    for row in table_rows(acceptance):
        if not re.search(r"\|\s*AC-\d{3}\s*\|", row):
            continue
        if not re.search(r"\b(Given|When|Then|必须|不得|通过|失败|拒绝|记录|检查)\b", row):
            errors.append(f"acceptance row is not clearly verifiable: {row[:120]}")
        if not MARKER_RE.search(row):
            errors.append(f"acceptance row lacks source marker: {row[:120]}")

    if "```mermaid" not in text:
        errors.append("missing Mermaid diagram for flow/state/dependency clarity")
    if "```latex" not in text:
        errors.append("missing LaTeX metric/formula block")

    if errors:
        fail(errors)

    print(f"PASS: PRD document validation ({path})")


if __name__ == "__main__":
    main()
