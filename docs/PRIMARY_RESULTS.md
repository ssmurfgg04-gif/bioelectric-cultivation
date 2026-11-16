# Primary Results (gates frozen in docs/PRIMARIES.md, commit 6d64990)

| Primary | Verdict | Primary p | Holm threshold | Confirmed |
|---|---|---|---|---|
| P1 target memory (exp448) | **PASS** (4/4 gates) | 9.5 × 10⁻⁷ | 0.0167 | ✅ |
| P2 sustained > one-shot (exp449) | **PASS** (2/2 gates) | 1.0 × 10⁻⁴ | 0.025 | ✅ |
| P3 engine sets Gompertz rate (exp450) | **FAIL** (0/2 gates) | 1.0 | 0.05 | ❌ |

## P1: target memory (20 seeds, 100–119)
- **Arm A** (−20 mV clamp under GJ block, then 2 amputations): rewritten in **20/20** seeds.
- **Arm B** (GJ block only): not rewritten in **20/20**.
- **Arm C** (same protocol as A, but ε = 0 so θ cannot learn): not rewritten in **20/20**. **θ plasticity is necessary** for the memory.
- **Arm D** (dose), seed-mean tail head-likeness: −35 mV → 0.17, −30 → 0.43, −25 → 0.68, −20 → 0.94, −15 → 1.00. The response is monotone and sigmoidal, with a half-effect near −29 mV.

**Caveat:** arm A sits at the ceiling (20/20). Seed noise does not challenge the result at these parameters, so the robustness claim is about seed noise, not parameter noise. A global parameter sweep remains on the roadmap.

## P2: maintenance schedule (20 seeds, 200–219, K=400 each)

| Arm | Mean ratio to no intervention | 95% CI |
|---|---|---|
| Sustained (10% pull + 3 cells cleared, every 4 yr from 48) | ×1.087 | 1.081–1.093 |
| Dose-matched one-shot at 48 | ×1.044 | 1.041–1.048 |
| Difference | +0.043 | 0.038–0.047 |

At the same total dose, spreading the correction over time roughly **doubles** the lifespan benefit.

## P3: Gompertz-rate repair (FAIL)
In the engine-dominant variant (h0 × 0.1), β *falls* as h_sys rises (elasticity −0.16 ± 0.04), and β / h_sys goes from 1.19 down to 0.24. The repair does not work.

**Exploratory diagnosis** (exp451 plus a burden trace; not a primary):
- Setting h0 = 0 makes things worse (elasticity −4.7). The adult hazard goes flat.
- The cause is structural. Death hazard is `mortality_k × sen_frac`, and `sen_frac` is capped at 1, so the hazard can never exceed k = 0.12/yr.
- A larger h_sys pushes the burden toward saturation *earlier*, so the adult window sees a plateau instead of exponential growth.
- **Next repair (unregistered):** make the death hazard exponential in burden, e.g. `k·(exp(c·sen_frac) − 1)`, or let organ-level failure, not a mean fraction, set death. This must be pre-registered as P3′ before it runs.

## What the project can now claim
1. Under these model assumptions, a slow homeostatic target variable is **sufficient and necessary** for persistent, amputation-surviving bioelectric pattern memory, with a monotone dose-response.
2. In this aging model, **sustained low-dose maintenance outperforms the same dose given once**.
3. The aging model produces a Gompertz-*shaped* hazard, but **no mechanism in it sets the Gompertz rate**.
