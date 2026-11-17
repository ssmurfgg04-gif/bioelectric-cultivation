# Primary Hypothesis, Round 6: FROZEN 2026-11-17

Same rules as `docs/PRIMARIES.md`. This file is committed and pushed before any run, and its gates are never edited afterwards. Calibration seeds are 1000–1002 and test seeds 1010–1014; all are new.

**Code added before freezing** (bit-exact at defaults):
- `AgingParams.noise_kappa_damage`
- `AgingCohort.damage_dose` = ∫ senesced fraction dt

With feedback switched on, noise follows σ = σ₀ · exp(κ_int · t_bio + κ_dam · D).

## P10: if damage drives noise, does damage repair alone escape? (exp460)

**Question.** P9 showed that escape needs the noise clock reset. In the base model, noise rises with time alone *by construction*. Real noise (e.g. epigenetic drift) may instead be driven partly by accumulated damage. If a fraction φ of the noise growth is damage-driven, does repairing state damage alone become enough?

**Variant at feedback fraction φ.**
- Intrinsic noise rate: κ_int = (1 − φ) · κ.
- Damage-driven rate κ_dam is **calibrated by a rule fixed here**: κ_dam = φ · κ · 70 / mean D(70).
- mean D(70) is the cohort-mean damage dose at age 70, over the individuals alive at 70, with no intervention, φ-variant intrinsic rate, calibration seeds 1000–1002, K = 200.
- This keeps the *unrepaired* noise at age 70 roughly equal to the base model's, so the comparison is fair.

**Arms.** φ ∈ {0.5, 0.9}, 5 test seeds, K = 200, 300 yr. Repairs every 10 yr from age 48.
- **none**
- **state-only:** θ reset and all senesced cells cleared. D is *not* reset, because past damage is history.
- **state + noise:** additionally, the noise clock is set to biological age 25 and D is set to 0.

**Gates.**
- **G10a:** at φ = 0.9, state-only escapes (more than 50% alive at 300 yr) in ≥ 4/5 seeds.
- **G10b:** at φ = 0.5, state-only does *not* escape in ≥ 4/5 seeds.

**PASS** = G10a and G10b. That outcome would mean a dominant damage→noise feedback makes damage repair sufficient, while a partial one does not.

**Reported.** All arms, plus the φ = 0 reference (P9: state-only ≈ 0% alive at 300 yr).
