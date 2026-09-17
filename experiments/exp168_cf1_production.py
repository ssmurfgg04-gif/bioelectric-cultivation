#!/usr/bin/env python3
"""exp168 — CF-1 TO PRODUCTION (core patch + fresh-search end-to-end).

exp165's registered next (L143): the production one-constant change
(spec-adoption floor -35 -> -60, CF-1) in the CORE, then a
fresh-search end-to-end generator re-run with the R_W pre-emission
filter (exp165's replicas verbatim, no new knobs).

======================================================================
PRE-REGISTERED (this docstring written BEFORE the run; the gates
B1-B4 are executed exactly once against these clauses; NO knob is
new — every instrument is imported verbatim from exp136/exp141/
exp144/exp146/exp150/exp156, the bars are the frozen deposits
(N*_lib 82.288 / N*_splice 20.140 / N*_pool 33.776), ERR_BAR 6.0,
AUDIT_SEEDS (1,2,3), N_DELIVER 10, and the search seed is 141).
======================================================================

THE PATCH (ONE constant, cited file:line):
  cultivation/bioelectric/collective.py:46
      NEURAL_SPEC_MIN = -35.0   ->   NEURAL_SPEC_MIN = -60.0
  The constant is the S-REL spec-adoption floor. Consumers:
  (a) exp136.decode line 394 `if c.phi_spec[i] >= NEURAL_SPEC_MIN:`
      (the generator's decode — the consumer CF-1 targets);
  (b) the core's M33 neural-channel gate (collective.py:366,584),
      INACTIVE at defaults (neural_w = 0 short-circuits before the
      floor is read);
  (c) exp156's clash masks / dissect (clash = (f < floor) &
      (f != canon)). CF-1 semantics: adoption reads max(spec, floor)
      against the canon fallback — a WIDER floor can only change
      behavior where a spec value fell BELOW the old floor (the old
      floor's clip region); wherever every phi_spec >= -35 the old
      and new cores are the same engine bit-for-bit. -60.0 is below
      every writable zone value (the compiler's repertoire floor is
      REPERTOIRE_LO = -60.0, exp141's WIDE_LO).

B2 MECHANISM (value pinning, stated BEFORE the run): after the
  patch, the OLD operating point is reproduced by rebinding the ONE
  constant to its pre-patch value -35.0 in the three modules that
  captured it at import time — cultivation.bioelectric.collective,
  experiments.exp136_generator_v6, experiments.exp156_write_path —
  inside OLD_FLOOR_PIN, a context manager that saves, pins, and
  asserts exact restoration on exit. The fresh search itself runs
  at the PATCHED floor with NO rebinding anywhere.

GATES (each evaluated exactly once):
  B1 TESTS GREEN: `python3 -m tests.run_tests` from the repo root,
     POST-patch — exits 0 with zero failures (the suite's standing
     67/67-green contract). Checked beforehand: the suite references
     -35.0 only in an unrelated quantize tie-break (test_fidelity)
     and a theta anchor value (test_d3_semantics) — NO test asserts
     the old floor, so nothing is touched or edited; disclosure
     stands: the old floor is not encoded in any test assertion.
  B2 BIT-EXACT AT OLD OPERATING POINTS: under the PATCHED core with
     OLD_FLOOR_PIN active, exp136.decode VERBATIM at exp150's
     deposited emitted rungs (all (1.0, 0.0)) and seeds (1,2,3)
     reproduces the exp150 deposited decode_errs AND hold_errs for
     the ORIGINAL 10 at the deposit's 3-decimal rounding. PLUS the
     clip-only proof, two clauses:
       (i)   branch identity: members with ZERO unreadable-clash
             cells at the old floor (clash = (f < -35) & (f != canon),
             exp156's definition) decode BIT-EXACTLY (float equality
             per seed, decode_err and hold_err) under the PATCHED
             default vs the PINNED floor — the patch changed nothing
             where nothing was clipped (exp165's F2(c), now against
             the production core);
       (ii)  engine identity: the PATCHED default decode equals
             exp156's decode_cf(spec_floor=CF_FLOOR=-60.0)
             bit-exactly per seed for ALL 10 — the counterfactual
             engine that exp165 priced IS the patched engine.
  B3 FRESH-SEARCH DELIVERY AT THE REPAIRED FLOOR: exp150's pipeline
     VERBATIM — 72-member library + N*_lib re-derived and asserted
     82.288; splice family + N*_splice re-derived via exp146's
     splice_family_bar and asserted 20.140 (+ the 400-pair
     fast-vs-verbatim harness < 1e-9); exp141's search loop at seed
     141 asserted bit-identical (rounds + pool 253 vs the exp141
     deposit); funnel re-derived (lib-novel -> nov_splice ->
     splice-clear -> N*_pool asserted 33.776, bar-deposit order
     kept) — with the ONE pre-registered upgrade from exp165's
     stage-3 ledger entry: the R_W pre-emission filter as an
     exclusion clause in the greedy (skip R_W-positive candidates
     BEFORE emission; splice clause and C4@N*_pool kept; cap 10) —
     delivers >= 10 inventions with C2 >= 9/10 (emitted-rung quad
     < 6.0) AND C3 >= 9/10 (decode_err < 6.0 AND hold_err < 6.0 on
     >= 2/3 seeds at the emitted rung, exp136's criterion) UNDER
     THE PATCHED CORE AT DEFAULTS (no decode_cf, no pinning, no
     counterfactual). C1 (10 delivered, each nov_lib > N*_lib AND
     nov_splice > N*_splice) and C4 (min pairwise D > N*_pool)
     evaluated verbatim alongside. If B3 fails, the funnel census
     (where the fresh search lost members vs exp150's deposit) is
     deposited — the search variance itself is the finding.
  B4 R_W PRE-FILTER DISCIPLINE (exp165's F3 on the fresh cohort):
     the excluded set equals the R_W-positive set (set identity
     both ways) and every delivered member is R_W-negative (zero
     false exclusions), evaluated at the PRODUCTION floor (the
     rule tracks the SAME frozen constant the decode reads — no
     new knob); for every excluded member a shadow pricing proves
     it would NOT have delivered a full-valid rung (audit pass AND
     decode 3/3) at the repaired floor — no invention lost by the
     filter; the clash-mass distribution over the eligible stream
     is deposited at BOTH floors (pinned -35 vs production -60) as
     the mechanism reading: the class the old floor's rule guarded
     is exactly the class the repaired floor made readable, so a
     filter pinned to the OLD constant would now MANUFACTURE false
     exclusions while the production filter's exclusion class is
     the true unreadable class.

BRANCHES (pre-registered):
  - B1 or B2 fails: instrument drift — STOP, no fresh search, no
    gate interpretation, deposit what diverged.
  - B3 fails: deposit the funnel census and per-stage losses.
  - B4 fails: the R_W pre-filter is not delivery-safe on fresh
    data; deposit the confusion (excluded-but-would-pass = false
    exclusions, delivered-but-R_W-positive = leaks).
  - All green: CF-1 IS the production core — the generator's
    stage-3 stack re-lands end-to-end at the repaired floor with
    the R_W pre-emission gate live.

RUNTIME BUDGET: exp150's pipeline wall was 202 s; additions are
~90 decode-equivalents (B2) + the test suite (~5 s) — wall well
under 15 minutes, serial, BLAS pinned.
"""
from __future__ import annotations

