"""Track B RED skeleton — D-MIS-01 (Report/09 §6.1). Domain Mock 금지."""

from __future__ import annotations

import pytest

from magicsquare.entity.resolver.missing_number_finder import find_not_exist_nums


class TestDMis01MissingNumbers:
    """D-MIS-01 — G1 missing numbers ascending."""

    def test_d_mis_01_g1_missing_seven_and_ten_sorted(self) -> None:
        # Given: G1 grid
        # When: find_not_exist_nums(grid)
        # Then: {7, 10} ascending
        pytest.fail(
            "RED: D-MIS-01 — G1 missing {7,10} ascending (I7, I11, FR-03, BR-06~07)"
        )
