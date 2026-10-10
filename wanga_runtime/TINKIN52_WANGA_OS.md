# Tinkin-52 inside WANGA OS

Tinkin is registered as an experimental compute runtime inside the WANGA Compute Fabric.

## Runtime topology
- 52 nested networks
- 4 layers
- 13 networks per layer
- 3 Galgal wheels per network
- 11 gates per wheel
- 33 gates per network
- 66 letter endpoints per network
- 6 Drift axes
- C0 global coordinator

Totals:
- 156 wheels
- 1,716 gates
- 3,432 letter endpoints

## Execution model
WANGA OS boot contract:
BOOT → LOAD CONFIG → REGISTER METHODS → INITIALIZE SENSORS → CREATE RUN → COLLECT OBSERVATIONS → VALIDATE INTEGRITY → ENABLE ANALYSIS

The Tinkin runtime supplies a deterministic computational observation. It does not label the output as empirical evidence and does not synthesize missing sensor observations.

## Propagation
Each layer is a 13-node ring. Horizontal propagation uses a frozen snapshot. Vertical propagation uses the aggregate drift of the preceding layer.

C0 receives the four layer aggregates and applies the configured global compensation rule when the macro threshold is crossed.

## Registry
wanga_runtime/TINKIN52_REGISTRY.json is the static topology declaration.
wanga_runtime/tinkin52.py is the executable runtime.
wanga_runtime/tinkin_bridge.py maps boot/run/results into the WANGA session and Agent Bridge message shape.

## Integrity boundary
The declared logic-term count remains 175 as a specification value. The 14 supplied counts sum to 188. The runtime reports that discrepancy rather than silently resolving it.