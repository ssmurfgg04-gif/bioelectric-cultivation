# Primary Hypotheses, Round 7: FROZEN 2026-11-17

Same rules as `docs/PRIMARIES.md`. This file is committed and pushed before any primary run, and its gates are never edited afterwards. Holm–Bonferroni applies across P11–P14.

**New code.** `cultivation/bioelectric/reliability.py` is a reliability-theory aging model after Gavrilov & Gavrilova (2001):
- n vital blocks in series, each holding a Poisson(λ) number of redundant elements;
- elements fail at rate k;
- death occurs when any block is empty;
- it supports optional repair with a per-event harm, and an extrinsic hazard.

The model is vectorised: a 10 000-individual cohort over 130 yr takes 0.14 s, against about 3.7 s for 400 individuals in `AgingCohort`. That is roughly **650× more individual-years per second**.

**Pre-freeze probe (disclosed).** A single calibration seed (1100) was run on a coarse (n, λ) grid at k = 0.085, only to see the lifespan scale. It showed median lifespans of 50–100 yr need λ in the hundreds to thousands. No test seeds were used.

---

## P13: fit to human mortality, then predict the late-life plateau (exp461)

**Real-data targets** (from the literature, typical modern low-mortality populations):
- Median adult lifespan ≈ 80 yr.
- Gompertz slope β ≈ 0.085/yr, i.e. a mortality doubling time of about 8 yr.

**Held-out observable.** The mortality plateau beyond age 105. Barbi et al. (2018, *Science* 360:1459), using Italian validated data, report the hazard levelling off at about 0.7/yr (annual death probability ≈ 0.5).

**Fit (ABC rejection).**
- Grid: n ∈ {2, 4, 8, 16, 32}, λ ∈ {300, 1000, 3000, 10 000, 30 000}, k ∈ {0.02, 0.03, 0.04, 0.05, 0.06, 0.08}.
- Calibration seed 1100, K = 4000, 140 yr.
- Accept a set if its median ∈ [77, 83] and β ∈ [0.075, 0.095], using the truncation-corrected fit on ages 35–100.
- Best fit = the accepted set minimising ((M − 80)/3)² + ((β − 0.085)/0.01)².

**Prediction.** Run every accepted set on test seeds 1110–1114 with K = 20 000, and measure the occurrence/exposure hazard on [105, 110) and [110, 115).

**Gates.**
- **G13a:** at least one set is accepted, and the median predicted hazard on [105, 115) across accepted sets lies in [0.40, 1.20]/yr.
- **G13b (plateau, not exponential):** for the best fit, h[110, 115) / h[105, 110) < 1.3. Pure Gompertz at β = 0.085 would give 1.53.

**PASS** = G13a and G13b.

## P11: the Gompertz rate is set by mechanism (exp462)

**Design.** Take the best-fit (n, λ) from P13 and scale k by {0.5, 0.71, 1, 1.41, 2}. Seeds 1120–1122, K = 10 000. The fit window scales with each run's median M: [0.45M, 1.25M], with the truncation-corrected MLE.

**Gates.**
- **G11a:** elasticity d ln β / d ln k ≥ 0.5.
- **G11b:** Gompertz AIC < Weibull AIC at all 5 levels (seed-pooled).

**PASS** = G11a and G11b. This is the target that P3 and P3′ failed in the bioelectric model.

## P12: with a cost to repair, the best repair schedule is interior (exp463)

**Design.** Best-fit P13 parameters, plus extrinsic hazard μ_ext = 5 × 10⁻⁴/yr. Complete repair (c = 1) every R ∈ {5, 10, 20, 30, 40} yr from age 48. Harm per event δ ∈ {0, 10⁻³}/yr, which is permanent and cumulative. Seeds 1130–1132, K = 4000, 600 yr. The metric is restricted mean lifespan (RMST) to 600 yr.

**Gates.**
- **G12a:** with δ = 0, RMST is non-increasing in R (tolerance 1%). More frequent repair is always better.
- **G12b:** with δ = 10⁻³, the RMST-maximising R is neither 5 nor 40, i.e. an interior optimum.

**PASS** = G12a and G12b.

## P14: target memory persists in 2D tissue (exp464)

**Design.** A 20 × 20 grid with 4-neighbour coupling (N = 400). Rows 0–4 are head (−20 mV), the rest trunk (−50 mV). The "tail" is rows 15–19. Seeds 1140–1159.
- **A:** clamp the tail at −20 mV under GJ block (0.05) for 24 h, release, then run 200 h.
- **B:** GJ block only.
- **C:** arm A with ε = 0.

The readout is tail head-likeness at the end.

**Gates.**
- **G14a:** A has h > 0.7 in ≥ 18/20 seeds.
- **G14b:** B has h < 0.35 in ≥ 18/20.
- **G14c:** C has h < 0.35 in ≥ 18/20.

**PASS** = all three. This tests whether the 1D memory mechanism survives the higher coordination number of 2D tissue.

## Not doable from code (recorded)
- **OSF registration:** Jack has to register these files at osf.io; the git commit hash is the interim timestamp.
- **Independent human review:** still pending.
