# Falsification status

Automated in `tests/test_falsification.py` (`python -m tests.run_tests --full`).
Every claim has a pre-registered criterion. Honest negatives are recorded in
CAPS and reported — they are results, not embarrassments.

## Level 1 — model validation (reproduce known biology)

| Test | Claim | Status | Evidence |
|---|---|---|---|
| T1.1a | 24h GJ-blockade + tail depolarization produces stable two-headed target | **PASS** | exp1: two-headed pattern error 3.96 mV |
| T1.1b | Reprogramming persists across 2 amputations (memory) | **PASS** | exp1: tail head-likeness > 0.7 after each round |
| T1.1c | GJ blockade ALONE does not reprogram (negative control) | **PASS** | exp1: control tail head-likeness < 0.35 |
| T1.1d | Dose-response of reprogramming voltage | **PASS** | exp1: monotone curve -35..-15 mV |
| T1.2a | Untreated (GJ-blocked) tumor persists | **PASS** | exp2: dep-frac 1.00 |
| T1.2b | Restoring GJ connectivity normalizes the tumor | **PASS** | exp2: dep-frac 1.00 -> 0.00 |
| T1.2c | Direct hyperpolarization works without connectivity | **PASS** | exp2 |
| T1.2d | Depolarizing intervention fails to normalize | **PASS** | exp2 |
| T1.2e | Constitutive ("locked") driver is not normalizable | **PASS** | exp2 — the boundary of the phenomenon |

## Level 2 — the aging hypothesis

| Test | Claim | Status | Evidence |
|---|---|---|---|
| T2.1a | Gompertz competitive in the adult window (AIC gap < 60) | **PASS** | exp3: gaps +17..+32 |
| T2.1b | Gompertz WINS the pre-saturation window (35-70) | **PASS** | exp3: best model on all seeds |
| T2.1c | fitted beta tracks the engine rate h_sys | **NEGATIVE** | exp3: beta ~0.077-0.082 regardless of h_sys in [0.05, 0.16]; the slope is an emergent property of the frailty mixture + saturation timing, not a dial |
| T2.1d | Sustained maintenance extends lifespan | **PASS** | exp3: x1.07 median |
| T2.2a | Cross-species lifespan ordering (Spearman) | **PASS** | exp4: rho = 1.00, hydra negligible senescence |
| T2.2b | Ordering robust to +-20% parameter jitter | **PASS** | exp4: coarse contrasts stable, mean rho >= 0.9 |
| T2.2c | Full lifespan-ratio span (mouse 3.5 -> bowhead 200 yr) | **NEGATIVE** | documented structural limitation: Gompertz-family dynamics compress ratios (Strehler-Mildvan alpha-beta tradeoff) |
| T2.3a | I(V;M) high when healthy | **PASS** | exp5: 1.55 bits |
| T2.3b | I(V;M) decays with aging (information loss) | **PASS** | exp5: 1.55 -> 0.83 bits (>45% loss) |
| T2.3c | Phi peaks at intermediate coupling; modular ~ 0 | **PASS** | exp5: small-world 2.98 bits vs modular ~0 |
| T2.3d | Coherent drive raises Phi | **NEGATIVE** | linearized fixed-point Phi cannot see coherence (Jacobian depends on activation magnitude only); time-resolved measures are future work |
| T2.4a | Periodic maintenance extends median lifespan | **PASS** | exp6: x1.08-1.10 |
| T2.4b | Codec (archive+BP+verification) beats local-only maintenance | **NEGATIVE** | on smooth patterns, neighbor information is near-archive quality; and this mortality model is insensitive to written-value correctness — verification's value cannot express itself |
| T2.4c | Verification pays in a noisy channel | **NEGATIVE** | same root cause as T2.4b; pattern-fidelity-dependent mortality is the follow-up test |

## Level 3 — intervention discovery (in silico)

| Test | Claim | Status |
|---|---|---|
| T3-lite | CEM inverse-design finds interventions that steer corrupted collectives back to target | unit-tested optimizer + exp-design machinery; full held-out validation is roadmap (needs the pattern-fidelity mortality model) |

## Level 4-6 — real-biology validation, causal confirmation, consciousness interface

Out of scope for computation-only runs by design. The program's position:
these require wet-lab evidence (planaria are the cheap/fast model organism).
The computational foundation — the code that decides WHAT to test — is what
this repository provides.

## The honest pattern

The strongest results are the reproductions (Level 1: 9/9) and the
emergence of Gompertz-form mortality in the pre-saturation window. The
negative results sharpen the research program: the slope of mortality is
not a simple dial; ratio-compression is structural; coherence-sensitivity
needs nonlinear measures; verification needs fidelity-sensitive mortality.
Each negative points at a specific next experiment.
