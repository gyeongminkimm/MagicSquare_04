"""Track B RED skeleton — D-VAL-01~06 (Report/09 §6.1). Domain Mock 금지."""

from __future__ import annotations

import pytest

from magicsquare.entity.validator.magic_square_validator import is_magic_square


class TestDVal01CompleteGrid:
    """D-VAL-01 — G0 complete → True."""

    def test_d_val_01_g0_complete_returns_true(self) -> None:
        # Given: G0 complete grid
        # When: is_magic_square(grid)
        # Then: True
        pytest.fail(
            "RED: D-VAL-01 — G0 complete magic square → True (I1~I5, FR-04 AC-12)"
        )


class TestDVal02RowSum:
    """D-VAL-02 — row sum mismatch → False."""

    def test_d_val_02_row_sum_mismatch_returns_false(self) -> None:
        # Given: G0 with row1 sum broken (e.g. (1,1) 16→15)
        # When: is_magic_square(grid)
        # Then: False
        pytest.fail("RED: D-VAL-02 — row sum ≠ 34 → False (I1)")


class TestDVal03ColSum:
    """D-VAL-03 — column sum mismatch → False."""

    def test_d_val_03_col_sum_mismatch_returns_false(self) -> None:
        # Given: G0 with column1 sum broken
        # When: is_magic_square(grid)
        # Then: False
        pytest.fail("RED: D-VAL-03 — column sum ≠ 34 → False (I2)")


class TestDVal04Diagonal:
    """D-VAL-04 — diagonal mismatch → False."""

    def test_d_val_04_diagonal_d2_mismatch_returns_false(self) -> None:
        # Given: G0 with D2 (1,4)(2,3)(3,2)(4,1) broken only
        # When: is_magic_square(grid)
        # Then: False
        pytest.fail("RED: D-VAL-04 — diagonal ≠ 34 → False (I3)")


class TestDVal05InvalidSet:
    """D-VAL-05 — 1~16 violation or duplicate → False."""

    def test_d_val_05_value_17_returns_false(self) -> None:
        # Given: complete 4×4 with cell 17
        # When: is_magic_square(grid)
        # Then: False
        pytest.fail("RED: D-VAL-05 — value 17 in complete grid → False (I4)")

    def test_d_val_05_duplicate_in_complete_returns_false(self) -> None:
        # Given: complete grid with duplicate non-zero
        # When: is_magic_square(grid)
        # Then: False
        pytest.fail("RED: D-VAL-05 — duplicate in complete grid → False (I4)")


class TestDVal06ZeroInComplete:
    """D-VAL-06 — zero in complete grid → False."""

    def test_d_val_06_zero_in_complete_grid_returns_false(self) -> None:
        # Given: G0 with one cell replaced by 0
        # When: is_magic_square(grid)
        # Then: False
        pytest.fail("RED: D-VAL-06 — 0 in complete grid → False (I4)")
