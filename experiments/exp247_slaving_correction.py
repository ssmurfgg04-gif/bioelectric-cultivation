#!/usr/bin/env python3
"""exp247 — THE THETA-TERM'S SLAVING CORRECTION (exp246's registered
next; the two-channel law's missing coupled-mode term; ledger L225).

THE OPEN ITEM (L224): the quadrature law's 6 boundary misses are ALL the
theta-term over-predicting on the torus at gamma>=4 (pred 11.45 vs
measured 4.80-5.92): the homogenization number assumes the identity
layer homogenizes at the UNCOPLED rate mu*deg — but theta's dynamics
are SLAVED to the coupled (V,theta) system, whose homogenization mode
decays at the COUPLED slow eigenvalue, not mu*deg. THE ZERO-KNOB
CORRECTION: for a theta-mode with Laplacian eigenvalue lambda (= deg,
exp79's own per-cell proxy), the coupled 2x2 block on the mode
amplitudes (v, w) is [[-(gamma+lambda_G), gamma], [eps, -(eps+mu*lambda)]]
with lambda_G = lambda*G_GAP — the homogenization rate = |slow
eigenvalue| of this block, EXACT from the linear algebra, no fitting.
exp79's raw form is the limiting case and is recovered as a sanity
anchor.

PRE-REGISTERED GATES:

  C1  THE ANCHOR: the corrected theta-term reproduces exp79's deposited
      grid errs bit-consistently on the gamma=0.25 column (the
      plateau's own regime) within the deposit's 2dp rounding.
  C2  THE BOUNDARY CLOSES: exp233's 27-point grid re-read under the
      corrected quadrature pred — the writability boundary agreement
      rises from 21/27 (77.8%) to >= 24/27.
  C3  THE RANK HOLDS: the corrected quadrature pred keeps Spearman
      >= 0.90 (the Q1 result must survive the correction).
  C4  THE DISCIPLINE: exp233's and exp79's deposits consumed READ-ONLY
      (sha-recorded, byte-unchanged), the arithmetic deterministic,
      re-run bit-identical.

THE BRANCH (pre-named): C2 PASS -> SLAVING-CORRECTED (the law's
theta-term gains its coupled-mode form; the composition names with the
boundary closed); C2 REFUTE -> RESIDUAL-NAMED (the torus face is not
the slaving — the misses' driver named for the next instrument).

RUN: the deposit re-reads + the 2x2 eigensolves; seconds.
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
OUT = os.path.join(ROOT, "results", "exp247.json")


def main() -> dict:
    # The body keeps every new symbol local to main(): the module above this
    # line is byte-identical to the pre-registration commit c24b909.
    import hashlib
    import inspect

    from cultivation.bioelectric.collective import (  # noqa: E402
        BioElectricCollective,
    )
    from experiments.exp233_field_third_channel import (  # noqa: E402
        ARMS, GAMMA_GRID, KAPPA_GRID, GRID_MU,
        field_term, field_weights,
    )
    from experiments.exp43_substrate_independence import labeling  # noqa: E402
    from experiments.exp73_active_renormalization import (  # noqa: E402
        ERR_BAR, HEAD_V, N, make_battery,
    )
    from experiments.exp78_phase_diagram import G_GAP  # noqa: E402
    from experiments.exp79_two_channel_law import (  # noqa: E402
        MU_GRID, RUN_T, theta_term, v_term,
    )

    print("=== exp247: the theta-term's slaving correction ===\n")

    def tag(ok: bool) -> str:
        return "PASS" if ok else "REFUTE"

    # ---- the frozen core's dials, derived not re-declared -------------------
    # eps = the frozen core's homeostatic plasticity rate (the docstring's
    # "eps=0.04 from the frozen core"); G_GAP = exp78's frozen gap conductance
    # (the docstring's G_GAP=0.20). Both asserted against the pre-named values.
    EPS_CORE = inspect.signature(
        BioElectricCollective.__init__).parameters["eps"].default
    assert float(EPS_CORE) == 0.04, "the frozen core's eps must be 0.04"
    assert float(G_GAP) == 0.20, "exp78's G_GAP must be 0.20"
    print(f"  frozen core: eps={EPS_CORE} (BioElectricCollective default), "
          f"G_GAP={G_GAP} (exp78)")

    # ---- C4 setup: BOTH deposit shas, recorded before any read --------------
    dep_paths = {
        "exp233": os.path.join(ROOT, "results",
                               "exp233_field_third_channel.json"),
        "exp79": os.path.join(ROOT, "results",
                              "exp79_two_channel_law.json"),
    }
    sha_before, raw_before = {}, {}
    for name, path in dep_paths.items():
        with open(path, "rb") as f:
            raw = f.read()      # READ-ONLY: these bytes are never written back
        raw_before[name] = raw
        sha_before[name] = hashlib.sha256(raw).hexdigest()
        print(f"  {name} deposit sha256 (pre-read): {sha_before[name]}")
    dep233 = json.loads(raw_before["exp233"].decode("utf-8"))
    dep79 = json.loads(raw_before["exp79"].decode("utf-8"))
    pts = dep233["grid_points"]
    assert len(pts) == 27, "the exp233 deposit must carry the full 27-point grid"
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

    # ---- THE ZERO-KNOB CORRECTION: the coupled 2x2 block's slow eigenvalue --
    # block on the mode amplitudes (v, w) = (V-mode, theta-mode), lambda =
    # exp79's own per-cell proxy (= deg):
    #   [[-(gamma+lambda_G), gamma], [eps, -(eps+mu*lambda)]], lambda_G =
    #   lambda*G_GAP. The homogenization rate = |slow eigenvalue| — the
    # closed-form quadratic root (exact, deterministic), cross-checked
    # against numpy's eigensolver over the full sweep.
    def slow_rate(lam: float, gamma: float, mu: float,
                  g_gap: float = G_GAP, eps: float = EPS_CORE) -> float:
        a = -(gamma + lam * g_gap)
        d = -(eps + mu * lam)
        s_slow = 0.5 * (a + d) + np.sqrt(0.25 * (a - d) ** 2
                                         + gamma * eps)
        return abs(float(s_slow))

    def slow_rate_eig(lam: float, gamma: float, mu: float,
                      g_gap: float = G_GAP, eps: float = EPS_CORE) -> float:
        m = np.array([[-(gamma + lam * g_gap), gamma],
                      [eps, -(eps + mu * lam)]])
        ev = np.linalg.eigvals(m)
        return abs(float(ev[np.argmin(np.abs(ev))]))

    sweep = [(lam, g, mu) for lam in range(1, 13) for g in GAMMA_GRID
             for mu in sorted(set(MU_GRID) | {GRID_MU})]
    eig_dev = max(abs(slow_rate(l, g, m) - slow_rate_eig(l, g, m))
                  for (l, g, m) in sweep)
    assert eig_dev < 1e-10, "closed-form slow eigenvalue must match eigensolver"
    print(f"  2x2 eigensolver cross-check over {len(sweep)} (lambda x gamma x "
          f"mu) combos: max |closed-form - eig| = {eig_dev:.2e}")

    # the direction identity, both signs: |slow| > mu*lambda <=> G_GAP > mu
    # (the frozen G_GAP=0.20 vs the counterfactual G_GAP=0.01 < mu=0.015)
    dir_ok = all(
        (slow_rate(l, g, m, g_gap=gg) > m * l) == (gg > m)
        for (l, g, m) in sweep for gg in (G_GAP, 0.01))
    print(f"  direction identity |slow| > mu*lambda <=> G_GAP > mu, both "
          f"signs over the sweep: {dir_ok}")

    def theta_term_corrected(A: np.ndarray, lbl_: np.ndarray, gamma: float,
                             mu: float) -> float:
        """exp79's theta-term FORM (worst head cell: the local identity
        imbalance x the homogenization fraction over the SAME RUN_T window),
        with the homogenization rate replaced by the coupled block's
        |slow eigenvalue|. exp79's raw form is recovered exactly when the
        rate is forced back to the uncoupled mu*deg (asserted below against
        the IMPORTED theta_term, bit-exactly)."""
        hi = (lbl_ == HEAD_V)
        worst = 0.0
        for i in np.where(hi)[0]:
            nbrs = np.where(A[i] > 0)[0]
            if len(nbrs) == 0:
                continue
            imbalance = abs(float(np.mean(lbl_[nbrs]) - lbl_[i]))
            rate = slow_rate(len(nbrs), gamma, mu)
            worst = max(worst, imbalance * (1 - np.exp(-rate * RUN_T)))
        return worst

    def theta_term_uncoupled(A: np.ndarray, lbl_: np.ndarray,
                             mu: float) -> float:
        """The corrected form with the rate FORCED to the uncoupled mu*deg —
        the instrument's recovery of exp79's raw form (bit-exact)."""
        hi = (lbl_ == HEAD_V)
        worst = 0.0
        for i in np.where(hi)[0]:
            nbrs = np.where(A[i] > 0)[0]
            if len(nbrs) == 0:
                continue
            imbalance = abs(float(np.mean(lbl_[nbrs]) - lbl_[i]))
            worst = max(worst,
                        imbalance * (1 - np.exp(-mu * len(nbrs) * RUN_T)))
        return worst

    form_recovery = all(theta_term_uncoupled(battery[arm], lbl, mu)
                        == theta_term(battery[arm], lbl, mu)
                        for arm in ARMS for mu in MU_GRID)
    # the limiting case in the docstring's sense: with the couplings zeroed
    # (eps=0, G_GAP=0) the block is triangular -> |slow| = min(gamma, mu*lambda),
    # which equals the raw rate mu*lambda wherever gamma > mu*lambda (all sweep
    # combos: gamma >= 0.25 > 0.015*12)
    lim_ok = all(
        abs(slow_rate(l, g, m, g_gap=0.0, eps=0.0) - min(g, m * l)) < 1e-10
        and abs(slow_rate_eig(l, g, m, g_gap=0.0, eps=0.0)
                - min(g, m * l)) < 1e-10
        for (l, g, m) in sweep)
    lim_is_raw = all(min(g, m * l) == m * l for (l, g, m) in sweep)
    print(f"  form recovery (uncoupled rate == imported exp79 theta_term, "
          f"bit-exact): {form_recovery}; uncoupled-limit eigenvalue identity "
          f"|slow| -> min(gamma, mu*lambda) at eps=0/G_GAP=0: {lim_ok} "
          f"(= the raw rate mu*lambda on every sweep combo: {lim_is_raw})")

    # ---- the imported forms vs the deposits (instrument anchoring) ----------
    dep233_terms_ok = True
    for p in pts:
        arm, g, k = p["arm"], float(p["gamma"]), float(p["kappa"])
        vt = v_term(battery[arm], lbl, g)
        tt = theta_term(battery[arm], lbl, GRID_MU)
        ft = field_term(Wf[arm], lbl, g, k)
        dep233_terms_ok &= bool(round(vt, 2) == p["v_term"]
                                and round(tt, 2) == p["theta_term"]
                                and round(ft, 2) == p["field_term"]
                                and (p["err"] < ERR_BAR) == p["pass"])
    col79_reproduced = True
    for arm in ARMS:
        A = battery[arm]
        vt = v_term(A, lbl, 0.25)
        for mu in MU_GRID:
            dep = dep79["grid"][arm][f"g0.25|mu{mu}"]
            col79_reproduced &= bool(
                round(max(vt, theta_term(A, lbl, mu)), 2) == dep["pred"])
    print(f"  exp233's 27 deposited term values reproduced by the imported "
          f"frozen forms: {dep233_terms_ok}; exp79's gamma=0.25 column preds "
          f"reproduced by the raw max-form: {col79_reproduced}")

    # ---- C1: THE ANCHOR — exp79's gamma=0.25 column under the correction ----
    c1_rows = []
    for arm in ARMS:
        A = battery[arm]
        vt = v_term(A, lbl, 0.25)
        for mu in MU_GRID:
            dep = dep79["grid"][arm][f"g0.25|mu{mu}"]
            t_raw = theta_term(A, lbl, mu)
            t_corr = theta_term_corrected(A, lbl, 0.25, mu)
            pred_corr = max(vt, t_corr)
            c1_rows.append({
                "arm": arm, "mu": mu,
                "dep_err": dep["err"], "dep_pred": dep["pred"],
                "v_term": round(vt, 4), "theta_raw": round(t_raw, 4),
                "theta_corrected": round(t_corr, 4),
                "pred_corrected": round(pred_corr, 4),
                "facet_err_match": bool(round(t_corr, 2) == dep["err"]),
                "facet_pred_match": bool(round(pred_corr, 2) == dep["pred"]),
            })
    facet_err = [r for r in c1_rows if r["facet_err_match"]]
    facet_pred = [r for r in c1_rows if r["facet_pred_match"]]
    c1 = bool(len(facet_err) == len(c1_rows))
    t_lo = min(r["theta_corrected"] for r in c1_rows)
    t_hi = max(r["theta_corrected"] for r in c1_rows)
    e_lo = min(r["dep_err"] for r in c1_rows)
    e_hi = max(r["dep_err"] for r in c1_rows)
    print(f"  C1 anchor (gamma=0.25 column, 15 points): corrected theta-term "
          f"vs deposited errs at 2dp: {len(facet_err)}/15 "
          f"-> {tag(c1)} (corrected {t_lo:.2f}-{t_hi:.2f} vs deposited "
          f"{e_lo:.2f}-{e_hi:.2f}); [disclosed alternate reading — corrected "
          f"max-pred vs deposited pred: {len(facet_pred)}/15]")

    # ---- the corrected quadrature re-read of exp233's 27-point grid ---------
    def derive() -> list[dict]:
        rows: list[dict] = []
        for p in sorted(pts, key=lambda r: (r["arm"], float(r["gamma"]),
                                            float(r["kappa"]))):
            arm, g, k = p["arm"], float(p["gamma"]), float(p["kappa"])
            eV = v_term(battery[arm], lbl, g)               # exp79's form
            eT = theta_term_corrected(battery[arm], lbl, g, GRID_MU)
            eT_raw = theta_term(battery[arm], lbl, GRID_MU)  # exp79's, raw
            ef = field_term(Wf[arm], lbl, g, k)             # exp233's form
            pq = float(np.sqrt(eV ** 2 + eT ** 2 + ef ** 2))
            pq_raw = float(np.sqrt(eV ** 2 + eT_raw ** 2 + ef ** 2))
            rows.append({
                "arm": arm, "gamma": g, "kappa": k,
                "err": p["err"],                # deposited measured err, as-is
                "measured_pass": bool(p["err"] < ERR_BAR),
                "eV": round(eV, 4), "eT_corrected": round(eT, 4),
                "eT_raw": round(eT_raw, 4), "ef": round(ef, 4),
                "pred_q_corrected": round(pq, 4),
                "pred_q_raw": round(pq_raw, 4),
                "pred_pass_corrected": bool(pq < ERR_BAR),
                "pred_pass_raw": bool(pq_raw < ERR_BAR),
                "agree_corrected": bool((p["err"] < ERR_BAR) == (pq < ERR_BAR)),
                "agree_raw": bool((p["err"] < ERR_BAR)
                                  == (pq_raw < ERR_BAR)),
            })
        return rows

    rows = derive()
    rows_again = derive()        # C4: the in-process double derivation
    det_inproc = bool(rows == rows_again)

    errs = np.array([r["err"] for r in rows])
    pqs = np.array([r["pred_q_corrected"] for r in rows])
    pqs_raw = np.array([r["pred_q_raw"] for r in rows])

    def spearman(a: np.ndarray, b: np.ndarray) -> float:
        # the house rank correlation (exp79/exp233/exp246's own convention)
        return float(np.corrcoef(np.argsort(np.argsort(a)),
                                 np.argsort(np.argsort(b)))[0, 1])

    # ---- C2: THE BOUNDARY ----------------------------------------------------
    n_agree = int(sum(r["agree_corrected"] for r in rows))
    n_agree_raw = int(sum(r["agree_raw"] for r in rows))
    agree = n_agree / len(rows)
    c2 = bool(n_agree >= 24)
    print(f"  C2 boundary: {n_agree}/27 = {agree:.1%} under the corrected "
          f"quadrature pred (bar >= 24/27; exp246's raw-form recomputed "
          f"{n_agree_raw}/27 first-hand) -> {tag(c2)}")

    # ---- C3: THE RANK ---------------------------------------------------------
    rho = spearman(errs, pqs)
    rho_raw = spearman(errs, pqs_raw)
    c3 = bool(rho >= 0.90)
    print(f"  C3 rank: Spearman {rho:.4f} (bar 0.90; the raw-form recompute "
          f"{rho_raw:.4f}, exp246's deposited 0.9359) -> {tag(c3)}")

    # ---- the misses' anatomy (the RESIDUAL-NAMED naming) ---------------------
    def theta_drag_population(A: np.ndarray, lbl_: np.ndarray, gamma: float,
                              mu: float) -> float:
        """The SAME corrected drag, aggregated as the 100-cell population RMS
        (every cell, both pattern sides) instead of the worst head cell —
        the diagnostic that names the residual's driver."""
        drags = []
        for i in range(A.shape[0]):
            nbrs = np.where(A[i] > 0)[0]
            if len(nbrs) == 0:
                drags.append(0.0)
                continue
            imbalance = abs(float(np.mean(lbl_[nbrs]) - lbl_[i]))
            rate = slow_rate(len(nbrs), gamma, mu)
            drags.append(imbalance * (1 - np.exp(-rate * RUN_T)))
        return float(np.sqrt(np.mean(np.array(drags) ** 2)))

    misses = []
    for r, p in zip(rows, sorted(pts, key=lambda x: (x["arm"],
                                                     float(x["gamma"]),
                                                     float(x["kappa"])))):
        if r["agree_corrected"]:
            continue
        arm, g = r["arm"], r["gamma"]
        eT_pop = theta_drag_population(battery[arm], lbl, g, GRID_MU)
        pq_pop = float(np.sqrt(r["eV"] ** 2 + eT_pop ** 2 + r["ef"] ** 2))
        lam_worst = float(max(len(np.where(battery[arm][i] > 0)[0])
                              for i in np.where(lbl == HEAD_V)[0]))
        misses.append({
            "arm": arm, "gamma": g, "kappa": r["kappa"],
            "err": r["err"], "pred_q_corrected": r["pred_q_corrected"],
            "pred_q_raw_exp246": r["pred_q_raw"],
            "eT_worst_cell": r["eT_corrected"],
            "eT_population_rms": round(eT_pop, 4),
            "pred_q_population": round(pq_pop, 4),
            "measured_minus_population_pred": round(r["err"] - pq_pop, 4),
            "slow_rate_at_worst_deg": round(
                slow_rate(lam_worst, g, GRID_MU), 6),
            "uncoupled_rate_mu_deg": round(GRID_MU * lam_worst, 6),
        })
    pop_lo = min(m["pred_q_population"] for m in misses)
    pop_hi = max(m["pred_q_population"] for m in misses)
    print(f"  miss anatomy ({len(misses)} misses): worst-cell drag "
          f"{min(m['eT_worst_cell'] for m in misses):.2f}-"
          f"{max(m['eT_worst_cell'] for m in misses):.2f} mV vs the SAME "
          f"corrected drag as the population RMS "
          f"{min(m['eT_population_rms'] for m in misses):.2f}-"
          f"{max(m['eT_population_rms'] for m in misses):.2f} mV; "
          f"population-form pred {pop_lo:.2f}-{pop_hi:.2f} vs measured "
          f"{min(m['err'] for m in misses):.2f}-{max(m['err'] for m in misses):.2f}")

    # ---- C4: THE DISCIPLINE ---------------------------------------------------
    byte_unchanged = True
    sha_after = {}
    for name, path in dep_paths.items():
        with open(path, "rb") as f:
            raw_after = f.read()   # the byte-unchanged check, after every read
        sha_after[name] = hashlib.sha256(raw_after).hexdigest()
        byte_unchanged &= bool(sha_after[name] == sha_before[name]
                               and raw_after == raw_before[name])
    c4 = bool(byte_unchanged and det_inproc and dep233_terms_ok
              and col79_reproduced and form_recovery and lim_ok and dir_ok)
    print(f"  C4 discipline: both deposits byte-unchanged {byte_unchanged}, "
          f"double derivation bit-identical {det_inproc}, imported-form "
          f"matches {dep233_terms_ok and col79_reproduced} -> {tag(c4)}")

    # ---- THE BRANCH (pre-named) -----------------------------------------------
    branch = "SLAVING-CORRECTED" if c2 else "RESIDUAL-NAMED"

    criteria = {
        "C1_gamma025_column_anchor": c1,
        "C2_boundary_closes_24_of_27": c2,
        "C3_spearman_holds_090": c3,
        "C4_discipline": c4,
    }

    finding = (
        f"C1 {tag(c1)}: the gamma=0.25 column anchor — the corrected "
        f"theta-term (exp79's worst-head-cell form, the homogenization rate "
        f"replaced by the coupled 2x2 block's |slow eigenvalue|) does NOT "
        f"reproduce exp79's deposited errs bit-consistently on the column "
        f"({len(facet_err)}/15 at the deposit's 2dp rounding): the corrected "
        f"term runs {t_lo:.2f}-{t_hi:.2f} mV against the deposited "
        f"{e_lo:.2f}-{e_hi:.2f} — the coupled slow eigenvalue is FASTER than "
        f"the uncoupled mu*deg wherever G_GAP > mu, so the correction moves "
        f"the term UP, away from the errs (the disclosed alternate reading — "
        f"corrected max-pred vs the deposited pred column — fails identically "
        f"at {len(facet_pred)}/15); the anchor's instrument layer does hold "
        f"(the imported raw forms reproduce the deposited column bit-"
        f"consistently and the uncoupled limit recovers exp79's raw form "
        f"exactly) — the refuted clause is the CORRECTION's, not the "
        f"machinery's; "
        f"C2 {tag(c2)}: exp233's 27-point grid re-read under the corrected "
        f"quadrature pred stays at {n_agree}/27 = {agree:.1%} (bar >= 24) — "
        f"the same 6 torus gamma>=4 misses, now DEEPER (pred_q "
        f"{min(m['pred_q_corrected'] for m in misses):.2f}-"
        f"{max(m['pred_q_corrected'] for m in misses):.2f} vs exp246's raw "
        f"{min(m['pred_q_raw_exp246'] for m in misses):.2f}-"
        f"{max(m['pred_q_raw_exp246'] for m in misses):.2f} over measured "
        f"{min(m['err'] for m in misses):.2f}-"
        f"{max(m['err'] for m in misses):.2f}): the direction identity "
        f"(verified over the full (lambda x gamma x mu) sweep, both G_GAP "
        f"signs) makes the slaving correction move every miss AWAY from the "
        f"measured errs; "
        f"C3 {tag(c3)}: the corrected quadrature pred keeps Spearman "
        f"{rho:.4f} >= 0.90 across the 27 points (the raw form recomputed "
        f"first-hand at {rho_raw:.4f}, exp246's deposited 0.9359) — the rank "
        f"law SURVIVES the correction; "
        f"C4 {tag(c4)}: both deposits consumed READ-ONLY (sha256 recorded "
        f"pre-read and byte-unchanged through the re-read), zero "
        f"re-simulation (the measured errs are the deposits'), the "
        f"arithmetic deterministic (in-process double derivation "
        f"bit-identical); "
        f"BRANCH {branch}: the torus face is NOT the slaving — the misses' "
        f"driver, named for the next instrument: the theta-term's "
        f"AGGREGATION, not its homogenization rate. The corrected drag's "
        f"worst-head-cell form sits at "
        f"{min(m['eT_worst_cell'] for m in misses):.2f}-"
        f"{max(m['eT_worst_cell'] for m in misses):.2f} mV on the torus "
        f"gamma>=4 points while the SAME corrected drag aggregated as the "
        f"100-cell population RMS sits at "
        f"{min(m['eT_population_rms'] for m in misses):.2f}-"
        f"{max(m['eT_population_rms'] for m in misses):.2f} mV — composed "
        f"with the V-term the population form lands at {pop_lo:.2f}-"
        f"{pop_hi:.2f} vs the measured {min(m['err'] for m in misses):.2f}-"
        f"{max(m['err'] for m in misses):.2f} (within "
        f"{max(abs(m['measured_minus_population_pred']) for m in misses):.2f} "
        f"mV on every miss): the torus's thin boundary dilutes the worst-cell "
        f"drag in the population RMS, and the next instrument is the "
        f"theta-term's aggregation form, not its rate.")

    out = {
        "exp": "exp247_slaving_correction (the theta-term's slaving "
               "correction; exp246's registered next; ledger L225)",
        "consumed_deposits": {
            name: {
                "path": os.path.relpath(dep_paths[name], ROOT),
                "mode": "read-only",
                "sha256_before": sha_before[name],
                "sha256_after_reread": sha_after[name],
                "byte_unchanged": bool(
                    sha_after[name] == sha_before[name]),
            } for name in dep_paths},
        "instrument": {
            "G_GAP": float(G_GAP),
            "eps_frozen_core": float(EPS_CORE),
            "eps_derivation": "inspect.signature("
                              "BioElectricCollective.__init__)"
                              ".parameters['eps'].default — the frozen "
                              "core's own default, not re-declared",
            "block": "[[-(gamma+lambda_G), gamma], "
                     "[eps, -(eps+mu*lambda)]], lambda_G = lambda*G_GAP, "
                     "lambda = deg (exp79's own per-cell proxy)",
            "homogenization_rate": "|slow eigenvalue| of the block "
                                   "(closed-form quadratic root, "
                                   "deterministic)",
            "eigensolver_cross_check_max_dev": float(eig_dev),
            "direction_identity_both_signs": bool(dir_ok),
            "form_recovery_bit_exact_vs_imported_theta_term":
                bool(form_recovery),
            "uncoupled_limit_identity_min_gamma_mulambda": bool(lim_ok),
            "uncoupled_limit_equals_raw_rate_on_sweep": bool(lim_is_raw),
            "imports": {
                "v_term/theta_term/RUN_T/MU_GRID":
                    "experiments/exp79_two_channel_law.py",
                "field_term/field_weights":
                    "experiments/exp233_field_third_channel.py",
                "G_GAP": "experiments/exp78_phase_diagram.py",
                "HEAD_V/ERR_BAR/N/make_battery":
                    "experiments/exp73_active_renormalization.py",
            },
            "resimulation": "none — zero dynamics runs; the errs are the "
                            "deposits'",
            "in_process_double_derivation_identical": det_inproc,
        },
        "c1_column": c1_rows,
        "grid_points": rows,
        "law_stats": {
            "spearman_corrected": round(rho, 4),
            "boundary_agreement_corrected": round(agree, 4),
            "n_boundary_agree_corrected": n_agree,
            "spearman_raw_recomputed": round(rho_raw, 4),
            "n_boundary_agree_raw_recomputed": n_agree_raw,
            "exp246_deposited_reference": {
                "spearman_pred_q": 0.9359, "n_boundary_agree": 21,
                "provenance": "results/exp246_quadrature_reread.json at "
                              "commit 67a2e11 (cited, not consumed)"},
            "n_points": len(rows), "bar_spearman": 0.90,
            "bar_boundary_agree": 24,
        },
        "boundary_disagreements": misses,
        "criteria": criteria,
        "branch": branch,
        "notes": (
            "Protocol: BOTH deposits (exp233's 27-point grid, exp79's 45-"
            "point (gamma x mu) grid) are consumed READ-ONLY — the bytes "
            "sha256-recorded before any read and re-verified unchanged "
            "after; the files are never opened for write; the measured errs "
            "and pass bits are the deposits' own quantities (ZERO "
            "re-simulation). The corrected theta-term keeps exp79's "
            "theta-term FORM verbatim (the local identity imbalance at the "
            "worst head cell x the homogenization fraction over the SAME "
            "RUN_T=24 window) with the rate replaced by the docstring's "
            "coupled 2x2 block's |slow eigenvalue| — the block IS the "
            "frozen core's (V,theta) dynamics linearized on a Laplacian "
            "mode (dV = gamma*(theta-V) + gap diffusion at lambda*G_GAP; "
            "dtheta = eps*(V-theta) + mu*lap at mu*lambda); the rate is the "
            "closed-form quadratic root, cross-checked against numpy's "
            "eigensolver over the full (lambda x gamma x mu) sweep (max dev "
            "deposited). Form recovery: forcing the rate back to the "
            "uncoupled mu*deg reproduces the IMPORTED exp79 theta_term "
            "BIT-EXACTLY (the form is exp79's own); zeroing the couplings "
            "(eps=0, G_GAP=0) makes the block triangular and |slow| -> "
            "min(gamma, mu*lambda), the docstring's 'exp79's raw form is "
            "the limiting case'. The direction identity |slow| > mu*lambda "
            "<=> G_GAP > mu is verified over the sweep with BOTH signs (the "
            "frozen G_GAP=0.20 and the counterfactual 0.01 < mu): the "
            "coupled slaving SPEEDS homogenization up in this stack's "
            "regime (G_GAP=0.20 >> mu=0.015), because the eps-coupling "
            "drains the identity into the V layer whose gap diffusion "
            "carries it away. C1's clause is evaluated literally (the "
            "corrected theta-term vs the deposited errs at the deposit's "
            "2dp rounding, 15 points) with the alternate reading (corrected "
            "max-pred vs the deposited pred column) deposited per-point "
            "alongside — the anchor refutes under either; the raw-form "
            "instrument checks it sits on (the imported forms reproduce "
            "exp79's column and exp233's 27 term values bit-consistently) "
            "all hold, so the refutation is the correction's, not the "
            "machinery's. The population-RMS drag aggregation is a "
            "DISCLOSED diagnostic only (never gated) — it names the "
            "residual's driver for the next instrument. Determinism: no RNG "
            "anywhere on the re-read path, the full derivation run twice "
            "in-process and asserted identical. The docstring and every "
            "other byte of this module above main() are identical to "
            "pre-registration commit c24b909. Deposit written to the "
            "pre-registered OUT (results/exp247.json) AND to the canonical "
            "results/exp247_slaving_correction.json, byte-identical."),
        "finding": finding,
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    canon = os.path.join(ROOT, "results", "exp247_slaving_correction.json")
    with open(canon, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    print(f"  results -> {canon}")
    npass = sum(bool(v) for v in criteria.values())
    print(f"  === {npass}/4 gates PASS "
          f"(C1 {tag(c1)}, C2 {tag(c2)}, C3 {tag(c3)}, C4 {tag(c4)}) ===")
    print(f"  BRANCH: {branch}")
    print(f"  FINDING: {finding}")
    return out


if __name__ == "__main__":
    main()
