"""[TAG][GoldenMaster] Magic Square solver Golden Master regression (GM-TC-01~05)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.golden_master.approval import approve_golden_master, approve_scenario_block
from tests.golden_master.capture import capture_scenario_by_key, render_golden_master
from tests.golden_master.contracts import (
    SEMANTIC_DUPLICATE_NUMBER,
    SEMANTIC_INVALID_BLANK_COUNT,
    SEMANTIC_NO_VALID_MAGIC_SQUARE,
    assert_error_contract,
    assert_int_six_format,
    assert_reverse_fallback_combination,
    assert_row_major_blank_order,
    assert_small_first_combination,
    assert_unsolvable_grid,
    parse_error_token,
    parse_success_output,
)
from tests.golden_master.scenarios import SCENARIO_BY_TC_ID

pytestmark = pytest.mark.golden_master


def _assert_golden_scenario(
    scenario_key: str,
    expected_path: Path,
    *,
    approve: bool,
) -> str:
    """Capture scenario, compare to baseline, return captured block."""
    actual_block = capture_scenario_by_key(scenario_key)
    approve_scenario_block(
        scenario_key,
        actual_block,
        expected_path,
        approve=approve or not expected_path.is_file(),
    )
    return actual_block


class TestGoldenMasterMagicSquare:
    """Golden Master approval tests — API Result DTO serialization vs baseline."""

    def test_gm_tc_01_normal_combination_success(
        self,
        golden_master_expected_path: Path,
        golden_master_approve: bool,
    ) -> None:
        """GM-TC-01: small-first combination success (F1 / TD-01)."""
        scenario = SCENARIO_BY_TC_ID["GM-TC-01"]
        block = _assert_golden_scenario(
            "normal_success",
            golden_master_expected_path,
            approve=golden_master_approve,
        )
        data = parse_success_output(block)
        assert_int_six_format(data)
        assert_row_major_blank_order(scenario.grid, data)
        assert_small_first_combination(scenario.grid, data)

    def test_gm_tc_02_reverse_combination_success(
        self,
        golden_master_expected_path: Path,
        golden_master_approve: bool,
    ) -> None:
        """GM-TC-02: reverse fallback success (F2 / TD-02)."""
        scenario = SCENARIO_BY_TC_ID["GM-TC-02"]
        block = _assert_golden_scenario(
            "reverse_success",
            golden_master_expected_path,
            approve=golden_master_approve,
        )
        data = parse_success_output(block)
        assert_int_six_format(data)
        assert_row_major_blank_order(scenario.grid, data)
        assert_reverse_fallback_combination(scenario.grid, data)

    def test_gm_tc_03_invalid_blank_count(
        self,
        golden_master_expected_path: Path,
        golden_master_approve: bool,
    ) -> None:
        """GM-TC-03: blank count != 2 → INVALID_BLANK_COUNT."""
        block = _assert_golden_scenario(
            "invalid_blank_count",
            golden_master_expected_path,
            approve=golden_master_approve,
        )
        assert_error_contract(parse_error_token(block), SEMANTIC_INVALID_BLANK_COUNT)

    def test_gm_tc_04_duplicate_number(
        self,
        golden_master_expected_path: Path,
        golden_master_approve: bool,
    ) -> None:
        """GM-TC-04: duplicate non-zero → DUPLICATE_NUMBER."""
        block = _assert_golden_scenario(
            "duplicate_number",
            golden_master_expected_path,
            approve=golden_master_approve,
        )
        assert_error_contract(parse_error_token(block), SEMANTIC_DUPLICATE_NUMBER)

    def test_gm_tc_05_no_valid_magic_square(
        self,
        golden_master_expected_path: Path,
        golden_master_approve: bool,
    ) -> None:
        """GM-TC-05: both assignments fail → NO_VALID_MAGIC_SQUARE."""
        scenario = SCENARIO_BY_TC_ID["GM-TC-05"]
        block = _assert_golden_scenario(
            "no_valid_magic_square",
            golden_master_expected_path,
            approve=golden_master_approve,
        )
        assert_error_contract(parse_error_token(block), SEMANTIC_NO_VALID_MAGIC_SQUARE)
        assert_unsolvable_grid(scenario.grid)

    def test_gm_full_baseline_file_matches(
        self,
        golden_master_expected_path: Path,
        golden_master_approve: bool,
    ) -> None:
        """Aggregate baseline: open(expected).read() vs render_golden_master()."""
        actual = render_golden_master()
        created = not golden_master_expected_path.is_file()
        approve_golden_master(
            actual,
            golden_master_expected_path,
            approve=golden_master_approve or created,
        )
        expected = golden_master_expected_path.read_text(encoding="utf-8")
        assert actual == expected
