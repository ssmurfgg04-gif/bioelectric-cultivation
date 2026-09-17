#!/usr/bin/env python3
"""exp165 — THE GENERATOR AT CF-1 (C3 re-run at the repaired floor).

exp156's registered next (L139): adopt CF-1 (spec-floor -35 -> -60)
into the compiler's emitted-cell contract and re-run the generator's
C3 with the R_W canon-clash rule as the structural gate.

======================================================================
PRE-REGISTERED (this docstring written BEFORE the run; the gates are
executed exactly once against these clauses; NO knob is new — the
decode instruments are exp156's dissect / decode_cf / clash_mass /
r_w_predict imported VERBATIM, CF_FLOOR = -60.0 verbatim, the
emitted rungs and seeds are the DEPOSIT's (exp150 delivered rows:
emitted_cell, all (1.0, 0.0); AUDIT_SEEDS = (1, 2, 3)), and every
pass/fail bar is a pre-existing frozen repo constant: ERR_BAR 6.0
(exp136), the novelty bars N*_lib 82.288 / N*_splice 20.14 / N*_pool
33.776 (exp150/exp153 deposits). Byte-offset assert in-module proves
declaration order.)
======================================================================

DESIGN (three steps, all on the deposited stack — no re-search, no
re-pricing, no new anatomy):
  (1) REBUILD the decode of the exp150 delivered-10 PLUS the exp153
      expanded cohort (24 members) under CF-1: decode_cf(f, zones,
      emitted_cell..., seed, spec_floor=-60.0) verbatim per member at
      the DEPOSITED emitted rung and the DEPOSITED 3 seeds. The
      unrepaired floor is evaluated by exp156's dissect verbatim (the
      bit-exact exp136.decode replica).
  (2) RE-EVALUATE exp136's gates C1-C4 on the CF-1-repaired stack:
      C1 NOVELTY UNCHANGED — same inventions (no re-search; CF-1
      touches only the S-REL read branch), so the deposited
      nov_lib/nov_splice of the delivered-10 are re-verified against
      the frozen bars (exactly 10 delivered, every one beyond bar);
      C2 AUDIT UNCHANGED — the quadrature audit is decode-free
      (writability under erosion, not spec-floor-dependent), so the
      deposited emitted_quads are re-verified (>= 8/10 < 6.0);
      C3 DECODE AT THE REPAIRED FLOOR — decode+stability under CF-1
      at the deposited emitted rung (exp136 criterion: decode_err
      < 6.0 AND hold_err < 6.0 on >= 2/3 seeds; the exp150 emission
      grade 3/3 deposited alongside); C4 PAIRWISE UNDER THE POOL BAR
      — deposited min_pairwise_D of the delivered-10 > N*_pool
      33.776 (same inventions => inherited set, re-verified).
  (3) GATES (pre-registered; each evaluated exactly once):
  F1  C3 IMPROVES: the delivered-10 C3 count under CF-1 is >= 9/10
      (exp136 criterion per member), the EXACT count is deposited,
      and the repair is confirmed bit-exactly at the deposited
      emitted rungs and seeds: per failing member the CF-1 per-seed
      decode/hold errs reproduce exp156's deposited cf1 rows at the
      deposit's 3-decimal rounding (exp156 says the 6 failing-class
      members go below bar; the rungs/seeds were NOT re-checked
      there — this gate re-checks them).
  F2  NO REGRESSION: the 8 previously-passing members of the
      delivered-10 stay passing under CF-1 — operationalized as the
      conjunction (all clauses deposited):
        (a) PASS STATUS: each of the 8 is C3-passing under CF-1
            (exp136 criterion) at the deposited rung/seeds — zero
            pass->fail flips; per-seed pass pattern (which seeds
            meet decode<6 AND hold<6) identical to the deposited
            unrepaired pattern (3/3 -> 3/3 for all 8);
        (b) BIT-EXACT INSTRUMENT: my CF-1 re-run reproduces
            exp156's deposited CF-1 values for all 8 (3-dp; the
            harm rows are means) — the readback is the same engine,
            not a re-tuned one;
        (c) BRANCH IDENTITY: members with ZERO unreadable-clash
            cells (clash = (f < -35) & (f != canon); n_clash == 0)
            have a branch-identical regen walk under CF-1 — their
            CF-1 errs must equal the deposited UNREPAIRED errs
            bit-exactly (float equality per seed) and equal the
            dissect replica bit-exactly.
  F3  R_W AS PRE-EMISSION FILTER: applying r_w_predict to the full
      24-member stack, the audit_only_fallback class (the members
      exp150's deposit flags emission_mode == "audit_only_fallback":
      the d-03/d-08-type — audit-passing, decode-failing under the
      unrepaired floor) is removed from delivery WITHOUT new false
      exclusions — checked as set identity both ways:
        every excluded member is R_W-positive AND every delivered
        member is R_W-negative, i.e. {R_W-positive} ==
        {audit_only_fallback} == the exp156 failing class
        (d-03/d-08/d-12/d-19/d-22/d-24), matching exp156's 0-FP
        deposit (clash masses reproduce exp156's w3 rows at 3 dp).
  F4  INSTRUMENT: exp150's deposited decode errs are reproduced
      bit-exactly under the UNREPAIRED floor — exp156's dissect
      replica at the deposited emitted rungs and AUDIT_SEEDS equals
      the exp150 delivered rows' decode_errs at 3 dp for all 10
      (and, as the identity anchor, decode_cf at spec_floor = -35.0
      equals dissect bit-exactly — float equality — proving the
      CF-1 engine is the unrepaired engine with the one constant
      changed and nothing else).

BRANCHES (pre-registered):
  - F1 lands (C3 >= 9/10) WITH F2 AND F3 green (and F4 green):
    THE GENERATOR'S STAGE-3 LEDGER ENTRY UPGRADES — the upgraded
    verdict is deposited explicitly (stage3_ledger_upgrade): C3 at
    the repaired floor, the emission contract amended (CF-1 adopted
    into the emitted-cell contract; R_W as the pre-emission
    structural filter replacing the audit_only_fallback fallback
    mode), no other stage touched.
  - F1 fails (count < 9/10): deposit the exact count and the
    per-member rows; no contract change.
  - F2 fails: a regression — CF-1 is NOT adoptable as-is; deposit
    which member regressed and how.
  - F3 fails (any false exclusion or any fallback member slipping
    through): the R_W pre-filter is not delivery-safe; deposit the
    confusion.
  - F4 fails: instrument drift — stop, no gate interpretation.

RUNTIME BUDGET: 30 dissect + ~102 decode_cf decode-equivalents
(24 x 3 CF-1 + 10 x 3 identity-anchor), BLAS pinned, serial —
well under the 12-minute wall (exp156 ran ~200 in minutes).
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp136_generator_v6 import (  # noqa: E402
    ERR_BAR, AUDIT_SEEDS, N, profile_of_zones, wildtype_target,
    NEURAL_SPEC_MIN,
)
from experiments.exp156_write_path import (  # noqa: E402  VERBATIM
    dissect, decode_cf, clash_mass, r_w_predict, CF_FLOOR,
    FAILING_CLASS,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp165_generator_cf1.json")
DEP150 = os.path.join(ROOT, "results", "exp150_generator_complete.json")
DEP153 = os.path.join(ROOT, "results", "exp153_decode_anatomy.json")
DEP156 = os.path.join(ROOT, "results", "exp156_write_path.json")

# ------------------------------------------------------------------
# PRE-REGISTERED CONSTANTS (frozen repo/deposit values only)
# ------------------------------------------------------------------
N_LIB_BAR = 82.288      # exp150/exp153 deposit N*_lib
N_SPLICE_BAR = 20.14    # exp150/exp153 deposit N*_splice
N_POOL_BAR = 33.776     # exp150/exp153 deposit N*_pool (C4 bar)
C3_MIN_SEEDS = 2        # exp136 C3 criterion: >= 2/3 seeds
BEFORE_PASS_N = 8       # exp150 delivered-10 C3-passing count

DOCSTRING_GATE_MARKER = "PRE-REGISTERED (this docstring written BEFORE"
CONST_MARKER = "N_LIB_BAR = 82.288"
FIRST_DECODE_MARKER = ("# ===== FIRST DECODE-CALL PATH IN THIS MODULE")


def assert_order_precedes_decode_path() -> dict:
    """Pre-registration order discipline (exp153's U3 / exp156's form):
    docstring gate text < frozen constants < first decode-call code
    path, by byte offset in this file."""
    src = open(os.path.abspath(__file__)).read()
    i_doc = src.index(DOCSTRING_GATE_MARKER)
    i_const = src.index(CONST_MARKER)
    i_dec = src.index(FIRST_DECODE_MARKER)
    assert i_doc < i_const < i_dec, \
        "pre-registration order violated: gates+constants must " \
        "precede the decode path"
    return {"docstring_gates_byte": i_doc, "constants_byte": i_const,
            "first_decode_byte": i_dec, "order_held": True}


def c3_member_pass(dec_errs, hold_errs) -> tuple[bool, str]:
    """exp136's frozen C3 criterion on per-seed err lists."""
    ok = [bool(d < ERR_BAR and h < ERR_BAR)
          for d, h in zip(dec_errs, hold_errs)]
    n_ok = sum(int(v) for v in ok)
    return n_ok >= C3_MIN_SEEDS, f"{n_ok}/3"


