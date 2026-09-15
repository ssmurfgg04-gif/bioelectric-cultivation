# Night-six synthesis — the published answers, pieced together

Source abstracts: `NIGHT_SIX_RESEARCH.md` (raw Europe PMC fetch, 14 queries).
This doc states, for each night-six open item, what the published literature
already answers and the mechanism decision that follows. Fetched 2026-09-15.

---

## 1. M31 — anchor availability is a STORAGE-HISTORY property

**Published answers (pieced):**

* *Positional Information and Stem Cells Combine to Result in Planarian
  Regeneration* (Ross et al. 2022, PMC34518341): planarians display
  **constitutive expression of positional information from muscle cells**
  (it is continuously maintained, not minted at wound time), and amputation
  triggers **rapid resetting** of that information — the reset is a
  **rewrite of what is already stored**, required for regeneration.
* *egal-1 and microtubules promote regeneration polarity* (2025,
  PMC41099308) + *Planarian microtubules form a network within muscle*
  (2025, PMC41099309): the polarity read is carried by a **physical
  substrate inside the pre-existing tissue** (longitudinal muscle fibers,
  their microtubule network, asymmetric RNA localization via Egal-1) —
  the wound reads a **stored, material state**, and colchicine shows the
  read is **dose-structured** (125 µg/ml ELEVATES ectopic notum at
  posterior wounds; >200 µg/ml PREVENTS wnt1/notum expression).

**Decision:** the stochastic unit for graded penetrance cannot be a fresh
coin flip at regrow time (exp38 amendment flipped a marginal seed exactly
because regrow-time RNG is unphysical). Implement M31 as
**anchor availability derived from the fragment's stored history**: the
wound-face anchor is AVAILABLE iff the fragment's own expressed identity at
the face still agrees with the spec that belongs there
(`|theta[face] - phi_spec[face]| <= threshold`). No regrow-time RNG;
seed-splitting arises from the seeds' genuinely different noise histories
during the 24h settle — the same way real fragments differ. This is
stream-neutral and bit-exact at defaults (threshold = inf).

## 2. innexin|head — the head-specific protection channel is NEURAL/MUSCLE, non-junctional

**Published answers:**

* *Neural control of body-plan axis in regenerating planaria* (Lobo,
  Emmons-Bell, Levin 2019, PMC30990801): the head-tail axis is controlled
  by the **net polarity of neurons**; the morphogen vector-transport field
  **coincides with nerve axon alignment** — a transport channel that is
  structurally independent of gap junctions.
* *Nervous system and tissue polarity dynamically adapt* (2020,
  PMC32882234): nerve transport drives regenerative outcomes and adapts
  even under stem-cell loss.
* *egal-1/microtubules* (2025): muscle-fiber polarity is a second
  non-junctional channel polarizing notum/wnt1 at wounds.

**Decision:** the record's innexin|head = 0.00 (no abnormality) while the
junction-only model predicts +1.00 is EXPLAINED: head-level regeneration
retains a **non-junctional neural/muscle polarity readout**. Implement M33
`neural_readout`: when active, the M25 blind-guess fallback is no longer
blind — its center is anchored to the spec value at the coordinate
(neurons/muscle tell each blastema cell what belongs there), independent of
gap_scale. Under full coupling it is inert (the guess is unused at
r >= 1.0), so all junction-intact arms stay bit-exact.

## 3. Compiler v1 — the hybrid rule: R1 writes the latch; regeneration reads the latch

**Published answers:**

* *Long-Term, Stochastic Editing of Regenerative Anatomy via Targeting
  Endogenous Bioelectric Gradients* (Pezzulo, Levin, et al. 2017,
  PMC28538159): a **temporary** bioelectric modulation permanently
  rewrites the regenerative pattern; the cryptic phenotype is
  **"stored in seemingly normal planaria via global patterns of cellular
  resting potential"** and is **"functionally instructive"** — subsequent
  regeneration reads the STORED GRADIENT, not the live appearance;
  experimental reversal of the bioelectric state resets the morphology
  back to wild-type (the switch is bidirectional).
* *A hybrid mathematical framework for morphogenesis and regeneration*
  (2026, PMC42671587): independent 2026 framework with "a **slow
  tissue-memory variable representing persistent cellular commitment**" as
  one of four coupled layers — external corroboration of the
  expression/positional/latch layering (V, theta, phi_spec, anchor) and of
  "target morphology as an attractor of coupled dynamics".

