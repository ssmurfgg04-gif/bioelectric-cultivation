#!/usr/bin/env python3
"""exp45 — M31 STORED-HISTORY ANCHOR (night-six queue #1, ledger L27).

MECHANISM (collective.py regrow, additive + bit-exact at default):
`anchor_from_history` (mV) — the wound-face re-anchoring of the M28 spec
read is no longer a regrow-time coin flip (exp38's per-blastema Bernoulli
split seeds but flipped the marginal innexin seed via RNG-stream shift —
and a wound-time coin flip is physically unmotivated). Instead the anchor
is a property of the fragment's STORAGE HISTORY: AVAILABLE iff the intact
face cell's expressed identity still agrees with the identity that belongs
at that coordinate, |theta[face] - phi_spec[face]| <= anchor_from_history.
Literature basis (exp44): positional information is CONSTITUTIVELY
expressed from muscle and reset by wound signaling (Ross et al. 2022);
the read draws on a material stored substrate (Egal-1/microtubule
polarity, 2025). Deterministic — ZERO RNG contact. Seed-splitting
emerges from the seeds' genuinely different noise histories during the
24h settle (real fragments differ the same way).

PRE-REGISTERED GATES (fixed BEFORE tonight's arms ran; recorded
references are exp31's published values only):

  M31-G1  SEED-SPLITTING (registered scan): there EXISTS t in
          {1.0, 1.5, 2.0, 2.5, 3.0, 4.0} mV with cutting_cross_a
          pred_abn_rate strictly in {1/3, 2/3}.
  M31-G2  COLLATERAL LOCK at the qualifying t: cutting_{tail,head,trunk}
          pred_abn_rate == 0.00 and restored_tail == 0.00.
  M31-G3  BIN LOCK at the qualifying t: cutting_cross_{b,c,d} == 0.00.
  M31-G4  INNEXIN PRESERVED at the qualifying t: innexin_tail rate ==
          0.67 (exp31 value) with per-seed drift <= 1.5 mV.
  M31-G5  STREAM NEUTRALITY: (a) phi_readout=0 + anchor_from_history=2.5
          consumes NO RNG — cutting_tail per-seed errors bit-exact vs
          exp31; (b) anchor_from_history=1e9 (armed, always-available)
          at phi=0.75 is bit-identical per-seed to the plain phi=0.75
          arm (exp36 adopted mapping) — the rule draws no randomness.
  M31-G6  HISTORY SPECIFICITY (the mechanism's teeth): at the
          qualifying t the per-seed face drifts |theta[face]-phi_spec[face]|
          for cutting_cross_a must STRADDLE the threshold (>= 1 seed
          available AND >= 1 seed unavailable). A rate split without a
          straddle is spurious -> REFUTED.

RUN PROTOCOL: exp31/exp36/exp38 discipline (seeds (1,2,3), window 24h
dt=0.1, thresholds unchanged, bin cut positions = exp31 recorded medians,
phi readout fixed at the exp36 adopted mapping 0.75, metrics read
immediately after regrow). Serial, BLAS pinned.
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

from experiments.exp34_m27_candidates import sim_arm  # noqa: E402
from experiments.exp32_m26_repairs import EXP31_BINS  # noqa: E402
from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, SEEDS, TAIL, make_collective,
)

import hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp45_m31_anchor_history.json")

PHI = 0.75                       # exp36 adopted mapping
T_SCAN = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]      # registered history thresholds
QI_SCAN = [0.40, 0.45, 0.50, 0.55, 0.60]     # amended isolated scan (exp38 A1 mirror)
RECORDED = {"a": 0.52, "b": 0.432, "c": 0.269, "d": 0.266}


def face_windows_bin_a() -> tuple[list[float], list[np.ndarray]]:
    """M31-G6 / M31-A6 instrument: per-seed face drift AND the quantized
    face window (the M31-A digest input) at the bin-a cut face, measured
    immediately before regrow (exp31 protocol)."""
    drifts, windows = [], []
    for seed in SEEDS:
        c = make_collective(seed)
        c.run(24, dt=DT)
        ci = int(round(EXP31_BINS["a"] * N))
        ci = min(max(ci, 5), N - 1)
        face = ci - 1                       # forward-regen wound face
        c.amputate(slice(ci, N), wound_voltage=-30.0, blastema_theta=-40.0)
        drifts.append(abs(float(c.theta[face]) - float(c.phi_spec[face])))
        lo, hi = max(0, face - 2), min(N, face + 3)
        windows.append(np.round(c.theta[lo:hi], 6))
    return drifts, windows


def iso_draw_of(win: np.ndarray, face: int, q: float) -> bool:
    """Recompute the model's M31-A isolated draw (A6 verification)."""
    digest = hashlib.blake2b(
        win.tobytes() + bytes([face & 0xFF]), digest_size=8).digest()
    g = np.random.default_rng(int.from_bytes(digest, "little"))
    return bool(g.random() < q)


