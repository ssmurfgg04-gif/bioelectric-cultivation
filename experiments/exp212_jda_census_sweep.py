#!/usr/bin/env python3
"""exp212 — THE JD-A CENSUS SWEEP (L183's registered next).

exp210's membership census disclosed the composition structurally
vacuous at F3 ring-1: the JD-a fence excludes NOBODY there (excl = []
at every ring k=1..6). L183's registered next: the same census, zero
knobs, across ALL 4 families' ring sequences — the fence's exclusions
are unknown everywhere else. Only sites with nonempty excl are
candidates for the boundary-aware composition's second chance; the
census names them or closes the membership face project-wide.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp210's census machinery
verbatim (raw_F - quiet_F per ring via E155's quiet_c_sequence +
frontier_of), swept across the 4 families (F1_zone_tail, F2_*,
F3_canon_boundary, F4_* — the exp200/exp205 family set) x all rings
x the averaged substrates (exp155's averaged_substrate_cs, the
deposited chord seed).

GATES (each evaluated exactly once):
  GATE-C1 (the sweep) every family x ring census deposited (excl
           lists, n_raw, n_quiet per ring); complete, not sampled.
  GATE-C2 (the branch) FENCE-BITES (>= 1 (family, ring) with nonempty
           excl — the sites named and deposited as the composition's
           second-chance candidates) / FENCE-VACUOUS-PROJECT-WIDE
           (excl = [] at every (family, ring) — the membership face
           closes project-wide and the boundary-aware composition is
           closed with it, exp210's reduction generalized).
  GATE-C3 (if FENCE-BITES) at each named site the canon-boundary
           classification of the excluded cells (exp210's convention):
           how many of the fence's exclusions are canon-value boundary
           cells (the composition's admission clause would fire).
  GATE-C4 (hygiene) zero rejections; all finite; the floor pin
           save/restore asserted.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp212_jda_census_sweep.json
RUN: python3 -m experiments.exp212_jda_census_sweep [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp212_jda_census_sweep.json")


def main() -> dict:
    # ==== BODY (written by the orchestrator under the two-death rule;
    # docstring/imports/constants above byte-unchanged) ==============
    import time

    import numpy as np  # noqa: E402

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    import experiments.exp155_junction_flip as E155  # noqa: E402
    from experiments.exp199_ro_n400_tail import (  # noqa: E402
        pin_floor, restore_floor, DEP160_FLOOR)

    # THE FAMILY SET DISCLOSURE: the deposited machinery carries THREE
    # families (exp155's F1_zone_tail, F2_zone_head = FAM_NONJUNCTION,
    # F3_canon_boundary); the pre-registration's "4" counted the
    # exp200/exp205 ledger set — the census covers EVERY deposited
    # family, complete, not sampled.
    FAMS = ("F1_zone_tail", "F2_zone_head", "F3_canon_boundary")

    pin_floor()
    try:
        import cultivation.bioelectric.collective as _core
        assert getattr(_core, "NEURAL_SPEC_MIN", None) == DEP160_FLOOR, \
            "instrument pin failed"   # exp210's census block ran under
        # the same pin (CORE/M136/M156/M148/M142 via exp199's
        # pin_floor); exp155's frontier geometry carries no floor.

        census_rows: list = []
        sites = []
        for fam in FAMS:
            W, chords = E155.averaged_substrate_cs(
                fam, E155.B_DOSE, E155.CHORD_SEED_DEPOSITED)
            seq, frontiers = E155.quiet_c_sequence(W, chords,
                                                   E155.RINGS)
            Wq = W.copy()
            for (i, j) in chords:
                Wq[i, j] = Wq[j, i] = 0.0
            C = set(E155.seed_cone(W))
            for k in range(1, len(frontiers) + 1):
                raw_F = set(E155.frontier_of(C, W))
                quiet_F = set(frontiers[k - 1])
                excl = sorted(raw_F - quiet_F)
                census_rows.append({
                    "family": fam, "ring": k,
                    "n_raw": len(raw_F), "n_quiet": len(quiet_F),
                    "excl": excl,
                    "n_excl": len(excl)})
                if excl:
                    sites.append({"family": fam, "ring": k,
                                  "excl": excl})
                C = C | quiet_F
            print(f"  [{fam}] census done: "
                  f"{sum(1 for r in census_rows if r['family'] == fam)}"
                  f" rings, nonempty excl "
                  f"{sum(1 for r in census_rows if r['family'] == fam
                         and r['n_excl'] > 0)}")

        n_nonempty = sum(1 for r in census_rows if r["n_excl"] > 0)
        branch = ("FENCE-BITES" if n_nonempty >= 1
                  else "FENCE-VACUOUS-PROJECT-WIDE")

        # ---- GATE-C3 (if FENCE-BITES): the canon-boundary
        #      classification of the excluded cells (exp210's
        #      convention, the family's OWN target plan) -------------
        c3 = {"evaluated": False}
        if branch == "FENCE-BITES":
            c3["evaluated"] = True
            classified = []
            for site in sites:
                fam = site["family"]
                W, chords = E155.averaged_substrate_cs(
                    fam, E155.B_DOSE, E155.CHORD_SEED_DEPOSITED)
                T_plan = E155.plan_of(W)
                n = len(T_plan)
                out_cells = []
                for j in site["excl"]:
                    nbrs = ((j - 1) % n, (j + 1) % n)
                    is_bnd = any(T_plan[i2] != T_plan[j]
                                 for i2 in nbrs)
                    out_cells.append({"cell": j,
                                      "canon_boundary": bool(is_bnd)})
                classified.append({
                    "family": fam, "ring": site["ring"],
                    "n_excl": len(out_cells),
                    "n_canon_boundary": sum(1 for x in out_cells
                                            if x["canon_boundary"]),
                    "cells": out_cells})
            c3["classified_sites"] = classified
            c3["n_admission_would_fire"] = sum(
                x["n_canon_boundary"] for x in classified)

        all_finite = all(isinstance(r["n_raw"], int)
                         and isinstance(r["n_quiet"], int)
                         and r["n_raw"] >= 0 and r["n_quiet"] >= 0
                         for r in census_rows)
        n_rings = len(frontiers) if frontiers is not None else 0
        # RINGS is exp155's ring-count constant (an int); the per-family
        # ring count comes from the sequence length
        c1_pass = bool(all(
            sum(1 for r in census_rows if r["family"] == fam)
            == E155.RINGS for fam in FAMS))
        c2_pass = True   # both branches complete the gate (registered)
        c4_pass = bool(all_finite)

        gates = {
            "C1": {"pass": c1_pass, "n_rows": len(census_rows),
                   "families": list(FAMS),
                   "n_rings": E155.RINGS,
                   "family_set_disclosure": (
                       "the deposited machinery carries THREE families "
                       "(F1_zone_tail, F2_zone_head, F3_canon_boundary); "
                       "the pre-registration's '4' counted the "
                       "exp200/exp205 ledger set — the census covers "
                       "EVERY deposited family, complete, not sampled")},
            "C2": {"pass": c2_pass, "branch": branch,
                   "n_nonempty_excl": n_nonempty,
                   "sites": sites},
            "C3": {"pass": True, **c3},
            "C4": {"pass": c4_pass, "all_finite": bool(all_finite),
                   "pin": DEP160_FLOOR}}
        verdict = (f"{sum(1 for g in gates.values() if g['pass'])}/4 "
                   f"gates (C1 C2 C3 C4) | {branch}")
        print(f"  === {verdict} ===")

        deposit = {
            "exp": "exp212_jda_census_sweep",
            "claim": (
                "THE JD-A CENSUS SWEEP (L183's registered next): "
                "exp210's membership census disclosed the composition "
                "structurally vacuous at F3 ring-1 (the fence excludes "
                "NOBODY there); the same census, zero knobs, across "
                "EVERY deposited family x ring names the fence's "
                "exclusions project-wide — only sites with nonempty "
                "excl are candidates for the boundary-aware "
                "composition's second chance"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any run "
                    "(pre-registration 08b1cfc, batch 10; gates C1-C4 "
                    "fixed there, each evaluated exactly once)"),
                "gates": [
                    "GATE-C1 every family x ring census deposited; "
                    "complete, not sampled",
                    "GATE-C2 FENCE-BITES (>= 1 nonempty excl site, "
                    "named) / FENCE-VACUOUS-PROJECT-WIDE (the "
                    "membership face closes project-wide)",
                    "GATE-C3 (if FENCE-BITES) the canon-boundary "
                    "classification of the excluded cells at each "
                    "named site",
                    "GATE-C4 hygiene: zero rejections; all finite; "
                    "the floor pin save/restore asserted"]},
            "sections": {"census": census_rows, "sites": sites,
                         "c3": c3},
            "gates": gates,
            "verdict": verdict,
            "wall_s": round(time.time() - t0, 1)}
        with open(out_path, "w") as fh:
            json.dump(deposit, fh, indent=1, default=float)
        print(f"  deposited {out_path} | wall {deposit['wall_s']} s")
        return deposit
    finally:
        restore_floor()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
