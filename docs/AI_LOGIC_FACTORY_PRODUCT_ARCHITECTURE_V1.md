# AI Logic Factory — Product Architecture & Delivery Plan v1.0

**Date:** 2026-11-25  
**Status:** PRODUCT CONCEPT / SPECIFIED ROADMAP / NOT_YET_VERIFIED  
**Canonical repository:** WANGA-LAB

## 1. Product definition

AI Logic Factory is a language-centered analytical workbench and runtime for mapping thought, expressing typed semantic/logical contracts, validating claims and transformations, coordinating models, and routing eligible workloads to compute resources.

The product's differentiator is not a claim that software is conscious. "Thinking language" means a structured representation that can retain a thought state, transform it under declared operators, test the result, and carry forward only accepted state.

## 2. Product users and initial use cases

Initial target users:
- AI engineering and evaluation teams that need traceable model outputs and controlled handoffs;
- research groups formalizing terminology, relations, visual patterns and hypotheses;
- organizations that need auditable semantic consistency and evidence-linked decisions.

Initial use cases:
1. Source-grounded logic / semantic audit.
2. Cross-model task handoff with contradiction preservation.
3. Thought-map and Place-contract authoring.
4. Visual/glyph transformation exploration with replay and human review.
5. Evidence-backed compute routing and benchmark reporting.

Market demand and willingness to pay remain unvalidated until customer interviews and paid pilots.

## 3. Product modules

| Module | User outcome | Inputs | Outputs | Delivery state |
|---|---|---|---|---|
| Logic Registry | Stable terms, sources and typed relations | Source text, locator, term record | Versioned term and relation records | Existing structured registries; coverage varies |
| Thinking Language Runtime | Represent and transform structured thought | Typed graph / LNL | AST, derivations, gate results | Bounded prototype exists; arbitrary-language semantics not verified |
| Place & Semantic Contract | Prevent ungrounded comparison and semantic scope drift | Identity, domain, observer/base, substrate, Π, κ, ρ | Place record, pass/review/abstain | Specified; runtime enforcement not verified |
| Thought Mapping | Show logical, semantic, word and letter/agent structures | Snapshots, terms, relations | Four linked maps | First two maps documented; semantic and letter/agent maps incomplete |
| Visual Transformation Studio | Explore image/glyph transformations reproducibly | Image, region, transform specification | Candidate transformations + replay receipt | New specified research module; not implemented |
| Fractal Composer | Reuse bounded source-linked structures | Catalog, composition contracts | Candidate packages | Deterministic candidate composer exists; candidates not semantic truth |
| Model Cabinet | Allocate bounded tasks across models/tools | Capability declarations, task contract | Reports, conflicts, handoff state | Architecture specified; external model mesh not proven deployed |
| KRAKEN Scheduler | Route work to appropriate compute | Validated workload + capability profile | Resource selection + telemetry | Expanded architecture specified; physical hardware unverified |
| Evidence & Governance | Preserve provenance and independent checks | Source, action, result, hashes | Audit receipts, review/lock state | Several repository components exist; end-to-end status varies |

## 4. End-to-end user journey

1. Create or import a source-backed thought snapshot.
2. Identify entities, names, types and qualitative relations.
3. Define Place: domain, context, observer/base, substrate, protocol Π, boundary κ, persistence ρ, time window and source references.
4. Add upper/lower boundary predicates and fifth-sphere containment only where the axis/domain and formal rules are explicit.
5. Express the structure in the typed Thinking Language.
6. Run logic, semantic, counterexample and provenance checks.
7. If images are involved, run a versioned visual transformation; retain source image, parameters, output and reviewer decision.
8. Compose a bounded fractal package.
9. Route to a model, conventional compute, simulation or a physical accelerator only if eligible and evidenced.
10. Independently verify output; LOCK only with complete acceptance evidence, otherwise REVIEW / ABSTAIN / HALT.
11. Save the accepted result as the next thought snapshot.

## 5. Product architecture

- **Experience layer:** Logic Factory workbench, source explorer, thought-map canvas, visual transformation panel, review queue and KPI dashboard.
- **API layer:** snapshot, term, Place, transform, workload, task, verification and telemetry APIs.
- **Logic layer:** LNL, symbolic kernel, typed formal checks, semantic contract and fractal composition.
- **Coordination layer:** model registry, capability profiles, task router, append-only reports and conflict ledger.
- **Execution layer:** conventional CPU/GPU first; simulation/emulation next; QPU only after hardware identity and evidence gates.
- **Evidence layer:** provenance, content hashes, replay, independent verification, audit receipts.
- **Data layer:** GitHub is canonical for code/contracts/diagrams; Notion for narrative and decisions; Airtable for structured registries and test rows. Cross-links must prevent competing sources of truth.

## 6. Product stages and release gates

### Stage 0 — Research package
- Freeze vocabulary and schema versions.
- Publish the product architecture, system map and evidence boundaries.
- Keep the 14 logic gates / 175 terms separate from the 231 letter-pair gates.

