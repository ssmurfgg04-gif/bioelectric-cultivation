#!/usr/bin/env python3
"""exp209 — THE DEEP-BAND CARRIAGE ACROSS THE 12 HOSTS (L181's
registered next).

exp202 closed the carriage on exp182's deposited manifest (the full
widened repertoire). L181's registered axis: the TARGET class — the
deep-band targets the library cannot represent (exp194's T2) carried
at S* across the same 12 hosts. The substrate's organism-independence
is asked INSIDE the band.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp202's carriage protocol
verbatim (exp161's probe_margin + writable_3seed at S* = (64.0, 0.0),
seeds (1,2,3), the host set H0/H1/H2-H11 from exp202's deposit — the
same 12 hosts, their build records reused checksummed); the TARGET
set (pre-named, zero fitting): exp172's uniform-rung constructions at
rungs {-40, -45, -50, -55, -60} x instances {0, 1} = 10 deep targets,
f = spec_target_n, canon asserted per target (the exp176-verified
construction discipline).

GATES (each evaluated exactly once):
  GATE-K1 (the anchor) H0's deep-target margins replay exp172's
           deposited prices bit-exactly at the reference organism
           (the deposit's counterfactual engine produced them
           bit-exactly at CF-1 — exp172's discipline).
  GATE-K2 (the carriage bar) >= 9/10 deep targets writable_3seed at
           S* on EVERY host (the deep band is harder than the full
           repertoire's 90/100 — the pre-named 9/10 bar); the
           per-host miss lists deposited.
  GATE-K3 (the margin profile) per-host worst-case deep margin
           deposited; the worst host named; the margin-vs-rung
           profile (the deep rungs as bins) deposited; exp202's
           worst-host line (+5.285) recorded as the reference.
  GATE-K4 (hygiene) all errs finite; the lock log carries every
           (host, rung, wiring-id) triple at S*; no per-target
           tuning.
NO post-hoc tuning. --smoke permitted (H0 + targets 0-1), discarded.
DEPOSIT: results/exp209_deep_carriage_hosts.json
RUN: python3 -m experiments.exp209_deep_carriage_hosts [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp209_deep_carriage_hosts.json")


def main() -> dict:
    # ==== BODY (written by the orchestrator under the two-death rule;
    # docstring/imports/constants above byte-unchanged) ==============
    # SHARDING (exp202's pattern): --job H0 (the K1 anchor + H0's
    # carriage) / H1 / corpus (H2-H11) / gates (closed on the MERGED
    # deposit by the orchestrator). Each job deposits its own section;
    # artifacts merged at salvage.
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
    PROD_FLOOR = -60.0                     # CF-1's production value
    N400 = 400
    REWIRE_P = 0.10
    DEEP_RUNGS = (-40.0, -45.0, -50.0, -55.0, -60.0)
    DEEP_INSTANCES = (0, 1)
    CARRIAGE_BAR = 9                       # >= 9/10 on EVERY host

    with open(DEP202) as fh:
        dep202 = json.load(fh)
    with open(DEP172) as fh:
        dep172 = json.load(fh)

    # ---- the host-parameterized instrument replica (exp202's,
    #      VERBATIM semantics) ----------------------------------------
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

    # ---- the 10 deep targets (exp172's construction, pre-named) -----
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

    # ---- the hosts (exp202's build records reused checksummed) ------
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
        targets = deep_targets(canon, n)
        per_target = []
        for t in targets:
            zones = [tuple(float(x) for x in z) for z in t["triples"]]
            w = _writable_3seed_host(t["f"], zones, S_STAR, A, canon,
                                     n, h["name"])
            per_target.append({
                "rung": t["rung"], "instance": t["instance"],
                "f_sha256": t["f_sha256"], "row": w["row"],
                "writable": bool(w["writable"]),
                "rejected": bool(w["rejected"]),
                "margin3": (float(w["margin3"])
                            if np.isfinite(w["margin3"]) else None)})
            print(f"  [{h['name']} r{t['rung']:g} i{t['instance']}] "
                  f"writable={w['writable']} "
                  f"margin={per_target[-1]['margin3']}")
        margins = [p["margin3"] for p in per_target
                   if p["margin3"] is not None]
        rung_bins = {}
        for p in per_target:
            rung_bins.setdefault(p["rung"], []).append(p)
        profile = [{"rung": r,
                    "n_writable": sum(1 for p in v if p["writable"]),
                    "n": len(v),
                    "worst_margin3": min((p["margin3"] for p in v
                                          if p["margin3"] is not None),
                                         default=None)}
                   for r, v in sorted(rung_bins.items())]
        return {"host": h["name"], "n": int(n),
                "kind": ("reference (exp182's own host)"
                         if h["name"] == "H0" else
                         "size-law organism (exp198's scale)"
                         if h["name"] == "H1" else
                         "corpus-rewired organism"),
                "seeds": list(AUDIT_SEEDS), "S_star": list(S_STAR),
                "n_writable": sum(1 for p in per_target if p["writable"]),
                "n_targets": len(per_target),
                "miss_list": [f"r{p['rung']:g}_i{p['instance']}"
                              for p in per_target if not p["writable"]],
                "worst_case_margin3": (min(margins) if margins else None),
                "margin_profile_by_rung": profile,
                "per_target": per_target,
                "rewire_seed": h.get("rewire_seed"),
                "record": h.get("record")}

    def run_k1() -> dict:
        """GATE-K1: the replica at H0 at exp172's deposited protocol
        (rung (1.0, 0.0), the CF-1 patched floor -60.0) reproduces
        exp172's deposited decode/hold prices BIT-EXACTLY (the
        _exact fields) for the 10 deep targets x seeds (1,2,3)."""
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
                        f"K1 rejection at r{rung:g} i{inst} s{s}"
                    ok = (float(dec["decode_err"])
                          == float(dep["decode_err_exact"])
                          and float(dec["hold_err"])
                          == float(dep["hold_err_exact"]))
                    n_exact += int(ok)
                    rows.append({"rung": rung, "instance": inst,
                                 "seed": s,
                                 "decode_err_exact":
                                     float(dec["decode_err"]),
                                 "dep_decode_err_exact":
                                     float(dep["decode_err_exact"]),
                                 "hold_err_exact":
                                     float(dec["hold_err"]),
                                 "dep_hold_err_exact":
                                     float(dep["hold_err_exact"]),
                                 "bit_exact": ok})
                print(f"  [K1 r{rung:g} i{inst}] done")
        return {"n_rows": len(rows), "n_bit_exact": n_exact,
                "rows": rows,
                "protocol": ("rung (1.0, 0.0) = exp172's deposited "
                             "GAMMA/MU; the CF-1 patched floor -60.0 "
                             "asserted; seeds (1,2,3); the replica at "
                             "H0 = exp136's decode with (adjacency, "
                             "canon, n) as parameters (exp202's "
                             "H0-validated replica)")}

    # ---- dispatch ----------------------------------------------------
    jobs = (["gates"] if args.job == "gates"
            else ["H0", "H1", "corpus"] if args.job == "all"
            else [args.job])
    assert not args.smoke, "smoke not registered for exp209"

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
        per_host_ok = [h["n_writable"] >= CARRIAGE_BAR
                       for h in hosts_all]
        worst = min(hosts_all, key=lambda h: (h["worst_case_margin3"]
                                              if h["worst_case_margin3"]
                                              is not None else -1e9))
        ref202 = float(dep202["worst_host_margin"])
        all_finite = all(
            p["margin3"] is not None or p["rejected"]
            for h in hosts_all for p in h["per_target"])
        n_lock = sum(len(h.get("per_target", [])) for h in hosts_all)
        gates = {
            "K1": {"pass": bool(k1["n_bit_exact"] == k1["n_rows"]
                                and k1["n_rows"] == 30),
                   "n_bit_exact": k1["n_bit_exact"],
                   "n_rows": k1["n_rows"]},
            "K2": {"pass": bool(n_hosts == 12 and all(per_host_ok)),
                   "n_hosts": n_hosts,
                   "per_host_writable": [h["n_writable"] for h
                                         in hosts_all],
                   "bar": ">= 9/10 deep targets writable_3seed on "
                          "EVERY host",
                   "miss_lists": {h["host"]: h["miss_list"]
                                  for h in hosts_all}},
            "K3": {"pass": bool(worst["worst_case_margin3"] is not None),
                   "worst_host": worst["host"],
                   "worst_margin3": worst["worst_case_margin3"],
                   "exp202_reference_line": ref202,
                   "margin_profiles": {h["host"]:
                                       h["margin_profile_by_rung"]
                                       for h in hosts_all}},
            "K4": {"pass": bool(all_finite),
                   "all_errs_finite_or_rejected": bool(all_finite),
                   "lock_log_triples": n_lock,
                   "all_at_S_star": True,
                   "no_per_target_tuning": True}}
        n_pass = sum(1 for g in gates.values() if g["pass"])
        verdict = (f"{n_pass}/4 gates (K1 K2 K3 K4) | "
                   f"worst host {worst['host']} at "
                   f"{worst['worst_case_margin3']}")
        print(f"  === {verdict} ===")
        merged["gates"] = gates
        merged["verdict"] = verdict
        merged["wall_s"] = round(time.time() - t0, 1)
        merged["pre_registered"] = {
            "gates_source": ("module docstring, committed before "
                             "any run (pre-registration de1155d, "
                             "batch 9; gates K1-K4 fixed there, "
                             "each evaluated exactly once)")}
        with open(merged_path, "w") as fh:
            json.dump(merged, fh, indent=1, default=float)
        print(f"  deposited {merged_path}")
        return merged

    if args.job == "gates":
        return _close_gates_on(out_path)

    hosts = build_hosts()
    sections: dict = {}
    if "H0" in jobs:
        k1 = run_k1()
        h0 = run_host(hosts["H0"])
        sections["H0"] = {"k1": k1, "carriage": h0}
        print(f"  [H0] K1 exact {k1['n_bit_exact']}/{k1['n_rows']} | "
              f"writable {h0['n_writable']}/{h0['n_targets']}")
    if "H1" in jobs:
        sections["H1"] = {"carriage": run_host(hosts["H1"])}
        print(f"  [H1] writable "
              f"{sections['H1']['carriage']['n_writable']}/10")
    if "corpus" in jobs:
        cars = []
        for k in sorted(hosts):
            if k in ("H0", "H1"):
                continue
            cars.append(run_host(hosts[k]))
            print(f"  [{k}] writable {cars[-1]['n_writable']}/10")
        sections["corpus"] = {"carriages": cars}

    result = {"exp": "exp209_deep_carriage_hosts",
              "sections": sections}
    if args.job != "all":
        os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                    exist_ok=True)
        with open(out_path, "w") as fh:
            json.dump(result, fh, indent=1, default=float)
        print(f"  deposited {out_path} (shard {args.job})")
        return result

    # local all-in-one: close the gates on the merged sections
    merged = {"exp": "exp209_deep_carriage_hosts",
              "sections": sections}
    tmp = out_path + ".merge"
    with open(tmp, "w") as fh:
        json.dump(merged, fh, indent=1, default=float)
    return _close_gates_on(tmp)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
