"""Deterministic, evidence-aware symbolic reasoning kernel (stdlib only).

This is a bounded symbolic reasoning prototype, not a general language model.
It never treats a derived conclusion as a verified fact.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

LETTERS = tuple("אבגדהוזחטיכלמנסעפצקרשת")
ELIGIBLE_INPUT_STATUSES = {"OBSERVED", "TEST_FIXTURE"}
ACTIVE_RULE_STATUSES = {"ACTIVE", "ACTIVE_SPECIFIED"}


def _text(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True, order=True)
class Atom:
    subject: str
    predicate: str
    object: str
    polarity: bool = True

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "Atom":
        return cls(
            subject=_text(value.get("subject"), "atom.subject"),
            predicate=_text(value.get("predicate"), "atom.predicate"),
            object=_text(value.get("object"), "atom.object"),
            polarity=value.get("polarity", True) is True,
        )

    def signature(self) -> tuple[str, str, str]:
        return (self.subject, self.predicate, self.object)

    def key(self) -> tuple[str, str, str, bool]:
        return (*self.signature(), self.polarity)

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.object,
            "polarity": self.polarity,
        }


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    source_uri: str
    source_version: str = ""
    location: str = ""
    status: str = "UNREVIEWED"
    note: str = ""

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "Evidence":
        return cls(
            evidence_id=_text(value.get("id"), "evidence.id"),
            source_uri=_text(value.get("source_uri"), "evidence.source_uri"),
            source_version=str(value.get("source_version", "")),
            location=str(value.get("location", "")),
            status=str(value.get("status", "UNREVIEWED")).upper(),
            note=str(value.get("note", "")),
        )


@dataclass(frozen=True)
class Claim:
    claim_id: str
    atom: Atom
    epistemic_status: str
    evidence_refs: tuple[str, ...]

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "Claim":
        refs = value.get("evidence_refs", [])
        if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
            raise ValueError("claim.evidence_refs must be a list of strings")
        return cls(
            claim_id=_text(value.get("id"), "claim.id"),
            atom=Atom.from_dict(value.get("atom", {})),
            epistemic_status=str(value.get("epistemic_status", "UNKNOWN")).upper(),
            evidence_refs=tuple(refs),
        )


@dataclass(frozen=True)
class Rule:
    rule_id: str
    antecedents: tuple[Atom, ...]
    consequent: Atom
    status: str = "ACTIVE_SPECIFIED"
    source_refs: tuple[str, ...] = ()
    description: str = ""

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "Rule":
        antecedents = value.get("antecedents", [])
        if not isinstance(antecedents, list) or not antecedents:
            raise ValueError("rule.antecedents must be a non-empty list")
        refs = value.get("source_refs", [])
        if not isinstance(refs, list) or any(not isinstance(ref, str) for ref in refs):
            raise ValueError("rule.source_refs must be a list of strings")
        return cls(
            rule_id=_text(value.get("id"), "rule.id"),
            antecedents=tuple(Atom.from_dict(item) for item in antecedents),
            consequent=Atom.from_dict(value.get("consequent", {})),
            status=str(value.get("status", "ACTIVE_SPECIFIED")).upper(),
            source_refs=tuple(refs),
            description=str(value.get("description", "")),
        )


def combinatorial_counts(letters: Sequence[str] = LETTERS) -> dict[str, Any]:
    alphabet = tuple(letters)
    if len(alphabet) != 22 or len(set(alphabet)) != 22:
        raise ValueError("The 231-gate profile requires exactly 22 distinct symbols.")
    unordered_pairs = list(itertools.combinations(alphabet, 2))
    ordered_pairs = list(itertools.permutations(alphabet, 2))
    unordered_triples = list(itertools.combinations(alphabet, 3))
    ordered_distinct_triples = list(itertools.permutations(alphabet, 3))
    return {
        "letters": len(alphabet),
        "undirected_pairs": len(unordered_pairs),
        "directed_distinct_pairs": len(ordered_pairs),
        "unordered_distinct_triples": len(unordered_triples),
        "ordered_distinct_triples": len(ordered_distinct_triples),
        "ordered_triples_with_repetition": len(alphabet) ** 3,
        "formulas": {
            "undirected_pairs": "C(22,2)=22*21/2=231",
            "directed_distinct_pairs": "22*21=462",
            "unordered_distinct_triples": "C(22,3)=22*21*20/6=1540",
            "ordered_distinct_triples": "22*21*20=9240",
            "ordered_triples_with_repetition": "22^3=10648",
        },
        "note": (
            "1540 counts unordered sets of three distinct symbols. "
            "Ordered triples without repetition count 9240."
        ),
    }


def _variables(atom: Atom) -> set[str]:
    return {
        value for value in (atom.subject, atom.predicate, atom.object)
        if value.startswith("$")
    }


def _unify(pattern: Atom, value: Atom, bindings: Mapping[str, str]) -> dict[str, str] | None:
    if pattern.polarity != value.polarity:
        return None
    updated = dict(bindings)
    for key in ("subject", "predicate", "object"):
        expected = getattr(pattern, key)
        actual = getattr(value, key)
        if expected.startswith("$"):
            existing = updated.get(expected)
            if existing is not None and existing != actual:
                return None
            updated[expected] = actual
        elif expected != actual:
            return None
    return updated


def _instantiate(pattern: Atom, bindings: Mapping[str, str]) -> Atom:
    values = []
    for key in ("subject", "predicate", "object"):
        value = getattr(pattern, key)
        if value.startswith("$"):
            if value not in bindings:
                raise ValueError(f"Unbound variable in rule consequent: {value}")
            value = bindings[value]
        values.append(value)
    return Atom(values[0], values[1], values[2], pattern.polarity)


def run_bundle(bundle: Mapping[str, Any], *, max_rounds: int = 20, corpus_context: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Evaluate referenced input claims and run explicit Horn-style rules.

    The engine checks structural evidence references; it does not authenticate a
    source, interpret natural language, or independently certify claim truth.
    """
    if not isinstance(bundle, Mapping):
        raise ValueError("bundle must be a JSON object")
    if max_rounds < 1 or max_rounds > 100:
        raise ValueError("max_rounds must be in the range 1..100")

    evidence_items = [Evidence.from_dict(item) for item in bundle.get("evidence", [])]
    claims = [Claim.from_dict(item) for item in bundle.get("claims", [])]
    rules = [Rule.from_dict(item) for item in bundle.get("rules", [])]

    for collection, label, key_fn in (
        (evidence_items, "evidence", lambda x: x.evidence_id),
        (claims, "claims", lambda x: x.claim_id),
        (rules, "rules", lambda x: x.rule_id),
    ):
        keys = [key_fn(item) for item in collection]
        if len(keys) != len(set(keys)):
            raise ValueError(f"duplicate {label} identifier")

    evidence = {item.evidence_id: item for item in evidence_items}
    input_reports: list[dict[str, Any]] = []
    eligible_claims: list[Claim] = []
    unsupported_count = 0

    for claim in sorted(claims, key=lambda item: item.claim_id):
        missing = [ref for ref in claim.evidence_refs if ref not in evidence]
        if missing:
            state = "MISSING_EVIDENCE_REFERENCE"
            reason = "One or more cited evidence IDs do not exist in the supplied evidence registry."
        elif not claim.evidence_refs:
            state = "UNSUPPORTED_NO_EVIDENCE"
            reason = "No evidence reference is attached; this claim cannot act as a rule premise."
        elif claim.epistemic_status not in ELIGIBLE_INPUT_STATUSES:
            state = "NOT_ELIGIBLE_EPISTEMIC_STATUS"
            reason = "Only explicitly OBSERVED or TEST_FIXTURE inputs can seed this bounded rule engine."
        else:
            state = "INPUT_ELIGIBLE_WITH_REFERENCED_EVIDENCE"
            reason = (
                "The evidence reference exists. This is a structural eligibility check, "
                "not source authentication or independent verification of truth."
            )
            eligible_claims.append(claim)
        if state != "INPUT_ELIGIBLE_WITH_REFERENCED_EVIDENCE":
            unsupported_count += 1
        input_reports.append({
            "claim_id": claim.claim_id,
            "atom": claim.atom.to_dict(),
            "epistemic_status": claim.epistemic_status,
            "evidence_refs": list(claim.evidence_refs),
            "engine_status": state,
            "reason": reason,
        })

    facts: dict[tuple[str, str, str, bool], dict[str, Any]] = {}
    rule_predicates = {atom.predicate for rule in rules for atom in rule.antecedents}
    corpus_fact_ids: set[str] = set()
    corpus_facts_available = 0
    if corpus_context is not None:
        if corpus_context.get("status") != "LOADED":
            raise ValueError("corpus_context must be returned by load_corpus_context() with status LOADED")
        for item in corpus_context.get("facts", []):
            raw_atom = item.get("atom")
            atom_obj = raw_atom if isinstance(raw_atom, Atom) else Atom.from_dict(raw_atom)
            if atom_obj.predicate not in rule_predicates:
                continue
            fact_id = str(item["fact_id"])
            corpus_fact_ids.add(fact_id)
            corpus_facts_available += 1
            key = atom_obj.key()
            if key not in facts:
                facts[key] = {
                    "atom": atom_obj,
                    "fact_id": fact_id,
                    "kind": "CORPUS_STRUCTURAL",
                    "status": "CORPUS_STRUCTURE_NOT_SEMANTIC",
                    "source_claim_ids": [],
                    "evidence_refs": [],
                    "derivations": [],
                    "corpus_file": str(item.get("corpus_file", "")),
                }
    for claim in eligible_claims:
        key = claim.atom.key()
        if key not in facts:
            facts[key] = {
                "atom": claim.atom,
                "fact_id": f"INPUT-{claim.claim_id}",
                "kind": "INPUT",
                "status": "ELIGIBLE_INPUT_NOT_VERIFIED",
                "source_claim_ids": [],
                "evidence_refs": [],
                "derivations": [],
            }
        facts[key]["source_claim_ids"].append(claim.claim_id)
        facts[key]["evidence_refs"].extend(claim.evidence_refs)

    contradiction_signatures = _contradiction_signatures(facts)
    trace: list[dict[str, Any]] = []
    rule_list = sorted(
        [rule for rule in rules if rule.status in ACTIVE_RULE_STATUSES],
        key=lambda item: item.rule_id,
    )
    skipped_rules = [
        {"rule_id": rule.rule_id, "reason": f"Rule status is {rule.status}; not executed."}
        for rule in rules if rule.status not in ACTIVE_RULE_STATUSES
    ]
    fired: set[tuple[str, tuple[str, ...], tuple[str, str, str, bool]]] = set()
    derived_counter = 0
    stable = False

    for round_number in range(1, max_rounds + 1):
        contradiction_signatures = _contradiction_signatures(facts)
        available = [
            item for item in facts.values()
            if item["atom"].signature() not in contradiction_signatures
        ]
        available.sort(key=lambda item: (item["atom"].key(), item["fact_id"]))
        additions: list[tuple[Rule, Atom, list[dict[str, Any]]]] = []

        for rule in rule_list:
            partials: list[tuple[dict[str, str], list[dict[str, Any]]]] = [({}, [])]
            for antecedent in rule.antecedents:
                next_partials: list[tuple[dict[str, str], list[dict[str, Any]]]] = []
                for bindings, premises in partials:
                    for fact in available:
                        merged = _unify(antecedent, fact["atom"], bindings)
                        if merged is not None:
                            next_partials.append((merged, premises + [fact]))
                partials = next_partials
                if not partials:
                    break
            for bindings, premises in partials:
                try:
                    conclusion = _instantiate(rule.consequent, bindings)
                except ValueError as exc:
                    skipped_rules.append({"rule_id": rule.rule_id, "reason": str(exc)})
                    continue
                premise_ids = tuple(sorted({p["fact_id"] for p in premises}))
                signature = (rule.rule_id, premise_ids, conclusion.key())
                if signature in fired:
                    continue
                fired.add(signature)
                additions.append((rule, conclusion, premises))

        new_fact_added = False
        for rule, conclusion, premises in additions:
            trace_item = {
                "round": round_number,
                "rule_id": rule.rule_id,
                "rule_status": rule.status,
                "premise_fact_ids": sorted({p["fact_id"] for p in premises}),
                "premise_atoms": [p["atom"].to_dict() for p in premises],
                "conclusion": conclusion.to_dict(),
                "conclusion_epistemic_status": "DERIVED_NOT_VERIFIED",
                "source_refs": list(rule.source_refs),
                "rule_description": rule.description,
                "premise_corpus_files": sorted({p.get("corpus_file", "") for p in premises if p.get("corpus_file")}),
            }
            trace.append(trace_item)
            key = conclusion.key()
            if key not in facts:
                derived_counter += 1
                facts[key] = {
                    "atom": conclusion,
                    "fact_id": f"DERIVED-{derived_counter:03d}",
                    "kind": "DERIVED",
                    "status": "DERIVED_NOT_VERIFIED",
                    "source_claim_ids": [],
                    "evidence_refs": [],
                    "derivations": [],
                }
                new_fact_added = True
            facts[key]["derivations"].append({
                "rule_id": rule.rule_id,
                "premise_fact_ids": trace_item["premise_fact_ids"],
                "source_refs": list(rule.source_refs),
            })

        if not new_fact_added:
            stable = True
            break

    contradiction_signatures = _contradiction_signatures(facts)
    used_corpus_fact_ids = {
        fact_id
        for trace_item in trace
        for fact_id in trace_item["premise_fact_ids"]
        if fact_id.startswith("CORPUS-")
    }
    rendered_facts = []
    for item in sorted(facts.values(), key=lambda x: (x["atom"].key(), x["fact_id"])):
        if item.get("kind") == "CORPUS_STRUCTURAL" and item["fact_id"] not in used_corpus_fact_ids and item["atom"].signature() not in contradiction_signatures:
            continue
        atom = item["atom"]
        status = "CONTRADICTED_REQUIRES_REVIEW" if atom.signature() in contradiction_signatures else item["status"]
        rendered_facts.append({
            "fact_id": item["fact_id"],
            "atom": atom.to_dict(),
            "kind": item["kind"],
            "status": status,
            "source_claim_ids": sorted(set(item["source_claim_ids"])),
            "evidence_refs": sorted(set(item["evidence_refs"])),
            "derivations": item["derivations"],
            **({"corpus_file": item["corpus_file"]} if item.get("corpus_file") else {}),
        })

    contradictions = []
    by_signature: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for item in rendered_facts:
        by_signature.setdefault(Atom.from_dict(item["atom"]).signature(), []).append(item)
    for signature, items in sorted(by_signature.items()):
        polarities = {item["atom"]["polarity"] for item in items}
        if len(polarities) > 1:
            contradictions.append({
                "signature": list(signature),
                "fact_ids": [item["fact_id"] for item in items],
                "source_claim_ids": sorted({cid for item in items for cid in item["source_claim_ids"]}),
                "status": "CONTRADICTION_DETECTED_REQUIRES_REVIEW",
            })

    run_status = "COMPLETED" if stable and not contradictions else "REVIEW"
    if not stable:
        run_status = "ROUND_LIMIT_REACHED_REVIEW"
    return {
        "engine": "WANGA Symbolic Logic Kernel v1",
        "engine_type": "DETERMINISTIC_SYMBOLIC_PROTOTYPE_NOT_GENERAL_AI",
        "status": run_status,
        "input_claims": input_reports,
        "facts": rendered_facts,
        "derived_claims": [x for x in rendered_facts if x["kind"] == "DERIVED"],
        "contradictions": contradictions,
        "trace": trace,
        "skipped_rules": skipped_rules,
        "corpus_context": ({
            "status": "LOADED",
            "registry_status": corpus_context.get("registry_status", "NOT_RECORDED"),
            "registered_letters": corpus_context.get("counts", {}).get("letters", 0),
            "available_structural_facts_for_this_run": corpus_facts_available,
            "used_structural_facts": len(used_corpus_fact_ids),
            "semantic_status": "STRUCTURAL_COMBINATORICS_ONLY",
        } if corpus_context is not None else {"status": "NOT_LOADED"}),
        "summary": {
            "claims_received": len(claims),
            "evidence_records": len(evidence_items),
            "eligible_input_claims": len(eligible_claims),
            "unsupported_or_ineligible_claims": unsupported_count,
            "facts_after_reasoning": len(rendered_facts),
            "corpus_structural_facts_available": corpus_facts_available,
            "corpus_structural_facts_used": len(used_corpus_fact_ids),
            "derived_claims": sum(1 for x in rendered_facts if x["kind"] == "DERIVED"),
            "rules_received": len(rules),
            "active_rules": len(rule_list),
            "rule_firings": len(trace),
            "contradictions": len(contradictions),
            "fixed_point_reached": stable,
        },
        "limitations": [
            "No natural-language understanding or generation is implemented.",
            "Rules are explicit symbolic rules, not learned from text.",
            "Evidence IDs are checked structurally; source authenticity and claim truth are not independently verified.",
            "Derived conclusions are always labelled DERIVED_NOT_VERIFIED.",
            "This prototype does not establish hallucination prevention or general reasoning competence.",
        ],
    }


