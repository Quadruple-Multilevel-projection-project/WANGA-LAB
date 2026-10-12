import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
class LogicWikiTests(unittest.TestCase):
 def test_seed_data_has_stable_unique_ids(self):
  data=json.loads((ROOT/'logic_wiki/data/articles.json').read_text(encoding='utf-8'))
  ids=[x['id'] for x in data['articles']]
  self.assertEqual(len(ids),len(set(ids)))
  sids=[x['id'] for x in data['sources']]
  self.assertEqual(len(sids),len(set(sids)))
 def test_relations_and_sources_are_resolvable(self):
  data=json.loads((ROOT/'logic_wiki/data/articles.json').read_text(encoding='utf-8'))
  ids={x['id'] for x in data['articles']}; sources={x['id'] for x in data['sources']}
  for article in data['articles']:
   self.assertTrue(set(article['sources']).issubset(sources), article['id'])
   self.assertTrue(set(article['relations']).issubset(ids), article['id'])
 def test_readiness_gate_is_explicitly_provisional(self):
  gate=json.loads((ROOT/'logic_wiki/data/readiness_gate.json').read_text(encoding='utf-8'))
  self.assertEqual(gate['status'],'CONFIGURED_NOT_EMPIRICALLY_VALIDATED')
  self.assertGreater(gate['thresholds']['min_test_cases'],0)
 def test_generator_builds_pages_and_reports_gate(self):
  out=ROOT/'logic_wiki/generated-test'
  p=subprocess.run([sys.executable,str(ROOT/'scripts/build_logic_wiki.py'),'--root',str(ROOT),'--out',str(out)],capture_output=True,text=True)
  self.assertEqual(p.returncode,0,p.stdout+p.stderr)
  self.assertTrue((out/'index.html').exists())
  self.assertTrue((out/'INDEX.md').exists())
  report=json.loads((out/'readiness-report.json').read_text(encoding='utf-8'))
  self.assertEqual(report['article_count'],17)
  self.assertNotEqual(report['readiness_gate_status'],'CANDIDATE_RELEASE_READY_FOR_HUMAN_REVIEW')
 def tearDown(self):
  p=ROOT/'logic_wiki/generated-test'
  if p.exists():
   import shutil; shutil.rmtree(p)
if __name__=='__main__': unittest.main()