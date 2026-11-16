# Primary Results, Round 2 (gates frozen in docs/PRIMARIES_ROUND2.md, commit 6d2231c)

| Primary | Verdict | Primary p | Holm threshold | Confirmed |
|---|---|---|---|---|
| P5: P1 robust to parameters (exp453) | **PASS** | 4 × 10⁻²⁷ | 0.0167 | ✅ |
| P4: information loss beyond noise (exp454) | **PASS** (effect small) | 2 × 10⁻⁴ | 0.025 | ✅ |
| P3′: odds link sets the Gompertz rate (exp452) | **FAIL** | 1.0 | 0.05 | ❌ |

## P5: robustness of target memory
Each of five parameters was scaled ×0.5 to ×2 one at a time, with 10 seeds per cell and 400 runs in total.
- **γ, g_gap, μ_θ, noise:** the rewrite holds in **10/10** seeds at every scale. Mean head-likeness stays between 0.86 and 0.96.
- **ε (θ plasticity) is the only sensitive parameter:**
  - ×0.5 → 0/10 rewritten (mean h = 0.54)
  - ×0.71 → 8/10, which just clears the gate
  - ×1.41 and ×2 → 10/10
- **The ε = 0 ablation fails in all 20 cells (10/10 each).** Necessity holds across the whole sweep.

**Exploratory ε scan** (rewrite rate against ε multiplier):

| ε multiplier | ≤ 0.5 | 0.75 | ≥ 1.0 |
|---|---|---|---|
| rewrite rate | 0 | 0.8 | 1.0 |

The cliff sits at ε ≈ 0.03 h⁻¹, i.e. ε/γ ≈ 0.12. With a 24 h clamp that is ε·T ≈ 0.72: θ has to move about half way (1 − e^{−0.72} ≈ 0.51) toward the clamp voltage during the exposure.

**New prediction, W5 (not yet registered):** the memory threshold depends on the product ε × exposure time. A shorter exposure should fail where a longer one at the same dose succeeds.

**Caveat:** the default parameters sit just above this cliff (×0.71 gives only 8/10). The result is robust in every direction except reduced plasticity.

## P4: is aging information loss more than noise?
20 seeds, 360 samples per estimate.

| Condition | I(V_mid; M), bits |
|---|---|
| Young | 1.553 |
| Full aging (noise ↑, gap junctions ↓) | 0.482 |
| Noise only (gap junctions intact) | 0.565 |
| Gap-junction decay only | 1.570 (no loss) |

- **Gap-junction decay adds 0.083 bits of loss** beyond noise (95% CI 0.060–0.104). This passes both gates.
- **But 92% of the information loss is explained by noise alone.**
- **Gap-junction decay alone does nothing.** It only hurts when noise is present, which fits gap junctions acting as a denoiser.

**Claim narrowed accordingly:** aging-as-information-loss in this model is overwhelmingly a noise effect. Gap-junction decay contributes a small, real, noise-dependent extra loss. The exp5 framing ("junctions decayed → state decouples from morphology") overstated the role of junctions.

## P3′: fails again; root cause found
Under the odds link, β still *falls* as h_sys rises (elasticity −0.32 ± 0.02). Removing the error term as well (exp455, exploratory) makes it worse (−1.90).

**Exploratory diagnosis** (homogeneous cohorts, frailty and heterogeneity switched off):
- β still collapses: 0.027 → 0.0007 as h_sys goes 0.05 → 0.20.
- The spread of death ages *widens* (p10 to p90 runs 37–114 yr at h_sys = 0.2).
- **Mechanism:** each individual's burden is a small-population stochastic contagion. Once the first senescent cells appear, a fast engine (large h_sys) carries the burden to fatal levels quickly. Death time therefore ≈ the random *onset* time, which is set by the constant `seed_rate`. A constant-rate onset gives a *flat* hazard.
- **Consequence:** the faster the engine, the more mortality looks like an exponential waiting time and the less like Gompertz. Inter-individual variance is not the cause; within-individual stochastic onset is.
- **What would work** (theory, cf. Gavrilov & Gavrilova 2001 reliability theory): many redundant independent subsystems, so that death requires failures to accumulate rather than a single onset. Any rate-setting claim needs a new, pre-registered model structure (P3″). Tuning this one will not do it.
