"""Shared helpers for panzer_island_pages tests."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
PUBLISHED_DIR = DOCS_DIR / "webnovel"

FOOTER_MARKER = "Author's note: Panzer Island is also a strategy game"
BANNED_PUNCTUATION_RE = re.compile(r"[\u2014]|(?<!\w)--(?!\w)")


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Parse YAML front matter from a Markdown file.

    Returns (metadata_dict, body_without_front_matter).
    """
    if not text.startswith("---"):
        return {}, text
    # Find the closing ---
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    fm_yaml = text[3:end].strip()
    body = text[end + 3:].lstrip("\n")
    try:
        meta = yaml.safe_load(fm_yaml) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, body


def strip_structural_elements(text: str) -> str:
    """Strip front matter, heading, date line, image refs, navigation, and footer from text.

    Returns only the prose body for comparison.
    """
    lines = text.split("\n")
    out = []
    in_front_matter = False

    for line in lines:
        stripped = line.strip()

        # Track YAML front matter boundaries
        if stripped == "---":
            in_front_matter = not in_front_matter
            continue

        # Skip everything inside front matter
        if in_front_matter:
            continue

        # Skip heading lines (# ...)
        if stripped.startswith("# ") and not stripped.startswith("## "):
            continue

        # Skip date line (*Published ...*)
        if re.match(r"^\*Published\s", stripped):
            continue

        # Skip revision line (*Revision N, updated ...*)
        if re.match(r"^\*Revision \d+", stripped):
            continue

        # Skip image references (![...](...))
        if re.match(r"^!\[.*\]\(.*\)", stripped):
            continue

        # Skip navigation links ([Previous Chapter: ...] | [Next Chapter: ...])
        if re.match(r"^\[Previous Chapter:.*\]\(.*\.md\)", stripped):
            continue

        # Skip footer (everything from "Author's note:" onward)
        if FOOTER_MARKER in stripped:
            break

        # Skip "Arc X..." lines after footer
        if re.match(r"^\*Arc \d+", stripped):
            break

        out.append(line)

    # Collapse multiple blank lines into single
    result = "\n".join(out)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()

