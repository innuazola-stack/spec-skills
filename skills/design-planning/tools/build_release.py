from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

ADAPTERS = {
    "codex": "system-prompt.md",
    "claude": "CLAUDE.md",
    "gemini": "GEMINI.md",
    "openclaw": "OPENCLAW.md",
    "hermas": "HERMAS.md",
}

SOURCE_INCLUDE_DIRS = ["adapters", "docs", "evals", "schemas", "skill", "tests", "tools", "validators"]
SOURCE_INCLUDE_FILES = ["SKILL.md", "agent.md", "manifest.yaml", "rules.md", "workflow.md"]


def version() -> str:
    manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
    match = re.search(r"^version:\s*(\S+)\s*$", manifest, re.MULTILINE)
    if not match:
        raise RuntimeError("manifest.yaml missing version")
    return match.group(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add_path(zf: zipfile.ZipFile, path: Path, base: Path) -> None:
    if path.is_dir():
        for child in sorted(path.rglob("*")):
            if child.is_file() and "__pycache__" not in child.parts and child.suffix != ".pyc":
                zf.write(child, child.relative_to(base))
    elif path.exists():
        zf.write(path, path.relative_to(base))


def validate() -> None:
    subprocess.run([sys.executable, str(ROOT / "validators" / "validate_harness.py")], check=True)


def build_source_zip(release_version: str) -> Path:
    DIST.mkdir(parents=True, exist_ok=True)
    out = DIST / f"design-planning-{release_version}-source.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in SOURCE_INCLUDE_FILES:
            add_path(zf, ROOT / rel, ROOT)
        for rel in SOURCE_INCLUDE_DIRS:
            add_path(zf, ROOT / rel, ROOT)
    return out


def build_runtime_zip(runtime: str, entry: str, release_version: str) -> Path:
    out = DIST / f"design-planning-{release_version}-{runtime}.zip"
    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp) / "design-planning"
        staging.mkdir(parents=True)
        for rel in ["SKILL.md", "agent.md", "manifest.yaml", "rules.md", "workflow.md"]:
            shutil.copy2(ROOT / rel, staging / rel)
        for rel in ["schemas", "validators", "evals"]:
            shutil.copytree(ROOT / rel, staging / rel)
        adapter_src = ROOT / "adapters" / runtime
        adapter_dst = staging / "adapter"
        shutil.copytree(adapter_src, adapter_dst)
        manifest = staging / "MANIFEST.runtime.yaml"
        manifest.write_text(
            "\n".join(
                [
                    "name: design-planning",
                    f"version: {release_version}",
                    f"runtime: {runtime}",
                    f"entry: adapter/{entry}",
                    "type: harness-workflow",
                    "planning_default: tasks/design",
                    "design_root: docs/design",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            for child in sorted(staging.rglob("*")):
                if child.is_file() and "__pycache__" not in child.parts and child.suffix != ".pyc":
                    zf.write(child, child.relative_to(staging))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate release inputs without writing dist artifacts")
    args = parser.parse_args()

    validate()
    if args.check:
        print("PASS: design-planning release check")
        return

    release_version = version()
    DIST.mkdir(parents=True, exist_ok=True)
    artifacts = [build_source_zip(release_version)]
    for runtime, entry in ADAPTERS.items():
        artifacts.append(build_runtime_zip(runtime, entry, release_version))

    lines = ["name: design-planning", f"version: {release_version}", "artifacts:"]
    for artifact in artifacts:
        rel = artifact.relative_to(ROOT).as_posix()
        lines.extend(
            [
                f"  - path: {rel}",
                f"    sha256: {sha256(artifact)}",
            ]
        )
    (DIST / "release-manifest.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS: design-planning release build")


if __name__ == "__main__":
    main()
