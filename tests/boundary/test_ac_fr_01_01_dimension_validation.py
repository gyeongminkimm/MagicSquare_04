"""AC-FR-01-01 dimension validation RED tests for MagicSquareBoundary."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from magicsquare.boundary.schemas import FailureResult
from magicsquare.boundary.ui.magic_square_boundary import MagicSquareBoundary

from tests.boundary.conftest import (
    GRID_3X4,
    GRID_FOUR_EMPTY_ROWS,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
)

_MODULE_PATH = Path(__file__)
_F1_GRID_SNIPPET = "".join(["[16,", "0,2,13]"])
_F2_GRID_SNIPPET = "".join(["[16,", "3,2,13]"])
_FORBIDDEN_ERROR_CODES = (
    "ERR_" + "BLANK_COUNT",
    "ERR_" + "DUPLICATE_VALUE",
    "ERR_" + "INVALID_VALUE",
    "UN" + "SOLVABLE",
)


class TestFailureReturnOnNoneGrid:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — grid=None happy path of failure."""

    def test_none_grid_returns_failure_not_success_list(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: explicit None grid input
        grid = None

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: failure contract is returned instead of int[6]
        assert isinstance(result, FailureResult)
        assert not isinstance(result, list)

    def test_none_grid_returns_invalid_size_code(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: explicit None grid input
        grid = None

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: code equals INVALID_SIZE exactly
        assert result.code == INVALID_SIZE_CODE

    def test_none_grid_returns_grid_must_be_4x4_message(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: explicit None grid input
        grid = None

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: message matches PRD §8.1 INVALID_SIZE wording
        assert result.message == INVALID_SIZE_MESSAGE

    def test_none_grid_returns_pydantic_failure_result_type(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: explicit None grid input
        grid = None

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: return type is FailureResult (pydantic BaseModel subclass)
        assert isinstance(result, FailureResult)
        assert issubclass(FailureResult, BaseModel)

    def test_none_grid_returns_identical_failure_on_repeat(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: explicit None grid input
        grid = None

        # When: Boundary.solve is invoked twice
        first = boundary.solve(grid)
        second = boundary.solve(grid)

        # Then: identical failure contract on both calls
        assert first.code == second.code == INVALID_SIZE_CODE
        assert first.message == second.message == INVALID_SIZE_MESSAGE


class TestBoundaryDimensionValues:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — structural boundary grids."""

    def test_empty_list_returns_invalid_size_code(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: empty list grid (zero rows)
        grid: list[list[int]] = []

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: INVALID_SIZE failure code is returned
        assert isinstance(result, FailureResult)
        assert result.code == INVALID_SIZE_CODE

    def test_four_empty_rows_returns_invalid_size_code(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: four rows with zero columns each ([[]] * 4)
        grid = [[]] * 4

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: INVALID_SIZE failure code is returned
        assert isinstance(result, FailureResult)
        assert result.code == INVALID_SIZE_CODE

    def test_three_by_four_returns_invalid_size_code(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: 3×4 grid (row count mismatch)
        grid = GRID_3X4

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: INVALID_SIZE failure code is returned
        assert isinstance(result, FailureResult)
        assert result.code == INVALID_SIZE_CODE

    def test_empty_list_returns_grid_must_be_4x4_message(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: empty list grid
        grid: list[list[int]] = []

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: message matches PRD §8.1 INVALID_SIZE wording
        assert result.message == INVALID_SIZE_MESSAGE

    def test_four_empty_rows_returns_grid_must_be_4x4_message(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: [[]] * 4 grid
        grid = GRID_FOUR_EMPTY_ROWS

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: message matches PRD §8.1 INVALID_SIZE wording
        assert result.message == INVALID_SIZE_MESSAGE


class TestDomainResolverIsolation:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — resolve() must not run on invalid input."""

    def test_none_grid_resolve_not_called(
        self,
        boundary: MagicSquareBoundary,
        mock_resolve: MagicMock,
    ) -> None:
        # AC-FR-01-01
        # Given: None grid and spied Domain resolve()
        grid = None

        # When: Boundary.solve is invoked
        boundary.solve(grid)

        # Then: resolve() is never called
        mock_resolve.assert_not_called()

    def test_empty_list_resolve_not_called(
        self,
        boundary: MagicSquareBoundary,
        mock_resolve: MagicMock,
    ) -> None:
        # AC-FR-01-01
        # Given: empty list grid and spied resolve()
        grid: list[list[int]] = []

        # When: Boundary.solve is invoked
        boundary.solve(grid)

        # Then: resolve() is never called
        mock_resolve.assert_not_called()

    def test_four_empty_rows_resolve_not_called(
        self,
        boundary: MagicSquareBoundary,
        mock_resolve: MagicMock,
    ) -> None:
        # AC-FR-01-01
        # Given: [[]] * 4 grid and spied resolve()
        grid = [[]] * 4

        # When: Boundary.solve is invoked
        boundary.solve(grid)

        # Then: resolve() is never called
        mock_resolve.assert_not_called()

    def test_three_by_four_resolve_not_called(
        self,
        boundary: MagicSquareBoundary,
        mock_resolve: MagicMock,
    ) -> None:
        # AC-FR-01-01
        # Given: 3×4 grid and spied resolve()
        grid = GRID_3X4

        # When: Boundary.solve is invoked
        boundary.solve(grid)

        # Then: resolve() is never called
        mock_resolve.assert_not_called()

    def test_none_grid_resolve_call_count_zero(
        self,
        boundary: MagicSquareBoundary,
        mock_resolve: MagicMock,
    ) -> None:
        # AC-FR-01-01
        # Given: None grid and call-count spy on resolve()
        grid = None

        # When: Boundary.solve is invoked
        boundary.solve(grid)

        # Then: resolve() call_count remains exactly zero
        assert mock_resolve.call_count == 0


class TestMessageExactMatch:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — byte-exact message contract."""

    @pytest.mark.parametrize(
        ("case_id", "grid"),
        [
            ("none", None),
            ("empty_list", []),
            ("four_empty_rows", [[]] * 4),
            ("three_by_four", GRID_3X4),
            ("two_by_two", [[1, 2], [3, 4]]),
        ],
        ids=["none", "empty_list", "four_empty_rows", "three_by_four", "two_by_two"],
    )
    def test_dimension_failure_message_exact_match_prd(
        self,
        boundary: MagicSquareBoundary,
        case_id: str,
        grid: Any,
    ) -> None:
        # AC-FR-01-01
        # Given: in-scope dimension failure grid
        _ = case_id

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: message equals PRD §8.1 INVALID_SIZE string byte-for-byte
        assert result.message == INVALID_SIZE_MESSAGE
        assert len(result.message) == len(INVALID_SIZE_MESSAGE)

    def test_none_grid_message_no_extra_whitespace(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: None grid
        grid = None

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: message has no extra whitespace padding
        assert result.message == result.message.strip()
        assert result.message == INVALID_SIZE_MESSAGE

    def test_none_grid_message_terminal_period_exact(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: None grid
        grid = None

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: terminal punctuation matches contract exactly
        assert result.message.endswith(".")
        assert not result.message.endswith("..")

    def test_none_grid_code_message_pair_consistency(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: None grid
        grid = None

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: INVALID_SIZE code pairs with Grid must be 4x4. message
        assert (result.code, result.message) == (
            INVALID_SIZE_CODE,
            INVALID_SIZE_MESSAGE,
        )

    def test_empty_list_message_matches_prd_not_null_wording(
        self,
        boundary: MagicSquareBoundary,
    ) -> None:
        # AC-FR-01-01
        # Given: empty list (not None)
        grid: list[list[int]] = []

        # When: Boundary.solve is invoked
        result = boundary.solve(grid)

        # Then: message is INVALID_SIZE wording, not alternate null wording
        assert result.message == INVALID_SIZE_MESSAGE
        assert "null" not in result.message.lower()


class TestScopeRestriction:
    """AC-FR-01-01, PRD §8.1 INVALID_SIZE — AC-FR-01-02~05 / FR-02~05 excluded."""

    def test_scope_excludes_f1_valid_grid_literal(self) -> None:
        # AC-FR-01-01
        # Given: this test module source
        source = _MODULE_PATH.read_text(encoding="utf-8")

        # When: scanning for F1 fixture grid literal
        # Then: F1 valid 4×4 grid must not appear (FR-05 success path out of scope)
        assert _F1_GRID_SNIPPET not in source

    def test_scope_excludes_f2_valid_grid_literal(self) -> None:
        # AC-FR-01-01
        # Given: this test module source
        source = _MODULE_PATH.read_text(encoding="utf-8")

        # When: scanning for F2 fixture grid literal
        # Then: F2 valid 4×4 grid must not appear (reverse success out of scope)
        assert _F2_GRID_SNIPPET not in source

    def test_scope_excludes_ac_fr_01_03_error_codes(self) -> None:
        # AC-FR-01-01
        # Given: this test module source
        source = _MODULE_PATH.read_text(encoding="utf-8")

        # When: scanning for AC-FR-01-03 blank-count error assertions
        # Then: blank-count error code must not appear as expected assert
        assert "ERR_" + "BLANK_COUNT" not in source

    def test_scope_excludes_ac_fr_01_04_error_codes(self) -> None:
        # AC-FR-01-01
        # Given: this test module source
        source = _MODULE_PATH.read_text(encoding="utf-8")

        # When: scanning for AC-FR-01-04 value error assertions
        # Then: duplicate-value error code must not appear as expected assert
        assert "ERR_" + "DUPLICATE_VALUE" not in source

    def test_scope_excludes_fr02_to_fr05_error_codes(self) -> None:
        # AC-FR-01-01
        # Given: this test module source
        source = _MODULE_PATH.read_text(encoding="utf-8")

        # When: scanning for FR-02~05 domain error codes and out-of-range literals
        # Then: forbidden codes and cell value 17 literal are absent
        for forbidden in _FORBIDDEN_ERROR_CODES:
            assert forbidden not in source
        assert ", " + "17," not in source
