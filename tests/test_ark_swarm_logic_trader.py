from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ark_swarm.coordinator import DEFAULT_TASK, build_cycle
from ark_swarm.logic_trader import rank_logic_assets, trade_logic
from ark_swarm.swarm_state import make_event, merge_event_sets
from logic_fractal.composer import load_contracts

CATALOG_PATH = ROOT / "logic_wiki/data/articles.json"
CONTRACTS_PATH = ROOT / "logic_fractal/data/composition_rules.json"


def load_catalog():
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


class LogicTraderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog()
        cls.contracts = load_contracts(CONTRACTS_PATH)

    def test_trader_builds_source_linked_candidate_not_released_model(self):
        result = trade_logic(DEFAULT_TASK, self.catalog, self.contracts)
        package = result["logic_package"]
        self.assertEqual(result["status"], "CANDIDATE_PACKAGE_ASSEMBLED")
        self.assertTrue(package["member_articles"])
        self.assertTrue(package["sources"])
        self.assertEqual(package["status"], "INTERNAL_CANDIDATE_NOT_RELEASED")
        self.assertEqual(package["semantic_status"], "NOT_YET_VERIFIED")
        source_ids = {s["id"] for s in self.catalog["sources"]}
        self.assertTrue(all(set(a["source_refs"]).issubset(source_ids) for a in package["member_articles"]))

    def test_ranking_is_deterministic_and_does_not_claim_semantic_relevance(self):
        first = rank_logic_assets("logical fractal composition provenance verification", self.catalog)
        second = rank_logic_assets("logical fractal composition provenance verification", self.catalog)
        self.assertEqual(first["selected_assets"], second["selected_assets"])
        self.assertTrue(all(x["semantic_relevance"] == "NOT_ESTABLISHED" for x in first["selected_assets"]))
        self.assertTrue(all(x["selection_score"] >= 0 for x in first["selected_assets"]))

    def test_trader_compositions_preserve_source_and_candidate_status(self):
        result = trade_logic(DEFAULT_TASK, self.catalog, self.contracts)
        candidates = result["candidate_compositions"]
        self.assertTrue(candidates)
        for candidate in candidates:
            self.assertTrue(candidate["source_refs"])
            self.assertEqual(candidate["status"], "INTERNAL_CANDIDATE_NOT_RELEASED")
            self.assertEqual(candidate["semantic_entailment"], "NOT_ESTABLISHED")

    def test_task_changes_selection_fingerprint(self):
        a = trade_logic("evidence provenance source logic", self.catalog, self.contracts)
        b = trade_logic("navigation sensory motor connectome", self.catalog, self.contracts)
        self.assertNotEqual(a["ranking"]["task_sha256"], b["ranking"]["task_sha256"])

    def test_swarm_cycle_runs_existing_builder_and_keeps_release_gate_closed(self):
        result = build_cycle(DEFAULT_TASK, root=ROOT, include_existing_agent_suite=False)
        report = result["report"]
        model = result["model_candidate"]
        self.assertEqual(report["status"], "SWARM_CYCLE_PASS_CANDIDATE_BUILT", report["agents"])
        self.assertGreaterEqual(report["agent_count"], 6)
        self.assertEqual(model["status"], "INTERNAL_CANDIDATE_NOT_RELEASED")
        self.assertEqual(model["release_gate"]["decision"], "BLOCKED_INTERNAL_CANDIDATE_ONLY")
        self.assertFalse(model["release_gate"]["automatically_released"])
        self.assertEqual(model["semantic_status"], "NOT_YET_VERIFIED")
        self.assertEqual(model["formalization_queue_item"]["solver_execution_status"], "NOT_RUN_NO_FORMAL_AST")
        self.assertEqual(model["formalization_queue_item"]["semantic_status"], "NOT_YET_VERIFIED")
        self.assertEqual(report["typed_formal_benchmark_suite"]["case_count"], 7)
        self.assertEqual(report["typed_formal_benchmark_suite"]["passed_cases"], 7)
        self.assertEqual(report["typed_formal_benchmark_suite"]["semantic_status"], "NOT_YET_VERIFIED")
        self.assertEqual(report["event_set"]["merge_semantics"], "GROW_ONLY_SET_UNION")
        self.assertEqual(report["capability_boundaries"]["peer_to_peer_transport"], "NOT_IMPLEMENTED")

    def test_swarm_records_source_and_composition_checks(self):
        result = build_cycle(DEFAULT_TASK, root=ROOT, include_existing_agent_suite=False)
        agents = {x["agent_id"]: x for x in result["report"]["agents"]}
        self.assertTrue(agents["source-catalog-guard"]["passed"])
        self.assertTrue(agents["source-provenance-gate"]["passed"])
        self.assertTrue(agents["typed-fragment-composer"]["passed"])
        self.assertTrue(agents["mirror-counter-reader"]["passed"])
        self.assertIn("formal-propositional-benchmark", agents)
        self.assertTrue(agents["formal-propositional-benchmark"]["passed"], agents["formal-propositional-benchmark"])
        self.assertTrue(agents["formal-typed-fragment-benchmark"]["passed"], agents["formal-typed-fragment-benchmark"])
        self.assertTrue(agents["formalization-queue-gate"]["passed"], agents["formalization-queue-gate"])

    def test_event_set_merge_is_commutative_and_idempotent(self):
        a = make_event(cycle_id="C1", agent_id="logic-trader", event_type="RANKED", payload={"candidate_count": 8})
        b = make_event(cycle_id="C1", agent_id="fractal-composer", event_type="COMPOSED", payload={"count": 42})
        ab = merge_event_sets([a], [b])
        ba = merge_event_sets([b], [a])
        aa = merge_event_sets([a], [a])
        self.assertEqual(ab["events"], ba["events"])
        self.assertEqual(aa["event_count"], 1)
        self.assertEqual(ab["event_count"], 2)
        self.assertEqual(ab["event_set_sha256"], ba["event_set_sha256"])

    def test_event_id_conflict_is_rejected(self):
        a = make_event(cycle_id="C1", agent_id="x", event_type="DONE", payload={"v": 1})
        b = dict(a)
        b["payload"] = {"v": 2}
        with self.assertRaises(ValueError):
            merge_event_sets([a, b])


if __name__ == "__main__":
    unittest.main()
