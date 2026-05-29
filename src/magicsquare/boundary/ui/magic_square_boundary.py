"""MagicSquareBoundary — solve API with input validation (FR-01)."""

from __future__ import annotations

from typing import Any, Protocol

from magicsquare.boundary.constants import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE
from magicsquare.boundary.schemas import FailureResult
from magicsquare.boundary.validation.boundary_validator import BoundaryValidator
from magicsquare.control.solve_two_blank_puzzle import SolveTwoBlankPuzzle


class PuzzleResolver(Protocol):
    """Domain resolver entry point injected for testability."""

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Solve a validated 4×4 grid with two blanks."""
        ...


class MagicSquareBoundary:
    """Boundary adapter: validate input, delegate solve to control layer."""

    def __init__(
        self,
        resolver: PuzzleResolver | SolveTwoBlankPuzzle | None = None,
        validator: BoundaryValidator | None = None,
    ) -> None:
        """Initialize boundary with optional resolver and validator."""
        self._resolver: PuzzleResolver = resolver or SolveTwoBlankPuzzle()
        self._validator = validator or BoundaryValidator()

    def solve(self, grid: Any) -> FailureResult | list[int]:
        """Validate grid structure and solve or return failure."""
        if not self._validator.is_valid_dimension(grid):
            return FailureResult(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        return self._resolver.resolve(grid)
