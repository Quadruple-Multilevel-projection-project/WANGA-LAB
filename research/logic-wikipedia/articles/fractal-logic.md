# Fractal Logic

Page ID: WIKI-FRACTAL-001  
Status: RESEARCH HYPOTHESIS; FIRST MODEL GATES DEFINED  
Related: M/L/N Continuous Field; The 231-Gate Combinatorial Map; Logic Before Weight.

## Proposed definition
Fractal logic is the hypothesis that small, source-backed logical fragments can be composed recursively into larger modules while preserving interfaces, derivation history and validation rules. A composed module may itself become a fragment at a higher scale. The relevant property is composable logical structure with testable invariants, not visual resemblance.

## Candidate fragment
Each fragment should record a stable ID/version; exact source spans or an explicit assumption; typed terms, variables, relations, rules and constraints; preconditions and postconditions; parent/child fragment IDs; composition interface and scale; tests, counterexamples, status and model hash.

## Proposed composition
compose(A, B, interface, constraints) → candidate C

Reject a composition when variables are unbound, interface types mismatch, lineage is lost, a prohibited dependency cycle appears, a conflict is hidden, or replay fails. Not every object should combine with every other object: compatibility must be typed and tested.

## Structural versus semantic similarity
Two fragments can have similar graph shapes but different meanings. Compare graph topology, interface signatures, source context, truth conditions/operational definitions, counterexamples and task tests. No layer substitutes for another.

## First-model acceptance
V0.1 must compose at least two fragments over two scales, produce deterministic hash and derivation trace, preserve conflicts, and pass positive/negative/boundary/adversarial tests. The output remains a candidate until independent review.

## Open questions
- Is self-similarity empirical, definitional or merely organizational?
- Which invariants survive composition across scales?
- How do different logic systems reconcile without collapsing meaning?
- How does the model find useful compositions rather than only enumerate combinations?
