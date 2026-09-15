#!/usr/bin/env python3
"""exp37 — FULL-CORPUS SWEEP (QUEST task 4 completed): every outcome-bearing
PlanformDB experiment mapped to a per-experiment sim arm.

This converts the class-level pilot (exp31: 31 arms on bin medians) into
the full per-experiment validation the quest asked for: each of the
~1,462 outcome-bearing experiments is mapped individually to
(class protocol, plane, recorded cut fraction), unique arms are deduped,
run at 3 seeds, and the prediction is compared to the experiment's own
recorded outcome.

MAPPINGS (all pre-registered in earlier experiments; the sweep uses the
ADOPTED model state, nothing new is fitted tonight):
  class -> protocol
    cutting        defaults (exp27/31)
    innexin        gap_scale=0.05 sustained (exp27/29)
    gj_block       gap_scale=0.05 sustained (exp31 drug enrichment)
    ion_channel    gamma x0.5 + noise x3 + M27b chain commitment diffusion
                   (cns=3.0, diff=1.5 — exp34 ADOPTED)
    morphogen(AP)  beta-catenin/wnt RNAi -> wnt_ (posterior -> head
                   identity, POST_Q -> WT_HEAD_V); apc/axin RNAi -> apc_
                   (anterior -> tail identity, ANT_Q -> WT_TAIL_V);
                   non-AP morphogen genes -> unmappable (DV/eye/brain
                   axes have no 1D-sheet layer)
    other_rnai     defaults (the model claims non-bioelectric RNAi does
                   not change the bioelectric map beyond the wound)
  plane -> geometry (exp31) with M26c adopted two-face trunk:
    tail forward / head backward / trunk BOTH faces (M26c) /
    head_tail tail+head / crosspiece per-experiment cut_f (clamped to
    [0.05, 0.95]) with the exp36 adopted phi_readout=0.75 spec layer
  unmappable (recorded, not hidden): graft, irr (no neoblast layer),
  lateral (2D cuts, no 2D sheet), none (no gene-expression layer),
  non-AP morphogen, drug_only (no concentration/mapping).

PRE-REGISTERED GATES (fixed BEFORE the sweep ran):
  G1  COVERAGE: the mappable fraction of the outcome corpus is >= 0.70.
  G2  CLASS ORDERING: across sim-mappable classes with >= 10 mapped
      experiments, Spearman rho(sim pred_abn_rate pooled per class,
      recorded abnormal mean) > 0.
  G3  PLANE ORDERING: across planes with >= 10 mapped experiments,
      Spearman rho > 0 likewise.
  G4  ABSOLUTE CALIBRATION: outcome-weighted MAE between per-experiment
      sim rate and recorded abnormal <= 0.34 (one seed's resolution —
      the model's grain at 3 seeds).
  G5  CONTROL REPRODUCTION: the sweep's cutting_tail per-seed errors
      are bit-exact vs exp31's recorded cutting_tail errs (the sweep
      must reuse the adopted protocol, not silently re-derive it).

RUN PROTOCOL: exp31/34/36 discipline (seeds (1,2,3), window 24h dt=0.1,
thresholds unchanged (ABN_ERR_MV=6.0, ABN_HL=0.7), metrics immediately
after regrow). Serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
OPENBLAS_NUM_THREADS = os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
MKL_NUM_THREADS = os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)
from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, SEEDS, TAIL, ABN_ERR_MV, ABN_HL, make_collective,
)
from experiments.exp32_m26_repairs import (  # noqa: E402
    HEAD, TAILP, TRUNK, POST_Q, ANT_Q, WT_HEAD_V, WT_TAIL_V,
)
from experiments.planform_mining import (  # noqa: E402
    DB, load_widened, AP_MORPHOGEN_RE,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp37_full_sweep.json")


# ---------------------------------------------------------------- protocol
def window(c, hours: float = 24.0) -> None:
    c.run(hours, dt=DT)


def regrow_kw(class_prefix: str) -> dict:
    """regrow kwargs per class protocol (adopted mechanisms only)."""
    kw = dict(cell_period=0.8, dt=DT, noise=0.6)
    if class_prefix == "ion_channel":
        kw.update(commitment_noise_scale=3.0, commitment_diffusion=1.5)
    if class_prefix == "crosspiece":
        kw.update(phi_readout=0.75)
    return kw


def run_plane(c, plane: str, cut_f: float, class_prefix: str,
              direction_map: dict) -> None:
    """Amputate + regrow one plane (exp31 geometry, M26c trunk both)."""
    if plane == "head":
        c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(HEAD, direction="backward", **regrow_kw(class_prefix))
    elif plane == "tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, **regrow_kw(class_prefix))
    elif plane == "trunk":
        c.amputate(TRUNK, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TRUNK, direction="both", **regrow_kw(class_prefix))
    elif plane == "head_tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, **regrow_kw(class_prefix))
        c.regrow(HEAD, direction="backward", **regrow_kw(class_prefix))
    elif plane == "crosspiece":
        ci = int(round(cut_f * N))
        ci = min(max(ci, 5), N - 1)
        c.amputate(slice(ci, N), wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(slice(ci, N), **regrow_kw("crosspiece"))
    else:
        raise ValueError(plane)
    del direction_map


def apply_class(c, class_prefix: str) -> None:
    if class_prefix in ("innexin", "gjblock"):
        c.block_gap_junctions(0.05)
    elif class_prefix == "ion_channel":
        c.gamma *= 0.5
        c.noise_std *= 3.0
    elif class_prefix == "wnt":
        c.corrupt_region(POST_Q, theta_value=WT_HEAD_V)
    elif class_prefix == "apc":
        c.corrupt_region(ANT_Q, theta_value=WT_TAIL_V)


def run_arm(class_prefix: str, plane: str, cut_f: float, seed: int) -> dict:
    c = make_collective(seed)
    apply_class(c, class_prefix)
    window(c)
    run_plane(c, plane, cut_f, class_prefix, {})
    m = {
        "wt_pattern_error": c.pattern_error(wildtype_target(N)),
        "head_likeness_tail": head_likeness(c.V, TAIL),
        "seed": seed,
    }
    m["predicted_abnormal"] = bool(
        m["wt_pattern_error"] >= ABN_ERR_MV
        or m["head_likeness_tail"] >= ABN_HL)
    return m


def sim_arm(class_prefix: str, plane: str, cut_f: float) -> dict:
    runs = [run_arm(class_prefix, plane, cut_f, s) for s in SEEDS]
    errs = [r["wt_pattern_error"] for r in runs]
    return {
        "err_mean": float(np.mean(errs)),
        "err_per_seed": errs,
        "pred_abn_rate": float(np.mean([r["predicted_abnormal"]
                                        for r in runs])),
    }


# ------------------------------------------------------------ mapping
def arm_key_for(e: dict) -> tuple[str, str, float] | None:
    """(class_prefix, plane, cut_f) or None if unmappable."""
    group, plane = e["group"], e["plane"]
    if plane in ("graft", "irr", "lateral", "none"):
        return None
    if plane not in ("head", "tail", "trunk", "head_tail", "crosspiece"):
        return None
    if group == "cutting":
        cp = "cutting"
    elif group in ("innexin", "gj_block"):
        cp = "innexin" if group == "innexin" else "gjblock"
    elif group == "ion_channel":
        cp = "ion_channel"
    elif group == "other_rnai":
        cp = "cutting"          # model claim: non-bioelectric RNAi == wound
    elif group == "morphogen":
        if not e.get("ap_morphogen"):
            return None         # DV/eye/brain axes: no 1D layer
        rnais = " | ".join(e.get("rnais", []))
        # apc/axin are beta-catenin ANTAGONISTS: their RNAi phenotype is
        # the beta-catenin gain-of-function direction (posterior->head).
        # Pre-registered rule: match the antagonist first (apc|axin),
        # else the ligand/core (beta-catenin|wnt|barhl-like names).
        if re.search(r"apc|axin", rnais, re.I):
            cp = "apc"
        else:
            cp = "wnt"
    else:
        return None             # drug_only and anything unmapped
    cut_f = 0.5
    if plane == "crosspiece":
        f = e.get("cut_f")
        cut_f = min(max(float(f), 0.05), 0.95) if f is not None else 0.5
        cut_f = round(cut_f, 2)
    return cp, plane, cut_f


def main() -> dict:
    print("=== exp37: full-corpus sweep (QUEST task 4) ===\n")

    exp31 = json.load(open(os.path.join(ROOT, "results",
                                        "exp31_stage2_widened.json")))
    con = sqlite3.connect(DB)
    exps = load_widened(con)
    con.close()
    print(f"  outcome-bearing experiments: {len(exps)}")

    # map every experiment
    rows: list[dict] = []
    unmappable: dict[str, int] = {}
    for eid, e in exps.items():
        key = arm_key_for(e)
        rec = {
            "eid": eid,
            "group": e["group"],
            "plane": e["plane"],
            "cut_f": e.get("cut_f"),
            "n": e.get("n", 1),
            "recorded_abnormal": e["abnormal"],
        }
        if key is None:
            reason = (f"{e['group']}|{e['plane']}" if e["plane"] in
                      ("graft", "irr", "lateral", "none")
                      else ("morphogen_nonAP" if e["group"] == "morphogen"
                            else f"{e['group']}|{e['plane']}"))
            unmappable[reason] = unmappable.get(reason, 0) + 1
            rec["sim"] = None
            rec["unmappable"] = reason
        else:
            rec["sim"] = list(key)
            rec["unmappable"] = None
        rows.append(rec)

    mapped = [r for r in rows if r["sim"] is not None]
    n_total = sum(r["n"] for r in rows)
    n_mapped = sum(r["n"] for r in mapped)
    coverage = n_mapped / n_total if n_total else 0.0
    print(f"  mappable: {len(mapped)}/{len(rows)} experiments "
          f"(n-weighted coverage {coverage:.3f})")
    for reason, cnt in sorted(unmappable.items(), key=lambda kv: -kv[1]):
        print(f"    unmappable {reason:22s} {cnt}")

    # unique arms
    keys = sorted({tuple(r["sim"]) for r in mapped})
    print(f"  unique sim arms: {len(keys)}")
    sim: dict[str, dict] = {}
    for i, (cp, plane, cf) in enumerate(keys):
        name = f"{cp}_{plane}" + (f"_f{int(round(cf * 100)):02d}"
                                  if plane == "crosspiece" else "")
        if name not in sim:
            sim[name] = sim_arm(cp, plane, cf)
        if (i + 1) % 10 == 0 or i == len(keys) - 1:
            print(f"    [{i + 1}/{len(keys)}] {name:28s} "
                  f"rate {sim[name]['pred_abn_rate']:.2f} "
                  f"err {sim[name]['err_mean']:5.2f}")

    # attach predictions
    for r in mapped:
        cp, plane, cf = r["sim"]
        name = f"{cp}_{plane}" + (f"_f{int(round(cf * 100)):02d}"
                                  if plane == "crosspiece" else "")
        r["sim_arm"] = name
        r["sim_rate"] = sim[name]["pred_abn_rate"]

    # ---- gates -----------------------------------------------------------
    g1 = coverage >= 0.70

    def pooled(items: list[dict], field: str) -> tuple[float, int, float]:
        """n-weighted mean of sim rates, n, recorded mean."""
        n = sum(x["n"] for x in items)
        if not n:
            return 0.0, 0, 0.0
        sr = sum(x["sim_rate"] * x["n"] for x in items) / n
        rr = sum(x["recorded_abnormal"] * x["n"] for x in items) / n
        return sr, n, rr

    classes: dict[str, list[dict]] = {}
    for r in mapped:
        classes.setdefault(r["group"], []).append(r)
    cls_stats = {}
    for g, items in classes.items():
        sr, n, rr = pooled(items, "sim_rate")
        cls_stats[g] = {"sim": sr, "n": n, "recorded": rr}
    big_cls = {g: s for g, s in cls_stats.items() if s["n"] >= 10}
    g2 = False
    if len(big_cls) >= 3:
        from scipy.stats import spearmanr
        rho = spearmanr([s["sim"] for s in big_cls.values()],
                        [s["recorded"] for s in big_cls.values()])
        g2 = bool(rho.statistic > 0 and len(big_cls) >= 3)
        print(f"  class ordering rho={rho.statistic:.3f} "
              f"({len(big_cls)} classes)")

    planes: dict[str, list[dict]] = {}
    for r in mapped:
        planes.setdefault(r["plane"], []).append(r)
    pl_stats = {}
    for p, items in planes.items():
        sr, n, rr = pooled(items, "sim_rate")
        pl_stats[p] = {"sim": sr, "n": n, "recorded": rr}
    big_pl = {p: s for p, s in pl_stats.items() if s["n"] >= 10}
    g3 = False
    if len(big_pl) >= 3:
        from scipy.stats import spearmanr
        rho = spearmanr([s["sim"] for s in big_pl.values()],
                        [s["recorded"] for s in big_pl.values()])
        g3 = bool(rho.statistic > 0 and len(big_pl) >= 3)
        print(f"  plane ordering rho={rho.statistic:.3f} "
              f"({len(big_pl)} planes)")

    wmae = (sum(abs(r["sim_rate"] - r["recorded_abnormal"]) * r["n"]
                for r in mapped) / n_mapped) if n_mapped else 1.0
    g4 = bool(wmae <= 0.34)
    print(f"  outcome-weighted MAE: {wmae:.3f}")

    sweep_cut = sim.get("cutting_tail", {}).get("err_per_seed")
    rec_cut = exp31["sim_arms"]["cutting_tail"]["err_per_seed"]
    g5 = bool(sweep_cut is not None and np.allclose(
        sweep_cut, rec_cut, atol=1e-9, rtol=0.0))

    print(f"\n  G1 coverage >= 0.70:                {coverage:.3f}  "
          f"{'PASS' if g1 else 'REFUTED'}")
    print(f"  G2 class ordering rho > 0:          "
          f"{'PASS' if g2 else 'REFUTED'}")
    print(f"  G3 plane ordering rho > 0:          "
          f"{'PASS' if g3 else 'REFUTED'}")
    print(f"  G4 weighted MAE <= 0.34:            {wmae:.3f}  "
          f"{'PASS' if g4 else 'REFUTED'}")
    print(f"  G5 control reproduction (bit-exact):"
          f" {'PASS' if g5 else 'REFUTED'}")

    print("\n  per-class (n >= 10):")
    for g, s in sorted(cls_stats.items(), key=lambda kv: -kv[1]["n"]):
        print(f"    {g:12s} n={s['n']:4d}  sim {s['sim']:.2f}  "
              f"recorded {s['recorded']:.2f}")
    print("  per-plane (n >= 10):")
    for p, s in sorted(pl_stats.items(), key=lambda kv: -kv[1]["n"]):
        print(f"    {p:11s} n={s['n']:4d}  sim {s['sim']:.2f}  "
              f"recorded {s['recorded']:.2f}")

    out = {
        "exp": "exp37_full_sweep",
        "quest_task": 4,
        "n_outcome_experiments": len(rows),
        "n_mapped": len(mapped),
        "n_unique_arms": len(keys),
        "n_weighted_coverage": coverage,
        "unmappable_counts": unmappable,
        "adopted_state_used": {
            "ion_channel": "M27b cns=3.0 diff=1.5 (exp34)",
            "trunk": "M26c two-face direction=both (exp32)",
            "crosspiece": "phi_readout=0.75 (exp36 adopted mapping)",
            "innexin/gj_block": "gap_scale=0.05 sustained (exp27/31)",
        },
        "sim_arms": sim,
        "per_class": cls_stats,
        "per_plane": pl_stats,
        "weighted_mae": wmae,
        "rows": rows,
        "criteria": {
            "G1_coverage_ge_070": g1,
            "G2_class_ordering_rho": g2,
            "G3_plane_ordering_rho": g3,
            "G4_weighted_mae_le_034": g4,
            "G5_control_reproduction_bitexact": g5,
        },
        "prediction_rule": (
            "unchanged from exp27: abnormal iff pattern_error >= 6.0 mV OR "
            "head_likeness(tail) >= 0.7; sim rate over seeds (1,2,3)"),
        "notes": (
            "Per-experiment recorded outcome is Num-weighted 1 - freq(WT) "
            "(exp21 pre-registration). Publication bias: absolute recorded "
            "rates run hot; G2/G3 test ordering, G4 the absolute grain. "
            "Unmappable classes/planes are recorded, not hidden — each is "
            "a named missing layer (2D sheet, neoblasts, gene-expression, "
            "concentrations)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
