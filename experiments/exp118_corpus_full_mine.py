#!/usr/bin/env python3
"""exp118 — THE PLANFORMDB FULL-CORPUS MINE (Stage-2 corpus integration;
task 2-d): the ADOPTED corpus stack run over ALL 1,716 PlanformDB
experiments (not a slice), with per-experiment predicted-vs-published
outcomes, aggregate error stats, slice-vs-full comparison columns, and
the full-run wall-clock estimate.

NUMBERING NOTE: ledger d19ef02 (L98) queued "exp118 = the TAS-P1 memory
co-metric spectrum test"; no exp118_* FILE existed at write time
(verified) and task 2-d assigns exp118 to this script. TAS-P1 keeps its
queue slot and takes the next free number. Nothing else was renamed.

WHAT THIS IS: the corpus-mining integrator. Every prior corpus script
mined a SLICE with an EARLIER stack:
  exp21  DB-vs-signature benchmark (no sim), pre-exp27 machinery
  exp27  cutting+innexin class pilot (pre-repair collective)
  exp37  full-outcome sweep (1,462) on the exp31/34/36-era stack
  exp60  the gene layer (other_rnai families, exp83-era protocol)
  exp70  onset-aware gj re-pass (pre-C1-window arm; MAE 0.522, L51)
  exp88  the corpus RE-WIRING (C1-C4; raw 0.365 / decoded 0.304, L70)
  exp91  the dose-axis refutation + the amplitude axis (L73)
  exp92  the fine ladder + the ROW-LEVEL dose mapping (L74)
The ADOPTED corpus mapping as of L98 is exp92's FINAL pass: the exp88
C1-C4 arm wiring + the row-level dose classes (effector d=1.0 /
modulator D_PAR=0.25 for AP-morphogen rows; other_rnai wnt_pos/wnt_ant
RNAi KNOCKOUTS pinned to the full arm — L74's owned scoping repair).
Its ledger reference: raw MAE 0.371 / decoded MAE 0.290 (L74).

SCOPE NOTE (the stack, stated): the corpus arms run on the standard 1D
N=100 sheet (exp27 make_collective) — the exp108-117 compiler arc (the
walk-speed dial, the mu-silence law, docs/PRICE_MAP_V2.md) prices
SUBSTRATE dials for the compiler and does not touch the 1D-sheet corpus
arms. The full mine therefore runs the L74-adopted mapping verbatim and
carries the ledger references as comparison columns; nothing is
re-fitted and no new mechanism is introduced.

MODES (the pilot is what THIS run executed):
  default        PILOT — deterministic systematic ~10% STRIDE sample:
                 outcome-bearing rows sorted by eid ascending, every
                 PILOT_STRIDE-th row (stride 10 fixed pre-run) gets its
                 sim run (147 of 1,462 members; 90 of them arm-mapped
                 in the executed pilot). Chosen over the first-N rule
                 because eid order clusters by publication (a first-200
                 cut would miss late-eid arm classes); the stride covers
                 the whole eid range. NOT the full run.
  --full         the FULL 1,716 run (the main agent executes this).
Record-side frame statistics (per-plane control rates, the C4 exclusion
set, the corrected frames, the pinned blocks) are FULL-CORPUS pure-DB
quantities computed identically in BOTH modes — so a pilot row's
recorded/corrected values and its arm rate are bit-identical to what the
full run will produce for that row; only the sim side is sampled.

DATA: PlanformDB 2.5.0 (Lobo et al. 2013, Bioinformatics 29:608),
data/planform/planformDB_2.5.0.edb — 1,716 experiments (eids 120..1855,
17 species), 1,462 outcome-bearing (>=1 post-regeneration result set),
905 mapped by the adopted mapping, 47 unique sim arms.

ADOPTED CONSTANTS (pinned, never re-derived here):
  D_PAR     0.25    the L74 modulator dose (exp92's pre-registered
                    selection from the 7-seed fine ladder)
  GEN_BIAS  0.321   exp83's measured control hot bias (L64)
  ABN verdict       pattern_error >= 6.0 mV OR head_likeness >= 0.7
                    (exp1 calibration, untouched)
  seeds             (1, 2, 3); arm rates = mean over seeds, rounded 3dp
                    (the L70-L74 convention; the per-row "n" weight is
                    the vestigial default 1 everywhere in L70-L74, kept
                    for comparability)

PRE-REGISTERED GATES (fixed before the pilot ran):

  G1  EXTRACTION PARITY (readable in pilot; pure DB): the recomputed
      corpus quantities equal the ledger's pinned values — the L73
      partial block (morphogen wnt|trunk, recorded < 0.5): n=17,
      mean 0.189; the L74 modulator block: n=11, mean 0.105; the
      per-plane control-family rates (other_rnai->cutting rows):
      head 0.00 / trunk 0.38 / tail 0.49 (tol 0.01); the C4 exclusion
      count: 21 rows. A miss means the DB extraction path drifted and
      the full run must NOT be started before diagnosis.
  G2  ARM INTEGRITY (readable in pilot; bit-exact anchors): (a) the
      wnt|trunk dose-1.0 arm's 3-seed verdicts are bit-exact vs exp88's
      run_arm_v5 wnt|trunk (the DA-G3 stream-neutrality contract); (b)
      the same for cutting|trunk (the dose knob is protocol-scoped);
      (c) determinism: one arm from the table re-run at close
      reproduces its rate bit-exactly.
  G3  MAPPING SCOPE (readable in pilot; the L74 repairs respected):
      every wnt/apc arm dose is in {1.0, D_PAR}; every other_rnai
      wnt_pos/wnt_ant row is dosed 1.0 (the knockout scoping); eid 421
      pins to ("gjblock","head",0.5); every crosspiece cut fraction is
      clamped to [0.05, 0.95].
  G4  FULL ACCOUNTING (readable in pilot): every Experiment row appears
      exactly once; the status accounting sums to 1,716 exactly; every
      scored row carries recorded (raw+corrected), sim, both-frame
      errors, and the decode fields.
  G5  CORPUS PARITY (FULL-RUN gate; pilot deposits the indicative
      delta): decoded MAE within 0.01 of the L74 reference 0.290 AND
      raw within 0.01 of 0.371 — the reconstruction-drift alarm for the
      adopted mapping (the full run re-derives L74's numbers
      independently; exp91/exp92's own results JSONs are NOT in
      results/, so this re-deposit is the reference artifact).
  G6  DECODE BAR (FULL-RUN gate; pilot indicative): dominant-class
      decode accuracy (sim >= 0.5 vs recorded >= 0.5, scored rows)
      >= 0.60 — the exp27 S2P3 instrument upgraded to a corpus bar.
  G7  TIMING DEPOSIT (deposit gate; readable in pilot): per-arm timings
      + the full-run wall-clock estimate (from per-arm timings x the
      full arm count) deposited and finite.

RUN PROTOCOL: deduped arms x 3 seeds, serial, BLAS pinned (the L70-L74
discipline). No core edits; experiment-local machinery only.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sqlite3
import sys
import time
from collections import Counter, defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp60_gene_layer import experiment_family  # noqa: E402
from experiments.exp70_onset_corpus import classify_onset  # noqa: E402
from experiments.exp88_corpus_rewire import run_arm_v5  # noqa: E402
from experiments.exp91_dose_axis_wiring import run_arm_dose  # noqa: E402
from experiments.exp92_fine_ladder_rowmap import EFFECTOR_RE, row_class  # noqa: E402
from experiments.planform_mining import DB, load_widened  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PILOT = os.path.join(ROOT, "results", "exp118_corpus_full_pilot.json")
OUT_FULL = os.path.join(ROOT, "results", "exp118_corpus_full.json")

SEEDS = (1, 2, 3)
D_PAR = 0.25              # L74-adopted modulator dose (pinned)
GEN_BIAS = 0.321          # exp83's measured control hot bias (L64)
PILOT_STRIDE = 10         # deterministic systematic ~10% sample
SIM_MAPPABLE_PLANES = ("head", "tail", "trunk", "head_tail", "crosspiece")

# ---- pinned ledger quantities (G1 / G5) --------------------------------
PIN_L73_BLOCK = {"n": 17, "mean": 0.189}
PIN_L74_MODULATOR = {"n": 11, "mean": 0.105}
PIN_CTRL_RATES = {"head": 0.00, "trunk": 0.38, "tail": 0.49}
PIN_C4_ROWS = 21
PIN_L74_MAE = {"raw": 0.371, "decoded": 0.290}
LEDGER_REFERENCES = {          # the slice history, for the comparison block
    "L51_exp70_onset": {"mae": 0.522, "mapping": "exp70 (pre-C1 arm)"},
    "L70_exp88_rewire": {"mae_raw": 0.365, "mae_decoded": 0.304,
                         "mapping": "C1-C4"},
    "L73_exp91_dose_axis": {"mae_raw": 0.436, "mae_decoded": 0.290,
                            "mapping": "C1-C4 + family d*=0.0"},
    "L74_exp92_rowmap": {"mae_raw": 0.371, "mae_decoded": 0.290,
                         "mapping": "C1-C4 + row-level dose classes "
                                    "(ADOPTED)"},
}


# --------------------------------------------------------------- mapping
def map_arm(eid: int, e: dict, onset_of: dict) -> tuple | None:
    """The ADOPTED corpus mapping (exp92 final pass, L74; verbatim).

    Returns (protocol, plane, cut_f, dose) or None. dose is set only
    where the L74 mapping sets it (morphogen rows 1.0/D_PAR; other_rnai
    wnt_pos/wnt_ant knockouts pinned 1.0); None elsewhere.
    """
    group, plane = e["group"], e["plane"]
    if plane not in SIM_MAPPABLE_PLANES:
        return None
    cf = 0.5
    if plane == "crosspiece":
        f = e.get("cut_f")
        cf = min(max(round(float(f), 2), 0.05), 0.95) if f else 0.5
    if group == "cutting":
        return ("cutting", plane, cf, None)
    if group in ("innexin", "gj_block"):
        if eid == 421:                       # the adopted pin (L70)
            return ("gjblock", "head", 0.5, None)
        onset = (onset_of.get(eid, "sustained")
                 if group == "gj_block" else "sustained")
        proto = {"sustained": "gjblock", "delayed": "gjblock_delayed",
                 "washout": "gjblock_washout"}.get(onset, "gjblock")
        return (proto, plane, cf, None)
    if group == "ion_channel":
        return ("ion_channel", plane, cf, None)
    if group == "morphogen":
        if e.get("ap_morphogen"):
            rnais = e.get("rnais", [])
            proto = ("apc" if re.search(r"apc|axin", " | ".join(rnais),
                                        re.I) else "wnt")
            dose = 1.0 if row_class(rnais) == "effector" else D_PAR
            return (proto, plane, cf, dose)
        return None                          # non-AP morphogen: no 1D layer
    if group == "other_rnai":
        fam = experiment_family(e.get("rnais", []))
        m = {"neoblast": "neoblast", "wnt_pos": "wnt", "wnt_ant": "apc",
             "neural": "generic", "generic": "generic",
             "control": "cutting"}.get(fam)
        if m:
            # the L74 scoping repair: the partial dose applies to the
            # morphogen DRUG rows only; the RNAi KNOCKOUT rows stay at
            # the full arm
            dose = 1.0 if m in ("wnt", "apc") else None
            return (m, plane, cf, dose)
    return None


def build_rows() -> tuple[list[dict], dict]:
    """Every Experiment row -> record; record-side frames from the FULL
    corpus (pure DB, no sim). Returns (rows, corpus_stats)."""
    con = sqlite3.connect(DB)
    drugname = {i: n for i, n in con.execute("SELECT Id, Name FROM Drug")}
    expdrugs: dict[int, list] = {}
    for e, d, st, et in con.execute(
            "SELECT Experiment, Drug, StartTime, EndTime FROM ExperimentDrug"):
        expdrugs.setdefault(e, []).append(
            {"drug": drugname.get(d, d), "start_h": st, "end_h": et})
    species = {i: n for i, n in con.execute("SELECT Id, Name FROM Species")}
    species_of = dict(con.execute("SELECT Id, Species FROM Experiment"))
    manip_name = {i: nm for i, nm in
                  con.execute("SELECT Id, Name FROM Manipulation")}
    manip_of = dict(con.execute("SELECT Id, Manipulation FROM Experiment"))
    all_exp = [(eid, manip_name.get(manip_of.get(eid), ""))
               for (eid,) in con.execute("SELECT Id FROM Experiment")]
    exps = load_widened(con)
    con.close()
    onset_of = {eid: classify_onset(v) for eid, v in expdrugs.items()}

    rows: list[dict] = []
    for eid, manip in all_exp:
        base = {"eid": int(eid),
                "species": species.get(species_of.get(eid), "?"),
                "manipulation": (manip or "")[:60]}
        e = exps.get(eid)
        if e is None:                        # no post-regen result set
            rows.append({**base, "status": "no_outcome", "group": None,
                         "plane": None, "arm": None, "sim": None,
                         "recorded_raw": None, "recorded_corrected": None,
                         "excluded_C4": False, "slices": None,
                         "pilot_member": False,
                         "n_result_sets": 0, "rnais": [], "drugs": [],
                         "cut_f": None, "ap_morphogen": False})
            continue
        arm = map_arm(eid, e, onset_of)
        rec = {**base,
               "group": e["group"], "plane": e["plane"],
               "cut_f": e.get("cut_f"),
               "rnais": e.get("rnais", []),
               "drugs": e.get("drugs", []),
               "n_result_sets": e["n_rs"],
               "ap_morphogen": bool(e.get("ap_morphogen")),
               "recorded_raw": round(float(e["abnormal"]), 4),
               "arm": list(arm) if arm else None,
               "sim": None, "excluded_C4": False, "pilot_member": False,
               "slices": {
                   "exp27": e["group"] in ("cutting", "innexin"),
                   "exp60_gene": e["group"] == "other_rnai",
                   "exp70_onset": e["group"] in ("innexin", "gj_block"),
                   "exp88_mapped": arm is not None,
                   "exp92_dose_class": bool(e["group"] == "morphogen"
                                            and e.get("ap_morphogen")),
               }}
        if arm is None:
            rec["status"] = ("unmapped_plane"
                             if e["plane"] not in SIM_MAPPABLE_PLANES
                             else "unmapped_group")
        else:
            rec["status"] = "scored"
        rows.append(rec)

    # ---- record-side frames (full-corpus pure-DB quantities) -----------
    ctrl_by_plane: dict[str, list] = defaultdict(list)
    for r in rows:
        if r["group"] == "other_rnai" and r["arm"] \
                and r["arm"][0] == "cutting":
            ctrl_by_plane[r["plane"]].append(r["recorded_raw"])
    ctrl_rate = {p: float(np.mean(v)) for p, v in ctrl_by_plane.items()}

    n_c4 = 0
    for r in rows:
        if r["recorded_raw"] is None:        # no_outcome row
            continue
        r["excluded_C4"] = bool(
            r["group"] == "cutting" and r["arm"]
            and r["recorded_raw"] >= 0.9
            and ctrl_rate.get(r["plane"], 1.0) <= 0.35)
        n_c4 += int(r["excluded_C4"])
    for r in rows:
        if r["recorded_raw"] is None:        # no_outcome row
            continue
        rec_corr = r["recorded_raw"]
        if r["group"] == "other_rnai" and r["arm"] \
                and r["arm"][0] == "generic":
            rec_corr = max(0.0, rec_corr - GEN_BIAS)   # C3
        elif r["plane"] in ctrl_rate:                  # C3'
            rec_corr = max(0.0, rec_corr - ctrl_rate[r["plane"]])
        r["recorded_corrected"] = round(rec_corr, 4)

    # ---- the G1 pinned blocks ------------------------------------------
    l73 = [r for r in rows
           if r["group"] == "morphogen" and r["arm"]
           and r["arm"][0] == "wnt" and r["arm"][1] == "trunk"
           and r["recorded_raw"] < 0.5]
    l74 = [r for r in rows
           if r["group"] == "morphogen" and r["arm"]
           and r["arm"][0] == "wnt" and r["arm"][1] == "trunk"
           and row_class(r["rnais"]) == "modulator"
           and r["recorded_raw"] < 0.5]

    stats = {"n_db_total": len(rows),
             "ctrl_rate": ctrl_rate,
             "n_c4": n_c4,
             "l73_block": {"n": len(l73),
                           "mean": float(np.mean([r["recorded_raw"]
                                                  for r in l73]))},
             "l74_modulator": {"n": len(l74),
                               "mean": float(np.mean([r["recorded_raw"]
                                                      for r in l74]))}}
    return rows, stats


# ------------------------------------------------------------------- sim
def run_arms(rows: list[dict]) -> tuple[dict, dict]:
    """Deduped arm table x3 seeds with per-arm wall timing."""
    arm_keys = sorted({tuple(r["arm"]) for r in rows
                       if r["status"] == "scored"})
    arms: dict[str, float] = {}
    timings: dict[str, float] = {}
    for k in arm_keys:
        protocol, plane, cf, dose = k
        t0 = time.perf_counter()
        if protocol in ("wnt", "apc"):
            runs = [run_arm_dose(protocol, plane, cf, s,
                                 cns=1.0, diff=0.0, dose=dose)
                    for s in SEEDS]
        else:
            runs = [run_arm_v5(protocol, plane, cf, s) for s in SEEDS]
        timings[str(k)] = time.perf_counter() - t0
        arms[str(k)] = round(float(np.mean(runs)), 3)
    return arms, timings


def attach_sim(rows: list[dict], arms: dict) -> None:
    for r in rows:
        if r["status"] != "scored":
            continue
        r["sim"] = arms[str(tuple(r["arm"]))]
        r["abs_err_raw"] = round(abs(r["sim"] - r["recorded_raw"]), 4)
        r["abs_err_corrected"] = round(
            abs(r["sim"] - r["recorded_corrected"]), 4)
        r["pred_dominant"] = "abnormal" if r["sim"] >= 0.5 else "wt"
        r["recorded_dominant"] = ("abnormal" if r["recorded_raw"] >= 0.5
                                  else "wt")
        r["decode_match"] = bool(r["pred_dominant"] == r["recorded_dominant"])


def mae(rows: list[dict], key: str, use_excl: bool) -> tuple[float, int]:
    d = [abs(r["sim"] - r[key]) for r in rows
         if r["sim"] is not None and not (use_excl and r["excluded_C4"])]
    return (float(np.mean(d)) if d else float("nan")), len(d)


# ----------------------------------------------------------------- gates
def gate_g1(stats: dict) -> tuple[bool, dict]:
    checks = {
        "l73_block_n": stats["l73_block"]["n"] == PIN_L73_BLOCK["n"],
        "l73_block_mean":
            abs(stats["l73_block"]["mean"] - PIN_L73_BLOCK["mean"]) <= 0.01,
        "l74_modulator_n":
            stats["l74_modulator"]["n"] == PIN_L74_MODULATOR["n"],
        "l74_modulator_mean":
            abs(stats["l74_modulator"]["mean"]
                - PIN_L74_MODULATOR["mean"]) <= 0.01,
        "ctrl_rates": all(
            p in stats["ctrl_rate"]
            and abs(stats["ctrl_rate"][p] - v) <= 0.01
            for p, v in PIN_CTRL_RATES.items()),
        "c4_rows": stats["n_c4"] == PIN_C4_ROWS,
    }
    return bool(all(checks.values())), checks


def gate_g2(arms: dict, timings: dict) -> tuple[bool, dict]:
    ref_wnt = [run_arm_v5("wnt", "trunk", 0.5, s) for s in SEEDS]
    dose_wnt = [run_arm_dose("wnt", "trunk", 0.5, s,
                             cns=1.0, diff=0.0, dose=1.0) for s in SEEDS]
    ref_cut = [run_arm_v5("cutting", "trunk", 0.5, s) for s in SEEDS]
    dose_cut = [run_arm_dose("cutting", "trunk", 0.5, s,
                             cns=1.0, diff=0.0, dose=1.0) for s in SEEDS]
    det_ok = None
    for k in sorted(arms):
        protocol, plane, cf, dose = ast.literal_eval(k)
        if protocol in ("wnt", "apc"):
            rerun = round(float(np.mean(
                [run_arm_dose(protocol, plane, cf, s, cns=1.0, diff=0.0,
                              dose=dose) for s in SEEDS])), 3)
        else:
            rerun = round(float(np.mean(
                [run_arm_v5(protocol, plane, cf, s) for s in SEEDS])), 3)
        det_ok = bool(rerun == arms[k])
        break
    checks = {"wnt_bitexact": ref_wnt == dose_wnt,
              "cutting_bitexact": ref_cut == dose_cut,
              "determinism_rerun": det_ok}
    return bool(all(checks.values())), checks


def gate_g3(rows: list[dict]) -> tuple[bool, dict]:
    dose_ok = all(r["arm"][3] in (1.0, D_PAR) for r in rows
                  if r["arm"] and r["arm"][0] in ("wnt", "apc")
                  and r["group"] == "morphogen")
    knock_ok = all(r["arm"][3] == 1.0 for r in rows
                   if r["arm"] and r["arm"][0] in ("wnt", "apc")
                   and r["group"] == "other_rnai")
    pin_ok = any(r["eid"] == 421 and r["arm"] ==
                 ["gjblock", "head", 0.5, None] for r in rows)
    cf_ok = all(0.05 <= r["arm"][2] <= 0.95 for r in rows
                if r["arm"] and r["arm"][1] == "crosspiece")
    checks = {"morphogen_doses": dose_ok,
              "knockout_rows_full_dose": knock_ok,
              "eid421_pinned": pin_ok,
              "crosspiece_cf_clamped": cf_ok}
    return bool(all(checks.values())), checks


def gate_g4(rows: list[dict], n_db_total: int) -> tuple[bool, dict]:
    eids = [r["eid"] for r in rows]
    statuses = Counter(r["status"] for r in rows)
    scored = [r for r in rows if r["status"] == "scored"]
    complete = all(
        r["recorded_raw"] is not None and r["recorded_corrected"] is not None
        and r["sim"] is not None and "abs_err_raw" in r
        and "decode_match" in r for r in scored)
    checks = {"unique_eids": len(set(eids)) == len(eids) == n_db_total,
              "status_sum": sum(statuses.values()) == n_db_total,
              "scored_fields_complete": complete}
    return bool(all(checks.values())), {"checks": checks,
                                        "statuses": dict(statuses)}


# ------------------------------------------------------------------ main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true",
                    help="run ALL 1,716 experiments (the main agent's "
                         "full pass); default is the stride-10 pilot")
    args = ap.parse_args()
    mode = "full" if args.full else "pilot"
    out_path = OUT_FULL if args.full else OUT_PILOT

    t_start = time.perf_counter()
    print(f"=== exp118: PlanformDB full-corpus mine "
          f"(mode={mode}) ===\n")

    rows, stats = build_rows()
    n_db = stats["n_db_total"]

    # ---- mode membership --------------------------------------------------
    outcome_rows = [r for r in rows if r["status"] != "no_outcome"]
    if mode == "pilot":
        for idx, r in enumerate(
                sorted(outcome_rows, key=lambda r: r["eid"])):
            r["pilot_member"] = bool(idx % PILOT_STRIDE == 0)
        n_deferred = 0
        for r in rows:
            if r["status"] == "scored" and not r["pilot_member"]:
                r["status"] = "deferred_full_run"
                n_deferred += 1
        print(f"  pilot: stride {PILOT_STRIDE} over {len(outcome_rows)} "
              f"outcome rows -> {sum(1 for r in rows if r['status'] == 'scored')}"
              f" scored, {n_deferred} deferred to the full run")
    else:
        for r in rows:
            r["pilot_member"] = True

    n_arms_full = len({tuple(r["arm"]) for r in rows if r["arm"]})

    # ---- gates G1-G3 (G1/G3 need no sim) -----------------------------------
    g1, g1_checks = gate_g1(stats)
    print(f"  G1 extraction parity: "
          f"{stats['l73_block']} / {stats['l74_modulator']} / "
          f"ctrl { {k: round(v, 3) for k, v in stats['ctrl_rate'].items()} } "
          f"/ C4 {stats['n_c4']} -> {'PASS' if g1 else 'REFUTED'}")
    if not g1:
        print("  G1 REFUTED: the DB extraction path drifted from the "
              "ledger pins — diagnose BEFORE the full run.")
    g3, g3_checks = gate_g3(rows)
    print(f"  G3 mapping scope: {g3_checks} -> "
          f"{'PASS' if g3 else 'REFUTED'}")

    # ---- sim ----------------------------------------------------------------
    t_sim0 = time.perf_counter()
    arms, timings = run_arms(rows)
    sim_s = time.perf_counter() - t_sim0
    attach_sim(rows, arms)
    t_map_s = time.perf_counter() - t_start - sim_s
    print(f"  sim: {len(arms)} arms x {len(SEEDS)} seeds in {sim_s:.1f}s "
          f"({n_arms_full} unique arms in the full corpus)")

    g2, g2_checks = gate_g2(arms, timings)
    print(f"  G2 arm integrity: {g2_checks} -> "
          f"{'PASS' if g2 else 'REFUTED'}")
    g4, g4_pack = gate_g4(rows, n_db)
    print(f"  G4 accounting: {g4_pack['checks']} -> "
          f"{'PASS' if g4 else 'REFUTED'}")
    print(f"  statuses: {g4_pack['statuses']}")

    # ---- aggregates ----------------------------------------------------------
    scored = [r for r in rows if r["status"] == "scored"]
    mae_raw, n_raw = mae(rows, "recorded_raw", use_excl=False)
    mae_cons, n_cons = mae(rows, "recorded_corrected", use_excl=False)
    mae_dec, n_dec = mae(rows, "recorded_corrected", use_excl=True)
    decode_acc = (float(np.mean([r["decode_match"] for r in scored]))
                  if scored else float("nan"))
    grouped: dict = defaultdict(list)
    for r in scored:
        grouped[r["group"]].append(r)
    decode_by_group = {
        g: {"n": len(v),
            "accuracy": round(float(np.mean([x["decode_match"]
                                             for x in v])), 4)}
        for g, v in sorted(grouped.items())}
    confusion = Counter((r["recorded_dominant"], r["pred_dominant"])
                        for r in scored)

    by_group = {}
    for g in sorted(grouped):
        gr = grouped[g]
        d = [abs(r["sim"] - r["recorded_corrected"]) for r in gr
             if not r["excluded_C4"]]
        by_group[g] = {"n": len(gr),
                       "recorded_mean": round(float(np.mean(
                           [r["recorded_raw"] for r in gr])), 3),
                       "sim_mean": round(float(np.mean(
                           [r["sim"] for r in gr])), 3),
                       "mae_dec": round(float(np.mean(d)), 4) if d
                       else None}

    print(f"\n  MAE raw {mae_raw:.3f} (n={n_raw}) | conservative "
          f"{mae_cons:.3f} (n={n_cons}) | decoded {mae_dec:.3f} "
          f"(n={n_dec}; L74 reference {PIN_L74_MAE['decoded']})")
    print(f"  decode accuracy: {decode_acc:.3f} over {len(scored)} "
          f"scored rows; confusion {dict(confusion)}")
    for g, v in by_group.items():
        print(f"    {str(g):12s} n={v['n']:4d} rec {v['recorded_mean']:.2f} "
              f"sim {v['sim_mean']:.2f} mae_dec {v['mae_dec']}")

    # ---- G5/G6 (full-run gates; pilot deposits the indicative value) ------
    if mode == "full":
        g5 = bool(abs(mae_dec - PIN_L74_MAE["decoded"]) <= 0.01
                  and abs(mae_raw - PIN_L74_MAE["raw"]) <= 0.01)
        g6 = bool(decode_acc >= 0.60)
        g5_note = (f"decoded {mae_dec:.4f} vs 0.290; raw {mae_raw:.4f} "
                   f"vs 0.371")
        g6_note = f"decode {decode_acc:.3f} vs bar 0.60"
    else:
        g5 = None
        g6 = None
        g5_note = (f"pilot indicative: decoded {mae_dec:.4f} vs 0.290, "
                   f"raw {mae_raw:.4f} vs 0.371 (readable only on the "
                   f"full run)")
        g6_note = (f"pilot indicative: decode {decode_acc:.3f} "
                   f"(readable only on the full run)")
    g7 = bool(np.isfinite(sim_s) and timings)

    # ---- timing + the full-run estimate --------------------------------------
    per_arm = sorted(timings.values())
    arm_mean = float(np.mean(per_arm)) if per_arm else 0.0
    if mode == "full":
        est_full_s = time.perf_counter() - t_start
        est_note = "measured (this run IS the full run)"
    else:
        unseen = max(0, n_arms_full - len(arms))
        # two bounds: optimistic (mean arm) and conservative (mean of the
        # slowest 3 observed arm classes — the inline-walk gj arms)
        slow = sorted(per_arm)[-3:]
        slow_mean = float(np.mean(slow)) if slow else arm_mean
        est_lo = unseen * arm_mean + t_map_s
        est_hi = unseen * slow_mean + t_map_s
        est_full_s = est_hi
        est_note = (f"extrapolated band: [{est_lo:.0f}s (unseen x mean arm), "
                    f"{est_hi:.0f}s (unseen x slow-arm mean)] + mapping "
                    f"{t_map_s:.1f}s; deposited number is the conservative "
                    f"end")
    wall_s = time.perf_counter() - t_start
    print(f"\n  wall {wall_s:.1f}s; full-run estimate {est_full_s:.0f}s "
          f"({est_full_s / 60.0:.1f} min) — {est_note}")

    unmapped = Counter((r["status"], r["group"], r["plane"])
                       for r in rows if r["status"].startswith("unmapped"))
    out = {
        "exp": "exp118_corpus_full_mine",
        "mode": mode,
        "pilot_rule": (f"systematic stride {PILOT_STRIDE} over the "
                       f"outcome-bearing rows sorted by eid (deterministic; "
                       f"chosen over first-N because eid order clusters "
                       f"by publication)") if mode == "pilot" else None,
        "stack": ("adopted corpus mapping = exp88 C1-C4 arms + exp91/92 "
                  "row-level dose classes (L74), exp108-117 compiler "
                  "dials out of scope for 1D-sheet corpus arms (L98)"),
        "n_db_total": n_db,
        "accounting": g4_pack["statuses"],
        "coverage": {
            "n_outcome_bearing": len(outcome_rows),
            "n_mapped_arms": sum(1 for r in rows if r["arm"]),
            "n_scored_this_run": len(scored),
            "mapped_fraction_of_outcome": round(
                sum(1 for r in rows if r["arm"]) / len(outcome_rows), 4),
            "unmapped_by_status_group_plane": {
                f"{s}|{g}|{p}": n for (s, g, p), n in
                sorted(unmapped.items(), key=lambda kv: -kv[1])},
        },
        "sim_cost": {
            "n_unique_arms_full_corpus": n_arms_full,
            "n_arms_run": len(arms),
            "per_arm_s_mean": round(arm_mean, 4),
            "per_arm_s_max": round(max(per_arm), 4) if per_arm else None,
            "total_sim_s": round(sim_s, 2),
            "wall_s": round(wall_s, 2),
            "full_run_estimate_s": round(est_full_s, 1),
            "full_run_estimate_min": round(est_full_s / 60.0, 2),
            "full_run_estimate_band_s": (
                None if mode == "full" else
                [round(est_lo, 1), round(est_hi, 1)]),
            "estimate_note": est_note,
            "per_arm_timings_s": {k: round(v, 4)
                                  for k, v in sorted(timings.items())},
        },
        "aggregates": {
            "mae_raw": round(mae_raw, 4),
            "mae_corrected_conservative": round(mae_cons, 4),
            "mae_corrected_decoded": round(mae_dec, 4),
            "n_raw": n_raw, "n_conservative": n_cons, "n_decoded": n_dec,
            "decode_accuracy": None if mode != "full" and
            not np.isfinite(decode_acc) else round(float(decode_acc), 4),
            "decode_by_group": decode_by_group,
            "confusion_recorded_vs_pred": {
                f"{k[0]}->{k[1]}": v for k, v in sorted(confusion.items())},
        },
        "by_group": by_group,
        "comparison": {
            "ledger_references": LEDGER_REFERENCES,
            "this_run": {"mae_raw": round(mae_raw, 4),
                         "mae_decoded": round(mae_dec, 4),
                         "decode_accuracy": round(float(decode_acc), 4),
                         "n_scored": len(scored),
                         "note": ("full corpus" if mode == "full" else
                                  "pilot stride-10 subsample; the "
                                  "record-side frames are full-corpus "
                                  "quantities in both modes")},
        },
        "arm_table": arms,
        "criteria": {
            "G1_extraction_parity": g1,
            "G2_arm_integrity": g2,
            "G3_mapping_scope": g3,
            "G4_full_accounting": g4,
            "G5_corpus_parity_l74": g5,
            "G6_decode_bar": g6,
            "G7_timing_deposit": g7,
        },
        "gate_details": {"G1": g1_checks, "G2": g2_checks, "G3": g3_checks,
                         "G4": g4_pack["checks"],
                         "G5_note": g5_note, "G6_note": g6_note},
        "per_record": rows,
        "notes": (
            "First run over ALL 1,716 PlanformDB experiments under the "
            "adopted corpus stack: per-experiment predicted-vs-published, "
            "three-frame MAE, decode accuracy, slice flags per row "
            "(exp27/exp60/exp70/exp88/exp92), full unmapped accounting, "
            "and the full-run wall-clock estimate. exp91/exp92's own "
            "results JSONs are absent from results/ (the 2-a rollback "
            "incident) — the full run re-deposits the L74 reference "
            "independently (G5). Nothing fitted; no core edits."),
    }
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {out_path}")
    readable = {k: v for k, v in out["criteria"].items() if v is not None}
    npass = sum(1 for v in readable.values() if v)
    deferred = [k for k, v in out["criteria"].items() if v is None]
    tail = (f" ({', '.join(deferred)} deferred to the full run)"
            if deferred else "")
    print(f"  === {npass}/{len(readable)} readable gates PASS{tail} ===")
    return out


if __name__ == "__main__":
    main()
