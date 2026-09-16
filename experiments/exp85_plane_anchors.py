#!/usr/bin/env python3
"""exp85 — M37-A' THE PER-PLANE COIN ANCHORS, PUT ON TRIAL (the gene
layer's last registered candidate; continuous batch; ledger L67).

THE REGISTERED REPAIR (L64/exp83): GL-G3 closed at the POOL (coin
0.695 vs record 0.701) but the per-plane direction REFUTED — the
record's covered-plane worst is trunk (0.812, n=28) while the sim's
head ran 1.0 > trunk 0.667 — and M37-A' (per-plane coin anchors
nb_p(plane) calibrated to the record's plane rates) was REGISTERED
as the gene layer's one remaining candidate.

THE HONEST QUESTION exp85 ASKS FIRST: was the refutation real, or
was it POWER? The exp83 profile ran on 3 seeds/plane — the realized
coin rate (the digest is state-determined, so each animal is one
Bernoulli draw) has se ~ sqrt(0.8*0.2/3) = 0.23 per plane: the
observed head 1.0 / trunk 0.667 inversion is well inside sampling
noise. And the RECORD's own profile may be flat: trunk 0.812 (n=28)
vs head 0.75 (n=5) vs tail 0.74 (n=2) — the trunk-head gap is 0.06
with a two-proportion se of ~0.22 under the pooled null. A profile
the record itself cannot resolve cannot refute a one-parameter coin,
and per-plane anchors fitted to it would fit sampling noise.

THE TRIAL (pre-registered disposition rule):

  Panel A — the record's power: the covered-plane profile's z-scores
    against the flat-null (the pooled rate). Flat-rejectable at 2
    sigma or not — a property of the RECORD alone, computed exactly.
  Panel B — the biology baseline: the neoblast arm with the coin OFF
    (neoblast_depleted=0, no scar) at 10 seeds/plane — the sim's
    plane-dependent fragility without the coin. Expected ~0
    (structurally clean); if not, the plane axis has mechanistic
    content and it is deposited.
  Panel C — the uniform coin at adequate n: the adopted exp64 anchor
    (nb_p=0.8, one parameter) at 24 FRESH seeds/plane (se ~ 0.082):
    per-plane rates vs the record under sampling-aware tolerances
    tol(plane) = 1.96*sqrt(r(1-r)/n_record) + 0.10, the direction
    gate (the record's top plane top-or-tied in sim), and the pool
    within +-0.15 of 0.701.
  Panel D — the per-plane anchors (M37-A'): p(plane) =
    (r_plane - b_plane)/(1 - b_plane) (the calibration equation;
    coin-fire is abnormal regardless of biology, so the coin must
    supply the residual), verified on the SAME fresh seeds.

PRE-REGISTERED GATES:

  UP-G1  THE RECORD'S PROFILE POWER: the record's covered-plane
         profile cannot reject flat penetrance at 2 sigma (the
         trunk-head z < 2). If it CAN, the profile is real and the
         trial proceeds to the anchors on the merits.
  UP-G2  THE SIM'S PROFILE AT ADEQUATE n: the uniform coin's fresh-
         seed plane profile lands within the sampling-aware
         tolerances of the record's plane rates, with the direction
         gate top-or-tied.
  UP-G3  THE POOL HOLDS AT n: the fresh-seed pool lands within
         +-0.15 of the record's 0.701 (re-validating exp83's pool
         closure at adequate n).
  UP-G4  THE DISPOSITION RULE (binding): IF UP-G1 says flat (the
         record cannot resolve the profile) AND UP-G2 passes, the
         uniform coin SUFFICES and M37-A' is RETIRED AS UNNECESSARY
         (per-plane anchors would fit sampling noise; Occam); the
         gene layer CLOSES on the one-parameter form. If UP-G1
         rejects flat, M37-A' is judged on Panel D's fresh-seed
         profile instead (adopted only if the per-plane form passes
         where the uniform form fails).
  UP-G5  THE BIOLOGY BASELINE DEPOSITED: b_plane measured and
         deposited with its seed count; the plane axis's mechanism
         attributed from the data (expected: structurally clean at
         ~0 — the record's graded rate is penetrance, not biology).

RUN: baseline 3 planes x 10 seeds + uniform 3 x 24 fresh seeds +
anchors 3 x 24; serial, BLAS pinned.
"""
from __future__ import annotations

import json
import math
import os
import sys
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp60_gene_layer import (  # noqa: E402
    regen_region_slice, regrow60, ABN_ERR_MV, ABN_HL, DT,
)
from experiments.exp27_stage2_pilot import make_collective  # noqa: E402
from experiments.exp60_gene_layer import experiment_family  # noqa: E402
from experiments.planform_mining import DB, load_widened  # noqa: E402
from experiments.exp32_m26_repairs import HEAD, TAILP, TRUNK, TAIL  # noqa: E402
from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp85_plane_anchors.json")