**Decision (CP-G3' resolution):** the v1 latch path was REFUTED because the
regen did not read the spec — per the 2017 paper the fix is not "make regen
read the spec", it is: **R1's sustained rewrite must WRITE the stored
gradient (the latch), and the regen then reads the latch it now carries**.
Compiled programs gain an explicit LATCH-WRITE step (phi_spec/latch target
:= spec target) before the trigger. Hybrid rule: `target = (1-blend)*latch
+ blend*spec` with the v1 adopted blend = 1.0 (the 2017 paper shows the
stored gradient dominates and is itself rewritable).

## 4. M32 — the graded rate is a MULTISTABLE SWITCH RATIO, not a dose curve

**Published answers:**

* Pezzulo/Levin 2017: perturbed trunk fragments produce "a **constant
  ratio** of two-headed to normal regenerates", "shown to be due **not to
  partial penetrance of treatment**" but to a hidden alteration — "a
  **multistable, epigenetic anatomical switch**".
* *Regenerative Adaptation to Electrochemical Perturbation* (2019,
  PMC31765995): continued exposure produces qualitatively different
  (adapted) outcomes — outcome ratios are state- and history-dependent,
  consistent with switch-like rather than graded pharmacology.
* *Stability and robustness properties of bioelectric networks* (2021,
  PMC38505634): system-level robustness — invariant patterning cues
  despite changing cell number/configuration — bounds what a per-class
  threshold may absorb.

**Decision:** the exp37 symmetric calibration signature (no-perturbation
classes undershoot, perturbation classes overshoot) is fit with a single
record-calibrated outcome threshold under a pre-registered train/held-out
split, testing whether the residual is a threshold artifact or structural
(the gene-layer case). The 2017 "constant ratio" finding predicts the
per-seed binary outcome rule is CORRECT (each animal is all-or-nothing;
the population ratio comes from the switch), which is exactly the model's
binary-threshold structure — so M32 expects a real interior optimum with
held-out improvement; a grid-edge optimum refutes M32 as registered and
strengthens the missing-gene-layer diagnosis.

## 5. The 24h window — published protocols perturb DURING REGENERATION

**Published answers:**

* Pezzulo/Levin 2017: the permanent rewrite follows "temporary modulation"
  of "amputated trunk fragments" — the perturbation window sits INSIDE the
  regenerative window, not on homeostatic intact animals.
* *Nervous system and tissue polarity dynamically adapt* (2020): the RATE
  of polarity adaptation depends on the anatomical configuration (the two
  heads regulate the rate of change) — cone width is anatomy-dependent.

**Decision (LC-G4 resolution):** the 2h-pulse light cone was measured on a
settled intact collective. The published rewrite regime is the REGEN
WINDOW: re-run the paired-trajectory light cone with the pulse delivered
while a regeneration walk is committing cells. Prediction (pre-registered):
the regen-window cone is dramatically wider — a 2 h pulse during regen
leaves a theta residue at half-chain (the commitment walk integrates the
pulse into stored identity through the M25 read), the residue persists
after regen completes, and it collapses under junction blockade. This
explains the model's own 24h sustained-forcing requirement AND the
published brief-perturbation-during-regen protocol with one mechanism.

## 6. R5 — substrate conditioning gets external corroboration

**Published answers:**

* The 2026 hybrid framework: damage is "a propagating wound signal **on
  the cellular graph**"; regenerative thresholds and attractor switching
  are graph-level phenomena — the substrate-dependence of what is an
  attractor is expected, not anomalous.
* *Stability and robustness of bioelectric networks* (2021): robustness
  ("invariant patterning despite changing anatomical configuration") is a
  DESIGN PROPERTY of some substrates — i.e., not every substrate supports
  every target partition.

**Decision:** R5 stands as registered (compiler refuses target partitions
whose boundary-to-volume ratio exceeds the substrate's calibrated limit),
now with the exp43 pass/fail signature (path/grid pass, 3-regular and
scale-free fail) as the calibration target and the 2021/2026 papers as
external precedent that substrate-conditioned pattern support is expected.

---

## Scoreboard of the directive

| Night-six item | Literature verdict | Mechanism outcome |
|---|---|---|
| M31 stored anchor | Ross 2022 constitutive+reset; egal-1 2025 material substrate | `anchor_from_history` (exp45) |
| innexin\|head | Lobo 2019 neural transport; 2025 microtubules | `neural_readout` M33 (exp46) |
| Compiler v1 | Pezzulo/Levin 2017 cryptic gradient | LATCH-WRITE rule (exp47) |
| M32 threshold | 2017 constant ratio = multistable switch | train/held-out threshold fit (exp48) |
| 24h window | 2017 perturbation during regen | regen-window light cone (exp49) |
| R5 | 2026 graph-wound framework; 2021 robustness | calibrated partition refusal (exp47) |
