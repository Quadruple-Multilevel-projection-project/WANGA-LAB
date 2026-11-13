import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from logic_fractal.readiness import is_readiness_eligible
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
 def test_logic_unit_registry_has_unique_source_mapped_spans(self):
  registry=json.loads((ROOT/'logic_fractal/data/logic_units.json').read_text(encoding='utf-8'))
  self.assertEqual(registry['schema_version'],'wanga-logic-units/1.0')
  units=registry['units']
  self.assertEqual(len(units),11)
  self.assertEqual(len({u['unit_id'] for u in units}),len(units))
  self.assertEqual(len({u['source_span_id'] for u in units}),len(units))
  required=('unit_id','source_span_id','source_id','source_version','source_uri','exact_locator','literal_excerpt','language','permission_scope')
  for unit in units:
   self.assertTrue(all(isinstance(unit.get(k),str) and unit[k] for k in required),unit.get('unit_id'))

 def test_readiness_excludes_test_fixture_spans(self):
  self.assertTrue(is_readiness_eligible({'permission_scope':'PUBLIC_READ'},{'type':'PROJECT_RESEARCH'}))
  self.assertFalse(is_readiness_eligible({'permission_scope':'TEST_FIXTURE_NOT_ELIGIBLE_FOR_READINESS'},{'type':'PROJECT_RESEARCH'}))
  self.assertFalse(is_readiness_eligible({'permission_scope':'PUBLIC_READ'},{'type':'TEST_FIXTURE'}))

 def test_generator_builds_pages_and_reports_gate(self):
  out=ROOT/'logic_wiki/generated-test'
  p=subprocess.run([sys.executable,str(ROOT/'scripts/build_logic_wiki.py'),'--root',str(ROOT),'--out',str(out)],capture_output=True,text=True)
  self.assertEqual(p.returncode,0,p.stdout+p.stderr)
  self.assertTrue((out/'index.html').exists())
  self.assertTrue((out/'INDEX.md').exists())
  report=json.loads((out/'readiness-report.json').read_text(encoding='utf-8'))
  catalog=json.loads((ROOT/'logic_wiki/data/articles.json').read_text(encoding='utf-8'))
  self.assertEqual(report['article_count'],len(catalog['articles']))
  self.assertEqual(report['observed']['source_linked_articles'],len(catalog['articles']))
  registry=json.loads((ROOT/'logic_fractal/data/logic_units.json').read_text(encoding='utf-8'))
  self.assertEqual(report['observed']['logic_units_with_provenance'],len(registry['units']))
  self.assertEqual(report['observed']['test_fixture_logic_units_excluded'],0)
  contracts=json.loads((ROOT/'logic_fractal/data/composition_rules.json').read_text(encoding='utf-8'))['rules']
  expected=sum(1 for r in contracts if r.get('status','').startswith('ACTIVE') and r.get('inputs') and r.get('output') and r.get('invariants'))
  self.assertEqual(report['observed']['composition_rules_with_contracts'],expected)
  self.assertIsNone(report['observed']['critical_core_contradictions'])
  self.assertFalse(report['checks']['critical_core_contradictions'])
  self.assertNotEqual(report['readiness_gate_status'],'CANDIDATE_RELEASE_READY_FOR_HUMAN_REVIEW')
 def test_wix_sync_manifest_records_stable_extended_resources(self):
  manifest=json.loads((ROOT/'logic_wiki/data/wix_sync_manifest.json').read_text(encoding='utf-8'))
  self.assertEqual(manifest['synced_article_count'],18)
  self.assertEqual(manifest['extended_topic_page_count'],10)
  ids=[x['id'] for x in manifest['extended_page_resources']]
  self.assertEqual(len(ids),10)
  self.assertEqual(len(ids),len(set(ids)))
  self.assertTrue(all(x.get('source_refs') for x in manifest['extended_page_resources']))
  self.assertTrue(manifest['all_extended_resources_have_source_or_explicit_local_boundary'])
  self.assertEqual(manifest['latest_audit']['observed_source_catalog_article_count'],30)
  self.assertEqual(manifest['latest_audit']['difference_from_manifest'],3)
  self.assertTrue(manifest['sync_required'])
  self.assertFalse(manifest['latest_audit']['deployment_performed'])
 def tearDown(self):
  p=ROOT/'logic_wiki/generated-test'
  if p.exists():
   import shutil; shutil.rmtree(p)
if __name__=='__main__': unittest.main()