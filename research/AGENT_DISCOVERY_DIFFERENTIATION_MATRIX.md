# Agent Discovery Market Evidence Matrix

Status: RESEARCH / NOT_YET_VERIFIED

## Observed overlap
- ARD v0.91 (Proposal) defines federated discovery for MCP, A2A, skills and APIs, with JSON-LD extension points and trust metadata.
- Kong MCP Registry covers enterprise discovery, governance and observability for MCP tools.
- AWS Agent Toolkit packages skills/plugins and provides guarded MCP access and observability.
- Neuronto ARD Index describes live federated discovery and introspection of MCP `tools/list` with input schemas.
- SkillIndex supports discovery and comparison by use case, compatibility, setup, permissions and source details.

## WANGA differentiation hypothesis
Registry/discovery alone is not a differentiator. Candidate differentiation is source-backed logic primitives plus behavioral contracts, provenance-separated evidence, version/revocation, and tested bundle composition. This remains a hypothesis, not a uniqueness claim.

## Next evidence
1. Compare WANGA schema against ARD v0.91 entry schema.
2. Add schema and reference-integrity tests.
3. Run end-to-end bundle tests before computing verified-coverage optimization.
4. Record a negative finding if no distinct capability survives comparison.

## Sources
- https://github.com/ards-project/ard-spec/blob/main/spec/ard.md
- https://konghq.com/company/press-room/press-release/kong-introduces-mcp-registry
- https://aws.amazon.com/about-aws/whats-new/2026/05/agent-toolkit/
- https://github.com/neuronto/agentic-resource-discovery
- https://skillindex.io/
