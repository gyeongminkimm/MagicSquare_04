#!/usr/bin/env python
"""Generate or refresh tests/golden_master_expected.txt (Golden Master baseline).

Usage:
    python scripts/generate_golden_master.py
    python scripts/generate_golden_master.py --approve

Exit code 0 on success; writes UTF-8 baseline with LF newlines.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from tests.golden_master.approval import DEFAULT_GOLDEN_PATH, approve_golden_master  # noqa: E402
from tests.golden_master.capture import render_golden_master  # noqa: E402


def main() -> int:
    """Capture solver output and write Golden Master baseline."""
    parser = argparse.ArgumentParser(description="Generate Golden Master baseline file.")
    parser.add_argument(
        "--approve",
        action="store_true",
        help="Overwrite existing baseline (default: only create if missing).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_GOLDEN_PATH,
        help=f"Output path (default: {DEFAULT_GOLDEN_PATH}).",
    )
    args = parser.parse_args()

    actual = render_golden_master()
    path = approve_golden_master(
        actual,
        args.output,
        approve=args.approve or not args.output.is_file(),
    )
    print(f"Golden Master written: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
