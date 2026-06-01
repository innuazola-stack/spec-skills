#!/usr/bin/env python3
"""Validate the spec-intake harness source package."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) == 2 else Path(__file__).resolve().parents[1]
    validator = root / "skill" / "scripts" / "validate_skill_package.py"
    skill_dir = root / "skill"
    return subprocess.run([sys.executable, str(validator), str(skill_dir)], check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
