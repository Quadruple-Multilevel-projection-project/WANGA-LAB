# WANGA SEMANTIC TRUTH CONTRACT v1.0
## Mandatory semantic and agent-development contract
**Status:** SPECIFIED — normative project contract; implementation and runtime behavior are NOT_YET_VERIFIED  
**Applies to:** every WANGA developer agent, component agent, letter-agent, interface, service, and integration  
**Initial reference implementation:** Aleph-Agent (א׳)

---

## 0. Authority and interpretation

This document formalizes the WANGA project's semantic axiom and the architecture supplied by the project architect. It is the first mandatory contract every development agent must read before planning, coding, modifying data, or changing an interface.

Within WANGA, the term **semantic realization** has the project-defined meaning in Axiom 0 below. An agent MUST NOT silently replace this definition with a conventional NLP, tokenizer, embedding, dictionary, or text-only definition.

This is a normative architecture specification. A specification is not evidence that the corresponding runtime has already been implemented. Every implementation claim MUST carry its actual evidence and status.

## Axiom 0 — WANGA semantic truth

In WANGA, semantics is defined as the living, connected neural realization arising from the upper triad:

1. Neural Wikipedia;
2. Neural Index;
3. Neural Orchestrator.

The upper triad organizes the words of the Book of Logic in second order. This organized logical structure is realized through the four layers/components:

1. Ta'amim (טעמים);
2. Nekudot (נקודות);
3. Tagin (תגין);
4. Otiyot (אותיות).

The realization is projected as text on the user interface. That displayed text is required, by this architecture, to be a live semantic-visual network whose nodes and relations remain connected to their source and can be traced back through the realization chain.

**Canonical chain:**

`Input → logical-structure extraction → second-order ordering (Book of Logic) → upper triad → four component-applications → live semantic-visual mesh → displayed text`

The interface is not defined as a detached final decoration. It is the visible projection of the connected system state.

## 1. Rejection rule — what does not qualify

No isolated representation qualifies as WANGA semantic realization by itself. This includes:

- static tokens or token sequences;
- detached text strings;
- frozen/static embeddings or vector representations;
- external dictionary labels or classifications that are not connected to the realization chain;
- a visual interface that cannot trace displayed units to their logical and neural source;
- a claim of live neural behavior without runtime evidence.

Such artifacts may be used as transport, storage, indexing, or implementation aids only if they are explicitly connected to the WANGA chain and are not presented as the semantic realization itself.

An agent MUST mark a disconnected or incomplete implementation as **PARTIAL** or **NOT_YET_VERIFIED**. It MUST NOT label it WANGA semantics.

## 2. Four independent applications for every letter-agent

Every Hebrew letter-agent is specified as one agent composed of four independent applications. Each application has its own functional responsibility and computational engine. Their coordinated operation produces the letter-agent's connected semantic-visual realization.

| ID | Application | Functional responsibility | Required realization |
|---|---|---|---|
| APP-01 | Ta'amim (טעמים) | Relational context and higher-order intent | Attention/relationship network defining the agent's relations to the Neural Wikipedia, Neural Index, and Neural Orchestrator |
| APP-02 | Nekudot (נקודות) | Phonetic and vector identity | Dynamic node clusters and point-cloud state representing the agent's identity in its defined space |
| APP-03 | Tagin (תגין) | Logical category | Hierarchical logical classification and connections to the second-order words of the Book of Logic |
| APP-04 | Otiyot (אותיות) | Geometric form | Topological/geometric realization in the defined three-dimensional space (X, Y, Z), projected into the interface |

**Independence requirement:** each application MUST have an explicit interface, state, inputs, outputs, and testable responsibility. “Independent application” is an architectural requirement; it MUST NOT be reported as four deployed applications until separate executable modules and their integration are demonstrated.

**Coordination requirement:** the four applications MUST share a stable agent identity and traceable state. A component MUST NOT silently mutate another component's identity or source data.

