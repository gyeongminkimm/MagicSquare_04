"""FR-01 structural validation — 4×4 grid dimension."""

from __future__ import annotations

from typing import Any

from magicsquare.boundary.constants import GRID_DIMENSION


class BoundaryValidator:
    """Validates puzzle grid structure before Domain resolution."""

    @staticmethod
    def is_valid_dimension(grid: Any) -> bool:
        """Return True only when grid is a 4×4 list of lists."""
        if grid is None:
            return False
        if not isinstance(grid, list):
            return False
        if len(grid) != GRID_DIMENSION:
            return False
        for row in grid:
            if not isinstance(row, list):
                return False
            if len(row) != GRID_DIMENSION:
                return False
        return True