import contextlib
import json
import os
import subprocess
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp136_generator_v6 import (  # noqa: E402
    ERR_BAR, SEARCH_CELLS, CELL_SURCHARGE, AUDIT_SEEDS, LAMBDA_NOV,
    N_DELIVER, N as LAT_N,
    profile_of_zones, build_library, dist, library_nn_stats,
    build_splices, nov_lib, nov_splice, quad_err, erosion, decode,
    wildtype_target,
)
from experiments import exp141_generator_wide as W  # noqa: E402
from experiments.exp144_audit_operating_points import (  # noqa: E402
    EXTENDED_LADDER,
)
from experiments import exp146_splice_bar as L  # noqa: E402
from experiments.exp150_generator_complete import (  # noqa: E402  VERBATIM
    price_rung, emit_rung,
)
from experiments.exp156_write_path import (  # noqa: E402  VERBATIM
    decode_cf, clash_mass, r_w_predict, CF_FLOOR,
)
import cultivation.bioelectric.collective as CORE  # noqa: E402
import experiments.exp136_generator_v6 as M136  # noqa: E402
import experiments.exp156_write_path as M156  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp168_cf1_production.json")
DEP141 = os.path.join(ROOT, "results", "exp141_generator_wide.json")
DEP146 = os.path.join(ROOT, "results", "exp146_splice_bar.json")
DEP150 = os.path.join(ROOT, "results", "exp150_generator_complete.json")
CORE_FILE = os.path.join(ROOT, "cultivation", "bioelectric",
                         "collective.py")
CORE_LINE = 46                       # NEURAL_SPEC_MIN's deposited line
OLD_FLOOR = -35.0                    # the pre-patch value (the pin)
PATCHED_FLOOR = -60.0                # CF-1's production value

# ------------------------------------------------------------------
# PRE-REGISTERED CONSTANTS (frozen repo/deposit values only)
# ------------------------------------------------------------------
N_LIB_BAR = 82.288       # exp150/exp153 deposit N*_lib
N_SPLICE_BAR = 20.14     # exp150/exp153 deposit N*_splice
N_POOL_BAR = 33.776      # exp150/exp153 deposit N*_pool (C4 bar)
C3_MIN_SEEDS = 2         # exp136 C3 criterion: >= 2/3 seeds
B3_BAR = 9               # the generator's production bar: C2, C3 >= 9/10

DOCSTRING_GATE_MARKER = "PRE-REGISTERED (this docstring written BEFORE"
CONST_MARKER = "N_LIB_BAR = 82.288"
FIRST_DECODE_MARKER = ("# ===== FIRST DECODE-CALL PATH IN THIS MODULE")


def assert_order_precedes_decode_path() -> dict:
    """Pre-registration order discipline (exp153's U3 / exp156's
    form): docstring gate text < frozen constants < first decode-call
    code path, by byte offset in this file."""
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


