"""D-MIS-01 — missing number finder (Report/09 §6.1). Domain Mock 금지."""

from __future__ import annotations

from magicsquare.entity.resolver.missing_number_finder import find_not_exist_nums
from magicsquare.entity.value_objects import MissingPair

from tests.entity.grid_fixtures import GRID_G1


class TestDMis01MissingNumberFinder:
    """D-MIS-01 — G1 missing numbers ascending."""

    def test_d_mis_01_g1_missing_seven_and_ten_sorted(self) -> None:
        # Given: G1 grid
        grid = GRID_G1

        # When: find_not_exist_nums is invoked
        result = find_not_exist_nums(grid)

        # Then: {7, 10} with smaller=7, larger=10
        assert isinstance(result, MissingPair)
        assert result.as_sorted_set() == {7, 10}
        assert result.smaller == 7
        assert result.larger == 10
