"""Golden Master input scenarios (Report/02 F1/F2 + FR-01 error paths)."""

from __future__ import annotations

from dataclasses import dataclass

from tests.boundary.u_in_constants import GRID_TD_05, GRID_THREE_BLANKS
from tests.entity.grid_fixtures import GRID_G1, GRID_G2

# GM-TC-01 — F1 / TD-01 small-first success (Report/02)
GRID_NORMAL_SUCCESS: list[list[int]] = GRID_G2

# GM-TC-02 — F2 / TD-02 reverse fallback success (Report/02)
GRID_REVERSE_SUCCESS: list[list[int]] = GRID_G1

# GM-TC-03 — three blanks (U-IN-05)
GRID_INVALID_BLANK_COUNT: list[list[int]] = GRID_THREE_BLANKS

# GM-TC-04 — non-zero duplicate (U-IN-08)
GRID_DUPLICATE_NUMBER: list[list[int]] = GRID_TD_05

# GM-TC-05 — both assignments fail (F3 stand-in until G3 SSOT)
GRID_NO_VALID_MAGIC_SQUARE: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 0, 12],
    [13, 14, 15, 0],
]


@dataclass(frozen=True)
class GoldenScenario:
    """One Golden Master scenario with stable section key and puzzle grid."""

    tc_id: str
    key: str
    grid: list[list[int]]
    expect_error: bool = False


GOLDEN_SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario("GM-TC-01", "normal_success", GRID_NORMAL_SUCCESS),
    GoldenScenario("GM-TC-02", "reverse_success", GRID_REVERSE_SUCCESS),
    GoldenScenario(
        "GM-TC-03",
        "invalid_blank_count",
        GRID_INVALID_BLANK_COUNT,
        expect_error=True,
    ),
    GoldenScenario(
        "GM-TC-04",
        "duplicate_number",
        GRID_DUPLICATE_NUMBER,
        expect_error=True,
    ),
    GoldenScenario(
        "GM-TC-05",
        "no_valid_magic_square",
        GRID_NO_VALID_MAGIC_SQUARE,
        expect_error=True,
    ),
)

SCENARIO_BY_TC_ID: dict[str, GoldenScenario] = {
    scenario.tc_id: scenario for scenario in GOLDEN_SCENARIOS
}
