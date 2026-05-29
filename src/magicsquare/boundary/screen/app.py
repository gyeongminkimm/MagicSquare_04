"""Magic Square 4×4 PyQt screen — composition root for UIBoundary."""

from __future__ import annotations

import argparse
import sys
from typing import TYPE_CHECKING

from magicsquare.boundary.constants import BLANK_CELL_VALUE, CELL_VALUE_MAX, GRID_DIMENSION
from magicsquare.boundary.schemas import FailureResponse, SuccessResponse
from magicsquare.boundary.screen.grid_defaults import DEFAULT_G1_GRID
from magicsquare.boundary.ui_boundary import UIBoundary
from magicsquare.control.solve_partial_magic_square import SolvePartialMagicSquare
from magicsquare.entity.exceptions import DomainError

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QSpinBox


WINDOW_TITLE = "Magic Square 4x4"
SOLVE_BUTTON_TEXT = "풀기"
HINT_TEXT = "0 = 빈칸 · 값 범위 0~16 · G1 기본 격자"


def _ensure_pyqt6() -> None:
    """Exit with install hint when PyQt6 is missing."""
    try:
        import PyQt6  # noqa: F401
    except ImportError:
        print(
            "PyQt6가 설치되어 있지 않습니다.\n"
            '  pip install -e ".[gui]"',
            file=sys.stderr,
        )
        raise SystemExit(1) from None


def create_boundary() -> UIBoundary:
    """Composition root: wire Control resolver into UIBoundary."""
    return UIBoundary(resolver=SolvePartialMagicSquare())


def _format_success_message(data: list[int]) -> str:
    """Format success envelope data for the result label."""
    parts = ", ".join(str(value) for value in data)
    return f"결과 (r1, c1, n1, r2, c2, n2): {parts}"


def _format_failure_message(message: str) -> str:
    """Format failure envelope message for the result label."""
    return f"오류: {message}"


class MagicSquareMainWindow:
    """Main window with 4×4 spin grid, solve button, and result label."""

    def __init__(self, boundary: UIBoundary) -> None:
        """Build UI widgets and connect solve action."""
        from PyQt6.QtCore import Qt
        from PyQt6.QtWidgets import (
            QGridLayout,
            QLabel,
            QMainWindow,
            QPushButton,
            QSpinBox,
            QVBoxLayout,
            QWidget,
        )

        self._boundary = boundary
        self._window = QMainWindow()
        self._window.setWindowTitle(WINDOW_TITLE)
        self._window.setMinimumSize(320, 360)

        central = QWidget()
        self._window.setCentralWidget(central)
        layout = QVBoxLayout(central)

        hint_label = QLabel(HINT_TEXT)
        hint_label.setWordWrap(True)
        layout.addWidget(hint_label)

        grid_layout = QGridLayout()
        self._spin_boxes: list[list[QSpinBox]] = []
        for row_index in range(GRID_DIMENSION):
            row_spins: list[QSpinBox] = []
            for col_index in range(GRID_DIMENSION):
                spin = QSpinBox()
                spin.setRange(BLANK_CELL_VALUE, CELL_VALUE_MAX)
                spin.setValue(DEFAULT_G1_GRID[row_index][col_index])
                spin.setMinimumWidth(52)
                spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
                grid_layout.addWidget(spin, row_index, col_index)
                row_spins.append(spin)
            self._spin_boxes.append(row_spins)
        layout.addLayout(grid_layout)

        solve_button = QPushButton(SOLVE_BUTTON_TEXT)
        solve_button.setMinimumHeight(36)
        solve_button.clicked.connect(self._on_solve_clicked)
        layout.addWidget(solve_button)

        self._result_label = QLabel("격자를 입력한 뒤 「풀기」를 누르세요.")
        self._result_label.setWordWrap(True)
        layout.addWidget(self._result_label)

    def show(self) -> None:
        """Display the main window."""
        self._window.show()

    def _read_grid(self) -> list[list[int]]:
        """Read current spin box values as int[4][4]."""
        return [
            [spin.value() for spin in row_spins]
            for row_spins in self._spin_boxes
        ]

    def _on_solve_clicked(self) -> None:
        """Invoke UIBoundary.solve and render success or failure text."""
        grid = self._read_grid()
        try:
            result = self._boundary.solve(grid)
        except DomainError as exc:
            self._result_label.setText(_format_failure_message(str(exc)))
            return
        if isinstance(result, FailureResponse):
            self._result_label.setText(_format_failure_message(result.message))
        elif isinstance(result, SuccessResponse):
            self._result_label.setText(_format_success_message(result.data))

    @property
    def qt_window(self) -> QMainWindow:
        """Underlying QMainWindow (for tests or hosting)."""
        return self._window


def run_verify_mode(boundary: UIBoundary) -> int:
    """Show grid=None validation result (AC-FR-01-01 manual check)."""
    from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

    app = QApplication(sys.argv)
    result = boundary.solve(None)

    window = QMainWindow()
    window.setWindowTitle(f"{WINDOW_TITLE} — verify")
    window.setMinimumSize(360, 120)
    central = QWidget()
    window.setCentralWidget(central)
    layout = QVBoxLayout(central)

    if isinstance(result, FailureResponse):
        text = _format_failure_message(result.message)
    else:
        text = "Unexpected success for grid=None"

    label = QLabel(text)
    label.setWordWrap(True)
    layout.addWidget(label)
    window.show()
    return app.exec()


def run_main_window(boundary: UIBoundary) -> int:
    """Launch the primary Magic Square puzzle UI."""
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    main_window = MagicSquareMainWindow(boundary)
    main_window.show()
    return app.exec()


def main(argv: list[str] | None = None) -> int:
    """Entry point for GUI application."""
    _ensure_pyqt6()

    parser = argparse.ArgumentParser(description="Magic Square 4×4 screen")
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Show grid=None failure envelope (diagnostic, not main UI)",
    )
    args = parser.parse_args(argv)

    boundary = create_boundary()
    if args.verify:
        return run_verify_mode(boundary)
    return run_main_window(boundary)


if __name__ == "__main__":
    raise SystemExit(main())
