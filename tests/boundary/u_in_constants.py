"""U-IN-04~08 contract constants and TD/G1 grids (Report/09)."""

from __future__ import annotations

from magicsquare.boundary.constants import (
    ERR_BLANK_COUNT_CODE,
    ERR_BLANK_COUNT_MESSAGE,
    ERR_DUPLICATE_VALUE_CODE,
    ERR_DUPLICATE_VALUE_MESSAGE,
    ERR_INVALID_VALUE_CODE,
    ERR_INVALID_VALUE_MESSAGE,
)

# G1 — Report/02 F2 / TD-02; blanks (2,2), (3,3) 1-index
GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# TD-04 — zero blanks (U-IN-04)
GRID_TD_04: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# TD-05 — duplicate non-zero (U-IN-08)
GRID_TD_05: list[list[int]] = [
    [16, 0, 2, 13],
    [5, 10, 5, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# TD-06 — value 17 (U-IN-06)
GRID_TD_06: list[list[int]] = [
    [16, 0, 2, 13],
    [5, 10, 17, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# TD-06 extension — value -1 (U-IN-07)
GRID_TD_06_NEGATIVE: list[list[int]] = [
    [16, 3, 2, 13],
    [-1, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# F1-derived — three blanks (U-IN-05)
GRID_THREE_BLANKS: list[list[int]] = [
    [16, 0, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

__all__ = [
    "ERR_BLANK_COUNT_CODE",
    "ERR_BLANK_COUNT_MESSAGE",
    "ERR_DUPLICATE_VALUE_CODE",
    "ERR_DUPLICATE_VALUE_MESSAGE",
    "ERR_INVALID_VALUE_CODE",
    "ERR_INVALID_VALUE_MESSAGE",
    "GRID_G1",
    "GRID_TD_04",
    "GRID_TD_05",
    "GRID_TD_06",
    "GRID_TD_06_NEGATIVE",
    "GRID_THREE_BLANKS",
]
