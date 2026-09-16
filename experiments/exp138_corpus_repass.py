#!/usr/bin/env python3
"""exp138 — THE CORPUS RE-PASS WITH THE CURRENT STACK (workstream E;
task E pre-registration written BEFORE the run).

CLAIM UNDER TEST: the CURRENT stack — the v2 price oracle (exp114/117),
the corrected censoring frame (the adopted C3/C3'/C4 record-side
corrections + the exp125/127 deadline-arc censoring instruments), the
coin L=0.75 prior (exp126 Panel A: the p=0.8 rung of the coin ladder
landed ON the record's plateau, rate 0.75), and the canon-read
re-pricing (exp128's gap-fidelity/zone-drag trade-off + exp133's
"ARZ readout rate-inert, anterior role = M33 pole alone") — beats the
L74-adopted corpus reference (decoded MAE 0.290, exp118 full mine)
on the FULL PlanformDB corpus when its components are applied at every
legitimate touchpoint, with NO free parameter re-fit against the
corpus (else REFUTE as leakage).

PRIOR REFERENCE (bit-identity precondition): exp118_corpus_full.json
(deposited): decoded MAE 0.290 (n=884), raw 0.3705 (n=905), decode
accuracy 0.6928, 47 deduped arms x 3 seeds (1,2,3), 905 scored rows of
1,716. The baseline pass below re-derives that deposit with the OLD
config (exp118's build_rows + run_arm_v5/run_arm_dose dispatch,
verbatim) and must match it BIT-IDENTICALLY before the current-stack
config is swapped in.

THE TOUCHPOINT MAP (pre-registered; where each current-stack component
can legally touch the corpus pipeline — everything else is verbatim):

  M-COIN  (coin L=0.75 prior, exp126 L107 + exp86 RR-G3): the
          neoblast-family arm (other_rnai -> protocol 'neoblast') is
          the ONE arm the coin mechanism was adopted into (M37-A pool
          composition, neoblast_coin_p=0.8, exp88 C2). The current
          stack's deposit for that arm is exp126's Panel A p=0.8 rung:
          run_arm86(plane, seed, 0.8, read_kw=M33_KW) on 12 FRESH
          seeds (11..22, the exp86 FRESH_SEEDS convention), pooled
          rate 0.75. The current-stack config re-estimates the three
          neoblast arms (head/tail/trunk) under exactly that deposited
          protocol (coin 0.8 unchanged; the deposited read weight
          phi_readout=0.75 of M33_KW replacing exp88's corpus-local
          1.0; 12 fresh seeds replacing 3). The estimator upgrade is
          NOT a re-fit: p, the read weight, and the seed convention
          are deposited constants (exp86/exp126); the rate is an
          output of a fixed mechanism, measured with the stack's own
          instrument.
  M-CANON (canon-read re-pricing, exp128 L112 + exp133): the corpus
          GJ-block arms carry arz_readout=1.0 (exp70). exp133's
          rate-inert deposit says the ARZ wound-domain readout moves
          no rate and the anterior role is the M33 pole alone. The
          re-pricing is MEASURED on the corpus arms as a side-car
          (SC-2: arz-on vs arz-off at 12 fresh seeds, pooled per
          schedule) but is NOT adopted into the gate config: the
          corpus mapping pins run_gj_onset verbatim (L70/L74), the
          arz knob shifts the RNG stream (1+K draws per guess-path
          cell) so a 3-seed "no-op" adoption would inject pure Monte
          Carlo noise into the gate. The neoblast arm's
          spec_read_bypass_gap is inert at gap 1.0 (w = phi_readout
          either way) — stated, zero by construction.
  M-ORACLE (v2 oracle, exp114/117): ZERO by scope. The exp108-117
          arc prices SUBSTRATE dials for the compiler (the walk-speed
          dial, the mu-silence law); the corpus arms run on the
          standard 1D N=100 sheet — the DEFAULT0 class at its
          verified cell (1, 0.015) — where the price map offers no
          dial (exp118's scope note, restated L98; exp114's domain
          statement: the oracle prices the ends at class level).
          Contributes exactly 0; nothing to run.
  M-CENSOR (corrected censoring): the record-side frame IS the
          corrected-censored frame in the 0.290 baseline (C3 the
          generic hot-bias subtraction, C3' the per-plane control
          anchor, C4 the scoring-inconsistency exclusion) — zero
          delta by construction; the deadline-arc censoring
          instruments (censored-onset cells) have no corpus
          touchpoint. Frame integrity is ASSERTED per-row against
          the exp118 deposit.

CONFIG DELTAS (complete list; everything else verbatim):
  neoblast arms: seeds (1,2,3) -> (11..22); read phi_readout
  1.0 -> 0.75 (M33_KW, exp86/126 deposited). Coin stays 0.8.
  PROVENANCE (all non-corpus): coin 0.8 = exp88 C2 / exp86 RR-G3 /
  exp126 Panel A; phi 0.75 = exp86 M33_KW (the established read
  weight) as used by exp126's deposited ladder; fresh-seed convention
  = exp86 FRESH_SEEDS / exp126 Panel A. No corpus-derived number
  enters the sim config.

PRE-REGISTERED GATES (fixed before the run):

  GATE-E0  SANITY PRECONDITION (must PASS before E1 is readable):
           (a) extraction parity — the L73 block (n=17, mean 0.189),
           the L74 modulator block (n=11, mean 0.105), the per-plane
           control rates (head 0.00 / trunk 0.38 / tail 0.49), the C4
           exclusion count (21); (b) the baseline arm table is
           BIT-IDENTICAL to the deposited exp118 arm_table (47/47
           rates); (c) the baseline aggregates reproduce the deposit
           (raw 0.3705, decoded 0.2900, decode 0.6928, n 905/884,
           each to 4dp); (d) frame integrity — every scored row's
           recorded_corrected equals the deposit's. A miss means the
           harness drifted: REFUTE the harness, no claim tested.
  GATE-E1  THE CLAIM: the current-stack config's FULL-corpus decoded
           MAE (same decoded row set, n=884) is STRICTLY < 0.290.
  GATE-E2  NO-SLICE-REGRESSION: three slices by arm protocol class —
           S1 junction/bioelectric {cutting, gjblock*}, S2 dose/
           pharmacology {ion_channel, wnt, apc}, S3 gene/knockout
           {neoblast, generic}. S1 and S2 deltas must be EXACTLY 0
           (no component touches them; a nonzero delta is a harness
           bug and voids the run) and S3's decoded MAE may regress by
           at most +0.02 (pre-registered tolerance). Per-slice deltas
           deposited.
  GATE-E3  NO-LEAKAGE (procedural): every config delta carries a
           deposited non-corpus provenance (the table above); no
           parameter is searched against the corpus MAE in this
           module (the sensitivity/side-car columns are reported but
           cannot feed back into the gate config); the gate config is
           the one written here, before the run.

REGISTERED SIDE-CHECKS (reported, NOT gates; cannot alter the config):
  SC-1  COIN CONTINUITY: the re-formed neoblast arms at 12 fresh
        seeds pooled over head/tail/trunk reproduce exp126's
        deposited p=0.8 rung BIT-EXACTLY (same functions, same seeds,
        same planes -> 0.75). A miss is a harness-drift alarm.
  SC-2  ARZ RATE-INERT ON THE CORPUS ARMS: per GJ schedule
        (sustained/delayed/washout), 12-fresh-seed pooled rates
        (planes head/tail/trunk, Panel-C comparable) with arz on
        (run_gj_onset verbatim) vs arz off (local one-knob copy):
        |on - off| <= 0.10 confirms the exp133 re-pricing transfers
        to the corpus operating point (gap 0.05); the arz-on column
        must also land within +/-0.15 of exp126 Panel C's coin=None
        rates (0.667/0.944/0.028) — the side-car's own continuity
        anchor.
  SC-3  FRAME SPLIT: the same config delta evaluated against the RAW
        record frame (no C3/C3'/C4) — names WHICH FRAME the coin
        prior helps (the decomposition's key column).
  SC-4  SENSITIVITY COLUMNS: (a) the estimator-only variant (12 fresh
        seeds at exp88's phi=1.0) — separates the seed-count effect
        from the read re-pricing effect; (b) the flat-prior variant
        (all three neoblast arms set to the deposited pooled 0.75,
        no runs) — the most leakage-proof form of the prior.

IF MAE DOES NOT IMPROVE: the decomposition below IS the result —
per-component deltas (coin measured; canon side-car verdict; oracle 0
by scope; censoring 0 by construction), per-plane neoblast rate
moves, per-arm deltas, and the SC-3 frame split naming which frame
fights the coin prior.

RUN: two full passes (old config, current config) over all 47 deduped
arms x seeds + 36 neoblast fresh-seed runs + the SC-2 side-car grid;
executed in the three slices for the run log; the gates are evaluated
on the FULL corpus. Wall-clock deposited (the 20-minute subsample
clause is not expected to bind: exp118's full sim was ~3 s).
"""
from __future__ import annotations

