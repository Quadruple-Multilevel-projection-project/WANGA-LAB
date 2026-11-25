# Diagram Catalog & AI Model Reading Guide v1

**For:** ChatGPT, Claude, Gemini, Grok, local models, agents and human contributors  
**Project:** AI Logic Factory — Unified Semantic & Analytical Processor  
**Authority:** Source contracts outrank explanatory diagrams and summaries.

## A. Read order for every model

1. `AI_LOGIC_FACTORY_DIAGRAM_INDEX.md` — canonical entry point and status vocabulary.
2. `docs/AI_MODEL_HANDOFF_PROTOCOL_V1.md` — contribution rules and handoff format.
3. `docs/AI_LOGIC_FACTORY_PRODUCT_ARCHITECTURE_V1.md` — product-level structure.
4. `ai-drift-forensics/david-jones-kraken/KRAKEN_CONFIGURATION_V0_2.md` — KRAKEN boundaries and compute tracks.
5. The specific source contract for the requested task.
6. The corresponding Mermaid diagram.
7. Relevant implementation files, only if implementation behavior is being assessed.

Do not infer source content from a filename, diagram label, previous model's summary or GitDiagram-generated description. Open the source file.

## B. Four-layer responsibility map

### L1 — Language & Contract
Owns:
- term identity, definitions, typed relations and semantic boundaries;
- distinction and Place/context;
- evidence and provenance requirements;
- rules for numeric derivation and semantic truth status.

Primary sources:
- `WANGA_NAMING_PLACE_NUMERIC_DERIVATION_CONTRACT_V1.md`
- `WANGA_SEMANTIC_TRUTH_CONTRACT_V1.md`

Does not own:
- image enhancement algorithms;
- hardware scheduling;
- app deployment.

### L2 — Analytics & Visualization
Owns:
- image/glyph intake and immutable source capture;
- visual feature extraction and candidate transformations;
- spatial/frequency-domain operations where technically specified;
- pattern comparison, uncertainty and candidate ranking;
- analyst review and experiment records.

Must distinguish:
- source image from transformed image;
- computational transformation from physical light propagation;
- candidate similarity from semantic identity;
- generated hypothesis from verified insight.

A photonic/optical physical implementation is not implied by a software visualization pipeline.

### L3 — KRAKEN
Owns:
- bounded fractal composition and package versioning;
- state-transition orchestration;
- workload admission and capability matching;
- routing to conventional compute, simulation/emulation or a physical QPU adapter when available;
- execution receipts and resource telemetry.

Primary source:
- `ai-drift-forensics/david-jones-kraken/KRAKEN_CONFIGURATION_V0_2.md`

KRAKEN coordinates layers; it must not redefine their terms or bypass their contracts.

### L4 — Orchestration & Product
Owns:
- workbench and user workflows;
- model/agent task assignment and handoffs;
- knowledge and artifact registries;
- API boundaries, permissions and audit records;
- human review, release and KPI dashboards.

Primary source:
- `docs/AI_LOGIC_FACTORY_PRODUCT_ARCHITECTURE_V1.md`
- `diagrams/AI_LOGIC_FACTORY_PRODUCT_DELIVERY_MAP_V1.mmd`

A connector name or external URL does not prove that the integration is connected or operational.

## C. Diagram catalog

| ID | Artifact | Read when |
|---|---|---|
| D-00 | `AI_LOGIC_FACTORY_DIAGRAM_INDEX.md` | Starting any task |
| D-01 | `diagrams/AI_LOGIC_FACTORY_MASTER_LINK_MAP_V1.mmd` | Understanding all layers and interfaces |
| D-02 | `ai-drift-forensics/david-jones-kraken/KRAKEN_COGNITIVE_LOGIC_FABRIC_V0_2.mmd` | Studying KRAKEN's cognitive/compute fabric |
| D-03 | `diagrams/AI_LOGIC_FACTORY_PRODUCT_DELIVERY_MAP_V1.mmd` | Studying product workflow and delivery |
| D-04 | `diagrams/diagram-registry.v1.json` | Programmatic discovery of diagrams and source links |

## D. Model-specific reading profiles

These are task profiles, not claims about any model's intelligence or capabilities.

- **High-capability research/reasoning model:** read the entire product architecture, KRAKEN configuration and relevant contracts; inspect implementation evidence; identify interface mismatches, missing tests, security implications and unproven claims. Do not rewrite source contracts without explicit authorization.
- **General-purpose model:** read the index, handoff protocol, product architecture summary and the one relevant contract; produce a bounded analysis with file paths and evidence.
- **Small/fast model:** receive one assigned file or one diagram node at a time. Extract only direct statements, paths, status labels and explicit gaps. Do not extrapolate across layers.
- **Code-oriented agent:** inspect actual code and tests for one assigned interface. Report file paths, symbols, test commands and observed results. Do not treat documentation as runtime proof.
- **Diagram-oriented agent:** edit Mermaid only after confirming source ownership and link targets. Preserve status styling and label proposed connections as proposed.
- **Independent verifier:** do not rely on the author model's conclusion. Reopen the source, reproduce the test and report PASS / FAIL / INCONCLUSIVE with evidence.

## E. Required output for every model

1. Assigned task and scope.
2. Files actually opened.
3. Findings, each tagged EXPLICIT / INFERRED / PROPOSED.
4. Status: EXISTING / SPECIFIED / PROPOSED / NOT_YET_VERIFIED / VERIFIED / SIMULATED.
5. Exact source paths and line/section references where available.
6. Contradictions or missing interfaces — do not resolve by invention.
7. Tests run and results, or state NOT RUN.
8. Suggested change as a separate proposal.
9. Handoff: next owner, exact file(s), acceptance condition.

## F. Diagram conventions

- Solid edge: documented/implemented connection only when supported by source evidence.
- Dashed edge: proposed, conceptual or not yet verified connection.
- Amber/status tag: specified but not verified.
- Red/status tag: blocked, abstain or halt.
- Every node should link to a source file, contract, API specification or explicitly say `NO SOURCE YET`.
- Mermaid diagrams are navigation and explanation artifacts, not proof of system behavior.

## G. Conflict handling

When two files disagree:
1. quote the exact conflicting statements and paths;
2. identify each source's status and date/version;
3. do not select a winner based on model preference;
4. mark the interface `CONFLICT / ABSTAIN`;
5. request owner review and preserve both records until a decision is logged.