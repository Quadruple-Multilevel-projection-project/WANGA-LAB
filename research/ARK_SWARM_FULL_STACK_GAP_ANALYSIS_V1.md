# ARK-Swarm + Logic Trader — Full-Stack Gap Analysis V1

**Audit date:** 2026-10-12  
**Basis:** uploaded research note `Pasted text.txt`, current WANGA-LAB implementation, and official project documentation checked for the shortlisted libraries.  
**Status:** DESIGN AUDIT · NO NEW SCIENTIFIC CLAIMS VERIFIED BY THIS DOCUMENT.

## Executive conclusion

The research note proposes a broad stack of 100+ libraries spanning spiking neural networks, connectomics, agent orchestration, P2P/CRDT, reinforcement learning, symbolic reasoning, ingestion, and evolutionary optimization. The current implementation is narrower and valuable as a deterministic first kernel:

- Logic Trader ranks source-linked Logic Wiki entries by lexical overlap plus small source/relation tie-breakers.
- ARK-Swarm Coordinator runs bounded software roles locally.
- The fractal composer assembles candidates from editorial catalog relations.
- The typed-fragment composer has a synthetic two-level composition probe.
- The local G-Set event ledger records role results; it does not network-replicate them.
- The existing six-role harness and GitHub Actions generate test reports and candidate artifacts.
- LNL compiles explicitly declared source/fact/rule/goal/constraint input, but is not a complete arbitrary-language semantics layer.
- MLN remains a numerical/operator research subsystem and does not independently prove meaning.
- The output remains `INTERNAL_CANDIDATE_NOT_RELEASED` / `NOT_YET_VERIFIED`.

**The next additions should be interfaces and validation layers, not wholesale installation of the entire library list.** There is no demonstrated need yet for 100+ dependencies, four fully simulated connectomes, GPU training, network P2P, or online reinforcement learning in the first model.

## Current capability ledger

| Area | Present implementation | Missing capability |
|---|---|---|
| Logic asset selection | Deterministic lexical ranking | Semantic retrieval / evaluated task relevance |
| Logic composition | Editorial relation graph + bounded candidate composition | Explicit typed semantics for each relation and proof-preserving composition |
| Evidence | Catalog source IDs and provenance checks | Exact spans/quotes, source-version resolution, evidence adjudication and provenance coverage benchmarks |
| Formal logic | LNL compiler and structural gates | Solver-backed interpretation for a declared supported fragment |
| Counter-reading | MIRROR member-order candidate | Logical negation/alternative derivation generated from actual formal semantics |
| Agent runtime | Bounded local coordinator and deterministic role functions | Queue/scheduler, separate model-provider interface, timeout/retry/resource policy |
| Shared state | Local grow-only event set, deterministic hash | Authenticated transport, durable replicated state, conflict/replay protocol |
| Reward | Test-outcome ratio for report only | A calibrated, multi-objective acceptance score; no validated learning/reward loop exists |
| Neural/connectome | Role abstractions only | Versioned dataset adapters, simulation experiments, task-level validation |
| Learning/RSI | Candidate artifacts and PR/CI | Candidate archive, benchmark-driven selection, holdout, rollback; no live self-modifying code |
| Publication | GitHub artifacts and existing Wix integration | Reviewed cross-system release manifest and published/read-back version association |
| Compute | CI-based CPU validation | Evidence of a GPU/training need, resource budget and measured scaling target |

## Prioritized additions

### P0 — Required before calling the output a logical model

**Existing on main:** `formal_reasoning/propositional.py`, its propositional benchmark and hard-gated evaluation policy. **Added in this branch (pending CI):** a typed Boolean/Int/Real/String AST complement, a seven-case synthetic fixture suite, a source-preserving formalization queue, a fail-closed logic-package lifecycle contract, schemas/tests, and ARK-Swarm integration. The new typed adapter complements the existing propositional implementation; it does not replace it or claim arbitrary natural-language formalization.

