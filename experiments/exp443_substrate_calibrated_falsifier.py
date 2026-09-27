#!/usr/bin/env python3
"""exp443 — THE SUBSTRATE-CALIBRATED FALSIFIER FOR d-02 (batch HU-14;
exp437's pre-named repair). exp437 deposited the minimal falsifiable
wet-lab test and exposed the in-silico tension: the sim's arms land
at contrast 7.41-7.86 mV, below the 9.42 bar derived from exp416's
NOMINAL 10.0 — the falsifier must be calibrated to the substrate's
ACHIEVED contrast. HYPOTHESIS: the calibrated falsifier (the
signature arm's achieved 3-seed mean contrast 7.41 plus/minus the
corpus's falsification band 0.58 -> the kill window < 6.83) remains
MINIMAL and FALSIFIABLE, and the d-02 claim survives its own
calibrated test in silico.

THE INSTRUMENT (exp437's machinery verbatim; the calibration as the
repair): re-run the signature arm's 3-seed contrast (the G1 anchor:
7.41 reproduced), the calibrated kill window = achieved - band; the
arm table re-deposited with the calibrated threshold; the d-02
claim's in-silico test evaluated against the calibrated window.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the anchor: exp437's deposited signature-arm contrast
      reproduced within 1e-3 (fail=STOP).
  G2  the discipline: the calibration uses the ACHIEVED contrast
      (not the nominal) and the SAME corpus band; no threshold
      tuned beyond the pre-named formula.
  G3  THE CALIBRATED TEST: the d-02 claim SURVIVES the calibrated
      in-silico test (the signature arm's contrast >= the kill
      window — CALIBRATED-AND-ALIVE) or does not (CALIBRATED-AND-
      DEAD — the d-02 mechanism is falsified in silico, deposited
      honestly: the wet-lab test then targets the residual).
  G4  the anatomy: the (nominal, achieved, calibrated-window)
      threshold table + the full arm signature re-deposited.
  G5  deposit results/exp443_substrate_calibrated_falsifier.json.

BRANCH LATTICE: CALIBRATED-AND-ALIVE / CALIBRATED-AND-DEAD /
INSTRUMENT-REFUTED.
"""
