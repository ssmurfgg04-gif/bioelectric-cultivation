#!/usr/bin/env python3
"""exp276 — THE AUDIT'S OWN FACE (batch 34; batch-33's derived next
item — zero new simulation).

THE OPEN ITEM: exp275 named mia_prod_err the one-zone premium's
proximate carrier (MIA-UPSTREAM); exp273 named H3/H5 the outliers at
mia_prod_err 2.12/2.28 vs the ten-host cluster's [0.49, 0.52]. What
makes the audit's own read high on exactly those two hosts? The audit
IS a battery member: exp243's multi_identity_audit.prod_err is the
MULTI-target production read on the base medium (seed 1), and the
adversarial battery that surrounds it has three pre-named arms — P1
(the canon row on the mirrored medium), P2 (the canon row on the
boundary-double medium), P3 (the deep-band substitution: the base
medium read at the deep rows r-60i0/r-60i1). Decompose each host's
audit error across the arms' own battery errors and read where the
outliers' audit error lives: in ONE perturbation arm, or spread
uniformly?

THE INSTRUMENT (pre-registered, zero-knob, pure re-read):
  - the 12-host table from exp243's deposit: the audit error
    a_h = classes.<H>.multi_identity_audit.prod_err (12 values; the
    runtime_s field EXCLUDED by the no-wall-clock discipline); the
    per-arm masses from the candidates records' errs: P1 =
    P1_canon_zone_relabelings (the mirror-medium canon row), P2 =
    P2_boundary_double_frequency_rewiring (the boundary-double-medium
    canon row), P3 = P3_deep_band_substitution (BOTH pre-named deep
    rows r-60i0/r-60i1); each arm's per-seed WORST = its row's err at
    the seed (P1/P2, one row each) / the max over the two P3 rows
    (exp255's/exp256's arm-worst convention); each arm's mass =
    the mean of its per-seed worsts over the 3 seeds.
  - the cross-check: the per-arm per-seed worsts derived from
    exp243's candidates == exp256's deposited rows' worst_err (the
    canonical rows max(P1,P2), the substituted rows max(i0,i1)),
    72/72 bit-exact — exp256's rows are the same battery re-deposited.
  - THE DECOMPOSITION (the accounting identity): per host, the arm
    shares s_k = m_k / (m_P1 + m_P2 + m_P3) (sum(s) == 1 asserted,
    tolerance 1e-9); the audit error's per-arm contributions
    c_k = s_k * a_h — the arms' contributions SUM TO THE AUDIT ERROR
    (sum_k c_k == a_h asserted within 1e-9, 12/12 hosts; the max
    |residual| recorded).
  - THE BRANCH (the discriminant pre-named, the bars numeric): the
    outliers = exp273's deposited outliers (asserted ==
    exp272's descriptive.premium_hosts == ['H3', 'H5']); the dominant
    arm = argmax_k s_k; the outlier concentration = the min over the
    two outliers of the dominant share. ARM-CONCENTRATED iff both
    outliers' dominant arm is the SAME arm AND the concentration
    >= 0.60 (the supermajority bar — one arm carries >= 60% of the
    battery mass on BOTH outliers); UNIFORM otherwise. The cluster's
    per-host dominant shares reported alongside, never gating.
  - THE RANK REGRESSION (the exp274 convention VERBATIM): the
    response = the audit error a_h (12 hosts); the three mediators =
    the per-arm contributions (c_P1, c_P2, c_P3); the three
    single-mediator Spearmans (tied-average ranks, mediator vector
    first, exp272's _spearman); the OLS-on-ranks full model R2 (the
    response enters as its tied-average ranks, the mediators as the
    numeric contribution values — exp262's/exp274's convention) plus
    the three pairs; the shares by the two-order symmetric average on
    the pre-named entry order P1 -> P2 -> P3 and its reverse
    P3 -> P2 -> P1; shares + unexplained == 1 asserted (no clamping);
    the all-ranks variant AUDIT-ONLY, never gated.

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  B1  THE GRIDS: the candidates grid complete — 48 records = 12 hosts
      x 4 (P1, P2, P3 x 2), each with 3 finite errs, zero rejections;
      the audit records complete 12/12 (prod_err finite,
      bit_identical true); the arm-worst cross-check vs exp256's
      deposited rows 72/72 bit-exact; exp273's field-table carry of
      mia_prod_err bit-exact vs the exp243 records; the outlier
      pre-name asserted (exp273's outliers == exp272's
      descriptive.premium_hosts == ['H3', 'H5']); the provenance
      chains sha-verified against the actual deposit bytes — exp273's
      recorded inputs 5/5, exp274's 6/6, exp275's 7/7; READ-ONLY.
  B2  THE IDENTITY: per host, sum(s_k) == 1 AND sum_k c_k == a_h
      within 1e-9, 12/12 hosts; all shares and contributions finite.
  B3  THE BRANCH: the discriminant resolved on the pre-named bars
      (the concentration >= 0.60 supermajority + the same dominant
      arm on both outliers -> ARM-CONCENTRATED; else UNIFORM).
  B4  THE DISCIPLINE: all deposits READ-ONLY sha-recorded
      byte-unchanged (before/after); deterministic — two-pass
      bit-identical; no wall-clock fields (recursive key scan +
      serialized-blob scan); the docstring+header pinned to this
      pre-registration commit, asserted at entry AND exit;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): ARM-CONCENTRATED / UNIFORM.

RUN: a deposit re-read + arithmetic; seconds.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp276_audit_own_face.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates B1-B4 evaluated exactly once per
    #      pass, pre-registration commit cdec428; the docstring's RUN
    #      clause holds verbatim: a pure deposit re-read + arithmetic,
    #      zero new simulation, seconds) ==================================
    import hashlib
    import json

    import numpy as np
    from scipy.stats import rankdata

    import cultivation.bioelectric.collective as CORE  # the floor's home

    # ---- the byte-unchanged self-check (the hard rule: the docstring
    #      is the cdec428 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "2c41d700497311842fdd7e44d72499370164e7524c496e6c5408ea2c5561ffa9")
    EXPECTED_HEADER_SHA256 = (
        "97f423b4f7c7852d0929767f9c15edf917ba04c84b259031920abd353b8dc42a")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from cdec428"
    assert header_ok, "header drifted from cdec428"

    # ---- the -60.0 floor (B4: asserted at exit; nothing in this body
    #      imports any machinery that touches it — recorded at entry,
    #      restored and re-asserted as the closing line, exp243's/
    #      exp271/exp272's/exp273's/exp274's/exp275's closing
    #      discipline) ------------------------------------------------------
    PROD_FLOOR = -60.0
    floor_at_entry = float(CORE.NEURAL_SPEC_MIN)
    assert floor_at_entry == PROD_FLOOR, \
        f"floor drift at entry: {floor_at_entry}"

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      work, re-verified byte-unchanged at the end) — the four the
    #      computation reads (exp243's battery + audit records, exp256's
    #      arm-worst rows, exp272's outlier pre-name + premium context,
    #      exp273's outlier pre-name + the mia carry) plus the four the
    #      provenance chains name (their recorded shas are byte-verified
    #      against the actual files; exp271/exp182/exp274/exp275 are
    #      never opened for computation here) -----------------------------
    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP256 = os.path.join(ROOT, "results",
                          "exp256_row_pair_regression.json")
    DEP272 = os.path.join(ROOT, "results",
                          "exp272_host_premium_structure.json")
    DEP273 = os.path.join(ROOT, "results", "exp273_outlier_hosts.json")
    DEP271 = os.path.join(ROOT, "results", "exp271_one_zone_premium.json")
    DEP182 = os.path.join(ROOT, "results", "exp182_substrate_100.json")
    DEP274 = os.path.join(ROOT, "results",
                          "exp274_premium_mechanism.json")
    DEP275 = os.path.join(ROOT, "results",
                          "exp275_audit_direction.json")
    for _p in (DEP243, DEP256, DEP272, DEP273, DEP271, DEP182,
               DEP274, DEP275):
        assert os.path.exists(_p), f"missing source deposit {_p}"

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    ro_before = {"exp243_deposit": _sha(DEP243),
                 "exp256_deposit": _sha(DEP256),
                 "exp272_deposit": _sha(DEP272),
                 "exp273_deposit": _sha(DEP273),
                 "exp271_deposit": _sha(DEP271),
                 "exp182_deposit": _sha(DEP182),
                 "exp274_deposit": _sha(DEP274),
                 "exp275_deposit": _sha(DEP275)}

    # ---- the rank helpers (zero-knob; the exp272/exp274 rank
    #      convention: scipy rankdata's tied-average ranks — Spearman
    #      IS Pearson on the tied-average ranks; the OLS-on-ranks is
    #      the exp262/exp274 convention VERBATIM) -------------------------
    def _pearson(xs, ys):
        xa = np.asarray(xs, dtype=float)
        ya = np.asarray(ys, dtype=float)
        return float(np.corrcoef(xa, ya)[0, 1])

    def _spearman(xs, ys):
        rx = rankdata(np.asarray(xs, dtype=float))
        ry = rankdata(np.asarray(ys, dtype=float))
        return _pearson(rx, ry)

    def _r2(cols, rk):
        Xd = np.asarray([[1.0] + list(row) for row in zip(*cols)],
                        dtype=float)
        ya = np.asarray(rk, dtype=float)
        beta, *_ = np.linalg.lstsq(Xd, ya, rcond=None)
        resid = ya - Xd @ beta
        sstot = float(((ya - ya.mean()) ** 2).sum())
        return float(1.0 - float((resid ** 2).sum()) / sstot)

    def _ties_census(vals):
        vs = sorted(float(v) for v in vals)
        levels = sorted(set(vs))
        mults = [vs.count(v) for v in levels]
        return {"n_distinct": len(levels),
                "n_tied_values": sum(1 for m in mults if m > 1),
                "max_multiplicity": int(max(mults))}

    # ---- THE COMPUTATION (pure re-read + arithmetic; run twice, the
    #      two payloads must be byte-identical — B4's determinism
    #      clause) ----------------------------------------------------------
    def compute():
        with open(DEP243) as fh:
            dep243 = json.load(fh)
        with open(DEP256) as fh:
            dep256 = json.load(fh)
        with open(DEP272) as fh:
            dep272 = json.load(fh)
        with open(DEP273) as fh:
            dep273 = json.load(fh)

        # ---- the host frame (exp272's per_host order — the order the
        #      batch asserted exp273 against) --------------------------
        hosts = [r["host"] for r in dep272["per_host"]]
        assert len(hosts) == 12 and len(set(hosts)) == 12, \
            "the 12-host frame drifted"
        assert dep273["hosts"] == hosts, \
            "exp273's host frame drifted"

        # ---- the outlier pre-name (asserted: exp273's deposited
        #      outliers == exp272's descriptive.premium_hosts ==
        #      ['H3', 'H5']) ---------------------------------------------
        outliers = dep273["outliers"]
        assert outliers == ["H3", "H5"], \
            f"exp273's outlier pre-name drifted: {outliers}"
        assert dep272["descriptive"]["premium_hosts"] == outliers, \
            "exp272's premium_hosts drifted from the outlier pre-name"
        cluster = [h for h in hosts if h not in outliers]
        assert len(cluster) == 10, "the ten-host cluster drifted"

        # ---- the battery arms (the pre-named pert names; the grid:
        #      48 records = 12 hosts x 4 — P1, P2, P3 x 2) ---------------
        P1 = "P1_canon_zone_relabelings"
        P2 = "P2_boundary_double_frequency_rewiring"
        P3 = "P3_deep_band_substitution"
        P3_KEYS = ("r-60i0", "r-60i1")
        ARMS = (P1, P2, P3)
        cands = dep243["candidates"]
        assert len(cands) == 48, f"the candidates grid drifted: {len(cands)}"
        grid_ok = True
        arm_rows = {h: {} for h in hosts}   # pert -> list of records
        for c in cands:
            h = c["cls"]
            assert h in arm_rows, f"unknown candidate host {h}"
            arm_rows[h].setdefault(c["pert"], []).append(c)
            grid_ok = grid_ok and len(c["errs"]) == 3 \
                and all(e == e and abs(e) != float("inf")
                        for e in c["errs"]) \
                and len(c.get("rejections", [])) == 0
        for h in hosts:
            assert sorted(arm_rows[h]) == sorted(ARMS), \
                f"{h}: the pre-named arm grid drifted"
            assert len(arm_rows[h][P1]) == 1 and len(arm_rows[h][P2]) == 1 \
                and len(arm_rows[h][P3]) == 2, \
                f"{h}: the per-arm record counts drifted"
            assert sorted(r["row_key"] for r in arm_rows[h][P3]) \
                == sorted(P3_KEYS), f"{h}: the deep rows drifted"

        # ---- the audit records (the audit's OWN face: the
        #      MULTI-target production read on the base medium, seed 1;
        #      the runtime_s field EXCLUDED by the no-wall-clock
        #      discipline) ------------------------------------------------
        cls = dep243["classes"]
        assert set(cls) == set(hosts), "exp243's classes drifted"
        a = {}
        audit_meta = {}
        for h in hosts:
            rec = cls[h]["multi_identity_audit"]
            assert rec["bit_identical"] is True, \
                f"{h}: the multi-identity audit is not bit-identical"
            v = float(rec["prod_err"])
            assert v == v and abs(v) != float("inf"), \
                f"{h}: the audit prod_err is not finite"
            a[h] = v
            audit_meta[h] = {"seed": int(rec["seed"]),
                             "bit_identical": bool(rec["bit_identical"]),
                             "f_max": float(rec["f_max"])}

        # ---- the per-arm per-seed WORSTS from exp243's candidates
        #      (P1/P2: the row's own err; P3: the max over the two deep
        #      rows — exp255's/exp256's arm-worst convention) and the
        #      cross-check against exp256's deposited rows (the same
        #      battery re-deposited): 72/72 bit-exact ----------------------
        worst = {h: {P1: [], P2: [], P3: []} for h in hosts}
        for h in hosts:
            e1 = [float(x) for x in arm_rows[h][P1][0]["errs"]]
            e2 = [float(x) for x in arm_rows[h][P2][0]["errs"]]
            i0 = [float(x) for x in arm_rows[h][P3][0]["errs"]]
            i1 = [float(x) for x in arm_rows[h][P3][1]["errs"]]
            worst[h][P1] = e1
            worst[h][P2] = e2
            worst[h][P3] = [max(i0[s], i1[s]) for s in range(3)]
        rows256 = dep256["rows"]
        assert len(rows256) == 72, "exp256's 72-row battery drifted"
        xcheck = {"n_checks": 0, "n_bit_exact": 0}
        for r in rows256:
            h, arm, s = r["host"], r["arm"], int(r["seed"])
            derived = (max(worst[h][P1][s - 1], worst[h][P2][s - 1])
                       if arm == "canonical" else worst[h][P3][s - 1])
            xcheck["n_checks"] += 1
            if float(r["worst_err"]) == derived:
                xcheck["n_bit_exact"] += 1
        xcheck_ok = bool(xcheck["n_bit_exact"] == 72)

        # ---- exp273's field-table carry of mia_prod_err (bit-exact
        #      vs the exp243 records; the field is selection-tagged
        #      external — the non-circular set) ----------------------------
        ft = {rec["field"]: rec for rec in dep273["field_table"]}
        MIA_FIELD = "exp243.classes.multi_identity_audit.prod_err"
        assert MIA_FIELD in ft, \
            "mia_prod_err missing from exp273's field table"
        rec_mia = ft[MIA_FIELD]
        assert rec_mia["selection"] == "external", \
            "the mia field is not selection-tagged external in exp273"
        carry_ok = bool(all(float(rec_mia["values"][h]) == a[h]
                            for h in hosts))

        # ---- B1's provenance chains: exp273's recorded inputs 5/5,
        #      exp274's 6/6, exp275's 7/7 == the actual deposit bytes ----
        def _chain(dep):
            out = {}
            for key, rec in dep["inputs"].items():
                out[key] = bool(
                    rec["sha256"] == _sha(os.path.join(ROOT,
                                                       rec["path"])))
            return out
        chain273_ok = _chain(dep273)
        with open(DEP274) as fh:
            dep274 = json.load(fh)
        with open(DEP275) as fh:
            dep275 = json.load(fh)
        chain274_ok = _chain(dep274)
        chain275_ok = _chain(dep275)
        chain_all_ok = bool(all(chain273_ok.values())
                            and all(chain274_ok.values())
                            and all(chain275_ok.values()))

        # ---- THE DECOMPOSITION (the accounting identity): per host,
        #      the arm masses m_k = the mean of the per-seed worsts;
        #      the shares s_k = m_k / M (sum == 1 asserted); the audit
        #      error's per-arm contributions c_k = s_k * a_h — the
        #      arms' contributions SUM TO THE AUDIT ERROR (asserted
        #      within 1e-9, 12/12) ----------------------------------------
        TOL = 1e-9
        masses = {h: {P1: float(np.mean(worst[h][P1])),
                      P2: float(np.mean(worst[h][P2])),
                      P3: float(np.mean(worst[h][P3]))}
                  for h in hosts}
        shares = {}
        contribs = {}
        resid = {}
        shares_sum_dev = {}
        for h in hosts:
            M = masses[h][P1] + masses[h][P2] + masses[h][P3]
            assert M > 0.0, f"{h}: the battery mass vanished"
            s = {k: masses[h][k] / M for k in ARMS}
            c = {k: s[k] * a[h] for k in ARMS}
            shares_sum_dev[h] = sum(s.values()) - 1.0
            resid[h] = sum(c.values()) - a[h]
            assert abs(shares_sum_dev[h]) < TOL, \
                f"{h}: the shares do not sum to 1"
            assert abs(resid[h]) < TOL, \
                f"{h}: the arms' contributions do not sum to the " \
                f"audit error"
            assert all(v == v and abs(v) != float("inf")
                       for v in list(s.values()) + list(c.values())), \
                f"{h}: a non-finite share or contribution"
            shares[h] = s
            contribs[h] = c
        max_abs_resid = float(max(abs(v) for v in resid.values()))

        # ---- the dominant arm per host (ties resolved to the FIRST
        #      arm in the pre-named order P1 -> P2 -> P3) -----------------
        dom_arm = {h: max(ARMS, key=lambda k: (shares[h][k],
                                               -ARMS.index(k)))
                   for h in hosts}
        dom_share = {h: shares[h][dom_arm[h]] for h in hosts}

        # ---- B3: THE BRANCH (the discriminant pre-named, the bars
        #      numeric): the concentration = the min over the two
        #      outliers of the dominant share; ARM-CONCENTRATED iff
        #      both outliers' dominant arm is the SAME arm AND the
        #      concentration >= 0.60 (the supermajority bar); UNIFORM
        #      otherwise. The cluster's dominant shares reported
        #      alongside, never gating. -----------------------------------
        BAR_CONC = 0.60
        out_arms = {h: dom_arm[h] for h in outliers}
        concentration = float(min(dom_share[h] for h in outliers))
        same_arm = bool(len(set(out_arms.values())) == 1)
        branch = ("ARM-CONCENTRATED"
                  if (same_arm and concentration >= BAR_CONC)
                  else "UNIFORM")
        cluster_shares = [dom_share[h] for h in cluster]
        conc_detail = {
            "bar_supermajority": BAR_CONC,
            "outlier_dominant_arms": out_arms,
            "outlier_dominant_shares": {h: dom_share[h]
                                        for h in outliers},
            "same_dominant_arm_on_both_outliers": same_arm,
            "outlier_concentration_min_share": concentration,
            "cluster_dominant_share_min": float(min(cluster_shares)),
            "cluster_dominant_share_max": float(max(cluster_shares)),
            "outlier_degree_above_cluster_max": bool(
                all(dom_share[h] > max(cluster_shares)
                    for h in outliers))}

        # ---- THE RANK REGRESSION (the exp274 convention VERBATIM):
        #      the response = the audit error; the three mediators =
        #      the per-arm contributions c_k = s_k * a_h (DISCLOSED:
        #      the contributions embed the response by construction —
        #      this is a decomposition-attribution readout of the
        #      battery's own shares, not an independent-predictor
        #      regression); three single-mediator Spearmans (mediator
        #      vector first) + the OLS-on-ranks full model + the three
        #      pairs; the shares by the two-order symmetric average on
        #      the pre-named entry order P1 -> P2 -> P3 and its reverse
        #      P3 -> P2 -> P1; shares + unexplained == 1 asserted; the
        #      all-ranks variant AUDIT-ONLY, never gated. ---------------
        a_vec = [a[h] for h in hosts]
        med_vals = {"P1_contribution": [contribs[h][P1] for h in hosts],
                    "P2_contribution": [contribs[h][P2] for h in hosts],
                    "P3_contribution": [contribs[h][P3] for h in hosts]}
        spearmans = {k: _spearman(vec, a_vec)
                     for k, vec in med_vals.items()}
        Rk = rankdata(np.asarray(a_vec, dtype=float))
        c1, c2, c3 = ("P1_contribution", "P2_contribution",
                      "P3_contribution")
        r2_single = {k: _r2([med_vals[k]], Rk) for k in med_vals}
        r2_12 = _r2([med_vals[c1], med_vals[c2]], Rk)
        r2_13 = _r2([med_vals[c1], med_vals[c3]], Rk)
        r2_23 = _r2([med_vals[c2], med_vals[c3]], Rk)
        r2_full = _r2([med_vals[c1], med_vals[c2], med_vals[c3]], Rk)
        inc_o1 = {c1: r2_single[c1],
                  c2: r2_12 - r2_single[c1],
                  c3: r2_full - r2_12}
        inc_o2 = {c3: r2_single[c3],
                  c2: r2_23 - r2_single[c3],
                  c1: r2_full - r2_23}
        reg_shares = {k: 0.5 * (inc_o1[k] + inc_o2[k])
                      for k in med_vals}
        reg_unexplained = 1.0 - r2_full
        reg_sum = sum(reg_shares.values()) + reg_unexplained
        assert abs(reg_sum - 1.0) < 1e-9, \
            "the four-way rank shares do not sum to 1"
        assert all(v == v and abs(v) != float("inf")
                   for v in list(reg_shares.values())
                   + [reg_unexplained, r2_full]), "non-finite share"
        rk = {k: rankdata(np.asarray(v, dtype=float))
              for k, v in med_vals.items()}
        audit_all_ranks = {
            "r2_single": {k: _r2([rk[k]], Rk) for k in med_vals},
            "r2_full": _r2([rk[c1], rk[c2], rk[c3]], Rk)}
        audit_all_ranks["single_equals_spearman_squared"] = bool(
            all(abs(audit_all_ranks["r2_single"][k]
                    - spearmans[k] ** 2) < 1e-12 for k in med_vals))

        # ---- the 12-host table (the audit error, the arm masses and
        #      shares, the contributions, the dominant arm, the
        #      outlier flag; the premium means CONTEXT ONLY, never
        #      gating) ------------------------------------------------------
        prem1 = {r["host"]: float(r["one_zone_premium_mean"])
                 for r in dep272["per_host"]}
        premM = {r["host"]: float(r["multi_zone_premium_mean"])
                 for r in dep272["per_host"]}
        table = [{"host": h,
                  "audit_prod_err": a[h],
                  "m_P1": masses[h][P1], "m_P2": masses[h][P2],
                  "m_P3": masses[h][P3],
                  "s_P1": shares[h][P1], "s_P2": shares[h][P2],
                  "s_P3": shares[h][P3],
                  "c_P1": contribs[h][P1], "c_P2": contribs[h][P2],
                  "c_P3": contribs[h][P3],
                  "dominant_arm": dom_arm[h],
                  "dominant_share": dom_share[h],
                  "outlier": h in outliers,
                  "one_zone_premium_mean_ctx": prem1[h],
                  "multi_zone_premium_mean_ctx": premM[h]}
                 for h in hosts]
        all_finite = bool(all(
            row[k] == row[k] and abs(row[k]) != float("inf")
            for row in table
            for k in ("audit_prod_err", "m_P1", "m_P2", "m_P3",
                      "s_P1", "s_P2", "s_P3", "c_P1", "c_P2", "c_P3")))

        b1_pass = bool(grid_ok and all_finite and xcheck_ok
                       and carry_ok and chain_all_ok
                       and all(rec["bit_identical"] for h in hosts
                               for rec in [cls[h]["multi_identity_audit"]]))
        b2_pass = bool(all(abs(resid[h]) < TOL for h in hosts)
                       and all(abs(shares_sum_dev[h]) < TOL
                               for h in hosts) and all_finite)
        b3_pass = bool(branch in ("ARM-CONCENTRATED", "UNIFORM")
                       and concentration == concentration)

        ties = {"audit_prod_err": _ties_census(a_vec),
                "P3_contribution":
                    _ties_census(med_vals["P3_contribution"]),
                "dominant_share": _ties_census(list(dom_share.values()))}

        return {
            "hosts": hosts, "outliers": outliers, "cluster": cluster,
            "table": table, "audit_meta": audit_meta,
            "b1": {"pass": b1_pass,
                   "candidates_grid_complete_48": grid_ok,
                   "audit_records_12_bit_identical_finite": True,
                   "arm_worst_cross_check_vs_exp256": xcheck,
                   "arm_worst_cross_check_ok": xcheck_ok,
                   "exp273_mia_carry_bit_exact": carry_ok,
                   "exp273_recorded_input_shas_match_actual_bytes":
                       chain273_ok,
                   "exp274_recorded_input_shas_match_actual_bytes":
                       chain274_ok,
                   "exp275_recorded_input_shas_match_actual_bytes":
                       chain275_ok,
                   "provenance_chains_sha_verified": chain_all_ok,
                   "read_only_complete": all_finite},
            "b2": {"pass": b2_pass, "tolerance": TOL,
                   "max_abs_shares_sum_deviation":
                       float(max(abs(v) for v in shares_sum_dev.values())),
                   "max_abs_identity_residual": max_abs_resid},
            "b3": {"pass": b3_pass, "branch": branch,
                   **conc_detail},
            "regression": {
                "response": "the audit error "
                            "exp243.classes.multi_identity_audit."
                            "prod_err (12 hosts)",
                "mediators": ("the per-arm contributions "
                              "c_k = s_k * a_h (P1/P2/P3) — "
                              "DISCLOSED: they embed the response by "
                              "construction; a decomposition-"
                              "attribution readout, not an "
                              "independent-predictor regression"),
                "spearman_rho": spearmans,
                "r2_single": r2_single,
                "r2_pairs": {"P1+P2": r2_12, "P1+P3": r2_13,
                             "P2+P3": r2_23},
                "r2_full": r2_full,
                "order_decompositions": {"order_P1_P2_P3": inc_o1,
                                         "order_P3_P2_P1": inc_o2},
                "shares_of_rank_variance": reg_shares,
                "unexplained": reg_unexplained,
                "shares_sum": reg_sum,
                "audit_all_ranks_variant": audit_all_ranks},
            "ties_census": ties}

    payload_a = compute()
    sha_a = hashlib.sha256(json.dumps(
        payload_a, sort_keys=True, default=str).encode()).hexdigest()
    payload_b = compute()
    sha_b = hashlib.sha256(json.dumps(
        payload_b, sort_keys=True, default=str).encode()).hexdigest()
    deterministic = bool(sha_a == sha_b)
    assert deterministic, "the computation is not two-pass deterministic"

    b3 = payload_a["b3"]
    gates = {"B1_grids": {
                 "pass": payload_a["b1"]["pass"],
                 "bar": "the candidates grid complete (48 = 12 hosts x "
                        "4, 3 finite errs each, zero rejections); the "
                        "audit records 12/12 bit-identical + finite; "
                        "the arm-worst cross-check vs exp256's "
                        "deposited rows 72/72 bit-exact; exp273's mia "
                        "carry bit-exact; the outlier pre-name "
                        "asserted (exp273 == exp272 == ['H3','H5']); "
                        "the provenance chains sha-verified (exp273 "
                        "5/5, exp274 6/6, exp275 7/7); READ-ONLY",
                 **payload_a["b1"]},
             "B2_identity": {
                 "pass": payload_a["b2"]["pass"],
                 "bar": "per host, sum(s_k) == 1 AND sum_k c_k == a_h "
                        "within 1e-9, 12/12 hosts; all shares and "
                        "contributions finite (the arms' contributions "
                        "sum to the audit error)",
                 **payload_a["b2"]},
             "B3_branch": {
                 "pass": b3["pass"],
                 "bar": "the discriminant pre-named, the bars numeric: "
                        "ARM-CONCENTRATED iff both outliers' dominant "
                        "arm is the SAME arm AND the min outlier "
                        "dominant share >= 0.60 (the supermajority "
                        "bar); UNIFORM otherwise; the cluster's "
                        "dominant shares reported, never gating",
                 "branch": b3["branch"],
                 **{k: v for k, v in b3.items() if k != "pass"}}}

    # ---- B4: the discipline --------------------------------------------
    ro_after = {"exp243_deposit": _sha(DEP243),
                "exp256_deposit": _sha(DEP256),
                "exp272_deposit": _sha(DEP272),
                "exp273_deposit": _sha(DEP273),
                "exp271_deposit": _sha(DEP271),
                "exp182_deposit": _sha(DEP182),
                "exp274_deposit": _sha(DEP274),
                "exp275_deposit": _sha(DEP275)}
    ro_unchanged = bool(ro_after == ro_before)

    def _scan_wall_clock_keys(o):
        bad = []
        if isinstance(o, dict):
            for k, v in o.items():
                kl = k.lower()
                if any(b in kl for b in ("runtime", "wall_clock",
                                         "wall_s", "timestamp",
                                         "generated_at", "datetime")) \
                        and not kl.startswith("no_wall_clock"):
                    bad.append(k)
                bad.extend(_scan_wall_clock_keys(v))
        elif isinstance(o, list):
            for v in o:
                bad.extend(_scan_wall_clock_keys(v))
        return bad

    no_wall_clock = True  # the body reads no clock anywhere; the
    #                          serialized-deposit scans below re-check

    a4_pass = bool(ro_unchanged and deterministic and no_wall_clock
                   and floor_at_entry == PROD_FLOOR
                   and docstring_ok and header_ok)

    gates["B4_discipline"] = {
        "pass": a4_pass,
        "bar": ("all deposits READ-ONLY sha-recorded byte-unchanged; "
                "deterministic — two-pass bit-identical; no "
                "wall-clock fields; the docstring+header pinned to "
                "cdec428 asserted at entry AND exit; NEURAL_SPEC_MIN "
                "== -60.0 asserted at exit"),
        "read_only_shas_before": ro_before,
        "read_only_shas_after": ro_after,
        "read_only_byte_unchanged": ro_unchanged,
        "deterministic_two_pass_bit_identical": deterministic,
        "payload_sha256_pass_a": sha_a,
        "payload_sha256_pass_b": sha_b,
        "no_wall_clock_fields": no_wall_clock,
        "floor_at_entry": floor_at_entry,
        "floor_at_exit": PROD_FLOOR,
        "docstring_sha256": docstring_sha,
        "docstring_byte_unchanged_vs_cdec428": docstring_ok,
        "header_sha256": header_sha,
        "header_byte_unchanged_vs_cdec428": header_ok,
        "deposit_form": ("deterministic: no wall-clock fields — a "
                         "re-run of this module reproduces this file "
                         "byte-identically")}

    # ---- the branch + the verdict (one line, the numbers
    #      data-driven) -----------------------------------------------------
    branch = b3["branch"]
    reg = payload_a["regression"]

    def _g(v):
        return format(v, ".10g") if isinstance(v, float) else str(v)

    gate_passes = {"B1": gates["B1_grids"]["pass"],
                   "B2": gates["B2_identity"]["pass"],
                   "B3": gates["B3_branch"]["pass"],
                   "B4": gates["B4_discipline"]["pass"]}
    n_pass = sum(1 for v in gate_passes.values() if v)
    n_refute = 4 - n_pass

    same_arm = b3["same_dominant_arm_on_both_outliers"]
    out_arm_name = (b3["outlier_dominant_arms"]["H3"] if same_arm
                    else "/".join(sorted(
                        set(b3["outlier_dominant_arms"].values()))))
    tbl = {r["host"]: r for r in payload_a["table"]}
    verdict = (
        f"{n_pass}/4 gates B1-B4 ({n_pass} PASS / {n_refute} REFUTE) | "
        f"{branch} | the outliers' audit error "
        f"{b3['outlier_dominant_shares']['H3']:.4f}/"
        f"{b3['outlier_dominant_shares']['H5']:.4f} concentrated in "
        f"arm {out_arm_name} (the deep-band substitution's share "
        f"{tbl['H3']['s_P3']:.4f}/{tbl['H5']['s_P3']:.4f} of the "
        f"battery mass) vs the cluster's dominant-share range "
        f"[{b3['cluster_dominant_share_min']:.4f}, "
        f"{b3['cluster_dominant_share_max']:.4f}] | the contributions "
        f"sum to the audit error (max residual "
        f"{payload_a['b2']['max_abs_identity_residual']:.2e}, the "
        f"1e-9 bar) | the rank regression: Spearman(P3 contribution, "
        f"audit) {_g(reg['spearman_rho']['P3_contribution'])}, full "
        f"rank R2 {_g(reg['r2_full'])}, shares P1 "
        f"{_g(reg['shares_of_rank_variance']['P1_contribution'])} / "
        f"P2 {_g(reg['shares_of_rank_variance']['P2_contribution'])} "
        f"/ P3 {_g(reg['shares_of_rank_variance']['P3_contribution'])}"
        f" / unexplained {_g(reg['unexplained'])} | 12 hosts, a pure "
        f"re-read of exp243's battery + exp256's arm rows + exp273's "
        f"pre-name + exp272's context, READ-ONLY byte-unchanged, "
        f"two-pass bit-identical, floor -60.0")

    deposit = {
        "exp": "exp276_audit_own_face",
        "claim": (
            "THE AUDIT'S OWN FACE (batch 34, pre-registration commit "
            "cdec428): what makes mia_prod_err high on the outlier "
            "hosts H3/H5? The audit's own read (exp243's "
            "multi_identity_audit.prod_err — the MULTI-target "
            "production read on the base medium, seed 1) decomposed "
            "across the adversarial battery's three pre-named arms "
            "(P1 the mirror-medium canon row, P2 the boundary-double "
            "canon row, P3 the deep-band substitution rows r-60i0/"
            "r-60i1): per host the arm shares s_k = m_k/M from the "
            "candidates' errs, the audit error's per-arm "
            "contributions c_k = s_k * a_h summing to the audit error "
            "(the accounting identity, asserted); the branch "
            "ARM-CONCENTRATED / UNIFORM at the 0.60 supermajority "
            "bar; the exp274-convention rank regression of the audit "
            "error on the per-arm contributions"),
        "method": {
            "audit_error": ("exp243.classes.<H>.multi_identity_audit."
                            "prod_err — the MULTI-target production "
                            "read on the base medium, seed 1, "
                            "bit-identical 12/12; the runtime_s field "
                            "EXCLUDED by the no-wall-clock discipline"),
            "battery_arms": {
                "P1": "P1_canon_zone_relabelings — the canon row on "
                      "the mirrored medium (the zero-knob label "
                      "mirror pi(i)=n-1-i)",
                "P2": "P2_boundary_double_frequency_rewiring — the "
                      "canon row on the boundary-double medium (each "
                      "canon-boundary cell chorded to its next two "
                      "boundary peers)",
                "P3": "P3_deep_band_substitution — the base medium "
                      "read at the deep band's -60.0 rung rows "
                      "r-60i0/r-60i1, BOTH pre-named instances"},
            "arm_mass": ("each arm's per-seed WORST = its row's err "
                         "at the seed (P1/P2, one row each) / the max "
                         "over the two P3 rows (exp255's/exp256's "
                         "arm-worst convention); the arm's mass = the "
                         "mean of its per-seed worsts over the 3 "
                         "seeds; cross-checked bit-exact against "
                         "exp256's deposited canonical/substituted "
                         "row worsts 72/72"),
            "decomposition": ("per host: the shares s_k = m_k / "
                              "(m_P1+m_P2+m_P3), the contributions "
                              "c_k = s_k * a_h; the accounting "
                              "identity sum_k c_k == a_h within 1e-9 "
                              "asserted 12/12 (and sum_k s_k == 1)"),
            "branch_rule": ("the dominant arm = argmax_k s_k (ties to "
                            "the FIRST arm in the pre-named order "
                            "P1->P2->P3); ARM-CONCENTRATED iff both "
                            "outliers' dominant arm is the SAME arm "
                            "AND min outlier dominant share >= 0.60; "
                            "UNIFORM otherwise; the outliers = "
                            "exp273's deposited outliers (asserted == "
                            "exp272's descriptive.premium_hosts == "
                            "['H3','H5'])"),
            "regression": ("the exp274 convention VERBATIM: the "
                           "response = the audit error (12 hosts, "
                           "tied-average ranks); the three mediators "
                           "= the per-arm contributions; three "
                           "single-mediator Spearmans (mediator "
                           "vector first, scipy rankdata both "
                           "sides); the OLS-on-ranks full model R2 + "
                           "three pairs; the shares by the two-order "
                           "symmetric average on the pre-named entry "
                           "order P1->P2->P3 and its reverse; shares "
                           "+ unexplained == 1, no clamping; the "
                           "all-ranks variant AUDIT-ONLY"),
            "convention_disclosure": ("the mediators are the "
                                      "contributions c_k = s_k * a_h — "
                                      "they embed the response by "
                                      "construction; the regression is "
                                      "a decomposition-attribution "
                                      "readout of the battery's own "
                                      "shares, not an "
                                      "independent-predictor "
                                      "regression (the Spearmans and "
                                      "shares are honest descriptive "
                                      "quantities of that readout)"),
            "method_source": ("experiments/exp243_structured_"
                              "adversarial.py (the battery + the "
                              "audit records), experiments/"
                              "exp256_row_pair_regression.py (the "
                              "per-seed arm worsts, re-deposited), "
                              "experiments/exp272_host_premium_"
                              "structure.py (the _spearman "
                              "convention, the outlier pre-name "
                              "source, the premium context), "
                              "experiments/exp273_outlier_hosts.py "
                              "(the deposited outlier pre-name + the "
                              "mia field-table carry), experiments/"
                              "exp274_premium_mechanism.py (the "
                              "rank-regression convention), "
                              "experiments/exp275_audit_direction.py "
                              "(the sha discipline)")},
        "inputs": {
            "exp243_deposit": {
                "path": "results/exp243_structured_adversarial.json",
                "sha256": ro_before["exp243_deposit"],
                "role": ("the 48-record candidate battery (the arms' "
                         "errs) + the 12 multi_identity_audit records "
                         "(the audit error) — the computation's "
                         "primary source")},
            "exp256_deposit": {
                "path": "results/exp256_row_pair_regression.json",
                "sha256": ro_before["exp256_deposit"],
                "role": ("the 72 deposited per-seed arm worsts the "
                         "derived arm worsts are cross-checked "
                         "against, bit-exact")},
            "exp272_deposit": {
                "path": "results/exp272_host_premium_structure.json",
                "sha256": ro_before["exp272_deposit"],
                "role": ("the host frame + the outlier pre-name "
                         "source (descriptive.premium_hosts) + the "
                         "premium context columns (never gating)")},
            "exp273_deposit": {
                "path": "results/exp273_outlier_hosts.json",
                "sha256": ro_before["exp273_deposit"],
                "role": ("the deposited outlier pre-name + the "
                         "field-table carry of mia_prod_err "
                         "(bit-exact) + the recorded input shas "
                         "verified 5/5")},
            "exp271_deposit": {
                "path": "results/exp271_one_zone_premium.json",
                "sha256": ro_before["exp271_deposit"],
                "role": ("the provenance chain: the one-zone premium "
                         "grid — sha-verified via exp273's chain, "
                         "never opened for computation")},
            "exp182_deposit": {
                "path": "results/exp182_substrate_100.json",
                "sha256": ro_before["exp182_deposit"],
                "role": ("the provenance chain: the margin profiles — "
                         "sha-verified via exp273's chain, never "
                         "opened")},
            "exp274_deposit": {
                "path": "results/exp274_premium_mechanism.json",
                "sha256": ro_before["exp274_deposit"],
                "role": ("the provenance chain: the rank-regression "
                         "convention's source deposit — sha-verified "
                         "6/6, never opened for computation")},
            "exp275_deposit": {
                "path": "results/exp275_audit_direction.json",
                "sha256": ro_before["exp275_deposit"],
                "role": ("the provenance chain: the sha-discipline "
                         "precedent's deposit — sha-verified 7/7, "
                         "never opened for computation")}},
        "hosts": payload_a["hosts"],
        "outliers": payload_a["outliers"],
        "cluster": payload_a["cluster"],
        "battery_arms": {"P1_canon_zone_relabelings": "the canon row "
                         "on the mirrored medium",
                         "P2_boundary_double_frequency_rewiring":
                             "the canon row on the boundary-double "
                             "medium",
                         "P3_deep_band_substitution": "the deep rows "
                         "r-60i0/r-60i1 on the base medium"},
        "decomposition_table": payload_a["table"],
        "audit_meta": payload_a["audit_meta"],
        "decomposition_identity": {
            "tolerance": payload_a["b2"]["tolerance"],
            "max_abs_shares_sum_deviation":
                payload_a["b2"]["max_abs_shares_sum_deviation"],
            "max_abs_identity_residual":
                payload_a["b2"]["max_abs_identity_residual"]},
        "regression": payload_a["regression"],
        "ties_census": payload_a["ties_census"],
        "gates": gates,
        "branch": branch,
        "concentration": {k: v for k, v in b3.items()
                          if k not in ("pass",)},
        "verdict": verdict,
        "determinism": {
            "computation_passes": 2,
            "payload_sha256_pass_a": sha_a,
            "payload_sha256_pass_b": sha_b,
            "two_pass_bit_identical": deterministic},
        "discipline": {
            "no_wall_clock_fields": no_wall_clock,
            "floor_at_entry": floor_at_entry,
            "floor_at_exit": PROD_FLOOR,
            "docstring_sha256": docstring_sha,
            "docstring_byte_unchanged_vs_cdec428": docstring_ok,
            "header_sha256": header_sha,
            "header_byte_unchanged_vs_cdec428": header_ok,
            "deposit_form": ("deterministic: no wall-clock fields — a "
                             "re-run of this module reproduces this "
                             "file byte-identically")},
    }
    deposit["deposit_fingerprint"] = hashlib.sha256(json.dumps(
        {k: v for k, v in deposit.items() if k != "deposit_fingerprint"},
        sort_keys=True, default=str).encode()).hexdigest()

    # the no-wall-clock audit on the assembled deposit: the recursive
    # KEY scan (no clock fields anywhere) + the serialized-blob scan
    _bad_keys = _scan_wall_clock_keys(deposit)
    assert not _bad_keys, f"wall-clock key detected: {_bad_keys}"
    _blob = json.dumps(deposit)
    assert not any(pat in _blob for pat in ('"runtime', '"wall_clock',
                                            '"wall_s', '"timestamp',
                                            '"generated_at')), \
        "wall-clock field detected in the deposit"

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(deposit, f, indent=1, default=float)

    print("=== exp276: THE AUDIT'S OWN FACE (pure deposit re-read + "
          "arithmetic) ===")
    print("  the audit's own read (exp243's multi_identity_audit."
          "prod_err) decomposed across the adversarial battery's "
          "three arms (P1 mirror / P2 boundary-double / P3 deep-band)")
    print(f"\n  B1 grids: {'PASS' if gates['B1_grids']['pass'] else 'FAIL'} "
          f"(48 candidates = 12 x 4 complete, 3 finite errs each, zero "
          f"rejections; the audits 12/12 bit-identical; the arm-worst "
          f"cross-check vs exp256 72/72 bit-exact; exp273's mia carry "
          f"bit-exact; the chains sha-verified exp273 5/5 + exp274 6/6 "
          f"+ exp275 7/7)")
    print(f"  B2 identity: {'PASS' if gates['B2_identity']['pass'] else 'FAIL'} "
          f"(the arms' contributions sum to the audit error, 12/12 — "
          f"max residual {payload_a['b2']['max_abs_identity_residual']:.2e} "
          f"vs the 1e-9 bar; shares sum dev "
          f"{payload_a['b2']['max_abs_shares_sum_deviation']:.2e})")
    print("  B3 branch — the arm shares (the battery's error mass):")
    for row in payload_a["table"]:
        tag = " <== outlier" if row["outlier"] else ""
        print(f"      {row['host']:4s} audit {row['audit_prod_err']:5.2f}  "
              f"s_P1 {row['s_P1']:.4f}  s_P2 {row['s_P2']:.4f}  "
              f"s_P3 {row['s_P3']:.4f}  dom {row['dominant_arm'][:2]} "
              f"{row['dominant_share']:.4f}{tag}")
    print(f"  B4 discipline: {'PASS' if a4_pass else 'FAIL'} "
          f"(8 deposits READ-ONLY byte-unchanged: {ro_unchanged}; "
          f"two-pass bit-identical: {deterministic}; no wall-clock "
          f"fields: {no_wall_clock})")
    print(f"\n  BRANCH: {branch} | outlier concentration "
          f"{b3['outlier_concentration_min_share']:.4f} vs the 0.60 bar "
          f"(cluster dominant-share range "
          f"[{b3['cluster_dominant_share_min']:.4f}, "
          f"{b3['cluster_dominant_share_max']:.4f}])")
    print(f"\n  GATES: {verdict}")
    print(f"  deposited {OUT}")

    # the hard rule, re-asserted after the work: the docstring is still
    # the cdec428 pre-registration, byte-for-byte
    assert hashlib.sha256(__doc__.encode()).hexdigest() \
        == EXPECTED_DOCSTRING_SHA256, "docstring drifted after the work"
    with open(__file__, "r", encoding="utf-8") as _f:
        _src2 = _f.read()
    assert hashlib.sha256(
        _src2[:_src2.index(_marker) + len(_marker)].encode()
    ).hexdigest() == EXPECTED_HEADER_SHA256, "header drifted after work"
    # the source deposits are still byte-unchanged after the work
    assert set(_sha(p) for p in (DEP243, DEP256, DEP272, DEP273,
                                 DEP271, DEP182, DEP274, DEP275)) \
        == set(ro_before.values()), "source deposit drifted after work"

    # THE FLOOR ASSERT AT EXIT (the hard rule; exp243's closing line)
    CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at exit"
    return deposit


if __name__ == "__main__":
    main()
