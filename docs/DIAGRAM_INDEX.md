# WANGA-LAB — Master Diagram Index

**Audit date:** 2026-11-25  
**Canonical repository:** [WANGA-LAB](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB)

This index is the navigation layer for repository diagrams. Mermaid files are source artifacts; GitHub renders them in the repository. The interactive GitDiagram view is a derived repository visualization, not proof that every displayed edge is a live runtime call.

## Master navigation

- [Master Diagram Map — Mermaid](../diagrams/MASTER_DIAGRAM_MAP_V1.mmd)
- [Interactive repository architecture — GitDiagram](https://gitdiagram.com/quadruple-multilevel-projection-project/wanga-lab)
- [WANGA Daily Processor Operating Map](./architecture/WANGA_DAILY_PROCESSOR_OPERATING_MAP.md)

## Diagram catalogue

| ID | Diagram | Scope | Source |
|---|---|---|---|
| D01 | AI Logic Factory Product Delivery Map | Product layers, Thinking Language, visual transformation, KRAKEN admission and compute planes, evidence/release | [Mermaid](../diagrams/AI_LOGIC_FACTORY_PRODUCT_DELIVERY_MAP_V1.mmd) |
| D02 | System-wide Integration — Thinking Language + KRAKEN | WANGA/AI231 system integration, thought maps, logic, KRAKEN and evidence | [Mermaid](../diagrams/system-wide-integration-thinking-language-kraken.mmd) |
| D03 | System-wide Integration — excluding KRAKEN | Logic, agent, evidence and governance target architecture without the KRAKEN track | [Mermaid](../diagrams/system-wide-integration-excluding-kraken.mmd) |
| D04 | Cabinet Unified Semantic Architecture | Model/plugin cabinet, runtime, logic and evidence architecture | [Mermaid](../diagrams/cabinet-unified-semantic-architecture.mmd) |
| D05 | Plugin Cabinet Coordination | Cabinet coordination and bounded handoffs | [Mermaid](../diagrams/plugin-cabinet-coordination.mmd) |
| D06 | Constitutional Fractal Governance | Governance invariants, provenance and bounded composition | [Mermaid](../diagrams/constitutional-fractal-governance.mmd) |
| D07 | Kraken Atomic Fractal Engine | KRAKEN/fractal research architecture | [Mermaid](../diagrams/kraken-atomic-fractal-engine.mmd) |
| D08 | KRAKEN Cognitive Logic + Heterogeneous Compute v0.2 | Cognitive Logic Plane, visual transformation, workload admission, heterogeneous compute and evidence gates | [Mermaid](../ai-drift-forensics/david-jones-kraken/KRAKEN_COGNITIVE_LOGIC_FABRIC_V0_2.mmd) |\n| D09 | Master Diagram Map | Clickable navigation graph linking the repository's diagram families | [Mermaid](../diagrams/MASTER_DIAGRAM_MAP_V1.mmd) |

## Related specifications and operating documents\n\n- [WANGA Daily Processor Operating Map — system flow and daily execution sequence (two embedded Mermaid diagrams)](./architecture/WANGA_DAILY_PROCESSOR_OPERATING_MAP.md)

- [KRAKEN configuration v0.1 — hardware requirements, NOT_YET_VERIFIED](../ai-drift-forensics/david-jones-kraken/KRAKEN_CONFIGURATION_V0_1.md)
- [KRAKEN configuration v0.2 — expanded two-plane architecture, SPECIFIED / NOT_YET_VERIFIED](../ai-drift-forensics/david-jones-kraken/KRAKEN_CONFIGURATION_V0_2.md)
- [KRAKEN evidence gate](../ai-drift-forensics/david-jones-kraken/EVIDENCE_GATE.md)
- [AI Logic Factory product architecture](./AI_LOGIC_FACTORY_PRODUCT_ARCHITECTURE_V1.md)
- [Master Map Integration Contract](./LOGIC_FACTORY/MASTER_MAP_INTEGRATION_CONTRACT.md)
- [Map registry](./LOGIC_FACTORY/map_registry.v1.json)
- [Reconstruction ledger and artifact-family boundaries](./LOGIC_FACTORY/RECONSTRUCTION_LEDGER_2026-11-18.md)

## Reading rules

1. A diagram is a navigation/projection artifact; repository code, schemas, tests and source records remain authoritative.
2. A drawn edge does not prove a live API call, deployed integration or runtime execution.
3. Statuses must remain distinct: SPECIFIED, BUILT, SIMULATED, TESTED, VERIFIED, HYPOTHESIS and NOT_YET_VERIFIED.
4. KRAKEN v0.1's 36 dual configurations / 72 QPU positions remain an unverified internal requirement, not an existing hardware fact.
5. KRAKEN v0.2's Cognitive Logic Plane and Heterogeneous Compute Plane are coordinated but separable.
6. The 13 legacy diagrams, 14 chapter maps, four meta-maps, 175 term maps and master network map are distinct inventory families. The planned total of 207 is not a claim that all 207 have been generated.
7. The chapter map sequence must not be equated to the 14 logic gates without source-backed evidence.

## Update protocol

When a source, contract, processor, app or relation changes:
- update the source artifact first;
- record the source commit/version and change event;
- identify affected diagrams through dependencies;
- update the relevant Mermaid source and this index;
- run link, node/edge, and semantic validation;
- mark affected views CURRENT, STALE or BLOCKED;
- do not promote an edge to VERIFIED from visual similarity alone.
