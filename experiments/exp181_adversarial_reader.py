#!/usr/bin/env python3
"""exp181 — UNIVERSAL READER: ADVERSARIAL MEDIA (path 1's closer).

Stage 5 path 1 (the handoff ledger's ~85%): exp160's 200 RANDOM media
decode with ZERO rejections (median 0.630 mV); the adversarial class
is untested at scale. The corner cells, the flip battery, and the
grouping pairs were all decoded in this session's experiments — but
never as a UNIVERSAL-READER battery. THIS EXPERIMENT runs 200
STRUCTURED adversarial media through the production read.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Cohort, read, and gates are fixed now.

THE COHORT (200 structured adversarial media, zero fitting):
  exp166's CornerMedium generator at the four ADVERSARIAL cells —
  c = 3 (h+t), c = 5 (o+t), c = 6 (o+h), c = 7 (o+h+t) — 50
  instances each, seed = 166166 + 1000*c + j, j = 0..49, n = 100
  (exp166's construction VERBATIM; its main batteries used the same
  cells at n=100). This is the class the random-media sweep only
  samples in the tail: every medium carries at least two ACTIVE
  violation dimensions by construction.

THE READ (production, exactly as deposited):
  exp160's READ_CONFIG VERBATIM (fingerprint 8e11e88c1c2f1518
  asserted at run time) with the ONE adoption from L157: the
  temporal dispatch is exp178's SCOPED arm (the diagnostic clause,
  zero knobs) — the production read this session installed. Seeds
  (1, 2, 3). -35.0 instrument pin for comparability with the
  deposited random-media records (exp160's 200 ran pre-CF-1).

GATES (each evaluated exactly once):

  GATE-U1 (zero rejections — the universal claim) 600 decodes
           (200 media x 3 seeds): zero rejections, all errs finite,
           verify recorded per decode.
  GATE-U2 (the adversarial median at the deposited bar) the pooled
           adversarial median <= 1.30 mV (exp160's U2 bar = 2.0x
           the OOD anchor 0.65); the per-cell medians deposited;
           the random-media comparison (0.630) recorded as context,
           NOT a bar (adversarial media are ALLOWED to be harder —
           the bar is the U2 ceiling).
  GATE-U3 (the tail is corner-owned, characterized) the above-bar
           instances (err > 1.30) tabulated per cell with their
           violation classes; the deposit names which cell owns the
           tail; no bar on the tail SIZE (characterization gate).
  GATE-U4 (the scoped arm's discipline holds) per-cell f_max
           classifications deposited; wherever the diagnostic
           selects the raw path (f_max >= 32), the decode is the
           temporal arm's (recorded); zero cross-arm anomalies.

NO post-hoc tuning. A --smoke check (cell 3, j = 0, seeds (1,)) is
permitted before the credited run and discarded.

DEPOSIT: results/exp181_adversarial_reader.json

RUN:
  python3 -m experiments.exp181_adversarial_reader            # full
  python3 -m experiments.exp181_adversarial_reader --smoke    # check
  python3 -m experiments.exp181_adversarial_reader --cell 3
  # jobs: c3 | c5 | c6 | c7
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


ADVERSARIAL_CELLS = [3, 5, 6, 7]     # h+t, o+t, o+h, o+h+t
PER_CELL = 50
SEEDS = (1, 2, 3)

OUT = os.path.join(ROOT, "results", "exp181_adversarial_reader.json")
DEP160 = os.path.join(ROOT, "results", "exp160_any_medium.json")


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

    if args.smoke:                              # the registered smoke scope
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
    print(f"=== exp181: THE ADVERSARIAL READER ({mode}) ===")
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
        """U4's cross-arm reference: the arm the diagnostic SHOULD have
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
            med = CornerMedium(100, gen_seed, cell_dims(c))
            violated = list(med.violated)
            fmax = float(f_max_frames(list(med.snapshots())))
            cls = "diffuse" if fmax < THRESHOLD else "concentrated"
            rec = {"j": j, "gen_seed": gen_seed,
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
            if (j + 1) % 10 == 0 or j == js[-1]:
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
        return {"exp": "exp181_adversarial_reader", "smoke": True,
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
    pooled_median = (float(np.median(pooled)) if pooled else None)

    # random-media comparison: exp160's DEPOSITED pooled median, context
    ctx = 0.630
    try:
        with open(DEP160) as f:
            ctx = float(json.load(f)["pooled_median_err"])
    except Exception:
        pass

    u1 = bool(n_rej_total == 0 and len(pooled) == expected
              and len(verify_flags) == expected and all_finite)

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
        "U1_zero_rejections": {
            "pass": u1, "decodes": len(pooled), "expected": expected,
            "rejections": n_rej_total, "rejection_records": rej_records,
            "all_errs_finite": bool(all_finite),
            "verify_recorded_per_decode":
                bool(len(verify_flags) == expected),
            "verify_rate": (float(np.mean(verify_flags))
                            if verify_flags else None)},
        "U2_adversarial_median": {
            "pass": u2, "pooled_median_err": pooled_median,
            "bar_mV": BAR, "anchor_mV": OOD_ANCHOR, "bound_ratio": 2.0,
            "per_cell_medians": per_cell_meds,
            "p90_err": (float(np.percentile(pooled, 90)) if pooled
                        else None),
            "max_err": (float(np.max(pooled)) if pooled else None),
            "context_random_media_pooled_median": ctx,
            "context_role": ("exp160's deposited random-media median — "
                             "recorded as context, NOT a bar (adversarial "
                             "media are allowed to be harder; the bar is "
                             "the U2 ceiling)")},
        "U3_tail_characterization": {
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
        "U4_scoped_discipline": {
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
        print(f"  pooled adversarial median {pooled_median:.3f} mV "
              f"(bar {BAR})  p90 {gates['U2_adversarial_median']['p90_err']:.3f}"
              f"  max {gates['U2_adversarial_median']['max_err']:.3f}"
              f"  | random-media context {ctx:.3f} (not a bar)")
        print(f"  per-cell medians: "
              + ", ".join(f"c{k[1:]}={v:.3f}" for k, v in
                          sorted(per_cell_meds.items())))

    result.update({
        "exp": "exp181_adversarial_reader",
        "claim": (
            "the adversarial class at scale: 200 STRUCTURED adversarial "
            "media (exp166's CornerMedium at the four 2+-dimension cells "
            "3/5/6/7, 50 instances each) through the production read — "
            "exp160's decode stack VERBATIM (fingerprint asserted) with "
            "the temporal dispatch being exp178's scoped arm — zero "
            "rejections, the adversarial median at exp160's U2 bar, the "
            "tail characterized per cell with violation classes, the "
            "scoped arm's discipline recorded"),
        "cohort": {
            "generator": ("exp166's CornerMedium VERBATIM at n = 100 "
                          "(exp166's construction; its main batteries "
                          "used the same cells at n = 100)"),
            "seed_base": EXP166_SEED_BASE,
            "seed_rule": "EXP166_SEED_BASE + 1000*c + j, j = 0..49",
            "cells": list(ADVERSARIAL_CELLS),
            "per_cell": PER_CELL,
            "n_media": len(insts_all),
            "seeds": list(seeds),
            "n_decodes": len(pooled),
            "cell_classes": {k: result["cells"][k]["violation_class"]
                             for k in cells_present}},
        "read": {**READ_CONFIG,
                 "fingerprint": fp,
                 "fingerprint_asserted": "8e11e88c1c2f1518",
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
                     "note": ("the deposited random-media records "
                              "(exp160's 200) ran pre-CF-1; the floor is "
                              "pinned to -35.0 for comparability, "
                              "save/restore asserted")}},
        "pooled_median_err": pooled_median,
        "random_media_context": {
            "exp160_pooled_median": ctx,
            "source": "results/exp160_any_medium.json (deposited)",
            "role": "context, NOT a bar"},
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
    ap.add_argument("--cell", type=int, choices=ADVERSARIAL_CELLS,
                    default=None)
    ap.add_argument("--job", choices=["c3", "c5", "c6", "c7", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--cell/--job/--out)
