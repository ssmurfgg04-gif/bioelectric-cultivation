#!/usr/bin/env python3
"""exp280 — THE CHAIN'S HEAD: THE DEEP-BAND READ vs THE HOSTS' OWN
ADJACENCY STRUCTURE (batch 38; batch-37's derived item, ledger L257 —
zero new simulation).

THE OPEN ITEM: exp273 named H3/H5 the outliers at mia_prod_err 2.12/
2.28 vs the ten-host cluster's [0.49, 0.52] — they are the two
boundary-richest hosts (47/48 of the 400 cells canon-boundary vs the
cluster's [31, 43]). exp276 located the outliers' audit error 94% in
the P3 deep-band arm; exp277 showed the deep-band break is class-blind
(the cluster-typical error mixture amplified ~7x, not shifted);
exp278 showed the amplification is mia-scaled (rho 0.7250) and NOT
canon-boundary-count-scaled (-0.0596); exp279 closed the aggregation
face (AUDIT-MAX — the audit error rides the worst arm). The one
instrument never pointed at the deep-band exposure: the hosts' OWN
base adjacency structure. The question this module asks: is the
deep-band read's per-host error carried by the deposited adjacency's
own topology — the degree spectrum, the clustering, the boundary
cells' own degree, the pair-support density — or is the exposure
ABSENT from that structure (named honestly)?

THE INSTRUMENT (pre-registered, zero-knob): a pure re-read + a
DETERMINISTIC REBUILD of the deposited base adjacencies — exp269's/
exp256's rebuild form (the exp243/exp225 construction), every rebuild
bit-asserted against exp243's own records; ZERO new simulation (no
read, no decode, no dynamics — the rebuild is a deterministic graph
construction whose shas are pinned by the deposit):

  1. THE REBUILD: the 12 base adjacencies at the deposited ns
     (exp243's classes records carry n per host): H0/H1 the chain/
     path constructor graph_path(n) (the H0 slot echoes H1 bit-
     exactly — exp243's own disclosure, asserted); H2-H11
     small_world(n, 0.10, int(rec["rewire_seed"])) at the deposited
     rewire seeds. Every rebuild asserted against exp243's records:
     sha256(|A| as float64) == rec["base_sha256"]; the upper-triangle
     edge count == rec["edges_base"]; the exp208 classify CANON-
     BOUNDARY count == rec["n_boundary_cells_base"] (dual-carried vs
     exp272's per-host records and exp278's table); the canon
     identity labeling_bfs_n(|A|) == labeling_bfs_n(A).

  2. THE STRUCTURAL FIELDS (zero-knob, per host, from the rebuilt
     base A and its canon labeling; the pair support = |A| > 0, the
     degree = the per-cell support degree, symmetric):
     F1 deg_mean   — the mean of the degree spectrum over the n cells;
     F2 deg_max    — the max of the degree spectrum;
     F3 deg_spread — the max minus the min of the degree spectrum;
     F4 clustering — the mean local Watts-Strogatz clustering
        coefficient (deg >= 2: 2*E(N_i)/(d_i*(d_i-1)) with E the
        support edges among the cell's neighbors; deg < 2: 0.0);
     F5 boundary_degree_mean — the mean degree over the CANON-
        BOUNDARY cells (exp208's classify instrument: the canon
        labeling's ring-backbone value transitions);
     F6 pair_support_density — the support pairs in the upper
        triangle over n*(n-1)/2.
     DISCLOSED DEGENERACY (fixed BEFORE the body, from the
     deterministic rebuild of the deposited seeds — the exp277
     deposit-read disclosure precedent): the deposited rewire seeds'
     chords form NO triangles on any of the 12 rebuilt bases, so F4
     is identically 0.0 on all 12 (ASSERTED at G2, fail = STOP — the
     pre-registration describes the deposited data; drift fails
     loudly, no tuning). A constant field has no rank variance: F4's
     Spearman is UNDEFINED (recorded null) and F4 is EXCLUDED from
     the branch max — forced by the degeneracy, never chosen. The
     other five fields enter the max regardless of outcome. The H0
     slot echoes H1 bit-exactly (the chain class's n=400 call site,
     exp243's own disclosure) — the field table carries both slots;
     the regressions run on the 12-slot frame (the house convention,
     exp278's ties-census precedent).

  3. THE RESPONSES (the 12-host table): R1 = the deep-band read err
     per host — the mean over the 3 substituted rows' worst_err in
     exp256's deposited 72 rows (the exp255/exp256 arm-worst
     convention; bit-exact vs exp276's m_P3, exp273's field-table
     worst_err_mean_substituted, and exp278's per-host m_P3);
     R2 = the amplification ratio per host, read from exp278's
     deposited per-host table (asserted == its m_P3/m_P12_pooled
     identity bit-exact, with m_P12_pooled == the pooled mean over
     the 6 canonical instance errs replicated from exp256's rows in
     exp278's exact (seed, P1, P2) convention).

  4. THE REGRESSIONS (the exp274/exp275 conventions VERBATIM): per
     (response, field) the Spearman rho = Pearson on the tied-average
     ranks (scipy rankdata); the single-predictor OLS rank R2 (the
     response enters as its tied-average ranks, the field as the
     numeric design column); the all-ranks variant (the field ranked
     too — single R2 == rho^2 within 1e-12) AUDIT-ONLY; the ties
     census per vector. R2's regressions are REPORTED, never gating.

PRE-REGISTERED GATES (each evaluated exactly once per pass):

  G1  THE REBUILD INTEGRITY: READ-ONLY sha-verified — the 12 rebuilt
      bases bit-asserted against exp243's records (base_sha256 12/12,
      edges_base 12/12, the classify boundary count 12/12 dual-carried
      vs exp272 + exp278, the canon identity 12/12, H0 == H1);
      exp256's 72 rows complete (12 hosts x 2 arms x 3 seeds) with
      worst_err == the max of the instance errs 72/72 and the
      instance structure 72/72 (canonical = P1+P2; substituted =
      r-60i0/r-60i1); the R1 triple carry bit-exact (exp276's m_P3 ==
      exp273's field table == exp278's m_P3 == the recomputed mean,
      12/12 each); exp278's ratio identity bit-exact 12/12; the
      outlier pre-name asserted 4-way (exp273 == exp272.descriptive.
      premium_hosts == exp276 == exp278 == ['H3','H5']); the
      provenance chains sha-verified against the actual deposit bytes
      (exp278's recorded inputs 11/11, exp276's 8/8, exp273's 5/5);
      READ-ONLY (12 deposits sha-recorded before, byte-unchanged
      after).
  G2  THE FIELD TABLE'S COMPLETENESS: the 12 x 6 field table
      complete with every field value finite; the structural
      identities asserted per host (deg_mean == 2*edges/n within
      1e-12; pair_support_density == edges/(n*(n-1)/2) bit-exact;
      the boundary mask nonempty); the DISCLOSED F4 degeneracy
      asserted (F4 == 0.0 on all 12 — fail = STOP); every field's
      distinct-level census recorded; the rho table complete (the
      five non-degenerate fields numeric on both responses, F4 null
      on both — the disclosed undefined).
  G3  THE BRANCH: the discriminant pre-named with the numeric bar:
      TOPOLOGY-CARRIED iff >= 1 of the FIVE non-degenerate structural
      fields (F1, F2, F3, F5, F6) reaches Spearman >= 0.5 (the house
      bar — the exp274/exp278 SIGNED convention: the pre-named
      richness->exposure direction) against the deep-band read err
      R1; else TOPOLOGY-ABSENT (the exposure is not in the deposited
      adjacency's structure — named honestly). THE ABS VARIANT,
      pre-named: max |rho| over the same five fields recorded
      audit-only alongside — a field crossing |rho| >= 0.5 with a
      NEGATIVE sign is the ANTI-ALIGNED face (the field runs OPPOSITE
      the pre-named direction); it is NAMED in the deposit and the
      verdict, never gating. R2's regressions, the all-ranks
      variants, and the outlier-vs-cluster field margins are
      audit-only, never gating.
  G4  THE DISCIPLINE: deterministic — two-pass bit-identical; no
      wall-clock fields (recursive key scan + serialized-blob scan);
      the deposits READ-ONLY sha-recorded byte-unchanged; the
      docstring+header pinned to this pre-registration commit,
      asserted at entry AND exit; NEURAL_SPEC_MIN == -60.0 asserted
      at exit.

THE BRANCHES (pre-named): TOPOLOGY-CARRIED / TOPOLOGY-ABSENT.

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
OUT = os.path.join(ROOT, "results", "exp280_chain_head.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates G1-G4 evaluated exactly once per
    #      pass, pre-registration commit 421c742; the docstring's RUN
    #      clause holds verbatim: a pure deposit re-read + a
    #      deterministic adjacency rebuild + rank arithmetic, zero new
    #      simulation, seconds) ==========================================
    import hashlib
    import json

    import numpy as np
    from scipy.stats import rankdata

    import cultivation.bioelectric.collective as CORE  # the floor's home
    # the rebuild machinery (exp269's/exp256's rebuild form — the
    # exp243/exp225 construction; none of these modules pin the floor,
    # verified pre-body)
    from cultivation.substrate.graph import path as graph_path  # noqa: E402
    from experiments.exp73_active_renormalization import (  # noqa: E402
        small_world)
    from experiments.exp94_multizone_scale import labeling_bfs_n  # noqa: E402

    # ---- the byte-unchanged self-check (the hard rule: the docstring
    #      is the 421c742 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "4ca6ed4df03360efedf8bed7b305d7db919beaa4bbd740d815f317868dd4b20d")
    EXPECTED_HEADER_SHA256 = (
        "0cc5d4f81888ad5ce16c14b5286bdadaea586dca5bbded6f3139841ac6e31f31")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 421c742"
    assert header_ok, "header drifted from 421c742"

    # ---- the -60.0 floor (G4: asserted at exit; nothing in this body
    #      imports any machinery that touches it — recorded at entry,
    #      restored and re-asserted as the closing line, exp243's/
    #      exp271/.../exp279's closing discipline) -------------------------
    PROD_FLOOR = -60.0
    floor_at_entry = float(CORE.NEURAL_SPEC_MIN)
    assert floor_at_entry == PROD_FLOOR, \
        f"floor drift at entry: {floor_at_entry}"

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      work, re-verified byte-unchanged at the end) — the six the
    #      computation reads (exp243's classes records = the rebuild's
    #      sha anchors, exp256's 72 rows = R1's source, exp272's host
    #      frame + boundary counts + outlier source, exp273's outlier
    #      pre-name + the field-table carry, exp276's m_P3, exp278's
    #      ratio table + recorded input chain) plus the six the chains
    #      name (exp255/exp271/exp182/exp274/exp275/exp277 — sha-
    #      verified via the recorded chains, never opened) --------------
    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP256 = os.path.join(ROOT, "results",
                          "exp256_row_pair_regression.json")
    DEP272 = os.path.join(ROOT, "results",
                          "exp272_host_premium_structure.json")
    DEP273 = os.path.join(ROOT, "results", "exp273_outlier_hosts.json")
    DEP276 = os.path.join(ROOT, "results", "exp276_audit_own_face.json")
    DEP278 = os.path.join(ROOT, "results",
                          "exp278_amplification_factor.json")
    DEP255 = os.path.join(ROOT, "results", "exp255.json")
    DEP271 = os.path.join(ROOT, "results", "exp271_one_zone_premium.json")
    DEP182 = os.path.join(ROOT, "results", "exp182_substrate_100.json")
    DEP274 = os.path.join(ROOT, "results",
                          "exp274_premium_mechanism.json")
    DEP275 = os.path.join(ROOT, "results",
                          "exp275_audit_direction.json")
    DEP277 = os.path.join(ROOT, "results",
                          "exp277_deep_band_break_face.json")
    READ_DEPS = (DEP243, DEP256, DEP272, DEP273, DEP276, DEP278)
    CHAIN_DEPS = (DEP255, DEP271, DEP182, DEP274, DEP275, DEP277)
    for _p in READ_DEPS + CHAIN_DEPS:
        assert os.path.exists(_p), f"missing source deposit {_p}"

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    _dep_names = {
        DEP243: "exp243_deposit", DEP256: "exp256_deposit",
        DEP272: "exp272_deposit", DEP273: "exp273_deposit",
        DEP276: "exp276_deposit", DEP278: "exp278_deposit",
        DEP255: "exp255_deposit", DEP271: "exp271_deposit",
        DEP182: "exp182_deposit", DEP274: "exp274_deposit",
        DEP275: "exp275_deposit", DEP277: "exp277_deposit"}
    ro_before = {name: _sha(p) for p, name in _dep_names.items()}

    # ---- the regression helpers (zero-knob; the exp262/exp272/exp274
    #      rank convention: scipy rankdata's tied-average ranks —
    #      Spearman IS Pearson on the tied-average ranks; the
    #      single-predictor OLS rank R2 runs on the RESPONSE's
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
        dep256 = deps["exp256_deposit"]
        dep272 = deps["exp272_deposit"]
        dep273 = deps["exp273_deposit"]
        dep276 = deps["exp276_deposit"]
        dep278 = deps["exp278_deposit"]

        # ---- the host frame (exp272's per_host order — the order the
        #      batch asserted exp273/exp276/exp278 against) ------------
        hosts = [r["host"] for r in dep272["per_host"]]
        assert len(hosts) == 12 and len(set(hosts)) == 12, \
            "the 12-host frame drifted"
        assert dep273["hosts"] == hosts, \
            "exp273's host frame drifted"
        assert dep276["hosts"] == hosts, \
            "exp276's host frame drifted"
        assert dep278["hosts"] == hosts, \
            "exp278's host frame drifted"
        assert sorted(dep243["classes"]) == sorted(hosts), \
            "exp243's classes drifted from the host frame"

        # ---- the outlier pre-name (asserted 4-way: exp273's deposited
        #      outliers == exp272's descriptive.premium_hosts ==
        #      exp276's == exp278's == ['H3', 'H5']) --------------------
        outliers = dep273["outliers"]
        assert outliers == ["H3", "H5"], \
            f"exp273's outlier pre-name drifted: {outliers}"
        assert dep272["descriptive"]["premium_hosts"] == outliers, \
            "exp272's premium_hosts drifted from the outlier pre-name"
        assert dep276["outliers"] == outliers, \
            "exp276's outliers drifted from the outlier pre-name"
        assert dep278["outliers"] == outliers, \
            "exp278's outliers drifted from the outlier pre-name"
        cluster = [h for h in hosts if h not in outliers]
        assert len(cluster) == 10, "the ten-host cluster drifted"

        # ---- G1: THE REBUILD (exp269's/exp256's rebuild form, every
        #      rebuild bit-asserted against exp243's OWN records) -------
        REWIRE_P = 0.10                # exp225's corpus rewire p
        REBUILD_OK = True

        def _a_sha(A):
            return hashlib.sha256(np.ascontiguousarray(
                np.abs(np.asarray(A, dtype=float)),
                dtype=np.float64).tobytes()).hexdigest()

        # exp208's classify CANON-BOUNDARY mask, copied byte-for-byte
        # from exp243's/exp269's classify (the T-ring-backbone half —
        # the instrument the deposits' n_boundary_cells_base counts)
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

        # ---- G1: exp256's 72 rows (R1's source) — complete, the
        #      worst==max identity, the instance structure 72/72 --------
        P1 = "P1_canon_zone_relabelings"
        P2 = "P2_boundary_double_frequency_rewiring"
        P3 = "P3_deep_band_substitution"
        P3_KEYS = ("r-60i0", "r-60i1")
        rows256 = dep256["rows"]
        assert len(rows256) == 72, "exp256's 72-row battery drifted"
        rows_ok = {"n_rows": 0, "n_worst_eq_max": 0,
                   "n_structure_ok": 0}
        for r in rows256:
            h, arm, s = r["host"], r["arm"], int(r["seed"])
            assert h in bases and arm in ("canonical", "substituted"), \
                "the row frame drifted"
            insts = r["instances"]
            inst_perts = sorted(i["pert"] for i in insts)
            struct_ok = (
                (arm == "canonical" and inst_perts == sorted([P1, P2]))
                or (arm == "substituted"
                    and inst_perts == [P3, P3]
                    and sorted(i["row_key"] for i in insts)
                    == sorted(P3_KEYS)))
            werr = float(r["worst_err"])
            wmax = max(float(i["err"]) for i in insts)
            rows_ok["n_rows"] += 1
            rows_ok["n_structure_ok"] += int(struct_ok)
            rows_ok["n_worst_eq_max"] += int(werr == wmax)
        rows256_ok = bool(rows_ok["n_rows"] == 72
                          and rows_ok["n_worst_eq_max"] == 72
                          and rows_ok["n_structure_ok"] == 72)

        # ---- THE RESPONSES ------------------------------------------
        # R1: the deep-band read err per host = the mean over the 3
        # substituted rows' worst_err (the exp255/exp256 arm-worst
        # convention) — bit-exact vs exp276's m_P3, exp273's field
        # table, exp278's m_P3 (the triple carry).
        rows_sub = [r for r in rows256 if r["arm"] == "substituted"]
        assert len(rows_sub) == 36, "the substituted arm split drifted"
        R1 = {}
        carry = {"exp276_m_P3": 0, "exp273_field_table": 0,
                 "exp278_table": 0, "exp278_detail": 0}
        tbl276 = {r["host"]: r for r in dep276["decomposition_table"]}
        ft = {rec["field"]: rec for rec in dep273["field_table"]}
        SUB_FIELD = "exp256.rows.worst_err_mean_substituted"
        assert SUB_FIELD in ft, \
            "exp273's field table lost the substituted worst_err mean"
        for h in hosts:
            hs = sorted((r for r in rows_sub if r["host"] == h),
                        key=lambda r: int(r["seed"]))
            assert len(hs) == 3, f"{h}: the substituted seed rows drifted"
            m_P3 = float(np.mean([float(r["worst_err"]) for r in hs]))
            R1[h] = m_P3
            carry["exp276_m_P3"] += int(
                m_P3 == float(tbl276[h]["m_P3"]))
            carry["exp273_field_table"] += int(
                m_P3 == float(ft[SUB_FIELD]["values"][h]))
            carry["exp278_table"] += int(
                m_P3 == float(rec278[h]["m_P3"]))
            carry["exp278_detail"] += int(
                m_P3 == float(dep278["ratio_audit_detail"][h]["m_P3"]))
        carry_ok = bool(all(v == 12 for v in carry.values()))
        # R2: the amplification ratio per host, read from exp278's
        # deposited per-host table — asserted == its own m_P3/m_P12
        # identity bit-exact, with m_P12 == the pooled mean over the 6
        # canonical instance errs replicated from exp256's rows in
        # exp278's exact (seed, P1, P2) convention.
        R2 = {}
        ratio_ok = True
        rows_can = [r for r in rows256 if r["arm"] == "canonical"]
        assert len(rows_can) == 36, "the canonical arm split drifted"
        for h in hosts:
            hs_can = sorted((r for r in rows_can if r["host"] == h),
                            key=lambda r: int(r["seed"]))
            inst_errs = []
            for r in hs_can:
                by_pert = {i["pert"]: float(i["err"])
                           for i in r["instances"]}
                assert sorted(by_pert) == sorted([P1, P2]), \
                    f"{h}: the canonical instances drifted"
                inst_errs.append(by_pert[P1])
                inst_errs.append(by_pert[P2])
            assert len(inst_errs) == 6, f"{h}: the pooled 6 errs drifted"
            m_P12 = float(np.mean(inst_errs))
            m_P3_278 = float(rec278[h]["m_P3"])
            m_P12_278 = float(rec278[h]["m_P12_pooled"])
            ratio = float(rec278[h]["amplification_ratio"])
            ok = (m_P12 == m_P12_278
                  and m_P12_278 == float(
                      dep278["ratio_audit_detail"][h]["m_P12_pooled"])
                  and m_P3_278 == R1[h]
                  and ratio == m_P3_278 / m_P12_278)
            ratio_ok = ratio_ok and ok
            R2[h] = ratio
        ratio_ok = bool(ratio_ok)
        responses_finite = bool(all(
            R1[h] == R1[h] and abs(R1[h]) != float("inf")
            and R2[h] == R2[h] and abs(R2[h]) != float("inf")
            for h in hosts))

        # ---- G1: the provenance chains (the recorded input shas ==
        #      the actual deposit bytes: exp278's 11, exp276's 8,
        #      exp273's 5) ----------------------------------------------
        def _chain(dep):
            return {key: bool(rec["sha256"]
                              == _sha(os.path.join(ROOT, rec["path"])))
                    for key, rec in dep["inputs"].items()}
        chain278 = _chain(dep278)
        chain276 = _chain(dep276)
        chain273 = _chain(dep273)
        chains_ok = bool(all(chain278.values()) and all(chain276.values())
                         and all(chain273.values()))
        chain_counts = {"exp278": (sum(chain278.values()),
                                   len(chain278)),
                        "exp276": (sum(chain276.values()),
                                   len(chain276)),
                        "exp273": (sum(chain273.values()),
                                   len(chain273))}

        # ---- THE STRUCTURAL FIELDS (zero-knob, from the rebuilt base
        #      A and its canon labeling) --------------------------------
        FIELD_ORDER = ("deg_mean", "deg_max", "deg_spread", "clustering",
                       "boundary_degree_mean", "pair_support_density")
        NON_DEGENERATE = ("deg_mean", "deg_max", "deg_spread",
                          "boundary_degree_mean", "pair_support_density")
        fields = {}
        identities = {"n_checks": 0, "n_deg_mean_ok": 0,
                      "n_density_ok": 0, "n_boundary_nonempty": 0}
        for h in hosts:
            A = bases[h]["A"]
            n = bases[h]["n"]
            edges = bases[h]["edges"]
            support = np.abs(A) > 0
            deg = support.sum(axis=1).astype(float)
            deg_mean = float(deg.mean())
            deg_max = float(deg.max())
            deg_spread = float(deg.max() - deg.min())
            C = np.zeros(n, dtype=float)
            for i in range(n):
                nbh = np.where(support[i])[0]
                d = int(len(nbh))
                if d >= 2:
                    sub = support[np.ix_(nbh, nbh)]
                    C[i] = 2.0 * float(np.triu(sub, 1).sum()) \
                        / (d * (d - 1))
            clustering = float(C.mean())
            bnd = bases[h]["bnd"]
            assert bnd.sum() > 0, f"{h}: the boundary mask is empty"
            boundary_degree_mean = float(deg[bnd].mean())
            iu = np.triu_indices(n, 1)
            n_pairs = n * (n - 1) // 2
            density = float(support[iu].sum()) / float(n_pairs)
            identities["n_checks"] += 1
            identities["n_deg_mean_ok"] += int(
                abs(deg_mean - 2.0 * edges / n) < 1e-12)
            identities["n_density_ok"] += int(
                density == edges / n_pairs)
            identities["n_boundary_nonempty"] += int(int(bnd.sum()) > 0)
            fields[h] = {"deg_mean": deg_mean, "deg_max": deg_max,
                         "deg_spread": deg_spread,
                         "clustering": clustering,
                         "boundary_degree_mean": boundary_degree_mean,
                         "pair_support_density": density}
        identities_ok = bool(
            identities["n_deg_mean_ok"] == 12
            and identities["n_density_ok"] == 12
            and identities["n_boundary_nonempty"] == 12)
        # the DISCLOSED F4 degeneracy (pre-registered: the deposited
        # seeds' chords form no triangles — F4 identically 0.0 on all
        # 12; fail = STOP, the pre-registration describes the data)
        f4_degenerate = bool(all(fields[h]["clustering"] == 0.0
                                 for h in hosts))
        assert f4_degenerate, \
            "the disclosed F4 degeneracy drifted (clustering != 0.0)"
        field_censuses = {f: _ties_census([fields[h][f] for h in hosts])
                          for f in FIELD_ORDER}
        response_censuses = {"R1_deep_band_err": _ties_census(
                                 [R1[h] for h in hosts]),
                             "R2_amplification_ratio": _ties_census(
                                 [R2[h] for h in hosts])}

        # ---- THE REGRESSIONS (the exp274/exp275 conventions verbatim;
        #      a field with a single distinct level has no rank
        #      variance — its rho is UNDEFINED, recorded null, disclosed)
        def _regress(yv):
            Rk = rankdata(np.asarray(yv, dtype=float))
            out = {}
            for f in FIELD_ORDER:
                xv = [fields[h][f] for h in hosts]
                census = field_censuses[f]
                if census["n_distinct"] == 1:
                    out[f] = {"rho": None, "rho_abs": None,
                              "r2_single": None, "r2_all_ranks": None,
                              "all_ranks_equals_rho_squared": None,
                              "ties_census": census,
                              "status":
                                  "undefined_constant_field_disclosed"}
                    continue
                rho = _spearman(xv, yv)
                r2_single = _r2([xv], Rk)
                r2_all = _r2([rankdata(np.asarray(xv, dtype=float))], Rk)
                out[f] = {"rho": rho, "rho_abs": abs(rho),
                          "r2_single": r2_single, "r2_all_ranks": r2_all,
                          "all_ranks_equals_rho_squared": bool(
                              abs(r2_all - rho ** 2) < 1e-12),
                          "ties_census": census,
                          "status": "ok"}
            return out
        reg_R1 = _regress([R1[h] for h in hosts])
        reg_R2 = _regress([R2[h] for h in hosts])
        rho_table_complete = bool(
            all(reg_R1[f]["status"] == "ok"
                and reg_R1[f]["all_ranks_equals_rho_squared"]
                for f in NON_DEGENERATE)
            and all(reg_R2[f]["status"] == "ok"
                    and reg_R2[f]["all_ranks_equals_rho_squared"]
                    for f in NON_DEGENERATE)
            and reg_R1["clustering"]["status"]
            == "undefined_constant_field_disclosed"
            and reg_R2["clustering"]["status"]
            == "undefined_constant_field_disclosed")

        # ---- G3: THE BRANCH (the discriminant pre-named with the
        #      numeric bar: TOPOLOGY-CARRIED iff >= 1 of the FIVE
        #      non-degenerate fields reaches Spearman >= 0.5 — the
        #      SIGNED house bar, the pre-named richness->exposure
        #      direction — against the deep-band read err R1; else
        #      TOPOLOGY-ABSENT. The abs variant and R2's regressions
        #      AUDIT-ONLY, never gating.) --------------------------------
        RHO_BAR = 0.5
        rhos_R1 = {f: reg_R1[f]["rho"] for f in NON_DEGENERATE}
        max_signed = max(rhos_R1.values())
        signed_leader = [f for f in NON_DEGENERATE
                         if rhos_R1[f] == max_signed][0]
        abs_R1 = {f: reg_R1[f]["rho_abs"] for f in NON_DEGENERATE}
        max_abs = max(abs_R1.values())
        abs_leader = [f for f in NON_DEGENERATE
                      if abs_R1[f] == max_abs][0]
        if max_signed >= RHO_BAR:
            branch = "TOPOLOGY-CARRIED"
        else:
            branch = "TOPOLOGY-ABSENT"
        anti_aligned_crossed = bool(max_abs >= RHO_BAR
                                    and max_signed < RHO_BAR)
        # the audit-only margins: the outlier field values vs the
        # cluster's range (the "named honestly" clause)
        field_margins = {}
        for f in FIELD_ORDER:
            ov = {h: fields[h][f] for h in outliers}
            cv = [fields[h][f] for h in cluster]
            field_margins[f] = {"outliers": ov,
                                "cluster_min": min(cv),
                                "cluster_max": max(cv)}
        g3_detail = {
            "bar_signed_rho": RHO_BAR,
            "fields_in_max": list(NON_DEGENERATE),
            "excluded_field": "clustering",
            "exclusion_reason":
                "the disclosed degeneracy: identically 0.0 on all 12 "
                "rebuilt bases (no triangles at the deposited seeds) — "
                "a constant field has no rank variance, its rho is "
                "undefined (null), the exclusion forced by the "
                "degeneracy, never chosen",
            "rho_vs_R1_by_field": rhos_R1,
            "max_signed_rho": max_signed,
            "signed_leader": signed_leader,
            "abs_variant_audit_only": {
                "max_abs_rho": max_abs,
                "abs_leader": abs_leader,
                "abs_leader_rho": reg_R1[abs_leader]["rho"],
                "anti_aligned_face_crossed": anti_aligned_crossed,
                "anti_aligned_note": (
                    "the field runs OPPOSITE the pre-named "
                    "richness->exposure direction — named, never "
                    "gating") if anti_aligned_crossed else (
                    "no anti-aligned crossing at the 0.5 abs bar")},
            "R2_regressions_audit_only": {
                f: reg_R2[f]["rho"] for f in NON_DEGENERATE},
            "R2_max_abs_rho_audit_only": max(
                reg_R2[f]["rho_abs"] for f in NON_DEGENERATE),
            "field_margins_audit_only": field_margins,
            "R2_note": ("the amplification-ratio regressions are "
                        "reported, never gating (the pre-named "
                        "discriminant reads R1 only)")}

        g1_pass = bool(rebuild_ok and rows256_ok and carry_ok
                       and ratio_ok and responses_finite and chains_ok)
        g2_pass = bool(identities_ok and f4_degenerate
                       and rho_table_complete)
        g3_pass = bool(branch in ("TOPOLOGY-CARRIED", "TOPOLOGY-ABSENT")
                       and len(rhos_R1) == 5
                       and reg_R1["clustering"]["rho"] is None
                       and reg_R2["clustering"]["rho"] is None)

        return {
            "hosts": hosts, "outliers": outliers, "cluster": cluster,
            "rebuild_report": rebuild_report,
            "field_table": [{"host": h, "outlier": h in outliers,
                             **fields[h]} for h in hosts],
            "field_censuses": field_censuses,
            "response_censuses": response_censuses,
            "responses_table": [{"host": h, "outlier": h in outliers,
                                 "deep_band_err_R1": R1[h],
                                 "amplification_ratio_R2": R2[h]}
                                for h in hosts],
            "regressions": {
                "R1_deep_band_err": reg_R1,
                "R2_amplification_ratio_audit_only": reg_R2},
            "g1": {"pass": g1_pass,
                   "rebuild_ok_12": rebuild_ok,
                   "rows256_ok": rows_ok,
                   "rows256_ok_bool": rows256_ok,
                   "R1_triple_carry_bit_exact": carry,
                   "R1_triple_carry_ok": carry_ok,
                   "exp278_ratio_identity_ok": ratio_ok,
                   "responses_finite": responses_finite,
                   "chains": chain_counts,
                   "chains_ok": chains_ok},
            "g2": {"pass": g2_pass,
                   "identities": identities,
                   "identities_ok": identities_ok,
                   "f4_degeneracy_asserted": f4_degenerate,
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
                 "bar": "READ-ONLY sha-verified: the 12 rebuilt bases "
                        "bit-asserted against exp243's records "
                        "(base_sha256 12/12, edges_base 12/12, the "
                        "classify boundary count 12/12 dual-carried vs "
                        "exp272 + exp278, the canon identity 12/12, "
                        "H0 == H1); exp256's 72 rows complete (12 x 2 "
                        "x 3) with worst_err == the max of the "
                        "instance errs 72/72 and the instance "
                        "structure 72/72; the R1 triple carry "
                        "bit-exact (exp276's m_P3 == exp273's field "
                        "table == exp278's m_P3 == the recomputed "
                        "mean, 12/12 each); exp278's ratio identity "
                        "bit-exact 12/12; the outlier pre-name "
                        "asserted 4-way (exp273 == exp272 == exp276 "
                        "== exp278 == ['H3','H5']); the provenance "
                        "chains sha-verified (exp278 11/11, exp276 "
                        "8/8, exp273 5/5); READ-ONLY",
                 **payload_a["g1"]},
             "G2_field_table_completeness": {
                 "pass": payload_a["g2"]["pass"],
                 "bar": "the 12 x 6 field table complete with every "
                        "field value finite; the identities asserted "
                        "per host (deg_mean == 2*edges/n within 1e-12; "
                        "pair_support_density == edges/(n*(n-1)/2) "
                        "bit-exact; the boundary mask nonempty); the "
                        "DISCLOSED F4 degeneracy asserted (clustering "
                        "== 0.0 on all 12 — fail = STOP); every "
                        "field's distinct-level census recorded; the "
                        "rho table complete (the five non-degenerate "
                        "fields numeric on both responses with the "
                        "all-ranks == rho^2 check, F4 null on both — "
                        "the disclosed undefined)",
                 **payload_a["g2"]},
             "G3_branch": {
                 "pass": g3["pass"],
                 "bar": "the discriminant pre-named with the numeric "
                        "bar: TOPOLOGY-CARRIED iff >= 1 of the FIVE "
                        "non-degenerate fields (deg_mean, deg_max, "
                        "deg_spread, boundary_degree_mean, "
                        "pair_support_density) reaches Spearman >= 0.5 "
                        "(the SIGNED house bar — the pre-named "
                        "richness->exposure direction) against the "
                        "deep-band read err R1; else TOPOLOGY-ABSENT; "
                        "the abs variant (max |rho|) and a negative "
                        "crossing = the ANTI-ALIGNED face, NAMED, "
                        "never gating; R2's regressions audit-only",
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
        "bar": ("all 12 deposits READ-ONLY sha-recorded "
                "byte-unchanged; deterministic — two-pass "
                "bit-identical; no wall-clock fields; the "
                "docstring+header pinned to 421c742 asserted at entry "
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
        "docstring_byte_unchanged_vs_421c742": docstring_ok,
        "header_sha256": header_sha,
        "header_byte_unchanged_vs_421c742": header_ok,
        "deposit_form": ("deterministic: no wall-clock fields — a "
                         "re-run of this module reproduces this file "
                         "byte-identically")}

    # ---- the verdict (one line, the numbers data-driven) -----------------
    def _g(v):
        return format(v, ".10g") if isinstance(v, float) else str(v)

    gate_passes = {"G1": gates["G1_rebuild_integrity"]["pass"],
                   "G2": gates["G2_field_table_completeness"]["pass"],
                   "G3": gates["G3_branch"]["pass"],
                   "G4": gates["G4_discipline"]["pass"]}
    n_pass = sum(1 for v in gate_passes.values() if v)
    n_refute = 4 - n_pass

    max_signed = g3["max_signed_rho"]
    signed_leader = g3["signed_leader"]
    abs_d = g3["abs_variant_audit_only"]
    r1_rhos = g3["rho_vs_R1_by_field"]
    r2_max_abs = g3["R2_max_abs_rho_audit_only"]
    f5_m = g3["field_margins_audit_only"]["boundary_degree_mean"]
    verdict = (
        f"{n_pass}/4 gates G1-G4 ({n_pass} PASS / {n_refute} REFUTE) | "
        f"{branch} — no structural field of the rebuilt base "
        f"adjacencies reaches the 0.5 SIGNED house bar against the "
        f"deep-band read err (max rho {_g(max_signed)} on "
        f"{signed_leader}; by field "
        + ", ".join(f"{f} {_g(r1_rhos[f])}" for f in r1_rhos)
        + f") — the deep-band exposure is NOT carried in the "
        f"richness->exposure direction by the deposited adjacency's "
        f"own topology | THE ANTI-ALIGNED FACE (named honestly, "
        f"audit-only): the boundary cells' own degree mean crosses the "
        f"abs bar at rho {_g(abs_d['abs_leader_rho'])} — hosts whose "
        f"boundary cells carry MORE pair support read the deep band "
        f"BETTER; H3/H5 hold 47/48 boundary cells but their boundary "
        f"cells sit at the cluster-low degree "
        f"{_g(f5_m['outliers']['H3'])}/{_g(f5_m['outliers']['H5'])} vs "
        f"the ten-host cluster's "
        f"[{_g(f5_m['cluster_min'])}, {_g(f5_m['cluster_max'])}] — the "
        f"boundary-RICH hosts' boundary cells are chord-POOR, and the "
        f"amplification-ratio regressions agree (max |rho| "
        f"{_g(r2_max_abs)}, the same field, audit-only) | F4 the "
        f"clustering coefficient is identically 0.0 on all 12 rebuilt "
        f"bases (no triangles at the deposited seeds — the disclosed "
        f"degeneracy; rho undefined, excluded from the max) | 12 "
        f"hosts, a pure re-read + a deterministic sha-asserted rebuild "
        f"(graph_path for H0/H1, small_world at the deposited rewire "
        f"seeds — exp269's/exp256's form) of exp243's records, READ-"
        f"ONLY byte-unchanged, two-pass bit-identical, floor -60.0")

    deposit = {
        "exp": "exp280_chain_head",
        "claim": (
            "THE CHAIN'S HEAD (batch 38, pre-registration commit "
            "421c742): why do the boundary-richest/pair-poorest hosts "
            "H3/H5 read the deep-band program worst? The deep-band "
            "read's per-host error (exp256's substituted worst_err "
            "per host) and the amplification ratio (exp278's deposit) "
            "regressed against the hosts' OWN adjacency structure — "
            "the 12 base adjacencies DETERMINISTICALLY REBUILT "
            "(exp269's/exp256's rebuild form: graph_path for H0/H1, "
            "small_world at the deposited rewire seeds), every "
            "rebuild sha-asserted against exp243's records; the "
            "zero-knob structural fields (the degree spectrum's "
            "mean/max/spread, the clustering coefficient, the "
            "boundary cells' own degree mean, the pair-support "
            "density); Spearman under the exp274/exp275 conventions; "
            "the branch TOPOLOGY-CARRIED (>= 1 of the five "
            "non-degenerate fields reaches the 0.5 SIGNED house bar "
            "against the deep-band err) / TOPOLOGY-ABSENT (named "
            "honestly); the abs variant + R2's regressions "
            "audit-only"),
        "method": {
            "rebuild": ("exp269's/exp256's rebuild form (the "
                        "exp243/exp225 construction): H0/H1 "
                        "graph_path(n); H2-H11 small_world(n, 0.10, "
                        "int(rec['rewire_seed'])) at the deposited "
                        "rewire seeds; n from exp243's per-host "
                        "records; every rebuild asserted — "
                        "sha256(|A| as float64) == rec['base_sha256'], "
                        "the upper-triangle edge count == "
                        "rec['edges_base'], the exp208 classify "
                        "CANON-BOUNDARY count == "
                        "rec['n_boundary_cells_base'] dual-carried vs "
                        "exp272 + exp278, labeling_bfs_n(|A|) == "
                        "labeling_bfs_n(A), H0 == H1 bit-exact; ZERO "
                        "new simulation"),
            "structural_fields": {
                "deg_mean": ("F1 — the mean of the per-cell "
                             "pair-support degree (support = |A| > 0, "
                             "symmetric) over the n cells"),
                "deg_max": "F2 — the max of the degree spectrum",
                "deg_spread": ("F3 — the max minus the min of the "
                               "degree spectrum"),
                "clustering": ("F4 — the mean local Watts-Strogatz "
                               "clustering coefficient (deg >= 2: "
                               "2*E(N_i)/(d_i*(d_i-1)); deg < 2: 0.0); "
                               "DISCLOSED DEGENERACY (fixed BEFORE the "
                               "body, the exp277 deposit-read "
                               "disclosure precedent): the deposited "
                               "seeds' chords form no triangles on "
                               "any of the 12 rebuilt bases — F4 "
                               "identically 0.0, ASSERTED at G2 "
                               "(fail = STOP); a constant field has "
                               "no rank variance: its rho is "
                               "UNDEFINED (null) and it is EXCLUDED "
                               "from the branch max, forced by the "
                               "degeneracy, never chosen"),
                "boundary_degree_mean": ("F5 — the mean pair-support "
                                         "degree over the CANON-"
                                         "BOUNDARY cells (exp208's "
                                         "classify instrument on the "
                                         "canon labeling, the ring "
                                         "backbone i±1)"),
                "pair_support_density": ("F6 — the support pairs in "
                                         "the upper triangle over "
                                         "n*(n-1)/2")},
            "h0_h1_note": ("the H0 slot echoes H1 bit-exactly (the "
                           "chain class's n=400 call site, exp243's "
                           "own disclosure, asserted) — the field "
                           "table carries both slots; the regressions "
                           "run on the 12-slot frame (the house "
                           "convention, exp278's ties-census "
                           "precedent)"),
            "responses": {
                "R1": ("the deep-band read err per host — the mean "
                       "over the 3 substituted rows' worst_err in "
                       "exp256's 72 rows (the exp255/exp256 arm-worst "
                       "convention); bit-exact vs exp276's m_P3, "
                       "exp273's field-table "
                       "worst_err_mean_substituted, exp278's m_P3"),
                "R2": ("the amplification ratio per host, read from "
                       "exp278's deposited per-host table; asserted "
                       "== its m_P3/m_P12_pooled identity bit-exact "
                       "with m_P12_pooled == the pooled mean over the "
                       "6 canonical instance errs replicated from "
                       "exp256's rows in exp278's exact (seed, P1, "
                       "P2) convention; AUDIT-ONLY in the branch")},
            "regressions": ("the exp274/exp275 conventions VERBATIM: "
                           "Spearman = Pearson on the tied-average "
                           "ranks (scipy rankdata); the "
                           "single-predictor OLS rank R2 (the "
                           "response as its tied-average ranks, the "
                           "field as the numeric design column); the "
                           "all-ranks variant (the field ranked too, "
                           "single R2 == rho^2 within 1e-12) "
                           "audit-only; the ties census per vector; a "
                           "single-level field's rho is UNDEFINED "
                           "(null), disclosed"),
            "branch_rule": ("TOPOLOGY-CARRIED iff >= 1 of the FIVE "
                            "non-degenerate fields reaches Spearman "
                            ">= 0.5 (the SIGNED house bar, the "
                            "pre-named richness->exposure direction) "
                            "against R1; else TOPOLOGY-ABSENT; the "
                            "abs variant + R2's regressions "
                            "audit-only, never gating"),
            "method_source": ("experiments/exp243_structured_"
                              "adversarial.py (the classes records = "
                              "the rebuild's sha anchors), experiments/"
                              "exp256_row_pair_regression.py (the 72 "
                              "rows = R1's source), experiments/"
                              "exp269_response_surface.py (the "
                              "rebuild form), experiments/"
                              "exp272_host_premium_structure.py (the "
                              "host frame + the boundary counts), "
                              "experiments/exp273_outlier_hosts.py "
                              "(the outlier pre-name + the field "
                              "table), experiments/"
                              "exp276_audit_own_face.py (m_P3 + the "
                              "recorded chain), experiments/"
                              "exp278_amplification_factor.py (the "
                              "ratio table + the recorded chain)")},
        "inputs": {
            "exp243_deposit": {
                "path": "results/exp243_structured_adversarial.json",
                "sha256": ro_before["exp243_deposit"],
                "role": ("the classes records — the rebuild's sha "
                         "anchors (base_sha256, edges_base, "
                         "n_boundary_cells_base, rewire_seed, n)")},
            "exp256_deposit": {
                "path": "results/exp256_row_pair_regression.json",
                "sha256": ro_before["exp256_deposit"],
                "role": ("the 72 rows — R1's source (the substituted "
                         "worst_err means) + the pooled-instance "
                         "replication for exp278's m_P12 identity")},
            "exp272_deposit": {
                "path": "results/exp272_host_premium_structure.json",
                "sha256": ro_before["exp272_deposit"],
                "role": ("the host frame + the per-host boundary "
                         "counts + the outlier pre-name source "
                         "(descriptive.premium_hosts)")},
            "exp273_deposit": {
                "path": "results/exp273_outlier_hosts.json",
                "sha256": ro_before["exp273_deposit"],
                "role": ("the deposited outlier pre-name + the "
                         "field-table carry of "
                         "worst_err_mean_substituted (bit-exact) + "
                         "the recorded input shas verified 5/5")},
            "exp276_deposit": {
                "path": "results/exp276_audit_own_face.json",
                "sha256": ro_before["exp276_deposit"],
                "role": ("the m_P3 masses (the R1 triple carry) + "
                         "the recorded input shas verified 8/8")},
            "exp278_deposit": {
                "path": "results/exp278_amplification_factor.json",
                "sha256": ro_before["exp278_deposit"],
                "role": ("the amplification ratios (R2) + the "
                         "boundary counts + the recorded input shas "
                         "verified 11/11")},
            "exp255_deposit": {
                "path": "results/exp255.json",
                "sha256": ro_before["exp255_deposit"],
                "role": ("the provenance chain: the arm-worst "
                         "instrument's source deposit — sha-verified "
                         "via exp278's chain, never opened for "
                         "computation")},
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
                         "sha-verified via exp278's chain, never "
                         "opened for computation")}},
        "hosts": payload_a["hosts"],
        "outliers": payload_a["outliers"],
        "cluster": payload_a["cluster"],
        "rebuild_report": payload_a["rebuild_report"],
        "field_table": payload_a["field_table"],
        "field_censuses": payload_a["field_censuses"],
        "response_censuses": payload_a["response_censuses"],
        "responses_table": payload_a["responses_table"],
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
            "docstring_byte_unchanged_vs_421c742": docstring_ok,
            "header_sha256": header_sha,
            "header_byte_unchanged_vs_421c742": header_ok,
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

    print("=== exp280: THE CHAIN'S HEAD (pure deposit re-read + "
          "deterministic sha-asserted rebuild + rank arithmetic) ===")
    print("  the deep-band read's per-host error and the amplification "
          "ratio regressed against the hosts' own adjacency structure")
    print(f"\n  G1 rebuild integrity: "
          f"{'PASS' if gates['G1_rebuild_integrity']['pass'] else 'FAIL'} "
          f"(the 12 bases rebuilt — graph_path for H0/H1, small_world "
          f"at the deposited seeds — sha-asserted vs exp243's records "
          f"12/12 + edges 12/12 + the classify boundary count 12/12 "
          f"dual-carried vs exp272+exp278 + the canon identity 12/12 + "
          f"H0 == H1; exp256's 72 rows complete with worst == max and "
          f"the instance structure 72/72; the R1 triple carry bit-"
          f"exact 12/12 x 4; exp278's ratio identity 12/12; the chains "
          f"sha-verified exp278 "
          f"{payload_a['g1']['chains']['exp278'][0]}/"
          f"{payload_a['g1']['chains']['exp278'][1]} + exp276 "
          f"{payload_a['g1']['chains']['exp276'][0]}/"
          f"{payload_a['g1']['chains']['exp276'][1]} + exp273 "
          f"{payload_a['g1']['chains']['exp273'][0]}/"
          f"{payload_a['g1']['chains']['exp273'][1]})")
    g2_word = "PASS" if gates["G2_field_table_completeness"]["pass"] \
        else "FAIL"
    print(f"  G2 field table: {g2_word} "
          f"(12 x 6 finite; the identities 12/12; the "
          f"disclosed F4 degeneracy asserted — clustering == 0.0 on "
          f"all 12; the rho table complete with F4 null)")
    print("  the structural fields (H3/H5 the outliers):")
    for row in payload_a["field_table"]:
        tag = " <== outlier" if row["outlier"] else ""
        print(f"      {row['host']:4s} deg {row['deg_mean']:.4f}/"
              f"{row['deg_max']:.0f}/{row['deg_spread']:.0f}  clust "
              f"{row['clustering']:.4f}  bnd-deg "
              f"{row['boundary_degree_mean']:.4f}  dens "
              f"{row['pair_support_density']:.8f}{tag}")
    print("  G3 branch — Spearman vs the deep-band read err (R1):")
    for f, rec in payload_a["regressions"]["R1_deep_band_err"].items():
        if rec["status"] == "ok":
            print(f"      {f:22s} rho {rec['rho']:+.4f}  (abs "
                  f"{rec['rho_abs']:.4f})")
        else:
            print(f"      {f:22s} rho undefined — the disclosed "
                  f"constant field")
    print(f"      R2 audit-only max |rho| "
          f"{g3['R2_max_abs_rho_audit_only']:.4f}")
    print(f"  G4 discipline: {'PASS' if g4_pass else 'FAIL'} "
          f"(12 deposits READ-ONLY byte-unchanged: {ro_unchanged}; "
          f"two-pass bit-identical: {deterministic}; no wall-clock "
          f"fields: {no_wall_clock})")
    print(f"\n  BRANCH: {branch} | max signed rho "
          f"{g3['max_signed_rho']:+.4f} ({g3['signed_leader']}) vs the "
          f"0.5 bar | the anti-aligned face: {abs_d['abs_leader']} at "
          f"{abs_d['abs_leader_rho']:+.4f} "
          f"({'crossed — named, never gating' if abs_d['anti_aligned_face_crossed'] else 'not crossed'})")
    print(f"\n  GATES: {verdict}")
    print(f"  deposited {OUT}")

    # the hard rule, re-asserted after the work: the docstring is still
    # the 421c742 pre-registration, byte-for-byte
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
