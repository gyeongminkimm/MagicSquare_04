"""Missing number pair from partial grid."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MissingPair:
    """Two missing values with smaller-first ordering (I11)."""

    smaller: int
    larger: int

    def as_sorted_set(self) -> set[int]:
        """Return {smaller, larger}."""
        return {self.smaller, self.larger}
