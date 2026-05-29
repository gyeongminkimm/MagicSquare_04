"""Entity-track fixtures — G0~G3 placeholders (Report/09 §4).

Domain Mock 금지. Grid literals activate in GREEN phase.
"""

# See tests/conftest.py for G0~G3 matrix definitions (comment placeholders).

# TD-04 — zero blanks (U-IN-04 skeleton Given reference)
# GRID_TD_04: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# TD-05 — duplicate non-zero (U-IN-07)
# GRID_TD_05: list[list[int]] = [
#     [16, 0, 2, 13],
#     [5, 10, 5, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]

# TD-06 — value 17 (U-IN-06)
# GRID_TD_06: list[list[int]] = [
#     [16, 0, 2, 13],
#     [5, 10, 17, 8],
#     [9, 6, 0, 12],
#     [4, 15, 14, 1],
# ]
