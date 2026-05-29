"""Golden Master contract assertions (Report/02 I-O1, I-O2, FR-02)."""

from __future__ import annotations

import ast

from magicsquare.boundary.constants import GRID_DIMENSION
from magicsquare.entity.locator.empty_cell_locator import find_blank_coords
from magicsquare.entity.resolver.missing_number_finder import find_not_exist_nums
from magicsquare.entity.solver.two_blank_puzzle_solver import solve_two_blank_puzzle
from magicsquare.entity.validator.magic_square_validator import is_magic_square

from tests.golden_master.capture import SEMANTIC_DUPLICATE_NUMBER, SEMANTIC_INVALID_BLANK_COUNT
from tests.golden_master.capture import SEMANTIC_NO_VALID_MAGIC_SQUARE


def parse_success_output(block: str) -> list[int]:
    """Parse ``Output:`` line from a Golden Master scenario block."""
    lines = block.splitlines()
    for index, line in enumerate(lines):
        if line == "Output:" and index + 1 < len(lines):
            return ast.literal_eval(lines[index + 1])
    raise ValueError("Golden Master block has no Output section")


def parse_error_token(block: str) -> str:
    """Parse ``Error:`` token from a Golden Master scenario block."""
    lines = block.splitlines()
    for index, line in enumerate(lines):
        if line == "Error:" and index + 1 < len(lines):
            return lines[index + 1].strip()
    raise ValueError("Golden Master block has no Error section")


def assert_int_six_format(data: list[int]) -> None:
    """Verify int[6] boundary output shape."""
    assert len(data) == 6, f"expected int[6], got length {len(data)}"
    assert all(isinstance(value, int) for value in data)
    row_one, col_one, num_one, row_two, col_two, num_two = data
    for row, col in ((row_one, col_one), (row_two, col_two)):
        assert 1 <= row <= GRID_DIMENSION, f"row {row} not 1-index in 1..{GRID_DIMENSION}"
        assert 1 <= col <= GRID_DIMENSION, f"col {col} not 1-index in 1..{GRID_DIMENSION}"
    assert 1 <= num_one <= 16 and 1 <= num_two <= 16
    assert num_one != num_two


def assert_row_major_blank_order(grid: list[list[int]], data: list[int]) -> None:
    """Verify coordinates follow row-major blank scan (FR-02)."""
    first_pos, second_pos = find_blank_coords(grid)
    assert data[0] == first_pos.row and data[1] == first_pos.col
    assert data[3] == second_pos.row and data[4] == second_pos.col


def assert_small_first_combination(grid: list[list[int]], data: list[int]) -> None:
    """Verify I-O2 small-first assignment (min at first blank, max at second)."""
    missing = find_not_exist_nums(grid)
    assert data[2] == missing.smaller
    assert data[5] == missing.larger
    filled = _filled_from_solution(grid, data)
    assert is_magic_square(filled)


def assert_reverse_fallback_combination(grid: list[list[int]], data: list[int]) -> None:
    """Verify I-O2 reverse fallback (max at first blank, min at second)."""
    missing = find_not_exist_nums(grid)
    assert data[2] == missing.larger
    assert data[5] == missing.smaller
    filled = _filled_from_solution(grid, data)
    assert is_magic_square(filled)
    # small-first must fail for this scenario
    small_first = _filled_from_solution(
        grid,
        [
            data[0],
            data[1],
            missing.smaller,
            data[3],
            data[4],
            missing.larger,
        ],
    )
    assert not is_magic_square(small_first)


def assert_error_contract(token: str, expected: str) -> None:
    """Verify semantic Error token matches Golden Master contract."""
    assert token == expected


def assert_unsolvable_grid(grid: list[list[int]]) -> None:
    """Verify both fill assignments fail (Domain unsolvable path)."""
    from magicsquare.entity.exceptions import UnsolvableDomainError

    try:
        solve_two_blank_puzzle(grid)
    except UnsolvableDomainError:
        return
    raise AssertionError("expected UnsolvableDomainError for unsolvable grid")


def _filled_from_solution(grid: list[list[int]], data: list[int]) -> list[list[int]]:
    """Apply int[6] vector back onto a puzzle copy."""
    import copy

    filled = copy.deepcopy(grid)
    filled[data[0] - 1][data[1] - 1] = data[2]
    filled[data[3] - 1][data[4] - 1] = data[5]
    return filled


__all__ = [
    "SEMANTIC_DUPLICATE_NUMBER",
    "SEMANTIC_INVALID_BLANK_COUNT",
    "SEMANTIC_NO_VALID_MAGIC_SQUARE",
    "assert_error_contract",
    "assert_int_six_format",
    "assert_reverse_fallback_combination",
    "assert_row_major_blank_order",
    "assert_small_first_combination",
    "assert_unsolvable_grid",
    "parse_error_token",
    "parse_success_output",
]
