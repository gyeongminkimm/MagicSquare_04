"""Golden Master (Approval) regression harness for Magic Square solver output."""

from tests.golden_master.approval import (
    approve_golden_master,
    approve_scenario_block,
    format_golden_diff,
)
from tests.golden_master.capture import capture_all_scenarios, render_golden_master

__all__ = [
    "approve_golden_master",
    "approve_scenario_block",
    "capture_all_scenarios",
    "format_golden_diff",
    "render_golden_master",
]
