# Pre-registered gate drafts — CG-P3, CG-P4, H-P2 (Task 5-b)

Subagent: subagent-gate-drafts (Task ID 5-b) · deposit: `research/gate_drafts_cg3_cg4_hp2.md`
Scope: paper only. No experiments run, no experiment scripts created, no existing
file modified. Nothing committed/pushed.

---

## 0. Where the predictions are defined (provenance)

- **All three are defined in `/home/z/my-project/research/papers/2026_mining.md`**
  (subagent 2-a's deposit, Task ID 2-a in worklog.md L296–L310) — *outside the
  repo*. CG-P3 and CG-P4 are §3 bullets ("Coupling response geometry in
  planarian polarity editing", Damon 2026, Zenodo record **18358611**, full PDF
  read); H-P2 is §4's second bullet + experiment sketch + gate (Han et al. 2026,
  "4D single-cell spatial transcriptomics reveals dynamic morphogenetic
  gradients and regenerative domains in planarians" (PRISTA4D), **GigaScience
  10.1093/gigascience/giag064**, MED 42172041, preprint
  10.64898/2026.02.18.706529, atlas db.cngb.org/stomics/prista4d; mined from the
  Europe PMC core-record abstract — full text Cloudflare-blocked, 8-timepoint
  grid UNVERIFIED, flagged by 2-a). H-P2 is ranked **#3** in the deposit's
  ranked top-3 (worklog L308, L111 of the deposit).
- **Queue authority**: worklog Task 3 Stage Summary (L410) and Task 4 Stage
  Summary (L428): "CG-P3/P4 + H-P2 from subagent 2-a's ranked list" are open
  work after exp119 (TAS-P1, REFUTED, L100) and exp120 (CG-P1 REFUTED in
  pre-owned mode / CG-G2 strength-cannot-reopen CONFIRMED, L101).
- **NOT in the repo**: a repo-wide grep for `CG-P3|CG-P4|H-P2` returns nothing;
  `research/NOVEL_PREDICTIONS.md` is the Stage-2 registry (ND-L34-* deposits,
  exp35/49/51) and does not carry these. **This file is therefore the first
  in-repo registration of the three predictions**; the deposit of record for
  their wording remains `research/papers/2026_mining.md`.

Status of the sibling predictions (context): CG-P1 tested by exp120 (the smooth
kernel does not exist on the stack — grid2d/path invulnerable at every onset,
torus a sharp edge; REFUTED in its pre-owned FAIL mode); CG-P2 tested by exp120
(strength-cannot-reopen CONFIRMED, max |d| 0.00). CG-P3/P4 were *not* covered by
exp120's grid (its arms were default/gamma64/mu03 on grid2d/torus/path).

---

## 1. The shared harness contract (what "reuse verbatim" means)

All three drafts map onto the deadline-arc machinery (ledger L100–L105).
Constants and semantics the drafts inherit and must NOT silently change:

- **Protocol skeleton** (`experiments/exp120_kernel_shape.py::run_kernel`,
  `experiments/exp124_deadline_curve.py::run_deadline`): compile `MULTI`
  (exp94: three zones f-spans **0.02–0.12 / 0.30–0.45 / 0.60–0.75**, all at
  −30 mV), `write_spec_layer(target)` over a trunk canon with the BFS-order
  head quarter (`order[:n//4] = HEAD_V`), 24 h clamped window
  (`WINDOW_H=24.0`), release clamps, amputate the zone union, commitment walk
  (0.8·n·0.73 h, 8 steps/cell, inheritance read per cell), settle
  (`SETTLE_H=15.0`), read.
