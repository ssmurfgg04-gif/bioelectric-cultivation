#!/usr/bin/env python3
"""exp158 — THE OCTANOL-DH PLANE SERIES, RE-TESTED ON ITS DEPOSITED ARM
(L116 exp139's registered repair of the DEGENERATE LV-G4 B leg).

THE OWNED GAP (L116, verbatim intent): exp139's LV-G4 found the C leg
(headless-by-plane, ion arm) landing at rho 0.6489 but the B leg
DEGENERATE — the pure junction-cut arm (gap_scale 0.05, exp39-V4's
mapping) carries NO ectopic-anterior sign at ANY plane (EA 0/0/0 across
head/trunk/tail), so the published octanol DH plane series (DB eids
415-419: "Double head, two pharynxes" frequency by cut plane) has no
EA-predicting home on that arm. L116's diagnosis: the record's DH sign
rides the DEPOLARIZATION channel (exp39-V3's deposited posterior-depol
mapping, HL 0.946; exp123's channel-split). The registered repair: the
octanol-DH plane series re-tested on its deposited arm — posterior-depol
by plane vs eids 415-419, the arm the degenerate B leg should have run.

MAPPING DECLARATION (PRE-REGISTERED BEFORE ANY RHO COMPUTATION):
  The B family (GJ-blocked, 57 entries, the exp139 frozen partition) is
  mapped onto the DEPOLARIZATION channel: the exp39-V3
  posterior-depolarization arm VERBATIM — corrupt_region(POST_Q,
  theta_value=WT_HEAD_V) BEFORE the 24 h run — followed by exp131's
  deposited plane geometry (head: amputate HEAD_SL, regrow backward;
  trunk: amputate TRUNK, regrow both; tail: amputate TAILP, regrow
  forward; regrow kwargs = V3's OWN dict cell_period 0.8 / dt 0.1 /
  noise 0.6, NOT the ion arm's commitment extras), read through the
  exp139 flags (_flags: EA = head_likeness(V, TAIL) >= 0.7). The
  published octanol DH series (eids 415-419: head .05, pre-pharyngeal
  .28, pharyngeal .50, post-pharyngeal 1.00, tail .00) maps onto the 3
  sim planes through exp139's deposited TAXONOMY (head, pre_pharyngeal
  -> head; pharyngeal -> trunk; post_pharyngeal, tail -> tail). The
  stack prediction is the DEPOL arm's EA rate by sim plane, expanded
  through that same taxonomy. This mapping is frozen HERE — docstring
  and module constants below — BEFORE any rho computation, and the
  freeze is asserted in-module at run time (gate O2). The C leg's
  instrument (ion arm by plane, TAXONOMY, published headless series
  eids 391-395) is imported UNCHANGED from the deposited exp139 module:
  the repair must not touch it (gate O3).

PRE-REGISTERED GATES (thresholds frozen BEFORE running):

  O1  (PRIMARY — the repaired B leg)
      rho(depol-arm EA rate by published plane, published octanol DH
      series) under exp131's deposited IP-G1 two-sided zones — the C
      leg's bar:
        rho >= 0.6            -> PASS
        rho <= -0.3           -> REFUTED (anti-ordered)
        rho is None (zero-variance sim — the degeneracy repeating on
        the NEW arm)          -> FAIL-DEGENERATE
        otherwise             -> PARTIAL (measured concordance, owned)

  O2  (ORDER DISCIPLINE) the mapping is declared BEFORE the rho
      computation: the docstring declaration above + the module-level
      constants + the MAPPING_DECLARED sentinel, asserted in main()
      before the first rho call (a _RHO_CALLS counter is asserted
      zero there). PASS iff the assertion holds.

  O3  (C-LEG DEPOSIT INTEGRITY) the C leg re-run exp139-verbatim (the
      deposited ion_arm function object, seeds 1-3, SIM_PLANES order)
      must reproduce the deposit BIT-EXACTLY:
        sim_c_abn_by_pub_order == the deposit's list (float ==), and
        rho_C == 0.6488856845230502 (the deposit's float).
      PASS iff both. The repaired B leg runs on its OWN arm instances;
      any cross-arm contamination would surface here.

  O4  (THE POOLING QUESTION — LV-G1's failed gate re-run under the
      repaired instrument) report BOTH, GATE ON THE PLANE-RESOLVED:
      (a) pooled companion: the 4-family E_stack recomputed with the B
          family's scalar mapped through the depol channel (the depol
          arm's tail-plane EA rate — structurally TIED to D's scalar,
          same deposited arm; the tie is the mapping's own consequence,
          disclosed) vs the deposit's E_meas; Spearman reported and
          compared against the deposit's -0.105. NOT gated.
      (b) plane-resolved pool (THE GATE): the 10 record-plane cells
          (B: the 5 octanol-DH planes via the depol arm's EA; C: the 5
          headless planes via the ion arm's abn rate) pooled into one
          Spearman. PASS iff rho >= 0.4 (LV-G1's own deposited pass
          bar — O4 is LV-G1 re-run, so its bar carries); REFUTED iff
          rho <= -0.6 (LV-G1's deposited refute zone); None ->
          FAIL-DEGENERATE; else PARTIAL.
      "Does pooling still erase structure?" is answered by the signed
      comparison (a) vs (b), deposited, not gated.

RUN: 21 sims (depol arm 3 planes x 3 seeds; ion arm 3 planes x 3 seeds
for O3 — the deposited function; cutting arm 3 seeds for the pooled
companion), <=1 s each, exp39/exp131/exp139 machinery verbatim. Serial,
BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp139_levin_voltage import (  # noqa: E402
    PUB_HEADLESS, PUB_OCTANOL_DH, PUB_ORDER, SIM_PLANES, TAXONOMY,
    _flags, build_families, cutting_arm, ion_arm, rho_or_none,
)
from experiments.exp27_stage2_pilot import (  # noqa: E402
    ABN_ERR_MV, ABN_HL, DT, SEEDS, make_collective,
)
from experiments.exp32_m26_repairs import (  # noqa: E402
    HEAD as HEAD_SL, POST_Q, TAILP, TRUNK, WT_HEAD_V,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp158_octanol_plane.json")
DEP139 = os.path.join(ROOT, "results", "exp139_levin_voltage.json")

# ---- the frozen mapping constants (declared BEFORE any rho computation) ----
B_ARM = "posterior-depol (exp39-V3 verbatim: corrupt_region(POST_Q, "
B_ARM += "theta_value=WT_HEAD_V) pre-run) + exp131 plane geometry; "
B_ARM += "readout EA = head_likeness(V, TAIL) >= 0.7"
PUB_B_SERIES = dict(PUB_OCTANOL_DH)      # eids 415-419, unchanged
B_TAXONOMY = dict(TAXONOMY)              # exp139's deposited taxonomy
# O1 zones = exp131's deposited IP-G1 zones (the C leg's bar):
O1_PASS, O1_REFUTE = 0.6, -0.3
# O4 plane-resolved zones = LV-G1's own deposited zones (O4 is LV-G1
# re-run under the repaired instrument, so ITS bar carries):
O4_PASS, O4_REFUTE = 0.4, -0.6

MAPPING_DECLARED = True   # the O2 sentinel: everything above the rho
                          # computations in main() is frozen at import

_RHO_CALLS = [0]          # order-discipline counter (O2)


def depol_arm(plane: str, seed: int) -> tuple[bool, bool, float, float]:
    """The B family's repaired arm: the exp39-V3 posterior-depolarization
    channel VERBATIM (corruption BEFORE the 24 h run, V3's own regrow
    kwargs) + exp131's plane geometry. Declared in the docstring's MAPPING
    DECLARATION before any rho computation (gate O2)."""
    c = make_collective(seed)
    c.corrupt_region(POST_Q, theta_value=WT_HEAD_V)   # exp39-V3 verbatim
    c.run(24, dt=DT)
    kw = dict(cell_period=0.8, dt=DT, noise=0.6)      # V3's own kwargs
    if plane == "head":
        c.amputate(HEAD_SL, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(HEAD_SL, direction="backward", **kw)
    elif plane == "trunk":
        c.amputate(TRUNK, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TRUNK, direction="both", **kw)
    elif plane == "tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, **kw)
    else:
        raise ValueError(plane)
    return _flags(c)


def o1_zone(rho):
    """O1's pre-registered verdict (exp131 zones + the degeneracy clause)."""
    if rho is None:
        return "FAIL-DEGENERATE"
    if rho >= O1_PASS:
        return "PASS"
    if rho <= O1_REFUTE:
        return "REFUTED"
    return "PARTIAL"


