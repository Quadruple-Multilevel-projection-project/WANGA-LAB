"""Deterministic WANGA-to-formal-proof bridge; no symbol semantics are inferred."""
import hashlib, json, shutil, subprocess
from pathlib import Path
from .models import ProofObligation, Specification, Status, StructuralInput, VerificationResult

def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def _hash(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def structure_to_specification(data: StructuralInput) -> Specification:
    issues=[]
    source_ids=[s.source_id for s in data.sources]
    node_ids=[n.node_id for n in data.nodes]
    relation_ids=[r.relation_id for r in data.relations]
    known_sources=set(source_ids); known_nodes=set(node_ids)
    for label, values in (("SOURCE",source_ids),("NODE",node_ids),("RELATION",relation_ids)):
        if len(values)!=len(set(values)): issues.append("DUPLICATE_"+label+"_ID")
    if not data.structure_id.strip(): issues.append("STRUCTURE_ID_MISSING")
    for s in data.sources:
        if not all((s.source_id,s.uri,s.locator,s.content_sha256)): issues.append("SOURCE_INCOMPLETE:"+s.source_id)
        if len(s.content_sha256)!=64: issues.append("SOURCE_HASH_INVALID:"+s.source_id)
    nodes=[]
    for n in data.nodes:
        if not n.source_ids: issues.append("NODE_WITHOUT_PROVENANCE:"+n.node_id)
        for sid in n.source_ids:
            if sid not in known_sources: issues.append("NODE_SOURCE_UNKNOWN:"+n.node_id+":"+sid)
        if not n.formal_type: issues.append("NODE_TYPE_UNDEFINED:"+n.node_id)
        nodes.append({"node_id":n.node_id,"symbol":n.symbol,"formal_type":n.formal_type,"source_ids":list(n.source_ids)})
    relations=[]
    for r in data.relations:
        if r.source_node not in known_nodes or r.target_node not in known_nodes: issues.append("RELATION_ENDPOINT_UNKNOWN:"+r.relation_id)
        if not r.source_ids: issues.append("RELATION_WITHOUT_PROVENANCE:"+r.relation_id)
        for sid in r.source_ids:
            if sid not in known_sources: issues.append("RELATION_SOURCE_UNKNOWN:"+r.relation_id+":"+sid)
        if not r.formal_statement: issues.append("RELATION_SEMANTICS_UNDEFINED:"+r.relation_id)
        relations.append({"relation_id":r.relation_id,"source_node":r.source_node,"target_node":r.target_node,"relation_type":r.relation_type,"formal_statement":r.formal_statement,"source_ids":list(r.source_ids)})
    body={"structure_id":data.structure_id,"source_ids":sorted(source_ids),"nodes":nodes,"relations":relations,"assumptions":list(data.assumptions),"unresolved":sorted(set(issues))}
    digest=_hash(_canonical(body))
    return Specification("SPEC-"+digest[:12],data.structure_id,tuple(sorted(source_ids)),tuple(nodes),tuple(relations),data.assumptions,tuple(sorted(set(issues))),digest)

def review_specification(spec: Specification) -> VerificationResult:
    if spec.unresolved:
        return VerificationResult(Status.UNRESOLVED,spec.specification_sha256,None,reason=";".join(spec.unresolved))
    return VerificationResult(Status.REVIEW,spec.specification_sha256,None,reason="STRUCTURE_VALID; HUMAN_APPROVAL_REQUIRED")

def generate_proof_obligations(spec: Specification) -> tuple[ProofObligation,...]:
    if spec.unresolved: return ()
    out=[]
    for r in spec.relations:
        if r.get("formal_statement"):
            out.append(ProofObligation("PO-"+_hash(r["relation_id"])[:12],spec.specification_sha256,r["formal_statement"],tuple(r["source_ids"])))
    return tuple(out)

def compare_approved_specification(current: Specification, approved_sha256: str|None) -> VerificationResult:
    if not approved_sha256: return VerificationResult(Status.BLOCKED,current.specification_sha256,None,reason="NO_APPROVED_SPECIFICATION_HASH")
    if current.specification_sha256!=approved_sha256: return VerificationResult(Status.FAIL,current.specification_sha256,approved_sha256,reason="SPECIFICATION_HASH_MISMATCH")
    if current.unresolved: return VerificationResult(Status.UNRESOLVED,current.specification_sha256,approved_sha256,reason="UNRESOLVED_ITEMS")
    return VerificationResult(Status.PASS,current.specification_sha256,approved_sha256,reason="EXACT_APPROVED_SPECIFICATION_MATCH")

def reconstruct_and_audit(spec: Specification, original: StructuralInput) -> VerificationResult:
    rebuilt=structure_to_specification(original)
    if rebuilt.specification_sha256!=spec.specification_sha256:
        return VerificationResult(Status.FAIL,rebuilt.specification_sha256,spec.specification_sha256,reason="RECONSTRUCTION_MISMATCH")
    return VerificationResult(Status.PASS if not rebuilt.unresolved else Status.UNRESOLVED,rebuilt.specification_sha256,spec.specification_sha256,reason="DETERMINISTIC_RECONSTRUCTION_MATCH")

def verify_with_lean(lean_file: str|Path, current_specification_sha256: str, approved_specification_sha256: str|None, timeout_seconds: int=30) -> VerificationResult:
    if not approved_specification_sha256:
        return VerificationResult(Status.BLOCKED,current_specification_sha256,None,reason="NO_APPROVED_SPECIFICATION_HASH")
    if current_specification_sha256!=approved_specification_sha256:
        return VerificationResult(Status.FAIL,current_specification_sha256,approved_specification_sha256,reason="SPECIFICATION_HASH_MISMATCH")
    exe=shutil.which("lean")
    if not exe: return VerificationResult(Status.BLOCKED,current_specification_sha256,approved_specification_sha256,reason="LEAN_EXECUTABLE_NOT_FOUND")
    path=Path(lean_file)
    if not path.is_file(): return VerificationResult(Status.BLOCKED,current_specification_sha256,approved_specification_sha256,reason="LEAN_FILE_NOT_FOUND")
    command=(exe,str(path))
    try: run=subprocess.run(command,capture_output=True,text=True,timeout=timeout_seconds,check=False)
    except subprocess.TimeoutExpired: return VerificationResult(Status.BLOCKED,current_specification_sha256,approved_specification_sha256,command=command,reason="LEAN_TIMEOUT")
    return VerificationResult(Status.PASS if run.returncode==0 else Status.FAIL,current_specification_sha256,approved_specification_sha256,command,run.returncode,run.stdout,run.stderr,"LEAN_EXIT_ZERO" if run.returncode==0 else "LEAN_REJECTED_FILE")
