"""EXP8-SWEEP — the Level-3 gate robustness landscape, sharded for the runners.

The exp8 result (verified maintenance beats consensus-only maintenance
under pattern-fidelity mortality) was established in ONE regime. This sweep
maps the gate across the physics landscape:

  jump_rate (regional corruption pressure): 0.003 / 0.005 / 0.008
  f_crit    (organ-failure fidelity floor): 0.55 / 0.62 / 0.70
  kappa     (channel noise growth):         0.020 / 0.030

= 18 landscape cells, PLUS 6 probe cells (degraded channel, cliff regime,
pattern-propagation boost, weaker inflammaging, coarser code, heavy
corruption) = 24 cells — one per GitHub runner shard.

Each shard runs the six exp8 arms (none / local / codec / regen / chan /
blind) x 3 seeds x K individuals and reports per-arm medians + the gate
gains. The aggregate job (experiments/aggregate_fidelity.py) builds the
landscape figure and the robustness verdict:

  in how many cells does the gate (codec/local >= 1.03) hold?

Usage (shard mode):
  python -m experiments.exp8_sweep --cell 7 --out results/sweep/cell_7.json
"""

from __future__ import annotations

import argparse
import sys

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import FidelityAgingCohort, FidelityCodec
from experiments.exp8_fidelity import (
    fidelity_target, age_preset, run_condition, REGIME, CLIFF_REGIME,
)
from experiments.viz import setup, dump_json

SEEDS = (5, 6, 7)
CONDS = ("none", "local", "codec", "regen", "chan", "blind")

# ------------------------------------------------------------ landscape grid
JUMP_RATES = (0.003, 0.005, 0.008)
F_CRITS = (0.55, 0.62, 0.70)
KAPPAS = (0.020, 0.030)


def build_cells() -> list[dict]:
    """24 landscape/probe cells, deterministically ordered."""
    cells = []
    for kappa in KAPPAS:
        for f_crit in F_CRITS:
            for jr in JUMP_RATES:
                cells.append({
                    "kind": "landscape",
                    "jump_rate": jr, "f_crit": f_crit, "kappa": kappa,
                    "regime": dict(REGIME, kappa_noise=kappa),
                })
    # ---- 6 probe cells (edge-of-map physics) ----
    cells.append({"kind": "probe_degraded_channel", "jump_rate": 0.005,
                  "f_crit": 0.62, "kappa": 0.020,
                  "regime": dict(REGIME), "channel_factor": 2.5})
    cells.append({"kind": "probe_cliff", "jump_rate": 0.005, "f_crit": 0.62,
                  "kappa": 0.048, "regime": dict(CLIFF_REGIME)})
    cells.append({"kind": "probe_fast_propagation", "jump_rate": 0.005,
                  "f_crit": 0.62, "kappa": 0.020,
                  "regime": dict(REGIME, mu_theta=0.06)})
    cells.append({"kind": "probe_weak_inflammaging", "jump_rate": 0.005,
                  "f_crit": 0.62, "kappa": 0.020,
                  "regime": dict(REGIME, h_sys=0.025, h_inflam=0.015)})
    cells.append({"kind": "probe_coarse_code", "jump_rate": 0.005,
                  "f_crit": 0.62, "kappa": 0.020,
                  "regime": dict(REGIME), "levels": 5})
    cells.append({"kind": "probe_heavy_corruption", "jump_rate": 0.012,
                  "f_crit": 0.62, "kappa": 0.020, "regime": dict(REGIME)})
    assert len(cells) == 24
    return cells


def run_cell(cell: dict, seeds=SEEDS, K: int = 250, years: float = 170.0) -> dict:
    med: dict[str, list[float]] = {}
    cohort_kw = {}
    # cohort-constructor axes (NOT AgingParams): jump_rate, f_crit, levels
    if "jump_rate" in cell:
        cohort_kw["jump_rate"] = cell["jump_rate"]
    if "f_crit" in cell:
        cohort_kw["f_crit"] = cell["f_crit"]
    if cell.get("levels", 7) != 7:
        cohort_kw["levels"] = cell["levels"]
    for seed in seeds:
        for cond in CONDS:
            r = run_condition(
                cond, seed=seed, K=K, years=years,
                channel_factor=cell.get("channel_factor", 1.0),
                regime=cell["regime"],
                cohort_kw=cohort_kw or None)
            med.setdefault(cond, []).append(r["median"])
    m = {c: float(np.mean(v)) for c, v in med.items()}
    out = {
        "kind": cell["kind"],
        "jump_rate": cell["jump_rate"], "f_crit": cell["f_crit"],
        "kappa": cell["kappa"], "channel_factor": cell.get("channel_factor", 1.0),
        "regime": {k: v for k, v in cell["regime"].items()},
        "levels": cell.get("levels", 7),
        "seeds": list(seeds), "K": K, "years": years,
        "medians": m,
        "medians_by_seed": {c: v for c, v in med.items()},
        "gains": {
            "codec_vs_none": m["codec"] / m["none"],
            "local_vs_none": m["local"] / m["none"],
            "codec_vs_local": m["codec"] / m["local"],
            "regen_vs_none": m["regen"] / m["none"],
            "chan_vs_codec": m["chan"] / m["codec"],
            "chan_vs_blind": m["chan"] / m["blind"],
        },
        "gate_holds": bool(m["codec"] / m["local"] >= 1.03),
    }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cell", type=int, required=True, help="cell index 0-23")
    ap.add_argument("--out", type=str, required=True)
    ap.add_argument("--K", type=int, default=250)
    ap.add_argument("--years", type=float, default=170.0)
    args = ap.parse_args()

    setup()
    cells = build_cells()
    cell = cells[args.cell]
    print(f"[exp8-sweep] cell {args.cell}/24: {cell['kind']} "
          f"(jump={cell['jump_rate']}, f_crit={cell['f_crit']}, "
          f"kappa={cell['kappa']})")
    out = run_cell(cell, K=args.K, years=args.years)
    for c in CONDS:
        print(f"  {c:6s}: median {out['medians'][c]:6.1f}")
    g = out["gains"]
    print(f"  codec/local x{g['codec_vs_local']:.3f}  "
          f"codec/none x{g['codec_vs_none']:.3f}  "
          f"regen/none x{g['regen_vs_none']:.3f}  "
          f"chan/blind x{g['chan_vs_blind']:.3f}  "
          f"gate: {'HOLDS' if out['gate_holds'] else 'FAILS'}")

    import json, os
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2, default=float)
    print(f"[exp8-sweep] -> {args.out}")


if __name__ == "__main__":
    main()
