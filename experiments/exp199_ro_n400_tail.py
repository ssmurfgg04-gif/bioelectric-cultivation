#!/usr/bin/env python3
"""exp199 — R_O AT n=400 ON THE C6 TAIL (the reader's residual map).

exp198's registered next (L171): the universal reader's residual map
is fully named — random 0.630, adversarial n=100 0.545, adversarial
n=400 0.705 with the tail 25/100 owned by cell c6 (A-SYM+A-PAIR) —
and the remaining edge is the c6 tail's mechanism: price R_O
(exp166's rule_oriented_restore, the oriented one-way support
restore) at n=400 on the c6 tail.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp198's n=400 adversarial
battery rebuilt (its seed rule and cell definitions VERBATIM, n=400
via the CornerMedium constructor's first parameter); exp160's decode
stack VERBATIM (fingerprint asserted == exp160's deposit) with the
temporal dispatch = exp178's scoped arm under the -35.0 pin; R_O =
exp166's rule_oriented_restore VERBATIM applied at the frames level.

GATES (each evaluated exactly once):
  GATE-A1 (replay) the 100-instance n=400 battery replays
           BIT-EXACTLY vs exp198's deposit under the production
           scoped arm (all errs + verdicts equal at the deposit's
           rounding, seeds (1,2,3)).
  GATE-A2 (R_O on the oriented cells) R_O armed on every
           oriented-active instance (the cells carrying A-SYM per
           exp181's definitions); per-instance deltas deposited;
           the c6 tail's median delta names the branch:
           REPAIR (median drops >= 20%), PARTIAL (0 < drop < 20%),
           NEUTRAL-HARM (median <= 0).
  GATE-A3 (no-regression) on oriented-INACTIVE instances R_O is a
           no-op by construction — bit-exact replay; on
           oriented-active NON-tail instances no instance degrades
           by more than +0.05 mV (the pre-named no-regression bar).
  GATE-A4 (hygiene) zero rejections; all errs finite; the -35.0
           instrument pin asserted; the fingerprint asserted.
NO post-hoc tuning. --smoke permitted before the credited run,
discarded.
DEPOSIT: results/exp199_ro_n400_tail.json
RUN: python3 -m experiments.exp199_ro_n400_tail [--smoke] [--job ...] [--out ...]
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

OUT = os.path.join(ROOT, "results", "exp199_ro_n400_tail.json")

from experiments.exp166_leading_edge import (  # noqa: E402
    CornerMedium, SEED_BASE as EXP166_SEED_BASE,
)
from experiments.exp160_any_medium import (  # noqa: E402
    BAR, OOD_ANCHOR, READ_CONFIG, config_fingerprint,
)

# ---- INSTRUMENT PIN (exp198's machinery VERBATIM) --------------------
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


# ---- the cohort: exp198's n=400 adversarial battery, VERBATIM --------
ADVERSARIAL_CELLS = [3, 5, 6, 7]     # h+t, o+t, o+h, o+h+t (exp181's cohort)
ORIENTED_CELLS = [5, 6, 7]           # the cells carrying A-SYM (o = 1)
PER_CELL = 25
N400 = 400
SEEDS = (1, 2, 3)

DEP198 = os.path.join(ROOT, "results", "exp198_adversarial_reader_n400.json")

# the pre-named bars
REPAIR_PCT = 20.0                    # A2: median drop >= 20% names REPAIR
NO_REGRESSION_MV = 0.05              # A3: the pre-named no-regression bar


def main() -> dict:
    import time

    from experiments.exp166_leading_edge import (
        cell_dims, RepairedMedium, rule_oriented_restore,
    )
    from experiments.exp169_rt_scoping import THRESHOLD, f_max_frames

    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true",
                    help="the permitted check: cell 6 (the c6 tail), "
                         "j = 0, seeds (1,) — discarded, no deposit")
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

    # ---- the replay target: exp198's deposit ------------------------
    assert os.path.exists(DEP198), \
        "exp198's deposit is missing — the replay target is required"
    with open(DEP198) as f:
        dep198 = json.load(f)
    want_cells = [f"c{c}" for c in sorted(ADVERSARIAL_CELLS)]
    assert sorted(dep198.get("cells", {}).keys()) == want_cells, \
        "exp198's deposit is partial — all four cells required"
    dep_by_cell = {c: {r["j"]: r
                       for r in dep198["cells"][f"c{c}"]["instances"]}
                   for c in ADVERSARIAL_CELLS}

    if args.smoke:                              # the registered scope
        cells, js, seeds = [6], [0], (1,)
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
    print(f"=== exp199: R_O AT n=400 ON THE C6 TAIL ({mode}) ===")
    print(f"  read: exp160's stack VERBATIM, fingerprint {fp} asserted; "
          f"temporal dispatch = exp178's SCOPED arm (R_T iff "
          f"f_max < {THRESHOLD} else raw temporal); "
          f"R_O = exp166's rule_oriented_restore VERBATIM at the frames "
          f"level, armed on the oriented-active cells {ORIENTED_CELLS}\n")

    # ---- instrument pin (restored-world semantics, save/restore) ----
    pin_floor()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP160_FLOOR
               for m in PIN_MODULES), "instrument pin to -35.0 failed"
    print(f"  pin: NEURAL_SPEC_MIN = {DEP160_FLOOR} on "
          f"{[m.__name__ for m in PIN_MODULES]}\n")

    def run_cell(c: int) -> tuple[dict, list]:
        insts: list[dict] = []
        base_errs_all: list[float] = []
        ro_errs_all: list[float] = []
        n_rej_base = 0
        n_rej_ro = 0
        rej_records: list[dict] = []
        oriented_active = c in ORIENTED_CELLS
        for j in js:
            gen_seed = EXP166_SEED_BASE + 1000 * c + j
            # THE n=400 construction: exp198's battery VERBATIM —
            # exp166's CornerMedium with n as the constructor's FIRST
            # parameter and exp181's seed rule.
            med = CornerMedium(N400, gen_seed, cell_dims(c))
            assert med.n == N400, \
                f"CornerMedium built off n={N400}: got n={med.n}"
            dep_rec = dep_by_cell[c][j]
            if not args.smoke:
                assert len(dep_rec["errs"]) == len(seeds), \
                    f"exp198 deposit instance c{c} j{j} is incomplete"
            fmax = float(f_max_frames(list(med.snapshots())))

            # ---- GATE-A1: the bit-exact baseline replay -------------
            # THE one call site — the production read, scoped arm
            # (exp198's arm, unchanged).
            b_errs, b_ver, b_rho, b_branch = [], [], [], []
            replay_flags = []
            for s, dep_err, dep_ver in zip(
                    seeds, dep_rec["errs"], dep_rec["verified"]):
                out = _m148.decode("scoped", med, s, f_max=fmax)
                if not out["ok"]:
                    n_rej_base += 1            # RECORDED, never hidden
                    rej_records.append({"arm": "baseline", "j": j,
                                        "seed": s, "f_max": fmax,
                                        "rejection": out["rejection"]})
                    continue
                err = float(out["err"])
                assert np.isfinite(err), \
                    f"non-finite baseline err at c{c} j{j} s{s}"
                b_errs.append(err)
                b_ver.append(bool(out["verified"]))
                b_rho.append(float(out["rho"])
                             if out.get("rho") is not None else None)
                b_branch.append(out.get("branch"))
                base_errs_all.append(err)
                # bit-exact at the deposit's rounding (exp142 rounds
                # err_vs_target to 2 dp — exp198's deposit is exact there)
                replay_flags.append(
                    round(err, 2) == float(dep_err)
                    and bool(out["verified"]) == bool(dep_ver))
            replay_exact = bool(b_errs and all(replay_flags)
                                and len(b_errs) == len(seeds))

            # ---- GATE-A2: the R_O arm (oriented-active cells only) --
            ro_rec = None
            if oriented_active:
                frames = med.snapshots()
                ro_frames = rule_oriented_restore(med, frames)
                wrapped = RepairedMedium(med, ro_frames, "oriented")
                fmax_ro = float(f_max_frames(list(wrapped.snapshots())))
                r_errs, r_ver, r_rho, r_branch = [], [], [], []
                for s in seeds:
                    out = _m148.decode("scoped", wrapped, s,
                                       f_max=fmax_ro)
                    if not out["ok"]:
                        n_rej_ro += 1          # RECORDED, never hidden
                        rej_records.append({"arm": "R_O", "j": j,
                                            "seed": s, "f_max": fmax_ro,
                                            "rejection": out["rejection"]})
                        continue
                    err = float(out["err"])
                    assert np.isfinite(err), \
                        f"non-finite R_O err at c{c} j{j} s{s}"
                    r_errs.append(err)
                    r_ver.append(bool(out["verified"]))
                    r_rho.append(float(out["rho"])
                                 if out.get("rho") is not None else None)
                    r_branch.append(out.get("branch"))
                    ro_errs_all.append(err)
                b_med = (float(np.median(b_errs))
                         if len(b_errs) == len(seeds) else None)
                r_med = (float(np.median(r_errs))
                         if len(r_errs) == len(seeds) else None)
                delta = (round(r_med - b_med, 6)
                         if b_med is not None and r_med is not None
                         else None)
                drop_pct = (round((b_med - r_med) / b_med * 100.0, 4)
                            if b_med and r_med is not None else None)
                ro_rec = {"errs": r_errs, "verified": r_ver,
                          "rho": r_rho, "branch": r_branch,
                          "median_err": r_med, "f_max_ro": fmax_ro,
                          "delta_mV": delta, "drop_pct": drop_pct}

            rec = {"j": j, "gen_seed": gen_seed,
                   "n": int(med.n),
                   "violated": list(med.violated), "T": int(med.T_eff),
                   "n_hyper": int(med.n_hyper),
                   "n_oneway": int(med.n_oneway),
                   "oriented_active": oriented_active,
                   "tail": bool(dep_rec["median_err"] > BAR),
                   "dep198_median_err": dep_rec["median_err"],
                   "f_max": fmax,
                   "replay_bit_exact": replay_exact,
                   "errs": b_errs, "verified": b_ver,
                   "rho": b_rho, "branch": b_branch,
                   "median_err": (float(np.median(b_errs))
                                  if len(b_errs) == len(seeds) else None),
                   "ro": ro_rec}
            insts.append(rec)
            print(f"  [c{c} j{j:2d}] base med {rec['median_err']} "
                  f"replay {'exact' if replay_exact else 'DRIFT'}"
                  + (f" | R_O med {ro_rec['median_err']} "
                     f"delta {ro_rec['delta_mV']} mV "
                     f"({ro_rec['drop_pct']}%)"
                     if ro_rec else " | R_O not armed"))
        section = {
            "cell": c,
            "violation_class": ("+".join(med.violated)
                                if med.violated else "none"),
            "n_instances": len(insts), "seeds": list(seeds),
            "n_build": int(N400),
            "oriented_active": oriented_active,
            "ro_armed": oriented_active,
            "n_base_decodes": len(base_errs_all),
            "n_ro_decodes": len(ro_errs_all),
            "n_rejections_base": n_rej_base,
            "n_rejections_ro": n_rej_ro,
            "rejection_records": rej_records,
            "median_err_base": (float(np.median(base_errs_all))
                                if base_errs_all else None),
            "median_err_ro": (float(np.median(ro_errs_all))
                              if ro_errs_all else None),
            "n_replay_exact": sum(int(r["replay_bit_exact"])
                                  for r in insts),
            "n_tail": sum(int(r["tail"]) for r in insts),
            "instances": insts,
        }
        return section, base_errs_all

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
        print(f"\n  [c{c}] class '{section['violation_class']}' "
              f"base median {section['median_err_base']} mV | "
              f"replay exact {section['n_replay_exact']}/{len(js)} | "
              f"R_O {'ARMED' if section['ro_armed'] else 'not armed'} "
              f"(ro median {section['median_err_ro']}) | "
              f"rejections base {section['n_rejections_base']} "
              f"ro {section['n_rejections_ro']} "
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
        return {"exp": "exp199_ro_n400_tail", "smoke": True,
                "verdict": "smoke (discarded)"}

    # ---- gates (each evaluated exactly once, over the merged cohort)
    cells_present = sorted(result["cells"].keys())
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
    n_base_decodes = sum(result["cells"][k]["n_base_decodes"]
                         for k in cells_present)
    n_ro_decodes = sum(result["cells"][k]["n_ro_decodes"]
                       for k in cells_present)
    n_rej_total = sum(result["cells"][k]["n_rejections_base"]
                      + result["cells"][k]["n_rejections_ro"]
                      for k in cells_present)
    rej_records = [x for k in cells_present
                   for x in result["cells"][k]["rejection_records"]]
    expected_base = len(insts_all) * len(seeds)
    expected_ro = (sum(len(result["cells"][k]["instances"])
                       for k in cells_present
                       if result["cells"][k]["oriented_active"])
                   * len(seeds))
    n400_ok = all(r.get("n") == N400 for r in insts_all)
    replay_exact_all = all(r["replay_bit_exact"] for r in insts_all)

    # GATE-A2: R_O on the oriented cells
    ro_insts = [r for r in insts_all if r["oriented_active"]]
    ro_deltas = [r["ro"]["delta_mV"] for r in ro_insts
                 if r["ro"] and r["ro"]["delta_mV"] is not None]
    c6 = result["cells"]["c6"]
    tail6 = [r for r in c6["instances"] if r["tail"] and r["ro"]]
    tail6_deltas = [r["ro"]["delta_mV"] for r in tail6
                    if r["ro"]["delta_mV"] is not None]
    tail6_drops = [r["ro"]["drop_pct"] for r in tail6
                   if r["ro"]["drop_pct"] is not None]
    tail6_base = [r["median_err"] for r in tail6]
    tail6_ro = [r["ro"]["median_err"] for r in tail6]
    median_delta_mV = (float(np.median(tail6_deltas))
                       if tail6_deltas else None)
    median_drop_pct = (float(np.median(tail6_drops))
                       if tail6_drops else None)
    agg_base_median = (float(np.median(tail6_base))
                       if tail6_base else None)
    agg_ro_median = (float(np.median(tail6_ro))
                     if tail6_ro else None)
    agg_drop_pct = (round((agg_base_median - agg_ro_median)
                          / agg_base_median * 100.0, 4)
                    if agg_base_median and agg_ro_median is not None
                    else None)
    if median_drop_pct is None:
        branch = None
    elif median_drop_pct >= REPAIR_PCT:
        branch = "REPAIR"
    elif median_drop_pct > 0:
        branch = "PARTIAL"
    else:
        branch = "NEUTRAL-HARM"
    u2 = bool(len(ro_insts) == len(ORIENTED_CELLS) * PER_CELL
              and len(ro_deltas) == len(ro_insts)
              and all(result["cells"][k]["n_rejections_ro"] == 0
                      for k in cells_present)
              and branch in ("REPAIR", "PARTIAL", "NEUTRAL-HARM"))

    # GATE-A3: no-regression
    inactive = [r for r in insts_all if not r["oriented_active"]]
    a3_inactive = bool(inactive
                       and all(r["replay_bit_exact"] for r in inactive)
                       and all(r["ro"] is None for r in inactive))
    non_tail_active = [r for r in ro_insts if not r["tail"]]
    worst_regression = (max((r["ro"]["delta_mV"] for r in non_tail_active),
                            default=None)
                        if all(r["ro"] for r in non_tail_active) else None)
    a3_active = bool(non_tail_active
                     and worst_regression is not None
                     and worst_regression <= NO_REGRESSION_MV + 1e-9)
    u3 = bool(a3_inactive and a3_active)

    # GATE-A4: hygiene
    pooled_all = [e for r in insts_all for e in r["errs"]] + \
                 [e for r in ro_insts if r["ro"] for e in r["ro"]["errs"]]
    all_finite = all(np.isfinite(e) for e in pooled_all)
    pin_ok = all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP160_FLOOR
                 for m in PIN_MODULES)
    u4 = bool(n_rej_total == 0 and len(pooled_all)
              == expected_base + expected_ro and all_finite
              and n400_ok and pin_ok
              and config_fingerprint() == fp
              and fp == "8e11e88c1c2f1518")

    u1 = bool(n_base_decodes == expected_base and n400_ok
              and replay_exact_all
              and all(result["cells"][k]["n_rejections_base"] == 0
                      for k in cells_present))

    gates = {
        "A1_replay_bit_exact_n400": {
            "pass": u1, "n_media": len(insts_all), "medium_n": N400,
            "baseline_decodes": n_base_decodes,
            "expected": expected_base,
            "replay_bit_exact": bool(replay_exact_all),
            "n_replay_exact_instances":
                sum(int(r["replay_bit_exact"]) for r in insts_all),
            "n400_construction_asserted": bool(n400_ok),
            "rejections": sum(result["cells"][k]["n_rejections_base"]
                              for k in cells_present),
            "comparison": ("round(err, 2) == exp198's deposited errs and "
                           "verified flags equal, per (cell, j, seed); "
                           "exp142 rounds err_vs_target to 2 dp — the "
                           "deposit's rounding")},
        "A2_ro_on_oriented_cells": {
            "pass": u2, "ro_armed_cells": ORIENTED_CELLS,
            "n_ro_armed_instances": len(ro_insts),
            "n_ro_decodes": n_ro_decodes,
            "ro_rejections": sum(result["cells"][k]["n_rejections_ro"]
                                 for k in cells_present),
            "per_instance_deltas_deposited":
                bool(len(ro_deltas) == len(ro_insts)),
            "c6_tail": {
                "n_tail": len(tail6),
                "tail_def": f"exp198 median_err > BAR ({BAR} mV)",
                "median_delta_mV": median_delta_mV,
                "median_drop_pct": median_drop_pct,
                "tail_median_base": agg_base_median,
                "tail_median_ro": agg_ro_median,
                "aggregate_drop_pct": agg_drop_pct,
                "per_instance": [{"j": r["j"],
                                  "base": r["median_err"],
                                  "ro": r["ro"]["median_err"],
                                  "delta_mV": r["ro"]["delta_mV"],
                                  "drop_pct": r["ro"]["drop_pct"]}
                                 for r in tail6]},
            "branch": branch,
            "branch_rule": (f"REPAIR (median drop >= {REPAIR_PCT}%), "
                            f"PARTIAL (0 < drop < {REPAIR_PCT}%), "
                            f"NEUTRAL-HARM (median <= 0)")},
        "A3_no_regression": {
            "pass": u3,
            "oriented_inactive": {
                "cells": [c for c in ADVERSARIAL_CELLS
                          if c not in ORIENTED_CELLS],
                "ro_noop_by_construction": True,
                "n_instances": len(inactive),
                "bit_exact_replay": bool(a3_inactive)},
            "oriented_active_non_tail": {
                "n_instances": len(non_tail_active),
                "no_regression_bar_mV": NO_REGRESSION_MV,
                "worst_regression_mV": worst_regression,
                "held": bool(a3_active)}},
        "A4_hygiene": {
            "pass": u4, "n_decodes_total": len(pooled_all),
            "expected_total": expected_base + expected_ro,
            "rejections": n_rej_total, "rejection_records": rej_records,
            "all_errs_finite": bool(all_finite),
            "instrument_pin": {"constant": "NEURAL_SPEC_MIN",
                               "pinned_to": DEP160_FLOOR,
                               "asserted": bool(pin_ok),
                               "saved_values": _PIN_SAVE,
                               "modules": [m.__name__
                                           for m in PIN_MODULES]},
            "fingerprint": fp,
            "post_run_fingerprint": config_fingerprint()},
    }
    n_pass = sum(int(g["pass"]) for g in gates.values())
    if branch is not None:
        verdict = (f"{n_pass}/{len(gates)} gates - c6 tail branch "
                   f"{branch} (median drop {median_drop_pct}%, "
                   f"{len(tail6)}/{len(c6['instances'])} tail instances)")
    else:
        verdict = f"{n_pass}/{len(gates)} gates - c6 tail branch unnamed"
    print(f"\n  GATES: {verdict}")
    for k, g in gates.items():
        print(f"    {k}: {'PASS' if g['pass'] else 'REFUTE'}")
    print(f"  c6 tail: base median {agg_base_median} mV -> R_O median "
          f"{agg_ro_median} mV (median per-instance delta "
          f"{median_delta_mV} mV, drop {median_drop_pct}%)")
    print(f"  oriented-active non-tail: {len(non_tail_active)} instances, "
          f"worst regression {worst_regression} mV, "
          f"{'within bars' if a3_active else 'REFUTED'}")
    print(f"  oriented-inactive (R_O not armed): {len(inactive)} "
          f"instances, "
          f"{'bit-exact replay' if a3_inactive else 'REFUTED'}")

    result.update({
        "exp": "exp199_ro_n400_tail",
        "claim": (
            "R_O (exp166's rule_oriented_restore VERBATIM, the oriented "
            "one-way support restore) priced at n=400 on the c6 tail — "
            "exp198's adversarial reader residual, tail 25/100 owned by "
            "cell c6 (A-SYM+A-PAIR): exp198's n=400 battery rebuilt "
            "VERBATIM (its seed rule and exp181's cell definitions, "
            "CornerMedium(400, ...) at cells 3/5/6/7 x 25 instances x "
            "seeds (1,2,3)), replayed bit-exactly under the production "
            "scoped arm; R_O armed at the frames level on every "
            "oriented-active instance (the A-SYM cells 5/6/7) with the "
            "temporal dispatch = exp178's scoped arm under the -35.0 "
            "pin; the c6 tail's median delta names the branch "
            "(REPAIR / PARTIAL / NEUTRAL-HARM); no-regression held on "
            "the oriented-inactive (bit-exact by construction) and "
            "oriented-active non-tail instances"),
        "cohort": {
            "generator": (
                "exp198's battery VERBATIM — exp166's CornerMedium with "
                "n=400 as the constructor's FIRST PARAMETER, asserted "
                "med.n == 400 at every build"),
            "seed_base": EXP166_SEED_BASE,
            "seed_rule": "EXP166_SEED_BASE + 1000*c + j, j = 0..24",
            "cells": list(ADVERSARIAL_CELLS),
            "oriented_active_cells": list(ORIENTED_CELLS),
            "per_cell": PER_CELL, "n": N400,
            "n_media": len(insts_all), "seeds": list(seeds),
            "cell_classes": {k: result["cells"][k]["violation_class"]
                             for k in cells_present}},
        "repair_rule": {
            "rule": "R_O",
            "source": ("exp166's rule_oriented_restore VERBATIM, "
                       "applied at the frames level "
                       "(RepairedMedium wrapper, rule='oriented')"),
            "description": (
                "support-level symmetrize: a pair with exactly one "
                "direction present gets the surviving value copied to "
                "the absent direction; no-op when the support is "
                "already symmetric"),
            "armed_on": "every oriented-active instance (A-SYM cells)",
            "not_armed_on": "oriented-inactive instances (cell 3, h+t)"},
        "read": {**READ_CONFIG,
                 "fingerprint": fp,
                 "fingerprint_asserted": "8e11e88c1c2f1518",
                 "medium_n": N400,
                 "medium_n_note": (
                     "READ_CONFIG's 'n': 100 field is exp160's "
                     "deposited fingerprint of record (asserted "
                     "unchanged pre/post run); the decode stack is "
                     "size-agnostic — exp199's cohort knob is the "
                     "CornerMedium construction n=400, as in exp198"),
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
        "replay_target": {
            "deposit": "results/exp198_adversarial_reader_n400.json",
            "exp198_pooled_median": dep198["pooled_median_err"],
            "exp198_tail_owner": dep198["gates"][
                "A3_tail_characterization"]["tail_owner_cell"],
            "exp198_n_above": dep198["gates"][
                "A3_tail_characterization"]["n_above"]},
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
