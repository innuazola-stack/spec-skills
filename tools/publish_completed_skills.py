from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
INDEX = ROOT / "dist" / "skill-release-index.yaml"


@dataclass(frozen=True)
class SkillRelease:
    name: str
    version: str
    root: Path
    builder: Path


def manifest_value(manifest: Path, key: str) -> str | None:
    prefix = f"{key}:"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip()
    return None


def discover(selected: set[str] | None) -> list[SkillRelease]:
    releases: list[SkillRelease] = []
    for skill_root in sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir()):
        manifest = skill_root / "manifest.yaml"
        builder = skill_root / "tools" / "build_release.py"
        if not manifest.exists() or not builder.exists():
            continue
        name = manifest_value(manifest, "name")
        version = manifest_value(manifest, "version")
        if not name or not version:
            continue
        if selected and name not in selected:
            continue
        release_note = skill_root / "releases" / f"{version}.md"
        if not release_note.exists():
            raise FileNotFoundError(f"{name} missing release note: {release_note.relative_to(ROOT)}")
        releases.append(SkillRelease(name=name, version=version, root=skill_root, builder=builder))
    if selected:
        found = {release.name for release in releases}
        missing = sorted(selected - found)
        if missing:
            raise ValueError("unknown or unpublished skill selection: " + ", ".join(missing))
    return releases


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def zip_has_runtime_manifest(path: Path) -> bool:
    with zipfile.ZipFile(path) as archive:
        return "MANIFEST.runtime.yaml" in set(archive.namelist())


def kind_for_artifact(skill: SkillRelease, artifact: Path) -> str:
    suffix = artifact.stem.removeprefix(f"{skill.name}-{skill.version}-")
    return suffix or "unknown"


def build_skill(skill: SkillRelease, check: bool) -> list[dict[str, str]]:
    command = [sys.executable, str(skill.builder)]
    if check:
        command.append("--check")
    subprocess.run(command, cwd=skill.root, check=True)
    if check:
        return []

    artifacts: list[dict[str, str]] = []
    for artifact in sorted((skill.root / "dist").glob(f"{skill.name}-{skill.version}-*.zip")):
        kind = kind_for_artifact(skill, artifact)
        if kind != "source" and not zip_has_runtime_manifest(artifact):
            raise RuntimeError(f"runtime artifact missing MANIFEST.runtime.yaml: {artifact.relative_to(ROOT)}")
        artifacts.append(
            {
                "kind": kind,
                "path": artifact.relative_to(ROOT).as_posix(),
                "sha256": sha256(artifact),
            }
        )
    if not artifacts:
        raise RuntimeError(f"{skill.name} produced no zip artifacts")
    return artifacts


def write_index(results: list[tuple[SkillRelease, list[dict[str, str]]]]) -> None:
    INDEX.parent.mkdir(parents=True, exist_ok=True)
    lines = ["schema: skill-release-index/v1", "skills:"]
    for skill, artifacts in results:
        lines.extend(
            [
                f"  - name: {skill.name}",
                f"    version: {skill.version}",
                f"    manifest: {skill.root.relative_to(ROOT).as_posix()}/manifest.yaml",
                "    artifacts:",
            ]
        )
        for artifact in artifacts:
            lines.extend(
                [
                    f"      - kind: {artifact['kind']}",
                    f"        path: {artifact['path']}",
                    f"        sha256: {artifact['sha256']}",
                ]
            )
    INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build zip releases for completed skills.")
    parser.add_argument("--check", action="store_true", help="validate publishable skills without writing zip artifacts")
    parser.add_argument("--skills", nargs="*", help="optional skill names to publish")
    args = parser.parse_args()

    selected = set(args.skills) if args.skills else None
    skills = discover(selected)
    if not skills:
        raise SystemExit("no publishable skills found")

    results: list[tuple[SkillRelease, list[dict[str, str]]]] = []
    for skill in skills:
        artifacts = build_skill(skill, check=args.check)
        results.append((skill, artifacts))

    if args.check:
        print("PASS: skill release checks")
        for skill, _ in results:
            print(f"checked: {skill.name} {skill.version}")
        return 0

    write_index(results)
    print(f"PASS: published {len(results)} skills")
    print(INDEX.relative_to(ROOT).as_posix())
    for skill, artifacts in results:
        print(f"{skill.name} {skill.version}")
        for artifact in artifacts:
            print(f"  {artifact['kind']}: {artifact['path']} {artifact['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
