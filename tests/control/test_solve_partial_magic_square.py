"""Control — SolvePartialMagicSquare orchestration (Track B, no Entity mock)."""

from __future__ import annotations

from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare

from tests.entity.grid_fixtures import GRID_G1


class TestSolvePartialMagicSquareResolve:
    """Control resolve() wires locate → find → solve (FR-05)."""

    def test_resolve_g1_returns_int_six_vector(self) -> None:
        # Given: G1 validated puzzle grid (F2 / TD-02)
        grid = GRID_G1
        use_case = SolvePartialMagicSquare()

        # When: resolve orchestrates domain services
        result = use_case.resolve(grid)

        # Then: F2 contract int[6] — [2,2,10,3,3,7] (Report/02, I-O2)
        assert result == [2, 2, 10, 3, 3, 7]
        assert len(result) == 6
