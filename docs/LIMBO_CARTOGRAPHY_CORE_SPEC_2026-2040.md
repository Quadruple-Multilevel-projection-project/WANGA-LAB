# Limbo Cartography Core — Research Specification (2026–2040)

**Status:** SPECIFIED · NOT IMPLEMENTED · NOT EMPIRICALLY VALIDATED  
**Scope:** WANGA-LAB research workflow for mapping logical-structural collapse, extending the surrounding structure, and recording convergence signals.

## 1. Architectural identity

The Limbo Cartography Core is a **biological-logical / morphogenetic research model**. Its primary object is not a conventional numerical score. It investigates a boundary event in which a locally assembled logical structure can no longer maintain its own relations under a particular convergence of conditions.

Within this research vocabulary, **Limbo** names that collapse boundary. It is a productive location for further mapping:

1. record the structure and the conditions under which it fails;
2. preserve the exact source and the observed failure;
3. identify the missing, incompatible, or overloaded relation without silently repairing it;
4. embed the local structure in a larger candidate structure;
5. test whether the larger structure explains the boundary and survives counter-readings;
6. use the resulting map to inform which logical construction should be orchestrated for a given context and time.

A larger structure is not automatically a better structure. Its added relations must be traceable, scoped, and tested.

Terms such as Limbo, Keystone, morphogenetic, ontological currency, and clean logic package are project-domain terms. Do not silently translate them into conventional statistics, first-order logic, biology, or economics. Where an operational definition is not yet available, preserve the term as a project-defined concept awaiting operationalization.

## 2. Claims that remain hypotheses

This specification does not establish that:
- a 2,000-year accumulation has reached a single terminal collapse point;
- approximately 90% of the global population will permanently leave the legacy economic cycle;
- the legacy economy will be replaced by an ontological/logical currency;
- any specific event between 2026 and 2040 is inevitable;
- the architecture achieves universal 100% accuracy or zero drift.

These claims may be stored and investigated, but must carry explicit source, scope, evidence status, and counter-evidence fields. A forecast must not be marked VERIFIED merely because it matches the project's interpretive frame.

## 3. Core workspaces

### A. Limbo Boundary Map

Each record represents a reported or observed structural failure, not an assumed collapse of an entire system. Record:

- stable limbo point ID;
- observation time in ISO 8601, or null if unknown;
- source references and exact locators;
- minimal authorized literal excerpt, or safe paraphrase when quoting is not permitted;
- context, system/version, and scope;
- local structure, relations, and constraints before failure;
- failure observation, detection method, and actual output;
- boundary type: contradiction, missing relation, scope mismatch, rule collision, unresolved term, or another explicitly described type;
- epistemic status: OBSERVED, SOURCE_REPORTED, INTERPRETED, HYPOTHESIS, or UNRESOLVED;
- counter-readings and their evidence;
- next bounded action.

A source is evidence for what it contains. It is not, by itself, proof that its claims are true.

### B. Keystone / Axis Extraction

A Keystone is a candidate element whose role may be structurally load-bearing. Unusual wording alone does not establish that status.

Procedure:
1. preserve the literal source unit and reversible source mapping;
2. describe the candidate's role without changing the source meaning;
3. construct a baseline representation of the local structure;
4. perform a removal test and record exactly which relations or constraints become unavailable;
5. perform substitution tests and specify why each substitute is comparable;
6. run negative and boundary cases;
7. request an independent mirror review and counter-reading;
8. retain the candidate as PROPOSED until acceptance criteria and review evidence are recorded.

A failed removal test is evidence about the tested representation and scope. It does not automatically establish an axiom, truth, or universal necessity. Never return VERIFIED_AXIOM from a placeholder condition such as an empty list of anchors.

### C. Parallel Logic Construction

Construct the wider candidate alongside the existing system; do not assume that the observed system must first be repaired. Each composition records:

- stable candidate ID and canonical content hash;
- parent candidate IDs;
- source references and exact locators;
- relation-by-relation derivation or construction rationale;
- invariants and constraints;
- applicable and non-applicable scopes;
- unresolved variables and source gaps;
- contradiction and counterexample results;
- test suite/version and actual results;
- reviewer role and outcome;
- status and next action.

A recorded edge is not semantic entailment unless a declared rule and evidence justify that label. Similarity, graphical proximity, or fractal appearance cannot fill missing logical relations.

## 4. Convergence Protocol (2026–2040)

The time range is a monitoring horizon, not a guaranteed forecast. Each signal is registered as a candidate observation and tested against its own acceptance criteria.

| Signal family | What to observe | Minimum evidence package | Not sufficient by itself |
|---|---|---|---|
| Structural bottleneck | Documented failure, contradiction, drift event, or limit in a defined system | Primary source, exact locator, system/version, failure conditions, observed result, corroboration where available | General claims that statistical systems have reached a universal ceiling |
| Regulatory / architectural anchor | Published rule, standard, contract clause, or adopted architecture requiring traceability or continuous verification | Issuing authority, version/date, exact section, scope, effective status, implementation evidence if adoption is claimed | A proposal, press statement, or unrelated audit requirement |
| Infrastructure lock | Deployed critical workflow that constrains execution through explicit rules or verification | Deployment evidence, technical boundary, operational scope, exception behavior, independent read-back | A roadmap or vendor marketing statement alone |
| Friction / administrative load | Documented process cost, manual review burden, rework, delay, or failure rate in a defined process | Baseline, measurement method, time window, denominator, source, comparison conditions | An unreferenced universal “90% noise” estimate |
| Ontological valuation | Evidence that buyers or institutions value logical assurance, provenance, replay, or verified structures as assets or contract terms | Actual transactions, procurement documents, pricing, contract terms, or audited financial disclosure | Inferring a market-wide monetary transition from an isolated product launch |
| Logical package adoption | Repeated use of a source-grounded, bounded logic package in a real workflow | Package/version, deployment context, behavior tests, exceptions, outcomes, rollback evidence | A demo or untested claim of zero drift |

