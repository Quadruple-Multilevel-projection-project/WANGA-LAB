#!/usr/bin/env python3
"""Run the fixed formal-reasoning smoke suite and write a machine-readable report."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from formal_reasoning.benchmark import run_benchmark_suite


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", default=str(ROOT / "formal_reasoning/examples/benchmark_cases.json"))
    parser.add_argument("--out", default=str(ROOT / "research/reports/formal-reasoning/benchmark-latest.json"))
    args = parser.parse_args(argv)
    report = run_benchmark_suite(args.cases)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "case_count": report["case_count"],
        "passed": report["passed"],
        "failed": report["failed"],
        "scope": report["scope"],
        "verification_status": report["verification_status"],
        "report_path": str(out_path),
    }, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
