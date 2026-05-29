"""Shared fixtures for AC-FR-01-01 Boundary RED tests."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from magicsquare.boundary.ui.magic_square_boundary import MagicSquareBoundary
from magicsquare.control.solve_two_blank_puzzle import SolveTwoBlankPuzzle

# AC-FR-01-01 contract constants (PRD §8.1 INVALID_SIZE)
INVALID_SIZE_CODE: str = "INVALID_SIZE"
INVALID_SIZE_MESSAGE: str = "Grid must be 4x4."

GRID_3X4: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

GRID_FOUR_EMPTY_ROWS: list[list[int]] = [[] for _ in range(4)]


@pytest.fixture
def mock_resolver() -> MagicMock:
    """Injected Domain resolver double (resolve() spy target)."""
    return MagicMock(spec=SolveTwoBlankPuzzle)


@pytest.fixture
def boundary(mock_resolver: MagicMock) -> MagicSquareBoundary:
    """Boundary SUT with mocked Domain resolver injected."""
    return MagicSquareBoundary(resolver=mock_resolver)


@pytest.fixture
def mock_resolve(mock_resolver: MagicMock) -> MagicMock:
    """Alias for resolve() on the injected resolver mock."""
    return mock_resolver.resolve


@pytest.fixture
def dimension_failure_grids() -> list[tuple[str, Any]]:
    """In-scope dimension failure inputs for parametrized cases."""
    return [
        ("none", None),
        ("empty_list", []),
        ("four_empty_rows", [[]] * 4),
        ("three_by_four", GRID_3X4),
        ("two_by_two", [[1, 2], [3, 4]]),
    ]
