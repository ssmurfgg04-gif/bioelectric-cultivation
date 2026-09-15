# Novel-prediction registry — Stage 2 (QUEST task 6)

Forward-looking, falsifiable predictions deposited from the current model
(M25 coupling-dependent readout + M26c two-face regrowth + M27b chain
commitment diffusion). These are NOT validations — each is untested
against the record (the PlanformDB cell is empty) and carries a
pre-registered falsification threshold. Protocol: seeds (1,2,3), window
24h dt=0.1, thresholds unchanged (abnormal iff pattern error >= 6.0 mV OR
head-likeness(tail) >= 0.7); recorded metric for any future series:
Num-weighted mean of 1 - freq(WT) over RegenPeriod>0 result sets.

## Deposits (results/exp35_novel_predictions.json)

| Cell | Sim prediction | Falsification threshold |
|---|---|---|
| ion_channel\|head_tail | 1.00 abnormal (err 9.55 mV) | series mean <= 0.10 refutes; >= 0.50 confirms |
| ion_channel\|crosspiece | 1.00 abnormal (err 35.37 mV) | same |
| innexin\|head_tail | 1.00 abnormal (err 10.44 mV) | same |
| gj_block\|crosspiece | 1.00 abnormal (err 12.78 mV) | same |
| morphogen\|crosspiece | **0.00 abnormal (err 4.40 mV)** — the crosspiece cut at f~0.42 REMOVES the re-specified posterior quarter; the model predicts wnt loss is harmless at this plane | series mean >= 0.50 refutes; <= 0.10 confirms |
| cutting\|lateral | STRUCTURAL GAP — 2D cuts not representable on the 1D AP sheet | n/a |

The morphogen|crosspiece deposit is the sharpest one: it is a
plane-SPECIFIC null prediction from the re-specification mechanism
itself — wnt/beta-catenin RNAi should be fully compensated when the
manipulation removes the corrupted territory. Any future crosspiece x
wnt experiment series with high abnormality refutes the mechanism's
spatial logic, not just a parameter.

## Refutation candidates (recorded cells the model had never faced)

- **innexin\|head: recorded 0.00 (n=2) vs sim 1.00 — gap +1.00.** Head
  regeneration under junction loss is fully protected in the record
  while tail (0.40) and trunk (0.60) suffer. The M25 blind-guess
  corruption is plane-agnostic — a HEAD-SPECIFIC readout channel
  (geometry, wound-face orientation, or non-junction positional signal)
  is missing. Highest-priority repair candidate.
- **ion_channel\|trunk: recorded 0.46 (n=60) vs sim 0.00 — gap -0.46.**
  The M27b chain-diffusion mapping (cns=3, diffusion=1.5) crosses the
  abnormality threshold at the tail-plane readout but not at trunk:
  the calibration is plane-sensitive. Night-four dose scan (cns x
  diffusion grid) queued.

## Interpretation

The two refutation candidates share a theme: the model's corruption
mechanisms are plane-blind where the record is plane-aware (head
protection under junction loss; trunk sensitivity under channel loss).
Both point at the same structural upgrade — the M28 dual-field
candidate (theta expression + phi positional map) plus plane-dependent
readout gains — registered in docs/FALSIFICATION.md L17 and the
night-four queue.

## Night six/seven deposits (exp49/exp52)

### ND-L34-directional-cone (exp49 G5; the sharpest new deposit)

**Claim.** Regeneration-window bioelectric perturbations rewrite the
regenerate ONLY from wound-adjacent sites. In the model: a 2h pulse at
the wound face DURING the commitment walk shifts the whole regenerate's
stored identity (far-end theta residue 2.44 mV); the identical pulse 5
cells anterior shifts nothing (0.00). The regen-window cone is aligned
with the commitment direction — it spans the regenerate forward from
the face and is razor-narrow backward.

**Protocol.** Planarian regeneration with matched-dose
illumination/depolarization at two sites during the regeneration
window: wound-adjacent vs body-far (plus sham). Prediction:
wound-adjacent raises the ectopic/abnormal phenotype rate relative to
sham; body-far does not differ from sham.

**Falsification.** Body-far perturbation matching wound-adjacent's
effect size (phenotype-rate difference >= half the wound-adjacent
effect at n>=10/group) refutes the directional-cone claim and the
commitment-walk propagation mechanism (M25 read riding the write).

**Status.** Model-verified (exp49: face 2.44 vs 5-anterior 0.00,
3/3 seeds, junction-carried, persists 15h). Untested in vivo —
deposit registered 2026-09-15.

### ND-L34-gene-layer-generic (exp51 N1)

A generic gene-RNAi perturbation (partial homeostatic impairment:
gamma x0.7 + commitment diffusion 1.5, WITHOUT ion-channel specificity)
predicts trunk-cut abnormality at rate 0.22-0.67 (sim: 0.67 at 3
seeds). Tested when PlanformDB's other_rnai experiments get gene
identities mapped per experiment: mapped series outside the band at
n>=6 falsifies the generic-layer abstraction and demands per-gene
mechanisms.

### ND-L34-m33x34-chain (exp51 N2; chained)

Under generic gene impairment WITH junction blockade: head cuts stay
0.00 abnormal WITH the neural/muscle polarity channel (anterior-pole
protection survives generic gene impairment); tail cuts go abnormal
(sim: 1.00). Falsified if impaired+blocked head cuts behave like
blocked tails at n>=6.
