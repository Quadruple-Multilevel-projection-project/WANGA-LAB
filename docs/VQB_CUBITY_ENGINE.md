# VQB Cubity Engine — software simulation

## Implemented model

- 36 named sub-spaces, each with INNER_nn and OUTER_nn node IDs.
- A deterministic connected multi-scale cyclic graph using offsets 1, 2, 4, 8, 16. Each node references VQB_36_TEMPLATE to represent recursive self-similarity symbolically, without infinitely expanding the graph.
- One visible/active sub-space per simulation step; every command records visibility ["ON", "OFF"].
- Fusion of wave, particle, and time feature vectors into a LanguagePoint using an explicit equal mean.
- Exactly three LanguagePoints fused through the recurrence x[t+1] = gamma*x[t] + (1-gamma)*W*sign(x[t]).
- A dimensionless five-coordinate ring-like embedding.
- A 120-step deterministic run emits 120 MAJORANA_2 command records and visits all 36 sub-spaces. The mode field is MAJORANA_2_ENTANGLE.
- JSON command report, SVG topology map, and self-contained HTML animation (play/pause/step) are emitted by tools/run_vqb_cubity_simulation.py.

## Explicit defaults

gamma=0.5; if no matrix is supplied, W defaults to the identity operator. These are visible simulation defaults, not learned weights and not source-derived physical constants. Input vectors are deterministic toy features. Ring radii are dimensionless visualization parameters.

## Evidence boundary

This is SIMULATED_NOT_PHYSICAL_VERIFICATION. The code does not establish physical superposition, Majorana quasiparticles, Einstein-ring spacetime geometry, quantum tunnelling, or time travel. TUNNELED and time_jump=true are command/state labels in the simulator. “Eulerian Sub-Space” is retained as the configured project label; this code does not demonstrate that the 36 spaces correspond to an established Eulerian mathematical construction.

## Run

From the repository root:

    python tools/run_vqb_cubity_simulation.py --steps 120 --output-dir artifacts
    python -m pytest -q tests/test_vqb_cubity_engine.py

The step count must be a positive multiple of three because each composite fixed-point merge consumes exactly three language points.
