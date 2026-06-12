#!/usr/bin/env python3
"""
Check or sync assets from the sister repo into this repo.

Usage:
  uv run python sync_assets.py          # report status, exit 1 if anything is stale
  uv run python sync_assets.py --sync   # copy updated/missing files, then exit 0
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
import tomllib
from pathlib import Path

MANIFEST = Path(__file__).parent / "sync_manifest.toml"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def status(src: Path, dst: Path) -> str:
    if not dst.exists():
        return "missing"
    if sha256(src) != sha256(dst):
        return "outdated"
    return "ok"


def copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sync", action="store_true", help="Copy updated/missing files")
    args = parser.parse_args()

    manifest = tomllib.loads(MANIFEST.read_text())
    repo_root = MANIFEST.parent
    sister_root = (repo_root / manifest["repos"]["sister"]).resolve()

    if not sister_root.exists():
        print(f"Sister repo not found at {sister_root} — skipping.")
        return 0

    issues: list[str] = []

    def handle(src: Path, dst: Path, label: str) -> None:
        if not src.exists():
            print(f"  MISSING SRC  {label}")
            issues.append(label)
            return
        state = status(src, dst)
        if state == "ok":
            print(f"  ok           {label}")
            return
        print(f"  {state.upper():<12} {label}")
        issues.append(label)
        if args.sync:
            copy(src, dst)
            print(f"               synced")

    for entry in manifest.get("files", []):
        handle(
            sister_root / entry["src"],
            repo_root / entry["dst"],
            entry["dst"],
        )

    for entry in manifest.get("dirs", []):
        src_dir = sister_root / entry["src"]
        dst_dir = repo_root / entry["dst"]
        glob = entry.get("glob", "*")
        if not src_dir.exists():
            print(f"  MISSING SRC  {entry['src']}/")
            issues.append(entry["src"])
            continue
        for src_file in sorted(src_dir.glob(glob)):
            rel = src_file.relative_to(src_dir)
            handle(src_file, dst_dir / rel, f"{entry['dst']}/{rel}")

    if not issues:
        return 0

    if args.sync:
        print(f"\nSynced {len(issues)} file(s).")
        return 0

    print(f"\n{len(issues)} file(s) out of date. Run with --sync to update.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
