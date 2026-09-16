# 101% PATH DESIGNS — the three targets, as registration-ready sketches

> Subagent 5-e (Task ID 5-e, agent `subagent-101path`). Design deposit only:
> NO experiments run, NO existing file modified, NO code created. Everything
> below reuses deposited machinery and is written so the next session can
> lift each section into a pre-registered `experiments/exp12*.py` after
> exp125 (the registered U-shape generalization) has run — exp129's SU-G2
> consumes exp125's output directly.
>
> The three 101% targets, restated as one-line theses:
>
> 1. **Stage 3 / v6 — the INVENTOR**: v4 generates *requested* novel
>    anatomies (exp81), v5 connects the reader (exp87); v6 must
>    *self-initiate* — propose, price, execute, verify, and register
>    anatomies no request asked for, where "novel" is decidable against the
>    repo's own corpora, not rhetorical (Section 1).
> 2. **Stage 4 — the cone expands ITSELF**: the k-dial reached 5→24 cells
>    (exp62) and its rule transfers (exp72); 101% is a cone whose own
>    measured reach sets the next cycle's reach (autocatalytic), stated in
>    cross-organism terms, and non-collapsing under the mu-silence deadline
>    via the M33 non-junctional read (Section 2).
> 3. **Stage 5 — break the coherence constraint**: exp68 showed the
>    boundary robust across 5 formalizations; exp124's deadline arc says
>    optimal pinning is INTERMEDIATE. Designs for two of the three paths:
>    (1) the universal reader (M33 extended to any medium — Section 3.2),
>    (2) a substrate coherent with ANY pattern (Section 3.3). Path 3
>    (CLOSED / re-formalization) is deliberately not designed here — it is
>    the fallback if both fail, and its shape depends on which gate fails.

Shared machinery referenced throughout (all deposited, all importable):

- `cultivation/compiler/anatomy.py` — `AnatomySpec`/`Zone`,
  `compile_anatomy`, `execute_and_verify`, `recut_stability`,
  `substrate_partition_check` (R5 + the L84 oracle annotation),
  repertoire `[-60, -15]` mV, `WINDOW_H=24`.
- v4/v5 logic: `experiments/exp81_compiler_v4.py`
  (`generate_specs`, `spec_class`, `admissible_v4` — the calibrated
  envelope: min zone width, min adjacent contrast; values as deposited),
  `experiments/exp87_compiler_v5.py` (`STAR_GAMMA=64.0`, `STAR_MU=0.0`,
  `star_dt`, `execute_v5`, `graph_multiregion`).
- The 19-substrate battery: `experiments/exp112_walk_speed_ladder.py ::
  build_battery()` (path, path200, cycle, small_world, star, torus,
  torus_elong, random3, random8, scale_free, scale_free200, tree, grid2d,
  grid_elong, ladder, random6, barbell, bipartite, complete).
- M33 non-junctional readout: `cultivation/bioelectric/collective.py ::
  NEURAL_SPEC_MIN = -35.0`, plus `write_spec_layer`,
  `spec_read_bypass_gap`, `ARZ_LINEAGES=3`, `ARZ_WIDTH=2`.
- Deadline harness: `experiments/exp124_deadline_curve.py :: run_deadline`
  (gamma fixed from t=0, mu 0.015 until `onset`, then 0; returns BREAK)
  and the deposited U-shape D(gamma) (gamma 1 never rescues, 4→48 h,
  16→72 h latest, 64 collapses to 36 h).
- Light-cone instruments: `cultivation/cognitive/lightcone.py`
  (`measure_lightcone`, `regen_lightcone`, `regen_pulse_timing`).
- Deposited continuity anchors named per section under "Anchors".

---

## SECTION 1 — Stage 3 101%: compiler v6, the generator that INVENTS

### 1.1 What is deposited (the floor v6 stands on)

- **v4 (exp81, L62, 5/5)**: 40 generated multi-zone anatomies all compile
  zero-search; R5-alone precision 15% = the finding (generator space ≫
  dynamic envelope); calibrated envelope reaches 100% test precision at
  ~40% coverage; 3 structural novel classes verified
  (`multi-zone-3/4+island`, `two-zone-island`); 100-gen hold stability;
  the operating-point escape (the two-channel law wired in as an
  audit-ready precondition). Trigger specs CANNOT regenerate novel zones —
  v4 compiles write-only; the regen-walk limitation is owned.
- **v5 (exp87, L69, 5/5)**: the reader connected — `write_spec_layer` +
  the exp79 reader weight + the M33 gate + the star operating point as
  R7' (zone errors 6–16 → 0.29 mV); domain rule R7 verified end to end;
  multi-region composition 10/10; graph reader 5/5.
