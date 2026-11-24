# WANGA RECURSIVE NEURAL AGENT CONTRACT v1.0
## Foundational contract for agents inside the Recursive Neural Hyper-Architecture

**Document status:** SPECIFIED — future architecture and normative development requirements  
**Runtime status:** NOT_YET_VERIFIED  
**Governing contract:** `WANGA_SEMANTIC_TRUTH_CONTRACT_V1.md`  
**Applies to:** every WANGA agent, sub-agent, application-agent, orchestration agent, index agent, knowledge-space agent, and semantic-visual interface node.

---

## 0. Purpose and scope

This contract defines how an agent is to be specified and developed within the WANGA Recursive Neural Hyper-Architecture.

The architecture is not specified as a conventional chatbot plus database, nor as a detached MCP/JSON pipeline whose only responsibility is to transfer records to a screen. Its target model is a recursively connected network in which information-bearing structures, executable behavior, agent identity, state, and interface projections remain linked as parts of one traceable system.

The phrase **living neural network** is an architectural term in this project. It describes the intended stateful, relational, recursively connected behavior. It does not, by itself, establish biological neural activity, consciousness, physical energy transfer, or a deployed runtime. Such claims require separate evidence.

This document is a specification, not proof of implementation.

## 1. Governing semantic authority

Every agent MUST first read and comply with:

1. `WANGA_SEMANTIC_TRUTH_CONTRACT_V1.md`;
2. this contract;
3. the relevant component-specific contract and source materials assigned to its role.

The WANGA semantic axiom remains authoritative. An agent MUST NOT replace the project's definition of semantic realization with a conventional NLP, token, embedding, dictionary, or text-only definition.

The Book of Logic and its authorized source materials remain the authority for the project's logical terms. Agents MUST NOT invent, expand, normalize, or silently reinterpret the defined term set.

## 2. Core architectural principle — network within network

An agent is specified as a **stateful relational node** embedded in a larger network.

At minimum, its contract must account for:

- **Identity:** stable identity of the agent and the component it represents.
- **State:** inspectable current state and versioned state history.
- **Relations:** explicit links to source nodes, peer agents, parent agents, and projections.
- **Lineage:** traceable origin of every accepted logical term, relation, and projected unit.
- **Transformation history:** record of the ordered transformations through which the current state was derived.
- **Interaction:** defined response to incoming events and user interaction.
- **Integrity:** LOCK, ABSTAIN, DRIFT, and HALT behavior.
- **Projection:** a traceable representation of the agent's current state in the semantic-visual interface.

These are required design properties. They do not imply that every property is already implemented.

### 2.1 No detached output

An agent MUST NOT treat its visible text as an untraceable terminal string. A displayed unit is specified as a projection linked to the source agent, relevant component states, logical source, and active relations.

If the implementation cannot preserve that linkage, it MUST identify the result as a detached preview or conventional output, not as a live semantic-visual projection.

### 2.2 No ungrounded autonomy

Autonomy means that an agent can perform only the operations permitted by its contract, available state, source lineage, and governing rules. It does not mean permission to invent missing source data, mappings, terms, weights, or state transitions.

## 3. Upper neural triad — source and delegation layer

Every semantic agent MUST declare its relationship to the three upper entities:

### 3.1 Neural Wikipedia
The connected knowledge and associative source environment. It supplies source material and source-linked relations. An agent must retain references to the specific source nodes or records on which its accepted state depends.

### 3.2 Neural Index
The navigational and topological coordinate layer. It is intended to locate concepts, nodes, relations, and mappings within the project's defined spaces, including the 231-gate and 230-space-group design.

No gate-to-group correspondence may be assumed merely from the stated counts. Every correspondence requires an explicit source record and validation evidence.

### 3.3 Neural Orchestrator
The coordination layer responsible for delegation, attention selection, synchronization, routing, and coordination among agents and applications.

The term “attention” or “global weights” describes a specified architectural responsibility. Numeric weights, learned parameters, or operational energy values MUST NOT be invented. The project rule `WEIGHTS = NOT_CREATED` remains in force unless the architect supplies and authorizes a new specification.

### 3.4 Triad coupling requirement
An agent's interface contract MUST state:
- which of the three entities it depends on;
- which information or events it receives from each;
- which outputs or state changes it may return;
- how source lineage is preserved;
- how missing, stale, conflicting, or unavailable triad state is handled.

A conventional API, MCP message, database record, or JSON envelope MAY be used as a transport mechanism. It MUST NOT be mistaken for the complete architectural coupling or for semantic realization by itself.

## 4. Second-order logical organization

The upper triad organizes the authorized words of the Book of Logic in **second order**: a structural-hierarchical organization of logical relations, not merely a chronological or linear sequence of natural-language tokens.

