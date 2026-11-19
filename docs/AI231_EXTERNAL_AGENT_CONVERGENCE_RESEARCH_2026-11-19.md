# AI231 external convergence research — 2026-11-19
Repository: `Quadruple-Multilevel-projection-project/WANGA-LAB`
Scope: agent orchestration, multi-agent communication, verification, sandboxing, evaluation and commercial alternatives.
Evidence rule: official specifications, SDK documentation and runnable examples are treated as implementation evidence at the documented API level—not proof of production performance or of an external system having the same architecture as AI231.

## 1. Findings

### A. Bounded agents, orchestration and guardrails are becoming explicit layers

**VERIFIED — OpenAI Agents SDK documentation.** The SDK separates an `Agent` definition (instructions, tools, handoffs, guardrails and structured output) from the `Runner` that manages turns, tool calls, handoffs and sessions. Tool guardrails can block or replace calls before execution and validate results after execution. Its testing utilities provide deterministic, in-memory tests for orchestration, tools, handoffs, guardrails and sessions without making model or sandbox-provider calls. The `SandboxAgent` path adds a manifest-defined isolated workspace and sandbox capabilities.

**Implication for AI231 — ASSESSMENT.** Keep the project’s logical policy/contract separate from the execution adapter. A blueprint is not a running agent. A runner is not automatically a security sandbox. Use deterministic tests for contract behavior, then separate integration tests for model, network and sandbox behavior.

### B. Durable orchestration is a separate concern from execution isolation

**VERIFIED — LangGraph documentation.** The documented graph pattern decomposes work into nodes, persists state through a checkpointer, and uses `interrupt()` to pause for human input and resume from saved state. The example demonstrates retries and inspection at node boundaries.

**Implication for AI231 — ASSESSMENT.** LangGraph can provide stateful orchestration and resumability. It does not, by itself, prove workspace isolation, least-privilege permissions or network-egress control. A separate sandbox/runtime boundary and per-agent acceptance evidence remain necessary.

### C. Agent-to-agent communication has a task/artifact contract

**VERIFIED — A2A Protocol v1.0.1 specification.** A2A defines stateful tasks, context IDs, task status, messages, artifacts and streaming status/artifact updates. It distinguishes task communication from output artifacts and defines terminal states such as completed, failed, canceled and rejected.

**Implication for AI231 — ASSESSMENT.** A2A is a candidate interoperability layer for exchanging bounded tasks and evidence artifacts between independently operated agents. It is not an agent runtime, a reasoning model, a ledger or a sandbox. Task ownership, authorization, artifact provenance and cancellation policy still belong to the implementation.

### D. Tool/resource interoperability and authorization must be enforced at the transport boundary

**VERIFIED — MCP documentation.** The MCP TypeScript SDK documents tools, resources, prompts and Streamable HTTP transport. The current MCP roadmap/specification work describes stronger authorization and agentic messaging primitives. The authorization guides describe the HTTP server as a resource server that validates bearer tokens and scopes; the server does not issue user tokens.

**Implication for AI231 — ASSESSMENT.** MCP is suitable for exposing narrowly scoped tools/resources to agents. It does not replace task orchestration or the application’s own authorization checks. A tool being listed is not permission to execute it; server-side identity, scope and audit controls remain mandatory.

### E. Evaluation is a product requirement, not a final polish step

**VERIFIED — Promptfoo/OpenAI guide.** The guide shows test cases and assertions for comparing prompts/models and red-teaming applications. It explicitly notes that model-backed evaluations incur API charges and that a passing assertion checks a specific condition, not overall quality.

**Implication for AI231 — ASSESSMENT.** Use fixed test cases, negative cases and adversarial probes; keep the assertions stable across revisions; record cost and latency when model calls are approved. Do not use a green CI run as evidence of semantic correctness beyond the tests actually executed.

## 2. Comparative matrix

| System | What its official sources demonstrate | What it does not prove by itself | AI231 use candidate |
|---|---|---|---|
| OpenAI Agents SDK | Agent/Runner loop, tool handoffs, input/output guardrails, structured outputs, deterministic test utilities, sandbox-agent interface | Production safety of a particular app; no automatic proof that every tool or handoff is isolated | Bounded agent execution, guardrails and deterministic contract tests |
| LangGraph | Explicit state graph, node-level work, checkpoint persistence, interrupt/resume and retry patterns | Sandbox isolation, network-egress restriction or least privilege | Durable supervisor/workflow state and human-review pauses |
| A2A v1.0.1 | Cross-agent task lifecycle, context, artifacts and streaming updates | Runtime execution, trust, identity or sandbox | Interoperability between independently hosted agents |
| MCP | Standard tools/resources/prompts and HTTP authorization patterns | Business workflow orchestration, agent identity policy or semantic verification | Least-privilege tool interface and resource access |
| Promptfoo | Repeatable test cases, assertions, model/prompt comparison and red-team probes | General truth or correctness outside the selected assertions | Fixed regression suite for agent behavior |
| Semrush Site Audit | Crawl-based technical SEO checks, severity-ranked findings, broken-link/canonicalization and AI-crawler visibility reporting | Logic-source provenance, AI-agent runtime safety or project-specific claim truth | Existing alternative for generic technical SEO audits |