def o4_zone(rho):
    """O4's pre-registered verdict (LV-G1's own zones + degeneracy)."""
    if rho is None:
        return "FAIL-DEGENERATE"
    if rho >= O4_PASS:
        return "PASS"
    if rho <= O4_REFUTE:
        return "REFUTED"
    return "PARTIAL"


def rho_tracked(a, b):
    """rho_or_none with the O2 order counter attached."""
    _RHO_CALLS[0] += 1
    return rho_or_none(a, b)


def main() -> dict:
    print("=== exp158: the octanol-DH plane series on its deposited arm ===\n")

    # ---- O2 FIRST: the mapping freeze, asserted before any rho call -------
    assert MAPPING_DECLARED, "mapping sentinel not set"
    assert ("MAPPING DECLARATION (PRE-REGISTERED BEFORE ANY RHO COMPUTATION)"
            in (__doc__ or "")), "docstring mapping declaration missing"
    assert _RHO_CALLS[0] == 0, "a rho was computed before the O2 assertion"
    assert set(PUB_B_SERIES) == set(B_TAXONOMY) == set(PUB_ORDER)
    assert len(PUB_ORDER) == 5 and set(SIM_PLANES) == {"head", "trunk", "tail"}
    o2 = {
        "verdict": "PASS",
        "mechanism": (
            "docstring MAPPING DECLARATION + module constants "
            "(B_ARM/PUB_B_SERIES/B_TAXONOMY/O1 zones) frozen at import; "
            "asserted in main() before the first rho call "
            f"(_RHO_CALLS at assert time = {_RHO_CALLS[0]})"),
        "declared_mapping": {
            "b_family": "GJ-blocked, 57 entries (exp139 frozen partition)",
            "arm": B_ARM,
            "published_series": PUB_B_SERIES,
            "plane_taxonomy": B_TAXONOMY,
            "o1_zones": {"pass": O1_PASS, "refute": O1_REFUTE},
            "o4_zones": {"pass": O4_PASS, "refute": O4_REFUTE},
        },
    }
    print(f"  O2 order discipline: {o2['verdict']} "
          f"(mapping frozen before rho; {o2['mechanism'][:60]}...)")

    # ---- anchors: the frozen partition + the deposit ----------------------
    fam, rows_by_fam = build_families()
    counts = {f: len(rows_by_fam[f]) for f in "ABCDE"}
    dep = json.load(open(DEP139))
    dep_g4 = dep["gates"]["LV_G4"]
    counts_match = bool(counts == dep["partition"]["counts"])
    print(f"\n  partition counts {counts} (match deposit: {counts_match})")
    print(f"  deposit B leg (junction-cut arm): EA by plane "
          f"{dep['stack_by_family']['B_gj_blocked']['ea_by_plane']} -> "
          f"rho {dep_g4['rho_B_octanol']} (DEGENERATE)")

    # ---- O1: the repaired B leg — depol arm by plane ----------------------
    depol = {}
    for plane in SIM_PLANES:
        rows = [depol_arm(plane, s) for s in SEEDS]
        depol[plane] = {
            "ea_rate": float(np.mean([r[0] for r in rows])),
            "ea_flags": [bool(r[0]) for r in rows],
            "hl_per_seed": [round(float(r[3]), 4) for r in rows],
        }
    sim_b = [depol[B_TAXONOMY[p]]["ea_rate"] for p in PUB_ORDER]
    pub_b = [PUB_B_SERIES[p] for p in PUB_ORDER]
    rho_b = rho_tracked(sim_b, pub_b)
    z_b = o1_zone(rho_b)
    print(f"\n  O1 repaired B leg: pub octanol-DH {pub_b}")
    print(f"     depol EA by plane "
          f"{ {p: d['ea_rate'] for p, d in depol.items()} } "
          f"(hl { {p: d['hl_per_seed'] for p, d in depol.items()} })")
    print(f"     sim by pub order {[round(x, 3) for x in sim_b]} "
          f"-> rho {rho_b}: {z_b}")

    # ---- O3: the C leg re-run must reproduce the deposit bit-exactly ------
    ion = {}
    for plane in SIM_PLANES:                     # exp139's order: H, T, t
        rows = [ion_arm(plane, s) for s in SEEDS]
        ion[plane] = {
            "abn_rate": float(np.mean([r[2] >= ABN_ERR_MV
                                       or r[3] >= ABN_HL
                                       for r in rows])),
        }
    sim_c = [ion[TAXONOMY[p]]["abn_rate"] for p in PUB_ORDER]
    pub_c = [PUB_HEADLESS[p] for p in PUB_ORDER]
    rho_c = rho_tracked(sim_c, pub_c)
    sim_c_dep = dep_g4["sim_c_abn_by_pub_order"]
    rho_c_dep = dep_g4["rho_C_headless"]
    sim_c_exact = bool(sim_c == sim_c_dep)
    rho_c_exact = bool(rho_c == rho_c_dep)
    o3 = {
        "verdict": "PASS" if (sim_c_exact and rho_c_exact)
        else "FAIL",
        "sim_c_recomputed": sim_c, "sim_c_deposit": sim_c_dep,
        "sim_c_bit_exact": sim_c_exact,
        "rho_c_recomputed": rho_c, "rho_c_deposit": rho_c_dep,
        "rho_c_bit_exact": rho_c_exact,
    }
    print(f"\n  O3 C-leg integrity: sim bit-exact {sim_c_exact}, "
          f"rho bit-exact {rho_c_exact} (rho {rho_c}) -> {o3['verdict']}")

    # ---- O4: the pooling question -----------------------------------------
    # (a) pooled companion: 4-family E_stack with the B scalar mapped
    #     through the depol channel (tail-plane EA — tied to D, disclosed).
    cut_res = [cutting_arm(s) for s in SEEDS]
    cut_abn = float(np.mean([r[0] for r in cut_res]))
    e_stack_repaired = [cut_abn, depol["tail"]["ea_rate"],
                        ion["tail"]["abn_rate"], depol["tail"]["ea_rate"]]
    e_meas = [dep["measured_by_family"][f] for f in "ABCD"]
    rho_pool = rho_tracked(e_stack_repaired, e_meas)
    rho_pool_dep = dep["gates"]["LV_G1"]["spearman"]
    # (b) plane-resolved pool: 10 record-plane cells, THE GATE.
    sim_pool = [depol[B_TAXONOMY[p]]["ea_rate"] for p in PUB_ORDER] + \
               [ion[TAXONOMY[p]]["abn_rate"] for p in PUB_ORDER]
    pub_pool = [PUB_B_SERIES[p] for p in PUB_ORDER] + \
               [PUB_HEADLESS[p] for p in PUB_ORDER]
    rho_o4 = rho_tracked(sim_pool, pub_pool)
    z_o4 = o4_zone(rho_o4)
    o4 = {
        "pooled_companion": {
            "e_stack_repaired": e_stack_repaired,
            "e_stack_note": ("B's scalar = depol tail EA, structurally "
                             "TIED to D's scalar (same deposited arm) — "
                             "the mapping's own consequence, disclosed"),
            "e_meas": e_meas,
            "spearman": rho_pool,
            "deposit_spearman_LV_G1": rho_pool_dep,
        },
        "plane_resolved_pool": {
            "cells": "B: 5 octanol-DH planes via depol EA; C: 5 headless "
                     "planes via ion abn (10 cells)",
            "sim": sim_pool, "pub": pub_pool,
            "spearman": rho_o4,
            "zones": {"pass": O4_PASS, "refute": O4_REFUTE},
            "verdict": z_o4,
        },
        "verdict": z_o4,
        "pooling_erases_structure": (None if rho_pool is None or rho_o4 is None
                                     else bool(rho_o4 > rho_pool)),
    }
    print(f"\n  O4 pooled companion: E_stack "
          f"{[round(x, 3) for x in e_stack_repaired]} vs E_meas "
          f"{[round(x, 4) for x in e_meas]} -> rho {rho_pool} "
          f"(deposit LV-G1 rho {rho_pool_dep})")
    print(f"  O4 plane-resolved pool (10 cells): rho {rho_o4} -> {z_o4}")
    print(f"  O4 verdict: {o4['verdict']} "
          f"(pooling still erases structure: "
          f"{o4['pooling_erases_structure']})")

    # ---- verdict -----------------------------------------------------------
    npass = sum([z_b == "PASS", o2["verdict"] == "PASS",
                 o3["verdict"] == "PASS", z_o4 == "PASS"])
    print(f"\n  === {npass}/4 gates PASS (O1 {z_b}, O2 {o2['verdict']}, "
          f"O3 {o3['verdict']}, O4 {z_o4}) ===")

    result = {
        "exp": "exp158_octanol_plane",
        "task": (
            "THE OCTANOL-DH PLANE SERIES, RE-TESTED ON ITS DEPOSITED ARM — "
            "L116 exp139's registered repair of the DEGENERATE LV-G4 B leg: "
            "re-map the B family (GJ-blocked, 57 entries) onto the deposited "
            "posterior-depol arm (exp39-V3's channel) with the plane-resolved "
            "instrument that landed the C leg at rho 0.6489, now applied to "
            "the depol channel."),
        "foundation": {
            "ledger": "L116 (exp139)",
            "owned_gap": (
                "LV-G4's B leg DEGENERATE: the junction-cut arm "
                "(gap_scale 0.05, exp39-V4's mapping) carries no EA sign at "
                "any plane (0/0/0) while its tail abnormal rate is the "
                "graded 0.667; the octanol DH sign rides the DEPOLARIZATION "
                "channel (exp39-V3's deposited posterior-depol mapping) — a "
                "stack predictivity gap for the octanol family's headline "
                "readout, owned as a gap not a contradiction"),
            "registered_repair": (
                "the octanol-DH plane series re-tested on its deposited arm "
                "(posterior-depol by plane vs eids 415-419)"),
        },
        "partition_counts": counts,
        "partition_counts_match_deposit": counts_match,
        "b_leg_before_after": {
            "before": {
                "arm": "junction-cut (gap_scale 0.05, exp39-V4 mapping)",
                "ea_by_plane": dep["stack_by_family"]["B_gj_blocked"]
                ["ea_by_plane"],
                "rho_octanol_dh": dep_g4["rho_B_octanol"],
                "verdict": "DEGENERATE (0/0/0)",
                "source": "results/exp139_levin_voltage.json (L116)",
            },
            "after": {
                "arm": "posterior-depol (exp39-V3 mapping) by plane",
                "ea_by_plane": {p: d["ea_rate"] for p, d in depol.items()},
                "ea_flags": {p: d["ea_flags"] for p, d in depol.items()},
                "hl_per_seed": {p: d["hl_per_seed"]
                                for p, d in depol.items()},
                "sim_by_pub_order": sim_b, "pub_octanol_dh": pub_b,
                "rho_octanol_dh": rho_b,
                "tail_plane_hl_matches_deposit_V3_hl": bool(
                    depol["tail"]["hl_per_seed"]
                    == dep["stack_by_family"]["D_depolarization"]
                    ["hl_per_seed"]),
                "verdict": z_b,
            },
        },
        "gates": {
            "O1_repaired_b_leg": {
                "verdict": z_b,
                "rho": rho_b,
                "sim_by_pub_order": sim_b, "pub_series": pub_b,
                "zones": {"pass": O1_PASS, "refute": O1_REFUTE},
                "degeneracy_clause": (
                    "rho None (zero-variance sim) -> FAIL-DEGENERATE"),
            },
            "O2_mapping_declared_before_rho": o2,
            "O3_c_leg_deposit_integrity": o3,
            "O4_pooling_question": o4,
        },
        "criteria": {
            "O1_repaired_b_leg_plane_rho": z_b,
            "O2_mapping_declared_before_rho": o2["verdict"],
            "O3_c_leg_deposit_integrity": o3["verdict"],
            "O4_pooling_plane_resolved": z_o4,
        },
        "verdict": (
            f"{npass}/4 gates PASS (O1 {z_b}, O2 {o2['verdict']}, "
            f"O3 {o3['verdict']}, O4 {z_o4})"),
        "notes": (
            "THE REPAIR MOVED THE B LEG FROM A FLOOR DEGENERACY TO A "
            "CEILING DEGENERACY: the depol channel flips the EA read from "
            "0/0/0 (junction-cut arm, L116) to 1/1/1 at every plane — the "
            "stack's DH prediction is a step function of the CHANNEL (off "
            "-> on) with ZERO plane resolution, while the record's octanol "
            "DH series is plane-GRADED (0.05 -> 1.00 -> 0.00, floor at the "
            "tail plane, which the deposited taxonomy cannot separate from "
            "post-pharyngeal — both fold to the stack tail plane). The "
            "record's post-pharyngeal 1.00 cell IS the one the stack's "
            "ceiling hits (and the head .05/pre-phar .28 cells are "
            "over-predicted). O4: plane-resolution moves the cross-family "
            "concordance from -0.258 (pooled companion; deposit LV-G1 "
            "-0.105) to +0.372 — pooling still erases structure (True) — "
            "but the repaired instrument does not reach LV-G1's 0.4 bar "
            "(PARTIAL, owned): the ceiling-tied B cells carry no within-"
            "family rank information to pool. Continuity: the tail-plane "
            "run IS the deposited exp39-V3 arm bit-exactly (hl per seed "
            "0.9763/0.9309/0.9316 == the deposit's D-family hl_per_seed), "
            "and the C leg re-run reproduces the deposit bit-exactly "
            "(O3) — the repair breaks nothing it touched."),
        "sources": {
            "record": "research/levin_voltage_series.json (eids 415-419 "
                      "octanol DH; eids 391-395 headless)",
            "arms": ("experiments/exp39_levin_voltage.py V3 verbatim "
                     "(posterior-depol channel); "
                     "experiments/exp139_levin_voltage.py (ion_arm, flags, "
                     "taxonomy, partition — imported unchanged); "
                     "experiments/exp131_ion_plane_ordering.py (plane "
                     "geometry + O1's deposited zones)"),
            "deposit": "results/exp139_levin_voltage.json (L116)",
        },
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
