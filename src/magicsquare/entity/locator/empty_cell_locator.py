"""Locate blank cells in row-major scan order (FR-02)."""

from __future__ import annotations

from magicsquare.entity.value_objects import BLANK_CELL_VALUE, GRID_SIZE
from magicsquare.entity.value_objects.cell_position import CellPosition


def find_blank_coords(
    grid: list[list[int]],
) -> tuple[CellPosition, CellPosition]:
    """Return first and second blank positions in 1-index row-major order.

    Args:
        grid: 4×4 puzzle grid with exactly two blank cells (0).

    Returns:
        Tuple of two CellPosition values in scan order.
    """
    blanks: list[CellPosition] = []
    for row_index in range(GRID_SIZE):
        for col_index in range(GRID_SIZE):
            if grid[row_index][col_index] == BLANK_CELL_VALUE:
                blanks.append(
                    CellPosition(row=row_index + 1, col=col_index + 1)
                )
    return blanks[0], blanks[1]
