# Primary Results, Round 7 (frozen in docs/PRIMARIES_ROUND7.md: b1d2c1b + amendment A 371b2c7)

| Primary | Verdict | Key number |
|---|---|---|
| P13: fit to human data, predict the plateau | **FAIL** | 0/150 sets accepted; the homogeneous model is too steep |
| P13′: frailty repair | **FAIL** (G13a fail, G13b pass) | plateau *shape* right (ratio 1.05), *level* 0.18 vs 0.7 observed |
| P11: Gompertz rate set by mechanism | **FAIL** (G11a pass, G11b fail) | elasticity **0.99 ± 0.004**, but Weibull fits better than Gompertz |
| P12: interior optimal repair interval | **FAIL** (G12a pass, G12b fail) | optimum lay beyond the grid (40 yr was its edge) |
| P14: memory persists in 2D tissue | **FAIL** (G14a fail) | 0/20 rewritten; mean h 0.53 after 200 h |

All five gates failed as frozen. Several failures are still informative.

## 1. Reliability model: speed, and a mechanism that sets the rate
- **Speed.** 10 000 individuals × 130 yr in 0.14 s, about **650× faster** per individual-year than `AgingCohort`. The full 180-set human fit ran in under a minute.
- **First mechanism that controls β.** β/k ≈ 0.89 at every k, with elasticity 0.991 (p = 5 × 10⁻²⁶). In the bioelectric model, exp447, P3 and P3′ all failed this test. The reliability structure fixes the *rate-setting* problem.
- **But the shape is Weibull-like** (AIC). That is the known reliability-theory result for systems that start out undamaged. Gavrilov's Gompertz case needs heavily damaged initial states, i.e. a small Poisson λ per element. Calibrating to a human median of 80 pushed λ into the thousands, so it never reached that regime.

## 2. Contact with real data: what the model gets wrong
- **Homogeneous individuals:** no parameter set gives both a median of 80 and β = 0.085. At median 80, β ≥ 0.106. Deaths are too concentrated.
- **With 10% frailty:** the model hits both targets (three sets accepted).
- **The plateau:** it *does* plateau (h at 110–115 / h at 105–110 = 1.05; pure Gompertz would give 1.53). But the level is **0.18/yr against the observed ~0.7** (Barbi et al. 2018), about 4× too low. Its 105+ survivors are also far too many (~3% of the cohort).
- **Conclusion:** the reliability model's late-life tail is too fat. Some failure process must accelerate at extreme ages. Fitting an observable the model was *not* tuned on is what exposed this.

## 3. Repair with costs
- **Without harm:** every schedule from 5 to 40 yr gives the same RMST (~517 of 600 yr). Even repair every 40 yr escapes, because of the large redundancy.
- **Harm of 10⁻³/yr per event:** more frequent repair is strictly worse inside the frozen grid (5 yr → 129, 40 yr → 256).
- **Exploratory extension:** the optimum is interior at **~60 yr** for harm 10⁻³ (RMST 282) and **~50 yr** for harm 10⁻⁴ (481). Beyond ~70 yr, aging kills.
- **Lesson:** once each therapy carries a cost, "repair as often as possible" becomes "repair at a specific interval". The optimal interval is set by the ratio of the harm per event to the damage accumulated between events.

## 4. 2D tissue: the memory is not a true attractor (the most important finding)
Exploratory follow-up, same protocol with no amputation. Tail head-likeness at 20 / 50 / 100 / 200 h after release:

| | 20 h | 50 h | 100 h | 200 h |
|---|---|---|---|---|
| 1D chain | 1.00 | 1.00 | 1.00 | 0.97 |
| 2D sheet | 0.88 | 0.78 | 0.68 | 0.53 |

- The rewritten target **leaks away in 2D**. Higher coordination (4 neighbours instead of 2) lets θ diffusion from the surrounding trunk erode it.
- In 1D, the same erosion is just slower.
- So P1's "memory" is a slowly decaying transient, not a bistable state. It looked permanent only because a chain has few neighbours and the protocol was short.
- **Consequence:** real tissue is 2D/3D. A model of genuine bioelectric memory needs a **nonlinear, bistable** single-cell term, such as voltage-gated channel feedback (Pietak & Levin 2017; Cervera et al. 2019). The linear relaxation in `collective.py` cannot hold it.

## New research gateways opened
1. **Bistable cells:** add voltage-gated channel nonlinearity to θ, so a rewritten pattern is a true attractor. Re-test P1 and P14 in 2D/3D. This is the top priority.
2. **Initial-damage reliability:** fit a small-λ, many-element Gavrilov model to recover a true Gompertz form, and match the plateau level (0.7), not just its shape.
3. **Therapy scheduling as optimal control:** with the fast simulator, optimise the repair interval and completeness jointly against harm. This gives a schedule a trial designer could actually use.
