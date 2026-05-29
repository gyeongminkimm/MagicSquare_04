"""Validate complete magic square grids (FR-04)."""

from __future__ import annotations

from magicsquare.entity.value_objects import (
    BLANK_CELL_VALUE,
    CELL_VALUE_MAX,
    CELL_VALUE_MIN,
    GRID_SIZE,
    MAGIC_SUM,
)


def is_magic_square(grid: list[list[int]]) -> bool:
    """Return True when grid is a complete valid 4×4 magic square.

    Args:
        grid: 4×4 grid with no blanks.

    Returns:
        True if all rows, columns, and diagonals sum to MAGIC_SUM and
        values are exactly {CELL_VALUE_MIN..CELL_VALUE_MAX} without duplicate.
    """
    values = [grid[row][col] for row in range(GRID_SIZE) for col in range(GRID_SIZE)]
    if BLANK_CELL_VALUE in values:
        return False
    if len(set(values)) != len(values):
        return False
    if any(value < CELL_VALUE_MIN or value > CELL_VALUE_MAX for value in values):
        return False
    if set(values) != set(range(CELL_VALUE_MIN, CELL_VALUE_MAX + 1)):
        return False

    for row_index in range(GRID_SIZE):
        if sum(grid[row_index][col] for col in range(GRID_SIZE)) != MAGIC_SUM:
            return False

    for col_index in range(GRID_SIZE):
        if sum(grid[row][col_index] for row in range(GRID_SIZE)) != MAGIC_SUM:
            return False

    main_diagonal = sum(grid[index][index] for index in range(GRID_SIZE))
    anti_diagonal = sum(
        grid[index][GRID_SIZE - 1 - index] for index in range(GRID_SIZE)
    )
    return main_diagonal == MAGIC_SUM and anti_diagonal == MAGIC_SUM
