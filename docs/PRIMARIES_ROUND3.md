# Primary Hypothesis, Round 3: FROZEN 2026-11-16

Same rules as `docs/PRIMARIES.md`. This file is committed and pushed before any run, and its gates are never edited afterwards. Seeds 700–709 are new.

## P6: the memory threshold depends on plasticity × exposure time (exp456)

**Source.** Prediction W5, from the exploratory ε scan in exp453. The rewrite appeared once ε·T_clamp was at least about 0.7.

**Claim.** Whether a transient clamp leaves a persistent rewrite depends on the product ε·T (how far θ can move during the exposure), not on ε or T separately. Halving plasticity is rescued by doubling the exposure.

**Design.** The exp448 arm-A protocol (clamp at −20 mV under gap-junction block, then 2 amputation rounds). The only change is the clamp duration T.
- ε multiplier ∈ {0.5, 0.75, 1, 1.5} (×0.04 h⁻¹)
- T ∈ {6, 12, 16, 24, 32, 48} h
- seeds 700–709 (10 per cell, 240 runs)

**Matched pairs** (ε·T = 0.96 for each): (0.5, 48), (0.75, 32), (1, 24), (1.5, 16).

**Gates.**
- **G6a (dose-time monotone):** at default ε, the rewrite count is non-decreasing in T (tolerance 1 seed), with ≤ 2/10 at T = 6 and ≥ 8/10 at T = 48.
- **G6b (rescue / collapse):** every matched pair has ≥ 8/10 rewritten.
- **G6c (product, not time alone):** at T = 24, ε × 0.5 (ε·T = 0.48) has ≤ 2/10 while ε × 1.5 (ε·T = 1.44) has ≥ 8/10.

**Primary p.** One-sided exact binomial test of the 40 matched-pair trials against 0.5.

**PASS** = G6a, G6b and G6c.

**Reported, not gated.** The full 4 × 6 grid of rewrite rates and a logistic fit of rewrite on log(ε·T).
