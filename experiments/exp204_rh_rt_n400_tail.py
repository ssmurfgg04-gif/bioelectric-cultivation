#!/usr/bin/env python3
"""exp204 — R_H AND R_T AT n=400 ON THE C6 TAIL (L174's registered next).

exp199 falsified R_O as the c6 tail's mechanism (NEUTRAL-HARM, the
no-regression clause refuted). The tail class is c6 = A-SYM+A-PAIR —
the pre-named suspect is the A-PAIR (hyper) dimension, whose rule is
R_H (exp166's rule_hyper_S, L142's cancellation-density weighting);
R_T (exp166's rule_temporal_core) is the temporal rule and must be a
bit-exact no-op on this non-temporal battery — the control clause.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp199's rebuilt n=400 battery
(its construction, seed rule and cell definitions VERBATIM); the base
arm = exp199's deposit replayed (its baseline errs are the replay
target — no re-decode of the base arm is needed beyond the replay
assert); R_H and R_T = exp166's rules VERBATIM armed at the frames
level under the -35.0 pin; exp160's decode stack VERBATIM (fingerprint
asserted), the temporal dispatch = exp178's scoped arm.

GATES (each evaluated exactly once):
  GATE-B1 (replay) exp199's base-arm errs replay bit-exactly vs its
           deposit at the deposit's rounding (the battery is the SAME
           construction; spot-assert on the c6 tail + one clean cell,
           all seeds).
  GATE-B2 (R_H on the tail) R_H armed on the hyper-active instances;
           per-instance deltas deposited; the c6 tail's median delta
           names the branch: REPAIR (median drops >= 20%),
           PARTIAL (0 < drop < 20%), NEUTRAL-HARM (median <= 0).
  GATE-B3 (the R_T control + composition) R_T on this battery is a
           bit-exact no-op (T=1 frames — exp166's rule_temporal_core
           identity); the R_H x R_T composition equals R_H alone
           bit-exactly (the exp170 dominated-composition lesson:
           deposited, pre-named, not an adoption candidate unless
           R_H itself repairs).
  GATE-B4 (hygiene + no-regression) zero rejections; all errs
           finite; the pin asserted; on hyper-INACTIVE instances
           R_H is a no-op bit-exact; on hyper-active non-tail
           instances no degradation beyond +0.05 mV.
NO post-hoc tuning. --smoke permitted before the credited run,
discarded.
DEPOSIT: results/exp204_rh_rt_n400_tail.json
RUN: python3 -m experiments.exp204_rh_rt_n400_tail [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp204_rh_rt_n400_tail.json")

from experiments.exp166_leading_edge import (  # noqa: E402
    CornerMedium, SEED_BASE as EXP166_SEED_BASE, cell_dims,
    RepairedMedium, pooled_F, rule_hyper_S, rule_temporal_core,
)
from experiments.exp160_any_medium import (  # noqa: E402
    BAR, OOD_ANCHOR, READ_CONFIG, config_fingerprint,
)

# ---- INSTRUMENT PIN (exp199's save/restore pattern; every module that
# ---- captured NEURAL_SPEC_MIN at import along the read chain is pinned)
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp136_generator_v6 as _m136          # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp156_write_path as _m156            # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP160_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m136, _m142, _m145, _m148, _m156, _m94)
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


# ---- the cohort: exp199's n=400 adversarial battery, VERBATIM --------
ADVERSARIAL_CELLS = [3, 5, 6, 7]     # h+t, o+t, o+h, o+h+t (exp181's cohort)
HYPER_CELLS = [3, 6, 7]              # the cells carrying A-PAIR (h = 1)
HYPER_INACTIVE_CELLS = [5]           # hyper-inactive control (R_H = identity)
TAIL_CELL = 6                        # the c6 tail owner (exp198's map)
SPOT_CELLS = [6, 5]                  # B1 spot-assert: c6 tail + one clean cell
PER_CELL = 25
N400 = 400
SEEDS = (1, 2, 3)

DEP199 = os.path.join(ROOT, "results", "exp199_ro_n400_tail.json")

# the pre-named bars
REPAIR_PCT = 20.0                    # B2: median drop >= 20% names REPAIR
NO_REGRESSION_MV = 0.05              # B4: the pre-named no-regression bar
EXP160_FP = "8e11e88c1c2f1518"       # exp160's deposited config fingerprint


def main() -> dict:
    import time

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
    assert fp == EXP160_FP, \
        f"exp160 READ_CONFIG fingerprint drifted: {fp}"
    assert THRESHOLD == 32.0, "scoped threshold drifted"
    assert hasattr(_m148, "read_scoped"), "scoped arm missing (exp178)"

    # ---- the replay target: exp199's deposit (the B1 target) --------
    assert os.path.exists(DEP199), \
        "exp199's deposit is missing — the replay target is required"
    with open(DEP199) as f:
        dep199 = json.load(f)
    want_cells = [f"c{c}" for c in sorted(ADVERSARIAL_CELLS)]
    assert sorted(dep199.get("cells", {}).keys()) == want_cells, \
        "exp199's deposit is partial — all four cells required"
    dep_by_cell = {c: {r["j"]: r
                       for r in dep199["cells"][f"c{c}"]["instances"]}
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
    print(f"=== exp204: R_H AND R_T AT n=400 ON THE C6 TAIL ({mode}) ===")
    print(f"  read: exp160's stack VERBATIM, fingerprint {fp} asserted; "
          f"temporal dispatch = exp178's SCOPED arm (R_T iff "
          f"f_max < {THRESHOLD} else raw temporal); "
          f"R_H = exp166's rule_hyper_S VERBATIM and R_T = exp166's "
          f"rule_temporal_core VERBATIM at the frames level; R_H armed on "
          f"the hyper-active cells {HYPER_CELLS} (identity by construction "
          f"on {HYPER_INACTIVE_CELLS}); R_T + composition armed on the "
          f"c6 tail cell (T=1)\n")

    # ---- instrument pin (restored-world semantics, save/restore) ----
    pin_floor()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP160_FLOOR
               for m in PIN_MODULES), "instrument pin to -35.0 failed"
    print(f"  pin: NEURAL_SPEC_MIN = {DEP160_FLOOR} on "
          f"{[m.__name__ for m in PIN_MODULES]}\n")

    # ---- R_H's zero-knob F (L142's pre-decode rule, exp166 VERBATIM) -
    # pooled median nonzero |W| over ALL frames of the registered
    # cohort's hyper-active media (c3/c6/c7 x 25 — the pre-named
    # battery, run-scope-independent so every --job split shares ONE
    # instrument), computed BEFORE any R_H decode.
    f_media: list = []
    for c in HYPER_CELLS:
        for j in range(PER_CELL):
            f_media.append(CornerMedium(N400, EXP166_SEED_BASE + 1000 * c + j,
                                        cell_dims(c)))
    assert all(m.n == N400 for m in f_media), \
        "F-pooling battery built off n != 400"
    F_RH = pooled_F(f_media) if f_media else None
    del f_media
    print(f"  R_H zero-knob F = {F_RH} (exp166's pooled_F over the "
          f"registered cohort's hyper-active media, pre-decode)\n")

    def run_cell(c: int) -> tuple[dict, list]:
        insts: list[dict] = []
        base_errs_all: list[float] = []
        rh_errs_all: list[float] = []
        rt_errs_all: list[float] = []
        comp_errs_all: list[float] = []
        n_rej = {"base": 0, "rh": 0, "rt": 0, "comp": 0}
        rej_records: list[dict] = []
        hyper_active = c in HYPER_CELLS
        for j in js:
            gen_seed = EXP166_SEED_BASE + 1000 * c + j
            # THE n=400 construction: exp199's battery VERBATIM —
            # exp166's CornerMedium with n as the constructor's FIRST
            # parameter and exp181's seed rule.
            med = CornerMedium(N400, gen_seed, cell_dims(c))
            assert med.n == N400, \
                f"CornerMedium built off n={N400}: got n={med.n}"
            dep_rec = dep_by_cell[c][j]
            if not args.smoke:
                assert len(dep_rec["errs"]) == len(seeds), \
                    f"exp199 deposit instance c{c} j{j} is incomplete"
            fmax = float(f_max_frames(list(med.snapshots())))
            t1 = int(med.T_eff) == 1

            # ---- GATE-B1: the bit-exact baseline replay -------------
            # THE one call site — the production read, scoped arm
            # (exp199's base arm, unchanged).
            b_errs, b_ver, b_rho, b_branch = [], [], [], []
            replay_flags = []
            for s, dep_err, dep_ver in zip(
                    seeds, dep_rec["errs"], dep_rec["verified"]):
                out = _m148.decode("scoped", med, s, f_max=fmax)
                if not out["ok"]:
                    n_rej["base"] += 1          # RECORDED, never hidden
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
                # err_vs_target to 2 dp — exp199's deposit is exact there)
                replay_flags.append(
                    round(err, 2) == float(dep_err)
                    and bool(out["verified"]) == bool(dep_ver))
            replay_exact = bool(b_errs and all(replay_flags)
                                and len(b_errs) == len(seeds))
            b_med = (float(np.median(b_errs))
                     if len(b_errs) == len(seeds) else None)

            # ---- GATE-B2/B4: the R_H arm (rule_hyper_S VERBATIM) ----
            # armed at the frames level on every instance; on
            # hyper-inactive media (no hyperedges) exp166's rule returns
            # the frames identity — the B4 no-op demonstration.
            frames = med.snapshots()
            rh_frames = rule_hyper_S(med, frames, F_RH)
            rh_noop_identity = rh_frames is frames
            wrapped = RepairedMedium(med, rh_frames, "hyper")
            fmax_rh = float(f_max_frames(list(wrapped.snapshots())))
            r_errs, r_ver, r_rho, r_branch = [], [], [], []
            for s in seeds:
                out = _m148.decode("scoped", wrapped, s,
                                   f_max=fmax_rh)
                if not out["ok"]:
                    n_rej["rh"] += 1            # RECORDED, never hidden
                    rej_records.append({"arm": "R_H", "j": j,
                                        "seed": s, "f_max": fmax_rh,
                                        "rejection": out["rejection"]})
                    continue
                err = float(out["err"])
                assert np.isfinite(err), \
                    f"non-finite R_H err at c{c} j{j} s{s}"
                r_errs.append(err)
                r_ver.append(bool(out["verified"]))
                r_rho.append(float(out["rho"])
                             if out.get("rho") is not None else None)
                r_branch.append(out.get("branch"))
                rh_errs_all.append(err)
            r_med = (float(np.median(r_errs))
                     if len(r_errs) == len(seeds) else None)
            delta = (round(r_med - b_med, 6)
                     if b_med is not None and r_med is not None
                     else None)
            drop_pct = (round((b_med - r_med) / b_med * 100.0, 4)
                        if b_med and r_med is not None else None)
            rh_rec = {"errs": r_errs, "verified": r_ver,
                      "rho": r_rho, "branch": r_branch,
                      "median_err": r_med, "f_max_rh": fmax_rh,
                      "delta_mV": delta, "drop_pct": drop_pct,
                      "noop_identity_frames": bool(rh_noop_identity),
                      "errs_bit_exact_vs_base":
                          bool(len(r_errs) == len(seeds)
                               and r_errs == b_errs)}

            # ---- GATE-B3: the R_T control + composition (c6, T=1) ---
            rt_rec = None
            comp_rec = None
            if c == TAIL_CELL:
                assert t1, "c6 media must be T=1 (the non-temporal cell)"
                raw_frames = med.snapshots()
                rt_frames = rule_temporal_core(med, raw_frames)
                rt_identity = all(np.array_equal(a, b)
                                  for a, b in zip(rt_frames, raw_frames))
                rt_wrapped = RepairedMedium(med, rt_frames, "temporal")
                fmax_rt = float(f_max_frames(list(rt_wrapped.snapshots())))
                t_errs, t_ver, t_rho, t_branch = [], [], [], []
                for s in seeds:
                    out = _m148.decode("scoped", rt_wrapped, s,
                                       f_max=fmax_rt)
                    if not out["ok"]:
                        n_rej["rt"] += 1        # RECORDED, never hidden
                        rej_records.append({"arm": "R_T", "j": j,
                                            "seed": s, "f_max": fmax_rt,
                                            "rejection": out["rejection"]})
                        continue
                    err = float(out["err"])
                    assert np.isfinite(err), \
                        f"non-finite R_T err at c{c} j{j} s{s}"
                    t_errs.append(err)
                    t_ver.append(bool(out["verified"]))
                    t_rho.append(float(out["rho"])
                                 if out.get("rho") is not None else None)
                    t_branch.append(out.get("branch"))
                    rt_errs_all.append(err)
                rt_rec = {"errs": t_errs, "verified": t_ver,
                          "rho": t_rho, "branch": t_branch,
                          "median_err": (float(np.median(t_errs))
                                         if len(t_errs) == len(seeds)
                                         else None),
                          "f_max_rt": fmax_rt, "t1": bool(t1),
                          "frames_identity_bit_exact": bool(rt_identity),
                          "errs_bit_exact_vs_base":
                              bool(len(t_errs) == len(seeds)
                                   and t_errs == b_errs)}
                # the composition: exp170's primary order (mask-then-
                # augment: rule_temporal_core THEN rule_hyper_S), same
                # zero-knob F — on T=1 it must equal R_H alone bit-exactly
                comp_frames = rule_hyper_S(med, rt_frames, F_RH)
                comp_eq_rh = all(np.array_equal(a, b)
                                 for a, b in zip(comp_frames, rh_frames))
                comp_wrapped = RepairedMedium(med, comp_frames,
                                              "temporal+hyper")
                fmax_c = float(f_max_frames(list(comp_wrapped.snapshots())))
                c_errs, c_ver, c_rho, c_branch = [], [], [], []
                for s in seeds:
                    out = _m148.decode("scoped", comp_wrapped, s,
                                       f_max=fmax_c)
                    if not out["ok"]:
                        n_rej["comp"] += 1      # RECORDED, never hidden
                        rej_records.append({"arm": "R_HxR_T", "j": j,
                                            "seed": s, "f_max": fmax_c,
                                            "rejection": out["rejection"]})
                        continue
                    err = float(out["err"])
                    assert np.isfinite(err), \
                        f"non-finite composition err at c{c} j{j} s{s}"
                    c_errs.append(err)
                    c_ver.append(bool(out["verified"]))
                    c_rho.append(float(out["rho"])
                                 if out.get("rho") is not None else None)
                    c_branch.append(out.get("branch"))
                    comp_errs_all.append(err)
                comp_rec = {"errs": c_errs, "verified": c_ver,
                            "rho": c_rho, "branch": c_branch,
                            "median_err": (float(np.median(c_errs))
                                           if len(c_errs) == len(seeds)
                                           else None),
                            "f_max_comp": fmax_c,
                            "frames_bit_exact_vs_rh": bool(comp_eq_rh),
                            "errs_bit_exact_vs_rh":
                                bool(len(c_errs) == len(seeds)
                                     and c_errs == r_errs)}

            rec = {"j": j, "gen_seed": gen_seed,
                   "n": int(med.n),
                   "violated": list(med.violated), "T": int(med.T_eff),
                   "n_hyper": int(med.n_hyper),
                   "n_oneway": int(med.n_oneway),
                   "hyper_active": hyper_active, "t1": bool(t1),
                   "tail": bool(dep_rec["median_err"] > BAR),
                   "dep199_median_err": dep_rec["median_err"],
                   "f_max": fmax,
                   "replay_bit_exact": replay_exact,
                   "errs": b_errs, "verified": b_ver,
                   "rho": b_rho, "branch": b_branch,
                   "median_err": b_med,
                   "rh": rh_rec, "rt": rt_rec, "comp": comp_rec}
            insts.append(rec)
            print(f"  [c{c} j{j:2d}] base med {rec['median_err']} "
                  f"replay {'exact' if replay_exact else 'DRIFT'}"
                  f" | R_H med {rh_rec['median_err']} "
                  f"delta {rh_rec['delta_mV']} mV "
                  f"({rh_rec['drop_pct']}%)"
                  + (f" | R_T noop {rt_rec['errs_bit_exact_vs_base']} "
                     f"comp==R_H {comp_rec['errs_bit_exact_vs_rh']}"
                     if rt_rec else ""))
        section = {
            "cell": c,
            "violation_class": ("+".join(med.violated)
                                if med.violated else "none"),
            "n_instances": len(insts), "seeds": list(seeds),
            "n_build": int(N400),
            "hyper_active": hyper_active,
            "rh_armed": True,
            "rt_comp_armed": c == TAIL_CELL,
            "n_base_decodes": len(base_errs_all),
            "n_rh_decodes": len(rh_errs_all),
            "n_rt_decodes": len(rt_errs_all),
            "n_comp_decodes": len(comp_errs_all),
            "n_rejections_base": n_rej["base"],
            "n_rejections_rh": n_rej["rh"],
            "n_rejections_rt": n_rej["rt"],
            "n_rejections_comp": n_rej["comp"],
            "rejection_records": rej_records,
            "median_err_base": (float(np.median(base_errs_all))
                                if base_errs_all else None),
            "median_err_rh": (float(np.median(rh_errs_all))
                              if rh_errs_all else None),
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
              f"R_H median {section['median_err_rh']} | "
              f"R_T/comp {'ARMED' if section['rt_comp_armed'] else 'not armed'} | "
              f"rejections base {section['n_rejections_base']} "
              f"rh {section['n_rejections_rh']} "
              f"rt {section['n_rejections_rt']} "
              f"comp {section['n_rejections_comp']} "
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
        return {"exp": "exp204_rh_rt_n400_tail", "smoke": True,
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
    n_rh_decodes = sum(result["cells"][k]["n_rh_decodes"]
                       for k in cells_present)
    n_rt_decodes = sum(result["cells"][k]["n_rt_decodes"]
                       for k in cells_present)
    n_comp_decodes = sum(result["cells"][k]["n_comp_decodes"]
                         for k in cells_present)
    n_rej_total = sum(result["cells"][k]["n_rejections_base"]
                      + result["cells"][k]["n_rejections_rh"]
                      + result["cells"][k]["n_rejections_rt"]
                      + result["cells"][k]["n_rejections_comp"]
                      for k in cells_present)
    rej_records = [x for k in cells_present
                   for x in result["cells"][k]["rejection_records"]]
    expected_base = len(insts_all) * len(seeds)
    expected_rh = len(insts_all) * len(seeds)
    expected_rt = (sum(len(result["cells"][k]["instances"])
                       for k in cells_present
                       if result["cells"][k]["rt_comp_armed"])
                   * len(seeds))
    expected_comp = expected_rt
    n400_ok = all(r.get("n") == N400 for r in insts_all)

    # GATE-B1: the spot replay (c6 tail + one clean cell, all seeds)
    spot_flags = []
    for sc in SPOT_CELLS:
        sec = result["cells"][f"c{sc}"]
        spot_flags += [r["replay_bit_exact"] for r in sec["instances"]]
    n_replay_all = sum(int(r["replay_bit_exact"]) for r in insts_all)
    u1 = bool(n_base_decodes == expected_base and n400_ok
              and spot_flags and all(spot_flags)
              and all(result["cells"][k]["n_rejections_base"] == 0
                      for k in cells_present))

    # GATE-B2: R_H on the tail
    rh_insts = [r for r in insts_all if r["hyper_active"]]
    rh_deltas = [r["rh"]["delta_mV"] for r in rh_insts
                 if r["rh"] and r["rh"]["delta_mV"] is not None]
    c6 = result["cells"]["c6"]
    tail6 = [r for r in c6["instances"] if r["tail"] and r["rh"]]
    tail6_deltas = [r["rh"]["delta_mV"] for r in tail6
                    if r["rh"]["delta_mV"] is not None]
    tail6_drops = [r["rh"]["drop_pct"] for r in tail6
                   if r["rh"]["drop_pct"] is not None]
    tail6_base = [r["median_err"] for r in tail6]
    tail6_rh = [r["rh"]["median_err"] for r in tail6]
    median_delta_mV = (float(np.median(tail6_deltas))
                       if tail6_deltas else None)
    median_drop_pct = (float(np.median(tail6_drops))
                       if tail6_drops else None)
    agg_base_median = (float(np.median(tail6_base))
                       if tail6_base else None)
    agg_rh_median = (float(np.median(tail6_rh))
                     if tail6_rh else None)
    agg_drop_pct = (round((agg_base_median - agg_rh_median)
                          / agg_base_median * 100.0, 4)
                    if agg_base_median and agg_rh_median is not None
                    else None)
    if median_drop_pct is None:
        branch = None
    elif median_drop_pct >= REPAIR_PCT:
        branch = "REPAIR"
    elif median_drop_pct > 0:
        branch = "PARTIAL"
    else:
        branch = "NEUTRAL-HARM"
    u2 = bool(len(rh_insts) == len(HYPER_CELLS) * PER_CELL
              and len(rh_deltas) == len(rh_insts)
              and all(result["cells"][k]["n_rejections_rh"] == 0
                      for k in cells_present)
              and branch in ("REPAIR", "PARTIAL", "NEUTRAL-HARM"))

    # GATE-B3: the R_T control + composition (c6, T=1)
    c6_insts = c6["instances"]
    b3_rt = bool(c6_insts
                 and all(r["rt"] and r["t1"]
                         and r["rt"]["frames_identity_bit_exact"]
                         and r["rt"]["errs_bit_exact_vs_base"]
                         for r in c6_insts)
                 and result["cells"]["c6"]["n_rejections_rt"] == 0)
    b3_comp = bool(c6_insts
                   and all(r["comp"]
                           and r["comp"]["frames_bit_exact_vs_rh"]
                           and r["comp"]["errs_bit_exact_vs_rh"]
                           for r in c6_insts)
                   and result["cells"]["c6"]["n_rejections_comp"] == 0)
    u3 = bool(b3_rt and b3_comp)

    # GATE-B4: hygiene + no-regression
    pooled_all = ([e for r in insts_all for e in r["errs"]]
                  + [e for r in insts_all if r["rh"]
                     for e in r["rh"]["errs"]]
                  + [e for r in c6_insts if r["rt"]
                     for e in r["rt"]["errs"]]
                  + [e for r in c6_insts if r["comp"]
                     for e in r["comp"]["errs"]])
    all_finite = all(np.isfinite(e) for e in pooled_all)
    pin_ok = all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP160_FLOOR
                 for m in PIN_MODULES)
    fp_ok = config_fingerprint() == fp == EXP160_FP
    inactive = [r for r in insts_all if not r["hyper_active"]]
    b4_noop = bool(inactive
                   and all(r["rh"] and r["rh"]["noop_identity_frames"]
                           and r["rh"]["errs_bit_exact_vs_base"]
                           for r in inactive))
    non_tail_active = [r for r in rh_insts if not r["tail"]]
    worst_regression = (max((r["rh"]["delta_mV"] for r in non_tail_active),
                            default=None)
                        if all(r["rh"] for r in non_tail_active) else None)
    b4_reg = bool(non_tail_active
                  and worst_regression is not None
                  and worst_regression <= NO_REGRESSION_MV + 1e-9)
    u4 = bool(n_rej_total == 0
              and len(pooled_all)
              == expected_base + expected_rh + expected_rt + expected_comp
              and all_finite and n400_ok and pin_ok and fp_ok
              and b4_noop and b4_reg)

    gates = {
        "B1_replay_exp199_deposit": {
            "pass": u1, "n_media": len(insts_all), "medium_n": N400,
            "baseline_decodes": n_base_decodes,
            "expected": expected_base,
            "spot_cells": list(SPOT_CELLS),
            "spot_def": ("the c6 tail cell + c5 (the hyper-inactive "
                         "clean cell), all instances, all seeds"),
            "spot_replay_bit_exact": bool(all(spot_flags)),
            "n_replay_exact_instances_all": n_replay_all,
            "n400_construction_asserted": bool(n400_ok),
            "rejections": sum(result["cells"][k]["n_rejections_base"]
                              for k in cells_present),
            "comparison": ("round(err, 2) == exp199's deposited errs and "
                           "verified flags equal, per (cell, j, seed); "
                           "exp142 rounds err_vs_target to 2 dp — the "
                           "deposit's rounding")},
        "B2_rh_on_c6_tail": {
            "pass": u2, "rh_armed_cells": HYPER_CELLS,
            "n_rh_armed_instances": len(rh_insts),
            "n_rh_decodes": n_rh_decodes,
            "rh_rejections": sum(result["cells"][k]["n_rejections_rh"]
                                 for k in cells_present),
            "per_instance_deltas_deposited":
                bool(len(rh_deltas) == len(rh_insts)),
            "f_rh": F_RH,
            "f_rh_source": ("exp166's pooled_F VERBATIM — median nonzero "
                            "|W| pooled over ALL frames of the registered "
                            "cohort's hyper-active media (c3/c6/c7 x 25), "
                            "computed BEFORE any R_H decode (L142's "
                            "zero-knob recipe; run-scope-independent — "
                            "every --job split shares this ONE F)"),
            "c6_tail": {
                "n_tail": len(tail6),
                "tail_def": f"exp199 median_err > BAR ({BAR} mV)",
                "median_delta_mV": median_delta_mV,
                "median_drop_pct": median_drop_pct,
                "tail_median_base": agg_base_median,
                "tail_median_rh": agg_rh_median,
                "aggregate_drop_pct": agg_drop_pct,
                "per_instance": [{"j": r["j"],
                                  "base": r["median_err"],
                                  "rh": r["rh"]["median_err"],
                                  "delta_mV": r["rh"]["delta_mV"],
                                  "drop_pct": r["rh"]["drop_pct"]}
                                 for r in tail6]},
            "branch": branch,
            "branch_rule": (f"REPAIR (median drop >= {REPAIR_PCT}%), "
                            f"PARTIAL (0 < drop < {REPAIR_PCT}%), "
                            f"NEUTRAL-HARM (median <= 0)")},
        "B3_rt_control_and_composition": {
            "pass": u3,
            "rt_noop": {
                "rule": "exp166's rule_temporal_core VERBATIM",
                "armed_on": "c6 (the battery's non-temporal cell, T=1)",
                "identity": "T=1 -> core = the frame's own support",
                "n_instances": len(c6_insts),
                "frames_identity_bit_exact": bool(b3_rt),
                "errs_bit_exact_vs_base": bool(b3_rt)},
            "composition": {
                "order": ("exp170's primary mask-then-augment: "
                          "rule_temporal_core THEN rule_hyper_S, "
                          "same zero-knob F"),
                "scope": "c6 (T=1 — R_T is the identity there)",
                "n_instances": len(c6_insts),
                "frames_bit_exact_vs_rh": bool(b3_comp),
                "errs_bit_exact_vs_rh": bool(b3_comp),
                "lesson": ("exp170's dominated-composition lesson: "
                           "deposited, pre-named, not an adoption "
                           "candidate unless R_H itself repairs")}},
        "B4_hygiene_no_regression": {
            "pass": u4, "n_decodes_total": len(pooled_all),
            "expected_total": (expected_base + expected_rh
                               + expected_rt + expected_comp),
            "rejections": n_rej_total, "rejection_records": rej_records,
            "all_errs_finite": bool(all_finite),
            "hyper_inactive_noop": {
                "cells": list(HYPER_INACTIVE_CELLS),
                "mechanism": ("exp166's rule_hyper_S returns the frames "
                              "identity when the medium has no "
                              "hyperedges — bit-exact by construction"),
                "n_instances": len(inactive),
                "identity_frames_and_bit_exact_errs": bool(b4_noop)},
            "hyper_active_non_tail": {
                "n_instances": len(non_tail_active),
                "no_regression_bar_mV": NO_REGRESSION_MV,
                "worst_regression_mV": worst_regression,
                "held": bool(b4_reg)},
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
    print(f"  c6 tail: base median {agg_base_median} mV -> R_H median "
          f"{agg_rh_median} mV (median per-instance delta "
          f"{median_delta_mV} mV, drop {median_drop_pct}%)")
    print(f"  R_T control on c6 (T=1): "
          f"{'bit-exact no-op, composition == R_H alone' if u3 else 'REFUTED'}")
    print(f"  hyper-active non-tail: {len(non_tail_active)} instances, "
          f"worst regression {worst_regression} mV, "
          f"{'within bars' if b4_reg else 'REFUTED'}")
    print(f"  hyper-inactive (c5, R_H identity): {len(inactive)} "
          f"instances, "
          f"{'bit-exact no-op' if b4_noop else 'REFUTED'}")

    result.update({
        "exp": "exp204_rh_rt_n400_tail",
        "claim": (
            "R_H (exp166's rule_hyper_S VERBATIM, L142's "
            "cancellation-density weighting) and R_T (exp166's "
            "rule_temporal_core VERBATIM) priced at n=400 on the c6 tail "
            "— L174's registered next after exp199 falsified R_O "
            "(NEUTRAL-HARM): exp199's n=400 battery rebuilt VERBATIM "
            "(its seed rule and exp181's cell definitions, "
            "CornerMedium(400, ...) at cells 3/5/6/7 x 25 instances x "
            "seeds (1,2,3)), the base arm = exp199's deposit replayed "
            "bit-exactly at the deposit's rounding (spot-assert on the "
            "c6 tail + c5, all seeds); R_H armed at the frames level on "
            "the hyper-active instances (the A-PAIR cells 3/6/7) with "
            "F = exp166's pooled_F over the registered cohort's "
            "hyper-active media computed BEFORE any R_H decode, the "
            "temporal dispatch = exp178's scoped arm under the -35.0 "
            "pin; the c6 tail's median delta "
            "names the branch (REPAIR / PARTIAL / NEUTRAL-HARM); R_T is "
            "the control — on the c6 tail's T=1 media exp166's "
            "rule_temporal_core is the frames identity, and the R_H x "
            "R_T composition (exp170's primary mask-then-augment order, "
            "same F) equals R_H alone bit-exactly; no-regression held on "
            "the hyper-inactive (identity by construction) and "
            "hyper-active non-tail instances"),
        "cohort": {
            "generator": (
                "exp199's battery VERBATIM — exp166's CornerMedium with "
                "n=400 as the constructor's FIRST PARAMETER, asserted "
                "med.n == 400 at every build"),
            "seed_base": EXP166_SEED_BASE,
            "seed_rule": "EXP166_SEED_BASE + 1000*c + j, j = 0..24",
            "cells": list(ADVERSARIAL_CELLS),
            "hyper_active_cells": list(HYPER_CELLS),
            "hyper_inactive_cells": list(HYPER_INACTIVE_CELLS),
            "tail_owner_cell": TAIL_CELL,
            "per_cell": PER_CELL, "n": N400,
            "n_media": len(insts_all), "seeds": list(seeds),
            "cell_classes": {k: result["cells"][k]["violation_class"]
                             for k in cells_present}},
        "repair_rule": {
            "rule": "R_H",
            "source": ("exp166's rule_hyper_S VERBATIM (L142's deposit at "
                       "the medium level), applied at the frames level "
                       "(RepairedMedium wrapper, rule='hyper')"),
            "description": (
                "cancellation-density weighting: A += F*S with S_ij = 1 "
                "iff i,j share a hyperedge and F the pre-decode pooled "
                "median nonzero |W|; identity (bit-exact) when the "
                "medium has no hyperedges"),
            "f_rh": F_RH,
            "f_recipe": (
                "exp166's pooled_F VERBATIM over the registered cohort's "
                "hyper-active media (c3/c6/c7 x 25 instances, ALL "
                "frames), computed BEFORE any R_H decode — "
                "run-scope-independent"),
            "armed_on": ("every hyper-active instance (A-PAIR cells "
                         "3/6/7); also run on the hyper-inactive control "
                         "(c5) where it is the identity by construction "
                         "— B4's bit-exact no-op demonstration"),
            "not_armed_on": None},
        "control_rule": {
            "rule": "R_T",
            "source": ("exp166's rule_temporal_core VERBATIM, applied at "
                       "the frames level (RepairedMedium wrapper, "
                       "rule='temporal')"),
            "description": (
                "flip-quiet windowing: every frame masked to the "
                "across-frame CORE support; on T=1 media core = the "
                "frame's own support — the frames identity"),
            "armed_on": ("the c6 tail cell only (the battery's "
                         "non-temporal cell, T=1) — where the "
                         "pre-registered identity holds")},
        "composition": {
            "order": ("exp170's primary mask-then-augment: "
                      "rule_temporal_core THEN rule_hyper_S, same "
                      "zero-knob F"),
            "f": F_RH, "scope": "c6 (T=1)",
            "expectation": ("equals R_H alone bit-exactly (the exp170 "
                            "dominated-composition lesson: deposited, "
                            "pre-named, not an adoption candidate unless "
                            "R_H itself repairs)")},
        "read": {**READ_CONFIG,
                 "fingerprint": fp,
                 "fingerprint_asserted": EXP160_FP,
                 "medium_n": N400,
                 "medium_n_note": (
                     "READ_CONFIG's 'n': 100 field is exp160's "
                     "deposited fingerprint of record (asserted "
                     "unchanged pre/post run); the decode stack is "
                     "size-agnostic — exp204's cohort knob is the "
                     "CornerMedium construction n=400, as in "
                     "exp198/exp199"),
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
                     "note": ("the -35.0 comparability pin on every "
                              "module that captured it at import along "
                              "the read chain (exp199's pattern, "
                              "save/restore asserted)")}},
        "replay_target": {
            "deposit": "results/exp199_ro_n400_tail.json",
            "exp199_verdict": dep199["verdict"],
            "exp199_branch": dep199["gates"][
                "A2_ro_on_oriented_cells"]["branch"],
            "exp199_c6_tail": dep199["gates"][
                "A2_ro_on_oriented_cells"]["c6_tail"]},
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
