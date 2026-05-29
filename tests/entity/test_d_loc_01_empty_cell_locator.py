"""D-LOC-01 — empty cell locator (Report/09 §6.1). Domain Mock 금지."""

from __future__ import annotations

from magicsquare.entity.locator.empty_cell_locator import find_blank_coords
from magicsquare.entity.value_objects import CellPosition

from tests.entity.grid_fixtures import GRID_G1


class TestDLoc01EmptyCellLocator:
    """D-LOC-01 — G1 row-major blank coordinates."""

    def test_d_loc_01_g1_row_major_blank_coords(self) -> None:
        # Given: G1 grid (F2 / TD-02)
        grid = GRID_G1

        # When: find_blank_coords is invoked
        first, second = find_blank_coords(grid)

        # Then: (2,2), (3,3) 1-index row-major scan order
        assert first == CellPosition(row=2, col=2)
        assert second == CellPosition(row=3, col=3)
