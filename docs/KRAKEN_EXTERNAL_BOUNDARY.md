# KRAKEN external-model boundary — implementation candidate

## Implemented in this branch
- `engine/sanitization_proxy.py`: fail-closed allowlist for a small set of public task forms; rejects internal markers and structured/code payloads.
- `engine/routing_network.py`: deterministic routing to six named spheres; ambiguity is rejected.
- `engine/kimi_connector.py`: Moonshot-compatible client for `https://api.moonshot.ai/v1`, model `kimi-k3`; requires a proxy-issued request and `LLM_EXTERNAL_API` permission.
- `config/brain.config.yaml` and `plugin_registry.json`: proposed role/plugin permissions and denied internal capabilities.
- `tests/test_kraken_external_boundary.py`: unit tests for fail-closed handling and permission checks.

## Security boundary
This is application-level isolation only. It is **not** a physical air gap. A real deployment must run the connector in a separate process/container, restrict egress to the provider, keep credentials in a secret manager, and prevent direct network access from internal workers. Do not pass internal prompts to the proxy and expect it to safely rewrite them: the current implementation rejects rather than summarizes them.

## Verification status
- Source changes: committed to a feature branch.
- Local test execution: not performed in this GitHub-only workflow.
- Live Moonshot/Kimi API call: not performed; requires credentials and explicit runtime environment.
- 10,000-request stress test: not performed.
- No data-leak-free guarantee is claimed from static unit tests alone.
- The requested 36-box / 126-dimensional hardware configuration remains specified, not physically verified, per `ai-drift-forensics/david-jones-kraken/KRAKEN_CONFIGURATION_V0_1.md`.
