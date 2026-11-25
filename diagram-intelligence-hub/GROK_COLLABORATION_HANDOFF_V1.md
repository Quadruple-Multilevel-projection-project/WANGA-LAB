# Grok ↔ WANGA-LAB Collaboration Handoff — v1

**Status:** SPECIFIED / NOT_YET_VERIFIED  
**Purpose:** Provide a deterministic collaboration protocol for Grok and other external models to inspect and challenge diagram architecture without granting them authority to silently change canonical sources.

## 1. Shared workspace

Repository: `Quadruple-Multilevel-projection-project/WANGA-LAB`

Start every review by reading, in order:

1. `AI_LOGIC_FACTORY_DIAGRAM_INDEX.md`
2. `docs/AI_MODEL_HANDOFF_PROTOCOL_V1.md`
3. `diagram-intelligence-hub/README_V1.md`
4. `diagram-intelligence-hub/DIAGRAM_INGEST_CONTRACT_V1.json`
5. The specific source contracts and diagram files named in the task.

The repository is the shared evidence surface. Airtable is the operational register; Notion is the decision record. Neither replaces source files.

## 2. Grok's permitted role

Grok may:
- inspect source files and diagram versions;
- extract nodes, edges, labels, subgraphs and references;
- identify duplicates, missing links, possible contradictions and drift;
- challenge interpretations made by another model;
- submit structured findings and proposed patches.

Grok must not:
- rewrite or delete canonical source files directly;
- mark its own output VERIFIED or LOCK;
- invent missing definitions, topology constraints, weights, coordinates or formulas;
- merge contradictory sources without explicit evidence;
- copy credentials, API keys or private data into repository artifacts.

## 3. Required candidate packet

Every submission must include:
- `candidate_id`
- `source_artifact_id`
- exact source URL and repository path where applicable
- source commit/ref and exact-byte SHA-256 where available
- extractor/model name and version
- contract/schema version
- extracted nodes and edges, each with source location
- findings, uncertainty notes and unresolved questions
- proposed relations with evidence
- requested next action: `REVIEW`, `ABSTAIN` or `PROPOSE_PATCH`

Use the JSON shape in `DIAGRAM_INGEST_CONTRACT_V1.json`.

## 4. Review protocol

1. **Independent pass:** Grok reads the source and submits its own candidate without copying another model's conclusion.
2. **Cross-examination:** a second reviewer compares each material claim against the original artifact and governing contracts.
3. **Difference report:** record agreement, disagreement, omissions and unsupported claims separately.
4. **Audit gate:** run source-integrity, parse, layer, contract, topology, safety and provenance checks.
5. **Human review:** unresolved contradictions, new architectural claims and high-impact changes go to the project architect.
6. **Patch proposal:** accepted changes are prepared on a branch and submitted as a pull request.
7. **Merge:** only an authorized human merges the PR after checking the diff and evidence.

A model-to-model exchange is not itself a meeting, consensus or verification event. Each review must be represented by a traceable candidate packet or GitHub discussion/PR.

## 5. Decision semantics

- `LOCK`: all mandatory checks pass, provenance is complete, and any required human approval is recorded.
- `HUMAN_REVIEW`: novelty, impact, conflicting evidence or a material architectural interpretation needs a human decision.
- `ABSTAIN`: a required definition, source, mapping or test is missing.
- `SANDBOX`: candidate material may be inspected but must not enter the canonical registry.

No vote count or model confidence overrides these rules.

## 6. Daily collaboration cycle

At each daily cycle:
- compare the current repository head with the previous recorded snapshot;
- ingest new Wix submissions and Grok candidate packets;
- compare each candidate to the canonical repository artifacts;
- write an evidence-backed report and proposed PR;
- publish a concise daily summary with changed files, findings, review decisions and blocked items.

The daily cycle remains **NOT_YET_VERIFIED** until a scheduler, source connectors and an end-to-end run have been tested. No fixed time is implied by this specification.

## 7. Security boundary

The Wix HTTP action inspected for the Logical AI Atlas site exposes URL, method and body configuration but no custom Authorization-header field. Therefore Wix must not call the Grok API directly with an exposed API key. Use a secured intermediary service with secrets stored in its secret manager, request validation, rate limiting and audit logging. Never put the Grok key in Airtable, Notion, Wix page content or GitHub.

## 8. Submission template

Use the schema in `DIAGRAM_INGEST_CONTRACT_V1.json`. If a required field cannot be established, leave it null and explain why. Do not guess.