1. **Formal semantics contract.** Extend the catalog/typed-fragment format with explicit type signatures, relation meaning, variable scope, assumptions, premises, conclusion, allowed inference rule, applicable domain and failure conditions. A relation label or visual edge is not enough to infer entailment.
2. **Bounded proof/constraint adapter.** The branch now contains an optional Z3 adapter for a deliberately restricted formal fragment. It must distinguish:
   - `SAT`: the encoded constraints have a satisfying assignment.
   - `UNSAT`: the encoded constraints have no satisfying assignment.
   - `UNKNOWN`: no determination was established.
   To test whether premises entail conclusion `P`, encode the premises and `not P`; an `UNSAT` result supports entailment only within that exact encoding and logic fragment. Check the premises for consistency separately so an inconsistent premise set does not vacuously pass every conclusion. Never map `SAT` alone to “true”, “proven”, or a positive reward.
3. **Benchmark and counterexample suite.** Seven synthetic adapter fixtures now cover entailment, countermodel, inconsistent premises, Boolean implication, unsupported operator and undeclared-variable rejection. This is adapter self-test only. Add source-grounded positive, negative, boundary, ambiguous, contradictory, missing-source and adversarial cases with expected structured outcomes. Separate development, validation and holdout cases; ensure exact replay by input hash.
4. **Logic asset contract.** Each pack must include stable ID/version, typed input/output, premises, claims, source references and spans, constraints, composition rule, tests, known limits, changelog and status. Fail closed when source IDs or required fields are missing.
5. **Reward/evaluation ledger.** A first hard-gated evaluation ledger is now implemented; it records an auditable evaluation vector without changing weights. It must be validated on source-grounded cases. Replace “shared dopamine” as a truth metaphor with an explicit auditable evaluation vector: proof check, premise consistency, source coverage, benchmark accuracy, counterexample rate, generalization/holdout score, deterministic replay and compute cost. Hard gates cannot be averaged away by a high aggregate score. The first implementation records scores only; it must not update model weights.
6. **Candidate comparison and release gate.** Compare candidate and baseline on the same frozen suite; retain failed candidates and rollback evidence. No auto-promotion from `TESTED` to `VERIFIED`.

### P1 — Needed to produce better candidate models

7. **Model-proposer interface.** Add a provider-neutral interface for an optional LLM to propose primitive mappings, rules or alternative compositions. Disabled by default until a provider is explicitly configured. All proposals go through the same formal/evidence gates; model confidence is not proof.
8. **Retrieval beyond keyword overlap.** Add a task benchmark for current lexical ranking, then compare it against a graph/metadata baseline and, only if justified, embedding retrieval. Record precision@k, recall@k, source coverage and false-selection rate. Do not replace deterministic scores without comparison evidence.
9. **Agent runtime contract.** Standardize input/output JSON Schemas, timeouts, bounded retries, cancellation, idempotency, role version, source refs, error states and resource budget. Keep orchestration separate from reasoning content.
10. **Evolution archive.** Store candidate variants with parent hashes, mutation description, score vector, test results and rollback link. Use Pareto or constrained selection. Candidate mutation happens in a sandbox/branch; never monkey-patch the live coordinator.
11. **Probabilistic logic option.** Consider ProbLog only for explicitly probabilistic facts/rules and calibrated uncertainty tasks. Keep probability of a query separate from proof, empirical truth and source authenticity.
12. **Observability.** One report per cycle: inputs, repository/data versions, sources, selected assets, composition trace, solver outputs, benchmark deltas, rejected proposals, runtime/cost, agent failures, next action and artifact hashes.

### P2 — Distributed swarm and connectome research

13. **Transport and network security.** Define peer identity, authorization, message schema/version, signatures, replay protection, duplicate handling, key rotation, privacy boundaries, timeouts and recovery before P2P. Current G-Set is local only. A grow-only set cannot remove a bad event; corrections must be append-only superseding events or a different state type.
14. **CRDT choice by data semantics.** Do not call the local event-union function “network CRDT sync”. Pick a CRDT separately for each shared data type, document conflict semantics and test partitions, duplicate delivery, out-of-order delivery, concurrent edits and malicious/stale peers. A JS/TS CRDT library is not a direct Python drop-in.
15. **Connectome data registry.** For each proposed organism, add dataset name/version/license/access date/coordinate and neuron ID conventions/synapse semantics/known incompleteness/preprocessing hash and reproducible task. Current repo has no evidence that the proposed biological datasets are imported into ARK-Swarm.
16. **One bounded connectome pilot.** Start with the smallest data-grounded experiment and test a narrow behavior hypothesis against a reference. OpenWorm c302 documents a 302-neuron C. elegans model and validation work; this makes it a plausible pilot, not a proof that a worm connectome transfers to AI agent intelligence. Treat Drosophila/FlyWire, zebrafish and mouse MICrONS as separate data adapters and validation tracks. The zebrafish entry needs a specific dataset/version and target behavior before assigning a model role.
17. **Neural simulator decision.** Select one simulator for a stated experiment only after defining the question, data format and metric. Brian2, Nengo and snnTorch solve different engineering needs. Do not install all SNN libraries into the core. c302/NeuroML is a connectome-model track, not a general AI agent.
18. **Reward learning only after the environment exists.** Build a replayable environment and verify its reward labels before RLlib, Google Dopamine or other RL tooling. Reward a measured task outcome, not just a satisfying solver result. Keep model training and the formal validator as separate components.

