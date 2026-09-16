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
