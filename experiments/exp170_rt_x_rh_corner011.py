#!/usr/bin/env python3
"""exp170 — R_T x R_H CROSS-CHECK ON THE 011 CELL (L145's follow-up).

exp145's registered next (via L147): "R_T x R_H cross-check on the 011
corner cell (L145's registered follow-up)" — the h+t cell (o=0, h=1,
t=1, cell index c = 4o+2h+t = 3) where exp166's above-bar tail lives
(9/50 main-battery instances above the 1.30 bar; cell median 0.820 mV
vs clean 0.670). exp166's P4 spot battery ran the single-rule mapping
ONLY (temporal -> R_T on the 111 corner and clean cells). The composed
rule on the 011 cell is untested. THIS EXPERIMENT runs it.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Arms, composition order, and gates are
fixed now; the credited run uses this file unchanged.

THE TWO RULES (both zero-knob, both deposited):
  R_T = exp166's rule_temporal_core VERBATIM (L140's flip-quiet
        discipline at the medium level: mask every frame to the
        across-frame core support; membership frozen).
  R_H = exp166's rule_hyper_S VERBATIM (L142's deposit at the medium
        level: A += F * S with S = co-hyperedge adjacency, F = the
        pre-decode pooled median nonzero |W| — pooled_F over the spot
        instances, computed BEFORE any decode).

THE COMPOSITION — the two rules act on DIFFERENT channels (R_T on the
  frame support/temporal channel, R_H on the projection's augmentation
  via hyperedge co-membership) and compose NON-trivially. Order is
  fixed by the data flow and named BEFORE the run:
    PRIMARY (mask-then-augment): frames' = R_T(frames); then the read
      computes A = project(frames') and A_ext = A + F' * S where F' =
      pooled median nonzero |W| of the MASKED frames (R_H's F computed
      on the masked frames — the augmentation reads the window it
      will decode) and S = the medium's co-hyperedge adjacency.
    REVERSED (augment-then-mask): frames'' = R_H(frames) i.e. each
      frame Wt + F * S with F = pooled |W| of the RAW frames; then
      R_T masks the augmented frames. Recorded arm, not primary.
  Both orders are zero-knob compositions of the two deposited rules;
  no third rule, no interpolation, no tuning.

INSTRUMENTS (zero new calibration):
  * exp166's module verbatim: CornerMedium (SEED_BASE 166166),
    rule_hyper_S, rule_temporal_core, pooled_F, the exp160 read stack
    via exp166's own dispatch, cell_dims.
  * THE PIN (exp167's mechanism, disclosed pre-run): exp166's deposit
    predates CF-1, so NEURAL_SPEC_MIN is pinned to -35.0 in every
    module whose bound name the read chain consults
    (cultivation.bioelectric.collective, exp142, exp145, exp148,
    exp94) — save/restore asserted; exp166's arm-A/B records were
    produced at that floor.
  * Deposit read at run time: results/exp166_leading_edge.json (the
    011 cell's main-battery stats: median, above-bar count).
  * Spot set: CornerMedium(n=100, seed = 166166 + 1000*3 + j),
    j = 0..9 (cell c=3, the 011 h+t cell), seeds (1, 2, 3) — 30
    decodes per arm, exp166's spot protocol verbatim.

ARMS (each exactly once, same 30 decodes):
  A0 raw          — exp160's stack verbatim, no rule.
  A1 R_T alone    — rule_temporal_core on the frames.
  A2 R_H alone    — rule_hyper_S on the frames (F from raw pooled |W|).
  A3 COMPOSED     — mask-then-augment (PRIMARY, defined above).
  A4 reversed     — augment-then-mask (recorded).

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-C1 (raw replay + tail presence) A0: zero rejections, all errs
           finite; the 30 raw errs deposited with per-instance
           medians; >= 5/10 spot instances' medians above exp160's
           deposited pooled median 0.630 (the cell is a tail cell —
           if the spot set fails to reproduce tail character, the
           construction is flagged and everything else deposited
           honestly with the construction caveat).
  GATE-C2 (single-rule prices) A1 and A2 medians and per-instance
           deltas vs A0 deposited; no pass bar — this gate PRICES the
           two channels separately so the composition's effect is
           attributable (record = pass always, values are the
           deposit).
  GATE-C3 (the composed rule) A3 vs A0: median(A3) < median(A0)
           AND >= 8/10 spot instances improved (per-instance median
           A3 < A0) AND median(A3) <= 0.60 mV (exp160's clean-cell
           parity bar — the L145-style "lands at clean scale"
           clause). Partial outcomes deposited honestly (median
           improvement without the parity bar = 2/3 clauses).
  GATE-C4 (order sensitivity + hygiene) A4 median deposited; the
           sign of median(A4) - median(A3) recorded (no bar);
           zero rejections across all five arms; the pin save/
           restore asserted in the deposit.

NO post-hoc knob tuning anywhere; exactly ONE composed rule is
primary. A --smoke instrument check (j = 0 only, seeds (1,)) is
permitted before the credited run and discarded; the credited full
run uses the committed script unchanged.

DEPOSIT: results/exp170_rt_x_rh_corner011.json

RUN:
  python3 -m experiments.exp170_rt_x_rh_corner011              # full
  python3 -m experiments.exp170_rt_x_rh_corner011 --smoke      # check
  python3 -m experiments.exp170_rt_x_rh_corner011 --arm A3     # split
  # arms: A0 | A1 | A2 | A3 | A4
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
    pooled_F, rule_hyper_S, rule_temporal_core,
)

# ---- run-agent additions: the docstring's remaining instruments
# (exp166's module VERBATIM: its read dispatch = read_temporal, the cell
# spec, the spot wrapper, the config fingerprint) + a runtime stamp.
# The pre-registered blocks above and below are byte-unchanged. --------
import time  # noqa: E402

from experiments.exp166_leading_edge import (  # noqa: E402
    RepairedMedium, cell_dims, config_fingerprint, read_temporal,
)

# ---- INSTRUMENT PIN (see docstring) --------------------------------
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP166_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP166_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


# ---- FIXED CONSTANTS ------------------------------------------------
CELL_011 = 3                                   # c = 4o + 2h + t = 3
SPOT_J = list(range(10))
SPOT_SEEDS = (1, 2, 3)
CLEAN_PARITY_BAR = 0.60                        # exp160's pooled median
IMPROVED_MIN = 8                               # of 10 instances

OUT = os.path.join(ROOT, "results", "exp170_rt_x_rh_corner011.json")
DEP166 = os.path.join(ROOT, "results", "exp166_leading_edge.json")

# ---- run-agent additions (named from the docstring's fixed gates) ----
TAIL_REF = 0.630                # exp160's deposited pooled median (C1 bar)
ARMS = ("A0", "A1", "A2", "A3", "A4")
ARM_DOC = {
    "A0": "raw — exp160's stack verbatim, no rule (decoded on the medium)",
    "A1": "R_T alone — rule_temporal_core on the frames",
    "A2": "R_H alone — rule_hyper_S on the frames (F from raw pooled |W|)",
    "A3": "COMPOSED PRIMARY — mask-then-augment (R_T first, R_H's F' from "
          "the masked frames)",
    "A4": "reversed — augment-then-mask (R_H with F from raw frames, then "
          "R_T masks)",
}


def frames_of(med: CornerMedium) -> list[np.ndarray]:
    return [Wt.copy() for Wt in med.snapshots()]


# ---- run-agent helpers ----------------------------------------------
def median_of(xs: list) -> float | None:
    """exp166's median over non-None values; None when nothing decoded."""
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None


