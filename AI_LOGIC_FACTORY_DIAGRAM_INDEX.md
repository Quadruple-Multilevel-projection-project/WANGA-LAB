# AI Logic Factory — Diagram & Model Reading Index

**Product:** AI Logic Factory — Unified Semantic & Analytical Processor  
**Repository:** WANGA-LAB  
**Index status:** Navigation / documentation entry point  
**Architecture status:** Mixed: existing repository components + specified product design + proposed interfaces. See status labels below.

> Start here before reading or changing any architecture diagram. This index is the canonical navigation page for humans and AI models. It does not replace the source contracts.

## 1. Master navigation

- [Master link map — four layers and cross-layer interfaces](diagrams/AI_LOGIC_FACTORY_MASTER_LINK_MAP_V1.mmd)
- [Diagram catalog and AI-model reading guide](docs/DIAGRAM_CATALOG_AND_MODEL_READING_GUIDE_V1.md)
- [AI-model handoff protocol](docs/AI_MODEL_HANDOFF_PROTOCOL_V1.md)
- [Machine-readable diagram registry](diagrams/diagram-registry.v1.json)
- [Interactive GitDiagram for WANGA-LAB](https://gitdiagram.com/quadruple-multilevel-projection-project/wanga-lab)

## 2. Four architecture layers — keep boundaries explicit

1. **Language & Contract** — terms, typed relations, distinctions, Place, semantic constraints, evidence requirements and truth-validation status.
2. **Analytics & Visualization** — glyph/image intake, visual transformations, pattern analysis, candidate generation and insight hypotheses.
3. **KRAKEN** — bounded fractal composition, state transitions, workload admission and capability-aware compute orchestration.
4. **Orchestration & Product** — workbench/apps, agents, knowledge stores, APIs, audit trail, review workflow and performance measurement.

The layers communicate through versioned contracts. A diagram arrow is not proof that an implementation or integration already exists.

## 3. Canonical diagrams and specifications

| Artifact | Purpose | Status |
|---|---|---|
| [KRAKEN Configuration v0.2](ai-drift-forensics/david-jones-kraken/KRAKEN_CONFIGURATION_V0_2.md) | KRAKEN scope, planes, admission and compute boundaries | SPECIFIED / NOT_YET_VERIFIED |
| [KRAKEN Cognitive Logic Fabric v0.2](ai-drift-forensics/david-jones-kraken/KRAKEN_COGNITIVE_LOGIC_FABRIC_V0_2.mmd) | KRAKEN cognitive/compute architecture | Diagram; inspect linked configuration |
| [AI Logic Factory Product Architecture v1](docs/AI_LOGIC_FACTORY_PRODUCT_ARCHITECTURE_V1.md) | Product components, interfaces, evidence and measurement | Product specification / NOT_YET_VERIFIED |
| [AI Logic Factory Product Delivery Map v1](diagrams/AI_LOGIC_FACTORY_PRODUCT_DELIVERY_MAP_V1.mmd) | Product delivery flow and workbench | Roadmap / NOT_YET_VERIFIED |
| [Naming–Place Numeric Derivation Contract v1](WANGA_NAMING_PLACE_NUMERIC_DERIVATION_CONTRACT_V1.md) | Conditions for grounded numeric derivation | Source contract; read before changing Place/numeric logic |
| [Semantic Truth Contract v1](WANGA_SEMANTIC_TRUTH_CONTRACT_V1.md) | Semantic truth and evidence constraints | Source contract; read before changing truth validation |
| [Recursive Neural Agent Contract v1](WANGA_RECURSIVE_NEURAL_AGENT_CONTRACT_V1.md) | Agent recursion and boundaries | Source contract; read before changing agent orchestration |
| [Architecture Registry](ARCHITECTURE_REGISTRY.json) | Existing architecture inventory | Repository registry |

## 4. How to read the status labels

- **EXISTING** — source file or implementation is present in the repository. Presence alone does not prove runtime behavior.
- **SPECIFIED** — documented design or contract; implementation may still be absent.
- **PROPOSED** — suggested interface, component or workflow awaiting approval/implementation.
- **NOT_YET_VERIFIED** — no sufficient independent test evidence has been recorded.
- **VERIFIED** — only use when a reproducible test, evidence artifact, version and acceptance result are linked.
- **SIMULATED** — produced by simulation/emulation, not a physical device.
- **ABSTAIN / HALT** — required information or safety condition is missing; do not infer or continue.

## 5. Non-mixing invariants

- Keep the 14 logic gates / 175 logic terms separate from the 231 letter-pair gates.
- Do not silently map letter gates to logic gates. A versioned, explicit interface is required.
- Keep visual resemblance, generated candidates and human interpretation separate from verified semantic identity.
- Keep naming/distinction and Place/context ahead of numeric measurement when applying the Naming–Place contract.
- Preserve qualitative causal roles when numbers are later introduced.
- Do not describe optical, photonic, quantum or other physical hardware as implemented unless hardware evidence exists.
- Do not turn a proposed diagram arrow into a claim of a live API, deployed integration or tested runtime path.

## 6. Change procedure

1. Read this index and the model handoff protocol.
2. Read the relevant source contracts before editing diagrams.
3. Identify whether the change is EXISTING, SPECIFIED, PROPOSED or NOT_YET_VERIFIED.
4. Update the source document first, then the affected Mermaid diagram and registry.
5. Check links, Mermaid syntax, layer ownership and cross-layer interface names.
6. Record what changed, what did not change, evidence used, unresolved gaps and next owner.
7. Never overwrite an unresolved contradiction. Record it and ABSTAIN pending review.

## 7. Diagram Intelligence Hub — multi-model diagram audit

- [Diagram Intelligence Hub README](diagram-intelligence-hub/README_V1.md)
- [Grok collaboration handoff protocol](diagram-intelligence-hub/GROK_COLLABORATION_HANDOFF_V1.md)
- [Diagram ingest contract](diagram-intelligence-hub/DIAGRAM_INGEST_CONTRACT_V1.json)
- [Daily reconciliation protocol](diagram-intelligence-hub/DAILY_RECONCILIATION_PROTOCOL_V1.md)
- [30-role proposed agent roster](diagram-intelligence-hub/DIAGRAM_AGENT_ROSTER_V1.json)
- [Diagram Intelligence Hub master architecture map](diagram-intelligence-hub/DIAGRAM_INTELLIGENCE_HUB_MASTER_V1.mmd)

The 30 entries are proposed audit roles, not deployed agents. Grok submissions are untrusted candidates until source-grounded review. Wix automation and Grok API connectivity remain NOT_YET_VERIFIED; see the handoff and daily reconciliation documents.

**Canonical rule:** diagrams explain and link to source artifacts; contracts govern.