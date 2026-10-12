import json, unittest
from pathlib import Path
from logic_fractal.composer import CompositionError, build_candidate_model, load_contracts

ROOT=Path(__file__).resolve().parents[2]

class LogicFractalComposerTests(unittest.TestCase):
 def setUp(self):
  self.catalog=json.loads((ROOT/"logic_wiki/data/articles.json").read_text(encoding="utf-8"))
  self.contracts=load_contracts(ROOT/"logic_fractal/data/composition_rules.json")

 def test_graph_edges_only_come_from_declared_relation_links(self):
  model=build_candidate_model(self.catalog,self.contracts)
  declared={(a["id"],target) for a in self.catalog["articles"] for target in a.get("relations",[])}
  self.assertTrue(all((e["source"],e["target"]) in declared for e in model["graph"]["edges"]))

 def test_all_nodes_keep_provenance(self):
  model=build_candidate_model(self.catalog,self.contracts)
  self.assertTrue(all(n["source_refs"] for n in model["graph"]["nodes"]))
  self.assertTrue(all(c["source_refs"] for c in model["candidate_fractals"]))

 def test_candidates_are_never_auto_verified(self):
  model=build_candidate_model(self.catalog,self.contracts)
  self.assertEqual(model["status"],"CANDIDATE_MAP_BUILT_NOT_RELEASED")
  self.assertTrue(all(c["status"]=="CANDIDATE_COMPOSITION_NOT_SEMANTICALLY_VERIFIED" for c in model["candidate_fractals"]))

 def test_composition_invariants_are_checked(self):
  model=build_candidate_model(self.catalog,self.contracts)
  self.assertGreater(model["candidate_composition_count"],0)
  self.assertTrue(all(all(c["invariants_checked"].values()) for c in model["candidate_fractals"]))

 def test_invalid_depth_is_rejected(self):
  with self.assertRaises(CompositionError):
   build_candidate_model(self.catalog,self.contracts,max_depth=8)

 def test_duplicate_or_dangling_relations_are_rejected(self):
  bad=json.loads(json.dumps(self.catalog))
  bad["articles"][0]["relations"].append("missing-logic-entry")
  with self.assertRaises(CompositionError):
   build_candidate_model(bad,self.contracts)

if __name__=="__main__": unittest.main()
