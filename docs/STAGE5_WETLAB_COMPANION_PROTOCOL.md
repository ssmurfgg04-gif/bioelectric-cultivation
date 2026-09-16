# Stage-5 Wet-Lab Companion Protocol — the record's missing dose axis, tested at the bench

**Status:** pre-registered; no wet-lab work performed. Wet-lab companion to
`docs/STAGE5_EXTERNAL_STORAGE_PROTOCOL.md` (the sim-side Stage-5 protocol,
exp80, 6/6, L61): what a real planarian regeneration lab would run to test
the same predictions the simulation carries.
**Predecessors:** exp91 (L73 — the amplitude axis), exp92 (L74 — the fine
ladder + the record property), exp93 (L75 — the refusal price hierarchy),
exp94 (L76 — the multi-zone scale-up), exp33/L16 + quest 001 (no
concentrations anywhere).
**Ledger discipline:** every section is a pre-registered prediction with an
explicit pass/fail gate, registered before the first animal is dosed. A failed
gate is REPORTED, not iterated past — the FALSIFICATION.md discipline applies
at the bench exactly as on the machine. No post-hoc endpoints; a vacuous gate
is repaired BEFORE the run or the run does not happen (the exp91 DA-G3 lesson).
**Ledger-state correction (recorded, not silent):** this protocol relies on
L73-L76 only — the amplitude axis, the fine ladder, the price hierarchy, and
the 11/12 topology scale-up all stand. The deg-99 star refusal of L76 is
cited solely as the sole refusal; L77-L78's mechanism account for it
(single-point integrator / architecture boundary) is UNDER ACTIVE REVISION —
a decomposition probe attributes the star's error to ~32
amputated-never-rebuilt cells at wound state, an executor coverage artifact —
and no gate below depends on that story.

## 0. The frame — what transfers and what does not

The simulation's amplitude axis `d` is a DIMENSIONLESS write amplitude
(theta interpolation toward the adopted full push; d=1.0 bit-exact vs
exp88's full-corruption arm, d=0.0 the plain protocol arm). The bench's dose
axis is a concentration in mM. The transfer claimed here is SHAPE-level —
monotone, graded, stratified, localized — never absolute-mV (the record's
absolute-value fidelity is already named untestable, L22/exp39). The
d-units-to-mM mapping is itself W1's deliverable; later sections consume it.

| Sim object (ledger) | Bench object (this protocol) |
|---|---|
| amplitude axis d (L73-L74) | octanol/heptanol concentration ladder (W1) |
| the M33 line (anterior identity, spec >= -35 mV) | amputation-plane taxonomy: pre-pharyngeal / trunk / post-pharyngeal (W2) |
| R5' price hierarchy (L75) | dose x duration price per tissue context (W3) |
| multi-zone write + two-source read (L72, L76) | patterned spatial write + regeneration localization (W4) |
| the record property (L74; exp33/L16) | the deposit schema — the table added back (W5) |

Standing toolkit (established; nothing invented here): heptanol / octanol /
lanthanum as gap-junction blockers (Saito et al. 2003, DOI 10.1002/dvdy.10246
— octanol/GJ blockade in planarians); the Durant et al. 2019 GJ-blocker
regeneration phenotype database (MED30799071) as the scoring reference;
wnt-1 / apc-1 RNAi as axis controls; DAPI + immunostaining (brain, eyes) as
confirming readouts; DiBAC4(3) voltage mapping and scrape-load calcein dye
coupling per the repo's FC measurement layer (`docs/FIDELITY_CLOCK.md`,
PMC10468776).

## 1. W1 — THE DOSE AXIS (the highest-value test)

**The sim prediction.** The amplitude axis is MONOTONE with a GRADED EDGE at
a threshold. exp91 (L73, DA-G4/DA-G5): wnt|trunk rates [0, 0, 1, 1, 1] across
d in {0, 0.25, 0.5, 0.75, 1.0}, Spearman 0.866; apc|trunk mirrors; threshold
region d in [0.25, 0.5]. exp92 (L74, FL-G1) resolves the fine ladder (7
seeds, d in {0.25 .. 0.50}): rates [0, 0, 0, 0.429, 1, 1] — graded window
d in [0.35, 0.45], the 3/7 rate at d=0.40. The record's partial block (mean
0.105, 11 modulator-class rows; the wider 17-row block spans [0.00, 0.45],
mean 0.189) sits inside the sim's reachable regime. And the axis is EMPTY ON
THE RECORD SIDE: PlanformDB has no concentrations (exp33, L16), the
literature has no partial-dose regeneration curve for planarian GJ blockers
(Europe PMC: supramaximal doses, timing ladders only — exp40's S2R3c
closure), quest 001's literature pass corroborated with 6 real PMIDs. The
wet-lab deliverable IS the dosing table.

