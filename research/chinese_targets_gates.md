# Chinese Dose/Morphology Targets — Pre-Registered Gates Against the Adopted Stack

**Task ID:** 5-c (subagent-chinese-targets). **Session:** 2026-09 (sandbox).
**Inputs:** `research/papers/chinese_planaria_mining.md` (the 3 machine-readable
targets, subagent 2-b), `research/chinese_literature.{md,json}` (R-3's
access-barrier map), the ADOPTED dose-mapping machinery (`exp91` L73, `exp92`
L74), the full-corpus harness (`exp118`, L99) and its deposited results
(`results/exp118_corpus_full.json`), `exp124`'s `run_deadline` (L105), ledger
L73/L74 in `docs/FALSIFICATION.md`.
**Rule of the document:** every gate below is pre-registered BEFORE any run;
constants are pinned, never re-derived on Chinese data; no existing file is
modified; the runnable artifact is `experiments/scaffold_chinese_targets.py`
(a SCAFFOLD — assign an exp number and finalize before running).

---

## 0. What the gates bind to (the ADOPTED stack, pinned)

The adopted corpus mapping is **exp92's final pass (L74)**: the exp88 C1–C4
arm wiring + the row-level dose classes. Its constants (pinned, bit-exact
required):

| Constant | Value | Origin |
|---|---|---|
| `D_PAR` | **0.25** | exp92's pre-registered selection: the fine-ladder dose whose wnt\|trunk rate (0.000) is closest to the pinned modulator-block mean (0.105); tie-break lowest d |
| `GEN_BIAS` | **0.321** | exp83's measured control hot bias (L64) |
| ABN verdict | pattern_error ≥ 6.0 mV OR head_likeness ≥ 0.7 | exp1 calibration, untouched |
| seeds | (1, 2, 3); arm rates = mean over seeds, 3 dp | the L70–L74 convention |
| eid 421 pin | ("gjblock", "head", 0.5) | the adopted pin (L70) |
| C4 exclusion rule | cutting ∧ recorded ≥ 0.9 ∧ plane ctrl-rate ≤ 0.35 → excluded from the decoded frame | exp88 (C4); **21 rows** |
| Class rule | effector = /bcatenin\|betacatenin\|beta-catenin\|apc\|axin/i → d = 1.0; else modulator → d = D_PAR | exp92, pre-registered from canonical Wnt biology |

Deposited reference numbers the anchor gate must reproduce
(`results/exp118_corpus_full.json`, L99; L74 before it):

- **decoded MAE 0.290** (n = 884; the L74 reference — exp118's full run
  re-derived it exactly after exp91/exp92's own result JSONs were lost in the
  2-a rollback incident); raw MAE 0.3705 (L74: 0.371, n = 905); conservative
  0.3063; decode accuracy 0.6928.
- DB extraction pins: L73 partial block n=17 / mean 0.189; L74 modulator
  block n=11 / mean 0.105; per-plane control rates head 0.00 / trunk 0.38 /
  tail 0.49; C4 = 21 rows.
- Mapped-arm rates the targets land on (deposited arm table):
  ('wnt','tail',0.5,**0.25**) → **0.0**; ('wnt','tail',0.5,**1.0**) → **1.0**;
  ('wnt','trunk',0.5,0.25) → 0.0; ('wnt','trunk',0.5,1.0) → 1.0;
  ('generic','trunk',0.5,None) → **0.667**; ('cutting','trunk',0.5,None) → **0.0**.
- **Honest coverage: 0.619** (905 of 1,462 outcome rows mapped; 1,716 total;
  47 unique sim arms; unmapped = graft/irr/lateral/no-cut/non-AP/no_outcome).
- **The D. japonica slice baseline** (per-species columns of exp118): 383 DJ
  experiments, 182 scored, decoded MAE **0.407** (n = 172 non-C4), decode
  accuracy **0.560** — the corpus's weakest major slice (corpus: 0.290 / 0.693).
  **All Chinese-target gates are judged against THIS baseline, not the corpus
  one** — judging them against 0.290/0.693 would be rigged to pass.