def _contradiction_signatures(facts: Mapping[tuple[str, str, str, bool], Mapping[str, Any]]) -> set[tuple[str, str, str]]:
    polarities: dict[tuple[str, str, str], set[bool]] = {}
    for item in facts.values():
        atom = item["atom"]
        polarities.setdefault(atom.signature(), set()).add(atom.polarity)
    return {signature for signature, values in polarities.items() if len(values) > 1}


def gate_action(request: Mapping[str, Any]) -> dict[str, Any]:
    action = _text(request.get("action"), "action")
    target = _text(request.get("target"), "target")
    allowed_actions = request.get("allowed_actions", [])
    allowed_targets = request.get("allowed_targets", [])
    if not isinstance(allowed_actions, list) or not isinstance(allowed_targets, list):
        raise ValueError("allowed_actions and allowed_targets must be lists")
    publish = request.get("publish", False) is True
    permitted = request.get("permission_granted", False) is True
    publish_permitted = request.get("publish_permission_granted", False) is True
    evidence_complete = request.get("evidence_complete", False) is True
    violations = []
    if action not in allowed_actions:
        violations.append("ACTION_OUTSIDE_DECLARED_SCOPE")
    if target not in allowed_targets:
        violations.append("TARGET_OUTSIDE_DECLARED_SCOPE")
    if not permitted:
        violations.append("ACTION_PERMISSION_MISSING")
    if publish and not publish_permitted:
        violations.append("EXPLICIT_PUBLICATION_PERMISSION_MISSING")
    if not evidence_complete:
        violations.append("EVIDENCE_OR_ACCEPTANCE_CHECK_INCOMPLETE")
    if "ACTION_OUTSIDE_DECLARED_SCOPE" in violations or "TARGET_OUTSIDE_DECLARED_SCOPE" in violations:
        decision = "DENY"
    elif "ACTION_PERMISSION_MISSING" in violations or "EXPLICIT_PUBLICATION_PERMISSION_MISSING" in violations:
        decision = "DENY"
    elif not evidence_complete:
        decision = "REVIEW"
    else:
        decision = "ALLOW_WITHIN_DECLARED_SCOPE"
    return {
        "decision": decision,
        "action": action,
        "target": target,
        "publish_requested": publish,
        "violations": violations,
        "note": "A logical ALLOW decision is not an executed action. An external executor must enforce authorization and verify the resulting state.",
    }


