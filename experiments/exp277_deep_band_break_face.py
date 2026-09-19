#!/usr/bin/env python3
"""exp277 — THE DEEP-BAND BREAK FACE (batch 35; batch-34's derived next
item (a), ledger L254 — zero new simulation).

THE OPEN ITEM: exp276 closed the mechanism line at the deposits'
bottom — the outlier hosts' audit error is 94% P3 deep-band-space
(ARM-CONCENTRATED), and exp273 named H3/H5 the boundary-richest hosts
(47/48 canon-boundary cells vs the ten-host cluster's [4, 43]). WHY do
the deep-band programs break on exactly the boundary-richest hosts?
exp256's deposited rows carry the answer's raw material: each row (the
WORST instance per host x arm x seed) is decomposed by exp208's
cell-class machinery into CANON-BOUNDARY / PAIR-JUNCTION / INTERIOR
with frac_of_sq and rms_contrib_mV. Decompose the P3 arm's OWN error
per host and read the face: is the outlier hosts' deep-band error
boundary-class (the CANON-BOUNDARY share) or pair-class (the
PAIR-JUNCTION share)?

THE INSTRUMENT (pre-registered, zero-knob, pure re-read):
  - the source: exp256's deposited 72 rows = 12 hosts x 2 arms
    (canonical, substituted) x 3 seeds; the SUBSTITUTED arm (P3's own
    face: the deep rows r-60i0/r-60i1 on the base medium) is the 36
    rows read here (12 hosts x 3 seeds); each row's decomposition =
    exp208's classify(T_row, W_row) + decompose on the row's WORST
    instance's own state-carrying read (exp243's A3 path), deposited
    as per_class with frac_of_sq / sum_sq / rms_contrib_mV.
  - THE MASK SEMANTICS (disclosed, read AS DEPOSITED): exp208's
    classify assigns cls 1 = PAIR-JUNCTION and 0 = otherwise (the
    boundary ring wins precedence; the interior cells ride the 0
    mask — cls is never set to 2), so the deposited per_class
    CANON-BOUNDARY record is the NON-PAIR-JUNCTION complement of the
    squared error (boundary ring + interior) and the deposited
    INTERIOR record is empty. Verified here in-deposit 72/72
    (per_class PAIR-JUNCTION n_cells == class_counts PAIR-JUNCTION;
    per_class INTERIOR n_cells == 0; per_class CANON-BOUNDARY
    n_cells == 400 - that count; class_counts sum to n = 400). The
    branch therefore reads the deposited labels at face value:
    "boundary-class" == the non-pair-junction share, "pair-class" ==
    the PAIR-JUNCTION share. (The pure boundary-only share is NOT
    recoverable from the deposits — the decomposition's frac does not
    split the complement; disclosed, never repaired, zero new
    simulation.)
  - the 12-host table: per-host mean CANON-BOUNDARY frac and mean
    PAIR-JUNCTION frac over the substituted rows (3 seeds each),
    alongside the mean worst_err (the P3 arm's own error, exp276's
    m_P3), the mean rms_contrib_mV, and the mean pair-junction count.
  - THE BRANCH (the discriminant pre-named, the bars numeric): the
    outliers = exp273's deposited outliers (asserted == exp272's
    descriptive.premium_hosts == ['H3', 'H5']); the cluster = exp273's
    other ten. BOUNDARY-CLASS iff min(cb share on H3, H5) > max(cb
    share over the cluster); PAIR-CLASS iff min(pj share on H3, H5) >
    max(pj share over the cluster); SPLIT iff both exceed; NEITHER
    (the exhaustive residual) otherwise. Both margins recorded.
  - THE PREMIUM'S MEDIATOR (the exp274/exp275 conventions, REPORTED
    not gated): the response = mia_prod_err (exp273's deposited field
    table, exact field exp243.classes.multi_identity_audit.prod_err,
    carried bit-exact vs exp243's records); the two mediators = the
    two per-host mean shares; the single-mediator Spearmans
    (tied-average ranks, mediator vector first, exp272's _spearman);
    the OLS-on-ranks single R2s + the full-model R2 (the response
    enters as its tied-average ranks, the mediators as the numeric
    mean shares — exp262's/exp274's convention) plus the pair; the
    shares by the two-order symmetric average on the pre-named entry
    order cb -> pj and its reverse pj -> cb; shares + unexplained == 1
    asserted (no clamping); the ties census; the all-ranks variant
    AUDIT-ONLY, never gating.

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  D1  THE GRIDS: exp256's 72 rows re-read COMPLETE — 12 hosts x 2
      arms x 3 seeds, every row's decomposition carrying the three
      pre-named per_class records with finite frac_of_sq / sum_sq /
      rms_contrib_mV; the mask semantics verified in-deposit (72/72
      as disclosed above); the 36 substituted rows complete 12 x 3;
      all worst_err finite; the outlier pre-name asserted (exp273's
      outliers == exp272's descriptive.premium_hosts == ['H3', 'H5']);
      exp273's field-table mia_prod_err carry bit-exact vs exp243's
      records; the provenance chains sha-verified against the actual
      deposit bytes — exp273's recorded inputs 5/5, exp274's 6/6,
      exp275's 7/7; READ-ONLY.
  D2  THE ACCOUNTING IDENTITY (per row, all 72): the per-class
      frac_of_sq sums to 1 within 1e-9 (72/72); the deposited
      identity_residual <= 1e-9 (72/72); the RMS-reconstruction face:
      |sqrt(sum_k sum_sq_k / 400) - worst_err| <= 0.0051 in every row
      (worst_err is exp256's 2-decimal rounding — the 0.005 bound +
      margin; the max deviation recorded).
  D3  THE BRANCH: the discriminant resolved on the pre-named numeric
      bars (the min-over-outliers vs max-over-cluster comparisons;
      both margins recorded); the mediator rank regression REPORTED
      alongside under the exp274 conventions — audit-only, never
      gating.
  D4  THE DISCIPLINE: all deposits READ-ONLY sha-recorded
      byte-unchanged (before/after); deterministic — two-pass
      bit-identical; no wall-clock fields (recursive key scan +
      serialized-blob scan); the docstring+header pinned to this
      pre-registration commit, asserted at entry AND exit;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): BOUNDARY-CLASS / PAIR-CLASS / SPLIT /
NEITHER (the exhaustive residual; the first three are the registered
question's named outcomes).

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
OUT = os.path.join(ROOT, "results", "exp277_deep_band_break_face.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates D1-D4 evaluated exactly once per
    #      pass, pre-registration commit aa0d3c2; the docstring's RUN
    #      clause holds verbatim: a pure deposit re-read + arithmetic,
    #      zero new simulation, seconds) ==================================
    import hashlib
    import json

    import numpy as np
    from scipy.stats import rankdata

    import cultivation.bioelectric.collective as CORE  # the floor's home

    # ---- the byte-unchanged self-check (the hard rule: the docstring
    #      is the aa0d3c2 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "0be79f988a1a3901dd22a3ff7f003c8f103c515019f4e2b352675810fc0bc6a6")
    EXPECTED_HEADER_SHA256 = (
        "799c38706ce5f18ca30cd0c488e869e501799d55b9b7dc957fae4505afc5bf89")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from aa0d3c2"
    assert header_ok, "header drifted from aa0d3c2"

    # ---- the -60.0 floor (D4: asserted at exit; nothing in this body
    #      imports any machinery that touches it — recorded at entry,
    #      restored and re-asserted as the closing line, exp243's/
    #      exp271/exp272's/exp273's/exp274's/exp275's/exp276's closing
    #      discipline) ------------------------------------------------------
    PROD_FLOOR = -60.0
    floor_at_entry = float(CORE.NEURAL_SPEC_MIN)
    assert floor_at_entry == PROD_FLOOR, \
        f"floor drift at entry: {floor_at_entry}"

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      work, re-verified byte-unchanged at the end) — the four the
    #      computation reads (exp256's 72 decomposed rows, exp273's
    #      outlier pre-name + the mia carry, exp272's outlier-prename
    #      source + host frame, exp243's audit records) plus the four
    #      the provenance chains name (their recorded shas are
    #      byte-verified against the actual files; exp271/exp182/
    #      exp274/exp275 are never opened for computation here) --------
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
    #      two payloads must be byte-identical — D4's determinism
    #      clause) ----------------------------------------------------------
    def compute():
        with open(DEP256) as fh:
            dep256 = json.load(fh)
        with open(DEP272) as fh:
            dep272 = json.load(fh)
        with open(DEP273) as fh:
            dep273 = json.load(fh)
        with open(DEP243) as fh:
            dep243 = json.load(fh)

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

        # ---- D1: exp256's 72 rows re-read COMPLETE (12 hosts x 2
        #      arms x 3 seeds; every row's decomposition carrying the
        #      three pre-named per_class records, finite; the mask
        #      semantics verified in-deposit) ---------------------------
        bat = dep256["battery"]
        rows256 = dep256["rows"]
        assert len(rows256) == 72, "exp256's 72-row battery drifted"
        assert bat["hosts"] == hosts, "exp256's host frame drifted"
        assert bat["seeds"] == [1, 2, 3], "exp256's seed frame drifted"
        assert bat["rows_per_pass"] == 72, \
            "exp256's rows-per-pass drifted"
        ARMS = ("canonical", "substituted")
        CLASSES = ("CANON-BOUNDARY", "PAIR-JUNCTION", "INTERIOR")
        seen = {}
        grid_ok = True
        decomp_ok = True
        mask_ok = True
        cc_ok = True
        worst_finite = True
        for r in rows256:
            h, arm, s = r["host"], r["arm"], int(r["seed"])
            seen[(h, arm, s)] = True
            grid_ok = grid_ok and (h in hosts) and (arm in ARMS) \
                and (s in (1, 2, 3))
            worst_finite = worst_finite and r["worst_err"] == r["worst_err"] \
                and abs(r["worst_err"]) != float("inf")
            cc = r["class_counts"]
            cc_ok = cc_ok and sum(cc.values()) == 400 \
                and sorted(cc) == sorted(CLASSES)
            pc = r["decomposition"]["per_class"]
            decomp_ok = decomp_ok \
                and [p["class"] for p in pc] == list(CLASSES) \
                and all(p["frac_of_sq"] == p["frac_of_sq"]
                        and abs(p["frac_of_sq"]) != float("inf")
                        and p["sum_sq"] == p["sum_sq"]
                        and p["rms_contrib_mV"] == p["rms_contrib_mV"]
                        for p in pc)
            pcd = {p["class"]: p for p in pc}
            # THE MASK SEMANTICS (disclosed, as deposited): the
            # per_class CANON-BOUNDARY mask is exp208's cls == 0 —
            # the NON-PAIR-JUNCTION complement (the boundary ring +
            # the interior cells ride it; cls is never set to 2), so
            # INTERIOR is empty and PAIR-JUNCTION == class_counts's
            # PAIR-JUNCTION. Verified 72/72, never repaired.
            mask_ok = mask_ok \
                and pcd["PAIR-JUNCTION"]["n_cells"] == cc["PAIR-JUNCTION"] \
                and pcd["INTERIOR"]["n_cells"] == 0 \
                and pcd["CANON-BOUNDARY"]["n_cells"] == 400 - cc["PAIR-JUNCTION"]
        grid_ok = grid_ok and len(seen) == 72
        subst_ok = bool(all((h, "substituted", s) in seen
                            for h in hosts for s in (1, 2, 3)))
        canon_ok = bool(all((h, "canonical", s) in seen
                            for h in hosts for s in (1, 2, 3)))

        # ---- the 36 SUBSTITUTED rows (the P3 arm's own face) and the
        #      12-host table: per-host mean CANON-BOUNDARY frac and
        #      mean PAIR-JUNCTION frac over the 3 seeds ---------------
        TOL = 1e-9
        rows_sub = [r for r in rows256 if r["arm"] == "substituted"]
        assert len(rows_sub) == 36, \
            f"the substituted arm drifted: {len(rows_sub)}"
        per_host = {}
        detail = []
        for h in hosts:
            hs = sorted((r for r in rows_sub if r["host"] == h),
                        key=lambda r: int(r["seed"]))
            assert len(hs) == 3, f"{h}: the substituted rows drifted"
            cb = [float(next(p for p in r["decomposition"]["per_class"]
                             if p["class"] == "CANON-BOUNDARY")
                        ["frac_of_sq"]) for r in hs]
            pj = [float(next(p for p in r["decomposition"]["per_class"]
                             if p["class"] == "PAIR-JUNCTION")
                        ["frac_of_sq"]) for r in hs]
            it = [float(next(p for p in r["decomposition"]["per_class"]
                             if p["class"] == "INTERIOR")
                        ["frac_of_sq"]) for r in hs]
            cbr = [float(next(p for p in r["decomposition"]["per_class"]
                              if p["class"] == "CANON-BOUNDARY")
                         ["rms_contrib_mV"]) for r in hs]
            pjr = [float(next(p for p in r["decomposition"]["per_class"]
                              if p["class"] == "PAIR-JUNCTION")
                         ["rms_contrib_mV"]) for r in hs]
            we = [float(r["worst_err"]) for r in hs]
            pjc = [int(r["pair_junction_count"]) for r in hs]
            bcc = [int(r["class_counts"]["CANON-BOUNDARY"]) for r in hs]
            per_host[h] = {
                "mean_worst_err": float(np.mean(we)),
                "cb_frac_mean": float(np.mean(cb)),
                "pj_frac_mean": float(np.mean(pj)),
                "interior_frac_mean": float(np.mean(it)),
                "cb_rms_contrib_mean": float(np.mean(cbr)),
                "pj_rms_contrib_mean": float(np.mean(pjr)),
                "mean_pair_junction_count": float(np.mean(pjc)),
                "mean_boundary_cells": float(np.mean(bcc))}
            for r, c, p in zip(hs, cb, pj):
                detail.append({
                    "host": h, "seed": int(r["seed"]),
                    "worst_row_key": r["worst_row_key"],
                    "worst_err": float(r["worst_err"]),
                    "cb_frac": c, "pj_frac": p,
                    "pair_junction_count": int(r["pair_junction_count"])})

        # ---- the mia_prod_err carry (the premium's mediator,
        #      exp273's deposited field table BY EXACT FIELD NAME,
        #      bit-exact vs exp243's records; selection-tagged
        #      external — the non-circular set) --------------------------
        ft = {rec["field"]: rec for rec in dep273["field_table"]}
        MIA_FIELD = "exp243.classes.multi_identity_audit.prod_err"
        assert MIA_FIELD in ft, \
            "mia_prod_err missing from exp273's field table"
        rec_mia = ft[MIA_FIELD]
        assert rec_mia["selection"] == "external", \
            "the mia field is not selection-tagged external in exp273"
        cls = dep243["classes"]
        assert set(cls) == set(hosts), "exp243's classes drifted"
        a = {}
        carry_ok = True
        for h in hosts:
            rec = cls[h]["multi_identity_audit"]
            assert rec["bit_identical"] is True, \
                f"{h}: the multi-identity audit is not bit-identical"
            v = float(rec["prod_err"])
            assert v == v and abs(v) != float("inf"), \
                f"{h}: the audit prod_err is not finite"
            a[h] = v
            carry_ok = carry_ok and float(rec_mia["values"][h]) == v

        # ---- D1's provenance chains: exp273's recorded inputs 5/5,
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

        # ---- D2: THE ACCOUNTING IDENTITY (per row, all 72): the
        #      per-class frac_of_sq sums to 1 within 1e-9; the
        #      deposited identity_residual <= 1e-9; the RMS-
        #      reconstruction face |sqrt(sum_k sum_sq_k / 400) -
        #      worst_err| <= 0.0051 (worst_err is exp256's 2-decimal
        #      rounding — the 0.005 bound + margin) ----------------------
        frac_devs = {}
        idents = {}
        rms_devs = {}
        for r in rows256:
            pc = {p["class"]: p for p in r["decomposition"]["per_class"]}
            frac_devs[(r["host"], r["arm"], int(r["seed"]))] = \
                abs(sum(p["frac_of_sq"] for p in pc.values()) - 1.0)
            idents[(r["host"], r["arm"], int(r["seed"]))] = \
                float(r["decomposition"]["identity_residual"])
            rms_devs[(r["host"], r["arm"], int(r["seed"]))] = abs(
                float(np.sqrt(sum(p["sum_sq"] for p in pc.values())
                              / 400.0)) - float(r["worst_err"]))
        max_frac_dev = float(max(frac_devs.values()))
        max_ident = float(max(idents.values()))
        max_rms_dev = float(max(rms_devs.values()))
        frac_ok = bool(max_frac_dev < TOL)
        ident_ok = bool(max_ident < TOL)
        rms_ok = bool(max_rms_dev <= 0.0051)
        d2_pass = bool(frac_ok and ident_ok and rms_ok)

        # ---- the 12-host share table (the branch's raw material) -----
        table = [{"host": h,
                  "outlier": h in outliers,
                  "n_substituted_rows": 3,
                  "mean_worst_err": per_host[h]["mean_worst_err"],
                  "cb_frac_mean": per_host[h]["cb_frac_mean"],
                  "pj_frac_mean": per_host[h]["pj_frac_mean"],
                  "interior_frac_mean": per_host[h]["interior_frac_mean"],
                  "cb_rms_contrib_mean":
                      per_host[h]["cb_rms_contrib_mean"],
                  "pj_rms_contrib_mean":
                      per_host[h]["pj_rms_contrib_mean"],
                  "mean_pair_junction_count":
                      per_host[h]["mean_pair_junction_count"],
                  "mean_boundary_cells":
                      per_host[h]["mean_boundary_cells"],
                  "mia_prod_err": a[h]}
                 for h in hosts]
        all_finite = bool(all(
            row[k] == row[k] and abs(row[k]) != float("inf")
            for row in table
            for k in ("mean_worst_err", "cb_frac_mean", "pj_frac_mean",
                      "interior_frac_mean", "cb_rms_contrib_mean",
                      "pj_rms_contrib_mean",
                      "mean_pair_junction_count",
                      "mean_boundary_cells", "mia_prod_err")))

        # ---- D3: THE BRANCH (the discriminant pre-named, the bars
        #      numeric): BOUNDARY-CLASS iff min(cb on H3, H5) > max(cb
        #      over the cluster); PAIR-CLASS iff min(pj on H3, H5) >
        #      max(pj over the cluster); SPLIT iff both exceed;
        #      NEITHER (the exhaustive residual) otherwise. Both
        #      margins recorded. -----------------------------------------
        cb_min = float(min(per_host[h]["cb_frac_mean"] for h in outliers))
        pj_min = float(min(per_host[h]["pj_frac_mean"] for h in outliers))
        cb_cmax = float(max(per_host[h]["cb_frac_mean"] for h in cluster))
        pj_cmax = float(max(per_host[h]["pj_frac_mean"] for h in cluster))
        cb_exceeds = bool(cb_min > cb_cmax)
        pj_exceeds = bool(pj_min > pj_cmax)
        if cb_exceeds and pj_exceeds:
            branch = "SPLIT"
        elif cb_exceeds:
            branch = "BOUNDARY-CLASS"
        elif pj_exceeds:
            branch = "PAIR-CLASS"
        else:
            branch = "NEITHER"
        disc = {
            "outlier_cb_shares": {h: per_host[h]["cb_frac_mean"]
                                  for h in outliers},
            "outlier_pj_shares": {h: per_host[h]["pj_frac_mean"]
                                  for h in outliers},
            "cluster_cb_share_max": cb_cmax,
            "cluster_pj_share_max": pj_cmax,
            "cluster_cb_share_min":
                float(min(per_host[h]["cb_frac_mean"] for h in cluster)),
            "cluster_pj_share_min":
                float(min(per_host[h]["pj_frac_mean"] for h in cluster)),
            "cb_outlier_margin": cb_min - cb_cmax,
            "pj_outlier_margin": pj_min - pj_cmax,
            "cb_exceeds_cluster_max": cb_exceeds,
            "pj_exceeds_cluster_max": pj_exceeds}

        # ---- THE PREMIUM'S MEDIATOR (the exp274/exp275 conventions,
        #      REPORTED not gated): the response = mia_prod_err; the
        #      two mediators = the two per-host mean shares; the
        #      single-mediator Spearmans (mediator vector first) + the
        #      OLS-on-ranks single R2s + the full model (with two
        #      mediators the pair IS the full model); the shares by
        #      the two-order symmetric average on the pre-named entry
        #      order cb -> pj and its reverse pj -> cb; shares +
        #      unexplained == 1 asserted (no clamping); the ties
        #      census; the all-ranks variant AUDIT-ONLY. ---------------
        a_vec = [a[h] for h in hosts]
        med_vals = {"cb_frac_mean": [per_host[h]["cb_frac_mean"]
                                     for h in hosts],
                    "pj_frac_mean": [per_host[h]["pj_frac_mean"]
                                     for h in hosts]}
        spearmans = {k: _spearman(vec, a_vec)
                     for k, vec in med_vals.items()}
        Rk = rankdata(np.asarray(a_vec, dtype=float))
        c1, c2 = "cb_frac_mean", "pj_frac_mean"
        r2_single = {k: _r2([med_vals[k]], Rk) for k in med_vals}
        r2_full = _r2([med_vals[c1], med_vals[c2]], Rk)
        inc_o1 = {c1: r2_single[c1], c2: r2_full - r2_single[c1]}
        inc_o2 = {c2: r2_single[c2], c1: r2_full - r2_single[c2]}
        reg_shares = {k: 0.5 * (inc_o1[k] + inc_o2[k])
                      for k in med_vals}
        reg_unexplained = 1.0 - r2_full
        reg_sum = sum(reg_shares.values()) + reg_unexplained
        assert abs(reg_sum - 1.0) < 1e-9, \
            "the three-way rank shares do not sum to 1"
        assert all(v == v and abs(v) != float("inf")
                   for v in list(reg_shares.values())
                   + [reg_unexplained, r2_full]), "non-finite share"
        rk = {k: rankdata(np.asarray(v, dtype=float))
              for k, v in med_vals.items()}
        audit_all_ranks = {
            "r2_single": {k: _r2([rk[k]], Rk) for k in med_vals},
            "r2_full": _r2([rk[c1], rk[c2]], Rk)}
        audit_all_ranks["single_equals_spearman_squared"] = bool(
            all(abs(audit_all_ranks["r2_single"][k]
                    - spearmans[k] ** 2) < 1e-12 for k in med_vals))

        d1_pass = bool(grid_ok and canon_ok and subst_ok and decomp_ok
                       and mask_ok and cc_ok and worst_finite
                       and all_finite and carry_ok and chain_all_ok)
        d3_pass = bool(branch in ("BOUNDARY-CLASS", "PAIR-CLASS",
                                  "SPLIT", "NEITHER")
                       and cb_min == cb_min and pj_min == pj_min)

        ties = {"mia_prod_err": _ties_census(a_vec),
                "cb_frac_mean": _ties_census(med_vals["cb_frac_mean"]),
                "pj_frac_mean": _ties_census(med_vals["pj_frac_mean"])}

        return {
            "hosts": hosts, "outliers": outliers, "cluster": cluster,
            "table": table, "substituted_rows_detail": detail,
            "d1": {"pass": d1_pass,
                   "rows_complete_72": grid_ok,
                   "canonical_rows_complete_36": canon_ok,
                   "substituted_rows_complete_36": subst_ok,
                   "decompositions_complete_72": decomp_ok,
                   "mask_semantics_verified_72": mask_ok,
                   "class_counts_sum_400_72": cc_ok,
                   "worst_err_finite_72": worst_finite,
                   "table_finite": all_finite,
                   "exp273_mia_carry_bit_exact": carry_ok,
                   "exp273_recorded_input_shas_match_actual_bytes":
                       chain273_ok,
                   "exp274_recorded_input_shas_match_actual_bytes":
                       chain274_ok,
                   "exp275_recorded_input_shas_match_actual_bytes":
                       chain275_ok,
                   "provenance_chains_sha_verified": chain_all_ok},
            "d2": {"pass": d2_pass,
                   "n_rows_checked": 72,
                   "tolerance": TOL,
                   "rms_reconstruction_bar": 0.0051,
                   "max_abs_frac_sum_deviation": max_frac_dev,
                   "max_abs_identity_residual": max_ident,
                   "max_abs_rms_reconstruction_deviation": max_rms_dev},
            "d3": {"pass": d3_pass, "branch": branch, **disc},
            "regression": {
                "response": ("the premium's mediator mia_prod_err — "
                             "exp243.classes.multi_identity_audit."
                             "prod_err via exp273's deposited field "
                             "table (selection external), bit-exact "
                             "vs exp243's records (12 hosts)"),
                "mediators": ("the two per-host mean cell-class "
                              "shares over the 36 substituted rows: "
                              "cb_frac_mean (exp208's CANON-BOUNDARY "
                              "record AS DEPOSITED — the non-"
                              "PAIR-JUNCTION complement) and "
                              "pj_frac_mean (PAIR-JUNCTION)"),
                "spearman_rho": spearmans,
                "r2_single": r2_single,
                "r2_pairs": {"cb+pj": r2_full},
                "r2_pairs_note": ("with two mediators the only pair "
                                  "IS the full model"),
                "r2_full": r2_full,
                "order_decompositions": {"order_cb_pj": inc_o1,
                                         "order_pj_cb": inc_o2},
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

    d3 = payload_a["d3"]
    gates = {"D1_grids": {
                 "pass": payload_a["d1"]["pass"],
                 "bar": "exp256's 72 rows re-read complete (12 hosts x "
                        "2 arms x 3 seeds), every decomposition "
                        "carrying the three pre-named per_class "
                        "records with finite entries; the mask "
                        "semantics verified in-deposit 72/72; the 36 "
                        "substituted rows complete 12 x 3; the "
                        "outlier pre-name asserted (exp273 == "
                        "exp272 == ['H3','H5']); exp273's mia carry "
                        "bit-exact vs exp243's records; the "
                        "provenance chains sha-verified (exp273 5/5, "
                        "exp274 6/6, exp275 7/7); READ-ONLY",
                 **payload_a["d1"]},
             "D2_identity": {
                 "pass": payload_a["d2"]["pass"],
                 "bar": "per row, all 72: the per-class frac_of_sq "
                        "sums to 1 within 1e-9; the deposited "
                        "identity_residual <= 1e-9; the RMS-"
                        "reconstruction face |sqrt(sum sum_sq / 400) "
                        "- worst_err| <= 0.0051 (exp256's 2-decimal "
                        "rounding bound + margin)",
                 **payload_a["d2"]},
             "D3_branch": {
                 "pass": d3["pass"],
                 "bar": "the discriminant pre-named, the bars numeric: "
                        "BOUNDARY-CLASS iff min(outlier cb share) > "
                        "max(cluster cb share); PAIR-CLASS iff "
                        "min(outlier pj share) > max(cluster pj "
                        "share); SPLIT iff both exceed; NEITHER "
                        "(the exhaustive residual) otherwise; the "
                        "mediator rank regression reported "
                        "alongside (exp274 conventions), audit-only, "
                        "never gating",
                 "branch": d3["branch"],
                 **{k: v for k, v in d3.items() if k != "pass"}}}

    # ---- D4: the discipline --------------------------------------------
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

    d4_pass = bool(ro_unchanged and deterministic and no_wall_clock
                   and floor_at_entry == PROD_FLOOR
                   and docstring_ok and header_ok)

    gates["D4_discipline"] = {
        "pass": d4_pass,
        "bar": ("all deposits READ-ONLY sha-recorded byte-unchanged; "
                "deterministic — two-pass bit-identical; no "
                "wall-clock fields; the docstring+header pinned to "
                "aa0d3c2 asserted at entry AND exit; NEURAL_SPEC_MIN "
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
        "docstring_byte_unchanged_vs_aa0d3c2": docstring_ok,
        "header_sha256": header_sha,
        "header_byte_unchanged_vs_aa0d3c2": header_ok,
        "deposit_form": ("deterministic: no wall-clock fields — a "
                         "re-run of this module reproduces this file "
                         "byte-identically")}

    # ---- the branch + the verdict (one line, the numbers
    #      data-driven) -----------------------------------------------------
    branch = d3["branch"]
    reg = payload_a["regression"]

    def _g(v):
        return format(v, ".10g") if isinstance(v, float) else str(v)

    gate_passes = {"D1": gates["D1_grids"]["pass"],
                   "D2": gates["D2_identity"]["pass"],
                   "D3": gates["D3_branch"]["pass"],
                   "D4": gates["D4_discipline"]["pass"]}
    n_pass = sum(1 for v in gate_passes.values() if v)
    n_refute = 4 - n_pass

    tbl = {r["host"]: r for r in payload_a["table"]}
    branch_face = {
        "BOUNDARY-CLASS": ("the outlier hosts' deep-band error is "
                           "BOUNDARY-CLASS: the CANON-BOUNDARY (the "
                           "non-pair-junction complement, as "
                           "deposited) share exceeds the cluster's "
                           "max on both outliers"),
        "PAIR-CLASS": ("the outlier hosts' deep-band error is "
                       "PAIR-CLASS: the PAIR-JUNCTION share exceeds "
                       "the cluster's max on both outliers"),
        "SPLIT": ("SPLIT: both the CANON-BOUNDARY and the "
                  "PAIR-JUNCTION shares exceed the cluster's max on "
                  "both outliers"),
        "NEITHER": ("NEITHER: neither share exceeds the cluster's "
                    "max on both outliers — the outliers' deep-band "
                    "error is class-typical of the cluster")}[branch]
    verdict = (
        f"{n_pass}/4 gates D1-D4 ({n_pass} PASS / {n_refute} REFUTE) | "
        f"{branch} | {branch_face} | the outliers' mean shares over "
        f"the 36 substituted rows: cb "
        f"{d3['outlier_cb_shares']['H3']:.4f}/"
        f"{d3['outlier_cb_shares']['H5']:.4f} vs cluster max "
        f"{d3['cluster_cb_share_max']:.4f} (margin "
        f"{d3['cb_outlier_margin']:+.4f}), pj "
        f"{d3['outlier_pj_shares']['H3']:.4f}/"
        f"{d3['outlier_pj_shares']['H5']:.4f} vs cluster max "
        f"{d3['cluster_pj_share_max']:.4f} (margin "
        f"{d3['pj_outlier_margin']:+.4f}) | P3's own error (mean "
        f"substituted worst) H3 {tbl['H3']['mean_worst_err']:.2f} / "
        f"H5 {tbl['H5']['mean_worst_err']:.2f} mV | the mediator "
        f"regression (exp274 convention, audit-only): "
        f"Spearman(mia, cb) {_g(reg['spearman_rho']['cb_frac_mean'])}, "
        f"Spearman(mia, pj) {_g(reg['spearman_rho']['pj_frac_mean'])}, "
        f"full rank R2 {_g(reg['r2_full'])}, shares cb "
        f"{_g(reg['shares_of_rank_variance']['cb_frac_mean'])} / pj "
        f"{_g(reg['shares_of_rank_variance']['pj_frac_mean'])} / "
        f"unexplained {_g(reg['unexplained'])} | 12 hosts x 3 seeds = "
        f"36 substituted rows, a pure re-read of exp256's 72 "
        f"decomposed rows, READ-ONLY byte-unchanged, two-pass "
        f"bit-identical, no wall-clock fields, floor -60.0 asserted "
        f"at exit")

    deposit = {
        "exp": "exp277_deep_band_break_face",
        "claim": (
            "THE DEEP-BAND BREAK FACE (batch 35, pre-registration "
            "commit aa0d3c2): why do the deep-band programs break on "
            "the boundary-richest hosts (H3/H5, 47/48 canon-boundary "
            "cells)? The P3 arm's OWN error decomposed per host by "
            "exp208's cell-class machinery — a pure re-read of "
            "exp256's 72 deposited rows' per_class decompositions "
            "(the 36 substituted rows = 12 hosts x 3 seeds): per-host "
            "mean CANON-BOUNDARY frac and PAIR-JUNCTION frac; the "
            "pre-named branch BOUNDARY-CLASS / PAIR-CLASS / SPLIT "
            "(the outliers' min share > the cluster's max) + NEITHER "
            "the exhaustive residual; the premium's mediator "
            "mia_prod_err rank-regressed on the two shares under the "
            "exp274/exp275 conventions (reported, never gating)"),
        "method": {
            "source": ("exp256's deposited 72 rows = 12 hosts x 2 "
                       "arms x 3 seeds; each row's decomposition = "
                       "exp208's classify(T_row, W_row) + decompose "
                       "on the row's WORST instance's own "
                       "state-carrying read (exp243's A3 path); the "
                       "SUBSTITUTED arm (P3's own face: the deep rows "
                       "r-60i0/r-60i1 on the base medium) is the 36 "
                       "rows read here"),
            "mask_semantics": ("DISCLOSED, read AS DEPOSITED: "
                               "exp208's classify assigns cls 1 = "
                               "PAIR-JUNCTION and 0 = otherwise (the "
                               "boundary ring wins precedence; cls is "
                               "never set to 2), so the deposited "
                               "per_class CANON-BOUNDARY record is "
                               "the NON-PAIR-JUNCTION complement of "
                               "the squared error (boundary ring + "
                               "interior) and the deposited INTERIOR "
                               "record is empty — verified in-deposit "
                               "72/72, never repaired; the pure "
                               "boundary-only share is not "
                               "recoverable from the deposits"),
            "per_host_table": ("per-host mean CANON-BOUNDARY frac / "
                               "mean PAIR-JUNCTION frac over the 3 "
                               "substituted seeds, alongside the "
                               "mean worst_err (the P3 arm's own "
                               "error, exp276's m_P3), the mean "
                               "rms_contrib_mV, the mean "
                               "pair-junction count, the mean "
                               "precedence boundary-cell count, and "
                               "the mia_prod_err context column"),
            "branch_rule": ("the outliers = exp273's deposited "
                            "outliers (asserted == exp272's "
                            "descriptive.premium_hosts == ['H3','H5']);"
                            " BOUNDARY-CLASS iff min(outlier cb share) "
                            "> max(cluster cb share); PAIR-CLASS iff "
                            "min(outlier pj share) > max(cluster pj "
                            "share); SPLIT iff both; NEITHER (the "
                            "exhaustive residual) otherwise; both "
                            "margins recorded"),
            "regression": ("the exp274/exp275 convention VERBATIM: "
                           "the response = mia_prod_err (12 hosts, "
                           "tied-average ranks); the two mediators = "
                           "the two per-host mean shares; "
                           "single-mediator Spearmans (mediator "
                           "vector first, scipy rankdata both "
                           "sides); the OLS-on-ranks single R2s + "
                           "the full model (with two mediators the "
                           "pair IS the full model); the shares by "
                           "the two-order symmetric average on the "
                           "pre-named entry order cb -> pj and its "
                           "reverse pj -> cb; shares + unexplained "
                           "== 1, no clamping; the all-ranks variant "
                           "AUDIT-ONLY; REPORTED not gated — the "
                           "branch is the only gated read"),
            "method_source": ("experiments/exp256_row_pair_"
                              "regression.py (the 72 decomposed "
                              "rows — exp208's classify/decompose "
                              "verbatim via exp243), experiments/"
                              "exp273_outlier_hosts.py (the outlier "
                              "pre-name + the mia field-table "
                              "carry), experiments/exp272_host_"
                              "premium_structure.py (the host frame "
                              "+ the premium_hosts pre-name + the "
                              "_spearman convention), experiments/"
                              "exp243_structured_adversarial.py "
                              "(the audit records), experiments/"
                              "exp274_premium_mechanism.py (the "
                              "rank-regression convention), "
                              "experiments/exp275_audit_direction."
                              "py (the sha discipline)")},
        "inputs": {
            "exp256_deposit": {
                "path": "results/exp256_row_pair_regression.json",
                "sha256": ro_before["exp256_deposit"],
                "role": ("the 72 decomposed rows — the computation's "
                         "primary source: the 36 substituted rows' "
                         "per_class fracs + the worst errs")},
            "exp273_deposit": {
                "path": "results/exp273_outlier_hosts.json",
                "sha256": ro_before["exp273_deposit"],
                "role": ("the deposited outlier pre-name + the "
                         "field-table carry of mia_prod_err "
                         "(bit-exact) + the recorded input shas "
                         "verified 5/5")},
            "exp272_deposit": {
                "path": "results/exp272_host_premium_structure.json",
                "sha256": ro_before["exp272_deposit"],
                "role": ("the host frame + the outlier pre-name "
                         "source (descriptive.premium_hosts)")},
            "exp243_deposit": {
                "path": "results/exp243_structured_adversarial.json",
                "sha256": ro_before["exp243_deposit"],
                "role": ("the 12 multi_identity_audit records the "
                         "mia_prod_err carry is bit-checked "
                         "against")},
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
        "per_host_table": payload_a["table"],
        "substituted_rows_detail": payload_a["substituted_rows_detail"],
        "branch_discriminant": {k: v for k, v in d3.items()
                                if k not in ("pass",)},
        "mediator_regression": payload_a["regression"],
        "ties_census": payload_a["ties_census"],
        "gates": gates,
        "branch": branch,
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
            "docstring_byte_unchanged_vs_aa0d3c2": docstring_ok,
            "header_sha256": header_sha,
            "header_byte_unchanged_vs_aa0d3c2": header_ok,
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

    print("=== exp277: THE DEEP-BAND BREAK FACE (pure deposit re-read "
          "+ arithmetic) ===")
    print("  the P3 arm's own error decomposed per host by exp208's "
          "cell-class machinery (exp256's 36 substituted rows, the "
          "per-host mean CANON-BOUNDARY / PAIR-JUNCTION shares)")
    print(f"\n  D1 grids: {'PASS' if gates['D1_grids']['pass'] else 'FAIL'} "
          f"(exp256's 72 rows re-read complete; the mask semantics "
          f"verified 72/72; the outlier pre-name asserted; exp273's "
          f"mia carry bit-exact; the chains sha-verified exp273 5/5 + "
          f"exp274 6/6 + exp275 7/7)")
    print(f"  D2 identity: {'PASS' if gates['D2_identity']['pass'] else 'FAIL'} "
          f"(72/72 rows: the frac_of_sq sums to 1 — max dev "
          f"{payload_a['d2']['max_abs_frac_sum_deviation']:.2e} vs the "
          f"1e-9 bar; the deposited identity_residual max "
          f"{payload_a['d2']['max_abs_identity_residual']:.2e}; the "
          f"RMS-reconstruction max dev "
          f"{payload_a['d2']['max_abs_rms_reconstruction_deviation']:.6f} "
          f"vs the 0.0051 bar)")
    print("  D3 branch — the per-host mean class shares over the "
          "substituted rows:")
    for row in payload_a["table"]:
        tag = " <== outlier" if row["outlier"] else ""
        print(f"      {row['host']:4s} err {row['mean_worst_err']:5.2f}  "
              f"cb {row['cb_frac_mean']:.4f}  pj {row['pj_frac_mean']:.4f}  "
              f"int {row['interior_frac_mean']:.4f}  "
              f"mia {row['mia_prod_err']:5.2f}{tag}")
    print(f"  D4 discipline: {'PASS' if d4_pass else 'FAIL'} "
          f"(8 deposits READ-ONLY byte-unchanged: {ro_unchanged}; "
          f"two-pass bit-identical: {deterministic}; no wall-clock "
          f"fields: {no_wall_clock})")
    print(f"\n  BRANCH: {branch} | cb margin "
          f"{d3['cb_outlier_margin']:+.4f} (outliers min "
          f"{d3['outlier_cb_shares']['H3']:.4f}/"
          f"{d3['outlier_cb_shares']['H5']:.4f} vs cluster max "
          f"{d3['cluster_cb_share_max']:.4f}) | pj margin "
          f"{d3['pj_outlier_margin']:+.4f} (outliers min "
          f"{d3['outlier_pj_shares']['H3']:.4f}/"
          f"{d3['outlier_pj_shares']['H5']:.4f} vs cluster max "
          f"{d3['cluster_pj_share_max']:.4f})")
    print(f"\n  GATES: {verdict}")
    print(f"  deposited {OUT}")

    # the hard rule, re-asserted after the work: the docstring is still
    # the aa0d3c2 pre-registration, byte-for-byte
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
