"""Track A RED skeleton — U-OUT-01~03 output contract (Report/09 §5.1)."""

from __future__ import annotations

import pytest


class TestUOut01LengthSix:
    """U-OUT-01 — success payload length == 6."""

    def test_u_out_01_solve_success_returns_length_six(
        self,
    ) -> None:
        # Given: G2 valid grid; mock_resolver.resolve → [1,2,3,2,3,11]
        # mock_resolver = MagicMock(spec=SolveTwoBlankPuzzle)
        # boundary = MagicSquareBoundary(resolver=mock_resolver)

        # When: MagicSquareBoundary.solve(grid)

        # Then: len(result) == 6
        pytest.fail(
            "RED: U-OUT-01 — G2 mock success → int[6] length 6 (FR-05 AC-18, UI-OUT-01)"
        )


class TestUOut02OneIndexedCoords:
    """U-OUT-02 — r,c ∈ [1,4] 1-index."""

    def test_u_out_02_solve_success_coordinates_one_indexed(self) -> None:
        # Given: G1 grid; mock resolve → [2,2,7,3,3,10]
        # boundary = MagicSquareBoundary(resolver=mock_resolver)

        # When: MagicSquareBoundary.solve(grid)

        # Then: r1,c1,r2,c2 each in 1..4
        pytest.fail(
            "RED: U-OUT-02 — G1 mock → coords 1-index [1,4] (FR-05 AC-19, UI-OUT-02)"
        )


class TestUOut03MissingNumbersDistinct:
    """U-OUT-03 — n1,n2 are distinct missing numbers in [1,16]."""

    def test_u_out_03_solve_success_n1_n2_distinct_in_range(self) -> None:
        # Given: G1; mock [2,2,7,3,3,10]
        # When: solve(grid)
        # Then: n1,n2 ∈ [1,16], n1 != n2 (UI-OUT-03, BR-13)
        pytest.fail(
            "RED: U-OUT-03 — n1,n2 distinct missing values 1..16 (UI-OUT-03, FR-05)"
        )
