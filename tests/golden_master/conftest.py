"""Golden Master pytest configuration."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from tests.golden_master.approval import DEFAULT_GOLDEN_PATH


def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "golden_master: Golden Master / Approval regression (GM-TC-*)",
    )


@pytest.fixture
def golden_master_expected_path() -> Path:
    """Path to the version-controlled Golden Master baseline file."""
    return DEFAULT_GOLDEN_PATH


@pytest.fixture
def golden_master_approve() -> bool:
    """True when GOLDEN_MASTER_APPROVE env requests baseline refresh."""
    return os.environ.get("GOLDEN_MASTER_APPROVE", "").lower() in {
        "1",
        "true",
        "yes",
    }
