# Deployment Architecture — RACI

**Status:** SPECIFIED; assignments require confirmation by the project owner before operational escalation.

| Work item | L0 Orchestrator | L1 Verification | L2–L4 Execution | Ontology Editor (S7) | DSA |
|---|---|---|---|---|---|
| Stop/rollback decision | A | C | I | I | R |
| Schema validation | I | A/R | C | C | C |
| Source sentence extraction | I | C | I | A/R | I |
| Chapter 13 lock | A | C | I | R | I |
| Gate 14 source-reference lock | A | R | I | R | C |
| Export blueprint and bundle | I | C | I | I | A/R |
| Secret screening and SBOM | I | C | I | I | A/R |
| CI evidence and release report | A | R | C | C | R |
| Wix briefing publication | A | C | I | C | R |

**Legend:** R = Responsible; A = Accountable; C = Consulted; I = Informed.  
This table is a proposed responsibility contract, not proof that these roles are staffed or that the controls are enforced.
