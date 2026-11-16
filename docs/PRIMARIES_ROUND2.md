# Primary Hypotheses, Round 2: FROZEN 2026-11-16

Same rules as `docs/PRIMARIES.md`. This file is committed and pushed before any run, and its gates are never edited afterwards. The seed ranges are new: 400–499 for P5, 500–519 for P4, 600–603 for P3′. Holm–Bonferroni applies across P3′, P4 and P5 at family α = 0.05.

The only code change made before freezing is the new option `AgingParams.hazard_link` (default `"linear"`, bit-exact with the existing model).

---

## P3′: the odds hazard link lets h_sys set the Gompertz rate (exp452)

**Rationale.** P3 failed because hazard = k·s is capped at k once burden s saturates. If the burden grows roughly logistically at rate r, then its odds s/(1−s) grow as e^{rt} *without* a ceiling. A hazard k·s/(1−s) is then exactly Gompertz with β = r.

**Variant.** `hazard_link="odds"`, `h0 × 0.1` (engine-dominant, as in P3), `mortality_k × 0.1` (so the odds hazard starts from a comparable scale). Nothing else changes.

**Design.** h_sys ∈ {0.05, 0.07, 0.10, 0.14, 0.20}, seeds 600–603, K = 400. Truncation-corrected Gompertz MLE on ages 35–100. If fewer than 30 deaths fall in the window, it extends to 130.

**Gates.**
- **G3′a:** elasticity d ln β / d ln h_sys ≥ 0.5.
- **G3′b:** β / h_sys ∈ [0.5, 1.5] at every level.

**Primary p.** One-sided OLS slope test of ln β on ln h_sys.

**PASS** = G3′a and G3′b.

## P5: P1 target memory is robust to parameter change, not just seed noise (exp453)

**Design.** Five parameters (γ, g_gap, ε, μ_θ, noise_std), each scaled one at a time by {0.5, 0.71, 1.41, 2}. Seeds 400–409 (10 per cell). Arms A (reprogram) and C (ε = 0 ablation) use the exp448 protocol. For the ε sweep, arm C stays at ε = 0 by definition.

**Gates.**
- **G5a (local robustness):** at scales 0.71 and 1.41, arm A is rewritten (h > 0.7) in ≥ 8/10 seeds for every parameter. That is 10 cells, all of which must pass.
- **G5b (mechanism necessity everywhere):** arm C is not rewritten (h < 0.35) in ≥ 9/10 seeds in all 20 cells.

**Primary p.** One-sided exact binomial test of the arm-A rewrite count over the 10 G5a cells (100 trials) against 0.5.

**PASS** = G5a and G5b.

**Reported, not gated.** The full ×0.5 / ×2 behaviour, and an exploratory ε/γ phase scan (ε × {0.05 … 3}).

## P4: aging destroys information *beyond* what added noise alone explains (exp454)

**Setup.** The exp5 MI pipeline: I(V_mid; M) with N = 60, 360 samples per estimate, 3 target basins, bins = 4. Age a ∈ [0, 1] sets noise σ = 3 + 25a and coupling g = 0.2(1 − 0.9a).

**Arms** at a = 1, each compared with young (a = 0) for the same seed:
- **full:** σ(1) and g(1). This is the exp5 aging.
- **noise-only null:** σ(1) with g = 0.2 kept intact.
- **GJ-only:** σ(0) with g(1).

**Readout.** Per-seed information drop, Δ = MI(young) − MI(arm). Seeds 500–519.

**Gates.**
- **G4a:** the 95% bootstrap CI of mean(Δ_full − Δ_noise) has its lower bound > 0. This is the test that gap-junction decay adds loss beyond noise.
- **G4b:** the 95% bootstrap CI of mean Δ_full has its lower bound > 0, i.e. aging loses information at all.

**Primary p.** Paired sign-flip permutation test of Δ_full − Δ_noise > 0 (10 000 permutations).

**PASS** = G4a and G4b.

If G4b passes but G4a fails, the "aging = information loss" claim reduces to "noise destroys information". That is trivial, and the claim would be withdrawn as a mechanism claim.
