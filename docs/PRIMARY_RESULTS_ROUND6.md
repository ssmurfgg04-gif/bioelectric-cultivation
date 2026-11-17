# Primary Result, Round 6 (gates frozen in docs/PRIMARIES_ROUND6.md, commit a5d7f39)

**P10 FAIL (near miss).** G10b passed and G10a failed.

Calibration as pre-specified: κ_dam = 1.49 (φ = 0.5) and 2.69 (φ = 0.9).

| Feedback fraction φ | Arm | Alive at 300 yr | KM median |
|---|---|---|---|
| 0 (P9 reference) | state-only | 0% | ~81 |
| 0.5 | none | 0% | ~93 |
| 0.5 | state-only | 0% | ~113 |
| 0.5 | state + noise reset | 81% | ∞ |
| 0.9 | none | 9% | ~100 |
| **0.9** | **state-only** | **47%** | **~287** |
| 0.9 | state + noise reset | 80% | ∞ |

**Gate outcome.** At φ = 0.9, state-only repair escaped in 0/5 seeds. Every seed landed just under the bar (median 279–298 yr; 47% alive on average, against the > 50% required). By the pre-registered rule this is a FAIL.

**What it still shows** (exploratory reading, not a confirmed claim):
- **The benefit of damage repair depends steeply on how much noise is damage-driven.**
  - φ = 0 → +11 yr from state-only repair
  - φ = 0.5 → +20 yr
  - φ = 0.9 → **about +190 yr**
- **When most noise is damage-driven, damage repair nearly self-sustains.** The repair also slows the noise clock.
- **State + noise reset escapes at every φ** (80–85%). That remains the only regime that robustly escapes.

**Caveat on the comparison.** The calibration matched the mean *unrepaired* noise at age 70, but the unrepaired feedback variants still live longer (~93–100 yr vs ~70 in the base model). Feedback lowers noise early in life. Absolute lifespans across φ are therefore not like-for-like; the within-φ arm comparisons are.

**Practical meaning (in-model).** Whether clearing damage alone could ever be enough depends on one empirical number: what fraction of age-related molecular noise is *caused by* accumulated damage rather than by time itself. Below about 90%, a separate noise-reset step is needed. Measuring that fraction (e.g. whether senolytic clearance slows epigenetic-clock drift, and by how much) is the key biological experiment this model points to.
