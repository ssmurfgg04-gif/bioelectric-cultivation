# Quest: Stage 2 validation against already-published experiments

The wet lab already happened. PlanformDB 2.5.0 (in-repo:
`data/planform/planformDB_2.5.0.edb`, Lobo et al. 2013) carries **1,716
recorded experiments** — cutting manipulations, RNAi targets, drugs, and
resultant morphologies **with frequencies** — across 119 publications. Levin
lab's 20+ years of published voltage patterns and dose-response curves, the
Chinese planarian literature (`research/chinese_literature.json`), and the
PSCA single-cell atlas (access probed in `research/task10_sweep/`) extend it.
Stage 2 is: **prove the model predicts the recorded outcomes.** Zero lab
cost. Pure computation.

## The pilot is already run (exp27) — and it produced the first diagnostic

`experiments/exp27_stage2_pilot.py` pre-registered four criteria, then ran
the actual simulator against the cutting + innexin slice (558 experiments):

| Criterion | Result |
|---|---|
| S2P1 ordering (innexin worse than cutting, sim + recorded) | **REFUTED** |
| S2P2 cutting mapping (sim WT, recorded WT-majority) | PASS (marginal: 0.487) |
| S2P3 class match rate (exploratory) | 0.50 |
| S2C restored-block control (T1.1c consistency) | PASS |

The negative is the payload: **sustained gap-junction loss during
regeneration does NOT corrupt the model's regeneration outcome** (pattern
error 2.87 mV vs the 6.0 mV pre-registered abnormality threshold — lower
than the cutting baseline). Cell-autonomous homeostatic target memory
(`theta`) carries regeneration alone, so the model currently lacks whatever
real junction loss removes. Recorded DB says innexin RNAi is at least as
abnormal as any other perturbation class (exp21 PB1, at low power: 9
experiments from 3 publications). The model disagrees with the record.
That is a precise, falsifiable gap — night one's opening task.

## Night-one task list (DeepScientist quest)

1. **Diagnose S2P1.** Why does the 100-cell sheet regenerate correctly with
   GJs blocked at 0.05 through amputation + regrow? Candidate mechanisms to
   implement and re-test (each is a model change with a predicted signature):
   - coupling-dependent blastema pattern extension (regrow should read the
     pattern THROUGH the junction network, not from per-cell memory);
   - noise-channel coupling: regional jump corruption (exp8's regime) during
     the un-coupled regen window, with no archive verification available;
   - electrophoretic/gradient re-specification: head/tail identity cues that
     require coupling to redistribute after amputation.
2. **Re-run exp27 unchanged** (same pre-registered thresholds). S2P1 must
   flip to PASS *without* breaking S2C/S2P2 — a fix that makes everything
   abnormal is not a fix. Iterate: change model, re-run, record.
3. **Widen the slice.** Extend the mapping to the ion_channel class
   (CaV/aquaporin -> voltage-param changes) and morphogen class
   (wnt/beta-catenin -> target-polarity parameters) — exp21's classifier
   already partitions all 412 RNAi targets. Pre-register per-class mappings
   BEFORE querying outcomes, same discipline as exp27's docstring.
4. **Per-experiment variation.** Map each experiment's recorded amputation
   plane (`Region`/`RemoveAction` tables) to the amputation slice, and RNAi
   dose/duration where recorded to block level and window. This converts a
   class-level pilot into the full 1,716-experiment validation.
5. **Score, then fix, then score.** Metric per exp27: predicted vs recorded
   dominant outcome (WT vs abnormal), reported per class, per publication,
   with mean absolute error on recorded abnormality frequencies where the
   sim supports graded output.
6. **Novel predictions as byproduct.** Once validated on the recorded slice,
   enumerate model predictions for recorded-NO-data scenarios in PlanformDB
   (interventions never run). Those become the testable-claims list for the
   preprint.
7. **Preprint skeleton** in `research/`: "Computational framework validated
   against PlanformDB: predictions, refutations, and the repair list."

## Overnight loop wiring (unchanged from DEEPSCIENTIST_PLAN.md)

- Eval contract for THIS quest: `candidate model change -> exp27-style
  re-run -> (S2P1, S2C, S2P2, match rate) tuple -> scalar fitness float`.
  Float = S2P1 pass (hard gate) + class match rate - penalty for any
  previously-PASS criterion flipped.
- Seeded state: exp27 result JSON (the refutation), exp21 group stats,
  FALSIFICATION ledger. Night one starts from a known failure point, not
  from zero.
- Morning deliverable: best model diff, criteria table before/after, failure
  log. Readable in five minutes.

## Honest bounds

- Publication bias: experiments are recorded because something happened;
  absolute recorded abnormality runs hot (cutting is 0.487, ~coin-flip).
  Orderings and per-class contrasts are the real signal, not absolute rates.
- Power: innexin slice is 9 experiments from 3 publications. The verdict
  available tonight is "model contradicts the record at this slice" — the
  repair list matters more than the p-value.
- The sim is a 100-cell species-agnostic sheet; the DB spans species
  (S. mediterranea, D. japonica, G. tigrina). Cross-species mapping is
  deliberately out of scope for night one.
