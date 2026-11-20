# WANGA MCP Capability Combinatorics Factory — V1

**Status:** DESIGN SPECIFICATION / NOT RUNTIME-ACTIVE  
**Canonical repository:** Quadruple-Multilevel-projection-project/WANGA-LAB  
**Workstream:** MCP discovery, capability mapping, combinatorial composition and action-coordinate generation

## 1. Purpose

Create a governed layer that discovers available MCP endpoints, connector surfaces, tools and skills; extracts their declared contracts; maps dependencies and compatibility; composes useful capability clusters; assigns traceable action coordinates; and provisions a dedicated application only for a distinct, validated capability.

This is an extension of the existing WANGA Logic Factory. It does not replace the 175-term source registry, 14-gate routing index, existing map registry, or WANGA Agent Factory.

## 2. Existing canonical integration

The current source contract is docs/LOGIC_FACTORY/MASTER_MAP_INTEGRATION_CONTRACT.md, with registry docs/LOGIC_FACTORY/map_registry.v1.json.

Preserve:
- 175 numbered term records and their source locators.
- 14 gate identifiers and the current gate-to-term ranges.
- SERIAL_RETURN, PARALLEL_14_GATE, and COMPARISON as distinct pipeline configurations.
- Existing epistemic statuses and evidence rules.
- Existing app/map registry identities; do not create duplicates.

The master contract currently labels pipeline runtime wiring and map application connections as unresolved or not deployed. This V1 does not upgrade those statuses.

## 3. Resource model

Keep the following resource classes distinct:

| Resource class | Meaning |
|---|---|
| MCP_SERVER | Remote MCP server and endpoint identity |
| CONNECTOR_SURFACE | Host-provided integration or connector namespace |
| TOOL | Callable operation with a declared input/output contract |
| SKILL | Reusable procedural instructions |
| APP | User-facing application or runtime |
| DATA_RESOURCE | File, database, API resource or other data source |
| CLIENT | ChatGPT, Codex, Copilot, Cursor, VS Code, or another host |
| AUTH_CONTEXT | Identity, credential reference, permission scope and approval policy |

A connector/tool namespace visible in one ChatGPT session is not proof that a remote MCP endpoint is registered in another coding client. Every connection record must name its client, scope, endpoint and observed authentication state.

## 4. Capability registry

Each capability record must preserve:
- stable provider_id, resource_id, capability_id, and version;
- resource class and exact source name;
- source endpoint, client and connection scope;
- operation class: READ, SEARCH, CREATE, UPDATE, DELETE, EXECUTE, DEPLOY, VERIFY;
- declared input and output schemas, required fields and examples where available;
- authentication mechanism and permission scope;
- side-effect class, reversibility and human-approval requirement;
- declared dependencies, compatibility constraints and rate limits;
- source evidence locator and discovery timestamp;
- status from the project's established vocabulary or a specifically approved discovery status.

Do not infer an input schema from a tool name. Use the actual tool declaration. Do not infer endpoint availability from a connector label.

## 5. Composition graph

A candidate composition is a directed graph of capability nodes and typed handoff edges.

An edge is eligible only when:
1. the producer output is declared;
2. the consumer input is declared;
3. schema compatibility is checked;
4. the auth context permits the handoff;
5. the edge has a source/evidence locator;
6. failure and compensation behavior are specified where side effects exist.

Composition constraints:
- default to acyclic execution graphs;
- reject cycles unless a bounded loop contract explicitly declares termination and retry limits;
- reject destructive or irreversible operations without explicit approval and recovery policy;
- detect duplicate or overlapping operations;
- preserve intermediate outputs and provenance;
- isolate planning from execution;
- keep human confirmation enabled for mutations;
- never pass secrets through model-visible text or ordinary logs.

Candidate generation must be bounded and dependency-aware. Do not materialize every permutation of all tools. Cluster by distinct user outcome and demonstrated capability, then prune duplicates, incompatible schemas, privilege escalation paths and unsupported edges.

## 6. Action coordinate

Each validated composition receives an action_coordinate_id that identifies its execution plan, not an execution result.

Required fields:
- action_coordinate_id
- capability_cluster_id
- ordered capability_ids
- execution_graph
- input_contract and output_contract
- preconditions and postconditions
- auth_context_ref, permission_scope, and approval_gate
- idempotency_policy
- timeout_retry_policy
- compensation_policy
- per-step evidence_locator
- verification_plan
- app_ref only after an app exists and has been read back
- version, timestamp and change_event_id

