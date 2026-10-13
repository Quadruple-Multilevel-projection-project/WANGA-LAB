# WANGA Formal Reasoning Adapter V1 — Z3 and Hard-Gated Evaluation

**Status: BOUNDED PROPOSITIONAL PROTOTYPE · OPTIONAL DEPENDENCY PINNED · FIVE SYNTHETIC BENCHMARK CASES · NOT A NATURAL-LANGUAGE PROVER.**

## Purpose

This addition advances the P0 items in `research/ARK_SWARM_FULL_STACK_GAP_ANALYSIS_V1.md`: a restricted formal semantics contract, solver-backed checks, countermodel output, an explicit candidate evaluation vector, and CI coverage.

## Components

- `formal_reasoning/propositional.py`: parser for explicitly supplied propositional formulas with variables and operators `not/!`, `and/&`, `or/|`, `->/implies`, and `<->/iff`. It does not run `eval`, rejects undeclared symbols/unsupported syntax, and applies explicit limits to formula length, tokens, nesting, variable count, premise count and solver timeout.
- `formal_reasoning/benchmark.py`: runs a fixed set of five synthetic cases.
- `formal_reasoning/evaluation.py`: applies hard gates to a candidate metric vector. Its descriptive score never overrides a failed hard gate and never updates weights.
- `requirements-formal.txt`: pins the optional Z3 adapter dependency.
- `schemas/formal-claim-v1.schema.json` and `schemas/formal-check-result-v1.schema.json`: machine-readable input/output contracts.
- `scripts/run_formal_reasoning_benchmarks.py`: writes the benchmark report to `research/reports/formal-reasoning/benchmark-latest.json`.
- `tests/test_formal_reasoning.py`: parser, entailment, countermodel, premise-consistency, evaluation-gate and benchmark tests.

## Decision semantics

1. Parse every premise and conclusion only in the declared propositional grammar.
2. Test premise consistency first.
   - `SAT`: premises have at least one satisfying assignment.
   - `UNSAT`: premises are inconsistent; entailment is not evaluated.
   - `UNKNOWN`: solver did not decide; remain unresolved.
3. Only if premises are consistent, test `premises AND NOT conclusion`.
   - `UNSAT`: the conclusion follows from those encoded premises within this propositional fragment.
   - `SAT`: a countermodel is emitted; the conclusion is not entailed by this encoding.
   - `UNKNOWN`: unresolved.
4. Retain `epistemic_status` unchanged and always emit `verification_status=NOT_YET_VERIFIED`.

A solver result is relative to the formulas supplied. This adapter does not translate arbitrary natural language, authenticate source documents, prove empirical truth, emit a Lean-style proof object, or certify semantics outside the declared grammar.

## Candidate evaluation

The evaluator also hard-gates reviewed evidence coverage, false-accept rate and counterexample-escape rate. `source_coverage` means that each packaged claim/component has a resolvable source reference; `evidence_coverage` means that the cited spans have been reviewed against the specific claim. `false_accept_rate` is the share of known-invalid benchmark candidates incorrectly accepted; `counterexample_escape_rate` is the share of registered counterexamples not detected by the applicable gates. Missing metrics are rejected instead of defaulted to zero. These initial thresholds are `INITIAL_CONFIG_NOT_EMPIRICALLY_CALIBRATED` and must be measured on a labeled dataset before they are used as evidence of readiness.

The evaluation vector contains premise consistency, formal-check result, source coverage, benchmark accuracy, counterexample rate, holdout score, replay stability, and compute time. Each hard gate must pass. The weighted descriptive index is for reporting only; it cannot compensate for a failed hard gate. Thresholds load from `formal_reasoning/config/evaluation_policy.json` and are explicitly labeled `INITIAL_CONFIG_NOT_EMPIRICALLY_CALIBRATED`. The evaluator never updates weights or changes a claim status.

## ARK-Swarm integration

The adapter is wired into ARK-Swarm as the `formal-propositional-benchmark` role. The swarm reads the fixed five-case synthetic suite and includes the outcomes in its candidate/report metadata. It does **not** claim that these cases prove the selected real-catalog package. Candidate-level eligibility remains a separate metric contract and no candidate is automatically released or promoted to VERIFIED.


The formal smoke benchmark is added as a separate deterministic coordinator role. It checks five synthetic formulas and contributes a test result to the cycle report. This is not treated as semantic validation of the Logic Trader's selected real-catalog package.

## Run locally

```bash
python -m pip install -r requirements-formal.txt
python -m unittest discover -s tests -p 'test_formal_reasoning.py' -v
python scripts/run_formal_reasoning_benchmarks.py
```

## Next required work

- Increase to at least 30 source-grounded negative/boundary/counterexample cases before any candidate-release decision.
- Define a versioned compiler from a carefully scoped subset of LNL into this formal AST; do not map natural-language text directly into Z3 assertions.
- Add differential tests against truth tables for small formula sizes.
- Add independent review of the mapping from source-backed claims to declared formulas.
- Use holdout evaluation and calibration before changing candidate selection policy.
- Extend to first-order logic or Lean only through separate adapters and proof/result contracts.
