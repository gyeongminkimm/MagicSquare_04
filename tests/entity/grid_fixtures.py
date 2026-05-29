"""G0~G2 grid fixtures for Track B (Report/09 §4)."""

from __future__ import annotations

# G0 — F1 complete magic square (no blanks)
GRID_G0: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# G1 — F2 / TD-02; blanks (2,2), (3,3) 1-index
GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# G2 — F1 / TD-01; blanks (1,2), (2,3) 1-index
GRID_G2: list[list[int]] = [
    [16, 0, 2, 13],
    [5, 10, 0, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]
