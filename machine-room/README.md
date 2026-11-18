# WANGA Machine Room

The Machine Room is the repository-managed control plane for external tools,
plugins, MCPs, agents and service connectors.

It does not pretend that a manifest entry is a live connection.

## Responsibilities

1. Maintain the canonical plugin inventory.
2. Define capability and health-check contracts.
3. Record observed connectivity and permission state.
4. Preserve recommendations from bounded agents.
5. Emit a compact bridge snapshot for the WANGA orchestrator.

## Separation

PLUGIN REGISTRY
  describes what a connector is supposed to provide.

PREFLIGHT
  establishes what is actually reachable in the current environment.

ADVISORY
  evaluates which reachable or candidate tool is suitable for the task.

BRIDGE
  transmits only the relevant state to the orchestrator.

EXECUTION
  performs the requested work.

VERIFICATION
  proves what actually happened.

## Security

Never store credentials, API keys, private tokens or private keys in this
directory. Runtime credentials belong in the appropriate secret manager or
GitHub secret/environment mechanism.

## Status rule

A registry record is configuration.
A preflight result is evidence.
A successful operation is execution evidence.
Verification is a separate state.
