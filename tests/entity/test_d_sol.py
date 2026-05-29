"""Track B RED skeleton — D-SOL-01~04 (Report/09 §6.1). Domain Mock 금지."""

from __future__ import annotations

import pytest

from magicsquare.control.solve_two_blank_puzzle import SolveTwoBlankPuzzle


class TestDSol01StepASuccess:
    """D-SOL-01 — G1 Attempt A success vector."""

    def test_d_sol_01_g1_step_a_returns_vector(self) -> None:
        # Given: G1 grid
        # When: solution(grid) / SolveTwoBlankPuzzle.solve(grid)
        # Then: [2,2,7,3,3,10]
        pytest.fail(
            "RED: D-SOL-01 — G1 → [2,2,7,3,3,10] (I8, I-O2, FR-05 AC-15)"
        )


class TestDSol02StepBFallback:
    """D-SOL-02 — G2 Step A fail, Step B success."""

    def test_d_sol_02_g2_step_b_success_vector(self) -> None:
        # Given: G2 grid (F1 / TD-01) — TBD wiring in fixture phase
        # When: solution(grid)
        # Then: [1,2,3,2,3,11]
        pytest.fail("RED: D-SOL-02 — G2 TBD")


class TestDSol03Unsolvable:
    """D-SOL-03 — G3 both attempts fail."""

    def test_d_sol_03_g3_raises_unsolvable_domain_error(self) -> None:
        # Given: G3 PLACEHOLDER grid (F3 / TD-07)
        # When: solution(grid)
        # Then: UnsolvableDomainError
        pytest.fail(
            "RED: D-SOL-03 — G3 PLACEHOLDER → UnsolvableDomainError (I10, FR-05 AC-17)"
        )


class TestDSol04OutputShape:
    """D-SOL-04 — return length 6."""

    def test_d_sol_04_solution_length_six(self) -> None:
        # Given: G1 or G2 valid puzzle grid
        # When: solution(grid)
        # Then: len(result) == 6
        pytest.fail(
            "RED: D-SOL-04 — solution vector length 6 (I8/I9, BR-13, FR-05 AC-18)"
        )
