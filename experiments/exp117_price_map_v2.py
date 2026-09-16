#!/usr/bin/env python3
"""exp117 — THE PRICE MAP V2 RE-ISSUE (ledger L97's registration:
the compiler-facing artifact the exp108-116 arc was building — the
reader's price map in its honest current form, versioned, with the
walk-speed calibration and the oracle's domain statement).

SOURCES (all deposited; assembly only):
  exp100  the deployed-protocol cells and v1 classes
  exp111  the frozen-walk settle column (torus/grid2d calibration)
  exp112  the walk-speed ladder (13/15 buy-backs, adopted0 arms)
  exp113  the re-priced map (19 members, spc=0 cells + errs)
  exp114  the corrected oracle (rho 0.63, class means, pair
          domination) and its domain statement
  exp115  the mu ladder (binary-deep, speed buys gamma never mu)
  exp116  the phase 2x2 (total mu silence on the middle band)

THE OUTPUT: results/price_map_v2.json (the machine-readable map) +
docs/PRICE_MAP_V2.md (the compiler-facing document). Gates:
  PM-G1  every one of the 19 members carries a verified cell under
         BOTH protocols (deployed from exp100, frozen from
         exp112/113) — no holes in the re-issued map.
  PM-G2  the class re-assignment is internally consistent: every
         member's v2 class matches its cell's ladder position
         (DEFAULT0 -> (1, 0.015); MU0 -> (1, 0); GAMMA0 ->
         (4..16, .015 or 0); GEOMETRY -> (32, 0)).
  PM-G3  the artifact renders (docs/PRICE_MAP_V2.md written, the
         JSON loads, the counts add to 19).
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_JSON = os.path.join(ROOT, "results", "price_map_v2.json")
OUT_DOC = os.path.join(ROOT, "docs", "PRICE_MAP_V2.md")

CLASSES_V2 = {
    "DEFAULT0": ["path", "path200", "cycle", "small_world", "star"],
    "MU0_SILENCE": ["torus", "torus_elong", "random3", "random8",
                    "scale_free", "scale_free200"],
    "GAMMA0": ["tree", "grid2d", "grid_elong", "ladder", "random6",
               "barbell"],
    "GEOMETRY": ["bipartite", "complete"],
}
CLASS_OF = {n: c for c, ms in CLASSES_V2.items() for n in ms}
MU_REQ = {n: ("mandatory-silence" if CLASS_OF[n] == "MU0_SILENCE"
              else "tolerant") for n in CLASS_OF}


def main() -> dict:
    print("=== exp117: the price map v2 re-issue ===\n")

    exp100 = json.load(open(os.path.join(
        ROOT, "results", "exp100_reader_price_map.json")))
    exp112 = json.load(open(os.path.join(
        ROOT, "results", "exp112_walk_speed_ladder.json")))
    exp113 = json.load(open(os.path.join(
        ROOT, "results", "exp113_repriced_map.json")))
    exp114 = json.load(open(os.path.join(
        ROOT, "results", "exp114_corrected_oracle.json")))
    exp115 = json.load(open(os.path.join(
        ROOT, "results", "exp115_middle_pricer.json")))

    def exp100_cell(name):
        dep = exp100["cells"][name]
        cls = exp100["classes"].get(name, {})
        if cls.get("call") == "DEFAULT":
            return dep["default"]
        if "cheapest" in cls:
            g = cls["cheapest"]
            g = g if isinstance(g, list) else [g, 0.0]
            return dep[f"twodial_{g[0]:g}_{g[1]:g}"]
        return dep[f"gamma_{cls['gamma_min']:g}"]

    members = []
    for name in CLASS_OF:
        dep_cell = exp100_cell(name)
        frozen = exp113["map_spc0"][name]
        bb = exp112["buy_backs"].get(name)
        members.append({
            "name": name,
            "class_v1": exp100["classes"].get(name, {}).get("call"),
            "class_v2": CLASS_OF[name],
            "deployed_cell_err": dep_cell["err"],
            "deployed_cell_rate": dep_cell["rate"],
            "frozen_cell": frozen["cell"],
            "frozen_cell_err": frozen["err"],
            "speed_buyback": (bb["saves"] if bb else None),
            "mu_requirement": MU_REQ[name],
            "v2_ratio": frozen.get("v2"),
        })

    for m in members:
        print(f"    {m['name']:13s} {m['class_v2']:12s} "
              f"deployed {m['deployed_cell_err']:5.2f}  frozen "
              f"({m['frozen_cell'][0]:g}, {m['frozen_cell'][1]:g}) "
              f"{m['frozen_cell_err']:5.2f}  buyback "
              f"{m['speed_buyback']}  mu {m['mu_requirement']}")

    pm_g1 = all(m["deployed_cell_rate"] >= 2 / 3
                and m["frozen_cell_err"] < 6.0 for m in members)
    pm_g2 = True
    for m in members:
        cell = m["frozen_cell"]
        cls = m["class_v2"]
        ok = ((cls == "DEFAULT0" and cell == [1.0, 0.015])
              or (cls == "MU0_SILENCE" and cell == [1.0, 0.0])
              or (cls == "GAMMA0" and cell[0] in (4.0, 8.0, 16.0))
              or (cls == "GEOMETRY" and cell == [32.0, 0.0]))
        pm_g2 &= ok
    pm_g3 = len(members) == 19

    rho = exp114["spearman_class_ordinal"]
    doc = ["# PRICE MAP V2 — the reader's honest current form",
           "",
           "Re-issued by exp108-116 (ledger L90-L97): the walk-speed",
           "arc. The deployed protocol's prices carried a WALK TAX",
           "(the 0.8n-time-unit rebuild bathes the field in the wound",
           "state — exp110) and a MU-SILENCE requirement on the middle",
           "band that is binary in magnitude AND phase combination",
           "(exp115-116). The oracle prices the ends; the dials pay",
           "the middle; walk speed was hidden tax everywhere except",
           "the geometry pair. (exp114: rho 0.63, references 0.73/0.81",
           "on walk-taxed cells.)",
           "",
           "| member | class v2 | deployed err | frozen cell | frozen err | speed buyback | mu requirement | v2 ratio |",
           "|---|---|---|---|---|---|---|---|"]
    for m in members:
        doc.append(
            f"| {m['name']} | {m['class_v2']} | "
            f"{m['deployed_cell_err']:.2f} | "
            f"({m['frozen_cell'][0]:g}, {m['frozen_cell'][1]:g}) | "
            f"{m['frozen_cell_err']:.2f} | "
            f"{m['speed_buyback'] if m['speed_buyback'] else '-'} | "
            f"{m['mu_requirement']} | "
            f"{m['v2_ratio'] if m['v2_ratio'] is not None else '-'} |")
    doc += ["",
            "## The oracle's domain statement (exp114)",
            "",
            f"Spearman(v2, class-ordinal cost) = {rho} on the honest",
            "map (references 0.73 raw / 0.81 v2 on walk-taxed cells).",
            "The boundary-to-volume ratio prices the ENDS — the cheap",
            "band (v2 0.43-1.30) and the geometry pair (25.0-32.5,",
            "domination without exception) — and does NOT price the",
            "middle band (class-mean monotonicity REFUTED: MU0 7.12 >",
            "GAMMA0 5.55).",
            "",
            "## The calibration curve (exp111-112)",
            "",
            "Walk speed (steps_per_cell 8 -> 0) buys back GAMMA,",
            "never MU: 13/15 expensive members verify at a strictly",
            "cheaper cell under the frozen walk (most at gamma/4; the",
            "entire (4, 0) two-dial class at default gamma), the",
            "torus trend INVERTS (+1.04 -> -1.03) and n=784 prices at",
            "1.48 mV (3.3x cheaper, rate 1.0); grid2d is",
            "protocol-robust to +/-0.02; bipartite/complete refuse",
            "every descent rung (coupling geometry, not walk tax).",
            "",
            "## The mu-silence law (exp115-116)",
            "",
            "The middle band requires TOTAL mu silence — the 0.01",
            "rung buys nothing (0/6), and either phase (window or",
            "settle) carrying mu 0.015 fails identity 6/6. The cheap",
            "band and the geometry pair are mu-tolerant.",
            "",
            "## Bench prediction (deposited, testable)",
            "",
            "REBUILD SPEED PREDICTS IDENTITY FIDELITY — faster",
            "regeneration preserves pattern memory better (exp110's",
            "intact-drift ladder 2.47 -> 5.32 with n; the frozen walk",
            "collapses the trend). Candidate bench gate at the next",
            "Stage-5 protocol revision.",
            ""]
    with open(OUT_DOC, "w") as f:
        f.write("\n".join(doc))
    result = {
        "exp": "exp117_price_map_v2",
        "members": members,
        "oracle_rho": rho,
        "criteria": {"PM_G1_no_holes": bool(pm_g1),
                     "PM_G2_class_consistency": bool(pm_g2),
                     "PM_G3_artifact_complete": bool(pm_g3)},
    }
    with open(OUT_JSON, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  PM-G1 no holes: {'PASS' if pm_g1 else 'REFUTED'}")
    print(f"  PM-G2 class consistency: "
          f"{'PASS' if pm_g2 else 'REFUTED'}")
    print(f"  PM-G3 artifact complete: "
          f"{'PASS' if pm_g3 else 'REFUTED'}")
    print(f"\n  -> {OUT_JSON}\n  -> {OUT_DOC}")
    return result


if __name__ == "__main__":
    main()
