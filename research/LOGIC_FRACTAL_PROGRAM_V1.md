# Logic Fractal Model Program V1

**Status:** RESEARCH PROGRAM DEFINED · FIRST MODEL NOT YET RELEASED · READINESS THRESHOLDS PROVISIONAL.

## Objective
Build a cumulative research system that collects source-grounded logical structures from accessible project conversations, exported conversation files, research papers, public repositories and WANGA archives; normalizes them into a versioned corpus; composes candidate logical fractals; tests counterexamples and benchmarks; and emits the first model only when an explicit readiness gate passes. After the first candidate, keep accumulating evidence and issue versioned improvements.

A **logical fractal** is defined for this research programme as a recursively composable logical structure: primitives and relations form substructures; validated substructures may compose into higher-level structures while preserving typed constraints, source lineage, boundaries and tests. Self-similarity alone is not logical validity.

## Separate computational layers
1. **Logic Wiki and source corpus:** sources, claims, stable concept IDs, primitives, relations, counterexamples and test records.
2. **Logic-fractal builder:** composition, recursive maps, dependency checks, bounded model proposals and counter-reading.
3. **MLN continuous field:** a separate numerical measurement/operator research subsystem. Its measurements do not replace source semantics.
4. **LNL:** the current explicit contract language for source/fact/rule/goal/constraint declarations. It is useful but is not the whole proposed model.

## Source-first method
1. Register source identity, URI or conversation-file reference, date/version, page/span, language, permission scope and hash where bytes are available.
2. Extract literal units without silently rewriting meaning.
3. Separate quotation, source claim, interpretation, hypothesis, design proposal, implementation and measured result.
4. Normalize only technical or reversible structural details; preserve the original and mapping.
5. Identify primitives, relations, operators, constraints and boundaries.
6. Formalize first-order relations where definitions permit it.
7. Review second-order/meta-level claims separately; a higher-level rule is not automatically second-order logic.
8. Check variable binding, source support, contradictions, boundaries, counterexamples and unresolved assumptions.
9. Only after closure checks, consider weights/parameters. Weights and fractal resemblance cannot invent missing source relations.
10. Record acceptance/rejection with evidence for status changes.

## First model readiness gate
These are configurable project thresholds, not universal scientific cutoffs. They start as CONFIGURED_NOT_EMPIRICALLY_VALIDATED.

- At least 50 logical-unit candidates with exact source references.
- At least 20 source/conversation records across 3 source classes.
- At least 20 composition rules with typed inputs, outputs, constraints and provenance.
- At least 30 negative, boundary or counterexample cases.
- At least 100 reproducible tests across 3 benchmark suites.
- Zero duplicate stable IDs or dangling source references.
- No unresolved critical contradiction in the release core.
- A separated holdout evaluation set, deterministic build hash and replay.
- A counter-reading/red-team cycle and two independent review cycles.

Until the gate passes, generated structures remain INTERNAL_CANDIDATE_NOT_RELEASED. Passing it permits review of Logic Fractal Alpha; it does not prove AGI, universal correctness or complete natural-language understanding.

## Agent roles
- **Conversation Collector:** ingests only accessible conversation material or user-provided exports; reports missing access explicitly.
- **Source Registrar:** records source identity, version, span and retrieval date; URL alone does not verify a claim.
- **Logic Extractor:** creates literal units and relation candidates without repairing missing source content.
- **Logic Normalizer:** creates typed primitives and reversible mappings.
- **Fractal Composer:** composes primitives/substructures with invariants and provenance.
- **Mirror Reviewer:** produces counter-readings, contradictions and boundary failures; counter-reading is not truth.
- **Benchmark Evaluator:** runs frozen tests and reports actual execution metrics.
- **Wiki Curator:** updates versioned articles and relation maps with visible epistemic statuses.
- **Report Publisher:** opens GitHub PRs, builds Wix sync manifest and confirms writes via read-back.

## Compute and scheduling
Start with GitHub Actions runners for schema validation, deterministic graph build, tests and report generation. Record runner minutes and artifact sizes. Configure an external model/local model only after profiling and explicit cost approval. No paid cloud resources are created here.

GitHub Actions can process content present in the repository. It cannot autonomously read all private ChatGPT history. Conversation exports must be placed in research/inbox/conversations or an accessible Library location. The existing daily WANGA Unified Work Loop has been updated to search actual accessible material, report gaps, and continue independent tasks.

