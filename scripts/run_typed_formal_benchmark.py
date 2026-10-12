#!/usr/bin/env python3
"""Run the small typed formal-fragment fixture suite and optionally write JSON output."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from formal_reasoning.typed_benchmark import run_typed_benchmark_suite


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", default=str(ROOT / "formal_reasoning/examples/typed_formal_cases.json"))
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)
    report = run_typed_benchmark_suite(Path(args.fixtures))
    output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        target = Path(args.out)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding="utf-8")
    print(json.dumps({k: report[k] for k in (
        "status", "fixture_status", "case_count", "passed_cases", "failed_cases", "semantic_status"
    )}, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
