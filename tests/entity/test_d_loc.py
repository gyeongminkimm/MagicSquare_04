"""Track B RED skeleton — D-LOC-01 (Report/09 §6.1). Domain Mock 금지."""

from __future__ import annotations

import pytest

from magicsquare.entity.locator.empty_cell_locator import find_blank_coords


class TestDLoc01BlankCoords:
    """D-LOC-01 — G1 row-major blank coordinates."""

    def test_d_loc_01_g1_row_major_blank_coords(self) -> None:
        # Given: G1 grid (F2 / TD-02)
        # grid = GRID_G1

        # When: find_blank_coords(grid)

        # Then: (2,2), (3,3) 1-index
        pytest.fail(
            "RED: D-LOC-01 — G1 row-major blanks (2,2) and (3,3) (I6, FR-02, BR-05)"
        )