- **The price context**: reader price map 19 substrates × 12 zone counts,
  zero refusals somewhere (exp100/101/103, L82-L85); PRICE_MAP_V2
  (docs/PRICE_MAP_V2.md, exp117/L98, corrected L105) — the oracle prices
  the ends, the dials pay the middle, the geometry pair untouchable; the
  deadline curve D(gamma) (exp124/L105) prices the temporal dimension.

**What v4/v5 cannot do**: generate anything. `generate_specs` is a fixed
uniform sampler; every anatomy in every deposited run was either requested
by the experimenter or drawn blind. "Self-initiates invention" is exactly
the missing act: the system must propose its own targets, price them
against the deposited map, execute, verify, and feed the result back as
prior — with no human request anywhere in the loop.

### 1.2 The design (registration sketch: `exp126_compiler_v6_inventor`)

A closed proposal→price→execute→verify→register loop, run for B batches
(B = 6) of P proposals each (P = 10), 60 inventions total:

1. **PROPOSE** (self-initiation): a proposal distribution q over
   `AnatomySpec` space — zone count 1–6, boundary placement, voltages in
   the repertoire, plane ∈ {None, tail, head, trunk}, latch on. The ONLY
   constraint at proposal time is admissibility-shaped (the v4 envelope's
   feature ranges, so proposals are not trivially malformed). **The
   corpus library enters nowhere in this step.** q starts at the exp81
   uniform and is updated BETWEEN batches by the loop's own outcomes
   (logistic weight on boundary-count, zone-width, and contrast features
   of verified inventions — a 3-parameter update, no learning framework).
2. **PRICE** (the deposited map is the cost model): each proposal is
   priced by (i) the L84/L95 oracle (boundary-to-volume names the ends),
   (ii) the PRICE_MAP_V2 class table (the dials that pay the middle),
   (iii) the exp124 deadline curve at the priced gamma (the cell's
   deadline must clear `WINDOW_H + walk + settle`). Output: the cell
   (gamma, mu) and a predicted-verify bit.
3. **EXECUTE + VERIFY**: `execute_v5`-style write (`write_spec_layer` +
   reader weight + M33 gate + star operating point where priced) on the
   chain (n=100, 3 seeds), identity read vs `spec_target` at the 6.0 bar;
   survivors get `recut_stability`.
4. **REGISTER** (novelty scoring, Section 1.3): each executed spec is
   scored NOV(spec) against the frozen reference library; the
   (spec, NOV, price, verify) record is appended and q is updated.
5. **HOLD**: the 6 highest-NOV verified inventions go to the 100-gen
   latching hold and the re-cut re-reachability arm (the exp90 two-source
   reader regen — the only path that can re-derive a novel zone).

The self-initiation discipline (what makes this v6 and not v4-again): no
requested spec exists anywhere in the run; the loop's only external
inputs are the frozen price artifacts and the frozen novelty library;
q's update is driven solely by the loop's own verify/novelty outcomes.

### 1.3 "Invents what evolution never made" — the decidable novelty metric

**NOV(spec)** — a boolean printed by a function, with every reference
object taken from the repo's own deposits:

- **Representation**: map spec to (a) a fate profile f ∈ R^100 via
  `spec_target` (exp87's instrument — the piecewise-constant voltage
  profile on the canonical axis at n=100), and (b) a boundary signature
  B = sorted cut points in [0,1].
- **Reference library R** (the "what was ever made" set, frozen at
  registration):
  1. **PlanformDB morphology vocabulary**: all 372 `Morphology` rows of
     `data/planform/planformDB_2.5.0.edb` (Wild type id 1 … ectopic
     brains, hypercephalized, etc.), each mapped to a canonical AP fate
     profile by a pre-registered region→repertoire-voltage table
     (head/eye/pharynx/trunk/tail identities → the WT band voltages;
     morphologies not expressible on the AP axis — cyclop, lateral
     heads — enter as structural labels: their boundary count and
     edge-touch pattern only). This is the vocabulary evolution +
     120 years of experimentation ever produced in this system.
  2. **The corpus sim arms**: the 47 unique arms of exp118 (L99) — what
     the record's interventions actually produce.
  3. **The battery's verified set**: every (substrate-class, zone-count)
     pair verified in exp100/exp101/exp103/exp112/exp113 deposits
     (19 × 12) — what the program has ever made writable.
  4. **The compiler's own history**: every spec in every
     `results/exp4*.json`–`exp12*.json` spec registry — everything the
     program itself has ever compiled, including exp81's 3 novel classes.
