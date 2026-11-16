# Units and Scales

The library has two time scales, and they are **not linked**. The collective layer runs in hours. The aging layer runs in years. No experiment in the repo converts between them.

## Collective layer (`cultivation/bioelectric/collective.py`): t in **hours**
The unit follows from usage: `run(24)` is the "24 h" reprogramming protocol (exp1, exp448).

| Symbol | Code | Default | Unit | Meaning |
|---|---|---|---|---|
| V | `S[:,0]` | −85…+5 | mV | membrane voltage (clipped to Nernst bounds) |
| θ | `S[:,1]` | — | mV | slow homeostatic target |
| γ | `gamma` | 0.25 | h⁻¹ | V relaxation toward θ (τ = 4 h) |
| g | `g_gap` | 0.20 | h⁻¹ | gap-junction coupling rate per edge |
| ε | `eps` | 0.04 | h⁻¹ | θ plasticity (τ = 25 h) |
| μ | `mu_theta` | 0.015 | h⁻¹ | θ diffusion per edge |
| σ_η | `noise_std` | 0.30 | mV·h⁻¹ᐟ² | V noise |
| dt | — | 0.1 | h | Euler–Maruyama step |

Ratio checks:
- ε/γ = 0.16, so θ is about 6× slower than V. This is the separation the memory mechanism relies on.
- With 2g/γ = 1.6, coupling and relaxation are comparable. The pattern is neither fully local nor fully smoothed.

## Aging layer (`cultivation/bioelectric/aging.py`): t in **years**

| Code | Default | Unit |
|---|---|---|
| `gamma`, `g0`, `eps` | 0.25, 0.20, 0.04 | yr⁻¹ (same numbers as above, *different* unit) |
| `lambda_gap`, `kappa_noise` | 0.030, 0.048 | yr⁻¹ |
| `sigma0`, `theta_drift` | 0.20, 0.045 | mV·yr⁻¹ᐟ² |
| `h0`, `h_sys`, `h_inflam`, `mortality_k`, `seed_rate` | — | yr⁻¹ |
| `margin`, `soft` | 6.0, 2.5 | mV |

**Known inconsistency.** The aging layer reuses the collective's rate constants with years in place of hours. That makes a cell's V–θ relaxation 8 760× slower than in the collective. The aging layer is therefore a phenomenological model of slow drift, not a time-scaled copy of the hourly physics. Results must not be carried between the layers quantitatively.

## Dormant channels (ch2–ch7)
The six dormant channels are kept, not removed. They have zero dynamics at defaults (the "dormancy contract" in `collective.py`), and 19 experiment scripts (exp257 onward) read or write them. Removing them would break those scripts for no behavioural change. **Rule:** no paper or README claim may depend on a dormant channel.
