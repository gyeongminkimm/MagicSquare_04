"""Track A RED skeleton — U-IN-04~08 input validation (Report/09 §5.1).

U-IN-01~03 covered by tests/boundary/test_ac_fr_01_01_dimension_validation.py (Report/08).
"""

from __future__ import annotations

import pytest

from magicsquare.boundary.validation.boundary_validator import BoundaryValidator

# Alias per design: InputValidator.validate → BoundaryValidator (GREEN wiring TBD)


class TestUIn04ZeroBlanks:
    """U-IN-04 — blank count 0 → E002."""

    def test_u_in_04_zero_empty_cells_returns_e002(self) -> None:
        # Given: TD-04 grid (zero blanks)
        # validator = BoundaryValidator()
        # grid = GRID_TD_04  # tests/entity/conftest placeholder

        # When: InputValidator.validate(grid) / BoundaryValidator.validate(grid)

        # Then: failure.code == "E002" (not implemented in skeleton)
        pytest.fail(
            "RED: U-IN-04 — zero blanks → E002, execute 0회 (FR-01 AC-03, BR-02)"
        )


class TestUIn05ThreeBlanks:
    """U-IN-05 — blank count 3 → E002."""

    def test_u_in_05_three_blanks_returns_e002(self) -> None:
        # Given: F1 + third blank at (3,3) — three zeros
        # grid = [[16,0,2,13],[5,10,0,8],[9,6,0,12],[4,15,14,1]]

        # When: BoundaryValidator.validate(grid)

        # Then: E002 + blank message exact
        pytest.fail(
            "RED: U-IN-05 — three blanks → E002, execute 0회 (FR-01 AC-03, ES-02)"
        )


class TestUIn06OutOfRange:
    """U-IN-06 — value ∉ {0}∪[1,16] → E004."""

    def test_u_in_06_cell_value_17_returns_e004(self) -> None:
        # Given: TD-06 grid (cell 17)
        # When: BoundaryValidator.validate(grid)
        # Then: E004 + value range message
        pytest.fail(
            "RED: U-IN-06 — TD-06 value 17 → E004 (FR-01 AC-02, BR-03, ES-03)"
        )

    def test_u_in_07_cell_value_negative_one_returns_e004(self) -> None:
        # Given: 4×4 grid with -1 at (1,1) (parametrize extension)
        # When: BoundaryValidator.validate(grid)
        # Then: E004
        pytest.fail(
            "RED: U-IN-07 — cell -1 → E004 (FR-01 AC-02, UI-IN-04)"
        )


class TestUIn08DuplicateNonZero:
    """U-IN-08 — non-zero duplicate → E005."""

    def test_u_in_08_duplicate_nonzero_returns_e005(self) -> None:
        # Given: TD-05 grid (duplicate 5)
        # When: BoundaryValidator.validate(grid)
        # Then: E005 + duplicate message exact
        pytest.fail(
            "RED: U-IN-08 — TD-05 duplicate → E005 (FR-01 AC-04, BR-04, ES-04)"
        )