## Publication and evidence policy
- Every article has a stable ID, source list, relations, version and last-reviewed status.
- Keep SOURCE_REFERENCE_LOCATED, SOURCE_SUPPORTED, PROPOSED, IMPLEMENTED, TESTED and VERIFIED separate.
- Automated schema validity is not claim truth.
- Wix entries should link to their GitHub article/source, and the GitHub record should link back to Wix.
- Scheduled generation opens or updates a PR; it does not write directly to main.
- Wix sync is complete only after a successful write and read-back. Otherwise mark BLOCKED.

## Typed multi-scale fragment composition

The page-graph composer and the typed-fragment composer solve two different tasks.

- The page-graph composer creates auditable navigation/path candidates from article relations already declared in the Logic Wiki catalog.
- The typed-fragment composer composes logic fragments through explicit input/output types, preserves every parent ID and source span, raises an error on missing required interfaces, creates a canonical hash, and labels the result CANDIDATE.
- The first candidate builder composes a synthetic observation fragment into a relation fragment (scale 1), then composes that candidate with a review fragment (scale 2). Its release gate stays blocked because these are synthetic fixtures, not a reviewed extraction from the conversation archive, and the negative/boundary benchmark and independent review are not complete.

This separates graph exploration from executable logical composition. Neither type compatibility nor article adjacency establishes semantic entailment.

## Current milestones
1. Establish data schema, seed glossary, article renderer and readiness gate.
2. Add conversation-export inbox and source/claim manifest.
3. Add recursive composition graph with edge-level provenance.
4. Build positive, negative, boundary and counterexample benchmark suites.
5. Produce initial source audit and readiness report.
6. Publish the Logic Wiki landing page and link the GitHub registry.
7. Generate a first internal candidate; release only if the readiness gate passes.
8. Continue daily collection and weekly repository builds with independent blocked/completed statuses.

## Limitations
The exact conversation from two days earlier has not been fully retrieved. Available context includes the Logic Mine tracks, NTM work, LNL/MLN material and the source-first-before-weights rule. This is a starting corpus, not proof of complete conversation coverage or of the future-market hypothesis.

## ARK-Swarm + Logic Trader integration

The first bounded integration is implemented in `ark_swarm/`. The Logic Trader ranks entries in the versioned Logic Wiki catalog by lexical overlap and source/link metadata, then packages a source-preserving candidate composition. The ARK-Swarm coordinator runs catalogue integrity, provenance, fractal graph composition, typed-fragment fixture tests, a counter-reading candidate and the existing six-role integration suite.

- `ark_swarm/logic_trader.py`: ranked logic assets and candidate package.
- `ark_swarm/coordinator.py`: bounded role coordinator and candidate reports.
- `ark_swarm/swarm_state.py`: local G-Set event union and test-only validation credit.
- `scripts/run_ark_swarm.py`: executable entry point.
- `research/ARK_SWARM_LOGIC_TRADER_INTEGRATION_V1.md`: architecture and runtime limits.

The first output is `INTERNAL_CANDIDATE_NOT_RELEASED`. Lexical overlap is not semantic understanding; type compatibility is not semantic equivalence. The current runtime is local and deterministic. Peer-to-peer transport, network CRDT replication, biological connectome execution, online reward learning, external language-model generation, and automatic publication remain NOT_IMPLEMENTED or NOT_CONFIGURED.


## Typed formal-fragment and formalization queue extension

The existing `formal_reasoning/` propositional adapter remains the canonical parser for the supported propositional language. The merged ARK-Swarm integration adds a complementary typed AST adapter for Boolean, integer, real and string expressions, plus a seven-case synthetic fixture suite. Logic Trader output is stored in `formal_reasoning/formalization_queue.py` with source IDs and missing-field diagnostics; its natural-language descriptions are not converted into formulas automatically. The coordinator emits a formalization queue artifact and stays `NOT_YET_VERIFIED` until the candidate has explicit formalization, source review, counterexamples and independent approval.

Run checks with:

```bash
python -m unittest discover -s tests -p 'test_formal_typed_fragment.py' -v
python -m unittest discover -s tests -p 'test_formal_typed_benchmark.py' -v
python -m unittest discover -s tests -p 'test_formalization_queue.py' -v
python -m unittest discover -s tests -p 'test_logic_package_contract.py' -v
python -m unittest discover -s tests -p 'test_formal_package_schemas.py' -v
python scripts/run_typed_formal_benchmark.py --out research/reports/formal-reasoning/typed-fragment-benchmark-latest.json
```

The added fixtures are synthetic adapter tests, not a source-grounded semantic benchmark. P2P, connectome execution, RL updates and self-modifying code remain separate future work.