def compare_thresholds(score: float, old_threshold: float, new_threshold: float) -> dict[str, Any]:
    values = (score, old_threshold, new_threshold)
    if any(not isinstance(x, (int, float)) or not math.isfinite(x) for x in values):
        raise ValueError("score and thresholds must be finite numbers")
    old_decision = "ACCEPT" if score >= old_threshold else "REJECT"
    new_decision = "ACCEPT" if score >= new_threshold else "REJECT"
    return {
        "score": float(score),
        "old_threshold": float(old_threshold),
        "new_threshold": float(new_threshold),
        "old_decision": old_decision,
        "new_decision": new_decision,
        "decision_changed": old_decision != new_decision,
        "interpretation": (
            "Same score, different decision caused by the threshold change."
            if old_decision != new_decision
            else "The decision remained the same for these thresholds."
        ),
        "status": "SYNTHETIC_CALCULATION_NOT_REAL_INCIDENT",
    }


def validate_corpus(repo_root: str | Path) -> dict[str, Any]:
    root = Path(repo_root)
    data_dir = root / "research" / "data"
    manifest_path = data_dir / "LOGIC_CORPUS_1000_PAGE_BLUEPRINT_V1.json"
    gate_path = data_dir / "LETTER_GATE_MAP_231_V1.json"
    triple_path = data_dir / "LETTER_TRIPLE_MAP_1540_V1.json"
    missing = [str(path.relative_to(root)) for path in (manifest_path, gate_path, triple_path) if not path.exists()]
    if missing:
        return {"status": "BLOCKED", "missing_files": missing, "checks": {}}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    gate_map = json.loads(gate_path.read_text(encoding="utf-8"))
    triple_map = json.loads(triple_path.read_text(encoding="utf-8"))
    groups = manifest.get("groups", [])
    pages: list[dict[str, Any]] = []
    group_results = []
    for group in groups:
        candidate = data_dir / group["path"]
        if not candidate.exists():
            group_results.append({"name": group["name"], "expected": group["count"], "actual": None, "ok": False, "reason": "SHARD_MISSING"})
            continue
        records = json.loads(candidate.read_text(encoding="utf-8"))
        pages.extend(records)
        group_results.append({"name": group["name"], "expected": group["count"], "actual": len(records), "ok": len(records) == group["count"]})

    page_ids = [item.get("id") for item in pages]
    gate_records = gate_map.get("undirected_gates", [])
    directed = gate_map.get("directed_transitions", [])
    reverse_by_id = {item.get("id"): item for item in directed}
    reverse_ok = all(
        (r := reverse_by_id.get(item.get("reverse_id"))) is not None
        and r.get("from") == item.get("to")
        and r.get("to") == item.get("from")
        for item in directed
    )
    triples = triple_map.get("triples", [])
    triple_keys = [tuple(item.get("letters", [])) for item in triples]
    counts = combinatorial_counts()
    checks = {
        "declared_total_1000": manifest.get("total_page_definitions") == 1000,
        "actual_page_record_count_1000": len(pages) == 1000,
        "page_ids_unique": len(page_ids) == len(set(page_ids)),
        "shard_counts_match_manifest": all(item["ok"] for item in group_results),
        "letter_nodes_22": len(gate_map.get("vertices", [])) == 22,
        "undirected_gates_231": len(gate_records) == 231,
        "directed_transitions_462": len(directed) == 462,
        "directed_reverse_links_valid": reverse_ok,
        "unordered_triples_1540": len(triples) == 1540,
        "triple_sets_unique": len(triple_keys) == len(set(triple_keys)),
        "calculated_counts_match": (
            counts["undirected_pairs"] == 231
            and counts["directed_distinct_pairs"] == 462
            and counts["unordered_distinct_triples"] == 1540
            and counts["ordered_distinct_triples"] == 9240
        ),
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "group_counts": group_results,
        "actual_page_records": len(pages),
        "unique_page_ids": len(set(page_ids)),
        "gate_count": len(gate_records),
        "directed_transition_count": len(directed),
        "reverse_links_valid": reverse_ok,
        "triple_count": len(triples),
        "math_counts": counts,
        "limitations": [
            "Validation checks registry shape and combinatorial invariants; it does not validate semantic meanings of letters or gates.",
            "A passing corpus check does not establish that the 1,000 page definitions are fully written or that the full AI architecture is implemented.",
        ],
    }