Harness reuse: `exp118_corpus_full_mine.py` supplies `build_rows` (the pure-DB
record side, full-corpus in both modes), `map_arm` (the adopted mapping,
verbatim), `run_arms`/`attach_sim`/`mae`, and the pinned constants.
`exp124_deadline_curve.run_deadline(adj, seed, gamma, onset) -> BREAK` is the
adopted onset-sweep (timing) instrument — **compiler substrate** (grid2d/torus
via `exp112.build_battery`), NOT the 1D corpus sheet; flagged where used.

---

## ANCHOR GATE (shared, must be read FIRST — before any target gate)

### A-G1 — the L74/exp118 reference reproduces bit-exactly

- **The deposited number:** decoded MAE **0.290** (n = 884) and raw MAE
  **0.371** (0.3705, n = 905) on the full-corpus mapped slice, with the pinned
  constants above, the DB extraction pins (L73 17/0.189, L74 11/0.105, ctrl
  0.00/0.38/0.49, C4 = 21), and the deposited arm-table entries the targets
  bind to (wnt\|tail 0.25 → 0.0; wnt\|tail 1.0 → 1.0; generic\|trunk → 0.667;
  cutting\|trunk → 0.0) each re-derived bit-exactly (3 dp) with one
  determinism re-run.
- **Pass:** decoded within ±0.005 of 0.290, raw within ±0.005 of 0.3705, all
  DB pins exact, all four arm anchors exact, determinism re-run exact.
- **Refute:** any miss = harness or extraction drift (the exp118 G1/G5
  discipline). **No target gate may be read after a refuted anchor.**
- **Third outcome:** decoded reproduces but one DB pin misses → the drift is
  record-side (DB load/rounding), not mapping-side; diagnose `build_rows`
  before anything else.
- **Runtime:** this is `exp118 --full` ≈ **3.3 s measured** (47 arms × 3 seeds,
  2.64 s sim). Honest note: this gate guards harness drift only — it is a
  re-derivation on the SAME corpus the mapping was fit on and must never be
  quoted as independent confirmation of the mapping (see §4, risk 5).

---

## TARGET 1 — Metformin: the recorded dose axis (biphasic)

### 1a. The published claim

**Zhao Z, Yin D, Yang K, Zhang C, Song L, Xu Z (2025)**, *Transcriptome
Sequencing Analysis of the Effects of Metformin on the Regeneration of
Planarian Dugesia japonica*, **Genes** 16(4):365. **PMID 40282325**, PMCID
PMC12026922, DOI 10.3390/genes16040365. Shandong University of Technology,
Zibo (affiliation verified via Crossref). Species **Dugesia japonica**.

- **10-point metformin concentration series**, amputation → **eyespot
  regeneration time in hours**, **n = 30 planarians per treatment**.
- Water control **76.57 h**; the recorded series runs 76.57, 76.25, 75.25,
  75.75, 74.9, 75.27, 74.35, **73.27** (fastest), 75.8, and **81.x h**
  (slowest) — promotion (faster eyespots) at **100 nmol/L, 10 µmol/L,
  1 mmol/L** (1 mM best), maximal inhibition at **40 mmol/L** — a
  **biphasic/hormetic** curve.
- Companion paper (same group): **Yang K et al. (2025)**, *Molecular Mechanism
  of Metformin Regulating the Regeneration of Planarian Dugesia japonica
  Through miR-27b*, **IJMS** 26(15):7092, **PMID 40806224** — dose ladder
  0.01/0.1/1/10 mM (1 mM promotes, 10 mM inhibits), baseline window 48–72 h,
  miR-27b → DjPax6 mechanism; supplies the 10 mM inhibit point.
- Mechanism handle: DjCK1α RNAi epistasis (metformin loses its effect after
  CK1α knockdown) — CK1 is a canonical Wnt-pathway regulator.
- **TO-PIN at scaffold finalization:** the exact per-dose mean ± SD table from
  PMC12026922 Fig. 2 (10 rows, n = 30 each) and the paper's own significance
  tests. The deposit above is the 2-b extraction; the table must be pinned in
  the scaffold constants before T1-G2 is readable.

### 1b. The stack mapping (and its honest limits)

- **Sim arm:** ("wnt", "trunk", 0.5) via `exp91.run_arm_dose` — the
  corruption-AMPLITUDE axis d (theta interpolation toward the adopted full
  push; d = 1.0 bit-exact vs the exp88 arm; d = 0.0 skips the corruption
  write). Rationale: metformin's recorded handle is DjCK1α (Wnt-pathway
  modulator), and exp91's amplitude axis is the adopted dose knob for the
  wnt family. **The mapping is a PROXY**: metformin is an AMPK/metabolic
  intervention, not a theta-identity corruption — the claim under test is
  whether the stack's ONLY dose axis can carry a recorded dose direction,
  not that metformin "is" a Wnt corruption.
