"""Validate the exact AI231 Logic Currency Ledger aggregate-state schema and fixture."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "logic-currency-ledger-state-v1.schema.json"
EXAMPLE_PATH = ROOT / "examples" / "logic-currency-ledger-state.v1.example.json"


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    example = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate(example)

    invalid_cases = []
    external_token = copy.deepcopy(example)
    external_token["balances"]["external_token_quantity"] = 1
    invalid_cases.append(("external token quantity", external_token))

    issued_internal = copy.deepcopy(example)
    issued_internal["balances"]["issued_internal_quantity"] = 1
    invalid_cases.append(("internal issuance", issued_internal))

    unverified_cash = copy.deepcopy(example)
    unverified_cash["cash_separation"]["status"] = "VERIFIED"
    invalid_cases.append(("unverified cash marked verified", unverified_cash))

    for label, candidate in invalid_cases:
        if not list(validator.iter_errors(candidate)):
            raise SystemExit(f"FAIL: schema accepted invalid {label}")

    print(f"PASS: {SCHEMA_PATH.relative_to(ROOT)} validates {EXAMPLE_PATH.relative_to(ROOT)}")
    print("PASS: non-zero external tokens, internal issuance and unverified cash promotion are rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
