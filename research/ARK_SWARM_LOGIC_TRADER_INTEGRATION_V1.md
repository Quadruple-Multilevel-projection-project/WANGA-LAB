# ARK-Swarm + Logic Trader Integration V1

**Status: BUILT AS A BOUNDED DETERMINISTIC RESEARCH PROTOTYPE · INTEGRATED TESTS REQUIRED · SEMANTIC VALIDITY NOT YET VERIFIED.**

## Objective

Connect the existing WANGA Logic Wiki, composition graph, typed-fragment composer, LNL/evidence checks and six-role integration harness into a first running ARK-Swarm + Logic Trader loop. The Logic Trader selects source-linked logic assets relevant to a declared task, composes catalog candidates and emits a candidate logic package with a provenance record. The swarm coordinator executes bounded specialist roles, evaluates their checks and records a deterministic event set.

## Data path

`task → Logic Trader lexical candidate ranking → Logic Wiki source/relation graph → candidate fractal compositions → selected source-backed package → typed-fragment composition check → counter-reading/MIRROR check → existing six-role agent suite → hashed event ledger + report`

## Implemented components

- `ark_swarm/logic_trader.py`: deterministic lexical ranking over article titles, categories and definitions; candidate graph construction through `logic_fractal.composer.build_candidate_model`; source-preserving candidate package assembly.
- `ark_swarm/coordinator.py`: runs source-integrity, Logic Trader, provenance, composition, typed-fragment, counter-reading and existing six-agent evaluation roles.
- `ark_swarm/swarm_state.py`: local grow-only event-set merge with idempotent/commutative union semantics and a shared validation-credit metric based only on explicit test outcomes.
- `scripts/run_ark_swarm.py`: command-line entry point.
- `ark_swarm/config/swarm-v1.json`: explicit runtime boundaries.
- `tests/test_ark_swarm_logic_trader.py`: tests for deterministic ranking, package source lineage, candidate status, swarm cycle, event merge semantics and collision rejection.
- `schemas/ark-swarm-cycle-report-v1.schema.json`: report contract.
- Outputs are written under `research/reports/ark-swarm/`.

## Relationship to current WANGA modules

- Logic Wiki articles/sources provide the current catalog.
- `logic_fractal/composer.py` creates auditable candidate paths from editorial relations already in the catalog.
- `logic_fractal/fragment_composer.py` checks typed interfaces and source/claim lineage for the separate synthetic fragment-fixture test.
- `scripts/evaluate_logic_agent_bundle.py` runs the existing six-role deterministic integration suite.
- The LNL model builder remains an explicit source/fact/rule/goal/constraint compiler; this integration does not bypass its evidence gates or automatically execute an LNL candidate.
- MLN continuous-field analysis remains separate; it is not silently turned into semantic relations.

## Logic Trader selection policy

The first version scores articles and candidate paths by lexical overlap with the task, with small source-count and relation-count tie-breakers. It is deterministic and inspectable, but **lexical relevance is not semantic relevance**. The report includes matched terms, score, source IDs, linked article IDs, candidate hash and the unchanged status of every selected item.

A candidate is not upgraded to `VERIFIED` because it was selected, composed or tested structurally. The release gate stays `BLOCKED_INTERNAL_CANDIDATE_ONLY` until real-source semantic benchmarks, counterexamples, independent review and reproducibility conditions are satisfied.

## Swarm semantics and current limits

Roles are deterministic software tasks in one local coordinator. The implementation does not claim separate neural agents or biological connectome execution. The event-set merge implements a local G-Set union function, but there is no P2P transport, network CRDT replication, authentication, shared dopamine/reward learning, dynamic code modification or autonomous production deployment. The validation-credit score summarizes tests; it does not update model weights.

## Bounded Z3 formal adapter

The bounded proposition parser/solver adapter is documented separately in [Formal Reasoning Adapter V1](FORMAL_REASONING_ADAPTER_V1.md). The integrated coordinator now includes a dedicated `formal-propositional-benchmark` role, which runs fixed propositional fixtures. Passing this role validates the adapter against these fixtures only; it does not translate natural language or verify the semantic correctness of the Logic Trader’s real-catalog package.

The workflow installs the pinned optional dependency from `requirements-formal.txt`, runs the formal adapter tests and writes `research/reports/formal-reasoning/benchmark-latest.json`.

## Running

```bash
python -m compileall -q ark_swarm scripts/run_ark_swarm.py
python -m unittest discover -s tests -p 'test_ark_swarm_logic_trader.py' -v
python scripts/run_ark_swarm.py
```

To test a different task:

```bash
python scripts/run_ark_swarm.py --task "Build source-grounded evidence gate logic"
```

The generated outputs are internal candidate artifacts and research reports. The scheduled workflow opens a PR for generated changes; it does not auto-merge or publish a candidate model to Wix.
