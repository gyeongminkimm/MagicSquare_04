"""Capture solver / Result-DTO output into Golden Master text blocks."""

from __future__ import annotations

from magicsquare.boundary.constants import (
    BLANK_CELL_VALUE,
    CELL_VALUE_MAX,
    CELL_VALUE_MIN,
    ERR_BLANK_COUNT_CODE,
    ERR_DUPLICATE_VALUE_CODE,
    EXPECTED_BLANK_COUNT,
)
from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
from magicsquare.entity.exceptions import UnsolvableDomainError

from tests.golden_master.scenarios import GOLDEN_SCENARIOS, GoldenScenario

GOLDEN_SECTION_SEPARATOR: str = "\n\n________________________________________\n\n"

# Semantic tokens stored in golden_master_expected.txt (contract-facing labels).
SEMANTIC_INVALID_BLANK_COUNT: str = "INVALID_BLANK_COUNT"
SEMANTIC_DUPLICATE_NUMBER: str = "DUPLICATE_NUMBER"
SEMANTIC_NO_VALID_MAGIC_SQUARE: str = "NO_VALID_MAGIC_SQUARE"

_BOUNDARY_CODE_TO_SEMANTIC: dict[str, str] = {
    ERR_BLANK_COUNT_CODE: SEMANTIC_INVALID_BLANK_COUNT,
    ERR_DUPLICATE_VALUE_CODE: SEMANTIC_DUPLICATE_NUMBER,
}

_SCENARIO_BY_KEY: dict[str, GoldenScenario] = {
    scenario.key: scenario for scenario in GOLDEN_SCENARIOS
}


def format_grid_input(grid: list[list[int]]) -> str:
    """Render 4×4 grid as space-separated rows for the baseline file."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def _count_blanks(grid: list[list[int]]) -> int:
    return sum(row.count(BLANK_CELL_VALUE) for row in grid)


def _validate_content(grid: list[list[int]]) -> FailureResponse | None:
    """FR-01 content rules used by Golden Master until UIBoundary fully GREEN."""
    blank_count = _count_blanks(grid)
    if blank_count != EXPECTED_BLANK_COUNT:
        return FailureResponse(
            code=ERR_BLANK_COUNT_CODE,
            message="Grid must contain exactly 2 blank cells (0).",
        )

    seen: set[int] = set()
    for row in grid:
        for value in row:
            if value == BLANK_CELL_VALUE:
                continue
            if value < CELL_VALUE_MIN or value > CELL_VALUE_MAX:
                return FailureResponse(
                    code="E004",
                    message="Cell value must be 0 or between 1 and 16.",
                )
            if value in seen:
                return FailureResponse(
                    code=ERR_DUPLICATE_VALUE_CODE,
                    message="Duplicate non-zero value is not allowed.",
                )
            seen.add(value)
    return None


def serialize_api_result(result: SuccessResponse | str) -> str:
    """Serialize API Result DTO or semantic error token for Golden Master."""
    if isinstance(result, SuccessResponse):
        return f"Output:\n{result.data}"
    return f"Error:\n{result}"


def capture_scenario(scenario: GoldenScenario) -> str:
    """Capture one scenario block: Input grid plus Output or Error section."""
    lines = [f"[{scenario.key}]", "Input:", format_grid_input(scenario.grid)]

    content_failure = _validate_content(scenario.grid)
    if content_failure is not None:
        token = _BOUNDARY_CODE_TO_SEMANTIC.get(
            content_failure.code,
            content_failure.code,
        )
        lines.append(serialize_api_result(token))
        return "\n".join(lines) + "\n"

    try:
        solution = SolvePartialMagicSquare().resolve(scenario.grid)
    except UnsolvableDomainError:
        lines.append(serialize_api_result(SEMANTIC_NO_VALID_MAGIC_SQUARE))
        return "\n".join(lines) + "\n"

    dto = SuccessResponse(data=solution)
    lines.append(serialize_api_result(dto))
    return "\n".join(lines) + "\n"


def capture_scenario_by_key(scenario_key: str) -> str:
    """Capture a single scenario block by section key."""
    scenario = _SCENARIO_BY_KEY[scenario_key]
    return capture_scenario(scenario)


def capture_all_scenarios() -> dict[str, str]:
    """Return section key → captured block for every Golden Master scenario."""
    return {scenario.key: capture_scenario(scenario) for scenario in GOLDEN_SCENARIOS}


def render_golden_master() -> str:
    """Render the full baseline file with section separators."""
    blocks = [capture_all_scenarios()[scenario.key] for scenario in GOLDEN_SCENARIOS]
    return GOLDEN_SECTION_SEPARATOR.join(blocks) + "\n"