- **Distance**: D(spec, r) = zone-structure edit distance (symmetric
  difference of boundary sets, normalized by max zone count) as the
  primary key, fate-profile RMS in mV at n=100 as the secondary key
  (lexicographic — structure dominates voltage, matching how the corpus
  itself distinguishes outcomes).
- **Novelty verdict**: spec is INVENTED-NOVEL iff
  - (i) D(spec, R) > N*, where **N* = the 95th percentile of
    nearest-neighbour distances WITHIN R** (the library's own internal
    spread — a threshold the corpus defines, not us);
  - (ii) **anti-recombination clause**: B is not the union of two library
    boundary sets with f the corresponding splice (a two-headed + island
    franken-splice of recorded morphologies is recombination, not
    invention);
  - (iii) the (spec_class, substrate-class) pair is absent from the
    verified-set reference (3).
- The metric's honesty properties: computable in milliseconds from
  deposited artifacts; symmetric (the library is scored against itself to
  set N*); and it makes "evolution never made it" falsifiable — a
  reviewer can rerun the scorer and get the same boolean.

### 1.4 Pre-registered gates (two-sided; third outcome named)

- **IV-G1 SELF-INITIATION** (does the loop invent, or just sample?):
  - *REFUTES v6*: with the novelty filter disabled INSIDE the loop, the
    successive-batch median NOV of accepted proposals does not rise
    (Spearman vs batch index ≤ 0.2, or median NOV ≤ N*/2) — the "inventor"
    is blind sampling wearing a post-hoc filter; self-initiation dies.
  - *CONFIRMS*: batch-median NOV rises AND q's shift from the exp81
    uniform is nonzero in the novelty direction (measured on
    boundary-count / width / contrast marginals), with the library
    absent from proposal time by construction.
  - *THIRD (named)*: **SPECIOUS INVENTION** — NOV rises but only along
    directions the executor cannot express (high-NOV proposals fail
    admissibility/verify wholesale); invention is real but empty; v6's
    claim downgrades to propose-not-execute and the registered repair is
    a priced proposal step (the loop must learn the price map, not just
    the novelty gradient).
- **IV-G2 EXECUTABLE INVENTION** (is the pricing load-bearing?):
  - *REFUTES*: the loop's verify rate at the priced cell ≤ exp81's
    blind-generator calibrated precision at matched admissible coverage
    — the inventor is no better than the sampler it replaced.
  - *CONFIRMS*: verify rate ≥ 2× blind at matched novelty depth, AND the
    predicted cell (oracle class + deadline-cleared gamma) is the
    verifying cell for ≥ 80% of verified inventions — the price map
    survives contact with inventiveness, not just with requests.
  - *THIRD (named)*: **STAR-ONLY** — every invention verifies only at
    (gamma=64, mu=0): the universal operating point does all the work,
    the per-spec pricing is inert; the claim degrades to "inventions are
    writable somewhere" (already v4's result) and priced self-initiated
    invention FAILS.
- **IV-G3 HERITABILITY** (do inventions persist as forms?):
  - *REFUTES*: invented forms are write-only ghosts — 100-gen hold fails
    or the first re-cut reverts the regen to WT on every substrate class
    (the exp81 write-only limitation extends to everything v6 makes).
  - *CONFIRMS*: ≥ 3 invented classes pass BOTH the 100-gen latching hold
    AND re-cut re-reachability through the two-source reader (exp90
    machinery) within the 6.0 bar — invented forms are inherited forms.
  - *THIRD (named)*: **LATCH-ONLY** — holds 100-gen but re-cut
    re-reachability succeeds only on a subset of substrate classes (map
    which: prediction from the reader's domain — DEFAULT0/MU0 yes,
    GEOMETRY pair no); the form is stable but its regenerability is
    class-bound, deposited as the invented-forms price map.

### 1.5 Runtime estimate + continuity anchors

- **Runtime**: ~2–3 h serial on the 2-core sandbox (BLAS pinned): 60
  inventions × 3 seeds × (window + walk + settle ≈ 0.5–1 k vectorized
  steps at n=100, ~10–40 ms/run) ≈ 30–60 min; + 6 × 100-gen holds
  (~1–1.5 h); + novelty scoring negligible (frozen artifacts, in-memory).
