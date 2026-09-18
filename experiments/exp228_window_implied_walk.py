#!/usr/bin/env python3
"""exp228 — THE WINDOW-IMPLIED SELF-FED WALK (L200's registered next).

exp223's refutation localized the value channel's limit: the read is
STRUCTURE-driven — the committed VALUES are invisible to the window,
so value-carrying breaks exactly at the host's structure
discontinuities (sub-mV between them). The structure-honest form: the
plan propagated by the WINDOW'S OWN IMPLIED VALUES — the emission the
structure dictates at each frontier cell (the ring's own read output)
becomes the NEXT round's plan at those cells; the walk's target is
then fully self-referential (round k's plan = round k-1's emissions),
no external plan beyond the seed round. The pre-named bar: 6 rings
under the 6.0 bar on H0 and H4.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp223's walk machinery
verbatim (the window construction, the exp178 production scoped read,
the S* lock, the floor-restore discipline, the P6 frozen-commit
discipline — Y2's bit-exact checks reused verbatim); the
WINDOW-IMPLIED PLAN (pre-named, zero knobs): round k's target at the
frontier = round k-1's EMITTED values at the previously-frontier
cells propagated by exp94's spec_target_n over the canon base (the
emission, not the committed frozen value, is what propagates — the
exp223 refutation's own diagnosis); the pre-named hosts: H0 and H4.

GATES (each evaluated exactly once):
  GATE-F1 (the walk) 6 window-implied rings complete with zero
           rejections on H0 and H4 (3 seeds each); ring errs under
           the 6.0 bar throughout.
  GATE-F2 (the frozen-commit clause) the committed values bit-stable
           (P6 verbatim, exp223's Y2 checks reused) — the emissions
           feed the PLAN, never the committed record retroactively.
  GATE-F3 (the self-reference profile) per-round the
           emitted-vs-implied-plan err deposited; the branch named:
           SELF-CARRYING (all 6 rings under the bar) / DEGRADES
           (any ring over).
  GATE-F4 (hygiene) all finite; the S* lock per write; the -60.0
           floor post-restore asserted; no per-target tuning.
NO post-hoc tuning. --smoke permitted (H0, 2 rings), discarded.
DEPOSIT: results/exp228_window_implied_walk.json
RUN: python3 -m experiments.exp228_window_implied_walk [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp228_window_implied_walk.json")


def main() -> dict:
    # ====================================================================
    # BODY (written by the run agent; the docstring's pre-registered
    # gates above byte-unchanged — exp174's body-only discipline)
    # ====================================================================
    # SHARDING (exp223's pattern): --job H0 / H4 (the pre-named hosts)
    # / gates (closed on the MERGED deposit). "all" runs everything
    # in-process and closes the gates on the merged deposit.
    import hashlib
    import time

    import numpy as np  # noqa: E402

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all", "H0", "H4", "gates"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    if args.out is not None:
        out_path = args.out
    elif args.job == "all":
        out_path = OUT
    else:
        out_path = os.path.join(ROOT, "results",
                                f"exp228_shard_{args.job}.json")

    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    from cultivation.compiler.anatomy import (  # noqa: E402
        AnatomySpec, Zone)
    from experiments.exp142_sign_read import (  # noqa: E402
        SEEDS, STAR_OP, execute_signed)
    from experiments.exp145_phase_read import (  # noqa: E402
        warnings_as_errors)
    from experiments.exp148_temporal_read import read_scoped  # noqa: E402
    from experiments.exp151_self_expansion import (  # noqa: E402
        ERR_BAR as WALK_ERR_BAR, RINGS as WALK_RINGS, frontier_of,
        plan_of, seed_cone, window_matrix)
    from experiments.exp169_rt_scoping import (  # noqa: E402
        THRESHOLD as SCOPED_THRESHOLD, f_max_frames)
    from experiments.exp182_substrate_100 import S_STAR  # noqa: E402
    from experiments.exp73_active_renormalization import (  # noqa: E402
        small_world)
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    # THE FLOOR RESTORE (exp218's disclosed discipline, reused by
    # exp223 and here): the body's import chain includes
    # exp169_rt_scoping, whose import flips CORE.NEURAL_SPEC_MIN to
    # -35.0 (the R_T battery's floor — verified empirically this
    # run). The read-chain modules captured CF-1's production -60.0
    # at their own import; exp169's flip is attribute-only. Restored
    # here so the walk's write path runs at the CF-1 production floor
    # the pre-registration asserts.
    CORE.NEURAL_SPEC_MIN = -60.0
    assert CORE.NEURAL_SPEC_MIN == -60.0, "floor restore failed"

    BAR = 6.0                              # the record's verify bar
    WALK_BAR = WALK_ERR_BAR                # exp151's ring-err bar (6.0)
    WALK_SEEDS = list(SEEDS)               # exp142's (1, 2, 3) — P7
    PROD_FLOOR = -60.0                     # CF-1's production value
    REWIRE_P = 0.10                        # exp202's redraw p
    DEP202 = os.path.join(ROOT, "results",
                          "exp202_cross_organism_carriage.json")
    assert os.path.exists(DEP202), f"reference deposit missing: {DEP202}"
    DEP223 = os.path.join(ROOT, "results",
                          "exp223_self_fed_walk.json")
    assert os.path.exists(DEP223), f"reference deposit missing: {DEP223}"
    F_HOSTS = ("H0", "H4")   # the pre-named hosts (the reference and
    #                          the worst-margin host — exp223's Y_HOSTS
    #                          reused verbatim)
    WIRING_ID = ("exp148.read_scoped | exp178 production wiring | "
                 "T=1 static window -> R_T -> execute_signed@STAR_OP")

    # THE WINDOW-IMPLIED PLAN (pre-named, zero knobs — the deposit
    # carries this string verbatim): round k's target at the frontier
    # = round k-1's EMITTED values at the previously-frontier cells
    # propagated by exp94's spec_target_n over the canon base — the
    # emission, not the committed frozen value, is what propagates
    # (the exp223 refutation's own diagnosis). The plan vector is
    # built by the spec_target_n instrument call (the
    # previously-frontier cells enter as width-one zones carrying
    # their own round-(k-1) emissions over the canon base); each
    # frontier cell's target = the round-(k-1) emission of its
    # nearest committed ring neighbor (the highest ring index among
    # the cell's committed neighbors; same-ring ties resolved ON the
    # canon labeling — the tied neighbor whose canon value matches
    # the frontier cell's own canon value, residual ties by lowest
    # cell index — deterministic, zero knobs). STRUCTURAL (GATE-F2):
    # the plan builder's inputs are the emission vector, the
    # previously-frontier cells, the canon labeling, the committed
    # ring structure and the adjacency — NEVER the committed/frozen
    # record; the emissions feed the PLAN, never the committed record
    # retroactively. For round 1 the previous round is the seed: the
    # previously-frontier cells are the P3 seed patch and the
    # emission vector is the P3 plan (the pre-named sole external
    # injection — exp223's T_plan clause reused verbatim).
    WINDOW_IMPLIED_RULE = (
        "round k's frontier plan = round k-1's EMITTED values at the "
        "previously-frontier cells propagated by exp94's spec_target_n "
        "on the canon labeling (the plan vector built by the "
        "spec_target_n instrument call: the previously-frontier cells "
        "enter as width-one zones carrying their own round-(k-1) "
        "emissions over the canon base); the frontier cells' target = "
        "the round-(k-1) emission of their nearest committed ring "
        "neighbor (the emission, not the committed frozen value, is "
        "what propagates — the exp223 refutation's own diagnosis); "
        "nearest committed ring = the highest ring index among the "
        "cell's committed neighbors; same-ring ties resolved on the "
        "canon labeling (canon match, else lowest index); the plan "
        "builder never receives the committed/frozen record "
        "(GATE-F2's clause, structural); round 1's previous round is "
        "the seed (the P3 plan — the pre-named sole external "
        "injection); T_plan is consumed solely by the P3 seed "
        "initialization")

    with open(DEP202) as fh:
        dep202 = json.load(fh)

    # ---- the floors: CF-1's production value asserted ----------------
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR \
        and g6.NEURAL_SPEC_MIN == PROD_FLOOR, \
        f"floor drift: {CORE.NEURAL_SPEC_MIN}, {g6.NEURAL_SPEC_MIN}"
    # ---- the S* identity of the walk's executor -----------------------
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        f"the walk's executor op {STAR_OP} != S* {S_STAR}"

    # ---- the pre-named hosts (exp223's build discipline verbatim) -----
    def build_f_hosts() -> dict:
        hosts = {}
        canon0 = labeling_bfs_n(g6.A_CHAIN)
        assert np.array_equal(canon0, g6.wildtype_target(g6.N))
        hosts["H0"] = {"name": "H0", "n": int(g6.N), "A": g6.A_CHAIN,
                       "canon": canon0}
        redraw = {r["host"]: r["seed"] for r in
                  dep202["sections"]["corpus"]["scan"]["redraw_log"]}
        seed4 = int(redraw["H4"])
        A4 = small_world(100, REWIRE_P, seed4)
        assert A4.sum() > 0
        dep_edges = dep202["sections"]["corpus"]["hosts"]["H4"].get("edges")
        got_edges = int(np.count_nonzero(np.triu(A4, 1)))
        if dep_edges is not None and isinstance(dep_edges, int):
            assert got_edges == dep_edges, \
                (f"H4 rebuild drift: edges {got_edges} != "
                 f"deposit {dep_edges}")
        hosts["H4"] = {"name": "H4", "n": 100, "A": A4,
                       "canon": labeling_bfs_n(A4),
                       "rewire_seed": seed4}
        return hosts

    # ============== THE WINDOW-IMPLIED WALK (exp223's machinery
    #                re-armed; the plan re-drawn per round from the
    #                EMISSION record — the window-implied plan) ========
    class _Win:
        """exp151's static window medium (the P5 closed-world node
        contract): one snapshot — the masked full-n x n window matrix."""
        kind = "window"

        def __init__(self, M):
            self._M = M

        def snapshots(self):
            return [self._M]

    _WALK_LOCK_LOG: list = []

    def _lock_walk_write(host, ring, seed):
        # the S* assertion on every ring write: the read wired through
        # exp178's production scoped arm ends in exp148's read_temporal
        # -> execute_signed at op=STAR_OP; STAR_OP IS S* = (64.0, 0.0)
        # (asserted at body start and re-asserted per write).
        assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
            f"walk write off S* on {host} ring {ring}"
        _WALK_LOCK_LOG.append((host, int(ring), WIRING_ID))

    def _window_implied_plan(frontier, W, canon, n, prev_emission,
                             prev_frontier, ring_of, C):
        """THE WINDOW-IMPLIED PLAN (see WINDOW_IMPLIED_RULE above).
        The plan vector is built by exp94's spec_target_n instrument
        call (the previously-frontier cells as width-one zones
        carrying their own round-(k-1) emissions over the canon base),
        then each frontier cell's target = the round-(k-1) emission of
        its nearest committed ring neighbor. STRUCTURAL (GATE-F2): the
        builder's inputs are the emission vector, the
        previously-frontier cells, the canon labeling, the committed
        ring structure and the adjacency — the committed/frozen record
        is NOT an input (the emissions feed the PLAN, never the
        committed record retroactively)."""
        prev_frontier = sorted(prev_frontier)
        spec = AnatomySpec(
            zones=[Zone(f0=i / n, f1=(i + 1) / n,
                        voltage=float(prev_emission[i]), name=f"c{i}")
                   for i in prev_frontier],
            amputate_plane=None, spec_name="exp228-window-implied",
            somatic_latch=False)
        plan = spec_target_n(spec, canon, n)
        sup = np.abs(W)
        prop_log = []
        for j in frontier:
            nbrs = [int(i) for i in np.where(sup[j] > 0)[0]
                    if int(i) in C]
            assert nbrs, f"frontier cell {j} has no committed neighbor"
            r_star = max(ring_of[i] for i in nbrs)
            cand = sorted(i for i in nbrs if ring_of[i] == r_star)
            matched = [i for i in cand if canon[i] == canon[j]]
            i_star = matched[0] if matched else cand[0]
            plan[j] = float(prev_emission[i_star])
            prop_log.append({"cell": int(j), "neighbor": int(i_star),
                             "neighbor_ring": int(r_star),
                             "n_same_ring_candidates": len(cand),
                             "canon_matched": bool(matched),
                             "plan_source": "round-(k-1) emission",
                             "plan_value":
                                 round(float(prev_emission[i_star]), 4)})
        return plan, prop_log

    def _implied_ring(h, W, canon, cone, ring_index):
        """One window-implied expansion step for one seed-cone —
        exp223's _selffed_ring machinery VERBATIM (the window
        construction, the exp178 production scoped read, the S* lock,
        the reduction datum, the P6 commit), with T_plan[F] replaced
        by the WINDOW-IMPLIED plan. The ONLY values that can enter the
        committed region are copied from the read's final V at the
        frontier (P6); the emission record (the ring's own read
        output) is what the NEXT round's plan propagates."""
        name, s = h["name"], cone["seed"]
        C = cone["C"]
        F = frontier_of(C, W)                    # exp151's P4 verbatim
        cone["frontier"] = [int(j) for j in F]
        if not F:
            return {"ring_index": ring_index, "ring_expanded": False,
                    "exhausted": True, "read_ok": True, "frontier": [],
                    "pass": False, "stop": "exhausted"}
        M, meta = window_matrix(W, C, F, None)   # exp151's P5 verbatim
        try:
            fmax = float(f_max_frames([M]))      # exp169's diagnostic
            with warnings_as_errors():
                out = read_scoped(_Win(M), s, return_state=True,
                                  f_max=fmax)   # exp178's wiring
            V = np.asarray(out["final_state"]["V"], dtype=float)
            read_ok, rejection = True, None
        except Exception as e:                   # zero-rejection hygiene
            return {"ring_index": ring_index, "ring_expanded": True,
                    "exhausted": False, "read_ok": False,
                    "rejection": f"{type(e).__name__}: {e}"[:200],
                    "frontier": [int(j) for j in F], "window": meta,
                    "pass": False, "stop": "rejection"}
        # wiring datum (NOT a gate): exp151's raw read on the same
        # window must reduce BIT-EXACTLY to the production scoped read
        # on a static window.
        with warnings_as_errors():
            raw = execute_signed(MULTI, M, s, op=STAR_OP,
                                 return_state=True)
        reduction = bool(np.array_equal(
            np.asarray(raw["final_state"]["V"], dtype=float), V))
        plan, prop_log = _window_implied_plan(
            [int(j) for j in F], W, canon, h["n"],
            cone["prev_emission"], cone["prev_frontier"],
            cone["ring_of"], C)
        emitted = V[F]
        err = float(np.sqrt(np.mean((emitted - plan[F]) ** 2)))
        # ---- GATE-F2's frozen discipline (exp223's Y2 checks reused
        #      verbatim, asserted): the committed prefix equals the
        #      frozen values bit-exactly (P6 verbatim) — the emissions
        #      feed the PLAN, never the committed record retroactively
        n_prefix = 0
        if ring_index >= 2:
            for c, v in cone["frozen"].items():
                assert cone["committed"][c] == v, \
                    f"frozen prefix drift at cell {c}"
                n_prefix += 1
        cone["n_prefix_checks"] = cone.get("n_prefix_checks", 0) \
            + n_prefix
        # ---- the ring write: the S* lock asserted, then P6's commit
        #      (the read's own outputs, full precision, verbatim);
        #      the emission record advances to THIS round's read
        #      output (the next round's plan source) ------------------
        _lock_walk_write(name, ring_index, s)
        cone["ring_V"][ring_index] = V
        for j in F:
            C.add(int(j))
            cone["committed"][int(j)] = float(V[int(j)])
            cone["frozen"][int(j)] = float(V[int(j)])
            cone["ring_of"][int(j)] = int(ring_index)
        cone["prev_emission"] = V                # the ring's own read
        cone["prev_frontier"] = [int(j) for j in F]   # output (E_k)
        return {"ring_index": ring_index, "ring_expanded": True,
                "exhausted": False, "read_ok": True,
                "rejection": rejection,
                "scoped_wiring": {"wiring_id": WIRING_ID,
                                  "f_max": fmax,
                                  "threshold": SCOPED_THRESHOLD,
                                  "branch": "R_T (static window)"},
                "reduction_bitexact_vs_exp151_raw": reduction,
                "frontier": [int(j) for j in F],
                "window": meta,
                "propagation": prop_log,
                "plan_source": "window-implied (round k-1 emissions)",
                "emitted": [round(float(x), 3) for x in emitted],
                "plan": [round(float(x), 3) for x in plan[F]],
                "ring_err_mV": round(err, 3),
                "pass": bool(np.isfinite(err) and err < WALK_BAR)}

    def run_walk_host(h, n_rings):
        """The window-implied walk on one host: exp151's protocol
        (P2/P3/P6/P7 verbatim — plan_of, seed_cone,
        commit-the-read's-own-outputs, seeds (1, 2, 3)) run in
        LOCKSTEP rounds across the seed cones. The plan for every
        ring is the WINDOW-IMPLIED plan (the rule above) — T_plan
        enters solely at the P3 seed initialization; rounds >= 2's
        plans propagate the EMISSION record (the previous round's
        read output), never the committed record."""
        name = h["name"]
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drifted mid-run"
        W = np.asarray(h["A"], dtype=float)
        canon = np.asarray(h["canon"], dtype=float)
        assert np.array_equal(canon, labeling_bfs_n(np.abs(W))), \
            "canon mismatch: the host canon != the engine canon"
        T_plan = plan_of(W)          # exp151's P2 verbatim — consumed
        seed_cells = seed_cone(W)    # ONLY by the P3 init below
        support_n = int(np.count_nonzero(np.abs(W).sum(axis=1)))
        cones = []
        for s in WALK_SEEDS:
            cone = {"seed": s, "C": set(seed_cells), "committed": {},
                    "frozen": {}, "ring_of": {}, "frontier": [],
                    "ring_V": {}, "rings": [], "broken": None,
                    # round 0's emission record: the P3 plan (the
                    # pre-named sole external injection); round 0's
                    # previously-frontier cells: the seed patch
                    "prev_emission": T_plan.copy(),
                    "prev_frontier": list(seed_cells)}
            for i in seed_cells:     # P3: the parent's committed values
                cone["committed"][i] = float(T_plan[i])
                cone["frozen"][i] = float(T_plan[i])
                cone["ring_of"][i] = 0
            cones.append(cone)
        for r in range(1, n_rings + 1):
            active = [c for c in cones if c["broken"] is None]
            if not active:
                break
            for c in active:
                rec = _implied_ring(h, W, canon, c, r)
                c["rings"].append(rec)
                if rec.get("stop"):
                    c["broken"] = rec["stop"]
        # ---- GATE-F2's close-out (exp223's Y2 checks reused
        #      verbatim): the full frozen-prefix check and the P6
        #      provenance (every committed cell's value equals its
        #      commit-round read's own final V, bit-exactly) --------
        y2 = {}
        for c in cones:
            n_close = 0
            for cc, v in c["frozen"].items():
                assert c["committed"][cc] == v, "frozen drift at close"
                n_close += 1
            n_prov = 0
            n_p3 = 0
            for cc, v in c["committed"].items():
                if c["ring_of"][cc] == 0:
                    # ring 0 = the P3 seed patch: the frozen value IS
                    # the P3 initialization (the parent's committed
                    # values); no read provenance applies
                    n_p3 += 1
                    continue
                rv = c["ring_V"][c["ring_of"][cc]]
                assert v == float(rv[cc]), "P6 provenance break"
                n_prov += 1
            y2[str(c["seed"])] = {
                "n_prefix_bitexact": int(c.get("n_prefix_checks", 0)),
                "n_close_bitexact": n_close,
                "n_p6_provenance_bitexact": n_prov,
                "n_p3_seed_cells": n_p3}
        out_cones = []
        for c in cones:
            expanded = [x for x in c["rings"]
                        if x.get("ring_expanded") and x.get("read_ok")]
            rings_expanded = len(expanded)
            n_rej = sum(1 for x in c["rings"] if not x.get("read_ok"))
            exhausted = bool(c["rings"][-1].get("exhausted")) \
                if c["rings"] else False
            errs = [x.get("ring_err_mV") for x in expanded]
            profile = [e for e in errs if e is not None]
            mono_nc = bool(all(profile[i + 1] >= profile[i]
                               for i in range(len(profile) - 1))
                           if len(profile) > 1 else True)
            mono_ni = bool(all(profile[i + 1] <= profile[i]
                               for i in range(len(profile) - 1))
                           if len(profile) > 1 else True)
            over = [{"ring": x["ring_index"],
                     "ring_err_mV": x.get("ring_err_mV"),
                     "frontier": x.get("frontier"),
                     "emitted": x.get("emitted"),
                     "plan": x.get("plan")}
                    for x in expanded
                    if x.get("ring_err_mV") is not None
                    and x["ring_err_mV"] >= WALK_BAR]
            complete = bool(rings_expanded == n_rings and n_rej == 0
                            and not exhausted
                            and len(profile) == n_rings
                            and all(e < WALK_BAR for e in profile))
            branch = "SELF-CARRYING" if complete else "DEGRADES"
            frozen_keys = sorted(c["frozen"])
            out_cones.append({
                "seed": c["seed"],
                "rings_expanded": rings_expanded,
                "exhausted": exhausted,
                "n_rejections": n_rej,
                "broken": c["broken"],
                "final_coverage": [len(c["C"]), support_n],
                "ring_errs_mV": errs,
                "rings_passed": sum(1 for x in expanded if x.get("pass")),
                "profile_monotone_nondecreasing": mono_nc,
                "profile_monotone_nonincreasing": mono_ni,
                "rings_over_bar": over,
                "branch": branch,
                "y2_frozen": y2[str(c["seed"])],
                "frozen_sha256_16": hashlib.sha256(
                    np.ascontiguousarray(
                        [c["frozen"][k] for k in frozen_keys],
                        dtype=np.float64).tobytes()
                ).hexdigest()[:16],
                "rings": c["rings"]})
        return {"host": name, "n": int(h["n"]),
                "kind": ("reference (exp182's own host)"
                         if name == "H0" else
                         "corpus-rewired organism (the pre-named "
                         "worst-margin host — exp223's Y_HOSTS "
                         "reused verbatim)"),
                "seeds": list(WALK_SEEDS), "S_star": list(S_STAR),
                "rings_registered": int(n_rings),
                "seed_cells": len(seed_cells),
                "propagation_rule": WINDOW_IMPLIED_RULE,
                "cones": out_cones}

    # ========================== --smoke (H0, 2 rings) ==================
    if args.smoke:
        hosts = build_f_hosts()
        w = run_walk_host(hosts["H0"], n_rings=2)

        def _prev_emission_match(c):
            # the plan-provenance spot check: every ring >= 2's logged
            # plan_value equals the PREVIOUS round's logged emitted
            # value at the logged neighbor (both 3-4dp as deposited) —
            # the plan is sourced from the EMISSION record
            ok = True
            for i, x in enumerate(c["rings"]):
                if not (x.get("ring_expanded") and x.get("read_ok")
                        and x["ring_index"] >= 2):
                    continue
                prev_rec = c["rings"][i - 1]
                for p in x["propagation"]:
                    pos = prev_rec["frontier"].index(p["neighbor"])
                    if abs(p["plan_value"]
                           - prev_rec["emitted"][pos]) > 1e-3:
                        ok = False
            return ok

        checks = {
            "rings_expanded_all_seeds": all(
                c["rings_expanded"] == 2 for c in w["cones"]),
            "zero_rejections": all(c["n_rejections"] == 0
                                   for c in w["cones"]),
            "ring_errs_finite": all(
                e is not None and np.isfinite(e)
                for c in w["cones"] for e in c["ring_errs_mV"]),
            "y2_frozen_bitexact": all(
                c["y2_frozen"]["n_close_bitexact"] > 0
                and c["y2_frozen"]["n_p6_provenance_bitexact"] > 0
                for c in w["cones"]),
            "reduction_bitexact": all(
                x.get("reduction_bitexact_vs_exp151_raw")
                for c in w["cones"] for x in c["rings"]
                if x.get("ring_expanded") and x.get("read_ok")),
            "implied_plan_sourced_from_emissions": all(
                _prev_emission_match(c) for c in w["cones"]),
            "lock_log_at_S_star": len(_WALK_LOCK_LOG) == 6,
            "floor_at_production": CORE.NEURAL_SPEC_MIN == PROD_FLOOR,
        }
        ok = all(checks.values())
        print(f"=== exp228 SMOKE (H0, 2 rings, DISCARDED) === "
              f"{checks} -> {'OK' if ok else 'INSTRUMENT BUG'} "
              f"({time.time() - t0:.1f}s)")
        dep = {"exp": "exp228_window_implied_walk", "kind": "smoke",
               "discarded": True, "checks": checks, "ok": ok,
               "walk": w}
        if args.out:
            os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                        exist_ok=True)
            with open(out_path, "w") as fh:
                json.dump(dep, fh, indent=1, default=float)
        return dep

    # ===================== the credited run ============================
    assert not args.smoke
    if args.job == "gates":
        # the gates close on the MERGED deposit (assembled at salvage);
        # every bar below is a pre-registered constant
        return _close_gates_on(out_path)
    hosts = build_f_hosts()
    assert all(k in hosts for k in F_HOSTS)

    jobs = ["H0", "H4"] if args.job == "all" else [args.job]

    sections: dict = {}
    for hname in ("H0", "H4"):
        if hname not in jobs:
            continue
        w = run_walk_host(hosts[hname], WALK_RINGS)
        sections[hname] = {"walk": w}
        print(f"  [{hname}] window-implied walk 6-ring complete "
              f"{sum(1 for c in w['cones'] if c['rings_expanded'] == WALK_RINGS)}/3 "
              f"seeds | zero rejections "
              f"{sum(1 for c in w['cones'] if c['n_rejections'] == 0)}/3 "
              f"| branches {[c['branch'] for c in w['cones']]} | "
              f"worst ring err "
              f"{max((e for c in w['cones'] for e in c['ring_errs_mV'] if e is not None), default=None)}")

    result = {"exp": "exp228_window_implied_walk", "sections": sections}
    if args.job != "all":
        os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                    exist_ok=True)
        with open(out_path, "w") as fh:
            json.dump(result, fh, indent=1, default=float)
        print(f"  deposited {out_path} (shard {args.job})")
        return result

    # local all-in-one: write the merged sections, close the gates
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=1, default=float)
    return _close_gates_on(out_path)


