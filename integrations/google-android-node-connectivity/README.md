# Google / Android Node Connectivity

Status: PROPOSED / repository research completed; no Google Cloud project, Android device, MCP endpoint, or Android Studio host has been connected from this commit.

## Purpose

Create a capability-based connectivity layer for WANGA that can discover, register, test, and map Android devices, emulators, edge compute nodes, cloud services, and remote MCP servers. A node is a bounded compute or service endpoint; it is not assumed to be a large model host.

## Design constraints

- Treat "nano-server" and "nano-processor" as project architecture terms for small, bounded compute nodes unless a physical hardware specification proves a literal nanoscale device.
- Do not move model weights between nodes by default. Route compact task envelopes, input references, bounded payloads, result records, and provenance.
- Keep compute, connectivity, and logical topology as separate layers.
- Require explicit identity, least-privilege authorization, capability discovery, health checks, and audit records before a node is marked VERIFIED.
- Never store API keys, OAuth secrets, service-account JSON, or device credentials in Git.
- An unavailable endpoint is UNKNOWN, not FAILED; a successful handshake is not proof of functional correctness.
- All generated applications are projections of an approved logical configuration; they cannot grant themselves new permissions.

## Google developer surface inventory

| Surface | Intended role | Evidence / maturity |
|---|---|---|
| Android CLI | Agent-accessible Android build, test, device, emulator, screen/layout inspection and Android Studio analysis | Official Android Developers CLI documentation |
| Android Studio BYOA / ACP | Bring compatible coding agents into Android Studio with IDE-native project context and tools | Announced as preview in Android Developers Blog, 2026-09-24 |
| Android Studio MCP Servers | Connect MCP tools from IDE Agent Mode | Android Studio documentation / release guidance |
| Android Management API MCP | Remote MCP for enterprise Android fleet data and policy operations | Preview; requires Google Cloud project and API enablement |
| Android Emulator Container Scripts | Containerized emulator infrastructure | Public Google repository |
| Android Cuttlefish | Virtual Android device infrastructure | Public Google repository |
| ADK Web / ADK Recipes | Agent development and reference patterns | Public Google repositories |
| XNNPACK | Optimized inference operators for mobile, server and web | Public Google repository |

## Official references

- https://developer.android.com/cli
- https://developer.android.com/studio/services
- https://developer.android.com/studio/intro
- https://developers.google.com/android/management/use-android-management-mcp
- https://github.com/google/android-emulator-container-scripts
- https://github.com/google/android-cuttlefish
- https://github.com/google/adk-web
- https://github.com/google/adk-recipes
- https://github.com/google/XNNPACK

## Node lifecycle

1. DISCOVER — identify provider, endpoint, protocol, device class and published capabilities.
2. DESCRIBE — obtain a bounded capability manifest and resource envelope.
3. AUTHORIZE — bind an identity and least-privilege scopes; secrets remain in a secret manager.
4. CONNECT — establish transport (MCP Streamable HTTP, ACP, HTTPS API, ADB/Android CLI, WebSocket or provider SDK).
5. PROBE — run non-destructive health and capability checks.
6. VERIFY — test an approved read-only operation and, separately, any authorized write/execute operation.
7. REGISTER — write a versioned node record and graph edges with evidence.
8. MONITOR — heartbeat, latency, resource pressure, capability drift and revocation.
9. QUARANTINE — remove routing eligibility when identity, schema, policy or integrity checks fail.

## Small-payload execution contract

A task envelope should contain:
- task_id, correlation_id, schema_version
- requested_capability and policy_scope
- input_refs (content-addressed references where possible)
- bounded inline_payload_bytes
- deadline_ms and resource_budget
- provenance_ref and expected_output_schema

A result should contain:
- task_id, node_id, status
- output_ref or bounded output_payload
- execution_metrics (duration, bytes_in, bytes_out, resource class)
- evidence_refs, error_code, completed_at

Large artifacts stay in object storage or their source system. Nodes exchange references and bounded excerpts, not entire repositories or model weights.

## Initial implementation phases

- Phase 0: maintain this provider inventory and schemas (this commit).
- Phase 1: implement read-only Android CLI discovery and local emulator inventory on a controlled host.
- Phase 2: implement MCP connector registry and handshake tests.
- Phase 3: integrate Google Cloud / Firebase service identities and approved APIs.
- Phase 4: build the live logical topology map and node health dashboard.
- Phase 5: enable task routing only after Analytics policy and independent verification approve each capability.

## Non-goals

- No automatic provisioning of paid cloud resources.
- No automatic creation of Google Cloud projects or OAuth credentials.
- No device management actions without explicit authorization.
- No claim that Android devices are physical nano-processors.
- No deployment or production readiness claim from repository documentation alone.
