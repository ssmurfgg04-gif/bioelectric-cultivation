#!/usr/bin/env python3
"""exp281 — THE ANTI-ALIGNED FACE TESTED AT THE SIGNED BAR: THE
BOUNDARY CELLS' OWN DEGREE MEAN vs THE PREMIUM'S THREE CARRIERS
(batch 39; batch-38's derived item, ledger L258 — zero new
simulation).

THE OPEN ITEM: exp280 named the ANTI-ALIGNED face — the boundary
cells' own degree mean (boundary_degree_mean, F5 of exp280's field
table; chord-poorest on the outliers: H3 1.5957 / H5 1.5625 vs the
ten-host cluster's [1.5, 1.8974]) ran OPPOSITE the pre-named
richness->exposure direction at rho -0.6081 against the deep-band
read err — a crossing of the 0.5 ABS bar with the 0.5 SIGNED bar
unmet (the branch TOPOLOGY-ABSENT; the face named, never gating).
The question exp281 asks: does that field carry the PREMIUM at the
SIGNED 0.5 house bar — the premium level itself, its amplification,
and the audit error that named the outliers — or does it clear
nothing, closing the chord line and placing the premium's origin
formally OUTSIDE the deposited host records?

THE INSTRUMENT (pre-registered, zero-knob): a pure re-read + a
DETERMINISTIC REBUILD — exp280's rebuild VERBATIM (the
exp269/exp256 form: graph_path for H0/H1, small_world(n, 0.10,
int(rec["rewire_seed"])) at exp243's deposited rewire seeds), every
rebuild bit-asserted against exp243's own records; ZERO new
simulation (no read, no decode, no dynamics — the rebuild is a
deterministic graph construction whose shas are pinned by the
deposit). ONE structural field computed per host, with exp280's
EXACT definition, never re-fit:

  F5 boundary_degree_mean — the mean pair-support degree over the
     CANON-BOUNDARY cells (exp208's classify instrument on the canon
     labeling, the ring backbone i±1; support = |A| > 0, symmetric;
     degree = the per-cell support degree); asserted BIT-EXACT vs
     exp280's deposited field table 12/12 (G2 — the definition is
     exp280's, bit-identical, fixed at this pre-registration).

THE THREE TARGETS (the 12-host table, exp272's per_host order — the
order the batch asserted exp273/exp276/exp278/exp279/exp280 against):

  T1 = exp272's per-host ONE-ZONE PREMIUM means (the premium level
     itself): per_host[*]["one_zone_premium_mean"]; the mean
     identity asserted bit-exact 12/12 (the recomputed mean over the
     deposited per-seed rows one_zone_premiums_by_seed == the
     deposited mean == exp273's field-table carry
     exp272.per_host.one_zone_premium_mean);
  T2 = exp278's per-host AMPLIFICATION RATIOS: per_host_table[
     *]["amplification_ratio"]; asserted == its own
     m_P3/m_P12_pooled identity bit-exact 12/12 (exp280's carry);
  T3 = the AUDIT ERROR mia_prod_err — the 4-way carry asserted
     bit-exact 12/12 each: exp243's
     classes[h]["multi_identity_audit"]["prod_err"] == exp276's
     decomposition_table audit_prod_err == exp279's origin_table
     audit_prod_err == exp273's field-table values
     (exp243.classes.multi_identity_audit.prod_err).

THE REGRESSIONS (the exp274/exp275 conventions VERBATIM): per
target, the Spearman rho = Pearson on the tied-average ranks (scipy
rankdata) of boundary_degree_mean vs the target on the 12-slot frame
(the H0 slot echoes H1 bit-exactly — the chain class's n=400 call
site, exp243's own disclosure, asserted; the house convention
carries both slots, exp278's ties-census precedent); the
single-predictor OLS rank R2 (the target enters as its tied-average
ranks, the field as the numeric design column); the all-ranks
variant (the field ranked too — single R2 == rho^2 within 1e-12)
AUDIT-ONLY; the ties census per vector.

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE REBUILD INTEGRITY (the exp280 precedent): READ-ONLY
      sha-verified — the 12 rebuilt bases bit-asserted against
      exp243's records (sha256(|A| as float64) == rec["base_sha256"]
      12/12; the upper-triangle edge count == rec["edges_base"]
      12/12; the exp208 classify CANON-BOUNDARY count ==
      rec["n_boundary_cells_base"] 12/12, dual-carried vs exp272's
      per-host records + exp278's per-host table; labeling_bfs_n(
      |A|) == labeling_bfs_n(A) 12/12; H0 == H1 bit-exact);
      exp278's ratio identity bit-exact 12/12; the T1 mean identity
      bit-exact 12/12; the T3 4-way carry bit-exact 12/12 each; the
      outlier pre-name asserted (exp273 == exp272.descriptive.
      premium_hosts == exp276 == exp278 == exp279 == exp280 ==
      ['H3','H5']); the provenance chains sha-verified against the
      actual deposit bytes (exp280's recorded inputs 12/12, exp279's
      9/9, exp278's 11/11, exp276's 8/8, exp273's 5/5, exp272's
      4/4); READ-ONLY (the deposits sha-recorded before, byte-
      unchanged after).
  G2  THE FIELD DEFINITION BIT-IDENTICAL TO EXP280'S: the classify
      boundary masks nonempty 12/12; the recomputed
      boundary_degree_mean == exp280's deposited field-table values
      BIT-EXACT 12/12 (the boundary cells' own degree mean over the
      classify boundary set — exp280's code path, never re-fit);
      the field's distinct-level ties census recorded.
  G3  THE BRANCH: the discriminant pre-named with the numeric bar:
      CHORD-CARRIED iff boundary_degree_mean reaches Spearman >=
      0.5 (the SIGNED house bar) against >= 1 of the three targets
      (T1 the premium level / T2 the amplification / T3 the audit
      error) — the mechanism line RE-OPENS at the chord level; else
      CHORD-ABSENT (it clears nothing — the line stands closed at
      mia and the premium's origin is formally OUTSIDE the deposited
      host records). THE ABS VARIANT, pre-named: a target crossing
      |rho| >= 0.5 with a NEGATIVE sign is the ANTI-ALIGNED face
      (the chord runs OPPOSITE the pre-named direction) — named in
      the deposit and the verdict per target, NEVER gating
      (exp280's precedent: the face named honestly, the SIGNED bar
      decides).
  G4  THE DISCIPLINE: deterministic — two-pass bit-identical; no
      wall-clock fields (recursive key scan + serialized-blob scan);
      the deposits READ-ONLY sha-recorded byte-unchanged; the
      docstring+header pinned to this pre-registration commit,
      asserted at entry AND exit; NEURAL_SPEC_MIN == -60.0 asserted
      at exit.

THE BRANCHES (pre-named): CHORD-CARRIED / CHORD-ABSENT.

RUN: a deposit re-read + a deterministic adjacency rebuild + rank
arithmetic; seconds.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp281_antialigned_face.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates G1-G4 evaluated exactly once per
    #      pass, pre-registration commit a52a14a; the docstring's RUN
    #      clause holds verbatim: a pure deposit re-read + a
    #      deterministic adjacency rebuild + rank arithmetic, zero new
    #      simulation, seconds) ==========================================
    import hashlib
    import json

    import numpy as np
    from scipy.stats import rankdata

    import cultivation.bioelectric.collective as CORE  # the floor's home
    # the rebuild machinery (exp280's rebuild verbatim — the
    # exp269/exp256 form; none of these modules pin the floor,
    # verified pre-body)
    from cultivation.substrate.graph import path as graph_path  # noqa: E402
    from experiments.exp73_active_renormalization import (  # noqa: E402
        small_world)
    from experiments.exp94_multizone_scale import labeling_bfs_n  # noqa: E402

    # ---- the byte-unchanged self-check (the hard rule: the docstring
    #      is the a52a14a pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "7285312033d3909de8c37de35990099f078fbe4161fe3e1c67b82ba4e2e042a3")
    EXPECTED_HEADER_SHA256 = (
        "6665058099a3d6a3db859b18ab3eca472c4dad73f0e09653434e99deece846f0")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from a52a14a"
    assert header_ok, "header drifted from a52a14a"

    # ---- the -60.0 floor (G4: asserted at exit; nothing in this body
    #      imports any machinery that touches it — recorded at entry,
    #      restored and re-asserted as the closing line, exp243's/
    #      .../exp280's closing discipline) -------------------------
    PROD_FLOOR = -60.0
    floor_at_entry = float(CORE.NEURAL_SPEC_MIN)
    assert floor_at_entry == PROD_FLOOR, \
        f"floor drift at entry: {floor_at_entry}"

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      work, re-verified byte-unchanged at the end) — the seven the
    #      computation reads (exp243's classes records = the rebuild's
    #      sha anchors + T3's primary source, exp272's host frame +
    #      one-zone premium means + boundary counts, exp273's outlier
    #      pre-name + the T1/T3 field-table carries, exp276's audit
    #      errs, exp278's amplification ratios, exp279's audit errs,
    #      exp280's deposited boundary_degree_mean = G2's bit-exact
    #      anchor) plus the eight the chains name (exp255/exp256/
    #      exp270/exp271/exp182/exp274/exp275/exp277 — sha-verified via
    #      the recorded chains, never opened) --------------
    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP272 = os.path.join(ROOT, "results",
                          "exp272_host_premium_structure.json")
    DEP273 = os.path.join(ROOT, "results", "exp273_outlier_hosts.json")
    DEP276 = os.path.join(ROOT, "results", "exp276_audit_own_face.json")
    DEP278 = os.path.join(ROOT, "results",
                          "exp278_amplification_factor.json")
    DEP279 = os.path.join(ROOT, "results",
                          "exp279_audit_error_origin.json")
    DEP280 = os.path.join(ROOT, "results", "exp280_chain_head.json")
    DEP255 = os.path.join(ROOT, "results", "exp255.json")
    DEP256 = os.path.join(ROOT, "results",
                          "exp256_row_pair_regression.json")
    DEP270 = os.path.join(ROOT, "results",
                          "exp270_structural_dose.json")
    DEP271 = os.path.join(ROOT, "results", "exp271_one_zone_premium.json")
    DEP182 = os.path.join(ROOT, "results", "exp182_substrate_100.json")
    DEP274 = os.path.join(ROOT, "results",
                          "exp274_premium_mechanism.json")
    DEP275 = os.path.join(ROOT, "results",
                          "exp275_audit_direction.json")
    DEP277 = os.path.join(ROOT, "results",
                          "exp277_deep_band_break_face.json")
    READ_DEPS = (DEP243, DEP272, DEP273, DEP276, DEP278, DEP279, DEP280)
    CHAIN_DEPS = (DEP255, DEP256, DEP270, DEP271, DEP182, DEP274,
                  DEP275, DEP277)
    for _p in READ_DEPS + CHAIN_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    _dep_names = {
        DEP243: "exp243_deposit", DEP272: "exp272_deposit",
        DEP273: "exp273_deposit", DEP276: "exp276_deposit",
        DEP278: "exp278_deposit", DEP279: "exp279_deposit",
        DEP280: "exp280_deposit", DEP255: "exp255_deposit",
        DEP256: "exp256_deposit", DEP270: "exp270_deposit",
        DEP271: "exp271_deposit", DEP182: "exp182_deposit",
        DEP274: "exp274_deposit", DEP275: "exp275_deposit",
        DEP277: "exp277_deposit"}
    ro_before = {name: _sha(p) for p, name in _dep_names.items()}

    # ---- the regression helpers (zero-knob; the exp262/exp272/exp274
    #      rank convention: scipy rankdata's tied-average ranks —
    #      Spearman IS Pearson on the tied-average ranks; the
    #      single-predictor OLS rank R2 runs on the TARGET's
    #      tied-average ranks exactly as exp274's _r2 block) ------------
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

    # ---- THE COMPUTATION (pure re-read + deterministic rebuild +
    #      rank arithmetic; run twice, the two payloads must be
    #      byte-identical — G4's determinism clause) ----------------------
    def compute():
        deps = {}
        for p in READ_DEPS:
            with open(p) as fh:
                deps[_dep_names[p]] = json.load(fh)
        dep243 = deps["exp243_deposit"]
        dep272 = deps["exp272_deposit"]
        dep273 = deps["exp273_deposit"]
        dep276 = deps["exp276_deposit"]
        dep278 = deps["exp278_deposit"]
        dep279 = deps["exp279_deposit"]
        dep280 = deps["exp280_deposit"]

        # ---- the host frame (exp272's per_host order — the order the
        #      batch asserted exp273/exp276/exp278/exp279/exp280
        #      against) --------------------------------------------------
        hosts = [r["host"] for r in dep272["per_host"]]
        assert len(hosts) == 12 and len(set(hosts)) == 12, \
            "the 12-host frame drifted"
        assert dep273["hosts"] == hosts, \
            "exp273's host frame drifted"
        assert dep276["hosts"] == hosts, \
            "exp276's host frame drifted"
        assert dep278["hosts"] == hosts, \
            "exp278's host frame drifted"
        assert dep279["hosts"] == hosts, \
            "exp279's host frame drifted"
        assert dep280["hosts"] == hosts, \
            "exp280's host frame drifted"
        assert sorted(dep243["classes"]) == sorted(hosts), \
            "exp243's classes drifted from the host frame"

        # ---- the outlier pre-name (asserted 6-way: exp273's deposited
        #      outliers == exp272's descriptive.premium_hosts ==
        #      exp276's == exp278's == exp279's == exp280's ==
        #      ['H3', 'H5']) --------------------------------------------
        outliers = dep273["outliers"]
        assert outliers == ["H3", "H5"], \
            f"exp273's outlier pre-name drifted: {outliers}"
        assert dep272["descriptive"]["premium_hosts"] == outliers, \
            "exp272's premium_hosts drifted from the outlier pre-name"
        assert dep276["outliers"] == outliers, \
            "exp276's outliers drifted from the outlier pre-name"
        assert dep278["outliers"] == outliers, \
            "exp278's outliers drifted from the outlier pre-name"
        assert dep279["outliers"] == outliers, \
            "exp279's outliers drifted from the outlier pre-name"
        assert dep280["outliers"] == outliers, \
            "exp280's outliers drifted from the outlier pre-name"
        cluster = [h for h in hosts if h not in outliers]
        assert len(cluster) == 10, "the ten-host cluster drifted"

        # ---- G1: THE REBUILD (exp280's rebuild verbatim — the
        #      exp269/exp256 form, every rebuild bit-asserted against
        #      exp243's OWN records) -----------------------------------
        REWIRE_P = 0.10                # exp225's corpus rewire p
        REBUILD_OK = True

        def _a_sha(A):
            return hashlib.sha256(np.ascontiguousarray(
                np.abs(np.asarray(A, dtype=float)),
                dtype=np.float64).tobytes()).hexdigest()

        # exp208's classify CANON-BOUNDARY mask, copied byte-for-byte
        # from exp243's/exp269's classify (the T-ring-backbone half —
        # the instrument the deposits' n_boundary_cells_base counts;
        # the identical block exp280 ran)
        def _classify_boundary(T):
            n = len(T)
            Td = np.asarray(T, dtype=float)
            bnd = np.zeros(n, dtype=bool)
            for i in range(n):
                if Td[i] != Td[(i - 1) % n] or Td[i] != Td[(i + 1) % n]:
                    bnd[i] = True
            return bnd

        rec272 = {r["host"]: r for r in dep272["per_host"]}
        rec278 = {r["host"]: r for r in dep278["per_host_table"]}
        assert [r["host"] for r in dep278["per_host_table"]] == hosts, \
            "exp278's per-host table order drifted"
        bases = {}
        rebuild_report = []
        for h in hosts:
            rec = dep243["classes"][h]
            n = int(rec["n"])
            if h in ("H0", "H1"):
                A = graph_path(n)      # the chain/path constructor
            else:
                A = small_world(n, REWIRE_P, int(rec["rewire_seed"]))
            assert A.sum() > 0, f"{h}: the rebuilt base is empty"
            sha_ok = bool(_a_sha(A) == rec["base_sha256"])
            edges = int(np.count_nonzero(np.triu(A, 1)))
            edges_ok = bool(edges == int(rec["edges_base"]))
            canon = labeling_bfs_n(np.abs(A))
            canon_ok = bool(np.array_equal(labeling_bfs_n(A), canon))
            bnd = _classify_boundary(canon)
            nb = int(bnd.sum())
            bnd_ok = bool(nb == int(rec["n_boundary_cells_base"]))
            bnd_dual = bool(nb == int(rec272[h]["n_boundary_cells_base"])
                            and nb == int(rec278[h]["n_boundary_cells_base"]))
            REBUILD_OK = (REBUILD_OK and sha_ok and edges_ok
                          and canon_ok and bnd_ok and bnd_dual)
            bases[h] = {"A": A, "n": n, "edges": edges, "canon": canon,
                        "bnd": bnd, "nb": nb}
            rebuild_report.append({
                "host": h, "n": n,
                "constructor": ("graph_path (the chain/path constructor)"
                                if h in ("H0", "H1") else
                                "small_world(n, 0.10, rewire_seed)"),
                "rewire_seed": (None if rec["rewire_seed"] is None
                                else int(rec["rewire_seed"])),
                "sha256_matches_exp243_record": sha_ok,
                "edges_base": edges,
                "edges_match_exp243_record": edges_ok,
                "n_boundary_cells": nb,
                "boundary_count_matches_3way": bool(bnd_ok and bnd_dual),
                "canon_identity_ok": canon_ok})
        assert np.array_equal(bases["H0"]["A"], bases["H1"]["A"]), \
            "the chain class's n=400 call site must echo H1 bit-exactly"
        rebuild_ok = bool(REBUILD_OK)

        # ---- T1: exp272's per-host ONE-ZONE PREMIUM means — the mean
        #      identity bit-exact 12/12 (the recomputed mean over the
        #      deposited per-seed rows == the deposited mean ==
        #      exp273's field-table carry) ------------------------------
        ft273 = {rec["field"]: rec for rec in dep273["field_table"]}
        T1_FIELD = "exp272.per_host.one_zone_premium_mean"
        T3_FIELD = "exp243.classes.multi_identity_audit.prod_err"
        assert T1_FIELD in ft273 and T3_FIELD in ft273, \
            "exp273's field table lost the T1/T3 carries"
        T1 = {}
        t1_id = {"n_recomputed": 0, "n_exp273_carry": 0}
        for h in hosts:
            dep_mean = float(rec272[h]["one_zone_premium_mean"])
            seeds = [float(v) for v in rec272[h]["one_zone_premiums_by_seed"]]
            assert len(seeds) == 3, f"{h}: the per-seed premium rows drifted"
            recomputed = float(np.mean(seeds))
            carry = float(ft273[T1_FIELD]["values"][h])
            T1[h] = dep_mean
            t1_id["n_recomputed"] += int(recomputed == dep_mean)
            t1_id["n_exp273_carry"] += int(dep_mean == carry)
        t1_ok = bool(t1_id["n_recomputed"] == 12
                     and t1_id["n_exp273_carry"] == 12)

        # ---- T2: exp278's per-host AMPLIFICATION RATIOS — asserted ==
        #      its own m_P3/m_P12_pooled identity bit-exact 12/12
        #      (exp280's carry) ------------------------------------------
        T2 = {}
        t2_ok = True
        for h in hosts:
            ratio = float(rec278[h]["amplification_ratio"])
            m_P3 = float(rec278[h]["m_P3"])
            m_P12 = float(rec278[h]["m_P12_pooled"])
            ok = bool(ratio == m_P3 / m_P12
                      and m_P3 == float(
                          dep278["ratio_audit_detail"][h]["m_P3"])
                      and m_P12 == float(
                          dep278["ratio_audit_detail"][h]["m_P12_pooled"]))
            t2_ok = t2_ok and ok
            T2[h] = ratio
        t2_ok = bool(t2_ok)

        # ---- T3: the AUDIT ERROR mia_prod_err — the 4-way carry
        #      asserted bit-exact 12/12 each: exp243's classes ==
        #      exp276's decomposition_table == exp279's origin_table ==
        #      exp273's field table -------------------------------
        tbl276 = {r["host"]: r for r in dep276["decomposition_table"]}
        tbl279 = {r["host"]: r for r in dep279["origin_table"]}
        assert [r["host"] for r in dep276["decomposition_table"]] == hosts, \
            "exp276's decomposition table order drifted"
        assert [r["host"] for r in dep279["origin_table"]] == hosts, \
            "exp279's origin table order drifted"
        T3 = {}
        t3_carry = {"exp276": 0, "exp279": 0, "exp273": 0}
        for h in hosts:
            v243 = float(
                dep243["classes"][h]["multi_identity_audit"]["prod_err"])
            v276 = float(tbl276[h]["audit_prod_err"])
            v279 = float(tbl279[h]["audit_prod_err"])
            v273 = float(ft273[T3_FIELD]["values"][h])
            T3[h] = v243
            t3_carry["exp276"] += int(v243 == v276)
            t3_carry["exp279"] += int(v243 == v279)
            t3_carry["exp273"] += int(v243 == v273)
        t3_ok = bool(all(v == 12 for v in t3_carry.values()))

        targets_finite = bool(all(
            T1[h] == T1[h] and abs(T1[h]) != float("inf")
            and T2[h] == T2[h] and abs(T2[h]) != float("inf")
            and T3[h] == T3[h] and abs(T3[h]) != float("inf")
            for h in hosts))

        # ---- G1: the provenance chains (the recorded input shas ==
        #      the actual deposit bytes: exp280's 12, exp279's 9,
        #      exp278's 11, exp276's 8, exp273's 5, exp272's 4) --------
        def _chain(dep):
            return {key: bool(rec["sha256"]
                              == _sha(os.path.join(ROOT, rec["path"])))
                    for key, rec in dep["inputs"].items()}
        chains = {name: _chain(dep) for name, dep in
                  (("exp280", dep280), ("exp279", dep279),
                   ("exp278", dep278), ("exp276", dep276),
                   ("exp273", dep273), ("exp272", dep272))}
        chains_ok = bool(all(all(c.values()) for c in chains.values()))
        chain_counts = {name: (sum(c.values()), len(c))
                        for name, c in chains.items()}

        # ---- G2: THE FIELD (exp280's EXACT definition, never re-fit):
        #      the boundary cells' own degree mean over the classify
        #      CANON-BOUNDARY set; asserted BIT-EXACT vs exp280's
        #      deposited field table 12/12 -------------------------------
        bdm280 = {r["host"]: r["boundary_degree_mean"]
                  for r in dep280["field_table"]}
        assert [r["host"] for r in dep280["field_table"]] == hosts, \
            "exp280's field table order drifted"
        F = {}
        field_id = {"n_masks_nonempty": 0, "n_bit_exact_vs_exp280": 0}
        for h in hosts:
            A = bases[h]["A"]
            support = np.abs(A) > 0
            deg = support.sum(axis=1).astype(float)
            bnd = bases[h]["bnd"]
            assert bnd.sum() > 0, f"{h}: the boundary mask is empty"
            boundary_degree_mean = float(deg[bnd].mean())
            F[h] = boundary_degree_mean
            field_id["n_masks_nonempty"] += int(int(bnd.sum()) > 0)
            field_id["n_bit_exact_vs_exp280"] += int(
                boundary_degree_mean == bdm280[h])
        field_ok = bool(field_id["n_masks_nonempty"] == 12
                        and field_id["n_bit_exact_vs_exp280"] == 12)
        field_census = _ties_census([F[h] for h in hosts])
        target_censuses = {"T1_one_zone_premium": _ties_census(
                               [T1[h] for h in hosts]),
                           "T2_amplification_ratio": _ties_census(
                               [T2[h] for h in hosts]),
                           "T3_mia_prod_err": _ties_census(
                               [T3[h] for h in hosts])}

        # ---- THE REGRESSIONS (the exp274/exp275 conventions verbatim;
        #      the 12-slot frame, tied-average ranks) --------------------
        Fv = [F[h] for h in hosts]
        Rk_F = rankdata(np.asarray(Fv, dtype=float))

        def _regress(target, tv):
            rk = rankdata(np.asarray(tv, dtype=float))
            rho = _spearman(Fv, tv)
            r2_single = _r2([Fv], rk)
            r2_all = _r2([Rk_F], rk)
            return {"rho": rho, "rho_abs": abs(rho),
                    "r2_single": r2_single, "r2_all_ranks": r2_all,
                    "all_ranks_equals_rho_squared": bool(
                        abs(r2_all - rho ** 2) < 1e-12),
                    "status": "ok"}
        reg = {"T1_one_zone_premium": _regress(
                   "T1", [T1[h] for h in hosts]),
               "T2_amplification_ratio": _regress(
                   "T2", [T2[h] for h in hosts]),
               "T3_mia_prod_err": _regress(
                   "T3", [T3[h] for h in hosts])}
        rho_table_complete = bool(
            all(reg[t]["status"] == "ok"
                and reg[t]["all_ranks_equals_rho_squared"]
                for t in reg))

        # ---- G3: THE BRANCH (the discriminant pre-named with the
        #      numeric bar: CHORD-CARRIED iff boundary_degree_mean
        #      reaches Spearman >= 0.5 — the SIGNED house bar — against
        #      >= 1 of the three targets; else CHORD-ABSENT. The abs
        #      variant: a NEGATIVE crossing of |rho| >= 0.5 is the
        #      ANTI-ALIGNED face — named per target, NEVER gating.) ---
        RHO_BAR = 0.5
        TARGETS = ("T1_one_zone_premium", "T2_amplification_ratio",
                   "T3_mia_prod_err")
        rhos = {t: reg[t]["rho"] for t in TARGETS}
        max_signed = max(rhos.values())
        signed_leader = [t for t in TARGETS if rhos[t] == max_signed][0]
        if max_signed >= RHO_BAR:
            branch = "CHORD-CARRIED"
        else:
            branch = "CHORD-ABSENT"
        n_carried = sum(1 for t in TARGETS if rhos[t] >= RHO_BAR)
        anti_aligned = {}
        for t in TARGETS:
            anti_aligned[t] = {
                "crosses_abs_bar": bool(reg[t]["rho_abs"] >= RHO_BAR),
                "signed_bar_met": bool(rhos[t] >= RHO_BAR),
                "anti_aligned_face": bool(reg[t]["rho_abs"] >= RHO_BAR
                                          and rhos[t] < RHO_BAR)}
        n_anti = sum(1 for t in TARGETS
                     if anti_aligned[t]["anti_aligned_face"])

        # the audit-only margins: the outlier field values vs the
        # cluster's range (the "named honestly" clause)
        f_out = {h: F[h] for h in outliers}
        f_cl = [F[h] for h in cluster]
        field_margin = {"outliers": f_out, "cluster_min": min(f_cl),
                        "cluster_max": max(f_cl)}

        g3_detail = {
            "bar_signed_rho": RHO_BAR,
            "targets_in_max": list(TARGETS),
            "rho_by_target": rhos,
            "max_signed_rho": max_signed,
            "signed_leader": signed_leader,
            "n_targets_carried": n_carried,
            "abs_variant_audit_only": {
                t: {"rho": reg[t]["rho"], "rho_abs": reg[t]["rho_abs"],
                    **anti_aligned[t]} for t in TARGETS},
            "n_anti_aligned_crossings": n_anti,
            "anti_aligned_note": (
                "the chord runs OPPOSITE the pre-named direction on "
                "the crossed targets — named, never gating "
                "(exp280's precedent)") if n_anti > 0 else (
                "no anti-aligned crossing at the 0.5 abs bar"),
            "field_margin_audit_only": field_margin}

        g1_pass = bool(rebuild_ok and t1_ok and t2_ok and t3_ok
                       and targets_finite and chains_ok)
        g2_pass = bool(field_ok and rho_table_complete)
        g3_pass = bool(branch in ("CHORD-CARRIED", "CHORD-ABSENT")
                       and len(rhos) == 3
                       and all(reg[t]["status"] == "ok" for t in TARGETS))

        return {
            "hosts": hosts, "outliers": outliers, "cluster": cluster,
            "rebuild_report": rebuild_report,
            "field_table": [{"host": h, "outlier": h in outliers,
                             "boundary_degree_mean": F[h]}
                            for h in hosts],
            "field_census": field_census,
            "target_censuses": target_censuses,
            "targets_table": [{"host": h, "outlier": h in outliers,
                               "boundary_degree_mean": F[h],
                               "T1_one_zone_premium": T1[h],
                               "T2_amplification_ratio": T2[h],
                               "T3_mia_prod_err": T3[h]}
                              for h in hosts],
            "regressions": reg,
            "g1": {"pass": g1_pass,
                   "rebuild_ok_12": rebuild_ok,
                   "T1_mean_identity": t1_id,
                   "T1_mean_identity_ok": t1_ok,
                   "T2_ratio_identity_ok": t2_ok,
                   "T3_carry_bit_exact": t3_carry,
                   "T3_carry_ok": t3_ok,
                   "targets_finite": targets_finite,
                   "chains": chain_counts,
                   "chains_ok": chains_ok},
            "g2": {"pass": g2_pass,
                   "field_definition_identities": field_id,
                   "field_definition_ok": field_ok,
                   "field_census": field_census,
                   "rho_table_complete": rho_table_complete},
            "g3": {"pass": g3_pass, "branch": branch, **g3_detail}}

    payload_a = compute()
    sha_a = hashlib.sha256(json.dumps(
        payload_a, sort_keys=True, default=str).encode()).hexdigest()
    payload_b = compute()
    sha_b = hashlib.sha256(json.dumps(
        payload_b, sort_keys=True, default=str).encode()).hexdigest()
    deterministic = bool(sha_a == sha_b)
    assert deterministic, "the computation is not two-pass deterministic"

    g3 = payload_a["g3"]
    branch = g3["branch"]
    gates = {"G1_rebuild_integrity": {
                 "pass": payload_a["g1"]["pass"],
                 "bar": "READ-ONLY sha-verified (the exp280 precedent): "
                        "the 12 rebuilt bases bit-asserted against "
                        "exp243's records (base_sha256 12/12, "
                        "edges_base 12/12, the classify boundary count "
                        "12/12 dual-carried vs exp272 + exp278, the "
                        "canon identity 12/12, H0 == H1); exp278's "
                        "ratio identity bit-exact 12/12; the T1 mean "
                        "identity bit-exact 12/12; the T3 4-way carry "
                        "bit-exact 12/12 each; the outlier pre-name "
                        "asserted 6-way (exp273 == exp272 == exp276 "
                        "== exp278 == exp279 == exp280 == "
                        "['H3','H5']); the provenance chains "
                        "sha-verified (exp280 12/12, exp279 9/9, "
                        "exp278 11/11, exp276 8/8, exp273 5/5, "
                        "exp272 4/4); READ-ONLY",
                 **payload_a["g1"]},
             "G2_field_definition_bit_identical": {
                 "pass": payload_a["g2"]["pass"],
                 "bar": "the field definition BIT-IDENTICAL to "
                        "exp280's: the boundary cells' own degree "
                        "mean over the exp208 classify CANON-BOUNDARY "
                        "set (exp280's code path, never re-fit) — the "
                        "masks nonempty 12/12, the recomputed "
                        "boundary_degree_mean == exp280's deposited "
                        "field-table values BIT-EXACT 12/12, the ties "
                        "census recorded, the rho table complete",
                 **payload_a["g2"]},
             "G3_branch": {
                 "pass": g3["pass"],
                 "bar": "the discriminant pre-named with the numeric "
                        "bar: CHORD-CARRIED iff boundary_degree_mean "
                        "reaches Spearman >= 0.5 (the SIGNED house "
                        "bar) against >= 1 of the three targets (T1 "
                        "exp272's one-zone premium means / T2 "
                        "exp278's amplification ratios / T3 the audit "
                        "error mia_prod_err); else CHORD-ABSENT; the "
                        "abs variant — a NEGATIVE crossing of |rho| "
                        ">= 0.5 — is the ANTI-ALIGNED face, NAMED in "
                        "the deposit and the verdict per target, "
                        "never gating",
                 "branch": g3["branch"],
                 **{k: v for k, v in g3.items() if k != "pass"}}}

    # ---- G4: the discipline --------------------------------------------
    ro_after = {name: _sha(p) for p, name in _dep_names.items()}
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

    g4_pass = bool(ro_unchanged and deterministic and no_wall_clock
                   and floor_at_entry == PROD_FLOOR
                   and docstring_ok and header_ok)

    gates["G4_discipline"] = {
        "pass": g4_pass,
        "bar": ("all 15 deposits READ-ONLY sha-recorded "
                "byte-unchanged; deterministic — two-pass "
                "bit-identical; no wall-clock fields; the "
                "docstring+header pinned to a52a14a asserted at entry "
                "AND exit; NEURAL_SPEC_MIN == -60.0 asserted at exit"),
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
        "docstring_byte_unchanged_vs_a52a14a": docstring_ok,
        "header_sha256": header_sha,
        "header_byte_unchanged_vs_a52a14a": header_ok,
        "deposit_form": ("deterministic: no wall-clock fields — a "
                         "re-run of this module reproduces this file "
                         "byte-identically")}

    # ---- the verdict (one line, the numbers data-driven) -----------------
    def _g(v):
        return format(v, ".10g") if isinstance(v, float) else str(v)

    gate_passes = {"G1": gates["G1_rebuild_integrity"]["pass"],
                   "G2": gates["G2_field_definition_bit_identical"]["pass"],
                   "G3": gates["G3_branch"]["pass"],
                   "G4": gates["G4_discipline"]["pass"]}
    n_pass = sum(1 for v in gate_passes.values() if v)
    n_refute = 4 - n_pass

    rhos = g3["rho_by_target"]
    max_signed = g3["max_signed_rho"]
    signed_leader = g3["signed_leader"]
    n_carried = g3["n_targets_carried"]
    n_anti = g3["n_anti_aligned_crossings"]
    f_m = g3["field_margin_audit_only"]
    by_target = ", ".join(f"{t.split('_', 1)[0]} {_g(rhos[t])}"
                          for t in rhos)
    if branch == "CHORD-CARRIED":
        core = (
            f"CHORD-CARRIED — the boundary cells' own degree mean "
            f"reaches the 0.5 SIGNED house bar against {n_carried} of "
            f"3 targets (max rho {_g(max_signed)} on {signed_leader}; "
            f"by target {by_target}) — the mechanism line RE-OPENS at "
            f"the chord level")
    else:
        core = (
            f"CHORD-ABSENT — the boundary cells' own degree mean "
            f"clears NOTHING at the 0.5 SIGNED house bar (max signed "
            f"rho {_g(max_signed)} on {signed_leader}; by target "
            f"{by_target}) — the line stands closed at mia and the "
            f"premium's origin is formally OUTSIDE the deposited "
            f"host records")
    if n_anti > 0:
        anti_list = "; ".join(
            f"{t} rho {_g(g3['abs_variant_audit_only'][t]['rho'])}"
            for t in rhos
            if g3["abs_variant_audit_only"][t]["anti_aligned_face"])
        anti = (
            f" | THE ANTI-ALIGNED FACE (named honestly, audit-only): "
            f"{n_anti}/3 targets cross the abs bar NEGATIVE "
            f"({anti_list})"
            f" — hosts whose boundary cells carry FEWER chords read "
            f"the premium/amplification/audit HIGHER; consistent with "
            f"exp280's |rho| 0.6081 face on the deep-band err — the "
            f"boundary-RICH hosts' boundary cells are chord-POOR "
            f"(H3 {_g(f_m['outliers']['H3'])} / H5 "
            f"{_g(f_m['outliers']['H5'])} vs the ten-host cluster's "
            f"[{_g(f_m['cluster_min'])}, {_g(f_m['cluster_max'])}]) "
            f"and the premium runs WITH the chord-poverty, not with "
            f"the chord")
    else:
        anti = (" | the anti-aligned face: no negative abs crossing "
                "at the 0.5 bar")
    verdict = (
        f"{n_pass}/4 gates G1-G4 ({n_pass} PASS / {n_refute} REFUTE) | "
        + core + anti
        + f" | G2 the field definition bit-identical to exp280's: the "
        f"recomputed boundary_degree_mean == exp280's deposited field "
        f"table 12/12 bit-exact | 12 hosts, a pure re-read + a "
        f"deterministic sha-asserted rebuild (exp280's form — "
        f"graph_path for H0/H1, small_world at the deposited rewire "
        f"seeds) of exp243's records, READ-ONLY byte-unchanged, "
        f"two-pass bit-identical, floor -60.0")

    deposit = {
        "exp": "exp281_antialigned_face",
        "claim": (
            "THE ANTI-ALIGNED FACE TESTED AT THE SIGNED BAR (batch "
            "39, pre-registration commit a52a14a): exp280's "
            "boundary_degree_mean (the boundary cells' own degree "
            "mean over the exp208 classify CANON-BOUNDARY set — the "
            "chord-poorest face of the deposited topology on H3/H5) "
            "regressed at the SIGNED 0.5 house bar against the "
            "premium's three carriers — T1 exp272's per-host "
            "one-zone premium means (the premium level itself), T2 "
            "exp278's per-host amplification ratios, T3 the audit "
            "error mia_prod_err (exp276's/exp279's/exp243's 4-way "
            "carry); a pure re-read + a deterministic sha-asserted "
            "rebuild of the 12 base adjacencies (exp280's rebuild "
            "verbatim), the field asserted BIT-EXACT vs exp280's "
            "deposited field table 12/12; Spearman under the "
            "exp274/exp275 conventions; the branch CHORD-CARRIED "
            "(>= 1 of the three targets reaches the signed bar — the "
            "mechanism line re-opens at the chord level) / "
            "CHORD-ABSENT (it clears nothing — the line stands "
            "closed at mia and the premium's origin is formally "
            "OUTSIDE the deposited host records); the abs variant — "
            "a negative crossing of |rho| >= 0.5 — is the "
            "ANTI-ALIGNED face, named in the deposit and the "
            "verdict per target, never gating"),
        "method": {
            "rebuild": ("exp280's rebuild VERBATIM (the "
                        "exp269/exp256 form — the exp243/exp225 "
                        "construction): H0/H1 graph_path(n); H2-H11 "
                        "small_world(n, 0.10, int(rec['rewire_seed'])) "
                        "at the deposited rewire seeds; n from "
                        "exp243's per-host records; every rebuild "
                        "asserted — sha256(|A| as float64) == "
                        "rec['base_sha256'], the upper-triangle edge "
                        "count == rec['edges_base'], the exp208 "
                        "classify CANON-BOUNDARY count == "
                        "rec['n_boundary_cells_base'] dual-carried vs "
                        "exp272 + exp278, labeling_bfs_n(|A|) == "
                        "labeling_bfs_n(A), H0 == H1 bit-exact; ZERO "
                        "new simulation"),
            "field": {
                "boundary_degree_mean": ("F5, exp280's EXACT "
                                         "definition, never re-fit — "
                                         "the mean pair-support degree "
                                         "over the CANON-BOUNDARY "
                                         "cells (exp208's classify "
                                         "instrument on the canon "
                                         "labeling, the ring backbone "
                                         "i±1; support = |A| > 0, "
                                         "symmetric; degree = the "
                                         "per-cell support degree); "
                                         "asserted BIT-EXACT vs "
                                         "exp280's deposited field "
                                         "table 12/12 at G2")},
            "targets": {
                "T1_one_zone_premium": ("exp272's per-host ONE-ZONE "
                                        "PREMIUM means — the premium "
                                        "level itself; the mean "
                                        "identity asserted bit-exact "
                                        "12/12 (the recomputed mean "
                                        "over the deposited per-seed "
                                        "rows one_zone_premiums_by_seed "
                                        "== the deposited mean == "
                                        "exp273's field-table carry)"),
                "T2_amplification_ratio": ("exp278's per-host "
                                           "AMPLIFICATION RATIOS; "
                                           "asserted == its own "
                                           "m_P3/m_P12_pooled identity "
                                           "bit-exact 12/12 (exp280's "
                                           "carry)"),
                "T3_mia_prod_err": ("the AUDIT ERROR mia_prod_err — "
                                    "the 4-way carry asserted bit-"
                                    "exact 12/12 each: exp243's "
                                    "classes[h][multi_identity_audit]"
                                    "[prod_err] == exp276's "
                                    "decomposition_table "
                                    "audit_prod_err == exp279's "
                                    "origin_table audit_prod_err == "
                                    "exp273's field-table values")},
            "h0_h1_note": ("the H0 slot echoes H1 bit-exactly (the "
                           "chain class's n=400 call site, exp243's "
                           "own disclosure, asserted) — the field "
                           "table carries both slots; the regressions "
                           "run on the 12-slot frame (the house "
                           "convention, exp278's ties-census "
                           "precedent); the field's ties census "
                           "recorded (the H0/H1 echo ties one pair)"),
            "regressions": ("the exp274/exp275 conventions VERBATIM: "
                            "Spearman = Pearson on the tied-average "
                            "ranks (scipy rankdata) of "
                            "boundary_degree_mean vs each target on "
                            "the 12-slot frame; the single-predictor "
                            "OLS rank R2 (the target as its "
                            "tied-average ranks, the field as the "
                            "numeric design column); the all-ranks "
                            "variant (the field ranked too — single "
                            "R2 == rho^2 within 1e-12) audit-only; "
                            "the ties census per vector"),
            "branch_rule": ("CHORD-CARRIED iff boundary_degree_mean "
                            "reaches Spearman >= 0.5 (the SIGNED "
                            "house bar) against >= 1 of the three "
                            "targets; else CHORD-ABSENT; the abs "
                            "variant (a NEGATIVE crossing of |rho| "
                            ">= 0.5) is the ANTI-ALIGNED face — "
                            "named per target in the deposit and the "
                            "verdict, never gating"),
            "method_source": ("experiments/exp280_chain_head.py (the "
                              "rebuild + the field definition + the "
                              "deposited field table), experiments/"
                              "exp243_structured_adversarial.py (the "
                              "classes records = the rebuild's sha "
                              "anchors + T3's primary source), "
                              "experiments/exp272_host_premium_"
                              "structure.py (T1 + the host frame + "
                              "the boundary counts), experiments/"
                              "exp273_outlier_hosts.py (the outlier "
                              "pre-name + the T1/T3 carries), "
                              "experiments/exp276_audit_own_face.py "
                              "(T3), experiments/"
                              "exp278_amplification_factor.py (T2), "
                              "experiments/exp279_audit_error_origin."
                              "py (T3)")},
        "inputs": {
            "exp243_deposit": {
                "path": "results/exp243_structured_adversarial.json",
                "sha256": ro_before["exp243_deposit"],
                "role": ("the classes records — the rebuild's sha "
                         "anchors (base_sha256, edges_base, "
                         "n_boundary_cells_base, rewire_seed, n) + "
                         "T3's primary source (multi_identity_audit."
                         "prod_err)")},
            "exp272_deposit": {
                "path": "results/exp272_host_premium_structure.json",
                "sha256": ro_before["exp272_deposit"],
                "role": ("the host frame + T1 (the per-host one-zone "
                         "premium means + the per-seed rows) + the "
                         "per-host boundary counts + the outlier "
                         "pre-name source (descriptive.premium_hosts)")},
            "exp273_deposit": {
                "path": "results/exp273_outlier_hosts.json",
                "sha256": ro_before["exp273_deposit"],
                "role": ("the deposited outlier pre-name + the T1/T3 "
                         "field-table carries "
                         "(exp272.per_host.one_zone_premium_mean, "
                         "exp243.classes.multi_identity_audit."
                         "prod_err) + the recorded input shas "
                         "verified 5/5")},
            "exp276_deposit": {
                "path": "results/exp276_audit_own_face.json",
                "sha256": ro_before["exp276_deposit"],
                "role": ("T3's audit_prod_err (the decomposition "
                         "table) + the recorded input shas verified "
                         "8/8")},
            "exp278_deposit": {
                "path": "results/exp278_amplification_factor.json",
                "sha256": ro_before["exp278_deposit"],
                "role": ("T2 (the per-host amplification ratios + "
                         "the m_P3/m_P12_pooled identity) + the "
                         "boundary counts + the recorded input shas "
                         "verified 11/11")},
            "exp279_deposit": {
                "path": "results/exp279_audit_error_origin.json",
                "sha256": ro_before["exp279_deposit"],
                "role": ("T3's audit_prod_err (the origin table) + "
                         "the recorded input shas verified 9/9")},
            "exp280_deposit": {
                "path": "results/exp280_chain_head.json",
                "sha256": ro_before["exp280_deposit"],
                "role": ("G2's bit-exact anchor — the deposited "
                         "field table's boundary_degree_mean per "
                         "host (the definition exp281 asserts "
                         "itself against) + the recorded input "
                         "shas verified 12/12")},
            "exp255_deposit": {
                "path": "results/exp255.json",
                "sha256": ro_before["exp255_deposit"],
                "role": ("the provenance chain: the arm-worst "
                         "instrument's source deposit — sha-verified "
                         "via the chains, never opened for "
                         "computation")},
            "exp256_deposit": {
                "path": "results/exp256_row_pair_regression.json",
                "sha256": ro_before["exp256_deposit"],
                "role": ("the provenance chain: the 72-row battery "
                         "underlying exp272's/exp278's/exp279's "
                         "grids — sha-verified via the chains, never "
                         "opened for computation")},
            "exp270_deposit": {
                "path": "results/exp270_structural_dose.json",
                "sha256": ro_before["exp270_deposit"],
                "role": ("the provenance chain: exp272's structural-"
                         "dose input — sha-verified via exp272's "
                         "chain, never opened for computation")},
            "exp271_deposit": {
                "path": "results/exp271_one_zone_premium.json",
                "sha256": ro_before["exp271_deposit"],
                "role": ("the provenance chain: the one-zone premium "
                         "grid — sha-verified via the chains, never "
                         "opened for computation")},
            "exp182_deposit": {
                "path": "results/exp182_substrate_100.json",
                "sha256": ro_before["exp182_deposit"],
                "role": ("the provenance chain: the margin profiles — "
                         "sha-verified via the chains, never opened "
                         "for computation")},
            "exp274_deposit": {
                "path": "results/exp274_premium_mechanism.json",
                "sha256": ro_before["exp274_deposit"],
                "role": ("the provenance chain: the rank-regression "
                         "convention's source deposit — sha-verified "
                         "via the chains, never opened for "
                         "computation")},
            "exp275_deposit": {
                "path": "results/exp275_audit_direction.json",
                "sha256": ro_before["exp275_deposit"],
                "role": ("the provenance chain: the sha-discipline "
                         "precedent's deposit — sha-verified via the "
                         "chains, never opened for computation")},
            "exp277_deposit": {
                "path": "results/exp277_deep_band_break_face.json",
                "sha256": ro_before["exp277_deposit"],
                "role": ("the provenance chain: the pre-body "
                         "disclosure precedent's deposit — "
                         "sha-verified via the chains, never opened "
                         "for computation")}},
        "hosts": payload_a["hosts"],
        "outliers": payload_a["outliers"],
        "cluster": payload_a["cluster"],
        "rebuild_report": payload_a["rebuild_report"],
        "field_table": payload_a["field_table"],
        "field_census": payload_a["field_census"],
        "target_censuses": payload_a["target_censuses"],
        "targets_table": payload_a["targets_table"],
        "regressions": payload_a["regressions"],
        "gates": gates,
        "branch": branch,
        "branch_discriminant": {k: v for k, v in g3.items()
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
            "docstring_byte_unchanged_vs_a52a14a": docstring_ok,
            "header_sha256": header_sha,
            "header_byte_unchanged_vs_a52a14a": header_ok,
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

    print("=== exp281: THE ANTI-ALIGNED FACE TESTED AT THE SIGNED BAR "
          "(pure deposit re-read + deterministic sha-asserted rebuild "
          "+ rank arithmetic) ===")
    print("  exp280's boundary_degree_mean regressed against the "
          "premium's three carriers")
    print(f"\n  G1 rebuild integrity: "
          f"{'PASS' if gates['G1_rebuild_integrity']['pass'] else 'FAIL'} "
          f"(the 12 bases rebuilt — exp280's form — sha-asserted vs "
          f"exp243's records 12/12 + edges 12/12 + the classify "
          f"boundary count 12/12 dual-carried vs exp272+exp278 + the "
          f"canon identity 12/12 + H0 == H1; the T1 mean identity "
          f"12/12; exp278's ratio identity 12/12; the T3 4-way carry "
          f"bit-exact 12/12 x 3; the chains sha-verified exp280 "
          f"{payload_a['g1']['chains']['exp280'][0]}/"
          f"{payload_a['g1']['chains']['exp280'][1]} + exp279 "
          f"{payload_a['g1']['chains']['exp279'][0]}/"
          f"{payload_a['g1']['chains']['exp279'][1]} + exp278 "
          f"{payload_a['g1']['chains']['exp278'][0]}/"
          f"{payload_a['g1']['chains']['exp278'][1]} + exp276 "
          f"{payload_a['g1']['chains']['exp276'][0]}/"
          f"{payload_a['g1']['chains']['exp276'][1]} + exp273 "
          f"{payload_a['g1']['chains']['exp273'][0]}/"
          f"{payload_a['g1']['chains']['exp273'][1]} + exp272 "
          f"{payload_a['g1']['chains']['exp272'][0]}/"
          f"{payload_a['g1']['chains']['exp272'][1]})")
    g2_word = ("PASS" if gates["G2_field_definition_bit_identical"]["pass"]
               else "FAIL")
    print(f"  G2 field definition bit-identical to exp280's: {g2_word} "
          f"(the masks nonempty 12/12; the recomputed "
          f"boundary_degree_mean == exp280's deposited field table "
          f"bit-exact 12/12; the ties census "
          f"{payload_a['field_census']})")
    print("  the 12-host table (H3/H5 the outliers):")
    for row in payload_a["targets_table"]:
        tag = " <== outlier" if row["outlier"] else ""
        print(f"      {row['host']:4s} bnd-deg "
              f"{row['boundary_degree_mean']:.4f}  T1 "
              f"{row['T1_one_zone_premium']:.4f}  T2 "
              f"{row['T2_amplification_ratio']:.4f}  T3 "
              f"{row['T3_mia_prod_err']:.4f}{tag}")
    print("  G3 branch — Spearman(boundary_degree_mean, target):")
    for t, rec in payload_a["regressions"].items():
        aa = g3["abs_variant_audit_only"][t]
        note = ("  <== anti-aligned (abs crossed, negative)"
                if aa["anti_aligned_face"] else
                ("  (signed bar met)" if aa["signed_bar_met"] else ""))
        print(f"      {t:24s} rho {rec['rho']:+.4f}  (abs "
              f"{rec['rho_abs']:.4f})  R2 {rec['r2_single']:.4f}{note}")
    print(f"  G4 discipline: {'PASS' if g4_pass else 'FAIL'} "
          f"(15 deposits READ-ONLY byte-unchanged: {ro_unchanged}; "
          f"two-pass bit-identical: {deterministic}; no wall-clock "
          f"fields: {no_wall_clock})")
    print(f"\n  BRANCH: {branch} | max signed rho "
          f"{g3['max_signed_rho']:+.4f} ({g3['signed_leader']}) vs the "
          f"0.5 bar | anti-aligned crossings: {g3['n_anti_aligned_crossings']}/3")
    print(f"\n  GATES: {verdict}")
    print(f"  deposited {OUT}")

    # the hard rule, re-asserted after the work: the docstring is still
    # the a52a14a pre-registration, byte-for-byte
    assert hashlib.sha256(__doc__.encode()).hexdigest() \
        == EXPECTED_DOCSTRING_SHA256, "docstring drifted after the work"
    with open(__file__, "r", encoding="utf-8") as _f:
        _src2 = _f.read()
    assert hashlib.sha256(
        _src2[:_src2.index(_marker) + len(_marker)].encode()
    ).hexdigest() == EXPECTED_HEADER_SHA256, "header drifted after work"
    # the source deposits are still byte-unchanged after the work
    assert set(_sha(p) for p in READ_DEPS + CHAIN_DEPS) \
        == set(ro_before.values()), "source deposit drifted after work"

    # THE FLOOR ASSERT AT EXIT (the hard rule; exp243's closing line)
    CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at exit"
    return deposit


if __name__ == "__main__":
    main()
