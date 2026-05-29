"""D-SOL-01~04 — two-blank puzzle solver (Report/09 §6.1). Domain Mock 금지."""

from __future__ import annotations

import pytest

from magicsquare.entity.solver.two_blank_puzzle_solver import solve_two_blank_puzzle

from tests.entity.grid_fixtures import GRID_G1


class TestDSol01StepASuccess:
    """D-SOL-01 — G1 valid assignment vector (F2 fixture)."""

    def test_d_sol_01_g1_step_a_returns_vector(self) -> None:
        # Given: G1 grid
        grid = GRID_G1

        # When: solve_two_blank_puzzle is invoked
        result = solve_two_blank_puzzle(grid)

        # Then: F2 contract [2,2,10,3,3,7] (min→first blank when valid)
        assert result.to_array() == [2, 2, 10, 3, 3, 7]


class TestDSol02StepBFallback:
    """D-SOL-02 — G2 Step A fail, Step B success."""

    def test_d_sol_02_g2_step_b_success_vector(self) -> None:
        pytest.fail("RED: D-SOL-02 — G2 → [1,2,3,2,3,11]")


class TestDSol03Unsolvable:
    """D-SOL-03 — G3 both attempts fail."""

    def test_d_sol_03_g3_raises_unsolvable_domain_error(self) -> None:
        pytest.fail("RED: D-SOL-03 — G3 → UnsolvableDomainError")


class TestDSol04OutputShape:
    """D-SOL-04 — return length 6."""

    def test_d_sol_04_solution_length_six(self) -> None:
        pytest.fail("RED: D-SOL-04 — solution vector length 6")
