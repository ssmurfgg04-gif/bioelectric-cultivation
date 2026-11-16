# Claims Audit: external review, 2026-11-16

This audit re-checks the README's headline claims against the code and the deposited results. Every number below can be reproduced from this branch.

**Status key**
- **STANDS**: the claim holds as stated.
- **NARROWED**: the claim is true only in a weaker form.
- **WITHDRAWN**: the claim is not supported.
- **POST-HOC**: the test could not have failed, or its gate was changed after a fail.

| # | Claim (README) | Status | Evidence |
|---|---|---|---|
| A1 | Gompertz-form mortality emerges | **STANDS** (form only) | exp3 AIC comparison |
| A2 | Mean fitted β = 0.090/yr, "the empirical human range" | **WITHDRAWN** | exp447 (below) |
| A3 | β is set by the inflammaging engine h_sys | **WITHDRAWN** | exp3 C2=False; exp447 elasticity −0.10 |
| A4 | Cross-species Spearman ρ = 1.00 | **WITHDRAWN as evidence** | presets constructed monotone in lifespan |
| A5 | Model "runs on the real HCP connectome", human transfer Outcome B | **NARROWED** | the input is functional connectivity, not a connectome |
| A6 | exp443 "CALIBRATED-AND-ALIVE" | **POST-HOC (tautological)** | see below |
| A7 | Stage scores "95% / 101% PASSED" | **WITHDRAWN** | no definition of the percentages exists |
| A8 | Level-1 planarian memory and cancer-normalisation reproductions | **STANDS** (qualitative) | tests green; structure matches Durant 2017 / Chernet & Levin 2015 |
| A9 | RS/GF(256) codec layer | **STANDS** | unit tests |
| A10 | Target memory needs θ plasticity (P1) | **CONFIRMED** (pre-registered) | exp448: 20/20, ε=0 ablation 0/20 |
| A11 | Sustained > one-shot maintenance (P2) | **CONFIRMED** (pre-registered) | exp449 |
| A12 | A mechanism sets the Gompertz rate (P3) | **REFUTED** (pre-registered) | exp450, exp451 |
| A13 | P1 memory robust to parameters (P5) | **CONFIRMED** — sensitive only to ε (cliff at ε/γ ≈ 0.12) | exp453 |
| A14 | Aging = information loss beyond noise (P4) | **CONFIRMED but narrowed** — GJ decay adds 0.08 bits; noise explains 92% | exp454 |
| A15 | Odds hazard link sets the Gompertz rate (P3′) | **REFUTED** — stochastic single-onset dynamics flatten hazard | exp452, exp455 |

---

## A2/A3: what sets the Gompertz slope (exp447)

**Fix first.** `hazard_and_fits` fitted the adult window (ages ≥ 35) without conditioning on survival to 35, so it treated a left-truncated sample as if it started at birth. It now takes `entry=` (default 0 keeps the old behaviour bit-exact). On synthetic Gompertz data the corrected fit recovers β within 6% across 0.05–0.16 (`tests/test_survival_fit.py`). The uncorrected fit overstates small slopes (true 0.05 came back as 0.058).

**Experiment.** `experiments/exp447_beta_sensitivity.py`, pre-registered in its docstring. It scales 9 aging parameters by ×0.5–×2 (5 levels, 3 seeds, K=400) and measures how strongly each one moves β (the log-log slope, called elasticity).

| parameter | elasticity | verdict |
|---|---|---|
| h_sys ("the engine") | −0.099 | INERT |
| soft, margin, h0, lambda_gap, sigma0 | ≈ 0 | INERT |
| mortality_k | 0.128 | WEAK |
| seed_rate | −0.162 | WEAK |
| kappa_noise | 0.439 (non-monotone) | WEAK |

**Corrected baseline:** β = **0.054 ± 0.002 /yr**. That is *below* the human range, which is roughly 0.07–0.10 (a mortality doubling time of about 7–10 yr).

**Pre-registered verdict:** no parameter controls β. The "human-range β" claim is withdrawn.

**Post-run observation** (exploratory, not pre-registered). Across the kappa_noise sweep, β peaks at the default value and falls on both sides (0.011 → 0.054 → 0.022). Meanwhile the median lifespan moves monotonically from 91 to 44 yr. So β is a **fitting-window artefact**: it is largest when the mortality wave happens to sit inside the 35–100 window. The model produces a Gompertz-*shaped* hazard, but it has no mechanism that sets its *rate*.

**What would fix it:** a mechanism whose time constant is the doubling time. One option is to make the inflammaging feedback the dominant senescence pathway, so the burden really grows as e^{h·t}. Then re-run exp447 and require |elasticity(h_sys)| ≥ 0.5.

## A4: cross-species ρ = 1.00

In `SPECIES_PRESETS`, `seed_rate`, `h_sys` and `mortality_k` are each strictly ordered by the observed lifespan they are meant to predict. A model whose death rate rises with every one of those parameters cannot produce any ordering other than the lifespan ordering, so ρ = 1 follows from the construction. With n = 5 the exact one-sided p is 1/120, even before accounting for that.

**To restore it:** source each species' parameters from measurements chosen without looking at lifespan (connexin turnover, somatic mutation rate, etc.), and predict a held-out sixth species.

## A5: the human graph

`data/human_fc_schaefer400.npy` holds HCP group-average **functional connectivity**: correlations between BOLD time series. `human/substrate.py` uses it, top-6 sparsified, as gap-junction conductance. Correlated activity is not physical coupling, and cortical parcels are not gap-junction coupled at this scale.

The human runs therefore show that the model's qualitative behaviour **is robust to graph topology**. They do not show transfer to humans. Real transfer would need, at minimum, structural (DWI) connectivity and an observable the model was not built from.

## A6: exp443 is tautological

exp443 defines its kill window as `achieved_contrast − band` = 7.41 − 0.58 = 6.83. It then tests whether `achieved_contrast ≥ kill_window`, i.e. whether 7.41 ≥ 7.41 − 0.58. That holds for every achieved value whenever the band is positive, so the test **cannot fail**.

The earlier, non-tautological gate (exp437: nominal bar 9.42) said **DEAD**. The honest reading is that d-02 failed its pre-named in-silico test. A valid falsifier must fix its threshold from something other than the value under test.

---

## Process rules adopted from this audit

1. **A gate is written and committed before the run and is never re-derived after a FAIL.** A repair becomes a *new* experiment with a *new* claim, labelled exploratory.
2. **No threshold may be a function of the quantity it tests.**
3. **Primary claims are capped at five**, with Holm–Bonferroni across them. Everything else is labelled exploratory.
4. **Any README number needs ≥ 20 seeds and a 95% bootstrap CI.**
5. **An agent that ran an experiment does not grade it.** A fresh reviewer checks the result against the frozen gate.
