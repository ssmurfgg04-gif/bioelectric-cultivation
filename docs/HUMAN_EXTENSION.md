# THE HUMAN EXTENSION — SYNTHESIS AND CLOSURE

**Batch HU-1 through HU-6 (experiments exp401–exp406; ledger L295–L301).**
**Date: 2026-09-27. Head at closure: see `git log -1` (this document was
deposited at the closure commit).**

---

## 0. THE ONE-LINE OUTCOME

> **Outcome B — PARTIAL TRANSFER.** The planarian corpus's structural
> findings transfer to real human data **in direction and shape**
> (the fidelity-stability envelope, the history register's protection,
> the two-channel gating, the deadline window), while the parametric
> details are **substrate-specific** (the composition law: super-additive
> on the planarian substrate, additive on the human substrate — agreeing
> with the human intervention literature). The model is not universal in
> its magnitudes; it is universal in its structural directions.

---

## 1. WHAT WAS TESTED

The hypothesis (handoff Section 2): the planarian project's structural
findings — the two-channel law, the history register, the composed
carrier, the deadline law — are **universal properties of bioelectric
systems**, not planarian-specific.

The test: extend the model to real human connectome and physiological
data, and check which findings transfer. No new experiments were run in
the wet-lab sense — every human-side number comes from either a **real
public dataset** or the **published literature**, exactly as the handoff
directed ("mine the data that's already been collected").

---

## 2. THE DATA MINED (all real, all committed or cited)

| Dataset | What was used | Where |
|---|---|---|
| **HCP group-average functional connectome** (Schaefer-400 parcellation; Vos de Wael et al. 2018, PNAS discovery cohort, as distributed with brainspace) | The 400×400 human graph substrate for every model run | `data/human_fc_schaefer400.npy` (sha-pinned) |
| **Sleep-EDF** (PhysioNet; subject SC4001, two consecutive nights, 100 Hz) | The real EEG for the fidelity↔stability mapping | `data/physionet/SC400[12]E0-PSG.edf` |
| **NSRDB record 16420** (PhysioNet; 24 h Holter ECG, 128 Hz, 102,067 annotated beats) | The real autonomic signal for the two-channel law | `data/physionet/16420.*` |
| **Preconditioning literature** (Murry 1986; Li 2011; Wegener 2004) | Published effect sizes for the register comparison | encoded in exp403's deposit |
| **Combined-intervention literature** (Celnik 2009 — the published 4-cell composition factorial) | The human composition class | encoded in exp404's deposit |
| **Responder-variability literature** (reviews) | The responder-fraction band [0.40, 0.60] | encoded in exp405's deposit |
| **Dose-timing literature** (Lees 2010, Lancet 375:1695–1703) | The published decay series for the deadline law | encoded in exp406's deposit |

Tier-2 applications (UK Biobank etc.) were **not** needed: the Tier-1
and literature sources already decided every gate.

---

## 3. THE MODEL EXTENSION

`human/substrate.py` — an ingestion layer, **zero core changes**
(asserted by exp401's G3: `git diff cultivation/` empty; the frozen
100-node instrument bit-exact at the anchor):

- **The preprocessing rule** (pre-registered, deterministic, nothing
  tuned): negatives → 0 (2.08% of edges, disclosed), diagonal → 0,
  per-node symmetric top-6 (the first k on the pre-named ladder
  {6, 8, 10, 12, 16} that connects 400/400), scaled to mean row-sum 0.4
  (the planarian path-regime comparability rule).
- **The dynamical parameters**: the planarian defaults everywhere. The
  human mapping enters through the **real connectivity structure only**.
  No parameter was fitted on human data. This is the honest default and
  the transfer test's teeth: if the findings hold anyway, they are
  carried by structure, not by tuning.
- **The identity target**: leading-eigenvector ordering, 5 zones × 80,
  the house ladder centers [−50, −40, −30, −20, −10] mV (synthetic
  semantics, as in the planarian corpus).
- **Bit-exactness where the parameters match** (handoff Phase 2 item 5):
  exp401's G3 anchor — the same module on the planarian path instrument
  reproduces the pre-registered reference bit-exact (err 4.3562672231;
  V[:5] digest `25d22aba033b9d9a`).

**Scale disclosure**: the handoff asked for the HCP 1,000-node
parcellation. The 1,000-parcel **labels** are distributed, but the
Tier-1 group-average FC in this distribution ships at the **400-parcel
scale**; 400 is within the model's proven range (exp230: the reader's
cost is n-invariant to 1,000). The graph face runs at 400. Honest
limitation, not a blocker.

