"""Bounded, optional formal checks for source-grounded WANGA logic packs."""
from .z3_adapter import check_entailment, check_consistency, validate_formal_spec
from .evaluation import evaluate_candidate

__all__ = ["check_entailment", "check_consistency", "validate_formal_spec", "evaluate_candidate"]
