#!/usr/bin/env python3
"""exp70 — ONSET-AWARE CORPUS RE-PASS (night nine continuous batch;
ledger L51).

The completion of the exp66 -> exp69 arc: the gj_block class's drug
schedules (StartTime/EndTime) classify its experiments into SUSTAINED
(start=0, end=0), DELAYED (start>0, end=0), and WASHOUT (start=0,
end>0) semantics; the washout/delayed arms use the adopted M40 rate
law (D=2.0, exp69); the sustained arms carry D=2 as well (their rates
are unchanged — M40-G2's delta 0.00 — for consistency with the
adopted model).

PRE-REGISTERED GATES:

  ON-G1  ONSET COVERAGE: every gj_block experiment with a drug
         schedule is classified (sustained/delayed/washout/mixed);
         the classification counts are reported.
  ON-G2  THE WASHOUT ARM MATCHES THE RECORD: e329's semantics at the
         adopted D rates <= 0.34 (recorded 0.00).
  ON-G3  THE DELAYED ARM RUNS COOLER THAN SUSTAINED: the delayed
         tail arm's rate <= the sustained tail arm's rate (pub20's
         direction: e328 0.19 < the sustained class's ~0.6-1.0).
  ON-G4  CORPUS MAE IMPROVES FURTHER: the onset-aware sweep's
         outcome-weighted MAE < exp67's 0.524.

RUN: DB classification + deduped arms x3 seeds. Serial, BLAS pinned.
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

import sqlite3  # noqa: E402

from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)
from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, SEEDS, TAIL, ABN_ERR_MV, ABN_HL, make_collective,
)
from experiments.exp32_m26_repairs import (  # noqa: E402
    HEAD, TAILP, TRUNK, POST_Q, ANT_Q, WT_HEAD_V, WT_TAIL_V,
)
from experiments.planform_mining import DB, load_widened  # noqa: E402
from experiments.exp60_gene_layer import experiment_family  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp70_onset_corpus.json")

WT = wildtype_target(N)
D_ADOPTED = 2.0
GJ_DRUGS = {"Hexanol", "Heptanol", "Octanol"}


def regen_region(plane: str) -> slice:
    return HEAD if plane == "head" else TAILP if plane == "tail" else TRUNK


def classify_onset(drugs: list[dict]) -> str:
    """sustained / delayed / washout / mixed from the schedule."""
    gj = [d for d in drugs if d["drug"] in GJ_DRUGS]
    if not gj:
        return "none"
    kinds = set()
    for d in gj:
        st, et = d.get("start_h"), d.get("end_h")
        if (st is None or st == 0) and (et is None or et == 0):
            kinds.add("sustained")
        elif (st is not None and st > 0) and (et is None or et == 0):
            kinds.add("delayed")
        elif (st is None or st == 0) and (et is not None and et > 0):
            kinds.add("washout")
        else:
            kinds.add("other")
    if len(kinds) == 1:
        return kinds.pop()
    return "mixed"


def run_gj_onset(seed: int, plane: str, cut_f: float,
                 onset: str) -> bool:
    """Blockade arms with the M40 rate law; delayed/washout switch r
    mid-walk (the inline rate-law walk mirrors regrow verbatim)."""
    c = make_collective(seed)
    c.block_gap_junctions(0.05)
    c.run(24, dt=DT)
    kw = dict(cell_period=0.8, dt=DT, noise=0.6,
              phi_readout=0.75, neural_readout=1.0, arz_readout=1.0,
              commitment_delay=D_ADOPTED)
    regions = []
    if plane == "head":
        c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
        regions = [(HEAD, "backward")]
    elif plane == "tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        regions = [(TAILP, "forward")]
    elif plane == "trunk":
        c.amputate(TRUNK, wound_voltage=-30.0, blastema_theta=-40.0)
        regions = [(TRUNK, "both")]
    elif plane == "head_tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
        regions = [(TAILP, "forward"), (HEAD, "backward")]
    elif plane == "crosspiece":
        ci = min(max(int(round(cut_f * N)), 5), N - 1)
        c.amputate(slice(ci, N), wound_voltage=-30.0,
                   blastema_theta=-40.0)
        regions = [(slice(ci, N), "forward")]
    if onset == "sustained":
        for reg, direction in regions:
            c.regrow(reg, direction=direction, **kw) \
                if direction != "forward" else c.regrow(reg, **kw)
    else:
        # inline rate-law walk with the mid-walk r switch
        t_switch = 2.0
        for reg, direction in regions:
            idx = list(np.arange(N)[reg])
            if direction == "backward":
                src = idx[-1] + 1 if idx[-1] + 1 < N else idx[-1]
                order = list(reversed(idx))
            else:
                src = idx[0] - 1 if idx[0] - 1 >= 0 else idx[0]
                order = idx
            wound_center = float(np.mean(c.theta[idx]))
            r = 1.0 if onset == "delayed" else 0.05
            t = 0.0
            for i in order:
                dur = 0.8 * (1.0 + D_ADOPTED * (1.0 - r))
                steps = max(1, int(round(dur / DT)))
                for _ in range(steps):
                    c.step(dt=DT)
                    t += DT
                    if onset == "delayed" and t >= t_switch and r != 0.05:
                        r = 0.05
                    if onset == "washout" and t >= t_switch and r != 1.0:
                        r = 1.0
                chain_base = c.theta[src]
                theta_new = chain_base + c.rng.normal(0.0, 0.6)
                if r < 1.0:
                    guess = wound_center + c.rng.normal(
                        0.0, c.blastema_readout_noise)
                    theta_new = r * theta_new + (1.0 - r) * guess
                c.theta[i] = theta_new
                c.V[i] = theta_new
                src = i
    c.run(15, dt=DT)
    reg = regen_region(plane)
    rerr = float(np.mean(np.abs(c.V[reg] - WT[reg])))
    return bool(rerr >= ABN_ERR_MV or head_likeness(c.V, TAIL) >= ABN_HL)


def run_arm(protocol: str, plane: str, cut_f: float, seed: int) -> bool:
    if protocol in ("gjblock", "gjblock_delayed", "gjblock_washout"):
        onset = {"gjblock": "sustained",
                 "gjblock_delayed": "delayed",
                 "gjblock_washout": "washout"}[protocol]
        return run_gj_onset(seed, plane, cut_f, onset)
    c = make_collective(seed)
    kw = dict(cell_period=0.8, dt=DT, noise=0.6)
    if protocol == "ion_channel":
        c.gamma *= 0.5
        c.noise_std *= 3.0
        kw.update(commitment_noise_scale=3.0, commitment_diffusion=1.5)
    elif protocol == "wnt":
        c.corrupt_region(POST_Q, theta_value=WT_HEAD_V)
    elif protocol == "apc":
        c.corrupt_region(ANT_Q, theta_value=WT_TAIL_V)
    elif protocol == "generic":
        c.gamma *= 0.7
        kw.update(commitment_diffusion=1.5)
    elif protocol == "neoblast":
        kw.update(neoblast_coin_p=0.8, commitment_diffusion=1.5)
    if plane == "head":
        c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(HEAD, direction="backward", **kw)
    elif plane == "tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, **kw)
    elif plane == "trunk":
        c.amputate(TRUNK, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TRUNK, direction="both", **kw)
    elif plane == "head_tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, **kw)
        c.regrow(HEAD, direction="backward", **kw)
    elif plane == "crosspiece":
        ci = min(max(int(round(cut_f * N)), 5), N - 1)
        c.amputate(slice(ci, N), wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(slice(ci, N), phi_readout=0.75, **kw)
    reg = regen_region(plane)
    rerr = float(np.mean(np.abs(c.V[reg] - WT[reg])))
    if protocol == "neoblast":
        return bool(rerr >= ABN_ERR_MV
                    or head_likeness(c.V, TAIL) >= ABN_HL)
    return bool(c.pattern_error(WT) >= ABN_ERR_MV
                or head_likeness(c.V, TAIL) >= ABN_HL)


def main() -> dict:
    print("=== exp70: onset-aware corpus re-pass ===\n")

    con = sqlite3.connect(DB)
    drugname = {i: n for i, n in con.execute("SELECT Id, Name FROM Drug")}
    expdrugs: dict[int, list] = {}
    for e, d, st, et in con.execute(
            "SELECT Experiment, Drug, StartTime, EndTime FROM ExperimentDrug"):
        expdrugs.setdefault(e, []).append(
            {"drug": drugname.get(d, d), "start_h": st, "end_h": et})
    exps = load_widened(con)
    con.close()

    onset_of = {eid: classify_onset(v) for eid, v in expdrugs.items()}
    counts: dict[str, int] = {}
    for eid, e in exps.items():
        if e["group"] == "gj_block":
            counts[onset_of.get(eid, "none")] = \
                counts.get(onset_of.get(eid, "none"), 0) + 1
    print(f"  gj_block onset classification: {counts}")
    on_g1 = bool(counts.get("sustained", 0) + counts.get("delayed", 0)
                 + counts.get("washout", 0) + counts.get("mixed", 0)
                 + counts.get("other", 0) >= 20)
    print(f"  ON-G1 onset coverage: "
          f"{'PASS' if on_g1 else 'REFUTED'}")

    # ---- the sweep -----------------------------------------------------------
    rows = []
    arm_keys = set()
    for eid, e in exps.items():
        group, plane = e["group"], e["plane"]
        cf = 0.5
        if plane == "crosspiece":
            f = e.get("cut_f")
            cf = min(max(round(float(f), 2), 0.05), 0.95) if f else 0.5
        if plane not in ("head", "tail", "trunk", "head_tail",
                         "crosspiece"):
            arm = None
        elif group == "cutting":
            arm = ("cutting", plane, cf)
        elif group in ("innexin", "gj_block"):
            if eid == 421:
                arm = ("gjblock", "head", 0.5)
            else:
                onset = onset_of.get(eid, "sustained") \
                    if group == "gj_block" else "sustained"
                proto = {"sustained": "gjblock",
                         "delayed": "gjblock_delayed",
                         "washout": "gjblock_washout"}.get(
                             onset, "gjblock")
                arm = (proto, plane, cf)
        elif group == "ion_channel":
            arm = ("ion_channel", plane, cf)
        elif group == "morphogen":
            if not e.get("ap_morphogen"):
                arm = None
            else:
                rnais = " | ".join(e.get("rnais", []))
                import re
                arm = (("apc", plane, cf)
                       if re.search(r"apc|axin", rnais, re.I)
                       else ("wnt", plane, cf))
        elif group == "other_rnai":
            fam = experiment_family(e.get("rnais", []))
            arm = {"neoblast": ("neoblast", plane, cf),
                   "wnt_pos": ("wnt", plane, cf),
                   "wnt_ant": ("apc", plane, cf),
                   "neural": ("generic", plane, cf),
                   "generic": ("generic", plane, cf),
                   "control": ("cutting", plane, cf)}.get(fam)
        else:
            arm = None
        rec = {"eid": eid, "group": group, "plane": plane,
               "n": e.get("n", 1), "recorded": e["abnormal"],
               "arm": list(arm) if arm else None}
        if arm:
            arm_keys.add(arm)
        rows.append(rec)

    print(f"  running {len(arm_keys)} deduped arms x {len(SEEDS)} seeds...")
    arms = {}
    for key in sorted(arm_keys):
        protocol, plane, cf = key
        runs = [run_arm(protocol, plane, cf, s) for s in SEEDS]
        arms[str(key)] = float(np.mean(runs))
    for r in rows:
        r["sim_rate"] = arms[str(tuple(r["arm"]))] if r["arm"] else None

    # ---- gates ------------------------------------------------------------------
    e329 = next(r for r in rows if r["eid"] == 329)
    on_g2 = bool(e329["sim_rate"] <= 0.34)
    print(f"\n  ON-G2 washout e329: sim {e329['sim_rate']:.2f} vs "
          f"recorded {e329['recorded']:.2f} "
          f"-> {'PASS' if on_g2 else 'REFUTED'}")

    del_tail = [r for r in rows if r["arm"] and r["arm"][0] ==
                "gjblock_delayed" and r["plane"] == "tail"]
    sus_tail = [r for r in rows if r["arm"] and r["arm"][0] ==
                "gjblock" and r["plane"] == "tail"]
    if del_tail and sus_tail:
        d_rate = float(np.mean([r["sim_rate"] for r in del_tail]))
        s_rate = float(np.mean([r["sim_rate"] for r in sus_tail]))
        on_g3 = bool(d_rate <= s_rate)
        print(f"  ON-G3 delayed tail {d_rate:.2f} <= sustained tail "
              f"{s_rate:.2f} -> {'PASS' if on_g3 else 'REFUTED'}")
    else:
        on_g3 = False
        print(f"  ON-G3 delayed tail experiments: {len(del_tail)} "
              f"-> REFUTED (no coverage)")

    w = np.array([r["n"] for r in rows if r["sim_rate"] is not None])
    d = np.array([abs(r["sim_rate"] - r["recorded"]) for r in rows
                  if r["sim_rate"] is not None])
    mae = float(np.average(d, weights=w))
    on_g4 = bool(mae < 0.524)
    print(f"  ON-G4 MAE {mae:.3f} < exp67's 0.524: "
          f"{'PASS' if on_g4 else 'REFUTED'}")

    out = {
        "exp": "exp70_onset_corpus",
        "onset_counts": counts,
        "mae": round(mae, 4),
        "e329_arm": e329["sim_rate"],
        "criteria": {
            "ON_G1_onset_coverage": bool(on_g1),
            "ON_G2_washout_matches": bool(on_g2),
            "ON_G3_delayed_cooler": bool(on_g3),
            "ON_G4_mae_improves": bool(on_g4),
        },
        "notes": (
            "The onset-aware mapping completes the exp66->exp69 arc: "
            "the gj_block class's drug schedules classify into "
            "sustained/delayed/washout; the washout and delayed arms "
            "use the adopted M40 rate law (D=2). The corpus MAE is "
            "the running integration metric for the adopted stack."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/4 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