- **Concentration → dose coarsening (pre-registered):** water control → d = 0;
  the promote band (100 nM / 10 µM / 1 mM) → d = D_PAR = 0.25 (the adopted
  modulator-class dose); the intermediate/no-effect band → d = 0.5; 10 mM
  (IJMS inhibit) → d = 0.75; 40 mM → d = 1.0. This coarsening deliberately
  collapses the promote-band dip onto one dose — the dip is T1-G2's business,
  not T1-G1's.
- **Readout transform (pre-registered, control-anchored):** f(dose) =
  clamp((t_dose − t_control) / (t_max − t_control), 0, 1). By construction
  control → 0 and 40 mM → 1.0; promote doses clamp to 0 (the transform
  DISCARDS the biphasic dip — deliberate, stated here). **Transform risk is
  flagged in §4 (risk 4).**
- **Decode path:** the exp118 decode (sim rate ≥ 0.5 ↔ abnormal dominant
  class); the hours → fraction transform is the record side, the sim rate the
  prediction side.
- **Coverage honesty:** the 0.619 mapped coverage is about ARM CLASSES; the
  readout TYPE here (hours-to-eyespot) exists nowhere in PlanformDB (the
  corpus readout is the abnormal fraction). The mapping covers arms, not
  readouts — the transform is the bridge and the weakest link.

### 1c. Protocol sketch (exp118 harness)

Reuse `build_rows` (anchor preflight) + `run_arm_dose` directly:
(a) coarse ladder d ∈ {0, 0.25, 0.5, 0.75, 1.0} × 3 seeds on wnt\|trunk —
d = 0.25 and d = 1.0 re-verify the deposited 0.0/1.0 bit-exactly;
(b) fine ladder d ∈ {0.25, 0.30, 0.35, 0.40, 0.45, 0.50} × 7 seeds (exp92's
FL-G1 instrument) on wnt\|trunk for the biphasic-capability probe.
**Estimated runtime:** (15 + 42) seed-runs ≈ 57 × ~19 ms ≈ **1.1 s sim +
~1 s DB load → < 5 s** total (per-seed-run 18.7 ms = exp118's measured
2.64 s / 141).

### 1d. Pre-registered gates (two-sided)

**T1-G1 — the recorded dose DIRECTION transfers at the coarse grain.**
- **Confirm:** Spearman(sim rate, transformed f) ≥ 0.6 across the five mapped
  doses AND the inhibit end lands high (sim rate at d = 1.0 ≥ 0.5 — the
  deposited full-corruption arm says 1.0; the re-run verifies) → the adopted
  amplitude axis carries a RECORDED, non-PlanformDB dose direction in
  D. japonica (first concentration→outcome direction the corpus stack has
  ever been asked to match).
- **Refute:** Spearman < 0.6, or the inhibit end fails to land high while the
  recorded 40 mM fraction ≥ 0.8 → the amplitude axis does not transfer a
  recorded dose direction; exp91's DA-G4 monotonicity is not sufficient for
  transfer.
- **Third outcome:** the sim ladder is degenerate (flat 0.0 or flat 1.0 across
  the mapped doses — Spearman undefined) → all mapped doses sit on one side of
  the sim's threshold (the L74 dose-threshold lesson at a new ladder); deposit
  WHICH side and re-register the coarsening span — this teaches
  concentration→amplitude span calibration, not mapping failure.

**T1-G2 — the biphasic stress-test of the monotone dose-response prediction.**
(The registered prediction: exp29's S2R3 — corruption rises MONOTONICALLY —
confirmed on PlanformDB grains by exp91 DA-G4; the Chinese curve is the first
recorded NON-monotone dose axis.)
- **Refute (of S2R3 as a general law):** the recorded promote-band dip is
  significant BY THE PAPER'S OWN STATISTICS (pinned at finalization: fastest
  promote dose vs control, n = 30/dose) AND the sim's 7-seed fine ladder shows
  NO interior dip (no dose with rate ≥ 2/7 below both neighbors) → hormetic
  dose structure is outside the stack's reachable regime on the 1D sheet;
  S2R3/DA-G4 monotonicity is corpus-grain-specific, not a law. Deposit the
  fine ladder as the slice's measured dose-response.