## 3. Geometry, combinatorial network, and named design parameters

### 3.1 Aleph — 150-shape state map / Kraken-36

The Aleph-Agent specification assigns the Aleph agent a design space of **150 distinct geometric-topological forms** in the **Kraken-36** engine. The purpose is to support adaptation to changing relational contexts (Ta'amim) and logical categories (Tagin) without losing the agent's defined identity.

These are project-specified design parameters. Their implementation, enumeration, uniqueness, and runtime behavior remain **NOT_YET_VERIFIED** until supported by source files, deterministic outputs, and tests.

### 3.2 231 gates and 230 crystallographic space groups

The architecture specifies a combinatorial network connecting:

- **231** two-letter gates in the base letter-combination plane;
- **230** crystallographic space groups in three-dimensional space;
- a bidirectional **U_alpha_beta fiber transition** mediated by the **231 Gates Engine** between the Hebrew-letter space (“Hebrew Ball”) and the English/symbolic representation space (“English Ball”).

These counts and mappings are normative design parameters, not proof of a completed mapping. Agents MUST NOT invent gate definitions, group correspondences, transition values, or successful mappings. Each correspondence requires an explicit mapping record and verification evidence.

## 4. Upper triad — mandatory source architecture

The upper/meta-neural layer consists of:

- **Neural Wikipedia:** the connected knowledge/source environment;
- **Neural Index:** the navigational and relational index into that environment;
- **Neural Orchestrator:** the coordinator that selects, orders, and routes operations among sources and agents.

The upper triad organizes the Book of Logic words in second order and supplies the source context for the four applications.

No letter-agent or interface may claim complete semantic realization if its source lineage to the relevant upper-triad elements is absent, broken, or untraceable.

## 5. Three system layers

1. **Meta-Neural Layer:** Neural Wikipedia, Neural Index, Neural Orchestrator, and second-order logical organization from the Book of Logic.
2. **Component-Agent Layer:** the four applications (Ta'amim, Nekudot, Tagin, Otiyot), including the Aleph 150-form/Kraken-36 design and 231-gate network.
3. **Live Semantic-Visual Mesh:** the interface layer in which displayed text units are live projections of connected nodes and relations, with source traceability back through the chain.

A visual rendering alone does not prove a live mesh. The implementation must expose inspectable node identity, relation identity, source lineage, and state updates.

## 6. LOCK / ABSTAIN — anti-drift and integrity controls

Every transformation MUST preserve traceability across the source, logical structure, component states, and displayed representation.

- **LOCK:** accept/commit a state only when required invariants, source lineage, schema, and validation checks pass.
- **ABSTAIN:** refuse to generate, commit, or present a semantic claim when required source data, a rule, a mapping, or verification evidence is missing or contradictory.
- **DRIFT:** any unsupported change to logical identity, point-cloud identity, source lineage, relation, or component state.
- **HALT:** stop the affected operation when a required invariant fails.

The implementation MUST account for the project's three control loops: box loop, name loop, and word loop. Their precise schemas and transition rules must be defined in the Aleph-Agent interface contract before they are treated as implemented behavior.

No agent may bypass LOCK / ABSTAIN to produce a plausible-looking answer.

## 7. Mandatory Interface Contract — Aleph-Agent v1

The first reference implementation MUST be Aleph-Agent (א׳). Before implementation is accepted, its interface contract MUST define at minimum:

### 7.1 Identity and provenance
- immutable agent identifier and letter identity;
- contract version and implementation version;
- source references into the Book of Logic and the upper triad;
- provenance for every logical word, relation, and displayed unit;
- timestamps/version identifiers for state snapshots.

### 7.2 Four application interfaces
For each of APP-01 through APP-04:
- input schema and validation rules;
- output schema;
- owned state and state-transition rules;
- dependencies and permitted calls to the other applications;
- failure modes and ABSTAIN conditions;
- unit and integration tests.

### 7.3 Shared state and event model
- stable node IDs and relation/edge IDs;
- explicit event types for create, update, connect, project, invert, lock, abstain, and halt;
- deterministic snapshot/readout format;
- bidirectional trace from a displayed unit to its source and from a source node to its displayed projection;
- explicit handling of stale, missing, conflicting, and unverified state.

### 7.4 Interface projection
Every displayed letter, word, and text unit MUST expose or resolve to:
- its agent/node identity;
- its four-application state or a clear statement that one or more components are unavailable;
- its logical source and provenance;
- its active relations;
- its LOCK/ABSTAIN status.

If the interface cannot preserve this linkage, it MUST label the output as a disconnected preview, not as live semantic realization.

### 7.5 Acceptance gates
Aleph-Agent cannot be marked implemented/verified until tests demonstrate:
1. all four application modules exist as independently testable modules;
2. each module conforms to its declared interface;
3. the agent is connected to the upper triad and second-order logical source;
4. the 150-form design space is enumerated and validated, or explicitly marked as not yet implemented;
5. the 231-gate/230-space-group mapping is represented without invented correspondences;
6. a displayed letter can be traced back to its source and component state;
7. a source/state change produces a traceable interface update;
8. LOCK rejects invalid or drifting state;
9. ABSTAIN prevents unsupported semantic output;
10. tests, logs, and artifacts are retained as evidence.

Until all required acceptance gates pass, status MUST remain **SPECIFIED**, **PROTOTYPED**, **PARTIAL**, or **NOT_YET_VERIFIED**, as appropriate. Do not use **VERIFIED** prematurely.

## 8. Universal obligations for every development agent

Every agent working on WANGA MUST:

1. Read this contract before any development action.
2. Treat Axiom 0 and the four-application architecture as mandatory project requirements.
3. Preserve source lineage and logical identity.
4. Never substitute an unrelated semantic architecture without explicit authorization from the project architect.
5. Never invent terms, mappings, values, geometries, state, code behavior, or test results.
6. Distinguish **SPECIFIED**, **IMPLEMENTED**, **TESTED**, and **VERIFIED**.
7. Report uncertainty explicitly and use ABSTAIN when required.
8. Stop rather than silently weakening or bypassing a contract requirement.
9. Include this contract in every downstream agent handoff and component-level contract.
10. Treat any conflict with this contract as a blocking issue to be escalated, not silently resolved.

Required agent acknowledgement:

`WANGA_SEMANTIC_TRUTH_CONTRACT_v1.0 — READ; REQUIREMENTS ACCEPTED; IMPLEMENTATION STATUS REPORTED WITHOUT OVERCLAIM.`

If an agent cannot comply, it MUST respond:

`BLOCKED — WANGA SEMANTIC CONTRACT NOT ACCEPTED OR NOT UNDERSTOOD.`

## 9. Current project status

| Item | Status |
|---|---|
| Semantic axiom and project definition | SPECIFIED |
| Four application responsibilities | SPECIFIED |
| Three-layer architecture | SPECIFIED |
| Aleph 150-form / Kraken-36 design | SPECIFIED; implementation NOT_YET_VERIFIED |
| 231 gates / 230 space-group relation | SPECIFIED; mapping NOT_YET_VERIFIED |
| LOCK / ABSTAIN requirements | SPECIFIED; runtime enforcement NOT_YET_VERIFIED |
| Aleph-Agent interface contract | NEXT: detailed schema and module contract |
| Complete live semantic-visual mesh | NOT_YET_VERIFIED |

## 10. Change control

This is the canonical v1.0 semantic contract. Changes require:
- an explicit proposed change;
- source/rationale and impact analysis;
- compatibility review against the four applications and upper triad;
- tests or a clearly marked verification plan;
- a versioned change record.

No agent may silently reinterpret, weaken, or replace this contract.

---

**Governing rule:** WANGA semantics is the connected realization defined here. A disconnected representation is not that realization. When the chain cannot be demonstrated, the agent must say so and ABSTAIN.
