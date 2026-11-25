# External Agent Convergence and Verification — 2026-11-25

**Evidence classification:** VERIFIED for the cited public specifications/documentation; ASSESSMENT for architectural comparison; NOT_YET_VERIFIED for AI231 runtime equivalence or independent semantic validation.

## Primary-source comparison

| System | Demonstrated/documented mechanism | Boundary that must not be confused |
|---|---|---|
| OpenAI agent platform | Current developer documentation separates tools, multi-agent handoffs, conversation state, background execution and production guidance. The SDK provides a structured agent loop and observability patterns. | A handoff or trace is not a sandbox; production safety still depends on tool permissions, backend and runtime configuration. |
| LangGraph | Graph API models execution as nodes, edges and shared state; persistence/checkpointing, interrupts and fault-tolerance support durable, resumable workflows. | Graph orchestration and persistence are not OS/container isolation or network-egress denial. |
| A2A v0.2.6 | Defines Agent Cards, tasks, messages, artifacts, JSON-RPC over HTTP(S), and optional SSE streaming for long-running agent interactions. | Interoperability does not establish trust, correctness or authority; each server remains responsible for authentication and authorization. |
| MCP 2026-07-28 | The protocol is stateless at the protocol layer; request context and task identifiers must be explicit. Authorization guidance requires audience-bound tokens, token validation and rejects token passthrough. | A tool protocol is not a policy engine or runtime sandbox. Token storage, scopes, consent and resource authorization remain implementation responsibilities. |
| Google Agent Mesh | The project documents service-name routing, outbound QUIC/TLS connections, no inbound ports by default, short-lived credentials and policy-controlled service calls. | This is a concrete project architecture, not a universal standard or proof that another agent runtime is isolated. |

## Architectural convergence

The strongest convergence is operational, not metaphysical: agent identity/capabilities, explicit task state, tool interfaces, durable execution, tracing, authorization, network boundaries and acceptance tests are becoming separate design concerns. A robust system composes these layers instead of treating a graph, prompt or protocol as the whole agent.

For AI231/WANGA, the resulting implementation order is:
1. keep each agent task-bounded with explicit inputs/outputs and least-privilege permissions;
2. use immutable, provenance-linked inputs and explicit task IDs;
3. separate orchestration/persistence from sandboxing;
4. deny network egress by default and broker only approved destinations;
5. log every tool invocation and policy decision;
6. test positive, negative and boundary cases on the exact commit;
7. keep all unverified claims and runtime states visibly unresolved.

## AI231 comparison and status

**VERIFIED:** the existing Wix Site Evidence Auditor blueprint and contract tests exist in WANGA-LAB; its current CI contract is read-only and requires supplied snapshots. This run adds a deterministic navigation-coverage classifier that distinguishes a multi-page isolated-page candidate from a legitimate single-page site and from insufficient evidence.

**NOT_YET_VERIFIED:** no exact-version backend configuration, successful non-dummy invocation log, OS/container isolation proof, network-egress denial test or production acceptance run was available. The auditor remains DRAFT / NOT_CONFIGURED. No external system is claimed to have adopted or validated AI231's logical architecture.

**Assessment:** the technical market is converging on bounded tool-using agents with explicit task state and stronger security controls. AI231 differentiation must therefore be demonstrated through reproducible logical checks, provenance quality, low false-positive rates and paid customer outcomes—not through agent count, protocol compatibility or architecture claims alone.

## Primary sources

- OpenAI developer documentation — Building agents: https://developers.openai.com/tracks/building-agents
- LangGraph — Thinking in the Graph API: https://docs.langchain.com/oss/javascript/langgraph/thinking-in-graph-api
- LangGraph — Persistence: https://docs.langchain.com/oss/python/langgraph/persistence
- A2A Protocol v0.2.6 specification: https://a2a-protocol.org/v0.2.6/specification/
- MCP stateless protocol specification: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/index.mdx
- MCP authorization security considerations: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/authorization/security-considerations.mdx
- Google Agent Mesh architecture: https://google.github.io/agentmesh/
- Google Agent Mesh external ingress: https://google.github.io/agentmesh/docs/guides/external-ingress/


## 2026-11-25 — Run 006 primary-source revalidation

### Demonstrated external architecture patterns

- **OpenAI Agents API and Agents SDK:** the official documentation describes durable sessions, events, resumable work, sub-agent delegation and optional sandbox environments. The sandbox guide separates the harness/control plane (agent loop, tool routing, approvals, tracing and recovery) from the compute plane (files, commands, packages, ports and snapshots). Isolation remains provider/backend-specific; the existence of an SDK or sandbox interface is not evidence that a particular application has a confined runtime.
- **LangGraph:** the official walkthrough decomposes workflows into nodes over shared state and uses a checkpointer for persistence. interrupt() pauses for human input and resumes from saved state. This is orchestration and durable execution, not an OS/container security boundary.
- **A2A:** the current project specification defines Agent Cards for capability and interaction discovery, task/message objects, asynchronous task lifecycle, status/artifact streaming and multi-turn context. It standardizes agent-to-agent interoperability; it does not by itself authorize a tool call or confine code execution.
- **MCP authorization:** the official 2026-07-28 security considerations recommend short-lived access tokens and require refresh-token rotation for public clients. OAuth/resource authorization is an identity and access-control layer, not a sandbox or proof of workload integrity.
- **Human review and guardrails:** OpenAI's official guide distinguishes automated input/output/tool checks from approval interruptions for sensitive side effects. Enforcement must be placed at the actual tool boundary; a prompt-only promise is insufficient.

### Convergence assessment

The demonstrated convergence is toward: (1) explicit task and capability contracts, (2) durable task state and resumability, (3) standard tool and agent interoperability, (4) human approval at side-effect boundaries, (5) structured traces/artifacts, and (6) provider-specific execution isolation. These capabilities are complementary, not interchangeable.

### AI231/WANGA implementation implication

Keep the Wix Site Evidence Auditor bounded and snapshot-only. The new canonical-metadata helper is deterministic and performs no network requests. Before describing any AI231 agent as active, require an exact-version configured backend, a non-dummy invocation record, task-scoped permissions, OS/container isolation, enforced network-egress denial, audit logs and acceptance results. The current runtime-catalog CI installs frameworks and runs generic graph/runtime tests, but it does not prove that this Wix auditor is deployed or isolated.

**VERIFIED:** official specifications and documentation describe the capabilities above; WANGA-LAB's exact blueprint/schema/test workflow passes on its recorded commit.

**ASSESSMENT:** these are converging engineering patterns, not evidence that external projects adopted AI231's logical architecture.

**HYPOTHESIS:** AI231 differentiation must be established by source-grounded logical cases, independent semantic benchmarks, low false-positive rates and paid customer outcomes—not by agent counts, protocol compatibility or workflow green status.

**NOT YET VERIFIED:** AI231 semantic truth, independent reviews, a deployed Wix auditor runtime, runtime isolation, customer willingness to pay, collected cash or positive contribution margin.

### Primary sources
- OpenAI Agents API: https://developers.openai.com/api/docs/guides/agents-api/overview
- OpenAI Sandbox Agents: https://developers.openai.com/api/docs/guides/agents/sandboxes
- OpenAI guardrails and human review: https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
- LangGraph — Thinking in LangGraph: https://docs.langchain.com/oss/javascript/langgraph/thinking-in-langgraph
- A2A protocol specification: https://github.com/a2aproject/A2A/blob/main/docs/specification.md
- MCP authorization security considerations: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2026-07-28/basic/authorization/security-considerations.mdx
