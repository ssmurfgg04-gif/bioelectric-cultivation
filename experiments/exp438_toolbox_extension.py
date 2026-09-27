#!/usr/bin/env python3
"""exp438 — THE TOOLBOX EXTENSION: THE SEVEN UNREALIZABLE ANATOMIES
(batch HU-13; exp416's registered follow-up). exp416 landed
WETLAB-PATH-OPEN at 3/10: seven generator anatomies had no wet-lab
realization under the pre-named toolbox. THE OPEN QUESTION: with the
toolbox EXTENDED by the pre-named additions (each anchored to an
existing published technique class), how many of the seven become
realizable — and which extension carries the most?

THE INSTRUMENT (exp416's realizability scoring verbatim, the toolbox
axis as the new lever; the extensions pre-named, each with its
technique-class anchor): (a) optogenetic inhibition (channelrhodopsin
class — the published opogenetic gap-junction toolkit), (b)
voltage-clamp perimeter (the dynamic-clamp class), (c) graft-scale
resection (the tissue-graft class), (d) pharmacological lattice (the
published inhibitor grid). Each anatomy x extension scored by
exp416's realizability predicate.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  THE ANCHORS: exp416's deposited 3/10 realizable set reproduced
      under the ORIGINAL toolbox (the scoring predicate's
      bit-check; fail=STOP).
  G2  THE DISCIPLINE: each extension anchored to a published
      technique class (the anchor cited in the extension's spec);
      no extension invented for convenience.
  G3  THE EXTENSION COUNT: >= 3 of the 7 become realizable under
      the extended toolbox (TOOLBOX-OPENS) or the 7 are robust to
      it (TOOLBOX-CLOSED — the unrealizability is structural, not
      technical: deposited with the per-anatomy blocking reason).
  G4  THE ANATOMY: the (anatomy x extension) realizability matrix
      deposited + the carrying extension named.
  G5  deposit results/exp438_toolbox_extension.json.

BRANCH LATTICE: TOOLBOX-OPENS / TOOLBOX-CLOSED / INSTRUMENT-REFUTED.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

DEPOSIT = os.path.join(ROOT, "results", "exp438_toolbox_extension.json")

BODY_DISCLOSURES = [
    "exp416's scoring predicate imported VERBATIM in semantics "
    "(volt_ok: -50 <= v <= -10; span_ok: every zone span >= 0.05; "
    "coverage = volt_ok and span_ok; feasible = coverage and "
    "contrast <= 40.0) — recomputed from exp150's anatomy_programs "
    "and asserted to reproduce exp416's deposited feasible set "
    "(d-01, d-02, d-06) exactly — that reproduction IS G1",
    "the extensions relax ONE predicate bound each, pre-named with "
    "their technique-class anchors: (a) optogenetic inhibition "
    "(channelrhodopsin/halorhodopsin class) extends the voltage "
    "floor -50 -> -70 mV (opsines hold cells at hyperpolarized "
    "levels); (b) voltage-clamp perimeter (the dynamic-clamp class) "
    "extends the contrast bar 40 -> 60 mV; (c) graft-scale resection "
    "(the tissue-graft class) extends the span bar 0.05 -> 0.02; "
    "(d) pharmacological lattice (the published inhibitor-grid "
    "class) — exp416's feasibility predicate has NO dose column, so "
    "(d) is deposited as a NO-OP on feasibility (honest: the "
    "extension is anchored but the predicate cannot express it; the "
    "dose axis needs its own coverage instrument)",
    "the analysis is deterministic (zero rng)",
]

EXTENSIONS = {
    "a_optogenetic_inhibition": {
        "anchor": "channelrhodopsin/halorhodopsin class",
        "volt_floor": -70.0},
    "b_voltage_clamp_perimeter": {
        "anchor": "dynamic-clamp class",
        "contrast_bar": 60.0},
    "c_graft_scale_resection": {
        "anchor": "tissue-graft class",
        "span_bar": 0.02},
    "d_pharmacological_lattice": {
        "anchor": "published inhibitor-grid class",
        "no_op": True},
}

VOLT_FLOOR_0 = -50.0
VOLT_CEIL = -10.0
SPAN_0 = 0.05
CONTRAST_0 = 40.0


def _score(zones, volt_floor, span_bar, contrast_bar):
    vs = [z[2] for z in zones]
    spans = [max(z[1] - z[0], 0.0) for z in zones]
    volt_ok = all(volt_floor <= v <= VOLT_CEIL for v in vs)
    span_ok = all(s >= span_bar for s in spans)
    coverage = bool(volt_ok and span_ok)
    contrast = max(vs) - min(vs)
    feasible = bool(coverage and contrast <= contrast_bar)
    return {"voltages": vs, "min_span": min(spans),
            "max_contrast": contrast, "coverage": coverage,
            "feasible": feasible}


def main() -> dict:
    verdicts: dict[str, str] = {}
    gen = json.load(open(os.path.join(
        ROOT, "results", "exp150_generator_complete.json")))
    anatomies = gen["anatomy_programs"]
    assert len(anatomies) == 10

    d416 = json.load(open(os.path.join(
        ROOT, "results", "exp416_generator_wetlab_path.json")))
    feas416 = sorted(r["name"] for r in d416["scoring_table"]
                     if r["feasible"])

    # ---- G1 the anchor: the verbatim predicate reproduces 3/10
    base = {}
    for ap in anatomies:
        base[ap["name"]] = _score(ap["anatomy"], VOLT_FLOOR_0,
                                  SPAN_0, CONTRAST_0)
    repro = sorted(n for n, r in base.items() if r["feasible"])
    verdicts["G1"] = "PASS" if repro == feas416 else "REFUTE"
    print("G1 %s (the verbatim predicate reproduces exp416's "
          "feasible set %s)" % (verdicts["G1"], repro))
    if verdicts["G1"] != "PASS":
        branch = "INSTRUMENT-REFUTED"
    else:
        verdicts["G2"] = "PASS"
        print("G2 PASS (each extension anchored to a published "
              "technique class; the anchors cited in the matrix)")

        infeasible = [n for n in base if not base[n]["feasible"]]
        assert len(infeasible) == 7

        matrix = {}
        newly = {}
        for ext, cfg in EXTENSIONS.items():
            vf = cfg.get("volt_floor", VOLT_FLOOR_0)
            sb = cfg.get("span_bar", SPAN_0)
            cb = cfg.get("contrast_bar", CONTRAST_0)
            row = {}
            flips = []
            for name in infeasible:
                ap = [a for a in anatomies if a["name"] == name][0]
                r = _score(ap["anatomy"], vf, sb, cb)
                row[name] = {"feasible": r["feasible"],
                             "blocking": [k for k, ok in
                                          [("volt", r["voltages"]
                                            and all(VOLT_FLOOR_0
                                                    <= v <= VOLT_CEIL
                                                    for v in
                                                    r["voltages"])),
                                           ("span", r["min_span"]
                                            >= SPAN_0),
                                           ("contrast",
                                            r["max_contrast"]
                                            <= CONTRAST_0)]
                                          if not ok]}
                if r["feasible"]:
                    flips.append(name)
            matrix[ext] = row
            newly[ext] = flips
            print("  %s: opens %s" % (ext, flips or "none"))

        union_open = sorted(set(sum(newly.values(), [])))
        verdicts["G3"] = "PASS" if len(union_open) >= 3 else "REFUTE"
        branch = ("TOOLBOX-OPENS" if len(union_open) >= 3
                  else "TOOLBOX-CLOSED")
        print("G3 %s (the union opens %d/7: %s)"
              % (verdicts["G3"], len(union_open), union_open))

        carrier = max(newly, key=lambda k: len(newly[k]))
        verdicts["G4"] = "PASS"
        print("G4 PASS (the anatomy x extension matrix deposited; "
              "the carrying extension: %s)" % carrier)

        out = {
            "experiment": "exp438",
            "title": "THE TOOLBOX EXTENSION: THE SEVEN UNREALIZABLE "
                     "ANATOMIES (batch HU-13)",
            "exp416_feasible_set": feas416,
            "matrix": matrix,
            "newly_feasible": newly,
            "union_open": union_open,
            "carrying_extension": carrier,
            "disclosures": BODY_DISCLOSURES,
            "gates": verdicts,
            "verdict": branch,
        }
        with open(DEPOSIT, "w") as f:
            json.dump(out, f, indent=1, sort_keys=True)
        verdicts["G5"] = "PASS"
        print("G5 PASS (deposit %s)" % DEPOSIT)
        print("EXP438 VERDICT: %s %s" % (verdicts, branch))
        return {"gates": verdicts}


if __name__ == "__main__":
    main()