- **Anchors**: `results/exp81_compiler_v4.json` (envelope calibration,
  novel classes, spec registry), `results/exp87_compiler_v5.json`
  (R7'/star point, reader), `results/exp100_reader_price_map.json`,
  `results/exp112_walk_speed_ladder.json`,
  `results/exp113_repriced_map.json` (battery + price classes),
  `results/exp124_deadline_curve.json` (temporal pricing),
  `results/exp118_corpus_full.json` (47-arm corpus), the PlanformDB
  `Morphology` table (372 rows), and the L62/L69/L84/L94/L105 ledger
  entries. Anchor-check vs the outside literature (one pass, done at
  design time): the "anatomical compiler / target morphology" framing is
  Levin-lab's own vocabulary, and recorded ectopic structures (e.g.
  spontaneous ectopic head formation, Tratkiewicz et al. 2025 bioRxiv)
  are all *within* the PlanformDB vocabulary — i.e. the library really is
  "what has ever been made", so NOV > N* is a strong claim, as intended.

---

## SECTION 2 — Stage 4 101%: the cone expands ITSELF

### 2.1 What is deposited (the floor)

- **The dial** (exp62, L43, target exceeded): coupling-kernel radius k
  takes the pulse light-cone horizon 5→10→16→24 cells (4.8×); the
  cross-stage rule: reach is bought with contrast — k=4 breaks the
  third-head verify, envelope k≤2 for fine identity.
- **The rule transfers** (exp72, L53): horizon is a function of
  NEIGHBORHOOD VOLUME, not radius (XT-G3, ρ ≥ 0.9 across
  chain/grid/small-world); the contrast envelope transfers with it.
- **The maintenance price** (exp82, L63): frontier duty is
  tissue-specific (chain k=4 → duty 0.75; small-world free-runs); the
  rule is universal, the envelope is readout-side.
- **The bypass** (exp79/86/90/97, L60/L68/L72/L79): the M33
  non-junctional anterior read (`NEURAL_SPEC_MIN=-35`) +
  `spec_read_bypass_gap` + the two-source frontier walk carries identity
  through ZERO junctions — the reader domain closed 19/19 × 12 with
  NO topological boundary.
- **The temporal map** (exp120–124, L101–L105): the blockade deadline is
  the MU-SILENCE DEADLINE — conjunctive (both channels must be cut,
  exp123), non-monotone in pinning (optimal INTERMEDIATE gamma, exp124),
  substrate-specific (grid2d/path invulnerable, torus a sharp edge,
  exp120-121).

**What is missing for 101%**: the dial is set from OUTSIDE each cycle.
The cone does not feed its own reach back into its own expansion; the
rule was stated cross-tissue but not run cross-ORGANISM (the 19-battery
of graph substrates / the 17-species corpus axis); and the temporal map
was measured on STATIC protocols, not on an expanding one.

### 2.2 The design (registration sketch: `exp127_cone_autocatalysis`)

Three arms, all on existing instruments:

- **A1 — AUTOCATALYTIC EXPANSION** (the self-set dial). Protocol: cycle
  t writes with coupling radius k_t; measure the regen-window cone
  horizon h_t (0.5 mV, 24 h — `regen_lightcone`/`regen_pulse_timing`
  verbatim); set **k_{t+1} = clip(h_t, 1, 8)** — the cone's own measured
  reach IS the next cycle's coupling. Run T=6 cycles × 3 seeds on the
  chain, with the exp82 maintenance schedule paying the frontier duty
  (the contrast envelope is the wall to respect: each cycle must keep
  the third-head-style contrast verifiable or the cycle is a breach).
  Comparator: the best FIXED-k envelope (the k≤2 contrast-preserving
  setting and the k=4 reach setting) — the question is whether ITERATION
  buys what no single setting does.
- **A2 — CROSS-ORGANISM TRANSFER**. The same rule (stated in
  neighborhood-volume terms per XT-G3, zero per-substrate parameters)
  runs on `build_battery()` via `GraphCollective`, with the reader
  (M33 gate + anchor) carrying the anterior span. Two modes per
  substrate: junction-only (the cone expands through coupling) and
  reader-assisted (the M33 read carries the span where the middle band's
  mu-silence binds). Verified horizon = identity holds at the 6.0 bar at
  the cycle's horizon.
- **A3 — BLOCKADE-PROOF EXPANSION**. Run A1's loop under
  `run_deadline`'s conjunctive cut: at the U-shape-optimal intermediate
  gamma (16 on the torus — the deadline peak), blockade lands at onsets
  spanning the deposited edge set {12, 24, 36, 48, 72} h; after washout
  the loop resumes. Readout: P(break) vs the static deadline curve, plus
  the post-washout horizon recovery fraction (does the cone remember its
  own size?).

### 2.3 Pre-registered gates (two-sided; third outcome named)

