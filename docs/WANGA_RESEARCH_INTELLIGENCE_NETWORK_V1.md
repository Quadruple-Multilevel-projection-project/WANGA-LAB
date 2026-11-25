# WANGA Research Intelligence Network v1.0
## Daily Fractal Knowledge Evolution

Status: ARCHITECTURE_PROPOSAL
Date: 2026-11-26
Canonical owner: WANGA-LAB
Related architecture: AI231/WANGA Thinking Language + Kraken Integration; WANGA Neural Second Brain.

## 1. Mission

Build a cross-platform research collection and knowledge-evolution network. It continuously collects new scientific and technical evidence, extracts candidate concepts and relations, compares them with the current WANGA contracts and knowledge graph, generates versioned fractal diagrams, and distributes approved updates to downstream agents through stable schemas and MCP/HTTP interfaces.

The network is a research intelligence and evidence-management system. It does not autonomously declare scientific truth, rewrite canonical contracts, or infer that every new paper changes the language.

## 2. Governing principles

1. Evidence before language change: a publication is a source, not an automatic truth or contract update.
2. Candidate before canonical: machine-extracted claims, relations, metrics and diagram edges remain CANDIDATE until audited.
3. Preserve source: never overwrite raw source records; retain DOI/URL, retrieval time, source hash, licence/access status and exact supporting passages or locations.
4. Naming–Place before measurement: DISTINGUISH -> NAME/TYPE -> DEFINE PLACE -> DEFINE COMPARISON + UNIT -> MEASURE/NUMBER. Missing context produces ABSTAIN.
5. Separate layers: (A) research evidence, (B) semantic/logical contract, (C) diagram projection, (D) runtime/tool execution. A diagram edge does not prove runtime integration.
6. Version, don't mutate: every accepted graph/contract change has a version, diff, rationale, provenance and rollback path.
7. Conflict preservation: contradictory sources remain linked as competing claims; no majority vote silently converts them into facts.
8. Cost-aware collection: use metadata and abstracts first; fetch full text only when open access, permitted and materially necessary.
9. Platform-neutral interchange: JSON Schema + stable IDs + HTTPS APIs; MCP adapters expose the same canonical operations to compatible agents.
10. Human gate for high-impact changes: novel definitions, altered invariants, safety/security issues and high-impact scientific claims require explicit review.

## 3. System architecture

### A. Collection plane
- Source adapters: OpenAlex, Crossref, arXiv, PubMed/Europe PMC, standards/patent feeds and explicitly approved project sources.
- Inputs: metadata, abstracts, identifiers, dates, author/institution, topic, source URL and access/licence metadata.
- Collector deduplication: DOI first; then normalized title + author + year; preserve duplicate source records where they represent different versions.
- Store immutable source envelopes before extraction.

### B. Research intelligence plane
Specialized logical roles (roles may be implemented by scripts, models or human review; they are not 30 deployed agents):
1. Scheduler/Collector — discovers new records and retries failed sources.
2. Normalizer — resolves identifiers, dates, versions and duplicate records.
3. Evidence Extractor — extracts claims, definitions, methods, findings and limitations with exact source anchors.
4. Relation Mapper — proposes typed links between claims, concepts, methods, entities and existing WANGA terms.
5. Novelty & Contradiction Auditor — checks novelty against the graph, finds conflicting/replicating evidence and detects unsupported leaps.
6. Contract Auditor — checks Naming–Place, logic gates, units, scope, invariants and layer boundaries.
7. Diagram Composer — generates diagram candidates from the graph diff, not freehand unsupported claims.
8. Release Curator — packages approved changes, changelog and downstream notifications.

A single orchestration workflow can invoke these roles sequentially. Do not provision 30 always-running agents for the MVP.

### C. Fractal diagram plane
One canonical graph, multiple deterministic projections:
- L0 Evidence atom: source, passage, claim, measurement or observation.
- L1 Concept/relation: typed concept and relation with evidence.
- L2 Local structure: method, mechanism, causal proposal or logical pattern.
- L3 Domain map: connected concepts and competing models within a research domain.
- L4 Cross-domain map: validated links between domains and WANGA contracts.
- L5 System map: approved effects on Thinking Language, Logic Registry, visual/glyph maps or Kraken workload contracts.

Each node/edge carries a stable ID, type, status, provenance, version and confidence/uncertainty description. Numeric confidence is not invented: if a score is used, its formula, calibration set and interpretation must be documented. Otherwise use categorical statuses.