- **The readout**: `BREAK = pattern_error(target) >= ERR_BAR` with
  **ERR_BAR = 6.0 mV** (`experiments/exp94_multizone_scale.py` L85).
  `P(break)` = mean over seeds; **SEEDS = 1..8**; **ONSETS =
  (0, 6, 12, 18, 24, 36, 48, 72) h** from protocol start; edge = first onset
  with P(break) ≥ 0.5 (exp124's definition).
- **The intervention dials**:
  - `block_gap_junctions(scale)` (`cultivation/bioelectric/collective.py`
    L169–173): sets `gap_scale=scale`, `G=G0·scale`, `deg=G.sum(axis=1)` — the
    **dual-channel cut** (V-coupling AND, through `gap_scale`, the
    theta-diffusion term `mu·gap_scale·lap_theta`). exp120's first-pass bug
    (using `gap_scale` alone) is owned in L101 — the blockade goes through
    `block_gap_junctions`.
  - `c.mu = 0.0` — the theta-diffusion cut alone (exp123's `mu_only`;
    CONJUNCTIVE refutation at gamma 1, L104).
  - `c.gamma = g` — the V-pinning gain; **`dt = star_dt(gamma, deg_max) =
    min(0.1, 1.2/(gamma+deg_max))`** (`exp90_two_source_read.py` L79–80)
    computed for the MAX gamma used (the Euler-stability bug owned in L101).
- **The reader/inheritance read** in the walk (run_kernel L172–179): per cell,
  `if phi_spec[i] >= NEURAL_SPEC_MIN (= −35 mV): theta_new = phi_spec[i] +
  N(0, 0.6); elif phi_spec_canon is not None: theta_new = phi_spec_canon[i] +
  N(0, 0.6); else: theta_new = theta[src] + N(0, 0.6)`. This three-way read is
  where H-P2's arms cut.
- **The M37-A coin** (chain side): `neoblast_coin_p` regrow kwarg
  (collective.py L204, L461–472; commit iff `coin_u < p`); **bit-exact at
  None** (FALSIFICATION L1772); record-matched value **0.8**; exp86's covered
  pool at 0.8 = **0.767** vs record **0.799**.
- **Determinism conventions**: serial, `OMP/OPENBLAS/MKL_NUM_THREADS=1`,
  BLAS-pinned; results JSON to `results/<exp>_<name>.json` with a
  `criteria` dict of named booleans (the exp120–124 deposit format).
- **Calibration point**: the exp124 batch = **256 runs** (4 gammas × 8 onsets
  × 8 seeds). Chain-side corpus runs are ~17–18 ms/seed-arm (exp118 full-corpus
  calibration: 47 arms × 3 seeds in 2.6 s) — graph-walk runs are the expensive
  class; run-count ratios below use exp124=256 as the unit.

---

## 2. CG-P3 — bounded plateau + drug convergence = the coin, not the coupling

### 2.1 Exact statement and source

From `research/papers/2026_mining.md` §3 (Damon 2026, Zenodo **18358611**;
record numbers it must meet: plateau **L ≈ 0.75** (Beane 2011), cross-drug
convergence **P ≈ 0.27**, timing closure tc ≈ 20 h / κ ≈ 10 h (Durant 2017),
posterior ≈ 75% two-headed under GJ block (Oviedo 2010)):

> **CG-P3 (bounded plateau + drug convergence = the coin, not the coupling).**
> The stack attributes L<1 and cross-drug convergence (P≈0.27) to pool
> composition (the M37-A coin), NOT to incomplete coupling. Testable
> discrimination: turning the coin OFF but leaving coupling intact should push
> the two-headed fraction toward its L, while varying coupling (gamma sweep) at
> fixed coin should move the ONSET but not the plateau. Two knobs, two curve
> parameters — the stack is falsifiable per axis.

### 2.2 Stack mapping (exact constants/dials)

| Prediction quantity | Stack quantity |
|---|---|
| the per-animal penetrance coin (pool composition) | `neoblast_coin_p` (collective.py regrow kwarg; commit iff `coin_u < p`; bit-exact at None; NB_P = 0.8 the record-matched value) |
| the bounded plateau L / two-headed fraction | the covered-pool abnormal rate (exp86 convention: mean over seeds of abnormal = err ≥ ABN_ERR_MV or head-likeness ≥ ABN_HL, planes head/tail/trunk); the ceiling `L_hat` = the coin-off rung's rate |
| cross-drug convergence (P ≈ 0.27) | the record's GJ-block family arms (Octanol/Heptanol/Hexanol-class, exp70's sustained/delayed/washout schedule classifier) landing in one rate band |
| coupling | `gamma` (V-pinning gain; the exp124 ladder {1, 4, 16, 64}) and the dual-channel cut `block_gap_junctions(0.05)` (the record's GJ-blocker mapping, L103–L104) |
| the onset | chain side: exp70's drug-schedule semantics (delayed vs sustained arms); graph side: exp124's edge D(gamma) — **already deposited**: 48 → 72 → 36 h across gamma {4, 16, 64} |
| abnormality bars | chain side ABN_ERR_MV / ABN_HL (exp27/exp60); graph side ERR_BAR = 6.0 |

The "onset moves, plateau doesn't" half is **pre-owned by exp124** (deposited
curves: the edge moves ≥ 12 h per rung while the plateau levels stay saturated
0.0/1.0 at 8 seeds). exp126's genuinely new content is the coin axis and the
convergence-survival test; the gamma-onset half enters as the anchor + citation.

### 2.3 Protocol sketch (proposed `experiments/exp126_plateau_coin.py` → `results/exp126_plateau_coin.json`)

- **Panel A — coin ladder (chain, corpus machinery verbatim)**: exp86's
  `run_arm86` semantics — `make_collective(seed)`, 24 h run, neoblast protocol
  (`neoblast_depleted=0.0`), M33 read kwargs (`phi_readout=0.75`,
  `spec_min=NEURAL_SPEC_MIN`, `spec_read_bypass_gap=True`), planes
  head/tail/trunk, fresh-seed convention (exp86's FRESH_SEEDS style; 12 seeds
  per rung). Coin rungs p ∈ {0.0, 0.4, 0.8, None}. 4 rungs × 3 planes × 12
  seeds = **144 chain runs** (seconds).
- **Panel B — coupling at fixed coin (chain)**: `gamma ∈ {0.7×, 1×, 4×}` at
  p = 0.8 (the 1× arm shared with Panel A's 0.8 rung), 3 planes × 12 seeds =
  **72 new chain runs**.
- **Panel C — convergence survival (chain)**: the record's GJ-block family
  arms at exp70's sustained schedule semantics × coin {0.8, None} × 3 planes ×
  12 seeds = **216 chain runs**.
- **Panel D — graph anchor arm**: the exp124 torus gamma-16 deadline curve
  re-run in-batch (8 onsets × 8 seeds = **64 graph runs**) as the continuity
  anchor and the pre-owned onset/plateau citation.
- **Estimated runtime**: ~430 chain runs (≈ 8 s at the exp118 rate) + 64 graph
  runs ≈ **0.25× the exp124 batch**. Sequencing: independent of exp125; can run
  any time.

### 2.4 Pre-registered gates

**CG3-G1 (the plateau is coin-carried).** The pool rate is monotone
non-decreasing in p, and the coin-off rung pushes the fraction toward the
ceiling: rate(None) − rate(0.8) ≥ 0.05, with L_hat := rate(None) deposited as
the stack's plateau number to face the record's L ≈ 0.75.
- *REFUTES the prediction if*: rate(None) ≤ rate(0.8) + 0.02 — the coin is not
  the binding constraint; the 0.767-vs-0.799 match was coincidental and the
  M37-A attribution of the bounded fraction fails. *Teaches*: the plateau is
  intrinsic to the commitment dynamics' own absorption (the TAS-P4-style
  saturating-accumulation picture), and the record's L should be re-fitted
  against a coin-free mechanism.
- *Confirms if*: monotone in p with the ≥ 0.05 lift — pool composition carries
  the boundedness, exactly CG-P3's attribution.

**CG3-G2 (coupling moves the onset, not the plateau).** At fixed coin, the
gamma sub-panel's pool rates stay within ±0.10 of the p = 0.8 anchor at every
rung (the plateau is gamma-insensitive on the chain), while the graph side's
deposited D(gamma) edges move ≥ 12 h across rungs (exp124: 48 → 72 → 36).
- *REFUTES the prediction if*: any gamma rung moves the chain pool rate beyond
  ±0.10 — coupling carries part of the bounded fraction and the two-knob
  separation fails. *Teaches*: Damon's L belongs to the coupling geometry; the
  coin's pool match was absorbing variance that actually lives in the V/theta
  dynamics — re-price the plateau on the v2 oracle's axis.
- *Confirms if*: the plateau is gamma-flat while the deposited edges move —
  the two knobs control two different curve parameters, per axis falsifiable
  as mined.

**CG3-G3 (drug convergence survives coin-off).** The GJ-block family's arm
rates land within ±0.15 of each other at coin 0.8 AND stay within ±0.15 at coin
None — convergence is carried by the shared dual-channel mechanism, not by pool
heterogeneity.
- *REFUTES the prediction if*: the arms converge at 0.8 but diverge > 0.15 at
  None — the convergence WAS the coin. *Teaches*: the record's P ≈ 0.27 needs a
  per-drug residual model (mechanistically distinct drugs would NOT converge on
  the stack once the pool is uniform — a discriminating bench prediction
  against Damon's drug-convergence reading).
- *Confirms if*: convergence survives — the mechanism-level convergence claim
  lands on the stack.

**CG3-A1 (harness-continuity anchor).** The in-batch Panel D torus gamma-16
curve reproduces exp124's deposited curve `[0,0,0,0,0,0,0,1]` (edge 72 h)
**bit-exactly** (same harness, seeds 1–8); tolerance 0.125 per onset only if a
float-order drift is owned in the deposit. FAIL = harness drift; all CG-P3
deposits void until re-anchored.

---

## 3. CG-P4 — the kernel onset tracks the v2 oracle

### 3.1 Exact statement and source

From `research/papers/2026_mining.md` §3 (Damon 2026, Zenodo **18358611**):

> **CG-P4 (onset tracks the v2 oracle).** Across substrates, the kernel onset
> parameter uc should order exactly as the v2 boundary term
> (crossing/sqrt(edges), Spearman 0.81) predicts the dial price — i.e., the
> coupling-geometry kernel and the compiler's price oracle are the same object
> measured on different axes. Gate: Spearman(uc, v2-ratio) >= 0.7 over the
> 7-substrate exp93 battery.

### 3.2 Stack mapping (exact constants/dials)

| Prediction quantity | Stack quantity |
|---|---|
| the kernel onset parameter uc | the **deadline edge** per substrate (exp124's definition: first onset with P(break) ≥ 0.5) under `run_deadline` verbatim (mu 0.015 from t=0 → `c.mu = 0.0` at onset; gamma fixed from t=0; `dt = star_dt(gamma, deg_max)`; SEEDS 1–8; ONSETS (0…72)) |
| the v2 boundary term | `crossing/sqrt(edges)` (exp106's `oracle_v2`; reference Spearman 0.811 on the dial-price axis). **Deposited values**: grid2d 4.174, torus 4.8083, random3 7.5118, random6 2.0378, scale_free 8.6209, path 0.603 at n=100 (`exp106…json: path_v2_by_n[0]`). **small_world is NOT deposited** — computed in-run by exp106's formula and deposited as a new number (a pure graph quantity, no sim involved). |
| the 7-substrate battery | exp93's `SUBSTRATES` list verbatim: path, grid2d, torus, random3, random6, scale_free, small_world (`build_battery`/`make_battery` constructors) |
| the standardized operating cell | gamma 16, mu 0.015 (exp124's peak rung; grid2d's own frozen gamma on PRICE_MAP_V2). Pre-registered fallback rungs {4, 64} (the deposited U-flanks) for substrates degenerate at 16 — the rung each substrate needs is itself a deposited price datum |
| the readout bar | ERR_BAR = 6.0; edge = first onset with P(break) ≥ 0.5 |

**Pre-owned complications owned up front**: exp120 REFUTED the smooth kernel's
existence on grid2d/path under the *blockade* protocol (P(break) = 0.0 flat);
exp122 revealed the unblocked default-cell torus control itself fails (10.00,
L103); exp124 made the deadline non-monotone in gamma (the U-shape). Whether
grid2d/path have finite kernels under the *mu-silence* protocol at gamma 16 is
exactly what exp125 (running) determines — **exp127 is sequenced after
exp125** so the finite-kernel substrate set and the analytic mode-rate law are
known before the Spearman is computed.

**Sign, pre-registered**: the stack's mechanism reading says the deadline
SHORTENS with fragility — cheap substrates (path-class, v2 ≈ 0.6–2.0) tolerate
mu through the whole protocol (edge = beyond-protocol, censored high);
expensive substrates (scale_free-class, v2 ≈ 8.6; geometry-like tails) close
early. So the signed prediction is **edge DECREASING in v2**
(Spearman(uc, v2) strongly NEGATIVE). The mined gate wrote the threshold
sign-free; both readings are registered below and the sign itself is a deposit.

### 3.3 Protocol sketch (proposed `experiments/exp127_onset_oracle.py` → `results/exp127_onset_oracle.json`)

- `run_deadline` **verbatim** (exp124) per substrate at the standardized cell
  (gamma 16, mu 0.015); degenerate substrates (flat-0.0 = no finite deadline,
  or flat-1.0 = refuses at every onset) re-run on the fallback rungs {4, 64}
  and the needed rung deposited.
- 7 substrates × 8 onsets × 8 seeds = **448 graph runs** ≈ **1.75× the exp124
  batch** (+ fallback rungs ≤ +112 runs if ≤ 2 substrates degenerate).
- In-run: uc_hat per substrate (edge, censored at "beyond-protocol" = scored
  at 96 h for ranking, deposited as `null` + flag), the v2 ratio for
  small_world computed by exp106's formula, Spearman(uc_hat, v2) with the
  censored treatment stated both ways (censored-at-96 and
  finite-only-subsets).
- **Sequencing**: AFTER exp125 (needs the finite-kernel substrate set; CG4-G3
  consumes exp125's analytic-deadline predictions on grid2d/path).

### 3.4 Pre-registered gates

**CG4-G1 (same-object ordering — the core).** With ≥ 4 substrates carrying
finite kernels: |Spearman(uc_hat, v2)| ≥ 0.7.
- *Confirms* the mined "same object on different axes" claim; the
  mechanism-confirming sign is NEGATIVE (edge decreases with v2, §3.2); a
  strong POSITIVE rho with ≥ 0.7 also passes the mined bar but deposits a
  sign-owned note that the deadline axis runs opposite to the fragility
  reading — reconciled only via exp125's analytic rate law.
- *REFUTES the prediction if*: |rho| < 0.3 — the deadline is NOT the oracle's
  object; it is a protocol transient (the walk-tax family, exp110–111), not a
  coupling-geometry price. *Teaches*: the oracle's domain (it prices the ends,
  exp114) is dial-axis-only; the temporal axis gets its own map, and Damon's
  kernel-onset claim dies at the stack level while the count-level fits stand.
- *Partial zone (0.3 ≤ |rho| < 0.7)*: deposited honestly as PARTIAL —
  consistent with the ends-only pricing; the middle band unordered on both
  axes (the exp114 picture repeated on a new axis — itself a confirm-shaped
  result for the oracle's domain statement, but a refutation of "exactly
  orders").

**CG4-G2 (censoring consistency — the cheap end).** Every substrate with NO
finite kernel at any registered rung must be a v2-cheap member (v2 ≤ 2.1, the
random6/path band): "no deadline" must itself track the oracle (tolerance at
the cheap end = the deadline beyond the protocol — the DC-G2
V_PRICED-emergence reading).
- *REFUTES the prediction if*: an expensive member (v2 ≥ 7) shows no finite
  kernel while a cheap one closes — the ordering inverts at the ends and the
  oracle's domain claim breaks on the temporal axis. *Teaches*: fragility and
  deadline are dissociable; the mandatory-silence column of PRICE_MAP_V2 is
  not the temporal map.

**CG4-G3 (the analytic cross-check, exp125-dependent).** Where exp125's
zero-free-parameter analytic deadline H(gamma, t) (rate mu·lambda +
eps·gamma·lambda/(gamma + g·lambda) per mode, fit once on the torus's four
edges) has PREDICTED edges for grid2d/path, those predicted edges must agree
in RANK with the measured uc_hat on the same substrates (rank agreement, not
value equality — the values are exp125's deposit).
- *REFUTES CG-P4 if*: the analytic and measured orders disagree while CG4-G1
  passes — uc and the homogenization integral would be different objects and
  the "kernel = oracle" reading dies even with a good Spearman. *Teaches*: two
  distinct temporal mechanisms both live; the deadline curve is a
  two-parameter family (pinning-flank + geometry term) and the map needs both.
- *Confirms if*: ranks agree — the empirical ordering and the mechanistic
  integral are one law, and CG-P4 lands fully.

**CG4-A1 (harness-continuity anchor).** The torus arm at the standardized cell
reproduces exp124's deposited gamma-16 curve `[0,0,0,0,0,0,0,1]` (edge 72 h)
**bit-exactly** (same seeds 1–8, same harness); tolerance 0.125 per onset only
if drift is owned. FAIL = void batch (the exp120→123 CS-G3/DC-G3 discipline).

---

## 4. H-P2 — Med8/ARZ depletion phenocopied by the M33 anterior-read knockout

### 4.1 Exact statement and source

From `research/papers/2026_mining.md` §4 (Han et al. 2026, PRISTA4D,
GigaScience **10.1093/gigascience/giag064**, MED 42172041; preprint
10.64898/2026.02.18.706529; abstract-level mining — flagged):

> **H-P2 (Med8 depletion = M33 read knockout → anterior-specific blastema
> failure).** Remove the stack's anterior read source (M33 gate off, canon
> source stripped) and run head vs tail vs trunk cuts. Prediction:
> anterior-pole rebuild fails (head-side zone error > the 6.0 mV abnormality
> bar; blastema/rebuild rate collapses) while posterior identity and
> trunk-side decisions degrade less — polarity establishment specifically
> lost, matching ARZ's anterior-restricted regulatory role. The inverse
> direction is already measured (the read UPGRADE fixed head fragility
> 0.70→0.00, exp86), which makes the knockout arm a clean, pre-owned
> prediction.
>
> Sketch/gate (mined): ~5 lines — grid2d(10,10), DEFAULT operating point, 3
> arm pairs (intact read / M33-off / canon-stripped), cut planes head/tail,
> 12 seeds each; readout = per-pole rebuild error and blastema-cell count.
> PASS = anterior rebuild error ≥ 2× posterior under M33-off AND head-cut
> abnormality rate > 0.5 while the intact read arm stays ≤ 0.29 mV-class
> errors. FAIL if knockout is polarity-symmetric (then ARZ maps to the whole
> wound-domain M35 readout instead, and the registered M35 test inherits this
> gate).

### 4.2 Stack mapping (exact constants/dials)

| Prediction quantity | Stack quantity |
|---|---|
| the anterior regenerative zone (ARZ) | the anterior read source in the regen walk: `phi_spec_canon` (installed by `write_spec_layer`, collective.py L139–147) — the walk's non-junctional fallback read `elif canon_src is not None: theta_new = canon_src[i] + N(0, 0.6)` (run_kernel L172–179) |
| the M33 anterior gating line | `NEURAL_SPEC_MIN = −35 mV` (collective.py; the read fires only above the neural line) and the regrow-side knobs `spec_min` / `spec_read_bypass_gap` / `phi_readout` (L204–207, L543–549) |
| Med8 depletion (the knockout) | **canon-stripped arm**: `phi_spec_canon` removed after `write_spec_layer` (the walk falls through to `theta[src]` — junction-carried inheritance only); chain-side equivalent: the M33 read kwargs omitted (exp86's `baseline_coin_off` arm, head 0.70) |
| the gating-axis control | **gate-open arm**: `spec_min` ignored (the phi_spec read fires below the neural line too; canon intact) — the exp66 plane-mis-map domain, separating knockout from gating |
| anterior vs posterior | MULTI's z0 (f 0.02–0.12, the BFS-ordered anterior span; the head quarter carries HEAD_V) vs z2 (f 0.60–0.75); per-zone pattern error at the final read |
| the 6.0 mV abnormality bar | **ERR_BAR = 6.0** (exp94 L85); per-zone BREAK = zone error ≥ 6.0 |
| blastema/rebuild rate | the committed fraction in the regen region at the read (cells with `phi_spec ≥ NEURAL_SPEC_MIN`) — the walk's commitment count |
| the pre-measured inverse | exp86 (L68): `baseline_coin_off` head **0.70** → `m33_read_coin_off` head **0.00**; gap panel no_read 1.0 / blend_plus_pole 0.0 |
| harness | exp120's `run_kernel` verbatim with the blockade NEVER applied (onset beyond protocol = the harness's own vacuous semantics, exp120 L86–87); substrates grid2d(10,10) + torus(10,10) via `build_battery`; gamma 1, mu 0.015 (the DEFAULT operating point); `dt = star_dt(1.0, deg_max)` |

### 4.3 Protocol sketch (proposed `experiments/exp128_anterior_read_knockout.py` → `results/exp128_anterior_read_knockout.json`)

- **Main grid**: 3 read arms (intact / canon-stripped / gate-open) × 2
  substrates (grid2d, torus) × **12 seeds** (the mined sketch's 12; the
  deadline arc's 8-seed convention noted — 12 wins, per the deposit) = **72
  unblocked runs**.
- **Readout per run**: per-zone mean error and per-zone BREAK (z0 = anterior,
  z2 = posterior), overall pattern error, committed-fraction count.
- **Bridge anchor arm**: intact read + full blockade (`block_gap_junctions(0.05)`)
  at onset 0, 8 seeds × 2 substrates = **16 runs** — must reproduce exp120's
  deposited early-onset zeros (the A1 anchor).
- **Cut-plane variant (optional, grid2d)**: anterior-span amputation (z0+z1)
  vs the standard full union, 3 arms × 12 seeds = **72 runs** — the mined
  sketch's head/tail plane axis; run only if the main grid's asymmetry needs
  the plane axis to resolve.
- **Optional chain-side re-anchor** (cheap, seconds): exp86 Panel A at 10
  seeds (60 chain runs) — the inverse-direction deposit re-verified in-batch.
- **Estimated runtime**: ~90–160 graph runs ≈ **0.35–0.6× the exp124 batch**
  (+ seconds for the optional chain panel). Sequencing: **independent of
  exp125**; may run before exp127.

### 4.4 Pre-registered gates

**HP2-G1 (the polarity asymmetry — the core claim).** Under the canon-stripped
arm: anterior-zone mean error ≥ 2× posterior-zone mean error AND the
anterior-zone BREAK rate (err ≥ 6.0) ≥ 0.5 across seeds, on ≥ 1 of 2
substrates.
- *Confirms*: the ARZ's anterior-restricted regulatory role is carried by the
  stack's canon read — the Med8-depletion phenocopy lands, wiring PRISTA4D
  (MED42172041) to the reader decomposition and feeding the registered M35
  wound-domain readout test.
- *REFUTES the prediction if*: the failure is polarity-symmetric (anterior
  within 2× of posterior) — the mined FAIL note applies: the ARZ maps to the
  WHOLE wound-domain read instead, and the registered M35 test inherits this
  gate. *Teaches*: the reader's knockout lesion is a general rebuild failure
  (a competence lesion), not a polarity lesion — Med8's role would be read
  competence, not anterior identity.

**HP2-G2 (reader-side, not pattern-side — the reader-swap logic).** The INTACT
arm verifies on the same deposited pattern (P(break) = 0.0 on grid2d,
exp120-consistent flat behavior on torus) while the canon-stripped arm fails
anteriorly — same pattern, reader swapped.
- *REFUTES in two informative directions*: (a) the intact arm ALSO fails →
  the knockout procedure corrupted the pattern (instrumentation; void run,
  fix and re-run); (b) the stripped arm does NOT fail anywhere → the
  junction-carried `theta[src]` inheritance alone suffices on graph
  substrates — a REAL result that localizes the M33 anterior read's necessity
  to the 1D-sheet corpus protocol (exp86's chain): the ARZ phenocopy is
  chain-specific, not graph-universal. *Teaches*: whether the canon source is
  redundancy or necessity per substrate class — the third reader decomposition
  datum after exp79 (head at zero junctions) and exp90 (two-source read).

**HP2-G3 (the gating axis is a different lesion).** The gate-open arm
(`spec_min` ignored, canon intact) does NOT reproduce the anterior failure —
its failure mode, if any, is posterior contamination (the exp66 mis-map
direction).
- *REFUTES the prediction if*: gate-open phenocopies canon-stripped
  (anterior-zone failure) — the knockout and the gating are one mechanism on
  this harness. *Teaches*: collapse the reader decomposition to a single
  anterior source for graph substrates; the M33 gate's domain discipline
  (TC-G5) would then be a chain-protocol property only.
- *Confirms if*: separable — the two reader axes (source removal vs domain
  removal) are distinct lesions, and H-P2's specificity claim survives its
  strongest internal control.

**HP2-A1 (harness-continuity anchor).** The bridge arm (intact read, full
blockade at onset 0) reproduces exp120's deposited curves **bit-exactly** at
seeds 1–8: torus P(break) = 0.0 at onsets {0, 36} (the deposited
`[0,0,0,0,0,0,1,1]` curve's first and sixth entries) and grid2d 0.0 flat (the
deposited `[0]*8`). Tolerance 0.125 per onset only if float-order drift is
owned. Optional chain anchor: exp86's head 0.70 / 0.00 inverse pair within
±0.1 at 10 seeds. FAIL = void batch.

---

## 5. Experiment-number reservation requests (PROPOSED — no files created)

Next free numbers: **exp125** is the main agent's currently-running registration
(L105: the U-shape generalization + the zero-free-parameter analytic deadline
test). The reservations below request **exp126–exp128**:

| # | Name (proposed) | Prediction | Script / result paths (proposed) | Runtime vs exp124 (256 runs) | Sequencing |
|---|---|---|---|---|---|
| **exp126** | THE PLATEAU SPLIT (coin-vs-coupling) | CG-P3 | `experiments/exp126_plateau_coin.py` → `results/exp126_plateau_coin.json` | ~0.25× (64 graph runs) + ~430 chain runs (seconds) | independent; any time |
| **exp127** | THE ORACLE-ONSET ORDER TEST | CG-P4 | `experiments/exp127_onset_oracle.py` → `results/exp127_onset_oracle.json` | ~1.75× (448 graph runs, + ≤ 112 fallback) | **after exp125** (finite-kernel set + analytic cross-check) |
| **exp128** | THE ANTERIOR-READ KNOCKOUT | H-P2 | `experiments/exp128_anterior_read_knockout.py` → `results/exp128_anterior_read_knockout.json` | ~0.35–0.6× (90–160 graph runs) | independent; may precede exp127 |

If the main agent's exp125 lands before exp126/exp128 are picked up, the
recommended order is exp128 → exp126 → exp127 (H-P2 is the ranked-#3
prediction, fully independent, cheapest decisive; exp127 consumes exp125's
outputs).

## 6. Gate count summary

| Prediction | Decision gates (two-sided) | Continuity anchor | Total |
|---|---|---|---|
| CG-P3 (exp126) | CG3-G1, CG3-G2, CG3-G3 | CG3-A1 | 4 |
| CG-P4 (exp127) | CG4-G1, CG4-G2, CG4-G3 | CG4-A1 | 4 |
| H-P2 (exp128) | HP2-G1, HP2-G2, HP2-G3 | HP2-A1 | 4 |
| **Total** | **9** | **3** | **12** |
