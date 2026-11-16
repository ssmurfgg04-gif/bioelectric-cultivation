# Primary Result, Round 4 (gates frozen in docs/PRIMARIES_ROUND4.md, commit 09bcd48)

**P7 PASS.** Both gates held in 5/5 seeds (sign-test p = 0.031 per gate).

| Arm (from age 48) | KM median lifespan (5 seeds) | Alive at 300 yr |
|---|---|---|
| none | 68–72 | 0% |
| M1: full state repair every 1 yr (θ reset + all senescent cells cleared) | 96–101 | 0% |
| M2: clock repair only, every 10 yr (junctions + noise reset to age 25) | 88–104 | 7% |
| **M3: state + clock repair every 10 yr** | **∞ (all seeds)** | **83%** |
| **M4: state + clock repair every 20 yr** | **∞ (all seeds)** | **77%** |

**Findings**
- **Neither repair alone is enough.** Even *maximal* yearly state repair adds only about 28 yr. Clock repair alone adds about 25 yr.
- **Together they are strongly synergistic.** Repairing both every 10 yr flattens mortality.
  - Residual hazard ≈ −ln(0.83)/252 yr ≈ 7 × 10⁻⁴ per year.
  - That is constant and not rising, i.e. negligible senescence in the model.
  - At that rate, half of a cohort dies after about 950 yr. The remaining deaths are accidents of noise, not aging.
- **Sparse is fine.** Full repair every 20 yr is almost as good as every 10 yr (77% vs 83% alive at 300).

**Interpretation (within the model).** Aging here has two independent damage channels: what the system *is* (state) and what it *has become* (the decay of coupling and noise). Escape requires periodically repairing **both**. Repairing one channel lets the other kill. The model mirrors the "repair all damage categories" logic of damage-repair approaches to longevity (cf. de Grey's SENS). It goes one step further by predicting a *synergy*: partial repair returns far less than its share.

**Scope.** "Resetting the clock" is an operation in the model. No current biology restores junction coupling and noise levels to a young state on demand. This is a design target, not a capability.
