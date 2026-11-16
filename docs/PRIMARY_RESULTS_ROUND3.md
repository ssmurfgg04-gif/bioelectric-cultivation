# Primary Result, Round 3 (gates frozen in docs/PRIMARIES_ROUND3.md, commit 3053b8c)

| Primary | Verdict | p |
|---|---|---|
| P6: memory threshold depends on plasticity × exposure time (exp456) | **PASS** (3/3 gates) | 9 × 10⁻¹³ |

Rewrites out of 10 seeds (seeds 700–709), by clamp duration T:

| ε multiplier | 6 h | 12 h | 16 h | 24 h | 32 h | 48 h |
|---|---|---|---|---|---|---|
| ×0.5  | 0 | 0 | 0 | 0 | 5 | 10 |
| ×0.75 | 0 | 0 | 0 | 8 | 10 | 10 |
| ×1.0  | 0 | 1 | 3 | 10 | 10 | 10 |
| ×1.5  | 0 | 9 | 10 | 10 | 10 | 10 |

- **Rescue works.** All four matched pairs with ε·T = 0.96 rewrote in 10/10 seeds. Halving plasticity is fully compensated by doubling the exposure.
- **The product collapses the data.** At every ε, the 50% point sits at ε·T ≈ 0.64–0.72. Examples: ×0.5 at 32 h (ε·T 0.64) gives 5/10; ×1.0 at 16 h (0.64) gives 3/10; ×1.5 at 12 h (0.72) gives 9/10.
- **Exploratory logistic fit:** the 50% point is at ε·T = 0.65. At that point θ has moved 1 − e^{−0.65} ≈ 48%, about half way toward the clamp voltage.

**Interpretation.** Memory forms when the exposure lasts long enough for the slow target to travel roughly half way to the imposed voltage. That gives a single dimensionless number, ε·T ≈ 0.65, with a sharp cliff around it.

**Wet-lab prediction W5** (added to docs/DATA_CONTACT.md):
- The probability of a two-headed outcome should be a steep function of exposure *duration* at a fixed dose.
- Any manipulation that slows the re-setting of resting potential (lower ε) should shift that duration curve right by the same factor.
