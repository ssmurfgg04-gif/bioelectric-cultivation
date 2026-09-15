#!/usr/bin/env python3
"""exp30 — CEM CONTINUATION: DeepScientist night-one Thread A.

exp28's search was recorded as "still improving on the last step — not
certified exhausted". This module resumes the search EXACTLY from the
preserved checkpoint (scripts_dev/exp28_cem.ckpt -> copied to exp30_cem.ckpt;
cem_optimize restores mu, sigma, best-so-far and the bit-generator state, so
the continuation is the same search, not a new one) and runs 10 more
iterations at the original protocol (pop 24, elite 0.25, search seeds 41/42,
seed 27, smooth 0.7). Baseline: disc28, the user's suggested preset
(held-out hold 0.683, +0.058 over the exp25 transplant).

PRE-REGISTERED:
  X1 (CONTINUATION PAYS): held-out hold(new best) >= held-out
     hold(disc28) + 0.02 on exp25's eval world (seeds 21-23, K=200,
     120yr) — exp28's C1 bar. Failing => disc28 was already at (or
     within 0.02 of) the competitive optimum: the search is certified
     exhausted instead — recorded either way, both readings are results.
  X2 (SEARCH-SIDE TRAJECTORY): the resumed best fitness improves on
     exp28's final search fitness (-0.7180). Purely diagnostic.
  X3 (ROBUSTNESS, exploratory): policy divergence between the continued
     best and disc28 in the exp28 C2 sense (>=1 schedule param shifted
     >= 25%).
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cultivation.inverse.cem import cem_optimize  # noqa: E402
from experiments import exp28_cem_search_competition as e28  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CKPT28 = os.path.join(ROOT, "scripts_dev", "exp28_cem.ckpt")
CKPT30 = os.path.join(ROOT, "scripts_dev", "exp30_cem.ckpt")
STATE28 = os.path.join(ROOT, "scripts_dev", "exp28_state.json")
OUT = os.path.join(ROOT, "results", "exp30_cem_continuation.json")

ITERS_TOTAL_DEFAULT = 20
POOL_SIZE = 0   # serial: 2-core box + BLAS thread contention made Pool(2) ~5x SLOWER


def main() -> dict:
    argv = sys.argv[1:]
    iters_target = int(argv[0]) if argv else ITERS_TOTAL_DEFAULT
    do_eval = bool(argv) and "eval" in argv
    print(f"=== exp30: CEM continuation (target iters={iters_target}, "
          f"eval={do_eval}) ===", flush=True)
    if not os.path.exists(CKPT30):
        shutil.copy(CKPT28, CKPT30)
        print("  checkpoint copied exp28 -> exp30 (resume anchor)")

    st28 = json.load(open(STATE28))
    disc28_u = np.asarray(st28["discovered_u"], float)
    disc28_search_hold = float(st28["search_hold"])
    print(f"  exp28 search best: fitness -{disc28_search_hold:.4f} "
          f"(hold {disc28_search_hold:.4f} on seeds 41/42)")

    pool = None
    try:
        from multiprocessing import Pool
        pool = Pool(POOL_SIZE)
        t0, f0 = time.time(), e28._fitness(disc28_u)
        print(f"  pool up; re-eval disc28 on search world: {f0:.4f} "
              f"({time.time()-t0:.1f}s)")
    except Exception as exc:                      # pragma: no cover
        print(f"  pool unavailable ({exc}); continuing serial")
        pool = None

    t0 = time.time()
    best_u, best_f, history = cem_optimize(
        e28._fitness, e28.BOUNDS, pop=e28.POP, elite_frac=e28.ELITE,
        iters=iters_target, seed=27, verbose=True, pool=pool,
        checkpoint=CKPT30,
    )
    print(f"  continuation: {len(history)} iters total, "
          f"{time.time()-t0:.0f}s wall", flush=True)
    if pool is not None:
        pool.close()
        pool.join()

    # persist search state EVERY chunk (checkpoint is authoritative anyway)
    with open(os.path.join(ROOT, "scripts_dev", "exp30_state.json"),
              "w") as f:
        json.dump({"discovered_u": [float(x) for x in best_u],
                   "search_hold": float(-best_f),
                   "iters_total": iters_target,
                   "history": [(int(i), float(bf), [float(x) for x in mu])
                               for i, bf, mu in history]}, f, indent=1)

    if not do_eval:
        print("  state saved; eval deferred", flush=True)
        return {}

    # ---- held-out eval: new best vs disc28 (exp28's eval world verbatim) ---
    print("\n  held-out eval (seeds 21-23, K=200, 120yr):", flush=True)
    new_pol = e28.decode(best_u)
    disc28_pol = e28.decode(disc28_u)
    new_pol["h_proc"] = e28.H_PROC          # decode() omits it; exp28's
    disc28_pol["h_proc"] = e28.H_PROC       # _fitness adds it manually
    agg_new = e28._agg(new_pol)
    agg_28 = e28._agg(disc28_pol)
    print(f"    disc28      hold {agg_28['hold_mean']:.4f}  "
          f"median {agg_28.get('median', float('nan')):.1f}")
    print(f"    cont-best   hold {agg_new['hold_mean']:.4f}  "
          f"median {agg_new.get('median', float('nan')):.1f}")

    delta = agg_new["hold_mean"] - agg_28["hold_mean"]
    x1 = bool(delta >= 0.02)
    x2 = bool(-best_f > disc28_search_hold)
    sched = ["write_age", "start_age", "period", "budget"]
    shifts = {k: abs(new_pol[k] - disc28_pol[k]) / max(abs(disc28_pol[k]),
                                                       1e-9) for k in sched}
    x3 = bool(any(v >= 0.25 for v in shifts.values()))

    print(f"\n  X1 continuation pays (+0.02 held-out): "
          f"{'PASS' if x1 else 'REFUTED'} (delta {delta:+.4f})")
    print(f"  X2 search-side improvement:             "
          f"{'PASS' if x2 else 'REFUTED'}")
    print(f"  X3 schedule divergence (exploratory):   {x3} {shifts}")

    out = {
        "exp": "exp30_cem_continuation",
        "baseline": "disc28 (exp28), user-suggested preset",
        "protocol": {
            "iters_total": iters_target, "continued_from": "exp28_cem.ckpt",
            "pop": e28.POP, "elite_frac": e28.ELITE, "seed": 27,
            "search_seeds": list(e28.SEARCH_SEEDS),
        },
        "disc28": {
            "policy": disc28_pol,
            "search_hold": disc28_search_hold,
            "heldout_hold": agg_28["hold_mean"],
            "heldout_by_seed": agg_28["hold_by_seed"],
            "median": agg_28.get("median"),
        },
        "continued_best": {
            "policy": new_pol,
            "search_fitness": float(best_f),
            "search_hold": float(-best_f),
            "heldout_hold": agg_new["hold_mean"],
            "heldout_by_seed": agg_new["hold_by_seed"],
            "median": agg_new.get("median"),
        },
        "heldout_delta": float(delta),
        "criteria": {"X1_continuation_pays": bool(x1),
                     "X2_search_improvement": bool(x2),
                     "X3_schedule_divergence": bool(x3)},
        "schedule_shifts": shifts,
        "notes": ("Exact checkpoint resume (mu/sigma/best/rng state). "
                  "Held-out world identical to exp28/exp25 for "
                  "comparability. Search-side improvement without "
                  "held-out improvement = search-seed overfit, recorded."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}", flush=True)
    return out


if __name__ == "__main__":
    main()
