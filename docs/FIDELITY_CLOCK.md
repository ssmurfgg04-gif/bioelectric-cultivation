# The Fidelity Clock — Planarian Experiment Series (FC1–FC5)

**Status:** design document, pre-registered before any wet-lab work.
**Blocker resolved:** D3 (the latch-vs-aging-stack joint) closed in exp16/17;
the pattern is now understood as a collective attractor with a protected
memory tier — the clock can be designed against grounded biology.
**Computational predictions being translated:** the bioelectric aging clock
(exp8 T3.2: pattern fidelity predicts remaining lifespan, rho 0.39–0.45),
the two-bottleneck law (pattern AND channel), the quarantine effect of
junction decay, the protected-tier bistability (exp17, +20% median),
the century-hold policy (exp19: write late, hold dense, weak anchor pull).
**Sharpened twice since first pre-registration (recorded, not silently
edited):** (M17) exp20's spatial transcriptomics refuted the
expression-level forms of the injury-transient and junction-smoothness
clauses (V3s/V3c/V4s) — several measurements moved from preferred to
NECESSARY; (M18) exp23's multi-pattern allocation added the two-layer
capacity law (storage free, expression budget-bound), the regional
equilibrium prediction, and the multi-write interference clause — each
carrying its own prediction letters below, tagged (M17)/(M18).

---

## 1. The computational result that demands a wet-lab test

The tower's aging result is specific and falsifiable: **mortality in this
model is driven by the FIDELITY of the somatic bioelectric pattern, not by
cell count, telomere-analog attrition, or damage accumulation per se.** The
bioelectric clock — the quantized 7-level Vmem map's deviation from its
target — predicts remaining lifespan (Spearman rho 0.39–0.45 across regimes,
exp8), and interventions pay only when the pattern (not the channel) is the
binding constraint (the two-bottleneck law, exp8/exp9). Junction decay does
not merely corrupt cells — it QUARANTINES them (islands of corrupted state
that verified maintenance cannot see, T3.1e), and the protected memory tier
holds a written pattern at 0.90 recoverability at age 100 with +20% median
lifespan (exp17, P2/P3 PASS).

None of this has been measured in a real animal as a *clock*. The published
planarian electrophysiology establishes the components — resting Vmem maps
are readable in live worms (Oviedo 2008, PMC10468776 DiBAC4(3) protocol),
innexin expression is spatially patterned and regeneration-critical (Nogi
2005/2007; Oviedo 2009; Peiris 2013), bioelectric memories persist >1 week
and are re-writable (Pezzulo & Levin 2021), injury depolarization precedes
and gates the Ca2+ wave (Chifflet 2005; Liu 2026) — but no one has asked
whether **spatial pattern fidelity of the Vmem map declines with age and
predicts organism-level outcome**. That is the fidelity clock.

**(M18) Which layer the clock lives in:** exp23's two-layer capacity law —
the protected memory tier stores written patterns for free (I_anchor =
1.000 for every pattern under zero maintenance) while the working state
(I_V, the fraction of cells whose membrane voltage actually encodes the
pattern) is the budget-bound, decaying layer. DiBAC reads the WORKING
STATE. The fidelity clock is therefore a claim about the EXPRESSION
layer, not the memory layer: an old worm may hold its target morphology
in (the analog of) stored somatic memory while failing to express it —
and that failure is the clock. FC1's metric must not be interpretable as
memory intactness; the regional-expression decomposition below keeps the
layers separable in principle (FC4 carries the memory-layer test).

## 2. The central hypothesis (falsifiable, one sentence)

> In aging planaria, the Vmem map loses spatial fidelity (quantization
> coherence across tissue regions degrades), this loss — not chronological
> age — predicts regeneration capacity and post-injury mortality, and the
> mechanism is junction-decay-driven quarantine of corrupted bioelectric
> state, reversible by re-derivation but not by naive cell repair.

Every clause maps to a stage below and to a computational result that
generated it.

## 3. Measurement layer (all established methods)

