# Constitutional Fractal Scan & Agent Dispatch Network — v1.0

**Date:** 2026-11-26  
**Status:** WORKFLOW SPECIFICATION / NOT_YET_VERIFIED as an automated runtime  
**Applies to:** WANGA-LAB, AI231, cross-model cabinet, Diagram Intelligence Hub

## 1. Operating rule

The Constitution governs the work. Models and agents are evidence collectors, source mappers, auditors, and report producers; they are not constitutional authorities.

The first round is mapping-only. It does not authorize full extraction, specification writing, code changes, implementation, constitutional amendment, or automatic reconciliation.

## 2. Two deliverables in Round 1

### A. Constitutional Fractal Map

Search all accessible sources, including sources not titled Constitution and material predating the formal constitutional document. Candidate material includes chats, source documents, diagrams, code, contracts, research notes, images, and other project records.

For each candidate fractal return only:
- short ID / name;
- source and exact location (repo/path/page/line/span/URL, version or commit when available);
- short quote or faithful description;
- EXPLICIT or IMPLICIT;
- contradiction, missing evidence, or uncertainty if present.

Do not merge similar fractals. Do not resolve conflicts. Do not invent missing content. Preserve each source's own wording, context, and date/version.

### B. Preliminary Priority List

Only after the constitutional scan, list remaining subject areas under P1–P7 as headings:
- what material exists;
- what should be extracted next;
- what is missing.

No long explanations and no implementation.

### C. Critical Gaps / Conflicts

List unresolved source gaps, contradictory formulations, inaccessible sources, and unknown canonical versions. Keep each branch separate.

## 3. Global sequence

1. Broad constitutional scan across source collections and models.
2. Per-model preliminary P1–P7 list.
3. Consolidate all reports into a shared constitutional map, source map, gap/conflict register, and unified priority list.
4. Only then begin full extraction of constitutional fractals in the consolidated order.
5. After verification of P0–P5, consider implementation through a separate authorization gate.

No model may skip a stage or expand its assignment without a new task instruction.

## 4. Agent network — functional roles

These are logical agent roles, not a claim that separate runtimes are deployed.

| Role | Responsibility | Output |
|---|---|---|
| Network Coordinator | Assign bounded tasks, enforce round and token limits | Task envelope / dispatch ledger |
| Source Discovery Agent | Locate candidate sources across assigned repositories and archives | Source index |
| Constitutional Fractal Scanner | Identify possible constitutional passages, including pre-constitution material | Fractal candidate rows |
| Provenance Agent | Preserve source path, version, commit, locator, and hash where available | Provenance record |
| Conflict & Gap Agent | Detect contradictions, missing source spans, inaccessible evidence | Open conflict/gap records |
| Priority Agent | Produce P1–P7 headings for non-constitutional material only | Preliminary priority list |
| Consolidation Agent | Combine reports without merging conflicts or upgrading status | Unified map and delta report |
| Diagram Agent | Generate derived Mermaid/JSON views from accepted registry records | Diagram diff / snapshot |
| Independent Audit Agent | Check coverage, provenance, status, and compliance with the assigned round | Audit receipt / ABSTAIN |
| Notification Router | Prepare change notices and route them to the relevant model/agent groups | Email dispatch package |

A role may be fulfilled by an existing agent seat or model. Do not create duplicate runtimes merely to match this list.

## 5. Dispatch modes

The coordinator selects a mode per task; modes can be combined when the task envelope says so.

- **HORIZONTAL_SWEEP:** parallel source/model scan across independent repositories, document groups, or providers. Used for broad coverage.
- **VERTICAL_SYNTHESIS:** combine findings across layers or sources into a common map, while preserving source-specific claims and open conflicts.
- **DEEP_EXTRACTION:** bounded, source-by-source full extraction. Disabled during Round 1; enabled only after consolidation.
- **TARGETED_REGION:** inspect one named source, file, node, layer, time range, or conflict cluster. Do not broaden beyond the target.
- **PRIORITY_CHAIN:** execute in P1→P7 order where dependencies or scarce model budget require serial dispatch.
- **PARALLEL_FANOUT:** distribute independent tasks concurrently, then collect results at the consolidation gate.
- **EVENT_DELTA:** process only the changed source/version and its declared dependants; do not rescan the entire corpus unless the change invalidates the index.
- **INDEPENDENT_REVIEW:** assign a different model/agent to verify critical findings without inheriting the author's conclusion as authority.

Every task envelope declares mode, scope, exclusions, source/version baseline, expected output, token/output cap, deadline if relevant, and return status.

