# AI231 Agent Flow Control — Product Concept and Collaboration Brief

**Status:** PROPOSED PRODUCT CONCEPT — NOT A DEPLOYED SERVICE  
**Date:** 2026-11-21  
**Project context:** AI231 / WANGA agent coordination  
**Publication purpose:** Invite technical collaborators, infrastructure partners, and design partners to help validate a safer, more efficient operating layer for multi-agent systems.

## The problem

Multi-agent systems can fail operationally even when individual agents are capable. Common failure modes include uncontrolled parallel work, duplicated tasks, overloaded agents, unbounded message traffic, unclear ownership, lost handoffs, repeated retries, and outputs that are not independently verified.

The problem addressed here is **flow control across agent teams**: deciding what work is released, to whom, in what size, at what rate, with what dependencies, and under what verification and approval conditions.

## The proposed approach

AI231 is designing a coordination layer that treats agents as workers in bounded teams rather than as an uncontrolled swarm.

### 1. Shared team inboxes — not one mailbox per agent

A mailbox is a communication endpoint for a team or workgroup. It is not itself an agent identity and is not the authoritative task database.

A proposed initial configuration is one team inbox serving a small group (for example, up to 10 agents), with:
- a unique identity and permissions for each agent;
- explicit task ownership and correlation IDs;
- separate inbound task, status, handoff, and exception message types;
- deduplication and idempotency controls;
- a durable task ledger outside email;
- configurable group size based on measured throughput and provider limits.

The number 10 is an initial design hypothesis, not a tested capacity limit. Group sizes must be load-tested before larger deployments.

### 2. Pulse-based workload release

The orchestrator does not send an entire day's workload to every agent at once. It releases bounded work packets according to capacity and dependencies.

A pulse may be:
- scheduled (for example, a half-day planning/release cycle);
- event-driven when an agent completes a task;
- triggered by a dependency becoming ready;
- triggered by an exception or human decision.

Each pulse contains a bounded set of tasks, priorities, deadlines, acceptance criteria, context references, and allowed tools. Agents report completion, blocked status, or a request for clarification. The orchestrator verifies the handoff and only then releases the next work packet.

This is intended to prevent work overload, uncontrolled concurrency, duplicate execution, and cascading failures. The pulse interval and batch size must be adaptive and evidence-based; a fixed half-day interval is only one possible operating mode.

### 3. Cross-platform communication adapters

The planned service is platform-neutral. Potential adapters include:
- Google Workspace / Gmail and Google Cloud;
- Microsoft 365 / Outlook, Teams, and Azure;
- GitHub for code changes, pull requests, CI evidence, and review;
- AgentMail or other email infrastructure;
- additional agent runtimes and enterprise systems through explicit connectors.

No integration is claimed to be active merely because a platform is listed. Each adapter requires authentication, least-privilege scopes, rate-limit handling, security review, and acceptance tests. Email is a notification and handoff channel, not a substitute for a durable queue or workflow state store.

### 4. Independent verification and governance

The proposed control plane records:
- agent identity, group, runtime, and permission scope;
- task ID, owner, parent task, dependencies, and state;
- dispatch and completion timestamps;
- retry count, timeout, and failure reason;
- evidence links and exact commit/run identifiers for software work;
- verification result and approver;
- immutable or tamper-evident audit events where supported.

An agent must not approve its own code or its own workflow change. Production changes, privileged network operations, external communications, spending, and irreversible actions require explicit authorization.

### 5. Proposed operating cycle

1. Receive a goal and define acceptance criteria.
2. Decompose the goal into bounded tasks.
3. Assign tasks to a qualified team and agent.
4. Check capacity, dependencies, permissions, and rate limits.
5. Release one bounded work packet (pulse).
6. Collect status, artifacts, and handoffs.
7. Independently verify outputs.
8. Retry, reassign, or escalate failures under policy.
9. Release the next pulse only when its prerequisites are satisfied.
10. Close the task with evidence and an audit record.

## Initial target workflows

- Software engineering: issue decomposition, isolated branches, code review, CI repair, and release preparation.
- IT and network operations: read-only diagnostics, alert triage, maintenance planning, and approval-gated remediation.
- Research and knowledge operations: parallel source collection, evidence comparison, and synthesis.
- Cross-platform enterprise workflows: controlled handoffs between agents operating in different provider environments.

## Architecture principles

- **One canonical task ledger:** no competing project queues.
- **Mailbox != agent:** mailboxes represent teams or channels; agent identities and permissions are separate.
- **Bounded concurrency:** limits are enforced centrally and tuned from measured load.
- **Small work packets:** agents receive only work they can safely process.
- **Event-driven plus scheduled pulses:** completion can release the next task; periodic pulses provide reconciliation and planning.
- **Idempotent dispatch:** duplicate messages must not create duplicate work.
- **Durable handoffs:** every handoff has a persistent record and explicit receiver.
- **Provider neutrality:** model inference and communication adapters must not create a single-vendor critical dependency.
- **Independent verification:** execution and approval are separated.
- **Human authority:** sensitive or irreversible operations remain approval-gated.

## What is and is not established

This document describes a product being designed. It does not claim:
- a deployed 20,000-agent network;
- a verified capacity of 10 agents per inbox or any other fixed ratio;
- production integrations with Google, Microsoft, AgentMail, or GitHub;
- measured savings, revenue, customer adoption, or reliability improvements;
- banking-grade certification, security assurance, or regulatory approval.

The next engineering proof points are a working durable queue, team inbox adapter, bounded dispatcher, idempotency and retry tests, agent identity/permission enforcement, audit log, and an end-to-end demonstration across at least two independently operated platforms.

## Collaboration invitation

We are looking for infrastructure, agent-runtime, workflow-orchestration, security, and enterprise-integration collaborators to help validate the design and build a measurable proof of concept.

Potential collaboration areas:
- durable queues and workflow state;
- group mailbox and messaging adapters;
- Google and Microsoft integration;
- agent runtime isolation and least-privilege access;
- adaptive batch sizing and back-pressure;
- verification, observability, and audit evidence;
- pilot design for software engineering and IT operations.

**Contact and partnership terms are to be agreed separately.** This publication is an invitation to technical discussion, not an offer of securities, a binding commercial offer, or a claim of an existing partnership.

## Preliminary value assessment — not a valuation

The concept sits in the agent orchestration and workflow-control category. Public market research describes this as a growing category, but broad market-size forecasts do not establish the value of this specific project.

At the current concept/design stage, with no verified production deployment, customer contracts, recurring revenue, or independently measured performance, a defensible company valuation cannot yet be calculated. Any early-stage figure would be a negotiation hypothesis, not an appraisal.

A valuation becomes more supportable after:
1. a working proof of concept;
2. independent load and failure-recovery tests;
3. verified cross-platform integrations;
4. security and permission testing;
5. paid design partners or signed pilot commitments;
6. measured unit economics and repeatable customer demand.

Do not use market-size forecasts as the project's revenue, valuation, or expected market share.

## References for market context

- NTT DATA, *Technology Foresight 2026* — reports a Technavio estimate for multi-agent orchestration of USD 0.63B in 2024 and USD 1.85B in 2029 (forecast, not audited project revenue): https://dam.nttdata.com/api/public/content/6fb4f3dc10a04e019c782c36ec056738?v=89995167
- Mordor Intelligence, *Multi-Agent Systems Market* — market estimate and forecast, methodology and scope are those of the publisher: https://www.mordorintelligence.com/industry-reports/multi-agent-systems-market

These third-party market estimates differ in scope and methodology. They are contextual references only.
