# Primary Hypotheses: FROZEN 2026-11-16

These are the only confirmatory claims of this project. Everything else in the repository is **exploratory**.

This file is committed **before** any of the runs below. The gates may not be edited after a run. A repair becomes a new, separately labelled experiment.

**Multiplicity.** Each primary reports one primary p-value. Holm–Bonferroni across P1–P3 at family α = 0.05.

**Seeds.** 20 independent seeds per arm unless stated: P1 uses seeds 100–119; P2 uses seeds 200–219. Seeds were not used anywhere before this file.

**Reviewer rule.** The script prints the gates and a machine-readable verdict. The verdict is computed by code from these thresholds only.

---

## P1: Bioelectric target memory (exp448)

**Claim.** A transient (24 h) depolarising clamp of the posterior quarter under gap-junction (GJ) block rewrites the slow target θ. The rewrite persists across two amputation–regeneration rounds, and the persistence *requires* θ plasticity (ε > 0).

**Arms** (protocol of exp1; N=100, dt=0.1):
- **A, reprogram:** clamp −20 mV, GJ block 0.05, 24 h, then 2 amputation rounds.
- **B, GJ-block-only control:** GJ block 24 h, no clamp, then 1 round.
- **C, ε-ablation:** arm A with `eps = 0` (θ cannot learn).
- **D, dose:** clamp voltage ∈ {−35, −30, −25, −20, −15} mV, 1 round.

**Readout.** Tail head-likeness h ∈ [0,1] (`morphospace.head_likeness`). A seed counts as "rewritten" if h > 0.7 and "not rewritten" if h < 0.35.

**Gates.**
- **G1a:** arm A rewritten in ≥ 18/20 seeds.
- **G1b:** arm B not rewritten in ≥ 18/20.
- **G1c:** arm C not rewritten in ≥ 18/20. This is the necessity test: if memory survives without θ plasticity, the mechanism claim fails.
- **G1d:** in arm D, the seed-mean h is non-decreasing with depolarisation (tolerance 0.02), the mean h at −35 mV is < 0.35, and the mean h at −20 mV is > 0.7.

**Primary p-value.** One-sided exact binomial test of arm-A successes against 10/20, i.e. whether the rewrite rate is above a coin flip.

**PASS** = all of G1a–G1d.

## P2: Sustained beats dose-matched one-shot maintenance (exp449)

**Claim.** A periodic partial correction extends median lifespan. A single correction of the **same total dose** at the first application time does not extend it as much.

**Arms** (AgingCohort, default params, K=400, 130 yr, dt=0.25):
- **none:** no intervention.
- **sustained:** the exp3 schedule. Every 4 yr from age 48: θ pulled 10% toward θ₀ and up to 3 senesced cells cleared, while alive.
- **one-shot:** at age 48, a single θ pull of 1 − 0.9¹³ ≈ 0.746 (13 = number of sustained applications from 48 to ≤ 100), and up to 39 senesced cells cleared.

**Readout.** Per-seed median lifespan ratios: sustained/none (R_s) and one-shot/none (R_o).

**Gates.**
- **G2a:** the 95% bootstrap CI of mean R_s has its lower bound > 1.00.
- **G2b:** the 95% bootstrap CI of mean (R_s − R_o) has its lower bound > 0.

**Primary p-value.** One-sided paired sign-flip permutation test of R_s − R_o > 0 (10 000 permutations).

**PASS** = G2a and G2b.

## P3: A Gompertz rate set by mechanism (exp450, model repair)

**Background.** exp447 showed that no parameter of the default model controls β. P3 tests a pre-specified repair: the **engine-dominant variant**, with the error-driven senescence scale `h0` reduced ×0.1 so that systemic self-catalysis (`h_sys`) dominates senescence. No other parameter changes.

**Claim.** In the variant, the adult Gompertz slope (truncation-corrected, window 35–100) tracks `h_sys`.

**Design.** h_sys ∈ {0.05, 0.07, 0.10, 0.14, 0.20}, 4 seeds each (300–303), K=400. If fewer than 30 deaths fall in the window, the window extends to 130.

**Gates.**
- **G3a:** the elasticity d ln β / d ln h_sys is ≥ 0.5.
- **G3b:** β / h_sys ∈ [0.5, 1.5] at every level.

**Primary p-value.** OLS slope test of ln β on ln h_sys over all 20 runs (H₀: slope ≤ 0, one-sided).

**PASS** = G3a and G3b.

Note: whatever P3's outcome, it does **not** license a "human-range β" claim. Choosing h_sys to hit 0.085 would be calibration, not prediction.

---

## Demoted to exploratory (and why)

- **"Aging = information loss" (I(V;M) 1.55 → 0.83 bits):** there is no noise-matched null with intact coupling yet, so the drop may just follow from adding noise.
- **Everything numbered exp4–exp446:** exploratory. Ledger entries L1–L301 stand as the exploratory record.
