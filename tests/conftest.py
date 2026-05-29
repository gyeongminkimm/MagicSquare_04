"""Shared grid placeholders for Dual-Track RED (Report/09 §4 G0~G3).

Fixtures are comment-only until GREEN; entity/boundary tests reference these literals
via tests/entity/conftest.py or inline comments in skeleton tests.
"""

# G0 — F1 complete magic square (no blanks)
# GRID_G0: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G1 — F2 / TD-02; blanks (2,2), (3,3) 1-index; missing {7, 10}
# GRID_G1: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 0, 11, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]

# G2 — F1 / TD-01; blanks (1,2), (2,3) 1-index; solve [1,2,3,2,3,11]
# GRID_G2: list[list[int]] = [
#     [16, 0, 2, 13],
#     [5, 10, 0, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G3 — PLACEHOLDER (F3 / TD-07); unsolvable both attempts
# GRID_G3: list[list[int]] = ...  # Decision Needed (Report/09 OQ-09-02)