def pooled_F_frames(frame_sets: list[list[np.ndarray]]) -> float:
    """pooled_F's statistic (median of the NONZERO |W_ij| pooled over ALL
    frames) over already-ruled frame lists — exp166's pooled_F body
    verbatim modulo the source of the frames (R_T's masked output)."""
    vals: list[np.ndarray] = []
    for frames in frame_sets:
        for Wt in frames:
            a = np.abs(Wt)
            vals.append(a[a > 0])
    return float(np.median(np.concatenate(vals)))


def arm_frames(arm: str, med: CornerMedium, F_raw: float,
               F_masked: float) -> list[np.ndarray]:
    """The arm's frames; the composition order is the docstring's, fixed:
    A3 PRIMARY = mask-then-augment (R_H's F' reads the masked window it
    will decode), A4 = augment-then-mask (R_H's F from the RAW frames).
    Both are zero-knob compositions of the two deposited rules."""
    raw = frames_of(med)
    if arm == "A0":
        return raw
    if arm == "A1":
        return rule_temporal_core(med, raw)
    if arm == "A2":
        return rule_hyper_S(med, raw, F_raw)
    if arm == "A3":                              # PRIMARY, mask-then-augment
        return rule_hyper_S(med, rule_temporal_core(med, raw), F_masked)
    if arm == "A4":                           # REVERSED, augment-then-mask
        return rule_temporal_core(med, rule_hyper_S(med, raw, F_raw))
    raise ValueError(arm)


