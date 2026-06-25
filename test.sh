#!/bin/bash
# Run the full test suite. Heavier than check.sh; run before pushing changes live.
# Usage: ./test.sh
set -euo pipefail

echo "=== panzer_island_pages test suite ==="

if ! command -v uv &>/dev/null; then
    echo "ERROR: uv not found. Install from https://docs.astral.sh/uv/"
    exit 1
fi

echo ""
echo "Running pytest..."
uv run pytest tests/ -v --tb=short 2>&1

echo ""
echo "=== ALL TESTS PASSED ==="