- **CA-G1 AUTOCATALYSIS**:
  - *REFUTES*: the iterated horizon sequence never exceeds the best
    fixed-k envelope — expansion saturates at cycle 1's reach or dies at
    the contrast envelope; the cone does not feed itself.
  - *CONFIRMS*: horizon_T ≥ 2× horizon_1 with identity verified every
    cycle (duty paid per the exp82 schedule) — iteration buys reach no
    single dial setting can, which is the operational content of "the
    cone expands itself".
  - *THIRD (named)*: **OSCILLATORY EXPANSION** — the horizon alternates
    (an expanded write dilutes contrast → contraction per the envelope →
    re-expansion); the autocatalysis exists only in the time-average;
    deposit the cycle length and its duty cost as the honest form.
- **CA-G2 CROSS-ORGANISM TRANSFER**:
  - *REFUTES*: the rule fails on the whole GAMMA0 band, or refuses on
    the geometry pair (bipartite/complete) even at their priced (32, 0)
    cells — the rule is chain-local and the "cross-organism" claim dies.
  - *CONFIRMS*: ≥ 15/19 substrates show a non-decreasing verified
    horizon under the same zero-parameter rule.
  - *THIRD (named)*: **M33-DEPENDENT TRANSFER** — transfers only with
    the reader-assisted mode (junction-only fails on the MU0 band):
    the cone expands through the non-junctional read, not the junctions.
    This is a different (still publishable) mechanism and must be
    renamed as such, not counted as a pass of the coupling rule.
- **CA-G3 BLOCKADE-PROOF EXPANSION**:
  - *REFUTES*: P(break) under the expanding loop equals the static
    deadline curve at every onset — the loop buys no temporal protection;
    expansion and survival are one dial, and "without collapsing under
    blockade" fails.
  - *CONFIRMS*: at intermediate gamma the loop's identity survives
    onsets where the static protocol breaks (deadline shifted LATER by
    ≥ 1 onset rung) — the iterated commits re-seed identity faster than
    the window's theta-homogenization erodes it (the exp124 mechanism's
    direct prediction).
  - *THIRD (named)*: **RESUME-WITHOUT-MEMORY** — identity survives (the
    M33 anterior read + anchor carries it) but the post-washout horizon
    resets to k=1: the cone survives the blockade yet does not remember
    its own size; deposit the recovery fraction as the cone-memory
    coefficient.

### 2.4 Runtime estimate + continuity anchors

- **Runtime**: ~2–3 h serial: A1 = 6 cycles × 3 seeds × ~1 k-step
  instruments (minutes); A2 = 19 substrates × 2 modes × 6 cycles × 3
  seeds ≈ 680 runs (~30–60 min); A3 = 2 substrates (torus + grid2d
  control) × 5 onsets × 3 seeds with the loop wrapper (~30 min).
- **Anchors**: `results/exp62_signal_range_dial.json`,
  `results/exp72_cross_tissue_dial.json`,
  `results/exp82_maintenance_map.json`,
  `results/exp79_two_channel_law.json`,
  `results/exp86_regen_read.json`, `results/exp90_two_source_read.json`
  (deposited per exp86/exp90 — if absent from results/ due to the known
  rollback incident, the ledger entries L68/L72 are the reference),
  `results/exp120_kernel_shape.json` … `results/exp124_deadline_curve.json`,
  `docs/PRICE_MAP_V2.md` (corrected mu column, L105).

---

## SECTION 3 — Stage 5 101%: breaking the coherence constraint (paths 1 and 2)

### 3.1 The deposited constraint state

- **exp68 (L49)**: the exp43 coherence boundary (R5, b2v ≤ 0.10) does
  NOT move under any of 5 dynamics-matched formalizations (b2v, label
  energy E, mean per-node force, λ₂, conductance) — robustness across
  formalization.
- **The star-search arc (exp73–79, L54–L60)**: remodeling moves the wall
  (rewiring makes torus/random3 writable), the two-channel law crosses
  the star at (gamma=64, mu=0) — coherence is an ARCHITECTURE REQUIREMENT
  (strong identity + non-diffusing anchor + non-junctional read), not a
  wall. The quadrature law: err = sqrt(eV² + eT²), Spearman 0.999 (L66).
- **The reader arc (exp97–106, L79–L88)**: the reader's domain is CLOSED
  and empty of refusals — 19/19 × 12 zone counts × n to 784 verify
  somewhere; the v2 oracle prices the ends (Spearman 0.73/0.63),
  the middle is priced by the mu-silence law (binary in magnitude and
  phase, exp115-116) and walk speed (buys gamma never mu, exp112).
