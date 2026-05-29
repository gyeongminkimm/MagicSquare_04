"""1-index cell position value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CellPosition:
    """Grid coordinate with 1-based row and column."""

    row: int
    col: int

    def as_tuple(self) -> tuple[int, int]:
        """Return (row, col) tuple."""
        return (self.row, self.col)
