# Tinkin / Maimonides Neural Architecture — Mathematical Runtime Contract

This document defines the executable interpretation of the supplied architecture. Terms such as
"neural" and "Metatron Crystal" are treated as architecture labels; the runtime makes no claim
that the structure is biological, physical, quantum, or empirically validated.

## 1. Envelope

State:

- spatial coordinate: p = (x, y, z) ∈ R^3
- temporal coordinate: t ∈ R
- combined state: e = (x, y, z, t)
- envelope vertices: V = 13

The 13 envelope nodes are registry entities. Their actual coordinates remain undefined until
coordinates are supplied; null coordinates are not replaced by invented geometry.

For an input vector x ∈ R^d:

z = φ(W_e x + b_e)

and tied reconstruction:

x_hat = ψ(W_e^T z + b_d)

where W_e ∈ R^(d × h), W_e^T ∈ R^(h × d).

## 2. Nested hierarchy

L1: term capsules T_i
L2: relation state R
L3: sentence configuration S = (T_a, T_b, R, Q, C)
L4: inference state I
L5: C0 meta-logic orchestration

A sentence is therefore a configuration over reusable capsules rather than a new neuron
allocation.

## 3. Reconstruction loss

For vector input x:

L_recon = (1 / d) ||x - x_hat||_2^2

The normalized runtime surprise index is:

surprise = clamp(L_recon / scale_recon, 0, 1)

The scale is configuration, not a universal physical constant.

## 4. Drift composition

For a network n:

D_n = D_recon + D_relation + D_noise + D_anomaly

Each component is normalized to [0,1]. The six named axes provide control channels:

alpha_up      threshold 0.02
beta_down     threshold 0.02
gamma_forward threshold 0.03
delta_backward threshold 0.03
epsilon_noise threshold 0.04
zeta_anomaly  threshold 0.01

Axis thresholds are configuration values. The current implementation must not infer scientific
semantics from the names alone.

## 5. Adaptive plasticity

If L_recon > θ_delta:

η_t+1 = clamp(η_t × (1 + k_plasticity × surprise), η_min, η_max)

Otherwise:

η_t+1 = η_t × stability_factor

The runtime records the adjustment rather than silently mutating the specification.

## 6. Critical-weight protection

For an EWC-compatible extension:

Ω(w) = Σ_j F_j (w_j - w*_j)^2

and the protected objective is:

L_total = L_recon + λ_EWC Ω(w)

F_j is supplied as an importance estimate. If F_j is absent, no EWC update is claimed.

## 7. Horizontal and vertical coupling

For layer l and ring position i:

H_i,l = (D_(i-1),l + D_(i+1),l) / 2

with modulo-13 indexing.

Vertical input:

V_i,l = mean(D_*,l-1), for l > 0

and V_i,0 = 0.

Coupled drift:

D'_i,l = clamp(
  D_i,l
  + κ_h |H_i,l|
  + κ_v |V_i,l|
)

where κ_h = 0.05 and κ_v = 0.10 by the supplied configuration.

## 8. C0

Global drift:

D_global = (1 / 4) Σ_l mean_i(D'_i,l)

C0 state machine:

- BALANCED: D_global < 0.75 θ_macro
- DRIFT_ALERT: 0.75 θ_macro ≤ D_global < θ_macro
- COMPENSATING: D_global ≥ θ_macro

Compensation is bounded and recorded; it does not erase the pre-compensation observation.

## 9. Logic-count integrity

The declared count is 175.

The supplied 14 gate counts sum to:

4 + 14 + 5 + 13 + 4 + 11 + 25 + 16 + 10 + 17 + 16 + 9 + 17 + 27 = 188.

Therefore:

count_delta = 188 - 175 = 13

This remains an explicit validation finding until a source resolves the discrepancy.

## 10. Runtime invariants

The machine must reject initialization when any of these are violated:

- network_count != 52
- layer_count != 4
- networks_per_layer != 13
- wheels_per_network != 3
- gates_per_network != 33
- letter_endpoints_per_network != 66
- wheel gate definitions do not contain 11 pairs each

The 13 envelope coordinates are not validated as complete until coordinate data exists.

## 11. Evidence boundary

The runtime distinguishes:

COMPUTATION → OBSERVATION → VALIDATION → ANALYSIS

A computed drift score is not automatically an empirical measurement.
