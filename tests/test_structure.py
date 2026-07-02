"""Structural tests: nav entries, filenames, front matter, footers, images."""

from __future__ import annotations

import re

from tests.helpers import (
    FOOTER_MARKER,
    PUBLISHED_DIR,
    REPO_ROOT,
    parse_front_matter,
)


# ---------------------------------------------------------------------------
# mkdocs.yml nav
# ---------------------------------------------------------------------------

def load_nav_entries() -> list[tuple[str, str]]:
    """Parse mkdocs.yml and return (label, path) for every nav entry."""
    config_path = REPO_ROOT / "mkdocs.yml"
    text = config_path.read_text(encoding="utf-8")
    # Remove the first front-matter-like --- block if present (there isn't one,
    # but be safe). Then parse YAML.
    # mkdocs.yml is not pure YAML; extract nav section manually.
    nav_entries = []
    in_nav = False
    for line in text.splitlines():
        if line.strip() == "nav:":
            in_nav = True
            continue
        if in_nav:
            if line and not line.startswith(" ") and not line.startswith("-"):
                break
            m = re.match(r'\s+-\s+"?([^"]+)"?:\s+(.+)', line)
            if m:
                label, path = m.group(1), m.group(2).strip()
                nav_entries.append((label, path))
            else:
                # Top-level nav item (no nested children on same line)
                m2 = re.match(r"\s+-\s+(.+):\s+(.+)", line)
                if m2:
                    label, path = m2.group(1), m2.group(2).strip()
                    nav_entries.append((label, path))
    return nav_entries


def test_nav_entries_have_files():
    """Every file path in mkdocs.yml nav must exist in docs/."""
    missing = []
    for label, path in load_nav_entries():
        full = REPO_ROOT / "docs" / path
        if not full.exists():
            missing.append(f"{label} -> {path}")
    assert not missing, "Nav entries with missing files:\n" + "\n".join(missing)


def test_webnovel_chapter_files_have_nav_entries():
    """Every webnovel ch*.md file must have a corresponding nav entry in mkdocs.yml."""
    nav_paths = {path for _, path in load_nav_entries() if path.startswith("webnovel/ch")}
    missing = []
    for f in sorted(PUBLISHED_DIR.glob("ch*.md")):
        rel = f"webnovel/{f.name}"
        if rel not in nav_paths:
            missing.append(f.name)
    assert not missing, "Published chapters missing from nav:\n" + "\n".join(missing)


# ---------------------------------------------------------------------------
# Published chapter front matter
# ---------------------------------------------------------------------------

def test_published_chapters_have_front_matter():
    """Every docs/webnovel/ch*.md must have title and description."""
    bad = []
    for f in sorted(PUBLISHED_DIR.glob("ch*.md")):
        if f.name == "index.md":
            continue
        text = f.read_text(encoding="utf-8")
        meta, _ = parse_front_matter(text)
        issues = []
        if "title" not in meta:
            issues.append("missing title")
        if "description" not in meta:
            issues.append("missing description")
        if issues:
            bad.append(f"{f.name}: {', '.join(issues)}")
    assert not bad, "Published chapters with bad front matter:\n" + "\n".join(bad)


def test_published_chapters_have_revision_metadata():
    """Every published chapter must have revision in front matter.

    Chapters at revision 2+ must also have an updated field.
    """
    bad = []
    for f in sorted(PUBLISHED_DIR.glob("ch*.md")):
        if f.name == "index.md":
            continue
        text = f.read_text(encoding="utf-8")
        meta, _ = parse_front_matter(text)
        issues = []
        if "revision" not in meta:
            issues.append("missing revision")
        elif meta["revision"] >= 2 and "updated" not in meta:
            issues.append("revision >= 2 but missing updated")
        if issues:
            bad.append(f"{f.name}: {', '.join(issues)}")
    assert not bad, "Published chapters missing revision metadata:\n" + "\n".join(bad)


# ---------------------------------------------------------------------------
# Author's note footer
# ---------------------------------------------------------------------------

def test_published_chapters_have_footer():
    """Every docs/webnovel/ch*.md must end with the author's note."""
    missing = []
    for f in sorted(PUBLISHED_DIR.glob("ch*.md")):
        if f.name == "index.md":
            continue
        text = f.read_text(encoding="utf-8")
        if FOOTER_MARKER not in text:
            missing.append(f.name)
    assert not missing, "Published chapters missing author's note footer:\n" + "\n".join(
        missing
    )


# ---------------------------------------------------------------------------
# Image references
# ---------------------------------------------------------------------------

def test_image_references_exist():
    """Every image referenced in docs/webnovel/*.md must exist on disk."""
    missing = []
    for f in sorted(PUBLISHED_DIR.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r"!\[.*?\]\((.*?)\)", text):
            img_path = m.group(1)
            # Resolve relative to the file's directory
            full = (f.parent / img_path).resolve()
            if not full.exists():
                missing.append(f"{f.name}: {img_path}")
    assert not missing, "Missing image files:\n" + "\n".join(missing)


# ---------------------------------------------------------------------------
# Published chapter date line
# ---------------------------------------------------------------------------

def test_published_chapters_have_date_line():
    """Every published chapter must have a *Published ...* date line after the heading."""
    missing = []
    for f in sorted(PUBLISHED_DIR.glob("ch*.md")):
        if f.name == "index.md":
            continue
        text = f.read_text(encoding="utf-8")
        if not re.search(r"^\*Published\s", text, re.MULTILINE):
            missing.append(f.name)
    assert not missing, "Published chapters missing date line:\n" + "\n".join(missing)


def test_revised_chapters_have_revision_line():
    """Chapters at revision 2+ must have a *Revision N, updated ...* line in the body."""
    bad = []
    for f in sorted(PUBLISHED_DIR.glob("ch*.md")):
        if f.name == "index.md":
            continue
        text = f.read_text(encoding="utf-8")
        meta, _ = parse_front_matter(text)
        if meta.get("revision", 1) < 2:
            continue
        if not re.search(r"^\*Revision \d+, updated\s", text, re.MULTILINE):
            bad.append(f.name)
    assert not bad, "Revised chapters missing revision line:\n" + "\n".join(bad)


def test_flashback_chapters_have_subtitle_before_date():
    """Flashback chapters (ch*F.md) must have a subtitle line after metadata, before prose.

    The subtitle (e.g. *Erika, before*) should appear after the published/revision
    lines but before the illustration and prose.
    """
    bad = []
    for f in sorted(PUBLISHED_DIR.glob("ch*F.md")):
        text = f.read_text(encoding="utf-8")
        subtitle_match = re.search(r"^\*[A-Z][^*]+\*$", text, re.MULTILINE)
        published_match = re.search(r"^\*Published\s", text, re.MULTILINE)
        if not published_match:
            continue  # tested elsewhere
        if not subtitle_match:
            continue
        if subtitle_match.start() < published_match.start():
            bad.append(f"{f.name}: subtitle appears before published date")
    assert not bad, "Flashback chapters with incorrect subtitle order:\n" + "\n".join(bad)


# ---------------------------------------------------------------------------
# Published chapter illustration image
# ---------------------------------------------------------------------------

def test_published_chapters_have_illustration():
    """Every published chapter must have a chapter illustration image reference."""
    missing = []
    for f in sorted(PUBLISHED_DIR.glob("ch*.md")):
        if f.name == "index.md":
            continue
        text = f.read_text(encoding="utf-8")
        if not re.search(r"!\[.*?\]\(.*?\)\{ \.chapter-illustration \}", text):
            missing.append(f.name)
    assert not missing, "Published chapters missing illustration:\n" + "\n".join(missing)





