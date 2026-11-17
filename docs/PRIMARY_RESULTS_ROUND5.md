# Primary Results, Round 5 (gates frozen in docs/PRIMARIES_ROUND5.md, commit 3111615)

| Primary | Verdict |
|---|---|
| P8: repair-budget frontier (exp458) | **PASS** (2/2 gates) |
| P9: which clock carries the synergy (exp459) | **PASS** (2/2 gates): it is the **noise** clock |

## P9: the noise clock carries everything (5 seeds, repairs every 10 yr)

| Arm | Alive at 300 yr | KM median |
|---|---|---|
| State + junction clock | 0% | ~81 yr |
| **State + noise clock** | **85%** | **∞** |
| State + both clocks | 85% | ∞ |
| Junction clock only | 0% | ~70 yr (= no repair) |
| Noise clock only | 7% | ~93 yr |

- **Junction-loss repair adds nothing at all.** Adding it to state repair, or using it alone, gives the same result as leaving it out.
- **Noise-growth repair is the whole effect.** This matches P4, where junction decay alone lost no information.
- **The two-channel synergy from P7 is really state × noise.** Damage is caused by the rising noise (accumulated molecular disorder). Escape requires repairing the damage *and* resetting the noise source.

## P8: how much repair, how often (3 seeds per cell)

Alive at 300 yr, by repair period (rows) and completeness c (columns):

| repair every | c = 0.25 | 0.5 | 0.75 | 1.0 |
|---|---|---|---|---|
| 10 yr | 0.02 | 0.19 | **0.66** | **0.84** |
| 20 yr | 0.00 | 0.03 | 0.16 | **0.76** |
| 30 yr | 0.00 | 0.00 | 0.04 | 0.46 |
| 40 yr | 0.00 | 0.00 | 0.01 | 0.19 |
| 60 yr | 0.00 | 0.00 | 0.00 | 0.02 |

- **The frontier:** escape needs ≥ 75% completeness every 10 yr, or full completeness every 20 yr. Nothing sparser than every 30 yr escapes, even at 100%.
- **Partial repair is sharply sub-proportional:** half-complete repair every 10 yr keeps only 19% alive, against 84% for full repair. The returns behave like a threshold, not a slope.
- **With full repair, median lifespan by period:** 60 yr → ~94, 40 yr → ~125, 30 yr → ~250, 20 yr → ∞.

**Design target this implies (in-model).** A rejuvenation therapy must reset the *noise source* (not junction coupling) together with clearing state damage. It has to be at least ~75% complete and applied about every decade. Weaker or rarer versions buy decades, not escape.

**Scope.** These are model results. "Noise" here is a phenomenological variable. A candidate biological reading is accumulated epigenetic / transcriptional noise, which partial-reprogramming studies target. That mapping is a hypothesis, not established by this work.
