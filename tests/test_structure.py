"""Structural tests: nav entries, filenames, front matter, footers, images."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from tests.helpers import (
    FOOTER_MARKER,
    PUBLISHED_DIR,
    REPO_ROOT,
    WEBNOVEL_DIR,
    parse_front_matter,
    published_filename_to_draft,
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
# Draft filename convention
# ---------------------------------------------------------------------------

def test_draft_filenames_follow_convention():
    """All draft chapter files must match ch[0-9]+[_name].md pattern."""
    bad = []
    for f in sorted(WEBNOVEL_DIR.glob("*.md")):
        if "_notes" in f.name:
            continue
        if not re.match(r"ch\d+[a-z]?_[a-z_]+\.md$", f.name):
            bad.append(f.name)
    assert not bad, "Draft files not matching convention:\n" + "\n".join(bad)


# ---------------------------------------------------------------------------
# Draft files should not have footers
# ---------------------------------------------------------------------------

def test_drafts_have_no_footer():
    """Draft chapter files should not contain the author's note footer."""
    has_footer = []
    for f in sorted(WEBNOVEL_DIR.glob("*.md")):
        if "_notes" in f.name:
            continue
        text = f.read_text(encoding="utf-8")
        if FOOTER_MARKER in text:
            has_footer.append(f.name)
    assert not has_footer, "Draft files with author's note footer (should be added at publish time):\n" + "\n".join(
        has_footer
    )


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


# ---------------------------------------------------------------------------
# Section divider count consistency (draft vs published)
# ---------------------------------------------------------------------------

def test_section_divider_count():
    """Published chapters must preserve draft's --- dividers plus 3 for front matter and footer.

    Drafts use --- as section dividers. Published versions add:
    - front matter opening ---
    - front matter closing ---
    - footer divider ---
    So published count should equal draft count + 3.
    """
    mismatches = []
    for pub in sorted(PUBLISHED_DIR.glob("ch*.md")):
        if pub.name == "index.md":
            continue
        draft_name = published_filename_to_draft(pub.name)
        if draft_name is None:
            continue
        draft_path = WEBNOVEL_DIR / draft_name
        if not draft_path.exists():
            continue

        pub_text = pub.read_text(encoding="utf-8")
        draft_text = draft_path.read_text(encoding="utf-8")

        pub_count = len(re.findall(r"^---$", pub_text, re.MULTILINE))
        draft_count = len(re.findall(r"^---$", draft_text, re.MULTILINE))

        expected = draft_count + 3
        if pub_count != expected:
            mismatches.append(
                f"{pub.name}: published={pub_count}, draft={draft_count}, expected={expected}"
            )
    assert not mismatches, "Section divider count mismatch:\n" + "\n".join(mismatches)
