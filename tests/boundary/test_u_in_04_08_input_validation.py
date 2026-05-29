"""U-IN-04~08 — FR-01 input validation beyond dimension (Report/09 §5.1)."""

from __future__ import annotations

from magicsquare.boundary.schemas import ValidationSuccess
from magicsquare.boundary.schemas import FailureResponse
from magicsquare.boundary.validation.input_validator import InputValidator

from tests.boundary.u_in_constants import (
    ERR_BLANK_COUNT_CODE,
    ERR_BLANK_COUNT_MESSAGE,
    ERR_DUPLICATE_VALUE_CODE,
    ERR_DUPLICATE_VALUE_MESSAGE,
    ERR_INVALID_VALUE_CODE,
    ERR_INVALID_VALUE_MESSAGE,
    GRID_G1,
    GRID_TD_04,
    GRID_TD_05,
    GRID_TD_06,
    GRID_TD_06_NEGATIVE,
    GRID_THREE_BLANKS,
)


class TestG1GivenPassesInputValidation:
    """G1 — Report/02 F2 grid passes FR-01 validate() (GREEN bundle 1)."""

    def test_g1_validate_returns_validation_success(self) -> None:
        # Given: G1 / F2 grid with exactly two blanks
        grid = GRID_G1

        # When: InputValidator.validate is invoked
        result = InputValidator.validate(grid)

        # Then: pass signal, not failure envelope
        assert isinstance(result, ValidationSuccess)
        assert not isinstance(result, FailureResponse)
        assert result.type == "OK"


class TestUIn04ZeroBlanks:
    """U-IN-04 — blank count 0 → E002."""

    def test_zero_blanks_returns_e002(self) -> None:
        # Given: TD-04 grid (zero blanks)
        grid = GRID_TD_04

        # When: InputValidator.validate is invoked
        result = InputValidator.validate(grid)

        # Then: E002 failure envelope
        assert isinstance(result, FailureResponse)
        assert result.type == "ERROR"
        assert result.code == ERR_BLANK_COUNT_CODE
        assert result.message == ERR_BLANK_COUNT_MESSAGE


class TestUIn05ThreeBlanks:
    """U-IN-05 — blank count 3 → E002."""

    def test_three_blanks_returns_e002(self) -> None:
        # Given: F1-derived grid with three blanks
        grid = GRID_THREE_BLANKS

        # When: InputValidator.validate is invoked
        result = InputValidator.validate(grid)

        # Then: E002 failure envelope
        assert isinstance(result, FailureResponse)
        assert result.type == "ERROR"
        assert result.code == ERR_BLANK_COUNT_CODE
        assert result.message == ERR_BLANK_COUNT_MESSAGE


class TestUIn06OutOfRange:
    """U-IN-06/07 — value ∉ {0}∪[1,16] → E004."""

    def test_cell_value_17_returns_e004(self) -> None:
        # Given: TD-06 grid (cell 17)
        grid = GRID_TD_06

        # When: InputValidator.validate is invoked
        result = InputValidator.validate(grid)

        # Then: E004 failure envelope
        assert isinstance(result, FailureResponse)
        assert result.type == "ERROR"
        assert result.code == ERR_INVALID_VALUE_CODE
        assert result.message == ERR_INVALID_VALUE_MESSAGE

    def test_cell_value_negative_one_returns_e004(self) -> None:
        # Given: 4×4 grid with -1 at (2,1) 1-index
        grid = GRID_TD_06_NEGATIVE

        # When: InputValidator.validate is invoked
        result = InputValidator.validate(grid)

        # Then: E004 failure envelope
        assert isinstance(result, FailureResponse)
        assert result.type == "ERROR"
        assert result.code == ERR_INVALID_VALUE_CODE
        assert result.message == ERR_INVALID_VALUE_MESSAGE


class TestUIn08DuplicateNonZero:
    """U-IN-08 — non-zero duplicate → E005."""

    def test_duplicate_nonzero_returns_e005(self) -> None:
        # Given: TD-05 grid (duplicate 5)
        grid = GRID_TD_05

        # When: InputValidator.validate is invoked
        result = InputValidator.validate(grid)

        # Then: E005 failure envelope
        assert isinstance(result, FailureResponse)
        assert result.type == "ERROR"
        assert result.code == ERR_DUPLICATE_VALUE_CODE
        assert result.message == ERR_DUPLICATE_VALUE_MESSAGE
