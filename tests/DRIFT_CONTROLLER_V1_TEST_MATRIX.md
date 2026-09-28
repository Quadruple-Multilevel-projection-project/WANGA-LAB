# Drift Controller V1 — Test Matrix

## Contract tests

1. REQUEST from Research to Document preserves task_id and message_id.
2. RESPONSE returns to the requester through the Relay.
3. Capability routing selects a provider from declared capabilities.
4. Missing capability returns UNAVAILABLE.
5. Missing authorized target returns BLOCKED.
6. Context transfer excludes unrelated global memory.
7. Evidence references survive relay.
8. Disagreement is preserved rather than overwritten.
9. VERIFIED cannot be emitted by the Relay.
10. Human approval cannot be synthesized by the Relay.

## Webhook tests

1. Missing/invalid authentication is rejected.
2. Malformed event is rejected before routing.
3. Valid event becomes a normalized task envelope.
4. Webhook cannot bypass Intent Gate.
5. Webhook cannot directly publish to GitHub.
6. Webhook cannot set verification state to VERIFIED.
7. Secrets are never persisted in repository configuration.

## NTM integration tests

1. NTM receives bounded state rather than global state.
2. Drift Controller preserves NTM return-envelope fields.
3. 28-mode taxonomy remains distinct from 32-root structure.
4. 52-configuration taxonomy remains pending until canonical history is recovered.