def load_corpus_context(repo_root: str | Path) -> dict[str, Any]:
    """Load validated structural facts from the WANGA-LAB corpus.

    These facts describe registry structure only. They do not assign meaning to
    letters or gates. During inference, only predicates explicitly mentioned in
    rule antecedents are added to the working memory.
    """
    root = Path(repo_root)
    validation = validate_corpus(root)
    if validation.get("status") != "PASS":
        raise ValueError(
            "Corpus validation failed; refusing to load registry facts: "
            + json.dumps(validation, ensure_ascii=False)
        )

    data_dir = root / "research" / "data"
    manifest = json.loads(
        (data_dir / "LOGIC_CORPUS_1000_PAGE_BLUEPRINT_V1.json").read_text(encoding="utf-8")
    )
    gate_map = json.loads(
        (data_dir / "LETTER_GATE_MAP_231_V1.json").read_text(encoding="utf-8")
    )
    triple_map = json.loads(
        (data_dir / "LETTER_TRIPLE_MAP_1540_V1.json").read_text(encoding="utf-8")
    )

    facts: list[dict[str, Any]] = []

    def add_fact(fact_id: str, subject: str, predicate: str, obj: str, corpus_file: str) -> None:
        facts.append({
            "fact_id": fact_id,
            "atom": {"subject": subject, "predicate": predicate, "object": obj, "polarity": True},
            "corpus_file": corpus_file,
            "status": "CORPUS_STRUCTURE_NOT_SEMANTIC",
        })

    gate_path = "research/data/LETTER_GATE_MAP_231_V1.json"
    triple_path = "research/data/LETTER_TRIPLE_MAP_1540_V1.json"
    for vertex in gate_map.get("vertices", []):
        add_fact(
            f"CORPUS-LETTER-{vertex['id']}",
            f"letter:{vertex['letter']}", "corpus_node_in", "K22", gate_path
        )
    for gate in gate_map.get("undirected_gates", []):
        add_fact(
            f"CORPUS-GATE-{gate['id']}",
            f"gate:{gate['id']}", "corpus_connects_unordered",
            f"{gate['a']}|{gate['b']}", gate_path
        )
    for transition in gate_map.get("directed_transitions", []):
        tid = transition["id"]
        add_fact(f"CORPUS-{tid}-FROM", f"transition:{tid}", "corpus_from", transition["from"], gate_path)
        add_fact(f"CORPUS-{tid}-TO", f"transition:{tid}", "corpus_to", transition["to"], gate_path)
        add_fact(f"CORPUS-{tid}-REVERSE", f"transition:{tid}", "corpus_reverse_is", transition["reverse_id"], gate_path)
        add_fact(f"CORPUS-{tid}-PARENT", f"transition:{tid}", "corpus_parent_gate", transition["gate_id"], gate_path)
    for triple in triple_map.get("triples", []):
        for letter in triple["letters"]:
            add_fact(
                f"CORPUS-{triple['id']}-CONTAINS-{letter}",
                f"triple:{triple['id']}", "corpus_contains", letter, triple_path
            )

    page_definitions = 0
    for group in manifest.get("groups", []):
        shard_path = data_dir / group["path"]
        page_records = json.loads(shard_path.read_text(encoding="utf-8"))
        for page in page_records:
            page_id = str(page["id"])
            page_type = str(page.get("type", "UNKNOWN"))
            add_fact(
                f"CORPUS-PAGE-{page_id}-TYPE",
                f"page:{page_id}", "corpus_page_type", page_type,
                str(Path("research/data") / group["path"])
            )
            macro_map = page.get("macro_map")
            if macro_map:
                add_fact(
                    f"CORPUS-PAGE-{page_id}-MAP",
                    f"page:{page_id}", "corpus_belongs_to_map", str(macro_map),
                    str(Path("research/data") / group["path"])
                )
            page_definitions += 1

    ids = [item["fact_id"] for item in facts]
    if len(ids) != len(set(ids)):
        raise ValueError("Corpus structural fact identifiers are not unique.")

    return {
        "status": "LOADED",
        "registry_status": validation["status"],
        "counts": {
            "letters": len(gate_map.get("vertices", [])),
            "undirected_gates": len(gate_map.get("undirected_gates", [])),
            "directed_transitions": len(gate_map.get("directed_transitions", [])),
            "unordered_triples": len(triple_map.get("triples", [])),
            "page_definitions": page_definitions,
            "structural_facts": len(facts),
        },
        "facts": facts,
        "limitations": [
            "Loaded facts describe registry structure only, not logical meanings of gates.",
            "Only predicates required by explicit rule antecedents are injected into a run.",
            "Corpus facts are marked CORPUS_STRUCTURE_NOT_SEMANTIC and cannot authenticate an interpretive claim.",
        ],
    }


