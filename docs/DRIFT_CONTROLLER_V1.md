# Drift Controller Core V1

Status: ARCHITECTURE_SPECIFIED / PROTOTYPE_PENDING

## Purpose

Unify WANGA tool/plugin orchestration around the Neural Thinking Machine and Drift Forensics without granting any plugin or relay autonomous authority.

Core path:

INTAKE
-> INTENT GATE
-> ROUTE REGISTRY
-> RELAY
-> SPECIALIST / CODEX EXECUTION
-> EVIDENCE
-> DRIFT CHECK
-> VERIFICATION GATE
-> RETURN / AUTHORIZED ACTION

## Control-plane components

- NTM Orchestrator: high-level reasoning and bounded orchestration.
- Drift Controller: detects configuration, representation, routing, semantic and structural drift across execution.
- Relay Agent: transport/context layer between groups.
- Capability Registry: maps task requirements to available plugins/agents.
- Project Registry: maps execution to an authorized project/repository.
- Evidence Gate: preserves provenance and verification state.
- Codex Coordinator: bounded parallel work in one shared checkout.
- Codex Process Jobs: durable local execution for long-running work.
- Codex Advisor: read-only material architecture consultation.
- GitHub: source/publication surface.
- Airtable: operational routing/configuration registry.
- Notion: decisions/checkpoints/knowledge.
- ProductOS: product specification and project workflow.
- Wayfinder: decision mapping/planning.
- Mavixx Forge: implementation/quality workflow.
- NVIDIA Skills: NVIDIA/GPU-specific capability provider.
- Supabase: backend/database capability provider.
- Empire LLM: quarantined external-model review/handoff.

## 52-configuration boundary

The historical 52-configuration set is a configuration taxonomy, not 52 independent models.

Until the canonical 52 entries are recovered from WANGA history, the registry must represent them as:

CONFIGURATION_PENDING

Do not invent missing configuration names.

The NTM 28-mode taxonomy and the 32-root structure remain separate architectural layers. They must not be flattened into a single model count.

## Relay contract

Every inter-group/system message uses:

message_id
task_id
parent_task_id
source_agent
source_group
destination_agent
destination_group
message_type
priority
payload
context_refs
evidence_refs
verification_state
requires_response
requires_human_approval
timestamp

Supported message types:

REQUEST
RESPONSE
QUESTION
RESULT
HANDOFF
STATUS
ERROR
ESCALATION
VERIFICATION_REQUEST
APPROVAL_REQUEST

## Routing rule

Route by capability and authorized target, not by fixed agent identity.

Required resolution:

TASK
-> CAPABILITY
-> AVAILABLE PROVIDER
-> AUTHORIZED PROJECT
-> EXECUTION MODE
-> VERIFICATION GATE

If any required element is unavailable, return BLOCKED/UNAVAILABLE. Never silently substitute an unrelated provider or target.

## Context boundary

Do not broadcast global memory.

Relay only:

task context
+ required data
+ relevant evidence
+ relevant prior messages

## Drift classes

At minimum:

LETTER_DRIFT
POSITION_DRIFT
SEQUENCE_DRIFT
WORD_DRIFT
SEMANTIC_DRIFT
STRUCTURAL_DRIFT
VERSION_DIRECTION_DRIFT
ROUTING_DRIFT
CONFIGURATION_DRIFT
CAPABILITY_DRIFT
PROVENANCE_DRIFT
INTENT_RECOVERY_CANDIDATE
UNAVAILABLE
REVIEW

## Evidence states

HYPOTHETICAL
ONTOLOGICAL_MODEL
SIMULATION_MODEL
ENGINEERING_ASSUMPTION
SPECIFIED
PROTOTYPED
TESTED
VERIFIED
NOT_YET_VERIFIED
UNVERIFIED

No SPECIFIED -> VERIFIED promotion without the appropriate test/evidence gate.

## Webhook boundary

A webhook may be used as an event transport into the controller.

It must NOT:

- contain secrets in committed configuration;
- bypass the Intent Gate;
- bypass capability routing;
- directly authorize external side effects;
- mark results VERIFIED;
- mutate GitHub or other project state without the normal execution/verification path.

Expected webhook path:

EXTERNAL EVENT
-> WEBHOOK INGRESS
-> AUTHENTICATE / VALIDATE
-> NORMALIZE EVENT
-> TASK ENVELOPE
-> DRIFT CONTROLLER
-> ROUTER
-> RELAY / EXECUTION
-> EVIDENCE
-> VERIFICATION
-> RETURN

Webhook URL/token values remain external secrets.

## Human approval boundary

requires_human_approval=true for external communication, publication, irreversible actions, commitments, or other actions explicitly designated by project policy.

The relay can carry an approval request. It cannot manufacture approval.

## Initial prototype

Start with:

Research Group
<-> Relay
<-> Document Group

Then add:

Browser
Presentation
Verification

Only after message identity, context isolation, receipts and failure behavior pass tests.

## Success criteria

- deterministic capability routing;
- stable task/message identity;
- bounded context transfer;
- preserved disagreement;
- provenance on returned results;
- explicit verification state;
- fail-closed unavailable routes;
- human-approval boundary respected;
- GitHub publication requires an authorized target;
- webhook events cannot bypass the control plane.

## Relationship to existing NTM

The existing NTM architecture remains authoritative for high-level reasoning flow:

OBSERVE -> REPRESENT -> COMPARE -> REASON -> DETECT CONFLICT -> PROPOSE REPAIR -> VERIFY -> RETURN

The Drift Controller adds the cross-system control plane around that process; it does not replace the NTM.