import json
import os
import sys
import time
from collections import defaultdict

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp118_corpus_full_mine import build_rows  # noqa: E402
from experiments.exp88_corpus_rewire import run_arm_v5, M33 as M33_EXP88  # noqa: E402
from experiments.exp91_dose_axis_wiring import run_arm_dose  # noqa: E402
from experiments.exp86_regen_read import run_arm86, M33_KW  # noqa: E402
from experiments.exp70_onset_corpus import (  # noqa: E402
    run_gj_onset, regen_region, D_ADOPTED,
)
from experiments.exp60_gene_layer import DT  # noqa: E402
from experiments.exp32_m26_repairs import (  # noqa: E402
    HEAD, TAILP, TRUNK, TAIL,
)
from cultivation.bioelectric.morphospace import (  # noqa: E402
    head_likeness, wildtype_target,
)
from experiments.exp27_stage2_pilot import (  # noqa: E402
    N as CHAIN_N, ABN_ERR_MV, ABN_HL, make_collective,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp138_corpus_repass.json")

SEEDS_BASE = (1, 2, 3)                 # the L70-L74 corpus convention
SEEDS_FRESH = tuple(range(11, 23))     # the exp86/exp126 fresh convention
COIN_P = 0.8                           # unchanged (exp88 C2, exp126)
REF = {"mae_raw": 0.3705, "mae_decoded": 0.29, "decode_acc": 0.6928,
       "n_raw": 905, "n_decoded": 884}
PIN = {"l73": {"n": 17, "mean": 0.189}, "l74": {"n": 11, "mean": 0.105},
       "ctrl": {"head": 0.00, "trunk": 0.38, "tail": 0.49}, "c4": 21}

SLICES = {
    "S1_junction_bioelectric": {"cutting", "gjblock", "gjblock_delayed",
                                "gjblock_washout"},
    "S2_dose_pharmacology": {"ion_channel", "wnt", "apc"},
    "S3_gene_knockout": {"neoblast", "generic"},
}

# exp126 Panel C coin=None column (the side-car's continuity anchor)
PANEL_C_NONE = {"sustained": 0.667, "delayed": 0.944, "washout": 0.028}
GJ_PLANES = ("head", "tail", "trunk")   # Panel-C comparable pooling


# ------------------------------------------------------------- arm runners
def run_arm_base(arm: tuple, seed: int) -> bool:
    """exp118's dispatch verbatim (the OLD config)."""
    protocol, plane, cf, dose = arm
    if protocol in ("wnt", "apc"):
        return run_arm_dose(protocol, plane, cf, seed,
                            cns=1.0, diff=0.0, dose=dose)
    return run_arm_v5(protocol, plane, cf, seed)


def run_neoblast_current(plane: str, seed: int) -> bool:
    """M-COIN: the neoblast arm under the exp126-deposited protocol —
    run_arm86 verbatim at coin 0.8 with the M33_KW read (phi 0.75)."""
    return run_arm86(plane, seed, COIN_P, read_kw=M33_KW)


def run_neoblast_phi1(plane: str, seed: int) -> bool:
    """SC-4a estimator-only variant: 12 fresh seeds at exp88's
    corpus-local read (phi 1.0) — coin and gating identical."""
    return run_arm86(plane, seed, COIN_P, read_kw=M33_EXP88)


def run_gj_onset_noarz(seed: int, plane: str, cut_f: float,
                       onset: str) -> bool:
    """SC-2's arz-off arm: run_gj_onset verbatim with the ONE-KNOB
    diff arz_readout 1.0 -> 0.0 (exp133's rate-inert claim under
    test on the corpus operating point)."""
    c = make_collective(seed)
    c.block_gap_junctions(0.05)
    c.run(24, dt=DT)
    kw = dict(cell_period=0.8, dt=DT, noise=0.6,
              phi_readout=0.75, neural_readout=1.0, arz_readout=0.0,
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
        ci = min(max(int(round(cut_f * CHAIN_N)), 5), CHAIN_N - 1)
        c.amputate(slice(ci, CHAIN_N), wound_voltage=-30.0,
                   blastema_theta=-40.0)
        regions = [(slice(ci, CHAIN_N), "forward")]
    if onset == "sustained":
        for reg, direction in regions:
            c.regrow(reg, direction=direction, **kw) \
                if direction != "forward" else c.regrow(reg, **kw)
    else:
        t_switch = 2.0
        for reg, direction in regions:
            idx = list(np.arange(CHAIN_N)[reg])
            if direction == "backward":
                src = idx[-1] + 1 if idx[-1] + 1 < CHAIN_N else idx[-1]
                order = list(reversed(idx))
            else:
                src = idx[0] - 1 if idx[0] - 1 >= 0 else idx[0]
                order = idx
            wound_center = float(np.mean(c.theta[idx]))
            r = 1.0 if onset == "delayed" else 0.05
            t = 0.0
            for i in order:
                dur = 0.8 * (1.0 + 2.0 * (1.0 - r))
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
    wt = wildtype_target(CHAIN_N)
    reg = regen_region(plane)
    rerr = float(np.mean(np.abs(c.V[reg] - wt[reg])))
    return bool(rerr >= ABN_ERR_MV or head_likeness(c.V, TAIL) >= ABN_HL)


# ------------------------------------------------------------ arm plumbing
def slice_of(arm: tuple) -> str:
    for name, protos in SLICES.items():
        if arm[0] in protos:
            return name
    raise ValueError(f"arm {arm} outside the slice map")


def run_pass(rows: list[dict], current: bool) -> tuple[dict, dict, dict]:
    """Run every deduped arm of the corpus under the requested config,
    executed slice-by-slice for the run log. Returns (rates, timings,
    per_slice_sim_s)."""
    arm_keys = sorted({tuple(r["arm"]) for r in rows
                       if r["status"] == "scored"})
    rates: dict[str, float] = {}
    timings: dict[str, float] = {}
    slice_s: dict[str, float] = {s: 0.0 for s in SLICES}
    for slice_name in SLICES:
        for k in arm_keys:
            if slice_of(k) != slice_name:
                continue
            t0 = time.perf_counter()
            if current and k[0] == "neoblast":
                runs = [run_neoblast_current(k[1], s)
                        for s in SEEDS_FRESH]
            else:
                runs = [run_arm_base(k, s) for s in SEEDS_BASE]
            dt = time.perf_counter() - t0
            timings[str(k)] = dt
            slice_s[slice_name] += dt
            rates[str(k)] = round(float(np.mean(runs)), 3)
    return rates, timings, slice_s


def aggregate(rows: list[dict], rates: dict, neoblast_override=None):
    """Attach sims and compute the frames. neoblast_override: optional
    {arm_key: rate} for the flat-prior sensitivity column."""
    scored = [r for r in rows if r["status"] == "scored"]
    for r in scored:
        key = str(tuple(r["arm"]))
        if neoblast_override is not None and r["arm"][0] == "neoblast":
            r["sim"] = neoblast_override[key]
        else:
            r["sim"] = rates[key]
        r["abs_err_raw"] = round(abs(r["sim"] - r["recorded_raw"]), 4)
        r["abs_err_corrected"] = round(
            abs(r["sim"] - r["recorded_corrected"]), 4)
        r["pred_dominant"] = "abnormal" if r["sim"] >= 0.5 else "wt"
        r["recorded_dominant"] = ("abnormal" if r["recorded_raw"] >= 0.5
                                  else "wt")
        r["decode_match"] = bool(r["pred_dominant"]
                                 == r["recorded_dominant"])
    dec = [r for r in scored if not r["excluded_C4"]]
    mae_raw = float(np.mean([r["abs_err_raw"] for r in scored]))
    mae_dec = float(np.mean([r["abs_err_corrected"] for r in dec]))
    acc = float(np.mean([r["decode_match"] for r in scored]))
    return scored, dec, {"mae_raw": mae_raw, "mae_decoded": mae_dec,
                         "decode_acc": acc, "n_raw": len(scored),
                         "n_decoded": len(dec)}


def slice_maes(dec: list[dict]) -> dict:
    out = {}
    for name in SLICES:
        rs = [r for r in dec if slice_of(tuple(r["arm"])) == name]
        out[name] = {
            "n": len(rs),
            "mae_decoded": round(float(np.mean(
                [r["abs_err_corrected"] for r in rs])), 4) if rs else None,
            "mae_raw": round(float(np.mean(
                [r["abs_err_raw"] for r in rs])), 4) if rs else None,
        }
    return out


def main() -> dict:
    t_start = time.perf_counter()
    print("=== exp138: the corpus re-pass with the current stack ===\n")

    # ---- the corpus extraction (exp118's exact path) --------------------
    rows, stats = build_rows()
    n_db = stats["n_db_total"]

    dep = json.load(open(os.path.join(
        ROOT, "results", "exp118_corpus_full.json")))
    dep_rows = {r["eid"]: r for r in dep["per_record"]}

    # ---- GATE-E0a: extraction parity ------------------------------------
    e0a = (stats["l73_block"]["n"] == PIN["l73"]["n"]
           and abs(stats["l73_block"]["mean"] - PIN["l73"]["mean"]) <= 0.01
           and stats["l74_modulator"]["n"] == PIN["l74"]["n"]
           and abs(stats["l74_modulator"]["mean"]
                   - PIN["l74"]["mean"]) <= 0.01
           and all(p in stats["ctrl_rate"]
                   and abs(stats["ctrl_rate"][p] - v) <= 0.01
                   for p, v in PIN["ctrl"].items())
           and stats["n_c4"] == PIN["c4"])
    print(f"  E0a extraction parity: l73 {stats['l73_block']} l74 "
          f"{stats['l74_modulator']} ctrl "
          f"{ {k: round(v, 3) for k, v in stats['ctrl_rate'].items()} } "
          f"C4 {stats['n_c4']} -> {'PASS' if e0a else 'REFUTED'}")

    # frame integrity (E0d, checked before any sim)
    frame_ok = True
    for r in rows:
        if r["status"] == "scored":
            d = dep_rows.get(r["eid"])
            if d is None or r["recorded_corrected"] != \
                    d["recorded_corrected"] or \
                    r["recorded_raw"] != d["recorded_raw"]:
                frame_ok = False
    print(f"  E0d frame integrity (per-row vs exp118 deposit): "
          f"{'PASS' if frame_ok else 'REFUTED'}")

    # ---- PASS 0: the OLD config (bit-identity precondition) --------------
    print("\n  PASS 0 — the old config (exp118 verbatim re-derivation):")
    base_rates, base_timings, base_slice_s = run_pass(rows, current=False)
    scored, dec, agg_base = aggregate(rows, base_rates)

    dep_arm = dep["arm_table"]
    arm_match = sum(1 for k, v in dep_arm.items()
                    if base_rates.get(k) == v)
    e0b = arm_match == len(dep_arm) == len(base_rates)
    print(f"  E0b arm-table bit-identity: {arm_match}/{len(dep_arm)} "
          f"-> {'PASS' if e0b else 'REFUTED'}")
    e0c = (round(agg_base["mae_raw"], 4) == REF["mae_raw"]
           and round(agg_base["mae_decoded"], 4) == REF["mae_decoded"]
           and round(agg_base["decode_acc"], 4) == REF["decode_acc"]
           and agg_base["n_raw"] == REF["n_raw"]
           and agg_base["n_decoded"] == REF["n_decoded"])
    print(f"  E0c aggregates: raw {agg_base['mae_raw']:.4f} decoded "
          f"{agg_base['mae_decoded']:.4f} decode "
          f"{agg_base['decode_acc']:.4f} n {agg_base['n_raw']}/"
          f"{agg_base['n_decoded']} -> {'PASS' if e0c else 'REFUTED'}")
    base_slices = slice_maes(dec)
    for s, v in base_slices.items():
        print(f"    {s}: n={v['n']} mae_dec={v['mae_decoded']} "
              f"mae_raw={v['mae_raw']}")

    # snapshot the baseline per-row state (for deltas)
    base_row = {r["eid"]: {"sim": r["sim"],
                           "err_dec": r["abs_err_corrected"],
                           "err_raw": r["abs_err_raw"]}
                for r in scored}

    # ---- SC-1: coin continuity (bit-exact vs exp126's p=0.8 rung) -------
    print("\n  SC-1 coin continuity (exp126 Panel A p=0.8 re-run):")
    sc1_runs = [run_neoblast_current(pl, s)
                for pl in ("head", "tail", "trunk") for s in SEEDS_FRESH]
    sc1_pooled = round(float(np.mean(sc1_runs)), 4)
    sc1_ok = abs(sc1_pooled - 0.75) <= 1e-9
    print(f"    pooled rate over 3 planes x 12 fresh seeds: "
          f"{sc1_pooled} (deposited 0.75) -> "
          f"{'MATCH' if sc1_ok else 'DRIFT'}")

    # ---- PASS 1: the CURRENT-STACK config --------------------------------
    print("\n  PASS 1 — the current-stack config (M-COIN live; "
          "M-CANON/M-ORACLE/M-CENSOR zero by the touchpoint map):")
    cur_rates, cur_timings, cur_slice_s = run_pass(rows, current=True)
    scored, dec, agg_cur = aggregate(rows, cur_rates)

    untouched_ok = all(cur_rates[k] == base_rates[k] for k in base_rates
                       if not k.startswith("('neoblast'"))
    changed_arms = {k: {"old": base_rates[k], "new": cur_rates[k]}
                    for k in base_rates if cur_rates[k] != base_rates[k]}
    print(f"  untouched-arm integrity (non-neoblast bit-identity): "
          f"{'PASS' if untouched_ok else 'REFUTED'}")
    print(f"  changed arms: {changed_arms}")
    cur_slices = slice_maes(dec)
    for s, v in cur_slices.items():
        print(f"    {s}: n={v['n']} mae_dec={v['mae_decoded']} "
              f"mae_raw={v['mae_raw']}")

    # ---- GATES E1 / E2 ---------------------------------------------------
    e1 = bool(agg_cur["mae_decoded"] < 0.290)
    print(f"\n  GATE-E1 decoded MAE {agg_cur['mae_decoded']:.4f} vs "
          f"0.290 -> {'PASS' if e1 else 'REFUTED'}")

    s1d = round(cur_slices["S1_junction_bioelectric"]["mae_decoded"]
                - base_slices["S1_junction_bioelectric"]["mae_decoded"], 6)
    s2d = round(cur_slices["S2_dose_pharmacology"]["mae_decoded"]
                - base_slices["S2_dose_pharmacology"]["mae_decoded"], 6)
    s3d = round(cur_slices["S3_gene_knockout"]["mae_decoded"]
                - base_slices["S3_gene_knockout"]["mae_decoded"], 6)
    e2 = bool(s1d == 0.0 and s2d == 0.0 and s3d <= 0.02)
    print(f"  GATE-E2 slice deltas: S1 {s1d:+.4f} (need 0) S2 {s2d:+.4f} "
          f"(need 0) S3 {s3d:+.4f} (tol +0.02) -> "
          f"{'PASS' if e2 else 'REFUTED'}")

    # ---- GATE-E3 (procedural): provenance table --------------------------
    provenance = {
        "coin_p_0.8": "exp88 C2 (L70) adopted; exp86 RR-G3; exp126 "
                      "Panel A deposit — non-corpus",
        "phi_readout_0.75": "exp86 M33_KW (the established read weight); "
                            "the exp126 deposited ladder's read form — "
                            "non-corpus",
        "seeds_11_22": "exp86 FRESH_SEEDS convention / exp126 Panel A "
                       "instrument — non-corpus",
        "record_frame": "UNCHANGED (C3/C3'/C4 verbatim from exp118)",
        "all_other_arms": "UNCHANGED (exp118 dispatch verbatim)",
    }
    e3 = all("non-corpus" in v or "UNCHANGED" in v
             for v in provenance.values())
    print(f"  GATE-E3 no-leakage provenance: {len(provenance)} entries "
          f"all deposited/non-corpus -> {'PASS' if e3 else 'REFUTED'}")

    # ---- SC-2: the ARZ rate-inert side-car -------------------------------
    print("\n  SC-2 ARZ rate-inert side-car (12 fresh seeds, pooled "
          "head/tail/trunk):")
    sc2 = {}
    for onset in ("sustained", "delayed", "washout"):
        on = [run_gj_onset(s, pl, 0.5, onset)
              for pl in GJ_PLANES for s in SEEDS_FRESH]
        off = [run_gj_onset_noarz(s, pl, 0.5, onset)
               for pl in GJ_PLANES for s in SEEDS_FRESH]
        r_on, r_off = float(np.mean(on)), float(np.mean(off))
        sc2[onset] = {"arz_on": round(r_on, 4),
                      "arz_off": round(r_off, 4),
                      "delta": round(r_off - r_on, 4),
                      "panelC_none_ref": PANEL_C_NONE[onset],
                      "on_vs_panelC": round(r_on - PANEL_C_NONE[onset],
                                            4),
                      "rate_inert": bool(abs(r_off - r_on) <= 0.10),
                      "continuity": bool(
                          abs(r_on - PANEL_C_NONE[onset]) <= 0.15)}
        print(f"    {onset:9s} on {r_on:.3f} off {r_off:.3f} "
              f"delta {r_off - r_on:+.3f} (tol 0.10) | PanelC-None ref "
              f"{PANEL_C_NONE[onset]:.3f} (tol 0.15) -> "
              f"inert {'Y' if sc2[onset]['rate_inert'] else 'N'} / "
              f"cont {'Y' if sc2[onset]['continuity'] else 'N'}")
    sc2_verdict = all(v["rate_inert"] for v in sc2.values())
    print(f"    SC-2 verdict: the exp133 rate-inert re-pricing "
          f"{'TRANSFERS to' if sc2_verdict else 'FAILS ON'} the corpus "
          f"GJ operating point")

    # ---- SC-3: the frame split -------------------------------------------
    raw_base = agg_base["mae_raw"]
    raw_cur = agg_cur["mae_raw"]
    sc3 = {"mae_raw_base": round(raw_base, 4),
           "mae_raw_current": round(raw_cur, 4),
           "delta": round(raw_cur - raw_base, 4)}
    print(f"\n  SC-3 frame split: raw-frame MAE {raw_base:.4f} -> "
          f"{raw_cur:.4f} (delta {raw_cur - raw_base:+.4f}) vs decoded "
          f"delta {agg_cur['mae_decoded'] - agg_base['mae_decoded']:+.4f}")

    # ---- SC-4: sensitivity columns ----------------------------------------
    print("\n  SC-4 sensitivity columns:")
    # (a) estimator-only: 12 fresh seeds at exp88's phi=1.0
    sens_rates = dict(base_rates)
    for pl in ("head", "tail", "trunk"):
        runs = [run_neoblast_phi1(pl, s) for s in SEEDS_FRESH]
        sens_rates[str(("neoblast", pl, 0.5, None))] = \
            round(float(np.mean(runs)), 3)
    _, dec_s, agg_sens = aggregate(
        [{**r} for r in rows], sens_rates)
    # (b) flat prior: the deposited pooled 0.75 for every neoblast arm
    flat = {str(("neoblast", pl, 0.5, None)): 0.75
            for pl in ("head", "tail", "trunk")}
    _, dec_f, agg_flat = aggregate([{**r} for r in rows],
                                   dict(base_rates),
                                   neoblast_override=flat)
    sc4 = {
        "estimator_only_12seed_phi1": {
            "arm_rates": {k: sens_rates[k] for k in sens_rates
                          if "neoblast" in k},
            "mae_decoded": round(agg_sens["mae_decoded"], 4),
            "mae_raw": round(agg_sens["mae_raw"], 4)},
        "flat_prior_0.75": {
            "mae_decoded": round(agg_flat["mae_decoded"], 4),
            "mae_raw": round(agg_flat["mae_raw"], 4)},
    }
    print(f"    estimator-only (12 seeds, phi=1.0): decoded "
          f"{agg_sens['mae_decoded']:.4f} raw {agg_sens['mae_raw']:.4f}")
    print(f"    flat prior (all neoblast arms = 0.75): decoded "
          f"{agg_flat['mae_decoded']:.4f} raw {agg_flat['mae_raw']:.4f}")

    # ---- the decomposition -------------------------------------------------
    neo_planes = {}
    for pl in ("head", "tail", "trunk"):
        key = str(("neoblast", pl, 0.5, None))
        rs = [r for r in scored if r["arm"] == ["neoblast", pl, 0.5, None]]
        if not rs:
            continue
        d_old = float(np.mean([base_row[r["eid"]]["err_dec"] for r in rs]))
        d_new = float(np.mean([r["abs_err_corrected"] for r in rs]))
        r_old = float(np.mean([base_row[r["eid"]]["err_raw"] for r in rs]))
        r_new = float(np.mean([r["abs_err_raw"] for r in rs]))
        neo_planes[pl] = {
            "n": len(rs),
            "rate_old": base_rates[key], "rate_new": cur_rates[key],
            "rate_phi1_12seed": sens_rates[key],
            "mae_dec_old": round(d_old, 4),
            "mae_dec_new": round(d_new, 4),
            "mae_raw_old": round(r_old, 4),
            "mae_raw_new": round(r_new, 4),
        }
        print(f"    neoblast {pl:6s} n={len(rs):2d} rate "
              f"{base_rates[key]} -> {cur_rates[key]} "
              f"(phi1@12seed {sens_rates[key]}); mae_dec "
              f"{d_old:.3f} -> {d_new:.3f}; mae_raw {r_old:.3f} -> "
              f"{r_new:.3f}")

    decomp = {
        "coin_prior": {
            "delta_mae_decoded": round(agg_cur["mae_decoded"]
                                       - agg_base["mae_decoded"], 4),
            "delta_mae_raw": sc3["delta"],
            "per_plane": neo_planes,
        },
        "canon_strip_repricing": {
            "delta_mae_decoded": 0.0,
            "note": "zero in the gate config by the verbatim-pins rule "
                    "(run_gj_onset pinned, L70/L74; the arz knob shifts "
                    "the RNG stream so a 3-seed adoption would inject "
                    "pure Monte Carlo noise); the side-car verdict is "
                    "SC-2",
            "sc2_rate_inert_transfers": sc2_verdict,
        },
        "v2_oracle": {
            "delta_mae_decoded": 0.0,
            "note": "zero by scope — the exp108-117 arc prices "
                    "substrate dials for the compiler; the corpus arms "
                    "are 1D-sheet chains (DEFAULT0, verified cell "
                    "(1, 0.015)); no dial to apply (exp118 scope note, "
                    "L98; exp114 domain statement)",
        },
        "corrected_censoring": {
            "delta_mae_decoded": 0.0,
            "note": "zero by construction — the record frame IS the "
                    "adopted C3/C3'/C4 corrected-censored frame in the "
                    "0.290 baseline (per-row integrity asserted, E0d)",
        },
    }

    # ---- per-record deltas (scored rows) -----------------------------------
    per_record = []
    for r in scored:
        b = base_row[r["eid"]]
        per_record.append({
            "eid": r["eid"], "group": r["group"], "plane": r["plane"],
            "arm": r["arm"],
            "recorded_raw": r["recorded_raw"],
            "recorded_corrected": r["recorded_corrected"],
            "excluded_C4": r["excluded_C4"],
            "sim_old": b["sim"], "sim_new": r["sim"],
            "err_dec_old": b["err_dec"], "err_dec_new":
                r["abs_err_corrected"],
            "err_raw_old": b["err_raw"], "err_raw_new": r["abs_err_raw"],
        })

    wall_s = time.perf_counter() - t_start
    gates = {"E0_sanity_precondition": bool(e0a and e0b and e0c
                                            and frame_ok),
             "E1_current_stack_beats_0290": e1,
             "E2_no_slice_regression": e2,
             "E3_no_leakage": e3}
    npass = sum(1 for v in gates.values() if v)
    print(f"\n  wall {wall_s:.1f}s "
          f"(PASS0 sim {sum(base_slice_s.values()):.1f}s, PASS1 sim "
          f"{sum(cur_slice_s.values()):.1f}s)")
    for s, v in base_slice_s.items():
        print(f"    slice {s}: base sim {v:.1f}s / current "
              f"{cur_slice_s[s]:.1f}s")
    print(f"  === {npass}/4 gates PASS ===")

    out = {
        "exp": "exp138_corpus_repass",
        "claim": "the current stack (v2 oracle + corrected censoring + "
                 "coin L=0.75 prior + canon-strip re-pricing) beats the "
                 "0.290 decoded MAE on the full corpus",
        "reference": {"source": "results/exp118_corpus_full.json "
                                "(L74-adopted mapping, exp118 full mine)",
                      **REF},
        "n_db_total": n_db,
        "config_deltas": provenance,
        "gates": gates,
        "gate_detail": {"E0a_extraction": e0a, "E0b_arm_bitidentity":
                        e0b, "E0c_aggregates": e0c, "E0d_frame": frame_ok,
                        "E1_mae_decoded_current":
                            round(agg_cur["mae_decoded"], 4),
                        "E2_slice_deltas": {"S1": s1d, "S2": s2d,
                                            "S3": s3d}},
        "aggregates": {"base": {k: round(v, 4) if isinstance(v, float)
                                else v for k, v in agg_base.items()},
                       "current": {k: round(v, 4)
                                   if isinstance(v, float) else v
                                   for k, v in agg_cur.items()}},
        "slices": {"base": base_slices, "current": cur_slices},
        "sc1_coin_continuity": {"pooled": sc1_pooled, "deposited": 0.75,
                                "match": sc1_ok},
        "sc2_arz_sidecar": {"per_schedule": sc2,
                            "verdict": ("RATE-INERT TRANSFERS"
                                        if sc2_verdict
                                        else "RATE-INERT FAILS ON THE "
                                             "CORPUS OPERATING POINT")},
        "sc3_frame_split": sc3,
        "sc4_sensitivity": sc4,
        "decomposition": decomp,
        "changed_arms": changed_arms,
        "arm_table_base": base_rates,
        "arm_table_current": cur_rates,
        "sim_cost": {"wall_s": round(wall_s, 2),
                     "pass0_sim_s": round(sum(base_slice_s.values()), 2),
                     "pass1_sim_s": round(sum(cur_slice_s.values()), 2),
                     "subsample_clause": "not bound (wall << 20 min); "
                                         "the FULL corpus was run"},
        "per_record": per_record,
        "notes": (
            "Workstream E: the full PlanformDB corpus (1,716 records; "
            "905 scored) re-passed through the current stack. The old "
            "config re-derives exp118's deposit bit-identically first "
            "(E0), then the current-stack config swaps in exactly one "
            "live component (the coin prior on the neoblast arm, at "
            "the exp126-deposited protocol) — the other three "
            "components have no legitimate corpus touchpoint and are "
            "deposited as zeros with their scope citations. The SC-3 "
            "frame split and the per-plane table carry the mechanism "
            "attribution either way."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
