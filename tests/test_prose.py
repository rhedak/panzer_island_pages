"""Prose quality tests: word count and banned punctuation."""

from __future__ import annotations

import re
from pathlib import Path

from tests.helpers import (
    BANNED_PUNCTUATION_RE,
    PUBLISHED_DIR,
    WEBNOVEL_DIR,
    published_filename_to_draft,
    strip_structural_elements,
    word_count,
)

MIN_WORDS = 1800
MAX_WORDS = 3500


def get_draft_chapters() -> list[Path]:
    """Get all non-notes draft chapter files."""
    return sorted(
        f for f in WEBNOVEL_DIR.glob("ch*.md") if "_notes" not in f.name
    )


def test_draft_word_count_in_range():
    """Each draft chapter should be between MIN_WORDS and MAX_WORDS."""
    violations = []
    for f in get_draft_chapters():
        text = f.read_text(encoding="utf-8")
        wc = word_count(text)
        if wc < MIN_WORDS:
            violations.append(f"{f.name}: {wc} words (minimum {MIN_WORDS})")
        elif wc > MAX_WORDS:
            violations.append(f"{f.name}: {wc} words (maximum {MAX_WORDS})")
    assert not violations, "Word count violations:\n" + "\n".join(violations)


def test_draft_no_banned_punctuation():
    """Draft chapters must not contain em dashes or double hyphens in prose."""
    violations = []
    for f in get_draft_chapters():
        text = f.read_text(encoding="utf-8")
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # Skip markdown horizontal rules
            if stripped == "---":
                continue
            if BANNED_PUNCTUATION_RE.search(stripped):
                violations.append(f"{f.name}:{i}: {stripped[:80]}")
    assert not violations, "Banned punctuation found in drafts:\n" + "\n".join(violations)


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
