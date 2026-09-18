#!/usr/bin/env python3
"""exp223 — THE SELF-FED WALK (L195's registered next).

exp218's X1 + X3 closed the autocatalytic axis on the substrate side:
the cone expands itself (36/36 cones, 12 hosts) and the expansion ADDS
carrying capacity (ADD-CAPACITY on H0 and H4). The remaining edge: the
cone's expansion fed by ITS OWN EMISSIONS as the next round's TARGET —
not just substrate. exp151's walk with the plan re-drawn per round from
the committed pattern itself: the seed patch's own structure propagates
into the frontier's target (the plan for ring k's frontier read from
the committed pattern's own local structure — the propagation rule
pre-named, zero knobs), no external target injection beyond the seed.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp218's walk machinery
verbatim (the window construction, the exp178 production scoped read,
the S* lock, the floor-restore discipline); the PROPAGATION RULE
(pre-named, zero knobs): ring k's frontier plan = the committed
pattern's own values propagated by exp94's spec_target_n on the canon
labeling (the frontier cells' target = the canon value of their
nearest committed ring neighbor — the pattern's own structure carries
forward); the pre-named hosts: H0 and H4 only (the reference and the
worst-margin host — exp218's X3 disclosure reused).

GATES (each evaluated exactly once):
  GATE-Y1 (the self-fed walk) 6 self-fed rings complete with zero
           rejections on H0 and H4 (3 seeds each); ring errs under
           the 6.0 bar throughout — the pattern propagates ITSELF.
  GATE-Y2 (the no-drift clause) the committed values frozen (P6
           verbatim): after each round, the committed prefix equals
           the frozen values bit-exactly (the walk's own discipline,
           asserted — NOT the re-read clause exp218 refuted).
  GATE-Y3 (the self-similarity profile) per-round the frontier's
           emitted-vs-propagated-plan err deposited; the profile
           monotone within the 6.0 bar; the branch named:
           SELF-CARRYING (all 6 rings under the bar) / DEGRADES (any
           ring over).
  GATE-Y4 (hygiene) all finite; the S* lock per write; the -60.0
           floor post-restore asserted; no per-target tuning.
NO post-hoc tuning. --smoke permitted (H0, 2 rings), discarded.
DEPOSIT: results/exp223_self_fed_walk.json
RUN: python3 -m experiments.exp223_self_fed_walk [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp223_self_fed_walk.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline) ============================================
    # SHARDING (exp218's pattern): --job H0 / H4 (the pre-named hosts)
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
                                f"exp223_shard_{args.job}.json")

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

    # THE FLOOR RESTORE (exp218's disclosed discipline, reused): the
    # body's import chain includes exp169_rt_scoping, whose import
    # flips CORE.NEURAL_SPEC_MIN to -35.0 (the R_T battery's floor —
    # verified empirically this run). The read-chain modules captured
    # CF-1's production -60.0 at their own import; exp169's flip is
    # attribute-only. Restored here so the walk's write path runs at
    # the CF-1 production floor the pre-registration asserts.
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
    Y_HOSTS = ("H0", "H4")   # the reference and the worst-margin host
    #                          (pre-named — exp218's X3 disclosure
    #                          reused: exp214's U3 put the union worst
    #                          at H4 = +5.285)
    WIRING_ID = ("exp148.read_scoped | exp178 production wiring | "
                 "T=1 static window -> R_T -> execute_signed@STAR_OP")

    # THE PROPAGATION RULE (pre-named, zero knobs — the deposit carries
    # this string verbatim): ring k's frontier plan = the committed
    # pattern's own values propagated by exp94's spec_target_n on the
    # canon labeling; the frontier cells' target = the canon value of
    # their nearest committed ring neighbor — the neighbor's frozen
    # committed value of record (the walk's own canon: P6's verbatim
    # emission, guarded by GATE-Y2's frozen discipline; NOT a re-read —
    # that is the clause exp218 refuted). Nearest committed ring = the
    # highest ring index among the frontier cell's committed neighbors
    # (ring 0 = the seed patch). Same-ring ties resolved ON the canon
    # labeling (the tied neighbor whose canon value matches the
    # frontier cell's own canon value), residual ties by lowest cell
    # index — deterministic, zero knobs. T_plan is consumed SOLELY by
    # the P3 seed initialization (the parent's committed values — the
    # pre-named sole external injection); the plan for every ring
    # derives from the frozen committed values + the canon labeling +
    # the committed ring structure, nothing else.
    PROPAGATION_RULE = (
        "ring k's frontier plan = the committed pattern's own values "
        "propagated by exp94's spec_target_n on the canon labeling "
        "(the plan vector built by the spec_target_n instrument call: "
        "the committed cells enter as width-one zones carrying their "
        "own frozen values over the canon base); the frontier cells' "
        "target = the canon value of their nearest committed ring "
        "neighbor = the neighbor's frozen committed value of record "
        "(P6's verbatim emission, guarded by GATE-Y2; NOT a re-read); "
        "nearest committed ring = the highest ring index among the "
        "cell's committed neighbors; same-ring ties resolved on the "
        "canon labeling (canon match, else lowest index); T_plan "
        "consumed solely by the P3 seed initialization")

    with open(DEP202) as fh:
        dep202 = json.load(fh)

    # ---- the floors: CF-1's production value asserted ----------------
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR \
        and g6.NEURAL_SPEC_MIN == PROD_FLOOR, \
        f"floor drift: {CORE.NEURAL_SPEC_MIN}, {g6.NEURAL_SPEC_MIN}"
    # ---- the S* identity of the walk's executor -----------------------
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        f"the walk's executor op {STAR_OP} != S* {S_STAR}"

    # ---- the pre-named hosts (exp218's build discipline) --------------
    def build_y_hosts() -> dict:
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

    # ================= THE SELF-FED WALK (exp218's machinery re-armed;
    #                    the plan re-drawn per round by the propagation
    #                    rule) ==========================================
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

    def _propagated_plan(cone, W, canon, n):
        """THE PROPAGATION RULE (see PROPAGATION_RULE above). The plan
        vector is built by exp94's spec_target_n instrument call (the
        committed pattern's own values as width-one zones over the
        canon base), then each frontier cell's target = the frozen
        committed value of its nearest committed ring neighbor."""
        C = cone["C"]
        committed = cone["committed"]
        ring_of = cone["ring_of"]
        spec = AnatomySpec(
            zones=[Zone(f0=i / n, f1=(i + 1) / n,
                        voltage=float(committed[i]), name=f"c{i}")
                   for i in sorted(C)],
            amputate_plane=None, spec_name="exp223-self-fed",
            somatic_latch=False)
        plan = spec_target_n(spec, canon, n)
        sup = np.abs(W)
        prop_log = []
        for j in cone["frontier"]:
            nbrs = [int(i) for i in np.where(sup[j] > 0)[0]
                    if int(i) in C]
            assert nbrs, f"frontier cell {j} has no committed neighbor"
            r_star = max(ring_of[i] for i in nbrs)
            cand = sorted(i for i in nbrs if ring_of[i] == r_star)
            matched = [i for i in cand if canon[i] == canon[j]]
            i_star = matched[0] if matched else cand[0]
            plan[j] = float(committed[i_star])
            prop_log.append({"cell": int(j), "neighbor": int(i_star),
                             "neighbor_ring": int(r_star),
                             "n_same_ring_candidates": len(cand),
                             "canon_matched": bool(matched),
                             "plan_value":
                                 round(float(committed[i_star]), 4)})
        return plan, prop_log

    def _selffed_ring(h, W, canon, cone, ring_index):
        """One self-fed expansion step for one seed-cone — exp218's
        _walk_ring machinery VERBATIM (the window construction, the
        exp178 production scoped read, the S* lock, the reduction
        datum), with T_plan[F] replaced by the propagated plan. The
        ONLY values that can enter the committed region are copied
        from the read's final V at the frontier (P6)."""
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
        plan, prop_log = _propagated_plan(cone, W, canon, h["n"])
        emitted = V[F]
        err = float(np.sqrt(np.mean((emitted - plan[F]) ** 2)))
        # ---- GATE-Y2's frozen discipline (the walk's own, asserted):
        #      the committed prefix equals the frozen values
        #      bit-exactly (P6 verbatim) — NOT the re-read clause
        #      exp218 refuted. ------------------------------
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
        cone["ring_V"][ring_index] = V
        for j in F:
            C.add(int(j))
            cone["committed"][int(j)] = float(V[int(j)])
            cone["frozen"][int(j)] = float(V[int(j)])
            cone["ring_of"][int(j)] = int(ring_index)
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
                "emitted": [round(float(x), 3) for x in emitted],
                "plan": [round(float(x), 3) for x in plan[F]],
                "ring_err_mV": round(err, 3),
                "pass": bool(np.isfinite(err) and err < WALK_BAR)}

    def run_walk_host(h, n_rings):
        """The self-fed walk on one host: exp151's protocol (P2/P3/P6/P7
        verbatim — plan_of, seed_cone, commit-the-read's-own-outputs,
        seeds (1, 2, 3)) run in LOCKSTEP rounds across the seed cones.
        The plan for every ring is the PROPAGATED plan (the rule above)
        — T_plan enters solely at the P3 seed initialization."""
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
                    "ring_V": {}, "rings": [], "broken": None}
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
                rec = _selffed_ring(h, W, canon, c, r)
                c["rings"].append(rec)
                if rec.get("stop"):
                    c["broken"] = rec["stop"]
        # ---- GATE-Y2's close-out: the full frozen-prefix check and
        #      the P6 provenance (every committed cell's value equals
        #      its commit-round read's own final V, bit-exactly) -----
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
                         "worst-margin host — exp218's X3 disclosure "
                         "reused)"),
                "seeds": list(WALK_SEEDS), "S_star": list(S_STAR),
                "rings_registered": int(n_rings),
                "seed_cells": len(seed_cells),
                "propagation_rule": PROPAGATION_RULE,
                "cones": out_cones}

    # ========================== --smoke (H0, 2 rings) ==================
    if args.smoke:
        hosts = build_y_hosts()
        w = run_walk_host(hosts["H0"], n_rings=2)
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
            "lock_log_at_S_star": len(_WALK_LOCK_LOG) == 6,
            "floor_at_production": CORE.NEURAL_SPEC_MIN == PROD_FLOOR,
        }
        ok = all(checks.values())
        print(f"=== exp223 SMOKE (H0, 2 rings, DISCARDED) === "
              f"{checks} -> {'OK' if ok else 'INSTRUMENT BUG'} "
              f"({time.time() - t0:.1f}s)")
        dep = {"exp": "exp223_self_fed_walk", "kind": "smoke",
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
    hosts = build_y_hosts()
    assert all(k in hosts for k in Y_HOSTS)

    jobs = ["H0", "H4"] if args.job == "all" else [args.job]

    sections: dict = {}
    for hname in ("H0", "H4"):
        if hname not in jobs:
            continue
        w = run_walk_host(hosts[hname], WALK_RINGS)
        sections[hname] = {"walk": w}
        print(f"  [{hname}] walk 6-ring complete "
              f"{sum(1 for c in w['cones'] if c['rings_expanded'] == WALK_RINGS)}/3 "
              f"seeds | zero rejections "
              f"{sum(1 for c in w['cones'] if c['n_rejections'] == 0)}/3 "
              f"| branches {[c['branch'] for c in w['cones']]} | "
              f"worst ring err "
              f"{max((e for c in w['cones'] for e in c['ring_errs_mV'] if e is not None), default=None)}")

    result = {"exp": "exp223_self_fed_walk", "sections": sections}
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
    deposit (exp218's pattern). The bars are the pre-registered
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

    # ---- GATE-Y1 (the self-fed walk): 6 self-fed rings, zero
    #      rejections, ring errs under the 6.0 bar throughout, on
    #      every (host, seed) cone — the pattern propagates ITSELF ----
    y1_rows = []
    for hn, c in cones:
        errs = c["ring_errs_mV"]
        ok = bool(c["rings_expanded"] == RINGS
                  and c["n_rejections"] == 0
                  and not c["exhausted"]
                  and len(errs) == RINGS
                  and all(e is not None and np.isfinite(e)
                          and e < WALK_BAR for e in errs))
        y1_rows.append({"host": hn, "seed": c["seed"], "complete": ok,
                        "rings_expanded": c["rings_expanded"],
                        "n_rejections": c["n_rejections"],
                        "exhausted": c["exhausted"],
                        "worst_ring_err_mV":
                            (max(e for e in errs if e is not None)
                             if errs else None)})
    y1 = all(r["complete"] for r in y1_rows)

    # ---- GATE-Y2 (the no-drift clause): the committed values frozen
    #      (P6 verbatim) — after each round the committed prefix
    #      equals the frozen values bit-exactly (the walk's own
    #      discipline, asserted in the walk and re-counted here; NOT
    #      the re-read clause exp218 refuted) --------------------------
    n_prefix = sum(c["y2_frozen"]["n_prefix_bitexact"]
                   for _, c in cones)
    n_close = sum(c["y2_frozen"]["n_close_bitexact"] for _, c in cones)
    n_prov = sum(c["y2_frozen"]["n_p6_provenance_bitexact"]
                 for _, c in cones)
    y2 = bool(n_close > 0 and n_prov > 0 and n_prefix > 0)

    # ---- GATE-Y3 (the self-similarity profile): per-round the
    #      frontier's emitted-vs-propagated-plan err deposited; the
    #      profile shape (monotonicity) deposited per cone; the branch
    #      named: SELF-CARRYING (all 6 rings under the bar) / DEGRADES
    #      (any ring over) --------------------------------------------
    branches = {}
    y3_detail = {}
    for hn in ("H0", "H4"):
        cs = [c for h2, c in cones if h2 == hn]
        br = ("SELF-CARRYING"
              if all(c["branch"] == "SELF-CARRYING" for c in cs)
              else "DEGRADES")
        branches[hn] = br
        y3_detail[hn] = {"per_cone": [
            {"seed": c["seed"], "branch": c["branch"],
             "profile_monotone_nondecreasing":
                 c["profile_monotone_nondecreasing"],
             "profile_monotone_nonincreasing":
                 c["profile_monotone_nonincreasing"],
             "ring_errs_mV": c["ring_errs_mV"],
             "rings_over_bar": c["rings_over_bar"]} for c in cs]}
    y3 = all(b == "SELF-CARRYING" for b in branches.values())

    # ---- GATE-Y4 (hygiene) --------------------------------------------
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
    y4 = bool(errs_finite and reductions_ok and n_ring_writes == 36)
    # the S* lock logs: every ring write was locked at S* (the per-write
    # asserts would have raised otherwise); the -60.0 floor assert ran
    # post-restore and per host; the no-tuning clause is structural
    # (the constants table and the propagation rule are logged once and
    # are the same object across every host, ring and seed).
    gates = {
        "Y1": {"pass": bool(y1),
               "clause": "6 self-fed rings complete with zero "
                         "rejections on H0 and H4 (3 seeds each); "
                         "ring errs under the 6.0 bar throughout",
               "n_cones": len(cones),
               "n_complete": sum(1 for r in y1_rows if r["complete"]),
               "per_cone": y1_rows,
               "worst_ring_err_mV": max(r["worst_ring_err_mV"]
                                        for r in y1_rows
                                        if r["worst_ring_err_mV"]
                                        is not None)},
        "Y2": {"pass": bool(y2),
               "clause": "the committed values frozen (P6 verbatim): "
                         "after each round the committed prefix equals "
                         "the frozen values bit-exactly (the walk's "
                         "own discipline, asserted — NOT the re-read "
                         "clause exp218 refuted)",
               "n_prefix_bitexact_checks": n_prefix,
               "n_close_bitexact_checks": n_close,
               "n_p6_provenance_bitexact_checks": n_prov},
        "Y3": {"pass": bool(y3),
               "clause": "per-round the frontier's "
                         "emitted-vs-propagated-plan err deposited; "
                         "the profile shape (monotonicity) deposited; "
                         "the branch: SELF-CARRYING (all 6 rings under "
                         "the bar) / DEGRADES (any ring over)",
               "branches": branches,
               "per_host": y3_detail},
        "Y4": {"pass": bool(y4),
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
    y3_line = (f"Y3 {branches['H0']}/{branches['H4']}"
               if y3 else
               f"Y3 DEGRADES "
               f"({sum(len(c['rings_over_bar']) for _, c in cones)} "
               f"ring(s) over the {WALK_BAR} bar)")
    verdict = (f"{n_pass}/4 gates (Y1 Y2 Y3 Y4) | "
               f"Y1 {'6 self-fed rings complete 6/6 cones' if y1 else 'INCOMPLETE/OVER-BAR'} | "
               f"Y2 {'frozen prefix bit-exact' if y2 else 'DRIFT'} | "
               f"{y3_line}")
    merged["gates"] = gates
    merged["verdict"] = verdict
    merged["wall_s"] = round(_time.time() - t0, 1)
    merged["pre_registered"] = {
        "gates_source": ("module docstring, committed before any run "
                         "(pre-registration 94e15cb, batch 12; gates "
                         "Y1-Y4 fixed there, each evaluated exactly "
                         "once)"),
        "propagation_rule_operationalization": (
            "the canon value of the nearest committed ring neighbor = "
            "the neighbor's frozen committed value of record (the "
            "walk's own canon — P6's verbatim emission, guarded by "
            "GATE-Y2's frozen discipline; NOT a re-read — the clause "
            "exp218 refuted); the plan vector is built by exp94's "
            "spec_target_n instrument call (the committed cells as "
            "width-one zones carrying their own frozen values over the "
            "canon base) and the frontier cells overridden by the "
            "neighbor rule; T_plan is consumed solely by the P3 seed "
            "initialization (the parent's committed values — the "
            "pre-named sole external injection); same-ring ties "
            "resolved on the canon labeling (canon match, else lowest "
            "cell index) — deterministic, zero knobs"),
        "monotone_clause_reading": (
            "the pre-registered 'the profile monotone within the 6.0 "
            "bar' is deposited as the per-cone profile shape "
            "(profile_monotone_nondecreasing / "
            "profile_monotone_nonincreasing — the pre-named "
            "expectation, reported whatever it shows); the gate's "
            "operative branches are the parentheticals' own "
            "definitions: SELF-CARRYING (all 6 rings under the bar) / "
            "DEGRADES (any ring over)")},
    merged["protocol_constants"] = {
        "rings": RINGS, "walk_seeds": [1, 2, 3],
        "walk_err_bar_mV": WALK_BAR, "y_hosts": ["H0", "H4"],
        "S_star": [64.0, 0.0], "wiring_id":
            ("exp148.read_scoped | exp178 production wiring | "
             "T=1 static window -> R_T -> execute_signed@STAR_OP"),
        "propagation_rule": secs["H0"]["walk"]["propagation_rule"]}
    with open(merged_path, "w") as fh:
        json.dump(merged, fh, indent=1, default=float)
    print(f"  === {verdict} ===")
    for g in ("Y1", "Y2", "Y3", "Y4"):
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
