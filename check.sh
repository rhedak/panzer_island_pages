#!/bin/bash
# Run basic site validation. Mirrors the role of check.sh in the sister repo.
set -euo pipefail

echo "=== panzer_island_pages check ==="

if ! command -v uv &>/dev/null; then
    echo "ERROR: uv not found. Install from https://docs.astral.sh/uv/"
    exit 1
fi

echo "Checking asset sync..."
uv run python sync_assets.py

echo "Building MkDocs site..."
uv run mkdocs build --strict 2>&1

echo "=== OK ==="
