# Agent convergence and runtime security — 2026-11-24 update

## Executive finding

The strongest practical architecture is layered, not a single-agent-framework choice:

- **LangGraph**: explicit workflow nodes, state, checkpointing, interruption and resumability.
- **A2A**: discovery and task/message/artifact exchange between independent agents.
- **MCP**: structured access to tools, APIs and data resources.
- **Sandbox backend**: OS/filesystem/process/network isolation for execution.
- **AI231 policy + verifier**: permission decisions, evidence provenance, acceptance tests, rollback and audit trail.

These layers solve different problems. None should be treated as a substitute for the others.

## Primary-source comparison

### 1. A2A Protocol

The current A2A specification defines task lifecycle operations, agent discovery through Agent Cards, asynchronous task updates and multiple protocol bindings. It describes in-task authorization using `TASK_STATE_AUTH_REQUIRED`, including a handoff to the client for approval. Crucially, the specification states that it does not define the scope, representation, validity or revocation semantics of the authorization decision/credential; the implementation or extension must define those details. The state transition itself is not authorization for a specific operation.

Source: https://a2a-protocol.org/latest/specification/  
Relevant sections: introduction and protocol layers; 7.6 In-Task Authorization; Appendix B Relationship to MCP. Accessed 2026-11-24.

### 2. Model Context Protocol authorization

The 2025-11-25 MCP authorization specification defines OAuth-based transport authorization for HTTP-based MCP implementations. It requires a server to validate that an access token is intended for that server, rejects tokens for other resources, and forbids token passthrough. Authorization is optional for MCP implementations, and STDIO transport uses a different credential model.

This is a strong tool-access boundary, but it is not a process sandbox and does not by itself prevent an agent from executing arbitrary code elsewhere.

Source: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization  
Relevant sections: Purpose and Scope; Access Token Usage; Token Audience Binding and Validation; Access Token Privilege Restriction. Accessed 2026-11-24.

### 3. OpenAI Agents SDK sandbox guidance

The official sandbox guide separates the agent definition, manifest, sandbox session and sandbox client. It explicitly says isolation depends on the backend and configuration; a sandbox session does not itself guarantee OS-level confinement. The guide also states that the Unix-local Linux backend runs host processes without OS-level confinement and that macOS filesystem restrictions do not provide network isolation. For untrusted commands it recommends a properly configured Docker or hosted provider, or external isolation.

This directly supports the AI231 runtime boundary: a LangGraph graph, an agent blueprint or a local workspace is not proof of a secure sandbox.

Source: https://openai.github.io/openai-agents-python/sandbox/guide/  
Relevant sections: Concepts; Choose a sandbox client; Permissions. Accessed 2026-11-24.

### 4. LangGraph workflow persistence

The LangGraph Graph API documentation models an agent as discrete nodes connected by shared state, with checkpointing and interrupt/resume behavior. This is useful for deterministic workflow structure, traceability and recovery. It does not establish OS isolation or network-egress policy.

Source: https://docs.langchain.com/oss/javascript/langgraph/thinking-in-graph-api  
Relevant sections: workflow nodes, shared state, checkpointer, interrupt/resume. Accessed 2026-11-24.

## Demonstrated internal implementation versus proposal

**VERIFIED**
- WANGA-LAB PR #160 head: `b06dbd05648fa90baa9ad1bc4787aacc599b8811`.
- Wix auditor blueprint: `agent_blueprints/ai231-wix-site-evidence-auditor.json`, SHA `4560b0b4ce900ace6c32cbbe9465f23b4da67bf2`, status `draft`.
- Agent contract CI run `45344474779`, job `138275622985`: contract verification, exact JSON Schema validation and Wix auditor tests all succeeded on that commit.
- Runtime catalog CI run `45344474785`: pinned framework installation, import/graph smoke test, runtime-catalog validation and blueprint validation succeeded on that commit.
- PR #167 is an internal research candidate. Its report records 28 source-referenced articles, 17 source records across 11 classes and 111 editorial relation links.

**NOT YET VERIFIED**
- No deployed Wix auditor runtime, real worker invocation, container image digest, OS isolation result or network-egress denial result is evidenced.
- PR #167 reports zero source-grounded semantic cases, zero benchmark suites and zero independent reviews. Editorial relation links are not semantic entailment evidence. Candidate remains NOT_READY / INTERNAL ONLY.
- No external team adoption, copying, causal influence or commercial demand is established by the source catalog.

## Architecture decision for WANGA

1. Keep LangGraph as orchestration/state/checkpointing only.
2. Use A2A for agent-to-agent task contracts, task status and artifacts.
3. Use MCP for narrowly scoped tool/resource access with audience-bound credentials and least privilege.
4. Put untrusted execution in an externally isolated container/VM with explicit filesystem mounts and denied network egress.
5. Keep authorization decisions outside agent-generated text. An A2A `AUTH_REQUIRED` state must be resolved by an explicit policy/credential issuer.
6. Hash the input snapshot, blueprint, runtime image/policy and output. Preserve an audit trail and a compensating rollback.
7. Do not mark any WANGA agent active until backend configuration, real invocation logs, isolation/egress tests and exact acceptance tests pass.

## Assessment

The external standards are converging on interoperable agent identity, task exchange, tool interfaces, structured authorization and resumable workflows. The engineering gap remains the enforcement layer: identity and protocols do not prove execution isolation, authorization scope, semantic correctness or safe side effects. WANGA should differentiate through evidence provenance and deterministic acceptance gates rather than claiming that protocol adoption alone creates a secure or verified agent network.
