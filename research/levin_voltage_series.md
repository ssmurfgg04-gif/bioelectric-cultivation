# The Levin voltage series — deep mine of the published Vmem record (Task 5-a)

**Agent:** subagent-levin-series · **Date:** 2026-09-16 · **Machine-readable series:**
`research/levin_voltage_series.json` (119 entries).

**Protocol.** Read-only deep mine, per the HANDOFF ("exp39 got 6/6 direction match; go
deeper"). Sources used, in order: (1) the repo's own artifacts —
`results/exp39_levin_voltage.json`, `research/LEVIN_VOLTAGE_COMPARISON.md`, the
PlanformDB 2.5.0 database (`data/planform/planformDB_2.5.0.edb`, direct SQL over
Publications 1/4/16/20 = Oviedo 2010, Beane 2011, Oviedo 2007, Nogi 2005),
`research/bioelectric_literature.{json,md}` (77 verified papers), the ledger
L66/L73/L74/L99–L105; (2) targeted verification fetches this session (Europe PMC REST
abstracts + open-access full texts; raw files in `/tmp/levin_series/`); (3) web search
for the Pietak/Levin BETSE modeling values, Marsh & Beams 1952, and Molano preprints.
No experiments were run; no existing file was modified.

**Entry kinds.** `recorded-outcome` (99 PlanformDB rows — every published
bioelectric-manipulation experiment the DB carries, with outcome frequencies and n),
`exp39 direction-match pair` (6), published quantitative series (3), direction claims
(4), timing claim (1), method anchor (1), review anchor (1), classic record (1),
absolute-mV measurement (1, Xenopus), modeling values (1, BETSE), stack-side inference
constants (1). **2 entries carry absolute mV** — both non-planarian. That is the
record's honest shape.

## 1. Honest scope (sharpened from exp39)

- **Zero absolute mV values are published for planarian tissues** — 70+ years after
  Marsh & Beams (1952) and through the DiBAC4(3) era (Oviedo 2008 protocol), the
  planarian record is a record of *relative* polarities, *outcome frequencies*, and
  *timing kernels*. exp39's scope statement stands; what changes here is that the
  series now carries **every** recorded quantitative row, not six direction claims.
- Absolute numbers exist in adjacent models only: Xenopus impalement
  (**−19.4 mV** hyperpolarization delta, Chernet 2013, n=5) and the lab's own
  simulator BETSE (resting **−63.7 mV**, band **−10..−80 mV**, bistable pair
  **−57 → −14 mV**, GJ voltage-gating half-closed **15 mV** — Pietak & Levin,
  doi:10.3389/fbioe.2016.00055, often cited as 2017).
- PlanformDB carries **no drug concentrations** (L16); the octanol/heptanol rows carry
  exposure timing under exp33's registered *hours* reading. The unit ambiguity for the
  Oviedo 2010 Fig 2A kernel is owned in Target T1.
- Flagged and excluded: Molano single-author bioRxiv barium preprints (2023/2024,
  non-peer-reviewed; not resolvable this session beyond subagent 2-b's note).
- Citation hygiene: the "Durant 2019 = PMID 30824103" directive claim was already
  corrected to MED30799071 (night eight); re-verified here. Durant 2017's octanol
  is **127 µM stated** (10 µL/500 mL); Emmons-Bell 2015's is **123 µM stated**
  (8 µL/500 mL).

## 2. The series (tables; every row is in the JSON)

### 2a. exp39's six published-vs-model pairs (re-verified, results file intact)

| # | Published claim (source) | Model quantity | Verdict |
|---|---|---|---|
| V1 | Depolarization drives head formation (Beane 2011, PMID 21276941) | head −24.86 mV > tail −50.26 mV | MATCH |
| V2 | H,K-ATPase RNAi hyperpolarizes → shrunken heads (Beane 2013, PMID 23250205) | ion-arm abnormal 1.00 vs cutting 0.00 | MATCH |
| V3 | GJ/neural modulation → ectopic anterior blastemas at posterior wounds (Oviedo 2010, PMID 20026026) | posterior-depol head-likeness 0.946 ≥ 0.7 | MATCH |
| V4 | smedinx-11 RNAi inhibits regeneration, mixed/graded (Oviedo 2007, PMID 17670787) | gap_scale 0.05 → blind-guess rate 0.667, errs [6.21, 7.00, 5.94] mV | MATCH |
| V5 | Wounds depolarize vs intact (wound-current lit; PMID 21276941) | wound −38.03 > settled mean −43.63 mV | MATCH |
| V6 | Stochastic phenotypes under identical perturbation; bistable memory (Pezzulo & Levin 2021, PMID 33550952) | exp38 re-anchor q=0.55 splits seeds [16.51, 14.66, 2.81] mV | MATCH |

### 2b. The octanol/GJ-blockade record (PlanformDB rows, Oviedo 2010 + Nogi 2005)

**The pre-treatment kernel (Oviedo 2010 Fig 2A; the record's sharpest timing
structure, 6 rungs + control).** Post-pharyngeal crop, D. japonica, DH = double-head
(ectopic anterior):

| eid | octanol pre-treatment (DB StartTime, exp33 hours-reading) | DH fraction | n |
|-----|-----|-----|-----|
| 434 | none (control) | 0.00 | 10 |
| 435 | 0.13 | 0.85 | 10 |
| 436 | 0.25 | 0.90 | 10 |
| 437 | 0.50 | 0.58 | 10 |
| 438 | 1 | 0.10 | 10 |
| 439 | 2 | 0.10 | 10 |
| 440 | 3 | 0.10 | 10 |

Edge between rung 3 and 4. Under the *days* reading (0.13 d ≈ 3 h … 3 d) the edge is
12–24 h — inside the stack's deadline band (12–72 h, exp121/124). Under exp33's
*hours* reading the edge is < 1 h. This ambiguity is T1's first gate.

**The VNC-disruption kernel (Fig 2B).** VNC cut at t = 0 / 0.125 / 0.5 / 1 (days per
exp33 reading) → DH 0.18 / 0.75 / 0.20 / 0.00 (n=10 each; eids 441–444).

**Amputation-level series (Fig 1A/1B, octanol, n = 107–178/eid).** DH fraction by
plane: head 0.05 (eid 415), pre-pharyngeal 0.28 (416), pharyngeal 0.50 (417),
**post-pharyngeal 1.00 (418, n=145 — the "100% DH pretail fragment" Durant 2017
cites)**, tail 0.00 (419). Head+post-pharyngeal double cut suppresses it (0.05, eid
423). Fig 3 innexin RNAi (Dj-inx-5+13, Dj-inx-12): pharyngeal 0.20 DH / post-pharyngeal
0.80 DH (eids 448/449); Fig 4 combined octanol+notch → double/triple/quadruple heads
(451–456); Fig 5 ectopic-polarity persistence through re-cut (457–461, all 1.00);
S9B b-catenin epistasis (1062–1071).

**Nogi 2005 heptanol series (Publication 20; the largest-n rows in the DB).**
Pharyngeal crop + heptanol: WT 0.57 / tailless 0.25 / DH 0.18 at **n=423** (eid 322);
pharyngeal heptanol n=111 (WT 0.32/tailless 0.59); pre-pharyngeal n=71; head n=54;
post-pharyngeal n=86; tail n=57 (all WT 1.00 — heptanol needs the posterior-facing
wound, same plane-dependence as octanol); hexanol n=1 (eid 324).

### 2c. The H,K-ATPase / depolarizing-drug record (Beane 2011 rows)

SCH-28080 (H,K-ATPase block → hyperpolarization), 0–3 d window, by amputation plane:

| eid | plane | WT | cyclop | headless | n |
|-----|-------|----|--------|----------|---|
| 391 | head crop | 1.00 | 0.00 | 0.00 | 120 |
| 392 | pre-pharyngeal | 1.00 | 0.00 | 0.00 | 138 |
| 393 | pharyngeal | 0.22 | 0.11 | **0.67** | 175 |
| 394 | post-pharyngeal | 0.68 | 0.16 | 0.16 | 111 |
| 395 | tail crop | 0.42 | 0.18 | 0.40 | 106 |

**The opposing pair (same slanted-fragment protocol).** Ivermectin (depolarizer):
DH **0.92** (eid 411, n=11) vs SCH-28080: headless **1.00** (eid 412, n=13);
ivermectin + chloride-flux rescue: WT 0.63 (eid 413); nicardipine: cyclop 0.34 /
headless 0.08 (eid 414, n=61); SCH-28080 + K⁺ rescue: WT 0.94 (eid 297).

### 2d. smedinx-11 (Oviedo 2007) and the curated quantitative entries

- **smedinx-11 RNAi** (S. mediterranea): trunk crop → trunk remnant 1.00 (n=30, eid
  279); homeostasis → contracted pre-pharyngeal 1.00 with reduced-posterior 0.87 (eid
  280) + the AP neoblast gradient claim.
- **Durant 2017** (PMID 28538159): octanol 127 µM on trunk fragments → DH:cryptic
  ratio ≈ **25:75% across all experiments**; cryptic state stored via global
  resting-potential gradient (DiBAC), re-cut reproduces the ratio for months; 2.1%
  radial morphs excluded.
- **Durant 2019** (PMID 30799071): depolarizing pulse in the **first 3 h** alters gene
  expression **by 6 h** → double-headed despite confirmed nigericin washout; 3 h
  sufficiency and 6 h transcriptional deadline are the two quantitative hooks
  (exp54's gates already encode them: 3 h pulse writes 3.00 mV; ≥1 h-later starts
  ~0.5 mV; 12 h start = 0).
- **Emmons-Bell 2015** (PMID 26610482): octanol 123 µM → stochastic species-specific
  head shapes in wild-type *G. dorotocephala*; control fidelity 100%; DiBAC 0.19 µM
  protocol; remodel-back within weeks.
- **Emmons-Bell 2019** (PMID 31765995): 1 mM BaCl₂ → anterior degeneration within
  72 h, adaptation over ~35 d of continuous exposure (N>50 × 3 replicates).
- **Chernet 2013** (PMID 23471912, Xenopus): GlyRF99A + 70 mM Cl⁻ hyperpolarizes by
  **−19.4 mV** (electrode impalement, n=5, P<0.001); depolarized ITLS signature;
  ivermectin 4-fold ITLS increase. **Chernet 2014** (PMID 24830454): remote-cell
  hyperpolarization normalizes KRAS tumorigenesis at long range.
- **BETSE** (PMID 27458581): −63.7 mV resting; −10..−80 mV band; −70/−18/−57→−14 mV
  panel incl. a bistable depolarized state; GJ gating 15 mV.
- **Marsh & Beams 1952** (doi:10.1002/jcp.1030390203): applied field strength controls
  axial polarity in *D. tigrina* — the founding direction claim.

## 3. Direction-signature patterns

1. **Polarity skeleton (universal):** anterior/head depolarized, posterior/trunk
   hyperpolarized, wounds depolarized. Every record row is consistent with it; none
   contradicts it (exp39's 6/6 is this pattern, minimally sampled).
2. **GJ blockade phenocopies depolarization at posterior-facing wounds** — octanol
   (123–127 µM), heptanol, innexin RNAi all shift posterior fates to ectopic anterior,
   with plane-dependence (post-pharyngeal ≫ head) and stochastic penetrance (25:75;
   species-specific shapes). 68 of the 99 DB rows carry this signature.
3. **H,K-ATPase block is the opposite lever:** hyperpolarization → anterior failure
   (headless/cyclop), pharyngeal worst, identity-vs-size dissociation (Beane 2013).
   The record's cleanest 2×2: ivermectin DH 0.92 vs SCH-28080 headless 1.00 on one
   protocol.
4. **The quantitative axes are TIME, not mV:** the 3 h write window / 6 h deadline
   (Durant 2019), the pre-treatment kernel (Fig 2A), the VNC-disruption kernel
   (Fig 2B), the 35 d adaptation (BaCl₂), months-long cryptic memory (Durant 2017),
   >1 week storage (Pezzulo 2021).
5. **Stochastic multi-attractor switching is measured, not anecdotal:** constant
   25:75 DH:cryptic ratio, re-cut-stable; species-specific head shapes; seed-split
   under identical perturbation — the bistability the stack's q/coin machinery models.
6. **Adjacent models carry the absolute scale:** Xenopus −19.4 mV impalement delta;
   BETSE −10..−80 mV band and bistable −57→−14 mV swing. These are the only mV anchors
   the series has, and they are enough for Target T5.

## 4. Ranked quantitative targets against the adopted stack

Stack constants (verified in `cultivation/bioelectric/collective.py`): dV/dt =
γ(θ−V) + ΣG(V−V) + η; dθ/dt = ε(V−θ) + μΣ(θ−θ); defaults γ=0.25, g_gap=0.20, ε=0.04,
μ=0.015. Laws: exp84 quadrature err=√(eV²+eT²) (bar 6.0 mV); exp120–124 mu-silence
deadline (γ1 never / γ4→48 h / γ16→72 h / γ64→36 h; μ doubling 48→36→12 h;
conjunctive); exp91/92 dose axes (threshold d∈[0.35,0.45], 3/7 at 0.40); exp54 write
window (3 h pulse = 3.00 mV, ≥1 h-later ~0.5 mV, 12 h = 0).

**T1 — Fit the octanol pre-treatment kernel with the mu-silence deadline (highest
rank: direct continuation of exp120–124 against the record's sharpest kernel).**
*Stack predicts:* GJ-blocker = dual-channel cut; the record's DH-vs-pre-treatment
curve is a deadline; exp124's analytic homogenization rate per mode
μλ + εγλ/(γ + gλ), fit once to the torus's four edges, predicts new edges with zero
free parameters. *Published:* DH 0.85/0.90/0.58/0.10/0.10/0.10 at rungs
0.13/0.25/0.5/1/2/3 (+control 0.00; eids 434–440) and the VNC kernel 0.18/0.75/0.20/0.00
(eids 441–444). *Gate:* (a) resolve the rung units against the paper (days-reading
brackets the edge at 12–24 h = inside the deadline band; hours-reading keeps exp33's
L16 directional miss and forces a remap — both outcomes decisive); (b) under the
chosen reading, one fit of the deadline curve to Fig 2A must predict Fig 2B's four
points (Spearman ≥ 0.8, zero refit). *Runtime:* ~1–3 min (11 arms × 8 onsets; exp123
machinery; exp118 full corpus = 2.6 s reference).

**T2 — Amputation-level ordering under hyperpolarization + the ivermectin/SCH
opposition.** *Stack predicts:* the ion arm (γ×0.5, noise×3, D_PAR per exp92) produces
plane-ordered anterior failure and, per exp39-V3, posterior depolarization → ectopic
anterior (HL 0.95): the 2×2 must come out sign-correct. *Published:* headless 0.67 /
0.16 / 0.40 / 0.00 / 0.00 across pharyngeal/post-pharyngeal/tail/pre-pharyngeal/head
(eids 391–395, n=106–175); ivermectin DH 0.92 vs SCH-28080 headless 1.00 (eids
411/412); chloride rescue WT 0.63 (eid 413). *Gate:* Spearman(published headless by
plane, sim ion-arm abnormal by plane) ≥ 0.6 AND both arms of the ivermectin/SCH
contrast sign-correct (strict — one wrong sign refutes the polarity mapping). 
*Runtime:* seconds (5 planes × 3 seeds; exp39 machinery).

**T3 — The 25:75 bistable ratio as the q-ladder's fixed point.** *Stack predicts:*
the M31-A re-anchor coin q splits seeds (exp39-V6's 3-seed split at q=0.55); there
exists q* with P(DH) = 0.25 exactly, and the ratio is re-cut-stable because the coin
is a stored face-window state. *Published:* DH:cryptic ≈ **25:75%** across all
Durant-2017 experiments, ratio reproduced on re-cut of normal-looking regenerates;
TAS's adjacent fitted re-challenge penetrance ~15% (PPRPPR1216581). *Gate:* find q*
in [0.4, 0.8] with split 0.25 ± 0.10 at n ≥ 24 seeds; second-round re-cut of normal
survivors reproduces the ratio within ±0.10 (the cryptic property — if the ratio
drifts, the memory-carrier story is wrong). *Runtime:* ~5–10 min (8 q-values × 24
seeds × 2 rounds).

**T4 — The dose axis meets the first recorded concentration ladder (biphasic risk
owned).** *Stack predicts:* exp29-S2R3 monotone junction-dose response (3.28→3.93→
4.54→6.03 mV at gap_scale 1.0→0.05) and exp91/92's threshold (graded window
d∈[0.35,0.45]); the record's morphogen partial block sits at 0.105–0.189 below the
sim threshold. *Published:* metformin 10-point concentration ladder in D. japonica
(Genes 2025, PMID 40282325, n=30/dose, eyespot-regeneration TIME in hours):
**100 nM / 10 µM / 1 mM promote, 40 mM inhibits — biphasic**. *Gate:* pre-registered
three-form comparison (monotone / threshold / biphasic-with-promote-band) on the 10
points; the biphasic shape, if it maps through a single monotone dial, REFUTES the
monotone dose-response prediction — the honest registered risk exp29's S2R3 carries.
Also extends exp91's amplitude axis to a real concentration axis (the first in the
program). *Runtime:* minutes (10 dose arms × 3 seeds at the exp92 mapping).

**T5 — Absolute-value anchor: GHK-inferred map vs the BETSE band and Chernet's
delta (cheapest, weakest refutation power — ranked last).** *Stack predicts:*
`cultivation/validation/vmem_inference.py` (GHK, E_K ≈ −90 mV, RT/F 26.7 mV) emits an
absolute planarian Vmem map; exp1's calibration (head −24.9 / trunk −50.3 / wound
−38.0) is a *choice*, and this target tests that choice against the only absolute
numbers the record has. *Published:* BETSE band −10..−80 mV with bistable swing
−57→−14 (43 mV); GJ gating 15 mV; Chernet's measured knockout delta −19.4 mV (n=5). 
*Gate:* inferred head/trunk/wound values inside the band with the head–trunk delta
(25.4 mV) and wound depolarization (12.2 mV) within ±50% of the bistable-swing and
knockout-delta scales; pre-registered as calibration (failure = recalibration
target, not falsification). *Runtime:* seconds (pure arithmetic; module + tests
exist).

## 5. What the series does NOT settle (honest gaps)

- Absolute planarian mV: still unpublished; T5 is an anchor against adjacent scales,
  not a validation.
- Organ-size scaling (Beane 2013) and the neoblast-gradient substrate (Oviedo 2007):
  still the model's named missing layers (exp39's gaps, unchanged).
- Durant 2019 per-arm percentages and Oviedo 2010's octanol concentration are not
  text-verifiable from here (paywalled; DB has no concentrations).
- Emmons-Bell 2015's per-shape frequencies live in figures only.
- Molano barium preprints: excluded (non-peer-reviewed, unresolvable this session).

## 6. Next actions for the main agent

1. Run T1 (the exp124 analytic deadline fit vs the Fig 2A/2B kernels) — it closes the
   L16 residual with the exp122 semantics and zero new model code.
2. Then T2 (one script, seconds) and T3 (the q-ladder) as a single session.
3. T4 needs the metformin Genes-2025 numbers pulled into a small data file first
   (subagent 2-b verified OA full text via Europe PMC).
4. T5 can run any time (module exists; `tests/test_vmem_inference.py` green).

*Deposit: this file + `research/levin_voltage_series.json` (119 entries; raw fetches
in /tmp/levin_series/). No experiments run; no existing files modified.*
