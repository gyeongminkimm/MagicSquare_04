"""Approve pattern — auto-generate or diff Golden Master baseline."""

from __future__ import annotations

import difflib
from pathlib import Path

from tests.golden_master.capture import GOLDEN_SECTION_SEPARATOR, render_golden_master

DEFAULT_GOLDEN_PATH: Path = (
    Path(__file__).resolve().parent.parent / "golden_master_expected.txt"
)


def normalize_block(text: str) -> str:
    """Normalize scenario block to single trailing newline."""
    return text.rstrip("\n") + "\n"


def parse_golden_sections(content: str) -> dict[str, str]:
    """Split baseline file into section-key → block text."""
    stripped = content.rstrip("\n")
    if not stripped:
        return {}
    sections: dict[str, str] = {}
    for block in stripped.split(GOLDEN_SECTION_SEPARATOR):
        header = block.split("\n", maxsplit=1)[0]
        key = header.strip("[]")
        sections[key] = normalize_block(block)
    return sections


def format_golden_diff(expected: str, actual: str) -> str:
    """Return unified diff with --- expected / +++ actual labels."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
        )
    )


def approve_golden_master(
    actual: str,
    expected_path: Path | None = None,
    *,
    approve: bool = False,
) -> Path:
    """Write baseline when missing or approve=True; otherwise assert equality.

    Args:
        actual: Freshly captured Golden Master text.
        expected_path: Baseline file path (defaults to tests/golden_master_expected.txt).
        approve: When True, overwrite baseline with ``actual``.

    Returns:
        Path to the baseline file used.

    Raises:
        AssertionError: When baseline exists, approve is False, and content differs.
    """
    path = expected_path or DEFAULT_GOLDEN_PATH
    if approve or not path.is_file():
        path.write_text(actual, encoding="utf-8", newline="\n")
        return path

    expected = path.read_text(encoding="utf-8")
    if actual == expected:
        return path

    raise AssertionError(
        "Golden Master mismatch - re-run with GOLDEN_MASTER_APPROVE=1 to update baseline.\n"
        f"{format_golden_diff(expected, actual)}"
    )


def approve_scenario_block(
    scenario_key: str,
    actual_block: str,
    expected_path: Path | None = None,
    *,
    approve: bool = False,
) -> None:
    """Compare one scenario block; regenerate full baseline on approve or missing file.

    Args:
        scenario_key: Section key inside ``[scenario_key]`` header.
        actual_block: Captured block for this scenario.
        expected_path: Baseline file path.
        approve: When True, overwrite full baseline from current capture.

    Raises:
        AssertionError: When the scenario block differs from baseline.
    """
    path = expected_path or DEFAULT_GOLDEN_PATH
    if approve or not path.is_file():
        approve_golden_master(render_golden_master(), path, approve=True)
        return

    expected_content = path.read_text(encoding="utf-8")
    sections = parse_golden_sections(expected_content)
    expected_block = sections.get(scenario_key)

    if expected_block is None:
        approve_golden_master(render_golden_master(), path, approve=True)
        return

    if normalize_block(actual_block) == normalize_block(expected_block):
        return

    raise AssertionError(
        f"[GoldenMaster] {scenario_key} mismatch - "
        "re-run with GOLDEN_MASTER_APPROVE=1 to update baseline.\n"
        f"{format_golden_diff(normalize_block(expected_block), normalize_block(actual_block))}"
    )
