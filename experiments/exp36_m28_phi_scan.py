#!/usr/bin/env python3
"""exp36 — M28 DUAL-FIELD: phi positional-layer scan (night-four queue,
pulled forward).

MECHANISM (collective.py regrow, additive + bit-exact at default,
verify_m26_bitexact.py green to 1e-9 + full suite green BEFORE this run):
the collective captures `phi_spec` — the identity-at-coordinate map —
when the pattern is first set (D3: the pattern survives fragmentation as
a DISTRIBUTED collective property; theta is the expression layer,
phi_spec the positional layer). regrow(phi_readout=w) blends each
committing cell's chain inheritance with phi_spec[i] at weight
w * gap_scale — the spec read is junction-carried exactly like the M25
chain read (blockade silences it). Deterministic, no new RNG draws.

RATIONALE: exp34 diagnosed the length-gradient refutation as STRUCTURAL —
a head-only fragment's stored theta carries no tail-ward trend, yet the
record shows head fragments regenerate tails at 0.52 penetrance. The phi
spec provides the missing positional information WITHOUT external target
knowledge: the spec is the animal's own distributed memory.

PRE-REGISTERED GATES (fixed BEFORE tonight's arms ran):

  M28-G1  GRADED PENETRANCE: there EXISTS phi_readout in the scan
          {0.70, 0.75, 0.80, 0.85, 0.90} with cutting_cross_a
          pred_abn_rate strictly in (0.0, 1.0) — seed-splitting,
          matching the recorded 0.52 penetrance direction (M26a/M27a
          left it 1.00 in all three seeds).
  M28-G2  COLLATERAL LOCK at every scan value:
          cutting_{tail,head,trunk} pred_abn_rate == 0.00 (they are
          0.00 and must not move), restored_tail == 0.00.
  M28-G3  innexin_tail rate preserved == 0.67 (phi_readout=0.75 arm):
          the spec read is junction-gated, so at gap_scale=0.05 only a
          ~5% bleed reaches the readout (same spirit as the M25
          r*chain term); per-seed drift <= 1.5 mV allowed, rate must
          not move.
  M28-G4  DIRECTION: at the qualifying value, sim cross-bin rates are
          non-increasing in cut fraction (Spearman rho < 0).

RUN PROTOCOL: exp31 discipline (seeds (1,2,3), window 24h dt=0.1,
thresholds unchanged, bin medians from exp31, metrics immediately after
regrow). Serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
OPENBLAS_NUM_THREADS = os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
MKL_NUM_THREADS = os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp34_m27_candidates import run_arm, sim_arm  # noqa: E402
from experiments.exp32_m26_repairs import EXP31_BINS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp36_m28_phi_scan.json")

PHI_SCAN = [0.70, 0.75, 0.80, 0.85, 0.90]
# REGISTERED AMENDMENT (after the registered scan ran): cross_a was fully
# normal at every registered value (the chain->spec transition lies BELOW
# 0.70), so the scan extends downward to locate the threshold region.
# Amendment results are labelled exploratory; G1 is evaluated on the
# REGISTERED scan only.
AMEND_SCAN = [0.20, 0.30, 0.40, 0.50, 0.60]


def main() -> dict:
    print("=== exp36: M28 dual-field phi_readout scan ===\n")

    exp31 = json.load(open(os.path.join(ROOT, "results",
                                        "exp31_stage2_widened.json")))

    sim: dict[str, dict] = {}
    for phi in PHI_SCAN:
        tag = f"p{int(round(phi * 100)):02d}"
        for b in ("a", "b", "c", "d"):
            arm = f"cutting_cross_{b}_{tag}"
            sim[arm] = sim_arm(arm, cut_f=EXP31_BINS[b], phi_readout=phi)
        for plane in ("tail", "head", "trunk"):
            arm = f"cutting_{plane}_{tag}"
            sim[arm] = sim_arm(arm, phi_readout=phi)
        sim[f"restored_tail_{tag}"] = sim_arm(f"restored_tail_{tag}",
                                              phi_readout=phi)
        s = sim[f"cutting_cross_a_{tag}"]
        print(f"  phi={phi:.2f}: cross_a rate {s['pred_abn_rate']:.2f} "
              f"(err {s['err_mean']:.2f}) | cross_b "
              f"{sim[f'cutting_cross_b_{tag}']['pred_abn_rate']:.2f} | "
              f"collat t/h/r {sim[f'cutting_tail_{tag}']['pred_abn_rate']:.2f}/"
              f"{sim[f'cutting_head_{tag}']['pred_abn_rate']:.2f}/"
              f"{sim[f'cutting_trunk_{tag}']['pred_abn_rate']:.2f} | "
              f"restored {sim[f'restored_tail_{tag}']['pred_abn_rate']:.2f}")

    sim["innexin_tail_p075"] = sim_arm("innexin_tail_m28", phi_readout=0.75)

    for phi in AMEND_SCAN:
        tag = f"p{int(round(phi * 100)):02d}"
        for b in ("a", "b", "c", "d"):
            sim[f"cutting_cross_{b}_{tag}"] = sim_arm(
                f"cutting_cross_{b}_{tag}", cut_f=EXP31_BINS[b],
                phi_readout=phi)
        s = sim[f"cutting_cross_a_{tag}"]
        print(f"  [amend] phi={phi:.2f}: cross_a rate "
              f"{s['pred_abn_rate']:.2f} (err {s['err_mean']:.2f})")

    # ---- gates ---------------------------------------------------------------
    qualifying = None
    for phi in PHI_SCAN:
        tag = f"p{int(round(phi * 100)):02d}"
        r_a = sim[f"cutting_cross_a_{tag}"]["pred_abn_rate"]
        coll_ok = all(sim[f"cutting_{p}_{tag}"]["pred_abn_rate"] == 0.0
                      for p in ("tail", "head", "trunk")) \
            and sim[f"restored_tail_{tag}"]["pred_abn_rate"] == 0.0
        if 0.0 < r_a < 1.0 and coll_ok:
            qualifying = phi
            break
    m28_g1 = qualifying is not None

    m28_g2 = True
    for phi in PHI_SCAN:
        tag = f"p{int(round(phi * 100)):02d}"
        if not all(sim[f"cutting_{p}_{tag}"]["pred_abn_rate"] == 0.0
                   for p in ("tail", "head", "trunk")):
            m28_g2 = False
        if sim[f"restored_tail_{tag}"]["pred_abn_rate"] != 0.0:
            m28_g2 = False

    inx = sim["innexin_tail_p075"]
    drift = float(np.max(np.abs(np.array(inx["err_per_seed"])
                                - np.array(exp31["sim_arms"]["innexin_tail"]["err_per_seed"]))))
    # exact-fraction comparison (2/3): the 0.67 literal is a float-equality bug
    m28_g3 = bool(abs(inx["pred_abn_rate"]
                      - exp31["sim_arms"]["innexin_tail"]["pred_abn_rate"]) < 1e-9
                  and drift <= 1.5)

    m28_g4 = False
    amend_split = None
    for phi in AMEND_SCAN:
        tag = f"p{int(round(phi * 100)):02d}"
        r_a = sim[f"cutting_cross_a_{tag}"]["pred_abn_rate"]
        if 0.0 < r_a < 1.0:
            amend_split = phi
            break
    if qualifying is not None:
        tag = f"p{int(round(qualifying * 100)):02d}"
        rates = [sim[f"cutting_cross_{b}_{tag}"]["pred_abn_rate"]
                 for b in ("a", "b", "c", "d")]
        fs = [EXP31_BINS[b] for b in ("a", "b", "c", "d")]
        from scipy.stats import spearmanr
        rho = spearmanr(fs, rates)
        m28_g4 = bool(rho.statistic < 0)

    print(f"\n  M28-G1 graded penetrance exists:          "
          f"phi={qualifying}  {'PASS' if m28_g1 else 'REFUTED'}")
    print(f"  M28-G2 collateral lock (all scan values): "
          f"{'PASS' if m28_g2 else 'REFUTED'}")
    print(f"  M28-G3 innexin rate preserved (drift {drift:.2f} mV): "
          f"{'PASS' if m28_g3 else 'REFUTED'}")
    print(f"  M28-G4 bin direction rho < 0:             "
          f"{'PASS' if m28_g4 else 'REFUTED'}")

    out = {
        "exp": "exp36_m28_phi_scan",
        "mechanism": (
            "phi_spec = identity-at-coordinate map captured at pattern set "
            "(distributed collective property, D3); regrow blends chain "
            "inheritance with spec at w = phi_readout * gap_scale "
            "(junction-carried); additive, bit-exact at default"),
        "phi_scan": PHI_SCAN,
        "sim_arms": sim,
        "qualifying_phi_readout": qualifying,
        "amendment_scan": {
            "values": AMEND_SCAN,
            "cross_a_split_at": amend_split,
            "status": "exploratory amendment — registered scan refuted G1",
        },
        "innexin_drift_mv": drift,
        "criteria": {
            "M28_G1_graded_penetrance": m28_g1,
            "M28_G2_collateral_lock": m28_g2,
            "M28_G3_innexin_rate_preserved": m28_g3,
            "M28_G4_bin_direction": m28_g4,
        },
        "recorded_reference": {
            "cross_bins": {"a": 0.52, "b": 0.432, "c": 0.269, "d": 0.266},
            "exp31_cross_a": 1.00,
        },
        "prediction_rule": (
            "unchanged from exp27: abnormal iff pattern_error >= 6.0 mV OR "
            "head_likeness(tail) >= 0.7"),
        "notes": (
            "The scan is the calibration instrument (exp26 precedent): the "
            "qualifying phi_readout is the M28 adopted mapping candidate; "
            "the residual per-bin undershoot (recorded 0.43/0.27/0.27 vs "
            "sim 0.00) is expected to persist and is the penetrance-"
            "dampening residual, recorded not hidden."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
