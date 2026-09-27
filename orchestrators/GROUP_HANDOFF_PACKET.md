# WANGA — GROUP HANDOFF / CONSTELLATION CONFIGURATION

## 1. Purpose

This packet is the single handoff reference for every working group.

Each group works on its assigned research/technical domain, but all outputs follow one common contract:

SOURCE → PRIMITIVES → OPERATIONS → RELATIONS → DERIVATION → ABSTRACTION → OUTPUT
                                      ↓
                              DRIFT FORENSICS
                                      ↓
                         EVIDENCE / PROVENANCE / RECEIPT
                                      ↓
                              VERIFICATION

No group may silently convert a representation, hypothesis, simulation, interpretation, or computational model into a physical or verified claim.

---

## 2. Two constellation spaces

### A. 28 Thinking Machines

Definition used by this project:

**28 = 22 letters + 5 final forms + repeated Aleph**

This is the personal Thinking Machine space.

The 28-group orchestrator routes work between the 28 Thinking Machine groups and the common WANGA infrastructure.

Canonical configuration:
- Group registry: `orchestrators/28-groups/groups.json`
- Group instructions: `orchestrators/28-groups/README.md`
- Orchestrator map: `orchestrators/ORCHESTRATOR_MAP.md`

### B. 32 Roots

Definition used by this research record:

**32 = 10 sephirot roots + 22 letter roots**

The 22 letter roots are structured as:
- 3 Mothers
- 7 Doubles
- 12 Simples

The 32-root research record is:
`research/32_shorashim.md`

The 32-root orchestrator routes the root/provenance layer independently from the 28 Thinking Machine layer.

---

## 3. Shared operating rule for every group

Every group must report:

1. INPUT — exact source/input received.
2. PRIMITIVES — names, symbols, terms, fields, or objects extracted.
3. OPERATIONS — exact transformations performed.
4. RELATIONS — relations established between nodes.
5. DERIVATION — how the output follows from prior states.
6. DRIFT — where the representation changes.
7. EVIDENCE — source/evidence references supporting the step.
8. VERIFICATION STATE — one of the permitted states below.
9. RECEIPT — hashes/metadata when an executable transformation is involved.
10. HANDOFF — what the next group is expected to do.

Do not report only the final answer when the task is a drift/reconstruction task.

---

## 4. Verification states

Use these labels exactly:

- VERIFIED
- CONDITIONALLY_VERIFIED
- NOT_YET_VERIFIED
- UNVERIFIED
- REPRESENTATION_ONLY
- SIMULATION_MODEL
- ENGINEERING_ASSUMPTION

Project implementation statuses remain separate:

ARCHITECTURE_SPECIFIED → BUILT → TESTED → REPLAY_VERIFIED → EVIDENCE_VERIFIED → VERIFIED

**SPECIFIED is not VERIFIED.**
**Simulation is not physical reality.**
**A hash proves integrity of data, not semantic truth.**
**Convergence between models is not proof of truth.**

---

## 5. Relay contract

Both orchestrators feed the common relay layer.

Logical path:

28 ORCHESTRATOR ─┐
                  ├→ RELAY → THINKING MACHINE → DERIVATION GRAPH
32 ORCHESTRATOR ─┘                                      ↓
                                                DRIFT FORENSICS
                                                       ↓
                                            EVIDENCE / RECEIPTS
                                                       ↓
                                                     RELAY
                                                       ↓
                                                  ORCHESTRATOR

Message types:
- REQUEST
- QUESTION
- RESULT
- HANDOFF
- VERIFICATION_REQUEST
- STATUS
- ERROR
- ESCALATION

Each message should carry:
- task_id
- message_id
- source
- destination
- context_refs
- evidence_refs
- verification_state

---

## 6. Core Wix sites

### Global Algorithmic G
https://beywolf5.wixsite.com/global-algorithmic-g

### ARK Research & Computing
https://beywolf5.wixsite.com/ark-research-compu

Research:
https://beywolf5.wixsite.com/ark-research-compu/research

Method:
https://beywolf5.wixsite.com/ark-research-compu/research#method

### Operational AI Drift
https://beywolf5.wixsite.com/operational-ai-drift

### International AI Forensic Framework
https://beywolf5.wixsite.com/international-ai-for

### Global Algorithmic Governance Institute
https://beywolf5.wixsite.com/institute-for-global

Research archive:
https://beywolf5.wixsite.com/institute-for-global/research-archive

Technology & Code:
https://beywolf5.wixsite.com/global-algorithmic-g/technology-code

---

## 7. Google Business Profile

Google Business Profile is now connected to the Wix site.

Current connection state verified through Wix:
**VALID**

Connection verified: 2026-09-27.

This means the Wix site has a usable Google Business Profile connection. It does not by itself prove that a particular Google listing is live/verified; listing-level status remains a separate check.

---

## 8. GitHub organization and administration links

### Organization
https://github.com/Quadruple-Multilevel-projection-project

Repositories:
https://github.com/Quadruple-Multilevel-projection-project?tab=repositories

Projects:
https://github.com/Quadruple-Multilevel-projection-project?tab=projects

Branches:
https://github.com/Quadruple-Multilevel-projection-project/branches-

