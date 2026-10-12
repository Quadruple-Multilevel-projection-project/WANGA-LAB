# WANGA Formal Logic Package Contract V1

## Purpose

A Logic Trader candidate is not automatically a formal model. This contract defines the structured handoff from source-linked candidate package to reviewed formal AST, and from there to a bounded solver result and candidate evaluation record.

## Contract lifecycle

1. **Candidate generated** — Logic Trader selects catalog assets and preserves article/source IDs, definitions, relations and candidate hash.
2. **Formalization queued** — `logic_proof.formalization_queue` records each candidate claim and missing fields. It does not generate a formal AST from prose.
3. **Formal representation reviewed** — premises, conclusion, variable declarations, assumption scope, source links and a counterexample suite are explicitly supplied.
4. **AST validation** — `logic_proof.z3_adapter` checks AST schema, variable declarations, operator/arity rules, expression depth and node budgets. Every premise must have source references or `assumption=true`.
5. **Formal check** — first check premise consistency, then premises AND NOT conclusion. Preserve SAT/UNSAT/UNKNOWN distinctions and countermodels.
6. **Candidate evaluation** — use the shared `formal_reasoning/config/evaluation_policy.json` with explicit source/evidence coverage, benchmark, false-accept, counterexample-escape, holdout, replay and compute metrics. Missing metrics fail closed.
7. **Independent release review** — a `VERIFIED` lifecycle state requires an independent reviewer record, evidence refs and the SHA-256 of a benchmark report. Neither a candidate nor its score can self-approve.

## Why two frontends are retained

`formal_reasoning.propositional` accepts a restricted textual propositional grammar. It converts only that explicit grammar into the common typed AST and delegates all solver execution to `logic_proof.z3_adapter`. It marks each textual premise as an explicit formal assumption unless a future format explicitly maps source evidence to each premise.

`logic_proof.z3_adapter` is the canonical solver backend. It accepts a typed AST fragment with Bool/Int/Real/String declarations and returns a result relative to that encoding. This is not arbitrary natural-language formalization.

## Evidence boundary

A source reference is provenance metadata, not a proof that the source is true. A formal proof is relative to encoded assumptions. Source authenticity, correctness of the formalization, empirical validity and generalization require separate checks.

## Current status

- Typed AST adapter, queue and package lifecycle contract: implemented on this branch, CI pending.
- Synthetic suites: 5 propositional frontend cases and 7 typed AST cases.
- Shared policy: initial thresholds not empirically calibrated.
- Source-grounded benchmark: not yet complete.
- Production P2P/CRDT, connectome execution, online RL and self-modifying code: not part of this change.
- Candidate release: blocked until real-source formalization and independent evaluation.

## Validation commands

```bash
python -m pip install -r requirements-logic.txt
python -m unittest discover -s tests -p 'test_logic_proof_adapter.py' -v
python -m unittest discover -s tests -p 'test_logic_proof_benchmark.py' -v
python -m unittest discover -s tests -p 'test_logic_package_contract.py' -v
python -m unittest discover -s tests -p 'test_logic_formalization_queue.py' -v
python -m unittest discover -s tests -p 'test_logic_json_schemas.py' -v
```