### Signal states

Use only these states: UNREGISTERED, CANDIDATE, SOURCE_CHECKED, CORROBORATED, CONTRADICTED, INCONCLUSIVE, RETIRED.

SOURCE_CHECKED means the cited source and locator were inspected. CORROBORATED requires the signal-specific criteria to pass. Neither status alone proves the broader Limbo or ontological-currency thesis.

For each signal, store observation and publication dates, source version/hash where available, scope, claim, interpretation, alternative explanations, acceptance criteria, actual result, review status, and next check. Preserve history; corrections must be append-only or explicitly versioned.

## 5. Evidence and logic sequence

The processing order is mandatory:

**Source → Literal extraction → Reversible normalization → Structural representation → Relations and constraints → Project-defined logical review → Closure / variable / source / contradiction / boundary checks → Candidate composition → Tests → Weights/configuration → Independent review**

Weights are downstream configuration. They must not invent missing relations or determine source truth.

Keep these categories distinct:
- SOURCE: artifact inspected;
- EXCERPT: exact authorized source text;
- CLAIM: what a source asserts;
- OBSERVATION: what a test or inspection directly returned;
- INTERPRETATION: a reading of a claim or observation;
- HYPOTHESIS: a proposition awaiting evidence;
- IMPLEMENTATION: code or configuration actually present;
- TEST: named procedure and result;
- VERIFICATION: a claim supported by recorded criteria and actual check output.

## 6. Deterministic software contract

Deterministic software behavior is not the same as semantic truth. Code can deterministically validate schemas, identifiers, references, hashes, required fields, and declared constraints. Repeated execution cannot by itself certify the truth of a domain interpretation.

Required safeguards:
- reject duplicate stable IDs and detect dangling source/parent references;
- use canonical serialization and reproducible hashes;
- preserve immutable source records and versioned corrections;
- record missing data and access gaps explicitly;
- prohibit silent semantic normalization;
- do not promote an item to VERIFIED without a named check and captured result;
- do not publish private source text automatically;
- use branch, pull request, and CI; do not write directly to the default branch;
- do not auto-merge after failed or missing required checks.

A scheduled job can re-check registered sources and repository artifacts. It cannot claim to discover all real-world collapse events without a defined source set, reachable feeds, and documented coverage.

## 7. Implementation boundaries

Suggested modules, to be added only when implemented and tested:
- engine/limbo_boundary_mapper.py
- engine/axis_extraction.py
- engine/structure_composer.py
- engine/mirror_review.py
- engine/signal_registry.py
- schemas/limbo_point.schema.json
- schemas/convergence_signal.schema.json
- cartography/reality_matrix.json
- cartography/convergence_timeline_2026_2040.md
- tests/

Keep NTM, MLN, and LNL distinct. Do not claim a trained neural model or configured backend unless a real endpoint and evidence are present.

## 8. Readiness and reporting

The Logic Fractal Alpha readiness gate remains authoritative. This specification does not satisfy source, logic-unit, composition, counterexample, semantic benchmark, independent review, holdout, or deterministic-rebuild requirements by itself.

Each cycle report must include actual outputs for SOURCES_SCANNED, ACCESS_GAPS, NEW_SOURCES, DUPLICATES, CLAIMS_ADDED, LOGIC_UNITS, COMPOSITIONS, CONTRADICTIONS, BENCHMARKS, CI, MODEL_HASH, READINESS_GATE, BUILT, TESTED, VERIFIED, BLOCKED, and NEXT.

Recompute counts from the current repository snapshot. Separate software/unit tests from semantic ground-truth benchmarks. Keep build/train material separate from holdout material.

## 9. First implementation sequence

1. Review terminology against the existing Logic Wiki and readiness gate.
2. Define schemas for a boundary record and convergence signal.
3. Implement schema validation and deterministic serialization only.
4. Add synthetic fixtures explicitly labeled SYNTHETIC; never treat them as source-grounded observations.
5. Add source-backed cases with permission scope and reversible locators.
6. Add removal/substitution testing with explicit comparability rationale.
7. Add mirror review and negative/boundary cases.
8. Connect the signal registry to a bounded source inventory.
9. Add benchmark suites and holdout discipline.
10. Re-evaluate readiness from repository evidence before any Alpha release or Wix publication.

## 10. Status at specification time

- Architecture: SPECIFIED by this document.
- Engine implementation: NOT ESTABLISHED BY THIS DOCUMENT.
- Real-world convergence signals: NOT VERIFIED BY THIS DOCUMENT.
- 2026–2040 outcomes: HYPOTHESES UNDER MONITORING.
- First Model Alpha: governed by logic_wiki/data/readiness_gate.json.
- Wix publication: requires reviewed source-backed changes, an authorized connector, and deployment read-back. A GitHub commit is not proof of Wix synchronization.