### P3 — Scale after evidence of need

19. Distributed RL / Ray workers / GPU compute.
20. Graph database or GNN; first benchmark the JSON catalog and in-memory graph.
21. Multi-objective evolutionary search libraries such as Nevergrad/PyGAD after the baseline archive and fitness metrics are stable.
22. Detailed multi-species connectome simulation, neuromorphic hardware backends and online RSI only with a research question, resources and reproducible evaluation.

## Library decision matrix — shortlist, not an install list

| Need | First candidate | Decision now | Reason / gate |
|---|---|---|---|
| Formal constraints | Z3 / z3-solver | **P0 pilot** | Restrict to explicitly encoded claims/constraints; test SAT/UNSAT/UNKNOWN and entailment separately. |
| Proof-producing mathematics | Lean 4 / LeanCopilot | **P1 research track** | LeanCopilot assists proof search using language models; integrate only with version-pinned Lean and kernel-checked proof artifacts. |
| Probabilistic rules | ProbLog | **P1/P2 opt-in** | Useful when probabilities are explicitly part of the model; not a source-truth meter. |
| In-memory graph | Existing JSON graph first; NetworkX if needed | **No dependency yet** | Measure catalog size/query latency before changing representation. |
| Multi-agent environment/training | RLlib + Gymnasium/PettingZoo | **P2** | Requires a defined environment, observation/action spaces and validated reward. Not needed to run the current deterministic agent roles. |
| P2P | py-libp2p / libp2p protocol | **P2 prototype only** | Current public Python implementation reports ongoing maturity work; security and protocol tests must precede production. |
| CRDT | Keep local G-Set; evaluate a compatible implementation later | **P2** | Automerge is JSON-like with repository/network adapters in its JS/TS ecosystem; do not assume it can be imported into Python directly. |
| Active inference | pymdp | **P2 research option** | Models are defined over discrete state/observation/action spaces; requires an explicit generative model and evaluation. |
| General SNN | Choose Brian2 OR Nengo OR snnTorch for one experiment | **P2** | Different simulators, training methods and runtime trade-offs; no evidence yet that this is needed for the logical model core. |
| Connectome pilot | OpenWorm c302 | **P2 data/model adapter** | Start with documented C. elegans model; do not equate biological topology with agent semantics. |
| Drosophila data | FlyWire/FlyBrainLab | **P2 adapter** | Pin dataset version, units and extraction pipeline; validate any inferred role against tasks. |
| Mouse data | MICrONS dataset portal | **P2 adapter** | MICrONS exposes versioned EM/connectivity/functional data; select a specific release and ROI before using. |
| Web ingestion | Existing authorized export intake; Playwright only if needed | **P0 provenance; P2 browser automation** | Store source, exact spans, retrieval time, hashes and permissions; no access-control bypass or broad unbounded scraping. |
| Evolution/RSI | Internal deterministic candidate archive first; Nevergrad/PyGAD later | **P1 archive, P3 library** | Need stable objectives, candidate lineage, holdout and rollback before evolutionary search. |
| Compute | GitHub Actions existing CPU workflow | **P0 resource logging** | Add cost/runtime limits; only request GPUs or paid resources after a measured need and approval. |

## Mandatory semantic corrections to the research note

