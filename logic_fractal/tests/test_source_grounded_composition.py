import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.build_source_grounded_fragments import build_candidates

class SourceGroundedCompositionTests(unittest.TestCase):
 def test_source_grounded_candidates_preserve_lineage_and_do_not_claim_entailment(self):
  artifact=build_candidates(ROOT)
  self.assertEqual(artifact["composition_candidate_count"],5)
  self.assertTrue(artifact["deterministic_rebuild"])
  self.assertEqual(artifact["semantic_entailments_claimed"],0)
  for candidate in artifact["candidates"]:
   self.assertEqual(candidate["status"],"CANDIDATE_NOT_SEMANTICALLY_VERIFIED")
   self.assertTrue(all(candidate["invariants_checked"].values()))
   self.assertEqual(candidate["semantic_status"],"NOT_YET_VERIFIED")
   self.assertEqual(candidate["fragment"]["composition"]["semantic_equivalence"],"NOT_ESTABLISHED")
   self.assertTrue(candidate["source_span_ids"])

if __name__=="__main__": unittest.main()