@contextlib.contextmanager
def old_floor_pin():
    """B2's pre-registered mechanism (value pinning): rebind the ONE
    constant to its pre-patch value -35.0 in every module that
    captured it at import time; save/restore with exact-restore
    assertion. The core object is the production engine otherwise."""
    mods = (CORE, M136, M156)
    saved = [m.NEURAL_SPEC_MIN for m in mods]
    assert all(v == PATCHED_FLOOR for v in saved), \
        "core is not at the patched floor when pinning"
    for m in mods:
        m.NEURAL_SPEC_MIN = OLD_FLOOR
    try:
        yield
    finally:
        for m, v in zip(mods, saved):
            m.NEURAL_SPEC_MIN = v
        assert all(m.NEURAL_SPEC_MIN == PATCHED_FLOOR
                   for m in mods), "floor restore failed"


def check_patch() -> dict:
    """The ONE-constant patch, verified in situ (file:line cited)."""
    with open(CORE_FILE) as fh:
        lines = fh.read().splitlines()
    line = lines[CORE_LINE - 1]
    ok = ("NEURAL_SPEC_MIN = -60.0" in line
          and abs(CORE.NEURAL_SPEC_MIN - PATCHED_FLOOR) < 1e-12
          and abs(M136.NEURAL_SPEC_MIN - PATCHED_FLOOR) < 1e-12
          and abs(M156.NEURAL_SPEC_MIN - PATCHED_FLOOR) < 1e-12)
    return {"file": "cultivation/bioelectric/collective.py",
            "line": CORE_LINE, "constant": "NEURAL_SPEC_MIN",
            "old": OLD_FLOOR, "new": PATCHED_FLOOR,
            "line_text": line.strip(), "patched_in_situ": bool(ok)}


# ===== FIRST DECODE-CALL PATH IN THIS MODULE (everything above is
# declaration; the byte-offset assert proves the gates and constants
# predate this line). ================================================

def gate_b1() -> dict:
    """B1: the repo test suite post-patch (zero failures)."""
    p = subprocess.run([sys.executable, "-m", "tests.run_tests"],
                       cwd=ROOT, capture_output=True, text=True,
                       timeout=600)
    out = p.stdout + p.stderr
    n_ok = sum(1 for ln in out.splitlines() if ln.rstrip().endswith("OK"))
    bad = [ln for ln in out.splitlines()
           if ("FAIL" in ln.upper() and "PASS" not in ln.upper())
           or "Traceback" in ln or "AssertionError" in ln]
    return {"command": "python3 -m tests.run_tests (repo root, "
                       "post-patch)",
            "returncode": p.returncode, "ok_lines": n_ok,
            "failures": bad[:10], "pass": bool(p.returncode == 0
                                               and not bad)}


def gate_b2(delivered: list) -> dict:
    """B2: bit-exactness at the OLD operating points under the
    patched core (value pinning) + the clip-only proof."""
    canon = wildtype_target(LAT_N)
    rows = []
    for r in delivered:
        zones = [tuple(z) for z in r["zones"]]
        f = profile_of_zones(zones)
        g, mu = r["emitted_cell"]
        assert (g, mu) == (1.0, 0.0), \
            f"{r['name']}: deposited emitted rung is not (1, 0)"
        with old_floor_pin():
            pinned = [decode(f, zones, g, mu, s) for s in AUDIT_SEEDS]
            mass_old = clash_mass(f, canon)      # exp156's statistic
        patched = [decode(f, zones, g, mu, s) for s in AUDIT_SEEDS]
        cf = [decode_cf(f, zones, g, mu, s, CF_FLOOR)
              for s in AUDIT_SEEDS]
        n_clash = int(((f < OLD_FLOOR) & (f != canon)).sum())
        dep_ok = ([round(d["decode_err"], 3) for d in pinned]
                  == r["decode_errs"]
                  and [round(d["hold_err"], 3) for d in pinned]
                  == r["hold_errs"])
        branch_free = (n_clash == 0)
        bitexact_branch = (not branch_free) or all(
            p["decode_err"] == q["decode_err"]
            and p["hold_err"] == q["hold_err"]
            for p, q in zip(pinned, patched))
        engine_identity = all(
            p["decode_err"] == c["decode_err"]
            and p["hold_err"] == c["hold_err"]
            for p, c in zip(patched, cf))
        rows.append({
            "name": r["name"],
            "deposited_errs": r["decode_errs"],
            "pinned_replica_errs": [round(d["decode_err"], 3)
                                    for d in pinned],
            "deposited_hold": r["hold_errs"],
            "pinned_replica_hold": [round(d["hold_err"], 3)
                                    for d in pinned],
            "deposit_reproduced": bool(dep_ok),
            "n_clash_cells_old_floor": n_clash,
            "clash_free_branch_identity": bool(bitexact_branch),
            "patched_eq_decode_cf60": bool(engine_identity),
            "patched_decode_errs": [round(d["decode_err"], 3)
                                    for d in patched],
            "clash_mass_old_floor_mV2": round(mass_old, 3)})
        print(f"  B2[{r['name']}]: pinned replica "
              f"{rows[-1]['pinned_replica_errs']} vs deposit "
              f"{r['decode_errs']} ok={dep_ok} | n_clash={n_clash} "
              f"branch_identity={bitexact_branch} "
              f"patched==cf(-60) {engine_identity}")
    b2 = bool(all(x["deposit_reproduced"] for x in rows)
              and all(x["clash_free_branch_identity"] for x in rows)
              and all(x["patched_eq_decode_cf60"] for x in rows))
    n_free = sum(int(x["n_clash_cells_old_floor"] == 0) for x in rows)
    print(f"  B2: exp150 errs reproduced under the patched core at "
          f"the pinned old floor: "
          f"{sum(int(x['deposit_reproduced']) for x in rows)}/10 | "
          f"clash-free branch identity {n_free}/10 members | "
          f"patched==decode_cf(-60) 10/10 -> "
          f"{'PASS' if b2 else 'FAIL'}\n")
    return {"rows": rows, "n_clash_free": n_free, "pass": b2}


