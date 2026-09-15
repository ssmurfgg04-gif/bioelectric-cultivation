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
