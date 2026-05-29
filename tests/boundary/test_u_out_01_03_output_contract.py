"""U-OUT-01~03 — success output contract (Report/09 §5.1)."""

from __future__ import annotations

import pytest

from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.boundary.ui_boundary import UIBoundary

from tests.entity.grid_fixtures import GRID_G1


class TestSuccessOutputContract:
    """U-OUT-01 — success envelope with int[6] data payload."""

    def test_u_out_01_success_returns_int_six_tuple(self) -> None:
        # Given: G1 valid puzzle grid (F2 / TD-02)
        grid = GRID_G1
        boundary = UIBoundary()

        # When: UIBoundary.solve is invoked (real Control resolve, no mock)
        result = boundary.solve(grid)

        # Then: OK envelope with F2 int[6] — Report/02 [2,2,10,3,3,7]
        assert isinstance(result, SuccessResponse)
        assert result.type == "OK"
        assert result.data == [2, 2, 10, 3, 3, 7]
        assert len(result.data) == 6
        payload = result.model_dump()
        assert "code" not in payload
        assert "message" not in payload


class TestUOut02OneIndexedCoords:
    """U-OUT-02 — r,c ∈ [1,4] 1-index."""

    def test_u_out_02_solve_success_coordinates_one_indexed(self) -> None:
        pytest.fail(
            "RED: U-OUT-02 — G1 → coords 1-index [1,4] (FR-05 AC-19, UI-OUT-02)"
        )


class TestUOut03MissingNumbersDistinct:
    """U-OUT-03 — n1,n2 distinct missing values in range."""

    def test_u_out_03_solve_success_n1_n2_distinct_in_range(self) -> None:
        pytest.fail(
            "RED: U-OUT-03 — n1,n2 distinct missing values 1..16 (UI-OUT-03, FR-05)"
        )
