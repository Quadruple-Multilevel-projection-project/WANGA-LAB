# Agent convergence and verification — primary-source update

Date: 2026-11-22
Status: VERIFIED_SOURCE_REVIEW / ASSESSMENT
Scope: external implementations and standards work; no WANGA adoption or equivalent capability is claimed.

## 1. OpenAI Agents SDK — traces, handoffs and guardrails
The current Agents SDK documentation describes a trace hierarchy spanning task, agent, turn, model generation, function-tool call, guardrail and handoff spans. This provides observability for what an agent run did and where control moved. The guardrails documentation describes tripwire behavior that halts execution when input, output or tool guardrails fail.

Assessment: tracing improves auditability, but a trace is not proof that the underlying action was authorized, correct or safe. Guardrails are one control layer; route-level authorization and tool-specific policy still matter.

Sources:
- https://openai.github.io/openai-agents-js/guides/tracing/
- https://openai.github.io/openai-agents-python/guardrails/
- https://openai.github.io/openai-agents-python/handoffs/

## 2. NIST — identity and authority for software agents
NIST published the concept paper “Accelerating the Adoption of Software and Artificial Intelligence Agent Identity and Authorization” on 5 February 2026. It frames agent identity, authorization, auditing, non-repudiation and prompt-injection controls as practical adoption issues. NIST's 18 May 2026 summary of responses to its AI-agent security RFI reports broad agreement that agents create novel security concerns and that existing cybersecurity practices need adaptation.

Assessment: this is standards-development and applied-research work, not a completed universal agent identity standard. It supports making agent identity, authority and accountability explicit before granting external tool access.

Sources:
- https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd
- https://www.nist.gov/publications/summary-analysis-responses-request-information-regarding-security-considerations-ai

## 3. A2A — interoperable agent tasks and artifacts
The A2A project's current key-concepts documentation defines Agent Cards for identity/capabilities/authentication metadata, stateful Tasks, Messages, Parts and Artifacts. It documents request/response polling, server-sent-event streaming and push notifications.

Assessment: A2A addresses discovery and task interoperability. It does not by itself prove that an agent is trustworthy, authorized for a particular tenant, sandboxed, or semantically correct. A2A and MCP address different integration layers and should not be treated as substitutes for authorization and execution isolation.

Source:
- https://github.com/a2aproject/A2A/blob/main/docs/topics/key-concepts.md

## 4. LangGraph — durable orchestration and human review
LangGraph documentation shows state-graph workflows with discrete nodes, checkpointing, retries and interrupt/resume behavior. A checkpointer preserves state so a workflow can pause for human input and resume.

Assessment: durable execution and human-in-the-loop are useful orchestration controls. LangGraph is not a sandbox and does not establish network-egress isolation.

Source:
- https://docs.langchain.com/oss/javascript/langgraph/thinking-in-langgraph

## 5. Hugging Face smolagents — code agents and sandbox boundary
The smolagents project documents CodeAgent and ToolCallingAgent patterns and supports external sandbox backends such as Docker, E2B, Modal and Blaxel. Its README explicitly warns that the local Python executor is not a security boundary.

Assessment: code-executing agents need real isolation. A local executor or an orchestration graph must not be described as a sandbox.

Source:
- https://github.com/huggingface/smolagents

## Cross-system comparison
| Layer | Demonstrated implementation | What it establishes | What it does not establish |
|---|---|---|---|
| Run observability | OpenAI Agents SDK tracing | Span-level run/tool/handoff records | Authorization or truth |
| Guardrail enforcement | OpenAI SDK tripwires | Halt behavior on configured guardrail failures | Complete coverage of all actions |
| Agent identity and authority | NIST concept/research program | A recognized standards and implementation problem | A final universal standard |
| Inter-agent interoperability | A2A | Discovery, task state, message/artifact exchange | Tenant authorization or semantic validity |
| Durable orchestration | LangGraph | Checkpoints, interrupts and resumable state | Sandbox isolation |
| Code execution isolation | smolagents with external sandbox backends | Supported sandbox integration options | Automatic safe configuration in every deployment |

## AI231 implications
1. Keep the agent route authorization finding P1 until the unprotected AppDeploy routes and unscoped task/ledger access are remediated and tested.
2. Keep task identity, owner, permissions, provenance, acceptance, rollback and run evidence as explicit fields.
3. Separate orchestration, runtime, sandbox, identity, observability and semantic verification; none substitutes for the others.
4. Use source-linked logic constraints and drift checks as an AI231 differentiator only after their own acceptance tests and independent review.
5. Do not claim external teams have adopted, copied or validated WANGA. The sources establish convergence in engineering concerns, not adoption of this project.