## 6. Diagram update contract

Diagrams are derived navigation and analysis views, not constitutional sources of authority.

A diagram update must:
1. reference the constitution/contract version and source commit used;
2. identify changed nodes and edges;
3. preserve relation types and evidence status;
4. show conflicts and unknowns rather than resolving them visually;
5. label proposed or not-yet-verified components;
6. include a diagram diff and generation timestamp;
7. never imply a provider connection or runtime deployment without evidence.

GitHub/WANGA-LAB remains the artifact and version record. GitDiagram is a read-only/derived visualization surface unless a verified write workflow is established.

## 7. Update and email routing policy

Email is a notification and task-dispatch channel, not a source of truth. GitHub stores the versioned task, report, diagram, and change record.

Routing rules:
- Constitutional or contract change: immediate notice to all affected agents/models, with the exact version, changed paths, and required acknowledgement.
- Dependency-ordered work: send top-down by priority/dependency (P0/P1 first, then dependent work).
- Independent horizontal work: fan out in parallel to the relevant source/model groups.
- Vertical synthesis: notify layer owners and the consolidation/review roles.
- Deep extraction: notify only assigned extractors and their independent reviewers.
- Targeted-region update: notify only agents subscribed to that region plus the coordinator.
- No relevant change: no email.
- No email is sent until recipient addresses and routing groups are supplied and approved.

Every notice links to a versioned GitHub task/change record. Never send secrets, API keys, private credentials, or unsupported claims in email.

## 8. Tool and platform responsibilities

| Platform | Assigned function | Current boundary |
|---|---|---|
| GitHub / WANGA-LAB | Canonical files, contracts, task envelopes, reports, diagrams, version history | Repository artifact presence does not prove runtime enforcement |
| Notion | Human-readable operating manual, decisions, source links, change history | Documentation layer; not source-code authority |
| Airtable | Agent roster, diagram registry, relationships, audit ledger, task/notification registry | Registry records do not prove agents are running |
| MongoDB Atlas | Optional graph/document/vector persistence when a connected project and approved schema exist | No Atlas project was visible in the current connected account check; do not assume deployment |
| MCP Precheck | Preflight review before adding/configuring an MCP server | Advisory until human approval; no new server is being added in this update |
| Codex Dev Workflows | Scoped repository investigation, orchestration, QA, code review, and session handoff | Workflow guidance, not a separate agent runtime |
| Codex Material Themes | Codex editor appearance and readability only | Not part of the agent execution graph |
| GitDiagram | Derived repository visualization | Existing snapshot was reported stale; refresh and write-back are not verified |
| AgentMail | Approved dispatch and response channel | Recipient network not yet supplied; no inbox creation or email send authorized |

## 9. Low-token and anti-stall controls

- Round 1 output is capped to the three deliverables above.
- No full extraction, code, implementation, or long narrative in Round 1.
- Use source IDs and short locators; quote only the minimum needed to identify a candidate.
- One task per bounded source group; split oversized work rather than retrying indefinitely.
- A model may return PARTIAL, NEEDS_SPLIT, or ABSTAIN with the reason.
- Coordinator tracks progress by source coverage, not by volume of generated text.
- Stop after one bounded retry for a failed source; record it as a gap and continue elsewhere.
- Do not repeatedly re-scan unchanged sources. Use EVENT_DELTA when a source changes.

## 10. Required report envelope

```text
TASK_ID:
ROUND: 1
MODE:
MODEL / AGENT:
CONSTITUTION_VERSION_READ:
SOURCE_SCOPE:
SOURCES_SCANNED:
A. CONSTITUTIONAL FRACTAL MAP:
  - ID | source/location | short quote/faithful description | EXPLICIT/IMPLICIT | gap/conflict
B. PRELIMINARY PRIORITY LIST:
  - P1–P7 heading | material exists | next extraction candidate | missing
C. CRITICAL GAPS / CONFLICTS:
STATUS: COMPLETE / PARTIAL / NEEDS_SPLIT / ABSTAIN
TOKEN / OUTPUT BOUNDARY:
NEXT_ACTION:
```

## 11. Acceptance boundary

Round 1 is complete only when each assigned model has returned A, B, and C or an explicit PARTIAL/ABSTAIN status; the coordinator has recorded source coverage and unresolved gaps; and the consolidated map has not silently merged or resolved conflicts.

**Implementation status:** This file defines the intended operating model. Automated orchestration, model-provider connections, scheduled diagram refresh, and email routing remain NOT_YET_VERIFIED until demonstrated by execution traces and acknowledgements.
