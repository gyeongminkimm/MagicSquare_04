"""Solution output value object — int[6] contract."""

from __future__ import annotations

from dataclasses import dataclass

from magicsquare.entity.value_objects.cell_position import CellPosition


@dataclass(frozen=True, slots=True)
class SolutionVector:
    """Encapsulates [r1, c1, n1, r2, c2, n2] with 1-index coordinates."""

    first_position: CellPosition
    first_value: int
    second_position: CellPosition
    second_value: int

    def to_array(self) -> list[int]:
        """Return flat int[6] per boundary contract."""
        return [
            self.first_position.row,
            self.first_position.col,
            self.first_value,
            self.second_position.row,
            self.second_position.col,
            self.second_value,
        ]