Every agent consuming this organization MUST preserve:
- the identity of each authorized logical term;
- the relation in which the term participates;
- the source and position of the term in the authorized logical structure;
- the distinction between source statement, extracted structure, formalized relation, derived result, and verified mapping.

No agent may infer an unstated relation property (including identity, equivalence, symmetry, transitivity, causality, or containment) without an explicit rule.

## 5. Four-layer realization contract

The agent realization chain is specified in this order:

`Ta'amim → Nekudot → Tagin → Otiyot`

Each layer is itself specified as an active, stateful application/network, not as a static decorative label.

### APP-01 — Ta'amim (טעמים): relational context
**Responsibility:** represent higher-order intent, relational context, and attention relationships to the upper triad and relevant logical structure.

The contract for this application MUST define its owned state, permitted relation operations, inputs, outputs, provenance, and validation rules.

No numeric attention weight or global parameter may be supplied without an authorized source.

### APP-02 — Nekudot (נקודות): phonetic and vector identity
**Responsibility:** represent the agent's phonetic/vector identity through dynamic nodes, point clusters, and point-cloud state.

The contract MUST define how point identity is preserved, how updates are recorded, and how unsupported or conflicting point-cloud changes are rejected.

No coordinates, dimensions, point counts, or vector values may be invented.

### APP-03 — Tagin (תגין): logical category and interfaces
**Responsibility:** represent logical categories, hierarchical classification, triggers, and higher-level interfaces linking the agent to authorized second-order logical terms.

The contract MUST distinguish an authorized category from a proposed or unresolved category. Every classification must retain its source and rule.

### APP-04 — Otiyot (אותיות): geometric form and projection
**Responsibility:** represent the converged geometric/topological form of the agent and its projection into the semantic-visual interface.

The contract MUST specify how a projected form links back to the agent identity, the other three application states, and the logical source.

The specified X/Y/Z geometry and any named shape-space parameters remain design requirements until enumerated and tested.

### 5.1 Four-application independence
Each application MUST be independently identifiable and testable, with:
- its own responsibility boundary;
- owned state;
- declared inputs and outputs;
- permitted dependencies;
- validation and failure rules;
- tests and evidence.

Independence does not mean isolation. The four applications MUST coordinate through declared relations and shared agent identity. They MUST NOT silently overwrite one another's state.

## 6. Recursive coupling and state propagation

The architecture is recursive: an agent may contain or coordinate sub-agents, and its own state may be represented as a node in a parent network. Each such relation MUST be explicit.

Every state propagation path MUST declare:
1. source node and source version;
2. receiving node and receiving version;
3. event or transformation type;
4. governing rule;
5. validation result;
6. resulting state reference;
7. provenance back to the initiating source.

A recursive cycle MUST NOT be treated as valid merely because it exists in a graph. Its termination, consistency, and update rules must be specified and tested.

No agent may claim that a user interaction changes the topology of the entire system unless the actual event path, affected nodes, state changes, and evidence are recorded.

## 7. Semantic-visual interface contract

The interface is specified as the **Live Semantic-Visual Mesh**: a network projection whose displayed letters, words, and sentences remain traceably connected to their source and realization chain.

For each displayed unit, the interface contract MUST provide a way to resolve:
- stable display-unit identity;
- source agent and source node identity;
- logical source and provenance;
- relevant Ta'amim, Nekudot, Tagin, and Otiyot state references;
- active relation references;
- current LOCK / ABSTAIN / DRIFT / HALT status;
- version or snapshot reference.

A click, selection, annotation, correction, or other user action MUST be represented as an explicit event. The system must identify which nodes and relations the event is allowed to affect. A user action is not automatically authorized to mutate the whole network.

If the displayed text is only a conventional rendering without live traceability, the implementation MUST label it accordingly.

## 8. Agent event and state contract

Each implementation MUST define its event vocabulary before claiming runtime conformance. The following event categories are required to be considered; their concrete schemas remain to be specified by the relevant implementation contract:

- create / initialize;
- receive-source;
- extract-structure;
- relate / connect;
- transform;
- project;
- user-interaction;
- snapshot / readout;
- invert;
- lock;
- abstain;
- drift-detected;
- halt;
- recover / resume, where explicitly authorized.

Each event MUST have a traceable origin, target, rule, result, and evidence reference. Unknown event types MUST be rejected or quarantined, not silently interpreted.

## 9. Integrity protocol

### LOCK
Accept or commit a state only after the required source, identity, relation, schema, and validation conditions pass.

### ABSTAIN
Do not produce or commit a semantic claim when required source material, a rule, a mapping, or verification evidence is absent, contradictory, or out of scope.

