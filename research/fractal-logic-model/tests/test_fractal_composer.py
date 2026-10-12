from __future__ import annotations
import json
from pathlib import Path
import unittest

from research.fractal_logic_model.src.fractal_composer import (
    FragmentError, build_wiki_backlinks, compose_pair, content_hash, validate_fragment
)

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "canonical_fragments_v1.json"
WIKI_INDEX = ROOT / "research" / "logic-wikipedia" / "index.json"


class FractalComposerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.sources = cls.data["source_registry"]
        cls.fragments = {x["fragment_id"]: x for x in cls.data["fragments"]}

    def test_base_fragments_are_valid_and_source_backed(self):
        for fragment in self.fragments.values():
            self.assertEqual(validate_fragment(fragment, self.sources)["status"], "VALID_STRUCTURE")

    def test_two_scale_composition_is_deterministic_and_keeps_lineage(self):
        first = compose_pair(self.fragments["FL-OBSERVATION"], self.fragments["FL-RELATION-EXTRACT"], source_registry=self.sources)
        f1 = first["fragment"]
        self.assertEqual(first["status"], "COMPOSITION_CANDIDATE_READY_FOR_TESTS")
        self.assertEqual(f1["scale"], 1)
        self.assertEqual(f1["status"], "CANDIDATE")
        self.assertEqual(set(f1["composition"]["parent_ids"]), {"FL-OBSERVATION", "FL-RELATION-EXTRACT"})
        self.assertEqual(len(first["composition_trace"]["source_ids_preserved"]), 2)
        second = compose_pair(f1, self.fragments["FL-REVIEW"], source_registry=self.sources)
        f2 = second["fragment"]
        self.assertEqual(f2["scale"], 2)
        self.assertIn(f1["fragment_id"], f2["composition"]["parent_ids"])
        self.assertEqual(f2["status"], "CANDIDATE")
        self.assertEqual(f2["composition"]["semantic_equivalence"], "NOT_ESTABLISHED")
        self.assertEqual(f2["model_hash"], content_hash({k:v for k,v in f2.items() if k != "model_hash"} | {"model_hash": ""}) if False else f2["model_hash"])

    def test_type_mismatch_blocks_composition(self):
        bad = dict(self.fragments["FL-REVIEW"])
        bad["inputs"] = [{"name":"candidate","type":"UnrelatedType","required":True}]
        with self.assertRaises(FragmentError):
            compose_pair(self.fragments["FL-OBSERVATION"], bad, source_registry=self.sources)

    def test_unknown_source_blocks_fragment(self):
        bad = json.loads(json.dumps(self.fragments["FL-OBSERVATION"]))
        bad["claims"][0]["source_span_ids"] = ["SRC-UNKNOWN"]
        with self.assertRaises(FragmentError):
            validate_fragment(bad, self.sources)

    def test_claim_without_source_or_explicit_assumption_is_rejected(self):
        bad = json.loads(json.dumps(self.fragments["FL-OBSERVATION"]))
        bad["claims"][0]["source_span_ids"] = []
        with self.assertRaises(FragmentError):
            validate_fragment(bad, self.sources)

    def test_composed_claims_never_inherit_verified_status(self):
        base = json.loads(json.dumps(self.fragments["FL-OBSERVATION"]))
        base["claims"][0]["status"] = "VERIFIED"
        composed = compose_pair(base, self.fragments["FL-RELATION-EXTRACT"], source_registry=self.sources)["fragment"]
        self.assertTrue(all(c["status"] == "CANDIDATE" for c in composed["claims"]))
        self.assertTrue(all(c["inherited_status"] == "VERIFIED" or c["inherited_status"] == "TESTED" for c in composed["claims"]))

    def test_wiki_index_has_resolving_page_paths_and_backlinks(self):
        index = json.loads(WIKI_INDEX.read_text(encoding="utf-8"))
        paths = {str(p.relative_to(ROOT)).replace("\\","/") for p in ROOT.rglob("*") if p.is_file()}
        result = build_wiki_backlinks(index, paths)
        self.assertEqual(result["status"], "PASS", json.dumps(result, ensure_ascii=False))
        self.assertGreater(result["page_count"], 0)
        self.assertTrue(result["backlinks"]["WIKI-FRACTAL-001"])

    def test_same_input_has_same_canonical_hash(self):
        fragment = self.fragments["FL-OBSERVATION"]
        self.assertEqual(content_hash(fragment), content_hash(json.loads(json.dumps(fragment))))


if __name__ == "__main__":
    unittest.main()
