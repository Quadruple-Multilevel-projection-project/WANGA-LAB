"""Bounded propositional text frontend for the canonical logic_proof typed-AST adapter.

This module parses only formulas written in the declared propositional grammar.
All Z3 solving is delegated to logic_proof.z3_adapter; results never establish
empirical truth or source authenticity.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping, Sequence

SCHEMA_VERSION = "wanga-formal-claim/1.0"
PARSER_VERSION = "wanga-propositional-parser/1.0"
MAX_FORMULA_CHARS = 4096
MAX_FORMULA_TOKENS = 512
MAX_FORMULA_NESTING = 32
MAX_VARIABLES = 256
MAX_PREMISES = 200
_TOKEN = re.compile(r"\s*(<->|->|[()!&|]|[A-Za-z_][A-Za-z0-9_]*)")
_RESERVED = {"not", "and", "or", "implies", "iff", "true", "false"}


class FormalInputError(ValueError):
    """The claim does not conform to the bounded formal input contract."""


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def tokenize_formula(text: str) -> list[str]:
    if not isinstance(text, str) or not text.strip():
        raise FormalInputError("formula must be non-empty text")
    if len(text) > MAX_FORMULA_CHARS:
        raise FormalInputError(f"formula exceeds {MAX_FORMULA_CHARS} character limit")
    result: list[str] = []
    pos = 0
    while pos < len(text):
        if text[pos:].isspace():
            break
        match = _TOKEN.match(text, pos)
        if not match:
            raise FormalInputError(f"unsupported token at character {pos}: {text[pos:pos + 16]!r}")
        result.append(match.group(1))
        pos = match.end()
    if not result:
        raise FormalInputError("formula has no tokens")
    if len(result) > MAX_FORMULA_TOKENS:
        raise FormalInputError(f"formula exceeds {MAX_FORMULA_TOKENS} token limit")
    depth = 0
    for token in result:
        if token == "(":
            depth += 1
            if depth > MAX_FORMULA_NESTING:
                raise FormalInputError(f"formula exceeds {MAX_FORMULA_NESTING} nesting limit")
        elif token == ")":
            depth = max(0, depth - 1)
    return result


class FormulaParser:
    """Recursive-descent parser: iff -> implies -> or -> and -> not -> atom."""

    def __init__(self, text: str, declared_variables: set[str]):
        self.tokens = tokenize_formula(text)
        self.position = 0
        self.declared_variables = declared_variables
        self.used_variables: set[str] = set()

    def _peek(self) -> str | None:
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def _take(self) -> str:
        token = self._peek()
        if token is None:
            raise FormalInputError("unexpected end of formula")
        self.position += 1
        return token

    def parse(self) -> tuple:
        ast = self._parse_iff()
        if self._peek() is not None:
            raise FormalInputError(f"unexpected token {self._peek()!r}")
        undeclared = self.used_variables - self.declared_variables
        if undeclared:
            raise FormalInputError(f"undeclared variables: {sorted(undeclared)}")
        return ast

    def _parse_iff(self) -> tuple:
        left = self._parse_implies()
        while self._peek() in {"<->", "iff"}:
            self._take()
            left = ("iff", left, self._parse_implies())
        return left

    def _parse_implies(self) -> tuple:
        left = self._parse_or()
        if self._peek() in {"->", "implies"}:
            self._take()
            return ("implies", left, self._parse_implies())
        return left

    def _parse_or(self) -> tuple:
        left = self._parse_and()
        while self._peek() in {"|", "or"}:
            self._take()
            left = ("or", left, self._parse_and())
        return left

    def _parse_and(self) -> tuple:
        left = self._parse_not()
        while self._peek() in {"&", "and"}:
            self._take()
            left = ("and", left, self._parse_not())
        return left

    def _parse_not(self) -> tuple:
        if self._peek() in {"!", "not"}:
            self._take()
            return ("not", self._parse_not())
        return self._parse_atom()

    def _parse_atom(self) -> tuple:
        token = self._take()
        if token == "(":
            node = self._parse_iff()
            if self._take() != ")":
                raise FormalInputError("expected closing parenthesis")
            return node
        if token == ")":
            raise FormalInputError("unexpected closing parenthesis")
        lower = token.casefold()
        if lower in {"true", "false"}:
            return ("const", lower == "true")
        if lower in _RESERVED:
            raise FormalInputError(f"operator {token!r} cannot be used as an atom")
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            raise FormalInputError(f"invalid variable {token!r}")
        self.used_variables.add(token)
        return ("var", token)


def _to_logic_ast(ast: tuple) -> dict[str, Any]:
    """Convert the text parser's validated AST into the canonical typed AST."""
    op = ast[0]
    if op == "var":
        return {"var": ast[1]}
    if op == "const":
        return {"const": ast[1]}
    if op == "not":
        return {"op": "not", "args": [_to_logic_ast(ast[1])]}
    if op == "and":
        return {"op": "and", "args": [_to_logic_ast(ast[1]), _to_logic_ast(ast[2])]}
    if op == "or":
        return {"op": "or", "args": [_to_logic_ast(ast[1]), _to_logic_ast(ast[2])]}
    if op == "implies":
        return {"op": "implies", "args": [_to_logic_ast(ast[1]), _to_logic_ast(ast[2])]}
    if op == "iff":
        # Both operands are Bool in this propositional frontend.
        return {"op": "eq", "args": [_to_logic_ast(ast[1]), _to_logic_ast(ast[2])]}
    raise FormalInputError(f"unsupported parsed AST operator: {op!r}")


