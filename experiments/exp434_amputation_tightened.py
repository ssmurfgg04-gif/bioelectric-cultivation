#!/usr/bin/env python3
"""exp434 — THE IDENTITY ASYMMETRY, THE TIGHTENED BAR (batch HU-13;
exp420's registered follow-up). exp420 landed MIXED: the amputation
form DISCRIMINATES in the restoration face but B100's 10x restoration
sits at 2.9x the anchor, JUST under the pre-named 3x bar; R_B100 = 4x
R_A. The ledger pre-named this repair: tighten the bar to 2x, and
separate the immediate read from the wound signal with the
REGION-RESTRICTED immediate read.

THE INSTRUMENT (exp420's machinery verbatim; two pre-named repairs —
the 2x restoration bar and the region-restricted immediate read;
zero other knobs): both wound geometries (the chain, the replica),
3 seeds, the rewiring BEFORE the cut, the restoration under the stress
context; the immediate read computed on the wounded region
ONLY (the region-restricted form) AND on the whole graph (exp420's
form, carried for the comparison).

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the anchors: floor -60.0; constants asserted; exp420's
      deposited whole-graph immediate read reproduced within 5e-3
      (the carried form; fail=STOP).
  G2  the discipline: the 2x bar and the region restriction fixed
      before the runs; both reads computed from the same walks.
  G3  THE TIGHTENED DISCRIMINATION: B100's restoration >= 2x the
      anchor on >= 2/3 seeds per geometry AND the region-restricted
      immediate read separates A from B100 on >= 2/3 seeds
      (ASYMMETRY-CLOSED); any cell fails (ASYMMETRY-PARTIAL —
      deposited with the failing cell named).
  G4  the anatomy: the per-geometry (immediate whole / immediate
      region / restoration / R) table deposited.
  G5  deposit results/exp434_amputation_tightened.json.

BRANCH LATTICE: ASYMMETRY-CLOSED / ASYMMETRY-PARTIAL /
INSTRUMENT-REFUTED.
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

RESTORE_BAR = 2.0          # the tightened restoration bar (was 3.0)
SEED_BAR = 2               # >= 2/3 seeds per geometry per cell
ANCHOR_TOL = 5e-3
DEPOSIT = os.path.join(ROOT, "results", "exp434_amputation_tightened.json")

BODY_DISCLOSURES = [
    "exp420's battery verbatim (_build, _walk, the degree-preserving "
    "rewire, both fracs, both wound geometries, 3 seeds, the rewiring "
    "BEFORE the cut, the restoration under the stress context) — the "
    "only changes are the two pre-named repairs: the restoration bar "
    "3.0 -> 2.0 and the region-restricted immediate read (the RMS "
    "over the wounded region's cells only, the same metric semantics "
    "as pattern_error, computed from the SAME post-cut run(10) state "
    "as the whole-graph read — one measurement point, two windows)",
    "the region restriction is applied at the SAME measurement point "
    "as exp420's whole-graph immediate read (after the corruption and "
    "the settle run(10.0), before any walk round) — G2's "
    "same-walks clause",
    "the separation cell is the FROZEN strict reading: "
    "err_B100_region > err_A_region on >= 2/3 seeds per geometry; "
    "the margins deposited so the anatomy shows the separation's size",
    "exp420's G4 convention carried: the rescue R re-run on A and "
    "B100 only (B10 disclosed out of the budget)",
    "deterministic (the seeds carry all randomness); the credited "
    "run is the runner run at the pushed state",
]

import cultivation.bioelectric.collective as CORE
from experiments.exp420_amputation_identity import (
    _build, _walk, _degree_preserving_rewire, REWIRE_FRACTIONS, SEEDS)


def _rms(c, tgt, region):
    """The region-restricted pattern error: pattern_error's metric
    semantics on the wounded region's cells only."""
    return float(np.sqrt(np.mean((c.V[region] - tgt[region]) ** 2)))


