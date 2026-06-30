"""Manual check: published webnovel chapters vs drafts in sister repo.

Run on demand as part of the publishing workflow:
    uv run python -m tests.content_consistency_check

Skips gracefully if the sister repo (../panzer_island_webnovel) is not present.
This is not auto-discovered by pytest (no test_ prefix).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Allow running as `python -m tests.content_consistency_check` from repo root
from tests.helpers import PUBLISHED_DIR, strip_structural_elements

SISTER_REPO = Path(__file__).resolve().parent.parent.parent / "panzer_island_webnovel"
DRAFT_DIR = SISTER_REPO / "chapters"


def _published_to_draft(stem: str) -> str | None:
    """Map a published chapter stem to its draft filename.

    e.g. 'ch01' -> 'ch01_first_steps.md'
         'ch02f' -> 'ch02f_population.md'
    """
    if not re.match(r"ch\d+[a-z]?$", stem):
        return None
    candidates = sorted(
        f
        for f in DRAFT_DIR.glob(f"{stem}_*.md")
        if "_notes" not in f.name
    )
    # Prefer the shortest stem (canonical file, no _old _v3 etc)
    canonical = [f for f in candidates if not re.search(r"_(old|v\d+)$", f.stem)]
    if canonical:
        return canonical[0].name
    if candidates:
        return candidates[0].name
    return None


def _check_all() -> int:
    """Run all checks, return number of failures (0 = ok)."""
    if not SISTER_REPO.is_dir():
        print(f"Sister repo not found at {SISTER_REPO}, skipping.")
        return 0

    failures = 0

    # Check 1: every published chapter has a matching draft
    for pub in sorted(PUBLISHED_DIR.glob("ch*.md")):
        if pub.name == "index.md":
            continue
        draft_name = _published_to_draft(pub.stem)
        if draft_name is None:
            print(f"FAIL  {pub.name}: no draft pattern match")
            failures += 1
            continue
        draft_path = DRAFT_DIR / draft_name
        if not draft_path.exists():
            print(f"FAIL  {pub.name}: draft not found ({draft_name})")
            failures += 1

    # Check 2: prose body matches (after stripping front matter, headings, etc.)
    for pub in sorted(PUBLISHED_DIR.glob("ch*.md")):
        if pub.name == "index.md":
            continue
        draft_name = _published_to_draft(pub.stem)
        if draft_name is None:
            continue
        draft_path = DRAFT_DIR / draft_name
        if not draft_path.exists():
            continue

        pub_text = pub.read_text(encoding="utf-8")
        draft_text = draft_path.read_text(encoding="utf-8")
        pub_body = strip_structural_elements(pub_text)
        draft_body = strip_structural_elements(draft_text)

        # Strip trailing whitespace on every line to ignore editorial padding
        pub_stripped = "\n".join(line.rstrip() for line in pub_body.splitlines())
        draft_stripped = "\n".join(line.rstrip() for line in draft_body.splitlines())
        if pub_stripped != draft_stripped:
            pub_lines = pub_stripped.splitlines()
            draft_lines = draft_stripped.splitlines()
            diff_line = "unknown"
            for i, (p, d) in enumerate(zip(pub_lines, draft_lines)):
                if p != d:
                    diff_line = f"line ~{i + 1}"
                    break
            else:
                if len(pub_lines) != len(draft_lines):
                    diff_line = f"line count: published={len(pub_lines)} draft={len(draft_lines)}"
            print(f"FAIL  {pub.name}: prose differs at {diff_line}")
            failures += 1

    if failures == 0:
        print("OK  all published chapters match their drafts.")
    return failures


if __name__ == "__main__":
    sys.exit(_check_all())
