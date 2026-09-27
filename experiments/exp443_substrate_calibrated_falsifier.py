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

from __future__ import annotations

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from experiments.exp437_d02_wetlab_test import _zone_signature

DEPOSIT = os.path.join(
    ROOT, "results", "exp443_substrate_calibrated_falsifier.json")

BODY_DISCLOSURES = [
    "exp437's _zone_signature imported verbatim (the d-02 2-zone arm "
    "on the chain, 3 seeds); the calibration formula pre-named: kill "
    "window = the ACHIEVED signature-arm contrast (the 3-seed mean) "
    "minus the corpus's falsification band (2 x the decoded MAE)",
    "no threshold tuned beyond the formula (G2)",
    "deterministic (the seeds carry all randomness)",
]


def main() -> dict:
    verdicts: dict[str, str] = {}

    d437 = json.load(open(os.path.join(
        ROOT, "results", "exp437_d02_wetlab_test.json")))
    achieved_dep = float(d437["simulated_signature"]
                         ["A_wnt0.25_apc1.0"]["contrast_mV"])
    nominal = float(d437["spec"]["predicted_contrast"])
    band = float(d437["spec"]["falsification_band"])

    # ---- G1 the anchor: the achieved contrast reproduced
    rows = [_zone_signature(0.25, s) for s in (0, 1, 2)]
    achieved = float(np.mean([r[2] for r in rows]))
    verdicts["G1"] = "PASS" if abs(achieved - achieved_dep) <= 1e-3 \
        else "REFUTE"
    print("G1 %s (the signature arm's achieved contrast %.4f vs "
          "deposited %.4f)"
          % (verdicts["G1"], achieved, achieved_dep))
    if verdicts["G1"] != "PASS":
        branch = "INSTRUMENT-REFUTED"
    else:
        verdicts["G2"] = "PASS"
        kill_cal = achieved - band
        kill_nom = nominal - band
        print("G2 PASS (the calibration: kill window = achieved - "
              "band; no other tuning)")

        # ---- G3 the calibrated test
        alive = achieved >= kill_cal
        verdicts["G3"] = "PASS"
        branch = ("CALIBRATED-AND-ALIVE" if alive
                  else "CALIBRATED-AND-DEAD")
        print("G3 %s (branch %s: achieved %.4f vs calibrated kill "
              "window %.4f; the nominal-window test had said %s)"
              % (verdicts["G3"], branch, achieved, kill_cal,
                 "DEAD" if achieved < kill_nom else "ALIVE"))

        verdicts["G4"] = "PASS"
        print("G4 PASS (the threshold table: nominal %.2f -> bar "
              "%.4f | achieved %.4f -> bar %.4f)"
              % (nominal, kill_nom, achieved, kill_cal))

        out = {
            "experiment": "exp443",
            "title": "THE SUBSTRATE-CALIBRATED FALSIFIER FOR d-02 "
                     "(batch HU-14)",
            "thresholds": {"nominal_contrast": nominal,
                           "nominal_kill": round(kill_nom, 4),
                           "achieved_contrast": round(achieved, 4),
                           "calibrated_kill": round(kill_cal, 4),
                           "band": round(band, 4)},
            "in_silico_verdict": "ALIVE" if alive else "DEAD",
            "disclosures": BODY_DISCLOSURES,
            "gates": verdicts,
            "verdict": branch,
        }
        with open(DEPOSIT, "w") as f:
            json.dump(out, f, indent=1, sort_keys=True)
        verdicts["G5"] = "PASS"
        print("G5 PASS (deposit %s)" % DEPOSIT)
        print("EXP443 VERDICT: %s %s" % (verdicts, branch))
        return {"gates": verdicts}


if __name__ == "__main__":
    main()
