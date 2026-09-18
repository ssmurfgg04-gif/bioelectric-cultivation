#!/usr/bin/env python3
"""exp235 — THE VMEM->TRANSCRIPTION GROUNDING (Cervera, Levin & Mafe 2026,
Scientific Reports 16(1996); the Section 6 item; ledger L211).

THE OPEN QUESTION: the stack's gene layer (M37, exp60/exp64) responds to
the voltage pattern, but the RESPONSE LAW was never grounded in the
biophysical mechanism. The Cervera 2026 mechanism: Vmem gates
transcription through voltage-sensitive membrane processes (voltage-gated
enzymes / Ca2+ entry alternating with the Nernst potential) — the
transcription factor activation is a THRESHOLD-RESTORED read of Vmem,
not a linear one: activation follows the fraction of time the local Vmem
spends beyond a gate voltage, with the Nernst alternation setting the
gate scale. The grounding test: does the M37 gene layer's response
follow the voltage-gated threshold law, and does the threshold restore
robustness the linear read lacks?

THE INSTRUMENT (zero-knob, from the mechanism): the activation of gene
g at cell i under the Cervera law: a_i,g = sigmoid((|V_i| - gate_g)/w_g)
evaluated on the time-averaged |V| over the write window (the
transcription integrates), with gate_g = the gene's Nernst-scale gate
(the gene layer's own frozen weight table from exp64's candidates — the
gates DERIVED from the layer's existing weights, no new fitting:
gate_g = the |theta| midpoint of the gene's recorded activation range,
w_g = the recorded range's quarter-width). The linear comparator: the
M37 layer's existing linear response (the frozen production read).

PRE-REGISTERED GATES:

  G1  THE THRESHOLD LAW: the Cervera-gated activation tracks the gene
      layer's measured response across the battery (the 3 arms x 5
      target classes x 3 seeds of exp225's target-class sweep machinery)
      with Spearman >= 0.85 — the biophysical mechanism reproduces the
      layer's response WITHOUT fitting.
  G2  THE THRESHOLD RESTORES ROBUSTNESS: under V-noise sigma in
      {2, 5, 10}, the gated read's zone-assignment accuracy degrades
      LESS than the linear read's at every sigma (the threshold's
      robustness margin; matched read: same layer, same genes, the only
      difference the gate).
  G3  THE NERNST ALTERNATION: the gate's dose-response follows the
      alternating pattern the mechanism predicts — activation vs |Vmem|
      is monotone WITHIN a gene but the gates ORDER the genes by their
      recorded ranges (Spearman(gate_g, range_g) >= 0.8 across the
      layer's genes): the layer's own structure carries the Nernst
      scale ordering.

THE BRANCH (pre-named): all three PASS -> GROUNDED (the gene layer's
response is the Cervera mechanism — the M37 layer gains its biophysical
reading); G1 REFUTE -> NOT-GROUNDED (the layer's response is NOT
voltage-gated-threshold — the linear read is the layer's true law and
the Cervera grounding is a scope mismatch, deposited honestly).

RUN: the sweep battery + the noise panel; serial, BLAS pinned; minutes.
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
OUT = os.path.join(ROOT, "results", "exp235_vmem_transcription.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    #      docstring byte-unchanged — exp174's body-only discipline;
    #      gates below evaluated exactly once) ============================
    import hashlib
    import time

    t0 = time.time()
    print("=== exp235: the Vmem->transcription grounding (Cervera 2026) ===\n")

    # ---- the frozen machinery, imported (never re-implemented) ----------
    from experiments.exp32_m26_repairs import WT_HEAD_V, WT_TAIL_V
    from experiments.exp60_gene_layer import FAMILY_PRIORITY
    from experiments.exp64_m37_candidates import REC as EXP64_REC
    from experiments.exp73_active_renormalization import make_battery, N
    from experiments.exp90_two_source_read import star_dt
    from experiments.exp94_multizone_scale import (
        MULTI, labeling_bfs_n, spec_target_n,
    )
    from experiments.exp136_generator_v6 import A_CHAIN, wildtype_target
    from experiments.exp140_state_space import spearman
    from experiments.exp142_sign_read import (
        SEEDS, STAR_OP, WINDOW_H, COMMIT_NOISE, STEPS_PER_CELL,
        NEURAL_SPEC_MIN as EXP142_FLOOR, execute_signed,
    )
    from experiments.exp172_deep_band_sweep import target_for as deep_target_for
    from cultivation.compiler.anatomy import AnatomySpec, Zone, compile_anatomy
    from cultivation.substrate.graph import GraphCollective
    import cultivation.bioelectric.collective as CORE

    # the production floor asserted at import (exp218's disclosed
    # exp169-import discipline): exp235 imports NO reader-line module,
    # so no restore is needed — the asserts prove the floors never moved.
    assert CORE.NEURAL_SPEC_MIN == -60.0, "production floor drifted"
    assert EXP142_FLOOR == -60.0, "exp142's captured floor drifted"

    ARMS = ("scale_free", "random3", "torus")   # exp79's plateau trio — the
    # stack's landed 3-arm battery convention (exp233/234/236), drawn from
    # exp73's make_battery.
    DEEP_RUNG = -60.0                       # the deep band's registered rung
    DEEP_INSTANCES = (0, 1)                 # both pre-named instances
    MANIFEST_INDICES = (0, 49, 99)          # the union's carried targets
    SIGMAS = (2.0, 5.0, 10.0)               # G2's pre-named V-noise ladder
    RECORD_EVERY = 10                       # exp73's frozen record stride
    G1_BAR = 0.85
    G3_BAR = 0.8

    battery = make_battery()

    # ---- the gene layer's frozen recorded tables (M37, exp60/exp64) -----
    dep60 = json.load(open(os.path.join(
        ROOT, "results", "exp60_gene_layer.json")))
    dep182 = json.load(open(os.path.join(
        ROOT, "results", "exp182_substrate_100.json")))
    _manifest = sorted(dep182["manifest"]["targets"],
                       key=lambda m: m["index"])
    assert len(_manifest) == 100

    # THE GENES: the M37 layer's own vocabulary — exp60's functional
    # families (GL-G1's exhaustive taxonomy: every RNAi name lands in
    # exactly one). exp64's weight table (REC, the adopted M37-A record)
    # is deposited as the layer's recorded-response anchor.
    GENES = list(FAMILY_PRIORITY)

    # THE RECORDED ACTIVATION RANGES (|theta| units, zero fitting): each
    # gene's range = the span of canon identity values over the planes its
    # experiments were recorded on (exp60's frozen plane_table), mapped by
    # the layer's own recorded identity constants — head -> |WT_HEAD_V|,
    # tail/trunk -> |WT_TAIL_V| (= the canon trunk identity TRUNK_V);
    # planes with no single canon identity (none/graft/irr/lateral/
    # crosspiece) record the intact whole-animal axis [20, 50].
    HEAD_ABS, TAIL_ABS = abs(WT_HEAD_V), abs(WT_TAIL_V)
    AXIS = (HEAD_ABS, TAIL_ABS)
    PLANE_BAND = {"head": (HEAD_ABS, HEAD_ABS),
                  "tail": (TAIL_ABS, TAIL_ABS),
                  "trunk": (TAIL_ABS, TAIL_ABS)}
    plane_tab = dep60["plane_table"]
    gate_table = {}
    for g in GENES:
        planes = sorted({k.split("|", 1)[1] for k in plane_tab
                         if k.split("|", 1)[0] == g})
        assert planes, f"{g}: no recorded planes in exp60's plane_table"
        los, his = [], []
        for p in planes:
            lo, hi = PLANE_BAND.get(p, AXIS)
            los.append(lo)
            his.append(hi)
        lo, hi = float(min(los)), float(max(his))
        gate_table[g] = {"planes": planes, "lo": lo, "hi": hi,
                         "gate": 0.5 * (lo + hi),        # the |theta| midpoint
                         "width": hi - lo,
                         "w": (hi - lo) / 4.0}           # the quarter-width
    gates_v = [gate_table[g]["gate"] for g in GENES]
    widths_v = [gate_table[g]["width"] for g in GENES]
    print("  the gene layer's recorded gate table (zero-knob derivation):")
    for g in GENES:
        t = gate_table[g]
        print(f"    {g:10s} planes={','.join(t['planes'])} -> range "
              f"[{t['lo']:g},{t['hi']:g}] gate={t['gate']:g} "
              f"w={t['w']:g}")

    # ---- target-class provenance (exp225's sweep machinery, asserted) ---
    line_canon = labeling_bfs_n(A_CHAIN)
    assert np.array_equal(line_canon, wildtype_target(100)), "canon drift"
    for m in _manifest:
        if m["index"] not in MANIFEST_INDICES:
            continue
        triples = [tuple(float(x) for x in z) for z in m["triples"]]
        spec = AnatomySpec(
            zones=[Zone(f0=s_, f1=e_, voltage=v, name=f"z{j}")
                   for j, (s_, e_, v) in enumerate(triples)],
            amputate_plane=MULTI.amputate_plane,
            spec_name=f"exp182-t{m['index']:03d}",
            somatic_latch=MULTI.somatic_latch)
        f = spec_target_n(spec, line_canon, 100)
        sha = hashlib.sha256(
            np.ascontiguousarray(f, dtype=np.float64).tobytes()).hexdigest()
        assert sha == m["f_sha256"], \
            f"manifest m{m['index']} rebuild drift vs exp182's deposit"
    for inst in DEEP_INSTANCES:
        f_ref, _tri, _ref = deep_target_for(DEEP_RUNG, inst)
        zs = [(z.f0 + inst / 100.0, z.f1 + inst / 100.0, DEEP_RUNG)
              for z in MULTI.zones]
        spec = AnatomySpec(
            zones=[Zone(f0=a, f1=b, voltage=DEEP_RUNG, name=nm)
                   for (a, b, nm) in zs],
            amputate_plane=MULTI.amputate_plane,
            spec_name=f"ms-multi-deep-i{inst}",
            somatic_latch=MULTI.somatic_latch)
        assert np.array_equal(spec_target_n(spec, line_canon, 100), f_ref), \
            f"deep {DEEP_RUNG:g} i{inst} rebuild drift vs exp172's build"
    print(f"  target classes: canon + manifest {MANIFEST_INDICES} + deep "
          f"{DEEP_RUNG:g} (both instances) — exp225's construction, "
          f"checksummed on the line canon")

    def build_rows(canon: np.ndarray, n: int) -> list:
        """exp225's target-class rows on THIS arm's own canon (exp142's R1
        canon rule: labeling_bfs_n(|A|)) — 5 pre-named classes, 6 decode
        rows (the deep class carries both instances, exp225's counting)."""
        rows = []
        spec_c = AnatomySpec(zones=[], amputate_plane=None,
                             spec_name="exp235-arm-canon",
                             somatic_latch=False)
        f_c = spec_target_n(spec_c, canon, n)
        assert np.array_equal(f_c, canon), "canon row target != canon"
        rows.append({"tclass": "canon", "key": "canon", "spec": spec_c,
                     "f": f_c})
        for m in _manifest:
            if m["index"] not in MANIFEST_INDICES:
                continue
            triples = [tuple(float(x) for x in z) for z in m["triples"]]
            spec = AnatomySpec(
                zones=[Zone(f0=s_, f1=e_, voltage=v, name=f"z{j}")
                       for j, (s_, e_, v) in enumerate(triples)],
                amputate_plane=MULTI.amputate_plane,
                spec_name=f"exp182-t{m['index']:03d}",
                somatic_latch=MULTI.somatic_latch)
            rows.append({"tclass": "manifest", "key": f"m{m['index']}",
                         "spec": spec, "f": spec_target_n(spec, canon, n)})
        for inst in DEEP_INSTANCES:
            zs = [(z.f0 + inst / 100.0, z.f1 + inst / 100.0, DEEP_RUNG)
                  for z in MULTI.zones]
            spec = AnatomySpec(
                zones=[Zone(f0=a, f1=b, voltage=DEEP_RUNG, name=nm)
                       for (a, b, nm) in zs],
                amputate_plane=MULTI.amputate_plane,
                spec_name=f"ms-multi-deep-i{inst}",
                somatic_latch=MULTI.somatic_latch)
            rows.append({"tclass": "deep", "key": f"r{DEEP_RUNG:g}i{inst}",
                         "spec": spec,
                         "f": spec_target_n(spec, canon, n)})
        assert len(rows) == 6, "row build drifted"
        return rows

    # ---- the write: exp142's execute_signed with the window RECORDED ----
    def recorded_write(spec: AnatomySpec, adjacency: np.ndarray,
                       seed: int) -> dict:
        """exp142's execute_signed, call-for-call verbatim (R1 structure on
        |A| via star_dt/labeling_bfs_n; R2 signed dynamics; the exp97 walk
        at STEPS_PER_CELL, commit noise COMMIT_NOISE), with ONE addition:
        the write window is RECORDED (record_every=10, exp73's frozen
        record stride). Recording consumes no rng draws, so the trajectory
        is bit-identical to execute_signed's — asserted per instance below
        (the machinery-drift guard; execute_signed exposes no record)."""
        n = adjacency.shape[0]
        gamma, mu = STAR_OP["gamma"], STAR_OP["mu"]
        absA = np.abs(adjacency)
        dt = star_dt(gamma, float(absA.sum(axis=1).max()))       # R1
        canon = labeling_bfs_n(absA)                             # R1
        target = spec_target_n(spec, canon, n)
        c = GraphCollective(adjacency=adjacency, seed=seed,
                            gamma=gamma, mu_theta=mu)            # R2
        c.set_target(canon)
        c.write_spec_layer(target)
        prog = compile_anatomy(spec, n=n)
        if prog.rejected:
            return {"rejected": True, "rejection": prog.rejected}
        for cl in prog.clamps:
            c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
        rec = c.run(WINDOW_H, dt=dt, record_every=RECORD_EVERY)  # the window
        vbar = np.mean(np.abs(rec), axis=0)
        c.release_clamps()
        reg_idx: list[int] = []
        for z in spec.zones:
            i0 = int(round(z.f0 * n))
            i1 = max(int(round(z.f1 * n)), i0 + 1)
            reg_idx.extend(range(i0, i1))
        reg_idx = sorted(set(reg_idx))
        if reg_idx:
            reg_walk = list(range(reg_idx[0], reg_idx[-1] + 1))
            region_set = set(reg_walk)
            c.amputate(slice(reg_idx[0], reg_idx[-1] + 1))
            wound_center = float(np.mean(c.theta[reg_walk]))
            parent_of: dict[int, int] = {}
            frontier: list[int] = []
            for i in reg_walk:
                nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                        if j not in region_set]
                if nbrs:
                    parent_of[i] = int(max(
                        nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
                    frontier.append(i)
            if not frontier:
                frontier = reg_idx[:1]
                parent_of[frontier[0]] = frontier[0]
            visited = set(frontier)
            order = [(i, parent_of[i]) for i in frontier]
            queue = list(frontier)
            while queue:
                i = queue.pop(0)
                for j in np.where(np.abs(c.A[i]) > 0)[0]:
                    if int(j) in region_set and int(j) not in visited:
                        visited.add(int(j))
                        parent_of[int(j)] = int(i)
                        order.append((int(j), int(i)))
                        queue.append(int(j))
            for i, src in order:
                for _ in range(STEPS_PER_CELL):
                    c.step(dt)
                canon_src = getattr(c, "phi_spec_canon", None)
                if c.phi_spec[i] >= EXP142_FLOOR:
                    theta_new = c.phi_spec[i] + c.rng.normal(0.0,
                                                             COMMIT_NOISE)
                elif canon_src is not None:
                    theta_new = canon_src[i] + c.rng.normal(0.0,
                                                            COMMIT_NOISE)
                else:
                    theta_new = c.theta[src] + c.rng.normal(0.0,
                                                            COMMIT_NOISE)
                c.theta[i] = theta_new
                c.V[i] = theta_new
        c.run(15.0, dt=dt)
        err = float(c.pattern_error(target))
        return {"rejected": False, "dt": float(dt), "canon": canon,
                "target": target, "vbar": vbar,
                "theta": c.theta.copy(), "V": c.V.copy(), "err": err}

    # ---- the two reads (same layer, same genes; only the gate differs) --
    def cervera_gated(vbar: np.ndarray, gate: float,
                      w: float) -> np.ndarray:
        """THE CERVERA LAW, zero-knob, per the docstring's definition:
        a_i,g = sigmoid((|V_i| - gate_g)/w_g) on the time-averaged |V|
        over the write window (the transcription integrates). A
        zero-width recorded range is the gate's step limit (w -> 0)."""
        if w > 0.0:
            return 1.0 / (1.0 + np.exp(-(vbar - gate) / w))
        return np.where(vbar > gate, 1.0,
                        np.where(vbar < gate, 0.0, 0.5))

    def linear_response(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
        """THE LINEAR COMPARATOR: the M37 layer's existing linear response
        — the linear position of the read value within the gene's recorded
        activation range (the frozen production read, no gate)."""
        if hi > lo:
            return np.clip((x - lo) / (hi - lo), 0.0, 1.0)
        return np.where(x > lo, 1.0, np.where(x < lo, 0.0, 0.5))

    def _sign_read(field: np.ndarray) -> np.ndarray:
        """The threshold sign read — exp142's sign semantics: the zone bit
        is the SIGN of (field - midline), the midline the field's OWN
        two-cluster midpoint (deterministic 2-means, zero knobs, RELATIVE
        hence offset-covariant). exp234's landed _sign_read is a main()
        closure and exp142 exposes no field-level read, so the LANDED form
        is mirrored VERBATIM line-for-line here (disclosed; no frozen file
        touched — the body-only discipline)."""
        c1, c2 = float(field.min()), float(field.max())
        if not c2 > c1:
            return np.zeros(field.shape, dtype=bool)
        for _ in range(200):
            mid = 0.5 * (c1 + c2)
            lo = field <= mid
            if not lo.any() or lo.all():
                break
            n1 = float(field[lo].mean())
            n2 = float(field[~lo].mean())
            if n1 == c1 and n2 == c2:
                break
            c1, c2 = n1, n2
        return field > 0.5 * (c1 + c2)

    # ---- the battery: 3 arms x 5 target classes (6 rows) x 3 seeds ------
    print(f"\n  running the battery: {len(ARMS)} arms x 6 rows x "
          f"{len(SEEDS)} seeds = {len(ARMS) * 6 * len(SEEDS)} instances "
          f"(each guarded bit-exact against exp142's execute_signed) ...")
    inst_rows: list[dict] = []
    pooled_gated: list[float] = []
    pooled_meas: list[float] = []
    per_gene: dict[str, dict[str, list]] = {g: {"ag": [], "m": [], "vbar": []}
                                            for g in GENES}
    n_rejections = 0
    n_guard_ok = 0
    n_instances = 0
    for gi, arm in enumerate(ARMS):
        A = battery[arm]
        rows = build_rows(labeling_bfs_n(np.abs(A)), N)
        for ri, row in enumerate(rows):
            row_errs: list[float] = []
            row_ag0: list[float] = []
            row_al0: list[float] = []
            row_guard: list[bool] = []
            for s in SEEDS:
                w = recorded_write(row["spec"], A, int(s))
                if w.get("rejected"):
                    n_rejections += 1
                    inst_rows.append({"arm": arm, "tclass": row["tclass"],
                                      "key": row["key"], "seed": int(s),
                                      "rejected": True})
                    print(f"    [{arm} {row['tclass']} {row['key']} s{s}] "
                          f"REJECTED (recorded honestly)")
                    continue
                ref = execute_signed(row["spec"], A, int(s), op=STAR_OP,
                                     return_state=True)
                if "final_state" not in ref:
                    n_rejections += 1
                    inst_rows.append({"arm": arm, "tclass": row["tclass"],
                                      "key": row["key"], "seed": int(s),
                                      "rejected": True,
                                      "where": "guard arm"})
                    continue
                guard = bool(
                    np.array_equal(w["V"], np.asarray(
                        ref["final_state"]["V"]))
                    and round(w["err"], 2) == float(ref["err_vs_target"]))
                n_guard_ok += int(guard)
                n_instances += 1
                row_errs.append(w["err"])
                vbar = w["vbar"]
                theta_abs = np.abs(w["theta"])
                a_g = np.stack([cervera_gated(vbar, gate_table[g]["gate"],
                                              gate_table[g]["w"])
                                for g in GENES])
                a_lin = np.stack([linear_response(vbar, gate_table[g]["lo"],
                                                  gate_table[g]["hi"])
                                  for g in GENES])
                m_resp = np.stack([linear_response(theta_abs,
                                                   gate_table[g]["lo"],
                                                   gate_table[g]["hi"])
                                   for g in GENES])
                # the zone ground truth: the target's own |identity|-axis
                # zone structure (the same threshold sign read, on the axis
                # both reads consume)
                z_star = _sign_read(np.abs(w["target"]))
                z_g0 = _sign_read(a_g.mean(axis=0))
                z_l0 = _sign_read(a_lin.mean(axis=0))
                # G2's V-noise: read-time Gaussian on the window-averaged
                # |V| (the sustained-noise convention, exp233's disclosure
                # precedent), deterministic per instance
                rng = np.random.default_rng([gi, ri, int(s)])
                acc_g_sig: dict[str, float] = {}
                acc_l_sig: dict[str, float] = {}
                for sigma in SIGMAS:
                    vb = vbar + sigma * rng.standard_normal(N)
                    ag = np.stack([cervera_gated(vb, gate_table[g]["gate"],
                                                 gate_table[g]["w"])
                                   for g in GENES])
                    al = np.stack([linear_response(vb, gate_table[g]["lo"],
                                                   gate_table[g]["hi"])
                                   for g in GENES])
                    acc_g_sig[str(sigma)] = float(np.mean(
                        _sign_read(ag.mean(axis=0)) == z_star))
                    acc_l_sig[str(sigma)] = float(np.mean(
                        _sign_read(al.mean(axis=0)) == z_star))
                row_ag0.append(float(np.mean(z_g0 == z_star)))
                row_al0.append(float(np.mean(z_l0 == z_star)))
                row_guard.append(guard)
                pooled_gated.extend(a_g.ravel().tolist())
                pooled_meas.extend(m_resp.ravel().tolist())
                for k, g in enumerate(GENES):
                    per_gene[g]["ag"].extend(a_g[k].tolist())
                    per_gene[g]["m"].extend(m_resp[k].tolist())
                    per_gene[g]["vbar"].extend(vbar.tolist())
                inst_rows.append({
                    "arm": arm, "tclass": row["tclass"], "key": row["key"],
                    "seed": int(s), "dt": w["dt"],
                    "err": round(w["err"], 3),
                    "guard_bit_exact": guard,
                    "vbar_mean": round(float(np.mean(vbar)), 4),
                    "theta_abs_mean": round(float(np.mean(theta_abs)), 4),
                    "acc_gated_0": float(np.mean(z_g0 == z_star)),
                    "acc_lin_0": float(np.mean(z_l0 == z_star)),
                    "acc_gated_sigma": acc_g_sig,
                    "acc_lin_sigma": acc_l_sig,
                    "rho_instance": round(float(
                        spearman(a_g.ravel().tolist(),
                                 m_resp.ravel().tolist())), 6),
                })
            print(f"    [{arm} {row['tclass']} {row['key']}] seeds "
                  f"{[int(x) for x in SEEDS]}: err mean "
                  f"{float(np.mean(row_errs)) if row_errs else float('nan'):.2f} "
                  f"acc0 gated/lin "
                  f"{float(np.mean(row_ag0)) if row_ag0 else float('nan'):.3f}/"
                  f"{float(np.mean(row_al0)) if row_al0 else float('nan'):.3f} "
                  f"guard {'OK' if row_guard and all(row_guard) else 'DRIFT/REJ'}")

    assert n_instances + n_rejections == len(ARMS) * 6 * len(SEEDS), \
        "instance count drifted"
    print(f"\n  battery complete: {n_instances} instances, "
          f"{n_rejections} rejections, machinery-drift guard "
          f"{n_guard_ok}/{n_instances} bit-exact")

    # ---- G1: THE THRESHOLD LAW ------------------------------------------
    rho_pooled = float(spearman(pooled_gated, pooled_meas))
    g1 = bool(np.isfinite(rho_pooled) and rho_pooled >= G1_BAR)
    rho_by_gene = {g: round(float(spearman(per_gene[g]["ag"],
                                           per_gene[g]["m"])), 6)
                   for g in GENES}
    # per-class mean instance rho (from the deposited per-instance values)
    rho_by_class = {
        tc: round(float(np.mean([r["rho_instance"] for r in inst_rows
                                 if not r.get("rejected")
                                 and r["tclass"] == tc])), 6)
        for tc in ("canon", "manifest", "deep")}
    print(f"\n  G1 the threshold law: pooled Spearman(gated, measured) over "
          f"{len(pooled_gated)} (instance, gene, cell) triples = "
          f"{rho_pooled:.4f} (bar {G1_BAR}) -> "
          f"{'PASS' if g1 else 'REFUTE'}")
    print(f"    per-gene pooled rho: {rho_by_gene}")
    print(f"    per-class mean instance rho: {rho_by_class}")

    # ---- G2: THE THRESHOLD RESTORES ROBUSTNESS ---------------------------
    acc_g0 = float(np.mean([r["acc_gated_0"] for r in inst_rows
                            if not r.get("rejected")]))
    acc_l0 = float(np.mean([r["acc_lin_0"] for r in inst_rows
                            if not r.get("rejected")]))
    drop_g: dict[str, float] = {}
    drop_l: dict[str, float] = {}
    g2 = True
    for sigma in SIGMAS:
        k = str(sigma)
        ag = float(np.mean([r["acc_gated_sigma"][k] for r in inst_rows
                            if not r.get("rejected")]))
        al = float(np.mean([r["acc_lin_sigma"][k] for r in inst_rows
                            if not r.get("rejected")]))
        drop_g[k] = acc_g0 - ag
        drop_l[k] = acc_l0 - al
        ok = bool(drop_g[k] < drop_l[k])
        g2 &= ok
        print(f"  G2 sigma={sigma:g}: gated acc {ag:.4f} (drop "
              f"{drop_g[k]:+.4f}) vs linear acc {al:.4f} (drop "
              f"{drop_l[k]:+.4f}) -> degrades-less "
              f"{'YES' if ok else 'NO'}")
    print(f"  G2 the threshold restores robustness (baseline acc "
          f"gated {acc_g0:.4f} / linear {acc_l0:.4f}; strict-less drops at "
          f"EVERY sigma) -> {'PASS' if g2 else 'REFUTE'}")

    # ---- G3: THE NERNST ALTERNATION --------------------------------------
    mono = {}
    for g in GENES:
        vb = np.asarray(per_gene[g]["vbar"])
        ag = np.asarray(per_gene[g]["ag"])
        order = np.argsort(vb, kind="stable")
        mono[g] = bool(np.all(np.diff(ag[order]) >= -1e-12))
    rho_gates = float(spearman(gates_v, widths_v))
    g3a = all(mono.values())
    g3b = bool(np.isfinite(rho_gates) and rho_gates >= G3_BAR)
    g3 = bool(g3a and g3b)
    print(f"\n  G3 the Nernst alternation:")
    print(f"    (a) activation vs |V| monotone within every gene: {mono} "
          f"-> {'PASS' if g3a else 'REFUTE'}")
    print(f"    (b) Spearman(gate_g, range_g) across the layer's "
          f"{len(GENES)} genes = {rho_gates:.4f} (bar {G3_BAR}) -> "
          f"{'PASS' if g3b else 'REFUTE'}"
          f" (tie structure: {sum(1 for w in widths_v if w > 0)}/"
          f"{len(GENES)} genes carry a non-degenerate recorded range)")
    print(f"  G3 -> {'PASS' if g3 else 'REFUTE'}")

    # ---- the pre-named branch --------------------------------------------
    npass = int(g1) + int(g2) + int(g3)
    branch = "GROUNDED" if npass == 3 else "NOT-GROUNDED"
    print(f"\n  === G1 {'PASS' if g1 else 'REFUTE'} | G2 "
          f"{'PASS' if g2 else 'REFUTE'} | G3 {'PASS' if g3 else 'REFUTE'} "
          f"({npass}/3) -> branch {branch} ===")

    deposit = {
        "exp": "exp235_vmem_transcription",
        "claim": ("THE VMEM->TRANSCRIPTION GROUNDING (Cervera, Levin & "
                  "Mafe 2026): is the M37 gene layer's response the "
                  "voltage-gated threshold law — a_i,g = "
                  "sigmoid((|V|-gate_g)/w_g) on the window-averaged |V|, "
                  "gates derived zero-knob from the layer's own recorded "
                  "activation ranges — and does the threshold restore the "
                  "robustness the linear read lacks?"),
        "instrument": {
            "genes": GENES,
            "gene_layer_source": ("exp60's FAMILY_PRIORITY vocabulary + "
                                  "exp60's frozen plane_table; exp64's "
                                  "REC (the adopted M37-A record) "
                                  "deposited as the recorded-response "
                                  "anchor"),
            "exp64_weight_table_anchor": {k: float(v)
                                          for k, v in EXP64_REC.items()},
            "recorded_gate_table": {
                g: {"planes": gate_table[g]["planes"],
                    "range_mV": [gate_table[g]["lo"], gate_table[g]["hi"]],
                    "gate": gate_table[g]["gate"], "w": gate_table[g]["w"]}
                for g in GENES},
            "gate_derivation": ("gate_g = the |theta| midpoint of the "
                                "gene's recorded activation range; w_g = "
                                "the range's quarter-width; ranges from "
                                "exp60's frozen plane_table mapped by the "
                                "layer's own identity constants (head -> "
                                "|WT_HEAD_V|=20, tail/trunk -> "
                                "|WT_TAIL_V|=50; none/graft/irr/lateral/"
                                "crosspiece -> the intact axis [20,50]) — "
                                "no new fitting"),
            "battery": ("exp73's make_battery, exp79's plateau trio "
                        "(scale_free, random3, torus) x exp225's 5 target "
                        "classes (canon + manifest 0/49/99 + the deep "
                        "-60.0 rung both instances = 6 rows) x exp142's "
                        "SEEDS (1,2,3)"),
            "write": ("exp142's execute_signed semantics (R1 structure on "
                      "|A|, R2 signed dynamics, exp97 walk, window 24 h, "
                      "commit noise 0.6, op STAR_OP=(64,0)) with the "
                      "write window recorded (record_every=10, exp73's "
                      "frozen stride); the recorded twin asserted "
                      "bit-identical to execute_signed per instance "
                      "(final V + err)"),
            "gated_read": ("a_i,g = sigmoid((|V_i|-gate_g)/w_g) on the "
                           "time-averaged |V| over the write window; "
                           "zero-width ranges take the step limit"),
            "linear_comparator": ("the same recorded-range linear ramp — "
                                  "the M37 layer's existing linear "
                                  "response; same layer, same genes, the "
                                  "only difference the gate"),
            "measured_response": ("the layer's committed identity "
                                  "|theta_final| scored linearly on the "
                                  "gene's recorded range (the frozen "
                                  "production read)"),
            "zone_assignment": ("the threshold sign read (exp142's sign "
                                "semantics: the bit is the sign of "
                                "(field - the field's OWN 2-cluster "
                                "midline); exp234's landed closure "
                                "mirrored verbatim, disclosed); the zone "
                                "ground truth = the sign read of the "
                                "target's |identity| field"),
            "noise_protocol": ("G2's V-noise is read-time Gaussian on the "
                               "window-averaged |V| (sustained-noise "
                               "convention, exp233's disclosure "
                               "precedent), sigma in the pre-named "
                               "{2,5,10}, deterministic per instance "
                               "(default_rng([gi, ri, seed]))"),
            "floor": ("production NEURAL_SPEC_MIN=-60.0 asserted at "
                      "import on collective and exp142's captured value "
                      "(exp218's discipline; no reader-line module "
                      "imported, no restore needed)"),
            "instances": n_instances, "rejections": n_rejections,
            "guard_bit_exact": n_guard_ok,
        },
        "gates": {
            "G1_threshold_law": {
                "pass": g1, "bar": G1_BAR,
                "pooled_spearman": (round(rho_pooled, 6)
                                    if np.isfinite(rho_pooled) else None),
                "n_triples": len(pooled_gated),
                "per_gene_spearman": rho_by_gene,
                "per_class_mean_instance_spearman": rho_by_class,
            },
            "G2_threshold_restores_robustness": {
                "pass": g2, "sigmas": list(SIGMAS),
                "acc_gated_0": round(acc_g0, 6),
                "acc_lin_0": round(acc_l0, 6),
                "drop_gated": {k: round(v, 6) for k, v in drop_g.items()},
                "drop_linear": {k: round(v, 6) for k, v in drop_l.items()},
                "rule": ("the gated read's zone-assignment accuracy drop "
                         "strictly less than the linear read's at every "
                         "sigma (pooled over the battery)"),
            },
            "G3_nernst_alternation": {
                "pass": g3, "bar": G3_BAR,
                "within_gene_monotone": mono,
                "spearman_gate_vs_range": (round(rho_gates, 6)
                                           if np.isfinite(rho_gates)
                                           else None),
                "gate_order": {g: gate_table[g]["gate"] for g in GENES},
                "range_width": {g: gate_table[g]["width"] for g in GENES},
            },
        },
        "instances": inst_rows,
        "criteria": {
            "G1_threshold_law": g1,
            "G2_threshold_restores_robustness": g2,
            "G3_nernst_alternation": g3,
        },
        "branch": branch,
        "verdict": (f"{npass}/3 gates PASS (G1 {'PASS' if g1 else 'REFUTE'}, "
                    f"G2 {'PASS' if g2 else 'REFUTE'}, G3 "
                    f"{'PASS' if g3 else 'REFUTE'}) -> {branch} "
                    f"(the pre-named branches: all three PASS -> "
                    f"GROUNDED; otherwise NOT-GROUNDED)"),
        "runtime_s": round(time.time() - t0, 1),
        "notes": (
            "Operationalization disclosures (docstring byte-unchanged, "
            "verified against pre-registration 2132308): (1) the layer's "
            "genes = exp60's functional families (the GL-G1 vocabulary — "
            "the layer's recorded unit of response); (2) the recorded "
            "activation ranges are derived zero-knob from exp60's frozen "
            "plane_table and the layer's own identity constants (WT_HEAD_V/"
            "WT_TAIL_V via exp32; the trunk canon = WT_TAIL_V = the "
            "stack's TRUNK_V) — planes without a single canon identity "
            "record the intact axis [20,50], so 5/6 genes share the "
            "full-axis range and wnt_ant (recorded on the head plane "
            "alone) carries the degenerate [20,20] range -> the step-"
            "limit gate; the G3(b) Spearman is therefore tie-structured "
            "and weak-powered at 6 genes, recorded honestly; (3) the "
            "write is exp142's execute_signed mirrored call-for-call with "
            "the window recorded — recording consumes no rng, and the "
            "twin is asserted bit-identical (final V + err) against "
            "execute_signed itself on every instance; (4) the zone "
            "assignment is the threshold sign read of exp142's sign "
            "semantics — exp234's landed _sign_read is a main()-closure "
            "and exp142 exposes no field-level read, so the landed form "
            "is mirrored verbatim (no frozen file touched); (5) the "
            "measured response (G1) is the layer's committed identity "
            "|theta_final| scored linearly on the gene's recorded range, "
            "while the linear comparator (G2's matched read) is the same "
            "ramp applied to the same window-averaged |V| the gated read "
            "consumes — same layer, same genes, the only difference the "
            "gate; (6) G2's drops are strict-less as pre-named ('degrades "
            "LESS'): a tie (both reads degrade equally, incl. zero) is a "
            "REFUTE; (7) the 3 arms are exp79's plateau trio drawn from "
            "exp73's make_battery (the stack's landed 3-arm convention, "
            "exp233/234/236)."),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(deposit, f, indent=1)
    print(f"\n  results -> {OUT}")
    return deposit


if __name__ == "__main__":
    main()
