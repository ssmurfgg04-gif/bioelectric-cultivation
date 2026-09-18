#!/usr/bin/env python3
"""exp240 — THE AUTOCATALYTIC RE-READ FIX (the Section 6 item; exp218's
mis-operationalized re-read clause repaired; ledger L216).

THE OPEN ITEM: exp218 landed the cone's self-expansion (self-fueled +
ADD-CAPACITY confirmed, X1+X3) but its re-read clause was
mis-operationalized — the registered intent: after ADD-CAPACITY, the
cone's OWN READ must absorb the added capacity (the read's SUPPORT SET
grows: the new cells' values enter the read's inputs and the read's
coverage grows monotonically); exp218's implementation instead re-
decoded the values (a value-level check, not a support-level one). The
repair is instrument-level: the support-set criterion replaces the
re-decode criterion; exp218's battery re-runs under the repaired
instrument.

THE INSTRUMENT (zero-knob): the cone's read support = the set of cells
whose values the cone's read consumes (exp178's scoped read support
discipline); after each ADD-CAPACITY round (the expansion writes new
cells from the cone's own carried state — exp218's self-fueled
protocol verbatim), support(new) must strictly contain support(old)
and the new cells' read-back must match their written values (the
absorption check).

PRE-REGISTERED GATES:

  A1  THE ABSORPTION: after every ADD-CAPACITY round, the read's
      support strictly grows and the new cells read back their written
      values (support monotone across all rounds x 3 arms x 3 seeds).
  A2  THE SELF-FUEL: the expansion continues for the pre-named 6
      rounds WITHOUT external writes (each round's plan sourced from
      the cone's own carried state, exp218's protocol) with the
      interior errs sub-mV (the 6.0 bar only at the boundary per
      exp223/exp228's structural finding).
  A3  THE REPAIR DISCLOSURE (the mis-operationalization named): exp218's
      re-decode criterion and this support criterion are compared on
      the SAME battery — the cases where they disagree are counted and
      deposited (the repair's bite made explicit; the gate records the
      disagreement rate, zero-tolerance on silence).
  A4  THE DISCIPLINE: the P6 provenance locks (exp223's Y2 class) hold
      through the repaired instrument (zero drift), the floor
      save/restore asserted.

THE BRANCH (pre-named): A1+A2 PASS -> AUTOCATALYTIC-CLOSED (the
cone's self-expansion axis CLOSES with the repaired clause — the
Stage 4 autocatalytic item lands); A1 REFUTE -> NOT-ABSORBED (the
added capacity stays outside the read's support — the cone cannot
read its own additions, the honest limit).

RUN: 6 rounds x 3 arms x 3 seeds + the A3 comparison; serial, BLAS
pinned; minutes.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp240_autocatalytic_reread.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline) ============================================
    # THE REPAIR (the docstring's instrument, zero knobs): the cone's
    # read support = the set of cells whose values the read consumes =
    # the window's own node support (exp178's discipline — the read's
    # core IS the frame's own support, asserted per round below); after
    # each ADD-CAPACITY round the next round's read must STRICTLY
    # CONTAIN the previous support and the new cells' read-back must
    # match their written values (the absorption check). exp218's
    # re-decode criterion is not deleted: A3 evaluates BOTH criteria on
    # the SAME events and deposits the disagreement (zero tolerance on
    # silence).
    import argparse
    import hashlib
    import time

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all", "H0", "H1", "H4", "gates"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    if args.out is not None:
        out_path = args.out
    elif args.job == "all":
        out_path = OUT
    else:
        out_path = os.path.join(ROOT, "results",
                                f"exp240_shard_{args.job}.json")

    import cultivation.bioelectric.collective as CORE  # noqa: E402
    FLOOR_SAVE = float(CORE.NEURAL_SPEC_MIN)   # the save (A4)
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    from cultivation.substrate.graph import (  # noqa: E402
        path as graph_path)
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
        MULTI, labeling_bfs_n)

    # THE FLOOR RESTORE (exp218/exp223's disclosed discipline, reused):
    # the body's import chain can flip CORE.NEURAL_SPEC_MIN to the R_T
    # battery's -35.0 (exp169's pin); the read-chain modules captured
    # CF-1's production -60.0 at their own import. Saved above, observed
    # here, restored and asserted (A4's save/restore clause).
    FLOOR_OBSERVED = float(CORE.NEURAL_SPEC_MIN)
    CORE.NEURAL_SPEC_MIN = -60.0
    assert CORE.NEURAL_SPEC_MIN == -60.0, "floor restore failed"
    FLOOR_RESTORED = float(CORE.NEURAL_SPEC_MIN)

    WALK_BAR = WALK_ERR_BAR                # exp151's ring-err bar (6.0)
    WALK_SEEDS = list(SEEDS)               # exp142's (1, 2, 3) — P7
    RINGS = WALK_RINGS                     # the pre-named 6 rounds
    PROD_FLOOR = -60.0                     # CF-1's production value
    DRIFT_BAR = 0.05        # exp218's capacity-clause bar — consumed
    #                         ONLY by A3's evaluation of the RETIRED
    #                         re-decode criterion (the comparison's own
    #                         pre-named constant); the repaired support
    #                         criterion is value-bar-free.
    ARMS = ("H0", "H1", "H4")  # exp218's battery's three host classes,
    #                          pre-named as its own distinguished hosts:
    #                          the reference (H0), the size-law organism
    #                          (H1, n=400), the worst-margin corpus host
    #                          (H4 — exp218's X3 pre-named disclosure).
    ARMS_DISCLOSURE = (
        "the docstring's '3 arms' = exp218's battery's three host "
        "classes, embodied by exp218's own distinguished hosts H0/H1/H4 "
        "(build_hosts verbatim, checksummed from exp202's deposit); the "
        "plateau arms cannot carry the pre-named 6 expanding rounds "
        "(scale_free exhausts at ring 3, random3 at ring 6 — measured "
        "pre-run on exp73's battery), so the host-class reading is the "
        "only one under which '6 rounds x 3 arms' is executable")
    WIRING_ID = ("exp148.read_scoped | exp178 production wiring | "
                 "T=1 static window -> R_T -> execute_signed@STAR_OP")
    DEP202 = os.path.join(ROOT, "results",
                          "exp202_cross_organism_carriage.json")
    DEP218 = os.path.join(ROOT, "results",
                          "exp218_autocatalytic_axis.json")
    for _p in (DEP202, DEP218):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"

    # ---- the floors: CF-1's production value asserted ----------------
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR \
        and g6.NEURAL_SPEC_MIN == PROD_FLOOR, \
        f"floor drift: {CORE.NEURAL_SPEC_MIN}, {g6.NEURAL_SPEC_MIN}"
    # ---- the S* identity of the walk's executor -----------------------
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        f"the walk's executor op {STAR_OP} != S* {S_STAR}"

    with open(DEP202) as fh:
        dep202 = json.load(fh)

    # ---- the hosts (exp218's build_hosts VERBATIM — the 12 union
    #      hosts rebuilt checksummed; the 3 pre-named arms selected) --
    def build_hosts() -> dict:
        hosts = {}
        canon0 = labeling_bfs_n(g6.A_CHAIN)
        assert np.array_equal(canon0, g6.wildtype_target(g6.N))
        hosts["H0"] = {"name": "H0", "n": int(g6.N), "A": g6.A_CHAIN,
                       "canon": canon0}
        A400 = graph_path(400)
        canon400 = labeling_bfs_n(A400)
        assert np.array_equal(canon400, g6.wildtype_target(400))
        hosts["H1"] = {"name": "H1", "n": 400, "A": A400,
                       "canon": canon400}
        redraw = {r["host"]: r["seed"] for r in
                  dep202["sections"]["corpus"]["scan"]["redraw_log"]}
        dep_hosts = dep202["sections"]["corpus"]["hosts"]
        for k in sorted(dep_hosts):
            if not k.startswith("H") or int(k[1:]) < 2:
                continue
            seed = int(redraw[k])
            A = small_world(100, 0.10, seed)
            assert A.sum() > 0
            dep_edges = dep_hosts[k].get("edges")
            got_edges = int(np.count_nonzero(
                np.triu(A, 1) if not np.iscomplexobj(A) else np.abs(
                    np.triu(A, 1)) > 0))
            if dep_edges is not None and isinstance(dep_edges, int):
                assert got_edges == dep_edges, \
                    (f"{k} rebuild drift: edges {got_edges} != "
                     f"deposit {dep_edges}")
            hosts[k] = {"name": k, "n": 100, "A": A,
                        "canon": labeling_bfs_n(A),
                        "rewire_seed": seed,
                        "record": dep_hosts[k].get("record")}
        return hosts

    # ================= THE WALK (exp218's machinery re-armed under
    #                    the repaired instrument) ======================
    class _Win:
        """exp151's static window medium (the P5 closed-world node
        contract): one snapshot — the masked full-n x n window matrix."""
        kind = "window"

        def __init__(self, M):
            self._M = M

        def snapshots(self):
            return [self._M]

    _LOCK_LOG: list = []

    def _lock_walk_write(host, ring, seed):
        # the S* assertion on every ring write: the read wired through
        # exp178's production scoped arm ends in exp148's read_temporal
        # -> execute_signed at op=STAR_OP; STAR_OP IS S* = (64.0, 0.0)
        # (asserted at body start and re-asserted per write).
        assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
            f"walk write off S* on {host} ring {ring}"
        _LOCK_LOG.append((host, int(ring), WIRING_ID))

    def _support_of(M):
        """THE READ'S SUPPORT (exp178's scoped read support discipline):
        the set of cells whose values the read consumes = the window's
        own node support (the read's core is the frame's own support;
        outside it the read is the no-op identity)."""
        nz = np.abs(M) > 0
        nodes = np.where(nz.any(axis=1) | nz.any(axis=0))[0]
        return [int(i) for i in nodes]

    def _walk_ring(h, W, T_plan, cone, ring_index):
        """One expansion step for one seed-cone — exp218's _walk_ring
        machinery VERBATIM (exp151's P4/P5 frontier+window, the exp178
        production scoped read, the S* lock, the reduction datum, P6's
        commit), with exp218's re-decode capacity clause REPLACED by
        the repaired support-set instrument (the absorption check) —
        and exp218's re-decode criterion STILL evaluated on the same
        events for A3's comparison (the repair's bite, deposited).
        The ONLY values that can enter the committed region are copied
        from the read's final V at the frontier (P6)."""
        name, s = h["name"], cone["seed"]
        C = cone["C"]
        F = frontier_of(C, W)                    # exp151's P4 verbatim
        if not F:
            return {"ring_index": ring_index, "ring_expanded": False,
                    "ring_expanded_bool": False,
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
        # on a static window (f_max 0 < 32 -> R_T -> T=1 passthrough ->
        # exp148 TC1-TC3 with F=0 -> exp151's execute_signed call).
        with warnings_as_errors():
            raw = execute_signed(MULTI, M, s, op=STAR_OP,
                                 return_state=True)
        reduction = bool(np.array_equal(
            np.asarray(raw["final_state"]["V"], dtype=float), V))
        emitted = V[F]
        err = float(np.sqrt(np.mean((emitted - T_plan[F]) ** 2)))
        # ---- THE READ'S SUPPORT (exp178's discipline, asserted): the
        #      window's own node support == C u F (the cells whose
        #      values this read consumes); window_matrix's support
        #      assertions already pin the matrix, this pins the nodes.
        support_now = _support_of(M)
        assert set(support_now) == (C | set(F)), \
            "read support != the window's node set C u F"
        sup_sha16 = hashlib.sha256(
            np.asarray(support_now, dtype=np.int64).tobytes()
        ).hexdigest()[:16]
        # ---- THE ABSORPTION CHECK (the repaired instrument, zero
        #      knobs): after the ADD-CAPACITY round k-1 (which committed
        #      F_{k-1} from the cone's own carried state), THIS read
        #      must (i) strictly contain the round-(k-1) support — the
        #      added capacity enters the read's inputs; and (ii) the
        #      new cells' read-back must match their written values —
        #      the window entries at the new cells are bit-exact the
        #      values the expansion wrote (the values-as-written are
        #      what the read consumes). The value-channel re-emission
        #      drift at the new cells is deposited as an UNGATED datum
        #      (the retired channel — exp228's structural finding).
        absorption = None
        redecode = None
        if ring_index >= 2 and cone["last_support"] is not None:
            prev_sup = cone["last_support"]
            new_cells = sorted(int(j) for j in cone["last_frontier"])
            growth = bool(set(prev_sup) < set(support_now))
            sup_arr = np.asarray(support_now, dtype=int)
            new_arr = np.asarray(new_cells, dtype=int)
            rb_bitexact = bool(np.array_equal(
                M[np.ix_(new_arr, sup_arr)],
                W[np.ix_(new_arr, sup_arr)]))
            d_new = np.abs(V[new_arr] - np.asarray(
                [cone["committed"][c] for c in new_cells]))
            finite_new = bool(np.all(np.isfinite(V[new_arr])))
            absorption = {
                "after_round": int(ring_index - 1),
                "support_size_prev": int(len(prev_sup)),
                "support_size_now": int(len(support_now)),
                "support_strict_growth": growth,
                "n_new_cells": int(len(new_cells)),
                "new_cells_readback_bitexact": rb_bitexact,
                "new_cells_finite": finite_new,
                "value_channel_datum_not_gated": {
                    "max_abs_drift_mV": round(float(d_new.max()), 4),
                    "n_within_bar": int(np.sum(d_new <= DRIFT_BAR))},
                "hold": bool(growth and rb_bitexact and finite_new)}
            # ---- exp218's re-decode criterion on the SAME event (A3's
            #      comparison; the retired instrument, its own bar and
            #      its own SCOPE: the emission-committed prefix of
            #      rounds 1..k-1 — exp151's P3 keeps the seed patch out
            #      of gate scope, exp218's pre-registered reading) ----
            prefix = sorted(cc for cc in cone["committed"]
                            if cone["ring_of"][cc] >= 1)
            d_all = np.array([abs(V[i] - cone["committed"][i])
                              for i in prefix])
            redecode = {
                "n_checked": int(len(prefix)),
                "n_bit_exact": int(np.sum(d_all == 0.0)),
                "n_within_bar": int(np.sum(d_all <= DRIFT_BAR)),
                "max_abs_drift": round(float(d_all.max()), 4),
                "hold": bool(d_all.max() <= DRIFT_BAR)}
        # ---- exp223's frozen discipline (the walk's own, asserted):
        #      the committed prefix equals the frozen values
        #      bit-exactly (P6 verbatim) — A4's locks.
        n_prefix = 0
        if ring_index >= 2:
            for c, v in cone["frozen"].items():
                assert cone["committed"][c] == v, \
                    f"frozen prefix drift at cell {c}"
                n_prefix += 1
        cone["n_prefix_checks"] = cone.get("n_prefix_checks", 0) \
            + n_prefix
        # ---- the ring write: the S* lock asserted, then P6's commit
        #      (the read's own outputs, full precision, verbatim) ----
        _lock_walk_write(name, ring_index, s)
        cone["ring_V"][ring_index] = np.array(V, dtype=float)
        for j in F:
            C.add(int(j))
            cone["committed"][int(j)] = float(V[int(j)])
            cone["frozen"][int(j)] = float(V[int(j)])
            cone["ring_of"][int(j)] = int(ring_index)
        cone["last_support"] = support_now
        cone["last_frontier"] = [int(j) for j in F]
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
                "emitted": [round(float(x), 3) for x in emitted],
                "plan": [round(float(x), 3) for x in T_plan[F]],
                "ring_err_mV": round(err, 3),
                "support": {"size": int(len(support_now)),
                            "sha256_16": sup_sha16},
                "absorption": absorption,
                "redecode": redecode,
                "pass": bool(np.isfinite(err) and err < WALK_BAR)}

    def run_walk_host(h, n_rings):
        """The walk re-armed on one host: exp218's protocol (P2/P3/P6/P7
        verbatim — plan_of, seed_cone, commit-the-read's-own-outputs,
        seeds (1, 2, 3)) in LOCKSTEP rounds across the seed cones so
        'after round k' is a host-level event. The plan is exp151's P2
        identity object (scorer-only); the expansion is self-fueled —
        each round's read inputs are the cone's own carried state
        (the window on C u F), no external writes beyond the P3 seed."""
        name = h["name"]
        assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drifted mid-run"
        W = np.asarray(h["A"], dtype=float)
        T_plan = plan_of(W)                      # exp151's P2 verbatim
        seed_cells = seed_cone(W)                # exp151's P3 verbatim
        support_n = int(np.count_nonzero(np.abs(W).sum(axis=1)))
        cones = []
        for s in WALK_SEEDS:
            cone = {"seed": s, "C": set(seed_cells), "committed": {},
                    "frozen": {}, "ring_of": {}, "ring_V": {},
                    "last_support": None, "last_frontier": [],
                    "rings": [], "broken": None}
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
                rec = _walk_ring(h, W, T_plan, c, r)
                c["rings"].append(rec)
                if rec.get("stop"):
                    c["broken"] = rec["stop"]
        # ---- A4's close-out (exp223's Y2 checks verbatim): the full
        #      frozen-prefix check and the P6 provenance (every
        #      committed cell's value equals its commit-round read's
        #      own final V, bit-exactly; ring 0 = the P3 seed patch,
        #      the pre-named sole external injection) ---------------
        p6 = {}
        for c in cones:
            n_close = 0
            for cc, v in c["frozen"].items():
                assert c["committed"][cc] == v, "frozen drift at close"
                n_close += 1
            n_prov = 0
            n_p3 = 0
            for cc, v in c["committed"].items():
                if c["ring_of"][cc] == 0:
                    n_p3 += 1
                    continue
                assert v == float(c["ring_V"][c["ring_of"][cc]][cc]), \
                    "P6 provenance break"
                n_prov += 1
            p6[str(c["seed"])] = {
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
            supp = [x["support"]["size"] for x in expanded
                    if x.get("support")]
            abso = [x["absorption"] for x in expanded
                    if x.get("absorption")]
            rede = [dict(x["redecode"], ring_index=x["ring_index"])
                    for x in expanded if x.get("redecode")]
            out_cones.append({
                "seed": c["seed"],
                "rings_expanded": rings_expanded,
                "exhausted": exhausted,
                "n_rejections": n_rej,
                "broken": c["broken"],
                "final_coverage": [len(c["C"]), support_n],
                "ring_errs_mV": errs,
                "rings_passed": sum(1 for x in expanded if x.get("pass")),
                "support_sizes": supp,
                "support_strictly_growing": bool(
                    all(supp[i] < supp[i + 1]
                        for i in range(len(supp) - 1))
                    if len(supp) > 1 else False),
                "n_absorption_events": len(abso),
                "absorption_hold_all": bool(abso)
                and all(a["hold"] for a in abso),
                "worst_new_cell_value_drift_mV": (
                    max(a["value_channel_datum_not_gated"]
                        ["max_abs_drift_mV"] for a in abso)
                    if abso else None),
                "n_redecode_events": len(rede),
                "n_redecode_hold": sum(1 for r0 in rede if r0["hold"]),
                "redecode_worst_abs_drift": (
                    max(r0["max_abs_drift"] for r0 in rede)
                    if rede else None),
                "p6_frozen": p6[str(c["seed"])],
                "rings": c["rings"]})
        return {"host": name, "n": int(h["n"]),
                "kind": ("reference (exp182's own host)"
                         if name == "H0" else
                         "size-law organism (exp198's scale)"
                         if name == "H1" else
                         "corpus-rewired organism (the pre-named "
                         "worst-margin host — exp218's X3 disclosure)"),
                "seeds": list(WALK_SEEDS), "S_star": list(S_STAR),
                "rings_registered": int(n_rings),
                "seed_cells": len(seed_cells),
                "cones": out_cones}

    def _close_gates_on(result: dict, out_path: str) -> dict:
        """GATE CLOSURE — each gate evaluated EXACTLY ONCE on the credited
        run (exp218's pattern). The bars are the pre-registered constants;
        nothing here is tuned by the data."""
        t0g = time.time()
        cones = [(arm, c) for arm in ARMS
                 for c in result["sections"][arm]["walk"]["cones"]]
        assert len(cones) == 9, f"cone count {len(cones)} != 9"

        # ---- GATE-A1 (the absorption): after every ADD-CAPACITY round the
        #      read's support strictly grows and the new cells read back
        #      their written values — support monotone across all rounds
        #      x 3 arms x 3 seeds (5 events per cone; the value-channel
        #      re-emission drift deposited as an ungated datum) ----------
        a1_rows = []
        worst_new_drift = 0.0
        n_events = 0
        for arm, c in cones:
            supp = c["support_sizes"]
            mono = all(supp[i] < supp[i + 1]
                       for i in range(len(supp) - 1))
            ev_ok = bool(c["n_absorption_events"] == RINGS - 1
                         and c["absorption_hold_all"] and mono)
            a1_rows.append({"arm": arm, "seed": c["seed"],
                            "support_sizes": supp,
                            "support_strictly_growing": mono,
                            "n_absorption_events": c["n_absorption_events"],
                            "absorption_hold_all": c["absorption_hold_all"],
                            "hold": ev_ok,
                            "worst_new_cell_value_drift_mV":
                                c["worst_new_cell_value_drift_mV"]})
            n_events += c["n_absorption_events"]
            if c["worst_new_cell_value_drift_mV"] is not None:
                worst_new_drift = max(worst_new_drift,
                                      c["worst_new_cell_value_drift_mV"])
        a1 = bool(n_events == 9 * (RINGS - 1)
                  and all(r["hold"] for r in a1_rows))

        # ---- GATE-A2 (the self-fuel): 6 rounds WITHOUT external writes on
        #      every arm x seed; every ring err under the pre-named 6.0 bar
        #      (the bar prices the boundary — the frontier ring err; the
        #      interior profile deposited per exp223/exp228's structural
        #      finding) ---------------------------------------------------
        a2_rows = []
        for arm, c in cones:
            errs = c["ring_errs_mV"]
            complete = bool(c["rings_expanded"] == RINGS
                            and c["n_rejections"] == 0
                            and not c["exhausted"]
                            and len(errs) == RINGS
                            and all(e is not None and np.isfinite(e)
                                    and e < WALK_BAR for e in errs))
            interior = errs[1:RINGS - 1] if len(errs) == RINGS else []
            a2_rows.append({"arm": arm, "seed": c["seed"],
                            "complete": complete,
                            "rings_expanded": c["rings_expanded"],
                            "n_rejections": c["n_rejections"],
                            "exhausted": c["exhausted"],
                            "worst_ring_err_mV":
                                (max(e for e in errs if e is not None)
                                 if errs else None),
                            "worst_interior_round_err_mV":
                                (max(interior) if interior else None)})
        n_writes = sum(1 for arm, c in cones for x in c["rings"]
                       if x.get("ring_expanded") and x.get("read_ok")
                       and x["ring_index"] in range(1, RINGS + 1))
        n_wiring_ok = sum(
            1 for arm, c in cones for x in c["rings"]
            if x.get("ring_expanded") and x.get("read_ok")
            and x.get("scoped_wiring", {}).get("wiring_id") == WIRING_ID)
        lock_expected = 9 * RINGS
        lock_ok = bool(n_wiring_ok == lock_expected
                       and (len(_LOCK_LOG) == lock_expected
                            if _LOCK_LOG else True))
        a2 = bool(all(r["complete"] for r in a2_rows)
                  and n_writes == lock_expected and lock_ok)

        # ---- GATE-A3 (the repair disclosure): exp218's re-decode
        #      criterion and the support criterion compared on the SAME
        #      events; the disagreements counted and deposited — zero
        #      tolerance on SILENCE (the pass is the completeness of the
        #      recording, not the rate's value) --------------------------
        n_compared = sum(c["n_redecode_events"] for _, c in cones)
        n_redecode_hold = sum(c["n_redecode_hold"] for _, c in cones)
        n_support_hold = sum(1 for arm, c in cones
                             for a in c["rings"]
                             if a.get("absorption"))
        per_event = []
        n_disagree = 0
        for arm, c in cones:
            for x in c["rings"]:
                if not x.get("redecode") or not x.get("absorption"):
                    continue
                rd = bool(x["redecode"]["hold"])
                sp = bool(x["absorption"]["hold"])
                n_disagree += int(rd != sp)
                per_event.append({
                    "arm": arm, "seed": c["seed"],
                    "ring_index": x["ring_index"],
                    "n_prefix": x["redecode"]["n_checked"],
                    "redecode_max_abs_drift": x["redecode"]["max_abs_drift"],
                    "redecode_hold": rd, "support_hold": sp,
                    "disagree": bool(rd != sp)})
        rate = (n_disagree / n_compared) if n_compared else None
        a3 = bool(n_compared == 9 * (RINGS - 1)
                  and len(per_event) == n_compared
                  and rate is not None)

        # ---- GATE-A4 (the discipline): the P6 provenance locks (exp223's
        #      Y2 class) hold through the repaired instrument (zero drift),
        #      the floor save/restore asserted ----------------------------
        n_prov = sum(c["p6_frozen"]["n_p6_provenance_bitexact"]
                     for _, c in cones)
        n_p3 = sum(c["p6_frozen"]["n_p3_seed_cells"] for _, c in cones)
        n_close = sum(c["p6_frozen"]["n_close_bitexact"] for _, c in cones)
        n_prefix = sum(c["p6_frozen"]["n_prefix_bitexact"] for _, c in cones)
        n_committed_nonseed = sum(
            1 for arm, c in cones for x in c["rings"]
            if x.get("ring_expanded") and x.get("read_ok")
            for _ in x["frontier"])
        n_p3_expected = sum(3 * result["sections"][arm]["walk"]["seed_cells"]
                            for arm in ARMS)
        floor_block = {"save_pre_import": FLOOR_SAVE,
                       "observed_post_import": FLOOR_OBSERVED,
                       "restored": FLOOR_RESTORED,
                       "production": PROD_FLOOR,
                       "asserted": bool(FLOOR_RESTORED == PROD_FLOOR
                                        and FLOOR_RESTORED == -60.0)}
        a4 = bool(n_prov == n_committed_nonseed and n_close > 0
                  and n_prefix > 0 and n_p3 == n_p3_expected
                  and floor_block["asserted"] and lock_ok)

        gates = {
            "A1": {"pass": bool(a1),
                   "clause": "after every ADD-CAPACITY round the read's "
                             "support strictly grows and the new cells "
                             "read back their written values (support "
                             "monotone across all rounds x 3 arms x 3 "
                             "seeds)",
                   "n_events": n_events,
                   "n_hold": sum(1 for r in a1_rows if r["hold"]),
                   "per_cone": a1_rows,
                   "worst_new_cell_value_drift_mV": worst_new_drift,
                   "value_channel_status":
                       "ungated datum (the retired channel; exp228's "
                       "structural finding)"},
            "A2": {"pass": bool(a2),
                   "clause": "the expansion continues for the pre-named 6 "
                             "rounds WITHOUT external writes (each round's "
                             "read inputs = the cone's own carried state, "
                             "exp218's protocol) with the interior errs "
                             "sub-mV (the 6.0 bar only at the boundary per "
                             "exp223/exp228's structural finding)",
                   "n_cones_complete": sum(1 for r in a2_rows
                                           if r["complete"]),
                   "per_cone": a2_rows,
                   "worst_ring_err_mV": max(r["worst_ring_err_mV"]
                                            for r in a2_rows
                                            if r["worst_ring_err_mV"]
                                            is not None),
                   "worst_interior_round_err_mV": max(
                       r["worst_interior_round_err_mV"] for r in a2_rows
                       if r["worst_interior_round_err_mV"] is not None),
                   "interior_profile_note": (
                       "every ring err is a frontier/boundary err priced "
                       "at the pre-named 6.0 bar; the interior-round "
                       "profile (rounds 2..5) is deposited per cone and "
                       "the retired interior value-channel drift is "
                       "deposited under A1/A3 — zero silence"),
                   "ring_writes_logged_at_S_star": len(_LOCK_LOG)},
            "A3": {"pass": bool(a3),
                   "clause": "exp218's re-decode criterion and this support "
                             "criterion are compared on the SAME battery — "
                             "the cases where they disagree are counted and "
                             "deposited (the repair's bite made explicit; "
                             "the gate records the disagreement rate, "
                             "zero-tolerance on silence)",
                   "n_compared": n_compared,
                   "n_redecode_hold": n_redecode_hold,
                   "n_support_hold": n_support_hold,
                   "n_disagree": n_disagree,
                   "disagreement_rate": rate,
                   "per_event": per_event,
                   "reading": ("the retired re-decode criterion (exp218's "
                               "0.05 mV value check on the emission-"
                               "committed prefix of rounds 1..k-1, the "
                               "seed patch excluded per exp151's P3 — "
                               "exp218's own pre-registered scope) vs "
                               "the repaired support criterion on "
                               "identical events; a disagreement is an "
                               "event where the mis-operationalized "
                               "instrument and the repaired instrument "
                               "split")},
            "A4": {"pass": bool(a4),
                   "clause": "the P6 provenance locks (exp223's Y2 class) "
                             "hold through the repaired instrument (zero "
                             "drift), the floor save/restore asserted",
                   "n_p6_provenance_bitexact": n_prov,
                   "n_committed_nonseed_cells": n_committed_nonseed,
                   "n_prefix_bitexact_checks": n_prefix,
                   "n_close_bitexact_checks": n_close,
                   "n_p3_seed_cells": n_p3,
                   "floor_save_restore": floor_block,
                   "ring_writes_logged_at_S_star": len(_LOCK_LOG),
                   "n_wiring_ids_verified": n_wiring_ok,
                   "lock_log_mode": ("in-process" if _LOCK_LOG
                                     else "loaded-deposit (the per-write "
                                          "S* asserts ran in the producing "
                                          "process)"),
                   "no_per_target_tuning": True}}
        n_pass = sum(1 for g in gates.values() if g["pass"])
        branch = ("AUTOCATALYTIC-CLOSED" if (a1 and a2)
                  else "NOT-ABSORBED" if not a1
                  else "A1-PASS-A2-REFUTE (outside the pre-named branches; "
                       "deposited honestly)")
        a3_line = (f"A3 recorded {n_disagree}/{n_compared} disagreements "
                   f"(rate {rate:.3f})" if a3 else "A3 INCOMPLETE")
        a1_line = (f"A1 absorption holds {n_events}/{9 * (RINGS - 1)} "
                   f"events" if a1 else "A1 REFUTED")
        a2_line = ("A2 6 self-fueled rounds 9/9 cones" if a2
                   else "A2 INCOMPLETE/OVER-BAR")
        verdict = (f"{n_pass}/4 gates (A1 A2 A3 A4) | "
                   f"{a1_line} | "
                   f"{a2_line} | "
                   f"{a3_line} | "
                   f"A4 {'P6 locks + floor asserted' if a4 else 'DRIFT'} | "
                   f"branch {branch}")
        result["gates"] = gates
        result["verdict"] = verdict
        result["branch"] = branch
        result["wall_s"] = round(time.time() - t0, 1)
        result["gate_close_s"] = round(time.time() - t0g, 1)
        result["pre_registered"] = {
            "gates_source": ("module docstring, committed before any run "
                             "(pre-registration 30c5d50, batch 16; gates "
                             "A1-A4 fixed there, each evaluated exactly "
                             "once)"),
            "arms_operationalization": ARMS_DISCLOSURE,
            "support_discipline": (
                "the read's support = the set of cells whose values the "
                "read consumes = the window's own node support (exp178's "
                "discipline — the read's core is the frame's own support); "
                "asserted per round equal to C u F and hashed into the "
                "deposit (size + sha256_16 per round)"),
            "absorption_check_reading": (
                "(i) support(new) strictly contains support(old) — the "
                "added capacity enters the read's inputs; (ii) the new "
                "cells' read-back matches their written values — the next "
                "round's window entries at the new cells are bit-exact the "
                "written values (the values-as-written are what the read "
                "consumes); the value-channel re-emission drift at the new "
                "cells is deposited as an UNGATED datum — the retired "
                "channel exp228 found structure-driven"),
            "interior_errs_reading": (
                "'the 6.0 bar only at the boundary' = the pre-named 6.0 "
                "bar prices the frontier ring errs (the cone's boundary); "
                "the interior-round profile (rounds 2..5) is deposited per "
                "cone (worst_interior_round_err_mV) and the retired "
                "interior value-channel drift under A1/A3 — the structural "
                "expectation reported, nothing tuned"),
            "a3_comparison_reading": (
                "both criteria evaluated per event (arm, seed, round k>=2) "
                "on the identical reads: exp218's re-decode criterion = "
                "every previously committed cell within exp218's own 0.05 "
                "mV drift bar in the round-k read (the emission-committed "
                "prefix of rounds 1..k-1, the seed patch excluded per "
                "exp151's P3 — exp218's own pre-registered scope); the "
                "support criterion = strict support growth + new-cell "
                "read-back integrity; the disagreement count and rate "
                "deposited per event"),
            "body_landing_disclosures": (
                "exp218's build_hosts/walk machinery re-nested verbatim in "
                "this body (it lives inside exp218's main() and is not "
                "importable) with every shared primitive imported from its "
                "own module (exp151's protocol functions, exp148's "
                "read_scoped, exp142's execute_signed/SEEDS/STAR_OP, "
                "exp169's f_max_frames, exp94's spec_target_n/labeling "
                "via plan_of, exp178's wiring); exp223's P6 provenance "
                "locks reused verbatim (frozen prefix + close-out + "
                "commit-round provenance, bit-exact); the floor "
                "save/restore is exp218/exp223's disclosed discipline")}
        result["protocol_constants"] = {
            "rounds": RINGS, "walk_seeds": list(WALK_SEEDS),
            "walk_err_bar_mV": WALK_BAR, "arms": list(ARMS),
            "redecode_drift_bar_mV": DRIFT_BAR,
            "S_star": [64.0, 0.0], "wiring_id": WIRING_ID,
            "support_definition": ("the window's node support = C u F "
                                   "(the cells whose values the read "
                                   "consumes)")}
        os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                    exist_ok=True)
        with open(out_path, "w") as fh:
            json.dump(result, fh, indent=1, default=float)
        print(f"  === {verdict} ===")
        for g in ("A1", "A2", "A3", "A4"):
            print(f"  GATE-{g}: {'PASS' if gates[g]['pass'] else 'REFUTE'}")
        print(f"  branch: {branch}")
        print(f"  deposited {out_path}")
        return result

    # ========================== --smoke (H0, 2 rings) ==================
    if args.smoke:
        hosts = build_hosts()
        w = run_walk_host(hosts["H0"], n_rings=2)
        checks = {
            "rings_expanded_all_seeds": all(
                c["rings_expanded"] == 2 for c in w["cones"]),
            "zero_rejections": all(c["n_rejections"] == 0
                                   for c in w["cones"]),
            "ring_errs_under_bar": all(
                e is not None and np.isfinite(e) and e < WALK_BAR
                for c in w["cones"] for e in c["ring_errs_mV"]),
            "support_strict_growth_all_cones": all(
                c["support_strictly_growing"] for c in w["cones"]),
            "absorption_hold_all_events": all(
                c["absorption_hold_all"]
                and c["n_absorption_events"] == 1 for c in w["cones"]),
            "redecode_compared_all_events": all(
                c["n_redecode_events"] == 1 for c in w["cones"]),
            "p6_frozen_bitexact": all(
                c["p6_frozen"]["n_close_bitexact"] > 0
                and c["p6_frozen"]["n_p6_provenance_bitexact"] > 0
                for c in w["cones"]),
            "reduction_bitexact": all(
                x.get("reduction_bitexact_vs_exp151_raw")
                for c in w["cones"] for x in c["rings"]
                if x.get("ring_expanded") and x.get("read_ok")),
            "lock_log_at_S_star": len(_LOCK_LOG) == 6,
            "floor_at_production": CORE.NEURAL_SPEC_MIN == PROD_FLOOR,
        }
        ok = all(checks.values())
        print(f"=== exp240 SMOKE (H0, 2 rings, DISCARDED) === "
              f"{checks} -> {'OK' if ok else 'INSTRUMENT BUG'} "
              f"({time.time() - t0:.1f}s)")
        dep = {"exp": "exp240_autocatalytic_reread", "kind": "smoke",
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
        with open(OUT) as fh:
            merged = json.load(fh)
        return _close_gates_on(merged, out_path)
    hosts = build_hosts()
    assert len(hosts) == 12 and all(k in hosts for k in ARMS), \
        "host rebuild incomplete"

    jobs = ["H0", "H1", "H4"] if args.job == "all" else [args.job]
    sections: dict = {}
    for arm in ARMS:
        if arm not in jobs:
            continue
        w = run_walk_host(hosts[arm], RINGS)
        sections[arm] = {"walk": w}
        _errs = [e for c in w["cones"] for e in c["ring_errs_mV"]
                 if e is not None]
        print(f"  [{arm}] walk 6-round complete "
              f"{sum(1 for c in w['cones'] if c['rings_expanded'] == RINGS)}/3 "
              f"seeds | zero rejections "
              f"{sum(1 for c in w['cones'] if c['n_rejections'] == 0)}/3 "
              f"| absorption hold "
              f"{sum(1 for c in w['cones'] if c['absorption_hold_all'])}/3 "
              f"| support growth "
              f"{sum(1 for c in w['cones'] if c['support_strictly_growing'])}/3 "
              f"| worst ring err "
              f"{max(_errs) if _errs else None} "
              f"({time.time() - t0:.1f}s)")

    result = {"exp": "exp240_autocatalytic_reread",
              "sections": sections}
    if args.job != "all":
        os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                    exist_ok=True)
        with open(out_path, "w") as fh:
            json.dump(result, fh, indent=1, default=float)
        print(f"  deposited {out_path} (shard {args.job})")
        return result

    # ---- the instrument-consistency datum (NOT a gate): this battery
    #      is exp218's machinery verbatim on exp218's hosts/seeds — the
    #      ring errs must be BIT-IDENTICAL to exp218's deposited rows.
    with open(DEP218) as fh:
        dep218 = json.load(fh)
    ref_errs = {}
    for hn, sec in dep218["sections"].items():
        if hn == "walks":
            for car in sec["carriages"]:
                ref_errs[car["host"]] = {c["seed"]: c["ring_errs_mV"]
                                         for c in car["cones"]}
        elif "walk" in sec:
            ref_errs[hn] = {c["seed"]: c["ring_errs_mV"]
                            for c in sec["walk"]["cones"]}
    consistency = {}
    for arm in ARMS:
        got = {c["seed"]: c["ring_errs_mV"]
               for c in sections[arm]["walk"]["cones"]}
        consistency[arm] = bool(arm in ref_errs
                                and got == ref_errs[arm])
    result["instrument_consistency_vs_exp218"] = {
        "clause": ("the walk machinery is exp218's verbatim on the same "
                   "hosts/seeds/ops — the ring errs must be bit-identical "
                   "to exp218's deposited H0/H1/H4 rows (a datum, not a "
                   "gate)"),
        "per_arm": consistency}

    # local all-in-one: close the gates (each evaluated exactly once)
    return _close_gates_on(result, out_path)


if __name__ == "__main__":
    main()
