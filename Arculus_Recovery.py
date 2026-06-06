#!/usr/bin/env python3
"""Compatibility launcher for Arculus Recovery.

Run without arguments or with ``--gui`` to open the PySide6 desktop app.
Pass ``--mnemonic`` and related flags to use the CLI derivation mode.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from arculus_recovery.cli import safe_main


if __name__ == "__main__":
    safe_main()
