# Night nine research — the Saito geometry and the corrected fire rule

## 1. Saito et al. 2003 FULL ABSTRACT RETRIEVED (the M-sheet repair's primary source)

DOI 10.1002/dvdy.10246 (Dev Dyn; PMID 12557211). Europe PMC resultType=core,
2026-09-15. OpenAccess status: BRONZE (Wiley pdfdirect bot-blocked; the
abstract retrieved complete via Europe PMC REST is the load-bearing text —
every geometric claim used below is verbatim from it).

> "We investigated how planarians organize their left-right axis by using
> ectopic grafting. [...] When a small piece is implanted into an ectopic
> region along the A-P and D-V axes, intercalary structures are always
> formed to compensate for positional gaps. There are two hypotheses
> regarding L-R axis formation in this organism: first, that the left and
> right sides of the animal may be recognized as different parts, and L-R
> intercalation can induce midline structures (**asymmetry hypothesis**);
> second, that both sides may have symmetrical positional values, and
> mediolateral (M-L) intercalation creates positional values along the L-R
> axis (**symmetry hypothesis**). [...] **A left lateral fragment containing
> a left auricle was implanted into the medial region of the host. Ectopic
> structures were always formed only on the left side of the graft, where
> lateral tissues abutted onto the medial tissues. However, no morphologic
> change was induced on the right side of the graft, where left-sided
> tissues faced onto right-sided tissues.** Molecular marker analyses
> indicated that ectopic structures formed on the left side of the graft
> were induced by M-L intercalation, supporting the "symmetry hypothesis."
> **When the midline tissues were implanted into a lateral region, they
> induced a complete ectopic head**, demonstrating that M-L intercalation
> may be sufficient to establish the L-R axis in planarians."

## 2. THE CORRECTED FIRE RULE (this inverts exp55's encoding)

Decode the three published junctions in the sheet's ML-field coordinates
(negative = left, 0 = midline, positive = right):

| Published junction | ML values in contact | Result |
|---|---|---|
| graft outer-lateral \| host medial (the graft's "left side") | same sign (both < 0), large gap (missing intermediate same-side values) | **ECTOPIC STRUCTURES** (M-L intercalation) |
| graft inner (left) \| host right medial ("left-sided tissues faced onto right-sided tissues") | opposite signs | **SILENT — no morphologic change** |
| midline donor (contains 0) \| host lateral | same-sign gap medial→lateral with the donor carrying the 0 source | **COMPLETE ECTOPIC HEAD** |

exp55's `intercalate()` fires on OPPOSITE-SIGN zero-crossing discontinuities
and is silent on same-sign gaps — **it encodes the asymmetry hypothesis,
which is precisely the hypothesis Saito refuted.** The corrected rule:

  FIRE:   same-sign ML juxtaposition with |ΔML| above the physiological
          adjacent gradient — missing intermediate same-side positional
          values are re-created by intercalation.
  SILENT: opposite-sign (L-R facing) contact, structurally, at ANY contrast
          — the axis can only be re-established BY the midline source
          itself (the midline-implant result), never by L-R contact.

This single correction also subsumes exp55's D1 fix (the native midline
zero-crossing becomes structurally silent — no discontinuity-threshold
exception needed for it anymore; the threshold now guards the same-sign
physiological ramp instead).

## 3. The M-sheet repair mechanism (registered in exp55's L36, now concretized)

1. **Same-sign intercalation fire rule** (above) — the front.
2. **Commitment at the front** — an exposure integrator
   E ← (1−leak)·E + drive; commitment fires at E ≥ budget_commit
   (the ZENODO:18358611 exposure axis; the budget maps exp54's published
   3h/6h window: T_onset = (3/6)·400 = 200 steps at the frozen-front drive).
3. **Inheritance-copy propagation** — while the originating front stays
   above budget_copy (half of budget_commit), committed cells copy their
   committed value to uncommitted neighbors at a fixed cadence
   (the exp27 chain commitment walk in 2D). Front death stops propagation —
   "source-dead fronts die first" (S4) vs "blending fronts stall" (S2) vs
   "frozen fronts sustain" (S1).
4. **Committed cells' AP pinned** at the committed value — the attractor
   that answers exp55's D2 diagnosis (pure diffusion cannot HOLD identity).

Parameter derivation (fixed before the arms run — no outcome peeking):
drive = drive_gain × excess (excess = |ΔML| − thresh); the exp55 geometry's
junction contrasts are computable from the field alone: S1 junction 0.36,
S2 junction 0.82 → drives 0.18 / 0.41 per step at gain 0.5. Budget_commit
= 30 (frozen front commits at ~167 steps ≤ 200 = the mapped T_onset, 1.2×
margin; blending fronts integrate ≈ 17 (S2) and ≈ 9 (S4) under contrast
decay tau ≈ L²/(π²D) ≈ 50 steps — both stall below 30). budget_copy = 15
(half — S2's front decays through it after ~1-2 copies; S4 never reaches
it). cadence = 20 (5-wide graft fills in ≤ 200 steps after commit — 2×
margin inside the 400-step window). leak = 0.01.

## 4. Re-registered gates (sides corrected; the flip is a prediction)

MSh-G1 complete ectopic head (graft fraction ≥ 0.8) — frozen-source front.
MSh-G2 local one-sided induction — side RE-REGISTERED to LEFT (the
   host-medial abutment side) vs exp55's right: the flip follows from the
   corrected geometry and matches the published figure. |L−R| ≥ 0.2,
   overall ≤ 0.6.
MSh-G3 isograft control ≤ 0.1.  MSh-G4 source load-bearing (S1−S4 ≥ 0.3).
MSh-G5 native-axis integrity ≥ 0.9 everywhere.
MSh-G6 (new) propagation-depth ordering: full > local > none.
MSh-G7 (new, the Saito silent-junction test): ZERO committed cells at the
   opposite-sign junction in S2 — the refuted-asymmetry-hypothesis rule,
   now structurally silent in the model.

## 5. M35 ARZ anchor (verbatim, MED42172041) and the night-nine target

The 4D atlas: "injury-induced spatial domain termed the anterior
regenerative zone"; "Mediator 8 is a critical regulator" — a DOMAIN, not a
gradient; multi-lineage convergence at the face. M35 (registered in the
night-eight synthesis): a wound-proximal zone readout whose identity source
is the convergence of the fragment's stored identity repertoire at the
face, targeting the corpus residual gj_block|head 0.177 (sim 0.00) WITHOUT
a free failure knob — the domain's convergence signal carries a
junction-dependent component (the multi-lineage convergence is junctional
in the model's M25 semantics), so blockade degrades the readout PARTIALLY
instead of leaving it untouched: graded residual penetrance, not zero.