**The wet-lab manipulation.** An octanol concentration ladder, 10 steps,
plus a heptanol cross-check:

- **Anchor.** C_full = the literature's established full-blockade working
  concentration (transcribed from Saito 2003's octanol protocol and the
  Durant 2019 database's sustained-bath arms at bench time — no numbers
  invented here, per the house discipline). Exposure window FIXED at the
  published sustained protocol (bath from amputation t=0 through the regen
  window — the record's pub1 anchor); washout arms are W3's business.
- **The ladder.** 10 steps as fractions of C_full: 1.00, 0.70, 0.50, 0.35,
  0.25, 0.18, 0.12, 0.08, 0.05, 0.03 — full blockade to below-effect.
  Concentration is the ONLY free parameter in W1.
- **Cross-check.** The same structure in heptanol, anchored at its own
  C_full (the record's 2005 heptanol protocol). Tests that the shape is
  blocker-family, not octanol-specific pharmacology.
- **Controls per block.** Vehicle-only (the d=0 anchor); cutting-only
  baseline (the record's cutting floor); wnt-1 and apc-1 RNAi arms as the
  axis-control positive controls for the rubric (the record's effector-class
  rows; the sim's d=1.0 arm reproduces the full push).
- **n.** 30 animals per step per blocker (~1,300 with controls). Amputation
  plane randomized within each step (W2 consumes the same animals).

**The readout.** Penetrance per step: fraction of animals scored
abnormal-or-worse per the Durant-database rubric at 7 and 14 days
post-amputation, blind-scored, DAPI / immunostaining (brain, eyes)
confirming every scored animal. Penetrance is the ONLY primary endpoint.
Scrape-load calcein dye coupling co-measured on 5 animals per step — the
functional blockade curve used in the calibration.

**Gates.**

- **W1-G1 (monotone) PASS** if penetrance vs log10(concentration) is
  monotone non-decreasing: one-sided Jonckheere-Terpstra p < 0.05 AND
  Spearman >= 0.8 (the sim's 0.866 sets the bar; seed noise is the
  allowance).
- **W1-G2 (graded band) PASS** if >= 1 step carries penetrance strictly
  between 0 and 1, AND the band width (log10 distance from the last step
  <= 5% to the first step >= 95% penetrance) exceeds one ladder step.
  **REFUTATION = the all-or-nothing switch:** wild-type or full-phenotype at
  every step, transition narrower than one step. A switch contradicts the
  amplitude-axis mechanism directly — the record's partial phenotypes (11
  rows, mean 0.105) cannot come from a step function; refutation indicts the
  record's decoding as well as the sim's curve.
- **W1-G3 (blocker family) PASS** if heptanol reproduces W1-G1 + W1-G2 at
  its own anchor.
- **W1-G4 (slice resistance, secondary) PASS** if at least one phenotype
  class stays at baseline across the FULL ladder — the wnt|crosspiece
  analog (flat 0 at every dose, exp91's deposited slice), pre-registered as
  the anterior-plane class under the M33 asymmetry. If every class responds
  somewhere, the regime-dependence prediction is refuted.

**The calibration deliverable (d-units to mM).** The map from sim d-units to
mM is the deliverable, not a fitted nuisance. Endpoint-anchored: d=1.0 <->
C_full (the sim's d=1.0 arm is bit-exact vs the full push; the bench's
C_full is the published full-blockade protocol), d=0.0 <-> vehicle; the
interior is fixed by the measured penetrance and dye-coupling curves
(coupling fraction is the functional dial; concentration only its proxy).
Output: the table — step, concentration, coupling fraction, penetrance,
d-equivalent — deposited per W5's schema. The calibration passes
intrinsically with W1-G1/G2: a monotone graded curve is what MAKES the map
definable; a switch is not.

**Feasibility, cost.** ~6-8 weeks, one culture room, no transgenics,
epifluorescence only. Octanol and heptanol are cheap; animals are asexual
clonal lines (the model's identical-genome assumption has a real
counterpart). The cheapest decisive experiment in the document.

## 2. W2 — THE TWO-SOURCE READ (the anterior-pole asymmetry)

**The sim prediction.** The regen read is TWO-SOURCE: an anterior
constitutive identity source above the M33 line (spec >= -35 mV, the
head/trunk fate-axis midpoint — the pole read, junction-independent) and
junction-carried canon memory below it (L72's repair; exp46's M33).
Consequence: GJ-blockade defects concentrate at POSTERIOR planes — anterior
identities do not need the junctions to be read. The record already carries
the asymmetry (L32, exp50): gj_block|tail 0.599 (n=7, the highest plane
rate) vs gj_block|head 0.177 (n=6, the lowest); the octanol sustained subset
is the M33-consistent 0.092 vs the heptanol delayed subset's 0.345 (the
mixture exp66 diagnosed).

**The wet-lab manipulation and readout.** The SAME sustained blockade (one
mid-band concentration — the step nearest the graded edge from W1) at
randomized amputation planes: pre-pharyngeal, trunk, post-pharyngeal —
identical concentration, window, strain, scoring. W1's animals carry this
arm for free (plane randomized at step level); standalone W2 is 3 planes x
n=60. Readout: plane-resolved penetrance at 14 dpi, same rubric; the
statistic is the tail-vs-head penetrance gap at matched dose.

**Gates.**

- **W2-G1 (direction) PASS** if posterior-plane penetrance exceeds
  anterior-plane penetrance (one-sided p < 0.05 at matched dose). The
  direction is pre-registered, not two-tailed.
- **W2-G2 (quantified gap) PASS** if, at the lowest step where posterior
  penetrance >= 0.5, anterior penetrance <= 0.25 (a >= 2x gap; the record's
  0.599/0.177 = 3.4x brackets the bar from above).
- **W2-G3 (blocker-plane interaction) PASS** if the direction holds under
  both blockers — not an octanol-specific vehicle artifact.

**Feasibility, cost.** Near-zero marginal cost piggybacked on W1
(randomization is the only addition). Standalone: ~3 weeks.

**What a refutation means.** Symmetric (or reversed) plane distribution at
matched dose: the M33 anterior-pole protection does not transfer to real
tissue, and the two-source read's wet-lab motivation dies — the sim keeps
the mechanism only as a record-fit device, a materially weaker claim. The
sharpest cheap test in the document.

## 3. W3 — THE PRICE HIERARCHY (R5' as substrate-dependence)

**The sim prediction.** exp93 (L75, RP-G3/RP-G4) prices every refusal as a
dial distance, and the prices STRATIFY INTO THREE CLASSES:
writable-at-default (price 0 — path, grid2d, random6, small_world),
theta-channel-priced (torus — the gamma ladder FAILS through 64 at default
mu; mu->0 alone buys it), two-dial-priced (random3, scale_free — only the
joint probe (4, 0) verifies; neither dial alone suffices). The star point
(64, 0) is overkill on the verify path. The universal claim is the
STRATIFICATION: contexts differ in price, not in whether a price exists.

**The wet-lab manipulation.** Price at the bench = the minimal
(concentration x exposure duration) product reaching the phenotype bar
(penetrance >= 0.5 at 14 dpi) per tissue context, measured with the SAME
blocker family:

- **Plane** (the record's taxonomy): pre-pharyngeal / trunk /
  post-pharyngeal.
- **Feeding state**: pre-feeding vs 7-days-post-feeding (the neoblast-cycle
  dial — the internal identity-state context).
- **Strain**: S. mediterranea clonal line vs G. dorotocephala (the
  head-shape-work strain; the Durant database's own heterogeneity).
- **Duration ladder** on one context (1, 2, 3, 6, 12, 24 h pulses + the
  sustained bath) to test concentration-duration substitutability — the
  two-dial structure.

Bracket-and-bisect pricing, not full ladders per context: 3-5 points around
each context's own bar. W1/W2 arms are reused as the plane-context data.
Readout: price per context in (C, t), with the iso-effect contour from the
duration ladder; secondary, dose-dominant vs duration-dominant pricing per
context — the measured analog of the channel attribution (V-channel ratio vs
theta homogenization), reported as measured.

**Gates.**

- **W3-G1 (not universal) PASS** if the universal-threshold null — one
  (C x t) price for all contexts — is refuted: context explains significant
  penetrance variance beyond concentration alone (likelihood-ratio
  p < 0.05).
- **W3-G2 (three classes) PASS** if >= 3 price classes separate by >= 1
  log10 step each across the context battery.
- **W3-G3 (the ordering) PASS** if plane price orders post-pharyngeal <
  trunk < pre-pharyngeal — pre-registered from the record's plane rates
  (0.599 / mid / 0.177) and W2's asymmetry; the one ordering the record
  already half-carries.
- **W3-G4 (dial structure) PASS** if an iso-effect contour exists on one
  context (concentration and duration substitutable within a measured
  band).

**Feasibility, cost.** The expensive section: context battery x
bracket-and-bisect pricing, ~1,000-1,500 animals over 10-12 weeks. No
instrumentation beyond W1; the duration ladder is the added labor, everything
else is assignment.

**What a refutation means.** A single universal threshold across all
contexts: the sim's substrate-dependence (R5') is a topology artifact in
silico, not a property of real tissue context — and the compiler's
context-priced intervention vocabulary does not transfer. Honest failure
mode noted in advance: partial stratification (2 classes, not 3) DOWNGRADES
the hierarchy claim but does not refute the transfer — the sim's own
classes were measured, not assumed; the bench's are read the same way.

## 4. W4 — MULTI-ZONE ANATOMY TARGETING (the hardest)

**The sim prediction.** The compiler writes multi-zone NOVEL patterns — the
canonical deposit: 3 zones at -30 mV in a trunk background — and
regeneration RESPECTS the written zones through the two-source read: 11/12
new topologies verify (L76, MS-G1, errors 0.49-3.34 mV, n=200 scale
included), the canon source is load-bearing 12/12 (MS-G3), and there is NO
BACKDOOR — a below-line novel spec is refused on every substrate (MS-G2;
TS-G3). The calibrated envelope (exp81): width >= 8 cells, contrast >= 4 mV.
The deg-99 star is the sole refusal (mechanism account under revision; not
load-bearing here). The bench question: does a spatially patterned
pharmacological write survive the regeneration read as a ZONED pattern, and
is writability one-directional along the identity axis?

**The wet-lab manipulation (the minimal pre-registered version).** ONE
patterned stripe + ONE control stripe. Not the full multi-zone battery —
that is not yet pharmacologically feasible, and pre-registering it would be
wishing.

- **The write.** A local depolarizing stripe at a posterior-lateral position
  — the established write direction (posterior depolarization -> anterior
  fates; the exp39 match set, Oviedo 2010 in the record). Delivery:
  modulator-soaked gel stripe (cheapest) or microelectrode iontophoresis
  (fallback), sized to the envelope — width >= 8% of body length (the
  8-cell width at n=100, translated), contrast >= 4 mV on the map.
- **Verification (a pipeline gate, not a biology gate).** The stripe is
  mapped pre-amputation with DiBAC4(3) — the sim-side protocol's CAPTURE
  step. If the write cannot be verified on the map, the run stops; not a
  biological result.
- **The challenge and the control.** Amputation through/beside the written
  region; mirror position on vehicle-only animals as the control stripe.
- **The domain arm (the sharp one).** The mirror-direction write —
  posterior-fate induction at an anterior wound — where the sim's
  no-backdoor rule predicts REFUSAL (the canon read gives each cell its own
  coordinate identity, never the novel spec); the record's one-way
  direction (exp39's match set) is the bench precedent.
- **n.** ~100-200 animals across write / control / domain arms (3-4 batches
  of 30-50; pilot n=5 per arm before scaling — the FC first-two-weeks
  discipline).

**The readout.** Ectopic structure scoring at 7/14/21 dpi (blind, DAPI +
immunostaining), localized against the PRE-WRITE map — the stripe's
coordinates fixed before amputation. The envelope check rides the same
images.

**Gates.**

- **W4-G1 (the write holds) PASS** if the stripe is measurable on the DiBAC
  map immediately post-write AND at amputation, at the registered contrast.
  Pipeline failure stops the section.
- **W4-G2 (regen respects the zone) PASS** if ectopic structures localize to
  the written stripe above the control-stripe rate (Fisher exact p < 0.05).
  **REFUTATION:** written patterns do not survive the regen read in tissue —
  the two-source read's central claim fails at the bench regardless of the
  sim's 11/12.
- **W4-G3 (the control stripe) PASS** if the un-patterned stripe produces
  baseline (no ectopic structures above intact-animal background) —
  handling-is-not-the-treatment.
- **W4-G4 (the domain rule) PASS** if the mirror-direction write produces NO
  ectopic structures above baseline — writability is one-directional along
  the identity axis, the no-backdoor rule in tissue. **REFUTATION:** ectopic
  structures form regardless of direction — a bigger real capability than
  the sim claims, and a refutation of the M33 domain rule's transfer,
  recorded as such.

**Feasibility, cost, refutation stakes.** Highest risk in the document:
spatial pharmacology with voltage-map verification, ~8-10 weeks, DiBAC rig
plus a working stripe-delivery method. Pre-registered at MINIMAL scale
deliberately: one stripe, one control, one domain arm; the full multi-zone
battery waits on this section's outcome, not on ambition. W4-G2 failure
kills the transfer of the multi-zone regen claim; W4-G4 failure kills the
domain rule's transfer and enlarges the wet-lab capability space — both
informative, neither silent; that is why the section is registered small
and specific.

## 5. W5 — THE RECORD PROPERTY (what the dosing table adds back)

**The sim finding being closed at the record level.** The corpus's morphogen
residual closed as a RECORD property, not a sim gap (L74): the lesson chain
family -> class -> within-class terminates in the database itself —
PlanformDB carries no drug concentrations (exp33, L16), so the row-level
dose identity of each record row is unknowable from the record's structure
alone. The class rule landed below bar (FL-G2, phi 0.375 — the record's dose
structure is gene-specific beyond canonical classes); decoded MAE stands at
0.290 (from exp70's 0.522); the morphogen share is 6.5% and
mechanism-closed; the sim-side Stage-2 queue is EMPTY. Quest 001
established the same hole on the published side: NO partial-dose curve
exists for planarian GJ-blocker regeneration — supramaximal doses, timing
ladders only.

**What W1-W3 add back.** The dosing table IS the missing record column.
Every W1/W2/W3 animal contributes one row with the measured dose identity
the record lacks, turning the within-class heterogeneity (the modulator
block's raw 0.05-0.45 spread that no single family dose fit — L74's core
deposit) from an unknowable into a measurement.

**The deposit schema.** Machine-readable (CSV + JSON), keyed to PlanformDB's
experiment schema (the `planform_mining.py` plane / drug taxonomy) so the
exp92 row-level mapping can be re-run with measured doses:

- species
- blocker (and vehicle)
- concentration (mM, and fraction of C_full)
- exposure window (start / end relative to amputation; sustained or pulse)
- amputation plane (pre-pharyngeal / trunk / post-pharyngeal)
- phenotype score (Durant-database rubric, plane-resolved penetrance)
- n

Extended columns per row: measured dye-coupling fraction (the functional
dial), the rig's intensity->mV calibration constants, blocker batch, and the
blind-scoring rubric version. Deposited with the publication (supplementary
table) and registered in this repo's record as the record-side repair — the
decoding-discipline act the ledger says the < 0.15 target requires.

**The downstream gate.** W5-G1 is a SIM-side re-analysis (no new mechanisms
— the ledger's own framing: record-side decoding discipline, not new sim
code), run once the deposit lands; registered here so the deposit has a
pre-committed reader.

- **W5-G1 PASS** if re-running the exp92 row-level dose mapping with the
  MEASURED concentrations (in place of the canonical class rule) resolves
  the within-class heterogeneity: the morphogen residual share falls from
  6.5% toward the record's series-variance floor (the cutting share, 10.0%,
  is the named next floor). **REFUTATION:** if measured doses still do not
  resolve the record's within-class spread, the residual is protocol
  heterogeneity (exp51's D1 measured gj_block's H at 0.432), not dose
  identity — the record property gets a second, sharper name, and the
  ledger row is written accordingly.

**What failure means.** If W1's ladder never assembles (a switch, not a band
— W1-G2 refuted), the table is deposited anyway: a measured all-or-none
column is still the record repair, and it converts the amplitude axis's
wet-lab status from "untested, stands" to "refuted at the bench" in one
deposit. The record property and the amplitude axis are separable claims;
this section keeps them separable at the outcome level too.
