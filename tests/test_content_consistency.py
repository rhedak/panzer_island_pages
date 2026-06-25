"""Tests that published webnovel pages match their draft counterparts."""

from __future__ import annotations

from pathlib import Path

from tests.helpers import (
    PUBLISHED_DIR,
    WEBNOVEL_DIR,
    parse_front_matter,
    published_filename_to_draft,
    strip_structural_elements,
)


def get_published_chapters() -> list[Path]:
    """Get all published chapter files (ch*.md but not index.md)."""
    return sorted(
        f
        for f in PUBLISHED_DIR.glob("ch*.md")
        if f.name != "index.md"
    )


def test_all_published_have_matching_draft():
    """Every published chapter should have a corresponding draft file."""
    missing = []
    for pub in get_published_chapters():
        draft_name = published_filename_to_draft(pub.name)
        if draft_name is None:
            missing.append(f"{pub.name} (no draft pattern match)")
            continue
        draft_path = WEBNOVEL_DIR / draft_name
        if not draft_path.exists():
            missing.append(f"{pub.name} -> {draft_name} (draft not found)")
    assert not missing, "Published chapters without drafts:\n" + "\n".join(missing)


def test_draft_to_published_prose_consistency():
    """Prose body of each published page must match its draft.

    Compares after stripping front matter, headings, date lines, images,
    and footers from the published version.
    """
    mismatches = []
    for pub in get_published_chapters():
        draft_name = published_filename_to_draft(pub.name)
        if draft_name is None:
            continue
        draft_path = WEBNOVEL_DIR / draft_name
        if not draft_path.exists():
            continue

        pub_text = pub.read_text(encoding="utf-8")
        draft_text = draft_path.read_text(encoding="utf-8")

        pub_body = strip_structural_elements(pub_text)
        draft_body = strip_structural_elements(draft_text)

        if pub_body != draft_body:
            # Find first differing line
            pub_lines = pub_body.splitlines()
            draft_lines = draft_body.splitlines()
            diff_line = "unknown"
            for i, (p, d) in enumerate(zip(pub_lines, draft_lines)):
                if p != d:
                    diff_line = f"line ~{i + 1}"
                    break
            else:
                if len(pub_lines) != len(draft_lines):
                    diff_line = f"line count: published={len(pub_lines)} draft={len(draft_lines)}"

            mismatches.append(f"{pub.name}: differs at {diff_line}")

    assert not mismatches, "Prose mismatches between draft and published:\n" + "\n".join(
        mismatches
    )
