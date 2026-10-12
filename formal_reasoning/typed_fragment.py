"""Safe, bounded typed Z3 adapter complementing the propositional formal_reasoning adapter.

This module checks only the supplied formal encoding. It does not translate
natural language, authenticate sources, or equate SAT with truth.
"""
from __future__ import annotations

import re
from typing import Any, Mapping

try:
    import z3  # type: ignore
except ImportError:  # Optional dependency: import should remain safe without it.
    z3 = None  # type: ignore

SCHEMA_VERSION = "wanga-formal-fragment/1.0"
_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,63}$")
_MAX_EXPR_DEPTH = 48
_MAX_EXPR_NODES = 512
_MAX_VARIABLES = 128
_MAX_PREMISES = 128
_ALLOWED_SORTS = {"Bool", "Int", "Real", "String"}
_ALLOWED_OPS = {"not", "and", "or", "implies", "eq", "neq", "lt", "le", "gt", "ge", "add", "sub", "mul"}


class FormalSpecError(ValueError):
    """Input is outside the declared, bounded formal fragment."""


class _Budget:
    def __init__(self) -> None:
        self.nodes = 0


def validate_formal_spec(spec: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(spec, Mapping):
        raise FormalSpecError("formal spec must be an object")
    if spec.get("schema_version") != SCHEMA_VERSION:
        raise FormalSpecError(f"schema_version must be {SCHEMA_VERSION}")
    variables = spec.get("variables")
    premises = spec.get("premises")
    conclusion = spec.get("conclusion")
    if not isinstance(variables, Mapping):
        raise FormalSpecError("variables must be an object")
    if len(variables) > _MAX_VARIABLES:
        raise FormalSpecError(f"variable count exceeds {_MAX_VARIABLES}")
    if not isinstance(premises, list) or len(premises) > _MAX_PREMISES:
        raise FormalSpecError(f"premises must be a list with at most {_MAX_PREMISES} items")
    if not isinstance(conclusion, Mapping):
        raise FormalSpecError("conclusion must be an expression object")
    for name, sort in variables.items():
        if not isinstance(name, str) or not _NAME.fullmatch(name):
            raise FormalSpecError(f"invalid variable name: {name!r}")
        if not isinstance(sort, str) or sort not in _ALLOWED_SORTS:
            raise FormalSpecError(f"unsupported sort for {name}: {sort!r}")
    ids: set[str] = set()
    for index, premise in enumerate(premises):
        if not isinstance(premise, Mapping):
            raise FormalSpecError(f"premise[{index}] must be an object")
        premise_id = premise.get("id")
        if not isinstance(premise_id, str) or not premise_id.strip() or premise_id in ids:
            raise FormalSpecError(f"premise[{index}] requires a unique non-empty id")
        ids.add(premise_id)
        if not isinstance(premise.get("expr"), Mapping):
            raise FormalSpecError(f"premise[{index}].expr must be an expression object")
        source_refs = premise.get("source_refs", [])
        if not isinstance(source_refs, list) or any(not isinstance(x, str) or not x for x in source_refs):
            raise FormalSpecError(f"premise[{index}].source_refs must be a list of non-empty strings")
        if not isinstance(premise.get("assumption", False), bool):
            raise FormalSpecError(f"premise[{index}].assumption must be boolean")
        if not source_refs and premise.get("assumption", False) is not True:
            raise FormalSpecError(
                f"premise[{index}] must cite at least one source_ref or be explicitly marked assumption=true"
            )
    # Validate AST shape/budgets independently of Z3 availability.
    for expr in [p["expr"] for p in premises] + [conclusion]:
        _validate_expr_shape(expr, 0, _Budget())
    return {
        "status": "VALID_FORMAL_FRAGMENT_SHAPE",
        "schema_version": SCHEMA_VERSION,
        "variable_count": len(variables),
        "premise_count": len(premises),
        "conclusion_present": True,
        "source_backed_premise_count": sum(1 for p in premises if p.get("source_refs")),
        "explicit_assumption_count": sum(1 for p in premises if p.get("assumption", False)),
        "semantic_status": "NOT_YET_VERIFIED",
    }


def _validate_expr_shape(expr: Mapping[str, Any], depth: int, budget: _Budget) -> None:
    budget.nodes += 1
    if budget.nodes > _MAX_EXPR_NODES:
        raise FormalSpecError(f"expression exceeds {_MAX_EXPR_NODES} AST nodes")
    if depth > _MAX_EXPR_DEPTH:
        raise FormalSpecError(f"expression exceeds depth {_MAX_EXPR_DEPTH}")
    if "var" in expr:
        if set(expr) != {"var"} or not isinstance(expr["var"], str) or not _NAME.fullmatch(expr["var"]):
            raise FormalSpecError("variable expression must be {'var': 'name'}")
        return
    if "const" in expr:
        if set(expr) != {"const"} or isinstance(expr["const"], (dict, list)) or expr["const"] is None:
            raise FormalSpecError("constant must be a scalar bool/int/float/string")
        if isinstance(expr["const"], float) and (expr["const"] != expr["const"] or abs(expr["const"]) == float("inf")):
            raise FormalSpecError("non-finite numeric constants are not supported")
        return
    op = expr.get("op")
    args = expr.get("args")
    if not isinstance(op, str) or op not in _ALLOWED_OPS or not isinstance(args, list):
        raise FormalSpecError(f"unsupported operator or missing args: {op!r}")
    expected_arity = 1 if op == "not" else (2 if op in {"implies", "eq", "neq", "lt", "le", "gt", "ge", "sub"} else None)
    if expected_arity is not None and len(args) != expected_arity:
        raise FormalSpecError(f"operator {op!r} expects {expected_arity} arguments")
    if op in {"and", "or"} and len(args) < 2:
        raise FormalSpecError(f"operator {op!r} requires at least two arguments")
    if op in {"add", "mul"} and len(args) < 2:
        raise FormalSpecError(f"operator {op!r} requires at least two arguments")
    if any(not isinstance(arg, Mapping) for arg in args):
        raise FormalSpecError(f"all arguments for {op!r} must be expression objects")
    for arg in args:
        _validate_expr_shape(arg, depth + 1, budget)


def _require_z3() -> None:
    if z3 is None:
        raise RuntimeError("z3-solver is not installed; install requirements-formal.txt")


def _mk_vars(declarations: Mapping[str, str]) -> dict[str, Any]:
    assert z3 is not None
    constructors = {"Bool": z3.Bool, "Int": z3.Int, "Real": z3.Real, "String": z3.String}
    return {name: constructors[sort](name) for name, sort in declarations.items()}


def _compile_expr(expr: Mapping[str, Any], variables: Mapping[str, Any]) -> Any:
    assert z3 is not None
    if "var" in expr:
        name = expr["var"]
        if name not in variables:
            raise FormalSpecError(f"undeclared variable {name!r}")
        return variables[name]
    if "const" in expr:
        value = expr["const"]
        if isinstance(value, bool):
            return z3.BoolVal(value)
        if isinstance(value, int):
            return z3.IntVal(value)
        if isinstance(value, float):
            return z3.RealVal(repr(value))
        if isinstance(value, str):
            return z3.StringVal(value)
        raise FormalSpecError(f"unsupported constant type: {type(value).__name__}")
    op = expr["op"]
    args = [_compile_expr(arg, variables) for arg in expr["args"]]
    try:
        if op == "not": result = z3.Not(args[0])
        elif op == "and": result = z3.And(*args)
        elif op == "or": result = z3.Or(*args)
        elif op == "implies": result = z3.Implies(args[0], args[1])
        elif op == "eq": result = args[0] == args[1]
        elif op == "neq": result = args[0] != args[1]
        elif op == "lt": result = args[0] < args[1]
        elif op == "le": result = args[0] <= args[1]
        elif op == "gt": result = args[0] > args[1]
        elif op == "ge": result = args[0] >= args[1]
        elif op == "add": result = args[0]
        elif op == "sub": result = args[0] - args[1]
        elif op == "mul": result = args[0]
        else:  # Protected by structural validation, kept as a fail-closed guard.
            raise FormalSpecError(f"unsupported operator: {op!r}")
        if op == "add":
            for value in args[1:]: result = result + value
        if op == "mul":
            for value in args[1:]: result = result * value
    except Exception as exc:
        if isinstance(exc, FormalSpecError):
            raise
        raise FormalSpecError(f"invalid typed expression for operator {op!r}: {exc}") from exc
    return result


def _compile_spec(spec: Mapping[str, Any]) -> tuple[dict[str, Any], list[Any], Any]:
    _require_z3()
    validate_formal_spec(spec)
    variables = _mk_vars(spec["variables"])
    premises = [_compile_expr(p["expr"], variables) for p in spec["premises"]]
    conclusion = _compile_expr(spec["conclusion"], variables)
    if any(not z3.is_bool(expr) for expr in premises):
        raise FormalSpecError("each premise must compile to a Boolean formula")
    if not z3.is_bool(conclusion):
        raise FormalSpecError("conclusion must compile to a Boolean formula")
    return variables, premises, conclusion


def _solver_result(solver: Any) -> dict[str, Any]:
    status = solver.check()
    if status == z3.sat:
        return {"status": "SAT", "reason_unknown": None}
    if status == z3.unsat:
        return {"status": "UNSAT", "reason_unknown": None}
    return {"status": "UNKNOWN", "reason_unknown": solver.reason_unknown()}


def check_consistency(spec: Mapping[str, Any], *, timeout_ms: int = 2000) -> dict[str, Any]:
    """Check satisfiability of the premises only; SAT is not truth."""
    variables, premises, _ = _compile_spec(spec)
    if not isinstance(timeout_ms, int) or not 1 <= timeout_ms <= 60000:
        raise ValueError("timeout_ms must be in [1, 60000]")
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    solver.add(*premises)
    result = _solver_result(solver)
    return {
        "schema_version": "wanga-formal-check-result/1.0",
        "check_type": "PREMISE_CONSISTENCY",
        "status": result["status"],
        "reason_unknown": result["reason_unknown"],
        "premise_count": len(premises),
        "variable_count": len(variables),
        "semantic_status": "NOT_YET_VERIFIED",
        "interpretation": {
            "SAT": "The encoded premises are jointly satisfiable; this does not establish truth.",
            "UNSAT": "The encoded premises are inconsistent in the supported formal fragment.",
            "UNKNOWN": "The solver did not determine satisfiability within the configured limits.",
        }[result["status"]],
    }


def check_entailment(spec: Mapping[str, Any], *, timeout_ms: int = 2000) -> dict[str, Any]:
    """Check premises ⊨ conclusion by separately checking consistency and P ∧ ¬C.

    The conclusion is supported as an entailment only if the premises are
    consistent and the conjunction of all premises with the negated conclusion
    is UNSAT in the encoded fragment.
    """
    variables, premises, conclusion = _compile_spec(spec)
    if not isinstance(timeout_ms, int) or not 1 <= timeout_ms <= 60000:
        raise ValueError("timeout_ms must be in [1, 60000]")
    consistency_solver = z3.Solver()
    consistency_solver.set(timeout=timeout_ms)
    consistency_solver.add(*premises)
    consistency = _solver_result(consistency_solver)
    if consistency["status"] == "UNSAT":
        return {
            "schema_version": "wanga-formal-check-result/1.0",
            "check_type": "ENTAILMENT",
            "premise_consistency": "UNSAT",
            "entailment_status": "BLOCKED_INCONSISTENT_PREMISES",
            "countermodel": None,
            "reason_unknown": None,
            "semantic_status": "NOT_YET_VERIFIED",
            "interpretation": "Premises are inconsistent; entailment is not accepted and no conclusion is promoted.",
        }
    if consistency["status"] == "UNKNOWN":
        return {
            "schema_version": "wanga-formal-check-result/1.0",
            "check_type": "ENTAILMENT",
            "premise_consistency": "UNKNOWN",
            "entailment_status": "UNKNOWN",
            "countermodel": None,
            "reason_unknown": consistency["reason_unknown"],
            "semantic_status": "NOT_YET_VERIFIED",
            "interpretation": "Premise consistency was not determined, so entailment is not evaluated as proven.",
        }
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    solver.add(*premises)
    solver.add(z3.Not(conclusion))
    result = _solver_result(solver)
    countermodel = None
    if result["status"] == "SAT":
        model = solver.model()
        countermodel = {
            name: str(model.eval(variable, model_completion=True))
            for name, variable in sorted(variables.items())
        }
    entailment_status = {
        "UNSAT": "ENTAILED_WITHIN_ENCODED_FRAGMENT",
        "SAT": "NOT_ENTAILED_COUNTERMODEL",
        "UNKNOWN": "UNKNOWN",
    }[result["status"]]
    return {
        "schema_version": "wanga-formal-check-result/1.0",
        "check_type": "ENTAILMENT",
        "premise_consistency": "SAT",
        "entailment_query_status": result["status"],
        "entailment_status": entailment_status,
        "countermodel": countermodel,
        "reason_unknown": result["reason_unknown"],
        "premise_ids": [p["id"] for p in spec["premises"]],
        "premise_source_refs": {
            p["id"]: sorted(set(p.get("source_refs", [])))
            for p in spec["premises"]
        },
        "encoding_hash": _hash_spec(spec),
        "semantic_status": "NOT_YET_VERIFIED",
        "interpretation": {
            "UNSAT": "Premises plus negated conclusion are unsatisfiable; the conclusion follows within this exact encoding and supported fragment.",
            "SAT": "A countermodel exists; the conclusion does not follow from these premises in this encoding.",
            "UNKNOWN": "The solver did not determine entailment within configured limits.",
        }[result["status"]],
        "truth_boundary": "A formal result is relative to the supplied encoding and assumptions. It does not authenticate sources or prove that a natural-language formalization is faithful.",
    }


def _hash_spec(spec: Mapping[str, Any]) -> str:
    import hashlib
    import json
    encoded = json.dumps(spec, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()
