from __future__ import annotations
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from wanga_x_v1.engine import append_rollback_frame, build_blueprint, detect_provider_state, load_catalog, normalize_requirement, workspace_state

EXAMPLE = ROOT / "wanga_x_v1" / "examples" / "logic_model_builder_requirement.json"


class WangaXBlueprintTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog()
        self.requirement = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_wanga_x_causal_chain_is_materialized(self):
        result = build_blueprint(self.requirement, repo_root=ROOT, catalog=self.catalog, provider_state=detect_provider_state({}))
        self.assertEqual(result["system"], "WANGA-X Requirement-Driven Blueprint Engine V1")
        self.assertGreater(len(result["required_neural_computation"]), 0)
        stages = [frame["stage"] for frame in result["construction_frames"]]
        self.assertEqual(stages[:5], [
            "REQUIREMENT_CAPTURED", "REQUIREMENT_NORMALIZED", "REQUIRED_COMPUTATION_DERIVED",
            "ARCHITECTURE_CANDIDATES_RANKED", "BLUEPRINT_GENERATED"
        ])
        self.assertEqual(result["verification"]["status"], "PASS")

    def test_different_requirements_generate_different_component_sets(self):
        logic = {"goal":"Build a formal logic model and test its derivations.", "task_kind":"logic_model_builder",
                 "input_types":["structured_requirements"], "required_capabilities":["logic_language_compilation","symbolic_inference"]}
        drift = {"goal":"Compare versions, identify structural changes, classify possible drift.",
                 "task_kind":"document_drift_analysis", "input_types":["source_records"],
                 "required_capabilities":["version_comparison","structural_diff","drift_classification"]}
        a = build_blueprint(logic, repo_root=ROOT, catalog=self.catalog, provider_state=detect_provider_state({}))
        b = build_blueprint(drift, repo_root=ROOT, catalog=self.catalog, provider_state=detect_provider_state({}))
        set_a, set_b = set(a["blueprint"]["component_order"]), set(b["blueprint"]["component_order"])
        self.assertNotEqual(set_a, set_b)
        self.assertIn("logic_native_compiler", set_a)
        self.assertIn("drift_forensics", set_b)

    def test_neural_runtime_is_reported_as_blocked_not_fabricated(self):
        result = build_blueprint(self.requirement, repo_root=ROOT, catalog=self.catalog, provider_state=detect_provider_state({}))
        self.assertIn("neural_runtime_materialization", result["blueprint"]["missing_capabilities"])
        self.assertTrue(any(x["component_id"] == "neural_runtime_materializer" for x in result["blueprint"]["planned_unbound_components"]))
        contract = result["blueprint"]["materialization_contract"]
        self.assertFalse(contract["actual_neural_weights_generated"])
        self.assertFalse(contract["live_model_endpoint_created"])
        self.assertEqual(result["build_status"], "BLUEPRINT_INCOMPLETE_REQUIRED_CAPABILITY_BLOCKED")

    def test_natural_language_needs_configured_model_endpoint(self):
        req = {"goal":"Interpret free-form language and construct logic models.", "task_kind":"logic_model_builder",
               "input_types":["natural_language"], "required_capabilities":["candidate_model_generation"]}
        result = build_blueprint(req, repo_root=ROOT, catalog=self.catalog, provider_state=detect_provider_state({}))
        self.assertIn("natural_language_requirement_interpretation", result["blueprint"]["missing_capabilities"])
        self.assertTrue(any(x["component_id"] == "llm_model_proposer" for x in result["blueprint"]["planned_unbound_components"]))

    def test_dependency_closure_and_structural_verification(self):
        result = build_blueprint(self.requirement, repo_root=ROOT, catalog=self.catalog, provider_state=detect_provider_state({}))
        self.assertEqual(result["verification"]["status"], "PASS")
        selected = set(result["blueprint"]["component_order"])
        lookup = {item["id"]: item for item in self.catalog["components"]}
        for component_id in selected:
            self.assertTrue(set(lookup[component_id]["dependencies"]).issubset(selected))

    def test_blueprint_hash_is_reproducible(self):
        a = build_blueprint(self.requirement, repo_root=ROOT, catalog=self.catalog, provider_state=detect_provider_state({}))
        b = build_blueprint(self.requirement, repo_root=ROOT, catalog=self.catalog, provider_state=detect_provider_state({}))
        self.assertEqual(a["blueprint"]["blueprint_hash_sha256"], b["blueprint"]["blueprint_hash_sha256"])

    def test_rollback_appends_frame_without_mutating_history(self):
        result = build_blueprint(self.requirement, repo_root=ROOT, catalog=self.catalog, provider_state=detect_provider_state({}))
        old_frames = json.loads(json.dumps(result["construction_frames"]))
        updated = append_rollback_frame(result, "F2", "Try another architecture from the computation frame.")
        self.assertEqual(result["construction_frames"], old_frames)
        self.assertEqual(len(updated["construction_frames"]), len(old_frames) + 1)
        rollback = updated["construction_frames"][-1]
        self.assertEqual(rollback["event_type"], "ROLLBACK_AND_BRANCH")
        self.assertEqual(rollback["state"]["rollback_target_frame_id"], "F2")
        self.assertEqual(updated["construction_frames"][-2]["frame_hash"], rollback["parent_frame_hash"])

    def test_unknown_capability_is_not_silently_accepted(self):
        with self.assertRaises(ValueError):
            normalize_requirement({"goal":"test", "task_kind":"custom", "required_capabilities":["magic_unverified_capability"]}, self.catalog)

    def test_inventory_keeps_slots_separate_from_live_connections(self):
        state = workspace_state(ROOT)
        self.assertEqual(state["model_fabric"]["target_slots"], 5000)
        self.assertEqual(state["model_fabric"]["connected_slots"], 0)
        self.assertEqual(state["model_fabric"]["verified_slots"], 0)
        self.assertEqual(state["model_fabric"]["status"], "ARCHITECTURAL_SLOTS_NOT_LIVE_ENDPOINTS")

    def test_configured_endpoint_is_not_called_verified(self):
        providers = detect_provider_state({"WANGA_MODEL_BASE_URL":"http://localhost:11434/v1", "WANGA_MODEL_NAME":"fixture-model"})
        self.assertTrue(providers["llm"]["configured"])
        self.assertEqual(providers["llm"]["status"], "CONFIGURED_NOT_PROBED")
        self.assertEqual(providers["llm"]["health_probe_status"], "NOT_RUN")

    def test_three_candidate_architectures_are_preserved(self):
        result = build_blueprint({"goal":"compile a logic model", "task_kind":"logic_model_builder",
                                  "input_types":["structured_requirements"],
                                  "required_capabilities":["logic_language_compilation"]},
                                 repo_root=ROOT, catalog=self.catalog, provider_state=detect_provider_state({}))
        self.assertEqual(len(result["blueprint"]["candidate_architectures"]), 3)
        self.assertTrue(all("candidate_score" in candidate for candidate in result["blueprint"]["candidate_architectures"]))


if __name__ == "__main__":
    unittest.main()