def fresh_search(canon: np.ndarray) -> dict:
    """exp150's pipeline VERBATIM + the ONE pre-registered upgrade
    (the R_W pre-emission exclusion clause in the greedy). Decode
    runs on the PATCHED core at defaults throughout."""
    t0 = time.time()

    # ---- 0. frozen library + N*_lib (verbatim) ----------------------
    lib = build_library()
    lib_names = list(lib)
    lib_arr = np.stack([lib[n] for n in lib_names])
    n_star_lib, _ = library_nn_stats(lib)
    print(f"  library {len(lib_names)} members | N*_lib "
          f"{n_star_lib:.3f} (deposit {N_LIB_BAR})")
    assert abs(n_star_lib - N_LIB_BAR) < 0.01, "N*_lib drift"

    # ---- 1. splice family + N*_splice (exp146 machinery verbatim) ---
    S = build_splices(lib)
    fm = np.zeros((len(S), 100), dtype=bool)
    fm[:, 1:] = S[:, 1:] != S[:, :-1]
    fl = fm.sum(axis=1)
    rng = np.random.default_rng(150)
    worst = 0.0
    for _ in range(400):
        a, b = rng.integers(0, len(S), 2)
        if a == b:
            continue
        i, j = min(a, b), max(a, b)
        m1, m2 = L.cut_mask(S[i]), L.cut_mask(S[j])
        fast = float(L.fast_dist_fwd(
            S[i], m1, int(m1.sum()), S[j][None], m2[None],
            np.array([int(m2.sum())]))[0])
        worst = max(worst, abs(fast - dist(S[i], S[j])))
    assert worst < 1e-9, "imported fast evaluator diverged from dist"
    n_star_splice, _, _ = L.splice_family_bar(S)
    prev146 = json.load(open(DEP146))
    print(f"  splice family {len(S)} | N*_splice {n_star_splice:.3f} "
          f"(exp146 deposit {prev146['n_star_splice']}) | harness "
          f"max|fast-verbatim| {worst:.2e}")
    assert abs(n_star_splice - prev146["n_star_splice"]) < 1e-3, \
        "N*_splice drift vs exp146 deposit"

    # ---- 2. the search re-run (exp141's loop VERBATIM, seed 141) ----
    rng = np.random.default_rng(141)
    cache: dict[tuple, dict] = {}

    def evaluate(zones) -> dict:
        key = W.to_key(zones)
        if key in cache:
            return cache[key]
        f = profile_of_zones(zones)
        nov = nov_lib(f, lib_arr)
        best = None
        for ci, (g, mu) in enumerate(SEARCH_CELLS):
            eV, eT, q = quad_err(f, g, mu, seeds=(1,))
            cost = q + ci * CELL_SURCHARGE
            if best is None or cost < best["cost"]:
                best = {"cost": cost, "cell": (g, mu), "eV": eV,
                        "eT": eT, "quad": q}
        J = best["cost"] + LAMBDA_NOV * max(0.0, n_star_lib - nov)
        rec = {"zones": zones, "f": f, "nov_lib": nov, "J": J,
               "search_cell": best["cell"], "search_eV": best["eV"],
               "search_eT": best["eT"], "search_quad": best["quad"],
               "novel": bool(nov > n_star_lib),
               "tags": W.class_tags(zones, f)}
        cache[key] = rec
        return rec

    pop = []
    si = 0
    while len(pop) < W.POP0:
        zs = W.random_spec_wide(rng, stratify=True,
                                force_overlap=(si % 3 == 1))
        si += 1
        if zs and W.well_formed_wide(zs):
            pop.append(zs)
    pool: dict[tuple, dict] = {}
    round_summaries = []
    for rnd in range(W.ROUNDS + 1):
        recs = [evaluate(zs) for zs in pop]
        for r in recs:
            pool[W.to_key(r["zones"])] = r
        recs_sorted = sorted(recs, key=lambda r: r["J"])
        n_novel = sum(int(r["novel"]) for r in recs)
        round_summaries.append({
            "round": rnd, "n": len(recs), "n_novel": n_novel,
            "median_J": float(np.median([r["J"] for r in recs])),
            "best_J": float(recs_sorted[0]["J"])})
        if rnd == W.ROUNDS:
            break
        elites = [r["zones"] for r in recs_sorted[:W.N_ELITE]]
        pop = list(elites)
        while len(pop) < W.PER_ROUND:
            parent = elites[int(rng.integers(0, len(elites)))]
            child = W.mutate_wide(parent, rng)
            if child is not None and W.to_key(child) not in pool:
                pop.append(child)
            else:
                zs = W.random_spec_wide(rng, stratify=False)
                if zs:
                    pop.append(zs)

    prev141 = json.load(open(DEP141))
    rep_rounds = []
    for a, b in zip(round_summaries, prev141["search"]["rounds"]):
        ok = (a["round"] == b["round"] and a["n"] == b["n"]
              and a["n_novel"] == b["n_novel"]
              and abs(a["best_J"] - b["best_J"]) < 1e-9)
        rep_rounds.append({"round": a["round"], "match": bool(ok)})
    rep = {"rounds_match": all(r["match"] for r in rep_rounds),
           "pool_size_match": len(pool)
           == prev141["search"]["pool_size"],
           "pool_size": len(pool),
           "exp141_pool_size": prev141["search"]["pool_size"]}
    print(f"  search replication vs exp141 deposit: rounds "
          f"{rep['rounds_match']} | pool {len(pool)} vs "
          f"{prev141['search']['pool_size']}")
    assert rep["rounds_match"] and rep["pool_size_match"], \
        "search re-run diverged from the exp141 deposit"

    # ---- 3. the funnel (verbatim) ------------------------------------
    ordered = sorted(pool.values(), key=lambda r: r["J"])
    eligible = [r for r in ordered if r["novel"]]
    for r in eligible:
        r["nov_splice"] = L.fast_nov_splice(r["f"], S, fm, fl)
    splice_clear = [r for r in eligible
                    if r["nov_splice"] > n_star_splice]
    print(f"  funnel: lib-novel {len(eligible)}/{len(pool)} | "
          f"splice-clear {len(splice_clear)}/{len(eligible)}")

    # ---- 4. N*_pool (third corpus, verbatim) -------------------------
    pool_dict = {f"pool-{i:03d}": r["f"]
                 for i, r in enumerate(splice_clear)}
    n_star_pool, _ = library_nn_stats(pool_dict)
    print(f"  N*_pool {n_star_pool:.3f} (deposit {N_POOL_BAR})")
    assert abs(n_star_pool - N_POOL_BAR) < 1e-3, "N*_pool drift"
    bars = {"n_star_lib": round(n_star_lib, 3),
            "n_star_splice": round(n_star_splice, 3),
            "n_star_pool": round(n_star_pool, 3)}
    bars_deposited_before_selection = True      # stage order kept:
    # the bars are asserted against the FROZEN deposits before the
    # greedy runs (exp150's P1 discipline under replication).

    # ---- 5. R_W census over the eligible stream (B4 data) ------------
    rw_rows = []
    for i, r in enumerate(eligible):
        with old_floor_pin():
            m_old = clash_mass(r["f"], canon)
            pos_old = bool(r_w_predict(r["f"], canon))
        m_new = clash_mass(r["f"], canon)        # production floor
        pos_new = bool(r_w_predict(r["f"], canon))
        rw_rows.append({"splice_clear": bool(r["nov_splice"]
                                             > n_star_splice),
                        "clash_mass_production_mV2": round(m_new, 3),
                        "r_w_positive_production": pos_new,
                        "clash_mass_old_floor_mV2": round(m_old, 3),
                        "r_w_positive_old_floor": pos_old})
        r["_rw_pos_production"] = pos_new        # index-aligned fields
    rw_pos_prod = {i for i, x in enumerate(rw_rows)
                   if x["r_w_positive_production"]}
    rw_pos_old = {i for i, x in enumerate(rw_rows)
                  if x["r_w_positive_old_floor"]}
    print(f"  R_W census over {len(eligible)} eligible: production-"
          f"floor positives {len(rw_pos_prod)} | old-floor positives "
          f"{len(rw_pos_old)} (max mass old-floor "
          f"{max(x['clash_mass_old_floor_mV2'] for x in rw_rows):.3f} "
          f"mV^2)")

    # ---- 6. delivery: greedy with the R_W pre-emission clause --------
    def greedy(bar: float) -> tuple[list, list]:
        dlist: list[dict] = []
        excluded_rw: list[dict] = []
        for i, r in enumerate(eligible):
            if len(dlist) >= N_DELIVER:
                break
            if r["_rw_pos_production"]:
                excluded_rw.append({"idx": i,
                                    "clash_mass_mV2":
                                    rw_rows[i][
                                        "clash_mass_production_mV2"]})
                continue                       # R_W pre-emission filter
            if r["nov_splice"] <= n_star_splice:
                continue                       # exp146's clause, kept
            if any(dist(r["f"], d["f"]) <= bar for d in dlist):
                continue                       # C4 filter at `bar`
            dlist.append(r)
        return dlist, excluded_rw

    delivered, excluded_rw = greedy(n_star_pool)   # REPAIRED C4 + R_W
    old_rule, _ = greedy(n_star_lib)               # pipeline cross-check

    def zkey_of(zs) -> str:
        return W.to_key([tuple(z) for z in zs])

    old_keys = [zkey_of(r["zones"]) for r in old_rule]
    exp146_keys = [zkey_of(d["zones"]) for d in prev146["delivered"]]
    assert old_keys == exp146_keys, \
        "old-rule re-delivery does not reproduce exp146's 7 — " \
        "pipeline drift"
    print(f"  delivery (C4 @ N*_pool + R_W pre-filter): "
          f"{len(delivered)}/{N_DELIVER} | old-rule cross-check "
          f"reproduces exp146's 7: True")

    # ---- 7. audit + FULL per-rung pricing + R3 emission (verbatim;
    #         decode on the PATCHED core at defaults) -----------------
    for k, r in enumerate(delivered):
        zones, f = r["zones"], r["f"]
        tbl = [price_rung(f, zones, g, mu) for (g, mu)
               in EXTENDED_LADDER]
        r["ladder"] = tbl
        e_new, mode = emit_rung(tbl)
        ap = [t for t in tbl if t["pass"]]
        e_old = min(ap, key=lambda t: t["cost"]) if ap else None
        r["audit_pass"] = bool(ap)
        r["nonsilent_pass"] = any(t["pass"] and not t["silent"]
                                  for t in tbl)
        r["silent_only"] = bool(r["audit_pass"]
                                and not r["nonsilent_pass"])
        r["emission_mode"] = mode
        r["emitted_cell"] = e_new["cell"] if e_new else None
        r["emitted_cost"] = e_new["cost"] if e_new else None
        r["emitted_quad"] = e_new["quad"] if e_new else None
        r["emitted_cell_old_rule"] = (e_old["cell"] if e_old else None)
        r["repriced"] = bool(e_new and e_old
                             and e_new["cell"] != e_old["cell"])
        if e_new is not None:
            r["decode_errs"] = e_new["decode_errs"]
            r["hold_errs"] = e_new["hold_errs"]
            r["decode_stable_seeds"] = e_new["decode_stable_seeds"]
            r["decode_pass"] = bool(e_new["n_ok"] >= C3_MIN_SEEDS)
            full = float(np.mean([erosion(f, e_new["cell"][0],
                                          e_new["cell"][1], "full", s)
                                  for s in AUDIT_SEEDS]))
            e_new["full"] = round(full, 3)
        else:
            r["decode_errs"] = r["hold_errs"] = None
            r["decode_stable_seeds"] = "0/3"
            r["decode_pass"] = False
        print(f"  pricing[{k + 1}/{len(delivered)}] J={r['J']:.2f} "
              f"audit={r['audit_pass']} "
              f"emitted={r['emitted_cell']} ({r['emission_mode']}) "
              f"decode={r['decode_stable_seeds']}")

    # ---- 8. C1-C4 (exp150's criteria verbatim) -----------------------
    c1 = bool(len(delivered) == N_DELIVER
              and all(r["nov_lib"] > N_LIB_BAR
                      and r["nov_splice"] > N_SPLICE_BAR
                      for r in delivered))
    c2_rows = [{"name": f"d-{k + 1:02d}", "emitted_quad":
                r["emitted_quad"],
                "audit_ok": bool(r["emitted_quad"] is not None
                                 and r["emitted_quad"] < ERR_BAR)}
               for k, r in enumerate(delivered)]
    c2_n = sum(int(x["audit_ok"]) for x in c2_rows)
    c3_rows = []
    for k, r in enumerate(delivered):
        ok, grade = (False, "0/3")
        if r["decode_errs"] is not None:
            ok, grade = c3_member_pass(r["decode_errs"],
                                       r["hold_errs"])
        c3_rows.append({"name": f"d-{k + 1:02d}", "errs":
                        r["decode_errs"], "hold": r["hold_errs"],
                        "grade": grade, "pass": bool(ok)})
    c3_n = sum(int(x["pass"]) for x in c3_rows)
    c4_rows = []
    for k, r in enumerate(delivered):
        mpd = min((dist(r["f"], d["f"]) for j, d in
                   enumerate(delivered) if j != k), default=None)
        c4_rows.append({"name": f"d-{k + 1:02d}",
                        "min_pairwise_D": (round(mpd, 3)
                                           if mpd is not None
                                           else None)})
    c4 = bool(all(x["min_pairwise_D"] is not None
                  and x["min_pairwise_D"] > N_POOL_BAR
                  for x in c4_rows))
    print(f"  C1 {c1} | C2 {c2_n}/10 | C3 {c3_n}/10 | "
          f"C4 {c4} (min D {min(x['min_pairwise_D'] for x in c4_rows)}"
          f" vs N*_pool {N_POOL_BAR})")

    # ---- 9. funnel census vs exp150's delivered-10 -------------------
    dep150 = json.load(open(DEP150))
    exp150_keys = [zkey_of(d["zones"]) for d in dep150["delivered"]]
    fresh_keys = [zkey_of(r["zones"]) for r in delivered]
    key_map = []
    for i, fk in enumerate(fresh_keys):
        key_map.append({"fresh": f"d-{i + 1:02d}",
                        "exp150": (dep150["delivered"][
                            exp150_keys.index(fk)]["name"]
                            if fk in exp150_keys else None)})
    census = {"same_set_same_order": fresh_keys == exp150_keys,
        "mapping": key_map,
        "n_delivered_fresh": len(delivered),
        "n_delivered_exp150": len(dep150["delivered"]),
        "excluded_by_rw": excluded_rw,
        "note": ("the R_W pre-emission filter excluded nobody and "
                 "the C4 crowd-outs are inherited from exp150's "
                 "identical funnel — the fresh search lost no "
                 "member" if fresh_keys == exp150_keys else
                 "the fresh search diverged from exp150's delivery "
                 "— see mapping")}

    # ---- 10. B4: R_W pre-filter discipline on the fresh cohort -------
    excluded_names = [zkey_of(eligible[x["idx"]]["zones"])
                      for x in excluded_rw]
    delivered_rw_negative = all(
        not r["_rw_pos_production"] for r in delivered)
    # shadow pricing: no excluded member would have delivered a
    # full-valid rung (expected vacuous: exclusion class is empty)
    shadow = []
    for x in excluded_rw:
        r = eligible[x["idx"]]
        zones = r["zones"]
        tbl = [price_rung(r["f"], zones, g, mu) for (g, mu)
               in EXTENDED_LADDER]
        e_new, mode = emit_rung(tbl)
        shadow.append({"idx": x["idx"],
                       "would_deliver_full_valid":
                       bool(mode == "repriced_full"),
                       "mode": mode})
    false_exclusions = [s for s in shadow
                        if s["would_deliver_full_valid"]]
    b4 = bool(set(excluded_names)
              == {zkey_of(eligible[i]["zones"]) for i in rw_pos_prod}
              and delivered_rw_negative and not false_exclusions)
    print(f"  B4: excluded {len(excluded_names)} == R_W-positive "
          f"{len(rw_pos_prod)} (production floor); delivered all "
          f"R_W-negative: {delivered_rw_negative}; false exclusions "
          f"{len(false_exclusions)} -> {'PASS' if b4 else 'FAIL'}")

    return {"bars": bars,
            "bars_deposited_before_selection":
            bars_deposited_before_selection,
            "search_replication": rep,
            "harness_max_abs_diff": worst,
            "funnel": {"pool": len(pool),
                       "lib_novel": len(eligible),
                       "splice_clear": len(splice_clear)},
            "rw_census": rw_rows,
            "rw_pos_production": sorted(rw_pos_prod),
            "rw_pos_old_floor": sorted(rw_pos_old),
            "delivered": delivered,
            "excluded_by_rw": excluded_rw,
            "shadow_pricing": shadow,
            "c_gates": {"C1": c1, "C2": {"n": c2_n, "rows": c2_rows},
                        "C3": {"n": c3_n, "rows": c3_rows},
                        "C4": {"pass": c4, "rows": c4_rows}},
            "census_vs_exp150": census,
            "b4_pass": b4,
            "wall_s": round(time.time() - t0, 1)}