- **The deadline arc (exp120–124, L101–L105)**: the temporal coherence
  constraint — the mu-silence deadline — is conjunctive, substrate-
  specific, and NON-MONOTONE in pinning: optimal pinning is INTERMEDIATE
  (gamma 16 → 72 h latest, gamma 64 collapses). This is the constraint's
  only known non-robust direction: it moves with the dials.

The 101% question, stated precisely: the constraint is robust in FORM
(exp68) but priced in DEGREE (the dial lattice). Breaking it means either
(1) extending the read architecture until the medium stops mattering
(path 1), or (2) covering the whole pattern space at SOME priced cell of
the hardest substrates (path 2) — with exp68's formalization-crossing
test re-run on the reader path as the shared control (SU-G3).

### 3.2 Path 1 — the UNIVERSAL READER (M33 extended to any medium)
Registration sketch: `exp128_universal_reader_domain`

**What is built/tested.** The M33 read is currently anterior-domain:
`spec >= NEURAL_SPEC_MIN (-35)` gates the non-junctional read; posterior
identity has no local pole and stays junction-carried (trunk 9.10 mV
fails at gap 0 — the recorded posterior bias as a theorem, L60). The
extension hypothesis: the missing posterior pole can be SUPPLIED rather
than discovered — two candidate mechanisms, both assembled from deposited
parts, zero new fitted constants:

- **(M-pole) the canon as a movable pole**: the exp90 two-source canon
  source (load-bearing, L72) is generalized to a per-cell pole-candidate:
  where no anterior-grade spec exists, the read falls back to the canon
  source's posterior identity (the archive stands in for the absent
  pole). This is the exp80 external-storage result turned into a read
  path: the form can be re-instantiated from storage; here, per-zone.
- **(M-arz) the M35-A ARZ multi-lineage read as a second non-junctional
  channel**: `ARZ_LINEAGES=3`, `ARZ_WIDTH=2` (deposited constants) — the
  wound-domain lineage read already aggregates K independent reads; test
  whether the lineage mixture carries posterior identity without
  junctions when the junction read is cut.

**Test arms** (the domain map): the 19-battery × posterior planes
(trunk/tail regen after head+trunk amputation) × gap-0 (full junctional
cut, both channels per exp123's semantics) × 3 seeds; identity read at
the 6.0 bar; the adaptive-ladder protocol of exp100 to find each
substrate's minimal reader cell. PLUS the exp124 deadline harness on the
reader arms: 4 gammas × 8 onsets × 3 seeds on torus/grid2d/path.

**Pre-registered gates (two-sided; third outcome named):**

- **UR-G1 THE POSTERIOR DOMAIN OPENS (or the theorem holds)**:
  - *REFUTES the extension*: posterior reads fail at gap 0 on every
    substrate where they fail today (trunk-style 9.10 mV everywhere);
    both candidate mechanisms are inert — the M33 domain is closed as a
    genuine theorem (the anterior asymmetry is constitutive, exactly as
    the literature anchor says), and path 1 is honestly DEAD.
  - *CONFIRMS*: ≥ 12/19 substrate classes read posterior identity at
    gap 0 within the 6.0 bar via at least one candidate mechanism with
    ZERO new fitted parameters.
  - *THIRD (named)*: **CANON-ONLY, NOVEL-EXCLUDED** — the read works for
    canon-conforming (WT-like) posterior zones but fails for novel
    posterior zones (the archive carries only what evolution stored —
    the exp80 resolution for novel forms); path 1 then opens for
    restorative reads only, and the novel-zone posterior read migrates
    to path 2's pattern-coverage framing.
- **UR-G2 THE READER OUTSIDE THE QUADRATURE (the deadline must not
  shrink)**: the exp124 mechanism says the deadline shortens when the
  eps channel opens (high gamma keeps V~θ, accelerating window
  homogenization). If the universal read rides the V/θ channels, it must
  pay the same U-shape.
  - *REFUTES the reader's independence*: the deadline curve under the
    universal read SHORTENS monotonically with reader strength (the read
    accelerates homogenization — it is inside the two-channel system).
  - *CONFIRMS*: the deadline curve under the reader is flat or shifted
    LATER at every gamma, AND the exp84 quadrature decomposition shows
    the reader's contribution is orthogonal to both channels (adding it
    does not change eV or eT at fixed pattern).
  - *THIRD (named)*: **ANTI-U** — the reader removes the U-shape entirely
    (monotone deadline in gamma): this would FALSIFY the exp124 mechanism
    claim (that joint relaxation rate μ·λ + eps·γ·λ/(γ+g·λ) is the
    deadline's carrier) and register a re-analysis, a bigger kill than
    the gate itself — pre-naming it keeps the refutation honest.
- **UR-G3 CLOSURE PARITY (no loss dressed as an upgrade)**:
  - *REFUTES*: the universal reader's domain (substrates × zone counts ×
    planes at gap 0) is strictly SMALLER than the junction-carried
    reader's closed domain (19/19 × 12, L82-L85) — the extension costs
    more than it buys.
  - *CONFIRMS*: domain ≥ the junctional domain (parity or better) with
    the anterior M33 behavior bit-preserved (defaults untouched —
    bit-exactness gate as in every core edit).
  - *THIRD (named)*: **PARITY-WITH-PRICE** — same domain coverage but a
    strictly higher dial price on the middle band (the reader pays what
    mu silence used to); deposit the re-priced map.
