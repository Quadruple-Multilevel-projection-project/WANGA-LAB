from __future__ import annotations

import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "logic_model_builder_v1"
sys.path.insert(0, str(ROOT))

from logic_model_builder_v1.builder import build_model, execute_model_artifact
from logic_model_builder_v1.logic_native_language import compile_lnl, parse_lnl
from logic_model_builder_v1.providers import OpenAICompatibleProvider, StructuredSpecProvider


SPEC_PATH = PACKAGE / "examples" / "site_change_spec.json"
LNL_PATH = PACKAGE / "examples" / "site_change.lnl"


def load_spec():
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


class LanguageTests(unittest.TestCase):
    def test_example_compiles_to_logic_graph(self):
        artifact = compile_lnl(LNL_PATH.read_text(encoding="utf-8"))
        self.assertEqual(artifact["status"], "COMPILED_FOR_REVIEW")
        self.assertEqual(artifact["language"], "lnl/0.1")
        self.assertGreater(len(artifact["model_graph"]["nodes"]), 0)
        self.assertEqual(len(artifact["execution_bundle"]["claims"]), 3)
        self.assertEqual(len(artifact["execution_bundle"]["rules"]), 1)
        self.assertEqual(artifact["semantic_status"], "NOT_YET_VERIFIED")

    def test_fact_without_declared_source_is_rejected(self):
        source = LNL_PATH.read_text(encoding="utf-8").replace(
            "evidence=E_REQUEST", "evidence=E_DOES_NOT_EXIST", 1
        )
        artifact = compile_lnl(source)
        self.assertEqual(artifact["status"], "REJECTED")
        self.assertIn("MISSING_SOURCE_REFERENCE", {x["code"] for x in artifact["diagnostics"]})

    def test_raw_fact_cannot_claim_verified(self):
        source = LNL_PATH.read_text(encoding="utf-8").replace(
            "status=TEST_FIXTURE evidence=E_REQUEST",
            "status=VERIFIED evidence=E_REQUEST", 1
        )
        artifact = compile_lnl(source)
        self.assertEqual(artifact["status"], "REJECTED")
        self.assertIn("RAW_FACT_CANNOT_BE_VERIFIED", {x["code"] for x in artifact["diagnostics"]})

    def test_unbound_rule_variable_is_rejected(self):
        source = LNL_PATH.read_text(encoding="utf-8").replace(
            "action.candidate_allowed($action)",
            "action.candidate_allowed($unbound)", 1
        )
        artifact = compile_lnl(source)
        self.assertEqual(artifact["status"], "REJECTED")
        self.assertIn("UNBOUND_CONSEQUENT_VARIABLE", {x["code"] for x in artifact["diagnostics"]})

    def test_unknown_constraint_is_rejected(self):
        source = LNL_PATH.read_text(encoding="utf-8") + "constraint pretend_formal_proof\n"
        artifact = compile_lnl(source)
        self.assertEqual(artifact["status"], "REJECTED")
        self.assertIn("UNSUPPORTED_CONSTRAINT", {x["code"] for x in artifact["diagnostics"]})

    def test_source_url_does_not_promote_claim_to_verified(self):
        artifact = compile_lnl(LNL_PATH.read_text(encoding="utf-8"))
        self.assertTrue(all(
            fact["epistemic_status"] != "VERIFIED"
            for fact in artifact["execution_bundle"]["claims"]
        ))
        self.assertEqual(artifact["status_contract"]["runtime_claims"], "DERIVED_NOT_VERIFIED")


class BuilderTests(unittest.TestCase):
    def test_structured_builder_constructs_candidate(self):
        result = build_model(load_spec(), StructuredSpecProvider())
        self.assertEqual(result["status"], "MODEL_BUILT_READY_FOR_REVIEW")
        self.assertEqual(result["model_artifact"]["model_name"], "site_change_logic")
        self.assertEqual(result["semantic_status"], "NOT_YET_VERIFIED")
        self.assertEqual(result["attempt_count"], 1)

    def test_built_model_executes_against_wanga_kernel_and_corpus(self):
        built = build_model(load_spec(), StructuredSpecProvider())
        result = execute_model_artifact(built["model_artifact"], repo_root=ROOT)
        self.assertEqual(result["status"], "GOALS_MET", json.dumps(result, ensure_ascii=False))
        self.assertEqual(result["runtime_status"], "COMPLETED")
        self.assertEqual(result["unmet_goals"], [])
        self.assertEqual(result["inference"]["corpus_context"]["status"], "LOADED")
        self.assertEqual(
            result["inference"]["derived_claims"][0]["status"],
            "DERIVED_NOT_VERIFIED",
        )

    def test_builder_retries_after_critic_rejection(self):
        valid = LNL_PATH.read_text(encoding="utf-8")
        invalid = valid.replace("evidence=E_REQUEST", "evidence=E_MISSING", 1)

        class SequenceProvider:
            name = "test-sequence-provider"
            def __init__(self):
                self.values = [invalid, valid]
                self.feedback = []
            def propose(self, specification, critique, attempt):
                self.feedback.append(list(critique))
                return self.values[min(attempt - 1, len(self.values) - 1)]

        provider = SequenceProvider()
        result = build_model(load_spec(), provider, max_attempts=3)
        self.assertEqual(result["status"], "MODEL_BUILT_READY_FOR_REVIEW")
        self.assertEqual(result["attempt_count"], 2)
        self.assertTrue(provider.feedback[1])
        self.assertIn("MISSING_SOURCE_REFERENCE", {x["code"] for x in result["attempt_log"][0]["errors"]})

    def test_llm_provider_requires_explicit_configuration(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                OpenAICompatibleProvider()

    def test_compiled_hash_is_stable(self):
        source = LNL_PATH.read_text(encoding="utf-8")
        self.assertEqual(
            compile_lnl(source)["model_hash_sha256"],
            compile_lnl(source)["model_hash_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