- **Confirm (a stack capability):** the fine ladder DOES resolve an interior
  dip ≥ 2/7 below both neighbors → the amplitude axis has untested hormetic
  capacity; register the concentration→d rewrite that would encode it (a NEW
  registered experiment — no silent patch).
- **Third outcome:** the recorded dip is NOT significant by the paper's own
  stats → the stress-test is moot at this readout's resolution; deposit the
  power statement (n = 30, per-dose SD) and leave S2R3's standing unchanged.

---

## TARGET 2 — Usp7: the wnt-channel tail arm (+ the timing axis)

### 2a. The published claim

**Usp7 contributes to the tail regeneration of planarians via Islet/Wnt1
axis**, **J Transl Med** (2025). **PMID 39885534**, PMCID PMC11783867, OA.
Henan Normal University, Xinxiang. Species **Dugesia japonica**.

- **Usp7 RNAi → trunk fragments FAIL tail regeneration** — binary penetrance,
  **near-complete** (amplitude ≈ 1.0 on the tail channel).
- **Islet and Wnt1 protein reduced** — WB time-course **R1d / R3d / R7d**
  (regeneration-day 1/3/7 sampling); the wnt1/P-1 dot-like posterior pattern
  is lost; proliferation ↓ / apoptosis ↑.
- **TO-PIN at scaffold finalization:** the exact penetrance percentage from
  PMC11783867 (the 2-b deposit records "near-complete"; the number must be
  pinned in the scaffold constants before T2-G1 is readable).
- **Honest scope note on the timing axis:** R1d/R3d/R7d is an EXPRESSION
  time-course (sampling days), NOT a timed-disruption ladder. There is no
  recorded "disrupt at day k" series to test a deadline against. The timing
  gate below therefore registers (i) the instrument anchor and (ii) an honest
  R-axis deferral (the expression layer is not carried by the 1D sheet) —
  same discipline as 2-b's voltage empty-result.

### 2b. The stack mapping (and its honest limits)

- **Sim arm:** ("wnt", **"tail"**, 0.5) — the Islet/Wnt1 axis is the posterior
  identity channel and the phenotype is tail-regeneration failure, so the
  plane is tail (distinct from the DB's wnt\|trunk partial block the mapping
  was fit on). **Dose by the exp92 class rule, applied mechanically to the
  row's target name:** "usp7" matches neither effector pattern → **modulator
  → d = D_PAR = 0.25**. The deposited modulator-dose arm ('wnt','tail',0.5,0.25)
  → **rate 0.0**; the full arm ('wnt','tail',0.5,1.0) → **1.0**. So the ADOPTED
  mapping's prediction for this row is **wt-like tail regeneration (0.0)**,
  while the record says ≈ 1.0 — the gate below makes this collision explicit
  and decidable rather than hiding it.
- **Decode path:** exp118 decode at the dominant-class grain (sim 0.0 → pred
  wt; recorded ≥ 0.5 → recorded abnormal).
- **Circularity note:** D_PAR was selected on PlanformDB's wnt\|trunk
  modulator block (§4, risk 1–2). The wnt\|TAIL slice at D_PAR was never fit
  (its 0.0 is a deposited corpus arm, not a tuned one), so the target is a
  genuine slice-transfer test — but the constant itself is corpus-derived.

### 2c. Protocol sketch

(a) **Penetrance part — no new sim runs are strictly required:** both arm
rates are deposited; the scaffold re-verifies the two wnt\|tail arms bit-exactly
(6 seed-runs ≈ 0.12 s) + anchor A-G1. The new content is the pinned Chinese
recorded fraction entering the decode comparison.
(b) **Timing part — the instrument anchor:** `exp124.run_deadline` on
grid2d (`exp112.build_battery`), γ = 1 (the exp123-conjunctive anchor), the
exp124 onset grid {0, 6, 12, 18, 24, 36, 48, 72} h × 8 seeds = **64 calls**.
**Estimated runtime:** (a) seconds; (b) **5–15 min extrapolated** — the
compiler substrate is heavier per step than the 1D sheet and exp124's own
256-run sweep has no deposited wall time (flagged as an extrapolation).
(c) **R-axis deferral:** registered as an honest EMPTY (no expression layer on
the 1D sheet; no timed-disruption ladder in the record) — deferred, not failed.