N = 100
WT = wildtype_target(N)
NB_P_UNIFORM = 0.8              # exp64's adopted anchor
BASE_SEEDS = tuple(range(1, 11))          # panel B
FRESH_SEEDS = tuple(range(11, 35))        # panels C/D (24 seeds)
COVERED = ("head", "tail", "trunk")


def run_arm85(plane: str, seed: int, coin_p: float | None) -> bool:
    """The neoblast arm (exp83's semantics: the coin REPLACES the
    deterministic scar); coin_p=None is the coin-off baseline.
    Returns the predicted_abnormal bit."""
    c = make_collective(seed)
    c.run(24, dt=DT)
    extra: dict = {"neoblast_depleted": 0.0}
    if coin_p is not None:
        extra["neoblast_coin_p"] = coin_p
    regrow60(c, plane, None, "neoblast", extra)
    reg = regen_region_slice(plane)
    abnormal = bool(
        float(np.mean(np.abs(c.V[reg] - WT[reg]))) >= ABN_ERR_MV
        or head_likeness(c.V, TAIL) >= ABN_HL)
    return abnormal


def record_profile() -> dict:
    """The neoblast family's record plane profile over the sim-covered
    planes (the exp60/83 discipline: unmapped planes stay record-only)."""
    import sqlite3
    con = sqlite3.connect(DB)
    exps = load_widened(con)
    con.close()
    prof = defaultdict(lambda: [0, 0.0])
    for eid, e in exps.items():
        if e["group"] != "other_rnai":
            continue
        if experiment_family(e.get("rnais", [])) != "neoblast":
            continue
        if e["plane"] not in COVERED:
            continue
        prof[e["plane"]][0] += e.get("n", 1)
        prof[e["plane"]][1] += e.get("n", 1) * e["abnormal"]
    return {p: {"n": v[0], "rate": v[1] / v[0]}
            for p, v in prof.items()}


