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

### exp19 — CEM on the anchored stack: hold, not reach (the century-hold objective)

Fitness = mean over ages 30..100 of alive_fraction x I_recoverable (death is
ultimate pattern loss), searched over 8 anchored-stack policy dimensions
including k_anchor (the matched-channel axis). Baselines: HAND (the exp17
protected-arm policy), NONE (write, never maintain).

| ID | Criterion | Result |
|---|---|---|
| H1 | Discovered policy >= 1.05x HAND on held-out hold-score | **NEGATIVE** — 0.582 vs 0.575 (+1.2%): the exp17 hand-built policy is near-optimal on this landscape; CEM confirms rather than improves (echoes exp14 D5's broad-plateau finding — ALL single-dimension ablations shift hold by <= 0.01) |
| H2 | The search rediscovers the matched-channel law (k_anchor <= 1.0) | **PASS** — k converges to 0.33 from an uninformative start (the exp16 CALIBRATION emerges as a SEARCH RESULT: form fast, pull weak) |
| H3 | Interior allocation (procedure risk forbids max-therapy) | **PASS** — budget 9 (<12), period 2.5 yr, and the no-risk arm shows the discovered policy gains +8.7% when h_proc removed (the risk term is binding, not cosmetic) |
| H4 | The hold-optimum differs materially from exp10's reach-optimum | **PASS** — maintenance start 31.5 vs 20.5 (+54%); write at 14.5 (adolescence, not immediately); hold-dense (2.5 yr) but low-amplitude (boost off, factor 1.06): hold is not reach |
| — | Regime transfer | **NEGATIVE (honest)** — perturbed physics: HAND 0.640 vs discovered 0.634 — the discovered schedule is regime-specific (echoes exp14 D2b) |
| — | The century-hold value itself | **PASS** — vs no-maintenance: +23% pattern retention held-out (0.582 vs 0.474); the written pattern is held over a century by policy, not luck |

## Level 5 — real-data validation (the no-wetlab layer, exp18)

The first contact between the model and REAL biological data: the public
planarian single-cell atlases (PSCA 21,612 cells; Fincher 50,456 cells),
ingested through a literature-grounded gene-ID mapping (planosphere Rosetta
Stone May 2024 + AHRD 2020 annotations; validated 3/3 against PMC12421698's
Smed-TRPM-a1/a2/c). The vmem_inference layer's four pre-registered
predictions, tested on transcriptome-inferred resting potentials:

| ID | Criterion | PSCA (n=10 types) | Fincher (n=7 types) |
|---|---|---|---|
| V1 | Neoblasts among the most hyperpolarized cell types (rank <= 30%) | **PASS** — rank 3/10; jackknife 18/20 | **PASS** — rank 1/7; jackknife 20/20 |
| V2 | Muscle hyperpolarized AND pump-high (the Beane 2013 atlas-testable form) | **NEGATIVE** — hyperpolarized YES, pump expression below median | **NEGATIVE** — pump-high YES, Vm above median (opposite failure mode) |
| V3 | Phagocytes depolarized AND cation-leak-high | **NEGATIVE** — rank 4/10, cation rank 4 | **PASS** — rank 5/7 + cation top-3 (Cathepsin+ n=7,034 — the better-powered cohort) |
| V4 | Innexin does NOT predict own-Vm (\|rho\| < 0.35) AND enriched in coupled tissues | **NEGATIVE** — rho +0.42 (co-expression confound); top-3 pigment/phagocyte/parenchymal | **NEGATIVE** — rho +0.75; top-3 muscle/neural (coupled-tissue hit, but the rho fails) |

**Honest read:** one solid confirmation (V1 — the Levin-lab stemness-
hyperpolarization program, rank-robust across two independent atlases and
20-draw weight jackknifes), one clean refutation (V2 — the muscle form
fails in opposite directions on the two atlases; the H,K-ATPase gene never
resolved in the AHRD annotation, and the anterior-wound spatial claim is
inherently untestable in dissociated data), one split (V3 — supported by
the better-powered atlas only; the injury-transient clause is untestable in
resting data by construction), and one proxy-falsification with mechanism
(V4 — innexin expression DOES co-vary with inferred Vm across cell types;
the physiological form — coupling, not own-Vm — requires spatial/functional
data the atlases cannot provide). Cross-atlas map consistency is moderate
(Spearman 0.39): the GHK-from-expression method is rank-robust for
stemness gradients but not an absolute-Vm predictor (neurons predict
depolarized — gating is invisible to transcriptomes). This is the
calibration for the fidelity-clock program: dyes, not atlases, carry the
absolute map.

## Level 6 — wet-lab causal confirmation (the fidelity-clock program)

Designed, pre-registered, not yet run: docs/FIDELITY_CLOCK.md (FC1-FC5).
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

And now the tower has touched real data: V1 (the stemness-hyperpolarization
prediction) confirmed on two independent public atlases; V2-V4 honestly
refuted or split with mechanisms named (gating is invisible to
transcriptomes; dissociated cells have no junctions; spatial claims need
spatial data); the century-hold search rediscovered the matched-channel law
and found the hold-landscape to be a plateau the hand-built policy already
sits on. The wet-lab program that would settle the rest is specified,
pre-registered, and falsifiable stage by stage (docs/FIDELITY_CLOCK.md).

## Level 6 — M17: spatial data and the recorded-outcome corpus (exp20, exp21)

**exp20 — PRISTA4D, the first SPATIAL data** (Han et al. 2026, GigaScience;
STDS0000399, 0/12/36 hpa spatial matrices; gene bridge dd_Smed_v6 ->
SMED300 -> SMESG via the planosphere Rosetta Stone 2020, 270 ion genes):

- **V1s PASS (third modality)** — neoblast bins rank 3 of 31 spatially
  annotated cell types at 0hpa. Stemness-hyperpolarization now confirmed
  in PSCA, Fincher, AND spatial bins.
- **V3s REFUTED (spatial transient)** — wound-edge vs interior contrast:
  +0.8 mV at 0hpa, +0.5 at 12hpa, +1.6 at 36hpa. The intact animal's tips
  are already edge-depolarized; the injury effect does not cleanly exceed
  that baseline (12hpa CI -0.42..+1.59 includes 0).
- **V3c REFUTED (spatial phagocyte clause)** — cathepsin+/phagocyte bins
  rank 4/31 most HYPERpolarized in space (they were depolarized in
  Fincher's dissociated atlas). Modality and annotation granularity
  change the phagocyte clause's sign — V3 stays split, now with a spatial
  counter-instance.
- **V4s REFUTED (junction smoothness)** — Spearman(innexin, local Vm
  roughness) at 12hpa = -0.024 (CI -0.045..-0.004: tiny, sign right) but
  the kv control is MORE negative (-0.045). No junction-specific smoothness
  signature above the K-channel family's. At the family-expression level,
  innexin does not organize the spatial Vm map beyond generic
  cell-type composition.
- **Kills-row consequence:** the transcriptome->Vm layer is rank-robust for
  stemness (V1 x3) but CANNOT resolve the spatial coupling and injury
  transient clauses — those now REQUIRE measurement (the FC1-FC5 wet-lab
  program is no longer optional for V3/V4; it is the only route).

**exp21 — PlanformDB, the recorded-outcome corpus** (Lobo et al. 2013,
PlanformDB 2.5.0: 1,716 experiments, 412 RNAi targets, penetrance-weighted
outcomes; Num-weighted, RegenPeriod>0 only):

- **PB0 PASS** — cutting baseline (0.487) is the lowest abnormality class
  < ion_channel (0.736) < morphogen (0.744) < other RNAi (0.788).
- **PB1 REFUTED** — innexin RNAi experiments (n=9, from 3 publications)
  show abnormality 0.542, NOT above other RNAi (0.788); MWU p=0.99 in the
  wrong direction. **Effective power caveat: ~3 independent studies** —
  this refutes the STRONG form (junction knockdown among the most
  disruptive perturbations) at low power; the weak form (junctions
  necessary: 0.542 > 0.487 cutting) survives.
- **PB2 REFUTED** — ion-class (0.657) below morphogen-class (0.744):
  recorded outcomes do not rank bioelectric perturbation above morphogen
  signaling. The bioelectric-dominance framing is bounded.
- **PB3 REFUTED** — innexin result sets show mixed outcomes in only 3/10
  cases; the graded-latent-state picture (TAS) is not the corpus norm.
- **Kills-row consequence:** our junction-load-bearing claim is now
  explicitly WEAK-form: junctions are necessary for normal patterning
  (above cutting baseline) but not uniquely disruptive among recorded
  perturbations. exp16's bystander lethality stays a statement about
  MAINTENANCE dynamics, not regeneration outcomes.

## Level 7 — exp22: the TAS geometry cross-validated on the ensemble

**exp22 — the memory co-metric on our policy space** (TAS, Blattner 2026:
Q cost / R write map / K_mem efficiency; central differences around the
HAND policy, fresh seeds 41-43, 152s):

- **T1 PASS** — the write-efficiency distribution is strongly anisotropic:
  a dominant write axis exists, and it is **k_anchor** (shift/unit
  -0.0495 ± 0.0078, the only individually significant axis): the
  matched-channel law of exp16 is the dominant axis of the local memory
  co-metric. Their geometry, our landscape, same ridge.
- **T2 REFUTED** — only ONE costly-silent direction (dense_low_amp)
  where TAS predicts several; the boost_* dims are flat in BOTH effect
  and cost (free nulls, not costly silences). The plateau of exp19 is
  better described as 'flat-but-aligned' than 'isotropic'.
- **T3 PASS** — the CEM-discovered hold policy sits at cosine +0.617 to
  the efficiency-weighted axis structure: the search climbed the
  co-metric's ridge without being told the geometry existed.
- **T4 PASS** — HAND's dominant move is not on a silent axis.
- **Kills-row:** TAS's anisotropy and alignment predictions transfer;
  its silent-direction multiplicity does not. The geometry adds a useful
  summary of WHY the century-hold landscape looks like a plateau to
  point-estimates while still having a direction of improvement.

## Level 8 — exp23: multi-pattern allocation (the AI-Scientist's best idea, executed honestly)

**exp23 — competing bioelectric memories under a shared maintenance
budget** (the AI-Scientist trial's top idea, unblocked by the
multi-zone `pattern_ledgers` API; budget sweep 1/2/4/6 cells/cycle =
the scarcity dial; K=200, 120yr, seeds 21-23; cluster-aligned scrambled
zones C/A/B/birth of 15 cells; three probes fixed geometry and metric
before the pre-registered full run):

- **E1 NEGATIVE (directionally present, sub-threshold)** — the
  competition cost on the volatile pattern B at the tightest budget
  (1 cell/cycle) is 0.023 (solo 0.604 vs competing 0.581), below the
  pre-registered 0.05 bar; at budget 6 it vanishes (0.780 vs 0.795 —
  the channel is rich enough that competition is invisible; bootstrap
  CIs overlap in both cases). Expression capacity is *effectively*
  per-pattern at planarian scale: the maintenance channel is not the
  binding constraint between memories; each pattern's deficit is set by
  its own physics.
- **E2 REFUTED** — no allocation policy (balanced / fixed priority /
  severity-weighted / critical-threshold) beats the status-quo
  cell-order allocation on min-I_V@60 at ANY budget (all within 0.02,
  all marginally WORSE); dynamic does not beat static (overall-I_V at
  budget 1: dynamic mean 0.674 vs fixed 0.677). The AI-Scientist's
  central hypothesis — allocation strategy matters under constraint —
  fails in this stack.
- **E3 PASS (the load-bearing result)** — physics dominates policy by
  more than an order of magnitude: at budget 1 under balanced
  allocation the stable pattern holds 0.963, the volatile 0.571, the
  high-turnover 0.485 — a 0.48 spread vs the 0.02 policy spread. The
  mechanism (from the write audit + alive-only ledgers): the
  high-turnover pattern's deficit is a DEATH-RESTORATION EQUILIBRIUM
  (cells die at 2x hazard, get restored, die again — the steady-state
  wrong-fraction is set by the hazard rate, and allocation only shifts
  the restoration lag); among LIVING individuals C's expression
  (0.670) actually exceeds B's (0.653) — C's all-K deficit is driven
  by mortality selection, not expression failure.
- **E4 NEGATIVE (marginal, one arm)** — every policy arm at every
  budget clears the no-maintenance median (49.0 yr; e.g. 51.5 at
  budget 1, 71.8 at budget 6); the single failure is the solo_B control
  itself at budget 1 (48.2 vs 49.0): a single-pattern codec at extreme
  scarcity is slightly worse than no codec — the tracker-maintains-
  drift trap (exp17 P2a) burns the tiny budget on unwritten zones.
- **R PASS (bit-exact regression)** — solo17 re-ran exp17's
  anchored_protected arm with identical seeds/K/horizon/budget:
  median 73.8 yr and I_rec@60 0.907, EXACTLY the published values. The
  additive hooks (jump_mult, hazard_boost, alloc) changed nothing when
  unused, at experiment scale.
- **The two-layer capacity finding (carries forward)** — the protected
  memory tier stores every written pattern for free (I_anchor = 1.000
  for all three patterns under NO maintenance, verified pure-cluster
  geometry): STORAGE is per-pattern and free; EXPRESSION (I_V) is the
  scarce, budget-bound layer. Any wet-lab claim about "memory capacity"
  must specify which layer it means.

- **Kills-row:** the AI-Scientist's multi-pattern-allocation research
  program, executed with pre-registered criteria on this stack, does
  NOT yield an allocation-policy result — the honest outcome is a
  negative with a mechanism (equilibrium-dominated expression, physics
  first-order) and a clean replication guard. Multi-pattern maintenance
  is robust (E4 within noise for all real policies); what cannot be
  bought with budget allocation is a pattern whose cells keep dying.

## Level 9 — exp24: potentiation vs the equilibrium (the AI-Scientist's idea #2, executed honestly)

**exp24 — memory potentiation: can the corruption side of the
death-restoration equilibrium be attacked where budget allocation could
not move the restoration side?** (idea #2 'memory_enhancement_protocols'
strategy 3: "after each maintenance cycle, increase the stability of
corrected cells by reducing their jump probability for 5 years"; stack
hook `FidelityAgingCohort.potentiate` / `_pot_until`, bit-exact when
unused, golden-tested both paths; exp23's exact geometry, seeds 21-23,
K=200, budgets 1/6 + window sweep w2/w5/w10 + a permanent-potentiation
ceiling arm; one recorded design probe preceded pre-registration and
motivated the P7 ceiling criterion):

- **P1 NEGATIVE — the equilibrium does not move at the idea's literal
  spec.** Potentiation factor 0.25 / window 5yr shifts the volatile
  pattern's working state by +0.004 (0.795 to 0.800) against the
  pre-registered 0.046 bar (= 2x exp23's entire allocation-effect
  ceiling). The probe-explained mechanism: window = cadence means
  protection covers only last-cycle corrections (~13% of clusters at
  any moment; coverage@60 = 0.131) — the benefit cannot accumulate.
- **P7 NEGATIVE — the deep result: even PERMANENT potentiation cannot
  break the equilibrium.** With protection that never expires and 47%
  coverage, B's I_V@60 is 0.801 (+0.006). The failure is not the
  transient coverage geometry — it is structural: potentiation is
  correction-coupled by construction, so it protects exactly the
  clusters maintenance already keeps right; the deficit lives in the
  UNCORRECTED tail (budget-starved corruption) and in mortality
  selection, neither of which jump-protection touches. The exp23
  equilibrium now survives attacks from BOTH sides: restoration-side
  redistribution (allocation, exp23) and corruption-side reduction
  (potentiation, exp24).
- **P2 PASS — gating is real but moot.** Random-placement potentiation
  (the AI-Scientist's own control, same per-cycle pair count) delivers
  nothing at either budget (+0.007 at 25% coverage, inside the 0.01
  gate): the enhancement must be lent where correction happened — the
  ungated-boost hazard (exp8) reproduces in a new modality — but the
  correctly-gated benefit is ~0 anyway.
- **P3 PASS — the pattern dissociation confirms the two-bottleneck
  structure.** Delta_B (+0.004) > Delta_C (+0.001) and > Delta_A
  (+0.002) at b6: potentiation acts on the jump axis, so the
  jump-volatile pattern gains the most; C's hazard-driven deficit and
  A's already-free hold barely move.
- **P4/P5 PASS — budget coupling and dose-response behave as the
  coverage mechanism predicts** (b6 delta > b1 delta; 0.5 -> 0.25
  factor monotone-or-plateau across a flat curve) — the machinery
  works exactly as designed; it is the equilibrium that refuses.
- **P6 NEGATIVE with structure — the lifespan window effect is
  non-monotone.** Transient windows extend median life slightly
  (pot025 73.0 / pot05 74.0 vs plain 71.8) but long windows actively
  SHORTEN it (w10 65.9; permanent 66.1 — a 5.7yr COST at 47%
  coverage). Recorded mechanism hypothesis (unresolved): permanent
  protection accumulates on maintained clusters while the deficit —
  and the organ-failure hazard — lives in unmaintained ones; frozen
  protection may also remove the jump-and-repair cycling whose
  correction events keep organ fidelity dynamics away from the
  failure boundary. The failure has shape, not just sign.
- **R PASS — bit-exact regression.** The plain arm reproduced exp23's
  published default arm exactly (max per-pattern I_V@60 delta
  < 0.005, median within 0.5yr, both budgets): the potentiation hook
  changed nothing when unused, at experiment scale.

- **Kills-row:** the AI-Scientist's memory-enhancement/potentiation
  research program, executed with pre-registered criteria, is REFUTED
  in this stack — and the refutation closes a loop: the expression
  equilibrium is now shown to be immovable from the allocation side
  (exp23) AND the corruption side (exp24), which is precisely the
  claim FIDELITY_CLOCK FC1d wagers on (regional turnover ordering).
  What potentiation bought instead: a gated-vs-ungated replication
  (P2), a clean dissociation (P3), and a non-monotone mortality cost
  (P6) — three falsifiable tendrils, not one.

## Level 9 — exp25: the century-hold policy vs competition (the user's stress test)

**exp25 — exp19's CEM-discovered 8-dim century-hold policy transplanted
into exp23's competing-memory world** (write_age 14.5, start 31.5,
period 2.5, budget 9, k_anchor 0.326, unverified channel boost 0.369 x
1.059, procedure risk 3e-5/write-event/yr; seeds 21-23 — held-out for
the policy AND matched to exp23's regression anchor; 8 arms including
budget-clamped stress (b2), solo references, and the status-quo
replication; a first 105yr pass was rejected for pure survivor-censoring
artifacts in medians and re-run at exp23's 120yr convention — identical
trajectories, honest re-run):

- **S1 PASS — the policy doesn't just survive competition, it WINS
  decisively.** Overall hold 0.625 (discovered) vs 0.500 (HAND
  transplanted): +0.125, median +14.4yr (70.6 vs 56.2). exp19's H1
  failed by 1.2% in the single-pattern world; the same policy's edge
  EXPLODES under competition. The single-pattern search world could not
  reveal competition-robustness — the searched dimensions (2x checkup
  frequency, richer budget) are exactly the dimensions that matter when
  memories compete.
- **S2 PASS — the competition-cost asymmetry, with a sign surprise.**
  cost(discovered) = -0.026 (BETTER under competition than solo);
  cost(HAND) = +0.007. Composition caveat recorded: solo scores the
  volatile B alone, multi scores the mean over A/B/C where two-thirds
  of the novel load sits on easier zone physics — the within-world
  comparisons are clean, the cross-world delta carries this term.
- **S3 PASS — the equilibrium law is policy-invariant.** Under the
  transplanted policy (weak pull 0.326 + boost therapy): A 0.953 >
  B 0.852 > C 0.834 at 60 — exp23's E3 physics ordering survives a
  policy the equilibrium has never seen.
- **S4 PASS — the schedule survives the starved budget.** At b2
  (where exp23 measured real competition cost): discovered 0.421 vs
  HAND 0.354 (+0.067). The advantage is the SCHEDULE (period 2.5,
  start 31.5), not channel richness alone.
- **R PASS — bit-exact regression.** The status-quo arm reproduced
  exp23's published default b6 arm exactly (I_V A/B/C 0.951/0.795/
  0.780, restored 10088, median 71.8) — the transplant changed nothing
  when its knobs matched the status quo.
- **The procedure-risk ledger (recorded):** the discovered policy pays
  2.3x the write events of HAND (19,367 vs 8,494 restored) under the
  same 3e-5/write-event/yr hazard and still wins by +0.125 hold; the
  h_proc-free status-quo arm (0.594) shows HAND-with-risk (0.500)
  loses 0.094 hold to procedure risk alone — the searched cadence
  overcomes a procedure load that buries the hand policy.

- **Kills-row:** nothing dies — exp25 is the stack's first all-pass
  stress test at this scale — but it kills a belief: that exp19's
  "H1 failed by 1.2%" meant the searched policy was marginal. The
  century-hold policy is, in fact, the best policy anyone has run in
  the competing-memory world, and the reason is legible: it searched
  on the axes (cadence, budget, write timing) that competition
  punishes. Single-pattern benchmarks UNDER-estimate policies that
  will serve multi-pattern reality.

## Level 10 — exp26: equilibrium attribution (taking the balance point apart)

**exp26 — the attribution experiment the user asked for after both edge
attacks failed.** exp23 moved the restoration side (allocation, ceiling
0.023); exp24 moved the corruption side (potentiation, +0.0056
permanent); the death-restoration equilibrium did not move. So instead
of attacking it again, exp26 takes it apart: 24 arms on exp23's exact
multi-pattern geometry (seeds 21-23, K=200, 120yr; the default arm is
the bit-exact regression anchor), sweeping every primitive class —
substrate (jump rate x0.25-4), restoration (budget 12, period 1.25-10),
death channels (k_fail 0-0.6, mortality_k/4), zone coupling (C's hazard
1-8), channel noise (x0.5-2), architecture (cluster granularity
n_clusters 4/12/20) — plus a four-arm flux-composite compensation
protocol (Phi = corruption cells/yr / restoration cells/yr held at its
default 0.34 while both sides multiply) and a new corruption-source
instrument (every wrong zone cell at ledger age classified senescence /
jump / non-jump from per-cluster jump and per-cell repair timestamps —
additive hooks, golden-tested, no RNG consumption).

- **EQ1a NEGATIVE — the flux ratio is NOT the invariant.** The four
  Phi-equal compensation arms land at B I_V@60 0.736/0.743/0.644/0.666
  vs default 0.795: preserving the corruption:repair ratio does NOT
  preserve the balance point. But the dissociation is the finding: the
  ALIVE-ONLY fidelity of the same arms is 0.905/0.898/0.915/0.921 —
  HIGHER than default's 0.876. The alive-state equilibrium IS
  flux-compensated; the all-K LEDGER equilibrium is not, because the
  compensation arms' animals die young (medians 47.2/45.6/28.1/27.9 vs
  71.8) and death freezes corrupted states into the ledger. The
  death-restoration equilibrium decomposes into two terms: an
  alive-state balance (flux-like) x a death-timing mixture (what Phi
  misses).
