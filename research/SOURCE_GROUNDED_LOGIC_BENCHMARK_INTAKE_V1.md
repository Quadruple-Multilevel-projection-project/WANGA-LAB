# Source-Grounded Logic Benchmark Intake V1

**Status: INTAKE CONTRACT CONFIGURED · ZERO REVIEWED CASES IN SEED MANIFEST · MODEL RELEASE BLOCKED.**

## Purpose

The current formal-reasoning fixtures test that the parser/solver behaves as designed. They are synthetic and cannot be counted as source-grounded semantic evidence. This intake contract supports the next Logic Fractal Alpha gate: accumulate reviewed, source-linked negative/boundary/counterexample cases without automatically converting article prose to formulas.

## Case flow

1. Record a public/licensed source ID that exists in `logic_wiki/data/articles.json`.
2. Record an exact locator (page/section/line range or stable source selector) and SHA-256 for the cited span. The benchmark file stores the hash and locator instead of copying private or copyrighted source passages.
3. Preserve the original claim text as a short reviewed paraphrase or reference, not as a claimed proof.
4. A reviewer explicitly defines a propositional formalization: variables, premises and conclusion.
5. A second source/formalization review accepts the mapping as faithful **within the declared propositional fragment**.
6. The runner checks the exact solver status. Any changed or missing status is a failed case; `UNKNOWN` remains unknown.
7. Only reviewed cases count toward the reviewed benchmark gate. Unformalized cases remain queued and are not passed to Z3.

## What the runner reports

- source reference resolution and span metadata validity;
- total cases, reviewed cases, risk cases and splits;
- per-case result versus the expected formal status;
- false-accept rate among known risk cases;
- counterexample-escape rate among counterexample cases;
- evidence-review coverage of the case registry;
- run/case hashes and a readiness decision.

A low case count yields `BLOCKED_INSUFFICIENT_REVIEWED_CASES`, not a fabricated pass. An empty registry has null rates, not 0.0. False-accept and counterexample rates use only reviewed cases with an explicit expected result. These metrics are not evidence about arbitrary natural language beyond the specific, reviewed encodings.

## Candidate compatibility decision

- **Z3 propositional adapter:** FITS for explicit Boolean premises/conclusions after reviewed formalization.
- **Typed AST adapter:** FITS as a separate experimental track when a case needs Bool/Int/Real/String expressions. Typed cases do not silently count as propositional cases.
- **LNL:** source/rule intake and future formalization interface; no automatic text-to-AST mapping is enabled.
- **ProbLog, LeanCopilot, active inference, RLlib, SNN simulators and P2P:** not included in this benchmark runner; keep deferred until their input contracts and task-specific benchmarks exist.

## Run

```bash
python scripts/audit_source_grounded_logic_benchmark.py
python -m unittest discover -s tests -p 'test_source_grounded_logic_benchmark.py' -v
```

Release stays blocked until there are at least 30 reviewed NEGATIVE/BOUNDARY/COUNTEREXAMPLE cases, coverage of TRAIN/VALIDATION/HOLDOUT, three source classes, and the separate whole-program test/review requirements. This benchmark is one gate, not the entire Alpha release checklist.