### Stage 1 — MVP: source-grounded logic workbench
- Import source text and record exact locators.
- Create thought snapshots, typed relations and Place records.
- Run existing symbolic/typed checks.
- Display contradictions and ABSTAIN reasons.
- Export evidence-linked report.
- Acceptance: reproducible test suite; source coverage; no silent contradiction deletion.

### Stage 2 — Visual Transformation Studio
- Upload a glyph/image sequence.
- Define transform operators and preserve the original.
- Compare output against declared shape constraints and source examples.
- Support human acceptance/rejection and deterministic replay.
- Acceptance: repeated runs under the same declared conditions; false-match and boundary-case tests; no automatic promotion to canonical glyph.

### Stage 3 — Cabinet and Fractal Reuse
- Capability-aware task routing.
- Append-only model reports and shared-state handoff.
- Candidate composition with source lineage.
- Acceptance: no cross-model semantic tail without versioned change; conflicts remain visible.

### Stage 4 — KRAKEN Compute Orchestration
- Benchmark conventional CPU/GPU scheduling first.
- Add simulation/emulation backends with explicit labels.
- Integrate hardware adapters only after interface and safety review.
- Acceptance: measured scheduling, latency, utilization, recovery and reproducibility.

### Stage 5 — Institutional pilots
- Select a narrow enterprise use case.
- Run matched baseline/treatment evaluations.
- Validate security, privacy, legal and procurement requirements.
- Convert to paid pilot only after customer value and delivery economics are evidenced.

## 7. Improvement metrics

Primary metric: **Quality-Adjusted Throughput (QAT)** = independently accepted tasks per hour and per unit cost, at a fixed quality threshold.

Track separately:
- source retrieval and reconstruction time;
- semantic rework / correction time;
- handoff and coordination time;
- independent acceptance rate;
- contradiction escape rate;
- invalid numeric-comparison rate;
- Place-field completeness;
- source-lineage coverage;
- visual transform reproducibility and false-match rate;
- model tokens and tool calls per accepted task;
- scheduler latency, utilization, error rate, energy/power where measurable;
- human review time and rollback/recovery rate.

### Planning forecast (not measured)

| Horizon | Conservative | Central | Optimistic |
|---|---:|---:|---:|
| Month 1 | 0–5% | 5–10% | 10–15% |
| Month 3 | 3–10% | 10–20% | 20–30% |

These ranges are planning hypotheses inherited from the current Kraken/Thinking Language integration record. They are not achieved results. Month 6 and Month 12 estimates are intentionally withheld until a frozen baseline, pilot results, task mix and integration overhead establish a defensible growth curve.

### Benchmark method

Use the same frozen tasks, source set, model budget and acceptance rubric for baseline and treatment. Calculate:

`QAT = independently\_accepted\_tasks / (elapsed\_hours × normalized\_cost)`

`Improvement\% = 100 × (QAT_treatment / QAT_baseline - 1)`

Also report quality and safety guardrails; a throughput gain does not count if acceptance quality falls or contradiction escape increases.

## 8. Non-negotiable invariants

- Distinguish → Name/Type → Define Place → Define unit/comparison → Measure/Number.
- Qualitative relations and causal roles survive numeric scoring.
- 14 logic gates / 175 terms are not merged with 231 letter-pair gates.
- Five-sphere model remains OPEN until formal topology, axis, boundaries and counterexamples are recorded.
- Visual similarity is not semantic identity.
- No model consensus substitutes for evidence.
- Contradictions are preserved, not silently reconciled.
- No unverified QPU capability or quantum advantage claim.
- Missing evidence yields REVIEW / ABSTAIN / HALT.
- No credentials or secrets in GitHub, Notion or Airtable.

## 9. Current integration observations

- WANGA-LAB README identifies existing bounded components: LNL, symbolic logic kernel, fractal composer, formal reasoning, ARK-Swarm, evidence and governance.
- The repository's KRAKEN v0.2 spec already defines cognitive logic + heterogeneous compute planes and the naming/place numeric gate.
- The Notion integration page records the four cognitive maps, the five-sphere model as open, and the forecast above.
- Airtable contains structured source, logic-unit, relation, formal-rule, map, review/test, processor and processor-function registries.
- Vercel connector returned zero projects for the connected account at this check. This does not prove that previously supplied AppDeploy URLs are offline; it means no Vercel projects were visible through this connection.
- External model provider connectivity and the physical Kraken hardware are not established by this product document.

## 10. Next execution sequence

1. Review and approve schemas for visual transformation and thought snapshots.
2. Build a single text-only MVP vertical slice using existing LNL/kernel/evidence paths.
3. Add a separate image/glyph replay prototype.
4. Register maps, processor roles and test cases in Airtable.
5. Connect the workbench UI only after a visual design direction is selected in Product Design Work mode.
6. Run baseline/treatment tests before publishing measured improvement claims.
