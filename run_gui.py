#!/usr/bin/env python3
"""Launch Magic Square 4×4 PyQt GUI.

Usage:
    python run_gui.py
    python run_gui.py --verify
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure src/ is on path when run without editable install.
_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from magicsquare.boundary.screen.app import main

if __name__ == "__main__":
    raise SystemExit(main())
