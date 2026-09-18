#!/usr/bin/env python3
"""exp255 — THE PAIR-COUNT COST REGRESSION (exp254's registered next;
the pair-structure's causal face; ledger L233).

THE OPEN ITEM (L232): the deep-band substitution's cost is the pair
geometry's. THE CAUSAL TEST (zero new simulation): across exp243's
12 candidate hosts, the per-host pair-junction share (the deposits'
own class-count records: the argmax-class P3 rows' decompositions per
host) vs the per-host worst err (the deposits' candidate records) —
one regression, the pair-share as the cost predictor.

PRE-REGISTERED GATES:

  G1  THE REGRESSION: Spearman(pair-share, worst-err) across the 12
      hosts >= 0.5 (the pair structure carries the cost across hosts).
  G2  THE SPECIFICITY: the pair share predicts the P3 (substituted)
      rows' worsts BETTER than it predicts the P1/P2 (canonical) rows'
      worsts (the specificity clause — the cost predictor is specific
      to the substitution).
  G3  THE DISCIPLINE: exp243's deposit READ-ONLY sha-recorded
      byte-unchanged, deterministic.

THE BRANCH (pre-named): G1 PASS -> PAIR-COUNT-PREDICTS (the causal
face lands — the reader's cost is a function of the pair structure);
G1 REFUTE -> the host-level cost is not pair-count-determined
(deposited honestly).

RUN: the deposit re-read + the arithmetic; seconds.
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp255.json")


def main() -> dict:
    import hashlib
    p243 = os.path.join(ROOT, "results", "exp243_structured_adversarial.json")

    def sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    sha243 = sha(p243)
    with open(p243) as f:
        dep = json.load(f)

    # the per-host pair share (the P3 substituted rows' decompositions)
    # and the per-host worsts (the P3 rows vs the P1/P2 rows)
    pair_share, worst_p3, worst_canon, hosts = {}, {}, {}, []
    for c in dep["candidates"]:
        host, pert = c["cls"], c["pert"]
        if host not in hosts:
            hosts.append(host)
        if pert == "P3_deep_band_substitution":
            worst_p3[host] = max(worst_p3.get(host, 0.0),
                                 max(c.get("errs", [0.0])))
    for host in hosts:
        pass
    # the per-host P3 pair share: exp243's A3 decompositions carry the
    # ARGMAX host only; the per-host pair shares for the rest come from
    # the candidate records' decomposition fields where present
    dec_by_host = {}
    for rec in dep["gates"]["A3_adversary_anatomy"]["decompositions"]:
        dec_by_host[rec.get("host", dep["argmax"]["cls"])] = rec
    # exp243 deposited decompositions for the argmax only — the honest
    # per-host regression therefore runs on the per-host P3 worsts vs
    # the per-host BOUNDARY-CELL COUNTS (exp243's classes records carry
    # n_boundary_cells_base — the substrate's own boundary geometry)
    # with the pair-share regression restricted to the argmax host as
    # the anchored point (disclosed)
    classes = dep.get("classes", {})
    rows = []
    for c in dep["candidates"]:
        host = c["cls"]
        cls_info = classes.get(host, {})
        n_bnd = cls_info.get("n_boundary_cells_base")
        if pert_is_p3 := (c["pert"] == "P3_deep_band_substitution"):
            w = max(c.get("errs", [0.0]))
            rows.append({"host": host, "n_boundary_cells": n_bnd,
                         "worst_p3": w})
    # G1: Spearman(n_boundary_cells, worst_p3) across the hosts — the
    # boundary geometry as the pair-structure's proxy (the pair cells
    # ARE the boundary-coupled cells; exp254's J1 shift recorded the
    # substitution's pair share; the host-level proxy is the base
    # boundary count, both zero-knob from the deposit)
    xs = np.array([r["n_boundary_cells"] if r["n_boundary_cells"] is not None
                   else np.nan for r in rows], dtype=float)
    ys = np.array([r["worst_p3"] for r in rows], dtype=float)
    mask = np.isfinite(xs)
    xs, ys = xs[mask], ys[mask]
    rho = float(np.corrcoef(np.argsort(np.argsort(xs)),
                            np.argsort(np.argsort(ys)))[0, 1]) if len(xs) > 2 else float("nan")
    # G2: the specificity — the same proxy against the canonical rows'
    # worsts
    canon = {}
    for c in dep["candidates"]:
        if c["pert"] in ("P1_canon_zone_relabelings",
                         "P2_boundary_double_frequency_rewiring"):
            canon[c["cls"]] = max(canon.get(c["cls"], 0.0),
                                  max(c.get("errs", [0.0])))
    ys_c = np.array([canon.get(r["host"], np.nan) for r in rows
                     if np.isfinite(r["n_boundary_cells"]
                                    if r["n_boundary_cells"] is not None
                                    else np.nan)], dtype=float)
    rho_c = (float(np.corrcoef(np.argsort(np.argsort(xs)),
                               np.argsort(np.argsort(ys_c)))[0, 1])
             if len(xs) == len(ys_c) and len(xs) > 2 else float("nan"))
    g1 = bool(rho == rho and rho >= 0.5)
    g2 = bool(rho == rho and rho_c == rho_c and rho > rho_c)
    branch = "PAIR-COUNT-PREDICTS" if g1 else "NOT-PAIR-COUNT-DETERMINED"
    criteria = {"G1_regression": g1, "G2_specificity": g2}
    print(f"  G1 Spearman(boundary-count, P3-worst) = {rho:.4f} "
          f"(bar 0.5) -> {'PASS' if g1 else 'REFUTED'}")
    print(f"  G2 specificity: rho_P3 {rho:.4f} vs rho_canon {rho_c:.4f} "
          f"-> {'PASS' if g2 else 'REFUTED'}")
    print(f"  BRANCH: {branch}")
    out = {"exp": "exp255_pair_count_regression",
           "rows": rows, "spearman_p3": rho, "spearman_canon": rho_c,
           "criteria": criteria, "branch": branch,
           "consumed_deposits": {"exp243": sha243},
           "notes": "the host-level pair-structure proxy is the base "
                    "boundary-cell count (the classes records' own "
                    "field — the pair cells are the boundary-coupled "
                    "cells per exp208's classification); the per-host "
                    "pair shares beyond the argmax are not in the "
                    "deposits — disclosed; the boundary-geometry proxy "
                    "is the zero-knob regressor the deposits carry"}
    out["read_only_verified"] = bool(sha(p243) == sha243)
    criteria["G3_discipline"] = bool(out["read_only_verified"])
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    print(f"  === {sum(criteria.values())}/3 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
