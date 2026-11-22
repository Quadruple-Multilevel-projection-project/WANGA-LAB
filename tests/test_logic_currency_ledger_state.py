import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from business_brain.ledger_state import (
    LedgerStateTransitionError,
    apply_event,
    validate_cash_separation,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "logic-currency-ledger-state-v1.schema.json"
EXAMPLE_PATH = ROOT / "examples" / "logic-currency-ledger-state.v1.example.json"


def proposed_event(quantity):
    return {
        "event_type": "CREDIT_PROPOSED",
        "quantity": quantity,
        "unit": "LOGIC_CREDIT_INTERNAL",
        "review_status": "UNREVIEWED",
        "authorization": {"state": "PENDING"},
    }


def approved_event(quantity):
    return {
        "event_type": "CREDIT_APPROVED",
        "quantity": quantity,
        "unit": "LOGIC_CREDIT_INTERNAL",
        "review_status": "ACCEPTED",
        "authorization": {"state": "APPROVED"},
    }


class LogicCurrencyLedgerStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.example = json.loads(EXAMPLE_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def test_exact_aggregate_schema_accepts_draft_fixture(self):
        self.validator.validate(self.example)
        validate_cash_separation(self.example["cash_separation"])

    def test_schema_rejects_external_token_quantity(self):
        unsafe = copy.deepcopy(self.example)
        unsafe["balances"]["external_token_quantity"] = 1
        self.assertTrue(list(self.validator.iter_errors(unsafe)))

    def test_schema_rejects_internal_issuance_in_v1(self):
        unsafe = copy.deepcopy(self.example)
        unsafe["balances"]["issued_internal_quantity"] = 1
        self.assertTrue(list(self.validator.iter_errors(unsafe)))

    def test_schema_rejects_negative_planned_quantity(self):
        unsafe = copy.deepcopy(self.example)
        unsafe["balances"]["planned_quantity"] = -1
        self.assertTrue(list(self.validator.iter_errors(unsafe)))

    def test_unverified_cash_must_remain_null(self):
        unsafe = copy.deepcopy(self.example)
        unsafe["cash_separation"]["actual_cash_collected_minor_units"] = 1
        self.assertTrue(list(self.validator.iter_errors(unsafe)))
        with self.assertRaisesRegex(LedgerStateTransitionError, "must remain null"):
            validate_cash_separation(unsafe["cash_separation"])

    def test_verified_cash_margin_must_equal_collected_minus_costs(self):
        valid_cash = {
            "status": "VERIFIED",
            "currency": "USD",
            "actual_cash_collected_minor_units": 12500,
            "actual_cash_costs_paid_minor_units": 4500,
            "contribution_margin_minor_units": 8000,
        }
        validate_cash_separation(valid_cash)

        invalid_cash = dict(valid_cash)
        invalid_cash["contribution_margin_minor_units"] = 8001
        with self.assertRaisesRegex(LedgerStateTransitionError, "must equal actual cash collected"):
            validate_cash_separation(invalid_cash)

    def test_verified_cash_allows_negative_margin_without_relabeling_revenue(self):
        cash = {
            "status": "VERIFIED",
            "currency": "EUR",
            "actual_cash_collected_minor_units": 1000,
            "actual_cash_costs_paid_minor_units": 1500,
            "contribution_margin_minor_units": -500,
        }
        validate_cash_separation(cash)

    def test_proposal_increases_planned_only(self):
        balances = {
            "planned_quantity": 0,
            "approved_quantity": 0,
            "issued_internal_quantity": 0,
            "external_token_quantity": 0,
        }
        updated = apply_event(balances, proposed_event(5))
        self.assertEqual(updated["planned_quantity"], 5)
        self.assertEqual(updated["approved_quantity"], 0)
        self.assertEqual(updated["issued_internal_quantity"], 0)
        self.assertEqual(updated["external_token_quantity"], 0)
        self.assertEqual(balances["planned_quantity"], 0)

    def test_approval_moves_quantity_from_planned_to_approved(self):
        balances = {
            "planned_quantity": 5,
            "approved_quantity": 0,
            "issued_internal_quantity": 0,
            "external_token_quantity": 0,
        }
        updated = apply_event(balances, approved_event(3))
        self.assertEqual(updated["planned_quantity"], 2)
        self.assertEqual(updated["approved_quantity"], 3)
        self.assertEqual(updated["issued_internal_quantity"], 0)

    def test_approval_without_explicit_authorization_is_blocked(self):
        balances = {
            "planned_quantity": 5,
            "approved_quantity": 0,
            "issued_internal_quantity": 0,
            "external_token_quantity": 0,
        }
        event = approved_event(2)
        event["authorization"]["state"] = "PENDING"
        with self.assertRaisesRegex(LedgerStateTransitionError, "APPROVED authorization"):
            apply_event(balances, event)

    def test_approval_cannot_exceed_planned_quantity(self):
        balances = {
            "planned_quantity": 2,
            "approved_quantity": 0,
            "issued_internal_quantity": 0,
            "external_token_quantity": 0,
        }
        with self.assertRaisesRegex(LedgerStateTransitionError, "exceeds planned"):
            apply_event(balances, approved_event(3))

    def test_internal_or_external_issuance_is_blocked(self):
        balances = {
            "planned_quantity": 0,
            "approved_quantity": 0,
            "issued_internal_quantity": 0,
            "external_token_quantity": 0,
        }
        with self.assertRaisesRegex(LedgerStateTransitionError, "issuance is blocked"):
            apply_event(balances, {
                "event_type": "CREDIT_ISSUED_INTERNAL",
                "quantity": 1,
                "unit": "LOGIC_CREDIT_INTERNAL",
                "review_status": "ACCEPTED",
                "authorization": {"state": "APPROVED"},
            })
        with self.assertRaisesRegex(LedgerStateTransitionError, "issuance is blocked"):
            apply_event(balances, {
                "event_type": "EXTERNAL_TOKEN_ISSUED",
                "quantity": 1,
                "unit": "LOGIC_CREDIT_INTERNAL",
                "review_status": "ACCEPTED",
                "authorization": {"state": "APPROVED"},
            })

    def test_reversal_is_blocked_until_semantics_are_defined(self):
        balances = {
            "planned_quantity": 0,
            "approved_quantity": 1,
            "issued_internal_quantity": 0,
            "external_token_quantity": 0,
        }
        with self.assertRaisesRegex(LedgerStateTransitionError, "reversal bucket semantics"):
            apply_event(balances, {
                "event_type": "CREDIT_REVERSED",
                "quantity": 1,
                "unit": "LOGIC_CREDIT_INTERNAL",
                "review_status": "REVERSED",
                "authorization": {"state": "APPROVED"},
            })


if __name__ == "__main__":
    unittest.main()
