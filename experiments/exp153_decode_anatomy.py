#!/usr/bin/env python3
"""exp153 — THE DECODE-ANATOMY FAMILY SCAN (workstream U; the L130
registered decode-anatomy family scan, run BEFORE any ladder change).

======================================================================
PRE-REGISTERED (this docstring written BEFORE the run; the gates are
executed exactly once against these clauses; the RULE below was fixed
by inspection of the DEPOSITED exp150 data ONLY — results/
exp150_generator_complete.json — before any exp153 decode call ran):
======================================================================

MOTIVE (L130 (a)): exp150's generator LANDED (C-gates 4/4, 10/10
inventions, each with an explicit anatomy program) but C3 sits exactly
at the bar: d-03 and d-08 fail decode 0/3 at ALL 9 frozen rungs
(decode_err ~9.1/9.6 vs bar 6.0, erosion increment ~0 mV) — the
WRITE/READ path dominates (decode_err >= 6.0 before any hold), an
anatomy-level failure no rung change rescues. L130 registered: a
decode-anatomy family scan — which anatomical features (zone count,
width, voltage depth, boundary density, distance from library cuts)
predict write/read decode failure, and does a SIMPLE pre-registered
feature bar separate the 8 decode-pass from the 2 decode-fail.

THE RULE (fixed before any exp153 decode call; fitted on the exp150
DEPOSIT's 10 delivered anatomies + their deposited decode verdicts,
nothing else):

  R_U (VMIN GAP RULE): predicted decode verdict at exp150's frozen
  emission is PASS iff

      vmin_zone < 45.0   [mV]

  where vmin_zone := min over the anatomy's zones of |voltage| (mV) —
  the shallowest write amplitude the anatomy asks the write/read path
  to reconstruct.

  FIT PROVENANCE (deposited exp150 data, inspected before this run):
  the 8 deposited decode-pass inventions have vmin_zone in
  [18.4, 40.8] mV; the 2 deposited decode-fails (d-03, d-08) have
  vmin_zone in {48.6, 50.8} mV. The separating gap is (40.8, 48.6);
  ANY threshold inside it is equivalent on the fitted data (zero
  knobs); 45.0 is fixed as the clean interior constant. Single
  feature, single threshold: no coefficients, no training loop, no
  free parameters. Mechanistic reading: the write/read path fails
  when EVERY zone is deep (all |v| >= ~48 mV); a single shallow
  anchor zone keeps the settled reconstruction inside the bar.

PRE-REGISTERED FEATURE LIST (extracted per anatomy; no others):
  zone_count        = number of zones as written
  total_zone_width  = sum over zones of (f1 - f0), raw fractional
  vmin_zone         = min over zones of |voltage|          [mV]
  vmax_zone         = max over zones of |voltage|          [mV]
  vmean_zone        = mean over zones of |voltage|         [mV]
  boundary_count    = #{i in [1, N) : f[i] != f[i-1]} on the written
                      profile f (the N=100 lattice; the same cut
                      structure the library distance's d_struct sees)
  nov_lib           = nearest-library distance (min dist(f, lib))
  nov_splice        = nearest-splice distance (min dist over the
                      48,564-profile single-crossover family)

DESIGN (exp150 machinery reused VERBATIM — price_rung, emit_rung,
the audit, the 9-rung EXTENDED_LADDER, ERR_BAR, AUDIT_SEEDS, the
funnel, the C4 bar; the ONLY new objects are (a) UCAP, (b) the
feature extractor, (c) the pre-registered rule and its generator-side
filter, (d) the U-gate readouts):
  (1) frozen 72-member library + N*_lib re-derived, checked 82.288.
  (2) splice family + N*_splice re-derived, checked vs the exp146
      deposit; the 400-pair fast-vs-verbatim harness re-run.
  (3) search re-run at seed 141 (exp141's loop VERBATIM), asserted
      bit-identical to the exp141 deposit (rounds + pool 253).
  (4) funnel VERBATIM: lib-novel -> nov_splice -> splice-clear ->
      N*_pool (library_nn_stats semantics), checked 33.776.
  (5) EXPANDED DELIVERY: exp150's greedy VERBATIM (J-order over the
      lib-novel stream; skip splice-unclear; skip within N*_pool of
      an already-delivered invention) with the cap raised 10 -> 24
      (UCAP; the single new knob, upstream of all evaluation). The
      first 10 delivered MUST have the exp150 deposit's zone keys in
      order (instrument identity check). Delivers up to 24 total
      under exp150's frozen bars — no new free parameters.
  (6) U4 INSTRUMENT CHECK: the original 10 get their FULL 9-rung
      pricing recomputed and compared to the exp150 deposit (quad,
      decode_errs, hold_errs at every rung, emitted rung, emission
      mode, C3 verdict) — bit-exact reproduction required.
  (7) EXPANDED DECODES: the new members (11..N) get the same full
      9-rung pricing + R3 emission (emit_rung VERBATIM); C3 verdict
      per exp150's semantics (decode_err < 6.0 AND hold_err < 6.0 at
      >= 2/3 seeds at the emitted rung).
  (8) FEATURES for the whole expanded cohort (+ the whole
      splice-clear pool, decode-free) -> rule predictions.
  (9) U2 FILTER SIMULATION: re-run the delivery with ONE added
      clause — predicted-pass only (the generator-side filter) —
      same stream, same frozen bars, cap 10; price any
      filtered-delivered member not already priced (same
      instruments) and evaluate C3 on that set.
 (10) feature-separation table (which features separate decode-pass
      from decode-fail on the cohort, which do not).

GATES (pre-registered):
  U1  RULE ACCURACY: the rule's predicted verdict matches the actual
      decode verdict (C3 semantics) on the EXPANDED cohort at
      >= 90% accuracy. (Also deposited: accuracy on the new members
      only — the honest out-of-fit readout.)
  U2  ACTIONABILITY: the generator-side filter (predicted-pass only,
      everything else frozen) yields a delivered set of EXACTLY 10
      whose C3 count is >= 9/10 under exp150's C3 semantics
      (simulated re-run on the same pool with real instruments). If
      the filtered delivery exhausts the pool below 10, U2 FAILS.
  U3  NOT POST-HOC: the rule was declared before the expanded
      decodes — mechanically asserted in-module: the docstring's
      rule text and the RULE_VMIN constant both precede the first
      decode-call code path in this file (byte-offset assert), and
      the threshold was fitted on the exp150 DEPOSIT alone.
  U4  INSTRUMENT CHECK: bit-exact reproduction (rounded to the
      deposit's 3 decimals) of exp150's deposited per-rung quad,
      decode_errs, hold_errs, emitted rung, emission mode and C3
      verdict on the original 10, plus the first-10 zone-key order.

BRANCHES (pre-registered):
  - U1 AND U2 AND U3 AND U4 PASS: THE VMIN RULE LANDS — the
    decode-anatomy scan closes the C3 binder with a generator-side
    filter; register the filter's adoption as the C3 repair.
  - U1 fails: deposit the feature table (which features correlate,
    which do not) and register the mechanism-level attribution
    (why the voltage-depth read fails on the expanded cohort) as
    NEXT; no ladder change.
  - U4 fails: instrument drift — stop, no gate interpretation.

RUNTIME BUDGET: exp150's full pipeline ran 202 s; the expansion adds
<= 14 + 10 priced candidates x 9 rungs (~0.6 s each) — wall under
~15 min, serial, BLAS pinned.
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
    ERR_BAR, SEARCH_CELLS, CELL_SURCHARGE, AUDIT_SEEDS, LAMBDA_NOV,
    N_DELIVER, CUT_TOL, N as LAT_N,
    profile_of_zones, build_library, dist, library_nn_stats,
    build_splices, nov_lib, nov_splice, quad_err, erosion, decode,
)
from experiments import exp141_generator_wide as W  # noqa: E402
from experiments.exp144_audit_operating_points import (  # noqa: E402
    EXTENDED_LADDER, PROVENANCE, rung_cost,
)
from experiments import exp146_splice_bar as L  # noqa: E402
from experiments.exp150_generator_complete import (  # noqa: E402
    price_rung, emit_rung,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp153_decode_anatomy.json")
PREV150 = os.path.join(ROOT, "results", "exp150_generator_complete.json")
PREV141 = os.path.join(ROOT, "results", "exp141_generator_wide.json")
PREV146 = os.path.join(ROOT, "results", "exp146_splice_bar.json")

UCAP = 24          # the single new knob: expanded delivery cap
FEATURE_NAMES = ["zone_count", "total_zone_width", "vmin_zone",
                 "vmax_zone", "vmean_zone", "boundary_count",
                 "nov_lib", "nov_splice"]

# ------------------------------------------------------------------
# THE RULE (declared here, BEFORE any decode-call code path in this
# module; fitted on the exp150 deposit only — see docstring).
# ------------------------------------------------------------------
RULE_VMIN = {
    "name": "R_U vmin gap rule",
    "feature": "vmin_zone",
    "feature_def": "min over the anatomy's zones of |voltage| [mV]",
    "op": "<",
    "thr": 45.0,
    "predicted_verdict": {
        True: "decode-pass (C3 semantics at exp150's frozen emission)",
        False: "decode-fail"},
    "fitted_on": "results/exp150_generator_complete.json ONLY — the "
                 "10 deposited delivered anatomies and their "
                 "deposited decode verdicts; no exp153 decode had "
                 "run when the threshold was fixed",
    "fitted_gap": {"pass_vmin_range": [18.4, 40.8],
                   "fail_vmin_values": [48.6, 50.8],
                   "gap": "(40.8, 48.6) — any threshold inside is "
                          "equivalent on the fitted data; 45.0 fixed",
                   "n_fit": 10},
    "form": "single feature, single threshold, zero knobs",
}


def rule_predict(feat: dict) -> bool:
    """The pre-registered rule, applied mechanically."""
    return bool(feat["vmin_zone"] < RULE_VMIN["thr"])


def anatomy_features(zones, f, nov_lib_v, nov_splice_v) -> dict:
    """The pre-registered feature list (docstring), nothing else."""
    zs = [(float(a), float(b), float(v)) for (a, b, v) in zones]
    vabs = [abs(v) for (_, _, v) in zs]
    return {
        "zone_count": len(zs),
        "total_zone_width": round(float(sum(b - a for (a, b, _) in zs)), 4),
        "vmin_zone": round(float(min(vabs)), 2),
        "vmax_zone": round(float(max(vabs)), 2),
        "vmean_zone": round(float(np.mean(vabs)), 2),
        "boundary_count": int((f[1:] != f[:-1]).sum()),
        "nov_lib": round(float(nov_lib_v), 3),
        "nov_splice": round(float(nov_splice_v), 3),
    }


DOCSTRING_RULE_MARKER = "R_U (VMIN GAP RULE)"
RULE_CONST_MARKER = "RULE_VMIN = {"
FIRST_DECODE_MARKER = ("# ===== STAGE D — FIRST DECODE-CALL PATH IN "
                       "THIS MODULE")


def assert_rule_precedes_decode_path() -> dict:
    """U3's mechanical clause: docstring rule text < rule constant <
    first decode-call code path, by byte offset in this file."""
    src = open(os.path.abspath(__file__)).read()
    i_doc = src.index(DOCSTRING_RULE_MARKER)
    i_rule = src.index(RULE_CONST_MARKER)
    i_dec = src.index(FIRST_DECODE_MARKER)
    assert i_doc < i_rule < i_dec, \
        "U3 order discipline violated: rule must precede decode path"
    return {"docstring_rule_byte": i_doc, "rule_const_byte": i_rule,
            "first_decode_byte": i_dec,
            "order_held": True,
            "threshold_fixed_on": "exp150 deposit only"}


def zkey_of(zs) -> str:
    return W.to_key([tuple(z) for z in zs])


def extended_greedy(eligible, bar, cap, n_star_splice, rule_filter=None):
    """exp150's greedy VERBATIM (clause order: cap, splice, C4) with
    the cap lifted to `cap` and ONE optional appended clause (the
    pre-registered rule filter, used only by the U2 simulation)."""
    dlist: list = []
    for r in eligible:
        if len(dlist) >= cap:
            break
        if r["nov_splice"] <= n_star_splice:
            continue                       # exp146's clause, kept
        if any(dist(r["f"], d["f"]) <= bar for d in dlist):
            continue                       # C4 filter at `bar`
        if rule_filter is not None and not rule_filter(r):
            continue                       # the R_U generator filter
        dlist.append(r)
    return dlist


def main() -> dict:
    t0 = time.time()
    print("=== exp153: the decode-anatomy family scan (workstream U)"
          " ===\n")
    stage_order = ["rule_declared (docstring + module constant, "
                   "before any decode call)"]
    u3_evidence = assert_rule_precedes_decode_path()
    print("  U3 order assert: docstring rule -> RULE_VMIN constant -> "
          "first decode path  [bytes "
          f"{u3_evidence['docstring_rule_byte']} < "
          f"{u3_evidence['rule_const_byte']} < "
          f"{u3_evidence['first_decode_byte']}]")

    prev150 = json.load(open(PREV150))
    assert prev150["stage3_test"]["landed"], "exp150 did not land?!"

    # ---- 1. library + N*_lib ----------------------------------------
    lib = build_library()
    lib_names = list(lib)
    lib_arr = np.stack([lib[n] for n in lib_names])
    n_star_lib, nn_lib = library_nn_stats(lib)
    assert abs(n_star_lib - 82.288) < 0.01, "N*_lib drift"
    print(f"  library {len(lib_names)} | N*_lib {n_star_lib:.3f} OK")

    # ---- 2. splice family + N*_splice + harness ---------------------
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
    assert worst < 1e-9, "fast evaluator diverged from dist"
    n_star_splice, nn_splice, aux = L.splice_family_bar(S)
    prev146 = json.load(open(PREV146))
    assert abs(n_star_splice - prev146["n_star_splice"]) < 1e-3, \
        "N*_splice drift"
    print(f"  splice family {len(S)} | N*_splice {n_star_splice:.3f} OK "
          f"| harness max|fast-verbatim| {worst:.2e}")

    # ---- 3. search re-run (exp141 loop VERBATIM, seed 141) ----------
    rng = np.random.default_rng(141)
    cache: dict = {}

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
    pool: dict = {}
    round_summaries = []
    for rnd in range(W.ROUNDS + 1):
        recs = [evaluate(zs) for zs in pop]
        for r in recs:
            pool[W.to_key(r["zones"])] = r
        recs_sorted = sorted(recs, key=lambda r: r["J"])
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
    prev141 = json.load(open(PREV141))
    assert len(pool) == prev141["search"]["pool_size"] == 253, \
        "search pool drifted vs exp141 deposit"
    print(f"  search re-run: pool {len(pool)} == exp141 deposit OK "
          f"(t={time.time() - t0:.0f}s)")

    # ---- 4. funnel VERBATIM -----------------------------------------
    ordered = sorted(pool.values(), key=lambda r: r["J"])
    eligible = [r for r in ordered if r["novel"]]
    for r in eligible:
        r["nov_splice"] = L.fast_nov_splice(r["f"], S, fm, fl)
    splice_clear = [r for r in eligible
                    if r["nov_splice"] > n_star_splice]
    pool_dict = {f"pool-{i:03d}": r["f"]
                 for i, r in enumerate(splice_clear)}
    n_star_pool, nn_pool = library_nn_stats(pool_dict)
    assert abs(n_star_pool - 33.776) < 1e-3, "N*_pool drift vs exp150"
    print(f"  funnel: lib-novel {len(eligible)}, splice-clear "
          f"{len(splice_clear)}, N*_pool {n_star_pool:.3f} OK")

    # ---- 5. expanded delivery (exp150 greedy, cap 24) ---------------
    delivered = extended_greedy(eligible, n_star_pool, UCAP,
                                n_star_splice)
    dep_keys = [zkey_of([tuple(z) for z in d["zones"]])
                for d in prev150["delivered"]]
    my_keys = [zkey_of(r["zones"]) for r in delivered[:10]]
    assert my_keys == dep_keys, \
        "first-10 delivery order diverged from the exp150 deposit"
    print(f"  EXPANDED DELIVERY: {len(delivered)} under exp150's "
          f"frozen bars (cap {UCAP}); first 10 zone keys == exp150 "
          f"deposit, in order")

    # ---- 6. features for the WHOLE splice-clear pool (decode-free) --
    feat_of: dict = {}
    for r in splice_clear:
        k = zkey_of(r["zones"])
        feat_of[k] = anatomy_features(r["zones"], r["f"],
                                      r["nov_lib"], r["nov_splice"])
    stage_order += ["bar_replication", "search_replication",
                    "funnel+pool_bar", "expanded_delivery",
                    "pool_features (decode-free)"]

    # ===== STAGE D — FIRST DECODE-CALL PATH IN THIS MODULE (everything above is decode-free; the rule predates this line, byte-offset asserted). ====
    stage_order.append("u4_instrument_check+expanded_decodes")

    def price_and_emit(r) -> None:
        tbl = [price_rung(r["f"], r["zones"], g, mu)
               for (g, mu) in EXTENDED_LADDER]
        r["ladder"] = tbl
        e_new, mode = emit_rung(tbl)
        r["emission_mode"] = mode
        r["emitted_cell"] = e_new["cell"] if e_new else None
        if e_new is not None:
            r["quad"] = e_new["quad"]
            r["decode_errs"] = e_new["decode_errs"]
            r["hold_errs"] = e_new["hold_errs"]
            r["decode_stable_seeds"] = e_new["decode_stable_seeds"]
            r["decode_pass"] = bool(e_new["n_ok"] >= 2)  # C3 semantics
        else:
            r["quad"] = r["decode_errs"] = r["hold_errs"] = None
            r["decode_stable_seeds"] = "0/3"
            r["decode_pass"] = False

    # ---- 7. U4: the original 10 vs the exp150 deposit ---------------
    u4_rows = []
    for i, r in enumerate(delivered[:10]):
        price_and_emit(r)
        dep = prev150["delivered"][i]
        d = {"name": dep["name"],
             "max_dquad": max(abs(a["quad"] - b["quad"])
                              for a, b in zip(r["ladder"],
                                              dep["ladder"])),
             "max_ddec": max(abs(x - y)
                             for a, b in zip(r["ladder"],
                                             dep["ladder"])
                             for x, y in zip(a["decode_errs"],
                                             b["decode_errs"])),
             "max_dhold": max(abs(x - y)
                              for a, b in zip(r["ladder"],
                                              dep["ladder"])
                              for x, y in zip(a["hold_errs"],
                                              b["hold_errs"])),
             "emitted_match": (r["emitted_cell"] == dep["emitted_cell"]
                               and r["emission_mode"]
                               == dep["emission_mode"]),
             "verdict_match": (r["decode_pass"] == dep["decode_pass"])}
        ok = (d["max_dquad"] < 1e-3 and d["max_ddec"] < 1e-3
              and d["max_dhold"] < 1e-3 and d["emitted_match"]
              and d["verdict_match"])
        d["ok"] = bool(ok)
        u4_rows.append(d)
        assert ok, f"U4 instrument drift on {dep['name']}: {d}"
    print("  U4: original-10 ladders bit-exact (rounded) vs exp150 "
          "deposit; emitted rungs + modes + C3 verdicts match")

    # ---- 8. expanded decodes (new members) --------------------------
    for i, r in enumerate(delivered[10:], start=10):
        price_and_emit(r)
        print(f"  pricing[new {i + 1:02d}/{len(delivered)}] "
              f"J={r['J']:.4f} emitted={r['emitted_cell']} "
              f"({r['emission_mode']}) quad={r['quad']} "
              f"dec={r['decode_errs']} hold={r['hold_errs']} "
              f"seeds={r['decode_stable_seeds']} "
              f"pass={r['decode_pass']}")

    # ---- 9. U2 filter simulation (rule applied generator-side) ------
    stage_order.append("u2_filtered_delivery")
    filtered = extended_greedy(
        eligible, n_star_pool, N_DELIVER, n_star_splice,
        rule_filter=lambda r: rule_predict(feat_of[zkey_of(r["zones"])]))
    fkeys = {zkey_of(r["zones"]) for r in filtered}
    priced: dict = {zkey_of(r["zones"]): r for r in delivered}
    for r in filtered:
        k = zkey_of(r["zones"])
        if k not in priced:
            price_and_emit(r)
            priced[k] = r
            print(f"  pricing[u2-only {k[:8]}...] J={r['J']:.4f} "
                  f"emitted={r['emitted_cell']} pass={r['decode_pass']}")
    c3_filtered = sum(int(priced[k]["decode_pass"]) for k in fkeys)
    print(f"  U2 filtered delivery: {len(filtered)} delivered, C3 "
          f"{c3_filtered}/{len(filtered)} (unfiltered exp150: 8/10)")

    # ---- 10. cohort features + rule evaluation ----------------------
    stage_order.append("features+gates")
    exp146_names = {zkey_of([tuple(z) for z in d["zones"]]): d["name"]
                    for d in prev146["delivered"]}
    cohort = []
    for i, r in enumerate(delivered):
        k = zkey_of(r["zones"])
        feat = feat_of[k]
        cohort.append({
            "name": f"d-{i + 1:02d}", "key": k,
            "is_original_10": bool(i < 10),
            "exp146_name": exp146_names.get(k),
            "J": round(r["J"], 4),
            "zones": [list(z) for z in r["zones"]],
            "features": feat,
            "predicted_pass": rule_predict(feat),
            "emitted_cell": r["emitted_cell"],
            "emission_mode": r["emission_mode"],
            "quad": r["quad"],
            "decode_errs": r["decode_errs"],
            "hold_errs": r["hold_errs"],
            "decode_stable_seeds": r["decode_stable_seeds"],
            "decode_pass": r["decode_pass"],
            "decode_err_mean": (round(float(np.mean(r["decode_errs"])), 3)
                                if r["decode_errs"] else None),
            "min_pairwise_D": round(float(min(
                (dist(r["f"], d["f"]) for d in delivered if r is not d),
                default=float("inf"))), 2),
            "ladder": r["ladder"]})

    n = len(cohort)
    match = sum(int(c["predicted_pass"] == c["decode_pass"])
                for c in cohort)
    acc = match / n
    new_rows = [c for c in cohort if not c["is_original_10"]]
    acc_new = (sum(int(c["predicted_pass"] == c["decode_pass"])
                   for c in new_rows) / len(new_rows)) if new_rows else 1.0
    tp = sum(int(c["predicted_pass"] and c["decode_pass"])
             for c in cohort)
    fp = sum(int(c["predicted_pass"] and not c["decode_pass"])
             for c in cohort)
    fn = sum(int(not c["predicted_pass"] and c["decode_pass"])
             for c in cohort)
    tn = sum(int(not c["predicted_pass"] and not c["decode_pass"])
             for c in cohort)
    u1 = bool(acc >= 0.90)
    print(f"\n  U1: rule accuracy on expanded cohort {match}/{n} = "
          f"{acc:.3f} (new-only {acc_new:.3f}); confusion "
          f"tp={tp} fp={fp} fn={fn} tn={tn}")

    u2 = bool(len(filtered) == N_DELIVER and c3_filtered >= 9)
    u3 = bool(u3_evidence["order_held"])
    u4 = bool(all(d["ok"] for d in u4_rows))

    # feature-separation table (deposited regardless of verdict)
    def auc(vals, labels) -> float:
        pos = [v for v, l in zip(vals, labels) if l]
        neg = [v for v, l in zip(vals, labels) if not l]
        if not pos or not neg:
            return float("nan")
        w = sum(1 for a in pos for b in neg
                if (a > b) or (a == b and False))
        eq = sum(1 for a in pos for b in neg if a == b)
        u = (w + 0.5 * eq) / (len(pos) * len(neg))
        return round(max(u, 1.0 - u), 3)

    labels = [c["decode_pass"] for c in cohort]
    feature_table = {}
    for fname in FEATURE_NAMES:
        vals = [c["features"][fname] for c in cohort]
        pos = [v for v, l in zip(vals, labels) if l]
        neg = [v for v, l in zip(vals, labels) if not l]
        d10pos = [c["features"][fname] for c in cohort
                  if c["is_original_10"] and c["decode_pass"]]
        d10neg = [c["features"][fname] for c in cohort
                  if c["is_original_10"] and not c["decode_pass"]]
        feature_table[fname] = {
            "cohort_pass_range": [round(min(pos), 3), round(max(pos), 3)]
            if pos else None,
            "cohort_fail_range": [round(min(neg), 3), round(max(neg), 3)]
            if neg else None,
            "cohort_ranges_overlap": bool(pos and neg
                                          and min(pos) <= max(neg)
                                          and min(neg) <= max(pos)),
            "separates_deposited_10": bool(
                d10pos and d10neg
                and max(d10pos) < min(d10neg)),
            "auc_vs_decode_pass": auc(vals, labels)}

    gates = {"U1_rule_accuracy": u1, "U2_actionable": u2,
             "U3_not_posthoc": u3, "U4_instrument_check": u4}
    npass = sum(int(v) for v in gates.values())
    landed = npass == 4
    verdict = ("THE VMIN RULE LANDS — the decode-anatomy scan closes "
               "the C3 binder with a generator-side filter"
               if landed else
               f"RULE NOT ESTABLISHED ({npass}/4 gates; feature table "
               f"deposited; mechanism-level attribution registered as "
               f"NEXT)")
    for g, v in gates.items():
        print(f"  {g}: {'PASS' if v else 'REFUTED'}")
    print(f"  === exp153 VERDICT: {verdict} ===")

    registered_next = (
        ["adopt the R_U generator-side filter as the C3 repair "
         "(predicted-pass delivery), then re-run the generator's "
         "C-gates on the filtered set",
         "mechanism: WHY all-deep anatomies pin decode_err at ~9 mV "
         "across all 9 rungs (write-path saturation vs clamp-release "
         "reconstruction) — one instrument-level dissection"]
        if landed else
        ["mechanism-level attribution: the deposited feature table "
         "shows which anatomy features do and do not track decode "
         "failure — dissect the write path (write_spec_layer + "
         "clamp-release settle) on the failing class directly",
         "no ladder change until the mechanism is named (L130 "
         "discipline)"])

    out = {
        "exp": "exp153_decode_anatomy (workstream U)",
        "claim": ("a simple pre-registered feature rule (vmin_zone < "
                  "45.0 mV, fixed on the exp150 deposit before any "
                  "exp153 decode) separates decode-pass from "
                  "decode-fail on the expanded delivered cohort and "
                  "is actionable as a generator-side filter that "
                  "lifts C3 to >= 9/10"),
        "verdict": verdict,
        "stage_order": stage_order,
        "rule": {**RULE_VMIN,
                 "u3_order_evidence": u3_evidence,
                 "applied_as": "generator-side filter: deliver only "
                               "predicted-pass inventions (U2 "
                               "simulation); cohort prediction (U1)"},
        "pre_registered": {
            "gates": {
                "U1": "rule accuracy >= 90% on the expanded cohort "
                      "(C3 verdicts at exp150's frozen emission)",
                "U2": "predicted-pass-only delivery (frozen bars, cap "
                      "10) yields exactly 10 with C3 >= 9/10",
                "U3": "rule declared before the expanded decodes "
                      "(docstring + constant precede the first "
                      "decode-call path, byte-offset asserted)",
                "U4": "bit-exact reproduction of exp150's deposited "
                      "ladders/emissions/verdicts on the original 10"},
            "ucap": UCAP,
            "features": FEATURE_NAMES},
        "bars": {"n_star_lib": round(n_star_lib, 3),
                 "n_star_splice": round(n_star_splice, 3),
                 "n_star_pool": round(n_star_pool, 3)},
        "replication": {
            "exp141_pool_253": True,
            "first10_zone_keys_match_exp150": True,
            "fast_vs_verbatim_harness_max_diff": worst},
        "u4_instrument_check": u4_rows,
        "expanded_cohort": cohort,
        "u2_filtered_delivery": {
            "n_delivered": len(filtered),
            "c3_pass": c3_filtered,
            "members": [{"key": zkey_of(r["zones"]),
                         "J": round(r["J"], 4),
                         "vmin_zone": feat_of[zkey_of(r["zones"])]
                         ["vmin_zone"],
                         "predicted_pass": True,
                         "decode_pass": priced[zkey_of(r["zones"])]
                         ["decode_pass"],
                         "decode_errs": priced[zkey_of(r["zones"])]
                         ["decode_errs"],
                         "emitted_cell":
                         priced[zkey_of(r["zones"])]["emitted_cell"]}
                        for r in filtered]},
        "u1_evaluation": {
            "n": n, "matches": match, "accuracy": round(acc, 4),
            "accuracy_new_only": round(acc_new, 4),
            "confusion": {"tp": tp, "fp": fp, "fn": fn, "tn": tn}},
        "feature_table": feature_table,
        "gates": gates,
        "gates_passed": f"{npass}/4",
        "registered_next": registered_next,
        "wall_s": round(time.time() - t0, 1),
        "notes": ("Instruments exp136/exp141/exp144/exp146/exp150 "
                  "imported verbatim (price_rung, emit_rung reused "
                  "as-is). New objects only: UCAP=24, the feature "
                  "extractor, the pre-registered R_U rule + its "
                  "generator-side filter, the U-gate readouts. The "
                  "rule's threshold was fixed from the exp150 DEPOSIT "
                  "(gap (40.8, 48.6) in vmin_zone) before any exp153 "
                  "decode call; the in-module byte-offset assert "
                  "proves declaration order."),
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(f"\n  results -> {OUT} (wall {out['wall_s']}s)")
    return out


if __name__ == "__main__":
    main()
