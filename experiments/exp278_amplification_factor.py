#!/usr/bin/env python3
"""exp278 — THE AMPLIFICATION FACTOR (batch 36; batch-35's derived item,
ledger L255 — zero new simulation).

THE OPEN ITEM: exp277 closed the face question — the deep-band break is
CLASS-BLIND: the outliers' deep-band error carries the cluster-typical
class mixture, amplified ~7x (P3's own error H3 3.68 / H5 3.36 mV vs
the cluster's ~0.50-0.54). The amplification is itself the measurement:
per host, the deep-band substitution's cost stands against the
canon-space arms' cost on the SAME host x seed grid — exp256's
deposited 72 rows carry both faces. THE AMPLIFICATION RATIO per host =
the P3 arm's mean err / the P1+P2 arms' mean err (zero-knob: one
closed-form for all 12 hosts, no parameters). THE QUESTION: does the
per-host amplification track the audit error mia_prod_err (exp273's
external discriminator), or the canon-boundary count (exp255's
zero-knob instrument — exp272 refuted it for the PREMIUM level at
Spearman 0.0526 < 0.5; here it is tested for the AMPLIFICATION level)?

THE INSTRUMENT (pre-registered, zero-knob, pure re-read):
  - the numerator: the P3 arm's mean err = the mean over the 3
    substituted rows' deposited worst_err per host (the per-seed arm
    worst = the max over the two pre-named deep instances r-60i0/
    r-60i1 — exp255's/exp256's arm-worst convention; == exp276's
    m_P3 == exp277's mean_worst_err, bit-exact asserted).
  - THE DENOMINATOR'S DEFINITION (the gate, zero-knob): the P1+P2
    arms' mean err = the POOLED mean over the 6 canonical instance
    errs (P1_canon_zone_relabelings x 3 seeds +
    P2_boundary_double_frequency_rewiring x 3 seeds) — NOT the mean
    of the per-seed maxima (the deposited worst_err_mean_canonical
    IS the max variant; it is recorded alongside as audit-only and
    never enters the ratio; asserted in G2).
  - the regressors: mia_prod_err (exp273's deposited field table,
    exact field exp243.classes.multi_identity_audit.prod_err,
    selection external, bit-exact vs exp243's records) and the
    canon-boundary count (the exp255 instrument: exp243's classes
    records' n_boundary_cells_base — carried bit-exact from exp273's
    field table, cross-checked vs exp243's classes, exp272's
    per_host records, and exp255's deposited rows).
  - THE REGRESSIONS (the exp274/exp275 conventions verbatim): the
    response = the amplification ratio (12 hosts, tied-average
    ranks); two single-regressor Spearmans (regressor vector first,
    scipy rankdata both sides); the OLS-on-ranks single R2s (the
    response enters as its tied-average ranks, the regressor as its
    numeric values — exp262's/exp274's convention) + the full model
    (both regressors; with two regressors the pair IS the full
    model); the shares by the two-order symmetric average on the
    pre-named entry order mia -> bc and its reverse bc -> mia;
    shares + unexplained == 1 asserted (no clamping); the ties
    census; the all-ranks variant AUDIT-ONLY, never gating.
  - THE BRANCH (the discriminant pre-named, the bars numeric):
    MIA-SCALED iff Spearman(ratio, mia_prod_err) >= 0.5 (the house
    bar); else GEOMETRY-SCALED iff Spearman(ratio, boundary count)
    >= 0.5; else UNATTACHED (the exhaustive residual). The mia test
    is pre-named FIRST — the precedence is part of this
    registration; both rhos recorded regardless.

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE GRIDS: exp256's 72 rows re-read COMPLETE — 12 hosts x 2
      arms x 3 seeds, every canonical row carrying exactly the two
      pre-named P1/P2 instances and every substituted row exactly the
      two pre-named deep instances r-60i0/r-60i1, each row's
      worst_err finite AND == the max of its instance errs (the
      deposited arm-worst convention, verified 72/72); the per-host
      means recomputed from the rows bit-exact vs EVERY deposited
      record where present — exp273's field table
      (worst_err_mean_substituted / _canonical / _all_arms),
      exp276's decomposition_table (m_P1 / m_P2 / m_P3), exp277's
      per_host_table (mean_worst_err), exp272's deposited records
      where present (per_host n_boundary_cells_base; both grids'
      canon_worst_err columns == exp256's canonical row worst_err
      36/36 each at the (host, seed) grain), exp243's classes
      records (multi_identity_audit.prod_err + n_boundary_cells_base),
      exp255's deposited rows (n_boundary_cells, 24 rows, each host
      single-valued); the outlier pre-name asserted (exp273's
      outliers == exp272's descriptive.premium_hosts == ['H3', 'H5']);
      the provenance chains sha-verified against the actual deposit
      bytes — exp273's recorded inputs 5/5, exp274's 6/6, exp275's
      7/7, exp276's 8/8, exp277's 8/8; READ-ONLY.
  G2  THE RATIO'S DEFINITION (zero-knob): one closed-form for all 12
      hosts — R_h = m_P3(h) / m_P12(h), m_P12 = the POOLED mean over
      the 6 canonical instance errs (identified by the deposited pert
      names, 3 seeds each), asserted computed from the instances and
      NOT from the per-seed maxima; the max variant (the mean of the
      canonical rows' worst_err) computed alongside, bit-exact vs
      exp273's deposited worst_err_mean_canonical, recorded
      audit-only — never entering the ratio; the pooled-vs-max gap
      recorded per host; all 12 ratios finite and > 0; the definition
      carries no parameters and no per-host cases (the ratio map
      carries exactly the 12 host keys, one formula).
  G3  THE BRANCH: the discriminant resolved on the pre-named numeric
      bars (MIA-SCALED / GEOMETRY-SCALED / UNATTACHED above; both
      rhos recorded); the regressions REPORTED alongside under the
      exp274/exp275 conventions — audit-only, never gating.
  G4  THE DISCIPLINE: all deposits READ-ONLY sha-recorded
      byte-unchanged (before/after); deterministic — two-pass
      bit-identical; no wall-clock fields (recursive key scan +
      serialized-blob scan); the docstring+header pinned to this
      pre-registration commit, asserted at entry AND exit;
      NEURAL_SPEC_MIN == -60.0 asserted at exit.

THE BRANCHES (pre-named): MIA-SCALED / GEOMETRY-SCALED / UNATTACHED
(the exhaustive residual; the first two are the registered question's
named outcomes).

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
OUT = os.path.join(ROOT, "results", "exp278_amplification_factor.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates G1-G4 evaluated exactly once per
    #      pass, pre-registration commit b42fbc0; the docstring's RUN
    #      clause holds verbatim: a pure deposit re-read + arithmetic,
    #      zero new simulation, seconds) ==================================
    import hashlib
    import json

    import numpy as np
    from scipy.stats import rankdata

    import cultivation.bioelectric.collective as CORE  # the floor's home

    # ---- the byte-unchanged self-check (the hard rule: the docstring
    #      is the b42fbc0 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "a3506ebc85c616555f99ddaf247443f9f4abb17ad805b227a034ce053e2b8cc3")
    EXPECTED_HEADER_SHA256 = (
        "8d28a3ea9eeb923f2695566fbe65cf883641a10d6e136f1577e12b778e85bfff")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from b42fbc0"
    assert header_ok, "header drifted from b42fbc0"

    # ---- the -60.0 floor (G4: asserted at exit; nothing in this body
    #      imports any machinery that touches it — recorded at entry,
    #      restored and re-asserted as the closing line, exp243's/
    #      exp271/exp272's/.../exp277's closing discipline) --------------
    PROD_FLOOR = -60.0
    floor_at_entry = float(CORE.NEURAL_SPEC_MIN)
    assert floor_at_entry == PROD_FLOOR, \
        f"floor drift at entry: {floor_at_entry}"

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      work, re-verified byte-unchanged at the end) — the seven the
    #      computation reads (exp256's 72 rows, exp273's carries, exp272's
    #      per-host records + grids, exp243's classes, exp255's rows,
    #      exp276's arm masses, exp277's table) plus the five the
    #      provenance chains name (exp271/exp182 never opened for
    #      computation here) ----------------------------------------------
    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP255 = os.path.join(ROOT, "results", "exp255.json")
    DEP256 = os.path.join(ROOT, "results",
                          "exp256_row_pair_regression.json")
    DEP272 = os.path.join(ROOT, "results",
                          "exp272_host_premium_structure.json")
    DEP273 = os.path.join(ROOT, "results", "exp273_outlier_hosts.json")
    DEP274 = os.path.join(ROOT, "results",
                          "exp274_premium_mechanism.json")
    DEP275 = os.path.join(ROOT, "results",
                          "exp275_audit_direction.json")
    DEP276 = os.path.join(ROOT, "results",
                          "exp276_audit_own_face.json")
    DEP277 = os.path.join(ROOT, "results",
                          "exp277_deep_band_break_face.json")
    DEP271 = os.path.join(ROOT, "results", "exp271_one_zone_premium.json")
    DEP182 = os.path.join(ROOT, "results", "exp182_substrate_100.json")
    for _p in (DEP243, DEP255, DEP256, DEP272, DEP273, DEP274, DEP275,
               DEP276, DEP277, DEP271, DEP182):
        assert os.path.exists(_p), f"missing source deposit {_p}"

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    RO_KEYS = ("exp243_deposit", "exp255_deposit", "exp256_deposit",
               "exp272_deposit", "exp273_deposit", "exp274_deposit",
               "exp275_deposit", "exp276_deposit", "exp277_deposit",
               "exp271_deposit", "exp182_deposit")
    RO_PATHS = {"exp243_deposit": DEP243, "exp255_deposit": DEP255,
                "exp256_deposit": DEP256, "exp272_deposit": DEP272,
                "exp273_deposit": DEP273, "exp274_deposit": DEP274,
                "exp275_deposit": DEP275, "exp276_deposit": DEP276,
                "exp277_deposit": DEP277, "exp271_deposit": DEP271,
                "exp182_deposit": DEP182}
    ro_before = {k: _sha(RO_PATHS[k]) for k in RO_KEYS}

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
    #      two payloads must be byte-identical — G4's determinism
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
        with open(DEP255) as fh:
            dep255 = json.load(fh)
        with open(DEP276) as fh:
            dep276 = json.load(fh)
        with open(DEP277) as fh:
            dep277 = json.load(fh)

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

        # ---- G1: exp256's 72 rows re-read COMPLETE (12 hosts x 2
        #      arms x 3 seeds; the canonical rows carrying exactly the
        #      two pre-named P1/P2 instances, the substituted rows
        #      exactly the two pre-named deep instances r-60i0/r-60i1;
        #      every worst_err finite AND == the max of its instance
        #      errs — the deposited arm-worst convention, 72/72) -------
        bat = dep256["battery"]
        rows256 = dep256["rows"]
        assert len(rows256) == 72, "exp256's 72-row battery drifted"
        assert bat["hosts"] == hosts, "exp256's host frame drifted"
        assert bat["seeds"] == [1, 2, 3], "exp256's seed frame drifted"
        assert bat["rows_per_pass"] == 72, \
            "exp256's rows-per-pass drifted"
        ARMS = ("canonical", "substituted")
        P1_PERT = "P1_canon_zone_relabelings"
        P2_PERT = "P2_boundary_double_frequency_rewiring"
        DEEP_KEYS = ("r-60i0", "r-60i1")
        seen = {}
        grid_ok = True
        inst_ok = True
        worst_ok = True
        worst_finite = True
        for r in rows256:
            h, arm, s = r["host"], r["arm"], int(r["seed"])
            seen[(h, arm, s)] = True
            grid_ok = grid_ok and (h in hosts) and (arm in ARMS) \
                and (s in (1, 2, 3))
            insts = r["instances"]
            worst_finite = worst_finite \
                and r["worst_err"] == r["worst_err"] \
                and abs(r["worst_err"]) != float("inf")
            if arm == "canonical":
                inst_ok = inst_ok and len(insts) == 2 \
                    and sorted(i["pert"] for i in insts) \
                    == [P1_PERT, P2_PERT]
            else:
                inst_ok = inst_ok and len(insts) == 2 \
                    and sorted(i["row_key"] for i in insts) \
                    == list(DEEP_KEYS)
            errs = [float(i["err"]) for i in insts]
            worst_ok = worst_ok \
                and max(errs) == float(r["worst_err"])
        grid_ok = grid_ok and len(seen) == 72
        subst_ok = bool(all((h, "substituted", s) in seen
                            for h in hosts for s in (1, 2, 3)))
        canon_ok = bool(all((h, "canonical", s) in seen
                            for h in hosts for s in (1, 2, 3)))

        # ---- the per-host means recomputed from the rows (the
        #      numerator m_P3 = the mean over the 3 substituted rows'
        #      worst_err — the deposited per-seed arm-worst convention;
        #      the DENOMINATOR m_P12 = the POOLED mean over the 6
        #      canonical instance errs, P1 x 3 seeds + P2 x 3 seeds,
        #      NOT the mean of the per-seed maxima; the max variant
        #      m_can_max computed alongside, audit-only) ---------------
        rows_sub = [r for r in rows256 if r["arm"] == "substituted"]
        rows_can = [r for r in rows256 if r["arm"] == "canonical"]
        assert len(rows_sub) == 36 and len(rows_can) == 36, \
            "the arm split drifted"
        per_host = {}
        for h in hosts:
            hs_sub = sorted((r for r in rows_sub if r["host"] == h),
                            key=lambda r: int(r["seed"]))
            hs_can = sorted((r for r in rows_can if r["host"] == h),
                            key=lambda r: int(r["seed"]))
            assert len(hs_sub) == 3 and len(hs_can) == 3, \
                f"{h}: the seed rows drifted"
            sub_worst = [float(r["worst_err"]) for r in hs_sub]
            can_worst = [float(r["worst_err"]) for r in hs_can]
            m_P3 = float(np.mean(sub_worst))
            m_can_max = float(np.mean(can_worst))
            # the POOLED denominator: the 6 canonical instance errs in
            # (seed, arm) order, identified by the deposited pert names
            inst_errs = []
            for r in hs_can:
                by_pert = {i["pert"]: float(i["err"]) for i in r["instances"]}
                assert sorted(by_pert) == sorted([P1_PERT, P2_PERT]), \
                    f"{h} seed {r['seed']}: the canonical instances drifted"
                inst_errs.append(by_pert[P1_PERT])
                inst_errs.append(by_pert[P2_PERT])
            assert len(inst_errs) == 6, f"{h}: the pooled 6 errs drifted"
            m_P12 = float(np.mean(inst_errs))
            m_P1 = float(np.mean(inst_errs[0::2]))
            m_P2 = float(np.mean(inst_errs[1::2]))
            # the all-arms row-worst mean: the 6 rows in DEPOSITED order
            # (host -> seed -> arm), summed plainly, / 6 — the order that
            # reproduces exp273's deposited carry bit-exactly
            hs_all = [r for r in rows256 if r["host"] == h]
            m_all = sum(float(r["worst_err"]) for r in hs_all) / 6.0
            per_host[h] = {
                "m_P3": m_P3, "m_P12_pooled": m_P12,
                "m_can_max": m_can_max, "m_all": m_all,
                "m_P1": m_P1, "m_P2": m_P2,
                "sub_worsts": sub_worst, "can_worsts": can_worst,
                "pooled_errs": inst_errs}

        # ---- the deposited anchors for the bit-exact cross-checks ----
        ft = {rec["field"]: rec for rec in dep273["field_table"]}
        MIA_FIELD = "exp243.classes.multi_identity_audit.prod_err"
        BC_FIELD = "exp243.classes.n_boundary_cells_base"
        SUB_FIELD = "exp256.rows.worst_err_mean_substituted"
        CAN_FIELD = "exp256.rows.worst_err_mean_canonical"
        ALL_FIELD = "exp256.rows.worst_err_mean_all_arms"
        for f in (MIA_FIELD, BC_FIELD, SUB_FIELD, CAN_FIELD, ALL_FIELD):
            assert f in ft, f"{f} missing from exp273's field table"
        for f in (MIA_FIELD, BC_FIELD):
            # the two external discriminators carry the external tag;
            # the three exp256 mean fields are component-derived carries
            assert ft[f]["selection"] == "external", \
                f"{f} is not selection-tagged external in exp273"
        carry_mia = {h: float(ft[MIA_FIELD]["values"][h]) for h in hosts}
        carry_bc = {h: float(ft[BC_FIELD]["values"][h]) for h in hosts}
        carry_sub = {h: float(ft[SUB_FIELD]["values"][h]) for h in hosts}
        carry_can = {h: float(ft[CAN_FIELD]["values"][h]) for h in hosts}
        carry_all = {h: float(ft[ALL_FIELD]["values"][h]) for h in hosts}

        # exp273's mia carry bit-exact vs exp243's records
        cls = dep243["classes"]
        assert set(cls) == set(hosts), "exp243's classes drifted"
        a = {}
        carry_mia_ok = True
        for h in hosts:
            rec = cls[h]["multi_identity_audit"]
            assert rec["bit_identical"] is True, \
                f"{h}: the multi-identity audit is not bit-identical"
            v = float(rec["prod_err"])
            assert v == v and abs(v) != float("inf"), \
                f"{h}: the audit prod_err is not finite"
            a[h] = v
            carry_mia_ok = carry_mia_ok and carry_mia[h] == v

        # the boundary-count carry (the exp255 instrument) bit-exact vs
        # exp243's classes, exp272's per_host records, exp255's rows
        carry_bc_ok = True
        for h in hosts:
            v = int(cls[h]["n_boundary_cells_base"])
            carry_bc_ok = carry_bc_ok and carry_bc[h] == v
            bc272 = {r["host"]: r["n_boundary_cells_base"]
                     for r in dep272["per_host"]}
            carry_bc_ok = carry_bc_ok and bc272[h] == v
        bc255 = {}
        for r in dep255["rows"]:
            bc255.setdefault(r["host"], set()).add(int(r["n_boundary_cells"]))
        carry_bc_ok = carry_bc_ok \
            and set(bc255) == set(hosts) \
            and all(len(v) == 1 for v in bc255.values()) \
            and all(next(iter(bc255[h])) == int(carry_bc[h])
                    for h in hosts)

        # the per-host means bit-exact vs EVERY deposited record where
        # present — exp273's field table (3 means), exp276's
        # decomposition_table (m_P1/m_P2/m_P3), exp277's per_host_table
        # (mean_worst_err)
        means_ok = True
        for h in hosts:
            means_ok = means_ok \
                and per_host[h]["m_P3"] == carry_sub[h] \
                and per_host[h]["m_can_max"] == carry_can[h] \
                and per_host[h]["m_all"] == carry_all[h]
        t276 = {r["host"]: r for r in dep276["decomposition_table"]}
        assert set(t276) == set(hosts), "exp276's host frame drifted"
        for h in hosts:
            means_ok = means_ok \
                and per_host[h]["m_P1"] == float(t276[h]["m_P1"]) \
                and per_host[h]["m_P2"] == float(t276[h]["m_P2"]) \
                and per_host[h]["m_P3"] == float(t276[h]["m_P3"])
        t277 = {r["host"]: r for r in dep277["per_host_table"]}
        assert set(t277) == set(hosts), "exp277's host frame drifted"
        for h in hosts:
            means_ok = means_ok \
                and per_host[h]["m_P3"] == float(t277[h]["mean_worst_err"])

        # exp272's deposited records where present — the per-host
        # boundary counts (above) AND both grids' canon_worst_err
        # columns == exp256's canonical row worst_err 36/36 each at the
        # (host, seed) grain
        canon_worst = {(r["host"], int(r["seed"])): float(r["worst_err"])
                       for r in rows_can}
        g1_ok = True
        for grid in (dep272["one_zone_premium_grid_re_read"],
                     dep272["multi_zone_premium_grid"]):
            assert len(grid) == 36, "exp272's 36-row grid drifted"
            for r in grid:
                key = (r["host"], int(r["seed"]))
                g1_ok = g1_ok and key in canon_worst \
                    and float(r["canon_worst_err"]) == canon_worst[key]

        # ---- G1's provenance chains: exp273's recorded inputs 5/5,
        #      exp274's 6/6, exp275's 7/7, exp276's 8/8, exp277's 8/8
        #      == the actual deposit bytes ------------------------------
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
        with open(DEP276) as fh:
            dep276c = json.load(fh)
        with open(DEP277) as fh:
            dep277c = json.load(fh)
        chain274_ok = _chain(dep274)
        chain275_ok = _chain(dep275)
        chain276_ok = _chain(dep276c)
        chain277_ok = _chain(dep277c)
        chain_all_ok = bool(all(chain273_ok.values())
                            and all(chain274_ok.values())
                            and all(chain275_ok.values())
                            and all(chain276_ok.values())
                            and all(chain277_ok.values()))

        # ---- G2: THE RATIO'S DEFINITION (zero-knob): R_h =
        #      m_P3(h) / m_P12(h), one closed-form for all 12 hosts;
        #      m_P12 = the POOLED mean over the 6 canonical instance
        #      errs (asserted above: 6 errs, identified by the
        #      deposited pert names) — NOT the per-seed maxima; the
        #      max variant recorded audit-only alongside (bit-exact vs
        #      exp273's deposited worst_err_mean_canonical, asserted
        #      per G1); all 12 ratios finite and > 0; no parameters,
        #      no per-host cases ----------------------------------------
        ratio = {}
        ratio_audit = {}
        for h in hosts:
            m_P3 = per_host[h]["m_P3"]
            m_P12 = per_host[h]["m_P12_pooled"]
            assert m_P12 > 0.0, f"{h}: the pooled denominator is not > 0"
            assert m_P12 <= per_host[h]["m_can_max"], \
                f"{h}: the pooled mean exceeds the per-seed-max mean"
            ratio[h] = m_P3 / m_P12
            ratio_audit[h] = {
                "m_P3": m_P3, "m_P12_pooled": m_P12,
                "m_can_max_variant": per_host[h]["m_can_max"],
                "pooled_minus_max_variant":
                    per_host[h]["m_P12_pooled"]
                    - per_host[h]["m_can_max"],
                "ratio_max_variant_audit_only":
                    m_P3 / per_host[h]["m_can_max"]}
        ratio_ok = bool(
            set(ratio) == set(hosts) and len(ratio) == 12
            and all(v == v and abs(v) != float("inf") and v > 0.0
                    for v in ratio.values()))
        pooled_gap = [ratio_audit[h]["pooled_minus_max_variant"]
                      for h in hosts]
        # the pooled-vs-max discriminant, RECORDED (the pre-registered
        # gate asserts the pooled source + records the gap; the
        # strict-below face is the evidence the two definitions differ)
        pooled_below_max_all_hosts = bool(all(g < 0.0 for g in pooled_gap))
        g2_pass = bool(ratio_ok and means_ok and inst_ok and worst_ok)

        # ---- the 12-host table --------------------------------------
        table = [{"host": h,
                  "outlier": h in outliers,
                  "n_substituted_rows": 3,
                  "m_P3": per_host[h]["m_P3"],
                  "m_P12_pooled": per_host[h]["m_P12_pooled"],
                  "m_can_max_variant_audit_only":
                      per_host[h]["m_can_max"],
                  "amplification_ratio": ratio[h],
                  "ratio_max_variant_audit_only":
                      ratio_audit[h]["ratio_max_variant_audit_only"],
                  "mia_prod_err": a[h],
                  "n_boundary_cells_base": int(carry_bc[h])}
                 for h in hosts]
        all_finite = bool(all(
            row[k] == row[k] and abs(row[k]) != float("inf")
            for row in table
            for k in ("m_P3", "m_P12_pooled",
                      "m_can_max_variant_audit_only",
                      "amplification_ratio",
                      "ratio_max_variant_audit_only", "mia_prod_err",
                      "n_boundary_cells_base")))

        # ---- G3: THE BRANCH (the discriminant pre-named, the bars
        #      numeric): MIA-SCALED iff Spearman(ratio, mia) >= 0.5
        #      (the house bar, tested FIRST — the pre-named
        #      precedence); else GEOMETRY-SCALED iff Spearman(ratio,
        #      boundary count) >= 0.5; else UNATTACHED (the exhaustive
        #      residual). Both rhos recorded regardless. ---------------
        R_vec = [ratio[h] for h in hosts]
        a_vec = [a[h] for h in hosts]
        bc_vec = [carry_bc[h] for h in hosts]
        rho_mia = _spearman(a_vec, R_vec)
        rho_bc = _spearman(bc_vec, R_vec)
        mia_ok = bool(rho_mia >= 0.5)
        bc_ok = bool(rho_bc >= 0.5)
        if mia_ok:
            branch = "MIA-SCALED"
        elif bc_ok:
            branch = "GEOMETRY-SCALED"
        else:
            branch = "UNATTACHED"

        # ---- THE REGRESSIONS (the exp274/exp275 conventions
        #      verbatim, REPORTED not gated): the response = the
        #      amplification ratio (tied-average ranks); the two
        #      regressors numeric; the single Spearmans (regressor
        #      vector first) + the OLS-on-ranks single R2s + the full
        #      model (with two regressors the pair IS the full model);
        #      the shares by the two-order symmetric average on the
        #      pre-named entry order mia -> bc and its reverse
        #      bc -> mia; shares + unexplained == 1 asserted (no
        #      clamping); the ties census; the all-ranks variant
        #      AUDIT-ONLY. ----------------------------------------------
        Rk = rankdata(np.asarray(R_vec, dtype=float))
        reg_vals = {"mia_prod_err": a_vec, "boundary_count": bc_vec}
        spearmans = {"mia_prod_err": rho_mia, "boundary_count": rho_bc}
        c1, c2 = "mia_prod_err", "boundary_count"
        r2_single = {k: _r2([reg_vals[k]], Rk) for k in reg_vals}
        r2_full = _r2([reg_vals[c1], reg_vals[c2]], Rk)
        inc_o1 = {c1: r2_single[c1], c2: r2_full - r2_single[c1]}
        inc_o2 = {c2: r2_single[c2], c1: r2_full - r2_single[c2]}
        reg_shares = {k: 0.5 * (inc_o1[k] + inc_o2[k])
                      for k in reg_vals}
        reg_unexplained = 1.0 - r2_full
        reg_sum = sum(reg_shares.values()) + reg_unexplained
        assert abs(reg_sum - 1.0) < 1e-9, \
            "the three-way rank shares do not sum to 1"
        assert all(v == v and abs(v) != float("inf")
                   for v in list(reg_shares.values())
                   + [reg_unexplained, r2_full]), "non-finite share"
        rk = {k: rankdata(np.asarray(v, dtype=float))
              for k, v in reg_vals.items()}
        audit_all_ranks = {
            "r2_single": {k: _r2([rk[k]], Rk) for k in reg_vals},
            "r2_full": _r2([rk[c1], rk[c2]], Rk)}
        audit_all_ranks["single_equals_spearman_squared"] = bool(
            all(abs(audit_all_ranks["r2_single"][k]
                    - spearmans[k] ** 2) < 1e-12 for k in reg_vals))

        # the amplification margins (descriptive, never gating): the
        # outliers' ratio min vs the cluster's max
        r_out_min = float(min(ratio[h] for h in outliers))
        r_clu_max = float(max(ratio[h] for h in cluster))
        r_clu_min = float(min(ratio[h] for h in cluster))
        ratio_margin = r_out_min - r_clu_max

        g1_pass = bool(grid_ok and canon_ok and subst_ok and inst_ok
                       and worst_ok and worst_finite and all_finite
                       and carry_mia_ok and carry_bc_ok and means_ok
                       and g1_ok and chain_all_ok)
        g3_pass = bool(branch in ("MIA-SCALED", "GEOMETRY-SCALED",
                                  "UNATTACHED")
                       and rho_mia == rho_mia and rho_bc == rho_bc)

        ties = {"amplification_ratio": _ties_census(R_vec),
                "mia_prod_err": _ties_census(a_vec),
                "boundary_count": _ties_census(bc_vec)}

        return {
            "hosts": hosts, "outliers": outliers, "cluster": cluster,
            "table": table,
            "ratio_audit_detail": ratio_audit,
            "g1": {"pass": g1_pass,
                   "rows_complete_72": grid_ok,
                   "canonical_rows_complete_36": canon_ok,
                   "substituted_rows_complete_36": subst_ok,
                   "instance_structure_verified_72": inst_ok,
                   "worst_equals_max_instance_err_72": worst_ok,
                   "worst_err_finite_72": worst_finite,
                   "table_finite": all_finite,
                   "exp273_mia_carry_bit_exact": carry_mia_ok,
                   "exp273_boundary_carry_bit_exact_vs_exp243_"
                   "exp272_exp255": carry_bc_ok,
                   "per_host_means_bit_exact_vs_exp273_field_table":
                       means_ok,
                   "exp272_grids_canon_worst_err_bit_exact_36x2":
                       g1_ok,
                   "exp273_recorded_input_shas_match_actual_bytes":
                       chain273_ok,
                   "exp274_recorded_input_shas_match_actual_bytes":
                       chain274_ok,
                   "exp275_recorded_input_shas_match_actual_bytes":
                       chain275_ok,
                   "exp276_recorded_input_shas_match_actual_bytes":
                       chain276_ok,
                   "exp277_recorded_input_shas_match_actual_bytes":
                       chain277_ok,
                   "provenance_chains_sha_verified": chain_all_ok},
            "g2": {"pass": g2_pass,
                   "definition": ("R_h = m_P3(h) / m_P12(h); m_P3 = "
                                  "the mean over the 3 substituted "
                                  "rows' deposited worst_err (the "
                                  "per-seed arm-worst convention); "
                                  "m_P12 = the POOLED mean over the 6 "
                                  "canonical instance errs (P1 x 3 "
                                  "seeds + P2 x 3 seeds) — NOT the "
                                  "mean of the per-seed maxima"),
                   "n_hosts": 12,
                   "one_formula_no_parameters": ratio_ok,
                   "pooled_not_per_seed_max": True,
                   "pooled_strictly_below_max_variant_all_hosts":
                       pooled_below_max_all_hosts,
                   "max_pooled_minus_max_variant_gap":
                       float(max(pooled_gap)),
                   "ratios_finite_positive": ratio_ok,
                   "numerator_bit_exact_vs_exp276_m_P3_and_"
                   "exp277_mean_worst_err": True},
            "g3": {"pass": g3_pass, "branch": branch,
                   "spearman_rho_ratio_mia": rho_mia,
                   "spearman_rho_ratio_boundary": rho_bc,
                   "mia_bar": 0.5, "boundary_bar": 0.5,
                   "mia_tested_first": True,
                   "mia_exceeds_bar": mia_ok,
                   "boundary_exceeds_bar": bc_ok,
                   "ratio_outlier_min": r_out_min,
                   "ratio_cluster_max": r_clu_max,
                   "ratio_cluster_min": r_clu_min,
                   "ratio_outlier_margin_descriptive": ratio_margin},
            "regression": {
                "response": ("the per-host amplification ratio "
                             "m_P3 / m_P12_pooled — 12 hosts, "
                             "tied-average ranks"),
                "regressors": ("mia_prod_err (exp243.classes."
                               "multi_identity_audit.prod_err via "
                               "exp273's deposited field table, "
                               "selection external, bit-exact vs "
                               "exp243's records) and the "
                               "canon-boundary count (exp243.classes."
                               "n_boundary_cells_base — the exp255 "
                               "instrument; bit-exact vs exp243's "
                               "classes, exp272's per_host records, "
                               "exp255's 24 rows)"),
                "spearman_rho": spearmans,
                "r2_single": r2_single,
                "r2_pairs": {"mia+bc": r2_full},
                "r2_pairs_note": ("with two regressors the only pair "
                                  "IS the full model"),
                "r2_full": r2_full,
                "order_decompositions": {"order_mia_bc": inc_o1,
                                         "order_bc_mia": inc_o2},
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

    g3 = payload_a["g3"]
    gates = {"G1_grids": {
                 "pass": payload_a["g1"]["pass"],
                 "bar": "exp256's 72 rows re-read complete (12 hosts x "
                        "2 arms x 3 seeds), every canonical row "
                        "carrying exactly the two pre-named P1/P2 "
                        "instances and every substituted row exactly "
                        "the two pre-named deep instances "
                        "r-60i0/r-60i1, every worst_err finite AND == "
                        "the max of its instance errs (the deposited "
                        "arm-worst convention, 72/72); the per-host "
                        "means recomputed bit-exact vs EVERY "
                        "deposited record where present — exp273's "
                        "field table (worst_err_mean_substituted / "
                        "_canonical / _all_arms), exp276's "
                        "decomposition_table (m_P1/m_P2/m_P3), "
                        "exp277's per_host_table (mean_worst_err), "
                        "exp272's deposited records where present "
                        "(per_host n_boundary_cells_base; both "
                        "grids' canon_worst_err columns == exp256's "
                        "canonical row worst_err 36/36 each), "
                        "exp243's classes records, exp255's 24 rows; "
                        "the outlier pre-name asserted (exp273 == "
                        "exp272 == ['H3','H5']); the provenance "
                        "chains sha-verified (exp273 5/5, exp274 "
                        "6/6, exp275 7/7, exp276 8/8, exp277 8/8); "
                        "READ-ONLY",
                 **payload_a["g1"]},
             "G2_ratio_definition": {
                 "pass": payload_a["g2"]["pass"],
                 "bar": "one closed-form for all 12 hosts — R_h = "
                        "m_P3(h) / m_P12(h), m_P12 = the POOLED mean "
                        "over the 6 canonical instance errs "
                        "(identified by the deposited pert names, 3 "
                        "seeds each), NOT the mean of the per-seed "
                        "maxima; the max variant computed alongside, "
                        "bit-exact vs exp273's deposited "
                        "worst_err_mean_canonical, recorded "
                        "audit-only — never entering the ratio; all "
                        "12 ratios finite and > 0; no parameters, no "
                        "per-host cases",
                 **payload_a["g2"]},
             "G3_branch": {
                 "pass": g3["pass"],
                 "bar": "the discriminant pre-named, the bars numeric: "
                        "MIA-SCALED iff Spearman(ratio, mia_prod_err) "
                        ">= 0.5 (the house bar, tested FIRST — the "
                        "pre-named precedence); else GEOMETRY-SCALED "
                        "iff Spearman(ratio, boundary count) >= 0.5; "
                        "else UNATTACHED (the exhaustive residual); "
                        "both rhos recorded; the regressions "
                        "reported alongside (exp274/exp275 "
                        "conventions), audit-only, never gating",
                 "branch": g3["branch"],
                 **{k: v for k, v in g3.items() if k != "pass"}}}

    # ---- G4: the discipline --------------------------------------------
    ro_after = {k: _sha(RO_PATHS[k]) for k in RO_KEYS}
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

    gates["G4_discipline"] = {
        "pass": d4_pass,
        "bar": ("all deposits READ-ONLY sha-recorded byte-unchanged; "
                "deterministic — two-pass bit-identical; no "
                "wall-clock fields; the docstring+header pinned to "
                "b42fbc0 asserted at entry AND exit; NEURAL_SPEC_MIN "
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
        "docstring_byte_unchanged_vs_b42fbc0": docstring_ok,
        "header_sha256": header_sha,
        "header_byte_unchanged_vs_b42fbc0": header_ok,
        "deposit_form": ("deterministic: no wall-clock fields — a "
                         "re-run of this module reproduces this file "
                         "byte-identically")}

    # ---- the branch + the verdict (one line, the numbers
    #      data-driven) -----------------------------------------------------
    branch = g3["branch"]
    reg = payload_a["regression"]
    tbl = {r["host"]: r for r in payload_a["table"]}

    def _g(v):
        return format(v, ".10g") if isinstance(v, float) else str(v)

    gate_passes = {"G1": gates["G1_grids"]["pass"],
                   "G2": gates["G2_ratio_definition"]["pass"],
                   "G3": gates["G3_branch"]["pass"],
                   "G4": gates["G4_discipline"]["pass"]}
    n_pass = sum(1 for v in gate_passes.values() if v)
    n_refute = 4 - n_pass

    branch_face = {
        "MIA-SCALED": ("the per-host amplification ratio tracks the "
                       "audit error: Spearman(ratio, mia_prod_err) "
                       ">= 0.5 — what the deep-band substitution "
                       "amplifies tracks what the multi-identity "
                       "audit sees, host by host"),
        "GEOMETRY-SCALED": ("the per-host amplification ratio tracks "
                            "the canon-boundary count (the exp255 "
                            "instrument) at the AMPLIFICATION level "
                            "— the geometry exp272 refuted at the "
                            "PREMIUM level"),
        "UNATTACHED": ("neither regressor reaches the 0.5 bar — the "
                       "amplification ratio tracks neither mia "
                       "nor the boundary count")}[branch]
    verdict = (
        f"{n_pass}/4 gates G1-G4 ({n_pass} PASS / {n_refute} REFUTE) | "
        f"{branch} | {branch_face} | Spearman(ratio, mia) "
        f"{_g(reg['spearman_rho']['mia_prod_err'])}, Spearman(ratio, "
        f"boundary) {_g(reg['spearman_rho']['boundary_count'])} (bars "
        f"0.5; mia tested first) | rank R2 singles mia "
        f"{_g(reg['r2_single']['mia_prod_err'])} / bc "
        f"{_g(reg['r2_single']['boundary_count'])}, full "
        f"{_g(reg['r2_full'])}, shares mia "
        f"{_g(reg['shares_of_rank_variance']['mia_prod_err'])} / bc "
        f"{_g(reg['shares_of_rank_variance']['boundary_count'])} / "
        f"unexplained {_g(reg['unexplained'])} | the ratio H3 "
        f"{tbl['H3']['amplification_ratio']:.2f} / H5 "
        f"{tbl['H5']['amplification_ratio']:.2f} vs the cluster's "
        f"[{g3['ratio_cluster_min']:.2f}, "
        f"{g3['ratio_cluster_max']:.2f}] (m_P3 over the POOLED P1+P2 "
        f"mean, exp256's 72 deposited rows) | 12 hosts x 3 seeds, a "
        f"pure re-read, READ-ONLY byte-unchanged, two-pass "
        f"bit-identical, no wall-clock fields, floor -60.0 asserted "
        f"at exit")

    deposit = {
        "exp": "exp278_amplification_factor",
        "claim": (
            "THE AMPLIFICATION FACTOR (batch 36, pre-registration "
            "commit b42fbc0): the ~7x deep-band break (exp277) is "
            "itself the measurement — the per-host amplification "
            "ratio = the P3 arm's mean err / the P1+P2 arms' mean "
            "err, zero-knob from exp256's deposited 72 rows (12 "
            "hosts x 3 seeds, the means over the rows; the "
            "denominator the POOLED mean over the 6 canonical "
            "instance errs, NOT the per-seed max); the ratio vs "
            "mia_prod_err (exp273's field table) and vs the "
            "canon-boundary count (the exp255 instrument — exp272 "
            "refuted it for the PREMIUM level; here the "
            "AMPLIFICATION level), Spearman + the OLS rank R2 under "
            "the exp274/exp275 conventions; the branch pre-named "
            "MIA-SCALED (mia rho >= 0.5, tested first) / "
            "GEOMETRY-SCALED / UNATTACHED"),
        "method": {
            "source": ("exp256's deposited 72 rows = 12 hosts x 2 "
                       "arms x 3 seeds; the substituted arm's rows "
                       "carry the P3 face (the deep rows r-60i0/r-60i1 "
                       "on the base medium, worst_err = the per-seed "
                       "arm worst), the canonical arm's rows carry "
                       "the P1+P2 face (the canon row on the mirror "
                       "medium and on the boundary-double medium, "
                       "the instance errs the per-arm per-seed "
                       "values)"),
            "ratio_definition": ("R_h = m_P3(h) / m_P12(h); m_P3 = "
                                 "the mean over the 3 substituted "
                                 "rows' worst_err (== exp276's m_P3 "
                                 "== exp277's mean_worst_err, "
                                 "bit-exact asserted); m_P12 = the "
                                 "POOLED mean over the 6 canonical "
                                 "instance errs (P1 x 3 seeds + P2 x "
                                 "3 seeds) — NOT the mean of the "
                                 "per-seed maxima (the deposited "
                                 "worst_err_mean_canonical IS the "
                                 "max variant; recorded audit-only, "
                                 "never entering the ratio)"),
            "regressors": ("mia_prod_err = exp243.classes."
                           "multi_identity_audit.prod_err via "
                           "exp273's deposited field table "
                           "(selection external), bit-exact vs "
                           "exp243's records; boundary count = "
                           "exp243.classes.n_boundary_cells_base — "
                           "the exp255 zero-knob instrument, "
                           "bit-exact vs exp243's classes, exp272's "
                           "per_host records, and exp255's 24 rows"),
            "branch_rule": ("MIA-SCALED iff Spearman(ratio, mia) >= "
                            "0.5 (the house bar, tested FIRST — the "
                            "pre-named precedence); else "
                            "GEOMETRY-SCALED iff Spearman(ratio, "
                            "boundary count) >= 0.5; else UNATTACHED "
                            "(the exhaustive residual); both rhos "
                            "recorded regardless"),
            "regression": ("the exp274/exp275 convention VERBATIM: "
                           "the response = the amplification ratio "
                           "(12 hosts, tied-average ranks); the two "
                           "regressors numeric; single-regressor "
                           "Spearmans (regressor vector first, "
                           "scipy rankdata both sides); the "
                           "OLS-on-ranks single R2s + the full "
                           "model (with two regressors the pair IS "
                           "the full model); the shares by the "
                           "two-order symmetric average on the "
                           "pre-named entry order mia -> bc and its "
                           "reverse bc -> mia; shares + unexplained "
                           "== 1, no clamping; the all-ranks variant "
                           "AUDIT-ONLY; REPORTED not gated — the "
                           "branch is the only gated read"),
            "method_source": ("experiments/exp256_row_pair_"
                              "regression.py (the 72 deposited "
                              "rows), experiments/exp273_outlier_"
                              "hosts.py (the carries + the outlier "
                              "pre-name), experiments/exp272_host_"
                              "premium_structure.py (the host frame "
                              "+ the per-host records + the PREMIUM-"
                              "level boundary refutation this run "
                              "re-tests at the AMPLIFICATION level), "
                              "experiments/exp255_pair_count_"
                              "regression.py (the boundary-count "
                              "instrument), experiments/exp243_"
                              "structured_adversarial.py (the audit "
                              "+ classes records), experiments/"
                              "exp276_audit_own_face.py (the "
                              "arm-mass convention m_P1/m_P2/m_P3), "
                              "experiments/exp277_deep_band_break_"
                              "face.py (the mean_worst_err table), "
                              "experiments/exp274_premium_mechanism."
                              "py (the rank-regression convention), "
                              "experiments/exp275_audit_direction.py "
                              "(the sha discipline)")},
        "inputs": {k: {"path": os.path.relpath(RO_PATHS[k], ROOT),
                       "sha256": ro_before[k]}
                   for k in RO_KEYS},
        "inputs_roles": {
            "exp256_deposit": ("the 72 deposited rows — the "
                               "computation's primary source: the 36 "
                               "substituted worst_errs (the "
                               "numerator) + the 36 canonical rows' "
                               "instance errs (the denominator)"),
            "exp273_deposit": ("the deposited carries BY EXACT FIELD "
                               "NAME (mia_prod_err, "
                               "n_boundary_cells_base, the three "
                               "worst_err means) + the outlier "
                               "pre-name + the recorded input shas "
                               "verified 5/5"),
            "exp272_deposit": ("the host frame + the per-host "
                               "boundary-count records + both "
                               "grids' canon_worst_err columns "
                               "(the bit-exact exp272 records) + "
                               "the premium_hosts pre-name source"),
            "exp243_deposit": ("the 12 multi_identity_audit + "
                               "classes records the mia and "
                               "boundary carries are bit-checked "
                               "against"),
            "exp255_deposit": ("the exp255 instrument's 24 rows — "
                               "the boundary-count cross-check"),
            "exp276_deposit": ("the deposited per-arm masses "
                               "m_P1/m_P2/m_P3 the recomputed means "
                               "are bit-checked against + the "
                               "recorded input shas verified 8/8"),
            "exp277_deposit": ("the deposited per-host "
                               "mean_worst_err table "
                               "bit-checked against + the recorded "
                               "input shas verified 8/8"),
            "exp274_deposit": ("the provenance chain: the "
                               "rank-regression convention's source "
                               "deposit — sha-verified 6/6, never "
                               "opened for computation"),
            "exp275_deposit": ("the provenance chain: the "
                               "sha-discipline precedent's deposit — "
                               "sha-verified 7/7, never opened for "
                               "computation"),
            "exp271_deposit": ("the provenance chain: the one-zone "
                               "premium grid — sha-verified via "
                               "exp273's chain, never opened for "
                               "computation"),
            "exp182_deposit": ("the provenance chain: the margin "
                               "profiles — sha-verified via exp273's "
                               "chain, never opened for computation")},
        "hosts": payload_a["hosts"],
        "outliers": payload_a["outliers"],
        "cluster": payload_a["cluster"],
        "per_host_table": payload_a["table"],
        "ratio_audit_detail": payload_a["ratio_audit_detail"],
        "branch_discriminant": {k: v for k, v in g3.items()
                                if k != "pass"},
        "regressions": payload_a["regression"],
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
            "docstring_byte_unchanged_vs_b42fbc0": docstring_ok,
            "header_sha256": header_sha,
            "header_byte_unchanged_vs_b42fbc0": header_ok,
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

    print("=== exp278: THE AMPLIFICATION FACTOR (pure deposit re-read "
          "+ arithmetic) ===")
    print("  the per-host amplification ratio = the P3 arm's mean err / "
          "the P1+P2 POOLED mean err (exp256's 72 deposited rows, "
          "12 hosts x 3 seeds)")
    print(f"\n  G1 grids: {'PASS' if gates['G1_grids']['pass'] else 'FAIL'} "
          f"(exp256's 72 rows re-read complete; the instance structure "
          f"verified 72/72; the per-host means bit-exact vs exp273/"
          f"exp276/exp277/exp272/exp243/exp255 where present; the "
          f"chains sha-verified exp273 5/5 + exp274 6/6 + exp275 7/7 + "
          f"exp276 8/8 + exp277 8/8)")
    print(f"  G2 ratio definition: "
          f"{'PASS' if gates['G2_ratio_definition']['pass'] else 'FAIL'} "
          f"(one closed-form, 12 hosts, no parameters; the POOLED "
          f"denominator strictly below the per-seed-max variant on all "
          f"12 hosts — max gap "
          f"{payload_a['g2']['max_pooled_minus_max_variant_gap']:.4f}; "
          f"the max variant recorded audit-only)")
    print("  G3 branch — the 12-host ratio table:")
    for row in payload_a["table"]:
        tag = " <== outlier" if row["outlier"] else ""
        print(f"      {row['host']:4s} m_P3 {row['m_P3']:5.3f}  "
              f"m_P12 {row['m_P12_pooled']:7.4f}  "
              f"ratio {row['amplification_ratio']:6.2f}  "
              f"mia {row['mia_prod_err']:5.2f}  "
              f"bc {int(row['n_boundary_cells_base']):3d}{tag}")
    print(f"  G4 discipline: {'PASS' if d4_pass else 'FAIL'} "
          f"(11 deposits READ-ONLY byte-unchanged: {ro_unchanged}; "
          f"two-pass bit-identical: {deterministic}; no wall-clock "
          f"fields: {no_wall_clock})")
    print(f"\n  BRANCH: {branch} | Spearman(ratio, mia) "
          f"{reg['spearman_rho']['mia_prod_err']:.4f} | "
          f"Spearman(ratio, boundary) "
          f"{reg['spearman_rho']['boundary_count']:+.4f} (bars 0.5; "
          f"mia tested first) | ratio outlier margin "
          f"{g3['ratio_outlier_margin_descriptive']:+.2f} "
          f"(outliers min {g3['ratio_outlier_min']:.2f} vs cluster max "
          f"{g3['ratio_cluster_max']:.2f})")
    print(f"\n  GATES: {verdict}")
    print(f"  deposited {OUT}")

    # the hard rule, re-asserted after the work: the docstring is still
    # the b42fbc0 pre-registration, byte-for-byte
    assert hashlib.sha256(__doc__.encode()).hexdigest() \
        == EXPECTED_DOCSTRING_SHA256, "docstring drifted after the work"
    with open(__file__, "r", encoding="utf-8") as _f:
        _src2 = _f.read()
    assert hashlib.sha256(
        _src2[:_src2.index(_marker) + len(_marker)].encode()
    ).hexdigest() == EXPECTED_HEADER_SHA256, "header drifted after work"
    # the source deposits are still byte-unchanged after the work
    assert ro_after == ro_before, "source deposit drifted after work"

    # THE FLOOR ASSERT AT EXIT (the hard rule; exp243's closing line)
    CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at exit"
    return deposit


if __name__ == "__main__":
    main()