- **Wet-lab tie-in (deposited prediction consumed)**: subagent 2-a's
  H-P2 — Med8/ARZ depletion should phenocopy an M33 anterior-read
  knockout. If UR-G1 confirms via the ARZ mechanism, H-P2 becomes the
  bench falsifier: Med8(RNAi) arms should specifically fail ANTERIOR
  reads. Registered as the bridge gate UR-G4 (one arm pair, no new
  machinery).

**Runtime**: ~2–3 h serial (19 × 2 planes × 2 mechanisms × 3 seeds ≈ 230
runs + the deadline sweep 3 substrates × 4 γ × 8 onsets × 3 seeds ≈ 290
runs). **Anchors**: `results/exp79_two_channel_law.json`,
`results/exp86_regen_read.json` (or L68), `results/exp90` (or L72),
`results/exp100_reader_price_map.json`, `results/exp101_zone_count_ladder.json`,
`results/exp103_resolution_ladder.json`, `results/exp123_channel_split.json`,
`results/exp124_deadline_curve.json`, `research/papers/2026_mining.md`
(H-P2), `collective.py` constants.

### 3.3 Path 2 — a SUBSTRATE COHERENT WITH ANY PATTERN
Registration sketch: `exp129_pattern_universal_substrate` (runs after
exp125 — SU-G2 consumes its analytic deadline fit)

**What is built/tested.** The coherence constraint's residual form: every
substrate supports SOME patterns at SOME priced cell, but coverage of the
PATTERN space has never been measured — exp81 measured coverage for blind
specs on the chain, exp100 measured coverage for ONE pattern (the canon)
across substrates. The 101% claim "substrate coherent with any pattern"
is operationalized as **pattern-space coverage at the substrate level**:

- **Pattern sample** (systematic, not random): zone counts {1, 2, 3, 4,
  6, 8} × contrasts {6, 10, 20} mV within the repertoire × island
  structures {none, interior-island, edge-island} × the exp126 invented
  classes (Section 1's deposits, if exp126 ran; else exp81's three
  classes) — ~60 patterns, each an `AnatomySpec` with the v4 envelope
  pre-checked so refusals mean physics, not malformation.
- **Substrates**: the three hardest members of the battery —
  **bipartite, complete** (the geometry pair: no dial ever touched them,
  L93), and **scale_free** (the degree-sequence wall, exp73-76). A
  substrate's claim to "coherent with any pattern" is made or broken
  exactly there; the other 16 members' coverage is assembled from
  existing deposits where possible.
- **Dial lattice per (substrate, pattern)**: the full deposited stack —
  the star point (64, 0), the deadline-optimal intermediate gamma
  (exp124's U-shape, at mu 0 and mu 0.015), the slow-anchor
  configuration (exp76), conductance thinning (exp77), walk_speed=0
  (exp112). Six cells, 3 seeds: coverage(S) = fraction of patterns
  verifying at ≥ 1 cell.

**Pre-registered gates (two-sided; third outcome named):**

- **SU-G1 COVERAGE = 1 (or the wall is pattern-universal)**:
  - *REFUTES path 2*: coverage(bipartite or complete) < 1.0 at every
    cell — there EXISTS a pattern no dial combination supports on that
    substrate; the coherence ceiling is the substrate's, not the
    pattern's, and "any pattern" is formally false. (This is a real
    possible outcome: the geometry pair held against EVERYTHING so far,
    including speed.)
  - *CONFIRMS*: coverage = 1.0 on ≥ 2 of {bipartite, complete,
    scale_free} — a substrate that supports every pattern in the sample
    at some priced cell; combined with the existing 16-member closure,
    the constraint is reduced to a PRICE, completing the L60 reframe at
    pattern depth.
  - *THIRD (named)*: **PATTERN-DEPENDENT WALL** — coverage = 1.0 up to
    zone count 6 then saturates below 1.0 with a class-specific ceiling
    (the wall is a pattern-CAPACITY); deposit capacity-per-class as the
    honest generalization and the capacity law becomes the new target.
