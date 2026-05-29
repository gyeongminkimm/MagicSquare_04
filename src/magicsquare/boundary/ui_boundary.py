"""UIBoundary — solve API with input validation (FR-01)."""

from __future__ import annotations

from typing import Any, Protocol

from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.boundary.validation.boundary_validator import BoundaryValidator
from magicsquare.boundary.validation.input_validator import InputValidator
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare


class PartialMagicResolver(Protocol):
    """Control resolver entry point injected for testability."""

    def resolve(self, grid: list[list[int]]) -> list[int]:
        """Solve a validated 4×4 grid with two blanks."""
        ...


class UIBoundary:
    """Boundary adapter: validate input, delegate solve to control layer."""

    def __init__(
        self,
        resolver: PartialMagicResolver | SolvePartialMagicSquare | None = None,
        validator: BoundaryValidator | None = None,
    ) -> None:
        """Initialize boundary with optional resolver and validator."""
        self._resolver: PartialMagicResolver = (
            resolver or SolvePartialMagicSquare()
        )
        self._validator = validator or BoundaryValidator()

    def solve(self, grid: Any) -> FailureResponse | SuccessResponse:
        """Validate grid, solve or return failure/success envelope."""
        validation = InputValidator.validate(grid)
        if isinstance(validation, FailureResponse):
            return validation
        solution = self._resolver.resolve(grid)
        return SuccessResponse(data=solution)


# Re-export envelope types for boundary consumers.
__all__ = ["FailureResponse", "SuccessResponse", "UIBoundary"]
