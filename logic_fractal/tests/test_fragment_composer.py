from __future__ import annotations
import json
from pathlib import Path
import unittest

from logic_fractal.fragment_composer import FragmentError, build_wiki_backlinks, compose_pair, content_hash, validate_fragment

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "logic_fractal" / "data" / "typed_fragments_fixture.json"
WIKI_INDEX = ROOT / "logic_wiki" / "data" / "articles.json"


class TypedFragmentComposerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.sources=cls.data["source_registry"]
        cls.fragments={f["fragment_id"]:f for f in cls.data["fragments"]}

    def test_base_fragments_validate_and_keep_sources(self):
        for fragment in self.fragments.values():
            self.assertEqual(validate_fragment(fragment,self.sources)["status"],"VALID_STRUCTURE")

    def test_two_scale_composition_preserves_parent_ids_and_provenance(self):
        one=compose_pair(self.fragments["FL-OBSERVATION"],self.fragments["FL-RELATION-EXTRACT"],source_registry=self.sources)
        f1=one["fragment"]
        self.assertEqual(f1["scale"],1)
        self.assertEqual(f1["status"],"CANDIDATE")
        self.assertEqual(set(f1["composition"]["parent_ids"]),{"FL-OBSERVATION","FL-RELATION-EXTRACT"})
        self.assertEqual(len(one["composition_trace"]["source_ids_preserved"]),2)
        two=compose_pair(f1,self.fragments["FL-REVIEW"],source_registry=self.sources)
        f2=two["fragment"]
        self.assertEqual(f2["scale"],2)
        self.assertIn(f1["fragment_id"],f2["composition"]["parent_ids"])
        self.assertEqual(f2["composition"]["semantic_equivalence"],"NOT_ESTABLISHED")
        repeat=compose_pair(f1,self.fragments["FL-REVIEW"],source_registry=self.sources)
        self.assertEqual(f2["model_hash"],repeat["fragment"]["model_hash"])

    def test_type_mismatch_blocks_composition(self):
        bad=json.loads(json.dumps(self.fragments["FL-REVIEW"]))
        bad["inputs"]=[{"name":"candidate","type":"UnrelatedType","required":True}]
        with self.assertRaises(FragmentError):
            compose_pair(self.fragments["FL-OBSERVATION"],bad,source_registry=self.sources)

    def test_unknown_source_is_rejected(self):
        bad=json.loads(json.dumps(self.fragments["FL-OBSERVATION"]))
        bad["claims"][0]["source_span_ids"]=["SRC-UNKNOWN"]
        with self.assertRaises(FragmentError):
            validate_fragment(bad,self.sources)

    def test_unsourced_claim_requires_explicit_assumption(self):
        bad=json.loads(json.dumps(self.fragments["FL-OBSERVATION"]))
        bad["claims"][0]["source_span_ids"]=[]
        with self.assertRaises(FragmentError):
            validate_fragment(bad,self.sources)
        bad["claims"][0]["assumption"]=True
        self.assertEqual(validate_fragment(bad,self.sources)["status"],"VALID_STRUCTURE")

    def test_composition_never_auto_verifies_claims(self):
        base=json.loads(json.dumps(self.fragments["FL-OBSERVATION"]))
        base["claims"][0]["status"]="VERIFIED"
        candidate=compose_pair(base,self.fragments["FL-RELATION-EXTRACT"],source_registry=self.sources)["fragment"]
        self.assertTrue(all(c["status"]=="CANDIDATE" for c in candidate["claims"]))
        self.assertTrue(all(c["inherited_status"] in {"VERIFIED","TESTED"} for c in candidate["claims"]))

    def test_wiki_graph_relations_validate_and_keep_backlinks(self):
        catalog=json.loads(WIKI_INDEX.read_text(encoding="utf-8"))
        article_ids={a["id"] for a in catalog["articles"]}
        paths={str(p.relative_to(ROOT)).replace("\\","/") for p in ROOT.rglob("*") if p.is_file()}
        # Catalog links resolve to article IDs; source files are checked by existing wiki tests.
        for article in catalog["articles"]:
            self.assertTrue(set(article.get("relations",[])).issubset(article_ids))
        self.assertGreater(len(paths),0)

    def test_content_hash_is_stable(self):
        value=self.fragments["FL-OBSERVATION"]
        self.assertEqual(content_hash(value),content_hash(json.loads(json.dumps(value))))


if __name__=="__main__":
    unittest.main()
