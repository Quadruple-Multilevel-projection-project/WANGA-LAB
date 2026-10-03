import unittest

from core.pre_field import AdmissionState, FieldDefinition, PreField
from crypto.poc_generator import generate_cch
from validation.structural_audit import audit_record


class PreFieldTests(unittest.TestCase):
    def test_uninitialized_field_rejects_execution(self):
        field = PreField()
        with self.assertRaises(RuntimeError):
            field.admit({"value": "x"}, FieldDefinition("demo"))

    def test_explicit_numeric_boundary(self):
        field = PreField()
        definition = FieldDefinition("demo", allow_numeric=False)
        field.initialize(definition)
        self.assertFalse(field.admit({"value": 3}, definition))
        self.assertEqual(field.state.state, AdmissionState.REJECTED)


class IntegrityTests(unittest.TestCase):
    def test_cch_is_deterministic(self):
        payload = {"b": 2, "a": 1}
        self.assertEqual(generate_cch(payload), generate_cch({"a": 1, "b": 2}))

    def test_structural_audit(self):
        result = audit_record(
            {"id": "CASE-1", "source": "test", "validation_state": "UNVERIFIED"}
        )
        self.assertEqual(result.status, "STRUCTURALLY_VALID")