def _map_solver_result(result: Any, z3_module: Any) -> str:
    """Compatibility helper; the actual solving is delegated to logic_proof.z3_adapter."""
    if result == z3_module.sat:
        return "SAT"
    if result == z3_module.unsat:
        return "UNSAT"
    return "UNKNOWN"


def _validate_claim(spec: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(spec, Mapping):
        raise FormalInputError("claim input must be an object")
    if spec.get("schema_version", SCHEMA_VERSION) != SCHEMA_VERSION:
        raise FormalInputError(f"schema_version must be {SCHEMA_VERSION}")
    claim_id = spec.get("claim_id")
    variables = spec.get("variables")
    premises = spec.get("premises")
    conclusion = spec.get("conclusion")
    source_refs = spec.get("source_refs", [])
    timeout_ms = spec.get("timeout_ms", 3000)
    if not isinstance(claim_id, str) or not claim_id.strip():
        raise FormalInputError("claim_id must be a non-empty string")
    if not isinstance(variables, list) or any(not isinstance(v, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", v) for v in variables):
        raise FormalInputError("variables must be a list of ASCII identifiers")
    if len(variables) != len(set(variables)):
        raise FormalInputError("variables must be unique")
    if len(variables) > MAX_VARIABLES:
        raise FormalInputError(f"variables exceed {MAX_VARIABLES} limit")
    if set(v.casefold() for v in variables) & _RESERVED:
        raise FormalInputError("variables may not use reserved logical operator names")
    if not isinstance(premises, list) or any(not isinstance(p, str) or not p.strip() for p in premises):
        raise FormalInputError("premises must be a list of non-empty formula strings")
    if len(premises) > MAX_PREMISES:
        raise FormalInputError(f"premises exceed {MAX_PREMISES} limit")
    if any(len(p) > MAX_FORMULA_CHARS for p in premises):
        raise FormalInputError(f"each premise must be at most {MAX_FORMULA_CHARS} characters")
    if not isinstance(conclusion, str) or not conclusion.strip():
        raise FormalInputError("conclusion must be a non-empty formula string")
    if len(conclusion) > MAX_FORMULA_CHARS:
        raise FormalInputError(f"conclusion exceeds {MAX_FORMULA_CHARS} character limit")
    if not isinstance(source_refs, list) or any(not isinstance(s, str) or not s.strip() for s in source_refs):
        raise FormalInputError("source_refs must be a list of non-empty strings")
    if not isinstance(timeout_ms, int) or isinstance(timeout_ms, bool) or not 1 <= timeout_ms <= 30000:
        raise FormalInputError("timeout_ms must be an integer between 1 and 30000")
    statuses = {"HYPOTHESIS", "OBSERVED", "TEST_FIXTURE", "SPECIFIED", "UNKNOWN"}
    epistemic_status = spec.get("epistemic_status", "HYPOTHESIS")
    if epistemic_status not in statuses:
        raise FormalInputError(f"epistemic_status must be one of {sorted(statuses)}")
    return {
        "schema_version": SCHEMA_VERSION,
        "claim_id": claim_id.stridef analyze_claim(spec: Mapping[str, Any]) -> dict[str, Any]:
    """Check explicitly supplied propositional formulas via the canonical typed-AST adapter.

    This frontend treats each textual premise as an explicit formal assumption unless
    a future version supplies per-premise source mappings. Top-level source_refs are
    retained as claim provenance metadata, but are not falsely attached to every premise.
    """
    normalized = _validate_claim(spec)
    from logic_proof.z3_adapter import check_entailment

    declared_variables = set(normalized["variables"])
    premise_asts = [
        FormulaParser(text, declared_variables).parse()
        for text in normalized["premises"]
    ]
    conclusion_ast = FormulaParser(normalized["conclusion"], declared_variables).parse()
    formal_spec = {
        "schema_version": "wanga-formal-fragment/1.0",
        "variables": {name: "Bool" for name in normalized["variables"]},
        "premises": [
            {
                "id": f"PREM-{index + 1}",
                "expr": _to_logic_ast(ast),
                "source_refs": [],
                "assumption": True,
            }
            for index, ast in enumerate(premise_asts)
        ],
        "conclusion": _to_logic_ast(conclusion_ast),
    }
    backend = check_entailment(formal_spec, timeout_ms=normalized["timeout_ms"])
    consistency = backend.get("premise_consistency", "UNKNOWN")
    backend_entailment = backend.get("entailment_status", "UNKNOWN")
    if consistency == "UNSAT":
        status = "INCONSISTENT_PREMISES"
        entailment = "NOT_EVALUATED"
    elif consistency == "UNKNOWN":
        status = "SOLVER_UNKNOWN_ON_PREMISES"
        entailment = "UNKNOWN"
    elif backend_entailment == "ENTAILED_WITHIN_ENCODED_FRAGMENT":
        status = "ENTAILED_WITHIN_ENCODING"
        entailment = "ENTAILED_WITHIN_PROPOSITIONAL_ENCODING"
    elif backend_entailment == "NOT_ENTAILED_COUNTERMODEL":
        status = "NOT_ENTAILED_BY_ENCODING"
        entailment = "COUNTERMODEL_FOUND"
    else:
        status = "SOLVER_UNKNOWN_ON_ENTAILMENT"
        entailment = "UNKNOWN"

    raw_countermodel = backend.get("countermodel")
    countermodel = None
    if isinstance(raw_countermodel, Mapping):
        countermodel = {
            name: str(value).casefold() == "true"
            for name, value in raw_countermodel.items()
        }
    solver_version = None
    try:
        from importlib.metadata import version
        solver_version = version("z3-solver")
    except Exception:
        pass

    return {
        "schema_version": "wanga-formal-check-result/1.0",
        "claim_id": normalized["claim_id"],
        "input_sha256": canonical_hash(normalized),
        "parser_version": PARSER_VERSION,
        "solver": "Z3_VIA_LOGIC_PROOF_TYPED_AST",
        "solver_version": solver_version,
        "premise_consistency": consistency,
        "premise_count": len(premise_asts),
        "variable_count": len(normalized["variables"]),
        "source_refs": normalized["source_refs"],
        "source_refs_supplied": bool(normalized["source_refs"]),
        "epistemic_status_before": normalized["epistemic_status"],
        "epistemic_status_after": normalized["epistemic_status"],
        "verification_status": "NOT_YET_VERIFIED",
        "formal_scope": "PROPOSITIONAL_LOGIC_ONLY",
        "formal_backend_status": backend_entailment,
        "explicit_formal_assumptions": [f"PREM-{index + 1}" for index in range(len(premise_asts))],
        "entailment": entailment,
        "status": status,
        "countermodel": countermodel,
        "reason_unknown": backend.get("reason_unknown"),
        "encoding_hash": backend.get("encoding_hash"),
        "semantic_boundary": (
            "The text frontend parses only the declared propositional grammar and delegates all solving "
            "to logic_proof.z3_adapter. Each premise is explicitly treated as a formal assumption; "
            "claim-level source_refs are not falsely attached to every premise. A solver result does not "
            "authenticate sources, validate natural-language translation, or establish empirical truth."
        ),
    }


iable_map)
            },
        })
    else:
        result.update({
            "status": "SOLVER_UNKNOWN_ON_ENTAILMENT",
            "entailment": "UNKNOWN",
            "solver_reason": entailment_solver.reason_unknown(),
        })
    return result