def sample_bundle() -> dict[str, Any]:
    return {
        "case_id": "SITE-UPDATE-SCOPE-DEMO-001",
        "description": "Synthetic example: reason over an explicitly stated request, scope and permission.",
        "evidence": [
            {"id": "E-REQUEST", "source_uri": "fixture://site-update/request", "source_version": "fixture-v1", "location": "input.request", "status": "TEST_FIXTURE"},
            {"id": "E-SCOPE", "source_uri": "fixture://site-update/scope", "source_version": "fixture-v1", "location": "input.scope", "status": "TEST_FIXTURE"},
            {"id": "E-PERMISSION", "source_uri": "fixture://site-update/permission", "source_version": "fixture-v1", "location": "input.permission", "status": "TEST_FIXTURE"},
        ],
        "claims": [
            {"id": "C-REQUEST", "atom": {"subject": "request", "predicate": "action", "object": "typo_fix"}, "epistemic_status": "TEST_FIXTURE", "evidence_refs": ["E-REQUEST"]},
            {"id": "C-SCOPE", "atom": {"subject": "scope", "predicate": "allows", "object": "typo_fix"}, "epistemic_status": "TEST_FIXTURE", "evidence_refs": ["E-SCOPE"]},
            {"id": "C-PERMISSION", "atom": {"subject": "permission", "predicate": "grants", "object": "typo_fix"}, "epistemic_status": "TEST_FIXTURE", "evidence_refs": ["E-PERMISSION"]},
            {"id": "C-UNSUPPORTED-PUBLISH", "atom": {"subject": "request", "predicate": "action", "object": "publish_without_approval"}, "epistemic_status": "HYPOTHESIS", "evidence_refs": []},
        ],
        "action_gate": {
            "action": "typo_fix",
            "target": "approved-page-1",
            "allowed_actions": ["typo_fix"],
            "allowed_targets": ["approved-page-1"],
            "permission_granted": True,
            "publish": False,
            "publish_permission_granted": False,
            "evidence_complete": True,
        },
        "threshold_comparison": {"score": 0.75, "old_threshold": 0.80, "new_threshold": 0.60},
        "rules": [
            {
                "id": "R-CORPUS-GATE-001-STRUCTURE",
                "status": "ACTIVE_SPECIFIED",
                "description": "Structural smoke test: the registry enumerates GATE-001 as the unordered pair א|ב. This does not assign meaning to that pair.",
                "antecedents": [
                    {"subject": "gate:GATE-001", "predicate": "corpus_connects_unordered", "object": "א|ב"}
                ],
                "consequent": {"subject": "corpus", "predicate": "gate_structure_loaded", "object": "GATE-001"},
                "source_refs": ["repo://research/data/LETTER_GATE_MAP_231_V1.json#GATE-001"]
            },
            {
                "id": "R-SCOPE-PERMISSION",
                "status": "ACTIVE_SPECIFIED",
                "description": "A candidate permission result follows only if request, scope, and permission facts are all present in the fixture.",
                "antecedents": [
                    {"subject": "request", "predicate": "action", "object": "$ACTION"},
                    {"subject": "scope", "predicate": "allows", "object": "$ACTION"},
                    {"subject": "permission", "predicate": "grants", "object": "$ACTION"},
                ],
                "consequent": {"subject": "action", "predicate": "candidate_allowed", "object": "$ACTION"},
                "source_refs": ["fixture://logic-kernel/rules/R-SCOPE-PERMISSION"],
            }
        ],
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bounded evidence-aware symbolic logic kernel")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("counts", help="Print exact 22-symbol combinatorial counts")
    default_repo_root = str(Path(__file__).resolve().parents[1])
    demo_parser = sub.add_parser("demo", help="Run the built-in synthetic reasoning example")
    demo_parser.add_argument("--compact", action="store_true", help="Print compact JSON")
    demo_parser.add_argument("--repo-root", default=default_repo_root, help="Repository root used to load the corpus")
    demo_parser.add_argument("--no-corpus", action="store_true", help="Run without corpus registry facts")
    run_parser = sub.add_parser("run", help="Run a user-supplied JSON bundle")
    run_parser.add_argument("bundle", help="Path to JSON bundle")
    run_parser.add_argument("--compact", action="store_true", help="Print compact JSON")
    run_parser.add_argument("--repo-root", default=default_repo_root, help="Repository root used to load the corpus")
    run_parser.add_argument("--no-corpus", action="store_true", help="Run without corpus registry facts")
    validate_parser = sub.add_parser("validate-corpus", help="Validate the WANGA-LAB 1,000-definition corpus")
    validate_parser.add_argument("--repo-root", default=".", help="Path to the WANGA-LAB repository root")
    args = parser.parse_args(argv)

    if args.command == "counts":
        output = combinatorial_counts()
    elif args.command == "demo":
        bundle = sample_bundle()
        context = None if args.no_corpus else load_corpus_context(args.repo_root)
        output = run_bundle(bundle, corpus_context=context)
        output["action_gate_result"] = gate_action(bundle["action_gate"])
        output["threshold_comparison"] = compare_thresholds(**bundle["threshold_comparison"])
        output["combinatorial_counts"] = combinatorial_counts()
    elif args.command == "run":
        bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
        context = None if args.no_corpus else load_corpus_context(args.repo_root)
        output = run_bundle(bundle, corpus_context=context)
        if "action_gate" in bundle:
            output["action_gate_result"] = gate_action(bundle["action_gate"])
        if "threshold_comparison" in bundle:
            output["threshold_comparison"] = compare_thresholds(**bundle["threshold_comparison"])
    else:
        output = validate_corpus(args.repo_root)

    print(json.dumps(output, ensure_ascii=False, indent=None if getattr(args, "compact", False) else 2))
    if args.command == "validate-corpus" and output.get("status") != "PASS":
        return 1
    if args.command in {"run", "demo"} and output.get("status") == "ROUND_LIMIT_REACHED_REVIEW":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
