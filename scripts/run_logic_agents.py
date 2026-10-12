#!/usr/bin/env python3
"""Run bounded deterministic Logic Fractal agent roles over repository-visible data."""
from __future__ import annotations
import datetime, hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from logic_fractal.composer import build_candidate_model, load_contracts

def read(path): return json.loads(path.read_text(encoding='utf-8'))
def main():
 catalog=read(ROOT/'logic_wiki/data/articles.json')
 contracts=load_contracts(ROOT/'logic_fractal/data/composition_rules.json')
 evidence_dir=ROOT/'research/inbox/conversations'
 files=sorted(p for p in evidence_dir.rglob('*.json') if p.is_file())
 imported=[]; errors=[]
 for p in files:
  try:
   data=read(p)
   if not data.get('record_id') or not data.get('segments') or not data.get('source_type'): errors.append({'file':str(p.relative_to(ROOT)),'status':'BLOCKED_INVALID_INTAKE_SCHEMA'})
   else:
    raw=p.read_bytes()
    imported.append({'record_id':data['record_id'],'file':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(raw).hexdigest(),'segment_count':len(data['segments']),'status':'REGISTERED_NOT_SEMANTICALLY_VERIFIED'})
  except Exception as exc: errors.append({'file':str(p.relative_to(ROOT)),'status':'FAILED_PARSE','reason':str(exc)})
 model=build_candidate_model(catalog,contracts)
 source_ids={s['id'] for s in catalog['sources']}
 missing_sources=sorted({r for a in catalog['articles'] for r in a.get('sources',[]) if r not in source_ids})
 cycle_candidates=[]
 edges=model['graph']['edges']
 edge_set={(e['source'],e['target']) for e in edges}
 for a,b in sorted(edge_set):
  if a!=b and (b,a) in edge_set: cycle_candidates.append({'pair':[a,b],'status':'RECIPROCAL_EDGE_REVIEW_CANDIDATE'})
 agent_results=[
  {'agent':'conversation-collector','status':'COMPLETED_WITH_NO_EXPORTS' if not imported and not errors else 'COMPLETED','record_count':len(imported),'errors':errors,'boundary':'Only repository-visible export files are scanned; no private chat history is fetched.'},
  {'agent':'source-registrar','status':'PASS' if not missing_sources else 'FAIL','declared_sources':len(source_ids),'dangling_source_refs':missing_sources},
  {'agent':'logic-normalizer','status':'COMPLETED','article_nodes':len(model['graph']['nodes']),'declared_edges':len(edges),'semantic_status':'EDITORIAL_STRUCTURAL_MAP_ONLY'},
  {'agent':'fractal-composer','status':'COMPLETED','candidate_compositions':model['candidate_composition_count'],'status_contract':'CANDIDATE_COMPOSITION_NOT_SEMANTICALLY_VERIFIED'},
  {'agent':'mirror-reviewer','status':'REVIEW_REQUIRED','reciprocal_edge_candidates':cycle_candidates,'note':'Reciprocal links are review candidates, not proof of logical equivalence.'},
  {'agent':'benchmark-evaluator','status':'BLOCKED_NO_GROUNDED_BENCHMARKS','test_suites_recorded':0,'note':'Unit tests verify code contracts; no model-quality benchmark ground truth has been registered.'},
  {'agent':'wiki-curator','status':'READY_FOR_REVIEW','articles':len(catalog['articles'])},
  {'agent':'report-publisher','status':'MANIFEST_ONLY','wix_write_performed':False,'note':'This runtime writes a sync manifest; Wix deployment remains a separate approved, read-back-verified operation.'}
 ]
 report={'date':datetime.date.today().isoformat(),'run_status':'PASS' if not errors and not missing_sources else 'REVIEW','catalog_hash':hashlib.sha256(json.dumps(catalog,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'agent_count':len(agent_results),'agents':agent_results,'conversation_records_ingested':imported,'candidate_model':model,'first_model_gate':'NOT_READY_INTERNAL_CANDIDATE_ONLY','open_gaps':['Chat history is ingested only when available exports are committed.','Benchmark gate remains unmet until source-grounded test cases and holdout data are registered.','Candidate graph edges reflect the authored relation index and need semantic review.']}
 out=ROOT/'logic_wiki/generated/agent_cycle_report.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+chr(10),encoding='utf-8')
 print(json.dumps({'status':report['run_status'],'agents':len(agent_results),'conversation_records':len(imported),'compositions':model['candidate_composition_count'],'first_model_gate':report['first_model_gate'],'report':str(out.relative_to(ROOT))},ensure_ascii=False))
 return 0 if report['run_status']=='PASS' else 2
if __name__=='__main__': raise SystemExit(main())