| Conceptual layer | Wet-lab readout | Grounding |
|---|---|---|
| Vmem map | DiBAC4(3) live imaging, calibrated against high-K/valinomycin clamps; ~2 µm resolution, whole-mount | Oviedo et al. 2008 protocol (PMC10468776, PMID 21356693) |
| Pattern fidelity | The SAME metric as the model: quantize the map into the 7-level scale, score region coherence + boundary sharpness (edge guard analog = exclude wound margins) | exp8 fidelity.py, translated |
| **(M17) Map smoothness** | Spatial autocorrelation length of the quantized map, per region — now a PRIMARY readout, not an imported assumption: exp20 refuted the expression-level form of "innexin expression → smooth map" (V4s: rho ≈ 0.02, sign-inconsistent across 0/12/36 hpa), so the coupling↔smoothness relationship must be MEASURED here | exp20 V4s; this series |
| Channel (coupling) | innexin mRNA spatial map (WISH/smFISH: inx-13, inx-11 and the 82-gene AHRD innexin family from the Rosetta mapping) + functional dye coupling (Lucifer-yellow / scrape-load calcein transfer = the bystander assay). **(M17) Functional coupling is the load-bearing measurement and must be taken in the SAME animals as the Vmem map; the innexin-expression map is retained as the expression correlate — expected to DISAGREE with function (the V4s lesson; the disagreement is itself a result)** | Nogi 2005/2007; Oviedo 2009; Decrock 2009; Cusato 2003; Spray 2012; exp20 |
| The write | Controlled Vmem writes: H,K-ATPase manipulation (omeprazole-class), 24h external fields, ion-free media depolarization | Beane 2013; Levin-lab voltage-control toolbox |
| The archive | genome (unchanged across ages — matched controls) | — |
| Stem-cell competence | piwi-1/piwi-2 WISH + X1(Xi+EdU) FACS counts | standard neoblast assays |
| Age staging | body size, fission-event count, lipofuscin/beta-gal, amputation-response latency | planarian aging literature |
| **(M17) Imaging positive control** | Neoblast-rich regions must read relatively HYPERPOLARIZED in the same DiBAC maps (V1s: neoblast ranks 3/31 spatial annotation types in PRISTA4D-inferred Vm — V1 confirmed in a third modality). A pipeline that cannot see this is broken; cohort labels stay blinded until the positive control passes | exp18 V1 + exp20 V1s |

**Honest limitations on record (from exp18, the first real-data test):**
transcriptome-level inference of Vm is rank-robust for stemness (V1 PASS,
both atlases) but cannot capture gating (neurons predict depolarized —
false) or absolute mV; DiBAC imaging is slow (minutes) and cannot resolve
fast transients. The clock claim concerns SLOW spatial structure (aging
timescale: weeks-months), which DiBAC CAN resolve. We do not extrapolate
the atlas inference to dynamics; the dyes carry the measurement.
**(M17 additions from exp20):** (i) the injury-depolarization transient is
INVISIBLE at family-expression level (V3s refuted: the 0→12 hpa Vm
contrast did not rise in PRISTA4D) — no expression-derived assay can
substitute for a direct fast measurement; (ii) innexin-expression maps do
NOT predict Vm-map smoothness (V4s refuted, rho ≈ 0.02) — junction claims
require the functional dye-coupling readout; (iii) phagocytes are NOT the
most depolarized spatial type (V3c refuted) — cell-type Vm ordering from
expression does not transfer; the only expression-inference claim that
survived spatial screening is the neoblast-hyperpolarization anchor (V1s,
now the positive control above).

## 4. The experiment series

### FC1 — the cross-sectional clock (the existence test)
**Design:** 3 age cohorts (young ~1 mo post-hatch, middle, old — staged by
size/fission count, n≥30 each, strain-matched, size-matched-across-stagings
where possible). DiBAC4(3) whole-mount imaging of intact animals (head,
pre-pharyngeal, tail regions), WITH same-animal dye-coupling measurement
(scrape-load calcein — the M17 load-bearing co-measurement) and per-region
spatial-autocorrelation of the quantized map. Compute the fidelity metric
per worm; decompose per region. Positive control (neoblast hyperpolarization,
V1s) must pass before unblinding cohort labels.
**Pre-registered predictions:**
- FC1a: fidelity declines monotonically with cohort age (one-sided
  Jonckheere-Terpstra, p<0.05).
- FC1b: spatial VARIANCE of the quantized map rises with age (the
  corruption signature). **(M18) Sharpened: the rise is REGIONALLY
  STRUCTURED, not uniform** — see FC1d.
