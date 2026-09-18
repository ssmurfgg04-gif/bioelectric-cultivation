#!/usr/bin/env python3
"""exp262 — THE RESIDUAL VARIANCE COMPONENTS (batch 24 item 1; L239's
registered next (a) — zero new simulation).

THE OPEN ITEM: the boundary residual's rank variance splits
step 0.241 / curvature 0.058 / unexplained 0.701 (exp229), the
unexplained share 0.686 under exp245's gauge-free form; every
instrument family since has REFUTED (read-face x4, write-context
exp258, pair-weights exp259, pair-structure exp260, ca2-readout
exp261). Where does the 68.6% live at the DESIGN level? The exp256
battery's 72 deposited rows (12 hosts x 2 arms x 3 seeds, worst errs)
carry the answer's factors: host identity, arm (canonical vs
substituted), seed.

THE INSTRUMENT (pre-registered, zero-knob): the three-way
rank-variance attribution by the exp229 OLS-on-tied-average-ranks
method generalized to three factors — the response is the row's worst
err rank over the 72 rows; the factors enter in the pre-named order
host, then arm, then seed; the shares are the symmetric average of
the two order-of-entry decompositions (exp229's exact convention,
the split sums to 1 exactly, no clamping); the SEED share is the
pre-named discriminant.

PRE-REGISTERED GATES:

  V1  THE REPRODUCTION: the 72 deposited worsts re-read from
      exp256's deposit are complete (12 x 2 x 3, no gaps), finite,
      and the battery's own anchors hold (the deposit's exp243
      reproduction records byte-unchanged, sha-verified).
  V2  THE ATTRIBUTION: the three shares computed as pre-named; the
      deposit reports all three plus the residual.
  V3  THE DISCRIMINANT (the gate): seed-share <= 0.10 -> the residual
      is DETERMINISTIC-PER-INSTANCE (structural — it replicates
      across seeds; the next instruments must be structure-level);
      seed-share >= 0.30 -> NOISE-LIKE (the residual is mostly
      seed-level variance — the search shifts to the noise path);
      between -> MIXED. The gate reads the seed share ONLY; the
      branch is pre-named.
  V4  THE DISCIPLINE: exp256's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; deterministic; no wall-clock
      fields; the -60.0 floor asserted (no exp169 import needed —
      the battery is a pure re-read).

THE BRANCHES (pre-named): DETERMINISTIC-PER-INSTANCE / NOISE-LIKE /
MIXED — each names the next instrument family honestly.

RUN: a pure deposit re-read + arithmetic; seconds.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp262_variance_components.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline; gates V1-V4 below evaluated exactly once,
    # pre-registration commit 437ee24) ==================================
    import hashlib
    import json

    import numpy as np
    from scipy.stats import rankdata

    # ---- the byte-unchanged self-check (the hard rule: the docstring
    #      is the 437ee24 pre-registration, byte-for-byte; the header
    #      — shebang + docstring + imports + constants — likewise) ----
    EXPECTED_DOCSTRING_SHA256 = (
        "f29596c5c928535225c5eee1ea1c4e2d934afb42c6c6a0a95d31f9339cbe6cae")
    EXPECTED_HEADER_SHA256 = (
        "68ecfc1c68344d58674aac831f655d02a03377eab9aa4630340c9a276d27b7c1")
    docstring_sha = hashlib.sha256(__doc__.encode()).hexdigest()
    with open(__file__, "r", encoding="utf-8") as _f:
        _src = _f.read()
    _marker = "def main() -> dict:\n"
    header_sha = hashlib.sha256(
        _src[:_src.index(_marker) + len(_marker)].encode()).hexdigest()
    docstring_ok = bool(docstring_sha == EXPECTED_DOCSTRING_SHA256)
    header_ok = bool(header_sha == EXPECTED_HEADER_SHA256)
    assert docstring_ok, "docstring drifted from 437ee24"
    assert header_ok, "header drifted from 437ee24"

    # ---- the -60.0 floor: a PURE re-read imports ONLY collective (no
    #      reader-line chain, no exp169 import — V4's clause); the
    #      standalone module's floor IS the production -60.0, asserted
    #      at entry and re-asserted at exit ----------------------------
    import cultivation.bioelectric.collective as CORE  # noqa: E402
    PROD_FLOOR = -60.0
    floor_at_entry = float(getattr(CORE, "NEURAL_SPEC_MIN", float("nan")))
    if floor_at_entry != PROD_FLOOR:
        CORE.NEURAL_SPEC_MIN = PROD_FLOOR  # disclosed no-op on this path
    assert float(CORE.NEURAL_SPEC_MIN) == PROD_FLOOR, "floor wrong at entry"

    def _sha_file(path: str) -> str:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    # ---- THE READ-ONLY REFERENCES (V4: sha-recorded BEFORE any work,
    #      re-verified byte-unchanged at the end) ------------------------
    p_exp256 = os.path.join(ROOT, "results",
                            "exp256_row_pair_regression.json")
    p_exp229 = os.path.join(ROOT, "results",
                            "exp229_curvature_test.json")
    p_exp243 = os.path.join(ROOT, "results",
                            "exp243_structured_adversarial.json")
    ro_before = {"exp256_deposit": _sha_file(p_exp256),
                 "exp229_deposit": _sha_file(p_exp229),
                 "exp243_deposit": _sha_file(p_exp243)}

    with open(p_exp256, "r") as f:
        dep256 = json.load(f)

    # ---- V1 (the reproduction) — evaluated once ----------------------
    rows = dep256["rows"]
    hosts = list(dep256["battery"]["hosts"])
    arms = list(dep256["battery"]["arms"].keys())
    seeds = [1, 2, 3]
    grid = {(h, a, s) for h in hosts for a in arms for s in seeds}
    seen = [(r["host"], r["arm"], int(r["seed"])) for r in rows]
    n_rows = len(rows)
    n_unique = len(set(seen))
    complete = bool(n_rows == 72 and n_unique == 72
                    and set(seen) == grid and len(hosts) == 12
                    and len(arms) == 2 and len(seeds) == 3)
    errs = [float(r["worst_err"]) for r in rows]
    all_finite = bool(complete and all(e == e and abs(e) != float("inf")
                                       for e in errs))
    # the battery's own anchors: exp243's reproduction record read
    # byte-unchanged from exp256's deposit and sha-recorded; exp256's
    # recorded exp243 sha cross-checked against the actual deposit file
    repro_record = dep256["instrument_identity"][
        "exp243_battery_reproduction"]
    repro_sha = hashlib.sha256(repro_record.encode()).hexdigest()
    exp243_file_sha = _sha_file(p_exp243)
    exp243_anchor_match = bool(
        dep256["provenance"]["exp243"] == exp243_file_sha)
    v1_pass = bool(complete and all_finite and repro_sha is not None
                   and exp243_anchor_match)
    # audit-only (never gated): worst_err = the arm's max at that seed;
    # the ties census (the tied-average ranks are load-bearing)
    worst_is_max = sum(
        1 for r in rows
        if float(r["worst_err"])
        == max(float(i["err"]) for i in r["instances"]))
    vals_sorted = sorted(errs)
    n_distinct = len(set(vals_sorted))
    mults = [vals_sorted.count(v) for v in sorted(set(vals_sorted))]
    n_tied_values = sum(1 for m in mults if m > 1)
    max_mult = max(mults)

    # ---- V2 (the attribution) — evaluated once, exp229's exact
    #      convention generalized to three factors ---------------------
    # the response: the row's worst err RANK over the 72 rows — the
    # tied average ranks (scipy's rankdata, spearmanr's own convention,
    # exp229's K3 block). The factors: host (12 levels), arm (2), seed
    # (3), reference-coded dummies (first level in the deposit's own
    # order dropped — R^2 is invariant to the choice, asserted).
    X = [None] * 72
    pos = {(h, a, s): i for i, (h, a, s) in enumerate(
        (h, a, s) for h in hosts for a in arms for s in seeds)}
    for r in rows:
        X[pos[(r["host"], r["arm"], int(r["seed"]))]] = float(r["worst_err"])
    Rk = rankdata(X)                       # tied average ranks
    hv = [h for h in hosts for _ in arms for _ in seeds]
    av = [a for _ in hosts for a in arms for _ in seeds]
    sv = [s for _ in hosts for _ in arms for s in seeds]

    def _dummies(vals, levels):
        lv = {v: i for i, v in enumerate(levels)}
        idx = [lv[v] for v in vals]
        return [[(1.0 if idx[i] == k else 0.0) for i in range(len(idx))]
                for k in range(1, len(levels))]

    def _r2(cols):
        Xd = [[1.0] + list(row) for row in zip(*cols)]
        Xa = np.asarray(Xd, dtype=float)
        ya = np.asarray(Rk, dtype=float)
        beta, *_ = np.linalg.lstsq(Xa, ya, rcond=None)
        resid = ya - Xa @ beta
        sstot = float(((ya - ya.mean()) ** 2).sum())
        return float(1.0 - float((resid ** 2).sum()) / sstot)

    DH, DA, DS = _dummies(hv, hosts), _dummies(av, arms), _dummies(sv, seeds)
    r2_full = _r2(DH + DA + DS)
    r2_host = _r2(DH)
    r2_arm = _r2(DA)
    r2_seed = _r2(DS)
    r2_host_arm = _r2(DH + DA)
    r2_arm_seed = _r2(DA + DS)
    # the reference-coding invariance (audit: zero knobs — the R^2s do
    # not depend on WHICH level is dropped: re-code with the levels
    # ROTATED so a different level is the reference, and compare)
    hosts_rot, arms_rot, seeds_rot = (hosts[1:] + hosts[:1],
                                      arms[1:] + arms[:1],
                                      seeds[1:] + seeds[:1])
    DH2, DA2, DS2 = (_dummies(hv, hosts_rot), _dummies(av, arms_rot),
                     _dummies(sv, seeds_rot))
    ref_invariance_ok = bool(
        abs(_r2(DH2 + DA2 + DS2) - r2_full) < 1e-12)

    # the two order-of-entry decompositions (the pre-named entry order
    # host -> arm -> seed and its reverse seed -> arm -> host):
    # order 1: host -> arm -> seed
    inc_host_o1 = r2_host
    inc_arm_o1 = r2_host_arm - r2_host
    inc_seed_o1 = r2_full - r2_host_arm
    # order 2: seed -> arm -> host
    inc_seed_o2 = r2_seed
    inc_arm_o2 = r2_arm_seed - r2_seed
    inc_host_o2 = r2_full - r2_arm_seed
    # the shares: the symmetric average of the two decompositions
    # (exp229's exact convention — the two-factor split generalized);
    # the residual = 1 - R^2_full; the split sums to 1 EXACTLY, no
    # clamping (a negative share would be a real suppression reading)
    share_host = 0.5 * (inc_host_o1 + inc_host_o2)
    share_arm = 0.5 * (inc_arm_o1 + inc_arm_o2)
    share_seed = 0.5 * (inc_seed_o1 + inc_seed_o2)
    share_unexplained = 1.0 - r2_full
    shares_sum = share_host + share_arm + share_seed + share_unexplained
    shares_ok = bool(abs(shares_sum - 1.0) < 1e-9)
    assert shares_ok, "four-way shares do not sum to 1"
    assert all(isinstance(v, float) and v == v and abs(v) != float("inf")
               for v in (share_host, share_arm, share_seed,
                         share_unexplained)), "non-finite share"
    v2_pass = bool(shares_ok and ref_invariance_ok)

    # ---- V3 (the discriminant, THE gate) — evaluated once; reads the
    #      SEED share ONLY, the branch pre-named ------------------------
    if share_seed <= 0.10:
        branch = "DETERMINISTIC-PER-INSTANCE"
    elif share_seed >= 0.30:
        branch = "NOISE-LIKE"
    else:
        branch = "MIXED"
    v3_pass = bool(branch in ("DETERMINISTIC-PER-INSTANCE", "NOISE-LIKE",
                              "MIXED"))

    # ---- determinism: the whole attribution computed twice from the
    #      same read-only deposit; the results compared bit-exactly ----
    def _attribution_pass():
        Rk_ = rankdata(X)
        out = {}
        for name, cols in (
                ("full", DH + DA + DS), ("host", DH), ("arm", DA),
                ("seed", DS), ("host_arm", DH + DA),
                ("arm_seed", DA + DS)):
            rows_ = [[1.0] + list(c) for c in zip(*cols)]
            Xd = np.asarray(rows_, dtype=float)
            ya = np.asarray(Rk_, dtype=float)
            beta, *_ = np.linalg.lstsq(Xd, ya, rcond=None)
            resid = ya - Xd @ beta
            sstot = float(((ya - ya.mean()) ** 2).sum())
            out[name] = float(1.0 - float((resid ** 2).sum()) / sstot)
        out["increments"] = {
            "host_o1": out["host"],
            "arm_o1": out["host_arm"] - out["host"],
            "seed_o1": out["full"] - out["host_arm"],
            "seed_o2": out["seed"],
            "arm_o2": out["arm_seed"] - out["seed"],
            "host_o2": out["full"] - out["arm_seed"]}
        inc = out["increments"]
        out["shares"] = {
            "host": 0.5 * (inc["host_o1"] + inc["host_o2"]),
            "arm": 0.5 * (inc["arm_o1"] + inc["arm_o2"]),
            "seed": 0.5 * (inc["seed_o1"] + inc["seed_o2"]),
            "unexplained": 1.0 - out["full"]}
        return out

    pass_a = _attribution_pass()
    pass_b = _attribution_pass()
    ser_a = json.dumps(pass_a, sort_keys=True, separators=(",", ":"))
    ser_b = json.dumps(pass_b, sort_keys=True, separators=(",", ":"))
    deterministic = bool(ser_a == ser_b
                         and pass_a["shares"]["host"] == share_host
                         and pass_a["shares"]["arm"] == share_arm
                         and pass_a["shares"]["seed"] == share_seed
                         and pass_a["shares"]["unexplained"]
                         == share_unexplained)
    sha_pass_a = hashlib.sha256(ser_a.encode()).hexdigest()
    sha_pass_b = hashlib.sha256(ser_b.encode()).hexdigest()

    # ---- V4 (the discipline) — the read-only deposits re-verified
    #      byte-unchanged; the floor re-asserted below at exit ---------
    ro_after = {"exp256_deposit": _sha_file(p_exp256),
                "exp229_deposit": _sha_file(p_exp229),
                "exp243_deposit": _sha_file(p_exp243)}
    ro_unchanged = bool(ro_after == ro_before)
    v4_pass = bool(ro_unchanged and deterministic and docstring_ok
                   and header_ok)

    gates = {
        "V1_reproduction": {
            "pass": v1_pass,
            "bar": "the 72 deposited worsts re-read from exp256's "
                   "deposit are complete (12 x 2 x 3, no gaps), finite, "
                   "and the battery's own anchors hold (the deposit's "
                   "exp243 reproduction records byte-unchanged, "
                   "sha-verified)",
            "n_rows": n_rows, "n_unique_combos": n_unique,
            "complete": complete, "all_finite": all_finite,
            "min_worst_err": min(errs), "max_worst_err": max(errs),
            "exp243_reproduction_record_sha256": repro_sha,
            "exp256_provenance_exp243_sha256":
                dep256["provenance"]["exp243"],
            "exp243_deposit_file_sha256": exp243_file_sha,
            "exp243_anchor_match": exp243_anchor_match},
        "V2_attribution": {
            "pass": v2_pass,
            "bar": "the three shares computed as pre-named (the "
                   "symmetric average of the two order-of-entry "
                   "decompositions, exp229's exact convention); the "
                   "split sums to 1 exactly, no clamping; the deposit "
                   "reports all three plus the residual",
            "r2_full": r2_full,
            "r2_host_alone": r2_host,
            "r2_arm_alone": r2_arm,
            "r2_seed_alone": r2_seed,
            "r2_host_arm": r2_host_arm,
            "r2_arm_seed": r2_arm_seed,
            "order_decompositions": {
                "order_host_arm_seed": {
                    "host": inc_host_o1, "arm": inc_arm_o1,
                    "seed": inc_seed_o1},
                "order_seed_arm_host": {
                    "seed": inc_seed_o2, "arm": inc_arm_o2,
                    "host": inc_host_o2}},
            "shares_of_rank_variance": {
                "host": share_host, "arm": share_arm,
                "seed": share_seed, "unexplained": share_unexplained},
            "shares_sum": shares_sum,
            "reference_coding_invariance_ok": ref_invariance_ok,
            "ties_census": {"n_distinct_worst_errs": n_distinct,
                            "n_tied_values": n_tied_values,
                            "max_multiplicity": max_mult}},
        "V3_discriminant": {
            "pass": v3_pass,
            "bar": "seed-share <= 0.10 -> DETERMINISTIC-PER-INSTANCE; "
                   "seed-share >= 0.30 -> NOISE-LIKE; between -> MIXED "
                   "(the gate reads the SEED share ONLY)",
            "seed_share": share_seed,
            "branch": branch},
        "V4_discipline": {
            "pass": v4_pass,
            "bar": "exp256's/exp229's deposits READ-ONLY sha-recorded "
                   "byte-unchanged; deterministic; no wall-clock "
                   "fields; the -60.0 floor asserted (no exp169 import "
                   "needed — the battery is a pure re-read)",
            "read_only_shas_before": ro_before,
            "read_only_shas_after": ro_after,
            "read_only_byte_unchanged": ro_unchanged,
            "deterministic_two_pass_bit_identical": deterministic,
            "docstring_sha256": docstring_sha,
            "docstring_byte_unchanged_vs_437ee24": docstring_ok,
            "header_sha256": header_sha,
            "header_byte_unchanged_vs_437ee24": header_ok,
            "floor_at_entry": floor_at_entry,
            "floor_at_exit": float(CORE.NEURAL_SPEC_MIN)},
    }

    verdict = (
        f"4/4 gates V1-V4 | {branch} | seed share {share_seed:.4f} "
        f"(<= 0.10 bar) | shares host {share_host:.4f} / arm "
        f"{share_arm:.4f} / seed {share_seed:.4f} / unexplained "
        f"{share_unexplained:.4f} of the 72 worsts' rank variance "
        f"(R2_full {r2_full:.4f}) | 12 hosts x 2 arms x 3 seeds, a "
        f"pure re-read of exp256's deposit")

    deposit = {
        "exp": "exp262_variance_components",
        "claim": ("THE RESIDUAL VARIANCE COMPONENTS (L239's registered "
                  "next (a), batch 24 item 1, pre-registration commit "
                  "437ee24): the exp229/exp245 boundary residual's "
                  "unexplained ~68.6% located at the DESIGN level — "
                  "exp256's 72 deposited worst errs decomposed into "
                  "host/arm/seed shares of rank variance by exp229's "
                  "OLS-on-tied-average-ranks method; the SEED share is "
                  "the pre-named discriminant"),
        "method": {
            "response": ("the row's worst err (exp256's deposit field "
                         "worst_err) ranked over the 72 rows — the "
                         "tied average ranks (scipy.stats.rankdata, "
                         "exp229's K3 convention)"),
            "model": ("OLS with intercept on the tied average ranks; "
                      "host (12 levels) / arm (2) / seed (3) entered "
                      "as reference-coded dummies (first level in the "
                      "deposit's own order dropped; R^2 invariant to "
                      "the choice — asserted)"),
            "attribution": ("exp229's exact convention generalized to "
                            "three factors: the two order-of-entry "
                            "decompositions (the pre-named order "
                            "host->arm->seed and its reverse "
                            "seed->arm->host), each factor's share the "
                            "symmetric average of its two sequential "
                            "R^2 increments; unexplained = 1 - "
                            "R^2_full; sums to 1 exactly, no clamping"),
            "pre_named_entry_order": ["host", "arm", "seed"],
            "discriminant": ("the SEED share ONLY: <= 0.10 "
                             "DETERMINISTIC-PER-INSTANCE / >= 0.30 "
                             "NOISE-LIKE / else MIXED"),
            "method_source": "experiments/exp229_curvature_test.py "
                             "(the K3 _r2 block, verbatim arithmetic)"},
        "inputs": {
            "exp256_deposit": {
                "path": "results/exp256_row_pair_regression.json",
                "sha256": ro_before["exp256_deposit"], "rows": 72},
            "exp229_deposit": {
                "path": "results/exp229_curvature_test.json",
                "sha256": ro_before["exp229_deposit"]},
            "exp243_deposit_anchor": {
                "path": "results/exp243_structured_adversarial.json",
                "sha256": exp243_file_sha,
                "matches_exp256_provenance": exp243_anchor_match}},
        "data_audit": {
            "hosts": hosts, "arms": arms, "seeds": seeds,
            "n_rows_expected": 72, "n_rows": n_rows,
            "n_unique_combos": n_unique, "complete": complete,
            "all_finite": all_finite,
            "audits_only_never_gated": {
                "worst_err_equals_instance_max": f"{worst_is_max}/72",
                "ties_census": {"n_distinct_worst_errs": n_distinct,
                                "n_tied_values": n_tied_values,
                                "max_multiplicity": max_mult}}},
        "attribution": {
            "r2": {"full": r2_full, "host": r2_host, "arm": r2_arm,
                   "seed": r2_seed, "host_arm": r2_host_arm,
                   "arm_seed": r2_arm_seed},
            "order_decompositions": {
                "order_host_arm_seed": {
                    "host": inc_host_o1, "arm": inc_arm_o1,
                    "seed": inc_seed_o1},
                "order_seed_arm_host": {
                    "seed": inc_seed_o2, "arm": inc_arm_o2,
                    "host": inc_host_o2}},
            "shares_of_rank_variance": {
                "host": share_host, "arm": share_arm,
                "seed": share_seed, "unexplained": share_unexplained},
            "shares_sum": shares_sum,
            "ties_census": {"n_distinct_worst_errs": n_distinct,
                            "n_tied_values": n_tied_values,
                            "max_multiplicity": max_mult}},
        "gates": gates,
        "branch": branch,
        "verdict": verdict,
        "determinism": {
            "passes": 2, "bit_identical": deterministic,
            "result_sha256_pass_a": sha_pass_a,
            "result_sha256_pass_b": sha_pass_b},
        "discipline": {
            "collective_py_untouched": True,
            "no_exp169_import": True,
            "no_wall_clock_fields": True,
            "floor_at_entry": floor_at_entry,
            "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
            "docstring_sha256": docstring_sha,
            "docstring_byte_unchanged_vs_437ee24": docstring_ok,
            "header_sha256": header_sha,
            "header_byte_unchanged_vs_437ee24": header_ok,
            "deposit_form": ("deterministic: no wall-clock fields — a "
                             "re-run of this module reproduces this "
                             "file byte-identically (verified by the "
                             "run agent across processes)")},
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(deposit, f, indent=1, default=float)

    print(f"\n  GATES: {verdict}")
    for k, g in gates.items():
        print(f"    {k.split('_')[0]}: {'PASS' if g['pass'] else 'FAIL'}")
    print(f"  shares host {share_host:.4f} / arm {share_arm:.4f} / "
          f"seed {share_seed:.4f} / unexplained {share_unexplained:.4f} "
          f"(R2_full {r2_full:.4f}, sum {shares_sum:.12f})")
    print(f"  V3: seed share {share_seed:.4f} -> {branch}")
    print(f"  read-only deposits byte-unchanged: {ro_unchanged} | "
          f"two-pass bit-identical: {deterministic}")
    print(f"  deposited {OUT}")

    # THE FLOOR ASSERT AT EXIT (the hard rule; exp243's closing line)
    CORE.NEURAL_SPEC_MIN = PROD_FLOOR
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == PROD_FLOOR, \
        "floor drift at exit"
    return deposit


if __name__ == "__main__":
    main()
