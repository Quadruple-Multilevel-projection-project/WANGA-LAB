"""Logic-Native Language (LNL) v0.1: a small declarative language for executable models.

The syntax is logic-first: facts, rules, goals, evidence, and constraints are
first-class statements. This module compiles LNL to the bounded WANGA symbolic
kernel's JSON bundle. It does not claim that unrestricted natural language is
already formalized or that every gate has a semantic interpretation.
"""
from __future__ import annotations

import hashlib
import json
import re
import shlex
from dataclasses import dataclass
from typing import Any, Mapping


ATOM_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\.([A-Za-z_][A-Za-z0-9_-]*)\(([^()]*)\)$")
MODEL_RE = re.compile(r"^model\s+([A-Za-z_][A-Za-z0-9_-]*)\s+version=([A-Za-z0-9_.+-]+)(?:\s+description=(.*))?$")
SOURCE_RE = re.compile(r"^source\s+(\S+)\s+(.+)$")
FACT_RE = re.compile(r"^fact\s+(\S+)\s+(\S+)\s+(.+)$")
RULE_RE = re.compile(r"^rule\s+(\S+)(.*?)\s*:\s*$")
GOAL_RE = re.compile(r"^goal\s+(.+)$")
CONSTRAINT_RE = re.compile(r"^constraint\s+([A-Za-z_][A-Za-z0-9_-]*)$")
TERM_RE = re.compile(r"^\$?[A-Za-z_][A-Za-z0-9_:-]*$")

RAW_CLAIM_STATUSES = {"OBSERVED", "TEST_FIXTURE", "HYPOTHESIS", "SPECIFIED", "UNKNOWN"}
SUPPORTED_CONSTRAINTS = {
    "require_evidence",
    "no_unbound_rule_vars",
    "no_automatic_verified_status",
    "require_rule_sources_or_explicit_assumption",
}


@dataclass(frozen=True)
class AtomExpr:
    subject: str
    predicate: str
    object: str
    polarity: bool = True

    @classmethod
    def parse(cls, text: str) -> "AtomExpr":
        match = ATOM_RE.fullmatch(text.strip())
        if not match:
            raise ValueError(f"Invalid atom expression: {text!r}; expected subject.predicate(term)")
        subject, predicate, obj = (item.strip() for item in match.groups())
        if not TERM_RE.fullmatch(subject) or not TERM_RE.fullmatch(predicate) or not TERM_RE.fullmatch(obj):
            raise ValueError(f"Invalid atom term in: {text!r}")
        if obj.startswith("$") and len(obj) == 1:
            raise ValueError("Empty variable name")
        return cls(subject, predicate, obj)

    def to_kernel(self) -> dict[str, Any]:
        return {
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.object,
            "polarity": self.polarity,
        }

    def variables(self) -> set[str]:
        return {part for part in (self.subject, self.predicate, self.object) if part.startswith("$")}

    def render(self) -> str:
        return f"{self.subject}.{self.predicate}({self.object})"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: str
    message: str
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"code": self.code, "severity": self.severity, "message": self.message, "line": self.line}


def _tokens(line: str) -> list[str]:
    try:
        return shlex.split(line, comments=False, posix=True)
    except ValueError as exc:
        raise ValueError(f"Could not tokenize declaration: {exc}") from exc


