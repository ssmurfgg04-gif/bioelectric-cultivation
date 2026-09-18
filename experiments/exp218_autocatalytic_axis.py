#!/usr/bin/env python3
"""exp218 — THE AUTOCATALYTIC AXIS (L190's registered next).

Stage 4's remaining 101% target: the cone expands ITSELF. exp151's
self-expansion walk (seed_cone -> frontier_of -> expansion_step, 6
rings, the committed set feeding the next round) is re-armed at S* on
the 12 union hosts (exp214's build): the expansion must be
SELF-FUELED on every organism — each ring's emission becomes the next
round's substrate with no external re-seeding — and the expansion must
ADD carrying capacity, never re-price it: the already-committed
cells' values are bit-stable across subsequent rounds, and the union
carriage margin profile is non-decreasing within the 0.05 bar across
rounds.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp151's walk machinery
VERBATIM (seed_cone, frontier_of, expansion_step, RINGS = 6, the
window discipline; the production scoped read via exp178's wiring);
the host set = exp214's build_hosts verbatim (H0/H1/H2-H11
checksummed from exp202's deposit); S* = (64.0, 0.0) asserted on
every write (the lock log); the CF-1 production floor -60.0 asserted.
THE CAPACITY CLAUSE (pre-named, zero knobs): after each ring k >= 2,
the committed prefix's per-cell values from round k-1 are re-read —
the clause holds iff every previously committed cell's value is
bit-unchanged or within the 0.05 mV drift bar (exp202's no-regression
bar); the margin profile clause is priced on H0 and H4 ONLY (the
reference and the worst-margin host — pre-named, disclosed): the
union manifest (exp214's 110) re-priced writable_3seed at S* after
rings 2, 4, 6 — the profile NON-DECREASING within 0.05.

GATES (each evaluated exactly once):
  GATE-X1 (the walk) the self-expansion walk completes 6 rings with
           zero rejections on EVERY one of the 12 hosts at S* (the
           cone expands itself on every organism; ring errs under
           exp151's 6.0 bar).
  GATE-X2 (the capacity clause) every previously committed cell's
           value bit-stable (or <= 0.05 mV drift) across subsequent
           rounds, all hosts, all rings — the expansion ADDS
           capacity, never disturbs it.
  GATE-X3 (the margin profile) the union carriage on H0 and H4
           re-priced after rings 2, 4, 6: per-round worst-case
           margin non-decreasing within the 0.05 bar (ADD-CAPACITY)
           vs re-priced (REFUTE).
  GATE-X4 (hygiene) all errs finite; the (host, ring, wiring-id)
           lock log at S*; the -60.0 floor asserted; no per-target
           tuning.
NO post-hoc tuning. --smoke permitted (H0, 2 rings), discarded.
DEPOSIT: results/exp218_autocatalytic_axis.json
RUN: python3 -m experiments.exp218_autocatalytic_axis [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp218_autocatalytic_axis.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline) ============================================
    # SHARDING (exp214's pattern): --job H0 (the walk + the X3 pricing
    # profile on the reference host) / H4 (walk + pricing on the
    # worst-margin host, pre-named) / walks (the other 10 hosts' walks)
    # / gates (closed on the MERGED deposit). Each job deposits its own
    # section; merged at salvage. "all" runs everything in-process.
    import hashlib
    import time

    import numpy as np  # noqa: E402

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all", "H0", "H4", "walks",
                                      "gates"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    if args.out is not None:
        out_path = args.out
    elif args.job == "all":
        out_path = OUT
    else:
        out_path = os.path.join(ROOT, "results",
                                f"exp218_shard_{args.job}.json")

    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    from cultivation.compiler.anatomy import (  # noqa: E402
        AnatomySpec, Zone, compile_anatomy)
    from cultivation.substrate.graph import (  # noqa: E402
        GraphCollective, path as graph_path)
    from experiments.exp136_generator_v6 import (  # noqa: E402
        AUDIT_SEEDS, ERR_BAR)
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
    from experiments.exp172_deep_band_sweep import (  # noqa: E402
        target_for as deep_target_for)
    from experiments.exp182_substrate_100 import S_STAR  # noqa: E402
    from experiments.exp73_active_renormalization import (  # noqa: E402
        small_world)
    from experiments.exp84_interaction_term import (  # noqa: E402
        ThetaOnlyCollective)
    from experiments.exp90_two_source_read import star_dt  # noqa: E402
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    BAR = ERR_BAR                          # 6.0 mV — the unchanged bar
    WALK_BAR = WALK_ERR_BAR                # exp151's ring-err bar (6.0)
    WALK_SEEDS = list(SEEDS)               # exp142's (1, 2, 3) — P7
    DEP202 = os.path.join(ROOT, "results",
                          "exp202_cross_organism_carriage.json")
    DEP172 = os.path.join(ROOT, "results",
                          "exp172_deep_band_sweep.json")
    DEP182 = os.path.join(ROOT, "results",
                          "exp182_substrate_100.json")
    DEP214 = os.path.join(ROOT, "results",
                          "exp214_union_carriage.json")
    for _p in (DEP202, DEP172, DEP182, DEP214):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"
    PROD_FLOOR = -60.0                     # CF-1's production value
    N400 = 400
    REWIRE_P = 0.10
    DEEP_RUNGS = (-40.0, -45.0, -50.0, -55.0, -60.0)
    DEEP_INSTANCES = (0, 1)
    DRIFT_BAR = 0.05        # the capacity clause's bar (exp202's
    #                         no-regression bar — pre-named, zero knobs)
    PRICING_ROUNDS = (2, 4, 6)             # re-priced after these rings
    X3_HOSTS = ("H0", "H4")  # the reference and the worst-margin host
    #                          (pre-named, disclosed — exp214's U3 put
    #                          the union worst at H4 = +5.285)
    INTERFERENCE_BAR = 0.05                # X3's pre-named bar (mV)
    WIRING_ID = ("exp148.read_scoped | exp178 production wiring | "
                 "T=1 static window -> R_T -> execute_signed@STAR_OP")

    with open(DEP202) as fh:
        dep202 = json.load(fh)
    with open(DEP172) as fh:
        dep172 = json.load(fh)
    with open(DEP182) as fh:
        dep182 = json.load(fh)

    # ---- the floors: CF-1's production value asserted ----------------
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR \
        and g6.NEURAL_SPEC_MIN == PROD_FLOOR, \
        f"floor drift: {CORE.NEURAL_SPEC_MIN}, {g6.NEURAL_SPEC_MIN}"
    # ---- the S* identity of the walk's executor -----------------------
    # exp151's walk reads through execute_signed at op=STAR_OP; STAR_OP
    # IS S* = (64.0, 0.0) — asserted once here and per ring write below.
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        f"the walk's executor op {STAR_OP} != S* {S_STAR}"

    # ---- the host-parameterized instrument replica (exp202's,
    #      VERBATIM semantics — exp214's copy re-used byte-for-byte) --
    _LOCK_LOG: list = []

    def _lock_substrate_host(host, rung, A):
        assert rung == S_STAR, \
            f"substrate drift on {host}: write used {rung}, fixed {S_STAR}"
        _LOCK_LOG.append((host, tuple(rung), id(A)))

    def _erosion_host(f, A, n, gamma, mu, config, seed):
        if config == "theta_only":
            c = ThetaOnlyCollective(adjacency=A, seed=seed,
                                    gamma=gamma, mu_theta=mu)
        else:
            c = GraphCollective(adjacency=A, seed=seed, gamma=gamma,
                                mu_theta=mu if config == "full" else 0.0)
        c.set_target(f)
        c.theta = f.copy()
        c.V = f + c.rng.normal(0.0, 2.0, n)
        dt = star_dt(gamma, float(A.sum(axis=1).max()))
        c.run(24.0, dt=dt)
        return c.pattern_error(f)

    def _decode_host(f, zones, A, canon, n, gamma, mu, seed):
        assert np.array_equal(canon, labeling_bfs_n(A)), \
            "canon mismatch: the builder's canon != the engine canon"
        spec = AnatomySpec(
            zones=[Zone(f0=a, f1=b, voltage=v, name=f"z{k}")
                   for k, (a, b, v) in enumerate(zones)],
            amputate_plane=None, spec_name="invention",
            somatic_latch=False)
        dt = star_dt(gamma, float(A.sum(axis=1).max()))
        c = GraphCollective(adjacency=A, seed=seed, gamma=gamma,
                            mu_theta=mu)
        c.set_target(canon)
        c.write_spec_layer(f)
        prog = compile_anatomy(spec, n=n)
        if prog.rejected:
            return {"decode_err": float("nan"),
                    "hold_err": float("nan"), "rejected": prog.rejected}
        for cl in prog.clamps:
            c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
        c.run(24.0, dt=dt)
        c.release_clamps()
        reg_idx = sorted(set(i for (a, b, _) in zones
                             for i in range(int(round(a * n)),
                                            int(round(b * n)))))
        if reg_idx:
            reg_walk = list(range(reg_idx[0], reg_idx[-1] + 1))
            region_set = set(reg_walk)
            c.amputate(slice(reg_idx[0], reg_idx[-1] + 1))
            wound_center = float(np.mean(c.theta[reg_walk]))
            parent_of: dict = {}
            frontier = []
            for i in reg_walk:
                nbrs = [j for j in np.where(c.A[i] > 0)[0]
                        if j not in region_set]
                if nbrs:
                    parent_of[i] = int(max(
                        nbrs, key=lambda j: -abs(c.theta[j]
                                                 - wound_center)))
                    frontier.append(i)
            if not frontier:
                frontier = reg_walk[:1]
                parent_of[frontier[0]] = frontier[0]
            visited = set(frontier)
            order = [(i, parent_of[i]) for i in frontier]
            queue = list(frontier)
            while queue:
                i = queue.pop(0)
                for j in np.where(c.A[i] > 0)[0]:
                    if int(j) in region_set and int(j) not in visited:
                        visited.add(int(j))
                        parent_of[int(j)] = int(i)
                        order.append((int(j), int(i)))
                        queue.append(int(j))
            canon_src = getattr(c, "phi_spec_canon", None)
            from cultivation.bioelectric.collective import (
                NEURAL_SPEC_MIN)
            for i, src in order:
                for _ in range(8):
                    c.step(dt)
                if c.phi_spec[i] >= NEURAL_SPEC_MIN:
                    theta_new = c.phi_spec[i] + c.rng.normal(0.0, 0.6)
                elif canon_src is not None:
                    theta_new = canon_src[i] + c.rng.normal(0.0, 0.6)
                else:
                    theta_new = c.theta[src] + c.rng.normal(0.0, 0.6)
                c.theta[i] = theta_new
                c.V[i] = theta_new
        c.run(15.0, dt=dt)
        e_decode = float(c.pattern_error(f))
        c.run(100.0, dt=dt)
        e_hold = float(c.pattern_error(f))
        return {"decode_err": e_decode, "hold_err": e_hold,
                "rejected": []}

    def _price_rung_host(f, zones, rung, A, canon, n, host):
        _lock_substrate_host(host, rung, A)
        g, mu = rung
        eV = float(np.mean([_erosion_host(f, A, n, g, 0.0, "V_only", s)
                            for s in AUDIT_SEEDS]))
        eT = float(np.mean([_erosion_host(f, A, n, g, mu,
                                          "theta_only", s)
                            for s in AUDIT_SEEDS]))
        quad = float(np.hypot(eV, eT))
        dec = [_decode_host(f, zones, A, canon, n, g, mu, s)
               for s in AUDIT_SEEDS]
        derr = [float(d["decode_err"]) for d in dec]
        herr = [float(d["hold_err"]) for d in dec]
        n_rej = int(sum(len(d.get("rejected", [])) for d in dec))
        n_ok = sum(int(a < BAR and b < BAR) for a, b in zip(derr, herr))
        return {"cell": [g, mu], "host": host,
                "eV": round(eV, 3), "eT": round(eT, 3),
                "quad": round(quad, 3), "pass": bool(quad < BAR),
                "silent": bool(mu == 0.0),
                "decode_errs": [round(e, 3) for e in derr],
                "hold_errs": [round(e, 3) for e in herr],
                "decode_err_mean": round(float(np.mean(derr)), 3),
                "hold_err_mean": round(float(np.mean(herr)), 3),
                "decode_stable_seeds": f"{n_ok}/3", "n_ok": int(n_ok),
                "dec333": bool(n_ok == len(AUDIT_SEEDS)),
                "full_valid": bool(quad < BAR
                                   and n_ok == len(AUDIT_SEEDS)),
                "n_rejected": n_rej}

    def _writable_3seed_host(f, zones, rung, A, canon, n, host):
        row = _price_rung_host(f, zones, rung, A, canon, n, host)
        rejected = bool(row["n_rejected"] > 0)
        if rejected:
            return {"row": row, "writable": False, "rejected": True,
                    "margin3": -float("inf")}
        m3 = BAR - max(row["quad"], max(row["decode_errs"]),
                       max(row["hold_errs"]))
        return {"row": row, "writable": bool(row["full_valid"]),
                "rejected": False, "margin3": float(m3)}

    def _f_sha(f):
        return hashlib.sha256(
            np.ascontiguousarray(f, dtype=np.float64).tobytes()
        ).hexdigest()

    # ---- TARGET CLASS 1: exp182's manifest (100, REUSED checksummed,
    #      exp214's manifest_targets VERBATIM) --------------------------
    manifest = dep182["manifest"]["targets"]
    assert len(manifest) == 100 and dep182["manifest"]["n_targets"] == 100
    assert [float(x) for x in dep182["battery"]["S_star"]] == \
        [S_STAR[0], S_STAR[1]], "exp182's deposited S* != this module's S*"
    manifest_block = {
        "source": "results/exp182_substrate_100.json",
        "sha256": hashlib.sha256(
            open(DEP182, "rb").read()).hexdigest(),
        "reused_not_regenerated": True,
        "target_seed": dep182["manifest"]["target_seed"],
        "n_targets": 100,
        "checksum_clause": ("f rebuilt per host from the deposited "
                            "triples via exp94's spec_target_n on the "
                            "HOST's canon; on H0 the rebuild's f_sha256 "
                            "must equal the deposited f_sha256 "
                            "(checksummed reuse; any mismatch raises)"),
    }
    _targets_cache: dict = {}

    def manifest_targets(host_name: str, canon: np.ndarray, n: int,
                         checksum: bool) -> list[dict]:
        if host_name in _targets_cache:
            return _targets_cache[host_name]
        made = []
        for m in manifest:
            triples = [tuple(float(x) for x in z) for z in m["triples"]]
            spec = AnatomySpec(
                zones=[Zone(f0=s, f1=e, voltage=v, name=f"z{j}")
                       for j, (s, e, v) in enumerate(triples)],
                amputate_plane=MULTI.amputate_plane,
                spec_name=f"exp182-t{m['index']:03d}",
                somatic_latch=MULTI.somatic_latch)
            f = spec_target_n(spec, canon, n)
            sha = _f_sha(f)
            if checksum:
                assert sha == m["f_sha256"], \
                    (f"checksum mismatch on {host_name} target "
                     f"{m['index']}: rebuilt {sha} != deposited "
                     f"{m['f_sha256']}")
            made.append({"index": m["index"],
                         "zone_count": m["zone_count"],
                         "triples": triples, "vmin": m["vmin"],
                         "vmax": m["vmax"], "f_sha256": sha, "f": f})
        _targets_cache[host_name] = made
        return made

    # ---- TARGET CLASS 2: the 10 deep targets (exp172's construction,
    #      exp214's build VERBATIM) -------------------------------------
    def deep_targets(canon, n):
        made = []
        for rung in DEEP_RUNGS:
            for inst in DEEP_INSTANCES:
                if n == g6.N and canon is not None \
                        and np.array_equal(canon,
                                           labeling_bfs_n(g6.A_CHAIN)):
                    f, triples, _ref = deep_target_for(rung, inst)
                else:
                    zs = [(z.f0 + inst / 100.0, z.f1 + inst / 100.0,
                           rung) for z in MULTI.zones]
                    spec = AnatomySpec(
                        zones=[Zone(f0=a, f1=b, voltage=v, name=nm)
                               for (a, b, v, nm) in
                               ((a, b, v, z.name) for (a, b, v), z
                                in zip(zs, MULTI.zones))],
                        amputate_plane=MULTI.amputate_plane,
                        spec_name=f"ms-multi-deep-i{inst}",
                        somatic_latch=MULTI.somatic_latch)
                    f = spec_target_n(spec, canon, n)
                    triples = [(a, b, rung) for (a, b, _nm) in zs]
                made.append({"rung": rung, "instance": inst,
                             "triples": [list(t) for t in triples],
                             "f_sha256": _f_sha(f), "f": f})
        return made

    # ---- the hosts (exp202's build records reused checksummed;
    #      exp214's build_hosts VERBATIM) --------------------------------
    def build_hosts() -> dict:
        hosts = {}
        canon0 = labeling_bfs_n(g6.A_CHAIN)
        assert np.array_equal(canon0, g6.wildtype_target(g6.N))
        hosts["H0"] = {"name": "H0", "n": int(g6.N), "A": g6.A_CHAIN,
                       "canon": canon0}
        A400 = graph_path(N400)
        canon400 = labeling_bfs_n(A400)
        assert np.array_equal(canon400, g6.wildtype_target(N400))
        hosts["H1"] = {"name": "H1", "n": N400, "A": A400,
                       "canon": canon400}
        redraw = {r["host"]: r["seed"] for r in
                  dep202["sections"]["corpus"]["scan"]["redraw_log"]}
        dep_hosts = dep202["sections"]["corpus"]["hosts"]
        for k in sorted(dep_hosts):
            if not k.startswith("H") or int(k[1:]) < 2:
                continue
            seed = int(redraw[k])
            A = small_world(100, REWIRE_P, seed)
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

    # ================= THE WALK (exp151's machinery re-armed) ==========
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
        # (asserted at module scope above and re-asserted per write).
        assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
            f"walk write off S* on {host} ring {ring}"
        _WALK_LOCK_LOG.append((host, int(ring), WIRING_ID))

    def _walk_ring(h, W, T_plan, cone, ring_index, in_zone):
        """One expansion step for one seed-cone — exp151's
        seed_cone -> frontier_of -> window_matrix VERBATIM, with the
        read wired through exp178's production scoped arm and the
        pre-named capacity clause instrumented on the read's own
        final V. The ONLY values that can enter the committed region
        are copied from the read's final V at the frontier (P6)."""
        name, s = h["name"], cone["seed"]
        C = cone["C"]
        F = frontier_of(C, W)                    # exp151's P4 verbatim
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
        # on a static window (f_max 0 < 32 -> R_T -> T=1 passthrough ->
        # exp148 TC1-TC3 with F=0 -> exp151's execute_signed call).
        with warnings_as_errors():
            raw = execute_signed(MULTI, M, s, op=STAR_OP,
                                 return_state=True)
        reduction = bool(np.array_equal(
            np.asarray(raw["final_state"]["V"], dtype=float), V))
        emitted = V[F]
        err = float(np.sqrt(np.mean((emitted - T_plan[F]) ** 2)))
        # ---- THE CAPACITY CLAUSE (pre-named, zero knobs): the
        #      committed prefix's per-cell values from round k-1 (the
        #      emission prefix, rounds 1..k-1 — exp151's P3 keeps the
        #      seed patch out of gate scope) are re-read by THIS ring's
        #      read; the clause holds here iff every previously
        #      committed cell's value is bit-unchanged or within the
        #      0.05 mV drift bar.
        capacity = None
        if ring_index >= 2 and cone["committed"]:
            prefix = sorted(cone["committed"])
            d = np.array([abs(V[i] - cone["committed"][i])
                          for i in prefix])
            top = np.argsort(-d)[:8]
            worst = [{"cell": int(prefix[t]),
                      "committed": round(float(cone["committed"]
                                                [prefix[t]]), 4),
                      "reread": round(float(V[prefix[t]]), 4),
                      "drift": round(float(d[t]), 4),
                      "in_zone": bool(in_zone(prefix[t]))}
                     for t in top]
            sd = np.array([abs(V[i] - float(T_plan[i]))
                           for i in cone["seed_cells"]])
            capacity = {
                "n_checked": len(prefix),
                "n_bit_exact": int(np.sum(d == 0.0)),
                "n_within_bar": int(np.sum(d <= DRIFT_BAR)),
                "max_abs_drift": round(float(d.max()), 4),
                "clause_hold_here": bool(d.max() <= DRIFT_BAR),
                "worst_cells": worst,
                "seed_patch_datum_not_gated": {
                    "n": int(len(sd)),
                    "max_abs_drift": round(float(sd.max()), 4)}}
        # ---- the ring write: the S* lock asserted, then P6's commit
        #      (the read's own outputs, full precision, verbatim) ----
        _lock_walk_write(name, ring_index, s)
        for j in F:
            C.add(int(j))
            cone["committed"][int(j)] = float(V[int(j)])
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
                "capacity_clause": capacity,
                "pass": bool(np.isfinite(err) and err < WALK_BAR)}

    def run_walk_host(h, n_rings, pricing_hook=None):
        """The walk re-armed on one host: exp151's protocol (P2/P3/P6/P7
        verbatim — plan_of, seed_cone, commit-the-read's-own-outputs,
        seeds (1, 2, 3)) run in LOCKSTEP rounds across the seed cones so
        'after ring k' is a host-level event; the pricing hook (X3, on
        the pre-named hosts only) fires after rings 2, 4, 6."""
        name = h["name"]
        W = np.asarray(h["A"], dtype=float)
        T_plan = plan_of(W)                      # exp151's P2 verbatim
        seed_cells = seed_cone(W)                # exp151's P3 verbatim
        support_n = int(np.count_nonzero(np.abs(W).sum(axis=1)))
        zone_ranges = [(int(round(z.f0 * W.shape[0])),
                        int(round(z.f1 * W.shape[0])))
                       for z in MULTI.zones]

        def in_zone(i):
            return any(a <= i < b for a, b in zone_ranges)

        cones = [{"seed": s, "C": set(seed_cells), "committed": {},
                  "seed_cells": list(seed_cells), "rings": [],
                  "broken": None} for s in WALK_SEEDS]
        pricing_log = []
        for r in range(1, n_rings + 1):
            active = [c for c in cones if c["broken"] is None]
            if not active:
                break
            for c in active:
                rec = _walk_ring(h, W, T_plan, c, r, in_zone)
                c["rings"].append(rec)
                if rec.get("stop"):
                    c["broken"] = rec["stop"]
            if pricing_hook is not None and r in PRICING_ROUNDS:
                pricing_log.append({"after_ring": r,
                                    "pricing": pricing_hook(h)})
        out_cones = []
        for c in cones:
            expanded = [x for x in c["rings"]
                        if x.get("ring_expanded") and x.get("read_ok")]
            rings_expanded = len(expanded)
            n_rej = sum(1 for x in c["rings"] if not x.get("read_ok"))
            exhausted = bool(c["rings"][-1].get("exhausted")) \
                if c["rings"] else False
            caps = [x["capacity_clause"] for x in expanded
                    if x.get("capacity_clause")]
            worst_drift = (max(x["max_abs_drift"] for x in caps)
                           if caps else None)
            hold_all = bool(caps) and all(x["clause_hold_here"]
                                          for x in caps)
            reductions = [x["reduction_bitexact_vs_exp151_raw"]
                          for x in expanded]
            out_cones.append({
                "seed": c["seed"],
                "rings_expanded": rings_expanded,
                "exhausted": exhausted,
                "n_rejections": n_rej,
                "broken": c["broken"],
                "final_coverage": [len(c["C"]), support_n],
                "ring_errs_mV": [x.get("ring_err_mV") for x in expanded],
                "rings_passed": sum(1 for x in expanded if x.get("pass")),
                "capacity": {
                    "rings_checked": [x["ring_index"] for x in expanded
                                      if x.get("capacity_clause")],
                    "clause_hold_all_rings": hold_all,
                    "worst_abs_drift": worst_drift,
                    "per_ring": [{"ring_index": x["ring_index"],
                                  **{k: v for k, v in
                                     x["capacity_clause"].items()
                                     if k != "worst_cells"},
                                  "worst_cells": x["capacity_clause"]
                                  ["worst_cells"][:3]}
                                 for x in expanded
                                 if x.get("capacity_clause")]},
                "wiring_datum": {
                    "reduction_bitexact_all_rings":
                        bool(reductions) and all(reductions),
                    "wiring_ids": sorted({x["scoped_wiring"]
                                          ["wiring_id"]
                                          for x in expanded})},
                "rings": c["rings"]})
        return {"host": name, "n": int(h["n"]),
                "kind": ("reference (exp182's own host)"
                         if name == "H0" else
                         "size-law organism (exp198's scale)"
                         if name == "H1" else
                         "corpus-rewired organism"),
                "seeds": list(WALK_SEEDS), "S_star": list(S_STAR),
                "rings_registered": int(n_rings),
                "seed_cells": len(seed_cells),
                "cones": out_cones,
                "pricing_rounds": pricing_log}

    # ---- X3: the union re-pricing (exp214's carriage replica) ---------
    def price_union(h) -> dict:
        A, canon, n = h["A"], h["canon"], h["n"]
        mans = manifest_targets(h["name"], canon, n,
                                checksum=(h["name"] == "H0"))
        deeps = deep_targets(canon, n)
        assert len(mans) == 100 and len(deeps) == 10
        per_target = []
        for t in mans:
            zones = [tuple(float(x) for x in z) for z in t["triples"]]
            w = _writable_3seed_host(t["f"], zones, S_STAR, A, canon,
                                     n, h["name"])
            per_target.append({
                "tclass": "manifest", "index": t["index"],
                "f_sha256": t["f_sha256"], "row": w["row"],
                "writable": bool(w["writable"]),
                "rejected": bool(w["rejected"]),
                "margin3": (float(w["margin3"])
                            if np.isfinite(w["margin3"]) else None)})
        for t in deeps:
            zones = [tuple(float(x) for x in z) for z in t["triples"]]
            w = _writable_3seed_host(t["f"], zones, S_STAR, A, canon,
                                     n, h["name"])
            per_target.append({
                "tclass": "deep", "rung": t["rung"],
                "instance": t["instance"],
                "f_sha256": t["f_sha256"], "row": w["row"],
                "writable": bool(w["writable"]),
                "rejected": bool(w["rejected"]),
                "margin3": (float(w["margin3"])
                            if np.isfinite(w["margin3"]) else None)})
        margins = [p["margin3"] for p in per_target
                   if p["margin3"] is not None]
        return {"host": h["name"], "n": int(n), "S_star": list(S_STAR),
                "seeds": list(AUDIT_SEEDS), "n_targets": len(per_target),
                "n_writable": sum(1 for p in per_target if p["writable"]),
                "n_rejected_rows": sum(1 for p in per_target
                                       if p["rejected"]),
                "worst_case_margin3": (min(margins) if margins else None),
                "per_target": per_target}

    def _ref214_map() -> dict:
        """exp214's deposited union margins (the no-walk reference for
        the ADD-CAPACITY disclosure — a datum, not a gate)."""
        ref = {}
        for r in dep214["sections"]["H0"]["carriage"]["per_target"]:
            ref[("H0", r["tclass"],
                 int(r["index"]) if r["tclass"] == "manifest"
                 else (float(r["rung"]), int(r["instance"])))] = \
                r.get("margin3")
        for c in dep214["sections"]["corpus"]["carriages"]:
            if c["host"] == "H4":
                for r in c["per_target"]:
                    ref[("H4", r["tclass"],
                         int(r["index"]) if r["tclass"] == "manifest"
                         else (float(r["rung"]), int(r["instance"])))] = \
                        r.get("margin3")
        return ref

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
            "capacity_clause_holds_at_ring_2": all(
                c["capacity"]["clause_hold_all_rings"]
                for c in w["cones"]),
            "reduction_bitexact": all(
                c["wiring_datum"]["reduction_bitexact_all_rings"]
                for c in w["cones"]),
            "lock_log_at_S_star": len(_WALK_LOCK_LOG) == 6,
        }
        ok = all(checks.values())
        print(f"=== exp218 SMOKE (H0, 2 rings, DISCARDED) === "
              f"{checks} -> {'OK' if ok else 'INSTRUMENT BUG'} "
              f"({time.time() - t0:.1f}s)")
        dep = {"exp": "exp218_autocatalytic_axis", "kind": "smoke",
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
        return _close_gates_on(out_path, WALK_BAR=float(WALK_BAR))
    hosts = build_hosts()
    assert len(hosts) == 12 and all(k in hosts for k in
                                    ("H0", "H1", "H4"))
    dep214 = json.load(open(DEP214))
    assert dep214["gates"]["U3"]["worst_host"] == "H4", \
        "exp218's pre-named worst-margin host != exp214's deposited one"
    ref214 = _ref214_map()
    assert len(ref214) == 220, f"ref214 map incomplete: {len(ref214)}"

    jobs = (["gates"] if args.job == "gates"
            else ["H0", "H4", "walks"] if args.job == "all"
            else [args.job])

    def run_priced_host(hname: str) -> dict:
        w = run_walk_host(hosts[hname], WALK_RINGS,
                          pricing_hook=lambda h: price_union(h))
        rounds = w.pop("pricing_rounds")
        assert [r["after_ring"] for r in rounds] == list(PRICING_ROUNDS)
        for r in rounds:
            key = lambda p: ((hname, p["tclass"],
                              int(p["index"])
                              if p["tclass"] == "manifest"
                              else (float(p["rung"]), int(p["instance"]))))
            n_exact = sum(1 for p in r["pricing"]["per_target"]
                          if p["margin3"] is not None
                          and float(p["margin3"]) == float(ref214[key(p)]))
            r["n_margin3_bit_exact_vs_exp214"] = n_exact
            r["n_compared_vs_exp214"] = len(ref214) // 2
        return {"walk": w, "pricing": {"rounds": rounds}}

    sections: dict = {}
    if "H0" in jobs:
        sections["H0"] = run_priced_host("H0")
        w0 = sections["H0"]["walk"]
        print(f"  [H0] walk 6-ring complete "
              f"{sum(1 for c in w0['cones'] if c['rings_expanded'] == WALK_RINGS)}/3 "
              f"seeds | capacity hold "
              f"{sum(1 for c in w0['cones'] if c['capacity']['clause_hold_all_rings'])}/3 "
              f"| pricing rounds "
              f"{[r['pricing']['worst_case_margin3'] for r in sections['H0']['pricing']['rounds']]}")
    if "H4" in jobs:
        sections["H4"] = run_priced_host("H4")
        w4 = sections["H4"]["walk"]
        print(f"  [H4] walk 6-ring complete "
              f"{sum(1 for c in w4['cones'] if c['rings_expanded'] == WALK_RINGS)}/3 "
              f"seeds | capacity hold "
              f"{sum(1 for c in w4['cones'] if c['capacity']['clause_hold_all_rings'])}/3 "
              f"| pricing rounds "
              f"{[r['pricing']['worst_case_margin3'] for r in sections['H4']['pricing']['rounds']]}")
    if "walks" in jobs:
        cars = []
        for k in sorted(hosts):
            if k in ("H0", "H4"):
                continue
            cars.append(run_walk_host(hosts[k], WALK_RINGS))
            print(f"  [{k}] walk 6-ring complete "
                  f"{sum(1 for c in cars[-1]['cones'] if c['rings_expanded'] == WALK_RINGS)}/3 "
                  f"seeds | capacity hold "
                  f"{sum(1 for c in cars[-1]['cones'] if c['capacity']['clause_hold_all_rings'])}/3")
        sections["walks"] = {"carriages": cars}

    result = {"exp": "exp218_autocatalytic_axis", "sections": sections}
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


def _close_gates_on(merged_path: str, WALK_BAR=None) -> dict:
    """GATE CLOSURE — each gate evaluated EXACTLY ONCE on the merged
    deposit (exp214's pattern). WALK_BAR (exp151's 6.0 ring bar) and
    the other bars are the pre-registered constants; nothing here is
    tuned by the data."""
    import time as _time

    import numpy as np

    t0 = _time.time()
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DEP214 = os.path.join(ROOT, "results", "exp214_union_carriage.json")
    with open(merged_path) as fh:
        merged = json.load(fh)
    secs = merged["sections"]
    assert all(k in secs for k in ("H0", "H4", "walks")), \
        f"merged deposit incomplete: {sorted(secs)}"
    walk_secs = [secs["H0"]["walk"], secs["H4"]["walk"]] \
        + secs["walks"]["carriages"]
    assert len(walk_secs) == 12, f"host count {len(walk_secs)} != 12"
    cones = [(h["host"], c) for h in walk_secs for c in h["cones"]]
    assert len(cones) == 36, f"cone count {len(cones)} != 36"
    RINGS = 6
    WALK_BAR = 6.0 if WALK_BAR is None else float(WALK_BAR)
    DRIFT_BAR = 0.05
    INTERFERENCE_BAR = 0.05

    # ---- GATE-X1 (the walk): 6 rings, zero rejections, ring errs
    #      under exp151's 6.0 bar, on EVERY (host, seed) cone ---------
    x1_rows = []
    for hn, c in cones:
        errs = c["ring_errs_mV"]
        ok = bool(c["rings_expanded"] == RINGS
                  and c["n_rejections"] == 0
                  and not c["exhausted"]
                  and len(errs) == RINGS
                  and all(e is not None and np.isfinite(e)
                          and e < WALK_BAR for e in errs))
        x1_rows.append({"host": hn, "seed": c["seed"], "complete": ok,
                        "rings_expanded": c["rings_expanded"],
                        "n_rejections": c["n_rejections"],
                        "exhausted": c["exhausted"],
                        "worst_ring_err_mV":
                            (max(e for e in errs if e is not None)
                             if errs else None)})
    x1 = all(r["complete"] for r in x1_rows)

    # ---- GATE-X2 (the capacity clause) -------------------------------
    failures = []
    n_checked = 0
    n_hold = 0
    for hn, c in cones:
        for cap in c["capacity"]["per_ring"]:
            n_checked += 1
            if cap["clause_hold_here"]:
                n_hold += 1
            else:
                failures.append({
                    "host": hn, "seed": c["seed"],
                    "ring": cap["ring_index"],
                    "max_abs_drift": cap["max_abs_drift"],
                    "n_within_bar": cap["n_within_bar"],
                    "n_checked": cap["n_checked"],
                    "worst_cells": cap.get("worst_cells", [])[:3]})
    n_prefix_cells = sum(x["n_checked"] for _, c in cones
                         for x in c["capacity"]["per_ring"])
    n_bit = sum(x["n_bit_exact"] for _, c in cones
                for x in c["capacity"]["per_ring"])
    worst = max((x["max_abs_drift"] for _, c in cones
                 for x in c["capacity"]["per_ring"]), default=0.0)
    x2 = bool(n_checked > 0 and not failures)

    # ---- GATE-X3 (the margin profile) --------------------------------
    branches = {}
    x3_detail = {}
    for hn in ("H0", "H4"):
        rounds = secs[hn]["pricing"]["rounds"]
        prof = [{"after_ring": r["after_ring"],
                 "worst_case_margin3": r["pricing"]["worst_case_margin3"],
                 "n_writable": r["pricing"]["n_writable"]}
                for r in rounds]
        deltas = [round(prof[i + 1]["worst_case_margin3"]
                        - prof[i]["worst_case_margin3"], 6)
                  for i in range(len(prof) - 1)]
        br = ("ADD-CAPACITY"
              if all(d >= -INTERFERENCE_BAR for d in deltas)
              else "RE-PRICED")
        branches[hn] = br
        x3_detail[hn] = {"profile": prof, "consecutive_deltas": deltas,
                         "branch": br}
    x3 = all(b == "ADD-CAPACITY" for b in branches.values())

    # ---- GATE-X4 (hygiene) --------------------------------------------
    n_rej_walk = sum(c["n_rejections"] for _, c in cones)
    n_rej_price = sum(r["pricing"]["n_rejected_rows"]
                      for hn in ("H0", "H4")
                      for r in secs[hn]["pricing"]["rounds"])
    errs_finite = all(
        e is not None and np.isfinite(e) for _, c in cones
        for e in c["ring_errs_mV"]) and n_rej_walk == 0 \
        and n_rej_price == 0
    n_ring_writes = sum(x["ring_index"] in range(1, RINGS + 1)
                        and x.get("ring_expanded") and x.get("read_ok")
                        for _, c in cones for x in c["rings"])
    reductions_ok = all(c["wiring_datum"]
                        ["reduction_bitexact_all_rings"]
                        for _, c in cones)
    pricing_rows = sum(r["pricing"]["n_targets"]
                       for hn in ("H0", "H4")
                       for r in secs[hn]["pricing"]["rounds"])
    x4 = bool(errs_finite and reductions_ok and pricing_rows == 660)
    # the S* lock logs: every ring write and every pricing write was
    # locked at S* (the per-write asserts would have raised otherwise);
    # the floor assert and the no-tuning clause are structural.
    gates = {
        "X1": {"pass": bool(x1),
               "clause": "the self-expansion walk completes 6 rings "
                         "with zero rejections on EVERY one of the 12 "
                         "hosts at S*; ring errs under exp151's 6.0 bar",
               "n_cones": len(cones),
               "n_complete": sum(1 for r in x1_rows if r["complete"]),
               "per_cone": x1_rows,
               "worst_ring_err_mV": max(r["worst_ring_err_mV"]
                                        for r in x1_rows)},
        "X2": {"pass": bool(x2),
               "clause": "every previously committed cell's value "
                         "bit-stable (or <= 0.05 mV drift) across "
                         "subsequent rounds, all hosts, all rings",
               "drift_bar_mV": DRIFT_BAR,
               "n_prefix_rereads": n_checked,
               "n_prefix_cells_checked": n_prefix_cells,
               "n_bit_exact": n_bit,
               "n_hold": n_hold,
               "worst_abs_drift": worst,
               "failures": failures[:24],
               "n_failures": len(failures)},
        "X3": {"pass": bool(x3),
               "clause": "the union carriage on H0 and H4 re-priced "
                         "after rings 2, 4, 6: per-round worst-case "
                         "margin non-decreasing within the 0.05 bar",
               "interference_bar_mV": INTERFERENCE_BAR,
               "branches": branches,
               "per_host": x3_detail},
        "X4": {"pass": bool(x4),
               "clause": "all errs finite; the (host, ring, wiring-id) "
                         "lock log at S*; the -60.0 floor asserted; no "
                         "per-target tuning",
               "all_errs_finite": bool(errs_finite),
               "walk_rejections": n_rej_walk,
               "pricing_rejected_rows": n_rej_price,
               "ring_writes_logged": n_ring_writes,
               "scoped_reduction_bitexact_all_cones":
                   bool(reductions_ok),
               "pricing_rows": pricing_rows,
               "floor_asserted": True,
               "no_per_target_tuning": True}}
    n_pass = sum(1 for g in gates.values() if g["pass"])
    x2_line = ("capacity clause HOLDS"
               if x2 else f"capacity clause REFUTED "
                          f"(worst drift {worst:.3f} mV, "
                          f"{len(failures)} ring re-reads over the bar)")
    verdict = (f"{n_pass}/4 gates (X1 X2 X3 X4) | "
               f"X1 {'6-ring complete 36/36' if x1 else 'INCOMPLETE'} | "
               f"{x2_line} | X3 {branches['H0']}/{branches['H4']}")
    merged["gates"] = gates
    merged["verdict"] = verdict
    merged["wall_s"] = round(_time.time() - t0, 1)
    merged["pre_registered"] = {
        "gates_source": ("module docstring, committed before any run "
                         "(pre-registration d52addd, batch 11; gates "
                         "X1-X4 fixed there, each evaluated exactly "
                         "once)"),
        "capacity_clause_reading": ("the committed prefix = the "
                                    "emission-committed cells of rounds "
                                    "1..k-1 (exp151's P3 keeps the seed "
                                    "patch out of gate scope; the seed "
                                    "patch's re-read drift is deposited "
                                    "as an ungated datum); the re-read "
                                    "is the ring-k read's own final V "
                                    "at those cells vs the values "
                                    "committed at their commit round"),
        "walk_interleave": ("the host's 3 seed-cones run in lockstep "
                            "rounds; 'after ring k' is the host-level "
                            "event; the X3 pricing hook fires on the "
                            "pre-named hosts only")}
    merged["protocol_constants"] = {
        "rings": RINGS, "walk_seeds": [1, 2, 3],
        "walk_err_bar_mV": WALK_BAR, "drift_bar_mV": DRIFT_BAR,
        "pricing_rounds": [2, 4, 6], "x3_hosts": ["H0", "H4"],
        "S_star": [64.0, 0.0], "wiring_id":
            ("exp148.read_scoped | exp178 production wiring | "
             "T=1 static window -> R_T -> execute_signed@STAR_OP")}
    with open(merged_path, "w") as fh:
        json.dump(merged, fh, indent=1, default=float)
    print(f"  === {verdict} ===")
    for g in ("X1", "X2", "X3", "X4"):
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