def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--arm", choices=list(ARMS) + ["all"], default="all")
    ap.add_argument("--out", default=None)
    args, _ = ap.parse_known_args()
    smoke = bool(args.smoke)
    spot_j = [0] if smoke else list(SPOT_J)
    seeds = (1,) if smoke else tuple(SPOT_SEEDS)
    arms = [args.arm] if args.arm != "all" else list(ARMS)
    full = (not smoke) and args.arm == "all"
    # deposit policy: the full run deposits (to --out or the default OUT);
    # a split run deposits ONLY with an explicit --out (it must never
    # touch the credited deposit); smoke NEVER deposits.
    deposit = full or (not smoke and args.out is not None)
    out_path = args.out if args.out else OUT
    t0 = time.time()
    mode = "SMOKE" if smoke else ("FULL" if full else f"SPLIT {args.arm}")
    print(f"=== exp170: R_T x R_H CROSS-CHECK ON THE 011 CELL ({mode}) ===")
    print(f"  cell c={CELL_011} (o=0,h=1,t=1)  j={spot_j}  seeds={list(seeds)}"
          f"  arms={arms}\n")

    # ---- deposits read at run time (011 main-battery anchor + fp)
    with open(DEP166) as f:
        dep166 = json.load(f)
    cell3 = next(c for c in dep166["cells"] if c["cell"] == CELL_011)
    fp = config_fingerprint()
    assert fp == dep166["config"]["fingerprint"], (
        f"config fingerprint {fp} != exp166's deposited read stack")

    spot_media = [CornerMedium(100,
                               seed=EXP166_SEED_BASE + 1000 * CELL_011 + j,
                               dims=cell_dims(CELL_011)) for j in spot_j]
    spot_meta = [{"j": j, "gen_seed": m.seed, "n_hyper": m.n_hyper,
                  "p_keep": round(m.p_keep, 3), "T": m.T_eff,
                  "violated": list(m.violated)}
                 for j, m in zip(spot_j, spot_media)]

    # ---- the two F statistics, computed BEFORE any decode
    F_raw = pooled_F(spot_media)                  # exp166's pooled_F verbatim
    F_masked = pooled_F_frames(                   # R_H's F on the MASKED frames
        [rule_temporal_core(m, frames_of(m)) for m in spot_media])
    print(f"  F_raw (raw pooled |W|)     {F_raw:.6f}\n"
          f"  F_masked (masked pooled |W|) {F_masked:.6f}"
          f"   (both pooled over all spot frames, BEFORE any decode)")

    pin_floor()
    rejections: list[dict] = []
    arm_records: dict[str, dict] = {}
    try:
        for arm in arms:
            instances = []
            for j, med in zip(spot_j, spot_media):
                fr = arm_frames(arm, med, F_raw, F_masked)
                target = (med if arm == "A0"
                          else RepairedMedium(med, fr, ARM_DOC[arm]))
                errs, vs, branches, rhos = [], [], [], []
                for s in seeds:
                    try:
                        out = read_temporal(target, s)
                        err = float(out["err_vs_target"])
                        if not np.isfinite(err):
                            raise ValueError(f"non-finite decode err {err}")
                        errs.append(err)
                        vs.append(bool(out["program_verified"]))
                        branches.append(out["branch"])
                        rhos.append(round(float(out["rho"]), 4))
                    except Exception as e:       # RECORDED, never hidden
                        rejections.append(
                            {"arm": arm, "j": j, "seed": s,
                             "rejection": f"{type(e).__name__}: {e}"[:200]})
                instances.append({
                    "arm": arm, "j": j, "gen_seed": med.seed,
                    "violated": list(med.violated),
                    "n_hyper": med.n_hyper, "p_keep": round(med.p_keep, 3),
                    "T": med.T_eff, "errs": errs,
                    "median_err": median_of(errs), "verified": vs,
                    "branch": branches, "rho": rhos, "config_fp": fp,
                })
            arm_records[arm] = {
                "arm": arm, "definition": ARM_DOC[arm],
                "instances": instances,
                "median_of_instance_medians": median_of(
                    [r["median_err"] for r in instances]),
                "pooled_median_all_decodes": median_of(
                    [e for r in instances for e in r["errs"]]),
                "n_decodes": sum(len(r["errs"]) for r in instances),
                "n_rejections": sum(1 for x in rejections
                                    if x["arm"] == arm),
            }
            a = arm_records[arm]
            print(f"  [{arm}] median-of-instance-medians "
                  f"{a['median_of_instance_medians']}  pooled "
                  f"{a['pooled_median_all_decodes']}  decodes "
                  f"{a['n_decodes']}  rejections {a['n_rejections']}")
    finally:
        restore_floor()
    pin_ok = all(getattr(m, "NEURAL_SPEC_MIN", None)
                 == _PIN_SAVE[m.__name__] for m in PIN_MODULES)
    assert pin_ok, "instrument pin save/restore FAILED"

    gates: dict | None = None
    if set(arm_records) == set(ARMS) and not smoke:
        a0, a1, a2, a3, a4 = (arm_records[k] for k in ARMS)
        med_of = lambda rec: rec["median_of_instance_medians"]   # noqa: E731
        per = lambda rec: {r["j"]: r["median_err"]               # noqa: E731
                           for r in rec["instances"]}

        # ---- GATE-C1 (raw replay + tail presence), evaluated once
        a0_per = per(a0)
        n_above = sum(1 for v in a0_per.values()
                      if v is not None and v > TAIL_REF)
        all_finite = all(np.isfinite(e) for r in a0["instances"]
                         for e in r["errs"])
        tail_ok = bool(n_above >= 5)
        c1 = bool(a0["n_rejections"] == 0 and all_finite and tail_ok)
        gates = {"C1_raw_replay_tail": {
            "pass": c1,
            "zero_rejections_A0": a0["n_rejections"] == 0,
            "all_errs_finite": bool(all_finite),
            "raw_errs_flat_30": [e for r in a0["instances"]
                                 for e in r["errs"]],
            "per_instance_medians": a0_per,
            "n_above_exp160_pooled": n_above,
            "required": 5, "TAIL_REF": TAIL_REF,
            "tail_clause_ok": tail_ok,
            "construction_caveat": (None if tail_ok else
                "the spot set failed to reproduce tail character "
                "(< 5/10 instance medians above exp160's deposited pooled "
                "median 0.630) — construction flagged; everything else "
                "deposited honestly with this caveat (registered clause)"),
        }}

        # ---- GATE-C2 (single-rule prices): record = pass always
        d1 = {j: (per(a1)[j] - a0_per[j])
              if (per(a1)[j] is not None and a0_per[j] is not None) else None
              for j in a0_per}
        d2 = {j: (per(a2)[j] - a0_per[j])
              if (per(a2)[j] is not None and a0_per[j] is not None) else None
              for j in a0_per}
        gates["C2_single_rule_prices"] = {
            "pass": True,
            "note": ("no pass bar — this gate PRICES the two channels "
                     "separately so the composition's effect is "
                     "attributable (record = pass always, values are the "
                     "deposit)"),
            "A1_median": med_of(a1), "A1_pooled": a1["pooled_median_all_decodes"],
            "A2_median": med_of(a2), "A2_pooled": a2["pooled_median_all_decodes"],
            "A0_median": med_of(a0),
            "per_instance_delta_A1_minus_A0": d1,
            "per_instance_delta_A2_minus_A0": d2,
        }

        # ---- GATE-C3 (the composed rule, A3 vs A0)
        a0m, a3m = med_of(a0), med_of(a3)
        improved = sorted(j for j in a0_per
                          if per(a3).get(j) is not None
                          and a0_per[j] is not None
                          and per(a3)[j] < a0_per[j])
        median_improved = bool(a0m is not None and a3m is not None
                               and a3m < a0m)
        parity_ok = bool(a3m is not None and a3m <= CLEAN_PARITY_BAR)
        count_ok = bool(len(improved) >= IMPROVED_MIN)
        c3 = bool(median_improved and count_ok and parity_ok)
        gates["C3_composed_rule"] = {
            "pass": c3,
            "median_A0": a0m, "median_A3": a3m,
            "median_improved": median_improved,
            "n_instances_improved": len(improved),
            "improved_instances": improved,
            "required": IMPROVED_MIN,
            "parity_bar": CLEAN_PARITY_BAR, "parity_ok": parity_ok,
            "clauses": ("median(A3) < median(A0) AND >= 8/10 spot "
                        "instances improved AND median(A3) <= 0.60 mV"),
        }

        # ---- GATE-C4 (order sensitivity + hygiene)
        a4m = med_of(a4)
        zero_rej_all = sum(a["n_rejections"]
                           for a in arm_records.values()) == 0
        diff = (a4m - a3m) if (a4m is not None and a3m is not None) else None
        sign = ("+" if diff > 0 else ("-" if diff < 0 else "0")) \
            if diff is not None else None
        c4 = bool(zero_rej_all and pin_ok and a4m is not None)
        gates["C4_order_sensitivity_hygiene"] = {
            "pass": c4,
            "median_A4": a4m, "A4_definition": ARM_DOC["A4"],
            "sign_median_A4_minus_A3": sign,
            "median_A4_minus_A3": diff,
            "zero_rejections_all_arms": zero_rej_all,
            "pin_save_restore_ok": bool(pin_ok),
        }

        n_pass = sum(int(g["pass"]) for g in gates.values())
        verdict = f"{n_pass}/4 gates"
        print(f"\n  C1 tail: {n_above}/10 above {TAIL_REF}  |  C3: "
              f"{a0m} -> {a3m} (improved {len(improved)}/10, parity bar "
              f"{CLEAN_PARITY_BAR})  |  A4 {a4m} (sign {sign})")
        print(f"  GATES: {verdict}  "
              + " ".join(f"{k.split('_')[0]}={int(g['pass'])}"
                         for k, g in gates.items()))
    else:
        n_pass = None
        verdict = "smoke (instrument check — discarded, not a deposit)" \
            if smoke else f"split run ({args.arm}) — gates evaluate on the full run only"
        print(f"  {verdict}")
    print(f"  rejections {len(rejections)}  pin save/restore {pin_ok}")

    result = {
        "exp": "exp170_rt_x_rh_corner011",
        "claim": (
            "exp145's registered follow-up via L145/L147: the R_T x R_H "
            "CROSS-CHECK on the 011 h+t corner cell (c=3, exp166's "
            "above-bar tail 9/50, cell median 1.075 vs clean 0.670) — the "
            "COMPOSED zero-knob rule (R_T mask-then-R_H augment, F' from "
            "the masked frames) vs both single rules and the reversed "
            "order on exp166's spot protocol verbatim (10 instances x "
            "seeds 1,2,3 = 30 decodes per arm, exp148's read_temporal via "
            "exp166's dispatch, NEURAL_SPEC_MIN pinned to the deposited "
            "-35.0 floor)"),
        "pre_registration": {
            "registered_next_source": ("L147 (exp167): R_T x R_H "
                                       "cross-check on the 011 corner cell "
                                       "— L145's registered follow-up"),
            "pre_reg_commit": "319c352",
            "docstring": "unchanged (gates C1-C4 + arms + composition "
                         "order fixed before any decode)",
            "arms": ARM_DOC,
            "composition": {
                "primary": ("mask-then-augment: frames' = R_T(frames); "
                            "R_H's F' = pooled median nonzero |W| of the "
                            "MASKED frames (the augmentation reads the "
                            "window it will decode); on the flip-quiet "
                            "window the flip clock is 0, so A_ext = "
                            "A_masked + F'*S with S the medium's "
                            "co-hyperedge adjacency"),
                "reversed": ("augment-then-mask: frames'' = R_H(frames) "
                             "with F from the RAW frames; then R_T masks "
                             "the augmented frames"),
            },
            "seed_rule": ("166166 + 1000*3 + j, j = 0..9 (cell c=3); "
                          "seeds (1,2,3); 30 decodes per arm"),
        },
        "config": {
            "read_stack": ("exp148's read_temporal VERBATIM via exp166's "
                           "dispatch (exp145 PN1/PN2 + TC1 flip-clock + "
                           "TC2 A_ext=A+F + exp142's execute_signed, spec "
                           "exp94 MULTI, STAR_OP); the rule lives entirely "
                           "in the frames a wrapper yields"),
            "fingerprint": fp,
            "fingerprint_asserted_eq_exp166": True,
            "n": 100, "cell": CELL_011,
            "cell_dims": cell_dims(CELL_011),
            "seeds": list(seeds), "spot_j": spot_j,
            "spot_protocol": "exp166's P4 verbatim (rules applied to "
                             "frames, wrapped, read verbatim)",
        },
        "instrument_pin": {
            "constant": "NEURAL_SPEC_MIN", "pinned_to": DEP166_FLOOR,
            "working_tree_values_seen": _PIN_SAVE,
            "modules": [m.__name__ for m in PIN_MODULES],
            "save_restore_ok": bool(pin_ok),
            "reason": ("exp166's deposit predates CF-1 (exp168's -60.0 "
                       "core patch); the pin restores the deposited -35.0 "
                       "floor world for this run only (exp167's "
                       "mechanism, disclosed pre-run)"),
        },
        "deposits_read": {
            "exp166_leading_edge": {
                "cell_011_main_battery": {
                    "median_err": cell3["median_err"],
                    "n_above_bar": cell3["n_above_bar"], "n": cell3["n"]},
                "config_fingerprint": dep166["config"]["fingerprint"],
            },
            "exp160_pooled_median_mV": TAIL_REF,
        },
        "spot_set": {"instances": spot_meta,
                     "cell": CELL_011, "n_instances": len(spot_media)},
        "F_statistics": {
            "F_raw_pooled_median_nonzero_absW": F_raw,
            "F_masked_pooled_median_nonzero_absW": F_masked,
            "F_raw_used_by": ["A2", "A4"], "F_masked_used_by": ["A3"],
            "pooled_over": ("all frames of the spot instances (cell c=3, "
                            "j = 0..9)"),
            "computed_before_any_decode": True,
        },
        "arms": arm_records,
        "gates": gates,
        "verdict": verdict,
        "rejections": rejections,
        "runtime_s": round(time.time() - t0, 1),
    }
    if deposit:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(result, f, indent=1)
        print(f"  deposited {out_path}")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--arm", choices=["A0", "A1", "A2", "A3", "A4",
                                      "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--arm/--out)