def analyze_claim_batch(specs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Run isolated claims; one malformed claim becomes an error row without hiding others."""
    if not isinstance(specs, Sequence) or isinstance(specs, (str, bytes)):
        raise FormalInputError("claims must be a sequence of objects")
    rows = []
    for index, spec in enumerate(specs):
        try:
            rows.append(analyze_claim(spec))
        except (ValueError, RuntimeError) as exc:
            rows.append({
                "claim_id": spec.get("claim_id") if isinstance(spec, Mapping) else None,
                "status": "INPUT_OR_DEPENDENCY_ERROR",
                "error": f"{type(exc).__name__}: {exc}",
                "batch_index": index,
                "verification_status": "NOT_YET_VERIFIED",
            })
    return {
        "schema_version": "wanga-formal-check-batch/1.0",
        "status": "COMPLETED_WITH_ERRORS" if any(row.get("status") == "INPUT_OR_DEPENDENCY_ERROR" for row in rows) else "COMPLETED",
        "claim_count": len(rows),
        "entailed_count": sum(row.get("status") == "ENTAILED_WITHIN_ENCODING" for row in rows),
        "not_entailed_count": sum(row.get("status") == "NOT_ENTAILED_BY_ENCODING" for row in rows),
        "inconsistent_premise_count": sum(row.get("status") == "INCONSISTENT_PREMISES" for row in rows),
        "unknown_count": sum("UNKNOWN" in row.get("status", "") for row in rows),
        "error_count": sum(row.get("status") == "INPUT_OR_DEPENDENCY_ERROR" for row in rows),
        "results": rows,
        "verification_status": "NOT_YET_VERIFIED",
    }
