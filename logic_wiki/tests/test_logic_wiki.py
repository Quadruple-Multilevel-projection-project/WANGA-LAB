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
  manifest=json.loads((ROOT/'logic_wiki/data/wix_sync_manifest.json').read_text(encoding='utf-8'))
  catalog=json.loads((ROOT/'logic_wiki/data/articles.json').read_text(encoding='utf-8'))
  reconciliation=manifest['catalog_reconciliation']
  readback=manifest['readback_scope']
  catalog_article_count=len(catalog['articles'])
  catalog_source_count=len(catalog['sources'])
  catalog_relation_count=sum(len(x.get('relations',[])) for x in catalog['articles'])
  self.assertEqual(manifest['status'],'PUBLISHED_READ_BACK_PARTIAL')
  self.assertEqual(manifest['synced_article_count'],readback['homepage_entry_cards'])
  self.assertEqual(manifest['source_record_count'],readback['synced_source_record_count'])
  self.assertEqual(manifest['relation_link_count'],readback['synced_relation_link_count'])
  self.assertLessEqual(manifest['synced_article_count'],catalog_article_count)
  self.assertEqual(manifest['source_class_count'],len({x['type'] for x in catalog['sources']}))
  self.assertEqual(reconciliation['current_branch_catalog_article_count'],catalog_article_count)
  self.assertEqual(reconciliation['current_branch_source_record_count'],catalog_source_count)
  self.assertEqual(reconciliation['current_branch_relation_link_count'],catalog_relation_count)
  self.assertEqual(reconciliation['unsynced_article_delta'],catalog_article_count-manifest['synced_article_count'])
  self.assertEqual(reconciliation['unsynced_source_record_delta'],catalog_source_count-manifest['source_record_count'])
  self.assertEqual(reconciliation['unsynced_relation_link_delta'],catalog_relation_count-manifest['relation_link_count'])
  self.assertEqual(reconciliation['status'],'DRAFT_BRANCH_UNAPPROVED_NOT_SYNCED')
  self.assertTrue(reconciliation['readback_required'])
  self.assertEqual(manifest['main_page_card_count'],manifest['synced_article_count'])
  self.assertEqual(manifest['main_page_catalog_article_count'],manifest['synced_article_count'])
  self.assertEqual(manifest['research_catalog_article_count'],manifest['synced_article_count'])
  self.assertEqual(manifest['extended_topic_page_count'],10)
  ids=[x['id'] for x in manifest['extended_page_resources']]
  self.assertEqual(len(ids),10)
  self.assertEqual(len(ids),len(set(ids)))
  self.assertTrue(all(x.get('source_refs') for x in manifest['extended_page_resources']))
  self.assertTrue(manifest['all_extended_resources_have_source_or_explicit_local_boundary'])
 def tearDown(self):
  p=ROOT/'logic_wiki/generated-test'
  if p.exists():
   import shutil; shutil.rmtree(p)
if __name__=='__main__': unittest.main()