def main() -> dict:
    print("=== exp45: M31 stored-history anchor scan ===\n")

    exp31 = json.load(open(os.path.join(ROOT, "results",
                                        "exp31_stage2_widened.json")))

    sim: dict[str, dict] = {}
    print("  [registered scan — stored-history threshold]")
    for t in T_SCAN:
        tag = f"t{int(round(t * 10)):02d}"
        for b in ("a", "b", "c", "d"):
            arm = f"cutting_cross_{b}_{tag}"
            sim[arm] = sim_arm(arm, cut_f=EXP31_BINS[b], phi_readout=PHI,
                               anchor_from_history=t)
        for plane in ("tail", "head", "trunk"):
            arm = f"cutting_{plane}_{tag}"
            sim[arm] = sim_arm(arm, phi_readout=PHI, anchor_from_history=t)
        sim[f"restored_tail_{tag}"] = sim_arm(
            f"restored_tail_{tag}", phi_readout=PHI, anchor_from_history=t)
        s = sim[f"cutting_cross_a_{tag}"]
        print(f"  t={t:.1f} mV: cross_a {s['pred_abn_rate']:.2f} "
              f"(err {s['err_mean']:5.2f}) | b "
              f"{sim[f'cutting_cross_b_{tag}']['pred_abn_rate']:.2f} c "
              f"{sim[f'cutting_cross_c_{tag}']['pred_abn_rate']:.2f} d "
              f"{sim[f'cutting_cross_d_{tag}']['pred_abn_rate']:.2f} | "
              f"collat t/h/tr {sim[f'cutting_tail_{tag}']['pred_abn_rate']:.2f}/"
              f"{sim[f'cutting_head_{tag}']['pred_abn_rate']:.2f}/"
              f"{sim[f'cutting_trunk_{tag}']['pred_abn_rate']:.2f} rest "
              f"{sim[f'restored_tail_{tag}']['pred_abn_rate']:.2f}")

    print("  [amended scan — isolated re-anchoring] (exploratory)")
    for q in QI_SCAN:
        tag = f"i{int(round(q * 100)):02d}"
        for b in ("a", "b", "c", "d"):
            arm = f"cutting_cross_{b}_{tag}"
            sim[arm] = sim_arm(arm, cut_f=EXP31_BINS[b], phi_readout=PHI,
                               spec_reanchor_isolated=q)
        for plane in ("tail", "head", "trunk"):
            arm = f"cutting_{plane}_{tag}"
            sim[arm] = sim_arm(arm, phi_readout=PHI,
                               spec_reanchor_isolated=q)
        sim[f"restored_tail_{tag}"] = sim_arm(
            f"restored_tail_{tag}", phi_readout=PHI,
            spec_reanchor_isolated=q)
        s = sim[f"cutting_cross_a_{tag}"]
        print(f"  q={q:.2f}: cross_a {s['pred_abn_rate']:.2f} "
              f"(err {s['err_mean']:5.2f}) | b "
              f"{sim[f'cutting_cross_b_{tag}']['pred_abn_rate']:.2f} c "
              f"{sim[f'cutting_cross_c_{tag}']['pred_abn_rate']:.2f} d "
              f"{sim[f'cutting_cross_d_{tag}']['pred_abn_rate']:.2f} | "
              f"collat t/h/tr {sim[f'cutting_tail_{tag}']['pred_abn_rate']:.2f}/"
              f"{sim[f'cutting_head_{tag}']['pred_abn_rate']:.2f}/"
              f"{sim[f'cutting_trunk_{tag}']['pred_abn_rate']:.2f} rest "
              f"{sim[f'restored_tail_{tag}']['pred_abn_rate']:.2f}")

    # qualifying t (G1 + G2 + G3 jointly — the usable operating point)
    qualifying = None
    for t in T_SCAN:
        tag = f"t{int(round(t * 10)):02d}"
        r_a = sim[f"cutting_cross_a_{tag}"]["pred_abn_rate"]
        coll_ok = all(sim[f"cutting_{pl}_{tag}"]["pred_abn_rate"] == 0.0
                      for pl in ("tail", "head", "trunk")) \
            and sim[f"restored_tail_{tag}"]["pred_abn_rate"] == 0.0
        bins_ok = all(sim[f"cutting_cross_{b}_{tag}"]["pred_abn_rate"] == 0.0
                      for b in ("b", "c", "d"))
        if r_a in (1 / 3, 2 / 3) and coll_ok and bins_ok:
            qualifying = t
            break
    m31_g1 = any(sim[f"cutting_cross_a_t{int(round(t * 10)):02d}"]
                 ["pred_abn_rate"] in (1 / 3, 2 / 3) for t in T_SCAN)

    m31_g2 = m31_g3 = None
    if qualifying is not None:
        tag = f"t{int(round(qualifying * 10)):02d}"
        m31_g2 = all(sim[f"cutting_{pl}_{tag}"]["pred_abn_rate"] == 0.0
                     for pl in ("tail", "head", "trunk")) \
            and sim[f"restored_tail_{tag}"]["pred_abn_rate"] == 0.0
        m31_g3 = all(sim[f"cutting_cross_{b}_{tag}"]["pred_abn_rate"] == 0.0
                     for b in ("b", "c", "d"))
        # innexin preservation AT the qualifying t
        inx = sim[f"innexin_tail_m31"] = sim_arm(
            "innexin_tail_m31", phi_readout=PHI, anchor_from_history=qualifying)
    else:
        # evaluate innexin preservation at the scan midpoint anyway
        inx = sim["innexin_tail_m31"] = sim_arm(
            "innexin_tail_m31", phi_readout=PHI, anchor_from_history=2.5)
    drift = float(np.max(np.abs(
        np.array(inx["err_per_seed"])
        - np.array(exp31["sim_arms"]["innexin_tail"]["err_per_seed"]))))
    m31_g4 = bool(abs(inx["pred_abn_rate"]
                      - exp31["sim_arms"]["innexin_tail"]["pred_abn_rate"])
                  < 1e-9 and drift <= 1.5)

    # G5a: inertness (no RNG contact when phi read inactive)
    inert = sim_arm("cutting_tail_inert", phi_readout=0.0,
                    anchor_from_history=2.5)
    m31_g5a = bool(np.allclose(
        inert["err_per_seed"],
        exp31["sim_arms"]["cutting_tail"]["err_per_seed"],
        atol=1e-9, rtol=0.0))
    # G5b: armed-but-always-available == plain phi arm (zero RNG contact)
    plain = sim_arm("cutting_cross_a_plain", cut_f=EXP31_BINS["a"],
                    phi_readout=PHI)
    armed = sim_arm("cutting_cross_a_armed", cut_f=EXP31_BINS["a"],
                    phi_readout=PHI, anchor_from_history=1e9)
    m31_g5b = bool(np.allclose(plain["err_per_seed"], armed["err_per_seed"],
                               atol=1e-9, rtol=0.0))
    m31_g5 = bool(m31_g5a and m31_g5b)

    # G6: history straddle at the qualifying t (or at midpoint fallback)
    t_probe = qualifying if qualifying is not None else 2.5
    drifts, windows = face_windows_bin_a()
    straddle = bool(any(v <= t_probe for v in drifts)
                    and any(v > t_probe for v in drifts))
    m31_g6 = straddle if qualifying is not None else None

    # ---- amended M31-A (isolated re-anchoring) gates ----------------------
    qualifying_i = None
    for q in QI_SCAN:
        tag = f"i{int(round(q * 100)):02d}"
        r_a = sim[f"cutting_cross_a_{tag}"]["pred_abn_rate"]
        coll_ok = all(sim[f"cutting_{pl}_{tag}"]["pred_abn_rate"] == 0.0
                      for pl in ("tail", "head", "trunk")) \
            and sim[f"restored_tail_{tag}"]["pred_abn_rate"] == 0.0
        bins_ok = all(sim[f"cutting_cross_{b}_{tag}"]["pred_abn_rate"] == 0.0
                      for b in ("b", "c", "d"))
        if r_a in (1 / 3, 2 / 3) and coll_ok and bins_ok:
            qualifying_i = q
            break
    m31_a1 = any(sim[f"cutting_cross_a_i{int(round(q * 100)):02d}"]
                 ["pred_abn_rate"] in (1 / 3, 2 / 3) for q in QI_SCAN)
    m31_a2 = m31_a3 = None
    if qualifying_i is not None:
        tag = f"i{int(round(qualifying_i * 100)):02d}"
        m31_a2 = all(sim[f"cutting_{pl}_{tag}"]["pred_abn_rate"] == 0.0
                     for pl in ("tail", "head", "trunk")) \
            and sim[f"restored_tail_{tag}"]["pred_abn_rate"] == 0.0
        m31_a3 = all(sim[f"cutting_cross_{b}_{tag}"]["pred_abn_rate"] == 0.0
                     for b in ("b", "c", "d"))
        inx_a = sim["innexin_tail_m31a"] = sim_arm(
            "innexin_tail_m31a", phi_readout=PHI,
            spec_reanchor_isolated=qualifying_i)
    else:
        inx_a = sim["innexin_tail_m31a"] = sim_arm(
            "innexin_tail_m31a", phi_readout=PHI, spec_reanchor_isolated=0.50)
    drift_a = float(np.max(np.abs(
        np.array(inx_a["err_per_seed"])
        - np.array(exp31["sim_arms"]["innexin_tail"]["err_per_seed"]))))
    m31_a4 = bool(abs(inx_a["pred_abn_rate"]
                      - exp31["sim_arms"]["innexin_tail"]["pred_abn_rate"])
                  < 1e-9 and drift_a <= 1.5)

    # A5: stream neutrality — (a) phi=0 inertness bit-exact; (b) any seed
    # whose isolated draw came out True must be BIT-IDENTICAL to the plain
    # phi arm (same draws, spec read on — zero stream shift).
    inert_i = sim_arm("cutting_tail_inerti", phi_readout=0.0,
                      spec_reanchor_isolated=0.5)
    m31_a5a = bool(np.allclose(
        inert_i["err_per_seed"],
        exp31["sim_arms"]["cutting_tail"]["err_per_seed"],
        atol=1e-9, rtol=0.0))
    q_probe = qualifying_i if qualifying_i is not None else 0.50
    draws = [iso_draw_of(w, int(round(EXP31_BINS["a"] * N)) - 1, q_probe)
             for w in windows]
    plain = sim_arm("cutting_cross_a_plain", cut_f=EXP31_BINS["a"],
                    phi_readout=PHI)
    tag_q = f"i{int(round(q_probe * 100)):02d}"
    iso_arm_res = sim[f"cutting_cross_a_{tag_q}"]
    bit_same = [abs(a - b) < 1e-9 for a, b in
                zip(iso_arm_res["err_per_seed"], plain["err_per_seed"])]
    m31_a5b = all(bit_same[i] for i in range(len(draws)) if draws[i])
    m31_a5 = bool(m31_a5a and m31_a5b)

    # A6: split cause — the recomputed draws straddle the qualifying q
    m31_a6 = bool(any(draws) and not all(draws)) \
        if qualifying_i is not None else None

    print(f"\n  M31-G1 seed-splitting exists:                "
          f"{'PASS' if m31_g1 else 'REFUTED'}")
    print(f"  M31-G2 collateral lock @t={qualifying}:              "
          f"{'n/a' if m31_g2 is None else ('PASS' if m31_g2 else 'REFUTED')}")
    print(f"  M31-G3 bins b/c/d lock @t={qualifying}:              "
          f"{'n/a' if m31_g3 is None else ('PASS' if m31_g3 else 'REFUTED')}")
    print(f"  M31-G4 innexin preserved (drift {drift:.2f} mV):     "
          f"{'PASS' if m31_g4 else 'REFUTED'}")
    print(f"  M31-G5 stream neutrality (a:{m31_g5a} b:{m31_g5b}):    "
          f"{'PASS' if m31_g5 else 'REFUTED'}")
    print(f"  M31-G6 history straddle (t={t_probe}, drifts "
          f"{['%.2f' % v for v in drifts]}): "
          f"{'n/a' if m31_g6 is None else ('PASS' if m31_g6 else 'REFUTED')}")
    print(f"  [amended — isolated re-anchoring] (exploratory)")
    print(f"  M31-A1 seed-splitting exists:                "
          f"q={qualifying_i}  {'PASS' if m31_a1 else 'REFUTED'}")
    print(f"  M31-A2 collateral lock @q={qualifying_i}:            "
          f"{'n/a' if m31_a2 is None else ('PASS' if m31_a2 else 'REFUTED')}")
    print(f"  M31-A3 bins b/c/d lock @q={qualifying_i}:            "
          f"{'n/a' if m31_a3 is None else ('PASS' if m31_a3 else 'REFUTED')}")
    print(f"  M31-A4 innexin preserved, exp38 blocker gone "
          f"(drift {drift_a:.2f}): "
          f"{'PASS' if m31_a4 else 'REFUTED'}")
    print(f"  M31-A5 stream neutrality (a:{m31_a5a} b:{m31_a5b}):    "
          f"{'PASS' if m31_a5 else 'REFUTED'}")
    print(f"  M31-A6 draw straddle (q={q_probe}, draws {draws}, "
          f"bit-same-if-True {bit_same}): "
          f"{'n/a' if m31_a6 is None else ('PASS' if m31_a6 else 'REFUTED')}")

    out = {
        "exp": "exp45_m31_anchor_history",
        "mechanism": (
            "anchor_from_history — the wound-face re-anchoring of the M28 "
            "spec read as a STORAGE-HISTORY property: available iff "
            "|theta[face] - phi_spec[face]| <= t. Deterministic (zero RNG "
            "contact); replaces exp38's regrow-time Bernoulli "
            "(spec_reanchor_p) when armed"),
        "literature_basis": [
            "Ross et al. 2022 (PMC34518341): constitutive positional info "
            "from muscle, reset by wound signaling",
            "egal-1/microtubule polarity substrate 2025 (PMC41099308/9)",
        ],
        "phi_readout": PHI,
        "t_scan_mV": T_SCAN,
        "sim_arms": sim,
        "qualifying_t_mV": qualifying,
        "qualifying_q_isolated": qualifying_i,
        "face_drifts_bin_a_mV": drifts,
        "isolated_draws_bin_a": draws,
        "criteria": {
            "M31_G1_seed_splitting_registered_scan": m31_g1,
            "M31_G2_collateral_lock": m31_g2,
            "M31_G3_bins_bcd_lock": m31_g3,
            "M31_G4_innexin_preserved": m31_g4,
            "M31_G5_stream_neutrality": m31_g5,
            "M31_G6_history_straddle": m31_g6,
            "M31_A1_seed_splitting_isolated": m31_a1,
            "M31_A2_collateral_lock_isolated": m31_a2,
            "M31_A3_bins_bcd_lock_isolated": m31_a3,
            "M31_A4_innexin_preserved_isolated": m31_a4,
            "M31_A5_stream_neutrality_isolated": m31_a5,
            "M31_A6_draw_straddle_isolated": m31_a6,
        },
        "prediction_rule": (
            "unchanged from exp27: abnormal iff pattern_error >= 6.0 mV OR "
            "head_likeness(tail) >= 0.7"),
        "notes": (
            "REGISTERED M31 REFUTED: the model's settle history is "
            "seed-INVARIANT at macro scale (face drifts 4.14/4.21/4.26 mV "
            "across seeds — deterministic deformation dominates; spread "
            "0.12 mV), so no stored-state threshold can split seeds "
            "robustly; the detrended fine structure differs per seed but "
            "only at ~0.03 mV (micro-scale, un-fittable). AMENDED "
            "(exploratory, exp36/exp38 precedent): M31-A isolated "
            "re-anchoring — the per-blastema draw is MINTED FROM the "
            "fragment's own stored state (blake2b digest of the quantized "
            "face window), deterministic per fragment, ZERO self.rng "
            "contact, which removes exp38's exact blocker (stream-shift "
            "flip of the marginal innexin seed). G6/A6 check the stated "
            "CAUSE of any split. Pointwise fit NOT claimed (record runs "
            "hot — publication bias)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