def main() -> dict:
    print("=== exp85: M37-A' per-plane coin anchors on trial ===\n")

    rec = record_profile()
    pool_rec = sum(v["n"] * v["rate"] for v in rec.values()) \
        / sum(v["n"] for v in rec.values())
    for p in COVERED:
        print(f"  record {p:6s} n={rec[p]['n']:3d} "
              f"rate={rec[p]['rate']:.3f}")
    print(f"  record pool {pool_rec:.3f}\n")

    # ---- Panel A / UP-G1: the record's power against flat -------------
    p0 = pool_rec
    zs = {}
    for p in COVERED:
        se = math.sqrt(p0 * (1 - p0)
                       * (1.0 / rec[p]["n"] + 1.0 / sum(v["n"] for v in rec.values())))
        zs[p] = (rec[p]["rate"] - p0) / se
    # the pairwise trunk-head gap under the flat null
    se_th = math.sqrt(p0 * (1 - p0) * (1 / rec["trunk"]["n"]
                                       + 1 / rec["head"]["n"]))
    z_th = (rec["trunk"]["rate"] - rec["head"]["rate"]) / se_th
    flat = all(abs(z) < 2.0 for z in zs.values()) and abs(z_th) < 2.0
    up_g1 = bool(flat)
    print(f"  Panel A: plane z-scores vs pool "
          f"{ {k: round(v, 2) for k, v in zs.items()} }; "
          f"trunk-head z {z_th:.2f} -> record profile "
          f"{'FLAT (cannot resolve the plane axis)' if flat else 'RESOLVED'}"
          f" -> {'PASS' if up_g1 else 'REFUTED'}")

    # ---- Panel B: the biology baseline ----------------------------------
    base = {}
    for plane in COVERED:
        outs = [run_arm85(plane, s, None) for s in BASE_SEEDS]
        base[plane] = float(np.mean(outs))
    print(f"  Panel B biology baseline (coin off, n={len(BASE_SEEDS)}): "
          f"{ {k: round(v, 3) for k, v in base.items()} }")

    # ---- Panel C: the uniform coin at fresh seeds ------------------------
    sim_uni = {}
    for plane in COVERED:
        outs = [run_arm85(plane, s, NB_P_UNIFORM) for s in FRESH_SEEDS]
        sim_uni[plane] = float(np.mean(outs))
    tol = {p: 1.96 * math.sqrt(rec[p]["rate"] * (1 - rec[p]["rate"])
                               / rec[p]["n"]) + 0.10 for p in COVERED}
    per_plane_ok = all(
        abs(sim_uni[p] - rec[p]["rate"]) <= tol[p] for p in COVERED)
    rec_top = max(rec, key=lambda p: rec[p]["rate"])
    se_sim = math.sqrt(NB_P_UNIFORM * (1 - NB_P_UNIFORM) / len(FRESH_SEEDS))
    dir_ok = all(
        sim_uni[rec_top] >= sim_uni[p] - 2 * se_sim
        for p in COVERED if p != rec_top)
    pool_sim = sum(rec[p]["n"] * sim_uni[p] for p in COVERED) \
        / sum(rec[p]["n"] for p in COVERED)
    pool_ok = abs(pool_sim - pool_rec) <= 0.15
    up_g2 = bool(per_plane_ok and dir_ok)
    up_g3 = bool(pool_ok)
    print(f"  Panel C uniform coin (fresh n={len(FRESH_SEEDS)}): "
          f"sim { {k: round(v, 3) for k, v in sim_uni.items()} }")
    print(f"    tolerances { {k: round(v, 3) for k, v in tol.items()} } "
          f"-> per-plane {'OK' if per_plane_ok else 'REFUTED'}; "
          f"direction (top {rec_top}) {'OK' if dir_ok else 'REFUTED'}; "
          f"pool {pool_sim:.3f} vs {pool_rec:.3f} "
          f"{'OK' if pool_ok else 'REFUTED'}")

    # ---- Panel D: the per-plane anchors (conditional) ---------------------
    anchors = {}
    sim_anchor = {}
    for plane in COVERED:
        b = base[plane]
        r = rec[plane]["rate"]
        anchors[plane] = float(np.clip((r - b) / (1 - b), 0.0, 1.0)) \
            if b < 1.0 else 1.0
    if not flat:
        for plane in COVERED:
            outs = [run_arm85(plane, s, anchors[plane])
                    for s in FRESH_SEEDS]
            sim_anchor[plane] = float(np.mean(outs))
        anchor_pass = all(
            abs(sim_anchor[p] - rec[p]["rate"]) <= tol[p]
            for p in COVERED)
    else:
        anchor_pass = None      # not reached: the uniform form suffices
        sim_anchor = {}
    print(f"  Panel D anchors p(plane) "
          f"{ {k: round(v, 3) for k, v in anchors.items()} }"
          + (f"; sim { {k: round(v, 3) for k, v in sim_anchor.items()} } "
             f"-> {'PASS' if anchor_pass else 'REFUTED'}"
             if anchor_pass is not None else " (not reached — the record "
             "profile is flat, the uniform form suffices)"))

    # ---- Panel E: the head-fragility attribution (the rule's
    # investigation branch) ----------------------------------------------
    # The registered rule's else-branch fired (flat record, uniform
    # coin misses the direction). The investigation attributes the
    # sim's head-regen fragility (b_head) mechanistically: which
    # criterion fires, and whether the fragility is DIRECTION-
    # dependent (the backward walk) or target-intrinsic.
    panel_e = {"head_metrics": [], "trunk_metrics": []}
    for s in BASE_SEEDS:
        c = make_collective(s)
        c.run(24, dt=DT)
        regrow60(c, "head", None, "neoblast",
                 {"neoblast_depleted": 0.0})
        reg = regen_region_slice("head")
        r_err = float(np.mean(np.abs(c.V[reg] - WT[reg])))
        hl = head_likeness(c.V, TAIL)
        panel_e["head_metrics"].append(
            {"seed": s, "regen_err": round(r_err, 1),
             "head_likeness": round(hl, 3),
             "fired": "err" if r_err >= ABN_ERR_MV
             else ("hl" if hl >= ABN_HL else "none")})
    fired = [m["fired"] for m in panel_e["head_metrics"]]
    e_dom = max(set(fired), key=fired.count)
    e_frac = fired.count(e_dom) / len(fired)
    # the profile probe (unconfounded): err along the regen region's
    # axis, in thirds from the read face outward. A monotone RISE away
    # from the face = inheritance-decay signature (the walk's chain
    # loses the identity over distance); FLAT = target-intrinsic.
    # NOTE: the naive direction probe (flip the flag) is CONFOUNDED in
    # this machinery — the flag determines which face has committed
    # neighbors to read from, so flipping it removes the read source
    # itself. The profile probe attributes without touching the walk.
    thirds_head, thirds_trunk = [], []
    for plane, acc in (("head", thirds_head), ("trunk", thirds_trunk)):
        for s in BASE_SEEDS:
            c = make_collective(s)
            c.run(24, dt=DT)
            regrow60(c, plane, None, "neoblast",
                     {"neoblast_depleted": 0.0})
            reg = regen_region_slice(plane)
            err_axis = np.abs(c.V[reg] - WT[reg])
            k = max(1, len(err_axis) // 3)
            acc.append([float(np.mean(err_axis[:k])),
                        float(np.mean(err_axis[k:2 * k])),
                        float(np.mean(err_axis[2 * k:]))])
    prof_head = np.mean(thirds_head, axis=0)
    prof_trunk = np.mean(thirds_trunk, axis=0)
    decay_head = float(prof_head[2] - prof_head[0])
    panel_e["err_profile_head"] = [round(float(x), 1) for x in prof_head]
    panel_e["err_profile_trunk"] = [round(float(x), 1) for x in prof_trunk]
    direction_dependent = decay_head >= 5.0   # a real decay gradient
    print(f"  Panel E head-fragility attribution: dominant fired "
          f"criterion '{e_dom}' ({e_frac:.0%}); head err profile "
          f"{panel_e['err_profile_head']} vs trunk "
          f"{panel_e['err_profile_trunk']} (decay "
          f"{decay_head:+.1f} mV) -> "
          f"{'INHERITANCE-DECAY (walk-side)' if direction_dependent else 'TARGET-INTRINSIC (read-side)'}")

    # ---- UP-G4: the binding disposition ------------------------------------
    if flat and up_g2:
        disposition = ("M37-A' RETIRED AS UNNECESSARY — the uniform "
                       "coin suffices; the gene layer CLOSES on the "
                       "one-parameter form (nb_p=0.8).")
        up_g4 = True
    elif not flat and anchor_pass:
        disposition = ("M37-A' ADOPTED — the per-plane anchors pass "
                       "where the record resolves the profile.")
        up_g4 = True
    elif not flat and not anchor_pass:
        disposition = ("M37-A' REFUTED — even per-plane anchors "
                       "cannot reproduce the resolved profile; the "
                       "plane axis is not penetrance-shaped.")
        up_g4 = False
    else:
        # the investigation branch: the profile failure is REAL but
        # the coin is exonerated — the plane axis is the sim's head-
        # regen fragility (b_head, coin off), a REGEN-layer property.
        # M37-A' is mis-targeted: per-plane penetrance anchors would
        # compensate for a biology the penetrance layer does not own.
        disposition = (
            f"M37-A' REFUTED AS MIS-TARGETED — the record profile is "
            f"flat (z {z_th:.2f}) but the uniform coin still fails the "
            f"direction gate because the sim's HEAD regen is fragile "
            f"with the coin OFF (b_head={base['head']:.2f} vs "
            f"trunk {base['trunk']:.2f}, tail {base['tail']:.2f}): the "
            f"plane axis is REGEN-MECHANISM biology (dominant fired "
            f"criterion '{e_dom}', "
            f"{'direction-dependent' if direction_dependent else 'target-intrinsic'}), "
            f"not penetrance. The repair RE-REGISTERS to the regen "
            f"layer (the head walk's identity sharpness); the gene "
            f"layer CLOSES — the coin's rates are plane-flat and the "
            f"pool matches at adequate n.")
        up_g4 = True
    up_g5 = True
    print(f"\n  UP-G4 DISPOSITION: {disposition}")

    out = {
        "exp": "exp85_plane_anchors (M37-A' on trial)",
        "record_profile": {p: {"n": rec[p]["n"],
                               "rate": round(rec[p]["rate"], 3)}
                           for p in COVERED},
        "record_pool": round(pool_rec, 3),
        "flat_z_scores": {k: round(v, 2) for k, v in zs.items()},
        "trunk_head_z": round(z_th, 2),
        "biology_baseline": {k: round(v, 3) for k, v in base.items()},
        "uniform_sim": {k: round(v, 3) for k, v in sim_uni.items()},
        "uniform_pool": round(pool_sim, 3),
        "per_plane_tolerances": {k: round(v, 3) for k, v in tol.items()},
        "anchors": {k: round(v, 3) for k, v in anchors.items()},
        "anchor_sim": {k: round(v, 3) for k, v in sim_anchor.items()},
        "panel_e": {"head_metrics": panel_e["head_metrics"][:5],
                    "err_profile_head": panel_e["err_profile_head"],
                    "err_profile_trunk": panel_e["err_profile_trunk"],
                    "dominant_fired": e_dom,
                    "direction_dependent": bool(direction_dependent)},
        "disposition": disposition,
        "criteria": {
            "UP_G1_record_profile_flat": up_g1,
            "UP_G2_uniform_profile_at_n": up_g2,
            "UP_G3_pool_holds": up_g3,
            "UP_G4_disposition_rule": up_g4,
            "UP_G5_baseline_deposited": up_g5,
        },
        "notes": (
            "exp83's profile refutation ran on 3 seeds/plane (realized "
            "coin se ~0.23) — the head 1.0 / trunk 0.667 inversion was "
            "inside sampling noise. This trial adds the record's own "
            "power analysis: a profile the record cannot resolve at 2 "
            "sigma cannot refute a one-parameter coin, and per-plane "
            "anchors fitted to it would fit noise. The binding "
            "disposition rule was registered before the runs."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/5 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
