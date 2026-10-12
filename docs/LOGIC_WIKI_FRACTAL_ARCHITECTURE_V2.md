# Logic Wiki and Logical-Fractal Research Architecture V2

## Workspace boundaries

- `logic_wiki/data/articles.json`: article definitions, source references and editorial cross-links.
- `logic_wiki/data/fractal_taxonomy.json`: multi-scale concept map. Every current catalog relation remains `EDITORIAL_RELATION_CANDIDATE`, not entailment.
- `logic_fractal/data/composition_rules.json`: existing page/relationship composition contracts.
- `logic_fractal/data/recursive_composition_contracts_v1.json`: L0-L3 recursive composition proposal.
- `logic_fractal/fragment_composer.py`: typed candidate composition and provenance preservation.
- `scripts/ingest_conversation_export.py`: local export intake and hash generation.
- `scripts/run_logic_agents.py`: bounded source/catalog/composition/readiness/Wix-sync audit roles.
- `logic_wiki/data/readiness_gate.json`: release gate for a first reviewable model.
- `research/reports/logic-fractal/`: dated output, benchmark results and review records.

## Logic-fractal scales

- **L0 — source-grounded primitive:** exact span, typed claim or relation candidate, source/version/hash, scope and epistemic status.
- **L1 — typed fragment:** one or more units with an explicit input/output contract, preserved parents, source references and tests.
- **L2 — recursive candidate:** composed fragments with a declared rule, canonical hash, invariants and inherited scope.
- **L3 — model candidate:** a versioned multi-scale structure that has passed structural checks and is being evaluated against semantic benchmarks, counterexamples, holdout and MIRROR review.

An edge in the Wiki is a navigation/research relationship. A composition edge is a contract-driven operation. Neither is semantic entailment by default.

## First-model gate

The gate currently requires 20 sources across 3 source classes, 50 provenance-linked units, 20 composition contracts, 30 counterexamples, 100 semantic test cases in 3 suites, two independent reviews, a zero-dangling-reference state, unique stable IDs, a measured critical-contradiction inventory, deterministic reconstruction, holdout and MIRROR review. The thresholds are provisional project policy. They must be recomputed rather than hardcoded in run reports.

## Longitudinal upgrade loop

Every report must record the current catalog/model hashes. Future versions compare candidate maps and test outcomes to prior builds; retain regressions and rejected candidates. After the first model becomes review-ready, collection, critique and benchmarking continue. The initial release is a milestone, not the end of the research cycle.
