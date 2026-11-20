# Agent Convergence, Interoperability and Verification — Evidence Review
Date: 2026-11-20
Status: RESEARCH / ASSESSMENT — not a claim that one universal architecture has emerged.

## Primary-source findings

### 1. OpenAI Agents SDK — runtime guardrails and observability
The current SDK documentation describes input/output guardrails, tool guardrails, tripwires, lifecycle hooks, tool approval and tracing metadata. This is an implemented developer interface, not proof that every agent runtime uses the same policy model.
- Guardrails: https://openai.github.io/openai-agents-python/guardrails/
- Agent lifecycle and hooks: https://openai.github.io/openai-agents-python/agents/
- Running agents, tracing and tool execution: https://openai.github.io/openai-agents-python/running_agents/

### 2. GitHub Agentic Workflows — agent execution inside CI
GitHub announced general availability on 28 October 2026. Its published design includes read-only repository access by default, a sandboxed container, an Agent Workflow Firewall, safe outputs and threat-detection review. The release also documents Cloud Hypervisor / NVX micro-VM isolation options. This is a released workflow product with concrete controls; the vendor's performance claims are not independently validated by this review.
- https://github.blog/changelog/2026-10-29-github-agentic-workflows-generally-available/

### 3. MCP — tool/context interoperability and long-running tasks
The 2026-07-28 MCP release candidate describes a stateless protocol core, authorization hardening, extensions and a Tasks lifecycle. The Tasks extension defines server-directed asynchronous work through `tasks/get`, `tasks/update` and `tasks/cancel`. This is protocol/specification evidence; compatibility and security still depend on each implementation.
- https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
- https://tasks.extensions.modelcontextprotocol.io/specification/2026-07-28/tasks

### 4. A2A — agent-to-agent communication
Google and the Linux Foundation announced the Agent2Agent project on 23 June 2025, with an open protocol and multi-company governance. A2A addresses agent-to-agent communication; MCP addresses tool/context access. They are complementary layers, not interchangeable protocols.
- https://developers.googleblog.com/en/google-cloud-donates-a2a-to-linux-foundation/
- https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/

### 5. LangGraph — durable orchestration and human interrupts
LangGraph documentation describes discrete stateful nodes, pause/resume, inspectable state and human-input interrupts. This is orchestration and durable execution; it does not itself provide a security sandbox or deny network egress.
- https://docs.langchain.com/oss/javascript/langgraph/thinking-in-langgraph

### 6. NIST — agent identity, authorization and adversarial evaluation
NIST's 18 May 2026 analysis of agent-security RFI responses identifies agent-specific security and assurance challenges. Its 27 October 2026 identity design-tenets post emphasizes identity and authorization as prerequisites for scale. NIST's 9 November 2026 draft taxonomy covers attacks on agentic systems, including multi-step and external-resource risks. These are standards/research inputs, not a certification of any specific product.
- https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai
- https://www.nist.gov/blogs/cybersecurity-insights/design-tenets-agent-identity-management-systems
- https://csrc.nist.gov/News/2026/adversarial-machine-learning-taxonomy-2026-draft

## Comparative synthesis

| Layer | Demonstrated direction | What remains unproven |
|---|---|---|
| Agent runtime | Guardrails, approvals, hooks, traces | Cross-vendor equivalence and measured reduction in harmful actions |
| Workflow execution | CI-native agents with sandbox and safe-output controls | Whether a specific repository workflow is safe without inspecting its exact policy and run |
| Tool/context access | MCP tools, resources and asynchronous Tasks | Uniform implementation quality, identity and permission semantics |
| Agent-to-agent | A2A open interoperability project | Universal adoption and end-to-end authorization across delegated chains |
| Orchestration | Durable state, pause/resume and human interrupts | Sandbox isolation, egress control and semantic correctness |
| Assurance | NIST identity, threat taxonomy and red-team research | A single complete, universally accepted agent-verification standard |

## Convergence assessment
**ASSESSMENT:** The strongest convergence is around five operational requirements:
1. least-privilege tool permissions and explicit approval boundaries;
2. interoperable tool/context and agent-to-agent protocols;
3. durable state and resumable workflows;
4. traceable runs, provenance and audit logs;
5. adversarial testing, identity controls and independent verification.

**NOT_YET_VERIFIED:** There is no evidence here of one universal agent architecture, a universal identity model, or a standard that proves semantic correctness of agent outputs. Protocol compatibility does not establish truth, safety or business value.

## Implication for WANGA
The current Wix Evidence Auditor blueprint is aligned with these controls at specification level: read-only inputs, no credentials, network egress denied, explicit acceptance tests, unresolved-state preservation and rollback. It remains `draft` / `NOT_CONFIGURED`; the passing blueprint CI validates the specification, not runtime isolation or deployment.

The defensible WANGA differentiator remains a hypothesis: source-linked logical capability packages plus deterministic verification and bounded execution. It must be tested against existing agent registries, audit products and customer workflows before any uniqueness or market-capture claim.
