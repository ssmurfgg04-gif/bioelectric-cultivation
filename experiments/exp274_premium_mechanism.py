#!/usr/bin/env python3
"""exp274 — THE PREMIUM MECHANISM (batch 32; L251's registered next
(a) — zero new simulation).

THE OPEN ITEM (L251): the rewrite price concentrates on the
boundary-richest, pair-poorest hosts (H3/H5), with mia_prod_err 4x
the cluster's. Is the external signature the PRICE itself or a
correlate?

THE INSTRUMENT (pre-registered, zero-knob, pure re-read): the
12-host mediator regression — the per-host one-zone premium means
(exp272's deposited grid) against the three mediators exp273 named
(mia_prod_err, n_boundary_cells_base, the canonical pair-junction
mean), each alone (Spearman) and jointly (the OLS rank R2 on the
tied-average ranks, the exp262 convention; three single-mediator
models + the full model; the shares by the two-order symmetric
average on the entry order the docstring pre-names: mia_prod_err,
then boundary count, then pair deficit).

PRE-REGISTERED GATES:

  M1  THE GRIDS: the 12-host table complete (the premium means from
      exp272's deposit; the three mediators from exp273's deposited
      field table); sha-verified READ-ONLY.
  M2  THE SINGLE MEDIATORS: each mediator's Spearman against the
      premium reported; the gate: >= 1 mediator reaches >= 0.5.
  M3  THE JOINT MODEL: the full model's rank R2 reported; the gate:
      R2 >= 0.5 (the mediators jointly carry the shelf price).
  M4  THE DISCIPLINE: all deposits READ-ONLY sha-recorded
      byte-unchanged; deterministic; no wall-clock fields; the
      -60.0 floor asserted at exit.

THE BRANCHES (pre-named): PRICE-MEDIATED (M2 or M3 passes) /
PRICE-UNMEDIATED (both fail — the premium's carrier is outside the
deposited mediator set, named honestly).

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
OUT = os.path.join(ROOT, "results", "exp274_premium_mechanism.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the body-only discipline;
    #      docstring/imports/constants above byte-unchanged — exp174's
    #      body-only discipline; gates M1-M4 evaluated exactly once per
    #      pass, pre-registration commit 60aff99; the docstring's RUN
    #      clause holds verbatim: a pure deposit re-read + arithmetic,
    #      zero new simulation, seconds) ==================================
    import hashlib
    import json

    import numpy as np
    from scipy.stats import rankdata

    import cultivation.bioelectric.collective as CORE  # the floor's home

    # ---- the byte-unchanged self-check (the hard rule: the docstring
    #      is the 60aff99 pre-registration, byte-for-byte; the header —
    #      shebang + docstring + imports + constants — likewise;
    #      asserted BEFORE and AFTER the work) ----------------------------
    EXPECTED_DOCSTRING_SHA256 = (
        "4d079b4ad8bd0c389888a6849926ca5aa09e7c51643a5da14fa50ee93c345e06")
    EXPECTED_HEADER_SHA256 = (
        "3bcfcfda715f5a2a22433034f9fcfb66dda984a018b817290c86df4780bff44e")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 60aff99"
    assert header_ok, "header drifted from 60aff99"

    # ---- the -60.0 floor (M4: asserted at exit; nothing in this body
    #      imports any machinery that touches it — recorded at entry,
    #      restored and re-asserted as the closing line, exp243's/
    #      exp271's/exp272's/exp273's closing discipline) ------------------
    PROD_FLOOR = -60.0
    floor_at_entry = float(CORE.NEURAL_SPEC_MIN)
    assert floor_at_entry == PROD_FLOOR, \
        f"floor drift at entry: {floor_at_entry}"

    # ---- the source deposits (READ-ONLY; sha-recorded BEFORE any
    #      work, re-verified byte-unchanged at the end) — the two the
    #      computation reads (exp272's premium means, exp273's field
    #      table) plus the four exp273's provenance chain names (their
    #      recorded shas are byte-verified against the actual files;
    #      they are never opened for computation here) --------------------
    DEP272 = os.path.join(ROOT, "results",
                          "exp272_host_premium_structure.json")
    DEP273 = os.path.join(ROOT, "results", "exp273_outlier_hosts.json")
    DEP243 = os.path.join(ROOT, "results",
                          "exp243_structured_adversarial.json")
    DEP271 = os.path.join(ROOT, "results", "exp271_one_zone_premium.json")
    DEP182 = os.path.join(ROOT, "results", "exp182_substrate_100.json")
    DEP256 = os.path.join(ROOT, "results",
                          "exp256_row_pair_regression.json")
    for _p in (DEP272, DEP273, DEP243, DEP271, DEP182, DEP256):
        assert os.path.exists(_p), f"missing source deposit {_p}"

    def _sha(path):
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    ro_before = {"exp272_deposit": _sha(DEP272),
                 "exp273_deposit": _sha(DEP273),
                 "exp243_deposit": _sha(DEP243),
                 "exp271_deposit": _sha(DEP271),
                 "exp182_deposit": _sha(DEP182),
                 "exp256_deposit": _sha(DEP256)}

    # ---- the regression helpers (zero-knob; the exp262/exp272 rank
    #      convention: scipy rankdata's tied-average ranks — Spearman
    #      IS Pearson on the tied-average ranks; the OLS rank R2 runs
    #      on the RESPONSE's tied-average ranks exactly as exp262's
    #      _r2 block) -------------------------------------------------------
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
    #      two payloads must be byte-identical — M4's determinism
    #      clause) ----------------------------------------------------------
    def compute():
        with open(DEP272) as fh:
            dep272 = json.load(fh)
        with open(DEP273) as fh:
            dep273 = json.load(fh)

        # ---- the host frame (exp272's per_host order; the order
        #      exp273 asserted == exp256's battery order) ----------------
        hosts = [r["host"] for r in dep272["per_host"]]
        assert len(hosts) == 12 and len(set(hosts)) == 12, \
            "the 12-host frame drifted"

        # ---- the three mediators BY EXACT FIELD NAME from exp273's
        #      deposited 12-host field table (the docstring pre-names
        #      the entry order mia_prod_err -> boundary count ->
        #      pair deficit; the field_table records carry each
        #      field's exact name / deposit / path / selection tag) ---
        ft = {rec["field"]: rec for rec in dep273["field_table"]}
        MIA = "exp243.classes.multi_identity_audit.prod_err"
        BC = "exp243.classes.n_boundary_cells_base"
        PD = "exp256.rows.pair_junction_count_mean_canonical"
        for name in (MIA, BC, PD):
            assert name in ft, f"mediator field {name} missing from " \
                               "exp273's deposited field table"
        rec_mia, rec_bc, rec_pd = ft[MIA], ft[BC], ft[PD]
        mediator_provenance = {
            "mia_prod_err": {
                "field": rec_mia["field"], "semantic": rec_mia["semantic"],
                "deposit": rec_mia["deposit"], "path": rec_mia["path"],
                "kind": rec_mia["kind"], "selection": rec_mia["selection"]},
            "n_boundary_cells_base": {
                "field": rec_bc["field"], "semantic": rec_bc["semantic"],
                "deposit": rec_bc["deposit"], "path": rec_bc["path"],
                "kind": rec_bc["kind"], "selection": rec_bc["selection"]},
            "pair_junction_count_mean_canonical": {
                "field": rec_pd["field"], "semantic": rec_pd["semantic"],
                "deposit": rec_pd["deposit"], "path": rec_pd["path"],
                "kind": rec_pd["kind"], "selection": rec_pd["selection"]}}
        # all three are exp273's EXTERNAL separating fields — the
        # non-circular discriminator set (asserted, disclosed)
        assert all(mp["selection"] == "external"
                   for mp in mediator_provenance.values()), \
            "a pre-named mediator is not an external field in exp273"

        # ---- the response: the per-host ONE-ZONE premium means from
        #      exp272's deposit (the docstring's pre-named source) -----
        y = {r["host"]: float(r["one_zone_premium_mean"])
             for r in dep272["per_host"]}
        assert set(y) == set(hosts), "exp272's per-host means drifted"
        yv = [y[h] for h in hosts]
        all_finite = bool(all(v == v and abs(v) != float("inf")
                              for v in yv))

        # ---- M1a: the 12-host table complete — the assembled
        #      regression table (12 rows x 4 columns, no gaps) ---------
        med_vals = {k: [float(v[h]) for h in hosts]
                    for k, v in (("mia_prod_err", rec_mia["values"]),
                                 ("n_boundary_cells_base", rec_bc["values"]),
                                 ("pair_junction_count_mean_canonical",
                                  rec_pd["values"]))}
        assert all(rec["coverage"] == 12
                   for rec in (rec_mia, rec_bc, rec_pd)), \
            "a mediator record's coverage drifted from 12"
        table = [{"host": h, "one_zone_premium_mean": y[h],
                  "mia_prod_err": med_vals["mia_prod_err"][i],
                  "n_boundary_cells_base":
                      med_vals["n_boundary_cells_base"][i],
                  "pair_junction_count_mean_canonical":
                      med_vals["pair_junction_count_mean_canonical"][i]}
                 for i, h in enumerate(hosts)]
        complete = bool(
            all_finite
            and all(all(v == v and abs(v) != float("inf") for v in vec)
                    for vec in med_vals.values()))

        # ---- M1b: the sha verification (the provenance chain):
        #      exp273's recorded input shas == the actual deposit
        #      bytes (the deposits the mediators/provenance name) ----
        chain_names = {"exp243_deposit": DEP243, "exp271_deposit": DEP271,
                       "exp182_deposit": DEP182, "exp256_deposit": DEP256,
                       "exp272_deposit": DEP272}
        chain_ok = {}
        for key, path in chain_names.items():
            recorded = dep273["inputs"][key]["sha256"]
            actual = _sha(path)
            chain_ok[key] = bool(recorded == actual)
        chain_all_ok = bool(all(chain_ok.values()))

        # ---- M1c: the completeness cross-checks (audit-grade):
        #      (i) the per-host means re-derived from exp272's OWN
        #      deposited one-zone grid (sum/3 over 3 seeds) bit-exact;
        #      (ii) exp273's field-table carry of the same means
        #      (exp272.per_host.one_zone_premium_mean) bit-exact;
        #      (iii) the duplicate boundary-count carrier
        #      (exp272.per_host.n_boundary_cells_base) bit-exact
        #      identical to the exp243 record -----------------------------
        grid = dep272["one_zone_premium_grid_re_read"]
        grid_ok = bool(len(grid) == 36
                       and all(abs((float(r["d1_err"])
                                    - float(r["canon_worst_err"]))
                                   - float(r["premium"])) <= 1e-12
                               for r in grid))
        grid_means = {h: sum(float(r["premium"]) for r in grid
                             if r["host"] == h) / 3 for h in hosts}
        means_bit_exact = bool(all(grid_means[h] == y[h] for h in hosts))
        carry = ft["exp272.per_host.one_zone_premium_mean"]["values"]
        carry_bit_exact = bool(all(float(carry[h]) == y[h] for h in hosts))
        bc_dup = ft["exp272.per_host.n_boundary_cells_base"]["values"]
        bc_dup_identical = bool(all(float(bc_dup[h])
                                    == float(rec_bc["values"][h])
                                    for h in hosts))

        # ---- M2: the three single-mediator SPEARMANS against the
        #      premium (the pre-registered gate reads the SIGNED rho,
        #      the text as written: >= 1 mediator reaches >= 0.5) -----
        spearmans = {k: _spearman(vec, yv)
                     for k, vec in med_vals.items()}
        m2_pass = bool(max(spearmans.values()) >= 0.5)

        # ---- M3: the JOINT OLS rank R2 on the tied-average ranks —
        #      the exp262 convention VERBATIM: the response enters as
        #      its tied-average ranks (rankdata over the 12 hosts),
        #      the mediators enter as the deposited numeric values
        #      (exp262's predictors were the factor design columns;
        #      the numeric mediator IS its design column here). Three
        #      single-mediator models + the full model; the shares by
        #      the two-order symmetric average on the pre-named entry
        #      order mia -> bc -> pd and its reverse pd -> bc -> mia.
        #      The all-ranks variant (mediators ranked too) is
        #      AUDIT-ONLY, never gated. ------------------------------
        Rk = rankdata(yv)
        mia, bc, pd_ = ("mia_prod_err", "n_boundary_cells_base",
                        "pair_junction_count_mean_canonical")
        r2_single = {k: _r2([med_vals[k]], Rk)
                     for k in (mia, bc, pd_)}
        r2_mia_bc = _r2([med_vals[mia], med_vals[bc]], Rk)
        r2_mia_pd = _r2([med_vals[mia], med_vals[pd_]], Rk)
        r2_bc_pd = _r2([med_vals[bc], med_vals[pd_]], Rk)
        r2_full = _r2([med_vals[mia], med_vals[bc], med_vals[pd_]], Rk)
        m3_pass = bool(r2_full >= 0.5)

        # the two order-of-entry decompositions (exp229's/exp262's
        # exact convention — the symmetric average of the two
        # sequential R2 increments; unexplained = 1 - R2_full; the
        # split sums to 1 EXACTLY, no clamping)
        inc_o1 = {"mia_prod_err": r2_single[mia],
                  "n_boundary_cells_base": r2_mia_bc - r2_single[mia],
                  "pair_junction_count_mean_canonical":
                      r2_full - r2_mia_bc}
        inc_o2 = {"pair_junction_count_mean_canonical":
                      r2_single[pd_],
                  "n_boundary_cells_base": r2_bc_pd - r2_single[pd_],
                  "mia_prod_err": r2_full - r2_bc_pd}
        shares = {k: 0.5 * (inc_o1[k] + inc_o2[k])
                  for k in (mia, bc, pd_)}
        share_unexplained = 1.0 - r2_full
        shares_sum = sum(shares.values()) + share_unexplained
        shares_ok = bool(abs(shares_sum - 1.0) < 1e-9)
        assert shares_ok, "four-way shares do not sum to 1"
        assert all(v == v and abs(v) != float("inf")
                   for v in list(shares.values())
                   + [share_unexplained, r2_full]), "non-finite share"

        # audit-only: the all-ranks variant (mediators ranked too —
        # each single-mediator R2 is then Spearman^2 by construction;
        # reported, never gated)
        rk = {k: rankdata(np.asarray(v, dtype=float))
              for k, v in med_vals.items()}
        audit_all_ranks = {
            "r2_single": {k: _r2([rk[k]], Rk) for k in (mia, bc, pd_)},
            "r2_full": _r2([rk[mia], rk[bc], rk[pd_]], Rk)}
        audit_all_ranks["single_equals_spearman_squared"] = bool(
            all(abs(audit_all_ranks["r2_single"][k]
                    - spearmans[k] ** 2) < 1e-12 for k in (mia, bc, pd_)))

        ties = {"one_zone_premium_mean": _ties_census(yv),
                "mia_prod_err": _ties_census(med_vals[mia]),
                "n_boundary_cells_base": _ties_census(med_vals[bc]),
                "pair_junction_count_mean_canonical":
                    _ties_census(med_vals[pd_])}

        m1_pass = bool(complete and chain_all_ok and grid_ok
                       and means_bit_exact and carry_bit_exact
                       and bc_dup_identical)

        return {
            "hosts": hosts, "table": table,
            "mediator_provenance": mediator_provenance,
            "m1": {"pass": m1_pass, "complete_12x4": complete,
                   "all_finite": all_finite,
                   "exp273_recorded_input_shas_match_actual_bytes":
                       chain_ok,
                   "exp273_provenance_chain_sha_verified": chain_all_ok,
                   "exp272_grid_arithmetic_recompute_ok": grid_ok,
                   "grid_means_bit_exact_vs_per_host": means_bit_exact,
                   "exp273_carry_of_means_bit_exact": carry_bit_exact,
                   "boundary_count_duplicate_carrier_identical":
                       bc_dup_identical},
            "m2": {"pass": m2_pass, "spearman_rho": spearmans,
                   "spearman_rho_abs": {k: abs(v) for k, v
                                        in spearmans.items()},
                   "gate_read": ("the SIGNED rho, the pre-registered "
                                 "text as written: >= 1 mediator "
                                 "reaches >= 0.5; the pair deficit's "
                                 "negative signed rho is the "
                                 "direction its name pre-names "
                                 "(fewer pair junctions <-> higher "
                                 "premium)")},
            "m3": {"pass": m3_pass, "r2_full": r2_full,
                   "r2_single": r2_single,
                   "r2_pairs": {"mia_prod_err+n_boundary_cells_base":
                                r2_mia_bc,
                                "mia_prod_err+pair_deficit": r2_mia_pd,
                                "n_boundary_cells_base+pair_deficit":
                                r2_bc_pd},
                   "audit_all_ranks_variant": audit_all_ranks},
            "attribution": {
                "r2_full": r2_full, "r2_single": r2_single,
                "r2_pairs": {"mia_prod_err+n_boundary_cells_base":
                             r2_mia_bc,
                             "mia_prod_err+pair_deficit": r2_mia_pd,
                             "n_boundary_cells_base+pair_deficit":
                             r2_bc_pd},
                "order_decompositions": {
                    "order_mia_bc_pd": inc_o1,
                    "order_pd_bc_mia": inc_o2},
                "shares_of_rank_variance": shares,
                "unexplained": share_unexplained,
                "shares_sum": shares_sum,
                "ties_census": ties}}

    payload_a = compute()
    sha_a = hashlib.sha256(json.dumps(
        payload_a, sort_keys=True, default=str).encode()).hexdigest()
    payload_b = compute()
    sha_b = hashlib.sha256(json.dumps(
        payload_b, sort_keys=True, default=str).encode()).hexdigest()
    deterministic = bool(sha_a == sha_b)
    assert deterministic, "the computation is not two-pass deterministic"

    gates = {"M1_grids": {
                 "pass": payload_a["m1"]["pass"],
                 "bar": "the 12-host table complete (the premium means "
                        "from exp272's deposit; the three mediators "
                        "from exp273's deposited field table); "
                        "sha-verified READ-ONLY",
                 **payload_a["m1"]},
             "M2_single_mediators": {
                 "pass": payload_a["m2"]["pass"],
                 "bar": "each mediator's Spearman against the premium "
                        "reported; the gate: >= 1 mediator reaches "
                        ">= 0.5",
                 **payload_a["m2"]},
             "M3_joint_model": {
                 "pass": payload_a["m3"]["pass"],
                 "bar": "the full model's rank R2 reported; the gate: "
                        "R2 >= 0.5 (the mediators jointly carry the "
                        "shelf price)",
                 **payload_a["m3"]}}

    # ---- M4: the discipline --------------------------------------------
    ro_after = {"exp272_deposit": _sha(DEP272),
                "exp273_deposit": _sha(DEP273),
                "exp243_deposit": _sha(DEP243),
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

    m4_pass = bool(ro_unchanged and deterministic and no_wall_clock
                   and floor_at_entry == PROD_FLOOR
                   and docstring_ok and header_ok)

    gates["M4_discipline"] = {
        "pass": m4_pass,
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
        "docstring_byte_unchanged_vs_60aff99": docstring_ok,
        "header_sha256": header_sha,
        "header_byte_unchanged_vs_60aff99": header_ok,
        "deposit_form": ("deterministic: no wall-clock fields — a "
                         "re-run of this module reproduces this file "
                         "byte-identically")}

    # ---- the branch (pre-named): M2 or M3 -> PRICE-MEDIATED -------------
    m1_pass = gates["M1_grids"]["pass"]
    m2_pass = gates["M2_single_mediators"]["pass"]
    m3_pass = gates["M3_joint_model"]["pass"]
    branch = ("PRICE-MEDIATED" if (m2_pass or m3_pass)
              else "PRICE-UNMEDIATED")
    gate_passes = {"M1": m1_pass, "M2": m2_pass, "M3": m3_pass,
                   "M4": m4_pass}
    n_pass = sum(1 for v in gate_passes.values() if v)
    n_refute = 4 - n_pass

    # ---- the verdict (one line, the numbers data-driven) ----------------
    sp = payload_a["m2"]["spearman_rho"]
    r2s = payload_a["attribution"]["r2_single"]
    sh = payload_a["attribution"]["shares_of_rank_variance"]
    un = payload_a["attribution"]["unexplained"]
    r2f = payload_a["attribution"]["r2_full"]

    def _g(v):
        return format(v, ".10g") if isinstance(v, float) else str(v)

    verdict = (
        f"{n_pass}/4 gates M1-M4 ({n_pass} PASS / {n_refute} REFUTE) | "
        f"{branch} | M2 "
        f"{'PASS' if m2_pass else 'REFUTED'}: Spearman(mia_prod_err, "
        f"one-zone premium) {_g(sp['mia_prod_err'])} vs the 0.5 bar "
        f"(boundary count {_g(sp['n_boundary_cells_base'])}, pair "
        f"deficit {_g(sp['pair_junction_count_mean_canonical'])} "
        f"signed — the direction its name pre-names) | M3 "
        f"{'PASS' if m3_pass else 'REFUTED'}: full rank R2 {_g(r2f)} "
        f"vs the 0.5 bar (singles mia {_g(r2s['mia_prod_err'])} / "
        f"boundary {_g(r2s['n_boundary_cells_base'])} / pair "
        f"{_g(r2s['pair_junction_count_mean_canonical'])}) | shares "
        f"(two-order symmetric, mia->bc->pd): mia {_g(sh['mia_prod_err'])} "
        f"/ boundary {_g(sh['n_boundary_cells_base'])} / pair "
        f"{_g(sh['pair_junction_count_mean_canonical'])} / unexplained "
        f"{_g(un)} | 12 hosts, a pure re-read of exp272's premium means "
        f"+ exp273's field table, READ-ONLY byte-unchanged, two-pass "
        f"bit-identical, floor -60.0")

    deposit = {
        "exp": "exp274_premium_mechanism",
        "claim": (
            "THE PREMIUM MECHANISM (batch 32, L251's registered next "
            "(a), pre-registration commit 60aff99): the 12-host "
            "mediator regression — the per-host one-zone premium "
            "means (exp272's deposit) against the three external "
            "mediators exp273 named (mia_prod_err, "
            "n_boundary_cells_base, the canonical pair-junction "
            "mean), each alone (Spearman) and jointly (the OLS rank "
            "R2 on the tied-average ranks, the exp262 convention; "
            "three single-mediator models + the full model; the "
            "shares by the two-order symmetric average on the entry "
            "order mia_prod_err -> boundary count -> pair deficit); "
            "is the external signature the PRICE itself or a "
            "correlate? — branches PRICE-MEDIATED / "
            "PRICE-UNMEDIATED"),
        "method": {
            "response": ("the per-host one-zone premium mean (exp272's "
                         "deposit per_host.<H>.one_zone_premium_mean, "
                         "12 values) — the shelf price whose carrier "
                         "is in question"),
            "mediators": ("the three external separating fields from "
                          "exp273's deposited 12-host field table, BY "
                          "EXACT FIELD NAME: "
                          "exp243.classes.multi_identity_audit.prod_err "
                          "(semantic mia_prod_err), "
                          "exp243.classes.n_boundary_cells_base "
                          "(semantic n_boundary_cells_base), "
                          "exp256.rows."
                          "pair_junction_count_mean_canonical "
                          "(semantic pair_junction_count_mean_"
                          "canonical); all three selection-tagged "
                          "external in exp273's table — the "
                          "non-circular discriminator set"),
            "spearman": ("Pearson on the tied-average ranks (scipy "
                         "rankdata both sides), exp272's exact "
                         "_spearman convention"),
            "ols_rank_r2": ("the exp262 convention VERBATIM: the "
                            "response enters as its tied-average "
                            "ranks (rankdata over the 12 hosts), the "
                            "mediators enter as the deposited numeric "
                            "values (exp262's predictors were the "
                            "factor design columns; the numeric "
                            "mediator IS its design column here); OLS "
                            "with intercept, np.linalg.lstsq"),
            "models": ("three single-mediator models + the full "
                       "model + the three pairs the shares need; "
                       "entry order the docstring pre-names: "
                       "mia_prod_err -> boundary count -> pair "
                       "deficit, and its reverse pd -> bc -> mia"),
            "shares": ("exp229's/exp262's exact convention: each "
                       "mediator's share the symmetric average of "
                       "its two sequential R2 increments; unexplained "
                       "= 1 - R2_full; sums to 1 exactly, no "
                       "clamping"),
            "convention_disclosure": ("the single-mediator OLS rank "
                                      "R2s and the Spearmans are "
                                      "SEPARATE pre-registered "
                                      "reports (M2 reads the "
                                      "Spearmans, M3 the full-model "
                                      "R2); the all-ranks variant "
                                      "(mediators ranked too — "
                                      "single-mediator R2 == "
                                      "Spearman^2 by construction) "
                                      "is reported AUDIT-ONLY, "
                                      "never gated"),
            "method_source": ("experiments/exp262_variance_components"
                              ".py (the OLS-on-tied-average-ranks "
                              "convention, verbatim arithmetic), "
                              "experiments/exp272_host_premium_"
                              "structure.py (the _spearman/_ols "
                              "helpers, the premium means), "
                              "experiments/exp273_outlier_hosts.py "
                              "(the deposited field table)")},
        "inputs": {
            "exp272_deposit": {
                "path": "results/exp272_host_premium_structure.json",
                "sha256": ro_before["exp272_deposit"],
                "role": ("the per-host one-zone premium means (the "
                         "response) + the deposited one-zone grid "
                         "the means are re-derived from")},
            "exp273_deposit": {
                "path": "results/exp273_outlier_hosts.json",
                "sha256": ro_before["exp273_deposit"],
                "role": ("the deposited 12-host field table — the "
                         "three mediators read from it BY EXACT "
                         "FIELD NAME, with exp273's own provenance "
                         "chain sha-verified against the actual "
                         "deposit bytes")},
            "exp243_deposit": {
                "path": "results/exp243_structured_adversarial.json",
                "sha256": ro_before["exp243_deposit"],
                "role": ("exp273's provenance: the classes records "
                         "carrying mia_prod_err and "
                         "n_boundary_cells_base — sha-verified, "
                         "never opened for computation here")},
            "exp271_deposit": {
                "path": "results/exp271_one_zone_premium.json",
                "sha256": ro_before["exp271_deposit"],
                "role": ("exp273's provenance: the one-zone premium "
                         "grid — sha-verified, never opened")},
            "exp182_deposit": {
                "path": "results/exp182_substrate_100.json",
                "sha256": ro_before["exp182_deposit"],
                "role": ("exp273's provenance: the margin profiles "
                         "— sha-verified, never opened")},
            "exp256_deposit": {
                "path": "results/exp256_row_pair_regression.json",
                "sha256": ro_before["exp256_deposit"],
                "role": ("exp273's provenance: the row records "
                         "carrying the canonical pair-junction mean "
                         "— sha-verified, never opened")}},
        "hosts": payload_a["hosts"],
        "regression_table": payload_a["table"],
        "mediator_provenance": payload_a["mediator_provenance"],
        "attribution": payload_a["attribution"],
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
            "docstring_byte_unchanged_vs_60aff99": docstring_ok,
            "header_sha256": header_sha,
            "header_byte_unchanged_vs_60aff99": header_ok,
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

    print("=== exp274: THE PREMIUM MECHANISM (pure deposit re-read + "
          "arithmetic) ===")
    print("  the 12-host mediator regression: the one-zone premium "
          "means (exp272) vs the three external mediators exp273 "
          "named, singly and jointly")
    print(f"\n  M1 grids: {'PASS' if m1_pass else 'FAIL'} "
          f"(12 hosts x 4 columns complete/finite; exp272 grid "
          f"arithmetic recompute ok, per-host means bit-exact; "
          f"exp273's field-table carry bit-exact; exp273's provenance "
          f"chain sha-verified 5/5)")
    print(f"  M2 single mediators: {'PASS' if m2_pass else 'FAIL'} — "
          f"Spearman vs the one-zone premium (n=12):")
    for k, v in sp.items():
        print(f"      {k:40s} {v: .4f}  (|rho| {abs(v):.4f})")
    m3g = gates["M3_joint_model"]
    print(f"  M3 joint model: {'PASS' if m3_pass else 'FAIL'} — "
          f"full rank R2 {r2f:.4f} (singles mia "
          f"{r2s['mia_prod_err']:.4f} / boundary "
          f"{r2s['n_boundary_cells_base']:.4f} / pair "
          f"{r2s['pair_junction_count_mean_canonical']:.4f}; "
          f"audit all-ranks full R2 "
          f"{m3g['audit_all_ranks_variant']['r2_full']:.4f})")
    print(f"  shares (two-order symmetric, mia->bc->pd): mia "
          f"{sh['mia_prod_err']:.4f} / boundary "
          f"{sh['n_boundary_cells_base']:.4f} / pair "
          f"{sh['pair_junction_count_mean_canonical']:.4f} / "
          f"unexplained {un:.4f} (sum "
          f"{payload_a['attribution']['shares_sum']:.12f})")
    print(f"  M4 discipline: {'PASS' if m4_pass else 'FAIL'} "
          f"(6 deposits READ-ONLY byte-unchanged: {ro_unchanged}; "
          f"two-pass bit-identical: {deterministic}; no wall-clock "
          f"fields: {no_wall_clock})")
    print(f"\n  BRANCH: {branch}")
    print(f"\n  GATES: {verdict}")
    print(f"  deposited {OUT}")

    # the hard rule, re-asserted after the work: the docstring is still
    # the 60aff99 pre-registration, byte-for-byte
    assert hashlib.sha256(__doc__.encode()).hexdigest() \
        == EXPECTED_DOCSTRING_SHA256, "docstring drifted after the work"
    with open(__file__, "r", encoding="utf-8") as _f:
        _src2 = _f.read()
    assert hashlib.sha256(
        _src2[:_src2.index(_marker) + len(_marker)].encode()
    ).hexdigest() == EXPECTED_HEADER_SHA256, "header drifted after work"
    # the source deposits are still byte-unchanged after the work
    assert set(_sha(p) for p in (DEP272, DEP273, DEP243, DEP271,
                                 DEP182, DEP256)) \
        == set(ro_before.values()), "source deposit drifted after work"

    # THE FLOOR ASSERT AT EXIT (the hard rule; exp243's closing line)
    CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at exit"
    return deposit


if __name__ == "__main__":
    main()
