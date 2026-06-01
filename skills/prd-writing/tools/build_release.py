from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

SOURCE_FILES = ["manifest.yaml", "agent.md", "workflow.md", "rules.md"]
SOURCE_DIRS = ["adapters", "docs", "releases", "skill", "tools"]
RUNTIME_FILES = ["manifest.yaml", "agent.md", "workflow.md", "rules.md"]
RUNTIME_DIRS = ["adapters/codex", "skill", "tools"]
RUNTIME_REQUIRED = [
    "manifest.yaml",
    "agent.md",
    "workflow.md",
    "rules.md",
    "adapters/codex/SKILL.md",
    "skill/SKILL.md",
    "skill/references/prd-methodology.md",
    "skill/references/prd-output-contract.md",
    "skill/assets/PRD.template.md",
    "tools/validate_prd_document.py",
    "MANIFEST.runtime.yaml",
]


def read_version() -> str:
    for line in (ROOT / "manifest.yaml").read_text(encoding="utf-8").splitlines():
        if line.startswith("version:"):
            return line.split(":", 1)[1].strip()
    raise RuntimeError("manifest.yaml missing version")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def copy_items(staging: Path, files: list[str], dirs: list[str]) -> None:
    for rel in files:
        src = ROOT / rel
        if not src.exists():
            raise FileNotFoundError(rel)
        dst = staging / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    for rel in dirs:
        src = ROOT / rel
        if not src.exists():
            continue
        dst = staging / rel
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".staging"))


def zip_dir(source: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for child in sorted(source.rglob("*")):
            if child.is_file() and "__pycache__" not in child.parts and child.suffix != ".pyc":
                archive.write(child, child.relative_to(source).as_posix())


def validate_zip(path: Path, required: list[str]) -> None:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
    missing = [item for item in required if item not in names]
    if missing:
        raise FileNotFoundError(f"{path.name} missing: " + ", ".join(missing))


def run_validation() -> None:
    subprocess.run([sys.executable, str(ROOT / "tools" / "validate_skill_static.py")], check=True)


def build() -> list[dict[str, str]]:
    version = read_version()
    staging_root = DIST / ".staging"
    shutil.rmtree(staging_root, ignore_errors=True)
    source_stage = staging_root / "source"
    runtime_stage = staging_root / "codex"
    source_stage.mkdir(parents=True, exist_ok=True)
    runtime_stage.mkdir(parents=True, exist_ok=True)

    copy_items(source_stage, SOURCE_FILES, SOURCE_DIRS)
    copy_items(runtime_stage, RUNTIME_FILES, RUNTIME_DIRS)
    (runtime_stage / "MANIFEST.runtime.yaml").write_text(
        "\n".join(
            [
                "name: prd-writing",
                f"version: {version}",
                "runtime: codex",
                "entry: skill/SKILL.md",
                "source_adapter: adapters/codex/SKILL.md",
                "",
            ]
        ),
        encoding="utf-8",
    )

    source_zip = DIST / f"prd-writing-{version}-source.zip"
    runtime_zip = DIST / f"prd-writing-{version}-codex.zip"
    zip_dir(source_stage, source_zip)
    zip_dir(runtime_stage, runtime_zip)
    validate_zip(source_zip, SOURCE_FILES + ["tools/build_release.py", "tools/validate_prd_document.py"])
    validate_zip(runtime_zip, RUNTIME_REQUIRED)

    artifacts = [
        {"kind": "source", "path": source_zip.relative_to(ROOT).as_posix(), "sha256": sha256(source_zip)},
        {"kind": "codex", "path": runtime_zip.relative_to(ROOT).as_posix(), "sha256": sha256(runtime_zip)},
    ]
    lines = ["name: prd-writing", f"version: {version}", "artifacts:"]
    for artifact in artifacts:
        lines.extend(
            [
                f"  - kind: {artifact['kind']}",
                f"    path: {artifact['path']}",
                f"    sha256: {artifact['sha256']}",
            ]
        )
    (DIST / "release-manifest.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    shutil.rmtree(staging_root, ignore_errors=True)
    return artifacts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate release inputs without writing artifacts")
    args = parser.parse_args()

    run_validation()
    if args.check:
        print("PASS: prd-writing release check")
        return 0
    artifacts = build()
    print("PASS: prd-writing release build")
    for artifact in artifacts:
        print(f"{artifact['kind']}: {artifact['path']} {artifact['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