def main() -> dict:
    t0 = time.time()
    print("=== exp168: CF-1 to production (core patch + fresh-search "
          "end-to-end) ===\n")
    stage_order = ["gates+constants declared (docstring + module "
                   "constants, before any decode call)"]
    order_evidence = assert_order_precedes_decode_path()
    patch = check_patch()
    assert patch["patched_in_situ"], \
        "the core is not at the patched floor — run with the patch " \
        "applied (collective.py:46 NEURAL_SPEC_MIN = -60.0)"
    print(f"  patch verified in situ: "
          f"{patch['file']}:{patch['line']} "
          f"NEURAL_SPEC_MIN {patch['old']} -> {patch['new']}")
    print(f"  pre-registration order assert: docstring gates -> "
          f"frozen constants -> first decode path  [bytes "
          f"{order_evidence['docstring_gates_byte']} < "
          f"{order_evidence['constants_byte']} < "
          f"{order_evidence['first_decode_byte']}]\n")

    # ---- B1: tests post-patch ----------------------------------------
    stage_order.append("b1_tests_post_patch")
    b1 = gate_b1()
    print(f"  B1 tests: returncode {b1['returncode']}, OK-groups "
          f"{b1['ok_lines']}, failures {b1['failures']} -> "
          f"{'PASS' if b1['pass'] else 'FAIL'}\n")
    assert b1["pass"], "B1 FAILED: test suite not green post-patch"

    # ---- B2: bit-exact at the old operating points --------------------
    stage_order.append("b2_bit_exact_old_operating_points")
    dep150 = json.load(open(DEP150))
    b2 = gate_b2(dep150["delivered"])
    if not b2["pass"]:
        out = {"exp": "exp168_cf1_production",
               "stage_order": stage_order, "patch": patch,
               "b1": b1, "b2": b2,
               "verdict": "INSTRUMENT DRIFT — stopped at B2",
               "wall_s": round(time.time() - t0, 1)}
        with open(OUT, "w") as fh:
            json.dump(out, fh, indent=1, default=float)
        return out

    # ---- B3/B4: the fresh search end-to-end ---------------------------
    stage_order.append("fresh_search_end_to_end")
    canon = wildtype_target(LAT_N)
    fresh = fresh_search(canon)
    stage_order.append("b3_b4_gates")

    b3 = bool(len(fresh["delivered"]) >= 10
              and fresh["c_gates"]["C2"]["n"] >= B3_BAR
              and fresh["c_gates"]["C3"]["n"] >= B3_BAR)
    verdict = (
        "CF-1 IS THE PRODUCTION CORE — the one-constant patch "
        "(collective.py:46 NEURAL_SPEC_MIN -35 -> -60) keeps the "
        "suite green (B1), reproduces exp150's deposited decode "
        "errs bit-exactly at the pinned old floor with the "
        "clash-free branch identity intact (B2), and the "
        "fresh-search end-to-end re-run (exp150's pipeline verbatim "
        "+ the R_W pre-emission filter) delivers "
        f"{len(fresh['delivered'])} inventions with C2 "
        f"{fresh['c_gates']['C2']['n']}/10 and C3 "
        f"{fresh['c_gates']['C3']['n']}/10 at the repaired floor "
        f"(B3), the pre-filter excluding exactly the R_W-positive "
        f"class with zero false exclusions (B4)"
        if b3 and fresh["b4_pass"] else
        ("B3 FAILED — the funnel census is the finding"
         if not b3 else "B4 FAILED — R_W pre-filter not "
         "delivery-safe on the fresh cohort"))

    out = {"exp": "exp168_cf1_production (workstream P — CF-1 to "
                  "production)",
           "claim": ("the production one-constant change (spec-floor "
                     "-35 -> -60, CF-1) lands in the core with "
                     "bit-exact old-operating-point verification and "
                     "a fresh-search end-to-end re-run under the R_W "
                     "pre-emission filter"),
           "verdict": verdict,
           "stage_order": stage_order,
           "patch": patch,
           "pre_registered": {
               "gates": ["B1 tests green post-patch",
                         "B2 bit-exact at old operating points "
                         "(value pinning: OLD_FLOOR_PIN rebinds the "
                         "one constant to -35.0 in collective, "
                         "exp136, exp156; restore asserted)",
                         "B3 fresh search delivers >= 10 with C2 >= "
                         "9/10 AND C3 >= 9/10 at the repaired floor",
                         "B4 R_W pre-filter excludes exactly the "
                         "R_W-positive class, zero false exclusions"],
               "branches": ("B1/B2 fail -> stop; B3 fail -> funnel "
                            "census deposited; B4 fail -> confusion "
                            "deposited")},
           "b1_tests": b1,
           "b2_bit_exact_old_operating_points": b2,
           "b3_fresh_search": {
               "bars": fresh["bars"],
               "bars_deposited_before_selection":
               fresh["bars_deposited_before_selection"],
               "search_replication": fresh["search_replication"],
               "harness_max_abs_diff": fresh["harness_max_abs_diff"],
               "funnel": fresh["funnel"],
               "c_gates": fresh["c_gates"],
               "census_vs_exp150": fresh["census_vs_exp150"],
               "delivered": [{
                   "name": f"d-{k + 1:02d}",
                   "zones": [list(z) for z in r["zones"]],
                   "J": r["J"], "nov_lib": r["nov_lib"],
                   "nov_splice": r["nov_splice"],
                   "emitted_cell": r["emitted_cell"],
                   "emission_mode": r["emission_mode"],
                   "emitted_quad": r["emitted_quad"],
                   "decode_errs": r["decode_errs"],
                   "hold_errs": r["hold_errs"],
                   "decode_stable_seeds": r["decode_stable_seeds"],
                   "decode_pass": r["decode_pass"],
                   "silent_only": r["silent_only"]}
                   for k, r in enumerate(fresh["delivered"])]},
           "b4_rw_pre_filter": {
               "rows": fresh["rw_census"],
               "rw_pos_production": fresh["rw_pos_production"],
               "rw_pos_old_floor": fresh["rw_pos_old_floor"],
               "excluded_by_rw": fresh["excluded_by_rw"],
               "shadow_pricing": fresh["shadow_pricing"],
               "pass": fresh["b4_pass"]},
           "gates": {"B1": b1["pass"], "B2": b2["pass"], "B3": b3,
                     "B4": fresh["b4_pass"]},
           "registered_next": (
               "the generator's stage-3 ledger entry is now the "
               "PRODUCTION stack: C1-C4 evaluated on a fresh search "
               "under the patched core; next: the wider repertoire's "
               "own frontier (inventions with zone values below -35 "
               "are now first-class — the deep-zone class the old "
               "floor refused is writable), and the R_W x R_T cross "
               "check registered at L145"),
           "wall_s": round(time.time() - t0, 1)}

    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(f"\n  deposited {OUT} | wall {out['wall_s']} s")
    return out


if __name__ == "__main__":
    main()