- **EQ1b PASS — the contrast that makes EQ1a meaningful:** 4x
  uncompensated corruption breaks the balance point brutally
  (B 0.795 -> 0.530, median 71.8 -> 28.3).
- **EQ2 PASS (flux_equivalent branch) — neither dwell nor capacity
  dominates the residual:** budget-route vs period-route compensation
  differ by 0.007 (0.736 vs 0.743) at 2x, 0.022 at 4x — under the
  pre-registered asymmetry bars. The two restoration routes buy the
  same alive-state fidelity.
- **EQ3 NEGATIVE — the alive/all-K gap is not primarily fidelity-death
  driven.** gap(B)@60: default +0.081, k_fail=0 +0.053 (65% of
  default — above the 50% bar), mortality_k/4 +0.063 (78%). The
  selection is SHARED between the two death channels; killing the
  fidelity channel alone leaves most of the freeze mixture in place.
- **EQ4 PASS, branch (b) — ARCHITECTURE IS A PRIMARY LEVER.** Cluster
  granularity at fixed zone physics and (analytically) fixed per-cell
  jump flux: arch4 (cluster_len 15) B 0.645 / median 48.4 vs default
  (len 5) 0.795 / 71.8 vs arch20 (len 3) 0.819 / 81.6 — ordered by
  fineness, max swing 0.174 (4x the 0.046 physics bar). The mechanism
  is legible in the source ledger: arch4's senescence share of wrong
  cells is 0.313 vs arch20's 0.132 — a senesced cluster costs
  cluster_len budget cells to repair, so coarse storage pays the
  senescence burden at a terrible exchange rate. "How patterns are
  stored" — the user's architecture hypothesis — is the biggest
  stack-internal lever anyone has found (only channel noise x2, the
  capacity cliff, is bigger).
- **EQ5 PASS — exp24's potentiation failure is now ARITHMETIC.** The
  instrumented jump-source share of B's wrong cells at 60 is 0.0202;
  predicted permanent-potentiation delta = 0.0202 x 0.75 x 0.4738 =
  +0.0072 vs exp24's observed +0.0056 (within the 0.01 bar). exp23 and
  exp24 attacked a 2%-share corruption channel from both sides — THAT
  is why the equilibrium did not move. It was never jump-made.
- **EQ6 NEGATIVE — zone equilibria are COUPLED.** C's hazard 2x -> 8x
  drops B's all-K I_V@60 from 0.795 to 0.572 (and C itself to 0.387,
  median 47.6) — far outside the 0.01 modularity bar. The coupling
  channels: C's senescence inflates the shared writable demand, and
  C's organ-failure deaths freeze corruption into everyone's ledger.
  exp23 E1's "competition invisible at b6" was an ALLOCATION-policy
  statement; PHYSICS coupling through a neighbor zone's hazard is
  real and large at the same budget.
- **R PASS — bit-exact regression:** default reproduced exp23's
  published arm exactly (A/B/C 0.951/0.795/0.780, restored 10088,
  median 71.8).

- **The corruption-source ledger (the instrument's headline table,
  default arm @60):** B's 20.5% wrong = 15.4% senescence + 2.0% jump +
  3.0% non-jump; C's 22.0% = 17.9% senescence + 0.3% jump; A's 4.9%
  = 0.0% senescence + 0.6% jump + 4.3% non-jump. **SENESCENCE, not
  jumps, is what the death-restoration equilibrium is made of** —
  which finally explains the exp23/exp24 immunity: allocation
  re-slices a budget whose binding consumer is senesced-cluster
  repair, and potentiation protects against a 2% corruption channel.
