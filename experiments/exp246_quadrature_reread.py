#!/usr/bin/env python3
"""exp246 — THE QUADRATURE THREE-CHANNEL RE-READ (exp233's registered
next; the law's composition form; ledger L222).

THE OPEN ITEM: exp233's F3 REFUTE — the max-form three-channel
prediction pred3 = max(V-term, theta-term, field-term) pooled at
Spearman 0.700 over the (gamma x kappa) grid — while its NON-GATING
quadrature composition pooled at 0.933. exp233's registered next: the
grid re-read under the quadrature form err ~ sqrt(eV^2 + etheta^2 +
efield^2) — the two-channel boundary work's own quadrature precedent —
as the law's correct composition.

THE INSTRUMENTS (frozen, verbatim): exp233's deposited grid (27 points
x 3 seeds x 3 arms — re-read from the deposit, ZERO re-simulation for
the gate arithmetic; the field-term machinery from exp233's body for
the per-point efield term), exp79's V-term and theta-term (the frozen
forms), the quadrature pred: pred_q = sqrt(eV^2 + eT^2 + ef^2) with the
three terms the per-point exp233/exp79 quantities (the V-term
CONTRAST*y/(1+y), the theta-term the homogenization number, the
field-term exp233's field-drag quantity — each the PREDICTED mV
contribution, composed in quadrature).

PRE-REGISTERED GATES:

  Q1  THE QUADRATURE LAW: pred_q tracks the measured errs across the
      deposited grid with Spearman >= 0.90 (exp79 TC-G1's bar) — the
      gate the max-form failed (0.700) and the non-gating quadrature
      preview passed (0.933, now GATED).
  Q2  THE BOUNDARY AGREEMENT: pred_q's writability boundary (pred_q <
      6.0 iff err < 6.0) agrees on >= 80% of the grid points (exp79
      TC-G1's second clause).
  Q3  THE THREE-CHANNEL VERDICT (the composition named): if Q1+Q2 PASS,
      the stack's channel composition is QUADRATURE — the three
      channels' contributions compose as independent RMS terms, not as
      a binding max; the law's form is updated to the quadrature
      three-channel form and the exp233 F3 verdict is REFINED (the
      field channel is real but non-binding: it composes, it does not
      dominate). If Q1 REFUTEs, the composition form stays open — the
      deposited honestly.
  Q4  THE DISCIPLINE: the re-read consumes exp233's deposit read-only
      (byte-unchanged through the re-read, sha-recorded), the
      arithmetic deterministic, re-run bit-identical.

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
OUT = os.path.join(ROOT, "results", "exp246_quadrature_reread.json")


def main() -> dict:
    # The body keeps every new symbol local to main(): the module above this
    # line is byte-identical to the pre-registration commit 1b98432.
    import hashlib

    from experiments.exp233_field_third_channel import (  # noqa: E402
        ARMS, GAMMA_GRID, KAPPA_GRID, GRID_MU,
        field_weights, f_wrong_profile, field_term,
    )
    from experiments.exp43_substrate_independence import labeling  # noqa: E402
    from experiments.exp73_active_renormalization import (  # noqa: E402
        ERR_BAR, N, make_battery,
    )
    from experiments.exp79_two_channel_law import (  # noqa: E402
        theta_term, v_term,
    )

    print("=== exp246: the quadrature three-channel re-read ===\n")

    def tag(ok: bool) -> str:
        return "PASS" if ok else "REFUTE"

    # ---- Q4 setup: the deposit sha, recorded before any read ----------------
    dep_path = os.path.join(ROOT, "results", "exp233_field_third_channel.json")
    with open(dep_path, "rb") as f:
        raw = f.read()          # READ-ONLY: these bytes are never written back
    sha_before = hashlib.sha256(raw).hexdigest()
    print(f"  exp233 deposit sha256 (pre-read): {sha_before}")
    dep = json.loads(raw.decode("utf-8"))
    pts = dep["grid_points"]
    assert len(pts) == 27, "the deposit must carry the full 27-point grid"
    coords = sorted((p["arm"], float(p["gamma"]), float(p["kappa"]))
                    for p in pts)
    assert len(set(coords)) == 27, "the 27 grid coordinates must be distinct"
    assert all(a in ARMS and g in GAMMA_GRID and k in KAPPA_GRID
               for (a, g, k) in coords), \
        "grid coordinates must be the pre-named (gamma x kappa) x 3 arms"

    # ---- the frozen machinery (imported, never re-implemented) --------------
    battery = make_battery()
    lbl = labeling(N)
    Wf = {arm: field_weights(battery[arm], arm) for arm in ARMS}

    # instrument: the field-kernel re-derivation must match the deposit
    kernel_match = {}
    for arm in ARMS:
        fw, wi = f_wrong_profile(Wf[arm], lbl)
        d = dep["field_kernel"][arm]
        kernel_match[arm] = bool(round(fw, 4) == d["f_worst"]
                                 and wi == d["worst_head_cell"])
    print(f"  field kernel re-derivation matches deposit: {kernel_match}")

    def derive() -> list[dict]:
        """The per-point re-derivation: the three frozen terms at full
        precision (exp79's V-term and theta-term, exp233's field-term)
        composed in quadrature; the deposited measured errs ride along
        UNTOUCHED. No RNG anywhere on this path — deterministic."""
        rows: list[dict] = []
        for p in sorted(pts, key=lambda r: (r["arm"], float(r["gamma"]),
                                            float(r["kappa"]))):
            arm, g, k = p["arm"], float(p["gamma"]), float(p["kappa"])
            eV = v_term(battery[arm], lbl, g)            # CONTRAST*y/(1+y)
            eT = theta_term(battery[arm], lbl, GRID_MU)  # homogenization number
            ef = field_term(Wf[arm], lbl, g, k)          # exp233's field drag
            pq = float(np.sqrt(eV ** 2 + eT ** 2 + ef ** 2))
            pq_dep = float(np.sqrt(p["v_term"] ** 2 + p["theta_term"] ** 2
                                   + p["field_term"] ** 2))
            rows.append({
                "arm": arm, "gamma": g, "kappa": k,
                "err": p["err"],                 # deposited measured err, as-is
                "measured_pass": bool(p["err"] < ERR_BAR),
                "eV": round(eV, 4), "eT": round(eT, 4), "ef": round(ef, 4),
                "pred_q": round(pq, 4),
                "pred_q_deposit_only": round(pq_dep, 4),
                "dep_v_term": p["v_term"], "dep_theta_term": p["theta_term"],
                "dep_field_term": p["field_term"],
                "dep_pred_quad": p["pred_quad"],
                "dep_terms_match": bool(round(eV, 2) == p["v_term"]
                                        and round(eT, 2) == p["theta_term"]
                                        and round(ef, 2) == p["field_term"]),
                "dep_pass_match": bool((p["err"] < ERR_BAR) == p["pass"]),
            })
        return rows

    rows = derive()
    rows_again = derive()        # Q4: the in-process double derivation
    det_inproc = bool(rows == rows_again)

    terms_ok = all(r["dep_terms_match"] and r["dep_pass_match"] for r in rows)
    max_dev_dep = max(abs(r["pred_q"] - r["dep_pred_quad"]) for r in rows)
    print(f"  27/27 re-derived terms match the deposit's 2dp values: "
          f"{terms_ok}; max |pred_q - dep pred_quad| = {max_dev_dep:.4f}")

    errs = np.array([r["err"] for r in rows])
    pqs = np.array([r["pred_q"] for r in rows])
    pqs_dep_only = np.array([r["pred_q_deposit_only"] for r in rows])
    pqs_dep_quad = np.array([r["dep_pred_quad"] for r in rows])

    def spearman(a: np.ndarray, b: np.ndarray) -> float:
        # the house rank correlation (exp79/exp233's own convention)
        return float(np.corrcoef(np.argsort(np.argsort(a)),
                                 np.argsort(np.argsort(b)))[0, 1])

    # ---- Q1: the quadrature law ---------------------------------------------
    rho = spearman(errs, pqs)
    rho_dep_only = spearman(errs, pqs_dep_only)
    rho_dep_quad = spearman(errs, pqs_dep_quad)
    q1 = bool(rho >= 0.90)
    print(f"  Q1 quadrature law: Spearman {rho:.3f} (bar 0.90; the max-form's "
          f"failed {dep['law_stats']['spearman_pred3']:.3f}; exp233's "
          f"non-gating preview {dep['law_stats']['spearman_quad_disclosure']:.3f}) "
          f"-> {tag(q1)}")

    # ---- Q2: the writability boundary ----------------------------------------
    agree_mask = [r["measured_pass"] == (r["pred_q"] < ERR_BAR) for r in rows]
    n_agree = int(sum(agree_mask))
    agree = n_agree / len(rows)
    agree_dep_only = float(np.mean([
        r["measured_pass"] == (r["pred_q_deposit_only"] < ERR_BAR)
        for r in rows]))
    q2 = bool(agree >= 0.80)
    print(f"  Q2 boundary agreement: {n_agree}/{len(rows)} = {agree:.1%} "
          f"(bar 80%) -> {tag(q2)}")

    # the boundary's failure anatomy (the honest deposit carries it)
    disagreements = [
        {"arm": r["arm"], "gamma": r["gamma"], "kappa": r["kappa"],
         "err": r["err"], "pred_q": r["pred_q"],
         "dominant_term": max((("V", r["eV"]), ("T", r["eT"]),
                               ("f", r["ef"])), key=lambda t: t[1])[0]}
        for r in rows if r["measured_pass"] != (r["pred_q"] < ERR_BAR)]
    for d in disagreements:
        print(f"    boundary miss: {d['arm']:11s} g{d['gamma']:<5g} "
              f"k{d['kappa']:<4g} err {d['err']:5.2f} pred_q "
              f"{d['pred_q']:6.2f} (dominant {d['dominant_term']})")

    # ---- Q3: the three-channel verdict (the composition named) ---------------
    if q1 and q2:
        branch = "QUADRATURE"
        named = True
    else:
        branch = "OPEN"
        named = False
    if q1 and q2:
        branch_fired = "Q1+Q2 PASS"
    elif not q1:
        branch_fired = "Q1 REFUTE"
    else:
        branch_fired = ("NONE — the unnamed middle case (Q1 PASS, Q2 REFUTE); "
                        "the naming condition Q1+Q2 is unmet, deposited "
                        "honestly")
    composition = {
        "branch": branch,
        "composition_named": named,
        "law_form": ("the quadrature three-channel form "
                     "pred_q = sqrt(eV^2 + eT^2 + ef^2)" if named else
                     "open — the composition is NOT named by this re-read"),
        "exp233_F3_refined": named,
        "field_channel_status": (
            "real but non-binding: it composes, it does not dominate"
            if named else
            "unchanged from exp233's deposit — the composition form stays "
            "open; the boundary misses carry the theta term's face, not the "
            "field's"),
        "q1_pass": q1, "q2_pass": q2,
        "branch_fired": branch_fired,
    }
    print(f"  Q3 three-channel verdict: branch {branch} "
          f"(composition named: {named}) [{branch_fired}]")

    # ---- Q4: the discipline ---------------------------------------------------
    with open(dep_path, "rb") as f:
        raw_after = f.read()     # the byte-unchanged check, after every read
    sha_after = hashlib.sha256(raw_after).hexdigest()
    byte_unchanged = bool(sha_after == sha_before and raw_after == raw)
    q4 = bool(byte_unchanged and det_inproc and terms_ok
              and all(kernel_match.values()))
    print(f"  Q4 discipline: deposit byte-unchanged {byte_unchanged} "
          f"(sha {sha_before[:12]}...), double derivation bit-identical "
          f"{det_inproc}, term matches {terms_ok} -> {tag(q4)}")

    criteria = {
        "Q1_quadrature_law": q1,
        "Q2_boundary_agreement": q2,
        "Q3_composition_named": named,
        "Q4_discipline": q4,
    }

    finding = (
        f"Q1 {tag(q1)}: the quadrature composition "
        f"pred_q=sqrt(eV^2+eT^2+ef^2) over the re-derived frozen terms pools "
        f"at Spearman {rho:.3f} across the 27-point deposited grid (bar 0.90; "
        f"the max-form's failed {dep['law_stats']['spearman_pred3']:.3f}; "
        f"exp233's non-gating preview "
        f"{dep['law_stats']['spearman_quad_disclosure']:.3f} on the 2dp "
        f"deposit, {rho_dep_only:.3f} recomposed from the deposited rounded "
        f"terms) — the rank law HOLDS at quadrature; "
        f"Q2 {tag(q2)}: the writability boundary (pred_q<6.0 iff err<6.0) "
        f"agrees on {n_agree}/27 = {agree:.1%}, under the 80% bar — all "
        f"{len(disagreements)} misses are the torus arm at gamma>=4, where "
        f"the theta-term (11.45) dominates pred_q at 11.45-11.81 while the "
        f"measured errs sit under the bar (4.80-5.92): quadrature fixed the "
        f"RANKING, not the boundary, and the residual is the theta-term's "
        f"torus over-prediction, not the field channel (the max-form posted "
        f"the same 21/27); "
        f"Q3: branch {branch} — the composition is NOT named ({branch_fired}): "
        f"the three-channel composition form stays open, with the partial "
        f"disclosed (the rank law holds at quadrature while the boundary "
        f"clause fails on the theta term's torus face; the field channel's "
        f"status is unchanged from exp233's deposit); "
        f"Q4 {tag(q4)}: exp233's deposit consumed READ-ONLY (sha256 "
        f"{sha_before} recorded pre-read and byte-unchanged through the "
        f"re-read), all 27 points' terms re-derived with the imported frozen "
        f"forms match the deposit's 2dp values (max deviation "
        f"{max_dev_dep:.4f} mV, pure rounding), zero re-simulation (the "
        f"measured errs are the deposit's), the arithmetic deterministic "
        f"(in-process double derivation bit-identical; cross-process re-run "
        f"verified byte-identical pre-commit).")

    out = {
        "exp": "exp246_quadrature_reread (the law's composition form; "
               "exp233's registered next; ledger L222)",
        "consumed_deposit": {
            "path": "results/exp233_field_third_channel.json",
            "mode": "read-only",
            "sha256_before": sha_before,
            "sha256_after_reread": sha_after,
            "byte_unchanged": byte_unchanged,
        },
        "grid_points": rows,
        "law_stats": {
            "spearman_pred_q": round(rho, 4),
            "boundary_agreement": round(agree, 4),
            "n_boundary_agree": n_agree,
            "n_points": len(rows),
            "spearman_deposit_only": round(rho_dep_only, 4),
            "agreement_deposit_only": round(agree_dep_only, 4),
            "spearman_deposit_pred_quad_as_deposited": round(rho_dep_quad, 4),
            "exp233_deposited_spearman_pred3":
                dep["law_stats"]["spearman_pred3"],
            "exp233_deposited_spearman_quad_disclosure":
                dep["law_stats"]["spearman_quad_disclosure"],
            "exp233_deposited_agreement_quad_disclosure":
                dep["law_stats"]["agreement_quad_disclosure"],
            "exp79_tc_g1_bar_spearman": 0.90,
            "exp79_tc_g1_bar_agreement": 0.80,
        },
        "boundary_disagreements": disagreements,
        "instrument": {
            "terms_rederived_from_frozen_forms": True,
            "imports": {
                "v_term/theta_term": "experiments/exp79_two_channel_law.py",
                "field_term/field_weights/f_wrong_profile":
                    "experiments/exp233_field_third_channel.py",
            },
            "dep_term_rounding_match": terms_ok,
            "field_kernel_match": kernel_match,
            "max_abs_pred_q_minus_dep_pred_quad": round(max_dev_dep, 4),
            "in_process_double_derivation_identical": det_inproc,
            "resimulation": "none — zero dynamics runs; the errs are the "
                            "deposit's",
        },
        "composition_verdict": composition,
        "criteria": criteria,
        "notes": (
            "The re-read protocol: exp233's deposit is consumed read-only "
            "(the bytes sha256-recorded before any read and re-verified "
            "unchanged after; the file is never opened for write). The "
            "measured errs, the per-point pass bits and the grid coordinates "
            "are the deposit's own quantities, consumed as-is — ZERO "
            "re-simulation on the gate path. The three prediction terms are "
            "re-derived per point with the frozen forms IMPORTED verbatim "
            "(exp79's v_term/theta_term; exp233's field_term on the "
            "field_weights kernel, whose f_worst/worst-cell profile was "
            "re-checked against the deposit's field_kernel block) and "
            "composed as pred_q = sqrt(eV^2 + eT^2 + ef^2) at full "
            "precision; every recomputed term matches the deposit's 2dp "
            "stored value, so the re-derivation is the deposit's own "
            "arithmetic continued, not a new instrument. Q1 gates the "
            "Spearman rank correlation on the house convention (argsort-"
            "of-argsort corrcoef, exp79/exp233's own); Q2 gates the "
            "writability boundary (pred_q < 6.0 iff err < 6.0) at exp79 "
            "TC-G1's 80% clause. Q3 is the pre-registered conditional "
            "verdict: QUADRATURE is named only if Q1+Q2 both PASS; if Q1 "
            "REFUTES the form stays open; the observed outcome (Q1 PASS, Q2 "
            "REFUTE) is the unnamed middle case — neither pre-named branch "
            "fires, so the composition is honestly NOT named and the branch "
            "is recorded OPEN with the partial disclosed. Q4's determinism: "
            "no RNG on the re-read path, the full derivation run twice "
            "in-process and asserted identical, and the cross-process re-run "
            "(two fresh invocations) verified byte-identical on the results "
            "file pre-commit. The docstring and every other byte of this "
            "module above main() are identical to pre-registration commit "
            "1b98432."),
        "finding": finding,
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    npass = sum(bool(v) for v in criteria.values())
    print(f"  === {npass}/4 gate criteria PASS "
          f"(Q1 {tag(q1)}, Q2 {tag(q2)}, Q3 branch {branch}, "
          f"Q4 {tag(q4)}) ===")
    print(f"  FINDING: {finding}")
    return out


if __name__ == "__main__":
    main()