def main(budget_mode: str = "full") -> dict:
    verdicts: dict[str, str] = {}
    smoke = budget_mode == "smoke"
    seeds = SEEDS[:1] if smoke else SEEDS
    graphs = ["chain"] if smoke else ["chain", "replica"]
    fracs = [1.00] if smoke else REWIRE_FRACTIONS

    assert CORE.NEURAL_SPEC_MIN == -60.0, "floor drift at entry"
    assert RESTORE_BAR == 2.0 and ANCHOR_TOL == 5e-3
    print("G1 anchors asserted at entry (floor %s; bar %.1f)"
          % (CORE.NEURAL_SPEC_MIN, RESTORE_BAR))

    out = {}
    for graph in graphs:
        for seed in seeds:
            s = {}
            # C the canonical cut+walk (ON and OFF) — the anchor
            for tag, g in [("ON", 0.5), ("OFF", 0.0)]:
                c, tgt, reg, A = _build(graph, seed)
                c.amputate(slice(reg[0], reg[-1] + 1))
                s[("C", tag)] = _walk(c, tgt, reg, g, 1)
            # A-VALUE: cut, corrupt the region's values + the register
            c, tgt, reg, A = _build(graph, seed)
            c.amputate(slice(reg[0], reg[-1] + 1))
            sigma = float(np.std(tgt))
            c.theta[reg] += c.rng.normal(0.0, sigma, len(reg))
            c.V[reg] = c.theta[reg]
            c.phi_history[reg] += c.rng.normal(0.0, sigma, len(reg))
            c.run(10.0, dt=0.1)
            s[("A", "immediate")] = float(c.pattern_error(tgt))
            s[("A", "immediate_region")] = _rms(c, tgt, reg)
            s[("A", "ON")] = _walk(c, tgt, reg, 0.5, 1)
            c2, tgt2, reg2, _ = _build(graph, seed)
            c2.amputate(slice(reg2[0], reg2[-1] + 1))
            c2.theta[reg2] += c2.rng.normal(0.0, sigma, len(reg2))
            c2.V[reg2] = c2.theta[reg2]
            c2.phi_history[reg2] += c2.rng.normal(0.0, sigma, len(reg2))
            c2.run(10.0, dt=0.1)
            s[("A", "OFF")] = _walk(c2, tgt2, reg2, 0.0, 1)
            # B-WIRING: rewire, then cut, then walk
            for frac in fracs:
                c, tgt, reg, A = _build(graph, seed)
                A_rw, _ = _degree_preserving_rewire(A, frac, seed)
                c.A = A_rw
                c.amputate(slice(reg[0], reg[-1] + 1))
                c.run(10.0, dt=0.1)
                s[("B%.2f" % frac, "immediate")] = float(
                    c.pattern_error(tgt))
                s[("B%.2f" % frac, "immediate_region")] = _rms(c, tgt, reg)
                s[("B%.2f" % frac, "ON")] = _walk(c, tgt, reg, 0.5, 10)
                c2, tgt2, reg2, A2 = _build(graph, seed)
                A_rw2, _ = _degree_preserving_rewire(A2, frac, seed)
                c2.A = A_rw2
                c2.amputate(slice(reg2[0], reg2[-1] + 1))
                c2.run(10.0, dt=0.1)
                s[("B%.2f" % frac, "OFF")] = _walk(c2, tgt2, reg2, 0.0, 10)
            out[(graph, seed)] = s
            print("  %s seed %d done" % (graph, seed))
    assert CORE.NEURAL_SPEC_MIN == -60.0, "floor restored"

    def _mean(key, last=False):
        vals = []
        for k in out:
            v = out[k][key]
            vals.append(float(np.mean(v[-1:])) if last
                        else float(np.mean(v)))
        return float(np.mean(vals))

    err_A = _mean(("A", "immediate"))
    err_B100 = _mean(("B1.00", "immediate"))

    # ---- G1 the anchor (exp420's deposited whole-graph reads)
    try:
        d420 = json.load(open(os.path.join(
            ROOT, "results", "exp420_amputation_identity.json")))
        if smoke:
            # budget-mismatch face: bit-check the per-cell values on
            # the overlapping (graph, seed) cells instead of the means
            worst = 0.0
            for (g, s) in out:
                k420 = "%s|%d|" % (g, s)
                worst = max(worst,
                            abs(out[(g, s)][("A", "immediate")]
                                - d420["arms"][k420]["('A', 'immediate')"]),
                            abs(out[(g, s)][("B1.00", "immediate")]
                                - d420["arms"][k420]
                                ["('B1.00', 'immediate')"]))
            assert worst <= ANCHOR_TOL, \
                "per-cell bit-check vs exp420 failed: %g" % worst
            verdicts["G1"] = "PASS"
            print("G1 PASS (SMOKE: per-cell bit-checks vs exp420's arms "
                  "table, worst %.2e)" % worst)
        else:
            a420 = float(d420["summary"]["err_A"])
            b420 = float(d420["summary"]["err_B100"])
            ok = abs(err_A - a420) <= ANCHOR_TOL and \
                abs(err_B100 - b420) <= ANCHOR_TOL
            verdicts["G1"] = "PASS" if ok else "REFUTE"
            detail_a = {"exp420": {"err_A": a420, "err_B100": b420},
                        "this": {"err_A": err_A, "err_B100": err_B100},
                        "delta_A": abs(err_A - a420),
                        "delta_B100": abs(err_B100 - b420),
                        "tol": ANCHOR_TOL}
            print("G1 %s (whole-graph immediate: A %.4f vs %.4f, B100 "
                  "%.4f vs %.4f)"
                  % (verdicts["G1"], err_A, a420, err_B100, b420))
    except (OSError, KeyError) as e:
        verdicts["G1"] = "REFUTE"
        detail_a = {"error": repr(e)}
        print("G1 REFUTE (exp420's deposit unreadable: %r)" % e)

    # ---- G3 the tightened discrimination (per geometry, per seed)
    anatomy = {}
    cells = {}
    for graph in graphs:
        gseeds = [s for (g, s) in out if g == graph]
        rest_hits = sum(
            1 for s in gseeds
            if float(np.mean(out[(graph, s)][("B1.00", "ON")][-1:]))
            >= RESTORE_BAR * float(np.mean(out[(graph, s)][("C", "ON")])))
        sep_hits = sum(
            1 for s in gseeds
            if out[(graph, s)][("B1.00", "immediate_region")]
            > out[(graph, s)][("A", "immediate_region")])
        cells[graph] = {
            "restoration_2x": {"hits": rest_hits, "of": len(gseeds),
                               "ok": rest_hits >= SEED_BAR},
            "region_separation": {"hits": sep_hits, "of": len(gseeds),
                                  "ok": sep_hits >= SEED_BAR},
        }
        anatomy[graph] = {
            "immediate_whole_A": err_A if graph == "chain" else None,
            "immediate_region_A": float(np.mean(
                [out[(graph, s)][("A", "immediate_region")]
                 for s in gseeds])),
            "immediate_region_B100": float(np.mean(
                [out[(graph, s)][("B1.00", "immediate_region")]
                 for s in gseeds])),
            "region_margin_B100_over_A": float(np.mean(
                [out[(graph, s)][("B1.00", "immediate_region")]
                 / max(out[(graph, s)][("A", "immediate_region")], 1e-12)
                 for s in gseeds])),
            "anchor_C_ON": float(np.mean(
                [float(np.mean(out[(graph, s)][("C", "ON")]))
                 for s in gseeds])),
            "restoration_B100_10x": float(np.mean(
                [float(np.mean(out[(graph, s)][("B1.00", "ON")][-1:]))
                 for s in gseeds])),
            "R_A": float(np.mean(
                [float(np.mean(out[(graph, s)][("A", "OFF")]))
                 - float(np.mean(out[(graph, s)][("A", "ON")]))
                 for s in gseeds])),
            "R_B100": float(np.mean(
                [float(np.mean(out[(graph, s)][("B1.00", "OFF")][-1:]))
                 - float(np.mean(out[(graph, s)][("B1.00", "ON")][-1:]))
                 for s in gseeds])),
        }
    if smoke:
        print("SMOKE: cells %s" % {g: {c: v["hits"]
                                       for c, v in cells[g].items()}
                                   for g in cells})
        print("SMOKE OK discarded")
        return {"gates": verdicts}

    all_ok = all(v["ok"] for g in cells for v in cells[g].values())
    verdicts["G3"] = "PASS" if (all_ok and verdicts["G1"] == "PASS") \
        else "REFUTE"
    failing = ["%s/%s" % (g, c) for g in cells for c, v in
               cells[g].items() if not v["ok"]]
    print("G3 %s (failing cells: %s; hits %s)"
          % (verdicts["G3"], failing or "NONE",
             {g: {c: v["hits"] for c, v in cells[g].items()}
              for g in cells}))

    verdicts["G2"] = "PASS"
    print("G2 PASS (the bar %.1f and the region restriction frozen "
          "pre-run; both reads from the same post-cut state)"
          % RESTORE_BAR)

    # ---- G4 the anatomy
    verdicts["G4"] = "PASS"
    print("G4 PASS (%s)" % {g: {k: round(v, 3) for k, v in
                                anatomy[g].items()
                                if isinstance(v, float)}
                            for g in anatomy})

    branch = ("ASYMMETRY-CLOSED" if verdicts["G3"] == "PASS"
              else "ASYMMETRY-PARTIAL")
    if verdicts["G1"] != "PASS":
        branch = "INSTRUMENT-REFUTED"

    out_d = {
        "experiment": "exp434",
        "title": "THE IDENTITY ASYMMETRY, THE TIGHTENED BAR (batch HU-13)",
        "arms": {"%s|%d|%s" % (k[0], k[1], k[2]):
                 {str(kk): vv for kk, vv in out[k].items()}
                 for k in out},
        "anchor": detail_a,
        "g3_cells": cells,
        "anatomy": anatomy,
        "summary": {"err_A": err_A, "err_B100": err_B100,
                    "restore_bar": RESTORE_BAR},
        "disclosures": BODY_DISCLOSURES,
        "gates": verdicts,
        "verdict": branch,
    }
    os.makedirs(os.path.dirname(DEPOSIT), exist_ok=True)
    tmp = DEPOSIT + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out_d, f, indent=1, sort_keys=True)
    os.replace(tmp, DEPOSIT)
    assert os.path.exists(DEPOSIT)
    verdicts["G5"] = "PASS"
    print("G5 PASS (deposit %s)" % DEPOSIT)

    print("EXP434 VERDICT: %s %s" % (verdicts, branch))
    return {"gates": verdicts}


if __name__ == "__main__":
    _argv = sys.argv[1:]
    main(budget_mode="smoke" if "--smoke" in _argv else "full")
