"""Prose quality tests: banned punctuation in published chapters."""

from __future__ import annotations

import re
from pathlib import Path

from tests.helpers import (
    BANNED_PUNCTUATION_RE,
    PUBLISHED_DIR,
)


def test_published_no_banned_punctuation():
    """Published chapters must not contain em dashes or double hyphens in prose."""
    violations = []
    for f in sorted(PUBLISHED_DIR.glob("ch*.md")):
        if f.name == "index.md":
            continue
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()
        in_front_matter = False
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Track front matter boundaries
            if stripped == "---":
                in_front_matter = not in_front_matter
                continue
            if in_front_matter:
                continue
            # Skip markdown horizontal rules
            if stripped == "---":
                continue
            # Skip author's note block
            if "Author's note:" in stripped:
                break
            if BANNED_PUNCTUATION_RE.search(stripped):
                violations.append(f"{f.name}:{i}: {stripped[:80]}")
    assert not violations, "Banned punctuation found in published chapters:\n" + "\n".join(
        violations
    )