- **SU-G2 THE U-SHAPE AS THE COHERENCE DIAL (needs exp125)**: the
  exp124 arc says optimal pinning is intermediate on the torus. If
  coherence is priced by the deadline, the verifying cell for each
  (substrate, pattern) should sit at the deadline-cleared gamma —
  predicted ZERO free parameters by exp125's analytic integral
  H(γ, t) fitted once on the torus.
  - *REFUTES*: the U-shape does not generalize (grid2d/path curves flat
    or inverted — exp125's registered question) OR the analytic
    prediction misses every geometry-pair edge by > 1 gamma rung: the
    deadline is not the coherence pricing off the torus.
  - *CONFIRMS*: predicted edges within 1 rung on ≥ 2 of 3 substrates —
    "optimal pinning is intermediate" becomes a quantitative, transferable
    coherence law, and the dial lattice collapses to a lookup.
  - *THIRD (named)*: **U-IN-POSITION-NOT-DEPTH** — the optimum's gamma
    position transfers but the deadline depths do not (the curve's
    amplitude is class-specific): the law is qualitative; deposit the
    depth-per-class table.
- **SU-G3 FORMALIZATION-CROSSING ON THE READER PATH (the exp68 control,
  re-run where the stack changed)**: exp68's five formalizations agreed
  because they were all WRITE-path statics. The reader path (post-exp97)
  has never been formalization-tested.
  - *REFUTES (robustness extends)*: no (substrate, pattern) in the SU-G1
    verified set is refused by all five formalizations + the v2 oracle +
    the deadline integral while verifying dynamically — the constraint
    keeps one invariant form even at 101% coverage.
  - *CONFIRMS (the constraint breaks)*: ≥ 1 dynamic verify that every
    static formalization refuses, with a pre-named candidate mechanism
    (the M33 read path — invisible to junction-based metrics by
    construction: b2v, conductance and λ₂ all measure the coupling
    graph, and the read bypasses it). That single crossing IS "breaking
    the coherence constraint" in exp68's own operational sense.
  - *THIRD (named)*: **CROSSING-ONLY-UNDER-BLOCKADE** — crossings appear
    only in gap-0 arms: the formalizations are valid write-path
    instruments but not read-path ones; deposit the split formalization
    (write-path metric + read-path metric) as the corrected constraint.

**Runtime**: ~4–6 h serial (60 patterns × 3 substrates × 6 cells × 3
seeds ≈ 3.2 k runs at 5–15 ms each for the identity read; the
deadline-priced cells and thinning arms are the slow tail; 100-gen
holds EXCLUDED — verdicts are identity-read only, holds are Section 1's
instrument). **Anchors**: `results/exp68_coherence_search.json`,
`results/exp73_active_renormalization.json` … `exp79` (the wall ladder),
`results/exp112_walk_speed_ladder.json`, `results/exp124_deadline_curve.json`
+ exp125's analytic fit (the run this design waits for),
`results/exp81_compiler_v4.json` (pattern classes),
`docs/PRICE_MAP_V2.md`, and the exp126 deposits if Section 1 ran first
(the invented classes enter the pattern sample — the two designs
compose: v6 invents, path 2 prices the inventions on the hardest media).

---

## The three theses, one line each

1. **v6**: a proposal→price→execute→verify→register loop with the corpus
   library frozen OUT of proposal time makes "self-initiated invention"
   decidable — NOV(spec) > the library's own 95th-percentile internal
   spread, non-recombinant, executable, heritable — or the gates say
   honestly which of sampling/specious/star-only it degenerated to.
2. **The cone**: setting k_{t+1} = the cone's own measured horizon h_t,
   on the 19-battery, under the exp124 deadline harness, tests
   autocatalysis (reach ≥ 2× any fixed dial), cross-organism transfer
   (≥ 15/19, zero parameters), and blockade survival (deadline shifted
   later, or the named RESUME-WITHOUT-MEMORY residue) — with M33
   dependence pre-named as its own outcome, not a hidden confound.
3. **The coherence constraint**: path 1 makes the reader universal by
   SUPPLYING the missing posterior pole (canon-as-pole, ARZ lineages) —
   falsifiable at gap 0 on all 19 media with the quadrature and deadline
   gates guarding against a read that secretly rides the two channels;
   path 2 measures pattern-space coverage on the geometry pair and
   scale_free at the full deposited dial stack, where coverage = 1.0
   (or the named capacity wall) plus one formalization-crossing on the
   read path is exactly exp68's own sense of "the constraint breaks".