## 3. Demonstrated versus announced

- The OpenAI SDK pages include concrete API definitions and runnable examples, plus deterministic testing recipes. This is stronger than an announcement, but remains SDK-level evidence.
- LangGraph’s documentation includes a runnable graph/checkpointer/interrupt pattern. It demonstrates a workflow mechanism, not an isolated execution environment.
- A2A v1.0.1 is a published protocol specification with task and artifact schemas. A protocol specification does not demonstrate that a given deployment implements it correctly.
- MCP’s current documentation describes concrete transport and authorization mechanisms. The application must still configure and test them.
- Vendor feature pages for Semrush describe a commercial site-audit product. This is evidence of a real market alternative category, not evidence that AI231 has demand or a competitive advantage.
- No source reviewed establishes that an external team has reproduced AI231’s 231-gate architecture or the user’s specific logic-processor design. No such convergence claim is made.

## 4. AI231 state comparison

**VERIFIED**
- The deployed Agent Foundry app `ai231-agent-foundry-35gumn` is marked `ready` by AppDeploy.
- Its backend source contains seven role profiles and an `ai.run()` execution path.
- The app source does not provide accessible successful invocation logs for each role, isolation evidence or network-egress controls.
- Three general routes lack `requireAuth()` and use shared task/ledger tables; see `docs/AGENT_FOUNDRY_SECURITY_REVIEW_2026-11-19.md`.

**ASSESSMENT**
- The strongest immediate convergence opportunity is not to copy a framework wholesale. It is to combine: (1) explicit bounded-agent contracts, (2) durable state and human interrupts, (3) task/artifact interoperability, (4) least-privilege tool authorization, and (5) deterministic evaluation.
- The Agent Foundry security gap is a release blocker before paid customer data or any credit workflow is used.

**NOT YET VERIFIED**
- A secure, isolated, end-to-end AI231 agent run.
- Runtime acceptance of all seven Agent Foundry roles.
- A2A or MCP integration in the AI231 application.
- Any measurable customer demand, conversion or revenue.

## 5. Commercial alternatives and positioning

**VERIFIED market alternatives:** Semrush Site Audit provides a mature technical-site crawler and severity-ranked SEO findings; Promptfoo provides repeatable LLM evaluation and red-team workflows. These products cover important portions of a generic website/AI audit.

**HYPOTHESIS — differentiated AI231 wedge:** a narrow evidence-backed audit that combines:
1. public-page and navigation checks;
2. source-linked consistency of technical and AI capability claims;
3. terminology and cross-page contradiction detection;
4. runtime-status and authorization-claim verification for agent workbenches; and
5. reversible remediation drafts with before/after evidence.

This is not yet a validated advantage. It must be tested against existing SEO audit, QA, accessibility and LLM-evaluation tools with real buyers. Do not compete on generic crawl volume or claim superior accuracy without benchmark evidence.

## 6. Next experiments

1. Fix the Agent Foundry API authorization/data-isolation gap before exposing any customer or confidential data.
2. Keep the new Robotics Site Auditor blueprint in `draft` until its own deterministic tests, runtime isolation and invocation evidence exist.
3. Add a fixed AI-claim/logic-consistency regression suite; do not call a model during CI unless the user authorizes the cost.
4. Compare the audit output against a baseline from an existing site-audit tool and a human reviewer on the same pages.
5. Run one paid pilot only after a buyer, budget authority, fixed scope, delivery-cost measurement and price are evidenced.

## Sources (official / primary)

- OpenAI Agents SDK — Agents: https://openai.github.io/openai-agents-python/agents/
- OpenAI Agents SDK — Tool guardrails: https://openai.github.io/openai-agents-python/guardrails/
- OpenAI Agents SDK — Testing: https://openai.github.io/openai-agents-python/testing/
- OpenAI Agents SDK — Sandbox concepts: https://openai.github.io/openai-agents-python/sandbox/guide/
- LangGraph — Thinking in LangGraph: https://docs.langchain.com/oss/javascript/langgraph/thinking-in-langgraph
- A2A Protocol v1.0.1 — Specification: https://a2a-protocol.org/v1.0.1/specification/
- MCP TypeScript SDK — Official overview: https://ts.sdk.modelcontextprotocol.io/index.html
- MCP Python SDK — Authorization: https://py.sdk.modelcontextprotocol.io/run/authorization/
- MCP — 2026-07-28 release candidate and authorization changes: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
- Promptfoo — OpenAI evaluation guide: https://developers.openai.com/api/docs/guides/promptfoo-codex
- Semrush — Site Audit technical checks: https://www.semrush.com/kb/31-site-audit

Accessed: 2026-11-19. The source material documents product capabilities and protocol semantics; it does not establish AI231 performance, external replication or market demand.