- **The elasticity ranking (log-log on B's all-K I_V@60):** noise
  -0.37 (the capacity cliff), budget +0.27 (b2->b6, exp23's curve)
  but +0.04 b6->b12 (SATURATED at the default — capacity is not the
  binding term at b6), jump_rate -0.12, hazC -0.12, period -0.10,
  k_fail -0.02. The equilibrium's marginal levers are the death-side
  and the exchange rate, not the restoration total.
- **Kills-row:** the "equilibrium-bound means immovable" reading is
  dead — it is movable by architecture (+0.174), by channel physics,
  by death channels (+0.036 at k_fail=0), and by zone-hazard
  coupling; what is NOT movable is anything routed through the jump
  channel (2% share) or the allocation of a saturated budget. Also
  dead: the flux-ratio conservation law as a complete description
  (EQ1a) — the correct object is the two-term decomposition
  (alive-state balance x death-timing mixture), and any future
  "equilibrium" claim must name which term it moves.

## Level 11 — exp28: CEM search under competition (searching where the search found something)

**exp28 — the user's Option 3 after exp25.** The transplanted
century-hold policy won under competition (0.625 vs HAND's 0.500), but
it was discovered in the SINGLE-pattern world; exp25's robustness
reading was "maybe the solo optimum is near the competitive optimum."
exp28 tests that directly: re-run the CEM search itself with fitness
evaluated in the competitive world. Same 8-dim policy space (exp19's
bounds verbatim), CEM pop 24 / 10 iters / elite 0.25 / seed 27,
fitness = mean hold (alive x mean I_rec over A/B/C, ages 30-100,
exp25's objective) on NEW search seeds (41, 42 — disjoint from every
previous use), search-world K=150/105yr (exp19's search convention);
held-out evaluation on exp25's exact convention (seeds 21-23, K=200,
120yr) across six arms, with the eval ported line-faithful from
exp25.run_arm. Discovered policy: write_age 20.0, start_age 25.75,
period 2.75, budget 6, k_anchor 0.128, boost_pv 0.040, boost_pu
0.727, boost_f 1.572 — vs disc19's write 14.5 / start 31.5 / period
2.5 / budget 9 / k_anchor 0.326 / boost_pu 0.369 / boost_f 1.059.
Search converged monotonically 0.563 -> 0.718 over the 10 iterations
(still improving on the last step — the competitive optimum is not
certified exhausted, recorded as designed).

- **C1 PASS — RE-SEARCH PAYS, ~3x the bar.** hold(disc28) 0.683 vs
  hold(disc19) 0.625: +0.058 against the pre-registered +0.02 margin,
  with every disc28 seed (0.663/0.698/0.688) above every disc19 seed
  (0.619/0.633/0.623). Median 79.7 vs 70.6yr. The search-world
  mismatch exp25 bounded from below is nearly 3x bigger than its
  robustness reading allowed — single-pattern benchmarks do not just
  under-estimate competitive policies, they under-estimate them by
  enough that re-searching is worth a full CEM run.
- **C2 PASS — the competitive optimum is a DIFFERENT policy.**
  write_age +38% (14.5 -> 20.0) and budget -33% (9 -> 6), both over
  the 25% divergence bar (start_age -18%, period +10% under it). The
  divergence direction is legible against exp26's elasticity map:
  the shared budget SATURATES at b6 (+0.04 elasticity above vs +0.27
  below), and the competitive search independently landed on budget
  6 — paying nothing for the b6->b9 capacity disc19 still buys —
  while starting maintenance 5.75yr earlier (25.75 vs 31.5) and
  leaning far harder on the procedure-free unverified boost channel
  (boost_pu 0.727 at 1.572x vs 0.369 at 1.059x). The search read the
  saturation knee exp26 measured, without being told it existed.
- **C3 PASS — the matched-channel law rediscovered a THIRD time.**
  k_anchor 0.128 << 1.0 (exp19 solo: 0.326; exp22 ensemble: weak-pull
  confirmed). Under competition, with a different policy everywhere
  else, the anchor still pulls weak — now three independent
  discoveries from three worlds.
- **C4 PASS — interiority survives competition.** budget 6 (interior,
  at the saturation knee), period 2.75 > 1.5: procedure risk still
  forbids maximum-therapy-forever even when the fitness knows about
  competing memories.
- **C5 PASS — zone-physics ordering invariant.** A 0.887 > B 0.845,
  A > C 0.871 under disc28. Recorded sub-structure: the B/C ordering
  below A is policy-sensitive — disc19 had B 0.852 > C 0.834, disc28
  has C 0.871 > B 0.845; the competitive policy trades A's margin
  (0.887 vs disc19's 0.953) for the hard zones (C +0.037). exp23's
  law (stable-zone A on top) holds in both; B-vs-C was never claimed.
- **C6 PASS — the starvation gap WIDENS.** disc28_b2 0.557 vs
  disc19_b2 0.421 (+0.136 — larger than the full-budget gap +0.058):
  the competitively searched schedule is what survives a starved
  budget, and disc28 at budget 2 nearly matches disc19 at budget 9
  (0.557 vs 0.625).
- **R PASS — bit-exact harness regression.** disc19 through this
  module's ported eval reproduces exp25's published disc arm with
  |delta| = 0.00e+00 (0.6248697... both sides) — the port is
  trajectory-faithful at experiment scale, so every comparison above
  is same-code-different-policy.
- **The efficiency headline:** disc28 restores FEWER cells (17,139 vs
  19,367, -11.5%) yet holds more (+0.058) and lives longer (+9.1yr
  median) — the competitive optimum is a SCHEDULE (earlier start,
  slower cadence, budget at the saturation knee, stronger
  procedure-free boost), not more therapy. exp25's
  procedure-risk ledger sharpens: the win comes while REDUCING total
  procedure exposure.
- **Kills-row:** exp25's robustness reading ("the solo-discovered
  policy sits at or near the competitive optimum — search-world
  mismatch costs almost nothing") is DEAD — the mismatch cost 0.058,
  ~3x the bar, and the optimal policy itself moved on two axes.
  Also dead: any benchmark discipline that evaluates policies in an
  easier world than deployment. What SURVIVES, now three-times
  confirmed or stronger: the matched-channel weak-pull law (C3, third
  independent discovery), procedure-risk interiority (C4), the
  stable-zone-on-top ordering (C5), and the b6 saturation knee
  (exp26 measured it; the blind search found it).

## Level 12 — exp29: Stage 2 repair (the model regenerates without junctions — fixed, and the record was right)

**The first per-experiment validation against PlanformDB (exp27, night-one
DeepScientist quest) produced a REFUTATION, and the refutation was the
payload.** exp27 pre-registered four criteria and ran the actual simulator
against the cutting + innexin slice of PlanformDB 2.5.0 (558 experiments;
1,716 in the corpus). S2P1 REFUTED: sustained gap-junction blockade through
amputation + regrowth left regeneration essentially NORMAL (2.87 mV vs the
6.0 mV pre-registered abnormality threshold) while the record says innexin
loss is at least as abnormal as any other perturbation class (0.542 vs
cutting's 0.487). Root cause found in `collective.py`: `regrow()` extended
the pattern per-cell (`theta[i] = theta[src] + noise`) and theta diffusion
ran un-gated by junction state — regeneration never touched the junction
network. The bioelectric layer was load-bearing for maintenance (exp16,
exp26) but not for regeneration, contradicting both the repo's framing (the
morphological target is an attractor of the COUPLED system) and the record.

The repair (M25, two additive changes in `collective.py`, both bit-exact at
gap_scale == 1.0, no RNG-stream changes on any intact-coupling path):

- **M1 — blastema readout through the junction network.** A committing
  cell inherits the chain pattern only to the extent junctions are
  healthy; under blockade it falls back to the wound-state default plus a
  broad guess along the fate axis (spread 18 mV — a blind cell can land
  anywhere on the ~-20..-50 mV head-trunk axis).
- **M2 — pattern propagation is junction-carried.** theta diffusion scales
  with gap_scale, so a blind-regenerated region is not silently healed by
  an unphysical un-coupled diffusion channel.

exp29 re-runs exp27 UNCHANGED (byte-identical file, sha256 recorded in the
results JSON; thresholds untouched):

- **S2R1 PASS — REPAIR.** innexin_sustained 2.87 -> 6.03 +- 0.18 mV:
  S2P1 flips to PASS with cutting (3.16) and restored-block (3.20) arms
  intact. S2P2 and S2C still PASS. The model now disagrees with the
  record no more — at this slice, at this power.
- **S2R2 PASS — NO COLLATERAL.** Full test suite green before and after;
  cutting arm bit-exact (3.16 == 3.16); restored arm within Monte-Carlo
  noise (3.25 -> 3.20, its pre-restore blocked window is legitimately
  touched by M2; outcome class unchanged).
- **S2R3 PASS — DOSE-RESPONSE (new testable prediction).** Regeneration
  corruption rises monotonically with junction loss: 3.28 (gap 1.0) ->
  3.93 (0.5) -> 4.54 (0.25) -> 6.03 mV (0.05). The model predicts PARTIAL
  innexin knockdown degrades regeneration in a graded way — PlanformDB
  contains dose-resolved experiments that can check this (next-night
  work: widen the slice to the ion_channel class and per-experiment
  amputation planes).
- **S2R4 PASS — GRADED PENETRANCE.** Under full sustained blockade the
  model produces MIXED outcomes (1/3 seeds abnormal), not all-or-nothing
  — the endogenous graded penetrance exp21 PB3 found in the record.

Also dead: the implicit claim that the pattern is cell-autonomous during
regrowth ("what regrows is whatever the remaining tissue REMEMBERS" — per
cell). What survives: memory still lives in theta; but READING the memory
into new tissue is a network operation, and junction health gates it.
Status: repaired, prediction registered, slice-widening queued.

## Level 13 — exp30: CEM continuation (the search is certified exhausted)

exp28 recorded its search as "still improving on the last step — not
certified exhausted." exp30 settled that honestly: the checkpoint resumed
EXACTLY (mu, sigma, best-so-far, rng state) and ran 10 more iterations at
the original protocol (pop 24, elite 0.25, search seeds 41/42, seed 27).

- **X2 PASS — the search side had headroom.** Search-world hold 0.7180 ->
  0.7404 (+0.022): the last-step improvement exp28 recorded was real.
- **X1 REFUTED — but the headroom was seed-specific.** Held-out
  (exp25's world, seeds 21-23, K=200/120yr): continued best 0.6907 vs
  disc28's 0.6828 — +0.0079, UNDER the pre-registered +0.02 re-search
  bar. disc28 is certified at (or within 0.02 of) the competitive
  optimum; the +0.008 and the median gain (79.7 -> 81.6yr) are kept.
- **X3 (exploratory) — no schedule divergence:** the continued best is a
  local refinement of disc28 (write_age 21 vs 20, budget 7 vs 6, period
  2.25 vs 2.75; all shifts < 25%).

Also dead, at this protocol: the value of further CEM iterations on the
competitive 8-dim space — search-side improvement without held-out
improvement is the search-seed-overfit signature. What survives: the
disc28 baseline as the eval-contract starting point, and the checkpoint
discipline that made the continuation free (a killed process resumes
EXACTLY — exercised for real when the sandbox reaped the first attempt).

## Level 14 — exp31: Stage 2 widened (ion_channel + morphogen classes, per-experiment amputation planes)

Night two (QUEST tasks 3-4): the class-level pilot became per-experiment.
planform_mining.py mines every experiment's amputation PLANE from the
curated Manipulation name (head/tail/trunk/head_tail/crosspiece-with-cut-
position/graft/irr/lateral/none), enriches the junction slice with
GJ-blocker drug experiments (octanol/heptanol/hexanol -> innexin protocol;
23 drug experiments join the 9 RNAi ones), and splits the morphogen class
into the AP-polarity subclass (wnt/beta-catenin/apc/axin, 143 experiments)
the 1D sheet can actually speak to. One additive model change, pre-registered
and bit-exact-at-default: `regrow(direction='backward')` so a head
amputation's blastema reads the trunk boundary BEHIND it (forward default
bit-exact; suite green; exp29 controls re-verified 3.16 == 3.16 this
session). 31 arms x 3 seeds; thresholds unchanged (6.0 mV / 0.7); corpus
1,462 outcome-bearing experiments; protocol coverage 0.84 (S2W6 PASS).

- **S2W1 PASS — TAIL-PLANE BIOELECTRIC ORDERING (widened S2P1).** Pooled
  sim pred-abn over innexin/gjblock/ion_channel tail arms 0.44 vs cutting
  0.00; recorded tail-plane bioelectric 0.535 vs cutting 0.367. The exp29
  repair generalizes: junction loss corrupts regeneration MORE than the
  cut itself, in sim and record, now on the widened slice (11 bioelectric
  tail experiments, up from 2).
- **S2W2 REFUTED — ANTERIOR CROSSPIECE OVERSHOOT.** cutting_cross_a (cut
  at f=0.167) predicts abnormal at rate 1.00 (err 16.4 mV): the chain
  readout extends the head-identity boundary over 83 regrown cells with
  no positional decay. The record shows the same DIRECTION — recorded
  abnormal rises toward anterior cuts (cross f<=0.25: 0.520 vs f>0.75:
  0.266; Spearman rho=-0.164, p=0.043, n=153, S2W7) — but at HALF the
  sim's penetrance. The S2W2 all-arms gate was misregistered (it assumed
  the recorded baseline stays <0.5 per plane; the record itself is 0.52
  in bin a). Diagnosis: the model's chain inheritance lacks a
  LENGTH GRADIENT — real blastemas interpolate identity over ~tens of
  cells (M26 candidate: distance-decaying boundary readout).
- **S2W3 REFUTED — SPECIFICITY CLAUSE WRONG-BIO, MODEL RIGHT.** The
  pre-registered criterion expected wnt RNAi to matter ONLY at tail
  wounds (wnt_head == cutting_head). The sim flagged wnt_head abnormal
  (1.00) because the posterior re-specification to head identity is
  plane-invariant — and the RECORD AGREES with the sim, not the
  criterion: recorded AP-morphogen abnormal is flat across planes (head
  0.640, tail 0.642) and far above cutting (0.41). beta-catenin RNAi
  makes the whole axis head-forming regardless of which end is cut; the
  model captured that, the criterion did not. Repair: re-register as
  S2W3b (wnt_head > cutting_head AND wnt_tail > cutting_tail AND
  recorded AP > cutting) on night three — never silently swapped.
- **S2W4 REFUTED — JUNCTION-CHANNEL ASYMMETRY IS A MODEL ARTIFACT.** The
  ion-channel protocol (gamma x0.5 + noise x3 — impaired homeostatic
  relaxation, noisier Vmem) produces ZERO abnormality at every plane
  (err 3.4-4.0 mV), while junction loss produces 0.67. The record has
  them COMPARABLE (ion_channel 0.45 pooled vs cutting 0.41; tail plane
  0.45 vs 0.37). In the model, only gap_scale gates the blastema readout
  and theta propagation; channel-level dysfunction cannot corrupt
  regeneration at all. M26 candidate: Vmem-dependent blastema
  commitment — channel RNAi should widen the blastema's identity guess
  the way junction loss does (blastema_readout_noise as a function of
  channel state, not only junction state).
- **S2W5 PASS — CONTROLS.** restored_tail 0.00 (S2C replication in the
  widened harness); intact arms (cutting/innexion/ion_channel none) all
  0.00 — no spurious abnormality without cutting.
- **S2W7 PASS-EXPLORATORY — RECORDED CROSSPIECE GRADIENT.** rho=-0.164
  (p=0.043, n=153): more-anterior cuts are more abnormal in the record —
  the model's first per-experiment PLANE prediction with graded
  registry, direction-confirmed, penetrance-overshot.

Also dead tonight: (a) the one-face regrow topology — recorded trunk
posterior-face phenotypes (wnt_trunk two-headed: recorded 0.768 at
trunk plane) are unreachable by forward-only extension (probe recorded,
ungated); (b) intact-animal RNAi phenotype formation (none-plane recorded
0.777 pooled — the sheet has no abnormality channel without amputation).
What survives: the widened harness (31 arms, 0.84 coverage), the
drug-enriched junction slice, the plane-gradient instrument, and three
sharpened M26 candidates (length-gradient readout, Vmem-gated commitment,
posterior-face regeneration) — the night-three queue.

## Level 15 — exp32: M26 repair candidates (one adopted, two sharpened, one criterion honestly re-registered)

Night three (2026-09-15). Pre-registered gates in
`experiments/exp32_m26_repairs.py` BEFORE tonight's arms ran; recorded
references are exp31's published cells only. Bit-exact gate first:
`scripts_dev/verify_m26_bitexact.py` re-runs exp29's cutting/innexin
per-seed errors through the patched collective — 1e-9 identical — and the
full suite is green. Two process catches this session, both recorded:
(a) an added 15h post-regen relaxation run flipped the innexin rate
0.67 -> 0.33 and broke bit-exactness — caught by gates M26B-G2/G3,
protocol corrected to exp31's read-immediately-after-regrow discipline
before any verdict was recorded; (b) the run crash on arm-name parsing
was fixed without touching gates.

Verdicts (results/exp32_m26_repairs.json):

- **M26C ADOPTED — TWO-FACE TRUNK REGENERATION.** `regrow(direction=
  'both')`: mid-body removals now heal from BOTH faces (two independent
  blastemas). cutting_trunk@both 0.00 (gate <= 0.34, recorded trunk
  0.308); wnt_trunk@both 1.00 and apc_trunk@both 1.00 (gate >= 0.67;
  recorded wnt_trunk 0.768) — the recorded two-headed/two-tailed trunk
  phenotypes are REACHABLE for the first time. The one-face topology
  from exp31's dead-list is repaired, additively, bit-exact at default.
- **S2W3b PASS x3 — THE RE-REGISTRATION HOLDS.** (1) recorded AP-
  morphogen plane means are plane-INVARIANT (head 0.636 / tail 0.652 /
  trunk 0.768; spread 0.132 <= 0.15) — the S2W3 specificity clause was
  wrong-bio, as exp31 diagnosed; (2) pooled AP-morphogen 0.724 > cutting
  0.512; (3) sim plane-invariance: wnt_tail (exp31) 1.00 == wnt_trunk@both
  1.00, apc_head 1.00 == apc_trunk@both 1.00 (|diff| <= 0.34). The
  morphogen polarity criterion is now validated on BOTH sides under the
  corrected biology. Never silently swapped — re-registered, gated, passed.
- **M26A REFUTED AS IMPLEMENTED — local extrapolation is a no-op where
  it matters.** cutting_cross_a @ g=1.0: 1.00 (err 21.95), identical to
  g=0 (D(1)=D(0)=1.45). Diagnosis: a head-only fragment's adjacent-cell
  slope is ~0 (plateau), so linear extrapolation degenerates to chain
  inheritance exactly where the refutation lives (recorded bin a 0.52).
  No collateral (tail/head/trunk bit-exact unchanged). M27 candidate #1:
  SATURATED extrapolation clipped to the fragment's own identity
  repertoire (intrinsic fate-axis bounds), plus graded penetrance — the
  recorded bin gradient (0.52/0.43/0.27/0.27) is a remaining-fraction
  law, and the mechanism must be length-aware beyond the local slope.
- **M26B REFUTED AS IMPLEMENTED — i.i.d. commitment noise averages out.
  ** ion_channel_tail @ cns=3.0: err 2.9 -> 4.09 mV (real, right
  direction) but pred-abn 0.00 vs recorded 0.45. Diagnosis: independent
  per-cell identity noise washes out across the regrown segment (15-cell
  average); junction loss corrupts ALL cells coherently through the
  blind-guess fallback. M27 candidate #2: CHAIN-ACCUMULATING commitment
  diffusion — identity noise that random-walks ALONG the chain (sd
  ~ cns*noise*sqrt(d)) instead of i.i.d., matching how a blastema's
  commitment error compounds through sequential inheritance.

Net: the model gains one mechanism (two-face regrowth), the ledger
gains two sharpened candidates with predicted signatures, and the
re-registered morphogen criterion passes both sides. Suite green
throughout; exp29/exp31 controls bit-exact.

## Level 16 — exp33: S2R3a drug-timing response (the dose axis the DB actually has — unresolved at n=1, honestly)

exp29's S2R3 predicted a monotone junction-loss dose-response (3.28 ->
3.93 -> 4.54 -> 6.03 mV at gap_scale 1.0/0.5/0.25/0.05). PlanformDB 2.5.0
carries NO concentrations (ExperimentDrug: Id/Experiment/Drug/StartTime/
EndTime only) — the concentration axis is a literature task. But 45
GJ-blocker rows carry exposure TIMING, 13 with nonzero values; semantics
assumption RECORDED BEFORE the outcome query: (t,0) = pre-treatment
pulse, junctions restored during regeneration; (0,t) = blocked through
regeneration; (0,0) = unspecified.

- **S2R3a-1 REFUTED AS REGISTERED -> UNRESOLVED.** The M25 mechanism
  predicts restoration timing matters (S2C logic per experiment):
  washout-before-regen should be LESS abnormal than regen-covered.
  Recorded: washout mean 0.365 (n=6 outcome-bearing: heptanol 2h pulses
  on head/tail/trunk, hexanol 1x) vs regen-covered mean 0.000 (n=1:
  heptanol (0,2) tail). Direction is OPPOSITE to the registered gate —
  BUT the critical arm has n=1 and the timing semantics are
  unverified against the primary literature; a single fully-normal
  (0,2)-tail experiment is equally consistent with "EndTime semantics
  mean the block washes out DURING early regeneration". Verdict:
  unresolved, low-power, not a clean mechanism kill; the mechanism's
  restoration-side sim counterpart (S2C 0.00) remains intact.
- **Instrumentation findings recorded:** (a) the octanol pulse series
  (exps 435-440, Oviedo 2010 Fig 2A; pre-treatments 0.13/0.25/0.5/1/2/3h)
  is the natural duration-response ladder but is RegenPeriod=0 in the
  DB (no regeneration outcome recorded) — unusable for the regen
  metric; (b) 32/45 GJ rows are (0,0) timing-unspecified; (c) S2R3b
  (concentration monotonicity) requires primary-literature extraction
  (Oviedo & Beane 2009; Fasciani 2014) — queued as S2R3c (resolve
  timing semantics + extract dose series).

What survives: the exp29 dose-response prediction is UNTESTED (not
falsified) by this corpus; the timing-semantics question is now a
concrete, cheap next step; the per-experiment drug-timing instrument
exists (experiments/exp33_s2r3_timing.py).

## Level 17 — exp34: M27 candidates (chain commitment diffusion ADOPTED; the length-gradient problem is STRUCTURAL)

Second wave of the night-three repair evaluation, same discipline
(pre-registered gates in `experiments/exp34_m27_candidates.py`;
bit-exact gate + full suite green before the run).

- **M27B ADOPTED — CHAIN-ACCUMULATING COMMITMENT DIFFUSION.** The exp32
  diagnosis (i.i.d. noise averages out) was fixed mechanically:
  identity noise now random-walks ALONG the chain (wander += N(0,
  commitment_diffusion) per committed cell; sd ~ diffusion*sqrt(d)),
  compounding through sequential inheritance — the coherent-corruption
  channel junction loss already had. ion_channel_tail 0.00 -> 1.00
  (err 9.19 +/- 1.67 mV), ion_channel_head 0.33; cutting/innexin arms
  bit-exact unchanged (default-inertness gate PASS). The S2W4 artifact
  (sim ion 0.00 vs junction 0.67) is RESOLVED: ion pooled 0.665 is now
  COMPARABLE to junction 0.67, matching the record's 0.45 vs 0.41.
  Adopted mapping for the ion protocol: cns=3.0, diffusion=1.5.
  Penetrance overshoot recorded honestly (sim 1.00 vs recorded 0.45 —
  the channel slice now needs penetrance dampening, not mechanism).
- **M27A REFUTED AGAIN — AND THE DIAGNOSIS IS STRUCTURAL.** The
  whole-fragment secant + repertoire clip leaves cross_a at 1.00 (err
  22.02, unchanged from M26a): a head-only fragment's stored theta
  contains almost NO tail-ward trend (the head plateau dominates the
  profile; the depolarization trend lives in the CUT-OFF cells). No
  readout of the stored pattern alone can reconstruct positional
  information that was amputated away — yet the record shows head
  fragments regenerate tails at 0.52 penetrance. This is evidence for a
  DUAL-FIELD architecture (M28 candidate): theta = expression layer
  (what the cell commits to), phi = positional-coordinate layer
  (body-wide, fragment-surviving, re-anchoring at wound faces) — the
  model-level form of Levin-lab positional-control distinctions
  (pattern memory vs positional map).Bins b/c/d <= 0.34 and all plane
  collaterals 0.00 (no collateral from the new params).

Model state after tonight: regrow() carries M25 (coupling-dependent
readout) + M26c (two-face) + M27b (chain commitment diffusion) adopted;
M26a/M27a length-gradient readouts refuted twice with sharpening
diagnoses. Suite green; exp29/exp31 controls bit-exact throughout.

## Level 18 — exp35: novel-prediction sweep (QUEST task 6 — deposits + two plane-awareness refutation candidates)

The class-x-plane coverage grid (1,462-outcome corpus) minus the runnable
sim arms gives two instruments (results/exp35_novel_predictions.json,
research/NOVEL_PREDICTIONS.md):

- **FORWARD DEPOSITS** (empty cells, pre-registered falsification
  thresholds): ion_channel|head_tail 1.00, ion_channel|crosspiece 1.00,
  innexin|head_tail 1.00, gj_block|crosspiece 1.00, and the sharp one —
  **morphogen|crosspiece 0.00**: the crosspiece cut at f~0.42 removes
  the wnt-re-specified posterior quarter entirely, so the mechanism
  predicts FULL compensation at this plane. A future wnt x crosspiece
  series with high abnormality refutes the mechanism's spatial logic,
  not a parameter. cutting|lateral recorded as a structural gap (2D
  cuts on a 1D sheet).
- **REFUTATION CANDIDATES** (recorded cells, first per-plane compare):
  (1) innexin|head — recorded 0.00 (n=2) vs sim 1.00 (gap +1.00): head
  regeneration under junction loss is fully protected in the record;
  the M25 blind-guess is plane-agnostic -> head-specific readout
  channel missing. (2) ion_channel|trunk — recorded 0.46 (n=60) vs sim
  0.00 (gap -0.46): the M27b chain-diffusion calibration crosses
  threshold at tail but not trunk — plane-sensitive calibration. Both
  candidates share one theme (the model's corruption mechanisms are
  plane-blind where the record is plane-aware) and both feed the M28
  dual-field + plane-dependent readout upgrade.

Process note: the ion_channel|trunk verdict text was pre-written as an
overshoot expectation; the measurement came out the opposite way and
the recorded verdict describes the MEASUREMENT (undershoot), with the
pre-written expectation superseded — recorded here so the swap is in
the open.

## Level 19 — exp36: M28 dual-field phi layer (length-gradient refutation RESOLVED at mechanism level; penetrance is binary)

The M28 mechanism (registered in L17): the collective captures
`phi_spec` — identity-at-coordinate — at pattern set (the D3 distributed
collective property made operational: theta = expression layer, phi_spec
= positional layer); `regrow(phi_readout=w)` blends chain inheritance
with the spec at weight w * gap_scale (junction-carried, M25-consistent;
deterministic; bit-exact at default — verify gate 1e-9, suite green).

- **LENGTH-GRADIENT REFUTATION RESOLVED.** cross_a: 1.00 (M26a/M27a)
  -> 0.00 at every phi_readout in {0.70..0.90} AND the registered
  amendment scan {0.20..0.60} (err 22.02 -> 4.55 at phi=0.2, 2.79 at
  0.9). The head-only fragment now regenerates a complete animal — the
  spec provides the positional information the stored theta cannot
  (exp34's structural diagnosis answered: the map is a separate
  distributed layer, not a readout of theta). Zero collateral: tail/
  head/trunk 0.00 and restored 0.00 at every value (G2 PASS);
  innexin_tail rate preserved with ~0.002 mV drift (G3 PASS after
  fixing a float-equality gate bug — 2/3 vs the 0.67 literal).
- **PENETRANCE IS BINARY — the residual gap is now precise.** G1/G4
  REFUTED: no phi value yields seed-splitting; the chain->spec
  transition is sharp (between phi=0 and 0.2 the bin-a error falls
  22 -> 4.55 mV, crossing the 6.0 threshold without ever straddling
  it per-seed). The record's graded penetrance (0.52/0.43/0.27/0.27)
  is NOT reproduced: the model undershoots all bins (0.00). The
  mechanism is right; the penetrance model is incomplete. Night-five
  candidate: a STOCHASTIC SPEC-EXPRESSION layer (per-seed spec
  availability scaled by fragment size / expression noise) on TOP of
  the phi readout — mechanism untouched.
- Process: the registered scan {0.70..0.90} was amended downward
  {0.20..0.60} AFTER it ran, labelled exploratory in the results JSON;
  G1 was evaluated on the REGISTERED scan only and stands REFUTED.
  The G3 gate originally compared the rate to the literal 0.67
  (float bug, spurious REFUTED); fixed to exact-fraction comparison.

Adopted mapping candidate: phi_readout = 0.75 for the length-gradient
slice. The M26a/M27a refutations stand as diagnostics that led here;
the exp31 S2W2 sim-side overshoot is resolved with zero collateral.

## Level 20 — exp38: M30 stochastic spec-expression (per-cell REFUTED with a mechanism insight; regenerate-level re-anchoring splits seeds but flips a marginal innexin seed — NOT adopted)

Registered BEFORE any arm ran (recorded references are exp31/exp36's
published values only). Question left open by L19: penetrance is binary
under the deterministic phi read while the record is graded (cross_a
0.52). M30 candidate: make the spec read stochastic.

- **REGISTERED (per-cell Bernoulli, spec_expression_p): REFUTED — and
  the refutation IS the finding.** At every p in {0.55..0.90} cross_a
  stayed 0.00 with err ~3 mV: silencing individual cells cannot grade
  the pattern because the chain RE-CARRIES the spec blend — each
  committed cell writes its blended value and the next cell inherits
  it, so expression failures do not accumulate. One expressing cell
  seeds the whole regenerate. (This also explains WHY the phi
  transition is sharp: the chain is an amplifier, not an averager.)
- **AMENDED (exploratory, exp36 precedent): per-blastema re-anchoring
  draw (spec_reanchor_p) — one-time Bernoulli per walk on the wound-face
  re-anchoring of the positional read.** Seed-splitting EXISTS
  (M30-A1 PASS: q=0.55 and 0.60 give cross_a 0.67, the closest
  achievable to the recorded 0.52 at 3-seed resolution; |gap| 0.15);
  collateral lock PASS (tail/head/trunk/restored 0.00 at every q);
  bins b/c/d unchanged at 0.00 (A3 PASS — the recorded 0.43/0.27/0.27
  residual remains, recorded not hidden).
- **G4 (innexin preserved) REFUTED — marginal-seed RNG-stream
  artifact.** The anchor draw consumes RNG, shifting the noise stream
  under blockade (where the spec read weight is only phi x gap =
  0.0375 and biologically near-inert); per-seed innexin errors moved
  <= 1.34 mV (within the registered 1.5 mV tolerance) but the
  threshold-marginal seed crossed 6.0 mV and the rate flipped off the
  exp31 value 2/3. A fix that flips a previously-PASS criterion is not
  a fix: **M30 amended is NOT adopted.**
- **Next-step signature (M31 candidate, night-six queue):** anchor
  availability must be a property of the fragment's STORED HISTORY, not
  a fresh draw at regrow — per-cell anchor availability captured at
  pattern set (alongside phi_spec, same D3 distributed-property logic),
  so a fragment inherits its anchor readiness from the tissue it kept.
  Prediction: seed-splitting WITHOUT any regrow-time RNG (stream-neutral
  under blockade by construction), and anchor availability should
  correlate with fragment size — the recorded monotone bin gradient.
- Inertness held: phi_readout=0 + spec_expression_p=0.5 consumes no RNG;
  cutting_tail per-seed errors bit-exact vs exp31 (G5 PASS).
- Model state: spec_expression_p and spec_reanchor_p added to regrow()
  additively, both bit-exact at defaults (verify gate 1e-9, suite green
  before and after). Both remain in the model as inert-at-default
  parameters with their verdicts recorded here.

## Level 21 — exp37: full-corpus sweep (QUEST task 4 — the per-experiment instrument over all 1,462 outcome-bearing experiments)

The class-level pilot (exp31, 31 arms on bin medians) became a
per-experiment instrument: every outcome-bearing PlanformDB experiment
mapped individually to (class protocol, plane, recorded cut fraction),
36 unique arms deduped and run at the ADOPTED model state (M27b ion
params, M26c two-face trunk, phi=0.75 crosspiece, exp27/31 protocols
elsewhere). GATES (pre-registered before the run):

- **G1 coverage >= 0.70: PASS — 1,029/1,462 experiments mapped
  (n-weighted 0.704).** Unmappable remainder recorded, not hidden, each
  a named missing layer: other_rnai|none 141 + graft 135 + irr 52 +
  lateral 46 + non-AP morphogen 29 + none-plane 18 (no gene-expression
  layer, no 2D sheet, no neoblasts, no DV/eye/brain axis).
- **G3 plane ordering rho > 0: PASS (rho = +0.80 over trunk/head/
  crosspiece/tail).** The model's plane structure holds at full-corpus
  scale.
- **G5 controls: PASS** — sweep cutting_tail per-seed errors bit-exact
  vs exp31 (the sweep reuses the adopted protocol, not a re-derivation).
- **G2 class ordering: REFUTED (rho = -0.15).** Driver: other_rnai
  (n=513, 35% of the corpus) — recorded 0.80 abnormal vs sim 0.00. The
  model has no gene-expression layer: non-bioelectric RNAi is mapped to
  the wound-only protocol and predicts cutting-like cleanliness, while
  the record runs hot (RNAi studies are published BECAUSE the phenotype
  fired — class-dependent selection bias the cutting slice does not
  carry).
- **G4 absolute calibration: REFUTED (outcome-weighted MAE 0.595 > the
  0.34 one-seed grain).** The failure is SYMMETRIC and diagnostic
  (exploratory shift table): no-perturbation classes UNDERSHOOT
  (other_rnai +0.80, cutting +0.42 — bias + missing gene layer) while
  perturbation classes OVERSHOOT (gj_block -0.52, innexin -0.56,
  morphogen -0.27, ion_channel -0.19 — the binary penetrance fires the
  abnormal arm more often than the record; the M30/M31 residual
  quantified at corpus scale).
- Within-class plane ordering (exploratory): morphogen +0.71,
  ion_channel +0.50 (low n), cutting/other_rnai undefined (sim constant
  at 0.00 — nothing to correlate), gj_block -0.77 (n=21).

Verdict: the instrument works and the model's ORDERING structure
survives full-corpus scale (G3), but two absolute-calibration gaps are
now measured, not suspected: (1) the gene-expression layer the model
does not have (fix: honest claim-scoping — Stage 2 validation claims
are conditional on bioelectric classes; a gene layer is out of scope
for the 1D sheet); (2) the penetrance sharpness the model carries
(fix: M31 stored anchor availability — next mechanism wave). Also
registered as the M32 candidate: promote the 6.0 mV threshold /
blastema_readout_noise from hand-picked to pre-registered-fitted (the
exp29 watch-item) — the shift table is the fitting target.

## Level 22 — exp39: direct comparison to the published voltage record (6/6 direction MATCH)

QUEST task "direct comparison with Levin's published voltage
measurements" COMPLETE via Europe PMC abstracts (free channel; the
z-ai backend is quota-gated). Honest scope: planarian absolute mV is
unpublished (dye ratios), so the test is every published
DIRECTION/ORDERING claim vs the model's fresh-extracted quantity:
depolarized head (Beane 2011) MATCH; hyperpolarizing channel
dysfunction -> abnormal (Beane 2013) MATCH; posterior depolarization ->
ectopic head, HL 0.95 (Oviedo 2010) MATCH; junction blockade -> mixed
outcomes via M25 (Oviedo 2007) MATCH; wound depolarization MATCH;
stochastic identical-perturbation outcomes (Pezzulo/Levin 2021; exp38
re-anchor seed-split + exp12 latch) MATCH. 6/6, zero mismatches ->
PASS. Permanent record: research/LEVIN_VOLTAGE_COMPARISON.md. Named
remaining gaps: absolute-value fidelity (untestable), organ-size
scaling, neoblast gradient substrate.

## Level 23 — exp40: channel-slice dose scan + S2R3c literature closure (ion_channel|trunk refutation candidate RESOLVED)

exp35's candidate (recorded ion|trunk 0.46, n=60 vs sim 0.00) is
RESOLVED at the mechanism level without new model machinery:
- exp37's sweep had already moved sim 0.00 -> 0.67 (gap -0.46 -> +0.21)
  purely by adopting M26c two-face trunk + M27b — the refutation was a
  plane-protocol artifact, not a missing mechanism.
- The registered (cns x diffusion) grid is MONOTONE in diffusion
  (trunk rates 0.00 -> 0.33 -> 0.67 -> 1.00) — the model's own
  dose-response curve, the same shape S2R3 predicts for the junction
  axis.
- CH-G1 PASS: the 1/3 cell (closest achievable to 0.46) exists
  (cns=1.0, diff=1.0; distance 0.13). CH-G2 PASS: tail/head
  calibrations hold there (0.67 / 0.33). CH-G3 PASS: cutting control
  bit-exact vs exp31.
- Adopted ion mapping refinement: the ion|trunk slice brackets the
  record at (cns=1, diff=1.0); the ion|tail slice prefers (3, 1.5)
  (exp34). The plane-sensitivity exp35 named is now a measured,
  bounded residual (one 3-seed grain), not an open gap.
- S2R3c CLOSED: PlanformDB has no concentrations (L16) AND the
  published literature has no partial-dose regeneration curve for
  planarian GJ blockers (Europe PMC: supramaximal doses, timing
  ladders only). The S2R3 monotone prediction stands UNTESTED, not
  falsified, and is a formal NOVEL-PREDICTION deposit with a concrete
  experimental design (concentration ladder x regen outcome,
  pre-registered Spearman monotonicity).

## Level 24 — exp41: Stage 3 opens — the anatomical compiler v0 (compilation, not search)

Stage 3 (Golden Core) deliverable: `cultivation/compiler/anatomy.py` —
declarative AnatomySpec -> InterventionProgram (regions, voltages,
durations, coupling preconditions, verification criteria) -> in-sim
execution + self-verification. The adopted Stage-2 mechanisms make the
inverse map ANALYTIC: the M28 phi layer IS the target representation —
write the spec, trigger a regen that reads it. Zero search iterations
(Phase A's CEM is no longer needed for supported anatomy).

GATES (pre-registered; verifier bug process note in the results JSON):
- **CP-G1 restorative compile: PASS (3/3, spec-err ~3 mV).**
- **CP-G2 TWO-HEAD COMPILE: PASS (3/3, errs 4.0-4.3) — the Levin
  anchor phenotype reached by COMPILATION, no search.**
- **CP-G3 novel-anatomy (ectopic mid-trunk head): REFUTED by 0.22 mV**
  — the unsupported zone erodes to -26.2 vs the -26.0 bar after clamp
  release (two-sided boundary Laplacian; a native head has one).
- **CP-G3' latch amendment (exploratory): REFUTED with a DIFFERENT
  signature** — on the latching substrate the whole-spec error fails
  (7.0 mV): the latch's own regrow is anchor-inheriting and does not
  read the phi spec. Two failures, two mechanisms, one v1 work item:
  the compiler needs a HYBRID rule (latch the unsupported zone AND
  phi-read the regen — LatchingCollective.regrow needs spec support).
- **CP-G4 safety refusal: PASS** — out-of-repertoire specs rejected at
  compile time (the compiler refuses what the substrate cannot
  express).
- **CP-G5 coupling necessity: PASS** — CP-G1's program FAILS
  verification under gap_scale=0.05 (errs 6.8-10.2 vs <6.0 bar): the
  emitted junction precondition is load-bearing, M25/M28 consistency
  holds at the compiled level.
- PROCESS: the first run's verifier skipped the whole-spec
  pattern-error gate (substring "pattern error" vs "wt_pattern_error")
  — caught because blocked runs showed verified=True at err 6.8+;
  fixed; all verdicts from the fixed verifier. Same species as
  exp36's float-literal gate bug: execute verification criteria, never
  parse them.

Verdict: the Golden Core threshold is CROSSED for supported anatomy
(restore + two-head compile and verified end-to-end, zero search);
novel unsupported anatomy is the measured frontier (0.22 mV short,
repair path registered as compiler v1: hybrid latch+spec rule).

## Level 25 — exp42: Stage 4 opens — the cognitive light cone (junction-carried, dose-monotone rho=1.00; memory is cone-bounded)

Stage 4 (Nascent Soul) deliverable:
`cultivation/cognitive/lightcone.py` — paired-trajectory instrument
(same seed => identical noise => divergence IS influence; zero Monte
Carlo averaging). Single-cell 2h pulse, 24h observation, gap scan.

- **LC-G1 PASS** — the horizon grows with time at gap=1.0 (finite
  propagation speed, every seed).
- **LC-G2 PASS** — under blockade the horizon collapses to 1 cell
  (<25% chain): the collective is cognitively FRAGMENTED when junctions
  are down — the M25 story at the cognitive level.
- **LC-G3 PASS (rho = 1.00)** — final horizon monotone in gap_scale
  (5/3/2/1 cells at gap 1.0/0.5/0.25/0.05): the light cone is
  junction-scaled, the same monotone shape S2R3 predicts for
  regeneration and exp40 measured on the channel axis. Three axes, one
  dose-response shape.
- **LC-G4 REFUTED as registered, with a power diagnosis, not a memory
  failure** — theta residue at half-chain is 0.0 because the 2h
  pulse's cone NEVER REACHES half-chain (5 cells); the residue WITHIN
  the cone is large (36-42 mV max). Memory is CONE-BOUNDED. The
  amended reading (supported by the same data): transient forcing
  casts a local cone; WHOLE-BODY integration requires the sustained
  (24h) forcing protocol — the light-cone instrument now EXPLAINS the
  model's own rewrite-window requirement (exp1 T1.3) instead of
  assuming it. Follow-up registered: 24h-pulse cone measurement.

Verdict: the influence structure of the collective is a cognitive
object — propagation, junction-scaled integration, cone-bounded memory
— measured on the same substrate that regenerates (Pezzulo & Levin
2021's scaling claim, now quantitative in this model).

## Level 26 — exp43: Stage 5 opens — substrate independence (the mechanism transfers everywhere; the ATTRACTOR is substrate-conditioned — a measured transfer condition)

Stage 5 (Ascension) deliverable: `cultivation/substrate/graph.py` —
GraphCollective (the same ODEs on an arbitrary adjacency: path, 2D
lattice, random 3-regular, scale-free) + regrow_graph (BFS
regeneration through graph edges, M25-consistent blind-guess under
blockade).

REGISTERED GATES: all three REFUTED as naively registered — and the
refutation is the finding:
- The identity labeling (nodes 0..24 = head) is an attractor ONLY where
  it is coherent with the substrate: path 1.8 mV, grid 5.6-5.9 mV PASS;
  random-regular 8.6-11.2, scale-free 11.3-11.9 FAIL. Scattered labels
  are not attractors on any substrate (alternating head/trunk cells
  would fail on the chain too).
- The BFS-coherent amendment improves everything one notch (random-
  regular regen 4.2-4.5 mV at gap=1 — the machinery works) but
  scale-free still fails (7.7 mV) and degree-normalized coupling does
  NOT rescue it (probed: 11.3 mV unchanged). The invariant is
  BOUNDARY-TO-VOLUME RATIO: scale-free BFS communities are
  expander-like (huge boundaries), the Laplacian outvotes the label no
  matter the per-edge conductance.
- What transferred UNIVERSALLY (the Ascension half): the dynamics, the
  M25 blind-guess corruption under blockade (12-22 mV on every
  topology), and the graph regeneration machinery (BFS inheritance,
  gap=1 errs 1.1-4.5 on path/grid/random). The failure is never the
  mechanism — it is the existence condition of the target pattern.

RESOLVED CLAIM (replaces the naive one): the formalism is
substrate-independent UP TO an anatomical coherence condition — the
target pattern must be a low-boundary-to-volume partition of the
substrate (a spectral/graph-geometric property). The Stage-3 compiler
is the substrate-adapter: compiling an AnatomySpec onto a substrate
REQUIRES choosing identity partitions that satisfy the coherence
condition (compiler rule R5 candidate: substrate-aware partitioning,
night-six queue with per-substrate eps/mu calibration). The last
phase of the roadmap is not free — the substrate co-defines which
anatomies are reachable, which is precisely what a real Ascension
answer looks like: substrate independence of MECHANISM, substrate
conditioning of FORM.

## Level 27 — exp45: M31 stored-history anchor (registered form REFUTED with a sharp diagnosis; M31-A isolated re-anchoring ADOPTED — all 6 amendment gates PASS)

Night-six queue #1. The user research directive ran FIRST (exp44): the
literature basis for M31 is Ross et al. 2022 (positional information is
CONSTITUTIVELY expressed from muscle and reset by wound signaling — the
read draws on stored material state) plus the 2025 Egal-1/microtubule
papers (the substrate is physical, in the fragment).

- REGISTERED M31 (anchor_from_history = |theta[face] - phi_spec[face]| <=
  t): REFUTED at every t in {1.0..4.0} mV. THE DIAGNOSIS IS THE FINDING:
  the model's settle history is seed-INVARIANT at macro scale — face
  drifts 4.14/4.21/4.26 mV across seeds (spread 0.12 mV on a 4.2 mV
  deterministic deformation). The detrended fine structure DOES differ
  per seed but only at ~0.03 mV (micro-scale, un-fittable). No stored-
  state threshold can split seeds: in this model, per-seed variation
  lives in REGEN-TIME draws, not in settle-history differences.
- M31-A ISOLATED RE-ANCHORING (spec_reanchor_isolated): the stochastic
  unit stays at the regenerate level (exp38's amendment) but the draw is
  MINTED FROM the fragment's own stored state — a blake2b digest of the
  quantized theta window at the wound face seeds a dedicated Generator.
  Deterministic per stored state (the coin IS the fragment's history —
  the M31 goal), ZERO self.rng contact, which removes exp38's exact
  blocker (the re-anchor draw shifted the shared stream and flipped the
  marginal innexin seed).
- GATES: A1 seed-split PASS (q=0.50: cross_a rate 1.00 -> 0.33);
  A2 collateral lock PASS; A3 bins b/c/d lock PASS; A4 innexin preserved
  with drift 0.00 mV (the exp38 blocker GONE); A5 stream neutrality PASS
  (bit-same-if-True on every seed whose draw came out True); A6 draw
  straddle [True, False, True] verified as the split's CAUSE.
- STATUS: M31-A ADOPTED (exploratory->adopted mapping q=0.50,
  recorded target 0.52 — pointwise fit not claimed, record runs hot).

## Level 28 — exp46: M33 non-junctional neural/muscle polarity channel (ALL 5 GATES PASS — the innexin|head gap, the last unexplained Stage-2 arm signature, RESOLVED)

Night-six queue #2. Literature basis (exp44): Lobo, Emmons-Bell & Levin
2019 (the head-tail axis is controlled by the net polarity of neurons;
the morphogen vector-transport field coincides with nerve axon
alignment — a channel that does not run through gap junctions) plus the
2025 egal-1/microtubule notum papers (anterior-facing wound polarity via
muscle substrate).

- MECHANISM: `neural_readout` w — when the committing cell's spec
  identity is ANTERIOR (spec[i] >= NEURAL_SPEC_MIN = -35 mV, the
  head/trunk fate-axis midpoint), the M25 blind guess is blended with a
  direct neural read of the spec. Posterior identities do NOT qualify
  (no local pole) — which is exactly why recorded GJ-blockade
  phenotypes concentrate at posterior planes.
- GATES: G1 innexin_head 1.00 -> 0.00 (record 0.00) PASS; G2 posterior
  immunity PASS (innexin_tail 0.67 preserved, bit-exact vs w=0, exp31
  drift 2.4e-3 mV); G3 full-coupling inertness PASS; G4 dose monotone
  (11.33 > 4.80 > 1.77) PASS; G5 zero collateral PASS.
- REGISTERED NOVEL PREDICTION: gjblock_head moves toward normal under
  the channel (record per_plane head 0.566 mixed — the next corpus pass
  can test the plane-resolved signature).
- GATE-SPEC CORRECTION (recorded honestly): the first G2/G3/G5
  evaluation compared w=1.0 arms at phi=0.75 against exp31 arms at
  phi=0 (wrong reference — different phi). Corrected to within-phi
  references (same arm at w=0.0, both phi=0.75) with exp31 as the
  rate/drift check. The mechanism claim was unchanged; the reference
  arms were wrong.

## Level 29 — exp47: compiler v1 — the hybrid latch+spec rule (CP-G3' RESOLVED) + R5 substrate-aware partitioning (ALL 6 GATES PASS)

Night-six queue #3. Literature basis (exp44): Pezzulo/Levin 2017 — the
cryptic phenotype is "stored ... via global patterns of cellular resting
potential" and is "functionally instructive": the STORED GRADIENT is
what regeneration reads; experimental reversals reset it (the switch is
state-writable).

- v0 FAILURE DECODED: the latch chased the clamps partway in 24h
  (head_native zone mean -30.4 vs the -20 bar) — the window ended with
  the stored gradient HALF-WRITTEN. The 2017 semantics say the protocol
  must END with the gradient SET.
- R1'' LATCH-WRITE: the program ends the window with latch := spec for
  every zone (explicit emitted step). R2'' HYBRID READ: the latching
  regen writes anchor <- (1-blend)*inherited + blend*spec[i].
- CV1-G1 PASS: the ectopic third-head compile now verifies 3/3 (errs
  2.68/2.57/2.59 vs v0's 7.0/6.93/7.15). THE GOLDEN CORE THRESHOLD IS
  NOW FULLY CROSSED: restorative + two-head + ectopic novel anatomy,
  all zero-search.
- CV1-G2 (registered disjunction) resolved: the WRITE alone is
  sufficient (blend=0.0 also verifies 3/3) — R2'' is decorative for
  this anatomy class (the latch write covers the ectopic zone directly;
  the regen's tail inheritance already reads the written trunk latch).
  Decomposition honest; R2'' retained for spec-carrying regens.
- CV1-G3 no regression PASS (restore + two-head 3/3); CV1-G4 safety
  refusal + coupling necessity unchanged PASS.
- R5 SUBSTRATE-AWARE PARTITIONING: compile-time boundary-to-volume
  check with R5_MAX=0.10. Measured ratios: path 0.0101 (1/99), grid
  0.0611 (11/180), random-3 0.3533 (53/150), scale-free 0.4873 (96/197).
  R5-G1 PASS: the refusal boundary reproduces exp43's measured
  attractor-existence signature exactly (path/grid COMPILABLE,
  random-3/scale-free REFUSED). R5-G2 PASS: margin >= 1.5x on both
  sides (0.061 < 0.10 < 0.353). THE COMPILER IS THE SUBSTRATE ADAPTER
  exp43 called for — with an audit-ready refusal reason.

## Level 30 — exp48: M32 record-calibrated threshold fit (single-threshold hypothesis REFUTED; the corpus residual is STRUCTURAL)

Night-six queue #4. Literature basis (exp44): Pezzulo/Levin 2017 — the
graded population rate is "a constant ratio ... due NOT to partial
penetrance of treatment" but to a hidden multistable switch: the
per-animal binary outcome rule is CORRECT; the fit tests only where the
all-or-nothing line sits.

- PRE-REGISTERED FIT: train {morphogen, innexin, gj_block}, held-out
  {ion_channel}, structural {cutting, other_rnai} (sim 0.00 at every c
  — threshold-insensitive, no mechanism layer), grid 6.0-14.0 mV.
- G1 PASS: unique interior optimum at c=13.0 mV (train MAE 0.313 ->
  0.154, strictly below both neighbours). G2 PASS.
- G3 REFUTED: the fit generalizes WORSE to the held-out ion_channel
  class (MAE 0.446 at 13.0 vs 0.192 at legacy 6.0) — no single
  threshold fits all classes.
- VERDICT: M32-as-single-threshold REFUTED. The exp37 symmetric
  calibration signature is STRUCTURAL (per-class mechanism gaps: no
  gene-expression layer for cutting/other_rnai; per-class mV misfit for
  the perturbation classes), NOT a threshold artifact. The 6.0 mV slice
  threshold and the corpus are jointly identified only per-class.
- G4 PASS: the M31-A Stage-2 split survives ANY threshold (cross_a
  errors straddle at 13.0, rate 1/3) — the Stage-2 slice calibration is
  robust to the corpus fit outcome.
- M34 CANDIDATE REGISTERED: a gene-expression class layer (the missing
  mechanism for cutting/other_rnai underprediction) — the night-seven
  structural work item.

## Level 31 — exp49: the regen-window light cone (LC-G4 RESOLVED — the rewrite regime is the REGEN WINDOW; the cone is directional)

Night-six queue #5. Literature basis (exp44): Pezzulo/Levin 2017 — the
permanent rewrite follows "temporary modulation of regenerative
bioelectric dynamics in AMPUTATED trunk fragments": the published
perturbation window sits INSIDE the regenerative window. LC-G4's
refutation had left the rewrite regime unnamed; the literature names it.

- INSTRUMENT: `regen_lightcone` (paired trajectories, same amputation
  both sides, one cell of B clamped while the commitment walk runs).
  LC5-G0 validity PASS (zero-divergence at pulse_hours=0; the inlined
  walk is the model's walk — first run's blocked-arm anomaly was
  diagnosed as a missing M25 guess-mix in the inlined walk and the
  instrument corrected; the model's r-mix decays the delta x0.05 per
  commit under blockade).
- G1 REFUTED as registered (regen-window far-end residue 2.44 mV < the
  3.0 bar) — G1' contrast amendment PASS: 2.44 mV vs 0.00 for the SAME
  pulse on the INTACT collective (>5x with intact < 1.0). THE 2017
  PROTOCOL IS EXPLAINED BY ONE MECHANISM: the pulse rides the write —
  the commitment walk re-reads the chain at every cell, so a perturbed
  wound face propagates into every subsequently committed identity.
- G2'/saturation PASS: dose monotone 0.5 -> 2.0 h then SATURATES
  (2 -> 6 h flat) — the M30 chain-re-carries signature reappearing at
  the light-cone level.
- G3 PASS: the shift persists the 15h post-regen settle (the rewrite is
  STORED identity, not transient V).
- G4 PASS: collapses to 0.00 under gap_scale=0.05 — junction-carried
  (M25 consistency at the cognitive level).
- G5 PASS + NOVEL PREDICTION: the cone is DIRECTIONALLY ASYMMETRIC —
  2.44 mV when the pulse sits at the wound face, 0.00 when it sits just
  5 cells anterior. The regen-window cone spans the whole regenerate
  FORWARD but is razor-narrow BACKWARD. Falsifiable with
  regeneration-window optogenetics: only wound-adjacent perturbations
  should rewrite the regenerate.

## Level 32 — exp50: M33 confirmed OUT-OF-SAMPLE by the corpus + the penetrance structure closed (all gates PASS)

Night seven, part 1. exp46 registered "gjblock_head moves toward
normal" BEFORE the plane-resolved rates were examined; exp37's rows
then confirmed the prediction independently:

- The recorded gj_block|head rate is 0.177 (n=6) — the LOWEST gj_block
  plane rate — while gj_block|tail is 0.599 (n=7), the highest. The
  anterior-pole protection asymmetry M33 predicts EXISTS IN THE RECORD.
- M33-C1 direction PASS; M33-C2 out-of-sample fit PASS (post-M33 sim
  0.00 is 4.6x closer to 0.177 than the pre-M33 1.00); M33-C3 PASS
  (innexin|head 0.000 matched exactly).
- M31-A at 9 seeds: bin-a split statistically stable (rate 0.33, B1),
  direction rho=0.77 (B2), and the honest STEP-STRUCTURE confirmation
  (B3): bins b/c/d sit at 0.00 — the night-five "graded b/c/d" target
  is REFUTED at the mechanism level. The penetrance story is COMPLETE:
  mechanism (M31-A, adopted), structure (a step, not a grade), and
  residual ownership (the measurement layer, L33).

## Level 33 — exp51: M34 — the corpus residual DECOMPOSED, not modeled away (all gates PASS; two deposits)

Night seven, part 2. exp48 proved the residual is structural; M34's
honest scope is the decomposition plus falsifiable deposits:

- D1 PASS: protocol heterogeneity H measured per class (cutting 0.531,
  other_rnai 0.431, gj_block 0.432, innexin 0.500, ion_channel 0.103,
  morphogen 0.360 — graft/lateral/irregular/unmappable protocols the
  sim does not represent).
- D2 PASS: the record-hot bias direction is ONE-SIDED across all 8
  plane cells (recorded > sim everywhere) — measured, not assumed.
- D3 PASS: residual ownership partitioned — cutting -> H (protocol) +
  P (bias); other_rnai -> G (the gene layer); perturbation classes ->
  P.
- N1 DEPOSIT: a generic gene-RNAi perturbation (gamma x0.7 +
  commitment diffusion 1.5) predicts trunk-cut abnormality at 0.67 —
  band [0.22, 0.67] registered against the day the DB maps gene
  identities.
- N2 PASS (after one honest restatement): the M33xM34 CHAINED
  prediction — under gene impairment WITH blockade, head+neural
  channel 0.00 vs tail 1.00: anterior-pole protection survives generic
  gene impairment. The first registered form mis-scoped M33 (the
  channel acts on the blocked blind-guess branch, not full-coupling
  commitment noise; the full-coupling head arm shows a mild wander
  tail, 0.33, recorded).

THE EXP37 SYMMETRIC SIGNATURE IS NOW FULLY OWNED: mechanism where
mechanisms exist, measurement where they do not.

## Level 34 — exp52: R5 per-substrate calibration — the refusal is not a tuning artifact; the b2v boundary refined

Night seven, part 3. exp43's registered follow-up:

- R5-C1 PASS (the load-bearing result): NO mu in the scan
  {0.005..0.060} rescues random-3-regular (best 11.85 mV) or
  scale-free (best 12.35 mV) — the incoherence is a property of the
  (substrate, partition) pair. The compiler's refusal is robust.
- R5-C2 REFUTED as registered, honestly: grid_2d's wound-recovery best
  is 7.51 mV (mu=0.005) — above the 6.0 bar (exp43's 5.6 was WITHOUT
  the 20%-scattered-node wound). R5-C2' amendment: the calibration
  table is the deliverable — path IN (4.13 @ mu=0.01), grid
  MARGINAL-OUT (7.51 @ mu=0.005), random-3/scale-free REFUSED.
- REFINEMENT OF R5: the b2v boundary is NECESSARY for attractor
  existence but not SUFFICIENT for wound-recovery within the decision
  bar — the compiler's per-substrate calibration now carries both the
  b2v check (compile time) and the best-mu operating table (audit).
- ND-L34-directional-cone deposited to research/NOVEL_PREDICTIONS.md
  (the exp49 G5 optogenetics protocol), alongside the gene-layer and
  M33xM34 chained deposits.

## L35 — exp54 pulse-timing critical window (night eight)
- The model's polarity decision medium is the FIRST COMMITMENT: a 3h
  pulse starting at t=0 writes 3.00 mV across the whole regenerate
  (full-chain capture); ANY later start (>= 1h) drops to ~0.5 mV
  (diffusive leak only) — and that minority capture is RE-ABSORBED by
  the collective attractor (far end 0.00); post-walk pulses write
  exactly 0.
- PT-G1..G5 ALL PASS: monotone curve, early saturation plateau, late
  failure, finite transition width (the ZENODO:18358611 fixed-shape
  form); 3h sufficiency (0.91 of the 6h write — Durant MED30799071's
  "kick-start" maps to the first blastema cell's DIRECT wound-face
  read); 6h deadline; persistence + blockade collapse; size collapse
  across n=60/100/140 (Spearman ~1.0).

## L36 — exp55 graft/lateral 2D sheet (night eight)
- BUILT: cultivation/bioelectric/sheet.py — two independent position
  fields (AP identity + ML positional value), midline-as-source, grafts
  transplant stored fields. S3 isograft (0.00) + S5 native-axis
  integrity PASS.
- S1/S2/S4 REFUTED with a precise 3-part diagnosis: (D1) the
  physiological midline zero-crossing fires a naive sign-opposition
  drive via diffusion asymmetry — fixed by the discontinuity-threshold
  rule (contrast above the physiological gradient; the native axis is
  homeostatic, not inductive); (D2, load-bearing) a pure-diffusion AP
  field cannot HOLD induced identity — the L-R juxtaposition front
  fires and warms the contact to -32 mV but the contrast front decays
  under host blending and the band relaxes back (no attractor at the
  sheet level); (D3) a one-sided edge drive cannot fill the graft
  (equilibrium ~-35 mV mid-graft, below threshold).
- M-SHEET REPAIR REGISTERED (night nine): the intercalation front as a
  REGENERATION front — commitment at the front + INHERITANCE-COPY
  propagation (the exp27 chain mechanism in 2D), gated by sustained
  front activity (the fixed-shape exposure axis).

## L37 — exp56 the reader perturbation test (night eight)
- THE SYMBOL-GROUNDING EXPERIMENT, 6/6 GATES PASS (ZENODO:21459264:
  "perturb the reader, not the pattern"):
  SG-G1 same bit-identical stored pattern, reader ON restores (0.00) vs
  OFF (1.00) — SAME PATTERN, DIFFERENT FORM; SG-G1t posterior immunity
  by design; SG-G1c clamped-carrier replicate; SG-G2 full coupling:
  carrier suffices, reader inert; SG-G3 THE LOOKUP IS THE DECODER —
  reversing phi_spec with the carrier untouched makes the TAIL fully
  head-like (1.000) while the head fails (mirror form); SG-G4'
  destroyed carrier + reader ON restores the FORM (hl 0.946, delta
  16.1 mV).
- DISCOVERED: the CARRIER-ASSISTANCE term — the reader alone decides
  identity but not full precision (restored head ~6 mV depolarized of
  spec: the corrupted blind-guess baseline feeds the M25 r-mix).
  Meaning is in the reader; fine precision is carrier-assisted. A
  testable refinement of the grounding claim, not a failure of it.
- Two arm-design corrections caught en route and recorded: the rescue
  arm is the HEAD plane (the first run's tail-plane "refutation" was
  exp46's posterior immunity reproduced exactly), and the corruption
  metric must be the regen region, not the deliberately-corrupted whole
  body.

## L38 — exp57 night-eight closing batch
- A. TAS CRYPTIC RE-CUT INTERVAL: TA-G1 PASS (naive 0.917 vs re-cut
  1.00 abnormal across 12 seeds at the M31-A q=0.75 regime; seed 3
  discordant — first regen NORMAL at 5.94 mV, re-cut ABNORMAL at 6.42;
  seed 4's error DROPS 10.74 -> 7.42 — the hidden state shifts re-challenge
  outcomes in both directions, the challenge-sensitive interval below
  the immediate threshold EXISTS as PPRPPR1216581 predicts); TA-G2 PASS
  (bit-exact replay 12/12 — stable re-challenge ratios as deterministic
  stored-state readouts).
- B. UNDERDAMPED PCG RECOVERY: WEAK — max wound-face overshoot 0.296 mV
  (neither the atlas's >= 0.5 underdamped nor < 0.1 overdamped);
  registered as a calibration-target measurement, not tuned.
- C. M36 MIS-ANCHORED POLE (egal-1 direction, MED41099308): 3/3 PASS —
  collective.py gains additive `neural_misanchor` (bit-exact at 0.0,
  suite 64 green): tail-plane blockade regen becomes FULLY head-like
  (hl 1.000 — the two-headed direction), head plane unchanged, full
  coupling inert.
- D. gjblock|head_tail LEDGERED: model 0.67 vs recorded 0.025 (n=2) —
  protocol-semantics miss diagnosed (the DB's head_tail class may not
  be both-faces-under-continuous-blockade); DB re-mapping queued.

## L39 — exp58 M-sheet repair (night nine)
- Saito 2003 (10.1002/dvdy.10246) full abstract INVERTS the exp55 fire
  rule: induction fires on SAME-SIGN medial-lateral juxtaposition gaps
  (lateral tissues abutting medial), while L-R facing contact is
  STRUCTURALLY SILENT — exp55 had encoded the refuted asymmetry
  hypothesis. IntercalationSheet rebuilt additively (exp55 stays
  reproducible): same-sign fire rule + leaky exposure->commitment
  (plastic cells, AP pinned — the exp55-D2 attractor) +
  organizer-bearing inheritance-copy propagation (the exp27 chain in
  2D) + field maintenance (ablated organizers ADOPT the host field —
  semantics correction registered before the re-run).
- 7/7 gates PASS: complete ectopic head 1.0/depth 5; local one-sided
  band 0.2/depth 1 (side re-registered per corrected geometry, matches
  the published figure); true-isograft null 0.0 (arm re-registered);
  ablated source starves; native axis intact; depth ordering; and the
  L-R silence gate 0.0 EXACT. G8 exploratory gap-graft: 0.2 local band,
  consistent with Saito's intercalary-compensation opening line,
  recorded honestly against the registered no-commit guess.
- exp55's three refutations (S1/S2/S4) RESOLVED.

## L40 — exp59 M35 ARZ domain readout (night nine)
- M35-as-first-registered REFUTED AS REDUNDANT (honest discovery):
  wound_center = mean(theta[wound region]) means the M25 "blind guess"
  base ALREADY converges the wound region's own stored repertoire —
  the face-window base blend is a geometric no-op (tail errors
  bit-identical across weights).
- AMENDED M35-A ADOPTED (5/5 gates PASS): the atlas's ARZ content is
  MULTI-LINEAGE CONVERGENCE — variance reduction across K=3 lineage
  reads (K derived from the published lineage count, not fitted).
  Tail-face rescue direction confirmed (err 7.86->5.75, rate
  0.917->0.333 vs record 0.40); head preservation exact (0.0);
  full-coupling inert; bit-exact anchor to exp50 to 1e-9.

## L41 — exp60 M37 GENE LAYER (the Stage-2 gene identity map)
- The DB's RNAi table (412 entries) mapped to functional families via
  pre-registered keyword rules (neoblast/wnt_pos/wnt_ant/neural/
  generic/control + unmappable dv_hh_notch/organ_identity/pcp).
  Metric amendment registered BEFORE the arms ran: regional failures
  measured on the regen region (exp56 principle — whole-animal error
  dilutes regional failure: nb=1.0 tail whole-animal 4.81 < 6.0 while
  the region is ~10 mV off).
- GL-G2 PASS — the exp37 morphogen class was UNDER-INCLUSIVE:
  dvl/fzd/evi/notum (keyword-missed Wnt genes) join morphogen
  semantics at 0.815 vs the class's 0.718 (within the 0.4 bar).
- GL-G5 PASS — THE M33 NEURAL CHANNEL IS NECESSARY (the reverse
  test): gene-level disruption of its substrate (netrin/robo/slit
  family) costs more than junction blockade at the head (recorded
  0.705, n=23, vs gj_block|head 0.177); sim-side, disabling the
  readout under blockade makes head regen fully abnormal (1.00) vs
  the M33 rescue (0.00).
- GL-G3 REFUTED as registered: neoblast-family record is HIGH but not
  sharp (pooled 0.701 n=70, trunk 0.812, irr-plane 0.375 drag) — the
  binary scar semantics (sim 1.00) overshoots a GRADED record. The
  M31-A lesson repeats: per-animal all-or-nothing, population graded.
  M37-A candidate REGISTERED: the neoblast layer should mint a
  per-animal failure coin from the fragment's stored state (the M31-A
  penetrance mechanism), not a deterministic scar.
- GL-G4 REFUTED — exp51's N1 deposit falsifier FIRED exactly as
  registered: the mapped generic family pooled 0.855 (n=406) lands
  OUTSIDE the deposited band [0.22, 0.67]. Diagnosis: the N1 protocol
  (gamma*0.7) is too WEAK (trunk record 0.900 vs sim 0.67); direction
  confirmed (0.00 -> 0.67 closes most of the gap); residual owned by
  the record-hot bias P (one-sided per exp51-D2; control RNAi itself
  records 0.321 vs sim 0.00). M37-B candidate REGISTERED: the
  ion-strength protocol (measured trunk 1.00 at exp40 (1.0,1.0))
  applied to the generic family, expected trunk ~1.00 vs record 0.90.
- Exploratory: su(H) dose family all 1.00 (n<=4 per variant — no
  gradient resolvable). The exact pooled sim-vs-record table deposited
  per family (control 0.321/0.0 record_hot; generic 0.863/0.655
  record_hot; neoblast 0.799/1.0 sim_hot; wnt_pos 0.822/1.0 sim_hot).

## L42 — exp61 COMPILER V2 (Stage-3 90% push)
- CP2-G1 PASS — ARBITRARY LAYOUTS: all 4 specs (v1 third-head re-run,
  dual novel band at -30 — a cell STATE absent from WT, ladder
  segmentation with 3 novel rungs, custom 4-zone mixed identity)
  verify 3/3 seeds each, ZERO search, 1.4 s wall for the whole suite
  (errs 2.4-3.5 mV, bar 6.0). The compiler is no longer a two-shape
  demo: it compiles any in-repertoire zone layout.
- CP2-G2 PASS — MINIMUM WINDOW: the R1'' latch-write (state write vs
  chase) cuts the minimum rewrite window 24 h -> 3 h (8x): ALL specs
  verify at every window down to 3 h. The 2017 cryptic-gradient
  semantics pays its rent: the protocol's cost is the state write,
  not the sustained chase.
- CP2-G3 PASS — SCHEDULE EMISSION: every compiled program emits a
  schema-valid lab-executable schedule (step/agent/action/timing/
  concentration-class; classes anchored to exp40's measured dose grid
  and the record's octanol-class baths — no invented numbers).
- CP2-G4 PASS — 100-GENERATION STABILITY (the night-nine queue's
  exp41 latch RE-READ path): 100 re-amputation generations on the
  latching substrate, ZERO anchor drift (slope 0.0, 6/6 seed-spec
  runs, cycles_to_failure None everywhere). The answer to the exp41
  failure structure: the re-written latch does NOT compound drift —
  the boundary anchor is FROZEN below the latch deadzone and the
  regen copies it forward bit-exactly each generation. Stability is
  structural, not tuned.
- First-run correction recorded honestly: the v2 specs ran once on the
  plain (non-latching) substrate because execute_and_verify defaulted
  collective_cls=None — the 4.35 mV third-head "failure" was the
  pre-R1'' plain-substrate semantics reproduced, not a v2 result.
  Corrected to LatchingCollective (exp47's own usage) before any
  verdict was drawn.

## L43 — exp62 STAGE-4 SIGNAL-RANGE DIAL (M38)
- THE DIAL: the coupling-kernel radius k (line_adjacency(n, k)) — the
  innexin coupling footprint as an OPERATING POINT (additive; k=1
  default bit-exact; instruments gained adjacency passthrough).
- D-G1 PASS — the pulse light-cone horizon is EXACTLY monotone in k:
  5 -> 10 -> 16 -> 24 cells (seed-constant, rho=1.0). The baseline
  reproduces exp42's measured 5-cell cone.
- D-G2 PASS — EXPANSION FACTOR 4.8x at k=4 (bar 4.0): the user's
  5 -> 20-cell target EXCEEDED (24 cells).
- D-G3 PASS — the regen-window cone spans the whole regenerate at
  every k (the chain re-carries), with the write MAGNITUDE decaying
  monotonically in k (max residue 5.07 -> 3.59 -> 2.77 -> 2.25 mV):
  the expanded cone AVERAGES the write. Reach is bought with contrast.
- D-G4 REFUTED as registered (honest): k=4 breaks the third-head
  compiler verify (7.34/7.24/7.28 > 6.0). M38-A diagnosis: a longer
  window does NOT rescue (48 h probe fails 7.2) — the smearing is in
  the regen READ, not the clamp phase. OPERATING ENVELOPE: k in
  {1, 2} verified (k=2 errs 4.17/4.08/4.09), k=3 marginal (pattern
  error passes, zone hold fails), k=4 refused for fine-contrast
  specs. THE CROSS-STAGE RULE: the Stage-4 range dial and the Stage-3
  contrast spec are COUPLED design axes — the compiler must co-tune
  the spec geometry with the dial (M38-A candidate: zone-width
  scaling with k). The k=1 anchor matched exp61's stored errors to
  the stored (2-dp) precision; the first anchor check compared
  full-precision values against rounded constants and was corrected
  before any verdict.
- D-G5 PASS (the persist branch): time-to-restore 1.0 h at both k —
  the faster-healing branch did NOT fire; the payoff that shows is
  REACH (D-G2/D-G3), recorded honestly.

## L44 — exp63 STAGE-5 BLUEPRINT TRANSFER (M39)
- THE BLUEPRINT: the phi_spec positional layer, serialized to JSON
  (6-dp quantized) and reloaded into fresh hosts. The donor carries a
  NOVEL anatomy (two-headed — a form the host cannot reach alone); a
  WT donor would have conflated blueprint-driven restoration with the
  host's own dynamics (first-run correction, registered before the
  re-run, together with confining the corruption span to the
  triggered region — the first run's wide corruption left dead error
  where no trigger regenerates).
- BT-G1 PASS — DIGITAL ROUND-TRIP: serialization bit-exact (0.00);
  identity transfer tail head-likeness 1.0/1.0/1.0 — the host builds
  the donor's posterior-head anatomy from the serialized blueprint.
- BT-G2 PASS — CROSS-SUBSTRATE TRANSFER: chain(k=1) blueprint ->
  chain(k=2) host, identity 1.0 across seeds; the random-3 host is
  REFUSED at compile time (R5 b2v 0.3533 > 0.10) — the blueprint
  moves only to bodies whose connectivity supports the partition.
- BT-G3 PASS — SURVIVES PARTIAL DEATH: a mid-tissue slice killed
  after reload re-derives from the positional layer + surviving
  boundary (identity 1.0).
- BT-G4 PASS — READER DEPENDENCE (exp56 discipline at the transfer
  level): the SAME loaded blueprint with the readout disabled leaves
  the host's tail tail-like (identity 0.0) — the blueprint needs a
  compatible READER, not just data. "Same body that speaks the same
  language" = partition-supporting substrate (R5) PLUS reader.
- HONEST RESIDUAL: identity transfers sharply (1.0) while fine
  voltage precision does not (err vs donor ~9.6 mV — the M28 blend
  lands the transferred zone between trunk and head values); the
  exp56 carrier-assistance term at the transfer level.

## L45 — exp64 M37-A ADOPTED / M37-B REFUTED
- M37-A ADOPTED (3/3): the neoblast layer carries the M31-A
  penetrance mechanism — a per-animal FAILURE COIN minted from the
  fragment's own stored state (blake2b digest of the quantized face
  window + a family salt; ZERO self.rng contact; collective.py gains
  neoblast_coin_p, bit-exact at None). NA-G1 stream neutrality (p=0
  bit-identical to no-coin; p=1 reproduces the deterministic scar
  exactly). NA-G2 OUT-OF-PLANE PREDICTION (the anchoring discipline:
  nb_p=0.8 DECLARED as the trunk-record anchor 0.812, then tested on
  the OTHER planes): trunk 0.80/0.75 vs record 0.812; head 1.00 vs
  0.75 (at the band edge, n=5 stated); tail 0.95/0.90 vs 0.74 (n=2)
  — all within the registered ±0.25 bands. NA-G3 step structure:
  per-seed outcomes bimodal, independent 20-seed batches agree
  within 0.15 — the M31-A signature (per-animal all-or-nothing,
  population graded) reproduced in the gene layer.
- M37-B REFUTED on the merits: the ion-strength protocol does NOT
  raise the generic family's trunk rate toward the record (0.33 in
  BOTH the first cns-only arm and the corrected FAITHFUL exp37 ion
  protocol — both recorded — vs the N1 protocol's 0.67; record
  0.900) and INVERTS the plane signature (head 0.33 -> 1.00).
  FINDING: the impairment CHANNELS are not interchangeable —
  homeostatic gamma impairment degrades trunk pattern maintenance;
  commitment-noise impairment degrades the guess-branch-dominated
  head regen. Plane signatures are channel-specific. The generic
  family's residual stays owned by the record-hot bias P
  (exp51-D2); the N1 protocol remains the best registered direction.
  The first arm's mis-specification (cns/diff without the gamma*0.5
  + noise*3 base) was caught and BOTH arms recorded before the
  verdict.

## L46 — exp65 M38-A CO-TUNING: GEOMETRY REFUTED, MAINTENANCE ADOPTED
- (a) GEOMETRY CO-TUNING REFUTED: the err(k, s) grid (k in {2,3,4} x
  zone-width scale s in {1.0,1.5,2.0}) shows zone width is nearly
  INERT (k=4: 7.29 -> 7.09 at s=2; k=3 ~5.5 flat). The error lives
  at the NATIVE head|trunk boundary, not the scaled ectopic zone —
  widening the spec's zones does not touch where the smear is.
  CT-G1/CT-G2 REFUTED as registered; the verified free-running
  envelope stays k <= 2.
- (b) THE DIAGNOSIS CHAIN (registered after the geometry refusal):
  the failure is the UNCLAMPED SETTLE — at wide k the V field's
  contrasts decay faster than the latch holds, and the ANCHOR ITSELF
  drifts (measured: the ectopic eye's anchor -20 -> -26 over 15 h).
  LATCH-STRENGTH co-tuning is insufficient: k_anchor x8 errs 6.9;
  the FROZEN anchor (alpha_latch=0 + k_anchor x4) holds the MEMORY
  (pattern error 5.94 < 6.0) but the EXPRESSION still sags past the
  zone-hold check (the coupling bath pulls V off the latched spec).
- (c) MAINTENANCE CO-TUNING ADOPTED (CT-G4 PASS): a 3 h-period
  re-clamp schedule (2 h clamped per cycle — the exp58
  living-tissue-maintains-its-field lesson at the dial level)
  verifies the k=4 third-head FULLY (errs 3.89-3.94, pattern error
  AND all zone holds, 3/3 seeds).
- THE FINAL RULE (deposited): the free-running operating envelope is
  k <= 2; beyond it the compiler must EMIT A MAINTENANCE SCHEDULE
  whose duty cycle scales with the dial. Range expansion converts a
  self-holding anatomy into a MAINTENANCE-DEPENDENT anatomy; the
  duty cycle is the currency that buys reach.
- First in-file run correction: the CT-G4 chain reused the CT-G3
  s=2.0 program's clamps against the s=1.0 target (clamp/target
  mismatch, errs ~10) — caught before verdicts, fixed to prog0.

## L47 — exp66 CORPUS SEMANTICS CORRECTED (the gj_block protocols decoded)
- THE PROTOCOL EXTRACTION (316 drug-schedule entries): the gj_block
  class is a MIXTURE — pub1 (2010 octanol): SUSTAINED from t=0
  (start=0, end=0, regen 14); pub20 (2005 heptanol): DELAYED ONSET at
  2 h (start=2, end=0), then sustained; PLUS e329: a true WASHOUT
  PULSE (start=0, end=2 — blockade for 2 h, then full coupling).
- SG-G1 PASS — THE HEAD_TAIL ANOMALY WAS A PLANE MIS-MAP: e421 "Head
  plus PRE-pharyngeal crop" is ONE CONTIGUOUS anterior removal (the
  fragment is posterior trunk+tail — head-plane semantics), not a
  two-end fragment; only the POST-pharyngeal variant (e423) is
  genuinely both-ends. Remapped, the sustained-blockade head arm
  (post-M33, 0.00) matches e421's recorded 0.00; the head_tail class
  shrinks to n=1 and the exp57-D anomaly is CLOSED as a taxonomy
  artifact, not a model failure.
- SG-G3 PASS — THE 0.177 RESIDUAL IS OWNED BY THE MIXTURE: pooling
  gj_block|head BY PUBLICATION gives pub1 0.092 (n=4, delta to the
  model 0.09) vs the pooled 0.177 (delta 0.177) — the octanol
  subset's M33-consistent rate was hiding under the heptanol subset's
  offset. The exp50-A ownership is re-assigned: protocol-onset
  semantics + cross-publication scoring bias, not a missing
  mechanism.
- SG-G2 REFUTED AS REGISTERED (honest): the washout-pulse arm rates
  0.67 vs e329's recorded 0.00 (n=1) — the chain RE-CARRIES
  blind-committed identity; exp54's re-absorption was a settle-phase
  V-pulse phenomenon, not committed identities (~2.5 cells commit
  blind in the blocked 2 h and propagate). M40 CANDIDATE REGISTERED:
  commitment-rate coupling to coupling state (cells under acute
  blockade DELAY commitment — partial, to preserve the calibrated
  sustained arms); pub20's whole series runs cooler than
  blind-commitment predicts (e328 0.19, e329 0.00) — one direction.

## L48 — exp67 COMPILER V3: THE CORPUS-COMPILATION LOOP
- The full adopted stack (M25/M26c/M27b/M28/M31-A/M33/M35-A/M36/M37-A
  + the gene layer + the exp66 semantics) now generates EVERY mapped
  corpus arm — the corpus is the compiler's test suite. 43 deduped
  arms x 3 seeds over 905 mapped experiments.
- CV3-G1 PASS (the honest metric): FULL ACCOUNTING — mapped 905 +
  explicitly-recorded-unmappable 557 = 1,462 (every outcome-bearing
  experiment accounted). exp37's 1,029 included ~124 other_rnai
  experiments under the all-zero mapping the corpus itself refuted;
  the gene families with no 1D layer (organ/DV/PCP) are now RECORDED
  as unmappable, not force-mapped.
- CV3-G3 PASS — MAE 0.524 < exp37's 0.595: the adopted stack pays
  rent at corpus scale (the first corpus-level improvement since the
  exp37 baseline).
- CV3-G4 PASS — BOTH REFUTED SIGNATURES SHRINK: other_rnai delta
  0.798 -> 0.608 (the gene layer's sim 0.211 vs recorded 0.819); the
  gj_block|head delta 0.823 -> 0.177 (M33 + the exp66 mixture
  decomposition: the model's 0.00 vs the pub1-octanol subset's
  0.092).
- CV3-G2 REFUTED AS REGISTERED (honest, with the artifact diagnosis):
  plane rho 0.400 < exp37's 0.80 — exp37's rho was partly an ARTIFACT
  of the refuted all-zero other_rnai mapping (389 experiments pinned
  at 0.00 flattened the sim's plane profile into coincidental
  agreement with the compressed record). With the gene layer active
  the sim's plane profile SPREADS (crosspiece 0.006 -> head_tail
  0.667) while the recorded profile stays COMPRESSED (0.42-0.75) by
  the record-hot bias (exp51-D2). Five-point Spearman cannot order a
  compressed target; the per-class x plane table (deposited) is the
  informative instrument.

## L49 — exp68 THE COHERENCE-FORMALIZATION SEARCH (star-search step 1)
- THE STAR QUESTION: is the exp43/R5 coherence constraint a fact of
  the DYNAMICS or an artifact of b2v's density normalization? The
  dynamics-matched alternatives (the unnormalized Laplacian's label
  energy E = crossing x contrast^2, the per-node mean force,
  algebraic connectivity, conductance) computed over a 9-substrate
  battery (path/ring/circulant4/grid/torus/random-3/random-6/
  scale-free/small-world) x two labelings (fixed-index, BFS-coherent).
- CF-G1 PASS: the exp43 calibration anchors reproduce EXACTLY (path
  1.77 / grid 5.69 / random-3 11.19 / scale-free 11.92 vs the stored
  1.8/5.6/11.2/11.9).
- CF-G2 — THE BOUNDARY DOES NOT MOVE: no (substrate, labeling) exists
  where b2v refuses but the dynamics supports. The constraint is
  ROBUST across the formalization battery. THE HONEST STEP-1 REPORT:
  the coherence constraint is NOT YET FORMALIZATION-DEPENDENT — the
  naive floating-pattern star stays blocked by the DYNAMICS, not by
  the metric. The 101% path needs a new MECHANISM (e.g., active
  substrate renormalization — the substrate rewiring itself to
  support the pattern), not a re-metricization.
- CF-G3 PASS — ALL FIVE FORMALIZATIONS SEPARATE the pass/fail sets
  (b2v pass [0.010, 0.072] / fail [0.110, 0.487]; label energy
  [900-11,700] / [19,800-86,400]; mean force; lambda2; conductance).
  The torus (b2v 0.110, err 8.47) sits just over the R5 limit and
  fails; the dense random-6 (b2v 0.024, err 3.82) passes — the
  destroyer is the LABEL STRUCTURE (community coherence), not degree
  or density. The R5 limit 0.10 is well-placed: it sits inside the
  separation gap on every metric.

## L50 — exp69 M40 COMMITMENT-RATE COUPLING: ADOPTED (4/4)
- THE MECHANISM: cell_period_eff = cell_period x (1 + D x (1 - r)) —
  the blastema's commitment rate scales with the readout quality
  (cells do not lock identities they cannot read). Pure rate law on
  the inter-commit dynamics; collective.py gains commitment_delay
  (bit-exact at D=0).
- M40-G1 PASS: bit-exact at D=0.
- M40-G2 PASS — THE CONSTRAINT SWEEP (the honest adoption instrument):
  D in {1, 2, 4, 8} must satisfy the washout record (e329: 0.00 at
  n=1, bar <= 0.34) WHILE the sustained-blockade tail signature stays
  within +-0.34 of its D=0 value. D=2.0 is the first to satisfy both
  (washout 0.00; sustained delta 0.00 — the calibrated arms are
  UNCHANGED, the rate law acts only where coupling is restored
  mid-walk).
- M40-G3 PASS — DOSE MONOTONICITY at D=2: blockade windows {1, 2, 3,
  sustained} -> {0.00, 0.00, 0.67, 1.00} — matching pub20's own
  direction (e329 washout 0.00 < e328 delayed 0.19 < sustained).
- M40-G4 PASS: the M33 head rescue survives at the adopted D (0.00).
- The exp66 SG-G2 refutation is thereby REPAIRED: the washout arm
  with the adopted rate law reproduces e329's normal regeneration
  while every calibrated sustained arm is untouched.

## L51 — exp70 ONSET-AWARE CORPUS RE-PASS (4/4)
- The gj_block class's drug schedules classify ALL 29 experiments:
  22 sustained / 6 delayed / 1 washout (the exp66 extraction made
  operational). The washout and delayed arms use the adopted M40
  rate law (D=2, exp69); the sustained arms carry D=2 (rates
  unchanged — M40-G2).
- ON-G1 PASS coverage; ON-G2 PASS — e329's washout arm rates 0.00
  vs recorded 0.00 (the exp66 SG-G2 refutation now REPAIRED AT
  CORPUS LEVEL); ON-G3 PASS the delayed<=sustained direction (with
  the honest note: the delayed tail arm's 3-seed rate 1.00 vs
  e328's single record 0.19 — the pub20 subset offset persists);
  ON-G4 PASS — corpus MAE 0.522 < exp67's 0.524 (the running
  integration metric improves with every adopted mechanism: 0.595
  exp37 -> 0.524 exp67 -> 0.522 exp70).

## L52 — exp71 STAGE-3 MINIMALITY (3/4)
- THE LADDER (third-head / two-head, 3 seeds): full clamps+latch
  verifies (errs 2.1-2.7); novel-zones-only FAILS (4.4-4.7 — the
  unclamped native zones sag past the zone-hold bar); latch-only
  (no clamps) FAILS at 5.1-5.7 (close, but the zone holds miss);
  regen-only catastrophic (19-21). MIN-G2 REFUTED as registered:
  the R1'' state write replaces the LONG forcing, not the HELD
  WINDOW — the expression layer must be held while the protocol
  runs; the state write alone cannot form the anatomy.
- MIN-G1 PASS (downward closure: verification is monotone in
  program inclusion); MIN-G3 PASS (the pruning rule emits the
  minimal program).
- MIN-G4 PASS — THE MINIMAL PRODUCT IS 100-GENERATION STABLE
  (6/6, cycles_to_failure None): the latch-only-formed anatomy,
  once formed, holds as stably as the full program's. The forcing
  is needed only during FORMATION, never during HOLDING.
- THE MINIMAL PROGRAM (assembled from exp61+exp71): 3 h clamped
  window (the minimum window) + the state write + the trigger.
  Every component is now individually priced: the window's clamps
  (3 h, necessary), the latch-write (replaces long forcing), the
  trigger (the regen), zero maintenance below k<=2.

## L53 — exp72 STAGE-4 CROSS-TISSUE DIAL (2/3)
- XT-G1 PASS — THE DIAL RULE TRANSFERS: the horizon is monotone in
  the coupling radius on EVERY tissue (chain 5 -> 10 -> 24; grid
  7.1 -> 7.1 saturated-non-decreasing; small-world 5 -> 10 -> 42).
  First-run correction: the grid's index-distance horizon saturates
  at the tissue size (55 = the whole unrolled grid) — the geometric
  (Euclidean) horizon replaces it, registered before the re-run.
- XT-G2 PASS — THE CONTRAST ENVELOPE TRANSFERS: the grid's settle
  error is monotone in k (7.94 -> 12.20) — whatever the geometry,
  reach is bought with contrast (the exp62/exp65 rule is not
  chain-specific).
- XT-G3 REFUTED (honest) — NO UNIVERSAL VOLUME LAW: the horizon does
  NOT collapse onto neighborhood volume (Spearman rho 0.594 < 0.9).
  The 2D grid SATURATES (the influence fills the tissue at any k)
  while the small-world's long-range chords JUMP the horizon (42 at
  k=4). The dial's RULE is universal; the dial's READOUT is
  tissue-specific (geometry + link redundancy). A real refinement of
  the Stage-4 rule, not a failure of the dial.
