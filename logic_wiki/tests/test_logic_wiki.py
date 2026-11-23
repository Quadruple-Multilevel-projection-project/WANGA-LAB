import json, subprocess, sys, unittest, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from scripts.build_logic_wiki import validate as validate_wiki
from scripts.run_logic_agents import wix_audit_state
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
  self.assertEqual(manifest['synced_article_count'],len(catalog['articles']))
  self.assertEqual(manifest['source_record_count'],len(catalog['sources']))
  self.assertEqual(manifest['source_class_count'],len({x['type'] for x in catalog['sources']}))
  self.assertEqual(manifest['relation_link_count'],sum(len(x.get('relations',[])) for x in catalog['articles']))
  self.assertEqual(manifest['main_page_card_count'],len(catalog['articles']))
  self.assertEqual(manifest['main_page_catalog_article_count'],len(catalog['articles']))
  self.assertEqual(manifest['research_catalog_article_count'],len(catalog['articles']))
  self.assertEqual(manifest['extended_topic_page_count'],10)
  ids=[x['id'] for x in manifest['extended_page_resources']]
  self.assertEqual(len(ids),10)
  self.assertEqual(len(ids),len(set(ids)))
  self.assertTrue(all(x.get('source_refs') for x in manifest['extended_page_resources']))
  self.assertTrue(manifest['all_extended_resources_have_source_or_explicit_local_boundary'])

 def test_unknown_core_contradictions_block_zero_gate(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)
   data=root/'logic_wiki'/'data'
   data.mkdir(parents=True)
   (data/'articles.json').write_text(json.dumps({
    'articles':[{'id':'a1','title':'A1','category':'test','kind':'ESTABLISHED_REFERENCE','status':'INDEXED','definition':'A bounded test entry.','scope_note':'Test-only scope.','sources':['s1'],'relations':[]}],
    'sources':[{'id':'s1','uri':'https://example.org/source','status':'INDEXED','type':'REFERENCE'}]
   }),encoding='utf-8')
   thresholds={
    'min_source_records':0,'min_source_classes':0,'min_logic_units_with_provenance':0,
    'min_composition_rules_with_contracts':0,'min_counterexample_cases':0,'min_test_cases':0,
    'min_benchmark_suites':0,'min_independent_review_cycles':0,
    'unresolved_dangling_source_refs':0,'unresolved_duplicate_stable_ids':0,
    'critical_core_contradictions':0,'deterministic_build_required':False,
    'holdout_split_required':False,'mirror_review_required':False
   }
   (data/'readiness_gate.json').write_text(json.dumps({
    'gate_id':'FIRST_MODEL_ALPHA','status':'CONFIGURED_NOT_EMPIRICALLY_VALIDATED','thresholds':thresholds
   }),encoding='utf-8')
   (data/'agent_registry.json').write_text(json.dumps({'agents':[{'id':'test-agent'}]}),encoding='utf-8')
   (data/'research_metrics.json').write_text(json.dumps({'critical_core_contradictions':None}),encoding='utf-8')
   _,_,report=validate_wiki(root)
   self.assertIsNone(report['observed']['critical_core_contradictions'])
   self.assertFalse(report['checks']['critical_core_contradictions'])
   self.assertIn('critical_core_contradictions',report['missing_requirements'])

 def test_wix_audit_surfaces_readback_without_claiming_publication(self):
  state=wix_audit_state({
   'status':'PUBLISHED_READ_BACK_PARTIAL',
   'current_cycle_sync_status':'READ_BACK_VERIFIED_NO_UPLOAD_NO_CATALOG_DELTA',
   'last_attempt':{
    'site_id':'9d15d5e8-ebae-4660-8092-81f1fc817509',
    'site_id_resolution':'RESOLVED_EXACT_HOST_MATCH',
    'read_back_performed':True,
    'publication_performed':False
   }
  })
  self.assertEqual(state['status'],'READ_BACK_VERIFIED_NO_UPLOAD')
  self.assertTrue(state['read_back_performed'])
  self.assertFalse(state['publication_performed'])
  self.assertEqual(state['current_cycle_sync_status'],'READ_BACK_VERIFIED_NO_UPLOAD_NO_CATALOG_DELTA')

 def tearDown(self):
  p=ROOT/'logic_wiki/generated-test'
  if p.exists():
   import shutil; shutil.rmtree(p)
if __name__=='__main__': unittest.main()