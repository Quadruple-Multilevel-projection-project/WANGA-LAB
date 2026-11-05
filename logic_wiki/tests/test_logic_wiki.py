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
  catalog=json.loads((ROOT/'logic_wiki/data/articles.json').read_text(encoding='utf-8'))
  self.assertEqual(report['article_count'],len(catalog['articles']))
  self.assertNotEqual(report['readiness_gate_status'],'CANDIDATE_RELEASE_READY_FOR_HUMAN_REVIEW')
 def test_wix_sync_manifest_records_stable_extended_resources(self):
  catalog=json.loads((ROOT/'logic_wiki/data/articles.json').read_text(encoding='utf-8'))
  manifest=json.loads((ROOT/'logic_wiki/data/wix_sync_manifest.json').read_text(encoding='utf-8'))
  self.assertEqual(manifest['synced_article_count'],len(catalog['articles']))
  self.assertEqual(manifest['source_record_count'],len(catalog['sources']))
  self.assertEqual(manifest['relation_link_count'],sum(len(a.get('relations',[])) for a in catalog['articles']))
  self.assertEqual(manifest['main_page_card_count'],len(catalog['articles']))
  self.assertEqual(manifest['extended_topic_page_count'],10)
  ids=[x['id'] for x in manifest['extended_page_resources']]
  self.assertEqual(len(ids),10)
  self.assertEqual(len(ids),len(set(ids)))
  self.assertTrue(all(x.get('source_refs') for x in manifest['extended_page_resources']))
  self.assertTrue(manifest['all_extended_resources_have_source_or_explicit_local_boundary'])

 def test_taxonomy_covers_catalog_and_declared_relations(self):
  catalog=json.loads((ROOT/'logic_wiki/data/articles.json').read_text(encoding='utf-8'))
  taxonomy=json.loads((ROOT/'logic_wiki/data/fractal_taxonomy.json').read_text(encoding='utf-8'))
  article_ids={x['id'] for x in catalog['articles']}
  node_ids={x['id'] for x in taxonomy['nodes']}
  source_ids={x['id'] for x in catalog['sources']}
  self.assertEqual(article_ids,node_ids)
  for node in taxonomy['nodes']:
   self.assertTrue(set(node.get('source_ids',[])).issubset(source_ids),node['id'])
   self.assertTrue(set(node.get('relation_ids',[])).issubset(node_ids),node['id'])
  self.assertEqual(taxonomy['validation']['article_count'],len(catalog['articles']))
  self.assertEqual(taxonomy['validation']['source_count'],len(catalog['sources']))
 def test_milot_higayon_gate_xiv_is_source_linked_and_bounded(self):
  data=json.loads((ROOT/'logic_wiki/data/articles.json').read_text(encoding='utf-8'))
  source=next(x for x in data['sources'] if x['id']=='SRC-RAMBAM-MILOT-HIGAYON-GATE-XIV')
  article=next(x for x in data['articles'] if x['id']=='milot-higayon-gate-xiv')
  self.assertEqual(article['sources'],[source['id']])
  self.assertEqual(article['status'],'SOURCE_SUPPORTED_SUMMARY')
  self.assertEqual(source['type'],'PRIMARY_TEXT_TRANSLATION')
  self.assertIn('783578',source['uri'])
  self.assertIn('unproofread',article['scope_note'].lower())
  self.assertIn('not a claim about Moreh Nevukhim chapter 14',article['scope_note'])

 def tearDown(self):
  p=ROOT/'logic_wiki/generated-test'
  if p.exists():
   import shutil; shutil.rmtree(p)
if __name__=='__main__': unittest.main()