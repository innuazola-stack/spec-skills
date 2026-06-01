# Skill Release Plan

## Release Boundary

A skill is publishable when its directory contains:

- `manifest.yaml` with `name` and `version`.
- `tools/build_release.py`.
- `releases/<version>.md`.
- Source/static validators that pass before packaging.
- A `dist/release-manifest.yaml` generated from the current build.

Directories without this boundary are treated as draft skills and are not packaged by the repository release command.

## Artifacts

Each publishable skill emits:

- `<skill>-<version>-source.zip`: full source package for review, migration, and future maintenance.
- `<skill>-<version>-<runtime>.zip`: runtime install package for a specific agent family, such as `codex`, `claude`, `gemini`, `openclaw`, or `hermas`.
- `dist/release-manifest.yaml`: per-skill artifact list with SHA-256 hashes.

The repository-level release command writes `dist/skill-release-index.yaml`, which records all packaged skills and their artifact hashes using paths relative to the repository root.

## Publish Command

Run from the repository root:

```bash
python tools/publish_completed_skills.py
```

To validate release inputs without writing zip artifacts:

```bash
python tools/publish_completed_skills.py --check
```

To publish a subset:

```bash
python tools/publish_completed_skills.py --skills brief-writing spec-intake
```

## Installation Guidance

Agents should install the runtime zip that matches their runtime. The `source` zip is for inspection and porting. Runtime packages include `MANIFEST.runtime.yaml` so an installer can find the entry file and runtime metadata without guessing.
