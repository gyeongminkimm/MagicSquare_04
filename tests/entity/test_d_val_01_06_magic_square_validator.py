"""D-VAL-01~06 — magic square validator (Report/09 §6.1). Domain Mock 금지."""

from __future__ import annotations

import pytest

from magicsquare.entity.validator.magic_square_validator import is_magic_square

from tests.entity.grid_fixtures import GRID_G0


class TestDVal01CompleteGrid:
    """D-VAL-01 — G0 complete → True."""

    def test_d_val_01_g0_complete_returns_true(self) -> None:
        # Given: G0 complete grid
        grid = GRID_G0

        # When: is_magic_square is invoked
        result = is_magic_square(grid)

        # Then: True
        assert result is True


class TestDVal02RowSum:
    """D-VAL-02 — row sum mismatch → False."""

    def test_d_val_02_row_sum_mismatch_returns_false(self) -> None:
        pytest.fail("RED: D-VAL-02 — row sum ≠ MAGIC_SUM → False (I1)")


class TestDVal03ColSum:
    """D-VAL-03 — column sum mismatch → False."""

    def test_d_val_03_col_sum_mismatch_returns_false(self) -> None:
        pytest.fail("RED: D-VAL-03 — column sum ≠ MAGIC_SUM → False (I2)")


class TestDVal04Diagonal:
    """D-VAL-04 — diagonal mismatch → False."""

    def test_d_val_04_diagonal_d2_mismatch_returns_false(self) -> None:
        pytest.fail("RED: D-VAL-04 — diagonal ≠ MAGIC_SUM → False (I3)")


class TestDVal05InvalidSet:
    """D-VAL-05 — 1~16 violation or duplicate → False."""

    def test_d_val_05_value_17_returns_false(self) -> None:
        pytest.fail("RED: D-VAL-05 — value 17 in complete grid → False (I4)")


class TestDVal06ZeroInComplete:
    """D-VAL-06 — zero in complete grid → False."""

    def test_d_val_06_zero_in_complete_grid_returns_false(self) -> None:
        pytest.fail("RED: D-VAL-06 — 0 in complete grid → False (I4)")
