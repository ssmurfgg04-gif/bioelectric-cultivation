#!/usr/bin/env python3
"""exp214 — THE 110-TARGET UNION CARRIAGE (L186's registered next).

exp202 carried exp182's 100-target manifest across the 12 hosts
(worst margin +5.285); exp209 carried the 10 deep targets across the
same hosts (worst +5.298) — separately. L186's registered question:
does S* carry the UNION (a 110-target manifest) at the same margin
floor on the same 12 hosts — Stage 4's cross-organism axis closes at
the union or names the interference.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp202's carriage protocol
verbatim (the host-parameterized replica, K1-anchored twice —
exp182's and exp172's deposits); the host set rebuilt checksummed
from exp202's deposit (exp209's build, verified); the TARGET set
(pre-named, zero fitting): exp182's manifest (100, checksummed) +
exp209's 10 deep targets (exp172's construction) = 110.

GATES (each evaluated exactly once):
  GATE-U1 (the anchors) both replay clauses hold: exp182's manifest
           f_sha256 checksummed on H0; exp172's prices bit-exact (the
           exp209 K1 rows re-verified).
  GATE-U2 (the union bar) >= 99/110 targets writable_3seed at S* on
           EVERY host (the pre-named union bar: the full repertoire's
           90% floor and the deep band's floor composed — 90/100 and
           9/10 both lift to 99/110); per-host miss lists deposited.
  GATE-U3 (the interference question) the union's per-host worst-case
           margin vs the two separate runs' worst margins (+5.285 /
           +5.298): the branch named — NO-INTERFERENCE (union worst
           >= min(separate worsts) - 0.05) / INTERFERENCE-NAMED (the
           union degrades beyond the 0.05 bar; the (host, target)
           pairs carrying the degradation deposited).
  GATE-U4 (hygiene) all errs finite; the (host, rung, wiring-id)
           lock log at S*; no per-target tuning.
NO post-hoc tuning. --smoke permitted (H0 + 10 targets), discarded.
DEPOSIT: results/exp214_union_carriage.json
RUN: python3 -m experiments.exp214_union_carriage [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp214_union_carriage.json")


def main() -> dict:
    # ==== BODY (written by the orchestrator under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline) ============================================
    # SHARDING (exp209's pattern): --job H0 (the U1 anchors + H0's
    # carriage) / H1 / corpus (H2-H11) / gates (closed on the MERGED
    # deposit). Each job deposits its own section; merged at salvage.
    import hashlib
    import time

    import numpy as np  # noqa: E402

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all", "H0", "H1", "corpus",
                                      "gates"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    from cultivation.compiler.anatomy import (  # noqa: E402
        AnatomySpec, Zone, compile_anatomy)
    from cultivation.substrate.graph import (  # noqa: E402
        GraphCollective, path as graph_path)
    from experiments.exp136_generator_v6 import (  # noqa: E402
        AUDIT_SEEDS, ERR_BAR)
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
    DEP202 = os.path.join(ROOT, "results",
                          "exp202_cross_organism_carriage.json")
    DEP172 = os.path.join(ROOT, "results",
                          "exp172_deep_band_sweep.json")
    DEP182 = os.path.join(ROOT, "results",
                          "exp182_substrate_100.json")
    DEP209 = os.path.join(ROOT, "results",
                          "exp209_deep_carriage_hosts.json")
    for _p in (DEP202, DEP172, DEP182, DEP209):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"
    PROD_FLOOR = -60.0                     # CF-1's production value
    N400 = 400
    REWIRE_P = 0.10
    DEEP_RUNGS = (-40.0, -45.0, -50.0, -55.0, -60.0)
    DEEP_INSTANCES = (0, 1)
    UNION_BAR = 99                         # >= 99/110 on EVERY host
    INTERFERENCE_BAR = 0.05                # mV, U3's pre-named bar
    SEP_WORST_202 = 5.285                  # exp202's deposited worst
    SEP_WORST_209 = 5.298                  # exp209's deposited worst

    with open(DEP202) as fh:
        dep202 = json.load(fh)
    with open(DEP172) as fh:
        dep172 = json.load(fh)
    with open(DEP182) as fh:
        dep182 = json.load(fh)
    with open(DEP209) as fh:
        dep209 = json.load(fh)

    # ---- the host-parameterized instrument replica (exp202's,
    #      VERBATIM semantics — exp209's copy re-used byte-for-byte) --
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
    #      exp202's _targets_for VERBATIM) ------------------------------
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
    #      exp209's build VERBATIM) -------------------------------------
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
    #      exp209's build VERBATIM) -------------------------------------
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

    # ---- the floors: CF-1's production value asserted ----------------
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR \
        and g6.NEURAL_SPEC_MIN == PROD_FLOOR, \
        f"floor drift: {CORE.NEURAL_SPEC_MIN}, {g6.NEURAL_SPEC_MIN}"

    def run_host(h: dict) -> dict:
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
        for p in per_target:
            tkey = (str(p["index"]) if p["tclass"] == "manifest"
                    else f"r{p['rung']:g}i{p['instance']}")
            print(f"  [{h['name']} {p['tclass']} {tkey}] "
                  f"writable={p['writable']} margin={p['margin3']}")
        margins = [p["margin3"] for p in per_target
                   if p["margin3"] is not None]
        return {"host": h["name"], "n": int(n),
                "kind": ("reference (exp182's own host)"
                         if h["name"] == "H0" else
                         "size-law organism (exp198's scale)"
                         if h["name"] == "H1" else
                         "corpus-rewired organism"),
                "seeds": list(AUDIT_SEEDS), "S_star": list(S_STAR),
                "n_writable": sum(1 for p in per_target if p["writable"]),
                "n_targets": len(per_target),
                "n_writable_manifest": sum(
                    1 for p in per_target
                    if p["writable"] and p["tclass"] == "manifest"),
                "n_writable_deep": sum(
                    1 for p in per_target
                    if p["writable"] and p["tclass"] == "deep"),
                "miss_list": [f"{p['tclass']}_"
                              f"{p.get('index', (p['rung'], p['instance']))}"
                              for p in per_target if not p["writable"]],
                "worst_case_margin3": (min(margins) if margins else None),
                "per_target": per_target,
                "rewire_seed": h.get("rewire_seed"),
                "record": h.get("record")}

    def run_k1() -> dict:
        """GATE-U1 clause (b): exp172's prices bit-exact at the
        reference (exp209's K1 rows re-verified — the same 30-row
        replay, the replica at H0 at exp172's deposited protocol)."""
        recs = {(r["rung"], r["instance"], r["seed"]): r
                for r in dep172["records"]}
        rows, n_exact = [], 0
        for rung in DEEP_RUNGS:
            for inst in DEEP_INSTANCES:
                f, triples, _ref = deep_target_for(rung, inst)
                for s in AUDIT_SEEDS:
                    dep = recs[(rung, inst, s)]["patched"]
                    dec = _decode_host(f, triples, g6.A_CHAIN,
                                       labeling_bfs_n(g6.A_CHAIN),
                                       g6.N, 1.0, 0.0, s)
                    assert not dec.get("rejected"), \
                        f"U1 rejection at r{rung:g} i{inst} s{s}"
                    ok = (float(dec["decode_err"])
                          == float(dep["decode_err_exact"])
                          and float(dec["hold_err"])
                          == float(dep["hold_err_exact"]))
                    n_exact += int(ok)
                    rows.append({"rung": rung, "instance": inst,
                                 "seed": s, "bit_exact": ok})
        return {"n_rows": len(rows), "n_bit_exact": n_exact,
                "rows": rows,
                "protocol": ("rung (1.0, 0.0) = exp172's deposited "
                             "GAMMA/MU; the CF-1 patched floor -60.0 "
                             "asserted; seeds (1,2,3); exp209's K1 "
                             "replay re-verified")}

    # ---- dispatch ----------------------------------------------------
    jobs = (["gates"] if args.job == "gates"
            else ["H0", "H1", "corpus"] if args.job == "all"
            else [args.job])
    assert not args.smoke, "smoke not registered for exp214"

    def _separate_margins() -> dict:
        """The two separate runs' per-(host, target) margin3 rows —
        the U3 reference (the union's own computation is identical
        machinery; any drift beyond 0.05 is interference named)."""
        sep = {}
        h0 = dep202["sections"]["H0"]
        h1 = dep202["sections"]["H1"]
        for hn, sec in (("H0", h0), ("H1", h1)):
            for r in sec["per_target"]:
                sep[(hn, "manifest", int(r["index"]))] = r.get("margin3")
        for k in sorted(dep202["sections"]["corpus"]["hosts"]):
            for r in dep202["sections"]["corpus"]["hosts"][k][
                    "per_target"]:
                sep[(k, "manifest", int(r["index"]))] = r.get("margin3")
        for hn in ("H0", "H1"):
            sec = dep209["sections"][hn]["carriage"]
            for r in sec["per_target"]:
                sep[(hn, "deep",
                     (float(r["rung"]), int(r["instance"])))] = \
                    r.get("margin3")
        for c in dep209["sections"]["corpus"]["carriages"]:
            for r in c["per_target"]:
                sep[(c["host"], "deep",
                     (float(r["rung"]), int(r["instance"])))] = \
                    r.get("margin3")
        return sep

    def _close_gates_on(merged_path: str) -> dict:
        with open(merged_path) as fh:
            merged = json.load(fh)
        secs = merged["sections"]
        assert all(k in secs for k in ("H0", "H1", "corpus")), \
            f"merged deposit incomplete: {sorted(secs)}"
        k1 = secs["H0"]["k1"]
        hosts_all = ([secs["H0"]["carriage"], secs["H1"]["carriage"]]
                     + secs["corpus"]["carriages"])
        n_hosts = len(hosts_all)
        per_host_ok = [h["n_writable"] >= UNION_BAR for h in hosts_all]
        worst = min(hosts_all,
                    key=lambda h: (h["worst_case_margin3"]
                                   if h["worst_case_margin3"]
                                   is not None else -1e9))
        all_finite = all(
            p["margin3"] is not None or p["rejected"]
            for h in hosts_all for p in h["per_target"])
        # U3: the interference question (each clause evaluated once)
        sep = _separate_margins()
        pairs = []
        n_bit_exact_vs_sep = 0
        n_compared = 0
        for h in hosts_all:
            for p in h["per_target"]:
                key = (h["host"], p["tclass"],
                       (int(p["index"]) if p["tclass"] == "manifest"
                        else (float(p["rung"]), int(p["instance"]))))
                s = sep.get(key)
                if s is None:
                    continue
                n_compared += 1
                if p["margin3"] is not None and \
                        float(p["margin3"]) == float(s):
                    n_bit_exact_vs_sep += 1
                if p["margin3"] is None or \
                        float(p["margin3"]) < float(s) - INTERFERENCE_BAR:
                    pairs.append({"host": h["host"],
                                  "tclass": p["tclass"],
                                  "target": key[2],
                                  "union_margin3": p["margin3"],
                                  "separate_margin3": s})
        min_sep = min(SEP_WORST_202, SEP_WORST_209)
        union_worst = worst["worst_case_margin3"]
        u3_branch = ("NO-INTERFERENCE"
                     if union_worst is not None
                     and union_worst >= min_sep - INTERFERENCE_BAR
                     else "INTERFERENCE-NAMED")
        gates = {
            "U1": {"pass": bool(
                k1["n_bit_exact"] == k1["n_rows"] == 30
                and merged["sections"]["H0"]["carriage"].get(
                    "manifest_checksum_ok", False)),
                   "k1_rows": k1["n_rows"],
                   "k1_bit_exact": k1["n_bit_exact"],
                   "manifest_checksum_on_H0": merged["sections"]["H0"][
                       "carriage"].get("manifest_checksum_ok", False),
                   "n_manifest": 100},
            "U2": {"pass": bool(n_hosts == 12 and all(per_host_ok)),
                   "n_hosts": n_hosts,
                   "bar": ">= 99/110 targets writable_3seed at S* on "
                          "EVERY host",
                   "per_host_writable": [
                       {"host": h["host"], "n_writable": h["n_writable"],
                        "manifest": h["n_writable_manifest"],
                        "deep": h["n_writable_deep"]}
                       for h in hosts_all],
                   "miss_lists": {h["host"]: h["miss_list"]
                                  for h in hosts_all}},
            "U3": {"pass": bool(u3_branch == "NO-INTERFERENCE"),
                   "branch": u3_branch,
                   "union_worst_margin3": union_worst,
                   "worst_host": worst["host"],
                   "min_separate_worst": min_sep,
                   "separate_worsts": {"exp202": SEP_WORST_202,
                                       "exp209": SEP_WORST_209},
                   "interference_bar_mV": INTERFERENCE_BAR,
                   "n_pairs_compared": n_compared,
                   "n_margin3_bit_exact_vs_separate":
                       n_bit_exact_vs_sep,
                   "interference_pairs": pairs},
            "U4": {"pass": bool(all_finite),
                   "all_errs_finite_or_rejected": bool(all_finite),
                   "lock_log_triples": len(_LOCK_LOG),
                   "all_at_S_star": True,
                   "no_per_target_tuning": True}}
        n_pass = sum(1 for g in gates.values() if g["pass"])
        verdict = (f"{n_pass}/4 gates (U1 U2 U3 U4) | {u3_branch} | "
                   f"worst host {worst['host']} at {union_worst}")
        print(f"  === {verdict} ===")
        merged["gates"] = gates
        merged["verdict"] = verdict
        merged["wall_s"] = round(time.time() - t0, 1)
        merged["pre_registered"] = {
            "gates_source": ("module docstring, committed before "
                             "any run (pre-registration 08b1cfc, "
                             "batch 10; gates U1-U4 fixed there, "
                             "each evaluated exactly once)")}
        merged["manifest_block"] = manifest_block
        with open(merged_path, "w") as fh:
            json.dump(merged, fh, indent=1, default=float)
        print(f"  deposited {merged_path}")
        return merged

    if args.job == "gates":
        return _close_gates_on(out_path)

    hosts = build_hosts()
    sections: dict = {}
    if "H0" in jobs:
        # U1 clause (a): the manifest's f_sha256 checksummed on H0
        # (the rebuild asserts inside manifest_targets)
        manifest_targets("H0", hosts["H0"]["canon"], hosts["H0"]["n"],
                         checksum=True)
        k1 = run_k1()
        h0 = run_host(hosts["H0"])
        h0["manifest_checksum_ok"] = True
        sections["H0"] = {"k1": k1, "carriage": h0}
        print(f"  [H0] U1 checksum 100/100 | K1 exact "
              f"{k1['n_bit_exact']}/{k1['n_rows']} | writable "
              f"{h0['n_writable']}/{h0['n_targets']}")
    if "H1" in jobs:
        sections["H1"] = {"carriage": run_host(hosts["H1"])}
        print(f"  [H1] writable "
              f"{sections['H1']['carriage']['n_writable']}/110")
    if "corpus" in jobs:
        cars = []
        for k in sorted(hosts):
            if k in ("H0", "H1"):
                continue
            cars.append(run_host(hosts[k]))
            print(f"  [{k}] writable {cars[-1]['n_writable']}/110")
        sections["corpus"] = {"carriages": cars}

    result = {"exp": "exp214_union_carriage", "sections": sections}
    if args.job != "all":
        os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                    exist_ok=True)
        with open(out_path, "w") as fh:
            json.dump(result, fh, indent=1, default=float)
        print(f"  deposited {out_path} (shard {args.job})")
        return result

    # local all-in-one: close the gates on the merged sections
    merged = {"exp": "exp214_union_carriage", "sections": sections}
    tmp = out_path + ".merge"
    with open(tmp, "w") as fh:
        json.dump(merged, fh, indent=1, default=float)
    return _close_gates_on(tmp)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all", "H0", "H1", "corpus",
                                      "gates"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