Diagrams are generated from graph records using Mermaid (and optionally Graphviz/PlantUML). The structured graph is canonical; rendered diagrams are views. This prevents the diagram and database from drifting independently.

### D. Contract evolution plane
For each daily batch:
1. Compare candidate graph with current canonical version.
2. Classify each proposed change: ADD, REFINE, SPLIT, MERGE, DEPRECATE, CONTRADICT, NO_CHANGE.
3. Check source sufficiency, exact evidence anchors, reproducibility, Place/context, unit compatibility, logical consistency and impact.
4. Produce a machine-readable diff and human-readable explanation.
5. Auto-accept only low-risk metadata/duplicate corrections under deterministic rules.
6. Send new scientific claims, new terms, altered definitions, altered invariants or high-impact relations to HUMAN_REVIEW.
7. If evidence is insufficient or incompatible, ABSTAIN and preserve the candidate in the sandbox.
8. Publish only approved changes as a new immutable version.

The daily output is allowed to be NO_CHANGE. The goal is correct evolution, not forced novelty.

### E. Knowledge graph / Neural Wikipedia
The “Neural Wikipedia” is a curated, source-linked knowledge graph plus readable pages generated from it:
- Every statement links to one or more source records and evidence anchors.
- Pages show accepted definitions, open hypotheses, competing claims, methods, counterexamples, change history and related diagrams.
- A model may retrieve and explain the graph but may not silently promote its own output into canonical knowledge.
- The first implementation is a conventional database/search + graph-shaped relations + model-assisted retrieval. It is not a newly trained neural network and does not require training a neural model.

### F. Distribution and MCP plane
Expose stable operations through HTTPS and MCP adapters:
- search_sources(query, filters)
- get_source(source_id)
- get_claim(claim_id)
- get_concept(concept_id)
- get_subgraph(root_id, depth, status)
- get_diagram(diagram_id, version)
- propose_change(change_set)
- get_contract(contract_id, version)
- subscribe_updates(topic)
- submit_audit(audit_result)

MCP is the tool interface, not the database, event bus or source of truth. Platforms that do not support MCP consume the same JSON/HTTPS API or exported Markdown/Mermaid/JSON artifacts. Use signed webhook notifications or scheduled polling for updates.

## 4. Daily cycle

1. UTC scheduled run opens a batch ID.
2. Collect incremental records since the last successful cursor.
3. Normalize and deduplicate; preserve source envelopes.
4. Extract claims and evidence anchors.
5. Map claims to existing concepts and contracts.
6. Run novelty, contradiction, safety, source and Place audits.
7. Create candidate graph delta and diagram projections.
8. Apply risk-based decision gate: AUTO_ACCEPT / HUMAN_REVIEW / ABSTAIN / REJECT.
9. Human-approved changes are committed as a versioned Git release.
10. Publish knowledge pages, diagrams, API/MCP notifications and a daily digest.
11. Record metrics, failures, costs, review backlog and rollback pointer.

Idempotency: rerunning the same source batch must not create duplicate canonical nodes. Every run stores batch_id, source cursor, schema version, model/prompt version, tool versions and result hashes.

## 5. Status model

- RAW: source captured, not interpreted.
- CANDIDATE: machine-extracted, not accepted.
- UNDER_REVIEW: awaiting human or independent audit.
- ACCEPTED: approved and source-grounded.
- HYPOTHESIS: explicit proposed interpretation, not established.
- CONFLICTED: credible evidence disagrees.
- REJECTED: failed a documented gate.
- DEPRECATED: no longer current, but retained historically.
- NOT_YET_VERIFIED: specification exists without runtime or empirical proof.

LOCK is reserved for an accepted, versioned artifact that passed the defined gates. A paper's publication status alone never implies LOCK.

## 6. Free-first cross-platform deployment options

### Option A — GitHub-first (recommended MVP)
- Public WANGA-LAB repository: canonical JSON schemas, source manifests, Mermaid diagrams, change sets, tests, daily digests and release history.
- GitHub Actions scheduled workflow: collector and deterministic validation for public-repository workloads. GitHub documents standard runner usage as free for public repositories.
- GitHub Issues/Pull Requests: review queue and approval record.
- GitHub Pages: optional read-only diagram/wiki portal.
- Model calls: optional external API, invoked only for bounded extraction/audit tasks. GitHub hosting being free does not make model inference free.

Advantages: lowest integration friction with the existing canonical repository, full diffs, provenance, rollback and cross-platform readability. Limitation: not a high-throughput database or long-running agent host; public repo content is public.