Cyber Department:
https://github.com/Quadruple-Multilevel-projection-project/think-thank-you-of-cyber-Department

WANGA-LAB:
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB

New repository:
https://github.com/new

Organization settings:
https://github.com/settings/organizations

Developer settings:
https://github.com/settings/developers

Packages:
https://github.com/globalworldparty-web?tab=packages

Projects:
https://github.com/globalworldparty-web?tab=projects

Repositories:
https://github.com/globalworldparty-web?tab=repositories

Globalworldparty-web:
https://github.com/globalworldparty-web

---

## 9. WANGA-LAB configuration files

### 28 groups
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/tree/agent/architecture-integration/wanga-ai231-bootstrap/orchestrators/28-groups

28-group registry:
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/agent/architecture-integration/wanga-ai231-bootstrap/orchestrators/28-groups/groups.json

28-group instructions:
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/agent/architecture-integration/wanga-ai231-bootstrap/orchestrators/28-groups/README.md

### 32 roots
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/tree/agent/architecture-integration/wanga-ai231-bootstrap/orchestrators/32-roots

32-root registry:
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/agent/architecture-integration/wanga-ai231-bootstrap/orchestrators/32-roots/roots.json

32-root instructions:
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/agent/architecture-integration/wanga-ai231-bootstrap/orchestrators/32-roots/README.md

### Unified map
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/agent/architecture-integration/wanga-ai231-bootstrap/orchestrators/ORCHESTRATOR_MAP.md

### External systems configuration
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/agent/architecture-integration/wanga-ai231-bootstrap/configs/external-systems.yaml

### 32 roots research record
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/agent/architecture-integration/wanga-ai231-bootstrap/research/32_shorashim.md

### AI Drift Forensics website copy
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/agent/architecture-integration/wanga-ai231-bootstrap/business/DRIFT_FORENSICS_WEBSITE_COPY.md

---

## 10. Drift Forensics research/business sites

ARK Research & Computing:
https://beywolf5.wixsite.com/ark-research-compu/research

Operational AI Drift Engine:
https://beywolf5.wixsite.com/operational-ai-drift

International AI Forensic Framework:
https://beywolf5.wixsite.com/international-ai-for

Global Algorithmic Governance Institute:
https://beywolf5.wixsite.com/institute-for-global

---

## 11. GitHub group operating procedure

### On task receipt
The group orchestrator creates/receives a task_id and records:
- source
- task
- expected output
- relevant group
- upstream context
- verification requirement

### During work
The group records the derivation path rather than only the conclusion.

### At handoff
Return:
- result
- derivation graph/reference
- evidence references
- verification state
- unresolved questions
- next destination

### On detected drift
Do not correct silently.

Record:
- BEFORE
- AFTER
- CHANGE_POINT
- AFFECTED_NODE
- AFFECTED_RELATION
- DRIFT_CLASS
- SOURCE_REF
- EVIDENCE_REF

Drift classes:
- DEFINITION_DRIFT
- PREMISE_DRIFT
- CRITERION_DRIFT
- RELATION_DRIFT
- OPERATION_DRIFT
- REFERENCE_DRIFT
- ABSTRACTION_DRIFT
- CONTEXT_DRIFT

---

## 12. First execution target

The first common test is deterministic replay:

SOURCE
→ EXTRACT
→ REPRESENT
→ DERIVE
→ RECONSTRUCT

Then:

same SOURCE + same TASK → two agents → two derivation graphs → DRIFT COMPARISON

The system must answer:

**WHAT INPUT?**
**WHAT PRIMITIVES?**
**WHAT OPERATIONS?**
**HOW WAS THE CONCEPT DERIVED?**
**WHERE DID THE REPRESENTATION CHANGE?**
**WHAT EVIDENCE SUPPORTS EACH STEP?**

---

## 13. Domain boundary

The architecture must keep these domains separate:

- HISTORICAL/TEXTUAL SOURCE
- STRUCTURAL EXTRACTION
- INTERPRETIVE MAPPING
- COMPUTATIONAL MODEL
- SIMULATION MODEL
- ENGINEERING ASSUMPTION
- PHYSICAL IMPLEMENTATION

A symbol, letter, name, model, graph, or representation is not automatically the physical structure it refers to.

A computational mapping is not automatically a physical mechanism.

An untraceable derivation is **not automatically false**; it is a provenance/reconstruction problem until evidence establishes more.

---

## 14. Canonical architecture

WANGA OS
→ Global Work Manager
→ Model Fabric
→ Digital Model Agents
→ Providers / Runtimes
→ Evidence / Provenance
→ Drift Forensics / Verification
→ Rational Logic ↔ Neural Thinking Machine
→ Work Memory

Lateral:
Perspective Layer

External/public:
GitHub = source of truth
Wix = publication/business layer
Google Business Profile = business discovery/presence layer

---

## 15. Rule for every group

**Do the assigned work.**
**Do not invent missing evidence.**
**Do not collapse distinct domains.**
**Do not promote status without the required test/evidence.**
**Do not overwrite another group's provenance.**
**Return a machine-readable handoff.**
**Route the handoff through the appropriate orchestrator.**
