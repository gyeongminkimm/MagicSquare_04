"""Named constants for boundary validation (no magic numbers in logic)."""

from __future__ import annotations

GRID_DIMENSION: int = 4
EXPECTED_BLANK_COUNT: int = 2
BLANK_CELL_VALUE: int = 0
CELL_VALUE_MIN: int = 1
CELL_VALUE_MAX: int = 16

INVALID_SIZE_CODE: str = "INVALID_SIZE"
INVALID_SIZE_MESSAGE: str = "Grid must be 4x4."

ERR_BLANK_COUNT_CODE: str = "E002"
ERR_BLANK_COUNT_MESSAGE: str = "Grid must contain exactly 2 blank cells (0)."
ERR_INVALID_VALUE_CODE: str = "E004"
ERR_INVALID_VALUE_MESSAGE: str = "Cell value must be 0 or between 1 and 16."
ERR_DUPLICATE_VALUE_CODE: str = "E005"
ERR_DUPLICATE_VALUE_MESSAGE: str = "Duplicate non-zero value is not allowed."