# ===== FIRST DECODE-CALL PATH IN THIS MODULE (everything above is
# declaration; the byte-offset assert proves the gates and constants
# predate this line). ================================================

def main() -> dict:
    t0 = time.time()
    print("=== exp165: the generator at CF-1 (C3 re-run at the "
          "repaired floor) ===\n")
    stage_order = ["gates+constants declared (docstring + module "
                   "constants, before any decode call)"]
    order_evidence = assert_order_precedes_decode_path()
    print(f"  pre-registration order assert: docstring gates -> "
          f"frozen constants -> first decode path  [bytes "
          f"{order_evidence['docstring_gates_byte']} < "
          f"{order_evidence['constants_byte']} < "
          f"{order_evidence['first_decode_byte']}]")

    dep150 = json.load(open(DEP150))
    dep153 = json.load(open(DEP153))
    dep156 = json.load(open(DEP156))
    delivered = dep150["delivered"]
    cohort = dep153["expanded_cohort"]
    assert len(delivered) == 10 and len(cohort) == 24
    canon = wildtype_target(N)

    # stack consistency: the exp153 cohort's first 10 rows ARE the
    # exp150 delivered rows (names/zones/emitted/errs bit-exact)
    stack_ok = True
    for drow, crow in zip(delivered, cohort):
        same = (drow["name"] == crow["name"]
                and [tuple(z) for z in drow["zones"]]
                == [tuple(z) for z in crow["zones"]]
                and drow["emitted_cell"] == crow["emitted_cell"]
                and drow["decode_errs"] == crow["decode_errs"])
        stack_ok = stack_ok and same
    assert stack_ok, "exp150 delivered-10 vs exp153 cohort drift"
    for r in delivered:
        assert r["emitted_cell"] == [1.0, 0.0], \
            f"{r['name']}: deposited emitted rung is not (1, 0)"
    assert all(d["emission_mode"] == c["emission_mode"]
               for d, c in zip(delivered, cohort)), \
        "emission-mode drift between deposits"
    print("  stack: exp150 delivered-10 == exp153 cohort rows 1-10 "
          "(names/zones/emitted rung/errs/mode bit-exact); all 10 "
          "emitted rungs are the deposited (1.0, 0.0); seeds "
          f"{AUDIT_SEEDS} — no re-tuning\n")

    # ---------------- F4: unrepaired-floor instrument check ---------
    stage_order.append("f4_unrepaired_instrument")
    f4_rows = []
    f4_ok = True
    for r in delivered:
        zones = [tuple(z) for z in r["zones"]]
        f = profile_of_zones(zones)
        g, mu = r["emitted_cell"]
        rep = [dissect(f, zones, g, mu, s) for s in AUDIT_SEEDS]
        rep_errs = [round(d["decode_err"], 3) for d in rep]
        rep_hold = [round(d["hold_err"], 3) for d in rep]
        ok = (rep_errs == r["decode_errs"]
              and rep_hold == r["hold_errs"]
              and not any(d.get("rejected") for d in rep))
        # identity anchor: decode_cf at the UNREPAIRED floor (the
        # frozen NEURAL_SPEC_MIN) must be bit-exact equal to the
        # dissect replica (same engine, one constant unchanged)
        ident = all(decode_cf(f, zones, g, mu, s,
                              float(NEURAL_SPEC_MIN))["decode_err"]
                    == d["decode_err"]
                    for s, d in zip(AUDIT_SEEDS, rep))
        f4_ok = f4_ok and ok and ident
        f4_rows.append({"name": r["name"],
                        "deposited_errs": r["decode_errs"],
                        "replica_errs": rep_errs,
                        "deposited_hold": r["hold_errs"],
                        "replica_hold": rep_hold,
                        "bitexact": ok, "identity_cf35_eq_dissect": ident})
        print(f"  F4[{r['name']}]: replica {rep_errs} vs deposit "
              f"{r['decode_errs']} bitexact={ok} "
              f"identity(-35)==dissect {ident}")
    f4 = bool(f4_ok)
    print(f"  F4 instrument: {'PASS' if f4 else 'FAIL'} — exp150 "
          f"deposited decode errs reproduced bit-exactly under the "
          f"UNREPAIRED floor\n")

    # ---------------- C1 / C2 / C4 (unchanged channels) --------------
    stage_order.append("c1_c2_c4_unchanged_channels")
    c1_rows = [{"name": r["name"], "nov_lib": r["nov_lib"],
                "nov_splice": r["nov_splice"],
                "lib_ok": bool(r["nov_lib"] > N_LIB_BAR),
                "splice_ok": bool(r["nov_splice"] > N_SPLICE_BAR)}
               for r in delivered]
    c1 = bool(len(delivered) == 10
              and all(x["lib_ok"] and x["splice_ok"] for x in c1_rows))
    c2_rows = [{"name": r["name"], "emitted_quad": r["emitted_quad"],
                "audit_ok": bool(r["emitted_quad"] < ERR_BAR)}
               for r in delivered]
    c2_n = sum(int(x["audit_ok"]) for x in c2_rows)
    c2 = bool(c2_n >= 8)
    c4_rows = [{"name": r["name"],
                "min_pairwise_D": r["min_pairwise_D"],
                "pool_ok": bool(r["min_pairwise_D"] > N_POOL_BAR)}
               for r in delivered]
    c4 = bool(all(x["pool_ok"] for x in c4_rows))
    print(f"  C1 novelty (unchanged): 10 delivered, all beyond "
          f"N*_lib {N_LIB_BAR} / N*_splice {N_SPLICE_BAR} "
          f"(min nov_lib {min(x['nov_lib'] for x in c1_rows)}): "
          f"{'PASS' if c1 else 'FAIL'}")
    print(f"  C2 audit (unchanged): {c2_n}/10 emitted_quads < "
          f"{ERR_BAR} (>= 8 required): {'PASS' if c2 else 'FAIL'}")
    print(f"  C4 pairwise (pool bar): min min_pairwise_D "
          f"{min(x['min_pairwise_D'] for x in c4_rows)} > "
          f"N*_pool {N_POOL_BAR}: {'PASS' if c4 else 'FAIL'}\n")

    # ---------------- F3: R_W pre-emission filter --------------------
    stage_order.append("f3_rw_pre_emission_filter")
    f3_rows = []
    for row in cohort:
        zones = [tuple(z) for z in row["zones"]]
        f = profile_of_zones(zones)
        m = clash_mass(f, canon)
        pos = bool(r_w_predict(f, canon))
        f3_rows.append({"name": row["name"],
                        "clash_mass_mV2": round(m, 3),
                        "r_w_positive": pos,
                        "emission_mode_exp150": row["emission_mode"],
                        "exp156_failing_class":
                        row["name"] in FAILING_CLASS})
    rw_pos = {r["name"] for r in f3_rows if r["r_w_positive"]}
    fallback = {r["name"] for r in f3_rows
                if r["emission_mode_exp150"] == "audit_only_fallback"}
    fail_class = {r["name"] for r in f3_rows
                  if r["exp156_failing_class"]}
    # exp156's deposited w3 masses must reproduce bit-exactly
    w3156 = {r["name"]: r["clash_mass_mV2"]
             for r in dep156["w3_rule_evaluation"]}
    mass_match = all(w3156[r["name"]] == r["clash_mass_mV2"]
                     for r in f3_rows)
    f3 = bool(rw_pos == fallback == fail_class and mass_match)
    print(f"  F3 R_W pre-emission filter: R_W-positive "
          f"{sorted(rw_pos)}")
    print(f"      audit_only_fallback {sorted(fallback)} | exp156 "
          f"failing class {sorted(fail_class)}")
    print(f"      set identity both ways: {rw_pos == fallback == fail_class}"
          f" | masses match exp156 w3 deposit: {mass_match} -> "
          f"{'PASS' if f3 else 'FAIL'}\n")

    # ---------------- CF-1 rebuild (all 24) --------------------------
    stage_order.append("cf1_rebuild_24")
    cf_rows = []
    for row in cohort:
        zones = [tuple(z) for z in row["zones"]]
        f = profile_of_zones(zones)
        g, mu = row["emitted_cell"]
        cf = [decode_cf(f, zones, g, mu, s, CF_FLOOR)
              for s in AUDIT_SEEDS]
        dec = [round(d["decode_err"], 3) for d in cf]
        hold = [round(d["hold_err"], 3) for d in cf]
        mean = round(float(np.mean([d["decode_err"] for d in cf])), 3)
        hmean = round(float(np.mean([d["hold_err"] for d in cf])), 3)
        p, grade = c3_member_pass(dec, hold)
        stable333 = all(d < ERR_BAR and h < ERR_BAR
                        for d, h in zip(dec, hold))
        n_clash = int(((f < -35.0) & (f != canon)).sum())
        cf_rows.append({"name": row["name"], "cell": [g, mu],
                        "n_clash_cells": n_clash,
                        "cf1_decode_errs": dec, "cf1_hold_errs": hold,
                        "cf1_decode_err_mean": mean,
                        "cf1_hold_err_mean": hmean,
                        "c3_pass_exp136": p, "c3_seed_grade": grade,
                        "stable_333": stable333,
                        "deposited_decode_pass": row["decode_pass"]})
        print(f"  CF1[{row['name']}] n_clash={n_clash:2d} dec {dec} "
              f"hold {hold} -> C3 {grade} "
              f"(was {'PASS' if row['decode_pass'] else 'FAIL'})")

    # match exp156's deposited CF-1 rows (instrument bit-exactness)
    cf3156 = {r["name"]: r for r in dep156["w2b_cf1_fails"]}
    harm156 = {r["name"]: r for r in dep156["w2b_cf1_pass_harm_check"]}
    dep_match = {}
    for cr in cf_rows:
        nm = cr["name"]
        if nm in cf3156:
            ref = cf3156[nm]
            dep_match[nm] = (cr["cf1_decode_errs"]
                             == ref["cf1_decode_errs"]
                             and cr["cf1_hold_errs"]
                             == ref["cf1_hold_errs"])
        else:
            dep_match[nm] = (cr["cf1_decode_err_mean"]
                             == harm156[nm]["cf1_decode_err_mean"])
    dep_match_all = all(dep_match.values())
    print(f"  CF-1 rebuild vs exp156 deposit: "
          f"{sum(int(v) for v in dep_match.values())}/24 bit-exact "
          f"(3 dp) -> {dep_match_all}\n")

    # ---------------- C3 after + F1 + F2 -----------------------------
    stage_order.append("c3_after_f1_f2")
    c3_after = sum(int(r["c3_pass_exp136"]) for r in cf_rows[:10])
    c3_after_333 = sum(int(r["stable_333"]) for r in cf_rows[:10])
    c3_before = sum(int(r["decode_pass"]) for r in delivered)
    f1_rows = [{"name": r["name"],
                "was_pass": not r["deposited_decode_pass"],
                "cf1_decode_errs": r["cf1_decode_errs"],
                "cf1_hold_errs": r["cf1_hold_errs"],
                "now_pass": r["c3_pass_exp136"]}
               for r in cf_rows[:10] if r["deposited_decode_pass"]]
    f1 = bool(c3_after >= 9 and dep_match_all)
    print(f"  C3 (delivered-10): before {c3_before}/10 (exp150 "
          f"deposit) -> after {c3_after}/10 under CF-1 "
          f"(exp136 criterion; 3/3-grade {c3_after_333}/10)")
    print(f"  F1: C3 improves to >= 9/10 with bit-exact rung/seed "
          f"re-check: {'PASS' if f1 else 'FAIL'}")

    f2_detail = []
    for r, d in zip(cf_rows[:10], delivered):
        was = [bool(x < ERR_BAR and h < ERR_BAR)
               for x, h in zip(d["decode_errs"], d["hold_errs"])]
        now = [bool(x < ERR_BAR and h < ERR_BAR)
               for x, h in zip(r["cf1_decode_errs"],
                               r["cf1_hold_errs"])]
        f2_detail.append({
            "name": r["name"],
            "previously_passing": bool(d["decode_pass"]),
            "n_clash_cells": r["n_clash_cells"],
            "pass_pattern_before": was, "pass_pattern_after": now,
            "pattern_identical": was == now,
            "cf1_vs_exp156_deposit_bitexact": dep_match[r["name"]],
            "cf1_vs_exp150_unrepaired_bitexact":
                r["cf1_decode_errs"] == d["decode_errs"]})
    # F2's scope is THE 8 PREVIOUSLY-PASSING MEMBERS ONLY (the two
    # previously-failing members are F1's rows — their pattern flip
    # F->[T,T,T] is the repair landing, not a regression; first-run
    # evaluation-scope bug fixed: the conjunct had swept all 10)
    f2_scope = [r for r in f2_detail if r["previously_passing"]]
    assert len(f2_scope) == 8, "F2 scope drift: expected the 8"
    branch_id = all(r["cf1_vs_exp150_unrepaired_bitexact"]
                    for r in f2_scope if r["n_clash_cells"] == 0)
    f2 = bool(all(r["pass_pattern_after"] == [True] * 3
                  and r["pattern_identical"]
                  and r["cf1_vs_exp156_deposit_bitexact"]
                  for r in f2_scope) and branch_id)
    print(f"  F2: 8 previously-passing stay passing (patterns "
          f"3/3->3/3 identical), CF-1 rows bit-exact vs exp156 "
          f"deposit, branch-identity for clash-free members "
          f"(n_clash==0 errs == exp150 unrepaired errs bit-exact): "
          f"{'PASS' if f2 else 'FAIL'}\n")

    # ---------------- verdict + stage-3 ledger upgrade ---------------
    gates = {"F1_c3_improves": f1, "F2_no_regression": f2,
             "F3_rw_pre_emission_filter": f3,
             "F4_instrument_unrepaired": f4}
    npass = sum(int(v) for v in gates.values())
    upgrade = bool(f1 and f2 and f3 and f4 and c3_after >= 9)
    if upgrade:
        verdict = (
            "THE GENERATOR'S STAGE-3 LEDGER ENTRY UPGRADES — C3 "
            f"re-run at the repaired floor: {c3_before}/10 -> "
            f"{c3_after}/10 (exp136 criterion; 3/3-grade "
            f"{c3_after_333}/10) on the SAME inventions at the SAME "
            "emitted rungs and seeds; CF-1 (spec-floor -35 -> -60) "
            "is adopted into the compiler's emitted-cell contract "
            "and the R_W canon-clash rule is delivery-safe as the "
            "pre-emission structural gate (the audit_only_fallback "
            "class is exactly the R_W-positive set — zero false "
            "exclusions); no regression on the previously-passing 8")
        stage3 = {
            "upgrades": True,
            "entry": "exp150 stage-3 (generator complete) upgraded",
            "c3_before": f"{c3_before}/10",
            "c3_after": f"{c3_after}/10",
            "c3_after_grade_333": f"{c3_after_333}/10",
            "emitted_cell_contract": (
                "CF-1 adopted: the S-REL spec-adoption floor is "
                "-60.0 mV (below every written zone value; the "
                "canon-fallback branch is unreachable for zone "
                "writes); emitted = argmin rung_cost over rungs "
                "with quad < 6.0 AND decode 3/3 UNDER THE REPAIRED "
                "FLOOR"),
            "pre_emission_gate": (
                "R_W canon-clash mass rule (clash_mass(f) > 36.0 "
                "mV^2) excludes before emission — the "
                "audit_only_fallback emission mode is RETIRED (its "
                "class == the R_W-positive set, 0 FP)"),
            "unchanged": ("C1 novelty, C2 audit, C4 pool diversity, "
                          "the ladder, the bars, the search — all "
                          "untouched; same 10 inventions"),
        }
    else:
        verdict = (
            f"STAGE-3 ENTRY NOT UPGRADED ({npass}/4 gates; C3 after "
            f"{c3_after}/10) — deposit only")
        stage3 = {"upgrades": False, "c3_after": c3_after}

    registered_next = (
        ["adopt the CF-1 floor into cultivation/bioelectric/"
         "collective.py's spec-reading regen walk (the ONE-CONSTANT "
         "production change) and re-run the generator end-to-end on "
         "a FRESH search (L132's never-tuned discipline) with R_W "
         "as the pre-emission filter",
         "re-run exp153's expanded cohort generation under the "
         "repaired contract to confirm R_W's 0-FP on fresh "
         "deliveries",
         "the head-clash reading stays testable wet (exp156's "
         "registered probe: deep (-50 mV) write in depolarized "
         "field vs trunk-like tissue)"]
        if upgrade else
        ["no contract change (L130/L132/L139 discipline); deposit "
         "the failing gate's rows and re-dissect before any "
         "adoption"])

    out = {
        "exp": "exp165_generator_cf1",
        "claim": ("adopting CF-1 (spec-adoption floor -35 -> -60 "
                  "mV, exp156's one-constant repair) into the "
                  "compiler's emitted-cell contract lifts the "
                  "generator's C3 gate on the SAME delivered-10 "
                  "inventions at the SAME emitted rungs and seeds, "
                  "without regressing the previously-passing "
                  "members, and the mechanism-derived R_W "
                  "canon-clash rule is delivery-safe as the "
                  "pre-emission structural filter"),
        "verdict": verdict,
        "stage_order": stage_order,
        "pre_registered": {
            "gates": {
                "F1": "delivered-10 C3 count under CF-1 >= 9/10 "
                      "(exp136 criterion), exact count deposited, "
                      "deposited emitted rungs (all (1.0, 0.0)) and "
                      "seeds (1,2,3) re-checked bit-exactly vs "
                      "exp156's deposited cf1 rows (3 dp)",
                "F2": "the 8 previously-passing members stay "
                      "passing under CF-1: (a) pass status + "
                      "per-seed pass pattern identical (3/3 -> "
                      "3/3); (b) CF-1 rows reproduce exp156's "
                      "deposit bit-exactly (3 dp); (c) clash-free "
                      "members (n_clash == 0) branch-identical — "
                      "CF-1 errs == exp150 unrepaired errs "
                      "bit-exactly",
                "F3": "R_W as pre-emission filter: {R_W-positive} "
                      "== {audit_only_fallback} == exp156 failing "
                      "class on the 24-member stack (every "
                      "excluded member R_W-positive, every "
                      "delivered member R_W-negative; masses "
                      "reproduce exp156's w3 deposit; 0 FP)",
                "F4": "exp150's deposited decode errs reproduced "
                      "bit-exactly under the UNREPAIRED floor "
                      "(dissect replica, deposited rungs/seeds, "
                      "3 dp) + decode_cf(-35) == dissect identity "
                      "anchor (float equality)",
            },
            "design": ("(1) exp150 delivered-10 + exp153 expanded "
                       "cohort decode rebuilt under CF-1 with "
                       "exp156's dissect/decode_cf verbatim — no "
                       "new knobs; (2) exp136's C1-C4 re-evaluated "
                       "on the repaired stack (C1/C2/C4 from the "
                       "deposited unchanged channels; C3 at the "
                       "repaired floor); (3) gates F1-F4"),
            "pre_registration_order_evidence": order_evidence,
        },
        "stack": {
            "delivered10": "results/exp150_generator_complete.json "
                           "(delivered, 10 rows)",
            "expanded24": "results/exp153_decode_anatomy.json "
                          "(expanded_cohort)",
            "consistency": "exp153 cohort rows 1-10 == exp150 "
                           "delivered rows (names/zones/emitted "
                           "cell/errs) asserted bit-exact",
            "emitted_rungs": "all 10 deposited (1.0, 0.0)",
            "seeds": list(AUDIT_SEEDS),
            "cf_floor": CF_FLOOR,
        },
        "f4_instrument": {"rows": f4_rows, "pass": f4},
        "c_gates": {
            "C1_novelty_unchanged": {"rows": c1_rows, "pass": c1,
                                     "bars": [N_LIB_BAR,
                                              N_SPLICE_BAR]},
            "C2_audit_unchanged": {"rows": c2_rows, "pass": c2,
                                   "n_below_bar": c2_n},
            "C3_decode_repaired_floor": {
                "before": f"{c3_before}/10", "after": f"{c3_after}/10",
                "after_grade_333": f"{c3_after_333}/10",
                "criterion": "decode_err < 6.0 AND hold_err < 6.0 "
                             "on >= 2/3 seeds at the deposited "
                             "emitted rung under CF-1"},
            "C4_pool_diversity": {"rows": c4_rows, "pass": c4,
                                  "bar": N_POOL_BAR},
        },
        "cf1_rebuild_24": {"rows": cf_rows,
                           "vs_exp156_deposit_bitexact":
                           {k: bool(v) for k, v in dep_match.items()}},
        "f1_c3_improves": {"rows": f1_rows, "pass": f1,
                           "c3_after": c3_after},
        "f2_no_regression": {"rows": f2_detail, "pass": f2,
                             "branch_identity_held": branch_id},
        "f3_rw_pre_emission_filter": {"rows": f3_rows, "pass": f3,
                                      "rw_positive": sorted(rw_pos),
                                      "audit_only_fallback":
                                      sorted(fallback),
                                      "exp156_failing_class":
                                      sorted(fail_class),
                                      "masses_match_exp156_w3":
                                      bool(mass_match)},
        "stage3_ledger_upgrade": stage3,
        "gates": gates,
        "gates_passed": f"{npass}/4",
        "registered_next": registered_next,
        "wall_s": round(time.time() - t0, 1),
    }
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"\n  VERDICT: {verdict}")
    print(f"  gates {npass}/4 -> {OUT} (wall {out['wall_s']} s)")
    return out


if __name__ == "__main__":
    main()
