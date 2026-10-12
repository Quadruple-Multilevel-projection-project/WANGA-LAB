"""Bounded formal reasoning, typed AST checks, and candidate contracts for WANGA-LAB."""
from .propositional import analyze_claim, analyze_claim_batch
from .evaluation import evaluate_candidate
from .typed_fragment import (
    check_entailment as check_typed_entailment,
    check_consistency as check_typed_consistency,
    validate_formal_spec as validate_typed_formal_spec,
)
from .formalization_queue import queue_candidate_for_formalization
from .package_contract import validate_package_contract

__all__ = [
    "analyze_claim",
    "analyze_claim_batch",
    "evaluate_candidate",
    "check_typed_entailment",
    "check_typed_consistency",
    "validate_typed_formal_spec",
    "queue_candidate_for_formalization",
    "validate_package_contract",
]
