# Primary Hypothesis, Round 4: FROZEN 2026-11-16

Same rules as `docs/PRIMARIES.md`. This file is committed and pushed before any run, and its gates are never edited afterwards. Seeds 800–804 are new.

**Code added before freezing** (bit-exact at defaults):
- `AgingCohort.clock_offset`: a per-individual offset to the time-driven decay. Junction loss and noise growth use t − offset.
- `summary()["median_lifespan_km"]`: a censoring-aware median, `inf` if more than half the cohort survives.

## P7: what must be repaired for negligible senescence ("escape") in the model (exp457)

**Question.** In this model, is there a maintenance regime under which most individuals never die within 300 simulated years? And which components must that regime repair?

The model has two kinds of damage:
- **State damage:** a drifted target θ and senesced cells. These are what P2 repaired.
- **Clock-driven decay:** gap-junction loss e^{−λt} and noise growth e^{κt}. Nothing has repaired these so far.

**Arms.** K = 200, 300 yr, dt = 0.25, seeds 800–804. All interventions start at age 48 and repeat while the individual is alive.
- **none**
- **M1, maximal state repair:** every 1 yr, θ is reset to θ₀ and *all* senesced cells are cleared.
- **M2, clock repair only:** every 10 yr, the clock offset is set so biological age = 25. No state repair.
- **M3, full:** M1 and M2 together, both every 10 yr.
- **M4, full, sparse:** M3 every 20 yr.

**Readout.** Censoring-aware median lifespan, and the fraction alive at 300 yr.

**Pre-registered expectation.** State repair alone is bounded, because the clock-driven decay keeps raising the error-driven senescence hazard. Escape needs clock repair.

**Gates.**
- **G7a (state repair is bounded):** M1's KM median is < 200 yr in all 5 seeds.
- **G7b (full repair escapes):** M3 has > 50% alive at 300 yr in all 5 seeds.

**Primary p.** Exact sign test: the probability of G7a and G7b both holding in 5/5 seeds under a coin-flip null, 0.5⁵ = 0.031 per gate. Reported per gate.

**PASS** = G7a and G7b.

**Reported, not gated.** M2 and M4, i.e. whether clock repair alone suffices and how sparse full repair can be.

**Scope note.** This is a statement about *this model*. Resetting the model's clock is a modelling operation. No current biology reverses junction loss and noise growth on demand.
