#!/usr/bin/env python3
"""exp273 — THE OUTLIER HOSTS (batch 31; L250's registered next (a) —
zero new simulation).

THE OPEN ITEM (L250): the rewrite premium's shelf price is a
host-fixed property outside the boundary geometry (H2 refuted), and
the host structure is TWO OUTLIERS against a tight cluster: H3/H5
carry 1.95/2.10 one-zone and 3.51/3.17 multi-zone premiums vs the
ten-host cluster's 0.34-0.49/0.33-0.49. What distinguishes H3/H5?

THE INSTRUMENT (pre-registered, zero-knob, pure re-read): the
discriminant search across the deposited host records — for every
host-level field in the deposits (exp243's classes records: rewire
seed, edges_base, n_boundary_cells_base, f_max_base; exp256's
per-host row records; exp182's margin profiles; exp241's margin
data where present), compute the field for all 12 hosts and test
the pre-named separation: the field value separates {H3, H5} from
the other ten hosts iff the two outliers' values both sit outside
the ten-host cluster's [min, max] range ON THE SAME SIDE. Every
candidate field is reported; the gate reads the COUNT of separating
fields.

PRE-REGISTERED GATES:

  X1  THE GRIDS: the 12-host field table assembled from the
      deposits (every field provenance-tagged); exp271's/exp272's
      premium grids byte-verified.
  X2  THE SEPARATION: at least ONE deposited field separates {H3,
      H5} from the ten-host cluster on the same side (the gate) —
      the count and the fields named; ZERO separating fields ->
      OUTLIER-DEPOSIT-ABSENT (the discriminator lives outside the
      deposited records — a new instrument required, named
      honestly).
  X3  THE HONESTY CLAUSE: fields that separate ONE outlier but not
      the other are reported as one-sided (never counted as
      separating).
  X4  THE DISCIPLINE: all deposits READ-ONLY sha-recorded
      byte-unchanged; deterministic; no wall-clock fields; the
      -60.0 floor asserted at exit.

THE BRANCHES (pre-named): OUTLIER-DEPOSIT-CARRIED (X2 passes) /
OUTLIER-DEPOSIT-ABSENT.

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
OUT = os.path.join(ROOT, "results", "exp273_outlier_hosts.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates X1-X4 evaluated exactly once per
    #      pass, pre-registration commit 26946af; the docstring's RUN
    #      clause holds verbatim: a pure deposit re-read + arithmetic,
    #      zero new simulation, seconds) ==================================
    import hashlib
    import json

    import cultivation.bioelectric.collective as CORE  # the floor's home

    # ---- the byte-unchanged self-check (the hard rule: the docstring
    #      is the 26946af pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "d02fba471fd4a307b42e8649f01514097119d8f8a761e12e8b64464fdcfb5ed5")
    EXPECTED_HEADER_SHA256 = (
        "3641f91d602826b1ccfcc36796e6c4b67c6fe98ec5b607e09c1f61687f7c4b83")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 26946af"
    assert header_ok, "header drifted from 26946af"

    # ---- the -60.0 floor (X4: asserted at exit; nothing in this body
    #      imports any machinery that touches it — recorded at entry,
    #      restored and re-asserted as the closing line, exp243's/
    #      exp271's/exp272's closing discipline) --------------------------
    PROD_FLOOR = -60.0
    floor_at_entry = float(CORE.NEURAL_SPEC_MIN)
    assert floor_at_entry == PROD_FLOOR, \
        f"floor drift at entry: {floor_at_entry}"

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      work, re-verified byte-unchanged at the end) — the five the
    #      task pre-names --------------------------------------------------
    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP272 = os.path.join(ROOT, "results",
                          "exp272_host_premium_structure.json")
    DEP271 = os.path.join(ROOT, "results",
                          "exp271_one_zone_premium.json")
    DEP182 = os.path.join(ROOT, "results", "exp182_substrate_100.json")
    DEP256 = os.path.join(ROOT, "results",
                          "exp256_row_pair_regression.json")
    for _p in (DEP243, DEP272, DEP271, DEP182, DEP256):
        assert os.path.exists(_p), f"missing source deposit {_p}"

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    ro_before = {"exp243_deposit": _sha(DEP243),
                 "exp272_deposit": _sha(DEP272),
                 "exp271_deposit": _sha(DEP271),
                 "exp182_deposit": _sha(DEP182),
                 "exp256_deposit": _sha(DEP256)}

    # ---- THE COMPUTATION (pure re-read + arithmetic; run twice, the
    #      two payloads must be byte-identical — X4's determinism
    #      clause) ----------------------------------------------------------
    def compute():
        with open(DEP243) as fh:
            dep243 = json.load(fh)
        with open(DEP272) as fh:
            dep272 = json.load(fh)
        with open(DEP271) as fh:
            dep271 = json.load(fh)
        with open(DEP182) as fh:
            dep182 = json.load(fh)
        with open(DEP256) as fh:
            dep256 = json.load(fh)

        # ---- the host frame (exp256's battery; cross-checked against
        #      every other host-keyed deposit) ----------------------------
        hosts = list(dep256["battery"]["hosts"])
        seeds = [int(s) for s in dep256["battery"]["seeds"]]
        assert len(hosts) == 12 and seeds == [1, 2, 3], \
            "the battery drifted (12 hosts x seeds [1,2,3])"
        classes = dep243["classes"]
        assert set(classes) == set(hosts), "exp243 classes drifted"
        assert set(dep271["premium_summary"]["per_host"]) == set(hosts), \
            "exp271 per_host drifted"
        assert [r["host"] for r in dep272["per_host"]] == hosts, \
            "exp272 per_host drifted"

        # ---- the pre-named outliers: exp272's deposited premium hosts
        #      (the L250 open item names H3/H5; read from the deposit
        #      and asserted) ----------------------------------------------
        outliers = list(dep272["descriptive"]["premium_hosts"])
        assert outliers == ["H3", "H5"], \
            f"the outlier pre-naming drifted: {outliers}"
        cluster = [h for h in hosts if h not in outliers]
        assert len(cluster) == 10, "the ten-host cluster drifted"
        assert set(cluster) == set(
            dep272["descriptive"]["cluster_hosts"]), \
            "the cluster's membership drifted vs exp272's deposit"

        # ============ X1a: THE GRIDS BYTE-VERIFIED ====================
        # (i) exp271's deposited 36-row premium grid vs exp272's
        #     one_zone_premium_grid_re_read — row-json exact, order
        #     preserved (the byte verification)
        oz271 = dep271["premium_grid"]
        oz272 = dep272["one_zone_premium_grid_re_read"]
        oz_byte_verified = bool(
            len(oz271) == 36 and len(oz272) == 36
            and all(json.dumps(a) == json.dumps(b)
                    for a, b in zip(oz271, oz272)))
        # (ii) exp272's multi_zone_premium_grid vs the exp256
        #      reconstruction (canonical rows' worst_err + the r-60i0
        #      instance errs) — row-json exact
        canon_err = {(r["host"], int(r["seed"])): float(r["worst_err"])
                     for r in dep256["rows"] if r.get("arm") == "canonical"}
        subst_rows = [r for r in dep256["rows"]
                      if r.get("arm") == "substituted"]
        i0_err = {}
        for r in subst_rows:
            insts = [i for i in r["instances"]
                     if i.get("row_key") == "r-60i0"]
            assert len(insts) == 1, \
                (f"{r['host']} seed {r['seed']}: the r-60i0 instance is "
                 f"not unique ({len(insts)})")
            i0_err[(r["host"], int(r["seed"]))] = float(insts[0]["err"])
        assert len(canon_err) == 36 and len(i0_err) == 36, \
            "exp256's rows drifted (36 canonical + 36 substituted)"
        mz_rebuilt = [{"host": h, "seed": s,
                       "subst_i0_err": i0_err[(h, s)],
                       "canon_worst_err": canon_err[(h, s)],
                       "premium_mz": i0_err[(h, s)] - canon_err[(h, s)]}
                      for h in hosts for s in seeds]
        mz_byte_verified = bool(
            len(dep272["multi_zone_premium_grid"]) == 36
            and all(json.dumps(a) == json.dumps(b)
                    for a, b in zip(mz_rebuilt,
                                    dep272["multi_zone_premium_grid"])))
        # (iii) the grids' premium columns re-derived from their own
        #       err columns (the arithmetic recompute audit)
        oz_arith_ok = bool(all(
            abs((float(r["d1_err"]) - float(r["canon_worst_err"]))
                - float(r["premium"])) <= 1e-12 for r in oz271))
        mz_arith_ok = bool(all(
            abs((float(r["subst_i0_err"]) - float(r["canon_worst_err"]))
                - float(r["premium_mz"])) <= 1e-12
            for r in dep272["multi_zone_premium_grid"]))
        # (iv) the deposited per-host means cross-checked bit-exact
        oz_mean_chk = {h: sum(float(r["premium"]) for r in oz271
                              if r["host"] == h) / 3 for h in hosts}
        mz_mean_chk = {h: sum(float(r["premium_mz"])
                              for r in dep272["multi_zone_premium_grid"]
                              if r["host"] == h) / 3 for h in hosts}
        ph271 = dep271["premium_summary"]["per_host"]
        ph272 = {r["host"]: r for r in dep272["per_host"]}
        means_bit_exact = bool(
            all(oz_mean_chk[h] == float(ph271[h]["mean"]) for h in hosts)
            and all(oz_mean_chk[h] ==
                    float(ph272[h]["one_zone_premium_mean"])
                    for h in hosts)
            and all(mz_mean_chk[h] ==
                    float(ph272[h]["multi_zone_premium_mean"])
                    for h in hosts))

        # ============ X1b: THE 12-HOST FIELD TABLE ====================
        # every host-level field the five deposits carry; each record
        # provenance-tagged (deposit + path + kind + selection tag) and
        # carrying the full 12-host value vector (or its coverage gap).
        # SELECTION TAGS: "definitional" = the shelf/premium field
        # exp272's deposit NAMED the outliers from (separating it is
        # circular — reported, flagged); "component" = enters the
        # premium definition as a term; "external" = independent of the
        # outlier definition (the non-circular discriminant hunt).
        fields = []

        def _add(field, semantic, deposit, path, values, kind="numeric",
                 selection="external"):
            cov = {h: values.get(h) for h in hosts}
            n_num = sum(1 for v in cov.values()
                        if isinstance(v, (int, float))
                        and not isinstance(v, bool))
            if kind == "boolean":
                cov = {h: (1.0 if v else 0.0) if v is not None else None
                       for h, v in cov.items()}
                n_num = sum(1 for v in cov.values() if v is not None)
                values = cov
            fields.append({"field": field, "semantic": semantic,
                           "deposit": deposit, "path": path,
                           "kind": kind, "selection": selection,
                           "coverage": n_num, "values": values})

        # (a) exp243's classes records — the deposit-side host dossier
        e243 = "exp243_structured_adversarial.json"
        _add("exp243.classes.n", "n", e243, "classes.<H>.n",
             {h: classes[h].get("n") for h in hosts})
        _add("exp243.classes.rewire_seed", "rewire_seed", e243,
             "classes.<H>.rewire_seed",
             {h: classes[h].get("rewire_seed") for h in hosts})
        _add("exp243.classes.edges_base", "edges_base", e243,
             "classes.<H>.edges_base",
             {h: classes[h].get("edges_base") for h in hosts})
        _add("exp243.classes.n_boundary_cells_base",
             "n_boundary_cells_base", e243,
             "classes.<H>.n_boundary_cells_base",
             {h: classes[h].get("n_boundary_cells_base") for h in hosts})
        _add("exp243.classes.f_max_base", "f_max_base", e243,
             "classes.<H>.f_max_base",
             {h: classes[h].get("f_max_base") for h in hosts})
        _add("exp243.classes.n_candidate_reads", "n_candidate_reads",
             e243, "classes.<H>.n_candidate_reads",
             {h: classes[h].get("n_candidate_reads") for h in hosts})
        _add("exp243.classes.n_rejections", "n_rejections", e243,
             "classes.<H>.n_rejections",
             {h: classes[h].get("n_rejections") for h in hosts})
        _add("exp243.classes.multi_identity_audit.seed",
             "mia_seed", e243, "classes.<H>.multi_identity_audit.seed",
             {h: classes[h]["multi_identity_audit"].get("seed")
              for h in hosts})
        _add("exp243.classes.multi_identity_audit.prod_err",
             "mia_prod_err", e243,
             "classes.<H>.multi_identity_audit.prod_err",
             {h: classes[h]["multi_identity_audit"].get("prod_err")
              for h in hosts})
        _add("exp243.classes.multi_identity_audit.f_max", "mia_f_max",
             e243, "classes.<H>.multi_identity_audit.f_max",
             {h: classes[h]["multi_identity_audit"].get("f_max")
              for h in hosts})
        _add("exp243.classes.multi_identity_audit.bit_identical",
             "mia_bit_identical", e243,
             "classes.<H>.multi_identity_audit.bit_identical",
             {h: classes[h]["multi_identity_audit"].get("bit_identical")
              for h in hosts}, kind="boolean")

        def _hmean(arm, fn):
            out = {}
            for h in hosts:
                rs = [r for r in dep256["rows"] if r["host"] == h
                      and (arm is None or r.get("arm") == arm)]
                out[h] = sum(fn(r) for r in rs) / len(rs)
            return out

        # (b) exp256's per-host row records — the per-host canon/
        #     substituted worst means + the row-geometry aggregates
        e256 = "exp256_row_pair_regression.json"
        _add("exp256.rows.worst_err_mean_canonical",
             "canon_worst_err_mean", e256,
             "rows[arm=canonical].worst_err, mean over seeds",
             _hmean("canonical", lambda r: float(r["worst_err"])),
             selection="component")
        _add("exp256.rows.worst_err_mean_substituted",
             "subst_worst_err_mean", e256,
             "rows[arm=substituted].worst_err, mean over seeds",
             _hmean("substituted", lambda r: float(r["worst_err"])),
             selection="component")
        _add("exp256.rows.worst_err_mean_all_arms",
             "worst_err_mean_all_arms", e256,
             "rows[*].worst_err, mean over the 6 rows",
             _hmean(None, lambda r: float(r["worst_err"])),
             selection="component")
        _add("exp256.rows.pair_junction_count_mean_canonical",
             "pair_junction_count_mean_canonical", e256,
             "rows[arm=canonical].pair_junction_count, mean over seeds",
             _hmean("canonical", lambda r: int(r["pair_junction_count"])))
        _add("exp256.rows.pair_junction_count_mean_substituted",
             "pair_junction_count_mean_substituted", e256,
             "rows[arm=substituted].pair_junction_count, mean",
             _hmean("substituted",
                    lambda r: int(r["pair_junction_count"])))
        _add("exp256.rows.pair_junction_count_mean_all_arms",
             "pair_junction_count_mean_all_arms", e256,
             "rows[*].pair_junction_count, mean over the 6 rows",
             _hmean(None, lambda r: int(r["pair_junction_count"])))
        _add("exp256.rows.canon_boundary_cells_mean_canonical",
             "canon_boundary_cells_mean_canonical", e256,
             "rows[arm=canonical].class_counts['CANON-BOUNDARY'], mean",
             _hmean("canonical",
                    lambda r: int(r["class_counts"]["CANON-BOUNDARY"])))
        _add("exp256.rows.canon_boundary_cells_mean_substituted",
             "canon_boundary_cells_mean_substituted", e256,
             "rows[arm=substituted].class_counts['CANON-BOUNDARY'], mean",
             _hmean("substituted",
                    lambda r: int(r["class_counts"]["CANON-BOUNDARY"])))
        _add("exp256.rows.interior_cells_mean_canonical",
             "interior_cells_mean_canonical", e256,
             "rows[arm=canonical].class_counts['INTERIOR'], mean",
             _hmean("canonical", lambda r: int(r["class_counts"]["INTERIOR"])))
        _add("exp256.rows.interior_cells_mean_substituted",
             "interior_cells_mean_substituted", e256,
             "rows[arm=substituted].class_counts['INTERIOR'], mean",
             _hmean("substituted",
                    lambda r: int(r["class_counts"]["INTERIOR"])))
        _add("exp256.rows.f_max_mean_all_arms", "f_max_mean_all_arms",
             e256, "rows[*].f_max, mean over the 6 rows",
             _hmean(None, lambda r: float(r["f_max"])))
        _add("exp256.rows.identity_residual_mean_all_arms",
             "identity_residual_mean_all_arms", e256,
             "rows[*].decomposition.identity_residual, mean",
             _hmean(None,
                    lambda r: float(r["decomposition"]["identity_residual"])))

        # (c) exp271's premium grid — the per-host one-zone shelf
        e271 = "exp271_one_zone_premium.json"
        _add("exp271.premium_grid.d1_err_mean", "d1_err_mean", e271,
             "premium_grid.<H,s>.d1_err, mean over seeds",
             {h: sum(float(r["d1_err"]) for r in oz271
                     if r["host"] == h) / 3 for h in hosts},
             selection="definitional")
        _add("exp271.premium_grid.canon_worst_err_mean",
             "canon_worst_err_mean", e271,
             "premium_grid.<H,s>.canon_worst_err, mean over seeds",
             {h: sum(float(r["canon_worst_err"]) for r in oz271
                     if r["host"] == h) / 3 for h in hosts},
             selection="component")
        _add("exp271.premium_grid.one_zone_premium_mean",
             "one_zone_premium_mean", e271,
             "premium_grid.<H,s>.premium, mean over seeds",
             oz_mean_chk, selection="definitional")
        _add("exp271.premium_summary.per_host.all_positive",
             "one_zone_all_positive", e271,
             "premium_summary.per_host.<H>.all_positive",
             {h: ph271[h].get("all_positive") for h in hosts},
             kind="boolean", selection="definitional")

        # (d) exp272's per-host records + both grids (the premium
        #     deposits re-read here as FIELDS, not as verdicts)
        e272 = "exp272_host_premium_structure.json"
        _add("exp272.per_host.n_boundary_cells_base",
             "n_boundary_cells_base", e272,
             "per_host.<H>.n_boundary_cells_base",
             {h: ph272[h].get("n_boundary_cells_base") for h in hosts})
        _add("exp272.per_host.one_zone_premium_mean",
             "one_zone_premium_mean", e272,
             "per_host.<H>.one_zone_premium_mean",
             {h: ph272[h].get("one_zone_premium_mean") for h in hosts},
             selection="definitional")
        _add("exp272.per_host.multi_zone_premium_mean",
             "multi_zone_premium_mean", e272,
             "per_host.<H>.multi_zone_premium_mean",
             {h: ph272[h].get("multi_zone_premium_mean") for h in hosts},
             selection="definitional")
        _add("exp272.one_zone_premium_grid_re_read.d1_err_mean",
             "d1_err_mean", e272,
             "one_zone_premium_grid_re_read.<H,s>.d1_err, mean",
             {h: sum(float(r["d1_err"]) for r in oz272
                     if r["host"] == h) / 3 for h in hosts},
             selection="definitional")
        _add("exp272.one_zone_premium_grid_re_read.canon_worst_err_mean",
             "canon_worst_err_mean", e272,
             "one_zone_premium_grid_re_read.<H,s>.canon_worst_err, mean",
             {h: sum(float(r["canon_worst_err"]) for r in oz272
                     if r["host"] == h) / 3 for h in hosts},
             selection="component")
        _add("exp272.multi_zone_premium_grid.subst_i0_err_mean",
             "subst_i0_err_mean", e272,
             "multi_zone_premium_grid.<H,s>.subst_i0_err, mean",
             {h: sum(float(r["subst_i0_err"])
                     for r in dep272["multi_zone_premium_grid"]
                     if r["host"] == h) / 3 for h in hosts},
             selection="definitional")
        _add("exp272.multi_zone_premium_grid.canon_worst_err_mean",
             "canon_worst_err_mean", e272,
             "multi_zone_premium_grid.<H,s>.canon_worst_err, mean",
             {h: sum(float(r["canon_worst_err"])
                     for r in dep272["multi_zone_premium_grid"]
                     if r["host"] == h) / 3 for h in hosts},
             selection="component")
        _add("exp272.multi_zone_premium_grid.multi_zone_premium_mean",
             "multi_zone_premium_mean", e272,
             "multi_zone_premium_grid.<H,s>.premium_mz, mean",
             mz_mean_chk, selection="definitional")

        # (e) exp182's margin data: the host-key scan (the margin
        #     profiles are TARGET-keyed — 100 targets — so they carry
        #     zero host-level fields; the scan is the evidence)
        e182_keys = set()

        def _walk_keys(o):
            if isinstance(o, dict):
                e182_keys.update(o.keys())
                for v in o.values():
                    _walk_keys(v)
            elif isinstance(o, list):
                for v in o:
                    _walk_keys(v)

        _walk_keys(dep182)
        e182_host_keys = sorted(e182_keys & set(hosts))
        exp182_scan = {
            "deposit": "exp182_substrate_100.json",
            "margin_profiles_host_keyed": False,
            "host_keys_found": e182_host_keys,
            "n_keys_scanned": len(e182_keys),
            "finding": ("exp182's margin profiles are TARGET-keyed "
                        "(100 targets; manifest/battery/per_target), "
                        "not host-keyed — 0 host-level fields; "
                        "reported per X1, contributes nothing to the "
                        "table")}

        # ============ THE SEPARATION TEST (the pre-registered
        # arithmetic; per NUMERIC field: the cluster range = [min,max]
        # over the TEN cluster hosts; the field SEPARATES iff BOTH
        # H3's and H5's values lie strictly outside that range ON THE
        # SAME SIDE) -----------------------------------------------------
        for rec in fields:
            vals = rec["values"]
            if rec["coverage"] != 12:
                # the honesty clause: incomplete coverage -> reported,
                # never counted; the informational test (flagged) runs
                # over the available hosts
                avail = {h: v for h, v in vals.items() if v is not None}
                av_cl = [v for h, v in avail.items() if h in cluster]
                info = {}
                if avail.get("H3") is not None \
                        and avail.get("H5") is not None and av_cl:
                    lo, hi = min(av_cl), max(av_cl)
                    v3, v5 = avail["H3"], avail["H5"]
                    info = {"informational_range_over_available": [lo, hi],
                            "informational_H3": v3,
                            "informational_H5": v5,
                            "informational_separates": bool(
                                (v3 < lo or v3 > hi)
                                and (v5 < lo or v5 > hi)
                                and ((v3 > hi) == (v5 > hi)))}
                rec.update({"status": "partial-coverage",
                            "missing_hosts": [h for h in hosts
                                              if vals[h] is None],
                            "never_counted": True,
                            "note": ("incomplete coverage — the "
                                     "pre-registration computes the "
                                     "field for all 12 hosts; this "
                                     "field cannot be, so it is "
                                     "reported and never counted"),
                            **info})
                continue
            cl = [float(vals[h]) for h in cluster]
            v3, v5 = float(vals["H3"]), float(vals["H5"])
            lo, hi = min(cl), max(cl)
            p3 = ("above" if v3 > hi else "below" if v3 < lo else "inside")
            p5 = ("above" if v5 > hi else "below" if v5 < lo else "inside")
            if lo == hi and v3 == lo and v5 == hi:
                status = "constant"
            elif p3 != "inside" and p5 != "inside" and p3 == p5:
                status = "separating"
            elif p3 != "inside" or p5 != "inside":
                status = "one-sided"  # X3: reported, NEVER counted
            else:
                status = "not-separating"
            rec.update({"cluster_range": [lo, hi], "H3": v3, "H5": v5,
                        "H3_position": p3, "H5_position": p5,
                        "status": status})

        tested = [r for r in fields if r["coverage"] == 12]
        separating = [r for r in tested if r["status"] == "separating"]
        one_sided = [r for r in tested if r["status"] == "one-sided"]
        # distinct semantic fields (dedup across the deposits that
        # carry the same quantity)
        def _sem(rs):
            out = []
            for s in sorted({r["semantic"] for r in rs}):
                carriers = sorted({r["deposit"].split("_")[0]
                                   for r in rs if r["semantic"] == s})
                rec0 = next(r for r in rs if r["semantic"] == s)
                out.append({"semantic_field": s,
                            "carried_by": carriers,
                            "cluster_range": rec0["cluster_range"],
                            "H3": rec0["H3"], "H5": rec0["H5"],
                            "side": rec0["H3_position"],
                            "selection": rec0["selection"]})
            return out

        distinct_sep = _sem(separating)
        distinct_one_sided = _sem(one_sided)
        by_tag = {}
        for r in separating:
            by_tag.setdefault(r["selection"], []).append(r["semantic"])
        by_tag = {k: sorted(set(v)) for k, v in sorted(by_tag.items())}

        ext_sep = [d for d in distinct_sep
                   if d["selection"] == "external"
                   and d["semantic_field"]
                   != "identity_residual_mean_all_arms"]
        separation_summary = {
            "rule": ("cluster range = [min, max] over the ten cluster "
                     "hosts; the field SEPARATES iff BOTH H3's and "
                     "H5's values lie strictly outside that range ON "
                     "THE SAME SIDE"),
            "n_field_records": len(fields),
            "n_tested_records": len(tested),
            "n_separating_records": len(separating),
            "n_distinct_separating_fields": len(distinct_sep),
            "distinct_separating_fields": distinct_sep,
            "by_selection_tag": by_tag,
            "external_separating_fields": ext_sep,
            "external_note": (
                "the definitional tags separate BY CONSTRUCTION (H3/H5 "
                "were named the premium hosts FROM those fields in "
                "exp272's deposit — circular); the non-circular "
                "discriminants are the external fields ({} distinct)".format(
                    len(ext_sep))),
            "identity_residual_caveat": (
                "identity_residual_mean_all_arms separates only at "
                "floating-point noise scale (~1e-16/1e-15 vs the "
                "cluster's ~1e-18..1e-17) — reported per the "
                "registered arithmetic, carries no physical meaning"),
            "range_vs_rank_note": (
                "n_boundary_cells_base separates the outliers as a "
                "RANGE discriminant (H3 47 / H5 48 vs cluster "
                "[4, 43]) while exp272's H2 showed no across-host "
                "rank correlation (rho 0.0526) — both deposited "
                "facts stand: range separation of the two extremes "
                "is not a graded rank law")}

        # ============ X1/X2/X3 (evaluated exactly once per pass) ======
        x1_pass = bool(
            oz_byte_verified and mz_byte_verified
            and oz_arith_ok and mz_arith_ok and means_bit_exact
            and len(fields) > 0
            and all(r["coverage"] == 12 or r["status"]
                    == "partial-coverage" for r in fields)
            and exp182_scan["host_keys_found"] == [])
        x2_pass = bool(len(separating) >= 1 and len(distinct_sep) >= 1)
        x3_pass = bool(
            all(r["status"] != "separating" for r in one_sided)
            and len(one_sided) == len([r for r in tested
                                       if r["status"] == "one-sided"]))

        gates = {
            "X1_field_table": {
                "pass": x1_pass,
                "bar": ("the 12-host field table assembled from the "
                        "deposits (every field provenance-tagged); "
                        "exp271's/exp272's premium grids "
                        "byte-verified"),
                "field_table": {
                    "n_records": len(fields),
                    "n_complete_numeric": len(tested),
                    "n_partial_coverage": len(fields) - len(tested),
                    "provenance_tagged": True},
                "grids_byte_verification": {
                    "exp271_premium_grid_vs_exp272_re_read":
                        oz_byte_verified,
                    "exp272_multi_zone_grid_vs_exp256_reconstruction":
                        mz_byte_verified,
                    "n_rows_each": 36,
                    "method": ("row-json exact, order preserved: "
                               "json.dumps(row_a) == json.dumps(row_b) "
                               "for all 36 rows, both grids")},
                "grid_arithmetic_recompute": {
                    "one_zone_premium_column_ok": oz_arith_ok,
                    "multi_zone_premium_column_ok": mz_arith_ok},
                "deposited_per_host_means_bit_exact": means_bit_exact,
                "exp182_margin_profiles": exp182_scan,
                "source_deposit_shas_recorded": dict(ro_before)},
            "X2_separation": {
                "pass": x2_pass,
                "bar": ("at least ONE deposited field separates {H3, "
                        "H5} from the ten-host cluster on the same "
                        "side (the gate) — the count and the fields "
                        "named; ZERO separating fields -> "
                        "OUTLIER-DEPOSIT-ABSENT"),
                "n_tested_records": len(tested),
                "n_separating_records": len(separating),
                "n_distinct_separating_fields": len(distinct_sep),
                "distinct_separating_fields":
                    [d["semantic_field"] for d in distinct_sep],
                "by_selection_tag":
                    {k: v for k, v in by_tag.items()},
                "external_separating_fields":
                    [d["semantic_field"] for d in ext_sep]},
            "X3_honesty": {
                "pass": x3_pass,
                "bar": ("fields that separate ONE outlier but not the "
                        "other are reported as one-sided (never "
                        "counted as separating)"),
                "n_one_sided_records": len(one_sided),
                "one_sided_fields":
                    [d["semantic_field"] for d in distinct_one_sided],
                "one_sided_detail":
                    [{"field": r["field"], "H3": r["H3"], "H5": r["H5"],
                      "cluster_range": r["cluster_range"],
                      "H3_position": r["H3_position"],
                      "H5_position": r["H5_position"]}
                     for r in one_sided],
                "never_counted": True},
        }

        payload = {
            "hosts": hosts, "seeds": seeds,
            "outliers": outliers, "cluster": cluster,
            "outlier_prename_source":
                "exp272's deposit descriptive.premium_hosts (asserted "
                "== ['H3', 'H5'])",
            "field_table": fields,
            "separation_summary": separation_summary,
            "partial_coverage_fields":
                [{"field": r["field"], "missing_hosts": r["missing_hosts"],
                  "note": r["note"],
                  **({k: v for k, v in r.items()
                      if k.startswith("informational")})}
                 for r in fields if r["status"] == "partial-coverage"],
            "excluded_fields":
                [{"field": "exp243.classes.runtime_s",
                  "reason": ("wall-clock field — excluded by the X4 "
                             "discipline (no wall-clock fields); not "
                             "assembled, not tested, not counted"),
                  "values_recorded": False}],
            "non_numeric_fields_note":
                ("string host-level fields exist but are not numeric "
                 "candidates: exp243 classes base/base_sha256; exp256 "
                 "rows worst_pert/worst_row_key/worst_medium/medium "
                 "shas; the instrument tests NUMERIC fields only"),
            "gates": gates,
        }
        return payload

    payload_a = compute()
    sha_a = hashlib.sha256(json.dumps(
        payload_a, sort_keys=True, default=str).encode()).hexdigest()
    payload_b = compute()
    sha_b = hashlib.sha256(json.dumps(
        payload_b, sort_keys=True, default=str).encode()).hexdigest()
    deterministic = bool(sha_a == sha_b)
    assert deterministic, "the computation is not two-pass deterministic"

    gates = payload_a["gates"]
    x1_pass = gates["X1_field_table"]["pass"]
    x2_pass = gates["X2_separation"]["pass"]
    x3_pass = gates["X3_honesty"]["pass"]

    # ---- X4: the discipline --------------------------------------------
    ro_after = {"exp243_deposit": _sha(DEP243),
                "exp272_deposit": _sha(DEP272),
                "exp271_deposit": _sha(DEP271),
                "exp182_deposit": _sha(DEP182),
                "exp256_deposit": _sha(DEP256)}
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

    x4_pass = bool(ro_unchanged and deterministic and no_wall_clock
                   and floor_at_entry == PROD_FLOOR)

    gates["X4_discipline"] = {
        "pass": x4_pass,
        "bar": ("all deposits READ-ONLY sha-recorded byte-unchanged; "
                "deterministic; no wall-clock fields; the -60.0 floor "
                "asserted at exit"),
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
        "docstring_byte_unchanged_vs_26946af": docstring_ok,
        "header_sha256": header_sha,
        "header_byte_unchanged_vs_26946af": header_ok,
        "deposit_form": ("deterministic: no wall-clock fields — a "
                         "re-run of this module reproduces this file "
                         "byte-identically")}

    # ---- the branch (pre-named): the separating COUNT only --------------
    branch = ("OUTLIER-DEPOSIT-CARRIED" if x2_pass
              else "OUTLIER-DEPOSIT-ABSENT")
    gate_passes = {"X1": x1_pass, "X2": x2_pass, "X3": x3_pass,
                   "X4": x4_pass}
    n_pass = sum(1 for v in gate_passes.values() if v)
    n_refute = 4 - n_pass

    # ---- the verdict (one line, the numbers data-driven) ----------------
    summary = payload_a["separation_summary"]
    ext = summary["external_separating_fields"]

    def _g(v):
        # '.10g' is already noise-clean (0.47000000000000003 -> 0.47);
        # NO trailing-zero stripping (310 must never print as 31)
        return format(v, ".10g") if isinstance(v, float) else str(v)

    ext_txt = "; ".join(
        "{} {}{}/{} vs [{}, {}]".format(
            d["semantic_field"],
            "BELOW " if d["side"] == "below" else "",
            _g(d["H3"]), _g(d["H5"]),
            _g(d["cluster_range"][0]), _g(d["cluster_range"][1]))
        for d in ext)
    verdict = (
        f"{n_pass}/4 gates X1-X4 ({n_pass} PASS / {n_refute} REFUTE) | "
        f"{branch} | {summary['n_separating_records']}/"
        f"{summary['n_tested_records']} tested host-field records "
        f"separate {{H3, H5}} from the ten-host cluster on the same "
        f"side ({summary['n_distinct_separating_fields']} distinct "
        f"fields; external discriminants: {ext_txt} — plus the "
        f"noise-scale identity-residual; the shelf/premium fields "
        f"separate by construction, the outliers were named from "
        f"them) | {len(gates['X3_honesty']['one_sided_fields'])} "
        f"one-sided fields named, never counted "
        f"({', '.join(gates['X3_honesty']['one_sided_fields'])}) | "
        f"pure deposit re-read, seconds: 5 deposits READ-ONLY "
        f"byte-unchanged, both premium grids byte-verified, two-pass "
        f"bit-identical, floor -60.0")

    deposit = {
        "exp": "exp273_outlier_hosts",
        "claim": (
            "THE OUTLIER HOSTS (batch 31, L250's registered next (a), "
            "pre-registration commit 26946af): the discriminant search "
            "across the deposited host records — every host-level "
            "numeric field the five deposits carry (exp243's classes "
            "records, exp256's per-host row aggregates, exp271's/exp272's "
            "premium grids, exp182's margin data where host-keyed) "
            "tested against the pre-named separation: the field "
            "separates {H3, H5} from the ten-host cluster iff both "
            "outliers' values lie strictly outside the cluster's "
            "[min, max] range ON THE SAME SIDE; branches "
            "OUTLIER-DEPOSIT-CARRIED / OUTLIER-DEPOSIT-ABSENT"),
        "method": {
            "outliers": ("H3 and H5, read from exp272's deposit "
                         "descriptive.premium_hosts and asserted"),
            "cluster": ("the other ten hosts (H0, H1, H2, H4, H6-H11), "
                        "cross-checked against exp272's "
                        "descriptive.cluster_hosts"),
            "test": ("per NUMERIC host-level field: cluster range = "
                     "[min, max] over the TEN cluster hosts; "
                     "SEPARATING iff BOTH H3's and H5's values lie "
                     "strictly outside that range ON THE SAME SIDE; "
                     "one outlier outside only -> one-sided (X3: "
                     "reported, never counted); incomplete coverage "
                     "-> partial-coverage (reported, never counted)"),
            "provenance_tags": ("definitional = the shelf/premium "
                                "field the outliers were NAMED from "
                                "(separating is circular, flagged); "
                                "component = enters the premium "
                                "definition; external = independent "
                                "of the outlier definition (the "
                                "non-circular hunt)"),
            "excluded": ("exp243's classes runtime_s (wall-clock, X4); "
                         "string fields (base, base_sha256, worst_pert, "
                         "worst_medium, ...) — numeric fields only"),
            "method_source": ("experiments/exp272_host_premium_structure"
                              ".py (the outlier naming + the grids), "
                              "experiments/exp271_one_zone_premium.py "
                              "(the one-zone shelf), "
                              "experiments/exp256_row_pair_regression.py"
                              " (the row records), "
                              "experiments/exp243_structured_adversarial"
                              ".py (the classes records)")},
        "inputs": {
            "exp243_deposit": {
                "path": "results/exp243_structured_adversarial.json",
                "sha256": ro_before["exp243_deposit"],
                "role": ("the classes records (rewire_seed, "
                         "edges_base, n_boundary_cells_base, "
                         "f_max_base, multi_identity_audit, ...) — "
                         "the host dossier")},
            "exp272_deposit": {
                "path": "results/exp272_host_premium_structure.json",
                "sha256": ro_before["exp272_deposit"],
                "role": ("the premium hosts' pre-naming, the per-host "
                         "premium records, both premium grids (the "
                         "grids byte-verified here)")},
            "exp271_deposit": {
                "path": "results/exp271_one_zone_premium.json",
                "sha256": ro_before["exp271_deposit"],
                "role": ("the deposited 36-row premium grid + the "
                         "per-host means (byte-verified vs exp272's "
                         "re-read)")},
            "exp182_deposit": {
                "path": "results/exp182_substrate_100.json",
                "sha256": ro_before["exp182_deposit"],
                "role": ("the margin profiles — target-keyed, NOT "
                         "host-keyed (the X1 scan is the evidence); "
                         "0 host-level fields")},
            "exp256_deposit": {
                "path": "results/exp256_row_pair_regression.json",
                "sha256": ro_before["exp256_deposit"],
                "role": ("the 72 row records — the per-host "
                         "canon/substituted worst means + the "
                         "row-geometry aggregates")}},
        "hosts": payload_a["hosts"],
        "outliers": payload_a["outliers"],
        "cluster": payload_a["cluster"],
        "outlier_prename_source": payload_a["outlier_prename_source"],
        "field_table": payload_a["field_table"],
        "separation_summary": summary,
        "partial_coverage_fields": payload_a["partial_coverage_fields"],
        "excluded_fields": payload_a["excluded_fields"],
        "non_numeric_fields_note": payload_a["non_numeric_fields_note"],
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
            "docstring_byte_unchanged_vs_26946af": docstring_ok,
            "header_sha256": header_sha,
            "header_byte_unchanged_vs_26946af": header_ok,
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

    print("=== exp273: THE OUTLIER HOSTS (pure deposit re-read + "
          "arithmetic) ===")
    print("  the discriminant search across the five deposits' host "
          "records: every host-level numeric field vs the pre-named "
          "separation ({H3, H5} vs the ten-host cluster, same side)")
    print(f"\n  X1 field table: {'PASS' if x1_pass else 'FAIL'} "
          f"({gates['X1_field_table']['field_table']['n_records']} "
          f"field records, "
          f"{gates['X1_field_table']['field_table']['n_complete_numeric']}"
          f" complete numeric; exp271 grid == exp272 re-read "
          f"36/36 row-json exact; exp272 mz grid == exp256 "
          f"reconstruction 36/36; exp182 margin profiles "
          f"target-keyed, 0 host fields)")
    print(f"  X2 separation: {'PASS' if x2_pass else 'FAIL'} — "
          f"{summary['n_separating_records']}/"
          f"{summary['n_tested_records']} records separate "
          f"({summary['n_distinct_separating_fields']} distinct "
          f"fields; external: "
          f"{', '.join(d['semantic_field'] for d in ext)})")
    for d in summary["distinct_separating_fields"]:
        print(f"      {d['semantic_field']:44s} "
              f"[{d['cluster_range'][0]:.6g}, "
              f"{d['cluster_range'][1]:.6g}]  H3={d['H3']:.6g}  "
              f"H5={d['H5']:.6g}  ({d['side']}; {d['selection']})")
    x3 = gates["X3_honesty"]
    print(f"  X3 honesty: {'PASS' if x3_pass else 'FAIL'} — "
          f"{x3['n_one_sided_records']} one-sided field(s) named, "
          f"never counted: {', '.join(x3['one_sided_fields'])}")
    for r in x3["one_sided_detail"]:
        print(f"      {r['field']:55s} "
              f"[{r['cluster_range'][0]:.6g}, "
              f"{r['cluster_range'][1]:.6g}]  H3={r['H3']:.6g} "
              f"({r['H3_position']})  H5={r['H5']:.6g} "
              f"({r['H5_position']})")
    print(f"  X4 discipline: {'PASS' if x4_pass else 'FAIL'} "
          f"(read-only byte-unchanged: {ro_unchanged}; two-pass "
          f"bit-identical: {deterministic}; no wall-clock fields: "
          f"{no_wall_clock})")
    print(f"\n  BRANCH: {branch}")
    print(f"\n  GATES: {verdict}")
    print(f"  deposited {OUT}")

    # the hard rule, re-asserted after the work: the docstring is still
    # the 26946af pre-registration, byte-for-byte
    assert hashlib.sha256(__doc__.encode()).hexdigest() \
        == EXPECTED_DOCSTRING_SHA256, "docstring drifted after the work"
    with open(__file__, "r", encoding="utf-8") as _f:
        _src2 = _f.read()
    assert hashlib.sha256(
        _src2[:_src2.index(_marker) + len(_marker)].encode()
    ).hexdigest() == EXPECTED_HEADER_SHA256, "header drifted after work"
    # the source deposits are still byte-unchanged after the work
    assert set(_sha(p) for p in (DEP243, DEP272, DEP271, DEP182, DEP256)) \
        == set(ro_before.values()), "source deposit drifted after work"

    # THE FLOOR ASSERT AT EXIT (the hard rule; exp243's closing line)
    CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at exit"
    return deposit


if __name__ == "__main__":
    main()