- FC1c: age-matched high-fidelity outliers exist (the clock ticks
  independently of calendar age — correlation of fidelity with functional
  age markers > with days-since-hatch).
- FC1d **(M18, from exp23's equilibrium law):** the regional fidelity
  deficit ORDERING follows regional cell-turnover burden — high-turnover
  regions (neoblast-rich) lose expression fidelity FIRST and MOST. In the
  model the deficit is a death-restoration equilibrium (the steady-state
  wrong-fraction is set by the regional hazard rate, not by maintenance
  budget or allocation); if real-worm fidelity decline is instead UNIFORM
  across regions, the aging vector is not turnover-driven and the
  model's mechanism does not transfer.
- FC1e **(M17, from V4s):** the map's spatial autocorrelation and the
  same-animal dye-coupling range are correlated ACROSS animals (the
  coupling↔smoothness relationship, measured for the first time).
  Pre-registered direction: positive. The expression-level form was
  refuted; this clause tests the FUNCTIONAL form.
**Falsifies:** the whole program if fidelity does not decline (the
bioelectric clock is not real in vivo). FC1d additionally kills the
turnover-equilibrium mechanism (though not the clock's existence) if
regional structure is absent.
**Cost:** ~6 weeks, one imaging rig, no transgenics. This is the minimal
viable experiment.

### FC2 — the clock predicts function (the prognosis test)
**Design:** within the old cohort, measure baseline fidelity (DiBAC, day 0),
then amputate pre-pharyngeally; score head regeneration at 7/14/21 dpi
(blind scoring, standard metrics), neoblast response (piwi-1 WISH at 3 dpi),
and survival to completion.
**Pre-registered predictions:**
- FC2a: baseline fidelity predicts regeneration score at 14 dpi
  (Spearman rho ≥ 0.4 — the computational value is 0.39–0.45; if the real
  clock is weaker than rho 0.25 the two-bottleneck law does not transfer).
- FC2b: fidelity predicts post-amputation survival (Cox, coefficient
  significantly negative, p<0.05).
- FC2c: fidelity out-predicts neoblast COUNT (the pattern is the bottleneck,
  not the stem-cell pool — regression model comparison, AIC).
- FC2d **(M17, from V3s):** the amputation-response transient clause.
  exp20 refuted the expression-level form of injury depolarization (the
  PRISTA4D 0→12 hpa contrast did not rise); DiBAC cannot resolve the
  transient's timescale (seconds-minutes). The fast transient is therefore
  NOT measurable in this series with the current readout — it is
  explicitly OUT of scope here and carried by: (i) amputation-response
  latency (behavioral, seconds-minutes) as a coarse surrogate, and (ii) a
  future collaborator with a fast genetically-encoded voltage indicator
  (GEVI-class) or double-barrel microelectrode. Recorded so nobody
  mistakes silence on the transient for evidence against it.
**Falsifies:** the mortality mechanism (if piwi-1 count out-predicts
fidelity, the model's causal ordering is inverted in vivo).

### FC3 — the quarantine test (the mechanism)
**Design A (accelerate):** young worms, RNAi of inx-13/inx-11 (the
characterized innexins) for 3 feedings; measure fidelity + dye-coupling
range (scrape-load calcein) + regeneration.
**Design B (rescue attempt):** aged worms with confirmed low coupling;
attempt junction restoration (rotigaptide-class connexin opener — NOTE:
innexin specificity unverified, first test in vitro on coupled planarian
cells; if no opener validates, rely on Design A + genetic rescue via
innexin-overexpression lines if available).
**Pre-registered predictions:**
- FC3a: innexin knockdown in YOUNG worms phenocopies OLD fidelity
  (fidelity drop ≥ the young→old gap) — junction decay is sufficient.
- FC3b: knockdown worms show ISLANDS of corrupted Vmem (spatial
  autocorrelation length collapses) — quarantine, not uniform drift.
- FC3c: dye-coupling range (bystander radius) correlates with fidelity
  across ALL animals regardless of age or treatment (the coupling→clock
  link, rho ≥ 0.5).
- FC3d: junction restoration in aged worms recovers fidelity FASTER than
  re-derivation but mortality SLOWER (the two-bottleneck prediction:
  un-quarantining corruption without repairing it should transiently HURT —
  the connexin-boost hazard T3.1e).
**(M18) Expectation calibration (so the design is not killed by its own
optimism):** exp21 bounded the junction claim to WEAK form — junctions
are NECESSARY for normal patterning (above the cutting baseline) but not
uniquely disruptive among recorded perturbations (the strong form failed
  at ~3-study effective power in PlanformDB); do not expect innexin RNAi
  to be the most abnormal phenotype in the room, expect it above cutting
  baseline. exp22 adds the geometry: the matched-channel memory axis
  (k_anchor) dominates the local write co-metric — effect sizes on OTHER
  axes (boost-type interventions) are expected SMALL and flat; the
  strongest junction-manipulation effects should sit on the coupling axis
  itself, and plateau-shaped dose responses are the expected norm, not a
  failure of the manipulation.
**Falsifies:** the quarantine mechanism specifically (if corruption stays
spatially uniform under knockdown, junction decay is not the vector).

### FC4 — the write/erase test (the protected tier in tissue)
**Design:** hyperpolarization writes at ectopic positions (H,K-ATPase
manipulation per Beane 2013 / defined external fields); then EITHER wait
(with no further intervention) OR apply the erasing stimulus (depolarizing
pulse / pump-blocker); measure persistence of the written Vmem region.
**Pre-registered predictions:**
- FC4a: a written ectopic Vmem region persists ≥ 7 days without
  maintenance (Pezzulo 2021's >1-week storage, now measured as a map
  feature — the protected tier).
- FC4b: persistence requires junction INTEGRITY (repeat after inx RNAi:
  the write decays without coupling — the collective, not the cell, holds
  the memory).
- FC4c: a second deliberate write overwrites the first (re-writability),
  while passive depolarization transients (injury-mimetic, ATP bath) do
  NOT (the deliberate-write gate — exp17's core distinction).
- FC4d **(M18, from exp23 E1):** two simultaneous ectopic writes show
  LITTLE interference. In the model, competing written patterns share
  the maintenance channel only marginally (competition cost ≈ 0.02 even
  at extreme maintenance scarcity, storage layer free — the two-layer
  capacity law); transfer prediction: writing region 2 does not
  measurably accelerate the decay of region 1 (paired comparison, effect
  < the write-to-erase contrast). If simultaneous writes DO interfere,
  tissue memory capacity is shared in a way the model's protected tier
  is not — the most informative possible failure.
**Falsifies:** the protected-tier semantics if writes decay passively or
if injury-mimetic transients overwrite them; FC4d kills the free-storage
layer claim if simultaneous writes interfere.

### FC5 — the clock reset (re-derivation rejuvenation)
**Design:** aged worms, repeated amputation-regeneration cycles (the
computational +20%/x1.25 re-derivation result, the Dai et al. 2025
analog); measure fidelity and coupling before/after each cycle; parallel
senolytic-style control (phagocyte ablation) to dissociate
cell-clearance from pattern re-derivation.
**Pre-registered predictions:**
- FC5a: each regeneration cycle partially RESETS fidelity (recovers
  toward the young value; effect size should exceed cell-turnover-only
  controls).
- FC5b: the reset decays — cycles must repeat (the channel engine is not
  reset; exp8's regenerate rejuvenation reproduces mechanistically).
- FC5c: post-cycle fidelity gains predict post-cycle survival gains
  (the clock is causal-proxy, not epiphenomenal — the strongest single
  test of the whole program).
**Falsifies:** the rejuvenation mechanism (if regeneration resets cells
but not fidelity, the pattern is not the aging-relevant variable).

## 5. Explicit falsification table

| Stage | Kills | If it fails |
|---|---|---|
| FC1 | the clock's existence | bioelectric fidelity is not age-structured → the model's mortality law is an artifact of the simulation regime |
| FC1d | the turnover-equilibrium mechanism (M18) | decline is regionally uniform → the aging vector is not cell-turnover burden |
| FC1e | the functional coupling↔smoothness link (M17) | autocorrelation is uncoupled from dye-coupling range → the junction-smoothness clause dies at the functional level too |
| FC2 | the clock's prognostic value | fidelity is descriptive but not predictive → the two-bottleneck law does not transfer |
| FC3 | the quarantine mechanism | junction decay corrupts uniformly → the island/quarantine architecture is model-specific |
| FC4 | the protected tier | memories decay passively → bistability claim unsupported in tissue |
| FC4d | the free-storage layer (M18) | simultaneous writes interfere → tissue memory capacity is shared in a way the model's protected tier is not |
| FC5 | the rejuvenation route | regeneration resets cells not pattern → the +20% result is a simulation artifact |

## 6. What the first two weeks look like (FC1 minimal viable protocol)

1. Culture expansion, age staging by size + fission history (3 cohorts × 40).
2. DiBAC4(3) calibration series: high-K depolarized vs valinomycin-clamped
   controls → the intensity→mV curve for OUR rig (the published protocol's
   step, non-negotiable for absolute claims; rank claims survive without
   it).
3. Pilot n=5 per cohort: exposure time, dye concentration, photobleaching
   budget, region segmentation (head/prepharyngeal/tail).
4. Lock the fidelity-metric implementation (the quantized-map coherence
   score, edge-guarded) BEFORE unblinding cohort labels — the metric code
   is committed to this repo (cultivation/bioelectric/fidelity.py's
   `pattern_fidelity` translated to 2D images).
5. **(M17) Positive-control gate BEFORE any aging analysis:** in the same
   pilot maps, neoblast-rich regions must read relatively hyperpolarized
   (the V1s anchor). Pipeline failure stops here — not a biological
   result.
6. **(M17) Same-animal coupling co-measurement:** scrape-load calcein on
   a pilot subset (n=5/cohort) to establish the dye-coupling assay's
   variance before scaling it into the full FC1 (the load-bearing
   junction measurement, per V4s).
7. **(M18) Per-region decomposition from day one:** the fidelity metric,
   spatial variance, and autocorrelation are computed per region
   (head/pre-pharyngeal/tail + neoblast-rich masks if WISH is run) — the
   FC1d ordering test needs the regional table, not a whole-animal scalar.
8. Power check from the pilot: if the young-vs-old fidelity effect is
   detectable at n=30 with the pilot's variance, proceed to full FC1.

## 7. Resource & risk register

- **Rig:** standard epifluorescence (DiBAC = FITC channel); no confocal
  required for FC1 (whole-mount coherence is a mesoscale metric).
- **Animals:** asexual clonal line (removes genetic variance — the model's
  identical-genome assumption has a real counterpart).
- **Drugs/reagents:** DiBAC4(3), valinomycin, nigericin, omeprazole-class
  pump inhibitors, octanol/heptanol (junction block controls), Lucifer
  yellow, calcein-AM.
- **Main risks:** (i) DiBAC toxicity/photobleaching at repeated-measure
  tempo (mitigate: cross-sectional primary, longitudinal secondary);
  (ii) innexin-opener pharmacology unvalidated on innexins (mitigate:
  FC3 Design A carries the mechanism claim, Design B is upside);
  (iii) regeneration scoring subjectivity (blind scoring, published
  rubrics).
- **Kill-switch discipline:** each stage's falsification row is
  pre-registered above; a failed stage is REPORTED, not iterated past —
  the project's own FALSIFICATION.md ledger discipline applies to the
  wet-lab program exactly as to the computational one.

## 8. The standing order (search-first)

Per the project directive adopted this session: before any new wet-lab or
computational stage, sweep the literature for an existing answer first
(this session's sweep found: the DiBAC protocol existed; the Rosetta
annotation existed; the write-protected consolidation model existed and
matched exp17). The default hypothesis is that 90% of what we're about to
build has a published method — the job is to find it, cite it, and spend
the novel effort only on the genuinely open joint.

**Sharpening-round audit trail:** (M17) the spatial sweep found PRISTA4D
(Han 2026, GigaScience) and used it to test the expression-level forms of
our spatial predictions BEFORE the wet lab — three of four died there,
which is the sweep doing its job; (M18) exp23 ran the AI-Scientist's
multi-pattern idea through the stack first, so the wet-lab program now
carries layer-explicit (storage vs expression) predictions, a regional
equilibrium clause, and a multi-write interference clause instead of
unexamined single-write assumptions. Both rounds are tagged inline above
— nothing was silently edited.
