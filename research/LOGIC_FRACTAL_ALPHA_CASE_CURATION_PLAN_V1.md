# Logic Fractal Alpha — Reviewed Case Curation Plan V1

**Status:** SPECIFIED — execution and release remain blocked until cases are reviewed.
**Purpose:** Build the first source-grounded evaluation set for the logical-model builder without treating solver correctness as proof that a source was interpreted correctly.

## Scope

This phase builds a curated benchmark, not a general natural-language reasoning model. It evaluates explicit formalizations in the propositional fragment. Typed Bool/Int/Real/String cases remain a separate track.

## Intake protocol

1. Select a source already recorded in `logic_wiki/data/articles.json`; record its license/permission scope.
2. Capture a stable locator and SHA-256 of the reviewed source span. Do not copy long copyrighted passages into the benchmark.
3. Write a concise claim paraphrase and mark its epistemic status: FACT, INTERPRETATION, HYPOTHESIS, or UNKNOWN.
4. A first reviewer writes variables, premises, conclusion and expected solver status.
5. A second reviewer independently checks that the formalization faithfully represents the claim within the declared fragment.
6. Add negative, boundary and counterexample cases, including plausible but invalid inferences.
7. Keep TRAIN, VALIDATION and HOLDOUT disjoint by source or source family where feasible. Do not tune against HOLDOUT.
8. Run the benchmark audit and preserve the JSON report, manifest hash, code revision and reviewer decisions.

## Minimum gate

The current intake contract requires at least 30 reviewed risk cases, coverage of TRAIN/VALIDATION/HOLDOUT, and at least three source classes. This is a minimum intake gate, not sufficient evidence for general intelligence or commercial readiness. Expand the set after reviewing error patterns.

## Required risk coverage

- NEGATIVE: premises do not entail the proposed conclusion.
- BOUNDARY: result changes or becomes unknown when a premise, type, quantifier, or domain condition changes.
- COUNTEREXAMPLE: an explicit model or assignment demonstrates the failure of a proposed inference.

## Metrics and interpretation

Report false-accept and counterexample-escape rates only where denominators exist. Empty or ineligible populations must be null/blocked, never 0%. Report source-mapping review coverage separately from solver accuracy. Solver results are relative to the formal encoding; they do not establish that the encoding matches natural language.

## Release decision

Do not promote a package to VERIFIED based on schema validity, synthetic fixtures, or one solver result. Require source review, independent formalization review, regression tests, reproducible report, and explicit approval metadata. Preserve failed cases as regression tests.

## Next implementation sequence

1. Curate and double-review the first 30 eligible risk cases.
2. Add per-case reviewer agreement and disagreement notes.
3. Generate a source-family leakage report for data splits.
4. Run a baseline and publish the failure taxonomy.
5. Only then decide whether a neural proposer, retrieval model, Lean integration, or probabilistic logic package is justified by measured failure modes.
