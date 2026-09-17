#!/usr/bin/env python3
"""exp202 — CROSS-ORGANISM CARRIAGE (Stage 4's cross-organism edge).

Stage 4's cross-substrate leg closed 100/100 (exp182: S* = (64.0,
0.0) carries 100 fresh targets at worst-case margin +5.404 on the
REFERENCE organism, the n=100 A_CHAIN lattice). The registered
cross-organism question: does the SAME substrate carriage hold on
DIFFERENT HOST GEOMETRIES — the size law's scale (n=400) and the
corpus's rewired organism structures?

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp182's protocol VERBATIM
(probe_margin + writable_3seed at the locked substrate rung
S* = (64.0, 0.0), seeds (1, 2, 3), exp161's _lock_substrate asserted
per write); TARGETS = exp182's DEPOSITED 100-target manifest reused
checksummed (zero new fitting — the manifest IS the pre-registration
artifact); HOSTS (the pre-named set, zero fitting):
  H0 the reference organism (n=100, A_CHAIN — exp182's own host; the
     replay anchor),
  H1 the size-law organism (n=400, labeling_bfs_n(A_CHAIN-400) —
     exp198's scale),
  H2-H11 TEN corpus-rewired organisms: exp88's rewire machinery
     applied to the first 10 PlanformDB records (seed = 202200 + i,
     disclosed), each yielding a host adjacency with its own canon
     labeling asserted == its engine canon.

GATES (each evaluated exactly once):
  GATE-H1 (anchors) H0 replays exp182's verdicts bit-exactly (the
           writability set and margins at deposit rounding); every
           host's canon == its engine canon asserted.
  GATE-H2 (the carriage bar) >= 90/100 targets writable_3seed at S*
           on EVERY host H1-H11; the per-host miss lists deposited;
           zero rejections.
  GATE-H3 (the margin profile — the deliverable) per-host worst-case
           margin deposited; the worst host NAMED; the per-host
           margin-vs-depth profile (exp182's four bins) deposited;
           exp182's +5.404 recorded as the reference line.
  GATE-H4 (hygiene) all errs finite; no per-target or per-host
           tuning anywhere; the substrate lock log carries every
           (host, rung, wiring-id) triple at S*.
NO post-hoc tuning. --smoke permitted (H0 + targets 0-2), discarded.
DEPOSIT: results/exp202_cross_organism_carriage.json
RUN: python3 -m experiments.exp202_cross_organism_carriage [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp202_cross_organism_carriage.json")


def main() -> dict:
    # ---- BODY (written by the run agent; docstring/imports/constants
    # ---- byte-unchanged). The __main__ block calls main() with no
    # ---- arguments, so the body re-parses sys.argv with the SAME
    # ---- flags to honor --smoke/--job/--out.
    #
    # IMPLEMENTATION DISCLOSURES (made now, BEFORE any instrument call;
    # deposited verbatim in pre_registered):
    #   * H0 runs exp161's probe_margin/writable_3seed VERBATIM (the
    #     A_CHAIN-fixed modules — the replay anchor needs the exact
    #     deposited code path). H1-H11 run the HOST-PARAMETERIZED
    #     replica of the same instruments: exp136's erosion/decode
    #     verbatim with (adjacency, canon, n) as parameters (they are
    #     A_CHAIN/N-hard-wired in exp136), exp150's price_rung row
    #     semantics verbatim, exp161's probe/writable/lock semantics
    #     verbatim. The replica is VALIDATED bit-exactly on H0 (both
    #     paths run the full 100-target battery there; deposited).
    #   * A host's canon = exp94's labeling_bfs_n(A_host) — the
    #     engine's deposited canon machinery for arbitrary wiring
    #     (in-module since exp94; used by every cross-topology run).
    #     Asserted == the engine canon computed FRESH inside every
    #     decode call (the split-brain guard), and on the path hosts
    #     (H0/H1) additionally == wildtype_target(n).
    #   * H1 = path(400) — the SAME constructor that builds A_CHAIN
    #     (cultivation.substrate.graph.path; A_CHAIN = path(100)),
    #     exp198's scale (N400 = 400).
    #   * H2-H11: exp88's loader verbatim (planform_mining.DB +
    #     load_widened + exp70's classify_onset + exp60's
    #     experiment_family) and exp88's record->arm mapping VERBATIM.
    #     A record whose arm is None cannot yield a host -> the
    #     disclosed host-reject list (cap 3; more fails H2's build
    #     clause). The first 10 arm-bearing records in loader order
    #     become H2..H11. Each host adjacency = the repo's frozen
    #     rewire machinery (exp73's small_world, its registered
    #     default rewire_p = 0.10) at a GLOBAL seed cursor starting at
    #     the pre-registered 202200 and consumed in order (one seed per
    #     host attempt); a rewired candidate that fails connectivity is
    #     redrawn at seed+1 (disclosed redraw log; hygiene — the
    #     instruments assume a connected host). The record's exp88 arm
    #     (protocol, plane, cf) is carried as the host's corpus
    #     provenance.
    import hashlib
    import re
    import sqlite3
    import time

    import numpy as np

    import experiments.exp136_generator_v6 as g6
    from cultivation.bioelectric.collective import (  # noqa: E402
        NEURAL_SPEC_MIN,
    )
    from cultivation.compiler.anatomy import (  # noqa: E402
        AnatomySpec, Zone, compile_anatomy,
    )
    from cultivation.substrate.graph import (  # noqa: E402
        GraphCollective, path as graph_path,
    )
    from experiments.exp136_generator_v6 import (  # noqa: E402
        AUDIT_SEEDS, ERR_BAR,
    )
    from experiments.exp161_universal_substrate import (  # noqa: E402
        _SUBSTRATE_FIXED, _SUBSTRATE_LOG,
        probe_margin as ref_probe_margin,
        writable_3seed as ref_writable_3seed,
    )
    from experiments.exp182_substrate_100 import S_STAR  # noqa: E402
    from experiments.exp60_gene_layer import experiment_family  # noqa: E402
    from experiments.exp70_onset_corpus import classify_onset  # noqa: E402
    from experiments.exp73_active_renormalization import (  # noqa: E402
        bfs_order, small_world,
    )
    from experiments.exp84_interaction_term import (  # noqa: E402
        ThetaOnlyCollective,
    )
    from experiments.exp90_two_source_read import star_dt  # noqa: E402
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n,
    )

    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["all", "H0", "H1", "corpus",
                                      "gates"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    t0 = time.time()
    out_path = args.out or OUT
    BAR = ERR_BAR                          # 6.0 mV — the unchanged bar
    DEP182 = os.path.join(ROOT, "results", "exp182_substrate_100.json")
    N400 = 400                             # exp198's scale
    REWIRE_P = 0.10                        # exp73 small_world's registered
    #                                        default — zero fitting
    SEED_CURSOR0 = 202200                  # the pre-registered seed base
    MAX_REJECTS = 3                        # the disclosed host-reject cap

    # ---- the host-parameterized instrument replica --------------------
    # (exp136 erosion/decode VERBATIM, (adjacency, canon, n) as
    # parameters; exp150 price_rung row semantics VERBATIM; exp161
    # probe/writable/lock semantics VERBATIM with the (host, rung,
    # wiring-id) lock triple of GATE-H4.)
    _LOCK_LOG: list[tuple] = []            # (host, rung, wiring-id)/write
    _HOST_WIRING: dict = {}                # host -> registered id(A)
    _n_canon_asserts = {"n": 0}            # engine-canon asserts fired

    def _lock_stats(entries: list) -> dict:
        rungs = [r for _h, r, _w in entries]
        wids = [w for _h, _r, w in entries]
        return {"n_writes": len(entries),
                "all_at_S_star": bool(all(r == S_STAR for r in rungs)),
                "wiring_id_constant": bool(len(set(wids)) <= 1),
                "n_unique_wiring_ids": len(set(wids)),
                "disclosure": ("the logged wiring-id is id(adjacency) "
                               "— process-local; the clause is its "
                               "CONSTANCY within a host's battery "
                               "(the lock also raises on any drift)")}

    def _lock_substrate_host(host: str, rung: tuple, A: np.ndarray) -> None:
        assert rung == S_STAR, \
            f"substrate drift on {host}: write used {rung}, fixed {S_STAR}"
        assert id(A) == _HOST_WIRING[host], \
            f"wiring object changed on {host}"
        _LOCK_LOG.append((host, rung, id(A)))

    def _erosion_host(f: np.ndarray, A: np.ndarray, n: int,
                      gamma: float, mu: float, config: str,
                      seed: int) -> float:
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

    def _decode_host(f: np.ndarray, zones, A: np.ndarray,
                     canon: np.ndarray, n: int, gamma: float, mu: float,
                     seed: int) -> dict:
        # THE ENGINE-CANON ASSERT (per call): the canon the target
        # builder used must be the engine canon of THIS wiring,
        # computed fresh via exp94's machinery.
        assert np.array_equal(canon, labeling_bfs_n(A)), \
            "canon mismatch: the builder's canon != the engine canon"
        _n_canon_asserts["n"] += 1
        spec = AnatomySpec(
            zones=[Zone(f0=a, f1=b, voltage=v, name=f"z{k}")
                   for k, (a, b, v) in enumerate(zones)],
            amputate_plane=None, spec_name="invention", somatic_latch=False)
        dt = star_dt(gamma, float(A.sum(axis=1).max()))
        c = GraphCollective(adjacency=A, seed=seed, gamma=gamma,
                            mu_theta=mu)
        c.set_target(canon)               # the D3 canon memory
        c.write_spec_layer(f)             # R1: the spec layer
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
            parent_of: dict[int, int] = {}
            frontier: list[int] = []
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
        c.run(100.0, dt=dt)               # the stability hold
        e_hold = float(c.pattern_error(f))
        return {"decode_err": e_decode, "hold_err": e_hold,
                "rejected": []}

    def _price_rung_host(f: np.ndarray, zones, rung: tuple,
                         A: np.ndarray, canon: np.ndarray, n: int,
                         host: str) -> dict:
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

    def _probe_margin_host(f: np.ndarray, zones, rung: tuple,
                           A: np.ndarray, canon: np.ndarray,
                           n: int) -> float:
        g, mu = rung
        eV = _erosion_host(f, A, n, g, 0.0, "V_only", 1)
        eT = _erosion_host(f, A, n, g, mu, "theta_only", 1)
        quad1 = float(np.hypot(eV, eT))
        d = _decode_host(f, zones, A, canon, n, g, mu, 1)
        if d.get("rejected"):
            return -float("inf")          # compiler rejection
        return BAR - max(quad1, float(d["decode_err"]),
                         float(d["hold_err"]))

    def _writable_3seed_host(f: np.ndarray, zones, rung: tuple,
                             A: np.ndarray, canon: np.ndarray, n: int,
                             host: str) -> dict:
        row = _price_rung_host(f, zones, rung, A, canon, n, host)
        rejected = bool(row["n_rejected"] > 0)
        if rejected:
            return {"row": row, "writable": False, "rejected": True,
                    "margin3": -float("inf")}
        m3 = BAR - max(row["quad"], max(row["decode_errs"]),
                       max(row["hold_errs"]))
        return {"row": row, "writable": bool(row["full_valid"]),
                "rejected": False, "margin3": float(m3)}

    # ---- io helpers ---------------------------------------------------
    def _sha_file(path: str) -> str:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()

    def _f_sha(f: np.ndarray) -> str:
        return hashlib.sha256(
            np.ascontiguousarray(f, dtype=np.float64).tobytes()
        ).hexdigest()

    def _load_out() -> dict:
        if os.path.exists(out_path):
            with open(out_path) as fh:
                return json.load(fh)
        return {}

    def _write_out(d: dict) -> str:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                    exist_ok=True)
        tmp = out_path + ".tmp"
        with open(tmp, "w") as fh:
            json.dump(d, fh, indent=1, default=float)
        os.replace(tmp, out_path)
        return out_path

    # ---- the exp182 manifest REUSED checksummed -----------------------
    with open(DEP182) as fh:
        dep182 = json.load(fh)
    manifest = dep182["manifest"]["targets"]
    assert len(manifest) == 100 and dep182["manifest"]["n_targets"] == 100
    assert [float(x) for x in dep182["battery"]["S_star"]] == \
        [S_STAR[0], S_STAR[1]], "exp182's deposited S* != this module's S*"
    ref_worst = float(dep182["battery"]["worst_case_margin3"])
    dep182_sha = _sha_file(DEP182)
    manifest_block = {
        "source": "results/exp182_substrate_100.json",
        "sha256": dep182_sha, "reused_not_regenerated": True,
        "target_seed": dep182["manifest"]["target_seed"],
        "n_targets": 100,
        "checksum_clause": ("f rebuilt per host from the deposited "
                            "triples via exp94's spec_target_n on the "
                            "HOST's canon; on H0 the rebuild's f_sha256 "
                            "must equal the deposited f_sha256 "
                            "(checksummed reuse; any mismatch raises)"),
        "targets": manifest,
    }

    # ---- target rebuild per host --------------------------------------
    _targets_cache: dict = {}

    def _targets_for(host_name: str, canon: np.ndarray, n: int,
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

    def _triples(t: dict) -> list[tuple]:
        return [tuple(z) for z in t["triples"]]

    # ---- the hosts ----------------------------------------------------
    def _build_fixed_hosts() -> dict:
        hosts: dict = {}
        canon0 = labeling_bfs_n(g6.A_CHAIN)
        assert np.array_equal(canon0, g6.wildtype_target(g6.N)), \
            "H0: canon mismatch vs the engine's wildtype"
        hosts["H0"] = {
            "name": "H0", "kind": "reference (exp182's own host)",
            "n": int(g6.N), "A": g6.A_CHAIN, "canon": canon0,
            "build": "exp136's A_CHAIN = path(100), the exp182 host; "
                     "canon asserted == wildtype_target(100)",
            "wildtype_checked": True}
        A400 = graph_path(N400)
        canon400 = labeling_bfs_n(A400)
        assert np.array_equal(canon400, g6.wildtype_target(N400)), \
            "H1: canon mismatch vs the engine's wildtype at n=400"
        hosts["H1"] = {
            "name": "H1", "kind": "size-law organism (exp198's scale)",
            "n": N400, "A": A400, "canon": canon400,
            "build": "path(400) — the SAME constructor that builds "
                     "A_CHAIN (A_CHAIN = path(100)); canon asserted == "
                     "wildtype_target(400)",
            "wildtype_checked": True}
        for h in hosts.values():
            _HOST_WIRING[h["name"]] = id(h["A"])
        return hosts

    def _exp88_records() -> list[dict]:
        """exp88's loader VERBATIM + exp88's record->arm mapping
        VERBATIM (its re-wiring). Returns the records in loader order
        with their exp88 arm (None where exp88's mapping yields none —
        the host-reject class)."""
        from experiments.planform_mining import DB, load_widened
        con = sqlite3.connect(DB)
        drugname = {i: nm for i, nm in
                    con.execute("SELECT Id, Name FROM Drug")}
        expdrugs: dict = {}
        for e, d, st, et in con.execute(
                "SELECT Experiment, Drug, StartTime, EndTime "
                "FROM ExperimentDrug"):
            expdrugs.setdefault(e, []).append(
                {"drug": drugname.get(d, d)})
        exps = load_widened(con)
        con.close()
        onset_of = {eid: classify_onset(v)
                    for eid, v in expdrugs.items()}
        rows = []
        for idx, (eid, e) in enumerate(exps.items()):
            group, plane = e["group"], e["plane"]
            cf = 0.5
            if plane == "crosspiece":
                f = e.get("cut_f")
                cf = min(max(round(float(f), 2), 0.05), 0.95) \
                    if f else 0.5
            arm = None
            if plane in ("head", "tail", "trunk", "head_tail",
                         "crosspiece"):
                if group == "cutting":
                    arm = ("cutting", plane, cf)
                elif group in ("innexin", "gj_block"):
                    if eid == 421:
                        arm = ("gjblock", "head", 0.5)
                    else:
                        onset = onset_of.get(eid, "sustained") \
                            if group == "gj_block" else "sustained"
                        proto = {"sustained": "gjblock",
                                 "delayed": "gjblock_delayed",
                                 "washout": "gjblock_washout"}.get(
                                     onset, "gjblock")
                        arm = (proto, plane, cf)
                elif group == "ion_channel":
                    arm = ("ion_channel", plane, cf)
                elif group == "morphogen":
                    if e.get("ap_morphogen"):
                        rnais = " | ".join(e.get("rnais", []))
                        arm = (("apc", plane, cf)
                               if re.search(r"apc|axin", rnais, re.I)
                               else ("wnt", plane, cf))
                elif group == "other_rnai":
                    fam = experiment_family(e.get("rnais", []))
                    arm = {"neoblast": ("neoblast", plane, cf),
                           "wnt_pos": ("wnt", plane, cf),
                           "wnt_ant": ("apc", plane, cf),
                           "neural": ("generic", plane, cf),
                           "generic": ("generic", plane, cf),
                           "control": ("cutting", plane, cf)}.get(fam)
            rows.append({"scan_index": idx, "eid": eid,
                         "group": group, "plane": plane,
                         "manipulation": e.get("manipulation"),
                         "arm": arm})
        return rows

    def _build_corpus_hosts(max_hosts: int = 10) -> tuple[dict, dict]:
        records = _exp88_records()
        chosen, rejects = [], []
        for r in records:
            if len(chosen) >= max_hosts:
                break
            if r["arm"] is None:
                rejects.append(r)
            else:
                chosen.append(r)
        hosts: dict = {}
        seed_cursor = SEED_CURSOR0
        redraw_log = []
        build_ok = bool(len(chosen) == max_hosts
                        and len(rejects) <= MAX_REJECTS)
        for k, r in enumerate(chosen):
            name = f"H{2 + k}"
            s = seed_cursor
            tries = 0
            while True:
                A = small_world(100, REWIRE_P, s)
                if len(bfs_order(A)) == 100:
                    break
                tries += 1
                s += 1
                if tries > 200:
                    raise RuntimeError(
                        f"{name}: no connected rewiring found")
            seed_cursor = s + 1
            redraw_log.append({"host": name, "seed": int(s),
                               "n_redraws": tries})
            canon = labeling_bfs_n(A)
            deg = A.sum(axis=1)
            hosts[name] = {
                "name": name,
                "kind": "corpus-rewired organism",
                "n": 100, "A": A, "canon": canon,
                "record": {"scan_index": r["scan_index"],
                           "eid": r["eid"], "group": r["group"],
                           "plane": r["plane"],
                           "manipulation": r["manipulation"],
                           "arm": list(r["arm"])},
                "rewire": {"machinery": "exp73's small_world (the "
                                        "repo's frozen rewire "
                                        "constructor)",
                           "rewire_p": REWIRE_P,
                           "seed": int(s), "n_redraws": tries,
                           "redraw_rule": "a candidate failing "
                                          "connectivity is redrawn at "
                                          "seed+1 (global cursor; "
                                          "hygiene, before any "
                                          "instrument call)"},
                "edges": int(np.triu(A, 1).sum()),
                "deg_range": [int(deg.min()), int(deg.max())],
                "wildtype_checked": False}
            _HOST_WIRING[name] = id(A)
        scan_block = {
            "construction": (
                "exp88's loader verbatim (planform_mining.DB + "
                "load_widened) and exp88's record->arm mapping "
                "verbatim; records scanned in loader order; a record "
                "whose exp88 arm is None cannot yield a host "
                "(host-reject list); the first 10 arm-bearing records "
                "become H2-H11; each host adjacency = exp73's "
                "small_world at its registered default rewire_p=0.10 "
                "with a global seed cursor from the pre-registered "
                "202200; the arm rides as the host's corpus "
                "provenance"),
            "n_records_scanned": len(records),
            "n_records_consumed": (chosen[-1]["scan_index"] + 1
                                   if chosen else 0),
            "n_chosen": len(chosen),
            "host_rejects": rejects,
            "n_host_rejects": len(rejects),
            "max_rejects_allowed": MAX_REJECTS,
            "build_ok": build_ok,
            "redraw_log": redraw_log,
        }
        return hosts, scan_block

    # ---- the battery on one host --------------------------------------
    def _run_battery(host: dict, targets: list[dict],
                     use_ref_instruments: bool) -> list[dict]:
        name, A, canon, n = (host["name"], host["A"], host["canon"],
                             host["n"])
        if use_ref_instruments:
            _SUBSTRATE_FIXED[:] = [S_STAR, id(g6.A_CHAIN)]
        per = []
        for t in targets:
            tr = _triples(t)
            if use_ref_instruments:
                pm = ref_probe_margin(t["f"], tr, S_STAR)
                v = ref_writable_3seed(t["f"], tr, S_STAR)
                _LOCK_LOG.append((name, S_STAR, id(g6.A_CHAIN)))
            else:
                pm = _probe_margin_host(t["f"], tr, S_STAR, A, canon, n)
                v = _writable_3seed_host(t["f"], tr, S_STAR, A, canon,
                                         n, name)
            row = v["row"]
            per.append({
                "index": t["index"], "zone_count": t["zone_count"],
                "triples": t["triples"], "vmin": t["vmin"],
                "vmax": t["vmax"], "f_sha256": t["f_sha256"],
                "probe_margin1": float(pm),
                "writable": bool(v["writable"]),
                "rejected": bool(v["rejected"]),
                "n_rejected": int(row["n_rejected"]),
                "margin3": float(v["margin3"]),
                "eV": row["eV"], "eT": row["eT"], "quad": row["quad"],
                "decode_errs": row["decode_errs"],
                "hold_errs": row["hold_errs"]})
            if (t["index"] + 1) % 10 == 0:
                print(f"  [{name}] ... {t['index'] + 1}/100 targets "
                      f"priced ({time.time() - t0:.0f}s)", flush=True)
        return per

    def _host_section(host: dict, per: list[dict],
                      extra: dict | None = None) -> dict:
        margins = [p["margin3"] for p in per
                   if np.isfinite(p["margin3"])]
        n_writable = sum(int(p["writable"]) for p in per)
        n_rej = sum(int(p["n_rejected"]) for p in per)
        worst = float(min(margins)) if margins else None
        mean_m = float(np.mean(margins)) if margins else None
        bins = [(-60.0, -50.0), (-50.0, -40.0), (-40.0, -30.0),
                (-30.0, -15.0)]
        profile = []
        for lo, hi in bins:
            tv, nv = [], 0
            for p in per:
                inb = [v for (_s, _e, v) in p["triples"]
                       if lo <= v < hi or (hi == -15.0 and v == hi)]
                if inb:
                    nv += len(inb)
                    if np.isfinite(p["margin3"]):
                        tv.append(p["margin3"])
            profile.append({
                "bin": f"[{lo:g},{hi:g}]" if hi == -15.0
                       else f"[{lo:g},{hi:g})",
                "n_zone_values": nv, "n_targets": len(tv),
                "worst_margin3": (round(float(min(tv)), 4) if tv
                                  else None),
                "mean_margin3": (round(float(np.mean(tv)), 4) if tv
                                 else None)})
        sec = {
            "host": host["name"], "n": host["n"],
            "kind": host["kind"],
            "seeds": list(AUDIT_SEEDS),
            "S_star": list(S_STAR),
            "n_writable": n_writable,
            "n_rejected_seeds": n_rej,
            "worst_case_margin3": (round(worst, 4)
                                   if worst is not None else None),
            "mean_margin3": (round(mean_m, 4)
                             if mean_m is not None else None),
            "miss_list": [{"index": p["index"],
                           "triples": p["triples"],
                           "margin3": (round(p["margin3"], 4)
                                       if np.isfinite(p["margin3"])
                                       else None),
                           "probe_margin1": (round(p["probe_margin1"], 4)
                                             if np.isfinite(
                                                 p["probe_margin1"])
                                             else None),
                           "rejected": p["rejected"],
                           "violated": [c for c, bad in [
                               ("audit", p["quad"] >= BAR),
                               ("decode",
                                max(p["decode_errs"]) >= BAR),
                               ("hold",
                                max(p["hold_errs"]) >= BAR)] if bad]}
                          for p in per if not p["writable"]],
            "margin_profile": {
                "bins": [b["bin"] for b in profile],
                "per_bin": profile,
                "note": "a target's margin enters every bin "
                        "containing >= 1 of its zone values "
                        "(exp182's four bins)"},
            "per_target": [{**p,
                            "probe_margin1": (
                                round(p["probe_margin1"], 4)
                                if np.isfinite(p["probe_margin1"])
                                else None),
                            "margin3": (round(p["margin3"], 4)
                                        if np.isfinite(p["margin3"])
                                        else None)}
                           for p in per],
            "n_canon_asserts": int(_n_canon_asserts["n"]),
        }
        if extra:
            sec.update(extra)
        return sec

    def _host_summary(host: dict, per: list[dict]) -> dict:
        margins = [p["margin3"] for p in per
                   if np.isfinite(p["margin3"])]
        return {"host": host["name"], "n": host["n"],
                "kind": host["kind"],
                "n_writable": sum(int(p["writable"]) for p in per),
                "n_rejected_seeds": sum(int(p["n_rejected"])
                                        for p in per),
                "worst_case_margin3": (round(float(min(margins)), 4)
                                       if margins else None),
                "mean_margin3": (round(float(np.mean(margins)), 4)
                                 if margins else None)}

    # ======================= --smoke ===================================
    if args.smoke:
        hosts = _build_fixed_hosts()
        h0 = hosts["H0"]
        targets = _targets_for("H0", h0["canon"], h0["n"],
                               checksum=True)[:3]
        print("=== exp202 SMOKE (H0 + targets 0-2, DISCARDED) ===")
        rows = []
        for t in targets:
            tr = _triples(t)
            _SUBSTRATE_FIXED[:] = [S_STAR, id(g6.A_CHAIN)]
            pm_r = ref_probe_margin(t["f"], tr, S_STAR)
            v_r = ref_writable_3seed(t["f"], tr, S_STAR)
            _LOCK_LOG.append(("H0", S_STAR, id(g6.A_CHAIN)))
            pm_l = _probe_margin_host(t["f"], tr, S_STAR, h0["A"],
                                      h0["canon"], h0["n"])
            v_l = _writable_3seed_host(t["f"], tr, S_STAR, h0["A"],
                                       h0["canon"], h0["n"], "H0")
            bitexact = bool(round(pm_r, 4) == round(pm_l, 4)
                            and v_r["writable"] == v_l["writable"]
                            and round(v_r["margin3"], 4)
                            == round(v_l["margin3"], 4))
            rows.append({"index": t["index"],
                         "probe_ref": round(pm_r, 4),
                         "probe_local": round(pm_l, 4),
                         "writable_ref": bool(v_r["writable"]),
                         "writable_local": bool(v_l["writable"]),
                         "margin3_ref": round(v_r["margin3"], 4),
                         "margin3_local": round(v_l["margin3"], 4),
                         "rejected": bool(v_r["rejected"]
                                          or v_l["rejected"]),
                         "bitexact": bitexact})
            print(f"  t{t['index']}: ref {pm_r:+.3f}/"
                  f"{v_r['writable']}/{v_r['margin3']:+.3f} | local "
                  f"{pm_l:+.3f}/{v_l['writable']}/"
                  f"{v_l['margin3']:+.3f} | bitexact {bitexact}")
        checks = {
            "zero_rejections": all(not r["rejected"] for r in rows),
            "all_finite": all(
                np.isfinite(r["probe_ref"]) and np.isfinite(r["probe_local"])
                for r in rows),
            "ref_lock_log_3_all_S_star": bool(
                len(_SUBSTRATE_LOG) == 3
                and all(r == S_STAR for r, _ in _SUBSTRATE_LOG)),
            "host_lock_log_6_all_S_star": bool(
                len(_LOCK_LOG) == 6
                and all(r == S_STAR for _h, r, _w in _LOCK_LOG)
                and all(h == "H0" for h, _r, _w in _LOCK_LOG)),
            "local_instrument_bitexact_on_H0": all(
                r["bitexact"] for r in rows),
        }
        ok = all(checks.values())
        print(f"  checks {checks} -> {'OK' if ok else 'INSTRUMENT BUG'} "
              f"({time.time() - t0:.1f}s)  [DISCARDED — no deposit]")
        dep = {"experiment": "exp202_cross_organism_carriage",
               "kind": "smoke", "discarded": True, "rows": rows,
               "checks": checks, "ok": ok}
        if args.out:
            _write_out(dep)
        return dep

    # =================== the credited run ==============================
    print(f"=== exp202: CROSS-ORGANISM CARRIAGE — 12 hosts x 100 "
          f"checksummed targets x 3 seeds at S* = {list(S_STAR)} "
          f"(job {args.job}) ===\n")
    print(f"  reference line (exp182, 100 targets on H0): worst-case "
          f"m3 {ref_worst:+.3f} | manifest {DEP182} "
          f"sha {dep182_sha[:12]}\n")

    jobs = ["H0", "H1", "corpus"] if args.job == "all" else [args.job]
    out = _load_out()
    out.setdefault("experiment", "exp202_cross_organism_carriage")
    out.setdefault("sections", {})
    changed = False

    if "H0" in jobs and "H0" not in out["sections"]:
        hosts = _build_fixed_hosts()
        h0 = hosts["H0"]
        targets = _targets_for("H0", h0["canon"], h0["n"],
                               checksum=True)
        print(f"  [H0] reference organism: n={h0['n']}, canon "
              f"== wildtype asserted; 100 targets checksummed vs the "
              f"deposit\n")
        per_ref = _run_battery(h0, targets, use_ref_instruments=True)
        lock_h0 = _lock_stats(_LOCK_LOG)
        print(f"  [H0] exp161 instruments done — now the "
              f"instrument VALIDATION: the host-parameterized replica "
              f"on H0 (must be bit-exact)\n")
        _n_canon_asserts["n"] = 0
        per_loc = _run_battery(h0, targets, use_ref_instruments=False)
        n_asserts_valid = _n_canon_asserts["n"]
        replay = []
        dep_rows = dep182["battery"]["per_target"]
        for a, b in zip(per_ref, dep_rows):
            assert a["index"] == b["index"]
            replay.append(bool(
                a["writable"] == b["writable"]
                and round(a["margin3"], 4) == round(b["margin3"], 4)
                and round(a["probe_margin1"], 4)
                == round(b["probe_margin1"], 4)))
        bitexact = bool(all(replay) and len(replay) == 100)
        valid = []
        for a, b in zip(per_ref, per_loc):
            valid.append(bool(
                a["writable"] == b["writable"]
                and round(a["margin3"], 4) == round(b["margin3"], 4)
                and round(a["probe_margin1"], 4)
                == round(b["probe_margin1"], 4)
                and a["quad"] == b["quad"]))
        valid_bitexact = bool(all(valid) and len(valid) == 100)
        sec = _host_section(h0, per_ref, extra={
            "instruments": "exp161's probe_margin + writable_3seed "
                           "VERBATIM (the exp182 code path)",
            "replay_bitexact": bitexact,
            "n_replay_rows": len(replay),
            "instrument_validation": {
                "what": "the host-parameterized replica run on H0 vs "
                        "the exp161 instruments (100 targets)",
                "bitexact": valid_bitexact,
                "n_rows": len(valid)},
            "n_canon_asserts": n_asserts_valid,
            "n_canon_asserts_note": ("the VALIDATION replica's "
                                     "engine-canon asserts; exp161's "
                                     "instruments assert nothing — "
                                     "H0's canon == wildtype is "
                                     "asserted at build"),
            "lock_log": lock_h0,
        })
        out["sections"]["H0"] = sec
        out.setdefault("host_summaries", {})
        out["host_summaries"]["H0"] = _host_summary(h0, per_ref)
        changed = True
        print(f"  [H0] replay vs exp182's deposit: "
              f"{'BIT-EXACT' if bitexact else 'MISMATCH'} | instrument "
              f"validation: {'BIT-EXACT' if valid_bitexact else 'MISMATCH'}"
              f" | writable {sec['n_writable']}/100, worst "
              f"{sec['worst_case_margin3']}\n")

    if "H1" in jobs and "H1" not in out["sections"]:
        hosts = _build_fixed_hosts()
        h1 = hosts["H1"]
        _n_canon_asserts["n"] = 0
        targets = _targets_for("H1", h1["canon"], h1["n"],
                               checksum=False)
        print(f"  [H1] size-law organism: n={h1['n']} path, canon "
              f"== wildtype(400) asserted; 100 targets rebuilt on the "
              f"host canon\n")
        lock_mark = len(_LOCK_LOG)
        per = _run_battery(h1, targets, use_ref_instruments=False)
        sec = _host_section(h1, per, extra={
            "instruments": "the host-parameterized replica (validated "
                           "bit-exact on H0)",
            "build": h1["build"],
            "lock_log": _lock_stats(_LOCK_LOG[lock_mark:])})
        out["sections"]["H1"] = sec
        out.setdefault("host_summaries", {})
        out["host_summaries"]["H1"] = _host_summary(h1, per)
        changed = True
        print(f"  [H1] writable {sec['n_writable']}/100, rejections "
              f"{sec['n_rejected_seeds']}, worst "
              f"{sec['worst_case_margin3']}\n")

    if ("corpus" in jobs or args.job == "all") \
            and "corpus" not in out["sections"]:
        chosts, scan_block = _build_corpus_hosts()
        print(f"  [corpus] {scan_block['n_chosen']} hosts built from "
              f"the first {scan_block['n_records_consumed']} loader "
              f"records; {scan_block['n_host_rejects']} "
              f"host-rejects (cap {MAX_REJECTS}); redraws "
              f"{sum(r['n_redraws'] for r in scan_block['redraw_log'])}"
              f"\n")
        corpus_hosts = {}
        for name in sorted(chosts):
            h = chosts[name]
            _n_canon_asserts["n"] = 0
            targets = _targets_for(name, h["canon"], h["n"],
                                   checksum=False)
            lock_mark = len(_LOCK_LOG)
            per = _run_battery(h, targets, use_ref_instruments=False)
            corpus_hosts[name] = _host_section(h, per, extra={
                "instruments": "the host-parameterized replica "
                               "(validated bit-exact on H0)",
                "record": h["record"], "rewire": h["rewire"],
                "edges": h["edges"], "deg_range": h["deg_range"],
                "lock_log": _lock_stats(_LOCK_LOG[lock_mark:])})
            out.setdefault("host_summaries", {})
            out["host_summaries"][name] = _host_summary(h, per)
            print(f"  [{name}] eid {h['record']['eid']} "
                  f"arm {h['record']['arm']}: writable "
                  f"{corpus_hosts[name]['n_writable']}/100, "
                  f"worst {corpus_hosts[name]['worst_case_margin3']}")
        out["sections"]["corpus"] = {"scan": scan_block,
                                     "hosts": corpus_hosts}
        changed = True

    # ---- shared blocks -------------------------------------------------
    out["claim"] = ("the SAME substrate carriage S* = (64.0, 0.0) "
                    "holds on DIFFERENT HOST GEOMETRIES: the n=400 "
                    "size-law organism and ten corpus-rewired "
                    "organisms, at the exp182 bar (>= 90/100 per host)")
    out["protocol"] = ("exp161's probe_margin + writable_3seed "
                       "semantics VERBATIM at the locked rung "
                       "S* = (64.0, 0.0), seeds (1, 2, 3); H0 via "
                       "exp161's modules verbatim; H1-H11 via the "
                       "host-parameterized replica (validated "
                       "bit-exact on H0); the (host, rung, wiring-id) "
                       "lock asserted per write")
    out["pre_registered"] = {
        "instruments": ("exp182's protocol VERBATIM: probe_margin + "
                        "writable_3seed at S* = (64.0, 0.0), seeds "
                        "(1, 2, 3), the substrate lock asserted per "
                        "write (exp161's _lock_substrate semantics, "
                        "extended with the host: the (host, rung, "
                        "wiring-id) triple)"),
        "targets": ("exp182's DEPOSITED 100-target manifest reused "
                    "checksummed (results/"
                    "exp182_substrate_100.json, sha256 recorded in "
                    "manifest.source); zero new fitting — the "
                    "manifest IS the pre-registration artifact; f "
                    "rebuilt per host on the host's canon (H0's "
                    "rebuild checksummed against the deposit)"),
        "hosts": ("H0 the reference organism (exp182's own host; the "
                  "replay anchor); H1 the size-law organism (path(400)"
                  ", exp198's scale); H2-H11 ten corpus-rewired "
                  "organisms (exp88's loader + arm mapping verbatim, "
                  "exp73's small_world rewire at its registered "
                  "default p=0.10, global seed cursor from 202200, "
                  "connected-redraw disclosed; arm rides as "
                  "provenance); the disclosed host-reject cap is 3"),
        "canon_clause": ("a host's canon = exp94's labeling_bfs_n(A) "
                         "(the engine's deposited canon machinery for "
                         "arbitrary wiring), asserted == the engine "
                         "canon computed fresh inside EVERY decode "
                         "call; on the path hosts it additionally "
                         "equals wildtype_target(n)"),
        "jobs": ("--job H0|H1|corpus run sections sequentially and "
                 "merge into the shared deposit; gates close exactly "
                 "once when all three sections are present"),
        "gates": {
            "H1": ("anchors) H0 replays exp182's verdicts bit-exactly "
                   "(the writability set and margins at deposit "
                   "rounding); every host's canon == its engine canon "
                   "asserted"),
            "H2": ("the carriage bar) >= 90/100 targets "
                   "writable_3seed at S* on EVERY host H1-H11; the "
                   "per-host miss lists deposited; zero rejections; "
                   "the corpus build clause (10 hosts, <= 3 "
                   "rejects) holds"),
            "H3": ("the margin profile — the deliverable) per-host "
                   "worst-case margin deposited; the worst host "
                   "NAMED; the per-host margin-vs-depth profile "
                   "(exp182's four bins) deposited; exp182's +5.404 "
                   "recorded as the reference line"),
            "H4": ("hygiene) all errs finite; no per-target or "
                   "per-host tuning anywhere; the substrate lock log "
                   "carries every (host, rung, wiring-id) triple at "
                   "S*"),
        },
        "no_post_hoc_tuning": ("S* fixed once before any verdict; the "
                               "host set + seeds fixed before any "
                               "instrument call; the manifest reused "
                               "checksummed"),
    }
    out["reference_line"] = {
        "source": "results/exp182_substrate_100.json",
        "sha256": dep182_sha,
        "S_star": [S_STAR[0], S_STAR[1]], "n_targets": 100,
        "worst_case_margin3": round(ref_worst, 4),
        "note": "exp182's +5.404 recorded as the reference line "
                "(GATE-H3)"}
    out["manifest"] = manifest_block
    out["smoke_disclosure"] = ("a --smoke check (H0 + targets 0-2) ran "
                               "before the credited run and was "
                               "discarded (no file; separate process)")
    out["wall_s"] = round(time.time() - t0, 1)

    # ---- gates (close exactly once, when all sections present) --------
    need = {"H0", "H1", "corpus"}
    have = set(out["sections"])
    if need <= have and "gates" not in out:
        gates = _close_gates(out, BAR, MAX_REJECTS, np)
        out["gates"] = gates
        out["gates_passed"] = f"{int(sum(gates.values()))}/4"
        out["verdict_one_line"] = _verdict_line(out, gates, np)
    elif "gates" in out:
        print("  gates already evaluated — the exact-once clause "
              "stands (no re-evaluation)")
    else:
        print(f"  partial deposit: sections {sorted(have)} merged; "
              f"gates pending {sorted(need - have)}")
        out["verdict"] = (f"partial — sections {sorted(have)} merged; "
                          f"gates pending {sorted(need - have)}")

    p = _write_out(out) if changed or "gates" in out else out_path
    if "gates" in out:
        g = out["gates"]
        print(f"\n  GATE-H1: {'PASS' if g['H1'] else 'REFUTE'} "
              f"(H0 replay {'bit-exact' if g['H1'] else 'BROKEN'}, "
              f"canon asserted on every host)")
        print(f"  GATE-H2: {'PASS' if g['H2'] else 'REFUTE'} "
              f"({g['h2_detail']})")
        print(f"  GATE-H3: {'PASS' if g['H3'] else 'REFUTE'} "
              f"(worst host {out.get('worst_host')}: "
              f"{out.get('worst_host_margin')} vs exp182's "
              f"{ref_worst:+.3f})")
        print(f"  GATE-H4: {'PASS' if g['H4'] else 'REFUTE'} "
              f"({g['h4_detail']})")
        print(f"  === {out['gates_passed']} gates PASS === "
              f"{out['verdict_one_line']}")
    print(f"  deposited {p} ({out['wall_s']}s)")
    return out


def _close_gates(out: dict, bar: float, max_rejects: int, np) -> dict:
    """GATES H1-H4 (each evaluated exactly once, over the merged
    deposit)."""
    s_h0 = out["sections"]["H0"]
    s_h1 = out["sections"]["H1"]
    s_cor = out["sections"]["corpus"]
    summaries = out["host_summaries"]

    # ---- GATE-H1 (anchors) -------------------------------------------
    # canon asserts: every decode call on H1-H11 asserted the host's
    # canon == its engine canon (any mismatch RAISES — the run's
    # completion is itself the evidence); count them for the record
    n_canon = (s_h1["n_canon_asserts"]
               + sum(h["n_canon_asserts"]
                     for h in s_cor["hosts"].values()))
    h1_gate = bool(s_h0["replay_bitexact"]
                   and s_h0["instrument_validation"]["bitexact"]
                   and n_canon > 0)

    # ---- GATE-H2 (the carriage bar) -----------------------------------
    corpus_build_ok = bool(s_cor["scan"]["build_ok"]
                           and s_cor["scan"]["n_host_rejects"]
                           <= max_rejects
                           and len(s_cor["hosts"]) == 10)
    per_host_ok = {}
    for name, s in [("H1", s_h1)] + list(s_cor["hosts"].items()):
        per_host_ok[name] = bool(s["n_writable"] >= 90
                                 and s["n_rejected_seeds"] == 0)
    n_hosts_ok = sum(per_host_ok.values())
    h2 = bool(corpus_build_ok and n_hosts_ok == 11)
    h2_detail = (f"{n_hosts_ok}/11 hosts at the >= 90/100 bar with "
                 f"zero rejections; corpus build "
                 f"{'ok' if corpus_build_ok else 'FAILED'} "
                 f"({s_cor['scan']['n_host_rejects']} rejects)")

    # ---- GATE-H3 (the margin profile — the deliverable) ----------------
    hosts_all = [summaries[k] for k in
                 sorted(summaries, key=lambda x: (len(x), x))]
    worsts = {s["host"]: s["worst_case_margin3"] for s in hosts_all}
    finite_worsts = {k: v for k, v in worsts.items() if v is not None}
    worst_host = (min(finite_worsts, key=finite_worsts.get)
                  if finite_worsts else None)
    out["worst_host"] = worst_host
    out["worst_host_margin"] = finite_worsts.get(worst_host)
    out["per_host_worst_margins"] = worsts
    profiles_ok = bool(
        len(s_h0["margin_profile"]["per_bin"]) == 4
        and len(s_h1["margin_profile"]["per_bin"]) == 4
        and all(len(h["margin_profile"]["per_bin"]) == 4
                for h in s_cor["hosts"].values()))
    h3 = bool(worst_host is not None
              and np.isfinite(finite_worsts[worst_host])
              and profiles_ok
              and len(hosts_all) == 12)

    # ---- GATE-H4 (hygiene) --------------------------------------------
    def _rows_fin(per: list) -> bool:
        return all(
            np.isfinite(p["quad"]) and np.isfinite(p["eV"])
            and np.isfinite(p["eT"])
            and all(np.isfinite(x) for x in p["decode_errs"]
                    if x is not None)
            and all(np.isfinite(x) for x in p["hold_errs"]
                    if x is not None)
            and (p["margin3"] is not None
                 and np.isfinite(p["margin3"])
                 if not p["rejected"] else True)
            for p in per)

    all_fin = bool(
        _rows_fin(s_h0["per_target"]) and _rows_fin(s_h1["per_target"])
        and all(_rows_fin(h["per_target"])
                for h in s_cor["hosts"].values()))
    lock_blocks = ([s_h0["lock_log"], s_h1["lock_log"]]
                   + [h["lock_log"] for h in s_cor["hosts"].values()])
    n_writes = sum(b["n_writes"] for b in lock_blocks)
    all_sstar = all(b["all_at_S_star"] for b in lock_blocks)
    wiring_const = all(b["wiring_id_constant"] for b in lock_blocks)
    h4 = bool(all_fin and all_sstar and wiring_const
              and n_writes == 12 * 100)
    h4_detail = (f"all channel errs finite={all_fin}; lock log "
                 f"{n_writes}/{12 * 100} (host, rung, wiring-id) "
                 f"triples, all at S*={all_sstar}, wiring-id "
                 f"constant per battery={wiring_const}")

    return {"H1": h1_gate, "H2": h2, "H3": h3, "H4": h4,
            "h2_detail": h2_detail, "h4_detail": h4_detail,
            "n_canon_asserts_h1_h11": n_canon,
            "per_host_bar": per_host_ok}


def _verdict_line(out: dict, gates: dict, np) -> str:
    if all(gates[g] for g in ("H1", "H2", "H3", "H4")):
        return (f"S* carries on ALL 12 hosts (>= 90/100 each, zero "
                f"rejections); worst host {out.get('worst_host')} at "
                f"{out.get('worst_host_margin')} vs exp182's "
                f"+5.404 on H0")
    bad = [g for g in ("H1", "H2", "H3", "H4") if not gates[g]]
    return f"gates REFUTED: {','.join(bad)}"


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