### DRIFT
Record unsupported changes to logical identity, point/vector identity, source lineage, relation structure, or component state.

### HALT
Stop the affected operation when a mandatory invariant fails. Preserve the failure record and the last valid snapshot.

No agent may bypass these controls to produce a plausible-looking output.

## 10. Required agent contract profile

Every concrete agent MUST publish a component contract containing the following sections:

1. Agent name and stable identity rule.
2. Role and responsibility boundary.
3. Parent network and child/sub-agent relations.
4. Upper-triad dependencies.
5. Book of Logic source dependencies and authorized term scope.
6. Four-application participation and owned state.
7. Inputs and outputs.
8. Event types and state-transition rules.
9. Provenance and snapshot model.
10. Interface projection behavior.
11. LOCK / ABSTAIN / DRIFT / HALT rules.
12. Failure modes and recovery boundaries.
13. Unit, integration, and conformance tests.
14. Evidence artifacts and current status.
15. Unresolved questions and explicit non-claims.

A profile that omits a required section MUST be marked incomplete.

## 11. First reference agent — Aleph-Agent (א׳)

Aleph-Agent is the first reference agent for this architecture.

Its detailed contract MUST be written separately and MUST inherit this document and the semantic truth contract. It must not invent:
- the 150 geometric-topological forms;
- Kraken-36 internal structures;
- the 231 gate definitions;
- the 230 space-group correspondences;
- U_alpha_beta transition values;
- any missing logical terms, coordinates, weights, or state schemas.

Those items must be supplied by authoritative project sources or marked unresolved.

Aleph-Agent may be used as the reference implementation only after its interfaces, states, mappings, and acceptance tests are explicitly defined.

## 12. Conformance and acceptance levels

Use these statuses precisely:

- **SPECIFIED:** a requirement or design is documented.
- **IMPLEMENTED:** corresponding code or executable modules exist.
- **TESTED:** defined tests were run and their results are available.
- **VERIFIED:** acceptance criteria passed with inspectable evidence.
- **PARTIAL:** only a subset is implemented or validated.
- **NOT_YET_VERIFIED:** evidence is absent or insufficient.
- **BLOCKED:** a missing authority, contradiction, failed invariant, or unavailable dependency prevents progress.

A document, diagram, mockup, API endpoint, JSON message, or successful render does not alone establish a living semantic network.

Minimum acceptance evidence for an agent:
1. independently testable application modules for each claimed application;
2. stable node and relation identity;
3. traceable source lineage;
4. explicit state transitions and event history;
5. demonstrated propagation across declared relations;
6. bidirectional traceability between source and interface projection;
7. LOCK rejection of invalid state;
8. ABSTAIN behavior for missing or contradictory evidence;
9. reproducible tests and retained logs/snapshots.

Until evidence passes the relevant criteria, the agent remains SPECIFIED, IMPLEMENTED, TESTED, PARTIAL, or NOT_YET_VERIFIED as applicable — never prematurely VERIFIED.

## 13. Mandatory obligations for all downstream agents

Every downstream agent MUST:
- read the semantic truth contract and this contract before work;
- inherit these requirements in its own component contract;
- preserve the project-defined semantic axiom;
- treat the recursive neural architecture as the target design, not as an already-proven runtime;
- maintain source lineage and state traceability;
- never invent terms, weights, coordinates, mappings, schemas, or test results;
- distinguish architectural language from demonstrated implementation;
- stop and report BLOCKED when a governing source or required rule is missing;
- report only actions actually performed and evidence actually inspected.

Required acknowledgement:

`WANGA_RECURSIVE_NEURAL_AGENT_CONTRACT_v1.0 — READ; REQUIREMENTS ACCEPTED; IMPLEMENTATION STATUS REPORTED WITHOUT OVERCLAIM.`

If the agent cannot comply:

`BLOCKED — WANGA RECURSIVE NEURAL AGENT CONTRACT NOT ACCEPTED OR NOT UNDERSTOOD.`

---

## 14. Initial status

| Area | Status |
|---|---|
| Recursive neural hyper-architecture | SPECIFIED |
| Upper triad roles | SPECIFIED |
| Second-order logical organization | SPECIFIED |
| Four application responsibilities | SPECIFIED |
| Semantic-visual mesh requirement | SPECIFIED |
| Recursive state propagation requirements | SPECIFIED |
| Concrete runtime schemas | NOT_YET_VERIFIED |
| Runtime neural coupling | NOT_YET_VERIFIED |
| Aleph-Agent implementation | NOT_YET_VERIFIED |
| End-to-end live interface behavior | NOT_YET_VERIFIED |

**Change control:** changes to this contract require explicit authorization from the project architect and a recorded version change. Downstream agents may propose amendments but MUST NOT silently weaken or replace this contract.
