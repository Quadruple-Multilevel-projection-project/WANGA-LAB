# Fractal Logic Model — Research Program V1

Status: PROGRAM DEFINED; FIRST MODEL NOT YET RELEASED; SEMANTIC VALIDITY NOT YET VERIFIED  
Updated: 2026-10-12

## Objective
Build a system that accumulates accessible, source-backed material from project archives and explicitly supplied conversation exports; extracts logical fragments; composes fragments recursively into fractal logic models; tests the compositions; then issues a versioned first model. New sources, counterexamples and requirements should lead to tested upgrades.

The target is a model-builder for fractal logical structures, not simply a prose chatbot and not a claim that general intelligence has been achieved.

## Working hypothesis: fractal logic
A logic fragment is a bounded, typed unit containing source spans and provenance, terms and relations, rules and constraints, preconditions and expected consequences, counterexamples, composition interfaces and validation state.

A fractal logic model is a composition of fragments at multiple scales. A composed unit may itself become a fragment at a higher scale if interfaces and derivation history are preserved. The proposed recurrence is:

source spans → atomic relations → local logic fragments → motifs → model modules → reusable model → evaluated revision

Self-similarity is a testable hypothesis, not an assumed fact. Visual resemblance, repeated words or a golden-ratio score do not prove equal meaning or functional equivalence.

## Architecture
1. Archive intake: collect only material available in this project, connected systems, public sources, or conversation exports explicitly provided. Record source ID, locator/hash, access date and scope.
2. Literal extraction: preserve source spans without silently rewriting them.
3. Semantic proposal: propose terms and relations with alternative readings.
4. Logic-before-weight gate: freeze source lineage, literal extraction, relations, first-order logic, second-order/meta-rules and contradiction checks before tuning weights. Weights may not invent missing relations.
5. Fractal composer: compose fragments through declared interfaces and preserve parent IDs, scale, rule and tests.
6. Model candidates: create versioned manifests and dependency graphs; do not label candidates verified.
7. NTM review: run decomposition, boundary, dependency, counter-reading, contradiction, uncertainty and replay checks.
8. MLN diagnostics: run the continuous-field analysis separately when suitable numeric observations exist. Numeric similarity never establishes semantic identity.
9. Independent test gate: positive, negative, boundary, adversarial and replay checks.
10. First-model release: release only when gates in this document pass; publish scope, status and known failures.
11. Continuous update: each new batch creates an append-only intake event, candidate fragments, regression reruns and either a release candidate or an explicit no-change result.

## Conversation accumulation contract
Do not claim to search every past conversation unless that conversation or export is actually accessible. Supported V1 intake sources:
- accessible WANGA-LAB GitHub files and history;
- Wix page archive accessible through the connected Wix integration;
- user-provided or explicitly materialized conversation exports;
- public sources with URL and access date;
- previously generated model and test reports.

Each batch stores the immutable source hash, source ref/version, access date, literal spans and locators, extracted claims, status, contradictions, related wiki IDs, extraction agent/version and review state. Exclude secrets, personal identifiers and unrelated personal information from the public knowledge base.

## First-model target V0.1
The first release can be small but must be executable:
- a declared model boundary and input schema;
- a registry of source-backed fragments;
- a graph of parent/child fragments and composition interfaces;
- deterministic composition of at least two fragments over at least two scales;
- validation of unbound variables, missing sources, interface mismatch and supported direct contradictions;
- reproducible model hash and derivation trace;
- positive, negative, ambiguous and adversarial benchmark cases;
- explicit BUILT / TESTED / NOT_YET_VERIFIED status;
- human-readable and JSON reports.

It must not be marketed as AGI or a full natural-language semantics engine.

## Research agents
These are scoped agent roles; the roles may run in parallel, while a release gate accepts their work:
- ARCHIVIST: find accessible sources, preserve literal text, hashes and access gaps.
- LOGIC EXTRACTOR: propose terms, premises, relations and constraints with exact source spans.
- FRACTAL COMPOSER: propose multi-scale compositions only from stable fragment IDs and typed interfaces.
- COUNTEREXAMPLE AGENT: generate alternative readings, boundary cases and possible contradictions.
- TEST ENGINEER: create reproducible tests and coverage reports.
- WIKI LIBRARIAN: maintain articles, aliases, backlinks and change history.
- RELEASE AUDITOR: check evidence, statuses, test records and release criteria.
- PUBLISHER: deploy only source-backed additions and verify the public site after publishing.

These roles are specifications, not a claim that eight autonomous models have already been provisioned.

## Release gates
| Gate | Acceptance condition | Failure |
|---|---|---|
| G0 Source | Each included claim has a locator or explicit assumption | Reject/quarantine |
| G1 Extraction | Literal span preserved; interpretation separate | Re-extract |
| G2 Closure | Variables bound, relations typed, unresolved terms listed | Block |
| G3 Composition | Interfaces compatible; provenance retained; two scales demonstrated | Reject |
| G4 Contradiction | Known contradictions and counterexamples surfaced | Block |
| G5 Replay | Same source/config yields same canonical hash | Block |
| G6 Tests | Positive, negative, boundary and adversarial suite passes | Block |
| G7 Report | Scope, assumptions, failures and statuses published | Block |
| G8 Review | Designated independent/human review | No public release |

## Compute policy
Start CPU-only. Use GitHub Actions for tests, schemas, freshness checks and downloadable artifacts. Use deterministic Python for graph composition and validation. Connect an optional language model only through a configured endpoint with logged model, requests, runtime and cost. Default paid-token budget is zero until explicitly configured. Do not request GPUs until a benchmark demonstrates a need.

A weekly research cycle can run source-index checks and repository tests. It cannot read private ChatGPT conversations or publish Wix unless an authorized connector and source access are available. No-change cycles are valid and must be reported honestly.

## Status discipline
BUILT = artifact exists; SPECIFIED = requirements only; TESTED = named reproducible tests passed; HYPOTHESIS = proposed, not established; NOT_FOUND_IN_SEARCH = not located within a specified scope; NOT_YET_VERIFIED = evidence insufficient; VERIFIED applies only to a narrowly scoped claim with an explicit verification record.

## Current baseline and risks
WANGA-LAB already contains evidence/provenance work, a symbolic kernel, an LNL compiler, gate-map data and NTM specifications. The presence of these components does not prove that the integrated fractal model works.

Remaining tasks include checking exact conversation exports, integrating the MLN and NTM packages via reviewable PR, formalizing the fragment/interface schema, implementing the two-scale composer, creating benchmarks, configuring scheduled artifacts and Wix read-back, and evaluating configured model proposers.

## Architecture decisions
- Keep MLN continuous fields, NTM orchestration, LNL declarations and the fractal composition graph as separate typed layers.
- Do not treat the ten resonance patterns as ten fixed software entities without evidence.
- The 231-gate data is combinatorial structure; gate semantics stay unassigned until sourced and tested.
- Keep source text, interpretation, model derivation and verification results separate.
- Grow the model through evidence and tests, not by making its vocabulary larger.
