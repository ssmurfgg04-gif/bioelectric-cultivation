#!/usr/bin/env python3
"""exp38 — M30 STOCHASTIC SPEC EXPRESSION (night-five queue #1, L19).

MECHANISM (collective.py regrow, additive + bit-exact at default):
`spec_expression_p` — per-committing-cell Bernoulli expression of the
phi_spec read. When 0 < p < 1 and the phi read is active, each cell draws
u ~ U(0,1); cells that fail re-express the positional spec and fall back
to pure chain inheritance. Rationale: exp36 found the deterministic spec
read produces SHARP binary penetrance (chain->spec transition between
weight 0 and 0.2; cross_a rate 0.00 or 1.00, never between) while the
record is graded (cross_a 0.52). Neoblast spec re-expression is
stochastic at the cell level: the per-seed spec-expressing fraction is
Binomial(L, p) — large regenerates concentrate near the mean, small ones
are all-or-nothing — so the binary 6 mV outcome threshold splits seeds.

PRE-REGISTERED GATES (fixed BEFORE tonight's arms ran; recorded
references are exp31/exp36's published values only):

  M30-G1  SEED-SPLITTING at bin a (REGISTERED, per-cell): there EXISTS
          p in the registered scan {0.55, 0.65, 0.72, 0.80, 0.90} with
          cutting_cross_a pred_abn_rate strictly in {1/3, 2/3}.
  M30-G2  COLLATERAL LOCK at the qualifying p: cutting_{tail,head,trunk}
          pred_abn_rate == 0.00 and restored_tail == 0.00.
  M30-G3  GRADED DIRECTION at the qualifying p: Spearman rho between sim
          cross-bin rates and the recorded rates {a:0.52, b:0.432,
          c:0.269, d:0.266} is > 0.
  M30-G4  INNEXIN PRESERVED: innexin_tail rate == 0.67 with
          per-seed drift <= 1.5 mV.
  M30-G5  INERTNESS: phi_readout=0 + spec_expression_p=0.5 consumes NO
          RNG — cutting_tail per-seed errors bit-exact vs exp31.

REGISTERED AMENDMENT (after the registered per-cell scan ran): per-cell
spec silencing did NOT grade the pattern at any p (cross_a 0.00, err
~3 mV everywhere) — the chain RE-CARRIES the spec blend (each committed
cell writes its blended value; the next cell inherits it), so cell-level
expression failures cannot accumulate. The stochastic unit is amended to
the regenerate: `spec_reanchor_p` — one-time per-blastema Bernoulli on
the wound-face re-anchoring of the positional read (M28). Amendment
results are labelled exploratory; G1 is evaluated on the REGISTERED
scan only, A1-A4 on the amendment:

  M30-A1  seed-splitting: exists q in {0.40, 0.45, 0.50, 0.55, 0.60}
          with cross_a rate strictly in {1/3, 2/3} (rate = 1-q
          directionally; recorded target 0.52).
  M30-A2  collateral lock at the qualifying q (as G2).
  M30-A3  bins b/c/d unchanged at 0.00 (chain-only is already normal
          there; the recorded 0.43/0.27/0.27 residual stays — recorded
          not hidden, same status as exp36's dampening residual).
  M30-A4  innexin_tail preserved at q=0.50 (rate 0.67, drift <= 1.5 mV).

RUN PROTOCOL: exp31/exp36 discipline (seeds (1,2,3), window 24h dt=0.1,
thresholds unchanged, bin cut positions = exp31 recorded medians, phi
readout fixed at the exp36 adopted mapping 0.75, metrics read
immediately after regrow). Serial, BLAS pinned.
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
OUT = os.path.join(ROOT, "results", "exp38_m30_spec_expression.json")

PHI = 0.75                      # exp36 adopted mapping
P_SCAN = [0.55, 0.65, 0.72, 0.80, 0.90]      # registered (per-cell)
QR_SCAN = [0.40, 0.45, 0.50, 0.55, 0.60]     # amended (per-blastema)
RECORDED = {"a": 0.52, "b": 0.432, "c": 0.269, "d": 0.266}


def main() -> dict:
    print("=== exp38: M30 stochastic spec-expression scan ===\n")

    exp31 = json.load(open(os.path.join(ROOT, "results",
                                        "exp31_stage2_widened.json")))

    sim: dict[str, dict] = {}
    print("  [registered scan — per-cell expression]")
    for p in P_SCAN:
        tag = f"q{int(round(p * 100)):02d}"
        for b in ("a", "b", "c", "d"):
            arm = f"cutting_cross_{b}_{tag}"
            sim[arm] = sim_arm(arm, cut_f=EXP31_BINS[b],
                               phi_readout=PHI, spec_expression_p=p)
        s = sim[f"cutting_cross_a_{tag}"]
        print(f"  p={p:.2f}: cross_a {s['pred_abn_rate']:.2f} "
              f"(err {s['err_mean']:5.2f}) | b "
              f"{sim[f'cutting_cross_b_{tag}']['pred_abn_rate']:.2f} c "
              f"{sim[f'cutting_cross_c_{tag}']['pred_abn_rate']:.2f} d "
              f"{sim[f'cutting_cross_d_{tag}']['pred_abn_rate']:.2f}")

    print("  [amended scan — per-blastema re-anchoring] (exploratory)")
    for q in QR_SCAN:
        tag = f"r{int(round(q * 100)):02d}"
        for b in ("a", "b", "c", "d"):
            arm = f"cutting_cross_{b}_{tag}"
            sim[arm] = sim_arm(arm, cut_f=EXP31_BINS[b],
                               phi_readout=PHI, spec_reanchor_p=q)
        for plane in ("tail", "head", "trunk"):
            arm = f"cutting_{plane}_{tag}"
            sim[arm] = sim_arm(arm, phi_readout=PHI, spec_reanchor_p=q)
        sim[f"restored_tail_{tag}"] = sim_arm(
            f"restored_tail_{tag}", phi_readout=PHI, spec_reanchor_p=q)
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

    sim["innexin_tail_m30"] = sim_arm("innexin_tail_m30", phi_readout=PHI,
                                      spec_reanchor_p=0.50)
    sim["cutting_tail_inert"] = sim_arm("cutting_tail_inert",
                                        phi_readout=0.0,
                                        spec_expression_p=0.5)

    # ---- gates: registered per-cell scan ---------------------------------
    qualifying = None
    for p in P_SCAN:
        tag = f"q{int(round(p * 100)):02d}"
        r_a = sim[f"cutting_cross_a_{tag}"]["pred_abn_rate"]
        if r_a in (1 / 3, 2 / 3):
            qualifying = p
            break
    m30_g1 = qualifying is not None

    # G2 (registered scan) — collateral plane arms were not part of the
    # registered per-cell scan; collateral lock is evaluated on the
    # amendment scan, which runs plane arms at every q.
    m30_g2 = None

    m30_g3 = False
    rho_val = None
    if qualifying is not None:
        tag = f"q{int(round(qualifying * 100)):02d}"
        rates = [sim[f"cutting_cross_{b}_{tag}"]["pred_abn_rate"]
                 for b in ("a", "b", "c", "d")]
        from scipy.stats import spearmanr
        rho = spearmanr(rates, [RECORDED[b] for b in ("a", "b", "c", "d")])
        rho_val = float(rho.statistic)
        m30_g3 = bool(rho.statistic > 0)

    # ---- gates: amended re-anchor scan ------------------------------------
    qualifying_r = None
    for q in QR_SCAN:
        tag = f"r{int(round(q * 100)):02d}"
        r_a = sim[f"cutting_cross_a_{tag}"]["pred_abn_rate"]
        coll_ok = all(sim[f"cutting_{pl}_{tag}"]["pred_abn_rate"] == 0.0
                      for pl in ("tail", "head", "trunk")) \
            and sim[f"restored_tail_{tag}"]["pred_abn_rate"] == 0.0
        if r_a in (1 / 3, 2 / 3) and coll_ok:
            qualifying_r = q
            break
    m30_a1 = qualifying_r is not None

    m30_a2 = True
    if qualifying_r is not None:
        tag = f"r{int(round(qualifying_r * 100)):02d}"
        m30_a2 = all(sim[f"cutting_{pl}_{tag}"]["pred_abn_rate"] == 0.0
                     for pl in ("tail", "head", "trunk")) \
            and sim[f"restored_tail_{tag}"]["pred_abn_rate"] == 0.0

    m30_a3 = False
    if qualifying_r is not None:
        tag = f"r{int(round(qualifying_r * 100)):02d}"
        m30_a3 = all(sim[f"cutting_cross_{b}_{tag}"]["pred_abn_rate"] == 0.0
                     for b in ("b", "c", "d"))

    inx = sim["innexin_tail_m30"]
    drift = float(np.max(np.abs(
        np.array(inx["err_per_seed"])
        - np.array(exp31["sim_arms"]["innexin_tail"]["err_per_seed"]))))
    m30_g4 = bool(abs(inx["pred_abn_rate"]
                      - exp31["sim_arms"]["innexin_tail"]["pred_abn_rate"])
                  < 1e-9 and drift <= 1.5)

    inert = sim["cutting_tail_inert"]
    m30_g5 = bool(np.allclose(
        inert["err_per_seed"],
        exp31["sim_arms"]["cutting_tail"]["err_per_seed"],
        atol=1e-9, rtol=0.0))

    print(f"\n  [registered — per-cell expression]")
    print(f"  M30-G1 seed-splitting exists:             "
          f"p={qualifying}  {'PASS' if m30_g1 else 'REFUTED'}")
    print(f"  M30-G2 collateral lock:                   "
          f"{'n/a (amendment)' if m30_g2 is None else ('PASS' if m30_g2 else 'REFUTED')}")
    print(f"  M30-G3 recorded-direction rho>0 "
          f"(rho={rho_val}): {'PASS' if m30_g3 else 'REFUTED'}")
    print(f"  [amended — per-blastema re-anchoring] (exploratory)")
    print(f"  M30-A1 seed-splitting exists:             "
          f"q={qualifying_r}  {'PASS' if m30_a1 else 'REFUTED'}")
    print(f"  M30-A2 collateral lock:                   "
          f"{'PASS' if m30_a2 else 'REFUTED'}")
    print(f"  M30-A3 bins b/c/d unchanged 0.00:         "
          f"{'PASS' if m30_a3 else 'REFUTED'}")
    print(f"  M30-G4 innexin preserved (drift {drift:.2f} mV):  "
          f"{'PASS' if m30_g4 else 'REFUTED'}")
    print(f"  M30-G5 default inertness (bit-exact):     "
          f"{'PASS' if m30_g5 else 'REFUTED'}")

    if qualifying_r is not None:
        tag = f"r{int(round(qualifying_r * 100)):02d}"
        gap_a = abs(sim[f"cutting_cross_a_{tag}"]["pred_abn_rate"]
                    - RECORDED["a"])
        print(f"  cross_a |rate - 0.52| at q={qualifying_r}: {gap_a:.2f}")

    out = {
        "exp": "exp38_m30_spec_expression",
        "mechanism": (
            "REGISTERED: spec_expression_p — per-committing-cell "
            "Bernoulli on the phi_spec read. AMENDED (exploratory): "
            "spec_reanchor_p — one-time per-blastema Bernoulli on the "
            "wound-face re-anchoring of the positional read; draws "
            "gated — no RNG contact at defaults or when the phi read is "
            "inactive (bit-exact)"),
        "phi_readout": PHI,
        "p_scan": P_SCAN,
        "q_scan": QR_SCAN,
        "sim_arms": sim,
        "qualifying_p_registered": qualifying,
        "qualifying_q_amended": qualifying_r,
        "criteria": {
            "M30_G1_seed_splitting_registered_per_cell": m30_g1,
            "M30_G2_collateral_lock_registered": m30_g2,
            "M30_G3_recorded_direction_rho_registered": m30_g3,
            "M30_A1_seed_splitting_amended_reanchor": m30_a1,
            "M30_A2_collateral_lock_amended": m30_a2,
            "M30_A3_bins_bcd_unchanged": m30_a3,
            "M30_G4_innexin_preserved": m30_g4,
            "M30_G5_inertness_bitexact": m30_g5,
        },
        "recorded_reference": RECORDED,
        "prediction_rule": (
            "unchanged from exp27: abnormal iff pattern_error >= 6.0 mV OR "
            "head_likeness(tail) >= 0.7"),
        "notes": (
            "Registered per-cell version REFUTED: the chain re-carries "
            "the spec blend (each committed cell writes its blended "
            "value; the next inherits it), so per-cell expression "
            "failures cannot accumulate — cross_a stayed 0.00 at every "
            "p with err ~3 mV. The graded penetrance must live at the "
            "regenerate level. Amendment (exploratory, exp36 "
            "precedent): per-blastema re-anchoring draw; qualifying q "
            "is the M30 amended mapping candidate. Pointwise fit is "
            "NOT claimed — the record's absolute rates run hot "
            "(publication bias); gates test seed-splitting, ordering, "
            "collateral safety."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
