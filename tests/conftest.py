"""Shared fixtures for panzer_island_pages tests."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
WEBNOVEL_DIR = REPO_ROOT / "webnovel" / "chapters"
PUBLISHED_DIR = DOCS_DIR / "webnovel"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def docs_dir() -> Path:
    return DOCS_DIR


@pytest.fixture(scope="session")
def webnovel_dir() -> Path:
    return WEBNOVEL_DIR


@pytest.fixture(scope="session")
def published_dir() -> Path:
    return PUBLISHED_DIR
