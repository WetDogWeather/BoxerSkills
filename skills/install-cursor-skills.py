#!/usr/bin/env python3
"""Install Boxer markdown skills into .cursor/skills/ (macOS, Linux, Windows)."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

SKILLS = ("boxer-geoservice", "boxer-wcs")


def skills_dir() -> Path:
    return Path(__file__).resolve().parent


def repo_root() -> Path:
    return skills_dir().parent


def install_skill(src_root: Path, dst_root: Path, name: str) -> None:
    src = src_root / name
    dst = dst_root / name
    if not src.is_dir():
        raise SystemExit(f"Missing skill directory: {src}")
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    for md in src.glob("*.md"):
        shutil.copy2(md, dst / md.name)
    scripts = src / "scripts"
    if scripts.is_dir():
        shutil.copytree(scripts, dst / "scripts")
    print(f"  {dst}")
    for item in sorted(dst.iterdir()):
        print(f"    {item.name}")


def main() -> int:
    personal = "--personal" in sys.argv
    root = repo_root()
    src = skills_dir()
    dst = (
        Path.home() / ".cursor" / "skills"
        if personal
        else root / ".cursor" / "skills"
    )
    dst.mkdir(parents=True, exist_ok=True)

    for name in SKILLS:
        install_skill(src, dst, name)

    shared = src / "_shared"
    if shared.is_dir():
        dest_shared = dst / "_shared"
        if dest_shared.exists():
            shutil.rmtree(dest_shared)
        shutil.copytree(shared, dest_shared)
        print(f"  {dest_shared}")

    print("Reload Cursor to pick up the skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
