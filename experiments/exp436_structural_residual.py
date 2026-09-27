#!/usr/bin/env python3
"""exp436 — THE STRUCTURAL RESIDUAL'S SHAPE, AND THE MODEL CHANGE
(batch HU-13; exp430's registered follow-up). exp430 landed
STRUCTURAL-COMPLETE: the sign clustering survives every bias key
(|z| 4.659 at the best MAE rung 0.2282; the limiting k-NN bias RAISES
|z| to 6.817) — the bias program is closed, the decode's defect is
its FORM. THE OPEN QUESTION: what shape is the residual, and does
the pre-named model change — a TWO-COMPONENT decode that predicts
the level and the sign flip separately — absorb it where no bias
could?

THE INSTRUMENT (exp428/430's corpus/split verbatim; the
characterization first, the model change second):
  the characterization (deposited, ungated): the residual's sign
  runs vs the corpus order; the residual's distribution per
  recorded_corrected level (the decode's own targets are
  4-level); the residual's dose dependence (|residual| vs
  recorded_corrected).
  THE MODEL CHANGE (the gate): sim' = sim - b_twokey -
  DELTA * 1[model flips], where the flip component is a
  train-fit logistic on the corpus's own fields (the SAME fields
  the bias keys used — the model differs in FORM, not in inputs:
  it may fit sign, not just shift level). No new fields.
PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the anchors: exp430's deposited ladder reproduced bit-exactly
      (the two-key rung 0.2317 / |z| 5.145; fail=STOP).
  G2  the discipline: train-only fit (the logistic's train rows
      only); the same even/odd split; zero new fields (the flip
      features = group, plane, species, cut_f, ap_morphogen
      one-hot).
  G3  THE MODEL CHANGE: the two-component decode cuts |z| below 3.0
      two-sided AND holds test MAE <= 0.2402 (MODEL-CHANGE-ABSORBS);
      |z| < 3.0 but MAE > 0.2402 (ABSORBS-DEARLY); |z| >= 3.0
      (MODEL-CHANGE-FAILS — the residual survives even the form
      change; the decode program's terminal state).
  G4  the anatomy: the characterization tables + the flip component's
      coefficients + the MAE/z anatomy deposited.
  G5  deposit results/exp436_structural_residual.json.

BRANCH LATTICE: MODEL-CHANGE-ABSORBS / ABSORBS-DEARLY /
MODEL-CHANGE-FAILS / INSTRUMENT-REFUTED.
"""
