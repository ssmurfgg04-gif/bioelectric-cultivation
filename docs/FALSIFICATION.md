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
| T2.4a | Periodic maintenance extends median lifespan | **PASS** | exp6: x1.08-1.10; exp8 fidelity regime: codec x1.11 |
| T2.4b | Codec (archive+BP+verification) beats local-only maintenance | **NEGATIVE -> RESOLVED** | exp6 (proximity mortality): equality, root-caused. exp8 (fidelity mortality): codec/local **x1.09 PASS** — the value of verification was real but inexpressible until mortality depended on discrete-state CORRECTNESS |
| T2.4c | Verification pays in a noisy channel | **NEGATIVE -> RESOLVED** | exp8 degraded channel (x2.5): codec/local x1.06 via consensus-read verification + the write-precision gate (refuse when actuation cannot place symbols) |

## Level 3 — intervention discovery (in silico)

Pattern-fidelity mortality (`cultivation/bioelectric/fidelity.py`, exp8): death
from discrete-state corruption (organ failure when the fraction of cells in the
correct Vmem band drops below critical), corruption as regional cluster jumps
(the two-headed-worm mechanism). This is the regime in which written-value
CORRECTNESS matters — the precondition the exp6 negatives identified.

| Test | Claim | Status |
|---|---|---|
| T3.1a | Verified maintenance extends life (codec/none >= 1.06) | **PASS** — exp8: x1.11 mean over 5 seeds |
| T3.1b | THE GATE: codec beats local under fidelity mortality (>= 1.03) | **PASS** — exp8: codec/local x1.09; regional jumps are invisible to consensus, only archive-referenced verification detects and restores them |
| T3.1c | Verification pays in a degraded channel | **PASS** — exp8 x2.5 channel: codec/local x1.06 (write-precision gate refuses reckless writes) |
| T3.1d | Regeneration rejuvenates (>= 1.25 and > codec) | **PASS** — exp8: regen/none x1.25, regen/codec x1.13; the planarian strategy (Dai et al. 2025) reproduced — cycles must repeat because the channel engines are not reset |
| T3.1e | Connexin restoration adds to verified maintenance | **NEGATIVE** — exp8: chan/codec x0.94; in the low-noise regime the boost is net-HARMFUL (un-quarantining corrupted domains). Value inverts with the binding constraint (cliff probe: chan/none x1.06 when noise binds) |
| T3.1f | Verification-gating the boost pays | **PASS (marginal)** — chan 76.7 vs blind 76.5; margin small because verification rarely refuses in a clean channel; the strong form is T3.1c |
| T3.1g | The channel limits even full regeneration | **PASS** — cliff probe: regen at x0.77 of its low-noise value when noise crosses the level spacing; two-bottleneck structure (pattern AND channel) |
| T3.2 | Bioelectric aging clock: fidelity predicts remaining lifespan | **PASS** — Spearman rho 0.39-0.45 at ages 30-60, p < 0.01, stable across seeds |
| T3.3 | Gompertz remains competitive under fidelity mortality | **PASS** — AIC gap within 30 (Weibull edges this weakened-engine regime; Gompertz emergence is exp3's default-regime result) |

## Level 3F — feasibility audits for the cultivation tiers (exp9)

Pure arithmetic on literature values; no tunable parameters.

| Claim | Status |
|---|---|
| F1 Contact-range biofield effects are physical | **SUPPORTED** — cardiac dipole E at 1 cm = 3.2e3 V/m vs 333 V/m needed for a 5 mV cell-state flip (Schwan); at 10 cm, 100x short |
| F2 Organism-range passive biofield influence | **DEAD-AS-STATED** — 1e5 coherent cardiac dipoles needed at 1 m: 1e5x the body's total ionic current budget |
| F3 Schumann/vacuum resonance coupling | **DEAD-AS-STATED** — induction path ~1e13 short; resonance gain Q-bounded (lossy tissue Q ~ 1-10) |
| F4 Macro telekinesis via micro-PK amplification | **DEAD-AS-STATED** — lifting 1 g at PEAR's epsilon and 1e6 bit/s addressing takes ~7e8 years; ceiling ~mW even biasing every thermal event in 10 g |
| F5 Selection-level effects are already macro IF real | **OPEN** — an amplified RNG bit IS macroscopic (energy from the supply; the quantum event only selects): this is what PEAR actually measured |
| F6 The bioelectric layer is the first physical expression point of any consciousness-matter interface | **OPEN, SHARPENED** — the mW-scale ceiling is ~9 orders above the 1.25e-16 J of a bioelectric state transition: IF the interface exists, it shows up in Levin's layer first |

## Level 4 — the tower: inverse design, novel morphology, interface, scaling, integration (exp10-15)

| Test | Claim | Status |
|---|---|---|
| T4.1 | CEM search converges on the policy landscape | **PASS** — exp10: 28x10 evals, best 93.1 on search fitness vs 81.9 best hand-built (+13.6% on paired seeds; +19% vs hand codec) |
| T4.2 | Discovered policy wins on held-out seeds | **PASS** — exp10 |
| T4.3 | Discovered policy transfers to a perturbed regime | **PASS** — +3.4% paired gain under perturbed physics |
| T4.4 | The discovered structure is nontrivial (not hand-guessable) | **PASS** — dense early schedule + verification-gated boost; no hand baseline reaches it |
| A1 | Novel morphologies reachable (third_eye, dual_zone >= 0.90) | **PASS** — 0.965 / 0.922 |
| A2 | Latched novel plans persist after clamp release | **PASS** — decay < 0.05 over 500 free units (all six targets) |
| A3 | Regenerative memory is LOCAL (partial yes, full no) | **PASS** — partial amputation recovers novel identity (with overshoot); full amputation loses it |
| A4 | Difficulty scales with novel-boundary count | **PASS** — Spearman rho > 0 |
| A5 | Controls: twoheaded >= 0.90 (Levin anchor), restorative >= 0.95 | **PASS** — 0.94 / 0.97 |
| B1 | Reflex-only control has a ceiling | **PASS** — exp12 |
| B2a-c | Training transcends the ceiling x5; coherence (not energy) carries precision; incentive loop tracks | **PASS** — 12% within-band for random vs 100% coherent; loop tracks +10 -> +5 |
| B3 | Practice sustains the written state | **PASS** |
| B4a-c | Discrete state flip: trained sticks, untrained doesn't, latch carries sticking | **PASS** — 100% / 0% / 0% |
| B5a-e | NOREREWARD (Pezzulo 2021): plateau above baseline, not decay to zero; latch carries retention | **PASS** — all five; the somatic latch IS the re-writable memory medium |
| B6a-c | Bistability (hysteresis), rewritability (A/B/A), bounded hopping | **PASS** — Ryom 2021 latching dynamics reproduced |
| C1a | Gate vs jump-rate: saturating quadratic, R2 >= 0.9 | **PASS** — R2 = 0.997 (1.25 -> 2.29) |
| C1b | Gate vs kappa: linear erosion, R2 >= 0.9 | **PASS** — R2 = 0.91 (1.59 -> 1.13) |
| C2 | Per-cell archive writes shift the cliff knee | **NEGATIVE** — both knees at kappa 0.055; write precision contributes only an additive 0.05-0.07 at low kappa |
| C3 | Low-difficulty protocols survive exp12's corruption stream; survival anti-correlates with difficulty | **PASS** |
| C4a | Overshoot scales with latch strength | **NEGATIVE** — overshoot does not scale with k_anchor/alpha_latch |
| C4b | Overshoot scales with junction sharing | **NEGATIVE** — no scaling with gap coupling either |
| C4c | Remodeling (overshoot) bounded by the latch | **PASS** — the bound is real even where the scaling is not |
| D1 | The exp8 gate transfers to the held-out corpus | **PASS** — x1.909 |
| D2 | Frozen discovered policy beats no-intervention | **PASS** — x1.752 |
| D2b | Discovered policy beats the hand-built arm on held-out | **NEGATIVE** — x0.895 (111 vs 124): the search found ITS regime's optimum; the milder held-out physics rewards pure maintenance over the discovered regen schedule |
| D3 | The latch layer composes onto the aging stack | **NEGATIVE -> RESOLVED** — x0.800 -> x1.000 (exp16: consensus-anchored latch v2 + matched-channel memory k=0.25/yr; the iteration-1 mechanism identified: the v1 pin ran ~100x the junction channel's bandwidth and chronically decoupled theta from V — see Level 5) |
| D4 | The stack tolerates noreward passive decay | **PASS** — x1.000 (decay_tau 80): the latch carries what was written |
| D5 (AUC) | CEM more sample-efficient than GA at matched budget | **NEGATIVE** — GA AUC 93.6 vs CEM 91.0 (140 evals, CRN): the landscape's broad ~94 plateau is reached by uniform sampling; exp10's own 280-eval CEM sat at 93.1 |
| D5 (final) | CEM final-best not worse than GA | **PASS** — 94.1 vs 93.9; either search beats hand design by ~19% |
| E1 | Random policies do not match the discovered one | **PASS** — 0/8 beat it (mean 90.9, best 104.5 vs 111.2) |
| E2 | No-latch relaxes exactly to the null baseline; latch holds the novel zone | **PASS** — 0.86 = null vs 0.96 native |
| E3 (sanity) | Shuffled genome leaves default physics untouched | **PASS** — none+shuffled 63.5 == none 63.5 |
| E3 | Archive correctness is load-bearing | **PASS** — codec+shuffled 48.3 < none 63.5: a wrong archive is worse than no archive |
| E4 (pre-registered amplitude/inertness) | Transfer <= 0.6x native; transfer >= null - 0.10 | **NEGATIVE x2** — transfers land at 0.75x/0.82x native AND below null (0.69/0.79 vs 0.87/0.86) |
| E4 (degrade-not-zero, pre-registered) | Transfer degrades but is not annihilated | **PASS** |
| E4 (sign-flip, POSTHOC) | The intervention's sign flips on the wrong target | **PASS** — native +0.05/+0.10 above null becomes -0.18/-0.07 below it: off-target reprogramming hazard; derived from this run's data, labeled post-hoc |

## Level 5 — the write semantics of death (exp16, D3 resolved)

The tower's last open joint, closed and turned into a measured finding. Four
competing write semantics for the moment a cell senesces (stasis / erasure /
transcription / broadcast — each a different universe), tested against
demographics (arm A), composition with the codec (arm C), and the
novel-pattern information ledger (arm D). Module:
`cultivation/bioelectric/senescence_semantics.py`; sweep citations:
`research/d3_sweep/README.md`.

| ID | Criterion | Result |
|---|---|---|
| C0 | The v1 negative reproduces on the held-out corpus | **PASS** — v1/plain x0.844 (was x0.800 in exp14) |
| C1 (iter 1) | Consensus anchoring alone composes | **NEGATIVE** — x0.881 at k_anchor=50: the mechanism identified — the pin's bandwidth dominates the junction channel it backs up, decoupling theta from V and inflating the senescence hazard (sen@60 0.048 vs no-latch 0.014) |
| C1 (matched) | The matched-channel latch composes with codec maintenance | **PASS** — x1.000 at k_anchor=0.25/yr; the D3 GATE IS OPEN |
| C2 | Composition holds under the biologically-corrected death semantics (broadcast) | **PASS** — v2+broadcast / broadcast-no-latch x0.991 |
| C3 | Interior optimum in the k-sweep | **NEGATIVE** — monotone: composition degrades smoothly from x1.000 (k=0.25) to x0.881 (k=50); the optimum sits at the sweep's lower edge. The D3 LAW: the somatic memory must FORM fast (alpha_latch ~20/yr) and PULL weakly (k <~ junction bandwidth ~0.4/yr); whether a lower floor exists (memory too weak to function) is untested below k=0.25 |
| A1 | The death semantics are demographically distinguishable | **NEGATIVE** — medians 60.2-60.9 yr, sen@60 within 0.003: the death-write is informationally decisive but demographically silent at biological amplitude (a real finding, not a power failure: ~15 cell deaths/individual against 60 cells) |
| A2 | The broadcast's spread is state-mediated (junction-dependent, dose-dependent) | **MIXED** — dose-response present at gain 8 (sen@60 +0.005, rate +0.003-0.007/yr), junction-dependence confounded: junction decay makes tissue MORE vulnerable to death broadcasts (perturbations linger when healing coupling is gone — matches the connexin-loss impaired-wound-healing literature) |
| D1 | Transcription preserves the novel pattern better than erasure | **NEGATIVE** — I_recoverable@60: 0.534 vs 0.535 (identical): single-cell memory copies are outvoted by the collective consensus within weeks; the pattern is an attractor of collective dynamics, not a property of individual cells |
| D2 | Transcription's memory carriers migrate outward | **NEGATIVE** — centroid drift 5.55 vs 5.50 (stasis): no migration signature |
| D3a | Erasure is the worst semantics for the pattern | **PASS (weak)** — erasure 0.535 vs stasis 0.560: the frozen-anchor stasis is worth +2.5% recoverable information |
| D4 | The live-tracking memory (v1) preserves the novel pattern best | **PASS** — I_anchor@60 0.746 vs v2's 0.55 — and this is exactly the property that made v1 fail composition: a memory that follows the live state has no firewall (cancer semantics). The trade-off is real and now measured |

| D5 | The archive-referenced codec erases novel morphologies | **PASS** — I_recoverable@60: 0.100 vs 0.584 (none): every maintenance cycle repairs the novel zone back to factory default. The hazard is INFORMATIONAL, not mortal: the same arm's median lifespan RISES to 83.7 vs 61.7 (maintenance value dominates the wrong-zone cost) — the current codec kills the pattern, not the animal |
| D6 | A memory-referenced codec (tracker memory) maintains the novel pattern | **NEGATIVE** — I_recoverable@60: 0.126: the consensus anchor TRACKS slow collective drift (boundary blur propagates inward); maintaining what the tissue remembers maintains the decay. Tracker-memory + memory-referenced maintenance = a feedback loop that faithfully maintains drift |
| D7 | The protected memory tier (on_write-marked, non-tracking) holds the written pattern | **PASS** — I_recoverable@60: 0.907, @100: 0.896; median 73.8 vs 61.7 none (+20%): the written pattern survives a century of aging, senescence broadcasts, and maintenance cycles — Pezzulo & Levin 2021 bistable somatic memories, implemented |
| D8 | Memory correctness is load-bearing (the E3 analog) | **PASS** — a coherent WRONG memory (zone written to -60) is maintained with full conviction: I_recoverable 0.000, median 54.1 (0.73x the correct-memory arm): a wrong memory is worse than a tracker |

**The D3 answer (the star question, in this model's currency):** death is a
transition for the pattern — but through DISTRIBUTED REDUNDANCY (collective
consensus + frozen stasis anchors + genomic archive), NOT through
transcription. The naive "the self moves cell-to-cell on death" fails not
because death erases, but because no single cell carries the self: the
pattern lives in the consensus, and the consensus cannot be moved one cell
at a time.

## Level 5-6 — real-biology validation, causal confirmation

Out of scope for computation-only runs by design. The program's position:
these require wet-lab evidence (planaria are the cheap/fast model organism).
The computational foundation — the code that decides WHAT to test — is what
this repository provides.

## The honest pattern

The strongest results are the reproductions (Level 1: 9/9), the emergence of
Gompertz-form mortality in the pre-saturation window, the Level-3 gate: under
fidelity-dependent mortality, archive-verified maintenance beats
consensus-only maintenance (x1.09), regeneration rejuvenates (x1.25), the
bioelectric clock predicts remaining lifespan (rho ~0.45), and the
two-bottleneck structure (pattern AND channel) emerged as a finding rather
than an assumption — and now the tower: the gate is a scaling law (R2 0.997),
novel morphologies are engineerable and persist (0.96, held after release),
the somatic latch is the re-writable memory medium (noreward plateau, not
decay), the whole stack composes on held-out physics (x1.91 gate, x1.71
stack), and the controls hold: no random policy matches the search, no-latch
relaxes to baseline, a shuffled genome turns maintenance into harm, and
misapplied protocols flip sign.

The remaining negatives are mechanistically understood: the slope of
mortality is not a simple dial; ratio-compression is structural;
coherence-sensitivity needs nonlinear measures; connexin restoration is
net-harmful in low-noise regimes (quarantine loss); per-cell write precision
does not shift the channel cliff; the latch does not yet compose with the
aging stack (x0.80 — the tower's open joint); CEM shows no sample-efficiency
edge over GA on this broad-plateau landscape; and transferred protocols are
actively destructive, not inert. Each negative points at a specific next
experiment — and the exp9 audits now bound which cultivation-tier claims are
worth running at all.
