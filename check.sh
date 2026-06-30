#!/bin/bash
# Run basic site validation. Mirrors the role of check.sh in the sister repo.
set -euo pipefail

echo "=== panzer_island_pages check ==="

if ! command -v uv &>/dev/null; then
    echo "ERROR: uv not found. Install from https://docs.astral.sh/uv/"
    exit 1
fi

echo "Checking asset sync..."
if ! uv run python sync_assets.py; then
    echo "  (assets out of sync -- run: uv run python sync_assets.py --sync)"
fi

echo "Checking punctuation (em dashes, double hyphens)..."
if ! bash check_punctuation.sh docs/webnovel; then
    echo "  (banned punctuation found in prose text)"
    exit 1
fi

echo "Building MkDocs site..."
uv run mkdocs build --strict 2>&1

echo "=== OK ==="