### 2d. Pre-registered gates (two-sided)

**T2-G1 — the class rule transfers to a Chinese-recorded Wnt1-axis row.**
- **Confirm:** pinned recorded penetrance < 0.5 → decode-match with the
  deposited 0.0 arm; the canonical-biology class rule (pre-registered in
  exp92, accepted on PlanformDB at φ = 0.375) transfers out-of-corpus with
  NO refit.
- **Refute:** pinned recorded penetrance ≥ 0.5 (the deposit says ≈ 1.0 — this
  is the expected branch) → decode-mismatch; at ≥ 0.9 the miss is maximal
  (0.0 vs ≥ 0.9). The row is REACHABLE by the arm (d = 1.0 → 1.0 deposited),
  so the lesson is a **dose-CLASS assignment failure**: a functionally-effector
  Wnt1-axis row (Usp7 stabilizes Wnt1 per the paper) that the name-rule files
  as modulator. The L74 closure of the within-class residual as a "record
  property" gains a CHINESE COUNTEREXAMPLE and must be upgraded to a mapping
  defect (a Wnt1/Islet-axis class or a functional reclassification — via a NEW
  registered experiment, never a silent patch).
- **Third outcome:** recorded in [0.5, 0.9) → dominant-class mismatch without
  the maximal-miss lesson; deposit the magnitude and treat as one more
  within-class heterogeneity instance (convergent with T3-G1's third outcome).

**T2-G2 — the timing instrument's anchor + the R-axis deferral.**
- **Confirm:** the γ = 1 deadline curve's edge lands in the deposited grid
  cell (36 h — exp123's anchor, DC-G3) within one onset step → the onset-sweep
  instrument is stable and the R-series has a registered (if deferred)
  encoding target: an early-requirement reading (Wnt1 present at R1d, reduced
  by R3d) maps to "disruption after the deadline spares" semantics.
- **Refute:** the edge moves ≥ 2 grid cells vs 36 h → seed or substrate
  sensitivity in the deposited deadline arc (exp121–124) — a harness alarm,
  diagnose before any timing claim.
- **Third outcome:** no edge inside the grid (P(break) = 1.0 flat — the
  exp122 control-failure mode — or 0.0 flat) → the sweep's operating point is
  wrong on this battery; re-scope the onset grid; the R-axis deferral stands
  either way (it was never contingent on this gate).

---

## TARGET 3 — opa1/drp1: the rescue-epistasis pair

### 3a. The published claim

**Pan X, …, Guo T, Lei K (2024)**, *Mitochondrial dynamics govern whole-body
regeneration through stem cell pluripotency and mitonuclear balance*,
**Nat Commun**. **PMID 39672898**, PMCID PMC11645412, OA. Lei Kai lab, Westlake
University (+ Guo Tiannan). Species **Dugesia japonica**.

- **opa1 RNAi** impairs regeneration; **drp1 co-RNAi RESCUES** — the
  impairment is quantitatively mitigated to control level ("opa1;drp1 RNAi
  animals showed noticeable regeneration, **mirroring egfp;egfp**").
- % readouts in text (proliferation/differentiation indices alongside).
- **TO-PIN at scaffold finalization:** the exact two-arm percentages from
  PMC11645412 (impaired arm and rescued-vs-control arm). The 2-b deposit
  records the amplitude shift qualitatively-quantitatively; the numbers must
  be pinned before T3-G1 is readable.
- This is the validation corpus's FIRST recorded rescue-epistasis pair
  (cut/graft/drug/RNAi arms exist; no recorded reversal).

### 3b. The stack mapping (and its honest limits)

- **Impaired arm:** the adopted family mapping sends mitochondrial-dynamics
  RNAi to the other_rnai **"generic"** family → ("generic", "trunk", 0.5) —
  deposited rate **0.667** (γ × 0.7, commitment_diffusion 1.5). Control arm
  ("cutting", "trunk", 0.5) → **0.0**.
- **Rescue arm — NO registered mapping exists.** The pre-registered candidate
  knob is the **commitment-kwargs channel** (exp40's (cns, diff) grid; the
  L70/L74 machinery), the only adopted mechanism that demonstrably moves
  verdicts on an unsaturated slice (FL-G4: 0.0 → 0.667). Rescue arm =
  ("generic", "trunk") + the kwargs grid. **Honesty:** the grid's DIRECTION on
  the generic arm is unknown (on wnt\|crosspiece it moves verdicts UP toward
  abnormal; rescue would need DOWN) — the two-sided gate below is genuinely
  open, and drp1-rescue semantics would be a claim ABOUT the kwargs channel,
  not an established one.
- **Decode path:** the Chinese row is other_rnai|generic by family → the C3
  decode applies: decoded = max(0, raw − GEN_BIAS = 0.321). **GEN_BIAS is a
  PlanformDB decode constant (exp83, L64)** — applying it to a Chinese row
  assumes the same decoding discipline (§4, risk 3).
- **Coverage honesty:** rescue-epistasis is a TWO-row structure (impaired,
  rescued) that the single-arm mapping was never built to score; the gates
  score the arms separately and the PAIR as the delta.

### 3c. Protocol sketch (exp118 harness)

(a) re-verify ('generic','trunk') and ('cutting','trunk') bit-exactly
(6 seed-runs ≈ 0.12 s); (b) the kwargs sweep on the generic arm: the exp40
grid (CNS_GRID × DIFF_GRID = 30 cells) × 3 seeds = **90 seed-runs ≈ 1.7 s**.
**Estimated runtime: < 10 s** including the DB load.

### 3d. Pre-registered gates (two-sided)

**T3-G1 — the impaired arm lands (family transfer + severity).**
- **Confirm:** pinned decoded impairment (raw − 0.321, clamped) within ±0.25
  of the deposited 0.667 (re-verified bit-exact) AND the raw impairment
  separates from the control arm by ≥ 0.25 → the one-knob generic-family
  mapping transfers to a Chinese metabolic-dynamics RNAi row.
- **Refute:** |decoded − 0.667| > 0.25 with the raw impairment still ≥ 0.25
  above control → the generic family's severity is not one-knob; a SEVERITY
  dimension beyond the family map is demanded (the second Chinese instance of
  the within-class lesson, convergent with T2-G1).
- **Third outcome:** the recorded impairment shows no separation from control
  (raw ≈ control) → the mapping's PREMISE fails on this row: either the
  paper's % readout is a different metric than the corpus abnormal fraction,
  or the phenotype is regeneration TIMING rather than completion — deposit as
  a readout-mismatch (a decode-discipline issue, the L74 lesson), NOT as an
  arm error.

**T3-G2 — the rescue exists in the stack (the kwargs channel as drp1).**
- **Confirm:** some (cns, diff) cell drops the generic arm's rate ≥ 0.3 below
  0.667 (i.e., ≤ 0.367) toward the 0.0 control → the stack HAS a candidate
  rescue channel; register "opa1;drp1 ≈ (generic, trunk) at that cell" as a
  concrete, testable mechanism claim (a NEW registered experiment).
- **Refute:** no cell moves the arm down ≥ 0.3 (grid minimum ≥ 0.367) →
  rescue-epistasis is OUTSIDE the adopted machinery; L70's repair claim is
  slice-specific (works on wnt\|crosspiece only) — the model cannot yet encode
  a recorded reversal.
- **Third outcome:** every cell moves the arm UP (≥ 0.667 everywhere) → the
  kwargs channel's polarity on the generic arm is INVERTED vs wnt\|crosspiece
  — a channel-polarity finding (the exp78 lesson: different path, different
  dominant channel); deposit and re-register the rescue direction question.

---

## 4. Circularity-risk assessment (explicit, numbered)

1. **`D_PAR = 0.25` was selected ON PlanformDB** (the fine-ladder dose whose
   wnt\|trunk rate is closest to the DB modulator-block mean 0.105). Testing
   Chinese rows against it is out-of-sample in ROWS only, not in constant
   selection. Any T1/T2 success partially reflects the constant's corpus
   origin. **Mitigation:** the constant is pinned; the gates test TRANSFER,
   never refit.
2. **The effector/modulator class rule was pre-registered from canonical Wnt
   biology but ACCEPTED on PlanformDB data** (FL-G2, φ = 0.375 — accepted
   "as the measured concordance" after missing the 0.4 bar). The Chinese rows
   (T2-G1, T1's CK1α-as-modulator coarsening) are acceptance tests
   out-of-corpus ONLY IF the rule is never re-fit on them. **Mitigation (hard
   commitment): no re-selection of D_PAR, no regex edit, no class revision on
   Chinese data — any revision is a NEW registered experiment with its own
   pre-registered gates.**
3. **`GEN_BIAS = 0.321` is a PlanformDB decode constant** (exp83's control hot
   bias, L64). T3's decode reuses it on a Chinese row; if Chinese controls
   carry a different hot bias, T3-G1's ±0.25 band is mis-centered. **Flagged
   on the target; no mitigation available without a Chinese control-family
   row set (none exists yet — Henan Normal catalog mostly paywalled).**
4. **Target 1's readout transform is OUR choice made on the Chinese numbers
   themselves** (hours → control-anchored fraction; the concentration → dose
   coarsening). This is the most circular element of Target 1: the transform
   determines both the recorded vector and the "significant dip" question.
   **Mitigation:** the formula is fixed in this document BEFORE any sim run,
   and the biphasic question is kept in the paper's own units (hours, the
   paper's own stats) in T1-G2.
5. **The anchor gate (0.290) is a re-derivation on the SAME corpus the mapping
   was fit on.** It guards harness/extraction drift, not mapping validity;
   it must never be quoted as independent confirmation.
6. **The D. japonica slice is the corpus's weakest** (decoded MAE 0.407 /
   decode accuracy 0.560 on 172 scored rows, vs corpus 0.290 / 0.693). All
   three Chinese targets are DJ rows. Judging them against the corpus baseline
   would be rigged to pass; the DJ-slice baseline is the honest reference and
   is deposited in §0.
7. **Coverage 0.619 is arm-class coverage, not readout coverage:** hours-to-
   eyespot (T1) and %-rescue (T3) are readout types PlanformDB does not carry;
   the bridges are pre-registered transforms/mapping choices (risks 3–4) and
   are the honest weak points of the whole exercise.
8. **Net verdict:** the exercise is a genuine out-of-sample TRANSFER test at
   the row level and (for wnt\|tail, the generic arm's kwargs direction) at the
   slice/level of mechanism — with the constant-selection and transform
   circularity above owned up front. The gates are written so that a REFUTE
   is publishable as a mapping defect and a CONFIRM is worth exactly "the
   adopted mapping transferred, unfitted, to Chinese-recorded rows."

## 5. Runtime summary (estimates; the only measured number is exp118's)

| Piece | Runs | Estimate |
|---|---|---|
| A-G1 anchor (exp118 --full re-run) | 47 arms × 3 seeds | **3.3 s (measured)** |
| T1 coarse + fine ladders | 57 seed-runs | < 5 s |
| T2 penetrance re-verify | 6 seed-runs | < 1 s |
| T2 timing anchor (`run_deadline`, γ=1) | 8 onsets × 8 seeds = 64 calls | **5–15 min (extrapolated; no deposited wall for the compiler substrate)** |
| T3 kwargs sweep + re-verify | 96 seed-runs | < 10 s |
| **Total** | | **seconds, except the T2 timing anchor (minutes)** |

## 6. Honesty notes

- The 3 targets and their extracted numbers come from subagent 2-b's deposit
  (`/home/z/my-project/research/papers/chinese_planaria_mining.md`); the
  per-dose/percentage tables marked TO-PIN must be transcribed from the PMCIDs
  at scaffold finalization before the dependent gates are readable.
- `research/chinese_literature.{md,json}` are R-3's access-barrier map and
  verified-source inventory — they contain NO dose numbers; the targets bind
  to the 2-b extraction, and this document says so rather than implying
  otherwise.
- The exp91/exp92 result JSONs are absent from `results/` (2-a rollback
  residue); the L74 reference lives in `results/exp118_corpus_full.json`
  (G5 re-deposit) — the anchor gate binds THERE.
- The exp108–117 compiler arc does not touch the 1D-sheet corpus arms (the
  L98 scope note); the only compiler-side machinery used here is `run_deadline`
  as the timing instrument, flagged as cross-substrate.
- No existing file modified; nothing committed or pushed. The runnable
  artifact is a SCAFFOLD (`experiments/scaffold_chinese_targets.py`) whose
  protocol bodies are `NotImplementedError` stubs; it has NOT been run.
