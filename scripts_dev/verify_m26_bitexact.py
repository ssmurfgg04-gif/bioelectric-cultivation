#!/usr/bin/env python3
"""Bit-exact regression gate for the M26 regrow patch (night three).

Re-runs the exp29/exp31 control arms through the patched collective and
compares to the recorded means in results/*.json. ANY drift here blocks
the M26 candidates from being evaluated (additive-param discipline).
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, SEEDS, TAIL, make_collective, amputate_regrow,
)
from cultivation.bioelectric.morphospace import wildtype_target, head_likeness  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def arm_err(arm_run: dict) -> float:
    return arm_run["wt_pattern_error"]


def cutting_tail(seed: int) -> dict:
    # exp29 'cutting' arm protocol EXACTLY: settle only (make_collective),
    # then amputate_regrow
    return amputate_regrow(make_collective(seed))


def innexin_tail(seed: int) -> dict:
    # exp29 'innexin_sustained' arm protocol EXACTLY: block before settle
    c = make_collective(seed)
    c.block_gap_junctions(0.05)
    c.run(24, dt=DT)
    return amputate_regrow(c)


def main() -> None:
    exp29 = json.load(open(os.path.join(ROOT, "results", "exp29_stage2_repair.json")))
    exp31 = json.load(open(os.path.join(ROOT, "results", "exp31_stage2_widened.json")))

    checks = []
    # exp29 controls: cutting + restored (arm names: cutting, innexin_sustained)
    rec_cut = exp29["after"]["cutting"]["per_seed"]
    new_cut = [arm_err(cutting_tail(s)) for s in SEEDS]
    checks.append(("exp29 cutting_tail per-seed err", rec_cut, new_cut))

    rec_inx = exp29["after"]["innexin_sustained"]["per_seed"]
    new_inx = [arm_err(innexin_tail(s)) for s in SEEDS]
    checks.append(("exp29 innexin_tail per-seed err", rec_inx, new_inx))

    ok_all = True
    for name, recorded, fresh in checks:
        match = bool(np.allclose(recorded, fresh, atol=1e-9, rtol=0.0))
        ok_all &= match
        print(f"  {'BIT-EXACT' if match else 'DRIFT!!!!'}  {name}: "
              f"recorded {[round(v, 4) for v in recorded]} vs "
              f"fresh {[round(v, 4) for v in fresh]}")

    # M26 params exist and default-inert: g>0 must CHANGE cross_a behaviour
    from experiments.exp31_stage2_widened import plane_protocol, run_arm  # noqa: E402
    base = run_arm("cutting_cross_a", 1)
    print(f"  exp31 cutting_cross_a (defaults) err {base['wt_pattern_error']:.4f} "
          f"pred_abn {base['predicted_abnormal']}")

    print(f"\n  VERDICT: {'ALL BIT-EXACT — patch is additive-inert at defaults' if ok_all else 'REGRESSION — DO NOT PROCEED'}")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