- **Z3 SAT is not a proof that a natural-language statement is true.** SAT means the encoded assertions are jointly satisfiable. Entailment requires a formalization and a specific unsatisfiability check such as premises plus negated conclusion. `UNKNOWN` stays unresolved.
- **A proof checker cannot authenticate premises.** It verifies a conclusion relative to specified assumptions and formal rules; source authenticity and empirical truth are separate gates.
- **A reward signal is not “dopamine” in the biological sense.** It can be a software metric. A QED result, SAT result or lower uncertainty alone must not automatically raise model trust or change weights.
- **ProbLog probability is model-relative.** It is computed from encoded probabilistic facts/rules; it is not automatically a calibrated measure of the truth of a retrieved source.
- **Active inference requires a specified generative model.** It is not a generic plug-in that automatically reduces all logical uncertainty.
- **Connectome role assignment is a research hypothesis.** Mapping C. elegans to a filter, Drosophila to navigation, zebrafish to fast anomaly response or mouse cortex to prediction requires a specific task, adapter and independent metric.
- **Fractal shape does not prove logical validity.** Every composition still requires typed contracts, meaning-preserving definitions, source lineage and counterexamples.
- **The uploaded note’s financial/crypto/market examples are outside this integration scope.** “Logic Trader” in this program means selection, composition and evaluation of logical assets, not a trading or betting system.

## Acceptance gates for the next cycle

1. Matrix and config pass schema/integrity validation.
2. The Z3 adapter returns `SAT`, `UNSAT` and `UNKNOWN` correctly on fixed formal fixtures and never maps SAT directly to truth.
3. At least 30 source-grounded counterexample/boundary cases exist before candidate release.
4. A benchmark reports current lexical ranking baseline, false selections and provenance coverage.
5. A candidate variant cannot change source records, policy gates or be promoted by its own score.
6. Any optional LLM output has prompt/model/version provenance and is independently checked.
7. Network sync remains off until peer auth, message validation and partition/replay tests pass.
8. The four proposed connectome tracks have dataset-specific manifests and task-level validation before being connected to the agent coordinator.

## Official references checked

- Z3 solver result semantics: https://z3prover.github.io/api/html/classz3py_1_1_solver.html
- ProbLog language and probabilistic rules: https://dtai.cs.kuleuven.be/problog/index.html
- LeanCopilot proof assistance and requirements: https://github.com/lean-dojo/LeanCopilot
- Ray RLlib environments and multi-agent training: https://docs.ray.io/en/latest/rllib/rllib-env.html
- py-libp2p status and feature breakdown: https://github.com/libp2p/py-libp2p
- GossipSub protocol and implementation status: https://github.com/libp2p/specs/blob/master/pubsub/gossipsub/README.md
- Automerge repository/network model: https://automerge.org/docs/reference/repositories/
- pymdp active inference: https://github.com/infer-actively/pymdp
- snnTorch training/simulation tutorials: https://snntorch.readthedocs.io/en/stable/tutorials/index.html
- Nengo simulator and backends: https://www.nengo.ai/documentation/
- OpenWorm c302: https://docs.openworm.org/preview/integrate-design-documents/Projects/c302/
- MICrONS dataset portal: https://www.microns-explorer.org/

**Decision:** The bounded proof adapter, synthetic tests and first hard-gated evaluation record are now configured in this research branch. The remaining P0 work is source-grounded formalization, real counterexample/holdout cases and an independent review gate. Build the proof/evidence/benchmark/reward contracts first. Keep the swarm local and deterministic. Then pilot one neural/connectome dataset. Do not add all libraries at once.

## Implementation delta after the initial audit snapshot

The current research branch adds the first P0 proof/evidence contracts (pending GitHub CI in this branch):

- `requirements-formal.txt` is the existing optional dependency file; this branch adds `jsonschema` there for schema tests and reuses the installed Z3 dependency.
- `formal_reasoning/typed_fragment.py` supports a bounded explicit AST for Boolean, integer, real and string variables; checks premise consistency separately; tests entailment through premises plus the negated conclusion; and preserves `UNKNOWN`.
- Every formal premise must have a source reference or be explicitly marked as an assumption.
- `formal_reasoning/evaluation.py` records hard-gated metrics without aggregating away failed gates, updating weights or promoting a package to `VERIFIED`.
- `formal_reasoning/package_contract.py` and the JSON Schemas require explicit semantics, sources, tests, known limits, and independent release-approval metadata for any verified lifecycle state.
- `formal_reasoning/typed_benchmark.py` supplies seven **synthetic adapter fixtures**, not a source-grounded semantic benchmark.
- `formal_reasoning/formalization_queue.py` preserves candidate claims/source IDs and lists missing formal fields. Logic Trader outputs with natural-language definitions are queued as `NOT_FORMALIZED`; Z3 is not run on them and no AST is fabricated.
- ARK-Swarm runs both the synthetic proof-adapter fixture gate and formalization-queue gate, and writes `logic-formalization-queue-latest.json` beside the candidate/report artifacts.

