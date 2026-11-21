# WANGA Ministry of Interior — Global Family & Architecture Map

Status: SPECIFIED / BUILDING

## Purpose

This registry is the central structural map for the WANGA "Ministry of Interior" layer.

It treats GitHub as an external architecture substrate and Vitruvius as the mapping layer. The objective is to reconstruct architecture as family trees rather than as a flat repository list.

## Core model

WANGA
→ Ministry of Interior / Internal Registry
→ Office
→ Architecture Family
→ Subfamily
→ Component
→ Child / Descendant
→ Branch / Repository Evidence
→ Vitruvius Node
→ Global Architecture Graph

The registry is structural. It does not imply external institutional authority over the mapped organizations or repositories.

## Existing architecture maps incorporated

### Global registries
- ARCHITECTURE_REGISTRY.json
- GLOBAL_ARCHITECTURE_REGISTRY.md
- ARCHITECTURE_ROADMAP.md
- RESEARCH_ARCHITECTURE_MAP.md
- docs/ARCHITECTURE/REPOSITORY_ATLAS_2026-09-19.json
- docs/ARCHITECTURE/CORPUS_INTEGRATION_REGISTRY.md
- docs/ARCHITECTURE/ARCHITECTURE_FAMILY_LINEAGE.md
- docs/ARCHITECTURE/ARCHITECTURE_TO_RESEARCH_MATRIX.md
- docs/ARCHITECTURE/WANGA_LINEAGE_SYSTEM.md
- docs/ARCHITECTURE/WANGA_LINEAGE_TREE.md
- docs/ARCHITECTURE/DYNAMIC_ARCHITECTURE_GENERATION.md
- docs/BRANCH_ARCHITECTURE_REGISTRY.md
- docs/ARCHITECTURE_INTEGRATION_INDEX.md

### Vitruvius / discovery
- vitruvius/MODEL_BRIDGE.md
- vitruvius/VITRUVIUS_INDEX_SCHEMA_V1.json
- vitruvius/RESEARCH_DISCOVERY_SOURCES_V1.yml
- scripts/vitruvius_automation_engine.py
- scripts/github_architecture_scout.py
- scripts/architecture_builder.py
- .github/workflows/vitruvius-research-index.yml
- .github/workflows/repository-architecture-audit.yml

### Governance / institutional architecture
- global-algorithmic-governance/FOUNDATION_ARCHITECTURE.md
- global-algorithmic-governance/NETWORK_MAP.md
- global-algorithmic-governance/DEPARTMENT_REGISTRY.md
- global-algorithmic-governance/CONTROL_PLANE.md
- global-algorithmic-governance/EXISTING_ASSETS_INDEX.md
- ai-drift-forensics/INSTITUTIONAL_ARCHITECTURE.md
- ai-drift-forensics/global-algorithmic-governance-institute/PROGRAM_ARCHITECTURE_V1.md

### Drift / evidence architecture
- ai-drift-forensics/global-drift-network/ARCHITECTURE.md
- ai-drift-forensics/global-drift-network/ARCHITECTURE_MAP.md
- ai-drift-forensics/global-drift-network/MASTER_ARCHITECTURE_REGISTRY.md
- ai-drift-forensics/CASE_ENGINE.md
- ai-drift-forensics/VERIFICATION_PROTOCOL.md
- ai-drift-forensics/FORENSIC_CARD_SCHEMA.md

### Neural / research architecture
- wanga-research-groups/neural-thinking-machine/NEURAL_OS_ARCHITECTURE_V1.md
- wanga-research-groups/neural-thinking-machine/NTM_ORCHESTRATOR_V1.md
- wanga-research-groups/neural-thinking-machine/ORCHESTRATION_MODEL_V1.md
- ai-drift-forensics/global-drift-network/neural-network-research-core/WANGA_OS_ARCHITECTURE_V1.md
- ai-drift-forensics/global-drift-network/neural-network-research-core/RESEARCH_PROTOCOL_V1.md
- docs/MODEL_AGENT_ARCHITECTURE_V1.md

### Publication / external interface architecture
- docs/WIX_ARCHITECTURE_REGISTRY.md
- docs/WIX_ARCHITECTURE_SNAPSHOT.json
- publication-network/WORDPRESS_FLEET_ARCHITECTURE.md

## Family-tree rules

1. Every mapped node must have a parent or explicit root classification.
2. Repository identity is evidence; it is not automatically an architectural relationship.
3. A branch is not automatically a family. Branches are implementation/evidence locations.
4. Family and subfamily labels require evidence from repository structure, documentation, code, metadata, or explicit registry records.
5. Unknown ancestry remains UNKNOWN.
6. Vitruvius may propose mappings; verification determines whether they are accepted.
7. External organizations, institutions, researchers, companies and governments are mapped as external architecture nodes only; mapping does not imply partnership, ownership, endorsement or authority.

## Initial capacity target

The structural target is:

15 Offices × 1,500 branch/routing positions per Office = 22,500 initial structural positions.

This is a capacity target, not a claim that 22,500 Git branches currently exist.

Atomic decomposition is intentionally a later layer:

Office → Branch → Family → Subfamily → Component → Atomic Node

The atomic layer can therefore grow beyond the initial 22,500-position structural target.

## Accuracy layer

The main engineering objective is accuracy, not manual branch creation.

GitHub supplies:
- repository metadata
- repository trees
- files and code
- branches
- commits
- Git objects

Vitruvius supplies:
- family detection
- hierarchy reconstruction
- cross-repository mapping
- lineage hypotheses
- architecture graph construction

Evidence / Verification supplies:
- provenance
- confidence
- reproducibility
- acceptance or rejection of mappings

No mapping should be promoted from discovered to verified merely because it looks plausible.

## Operational direction

The intended future pipeline is:

GitHub discovery
→ normalize
→ classify
→ family reconstruction
→ Office routing
→ Vitruvius graph
→ evidence capture
→ verification
→ registry update

The registry should expand from evidence and architecture discovery rather than from arbitrary branch-count targets.

## Boundary

The Ministry of Interior layer is an internal WANGA architectural registry concept. It is not a real government ministry and does not create legal, regulatory, financial, organizational or jurisdictional authority over external entities.
