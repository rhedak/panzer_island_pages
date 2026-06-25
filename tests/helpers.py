"""Shared helpers for panzer_island_pages tests."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
WEBNOVEL_DIR = REPO_ROOT / "webnovel" / "chapters"
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
    """Strip front matter, heading, date line, image refs, and footer from text.

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


def draft_filename_to_published(filename: str) -> str | None:
    """Map a draft chapter filename to its published counterpart.

    e.g. ch01_first_steps.md -> ch01.md
         ch02f_population.md -> ch02f.md
    """
    stem = Path(filename).stem
    # Extract ch number + optional letter suffix
    m = re.match(r"(ch\d+[a-z]?)_", stem)
    if m:
        return m.group(1) + ".md"
    return None


def published_filename_to_draft(filename: str) -> str | None:
    """Map a published chapter filename to its draft counterpart.

    e.g. ch01.md -> ch01_first_steps.md (looks up webnovel/chapters/)
    """
    stem = Path(filename).stem  # e.g. "ch01"
    if not re.match(r"ch\d+[a-z]?$", stem):
        return None
    # Find matching draft file
    for f in WEBNOVEL_DIR.glob(f"{stem}_*.md"):
        if "_notes" not in f.name:
            return f.name
    return None


def word_count(text: str) -> int:
    """Count words in prose text."""
    return len(text.split())