This makes the boundary explicit: the solver can check an encoding after it exists; it does not translate arbitrary language into faithful logic, validate a source's authenticity, or determine empirical truth.


## Implementation delta: reuse canonical formal_reasoning

The repository's current `formal_reasoning/` module already supplies a bounded propositional parser, Z3 adapter, five synthetic benchmark cases and a hard-gated evaluation policy. The integration branch **extends that module instead of adding a second top-level proof engine**:

- `formal_reasoning/typed_fragment.py`: optional Boolean/Int/Real/String AST adapter for explicitly encoded typed expressions; no natural-language formalizer.
- `formal_reasoning/typed_benchmark.py` and `formal_reasoning/examples/typed_formal_cases.json`: seven synthetic adapter fixtures.
- `formal_reasoning/formalization_queue.py`: source-linked surface definitions stay `NOT_FORMALIZED` until an explicit AST is authored/reviewed; Z3 does not run on raw article prose.
- `formal_reasoning/package_contract.py`: fail-closed lifecycle and independent release-approval contract.
- New schemas and tests are added to the existing formal-reasoning CI workflow.
- `ark_swarm/coordinator.py` adds formalization-queue and typed-benchmark roles and writes queue/benchmark reports alongside the candidate.

The typed extension is complementary to `formal_reasoning/propositional.py`, not a replacement. Both return `NOT_YET_VERIFIED` for solver checks; only the main propositional adapter remains the existing canonical logic-language parser. Synthetic fixture passes verify implementation behavior, not source-grounded semantic validity.


## Post-merge implementation and CI snapshot — 2026-10-12

The typed formal reasoning extension has been merged into `main` in PR #114. The final PR-head Logic Fractal Wiki Research workflow passed, as did Repository Integrity, WANGA Ecosystem Agent Sweep and both CodeQL analyses.

Verified in that run:
- Existing propositional formal adapter: 18 tests passed.
- Typed AST adapter: 9 tests passed.
- Typed formal fixture benchmark: 7/7 synthetic cases passed.
- Formalization queue: 3 tests passed.
- Logic package contract: 5 tests passed.
- Formal package/queue schemas: 6 tests passed.
- Existing Logic Wiki, typed fragment composition, source intake and ARK-Swarm integration tests passed.
- ARK-Swarm cycle: 10/10 role checks passed; zero failed roles. Candidate ID: `LT-c1918183cff25c53`.
- Logic Wiki build: 28 articles, 17 sources, 523 composition candidates; readiness remains `NOT_READY_INTERNAL_CANDIDATE_ONLY`.

These are software/integration results. The seven typed-formal cases are synthetic adapter fixtures, not source-grounded semantic benchmarks. No candidate was promoted to `VERIFIED`; no weights were updated. The next P0 requirement remains source-grounded formalization, negative/boundary cases, holdout testing and independent review.



## Source-grounded benchmark intake scaffold

A versioned schema and runner have now been added on the research branch: `schemas/source-grounded-logic-benchmark-case-v1.schema.json`, `schemas/source-grounded-logic-benchmark-manifest-v1.schema.json`, `formal_reasoning/examples/source_grounded_benchmark_manifest.json`, and `scripts/audit_source_grounded_logic_benchmark.py`. The initial manifest is intentionally empty. The runner will report `BLOCKED_INSUFFICIENT_REVIEWED_CASES`, with null rates, until source-backed cases are explicitly formalized/reviewed and the case count, risk types, splits, source-class and metric gates all pass. The file contract records source URI IDs, span locator and hash; the runner checks IDs/schema and review status but **does not fetch or re-hash the underlying website span**, so that source-span hash is a reviewer attestation and must be checked during ingestion/review. Synthetic test fixtures are excluded from readiness metrics.
