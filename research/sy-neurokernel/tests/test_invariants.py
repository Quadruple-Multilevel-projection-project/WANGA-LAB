import unittest
from sy_neurokernel import AlphabetKernel, RelationGraph, NeuroSymbolicEngine, Provenance

class KernelInvariantTests(unittest.TestCase):
    def test_hard_counts(self):
        k = AlphabetKernel()
        self.assertEqual(k.n_nodes, 22)
        self.assertEqual(k.n_gates, 231)
        self.assertEqual(k.n_directed, 462)
        self.assertEqual(k.n_full, 484)

    def test_graph_support(self):
        g = RelationGraph(AlphabetKernel())
        self.assertEqual(len(g.nodes), 22)
        self.assertEqual(len(g.gates), 231)
        self.assertEqual(len(g.directed), 462)
        self.assertTrue(g.supports((1, 2)))
        self.assertFalse(g.supports((1, 1)))

    def test_provenance_transition(self):
        e = NeuroSymbolicEngine(RelationGraph(AlphabetKernel()))
        s0 = e.initial_state()
        self.assertEqual(s0.provenance, Provenance.VERIFIED_FROM_SOURCE)
        s1 = e.step(s0)
        self.assertEqual(s1.provenance, Provenance.COMPUTATIONAL_HYPOTHESIS)
        self.assertEqual(len(s1.neural.embeddings), 22)
        self.assertEqual(len(s1.neural.embeddings[0]), 16)
        self.assertEqual(len(s1.neural.edge_scores), 462)

if __name__ == "__main__":
    unittest.main()
