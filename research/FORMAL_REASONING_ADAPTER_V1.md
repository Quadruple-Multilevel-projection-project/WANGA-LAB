# WANGA Formal Reasoning Adapter V1 — Text Frontend + Canonical Typed AST

**Status: BUILT ON BRANCH · CI VALIDATION PENDING · SYNTHETIC FIXTURES ONLY · SOURCE-GROUNDED SEMANTIC VALIDITY NOT YET VERIFIED.**

## Architecture decision

There is one solver execution layer: `logic_proof.z3_adapter`.

- `formal_reasoning.propositional` is a bounded text frontend for explicitly supplied propositional formulas. It parses a restricted grammar, converts its parsed tree into the typed AST, and delegates solving to `logic_proof.z3_adapter`. It does not call a separate Z3 solver implementation.
- `logic_proof.z3_adapter` validates explicit typed AST nodes and supports Bool, Int, Real and String variables with a bounded operator set. It requires every premise to contain source references or to be explicitly marked as an assumption.
- `logic_proof.formalization_queue` receives a Logic Trader candidate and records missing formal fields. It never infers a premise, conclusion, proof or AST from surface prose.
- `logic_proof.package_contract` validates the source-grounded package lifecycle and requires an independent review record for a `VERIFIED` package.
- Both evaluation interfaces read a single versioned threshold file: `formal_reasoning/config/evaluation_policy.json`.

## Decision semantics

1. Test encoded premise consistency.
   - `SAT`: at least one assignment satisfies the encoded premises; not a truth judgement.
   - `UNSAT`: the encoded premises are inconsistent; do not accept entailment.
   - `UNKNOWN`: the solver did not determine the result; keep it unresolved.
2. For consistent premises, test premises AND NOT conclusion.
   - `UNSAT`: the conclusion follows within the exact encoded fragment.
   - `SAT`: return a countermodel; the conclusion is not entailed by this encoding.
   - `UNKNOWN`: remain unresolved.
3. Preserve the input epistemic status and always return `NOT_YET_VERIFIED`.
4. Do not treat claim-level source references as evidence for every formal premise. The text frontend marks typed premises as explicit formal assumptions unless a future schema adds per-premise source mappings.
5. Never map SAT, one passing fixture, or an evaluation score to natural-language truth or automatic `VERIFIED` status.

The typed AST adapter is deliberately limited. It does not formalize arbitrary natural language, authenticate documents or prove that the encoding matches its source statement.

## Benchmarks

- Five propositional cases test the text-parser frontend and delegation.
- Seven typed-AST cases test the canonical solver adapter, countermodel, inconsistent-premise handling, explicit assumptions and malformed inputs.
- Both sets are synthetic adapter tests. They do not constitute source-grounded task benchmarks or prove that a Logic Trader-selected package is semantically correct.

## Shared candidate evaluation

The single policy `formal_reasoning/config/evaluation_policy.json` currently has status `INITIAL_CONFIG_NOT_EMPIRICALLY_CALIBRATED`. Gates cover premise consistency, formal entailment, source/evidence coverage, benchmark accuracy, false acceptance, counterexample escape, holdout and compute budget. Both evaluators require explicit metric inputs; missing holdout or compute measurements block eligibility for independent review. The score remains descriptive, no weights change, and no package promotes its own status.

## Run

```bash
python -m pip install -r requirements-logic.txt
python -m unittest discover -s tests -p 'test_formal_reasoning.py' -v
python -m unittest discover -s tests -p 'test_logic_proof_adapter.py' -v
python -m unittest discover -s tests -p 'test_logic_proof_benchmark.py' -v
python -m unittest discover -s tests -p 'test_logic_package_contract.py' -v
python -m unittest discover -s tests -p 'test_logic_formalization_queue.py' -v
python -m unittest discover -s tests -p 'test_logic_json_schemas.py' -v
python scripts/run_formal_logic_benchmark.py --out research/reports/ark-swarm/formal-logic-benchmark-latest.json
```

## Remaining evidence requirement

Before candidate release, add at least 30 source-grounded negative, boundary or counterexample cases; preserve exact source spans and per-premise provenance; compare against an independent holdout set; measure false acceptance and counterexample escape; and have an independent reviewer inspect the formalization. The current synthetic test suites are not a substitute.
