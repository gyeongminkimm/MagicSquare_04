"""Resolve missing numbers from partial grid (FR-03)."""

from __future__ import annotations

from magicsquare.entity.value_objects import (
    BLANK_CELL_VALUE,
    CELL_VALUE_MAX,
    CELL_VALUE_MIN,
)
from magicsquare.entity.value_objects.missing_pair import MissingPair


def find_not_exist_nums(grid: list[list[int]]) -> MissingPair:
    """Return the two missing values from {CELL_VALUE_MIN..CELL_VALUE_MAX}.

    Args:
        grid: 4×4 puzzle grid with non-blank values present.

    Returns:
        MissingPair with smaller-first ordering.
    """
    present = {
        value
        for row in grid
        for value in row
        if value != BLANK_CELL_VALUE
    }
    full_set = set(range(CELL_VALUE_MIN, CELL_VALUE_MAX + 1))
    missing = sorted(full_set - present)
    return MissingPair(smaller=missing[0], larger=missing[1])