def _close_gates_on(merged_path: str) -> dict:
    """GATE CLOSURE — each gate evaluated EXACTLY ONCE on the merged
    deposit (exp223's pattern). The bars are the pre-registered
    constants; nothing here is tuned by the data."""
    import time as _time

    import numpy as np

    t0 = _time.time()
    with open(merged_path) as fh:
        merged = json.load(fh)
    secs = merged["sections"]
    assert all(k in secs for k in ("H0", "H4")), \
        f"merged deposit incomplete: {sorted(secs)}"
    walk_secs = [secs["H0"]["walk"], secs["H4"]["walk"]]
    cones = [(h["host"], c) for h in walk_secs for c in h["cones"]]
    assert len(cones) == 6, f"cone count {len(cones)} != 6"
    RINGS = 6
    WALK_BAR = 6.0
    DEP223 = os.path.join(ROOT, "results", "exp223_self_fed_walk.json")
    assert os.path.exists(DEP223), f"reference deposit missing: {DEP223}"

    # ---- GATE-F1 (the walk): 6 window-implied rings, zero
    #      rejections, ring errs under the 6.0 bar throughout, on
    #      every (host, seed) cone — the emission carries the walk ----
    f1_rows = []
    for hn, c in cones:
        errs = c["ring_errs_mV"]
        ok = bool(c["rings_expanded"] == RINGS
                  and c["n_rejections"] == 0
                  and not c["exhausted"]
                  and len(errs) == RINGS
                  and all(e is not None and np.isfinite(e)
                          and e < WALK_BAR for e in errs))
        f1_rows.append({"host": hn, "seed": c["seed"], "complete": ok,
                        "rings_expanded": c["rings_expanded"],
                        "n_rejections": c["n_rejections"],
                        "exhausted": c["exhausted"],
                        "worst_ring_err_mV":
                            (max(e for e in errs if e is not None)
                             if errs else None)})
    f1 = all(r["complete"] for r in f1_rows)

    # ---- GATE-F2 (the frozen-commit clause): the committed values
    #      bit-stable (P6 verbatim, exp223's Y2 checks reused
    #      verbatim) — the emissions feed the PLAN, never the
    #      committed record retroactively (structural: the plan
    #      builder's inputs are the emission vector, the
    #      previously-frontier cells, the canon labeling, the
    #      committed ring structure and the adjacency — never the
    #      committed/frozen record) ----------------------------------
    n_prefix = sum(c["y2_frozen"]["n_prefix_bitexact"]
                   for _, c in cones)
    n_close = sum(c["y2_frozen"]["n_close_bitexact"] for _, c in cones)
    n_prov = sum(c["y2_frozen"]["n_p6_provenance_bitexact"]
                 for _, c in cones)
    f2 = bool(n_close > 0 and n_prov > 0 and n_prefix > 0)

    # ---- GATE-F3 (the self-reference profile): per-round the
    #      emitted-vs-implied-plan err deposited; the branch named:
    #      SELF-CARRYING (all 6 rings under the bar) / DEGRADES (any
    #      ring over) -------------------------------------------------
    branches = {}
    f3_detail = {}
    for hn in ("H0", "H4"):
        cs = [c for h2, c in cones if h2 == hn]
        br = ("SELF-CARRYING"
              if all(c["branch"] == "SELF-CARRYING" for c in cs)
              else "DEGRADES")
        branches[hn] = br
        f3_detail[hn] = {"per_cone": [
            {"seed": c["seed"], "branch": c["branch"],
             "profile_monotone_nondecreasing":
                 c["profile_monotone_nondecreasing"],
             "profile_monotone_nonincreasing":
                 c["profile_monotone_nonincreasing"],
             "ring_errs_mV": c["ring_errs_mV"],
             "rings_over_bar": c["rings_over_bar"]} for c in cs]}
    f3 = all(b == "SELF-CARRYING" for b in branches.values())

    # ---- GATE-F4 (hygiene) --------------------------------------------
    n_rej_walk = sum(c["n_rejections"] for _, c in cones)
    errs_finite = all(
        e is not None and np.isfinite(e) for _, c in cones
        for e in c["ring_errs_mV"]) and n_rej_walk == 0
    n_ring_writes = sum(x["ring_index"] in range(1, RINGS + 1)
                        and x.get("ring_expanded") and x.get("read_ok")
                        for _, c in cones for x in c["rings"])
    reductions_ok = all(
        x.get("reduction_bitexact_vs_exp151_raw")
        for _, c in cones for x in c["rings"]
        if x.get("ring_expanded") and x.get("read_ok"))
    f4 = bool(errs_finite and reductions_ok and n_ring_writes == 36)
    # the S* lock logs: every ring write was locked at S* (the per-write
    # asserts would have raised otherwise); the -60.0 floor assert ran
    # post-restore and per host; the no-tuning clause is structural
    # (the constants table and the window-implied rule are logged once
    # and are the same object across every host, ring and seed).
    gates = {
        "F1": {"pass": bool(f1),
               "clause": "6 window-implied rings complete with zero "
                         "rejections on H0 and H4 (3 seeds each); "
                         "ring errs under the 6.0 bar throughout",
               "n_cones": len(cones),
               "n_complete": sum(1 for r in f1_rows if r["complete"]),
               "per_cone": f1_rows,
               "worst_ring_err_mV": max(r["worst_ring_err_mV"]
                                        for r in f1_rows
                                        if r["worst_ring_err_mV"]
                                        is not None)},
        "F2": {"pass": bool(f2),
               "clause": "the committed values bit-stable (P6 "
                         "verbatim, exp223's Y2 checks reused) — the "
                         "emissions feed the PLAN, never the "
                         "committed record retroactively",
               "n_prefix_bitexact_checks": n_prefix,
               "n_close_bitexact_checks": n_close,
               "n_p6_provenance_bitexact_checks": n_prov,
               "plan_provenance_structural": True,
               "plan_provenance_note": (
                   "the plan builder (_window_implied_plan) receives "
                   "the emission vector, the previously-frontier "
                   "cells, the canon labeling, the committed ring "
                   "structure and the adjacency — the committed/"
                   "frozen record is not an input; see "
                   "disclosures.exp223_provenance_identity for the "
                   "non-gating cross-deposit comparison")},
        "F3": {"pass": bool(f3),
               "clause": "per-round the emitted-vs-implied-plan err "
                         "deposited; the branch named: SELF-CARRYING "
                         "(all 6 rings under the bar) / DEGRADES (any "
                         "ring over)",
               "branches": branches,
               "per_host": f3_detail},
        "F4": {"pass": bool(f4),
               "clause": "all finite; the S* lock per write; the -60.0 "
                         "floor post-restore asserted; no per-target "
                         "tuning",
               "all_errs_finite": bool(errs_finite),
               "walk_rejections": n_rej_walk,
               "ring_writes_logged": n_ring_writes,
               "scoped_reduction_bitexact_all_cones":
                   bool(reductions_ok),
               "floor_asserted": True,
               "no_per_target_tuning": True}}
    n_pass = sum(1 for g in gates.values() if g["pass"])
    f3_line = (f"F3 {branches['H0']}/{branches['H4']}"
               if f3 else
               f"F3 DEGRADES "
               f"({sum(len(c['rings_over_bar']) for _, c in cones)} "
               f"ring(s) over the {WALK_BAR} bar)")
    verdict = (f"{n_pass}/4 gates (F1 F2 F3 F4) | "
               f"F1 {'6 window-implied rings complete 6/6 cones' if f1 else 'INCOMPLETE/OVER-BAR'} | "
               f"F2 {'frozen prefix bit-exact; plan sourced from the emissions' if f2 else 'DRIFT'} | "
               f"{f3_line}")

    # ---- DISCLOSED non-gating diagnostic: the provenance-identity
    #      cross-check against exp223's deposit. The walk trajectory
    #      is plan-independent (P5's window carries adjacency only),
    #      and P6 makes the committed record the ring's own read
    #      output — so the window-implied plan (sourced from the
    #      emission record) can be compared bit-exactly against
    #      exp223's committed-carry errs as deposited. A match
    #      localizes the boundary errs to the STRUCTURE alone
    #      (provenance-invariant), not to the plan's value
    #      provenance. ----------------------------------------------
    with open(DEP223) as fh:
        dep223 = json.load(fh)
    disc_rows = []
    for hn in ("H0", "H4"):
        new = {c["seed"]: c for c in secs[hn]["walk"]["cones"]}
        old = {c["seed"]: c
               for c in dep223["sections"][hn]["walk"]["cones"]}
        for s in sorted(new):
            errs_n = new[s]["ring_errs_mV"]
            errs_o = old[s]["ring_errs_mV"]
            disc_rows.append({
                "host": hn, "seed": s,
                "frozen_sha256_16_match":
                    new[s]["frozen_sha256_16"]
                    == old[s]["frozen_sha256_16"],
                "ring_errs_bitidentical_3dp": errs_n == errs_o,
                "max_abs_err_delta_3dp":
                    round(max(abs(a - b)
                              for a, b in zip(errs_n, errs_o)), 6)
                    if len(errs_n) == len(errs_o) else None})
    n_hash = sum(r["frozen_sha256_16_match"] for r in disc_rows)
    n_errs = sum(r["ring_errs_bitidentical_3dp"] for r in disc_rows)
    merged["disclosures"] = {
        "exp223_provenance_identity": {
            "clause": ("NON-GATING diagnostic: P6 makes the committed "
                       "record the ring's own read output, so the "
                       "window-implied plan (sourced from the "
                       "emission record) is compared against "
                       "exp223's committed-carry errs as deposited; "
                       "a bit-exact match proves the boundary errs "
                       "are PROVENANCE-INVARIANT — the committed "
                       "carry and the emission carry are the same "
                       "object, and the exp223 boundary is "
                       "structural, not a value-provenance artifact"),
            "n_cones_frozen_hash_match": int(n_hash),
            "n_cones": len(disc_rows),
            "all_frozen_hashes_match": bool(n_hash == len(disc_rows)),
            "all_ring_errs_bitidentical_3dp":
                bool(n_errs == len(disc_rows)),
            "per_cone": disc_rows}}

    merged["gates"] = gates
    merged["verdict"] = verdict
    merged["wall_s"] = round(_time.time() - t0, 1)
    merged["pre_registered"] = {
        "gates_source": ("module docstring, committed before any run "
                         "(pre-registration 711bba0, batch 13; gates "
                         "F1-F4 fixed there, each evaluated exactly "
                         "once)"),
        "window_implied_rule_operationalization": (
            "round k's target at the frontier = round k-1's EMITTED "
            "values at the previously-frontier cells propagated by "
            "exp94's spec_target_n over the canon base (the plan "
            "vector built by the spec_target_n instrument call: the "
            "previously-frontier cells as width-one zones carrying "
            "their own round-(k-1) emissions over the canon base); "
            "the frontier cells' target = the round-(k-1) emission of "
            "their nearest committed ring neighbor (highest ring "
            "index; same-ring ties resolved on the canon labeling — "
            "canon match, else lowest cell index) — deterministic, "
            "zero knobs; the emission, not the committed frozen "
            "value, is what propagates — the exp223 refutation's own "
            "diagnosis; the plan builder never receives the "
            "committed/frozen record (GATE-F2's clause, structural); "
            "round 1's previous round is the seed (the P3 plan — the "
            "pre-named sole external injection); T_plan is consumed "
            "solely by the P3 seed initialization; the emission "
            "record = the ring's own read output (the read's final V, "
            "exp223's ring_V machinery verbatim)")},
    merged["protocol_constants"] = {
        "rings": RINGS, "walk_seeds": [1, 2, 3],
        "walk_err_bar_mV": WALK_BAR, "f_hosts": ["H0", "H4"],
        "S_star": [64.0, 0.0], "wiring_id":
            ("exp148.read_scoped | exp178 production wiring | "
             "T=1 static window -> R_T -> execute_signed@STAR_OP"),
        "propagation_rule": secs["H0"]["walk"]["propagation_rule"]}
    with open(merged_path, "w") as fh:
        json.dump(merged, fh, indent=1, default=float)
    print(f"  === {verdict} ===")
    for g in ("F1", "F2", "F3", "F4"):
        print(f"  GATE-{g}: {'PASS' if gates[g]['pass'] else 'REFUTE'}")
    print(f"  deposited {merged_path}")
    return merged


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
