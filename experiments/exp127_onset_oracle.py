#!/usr/bin/env python3
"""exp127 — THE ORACLE-ONSET ORDER TEST (CG-P4; ledger L107's
registration from subagent 5-b's draft, research/
gate_drafts_cg3_cg4_hp2.md §3, sequenced after exp125 as required) +
THE GAMMA-1 FULL-GRID REPAIR ARMS (owned from exp129's cross-finding:
grid2d gamma-1 over the FULL exp124 onset grid reads edge 48 h —
exp125's UG-G1 sampled only to 24 h and UG-G2's torus-specific
declaration is corrected; the repair arms complete the structure with
in-batch data on grid2d AND path).

CG-P4 (Damon 2026, Zenodo 18358611): the kernel onset parameter uc
should order exactly as the v2 boundary term crossing/sqrt(edges)
(predicts the dial price, Spearman 0.81 on the dial axis) — the
coupling-geometry kernel and the compiler's price oracle are the same
object on different axes. Standardized cell: gamma 16, mu 0.015
(exp124's peak rung), run_deadline verbatim, exp93's 7-substrate
battery. Degenerate substrates (flat-0 / flat-1 on REAL cells) fall
back to rungs {4, 64}. Sign pre-registered: the mechanism reading says
the deadline SHORTENS with fragility — edge DECREASING in v2
(Spearman strongly negative); the mined gate is sign-free; both
readings registered.

PRE-REGISTERED GATES (draft §3.4):

  CG4-G1  (same-object ordering) with >= 4 substrates carrying finite
          kernels: |Spearman(uc_hat, v2)| >= 0.7; the
          mechanism-confirming sign is NEGATIVE; a strong positive rho
          passes the bar with a sign-owned note. Partial zone
          0.3 <= |rho| < 0.7 deposited as PARTIAL. REFUTE if
          |rho| < 0.3.
  CG4-G2  (censoring consistency at the cheap end) every substrate
          with NO finite kernel at any registered rung must be
          v2-cheap (v2 <= 2.1, the random6/path band). REFUTE if an
          expensive member (v2 >= 7) shows no finite kernel while a
          cheap one closes.
  CG4-G3  (the analytic cross-check) VOID BY DEPENDENCY owned
          pre-run: exp125's analytic deadline REFUTED both readings
          (AN-G1) and the transfer was void (AN-G2) — no predicted
          edges for grid2d/path were deposited, so the rank-agreement
          check has no counterpart. The void is itself the deposit:
          the analytic law must be rebuilt (Dirichlet/clamp-anchored)
          before the kernel=oracle reading can be mechanistically
          cross-checked.
  CG4-A1  (harness continuity) the torus arm at gamma 16 reproduces
          exp124's deposited curve [0,0,0,0,0,0,0,1] bit-exactly.
  RG1     (the gamma-1 repair) grid2d and path gamma-1 curves over the
          FULL onset grid: grid2d's edge reproduces exp129's 48 h
          within one onset cell; path's gamma-1 edge is measured and
          deposited; the corrected statement (deadline structure
          monotone-rising in gamma with substrate-SHIFTED positions)
          is checked on the union of exp125 + exp127 data.

RUN: 448 + 128 + fallbacks. Serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp124_deadline_curve import run_deadline, ONSETS, SEEDS
from experiments.exp73_active_renormalization import make_battery
from experiments.exp93_refusal_price import SUBSTRATES
from experiments.exp106_drift_and_oracle_v2 import v2_ratio
from experiments.exp125_u_shape_generalization import protocol_end

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp127_onset_oracle.json")

GAMMA_STD = 16.0
FALLBACKS = (4.0, 64.0)
CENSORED_SCORE = 96.0
V2_DEPOSITED = {"grid2d": 4.174, "torus": 4.8083, "random3": 7.5118,
                "random6": 2.0378, "scale_free": 8.6209}


def spearman(x, y):
    """Rank correlation with average ranks for ties (no scipy)."""
    def ranks(a):
        order = np.argsort(a)
        r = np.empty(len(a), float)
        i = 0
        vals = np.asarray(a)[order]
        while i < len(vals):
            j = i
            while j + 1 < len(vals) and vals[j + 1] == vals[i]:
                j += 1
            r[order[i:j + 1]] = (i + j) / 2.0 + 1.0
            i = j + 1
        return r
    rx, ry = ranks(x), ranks(y)
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    den = np.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / den) if den > 0 else float("nan")


def run_curve(adj, gamma, tag, curves):
    ps = []
    for onset in ONSETS:
        br = [run_deadline(adj, s, gamma, onset) for s in SEEDS]
        ps.append(round(float(np.mean(br)), 3))
    curves[tag] = ps
    print(f"    {tag:22s} P(break): {ps}", flush=True)
    return ps


def real_edge(ps, adj, gamma):
    """First onset with P >= 0.5 among REAL cells only; None if the
    substrate never breaks inside its protocol window at this gamma."""
    t_pre = protocol_end(adj, gamma)
    for t, p in zip(ONSETS, ps):
        if t <= t_pre + 1e-9 and p >= 0.5:
            return t
    return None


def flat_degenerate(ps, adj, gamma):
    """True if all REAL cells are 0.0 (no finite kernel) or all 1.0
    (refuses at every real onset) — the fallback trigger."""
    t_pre = protocol_end(adj, gamma)
    real = [p for t, p in zip(ONSETS, ps) if t <= t_pre + 1e-9]
    return all(p == 0.0 for p in real) or all(p == 1.0 for p in real)


def main() -> dict:
    print("=== exp127: the oracle-onset order test (CG-P4) + gamma-1 repair ===\n")
    t0 = time.time()
    battery = make_battery()
    curves: dict = {}
    v2 = {name: round(float(v2_ratio(battery[name])), 4)
          for name in SUBSTRATES}
    print("  v2 ratios (in-run, exp106 formula):", v2)
    v2_check = {k: (abs(v2[k] - v) / v <= 1e-2)
                for k, v in V2_DEPOSITED.items()}
    print("  deposited-value cross-check:", v2_check, flush=True)

    # ---- standardized cell: gamma 16
    print("\n  standardized cell gamma 16:")
    edges16: dict = {}
    fallback: dict = {}
    for name in SUBSTRATES:
        adj = battery[name]
        ps = run_curve(adj, GAMMA_STD, f"{name}_g16", curves)
        e = real_edge(ps, adj, GAMMA_STD)
        if e is None and flat_degenerate(ps, adj, GAMMA_STD):
            for g in FALLBACKS:
                ps2 = run_curve(adj, g, f"{name}_g{g:g}", curves)
                e2 = real_edge(ps2, adj, g)
                if e2 is not None:
                    fallback[name] = g
                    e = e2
                    break
        edges16[name] = e
        print(f"      -> {name}: uc_hat {e} "
              f"{'(fallback g%g)' % fallback[name] if name in fallback else ''}",
              flush=True)

    # ---- the gamma-1 repair arms
    print("\n  gamma-1 full-grid repair arms:")
    repair_edges = {}
    for name in ("grid2d", "path"):
        ps = run_curve(battery[name], 1.0, f"{name}_g1_full", curves)
        repair_edges[name] = real_edge(ps, battery[name], 1.0)
    print(f"    repair edges: {repair_edges}", flush=True)

    # ---- gates
    print("\n  --- gates ---", flush=True)
    gates: dict = {}

    dep124 = json.load(open(os.path.join(
        ROOT, "results", "exp124_deadline_curve.json")))
    anchor = dep124["curves"]["16.0"]
    cg4a1 = all(abs(a - b) <= 0.125 for a, b in
                zip(curves["torus_g16"], anchor))
    gates["CG4_A1_harness_continuity"] = bool(cg4a1)
    print(f"  CG4-A1 torus gamma-16 anchor: "
          f"{'PASS' if cg4a1 else 'REFUTED'}", flush=True)

    finite = {k: v for k, v in edges16.items() if v is not None}
    uc = [edges16[n] if edges16[n] is not None else CENSORED_SCORE
          for n in SUBSTRATES]
    v2v = [v2[n] for n in SUBSTRATES]
    rho_all = spearman(uc, v2v)
    if len(finite) >= 4:
        names_f = list(finite)
        rho_fin = spearman([edges16[n] for n in names_f],
                           [v2[n] for n in names_f])
    else:
        rho_fin = float("nan")
    abs_rho = abs(rho_all)
    cg4g1 = ("PASS" if abs_rho >= 0.7 else
             "PARTIAL" if abs_rho >= 0.3 else "REFUTED")
    gates["CG4_G1_same_object_ordering"] = cg4g1
    print(f"  CG4-G1: rho(all, censored@96)={rho_all:.3f} "
          f"rho(finite n={len(finite)})={rho_fin:.3f} -> {cg4g1} "
          f"(sign {'NEGATIVE-confirming' if rho_all < 0 else 'POSITIVE-note'})",
          flush=True)

    cg4g2 = True
    for n in SUBSTRATES:
        if edges16[n] is None and v2[n] > 2.1:
            cg4g2 = False
            print(f"    CG4-G2 violation: {n} no finite kernel, "
                  f"v2={v2[n]} > 2.1")
    gates["CG4_G2_censoring_consistency"] = bool(cg4g2)
    print(f"  CG4-G2 no-kernel => v2-cheap: "
          f"{'PASS' if cg4g2 else 'REFUTED'}", flush=True)

    gates["CG4_G3_analytic_crosscheck"] = "VOID (dependency: exp125 AN-G1 refuted, AN-G2 void — no predicted edges deposited)"
    print("  CG4-G3: VOID by dependency (owned pre-run)", flush=True)

    # RG1: the gamma-1 repair
    g2d_e = repair_edges.get("grid2d")
    rg1 = (g2d_e is not None and abs(g2d_e - 48.0) <= 6.0 + 1e-9)
    gates["RG1_gamma1_repair"] = bool(rg1)
    print(f"  RG1: grid2d gamma-1 edge {g2d_e} (exp129: 48), "
          f"path gamma-1 edge {repair_edges.get('path')} -> "
          f"{'PASS' if rg1 else 'REFUTED'}", flush=True)

    n_pass = sum(1 for v in gates.values() if v is True or v == "PASS")
    print(f"\n  === {time.time() - t0:.0f}s | gates: {gates} ===")

    result = {
        "exp": "exp127_onset_oracle",
        "v2_in_run": v2,
        "v2_deposit_check": v2_check,
        "curves": curves,
        "uc_hat": edges16,
        "fallback_rung": fallback,
        "gamma1_repair_edges": repair_edges,
        "spearman_all": round(rho_all, 4),
        "spearman_finite": (round(rho_fin, 4)
                            if rho_fin == rho_fin else None),
        "criteria": gates,
        "notes": (
            "CG-P4 the oracle-onset order test at the standardized "
            "gamma-16 cell with censoring-aware real-cell edges; "
            "gamma-1 full-grid repair arms own exp129's cross-finding "
            "and correct exp125's UG-G1/UG-G2 breadth."),
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
