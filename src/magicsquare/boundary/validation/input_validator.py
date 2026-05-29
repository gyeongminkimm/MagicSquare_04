"""FR-01 input validation — dimension and content rules (short-circuit)."""

from __future__ import annotations

from typing import Any

from magicsquare.boundary.constants import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE
from magicsquare.boundary.schemas import FailureResponse, ValidationSuccess
from magicsquare.boundary.validation.boundary_validator import BoundaryValidator


class InputValidator:
    """Validates puzzle grid input before control/domain delegation."""

    @staticmethod
    def validate(grid: Any) -> FailureResponse | ValidationSuccess:
        """Return failure envelope or pass signal (short-circuit on first rule)."""
        if not BoundaryValidator.is_valid_dimension(grid):
            return FailureResponse(
                code=INVALID_SIZE_CODE,
                message=INVALID_SIZE_MESSAGE,
            )
        return ValidationSuccess()
