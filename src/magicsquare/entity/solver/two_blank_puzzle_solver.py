"""Two-blank puzzle solver — UC-D4 (Report/02 §1.3)."""

from __future__ import annotations

import copy

from magicsquare.entity.exceptions import UnsolvableDomainError
from magicsquare.entity.locator.empty_cell_locator import find_blank_coords
from magicsquare.entity.resolver.missing_number_finder import find_not_exist_nums
from magicsquare.entity.validator.magic_square_validator import is_magic_square
from magicsquare.entity.value_objects.cell_position import CellPosition
from magicsquare.entity.value_objects.solution_vector import SolutionVector


def solve_two_blank_puzzle(grid: list[list[int]]) -> SolutionVector:
    """Solve a two-blank puzzle by trying both fill assignments.

    Args:
        grid: Validated 4×4 puzzle with exactly two blanks.

    Returns:
        SolutionVector for the valid min/max assignment per I-O2.

    Raises:
        UnsolvableDomainError: When neither assignment yields a magic square.
    """
    first_pos, second_pos = find_blank_coords(grid)
    missing = find_not_exist_nums(grid)
    smaller = missing.smaller
    larger = missing.larger

    first_attempt = _filled_grid(grid, first_pos, smaller, second_pos, larger)
    if is_magic_square(first_attempt):
        return SolutionVector(first_pos, smaller, second_pos, larger)

    second_attempt = _filled_grid(grid, first_pos, larger, second_pos, smaller)
    if is_magic_square(second_attempt):
        return SolutionVector(first_pos, larger, second_pos, smaller)

    raise UnsolvableDomainError("No valid assignment for two-blank puzzle.")


def _filled_grid(
    grid: list[list[int]],
    first_pos: CellPosition,
    first_value: int,
    second_pos: CellPosition,
    second_value: int,
) -> list[list[int]]:
    """Return a copy of grid with both blanks filled."""
    filled = copy.deepcopy(grid)
    filled[first_pos.row - 1][first_pos.col - 1] = first_value
    filled[second_pos.row - 1][second_pos.col - 1] = second_value
    return filled
