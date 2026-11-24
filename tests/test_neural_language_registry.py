import json
import unittest
from collections import Counter
from pathlib import Path

DATA = Path(__file__).parents[1] / "research" / "data" / "NEURAL_LANGUAGE_POINTS_AND_LINES_V1.json"


class NeuralLanguageRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_22_unique_letters_partitioned_once(self):
        letters = self.data["letters"]
        self.assertEqual(len(letters), 22)
        self.assertEqual(len({x["id"] for x in letters}), 22)
        self.assertEqual(len({x["hebrew"] for x in letters}), 22)
        memberships = [letter for root in self.data["roots"] for letter in root["letters"]]
        self.assertEqual(len(memberships), 22)
        self.assertEqual(Counter(memberships), Counter(x["hebrew"] for x in letters))
        for node in letters:
            matching = [r for r in self.data["roots"] if node["hebrew"] in r["letters"]]
            self.assertEqual(len(matching), 1)
            self.assertEqual(node["root_id"], matching[0]["id"])

    def test_expected_root_memberships(self):
        expected = {
            "ROOT-THROAT": ["א", "ה", "ח", "ע"],
            "ROOT-PALATE": ["ג", "י", "כ", "ק"],
            "ROOT-TONGUE": ["ד", "ט", "ל", "נ", "ת", "ר"],
            "ROOT-LIPS": ["ב", "ו", "מ", "פ"],
            "ROOT-TEETH": ["ז", "ס", "צ", "ש"],
        }
        self.assertEqual({r["id"]: r["letters"] for r in self.data["roots"]}, expected)

    def test_k22_counts_and_degree(self):
        graph = self.data["graph"]
        self.assertEqual(graph["vertex_count"], 22)
        self.assertEqual(len(graph["gates"]), 231)
        self.assertEqual(len(graph["transitions"]), 462)
        degree = Counter()
        pairs = set()
        for gate in graph["gates"]:
            self.assertNotEqual(gate["letter_a"], gate["letter_b"])
            pair = frozenset((gate["letter_a"], gate["letter_b"]))
            self.assertNotIn(pair, pairs)
            pairs.add(pair)
            degree[gate["letter_a"]] += 1
            degree[gate["letter_b"]] += 1
        self.assertEqual(len(pairs), 231)
        self.assertEqual(set(degree.values()), {21})

    def test_directed_reverse_links(self):
        transitions = {x["id"]: x for x in self.data["graph"]["transitions"]}
        self.assertEqual(len(transitions), 462)
        for item in transitions.values():
            reverse = transitions[item["reverse_id"]]
            self.assertEqual(reverse["from_letter"], item["to_letter"])
            self.assertEqual(reverse["to_letter"], item["from_letter"])
            self.assertEqual(reverse["reverse_id"], item["id"])
            self.assertEqual(reverse["gate_id"], item["gate_id"])

    def test_gate_endpoint_roots_match_nodes(self):
        roots = {letter["hebrew"]: letter["root_id"] for letter in self.data["letters"]}
        for gate in self.data["graph"]["gates"]:
            self.assertEqual(gate["root_a"], roots[gate["letter_a"]])
            self.assertEqual(gate["root_b"], roots[gate["letter_b"]])

    def test_undefined_operations_are_not_filled(self):
        for key in ("V1", "V2", "gate_payloads", "gate_weights", "braiding_rules",
                    "letter_arithmetic", "entry_exit_conditions", "exact_vector_geometry",
                    "processor_layer", "logical_semantics_for_231_gates"):
            self.assertIsNone(self.data["undefined"][key], key)
        for gate in self.data["graph"]["gates"]:
            self.assertIsNone(gate["V1"])
            self.assertIsNone(gate["V2"])
            self.assertIsNone(gate["gate_payload"])

    def test_spreadsheet_crosswalk_is_unresolved(self):
        rows = self.data["worksheet_crosswalk"]
        self.assertEqual(len(rows), 10)
        for row in rows:
            self.assertIsNone(row["gate_id"])
            self.assertIsNone(row["letter_ids"])
            self.assertIsNone(row["formal_rule"])
            self.assertEqual(row["status"], "SOURCE_EXTRACTED_UNRESOLVED_CROSSWALK")


if __name__ == "__main__":
    unittest.main()
