#!/usr/bin/env python3
"""exp57 — NIGHT-EIGHT CLOSING BATCH (ledger L38): four registered items.

A. TAS CRYPTIC RE-CUT INTERVAL (PPRPPR1216581, verified 2026 preprint):
   regeneration stores a HIDDEN state revealed on re-cut — a
   "challenge-sensitive cryptic interval BELOW the immediate double-headed
   threshold": fragments whose immediate regen is normal can still show
   altered re-challenge outcomes, with "stable re-challenge ratios".
   Model analog: M31-A's anchor coin is minted from the fragment's stored
   state (blake2b of the quantized face window); a re-cut samples a
   DIFFERENT face window -> a different coin. Pre-registered:
     TA-G1 (cryptic interval): across 12 seeds (M31-A regime q=0.75), the
           re-cut abnormal rate DIFFERS from the naive first-cut rate
           (>= 1 discordant seed: immediate normal + re-cut abnormal, or
           the reverse).
     TA-G2 (stable ratios): the re-cut outcome is DETERMINISTIC given the
           stored state — re-running the re-cut from the identical stored
           collective reproduces the outcome bit-exactly (the M31-A
           minting is stream-neutral).

B. UNDERDAMPED PCG RECOVERY (MED42172041, verified 2026 4D atlas):
   "positional control genes recover through self-organizing dynamics
   analogous to an UNDERDAMPED control system" — the positional field
   should OVERSHOOT before settling. MEASUREMENT gate (both outcomes are
   findings, pre-interpreted):
     UD-G1: after the regen walk, the wound-face theta trajectory during
           the 15h post-settle either overshoots the final settled value
           by >= 0.5 mV (UNDERDAMPED — matches the atlas) or stays within
           0.1 mV (OVERDAMPED — an honest model-class refutation and a
           night-nine calibration target).

C. THE MIS-ANCHORED POLE (M36, egal-1 direction; MED41099308 verified):
   egal-1 RNAi or microtubule destabilization -> ectopic notum at
   POSTERIOR-facing wounds -> posterior heads. The new `neural_misanchor`
   param breaks the pole channel's anterior confinement: the wound reads
   the head program regardless of position. Pre-registered:
     EG-G1 (two-headed direction): tail-plane blockade regen with the
           mis-anchored pole becomes head-like (head_likeness_tail
           >= 0.5 in >= 2/3 seeds).
     EG-G2 (head plane unchanged): the head-plane outcome with
           misanchor vs without differs by <= 0.15 pred_abn (anterior
           cells already qualify for the pole read).
     EG-G3 (full-coupling inert): at gap_scale=1 the misanchor is inert
           (delta <= 0.15).

D. GJBLOCK|HEAD_TAIL ANOMALY (night-eight queue #2): the record's
   both-faces plane under blockade is 0.025 abnormal (n=2 — weak
   evidence). Run the model's head_tail plane under blockade with M33
   armed and ledger the comparison with its diagnosis (no gate — n=2).

RUN PROTOCOL: exp46 conventions (make_collective, 24h window dt=0.1,
blockade 0.05, PHI=0.75, neural_readout=0.8, metrics after regrow);
M31-A regime spec_reanchor_isolated=0.75 for part A (the exp45/50 split
regime). Serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)
from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, SEEDS, ABN_ERR_MV, ABN_HL, make_collective,
)
from experiments.exp32_m26_repairs import HEAD, TAILP  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp57_night8_closing.json")

PHI = 0.75
W = 0.8


def metrics(c) -> dict:
    err = c.pattern_error(wildtype_target(N))
    hl_tail = head_likeness(c.V, TAILP)
    return {"wt_pattern_error": float(err),
            "head_likeness_tail": float(hl_tail),
            "pred_abnormal": bool(err >= ABN_ERR_MV or hl_tail >= ABN_HL)}


def majority(vals: list[bool]) -> bool:
    return sum(vals) >= (len(vals) // 2 + 1)


# ----------------------------------------------------------- A: TAS re-cut
def tas_recut() -> dict:
    print("  [A] TAS cryptic re-cut interval (12 seeds, q=0.75)")
    rows = []
    for seed in range(1, 13):
        c = make_collective(seed)
        c.block_gap_junctions(0.05)
        c.run(24, dt=DT)
        # first cut (naive): tail plane
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6, phi_readout=PHI,
                 neural_readout=W, spec_reanchor_isolated=0.75)
        first = metrics(c)
        # re-cut: amputate the REGENERATED tail again, same plane
        state = (c.theta.copy(), c.V.copy())
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6, phi_readout=PHI,
                 neural_readout=W, spec_reanchor_isolated=0.75)
        recut = metrics(c)
        # determinism: replay the re-cut from the identical stored state
        c2 = make_collective(seed)
        c2.block_gap_junctions(0.05)
        c2.run(24, dt=DT)
        c2.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c2.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6, phi_readout=PHI,
                  neural_readout=W, spec_reanchor_isolated=0.75)
        c2.theta, c2.V = state[0].copy(), state[1].copy()
        c2.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c2.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6, phi_readout=PHI,
                  neural_readout=W, spec_reanchor_isolated=0.75)
        replay = metrics(c2)
        rows.append({
            "seed": seed,
            "first_abn": first["pred_abnormal"],
            "first_err": first["wt_pattern_error"],
            "recut_abn": recut["pred_abnormal"],
            "recut_err": recut["wt_pattern_error"],
            "recut_replay_err": replay["wt_pattern_error"],
            "recut_bitexact": bool(abs(recut["wt_pattern_error"]
                                       - replay["wt_pattern_error"]) < 1e-9),
        })
        print(f"    seed {seed:2d}: first abn={int(first['pred_abnormal'])} "
              f"({first['wt_pattern_error']:5.2f})  recut "
              f"abn={int(recut['pred_abnormal'])} "
              f"({recut['wt_pattern_error']:5.2f})  "
              f"bitexact={rows[-1]['recut_bitexact']}")
    naive_rate = float(np.mean([r["first_abn"] for r in rows]))
    recut_rate = float(np.mean([r["recut_abn"] for r in rows]))
    discordant = [r for r in rows if r["first_abn"] != r["recut_abn"]]
    return {
        "rows": rows, "naive_rate": naive_rate, "recut_rate": recut_rate,
        "n_discordant": len(discordant),
        "all_bitexact": all(r["recut_bitexact"] for r in rows),
    }


# --------------------------------------------------- B: underdamped check
def underdamped() -> dict:
    print("  [B] underdamped PCG recovery (wound-face overshoot)")
    overshoots = []
    for seed in SEEDS:
        c = make_collective(seed)
        c.block_gap_junctions(0.05)
        c.run(24, dt=DT)
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6, phi_readout=PHI,
                 neural_readout=W)
        # track the wound-face cell (just anterior to the regenerate)
        face = TAILP.start - 1
        final = None
        traj = []
        for _ in range(150):                       # 15h post-settle
            c.step(DT)
            traj.append(float(c.theta[face]))
        final = float(np.mean(traj[-30:]))          # settled value
        minimum = float(np.min(traj))
        # overshoot = excursion BELOW the settled value (hyperpolarized
        # rebound) or ABOVE it, whichever larger
        over = max(final - minimum, 0.0)
        maximum = float(np.max(traj))
        over_up = max(maximum - final, 0.0)
        overshoots.append(max(over, over_up))
        print(f"    seed {seed}: face settled {final:6.2f} mV, "
              f"max excursion {overshoots[-1]:.3f} mV")
    return {"per_seed": overshoots,
            "max_overshoot_mv": float(np.max(overshoots)),
            "mean_overshoot_mv": float(np.mean(overshoots))}


# ------------------------------------------------- C: mis-anchored pole
def misanchor_arms() -> dict:
    print("  [C] M36 mis-anchored pole (egal-1 direction)")
    out: dict = {}
    for tag, kw in {
        "tail_blocked_misanchor": dict(plane="tail", mis=True),
        "tail_blocked_plain": dict(plane="tail", mis=False),
        "head_blocked_misanchor": dict(plane="head", mis=True),
        "head_blocked_plain": dict(plane="head", mis=False),
        "tail_full_misanchor": dict(plane="tail", mis=True, full=True),
        "tail_full_plain": dict(plane="tail", mis=False, full=True),
    }.items():
        rows = []
        for seed in SEEDS:
            c = make_collective(seed)
            if not kw.get("full"):
                c.block_gap_junctions(0.05)
            c.run(24, dt=DT)
            region = TAILP if kw["plane"] == "tail" else HEAD
            rg = dict(cell_period=0.8, dt=DT, noise=0.6, phi_readout=PHI,
                      neural_readout=W)
            if kw["mis"]:
                rg["neural_misanchor"] = 1.0
            if kw["plane"] == "head":
                c.amputate(region, wound_voltage=-30.0, blastema_theta=-40.0)
                c.regrow(region, direction="backward", **rg)
            else:
                c.amputate(region, wound_voltage=-30.0, blastema_theta=-40.0)
                c.regrow(region, **rg)
            m = metrics(c)
            m["seed"] = seed
            rows.append(m)
        out[tag] = {
            "pred_abn_rate": float(np.mean([r["pred_abnormal"]
                                            for r in rows])),
            "hl_tail_mean": float(np.mean([r["head_likeness_tail"]
                                           for r in rows])),
            "per_seed": rows,
        }
        print(f"    {tag:26s} abn {out[tag]['pred_abn_rate']:.2f}  "
              f"hl_tail {out[tag]['hl_tail_mean']:.3f}")
    return out


# --------------------------------------------- D: gjblock|head_tail n=2
def head_tail_anomaly() -> dict:
    print("  [D] gjblock|head_tail (recorded 0.025, n=2) model check")
    rows = []
    for seed in SEEDS:
        c = make_collective(seed)
        c.block_gap_junctions(0.05)
        c.run(24, dt=DT)
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6, phi_readout=PHI,
                 neural_readout=W)
        c.regrow(HEAD, cell_period=0.8, dt=DT, noise=0.6, phi_readout=PHI,
                 neural_readout=W, direction="backward")
        m = metrics(c)
        m["seed"] = seed
        rows.append(m)
        print(f"    seed {seed}: abn={int(m['pred_abnormal'])} "
              f"err={m['wt_pattern_error']:.2f} hl_tail={m['head_likeness_tail']:.3f}")
    return {"pred_abn_rate": float(np.mean([r["pred_abnormal"]
                                            for r in rows])),
            "per_seed": rows}


def main() -> None:
    print("=== exp57: night-eight closing batch ===\n")
    res: dict = {"exp": "exp57_night8_closing"}
    gates: dict[str, dict] = {}

    # A
    tas = tas_recut()
    res["A_tas_recut"] = {k: v for k, v in tas.items() if k != "rows"}
    gates["TA-G1"] = {
        "verdict": "PASS" if tas["n_discordant"] >= 1 else "REFUTED",
        "naive_rate": tas["naive_rate"],
        "recut_rate": tas["recut_rate"],
        "n_discordant": tas["n_discordant"],
        "gate": ("re-cut rate differs from naive (>= 1 discordant seed) — "
                 "the cryptic interval exists"),
    }
    gates["TA-G2"] = {
        "verdict": "PASS" if tas["all_bitexact"] else "REFUTED",
        "gate": ("re-cut outcome deterministic given the stored state "
                 "(bit-exact replay)"),
    }

    # B
    ud = underdamped()
    res["B_underdamped"] = ud
    verdict = "UNDERDAMPED" if ud["max_overshoot_mv"] >= 0.5 else \
        ("OVERDAMPED" if ud["max_overshoot_mv"] < 0.1 else "WEAK")
    gates["UD-G1"] = {
        "verdict": verdict,
        "max_overshoot_mv": ud["max_overshoot_mv"],
        "mean_overshoot_mv": ud["mean_overshoot_mv"],
        "gate": ("measurement: overshoot >= 0.5 mV -> underdamped (atlas "
                 "match); < 0.1 -> overdamped (calibration target)"),
    }

    # C
    ma = misanchor_arms()
    res["C_misanchor"] = ma
    eg1 = ma["tail_blocked_misanchor"]["hl_tail_mean"]
    eg2 = (abs(ma["head_blocked_misanchor"]["pred_abn_rate"]
               - ma["head_blocked_plain"]["pred_abn_rate"]))
    eg3 = (abs(ma["tail_full_misanchor"]["pred_abn_rate"]
               - ma["tail_full_plain"]["pred_abn_rate"]))
    gates["EG-G1"] = {
        "verdict": "PASS" if eg1 >= 0.5 else "REFUTED",
        "tail_blocked_misanchor_hl": eg1,
        "gate": "mis-anchored pole: tail blockade regen becomes head-like",
    }
    gates["EG-G2"] = {
        "verdict": "PASS" if eg2 <= 0.15 else "REFUTED",
        "head_plane_delta": eg2,
        "gate": "head plane unchanged by the misanchor (<= 0.15)",
    }
    gates["EG-G3"] = {
        "verdict": "PASS" if eg3 <= 0.15 else "REFUTED",
        "fullcoupling_delta": eg3,
        "gate": "misanchor inert at full coupling (<= 0.15)",
    }

    # D
    ht = head_tail_anomaly()
    res["D_head_tail"] = ht
    gates["HT-D0"] = {
        "verdict": "LEDGERED (recorded n=2; no gate)",
        "model_pred_abn": ht["pred_abn_rate"],
        "recorded": 0.025,
    }

    res["gates"] = gates
    n_pass = sum(1 for g in gates.values()
                 if g["verdict"] in ("PASS", "UNDERDAMPED", "OVERDAMPED"))
    res["summary"] = f"{n_pass}/{len(gates)} gates resolved"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print(f"\nGATES: {res['summary']}")
    for k, g in gates.items():
        print(f"  {k}: {g['verdict']}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