---

## 4. THE SIX EXPERIMENTS (all pre-registered, all deposited)

| # | Experiment | Verdict | One line |
|---|---|---|---|
| exp401 | The human substrate ingestion | **HUMAN-SUBSTRATE-LIVE** (4/4) | The machinery runs on a real human connectome; settled errs 4.48–4.53 (bar 6.0), the zero-drift anchor bit-exact |
| exp402 | Fidelity ↔ EEG stability | **FIDELITY-MAPS** (5/5) | Real two-night EEG: the human pattern persists (3/4 high-power R < 0.5) and the model's drift (0.145) sits inside 2× the human's (0.429) |
| exp403 | History register ↔ preconditioning | **HISTORY-PROTECTS-HUMAN** (5/5) | On the human connectome the register saves 1.06 mV under write-time stress (harm ratio 1.14 > 1) — the preconditioning DIRECTION transfers (Murry ratio 4.0, Li 2.05; magnitude AUDIT-ONLY) |
| exp404 | Composition ↔ combined intervention | **COMPOSITION-CLASS-MATCH** (5/5) | The human graph's composition is ADDITIVE (f = −0.025) and Celnik 2009's human data is too (f = −0.072) — while the planarian super-additivity does NOT reproduce (the naive universal-transfer claim refuted on this leg) |
| exp405 | Two-channel law ↔ autonomic | **TWO-CHANNEL-MAPS** (6/6) | Real 24 h ECG: LF/HF day 3.410 > night 2.551 (the canonical shift); the voltage-gated responder sweep monotone (0.632→0.292) with vgates inside the literature band [0.40, 0.60]; the homogenization channel direction-positive but NOT significant (ρ = 0.067, p = 0.18 — disclosed) |
| exp406 | Deadline law ↔ dose-timing | **DEADLINE-MAPS** (6/6) | The model's rescue decays monotonically with delay (Spearman −1.000; τ* = 1268.8 tu finite — the deadline exists); Lees 2010's normalized effect decays 1.000→0.116 — the human window closes; SHAPE transfers, rate AUDIT-ONLY |

Every experiment: docstring pre-registration frozen before the run
(the two-commit discipline), gates evaluated exactly once, runtime body
fixes disclosed in-ledger (exp401's scalar-pin comparison; exp405's
beat-span bar), deposits in `results/`, ledger entries L295–L300.

---

## 5. THE OUTCOME DETERMINATION

**Outcome B — PARTIAL TRANSFER.** Leg by leg:

### What transfers (the structural directions)

1. **The fidelity notion** (exp402). A pattern held by a coupled
   bioelectric collective drifts at the same ORDER under matched noise
   on the human connectome as real human cortical signals drift across
   nights. Not frozen, not runaway — the same kind of quantity.
2. **The history register's protection** (exp403). The planarian
   corpus's "refinement" mechanism — a per-cell register of the last
   committed identity, blended at the commit boundary — **protects a
   pattern on a real human connectome under write-time stress**
   (P = +1.06 mV; harm ratio 1.14). The direction matches the
   preconditioning literature (prior exposure protects: Murry, Li,
   Wegener). The magnitude does not match (1.14 vs 2–4×) — the units
   differ (mV error vs infarct %) and the comparison is honest
   AUDIT-ONLY.
3. **The two-channel gating** (exp405). The voltage state gates the
   intervention (the responder fraction falls monotonically as the gate
   rises — the direction the literature's baseline-state dependency
   claims), and the model's gate ladder passes through the literature's
   responder band. The real autonomic substrate carries the two-branch
   day-night shift (LF/HF 3.41 > 2.55) on the raw record.
4. **The deadline law** (exp406). Both the model (τ* = 1268.8 tu,
   finite) and the human dose-timing data (Lees: the normalized effect
   1.000 → 0.116, gone by ~4.5–6 h) carry a **closing window**. The
   shape transfers; the rates are incommensurable units (AUDIT-ONLY).

### What does NOT transfer (the substrate-specifics)

1. **The composition law's class** (exp404). On the planarian substrate
   the composed carrier is SUPER-additive under stress (exp299). On the
   human connectome it is ADDITIVE (f = −0.025) — and the human
   intervention literature agrees (Celnik: f = −0.072). The human
   substrate and the human data cohere with each other and diverge from
   the planarian stack. **The naive universal-transfer claim is refuted
   here, and the refutation is the finding**: the composition law is
   regime/substrate-dependent, not universal.
