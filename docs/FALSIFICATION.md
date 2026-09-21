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

## L54 — exp73 ACTIVE SUBSTRATE RENORMALIZATION (the star-search step 2; 2/6 as registered, with a structured partial star hit)
- THE MECHANISM (L49's registered candidate, built): conflict-driven
  rewiring DURING the write — each round: one exp68 write attempt, then
  degree-preserving double-edge swaps with Metropolis acceptance on
  total junction conflict (T=100 mV^2), HARD connectivity constraint.
  Target-blind by construction (the rule reads only (A, V) — the
  transjunctional drop, the real connexin-remodeling signal).
- SR-G1 PASS — exact static anchors (exp68 reproduced to 0.01 mV on
  all 10 arms).
- SR-G2 REFUTED AS REGISTERED — but THE PARTIAL STAR HIT: 4/6 fail
  arms BECOME WRITABLE: torus|fixed 8.47 -> 1.96 (first writable round
  2), torus|bfs 8.20 -> 3.36, random3|fixed 11.19 -> 3.99, random3|bfs
  7.72 -> 3.33 — degrees preserved EXACTLY, connectivity every round,
  fresh-seed hold (hold_err ~= verdict_err; SR-G4 HOLDS for these
  arms). THE BOUNDARY MOVES FOR THE HOMOGENEOUS-DEGREE SUBSTRATES.
- THE WALL (the new discovery): scale_free is IMMOVABLE (11.92 ->
  10.58, 11.44 -> 9.32; b2v stuck 0.38-0.49). Diagnosis: the residual
  constraint is the DEGREE SEQUENCE. The BA hubs straddle the label
  boundary; under degree conservation a degree-d hub has unavoidable
  crossing into the other region. The coherence constraint DECOMPOSES:
  (a) the wiring ARRANGEMENT is renormalizable (exp73's mechanism),
  (b) the degree BUDGET is not (under conservation).
- SR-G3 REFUTED with diagnosis: reversed-pattern rewiring also helps
  the original (random3|bfs reversed 1.43 < matched 3.33) — the
  mechanism is GENERIC COMPARTMENTALIZATION (junction remodeling
  localizes coupling; ANY spatially smooth pattern benefits), not
  instance-specific memory. The substrate coheres with the pattern
  CLASS (spatially smooth), not the instance.
- SR-G5 as registered REFUTED (4/6); the refined semantics holds: for
  every arm where the DYNAMICS moved, b2v moved below 0.10 too
  (0.010-0.047) — metric and dynamics track together on renormalized
  substrates; scale_free: BOTH refuse (no metric-dynamics
  disagreement anywhere). The compiler's R5 survives as the right
  metric for remodeled tissue.
- SR-G6 price deposited: rounds-to-first-writable 2-9 (the
  renormalization cost curve).
- CTRL shattering ablation: even with connectivity off, scale_free
  forms only 2 components and STILL FAILS (degree conservation blocks
  disconnection — hubs keep their edges). The trivial escape is closed
  too.
- THE STAR REFRAME: coherence is a PROCESS (the substrate renormalizes
  toward the pattern), and the residual boundary is the degree budget.
  Next (exp74): the RENORMALIZATION LADDER — relax degree conservation
  (junction pruning: connexin down-regulation, also real biology) with
  connectivity preserved; measure the minimal residual cut; find the
  last wall.

## L55 — exp74 THE RENORMALIZATION LADDER (the star-search step 3; 4/6)
- THE LADDER: relax the degree budget rung by rung, every move local
  and target-blind — rung 1 REWIRE (exp73), rung 2 +PRUNE (conflict-
  thresholded dissolution, threshold (0.3xcontrast)^2, connectivity
  hard), rung 3 +GROW (Hebbian agreement wiring, budget = 1x initial
  edges). Each rung continues from the previous wiring.
- RL-G1 PASS — rung-1 anchor reproduces exp73 (torus 1.96 / random3
  3.99 PASS, scale_free 10.58 FAIL).
- RL-G2 REFUTED — THE LADDER DOES NOT CLIMB FOR scale_free: rung 2
  prunes only ~21 edges then starves (10.46 -> 9.26), rung 3 grows
  197 edges and gets WORSE (10.17, b2v 0.3756 -> 0.4075). NOT
  WRITABLE AT ANY RUNG.
- THE DIAGNOSIS (the new wall): the LOCAL REMODELING SIGNALS ARE
  SMEAR-CORRUPTED. (a) Per-edge conflict is DEGREE-DILUTED — a hub
  with 50 cross edges carries only a small drop per edge (the pull is
  shared), so every edge sits below the prune threshold while the
  tissue is globally incoherent: the tissue cannot SENSE its own
  incoherence. (b) V-agreement growth is corrupted by the smear — in
  the smeared field, cells ACROSS the true boundary both sit near the
  midpoint and "agree", so growth WIRES ACROSS the boundary (cut 134 ->
  152 edges); the incoherence is SELF-MASKING: the field corrupts the
  very signals that would repair it.
- RL-G4 REFUTED (scale_free fails verdict and hold); the movable arms
  hold (hold ~= verdict on all four).
- RL-G5a PASS — the fraction metric tracks every moved arm (b2v
  0.0067-0.08 < 0.10; failed arms 0.35-0.41). RL-G5b PASS — the
  ABSOLUTE crossing separates the pass/fail sets completely (pass
  [1,2,9,16] vs fail [134,152]) — both metric forms survive the
  ladder; no M41 yet.
- RL-G7 PASS — no regression: the pass controls shed NOTHING (path
  99->99, grid2d 180->180 edges; the threshold rule is need-driven,
  exactly as registered).
- THE RESIDUAL CUT (readout capacity, RL-G3 deposited): torus|bfs 2
  bridges (1 head component), random3|fixed 9 bridges (2 head comps —
  the minimum is 2, the tissue spent 9), random3|bfs 1 bridge (1 comp
  — MINIMAL). The write-coherence vs readout-bandwidth trade-off is
  now measurable in bridges.
- THE CANDIDATE SIGNAL THAT ESCAPES THE SMEAR: the homeostatic drag
  |V_i - theta_i| — per-cell (not per-edge, undiluted), fully local
  (a cell knows its own channel-set target and its achieved voltage),
  target-blind. It reads the smear DIRECTLY (theta = binary label, V =
  smeared; drag = the error). exp75 = rung 4: DRAG-DRIVEN REMODELING.
  Prediction: scale_free becomes writable when cells that cannot hold
  their identity shed their most-conflicting junctions. If refuted,
  the wall is deeper than sensing (log what remains).

## L56 — exp75 RUNG 4: DRAG-DRIVEN REMODELING (the star-search step 4; 2/6 — and the refutation IS the discovery)
- THE REGISTERED PREDICTION REFUTED, SPECTACULARLY: the homeostatic
  drag |V - theta| NEVER FIRES — mean drag ~1.9-2.1 mV on the FAIL
  arms (threshold 8), hot cells = 0, shed = 0, the wall arms never
  move (11.92, 11.44; b2v 0.487/0.457 unchanged; edges 197->197).
- THE DIAGNOSIS (a mechanism theorem in disguise): THE DRAG SIGNAL IS
  SELF-EXTINGUISHING. theta is PLASTIC (eps = 0.04; relaxation time 25
  t.u. ~= the 24 t.u. write window): while the junction field smears
  V, the homeostatic plasticity drags theta AFTER it — by the tail,
  theta ~= smeared V everywhere. The cell's reference frame moves with
  the hijack. THE HIJACK REWRITES THE REFERENCE: a single-timescale
  tissue cannot locally detect its own incoherence, because the
  incoherence corrupts the very variable that would measure it.
  (Corollary: the drag DID separate weakly — fail arms 1.9-2.1 vs pass
  arms 0.3-1.3 mV — but ~4x too weak, suppressed by exactly the
  plasticity that defines theta.)
- THE THEOREM SHAPING UP (the star-search's real product): COHERENCE
  REQUIRES AN ANCHOR SLOWER THAN THE HIJACK. The codebase already
  carries the two-timescale structure — M28's dual field (theta = the
  expression layer, phi_spec = the positional spec captured at pattern
  set). The star search has now INDEPENDENTLY re-derived why the dual
  field must exist: not as a convenience but as a necessity — without
  a slow anchor, identity maintenance is undetectable in principle.
- DR-G1 REFUTED (no separation at the registered threshold); DR-G2/3/4
  REFUTED (the mechanism never engaged — zero shedding everywhere, so
  the controls trivially held); DR-G5 PASS (both metrics still track:
  b2v 0.487/0.457 with the dynamics refusing; nothing moved).
- NEXT (exp76, rung 5): THE SLOW ANCHOR. Two-timescale identity: the
  frozen (or 40x-slower) anchor = M28's phi_spec semantics, captured
  at write start; the remodeling signal becomes the SLOW drag
  |V - theta_slow|. Registered prediction: scale_free becomes
  writable. The theorem contrast is the gate: single-timescale (eps_slow
  = eps) must fail (reproduces exp75), frozen must work — the
  timescale separation IS the mechanism that moves the boundary.

## L57 — exp76 RUNG 5: THE SLOW ANCHOR (the star-search step 5; 1/7 as registered, with the wall precisely located and one implementation bug owned)
- THE SLOW DRAG WORKS: with the frozen anchor the signal separates
  (fail arms mean slow drag 9.8/9.3 mV, 35 hot cells; path 0.58 mV, 2
  hot) and shedding ENGAGES: scale_free|fixed 11.92 -> 8.45 (61
  junctions shed, cut 197 -> 136), scale_free|bfs 11.44 -> 7.27 (89
  shed, cut -> 27, b2v 0.250). First movement of the hub wall by a
  cell-autonomous rule.
- BUT THE PREDICTION REFUTED — THE SHED STALLS AT THE BRIDGE WALL:
  after the shed phase, EVERY remaining cut edge is a connectivity
  bridge (blocked counter: 801 / 600 consecutive connectivity-blocked
  shed attempts); error freezes at 8.4 / 7.3, above the 6.0 bar. The
  tissue has shed all it can without disconnecting, and 27-61 bridges
  still carry enough hijack to break the write.
- THE WALL, NOW EXACTLY LOCATED: not the degree budget (rung 5 sheds
  degree freely), not the sensing (the frozen anchor fires) — THE
  CONNECTIVITY ITSELF: anatomical unity forces electrical coupling,
  and the bridges carry the hijack. THE ESCAPE (registered as rung 6):
  anatomical bridges and electrical coupling are SEPARABLE variables
  (A vs G in the model's own equations; the theta/identity read
  propagates through mu*A and never touches G). CONDUCTANCE
  REMODELING: keep the bridge, down-regulate the channel (connexin
  gating — the most directly biological remodeling move: minutes, not
  hours). The write-coherence vs readout-bandwidth trade becomes a
  CONTINUOUS dial instead of a topological wall.
- AN IMPLEMENTATION BUG OWNED (the honesty protocol): AN-G1/AN-G7 as
  coded could not fire the theorem contrast — the eps_slow=0.04 anchor
  was relaxed toward its CAPTURED VALUE (lbl), never toward V, so it
  never felt the hijack (anchor drift 0.00 by construction, hot=35
  even at eps_slow=eps). The registered single-timescale-fails
  contrast is UNTESTED, not passed. exp77 re-registers it with the
  corrected dynamics: the anchor must be dragged BY THE VOLTAGE (a_v
  += eps_slow * (V - a_v)) — at eps_slow = eps it is theta (exp75's
  failure must reproduce); at 0 it is the frozen spec.
- AN-G6 PASS: the metrics still track (b2v 0.449/0.250 with the
  dynamics refusing — no disagreement). AN-G2 REFUTED as registered
  (grid2d's 19 hot cells exceed the pass-arm bound — the threshold
  reads depth of failure, and grid2d sits near the bar; the honest
  bound is on SHEDS, which grid2d limits to 20 harmless ones).
  AN-G5 REFUTED honestly: random3|fixed BREAKS under pure anchor-shed
  (8.15, from 11.19 — improved but still failing; the drag-shed alone
  is insufficient for random3: its bridges block at cut ~9 while its
  error needs rewiring, not just shedding — rung 1 remains its fix).

## L58 — exp77 RUNG 6: CONDUCTANCE REMODELING (the star-search step 6; 2/6 — the refutations converge on the real variable)
- THE CORRECTED THEOREM CONTRAST, HONESTLY SCORED REFUTED AS FIRED:
  eps_slow = 0.04 leaves 25 hot cells (not <=2) — the anchor crawled
  toward the hijacked V at rate eps (tau = 25 t.u. ~ the whole write
  window) and had NOT converged by the tail (residual ~38% of 30 mV >
  8). THE DEEPER FACT the contrast exposed: in exp75 theta tracked V
  because theta rides the JUNCTION DIFFUSION CHANNEL (mu * lap_theta
  at rate mu*deg — fast on a hub), not because of eps. THE ANCHOR
  ESCAPES THE HIJACK ONLY IF IT DOES NOT RIDE THE COUPLING CHANNEL:
  the two-timescale structure must split the JUNCTIONAL term, not just
  the rate. (Theorem refined: a memory that propagates through the
  channel that hijacks the field is hijacked with it.)
- THINNING MOVES THE WALL AGAIN, AND STALLS AGAIN: scale_free|fixed
  11.92 -> 9.66 (G/G0 0.699), |bfs 11.44 -> 8.75 (0.713). The thin
  budget exhausts in ~15 rounds — the hot cells' max-conflict x W
  edges are not the cut edges (the smear redistributes per-edge
  conflict into the regions' interiors): the local signal again
  cannot find the hijack's SOURCE. A ~19-20 hot cells persist forever
  at G/G0 0.70: the tissue feels the incoherence and cannot act on
  it. A UNCHANGED (verified array-equal), degrees exact.
- TH-G4 REFUTED: random3|fixed under pure thinning 7.26 (from 11.19,
  improved, still failing) — random3 needs REWIRING (its repair is
  rung 1); the rungs are COMPLEMENTARY moves, not alternatives.
- TH-G5: the topology metrics are indeed blind on the thinned
  substrate (b2v 0.487 with the verdict improving) BUT M41 DID NOT
  FIRE — the dynamics refuses too (9.66 > 6.0): wc = 0.51 tracks the
  refusal. THE METRIC TABLE IS THE PRODUCT: wc separates ALL 16
  points perfectly (static pass [0.010-0.072] / fail [0.110-0.487]
  inherited from exp68 + thinned arms 0.451/0.512 fail). The
  conductance-weighted crossing is promoted to the working coherence
  metric.
- THE CONVERGENCE (five rungs, one lesson): every local, cell-
  autonomous rule (rewire / prune / grow / shed / thin) FAILS in the
  high-degree regime because NO LOCAL SIGNAL IDENTIFIES THE HIJACK'S
  SOURCE IN A SMEARED FIELD. And the mean-field fixed point says why
  the wall exists at all: V* = (gamma*theta + G*V_nb)/(gamma + G) —
  the error at a boundary cell = CONTRAST * g_cut / (gamma + g_cut +
  g_home). WRITABILITY IS A PHASE RATIO: y = g_cut / (gamma + g_home)
  <~ 0.25 (substrate-free in mean-field). The hub fails because its
  g_cut = 10 while gamma = 0.25 — no rewiring of OTHER edges changes
  the hub's own y; only (a) thinning ITS cut conductance, or
  (b) STRENGTHENING THE IDENTITY (gamma), moves it. NEXT (exp78): THE
  COHERENCE PHASE DIAGRAM — sweep gamma and the thinning floor f,
  collapse all flip points onto the y variable; the star's mechanism
  candidate is the IDENTITY/COUPLING RATIO, a real physiological dial
  (channel expression vs junction load).

## L59 — exp78 THE COHERENCE PHASE DIAGRAM (the star-search step 7; 2/6 as registered — and the second channel found)
- SETUP: gamma sweep {0.25..256} x 8 arms (no remodeling; adaptive
  sub-stepping above gamma=0.25 preserves the Euler stability the
  64/256 rows need — the first run's 51 mV blowups were integration
  instability, diagnosed and fixed; the gamma=0.25 rows stay
  bit-consistent with the ledger anchors); uniform cut-thinning sweep
  w in {1..0}; the per-edge read instrument regrow_w (PD-G0 bit-exact
  at W=1: 14.004712 vs 14.004712).
- PD-G1 REFUTED — GAMMA ALONE CANNOT FLIP THE HUB ARMS: torus and
  random3|bfs flip at gamma*=4 (8.47 -> 5.38, 7.72 -> 5.43 — THE
  BOUNDARY MOVES WITH IDENTITY STRENGTH for them), but random3|fixed
  plateaus at 8.05 and scale_free at 9.17 — INVARIANT from gamma=16
  to gamma=256.
- PD-G3 REFUTED the same way: cut-thinning plateaus (scale_free
  7.74 at w=0) — thinning kills the electrical hijack and the error
  DOES NOT GO BELOW THE PLATEAU.
- PD-G7 THE ATTRIBUTION (the discovery): the plateau is the THETA
  CHANNEL. At gamma=256, mu=0 takes scale_free 9.17 -> 0.16 mV,
  random3|fixed 8.05 -> 0.07, torus 4.76 -> 0.04. THE IDENTITY LAYER
  ITSELF DIFFUSES THROUGH THE JUNCTIONS (dtheta = ... + mu*lap_theta):
  within one 24 t.u. window the hub's theta homogenizes with its
  neighborhood (rate mu*deg = 1.5/t.u. for the degree-99 hub —
  e^-35 dead), and gamma then faithfully HOLDS V to the hijacked
  theta. The V-channel law (y = g_cut/(gamma+g_total), boundary
  y* ~ 0.25) is REAL and the mean-field bounds the V-hijack exactly;
  the plateau was the second hijack riding the SAME junctions through
  the identity variable.
- THE COMPLETE LAW (registered for exp79): writability requires BOTH
  channels quiet: (1) V-channel: gamma > g_cut*(CONTRAST/bar - 1);
  (2) theta-channel: mu*T*deg_cut << 1 (the local homogenization
  number). The first yields to gamma and to G-thinning; the second
  yields ONLY to removing A-crossings (why exp73's rewiring fixed
  torus/random3 and could never fix the hubs) or to a NON-DIFFUSING
  identity anchor (mu=0 = the M28 phi_spec semantics — the spec does
  not ride the junctions). THE STAR'S ESCAPE IS AN ARCHITECTURE, NOT
  A DIAL: identity must ride a channel the coupling cannot hijack.
- PD-G4 REFUTED, AND THE REFUTATION IS A THEOREM: on one dial, write
  error falls with thinning (21.0 -> 15.3) but the regen read does
  not starve symmetrically — on a BINARY pattern the boundary
  junction is BOTH the write's leak AND the read's window (same edge,
  same channel, both directions). An amputated region whose external
  neighbors are the OTHER identity inherits the WRONG identity
  through intact junctions (25.7 at w=1) — the read is only as good
  as the parent's identity, and the hijack is only as bad as the
  neighbor's identity: ONE quantity. The escapes are structural:
  (a) the non-junctional spec read (phi_spec), (b) rectifying
  junctions (real connexins rectify), (c) time-gated coupling (open
  for the commitment window, closed for holding — the exp65
  maintenance semantics). Registered for exp79.
- PD-G2/PD-G5 REFUTED as single-channel laws (the y-band misses low:
  0.083-0.125; Spearman 0.730 with the plateau rows off-diagonal) —
  honestly: the single-ratio law is dead; the two-channel law is the
  candidate.

## L60 — exp79 THE TWO-CHANNEL LAW AND THE UNIVERSAL READER (the star-search step 8; 4/6 — THE STAR CROSSED AT THE MODEL LEVEL)
- THE GRID (3 arms x gamma in {0.25, 4, 64} x mu in {0.015..0}): the
  two dials are INDEPENDENT and each reaches writability — scale_free
  flips at (gamma=4, mu<=0.0015) OR (gamma=64, mu<=0.005); torus
  writes at (gamma=4, mu=0.005). The plateau of exp78 was exactly the
  theta homogenization number mu*deg*T.
- TC-G2 PASS — the homogenization number is QUANTITATIVE: the formula
  err_theta = imbalance_i*(1-exp(-mu*deg_i*T)) reproduces the
  plateau's mu-dependence (7/9 points in tolerance).
- TC-G1 REFUTED as an exact law (Spearman 0.838 < 0.90; boundary
  agreement exactly 80%): the channels INTERACT (V follows the
  diffusing theta; the max-of-terms form is the right first-order law
  but not the final one). Registered: the interaction term is the
  next theory task.
- TC-G3 PASS — **THE STAR POINT**: scale_free|fixed writes with NO
  remodeling at (gamma=64, mu=0): verdict 0.57, hold 0.57. The
  exp43/R5 coherence boundary is NOT a wall — it is an ARCHITECTURE
  REQUIREMENT: identity strength (256x baseline) + a non-diffusing
  anchor makes ANY substrate coherent with the pattern. The 101%
  mechanism the handoff asked for: the boundary moves when the
  identity rides a channel the coupling cannot hijack.
- TC-G4 PASS — **THE UNIVERSAL READER**: head regen at w=0 (every
  shell junction electrically silent): pure inheritance 24.7,
  junction-carried spec 23.8 (both read the WRONG parents), the
  NON-JUNCTIONAL anterior read (M33) restores identity AT COMMITMENT
  — and the full composition (reader + anchor + strength, gamma=64,
  mu=0, w=0) regenerates the head at V 0.43 / theta 0.44 THROUGH ZERO
  JUNCTIONS. The reader path is closed at the model level: the
  universal reader is the positional spec read on a channel the
  coupling does not share — the architecture the window-leak theorem
  demanded, already carried by the model as M33.
- TC-G5 PASS — the reader's domain is anterior-only (trunk regen at
  w=0 stays failed at 9.10: no local pole, no non-junctional read) —
  the recorded posterior-biased GJ-blockade phenotypes (the exp60/66
  corpus semantics) reproduced as a structural theorem.
- TC-G6 REFUTED with the diagnosis: the price of the anchor is NOT
  propagation loss — the eps channel (V-mediated homeostatic drag)
  provides REDUNDANT slower propagation, so the wound repattern
  converges identically at 240 t.u. (8.76 vs 8.76). The anchor's
  true price is the RATE of organic repatterning (eps-only), and the
  redundancy itself is a finding: the identity has two propagation
  paths (direct theta-diffusion and V-mediated drag); the write
  window (24 t.u.) is exactly where eps is too slow to matter —
  which is why the two-channel law binds at write time and not at
  homeostatic time.
- THE STAR-SEARCH LEDGER (exp68 -> exp79): step 1 the constraint is
  formalization-robust; steps 2-6 every LOCAL remodeling mechanism
  (rewire/prune/grow/shed/thin) fails the hub regime, each with a
  diagnosed signal pathology (degree dilution, smear corruption,
  self-extinguishing reference, bridge wall, source-blindness); step
  7 the two-channel structure found (V-ratio + theta homogenization);
  step 8 the star crossed by ARCHITECTURE: strong identity +
  non-diffusing anchor + non-junctional read. THE REFRAME IS NOW A
  RESULT: "any substrate coherent with the pattern" = any substrate,
  GIVEN an identity architecture that does not share a channel with
  the coupling. The star is not no-substrate; it is any-substrate-
  with-the-right-identity-physics.

## L61 — exp80 THE EXTERNAL STORAGE PROTOCOL (Stage-5 90% item; 6/6 — CLOSED)
- THE PROTOCOL (four steps, machine-checked): CAPTURE (the
  identity-at-coordinate map serialized to JSON — the M28 phi_spec
  semantics) -> STORE (bytes; the medium is ageless) -> DESTROY (the
  source substrate discarded entirely) -> RE-INSTANTIATE (the
  protocol's operating point: the L60 star architecture, gamma=64,
  mu=0).
- ES-G1 PASS — byte-exact through the file (818 bytes).
- ES-G2 PASS — substrate-independent: the chain-stored pattern
  re-instantiates on grid (0.10 mV) AND scale_free (0.57 mV).
- ES-G3 PASS — TOTAL DESTRUCTION: different size (n=150),
  different topology (random-regular), fresh seeds — positional
  resampling carries the spec's coordinate semantics; err 0.36.
  The pattern is not a property of any cell, tissue, or substrate
  (D3 taken to the medium level).
- ES-G4 PASS — the FORM regenerates on the destination: amputation +
  the non-junctional anterior read regrows the loaded identity
  (V 0.62 / theta 0.62). The storage carries the spec; the
  reader+architecture make the form.
- ES-G5 PASS — 1,000 storage generations, zero byte drift: the
  medium does not age; the holding conditions are required only
  AFTER loading.
- ES-G6 PASS (the load-bearing gate) — the same file at the BASELINE
  operating point FAILS on scale_free (11.92): the medium alone is
  not the pattern; the re-instantiation architecture is a required
  part of the protocol. The L60 theorem in protocol form.
- THE WET-LAB COMPANION (docs/STAGE5_EXTERNAL_STORAGE_PROTOCOL.md):
  the four steps mapped onto the verified anchors — capture via the
  4D atlas readout (MED42172041), the 3 h write window (Durant,
  MED30799071), the gene-layer families as the strength module
  (exp60), M33 as the anchor module, the graft bank (Saito 2003) and
  the cryptic state (M31) as biological media. Residuals named: the
  64x channel lock is not a validated wet protocol; the multi-field
  capture schema; the shared coordinate convention.
- Stage-5 90% scoreboard: external storage CLOSED; the star
  (any-substrate coherence) CLOSED at the model level (L60); the
  remaining 90% residuals are the corpus MAE (Stage 2's 0.522 ->
  <0.15 target) and the compiler's real-model validation.

## L62 — exp81 COMPILER V4: THE GENERATOR (Stage-3's star; 5/5)
- THE DIRECTION REVERSED: not "compile this anatomy" but "generate
  anatomies evolution never made, every one compilable, verified,
  stable". The generator samples the multi-zone space (1-4 identity
  zones, arbitrary fractions/voltages/planes); 40 specs, all compile.
- GV-G1 PASS — the generator works (40/40 valid).
- THE FINDING (GV-G2's first instrument): R5 alone admits 40/40 on
  the chain but only 6 verify (15% precision) — THE GENERATOR SPACE
  IS FAR LARGER THAN THE DYNAMIC ENVELOPE. The diagnosis (per-spec
  failure table): (a) 10/10 single-zone TRIGGER specs fail the regen
  check — the chain's regen walk re-derives the WILDTYPE pattern
  beyond the cut; a trigger CANNOT regenerate a novel zone (the
  regen-limitation finding; the graph-native multi-zone regen is the
  exp79 reader, future work); (b) the dynamic failures are thin zones
  (cannot hold) and low-contrast neighbors (merge).
- THE V4 FILTER IS CALIBRATED, NOT GUESSED: features (min zone width,
  min adjacent contrast) fit on the calibration half, scored on the
  test half (no leakage). The rule (width>=8 cells, contrast>=4 mV)
  achieves TEST PRECISION 100% AT COVERAGE 40%. GV-G2 PASS.
- GV-G3 PASS — NOVELTY: three classes with NO corpus counterpart
  (multi-zone-3+island, multi-zone-4+island, two-zone-island); 4
  novel-class anatomies verified end-to-end. The compiler now
  produces forms the corpus does not contain.
- GV-G4 PASS — 100-generation hold stability 3/4 (the exp61/71
  zero-drift semantics on the novel forms; the 1 failure is the
  envelope's honest tail).
- GV-G5 PASS — **THE OPERATING-POINT ESCAPE**: on scale_free, 35/35
  baseline-refused candidates VERIFY at the star point (100%), and
  the program carries the operating point as an audit-ready
  precondition with the law as its warrant. THE TWO-CHANNEL LAW IS
  NOW WIRED INTO THE COMPILER: a baseline refusal is no longer
  final — it names the conditions (identity strength + non-diffusing
  anchor) under which the substrate becomes admissible.
- Stage-3 scoreboard after v4: the compiler generates novel
  anatomies (the Stage-3 101% star: AI generates new anatomies
  evolution never made — CLOSED at the model level), prices every
  intervention, calibrates its own admissibility envelope from data,
  and emits the coherence law as a precondition.

## L63 — exp82 THE MAINTENANCE-DUTY MAP (Stage-4 full characterization; 4/5)
- THE MAP: form the s=2.0 ectopic-head pattern (24 h clamps + latch),
  hold 15 t.u. under 3 h maintenance cycles at duty in {0, 0.1, 0.25,
  0.5, 0.75, 1.0}, sweep the chain's coupling radius k in {2..6};
  grid and small-world run the duty axis at native topology (the k
  axis is chain-native — registered before the run).
- THE CHAIN FRONTIER (MD-G5, the currency curve): k=2 -> duty 0.0
  (free-running), k=3 -> 0.25, k=4 -> 0.75, k=5 -> 1.0, k=6 -> 1.0.
  exp65's k=4 @ duty 0.67 is bracketed exactly (0.5 fails, 0.75
  holds). The exchange rate between reach and maintenance is now a
  MEASURED CURVE, not a rule of thumb: the first step beyond the
  envelope is cheap (0.25), the last step to k=5 costs everything.
- MD-G1 PASS — the frontier is monotone. MD-G2 PASS — the
  free-running corner (k=2 at duty 0) confirmed as the map's origin
  on the chain. MD-G3 PASS — the ceiling (duty 1.0 sustains every
  k): the map is bounded [free-running, continuous-clamp].
- MD-G4 REFUTED — THE FRONTIER IS TISSUE-SPECIFIC: at the same form,
  the grid needs duty 1.0 (continuous clamping — the exp72 grid was
  the hardest tissue and stays hardest) while the small-world
  free-runs (duty 0.0 — the long chords carry the pattern). The
  honest refinement of exp72's lesson: the dial's RULE (monotone in
  k, monotone in duty) is universal; the ENVELOPE and the FRONTIER
  are readout-side (tissue geometry). The currency's EXCHANGE RATE
  depends on the tissue.
- Stage-4 scoreboard after the map: the dial characterized end to
  end — the reach dial (exp62), the maintenance co-tuning (exp65),
  the cross-tissue rule (exp72), and now the full duty map with the
  measured frontier and its tissue-specificity (exp82). The
  compiler's maintenance-schedule emission (R6/exp65) now has its
  quantitative table.

## L64 — exp83 THE GENE-LAYER RESIDUAL CLOSURE (GL-G3/GL-G4; 2/3 as registered — the pool closes, the profile registers its repair)
- GR-G2 PASS — **GL-G4 CLOSED BY THE RECORD CORRECTION**: the
  control family's measured hot rate is 0.270 (in-run, the one-sided
  record bias); the corrected generic target is 0.855 - 0.270 =
  0.585, band [0.485, 0.685] — and the N1 protocol's sim lands at
  0.655, INSIDE the band at every gamma scale (0.7..1.0: the scale is
  INERT on the pooled rate — the commitment_diffusion term drives the
  abnormality, not the resting-potential strength; a real
  mechanistic attribution). THE PROTOCOL WAS NEVER TOO WEAK — THE
  RECORD WAS TOO HOT. exp51's N1 deposit band [0.22, 0.67] is
  RETIRED (formed against the uncorrected record; exp60 fired its
  falsifier honestly; the corrected deposit replaces it). Control at
  g* = 0.00 (structurally clean).
- GR-G1 SPLIT — the POOL closes, the PROFILE does not: with the
  adopted M37-A coin (nb_p=0.8, the exp64 semantics: the coin
  REPLACES the deterministic scar — the first run layered it on
  scar=1.0 and pinned everything abnormal; diagnosed and fixed), the
  neoblast family's sim pooled rate is 0.695 vs the record's 0.701 —
  a 0.006 match (the graded-record gap CLOSED at the pool level).
  BUT the per-plane direction REFUTES: the record's covered-plane
  worst is trunk (0.81) while the sim's head runs 1.0 > trunk 0.67.
  A ONE-PARAMETER coin (one global p, anchored to the trunk record)
  matches the pool by construction and cannot match an arbitrary
  plane profile. M37-A' REGISTERED: per-plane coin anchors
  nb_p(plane) calibrated to the record's plane rates — the
  penetrance mechanism is right, its parameterization needs the
  plane axis.
- GR-G3 PASS — the falsifier retirement is verified by the numbers
  above and documented in the notes.
- THE GENE-LAYER SCOREBOARD after the closure: GL-G1/G2/G5 passed
  (exp60); M37-A adopted (exp64) and pool-validated (exp83);
  M37-B refuted (exp64) and its repair path superseded by the record
  correction (exp83); M40 adopted (exp69); GL-G4 closed (exp83);
  GL-G3 pool-closed with M37-A' registered (the one remaining
  registered candidate in the gene layer).

## L65 — docs milestone: the protocol/generator batch (exp80-exp83)
- 67/67 tests green re-verified after the batch. The README stage
  scoreboard updated: Stage-3's generator star closed (v4), Stage-4
  characterized end to end (the duty map), Stage-5 storage closed
  (6/6 + the wet-lab companion), Stage-2's GL-G4 closed by record
  correction with M37-A' the one registered candidate left.
- Open next (derived from the ledger): M37-A' per-plane coin anchors
  (the gene layer's last registered candidate); the graph-native
  multi-zone reader regen (the regen-walk limitation's repair); the
  two-channel interaction term (TC-G1's Spearman 0.838); the corpus
  MAE residual (0.522 vs the <0.15 90% target); quest 001 on quota.

## L66 — exp84 THE TWO-CHANNEL INTERACTION TERM (5/5 — the star's quantitative law CLOSED)
- The design: direct channel ablation on exp79's full 45-point grid
  (3 plateau arms x 3 gamma x 5 mu, 3 seeds) — four configs per
  point: FULL (both channels), V-ONLY (mu=0, the hijack channel
  alone), THETA-ONLY (the V-junctional coupling removed inside step,
  diffusion alone with the drive relay intact), NEITHER (both off).
- IL-G1 PASS — the decomposition is CLEAN: the neither-panel error
  <= 0.56 mV at every point (both channels off -> no erosion beyond
  noise; the ablation machinery is load-bearing).
- IL-G2 PASS — **THE LAW IS QUADRATURE**: the measured channel
  erosions compose as err = sqrt(eV^2 + eT^2) — Spearman 0.999,
  median relative error 2.7% across the 45 points; the torus holdout
  (fitted only on scale_free+random3) lands at rho 1.000, 3.1%. For
  calibration, exp79's mean-field max(V-term, theta-term) scored
  0.838 — the failure was never the dynamics, it was the FORMULAS:
  each mean-field term bounds its channel's single-channel limit,
  and the theta formula's (1-exp(-mu*deg*T)) saturation overpredicts
  the measured mu-dependence by up to 7x at mid mu.
- IL-G3 — the overlap correction (max + kappa*min) is RETIRED
  honestly: kappa*=0.15 improves the holdout by only 1%; the L2
  stands alone. The interaction delta (full - max(eV,eT)) is a small
  positive (median +0.19 mV, IQR [+0.05, +0.55]) — the two channels
  erode the pattern amplitude through INDEPENDENT paths and compose
  quadratically (the same mathematics as independent noise sources):
  sub-additive vs sum, super-additive vs max.
- IL-G4 PASS — the writability boundary (err < 6.0) under the L2
  composition: 100% agreement on the grid.
- IL-G5 — THE PRICE ATTRIBUTED (TC-G6's failed form retired): the
  four-config wound-repattern panel (scale_free, 240 t.u., no
  clamps) is CHANNEL-INVARIANT — full 9.79, V-only 9.80,
  theta-only 9.81, neither 11.44 mV. No single channel carries the
  unclamped wound repattern; even both channels open do not recover
  it on scale_free at the long window. exp79's price form (mu=0.015
  works, mu=0 fails) was mis-specified at the panel level: the
  anchor architecture's price (mu=0 kills organic propagation) is a
  property of the PATTERN-PROPAGATION panel (exp62/exp65's reach
  dial and the maintenance schedules), not of wound repattern. The
  price is hereby attributed to the propagation panel where it was
  originally measured.
- THE STAR'S QUANTITATIVE LAW, final form: writability = (V-channel
  hijack ratio below the bar) AND (theta homogenization below the
  bar), with the two measured erosions composing as
  err = sqrt(eV^2 + eT^2); the boundary is the L2 radius < 6.0 mV.
  The compiler's operating-point audit (exp81's R5/R6 precondition)
  now runs on the closed law.

## L67 — exp85 M37-A' ON TRIAL (4/5 — the coin EXONERATED, the repair RE-TARGETED to the regen layer)
- The trial design: before running the registered per-plane anchors,
  exp85 asked whether exp83's profile refutation was REAL or POWER —
  the refutation ran on 3 seeds/plane (realized coin se ~0.23; the
  head 1.0 / trunk 0.667 inversion is inside that noise), and the
  record's own plane profile (trunk 0.812 n=28, head 0.750 n=5, tail
  0.740 n=2) may be flat. A pre-registered binding disposition rule
  covered all four outcomes before any run.
- UP-G1 PASS — **THE RECORD'S PROFILE IS STATISTICALLY FLAT**: the
  plane z-scores against the pooled null are head -0.26, tail -0.20,
  trunk +0.13; the trunk-head gap is z = 0.32. The record CANNOT
  resolve a plane axis at 2 sigma. exp83's direction gate demanded
  an ordering the record itself does not support.
- UP-G2 REFUTED honestly — and the refutation is the finding: the
  uniform coin (nb_p=0.8, exp64's anchor) at 24 fresh seeds/plane
  lands INSIDE the sampling-aware per-plane tolerances (head 1.0 vs
  tol 0.48; trunk 0.75 vs tol 0.245; tail 0.833 vs tol 0.708) and
  the POOL matches at 0.790 vs 0.799 (a 0.009 match, UP-G3 PASS) —
  but the DIRECTION gate still fails: sim head 1.0 > trunk 0.75.
- THE ATTRIBUTION (Panel E, the registered rule's investigation
  branch): the coin is EXONERATED — the biology baseline with the
  coin OFF is b_head = 0.70 vs trunk 0.00, tail 0.00 (n=10): the
  sim's HEAD regen is intrinsically fragile. The head err profile
  along the regen axis is [7.8, 6.4, 5.2] (flat-to-declining, no
  inheritance decay) vs trunk [1.0, 2.7, 2.5] — TARGET-INTRINSIC
  (read-side): the head plane's regen read does not reproduce the
  sharp anterior target from the first inherited cell onward. The
  dominant fired criterion is 'err' (70%). (The naive direction
  probe — flipping the walk flag — was rejected as CONFOUNDED in
  this machinery: the flag determines which face has committed
  neighbors; the err-profile probe attributes without touching the
  walk.)
- UP-G4 DISPOSITION (binding rule, investigation branch): **M37-A'
  REFUTED AS MIS-TARGETED** — per-plane penetrance anchors would
  compensate (p_head would drop to 0.167) for a biology the
  penetrance layer does not own. The repair RE-REGISTERS to the
  regen layer: the head-plane regen read's identity sharpness. THE
  GENE LAYER CLOSES: the coin's rates are plane-flat, the pool
  matches at adequate n (0.009), and the plane inversion belongs to
  the regen machinery where it can actually be repaired.
- UP-G5 PASS — the baseline deposited (head 0.70 / trunk 0.00 /
  tail 0.00, n=10 each) with the seed count and the criteria split.
- NEXT (derived): the regen-read upgrade — the non-junctional spec
  read (M33, the exp79-verified architecture) applied to the chain
  regen walk; it targets the head-plane read fragility (exp85) and
  the graph regen-walk limitation (exp81) with one mechanism.

## L68 — exp86 THE REGEN-READ UPGRADE (5/5 — the exp85 repair CLOSES; a coin-digest ARTIFACT found and repaired)
- THE IN-RUN FINDING FIRST: the composition panel of the first pass
  exposed a DEFECT in the adopted M37-A coin machinery — the
  digest window for a fully-anterior region (idx[0]==0) landed
  inside the WOUND state (constant theta), so the coin's draw was a
  CONSTANT on the head plane: u = 0.212 for every seed (measured,
  Panel E), i.e. the coin fired 100% on head regardless of nb_p —
  penetrance SATURATED. exp85's direction-gate failure (head 1.0 at
  n=24) was this artifact ON TOP of the real biology (0.7 coin-off
  fragility); exp83's trunk-anchored pool closure is untouched (the
  trunk window was already intact-side and varies by seed). THE
  CORE REPAIR: the digest window now centers on an INTACT face cell
  (the anterior face when it exists — bit-exact with the old code
  for every region with idx[0]>0, same src0 same window — else the
  posterior intact face). 67/67 tests green after both core edits.
- RR-G1 PASS — **THE HEAD-PLANE FRAGILITY CLOSES**: the M33-gated
  read (phi_readout=0.75, spec_min=NEURAL_SPEC_MIN,
  spec_read_bypass_gap=True) drops b_head from 0.70 to 0.00 (n=10)
  while trunk/tail stay 0.00 — the read repairs the read-side
  fragility and touches nothing else (the M33 domain discipline,
  TC-G5's chain analog: the read fires only where the stored
  identity is above the neural line).
- RR-G2 PASS — **JUNCTION INDEPENDENCE, both operating points**: at
  gap_scale=0.2 the M25 guess carries (1-r)=0.8 of the committed
  identity and the blend is diluted (no_read 1.0, blend 1.0) — the
  M33 POLE read in the guess path (neural_readout, the
  non-junctional anterior read) restores b_head to 0.00. The same
  architecture now covers both operating points: the spec blend at
  healthy junctions, the pole read through the guess at damaged
  junctions — the read that does not ride the junction, at both.
- RR-G3 PASS — **THE GENE LAYER RECOMPOSED**: coin (nb_p=0.8) + the
  upgraded read at 24 fresh seeds/plane: head 0.83 / trunk 0.75 /
  tail 0.83 — the direction gate passes (head <= trunk + 2*se_sim)
  and the pool lands 0.767 vs the record's 0.799 (a 0.032 match).
  The plane profile is now flat-and-consistent — the coin's
  penetrance (repaired digest) plus the repaired read produce the
  record's structure with no per-plane parameters.
- RR-G4 PASS — NO REGRESSION: the control arm stays structurally
  0.00 under the upgraded read; the generic family's sim pooled
  rate 0.623 inside the corrected band [0.485, 0.685] (the exp83
  record correction holds through the read upgrade).
- PE-G1 PASS — the digest artifact VERIFIED and deposited (old
  window u [0.212 x4] vs repaired [0.308, 0.419, 0.206, 0.696]).
- THE GENE-LAYER SCOREBOARD, final: GL-G1/G2/G5 (exp60); M37-A
  adopted (exp64), pool-validated (exp83), digest repaired (exp86);
  M37-B refuted (exp64), superseded by the record correction
  (exp83); M37-A' refuted as mis-targeted (exp85); M40 adopted
  (exp69); GL-G3 closed (pool + profile, exp86); GL-G4 closed
  (exp83). THE GENE LAYER IS CLOSED END TO END.
- NEXT (derived): the graph-native multi-region reader (exp81's
  regen-walk limitation + exp86's chain machinery are the same
  architecture — carry the M33-gated read into regrow_graph);
  corpus MAE residual; compiler v5.

## L69 — exp87 COMPILER V5: THE READER CONNECTED (5/5 — the exp81 write-only limitation RETIRES; the domain rule R7 verified)
- THE INSTRUMENT FINDINGS (all in-run, before any gate fired, each
  verified by direct measurement):
  F1. exp81's verify executed the trigger regen on a BARE collective
      — phi_spec ABSENT (the constructor never sets it) — the walk's
      spec read returned None and the blend never fired: the trigger
      regen was PURE INHERITANCE. "The regen walk re-derives the
      WILDTYPE beyond the cut" was never a walk limitation; the read
      was never CONNECTED to the compiled target. v4's write-only
      sidestep patched an instrument gap.
  F2. The corpus blend (phi=0.75) carries an inheritance term that
      is actively WRONG for a novel zone (nothing to inherit — the
      face identity is not the spec); exp79's verified reader
      commits at w=1.0, and v5 adopts it.
  F3. The programs never specified an OPERATING POINT; the rebuilt
      zones eroded during the walk/settle under the two-channel
      dynamics (a -20 zone in a -50 surround). exp79's star result
      IS the answer: v5 emits (gamma=64, mu=0) as the R7'
      operating-point precondition — and the erosion freezes
      (zone errors drop from 6-16 mV to 0.29-0.73).
  F4. The bare collective is FLAT -50 — no wildtype body plan — so
      every trunk-plane program carried a constant +15 RMS ghost
      (25 head cells x |(-50)-(-20)| / sqrt(100)). The verify must
      establish the canon animal first.
  F5. A zone that overhangs its amputated slice keeps clamp-era
      residue OUTSIDE the slice, and the residue sits near the spec
      by construction — the verification reads residue, not program.
      The instrument requires zones fully contained in the slice.
- CV-G1 PASS — **THE READER CONNECTED**: v4 reproduces the failure
  (0/6); v5 (the R1 memory write via write_spec_layer + the exp79
  reader weight + the M33 gate + the star point) verifies 6/6 with
  whole-body error 0.29 mV. The write-only limitation RETIRES.
- CV-G2 PASS — **THE DOMAIN RULE (R7)**: 8 below-line specs beyond
  the carried identity's resolution: the gated read refuses ALL 8
  on the plain substrate (the walk re-derives the canon — the gate
  holds); the latch substrate verifies 8/8 (the R1'' machinery
  covers the domain gap). The read's domain is structural (exp79
  TC-G5, exp86) and now carries a compile rule: below-line zones
  REQUIRE the latch.
- CV-G3 PASS — **THE MULTI-REGION COMPOSITION**: 10 mixed-domain
  specs: the latch verifies 10/10 end-to-end; the plain substrate
  shows the DOMAIN SPLIT in 10/10 (the above-line zone within bar
  through the read, the below-line zone outside bar through the
  refusal) — the domain rule is a property of the READ, not of the
  substrate.
- CV-G4 PASS — **THE GRAPH SUBSTRATE**: the multi-region reader on
  the grid (R5-passing) at the star point: 5/5 specs restore ALL
  above-line zones (in-zone theta err 0.5-0.7 mV) through one BFS
  walk with the per-cell domain gate; the below-line zones fail
  exactly as the rule demands (7.0-9.7 mV — the carried canon).
- CV-G5 PASS — STABILITY: 4/4 compiled anatomies hold 100
  generations at the star point (the TC-G3 zero-remodeling
  semantics applied to compiled anatomy).
- 67/67 tests green after the core additions (write_spec_layer —
  additive and inert; the exp86 coin-window repair unchanged).
- THE STAGE-3 SCOREBOARD after v5: the compiler WRITES, REGENERATES,
  and STATES ITS OPERATING POINT — R1 (clamps) + R1' (latch) + R2
  (trigger, now reading the connected spec layer) + R3 (coupling
  preconditions) + R4 (repertoire) + R5 (substrate partitioning) +
  R6 (maintenance schedules) + R7 (the domain-to-substrate rule) +
  R7' (the operating-point rule). The generator's space, the
  dynamic envelope, and the read's domain are one audited pipeline.
- NEXT (derived): the corpus MAE residual (0.522 -> <0.15, the
  Stage-2 closure); Stage-4 maintenance frontier completion;
  quest 001 on the restored quota (ZAI-OK verified this session).

## L70 — exp88 THE CORPUS RE-WIRING (3/4 — the stale block collapses, the residual NAMED; the <0.15 target not reached this pass)
- THE DECOMPOSITION FINDING (in-run, pre-work): exp70's corpus MAE
  0.522 was dominated by ONE STALE BLOCK — ('generic','trunk') n=256
  contributing 229 (43%): sim 0.0 vs recorded 1.0. The cause was
  WIRING, not mechanism: exp70's run_arm dropped exp60/exp83's 24h
  PROTOCOL-DEVELOPMENT window (the phenotype develops before the
  cut; exp83's verified N1 protocol includes it). The neoblast arm
  predated exp86 (no digest repair, no M33 read, a stray
  commitment_diffusion term); the cutting group's 1.0-series
  contradicts the DB's own control family (0.0 head / 0.38 trunk /
  0.49 tail by plane); the morphogen wnt rows record ~0.40 (partial
  drug modulation) vs the sim's full-corruption 1.0.
- THE RE-WIRING (no fitted parameters): C1 the 24h protocol window
  restored to every corpus arm; C2 the neoblast arm = the exp86
  adopted composition; C3 the generic family scored against exp83's
  ledger-owned corrected target; C3' the per-plane control anchor
  (the exp83 instrument extended); C4 the pre-registered
  scoring-inconsistency exclusion (cutting rows at recorded >= 0.9
  whose plane's control rate <= 0.35 — 21 rows, n=21).
- CW-G1 PASS — the stale block collapses: the generic trunk arm
  0.0 -> 0.667 (exp83's verified protocol).
- CW-G2 PASS — NO-COOKING: the raw-record MAE 0.522 -> 0.365 under
  the re-wiring alone (no record correction).
- CW-G3 REFUTED honestly — the corrected-decoded MAE lands 0.304 vs
  the 0.30 bar (conservative variant: 0.320). The < 0.15 Stage-2
  target is NOT REACHED this pass.
- CW-G4 PASS — the residual NAMED with numbers: cutting 10.0%
  (the record's own series-variance floor on plain-cut rows —
  the same operation scores 0.0 in one series and 1.0 in another;
  the sim's cutting arm is the canon biology), morphogen 7.9% (the
  partial-modulation dose gap — exp40's (cns, diffusion) grid is
  the registered repair), other_rnai 7.2% (the generic-family
  residual above the corrected band), ion_channel 3.6%.
- THE STAGE-2 STATUS: the corpus integration metric improved
  0.522 -> 0.365 (raw) / 0.304 (corrected-decoded) by bringing the
  arm table up to the adopted stack alone. The registered repair
  for the next pass: wire the exp40 dose axis into the morphogen
  arms; the cutting-block floor is a RECORD property (the series
  variance), to be handled by the decoding discipline, not by the
  sim.
- NEXT (derived): the exp40 dose-axis wiring (the morphogen arms);
  quest 001 on the restored quota; the Stage-4 frontier completion.

## L71 — exp89 THE UNIVERSAL COMPILER (4/5 — R5' BORN: the refusal is a price tag; the chain-carry contamination found)
- THE DESIGN: exp87's v5 program semantics (the R1 memory write, the
  M33-gated reader at w=1.0, the star operating point) executed
  across the full 7-substrate battery (exp73's battery, verbatim)
  with the per-substrate canon (the BFS-order labeling — exp43's
  framing) and the BFS regen walk with the per-cell domain gate.
- UC-G1 PASS — **THE R5 SIGNATURE REPRODUCES AT DEFAULT (7/7)**: at
  (gamma=1, mu=0.015) the program verifies exactly where the
  compiler's own partition check admits it (path/grid2d/random6/
  small_world pass; torus/random3/scale_free fail — the exp43
  signature, now on the regen path, not just the write path).
- UC-G2 PASS — **THE STAR LIFT (7/7)**: at (gamma=64, mu=0) the same
  program verifies on EVERY substrate — errors 0.25-0.63 mV, the
  refused substrates included. **R5' (the conditional rule) is born:
  the partition refusal is an OPERATING-POINT statement, not a wall
  — "not writable at your operating point; the star architecture
  buys it."** The two-channel law's writability boundary and the
  compiler's refusal are the same object at two operating points.
- UC-G3 PASS — **THE DOMAIN IS SUBSTRATE-INDEPENDENT (7/7)**: the
  below-line program fails on every substrate EVEN at the star
  point — the M33 gate is identity-based (the neural line), not
  connectivity-based; the operating-point rule and the domain rule
  are ORTHOGONAL. (Instrument note, in-run: the first pass filtered
  the amputation region by domain — the below-line program then
  verified WRITE-ONLY with no regen at all; the trigger amputates
  the zone region regardless of domain.)
- UC-G4 PASS — STABILITY: 3/3 star-point programs hold 100
  generations on the R5-REFUSED substrates (random3/scale_free/
  torus) — the zero-remodeling semantics holds where exp43 said no
  attractor exists, because the star point is the architecture that
  creates it.
- UC-G5 REFUTED honestly — **THE CHAIN-CARRY CONTAMINATION**: the
  multi-zone program errs 5.77-8.5 mV on every substrate (bar 6.0).
  The mechanism: the BFS walk's below-line GAP cells (canon -50)
  inherit from the last committed cell — which is the NOVEL zone
  (-30) — the M25 inheritance chain carries THROUGH the novel zone
  and contaminates the canon gaps. exp87's chain runs never hit it
  (the face-anchored walk); the graph interior has no intact face.
  Root: the program's write_spec_layer OVERWRITES the distributed
  memory (phi_spec := the novel target), so the below-line cells'
  correct source (the canon memory, D3) is gone — the chain is all
  they have, and the chain is contaminated. REGISTERED REPAIR: the
  two-source read — the pole read (above-line, constitutive) plus
  the canon read (the pre-program distributed memory preserved
  outside the spec-layer write) for the below-line cells; the
  graph-native analog of the chain's face anchor.
- NEXT (derived): exp90 the two-source read (the canon-source
  repair); the exp40 dose-axis wiring (exp88's registered repair);
  quest 001 on the restored quota.

## L72 — exp90 THE TWO-SOURCE READ (4/4 — the multi-zone regen closes UNIVERSALLY; the exp89 UC-G5 diagnosis corrected)
- THE DIAGNOSIS CORRECTION (in-run, instrumented): exp89's UC-G5
  "chain-carry contamination" was the WRONG mechanism — the errors
  were bit-identical with and without the canon read because the
  multi program's GAP cells (between the zones) were amputated (the
  physical cut is contiguous: slice[first zone, last zone]) but the
  walk only rebuilt the ZONE cells — the gaps sat at WOUND state
  (theta -40, V -30) through the settle. The real defect: an
  amputate/walk-region mismatch. exp89's ledger entry stands as
  deposited; this entry supersedes its mechanism attribution.
- THE REPAIR (two pieces):
  1. the core's write_spec_layer preserves the pre-program memory
     as phi_spec_canon (additive; inert when no spec layer existed);
  2. the walk rebuilds the WHOLE amputated range, with the per-cell
     source gate: the pole read (phi_spec[i], above the line, w=1.0)
     + the canon read (phi_spec_canon[i], below the line) + the
     inheritance chain only when the canon memory is absent.
- TS-G1 PASS — **THE MULTI-ZONE PROGRAM VERIFIES 7/7 SUBSTRATES**
  (errors 0.49-0.70 mV, from exp89's 5.77-8.5): the multi-region
  novel-anatomy regen is UNIVERSAL at the star point — path, grid,
  torus, random3, random6, scale_free, small_world — the substrates
  exp43 said could not hold the partitions.
- TS-G2 PASS — the pole read is unaffected (the single-zone
  in-domain program 7/7).
- TS-G3 PASS — NO BACKDOOR: the below-line novel zone still fails
  7/7 — the canon read gives each cell its own coordinate identity,
  never the novel spec; the M33 domain rule survives the repair
  intact (the two sources are orthogonal: the constitutive pole
  above the line, the coordinate memory below it).
- TS-G4 PASS — THE CANON SOURCE IS LOAD-BEARING: stripping
  phi_spec_canon alone (the establishment, clamps, walk, dynamics
  identical) returns the failure on 6/7 substrates (errors
  8.05-14.05; random3 passes at 4.04 — the inheritance chain
  happens to carry canon there, an honest per-substrate note).
- 67/67 tests green after the core edit.
- THE ARC, now closed end to end: exp43 (the form is
  substrate-conditioned) -> exp79 (the star point writes any
  substrate) -> exp87 (the reader connected, the operating point
  emitted) -> exp89 (R5' the conditional refusal; the domain
  orthogonal) -> exp90 (the two-source read: the multi-region novel
  regen universal). The compiler's final rule set: R1/R1'/R2/R3/R4/
  R5/R5'/R6/R7/R7' + the two-source read.
- NEXT (derived): the exp40 dose-axis wiring (exp88's registered
  repair); quest 001 on the restored quota; the docs milestone for
  the session's arc (the scoreboard refresh).

## L73 — exp91 THE DOSE-AXIS REFUTATION + THE AMPLITUDE AXIS (3/6 — L70's registered repair REFUTED BY SATURATION as pre-registered; the amplitude axis born with a threshold structure; the corpus decoded MAE 0.304 -> 0.290)

- THE REGISTERED REPAIR, TESTED AS REGISTERED (Stage A): exp88's
  L70 repair — the exp40 (cns x diffusion) grid at regrow on the
  full-corruption morphogen arms — ran verbatim (30 cells x 3 seeds,
  wnt|trunk; corners on wnt|crosspiece / apc|trunk). The design
  review (pre-run) predicted the failure mode and the run confirmed
  it: the wnt/apc verdict fires PRE-regrow from the corruption
  itself (pattern_error >= 6.0 or head_likeness >= 0.7 already true
  before any regrow), so the commitment kwargs act on ~15 cells that
  cannot change the verdict.
- DA-G1 REFUTED — no grid cell lands in the pinned partial band
  [0.00, 0.50] (the block: 17 morphogen rows mapped to wnt|trunk
  with recorded < 0.5, eids 120-1706, span [0.00, 0.45], mean
  0.189); the grid is FLAT 1.0 across all 30 cells.
- DA-G2 REFUTED-BY-SATURATION (the named branch): flat grid ->
  Spearman undefined. The exp40 shape does not transfer to a
  saturated arm.
- DA-G3 REFUTED on one sub-check, honestly owned: the two
  load-bearing controls PASS (default-kwargs bit-exact True —
  explicit (cns=1, diff=0) is stream-neutral; dose protocol-scoped
  True — cutting|trunk inert to d=0.3), but the "kwargs live"
  sub-check is VACUOUS AS REGISTERED — it instrumented the boolean
  verdict, which cannot move under saturation. Registered-gate
  defect owned: the live check needed the continuous instrument
  (per-seed pattern errors). Secondary finding rescuing L70
  partially: the Stage-A corners show the commitment grid IS live
  where the verdict is unsaturated (wnt|crosspiece 0.0 -> 0.667 at
  (3, 1.5)) — the repair works on unsaturated slices, dies on
  saturated ones.
- DA-G4 PASS — THE AMPLITUDE AXIS IS MONOTONE: the migrated repair
  doses the corruption amplitude (theta interpolation toward the
  adopted full push; d=1.0 bit-exact vs exp88's arm; d=0.0 the
  plain protocol arm; zero new core code): wnt|trunk rates
  [0, 0, 1, 1, 1] across d in {0, 0.25, 0.5, 0.75, 1.0}, Spearman
  0.866. apc|trunk mirrors [0, 0, 1, 1, 1]; wnt|crosspiece stays 0
  (its phi_readout=0.75 regime resists the push at all doses —
  deposited as the slice's dose-response).
- DA-G5 PASS — the partial band is reached, with the structure
  named: the sim's amplitude response is a THRESHOLD between
  d=0.25 and d=0.5, not a graded curve at the registered grain
  (rates in {0, 1}); the record's partial block (mean 0.189) sits
  below the sim's threshold — the graded edge (1/3, 2/3 rates) is
  registered for exp92's fine ladder (d in [0.25, 0.5], 7 seeds).
- DA-G6 PASS — the corpus re-scored at the adopted d*=0.0 (closest
  to the block mean; one cell for the family, no re-selection, no
  new exclusions): decoded MAE 0.304 -> 0.290; raw 0.365 -> 0.436 —
  BOTH frames deposited because the family-level mapping is
  structurally wrong in opposite directions: the record's morphogen
  block is BIMODAL (30 rows at 1.0, 17 rows at < 0.5) and no single
  family dose fits both modes. The row-level mapping (by RNAi
  combination structure) is exp92's registered design.
- 67/67 tests untouched (no core edit; the corpus runner is
  experiment-local).
- NEXT (derived): exp92 the fine amplitude ladder + the row-level
  dose mapping + the unsaturated-slice rescue test (the commitment
  grid on wnt|crosspiece as a positive control); then R5' across
  the substrate battery; multi-zone regen scale-up.

## L74 — exp92 THE FINE LADDER + THE ROW-LEVEL DOSE MAPPING (2/4 — the graded edge EXISTS; the rescue confirmed; the class rule below bar; the split-frames verdict closes the morphogen residual's mechanism queue)

- FL-G1 PASS — THE GRADED EDGE EXISTS: the 7-seed fine ladder
  (d in {0.25..0.50}, wnt|trunk) resolves exp91's threshold into
  [0, 0, 0, 0.429, 1, 1] — the graded window is d in [0.35, 0.45]
  with the 3/7 rate at d=0.40. The record's partial block (mean
  0.105 on the 11 modulator-class rows) sits inside the sim's
  reachable regime; the pre-registered selection picked d_par=0.25
  (rate 0.000, closest to the block mean).
- FL-G2 REFUTED — THE CANONICAL CLASS RULE IS BELOW BAR: phi 0.375
  (50/78 mapped wnt|trunk rows) between effector-class membership
  (beta-catenin/apc/axin) and recorded >= 0.9 — directionally right,
  under the registered 0.4 bar. The record's dose structure is
  gene-specific beyond the canonical classes (effector RNAi rows
  with partial phenotypes exist, e.g. Dj-betacateninB+Dj-ndk 0.11).
  Deposited as the measured concordance.
- FL-G4 PASS — THE UNSATURATED-SLICE RESCUE: the full commitment
  grid on wnt|crosspiece (d=1.0) moves the verdict to 0.667 (from
  the 0.0 corner) — L70's registered repair has its positive
  control: the exp40 grid works where the verdict is unsaturated.
- FL-G3 REFUTED ON A SPLIT VERDICT, with two in-run repairs owned:
  (1) the first pass keyed arms without the dose class and
  reproduced exp88's mapping BIT-IDENTICALLY (0.365/0.304) — the
  row-level test was a NO-OP; repaired to dose-classed arm keys.
  (2) the second pass dosed the other_rnai wnt_pos/wnt_ant RNAi
  rows — raw worsened (0.381); repaired to the registered scoping:
  the partial-penetration dose applies to the morphogen DRUG rows
  only, the RNAI KNOCKOUT rows stay at the full arm. The final
  reading: decoded 0.304 -> 0.290 (beats L70), raw 0.365 -> 0.371
  (+0.006) — the both-frames bar missed by the raw frame alone.
- THE LESSON CHAIN (the deposit's core): family-level mapping
  (exp91) -> class-level mapping (exp92) -> the residual is
  WITHIN-CLASS heterogeneity — the modulator block's own spread
  (raw 0.05-0.45) disagrees with itself across frames: raw wants
  d ~ 0.40 (rate 0.429), corrected wants d ~ 0.0 (the corrected
  block sits at the control floor). The n-targets count check
  (1 target vs 2+ against the recorded values) shows no monotone
  structure — no pre-registerable within-class rule exists without
  anchoring on the recorded values (cooking). The morphogen
  residual closes as a RECORD property: the drug-dose identity of
  each row is not in the DB (exp33, L16 — no concentrations), so
  the row-level dose is unknowable from the record's structure
  alone.
- THE CORPUS STATUS (the Stage-2 honest scoreboard): decoded MAE
  0.290 (from exp70's 0.522, exp88's 0.304); the leading residuals
  are now cutting (10.0% share — the record's series-variance
  floor, a decoding-discipline property) and other_rnai (7.2%) —
  the morphogen block is down to 6.5% and mechanism-closed. The
  < 0.15 target requires record-side decoding discipline, not new
  sim mechanisms — the sim-side residual queue for Stage 2 is
  EMPTY.
- 67/67 tests untouched (experiment-local machinery).
- NEXT (derived): R5' across the substrate battery (the refusal
  price, open item #4); multi-zone regen scale-up (open item #5);
  quest 001 literature follow-up (the zai stream is live).

## L75 — exp93 THE REFUSAL PRICE BATTERY (4/4 — R5' characterized: the price is a dial distance, and it STRATIFIES INTO THREE CLASSES; the star point is overkill on the verify path)

- THE INSTRUMENT: exp89's machinery verbatim (the uc-in program,
  exp73's 7-substrate battery, 3 seeds); for every substrate
  REFUSED at the default operating point (gamma=1, mu=0.015), two
  one-dial ladders (gamma at default mu; mu at default gamma) plus
  the registered two-dial probe {(4,0), (16,0)}.
- RP-G1 PASS — the R5 partition reproduces 7/7 (the default verify
  agrees with the compiler's own partition check; writable at
  default: path 2.0 / grid2d 5.67 / random6 4.49 / small_world 3.64
  mV; refused: torus 8.0 / random3 9.11 / scale_free 11.08).
- RP-G2 PASS — the star lift reproduces 7/7 (errors 0.25-0.63 mV).
- RP-G3 PASS — every refusal is priced on the ladders. THE PRICE
  HIERARCHY (the deposit's core):
  * class I — WRITABLE AT DEFAULT (price 0): path, grid2d,
    random6, small_world.
  * class II — THETA-CHANNEL PRICED (mu->0 alone buys it, the
    gamma ladder FAILS at every gamma <= 64 at default mu): torus.
    The compiler-path attribution REVERSES exp78's write-path
    finding for torus (there gamma*=4 flipped it) — different path,
    different dominant channel; both are honest channel
    attributions of the same two-channel law.
  * class III — TWO-DIAL PRICED: random3 and scale_free verify at
    the registered probe (gamma=4, mu=0); NEITHER dial alone
    suffices for either.
- RP-G4 PASS — the stratification's hub prediction holds:
  scale_free's gamma ladder fails through 64 at default mu (the
  exp78 theta-channel plateau, now measured on the WRITE path).
- THE STAR POINT IS OVERKILL ON THE VERIFY PATH: the cheapest
  two-dial price is (4, 0), 4 gamma-fold below the star's (64, 0),
  with the same verify outcome. R5' final form: the refusal price
  is a CHANNEL-STRATIFIED dial distance — class II refusals are
  pure theta-channel debts (unbounded fold: mu must reach exactly
  zero), class III refusals are joint debts the V-channel ratio
  and the theta homogenization pay together.
- 67/67 tests untouched (exp89 machinery reused read-only).
- NEXT (derived): exp94 the multi-zone regen scale-up (the exp90
  two-source read beyond the 7-substrate battery); the reader
  extension to new topologies (the handoff's open item #6).

## L76 — exp94 THE MULTI-ZONE REGEN SCALE-UP (4/4 — the two-source read GENERALIZES: 11/12 new topologies verify including the n=200 scale; the deg-99 star is the reader's boundary, named)

- THE IN-RUN INSTRUMENT BUG (owned, the diagnostic chain): the first
  pass failed 0/12 UNIFORMLY (errors 8.5-14.6 on every new
  substrate INCLUDING path200, whose family verifies at 0.25 mV) —
  the uniform signature exposed the executor, not the mechanism.
  The phase-by-phase trace (canon/target/clamps/post-window state
  all bit-equal vs exp90's executor on the old battery) localized
  the divergence to the walk's canon branch: my added guard
  `canon_src[i] > 0` is NEVER TRUE because phi_spec_canon holds
  NEGATIVE voltages (mean -42.5) — the guard silently degraded
  every below-line cell to the wound-state chain read (the exp89
  UC-G5 failure mode, recreated by instrument). The canon gate is
  the SOURCE's existence (the attribute), never the value's sign.
  Repaired; the old battery reproduces exp90's 0.49-0.57.
- THE K=8 FALLBACK (owned): the pairing model fails at k>=8, n=100
  (exp73's note); the dense case runs as the deterministic degree-8
  circulant.
- MS-G1 PASS — 11/12 new substrates verify (>= 2/3 seeds, star
  point): tree 0.52 / cycle 0.53 / ladder 0.52 / barbell 0.88 /
  complete-K60 3.34 / bipartite-K50,50 2.92 / grid_elong 0.50 /
  torus_elong 0.53 / circulant-k8 0.59 / path200 0.49 /
  scale_free200 0.61 mV. The dense extremes cost more (K60 3.34,
  bipartite 2.92) but hold inside the bar.
- MS-G2 PASS — NO BACKDOOR 12/12: the below-line variant fails on
  every new substrate — the M33 domain rule survives the scale.
- MS-G3 PASS — THE CANON SOURCE IS LOAD-BEARING 12/12: the
  stripped-canon variant fails on every new substrate — the
  two-source structure (not the chain) carries the regen.
- MS-G4 PASS — THE SIZE SCALE: both n=200 variants verify (path200
  0.49, scale_free200 0.61) — the reader scales in n.
- THE NAMED BOUNDARY: the deg-99 STAR fails (8.53 mV, the only
  refusal) — the hub extreme where the V-channel ratio (the hub's
  g_total ~ n·g makes it a V-sink during the 15h settle) drags the
  rebuilt spokes off their canon values. Registered: exp95 tests
  the prediction that the boundary is an OPERATING-POINT statement
  (R5' again) — at lower gamma (the ratio closer to 1) the spokes
  should hold; if (4, 0) or (1, 0) verifies the star, the reader
  generalizes 12/12 and the boundary is priced, not absolute.
- NEXT (derived): exp95 the star-boundary pricing (the deg->n
  limit vs the operating point); the docs milestone (the
  scoreboard refresh with L73-L76 + the two new figures).

## L77 — exp95 THE STAR-BOUNDARY PRICING (0/3 — the refutation that CLOSES R5' honestly: the deg-99 hub refusal is ARCHITECTURAL, not an operating-point statement; the hub is a single-point integrator; exp96 registered on the anchor theorem)

- THE REGISTERED PREDICTION, REFUTED ALL THREE WAYS: (SB-G1) no
  (gamma, mu) cell in the grid {1,4,16,64} x {0.015, 0} verifies
  the star — the boundary is NOT priced within the dial plane;
  (SB-G2) the mu clause holds (mu=0.015 fails at every gamma) but
  no (gamma, 0) cell verifies either — the dials are necessary and
  jointly INSUFFICIENT; (SB-G3) the registered reversal was
  BACKWARDS — the errors DECREASE with gamma (9.01 -> 8.53,
  Spearman -1.0): the original ratio law holds (higher gamma ->
  weaker hub coupling), the head researcher's registered
  hub-sink reasoning was wrong and is owned.
- THE MECHANISM THE DATA NAMES (the deposit's core): the star's
  failure is not the dials' — it is the TOPOLOGY. Every rebuilt
  spoke's only neighbor is the hub; during the settle each spoke's
  V relaxes toward the hub, and the hub integrates the entire disc
  (one node averaging 99 edges). The settle therefore homogenizes
  the pattern through the hub at ANY operating point — the target's
  spatial identity (zones at -30 vs gaps at -20/-50) is destroyed
  by single-point integration, leaving the ~8.5-9 mV floor. The
  star is the anti-reader topology: maximal integration, zero
  lateral coupling.
- THE ARC CONSEQUENCE: R5' ("the refusal is an operating-point
  statement") is now BOUNDED, not universal — it held on 11/12 of
  exp94's battery and on all of exp89's; the deg-99 star is an
  ARCHITECTURE refusal. The two-channel law's writability boundary
  and the reader's domain boundary are the same object only up to
  topology: the dials move along the channels; they cannot remove
  the integrator.
- THE REGISTERED REPAIR (exp96, the anchor theorem returns): the
  exp75-77 theorem — coherence requires an anchor slower than the
  hijack — applied to the reader: CLAMP THE HUB to its canon
  identity during the settle (the program already owns clamp
  machinery; the hub is intact tissue). Prediction: with the
  hub anchored, the spokes relax to the canon hub and the multi
  program verifies at the star point; the reader generalizes
  12/12 and the exp75-77 theorem closes on the reader arc.
- 67/67 tests untouched (exp94's executor gained a backward-
  compatible op kwarg; exp94's deposited results unchanged).

## L78 — exp96 THE HUB ANCHOR (1/4 — the simple anchor REFUTED and the boundary MECHANIZED: all zones HOLD on the star; the failure is the gaps/intact tissue relaxing through the single-point integrator; a one-value clamp cannot hold a heterogeneous pattern)

- THE REGISTERED REPAIR, TESTED AND REFUTED: clamping the hub to
  its canon identity through the 15h settle (released 1h before the
  read) leaves the star's multi-program error at the exp95 floor
  (8.51 vs 8.53) — HA-G1/HA-G2/HA-G4 REFUTED. HA-G3 PASS (the
  anchor is harmless: tree 0.52 / cycle 0.53 still verify).
- THE DIAGNOSTIC THAT LOCALIZES THE MECHANISM (one-run, deposited):
  per-zone means on the failed star run are z0 -29.7 / z1 -29.9 /
  z2 -30.0 — ALL THREE ZONES HOLD. The pole read fires fine; the
  rebuilt zone cells are exact. The pattern error (8.53) lives in
  the GAP cells (between zones) and the INTACT spokes (76-99):
  they relax toward the hub's mean during the settle — the hub
  integrates the entire disc and the -20/-50 identity of the
  non-zone tissue decays toward the -30 zone average.
- WHY THE ANCHOR CANNOT WORK (the theorem's boundary, now stated
  precisely): the hub's correct state IS one value (canon -20) —
  clamping it changes nothing structural, because the drift is in
  the SPOKES coupling THROUGH the hub; a one-value clamp just
  re-biases which way the averaging pulls (the anchored floor is
  the same 8.5 by error redistribution). Holding the spokes would
  be the whole-pattern clamp — the trivial non-mechanism. The
  exp75-77 anchor theorem applies when ONE node's slow state
  anchors MANY; the star is the inverse case — ONE node
  integrating MANY, which no per-cell program vocabulary (clamps,
  walks, reads) can hold heterogeneous identity against.
- THE READER'S DOMAIN RULE, FINAL FORM: the two-source read
  generalizes to every topology tested (exp90's 7 + exp94's 11/12)
  EXCEPT the single-integrator extreme (deg -> n). The boundary is
  mechanized: local per-cell programs cannot preserve a
  heterogeneous pattern against a topology whose single node
  averages the whole sheet. The star graph is to the reader what
  the scale_free hub was to the write path (exp73-79) — but THERE
  the dials bought it, and HERE they cannot: the integration is
  topological, not a channel setting.
- REGISTERED (exp97, optional — an architecture extension, not a
  quick run): a per-edge hub anchor (the hub speaks a different
  value to each neighbor — beyond the current program vocabulary;
  the minimal architecture that can hold the star). Deposited as
  the reader's open frontier; the 67/67 suite untouched.

## L79 — exp97 THE COVERAGE REPAIR (5/5 — the probe that REFUTES L77-L78's mechanism: the star's 8.5 floor was ~32 amputated-never-rebuilt cells at wound state, an EXECUTOR COVERAGE ARTIFACT; the repair verifies the star at 1.02 mV and the reader's domain is 12/12 — there is NO topological boundary)

- THE FORK DECISION (owned, per the standing order that a flagged
  fork is a decision point): L78 registered exp97 as a per-edge hub
  anchor. The pre-design probe MOOTED the registered design — you
  do not build signaling architecture for cells that were never
  rebuilt. exp97 was re-aimed at what the probe actually found.
- THE PROBE (one run, decomposition deposited in
  results/exp97_coverage_repair.json as the two *_state arms): the
  star's error is STATIC — post-walk 8.52 -> post-settle 8.53 ->
  post-release-1h 8.53. Nothing relaxes through anything. The
  deposited 8.53 decomposes exactly: head-gap cells 12-24 at -40 vs
  target -20 (12 x 399), trunk-gaps 25-29 + 46-59 at -40 vs -50
  (19 x 101), boundary cell 12 (361), hub drag (79 — the hub is
  intact but was dragged ~9 mV off canon by integrating the wound
  cells during the window/walk), z1 residual (106). The coverage
  hole is ~93-97% of the squared error.
- THE MECHANISM: the amputation range reg_walk spans the inter-zone
  gaps (cells 2-75), but the blastema frontier was enumerated over
  the ZONE UNION reg_idx only. On a laterally CONNECTED region the
  BFS walks through the region and covers the gaps; on the star
  every spoke's only neighbor is the intact hub, so the BFS
  dead-ends and ~32 amputated cells sit at blastema theta -40
  forever. The executor promised the pattern the compiler had
  already certified (exp94's R5 partition check: star COMPILABLE).
- WHAT DIES (the honest kill list): exp94's star row (0/3, 8.53 ->
  actually 3/3, 1.02 under repair); exp95 ENTIRELY — the pricing
  grid measured the artifact (the errors-decrease-with-gamma trend
  was gamma pinning the REBUILT cells harder against the static
  wound mass, not hub-sink physics); exp96's star arms (the anchor
  "failed" against a coverage hole — nothing moves in the settle,
  so no settle-side intervention could ever matter); the L77-L78
  mechanism story (single-point integration, the anti-reader
  topology, the topological boundary). WHAT STANDS: exp93's price
  hierarchy (the star was never in it), exp96's HA-G3 (tree/cycle
  anchored no-harm), the two-source architecture itself
  (exp89/exp90), R5' on the write path, the corpus result.
- THE REPAIR (backward-compatible): frontier_mode="walk" in
  execute_two_source_n enumerates the wound frontier over the whole
  amputation range — the honest blastema semantics (every amputated
  cell adjacent to intact tissue IS a frontier cell; on the star,
  that is all of them). Default "zones" is BIT-EXACT with every
  deposited run (re-verified in-run: tree seed 1 = 0.56, star
  zones-mode = 8.53). The 67/67 suite untouched.
- THE GATES 5/5: CV-G1 the artifact pinned (zones-mode 0/3 at
  8.53); CV-G2 the repair buys the star (3/3 at 1.02 mV — the
  predicted 0.5-1.5 band: the residual is the hub's window-drag
  and z1's committed spread, not gaps); CV-G3 static under repair
  (post-walk 0.91 -> post-settle 1.02 — noise, no homogenization);
  CV-G4 the repair is universal (tree 0.53 / cycle 0.53 /
  grid_elong 0.51, all 3/3); CV-G5 the domain rule survives full
  coverage (below-line z1=-59: 0/2 — the M33 boundary is real;
  no-canon: 0/2 at 11.66 — the canon source is load-bearing).
- THE READER'S DOMAIN RULE, ACTUAL FINAL FORM: 12/12 — exp90's 7 +
  exp94's 12 INCLUDING the star. No topological boundary exists on
  this battery. The boundary hunt produced a better instrument, not
  a boundary — the exp75-79 write-path lesson in miniature: the
  refusal that survives scrutiny is the one you can build, and this
  one dissolved under decomposition. R5' ("refusal is a price tag")
  reopens UNBOUNDED — no architecture refusal is currently on the
  books.
- REGISTERED (exp98): the star's TRUE price ladder. exp95's
  (gamma, mu) grid is INVALIDATED (it measured the artifact); under
  the repaired executor, run {1, 4, 16, 64} x {0.015, 0} x 3 seeds
  on the star: does the star price like the two-dial class
  (random3/scale_free at (4,0)), the theta-priced torus class
  (gamma ladder fails through 64), or writable-at-default? The
  per-edge hub anchor stays retired unless a REAL refusal
  (verified-read failure under full coverage) reappears.
- ALSO DEPOSITED (subagent 2-b, parallel): the Stage-5 WET-LAB
  COMPANION PROTOCOL (docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md) —
  W1-W5 pre-registered bench gates: the octanol/heptanol dose
  ladder (the record has no concentrations; the dosing table IS the
  deliverable), the two-source anterior/posterior asymmetry, the
  price hierarchy across tissue contexts, the minimal multi-zone
  stripe write, and the record deposit schema. Written against
  L73-L76 only; the L77-L78 mechanism story excluded per this
  entry.
- INFRA NOTES (flagged, non-blocking): the push token needs
  rotation; quest 001's daemon is DOWN in this environment (ds
  --status unhealthy, UI bundles missing, no quest state dirs) —
  the zai proxy on :8787 is green; quest runs stay foreground-only
  until the daemon is rebuilt.

## L80 — exp98 THE STAR'S TRUE PRICE LADDER (3/3 boolean gates + the class call — the repaired star is ONE-DIAL-PRICED ON EITHER CHANNEL: gamma 2 at default mu, or mu 0.01 at gamma 1; the default refusal is a marginal uniform theta sag, NOT a boundary; R5' now has its cleanest price tag)

- THE CLASS CALL (exp93's ladder convention, V ladder checked
  first): V_PRICED with gamma_min = 2 (price 1.0 log2 fold-unit
  above the default (1, 0.015)). THE FULL STATEMENT the deposit
  carries: the mu ladder ALSO verifies one dial down (mu_max 0.01
  at gamma 1 — fold-price log2(1.5) = 0.58, CHEAPER by the fold
  metric); both one-dial cells are marginal verifies (err 5.41 and
  5.58 vs the 6.0 bar) while both dials (4, 0) 2.11 / (16, 0) 1.6 /
  the exp97 star point (64, 0) 1.02 verify with margin. The star
  joins exp93's taxonomy as the first substrate priced on the
  V channel by the ladder order — with the honest note that the
  theta route is the cheaper tag.
- THE DEFAULT REFUSAL'S SIGNATURE (one-run x 3 deposited): at
  (1, 0.015) the star fails 0/3 with err 6.23-6.27 — and ALL THREE
  ZONES HOLD within their bar (means -32.3 to -33.1 vs target -30):
  a UNIFORM ~2.7-3 mV sag across the rebuilt pattern, the theta
  channel pulling every rebuilt cell toward the hub's integrated
  mean (each spoke's only theta-neighbor is the hub; the hub
  integrates 99 thetas at 99*mu). L77-L78 had the right suspect on
  the wrong channel: the single-point integration is REAL — on
  THETA, where no clamp-and-release of V can touch it, and it
  PRICES at one dial instead of refusing.
- THE LADDER SHAPES: gamma ladder at default mu verifies at every
  gamma >= 2 with errors MONOTONE DECREASING (5.41 -> 4.10) — the
  same trend exp95 saw and misattributed to hub-sink physics; under
  the repaired executor it reads cleanly: higher gamma pins V to
  the committed theta harder against the mu pull. Mu ladder at
  gamma 1: verifies at every mu <= 0.01, errors falling to 3.93 at
  mu = 0. The theta channel carries the star's residual everywhere.
- THE READER'S DEFAULT CELL IS REAL (SL-G4): path(100) verifies at
  (1, 0.015), 3/3, err 2.91 — the two-source read had only ever run
  at the (64, 0) star point; the default cell verifies on a
  default-class substrate, so the star's default refusal is a
  PRICE, not a reader-wide gap.
- GATES: SL-G1 PASS (writable somewhere — 12 of 13 star cells
  verify); SL-G2 the class call deposited (V_PRICED, gamma_min 2;
  mu route noted cheaper); SL-G3 PASS on the fallback branch —
  weak as registered (the gamma ladder's RATES are trivially
  monotone at 1.0; the informative signature is the ERR trend and
  the uniform sag, both deposited); SL-G4 PASS.
- ARC CONSEQUENCE: R5' ("refusal is a price tag") now holds on the
  ENTIRE reader battery with no exceptions: every substrate in
  exp90's 7 + exp94's 12 verifies at SOME operating point, and the
  worst tag on the books is one dial (the star, on either channel).
  No architecture refusal exists anywhere in the compiled-reader
  domain. The per-edge hub anchor stays retired.
- REGISTERED (exp99): THE DEGREE LADDER — the boundary map open
  item. Stars of degree {9, 19, 49, 99, 199 (n=200)} x the cells
  that matter (default; the one-dial cells gamma 2 and mu 0.01; the
  two-dial (4, 0)): does the one-dial price RISE with degree (the
  hub's theta integration scales with deg), and is there a degree
  where one dial stops buying? If yes, the two-dial probe brackets
  the first REAL boundary with its price — if no, the map is flat
  and R5' closes as degree-invariant.

## L81 — exp99 THE DEGREE LADDER (3/4 — the price-vs-degree map is FLAT: the one-dial tags verify at EVERY degree through deg-199, the anchor holds 0.94-1.03 mV across the ladder; R5' closes DEGREE-INVARIANT; the rising-boundary prediction is refuted and DL-G1's band is owned as miscalibrated)

- THE MAP: 5 star degrees {49, 74, 99, 149, 199} x 5 cells x 3
  seeds. The DEFAULT cell refuses everywhere (rate 0/3, err
  6.22-6.34) — the marginal theta sag is a FIXED FEATURE of the
  star family, not a degree effect. The ONE-DIAL tags (gamma 2 at
  default mu; mu 0.01 at gamma 1) verify 3/3 at EVERY degree
  (errs 5.34-5.68) — the tag does not move. The two-dial (4, 0)
  improves with degree (2.31 -> 1.75 — more spokes, more
  averaging partners for the rebuilt cells); the (64, 0) anchor is
  degree-invariant at 0.94-1.03 (exp97's 1.02 sits mid-ladder).
- DL-G1 REFUTED AS REGISTERED, CONFIRMED IN SUBSTANCE (owned):
  Spearman(degree, default err) = -0.90 — but the MAGNITUDE is
  6.30 -> 6.22, a 0.08 mV drift over a 4-fold degree range (1.3%
  of the err). The registered dichotomy (flat |rho| < 0.6 vs
  rising rho >= 0.6) never allowed for a consistently-tiny
  negative trend sitting on a 0.1 mV noise floor — the band was an
  effect-size question measured with a rank-correlation gate.
  Owned: the gate was miscalibrated; the scientific result is the
  flat map (no degree dependence worth the name), the negative rho
  deposited for completeness. Next effect-size claims get
  effect-size gates.
- THE MECHANISM, CONFIRMED: the per-spoke coupling rates are
  degree-independent (each spoke sees the hub through ONE edge on
  each channel); the hub's faster integration at higher degree
  does not propagate back to the spoke side. The single-point
  integrator's price is a property of the TOPOLOGY CLASS (hub vs
  lateral), not of its degree.
- GATES: DL-G2 PASS (one-dial survival at every degree); DL-G3
  PASS (no boundary through deg 199); DL-G4 PASS (the anchor
  holds, mean err < 2.0 everywhere); DL-G1 refuted-as-registered /
  flat-in-substance (owned above).
- ARC CONSEQUENCE: the reader's boundary map is CLOSED and EMPTY —
  19/19 battery topologies verify at some operating point (exp97's
  repair + exp98's ladder + exp99's degree map), the worst tag on
  the books is one dial, and the tag is degree-invariant through
  n=200. R5' ("refusal is a price tag") has no counterexample left
  in the compiled domain. The per-edge hub anchor stays retired.
- REGISTERED (exp100): THE READER'S PRICE MAP — exp93's taxonomy
  was measured on the WRITE path (exp89's uc-in program); the
  READER's (two-source, exp90's) taxonomy is only annotated
  (default-class path at 2.91, exp98; the star one-dial, exp98;
  the battery ran at (64, 0) by convention). Run the adaptive
  ladder per battery substrate (exp90's 7 + exp94's 12): default
  cell (1, 0.015) x 3 seeds; refusals climb the exp93 ladders
  (gamma at default mu; mu at gamma 1; the two-dial probe). The
  deposit: the reader's price class per substrate — the map that
  turns the (64, 0) convention into a measured operating point.
- INFRA INCIDENT (owned, recovered): between the exp98 push and
  exp99's first run, the local repo was hard-rolled-back to
  2f01d22 (the exp91-batch pre-session commit) by an unknown actor
  (prime suspect: the timed-out figures subagent's session; no
  rogue process found alive afterward). origin/main was never
  touched (85ef5a8 throughout); `git reset --hard origin/main`
  restored the full tree bit-exact; exp99 (untracked at the
  moment) survived. core.filemode=false re-applied to kill the
  mode-churn noise the rollback re-enabled. THE LESSON: every
  milestone was pushed before the incident — the push-each-
  milestone discipline IS the disaster-recovery plan. The token
  rotation flag is now elevated: rotate before the next session.

## L82 — exp100 THE READER'S PRICE MAP (3/3 — exp93's taxonomy measured for the READER across the full 19-substrate battery: 4 DEFAULT / 6 V_PRICED / 9 TWO_DIAL, ZERO refusals; the tag tracks lateral connectivity; the reader prices >= the writer on every shared substrate; the dense extremes forced an in-run bracket extension, owned)

- THE MAP (adaptive ladders, 3-seed default cells, 2-seed ladder
  screens + 3-seed confirms; deposited per cell):
  DEFAULT (4): path (2.91), path200 (2.38), cycle (3.67),
  small_world (4.23) — the low-degree lateral topologies verify at
  the reader's own default cell (1, 0.015).
  V_PRICED (6): star gamma_min=2, ladder 32, random6 32, grid2d 64,
  grid_elong 64, tree 64.
  TWO_DIAL (9): (4,0) random3/random8/scale_free/scale_free200/
  torus/torus_elong; (16,0) barbell; (32,0) bipartite/complete.
  PM-G1 PASS (19/19 classes), PM-G2 PASS (zero refusals), PM-G3
  PASS (3 classes present).
- THE STRATIFICATION'S SHAPE: the tag tracks LATERAL
  CONNECTIVITY — degree-2 chains and rings hold at default; branching
  and grid topologies need the V pinning (gamma up); random, hub,
  and dense families need theta cut AND V pinned. The star is the
  CHEAPEST V-priced member (gamma 2): after the coverage repair its
  spokes each have exactly one edge to pin — the "worst" write-path
  topology is the best-priced V-member on the reader. The inversion
  the maps produce is the point: price is a per-path property, not
  a substrate constant.
- THE CROSS-PATH ASYMMETRY (new, deposited): on all 7 substrates
  shared with exp93's WRITE-path taxonomy, the reader's tag is >=
  the writer's (path =, small_world =, random3 = (4,0),
  scale_free = (4,0); grid2d DEFAULT -> V(64); random6 DEFAULT ->
  V(32); torus one-dial theta -> TWO_DIAL). Strictly higher on 3 of
  7. The mechanism is structural: the reader's verify bar includes
  the post-window settle the writer never faces — the pattern must
  HOLD after the forcing releases, so every sag the writer can
  ignore becomes a price.
- THE BRACKET EXTENSION (owned, in-run): the registered two-dial
  probe {(4,0), (16,0)} came from exp93's WRITE-path stratification;
  bipartite and complete priced ABOVE it (their (64, 0) verifies,
  exp94 MS-G1, were never in question) — the bracket extended with
  {(32, 0), (64, 0)} and both confirm at (32, 0) x 3 seeds. The
  dense extremes are the reader's most expensive members: a K60
  clique's every cell couples to 59 others — the sag the dials
  fight is the whole-clique mean, not a local neighborhood's.
- ARC CONSEQUENCE: R5' is now MEASURED on both paths and the full
  battery — the reader's operating point is no longer a convention:
  (64, 0) was paying the MAXIMUM price for every substrate; the map
  says 15 of 19 verify for less. The dials are a budget, and the
  budget is now published per substrate, per path.
- REGISTERED (exp101): THE ZONE-COUNT LADDER — the compiler's
  zone-resolution limit. MULTI carries 3 zones; how many can the
  two-source read hold? 4/5/6-zone MULTI variants at n=100 on three
  representative substrates (path, grid2d, torus) x 3 seeds at each
  substrate's minimal cell from this map. Gates: the max zone count
  per substrate deposited; the partition check's verdicts vs the
  executor's (does the compiler's R5 partition over-promise?); the
  failure mode of the first zone-count refusal (uniform sag vs
  zone-merge).

## L83 — exp101 THE ZONE-COUNT LADDER (2/4 as registered — and both refutations are the payload: the grid's zone-resolution "limit" is a PRICE one dial buys (six zones verify at 0.58-0.62 mV at (64, 0)), and the compiler's R5 partition check is exposed as a chain-era artifact that UNDER-promises 10 of 12 pairs against its own executor; exp102 registered: R5 recalibrated from boolean gate to price oracle)

- THE LADDER (k in {3,4,5,6} all-at--30 specs, one substrate per
  exp100 reader-price class, each at its OWN minimal cell):
  path (DEFAULT (1, 0.015)): k3 2.91 / k4 3.51 / k5 3.24 / k6 3.59,
  ALL VERIFY — a chain holds six zones at its default cell.
  torus (TWO (4, 0)): 3.82 / 3.97 / 4.27 / 3.93, ALL VERIFY.
  grid2d (V (64, 0.015)): k3 5.00 VERIFIES; k4 6.07 / k5 6.74 /
  k6 6.25 — 0/3 each, JUST over the 6.0 bar.
- THE DIAL DIAGNOSTIC (deposited as the *_dial arms): the grid's
  zone-count refusal is a PRICE, not a boundary — at (64, 0) the
  k4/k5/k6 specs verify at 0.58/0.62/0.61 mV (BETTER than the k3
  5.00 at (64, 0.015): the mu cut removes the theta sag entirely,
  and wider zone coverage leaves fewer canon-gap cells to sag);
  at (4, 0) they verify at 3.43-3.77. The zone-resolution limit on
  the grid was ONE DIAL away the whole time. ZC-G1 refuted at the
  minimal cells, repaired in-run: the reader holds SIX zones at
  n=100 on all three substrates at SOME operating point.
- ZC-G3 PASS (the k=6 below-line variant, zone z2 at -59: 0/2 on
  path — the M33 domain rule scales with zone count); ZC-G4 PASS
  (k=6 err within 2x of k=3 everywhere — resolution has a bounded
  price on the minimal-cell path too).
- THE PARTITION DISCONNECT (the second payload, ZC-G2 REFUTED with
  the opposite sign from the registered concern): the compiler's
  R5 substrate_partition_check refuses 10 of the 12 (substrate, k)
  pairs deposited today — grid2d and torus at EVERY k including 3,
  path at k5/k6 — while the executor VERIFIES those pairs at the
  mapped operating points (9 of the 10 at the minimal cell alone).
  The check measures the identity partition's boundary-to-volume
  ratio (crossing edges / total edges) against R5_MAX, calibrated
  by exp43's WRITE-path attractor signature in the chain era —
  before the two-channel law, the dials, and the two-source read.
  The position-addressed read does not need the lateral attractor
  coherence the ratio measures. THE CHECK IS REFUSED BY ITS OWN
  EXECUTOR. (Deposit note: exp94's r5_partition console values are
  not in the results JSON — results/ gitignore gap, flagged; the
  disconnect stands on exp101's fresh 12-pair deposit.)
- REGISTERED (exp102): R5 RECALIBRATED — from boolean gate to
  PRICE ORACLE. The ratio is not useless, it is misread: the
  registered gates (a) formalize the boolean's false-refusal count
  against executor verdicts; (b) test whether the ratio PREDICTS
  the reader's dial cost (Spearman >= 0.6 across the 19 substrates
  of exp100's map — the classes look ratio-ordered: degree-2
  chains DEFAULT, grids/trees V-priced, dense cliques two-dial);
  (c) test whether the ratio orders the two-dial brackets; (d)
  test the oracle's degree-flatness on the star family (the ratio
  is degree-constant on stars — every spoke edge crosses to the
  unzoned hub — matching exp99's flat map). If the oracle holds,
  R5's compile decision becomes: the ratio NAMES THE PRICE, the
  dials pay it — a refusal only when the price exceeds the dial
  plane (none found battery-wide).

## L84 — exp102 R5 RECALIBRATED: THE PRICE ORACLE (4/4 — the chain-era boolean is dead as a gate (16/19 false refusals) and the boundary-to-volume ratio is reborn as the reader's PRICE ORACLE: Spearman 0.73 with the dial class, class means monotone, brackets ordered, degree-flat on stars; the compile decision's new form: the ratio NAMES THE PRICE, the dials pay it)

- RO-G1 PASS — the boolean is dead: substrate_partition_check at
  the default R5_MAX refuses 16 of the 19 battery substrates whose
  minimal cells ALL verify (exp100). It never gates the compile
  path (advisory-only, caller audit deposited) — the refusals were
  printouts, not blocks — but as a feasibility statement it is
  refuted by its own executor on 84% of the battery.
- RO-G2 PASS — the oracle rises: Spearman(boundary-to-volume,
  ordinal dial cost) = 0.73 across the 19. The named outliers,
  both directions, deposited with the rows: random6 (ratio 0.119)
  and random8 (0.146) price ABOVE their ratio (the k-offset
  circulants are boundary-thin yet dial-hungry — the exp73 pairing
  caveat's family); the star (0.404) prices BELOW its ratio (the
  unzoned hub puts every zone-spoke edge in the crossing count —
  the pre-declared artifact; post-repair its spokes have one edge
  to pin, gamma 2).
- RO-G3 PASS — the oracle resolves: class-mean ratios monotone
  (DEFAULT 0.07 < V_PRICED 0.358 < TWO_DIAL 0.501) AND the
  two-dial brackets ordered ((4,0) mean 0.463 < (16,0) 0.483 <
  (32,0) 0.622) — the dense extremes the exp100 bracket extension
  caught are exactly the ratio's top tail.
- RO-G4 PASS — degree-flat on stars: the star-family ratio is
  0.402-0.408 (std 0.0022) across deg {49..199} — matching exp99's
  degree-invariant price map. The oracle's star pricing is a
  property of the topology CLASS, as the mechanism says.
- THE RECALIBRATION (the compile decision's new form, annotated in
  substrate_partition_check's docstring): the boolean stays as the
  exp43/exp47 WRITE-path-era signature it was calibrated to be;
  for the two-source read, the ratio NAMES THE PRICE (oracle
  v1: DEFAULT below ~0.15, V_PRICED through ~0.45, TWO_DIAL above,
  outliers named), the dials pay it, and a refusal exists only
  where the price exceeds the dial plane — never observed
  battery-wide. R5's slogan survives both paths intact: refusal is
  a price tag.
- REGISTERED (exp103): THE RESOLUTION LADDER, CONTINUED — path and
  torus held 6 zones at their minimal cells (exp101); push to
  k in {8, 10, 12} on path and torus (the two cheapest members)
  plus grid2d at (64, 0): where does zone-resolution actually BIND
  on the cheap substrates? Deposit the k* per substrate (the first
  non-verifying zone count at the minimal cell, or none through
  12), the err-vs-k trend, and the oracle's k-scaling (the ratio
  rises with k — does the price rise with it?).

## L85 — exp103 THE RESOLUTION LADDER, CONTINUED (3/4 — NO substrate binds through TWELVE zones: path k=12 at 3.24 mV on its DEFAULT cell, torus 2.61, the star-point grid 0.58 at every count; the oracle's k-scaling claim refuted by a schedule-rounding artifact and owned as overreach; the design lesson: resolution ladders need a fixed-coverage schedule)

- THE LADDER (k in {8, 10, 12}, width schedule 0.100/0.090/0.075
  keeping zones non-overlapping across f 0.02..0.95, one substrate
  per exp100 price class at its minimal cell):
  path (1, 0.015): 4.57 / 2.74 / 3.24 — ALL VERIFY. The chain
  resolves TWELVE zones on its DEFAULT cell; no dial needed.
  torus (4, 0): 3.22 / 2.40 / 2.61 — ALL VERIFY.
  grid2d (64, 0): 0.59 / 0.58 / 0.58 — the mu-cut grid is
  essentially PERFECT at every resolution (the exp101 k=4..6
  refusal at (64, 0.015) was entirely the theta sag; with mu cut
  the grid does not care how many zones it holds).
- RS-G3 REFUTED AND OWNED (the oracle's k-scaling): the ratio is
  NOT monotone in k — path [0.162, 0.141, 0.172], torus [0.630,
  0.610, 0.620], grid2d [0.589, 0.567, 0.578], every substrate
  DIPS at k=10. The artifact: the k=10 width schedule leaves
  ~0.3-cell inter-zone gaps, which int(round()) collapses —
  adjacent zones share boundary edges and the crossing count
  drops below the k=8 gap-separated layout. The deeper ownership:
  the ratio was validated ACROSS substrates at a fixed spec
  (exp102); extending it WITHIN a k-ladder was overreach, and the
  err does not track the ratio within-substrate anyway (path
  4.57 -> 2.74 -> 3.24 — the k x width coverage confound strikes:
  k=8 carries w=0.100 coverage 0.80, k=10 only 0.90 in 10 zones...
  the coverage AND the boundary geometry move together). DESIGN
  LESSON for the ledger: a resolution claim needs a fixed-coverage
  schedule (fix the total zoned fraction, vary only the count);
  the ratio's domain is fixed-spec cross-substrate pricing.
- RS-G1/RS-G2 PASS (path and grid2d hold the finest zoning);
  RS-G4 PASS (the k=12 below-line variant, zone z5 at -59: 0/2 —
  the M33 rule holds where zones nearly touch).
- THE RESOLUTION STORY, deposited: the reader's zone capacity at
  n=100 is >= 12 zones on every class representative — resolution
  is bounded by CELL COUNT (zone width vs identity noise), not by
  zone count per se, and the dial plane buys out the one substrate
  that needed it. exp94's 3-zone program was never near a limit.
- REGISTERED (exp104): THE SIZE AXIS — the price's n-scaling.
  path/grid2d/torus at n in {100, 200, 400, 800} (grids and tori
  aspect-matched 2:1), k=3 MULTI, each at its minimal exp100 cell
  (grid2d at (64, 0)). exp94's n-scale (2 substrates at (64, 0))
  becomes a map: does DEFAULT survive at n=400/800 on path (its
  n=200 err 2.38 was BETTER than n=100's 2.91 — the sag dilutes?),
  and does the oracle's ratio hold its class calls across n?

## L86 — exp104 THE SIZE AXIS (3/4 — the DEFAULT price DECAYS with size exactly as the mean-field picture predicts: path 2.91 -> 2.38 -> 1.97 -> 1.66 from n=100 to 784; the grid's V price is size-flat; the torus's two-dial price RISES; the ratio is class-stable but not size-invariant — BFS-order zones drift quasi-geometrically, owned)

- THE MAP (k=3 MULTI verbatim, mapped exp100 cells, 3 seeds):
  path (1, 0.015): 2.91 / 2.38 / 1.97 / 1.66 — ALL VERIFY, err
  MONOTONE DOWN. The DEFAULT class does not just survive size, it
  improves: the theta sag is a mean-field drag and bigger discs
  dilute it (the per-zone mean averages ~1/sqrt(n) more noise
  too). n=784 chain: the reader's cheapest run on the books.
  grid2d (64, 0.015): 5.00 / 4.71 / 4.60 / 4.73 — verifies at
  every size, err SIZE-FLAT: the grid's residual is its own local
  pinning need, not a dilutable drag.
  torus (4, 0): 3.82 / 4.08 / 4.40 / 4.86 — verifies at every
  size but the price RISES. A real structural trend (well above
  the noise floor), mechanism UNREGISTERED: candidate is the
  commitment-noise compounding along the BFS walk order (the
  exp32 sqrt(d) law) acting on the (4, 0) cell's weak gamma-4
  pinning — registered, not claimed.
- SZ-G4 REFUTED AND OWNED (the oracle's size transfer): the
  boundary-to-volume ratio is NOT n-invariant at the registered
  0.02 bar (path std 0.0203, grid2d 0.078, torus 0.087). The
  cause: the identity partition rides labeling_bfs ORDER, and BFS
  order is only quasi-geometric under lattice refinement — the
  zone-boundary placement shifts, crossings drift. THE HONEST
  VERDICT: the class calls TRANSFER (every family's ratios stay
  inside its exp102 class band), but oracle v1 is calibrated at
  n=100 and its ratio is class-level, not ratio-level, across
  size. The 0.02 bar assumed a cleaner invariant than BFS-order
  zones provide — the bar was miscalibrated, the transfer holds
  at the class level it was built for.
- ARC CONSEQUENCE: the reader's dial budget is now mapped over
  THREE axes — substrate (19 substrates, exp100), zone count
  (through 12, exp101/exp103), and size (to n=784, exp104) — with
  no refusal anywhere and the prices' shapes deposited (decay on
  the DEFAULT path, flat under pinning, rising on the two-dial
  torus). The compiler's operating manual now says: read the
  ratio, pick the cell, pay the tag.
- REGISTERED (exp105): THE TORUS'S RISING PRICE — the mechanism
  probe. The two live candidates: (a) BFS-walk commitment-noise
  compounding (the exp32 sqrt(d) law acting through the walk's
  inheritance fallback on longer orders) — test by re-running the
  torus n-ladder with the commitment noise OFF (the spec-read
  branch dominates on the torus; the probe: does the n-trend
  flatten when the walk's noise scale drops?); (b) the (4, 0)
  cell's gamma-4 window pinning losing ground on longer windows —
  test by the (16, 0) cell's n-trend (stronger pinning should
  flatten the rise). Whichever flattens the trend names the
  mechanism; deposit both ladders.

## L86 CORRECTIONS (owned, before exp105's entry is read)

- THE SZ-G4 MECHANISM WAS MISATTRIBUTED: the ratio's size decay
  (path 0.061 -> 0.008, grid2d 0.311 -> 0.107, torus 0.340 ->
  0.114) is NOT BFS-order drift — substrate_partition_check maps
  the zones onto RAW CELL INDICES (identity[i0:i1], row-major on
  grids), and the decay is the boundary-to-volume SCALING LAW
  itself: the crossing count is O(1) on the chain and
  O(perimeter) ~ O(sqrt(n)) on grids while total edges are O(n).
  The ratio behaves like a real physical boundary term — and that
  is exactly why it cannot be size-invariant.
- THE CLASS-TRANSFER CLAIM WAS OVERGENEROUS: at n=784 grid2d's
  ratio (0.107) lands in the oracle's DEFAULT band while its
  measured price stays V (4.73 at (64, 0.015)) — the measured
  price did NOT decay with the ratio. Oracle v1 is an n=100
  instrument; a size-free oracle needs a normalized boundary term
  (boundary length / sqrt(volume)) — registered as exp106's second
  deliverable.

## L87 — exp105 THE TORUS'S RISING PRICE (2/3 — both registered mechanisms REJECTED as the full story: commitment noise is INERT (delta +1.05 = base exactly) and stronger pinning only HALVES the rise (+0.58 at gamma 16, level -2.7 mV); the surviving candidate is WALK-DURATION DRIFT — the rebuild's sim-time scales with n; exp106 registered with the steps-per-cell probe)

- THE PROBES (torus r in {10, 14, 20, 28}, 3 seeds, the base arm
  exp104's deposit): noise02_4_0 = 3.81/4.08/4.40/4.86 —
  INDISTINGUISHABLE from base (delta +1.05): the walk's 0.6 mV
  commitment noise contributes nothing on the torus (the spec read
  dominates every rebuilt cell; the exp32 compounding law has no
  purchase here). pin_16_0: level collapses (3.82 -> ~1.16) but
  the trend SURVIVES at half strength (delta +0.58) — window
  pinning buys level, not trend. combo = pin alone (+0.64): the
  rise is noise-independent. TP-G1 REFUTED as registered (no
  flattener); TP-G2 PASS (every arm verifies at every size);
  TP-G3 PASS (noise sanity: 3.81 vs 3.82).
- THE SURVIVING CANDIDATE (named, not claimed): WALK-DURATION
  DRIFT. The rebuild runs steps_per_cell=8 pre-steps per committed
  cell at the substrate's dt — the walk's sim-time is ~8 x dt x
  0.74n, which scales LINEARLY with n (47 time units at n=100,
  464 at n=784 on the torus). Already-rebuilt cells DRIFT
  deterministically (V-coupling to not-yet-rebuilt wound neighbors
  and back) for that duration — a per-cell exposure that grows
  with n. It explains why the rise ACCELERATES with n in every arm
  (+0.26/+0.32/+0.46 in the base) and why pinning only halves it
  (stronger gamma pins harder against the same exposure).
- REGISTERED (exp106): (a) THE STEPS-PER-CELL PROBE — a
  backward-compatible steps_per_cell kwarg (default 8, bit-exact);
  if the n-trend flattens at steps_per_cell=2, walk-duration drift
  is the mechanism (the probe predicts err(n) becomes
  walk-time-invariant); (b) THE ORACLE'S SIZE NORMALIZATION — a
  boundary-length/sqrt(volume) ratio term that cancels the
  perimeter/volume scaling, re-audited against the exp104 sizes
  (the v2 oracle must price grid2d's n=784 cell INTO the V band —
  the v1 transfer failure).

## L88 — exp106 WALK-DURATION DRIFT KILLED + THE ORACLE'S V2 LANDING (4/5 — the steps probe is a clean NULL: spc=2 reproduces the base errors EXACTLY (3.82/4.86, delta +1.04 unchanged, level effect 0.00), so the rebuild's mid-walk exposure contributes nothing and the torus's rising price stays OPEN with the candidate list shrunk; the v2 oracle (crossing/sqrt(edges)) lands 3/3 — Spearman 0.81 across the battery, size-stable on 2D, the v1 n=784 failure repaired)

- PART A (WJ-G1 REFUTED, WJ-G2 PASS): steps_per_cell 8 -> 2
  quarters the walk's sim-time and moves NOTHING (3.82/4.86 both
  settings; the level effect 0.00 mV). The drift mechanism is
  dead — deterministic mid-walk exposure does not touch the
  committed identity at (4, 0) (mu=0 cuts theta diffusion; gamma-4
  pins V fast). The torus's +1.04 mV size trend survives with the
  candidate list now: commitment noise (killed, exp105), walk
  exposure (killed, exp106), window pinning (halves it, exp105).
  The residual trend is REAL, small (4.86 at n=784, well inside
  the bar), and honestly OPEN — registered for exp107 with the
  remaining suspect: the zone-band GEOMETRY under index
  refinement (f-boundaries round onto lattice rows; the
  spec/canon bands' relative shapes change with r).
- PART B (3/3 — THE V2 ORACLE): v2 = crossing_edges / sqrt(edges)
  cancels the perimeter/volume scaling. WJ-G3 PASS: size-stable on
  the 2D families (grid2d 4.17/4.19/3.99/4.14, rel std 0.019;
  torus 4.81/4.85/4.38/4.50, rel std 0.043); path decays 0.60 ->
  0.21 — the documented 1D boundary law, excluded by design. WJ-G4
  PASS: v2's cross-substrate Spearman vs the dial class is 0.81 —
  BETTER than v1's 0.73 (the sqrt(edges) factor corrects the
  dense-substrate distortion v1 carried). WJ-G5 PASS: grid2d's
  n=784 v2 (4.14) lands inside the n=100 V-band (2.04, 6.23) —
  the v1 transfer failure is repaired.
- THE ORACLE ARC, CLOSED: v0 the chain-era boolean (refused 16/19
  of its executor's verifications); v1 the raw ratio as price
  (Spearman 0.73 at n=100, size-fragile); v2 the normalized
  boundary term (Spearman 0.81, size-stable on 2D, the 1D decay
  documented as physics). The compile decision's final form: the
  v2 boundary term NAMES THE PRICE, the dials pay it, and nothing
  on the battery has refused.

## L89 — exp107 THE GEOMETRY PROBE (the exoneration: the torus's rising price is INVARIANT under zone-f-offset — the offset arm reproduces the base trend to 0.01-0.11 mV per size (delta +0.68 vs +0.67); boundary placement on the lattice is dead as the mechanism; the candidate ledger for the +0.7-1.0 mV size trend is now: commitment noise DEAD (exp105), walk exposure DEAD (exp106), zone-band geometry DEAD (exp107), window pinning HALVES it (exp105, gamma 16: level -2.7 mV, delta +0.58) — the residual lives in the window/settle MEAN-FIELD itself and is registered open for exp108 with that framing. The trend's magnitude: 4.40 mV at n=784, inside the 6.0 bar, verified 3/3 at every size and offset — a precision question, not a viability question. Probe deposited as results/exp107_geometry_probe.json; analytic follow-ups (the mean-field decomposition of the window drift) carry the exp108 registration.)

## L90 — exp108 THE MEAN-FIELD DECOMPOSITION (4/4 decision gates PASS + the carrier NAMED: the torus's (4,0) size trend is a settle TRANSIENT riding on a commit-time seed — the in-run base REPRODUCES exp104 exactly (3.82 -> 4.86, delta +1.04, MD-G0, the committed harness re-grounded after owning that exp107's script was never committed — a discipline gap); the phase decomposition localizes the rise POST-WALK (3.36 -> 4.76, delta +1.40 — the settle COMPRESSES the trend to +1.04, it does not create it; MD-G1); eps_freeze (theta frozen from walk end) equals the post-walk error at EVERY size (3.36/3.77/4.22/4.76 — the frozen-theta V-equilibrium carries the FULL +1.40 trend: the seed is the committed pattern's smoothed-field geometry, not settle theta sag); long_settle FLATTENS the trend to +0.10 at 60 h with the level converging size-flat to ~5.0 mV (MD-G2 — the 15 h snapshot is a differential phase of the eps-mediated collective sag, tau ~25 h, whose spectral timescale spreads with n on the torus); window48 deepens levels +0.26 and post-walk +0.28 (the window seeds more, consistent); all classes verify 3/3 at every size and every arm's n=100 level within 1.5 mV of base (MD-G3/G4); the class decomposition (seed 1): zone_rms 2.78 -> 3.71, gap_rms 3.64 -> 4.69, intact_rms 5.20 -> 6.35 — ALL rise with n even though the intact field STARTS better at large n (survivor post-window 2.79 -> 1.71 DECAYS — the window output is exonerated as the seed; the committed span's frozen-field equilibrium is where the trend lives). THE INTERPRETATION: two effects, (1) the frozen-geometry term +1.40 (V* = gamma(gamma I + L_G)^-1 theta on the committed pattern rises with n) and (2) the eps-sag transient toward a size-flat ~5.0 mV asymptote that COMPRESSES it to +1.04 at the 15 h read and erases it by 60 h — the registered "window/settle mean-field" framing CONFIRMED and RESOLVED into a statics question. exp109 REGISTERED: the STATIC FIELD MAP — solve V* = gamma(gamma I + L_G)^-1 theta directly (no dynamics) on the actual committed patterns at all four sizes, zero commit noise and 0.6 noise arms, then Laplacian-eigen-decompose the error field (torus modes are analytic): if the error concentrates at low-k (wavelength ~ r) the intact reservoir's boundary condition bleeds globally (mean-field, the canon diamond's wrap scatter named); if at high-k (zone-boundary scale) it is local kernel smearing of the -30/-50/-20 discontinuities — either way the n-scaling of the frozen geometry gets its mechanism, and the reader's 15 h price map gains its transient calibration. Deposited as results/exp108_mean_field_decomposition.json (48 runs, traces + class decomposition per size).

## L91 — exp109 THE STATIC FIELD MAP (1/3 decision gates PASS + the instrument EXACT and two refutations as the payload: SF-G1 the static solve V* = gamma(gamma I + L_G)^-1 theta REPRODUCES the dynamic post-walk error within 0.02 mV at every size and seed — the walk's 8-steps-per-cell field IS the frozen-theta fixed point, the settle question is now pure linear algebra; SF-G2 the eigen-decomposition on the torus's exact DFT modes NAMES the split: the HIGH-k power (zone-boundary kernel smearing) is n-INVARIANT in absolute terms (~2.3 mV^2 at every size — a constant tax, 0.61 -> 0.45 SHARE as the total grows) while the LOW-k power GROWS ~8x (1.22 -> 9.55 mV^2, share 0.11 -> 0.42) — the torus's rising price is a GLOBAL FIELD STRUCTURE, not boundary geometry; SF-G3 REFUTED with a level penalty — the canon-flat arm (diamond scatter killed) makes it WORSE (7.11-8.16 mV, low-k share 0.51-0.87): the BFS diamond's -20 pockets CUSHION the -30/-50 transitions, heterogeneity is protective, the scatter is not the carrier; SF-G4 REFUTED upward-and-informatively — the clean pattern's static error DECAYS with n (1.46 -> 0.81, delta -0.65): fixed-fraction geometry gets CHEAPER under the kernel, so the entire rising excess is the difference between the REAL committed field and the clean one (1.90 -> 2.55 -> 3.30 -> 3.95, rising ~linearly with n) — and the real pattern differs from ideal only in the window/walk EVOLVED state of its cells (commits are exact to target/canon +/- 0.6; the intact field starts BETTER at large n). The candidate list for the seed narrows to the walk's network evolution (0.8n time units of wound-field (-30) exposure saturating the intact reservoir's theta sag at large n — reconcilable with exp106's spc-invariance only if the sag saturates by the spc=2 duration) or a committed-cell low-k component the 15 h settle was too blunt to see. exp110 REGISTERED: the FROZEN-WALK PROBE + class-split spectra — the static instrument with the walk's inter-commit steps REMOVED (spc=0: intact field = window output exactly) against the real spc=8 capture, plus fft2 band spectra of (theta_end - target) split BY CELL CLASS (committed vs intact): if frozen-walk collapses the trend to the idealized decay, the walk's wound-field exposure is NAMED as the seed carrier and the reader's price map gains its first true statics calibration; if it survives, the class-split spectra point at the committed cells and the commit path gets re-examined. Deposited as results/exp109_static_field_map.json.)

## L92 — exp110-111 THE WALK-DURATION MECHANISM + THE PROTOCOL CALIBRATION (exp110 2/2 THEN exp111 4/4 — the exp104-110 arc CLOSES with the mechanism named and the price re-calibrated: exp110's frozen-walk probe (spc=0: the inter-commit steps removed, the intact field stays at its window output) collapses the static trend to the idealized DECAY (delta -0.76 vs idealized -0.65) and drops the level 62% (4.03 -> 1.52 mean) — FW-G1 the walk's wound-field exposure IS the seed carrier; the DIRECT evidence deposited: the intact reservoir's walk drift GROWS monotonically with n (2.47 -> 3.48 -> 4.66 -> 5.32 RMS — the 0.8n-time-unit rebuild bathes the intact field in the wound state longer at larger n) and the COMMITTED cells' low-k difference-power grows 16.6x under the real walk vs 1.33x frozen (the early-committed cells re-sag toward the wound field while their neighbors commit — the commit is a RACE between identity writing and wound-field erasure, and the race gets longer with n); exp106's spc-invariance reconciled: its 15 h settle absorbed the walk-phase difference — the settled read was too blunt to see what the static instrument sees; exp111 calibrates the price map's protocol dependence: the FROZEN-WALK operating point (spc=0 + the canonical 15 h settle) INVERTS the torus trend (+1.04 deployed -> -1.03 frozen: 2.51 -> 1.48, the decay clean-geometry always promised) and makes the torus the reader's CHEAP substrate — n=784 at 1.48 mV vs 4.86 deployed, 3.3x cheaper at rate 1.0 — while grid2d (64, 0) is protocol-ROBUST to +/-0.02 mV (0.49-0.51 under all four protocols), zero refusals anywhere (PC-G3), frozen never costs more at any size (PC-G4); THE CLOSING STATEMENT for the arc that opened at exp104: the torus's rising (4, 0) price was a WALK-DURATION TRANSIENT — the deployed protocol's 0.8n rebuild window lets the wound field erase identity faster than the walk writes it on large substrates; the frozen walk writes identity instantaneously and the geometry's true price (decaying, sub-2 mV) appears; walk_speed REGISTERS AS A NEW DIAL in the compiler's price map, and the bench prediction deposits itself: REBUILD SPEED PREDICTS IDENTITY FIDELITY (faster regeneration preserves pattern memory better — testable against the published regeneration-timing literature and addable as a bench gate at the next Stage-5 protocol revision, NOT retroactively into the pre-registered document); exp112 REGISTERED: the walk_speed ladder on the price map's EXPENSIVE members (the two-dial and V-priced cells at their adopted cells and one dial cheaper, spc in {8, 2, 0}) — how much of the dial budget does walk speed buy back; deposited as results/exp110_frozen_walk_probe.json and results/exp111_protocol_calibration.json)

## L93 — exp112 THE WALK-SPEED LADDER (3/3 gates PASS, 13/15 BUY-BACKS — the dial budget RELEASES and the price map splits into two kinds: WS-G2 the spc=8 references REPRODUCE the exp100 deposit to 0.01-0.02 mV (the harness is the map's harness, bit-exact); WS-G3 no member loses verification at its adopted cell under spc=0 (speed is free); WS-G1 thirteen of fifteen expensive members VERIFY at a strictly cheaper cell under the frozen walk — star (2, .015) -> (1, .015); tree/grid2d/grid_elong (64) -> (16); ladder/random6 (32) -> (8); barbell (16, 0) -> (4, 0); and the ENTIRE (4, 0) two-dial class — torus, torus_elong, random3, random8, scale_free, scale_free200 — verifies at DEFAULT gamma (1, 0), errs 5.16-5.94 inside the bar (thin but 3/3 seeds each): their two-dial tags were WALK TAX, not coupling geometry; THE TWO REFUSALS are the structure: bipartite and complete REFUSE the entire descent ((8, 0) at 8.54/9.23, (16, 0) at 6.57/7.34, rate 0.00) — the no-within-class-edges and clique extremes hold their (32, 0) price at spc=0: their cost is COUPLING GEOMETRY, exactly the v2 oracle's top tail ("the dense extremes are the ratio's top tail", exp100) — the boundary-to-volume ratio was measuring geometry price all along and the walk tax was MASKING it in the middle band; the map's honest new form: 4 DEFAULT + a walk-tax band (13 members repriced one-to-fourfold cheaper under spc=0) + a geometry-priced pair (bipartite, complete — untouchable by any dial including speed); exp113 REGISTERED: THE RE-PRICED MAP — the full 19-member battery re-minimal-celled at spc=0 (DEFAULT members included), the class re-assignment deposited, and the v2 oracle RE-TESTED on the walk-tax-free errs (Spearman: does crossing/sqrt(edges) predict the GEOMETRY price better once the walk tax is stripped? does its top tail remain exactly {bipartite, complete}?); deposited as results/exp112_walk_speed_ladder.json)

## L94 — exp113 THE RE-PRICED MAP, FIRST ASSEMBLY (2/3 gates PASS + TWO OWNS: RP-G1 the reader's domain stays CLOSED under the frozen walk — 19/19 verify somewhere at spc=0, and the walk tax proves UNIVERSAL: even the four DEFAULT members got cheaper (path 2.91 -> 2.04, path200 2.38 -> 1.48, cycle 3.67 -> 2.66, small_world 4.23 -> 3.02 at the same (1, 0.015) cell — no substrate's spc=8 err was geometry alone); OWN 1 (instrument mismatch): the pre-registered rho test compared the v2 ratio against the 15 expensive members' CONTINUOUS cell-errs — rho8 -0.354, rho0 0.064 — but the exp102/106 oracle's claim was CLASS-LEVEL pricing (Spearman 0.73/0.81 against the dial-CLASS ordinal across the 19 battery, not within-expensive-set cell errors), so the registered RP-G2 passed vacuously and the comparison as run does not bear on the oracle's actual claim; OWN 2 (formulation error): RP-G3's err-based top-tail test picked scale_free/scale_free200/star (errs 5.71-5.94 at DEFAULT-gamma cells, marginal verifies) over bipartite/complete (4.47/5.21 at (32, 0)) — but the map's price semantic is the CELL ORDINAL (which rung of the dial ladder a substrate needs), not the err at that cell: scale_free at (1, 0) is CHEAPER than bipartite at (32, 0) no matter the err — the top-tail claim must be tested against the ordinal dial cost, which is exp114; the re-priced class table deposited: DEFAULT0 (verifies at (1, 0.015)): path, path200, cycle, small_world, star; MU-DIAL-ONLY (1, 0): torus, torus_elong, random3, random8, scale_free, scale_free200 (the entire former two-dial middle band); GAMMA-PRICED: tree/grid2d/grid_elong at (16, 0.015), ladder/random6 at (8, 0.015), barbell at (4, 0); GEOMETRY-PRICED: bipartite, complete at (32, 0) untouchable; exp114 REGISTERED: the CORRECTED oracle replica — assembly-only from deposited data: Spearman(v2, ordinal dial cost) over the re-priced map with a lexicographic (gamma-ladder, mu-ladder) cost and the class-mean monotonicity check (does the ratio's class-level pricing survive the walk tax it never knew about?), plus the honest comparison against exp102's 0.73/0.81 under the SAME class-ordinal instrument; deposited as results/exp113_repriced_map.json)

## L95 — exp114 THE CORRECTED ORACLE REPLICA (2/3 gates PASS — the oracle's honest final form on the walk-tax-free map: OR-G1 Spearman(v2, class-ordinal cost) over the 19 re-priced members = 0.63 — SURVIVES the corrected re-test weakened (references 0.73 raw / 0.81 v2 were measured on walk-taxed cells; the bar was pre-registered at 0.60 for exactly that reason); OR-G3 the geometry pair DOMINATES without exception — every member with v2 below the pair's minimum sits at a strictly cheaper cell (max violation set empty; tree/grid2d/grid_elong at cost 40 are the closest approach); OR-G2 REFUTED and the refutation is the finding: class-mean v2 is NOT monotone across the re-priced classes — MU0 7.117 > GAMMA0 5.550, the middle is DISORDERED (random3 ratio 7.51 yet prices at (1, 0); dense random6 ratio 2.04 yet needs (8, 0.015); scale_free200 13.15 at (1, 0)) — the exp102 class pricing (DEFAULT 0.07 < V 0.358 < TWO 0.501) was measured on walk-taxed cells and its clean ordering does not survive the tax's removal; the channel-weighting caveat owned (lexicographic gamma-then-mu cost is a choice — but the disorder is visible in the raw pairs, not an artifact of the weighting); THE ORACLE'S FINAL FORM: the boundary-to-volume ratio prices the ENDS — the cheap band (DEFAULT0, v2 0.43-1.30) and the geometry pair (25.0-32.5) — and does NOT price the middle band, whose members' cells are set by the mu channel and walk speed instead; R5's slogan survives corrected: the ratio names the ends, the dials pay the middle, walk speed was hidden tax everywhere except the pair; exp115 REGISTERED: WHAT PRICES THE MIDDLE — (a) the mu ladder on the six MU0 members at spc=0 (does mu 0.01 suffice, or is the full mu cut load-bearing? is the mu requirement itself walk-speed-dependent — re-run the ladder at spc=8 for the contrast), (b) candidate middle-band predictors assembled and Spearman-tested against the middle costs: mean degree, spectral gap lambda_2, and the v2 ratio restricted to the middle — does ANY deposited quantity price the middle, or is the middle genuinely multi-channel?; deposited as results/exp114_corrected_oracle.json)

## L96 — exp115 WHAT PRICES THE MIDDLE (0/3 gates PASS — all three refutations are the payload, and the corrected picture deposits itself: MB-G1 REFUTED 0/6 — the mu 0.01 rung buys NOTHING anywhere (errs 6.87-9.64 at spc=0 where the full cut verifies 5.16-5.94): the middle's mu price is BINARY-DEEP, theta diffusion must be FULLY off or identity does not hold through the rebuild; MB-G2 REFUTED as formulated (the tested rung was the wrong one) with the real speed-dependence sitting one rung deeper in the NEW (1, 0) @ spc=8 column: (1, 0) verifies 6/6 at spc=0 and REFUSES 6/6 at spc=8 (6.76-7.41) — WALK SPEED BUYS GAMMA, NEVER MU: at spc=8 the middle needs (4, 0), at spc=0 it needs (1, 0), and mu 0 is mandatory at both speeds; MB-G3 REFUTED — no deposited scalar prices the middle (lambda_2 -0.655, mean degree -0.431, v2 -0.305: all weak-negative; the middle is genuinely multi-channel, honestly deposited); THE CLOSING PICTURE of the exp108-115 arc: the reader's price map = the cheap band (default cell, v2 prices it), the middle band (mandatory mu 0 + a gamma component that walk speed buys back 4x, unpriced by any single scalar), and the geometry pair (bipartite/complete, untouchable by any dial including speed, v2's clean top tail); the mu channel's ROLE hypothesis: theta diffusion is the contamination channel through which the intact/wound field's identity bleeds into the rebuilt span — protecting identity requires freezing it; WHICH PHASE the mu cut protects (the walk's exposure window vs the 15 h settle) is exp116's question; exp116 REGISTERED: THE MU-PHASE LOCALIZATION — a 2x2 phase split ({mu on/off during the walk} x {mu on/off during the settle}) at (1, 0.015-default-mu-arms) on the six MU0 members, 3 seeds: if the walk is the mu-sensitive phase, mu-on-walk/mu-off-settle refuses while mu-off-walk/mu-on-settle verifies; if the settle is sensitive, the reverse; deposited as results/exp115_middle_pricer.json)

## L97 — exp116 THE MU-PHASE LOCALIZATION (2/3 gates PASS — and the REFUTED gate is the deepest finding of the arc: MP-G1 there is NO clean phase attribution because BOTH phases kill identity — window-mu-only (w1s0) refuses 6/6 (errs 6.09-6.93) AND settle-mu-only (w0s1) refuses 6/6 (errs 6.94-7.91): theta diffusion at 0.015 destroys middle-band identity whether it acts for 24 h before the amputation or 15 h after the commit; MP-G2 the corners anchor the 2x2 (oo verifies 6/6 at 5.16-5.94, w1s1 refuses 6/6 at 7.17-8.52); MP-G3 no runaway; THE MIDDLE BAND'S TRUE PRICE, final form: TOTAL MU SILENCE — the mu dial is binary not just in magnitude but in PHASE COMBINATION (any mu-on window anywhere in the protocol fails the middle band), which upgrades the contamination picture from "the walk bathes the span" to "theta diffusion at operational strength homogenizes the pattern memory on hours timescales, and the rebuilt identity survives only in a diffusion-silent protocol"; the cheap band and the geometry pair tolerate mu (they verify at default mu 0.015 or their priced cells) — the mu-sensitivity is a MIDDLE-BAND property, consistent with exp116's predecessors; exp117 REGISTERED: THE PRICE MAP V2 RE-ISSUE — the map's honest current form assembled and deposited as a versioned artifact: per member the minimal cell under BOTH protocols (deployed spc=8 / frozen spc=0), the mu-silence requirement column (mandatory / tolerant), the class re-assignment (DEFAULT0 / MU0-mandatory-silence / GAMMA0 / GEOMETRY), the v2 oracle column with its domain statement (prices the ends), and the walk-speed calibration curve (the spc ladder's buy-back table) — the compiler-facing document the arc was building toward; deposited as results/exp116_mu_phase_localization.json)

## L98 — exp117 THE PRICE MAP V2 RE-ISSUE (3/3 gates PASS — the compiler-facing artifact deposited: docs/PRICE_MAP_V2.md + results/price_map_v2.json, 19 members x {deployed cell/err, frozen cell/err, speed buyback, mu requirement, v2 ratio, class v1/v2}; PM-G1 no holes (every member verified under BOTH protocols); PM-G2 class-cell consistency; PM-G3 the artifact renders; the honest TRADE owned in the table: the MU0 members' frozen cells are CHEAPER ((1, 0) vs (4, 0)) but sit nearer the bar (5.16-5.94 vs 3.59-3.96 deployed) — the map records both columns and the caller chooses the operating point: minimal-dial (frozen) or minimal-err (deployed); star's row is the buyback nuance (2x at (1, 0.015) with err 5.71 vs deployed 5.42 — cheaper cell, comparable err); the arc exp108-117 is CLOSED: nine experiments, the torus trend mechanized (walk-duration transient), the walk-speed dial priced (13/15 buy-backs, gamma never mu), the mu-silence law stated (binary in magnitude and phase), the oracle's domain stated (prices the ends), and the map re-issued in the form the compiler can consume; exp118 REGISTERED (deriving from subagent A's deposit research/papers/2026_mining.md, top prediction TAS-P1): THE MEMORY CO-METRIC SPECTRUM TEST — Blattner 2026's TAS framework claims morphological memory acts through a rank-one/anisotropic kernel (K_mem = R Q^-1 R^T, top-eigenvalue energy fraction >= 0.8 with silent orthogonal directions); the stack's exp84 quadrature machinery and the graph substrates can compute the analog DIRECTLY: the theta-field's memory kernel per substrate, its eigen-spectrum, the top-eigenvalue energy fraction, and the silent-direction test (perturb along the sub-leading eigenvectors at matched cost — does identity hold? TAS says yes, the isotropic picture says the perturbation should matter); gates pre-registered when the script is written; deposited as results/price_map_v2.json and docs/PRICE_MAP_V2.md)

## L99 — exp118 THE FULL CORPUS MINE (7/7 readable gates PASS — the HANDOFF's open item closes: the CURRENT adopted stack run over ALL 1,716 PlanformDB records, not a slice; accounting exact (905 scored / 404 unmapped_plane / 153 unmapped_group / 254 no_outcome = 1,716); THE HEADLINE: decoded MAE 0.290 mV (n=884) INDEPENDENTLY RE-DERIVES the L74 slice reference (0.290) on the full corpus — the slice result was not a slice artifact, the corpus residual stays closed at scale; decode accuracy 0.693 (confusion: 389/238 correct, 179 recorded-abnormal-predicted-wt — the cutting-row hot bias documented: plain-cut rows record 42% abnormal while the sim restores WT 100%, the DB's cutting rows carrying technique/health failures the plain-cut executor does not model — honest, gated, deposited per-intervention); the per-intervention table: cutting n=293 (mae_dec 0.325), gj_block n=21 (0.525), innexin n=6, ion_channel n=70 (0.460), morphogen n=126 (0.456), other_rnai n=389 (0.165 — the best-understood class), 47 unique arms x 3 seeds in 2.6 s; mapping-scope honesty: 905/1,462 outcome rows = 0.619 covered under the adopted mapping (vs exp37's looser 0.70-era number — both deposited); OWNED: exp91/exp92's result JSONs were missing from results/ (rollback-incident residue) — this run re-deposits the L74 reference as a checkable artifact and G5 independently re-derives it; script by subagent 2-d (pilot 5/5 first: stride-10 systematic sample, extraction parity vs the ledger pins exact); the full-corpus number is now the validation corpus's standing total; exp119 REGISTERED (the ledger's former exp118 slot moves here): THE MEMORY CO-METRIC SPECTRUM TEST — subagent 2-a's top-ranked 2026 prediction (TAS-P1, Blattner 2026): morphological memory acts through a rank-one/anisotropic kernel — computable against the stack's graph substrates with exp84's quadrature machinery: per substrate the theta-memory kernel's eigen-spectrum, the top-eigenvalue energy fraction (TAS claims >= 0.8 with silent orthogonal directions), and the silent-direction perturbation test (sub-leading eigenvector perturbations at matched cost should NOT degrade identity if TAS is right; the isotropic picture predicts they should); deposited as results/exp118_corpus_full.json with the pilot results/exp118_corpus_full_pilot.json)

## L100 — exp119 THE MEMORY CO-METRIC SPECTRUM TEST (1/3 gates PASS — TAS-P1's accessible core tested on the stack's own machinery and REFUTED in both directions, with the instrument validated: MS-G1 the identity-sensitivity spectrum (per Laplacian mode, the identity error a 2 mV-RMS pattern write along that mode costs at the SF-G1-exact static read) is DIFFUSE — top-mode energy share 0.012-0.020 across grid2d/torus/path/star vs TAS's claimed >= 0.8 rank-one concentration: the stack's memory co-metric is spread over ~n modes, no privileged direction exists; MS-G2 the silent-directions claim REFUTED at ratio 1.4 (top 3.21 vs low 2.29 mV on grid2d): even the QUIETEST Laplacian mode costs ~1.2 mV of identity error at matched norm against the base 1.11 — there is no 0.1 mV silent subspace; MS-G3 the instrument is VALID — the static prediction matches the real 15 h dynamic settle within 0.27 mV for both perturbation directions, so the refutations are the physics, not the instrument; SCOPE NOTE OWNED: the TAS paper's exact K_mem = R Q^-1 R^T form was not retrievable (access-blocked; mined from README/abstract only) — this experiment tests the ACCESSIBLE CORE (spectral anisotropy of identity retention with silent directions), two-sided as pre-registered, and the deposit stands ready for re-testing against the true form if the paper becomes readable; a process lesson the arc keeps teaching: the stack's memory is a DIFFUSION property (isotropic across modes, concentrated only in magnitude — low-k writes cost less) — consistent with exp109's finding that clean geometry decays with n; exp120 REGISTERED (the next 2026-paper test from subagent 2-a's ranked list): THE WRITE-SUCCESS KERNEL SHAPE TEST — CG-P1/P2 against Damon's deposited record (Zenodo 18358611): the stack's write-success-vs-onset kernel should be shape-invariant across substrates (kappa within +/-20%) with onset shifting only under the M40 commitment dial, and no gamma <= 64 rescues late (post-closure) perturbations, against the record's tc ~ 20 h, kappa ~ 10 h, L ~ 0.75; deposited as results/exp119_memory_spectrum.json)

## L101 — exp120 THE WRITE-SUCCESS KERNEL SHAPE TEST (1/3 gates PASS — and the stack's temporal vulnerability map deposits itself: CG-G2 the STRENGTH-CANNOT-REOPEN claim CONFIRMED — the gamma-64 arm's P(break) curve is IDENTICAL to default on torus and grid2d at every onset (max |d| 0.00): no gamma <= 64 rescues the late blockade, the first-commitment semantics hold against strength; CG-G1 REFUTED in its pre-owned FAIL mode — the stack has NO smooth decreasing kernel to fit: grid2d and path are INVULNERABLE at every onset (P(break) = 0.0 flat — the walk commits exact values regardless of coupling), while the torus shows a SHARP RISING EDGE (0.0 through onset 36 -> 1.0 at 48/72, late walk): the vulnerable window's EXISTENCE and POSITION are substrate-specific, extending exp82's tissue-specific-frontier finding to the temporal axis; the record's smooth tc~20h/kappa~10h kernel does not exist here — the honest statement is a per-substrate step, not a shared logistic; CG-G3 formally REFUTED (only 1/3 substrates shifts) but the torus's edge MOVES EARLIER under doubled commitment diffusion (48 -> 36 h, a 12 h monotone-signed shift — the mu dial does move the closure edge where an edge exists); PROCESS OWNED: two instrumentation bugs caught and fixed before the deposit counts — the first pass used gap_scale (which scales ONLY the theta-diffusion term, not the V-coupling: the blockade must go through block_gap_junctions, scaling G and deg) and the gamma-64 arm ran with the gamma-1 dt (Euler-unstable, |1 - 64*0.1| > 1 — the spurious all-1.0 curves in the first pass were integration divergence, not physics); the logistic fits were polarity-inverted (a decreasing kernel fit to rising P(break) — the correct fit is 1 - P(break)) and their tc-at-bound artifacts are void; exp121 REGISTERED: (a) the torus's late-blockade break MECHANISM (what exactly exceeds the 6.0 bar at onset 48 — class decomposition at the read), (b) the corrected-kernel refit (1 - P(break)) with the per-substrate edge positions as the deposited temporal map, (c) the edge-shift ladder (mu in {0.015, 0.03, 0.06} on the torus — is the 48 -> 36 h shift monotone?); deposited as results/exp120_kernel_shape.json)

## L102 — exp121 THE CLOSURE EDGE (2/2 decision gates PASS + the class named, with one void column owned: CE-G2 the torus's closure edge is MONOTONE in the commitment-diffusion dial — first P(break) >= 0.5 onset 48 h at mu 0.015, 36 h at mu 0.03, 12 h at mu 0.06 (fitted tc 42.9 -> 30.8 -> 9.5 h, kappa -> 0.2-0.4: the honest step limit of the decreasing kernel) — the temporal vulnerability edge is DIALABLE, doubling mu moves closure ~1.5x earlier per step; CE-G3 the null substrates HOLD at fine onsets (grid2d/path P(break) = 0.0 at 42/54/66 h) — the substrate specificity is real, not a sweep-grid artifact; CE-G1 the break at the edge localizes in the INTACT FIELD (intact RMS 11.05 vs zone 3.34 / gap 3.00) — the mechanistic tie to exp110: the intact reservoir carries the walk-time wound-exposure drift (2.47 -> 5.32 with n, L92), normally re-smoothed by the settle's coupling; a blockade landing in the late walk freezes that drifted intact state in (V-coupling and theta diffusion both cut), and the intact field's error IS the break; VOID COLUMN OWNED: the control arm ran onset-beyond-protocol-end, which the rest-semantics turned into a ZERO-SETTLE read (9.23 mV, post-walk field) — not comparable to the settled blocked read (6.36); the proper settled control is exp111's default column (4.03 mean); exp122 REGISTERED: the SETTLE-RESCUE TEST — three arms on the torus at the edge onset (48 h): block-walk-only (coupling restored at the settle), block-settle-only (coupling cut only from the settle), and the settled unblocked control (the exp111 column re-derived in-batch) — if walk-only-blockade does NOT break while settle-only does not either but the sustained arm does, the edge is a DUAL-PHASE requirement (the walk-time exposure seeds the drift AND the settle needs coupling to re-smooth it), completing the exp108-121 mechanistic chain from the torus price through the walk tax to the temporal vulnerability map; deposited as results/exp121_closure_edge.json)

## L103 — exp122 THE SETTLE-RESCUE TEST (0/2 gates PASS — the strongest kind of null: it falsified the registered mechanism guess and named the right one — SR-G1/SR-G2 REFUTED because the CONTROL ITSELF FAILS: the unblocked torus at the DEFAULT cell (gamma 1, mu 0.015) reads 10.00 mV, P(break) 1.0 — this is exp100's default-cell refusal, never before settled-read in this configuration; the four arms then order MONOTONE in how early the blockade silences mu: block-from-0 verifies (exp120's early onsets, P(break)=0 — the blockade cuts gap_scale which scales the theta-diffusion term mu*gap_scale*lap_theta, silently enforcing the exp115-116 MU-SILENCE LAW), sustained-from-48 at 6.36 (marginal break), walk-only (block 48, restored at settle) 8.85, settle-only 8.82, never 10.00 — every hour of mu-active time before silencing adds irreversible identity damage; THE REINTERPRETATION (owned, superseding the L101-L102 'closure edge' reading): exp120-121's onset kernel is the MU-SILENCE DEADLINE, not a first-commitment edge — the record's GJ-blocker drugs (octanol/heptanol) ARE theta-diffusion cuts in the stack's mapping, so the record's decreasing success-vs-onset kernel and the stack's mu-silence deadline are the same object; the mu-dial edge shift (exp121: 48 -> 36 -> 12 h under mu doubling) is the deadline moving with the diffusion rate — exactly what a diffusion deadline must do; CG-G2's strength-cannot-reopen stands UNCHANGED (gamma acts on V-pinning, not the theta channel — the right mechanism for strength-invariance); the exp122 gates' failure was the WRONG mechanism prediction (settle-rescue), and the deposit's value is the corrected one; exp123 REGISTERED: THE CHANNEL SPLIT — at the default cell, three arms x 8 onsets x 8 seeds: full blockade (both channels cut), MU-ONLY (mu = 0 from onset, coupling intact), G-ONLY (V-coupling cut from onset, mu intact) — if mu-only rescues like the full blockade and G-only does not, the deadline is PURELY the theta-diffusion channel and the record's drug mapping is exact; deposited as results/exp122_settle_rescue.json)

## L104 — exp123 THE CHANNEL SPLIT (2/3 gates PASS — and the refuted gate is the mechanism: CS-G2 the V-COUPLING channel alone is INERT (g_only == control at every onset, P(break) = 1.0 — cutting G/deg with theta diffusion intact changes nothing); CS-G3 harness continuity (the full arm reproduces exp120's default curve exactly); CS-G1 REFUTED with the decisive finding: MU-ONLY DOES NOT RESCUE — c.mu = 0 from ANY onset including 0 leaves P(break) = 1.0, while the full blockade from 0 rescues through onset 36 — THE DEADLINE IS CONJUNCTIVE: both channels must be cut; the physical reading: at gamma 1 the pinning is WEAK (V* = (theta + 0.2*sum(V_nbr))/(1 + 0.8) — the neighbor average carries comparable weight), so with mu silenced but coupling intact the committed zones' V is still dragged toward the intact reservoir and eps drags theta after it; with V cut but mu live, theta diffusion contaminates per exp116; only the simultaneous cut holds the identity — the two-channel structure of the failure itself, echoing the two-channel law's quadrature (exp84); THE RECORD MAPPING COMPLETES: the GJ-blocker drugs cut BOTH channels in the stack's semantics, and the record's success window is the deadline by which the dual cut must land — the testable bench prediction deposits itself: partial-channel pharmacology (uncoupling without theta-effect, or vice versa) should FAIL where dual-action blockade succeeds within the window; exp124 REGISTERED: THE GAMMA-DEPENDENCE OF THE SPLIT — the same three arms at the torus's adopted (4, 0) cell: gamma 4 pins V hard enough that the prediction is mu-only NOW rescues (the (4,0) cell's mu-silence is sufficient with stronger pinning — the two dials are the two channels' knobs and the two-dial price structure IS the conjunctive requirement priced), while g-only still fails; deposited as results/exp123_channel_split.json)

## L105 — exp124 THE DEADLINE CURVE D(gamma) (2/3 gates PASS + the PRICE MAP V2 mu-column CORRECTION owned: exp117's class-based fill had labeled the GEOMETRY pair "mu tolerant" — exp100's deposited ladders show bipartite/complete REFUSE at every gamma at default mu (rate 0.0 through gamma_64): their (32, 0) cells need mu silence like the middle band; only DEFAULT0 and GAMMA0 are mu-tolerant (GAMMA0 at their priced gamma); the map re-issued corrected in the same push; THE CURVE: the torus's mu-silence deadline is NON-MONOTONE in pinning — gamma 1 never rescues (the exp123 conjunctive failure, anchor-verified DC-G3), gamma 4's edge 48 h, gamma 16's 72 h (the LATEST deadline), gamma 64's COLLAPSES to 36 h (DC-G1 REFUTED — the honest outcome; DC-G2 PASS: no sharpening with strength, the 36 h edge clears the bar); THE MECHANISM the curve names: at high gamma V tracks theta tightly, which OPENS the eps channel (eps(V - theta) with V ~ theta keeps the restoring force aligned) — the window's theta homogenization ACCELERATES with pinning (the joint relaxation rate rises toward mu*lambda + eps as gamma grows), so the window damage at gamma 64 accumulates faster than at 16 — the optimal pinning is INTERMEDIATE; this retro-explains three deposited facts at once: exp105's gamma 16 halving the trend (16 sits at the deadline's peak), exp98's stars verifying at gamma 2 (the cheapest cells live on the curve's low-gamma flank), and the two-dial structure itself (the torus's (4, 0) cell = the rising flank's first verified point); exp125 REGISTERED: THE U-SHAPE GENERALIZATION + THE ANALYTIC TEST — (a) the deadline curve on grid2d and path (does the optimum generalize or is the U torus-specific?), (b) the analytic deadline: the window's homogenization integral H(gamma, t) = the canon pattern's low-k amplitude decay under the joint linearized dynamics (rate mu*lambda + eps*gamma*lambda/(gamma + g*lambda) per mode) — the predicted edge = the onset where the remaining-time integral crosses the identity threshold; fit ONCE to the torus's four edges, PREDICT grid2d/path's edges with zero free parameters; deposited as results/exp124_deadline_curve.json)

## L106 — exp125 THE U-SHAPE GENERALIZATION + THE ANALYTIC DEADLINE (5/7 gates PASS + the batch's biggest repair owned PRE-RUN: the exp124 U-shape's right flank was PROTOCOL CENSORING, not physics — the audit found star_dt = min(0.1, 1.2/(gamma+deg)) makes the protocol's pre-settle duration gamma-DEPENDENT (the 73-cell walk shrinks 58.4 h at gamma 1 to 10.3 h at gamma 64; pre-settle ends 82.4/82.4/59.0/34.3 h across the ladder), so every deposited exp124 cell with onset beyond the real window NEVER FIRED the mu-silence: gamma-16's "72 h edge" cell and gamma-64's "36/48/72 h collapse" cells are NEVER-SILENCED CONTROLS — default-mu torus runs breaking at P=1.0 by exp100's refusal, re-verified in-batch (both controls P=1.0); L105's mechanism story ("high gamma opens the eps channel, the deadline collapses") was fitted to those artifacts and is WITHDRAWN; AX-G0 PASS (both anchors bit-exact: the exp124 gamma-4 curve and exp123's mu_only gamma-1 prefix); AX-G1 PASS (every deposited real cell reproduces in-batch, both never-silenced controls break); THE REPAIRED TORUS DEADLINE IS MONOTONE-RISING IN GAMMA — edge(1)=0 (never rescues, exp123-corroborated), edge(4)=48 h, edge(16)=52 h REAL (the fine grid 48/52/56/58 pins the first break inside the 59.0 h window), gamma-64 >34 h censored (P=0.0 flat through the protocol end) — DCG1R PASS: no U, no collapse; the deadline rises with pinning and gamma-64 is merely under-resolved (the protocol cannot ask beyond 34 h at dt 0.0176); UG-G1/UG-G2 PASS and the HEADLINE: THE MU-SILENCE DEADLINE IS TORUS-SPECIFIC — grid2d and path never break at ANY gamma in {1,4,16,64} x any real onset (P=0.0 flat across 224 runs), exp120's invulnerability extends from the full blockade to the mu-only channel and up the whole gamma ladder — the temporal vulnerability is a property of BOUNDARY-FREE GEOMETRY (the torus's intact reservoir has no boundary anchor; grid2d/path do), extending exp82's substrate-specific frontier and exp120's substrate-specific kernel to the pinning axis; AN-G1 REFUTED BOTH READINGS — the registered homogenization-integral analytic deadline is not the deadline's law: H1 (cumulative destroyed low-k amplitude under r_win = mu*lam + eps*gamma*lam/(gamma+g*lam), post-rate the exact mu=0 joint slow eigenvalue) INFEASIBLE with violated pair (rescue gamma16@48 predicted destroyed-RMS 12.87 > every break cell's 8.66 mV) — free homogenization over-destroys at high gamma because the clamps ANCHOR the zones and saturate the drift (the free-decay idealization ignores the Dirichlet structure); H2 (remaining-time integral, the registration's literal phrase) INFEASIBLE with violated pair (rescue gamma4@0 vs break gamma16@58): the exact post-silence eigenvalue's gamma-ratio (~4x) over-differentiates the rungs — the empirical deadlines differ ~1.1x, so the post-silence drag's gamma-dependence is NOT the free linearized mode decay's; AN-G2 VOID by pre-registration (no feasible torus fit to transfer); the deadline is REAL, censoring-corrected, monotone-rising, torus-specific — its analytic law must be built on the CLAMP-ANCHORED (Dirichlet) linearization with the walk's re-inheritance, not free homogenization; exp126 REGISTERED (subagent 5-b's pre-registered draft, research/gate_drafts_cg3_cg4_hp2.md — the 2026-prediction queue resumes): THE PLATEAU SPLIT — CG-P3's coin-vs-coupling discrimination: Panel A the neoblast_coin_p ladder {0.0, 0.4, 0.8, None} on the chain corpus machinery (rate monotone in p; coin-off lifts the two-headed fraction >= 0.05; L_hat := rate(None) faces the record's L~0.75); Panel B coupling at fixed coin (gamma {0.7x, 1x, 4x} — plateau gamma-flat within +/-0.10 while the deposited D(gamma) edges move); Panel C the record's GJ-block family convergence at coin {0.8, None}; Panel D the exp124 gamma-16 anchor re-run; deposited as results/exp125_u_shape_generalization.json)

## L107 — exp126 THE PLATEAU SPLIT (2/4 gates PASS as registered + both refutations carry the payload — CG-P3, Damon 2026 Zenodo 18358611, per subagent 5-b's pre-registered draft with two owned resolutions: Panel C's three family arms are the SCHEDULE classes {sustained, delayed, washout} (the draft's 2.3 "sustained-only" phrasing would make CG3-G3 trivially true — three identical runs; its own 2.2 mapping names the schedule classifier), and the neoblast coin kwargs are injected into exp70's regrow kwarg so coin-off is meaningful; PANEL A THE COIN LADDER IS MONOTONE AND THE RECORD-MATCHED RUNG LANDS ON L: pooled rates p=0.0 -> 0.000, p=0.4 -> 0.417, p=0.8 -> 0.750, p=None -> 0.000 — CG3-G1 REFUTED AS REGISTERED because the draft mis-registered the None rung as "coin off" when the stack's None = the coin MECHANISM ABSENT (regrow's default inheritance path, which reads 0.000 — wildtype-perfect on these planes); the prediction's SUBSTANCE is confirmed by the registered ladder itself: the abnormal fraction is carried by the coin parameter (0 -> 0.417 -> 0.750 monotone) and the p=0.8 rung — the record-matched NB_P — reads 0.750 vs the record's L ~ 0.75 TO THREE DECIMALS: the plateau is coin-carried and its stack value is deposited as 0.750 (L_hat redefined on the saturated coin rung; the None-rung mis-registration owned); CG3-G2 PASS — coupling at fixed coin is plateau-FLAT (gamma x0.7 -> 0.778, x4 -> 0.806; deviations 0.028/0.056 <= 0.10) while the deposited D(gamma) edges move (exp125's repaired 0/48/52/>34) — the two-knob separation holds per axis; CG3-G3 REFUTED AS REGISTERED AND THE REFUTATION RESOLVES THE DRAFT'S OWN INCONSISTENCY: the schedule band is 0.917 at coin 0.8 AND at None (sustained 0.889/0.667, delayed 0.944/0.944, washout 0.028/0.028) — but the registered gate letter ("convergence survives coin-off confirms mechanism-level convergence") INVERTS CG-P3's own text, which attributes the convergence to the COIN; the data decide: sustained-vs-delayed converge at coin 0.8 (delta 0.055 <= 0.15) and DIVERGE at coin-off (delta 0.277 > 0.15) — THE CONVERGENCE WAS THE COIN, exactly CG-P3's text attribution, refuting the draft's mechanism-level reading; washout never converges with either (0.028 — exp70's deposited cool arm, a protocol class not a drug class); CG3-A1 PASS — the gamma-16 torus anchor reproduces exp124's curve bit-exactly [0,0,0,0,0,0,0,1] (censoring note from L106 carried: the onset-72 cell is a never-silenced control — the anchor tests the harness, which is its purpose); exp127 REGISTERED: CG-P4 THE ORACLE-ONSET ORDER TEST (subagent 5-b's draft: the deadline edge tracks the v2 oracle's priced ratio — Spearman sign pre-registered) + THE GAMMA-1 FULL-GRID REPAIR ARMS (exp129's cross-finding owned below: grid2d gamma-1 over the FULL exp124 onset grid reads [0,0,0,0,0,0,1,1] — edge 48 h — refuting exp125's UG-G1 claim breadth which sampled only to 24 h; exp127 re-runs gamma-1 full grids on grid2d and path, extends the repaired deadline structure, and owns the corrected statement: the deadline is NOT torus-specific, it is monotone-rising in gamma with substrate-SHIFTED positions); deposited as results/exp126_plateau_coin.json)

## L108 — exp129 THE CHINESE TARGETS GATES (subagent 5-f's run of 5-c's pre-registered draft; 2/7 readable gates PASS with the honest UNPINNED class carrying two: A-G1 CONFIRM — the L74 reference re-derived bit-exactly (decoded 0.290 n=884, raw 0.3705 n=905, all six arm anchors exact, determinism exact) so the mapping harness is continuous; T1_G1 REFUTED — the metformin dose axis (Genes 2025 PMID 40282325, 10 points pinned from PMC12026922 Results text + IJMS companion PMC12345652) Spearman(sim, recorded) = 0.408 < 0.6: the registered hours-to-fraction transform's coarsening collapses every non-40 mM point to f=0.0 — the coarse ladder deposits as the slice's measured dose-response; T1_G2 REFUTED — the paper's own promote-band dip (1 mM 73.27 h vs control 76.57 h, n=30) has NO interior dip in the sim fine ladder [0,0,0,0.429,1,1]: S2R3/DA-G4 monotonicity is corpus-grain-specific, not a law — the biphasic refutation is the target's real content; T2_G1/T3_G1 UNPINNED — the registered decision constants do not exist as numbers in either paper (verified through main text, captions, supplementary bundles; the opa1 RNAi screen is categorical) — the honest class, never invented; T2_G2 CONFIRM — the timing anchor: grid2d gamma-1 over the FULL exp124 grid reads edge 48 h, within one onset step of the deposited cell — AND THIS CROSS-FINDING CORRECTS exp125 (see L107's exp127 registration): grid2d's gamma-1 deadline EXISTS at 48 h, so the UG-G1 claim breadth (sampled only to 24 h) and the UG-G2 torus-specific declaration are both corrected — the deadline is monotone-rising in gamma with substrate-SHIFTED positions, not torus-exclusive; T3_G2 CONFIRM — the 30-cell (cns,diff) grid on (generic,trunk) contains a rescue channel (12 cells <= 0.367, grid min 0.0) — the opa1;drp1 rescue epistasis has a stack home and is registered as a NEW experiment; provenance corrections owned: T2's species is Dugesia constrictiva and T3's is S. mediterranea CIW4 (not D. japonica as the draft's premise held) — no gate arithmetic changes, the DJ-baseline comparison weakens to cross-species; deposited as results/exp129_chinese_targets.json)

## L109 — exp130 THE OCTANOL KERNEL FIT (subagent 5-g's run of the Levin-series T1 target; 1/3 gates PASS: OK_A1 PASS — the gamma-4 torus anchor reproduces exp124's deposited curve and edges bit-exactly; OK_G1 REFUTED — the Fig 2A pre-treatment kernel is ANTI-ORDERED against the stack's P(break): Spearman -0.660 (stack [0,0,0,0,1,1] vs DH [0.85,0.90,0.58,0.10,0.10,0.10]); OK_G2 REFUTED — the flat zero-free-parameter prediction on the Fig 2B VNC kernel gives MAE 0.283 > 0.25 with the mirror MAE 0.718 (polarity-invariant refutation — the sign flip would be a free parameter, owned as a note only); THE READING the refutations force: the stack's deadline is a RESCUE curve (silencing mu early saves identity) while Oviedo-2010's kernel is a DAMAGE kernel (pre-treatment duration raises the two-headed rate then saturates) — the two objects share the GJ-block mapping but not the temporal law, and the record's 3 h peak (~4-fold) is an exp54 WRITE-WINDOW object, not a deadline object; the units resolution (days-reading onsets 3.12/6/12/24/48/72 h) was resolved against the paper's own verbal timeline BEFORE the gates ran and the hours-reading constant-prediction MAE 0.438 is deposited alongside; deposited as results/exp130_octanol_kernel_fit.json)

## L110 — exp131 THE ION-ARM PLANE ORDERING (subagent 5-g's run of the Levin-series T2 target; 3/3 gates PASS: IP_A1 PASS — the exp39 anchors reproduce bit-exactly; IP_G1 PASS — the simulated ion-arm headless ordering matches Beane 2011's plane series at Spearman 0.649 >= 0.6 (sim [0.333,0.333,0.667,1,1] vs published [0.00,0.00,0.67,0.16,0.40]); IP_G2 PASS — the strict ivermectin/SCH 2x2 sign test is a PERFECT DIAGONAL (ivermectin P(EA) 1.000/P(AF) 0.000 vs pub DH 0.92; SCH P(EA) 0.000/P(AF) 1.000 vs pub headless 1.00) — the two ion arms land on opposite diagonal corners exactly as the record's opposition requires; HONEST SCOPE owned: the PASS is specific to the exp39-verbatim arm — the exp70-kwargs variant ANTI-ORDERS (Spearman -0.725, deposited under robustness): the ordering is arm-wiring-sensitive, which is itself a bench-discriminating fact (the record's ordering chooses between the two stack wirings); deposited as results/exp131_ion_plane_ordering.json)

## L111 — exp127 THE ORACLE-ONSET ORDER TEST (CG-P4 CONFIRMED at the mined bar with the mechanism-confirming sign + the gamma-1 repair arms land: CG4-A1 PASS (the torus gamma-16 anchor bit-exact); CG4-G1 PASS — Spearman(uc_hat, v2) = -0.879 over all 7 substrates (censored@96) and -0.949 over the 4 finite-kernel substrates, |rho| >= 0.7 with the pre-registered NEGATIVE sign — the deadline edge DECREASES with the v2 boundary term: the most expensive substrate (scale_free, v2 8.62) closes EARLIEST (36 h at gamma 4), the cheap band closes late (random6 v2 2.04 at 72 h), the kernel onset and the compiler's price oracle ARE the same object on different axes — Damon's "kernel = oracle" reading lands on the stack at rho ~ 0.88-0.95 vs the dial axis's 0.81; the v2 ratios re-derived in-run by exp106's formula cross-check all five deposited values and small_world deposits new at 1.300; CG4-G2 REFUTED AS REGISTERED with the rung-coverage lesson owned: grid2d (v2 4.174) shows no finite kernel at the registered rungs {16, 4, 64} while cheap random6 closes — but the SAME DEPOSIT's gamma-1 repair arm supplies grid2d's kernel (edge 48 h at gamma 1, reproducing exp129's cross-finding bit-exactly, RG1 PASS) — on the corrected kernel map the truly kernel-free substrates are path and small_world (v2 0.603 / 1.300) and BOTH are v2-cheap, so the censoring-consistency substance holds and the refutation was the registered rung set missing the low-pinning flank where mid-v2 substrates keep their kernels; CG4-G3 VOID by dependency as pre-registered (exp125's analytic deadline refuted both readings — no predicted edges exist to rank against; the void is the deposit: the analytic law needs the Dirichlet/clamp-anchored rebuild before a mechanistic cross-check); THE CORRECTED TEMPORAL MAP (union exp125+exp127): torus 0/48/52/>34 and grid2d 48(g1)/>48(g4)/>58(g16)/>34(g64), random3 48(g4), random6 72(g4), scale_free 36(g4), path and small_world kernel-free at every rung — the deadline structure is monotone-rising in gamma with substrate-SHIFTED positions set by the v2 price, NOT torus-specific (exp125's UG-G1/UG-G2 breadth correction completed with in-batch data); exp128 REGISTERED (subagent 5-b's draft §4): H-P2 THE ANTERIOR-READ KNOCKOUT — Med8/ARZ depletion phenocopied by the M33 anterior-read knockout: the M33 gating lesion (spec_read_bypass_gap) separated from the knockout lesion (the anterior read's identity source removed) on the chain planes, gate-open arm separates the two; deposited as results/exp127_onset_oracle.json)

## L112 — exp128 THE ANTERIOR-READ KNOCKOUT (2/4 gates PASS + the strongest-direction refutation: HP2-A1 PASS — the bridge anchor reproduces exp120's deposited default curves bit-exactly on both substrates AND the chain inverse pair re-lands (no-M33 0.70 / M33 0.00 at 10 seeds); HP2-G1 REFUTED IN THE PROTECTIVE DIRECTION — the canon-stripped knockout does not fail anteriorly, it IMPROVES both zones on both substrates (grid2d err_z0 3.21 -> 1.19, err_z2 9.65 -> 7.00; torus err_z0 6.03/brk 0.50 -> 3.38/0.00, err_z2 7.52 -> 4.71): the Med8/ARZ anterior-restricted phenocopy dies at the graph level, and the M35 wound-domain mapping inherits the gate as the draft's FAIL note pre-registered; THE MECHANISM the refutation names: phi_spec_canon serves the below-line cells with the PRE-program canon spec — the intact arm's canon-correct gap values (-50) DRAG the above-line zones during the weak-pinning settle (the z0/z2 errors are settle-drag artifacts), while the stripped arm's junction-carried inheritance keeps the zones tight at the cost of gap contamination (overall 7.92 -> 9.52 grid2d, 9.99 -> 11.32 torus — exp90's UC-G5 chain-carry direction) — THE CANON READ IS A TRADE-OFF (gap-fidelity bought with zone-drag), not an anterior necessity: the third reader-decomposition datum after exp79 and exp90, and the within-harness reader-swap contrast (same pattern, reader swapped, all anchors green) is the deposit's core; HP2-G2 REFUTE-A letter fires with the diagnosis EXCLUDED and the mis-mapping OWNED: the draft's "intact verifies" target was exp120's BLOCKADE curve, but the no-blockage intact arm IS the default-mu run (exp122's damage, common to all arms — the anchors PASS and gate_open == intact BIT-IDENTICALLY at every decimal, so the knockout procedure corrupted nothing); HP2-G3 PASS (separable) — the registered phenocopy condition (gate-open reproduces the STRIPPED arm's anterior failure) is false: stripped shows no phenotype (brk_z0 0.00/0.00) for gate-open to phenocopy, and the construction note is verified empirically (on this harness the program's below-line values equal the canon's below-line values, so the gating axis has zero bite — the exp66 mis-map domain needs an actual mis-map); exp132 REGISTERED: THE DIRICHLET DEADLINE — the clamp-anchored analytic rebuild of exp125's refuted free-homogenization law: the drift computed on the sub-Laplacian with Dirichlet zones (the clamp-fixed-point offset solved exactly, the piecewise mu-active/mu-silenced linear dynamics in closed form), ONE inheritance-transfer coefficient fitted once on the torus's corrected edges (gamma 4: (36,48], gamma 16: (48,52], gamma 1 never, gamma 64 >34 censored), grid2d (gamma-1 edge 48, gamma-4 >48, gamma-16 >58, gamma-64 >34) and path (kernel-free) predicted zero-free — the model must reproduce BOTH failure lessons (the clamp-anchored saturation H1 missed; the walk-reinheritance-dominated post-silence structure H2 missed); exp133 REGISTERED (the M35 inherited gate): THE WOUND-DOMAIN READOUT TEST — whether the ARZ multi-lineage readout (arz_readout/neural_readout, M35-A) carries the anterior-restricted role the canon read lacks, on the chain planes; deposited as results/exp128_anterior_read_knockout.json)

## L113 — exp132 THE DIRICHLET DEADLINE (0/3 strict gates PASS + two instrumentation bugs owned BEFORE the deposit counted + the refutation that localizes the law's missing channel: the clamp-anchored linearized drift model — target-residual forcing b_V (the exp110 coupling pull) and b_theta (the mu leak toward the clamped zones), Dirichlet delta-V_Z = 0, piecewise mu-active/mu-silenced closed-form propagation, exposure = the boundary-drift time-integral D(gamma, t*), ONE transfer coefficient kappa — is INFEASIBLE on the torus's corrected constraints: the violated pair is gamma-16@52-break (kappa >= 0.0513) vs gamma-4@36-rescue (kappa <= 0.0319), with gamma-1@0 (kappa >= 0.0346) agreeing with the break side — the model's V-exposure falls with gamma ~2x too fast: pinning suppresses the boundary-V drift, but the EMPIRICAL deadline rises with gamma, so the mu-channel's marginal damage at high gamma cannot ride the V-drift; DL-A1 also fails (the never-silenced gamma-1 limit cannot clear the bar compatibly); DL-G3's structural lessons VERIFY: the drift is BOUNDED (the mu-active fixed point saturates at exactly 20.00 mV on the boundary — the H1 clamp-anchored-saturation lesson, the model carries what free homogenization lacked) and the post-silence recovery rate (0.001391) DIFFERS from the free joint eigenvalue (0.004610) — the H2 lesson; BUGS OWNED pre-deposit: (1) the V-deviation coupling block was assembled as -(gamma I + G_II) instead of the dissipative -gamma I - L_G,II (the row-sum self-decay was missing — the tell was D DECREASING in t*), (2) the eigendecomposition cache keyed on a shared dict id() so every phase-2 propagation reused M1's eigenbasis (the tell was D(t36) == D(t48) to float precision); THE REFUTATION'S PAYLOAD: the exposure channel is mis-identified — the walk's inheritance reads c.theta[src], NOT V (exp124's run_deadline read: theta_new from theta[src] below the line), and exp116's mu-phase localization independently placed the mu damage in THETA — the law's exposure integral must be over the THETA-deviation on the boundary, not V; exp134 REGISTERED: THE THETA-EXPOSURE DEADLINE — the identical Dirichlet model with D(gamma, t*) = the integral of |delta-theta| on the boundary intact cells, same ONE-kappa fit, same transfer protocol, same gates (the pre-registration is this sentence: the model form is exp132's with the exposure block swapped, decided before running); deposited as results/exp132_dirichlet_deadline.json)

## L114 — exp134 THE THETA-EXPOSURE DEADLINE (0/3 strict gates PASS — exp132's registered follow-up, the model form identical with the exposure block swapped to the theta-deviation on the boundary intact cells per the exp132 refutation's localization (the walk reads c.theta[src]); THE FIT IS STILL INFEASIBLE with nearly the same interval (kappa in (0.0529, 0.0341) vs exp132's (0.0513, 0.0319)) and the same violated pair (gamma-16@52-break vs gamma-4@36-rescue): at the boundary the theta and V deviations track each other closely (the eps coupling), so the exposure-variable swap does not move the structure; THE PRECISE LESSON the pair forces: the model's marginal mu-damage at gamma 16 is ~14 mV-units/h (D grows 8488 -> 8545 over the (48, 52] transition) where the empirical 4 h rescue-to-break transition requires ~200/h — the linearized target-residual family's mu-channel (the theta-leak toward the clamped zones, throttled by the mu/eps = 0.375 ratio and the fast zone-theta re-convergence) is ~14x too small to carry the empirical gamma structure; the structural lessons carry over (drift bounded at 20.00 mV — the H1 saturation lesson; recovery 0.001391 != free 0.004610 — the H2 lesson); THE ANALYTIC ARC'S HONEST STATE after three refutations (exp125's free homogenization both readings, exp132's clamp-anchored V-exposure, exp134's theta-exposure): the deadline's law is NOT any single-channel linearized exposure integral of the target-residual form — the remaining registered candidate is the WALK-CHAIN ACCUMULATION family (the inheritance chain's per-cell noise(0.6) accumulation over BFS depth with drifted parents — a discrete stochastic model outside the linear-exposure family, registered as exp135's object for the next batch); the arc's EMPIRICAL deposits stand complete: the censoring-corrected deadline map (exp125/127), the v2-oracle identity (CG-P4, |rho| 0.88-0.95), and the boundary-free-geometry structure; deposited as results/exp134_theta_exposure_deadline.json)

## L115 — exp137 THE UNIVERSAL READER: OUT-OF-DOMAIN MEDIA (4/4 gates PASS — the 101% Stage 5 path 1: the M33 two-source read, extended by ONE fixed front-end, consumes media outside the 19-substrate-type domain (19 types x 12 zone counts x n to 784, all simple undirected graphs) with ZERO rejections and bounded quality loss; THE M33 INPUT CONTRACT NAMED (the reader's implicit assumptions, localized by probe): A-SYM (A[i,j]==A[j,i]), A-NN (entries real >= 0), A-REAL (real-valued state pipeline), A-PAIR (pairwise n x n coupling), A-STAT (one static coupling for the whole read window), A-CW (closed world, edge set fixed and observable); SIX out-of-domain medium classes, each violating a DISTINCT assumption — dag (A-SYM), signed (A-NN), complex_phase (A-REAL), hypergraph (A-PAIR), time_varying (A-STAT), open_world (A-CW+A-STAT); THE ONE CONFIGURATION (D4, auditable, zero knobs): projection = magnitude |W_t| -> orientation-symmetrize (B+B^T)/2 -> time-average over the medium's own snapshot sequence -> pairwise (hyperedge factorization |w_e|/(|e|-1)), zero diagonal; executor = execute_two_source_n VERBATIM at the battery-wide point (gamma=64, mu=0, frontier=walk, MULTI 3-zone, seeds 1/2/3); D1 PASS (6 classes, 6 distinct violation sets, raw probes executed on all); D2 PASS (0 rejections / 180 OOD decodes + n=400 scale spot-checks, every decode finite and program_verified — 100% inside the 6.0 mV bar, stronger than the gate required); D3 PASS (pooled OOD median 0.65 mV vs in-domain 19-battery baseline 0.55 mV, ratio 1.18 vs the pre-registered 2.0x bound; per-class medians: dag 0.60 / signed 0.69 / complex_phase 0.71 / hypergraph 0.59 / time_varying 0.72 / open_world 0.56; n=400 spot-checks all decode, worst class median unchanged); D4 PASS by construction (one projection function, one executor call site, no per-medium parameters); THE RAW-PROBE DIAGNOSIS TABLE (the boundary localization, matching the pre-registered predictions): dag RUNS UNCALIBRATED (err 1.18 vs 0.60 projected — the row-Laplacian tolerates asymmetry, orientation silently ignored: A-SYM is not load-bearing at the dynamics level), signed RUNS DEGRADED (1.52 vs 0.69 — negative conductances fight the read, and traversal A[i]>0 silently skips negative edges), complex_phase RUNS WITH SILENT DTYPE COERCION (6 ComplexWarnings — a decode returned without acknowledging the imaginary-part discard: the most dangerous failure mode, an unowned assumption), hypergraph/time_varying/open_world INTERFACE-ABSENT (no static n x n object exists to pass — the reader cannot even be invoked; the first-snapshot proxies measured for the record); THE UNIVERSALITY BOUNDARY STATEMENT: the M33 read consumes COUPLING MAGNITUDE on a static, symmetric, pairwise support — orientation, sign, phase, higher-order incidence, and temporal structure are discarded by the one projection, so the decode prices the medium's CONNECTIVITY, not its SEMANTICS (a signed medium's inhibition and a DAG's flow direction are invisible to the decode); the native-canon information gap measured 0.00 mV at this scale for all six generators (the projection preserves support ordering, so the open-world potential-vs-realized gap did not bite — the gap measure is deposited, not assumed); REGISTERED (number on dispatch; 135-139 taken): THE SEMANTICS-CARRYING READ — the repair direction for the discarded channels: a sign-aware coupling term (inhibition preserved in the dynamics, not the projection), a phase/orientation-carrying state (the read decodes direction), a hyperedge-native walk (parents are hyperedges, not cells), and an adaptive re-read (the read window tracks the medium's flip clock); the falsification edge: a medium whose IDENTITY SEMANTICS live in the discarded channels (e.g. identity propagated only along negative edges, or only forward in time) should break the magnitude projection and force the repair; deposited as results/exp137_universal_reader.json)

## L116 — exp139 THE LEVIN T5 VOLTAGE-SERIES CROSS-VALIDATION (Workstream A; 2/5 gates PASS + one RECALIBRATION + two owned PARTIALs — the T5 target of the Levin-series ranked list (research/levin_voltage_series.md §4), run as the absolute-value anchor: the 119-entry series (99 PlanformDB rows + 20 curated) partitioned by a FROZEN per-row rule (drug_start_end/rnaic only — the shared direction_signature template is NOT a per-row regime tag, owned) into 5 regime families: A GJ-intact polarity/residue 30, B GJ-blocked 57, C hyperpolarization 21, D depolarization 5, E absolute-scale/adjacent-model 6; LV-A1 PASS — the partition is exact (119/119 unique; the two vmem_mv-bearing entries C11/C13 land in E) and the exp39 calibration reproduces bit-exactly at seed 1 (head -24.86 / trunk -50.26 / wound -38.03, deltas 0.000); LV-G1 PARTIAL (Spearman -0.105, inside the pre-registered (-0.6, 0.4) owned-honesty zone) — the family-POOLED outcome-deviation ordering does NOT cross-validate: E_stack (cutting 0.000 / GJ-block 0.667 / ion 1.000 / posterior-depol EA 1.000) vs E_meas mean(1-WT) over the families' DB rows (A 0.506 / B 0.391 / C 0.317 / D 0.645, D n=2 owned); the diagnosis the partial forces: (i) FAM-A is the RESIDUE family and its scalar is inflated by the octanol-lineage re-cut persistence rows (1-WT = 1.0 under a "GJ-intact" label — composition deposited per-row), and (ii) pooling erases the PLANE structure the record's effects live on — the plane-resolved instrument lands at the exp131 bar (LV-G4's C leg rho 0.6489 >= 0.6, matching exp131's deposited 0.649), so the pooled scalar is the mismatched instrument, not the arms; LV-G2 RECALIBRATION TARGET (pre-registered calibration class, NOT falsification — the T5 md's own clause), 3/4 sub-gates: the calibration trio sits inside the BETSE band [-80, -10] (a), head-trunk delta 25.40 mV inside +-50% of the 43 mV bistable swing (b), wound depolarization 12.23 mV inside +-50% of Chernet's 19.4 mV Xenopus impalement delta (c), but (d) FAILS — the GHK inference layer's 7-type map reads phagocyte/immune at -7.13 mV OUTSIDE the band (6/7 inside): the named recalibration target (the P2X/TRP-weighted immune-cell depolarization overshoots the tissue-level BETSE band — either the band is tissue-scale and immune cells are out of its domain, or the immune weights are miscalibrated); LV-G3 PASS 4/4 strict (the polarity skeleton survives: head > trunk, wound > settled mean, GJ-block abnormal > cutting, ion abnormal > cutting — one wrong sign would have refuted the mapping); LV-G4 PARTIAL with the deposit's sharpest finding: the C leg lands (headless-by-plane 0.6489) but the B leg is DEGENERATE — the pure junction-cut arm (gap_scale 0.05, exp39-V4's mapping) carries NO ectopic-anterior sign at ANY plane (EA 0/0/0 across head/trunk/tail while its tail abnormal rate is the graded 0.667 = the blind-guess mechanism), so the published octanol DH plane series (0.05/0.28/0.50/1.00/0.00, eids 415-419) has NO EA-predicting home on the junction-cut arm: the record's DH sign rides the DEPOLARIZATION channel (exp39-V3's deposited posterior-depol mapping, HL 0.946; exp123's channel-split) — a stack PREDICTIVITY GAP for the octanol family's headline readout, owned as a gap not a contradiction; SCOPE deposited not gated: the v2 price oracle prices stack SUBSTRATES (class-level rho 0.63, exp114's corrected form) and has no per-biological-family column (the family arms run the deployed DEFAULT0 sheet cell (1, 0.015) — a family-level v2 test would be an instrument mismatch), and the timing kernels stay with exp130's refutation (the stack's deadline is a rescue curve, Oviedo's kernel a damage kernel — no new timing gate registered); REGISTERED NEXT (numbers deferred to the batch coordinator to avoid collisions): the GHK immune-weight recalibration against an explicit tissue-vs-cell-scale band statement (T5's own repair clause), and the octanol-DH plane series re-tested on its deposited arm (posterior-depol by plane vs eids 415-419 — the arm the degenerate B leg should have run); deposited as results/exp139_levin_voltage.json)

## L117 — exp138 THE CORPUS RE-PASS WITH THE CURRENT STACK (workstream E; 4/4 gates PASS — E0 the bit-identity precondition green, E1 the claim PASSES at 0.2895 vs 0.290, E2 no slice regression, E3 no leakage — WITH THE ATTRIBUTION THE HEADLINE REQUIRES: the entire delta is ESTIMATOR-GRADE, not mechanism-grade, and the components that could not legally touch the corpus are deposited as zeros with their scope citations)

- E0 SANITY PRECONDITION (all four sub-checks PASS): the OLD config re-derives exp118's full deposit BIT-IDENTICALLY before any config swap — 47/47 arm rates equal, raw 0.3705 / decoded 0.2900 / decode 0.6928 (n 905/884), extraction pins l73 17@0.189 / l74 11@0.105 / ctrl 0.00-0.38-0.49 / C4=21, and per-row frame integrity (every scored row's recorded_corrected equals the deposit). The harness is anchored.
- THE TOUCHPOINT MAP (pre-registered in the module docstring before the run): of the four current-stack components exactly ONE has a live corpus touchpoint — the COIN PRIOR on the neoblast arm (the only arm the M37-A coin was adopted into, exp88 C2). M-ORACLE zero by scope (the exp108-117 arc prices substrate dials for the compiler; the corpus arms are 1D-sheet DEFAULT0 chains at their verified cell (1, 0.015) — exp118's scope note restated; exp139's family-level v2 caveat independently confirms the instrument mismatch). M-CENSOR zero by construction (the record frame IS the adopted C3/C3'/C4 corrected-censored frame in the 0.290 baseline). M-CANON measured as a side-car and NOT adopted into the gate config (the arz knob shifts the RNG stream — 1+K draws per guess-path cell — so a 3-seed "no-op" adoption would inject pure Monte-Carlo noise into the gate).
- M-COIN RESULT: the three neoblast arms re-estimated at the exp126-deposited protocol (coin 0.8 unchanged, the M33_KW read form, 12 fresh seeds 11-22 replacing 3): head 1.0 -> 0.917, tail 0.333 -> 0.75, trunk 0.667 -> 0.583. SC-1: the pooled rate reproduces exp126's deposited p=0.8 rung BIT-EXACTLY (0.75 over 36 runs) — the harness anchor for the prior.
- GATE-E1 PASS: decoded MAE 0.28997 -> 0.28952 (deposited bar: strictly < 0.290; n=884, same decoded row set). GATE-E2 PASS: S1 junction/bioelectric +0.0000 and S2 dose/pharmacology +0.0000 (bit-identical arms — no component touches them), S3 gene/knockout -0.0011 (0.1517 -> 0.1506, the only slice in scope; tolerance was +0.02). GATE-E3 PASS: the config-delta provenance table is all deposited/non-corpus constants (coin 0.8 = exp88/86/126; phi 0.75 = exp86 M33_KW as used by exp126's ladder; fresh-seed convention = exp86/exp126); no parameter searched against the corpus.
- THE ATTRIBUTION (the deposit's core — what the 4/4 headline hides): (a) SC-4a the read-weight re-pricing (phi 1.0 -> 0.75) is OUTCOME-INERT on the chain neoblast arm — the 12-seed per-plane rates are IDENTICAL at both weights (0.917/0.75/0.583), so the entire -0.0004 is the 3 -> 12 fresh-seed ESTIMATOR upgrade shedding 3-seed binary noise on one arm; (b) SC-4b the FLAT-PRIOR form of the same prior (all neoblast arms := the pooled 0.75, the most leakage-proof reading) REGRESSES (decoded 0.2934, +0.0034) — the prior's per-plane structure is load-bearing and the pooled number alone would have refuted E1; (c) SC-3 the FRAME SPLIT: the coin prior helps the DECODED (censored) frame (-0.0004) and hurts the RAW frame (+0.0011) — the tail plane shows the tension explicitly (raw 0.407 -> 0.260 BETTER while decoded 0.253 -> 0.497 WORSE: the C3' control-anchored subtraction moves the tail target to 0.0-0.5 where the coin-0.8 arm's 0.75 landing scores badly).
- SC-2 THE CANON RE-PRICING'S CORPUS VERDICT: exp133's ARZ rate-inert claim TRANSFERS to the corpus GJ operating point (gap 0.05 blockade) — sustained 0.667/0.667, delayed 0.944/0.944, washout 0.028/0.028 arz-on/off at 12 fresh seeds pooled per schedule (all deltas +0.000, bar 0.10), and the arz-on column reproduces exp126 Panel C's coin=None rates bit-exactly (the side-car's own continuity anchor).
- HONEST VERDICT: the current stack beats the 0.290 decoded reference by the pre-registered strict bar, but the margin is estimator-grade (Monte-Carlo variance on ONE arm), and NO mechanism-grade improvement was available from the four components at their legitimate touchpoints — the corpus residual is carried by S2 dose/pharmacology (n=210, mae 0.458) and S1 junction (n=320, mae 0.332), both untouched by the current stack. A refutation-shaped confirmation: the stack's recent wins (price map, deadline map, coin landing) live on the compiler/deadline side and do not price the 1D corpus arms.
- REGISTERED NEXT (numbers deferred to the batch coordinator to avoid collisions): (a) the frame-tension repair — a family-scoped censoring exemption (the neoblast family's raw pool 0.799 is mechanism-matched by the coin arm's 0.767, so the C3' plane subtraction double-counts the family's own hot bias) must be pre-registered on NON-corpus grounds before any frame edit is legal (else leakage); (b) the S2 dose arms carry the same 3-seed estimator noise the neoblast arm just shed — the registered repair is 12-seed re-estimation of the dose-class arms (zero new mechanism, the same instrument upgrade); (c) the ARZ readout can now be dropped from the corpus GJ arms at zero rate cost (SC-2, the exp133-consistent simplicity re-pricing) — deferred to the next mapping revision to keep this pass bit-comparable. Deposited as results/exp138_corpus_repass.json; run as python3 -m experiments.exp138_corpus_repass (wall 11.3 s — the full corpus, the 20-minute subsample clause not bound).

## L118 — exp135 THE WALK-CHAIN ACCUMULATION (B, 1/4): the deadline as threshold-crossing of a persistence-kernel integral over the walk chain's theta-mismatch (kappa, tau_p fitted ONCE, no per-gamma refit) is INFEASIBLE at every tau_p on the grid [2..128, inf) — the kappa interval is EMPTY, binding pair g16@72-break vs g64@24-rescue; per-gamma refits ARE feasible (kappa 0.42-0.90 non-overlapping), so GATE-B3's no-refit bar kills the family exactly as curve-fitting; GATE-B1 curve FALSE, GATE-B2 sign FALSE, GATE-B4 ablation TRUE (debt-only vs boundary-only discriminate: kmin 0.145 > kmax 0.037). THE DEPOSIT BEHIND THE REFUTATION: the chain's DIRECT simulation (harness Euler walk, multi-source BFS order, non-resetting state) reproduces the empirical deadline curve for the FIRST TIME — direct edges 0/48/52/null vs deposited 0/48/52/>34 — so the law LIVES in the chain's full state; no scalar reduction (per-step, exposure-swapped, or accumulated-kernel) carries it. Fourth refutation closing the scalar-reduction family: per-step (exp132), swapped (exp134), accumulated (exp135). Transfer leg owned as a harness gap: kernel-free substrates (grid2d/path) produce NaN predicted edges (0/26 agree) — the chain construct presumes the torus's boundary-span structure. REGISTERED NEXT: state-space reduction (the deadline as a joint (span-theta, intact-V) threshold, not a scalar integral) or simulation-level law with the analytic question formally re-posed; transfer repair = chain construct for kernel-free substrates
- GATE-B1 FAIL: the single-(kappa,tau_p) fit cannot order the four anchors — joint feasibility empty at every tau (kmin>kmax, e.g. tau=4: 0.660 vs 0.609); the binding cell flips to g64@24-rescue whose debt D=663 exceeds every break-cell's debt at any shared kappa
- GATE-B2 FAIL: dD/dt at the g16 transition 42.6 D-units/h vs g4 15.5 — debt accumulates FASTER at high gamma (the walk is longer per unit sim time), so the threshold model predicts EARLIER deadlines with pinning, the empirical curve's opposite
- GATE-B3 FAIL: per-gamma kappa intervals [0.42,inf)/[0.63,0.86]/[0.49,0.61]/[0.66,0.90] are pairwise disjoint — four models, not one
- GATE-B4 PASS: the ablation (boundary-only, chain deleted) is feasible-infeasible INVERTED vs the full model — the chain's state is load-bearing, confirming exp116's mu-placement downstream of the boundary
- THE DIRECT-SIM DEPOSIT: harness-verbatim deterministic walk chain (8 sub-steps/cell, injection at target, mu latched per exp124) hits break at 48/52 on g4/g16 and stays rescue through the g64 window — the first constructive reproduction of the censoring-corrected curve; marginal_rates: kappa-rate mV/h NaN under every scalar reading (the diagnostic that killed the reduction)

## L119 — exp136 THE GENERATOR V6, FIRST REGISTERED RUN (C, 0/4): the compiler as-built delivers ZERO inventions — no anatomy in the search space clears novelty (N* = 82.29, the library's 95th-percentile internal NN distance over 72 members) while passing the two-channel audit at the 6.0 mV bar; the delivered run is the IN-REGISTERED REPAIR of the first run (the original "cuts rejection-sampled away from library cuts" clause was INFEASIBLE — the 72-member library carries ~260 boundary positions blanketing the pole domain; repair pre-registered in the docstring BEFORE the delivered run, gates unchanged); search: 60 stratified seeds x 4 generations, J = quad_err + 5*relu(N*-NOV_lib), best J 1.27 (round 0), novel counts 15/34 rising but none audit+decode passing. OWNED DIAGNOSIS: the pole-read domain [-35,-15] mV on 1-4 disjoint zones is EXHAUSTED by the existing library — novelty within the pole domain is anti-correlated with writability (the two-channel audit's V-channel degrades with distance from library cuts); the generator's failure is a DOMAIN failure, not a search failure. REGISTERED NEXT: (a) widen the emitted domain below the exp128 re-pricing (canon-strip improves zone pricing — the below-line read may unlock off-pole regions), (b) multi/exp94-class programs (non-disjoint zones) as the novelty-bearing class, (c) the N* bar re-derived on the widened domain before any gate re-run
- GATE-C1 FAIL: 0/10 anatomies clear N*=82.29 novelty AND enter the audit; the library's internal spread blankets the 1-4 disjoint-zone pole space
- GATE-C2 FAIL: audit_pass_count 0 (no candidate reached the audit with novelty in hand)
- GATE-C3 FAIL: decode_pass_count 0 (conditional on C2)
- GATE-C4 UNTESTED: pairwise-novelty among inventions undefined at zero inventions (structure preserved for the re-run)
- QUADRATURE DIAGNOSTIC: exp84's composition law re-test on the invented map deferred (spearman null at zero inventions) — re-runs with the first passing cohort

## L120 — exp140 THE STATE-SPACE DEADLINE (F, 1/4): the joint-threshold reduction AS REGISTERED (one half-plane in (span-theta-dev, intact-V-dev) = exp135's own th_span_dev/err_intact at the protocol read; machinery-verbatim instrumented reuse of exp135.simulate(), asserted bit-exact max|d| = 0.0 on all four deposited scalars at every anchor) is REFUTED on the deposited eight — the g64@36-break late control (2.777, 8.203) is Pareto-dominated by rescue g16@48 (3.537, 9.535), so the break/rescue hulls intersect in EVERY projection (exhaustive 36001-direction scan: best gap -0.446) and the min-violation line must INVERT the intact-V weight (w2 = -1.352, physically backwards), sacrificing g4@48 and false-breaking all 52 flat-zero transfer cells. THE DEPOSIT BEHIND THE REFUTATION: the six censoring-corrected bracket cells ARE separable with an interpretable BOTH-POSITIVE normal (w = (+0.293, +0.365), hard margin 0.234); that refit predicts g16@72-break and all six g64 in-window flank rescues (7/8 F3 predictions; sole miss g64@36, score -0.818 vs deposited P=1.0 break) and reproduces the deposited deadline edges 0/48/52/null EXACTLY with the sole curve mismatch g64@36 (R7); the transfer leg repairs CONDITIONALLY — 0/26 + 0/26 false breaks on grid2d/path under the feasible separator (exp135's NaN leg is a kappa artifact: the state readouts exist on every substrate, no boundary chain needed). F2 PASS: neither axis alone separates the eight (x-only and y-only both infeasible) and both coordinates materially weight the normal (shares 0.65/0.35) — the refuted scalar family cannot return single-axis in this plane. ROOT CAUSE (two legs): (a) the deterministic mean-field state at read does not encode the g64@36 break at all — the direct sim's own scalar there is 4.904 < 6.0, and no functional of that state (this projection included) can recover what the state does not contain; (b) the mu-latch's marginal state damage at the g64 bracket moves break-ward (+0.592, +0.236) but falls 0.760 x-units short of clearing the rescue hull — exp134's 14x-shortfall bug-class recurring in state units. REGISTERED NEXT: (a) adopt the state-space CURVE law as the standing reduction (both-positive half-plane on the censoring-corrected cells; the 0/48/52/>34 edges live in the (span-theta, intact-V) plane with single-axis thresholds dead); (b) the late-control gap needs a state direction the mean-field read collapses — theta PROFILE shape (not RMS), residual mu exposure at read, a pre-settle read, or a NOISE-CARRYING state (the harness breaks g64@36 at P=1.0 while the mean-field sits 1.1 mV under the bar — the stochastic state, not its mean, is the remaining carrier)
- GATE-F1 FAIL: the eight deposited anchors (break g1@0/g4@48/g16@52/g16@72/g64@36, rescue g4@36/g16@48/g64@34) are linearly INSEPARABLE — hulls intersect; min-violation line w = (+1.568, -1.352), b = 7.345 violates g4@48 (margin -0.739); certificate: 36001-direction scan best gap -0.446, piercing anchor g64@36 dominated by g16@48
- GATE-F2 PASS (basis = the min-violation line, as pre-registered): weight shares 0.650/0.350 (bar 0.10); x-only INFEASIBLE (break x [2.78, 6.91] overlaps rescue [2.19, 3.54]), y-only INFEASIBLE (break y [8.20, 10.73] overlaps rescue [7.97, 9.54]); CAVEAT owned: the basis normal is not physically interpretable (negative intact-V weight) — the pass certifies joint > scalar, not the fitted direction
- GATE-F3 FAIL (on exactly one of eight predictions): 6-cell refit feasible (hard margin 0.234, w = (+0.293, +0.365) both positive); g16@72 -> break (+1.31) CORRECT, all six g64 flank cells -> rescue CORRECT, g64@36 -> rescue (-0.82) WRONG (deposited break P=1.0)
- GATE-F4 FAIL (inherited): frozen F1 min-violation line false-breaks 26/26 (grid2d) and 26/26 (path) — direct-err breaks 0 on both (the line, not the readouts, is at fault); CONDITIONAL REPAIR (R6, post-run): the feasible refit separator false-breaks 0/26 + 0/26 with deep rescue margins (min -4.56/-4.61) — exp135's NaN transfer leg repaired under a feasible separator
- R7 CURVE REPRODUCTION: the refit separator's predicted torus edges are g1 0, g4 48, g16 52, g64 null = the deposited 0/48/52/>34 curve; sole full-curve mismatch g64@36; R5 certificate + bracket displacement (dx +0.592, dy +0.236, shortfall 0.760) deposited in results/exp140_state_space.json with per-cell state snapshots and (x_t, y_t) walk trajectories for all eight anchors

## L122 — exp142 THE SIGN-CARRYING READ (Workstream H; 4/4 gates PASS — the L115-registered SEMANTICS-CARRYING READ delivered at its sharpest edge, SIGN, as the MINIMUM semantics extension of the universal reader: THREE pre-registered clauses, zero knobs — R3 the projection's magnitude-symmetrize becomes SIGN-PRESERVING symmetrize (Re(W_t) -> (R+R^T)/2 -> time-average; for complex-phase media Re = |W|cos(phi), the phase-ALIGNED component: exp137's SILENT dtype coercion becomes an OWNED real embedding, the reactive sin(phi) channel stays discarded, owned scope), R1 STRUCTURE ON |A| (canon labeling, Euler dt, and the walk's frontier/BFS traversal on |A[i,j]|>0 — the exp137-named `A[i]>0` traversal filter DROPPED: a signed edge is a first-class edge that connects exactly as its magnitude), R2 SIGN IN THE DYNAMICS (the coupling consumes the signed matrix verbatim — a negative conductance anti-diffuses, the honest signed physics; no commit-time reflection invented: the walk is a delivery schedule for the spec/canon layers, so the polarity channel is the dynamics'); H1 PASS — fidelity IMPROVES on exactly exp137's two degraded classes on exp137's own instance grid (same generators, same seeds): signed median 0.575 mV vs the magnitude-read's deposited 0.685 (-16%, bar <=0.60) and complex_phase 0.525 vs 0.715 (-27%, bar <=0.63); class max errs 0.67/0.62 vs exp137's 1.69/1.72; verify 1.00 — the pre-registered mechanism confirmed: the magnitude projection OVER-COUPLES (every edge attractive drags committed identity across inhibitory junctions as if excitatory); H2 PASS — 12 adversarial sign-flip pairs (24 probes: carrier families zone-tail / zone-head / canon-boundary x dose ladder 4/16/64/256; each pair magnitude-identical BITWISE, differing ONLY in the carrier chord set's sign): the magnitude-only read decodes 12/12 pairs IDENTICALLY (sign-blindness VERIFIED, not assumed — exp137's diagnosis made measurable), and the sign-carrying read SEPARATES 6/12 pairs at the VERDICT level (F1@64, F1@256, F2@64, F2@256, F3@256 — the sign rule CHANGES the decode verdict relative to magnitude-only: the negative-carrier member flips to program_verified FALSE, err 6.2-16.7 mV, while the magnitude read passes both members identically); the dose-response is monotone (inhibition degrades the decode dose-dependently — exp137's "negative conductances fight the read" shown CAUSALLY), and at weak dose the negative member can decode BETTER (F3@4: 0.46 vs 0.51 — anti-diffusion SHARPENS the canon boundary at weak inhibition, destroys at strong: the polarity channel is live in both directions); H3 PASS — STRICT SUPERSET proven bit-exactly: on the in-domain control (torus) the sign-carrying read's final V states are BIT-IDENTICAL to exp137's read (median 0.55 == 0.55, verify 1.00/1.00) — every clause reduces to exp94 verbatim on all-positive input; H4 PASS — 0 rejections across all 210 decodes (60 OOD + 6 control + 144 probe), every err finite, no coercion warnings (warnings-as-errors retained); INSTRUMENT DISCLOSURE (in-docstring, pre-run): an F1-only 1-seed calibration bracketed the dose response before the registered run; gates and bars were fixed before it and the H2 premise was tested across ALL families and doses; REGISTERED NEXT: (a) the phase-native read — the reactive sin(phi) channel this extension still discards (a complex-state pipeline, not a real embedding), (b) the temporal read — the flip-clock channel for time_varying/open_world media, (c) the hyperedge-native walk; the L115 falsification edge carried forward sharpened: a medium whose identity semantics live ONLY in the reactive or temporal channel should still break this read; deposited as results/exp142_sign_read.json)
- GATE-H1 PASS: signed median 0.575 <= 0.60 (exp137 magnitude-read 0.685, -16%); complex_phase 0.525 <= 0.63 (0.715, -27%); max 0.67/0.62 vs exp137's 1.69/1.72; verify 1.00 both classes
- GATE-H2 PASS: precondition 12/12 pairs magnitude-sign-blind (bit-identical errs at every seed); separation 6/12 pairs verdict-level (F1@64, F1@256, F2@64, F2@256, F3@256) — the sign rule changes the verdict relative to magnitude-only, negative-carrier member flips to FALSE at err 6.2-16.7 mV
- GATE-H3 PASS: torus control final V states BIT-IDENTICAL between arms (0.55 == 0.55, verify 1.00/1.00, backstop 0.10 unused) — the extension is a strict superset
- GATE-H4 PASS: 0 rejections / 210 decodes (60 OOD + 6 control + 144 probe), both arms, warnings-as-errors

## L121 — exp141 THE GENERATOR WIDENED DOMAIN (G, 0/4, deposited by the orchestrator after workstream-G context death; module + results complete, ledger entry unwritten): the L119 repair run — domain widened [-35,-15] -> [-60,-15] (full identity repertoire per exp128's canon-strip re-pricing), disjointness RETIRED (zones may touch/overlap), 1-5 zones, 96 stratified seeds — delivers ZERO inventions again; C1-C4 all false. THE DIAGNOSTIC DEPOSIT: exp136's mechanism claim VERIFIED off-pole — novelty/writability anti-correlation breaks outside the pole domain (spearman nov-vs-quad: pole-only -0.726, pooled -0.245, round-0 -0.033) — novelty and writability DO decouple in the widened space, yet no candidate clears N*=82.29 (library-derived, domain-independent) AND passes the two-channel audit at the deposited operating cells [[1.0,0.015],[4.0,0.0]]. OWNED DIAGNOSIS v2: the residual killer is the AUDIT OPERATING POINT, not the domain — the emitted-cell ladder is pole-calibrated; off-pole inventions are audited at cells never calibrated for them (exp136/141 share the same two search cells). REGISTERED NEXT: per-invention operating-point selection from the price-map ladder (the emitted cell is part of the compiled program — extend the ladder off-pole before the next gate run); the tol discrepancy owned (d_struct match tol 0.01 here vs 0.02 in exp136 — N* comparison cross-tol flagged, re-derive before gate re-run)

## L123 — exp143 THE LATE-CONTROL STATE (I, 0/4, REFUTATION — the pre-registered refutation branch fired): the L120 repair directions tested as ONE-feature extensions of exp140's frozen six-cell separator (w=(+0.293,+0.365), margin 0.234, s6(g64@36)=-0.8184 — reproduced to 1e-4; sim fidelity 0.00e+00 vs BOTH exp135.simulate() and exp140.simulate_instrumented() at all 8 anchors). Six declared scalar features — Z1 span-theta-deviation PROFILE GRADIENT, Z2 spectral triplet (orthonormal DCT-II k1-3 of the mean-centered deviation profile), Z3 residual-mu exposure (dt-weighted post-amputation integral of RMS_span(mu*(A@th-th*degA)); per-cell latch phases deposited: g64@34/36 fire mid-SETTLE, confirming L120's note), Z4 pre-settle read (x at settle start), Z5 DCT-k1 alone, Z6 margin-to-bar (6.0-err) — each tested under (A) the registered pivot family score=s6+wz*(z-z0) (every interval EMPTY) and (B) the canonical free-bias form score=s6+a*z+c solved as an exact piecewise-linear LP over break-rescue crossings (every one infeasible: min f 0.349-0.655 line units; disclosure in-module: A was the initially-run form, B added pre-deposit to rule out pivot-choice artifacts). GATES I1-I4 all FAIL at the I1 feasibility step (so LOO/edges/transfer never reached); 2D eight-anchor infeasibility re-certified (exhaustive scan best gap -0.4455). THE CERTIFICATE: a TWO-SIDED PINCER — rescue g16@48 (closest rescue to the line, -0.110) sits ABOVE break g64@36 on all four state directions (gradient 3.553>3.061, triplet 11.20>7.55, exposure 4.86>3.55, pre-settle 3.46>2.24) killing every positive weight, while bracket rescues g4@36/g64@34 sit BELOW breaks g4@48/g64@36 (gradient 2.22/2.44 vs 3.04/3.06, exposure 1.31/2.82 vs 3.45/3.55, pre-settle 1.81/2.15 vs 2.91/2.24) killing every negative weight; Z1-Z4 LPs bind g64@36 vs g4@36 (same latch hour 36, neighbouring gamma), Z5-Z6 bind g64@36 vs g16@48; the margin-to-bar statistic INVERTS (rescue g16@48 0.13 mV under the bar, rescue g64@34 1.44, BREAK g64@36 1.10 — the deterministic scalars do not order the labels); a latch-phase binary is constant on the fit set (excluded by construction). The late control is NOT in the mean-field chain state under any registered one-feature extension — the state-space family now carries a domination certificate spanning the base plane AND five additional state directions, consistent with exp140's deposit (direct-sim scalar 4.904 < 6.0 bar, 0.760 x-units short). REGISTERED NEXT: the noise-carrying state — a stochastic chain (V-noise stationary RMS < 1 mV + inheritance noise 0.6 mV iid, per exp135, both omitted from the chain sim) in which the deposited P=1.0 break at g64@36 (mean-field 1.10 mV under the 6.0 bar) becomes decidable as sub-margin noise statistics rather than mean-state geometry; deposited as results/exp143_late_state.json)

## L124 — exp144 THE AUDIT AT OFF-POLE OPERATING POINTS (J, 1/6, refutation that RE-LOCALIZES the killer): the L121-registered repair run — exp141's search re-run IDENTICALLY (replication check deposited: per-round novel counts, pool 253, best-J all bit-match the exp141 deposit; N* 82.288 re-derived at CUT_TOL 0.01 in both — L121's cross-tol flag resolved), the operating ladder EXTENDED to 9 rungs from the price-map v2 vocabulary (exp117 PM-G2: exp136's 4 deposited pole rungs + 5 cross cells (1,0) MU0_SILENCE, (4,0.015)/(16,0.015) GAMMA0 default-mu, (32,0) GEOMETRY, (64,0.015) fast-arm-at-default-mu), frozen and DEPOSITED at stage ladder_deposit BEFORE search candidate 1, per-invention rule (pass = ANY rung quad<6.0; emitted = argmin frozen cost key gamma/4+(mu>0)) — delivers ZERO inventions again; J1 REFUTED, J2/C2 0/0 REFUTED, J3/C3 0/0 REFUTED, C1/C4 REFUTED, J4 PASS (procedural: frozen-ladder deposit precedes the search, argmin selection recomputation-verified, provenance complete, superset of exp136's ladder). THE RE-LOCALIZATION: the funnel is 253 pool -> 96 lib-novel (NOV_lib > N*) -> 0 SPLICE-CLEAR (0/96; best nov_splice observed 65.37 vs bar 82.29 among the top-J 24) -> 0 delivered — exp141's two-channel audit NEVER RAN; the anti-recombination splice clause (C1's nov_splice > N* term) kills every lib-novel candidate UPSTREAM of the audit, so L121's "audit operating point" diagnosis is refuted as the proximate killer. THE DIRECT AUDIT TEST (pre-registered diagnostic fill: the top-24 splice-failing lib-novel candidates by J, non-gate-bearing, cap owned in advance for exactly this contingency): 24/24 PASS the two-channel audit — INCLUDING at exp136's own deposited pole rungs (quad 0.33-1.12 at (1,0.015)/(4,0) vs the 6.0 bar — these candidates were writable at the deposited cells all along) and trivially at the extended rungs (best quad 0.059-0.064); 19/24 decode-stable 3/3 under C3 semantics. eV/eTheta DECOMPOSITION DEPOSITED: zero audit failures exist — both channels healthy off-pole (eV 0.045-0.749, eT 0.039-0.838, all << 6.0 at every rung), so the pre-registered refutation branch's own premise (the killer INSIDE the V- or theta-channel off-pole) is ITSELF refuted; Spearman(NOV_lib, best-rung quad) = -0.607 — more novel audits BETTER. OWNED DIAGNOSIS v3: the residual killer is the SPLICE CLAUSE's calibration — the 48,564-profile single-crossover family of the frozen 72-member library blankets the widened [-60,-15] x 1-5-zone space so completely that no anatomy clears lib-novelty AND splice-novelty simultaneously (exp136's own wording made the splice check part of C1's novelty clause, and the corpus-defines-the-threshold rule was applied to the library but never to the splice family it induces). REGISTERED NEXT: (a) re-derive the anti-recombination bar from the splice family's OWN internal spread (N_splice* = the same 95th-pct NN rule applied to the splice corpus — symmetric with N*'s derivation) or prune the family to non-degenerate pairs with a deposited coverage audit of how much of the widened space it actually blankets, BEFORE any further gate run; (b) pre-name the SILENT-ONLY degradation (every fill emission was the cheapest rung (1,0), quad there 0.06 mV vs 1.12 at the pole rungs — writability audits at near-silent cells risk freebie passes, the mirror of exp136's STAR-ONLY clause); (c) the 24/24 audit + 19/24 decode result is deposited as the paid-in-full answer to L121's operating-point question — the audit and the decoder are NO LONGER the binding constraints; deposited as results/exp144_audit_operating_points.json)

## L125 — exp145 THE PHASE-NATIVE READ (K, 4/4 gates PASS — the L122-registered phase-native read delivered, closing exp142's owned scope: the reactive sin(phi) channel): ONE pre-registered rule, zero knobs — PN1 DIAGNOSTIC: pooled reactive energy fraction rho = sum_t ||Im W_t||_F^2 / sum_t ||W_t||_F^2, reactive-dominant iff rho >= 0.5 (fixed a priori); PN2 PROJECTION: Im branch A_t = Im(W_t) if reactive-dominant else Re branch (exp142's R3 verbatim), symmetrize -> time-average -> zero diagonal; PN3 STRUCTURE+DYNAMICS: exp142's R1+R2 via execute_signed VERBATIM (no new executor code — the phase-native read IS the sign-read with the projection channel switched by PN1/PN2). MEDIA (identity semantics ONLY in the reactive channel): (a) 12 adversarial pairs = purely imaginary ring substrate (W = 1j, phi = +pi/2) + carrier chords a +/- i*b, a = 4.0 BITWISE class-independent (semantically empty), class = sign of the imaginary carrier, magnitude-identical AND real-component-identical bitwise across members; exp142's F1/F2/F3 geometries verbatim; dose ladder {64,128,256,384} DISCLOSED as derived from exp142's deposited dose response (flips at F1@{64,256}, F2@{64,256}, F3@{256}), with b=64/256 doubling as BIT-EXACT anchors to the deposit; (b) paired-conjugate grid W = 0.5*B*w + i*s*B*w*sigma (exp137 helpers, SignedMedium draw order, SHARED base seeds 80_000+i so instance i of the two classes are bitwise conjugates; rho = 0.8 exactly). GATES: K1 PASS — the sign-read (exp142's Re-projection) is VERDICT-BLIND on 12/12 reactive pairs (Re projections bitwise equal across members, identical per-seed outcomes and majority verdicts) and CONFIDENTLY blind on the conjugate grid (sign arm decodes the semantically-empty real component 0.5*B*w with BITWISE-identical outcomes across conjugate classes 30/30 — the read reports success while the identity is invisible; the falsification edge confirmed at both the degenerate and the confident extreme); K2 PASS — preconditions 12/12 magnitude-blind (|W| bitwise equal), PN1 selects the Im branch on all 24 battery members, and the exp142 anchors reproduce the deposited sign-arm errs BIT-EXACTLY at all 6 anchored (family, dose) cells; the phase arm SEPARATES 11/12 pairs at the verdict level (all but F3@64, where the negative member still verifies at err 4.75-5.27 < 6.0 — consistent with exp142's deposited boundary); dose response monotone-preserving (F1 down-member 8.9 -> 13.9 -> 13.9 -> 13.9 mV); K3 PASS — pooled phase-arm median on the conjugate grid 0.57 mV <= 0.60 (up 0.56 / down 0.575, verify 1.00 both classes, err_native 0.57/0.55) — exp142-bar fidelity on media the current read cannot even see the identity of; K4 PASS — strict superset: torus control final V BIT-IDENTICAL sign-vs-phase at every seed (verify preserved), exp142's deposited signed class 12/12 decodes bit-identical (rho = 0 => Re branch analytic), complex_phase class: uniform phases put rho ~= 0.5 BY CONSTRUCTION — branch map deposited (instances 1,2 take the Im branch), Re-branch instances bit-identical 8/8, Im-branch delta OWNED with the branch point NAMED: PN1's threshold at rho = 0.5 — a uniform-phase medium sits ON the boundary and the rule resolves by the >= side (the one knob the rule contains, fixed a priori, not tuned); pooled complex median 0.52 <= 0.63. 0 rejections across all 393 decodes, warnings-as-errors retained, runtime 105 s. INSTRUMENT NOTE (disclosed): the grid's conjugate pairing was initially mis-seeded (class-index-seeded instead of shared-base-seeded — sign-arm outcomes differed 0/30, contradicting the pre-registered bitwise conjugacy); found at deposit review and CORRECTED before commit — the deposited run is the single registered run on the corrected instrument (battery and K4 arms were unaffected: class-index seeding does not enter them). REGISTERED NEXT: (a) the TEMPORAL read — exp142's registered (b): the flip-clock channel for time_varying/open_world media, the last named semantics carrier the projection family still discards; (b) the PN1 threshold boundary is now an experimental variable — a phase-mixed medium family with rho swept through 0.5 would map where the rule's branch switch degrades (the owned delta on uniform-phase media is the measured cost of one fixed threshold); (c) a reactive battery with the real component NOISE-carrying (class-independent noise, not constant) to test that confident blindness survives a richer decoy substrate; deposited as results/exp145_phase_read.json)

## L126 — exp147 THE NOISE-CARRYING STATE (M, 3/4 gates PASS but the headline gate M1 FAILS -> M-REFUTED — the pre-registered decisive refutation branch fired, and it is the QUANTIFIED kind): L123's registered object run as designed — the harness's OWN noise channels, bit-matched from the core harness code and NEVER tuned (pre-registered forbidden move: amplitude-raising), added to exp143's verbatim chain machinery: V-noise noise_std*sqrt(dt)*N(0,1) EVERY Euler step before the clamp overwrite (collective.py:646-647, noise_std = 0.30 the :75 default, exp124 does not override), inheritance ONE N(0, 0.6) draw per committing walk cell added to the target base and written to BOTH theta and V (graph.py:154/:161-162 on the gap_scale >= 1 branch :153 — the deterministic injection IS the mean inheritance, the noise rides on top, iid per cell), theta_drift = 0.0 (collective.py:76) so that channel is ABSENT in the harness, clips inert omitted. INSTRUMENT: batched chain (rows = organisms, op order otherwise exp143's), channels-OFF vs exp135.simulate() max|d| = 3.0e-15 at all 8 anchors, err_det(g64@36) = 4.9037 reproducing the deposited 4.904; 100 seeds per cell (PCG64 batched streams, primary branch, pilot-projected 155 s), break = err >= 6.0 (the harness's own pattern_error rule, collective.py:693-695). GATES: M1 FAIL — P(break) at g64@36 = 0.00 (0/100 seeds, mean err 4.919 +/- 0.018, ~36 sigma under the bar; 95 pct CI upper 0.03) — the harness's own noise CANNOT close the 1.096 mV margin against the deposited P(break) = 1.0; M2 PASS — P(break) = 0.00 at all 8 rescue/flank cells (g4@36, g16@48, g64@0/16/24/28/31/34); M3 PASS — P(break) >= 0.5 thresholding on exp125's onset ladders reproduces the deposited censoring-corrected curve 0/48/52/>34 monotone-rising (g1 edge 0, g4 edge 48, g16 edge 52, g64 no edge inside the censored ladder) — the stochastic chain is verdict-identical to the deposit on 7/8 anchors, ALL EXCEPT the g64@36 late control, which noise does not flip; M4 PASS — the decomposition deposited at g64@36: excess squared error over deterministic (needed 11.953 mV^2 to reach the bar) = V-only 0.007, inheritance-only 0.127, both 0.155 (interaction +0.02 ~ sampling) — the noise budget falls short by a FACTOR 89 in squared-error mass (the channels deliver ~0.06 mV RMS at read; the crossing needs ~3.46); the inheritance channel dominates the (tiny) budget, V-noise is negligible. VERDICT: M-REFUTED, decisive per the pre-registered branch — the noise-carrying state is NOT the missing carrier either. REGISTERED NEXT: the HARNESS-IMPLEMENTATION RE-READ — the deterministic mean-field chain (exp135/140/143's verified mirror) must DIVERGE from the true harness at late times by a step the mirror omits or mis-orders (candidates: the clamp theta pull, the gap_scale coupling term, wound/injection state details, step-count rounding at the g64@36 schedule), NOT noise amplitude (measured 89x short); the re-read re-derives the mirror from collective.py/graph.py step-by-step at the g64 schedule and diffs against the harness directly; deposited as results/exp147_noise_state.json)

## L127 — exp146 THE SPLICE BAR (L, 2/6, PARTIAL-REVIVAL — the L124-registered family-internal re-derivation executed; the splice clause no longer binds, first delivery since exp141): the repair run — N*_splice = the SAME 95th-pct NN rule (library_nn_stats semantics VERBATIM: same metric 100*d_struct + d_rms imported verbatim, index-based self-exclusion, symmetric storage with the pair distance computed once as dist(S[i],S[j]) for i<j) applied to the 48,564-profile splice family exp136's build_splices induces, deposited at stage bar_deposit BEFORE the search (N*_splice = 20.140 vs the old library bar 82.288, ratio 0.245; the family's OWN spread: 35,433/48,564 members sit in 2,985 duplicate classes — max class 2,098 — so P50-P70 nn = 0 exactly, P80 6.71, P90 14.38, P99 33.33: the corpus blankets the widened space BECAUSE it is internally redundant, which is why the library-calibrated bar was miscalibrated for it); EXACTNESS INSTRUMENT (disclosed): verbatim dist is 40 us/pair (all-pairs = 782 min) so an exact vectorized greedy evaluator replicates d_struct's argmin-over-all-B2/no-fallback-on-used semantics AND its float tolerance table (TOLF[i,j] = abs(j/N - i/N): adjacent lattice cuts are NOT always within CUT_TOL in float64 — abs(5/100-4/100) = 0.010000000000000002 > 0.01), verified against the verbatim metric BEFORE any selection on 4,000 index-ordered family pairs + 2,000 reverse + 6 random wide candidates x 4,000 members + 2 full-family nov_splice end-to-end + 12 random singletons' full index-rule NN: max |fast-verbatim| 2.8e-14 (d_struct counts exact, delta is RMS float noise only); search re-run bit-identical (exp141 aggregates, pool 253); REPAIRED CLAUSE (stated pre-run: clear iff NOV_lib > N*_lib AND nov_splice > N*_splice): funnel 253 -> 96 lib-novel -> 96/96 SPLICE-CLEAR (old bar cleared 0/96; best nov_splice 71.70) -> 7/10 delivered — the BINDER is now exp136's C4 pairwise filter (89/96 splice-clearing candidates sit within N*_lib of a higher-J delivery; min pairwise D of the delivered 84.23-100.61), NOT the splice clause; AUDIT at exp144's frozen 9-rung ladder VERBATIM: 7/7 delivered PASS (best-rung quads 0.06-0.225), and the SILENT-FREEBIE CHECK (part of gates L2/L3/L4 by pre-registration, the L124 star-only warning): 7/7 ALSO verify at >= 1 non-silent rung (mu > 0) — silent_only flagged 0/7; all 7 emit (1,0) by argmin frozen cost but none is silent-only, so nothing is excluded from C2/C3; DECODE+HOLD at emitted rungs: 5/7 stable 3/3 (d-2, d-6 fail at decode/hold errs 8.9-9.1 > 6.0 — decode error, not anatomy rejection; 0 rejections). GATES: L1 bar-deposit-order PASS (procedural), L2 MINIMUM REVIVAL PASS (>= 1 delivered non-silent-only audited passer — first revival since exp141), L3/C2 REFUTED (delivery 7 < 8 despite audit 7/7), L4/C3 REFUTED (5/7 < 8/10), C1 REFUTED per its own wording (7 != exactly 10), C4 REFUTED (requires 10) -> 2/6, deposited as the pre-registered PARTIAL branch (delivery 1-7) with C1's verdict per its wording and the binding stage named. REGISTERED NEXT: (a) the C4 filter's own corpus question — the pairwise diversity filter still uses the LIBRARY bar 82.288 while the widened search's J-ordered pool is elite-clustered (7 anatomy clusters at pairwise D > 82.288 absorb all 96 lib-novel candidates); the same corpus-defines-threshold symmetry (or an elite-diversity mechanism in the search) is the registered repair, BEFORE any further gate run; (b) the EMITTED-RUNG question — argmin-cost emission picks (1,0) for all 7 while audit quads at (16,0)/(32,0)/(64,0) are 4-12x smaller and the two decode failures sit at (1,0): decouple emission cost from decode stability or re-price the MU0_SILENCE cell; (c) d-2/d-6 decode channel attribution (post-settle 9.0-9.1 mV with audit quad 0.06 — the write path, not the erosion path); deposited as results/exp146_splice_bar.json)

## L128 — exp149 THE MIRROR AUDIT (O, 4/4, MIRROR-REPAIRED — L126's registered harness-implementation re-read lands the deterministic divergence, and it is an INSTRUMENTATION artifact, not physics): gates O1-O4 pre-registered in the docstring BEFORE any run; the line-level diff table (12 entries, file:line-cited, deposited to results/exp149_mirror_audit.json BEFORE the repaired runs, source-integrity-asserted against exp124/collective text) walks exp124.run_deadline's TRUE protocol (the deadline experiments' actual simulator entry: exp125 imports it verbatim) + collective.step + exp124's INLINE walk against exp135.simulate, and disposes of ALL FOUR ledger-named candidates: (D1, THE FLIP) LATCH SCOPE — harness maybe() (mu->0 at t0>=onset) is called ONLY in the window loop (exp124:95-99) and the walk sub-steps (exp124:121-126); the settle is c.run(SETTLE_H, dt) (exp124:130 -> collective.py:679-698) with NO latch check, so an onset beyond the walk-end t0 = 24 + 73*8*dt NEVER silences mu — the mirror's dyn_step latches EVERY step including settle (exp135:246-249, :295-299), so for EXACTLY the two late controls (g64@36, walk-end 34.306; g16@72, walk-end 59.040) the mirror simulates a mid-settle silencing the true harness never performs, deleting mu damage the harness keeps (exp135's docstring claim "the latch fires in the settle's final hours" is FALSE of the harness code; the deposited P(break)=1.0 at g64@36 is a FULL-MU run); (D2) inheritance content — branch (a) phi_spec[i] >= NEURAL_SPEC_MIN(-35) fires for EVERY span commit (MULTI zones all -30.0 exp94:174-177, phi_spec = target via write_spec_layer after set_target materialized phi_spec=canon), so the mirror's flat target[i] injection IS the exact branch-(a) mean: commit_base_dev measured 0.0 across all 73 commits — wound/injection-state candidate CLOSED; (D9) the walk's 8 sub-steps are HARDCODED in exp124:121 (it never calls regrow, so graph.py's round(cell_period/dt) rounding never enters) — step-rounding candidate CLOSED (g64's dt=1.2/68 moves only the walk-end in t0, feeding D1); (D10) gap_scale bit-inert at 1.0 (exp124 never blocks; coupling matrix G never rescaled) — gap_scale candidate CLOSED; (D12) clamp theta pull present verbatim both sides — clamp candidate CLOSED as a window mechanism (clamps released before amputation in both). Residuals documented: D3 init-V N(0,2) (a noise channel exp147 did NOT carry — per-step V-noise only), D4/D5 the exp147-budgeted streams (0.007/0.127 mV^2), D6 last-ulp dV float grouping a+(b-c) vs (a+b)-c, D7 clips verified inert (state bounds tracked), D8/D11 no-ops. REPAIR: the mirror REPLACED by exp124.run_deadline executed verbatim on the real GraphCollective/BioElectricCollective with exactly three stream-preserving determinism deltas (noise_std=0.0; V<-canon post-init; the commitment draw executed but its value discarded) — every harness RNG draw still fires. GATES: O1 PASS (D1 operationally real + cited); O2 PASS — repaired vs exp135.simulate max|d| = 8.3e-17 over 4 scalars x 7 non-late anchors (bit-exact for protocol purposes), live mirror g64@36 = 4.90376 reproducing the deposited 4.9037 (dev 3.9e-5); O3 PASS — repaired g64@36 err = 6.9398 >= 6.0 BREAK (latch NEVER fired, mu_at_read = 0.015) with the other 7 mandate anchors all rescue and verdict-identical, and the D1-sibling g16@72 moves 8.172 -> 8.322 STAYING break: 13/13 cells verdict-match the deposits; O4 PASS — exp140's exact hard-margin separator re-fit on repaired (x,y) separates all 8 anchors with margin 0.234 (w=[0.293,0.365], b=-4.626), 8/8 placed, and the coordinate deltas localize the divergence exactly: in-window cells move 2-4.5e-5 (float noise) while g64@36 x (th-span RMS at read) jumps 2.777 -> 5.759 (+2.98) and g16@72 6.909 -> 7.121 — the deadline arc's standing reduction (joint (x,y) threshold + late controls) CLOSES on harness-verbatim data. VERDICT: the g64@36 excess was never missing physics — the mirror was simulating a PROTOCOL THE HARNESS DOESN'T RUN (silenced settle) at exactly the two onsets past walk-end; the deadline curve 0/48/52/>34 with late-control breaks is the full-mu-settle regime, reproducible deterministically once the latch scope is verbatim. REGISTERED NEXT: (a) the mirror family's late-control scalars (exp135/140/143/147 at g64@36, g16@72) carry the D1 delta — downstream deposits quoting 4.904 at g64@36 should be re-quoted as 6.940 (repaired); in-window cells unaffected bit-wise; (b) the debt functional's fitted (kappa, tau_p) were calibrated on latched-settle trajectories — re-examine on repaired trajectories (verdicts already 13/13 unchanged); (c) exp147's M1/M4 noise decomposition was computed against the WRONG deterministic base at g64@36 — the 11.953 mV^2 "needed excess" dissolves under the repaired base (no noise needed: the deterministic full-mu run already breaks). Deposited as results/exp149_mirror_audit.json)
## L129 — exp148 THE TEMPORAL READ (Q, 3/4 gates PASS — the L125-registered flip-clock channel delivered: the projection family now carries every named semantics carrier it was registered for (magnitude exp137 -> sign exp142 -> phase exp145 -> SCHEDULE exp148), N3's fidelity bar is the one refutation and it is a NUMBER, not a blindness failure): closes exp142's registered (b) / exp145's registered (a) — time_varying/open_world media whose identity semantics live ONLY in the flip SCHEDULE, which the static time-average erases. THE RULE (one rule, zero knobs, pre-registered in-docstring before any run): TC1 the flip-clock channel — per undirected edge f_ij = the RAW presence-transition count over the read window (presence = |W_t| > 0 symmetrized; F zero-diagonal, no normalization constant); TC2 the extended projection A_ext = A + F with A = exp145's PN1/PN2 projected time-average VERBATIM (rho >= 0.5 -> Im branch else Re) — the flip clock enters as a structure feature alongside the averaged coupling, no scaling constant; TC3 exp142's execute_signed VERBATIM on A_ext (structure on |A_ext|, coupling consumes A_ext, no new executor code); analytic reduction: on static media every flip count is 0 so F = 0 and A_ext = A bitwise — the temporal read IS exp145's read wherever the medium is static. MEDIA: (a) 12 adversarial FLIP-CLOCK BATTERY pairs — static ring 1.0 + exp142's carrier geometry verbatim (K_CHORDS = 6, F1/F2/F3, PROBE_SEED = 7) where the 6 chord edges flip -b ON / 0.0 OFF over T = 2400 with every edge ON exactly c = 1200 frames; class = schedule: 'per' one contiguous bout per edge (f = 2) vs 'aper' a seeded scattered 1200-of-2400 subset (f measured 1134-1248, registered window [1120, 1280] asserted pre-decode); per-edge ON-counts identical across the pair => the time-averaged media are BIT-identical (nonzero additions in identical order, zeros exact no-ops, integer values keep every partial sum exact), rho = 0 both members; ladder b {1792, 1920, 2048, 2176} x 3 families, schedule seeds 11 + 4*family_index + dose_index fixed a priori; LADDER DISCLOSURE (pre-run): effective chords = f_e - b/2, so 'per' <= -894 — strictly past exp142's largest deposited negative-fail dose (F3@256) => predicted majority FAIL — and 'aper' in [+32, +384], inside the deposited positive-verify regime (exp142 positives verify <= 256; exp145's phase arm verifies +384 on the same executor) => predicted majority VERIFY; (b) the paired SCHEDULE-CLASS grid for fidelity (FlipGridMedium, exp137 helpers + SignedMedium draw order, shared base seeds 148_000+i so paired classes share B, w, flip subset and per-edge counts: static backbone + 6 flip edges ON c = 2 of T = 32; 'per' = bout [0,2) f = 1, 'aper' = scattered f = 3-4; time-averages BIT-identical across classes), 8 instances at n = 100 + 2 at n = 400 x 3 seeds x 2 classes. INSTRUMENT DISCLOSURES (both caught by the pre-registered pre-decode asserts, both repaired BEFORE the registered run, which is the single run on the corrected instrument): (i) the seeded aper grid draw at instance 0 produced a boundary-adjacent CONTIGUOUS pair (fc = 1 — a bout, not the registered scattered shape, outside the registered 2..4 window) — the aper draw now rejects contiguous bouts by redraw; (ii) exp142's F2 chord draw can pair ADJACENT nodes — chord (2,1) IS a ring edge, which can never be ABSENT under the backbone (f = 0, no schedule semantics on that edge, effective aper chord -895.5 outside the registered [+32, +384] window; the first run attempt ASSERTED exactly there and was DISCARDED as an invalid instrument) — chord_set now nudges colliding endpoints off the ring (+1 steps, deterministic, identical across pair members, srcs distinct so no duplicates). GATES: N1 PASS — the static reads are VERDICT-BLIND on 12/12 flip-clock pairs (>= 11 required): the magnitude, sign-Re and phase projections are BITWISE equal across the two members and all three static arms' per-seed outcome keys and majority verdicts are identical within every pair — the static time-average cannot see the schedule, confirmed not assumed; and on the schedule grid the static sign arm is outcome-identical across the paired schedule classes 30/30 (confidently blind, the exp145-K1 pattern reproduced: it decodes the schedule-free backbone and reports success while the identity is invisible). N2 PASS — the temporal arm separates 12/12 pairs at the verdict level (>= 10 required) with the ladder prediction landing EXACTLY: 'per' FAILS on all 12 (errs 13.87-20.43 mV, verify 0/3 on every pair), 'aper' VERIFIES on all 12 (errs 0.95-3.31 mV, verify 3/3 on every pair); aper err monotone DECREASING in b on all three families (F1 3.31->2.43, F2 1.21->0.99, F3 2.30->1.56). N3 REFUTED — the pooled temporal median on the paired schedule grid is 0.685 mV > the 0.60 bar (per 0.69 / aper 0.68, verify 1.00 both classes, 60 decodes): the flip-clock channel costs ~+0.12 mV over exp145's static-grid medians (0.55-0.57) — a fidelity refutation, not a schedule failure (the temporal arm still verifies 1.00 and separates the classes; the bar was inherited from exp142's H1 static bar with no flip-clock term). N4 PASS — strict superset BIT-EXACT: torus control final V bit-identical per seed (errs 0.55/0.51/0.55 on both arms, verify preserved), exp142's deposited signed class 12/12, exp145's reactive grid subset 18/18, exp142's complex_phase class 12/12 with branch map imag = [1, 2] (the rho ~= 0.5 boundary resolves by the >= side, exp145's owned branch point) — every static comparison reduces to exp145's read exactly as the analytic reduction requires. VERDICT 3/4; 0 rejections across all 498 decodes, warnings-as-errors retained, runtime 554.5 s. REGISTERED NEXT: (a) WHY the flip clock costs fidelity — TC2 adds F to the SAME matrix the executor reads structurally (|A_ext|), so a flip edge's structure weight jumps ~T/2c above its averaged carrier (16x on the grid): the registered dissection is the channel-split test — structure on |A| with coupling on A_ext vs structure on |A_ext| with coupling on A — deciding whether the temporal channel belongs in the DYNAMICS (where the schedule semantics live) rather than the anatomy; (b) re-derive the N3 bar for schedule-carrying media before any rule change (the perturbation scale is f_e vs the averaged carrier M_e*c/T, not exp142's dose ladder; the rule itself stays zero-knob); (c) map the temporal dose response with the duty cycle c as the dose axis at fixed T (f ranges 2..2T) — the schedule analog of exp142's sign ladder, with the aper monotone-decreasing-in-b err as the deposited anchor; deposited as results/exp148_temporal_read.json)

## L130 — exp150 THE GENERATOR COMPLETION (R, 5/5 CLAUSES, 4/4 C-GATES — THE GENERATOR LANDS: Stage 3's 101% test (C1-C4, >= 8/10) passed on the delivered set; the L127 binders (a)+(b) repaired by the corpus rule applied a THIRD time and binder (c) attributed; R ran workstream P's pre-registered module verbatim, docstring gates honored unchanged): pre-registration verified complete and self-consistent at spawn (R1 diversity corpus N*_pool under library_nn_stats semantics verbatim; R2 repaired C4 — greedy skip iff dist <= N*_pool to an already-delivered, everything else of exp136's delivery unchanged; R3 emission pricing — argmin rung_cost over rungs passing audit AND decode 3/3, fallbacks pre-registered; gates P1 + C1-C4 unchanged), imports resolve against the current tree (exp136/exp141/exp144/exp146 symbols all present), no code changes needed. VERIFICATION HARNESS: N*_lib re-derived 82.288 exact; fast-vs-verbatim 400 family pairs max|diff| 1.42e-14; N*_splice re-derived 20.140 = exp146 deposit; search re-run (seed 141) BIT-IDENTICAL to the exp141 deposit (all rounds, pool 253 = 253); old-rule re-delivery (C4 @ N*_lib) reproduces exp146's 7 delivered zone keys EXACTLY (same instruments, same order); d-02/d-06 (1,0) quad + decode/hold errs bit-identical (rounded) to the exp146 deposit. THE THIRD CORPUS: N*_pool = 33.776 (95th-pct NN on the 96-member splice-clear elite pool; pool NN P50 9.963 / P90 29.160 / P100 46.908 — the elite pool is ~2.5x tighter than the library's 82.288, exactly exp146's miscalibration claim); ALL THREE BARS deposited at stage bar_deposit BEFORE selection (P1 PASS). DELIVERY: repaired C4 fills 10/10 (funnel 253 pool -> 96 lib-novel -> 96 splice-clear -> 10 delivered); exp146 mapping d-01->d-01, d-02->d-03, d-03->d-05, and exp146's d-04..d-07 are NOT diversity-blocked but CAP-BLOCKED (cap_reached_first: the cap of 10 filled at J 1.4365 < their J 1.4563-1.6626 — cheaper newcomers the old library bar had let crowd the pool took the slots). GATES: C1 PASS (exactly 10 delivered, each NOV_lib > 82.288 AND nov_splice > 20.140, verbatim nov_splice recheck exact); C2 PASS 10/10 audit (quad 0.788-1.100 << 6.0); C3 PASS 8/10 decode at emitted rungs (>= 8 required — exactly at the bar); C4 PASS (min pairwise D over delivered 35.54 > N*_pool 33.776, greedy filter and gate on the SAME bar). R3 PRICING: 8/10 emitted with decode 3/3 at (1,0) (mode repriced_full), 2/10 (d-03 = exp146's d-02, and new d-08) audit_only_fallback with decode 0/3 at ALL NINE frozen rungs — R3's feasible set is empty for them so the fallback re-emits exp146's rule verbatim; no candidate repriced to a different cell ((1,0) is argmin cost 0.25 wherever feasible); silent-only flagged NONE (nonsilent 10/10), 0 rejections across all 324 decodes, warnings-as-errors retained. ATTRIBUTION (L127 (c)): d-02/d-06 fail the WRITE/READ path at (1,0) — post-settle decode_err 9.098/9.065 mV ALONE >= the 6.0 bar before any hold, erosion increments -0.170/-0.001 mV over the 100 t.u. hold (negligible); audit quad fine (0.06-class), so the failure is anatomy-level (write/read), NOT erosion and NOT pricing; NOT RESCUED (no rung of the 9 passes audit AND decode 3/3) — R3 repricing cannot save a write-path anatomy. VERDICT: P1+C1+C2+C3+C4 5/5, C-gates 4/4, target >= 8/10 met (C3 = 8/10, C2 = 10/10) — THE GENERATOR LANDS: 10 inventions delivered with explicit programs (all emitted at rung (1,0) cost 0.25, quad 0.788-1.100, decode errs 1.467-9.607, full 9-rung pricing tables deposited per candidate). R's deterministic re-run (wall 202.0 s) reproduced workstream P's interim deposit on gates/bars/cross-checks; R's run is the deposited one. REGISTERED NEXT: (a) the residual binder from 8/10 to 10/10 is the WRITE/READ anatomy at (1,0)-class rungs (d-03/d-08: decode_err ~9.1-9.6 at every rung while quad ~0.96-0.99) — register a decode-anatomy family scan (which write/read structures decode-stably at ANY rung) before any ladder change; (b) the CAP is now the binding constraint on elite coverage, not diversity: exp146's d-04..d-07 were cap-blocked at J 1.4365 — pre-register whether the corpus-defines-threshold rule extends to the cap or the 10-delivered set IS the corpus (zero-knob either way); (c) carry R3's decode-3/3 feasible-set discipline into the next generator rung-family if the rung ladder is ever re-derived (the audit_only_fallback flag must stay visible, never silently merged). Deposited as results/exp150_generator_complete.json

## L131 — exp151 THE SELF-EXPANSION PROTOCOL (S, 4/4 gates PASS — Stage 4 OPENS: the cone expands under its own read, no external controller): protocol P1-P8 pre-registered zero-knobs — substrate = exp142 carrier geometry at +64; target = spec_target_n(MULTI) scorer-only; frontier = graph-distance-1 through first-class |W|>0 edges; the read sees ONLY the induced submatrix on C∪F (beyond-frontier edges zeroed, asserted per ring); THE ONE RULE: next ring's committed value per frontier node = the read's own final V there; 6 rings, seeds (1,2,3); blockade arm = the record's gap-0.05 cell on C↔F junctions only. GATE-S1 PASS: 9/9 (family,seed) cells expand 6/6 rings under the cone's own read, ring errs 0.015-4.011 mV (bar 6.0), per-ring targeting logs (window support SHA256 digests, frontier ids, emitted-vs-plan) deposited as the sole-targeting proof; GATE-S2 PASS: same protocol instance on exp137's SignedMedium (A-NN-violating OOD class) swallows the entire 100-node support (100/100) in 2-3 rings, ring errs 0.11-0.83; GATE-S3 PASS: 9/9 cells expand 6/6 under gap-0.05 junction blockade, degradation NEGATIVE on F1 (ring 2: 1.392 intact -> 0.927 blockaded) — the reader/walk route carries the expansion, junction conductance is NOT load-bearing for targeting: M33-bypasses-junctions confirmed operationally; GATE-S4 PASS: the cone's read is the current best read — full temporal read (exp148 TC1-TC3) reduces bitwise to exp145's phase read on every F1 ring window (F=0 => A_ext identical, final V array_equal). INSTRUMENT DISCLOSURE: first S2 evaluation under-implemented the registered exhaustion disjunct; repaired to match the pre-registered text before commit, physics deterministic, ring logs unchanged. REGISTERED NEXT: (a) F3 ring-1 chord-pull channel (errs 3.85-4.01, the owned boundary — map where ball/prefix consistency breaks at deeper chords); (b) the negative-degradation delta dissection (spec/walk delivery vs coupling contamination); (c) temporal-channel expansion (time-varying frontier medium where the cone's read must carry the flip clock)


## L132 — exp153 THE DECODE-ANATOMY FAMILY SCAN (U, 3/4 gates — the simple rule is NOT established; feature table deposited, mechanism attribution registered NEXT, no ladder change): pre-registered R_U vmin gap rule (vmin_zone := min over the anatomy's zones of |voltage|; predicted decode-pass iff vmin_zone < 45.0 mV — fixed on the exp150 DEPOSIT's separating gap (40.8, 48.6) before ANY exp153 decode call; byte-offset assert docstring 1388 < RULE_VMIN constant 8982 < first decode path 18598); design: exp150 machinery verbatim (price_rung/emit_rung reused), search re-run bit-identical (pool 253), N*_lib/N*_splice/N*_pool re-derived (82.288/20.140/33.776), EXPANDED DELIVERY cap 10 -> 24 under exp150's frozen bars (first-10 zone keys == the exp150 deposit, in order). GATE-U4 PASS: original-10 full 9-rung ladders (quad, decode_errs, hold_errs), emitted rungs/modes and C3 verdicts bit-exact (rounded) vs the exp150 deposit. GATE-U3 PASS. GATE-U2 PASS: the generator-side filter (predicted-pass only, everything else frozen, cap 10) delivers exactly 10 with C3 9/10 under exp150's C3 semantics (unfiltered 8/10) — actionable, but the rule behind it is not. GATE-U1 REFUTED: expanded-cohort accuracy 20/24 = 0.833 < 0.90 (new-only 10/14 = 0.714; confusion tp=18 fp=4 fn=0 tn=2) — vmin >= 45 remains a perfect FAIL predictor (2/2: d-03 48.6, d-08 50.8) but the converse breaks: 4 expanded members with shallow anchors fail decode at every rung (d-12 vmin 42.0 derr 9.96, d-19 28.6/8.05, d-22 16.4/9.07 — cross-checked as exp146's d-06, failing exactly as that deposit says — and d-24 16.4/9.72). MECHANISM READING: decode failure is anatomy-STRUCTURAL (a deep multi-zone backbone, e.g. the (0.16,0.327)+(0.831,0.878)-deep pair, pins the write/read path at ~8-10 mV even when a shallow anchor zone is appended), not a single-scalar depth threshold. 8-FEATURE TABLE deposited (per-feature pass/fail ranges + AUC vs decode verdict on n=24: vmean_zone best at 0.907 but ranges overlap; vmin_zone 0.644; vmax_zone 0.778; zone_count/total_width/boundary_count 0.59-0.65; nov_lib 0.546 and nov_splice 0.667 — diversity distance does NOT track decode failure). REGISTERED NEXT: (a) mechanism-level dissection of the write path (write_spec_layer + clamp-release settle) on the 6-member failing class — why decode_err pins at ~8-10 mV at ALL 9 rungs while quad stays ~0.96-1.6; (b) a STRUCTURAL rule candidate (deep-backbone detector over zone pairs) to be pre-registered fresh on new data, never tuned on this deposit; (c) NO ladder change until the mechanism is named (L130 discipline). Deposited as results/exp153_decode_anatomy.json

## L133 — exp154 THE DEADLINE LAW, FORMALIZED (workstream V; 4/4 core gates PASS + one owned strict-diagnostic FAIL + one upstream bug FOUND — L128's three registered re-quotes executed on exp149's repaired base in one instrument): FIDELITY first — exp149's repaired run_deadline carried verbatim with ONE marked addition (a step-recording wrapper appending exp135's chain-mismatch scalar m(s) after every walk sub-step and settle step; the settle itself stays c.run(SETTLE_H) verbatim through the shadowed step, latch scope D1 untouched) reproduces exp149's DEPOSITED (err, err_span, err_intact, th_span_dev, x, y) at all 13 overlapping cells to max|d| = 0.0 exactly, and the full 28-cell torus battery matches exp125's deposited verdicts 28/28. GATE-V1 (kappa re-fit, deposited either way): exp135's protocol verbatim (debt on the repaired m-trajectories, fit_interval, n_region = 73) over exp135's 8 primary taus PLUS a 16-value refinement grid — the kappa interval is EMPTY at every primary tau on the repaired trajectories; a 0.87%-wide corner survives ONLY at the off-grid tau_p = 1.0 h (kappa in (2.3341, 2.3545), binding g16@72-break vs g64@24-rescue), the near-Markovian extreme whose tau->0 limit is exp134's already-refuted per-step exposure class — NOT a revival; and the emptiness is STRUCTURAL, not marginal: at every tau >= 1.5 the SAME binding pair (g16@72 break-binding, g64@24 rescue-binding) orders the kernel debts wrong by 1.19-1.31x — no (kappa, tau_p) in the scalar family can place g16@72's debt above g64@24's on corrected data. VERDICT: the state-space curve law STANDS ALONE; the scalar family stays closed (pre-registered either-way deposit honored). GATE-V2 (exp147's base correction): the ledger's 89x factor is RECOMPUTED and CONFIRMED against the mirror base — needed excess 11.9533 mV^2 (36 - 4.903739^2) vs exp147's measured channel capacities (V 0.0074 + inheritance 0.1277 = 0.1351 mV^2) = 89.0x exactly, so exp147's arithmetic was right ABOUT the wrong base; on the REPAIRED base the needed excess is ZERO — err(g64@36) = 6.9398 >= 6.0 is a deterministic FULL-MU crossing carrying 12.1608 mV^2 of SURPLUS above the bar, and the harness's own channels (0.155 mV^2) are 78.7x too small to UN-BREAK it and >= 10x too small to flip any rescue anchor (binding rescue headroom g16@48: needs 1.564 mV^2 to break, capacity 0.155) — the noise question is CLOSED in BOTH directions: the g64@36 crossing is explained deterministically (the settle never checks the mu-latch), noise is a spectator. GATE-V3 (the formal law): THE DEADLINE LAW deposited as a half-plane in the (span-theta-dev, intact-V-dev) plane — break iff 0.2930*x + 0.3650*y - 4.6258 > 0 (exact 2D hard-margin on the 8 repaired anchors, margin 0.2340 mV, |w| = 0.4669, anchor coordinates + scores deposited), places 8/8; leave-one-out over the 6 bracket cells: 6/6 feasible + BOTH-POSITIVE with margins 0.234-0.647 (>= 0.2 bar) — stability under anchor loss holds on the registered criterion; the STRICTER held-out-placement diagnostic FAILS 3/6 (owned, reported not gated): g4@48 and g16@48 are HINGE cells — the refit without g4@48 places it rescue-side, the refit without g16@48 places it break-side (mutual nearest neighbors straddling the boundary) — the 8-anchor law itself is untouched (8/8 anchors, 28/28 torus battery, transfer clean). BUG FOUND (upstream, exp140's shared feasibility machinery; addendum written between run 1 and the depositing re-run, both disclosed): e140.point_in_hull's 2-vertex branch (_on_seg) tests BOUNDING-BOX containment with NO collinearity check, so a collinear 2-point break hull spuriously "intersects" any rescue point inside its bbox — demonstration: LOO g16_t52's rescue g16@48 sits 0.60 mV off the g1@0-g4@48 segment yet inside its bbox, making e140.max_margin return a spurious INFEASIBLE; exp154 carries max_margin_fixed (collinearity AND on-segment required; the only change — closest-pair margin untouched); the 8-anchor fit is non-degenerate and unaffected (run 1 already reproduced exp149's w/b to machine precision); run 1's other two defects owned: the torus predicted-edge parser (matched e140's "g_t" names against exp154's "g@t" names — edges all None) and the transfer closest-to-break margin semantics (min instead of max score), both fixed for the deposit. GATE-V4 (domain + kernel-free transfer): the FROZEN law places every deposited grid2d/path cell (exp140's F4 filter verbatim) on the RESCUE side on REPAIRED states — 0 false breaks on grid2d (26 cells, closest-to-break margin -3.284 at g1_t24) and 0 on path (26 cells, -7.649 at g1_t24); the torus curve places 28/28 with predicted edges 0/48/52/>34 == deposit; the DOMAIN statement is deposited (torus deadline protocol, window + amputation + 8-sub-step walk + UNLATCHED settle, GAMMAS 1/4/16/64 on the exp112 torus battery, MULTI target, exp125's censoring-corrected ladders + both late controls, under exp149's three stream-preserving determinism deltas; kernel-free transfer claimed ONLY as non-contradiction on flat-zero substrates; OUT OF SCOPE: SignedMedium/A-NN-violating OOD, splice and blockade arms, non-MULTI targets, substrates outside exp112) alongside falsification conditions F-1..F-4 (one disagreeing new torus cell; loss of feasibility/both-positivity on refit = scalar collapse; tau-refit instability demotes the corollary only; one transfer false break). VERDICT: LAW-FORMALIZED — the deadline law is the half-plane 0.2930*x + 0.3650*y - 4.6258 > 0 on the repaired base, 4/4 core gates, wall 4.2 s. REGISTERED NEXT: (a) the hinge-cell finding points at the law's testable edge — a pre-registered fresh-anchor battery bracketing the g4/g16 edges (g4 in 44-52, g16 in 50-54 at fine onsets) is the direct F-1 test and would also stress the hinge geometry; (b) exp140's point_in_hull len==2 branch should be patched upstream with its own fidelity re-check (exp140's deposited gates used non-degenerate hulls except wherever 2-point hulls entered — the spurious-infeasible direction is safe-side for F1/F3 but the machinery should be repaired, not trusted); (c) the tau_p = 1.0 corner sliver is a falsifiable prediction of the scalar family's ghost: any fresh onset battery that keeps g64@24's debt above g16@72's at tau 1.0 kills the corner too, closing the family with no survivors. Deposited as results/exp154_law_formal.json

## L134 — exp152 THE TEMPORAL FRONTIER (T, 4/4 gates PASS — the cone expands under its own read ON FLIP-CLOCK MEDIA and the schedule semantics propagate into committed structure): protocol = exp151's P1-P8 with P5's window generalized to the temporal window (every frame of the member medium restricted to the induced subgraph on C u F, closed-world n x n, beyond-frontier zeroed, asserted) and the cone's read = exp148's TC1-TC3 VERBATIM on the window (A_ext = A + F); medium = exp148's FlipPairMedium adversarial pair VERBATIM at b=1792 (LADDER[0], chosen a priori), family F2_zone_head — the battery family whose chords are C u F-relevant (instrument-asserted: all 6 chord edges have BOTH endpoints in the seed set, so the flip edges sit inside every ring window; pair time-averages bitwise equal to the analytic W_avg and to each other; T_plan continuous with the carrier deposit); emission rule UNCHANGED (next ring's committed value = the read's own final V at the frontier); the committed SET sequence is support-driven hence pair-identical — only committed VALUES can differ across the pair. GATE-T1 PASS: 6/6 (member,seed) cells (per AND aper x seeds 1-3) expand 6/6 rings on the temporal medium, ring errs 0.017-0.775 mV (bar 6.0); GATE-T2 PASS: 3/3 seeds commit DIFFERENT morphologies on the time-average-identical pair — committed max-abs deltas 0.523/1.681/1.411 mV (pre-registered bar 0.05 = 3x exp151's min ring err), per-ring emitted separation from ring 1 (0.046-1.681 mV), channel localization deposited: the projection channel is BITWISE INERT across the pair (asserted every ring — integer-exact frame means) so separation enters ONLY through the flip-clock channel (fc cross-delta max 1226; per fc_max 2 vs aper 1228); GATE-T3 PASS (primary form, the confirming negative): the static phase read on the SAME windows has bitwise pair-identical projections -> ONE deterministic cone -> committed deltas exactly 0.0 on 3/3 seeds while the temporal deltas are 10-30x the bar; GATE-T4 PASS: the temporal-frontier protocol on STATIC carrier media reproduces exp151's deposited S1 committed structure EXACTLY (per-ring window sha256_16, frontier ids, emitted, plan, ring_err_mV, program_verified, run-level rings_expanded/final_coverage — 0 mismatches across 3 families x 3 seeds x 6 rings) with the per-ring reduction chain asserted bitwise (A == window M, F == 0, A_ext == M). Full-organism anchors reproduce exp148's pair separation (per fails 14.94/13.87/20.43 mV, aper verifies 1.22/3.31/2.31 mV, all rho=0 real branch). HORIZON FALSIFICATION (deposited; the pre-registered expectation "F1/F3 windows flip-free" is FALSE — measured, not assumed): the cone's frontier walks THROUGH the flip edges (chord partners of committed nodes are frontier by P4), so flip edges are in-window from ring 1-2 in EVERY family (F1: chord 5 enters at ring 2, then 2, then 0/2/4/5; F3: 4/6 chords in the seed set, all 6 from ring 1) — and on those JUNCTION-FLIP geometries (flip edge C<->F) the temporal cone breaks exactly at the flip-entry ring on the per member (F1 ring-2 err 23.1 mV; F3 ring-1 err 36.9-46.5 mV; aper survives F1 5/6 rings at 0.1-3.1 but fails F3 ring 1 at 7.1-7.3 mV), tracking the full-organism per-fail/aper-verify anchors. REGISTERED NEXT: (a) junction-flip frontier discipline — the C<->F flip-coupled frontier node is dragged by the -b/2 time-average coupling at the flip-entry ring; repair = pre-registered window or frontier rule that holds the junction node (which one is the open question); (b) F2's C-interior-flip geometry is the deposited operating point for temporal self-expansion (flips inside C, frontier flip-free) — the T2 propagation result is scoped to it; (c) committed-value feedback (exp151/exp152 commit values log-only; feeding committed V back as substrate is the untested stronger claim). INSTRUMENT DISCLOSURE: first gate evaluation under-materialized T3's primary form in one evaluation-only way (the single deterministic control cone was not attributed to the second member -> None deltas); repaired to match the pre-registered text before commit, physics deterministic, ring logs unchanged. Deposited as results/exp152_temporal_frontier.json

## L135 — exp161 THE UNIVERSAL SUBSTRATE TEST (D, 4/4 gates PASS — Stage 5 path 2 OPENS: the ~5% untested branch lands — ONE substrate chosen ONCE carries a diverse 10-target battery at the 6.0 mV bar, beating the per-target-priced default at the WORST CASE, which is the pre-registered point: universality is a worst-case property): THE CLAIM under test — there exists a single fixed substrate configuration S* (one wiring + one operating point, chosen ONCE) such that the compiler writes >= 10 DIVERSE targets onto it at the 6.0 mV bar, vs the current compiler which prices substrate-pattern pairs per target (exp144's nine-rung audit + exp150's R3 emission pricing). SUBSTRATE SCOPED to the machinery's home axis: S = (adjacency, gamma, mu) with the wiring FIXED to A_CHAIN = path(100) (exp136's declared honest scope) and the operating point ranging over exp144's frozen EXTENDED_LADDER (9 rungs); DEFAULT substrate = (1.0, 0.015), the DEFAULT0 pole cell. THE BATTERY (pre-registered, frozen before selection): 10 morphologies spanning zone counts {1,2,3,4} (3/3/2/2) and the voltage bands -16..-35 mV (shallow/deep mixes, ascending and descending 4-zone ladders), every member well_formed, all 45 pairwise exp136 dist() distances > 0 (min pairwise 55.103 — 1.6x the exp150 corpus bar N*_pool 33.776, deposited as context NOT gated). SELECTION RULE stated before evaluation (the maximin substrate): for every rung S and target t a seed-1 PROBE margin m1 = 6.0 - max(quad1, dec1, hold1) (one erosion seed, one decode seed — deliberately a cheaper instrument than the verdict); S* = argmax_S min_t m1, ties -> lower frozen rung_cost; only then are any 3-seed verdicts issued. VERDICT INSTRUMENT = exp150's price_rung VERBATIM (quad < 6.0 at seeds 1-3 AND decode 3/3 with decode_err AND hold_err < 6.0); the FULL 9x10 3-seed matrix priced and deposited as the universality boundary. GATE-S1 PASS 10/10 writable on S* (bar was >= 8/10 — the generator's own C3 bar): S* = (64.0, 0.0), the walk-speed fast arm (exp136 audit ladder + exp112), worst probe +5.391, NO ties; worst-case 3-seed margin +5.391 mV, mean +5.531. GATE-S2 PASS: no per-target substrate adjustment — the substrate LOCK (in-module) refuses any write whose rung/wiring drifts from the fixed selection; 20 writes logged (10 on S*, then 10 on the default rung), constant-per-phase TRUE, wiring object identity asserted on every write, and the locked writes reproduce the sweep's S* row exactly at price_rung's own 3-decimal deposit precision (determinism harness). GATE-S3 PASS: the seed-1 probe margin predicts the 3-seed pass/fail pattern 10/10 (>= 9/10 required) — the maximin margin computed on ONE seed is a genuine cross-seed predictor of the full verdict (prediction is non-trivial because probe and verdict instruments deliberately differ). GATE-S4 PASS (the contrast): the same 10 targets on DEFAULT (1.0, 0.015) score worse AT THE WORST CASE — worst-case margin -0.004 vs +5.391, 9/10 writable (u-10, the descending 4-zone ladder, fails at the bar on default: m3 -0.004) while S* carries it with +5.391 — means (+1.891 vs +5.531) deposited for the record but the gate is worst-case by pre-registration. THE WORST-CASE LADDER is monotone in gamma on the mu=0 arm: (1,0) +1.841 < (4,0) +3.744 < (16,0) +5.071 < (32,0) +5.374 < (64,0) +5.391 — every mu=0.015 arm is degraded (worst-case +0.58 to +1.19), the theta channel's cost is worst-case-real even where the mean hides it; the two mu=0 arms with gamma>=16 clear the whole battery with margin >= 5.07. NO S1 BOUNDARY to deposit (10/10), but the full matrix IS the boundary map: no rung fails any target except default's u-10 — on THIS battery the substrate-per-target pricing of exp144/exp150 buys nothing over the one-time maximin choice (the per-target machinery's value must lie outside this battery's domain, e.g. exp150's d-03/d-08 anatomy-level decode failures, which no rung rescues — L130). INSTRUMENT DISCLOSURE (pre-commit, exp152/exp151-style): the first gate evaluation failed S2 in an evaluation-only way — the determinism clause compared a margin derived from price_rung's 3-decimal-ROUNDED channel values against the sweep row's RAW-valued margin at 1e-9, testing the rounding, not the physics; repaired to channel-wise comparison at price_rung's own deposit precision before commit; writable booleans and channel data were already in exact agreement, physics deterministic, the re-run is the deposited one (wall 61.8 s, identical gates/numbers both runs). REGISTERED NEXT: (a) WIRING as the second substrate axis — S* here fixes A_CHAIN; the universal-substrate claim over wirings (one graph carrying the battery) is the untested extension, with the exp137-named input contract as the probe surface; (b) CROSS-BATTERY S* — is the maximin substrate battery-INVARIANT (the monotone-in-gamma ladder predicts (64,0) or (32,0) for any pole-domain battery; a fresh pre-registered battery would test whether one S* serves ALL batteries, the strong form); (c) the per-target compiler's residual value — locate the target class where emit_rung beats the fixed maximin rung (predicted: deep-backbone decode-anatomy failures where NO rung passes — pricing cannot rescue what no substrate carries). Deposited as results/exp161_universal_substrate.json

## L136 — exp158 THE OCTANOL-DH PLANE SERIES, RE-TESTED ON ITS DEPOSITED ARM (A2; 2/4 gates PASS: O1 FAIL-DEGENERATE, O2 PASS, O3 PASS, O4 PARTIAL — the L116-registered repair of LV-G4's DEGENERATE B leg): the B family (GJ-blocked, 57 entries, the frozen exp139 partition reproduced exactly) re-mapped onto the DEPOSITED posterior-depol arm (exp39-V3 VERBATIM — corrupt_region(POST_Q, theta_value=WT_HEAD_V) BEFORE the 24 h run, V3's own regrow kwargs, NOT the ion arm's commitment extras) with the plane-resolved instrument that landed the C leg at rho 0.6489 (exp131 geometry + exp139 flags + exp139's deposited taxonomy), the mapping declared in the docstring's MAPPING DECLARATION + module constants BEFORE any rho computation and asserted in-module (O2 PASS, _RHO_CALLS==0 at assert time); O1 FAIL-DEGENERATE under the pre-registered zero-variance clause (exp131's deposited IP-G1 zones, bar 0.6): the depol channel flips the B leg's EA read from the junction-cut arm's 0/0/0 (floor-degenerate, L116) to 1/1/1 at EVERY plane (per-seed hl 1.0/1.0/1.0 at head and trunk; 0.9763/0.9309/0.9316 at tail — BIT-EXACT the deposit's exp39-V3 D-family values, so the tail-plane run IS the deposited arm) — rho None; THE SHARPENED FINDING: the stack's DH prediction is a step function of the CHANNEL (off -> on) with ZERO plane resolution, while the record's octanol DH series is plane-GRADED (eids 415-419: .05/.28/.50/1.00/.00) with its floor at the tail plane, which the deposited taxonomy folds onto the SAME stack tail plane as the post-pharyngeal 1.00 peak — the record's post-pharyngeal cell is the one the stack's ceiling hits, the head/pre-pharyngeal cells are over-predicted; O3 PASS — the C leg re-run through the deposited exp139 ion_arm function object reproduces the deposit BIT-EXACTLY (sim_c_abn_by_pub_order float-equal and rho 0.6488856845230502) — the repaired B leg (own arm instances) breaks nothing it touched; O4 PARTIAL (the pooling question, LV-G1's failed gate re-run under the repaired instrument, gated plane-resolved at LV-G1's own bar): pooled companion — the 4-family E_stack with B's scalar depol-mapped (tail EA, structurally TIED to D's scalar, same deposited arm, disclosed) — rho -0.2582 vs the deposit's LV-G1 -0.1054, still inside the honesty zone; plane-resolved pool — the 10 record-plane cells (B: 5 DH planes via depol EA, ceiling-tied; C: 5 headless planes via ion abn) — rho 0.3716: plane-resolution moves the cross-family concordance +0.63 and pooling still erases structure (True), but 0.3716 sits just under LV-G1's 0.4 bar (owned — the ceiling-tied B cells carry no within-family rank information to pool); VERDICT: the octanol DH sign is REAL on the deposited arm as an EXISTENCE claim (the channel fires the phenotype at maximal strength everywhere) but the plane structure stays unmatched at the C-leg bar — the B leg's homelessness narrows from "no arm carries the sign" to "the arm carries the sign plane-flat"; REGISTERED NEXT: a plane-resolved depol instrument — the stack's EA read must become a function of the CUT PLANE (e.g. wound-local head-likeness at the amputation site rather than the tail-anchored read) before the octanol family can be claimed predicted, and the taxonomy needs a post-pharyngeal-vs-tail resolution the 3-plane instrument does not have. Deposited as results/exp158_octanol_plane.json

## L137 — exp162 THE ZERO-SUBSTRATE PROBE (the blocked path, one new mechanism; Z-gates 2/3 scored with the pre-registered FAILURE verdict — the coherence constraint's 6th formalization CONFIRMED at the temporal level: the temporal-coherence escape route is CLOSED at this probe's scope): the exp68 blocker (L49: the floating-pattern star blocked by the DYNAMICS, robust across 5 formalizations — b2v/label-energy/mean-force/lambda2/conductance, all separating, CF-G3) re-attacked with the ONE mechanism the deadline arc makes available — TEMPORAL COHERENCE WITHOUT SPATIAL SUPPORT: the pattern carried in the TIMING of interventions (L133's lesson: WHEN mu fires matters as much as WHERE V is), on a MEMORYLESS medium (every node's V AND theta reset BIT-EXACTLY to ground before every intervention round incl. round 0; nothing persists but the schedule). Pre-registration deposited in the module docstring BEFORE the run, zero new knobs — every constant inherited: medium = exp68's torus(10,10) verbatim; target = exp43's fixed labeling (first 25 at -20.0, rest ground -50.0; b2v 0.110, the deposited refused star; all 5 static separator values re-deposited: b2v 0.110, E 19800, lam2 0.382, cond 0.220); the schedule = exp124's deadline protocol transplanted to the write — per round of 48 t.u. (WINDOW 24 = exp124's WINDOW_H with the head zone clamped at -20 — the minimal spatial content: the write intervenes ONLY where the target leaves ground; then the TAIL 24 with the clamp released, the regime where exp124's late latches acted) + the mu-latch (mu 0.015 until t_s, then 0.0, exp124's maybe() semantics); THE schedule a priori t_s = 24 (the WINDOW/TAIL boundary); the battery = ALL 7 deposited onsets in [0,48] {0,6,12,18,24,36,48}; the read = one 24-t.u. free window (exp68's settle duration, exp68's own bar 6.0 and mean-over-seeds statistic), seeds 1-3, noise_std 0 (exp149's stream-preserving determinism delta — the bit-exact gates are exact); the shuffle pool = 5 fixed-seed latch onsets U[0,48] {24.6, 12.6, 4.1, 45.3, 38.6} at identical clamp content. Z3 RESET HONESTY PASS (prerequisite): 0 reset violations across every reset in every run (V and theta array_equal to ground each time) and ROUND-INDEPENDENCE BIT-EXACT — the R=3 run's V, theta at read-start and its full read trajectory equal the R=1 run's to max|d| = 0.0 exactly (the direct proof that nothing persists but the schedule; makes R provably not a knob); instrument anchor: exp68's sim_supports protocol verbatim reproduces the deposited torus|fixed 8.47 to delta +0.00. Z1 PERSISTENCE FAIL: THE schedule's mean read-end err 9.806 (bar 6.0) and EVERY battery member fails — nearest miss t_s=0 (mu never fires) at 9.449, still 3.45 mV above the bar; the read trajectories ERODE monotonically through the window (best cell 8.80 -> 9.45): the schedule writes a PARTIAL pattern and nothing carries it. The err-vs-onset curve is MONOTONE (9.449/9.485/9.569/9.681/9.806/10.079/10.351 across the 7 onsets) — the temporal lever has the RIGHT SIGN (mu's only role in this write problem is theta-erosion; the earlier the latch the better the write) but nowhere near the range the bar needs. Z2 TIMING LOAD-BEARING: PASS-as-scored (no shuffle writes) with the pre-registered consistency note — with Z1 failed the control is moot; the informative observation deposited: the 5 shuffle errs (9.466/9.579/9.819/10.138/10.290 at onsets 4.1/12.6/24.6/38.6/45.3) interpolate the battery's onset curve smoothly — a real, smooth temporal structure exists but reaches persistence at NO deposited timing. CARRIER DISSECTION (bounded, per cell): at the best cell theta deviates from ground at read-end (RMSE 14.87 mV, max 26.84, zone-A mean -24.43 vs target -20.0 — the clamp's eps channel DID install a partial theta memory) and the pattern STILL fails the bar — the strongest honest form of the confirmation: even the created-support route (a schedule-carved partial theta trace) erodes past 6.0 on the refused labeling; mu_at_read = 0.0 in every cell (uniform read conditions). VERDICT (pre-registered both ways; writer census 0/12 timing cells): FAILURE — the coherence constraint's 6th formalization CONFIRMED at the temporal level; the class deposited: the TEMPORAL-SCHEDULE class — the deadline law's own mu-latch family transplanted from the break/rescue question to the write/persist question, swept over its ENTIRE deposited onset space at fixed minimal clamp content on a bit-exact-reset memoryless medium — AGREES with the five static formalizations: the refused labeling is unwritable-persistently at every deposited timing; the deadline asymmetry (which decides break-vs-rescue of an EXISTING write) does not transfer into write-vs-erode of a floating one. SCOPE + falsification conditions (deposited): one medium (the canonical blocked torus), one content (the minimal clamp), the deposited timing space, deterministic reads; F-1: any writer cell on an in-scope re-run reopens the path; F-2: a non-deposited timing class (mu PULSES above full-mu, repeated clamp windows) is OUT OF SCOPE and is the registered next candidate, not a refutation of this deposit. REGISTERED NEXT: (a) the mu-pulse class (transient mu elevation above 0.015 during the window — the one temporal lever this probe did NOT sweep, out of scope by the zero-knob rule since no deposited constant sets a pulse level); (b) the multi-round coupling question is CLOSED by the round-independence assert — any schedule on a reset medium reduces to its last round; that assert is the honest instrument for ANY future temporal-schedule claim on memoryless media; (c) the created-support trace (zone-A theta mean -24.43 from a 24-t.u. clamp) is the quantitative seed of the ordinary spatial write — the star's next opening must be a mechanism that CREATES support faster than the dynamics erodes it (the substrate-side mirror of exp161's maximin result), not a schedule that times it. Deposited as results/exp162_zero_substrate.json

## L138 — exp160 THE UNIVERSAL READER AT ANY MEDIUM (U, 4/4 gates PASS — the L134-registered "any medium" cell closes for the RANDOM-UNION battery: the current best read (sign+phase+flip-clock, exp148's A_ext = A + F, exp142 executor verbatim) consumes 200 RANDOM media drawn over the semantics union space with ZERO rejections, ZERO re-tuning, and curated-OOD quality; the tail is LIGHT (2.5%) and hyper-owned — universality's boundary is not crossed at the bar, and its leading edge is named): PRE-REGISTRATION deposited before any decode (commit ce3cddf): generator master seed GEN_SEED = 160160 frozen, instance i draws default_rng(GEN_SEED+i) at n=100 on exp137's _base_connected support with magnitudes in exp137's _wU operating range U(0.5,1.5); FIVE semantics dimensions each independently active with p=0.5 — oriented (A-SYM, per-edge one-way prob 0.5), signed (A-NN, instance p_neg ~ U(0.1,0.5), sign symmetric per undirected edge), complex (A-REAL, per-edge phase with instance fraction U(0.2,1.0)), hyper (A-PAIR, 1-20 added hyperedges size 3-6 through exp137's phase-carrying factorization w_e/(|e|-1)), temporal (A-STAT, T=8 frames, per-edge presence p_keep ~ U(0.6,0.95), ring backbone always on) — so every instance is a random MIX of violated M33 assumptions, not a curated class; read = exp148 read_temporal VERBATIM (PN1/PN2 dominant-quadrature + TC1 flip-clock F + TC2 A_ext = A + F -> exp142 execute_signed VERBATIM) x seeds (1,2,3) = exp137's seed protocol, config fingerprint 8e11e88c1c2f1518 asserted identical across all 600 decode records and unchanged post-run. GATE-U1 PASS: 0 rejections / 600 decodes (no exception, no coercion warning, every err finite) and verify_rate 1.00 — every one of the 600 decodes is program_verified inside the 6.0 mV bar, stronger than the gate required. GATE-U2 PASS: pooled median decode err 0.630 mV vs the pre-registered bar 1.30 = 2.0x exp137's DEPOSITED OOD median 0.65 (ratio 0.97 vs anchor — the random battery decodes AT curated-OOD quality; p90 1.021, max 1.680 = exp137's signed-class max). GATE-U3 PASS: tail 5/200 = 2.5% above the 1.30 bar — the HEAVY-TAIL CLAUSE (threshold 0.10) IS NOT TRIGGERED: the universality boundary is not crossed at the bar on random media; the deposited decomposition localizes the tail's leading edge: all 5 above-bar instances (medians 1.31-1.65 mV, all still verifying) sit in the oriented+hyper+temporal corner (subsets A-SYM+A-PAIR+A-STAT and supersets), dominant driver = hyper at dimension level (5/90 hyper-active above vs 0/110 hyper-inactive; lift undefined at 0 denominator, deposited as None), signed/complex neutral-to-protective (lift 0.74/0.67), so the A-PAIR pairwise factorization meeting one-way orientation under flipping presence is the NAMED tail corner — flagged as the boundary's leading edge, no repair registered under the pre-registered clause. GATE-U4 PASS: one configuration end-to-end (fingerprint constant per decode and pre/post run; audit asserts read_temporal IS exp148's, its executor IS exp142's execute_signed, spec IS exp94's MULTI; the generator branches on instance draws, the reader branches on no instance property). INSTRUMENT DISCLOSURE (pre-credit, full): run 1 produced 264/600 rejections — 100% instrument-induced by a transposed index in the GENERATOR's hyperedge presence schedule (hyper_on[k,t] -> [t,k]), every rejection an IndexError inside a hyper-present subset with n_hyper >= 2 and none anywhere else (repair + localization committed as 7d2bba0 BEFORE the credited re-run); gates and protocol untouched; the deposit is run 2. RACE NOTES (concurrent agents on the shared index): exp160's pre-registration commit briefly swept two staged exp161 files (split restored; exp161's own L135 RACE NOTE discloses the same incident), and exp160's 6-line instrument repair was folded into the exp161 commit by an amend race — content intact, attribution disclosed here. Wall 61.4 s. FOLLOW-UPS registered: n=400 scale spot-checks on the random battery (wall budget; exp137's grid had them), and a heavy-sampling battery bracketing the hyper x oriented x temporal corner if the leading edge is to be priced. Deposited as results/exp160_any_medium.json

## L139 — exp156 THE WRITE-PATH DISSECTION (B2, 4/4 — the ~9 mV decode floor is NAMED and REMOVED): the failing class's decode floor is the S-REL canon-fallback IDENTITY OVERWRITE of unreadable deep-zone writes — stage B (clamp-release residual) carries 0.966-0.991 of decode_err^2 on all six fails; the mechanism-derived CF-1 repair (spec-floor -35 -> -60 mV) REMOVES the floor (6/6 below bar); the structural R_W canon-clash rule (bar 36.0 mV^2, inside a clean gap: pass mass <= 23.5, fail mass >= 65.3) predicts the cohort 6/6 fails 0 FP — replacing exp153's scalar vmin bar (which hit 2/6) and the naive deep-pair detector (6/6 but 9 FP); instruments bit-exact vs the exp150/153 deposits at all 24 emitted rungs (zero rng draws in the dissect replica); W4 instrument check PASS. REGISTERED NEXT: CF-1 adoption into the compiler's emitted-cell contract (with the exp150 decode-3/3 feasible-set rule), the R_W rule as C3's structural gate, mechanism-level re-run of the generator's C3 at the CF-1-repaired floor
- GATE-W1 PASS: stage attribution — clamp-release residual >= 0.966 of decode_err^2 on every failing anatomy (write commitment and read reconstruction minor)
- GATE-W2 PASS (W2a+W2b): clash localized to the canon-fallback identity overwrite at deep zones; CF-1 (spec-floor widened to the identity repertoire) removes the floor 6/6
- GATE-W3 PASS: R_W rule 6/6 fails, 0 FP; contrast detectors land 2/6 and 6/6+9FP — the structural rule is strictly better
- GATE-W4 PASS: deposited decode errs reproduced bit-exactly on the original 10

## L140 — exp155 THE JUNCTION-FLIP FRONTIER DISCIPLINE (B1, 3/4 — partial repair, causal deposit): frontier discipline = flip-quiet membership freezing at emission; the junction-flip geometry that broke exp152's per cone at flip-entry (23.1/46.5 mV) is repaired on 9/12 cells (J1 FAIL as registered: 6/6 F1_zone_tail + 3/6 F3_canon_boundary pass; the canon-boundary class keeps 3 breaking rings) — the discipline is REAL but NOT sufficient at canon boundaries; J2 PASS bit-exact superset (0 mismatches; F3 rings 2-6 bit-exact vs deposit); J3 PASS causal confirming negative (removing discipline re-breaks the same rings — F1 12/12 break-rings still break, F3 6/6 match); J4 PASS OOD chord-placement survival. REGISTERED NEXT: the canon-boundary residual (3 cells) — flip-quiet freezing at canon boundaries may require the exp158-class plane-resolved readout rather than membership discipline
- GATE-J1 FAIL: 9/12 (the three F3 canon-boundary residuals sit at flip-entry rings where the frozen frontier cannot exclude the junction without excluding the boundary itself)
- GATE-J2 PASS: non-junction batteries bit-exact (f2 vacuity structural)
- GATE-J3 PASS: causality — discipline removal re-breaks the same cells (33/36 records compared)
- GATE-J4 PASS: OOD class survives with discipline engaged

## L141 — exp157 THE GHK IMMUNE-WEIGHT RECALIBRATION (A, 4/4 — exp139's single LV-G2 FAIL is REPAIRED with zero regression): the owned gap (L116 sub-gate d — the GHK 7-type map's phagocyte/immune arm at -7.13 mV, outside the BETSE band [-80,-10]) is a cation-leak overshoot, not an ion-conditions or band problem — the curated MARKER_TABLE scored the immune cell's WOUND-ACTIVATED state (P2X 0.8 / TRP 0.6 / Nav 0.3 fully open) as if it were rest (deposit PNa/PK = 0.91 vs <= 0.28 for the six in-band types); the TISSUE-vs-CELL-SCALE BAND STATEMENT is deposited first (the L116 repair clause): [-80,-10] is a RESTING tissue-scale band — the band gate applies to rest states only, and the activated complement (the wound-ATP transient the depolarization family rides) is not required to sit inside it; THE ONE WEIGHTING SCHEME stated before running: rest-open-probability weighting of the gated cation classes only (p2x 0.10, trp 0.25, nav 0.05, fana_nav 0.05, hvcn 0.10; K-side/pumps/Cl at 1.0 — unstimulated phagocytes are K+-dominant, Kv1.3/KCa-class), ADOPTED ON THE IMMUNE ROW ONLY (the other six rows stay bit-exact vs the deposit; the all-rows application is context, not adopted); ion conditions are ABSENT in the 119-entry deposit for the immune arm (scan deposited: 3 raw hits classified from context as drug-bath/dye-stock/external-protocol concentrations — C05 DiBAC stock, C06 BaCl2 bath, C11 external Cl- — ZERO cell-class in/out Nernstian sets), so the standard phagocyte Nernstian assumptions are the deposit of record (module ION trio kept unchanged — conductance-only recalibration; Nernst anchors E_K -84.85 / E_Na +55.52 / E_Cl -29.33 mV; literature rest window -60..-30 mV as context); immune arm -7.134 -> -41.088 mV (in band, in the literature window; activation swing +33.954 mV, the largest in the table); INSTRUMENT DISCLOSURE pre-commit: the ion-condition scan first reported its 3 raw string hits as "PRESENT", repaired to classify raw hits vs cell-class Nernstian sets — gates/physics untouched, both runs identical on every gated number; R1-R4 below
- GATE-R1 PASS: corrected immune REST arm -41.088 mV inside [-80,-10] under the ONE pre-registered scheme (C14 layer arithmetic verbatim, ION trio unchanged)
- GATE-R2 PASS (no regression): LV-G2 re-run on exp139's instruments verbatim — (a) trio in band (head -24.86 / trunk -50.26 / wound -38.03, re-run deltas 0.000 vs deposit), (b) head-trunk 25.40 vs 43+-50%, (c) wound depol 12.23 vs Chernet 19.4+-50%, (d) corrected map 7/7 in band with the six non-immune rows BIT-IDENTICAL (Vm/PK/PNa/PCl) and the before value reproducing the deposit's -7.134
- GATE-R3 PASS (held-out, direction pre-registered): the depolarization family held OUT of the recalibration (exp139's frozen partition re-run: exactly 5 entries — V6, DB-411, DB-413, C04, C09); the pre-registered direction holds — activation swing Vm_act - Vm_rest = +33.954 > 0 (the depolarization channel SURVIVES the recalibration), and the family's stack arm reproduces the deposited wnt EA 1.000 bit-exactly (seeds 1-3) — a conductance-only GHK change provably does not touch it
- GATE-R4 PASS: the corrected GHK table deposited for all families (7 rest rows with PK/PNa/PCl/in-band/delta-vs-deposit/changed flags; immune activated complement = the deposit map bit-exact; global-rule rest map as context — all 7 stay in band, epidermis -16.885 -> -48.566; ion-condition deposit; band-scope statement; per-family anchor map E/A/B/C/D)
- OWNED: REST-RANK SHIFT — under the corrected rest map immune leaves the most-depolarized rank (prediction V3 re-anchors to the ACTIVATED state, where its own ground truth lives: activated immune is the map's most depolarized state); exp139's LV-G1/G3/G4 verdicts not re-adjudicated (the D-arm EA re-run is the no-regression proxy on the one family R3 touches). REGISTERED NEXT: the same rest-open correction's all-rows adoption when the atlas matrix is ingested (context map already computed: every type stays in band; the epidermis row carries the same over-count bias), and an activated-state band anchor for the wound-ATP transient if the record ever gains one (today: none — owned); deposited as results/exp157_ghk_immune.json

## L142 — exp159 THE HYPEREDGE-NATIVE WALK (C1S, 3/4 — blindness PROVEN, native rule registered but separation FAILS at the verdict bar): exp137's pairwise projection (L115: each hyperedge e contributes |w_e|/(|e|-1) to every member pair) provably DISCARDS hyperedge grouping — 12 adversarial pairs (n = 30/32, construction seed 159 deposited; signed-cancellation gadgets: member 1 holds opposite-signed size-k hyperedge pairs (k = 3/4/5 by pair class) whose shared-pair contributions cancel to A = 0 exactly, member 2 covers the SAME nonzero pairs with size-2 hyperedges only; per-pair in-module asserts np.array_equal(A_1, A_2), S_1 != S_2, connectivity) decode to IDENTICAL verdicts under exp142's execute_signed 12/12 for both targets (H1 blindness PASS — arm-1 verdict tuples bit-identical across members, the grouping is invisible to the current read core); DESIGN FINDING deposited: the naive clique decomposition (hyperedge {a,b,c} vs three pairwise edges, exp137's e.g.) yields an IDENTICAL co-membership matrix S and can never separate — signed cancellation is the ONLY grouping signal that survives the pairwise projection; arm 2 = ONE pre-registered rule, zero knobs: A_ext = A + F*S (S_ij = 1 iff i,j share a hyperedge), F = 0.75 = median nonzero |A_ij| pooled over all 12 arm-1 projections computed BEFORE any decode; the augmentation genuinely injects the grouping (matrices differ on the 10/24/36 canceled entries at k = 3/4/5) but H2 separation FAILS 0/12 — the arm-2 verdict is TARGET-determined, not member-determined: T1 (uniform -30, exp94 MULTI layout) sustains (err 0.37-0.76 mV, 9/12 member-1 runs) and T2 (middle -59, exp94 BELOW layout) is verdict-false (err 3.2-4.0 mV) on BOTH members' augmentations, so the 6.0 mV verdict bar swamps the 0.00-0.09 mV cross-member err perturbations (grouping survives only SUB-verdict, largest at k = 5 = highest cancellation density — survival-by-class deposited); H3 median err on correct matches 0.53 <= 0.60 mV PASS (9 matches, all member-1/T1); H4 superset reduction PASS — when all hyperedges are size 2, S equals the support of A BIT-EXACTLY (array_equal, asserted 12/12 on the pairwise-only members) and the dedicated all-size-2 instance reproduces arm-1's blindness relation bit-exactly across members (separation power provably vanishes — the protocol is a strict superset); REPAIR REGISTERED for the next experiment: decode at the err level with the grouping contrast as readout (same target, S_1 vs S_2 augmentations, pre-registered |err_1 - err_2| threshold) or cancellation-density-weighted S; deposited as results/exp159_hyperedge_walk.json
## L143 — exp165 THE GENERATOR AT CF-1 (E2, 4/4 — exp156's registered repair ADOPTED: the generator's stage-3 ledger entry UPGRADES): CF-1 (the S-REL spec-adoption floor -35 -> -60 mV, exp156's one-constant repair) is adopted into the compiler's emitted-cell contract and the generator's C3 is re-run at the repaired floor on the SAME stack — the exp150 delivered-10 + the exp153 expanded cohort (24 members) — with exp156's dissect/decode_cf/clash_mass/r_w_predict imported VERBATIM (no new knobs; the deposited emitted rungs all (1.0, 0.0) and seeds (1,2,3) re-checked, no re-tuning; byte-offset assert proves docstring gates < frozen constants < first decode path); C1/C2/C4 unchanged channels re-verified from the deposits (10 delivered all beyond N*_lib 82.288 / N*_splice 20.14; 10/10 emitted_quads < 6.0; min min_pairwise_D 35.54 > N*_pool 33.776); F4 INSTRUMENT PASS — exp150's deposited decode errs reproduced bit-exactly under the UNREPAIRED floor (10/10 at 3 dp) plus the identity anchor decode_cf(NEURAL_SPEC_MIN) == dissect float-equal per seed (the CF-1 engine IS the unrepaired engine with the one constant changed and nothing else); F1 PASS — C3 (exp136 criterion: decode < 6.0 AND hold < 6.0 on >= 2/3 seeds at the deposited emitted rung) improves 8/10 -> 10/10, exact count deposited, 3/3-grade also 10/10: the six failing-class members land at 1.591-2.535 mV decode (d-03 9.10 -> 1.62, d-08 9.59 -> 1.68, d-12 9.96 -> 1.86, d-19 8.05 -> 2.20, d-22 9.07 -> 2.51, d-24 9.72 -> 2.50 seed-means), each reproducing exp156's deposited cf1 rows bit-exactly (24/24 cohort rows bit-exact at 3 dp); F2 PASS — the 8 previously-passing members stay passing with per-seed pass patterns 3/3 -> 3/3 IDENTICAL, CF-1 rows match exp156's harm deposit bit-exactly, and the branch-identity clause holds (d-06, the only clash-free delivered member: n_clash == 0 and CF-1 errs == exp150 unrepaired errs bit-exactly per seed — the repair is a no-op exactly where the mechanism says it must be); F3 PASS — R_W as pre-emission filter: {R_W-positive} == {audit_only_fallback} == exp156 failing class == {d-03, d-08, d-12, d-19, d-22, d-24} on the 24-member stack with clash masses reproducing exp156's w3 deposit bit-exactly — the filter excludes exactly the audit-only fallback class with ZERO false exclusions and every delivered member is R_W-negative (exp156's 0-FP deposit confirmed on the delivery semantics); STAGE-3 LEDGER UPGRADE deposited explicitly (exp150's stage3_test upgraded): emitted-cell contract amended to the CF-1 floor -60.0 with emitted = argmin rung_cost over rungs with quad < 6.0 AND decode 3/3 UNDER THE REPAIRED FLOOR, and the R_W canon-clash mass rule (clash_mass(f) > 36.0 mV^2) adopted as the pre-emission structural gate — the audit_only_fallback emission mode is RETIRED (its class == the R_W-positive set); C1/C2/C4, the ladder, the bars, the search all untouched. INSTRUMENT DISCLOSURE: the first run's F2 FAIL was an evaluation-scope bug (the conjunct swept all 10 delivered members instead of the pre-registered 8 — the two previously-failing members' F,F,F -> 3/3 pattern flip is the repair landing, not a regression); the docstring gate clause was always scoped to the 8, the code was fixed to that scope and re-run 4/4 — gates/clauses/physics untouched. REGISTERED NEXT: make the ONE-CONSTANT production change in cultivation/bioelectric/collective.py's spec-reading regen walk and re-run the generator END-TO-END on a FRESH search with R_W as the pre-emission filter (L132's never-tuned discipline — the 0-FP is cohort-confirmed; fresh-cohort confirmation is the remaining clause); deposited as results/exp165_generator_cf1.json

## L144 — exp163 THE GROUPING CONTRAST (E1, 3/4 — exp159's registered repair run FULLY PRE-REGISTERED; the err-level attributed grouping contrast FAILS its primary gate 2/12 — the read core stays grouping-blind AT ERR LEVEL; improvement/superset/instrument gates hold): construction reused exp159 VERBATIM (build_pair/project/co_membership imported, same 12 adversarial pairs, construction seed 159, bit-identical projections + S_1 != S_2 + S_2 == support(A) + cancellation layout + connectivity re-asserted per pair); THRESHOLD DEPOSITED BEFORE DECODING (two-phase write: phase-B JSON with the full pre-registration on disk before the first execute_signed call): noise floor = exp159's deposited max cross-member same-target err delta = 0.09 mV, theta = 3x = 0.27 mV; V2 WEIGHTING PRE-REGISTERED ONCE for both members: W(m)_ij = sum over member-m size->=3 hyperedges e containing {i,j} of |w_e|/(|e|-1) — the absolute signed-cancellation mass, peaking exactly on the 10/24/36 canceled entries where two opposite-signed flows cross; member 2 (all-size-2 clique/triad cover) has no size->=3 hyperedges -> W == 0 -> S_w(m2) == 0 -> A + F*S_w(m2) == A BIT-EXACTLY: any crossing is attributable to the sign-cancellation member BY CONSTRUCTION; readout two-sided own-target (m1 -> T1, m2 -> T2, seed 1, STAR_OP verbatim): C = |err(A+F*S_v(m1), T1) - err(A+F*S_v(m2), T2)| with attribution devs vs the shared arm-1 null, separation iff C > theta AND dev1 > theta AND dev2 <= theta (crossed ON the sign-cancellation member, NOT on the clique/triad member); G1 FAIL 2/12 (pairs 1 and 11 only, dev1 0.28/0.32 vs theta 0.27 — max signed-cancellation-side response 0.32 mV, median by class 0.205/0.045/0.22 mV — the read's err stays sub-threshold on 10/12 pairs; survival-by-class deposited); the V1 unweighted repair separates 0/12 (contrast 2.3-3.5 mV is target-baseline/regime-flip dominated: dev2 > theta exactly on exp159's 3 flip pairs 0/1/10 at 5.86/6.30/4.38 mV, sub-threshold elsewhere — never the member-1-only pattern); G2 PASS via the >= 2 clause (V2 2 vs V1 0) but the monotone density clause FAILS (d_k 43.5 < 73.0 < 85.5 pooled canceled mass yet median dev1 0.205 -> 0.045 -> 0.22 dips at k = 4 — NO dose-response, the err perturbation does not track cancellation density); G3 PASS (S_2 == support(A) bit-exact 12/12; S_w(m2) == 0 and augmented == A bit-exact 12/12; dedicated all-size-2 instance verdicts bit-identical across members under BOTH variants, V2 devs exactly 0.0 — separation power provably vanishes where no cancellation exists, strict superset); G4 PASS (arm-1 blindness 12/12 reproduced AND verdict tuples bit-identical to exp159's deposited arm-1 12/12 — instrument integrity); FINDING: zeroing the clique side makes the contrast attributable but the read STILL does not hear the grouping — the err response to the cancellation-reweighted augmentation is <= 0.32 mV on 10/12 pairs while the target-determined err scale is 0.3-4.0 mV; scalar single-pair err deltas are at their instrument floor for this construction; NEXT REGISTERED: the contrast needs either (a) a structure-sensitive err (canon/labeling-level or profile-shape contrast, not scalar profile err) or (b) a pooled/ensemble statistic across pairs (sum/median of signed dev asymmetries) — the single-pair err-level channel is exhausted at the deposited floor; deposited as results/exp163_grouping_contrast.json

## L145 — exp166 THE LEADING EDGE (U, 4/4 — exp160's registered corner PRICED: the powered 2^3 factorial names TEMPORAL the dominant main effect (refining exp160's lift-based hyper attribution on small cells), the pre-registered monotone-degradation expectation HOLDS, and the ONE mapped zero-knob rule R_T repairs the corner cell BELOW exp160's pooled median at the spot battery): 400 random media = crossed factorial over {oriented, hyper, temporal} active/inactive (8 cells x 50) with signed/complex PINNED INACTIVE (exp160's U3: neutral-to-protective, lift 0.74/0.67 — the corner cell stays inside exp160's named tail class A-SYM+A-PAIR+A-STAT and supersets); generator = exp160's RandomMedium VERBATIM with the five DIM_P coins replaced by the cell spec (_base_connected ring+chords p=0.04 support, _wU U(0.5,1.5) magnitudes, hyperedges 1-20 size 3-6 via w_e/(|e|-1), temporal T=8 p_keep~U(0.6,0.95) ring backbone always on; all frames real nonneg as a deposited consequence); generator seeds deposited FIRST (SEED_BASE 166166, rule SEED_BASE + 1000*c + j, c = 4o+2h+t, j = 0..49) and the pre-registration (gates P1-P4 + the repair-rule mapping hyper->R_H cancellation-density-weighted S per L142 / temporal->R_T flip-quiet core masking per L140 / oriented->R_O one-way restore with the pre-registered 'symmetrize already handles' audit note) committed as 701deaa BEFORE any decode; read = exp160's stack VERBATIM x seeds (1,2,3) = 1200 decodes, ONE configuration (READ_CONFIG = exp160's dict verbatim, fingerprint 8e11e88c1c2f1518 asserted == exp160's deposit; read_temporal IS exp148's, its executor IS exp142's execute_signed, spec IS exp94's MULTI; the rule lives entirely in the frames a wrapper yields — the reader branches on no instance property); GATE-P1 PASS: per-cell medians deposited (000 0.670 / 001 0.820 / 010 0.690 / 011 1.075 / 100 0.610 / 101 0.935 / 110 0.640 / 111 1.110 mV) + the 7-row Yates effect table from the 8 cell medians ((1/4)-scale, positive = active side degrades): main TEMPORAL +0.333 DOMINANT, main hyper +0.120, main oriented +0.010 (symmetrize already handles CONFIRMED by pricing — PN2's per-frame S = (R+R.T)/2 absorbs A-SYM), interactions o x h +0.018 / o x t -0.065 / h x t -0.095 (SUB-ADDITIVE — the corner is worse than any single dimension but NOT super-additive), triple -0.023; GATE-P2 PASS (registered expectation HELD, not the violation clause): mean-of-cell-medians strictly monotone along the active-count axis 0.670 < 0.707 < 0.883 < 1.110 for k = 0..3 and the corner cell (111) is the max cell median; GATE-P3 PASS: zero rejections, 1200/1200 errs finite, verify_rate 1.00, and the above-bar tail (1.30 bar) characterized: 23/400 concentrated EXACTLY in the hyper x temporal corner (14/50 in 111, 9/50 in 011 h+t, 0 in all six other cells, max 1.72-1.73 mV, all verifying) — the TAIL stays corner-owned exactly as exp160 named it while the MEDIAN shift is temporal-owned (refinement, not contradiction: exp160's lift cells were n=90/110 pooled, these are powered n=50/cell); GATE-P4 PASS: P1 named temporal -> the pre-registered mapping selects R_T 'flip-quiet windowing' (L140's discipline at the medium level, ZERO knobs: every frame masked to the across-frame CORE support — membership frozen, zero presence transitions, flip-clock F = 0, A_ext = A); spot battery (corner cell j=0..9 + clean cell j=0..9, seeds 1,2,3, 120 decodes): arm A replay BIT-EXACT vs the main battery 20/20, clean cell arm B BIT-IDENTICAL to arm A (the no-op-by-construction clause verified exactly — zero regression), corner median 1.015 -> 0.535 mV with 10/10 instances improved (per-instance 0.89-1.29 -> 0.50-0.60 — every corner spot instance lands below exp160's deposited pooled median 0.630): the corner's excess is largely the TC1 flip-clock channel's own response to presence transitions, not lost-edge information, and the L140 discipline repairs it at the medium level with the read core untouched; INSTRUMENT NOTE: the smoke run caught a spot-battery indexing bug before the pre-registration commit; the credited full run used the committed script unchanged, wall 137.6 s (budget 12 min). REGISTERED NEXT: R_T as a zero-knob ADOPTION candidate into exp148's read_temporal for temporal media (one clause: mask frames to the core support when T > 1 — the bit-exact clean-cell no-op property is the adoption-safety proof), and an R_T x R_H cross check on the 011 h+t cell where the tail lives; deposited as results/exp166_leading_edge.json

## L146 — exp168 CF-1 TO PRODUCTION (P, 4/4 — exp165's registered next EXECUTED: the ONE-constant repair LANDS IN THE CORE and the generator re-lands END-TO-END on a fresh search under the R_W pre-emission filter): the production patch is exactly ONE constant — cultivation/bioelectric/collective.py:46 NEURAL_SPEC_MIN = -35.0 -> -60.0 (the S-REL spec-adoption floor; consumers: exp136.decode:394 `if c.phi_spec[i] >= NEURAL_SPEC_MIN` — the generator's decode CF-1 targets — and the core's M33 neural-channel gate collective.py:366/584, INACTIVE at defaults since neural_w = 0 short-circuits before the floor is read); CF-1 semantics: adoption reads max(spec, floor) against the canon fallback, so the wider floor can only change behavior where a spec value fell BELOW the old floor (the old clip region) — -60.0 is below every writable zone value (the compiler's repertoire floor WIDE_LO/REPERTOIRE_LO = -60.0); pre-registration (gates B1-B4 + the pin mechanism + branches) committed as 2f9f785 BEFORE any decode, byte-offset assert proves docstring gates < frozen constants < first decode path; GATE-B1 PASS: python3 -m tests.run_tests from the repo root POST-patch exits 0 with ZERO failures (default suite and --full both clean; checked beforehand — NO test asserts the old floor: tests reference -35.0 only in test_fidelity's unrelated quantize tie-break and test_d3_semantics' theta anchor value; nothing touched, disclosure stands); GATE-B2 PASS (bit-exactness at the OLD operating points, pre-registered mechanism = value pinning: OLD_FLOOR_PIN rebinds the ONE constant to -35.0 in the three modules that captured it at import time — collective/exp136/exp156 — with save/restore asserted): exp150's deposited decode AND hold errs on the ORIGINAL 10 reproduced 10/10 at the deposit's 3-dp rounding under the patched core at the pinned old floor (exp136.decode VERBATIM at the deposited emitted rungs, all (1.0, 0.0), seeds 1,2,3); clip-only proof: (i) branch identity — the only clash-free delivered member d-06 (n_clash = 0 cells with (f < -35) & (f != canon)) decodes BIT-EXACTLY (float equality per seed) under the PATCHED default vs the PINNED floor — the patch changed nothing where nothing was clipped; (ii) engine identity — the patched default decode == exp156's decode_cf(spec_floor = -60.0) bit-exactly per seed for ALL 10 (the counterfactual engine exp165 priced IS the production engine); GATE-B3 PASS (fresh-search end-to-end): exp150's pipeline VERBATIM — 72-member library with N*_lib re-derived 82.288, splice family 48,564 with N*_splice re-derived 20.140 via exp146's splice_family_bar (400-pair fast-vs-verbatim harness max diff 1.4e-14), exp141's search loop at seed 141 BIT-IDENTICAL (all rounds + pool 253 vs the exp141 deposit), funnel 96/253 lib-novel -> 96/96 splice-clear, N*_pool re-derived 33.776 before selection — with the ONE pre-registered upgrade from exp165's stage-3 ledger entry (the R_W pre-emission exclusion clause in the greedy; splice clause and C4@N*_pool kept; cap 10) DELIVERS 10/10: C1 True (every member beyond N*_lib 82.288 AND N*_splice 20.14), C2 10/10 (emitted-rung quads < 6.0), C3 10/10 AT THE REPAIRED FLOOR (decode < 6.0 AND hold < 6.0 on 3/3 seeds for ALL 10 — errs 1.225-1.698 mV, bit-for-bit exp165's counterfactual values now produced by the production core, e.g. d-03 9.099 -> 1.591), C4 True (min pairwise D 35.538 > N*_pool 33.776), all emitted rungs (1.0, 0.0) with emission mode repriced_full — the audit_only_fallback mode NEVER fires (retired per L143); the fresh delivery is exp150's delivered-10 EXACTLY (same zone keys, same order — the search is bit-identical so the funnel lost nobody, and the filter excluded nobody); GATE-B4 PASS (R_W discipline on the fresh cohort): the production-floor R_W-positive set is EMPTY over all 96 eligible and equals the excluded set (set identity both ways), all 10 delivered are R_W-negative, zero false exclusions (shadow pricing vacuous); the mechanism reading deposited: 27/96 eligible are R_W-positive at the OLD floor (max clash mass 111.586 mV^2) — the class the old-constant rule would now falsely exclude is exactly the class the repaired floor made readable (d-03/d-08-class members decode 3/3 under production), so the pre-filter tracking the SAME frozen constant the decode reads (zero new knobs) is structurally silent precisely because its failure mechanism is retired; INSTRUMENT NOTES: no instrument bug this run — the credited run used the committed pre-registration script unchanged, wall 178.1 s (budget 15 min), tests + patch + fresh search all in one process with the pin restored-asserted between stages. REGISTERED NEXT: the widened floor makes deep-zone writes FIRST-CLASS (the search's own deep voltage band down to -60 is now fully readable — the class the old floor effectively refused at decode is writable, so a deep-band invention sweep prices the widened repertoire's own frontier), and the L145 R_T adoption + R_T x R_H cross check remain the open read-core candidates; the M33 gate's new [-60, -35) regime (collective.py:366/584) is unexercised by any deposited experiment — its first use should carry its own bit-exact-at-old-operating-points audit; deposited as results/exp168_cf1_production.json

## L147 — exp167 R_T ADOPTED (orchestrator-run salvage; module complete from workstream F1, unrun at context death; 3/4): the flip-quiet core-support windowing (R_T, zero knobs) adopted into the exp148 read for time-varying media — A_ext = A + F on R_T-masked frames; verdict: adoption is SAFE and fidelity-positive where scoped, separation PRESERVED, but the N3 bar is not uniformly reached (see gate detail; the aperiodic-media scoping question registered). REGISTERED NEXT: per-media scoping diagnostic (PN1-style, pre-registered) for R_T on aperiodic media; R_T x R_H cross-check on the 011 corner cell (L145's registered follow-up)


## L148 — exp169 R_T SCOPED (orchestrator-salvaged from a post-run subagent death; 4/4): exp167's registered per-media diagnostic RUNS and RECONCILES what the blanket clause could not — the diagnostic f_max = max per-edge presence-transition count (PAIR-JOINT max for paired constructions: one arm per pair or the N2 contrast is an instrument artifact), threshold 32.0 fixed from the DEPOSITED empty gap (7 = corner/diffuse ceiling, 1165 = battery/concentrated floor; >= 4x and >= 36x margins) BEFORE any decode; rule: R_T (exp167's adopted read) iff f_max < 32 else exp148's RAW temporal read; GATE-S1 PASS (20/20 corner+clean spot media f_max < 32, 12/12 battery pair-joint >= 32, per-chord counts match exp167's deposit exactly); GATE-S2 PASS (battery under the scoped read IS exp148's raw temporal bit-exactly — 12/12 N2 separation restored, 12/12 N1 blindness reproduced: the schedule channel survives wherever it lives); GATE-S3 PASS (corner spot under the scoped read IS exp167's adopted bit-exactly — median 0.535 replayed, the corner repair kept); GATE-S4 PASS (all 20 grid instances classify DIFFUSE at T=32 — the grid's flip clocks live at the flip-edge scale, never chord-concentrated; scoped pooled median 0.68 <= 0.685 no-regression; the concentrated side is carried entirely by the battery); FINDING: the blanket clause falsified because it was SCOPED WRONG, not because R_T is wrong — each medium gets the read its channel structure supports and the fidelity-vs-separation trade dissolves; pre-registration 9d61e3b, credited run used the committed script unchanged, deposited as results/exp169_rt_scoping.json. REGISTERED NEXT: (i) the scoped read as the ADOPTION candidate for exp148's production temporal read (the diagnostic clause is one function, zero knobs); (ii) the grid's all-diffuse classification means N3's 0.60 bar is never reached by R_T on the grid (0.68 stands) — the temporal channel's remaining excess is NOT flip-clock: price it (the pre-registered suspect is the hyper dimension the grid shares with the corner)

## L149 — exp170 R_T x R_H CROSS-CHECK ON THE 011 CELL (C, 3/4): L145's registered follow-up RUNS — the composed zero-knob rule lands the median but NOT the parity bar (C3 REFUTE at the pre-named 2/3 partial: median 1.05 -> 0.61 mV, 10/10 spot instances improved, parity 0.61 > 0.60 by 0.01); C1 PASS (raw replay: 30/30 finite, 0 rejections, tail character reproduced 10/10 instance medians above exp160's pooled 0.630, spot median 1.05 ~ main battery 1.075); C2 PASS (the two channels PRICED separately: R_T alone 0.525 owns the repair; R_H alone 0.905 barely moves it — the hyper channel is NOT the 011 cell's repair); C4 PASS (150 decodes, 0 rejections, pin save/restore asserted; order sensitivity recorded: reversed augment-then-mask A4 0.625 > primary mask-then-augment A3 0.61, sign +0.015, no bar); composition = exp166's rule_temporal_core then rule_hyper_S with F' = pooled median nonzero |W| of the MASKED frames (0.942311; raw pooled F 0.858492), both computed BEFORE any decode; spot set CornerMedium cell c=3 j=0..9 seeds (1,2,3), exp166's P4 protocol verbatim, fingerprint 8e11e88c1c2f1518 asserted; pre-registration 319c352, credited run body-only-filled, wall 17.4 s, deposited as results/exp170_rt_x_rh_corner011.json. REGISTERED NEXT: the composed rule is DOMINATED (R_T alone beats it on the same cell) — R_H is retired for the 011 cell and the composition is not an adoption candidate; the remaining 011 excess after R_T (0.525 vs clean 0.630 — ALREADY below the pooled clean median) makes the parity question moot at the median: the 011 cell's repair is R_T ALONE and the parity bar's 0.01 miss belongs to the tail instances, not the median — price the tail instances' residual channel (the pre-registered suspect: the oriented dimension's absence, o=0, which R_O was already priced to absorb)

## L150 — exp171 M33'S NEW [-60,-35) REGIME (P, 4/4 — the FIRST neural_readout > 0 run in the corpus): L146's registered note EXECUTED with its own bit-exact-at-old-operating-points audit — core engine VERBATIM (M33 branch collective.py:582-587, pole params 199-200, floor line 46) under sustained corpus blockade block_gap_junctions(0.05) -> r=0.05, uniform per-plane spec identities on the exp32 TAILP blocked plane, seeds (1,2,3), patched (CF-1 -60.0) vs pinned (OLD_FLOOR_PIN -35.0, save/restore asserted), neural_w = 0.5 the ONE pre-registered weight; M1 PASS (HEAD -20 / LINE -35 bit-identical patched vs pinned: final V, phi_spec, guess stream, full draw-log sha256 — the patch invisible where already active); M2 PASS (TRUNK -50 / DEEP -60 LIVE: qualifying cells 15/15 patched vs 0 pinned, streams split exactly at the branch, the first divergent step reproduces the M33 blend bit-exactly — guess = (1-w)*(wound_center+draw) + w*(spec+nread) over the pinned arm's shared draw, replay-verified through the whole engine by the pinned-floor M36 misanchor=1.0 instrument, bit-identical 6/6); M3 PASS (the literature asymmetry PRICED: err = |guess-spec| pooled, A_pinned 3.7682 (TRUNK 13.8492 vs HEAD 10.0810), A_patched 0.5840 (TRUNK 9.4970 vs HEAD 10.0810), ratio 0.1550 < 0.5 -> PRE-NAMED BRANCH (b): the head/tail blockade asymmetry COLLAPSES toward the patched floor's eligibility — the widened floor makes the -50 trunk identity pole-eligible, which erases exactly the posterior-plane junction-carried phenomenology M33 encodes); M4 PASS (neural_w = 0 bit-identical across all four families whole-sweep, pin asserted across 30 pinned runs, zero non-finite); pre-registration 7de4a68, credited run body-only-filled, wall 1.3 s, deposited as results/exp171_m33_widened_regime.json. REGISTERED NEXT: the SPLIT is the registered next — M33 needs its OWN anterior line constant (M33_LINE = -35.0, the literature midpoint) distinct from the S-REL adoption floor (NEURAL_SPEC_MIN = -60.0); the patch is one new constant + one gate-branch change, carries the same bit-exact-at-old-operating-points audit (HEAD/LINE unchanged at both floors, TRUNK/DEEP return to pinned behavior under M33 while adoption keeps CF-1), and the fresh-question it opens: whether any substrate in the corpus WANTS pole-eligible deep identities (the -60 pole readout as a FEATURE, priced separately if the split lands)

## L151 — exp172 DEEP-BAND INVENTION SWEEP (P, 4/4): L146's registered frontier pricing EXECUTED — the widened repertoire's deep band is REAL all the way to the floor; DEEP rungs {-40,-45,-50,-55,-60} x 10 instances (MULTI 3-zone program translated +i cells, instance 0 = MULTI verbatim) x seeds (1,2,3) vs SHALLOW controls {-20,-25,-30}, patched (CF-1 -60.0) vs pinned (OLD_FLOOR_PIN -35.0, core + exp136's import-time capture, save/restore asserted), exp136.decode VERBATIM at the deposited production cell (1.0, 0.0); D1 PASS (90/90 shallow records bit-exact patched vs pinned — the adoption branch consumed one normal draw on EITHER side pre-patch so the rng streams align; any mismatch would have been an instrument bug); D2 PASS (150/150 deep records pinned > patched, and the pinned errs sit AT the canon-refusal scale: 8.33/9.49/11.42/13.80 vs canon-projection 8.37/9.49/11.40/13.78 — the write demonstrably did not take under the old floor); D3 PASS (the frontier rung NAMED = -60.0, the deepest of the ladder: patched medians 2.80 decode / 3.91 hold <= the production 6.0 bar — EVERY deep rung passes, the whole [-60,-35) band is writable, no depth cliff inside the repertoire); D4 PASS (0 rejections, all finite, shallow arm first so pin leakage would fail D1 loudly, canon == wildtype asserted); pre-registration 5013e92, credited run body-only-filled, wall 27.1 s, deposited as results/exp172_deep_band_sweep.json. REGISTERED NEXT: the band is writable but the GENERATOR has never BEEN SENT there — the search's own target families (exp150's pipeline) have never carried a deep-band target; next: the fresh-search end-to-end with deep-band target families (the exp168 B3 pipeline verbatim, targets at the deep rungs, bars re-derived at the pipeline's own N*_lib/N*_splice/N*_pool), which tests whether the search's selection machinery VALUES the widened band or the band's writability stays dormant until targets ask for it

## L152 — exp173 THE POOLED GROUPING STATISTIC (E, 4/4): L144's registered repair (b) EXECUTED — the sign structure exp163 never read CARRIES the grouping at the ensemble level; construction replayed bit-exactly (exp159's build_pair/project/co_membership, 12 adversarial pairs, seed 159, A1 == A2 12/12, m2 augmentation bit-exact identity, unsigned devs match exp163's deposit 12/12 both sides within the 2-dp rounding); the NEW statistic: dev_signed = err(aug) - err(null) SIGNED per pair, pooled = mean over 12 pairs, V2 weighting verbatim, STAR_OP readout, -35.0 instrument pin; two-phase discipline held (phase-A null bar frozen on disk at byte 6980 < first phase-B decode 7058; seed-1 null replay bit-exact 24/24 vs exp163's deposited null_errs; bar = max |pooled null stat| over exp142's deposited seeds = 0.0717 mV); E3 PASS (stat_m1 = +0.1417 mV > bar 0.0717 with a 10/12 MAJORITY SIGN on the cancellation side — a consistent ensemble response, not 12 independent coin flips; the positive sign reads: the cancellation-reweighted augmentation IMPROVES the own-target err, i.e. the grouping is audible in the signed aggregate even though every per-pair contrast sat under theta); E4 PASS (clique side silent |stat_m2| = 0.0 <= bar — attribution survives at ensemble level, exp163's G3 discipline carried over); E1/E2 PASS as above; pre-registration 0f55852, credited run body-only-filled, wall 7.4 s, deposited as results/exp173_pooled_grouping.json. REGISTERED NEXT: the ensemble statistic is a READ INSTRUMENT, not just a verdict — its per-pair signed devs (deposited) localize WHERE the grouping is audible (the 2 minority-sign pairs are the pre-registered suspects for a structure-sensitive split); next: (a) minority-pair anatomy — what distinguishes pairs 2 and 11's sign flips (density d_k, cancellation layout, gadget size), and (b) the ensemble as the production grouping read: a second cohort of 12 FRESH adversarial pairs (same construction, new construction seed) to test the signed-mean signature REPLICATES (the ensemble's power claim is only as good as its second cohort)


## L153 — exp174 THE REPLICATION COHORT (E, 4/4): exp173's signed-mean signature REPLICATES on 12 FRESH adversarial pairs (exp159's construction verbatim, the ONE disclosed changed input SEED_CONSTRUCT rebound 159 -> 174174, save/rebind/restore asserted; fresh projections bit-independent of the original cohort 12/12; construction integrity A1==A2 / S1!=S2 / S2==support(A) / connectivity 12/12); F2 PASS (two-phase null discipline: fresh bar 0.098333 frozen on disk 2036 bytes BEFORE any real-arm decode, byte order 6743 < 6821); F3 PASS (|stat_m1_fresh| = +0.1075 mV > bar 0.0983 with an 11/12 MAJORITY SIGN — the ensemble verdict survives independent draws, NOT cohort luck); F4 PASS (clique side silent |stat_m2_fresh| = 0.0 <= bar, V2 identity 12/12); F = 0.75 recomputed from the fresh pool pre-decode (same rule, same value); MINORITY ANATOMY recorded no-bar: all three minority-sign pairs across both cohorts are k = 4 gadgets (original p4/p6, fresh p5) — the density hypothesis registered; pre-registration f75075f, wall 5.4 s, deposited as results/exp174_replication_cohort.json. REGISTERED NEXT: the k-controlled cohort — gadget-size-stratified fresh pairs (k = 3 only vs k = 4 only, 6 pairs each), signed-mean per stratum: if the k = 4 stratum flips sign while k = 3 holds, the ensemble's sign structure is a DENSITY effect and the grouping read gains its first structural covariate

## L154 — exp175 THE M33 SPLIT TO PRODUCTION (P, 4/4): exp171's registered repair LANDS — ONE new constant collective.py:47 M33_LINE = -35.0 (the anterior/posterior literature midpoint, directly under NEURAL_SPEC_MIN) + the M33 gate branch (pre-patch collective.py:582) reads M33_LINE where it read NEURAL_SPEC_MIN; exactly two lines (P4 numstat asserted from git diff pre-commit); NEURAL_SPEC_MIN stays -60.0 (the S-REL adoption floor; exp136.decode untouched, CF-1 stands); P1 PASS (tests green post-patch, exit 0); P2 PASS (M33 restored BIT-EXACTLY: exp171's four families re-run at neural_w 0.5, r 0.05, seeds (1,2,3) — TRUNK/DEEP qualifying cells 15 -> 0, every re-run bit-identical to exp171's deposited PINNED arm (final_V/theta/phi_spec/guess_stream + full draw-log sha256), HEAD/LINE identical to BOTH arms, asymmetry ratio A_patched/A_pinned = 1.0 EXACTLY — exp171's pre-named branch (a) by construction, the 0.1550 collapse repaired); P3 PASS (adoption untouched: exp172's frontier rung -60.0 + all 90 shallow controls replay bit-exact under the split core on BOTH arms, patched adopts / pinned refuses at the canon scale); P4 PASS (pin asserted across 105 pinned runs, zero non-finite; M36 disclosed: inactive at defaults, floor NOT changed — the misanchor branch's floor is now NEURAL_SPEC_MIN while M33's is M33_LINE, a disclosed asymmetry to audit IF M36 is ever exercised); pre-registration 006ccc9, wall 14.8 s, deposited as results/exp175_m33_split.json. REGISTERED NEXT: the split's second consumer — M36 (mis-anchored pole) is now the ONLY branch still reading NEURAL_SPEC_MIN for eligibility; either pin it to M33_LINE for consistency (one line, same audit) or deposit the disclosed asymmetry as intended; and the feature question from L150 stands open: whether any substrate WANTS pole-eligible deep identities (the -60 pole readout as a feature, priced only if a substrate family asks)

## L155 — exp176 DEEP-BAND GENERATOR SEARCH (P, 3/4): L151's registered dormancy question ANSWERED SPLIT — the pipeline is exp168's B3 verbatim with the ONE swapped input (deep-band targets, rungs -40/-50/-60, exp172's construction, canon == wildtype asserted, f_sha256 deposited); G1 PASS (bars re-derive bit-exact 82.288/20.140/33.776; the search loop at seed 141 BIT-IDENTICAL through the funnel — the search's selection does NOT consult the targets, PROVEN by bit-identity); G2 REFUTE (0/10 delivered members decode+hold < 6.0 at the deep targets: decode 6.12-6.19 at rung -40, 9.3+ at -50; hold 6.27-6.38 / 9.3+ — every (member, rung, seed) row deposited); G3 PASS (9/10 delivered members carry >= 1 emitted rung in [-60,-35) — the compiler REACHES into the band when targets ask; the repertoire is not dormant); G4 PASS (R_W set identity, zero false exclusions, delivered all R_W-negative); THE FINDING: the search's selection machinery is TARGET-FREE — it VALUES the band (members emit deep rungs) but nothing in the funnel chases target fidelity, so the structure-selected cohort fails deep-target delivery at 6.1-9.3 mV; pre-registration 0ddb58e, orchestrator-salvaged from a post-run subagent death, deposited as results/exp176_deep_band_search.json. REGISTERED NEXT: the TARGET-AWARE DELIVERY clause — rank the 96-eligible pool by price at the GIVEN target set before the cap-10 selection (exp150's price_rung machinery already computes decode prices; the clause adds NO new knobs); its gates: bit-exact reproduction of exp150's delivered-10 at exp150's own targets (the clause must be inert at the old operating point), >= 9/10 deep-target delivery at the deep rungs, R_W discipline, zero rejections

## L156 — exp177 THE GRID RESIDUAL DECOMPOSITION (E, 4/4): L148's registered pricing EXECUTED — the grid's residual above N3's 0.60 bar is a SCALE effect, NOT a channel the RULE_MAP knows; R1 PASS (the 20 grid instances rebuilt exactly as exp169's S4, identity bit-exact, the 60 per-(instance,seed) scoped errs replayed bit-exactly from the deposit, pooled median 0.68 reproduced, ZERO new decodes); R2 PASS (all seven feature families computed from the media alone, finite, Spearman per class and pooled); R3 PASS (dominant channel NAMED: c2_n at pooled rho = +0.6984 >= 0.5 — runner-up c5_support_density -0.6809; the schedule channel is SILENT under the scoped read: paired classes replay bit-identical errs, c1 rho = 0.00, c4 +0.059, c7 -0.298; n=400 instances carry residuals +1.10/+1.11 vs 0.00-0.16 at n=100); candidate repair NOT priced — no rule in exp166's RULE_MAP maps the scale dimension, the gap is REGISTERED; R4 PASS (zero rejections, zero decodes, pin asserted); pre-registration a91252b, deposited as results/exp177_grid_residual.json. REGISTERED NEXT: the scale channel's anatomy — the read's own instruments at n=400 (labeling_bfs_n's BFS label order, spec_target_n's coverage, PN2's per-frame symmetrize cost at scale) decomposed on FRESH n=400 instances (the grid's deposited 2 are too few to price a repair): if the residual tracks label-ORDER coverage, the zero-knob candidate is a size-aware BFS source set (multi-source at n >= 300, the threshold pre-registered from the n=100/n=400 boundary the deposit already names); if it tracks support density instead, the residual belongs to c5 and the R_H family is back on the table AT SCALE

## L157 — exp178 THE SCOPED READ TO PRODUCTION (C, 4/4): L148's registered adoption CLOSED — exp148's production decode dispatch gains the ADDITIVE arm 'scoped' (read_scoped: ONE function, zero knobs; f_max via exp169's f_max_frames VERBATIM with THRESHOLD 32.0, PAIR-JOINT max for paired constructions; R_T (exp167's adopted path) iff f_max < 32 else the existing temporal path UNCHANGED; every pre-existing arm and caller untouched); A1 PASS (static bit-exactness: torus final V bit-identical to the temporal arm 3/3, verify preserved, errs == exp148's deposited static records; signed 12/12, complex_phase 12/12, reactive 18/18 bit-identical + replay; f_max == 0 < 32 at T=1 -> the rule selects R_T and rule_temporal_core's T=1 no-op identity makes it EXACTLY the old read); A2 PASS (the 12 battery pairs under the scoped arm ARE exp148's raw temporal bit-exactly: errs + verdicts 12/12, separation 12/12, blindness 12/12, pair-joint f_max 1206-1248); A3 PASS (corner spot set under the scoped arm IS exp167's adopted bit-exactly: median 0.535 replayed, clean no-op vs exp166's arm-A); A4 PASS (grid: zero rejections, pooled median 0.68 <= 0.685, classification identical to exp169's S4, tests suite green POST-wiring exit 0); the -35.0 instrument pin asserted; credited run via the pre-registered split runner (A2 229.0 s + A1 17.9 s + A3 5.6 s + A4 22.5 s, each gate exactly once, merged deposit); pre-registration fc5f601, deposited as results/exp178_scoped_production.json. REGISTERED NEXT: the scoped arm is PRODUCTION — the corpus's temporal-read experiments adopt it as the default temporal dispatch in the NEXT experiment that touches the read chain (one-line arm switch at the call sites, zero semantic change: the scoped arm IS the old read on every deposited battery); the read core's remaining open channel is the scale gap (L156) and the adversarial-media extension of the universal reader (Stage 5 path 1's ~85% -> close)


## L158 — exp179 TARGET-AWARE DELIVERY (P, 3/4): exp176's registered repair clause RUNS and the refutation moves UPSTREAM — H1 PASS (pipeline bit-identity at seed 141: bars 82.288/20.140/33.776 float-equal, funnel 96/253 -> 96/96, J-order delivery identical to exp150's deposited cohort, harness max diff < 1e-9; price tables 96 + 96 rows computed FRESH after the funnel); H2 PASS (the clause's delivered-10 scored at exp150's OWN targets pass C1-C4 ALL — min pairwise D 34.791 > N*_pool 33.776, quads < 6.0, zero rejections: the clause is quality-preserving at the old operating point, member set may differ, bars may not); H3 REFUTE (deep-target delivery 1/10 — per-rung full-valid passes {-40: 2, -50: 1, -60: 1}, zero rejections, and the retired audit_only_fallback mode FIRES on the deep rows: even price-ranked delivery across the WHOLE 96-eligible pool cannot assemble 10 deep-writable members); H4 PASS (R_W set identity, 0/1248 rows rejected); THE FINDING: the deep-delivery failure is NOT a delivery-ranking problem — the pool's members carry MIXED-VALUE programs (e.g. -40.8/-28.6/-42.7) and the deep targets demand UNIFORM-deep patterns (all zones at the rung), which the U(-60,-15) per-zone library draw makes vanishingly rare; exp172 wrote uniform-deep patterns by DIRECT construction, bypassing the library; pre-registration c7c0dea, orchestrator-run, deposited as results/exp179_target_aware_delivery.json. REGISTERED NEXT: the DEEP-PROGRAM LIBRARY COHORT — library members whose zones are ALL-DEEP (exp172's uniform-rung construction as library programs, rungs -40/-50/-60 x the zone-layout ladder), pushed through the SAME splice/funnel machinery with the structure bars RE-DERIVED (they are structure bars, not fixed constants), then the same clause delivery at the deep targets: the question is whether the machinery that selected 10/10 at the original classes selects deep-writable members when the library CONTAINS them

## L159 — exp180 THE SCALE ANATOMY (E, 3/4): exp177's mechanism-first pricing RUNS — 12 fresh n=400 + 12 fresh n=100 grid instances built and decoded under the scoped arm (-35.0 pin); T1 REFUTE (one fresh n=100 instance lands at residual -0.01 mV, ONE 2-dp tick below the deposited reference range [0.00, 0.16] — the reference-range clause was defined on 2-dp medians and the boundary tick failed it; binary gate, binary verdict, no loosening); T2 PASS (all five feature families computed and finite at both scales, Spearman table deposited); T3 PASS with the GENERIC branch (NO feature separates the scales at the pre-registered bars |rho| >= 0.5 at n=400 AND < 0.3 at n=100: support coverage/density are the borderline pair +0.6014 / +0.3636, BFS reach is degenerate 1.0 at both scales, asymmetry 0, seed-spread 0.23 / -0.45 — the residual is a GENERIC size effect at this census, and the n-scaling of the read is registered as its own instrument question); T4 PASS (the ONE disclosed candidate — the reverse-BFS label order — is a NO-OP at n=400: err_fwd == err_rev = 1.6975 exactly, registered=False); DISCLOSURE: a3 (the eV/eT split) was substituted by the computable proxy pair (native-gap, seed-spread) because exp160's module exposes no per-decode read-chain quadrature split; pre-registration c7c0dea, orchestrator-run after two subagent deaths, deposited as results/exp180_scale_anatomy.json. REGISTERED NEXT: the N-SCALING LADDER — the read's err profile at n = 100/200/300/400/500 (10 fresh instances per rung, both schedule classes, the scoped arm), the residual-vs-n curve and the coverage features per rung: if the curve is monotone the instrument has a scaling law to name; if it saturates at n >= 300 the grid's n=400 residual is a finite-size plateau, not a trend


## L160 — exp184 THE DEEP-PROGRAM LIBRARY COHORT (P, 2/4): the refutation chain COMPLETES — the funnel itself is deep-hostile; the extended library (exp141's 72 + 15 all-deep members, exp172's uniform-rung construction as LIBRARY programs, rungs -40..-60 x 3 MULTI-layout shifts) builds with bars re-derived (N*_lib 81.523 / N*_splice 18.666 / N*_pool 32.664, deposited before selection); X1 PASS (extended pipeline integrity, funnel 270 -> 88 -> 88, harness < 1e-9); X2 REFUTE (0/15 all-deep members in the eligible pool — the novelty/splice criteria exclude EVERY deep program; splice-clear 0); X3 REFUTE (clause delivery at deep targets 1/10 from the deep-empty pool, per-rung {-40: 3, -50: 2, -60: 1}); X4 PASS (the extended library still delivers 10/10 at exp150's own targets, min D 40.430 > 32.664 — the old class untouched); THE CHAIN: exp176 cohort fails -> exp179 pool-ranking fails -> exp184 the FUNNEL excludes deep programs even when the library contains them — structural, upstream of delivery and ranking; pre-registration 357faa4, orchestrator-run, deposited as results/exp184_deep_library.json. REGISTERED NEXT: the FUNNEL EXCLUSION ANATOMY — trace each of the 15 deep members through every funnel stage (lib-novel distance vs N*_lib, splice-family membership, splice-clear price vs N*_splice), name the excluding stage and the per-member criterion values: is the exclusion a DISTANCE failure (deep programs too similar to each other), a NOVELTY-rank failure (out-competed by the 72), or a SPLICE-clear failure (their splices price above N*_splice)

## L161 — exp185 THE N-SCALING LADDER (E, 4/4): exp180's registered instrument question RUNS — the read's residual-vs-n curve over n = 100/200/300/400/500 (10 fresh instances per rung, 5 per schedule class, the scoped production arm, -35.0 pin) is MONOTONE: strictly rising per-rung pooled medians 0.075 -> 0.355 -> 0.680 -> 1.105 -> 1.480 mV (n500 - n100 = +1.405, no plateau: the n >= 300 tail spans 0.80 >> the 0.05 saturation tolerance); Y1 PASS (50 instances, zero rejections, the n=100 rung inside the deposited scale); Y2 PASS with the MONOTONE branch named (a scaling law to name, not a finite-size plateau); Y3 PASS (support coverage rho = +0.974 and density rho = -0.927 carry the size effect on the pooled 50 — the mechanism side-data exp180's census only glimpsed at two scales); Y4 PASS (pin asserted, the n=100 rung replays exp169's grid band); pre-registration 357faa4, deposited as results/exp185_n_scaling.json. REGISTERED NEXT: the scaling law's MECHANISM — the per-cell error map at n = 400/500 decomposed boundary-vs-interior (zone-boundary cells vs zone-interior cells): if the error lives at the boundaries, the law is the LABELING RESOLUTION (spec_target_n's spans scale with n while the read's projection resolves them at fixed cost); if interior, it is VALUE FIDELITY at depth; the split is computable from the deposited read states with zero new decodes

## L162 — exp186 THE POLE-FEATURE PRICE (P, 4/4): L154's open question ANSWERED — branch HELP: the deep pole readout is a FEATURE WORTH ARMING; the counterfactual ARM-DEEP (core.M33_LINE rebound -60.0, save/rebind/restore asserted; the CF-1-world M33 behavior) vs ARM-PROD (the production split, M33_LINE = -35.0) on exp171's four families (neural_w 0.5, r 0.05, seeds (1,2,3), protocol verbatim); Z1 PASS (ARM-PROD reproduces exp175's P2 records 12/12 bit-exactly — final V/theta/phi_spec/guess stream + draw-log sha256); Z2 PASS (the counterfactual is live: TRUNK/DEEP qualifying 0 -> 15/15 under ARM-DEEP, streams diverge exactly at the first pole-read draw with the blend reproduced bit-exactly; HEAD/LINE bit-identical); Z3 PASS branch HELP (pooled |guess - spec| at the blocked plane: TRUNK 13.8492 -> 9.4970, delta -4.3523 mV; DEEP 18.5228 -> 12.6315, delta -5.8913 mV; BOTH < 0 — arming helps both deep-eligible families; HEAD/LINE exactly 0.0); Z4 PASS (rebind asserted, zero non-finite); the production split is literature-faithful but LEAVES SUBSTRATE VALUE ON THE TABLE; pre-registration 357faa4, deposited as results/exp186_pole_feature_price.json. REGISTERED NEXT: the feature's OPERATING ENVELOPE — the delta's sign across the blockade-depth ladder r in {0.05, 0.2, 0.5} (the disclosed sweep, TRUNK/DEEP families, the pre-registered reading: the deep pole readout is a BLOCKADE-REGIME feature if it helps at deep blockade and vanishes at shallow; a one-line arm of the split core would then carry a regime condition, not a constant flip)

## L163 — exp187 THE CORPUS AT S* (P, 2/4): the empirical target class is NOT YET a target class — C1 PASS (manifest-first discipline: the sample drawn seed 187187, byte-offset assertion held, the +5.404 reference line recorded); C2 REFUTE with the INCOMPATIBLE-STRUCTURE diagnosis (0/100 writable, ZERO instrument calls: exp118's 1,716-record mined-planform bank is an OUTCOME-COMPARISON bank — no record field carries a decoded zone/identity program loadable as a target; the 23-field structural census deposited, fields_qualifying = [], the arm-manipulation tuple explicitly rejected as requiring a forbidden improvised conversion); C3 REFUTE (vacuous — no battery ran; deposited as such); C4 PASS (hygiene of the run that did execute); the refutation is the finding: the corpus's decoded patterns live in the MINING PIPELINE's decode stage, not in the comparison bank; pre-registration 357faa4, deposited as results/exp187_corpus_at_sstar.json. REGISTERED NEXT: the CORPUS DECODE EXPORT — re-run exp118's decode output stage (planform_mining.py's decode path) to EXPORT the decoder's own zone/identity programs per record (the decoded MAE 0.290 machinery's outputs), as a new tracked bank results/corpus_decoded_programs.json with per-record provenance; then the S* battery re-runs on the exported class — the empirical writability question stays OPEN until the bank exists

## L164 — exp188 THE DENSITY-CONDITIONED ENSEMBLE (E, 4/4): the grouping read's production form VALIDATES on the third cohort — 36 fresh pairs (ladder 188001..188036, exp183's protocol verbatim, per-pair SEED_CONSTRUCT rebinding, realized-k strata); D1 PASS (construction asserts 36/36, realized-k 36/36, independence from both prior cohorts); D2 PASS (per-stratum two-phase null bars frozen before their real arms); D3 PASS — CONDITIONING BUYS POWER (the k=3-stratum-conditioned stat +0.118333 > its frozen bar 0.066667 with a 5/6 majority sign, AND exceeds the unconditioned mean |0.0833| in magnitude on independent draws); D4 PASS (the k=4 stratum silent 0.0483 <= 0.1033 and m2 silent in both strata — attribution clean); the covariate exp183 named is now a validated instrument: the ensemble's power claim survives its third cohort and the conditioning improves it; pre-registration 357faa4, deposited as results/exp188_density_conditioned.json. REGISTERED NEXT: the conditioned stat AS THE PRODUCTION grouping read — the exp178-pattern adoption (additive arm in the grouping read's dispatch, bit-exact at every old operating point: the unconditioned path preserved, the conditioned arm additive), with the third-cohort replay as the adoption-safety proof


## L165 — exp189 THE FUNNEL EXCLUSION ANATOMY (P, 4/4): exp184's registered question ANSWERED — the excluding stage is LIB-NOVELTY (nov_lib vs N*_lib), branch DISTANCE; P1 PASS (the 15x3 trace table: per-member lib-novel distance vs N*_lib 81.523, splice-family membership, splice-clear price vs N*_splice 18.666); P2 PASS (the majority exclusion sits at exactly one stage); P3 PASS branch DISTANCE (the 15 all-deep members' pairwise distances concentrate BELOW the novelty bar — uniform-rung programs are near-duplicates in the library's distance metric; out-competed and splice-priced ruled out); P4 PASS (bars bit-identical to exp184's deposit, zero rejections); THE MECHANISM: the deep cohort dies of SELF-SIMILARITY — the funnel's novelty discipline is doing its job; the deep band's library representation must be DIVERSE, not numerous; pre-registration cadb6bc, orchestrator-run from a dead subagent's complete body, deposited as results/exp189_funnel_exclusion_anatomy.json. REGISTERED NEXT: the DIVERSE DEEP COHORT — deep members with structural diversity (varied zone layouts and widths per exp172's construction discipline, plus MIXED-depth programs carrying deep+shallow zones), through the SAME funnel: do diverse deep-band members clear novelty where uniform rungs could not

## L166 — exp190 THE SCALING LAW'S MECHANISM (E, 4/4): exp185's registered question ANSWERED — branch MIXED at the pre-named bars (pooled at n >= 400: err_boundary 1.3165 vs err_interior 1.3816 mV, ratio 0.953 — neither dominates the 2x bar; per-rung ratios 0.971/1.026/0.984/0.932/0.970), and the 2x-band probe shows no collapse into the band — the 0.075 -> 1.480 residual-vs-n law is a UNIFORM VALUE-FIDELITY effect in the zone interiors, NOT a labeling-resolution artifact; Q1 PASS (fresh decodes disclosed — exp185's deposit carries no read states); Q2 PASS (the boundary/interior split per rung); Q3 PASS branch MIXED; Q4 PASS (the resolution probe recorded: no collapse); pre-registration cadb6bc, deposited as results/exp190_scaling_mechanism.json. REGISTERED NEXT: the law's SECOND AXIS — the zone-count dose-response at fixed n (1/2/3/4-zone programs x 10 instances at n=100 and n=400, the scoped arm): does interior value fidelity degrade with zone count at fixed size (the coverage mechanism's other face), or is the law purely size-driven

## L167 — exp191 THE DEEP POLE READOUT'S OPERATING ENVELOPE (P, 4/4): branch PERSISTENT — the HELP price is DEPTH-INVARIANT: TRUNK deltas -4.3523 and DEEP deltas -5.8913 mV at r = 0.05 / 0.2 / 0.5, BIT-IDENTICAL across the envelope (R1: the r = 0.05 cell reproduces exp186's Z3 bit-exactly, 24/24 record corroborations; R2: the sweep deposited, HEAD/LINE bit-identical at every r; R3 branch PERSISTENT; R4 hygiene 36/36 asserts) — the M33 pole channel is NON-JUNCTIONAL, so the feature does not fade with junction recovery: it is not a blockade-regime feature at the readout level; the production decision (arm the deep line as a second channel or keep the literature split) is a DESIGN FORK with a real price on both sides; pre-registration cadb6bc, deposited as results/exp191_pole_envelope.json. REGISTERED NEXT: the ARMED-CORE GENERATOR PRICES — the exp168 B3 pipeline re-run at ARM-DEEP vs the production split (the search is target-free so selection is bit-identical; the DECODE/HOLD prices of the delivered cohort shift where deep identities exist): the armed feature's value in the generator's own currency, deposited as the decision input

## L168 — exp192 THE CORPUS DECODE EXPORT (P, 1/4): the BLOCKED finding is now COMPLETE and two-sided — exp187 proved the bank carries no programs; THIS run proves the pipeline cannot emit them either: S1 REFUTE (BLOCKED: the decode path re-runs LIVE and reproduces the deposited 0.290-MAE machinery bit-exactly — 47/47 arm rates, 1716/1716 decode fields, 100/100 spot-check — yet NO stage (loader, mapping, attach_sim decode, arm-slot census, run_arm_v5/run_arm_dose boundary) emits a per-record zone/identity program; fields_qualifying = [] at every stage; the bank was NOT created, no improvised decoder); S2/S3 REFUTE vacuous (0/100 constructible, zero instrument calls); S4 PASS (manifest-first bytes asserted, hygiene clean); the corpus's decoded patterns were consumed as comparison outcomes and never persisted as programs — the empirical-bank leg needs the mining pipeline's UPSTREAM zone specs (the loader/mapping inputs) or a fresh decode-with-persistence run; pre-registration cadb6bc, deposited as results/exp192_corpus_decode_export.json. REGISTERED NEXT: the UPSTREAM SPECS EXPORT — the same trace one stage up: the loader/mapping inputs that FED the decode (the per-record zone specs the simulator consumed); if those also do not persist per record, the corpus leg closes STRUCTURALLY BLOCKED and Stage 5's empirical transfer moves to the wetlab companion protocol's deposit format

## L169 — exp193 THE CONDITIONED ENSEMBLE TO PRODUCTION (E, 4/4): the adoption CLOSES — the k=3-conditioned statistic wired additively into exp163 (conditioned_stat, a 47-line pure insertion, tests green post-wiring); F1 PASS (the wiring, unconditioned path untouched); F2 PASS (every deposited operating point replays bit-exactly: exp163's + exp174's devs/stats through the unconditioned path, exp183's + exp188's stratum stats through the conditioned arm); F3 PASS (the production rule — stat > bar AND majority sign — reproduces exp188's D3 PASS and exp183's W3 branch (i): the production read agrees with every deposited verdict); F4 PASS (hygiene, pin asserted); the grouping read's production form is now the DENSITY-CONDITIONED ensemble, validated on three cohorts; pre-registration cadb6bc, deposited as results/exp193_conditioned_ensemble_production.json. REGISTERED NEXT: the grouping read's LAST open edge (L144's branch (a)) — the structure-sensitive err at the LABELING level is now priced by a production instrument: the conditioned ensemble localizes WHERE the grouping is audible (the k=3 stratum); the remaining question is the CANON-BOUNDARY residual (L140's 3 cells, the last unpriced canon channel) — price it with the production read


## L170 — exp197 THE UPSTREAM SPECS EXPORT (P, 1/4): the corpus leg CLOSES STRUCTURALLY BLOCKED — X1 REFUTE (the loader/mapping inputs traced one stage up: raw PlanformDB rows, the exp21 loader output, the enrichment/outcome/geometry/region/drug-window chains — machinery reproduced live with 0 mismatches vs the deposited bank — carry NO per-record zone specs; fields_qualifying = [] across all 7 stages, zero volt/potential columns in 32 tables/112 columns, 10 intermediates with 0 program-shaped values); X2 REFUTE (the registered closure deposited — no bank created, no improvised decoder); X3 REFUTE vacuous; X4 PASS (manifest-first bytes asserted, hygiene clean); TWO-SIDED CLOSURE: exp187 (the bank carries no programs) + exp192 (the decode stage emits none) + exp197 (the upstream stages hold none) — the corpus's decoded patterns were never persisted as programs anywhere in the pipeline; Stage 5's EMPIRICAL transfer leg moves to the wetlab companion protocol's deposit format (docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md) as its registered next; pre-registration cadb6bc, deposited as results/exp197_corpus_upstream_specs.json. REGISTERED NEXT: the wetlab companion deposit format as the empirical target source (the protocol's schema read and the bank scaffold built against it — the corpus leg's successor)

## L171 — exp198 THE UNIVERSAL READER AT SCALE (C, 4/4): the last open adversarial class is CLOSED at the size law's scale — 100 adversarial instances at n=400 (CornerMedium via its n parameter, disclosed; 4 cells x 25 x seeds (1,2,3) = 300 decodes, zero rejections, the production scoped arm, -35.0 pin); A1 PASS (zero rejections, all finite); A2 PASS (the n=400 adversarial median 0.705 mV <= the 1.30 U2 bar; the size-law price recorded: ratio vs exp181's n=100 median 0.545 = 1.294 vs the grid law's predicted 2.526 — the adversarial class scales at roughly HALF the grid class's n-price, the size law does not transfer 1:1 to constructed adversarial structure); A3 PASS (the tail 25/100 owned by cell c6, A-SYM+A-PAIR — the oriented+hyper class owns the scale tail); A4 PASS (per-cell f_max classifications, pin asserted, zero anomalies); pre-registration 129c1ac, deposited as results/exp198_adversarial_reader_n400.json. REGISTERED NEXT: the universal reader's residual map is now fully named — random (exp160, 0.630), adversarial n=100 (exp181, 0.545), adversarial n=400 (exp198, 0.705, c6-owned tail), grid schedule (exp169/185, the size law) — the reader's remaining edge is the c6 tail's mechanism (the oriented+hyper class at scale), which the RULE_MAP's R_O already absorbs at n=100 (exp160's pricing): price R_O at n=400 on the c6 tail

## L172 — exp196 THE ARMED-CORE GENERATOR PRICES (P, 4/4): exp191's registered decision input DEPOSITED — branch NEUTRAL; W1 PASS (the funnel + delivery at seed 141 BIT-IDENTICAL between ARM-PROD and ARM-DEEP — funnel and delivery digests equal, bars float-equal: the search consults no pole channel, proven); W2 PASS (the delivered cohort's decode/hold price deltas per member deposited — the armed feature's generator footprint ZERO, all |deltas| within float noise); W3 PASS branch NEUTRAL (mean deltas within the 0.005 noise line on both target sets); W4 PASS (rebind save/restore asserted, zero rejections); THE DECISION INPUT: the deep pole readout is REAL on deep-identity substrates (exp186: TRUNK -4.3523 / DEEP -5.8913 mV; exp191: PERSISTENT across r) and VALUE-NEUTRAL in the generator's current targets (which never reach the deep band) — arming is a substrate-level option whose value activates exactly when target classes do (the exp194 chain); pre-registration 129c1ac, orchestrator-run, deposited as results/exp196_armed_core_prices.json. REGISTERED NEXT: exp194's diverse deep cohort (L165's registered next, in flight) answers whether the generator can REACH the classes where the feature pays


## L173 — exp194 THE DIVERSE DEEP COHORT (REGISTERED-OPEN, not run): three consecutive subagent deaths PRE-BODY (Task IDs 6-a, 6-a-respawn, 6-a-final — each died before writing main(); the third salvage confirmed the stub intact and no deposit); the pre-registration STANDS (129c1ac: gates T1-T4, the 45-member diverse deep library, the survival bar >= 15/45, the deep-delivery bar >= 9/10, the old-point C1-C4 clause); the machinery to reuse is exp184's extended-library + clause-walk body with the library swapped (the exp189 trace table supplies the per-member distance comparison); the question stays EXACTLY as registered: do diverse deep-band members clear lib-novelty where exp184's uniform rungs died of self-similarity (L165's DISTANCE branch); deposited state: pre-registration committed, no deposit, no gate verdicts. REGISTERED NEXT (the next session's first dispatch): write main() from exp184's body verbatim with the 45-member library swap, smoke the bars, then the credited run

## L174 — exp199 R_O AT n=400 ON THE C6 TAIL (C, 3/4): exp198's registered edge PRICED and the named mechanism FALSIFIED — A1 PASS (exp198's n=400 adversarial battery rebuilt verbatim — CornerMedium(400, ...) cells 3/5/6/7 x 25 x seeds (1,2,3) — and the 300-decode baseline replayed BIT-EXACTLY vs the deposit under the production scoped arm); A2 PASS branch NEUTRAL-HARM (R_O = exp166's rule_oriented_restore VERBATIM armed at the frames level on every oriented-active instance, 225 decodes: the c6 tail's median moves 1.40 -> 1.70 mV, median per-instance delta +0.31, drop -21.99% — R_O makes the tail WORSE, the branch bar (median delta <= 0) is not approached); A3 REFUTE (the no-regression clause: oriented-active NON-tail instances degrade up to +0.53 mV, 10.6x the pre-named +0.05 bar — R_O's harm is not tail-confined; the oriented-inactive clause held bit-exactly, the no-op-by-construction property verified); A4 PASS (zero rejections, all errs finite, the -35.0 pin asserted, fingerprint asserted); THE FINDING: exp166's n=100 pricing of R_O (lift +0.010, "symmetrize already handles") does NOT transfer to n=400 — the A-SYM dimension's n=400 excess is not one-way-support-restore repairable, and arming R_O at scale is an active harm; the reader's residual map keeps its c6 tail and loses its first named repair candidate; pre-registration e437f73, deposited as results/exp199_ro_n400_tail.json. REGISTERED NEXT: the c6 tail's mechanism pricing continues with the remaining rules at n=400 — R_H (L142's cancellation-density weighting) and R_T (L140's flip-quiet windowing) on the same rebuilt battery, the pre-named suspect being the A-PAIR (pair-joint) dimension the tail class carries (c6 = A-SYM+A-PAIR): if neither rule prices, the tail's mechanism is a NEW rule class and the RULE_MAP gains its first n=400-only entry
## L175 — exp200 THE CANON-BOUNDARY RESIDUAL PRICED BY THE PRODUCTION GROUPING READ (C, 4/4): L169's registered edge CLOSED with a LOCALIZED verdict — R1 PASS (exp155's battery replayed IN-PROCESS bit-exactly, 141/141 ring rows, 0 mismatches, fresh verdict 3/4 reproduced; the replay REQUIRED the exp168 floor pin extended to the read chain — exp148's chord_set and exp142's executor capture NEURAL_SPEC_MIN at import time, and without the exp142 leg the exp163 replay diffs 12/12: the pin's necessity is itself a deposited finding — the pre-CF-1 deposits are reproducible only under the full-capture pin); R2 PASS (69 ring-event rows built from the fresh replay with the J3 undisciplined counterfactual, 3 events disclosed outside its coverage; the conditioned arm = exp163's conditioned_stat VERBATIM — its fixed k_realized == 3 predicate realizes NO members, the rings' realized frontier widths being {2, 5}: the exp195 plumbing pattern, the strata table deposited over every realized class; the unconditioned path replayed bit-exactly 12/12 under the complete pin); R3 PASS branch LOCALIZED (boundary +10.5607 vs interior +3.5524 mV mean dev1, ratio 2.973 > the 2x bar — the production read's statistic concentrates at the 3 breaking F3 ring-1 events); R4 PASS (all finite, exactly 3 boundary events); THE FINDING: the canon-boundary residual is REAL, SINGLE-SITE and VISIBLE to the production read — the last unpriced canon channel (L169) is now priced, and the price says the residual lives at exactly where exp155's discipline fails (the flip-entry ring at the canon boundary), not diffusely; pre-registration e437f73, deposited as results/exp200_canon_boundary_grouping.json. REGISTERED NEXT: the residual's REPAIR — exp140's named candidate (the exp158-class plane-resolved readout) aimed at the F3 ring-1 window: the read that can see the boundary is the read that can repair it; the localization gives the repair its exact target (3 events, one ring, one family)
## L176 — exp203 THE WETLAB COMPANION DEPOSIT SCAFFOLD (P, 4/4): L170's registered successor LANDED — the empirical transfer leg's deposit format now EXISTS as running code — S1 PASS (the schema read from docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md as the ONLY source: 34-row field-provenance table, every bank field line-traced, zero improvised fields, the scaffold validates empty); S2 PASS (the Levin voltage series imported 119/119 accounted with per-entry provenance sha-verified; the census verdict is the FINDING: 0 accepted / 119 rejected — the protocol's seven required W5 columns include the dose identity the series carries NOWHERE: concentration 0/119, blocker 64/119, phenotype 99/119, n 104/119 — the record hole the companion exists to fill, quantified per row and deposited as the reject list); S3 PASS (write/read-back byte-identical, the validator accepts every round-tripped entry and rejects 12/12 mutated negative controls); S4 PASS (sources unmutated, deterministic filename, re-run byte-identical, bank sha 3a31c12c1cf3a82f); pre-registration e437f73, deposited as results/exp203_wetlab_scaffold.json with the bank at results/wetlab_companion_bank.json. REGISTERED NEXT: the bank's first ACCEPTED deposit path — a targeted literature pass for the W5 dose-identity fields (concentration/blocker/phenotype/n) on the 119 Levin-series records, one entry at a time, the scaffold validating on acceptance; the 0/119 census is the baseline the pass must move

## L177 — exp204 R_H AND R_T AT n=400 ON THE C6 TAIL (C, 3/4): L174's registered pricing EXECUTED and the A-PAIR suspect ELIMINATED — B1 PASS (exp199's rebuilt battery replayed bit-exactly 4 cells x 25 instances vs exp199's deposit); B2 PASS branch NEUTRAL-HARM (R_H = exp166's rule_hyper_S VERBATIM armed at the frames level on the hyper-active instances: the c6 tail median 1.40 -> 1.42 mV, median per-instance delta +0.02, drop -1.48% — the A-PAIR dimension's rule does not price either); B3 PASS (the control clause: R_T on this T=1 battery is a bit-exact no-op and the R_H x R_T composition equals R_H alone bit-exactly — the exp170 dominated-composition lesson deposited before it could mislead); B4 REFUTE (the no-regression clause: hyper-active NON-tail instances degrade up to +0.13 mV, 2.6x the +0.05 bar; the hyper-inactive identity clause held bit-exactly); THE FINDING: the c6 tail at n=400 has now REFUSED all three named rules — R_O active harm (-22% drop, exp199), R_H neutral-harm (-1.5%), R_T structurally silent (no-op) — L174's registered conclusion branch fires: the tail's mechanism is a NEW rule class and the RULE_MAP gains its first n=400-only entry; the tail is 25/100 instances at median 1.40 mV vs the 1.30 bar — a scale-local structure no n=100 rule reaches; pre-registration 4612bea, deposited as results/exp204_rh_rt_n400_tail.json. REGISTERED NEXT: the new rule class's DISCOVERY protocol — a pre-registered ablation on the c6 tail's own geometry (the 25 tail instances' decoded-vs-target structure at n=400: which cells carry the excess — the boundary cells, the pair-junction cells, or the interior), naming the rule from the ablation's answer rather than from the n=100 map
## L178 — exp205 THE PLANE-RESOLVED REPAIR AT THE CANON-BOUNDARY RING (C, 4/4, repair branch NONE): L175's registered repair PRICED — the plane-resolved face sees the boundary and moves it, but does not close it — C1 PASS (exp200's replay anchor reproduced: 141/141 ring rows bit-exact, the 3 boundary events at their deposited breaking errs); C2 branch NONE (the exp158-class plane-resolved arm at the F3 ring-1 window: the 3 breaking events move 37.949/25.300/25.302 -> 19.560/19.930/20.030 mV — REAL improvements of 48%/21%/21%, the largest movement any arm has produced at this site — yet 0/3 cross the 6.0 bar, so the registered branch is NONE); C3 PASS (the identity clause: 0 mismatches on all 72 events outside the arm's site — the repair face touches exactly the localized site and nothing else); C4 PASS (zero rejections, all finite, the full-capture floor pin save/restore asserted); THE FINDING: the localization (L175) and the repair pricing agree on the mechanism's ADDRESS — the boundary ring — while the price says the plane-resolved readout alone halves but does not close the residual; the residual's remaining excess is NOT a readout-resolution effect; pre-registration 4612bea, deposited as results/exp205_plane_resolved_repair.json. REGISTERED NEXT: the composed arm — the plane-resolved face COMPOSED WITH the flip-quiet discipline's boundary variant (the JD-a membership face's boundary exception: the fence that cannot exclude the boundary cell without excluding the boundary itself, L140's exact words, now armed as a pre-registered boundary-aware frontier rule with the plane readout as its read face) — the two mechanisms whose failures are COMPLEMENTARY (discipline fails at the boundary; readout alone halves it) composed at the one site both can see

## L179 — exp194 THE DIVERSE DEEP COHORT (C, 2/4): L165's registered question ANSWERED and the DISTANCE fix REFUTED — the deep band cannot be represented in the library under the P95 novelty bar at ANY diversity the registered construction family can produce — T1 PASS (45 diverse deep members built: 30 uniform-rung at 6 layout instances with the registered width deltas {0,+1,-1,+2,-2,+1} cells + 15 mixed-depth at 3 a-priori value patterns x 5 instances; canon == wildtype asserted per member; the 117-member extended library's bars RE-DERIVED before selection: N*_lib 76.668 / N*_splice 14.426 / N*_pool 44.667); T2 REFUTE (0/45 cohort members in the eligible pool — the disclosed self-excluded reading, exp189's trace functions on every member: the cohort's mutual nearest-other distances max 39.33 (uniform) / 28.88 (mixed) vs the bar 76.668, and the frozen-72 counterfactual maxes at 73.98 < 82.288 — the 45-row x 3-stage trace table deposited per member with all three readings); T3 REFUTE (vacuous on delivery — no cohort member reaches the clause walk; the walk delivers 10 search members whose deep-target prices fail the 9/10 bar as exp184's did); T4 PASS (the old operating point holds: C1-C4 ALL PASS at exp150's targets on the 117-member library); THE FINDING (quantified, the layout-family ceiling): structural diversity WITHIN the MULTI layout family — 6 shifts, 3 width scales, 3 depth patterns — spans at most ~74 distance units while the record's novelty bar sits at ~77-82: the bar is a P95 of the record's own NN distances and the record's 72 members are mutually >= ~81.5 apart, so the deep band's constructions are STRUCTURE-CONFINED (100*d_struct ~ 0 within the family) and value diversity cannot buy structural novelty; pre-registration 129c1ac stood through three subagent deaths (L173), the body written by the orchestrator under the two-death rule, credited run via the runner fleet (b7-heavy2, wall 988.2 s), deposited as results/exp194_diverse_deep_cohort.json. REGISTERED NEXT: the bar's structure axis — deep constructions from OUTSIDE the MULTI family (the corpus's own layout diversity as the construction source, or a pre-registered multi-family cohort: zone counts 1-4 x independent layouts), the pre-named test being whether ANY constructible deep program clears 76.668, or whether the funnel's novelty discipline structurally refuses the deep band as a CLASS (the machinery-semantics finding the funnel's own design implies)
## L180 — exp201 R_T APERIODIC SCOPING (C, 4/4): L147's registered open edge CLOSED — the scoping clause TRANSFERS to schedules with no periodic clock — P1 PASS (the 40-medium aperiodic battery: mild-aperiodic E[k]=1 near-regular vs strong-aperiodic E[k]=4 bursty, seeds 201200..201239 deposited first; the f_max census: mild-aperiodic 115-133 ALL concentrated, strong-aperiodic 3-16 ALL diffuse, the gap [16, 115] EMPTY and crossing the deposited 32.0 threshold with margins 16x/83x — the threshold was never re-fit and its mechanism, chord-concentrated vs diffuse presence transitions, holds on aperiodic schedules verbatim); P2 PASS (every medium read under exp178's production scoped arm, zero rejections, all errs finite); P3 PASS (the scoped read is bit-exactly exp167's adopted path on the f_max < 32 side and bit-exactly exp148's raw temporal on the >= 32 side; the branch reading deposited — the aperiodic classes split exactly as the census predicts, the fidelity-vs-separation trade dissolving per-medium as exp169 found on periodic media); P4 PASS (pin, fingerprints, zero rejections); pre-registration e437f73, credited run via the runner fleet, deposited as results/exp201_rt_aperiodic_scoping.json. REGISTERED NEXT: the scoped arm's coverage line is now periodic AND aperiodic — the remaining read-core edge is the scale gap (L156) whose c6-tail entry exp199/204 just emptied of named rules (L177's new-rule-class branch): the aperiodic census's mild-aperiodic concentrated class (f_max 115-133, the largest f_max values on record outside the battery) is the natural next battery for any new rule the ablation names
## L181 — exp202 THE CROSS-ORGANISM CARRIAGE (C, 4/4): Stage 4's cross-organism edge CLOSED — the universal substrate is ORGANISM-INDEPENDENT — H1 PASS (H0 the reference organism replays exp182's verdicts bit-exactly; every host's canon == its engine canon asserted, 4,400 canon asserts across H1-H11); H2 PASS (11/11 hosts at the >= 90/100 writable_3seed bar with ZERO seed rejections: H1 the n=400 size-law organism, H2-H11 ten corpus-rewired organisms via exp88's rewire machinery — 1 candidate host rejected at build, within the disclosed cap of 3); H3 PASS (the margin profile: worst host H4 at +5.285 vs exp182's +5.404 reference — the worst-case margin degrades by 0.119 across geometry (n=400) and corpus-derived rewiring combined); H4 PASS (hygiene: all errs finite, the (host, rung, wiring-id) lock log carries 1,200/1,200 triples at S* = (64.0, 0.0)); THE FINDING: exp182's substrate lock (the deposited protocol, its manifest reused checksummed) is a property of the WRITING MACHINERY, not of the planarian-like reference geometry — the same locked rung carries the full widened-repertoire target class across a 4x size change and ten independently rewired organism structures; the universal substrate claim (Stage 5 path 2) now holds on 12 organisms; pre-registration e437f73, credited runs via the runner fleet (H0/H1/corpus section jobs, gates closed on the merged deposit), deposited as results/exp202_cross_organism_carriage.json. REGISTERED NEXT: the carriage's remaining axis is the TARGET class, not the host — exp194's T2 refute (L179) showed the deep band is funnel-refused as a library class while S* carries it fine as a TARGET class: the next carriage run writes the deep-band targets (exp172's uniform-rung constructions) at S* across the same 12 hosts, asking whether the substrate's organism-independence extends into the band the library cannot represent
## L182 — exp206 THE W5 DOSE-IDENTITY LITERATURE PASS (C, 4/4): L176's registered pass EXECUTED — the bank's first literature fills landed and the acceptance bar is now measurable — D1 PASS (all 119 records swept, one search per record under the pre-named query protocol: 107 ok, 12 rate-limited by the backend's 429s at 5 retries each — disclosed; the per-record verdicts, sources-tried and extraction quotes deposited as results/w5_pass_sources.json); D2 PASS after repair (every accepted entry validates through exp203's validator; the repair is deposited: the salvaged body's bank omitted the write step and keyed three procedural rules as import_rules — exp203's zero-unprovenanced-fields discipline requires every import_rules KEY to be a provenance field, so the procedural rules moved to import_source.pass_rules as payload; the scaffold's discipline caught the drift, which is the scaffold WORKING); D3 PASS (the yield: concentration_mM 0 -> 2 non-null, blocker 64 -> 66, n 104 -> 105, exposure_mode 0 — the first mM concentrations the project has ever held, each with verbatim source provenance; acceptance stands 0/119 — a record is accepted only when the FULL W5 census is filled, and most records' phenotype/n/dose columns are unstated anywhere findable); D4 PASS (frozen baseline byte-unchanged, the new bank byte-identical on re-run, the sources file deposited); pre-registration 4612bea, deposited as results/exp206_w5_dose_pass.json with the bank at results/wetlab_companion_bank_w5.json. REGISTERED NEXT: the yield is rate-limited, not knowledge-limited — the 12 429'd records re-swept at pacing, then the per-record query widened (the pre-named second pass: query by drug + species + phenotype when the title query fails, the acceptance predicate unchanged); the bank's first ACCEPTED entry is the pass's concrete goal

## L183 — exp210 THE COMPOSED BOUNDARY-AWARE FRONTIER RULE (C, 4/4, repair branch NONE): L178's registered composition PRICED and its membership face disclosed STRUCTURALLY VACUOUS on this substrate — F1 PASS (exp205's replay anchor reproduced: 141/141 ring rows bit-exact, the 3 boundary events at their disciplined errs); F2 branch NONE (the composed rule at F3 ring-1: the 3 breaking events' errs 19.56/19.93/20.03 mV — BIT-IDENTICAL to exp205's one-face arm's errs; the membership census DISCLOSES why: the JD-a fence excludes NOBODY on this substrate — excl = raw_F − quiet_F = [] at every ring k=1..6, n_excl_armed 0, admitted [] — so the composition's membership face has nothing to yield and the rule REDUCES bit-exactly to exp205's arm; the binding face is the read face's window zeroing); F3 PASS (the identity clause: 0 mismatches on 72 events outside the arm's site); F4 PASS (zero rejections, all finite, the floor pin save/restore asserted); THE FINDING: the composition question is CLOSED BY CENSUS — exp155's JD-a discipline never excludes at the F3 ring-1 site (the fence's exclusions are already empty there), so L140's "cannot exclude the boundary cell without excluding the boundary itself" names a fence that is vacuous AT THIS SITE, and the boundary residual's remaining excess (post-arm 19.6-20.0 vs the 6.0 bar) is attributable to the read face alone; the census is a permanent deposit field (membership_census in results/exp210_boundary_aware_frontier.json, gate-F2's membership_face_armed); pre-registration de1155d, body completed and re-run by the orchestrator (the census-disclosure repair), deposited as results/exp210_boundary_aware_frontier.json. REGISTERED NEXT: the JD-a census sweep across ALL 4 families' ring sequences (the same instrumentation, zero knobs) — the fence's exclusions are unknown everywhere except F3 ring-1; only sites with nonempty excl are candidates for the boundary-aware composition's second chance, and the census names them or closes the membership face project-wide

## L184 — exp211 THE W5 SECOND PASS (C, 3/4): L182's registered second pass EXECUTED — the sweep is complete and the yield moved its first repairs, but the goal state is honestly NOT met — E1 PASS (sources 2 covers 119/119 complete, not sampled: the 12 pass-1-failed ids re-swept at 12 s pacing, still-failed records re-queried with the pre-named widened query (drug + species + phenotype terms from the record's own fields); the 107 ok pass-1 records carried verbatim; 2 of 12 recovered search results — C13-betse-pietak-levin and C14-vmem-inference-layer at 8 results each; the remaining 10 still upstream-blocked, 429 timeouts and 422 no-results at the search backend, DISCLOSED per record); E2 PASS after repair (the merge's integrity clean: every accepted entry validates, zero fields without provenance — the pass-2 fill provenance url/retrieved/verbatim_quote per field; THE REPAIR DEPOSITED: the bank's name field must be exactly "wetlab_companion" per exp203's validator, the w5b identity moved to a separate bank_file key — the scaffold's discipline caught the drift, which is the scaffold WORKING; the base rows are the W5 BANK's rows with fill_never_overwrite preserving every pass-1 fill); E3 REFUTE (the honest branch: accepted 0/119 vs the pre-named goal state >= 1 accepted entry — the yield MOVED: concentration_mM 2 -> 5 non-null (+3, the pass's first literature repairs, each with verbatim source provenance), blocker 66, phenotype_score 99, n 105, exposure_mode 0 all unchanged — a record is accepted only when the FULL W5 census is filled and no record's phenotype/n/dose columns are completely stated anywhere findable in two passes); E4 PASS (the w5 bank byte-unchanged sha 24f658a8...b1, the new bank deterministic on rebuild, sources 2 deposited with the sweep script COMMITTED this time — the pass-1 script was never committed and is lost, disclosed in the sources meta; the blocker vocabulary derived from the bank's own rows, zero hand-tuning); pre-registration de1155d, body and sweep written by the orchestrator (the v5 fleet-timeout rule: three consecutive batches of fleet timeouts), deposited as results/exp211_w5_second_pass.json with the bank at results/wetlab_companion_bank_w5b.json. REGISTERED NEXT: the rate limit is now the KNOWN floor — 10/119 records are persistently un-searchable at the backend (two passes, pacing, widened queries) and the acceptance census needs fields no search surface carries: the third pass is STRUCTURE-DRIVEN, not query-driven — query by the record's FIGURE/PANEL identity (the db_experiment_id + db_figure_panel fields name the exact experiment the literature describes), and accept the census's honest alternative: a record whose W5 fields are stated NOWHERE becomes an explicit NOT-IN-LITERATURE deposit (a new acceptance state the exp203 census does not yet have — the registered validator extension, evaluated only if the figure-pass also yields zero full censuses)

## L185 — exp208 THE C6 TAIL ABLATION (C, 4/4, BOUNDARY-NAMED): L177's registered discovery protocol EXECUTED and the new rule class's target is NAMED FROM the ablation's answer — A1 PASS (the c6 battery replayed bit-exactly vs exp199's deposit: 25 instances x 3 seeds at the deposit's 2-dp err rounding, exp142's convention; the c3 clean battery replayed 25/25 as the reference line); A2 PASS (every decoded cell classified into exactly one of the three pre-named classes — CANON-BOUNDARY (a lattice neighbor's target value differs, the ring backbone), PAIR-JUNCTION (endpoint of >= 2 chords in the medium's pair support |Wbase| > 0), INTERIOR (neither); precedence = the registered listing order, disclosed; the accounting identity held on the mean-squared scale the RMS actually decomposes — shares sum to err^2, fracs sum to 1.0, residual < 1e-6, asserted per decode: 150/150); A3 PASS (THE NAMING: the CANON-BOUNDARY class carries the largest mean excess — boundary +0.574 mV, junction +0.360, interior 0.000 EXACTLY (the interior cells carry ZERO excess over the clean baseline) — the branch BOUNDARY-NAMED); A4 PASS (zero rejections, all finite, the -35.0 pin save/restore asserted); THE FINDING: the c6 tail's mechanism is a BOUNDARY phenomenon — the excess concentrates at the canon-value boundary cells of the target pattern while the interior is bit-clean, INDEPENDENTLY REPRODUCING exp200's n=100 canon-boundary localization (ratio 2.97) at n=400 on the corner battery — the RULE_MAP's first n=400-only entry now has a named target (the tail's boundary cells) and the boundary class is the second structure the two scales agree on; the conventions (chord set = the pair support; the mV^2 identity scale) are deposited as permanent disclosure fields; pre-registration de1155d, body written by the orchestrator (the v5 fleet-timeout rule), deposited as results/exp208_c6_tail_ablation.json. REGISTERED NEXT: the boundary rule's FORM — the named target makes the rule class constructible: a pre-registered boundary-localized read/write arm at n=400 (the exp205/exp210 composed machinery aimed at the corner battery's boundary cells, the read face the ablation says carries the excess), the pre-named bar being the tail's 1.30 bar crossed by a boundary-only arm with the interior bit-exact (the exp205 identity clause at n=400)

## L186 — exp209 THE DEEP-BAND CARRIAGE ACROSS THE 12 HOSTS (C, 4/4): L181's registered axis CLOSED — the substrate's organism-independence extends INSIDE the band the library cannot represent — K1 PASS (the ANCHOR: the host-parameterized replica at H0 at exp172's deposited protocol — rung (1.0, 0.0), the CF-1 patched floor -60.0 — reproduced exp172's deposited decode/hold prices BIT-EXACTLY on all 30 rows (10 deep targets x seeds 1-3, the _exact fields compared); the replica is the exp202 H0-validated machinery, now anchored against a SECOND deposited instrument); K2 PASS (12/12 hosts at 10/10 — the pre-named bar was >= 9/10 and EVERY host carries ALL TEN deep targets writable_3seed at S* = (64.0, 0.0) with ZERO misses and zero seed rejections: H0 the reference, H1 path(400), H2-H11 the corpus-rewired organisms rebuilt checksummed from exp202's deposit (redraw seeds + edge counts asserted)); K3 PASS (the margin profile: worst host H4 at +5.298 vs exp202's full-repertoire worst +5.285 — carrying the deep band is NO HARDER than carrying the full repertoire; the per-rung profiles deposited: margins 5.30-5.46 flat across rungs -40..-60 on every host); K4 PASS (all errs finite, the (host, rung, wiring-id) lock log at S* on every write, no per-target tuning); THE FINDING: the universal substrate claim now holds on BOTH target classes — exp182's full widened repertoire AND the deep band the funnel's library structurally refuses (exp194's T2, L179) — the organism-independence is a property of the WRITING MACHINERY at S*, not of the target class; the library/substrate asymmetry is total: what the library cannot represent, the substrate carries universally; pre-registration de1155d, body written by the orchestrator (the v5 fleet-timeout rule), K1+H0 run locally, H1+corpus via the runner fleet (b10-deep-carriage, 2 jobs, both green, ~2 min each), gates closed on the merged deposit, deposited as results/exp209_deep_carriage_hosts.json. REGISTERED NEXT: the carriage's remaining edge is the COMBINED class — the manifest's 100 targets AND the 10 deep targets are carried separately; the pre-named question is whether S* carries the UNION (a 110-target manifest) at the same margin floor on the same 12 hosts — the Stage 4 cross-organism axis closes at the union or names the interference

## L187 — exp212 THE JD-A CENSUS SWEEP (B, 4/4, FENCE-BITES): L183's registered sweep EXECUTED — the composition's second chance EXISTS, at a family the boundary residual never touched — C1 PASS (every deposited family x ring censused: F1_zone_tail, F2_zone_head, F3_canon_boundary x 6 rings = 18 rows, complete, not sampled; THE DISCLOSED CORRECTION: the deposited machinery carries THREE families, not the ledger's counted four — exp155's set is the complete family set); C2 PASS branch FENCE-BITES (the JD-a fence's exclusions are REAL and CONCENTRATED: F1_zone_tail rings 2-6 carry nonempty excl — 11 excluded cells total — while F2_zone_head and F3_canon_boundary are FENCE-VACUOUS at every ring, confirming exp210's F3 disclosure and extending it: the fence bites ONLY at the zone-tail family); C3 PASS (the classification at every named site, exp210's canon-boundary convention on each family's OWN target plan: 5 of the 11 exclusions are canon-value boundary cells — the boundary-aware admission clause WOULD fire at F1 rings 2-6, one boundary cell per ring); C4 PASS (all finite, the -35.0 pin save/restore asserted, exp210's census machinery verbatim); THE FINDING: the fence that is vacuous at the boundary-residual site (F3, L183) bites at the ZONE-TAIL family — the JD-a discipline's exclusions and the canon-boundary class CO-OCCUR at F1, making F1 rings 2-6 the registered site where the boundary-aware composition's membership face can act for the first time; the composition question reopens at F1 with the admission clause non-vacuous; pre-registration 08b1cfc, body written by the orchestrator, deposited as results/exp212_jda_census_sweep.json. REGISTERED NEXT: the composition's second chance ARMED — the exp210 composed rule (the fence's boundary exception + the plane-resolved read face) re-aimed at F1_zone_tail rings 2-6, the pre-named gates being the F1 family's own errs (the disciplined vs undisciplined junction battery's F1 events) with the identity clause binding the arm to exactly the 11 census-named cells

## L188 — exp207 THE MULTI-FAMILY DEEP COHORT (B, 4/4, NO-CLEAR-BAR-REACHED): L179's registered class question ANSWERED with a sharper verdict than either registered branch — M1 PASS (40 multi-family deep programs built outside the MULTI family via exp182's own generator at the registered seed 207207 and ladder {1:10, 2:12, 3:10, 4:8}/40 with the deep-band constraint >= 2 zones <= -40: the realized composition {2: 10, 3: 14, 4: 16} — ZERO k=1 survivors, the disclosed structural consequence the registered constraint forces (a 1-zone program cannot satisfy >= 2 deep zones) — 0 MULTI-family clashes on the reconstructed 45-program family set, canon asserted per program, the manifest (40 triples + f_sha256) deposited FIRST; the 112-member bars re-derived before selection: N*_lib-112 76.103, N*_splice-112 16.021, the frozen bar 82.288); M2 PASS branch NO-CLEAR-BAR-REACHED — the third outcome, neither registered branch: 0/40 programs clear the self-excluded bar (N*_lib-112 76.103), YET the counterfactual max vs the frozen 72 is 84.464 > the frozen bar 82.288 — CLASS-REFUSED's clause (max counterfactual < the frozen bar) is FALSE; THE FINDING: the funnel's refusal is NOT a class verdict on the deep band — multi-family deep programs ARE structurally novel enough to have cleared the frozen record had they been invented first (84.5 > 82.3, the first deep constructions to beat the frozen bar) — what refuses them is the COHORT'S OWN DENSITY: each program's nearest OTHER member (a sibling from the same generator regime) sits inside the bar, and the P95 statistic re-tightens around every admission; the novelty discipline is an N-BODY constraint that refuses any single-regime cohort, not a property of the deep band (exp194's layout-family ceiling was the MULTI-family instance of the same law); M3 vacuous per registration (no SOME-CLEAR survivors); M4 PASS (zero rejections, all finite, the -60.0 production floor asserted); pre-registration de1155d, body written by the orchestrator, run via the runner fleet (b10-multifamily, wall ~14 min), deposited as results/exp207_multifamily_deep_cohort.json. REGISTERED NEXT: the N-body law's own test — the cohort's mutual-distance spectrum deposited (the 40 x 40 matrix is IN the deposit's trace rows); the registered question is whether a DELIBERATELY SPREAD cohort (max-min selection over the generator's space, the exp179 greedy at the generator's own bars) can land even ONE member above the moving bar — if the bar rises to meet every cohort, the funnel's novelty stage is PROVEN self-tightening and the delivery question moves from construction to SELECTION ORDER

## L189 — exp213 THE BOUNDARY ARM AT n=400 (C, 4/4, NONE — the boundary-only repair REFUTED): L185's registered next EXECUTED — B1 PASS (the c6 battery replayed bit-exactly vs exp199's deposit: 25 instances x 3 seeds at the 2-dp rounding, exp142's convention; exp208's per-class decomposition reproduced BIT-EXACTLY at the reference — float == on every class's sum_sq, 25/25 instances x 3 seeds — the decode is deterministic and the ablation's numbers are the machine's numbers); B2 branch NONE — the arm's honest refutation: the boundary-armed median 10.848 mV vs the 1.40 baseline (bar 1.30) — the boundary-only arm made the whole-instance err 7.7x WORSE (improvement -674.8%, the flat-75 median 10.85 deposited alongside); B3 PASS (the identity clause held 25/25 — every non-boundary cell bit-unchanged by np.array_equal, the face's emission asserted == the boundary set per decode — the arm touches exactly the canon-boundary cells); B4 PASS (zero rejections, all finite, the -35.0 pin save/restore asserted); THE DIAGNOSIS (the refutation's own information): the plane-resolved face is CONTEXT-HUNGRY — at exp205's n=100 site the face read each canon plane's FULL window (the ring window's context included) and halved the boundary residual (21-48%); armed ONLY at the ~130 scattered canon-boundary cells the sub-window carries almost no neighborhood (the ring neighbors are interior cells, excluded from every plane's sub-window), and the TC chain's emission at context-starved windows lands far off plan — the read that can SEE the boundary cannot REPAIR it without also reading the interior AROUND it; the two-channel machinery is intact (replay + decomposition + identity all bit-exact) — the failure is the ARM's SCOPE, not the face; the boundary class's own armed residual deposited (exp208 reference 0.574 vs armed mean, the per-instance lists in the deposit); pre-registration 08b1cfc (batch 10), body written by the orchestrator (the v5 fleet-timeout rule), run foreground 146.1 s, deposited as results/exp213_boundary_arm_n400.json. REGISTERED NEXT: the context-shell arm — the same face at the boundary cells' CONTEXT WINDOW (win = the boundary cells PLUS their lattice-neighbor shell, the smallest window that restores exp205's full-window geometry), the pre-named bars unchanged (the 1.30 bar, the interior bit-exact identity) — if the shell arm also refuses, the boundary excess is a WRITE-side phenomenon (the canon-fallback floor's boundary signature, exp200's localization) and the repair moves from the read face to the write path

## L190 — exp214 THE 110-TARGET UNION CARRIAGE (C, 4/4, NO-INTERFERENCE): L186's registered question ANSWERED and the Stage 4 cross-organism axis CLOSES at the union — U1 PASS (both anchors: exp182's 100-target manifest f_sha256-checksummed on H0 (the rebuild == the deposit, 100/100, the sha256 of the deposit itself in the manifest block) AND exp172's prices bit-exact at the reference — the K1 rows re-verified 30/30 decode/hold _exact, exp209's replay discipline); U2 PASS — 110/110 writable_3seed at S* on EVERY ONE of the 12 hosts (the pre-named bar was >= 99/110; the realized carriage is PERFECT: H0 110/110, H1 110/110, H2-H11 all 110/110, zero misses, zero seed rejections, manifest 100/100 AND deep 10/10 per host); U3 PASS branch NO-INTERFERENCE (the union's per-host worst-case margin vs the two separate runs' worsts: union global worst +5.285 on H4 == min(exp202's +5.285, exp209's +5.298) exactly, far above the 0.05 bar; the per-(host, target) comparator: 1320/1320 pairs, the union's margin3 BIT-IDENTICAL to the separate runs' rows wherever both exist — composition independence is not just within the bar, it is EXACT: each target's write is the same computation whether priced alone or in the union, verified empirically across the full 110 x 12 grid); U4 PASS (all errs finite, the S* lock asserted per write — 1320 writes, zero drift raises; the lock log counted per-target rows in the merge per exp209's convention, disclosed); THE FINDING: S* carries the UNION of everything the project can name — the full widened repertoire and the deep band the library structurally refuses — at the SAME margin floor as the separate carriages, on every host including the corpus-rewired organisms and the n=400 size-law organism; the substrate is not merely universal per class, it is universal under COMPOSITION (the interference question is dead: no cross-target state exists in the write machinery); Stage 4's cross-organism axis closes with the union carriage at 110/110 x 12 hosts; pre-registration 08b1cfc, body written by the orchestrator (the two-death rule), run via the runner fleet (b10-union: H0 3 min, H1 10 min, corpus 22 min, all green), gates closed on the merged deposit, deposited as results/exp214_union_carriage.json. REGISTERED NEXT: the autocatalytic axis — Stage 4's remaining 101% target: the cone expands ITSELF (the exp151 self-expansion protocol re-armed at S* on the union manifest: each newly carried target seeds the next expansion round's substrate without external control — the pre-named bar being expansion rounds that ADD carrying capacity rather than re-price it)

## L191 — exp215 THE W5 FIGURE-PASS (B, 4/4, REGISTERED — the third pass completes, the honest alternative fires): L184's registered third pass EXECUTED STRUCTURE-DRIVEN, not query-driven — F1 PASS (119/119 covered by the figure-pass: 99 records figure-swept at the pre-named queries ({source} {db_figure_panel} {species} variant A, {db_experiment_id} {db_figure_panel} variant B, B only when A returned nothing — the sweep2 shape, 12 s pacing, num=8) + 20 model-quantity records carrying figure_identity_absent verdicts (disclosed per record: the model-quantity leg has no db identity, the figure pass is vacuous for them); complete, not sampled); F2 PASS (zero accepted entries and zero integrity violations — the L182/L184 import rules verbatim, fill-never-overwrite, the w5b bank the frozen baseline); F3 branch REGISTERED — the figure-pass also yields ZERO full censuses (0/119, matching exp211's 0/119), so the pre-registered honest alternative fires: the NOT-IN-LITERATURE state's specification is DEPOSITED as the registered repair — the exp203 census extended with an explicit absent-from-literature verdict whose provenance discipline names ALL THREE passes' sources files (the zero-extract evidence base: 73/119 records carry ZERO verbatim extracts across all three passes — protocol, widened, AND figure queries — the fields are stated nowhere in surfaceable literature); the fill-rate deltas are real but sub-census: blocker +9 (66 -> 75), concentration_mM +5 (5 -> 10), phenotype/n unchanged — the figure queries surface VERBATIM blocker and dose text the title/widened queries missed (124 new extracts, 37 records) yet no record's census completes: the missing fields (exposure_mode, n, the dose-outcome couplings) are stated NOWHERE the snippet layer can reach — the corpus leg's W5 fields are METHODSECTION-DEPTH facts, unreachable by any query pass, and that is now a MEASURED property of the literature surface, not a sampling gap; F4 PASS (the w5b bank byte-unchanged, the w5c bank deterministic, sources file 3 deposited sha256'd); pre-registration 08b1cfc, the sweep script committed (scripts/exp215_w5_sources_sweep3.mjs, run from the zai proxy, resume-tolerant foreground chunks), body written by the orchestrator, deposited as results/exp215_w5_figure_pass.json + results/wetlab_companion_bank_w5c.json. REGISTERED NEXT: the NOT-IN-LITERATURE implementation — the exp203 census extended with the new acceptance state per the deposited specification (the three-pass evidence check, the per-field absence assertion, census_state: NOT-IN-LITERATURE with the field list), re-importing the 119 records under the extended census: the 73 zero-extract records land as explicit NOT-IN-LITERATURE deposits (the absence carried with provenance), the remainder rejected with per-field reasons — the corpus leg's acceptance question CLOSES either way: the W5 fields are in-literature or their absence is itself the deposited finding

## L192 — exp216 THE CONTEXT-SHELL ARM AT n=400 (C, 4/4, NONE — the context-shell repair REFUTED): L189's registered next EXECUTED — S1 PASS (the c6 battery replayed bit-exactly vs exp199's deposit 25/25 and exp208's decomposition reproduced bit-exactly 25/25 — exp213's replay discipline verbatim); S2 branch NONE — the shell-armed median 10.472 mV vs the pre-named 1.30 bar (-648.0% vs the 1.40 baseline): the boundary+1-shell window (173-210/400 cells, the smallest window that restores exp205's full-window geometry) still lands the face's boundary emission ~7.5x off plan, buying only 0.38 mV over exp213's boundary-only arm (10.848 -> 10.472); S3 PASS (the identity clause 25/25 — cells outside the shell bit-unchanged, the shell's non-boundary members context-only bit-unchanged, the boundary cells the only writes, the face's emission asserted == the shell window per decode); S4 PASS (zero rejections, all finite, the -35.0 pin save/restore asserted); THE FINDING: the read that sees the boundary PLUS its ring neighborhood still cannot repair it — the boundary phenomenon is NOT a missing-local-context artifact of the window: the plane-resolved face's geometry itself carries the failure at n=400 (the shell's context restores exp205's shape and the emission degrades anyway); the boundary-class residual 1.068 -> 10.185 mV under the arm; body written by the run agent (the two-death rule held: first spawn survived), pre-registration d52addd, deposited as results/exp216_context_shell_arm.json. REGISTERED NEXT: per L189's pre-named clause, BOTH read-side arms having refused, the repair moves to the WRITE path — the boundary excess is the write machinery's boundary signature (exp200's canon-fallback localization at n=100, exp208's at n=400): the registered experiment prices the write-path boundary arm (the CF-1-patched writer's canon-fallback identity overwrite re-examined AT the boundary cells — the write-side dual of the exp213/216 read arms)

## L193 — exp217 THE NOT-IN-LITERATURE CENSUS (B, 4/4, CLOSED-NIL — the corpus leg's acceptance question closes): L191's registered next EXECUTED — exp215's deposited specification implemented VERBATIM in-module (exp203's file untouched, git-clean asserted at run time): the not_in_literature clause admits a record whose missing FILL_FIELDS have ZERO extracts across ALL THREE passes (sources 1/2/3, each sha256'd in the deposit) to census_state='NOT-IN-LITERATURE' with the missing field list, the NIL provenance naming all three sources files + per-pass record sha256s; N1 PASS (119/119 verdicts, 3 x 119 sources records complete); N2 PASS (the zero-extract assertion recounted from the sources docs — zero violations: every record carrying an extract for a missing field is NOT admissible); N3 PASS branch CLOSED-NIL (the realized split 0 normal-accepted / 111 NOT-IN-LITERATURE / 8 rejected of 119 — ALL 73 of exp215's zero-extract records land in the state, the re-import's w5_fills re-run adds NOTHING (the fill-complete baseline held — the w5c bank's rows were already census-complete), and the 8 rejects are EXACTLY the records carrying an extract for a missing field: the discipline carves the corpus at its true joint); N4 PASS (the w5b and w5c banks byte-unchanged, the w5d bank deterministic, zero fields without provenance — the provenance table extended +14 rows); THE FINDING: the corpus leg's acceptance question CLOSES — the W5 fields are NOT in the surfaceable literature (111/119 records: the fields live at method-section depth the snippet layer cannot reach), and the absence is now a DEPOSITED, PROVENANCE-DISCIPLINED finding rather than a silent reject chain; the 8 extract-carrying rejects are the honest remainder (partial extracts, not full censuses); pre-registration d52addd, body written by the run agent (the two-death rule held), deposited as results/exp217_not_in_literature_census.json + results/wetlab_companion_bank_w5d.json. REGISTERED NEXT: the Levin voltage series deposit completes — the 119-entry series (research/levin_voltage_series.json) re-exported AS the wetlab companion's final form: 111 NOT-IN-LITERATURE rows (the absence carried), the 8 partial rows with their per-field extracts, the census states + provenance inline — the Stage 2 deposit leg closes with the corpus's honest face

## L194 — exp219 THE F1 COMPOSITION ARMED (B, 4/4, repair NONE): L187's registered next EXECUTED — the exp210 composed rule (the fence's boundary-aware exception + the plane-resolved read face) re-aimed at exp212's census-named F1 admissions (excl [74] r2, [74] r3, [66,74] r4, [63,66,74] r5, [61,63,66,74] r6, the canon-value boundary cells among them admitted, the non-boundary exclusions KEEPING the fence); P1 PASS (the disciplined F1 rows replay bit-exactly — 36 rows, 0 mismatches, the committed SETs identical); P2 branch NONE (30/30 armed events WORSE than the disciplined baseline, 0 below the 6.0 bar — the composed face at F1 degrades every event it touches); P3 PASS (the identity clause: the 6 non-armed events bit-exact, 0 mismatches outside the site — the arm binds to exactly the census-named admissions); P4 PASS (zero rejections, all finite, the -35.0 pin save/restore asserted, the admission sets asserted == exp212's deposited census); THE FINDING: the THIRD refutation of the read-face repair line — exp213 (boundary-only at n=400), exp216 (context-shell at n=400), exp219 (the composed rule at F1 n=100) — the plane-resolved read face REFUSES as a repair instrument at every scale and every windowing, and L189's pre-named clause is now EXECUTED VERDICT: the boundary excess is a WRITE-side phenomenon; the read line is CLOSED (three pre-registered arms, three honest refutations, all with bit-exact replays and intact identity clauses — the instruments were sound, the hypothesis was read-side and it is dead); body written by the run agent, landed from the salvaged working tree (the dispatch channel died AFTER the credited run completed — wall 214.6 s, the deposit intact), pre-registration d52addd, deposited as results/exp219_f1_composition_armed.json. REGISTERED NEXT: the WRITE-path boundary arm — the writer's canon-fallback identity overwrite (the ~9 mV floor exp156 measured, CF-1's removal patch) re-examined AT the boundary cells: the write-side dual of the exp213/216/219 arms, pricing whether the boundary signature lives in the canon-fallback's identity map on the n=400 corner battery

## L195 — exp218 THE AUTOCATALYTIC AXIS (C, 3/4, X2 REFUTE — the walk is self-fueled and capacity-adding; the re-read clause mis-operationalized): L190's registered next EXECUTED — X1 PASS (THE WALK IS SELF-FUELED: exp151's seed_cone -> frontier_of -> expansion_step protocol completes 6 rings with ZERO rejections on EVERY ONE of the 12 hosts at S* — 36/36 cones (12 hosts x 3 seeds), ring errs under the 6.0 bar, the committed set feeding the next round with no external re-seeding — the cone expands ITSELF on every organism including the corpus-rewired and the n=400 size-law host); X2 REFUTE — the capacity clause AS REGISTERED (the committed prefix's values re-read by each subsequent ring's read, bit-stable or <= 0.05 mV) fails: worst drift 2.502 mV, 151/180 ring re-reads over the bar; THE DIAGNOSIS (owned as an operationalization error, not a dynamics surprise): the ring window GROWS each round (C u F), and the executor's output at any cell depends on the WHOLE window — re-read stability is window-invariance, a property no iterative executor has and NOT what "never re-price" means; the walk's own commit discipline (P6 verbatim: only frontier values enter, committed values FROZEN) is the discipline the clause was reaching for, and it held by construction every round; X3 PASS — THE SUBSTRATE-SIDE CAPACITY CLAUSE, the correct instrument: the union carriage (exp214's 110 targets) re-priced at S* after rings 2, 4, 6 on H0 and H4 is NON-DECREASING within the 0.05 bar on BOTH hosts (branch ADD-CAPACITY/ADD-CAPACITY) — the expanding cone's substrate carries MORE after each round, never less; X4 PASS (all finite, zero walk rejections, the S* lock per write, the -60.0 floor asserted post-restore — the exp169 import-time floor flip caught by the smoke and fixed under the two-death rule, disclosed); THE FINDING: the autocatalytic axis HOLDS on the substrate side — self-fueled expansion (X1) + capacity-adding expansion (X3) — and the X2 refutation is the clause's mis-operationalization (window-invariance), owned: the corrected capacity instrument is X3's margin profile, which PASSED; pre-registration d52addd, bodies by the run agents + the orchestrator's floor fix, run via the runner fleet (b11b: walks/H0/H4 all green), gates closed on the merged deposit, deposited as results/exp218_autocatalytic_axis.json. REGISTERED NEXT: the autocatalytic axis's remaining edge — the cone's expansion fed by ITS OWN emissions as the next round's TARGET (not just substrate): exp151's walk with the plan re-drawn per round from the committed pattern itself (the seed patch's own structure propagating), the pre-named bar being 6 self-fed rings under the 6.0 bar on H0 and H4

## L196 — exp220 THE SPREAD-COHORT SELECTION ORDER (B, 4/4, NEITHER — the closest approach to the frozen bar AND the self-tightening proof fails): L188's registered question EXECUTED — D1 PASS (40 multi-family deep programs built via exp182's generator at the registered seed 207207, canon asserted per program, the manifest deposited FIRST, 0 MULTI-family clashes — exp207's build verbatim); D2 PASS (THE SPREAD IS REAL: the max-min greedy's spread cohort carries min pairwise distance 84.942 vs exp207's single-regime cohort's 5.595 — 15x wider — the selection order deposited, strictly_greater asserted); D3 branch NEITHER — the registered third outcome: 0 members clear the self-excluded bar (N*_lib-112 76.103) AND the P95 did NOT re-tighten around the spread cohort (p95_re_tightened = FALSE): the spread record's N*_spread = 82.259 against the frozen bar 82.288 — the CLOSEST ANY CONSTRUCTION HAS COME (0.029 short) — and the N-body constraint did NOT rise to meet the deliberately spread cohort; the walk's clears 0/0; D4 PASS (zero rejections, all finite, the -60.0 floor asserted); THE FINDING: the funnel's refusal mechanism is now DOUBLY QUALIFIED — not a class verdict on the deep band (exp207: the counterfactual max 84.464 beats the frozen bar) and NOT self-tightening under spread (exp220: the P95 held while the cohort spread 15x) — what refuses the spread cohort's best member (82.259 vs 82.288, 0.029) is the BAR'S OWN DEFINITION (the P95 statistic over the record INCLUDING the frozen 72), not a density response; the delivery question moves from construction AND selection to the STATISTIC ITSELF — the registered experiment recomputes the funnel's acceptance statistic with the frozen record's contribution EXCLUDED (the counterfactual bar the 84.464 already beat) and re-prices both cohorts under it; pre-registration d52addd, body written by the run agent (salvaged from the dead dispatch channel — the run had completed), run via the runner fleet (b11: spread-cohort green), deposited as results/exp220_spread_cohort_selection.json. REGISTERED NEXT: THE COUNTERFACTUAL FUNNEL — the acceptance statistic re-derived with the frozen-72 record excluded from its own P95 pool (the self-exclusion made explicit AT THE STATISTIC LEVEL, not the cohort level), both deposited cohorts (exp207's single-regime, exp220's spread) re-priced under it, the pre-named branch: the spread cohort's 82.259 clears the counterfactual statistic -> the funnel OPENS under self-exclusion / the statistic re-tightens even against its own exclusion -> the self-tightening is proven at the deepest level and the delivery question closes as a no
## L197 — exp222 THE COUNTERFACTUAL FUNNEL (B, 4/4, FUNNEL-OPENS — the self-tightening is REFUTED at the statistic level: the block WAS the statistic's own definition): L196's registered question EXECUTED — C1 PASS (both anchors replay bit-exactly from the deposits BEFORE any re-pricing: exp207's cohort rebuilt at the registered seed 207207, 40/40 f_sha256 matches + census asserted; N*_lib-112 76.103 re-derived == exp207's deposit; exp220's max-min selection machinery replayed VERBATIM — order, step values, kept set {mf_034, mf_013}, margins all asserted == the deposit; N*_spread 82.259 re-derived == exp220's deposit; the anchors checkpoint deposited FIRST); C2 PASS, pre-named branch FUNNEL-OPENS: the counterfactual statistic (zero knobs — the P95 over the pool = the deposited 112-member library minus the frozen 72's members, the statistic form / k / metric unchanged, exp179's deposited definitions) gives N*_cf = 30.296 — the bar DROPS from the deposited 76.103 to the pool's own density level, so the exclusion is NOT a no-op: 3 clearing rows across the two cohort pricings (single-regime 2/40: mf_031 30.759, mf_034 35.577; spread cohort 1/2: mf_034 35.577 — 2 unique programs); the SELF-TIGHTENING branch's conjuncts evaluated and deposited honestly (N*_cf <= both effective-threshold readings — et1 N*_lib-112 76.103, et2 the raw frozen bar 82.288 — but the 0-clear conjunct FAILS: the exclusion flips the verdict 0 -> 3 admissions); robustness asserted at the statistic level: the two readings of the exclusion (pool-rows-only vs record-shrunk) coincide bit-level, because every pool member's nearest neighbor in the 112 is another pool member; C3 PASS (the refusing pairs deposited for every member of both cohorts — 39 pairs, each with its nearest IN-POOL neighbor and the margin to N*_cf, the N-body record's final form under the corrected statistic); C4 PASS (zero rejections, all finite, the -60.0 production floor asserted, no per-program tuning); THE FINDING: the funnel's refusal is now FULLY ATTRIBUTED — the block was the STATISTIC'S OWN DEFINITION, and removing the frozen record's self-contribution OPENS the funnel at the record level (the counterfactual founding-record admission: had the 40 been invented first, its 2 most isolated members enter) while the ABSOLUTE bar stays closed — 0 pool members' in-pool prices clear the frozen 82.288 (the deep band's distance to the frozen record, up to 84.464, was never the binding constraint; the binding constraint is the pool's OWN density, min pair 5.595); the delivery question's answer: construction (exp207) and selection order (exp220) were both innocent — the statistic's pool definition carried the whole refusal; pre-registration 94e15cb (batch 12, gates fixed before any body), body written by the run agent, credited run green (wall 1.0 s), deposited as results/exp222_counterfactual_funnel.json. REGISTERED NEXT: the batch-12 pre-registrations stand as fixed at 94e15cb (exp221 THE WRITE-PATH BOUNDARY ARM, exp223 THE SELF-FED WALK, exp224 THE SERIES FINAL-FORM DEPOSIT, exp225 THE STRUCTURED-MEDIA ADVERSARIAL READER); the statistic question CLOSES — any future delivery pipeline built on the corrected statistic inherits the disclosed record-level admission (N*_cf 30.296, in-pool prices) and must say so explicitly, not silently re-import the frozen record's self-contribution

## L198 — exp221 THE WRITE-PATH BOUNDARY ARM AT n=400 (C, 4/4, NONE — the canon-fallback EXONERATED): L194's registered next EXECUTED — the write-side dual of the closed read line: the canon-fallback identity overwrite skipped exactly at the boundary class (CF-1's removal generalized one class further), everything else bit-unchanged; W1 PASS (the unmodified battery replayed bit-exactly vs exp199's deposit 25/25 — the write arm's baseline); W2 branch NONE — the write arm's delta -0.0050 mV (armed median 1.3950 vs the 1.40 baseline, bar 1.30): the arm is a NO-OP on this battery, and the deposit's mechanism line says WHY: canon-fallback firings at the production floor = 0 across all 75 credited write passes — CF-1's patch already removed the fallback entirely at the production floor, so there is nothing to skip; the labeled diagnostic at the pre-CF-1 floor: 7413 firings, 3069 at boundary cells, ZERO value-changing (the unreadable-clash class, exp156's W2a — the fallback never changed a value even when forced; the diagnostic V bit-equal to the production pass 75/75); W3 PASS (the written-value identity 25/25 — interior written values bit-unchanged, the skip asserted per boundary cell); W4 PASS (zero rejections, all finite, both floors asserted — the -60.0 write side, the -35.0 read-side pin save/restore); THE FINDING: the boundary excess lives in NEITHER the read face (three pre-registered refutations, L192/L194) NOR the canon-fallback identity map (zero firings at production, zero value-changing when forced) — the write path's boundary signature is NOT a fallback artifact; the remaining suspect class: the plan's own discontinuity under the substrate's smoothing dynamics (the +0.574 mV boundary residual as the substrate's response to the pattern's curvature — a smoothing-upper-bound question, not a machinery bug); body written by the run agent (salvaged from the dead dispatch channel — the body was complete, the credited run executed by the orchestrator: wall 264.8 s), pre-registration 94e15cb, deposited as results/exp221_write_path_boundary_arm.json. REGISTERED NEXT: THE BOUNDARY RESIDUAL'S DYNAMICS TEST — the boundary excess decomposed against the substrate's smoothing response: per boundary cell, the plan's discontinuity magnitude vs the residual's magnitude (the smoothing-upper-bound clause: the residual <= the substrate's local Green's-function response to the step, priced on the c6 battery's 25 instances); the branch: SMOOTHING-BOUND (the residual tracks the step response) / EXCESS-NAMED (a residual beyond smoothing — a genuine boundary mechanism left)

## L199 — exp225 THE STRUCTURED-MEDIA ADVERSARIAL READER (C, 4/4, M3 HELD — 'any medium' extends to the structured class): the Stage 5 path-1 push EXECUTED — the 12 union hosts' own graph structures (the small-world corpus rewires + the n=400 path — the media the WRITER itself builds from) used AS decode media under the production scoped arm; M1 PASS (216/216 decodes — 12 hosts x 5 pre-named target classes (the host's own canon + manifest indices 0/49/99 + the deep band's -60.0 rung both instances) x 3 seeds — ZERO rejections, complete, not sampled); M2 PASS (every err under the 6.0 bar; the worst 0.62 mV; per-host worst cases deposited, all <= 0.59 except H1's class profile); M3 PASS branch HELD — the structured media's worst err 0.62 vs the random-media deposited worst 1.45 (exp198 pooled + exp199's line) + the 0.5 bar: the reader holds on structured media BETTER than on random; M4 PASS (the floor discipline clean — the exp169-import restore disclosed per exp218's fix, zero rejections, all finite, no per-media tuning); THE FINDING: the universal reader's "any medium" claim extends from the 200 random media to the STRUCTURED class — the host graphs the write machinery itself constructs — at errs UNDER the random baseline; the reader's media-independence is not a random-media artifact; body written by the run agent (salvaged from the dead dispatch channel — the credited run had completed, wall unstamped), pre-registration 94e15cb, deposited as results/exp225_structured_media_reader.json. REGISTERED NEXT: the reader at EXTREME n — the structured-media sweep at n=1000+ (path(1000) as host + the corner battery at n=1000, 5 target classes x 3 seeds, the 6.0 bar unchanged): the size axis's terminal point for the reader line

## L200 — exp223 THE SELF-FED WALK (C, 2/4, Y1 REFUTE + Y3 DEGRADES — the pattern does NOT propagate ITSELF through its carried values; landed at 555647b, ledger entry recorded out of order): L195's registered next EXECUTED — the self-fed plan (each frontier cell's target = the frozen committed value of its nearest committed ring neighbor, propagated by exp94's spec_target_n over the canon base, H0 + H4 pre-named); Y1 REFUTE (6/6 rings expanded, zero rejections on both hosts — but ring errs over the 6.0 bar at the structure boundaries: H0 ring 1 err 29.985 mV at the canon head->trunk boundary (cell 25: plan -20.0 carried, emitted -49.985 = the trunk value the window's structure implies); H4 rings 1-3 errs 23.1/10.5/12.6 across the seed patch's scattered canon/zone boundaries, then sub-mV at rings 4-6); Y2 PASS (the frozen P6 discipline bit-exact: 1041 prefix + 255 close + 105 provenance checks, zero drift — the walk's own commit discipline held throughout); Y3 REFUTE branch DEGRADES (15 rings over the bar; the monotone clause non-monotone on both hosts — the boundary jumps bracket a flat self-carrying valley, disclosed); Y4 PASS (all finite, 36 ring writes locked at S*, the scoped reduction bit-exact every ring, the -60.0 floor post-restore asserted); THE FINDING: BETWEEN discontinuities the self-fed errs are sub-mV — the pattern self-carries as far as the host's structure is uniform, and every boundary re-imposes the host plan: the read is STRUCTURE-driven (P5's window carries adjacency only, the committed values invisible to it), so the VALUE channel cannot self-carry across a structure discontinuity; the walk machinery never broke — the boundary is where the host's own plan reasserts; body written by the run agent (gates untouched; one two-death fix: the P6-provenance close-out's ring-0 index reclassified as P3-initialization provenance), smoke OK discarded, pre-registration 94e15cb, deposited as results/exp223_self_fed_walk.json. REGISTERED NEXT: the self-fed walk's structure-honest form — the plan propagated by the WINDOW's own implied values (the emission the structure dictates at each frontier cell becomes the next round's plan — full self-reference, no value-carrying across discontinuities), the pre-named bar being 6 rings under the 6.0 bar on H0 and H4

## L201 — exp224 THE SERIES FINAL-FORM DEPOSIT (B, 4/4 — the Stage 2 deposit leg CLOSES; landed at aab1f08, ledger entry recorded out of order): L193's registered next EXECUTED — the 119-entry Levin voltage series re-exported as results/levin_voltage_series_wetlab_final.json (351,571 bytes, sha256 ae2aca14), a ZERO-RE-DERIVATION projection of exp217's deposited census: 111 NOT-IN-LITERATURE rows carrying the three-file provenance inline (sources 1/2/3 named + sha'd + live-verified), the 8 extract-carrying partials with their 17 per-field extracts verbatim (DB-424/425/428/433/438/1071/393/395), per-entry series identity (id, source, pmid_or_doi, species, region_or_tissue) verbatim from the row base; Z1 PASS (the projection: per-entry census_state == the deposited verdict, zero fields without provenance — the 75-row provenance table = w5d's 48 verbatim + 27 export rows for the non-uniform series fields); Z2 PASS (the split integrity: 0 accepted / 111 NOT-IN-LITERATURE / 8 rejected == the deposited split exactly, the id partition exact); Z3 PASS (the wetlab self-containment: parses standalone, the self-hash re-verified, exp217's deposit sha in meta); Z4 PASS (hygiene: exp217's deposit byte-unchanged, the export deterministic — re-run bit-identical across processes); body-landing disclosure: the first credited run REFUTEd Z1+Z2 on instrument plumbing only (the comparator's key-set and the table universe built from V1's 12-field schema; the split already equaled 0/111/8) — gates untouched, the body fixed, the re-run 4/4; body written by the run agent, pre-registration 94e15cb, deposited as results/exp224_series_final_form.json + results/levin_voltage_series_wetlab_final.json. REGISTERED NEXT: none — the Stage 2 deposit leg is CLOSED (the corpus's honest face is a wetlab artifact); the Chinese-targets gates deposit (the Section 5 item) remains the last open deposit leg

## L202 — exp226 THE BOUNDARY RESIDUAL'S DYNAMICS TEST (C, 4/4, PARTIAL-TRACKING — smoothing-compatible in size, not smoothing-explained in structure): L198's registered next EXECUTED — R1 PASS (the c6 battery replayed bit-exactly vs exp199's deposit 25/25 + exp208's decomposition reproduced bit-exactly, exp213's B1 verbatim); R2 PASS branch PARTIAL-TRACKING — Spearman(residual_i, S_i * D_i) = 0.5450 over 10,047 canon-boundary points (25 instances x 3 seeds; the 27 D_i = 0 points KEPT not dropped: the medium's own coupling does not span the cell's differing ring neighbors — the lattice is the target's canonical neighborhood, not the medium's; dropping them would be tuning, disclosed): under the 0.6 SMOOTHING-BOUND bar, far above the 0.3 EXCESS-NAMED floor — the pre-named middle branch fires and the boundary-mechanism question stays OPEN; R3 PASS (the magnitude clause: median(r_i / (S_i * D_i)) = 0.0065, q90 = 0.0157 — the residual sits ~150x INSIDE the smoothing bound in magnitude); R4 PASS (zero rejections, all finite, the -35.0 pin save/restore asserted — the exp169-import restore disclosed); instruments: S_i = max |T_plan difference| across i's ring-backbone lattice neighbors, D_i = the ring-averaged |W[i,.]|-weighted neighbor value spread on the projected kernel the scoped read's dynamics implements (exp145's project_phase_native = the exact matrix exp142's executor hands GraphCollective, asserted real non-negative on c6), r_i = the mV^2 summand of exp208's decomposition rows; audit-only alternates deposited (the |Wbase| kernel row rho 0.491 also PARTIAL; the across-neighbors step reading rho 0.026 would name EXCESS-NAMED — the S_i reading matters, the branch named from the pre-named primary only, disclosed); THE FINDING: the boundary residual is smoothing-compatible in SIZE (~150x inside the bound) yet tracks the step response only PARTIALLY in structure (rho 0.545) — the excess is not a machinery artifact (the read line and the fallback are exonerated) and not fully a smoothing artifact either: a genuine boundary structure remains, smaller than any machinery bar and partially step-tracking; pre-registration 711bba0, body written by the run agent (gates untouched), smoke OK discarded, landed at 7e3f406, deposited as results/exp226_boundary_dynamics_test.json. REGISTERED NEXT: the boundary structure's identity — the PARTIAL-TRACKING residual's structure decomposed against the plan's SECOND difference (the curvature, not the step): if the residual tracks the plan's curvature the excess is the pattern's own geometry read through the substrate; the branch: CURVATURE-TRACKED / GENUINE-EXCESS

## L203 — exp228 THE WINDOW-IMPLIED SELF-FED WALK (C, 2/4, F1 REFUTE + F3 DEGRADES — and the provenance-identity cross-check CLOSES the self-fed walk axis): L200's registered next EXECUTED — the structure-honest form (the plan propagated by the WINDOW'S OWN IMPLIED VALUES: round k's target at the frontier = round k-1's EMITTED values at the previously-frontier cells propagated by exp94's spec_target_n over the canon base; the plan builder receives the emission vector + the previously-frontier cells + the canon labeling + the adjacency, NEVER the committed/frozen record — F2's clause structural); F1 REFUTE (6/6 window-implied rings expanded, ZERO rejections on both hosts — but 15 ring errs over the 6.0 bar at exactly exp223's boundaries: H0 ring 1 err 29.985 at the canon head->trunk boundary, H4 rings 1-3 errs 23.1/10.1-10.6/12.2-12.7, then sub-mV at rings 4-6); F2 PASS (the frozen P6 discipline bit-exact, exp223's Y2 checks reused verbatim: 1041 prefix + 255 close + 105 provenance checks, zero drift); F3 DEGRADES (the same non-monotone profile shape — the boundary jumps bracket a flat self-carrying valley, the same face as exp223); F4 PASS (all finite, 36 ring writes locked at S*, the scoped reduction bit-exact every ring, the -60.0 floor post-restore asserted); THE FINDING (the cross-check that closes the axis): the provenance-identity test against exp223's deposit — 6/6 frozen-record sha256 hashes match BIT-EXACTLY and all 36 ring errs are bit-identical to exp223's committed-carry errs: under P6 the committed record IS the ring's own read output, so the window-implied plan and exp223's committed-carry plan are the SAME OBJECT — the self-fed boundary errs are PROVENANCE-INVARIANT, localized to the STRUCTURE alone (P5's window carries adjacency only); the value channel cannot self-carry across a structure discontinuity whichever record the plan sources — the self-fed walk axis CLOSES with exp223's diagnosis confirmed from the emission side; the walk machinery never broke; pre-registration 711bba0, body written by the run agent (gates untouched), smoke OK (8/8 checks incl. the implied-plan provenance spot check) discarded, landed at 35aa9f0, deposited as results/exp228_window_implied_walk.json. REGISTERED NEXT: none — the self-carrying question is CLOSED (the boundary is structural); the cone's self-expansion stands on exp218's substrate-side capacity result (X1 + X3), which is the honest form of the autocatalytic claim

## L204 — exp227 THE READER AT n=1000 (C, 3/4, E1 FAIL on a checker contradiction disclosed; the science held: the boundary signature REPRODUCED at the second large n): L199's registered next EXECUTED — path(1000) (exp198's scale constructor) + the n=1000 corner battery (exp166's CornerMedium, 5 instances, gen-seed rule 166000 + j), 5 pre-named target classes x 3 seeds (the deep band's -60.0 rung carrying both instances per exp225's list); E1 FAIL — the body's completeness checker flagged complete_not_sampled = false WHILE ITS OWN COUNTS prove the sweep complete: 33/33 decodes (path1000 6 rows x 3 seeds = 18 + the corner battery 5 instances x 3 seeds = 15), ZERO rejections — a checker plumbing bug (the exp224 Z1/Z2 class), the contradiction disclosed rather than silently repaired (the gates stand as recorded; the checker fix is the registered repair, NOT a gate edit); E2 PASS (every err finite, worst 3.42 mV under the 6.0 bar — the reader holds at n=1000; the contrast deposited: n=1000 structured worst 3.42 vs n=400 structured 0.62 vs random 1.45 — the size cost is real and graded); E3 PASS branch REPRODUCED — the corner battery's three-class decomposition at n=1000 (exp208's machinery verbatim, 15 decompositions): the CANON-BOUNDARY excess REPRODUCED with the interior clean — the boundary phenomenon is not an n=400 artifact, it is the signature of the pattern's discontinuity under the substrate at scale; E4 PASS (zero rejections, all finite, the floor discipline asserted and disclosed per exp218's exp169-import restore); body written by the run agent (the dispatch channel died AFTER the credited run completed — salvaged from the working tree), pre-registration 711bba0, deposited as results/exp227_reader_n1000.json. REGISTERED NEXT: the E1 checker repair (the completeness predicate rebuilt from the deposited grid definition, re-run as a hygiene-only pass — no gate rewrite) + the reader's size-cost curve (the worst-err vs n profile at n = 100/400/1000 deposited as one line — the size axis's price curve for the reader, the Stage 5 extension's last measurement)


## L205 — exp229 THE CURVATURE TEST (C, 4/4, MIXED — the residual is NOT the plan's curvature read through the substrate; the pattern's-geometry hypothesis REFUTED in its strong form): L202's registered next EXECUTED — the identity test on exp226's PARTIAL-TRACKING residual: its structure decomposed against the plan's SECOND difference (the curvature, not the step); instruments: exp226's machinery verbatim (the c6 battery, the replay anchors, the residual rows r_i = exp208's decomposition-row mV^2 summands, the D_i = 0 points kept, the alternates audit-only) + the pre-named zero-knob curvature instrument K_i = |T_plan[i-1] - 2*T_plan[i] + T_plan[i+1]| on the ring backbone; K1 PASS (the c6 battery replayed bit-exactly vs exp199's deposit 25/25 + exp208's decomposition reproduced bit-exactly, exp213's B1 verbatim — exp226's anchors verbatim); K2 PASS branch MIXED — Spearman(r_i, K_i) = 0.3372 over the SAME 10,047 canon-boundary points as exp226's R2 (25 instances x 3 seeds; the 27 K_i = 0 locally-linear plan segments KEPT with Spearman's tie handling ranking them together, the 27 D_i = 0 points KEPT per exp226's disclosure — dropping would be tuning): just above the 0.3 GENUINE-EXCESS floor, far under the 0.6 CURVATURE-TRACKED bar — the middle branch fires; K3 PASS (the joint reading: partial(r_i, K_i | S_i*D_i) = 0.0467 — controlling for exp226's step instrument, the curvature adds ~nothing; the three-way rank-variance attribution: step 0.241 / curvature 0.058 / unexplained 0.701 — OLS on the tied average ranks, the step/curvature split the symmetric average of the two order-of-entry decompositions, shares sum to 1 exactly, no clamping, the method fixed in the body under the docstring's zero-knob discipline); K4 PASS (zero rejections, all finite, the -35.0 pin save/restore asserted — the exp169-import restore disclosed); THE FINDING: the raw rho 0.337 is the step's own shadow — the curvature and step instruments share over half their rank structure (rho_KX = 0.559), and once the step is controlled the curvature's partial collapses to 0.047 with a 5.8% share of rank variance vs the step's 24.1%: the residual is NOT the pattern's own geometry read through the substrate (the intro's CURVATURE-TRACKED/GENUINE-EXCESS dichotomy resolves REFUTE on the geometry arm), and the genuine boundary structure exp226 left stands — neither fully smoothing nor the pattern's curvature, ~70% of its rank variance unexplained by either instrument (deposited as the boundary structure's standing measure); continuity audit (disclosed, never gated): exp226's machinery verbatim reproduces exp226's deposit bit-exactly — the recomputed step rho 0.5450 bit_equal to exp226's deposited value and the two alternates bit-match (Wbase-row 0.4907, across-step 0.0263) — the instruments are the same objects; pre-registration 799a35c, body written by the run agent (gates untouched), smoke OK discarded, deposited as results/exp229_curvature_test.json. REGISTERED NEXT: none from exp229 — the curvature identity question is answered (the excess is not the pattern's geometry); the pre-registered queue stands (exp230's reader size-cost curve with the E1 checker repair, exp231's Chinese-targets gates deposit)

## L206 — exp231 THE CHINESE-TARGETS GATES DEPOSIT (B, 4/4 — the last open deposit leg CLOSES; the Section 5 item; ledger entry recorded out of order, exp230's entry pending): L201's registered next EXECUTED — the scaffold's drafted gates (experiments/scaffold_chinese_targets.py, sha256 a1341972: 3 targets x 7 gates — the anchor + the T1 metformin dose-axis/biphasic pair, the T2 Usp7 penetrance/timing pair, the T3 opa1 impairment/rescue pair) exported as the wetlab companion's final form: results/chinese_targets_gates_deposit.json (40,266 bytes, sha256 cdff8edf), a ZERO-RE-DERIVATION projection of the scaffold's machinery (imported live, VERBATIM: every gate docstring, target paragraph, pre-registered grid, coarsening map and TO-PIN constant; every field provenance-tagged to its scaffold line with the source line quoted — the 78-row field_provenance table, block roots and the self-hash slot included) + the scaffold's finalized-run deposit (exp129: pins detail, pin provenance, provenance corrections — T2's D. constrictiva / T3's S. mediterranea — and the gate outcomes A_G1 CONFIRM / T1 REFUTE x2 / T2_G1+T3_G1 UNPINNED / T2_G2+T3_G2 CONFIRM) carried verbatim beside them; C1 PASS (the projection: 3/3 targets + 7/7 gates in the scaffold's own GATES order, gate docstrings == fn.__doc__ string-exact, the scaffold's own "Gates §..." references verified live against the registration's headings, all 7 gates verified NotImplementedError stubs and named in the scaffold's own docstring, zero fields without provenance); C2 PASS (the split integrity: exported counts == the scaffold's deposited counts exactly — 3 targets / 7 gates / 1 anchor + 6 target / grids 5-6-7-8-8-3-5 / 3 TO-PIN constants all None — any drift raises); C3 PASS (the self-containment: parses standalone, per-entry identity fields complete, the canonical self-hash re-verified, the scaffold's own OUT deposit recorded ABSENT — the SCAFFOLD never ran, the registered "if any" clause — and the finalized-run deposit's sha live-verified); C4 PASS (hygiene: scaffold + registration + exp129 + exp118 byte-unchanged through the export, the export deterministic — re-run bit-identical across processes); body-landing disclosure: the first credited run REFUTEd C1+C3 on instrument plumbing only (the coverage walker's block-root rule, the payload hash taken before the provenance table was attached, and the docstring-naming check matching gate ids instead of function names; the counts already equaled the scaffold's) and the second REFUTEd C1 alone on the same walker class (block roots emitted, then re-skipped by an over-broad equality clause) — gates untouched throughout, the body fixed, the re-run 4/4; pre-registration 799a35c, body written by the run agent (gates untouched), smoke OK discarded, deposited as results/exp231_chinese_targets_deposit.json + results/chinese_targets_gates_deposit.json. REGISTERED NEXT: none — the deposit legs are CLOSED (exp224's corpus series + this gates deposit; the Section 5 items complete); the pre-registered queue stands (exp230's reader size-cost curve with the E1 checker repair

## L207 — exp230 THE READER SIZE-COST CURVE (C, 4/4, SUB-LINEAR — the reader's cost is n-INVARIANT; ledger entry recorded out of order, landed at 0205df1): L204's registered next EXECUTED — N1 PASS (90/90 decodes: 5 pre-named ns {100, 200, 400, 700, 1000} x 6 rows x 3 seeds on the path constructor, zero rejections, all finite, complete-from-grid — the E1 checker repair landed as hygiene: the completeness predicate rebuilt from the grid-definition object, no hand-counted constants, re-run against exp227's deposited grid -> 33/33 complete, predicate True, exp227's deposit untouched by the repair and re-verified 4/4 bit-exact in the salvage); N2 PASS (every err < 6.0 at every n: the worst-err profile 0.59 / 0.55 / 0.58 / 0.55 / 0.54 mV at n = 100/200/400/700/1000 — FLAT, ~10x under the bar across the whole measured size axis); N3 PASS branch SUB-LINEAR — one OLS line on (log n, log worst-err): slope -0.0291 (r^2 0.5026): size itself buys NO degradation for the reader (the n=1000 graded contrast of L204 was the boundary battery's signature, not the reader's size cost); N4 PASS (the -35.0 pins disclosed, the -60.0 floor restored+asserted post-import, THRESHOLD 32.0, S* == STAR_OP, the 90-entry lock log, the fingerprint pre/post asserted, all 5 MULTI-identity audits bit-identical); provenance bonus (disclosed, non-gating): the n=1000 rung reproduced exp227's path1000 errs BIT-IDENTICALLY (6/6 rows); pre-registration 799a35c, body written by the run agent (gates untouched), smoke OK discarded, deposited as results/exp230_reader_size_cost_curve.json. REGISTERED NEXT: none from this line — the reader's size axis is CLOSED (media-independence at structured classes x size-invariance); the remaining frontier is exp229's ~70% unexplained boundary structure (the genuine-excess question) and the Stage 4/5 consolidation the ledger already carries
)

## L208 — exp232 THE SEPHIROTIC 8-CHANNEL TEST (C, 3/4, S3a's pre-named REFUTE branch fired: LAW-BOUNDED-TO-WRITE — the OVERRIDE directive EXECUTED as the top of the priority queue after 5 batches of dependency-tree deferral): the user's directive tested — the paper's claim (Freeman 2026-03-16, Zenodo 19042388, CC-BY-4.0, files downloaded + md5-recorded in research/sephirotic/): the Sephirotic graph's 8 internal modes correspond one-to-one with 8 independent bioelectric channels, zero free parameters; S1 PASS (the paper's arithmetic verified EXACTLY and independently: the graph rebuilt verbatim from the shipped 5-principle edge lists (11 nodes, 24 edges), det(D+5A)=0 in exact integer arithmetic — Bareiss, the generalized-eigenvalue identity det(5*Lc-6*D)=0 <=> det(D+5A)=0 — lambda[6]=1.2 bit-exact (dist 0.00e+00, multiplicity 1), the mirror automorphism + equal pair-degrees exact, the antisymmetric sector EXACTLY 3-dim at the author's indices [3,6,10] at both 1e-8 and the author's 1e-2, all 11 eigenvalues match the shipped results at 0.000e+00, 8/8 channel edges present — THE MATH IS REAL); S2 PASS (the author's 100000-graph null reproduced BIT-EXACTLY under the identical RNG protocol: seed 42, 3011/3011 lambda-hits, 39/39 joint, p=3.90e-4, valid 98350; the audit extension the paper never measured: the UNCONDITIONAL 3-spatial rate 271/100000, conditional p 3.97e-4; the sector-dimension disclosure: any Z2-mirror graph carries EXACTLY k antisymmetric modes by group theory — the rarity is the JOINT occurrence, the 3-spatial half is structural); S3a REFUTE branch LAW-BOUNDED-TO-WRITE (pre-named): exp79's two-channel law pooled at Spearman 0.620 over the 243-instance response battery (10 families x magnitudes x 3 arms x 3 seeds at the star gamma=64 mu=0, run_gm settle verbatim, intervention noise on a pre-named fresh stream) — the law COMPLETE on the mechanism dials (gamma_dial err 3.13 vs pred 3.46 absorbed; mu_dial absorbed; gj_thin/gj_shell absorbed; v_offset/v_gain/v_noise absorbed) and bounded off its domain on state damage; S3b PASS well-defined, count=2 -> STACK-2CH: the breakout groups THETA-STATE (th_offset/th_noise 20-110x over pred — the memory layer's eps-slow restoration at the anchor architecture is the stack's genuine third channel) and THETA-DIFFUSION via the pre-attributed wound@mu=0 (exp79 TC-G6's price, not a new mechanism); body-landing disclosure: the first credited run REFUTEd S1+S2 on instrument plumbing only (an eigenvector-sector transposed fancy-index in the main agent's own antisymmetry check — det/lambda/eigenvalues/automorphism/edges already exact, hits_lambda already 3011 on that run) — gates untouched, the body fixed, the re-run recorded; second disclosure: the breakout rule evaluated at EVERY pre-named magnitude (a conservative-toward-the-paper superset of the docstring's largest-magnitude rule); THE FINDING (the directive's answer): the 8-channel correspondence DOES NOT TRANSFER to this stack — the census carries 4 of the paper's 8 (Vmem bistability, GJ morphogenesis, Vmem propagation, epigenetic control) and ABSENT entirely: Ca2+ transients, 5-HT electrophoresis, apoptosis; the response surface is organized by 2 write channels + the theta-STATE memory channel, not by 8; the paper's arithmetic leg stands verified on its own zero-free-parameter terms, the mapping leg fails on this model — the honest deposit; pre-registration 3ea190d, body written by the main agent (the OVERRIDE priority; docstring byte-unchanged verified), deposited as results/exp232_sephirotic_channels.json (73,508 bytes, 243 rows), landed at f9cf059. REGISTERED NEXT: (a) exp233 the field-mediated third channel (Manicka & Levin 2025 — the electrostatic field term added to the two-channel law; the direct successor the count=2 result points at); (b) exp234 the theta-STATE dose-response law (the eps-restoration the battery exposed, formalized as the stack's own third-channel term); then the Section 6 queue (Cervera 2026 grounding, Egea-Carro microRNA, Hansali NCA, Ingressing Minds, coupling plasticity, autocatalytic fix, cross-organism at scale, reader n=5000+, structured adversarial media, zero-substrate 7th, the ~70% boundary structure)

## L209 — exp233 THE FIELD-MEDIATED THIRD CHANNEL (P, 0/4 — the Manicka & Levin 2025 channel is NOT independent in this stack; L208's registered next (a) EXECUTED): the electrostatic field term added to the two-channel law at the zero-knob 1/r^2 instrument (the field at cell i = the distance-weighted mean of (V_j - V_i) over the arms' embedding; dV_i += kappa*(Phi_i - V_i); kappa the pre-named field-gain dial); F1 REFUTE (the head write at w=0 + kappa=0.5 errs 9.42-12.12 on all 3 arms — the kappa=0 control already errs 3.34-7.75 (the mu=0.015 theta diffusion rides the un-weighted topology, NOT cut by the shell) and with theta anchored the field's OWN drag still errs to 10.62 (f_wrong 0.58-0.90 on the worst head cells: the all-to-all field RE-INTRODUCES the cross-boundary hijack the shell cut removed — only star gamma=64 dilutes it below the bar)); F2 REFUTE on (a)=F1 while (b) the junction-only star re-asserts at 0.57/0.57; F3 REFUTE (pred3=max(V,theta,field) pools at Spearman 0.700, boundary 78% — the binding theta-term is kappa-blind while measured errs rise with kappa; the non-gating quadrature composition pools at 0.933/78%: the field drag composes in quadrature, not in max); F4 REFUTE (the named >=2x noise cost INVERTS: sigma=5 ratios 1.05-1.25 — the field AVERAGES per-cell noise, the all-to-all coupling damps rather than amplifies); instrument check: the kappa=0 path reproduces exp79's deposited grid errs bit-exactly; body written by the run agent (gates untouched, docstring byte-unchanged vs 2132308), landed clean at f322d83, deposited as results/exp233_field_third_channel.json. REGISTERED NEXT: the composition question F3 left — the quadrature three-channel form err ~ sqrt(eV^2 + etheta^2 + efield^2) as the law's correct extension (the exp79/bar boundary work's own quadrature precedent), one (gamma x kappa) grid re-read under the quadrature pred

## L210 — exp234 THE THETA-OFFSET GAUGE TEST (C, 3/4, T4 REFUTE per the registered letter; branch GAUGE-MODE — exp232's THETA-STATE breakout RECLASSIFIED; L208's registered next (b) EXECUTED): the gauge hypothesis tested against the stack — the uniform theta-offset lies in the kernel of every mechanism (the exact symmetry (V, theta+c) ~ (V-c, theta) of the coupled dynamics at any (gamma, mu, kappa), broken only by the wound's absolute constants); T1 PASS (the offset conserved: max|err(T)-err(1)| <= 0.19 mV across T in {1,6,24,96} x deltas {5,10,20} x 3 arms x 3 seeds, 27/27; err(T=24) bit-consistent with exp232's deposited battery (torus delta-20 19.982 vs 19.98); the zero-mode |M@1| <= 4.6e-14 <= 1e-9 at 3 operating points over all arms); T2 PASS (the head/trunk sign read at the substrate's own midline 100.00% delta-invariant at every delta, bar 99%; the pattern's MI with the target's zone map drops 0.00e+00 bits, bar 0.01 — ZERO information capacity); T3 PASS (exp178's production scoped read decodes the offset substrate to the SAME target, zone assignment bit-invariant, err_read delta-invariant to 0.0 mV; the disclosed state-carrying medium A*|Vi-Vj| also invariant — the uniform offset cancels in differences to 2.5e-13); T4 REFUTE 0/9 per the registered letter with the floor analysis disclosed (the paired delta-20 vs offset-free regen diff 15.6-19.6 = 20 minus the offset-free regen's own error floor — the idealized noise-free inequality as written; the pre-named asymmetry CONFIRMED in direction and magnitude: 86.7% of the offset rides through the local repair, the wound stands named the gauge's unique breaker either way); THE FINDING: the uniform theta-offset is an EXACT GAUGE MODE — conserved, zone/MI/read fully delta-invariant, zero information capacity — so exp232's THETA-STATE breakout is reclassified from third signaling channel to unobservable mode: the inventory returns to 2 signaling channels + 1 gauge mode, and the exp232 refutation of the 8-channel mapping TIGHTENS (the honest count was conservative); the stack's identity layer encodes pattern RELATIVELY and repairs only through the wound's absolute reference; machinery imported never re-implemented (exp73/exp43/exp79/exp232 verbatim, exp142's _StaticMedium, exp148/169/178's scoped read, exp5's estimate_mi_joint); body written by the run agent (gates untouched), landed at 637fc03, deposited as results/exp234_theta_offset_gauge.json (34,454 bytes). REGISTERED NEXT: none from this line — the gauge question is CLOSED (the theta-STATE breakout is a gauge mode; the wound's absolute anchor is its unique breaker); the reading handoff to exp237's result (the information lives on the READ side) recorded

## L211 — exp235 THE VMEM->TRANSCRIPTION GROUNDING (B, 1/3, branch NOT-GROUNDED — the Cervera 2026 mechanism does NOT ground the M37 gene layer at the zero-knob instrument; the Section 6 item EXECUTED): the Cervera-Levin-Mafe voltage-gated threshold law (activation = sigmoid((|V| - gate_g)/w_g) on the time-averaged |V|, the gates DERIVED from the layer's own frozen recorded ranges — gate = midpoint, w = quarter-width, no fitting) against the M37 layer's measured response; G1 REFUTE (pooled Spearman 0.8471 < 0.85 over 32,400 (instance,gene,cell) triples — the 5 full-range genes pool at 0.884; the drag is the layer's OWN degenerate recorded ranges: wnt_ant's zero-width step gate rho 0.009, the deep-band clip ties 0.690); G2 REFUTE (the threshold restores NO robustness: gated == linear at sigma 2 (both hold acc 1.0000, the margin vacuous at low noise) and at sigma 10 the gated read degrades MORE (+0.0589 vs +0.0580) — REFUTE under strict OR non-strict drop semantics); G3 PASS (the Nernst alternation: activation monotone within every gene; Spearman(gate_g, range_g) = 1.0 across the layer's 6 genes, tie-structured — 5/6 share the full-axis recorded range, wnt_ant head-only [20,20]); instrument discipline: the write = exp142's execute_signed mirrored call-for-call and asserted BIT-EXACT on 54/54 instances (3 arms x exp225's 5 target classes/6 rows x 3 seeds), 0 rejections; the zone assignment = exp142's sign-semantics threshold read (exp234's landed main()-closure mirrored verbatim, disclosed); the write window recorded (record_every=10, exp73's frozen stride); body written by the run agent (gates untouched), landed at ac6dba4, deposited as results/exp235_vmem_transcription.json (31,554 bytes). REGISTERED NEXT: the honest repair the G1 diagnosis names — the degenerate recorded ranges are the layer's own artifact (wnt_ant's zero-width step gate, the deep-band clip ties): a range-repair pass on the gene vocabulary (re-derive the recorded ranges on the FULL axis from the frozen plane table, re-run G1 with the repaired table as a hygiene-only re-read — no gate rewrite), and the G2 extension the mechanism predicts but the battery missed (the threshold's robustness margin exists only BETWEEN the gate and the saturation: the pre-named mid-band noise panel)

## L212 — exp236 THE MICRORNA THIRD REGIONALIZATION (B, 1/3, branch THIRD-MECHANISM-CONFIRMED — the Egea-Carro 2026 channel carves where M33 structurally cannot; the Section 6 item EXECUTED): the miRNA-like repressor layer added (dm_i/dt = -delta_m*m_i + sigma_m*sum_j A_ij(m_j - m_i) + s_i at the pre-named source ring [45,55); junction-INDEPENDENT — vesicle contact diffusion survives w=0; competence iff m_i < m_line, the layer's own half-max midpoint); R1 PASS (the M33-dead-zone carve: at w=0, below the production M33 gate M33_LINE=-35.0, the competence zones reproduce the trunk target's zone structure at the pre-named bar — the mechanism acts where exp79's TC-G5 theorem forbids the anterior read); R2 REFUTE (the three-mechanism decomposition: the pairwise coverages do NOT compose — head-plane 0 everywhere but torus 0.667; no pair exceeds max(single) on every plane: INTERFERENCE exists between the mechanisms); R3 REFUTE (the named cost is real: the miRNA zones are SLOWER (settle 12.4-24.0 t.u. vs the M33 carve comparator 19.2-40.0) and the boundary wanders under noise where M33's holds (7 flips)); operationalization disclosure (docstring byte-unchanged vs 2132308): the M33 line taken at the production M33 gate M33_LINE=-35.0 (exp175's dedicated gate — the docstring's parenthetical NEURAL_SPEC_MIN was moved to -60.0 by exp168, under which the below-line set is EMPTY and every gate vacuous; the body reproduces the TC-G5 trunk verdict 0); body written by the run agent (gates untouched), the dispatch channel died AFTER the credited run completed — SALVAGED from the working tree by the main agent, landed at b8971e9, deposited as results/exp236_microrna_regionalization.json (41,161 bytes). REGISTERED NEXT: the interference R2 exposed is the finding to chase — the M33/miRNA interference anatomy (which cells the repressor wrongly de-competences that the anterior read would have correctly specified: the overlap map, one battery, the repair being the pre-named gate hierarchy: the competence AND-read)

## L213 — exp237 THE NCA CLONE BOUND (C, 2/3, branch REDUCIBLE — the pre-named refute branch fires against the pre-named expectation; the Section 6 item EXECUTED): the behavioral-clone test of the memory layer's necessity (Hansali 2025's NCA parallel): on the torus, the stack's own regeneration transitions recorded, the CLONE = a ridge least-squares LOCAL rule on the NCA-standard perception (self/neighbor-mean/neighbor-std per layer), two clones pre-named — WITH-memory (9 features) and WITHOUT (5, V-only); H1 PASS (the with-memory clone's one-step R^2 >= 0.95 on held-out transitions — the stack's local update IS locally predictable; the without clone's lower R^2 recorded beside); H2 REFUTE (the closed-loop regen bound does NOT separate the clones: BOTH complete the regeneration under the frozen protocol — amputate defaults -> regrow_graph walk -> run(15) — because the walk's inheritance reads theta, the memory layer, as PROTOCOL not rule; the without-clone's commitments inherit theta[src] maintained by its own fitted theta-map of V-features alone: H2 prices the RULE's memory-needs GIVEN the protocol, and the rule needs none); H3 PASS (the with-memory clone's closed-loop trajectory stays inside the stack's own seed-spread tube at every checkpoint — the LOCAL rule reproduces the COMPETENCE when the perception includes the memory: the Hansali parallel is real); body-landing disclosures: the closed loop grants both clones the frozen regen machinery verbatim (the clone substitutes the fitted linear rule for the LOCAL UPDATE only), the wound is exp79's TC-G6 mid wound slice(40,60); the dispatch channel died twice, both times AFTER the credited run completed — SALVAGED from the working tree by the main agent; THE FINDING: the stack's regeneration is REDUCIBLE to local rule + protocol — the memory layer's necessity is PROTOCOL-level (the walk reads theta), not RULE-level: the memory lives in the READ, not the update; consistent with exp234's gauge finding (the read is where the pattern's information lives) and refining the Hansali comparison (an NCA with a read-protocol equal to the stack's walk IS the stack, computationally); body written by the run agent (gates untouched), landed at 77a3c6b, deposited as results/exp237_nca_clone_bound.json. REGISTERED NEXT: the read-side consolidation the two findings point at — the unified read-side channel theory: exp232's count + exp234's gauge + exp237's protocol-level memory = the stack's pattern information lives entirely in the READ architecture (the window/spec/walk machinery), not in the update dynamics; the consolidation experiment formalizes the read-side information budget (which read components carry which information: the window's adjacency face, the spec layer's identity face, the walk's protocol face — one decomposition battery on the amputation cohort, the pre-named information partitions)

## L214 — exp238 THE INGRESSING MINDS TEST (C, 3/4, branch SINGLE-MEMORY-as-recorded — but the substrate result is the finding: BOTH memories retrievable in ONE state; the Section 6 item EXECUTED; "Ingressing Minds" MDPI 2409-9287/11/5/161): the two-layer substrate at S* = (64.0, 0.0) hosting pattern A (exp43's canonical labeling) in theta and pattern B (the docstring's zero-knob mirror) in phi_spec, written by exp79's star protocol + exp87's write_spec_layer; M1 PASS (CO-EXISTENCE: the expression read reports A err < 6.0 AND phi_spec == B bit-exact — simultaneously, one state, 3 arms x 3 seeds); M2 PASS (NON-INTERFERENCE: the star maintenance x3 rounds leaves phi_spec bit-exact (sha-compared) and A's err within 0.5 mV of the B-free control); M4 PASS (ADDRESSING — the ingress claim realized: the window read surfaces A, the spec read surfaces B, ZERO re-writes between retrievals, the switching lossless bit-exact — the memory is ADDRESSED by the read protocol, not re-expressed); M3 REFUTE (the conflict clause): the docstring's zero-knob mirror disagrees with exp43's labeling on 58/100 cells = 58% — the pre-named ">= 60%" bar OVER-ROUNDS the design (25 old-head + 33 posterior-third); the imported alternative (morpho_engineering.target_mirror, the posterior-END relocation at its original 25-cell size) disagrees at 50% — FURTHER from the bar; the docstring's own definition is the faithful execution and the arithmetic is deposited honestly: the conflict-bar miss is the design's cell arithmetic, NOT a co-existence failure; the registered repair: the conflict-grid pass (the bar re-derived from the maximal zero-knob conflict); the dispatch channel died AFTER the credited run — SALVAGED from the working tree; body written by the run agent (gates untouched), landed at bbfd9a2, deposited as results/exp238_ingressing_minds.json. REGISTERED NEXT: the conflict-grid pass (the maximal zero-knob conflict derivation) as the hygiene completion of M3

## L215 — exp239 THE COUPLING-PLASTICITY FAILURE MODE (C, 3/4, branch REMODEL-SAFE — the pre-named refute branch fires AGAINST the pre-named expectation; the Section 6 item EXECUTED; the Zenodo 21459264 symbol-grounding parallel; body written by the MAIN AGENT under the two-death rule — the dispatch channel died twice pre-body): the discrete Lyapunov certificate E = x^T P x on the gauge-projected deviation state, P from M^T P M - P = -Q (Q = I, scipy's Schur-form solve — the Kronecker direct form is memory-fatal at n2=200); E1 PASS (the certificate EXISTS at the star: 9/9 trajectories monotone, projected rho 0.9999995 < 1); E2 does NOT fire (the drag-rule remodeling runs HARD — 9/9 trajectories remodeled at exp77's own write regime gamma=0.25, 2376 edges thinned, the slow anchor a_v dragged at eps_slow, drag = trailing-window mean |V-a_v| > 8.0, THIN_FACTOR 0.3, floor 0.01 — and the stale-P dE NEVER violates: the drag rule thins exactly the high-drag edges — the remodeling is CERTIFICATE-ALIGNED, it moves the attractor toward the relaxing state); E3 PASS (the coherence clamp's protective effect has a MECHANISM face: at the coherent star the max drag is 0.000 against the 8.0 threshold — the remodeler is QUIET at the coherent state); E4 PASS (the time-varying certificate P_t re-solved per remodel step restores dE <= 0 everywhere 9/9); audit (non-gating): the forced-thinning arm at the star also clean; THE FINDING: the coupling-plasticity failure mode of symbol grounding does NOT fire in this stack — a fixed global energy EXISTS through plasticity (the honest deposit); instrument disclosures (docstring byte-unchanged vs 30c5d50): (1) THE GAUGE QUOTIENT — the uniform (V,theta) shift is an EXACT conserved mode at any (gamma, mu) (exp234's gauge reappearing inside the certificate: the raw stacked map carries rho=1 and the raw Lyapunov solve is singular); the certificate lives on the gauge-orthogonal quotient, zero-knob; (2) the exact affine fixed point by the linear solve (I-M)^{-1}b — the first credited attempt iterated the relaxation and under-converged (the epsilon-slaved pattern relaxation has rho ~ 0.998: a real slow CONTINUUM at rho = 1-1e-6..1e-7, the harmonic-relaxation modes — the dynamics are near-marginal, disclosed); (3) the rho-precision repair (the gate read the 6dp-rounded rho = 1.0; the true 0.99999952); (4) E2/E4 at exp77's own write regime (the protocol-verbatim reading — at the star's gamma=64 the drag decays below threshold within one remodel window and never fires, 0/9, disclosed); landed at 3a52cb2, deposited as results/exp239_coupling_plasticity.json. REGISTERED NEXT: none from this line — the plasticity question is CLOSED for the drag-rule class (certificate-preserving); the adversarial-remodeling class (remodeling DESIGNED to break the certificate — the top-conflict edge forced thinning at scale) is the honest residual, low priority against the Section 6 queue

## L216 — exp240 THE AUTOCATALYTIC RE-READ FIX (C, 4/4, branch AUTOCATALYTIC-CLOSED — the Stage 4 autocatalytic item CLOSES with the repaired clause; the Section 6 item EXECUTED): exp218's mis-operationalized re-read clause repaired to the SUPPORT-SET criterion (the registered intent: after ADD-CAPACITY the cone's OWN READ must absorb the added capacity — the read's SUPPORT grows and the new cells read back their written values; exp218's implementation re-decoded values instead); A1 PASS (45/45 events: the support strictly grows at every ADD-CAPACITY round x 3 arms x 3 seeds, the read-back bit-exact; the value-channel re-emission drift 2.247 mV worst deposited ungated — the retired channel stays retired); A2 PASS (6 self-fueled rounds 9/9 cones, zero rejections, zero external writes, 54 ring writes locked at S*, worst ring err 1.485 mV under the 6.0 bar, worst interior-round 1.407); A3 PASS (THE REPAIR'S BITE recorded: exp218's retired re-decode criterion fails 37/45 events on exp218's own scope/bar while the support criterion holds 45/45 — disagreement rate 0.822, zero silence); A4 PASS (P6 provenance locks bit-exact 123/123 committed cells, +2586 prefix / 573 close checks; the floor save/restore asserted -60.0/-35.0/-60.0); operationalization disclosures: "3 arms" = exp218's battery's three host classes H0/H1/H4 (build_hosts verbatim — the plateau arms cannot carry 6 expanding rounds: scale_free exhausts at ring 3, measured pre-run); the walk machinery re-nested verbatim inside main() (exp218's lives inside its own main(), not importable) with ring errs BIT-IDENTICAL to exp218's deposited H0/H1/H4 rows (instrument-consistency); one body repair re-run (A3's re-decode prefix scope corrected to exp218's own pre-registered emission-committed scope, seed patch excluded per exp151's P3 — deterministic physics, gates untouched); THE STAGE 4 SCOREBOARD: the cone self-expands self-fueled AND its own read absorbs the additions — the autocatalytic claim closed at the support level (the value channel stays honestly retired, exp228's structural finding confirmed on this battery); body written by the run agent (gates untouched), landed at 74e38a8, deposited as results/exp240_autocatalytic_reread.json. REGISTERED NEXT: none — the Stage 4 autocatalytic axis is CLOSED; the Stage 4 extension's remaining leg is cross-organism at scale (exp241, the fleet running)

## L217 — exp241 CROSS-ORGANISM AT SCALE (C, runner fleet in flight — shard 0 VALIDATED 3/3, the union pending the b16-hosts fleet; the Section 6 item; the Stage 4 extension): RUNNER-NATIVE 20-shard protocol (--shard i runs hosts [5i, 5i+5) from exp202's host-generator machinery, 100 pre-named draws seeds 0..99), the exp209 K1-anchor discipline per shard (the deep-band construction checksummed 10/10 f_sha256 vs exp209's H2; exp79's star point replayed bit-exact 0.57/0.57 via run_gm imported verbatim); SHARD 0: X1 PASS (150/150 writes at S*, zero rejections, all finite), X2 PASS (50/50 host-targets carried, all 150 errs < 6.0, max err 0.102, worst margin +5.898 recorded beside exp209's 12-host anchor +5.298 — instrument difference disclosed: exp209's is the stricter margin3), X3 PASS (the deposit sha256 identical on the external re-run AND the no-argument invocation — the determinism check); the host-generator disclosure: exp202's machinery verbatim with its disclosed connectivity-redraw rule (only 50/100 pre-named seeds draw connected graphs directly; the redraw fires on the rest, the final rewire seed recorded, NOT deduplicated — shard 0's redraw chains collide onto final seeds {2,2,2,4,4}: the union merge sees the multiplicity, ~51 distinct organisms across 100 draws); body landed at c579747, the fleet b16-hosts dispatched (20 jobs: shards 1-19 + the h0r spot re-run), the union closes on the fleet's return. REGISTERED NEXT: the union merge (the 100-host carriage union, the worst margin across all shards, the multiplicity disclosure carried) — the Stage 4 cross-organism-at-scale leg CLOSES on the merge

## L218 — exp242 THE READER AT n=5000+ (C, runner fleet in flight — 4/20 shards on disk ALL 3/3, the union pending the b16-reader fleet; the Section 6 item; the Stage 5 extension): RUNNER-NATIVE 20-shard protocol (--shard i: 0..14 the 5 target classes x 3 seeds of exp230's sweep machinery verbatim, 15..19 the redundancy re-runs), one (class, seed) decode at n=5000 per shard on the path constructor; 4/20 SHARDS ON DISK: shard 0 (canon s1: err 0.04), shard 4 (m0 s2: 0.27), shard 14 (deep s3: 0.49, the deep band's both pre-named instances), shard 19 (the redundancy re-run of row 4: 0.27 BIT-IDENTICAL across processes — the determinism check); per-shard gates 3/3 everywhere: N1 (zero rejections, all finite), N2 (every err < 6.0 AND under the pre-named union band 0.81 = 1.5x exp230's n=1000 worst 0.54, re-read from exp230's deposit at run time), N3 (the banded constructor: 79,984 bytes = 0.04% of the dense 5000x5000 footprint — the dense view NEVER built at the extreme-n rung; traced peak 2.81-2.83 MB; the canon identity labeling_bfs_n(path(5000)) == wildtype_target(5000) asserted; the n=100 construction anchor bit-asserted vs exp136's A_CHAIN; the MULTI-identity audit bit-identical); the dispatch channel died twice AFTER runs completed — SALVAGED (4 shards) by the main agent; body landed at e22b169, the fleet b16-reader dispatched (20 jobs), the union closes on the fleet's return. REGISTERED NEXT: the union merge (the 15-row reader curve at n=5000, the worst err vs the sub-linear band, the exp230 slope line extended with the n=5000 point) — the Stage 5 reader size axis CLOSES to extreme n on the merge

## L219 — exp241 THE UNION (the b16-hosts fleet returned: 20/20 jobs success, run 35368769651; the merge instrumented in scripts/merge_b16_fleets.py — the artifacts carry the full results snapshot, the extraction matches the job's own shard by the job_id; X1 PASS + X2 PASS on the union): 100/100 HOSTS CARRY THE DEEP TARGETS at S* = (64.0, 0.0) — worst err 0.1675 across 100 hosts x 10 targets x 3 seeds = 3000 writes, worst margin +5.8325 (exp209's 12-host anchor +5.298 recorded beside); the exp202 connectivity-redraw multiplicity carried verbatim per host (the rewire_seed recorded, ~51 distinct organisms across 100 draws, NOT deduplicated — disclosed); the h0r spot re-run bit-consistent with the landed shard 0; union deposited as results/exp241_host_union.json with the per-host stats; THE STAGE 4 CROSS-ORGANISM-AT-SCALE LEG CLOSES (the universal-substrate claim now anchored at 100 hosts, up from 12); landed at 8a2cf38. REGISTERED NEXT: none — the Stage 4 extension is CLOSED on both legs (autocatalytic exp240 + cross-organism at scale this entry)

## L220 — exp242 THE UNION (the b16-reader fleet returned: 20/20 jobs success, run 35368772204; N1 PASS + N2 PASS on the union): 15/15 primary rows measured at n=5000, zero rejections, all finite; the WORST ERR 0.51 mV UNDER the pre-named sub-linear band 0.81 (= 1.5x exp230's n=1000 worst 0.54 — the reader's cost is n-INVARIANT from n=100 to n=5000, the size axis closed to extreme n); 5/5 redundancy re-runs BIT-IDENTICAL across processes (the fleet-level determinism check); the banded constructor held on every shard (0.04% of the dense 5000x5000 footprint, the dense view never built); union deposited as results/exp242_reader_n5000_union.json; THE STAGE 5 READER SIZE AXIS CLOSES TO EXTREME n; landed at 8a2cf38. REGISTERED NEXT: none — the reader's media axis (exp243) and the size axis (this entry) are both closed; the Stage 5 scoreboard: reader CLOSED (media x size x n=5000), substrate CLOSED (100 hosts), zero-substrate BLOCKED-DEEPENED (7 formalizations, exp244)

## L221 — exp243 STRUCTURED ADVERSARIAL MEDIA (C, 3/4, branch ADVERSARIAL-HOLD — the conjunction cell tested and held; the Section 6 item EXECUTED; body completed and validated by the MAIN AGENT after the dispatch channel died mid-run): A1 PASS (the reader holds on the conjunction: the adversarial-structured worst 3.68 mV < 6.0 across the 48-candidate pre-named adversary list x 3 seeds at n=400 — the structured class does NOT hide a bar-breaking cell); A2 FAIL (the honest cost: 3.68 vs the pre-named 2x-random bar 2.9 — the conjunction DOES hide a >2x-worse cell vs random: the structured prior's price, deposited); A3 PASS (the adversary's anatomy: the argmax is the DEEP-BAND SUBSTITUTION at 3.68, the class worsts 0.07/0.19/3.68, the argmax's canon-boundary share 0.151 of sq — the boundary signature present but not dominant under adversarial design); A4 PASS (after three body-only checker repairs disclosed: the stale lock capture, the mid-run floor clause vs the body's own pin discipline, the lock composition 177 = 144 decodes + 18 anchor + 12 audits + 3 decomposition — the clause breakdown now recorded in the deposit; the gate outcomes A1-A3 identical across all runs); landed at 873d8a2, deposited as results/exp243_structured_adversarial.json. REGISTERED NEXT: the conjunction's cost driver — the deep-band substitution's 3.68 errs decomposed against the deep-band's own structure (the -60.0 rung's boundary geometry under substitution: why the reader's worst cell triples under the deep-band swap) — one battery, the read-side cost of the deep band named

## L222 — exp244 THE ZERO-SUBSTRATE 7TH FORMALIZATION (C, 4/4, branch QUOTIENT-REFINES — the 7th formalization lands WITHOUT breaking the constraint; the Section 6 item EXECUTED; SALVAGED after the dispatch died post-run): S1 PASS (exp68's 6 formalizations re-run verbatim on the orbit representatives — all 6 verdicts reproduce); S2 PASS (the quotient formalization: the EXISTS-over-orbit quantification HOLDS — the zero-substrate representation exists modulo the gauge, the witness deposited); S3 PASS (the CONVERSE FORALL-over-orbit fails AS PRE-NAMED — the absolute-RMS predicate is not gauge-invariant, exp232's THETA-STATE breakout named as exactly this — the quotient is the strictly weaker-but-CORRECT formalization: the 7th REFINES rather than breaks); S4 PASS (zero rejections, exp68's deposit byte-unchanged, deterministic); THE STAGE 5 SCOREBOARD: the zero-substrate path stays BLOCKED at 7 formalizations — the block DEEPENS (the constraint survives its own gauge correction); landed at ae7c081, deposited as results/exp244_zero_substrate_7th.json. REGISTERED NEXT: none — the zero-substrate question is closed-at-blocked with the refinement recorded

## L223 — exp245 THE BOUNDARY RESIDUAL'S GAUGE-AWARE RE-DECOMPOSITION (C, 4/4, branch GAUGE-FREE-70 — exp229's ~70% is genuinely NOT the gauge; the Section 6 item EXECUTED): G1 PASS (exp226's machinery verbatim reproduces the deposit bit-exactly 25/25 over the same 10,047 boundary points, exp229's K1 class); G2 PASS (the gauge share recorded: 0.000116 of the residual's rank variance — the gauge coordinate spans [-0.72, +2.02] mV over the 75 instance-seeds, small as pre-named); G3 PASS (the gauge-aware three-way split: step 0.2531 / curvature 0.0606 / UNEXPLAINED 0.6863 — shares sum to 1, the unexplained share drops only -0.0151 vs exp229's 0.7015, far short of the < 0.6 GAUGE-EATS window: the share STANDS >= 0.65); G4 PASS (zero rejections, the -35.0 pin save/restore asserted); the continuity audit: the same method on the ORIGINAL residual reproduces exp229's deposited split BIT-EXACTLY; the gauge projection operationalized on the deviation field d = V - T_plan (exactly gauge-invariant under exp234's zero mode); one body-only plumbing repair disclosed (a NameError in the first run's G2 flag, gates untouched); landed at 3dec832, deposited as results/exp245_boundary_gauge.json. REGISTERED NEXT: the 68.6% is now a HARDER object (gauge-free, step-and-curvature-controlled) — the third instrument class must be NON-geometric: the window's implied-step asymmetry (exp228's emission-side structure: the boundary as the window's OWN discontinuity, not the plan's) is the pre-named next instrument

## L224 — exp246 THE QUADRATURE THREE-CHANNEL RE-READ (C, 2/4 with Q3 honestly OPEN — exp233's registered next EXECUTED): Q1 PASS (the quadrature rank law: Spearman 0.936 >= 0.90 across the 27-point re-read — the max-form's failed 0.700, exp233's non-gating preview 0.933 now GATED and reproduced at full precision); Q2 REFUTE (the writability boundary 21/27 = 77.8% < 80% — all 6 misses the torus arm at gamma>=4 where the theta-term 11.45 dominates pred_q over measured 4.80-5.92; the max-form posted the same 21/27: quadrature fixed the RANKING, not the boundary, and the residual is the THETA-TERM's torus face, not the field channel); Q3 OPEN (the composition NOT named — the pre-named branches didn't cover the middle case, deposited honestly: the field channel's status unchanged from exp233); Q4 PASS (exp233's deposit consumed READ-ONLY sha-recorded, all 27 terms re-derived with the imported frozen forms matching the deposit's 2dp values, zero re-simulation, bit-identical re-runs); landed at 67a2e11, deposited as results/exp246_quadrature_reread.json. REGISTERED NEXT: the theta-term's SLAVING CORRECTION — the 6 boundary misses are the homogenization number over-predicting at gamma>=4: the coupled (V,theta) system's homogenization mode decays at a rate REDUCED by the V-slaving (the exact zero-knob rate from the 2x2 coupled block, the law's missing term since exp79), one re-read of exp233's grid + exp79's grid under the corrected theta-term — the boundary should close to >= 80% and the three-channel composition name with it

## L225 — exp247 THE THETA-TERM'S SLAVING CORRECTION (C, 2/4, branch RESIDUAL-NAMED — the correction refutes AND names the true driver; exp246's registered next EXECUTED): C1 REFUTE (the coupled 2x2 block's exact slow eigenvalue makes the theta-term LARGER, not smaller — |s_slow| > mu*deg iff G_GAP > mu (0.20 vs 0.015), proven over the full (lambda x gamma x mu) sweep with both signs — so the corrected term moves AWAY from exp79's deposited gamma=0.25 column, 0/15 at 2dp; the instrument layer holds: the imported raw forms reproduce the deposited column bit-consistently and the uncoupled limit recovers exp79's raw form exactly — the refuted clause is the CORRECTION's, not the machinery's); C2 REFUTE (exp233's grid under the corrected quadrature stays 21/27 — the same 6 torus misses, deeper); C3 PASS (the rank law SURVIVES the correction: 0.9280 >= 0.90; the raw form recomputed first-hand at 0.9359 = exp246's deposit); C4 PASS (both deposits READ-ONLY sha-recorded byte-unchanged, deterministic); THE FINDING (the residual NAMED for the next instrument): the theta-term's AGGREGATION, not its rate — the worst-head-cell corrected drag 11.48-11.94 mV vs the SAME corrected drag as the 100-cell POPULATION RMS 4.14-4.30 mV; the population-form pred 4.14-5.21 vs measured 4.80-5.92, WITHIN 0.71 mV on every miss (the torus's thin boundary dilutes the worst-cell drag in the population RMS — exp79's worst-cell form is the write-regime's conservative face, the response regime's face is the population RMS); landed at bbafad6, deposited as results/exp247_slaving_correction.json. REGISTERED NEXT: the theta-term's aggregation form — the population-RMS corrected term as the law's response-domain face, re-read of the same grids under the population aggregation (the zero-knob form change the data themselves named)

## L226 — exp248 THE CONFLICT-GRID PASS (C, 3/3, branch MULTI-MEMORY-CONFIRMED — exp238's branch UPDATED at the honest bar; exp238's registered next EXECUTED): D1 PASS (the maximal zero-knob conflict recorded over the complete pre-named 10-candidate grid {10,20,25,33,50}x2: 75/100 = 75% at the head-to-posterior relocation of the 50-cell block; the >= 66% expectation LEVEL met but its 25-cell argmax hint REFUTED — that relocation is exactly morpho_engineering.target_mirror's 50%, no 25-cell relocation can exceed 50 differing cells — disclosed); D2 PASS (the M3 bar RE-DERIVED from the maximal candidate 60% -> 75%; exp238's M1/M2/M4 battery re-runs at the 75% conflict: co-existence, non-interference (the control delta exactly 0.0 — the spec layer is dynamics-inert), read-addressing ALL 9/9; the 9/9 theta-field witness matches vs exp238's deposit certify the verbatim re-run); D3 PASS (zero rejections, exp238's deposit byte-unchanged sha-stable, deterministic in-process AND across full process re-runs); THE INGRESSING MINDS CLAIM LANDS: multiple memories in the same body, simultaneously retrievable, non-interfering, read-addressed — at the maximal zero-knob conflict the machinery can express; landed at 88fbc76, deposited as results/exp248_conflict_grid.json. REGISTERED NEXT: none — the multiple-memories question is CLOSED (confirmed at the honest bar; the address-by-read protocol is the mechanism, exp238's M4 + this entry)

## L227 — exp249 THE GENE-RANGE REPAIR RE-READ (C, 3/3, branch GROUNDED-UNDER-REPAIR — exp235's NOT-GROUNDED verdict UPDATED; exp235's registered next EXECUTED; SALVAGED after the dispatch died post-run): R1 PASS (the repaired pooled Spearman >= 0.85 — the original bar — the drag WAS the layer's own degenerate recorded ranges, not the mechanism: the zero-width step gates expanded to the layer's own identity constants, the deep-band clip ties broken by the rung ordering, zero-knob); R2 PASS (the mid-band noise panel: the gated read's accuracy drop < the linear read's at every sigma — the threshold's robustness margin EXISTS between the gate and the saturation, the G2 result the original battery missed); R3 PASS (exp235's deposit READ-ONLY sha-recorded byte-unchanged, deterministic); THE CERVERA SCOREBOARD: the M37 gene layer's response IS the voltage-gated threshold law once the layer's own range artifacts are repaired — the biophysical mechanism grounds the layer; landed at f52c67f, deposited as results/exp249_gene_range_repair.json. REGISTERED NEXT: none — the grounding question is CLOSED (grounded under the range repair)

## L228 — exp250 THE M33/miRNA INTERFERENCE ANATOMY (C, 2/3, branch INTERFERENCE-STRUCTURAL — exp236's R2 REFUTE stands as a STRUCTURAL property; exp236's registered next EXECUTED): I1 PASS (the overlap map deposited per arm — the wrongly-de-competenced set is EMPTY on every arm: miRNA-repressed = the source ring [45,54) never intersects M33-specified = the head [0,25) — NO cell-level miRNA->M33 veto exists); I2 REFUTE (the AND-read destroys the trunk plane's sole competence: AND 0.00 < OR 1.00 on the M33+miRNA pair across all three arms — the strict intersection kills the miRNA-carried trunk competence because M33's predicate is false across the whole trunk (the TC-G5 dead zone); the AND compositions 21/27, only the gate-less M35+miRNA pair holds the trunk); I3 PASS (exp236's deposit byte-unchanged sha-stable, 189 rows x 2 passes bit-identical, the exp236 anchor exact 54/54); THE FINDING: the interference is DOMAIN-level, not cell-level — the mechanisms' competence domains are disjoint by construction (M33 anterior-only, miRNA mid-ring) and the AND-hierarchy cannot compose what the domains partition; the three-mechanism regionalization is a COVER, not a composition (each mechanism owns its plane); landed at 3859d3f, deposited as results/exp250_interference_anatomy.json. REGISTERED NEXT: none — the interference question is CLOSED (structural; the cover structure is the stack's regionalization architecture)

## L229 — exp251 THE THETA-TERM'S AGGREGATION FORM (C, 2/4, branch AGGREGATION-NOT-SUFFICIENT — exp247's registered next EXECUTED; the bodies written by the MAIN AGENT under the fleet-timeout rule): P1 REFUTE (the population-RMS aggregation ALONE drops the boundary agreement to 18/27 < 24 — the form UNDER-predicts on the arms the worst-cell form was right about: the aggregation trades boundary agreement for rank); P2 PASS (Spearman 0.9554 — the BEST rank of the three forms: raw worst-cell 0.9359, corrected worst-cell 0.9280, population 0.9554 — the rank and the boundary PULL APART: the response-law's form stays open, honestly not named); P3 REFUTE (the former misses' |pred-err| 2.63-3.46 > the 1.5 tolerance — exp247's suggestive non-gating population observation did NOT survive the pre-registered gate: the discipline held); P4 PASS (both deposits READ-ONLY sha-recorded byte-unchanged, deterministic); one body-only plumbing repair disclosed (exp233's field_term signature (Wf, lbl, gamma, kappa) with field_weights(A, arm)); landed at 394cf95, deposited as results/exp251.json. REGISTERED NEXT: the response-law form question stays OPEN with the strongest constraint set yet deposited (the rank ordering population > raw > corrected; the boundary ordering raw = corrected > population; the two faces the law must unify are the WRITE-regime worst-cell face and the RESPONSE-regime mixture — the pre-named next instrument: the per-arm aggregation (the population RMS on the arms where the boundary is thin, the worst-cell where it is thick — the arm-conditioned form, zero-knob if the conditioner is the arm's boundary-cell count, which the deposits carry)

## L230 — exp252 THE DEEP-BAND SUBSTITUTION'S COST (C, 3/3, branch INTERIOR-CARRIED — exp243's registered next EXECUTED; the body written by the MAIN AGENT under the fleet-timeout rule): B1 recorded (the argmax's boundary share mean 0.1513, interior 0.8487 — exp243's own exp208-machinery decompositions aggregated, per-seed shares deposited); B2 PASS (the deep-band rows' worst 3.68 vs the canonical rows' 0.19 — the substitution IS the cost's carrier); B3 PASS (exp243's deposit READ-ONLY sha-recorded byte-unchanged); THE FINDING: the conjunction's price is INTERIOR-carried — the deep band's own geometry costs, NOT the boundary signature (the honest surprise vs the pre-named boundary expectation; consistent with exp245's boundary-share finding — the boundary residual is a small-share object everywhere it has been measured); landed at 394cf95, deposited as results/exp252.json. REGISTERED NEXT: the interior cost's mechanism — the deep-band substitution's errs live in the PAIR-JUNCTION class (exp208's structure-coupled interior): the junction-pair geometry under the -60.0 rung swap is the named instrument (one battery on the substituted medium's pair structure)

## L231 — exp253 THE DEG-WEIGHTED AGGREGATION (C, 3/4, branch FORM-OPEN — exp251's registered next EXECUTED; the body written by the MAIN AGENT under the fleet-timeout rule): W2 PASS (Spearman 0.9597, the best rank yet — the form family's rank ordering: raw worst-cell 0.9359 < population 0.9554 < deg-weighted 0.9597); W3 PASS (>= both priors' 21/27); W1 REFUTE (the boundary still short of 24 — the aggregation family's two-point interpolation does not close it); W4 PASS (READ-ONLY sha-recorded, deterministic); THE FINDING: the rank rises monotonically along the mechanistic weighting direction (flat -> deg-participation) while the boundary stays pinned — the law's response-domain form needs a STRUCTURAL term (the boundary geometry itself), not a better aggregation; the constraint set widens (three forms, one rank ordering, one boundary pin); landed at 8b91bdb, deposited as results/exp253.json. REGISTERED NEXT: the structural term — the boundary-geometry instrument (the arm's canon-boundary cell count as the law's extra regressor, zero-knob from the deposits' own records) is the pre-named next test of the rank/boundary pull-apart

## L232 — exp254 THE PAIR-JUNCTION GEOMETRY UNDER SUBSTITUTION (C, 3/3, branch PAIR-GEOMETRY-CARRIED — exp252's registered next EXECUTED; the body written by the MAIN AGENT under the fleet-timeout rule; one body-only plumbing repair disclosed — the classify instrument re-nested inside exp208's/exp243's main()s, J1 evaluated from the two deposits' own class-count records, the record-only form the pre-named fallback): J1 recorded (the pair-junction SHARE SHIFTS UP under the deep-band substitution: the canonical battery's 42066/60000 = 70.1% vs the substituted argmax rows' 1002/1200 = 83.5%); J2 PASS (the substituted medium's pair cells' RMS err 3.706 vs the rest's pooled 3.520 — the cost lives where the geometry changed); J3 PASS (exp243's deposit READ-ONLY sha-recorded byte-unchanged); THE FINDING: the conjunction's interior price is the PAIR GEOMETRY's — the deep band's swap re-wires the pair-junction structure and the reader's price follows it (the mechanism exp252 named, now measured); landed at the batch-20 head, deposited as results/exp254.json. REGISTERED NEXT: the pair-structure's causal face — the pair-cell count as the reader's cost predictor across the 12 candidate hosts (the deposits' per-host class counts vs the per-host worsts: one regression, zero new simulation)

## L233 — exp255 THE PAIR-COUNT COST REGRESSION (C, 1/3, branch NOT-PAIR-COUNT-DETERMINED — exp254's registered next EXECUTED; the body written by the MAIN AGENT under the fleet-timeout rule; one body-only plumbing repair disclosed — the per-host pair shares beyond the argmax are not in the deposits, the base boundary-cell count the zero-knob host-level proxy): G1 REFUTE (Spearman(boundary-count, P3-worst) = 0.1374 < 0.5 across the 12 hosts); G2 REFUTE with the specificity INVERTED (rho_canon = 0.8574 >> rho_P3 = 0.1374 — the CANONICAL rows' cost IS boundary-count-determined across hosts, the boundary frontier confirmed at the host level, while the SUBSTITUTED rows' cost has a different driver); G3 PASS (exp243's deposit READ-ONLY sha-recorded byte-unchanged); THE FINDING: the boundary geometry drives the CANONICAL cost across hosts (0.857) but the deep-band substitution BREAKS that dependence (0.137) — the substitution decouples the cost from the boundary geometry, exp254's pair-structure mechanism operating at the ROW level, not the host level; deposited as results/exp255.json. REGISTERED NEXT: the substitution's row-level driver — the deep-band rows' errs vs their own pair-junction counts (the row-level regression the decomposition records carry per-seed), the host-level null sharpening the row-level test

## L234 — exp256 THE ROW-LEVEL PAIR REGRESSION (C, 3/4, branch ROW-DRIVER-ABSENT at the pooled level — exp255's registered next EXECUTED; the body written by the run agent; two body-only plumbing repairs disclosed: the pre-registered stub lacked the __main__ guard, json/numpy imported in-body beneath the BLAS pins): L233's registered next EXECUTED — the row-level regression the decomposition records carry per-seed, generated fresh: exp243's machinery VERBATIM (imports, floor restore, HostWMedium, scoped-arm replicas, build_rows, p1/p2/p3, exp208's classify/decompose with precedence intact), 12 hosts rebuilt FROM exp243's own deposit records (rewire seeds + base/edges/f_max/boundary sha-asserted), arms = exp243's P1/P2 canonical vs P3 deep-band substituted, seeds = exp142's (1,2,3) — 72 rows (12 hosts x 2 media x 3 seeds), each with its per-class decomposition and worst err; R1 REFUTE (Spearman(per-row PAIR-JUNCTION count, per-row worst err) = 0.2943 < 0.5 across the 72 rows — the pair-junction COUNT is not the across-battery row-level driver); R2 PASS (rho_subst = -0.1266 > rho_canon = -0.7199 on the same 36-row halves — the row-level mirror of exp255's host-level inversion: the substitution DECOUPLES the cost from the boundary geometry at the row level too); R3 PASS (pooled within-host rank correlation 0.5888 >= 0.5; 10/12 hosts >= 0.75 within-host — the pair mechanism is REAL WITHIN hosts; the two path hosts H0/H1 inverted at -0.906 and drag the pooled rho under the bar — the honest structure deposited, not smoothed away); R4 PASS (exp243's deposit READ-ONLY sha 26239a50 byte-unchanged; deterministic — 2x72-row battery bit-identical in-process AND the deposit byte-identical across two independent process runs, sha 3c8f0473; -60.0 floor restored + exit assert; 12/12 MULTI-identity audits; all 48 exp243 candidate errs reproduced exactly; zero rejections; foreground ~292 s); deposited as results/exp256_row_pair_regression.json. REGISTERED NEXT: the batch-22 queue — exp257 the architectural override (the 8-channel schema; the pair mechanism's within-host structure and the H0/H1 inversion both feed the activation tests' interpretation), then exp258/exp259

## L235 — exp257 THE NATIVE MULTI-CHANNEL WRITE-PATH SCHEMA (C, 8/8, branch SCHEMA-8-NATIVE — THE ARCHITECTURAL OVERRIDE LANDS; the body written by the MAIN AGENT, docstring sha-verified byte-unchanged e51cacc4 vs pre-registration 276e41e): the user's directive executed — the lower-level write path refactored from the 2-tuple (V, theta) to a native named 8-channel state array S (n, 8) on BioElectricCollective (and every state-carrying subclass through the shims); channels named per exp232's census: vmem/theta ACTIVE (the legacy pair, ch0/ch1), gj/ctx/ca2/sht/apop/ichan DORMANT (init 1.0/0.0/0.0/0.0/0.0/gamma, zero dynamics, zero feedback into ch0/ch1, carried only — the dormancy contract); the paper's 8 channels ALL have native state from this commit; the three ABSENT substrates (Ca2+ transients, 5-HT electrophoresis, apoptosis) EXIST from this commit; compatibility shims: self.V/self.theta properties backed by S[:,0]/S[:,1] (item assignment writes through), clone_state/restore_state exact legacy semantics (restore writes channels 0/1 ONLY, dormants untouched), new set_channel/read_channel/clone_state_full/restore_state_full + CHANNEL_NAMES/ACTIVE_CHANNELS/DORMANT_CHANNELS; S1 PASS (16/16 schema checks: constants, S shape, dormant inits, shims view, set_state/set_target route into S, phi_spec capture, clone 2-tuple, restore-dormant-untouched under live perturbation, full-state round-trip, item-assign write-through, unknown-channel raises, GraphCollective + LatchingCollective carry S with theta_anchor consistent); S2 PASS zero delta — B1 exp79's 45-point grid 45/45 bit-exact at the deposit's own precision (full-precision errs recorded), B2 exp32's 15 deposited arms 15/15 at FULL float precision (the M26 regrow walk — the write path — bit-exact; one body-side protocol repair disclosed BEFORE any gate read: exp32's arm_defs kwargs are part of the protocol — bare sim_arm(arm) is arm-independent on the crosspiece family and the first b2 run 3/15 was the transcription miss, fixed, re-run 15/15), B3 exp198's c3 cell at n=400 25/25 instances bit-exact + 8/8 summary anchors (median_err, median-of-medians, rejections 0, verify_rate, diffuse/concentrated split, f_max bounds — the production scoped read through CornerMedium under exp198's own pin discipline), B4 the full test suite green from the repo root; S3 PASS (dormancy asserted empirically: ca2+ctx scrambled mid-run on exp79's settle path — ch0/ch1 trajectories bit-identical, the perturbations drawn from a SEPARATE rng so the noise stream never shifts [the probe's own trap, pre-diagnosed]; no experiment module modified — only collective.py state plumbing, sha f8bd12a6 recorded); S4 PASS (in-process re-runs bit-identical, deposit fingerprint df1fea2e, no wall-clock fields; the exp169 floor trap caught at the body: the import chain pins -35.0 BEFORE exp198's save captures it, so restore_floor() restores the pinned value — the convention's explicit -60.0 restore applied and exit-asserted); landed at 178ce99, deposited as results/exp257_native_8channel_schema.json (merged from 6 deterministic segment files). REGISTERED NEXT: exp258 the interior-context boundary write coupling — the FIRST channel activation (ch3 ctx at the pre-named g_ctx grid {0, 0.25, 0.5, 1.0}, gates X1-X4; the truncation diagnosis's causal test: exp213/216/219/221's read-face repairs failed because the context was never IN the state to read), then exp259 the second activation (ch2 gj, the pair-cell canonical-match compensation, gates P1-P4)

## L236 — exp258 THE INTERIOR-CONTEXT BOUNDARY WRITE COUPLING (C, 3/4, branch CONTEXT-INERT — the FIRST channel activation under the exp257 schema, ch3 "ctx"; the body written by the run agent [the first dispatch died pre-body on an infra timeout and wrote the body uncommitted in the tree; the respawn verified it line-by-line against the pre-registration and the source machinery, then ran it — the salvage disclosed]): X1 PASS (the dormant identity, 75/75: g_ctx = 0 reproduces the production decode bit-exactly — V/T states bit-exact, errs + verified equal, exp199's deposit replayed at its 2-dp rounding, exp208's decomposition rows reproduced bit-exactly, exp226's R1 verbatim — the migration gate clean BEFORE any g_ctx > 0 run); X2 REFUTE (the pre-named grid {0, 0.25, 0.5, 1.0} — the best cell g_ctx = 0.25 REDUCED the worst boundary-row err by -2.3238, i.e. DEGRADED it: 4.3623 dormant -> 14.4993/25.59/49.25 at the three activations — monotonically worse with gain; nowhere near the +10% reduction bar); X3 PASS-vacuous (the pre-named exp208 INTERIOR class is EMPTY on the c6 battery — INTERIOR n_cells = 0 in all 75 of exp208's own deposited decompositions — the class kept STRICTLY pre-named, the vacancy disclosed, the non-boundary complement deposited audit-only, never gated: -0.0532 at g*); X4 PASS (exp226/exp229/exp199/exp208 deposits READ-ONLY sha-recorded byte-unchanged; collective.py untouched sha-recorded; public accessors only — set_channel/read_channel, the activation instrument entirely inside the experiment module; the -60.0 floor restore moved into _merge after the exp169->exp199 import chain pinned -35.0 [the exp257 precedent]; deterministic re-runs byte-identical; no wall-clock fields, fingerprint fd11edf2); landed at 505b3d6, deposited as results/exp258_interior_context_coupling.json. THE FINDING (the truncation diagnosis's causal test): the interior context written INTO the state and blended into the boundary commits does not close the boundary excess — it DEGRADES it monotonically with gain; exp213/216/219/221's read-face refutations are now joined by the write-face refutation: the ~0.686 boundary residual's carrier is NOT the missing interior context (the exp257 refactor made the test POSSIBLE — the channel had nowhere to exist before — and the answer is honest INERT). REGISTERED NEXT: exp259 (the second activation, ch2 gj — executed in parallel, see L237); then the batch-23 derivation from the activation record

## L237 — exp259 THE PAIR-CELL GEOMETRY COMPENSATION (C, 1/4, branch COMPENSATION-INERT — the SECOND channel activation under the exp257 schema, ch2 "gj"; the body written by the MAIN AGENT under the two-death rule [the fleet died twice pre-body on dispatch]; docstring sha-verified byte-unchanged f898d072): P1 PASS (the dormant identity: the identity multipliers are a no-op — W == A array-equal on all 12 hosts + the H3 battery at identity reproduces exp243's deposited worsts 6/6 bit-exact [3 seeds x 2 arms; the stdout label said /12 — a cosmetic print denominator bug, the gate and deposit carry the correct 6-row form, disclosed]); P2 REFUTE (the canonical-match renormalization REDUCED the substituted worst-errs by -0.41% — off 1.0139 -> on 1.0181, the pooled mean-of-worsts over the 36 rows [12 hosts x 3 seeds], the form fixed in the body's READ_CONFIG — nowhere near the pre-named +10% bar: renormalizing the pair cells' participation toward the canonical mean does NOT close the substituted medium's reader cost); P3 REFUTE with the lever's specificity INVERTED (the SAME compensation DEGRADED the canonical media by +12.7% >> the +5% non-interference bar — the participation renormalization perturbs any medium it touches); P4 PASS (exp243/exp254 deposits READ-ONLY sha-recorded byte-unchanged [sha 26239a50 / 09ac269e]; conductance conservation asserted per compensation — the global renormalization sum(W_post) == sum(W_pre), the compensation redistributes and does not amplify; the gj channel is the multipliers' carrier of record, set_channel/read_channel round-trip asserted per decode; floor -60.0 restored + asserted; the subst arm re-run on H0-H5 bit-identical in-process); THE FINDING: exp254's pair-geometry correlation (J2's pair-cell RMS 3.706 vs the rest's 3.520) and exp256's within-host driver (0.5888) are REAL but NOT causally manipulable through participation MAGNITUDES — the reader's cost lives in the pair STRUCTURE (which cells carry chords), not in the participation weights; the zero-knob renormalization is inert on the substituted medium and actively harmful on the canonical ones; the OFF baseline is exp243's deposited errs (the zero-drift baseline after exp256's bit-exact verification); landed at 2183b56, deposited as results/exp259_pair_geometry_compensation.json. THE ACTIVATION RECORD (batch 22 closes): the 8-channel schema EXISTS (exp257 SCHEMA-8-NATIVE, bit-exact at every legacy call site) but NEITHER activation lever moved the cost — ch3 ctx INERT-degrading (exp258), ch2 gj INERT-harmful (exp259): the boundary/pair residual's carrier is neither interior-context-in-state nor participation-weights. REGISTERED NEXT (batch 23, derived): (a) the pair STRUCTURE lever — the exp254 shift was a STRUCTURAL rewiring (which cells carry >= 2 chords), so the next instrument is structure-level: add/remove pair-chords at the substituted rows' pair cells (the pre-named structural dual of exp259's weight-level test), (b) the exp229/exp245 residual's next instrument family under the exp257 schema's new state surface, (c) the remaining dormant channels (ca2/sht/apop) each with its own pre-registered activation test, (d) BETSE's multi-channel ion dynamics (the user's directive: the betse-reference clone at /home/z/my-project/betse-reference) as the design reference for the ca2 activation's kinetics (the channel with the richest external grounding: BETSE's Na+/K+/Cl- flux machinery)

## L238 — exp260 THE PAIR-STRUCTURE LEVER (C, 3/4, branch STRUCTURE-INERT — L237's registered next (a) EXECUTED, exp259's structural dual; the body written by the run agent [salvage-verified: the first dispatch died pre-body on the infra timeout and left the body in the tree; the respawn verified it line-by-line vs the pre-registration and the exp259 precedent, then ran it — the third independent process run reproduced the deposit byte-identically, sha 2e244371, fingerprint 9669017854fef85d]; landed at 096f5f0): Q1 PASS (the identity gate ran FIRST and stayed clean — the canonical rows' no-op array-equal 24/24 on the 12 hosts + the un-operated substituted rows reproducing exp243's deposited worsts 72/72 bit-exact); Q2 REFUTE with the lever INVERTED (the DE-PAIRING operation — 225 lowest-index-first minimal chord removals across the 24 substituted rows, both-endpoints-non-boundary freeze honored, every removal recorded — made the pooled worst-err ~6x WORSE: off 1.0139 -> on 6.1794, -509% vs the pre-named +10% bar); Q3 PASS (the canonical rows' worst-errs unchanged bit-exactly, verified live); Q4 PASS (exp243/exp254 READ-ONLY sha-recorded; the -60.0 floor restored+asserted; the 6-host determinism re-run bit-identical; one cosmetic disclosure: the note's "H0-H5" label is the lexicographic first six H0/H1/H10/H11/H2/H3 — no gate semantics, disclosed not hand-edited); THE FINDING: the chord set is not a cost lever either — removing the substituted rows' non-canonical pair chords BREAKS the read's own transport (the pair chords are functional infrastructure the decode routes through), so the pair-geometry correlation (exp254 J2, exp256 within-host 0.5888) is DIAGNOSTIC-ONLY: weights inert (exp259), structure harmful (exp260), the cost lives elsewhere; deposited as results/exp260_pair_structure_lever.json. REGISTERED NEXT: the batch-23 remainder — exp261 the ca2 activation (executed in parallel, L239), then the residual's variance-components decomposition (the exp256 battery's own 72-row worsts decomposed host/arm/seed — zero new simulation)

## L239 — exp261 THE CA2 CHANNEL ACTIVATION, BETSE-GROUNDED (C, 2/3 evaluated, branch CA2-INERT — the THIRD activation under the exp257 schema, ch4 "ca2", the user's BETSE directive executed as the external grounding; the body written by the run agent [salvage-verified from the interrupted first dispatch's tree state]; landed at fa63301): C1 PASS (the port: BETSE's Cav3.3 T-type HH kinetics [vg_ca.py class Cav3p3, Traboulsie et al. 2007] + the pumpCa Keq face [sim_toolbox.py] ported VERBATIM — all 13 quoted source lines byte-match the reference tree [tree shas 843d83f9/d94b50e8 recorded], the 401-point V-grid recomputation 0.0 delta on m_inf/m_tau/h_inf/h_tau/P; ONE pre-registration prose defect caught and disclosed: the docstring's K1 m_inf form is the exact complement of BETSE's own file line [dropped sign] — the body kept the FILE line authoritative per the docstring's own VERBATIM clause and demonstrated the complement numerically, sum 1.0 delta < 1e-12); C2 REFUTE (the readout: pooled Spearman(P_i, |V_i - theta_i|) = 0.1738 << 0.5 over 30,000 cell-points on the c6 battery's settled states — the Cav3.3 open-probability field does NOT track the V/theta mismatch; the localization clause held [boundary mean P 0.010150 > non-boundary 0.009506] but the association gate is the pre-named one and it failed); C3 SKIPPED-C2-FAIL (the write coupling untested BY DESIGN — the dispatch assert never launched the grid); C4 PASS (the identity gate 75/75 bit-exact; exp226/exp229 READ-ONLY; collective.py untouched sha-recorded; the BETSE tree READ-ONLY; the -60.0 floor restored+asserted at every exit; the merge re-run byte-identical, fingerprint 8be9582d538f23ef); THE FINDING: the externally-grounded Ca2+ readout localizes weakly and associates not at all — the activation record now reads ctx INERT (exp258), gj INERT (exp259), ca2 INERT (exp261), pair-structure INERT-HARMFUL (exp260); deposited as results/exp261_ca2_activation_betse.json. REGISTERED NEXT (batch 24, derived): (a) exp262 the residual's three-way variance-components decomposition — the exp256 battery's 72 deposited worsts decomposed host/arm/seed by the exp229 OLS-on-tied-ranks method, zero new simulation: WHERE does the 68.6% live at the design level [seed-share ~0 = deterministic-per-instance structural; seed-share high = noise-like]; (b) exp263 the sht activation (the paper's 5-HT electrophoresis face, stack-native spec: the transporter-mediated flux of the theta-gradient — the exp258/261 mold: dormant identity + readout + the gated coupling); (c) exp264 the apop activation (the paper's apoptosis-as-morphogenetic-signal face: the extreme-theta marking channel's readout + gated coupling)

## L240 — exp262 THE RESIDUAL VARIANCE COMPONENTS (C, 4/4, branch DETERMINISTIC-PER-INSTANCE — L239's registered next (a) EXECUTED, zero new simulation; the body written by the run agent; landed at d2c9944): V1 PASS (72/72 rows complete and finite; exp256's reproduction records sha-verified byte-unchanged, the exp243 provenance sha cross-checked); V2 PASS (the three-way rank-variance attribution by exp229's OLS-on-tied-average-ranks method generalized to three factors, the shares the symmetric average of the two order-of-entry decompositions [host->arm->seed and its reverse], R2_full 0.8856, the shares sum to 1.000000 exactly, no clamping; reference-coding invariance asserted; 15 tied values handled by the tied-average rankdata); V3 PASS on the pre-named discriminant — THE SEED SHARE IS 0.0073 <= 0.10 (host 0.1213 / arm 0.7570 / seed 0.0073 / unexplained 0.1144); V4 PASS (exp256/exp229/exp243 deposits READ-ONLY sha-recorded byte-unchanged; deterministic across two independent process runs, sha b4fbe192; one in-run catch repaired pre-commit: a last-ulp float-association mismatch between the primary and pass-A share formulas tripped the module's own bit-identity gate — the increments-first identical formula form fixed it, never reached a deposit or gate outcome); THE FINDING: the exp229/exp245 residual REPLICATES across seeds — it is a deterministic property of the (medium, row) configuration, and 75.7% of the explainable rank variance sits on the canonical-vs-substituted ARM contrast: the residual lives in the SUBSTITUTION's interaction with the read, not in seed-level noise; the next instruments must be structure-level, and the arm share itself names the target: the deep band's own TARGET GEOMETRY; deposited as results/exp262_variance_components.json. REGISTERED NEXT: (b)/(c) the sht/apop activations (L241/L242), then the target-geometry regression (the arm share decomposed against the deep rows' own target properties)

## L241 — exp263 THE SHT CHANNEL ACTIVATION (C, 2/3 evaluated, branch SHT-INERT — the FOURTH activation, ch5 "sht", the paper's 5-HT electrophoresis face stack-native; the body written by the run agent; landed at 1668e7a): H1 PASS run FIRST (the dormant identity 75/75 bit-exact vs the production scoped decode — the run() unroll is bit-exact by construction, the read-only flux accumulation interleaved); H2 REFUTE (the accumulated electrochemical flux field S_i = the per-cell inward-directed sum sum_j (V_j - V_i) over the junction neighbors [the GJ network's own coupling face read through the transporter's inward-positive convention; the sign resolution fixed outcome-blind before the readout ran and the mirror convention reads -0.0825, also a clean REFUTE — the gate is sign-immune]: pooled Spearman(S_i, |V_i - theta_i|) = 0.0825 << 0.5 over 30,000 points, per-seed 0.0827/0.0826/0.0823, all 75 per-row rho in [0.020, 0.124] uniformly positive-but-small — the flux field is a SMOOTH LOCAL transport face [battery-wide antisymmetric, sum_i S_i = 0 identically, mean |S| 7.65e5], not the reader's mismatch carrier); H3 SKIPPED-H2-FAIL (the pre-named grid never launched — the dispatch asserts H2's checkpoint before running; NO g_sht > 0 decode exists); H4 PASS (exp226/exp229/exp199/exp208 READ-ONLY sha-recorded; collective.py untouched sha f8bd12a6; floor -60.0 restored+asserted at every exit; pass A == pass B byte-identical 0e2e3b0e, the merge re-run byte-identical fd3cca89, fingerprint 1aded5ab2f292682); deposited as results/exp263_sht_activation.json. REGISTERED NEXT: exp264 (L242); then the target-geometry regression

## L242 — exp264 THE APOP CHANNEL ACTIVATION (C, 2/3 evaluated, branch APOP-INERT — the FIFTH activation, ch6 "apop", the apoptosis-as-morphogenetic-signal face; the body written by the run agent [salvage-verified from the interrupted session's tree state — zero defects found, across-session byte replication of the a1 segment]; landed at d6f08b2): A1 PASS run FIRST (the dormant identity 75/75 bit-exact, 0 rejections); A2 REFUTE with the mark set's enrichment INVERTED (the pre-named mark set — settled-theta battery-wide extreme decile both tails OR the blastema band — is canon-boundary-DEPLETED: the marked cells' boundary membership rate 0.2745 vs the unmarked 0.5251, the enrichment ratio 0.5227 vs the pre-named 2.0 bar, Fisher p underflows to 0.0 — APOPTOSIS MARKS THE INTERIOR, NOT THE BOUNDARY: the extreme-theta cells are the deep-band's own interior, the opposite of a boundary signal); A3 SKIPPED-A2-FAIL (the commitment-noise-relaxation grid never launched; NO g_apop > 0 decode exists); A4 PASS (all READ-ONLY shas unchanged; collective.py untouched f8bd12a6; the -60.0 floor restored+asserted at every exit; pass A == pass B byte-identical and == the salvaged segment [across-session replication]; the merge re-run byte-identical f6e091de, fingerprint 57d0b0c0b1d52213); deposited as results/exp264_apop_activation.json. THE ACTIVATION RECORD, COMPLETE: all five dormant channels activated and tested under the exp257 schema — ch3 ctx INERT-degrading (exp258), ch2 gj INERT (exp259), ch4 ca2 INERT [BETSE-grounded, the port 0.0-delta clean] (exp261), ch5 sht INERT (exp263), ch6 apop INERT with the mark set INTERIOR-depleted (exp264) — plus the pair levers: weights INERT (exp259), structure INERT-HARMFUL (exp260); THE PAPER'S 8-CHANNEL CORRESPONDENCE ON THIS STACK: 2 active channels (the exp232 verdict) + 5 activated-but-inert native channels + the schema carrying all 8 natively (exp257) — the channels EXIST and none of them carries the boundary residual. REGISTERED NEXT (batch 25, derived from exp262's arm share 0.757): (a) exp265 THE TARGET-GEOMETRY REGRESSION — the substituted rows' worst errs (exp256's deposited rows) regressed against the deep rows' OWN target properties (the -60.0 rung's zone structure: the target's own boundary-cell count, zone count, and the rung instances), zero new simulation: does the arm contrast decompose into target geometry?; (b) exp266 THE LAW'S STRUCTURAL TERM — the two-channel law's response form extended with the pre-named structural regressors the batteries named (the arm indicator + the host boundary count), evaluated on the deposited battery, the exp251/exp253 aggregation line's honest close: the rank the structural terms reach vs the boundary pin

## L243 — exp265 THE TARGET-GEOMETRY REGRESSION (C, 3/4, branch TARGET-GEOMETRY-ABSENT — L242's registered next (a) EXECUTED, zero new simulation; the body written by the run agent; landed at 92ccb71): G1 PASS (the deep targets rebuilt at n=400 via exp256's verbatim build_rows bit-match all 144 deposited row_target_sha256 records); G2 REFUTE (no pre-named target property carries the substituted rows' worst errs — the target's own canon-boundary count rho -0.0265; the zone count 3 and the value range 40.0 are construction-constants on this battery); G3 PASS (the host-level specificity mirror stays strong: rho 0.8362 on the 36 rows / 0.8767 on the 12 points vs exp255's 0.8574); G4 PASS (all deposits READ-ONLY sha-recorded byte-unchanged; deterministic across independent process runs; floor asserted); THE FINDING: the -60.0 paint ERASES the host's scattered head/trunk transitions exactly where they were most numerous — the arm share's carrier is the READ's own response to the substitution, not the target's geometry; deposited as results/exp265_target_geometry.json. REGISTERED NEXT: exp266 (L244), then the read-stage attribution

## L244 — exp266 THE LAW'S STRUCTURAL TERM (C, 3/4, branch LAW-OPEN — L242's registered next (b) EXECUTED, the exp251/exp253 aggregation line's honest close; the body written by the run agent; landed at e5de916): W1 PASS (72 rows complete/finite, all deposits READ-ONLY sha-verified); W2 REFUTE (the OLS rank ladder: M0 degenerate [exp232's star-point pred is a constant per the pre-registered fallback, asserted immaterial] / M1 rank 0.8700 [R2 0.7570 == exp262's arm share exactly] / M2 0.8841 / M3 0.8308 — the arm x boundary INTERACTION REGRESSES the rank, and M3 falls short of the pre-named 0.90 bar); W3 PASS (the boundary pin holds 72/72 — BAR 6.0 reconstructed exactly from exp251's 27 rows; the vacuity disclosed: the battery never crosses 6.0); W4 PASS (deterministic, two in-run passes sha-identical + independent-process deposit byte-identity); THE FINDING: the structural terms close the rank to 0.884 and the interaction overfits it back down — the law's response form needs the READ's OWN RESPONSE SURFACE, not more deposit-level structure; the two-line convergence (exp265's absent target geometry + exp266's open law) names the next instrument family precisely: the read-stage attribution; deposited as results/exp266_law_structural_term.json. REGISTERED NEXT (batch 26, derived): exp267 THE READ-STAGE ATTRIBUTION — the arm contrast localized INSIDE the read stack: re-run the substituted rows' decodes with each read stage's output held at its canonical-row value in turn (the projection PN1/PN2, the flip-clock F, the executor walk — the exp208 c6-tail-ablation's own mold, applied to the read's stages); the stage whose canonicalization closes the arm contrast CARRIES the residual

## L245 — exp267 THE READ-STAGE ATTRIBUTION (C, 3/4, branch DISTRIBUTED — L244's registered next EXECUTED; the body written by the run agent [salvage-verified from the interrupted dispatch's tree state, zero defects, anchors AST-verified verbatim vs exp256]; landed at 9253f8c): R1 PASS (S0 reproduces the deposited errs bit-exact 72/72 vs exp256 AND exp243; the MULTI-identity audits 12/12); R2 REFUTE (the stage-delta rank shares: the PROJECTION's canonicalization 0.4406 — the largest single stage — the EXECUTOR's canonical walk 0.1990, the FLIP-CLOCK hold 0.0000 [a VERIFIED structural no-op: TC1 is identically zero on static single-frame media, S2 bit-identical to S0 on all 72 rows — the flip-clock never fires on this battery's media class], unexplained 0.3604; no stage reaches the 0.5 bar); R3 PASS (fired — the honesty clause: the arm contrast does not localize to a single stage, the shares named); R4 PASS (all 8 discipline clauses: deposits READ-ONLY sha-recorded, the production fingerprint asserted pre/post, the -60.0 floor restored+asserted at every exit, the 6-host determinism re-run bit-identical, no wall-clock fields); THE FINDING: the arm contrast lives in the read stack's JOINT, INTERACTING response to the deep-band substitution — the projection is the dominant single face (0.44) and the executor the second (0.20), jointly 0.64 with 0.36 irreducible-in-this-instrument; deposited as results/exp267_read_stage_attribution.json. REGISTERED NEXT: exp268 THE JOINT HOLD — S1 x S3 canonicalized SIMULTANEOUSLY on the same 72 rows: does the joint hold close the arm contrast [the interaction is the carrier] or leave the 0.36 [the joint's irreducible face]? — plus the disclosed flip-clock finding [TC1's zero on static media is itself a stack fact the read's own docs should carry]

## L246 — exp268 THE JOINT HOLD (C, 3/4, branch NOT-STAGE-DECOMPOSABLE — L245's registered next EXECUTED; the body written by the run agent [exp267's machinery verbatim, the J replica disclosed-in-advance and verified]; landed at 9155e0e): J1 PASS (exp267's S0/S1/S3 rows byte-verified 72/72; the canon decodes 54/54 bit-exact across the exp256/exp243/exp267 anchors; the canon stage outputs sha-verified 24/24; 12/12 MULTI audits; the 6-host pass-2 bit-identical); J2 REFUTE (the joint hold's delta is BIT-IDENTICAL to the S3 executor single — J == S3 72/72, exact scale 72/72: the executor hold SUBSUMES the projection hold [the held walk's input IS the held projection] and the flip-clock is the verified zero; the joint share 0.3551 < the 0.5 bar AND < max(single) 0.4406 + 0.10 — under the same convention the singles read S1 0.5967 / S2 0.0000 / S3 0.3551; holding BOTH stages closes LESS than the projection single alone); J3 PASS (the residual after the joint hold 0.6449 — the honest branch named from the numbers: NOT-STAGE-DECOMPOSABLE); J4 PASS (all deposits READ-ONLY sha-recorded; the fingerprint asserted pre/post; the -60.0 floor restored+asserted at every exit; the merge re-run byte-identical; one plumbing fix disclosed pre-gate: the first merge attempt's KeyError crashed BEFORE any gate evaluation, the fixed merge is the single evaluation); THE FINDING: the read's response to the deep-band substitution is NOT stage-decomposable — the stage-hold ablation class is EXHAUSTED (single holds exp267, the joint hold exp268): the residual is the WHOLE STACK's joint response surface, deterministic-per-instance (exp262), arm-carried (0.757), irreducible at every decomposition level tried; THE BOUNDARY RESIDUAL'S FINAL CHARACTERIZATION AT THE READ-STACK LEVEL: a genuine, replicating, non-localizable property of the production read's engagement with the deep-band substitution; deposited as results/exp268_joint_hold.json. REGISTERED NEXT (batch 27, derived): the read-stack line closes where it started — the residual's existence is now characterized at every level [substrate exp256/262, target exp265, law exp266, stages exp267/268, channels exp258-264]; the honest next instruments are (a) exp269 THE RESPONSE-SURFACE SAMPLE — the read's err surface sampled DENSELY over the substitution's own parameter [the deep rung's voltage: -60 -> a pre-named rung ladder {-30, -40, -50, -55, -60, -65, -70} x the 12 hosts x 3 seeds, the substitution's dose-response curve per host — the first direct measurement of the read's response SHAPE], (b) the ledger's standing repair line [exp251's aggregation family stays pinned at the boundary], (c) the BETSE reference's remaining grounding value [the user's directive] recorded in the repo docs as the multi-channel design reference the exp257 schema + exp261 port consumed

## L247 — exp269 THE RESPONSE-SURFACE SAMPLE (C, 2/4, branch SCATTER — L246's registered next (a) EXECUTED; the body written by the run agent [salvage-verified, zero fixes, the machinery byte-verbatim vs exp267, the mean-canon recomputation bit-asserted vs the deposited 0.13777]; landed at 97140ac): U1 PASS (the -60.0 rung reproduced exp256's deposited substituted errs bit-exact 72/72 — the anchor clean, ran FIRST); U2 REFUTE with the refusal RECORD (360/504 finite: the -65.0/-70.0 rungs sit BELOW the production identity repertoire [-60.0, -15.0] and all 144 rows return the compiler's OWN safety refusal — recorded, never patched: the surface truncates at the floor); U3 REFUTE on both conjuncts (pooled |rung|-vs-err Spearman 0.0745 << 0.5 — FLAT within the repertoire, 5/12 host curves rank-constant; the extreme rungs neither saturate nor diverge — no finite err exists beyond the floor); U4 PASS (all deposits READ-ONLY sha-recorded byte-unchanged, the fingerprint asserted pre/post, the -60.0 floor restored+asserted at every exit, the -65.0 six-host pass-2 bit-identical, the merge re-run byte-identical a244d171); THE FINDING: the read's response to the deep-band substitution is NOT dose-dependent on the substitution's own voltage — rung-insensitive inside the repertoire, hard-refused beyond it; THE RESIDUAL'S COMPLETE CHARACTERIZATION (the read-stack line closes): deterministic-per-instance (exp262), arm-carried 0.757 (exp262), not the target's geometry (exp265), not closable by structural terms (exp266), not stage-decomposable (exp267/268), and NOT dose-dependent on the substitution's parameter (exp269) — the residual is the read's CATEGORICAL response to the substitution EVENT itself (the identity-structure rewrite), not a continuous response to any of its parameters; the deep band is either IN the repertoire (and then its cost is flat) or OUT (and the compiler refuses) — there is no analog dose face; deposited as results/exp269_response_surface.json. REGISTERED NEXT (batch 28, derived): the categorical finding points at the identity STRUCTURE, not the voltage: exp270 THE STRUCTURAL DOSE — the substitution's event size as the parameter [the deep band's zone count scaled 1..MULTI's full zone set at the fixed -60.0 rung: how many zones the rewrite touches is the dose the voltage ladder could not see; the same 12 hosts x 3 seeds; the -60.0 single-zone form the exp256 anchor] — the categorical response's own dose curve, or its flatness, is the last unmeasured face of the surface

## L248 — exp270 THE STRUCTURAL DOSE (C, branch FLAT-REFUSAL with the STEP structure named — L247's registered next EXECUTED; the body written by the MAIN AGENT under the two-death rule [the fleet died twice pre-body]; docstring sha-verified byte-unchanged; two body-side repairs disclosed pre-gate: the flip_clock_matrix import in the verbatim reader block, and the anchor-grid count 24->36 [a docstring-side miscount, the deposit discloses]; landed at 1098393): Z1 PASS (the anchor: the saturated dose d >= 3 IS exp256's full deep form — MULTI carries 3 zones so the pre-named ladder {1,2,4,8,16} saturates, the saturated form bit-asserted == exp172's construction on the n=100 H0 rebuild, and it reproduces exp256's deposited i0 substituted errs 36/36 bit-exact); Z2's SUBSTANCE PASSES (180/180 rows complete, finite, ZERO rejections — the gate constant's FAIL is the body's own 24-vs-180 miscount, disclosed, the grid itself complete); Z3 REFUTE on the pre-named pooled monotonicity (Spearman 0.0075) with the per-dose means carrying the honest structure: d=1 mean 0.7939 -> d=2 1.0042 -> d=4/8/16 1.0131 identical — THE RESPONSE IS A STEP, NOT A GRADIENT: one-zone rewrites cost less, ANY multi-zone rewrite costs the same, the categorical face confirmed at the event-size axis; Z4 PASS (deposits READ-ONLY sha-recorded; the fingerprint + the identity repertoire [-60, -15] asserted; the -60.0 floor restored+asserted; the d=2 form re-run on 6 hosts bit-identical); deposited as results/exp270_structural_dose.json. THE SUBSTITUTION EVENT'S FULL PORTRAIT — the read-stack line CLOSES (batch 28's close): the boundary residual is deterministic-per-instance (exp262), arm-carried 0.757 (exp262), not the target's geometry (exp265), not closable by structural terms (exp266), not stage-decomposable (exp267/268), not voltage-dose-dependent (exp269), and a STEP in the event size (exp270) — the read's categorical response to the identity-structure rewrite itself, characterized at every axis the batteries expose; the 8-channel schema (exp257) + the five activations (exp258/259/261/263/264) + the pair levers (exp259/260) stand as the architectural record. REGISTERED NEXT (batch 29, derived): the categorical step names one live question — the ONE-ZONE regime's own structure [d=1's 0.794 vs the canon baseline's ~0.55-0.62: the single-zone rewrite's premium over canon, decomposed the exp262 way]; then the standing frontiers: the aggregation family's boundary pin (exp251/253), exp243's A2 price re-read, and the BETSE design-reference record (the user's directive) written into the repo docs as the exp257/261 grounding provenance

## L249 — exp271 THE ONE-ZONE PREMIUM (C, 4/4, branch PREMIUM-STRUCTURAL — L248's registered next EXECUTED; the body written by the run agent; landed at f0419b3): P1 PASS (the canon grid re-read from exp256 36/36 finite; the d=1 grid — ONE PRE-REGISTRATION DEFECT CAUGHT AND REPAIRED, disclosed: exp270's z2 block was deposited as summary counts only, the per-row d=1 errs existed in NO deposit; per exp270's own Z1 precedent the d=1 grid was RECONSTRUCTED with exp270's verbatim machinery, verified two ways [tier 1: the machinery reproduced exp270's deposited saturated z1 grid 36/36 bit-exact; tier 2: the reconstructed d=1 mean == the deposited anchor 0.7938888888888889 bit-exact], two-pass bit-identical; the repair waives the zero-new-simulation clause and the no-exp169-import clause, both disclosed); P2 PASS (the mean premium +0.6561 > 0, 36/36 rows positive, 12/12 hosts all-positive — the premium is SYSTEMATIC); P3 PASS (the premium's rank shares: host 0.8143 / seed 0.0581 / unexplained 0.1277, R2_full 0.8723, the exp262 convention — the seed share 0.0581 <= 0.10: the step's lower-shelf height is a HOST property, deterministic-per-host); P4 PASS (exp270/exp256/exp243 deposits READ-ONLY sha-recorded byte-unchanged; two-pass determinism; the -60.0 floor restored+asserted at exit); deposited as results/exp271_one_zone_premium.json. THE FINDING: the structural step's lower shelf is itself structured — every host pays a positive premium for even a ONE-zone rewrite (+0.66 over canon on average), and the shelf's height is a deterministic host property (host share 0.81): the read's categorical response prices the identity-structure rewrite per-host, from the first zone; THE STANDING REPAIR this run exposes, recorded: future batteries deposit the PER-ROW GRID, never counts-only (exp270's z2 shortfall, caught here). REGISTERED NEXT (batch 30, derived): (a) exp272 THE HOST PREMIUM STRUCTURE — the shelf height's own predictor across the 12 hosts [the host's canon-boundary count, the exp255 instrument, vs the per-host premium means — one regression, zero new simulation: is the step's price a function of the host's own boundary geometry?]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record (the user's directive) written into the repo docs as the exp257/261 grounding provenance

## L250 — exp272 THE HOST PREMIUM STRUCTURE (C, 3/4, branch PRICE-HOST-OTHER — L249's registered next (a) EXECUTED; the body written by the run agent; landed at 8d6d6bc): H1 PASS (all grids complete/finite; the audit-only cross-check: exp270's deposited saturated z1 grid bit-identical to exp256's i0 errs 36/36 — the saturated-dose==deep-form identity re-verified); H2 REFUTE (the one-zone premium does NOT track the host's canon-boundary count: Spearman 0.0526, slope +0.0159/cell, R2 0.135 — the exp255 law does NOT extend to the substitution's categorical face: the canonical cost is boundary-geometric, the rewrite premium is NOT); H3 PASS (the shelf-to-shelf regression: Spearman 0.9912, OLS R2 0.986 — the one-zone and multi-zone premium shelves are the SAME host property at different depths: a host-fixed price with a depth offset; the outlier structure named: premium hosts H3/H5 at 1.95/2.10 one-zone and 3.51/3.17 multi-zone vs the ten-host cluster's 0.34-0.49/0.33-0.49); H4 PASS (exp271/exp256/exp243 deposits READ-ONLY sha-recorded byte-unchanged; two-pass determinism; the deposit byte-identical across two full processes, fingerprint 5b14aced755285cb; the -60.0 floor asserted at exit); THE FINDING: the step's price is a host-fixed property OUTSIDE the boundary geometry — the read prices the identity-structure rewrite per-host from a source that is neither the host's boundary nor the rewrite's depth (depth only OFFSETS the price, rho 0.99): the two-host outlier structure (H3/H5) is the next named target; deposited as results/exp272_host_premium_structure.json. REGISTERED NEXT (batch 31, derived): (a) exp273 THE OUTLIER HOSTS — H3/H5's shared property hunt across the deposited host records [the exp243 classes records' full fields, the exp182 margin profiles, the exp241 margin data: what distinguishes the two premium hosts from the ten-host cluster — one discriminant search, zero new simulation]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs

## L251 — exp273 THE OUTLIER HOSTS (C, 4/4, branch OUTLIER-DEPOSIT-CARRIED — L250's registered next (a) EXECUTED; the body written by the run agent; landed at e1cd765): X1 PASS (the 35-field provenance-tagged 12-host table assembled from five deposits; exp271's grid == exp272's re-read 36/36 exact; exp182's margin profiles target-keyed, 0 host fields — evidence recorded; rewire_seed partial-coverage reported never counted); X2 PASS (19/34 tested fields separate {H3, H5} from the ten-host cluster on the same side, 12 distinct fields, with NON-CIRCULAR external discriminants: mia_prod_err 2.12/2.28 vs the cluster's [0.49, 0.52] — 4x — n_boundary_cells_base 47/48 vs [4, 43] [the TOP TWO boundary counts], the canonical pair-junction mean BELOW 295/283 vs [301, 393] [the BOTTOM TWO], the all-arms pair-junction mean below 314.5/310 vs [319, 389]; the shelf/premium fields tagged definitional — H3/H5 were NAMED from them — never presented as findings); X3 PASS (2 one-sided fields named, never counted); X4 PASS (5 deposits READ-ONLY sha-recorded byte-unchanged; two-pass bit-identical; the deposit byte-identical across processes 26337306; the -60.0 floor asserted at entry and exit; runtime 0.2 s — the pure-re-read clause holds verbatim); THE FINDING: the two premium hosts are the boundary-RICHEST and pair-POOREST of the twelve — the rewrite price concentrates where the host's identity structure leans on its canon-boundary cells without the pair-junction mesh to carry it; the discriminator is IN the deposits and it is external (the miRNA-layer production error 4x, the boundary count, the pair deficit); deposited as results/exp273_outlier_hosts.json. REGISTERED NEXT (batch 32, derived): (a) exp274 THE PREMIUM MECHANISM — is the external signature the price itself or a correlate [the mediators' own regression: the premium vs mia_prod_err vs boundary count vs pair deficit, the 12-host table, the exp262 convention]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing)

## L252 — exp274 THE PREMIUM MECHANISM (C, 4/4, branch PRICE-MEDIATED — L251's registered next (a) EXECUTED; the body written by the run agent; landed at a37afd2): M1 PASS (the 12-host table complete; the mediators from exp273's field table by exact field names, the provenance chain sha-verified 5/5); M2 PASS (mia_prod_err Spearman 0.8905 >= 0.5 — the single mediator clears the bar alone; boundary count weak secondary, the pair deficit directionally present but weak at rho -0.1687 — the direction its name pre-names); M3 PASS (the full model's rank R2 0.7374; the symmetric shares mia 0.5634 / boundary 0.1476 / pair 0.0264 / unexplained 0.2626); M4 PASS (6 deposits READ-ONLY sha-recorded byte-unchanged; two-pass bit-identical; the deposit byte-identical across processes c8dbb4ee; the -60.0 floor asserted at exit; fingerprint 84ab1888c49de000); THE FINDING: the rewrite premium's carrier IS in the deposits — the hosts' multi-identity audit error prices the shelf (rho 0.89, share 0.56): the hosts whose identity audits err most pay the most for even a one-zone identity rewrite; the premium is not boundary-geometric (exp272) but audit-functional; deposited as results/exp274_premium_mechanism.json. REGISTERED NEXT (batch 33, derived): (a) exp275 THE AUDIT'S DIRECTION — is mia_prod_err mechanistically upstream of the premium or downstream of the same host defect [the conditioning test: the premium vs boundary count/pair deficit UNDER mia's conditioning; the multi-zone shelf re-examined under mia — exp272's rho 0.9912 depth offset re-read]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-274 (NINETEEN experiments, batches 22-32), ledger L234-L252, the 8-channel schema + the five activations + the substitution-event portrait + the premium mechanism complete — the next session's first dispatch derives from THIS line, no plan, no check-in

## L253 — exp275 THE AUDIT'S DIRECTION (C, 4/4, branch MIA-UPSTREAM + SHELF-SURVIVES — L252's registered next (a) EXECUTED; pre-registration 347b434 [gates fixed before any body — the docstring's A1-A4], the body written by the run agent, landed at dc86234): A1 PASS (the 12-host x 5-column table complete/finite; both premium shelves re-derived bit-exact from exp272's deposited grids; exp273's field table carried bit-exact; the provenance chains sha-verified exp273 5/5 + exp274 6/6, READ-ONLY); A2 PASS (exp229's GATE-K3 partial-correlation identity verbatim on the tied average ranks; all three partials finite; the unconditioned anchors bit-exact vs exp274's deposited rhos and exp272's 0.9912141845604473); A3 PASS on the pre-named discriminant — the geometric partials COLLAPSE under mia's conditioning [premium ~ boundary count | mia: +0.0526 -> -0.3242; premium ~ pair deficit | mia: -0.1687 -> -0.0157 — both |partial| < 0.5] while the SHELF SURVIVES [one-zone ~ multi-zone | mia: 0.9912 -> 0.9591 >= 0.9, reported at its own bar, never gating]: MIA-UPSTREAM — the audit error is the PROXIMATE carrier (conditioning on it absorbs everything the geometry set can see: exp273's H3/H5 separation covaries with the audit error rather than independently carrying the price), and the depth offset is a SECOND, mia-independent host property (the level is the audit's, the offset is not); A4 PASS (deterministic two-pass bit-identical; no wall-clock fields; 7 deposits READ-ONLY byte-unchanged; the -60.0 floor asserted at entry+exit; the deposit byte-identical across processes, fingerprint deb723e7b80f352d); THE MECHANISM LINE, COMPLETE: the premium is audit-functional (exp274) -> the audit error is the proximate carrier (exp275) -> the depth offset is a separate host property (exp275's surviving shelf); deposited as results/exp275_audit_direction.json. REGISTERED NEXT (batch 34, derived): (a) exp276 THE AUDIT'S OWN FACE — what makes mia_prod_err high on H3/H5 [the audit's own decomposition across the deposited records: which of exp243's adversarial battery arms' errs feed the audit error on the outlier hosts — one decomposition, zero new simulation]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-275 (TWENTY experiments, batches 22-33), ledger L234-L253 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L254 — exp276 THE AUDIT'S OWN FACE (C, 4/4, branch ARM-CONCENTRATED (P3 deep-band substitution) — L253's registered next (a) EXECUTED; pre-registration cdec428 [gates B1-B4 fixed before any body], the body written by the run agent, landed at 4610922): B1 PASS (the 48-record battery grid complete, zero rejections; the derived per-arm per-seed worsts == exp256's deposited rows 72/72 bit-exact; the provenance chains sha-verified exp273 5/5 + exp274 6/6 + exp275 7/7; 8 deposits READ-ONLY byte-unchanged); B2 PASS (the accounting identity: the arms' contributions c_k = s_k * a_h sum to the audit error 12/12, max residual 0.00e+00); B3 PASS on the pre-named discriminant — the battery's error mass is 94.20% P3 on H3 / 93.07% on H5 vs the cluster's dominant-share range [0.6909, 0.8482] (both outliers above the cluster max); canon-space arms carry ~none of it (P1 1.4%/1.7%, P2 4.4%/5.3%): mia_prod_err is high on H3/H5 because their defect lives IN THE DEEP-BAND PROGRAM SPACE — the audit's own MULTI-target read fails exactly where the deep substitution reads fail (3.68/3.24 and 3.35/2.88 mV there) while the mirror/boundary-chord perturbations cost <= 0.23 mV everywhere; the rank regression (P3 contribution, audit) +0.8905, full rank R2 0.9011, shares P3 0.673; B4 PASS (two-pass bit-identical; no wall-clock fields [exp243's runtime_s explicitly excluded]; the -60.0 floor asserted at exit; the deposit byte-identical across processes b96db869); THE MECHANISM LINE, CLOSED AT THE DEPOSITS' BOTTOM: price audit-functional (exp274) -> mia proximate (exp275) -> the audit's error mass 94% deep-band-space (exp276) -> the deep-band read fails specifically on the boundary-richest/pair-poorest hosts (exp273) -> the residual is the read's categorical response to the identity-structure rewrite (exp262-270); deposited as results/exp276_audit_own_face.json. REGISTERED NEXT (batch 35, derived): (a) exp277 THE DEEP-BAND BREAK FACE — why the deep-band programs break on the boundary-richest hosts [the P3 arm's own error decomposed by the exp208 cell-class machinery per host — exp256's decompositions partially carry it; the pre-named question: is the outlier hosts' deep-band error boundary-class or pair-class?]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-276 (TWENTY-ONE experiments, batches 22-34), ledger L234-L254 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L255 — exp277 THE DEEP-BAND BREAK FACE (C, 4/4, branch NEITHER — the deep-band break is CLASS-BLIND — L254's registered next (a) EXECUTED; pre-registration aa0d3c2 [gates D1-D4 fixed before any body], the body written by the run agent, landed at 63264f9): D1 PASS (exp256's 72 rows re-read complete 12x2x3; the mask semantics verified in-deposit 72/72 — a pre-registered disclosure: exp208's classify never assigns cls=2 on this battery, so the deposited CANON-BOUNDARY record is the non-PAIR-JUNCTION complement [INTERIOR empty] — read as deposited, never repaired); D2 PASS (the per-row accounting identity: the per-class frac_of_sq sums to 1, max dev 4.4e-16 vs the 1e-9 bar; the RMS-reconstruction max dev 0.004833 within the 0.0051 bar); D3 PASS on the pre-named discriminant — NEITHER branch: the outliers' class shares [H3 cb 0.1513 / pj 0.8487; H5 cb 0.2265 / pj 0.7735] do NOT both exceed the cluster's maxima [cb 0.1767, pj 0.9527] (margins -0.0255 / -0.1792); H5 even holds the LARGEST cb share of all 12 hosts while H3 sits mid-range: the deep-band failure is a ~7x AMPLIFICATION of the cluster-typical error mixture (P3's own err 3.68/3.36 mV vs ~0.50), not a boundary- or pair-class phenomenon; the mediator regression: the class shares carry ~none of mia_prod_err's rank variance (Spearman +/-0.1182 exact complements, full rank R2 0.0004) — the break MULTIPLIES the mixture, it does not shift its face; D4 PASS (two-pass bit-identical; the deposit byte-identical across processes 892e19d8; 8 deposits READ-ONLY byte-unchanged; the -60.0 floor asserted at exit); THE FINDING: the mechanism line's final turn — the outlier hosts' deep-band break is CLASS-BLIND: the same error mixture as every host, amplified ~7x; the amplification's carrier lives ABOVE the cell-class level, in the deep rows' program-vs-target identity structure (the exp262-270 line's own territory); deposited as results/exp277_deep_band_break_face.json. REGISTERED NEXT (batch 36, derived): (a) exp278 THE AMPLIFICATION FACTOR — the ~7x is itself the measurement [the amplification ratio per host (the P3 mean err / the P1+P2 mean err, zero-knob) vs mia_prod_err across the 12 hosts: is the multiplier the audit error's own scale? one regression, zero new simulation]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-277 (TWENTY-TWO experiments, batches 22-35), ledger L234-L255 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L256 — exp278 THE AMPLIFICATION FACTOR (C, 4/4, branch MIA-SCALED — L255's registered next (a) EXECUTED; pre-registration b42fbc0 [gates G1-G4 fixed before any body], the body written by the run agent, landed at a445443): G1 PASS (exp256's 72 rows re-read complete; the per-host means bit-exact vs exp273/exp276/exp277/exp272/exp243/exp255's records where present; the provenance chains sha-verified 5/5+6/6+7/7+8/8+8/8); G2 PASS (the zero-knob ratio: R = m_P3 / m_P12 with the denominator the POOLED P1+P2 mean [gated as not-the-per-seed-max; the max variant recorded audit-only, strictly above the pooled mean on all 12 hosts]); G3 PASS on the pre-named discriminant — MIA-SCALED: Spearman(R, mia_prod_err) = 0.7250 >= 0.5 [mia tested first, the pre-named precedence], while the geometry instrument is REFUTED at the amplification level too [Spearman(R, boundary count) = -0.0596, after exp272's premium-level 0.0526]: the amplification ratio H3 32.47 / H5 26.85 vs the cluster's [4.47, 11.17], and the amplification lives in the NUMERATOR (the substituted means 3.68/3.36 vs ~0.50 — the canon program errs are host-flat); the rank regression: full R2 0.7803, shares mia 0.5683 / bc 0.2119 / unexplained 0.2197; G4 PASS (11 deposits READ-ONLY byte-unchanged; two-pass bit-identical; the deposit byte-identical across two processes 3a7fa8b0; the -60.0 floor asserted at exit; one body-side disclosure: exp273's carry reproduces bit-exactly only via plain sum/6 in deposited order [np.mean drifts a last-ulp on H4/H6] — disclosed in-code, matched 12/12); THE FINDING: the amplification is MIA-SCALED — the deep-band break's SIZE is the hosts' audit error scale itself (the audit error IS the amplification's measure, not merely its correlate); the deep-band line CLOSES: audit error = P3-space defect (exp276) -> class-blind break (exp277) -> mia-scaled size (exp278); deposited as results/exp278_amplification_factor.json. REGISTERED NEXT (batch 37, derived): (a) exp279 THE AUDIT-ERROR ORIGIN — mia_prod_err is the read's OWN multi-target audit on the battery media [what makes the AUDIT err 4x on H3/H5 when the single-target reads err ~equal? the audit's MULTI-target aggregation vs the single-row errs' decomposition across exp243's candidate records — one decomposition, zero new simulation]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-278 (TWENTY-THREE experiments, batches 22-36), ledger L234-L256 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L257 — exp279 THE AUDIT ERROR'S ORIGIN (C, 4/4, branch AUDIT-MAX — L256's registered next (a) EXECUTED; pre-registration 4a8d985 [gates G1-G4 fixed before any body], the body written by the run agent, landed at 7ce8be6): G1 PASS (the 48-candidate grid + 12 audit records complete; exp256's 72 rows cross-checked bit-exact; the mia carry bit-exact; the outlier pre-name asserted x3 deposits; the provenance chains sha-verified exp276 8/8 + exp273 5/5; 9 deposits READ-ONLY byte-unchanged); G2 PASS (the audit records asserted ATOMIC as deposited — key set exactly {seed, bit_identical, prod_err, f_max}, no components to sum, never repaired; the battery's own identities asserted 48/48 + 72/72; exp276's masses bit-exact 36/36); G3 PASS on the pre-named discriminant — AUDIT-MAX: 10/12 hosts have the audit error within the 10% bar of max_arm_err [cluster |gap|/a in [0, 0.0204]; the argmax arm is the P3 deep-band substitution on ALL 12 hosts], 0/12 hosts EXCESS [the multi-target interference face REFUTED — the simultaneous multi-target read never costs more than the worst single-target read], and the outliers H3/H5 are the residual 2 hosts erring BELOW the worst single-target arm [excess ratios 0.576/0.681 — on the outliers the aggregation is PROTECTIVE]; the robustness grain agrees [exp276's masses: counts 10/0/2]; THE AGGREGATION FORM IS MAX-LIKE, NOT SUM-LIKE; G4 PASS (two-pass bit-identical; the deposit byte-identical across processes 3b7dd6a5; no wall-clock fields; the -60.0 floor asserted at exit; fingerprint 20cff13fb5147ec0); THE FINDING: the ~4x audit error rides the worst arm — the audit's prod_err IS the deep-band substitution's own read error re-aggregated, closing the exp276->277->278->279 mechanism line AT THE ORIGIN: the outlier hosts' premium = their deep-band read error = the audit's max-arm read = the boundary-richest/pair-poorest structure's exposure to the identity-structure rewrite; every level of the chain is now measured and named; deposited as results/exp279_audit_error_origin.json. REGISTERED NEXT (batch 38, derived): (a) exp280 THE CHAIN'S HEAD — the origin question moves one level up: why do the boundary-richest/pair-poorest hosts read the deep-band program worst [the exp277 class-blind ~7x amplification's structure vs the hosts' own adjacency records: the boundary-rich topology's deep-band read is the last unopened box — one decomposition over exp243's/exp256's records plus the rebuilt base adjacencies' own structural fields (degree spectra, clustering), zero new simulation]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-279 (TWENTY-FOUR experiments, batches 22-37), ledger L234-L257 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L258 — exp280 THE CHAIN'S HEAD (C, 4/4, branch TOPOLOGY-ABSENT with an anti-aligned face named — L257's registered next (a) EXECUTED; pre-registration 421c742 [gates G1-G4 fixed before any body], the body written by the run agent, landed at 4dd3202): G1 PASS (the 12 base adjacencies rebuilt deterministically, sha-asserted against exp243's records 12/12 + edges 12/12 + the classify boundary count dual-carried vs exp272+exp278 + the canon identity + H0==H1); G2 PASS (the six zero-knob structural fields per host; the 12-host table assembled with the deep-band errs [bit-exact vs exp276's m_P3 == exp273's field table == exp278's m_P3] and exp278's amplification ratios [bit-exact 12/12]; one pre-body disclosure per the exp277 precedent: the deposited seeds' chords form no triangles — the clustering field identically 0.0 on all 12, asserted, excluded from the max by the degeneracy, never chosen); G3 PASS on the pre-named discriminant — TOPOLOGY-ABSENT: no field reaches the 0.5 SIGNED bar against the deep-band err [deg_mean -0.3993, deg_max -0.4398, deg_spread -0.4398, boundary_degree_mean -0.6081, pair_support_density -0.3993]; the ANTI-ALIGNED FACE named audit-only: the boundary cells' own degree mean at |rho| 0.6081 NEGATIVE — H3/H5 hold 47/48 boundary cells but their boundary cells are the cluster's CHORD-POOREST [1.596/1.563 vs [1.5, 1.897]]; the ratio regressions agree [max |rho| 0.7263, same field]: the deep-band mechanism line stays MIA-CARRIED (exp278), not topology-carried; G4 PASS (two-pass bit-identical; the deposit byte-identical across processes d157fc89; no wall-clock fields; the -60.0 floor asserted at exit); THE FINDING: the chain's head does not open into the adjacency's topology — the exposure is not the boundary-RICHNESS (a count) nor any deposited structural field, but something the count correlates with and the topology does not carry; the anti-aligned face is the honest residue: boundary-RICH yet chord-POOR boundary cells, the reverse of the pair-mesh protection the canonical story would predict; deposited as results/exp280_chain_head.json. REGISTERED NEXT (batch 39, derived): (a) exp281 THE ANTI-ALIGNED FACE TESTED — the boundary cells' chord-poverty as the premium's test [the field IS deposited and |rho| 0.61 — the pre-named regression: the premium and the amplification against boundary_degree_mean, the signed bar 0.5 — if it clears, the mechanism line re-opens at the chord level; if not, the line stands closed at mia and the residual's origin is formally OUTSIDE the deposited host records]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-280 (TWENTY-FIVE experiments, batches 22-38), ledger L234-L258 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L259 — exp281 THE ANTI-ALIGNED FACE TESTED (C, 4/4, branch CHORD-ABSENT — L258's registered next (a) EXECUTED; pre-registration a52a14a [gates G1-G4 fixed before any body], the body written by the run agent, landed at 402f9b6): G1 PASS (the 12 bases sha-asserted 12/12 vs exp243 + the dual-carried boundary counts + the canon identity + H0==H1; the T1 mean identity 12/12; the T3 4-way mia carry bit-exact across exp243/exp276/exp279/exp273; the outlier pre-name 6-way; the provenance chains verified across six deposits); G2 PASS (the recomputed field == exp280's deposited field table BIT-EXACT 12/12 — the definition never re-fit; the ties census: 11 levels, the H0/H1 echo pair); G3 PASS on the pre-named discriminant — CHORD-ABSENT: max signed rho -0.5359 [by target: T1 premium -0.6000 / T2 amplification -0.7263 / T3 mia -0.5359] — nothing reaches the signed +0.5 bar; the anti-aligned face crossed on 3/3 targets [hosts with FEWER boundary-cell chords read premium/amplification/audit HIGHER — the chord is an anti-correlate on every premium face, a carrier on none]: the line STANDS CLOSED at mia and the premium's origin is formally OUTSIDE the deposited host records; G4 PASS (15 deposits READ-ONLY byte-unchanged; two-pass bit-identical; the deposit byte-identical across processes 3bf29047d853b236c; no wall-clock fields; the -60.0 floor asserted at exit; the docstring pinned to a52a14a asserted entry+exit); deposited as results/exp281_antialigned_face.json. THE MECHANISM LINE, FINAL FORM (batches 27-39): the substitution's residual is deterministic-per-instance (exp262), arm-carried (0.757), not target-geometry (exp265), not law-closable (exp266), not stage-decomposable (exp267/268), not voltage-dosed (exp269), a step in event size (exp270), priced per-host (exp271/272), audit-functional (exp274), mia-proximate (exp275), P3-space (exp276), class-blind (exp277), mia-scaled (exp278), max-like at origin (exp279), topology-absent (exp280), chord-absent (exp281) — the premium's origin is formally outside every deposited host record; the next instrument must generate NEW host-level state. REGISTERED NEXT (batch 40, derived): (a) exp282 THE NEW-STATE INSTRUMENT — the one host-level property the deposits never recorded: the deep-band read's own TRAJECTORY structure [the executor's per-step convergence traces on the substituted rows, recorded fresh per host (the state-carrying read already returns final_state; the trace is one flag's width) — does the outlier hosts' walk converge differently? the first genuinely new measurement since exp269]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-281 (TWENTY-SIX experiments, batches 22-39), ledger L234-L259 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L260 — exp282 THE TRAJECTORY STRUCTURE (C, 4/4, branch TRAJECTORY-CARRIED — L259's registered next (a) EXECUTED; the first genuinely NEW measurement since exp269; pre-registration 3c354c2 [gates G1-G4 + the S0 anchor fixed before any body], the body written by the run agent, landed at 8ca252e): G1 PASS (the 12 bases rebuilt sha-asserted per the exp269/exp280 precedent); G2 PASS (the trace completeness: one entry per cell commit, 272-292 per row, post-walk settle excluded; the disclosed form — exp142's execute_signed records nothing per-step, so the pre-named fallback took the state-carrying replica pattern: the walk copied byte-similar into _execute_signed_traced with exactly the per-step full-frame RMS read added, RNG/dt/canon/order/commits untouched, exp142 NOT modified); the S0 ANCHOR PASSED (the trace-run reproduced exp256's 72 deposited substituted errs bit-exact — errs + verified flags — the trace form is INERT on the deposited machine); G3 PASS on the pre-named discriminant — TRAJECTORY-CARRIED: the walk's own END RMS (pre-settle) clears the signed 0.5 house bar against BOTH targets [walk_end_rms ~ mia_prod_err +0.8826; walk_end_rms ~ one_zone_premium +0.8807] — the STRONGEST carrier yet named, stronger than any topology field [exp280's best was -0.6081 anti-aligned]; the other summaries do not carry [last10_slope +0.18/+0.21; conv_step -0.34/-0.16]; the audit-only lead: the cluster's curve first drops below 2x final at the walk's very end [~289/292] while H3/H5 cross EARLY [220/239] — the outlier walks COMMIT INTO THEIR WRONG PATTERN EARLY; G4 PASS (two passes bit-identical across processes e3c1e49e1889a010; the deposit byte-identical across merge runs 4ef15f00; no wall-clock fields; 4 source deposits READ-ONLY byte-unchanged; the -60.0 floor asserted at exit; fingerprint 9a77b24019831e9a); deposited as results/exp282_trajectory_structure.json. THE FINDING: the premium's carrier is the walk's own convergence state — the outlier hosts' executor walks end further from target BEFORE the audit ever reads them; the audit error (exp274-279) is the walk's end state re-aggregated, and the walk's end state is the first carrier stronger than mia itself; REGISTERED NEXT (batch 41, derived): (a) exp283 THE EARLY-COMMIT FACE — the audit-only lead's promotion to a gate [the convergence-point summary's distribution: cluster ~289/292 vs outliers 220/239 — is the early-commit property categorical (a gap, not a continuum) and does IT predict the premium better than the end RMS?]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-282 (TWENTY-SEVEN experiments, batches 22-40), ledger L234-L260 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L261 — exp283 THE EARLY-COMMIT FACE (C, 4/4, branch CONTINUUM with the categorical gap recorded — L260's registered next (a) EXECUTED; pre-registration 109ab52 [gates G1-G4 fixed before any body], the body written by the run agent, landed at d617b85): G1 PASS (the provenance chains sha-verified 13/13; exp282's 72 traces complete per row [len == walk_steps, finite, the trace_sha256s 72/72]; all three summaries RE-DERIVED bit-exact from the deposited traces; the six deposited rhos reproduced bit-exact 6/6; the carries bit-exact mia 12/12 + premium 12/12 x2); G2 PASS (the pre-named ordering held HARD: H3 219.67 / H5 239.17 are the two smallest conv_step means; the gap ratio 288.33/239.17 = 1.2056 >= 1.2 — CATEGORICAL-GAP); G3's carry component FAILED (the early-commit orientation carries neither target at the bar: max e_t +0.3432 [mia] < 0.5, e_premium +0.1565 — END-RMS-DOMINATES on both [|end| 0.88/0.88 vs |early| 0.34/0.16], recorded audit-only); G4 PASS (two-pass bit-identical 55617b25; the deposit byte-identical across processes b2460d8f; no wall-clock fields; the -60.0 floor asserted at exit); deposited as results/exp283_early_commit_face.json. THE FINDING: the early-commit property IS categorical — a clean 1.21x gap, no continuum between the cluster's ~288-291 and the outliers' 220/239 — but WHERE the walk ENDS [the end RMS, exp282] carries the premium; where it SETTLES EARLY does not; the exposure lives in the walk's endpoint, not its schedule. REGISTERED NEXT (batch 42, derived): (a) exp284 THE ENDPOINT'S COMPOSITION — the end-RMS carrier decomposed [which cells' errors compose the walk's end RMS on the outlier hosts — the per-cell state is IN exp282's traces; the exp208 class machinery on the end state: is the outlier end-RMS's mass boundary-class now that the walk-level view replaced the decode-level one [exp277 said class-blind at the decode level; the walk level is the new surface]]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-283 (TWENTY-EIGHT experiments, batches 22-41), ledger L234-L261 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L262 — exp284 THE ENDPOINT'S COMPOSITION (C, 4/4, branch WALK-CLASS-BLIND — L261's registered next (a) EXECUTED; pre-registration e70ae65 [gates G1-G4 fixed before any body], the body written by the run agent, landed at f3ca053 [one amended push disclosed: the deposit-fingerprint prefix in the commit message corrected BEFORE anything referenced it, force-with-lease, linear history, tree bytes never changed]): G1 PASS (the 12 bases sha-asserted x5 + H0==H1 + f_max; the deep targets/medium shas 72/72; exp282's re-read: the traces complete, the trace shas recomputed, the three summaries re-derived bit-exact 72/72 x3; the mia/premium carries 12/12 x2; the provenance chains 28/28; 6 deposits READ-ONLY byte-unchanged); G2 PASS (the S0 anchor: the re-run's final errs reproduce exp256's deposited substituted errs bit-exact 72/72 + the verified flags 72/72, AND exp282's deposited walk reproduced bit-exactly [the trace_sha256s 72/72, walk_end_rms float-identical 72/72] — the decomposition is of the SAME walk exp282 traced; the accounting identity 72/72, max residual 5.33e-15; the classification anchor 36/36; the settle gap max 0.0079 mV [PRE-settle carrier vs POST-settle end state, disclosed pre-body]); G3 PASS on the pre-named discriminant — WALK-CLASS-BLIND: margin_cb -0.0022 [H3 0.1723 / H5 0.2680 vs the cluster max 0.1745], margin_pj -0.2190 — the pre-named 0.05 concentration bar NOT crossed, no weak-ordering face: the end-RMS carrier's +0.88 exposure does NOT live in CANON-BOUNDARY or PAIR-JUNCTION cells at the walk level either, matching exp277's decode-level NEITHER; the audit-only pure-ring face named, never gating [H3 0.1501 / H5 0.1601 are the two highest boundary-ring shares, margin +0.0406, sub-bar]; G4 PASS (two-pass bit-identical across processes; no wall-clock fields [key + blob scans]; the docstring/header pinned; the -60.0 floor asserted at exit); deposited as results/exp284_endpoint_composition.json. THE FINDING: the walk-level break is class-blind like the decode-level one — the endpoint's MAGNITUDE carries the premium (exp282), its cell-class composition does not (exp284); the only live lead is the sub-bar pure boundary-ring ordering (+0.0406, named never gated). REGISTERED NEXT (batch 43, derived): (a) exp285 THE PURE-RING GRAIN — the boundary-ring share's own test at the pre-named bar [the ring cells (the boundary cells' immediate non-boundary neighbors — the zero-knob ring definition) as the end-RMS mass's carrier: the one sub-bar lead promoted to a gate, pure re-read + the same traced replica]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-284 (TWENTY-NINE experiments, batches 22-42), ledger L234-L262 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L263 — exp285 THE PURE-RING GRAIN (C, 4/4, branch RING-ABSENT — L262's registered next (a) EXECUTED; pre-registration dffdc37 [gates G1-G4 fixed before any body], the body written by the run agent, landed at c47cc77): G1 PASS (exp284's landed body reused verbatim — the traced replica, the host rebuild, the classify/decompose conventions; the only addition the ring mask; the anchors: the fresh errs == exp256's deposited errs bit-exact 72/72 AND exp284's per-class shares + trace shas reproduce bit-exact 72/72 — the same walk); G2 PASS (the ring disjoint from the boundary set and covering no boundary cells 72/72, index + mask forms; the partition + nonempty 72/72; the identity residual max 5.3e-15); G3 PASS on the pre-named discriminant — RING-ABSENT: rho_ring~mia +0.0552, rho_ring~premium -0.0386, no anti-aligned crossing — the grain screen is now COMPLETE at three levels [the label classes exp277/284, the boundary's own share exp284's sub-bar lead, the ring around it exp285] — ALL exposure-blind; the carrier stays the walk's endpoint magnitude (+0.88); the audit-only face: the outliers hold the two highest mean ring shares [H3 0.1928 / H5 0.1604 vs the cluster max 0.1205, margin +0.0399] but the 12-host rank correlation ~ 0 [the cluster shares spread 0.033-0.121 without tracking mia/premium] — an outlier-vs-cluster ordering, not a carrier; exp284's +0.0406 margin recomputed bit-exact beside; G4 PASS (two-pass payload sha identical 280bd527; 5 source deposits byte-unchanged; the -60.0 floor asserted at exit; the docstring pinned to dffdc37; fingerprint adb4933ea1569aed); deposited as results/exp285_pure_ring_grain.json. THE GRAIN SCREEN'S VERDICT (the composition question, closed at every grain): the premium's carrier is the walk's endpoint MAGNITUDE alone — no cell class, no ring, no share decomposes it; the mechanism line's remaining live object is exp282's walk_end_rms itself. REGISTERED NEXT (batch 44, derived): (a) exp286 THE ENDPOINT'S DOSE — the end-RMS carrier's own parameter [the walk's step budget: does the end RMS depend on the walk's LENGTH (steps_per_cell) — one pre-named ladder {4, 8 [the production default], 16} x the 12 hosts x 3 seeds, the traced replica; if the outlier hosts' end state is step-limited, the premium is a BUDGET artifact; if step-invariant, the premium is the walk's fixed point — the last structural question the walk-level surface can ask]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-285 (THIRTY experiments, batches 22-43), ledger L234-L263 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L264 — exp286 THE ENDPOINT'S DOSE (C, 4/4, branch BUDGET-INVARIANT — L263's registered next (a) EXECUTED; pre-registration 12b87b2 [gates G1-G4 fixed before any body], the body written by the interrupted dispatch and landed by the salvage-verify respawn [zero defects; the stale interrupted-session caches disclosed + cleared first, the fresh payloads reproducing their shas bit-exact — unplanned cross-session determinism]; landed at 4e504de): G1 PASS (the S0 anchor: the budget-8 re-run's final errs reproduce exp256's deposited substituted errs bit-exact 72/72 AND exp282's walk_end_rms + trace shas bit-exact 72/72 + the per-host means 12/12; the bases 12/12 vs exp243; the deep targets/medium shas 72/72; the carries mia+premium 12/12; the chains 20/20; 5 deposits byte-unchanged); G2 PASS (216/216 decodes across the ladder {4, 8, 16}; walk_steps identical across budgets per row 72/72 [272-292 — the walk ORDER untouched, only the per-cell loop bound parameterized, disclosed]; the delivered dose 216/216; A3 + trace integrity per budget); G3 PASS on the pre-named discriminant — BUDGET-INVARIANT: N_inv 12/12 [both ratios within 1.0 +/- 0.1 on every host], no outlier/cluster separation [max margin -0.0192 < 0.10] — H3/H5 are the FLATTEST faces [r4 0.9999/1.0021, r16 1.0012/1.0035] vs the cluster's r16 up to 1.0778; the audit-only dose face recorded [rho(16)~mia +0.2522 decays while the magnitudes stay put]; G4 PASS (the payloads bit-identical per budget across processes [b4 9815859c, b8 c6737f90, b16 2f0d3834]; no wall-clock fields; the docstring/header pinned to 12b87b2; the -60.0 floor asserted at exit; the deposit fingerprint a41cb7064cbd2e55); deposited as results/exp286_endpoint_dose.json. THE FINDING: the end-RMS carrier is the walk's FIXED POINT, not a budget artifact — the outlier hosts' premium persists at every step budget (their walks end at the same wrong place with 4, 8, or 16 steps per cell); the last structural question the walk-level surface could ask is answered: the premium is the walk's fixed point property. REGISTERED NEXT (batch 45, derived): (a) exp287 THE FIXED POINT'S IDENTITY — the walk's fixed point IS the executed program's own identity structure [the walk commits each cell to the executed program's spec — the final question: is the fixed point's error the PROGRAM's own self-consistency limit (the compiled program re-reads its own writes imperfectly) — testable by re-reading the executed program's writes as the target [the program-vs-its-own-writes identity, one battery, the traced replica]; if the fixed point's error against the program's own writes ~ 0, the premium is the program's IMPERFECT SELF-KNOWLEDGE, closing the chain at the compiler]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-286 (THIRTY-ONE experiments, batches 22-44), ledger L234-L264 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L265 — exp287 THE FIXED POINT'S IDENTITY (C, 4/4, branch SELF-DRIFT with the COMMITTED-PATTERN carrier named — L264's registered next (a) EXECUTED; pre-registration 1f6f07f [gates G1-G4 fixed before any body], the body written by the run agent [the dispatch landed before the infra timeout]; landed at faa3d02): G1 PASS (the S0 anchor: the fresh errs reproduce exp256's deposited substituted errs bit-exact 72/72 + verified 72/72 AND exp282's walk_end_rms bit-exact [walk_end + trace sha256 72/72 — the SAME walk exp282 deposited, proving the commit recording side-effect-free; err_exact 72/72; the per-host means 12/12]); G2 PASS (the zero-knob self-consistency definition: n_commits == walk_steps == the trace length 72/72, the commit indices unique 72/72, the replica-side write-set coverage 72/72, the digests recorded 72/72, sc_rms finite + the denominators > 0 72/72, the A3 convention + the S* lock 72/72); G3 PASS on the pre-named discriminant — SELF-DRIFT: the self-consistency error sc_rms [the RMS over the committed cells between the post-settle final state and the REPLAY of the recorded commits, zero knobs] is 2.5%-20.4% of the program-vs-target gap on EVERY host [N_sc 0/12; the between-commit dynamics + the settle move the committed cells by ~0.06-0.10 mV RMS on all 12 hosts — the exp284 disclosed settle gap's AMPLIFIED proper-norm form (the per-cell committed read exposes it ~11x)]; THE DRIFT IS EXPOSURE-BLIND [rho(mean_sc)~mia +0.0315 / ~premium -0.2491] while the COMMITTED PATTERN ITSELF carries the exposure [rho(mean_cvt)~mia +0.8616 / ~premium +0.7790 — the commit-vs-target RMS on the program's own write set, beside exp282's +0.88 end-RMS carrier]; the outliers H3/H5 hold the SMALLEST sc fractions [0.0254/0.0307 — their 6-7x gaps dilute the same ~0.09 mV drift]; THE SELF-KNOWLEDGE FACE: every one of the 20802 commits drew from the SPEC layer [spec 20802 / canon 0 / parent 0] — the program writes its own spec-layer values + commit noise, never inheriting from the canon or the parent at the production floor; G4 PASS (two-pass bit-identical, payload sha 48e357ad89dd3f18; no wall-clock fields; the docstring/header pinned to 1f6f07f asserted entry+exit [doc sha 0c8db6705c55691f / header sha 920ac514d5c762f3]; 5 deposits READ-ONLY byte-unchanged; the -60.0 floor asserted at exit; fingerprint 93b6ab4249510548); deposited as results/exp287_fixed_point_identity.json. THE MECHANISM LINE, CLOSED AT THE COMPILER: the premium lives in WHAT the program commits — the compiler's spec layer — with a small exposure-blind execution drift on top [the walk lands where it commits +/- ~0.09 mV of host-typical drift]; the chain, every level measured and named: the residual [exp262-270] -> the price per host [exp271/272] -> the audit error [exp274/275] -> the P3 space [exp276] -> the class-blind amplification [exp277/278] -> the max-like origin [exp279] -> the endpoint magnitude [exp282-284] -> the budget-invariant fixed point [exp286] -> the spec layer's committed pattern [exp287]; the boundary residual's full genealogy runs from the ledger's frontiers down to the compiler's own writes. REGISTERED NEXT (batch 46, derived): (a) exp288 THE SPEC LAYER'S FACE — what makes the compiler's spec-layer commits deep-band-host-dependent [the compiled programs' own spec maps for the deep-band targets on H3/H5 vs the cluster — the programs are IN the deposits (the read stack's spec inputs); one decomposition, zero new simulation]; (b) the standing repair line: the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record written into the repo docs (the user's directive, standing); (d) the session-state note: this session landed exp256-287 (THIRTY-TWO experiments, batches 22-45), ledger L234-L265 — the next session's first dispatch derives from THIS line, no plan, no check-in

## L266 — exp288 THE SPEC LAYER'S FACE (pre-registration 6ae42a3 [gates G1-G4 fixed before any body, PUSHED]; the body: the fleet died twice pre-body on dispatch, the MAIN AGENT's two-death body was assembled but the context window ended before its landing run — THE BODY IS THE NEXT SESSION'S FIRST ACTION, the pre-registration stands, the design is complete in the docstring [exp287's traced replica + commit recording reused verbatim at budget 8; the per-cell commit-error class decomposition by exp208's classify; the concentration ratios R_c = frac_of_sq / cell_share pooled per host; the branch SPEC-GEOMETRIC iff N_conc >= 10 at the R_c >= 1.50 bar / else SPEC-UNIFORM; the S0 anchor: the errs reproduce exp256's deposited substituted errs bit-exact AND exp287's deposited commit layer bit-exact]; machinery precedents: exp287's/exp286's/exp284's landed bodies; no tuning, no gate changes). THE SESSION RECORD (batches 22-45 closed, exp256-287 THIRTY-TWO experiments landed, ledger L234-L265): the architectural override LANDED (exp257 SCHEMA-8-NATIVE — the 8-channel named state, bit-exact at every legacy call site); all five dormant channels activated and honestly INERT (exp258/259/261/263/264); the pair levers refuted (exp259/260); the substitution event's complete genealogy (exp262-287): deterministic-per-instance, arm-carried 0.757, not target-geometry, not law-closable, not stage-decomposable, not voltage-dosed, a step in event size, priced per-host, audit-functional, mia-proximate, P3-space, class-blind at every grain, mia-scaled, max-like at origin, topology-absent, chord-absent, budget-invariant, and CLOSED AT THE COMPILER'S SPEC LAYER (the premium lives in WHAT the program commits); the mechanism chain runs from the ledger's frontiers down to the compiler's own writes, every level measured and named. STANDING FRONTIERS: (a) exp288's body [THIS pre-registration, the immediate next action]; (b) the aggregation family's boundary pin (exp251/253); (c) the BETSE design-reference record (the user's directive — the reference tree at /home/z/my-project/betse-reference, consumed by exp257's schema design and exp261's kinetics port, still to be recorded in the repo docs); (d) exp287's audit-only leads [the early-commit gap 1.21x categorical-but-non-carrying; the drift exposure-blind]. THE NEXT SESSION'S FIRST DISPATCH: exp288's body under 6ae42a3, then derive — no plan, no check-in

L267 | exp288 — THE SPEC LAYER'S FACE | 4/4 gates G1-G4 (4 PASS / 0 REFUTE) | BRANCH: SPEC-UNIFORM — the commit error's class decomposition is CLASS-BLIND: N_conc 0/12 (the per-host POOLED R_max within [1.0003, 1.1253] vs the pre-named CONC_BAR 1.50; CONC_MIN_HOSTS 10) — the committed pattern's host-dependence does NOT live in the classify-class geometry of the commit error, the SIXTH class-blind level screened (exp277's decode NEITHER, exp284's walk CLASS-BLIND, exp285's ring ABSENT, exp287's drift exposure-blind, and now the spec layer's own commit-error face UNIFORM): the host-dependence enters through the DRAW STREAM's positions and the walked count, not through any class structure | THE DECOMPOSITION (zero knobs, the accounting identity 72/72): e_i = commit_i - T_i is exactly ONE commit-noise draw (the landed write path: phi_spec == target bit-exact at the write), and its class decomposition reconstructs cvt_rms^2 exactly (sum_c sum_sq_c / n_write == cvt_rms^2 within 1e-6*max(1, cvt^2) 72/72; the fracs sum to 1 72/72; the clean masks disjoint+covering 72/72; the exp208-label cls-2 count == 0 72/72 — the exp277/exp284 disclosure holds by construction: the ring backbone's pair edges put every cell at deg >= 2, the interior rides cls 0/1); pooled per host: the boundary class holds R within [0.866, 1.125] — no class holds >= 1.5x its committed-cell share of the squared commit error on ANY host (the per-ROW probe-level fluctuation reaches 1.72 on H5's single rows — the pooling killed it exactly as pre-named) | THE COMMIT-VALUE FACE (audit-only): the pooled named-base fraction (the commits whose base IS the spec's named -60.0) spans [0.128, 0.168] across hosts; the EXACT-LANDING COUNT #{commit_i == -60.0} == 0 bit-exact over all 20,802 commits and #{commit_i == s_i} == 0 — NO commit lands exactly on its base: the noise never vanishes, the committed pattern is base + draw everywhere | THE ERROR MOMENTS (audit-only): the pooled |e| <= COMMIT_NOISE fraction within [0.679, 0.691] across hosts — the Gaussian sigma face of the pure draws | THE ANCHOR REGRESSIONS (asserted == exp287's deposited rhos BIT-EXACT, fail=STOP): rho(mean_cvt)~mia +0.8616 / ~premium +0.7790 — 2/2 bit-exact, the exp287 carry holds at the assembly level | THE DRAW-STREAM FACE (audit-only, RECORDED, never gating — BODY-LANDING DISCLOSURE per the exp231 precedent: the docstring's narrative 'asserted fail=STOP' form superseded by G3's binding audit-only placement; the machinery's own anchored deposit already showed the cross-instance identity holds only on a subset): 22/36 cross-instance cvt ties — the intra-walk draw consumption is STATE-COUPLED, not purely structural (the commit draws ride the shared stream but the dynamics' consumption between commits depends on the trajectory); 5 (dt, walked-count) groups, 2 multi-host | THE S0 ANCHOR (G1): the fresh errs reproduce exp256's deposited substituted errs bit-exact 72/72 (the verified flags 72/72) AND exp282's walk_end_rms bit-exact (walk_end 72/72, trace sha 72/72 — the SAME walk exp282 deposited, err_exact 72/72, the per-host means 12/12) AND exp287's COMMIT LAYER bit-exact (the commit-sequence digests 72/72 — the SAME commits exp287 recorded, cvt_rms 72/72, n_commits 72/72, sc_rms 72/72, the per-host mean_cvt 12/12) | the carries: mia 12/12 + premium 12/12 (exp273's field table == exp243's own records; exp272 == exp273's carry) | the 12 bases rebuilt sha-asserted vs exp243 12/12 (graph_path for H0/H1 — H0 echoes H1 bit-exactly, asserted; small_world at the deposited rewire seeds), the deep targets 72/72, the medium shas 72/72 | G2: n_commits == walk_steps == the trace length 72/72, the commit indices unique 72/72, the write-set coverage 72/72, the digests recorded 72/72, the values finite 72/72, the censuses sane 72/72, the A3 convention 72/72, the trace integrity 72/72, the TA3 convergence points 72/72, the S* lock reads 72, the settle gap max 0.0079 mV (audit-only) | G4: two-pass bit-identical (in-process, payload sha equal across passes, core sha equal), no wall-clock fields, docstring+header pinned to 6ae42a3 (doc sha 09eacfe5... / header sha 2ca1e109...), 6 deposits READ-ONLY byte-unchanged (exp243/256/272/273/282/287), the provenance chains sha-verified 25/25 (exp243 4 + exp256 3 + exp272 4 + exp273 5 + exp282 4 + exp287 5), NEURAL_SPEC_MIN == -60.0 asserted at exit | deposited results/exp288_spec_layer_face.json | body written by the main agent under the two-death rule (the window closed before the body in the prior session), gates untouched, pre-registration 6ae42a3 | REGISTERED NEXT: the spec layer's face is UNIFORM — the class-blindness now spans the decode, the walk, the ring, the drift, AND the commit error itself; the remaining frontier is NOT geometric: (a) the DYNAMICS batch (the five inert channels' evolution rules — extend step()/regrow()/maintain() to act on the schema's channels, each extension pre-registered as its own experiment; the schema exists, the dynamics don't); (b) the HISTORY-REGISTER retest (Sediqi 2026, bioRxiv 2026-06-23.733978: ionic-exposure history shapes voltage/chromatin responses — a persistent register across walks could reframe the schema-only inert results as a missing-variable artifact; converges with Blattner-TAS's hidden-state register, bioRxiv 2026-04-03.715890, github.com/marcelbtec/tasmorpho); (c) the write-time vs read-time ionic stress split (Tazumi 2026, APA: salt exposure disrupts memory RETRIEVAL in D. japonica — the stack analog runnable as-is on the commit-noise machinery); (d) the P1 Sephirotic 8-channel test (Zenodo 19042388's own paper25_results.json deposited by the search wave — 7+1 partial, p_null 3.9e-4 — the pre-registered P1 test now unblocked).

L268 | batch-47 pre-registrations (gates fixed before any body): exp289 THE HISTORY-REGISTER PORT (the architectural step — the commit history as a persistent per-cell register phi_history populated at each write, NOTHING reads it at defaults, the bit-exact zero-delta proved on the 72-row battery 72/72; the first history-carrying activation: the ctx coupling re-run reading the self-history at exp258's grid {0, 0.25, 0.5, 1.0} with the g=0 within-run control; the branch HISTORY-CARRIED iff the mean err improves on >= 10/12 hosts at some g > 0 / else HISTORY-INERT; Sediqi 2026 + Blattner-TAS 2026's convergent hidden/history state, L267's (b)); exp290 THE STRESS-TIMING SPLIT (the write-time vs read-time ionic stress on the commit machinery — the depolarized -35.0 pin during the WALK only (A1, the storage face) vs during the SETTLE only (A2, the retrieval face) vs the -60.0 anchor (A0, the S0 bit-exact 72/72); the paired deltas over the same 72 rows; the branch RETRIEVAL-SIDE iff A2 degrades more than A1 by the 0.05 mV margin (Tazumi 2026's direction) / STORAGE-SIDE / SYMMETRIC-INERT; L267's (c)); exp291 THE P1 SEPHIROTIC TEST (the record's own arithmetic reproduced locally — lambda_6 == 1.2 exact, the spectra within 1e-12, the indices exact, the stochastic null NOT re-run disclosed — and the 8-mode mapping reconciled against exp257's 8-channel schema with the stack's honest trichotomy 3 confirmed / 1 partial / 4 inert vs the record's own 7+1; the branch P1-ALIGNED iff the reproduction passes AND the mapping is total 8/8 / else P1-DRIFTED; L267's (d), the search wave's paper25 deposits). The queue: exp289 -> exp290 -> exp291, minimum-viable subagent prompts, the two-death rule, commit-before-dispatch.

L269 | exp289 — THE HISTORY-REGISTER PORT | 4/4 gates G1-G4 (4 PASS / 0 REFUTE) | BRANCH: HISTORY-CARRIED — THE FIRST NON-INERT ACTIVATION AMONG THE DORMANT CHANNELS: the commit-history register phi_history (the additive port on the collective: initialized to the spec install at write_spec_layer time — the never-written cells' history IS the spec layer — populated AT EACH commit write, NOTHING reads it at defaults) + the ctx coupling (exp258's channel, its registered next) re-run reading the SELF-HISTORY (the cell pulled toward its own last commit): the mean err IMPROVES on 12/12 hosts at EVERY grid point of exp258's verbatim grid {0, 0.25, 0.5, 1.0}, MONOTONE in g — total delta -0.1367 (g=0.25) / -0.2300 (g=0.5) / -0.3100 (g=1.0), the g=0.0 within-run control asserted bit-exact vs the anchor — the schema-only inertness (L234-L247) was a MISSING-VARIABLE artifact: the channels needed a state variable that SURVIVES THE WALK (Sediqi 2026's ionic-exposure history + Blattner-TAS 2026's hidden state, L267's (b) — the search wave's convergent prediction CONFIRMED) | G1 the port's zero-delta at defaults: the 72-row battery with the register live reproduces exp256's deposited substituted errs BIT-EXACT 72/72 (the verified flags 72/72) + exp282's walk_end_rms 72/72 (the trace shas 72/72) + exp287's commit layer 72/72 + the register presence/init 72/72 + the repo test suite green (5 PASS lines) + the provenance chains 31/31; G2 the register IS the commit sequence: phi_history[write_set] == the commit replay's values BIT-EXACT 72/72 (the same replay exp287/exp288 anchored, now read from the register) + the spec-install complement 72/72 + the bookkeeping (count == walk_steps == trace length, unique, coverage) 72/72; G3 the grid: 12/12 improved at all three g > 0 points (the HISTORY_MIN_HOSTS 10 bar cleared 3/3), the worst-err 3.67 < 6.0 at every point (the bar unchanged), the audit R_max face 0/12 concentrating — the exp288 SPEC-UNIFORM anchor face is UNCHANGED under the history activation: the improvement is NOT class-geometric; G4 deterministic one-pass per grid point, 7 deposits READ-ONLY byte-unchanged, exp142 NOT modified, the floor -60.0 asserted at exit | deposited results/exp289_history_register.json | the port: cultivation/bioelectric/collective.py +21 lines additive (the getattr guard keeps the pre-spec legacy paths untouched); the body written in-flight by a fleet agent, the run completed by the main agent under the two-death rule (one plumbing fix disclosed: pass1's payload carries the port/exp142 shas at the top level as _assemble reads them — gates untouched) | REGISTERED NEXT: (i) the HISTORY DOSE ladder (g in {1.0, 2.0, 4.0} — where does the monotone improvement saturate or break?); (ii) the HISTORY SOURCE decomposition (the SELF-history vs the NEIGHBOR-history form — whose commits protect the boundary?); (iii) the cross-channel sweep (the other four dormant channels' history-reading forms); (iv) the spec-layer premium under the history activation (the exp287/exp288 faces re-run on history-carrying walks — does rho(mean_cvt)~mia survive the improvement?).

L270 | exp290 — THE STRESS-TIMING SPLIT | 4/4 gates G1-G4 (4 PASS / 0 REFUTE) | BRANCH: STORAGE-SIDE — the write-time ionic stress degrades the decode MASSIVELY, the read-time stress has ZERO effect: mean paired delta(A1 WRITE-STRESS, the walk at the depolarized -35.0 pin) = -13.1292 mV (the errs explode on every host, within [−10.86, −14.72]); mean paired delta(A2 READ-STRESS, the settle at -35.0) = +0.0000 mV — the A2 errs and trace shas are BIT-IDENTICAL to the A0 anchor 72/72 (the settle+decode NEVER reads the floor — the consolidation is floor-blind): the storage face (the walk's commits) holds EVERYTHING, the retrieval face holds NOTHING on this machinery — Tazumi 2026's retrieval-side prediction (the planarian memory-retrieval sensitivity) REFUTED on the stack, an honest external disanalogy recorded (L267's (c)) | G1 the anchor: A0's errs == exp256's deposited substituted errs BIT-EXACT 72/72 (the verified flags 72/72) + exp282's walk_end_rms 72/72 (the trace shas 72/72) + the floor asserts (A0/A2 encode -60.0 144/144, A1 walk -35.0 72/72) + 7 deposits READ-ONLY; G2 the arms' integrity: finite/A3/trace-lengths/commit-counts 72/72 per arm, the S* lock reads 216/216, the settle-boundary floor asserts (A1 -60.0 72/72, A2 -35.0 72/72, the decode -60.0 144/144); G3 the branch by the pre-named 0.05 mV margin form; G4 deterministic (the canary True), no wall-clock, the docstring+header pinned to 982cb81 (the pin constant repaired to the true sha256(__doc__) — the agent's constant was miscomputed, the docstring bytes proven intact by the header sha; the exp231 plumbing precedent), floor -60.0 at exit | deposited results/exp290_stress_timing.json | REGISTERED NEXT: (i) the WRITE-STRESS dose ladder (-45/-35/-25 — the degradation curve); (ii) the HISTORY x STRESS interaction (does the exp289 history register PROTECT the decode under the write-time stress? — the memory-protection face); (iii) the stress-source decomposition (which commit faces carry the degradation — the census, the R_max face, the trace).

L271 | exp291 — THE P1 SEPHIROTIC TEST | 4/4 gates G1-G4 (4 PASS / 0 REFUTE) | BRANCH: P1-ALIGNED — the record's own arithmetic reproduced locally AS-IS: research/sephirotic/paper25_computation.py (Zenodo 19042388's own code, sha 40bfaf24, byte-unchanged, imported twice in-process, stdout sha-identical) reproduces the deposited paper25_results.json's deterministic face BIT-EXACT: lambda_6 == 1.2 EXACT, lambda_distance == 0.0, the spatial spectrum 3/3 and the internal spectrum 8/8 at max-abs-diff 0.0 (the bar 1e-12), the indices [3,6,10]/[0,1,2,4,5,7,8,9] exact, the graph identity exact, all 21 deposit fields agree (the record's own seed-42 null reproduced 3011/39/100000, audit-only); the 8-mode mapping RECONCILED total 8/8 both ways vs exp257's native schema, the stack's honest trichotomy 3 CONFIRMED / 1 PARTIAL / 4 INERT (the ledger's causal record) RECONCILED — not equated — against the record's own 7 confirmed + 1 partial (the record's knockout test is in-silico on its own model; the stack's is the ledger's causal record) | the core NOT imported (no stack state), deposits READ-ONLY byte-unchanged, deterministic, no wall-clock, ~38 s | deposited results/exp291_sephirotic_p1.json | the body written by the run agent under the body-only discipline (the record's terminal own-machine save pre-named and disclosed) | REGISTERED NEXT: (i) the record's PARTIAL channel localized against the stack's five inert channels (the exp289 HISTORY-CARRIED result re-reads the trichotomy: the ctx-form channel is now CONFIRMED-CARRIED — the trichotomy moves to 3/1/3+1); (ii) the record's knockout protocol ported to the stack's channel schema (the in-silico knockout form on the 8-channel state).

L272 | batch-48 pre-registrations (gates fixed before any body): exp292 THE HISTORY DOSE AND SOURCE (exp289's carrier pushed to its limits — the SELF form's dose ladder extended to {1.0, 2.0, 4.0} (the anchor: the g=1.0 errs reproduce exp289's deposited bit-exact 72/72) crossed with the NBOR form (the coupling source switched to the neighbor mean of phi_history — the social face: the boundary cells' neighbors are the unwound tissue whose history is the spec install); the dose face DOSE-SATURATING / DOSE-REVERSAL and the source face SELF-DOMINANT / NBOR-DOMINANT / SOURCE-SYMMETRIC at the 0.05 margin form, recorded independently; L269's (i)+(ii)); exp293 THE HISTORY x STRESS INTERACTION (the 2x2 factorial: register OFF/ON x stress OFF/ON, three of the four cells anchored bit-exact to exp256/exp289/exp290's deposits, the H1-S1 cell new; the protection delta P = the standard interaction; PROTECTED iff P >= 0.05 / AMPLIFIED iff P <= -0.05 / ADDITIVE otherwise — the memory-protection face, the Sediqi history form's causal test; L270's (ii)). The queue: exp292 -> exp293, minimum-viable subagent prompts, the two-death rule, commit-before-dispatch.

L273 | exp292 — THE HISTORY DOSE AND SOURCE | 3/4 gates G1-G4 (3 PASS / 1 REFUTE) | BRANCH: DOSE-REVERSAL x SELF-DOMINANT — the history carrier is SELF-SOURCED and DOSE-PEAKED | THE SOURCE FACE (decisive): the SELF form (the cell pulled toward its OWN last commit) improves 12/12 at g=1.0 (the mean paired delta -0.0258, == exp289's deposited per-host deltas reproduced bit-exact — the anchor), while the NBOR form (the neighbor mean of phi_history — the social face) DEGRADES 12/12 at every dose (mean +1.8385 err-delta at g=1.0, per-host within [+0.690, +2.858]): the neighbors' last commits POISON the decode — the boundary cells' neighbors are the unwound tissue whose register holds the spec install, so the NBOR coupling re-injects the spec's own values as a false history; SELF-DOMINANT by 1.86 mV at the best shared dose (the margin 0.05) | THE DOSE FACE (the SELF ladder {1.0, 2.0, 4.0}): the improvement REVERSES past the peak — monotone-through-g2 0/12, no-reversal 0/12, REVERSAL 12/12 (the errs grow from ~0.49-0.53 at g=1.0 to ~0.70-0.81 at g=4.0 on the cluster hosts): over-coupling to the self-history pulls the cells too hard toward stale commits — the carrier has a nontrivial OPTIMAL DOSE at g ~ 1.0 (exp289's landed point sits at the peak, its grid {0, 0.25, 0.5, 1.0} stopped just short of the reversal) | the audit R_max face at the best arm-cell 0/12 (the exp288 SPEC-UNIFORM anchor face unchanged — the carrier's action is not class-geometric) | G1 PASS: the SELF g=1.0 anchor bit-exact vs exp289's deposited g=1.0 errs 72/72 + the trace shas 72/72 + the arm-cell integrity 432 lock reads + 8 deposits READ-ONLY | G2 REFUTE — DIAGNOSED AS A TALLY-SCOPE ARTIFACT, the underlying face intact: the register replay equality held on EVERY row (the body's tallies read 216/216 per source over the 3-dose ladder) while the gate text's pre-registered numeric form demanded the PER-ARM 72/72 scope — the body tallied per-ladder, the comparison 216 vs 72 evaluated FALSE on the scope mismatch alone; recorded as the REFUTE it evaluated, the diagnosis disclosed (the exp290 disclosed-convention precedent), NO gate rewrite, NO re-run to flip | G4 PASS (deterministic, no wall-clock, the core + exp142 NOT modified, floor -60.0) | one plumbing fix disclosed (the exp289 precedent): the cells dict carries delta_rows as _assemble reads it | deposited results/exp292_history_dose_source.json | the body written in-flight by a fleet agent, the run completed by the main agent under the two-death rule | REGISTERED NEXT: (i) the dose curve refined around the peak (the pre-named {0.75, 1.0, 1.25, 1.5} — the reversal's sharpness); (ii) the NBOR form's failure decomposition (the spec-install leak face: the neighbor mean mixes the spec install with the true commits — the weighting by the neighbor's write-set membership is the repair candidate); (iii) the premium-under-history face (L269's (iv): the exp287/exp288 faces re-run on the SELF g=1.0 walks — does rho(mean_cvt)~mia survive the improvement, or does the carrier dissolve the premium?).

L274 | batch-48 pre-registration (gates fixed before any body): exp294 THE PREMIUM UNDER THE HISTORY CARRIER (the chain's standing finding vs the carrier's improvement — exp287's rho(mean_cvt)~mia +0.8616 / ~premium +0.7790 re-measured on the SELF g=1.0 carrier walks (the anchor: the errs + trace shas reproduce exp289's deposited g=1.0 records bit-exact 72/72 — the SAME walk, the commit layer IS the carrier's); the branch PREMIUM-DISSOLVED iff both fresh |rho| < 0.40 (the premium was the un-coupled noise) / PREMIUM-CARRIED iff both >= 0.60 (the premium is structural to the spec layer) / PREMIUM-MIXED otherwise; the bars fixed here, never fit; R2 audit-only: the improvement's address (the err deltas vs the mean_cvt deltas), the exp288 R_max face on the carrier's commits; L269's (iv) == L273's (iii)).

L275 | exp294 — THE PREMIUM UNDER THE HISTORY CARRIER | 4/4 gates G1-G4 (4 PASS / 0 REFUTE) | BRANCH: PREMIUM-MIXED — the honest middle, the faces SPLIT: on the SELF g=1.0 carrier's commits (the SAME walk exp289 deposited — the anchor bit-exact 72/72, the trace shas 72/72, the commit digests/cvt_rms/n_commits faces 72/72) the anchor regressions read rho(mean_cvt)~mia_prod_err +0.2679 (exp287's deposited +0.8616 — BELOW the pre-named 0.40 bar: the mia face reads DISSOLVED) and rho(mean_cvt)~one_zone_premium +0.4175 (exp287's deposited +0.7790 — BETWEEN the bars: the premium face reads MIXED) — neither pre-named branch met both-wise | THE CONCEPTUAL READ: the history carrier BOTH improves the decode (exp289: 12/12, -0.0258 mean paired at g=1.0) AND flattens the premium's main carrier (the mia rho +0.86 -> +0.27): a REAL FRACTION of the spec-layer premium WAS the un-coupled commit noise's host structure — re-coupling the commits to their own history dissolves that fraction; the residual premium face (+0.42) is the spec layer's structural host-dependence, persisting at reduced strength — the premium is not ONE thing: the noise-carried fraction (dissolved by the carrier) + the structure-carried fraction (persists) | the convention self-check bit-exact 2/2 (the machinery fed exp287's own carrier reproduces its deposited rhos — the regression instrument verified against its own anchor) | R2 audit-only: the delta correlation +0.4851 (the improvement moderately tracks the commit-layer change), the pooled-R_max face 0/12 (the exp288 SPEC-UNIFORM face unchanged under the carrier — the carrier's action is not class-geometric, consistent with exp289/exp292), the worst-err 3.67 < 6.0 | the provenance chains sha-verified 29/29 across 9 deposits (the pre-named split 4+3+4+5+4+5+1+2+1) | G2 the commit-layer definition 72/72 + the register's replay equality 72/72 (the PER-ARM scope — exp292's diagnosis honored); G4 deterministic, no wall-clock, the core + exp142 NOT modified, 9 deposits READ-ONLY byte-unchanged, floor -60.0 at exit | deposited results/exp294_premium_under_history.json | the body written by the run agent under the body-only discipline (exp289's landed source reused via programmatic byte-slices — no retyping) | REGISTERED NEXT: (i) the shelf faces on the carrier walks (the exp271-274 price/shelf battery re-run at SELF g=1.0 — does the shelf price move with the carrier? the boundary genealogy's next link); (ii) the NBOR failure decomposition (L273's (ii): the spec-install leak face — the neighbor mean mixes the spec install with the true commits; the write-set-weighted neighbor form is the repair candidate); (iii) the dose curve refined around the peak (L273's (i): {0.75, 1.0, 1.25, 1.5}).

L276 | batch-48 pre-registration (gates fixed before any body): exp295 THE DOSE CURVE REFINED AND THE NBOR LEAK REPAIR (two faces, one battery — the SELF-R refined ladder {0.75, 1.0, 1.25, 1.5}: PEAK-FLAT iff the |delta| differences among {0.75, 1.0, 1.25} all < 0.01 mV on >= 10/12 hosts / else PEAK-SHARP; the NBW write-set-weighted neighbor form (the leak repair: neighbors the program actually wrote contribute their true commit history, unwritten neighbors contribute ZERO weight, the no-written-neighbor fallback to self disclosed) at exp292's NBOR grid {0.25, 0.5, 1.0}: LEAK-CONFIRMED iff the NBW delta at g=1.0 improves vs exp292's deposited NBOR +1.8385 by > 0.05 mV on >= 10/12 hosts / else LEAK-NOT-SUFFICIENT; the g=1.0 SELF anchor bit-exact vs exp289's deposit 72/72; the per-arm register-replay scope per exp292's diagnosis; L273's (i)+(ii)).

L277 | exp295 — THE DOSE CURVE REFINED AND THE NBOR LEAK REPAIR | 4/4 gates G1-G4 (4 PASS / 0 REFUTE) | BRANCH: PEAK-FLAT x LEAK-NOT-SUFFICIENT | THE DOSE FACE: the SELF-R refined ladder {0.75, 1.0, 1.25, 1.5} reads a PLATEAU, not a sharp peak — the |delta| spread among {0.75, 1.0, 1.25} < 0.01 mV on 12/12 hosts (the mean paired improvements -0.0244 / -0.0258 / -0.0246, easing to -0.0193 at g=1.5): the carrier is ROBUST around its optimum — exp289's landed g=1.0 sits mid-plateau, the exp292 reversal begins past g=1.25 | THE LEAK FACE: the NBW write-set-weighted repair (unwritten neighbors weigh ZERO — the spec-install leak isolated) SOFTENS the social form's failure but does NOT SUFFICE: NBW g=1.0 mean delta +1.4172 vs exp292's deposited leaky NBOR +1.8385 (a -0.42 mV repair), the per-host >0.05 improvement clause met on only 9/12 (< the pre-named 10 bar) — the social form's failure is DEEPER than the leak: the neighbors' TRUE commit histories also poison the decode (the neighboring tissue's own commits are wrong FOR THIS CELL — the history is CELL-IDENTITY-SPECIFIC, the program's self-knowledge is per-cell, not per-neighborhood; the fallback-to-self count 297 across 7857 armed writes, disclosed) | G1 the anchor bit-exact 72/72 (the errs + trace shas vs exp289's g=1.0 deposit) + 7 arm-cells x 4 faces 72/72 + the S* lock reads 504 + 9 deposits READ-ONLY; G2 the register-replay tallies 72/72 per arm-cell x 7 (exp292's per-arm scope diagnosis honored) + the zero-knob weights from the commit-sequence support; G3 both faces recorded independently, honest counts; G4 deterministic, no wall-clock, the core + exp142 NOT modified, floor -60.0 | one plumbing fix disclosed (the armed-read counter scoped to the weighted-mean reads so the armed-write partition holds — the decode path untouched) | deposited results/exp295_dose_curve_leak_repair.json | the body written by the run agent (exp292's landed source verbatim + the marked exp295 deltas) | REGISTERED NEXT: (i) the cross-channel sweep (L269's (iii) — the other four dormant channels' history-reading forms: does the carrier generalize beyond ctx?); (ii) the shelf faces on the carrier walks (L275's (i) — the exp271-274 battery at SELF g=1.0: does the shelf price move?); (iii) the per-neighborhood commit identity face (the NBOR failure's next decomposition: the neighbors' commits vs the cell's own — the identity-specificity's dose-response).

L278 | batch-49 pre-registration (gates fixed before any body): exp296 THE CROSS-CHANNEL HISTORY SWEEP (the carrier's generality test — each of the four remaining dormant channels' landed activation forms (exp259 gj / exp260 structure / exp261 ca2 / exp263-264 apop) re-run with its coupling reading phi_history (the self form at the plateau dose g=1.0); each arm's control is its own deposited no-history errs bit-exact; the ctx-HIST positive control anchors to exp289's deposit; the branch CARRIER-GENERAL iff >= 3 of 4 carry (the house -0.05 mV margin + the 10/12 clause) / CARRIER-PARTIAL (1-2) / CARRIER-CTX-ONLY (0 — the honest null); 360 decodes, the checkpoint-split pass1|pass2|merge; L277's (i) == L269's (iii) — the dynamics batch's last architectural gate).

L279 | exp296 — THE CROSS-CHANNEL HISTORY SWEEP: THE BODY PENDING (the two-death rule fired: the fleet dispatch died twice pre-body (the context deadline), the main agent's window closed before the faithful four-arm body could be written — the four arms need each channel's landed coupling form (exp259/exp260/exp261/exp263-264's landed modules) re-plumbed to the phi_history source, and the faithful re-plumbing exceeds this session's remaining window; THE PRE-REGISTRATION STANDS (commit d6e81ea, gates fixed, the branch bars pre-named), the body is the next session's first dispatch — the exp288 precedent: this session's first dispatch landed exp288 4/4 under exactly this standing-state form) | THE SESSION RECORD (batches 46-48 closed, exp288-295 EIGHT experiments landed, ledger L267-L277, every one pushed): exp288 4/4 SPEC-UNIFORM (the spec layer's face is class-blind — the sixth class-blind level; the frontier is NOT geometric); exp289 4/4 HISTORY-CARRIED (THE BREAKTHROUGH: the commit-history register phi_history — the five dormant channels are no longer all-inert, the ctx self-history activation improves the decode 12/12, monotone to g=1.0); exp290 4/4 STORAGE-SIDE (the write-time stress degrades 13.13 mV, the read-time stress is bit-identical to the anchor — the commits hold everything); exp291 4/4 P1-ALIGNED (the record's own arithmetic reproduced bit-exact, the 8-mode mapping total 8/8); exp292 3/4 DOSE-REVERSAL x SELF-DOMINANT (the carrier is self-sourced and dose-peaked; the G2 REFUTE diagnosed as a tally-scope artifact, the face intact 216/216); exp293 4/4 PROTECTED (the register protects under write-time stress, super-additively, P +0.7285 — the history is worth ~29x more under stress than at rest); exp294 4/4 PREMIUM-MIXED (the carrier flattens the premium's mia face +0.86 -> +0.27 — a real fraction of the premium WAS the un-coupled commit noise; the structural residual +0.42 persists); exp295 4/4 PEAK-FLAT x LEAK-NOT-SUFFICIENT (the dose curve is a plateau — the carrier robust; the social form's failure is deeper than the spec-install leak — the history is CELL-IDENTITY-SPECIFIC) | THE SEARCH WAVE: 57 findings deposited in research/ (5 dated files), the convergent predictions (Sediqi's ionic history + Blattner-TAS's hidden state) CONFIRMED by exp289's landing | STANDING FRONTIERS: (a) exp296's body [THIS pre-registration, the immediate next action]; (b) the shelf faces on the carrier walks (L275's (i)); (c) the per-neighborhood commit identity face (L277's (iii)); (d) the write-set-weighted NBW form's deeper repair (the leak was not the whole failure). THE NEXT SESSION'S FIRST DISPATCH: exp296's body under d6e81ea, then derive — no plan, no check-in.
L280 | exp296 — THE CROSS-CHANNEL HISTORY SWEEP (C, 4/4, branch CARRIER-GENERAL — L278's pre-registration d6e81ea EXECUTED, L277's registered next (i) == L269's (iii), the dynamics batch's last architectural gate; the body written by the MAIN AGENT under the two-death rule [the fleet died twice pre-body last session; the exp288/exp296 precedent: the body-only discipline, the docstring/header sha-asserted at entry+exit, pinned to d6e81ea]; landed at 6471564): G1 PASS (the ctx positive control — exp289's landed g=1.0 form re-run — reproduces the deposit's errs + trace shas + arm-write counts BIT-EXACT 72/72, the instrument's fidelity proven; the S* lock reads 360/360; the rebuild shas 12/12; the exp288 chain 72/72; the four control extracts 72/72 per arm [gj <- exp259's compensated battery substituted arm; str <- exp260's battery rows; ca2/apop <- exp256's deposited substituted errs — the channels' landed no-history faces, their own armed grids never launched C3/A3 SKIPPED L239/L242, DISCLOSED: the HIST arms are the first armed ca2/apop decodes on this stack]; the test suite green; 15 deposits READ-ONLY sha before/after) | G2 PASS (the register faces 72/72 per arm — present + init + replay + complement + finite; the stream faces 72/72 per arm vs exp282's/exp287's deposited walk_steps/n_commits — the coupling is VALUE-LEVEL ONLY, one draw per commit for every arm, the RNG positions preserved; the across-seed site constancy; the gj arm's landed assert re-run per row: exp259's compensate VERBATIM + the conservation renorm) | G3 PASS THE BRANCH: **CARRIER-GENERAL** — 3 of the 4 dormant channels' history forms CARRY: GJ-HIST −0.2722 mV mean paired delta, 12/12 hosts improved (the blend at exp259's pair-junction site, ch2 carrying the register read); STR-HIST −5.0706 mV, 10/12 (the blend at exp260's de-pairing target cells, computed NOT applied — the outliers H3/H5 carry the mean at −3.84/−3.65: the non-canonical pair-junction cells are WHERE THE BOUNDARY STRUCTURE LIVES); AP-HIST −0.3550 mV, 12/12 (exp264's landed sigma form with the mark read from the register's init face — the extreme decile of the spec install + the band); CA2-HIST +0.0042 mV, 0/12 — DOES NOT CARRY, the honest inert (exp261's landed HH-gated gain reading the register is a deterministic per-cell rescale of the commit displacement — no noise to remove, no memory to re-assert: the gain form has no history-shaped hole) | G4 PASS (deterministic one pass per arm, no wall-clock fields, exp142 + the core NOT modified sha-asserted, floor −60.0 at exit) | THE FINDING: the commit-history register is NOT a ctx-specific hole — it is the stack's FIRST GENERAL COUPLING: three of the four dormant channels' sites carry the self-history source at the plateau dose, the carrier's mechanism (the spec install re-asserted through the register at the commit, the commit noise dropped) works wherever the site touches the boundary-carrying cells, and the two inert/harmful landed forms (the HH gain, the medium compensation) become CARRIERS when their scalar reads the register — the channel identity lives in the SITE, the dynamics live in the SOURCE. The paper's 8-channel correspondence now reads: 2 active channels + 1 general history carrier (4 sites carried: ctx/gj/str/apop) + 1 honest inert form (the ca2 gain) + the schema carrying all 8 natively. THE RE-PLUMB DISCLOSURE (fixed in the body before any armed decode): the four landed coupling forms are heterogeneous; the sweep re-plumbed each along the house's commit-coupling mold (the channel's SITE carries the coupling, the channel vector carries the scalar) — str's landed structural operation itself NOT applied (exp260's harm would confound the history question); the ca2 pbar over the register's init face (exp261's Pbar construction's analog, zero re-fit); the apop mark from the register's init face (exp264's zero-knob decile rule) | body fixes disclosed: 6 commits of plumbing (the docstring pin's AST form; exp259's compensate VERBATIM replacing my pairwise reconstruction [the identity 0.099 violation caught by the first probe]; the r289g key round-trip int coercion x2; the G2 gate's site-constancy scope restored to the pre-registration — the cross-host and within-host checks were over-implementations, the site size is a (host, instance) property, the across-seed constancy is the determinism face) — the gates' TEXT never changed, the branch bars never moved | deposited results/exp296_channel_sweep.json | REGISTERED NEXT (batch 51, derived): (a) exp297 THE CARRIER'S DOSE-RESPONSE ON THE NEW SITES — the gj/str/apop sites' g-ladders {0.25, 0.5, 1.0, 1.5} on the exp292 form: does each new site plateau like ctx, and does the STR site's huge outlier-carried improvement hold a monotone face?; (b) exp298 THE STR SITE'S ANATOMY — the de-pairing target cells' history coupling decomposed by class and instance on the outliers (the −5.07 mean is outlier-carried; is the site's improvement boundary-concentrated or interior-wide? the exp208 decomposition + the H3/H5 per-row deltas); (c) exp299 THE COMBINED-SITE CARRIER — the ctx+gj+apop sites' coupling TOGETHER at g=1.0 (the sites are disjoint by construction — the union's improvement vs the sum of the singles: super-additive, additive, or interfering?); (d) the ca2 form's post-mortem — the gain form's honest inert recorded as the 8th form-face; the remaining dynamics edge: the sigma/blend FAMILY vs the gain FAMILY (the carriers blend or remove noise; the inert form rescales).
L281 | exp297 — THE CARRIER'S DOSE-RESPONSE ON THE NEW SITES (C, 4/4, branches GJ-HIST PEAKED-AT-1.0 / AP-HIST CARRYING-MONOTONE / STR-HIST DOSE-INERT — L280's registered next (a) EXECUTED; the body written by the MAIN AGENT (exp296's landed instrument re-threaded with the dose dial; the body-only discipline, the pins sha-asserted vs the exp297 pre-registration ed00a44); landed at 0b5808b): G1 PASS (each site's g=1.0 rows reproduce exp296's deposited arm rows BIT-EXACT 72/72 — errs + trace shas, the instrument-reuse proof; the S* lock 792/792; the test suite green) | G2 PASS (the register + stream faces 72/72 per (site, dose); the site-write counts dose- and seed-invariant per (host, instance) — the dose does not move the site) | G3 THE BRANCHES: GJ-HIST PEAKED-AT-1.0 — the mean paired deltas vs exp256's dormant baseline −0.0901/−0.1735/−0.2707/−0.1740 at {0.25, 0.5, 1.0, 1.5}, 12/12 hosts at EVERY dose, the reversal past 1.0 — THE CTX SITE'S DOSE-REVERSAL GEOMETRY REPLICATES on the pair-junction site (exp292's self-sourced optimum at g≈1.0 is not ctx-specific; the blend's optimum is the CARRIER's property, not the site's); AP-HIST CARRYING-MONOTONE — −0.1042/−0.2069/−0.3550, 12/12 at every dose, saturating at the domain edge g=1.0 (sigma=0 by construction — the noise-removal face materializes fully); STR-HIST DOSE-INERT — −0.0017/−0.0039/−0.0050/−0.0039, below the 0.05 bar at every dose | **THE CONTROL-DEPENDENCE DECOMPOSITION (the batch's finding)**: exp296's str "carry" (−5.0706 mV) was measured against exp260's deposited errs — the DE-PAIRING-HARMED battery (the landed form's own ~6x damage); against the DORMANT baseline (exp256's errs) the str site's history blend is dose-inert: the "improvement" was NOT-APPLYING-THE-HARM, not the history. The carry verdicts are CONTROL-RELATIVE; the honest absolute face reads: gj CARRIES absolutely (−0.27 at the optimum), apop CARRIES absolutely (−0.36 at saturation), str is INERT vs the dormant face (the site is small — 0-15 cells — and interior-skewed; the chain hosts H0/H1 carry NO junction cells at all), ca2 INERT (exp296). The paper's channel record after batch 51: the history carrier works ABSOLUTELY on the ctx and gj sites (peaked at g≈1.0 — the blend's optimum is the carrier's property), absolutely on the apop site (monotone to saturation), and not at all on the str (vs baseline) and ca2 (gain form) sites | the domain disclosure: the pre-registration's ladder named g=1.5 for all three sites but exp264's landed sigma form has domain [0,1] by construction (sigma < 0 at 1.5 — the rng's scale<0 the run caught before any apop row ran); the apop ladder domain-restricted to {0.25, 0.5, 1.0}, the docstring pin standing, the deviation carried here | body fixes disclosed: 7 plumbing commits (the __main__ block the tail stitch dropped; the constants-block names G_PLATEAU/ARMS_ORDER inlined; the apop domain restriction; the ladder-length asserts per site) — the gates' TEXT never changed, the branch bars never moved | deposited results/exp297_site_dose_ladders.json | REGISTERED NEXT (batch 52, derived): (a) exp298 THE COMBINED-SITE CARRIER — the ctx+gj+apop sites' couplings TOGETHER at g=1.0 vs the singles (the sites are not disjoint — the apop mark's band clause covers the walked region including the boundary and junction cells; the union's improvement vs the sum of the singles: super-additive, additive, or interfering? the honest absolute control = exp256's baseline per row, the pre-named bars: ADDITIVE iff |union − best-single| < 0.05 / SUPER-ADDITIVE iff the union beats the best single by >= 0.05 / INTERFERING iff the union is worse than the best single); (b) the str site's post-mortem is CLOSED by exp297's absolute face (no new experiment needed — the ledger records it); (c) the ca2 form's post-mortem (the gain family vs the blend/sigma family: the carriers remove or re-assert noise; the gain rescales — the 8th form-face recorded in the ledger, no new experiment); (d) the history register's remaining architectural edge: the register's WRITE-side face under the combined coupling (does the union's walk leave a different commit sequence? the exp287 commit-layer face on the union walks).
L282 | exp298 — THE COMBINED-SITE CARRIER (C, 4/4, branch ADDITIVE — L281's registered next (a) EXECUTED; the body written by the MAIN AGENT [exp297's instrument composed via the faces parameter; the body-only discipline, the pins sha-asserted vs the exp298 pre-registration b5102c4]; landed at 17cbd78): G1 PASS (the anchor ladder: the ctx/gj/apop single-face arms reproduce exp296's deposited rows BIT-EXACT 72/72 each — the composition's fidelity proven: the faces parameter changes nothing when a face runs alone; the S* lock 288/288; the test suite green) | G2 PASS (the register + stream faces 72/72 per arm; the site writes seed-invariant per (host, instance); the gj landed assert) | G3 THE BRANCH: **ADDITIVE** — the union −0.3550 mV == the best single (apop) −0.3550 mV EXACTLY (bit-exact per row, the band 0.05); **THE MECHANISM FINDING: the three carrying faces are ONE mechanism at different site granularities** — at g=1.0 the sigma face (sigma = COMMIT_NOISE*(1−g) = 0) and the blend form both land the commit on the SPEC INSTALL (the register's init face) for spec-sourced commits; the mark's band clause covers the ENTIRE walked region (every region cell is marked), so the apop face IS the maximal site and SUBSUMES the ctx/gj blends — the union's errs == the apop single's errs bit-for-bit; no interference, no compounding: the faces are not independent mechanisms but one carrier (the spec-install re-assertion = the commit-noise removal) at nested site granularities; the sites' differential value scales with the SITE SIZE: apop −0.3550 (the whole region, 292 cells) > gj −0.2707 (the junction cells) > ctx −0.0258 (the boundary cells), 12/12 hosts each — the improvement is MONOTONE in the site coverage | G4 PASS (deterministic, no wall-clock, 16 deposits READ-ONLY sha before/after, exp142 + the core NOT modified, floor −60.0) | THE CARRIER'S COMPLETE CHARACTERIZATION AFTER BATCH 52: the commit-history register's carrier is the spec-install re-assertion at the commit; its forms (the blend, the sigma relaxation, the register-face mark) are one mechanism; its optimum dose is g≈1.0 (the plateau on the ctx site, the peak on the gj site, the saturation on the apop site — the domain edge); its improvement scales with the site coverage (the region > the junction > the boundary); the honest inerts: the str site (vs the absolute baseline — the control-dependence lesson) and the ca2 gain form (a rescale, not a re-assertion) | body fixes disclosed: 2 plumbing commits (the zero-reader scan's allowlist; the union arm's delta key) — the gates' TEXT never changed | deposited results/exp298_combined_site_carrier.json | REGISTERED NEXT (batch 53, derived): (a) exp299 THE CARRIER AT THE SUB-SATURATION FACES — the union's faces at g=0.5 (the sigma NOT saturated: sigma = 0.5*COMMIT_NOISE at the marked cells): does the blend face add value where the sigma face leaves noise? THE test of the mechanism's decomposition — at g<1 the two forms DIFFER (the blend re-asserts, the sigma half-removes): the union at 0.5 vs the singles at 0.5 vs the baseline; (b) the write-side face on the carrier walks (L280's (d) — the exp287 commit-layer face on the union walks: does the carrier change WHAT the program commits? the register's replay face says the commits ARE the write values — the census face); (c) the zero-substrate path's 8th formalization (the standing frontier, unstarted — the carrier's mechanism (the spec-install re-assertion) is now the strongest architectural hint: the reader's excess IS the program's un-asserted spec).
L283 | exp299 — THE CARRIER AT THE SUB-SATURATION FACES (C, 4/4, branch SUPER-ADDITIVE — L282's registered next (a) EXECUTED; the body written by the MAIN AGENT [exp298's composition re-threaded to g=0.5; the body-only discipline, the pins sha-asserted vs the exp299 pre-registration c32c931]; landed at bb460ac): G1 PASS (the deposited g=0.5 single-face rows reproduced BIT-EXACT 72/72 per face — ctx from exp289's own grid rows, gj/apop from exp297's ladder rows: the dose-ladder chain face intact across three batches' deposits; the S* lock 288/288; the test suite green) | G2 PASS (the register + stream faces 72/72 per arm; the site writes seed-invariant; the gj landed assert) | G3 THE BRANCH: **SUPER-ADDITIVE** — the union −0.3000 mV beats the best single (apop −0.2069) by 0.093 mV at the pre-named 0.05 band, 12/12 hosts: at g=0.5 the two forms GENUINELY DIFFER and COMPOSE — the sigma face shrinks the noise (sigma = 0.5*COMMIT_NOISE at the marked cells, the draw still scattered), the blend face re-asserts the register value on top of the shrunk-noise draw; the compounding is real (the union's errs strictly below every single's on the clean hosts); the singles at 0.5: ctx −0.0192, gj −0.1735, apop −0.2069 | **THE COMPLETE DOSE-MECHANISM PICTURE (the carrier's final form after batches 50-53)**: at saturation (g=1.0) the re-assertion subsumes (exp298: ADDITIVE, the union == the apop single bit-exact — the sigma=0 draw already lands on the spec install, the blend adds nothing); below saturation the two mechanisms COMPOSE SUPER-ADDITIVELY (exp299): the carrier is TWO complementary mechanisms — the noise shrink (the sigma face, the exp264 landed form reading the register's mark face) and the value re-assertion (the blend face, the exp289 landed form) — that converge at the domain edge; the improvement scales with the site coverage at every dose (the region > the junction > the boundary, 12/12 hosts everywhere measured) | G4 PASS (deterministic, no wall-clock, 16 deposits READ-ONLY sha before/after, exp142 + the core NOT modified, floor −60.0) | body fixes disclosed: 1 plumbing commit (the zero-reader scan's allowlist adds the module) | deposited results/exp299_subsaturation_faces.json | REGISTERED NEXT (batch 54, derived): (a) exp300 THE COMPOSED OPTIMUM — the union's dose ladder {0.25, 0.5, 0.75, 1.0} at the composed faces (exp297's ladder logic on the union arm: where is the composition's optimum? the pre-named branches: PEAKED / PLATEAU / MONOTONE-RISING on the union's deltas, the sub-saturation compounding predicts the optimum PAST the singles' peaks if the composition's gain grows as the sigma face's noise-shrink weakens); (b) the write-side face on the carrier walks (L280's (d), carried): the exp287 commit-layer face on the union walks — does the composed carrier change WHAT the program commits (the register's replay face says the commits ARE the write values; the census face the pre-named read); (c) the zero-substrate path's 8th formalization (the standing frontier, the carrier's mechanism now the strongest architectural hint: the reader's excess IS the program's un-asserted spec — the 8th attempt pre-registered when the window allows a full formalization cycle).
L284 | exp300 — THE COMPOSED OPTIMUM (C, 4/4, branch MONOTONE-TO-1.0 — L283's registered next (a) EXECUTED; the body written by the MAIN AGENT [the exp299 composition re-threaded to the union's own ladder; the body-only discipline, the pins sha-asserted vs the exp300 pre-registration 8f8b732]; landed at b438908): G1 PASS (the deposited single-face rows reproduced BIT-EXACT per dose — ctx 216/216 [exp289's grid {0.25, 0.5} + exp296's g=1.0], gj/apop 216/216 [exp297's ladders + exp296's] — the dose-ladder chain face intact across FOUR batches' deposits; the S* lock 936/936; the test suite green) | G2 PASS (the register + stream faces per arm per dose; the site writes dose- and seed-invariant) | G3 THE BRANCH: **MONOTONE-TO-1.0** — the union's mean paired deltas −0.1814 / −0.3000 / −0.3499 / −0.3550 at {0.25, 0.5, 0.75, 1.0}, 12/12 hosts at EVERY dose: the composed carrier's optimum IS the saturated face — no trade-off peak below 1.0 | THE COMPOSITION'S GAIN FACE (the audit): the union minus the best single shrinks as the dose rises — −0.0772 at 0.25, **−0.0931 at 0.5 (the compounding's own peak)**, n/a at 0.75 (the singles' deposited doses exclude it, disclosed), +0.0000 at 1.0 (the re-assertion subsumes, exp298's bit-exact face) — the two mechanisms converge at the domain edge exactly as the mechanism picture predicted; the sub-saturation compounding is real but its maximum lives at the middle of the ladder, while the ABSOLUTE improvement is monotone to saturation | G4 PASS (deterministic, no wall-clock, 16 deposits READ-ONLY sha before/after, exp142 + the core NOT modified, floor −60.0) | the granularity disclosure: the pre-registered pass1 (648 decodes + the suite) exceeded the foreground cap — split to four per-cell sub-passes (ctx/gj/apop anchors + the union ladder), the gates/arithmetic/bars unchanged, the body carries the disclosure | body fixes disclosed: 8 plumbing commits (the scan allowlist; the stale G_SUB field; the four-pass payloads join; the G2 tallies scaled to the sub-pass counts; the per-face row count; the 0.75 gain guard; the G1 tallies' dose scaling; the G1 print's lock sum) — the gates' TEXT never changed, the branch bars never moved | deposited results/exp300_composed_optimum.json | REGISTERED NEXT (batch 55, derived): (a) exp301 THE CARRIER'S WRITE-SIDE FACE — the exp287 commit-layer face on the union walks at the composed optimum (does the composed carrier change WHAT the program commits? the register's replay face says the commits ARE the write values; the pre-named read: the commit-sequence digests vs the singles' + the census face — the carrier's effect on the PROGRAM's own output, the spec layer's face); (b) the carrier's stress face at the composed optimum (exp293's PROTECTED form re-run on the union: is the ~29x protection preserved under composition?); (c) the zero-substrate path's 8th formalization (the standing frontier — the carrier's mechanism, the spec-install re-assertion, is the strongest hint: the reader's excess IS the program's un-asserted spec; the 8th attempt when the window allows a full cycle).
L285 | batch-55 standing state (the window brink — the exp288/exp296 discipline held: the next body stubbed with the full implementation plan inline, the pre-registration 046aa06 stands, the body is the next session's first dispatch): exp301 THE CARRIER'S WRITE-SIDE FACE (3 arms x 72 = 216 decodes: the dormant anchor g=0.0 MUST reproduce exp287's deposited commit layer bit-exact 72/72 — the commit_seq_sha256 + the cvt_rms + the n_commits + the sc_rms + exp256's errs; the union at the composed optimum g=1.0 + at the sub-saturation g=0.5; the digest face — the carrier's commit digests differ from the dormant's; the cvt face — WRITE-SIDE-CARRIED iff the union-1.0 mean cvt drop > 0.05 mV AND >= 10/12 hosts; the census face audit — the branch chain's structure carrier-invariant; the full implementation plan inlined in the stub, zero new machinery — exp300's tail re-threaded to the write-side battery) | THE SESSION RECORD (batches 50-54 closed, exp296-300 FIVE experiments landed, ledger L280-L284, every one pushed): exp296 4/4 CARRIER-GENERAL (the cross-channel sweep: gj −0.2722 12/12, str −5.0706 10/12 [control-relative], apop −0.3550 12/12, ca2 +0.0042 inert; the ctx positive control bit-exact 72/72); exp297 4/4 (the dose faces: gj PEAKED-AT-1.0, apop CARRYING-MONOTONE, str DOSE-INERT vs the absolute baseline — the control-dependence decomposition); exp298 4/4 ADDITIVE (at saturation the re-assertion subsumes — the union == the apop single bit-exact); exp299 4/4 SUPER-ADDITIVE (at g=0.5 the two mechanisms compose: the noise shrink + the value re-assertion); exp300 4/4 MONOTONE-TO-1.0 (the composed optimum IS the saturated face; the compounding's own peak at g=0.5, −0.0931) | THE CARRIER'S FINAL CHARACTERIZATION: the commit-history register's carrier = the spec-install re-assertion at the commit; two complementary mechanisms (the noise shrink + the value re-assertion) converging at the domain edge; the improvement monotone in the site coverage; the honest inerts named (the str site vs the absolute baseline, the ca2 gain form) | THE SEARCH WAVE's convergent predictions (Sediqi's ionic history, Blattner-TAS's hidden state) now confirmed AND characterized | STANDING FRONTIERS: (a) exp301's body [THIS pre-registration, the immediate next action — the plan is in the stub]; (b) the composed stress face (exp293's PROTECTED form on the union: is the ~29x protection preserved under composition?); (c) the zero-substrate path's 8th formalization (the carrier's mechanism the strongest hint: the reader's excess IS the program's un-asserted spec) | THE NEXT SESSION'S FIRST DISPATCH: exp301's body under 046aa06, then derive — no plan, no check-in.
L286 | exp301 — THE CARRIER'S WRITE-SIDE FACE (C, 4/4, branch WRITE-SIDE-CARRIED — L285's standing pre-registration 046aa06 EXECUTED, the stub's inlined plan landed verbatim; the body written by the MAIN AGENT [exp300's tail re-threaded to the write-side battery; the body-only discipline, the pins sha-asserted vs 046aa06]; landed at a15c485): G1 PASS (the dormant anchor: exp287's deposited commit layer reproduced BIT-EXACT 72/72 — the commit_seq_sha256 + the cvt_rms + the n_commits + exp256's errs — the machinery's fidelity proven on the write side; the S* lock 216/216; the test suite green) | G2 PASS (the register faces 72/72 per arm — the replay equality IS the write-side core: the register IS the commit sequence; the stream faces 72/72 per arm; the site writes seed-invariant) | G3 THE BRANCH: **WRITE-SIDE-CARRIED** — the digest face: the union's commit sequences differ from the dormant's on 72/72 rows at BOTH doses (g=1.0 AND g=0.5 — the carrier writes DIFFERENT values, the write-side face is REAL); the cvt face: the commit-vs-target RMS drops +0.5954 mV at g=1.0 (12/12 hosts) and +0.4465 mV at g=0.5 (12/12) — the carrier's commits land closer to the target, the write-side counterpart of the read-side improvement; the census face (audit): the source tags IDENTICAL across all arms (spec 20802 / canon 0 / parent 0) — **the branch chain's structure is carrier-INVARIANT: the carrier changes the VALUES the program commits, not the structure of how it commits them** — the program's output improves at its own layer while its control flow is untouched | G4 PASS (deterministic, no wall-clock, 16 deposits READ-ONLY sha before/after, exp142 + the core NOT modified, floor −60.0) | body fixes disclosed: 3 plumbing commits (the scan allowlist; the G2 (arm, dose) grouping; the _exit_checks def the stage stitch cut — the first run's deposit was already written, the deterministic re-run completed the exit discipline) — the gates' TEXT never changed | deposited results/exp301_write_side_face.json | THE CARRIER'S COMPLETE LEDGER PICTURE AFTER BATCH 55: read-side carried (exp296), the dose geometry mapped (exp297), the mechanisms decomposed and composed (exp298/299), the composed optimum at saturation (exp300), the write-side face real and structure-preserving (exp301) | REGISTERED NEXT (batch 56, derived): (a) exp302 THE COMPOSED STRESS FACE — exp293's PROTECTED form re-run on the union at the composed optimum: is the ~29x protection preserved under composition (the write-time stress × the composed faces)?; (b) the carrier's shelf faces (L275's (i), carried: the exp271-274 battery on the carrier walks — does the shelf price move?); (c) the zero-substrate path's 8th formalization (the standing frontier — the write-side face's finding sharpens the hint: the carrier's value changes are the program's own spec re-asserted; the reader's excess IS the un-asserted spec).
L287 | exp302 — THE COMPOSED STRESS FACE (C, 4/4, branch PROTECTED-PRESERVED — L286's registered next (a) EXECUTED, the body written by the MAIN AGENT [pre-registration 26e15a1, the body-only discipline, the pins sha-asserted vs 26e15a1]): G1 PASS (the anchors: U0-S0 == exp256's errs BIT-EXACT 72/72 (the verified flags 72/72, exp282's walk anchors 72/72 + trace shas 72/72 + err_exact 72/72; the commit-layer digests vs exp287/288 audit-only); U1-S0 == exp300's deposited union g=1.0 rows BIT-EXACT 72/72 errs + trace shas (the walk-end/register-digest/write-count/cvt faces audit-only 72/72 each); U0-S1 == exp290's A1 errs BIT-EXACT 72/72 (the fresh trace shas + floor schedules audit-only); THE MARKS' VALIDITY: the rebuilt q10/q90 (-60.0/-20.0) + target_part + bands reproduce exp300's deposited arm_inputs 24/24 + 12/12 (fail=STOP at the rebuild — the union's armed-site plan pinned to the deposited one); the floor asserts: the S1 walk pin 144/144, the S0 encode -60.0 144/144, the settle/decode -60.0 288/288; the test suite green) | G2 PASS (the new cell U1-S1: finite errs 72/72, the A3 convention 72/72, the trace lengths 72/72, the commit counts 72/72, the register's replay equality 72/72, the stream face 72/72 (the commit-index digests + walk_steps + n_commits identical across ALL FOUR cells), the plan face 72/72 (the union's armed-site counts identical across U1-S0/U1-S1 — the plan is (target, A)-determined, stress-independent), the gj landed compensation asserts 144/144, the S* lock 288/288) | G3 THE BRANCH: **PROTECTED-PRESERVED** — P_union = +13.1292 mV vs the pre-named PROTECT_BAR 0.05 mV (the stress degradation WITHOUT the union +13.1292 mV — reproducing exp290's landed 13.13 mV form; WITH the union +0.0000 mV — the composed carrier makes the write-time stress INVISIBLE at the decode: the U1-S1 cell mean equals the U1-S0 cell mean to 4 decimals, 0.6189 mV both); the composition's protection comparison (AUDIT-ONLY): P_union +13.1292 vs exp293's deposited P_ctx +0.7285 — **the composed protection is ~18x the single register's** (the delta +12.4007 mV); the ratio face: the union 36.98x vs the ctx register's 28.20x (protection / rest-improvement); 12/12 hosts protected (the per-host P +10.86..+14.72, the outliers H3 +13.27 / H5 +11.98 in-band); the worst-err per cell vs the 6.0 bar unchanged (audit) | G4 PASS (deterministic, the canary bit-identical 4/4, no wall-clock fields, 11 deposits READ-ONLY sha before/after, exp142 + the core NOT modified, floor -60.0 at exit, the test suite green) | run form: the checkpoint-split pass1|pass2 + merge (the in-process default pre-named for the runners) | deposited results/exp302_composed_stress_face.json | THE MECHANISM FACE: the union at the composed optimum g=1.0 overwrites every armed cell's write with the register's own value (the blend weight 1.0 discards theta_new entirely at the boundary + junction cells) and kills the noise at the marked cells (sigma=0 at g=1.0) — the stress's only remaining channel is the unarmed interior cells' dynamics, and the decode cannot see it | REGISTERED NEXT (batch 57, derived): (a) the carrier's shelf faces (L275's (i), carried: the exp271-274 battery on the carrier walks — does the shelf price move under the composed carrier?); (b) the write-side stress face (exp301's digest/cvt form re-run under the A1 pin — does the carrier's commit sequence remain closer to the target under write-time stress? the write-side counterpart of P_union); (c) the zero-substrate path's 8th formalization (the standing frontier — sharpened by exp302: the carrier's protection IS the spec re-asserted at the armed sites; the reader's excess IS the un-asserted spec).
L288 | exp303 — THE ZERO-SUBSTRATE 8TH FORMALIZATION: THE TRANSPORT FORM (C, 4/4, branch TRANSPORT-BREAKS on the pre-named clause WITH THE DEGENERACY DISCLOSED — the honest scientific reading is TRANSPORT-REFINES-DEEPENED: the zero-substrate path stays BLOCKED at 8 formalizations, and the block now covers the program's own output; ledger L287's registered next (c) EXECUTED, the body written by the MAIN AGENT [pre-registration 7a968de, the body-only discipline, the pins sha-asserted vs 7a968de]): R1 PASS (the anchors: the 72 dormant walks reproduce exp256's deposited errs BIT-EXACT 72/72 + exp282's walk anchors 72/72 + **exp287's deposited commit_seq_sha256 BIT-EXACT 72/72 — the streams ARE the deposited commit sequences**; the rebuild sha-asserted 12/12; the floor -60.0 at every replay's settle and at exit; 6 deposits READ-ONLY; the test suite green) | R2 PASS (the content face: **72/72 within the 6.0 bar, the mean region rms 0.5921 mV** — THE STREAM CARRIES THE PATTERN'S CONTENT COMPLETELY ON ITS OWN SUBSTRATE: replaying the bare commit stream into a fresh wiring-only substrate (NO spec install, NO clamps, NO encode window, NO carried state — the register port never touched, the zero-substrate discipline protocol-level) reconstructs the walked region to ~0.59 mV, the walked decode's own quality; the full-target decode within the bar 0/72 audit-only — the encode's zones are NOT the stream's to claim, as pre-named; the canary bit-exact) | R3 PASS (the transport face: 2/132 within the bar on the pre-named clause — **THE DEGENERACY DISCLOSED: the 2 in-bar transports are exactly the H0↔H1 pair, whose substrates are BIT-IDENTICAL (exp243's chain constructor echoes H0 == H1, asserted in the rebuild)** — the H0→H1 'transport' is the same-substrate replay in disguise; EXCLUDING the degenerate pair: **0/130 GENUINE cross-substrate transports within the bar, the mean transport price +15.7576 mV (the best genuine 10.81 mV)** — the same scale as the write-time stress degradation (exp290's 13.13 mV): the substrate-binding of the stream is a REAL dynamical quantity; the m/m' prefix mismatch is not the driver (n_written 272..292, 90/132 pairs length-matched); the failure mode is the INDEXATION: the stream's values are zone-meaningful only along the SOURCE's own BFS order — the j-th destination cell sits in a different zone than the j-th source cell, the values land zone-inconsistent, the settle cannot repair a zone-misassigned write; the canary bit-exact) | R4 PASS (deterministic, no wall-clock fields, 6 deposits READ-ONLY sha before/after, exp142 + the core NOT modified, floor -60.0, the test suite green) | run form: in-process one invocation (~6 min) | deposited results/exp303_zero_substrate_8th.json | **THE HONEST VERDICT**: the 8th formalization's pre-named branch clause resolves TRANSPORT-BREAKS as written (it counts the degenerate pair — a pre-registration hole, disclosed, never patched in-gate), but the scientific reading is **TRANSPORT-REFINES-DEEPENED**: (i) the commit stream is a COMPLETE same-substrate representation (a NEW positive finding — the write product IS the pattern on its own wiring, 72/72 at 0.59 mV with no spec install and no carried state); (ii) it is a FAILED transport object (0/130 genuine pairs, the price +15.8 mV) — the pattern lives in the WIRING-KEYED indexation as much as in the values; the coherence constraint survives its 8th formalization and the 8th is the strongest form yet: not even the program's own output transports | REGISTERED NEXT (batch 58, derived): (a) exp304 the degeneracy repair + the carrier-stream transport — the transport face re-scoped to the 10 genuinely distinct substrates (the H0↔H1 exclusion pre-named THIS time) x {the dormant stream, the composed carrier's stream (exp301's union form)}: does the carrier's re-assertion stream transport where the dormant's fails (the armed sites' values ARE the spec install — the zone-consistency question)?; (b) the carrier's shelf faces (L275's (i), carried); (c) the write-side stress face (exp301's form under the A1 pin).
L289 | exp304 — THE TRANSPORT FACE RE-SCOPED: THE DEGENERACY REPAIR + THE CARRIER'S STREAM (C, 4/4, branch **BOTH-BOUND** — the indexation binds both forms; ledger L288's registered next (a) EXECUTED, the body written by the MAIN AGENT [pre-registration c4c563b, the body-only discipline, the pins sha-asserted vs c4c563b]): G1 PASS (the anchors: the 12 dormant slice walks reproduce exp256's errs + exp282's walk anchors + exp287's commit digests BIT-EXACT 12/12; the 12 carrier slice walks reproduce exp300's deposited union g=1.0 rows (the errs + the trace shas) BIT-EXACT 12/12; the walk orders ARM-INDEPENDENT 12/12 (the commit-index digests equal across the forms — exp300's G2 stream face re-confirmed); the MARKS' VALIDITY vs exp300's arm_inputs 24/24 + 12/12; the rebuild sha-asserted 12/12 + H0 == H1; 9 deposits READ-ONLY; the test suite green) | G2 PASS (**F1 THE REPAIR: the 130 genuine dormant transports reproduce exp303's deposited per-pair region rms BIT-EXACT 130/130** — the cross-deposit anchor lands, the re-scoping is a re-scoping and not a re-run with new knobs; the exclusion's honesty pinned: exp303's in-bar pairs == exactly the pre-named degenerate set {(H0,H1),(H1,H0)}; the canaries bit-exact 2/2) | G3 THE BRANCH: **BOTH-BOUND** — F2 the carrier content face: **12/12 within the 6.0 bar, the mean region rms 0.0548 mV — the carrier's stream reconstructs its own substrate ~11x BETTER than the dormant's (0.0548 vs 0.5921: the re-asserted values ARE the spec install, the content face near-exact)**; F3 the carrier transport face: **0/130 genuine transports within the bar** (the mean region rms 16.3305, the best 10.8127, the mean transport price +16.2756 mV vs the destination's own replay) — the carrier's stream is wiring-bound EXACTLY as the dormant's; the zone-assignment of the j-th walked cell is substrate-idiosyncratic and the values alone do not carry it — not even the re-asserted spec's own stream transports | G4 PASS (deterministic, no wall-clock fields, 9 deposits READ-ONLY sha before/after, exp142 + the core NOT modified, floor -60.0, the test suite green) | run form: in-process one invocation (~4 min) | deposited results/exp304_transport_rescoped.json | **THE ZERO-SUBSTRATE BLOCK'S FINAL FORM (the 8th formalization arc closed by exp303+exp304)**: (i) the commit stream is a COMPLETE same-substrate representation — near-exact under the carrier (0.05 mV, 12/12) and exact-scale under the dormant (0.59 mV, 72/72); (ii) it TRANSPORTS NOWHERE — 0/130 genuine pairs in BOTH forms (the price ~16 mV, the stress-degradation scale); the coherence constraint survives its 8th formalization and the block is now maximally sharp: **the pattern lives in the wiring-keyed indexation as much as in the values — a representation exists only RELATIVE TO its own wiring, and no representation transports across wirings** (the honest negative, reported as a result) | REGISTERED NEXT (batch 59): none — the transport arc is closed on both sides (the content face positive, the transport face negative, the degeneracy repaired, the anchor bit-exact); the remaining standing frontiers (the carrier's shelf faces (b), the write-side stress face (c)) stand as the honest open list for the close-out.
L290 | THE FINAL SESSION'S CODE REVIEW + PERFORMANCE PASS (Phase 3; the full record deposited at docs/CODE_REVIEW_FINAL.md; every applied fix verified bit-exact — the full suite green + the exp304 deposit re-run BYTE-IDENTICAL sha 36fce7c8 before/after): 4 fixes landed — (1) PERF the step() hot loop's per-step O(n^2) A.sum(axis=1) recomputation cached at init as _A_rowsum (A is fixed after construction: amputate touches V/theta only, no method and no landed experiment writes A); (2) the combined deposit+safety sweep test (tests/test_deposits_and_safety.py, 5 tests: D1 the fingerprint integrity across 34 deposits, D2 the frozen-era wall-clock key scan, D3 the repo-wide token-literal scan, D4 the tracked-deposit guarantee, D5 the classify bit-equality); (3) 58 UNTRACKED DEPOSITS RECOVERED (the exp1-133 era predated the results/ gitignore's add -f discipline — a sandbox revert would have destroyed them; all added); (4) classify_vectorized landed in graph.py (the O(n) roll form, bit-equal to exp208's reference loop, asserted over a fixed battery) | 6 found-and-disclosed, deliberately not patched: exp288's fingerprint (the regeneration-era round-trip coercion — the pre-named D1 exception, historical not live); the ~700-line machinery duplication across exp302/303/304 (frozen bodies take precedence); the _target_of BFS recomputation per transport; the _replay star_dt recomputation; the set_floor_seen dead recording; the deliberately-serial suite (the floor pins make xdist unsafe) | REGISTERED NEXT: the completion entry (Phase 4).
L290b | ==================== THE COMPLETION ENTRY (the terminal condition; the Phase 4 trigger fired — the project is CLOSED, not abandoned) ==================== | THE COMPLETION DATE: 2026-09-21. THE FINAL HEAD: 0938512 (main == origin/main). | **ALL 5 STAGES AT THEIR ACHIEVED MAXIMUM**: Stage 1 Map ~95% (complete); Stage 2 Validate ~90% (complete); Stage 3 Engineer ~95% (101% PASSED — 10/10 novel anatomies, the spec face class-blind); Stage 4 Expand ~90% (cross-organism CLOSED, autocatalytic CLOSED 100/100); Stage 5 Transfer ~90% (the reader CLOSED across media x sizes to n=5000; the substrate CLOSED at 100 hosts; the zero-substrate path BLOCKED — the honest negative, reported as a result). | **THE REFRAMED STAR CROSSED**: the universal reader (media x size x n=5000, sub-linear n-invariant cost) + the universal substrate (100 hosts) — crossed with bit-exact evidence, consumed as anchored machinery by every final-session experiment and refuted by none. | **THE ZERO-SUBSTRATE STAR CONFIRMED BLOCKED AT 8 FORMALIZATIONS**: the five static metrics (exp68) + the temporal schedule (exp162) + the gauge quotient (exp244) + THE TRANSPORT FORM (exp303/304) — the final form the sharpest: the commit stream is a COMPLETE same-substrate representation (0.59 mV dormant / 0.05 mV carrier, the content face near-exact with no spec install, no clamps, no encode, no carried state) and TRANSPORTS NOWHERE (0/130 genuine pairs in both forms, the price ~16 mV) — **the pattern lives in the wiring-keyed indexation as much as in the values; a representation exists only relative to its own wiring**. | **THE HISTORY REGISTER CHARACTERIZED** (the first non-inert channel, exp289-304): carried, storage-side, P1-aligned, self-dominant, protected (29x), premium-mixed, peak-flat, carrier-general, dose-mapped, additive-at-saturation, super-additive-below, monotone-to-1.0, write-side-carried, and — the final headline — **stress-protective under composition at +13.13 mV (18x the single register's), the write-time stress decode-invisible (+0.0000 mV, 12/12 hosts, exp302)**. | **ALL DEPOSITS CLOSED**: the Levin series, the Chinese targets, the NOT-IN-LITERATURE spec, the wetlab format — closed; 342+ deposits git-tracked (58 recovered from the untracked state by the final review); the anchors re-verified across the entire session without a single drift. | **THE PERFORMANCE IMPROVEMENTS LANDED**: the step() hot-loop O(n^2) cache (verified by the exp304 byte-identical re-run), the combined deposit/safety sweep (5 tests), 58 deposits recovered, the shared vectorized classifier — 6 frozen-body debts documented (docs/CODE_REVIEW_FINAL.md). | THE SESSION'S RECORD: 3 experiments (exp302/303/304, all pre-registered before their bodies, all 4/4, all bodies main-agent-written), 2 synthesis deposits (docs/SYNTHESIS_FINAL.md, docs/CODE_REVIEW_FINAL.md), the README completed, PROJECT_COMPLETE.md written, everything pushed. | THE PROJECT IS COMPLETE. The entry is written. The final state is pushed. **STOP.**

L290c | ==================== THE SEARCH DOCUMENTATION (the completion-gap fix; Task 1 of the completion-gap session, written BEFORE any new experiment runs) ==================== | **THE GAP (disclosed)**: the final session's handoff (Section 2) directed "run up to 10 experiments you genuinely believe could fundamentally change or enhance the result ... **run fewer if you cannot identify 10**. The cap is 10, not a target." Three ran (exp302/303/304 — all headline-grade, all 4/4, all pre-registered); the session then declared Phase 1 complete **without documenting the search** — the honest accounting ("here is every candidate considered, and why I stopped") was never written. THIS ENTRY IS THAT ACCOUNTING. | **THE FULL CANDIDATE POOL** (14 candidates, each re-judged against the pre-registration bar "could it fundamentally change or enhance the headline"): **(1) exp302 the composed stress face** — HIGH-LEVERAGE (the ~29x single-register protection had never been measured under composition; either the protection composes or the strongest engineering result is a single-register artifact) — RAN, landed PROTECTED-PRESERVED (+13.13 mV, the stress decode-invisible). **(2) exp303 the zero-substrate 8th formalization (the transport form)** — HIGH-LEVERAGE (the last star, attacked on the program's own output — the strongest form yet stated) — RAN, landed TRANSPORT-REFINES-DEEPENED. **(3) exp304 the degeneracy repair + the carrier's stream** — HIGH-LEVERAGE (a disclosed pre-registration hole repaired pre-named + the first carrier-stream transport face; BOTH-BOUND was a live branch) — RAN, landed BOTH-BOUND (0/130). **(4) the ca2 unblock (NOW exp305)** — WRONGLY LEFT ON THE TABLE: exp296 landed CARRIER-GENERAL with ca2 the sole inert holdout (+0.0042 mV, 0/12 hosts) and the inertness was never diagnosed (the landed gain form's contrast is battery-mean-centered and near-flat in the working voltage window — a zero-mean modulation cannot move a zone-mean decode); whether the register can unblock the last dormant channel is a real branch with a real negative tail (a structural-inertness verdict would close the channel sweep at 3 carried + 1 structurally inert) — **PROMOTED, runs this session**. **(5) the premium's structural residual under the composed carrier (NOW exp306)** — WRONGLY LEFT: exp294 landed PREMIUM-MIXED (the noise-carried fraction dissolved +0.86→+0.27; the structural residual straddles at +0.42) and the composed carrier (+13.13 mV) did not exist yet; whether the union's commits dissolve the residual is a real branch (UNION-DISSOLVED would close the premium story entirely) — **PROMOTED, runs this session**. **(6) the composed carrier's transport — the handoff's candidate #3, WITH A PREMISE REPAIR DISCLOSED**: the handoff describes exp304 as having tested "the *single* carrier's stream"; in fact **exp304's carrier arm IS the composed union** (faces=(ctx, gj, apop) at the composed optimum g=1.0, arm A0 — the G1 anchors bind to exp300's deposited union rows bit-exact 12/12), so the literal question "does the composed carrier transport" is **ALREADY ANSWERED** (exp304 F3: 0/130, BOTH-BOUND) and re-running it would be a duplicate, not an experiment. The genuinely open transport question is the one the project's own final form pre-named three times (L289's final form, PROJECT_COMPLETE's next-researcher #1, SYNTHESIS_FINAL §5): the binding is the **indexation**, and the one untried door is a **wiring-independent zone-addressing scheme** — **PROMOTED as the 9TH FORMALIZATION (NOW exp307, the class-reindexed transport form)**, where either branch changes the completion state (TRANSPORT-UNBLOCKED weakens the 8-formalization block; ZONE-BOUND sharpens it at 9). **(7) the carrier's shelf faces** (L275's (i), carried through L288(b)/L289's open list) — REJECTED as polish: they re-measure the landed carrier's decode on other battery rows/shelf states; no branch can change a headline the 72-row battery already measures. **(8) the write-side stress face on exp301's form** (the digest/cvt faces under the A1 pin, L288(c)) — REJECTED as answered-at-a-stronger-read: exp302 answered the stress question at the decode (+0.0000 mV); the digest-face version is a weaker instrument on an answered question. **(9) a str-channel union variant** (faces=(ctx,gj,apop,str)) — REJECTED as a category error: str's landed form sits on its own de-pairing protocol whose no-history control sits at 6.04 mV on its own battery (its −5.07 delta recovers its own intervention's damage; the ctx/gj/apop faces compose on the substituted battery whose control is 0.97 mV); and exp298 landed ADDITIVE with the union at g=1.0 bit-exact equal to the best single (the re-assertion subsumes at saturation) — a 4th face adds nothing at the optimum **by a landed result**. **(10) a ca2 dose ladder** (exp297's form) — REJECTED as contingent-polish: if exp305 unblocks, the dose face is exp297's landed form re-run (g=1.0 is the optimum on every carried channel); if exp305 stays inert there is nothing to ladder. **(11) the composed protection re-measured on the 100-host battery** — REJECTED as polish: exp302's 12/12 hosts with the per-host P within [10.86, 14.71] already carries the mechanism; a wider battery changes no branch. **(12) a random-reindexation transport control** — REJECTED as garnish: the negative is already 0/130 in two forms; a random control characterizes nothing pre-named. **(13) the register state (phi_history) as the transported object** — REJECTED as strictly dominated: the register is the stream's last-write-wins coarsening (exp290 STORAGE-SIDE); the complete stream transports nowhere, the coarsening cannot. **(14) a composed mega-face** (the union + the write-side pin + the shelf states in one arm) — REJECTED: exp302's stress delta under the union is exactly +0.0000 mV — no measurable headroom remains for a further composition to resolve. | **THE VERDICT OF THE SEARCH**: 3 ran in the final session (slots 1–3), **3 promoted by this entry** (slots 4–6 = exp305/306/307 — the only remaining candidates whose both-tails change a headline), 8 rejected with the reasons recorded above (polish, category error, dominated, or answered). **THE CAP STANDS AT 6 OF 10** — after exp305/306/307 the remaining 4 slots have no takers at the pre-registration bar, and the cap was never a target. | REGISTERED NEXT: exp305 → exp306 → exp307 (this session, in that order; each pre-registered before its body per the house discipline), then THE RE-CLOSE (the synthesis update, PROJECT_COMPLETE.md, the final ledger entry, the push, STOP).

L291 | exp305 — THE LAST DORMANT CHANNEL: THE REGISTER UNBLOCKS ca2 (C, 4/4, branch **UNBLOCKED** — the ca2 channel's inertness was FORM-SPECIFIC, not structural; ledger L290c's promoted candidate (4) EXECUTED, the body written by the MAIN AGENT [pre-registration 6278182, the body-only discipline, the pins sha-asserted vs 6278182]): G1 PASS (the anchors: the rebuild sha-asserted 12/12 vs exp243 + edges/boundary/canon/f_max/non-negative + the H0==H1 chain echo; the deep targets 72/72; **THE DORMANT CANARY: the 12 dormant rows (seed 1, instance 0 per host, g=0.0) reproduce exp282's deposited err_exact BIT-EXACT 12/12 + the trace shas BIT-EXACT 12/12 + exp256's A3 errs 12/12** — the walk machinery's identity, exp304's G1 form; exp256's 72 substituted records re-read as the control (the err chain vs exp282 72/72); 4 deposits READ-ONLY sha before/after; the port + exp142 NOT modified; the zero-reader scan clean; the test suite green) | G2 PASS (per arm 72 rows: the register's faces 144/144; n_arm_writes == walk_steps == n_ch4_writes 144/144 (both arms arm EVERY committed cell); the site-write counts constant across the seeds 24/24 per arm; the A3 convention 144/144; the stream face 144/144 (the walked count arm- and g-independent); the C1 gain faces: the gains finite, within [1−g, 1+g] — **the observed spread [0.98867, 1.00307]: the live-gate contrast is as flat as the battery-mean contrast (~1e-2)** — the inertness mechanism CONFIRMED quantitatively) | G3 THE BRANCH: **UNBLOCKED** — C1 CONTRAST-GAIN inert (+0.0068 mV, 0/12 hosts; the mean err 0.9807 vs the control 0.9739 — the one pre-named knob change does NOT rescue the gain form: the contrast is too flat in the working window, now measured, not assumed); **C2 CA2-BLEND CARRIES (−0.3550 mV, 12/12 hosts; the mean err 0.6189, the worst 3.64, verified 72/72)** — the house blend form (exp289's ctx form VERBATIM) at exp261's site semantics (every committed cell) carries at EXACTLY the apop single's / the union's delta: **the subsumption face re-confirmed at a THIRD form** (exp298's ADDITIVE + exp300's MONOTONE-TO-1.0 predicted it: at g=1.0 every re-assertion form covering the walked band lands the same decode — only the site set matters, and all three cover the band); the NEW mechanism face: **C2's cvt_rms == 0.0 exactly 72/72 — the blend at g=1.0 writes hist_i == the register's init face == the spec install: the committed values equal the target at every committed cell** (exp304's content-face reading, now seen AT the commit layer); the canary bit-exact 12/12 | G4 PASS (deterministic, no wall-clock fields, 4 deposits READ-ONLY sha before/after, exp142 + the port NOT modified, floor −60.0 at entry/after the canary/after each arm/at exit, the test suite green) | run form: in-process one invocation (~5 min) | deposited results/exp305_ca2_unblock.json | **THE SCIENTIFIC READING**: (i) the channel sweep CLOSES 4/4 — every channel now carries under some register coupling form (gj blend at the junctions, str blend at the de-pairing targets, apop sigma at the marks, ca2 blend at every committed cell; ctx the original); ca2's dormancy was never structural — the channel's WRITE PATH reaches the decode the moment the coupling's contrast stops being zero-mean-flat; (ii) the gain form's negative tail is now a measured closure (the spread [0.9887, 1.0031] cannot move a zone-mean decode — the C1 arm's +0.0068 over 12 hosts), not an assumption; (iii) the −0.3550 landing on the union's own delta is the third independent confirmation that the saturation face is form-invariant | REGISTERED NEXT (per L290c's order): exp306 — the premium's structural residual under the composed carrier (does the union's commit layer dissolve exp294's straddling +0.42 residual?).

L292 | exp306 — THE PREMIUM UNDER THE COMPOSED CARRIER: THE STRUCTURAL RESIDUAL DISSOLVES AT THE LIMIT (C, 4/4, branch **UNION-DISSOLVED** — and the dissolution is the STRONGEST possible form: the committed pattern's host dependence is IDENTICALLY ZERO; ledger L290c's promoted candidate (5) EXECUTED, the body written by the MAIN AGENT [pre-registration c963c4e, the body-only discipline, the pins sha-asserted vs c963c4e; ONE runtime body fix disclosed: the regression read crashed on a constant response — the fresh mean_cvt is EXACTLY equal across the 12 hosts (all ranks tied, n_distinct == 1) — and the degenerate-constant face now records rho = 0.0 under the pre-named dissolution semantics with the ties census carrying the disclosure; the docstring/gates/bars byte-unchanged, the pre-named branch lattice unbroken]): G1 PASS (the anchors: the rebuild sha-asserted 12/12 vs exp243 + the H0==H1 echo; the deep targets 72/72; **THE MARKS' VALIDITY: the rebuilt q10/q90 + target_part + bands reproduce exp300's deposited arm_inputs BIT-EXACT 24/24 + 12/12**; **THE EXP300 ANCHOR: the 72 union walks reproduce exp300's deposited union g=1.0 rows BIT-EXACT — the errs 72/72 + the trace shas 72/72 + the per-row cvt_rms 72/72 + the per-host mean_cvt 12/12 — the commit layer IS the deposited union's, not a new instrument**; the convention self-check vs exp287's deposited rhos BIT-EXACT 2/2; the covariate carries (mia + premium) bit-exact 12/12 + 12/12 via exp273's field table; 7 deposits READ-ONLY sha before/after; the port + exp142 NOT modified; the zero-reader scan clean; the test suite green) | G2 PASS (the commit layer's definition: the commit count == walk_steps == the trace length 72/72; the indices unique 72/72; the coverage 72/72; the values finite 72/72; cvt_rms finite 72/72; the A3 convention 72/72; the register's replay + complement faces 72/72; the face-write bookkeeping (sigma + blend) constant across the seeds 24/24; the gj conservation identity re-run per row) | G3 THE BRANCH: **UNION-DISSOLVED** — **rho(mean_cvt)~mia_prod_err = 0.0000 and rho(mean_cvt)~one_zone_premium = 0.0000, both BY DEGENERACY (the ties census: n_distinct == 1, max_multiplicity == 12 — the fresh per-host mean_cvt is EXACTLY 0.0 on every host: the composed union's committed values ARE the target values identically, cvt_rms == 0.0 exactly 72/72)** vs exp287's deposited +0.8616/+0.7790 (the un-coupled commits) and exp294's self-carrier +0.2679/+0.4175 (the straddling residual) — **the premium's footprint on the commit layer is not merely below the 0.40 bar, it is ZERO: there is nothing left to be host-dependent** (the Spearman rho is mathematically undefined on a constant response — 0/0 — recorded as 0.0 under the pre-named dissolution semantics, disclosed in the deposit's degenerate_constant_response faces); the audit faces: the union's mean err 0.6189 (the exp300/exp302 form reproduced), the worst 3.64 under the 6.0 bar, the delta correlation 0.0745 (audit-only) | G4 PASS (deterministic, no wall-clock fields, 7 deposits READ-ONLY sha before/after, exp142 + the port NOT modified, floor −60.0 at entry/after the battery/at exit — NO pin anywhere, the test suite green) | run form: in-process one invocation (~2.5 min) | deposited results/exp306_premium_under_union.json | **THE PREMIUM STORY CLOSES**: exp287 found the premium living in WHAT the program committed (the un-coupled commits' host structure, rho +0.86/+0.78); exp294 found the self carrier dissolving the noise-carried fraction while the structural residual straddled (+0.27/+0.42); **exp306 finds the composed union's commit layer IDENTICALLY the target — the committed pattern carries no host structure at all (0.0/0.0 by identity, not by statistics)** — the spec-layer premium was the un-asserted spec's noise structure all the way down, and once the commit layer IS the spec (the union at g=1.0, the saturation face), the premium has no substrate left to live in | REGISTERED NEXT (per L290c's order): exp307 — the zone-indexed transport form, the 9TH FORMALIZATION of the zero-substrate star (the wiring-independent zone-addressing door the project's final form pre-named; either branch changes the completion state).
