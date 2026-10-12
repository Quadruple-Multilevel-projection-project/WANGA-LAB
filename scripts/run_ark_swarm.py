#!/usr/bin/env python3
"""Entry point for the integrated ARK-Swarm + Logic Trader research cycle."""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ark_swarm.coordinator import main

if __name__ == "__main__":
    raise SystemExit(main())
