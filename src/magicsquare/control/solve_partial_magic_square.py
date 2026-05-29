"""SolvePartialMagicSquare — orchestrates domain locate → find → solve."""

from __future__ import annotations

from magicsquare.entity.locator.empty_cell_locator import find_blank_coords
from magicsquare.entity.resolver.missing_number_finder import find_not_exist_nums
from magicsquare.entity.solver.two_blank_puzzle_solver import solve_two_blank_puzzle


class SolvePartialMagicSquare:
    """Control use case: two-blank magic square completion."""

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Orchestrate domain services and return int[6] solution vector.

        Args:
            grid: Validated 4×4 puzzle with exactly two blanks.

        Returns:
            Solution as [r1, c1, n1, r2, c2, n2] with 1-index coordinates.
        """
        find_blank_coords(grid)
        find_not_exist_nums(grid)
        solution = solve_two_blank_puzzle(grid)
        return solution.to_array()
