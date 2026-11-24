import unittest
from wflvb import *
class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.src=SourceRef("SRC-1","https://example.invalid/source","section-1","a"*64)
        self.data=StructuralInput("S",(self.src,),(LogicNode("A","Aleph",("SRC-1",),"Symbol"),LogicNode("B","Bet",("SRC-1",),"Symbol")),(Relation("R1","A","B","pair",("SRC-1",),"True"),),("Symbols are opaque identifiers.",))
    def test_compile_and_obligation(self):
        spec=structure_to_specification(self.data)
        self.assertEqual(spec.unresolved,())
        self.assertEqual(len(generate_proof_obligations(spec)),1)
        self.assertEqual(review_specification(spec).status,Status.REVIEW)
    def test_missing_semantics_unresolved(self):
        bad=StructuralInput("S",(self.src,),(LogicNode("A","Aleph",("SRC-1",),"Symbol"),),(Relation("R","A","A","self",("SRC-1",),None),))
        spec=structure_to_specification(bad)
        self.assertIn("RELATION_SEMANTICS_UNDEFINED:R",spec.unresolved)
        self.assertEqual(generate_proof_obligations(spec),())
    def test_approval_hash_gate(self):
        spec=structure_to_specification(self.data)
        self.assertEqual(compare_approved_specification(spec,spec.specification_sha256).status,Status.PASS)
        self.assertEqual(compare_approved_specification(spec,"0"*64).status,Status.FAIL)
    def test_reconstruction(self):
        spec=structure_to_specification(self.data)
        self.assertEqual(reconstruct_and_audit(spec,self.data).status,Status.PASS)
if __name__=="__main__": unittest.main()
