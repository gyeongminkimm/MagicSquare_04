"""Track A RED skeleton — U-FLOW-02 extended (Report/09 §5.1, PRD AC-05).

Extends Report/08 dimension-only isolation to blank/range/duplicate invalid inputs.
"""

from __future__ import annotations

import pytest

from magicsquare.boundary.ui.magic_square_boundary import MagicSquareBoundary


class TestUFlow02ExecuteNeverCalled:
    """U-FLOW-02 — invalid input → SolveTwoBlankPuzzle.resolve / execute 0회."""

    def test_u_flow_02_zero_blanks_resolve_call_count_zero(self) -> None:
        # Given: TD-04 grid; mock_resolver spy on resolve()
        # boundary = MagicSquareBoundary(resolver=mock_resolver)

        # When: boundary.solve(grid)

        # Then: mock_resolver.resolve.call_count == 0
        pytest.fail(
            "RED: U-FLOW-02 — zero blanks → resolve() 0회 (AC-05, U-FLOW-02)"
        )

    def test_u_flow_02_three_blanks_resolve_call_count_zero(self) -> None:
        # Given: three-blank grid; spied resolver
        # When: boundary.solve(grid)
        # Then: call_count == 0
        pytest.fail(
            "RED: U-FLOW-02 — three blanks → resolve() 0회 (AC-05)"
        )

    def test_u_flow_02_out_of_range_resolve_call_count_zero(self) -> None:
        # Given: TD-06 (17); spied resolver
        # When: boundary.solve(grid)
        # Then: call_count == 0
        pytest.fail(
            "RED: U-FLOW-02 — value 17 → resolve() 0회 (AC-05, ES-03)"
        )

    def test_u_flow_02_duplicate_resolve_call_count_zero(self) -> None:
        # Given: TD-05 duplicate; spied resolver
        # When: boundary.solve(grid)
        # Then: call_count == 0
        pytest.fail(
            "RED: U-FLOW-02 — duplicate → resolve() 0회 (AC-05, ES-04)"
        )
