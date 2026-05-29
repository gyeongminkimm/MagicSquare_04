"""AC-FR-01-01 UI boundary flow — resolve isolation (U-FLOW)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from magicsquare.boundary.schemas import FailureResponse
from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare

from tests.boundary.conftest import INVALID_SIZE_CODE, INVALID_SIZE_MESSAGE


@pytest.fixture
def mock_partial_resolver() -> MagicMock:
    """Injected control resolver double (resolve() spy target)."""
    return MagicMock(spec=SolvePartialMagicSquare)


@pytest.fixture
def ui_boundary(mock_partial_resolver: MagicMock) -> UIBoundary:
    """UIBoundary SUT with mocked SolvePartialMagicSquare injected."""
    return UIBoundary(resolver=mock_partial_resolver)


class TestResolveIsolation:
    """AC-FR-01-01 — invalid grid must not call SolvePartialMagicSquare.resolve()."""

    def test_none_grid_resolve_never_called_spy(
        self,
        ui_boundary: UIBoundary,
        mock_partial_resolver: MagicMock,
    ) -> None:
        # AC-FR-01-01
        # Given: None grid and spied resolve()
        grid = None

        # When: UIBoundary.solve is invoked
        result = ui_boundary.solve(grid)

        # Then: resolve() is never called; failure envelope returned
        mock_partial_resolver.resolve.assert_not_called()
        assert isinstance(result, FailureResponse)
        assert result.type == "ERROR"
        assert result.code == INVALID_SIZE_CODE
        assert result.message == INVALID_SIZE_MESSAGE