An action coordinate becomes EXECUTED only with actual tool/runtime evidence for every required step. A plan or successful render is not execution evidence.

## 7. Application generation policy

Candidate application families:
1. MCP Discovery & Registry.
2. Capability Graph & Relations.
3. Combinatorial Planner.
4. Action Coordinate Builder.
5. Capability App Foundry.
6. Execution & Evidence Monitor.

These are candidate product boundaries, not deployed apps. Search existing app and map registries before creating any new application. Extend an existing application when it already owns the same user workflow.

Create a separate application only when:
- the capability cluster has a distinct user outcome;
- its component tools and edges are source-backed;
- schemas and permission boundaries pass checks;
- its action coordinate is stable;
- an acceptance test covers its material workflow;
- Product Design has selected the visual direction;
- deployment and read-back evidence can be captured.

Do not create one app per arbitrary tool sequence.

## 8. Mapping pipeline

DISCOVER → IDENTIFY → EXTRACT_CONTRACT → NORMALIZE → MAP_RELATIONS → GENERATE_CANDIDATES → PRUNE → VALIDATE → ASSIGN_ACTION_COORDINATE → DESIGN → BUILD → TEST → DEPLOY → READ_BACK → MONITOR

Maintain separate records for discovery evidence, capability definitions, relation/compatibility evidence, candidate compositions, validation results, action coordinates, application records and runtime execution events.

## 9. Evidence and status rules

Use the existing WANGA evidence discipline:
- INDEXED is not SOURCE-CHECKED.
- SOURCE-CHECKED is not RELATION-CHECKED.
- RELATION-CHECKED is not automatically VERIFIED.
- Missing source, schema or evidence => BLOCKED or UNRESOLVED.
- Ambiguous inputs => ABSTAIN.
- Contradiction with a verified source => REJECTED / HALT for the affected path.
- No invented tool capabilities, endpoint URLs, costs, latencies, permission scopes or weights.
- WEIGHTS = NOT_CREATED until the governing logic is source-grounded and verified.

## 10. Initial environment inventory

The connected ChatGPT tool catalog exposed 24 integration/tool namespaces and 898 declared tool entries in the current session inventory. This is a host-session inventory only. It is not a verified list of 24 remote MCP servers, and it does not establish that these endpoints are registered in Codex CLI or another local client.

See docs/LOGIC_FACTORY/connected_tool_surface_inventory_2026-11-20.json.

## 11. Implementation gates

1. Complete connector/tool inventory and capture exact declared schemas.
2. Inspect WANGA-LAB.-01 Agent Factory routing and existing connection records.
3. Add capability registry and action-coordinate schemas.
4. Build a small evidence-backed sample of useful compositions.
5. Validate schema handoffs, permissions, duplicate suppression and failure recovery.
6. Use Product Design in ChatGPT Work mode to select one of three visual directions before UI implementation.
7. Build and deploy the first registry/planner app only after the product brief and tests are complete.
8. Create additional apps only from distinct, validated capability clusters.

## 12. Current status

- Existing WANGA master map contract and registry were inspected at commit 3e5e02fe691198176f61edb0ea6e1df0555ed24b.
- Notion coordination draft was created and read back: https://app.notion.com/p/41e49ee8e17d81cd96a5f993ab0763f8.
- AppDeploy instructions were retrieved for a React/Vite frontend+backend build; no app was deployed.
- Vercel connector documentation and authenticated team listing were previously accessible; the CLI install attempt timed out in the execution container.
- Product Design's full workflow is not available in standard ChatGPT chat. UI ideation/build is pending Work mode.
- Remote MCP registration in an external coding client remains unverified.
- No autonomous agents or MCP-composition runtime are claimed active.

## 13. Action signatures

### Branch creation
Timestamp=2026-11-20T02:55:43+02:00  
Contract_Start_Time=2026-11-17T20:29:00+02:00  
Action_ID=WANGA-MCP-FACTORY-GITHUB-BRANCH-001  
SHA256=9fc53e5ff3a821b83659077e28cbaf15ea62f118a3a111d928aa2bb234441869

### Specification file creation
Timestamp=2026-11-20T02:56:01+02:00  
Contract_Start_Time=2026-11-17T20:29:00+02:00  
Action_ID=WANGA-MCP-FACTORY-GITHUB-SPEC-002  
SHA256=333adbb1cb8a2db6cb8b5f5f7f894409cc87eb9140e996522aab1865d3731199

Status: SPECIFICATION ONLY. No contract seal, runtime activation, deployment or end-to-end verification is claimed.