def _key_values(tokens: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for token in tokens:
        if "=" not in token:
            raise ValueError(f"Expected key=value option, got {token!r}")
        key, value = token.split("=", 1)
        if not key or key in result:
            raise ValueError(f"Empty or duplicate option key {key!r}")
        result[key] = value
    return result


def _parse_atom_list(text: str) -> list[AtomExpr]:
    atoms = [piece.strip() for piece in re.split(r"\s+AND\s+", text.strip())]
    if not atoms or any(not atom for atom in atoms):
        raise ValueError("Rule antecedent list is empty or malformed")
    return [AtomExpr.parse(atom) for atom in atoms]


def parse_lnl(text: str) -> dict[str, Any]:
    """Parse LNL v0.1 into a typed intermediate model plus diagnostics."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("LNL input must be non-empty text")

    model: dict[str, Any] = {
        "schema_version": "lnl/0.1",
        "name": None,
        "version": None,
        "description": "",
        "sources": [],
        "facts": [],
        "rules": [],
        "goals": [],
        "constraints": [],
        "source_lines": {},
    }
    seen_ids: dict[str, str] = {}
    warnings: list[Diagnostic] = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        i += 1
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("model "):
            match = MODEL_RE.fullmatch(stripped)
            if not match:
                raise ValueError(f"Line {i}: malformed model header")
            if model["name"] is not None:
                raise ValueError(f"Line {i}: only one model declaration is allowed")
            model["name"], model["version"], description = match.groups()
            model["description"] = (description or "").strip().strip('"')
            model["source_lines"]["model"] = i
            continue

        if stripped.startswith("source "):
            match = SOURCE_RE.fullmatch(stripped)
            if not match:
                raise ValueError(f"Line {i}: malformed source declaration")
            source_id, options_text = match.groups()
            opts = _key_values(_tokens(options_text))
            if "uri" not in opts:
                raise ValueError(f"Line {i}: source requires uri=...")
            if source_id in seen_ids:
                raise ValueError(f"Line {i}: duplicate identifier {source_id}")
            seen_ids[source_id] = "source"
            model["sources"].append({
                "id": source_id,
                "source_uri": opts["uri"],
                "source_version": opts.get("version", ""),
                "location": opts.get("location", ""),
                "status": opts.get("status", "UNREVIEWED").upper(),
                "note": opts.get("note", ""),
                "line": i,
            })
            continue

        if stripped.startswith("fact "):
            match = FACT_RE.fullmatch(stripped)
            if not match:
                raise ValueError(f"Line {i}: malformed fact declaration")
            claim_id, atom_text, options_text = match.groups()
            atom = AtomExpr.parse(atom_text)
            opts = _key_values(_tokens(options_text))
            if claim_id in seen_ids:
                raise ValueError(f"Line {i}: duplicate identifier {claim_id}")
            seen_ids[claim_id] = "fact"
            evidence_refs = [item for item in opts.get("evidence", "").split(",") if item]
            model["facts"].append({
                "id": claim_id,
                "atom": atom,
                "epistemic_status": opts.get("status", "UNKNOWN").upper(),
                "evidence_refs": evidence_refs,
                "line": i,
            })
            continue

        if stripped.startswith("rule "):
            match = RULE_RE.fullmatch(stripped)
            if not match:
                raise ValueError(f"Line {i}: malformed rule header; expected 'rule ID [options]:'")
            rule_id, option_text = match.groups()
            opts = _key_values(_tokens(option_text.strip())) if option_text.strip() else {}
            if rule_id in seen_ids:
                raise ValueError(f"Line {i}: duplicate identifier {rule_id}")
            if i >= len(lines) or not lines[i].strip():
                raise ValueError(f"Line {i}: rule requires an indented rule expression")
            expression_line = lines[i]
            if not expression_line[:1].isspace():
                raise ValueError(f"Line {i + 1}: rule expression must be indented")
            i += 1
            expression = expression_line.strip()
            if expression.count("=>") != 1:
                raise ValueError(f"Line {i}: rule expression needs exactly one '=>'")
            lhs, rhs = (side.strip() for side in expression.split("=>"))
            antecedents = _parse_atom_list(lhs)
            consequent = AtomExpr.parse(rhs)
            source_ids = [item for item in opts.get("source", "").split(",") if item]
            assumption = opts.get("assumption", "false").lower() == "true"
            seen_ids[rule_id] = "rule"
            model["rules"].append({
                "id": rule_id,
                "antecedents": antecedents,
                "consequent": consequent,
                "source_ids": source_ids,
                "assumption": assumption,
                "description": opts.get("description", ""),
                "line": i,
            })
            continue

        if stripped.startswith("goal "):
            match = GOAL_RE.fullmatch(stripped)
            if not match:
                raise ValueError(f"Line {i}: malformed goal")
            model["goals"].append({"atom": AtomExpr.parse(match.group(1)), "line": i})
            continue

        if stripped.startswith("constraint "):
            match = CONSTRAINT_RE.fullmatch(stripped)
            if not match:
                raise ValueError(f"Line {i}: malformed constraint")
            model["constraints"].append({"name": match.group(1), "line": i})
            continue

        raise ValueError(f"Line {i}: unknown LNL statement: {stripped[:80]}")

    if model["name"] is None:
        raise ValueError("Missing model declaration")

    errors: list[Diagnostic] = []
    source_ids = {item["id"] for item in model["sources"]}
    constraints = {item["name"] for item in model["constraints"]}
    if len(constraints) != len(model["constraints"]):
        errors.append(Diagnostic("DUPLICATE_CONSTRAINT", "ERROR", "A constraint is declared more than once."))

    unknown_constraints = sorted(constraints - SUPPORTED_CONSTRAINTS)
    for name in unknown_constraints:
        errors.append(Diagnostic("UNSUPPORTED_CONSTRAINT", "ERROR", f"Constraint {name!r} is not implemented in LNL v0.1."))

    for fact in model["facts"]:
        if fact["epistemic_status"] == "VERIFIED":
            errors.append(Diagnostic("RAW_FACT_CANNOT_BE_VERIFIED", "ERROR", f"Fact {fact['id']} cannot declare VERIFIED status; verification requires a separate result record.", fact["line"]))
        elif fact["epistemic_status"] not in RAW_CLAIM_STATUSES:
            errors.append(Diagnostic("UNKNOWN_EPISTEMIC_STATUS", "ERROR", f"Unsupported raw-fact status {fact['epistemic_status']!r}.", fact["line"]))
        if "require_evidence" in constraints and not fact["evidence_refs"]:
            errors.append(Diagnostic("FACT_WITHOUT_EVIDENCE", "ERROR", f"Fact {fact['id']} has no evidence reference.", fact["line"]))
        for ref in fact["evidence_refs"]:
            if ref not in source_ids:
                errors.append(Diagnostic("MISSING_SOURCE_REFERENCE", "ERROR", f"Fact {fact['id']} references undeclared source {ref!r}.", fact["line"]))

    for rule in model["rules"]:
        for source_id in rule["source_ids"]:
            if source_id not in source_ids:
                errors.append(Diagnostic("MISSING_RULE_SOURCE", "ERROR", f"Rule {rule['id']} references undeclared source {source_id!r}.", rule["line"]))
        if "require_rule_sources_or_explicit_assumption" in constraints and not rule["source_ids"] and not rule["assumption"]:
            errors.append(Diagnostic("UNSOURCED_RULE_WITHOUT_ASSUMPTION", "ERROR", f"Rule {rule['id']} must cite a source or set assumption=true.", rule["line"]))
        antecedent_vars = set().union(*(atom.variables() for atom in rule["antecedents"]))
        consequent_vars = rule["consequent"].variables()
        if "no_unbound_rule_vars" in constraints and not consequent_vars.issubset(antecedent_vars):
            missing = sorted(consequent_vars - antecedent_vars)
            errors.append(Diagnostic("UNBOUND_CONSEQUENT_VARIABLE", "ERROR", f"Rule {rule['id']} has consequent variables not bound in antecedents: {missing}.", rule["line"]))
        if not rule["source_ids"] and not rule["assumption"]:
            warnings.append(Diagnostic("RULE_WITHOUT_PROVENANCE", "WARNING", f"Rule {rule['id']} has no source reference and is not marked as an explicit modeling assumption.", rule["line"]))

    if not model["goals"]:
        warnings.append(Diagnostic("NO_GOAL_DECLARED", "WARNING", "No goal was declared; the model can still be compiled, but there is no target query to evaluate."))
    if not model["facts"] and not model["rules"]:
        errors.append(Diagnostic("EMPTY_MODEL", "ERROR", "A model must contain at least one fact or one rule."))

    model["errors"] = errors
    model["warnings"] = warnings
    return model


def compile_lnl(text: str) -> dict[str, Any]:
    """Compile a valid LNL program into a WANGA kernel bundle and audit graph."""
    model = parse_lnl(text)
    if model["errors"]:
        return {
            "status": "REJECTED",
            "language": model["schema_version"],
            "model_name": model["name"],
            "model_version": model["version"],
            "source_text": text,
            "diagnostics": [item.to_dict() for item in model["errors"] + model["warnings"]],
            "compiled_model": None,
            "execution_bundle": None,
            "model_graph": None,
        }

    evidence = [{key: value for key, value in source.items() if key != "line"} for source in model["sources"]]
    claims = [{
        "id": fact["id"],
        "atom": fact["atom"].to_kernel(),
        "epistemic_status": fact["epistemic_status"],
        "evidence_refs": fact["evidence_refs"],
    } for fact in model["facts"]]
    source_by_id = {source["id"]: source for source in evidence}
    rules = [{
        "id": rule["id"],
        "status": "ACTIVE_SPECIFIED",
        "description": rule["description"] or "Compiled from LNL v0.1.",
        "antecedents": [atom.to_kernel() for atom in rule["antecedents"]],
        "consequent": rule["consequent"].to_kernel(),
        "source_refs": [source_by_id[source_id]["source_uri"] for source_id in rule["source_ids"]],
    } for rule in model["rules"]]

    constants: set[str] = set()
    graph_nodes: dict[str, dict[str, Any]] = {}
    graph_edges: list[dict[str, Any]] = []

    def add_atom_graph(atom: AtomExpr, node_id: str, kind: str, source_id: str) -> None:
        for value in (atom.subject, atom.object):
            if not value.startswith("$"):
                constants.add(value)
        graph_nodes[node_id] = {"id": node_id, "kind": kind, "label": atom.render()}
        graph_edges.append({
            "id": f"EDGE-{len(graph_edges)+1:04d}",
            "source": node_id,
            "target": atom.subject if atom.subject.startswith("$") else f"SYMBOL:{atom.subject}",
            "relation": "SUBJECT",
            "origin_id": source_id,
        })
        graph_edges.append({
            "id": f"EDGE-{len(graph_edges)+1:04d}",
            "source": node_id,
            "target": atom.object if atom.object.startswith("$") else f"SYMBOL:{atom.object}",
            "relation": atom.predicate,
            "origin_id": source_id,
        })
        for value in (atom.subject, atom.object):
            if not value.startswith("$"):
                graph_nodes.setdefault(f"SYMBOL:{value}", {"id": f"SYMBOL:{value}", "kind": "SYMBOL", "label": value})

    for fact in model["facts"]:
        add_atom_graph(fact["atom"], f"FACT:{fact['id']}", "FACT", fact["id"])
    for rule in model["rules"]:
        for index, atom in enumerate(rule["antecedents"], start=1):
            add_atom_graph(atom, f"RULE:{rule['id']}:PREMISE:{index}", "RULE_PREMISE", rule["id"])
        add_atom_graph(rule["consequent"], f"RULE:{rule['id']}:CONCLUSION", "RULE_CONCLUSION", rule["id"])
    for goal in model["goals"]:
        add_atom_graph(goal["atom"], f"GOAL:{len(graph_nodes)+1}", "GOAL", "GOAL")

    return {
        "status": "COMPILED_FOR_REVIEW",
        "semantic_status": "NOT_YET_VERIFIED",
        "language": model["schema_version"],
        "model_name": model["name"],
        "model_version": model["version"],
        "source_text": text,
        "model_hash_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "diagnostics": [item.to_dict() for item in model["warnings"]],
        "compiled_model": {
            "name": model["name"],
            "version": model["version"],
            "description": model["description"],
            "symbols": sorted(constants),
            "goals": [goal["atom"].to_kernel() for goal in model["goals"]],
            "constraints": [item["name"] for item in model["constraints"]],
            "rule_count": len(rules),
            "fact_count": len(claims),
            "source_count": len(evidence),
        },
        "execution_bundle": {
            "case_id": model["name"],
            "description": model["description"] or "Compiled LNL v0.1 model.",
            "evidence": evidence,
            "claims": claims,
            "rules": rules,
        },
        "model_graph": {
            "nodes": list(graph_nodes.values()),
            "edges": graph_edges,
        },
        "goals": [goal["atom"].to_kernel() for goal in model["goals"]],
        "source_registry": evidence,
        "status_contract": {
            "compile_status": "COMPILED_FOR_REVIEW",
            "runtime_claims": "DERIVED_NOT_VERIFIED",
            "publication": "NOT_AUTOMATIC",
        },
    }