2. **The homogenization channel's magnitude** (exp405 G5). Direction
   positive as pre-registered, but ρ = 0.067, p = 0.18 — NOT
   significant. The second channel's evidence on the human graph is
   weak; the first channel carries the transfer. Disclosed verbatim.
3. **Every magnitude and rate** (all legs). The model's numbers are in
   model units; the human numbers are in mV-drift, hours, percentages.
   No rate or magnitude comparison was allowed as a gate — the
   transfer claims that fired are direction, shape, class, and range
   claims. This restraint is deliberate: it is the honest response to
   the handoff's translation-gap warning (Section 8 of the closure
   charter).

### What remains DATA-INSUFFICIENT (Outcome D fragments inside B)

- **Per-node fidelity ↔ per-region EEG stability**: 2 scalp channels
  cannot address 400 parcels. The envelope-level test passed; the
  per-node rank-correlation test needs high-density EEG (64–256 ch) or
  iEEG linked to individual connectomes. **What would need measuring**:
  within-subject high-density EEG test-retest, per-region, with the
  subject's own structural connectome.
- **Individual-difference two-channel predictions**: the two-channel
  law predicts WHO responds from (V-ratio × θ-homogenization); testing
  that needs per-subject connectomes linked to stimulation outcomes
  (the Tier-2 applications: UK Biobank's imaging-plus-physiology
  depth). The literature band match (exp405 G4) is the cohort-level
  shadow of that test.
- **The 1,000-node face**: the group FC at the 1,000-parcel scale was
  not in the Tier-1 sources; the labels are. A 1,000-scale group
  connectome would close the scale gap.

---

## 6. THE HONEST LIMITS (the closure charter's Section 8, answered)

1. **The coarse-graining**: 400 parcels over 86 billion neurons. The
   model runs on the parcellated graph, not the tissue. The test's
   claim is correspondingly coarse: structural directions, not
   cellular mechanism.
2. **FC is functional, not structural**: the substrate is group-average
   functional connectivity. The model's "gap junctions" are an analogy
   on this substrate (disclosed at ingestion). A structural
   (dMRI-based) connectome face would strengthen the claim.
3. **The planarian defaults**: no parameter was fitted to the human
   side. This makes the transfer results meaningful — and it means the
   magnitudes are EXPECTED to be off. They are.
4. **Correlational, not causal**: every literature comparison is a
   population-level agreement, not a trial. The model does not replace
   clinical prediction and was not gated as if it could (the handoff's
   own MAE-0.290 scrutiny applies: the planarian model's remaining 29%
   error is a data-side AND model-side gap, and the human extension
   inherits both limits).
5. **The consciousness question is untouched**: the wiring-keyed
   indexation finding (the pattern lives in the wiring, not the values)
   is consistent with the human results (the structural directions
   transfer while the parametric content does not — exactly what a
   wiring-carried pattern account predicts), but nothing here bears on
   subjective experience. The zero-substrate star remains blocked at 9
   formalizations; nothing in the human data reopens it.

---

## 7. THE CLOSURE ARTIFACTS (per the closure charter)

1. **This document** — the outcome (B) and the leg-by-leg map.
2. **The ledger extension** — L295–L301 in `docs/FALSIFICATION.md`,
   same discipline as the planarian work.
3. **The model extension** — `human/substrate.py` + the six experiment
   modules, bit-exact where the parameters match.
4. **The README update** — one paragraph stating the outcome.
5. **The final push** — the closure commit.

**The hard cap**: 6 of 30 experiments used. The remaining 24 are NOT
spent on polish: the four outcomes were defined as closures, Outcome B
fired, the map is written. The cap exists to stop exactly this kind of
indefinite extension, and it is honored — see the terminal note below.

---

## 8. WHAT THE RESULT MEANS (the one-paragraph reading)

The planarian model's laws are **real properties of coupled
bioelectric collectives** to the extent that they survive transplantation
onto a real human connectome with zero re-tuning: the stability
envelope, the history-protection direction, the voltage-gated responder
structure, and the closing intervention window all hold in direction,
shape, class, or range against real human signals and the published
literature. What fails to transfer is the planarian stack's
**parametric texture** — most sharply the composition law, where the
human substrate's additivity coheres with the human intervention data
against the planarian super-additivity. The bridge is crossed in the
only sense honest measurement allows: the model's structural grammar is
species-general; its numbers are species-specific. The next real
question is not another extension — it is what fixes the composition
class (the substrate's coupling regime? the wound's stress context?
the spec layer's persistence?) — and that question is recorded, not
pursued, because the closure rule fired.
