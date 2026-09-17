#!/usr/bin/env python3
"""exp198 — THE UNIVERSAL READER AT SCALE (adversarial media x the
size law).

The universal reader's last open class: adversarial media at n=400 —
exp181's four-cell adversarial cohort rebuilt at n=400 (the size law's
class), 4 cells x 25 instances x seeds (1,2,3).

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp181's cohort machinery verbatim (CornerMedium at n=400), exp178's scoped arm, the -35.0 pin.

GATES (each evaluated exactly once):
  GATE-A1 (build + decode) 100 adversarial instances at n=400
           decode with zero rejections through the production
           scoped arm (the CornerMedium construction at n=400,
           exp166's generator verbatim with n=400).
  GATE-A2 (the scale bar) the pooled adversarial median <= 1.30
           (the U2 bar); the size law's prediction priced: the
           n=400 adversarial median vs exp181's n=100 median 0.545
           — the ratio deposited against exp185's monotone law
           (predicted ratio ~ the n-law's, recorded not gated).
  GATE-A3 (the tail) above-bar instances tabulated per cell; the
           tail's ownership deposited (characterization gate).
  GATE-A4 (hygiene) per-cell f_max classifications deposited; pin
           asserted; zero cross-arm anomalies.
NO post-hoc tuning. --smoke permitted before the credited run, discarded.
DEPOSIT: results/exp198_adversarial_reader_n400.json
RUN: python3 -m experiments.exp198_adversarial_reader_n400 [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp198_adversarial_reader_n400.json")

from experiments.exp166_leading_edge import (  # noqa: E402
    CornerMedium, SEED_BASE as EXP166_SEED_BASE,
)
from experiments.exp160_any_medium import (  # noqa: E402
    BAR, OOD_ANCHOR, READ_CONFIG, config_fingerprint,
)

# ---- INSTRUMENT PIN -------------------------------------------------
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP160_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP160_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


ADVERSARIAL_CELLS = [3, 5, 6, 7]     # h+t, o+t, o+h, o+h+t (exp181's cohort)
PER_CELL = 25                        # exp181's 50 halved at 4x the size
N400 = 400                           # the size law's class (exp185's rung)
SEEDS = (1, 2, 3)

DEP181 = os.path.join(ROOT, "results", "exp181_adversarial_reader.json")
DEP185 = os.path.join(ROOT, "results", "exp185_n_scaling.json")

# deposited law anchors (fallbacks; the deposits are re-read at run time)
EXP181_N100_MEDIAN = 0.545
EXP185_LAW = {"n100": 0.675, "n400": 1.705}   # MONOTONE branch deposited


def main() -> dict:
    import time

    from experiments.exp166_leading_edge import cell_dims
    from experiments.exp167_rt_adopted import read_adopted
    from experiments.exp169_rt_scoping import THRESHOLD, f_max_frames

    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="the permitted check: cell 3, j = 0, seeds (1,) "
                         "— discarded, no deposit")
    ap.add_argument("--cell", type=int, choices=ADVERSARIAL_CELLS,
                    default=None)
    ap.add_argument("--job", choices=["c3", "c5", "c6", "c7", "all"],
                    default="all",
                    help="runner split; each job deposits its cell section "
                         "and merges into the shared result")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT
    t0 = time.time()

    # ---- the read stack, asserted before any decode -----------------
    fp = config_fingerprint()                   # exp160's READ_CONFIG
    assert fp == "8e11e88c1c2f1518", \
        f"exp160 READ_CONFIG fingerprint drifted: {fp}"
    assert THRESHOLD == 32.0, "scoped threshold drifted"
    assert hasattr(_m148, "read_scoped"), "scoped arm missing (exp178)"

    if args.smoke:                              # exp181's registered scope
        cells, js, seeds = [3], [0], (1,)
    else:
        cells = list(ADVERSARIAL_CELLS)
        if args.cell is not None:
            cells = [c for c in cells if c == args.cell]
        if args.job != "all":
            cells = [c for c in cells if c == int(args.job[1:])]
        assert cells, "empty cell selection"
        js, seeds = list(range(PER_CELL)), SEEDS
    mode = ("SMOKE instrument check - discarded" if args.smoke else
            f"FULL cells={cells} x {len(js)} instances x seeds {seeds}")
    print(f"=== exp198: THE UNIVERSAL READER AT SCALE, n=400 ({mode}) ===")
    print(f"  read: exp160's stack VERBATIM, fingerprint {fp} asserted; "
          f"temporal dispatch = exp178's SCOPED arm (R_T iff "
          f"f_max < {THRESHOLD} else raw temporal)\n")

    # ---- instrument pin (restored-world semantics, save/restore) ----
    pin_floor()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP160_FLOOR
               for m in PIN_MODULES), "instrument pin to -35.0 failed"
    print(f"  pin: NEURAL_SPEC_MIN = {DEP160_FLOOR} on "
          f"{[m.__name__ for m in PIN_MODULES]}\n")

    def ref_decode(med, s, fmax):
        """A4's cross-arm reference: the arm the diagnostic SHOULD have
        selected, called directly (R_T = exp167's read_adopted when
        diffuse; exp148's raw temporal arm when concentrated)."""
        if fmax < THRESHOLD:
            o = read_adopted(med, s)
            return {"ok": True, "err": float(o["err_vs_target"]),
                    "verified": bool(o["program_verified"]),
                    "rho": (float(o["rho"]) if o.get("rho") is not None
                            else None),
                    "branch": o.get("branch")}
        return _m148.decode("temporal", med, s)

    def run_cell(c: int) -> tuple[dict, list]:
        violated: list[str] = []
        insts: list[dict] = []
        errs_all: list[float] = []
        rej_records: list[dict] = []
        audits: list[dict] = []
        n_rej = 0
        for j in js:
            gen_seed = EXP166_SEED_BASE + 1000 * c + j
            # THE n=400 construction: exp166's CornerMedium VERBATIM —
            # n is the constructor's FIRST PARAMETER (exp181 called it
            # with 100; the size law's class is a call-site disclosure,
            # NO subclass needed), asserted at build time below.
            med = CornerMedium(N400, gen_seed, cell_dims(c))
            assert med.n == N400, \
                f"CornerMedium built off n={N400}: got n={med.n}"
            violated = list(med.violated)
            fmax = float(f_max_frames(list(med.snapshots())))
            cls = "diffuse" if fmax < THRESHOLD else "concentrated"
            rec = {"j": j, "gen_seed": gen_seed,
                   "n": int(med.n),
                   "violated": violated, "T": int(med.T_eff),
                   "p_keep": round(float(med.p_keep), 3),
                   "n_hyper": int(med.n_hyper),
                   "n_oneway": int(med.n_oneway),
                   "f_max": fmax, "class": cls,
                   "errs": [], "verified": [], "branch": [], "rho": []}
            for s in seeds:
                # THE one call site — the production read, scoped arm
                out = _m148.decode("scoped", med, s, f_max=fmax)
                if not out["ok"]:
                    n_rej += 1                # RECORDED, never hidden
                    rej_records.append({"j": j, "seed": s,
                                        "f_max": fmax,
                                        "rejection": out["rejection"]})
                    continue
                err = float(out["err"])
                assert np.isfinite(err), \
                    f"non-finite decode err at c{c} j{j} s{s}"
                rec["errs"].append(err)
                rec["verified"].append(bool(out["verified"]))
                rec["branch"].append(out.get("branch"))
                rec["rho"].append(float(out["rho"])
                                  if out.get("rho") is not None else None)
                errs_all.append(err)
                if j == js[0]:                # per-cell cross-arm audit
                    ref = ref_decode(med, s, fmax)
                    anomaly = (ref.get("ok") != out["ok"]
                               or ref.get("err") != err
                               or ref.get("verified") != out["verified"]
                               or ref.get("rho") != rec["rho"][-1]
                               or ref.get("branch") != out.get("branch"))
                    audits.append({"j": j, "seed": s, "f_max": fmax,
                                   "class": cls,
                                   "expected_arm":
                                       "R_T/exp167" if cls == "diffuse"
                                       else "raw_temporal",
                                   "anomaly": bool(anomaly)})
            rec["median_err"] = (float(np.median(rec["errs"]))
                                 if rec["errs"] else None)
            insts.append(rec)
            if (j + 1) % 5 == 0 or j == js[-1]:
                m = f"{float(np.median(errs_all)):.3f}" if errs_all else "-"
                print(f"  [c{c} {j + 1:3d}/{len(js)}] decodes "
                      f"{len(errs_all)} rejections {n_rej} "
                      f"median-so-far {m}")
        above = [r for r in insts
                 if r["median_err"] is not None and r["median_err"] > BAR]
        fmaxes = [r["f_max"] for r in insts]
        meds = [r["median_err"] for r in insts
                if r["median_err"] is not None]
        section = {
            "cell": c,
            "violation_class": "+".join(violated) if violated else "none",
            "n_instances": len(insts), "seeds": list(seeds),
            "n_build": int(N400),
            "median_err": (float(np.median(errs_all)) if errs_all
                           else None),
            "median_of_instance_medians": (float(np.median(meds))
                                           if meds else None),
            "n_rejections": n_rej, "rejection_records": rej_records,
            "verify_rate": (float(np.mean([v for r in insts
                                           for v in r["verified"]]))
                            if any(r["verified"] for r in insts) else None),
            "n_diffuse": sum(1 for r in insts if r["class"] == "diffuse"),
            "n_concentrated": sum(1 for r in insts
                                  if r["class"] == "concentrated"),
            "f_max_min": min(fmaxes) if fmaxes else None,
            "f_max_max": max(fmaxes) if fmaxes else None,
            "n_above_bar": len(above),
            "above_bar": [{"j": r["j"], "median_err": r["median_err"],
                           "violated": r["violated"], "errs": r["errs"]}
                          for r in above],
            "cross_arm_audit": {"n": len(audits),
                                "n_anomalies": sum(int(a["anomaly"])
                                                   for a in audits),
                                "records": audits},
            "instances": insts,
        }
        return section, errs_all

    # split runs accumulate cell sections across --job/--cell invocations
    split = (args.job != "all") or (args.cell is not None)
    result: dict = {}
    if not args.smoke and split and os.path.exists(out_path):
        with open(out_path) as f:
            result = json.load(f)
    result.setdefault("cells", {})

    for c in cells:
        ts = time.time()
        section, _errs = run_cell(c)
        section["runtime_s"] = round(time.time() - ts, 1)
        result["cells"][f"c{c}"] = section
        print(f"\n  [c{c}] class '{section['violation_class']}' median "
              f"{section['median_err']} mV | above-bar "
              f"{section['n_above_bar']}/{len(js)} | "
              f"{section['n_diffuse']} diffuse / "
              f"{section['n_concentrated']} concentrated "
              f"(f_max {section['f_max_min']}..{section['f_max_max']}) | "
              f"cross-arm audits {section['cross_arm_audit']['n']}, "
              f"anomalies {section['cross_arm_audit']['n_anomalies']} "
              f"({section['runtime_s']} s)\n")

    if args.smoke:
        print("\n  SMOKE instrument check complete - DISCARDED "
              "(no deposit, gates not evaluated)")
        restore_floor()
        assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                   == _PIN_SAVE[m.__name__] for m in PIN_MODULES), \
            "instrument floor restore failed"
        print(f"  floor restored to the saved world (asserted): "
              f"{_PIN_SAVE}")
        return {"exp": "exp198_adversarial_reader_n400", "smoke": True,
                "verdict": "smoke (discarded)"}

    # ---- gates (each evaluated exactly once, over the merged cohort)
    cells_present = sorted(result["cells"].keys())
    want_cells = [f"c{c}" for c in sorted(ADVERSARIAL_CELLS)]
    if cells_present != want_cells:
        result["verdict"] = (f"partial - cells {cells_present} merged; "
                             f"gates pending all four")
        result["cells_run"] = cells_present
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=1)
        print(f"  partial deposit written ({out_path}); rerun the "
              f"remaining jobs to close the gates")
        restore_floor()
        assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                   == _PIN_SAVE[m.__name__] for m in PIN_MODULES), \
            "instrument floor restore failed"
        return result

    insts_all = [r for k in cells_present
                 for r in result["cells"][k]["instances"]]
    pooled = [e for k in cells_present
              for r in result["cells"][k]["instances"] for e in r["errs"]]
    expected = (sum(result["cells"][k]["n_instances"]
                    for k in cells_present) * len(seeds))
    n_rej_total = sum(result["cells"][k]["n_rejections"]
                      for k in cells_present)
    rej_records = [x for k in cells_present
                   for x in result["cells"][k]["rejection_records"]]
    verify_flags = [v for k in cells_present for r in
                    result["cells"][k]["instances"] for v in r["verified"]]
    all_finite = all(np.isfinite(e) for e in pooled)
    n400_ok = all(r.get("n") == N400 for r in insts_all)
    pooled_median = (float(np.median(pooled)) if pooled else None)

    # ---- the scale-law pricing (A2's recorded, NOT gated, clause) ----
    # exp181's deposited n=100 adversarial median (0.545)
    n100_med = EXP181_N100_MEDIAN
    try:
        with open(DEP181) as f:
            n100_med = float(json.load(f)["pooled_median_err"])
    except Exception:
        pass
    # exp185's deposited MONOTONE n-law (grid media): the n=400 rung's
    # median over the n=100 rung's median = the n-law's predicted ratio
    law = dict(EXP185_LAW)
    try:
        with open(DEP185) as f:
            curve = json.load(f)["gates"]["Y2_curve_branch"]["curve"]
        by_n = {int(c["n"]): float(c["pooled_median_err"]) for c in curve}
        law = {"n100": by_n[100], "n400": by_n[400]}
    except Exception:
        pass
    predicted_ratio = (law["n400"] / law["n100"]) if law["n100"] else None
    observed_ratio = (pooled_median / n100_med
                      if pooled_median is not None and n100_med else None)

    u1 = bool(n_rej_total == 0 and len(pooled) == expected
              and len(verify_flags) == expected and all_finite
              and n400_ok)

    per_cell_meds = {k: result["cells"][k]["median_err"]
                     for k in cells_present}
    u2 = bool(pooled_median is not None and pooled_median <= BAR)

    above_recs = [{"cell": k, **a}
                  for k in cells_present
                  for a in result["cells"][k]["above_bar"]]
    n_above = len(above_recs)
    coverage = all(len(a["violated"]) > 0 for a in above_recs)
    counts_ok = (sum(result["cells"][k]["n_above_bar"]
                     for k in cells_present) == n_above)
    if n_above:
        owner = max(cells_present,
                    key=lambda k: (result["cells"][k]["n_above_bar"],
                                   max((a["median_err"]
                                        for a in result["cells"][k]
                                        ["above_bar"]), default=0.0),
                                   -int(k[1:])))
        owner_named = result["cells"][owner]["n_above_bar"] > 0
        owner_class = result["cells"][owner]["violation_class"]
    else:
        owner, owner_named, owner_class = None, True, None
    u3 = bool(coverage and counts_ok and owner_named)

    class_ok = all((r["f_max"] < THRESHOLD) == (r["class"] == "diffuse")
                   for r in insts_all)
    n_audits = sum(result["cells"][k]["cross_arm_audit"]["n"]
                   for k in cells_present)
    n_anomalies = sum(result["cells"][k]["cross_arm_audit"]["n_anomalies"]
                      for k in cells_present)
    audit_records = [a for k in cells_present for a in
                     result["cells"][k]["cross_arm_audit"]["records"]]
    n_raw_decodes = (sum(result["cells"][k]["n_concentrated"]
                         for k in cells_present) * len(seeds))
    n_rt_decodes = (sum(result["cells"][k]["n_diffuse"]
                        for k in cells_present) * len(seeds))
    u4 = bool(class_ok and n_anomalies == 0
              and config_fingerprint() == fp)

    gates = {
        "A1_zero_rejections_n400": {
            "pass": u1, "decodes": len(pooled), "expected": expected,
            "n_media": len(insts_all), "medium_n": N400,
            "n400_construction_asserted": bool(n400_ok),
            "rejections": n_rej_total, "rejection_records": rej_records,
            "all_errs_finite": bool(all_finite),
            "verify_recorded_per_decode":
                bool(len(verify_flags) == expected),
            "verify_rate": (float(np.mean(verify_flags))
                            if verify_flags else None)},
        "A2_adversarial_median_at_scale": {
            "pass": u2, "pooled_median_err": pooled_median,
            "bar_mV": BAR, "anchor_mV": OOD_ANCHOR, "bound_ratio": 2.0,
            "per_cell_medians": per_cell_meds,
            "p90_err": (float(np.percentile(pooled, 90)) if pooled
                        else None),
            "max_err": (float(np.max(pooled)) if pooled else None),
            "scale_law_pricing": {
                "role": ("RECORDED, NOT GATED — the size law's "
                         "prediction priced, per the pre-registration"),
                "exp181_n100_adversarial_median": n100_med,
                "exp181_source": ("results/exp181_adversarial_reader.json"
                                  " (deposited pooled_median_err)"),
                "observed_ratio_n400_vs_n100": observed_ratio,
                "exp185_law_n100_median_grid": law["n100"],
                "exp185_law_n400_median_grid": law["n400"],
                "exp185_law_branch": "MONOTONE (deposited Y2)",
                "exp185_predicted_ratio": predicted_ratio,
                "ratio_gap_observed_minus_predicted":
                    (observed_ratio - predicted_ratio
                     if observed_ratio is not None
                     and predicted_ratio is not None else None),
                "note": ("predicted ratio ~ the n-law's (exp185's "
                         "MONOTONE curve, grid media); the adversarial "
                         "ratio is deposited against it, no bar")}},
        "A3_tail_characterization": {
            "pass": u3, "bar_mV": BAR, "n_above": n_above,
            "n_instances": len(insts_all),
            "tail_frac": (n_above / len(insts_all)) if insts_all else 0.0,
            "attribution_coverage": bool(coverage),
            "counts_consistent": bool(counts_ok),
            "tail_owner_cell": owner,
            "tail_owner_class": owner_class,
            "per_cell": {k: {"n_above": result["cells"][k]["n_above_bar"],
                             "class": result["cells"][k]["violation_class"],
                             "above_bar": result["cells"][k]["above_bar"]}
                         for k in cells_present},
            "note": ("characterization gate: no bar on the tail SIZE — "
                     "the deposit names which cell owns the tail")},
        "A4_scoped_discipline_hygiene": {
            "pass": u4, "threshold": THRESHOLD,
            "classification_consistent": bool(class_ok),
            "n_diffuse_decodes_R_T": n_rt_decodes,
            "n_raw_path_decodes": n_raw_decodes,
            "per_cell_class": {k: {"n_diffuse": result["cells"][k]
                                   ["n_diffuse"],
                                   "n_concentrated": result["cells"][k]
                                   ["n_concentrated"],
                                   "f_max_min": result["cells"][k]
                                   ["f_max_min"],
                                   "f_max_max": result["cells"][k]
                                   ["f_max_max"]}
                               for k in cells_present},
            "cross_arm_audits": {"n": n_audits, "n_anomalies": n_anomalies,
                                 "records": audit_records},
            "pin_asserted": DEP160_FLOOR,
            "fingerprint": fp,
            "post_run_fingerprint": config_fingerprint()},
    }
    n_pass = sum(int(g["pass"]) for g in gates.values())
    if n_above:
        verdict = (f"{n_pass}/{len(gates)} gates - tail {n_above}/"
                   f"{len(insts_all)} above bar, owned by cell "
                   f"{owner} ({owner_class})")
    else:
        verdict = f"{n_pass}/{len(gates)} gates - no above-bar tail"
    print(f"\n  GATES: {verdict}")
    for k, g in gates.items():
        print(f"    {k}: {'PASS' if g['pass'] else 'REFUTE'}")
    if pooled:
        print(f"  pooled adversarial median at n=400 "
              f"{pooled_median:.3f} mV (bar {BAR})  "
              f"p90 {gates['A2_adversarial_median_at_scale']['p90_err']:.3f}"
              f"  max {gates['A2_adversarial_median_at_scale']['max_err']:.3f}")
        print(f"  scale-law pricing (recorded, not gated): ratio vs "
              f"exp181's n=100 median {n100_med:.3f} = "
              f"{observed_ratio:.3f}  |  exp185's n-law predicted ratio "
              f"{predicted_ratio:.3f} "
              f"({law['n400']:.3f}/{law['n100']:.3f}, MONOTONE)")
        print(f"  per-cell medians: "
              + ", ".join(f"c{k[1:]}={v:.3f}" for k, v in
                          sorted(per_cell_meds.items())))

    result.update({
        "exp": "exp198_adversarial_reader_n400",
        "claim": (
            "the universal reader's last open class at the size law's "
            "scale: exp181's four-cell adversarial cohort REBUILT AT "
            "n=400 (exp166's CornerMedium with n passed as the "
            "constructor's first parameter — no subclass; 4 cells "
            "3/5/6/7 x 25 instances, exp181's seed rule) through the "
            "production read — exp160's decode stack VERBATIM "
            "(fingerprint asserted) with the temporal dispatch being "
            "exp178's scoped arm under the -35.0 pin — zero "
            "rejections, the adversarial median at exp160's U2 bar, "
            "the n=400-vs-n=100 ratio priced against exp185's MONOTONE "
            "n-law (recorded, not gated), the tail characterized per "
            "cell, the scoped arm's discipline recorded"),
        "cohort": {
            "generator": (
                "exp166's CornerMedium VERBATIM at n = 400 — the "
                "constructor takes n as its FIRST PARAMETER (exp181's "
                "n=100 was a call-site value; exp166's module-level N "
                "was never hardcoded in the class), so n=400 is a "
                "call-site disclosure, NO subclass needed; asserted "
                "med.n == 400 at every build"),
            "seed_base": EXP166_SEED_BASE,
            "seed_rule": "EXP166_SEED_BASE + 1000*c + j, j = 0..24",
            "cells": list(ADVERSARIAL_CELLS),
            "per_cell": PER_CELL,
            "n": N400,
            "n_media": len(insts_all),
            "seeds": list(seeds),
            "n_decodes": len(pooled),
            "cell_classes": {k: result["cells"][k]["violation_class"]
                             for k in cells_present}},
        "read": {**READ_CONFIG,
                 "fingerprint": fp,
                 "fingerprint_asserted": "8e11e88c1c2f1518",
                 "medium_n": N400,
                 "medium_n_note": (
                     "READ_CONFIG's 'n': 100 field is exp160's "
                     "deposited fingerprint of record (asserted "
                     "unchanged pre/post run); the decode stack is "
                     "size-agnostic (exp185 ran it to n=500; exp190 "
                     "re-decoded n=400/500 fresh) — exp198's cohort "
                     "knob is the CornerMedium construction n=400"),
                 "temporal_dispatch": (
                     "exp178's SCOPED arm — exp148 decode('scoped'): "
                     "exp169's f_max_frames VERBATIM, R_T (exp167's "
                     "read_adopted) iff f_max < 32.0 else the existing "
                     "raw temporal path UNCHANGED"),
                 "instrument_pin": {
                     "constant": "NEURAL_SPEC_MIN",
                     "pinned_to": DEP160_FLOOR,
                     "saved_values": _PIN_SAVE,
                     "modules": [m.__name__ for m in PIN_MODULES],
                     "note": ("exp181's comparability pin — the floor "
                              "is pinned to -35.0, save/restore "
                              "asserted")}},
        "scale_law": {
            "exp181_n100_adversarial_median": n100_med,
            "n400_adversarial_median": pooled_median,
            "observed_ratio": observed_ratio,
            "exp185_monotone_law": {
                "n100_median": law["n100"], "n400_median": law["n400"],
                "predicted_ratio": predicted_ratio,
                "source": ("results/exp185_n_scaling.json Y2 curve "
                           "(grid media, MONOTONE branch)")},
            "role": "recorded, NOT gated (pre-registered)"},
        "pooled_median_err": pooled_median,
        "gates": gates,
        "cells_run": cells_present,
        "verdict": verdict,
        "runtime_s": round(time.time() - t0, 1),
    })
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1)
    print(f"  deposited {out_path} (runtime {result['runtime_s']} s)")

    restore_floor()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None)
               == _PIN_SAVE[m.__name__] for m in PIN_MODULES), \
        "instrument floor restore failed"
    print(f"  floor restored to the saved world (asserted): {_PIN_SAVE}")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