### Option B — Cloudflare-first
- Workers + Cron Triggers for scheduled collection and API endpoints.
- D1 for structured metadata/relations; R2 for permitted source artifacts; Queues/Workflows only if current free quotas fit.
- Current Workers Free documentation lists 100,000 requests/day, 10 ms CPU per invocation and 5 Cron Triggers/account. Check all product-specific quotas before relying on them.
Advantages: API and scheduler in one edge platform; suitable for lightweight always-on ingestion.
Limitations: CPU ceiling, product-specific quotas, additional engineering and vendor coupling.

### Option C — Supabase-first
- Postgres for normalized records and graph relations; Storage for permitted files; Edge Functions for APIs.
- Current Free pricing lists 500 MB database per project, 1 GB file storage, 5 GB egress and project pausing after one week of inactivity; free plan has up to two active projects.
Advantages: relational queries, SQL, auth and structured dashboard backend.
Limitations: free-tier pausing and storage/egress limits; scheduled collection and durable operations need careful configuration.

### Option D — n8n self-hosted
- Community Edition can be free when self-hosted for internal workflows under its Sustainable Use License.
- Requires an always-on host, backups, patching and credential security.
- Not recommended as the canonical data store. Avoid exposing workflow-editor access or repackaging it as a hosted customer automation service without checking licensing.

### Recommended combination
Start with Option A as canonical store and daily batch runner. Keep the schemas platform-neutral so Option B can later host collection APIs or Option C can host a queryable graph database. Use Notion for narrative decisions and human-readable research briefs; Airtable only as an optional operational review table; Wix as a portal/dashboard, not the canonical store. Keep the existing WANGA-LAB repository as the authoritative source.

## 7. Research source plan

Initial source adapters:
- OpenAlex: broad scholarly works/authors/topics graph; free API key currently includes $1/day usage, with usage-based costs beyond that. Use filters and incremental windows to keep costs low.
- Crossref: DOI and publication metadata; public REST API, polite pool via mailto.
- arXiv: subject-specific preprints and version updates.
- PubMed / Europe PMC: biomedical literature and metadata; respect API limits and full-text licences.
- Standards and patent sources: add only after defining domain scope and terms.
- Project repositories and approved institutional sources: use versioned feeds/API endpoints.

Do not treat search-result snippets as adequate evidence for a canonical claim. Store bibliographic metadata and permitted abstracts; store full text only when the licence and access terms allow it.

## 8. Optimization metrics

Primary: QAT = independently accepted research/knowledge updates per unit time and cost at a fixed quality threshold.

Track:
- source coverage by selected topic and source;
- time from publication/discovery to candidate and approved update;
- duplicate rate and identifier resolution rate;
- evidence-anchor completeness;
- unsupported-claim rate in audited samples;
- contradiction detection precision/recall (requires labelled test set);
- false promotion rate and false abstention rate;
- proportion of proposed changes accepted, rejected and deferred;
- diagram reproducibility from the same graph version;
- schema/contract validation pass rate;
- API/model cost per accepted update;
- review minutes per accepted update;
- downstream agent acknowledgement and stale-version rate.

Do not publish numerical improvement forecasts until a baseline and a labelled evaluation set exist.

## 9. MVP sequence

Phase 0 — Freeze scope: choose 3 research domains, source list, watch terms and acceptance rules.
Phase 1 — Repository schema: JSON Schema, source envelope, claim/relation model, status model and sample fixtures.
Phase 2 — Daily collector: OpenAlex + Crossref + arXiv metadata; incremental cursor, deduplication and raw archive.
Phase 3 — Evidence extraction: source-anchored claims and relation candidates; no auto-promotion.
Phase 4 — Diagram compiler: graph JSON -> Mermaid L0-L4, deterministic rendering and visual diffs.
Phase 5 — Audit/review: contradiction checks, Naming–Place checks, human approval and immutable releases.
Phase 6 — Distribution: GitHub releases + static wiki + HTTPS/MCP read APIs.
Phase 7 — Optional database/UI: Cloudflare or Supabase only when repository-based querying becomes insufficient.
Phase 8 — Benchmark: compare daily workflow against manual research using the same tasks and quality rubric.

## 10. Current implementation status

This file defines the proposed architecture. It does not assert that collectors, agents, cron jobs, MCP servers, databases or a neural wiki have been deployed. Runtime status must be reported separately from specification status.

Acceptance condition for the first real pilot: a daily run produces a reproducible source batch, source-linked candidate claims, a graph diff, at least one generated diagram (or an explicit NO_CHANGE), a human-review decision and an immutable run receipt.
