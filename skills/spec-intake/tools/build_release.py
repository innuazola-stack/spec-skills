#!/usr/bin/env python3
"""Build release zips for the spec-intake harness."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


SOURCE_FILES = [
    "manifest.yaml",
    "agent.md",
    "workflow.md",
    "rules.md",
]
SOURCE_DIRS = [
    "schemas",
    "validators",
    "evals",
    "adapters",
    "skill",
    "docs",
    "tests",
    "tools",
    "releases",
]
RUNTIME_DIRS = [
    "schemas",
    "validators",
    "evals",
    "adapters/codex",
    "skill",
]
REQUIRED_RUNTIME_FILES = [
    "manifest.yaml",
    "agent.md",
    "workflow.md",
    "rules.md",
    "schemas/contract-envelope.schema.md",
    "validators/validate_harness.py",
    "evals/cases/meeting-action-positive.md",
    "evals/cases/customer-data-negative.md",
    "evals/cases/one-line-draft-boundary.md",
    "adapters/codex/SKILL.md",
    "adapters/codex/mapping.md",
    "adapters/codex/install.md",
    "skill/SKILL.md",
    "skill/references/prd-quality-reference.md",
    "MANIFEST.runtime.yaml",
]


def read_version(root: Path) -> str:
    for line in (root / "manifest.yaml").read_text(encoding="utf-8").splitlines():
        if line.startswith("version:"):
            return line.split(":", 1)[1].strip()
    raise ValueError("manifest.yaml missing version")


def run_source_validation(root: Path) -> None:
    validator = root / "validators" / "validate_harness.py"
    result = subprocess.run([sys.executable, str(validator), str(root)], text=True, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def copy_tree_items(root: Path, staging: Path, files: list[str], dirs: list[str]) -> None:
    for item in files:
        src = root / item
        dst = staging / item
        if not src.exists():
            raise FileNotFoundError(item)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    for item in dirs:
        src = root / item
        if not src.exists():
            continue
        dst = staging / item
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".tmp-*", "__pycache__", "*.pyc"))


def write_runtime_manifest(staging: Path, version: str) -> None:
    (staging / "MANIFEST.runtime.yaml").write_text(
        "\n".join([
            "name: spec-intake",
            f"version: {version}",
            "runtime: codex",
            "entry: skill/SKILL.md",
            "source_adapter: adapters/codex/SKILL.md",
            "",
        ]),
        encoding="utf-8",
    )


def validate_runtime_staging(staging: Path) -> None:
    missing = [item for item in REQUIRED_RUNTIME_FILES if not (staging / item).exists()]
    if missing:
        raise FileNotFoundError("runtime staging missing: " + ", ".join(missing))


def zip_dir(source: Path, output: Path) -> str:
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source).as_posix())
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    return digest


def validate_zip(output: Path, required_files: list[str]) -> None:
    with zipfile.ZipFile(output) as archive:
        names = set(archive.namelist())
    missing = [item for item in required_files if item not in names]
    if missing:
        raise FileNotFoundError(f"{output.name} missing: " + ", ".join(missing))


def write_release_manifest(dist: Path, artifacts: list[dict[str, str]]) -> None:
    lines = ["name: spec-intake", "artifacts:"]
    for artifact in artifacts:
        lines.extend([
            f"  - kind: {artifact['kind']}",
            f"    path: {artifact['path']}",
            f"    sha256: {artifact['sha256']}",
        ])
    (dist / "release-manifest.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) == 2 else Path(__file__).resolve().parents[1]
    version = read_version(root)
    run_source_validation(root)

    dist = root / "dist"
    staging_root = dist / ".staging"
    shutil.rmtree(staging_root, ignore_errors=True)
    staging_root.mkdir(parents=True, exist_ok=True)

    source_stage = staging_root / "source"
    runtime_stage = staging_root / "codex"
    source_stage.mkdir(parents=True)
    runtime_stage.mkdir(parents=True)

    copy_tree_items(root, source_stage, SOURCE_FILES, SOURCE_DIRS)
    copy_tree_items(root, runtime_stage, SOURCE_FILES, RUNTIME_DIRS)
    write_runtime_manifest(runtime_stage, version)
    validate_runtime_staging(runtime_stage)

    source_zip = dist / f"spec-intake-{version}-source.zip"
    runtime_zip = dist / f"spec-intake-{version}-codex.zip"
    source_hash = zip_dir(source_stage, source_zip)
    runtime_hash = zip_dir(runtime_stage, runtime_zip)
    validate_zip(source_zip, SOURCE_FILES + ["tools/build_release.py"])
    validate_zip(runtime_zip, REQUIRED_RUNTIME_FILES)

    artifacts = [
        {"kind": "source", "path": source_zip.relative_to(root).as_posix(), "sha256": source_hash},
        {"kind": "codex", "path": runtime_zip.relative_to(root).as_posix(), "sha256": runtime_hash},
    ]
    write_release_manifest(dist, artifacts)
    shutil.rmtree(staging_root, ignore_errors=True)
    print(json.dumps({"ok": True, "artifacts": artifacts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
