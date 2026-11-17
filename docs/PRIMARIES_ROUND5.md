# Primary Hypotheses, Round 5: FROZEN 2026-11-17

Same rules as `docs/PRIMARIES.md`. This file is committed and pushed before any run, and its gates are never edited afterwards. Seeds 900–902 (P8) and 950–954 (P9) are new.

**Code added before freezing** (bit-exact at defaults): `AgingCohort.gap_offset` and `noise_offset`. These are channel-specific clock offsets, so junction loss and noise growth can be rejuvenated separately.

Shared setup: K = 200, 300 yr, dt = 0.25. Repairs start at age 48 and repeat every R yr while alive. "Escape" means more than 50% of the cohort is alive at 300 yr.

## P8: the repair-budget frontier (exp458)

**Repair at completeness c** applies, at each event:
- θ pulled a fraction c of the way to θ₀;
- each senesced cell cleared with probability c;
- both clocks rolled back by c × (biological age − 25).

**Grid.** R ∈ {10, 20, 30, 40, 60} yr × c ∈ {0.25, 0.5, 0.75, 1.0}, 3 seeds per cell.

**Gates.**
- **G8a (monotone frontier):** the mean alive-at-300 is non-increasing in R at every c, and non-decreasing in c at every R (tolerance 0.05).
- **G8b (partial repair is sub-proportional):** at R = 10, alive@300(c = 0.5) < 0.5 × alive@300(c = 1.0).

**PASS** = G8a and G8b.

**Reported.** The minimal completeness that achieves escape at each R (the frontier).

## P9: which clock carries the synergy? (exp459)

**Arms.** 5 seeds; every arm repairs every 10 yr.
- **S+G:** state repair + junction clock only
- **S+N:** state repair + noise clock only
- **S+GN:** state repair + both clocks (= P7 M3)
- **G only**, **N only:** no state repair

**Prediction.** Noise growth drives the error-driven senescence hazard, so the noise clock is the one that matters.

**Gates.**
- **G9a:** S+N escapes in all 5 seeds.
- **G9b:** S+G does *not* escape in any of the 5 seeds.

**PASS** = G9a and G9b. If it fails, the junction clock (or both together) carries the synergy, and the prediction is refuted.
