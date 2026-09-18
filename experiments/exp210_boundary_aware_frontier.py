#!/usr/bin/env python3
"""exp210 — THE COMPOSED BOUNDARY-AWARE FRONTIER RULE (L178's
registered next).

exp205's pricing: the plane-resolved face halves the boundary residual
(21-48% improvements at exactly the localized site) yet 0/3 cross the
bar; exp155's discipline fails AT the boundary ("cannot exclude the
boundary cell without excluding the boundary itself", L140's exact
words). The registered composition: the two complementary mechanisms
at the one site both can see — the JD-a membership face gains a
BOUNDARY-AWARE exception (the fence yields exactly at canon-boundary
cells) and the boundary cells' read face is plane-resolved
(exp158's machinery, exp205's armed face). One composed rule, zero
knobs, aimed at the 3 breaking F3 ring-1 events.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp205's replay machinery
verbatim (the full-capture floor pin, the 141-row anchor, the 69-row
ring-event table); the composed rule (pre-registered here, zero
knobs): JD-a' = the flip-quiet reach F_q of exp155's JD-a, EXCEPT
that a node whose only committed-adjacency is a flip edge AND which
sits on a canon-value boundary in the target is ADMITTED to the
frontier with the plane-resolved read face (exp158's machinery)
instead of exclusion; everything else exp155's protocol verbatim.

GATES (each evaluated exactly once):
  GATE-F1 (anchor) exp205's replay reproduces (141/141 ring rows;
           the 3 boundary events at their disciplined errs).
  GATE-F2 (the composition) the composed rule at F3 ring-1: per-event
           errs for all 3 seeds; the branch named: REPAIR (all 3 <
           6.0), PARTIAL (>= 1 < 6.0 and none worse than the
           disciplined baseline), NONE.
  GATE-F3 (no-regression) every passing ring's err bit-exact vs the
           replay outside the F3 ring-1 site (the identity clause;
           the composed rule touches only the boundary site).
  GATE-F4 (hygiene) zero rejections; all finite; the pin
           save/restore asserted.
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp210_boundary_aware_frontier.json
RUN: python3 -m experiments.exp210_boundary_aware_frontier [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp210_boundary_aware_frontier.json")


def main() -> dict:
    # ==== BODY (written by the run agent under the two-death rule;
    # docstring/imports/constants above byte-unchanged — exp174's
    # body-only discipline) ============================================
    import time
    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    import hashlib

    import numpy as np

    from cultivation.bioelectric import collective as CORE
    from experiments import exp136_generator_v6 as M136
    from experiments import exp156_write_path as M156
    from experiments import exp148_temporal_read as M148
    from experiments import exp142_sign_read as M142
    from experiments import exp155_junction_flip as E155
    from experiments.exp94_multizone_scale import labeling_bfs_n

    OLD_FLOOR = -35.0
    PIN_MODS = [m for m in (CORE, M136, M156, M148, M142)
                if hasattr(m, "NEURAL_SPEC_MIN")]

    FLOORS_ORIGINAL = [m.NEURAL_SPEC_MIN for m in PIN_MODS]

    def old_floor_pin():
        """exp200's full-capture pin VERBATIM (exp168's B2 mechanism,
        extended to the read-chain modules that captured the constant
        at import time). Save/pin, exact-restore asserted by the
        caller."""
        saved = [m.NEURAL_SPEC_MIN for m in PIN_MODS]
        for m in PIN_MODS:
            m.NEURAL_SPEC_MIN = OLD_FLOOR
        return saved

    def restore_floors(saved):
        for m, v in zip(PIN_MODS, saved):
            m.NEURAL_SPEC_MIN = v
        assert all(m.NEURAL_SPEC_MIN == v
                   for m, v in zip(PIN_MODS, saved)), \
            "floor restore failed"

    DEP155 = os.path.join(ROOT, "results", "exp155_junction_flip.json")
    DEP200 = os.path.join(ROOT, "results",
                          "exp200_canon_boundary_grouping.json")
    ERR_BAR = E155.ERR_BAR
    FAMS = ("F1_zone_tail", "F3_canon_boundary")
    VARS = ("per", "aper")
    ERR_MARGIN = 6.0                     # exp151/152's cell bar

    dep155 = json.load(open(DEP155))
    dep200 = json.load(open(DEP200))

    def ring_table(payload: dict, section: str) -> list:
        # exp200's ring_table VERBATIM
        rows = []
        for fam in FAMS:
            sec = payload[section][fam]
            for var in VARS:
                for run in sec["members"][var]["runs"]:
                    for r in run["rings"]:
                        rows.append({
                            "section": section, "family": fam,
                            "variant": var, "seed": run["seed"],
                            "ring_index": r["ring_index"],
                            "frontier": list(r["frontier"]),
                            "n_frontier": len(r["frontier"]),
                            "ring_err_mV": r.get("ring_err_mV"),
                            "pass": bool(r.get("pass"))})
        return rows

    # ==================================================================
    # THE PLANE-RESOLVED FACE (exp158's machinery, zero knobs).  The
    # canon planes are the construction's OWN labeling (exp148
    # chord_set's canon: labeling_bfs_n on the ring substrate, head =
    # canon >= the pinned NEURAL_SPEC_MIN) — the same labeling that
    # BUILT the F3_canon_boundary family, not a new object.  The face
    # reads the window PLANE-RESOLVED: each canon plane's induced
    # sub-window is a WindowQuietMedium (E155's class verbatim, mask
    # restricted to the plane's nodes) decoded by the verbatim
    # TC1/TC2/TC3 chain (PN projection -> flip clock -> A_ext ->
    # execute_signed), and the frontier emission is stitched per plane
    # (each frontier node emitted by its OWN plane's read; the pooled
    # RMS err convention unchanged).  The boundary-plane cells — window
    # cells whose endpoints sit on different canon planes — have no
    # plane home and enter NO plane's decode: the read that sees the
    # boundary.  Arm scope: the exact site the exp200 localization
    # named — (F3_canon_boundary, member per, ring 1) — the 3 boundary
    # events; GATE-F3's identity clause (every passing ring bit-exact,
    # including the passing aper ring-1 reads at the same window)
    # binds the arm to exactly those events.
    # ==================================================================
    def plane_of_map(W: np.ndarray) -> dict:
        canon = labeling_bfs_n(W)
        return {j: ("head" if canon[j] >= OLD_FLOOR else "tail")
                for j in range(W.shape[0])}

    def plane_resolved_read(member, win: set, crossing: list, s: int,
                            plane_of: dict, planes=("head", "tail"),
                            sweep: bool = False):
        """THE FACE. Returns (V_stitched, meta). meta carries per-plane
        geometry, flip-clock occupancy, program flags and the belt-and-
        braces window sweep (first seed only)."""
        n = member.A.shape[0]
        V = np.zeros(n)
        meta = {"planes": {}, "sweep_ok": None}
        outs = []
        for p in planes:
            pw = sorted(j for j in win if plane_of[j] == p)
            pcross = [(i, j) for (i, j) in crossing
                      if i in pw and j in pw]
            wm = E155.WindowQuietMedium(member, pw, pcross)
            if sweep:
                sw = wm.sweep_assert()
                assert sw["ok"], f"plane window sweep failed ({p})"
                if meta["sweep_ok"] is None:
                    meta["sweep_ok"] = True
            with E155.warnings_as_errors():
                A0 = E155.project_phase_native(wm)[0]
            Fc = E155.flip_clock_matrix(wm)
            A_ext = A0 + Fc                    # TC2 (verbatim)
            with E155.warnings_as_errors():
                out = E155.execute_signed(E155.MULTI, A_ext, s,
                                          op=E155.STAR_OP,
                                          return_state=True)
            Vp = np.asarray(out["final_state"]["V"], dtype=float)
            V[pw] = Vp[pw]
            outs.append(bool(out.get("program_verified", False)))
            meta["planes"][p] = {
                "n_nodes": len(pw),
                "nodes": [int(x) for x in pw],
                "n_crossing_zeroed": len(pcross),
                "n_flip_entries": int(np.count_nonzero(Fc)),
                "program_verified":
                    bool(out.get("program_verified", False))}
        meta["program_verified_all_planes"] = bool(all(outs))
        return V, meta

    def armed_run_quiet_cone(members: dict, W_avg: np.ndarray,
                             chords: list, T_plan: np.ndarray,
                             seeds: list, arm: dict = None,
                             face_log: list = None,
                             census_out: dict = None) -> dict:
        """E155.run_quiet_cone copied VERBATIM with ONE face added: when
        arm = {"member": m, "ring": k, ...} and the current
        (member, ring) matches, the pooled read of that ring-event is
        replaced by plane_resolved_read (the face above). Everything
        else — walk, windows, channel log, attribution, finalize — is
        the deposited JD protocol byte-for-byte."""
        seq, frontiers = E155.quiet_c_sequence(W_avg, chords, E155.RINGS)
        # THE COMPOSED RULE (the one delta vs exp205's arm): at the
        # armed ring the frontier is COMPOSED — the flip-quiet reach
        # plus the JD-excluded cells that sit on canon-value boundaries
        # in the target plan (the fence yields for READING at the
        # site); the walk's committed set continues from the QUIET C
        # (exp155 verbatim), so every other ring is the replay's by
        # construction. The admitted set is computed once, here.
        admitted = {}
        if arm is not None:
            Wq = W_avg.copy()
            for (i, j) in chords:
                Wq[i, j] = Wq[j, i] = 0.0
            C = set(E155.seed_cone(W_avg))
            if census_out is not None:
                census_out["rings"] = []
            for k in range(1, len(frontiers) + 1):
                raw_F = set(E155.frontier_of(C, W_avg))
                quiet_F = set(frontiers[k - 1])
                if census_out is not None:
                    # THE CENSUS DISCLOSURE: per-ring membership
                    # census of the JD-a face — the fence's
                    # exclusions (raw_F - quiet_F) recorded at EVERY
                    # ring, so the composition's vacuity (if any) is
                    # a disclosed fact of the deposit, not a silent
                    # no-op.
                    census_out["rings"].append({
                        "k": k, "n_raw": len(raw_F),
                        "n_quiet": len(quiet_F),
                        "excl": sorted(raw_F - quiet_F)})
                if k == arm["ring"]:
                    T_plan_here = arm["T_plan"]
                    n = len(T_plan_here)
                    excl = raw_F - quiet_F
                    adm = set()
                    for j in excl:
                        # canon-value boundary cell: some lattice
                        # neighbor's target value differs from j's
                        # (the 100-node ring backbone: j +/- 1)
                        nbrs = ((j - 1) % n, (j + 1) % n)
                        if any(T_plan_here[i] != T_plan_here[j]
                               for i in nbrs):
                            adm.add(j)
                    admitted[k] = sorted(adm)
                    if census_out is not None:
                        census_out["armed_ring"] = k
                        census_out["n_excl_armed"] = len(excl)
                        census_out["admitted_at_armed"] = sorted(adm)
                    frontiers[k - 1] = sorted(quiet_F | adm)
                C = C | quiet_F
        names = list(members)
        runs = {m: {s: {"rings": [], "active": True, "committed": {},
                        "rings_expanded": 0}
                    for s in seeds} for m in names}
        chan_log, sweep = [], None
        for k, F in enumerate(frontiers, 1):
            win, C_prev = seq[k], seq[k - 1]
            if arm is not None and k in admitted:
                win = win | set(admitted[k])   # the read sees the site
                seq[k] = win
            crossing = E155.crossing_chords(chords, C_prev, F)
            wms = {m: E155.WindowQuietMedium(members[m], win, crossing)
                   for m in names}
            if arm is not None and k == arm["ring"] and sweep is None:
                sweep = {"ring": k, "member": arm["member"],
                         "armed": True}
            projs, Fcs = {}, {}
            for m in names:
                with E155.warnings_as_errors():
                    projs[m] = E155.project_phase_native(wms[m])
                Fcs[m] = E155.flip_clock_matrix(wms[m])
            A0 = projs[names[0]][0]
            proj_bitident = all(np.array_equal(A0, projs[m][0])
                                for m in names)
            fc0 = Fcs[names[0]]
            fc_bitident = all(np.array_equal(fc0, Fcs[m]) for m in names)
            fc_delta = max(float(np.max(np.abs(fc0 - Fcs[m])))
                           for m in names)
            bitident = bool(proj_bitident and fc_bitident)
            run_members = [names[0]] if bitident else names
            ring = {"ring_index": k,
                    "frontier": [int(j) for j in F],
                    "n_crossing_zeroed": len(crossing),
                    "crossing_edges": [[int(i), int(j)]
                                       for (i, j) in crossing],
                    "n_window_nodes": len(win),
                    "n_window_edges": int(np.count_nonzero(
                        np.triu(np.abs(A0) > 0, 1))),
                    "window_sha256_16": hashlib.sha256(
                        np.ascontiguousarray(A0).tobytes()
                    ).hexdigest()[:16],
                    "proj_bitident_across_pair": bool(proj_bitident),
                    "fc_bitident_across_pair": bool(fc_bitident),
                    "fc_cross_delta_max": round(fc_delta, 3),
                    "members": {}}
            for m in names:
                Fc = Fcs[m]
                ring["members"][m] = {
                    "fc_max": float(np.max(Fc)),
                    "fc_sum": float(np.sum(Fc)),
                    "n_flip_entries": int(np.count_nonzero(Fc))}
            emitted_by = {}
            for m in run_members:
                A = projs[m][0]
                A_ext = A + Fcs[m]       # TC2 (temporal read, verbatim)
                armed_here = bool(arm is not None
                                  and m == arm["member"]
                                  and k == arm["ring"])
                for s in seeds:
                    st = runs[m][s]
                    if not st["active"]:
                        continue
                    try:
                        if armed_here:
                            V, face_meta = plane_resolved_read(
                                members[m], win, crossing, s,
                                arm["plane_of"],
                                sweep=(s == seeds[0]))
                            out = {"program_verified":
                                   face_meta["program_verified_all_planes"]}
                            if face_log is not None:
                                face_log.append({
                                    "member": m, "seed": s,
                                    "ring": k, "face": face_meta})
                        else:
                            with E155.warnings_as_errors():
                                out = E155.execute_signed(
                                    E155.MULTI, A_ext, s,
                                    op=E155.STAR_OP,
                                    return_state=True)
                            V = np.asarray(out["final_state"]["V"],
                                           dtype=float)
                            face_meta = None
                        emitted = V[F]
                        err = float(np.sqrt(np.mean(
                            (emitted - T_plan[F]) ** 2)))
                        rec = {"ring_expanded": True, "exhausted": False,
                               "read_ok": True,
                               "program_verified":
                                   bool(out.get("program_verified",
                                                False)),
                               "ring_index": k,
                               "frontier": [int(j) for j in F],
                               "emitted": [round(float(x), 3)
                                           for x in emitted],
                               "plan": [round(float(x), 3)
                                        for x in T_plan[F]],
                               "ring_err_mV": round(err, 3),
                               "attributed_from": None}
                        if face_meta is not None:
                            rec["plane_face"] = face_meta
                        rec["pass"] = bool(np.isfinite(err)
                                           and err < ERR_BAR)
                        st["rings"].append(rec)
                        st["rings_expanded"] += 1
                        for j, v in zip(F, emitted):
                            st["committed"][int(j)] = float(v)
                        emitted_by.setdefault(m, {})[s] = emitted
                    except Exception as e:    # zero-rejection hygiene
                        st["rings"].append({
                            "ring_expanded": True, "exhausted": False,
                            "read_ok": False, "ring_index": k,
                            "rejection":
                                f"{type(e).__name__}: {e}"[:200],
                            "attributed_from": None, "pass": False})
                        st["active"] = False
            if bitident and len(run_members) == 1:
                # per-ring attribution: the ONE deterministic cone IS
                # both members' cone (inputs bitwise-asserted above).
                for s in seeds:
                    src_list = runs[names[0]][s]["rings"]
                    if not (src_list and
                            src_list[-1].get("ring_index") == k):
                        continue
                    src = src_list[-1]
                    for m in names:
                        if m == names[0]:
                            continue
                        st = runs[m][s]
                        if not st["active"]:
                            continue
                        st["rings"].append(dict(src,
                                                attributed_from=names[0]))
                        if src.get("read_ok"):
                            st["rings_expanded"] += 1
                            for j, v in zip(src["frontier"],
                                            src["emitted"]):
                                st["committed"][int(j)] = float(v)
                        else:
                            st["active"] = False
            if not bitident:
                deltas = {}
                for s in seeds:
                    if all(s in emitted_by.get(m, {}) for m in names):
                        d = np.abs(emitted_by[names[0]][s]
                                   - emitted_by[names[1]][s])
                        deltas[str(s)] = round(float(np.max(d)), 6)
                ring["emitted_delta_max_by_seed"] = deltas
            chan_log.append(ring)
        # ---- finalize per (member, seed) cells (exp151/exp152 form) --
        out_members = {}
        for m in names:
            rlist = []
            for s in seeds:
                st = runs[m][s]
                expanded = [x for x in st["rings"] if x.get("read_ok")]
                n_pass = sum(1 for x in expanded if x.get("pass"))
                cell = bool(len(expanded) >= 3
                            and n_pass == len(expanded))
                committed_vec = None
                if st["committed"]:
                    nodes = sorted(st["committed"])
                    committed_vec = {"nodes": nodes,
                                     "values": [round(
                                         st["committed"][n], 3)
                                         for n in nodes]}
                n_attr = sum(1 for x in st["rings"]
                             if x.get("attributed_from"))
                rlist.append({"seed": s,
                              "rings_expanded": len(expanded),
                              "rings_passed": n_pass,
                              "exhausted": bool(
                                  st["rings"] and
                                  st["rings"][-1].get("exhausted"))
                              or len(frontiers) < E155.RINGS,
                              "cell_pass": cell,
                              "attributed_from": (names[0] if
                                                  m != names[0] and
                                                  n_attr > 0 else None),
                              "committed": committed_vec,
                              "rings": st["rings"]})
            out_members[m] = {"runs": rlist}
        return {"members": out_members, "ring_channel_log": chan_log,
                "sweep_ring1": sweep, "n_frontier_walk": len(frontiers)}

    # ==================================================================
    # --smoke: instrument subset only, discarded (permitted by the
    # pre-registration; evaluates NO gate).  Builds the F3@cs7
    # instance, asserts the verbatim JD pooled read reproduces the
    # deposit's breaking err at ring 1 (seed 1), runs the face once,
    # deposits the smoke record, returns.
    # ==================================================================
    if args.smoke:
        fam = "F3_canon_boundary"
        saved = old_floor_pin()
        try:
            W, chords = E155.averaged_substrate_cs(fam, E155.B_DOSE, 7)
            members = E155.pair_members_cs(fam, E155.B_DOSE, 7)
            T_plan = E155.plan_of(W)
            seq, frontiers = E155.quiet_c_sequence(W, chords, E155.RINGS)
            F1r, win1, C_prev = frontiers[0], seq[1], seq[0]
            crossing = E155.crossing_chords(chords, C_prev, F1r)
            wm = E155.WindowQuietMedium(members["per"], win1, crossing)
            with E155.warnings_as_errors():
                A_ext = (E155.project_phase_native(wm)[0]
                         + E155.flip_clock_matrix(wm))
            out = E155.execute_signed(E155.MULTI, A_ext, 1,
                                      op=E155.STAR_OP,
                                      return_state=True)
            V = np.asarray(out["final_state"]["V"], dtype=float)
            jd_err = round(float(np.sqrt(np.mean(
                (V[F1r] - T_plan[F1r]) ** 2))), 3)
            plane_of = plane_of_map(W)
            Vs, meta = plane_resolved_read(members["per"], win1,
                                           crossing, 1, plane_of,
                                           sweep=True)
            face_err = round(float(np.sqrt(np.mean(
                (Vs[F1r] - T_plan[F1r]) ** 2))), 3)
        finally:
            restore_floors(saved)
        dep_err = next(rr["ring_err_mV"]
                       for run in dep155["disciplined_junction"][fam]
                       ["members"]["per"]["runs"] if run["seed"] == 1
                       for rr in run["rings"]
                       if rr["ring_index"] == 1)
        smoke = {
            "exp": "exp210_boundary_aware_frontier", "smoke": True,
            "instrument_check": {
                "jd_pooled_ring1_seed1_err_mV": jd_err,
                "deposit_err_mV": dep_err,
                "bit_exact_vs_deposit": bool(jd_err == dep_err)},
            "face_probe": {
                "plane_resolved_ring1_seed1_err_mV": face_err,
                "planes": meta["planes"], "sweep_ok": meta["sweep_ok"],
                "frontier_planes": {int(j): plane_of[j]
                                    for j in sorted(F1r)}}}
        assert smoke["instrument_check"]["bit_exact_vs_deposit"], \
            "smoke: JD pooled read drifted from the deposit"
        os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                    exist_ok=True)
        with open(out_path, "w") as fh:
            json.dump(smoke, fh, indent=1, default=float)
        print(f"  smoke deposited {out_path} (discarded; no gates) "
              f"| JD {jd_err} vs deposit {dep_err} | face {face_err}")
        return smoke

    # ==================================================================
    # GATE-F1 (anchor): exp200's replay machinery VERBATIM — exp155's
    # battery re-run in-process under the FULL floor pin, ring tables
    # diffed vs the deposit (141 rows expected), the 69-row ring-event
    # table rebuilt, the 3 boundary events checked against BOTH the
    # exp155 deposit and the exp200 deposit.
    # ==================================================================
    fresh155_path = os.path.join(ROOT, "results",
                                 "_exp205_replay_exp155.json")
    saved_out = E155.OUT
    E155.OUT = fresh155_path
    saved_argv = sys.argv
    sys.argv = [sys.argv[0]]          # the replay's parser sees no args
    saved_floors = old_floor_pin()
    try:
        fresh155 = E155.main()
    finally:
        E155.OUT = saved_out
        sys.argv = saved_argv
        restore_floors(saved_floors)

    sections_155 = ("disciplined_junction", "undisciplined_junction")
    replay = {"rows_checked": 0, "mismatches": [], "per_section": {}}
    for sec in sections_155:
        old = ring_table(dep155, sec)
        new = ring_table(fresh155, sec)
        assert len(old) == len(new), \
            f"{sec}: ring count drift {len(old)} vs {len(new)}"
        mism = []
        for a, b in zip(old, new):
            replay["rows_checked"] += 1
            key = (a["section"], a["family"], a["variant"],
                   a["seed"], a["ring_index"])
            if a["frontier"] != b["frontier"]:
                mism.append({"key": key, "field": "frontier"})
            if round(a["ring_err_mV"], 3) != round(b["ring_err_mV"], 3):
                mism.append({"key": key, "field": "ring_err_mV",
                             "old": a["ring_err_mV"],
                             "new": b["ring_err_mV"]})
            if a["pass"] != b["pass"]:
                mism.append({"key": key, "field": "pass"})
        replay["per_section"][sec] = {
            "rows": len(old), "mismatches": len(mism)}
        replay["mismatches"].extend(mism)

    # the ring-event rows (exp200's construction verbatim) + the
    # boundary events vs BOTH deposits
    disc = {(r["family"], r["variant"], r["seed"], r["ring_index"]): r
            for r in ring_table(fresh155, "disciplined_junction")}
    undisc = {(r["family"], r["variant"], r["seed"], r["ring_index"]): r
              for r in ring_table(fresh155, "undisciplined_junction")}
    rows, n_missing_undisc = [], 0
    for key, d in sorted(disc.items()):
        u = undisc.get(key)
        if u is None:
            n_missing_undisc += 1
            continue
        dev = float(u["ring_err_mV"]) - float(d["ring_err_mV"])
        rows.append({
            "family": d["family"], "variant": d["variant"],
            "seed": d["seed"], "ring_index": d["ring_index"],
            "k_realized": int(d["n_frontier"]),
            "err_disciplined_mV": float(d["ring_err_mV"]),
            "err_undisciplined_mV": float(u["ring_err_mV"]),
            "dev1_signed": round(dev, 6),
            "residual_excess_mV": round(float(d["ring_err_mV"])
                                        - ERR_MARGIN, 6),
            "disc_pass": bool(d["pass"]),
            "boundary_event": bool(
                d["family"] == "F3_canon_boundary"
                and d["variant"] == "per"
                and d["ring_index"] == 1
                and not d["pass"])})
    boundary = [r for r in rows if r["boundary_event"]]
    dep200_rows = {(r["family"], r["variant"], r["seed"],
                    r["ring_index"]): r
                   for r in dep200["sections"]["rows"]}
    boundary_repro = []
    for r in boundary:
        key = (r["family"], r["variant"], r["seed"], r["ring_index"])
        d155r = next(x for x in ring_table(dep155, "disciplined_junction")
                     if (x["family"], x["variant"], x["seed"],
                         x["ring_index"]) == key)
        d200r = dep200_rows[key]
        boundary_repro.append({
            "variant": r["variant"], "seed": r["seed"],
            "ring_index": r["ring_index"],
            "frontier": disc[key]["frontier"],
            "err_disciplined_mV": r["err_disciplined_mV"],
            "err_undisciplined_mV": r["err_undisciplined_mV"],
            "k_realized": r["k_realized"],
            "matches_exp155_deposit": bool(
                r["err_disciplined_mV"] == d155r["ring_err_mV"]
                and r["err_undisciplined_mV"]
                == next(x["ring_err_mV"] for x in
                        ring_table(dep155, "undisciplined_junction")
                        if (x["family"], x["variant"], x["seed"],
                            x["ring_index"]) == key)),
            "matches_exp200_deposit": bool(
                r["err_disciplined_mV"]
                == d200r["err_disciplined_mV"]
                and r["err_undisciplined_mV"]
                == d200r["err_undisciplined_mV"]
                and r["k_realized"] == d200r["k_realized"])})
    fresh_verdict = str(fresh155.get("verdict", ""))
    c1_pass = bool(replay["rows_checked"] == 141
                   and len(replay["mismatches"]) == 0
                   and "3" in fresh_verdict and "PASS" in fresh_verdict
                   and len(rows) == 69 and len(boundary) == 3
                   and all(r["matches_exp155_deposit"]
                           and r["matches_exp200_deposit"]
                           for r in boundary_repro))
    print(f"  GATE-F1 anchor: {replay['rows_checked']} ring rows, "
          f"{len(replay['mismatches'])} mismatches | {len(rows)} "
          f"ring-events, {len(boundary)} boundary events | fresh "
          f"verdict {fresh_verdict}")

    # ==================================================================
    # THE ARMED PROTOCOL: the JD battery re-run with the face armed at
    # (F3_canon_boundary, member per, ring 1) ONLY — the exact site the
    # exp200 localization named.  F1 runs through E155.run_quiet_cone
    # VERBATIM (the deposited function object); F3 runs through the
    # armed copy (the face is its only delta — GATE-F3 verifies the
    # copy's fidelity on every ring the arm does not touch).
    # ==================================================================
    armed = {}
    face_log = []
    census = {}
    plane_geoms = {}
    saved_floors = old_floor_pin()
    try:
        for fam in FAMS:
            W, chords = E155.averaged_substrate_cs(fam, E155.B_DOSE,
                                                   E155.CHORD_SEED_DEPOSITED)
            members = E155.pair_members_cs(fam, E155.B_DOSE,
                                           E155.CHORD_SEED_DEPOSITED)
            T_plan = E155.plan_of(W)
            if fam == "F3_canon_boundary":
                plane_of = plane_of_map(W)
                plane_geoms[fam] = {
                    "planes_source": ("labeling_bfs_n on the averaged "
                                      "substrate (the construction's "
                                      "own canon), head = canon >= "
                                      "pinned NEURAL_SPEC_MIN "
                                      f"({OLD_FLOOR})"),
                    "n_head": sum(1 for v in plane_of.values()
                                  if v == "head"),
                    "n_tail": sum(1 for v in plane_of.values()
                                  if v == "tail")}
                armed[fam] = armed_run_quiet_cone(
                    members, W, chords, T_plan, list(E155.SEEDS),
                    arm={"member": "per", "ring": 1,
                         "plane_of": plane_of, "T_plan": T_plan},
                    face_log=face_log, census_out=census)
            else:
                armed[fam] = E155.run_quiet_cone(
                    members, W, chords, T_plan, list(E155.SEEDS))
    finally:
        restore_floors(saved_floors)

    # the boundary-plane cells of the armed window (disclosure): the
    # window cells the face removes from every plane's decode
    saved_floors = old_floor_pin()
    try:
        W_f3, chords_f3 = E155.averaged_substrate_cs(
            "F3_canon_boundary", E155.B_DOSE, E155.CHORD_SEED_DEPOSITED)
        plane_of_f3 = plane_of_map(W_f3)
        seq_f3, front_f3 = E155.quiet_c_sequence(
            W_f3, chords_f3, E155.RINGS)
    finally:
        restore_floors(saved_floors)
    win_f3, crossing_f3 = seq_f3[1], E155.crossing_chords(
        chords_f3, seq_f3[0], front_f3[0])
    boundary_cells = sorted(
        (i, j) for i in win_f3 for j in win_f3
        if i < j and (W_f3[i, j] != 0.0
                      or (i, j) in crossing_f3)
        and plane_of_f3[i] != plane_of_f3[j])
    face_events = []
    for run in armed["F3_canon_boundary"]["members"]["per"]["runs"]:
        rec = next(x for x in run["rings"] if x["ring_index"] == 1)
        face_events.append({
            "variant": "per", "seed": run["seed"],
            "ring_index": 1, "frontier": rec["frontier"],
            "armed_err_mV": rec["ring_err_mV"],
            "emitted": rec["emitted"], "plan": rec["plan"],
            "pass": rec["pass"],
            "planes_program_verified":
                rec.get("plane_face", {})
                .get("program_verified_all_planes"),
            "plane_flip_entries":
                {p: rec.get("plane_face", {}).get("planes", {})
                 .get(p, {}).get("n_flip_entries")
                 for p in ("head", "tail")}})
    face_events.sort(key=lambda r: r["seed"])

    # ==================================================================
    # GATE-F2 (the repair): per-event errs for all 3 seeds; branch:
    # REPAIR (all 3 < 6.0) / PARTIAL (>= 1 < 6.0 and none worse than
    # the disciplined baseline) / NONE (otherwise).  The disciplined
    # baseline = the fresh replay's errs at the same 3 events (C1).
    # ==================================================================
    baseline = {r["seed"]: r["err_disciplined_mV"] for r in boundary}
    n_below = sum(1 for r in face_events if r["armed_err_mV"] < ERR_BAR)
    n_worse = sum(1 for r in face_events
                  if r["armed_err_mV"] > baseline[r["seed"]])
    if n_below == len(face_events) == 3:
        branch = "REPAIR"
    elif n_below >= 1 and n_worse == 0:
        branch = "PARTIAL"
    else:
        branch = "NONE"
    c2_pass = True   # all three branches complete the gate (registered)
    print(f"  GATE-F2 repair: armed errs "
          f"{[r['armed_err_mV'] for r in face_events]} vs baseline "
          f"{[baseline[r['seed']] for r in face_events]} "
          f"(< bar {n_below}/3, worse than baseline {n_worse}) -> "
          f"{branch}")

    # ==================================================================
    # GATE-F3 (no-regression, the identity clause): every ring-event
    # OUTSIDE the arm's site must be bit-exact vs exp200's replay
    # (ring_err_mV, emitted, frontier, pass).  The arm's site = the 3
    # boundary events; every other ring-event — including the passing
    # aper ring-1 reads at the SAME window — must be untouched.
    # ==================================================================
    identity = []
    n_identity_mism = 0
    for fam in FAMS:
        for m in ("per", "aper"):
            ra_list = fresh155["disciplined_junction"][fam][
                "members"][m]["runs"]
            rb_list = armed[fam]["members"][m]["runs"]
            assert len(ra_list) == len(rb_list)
            for ra, rb in zip(ra_list, rb_list):
                assert ra["seed"] == rb["seed"]
                for x, y in zip(ra["rings"], rb["rings"]):
                    key = {"family": fam, "member": m,
                           "seed": ra["seed"],
                           "ring": x["ring_index"]}
                    armed_site = bool(fam == "F3_canon_boundary"
                                      and m == "per"
                                      and x["ring_index"] == 1)
                    fields_exact = bool(
                        x.get("ring_err_mV") == y.get("ring_err_mV")
                        and x.get("emitted") == y.get("emitted")
                        and x.get("frontier") == y.get("frontier")
                        and x.get("pass") == y.get("pass"))
                    if not armed_site:
                        n_identity_mism += int(not fields_exact)
                    identity.append(dict(
                        key, armed_site=armed_site,
                        replay_err_mV=x.get("ring_err_mV"),
                        armed_err_mV=y.get("ring_err_mV"),
                        bit_exact=fields_exact))
    n_armed_site = sum(1 for r in identity if r["armed_site"])
    c3_pass = bool(n_identity_mism == 0 and n_armed_site == 3)
    print(f"  GATE-F3 identity: {len(identity)} ring-events, "
          f"{n_armed_site} at the arm's site, {n_identity_mism} "
          f"identity mismatches outside the site")

    # ---- GATE-F4 (hygiene) ------------------------------------------
    def n_rej_cone(cone: dict) -> int:
        bad = 0
        for m in cone["members"]:
            for run in cone["members"][m]["runs"]:
                bad += sum(1 for x in run["rings"]
                           if not x.get("read_ok", True))
        return bad

    n_rej = sum(n_rej_cone(fresh155["disciplined_junction"][fam])
                for fam in FAMS) + sum(n_rej_cone(armed[fam])
                                       for fam in FAMS)
    def errs_of(cone: dict) -> list:
        return [x.get("ring_err_mV") for m in cone["members"]
                for run in cone["members"][m]["runs"]
                for x in run["rings"] if x.get("read_ok")]

    errs_all = ([x for fam in FAMS
                 for x in errs_of(fresh155["disciplined_junction"][fam])]
                + [x for fam in FAMS for x in errs_of(armed[fam])])
    all_finite = all(e is not None and np.isfinite(e) for e in errs_all)
    floors_restored = all(m.NEURAL_SPEC_MIN == v for m, v in
                          zip(PIN_MODS, FLOORS_ORIGINAL))
    c4_pass = bool(n_rej == 0 and all_finite and floors_restored)
    print(f"  GATE-F4 hygiene: rejections {n_rej}, all errs finite "
          f"{all_finite}, floors restored to originals "
          f"{floors_restored} (pin save/restore asserted at every "
          f"stage)")

    verdict = (f"{sum(int(x) for x in (c1_pass, c2_pass, c3_pass,
                                       c4_pass))}/4 gates "
               f"(C1 C2 C3 C4) | repair {branch}")
    print(f"  === {verdict} ===")

    result = {
        "exp": "exp210_boundary_aware_frontier",
        "claim": (
            "THE COMPOSED BOUNDARY-AWARE FRONTIER RULE (L178's "
            "registered next): exp205's pricing — the plane-resolved "
            "face halves the boundary residual (21-48% improvements "
            "at exactly the localized site) yet 0/3 cross the bar; "
            "exp155's discipline fails AT the boundary. The registered "
            "composition: the JD-a membership face gains a "
            "BOUNDARY-AWARE exception (the fence yields exactly at "
            "canon-boundary cells) and the boundary cells' read face "
            "is plane-resolved (exp158's machinery, exp205's armed "
            "face). One composed rule, zero knobs, aimed at the 3 "
            "breaking F3 ring-1 events."),
        "pre_registered": {
            "gates_source": ("module docstring, committed before any "
                             "run (pre-registration de1155d, batch 9; "
                             "gates F1-F4 fixed there, each evaluated "
                             "exactly once)"),
            "gates": [
                "GATE-F1 (anchor) exp205's replay reproduces (141/141 "
                "ring rows; the 3 boundary events at their "
                "disciplined errs)",
                "GATE-F2 (the composition) the composed rule at F3 "
                "ring-1: per-event errs for all 3 seeds; the branch "
                "named: REPAIR (all 3 < 6.0), PARTIAL (>= 1 < 6.0 and "
                "none worse than the disciplined baseline), NONE",
                "GATE-F3 (no-regression) every passing ring's err "
                "bit-exact vs the replay outside the F3 ring-1 site "
                "(the identity clause; the composed rule touches only "
                "the boundary site)",
                "GATE-F4 (hygiene) zero rejections; all finite; the "
                "pin save/restore asserted"],
            "composed_rule": (
                "JD-a' = the flip-quiet reach F_q of exp155's JD-a, "
                "EXCEPT that a node whose only committed-adjacency is "
                "a flip edge AND which sits on a canon-value boundary "
                "in the target is ADMITTED to the frontier with the "
                "plane-resolved read face (exp158's machinery) "
                "instead of exclusion; everything else exp155's "
                "protocol verbatim. Zero knobs."),
            "face_implementation": (
                "the canon planes are the construction's OWN labeling "
                "(labeling_bfs_n on the averaged substrate, head = "
                "canon >= the pinned NEURAL_SPEC_MIN — the same "
                "labeling that built the F3_canon_boundary family); "
                "each canon plane's induced sub-window is an "
                "E155.WindowQuietMedium (the JD window machinery "
                "verbatim, mask restricted to the plane's nodes) read "
                "by the verbatim TC1/TC2/TC3 chain (PN projection -> "
                "flip clock -> A_ext -> execute_signed); the frontier "
                "emission is stitched per plane (each frontier node "
                "emitted by its OWN plane's read); the ring-err "
                "convention (pooled RMS at the frontier) unchanged. "
                "The boundary-plane cells — window cells whose "
                "endpoints sit on different canon planes — have no "
                "plane home and enter NO plane's decode. Arm scope: "
                "the 3 boundary events (F3_canon_boundary, member "
                "per, ring 1, seeds 1/2/3) — GATE-F3's identity clause "
                "(every passing ring bit-exact, including the passing "
                "aper ring-1 reads at the same window) binds the arm "
                "to exactly the site the exp200 localization named"),
        },
        "sections": {
            "replay": replay,
            "rows": rows,
            "n_missing_undisc": n_missing_undisc,
            "boundary_events": boundary_repro,
            "exp155_fresh_verdict": fresh155.get("verdict"),
            "plane_geometry": plane_geoms,
            "armed_site": {"family": "F3_canon_boundary",
                           "member": "per", "ring": 1,
                           "seeds": list(E155.SEEDS)},
            "boundary_plane_cells": {
                "description": (
                    "window cells (i<j) with a nonzero averaged entry "
                    "or a JD-zeroed crossing edge whose endpoints sit "
                    "on different canon planes — removed from every "
                    "plane's decode by the face (5 chords + the ring "
                    "backbone edge at the boundary; the JD crossing "
                    "(12, 18) was already zeroed by the discipline)"),
                "cells": [[int(i), int(j)] for (i, j)
                          in boundary_cells]},
            "face_events": face_events,
            "face_log": face_log,
            "membership_census": {
                "disclosure": (
                    "per-ring census of the JD-a membership face on "
                    "this substrate: excl = raw_F - quiet_F at every "
                    "ring; the composed rule's membership face admits "
                    "ONLY fence-excluded canon-boundary cells at the "
                    "armed ring, so an empty excl list there means "
                    "the composed rule REDUCES to exp205's arm and "
                    "the binding face is the read face's window "
                    "zeroing"),
                "census": census.get("rings", []),
                "armed_ring": census.get("armed_ring"),
                "n_excl_armed": census.get("n_excl_armed"),
                "admitted_at_armed": census.get("admitted_at_armed")},
            "armed_protocol": armed,
            "identity_table": identity,
        },
        "gates": {
            "F1": {"pass": c1_pass,
                   "rows_checked": replay["rows_checked"],
                   "mismatches": len(replay["mismatches"]),
                   "n_ring_events": len(rows),
                   "n_boundary_events": len(boundary),
                   "boundary_repro": boundary_repro},
            "F2": {"pass": c2_pass, "branch": branch,
                   "armed_errs_mV": {str(r["seed"]): r["armed_err_mV"]
                                     for r in face_events},
                   "disciplined_baseline_mV":
                       {str(k): v for k, v in baseline.items()},
                   "n_below_bar": n_below, "n_worse_than_baseline":
                       n_worse,
                   "membership_face_armed": {
                       "n_excl": census.get("n_excl_armed"),
                       "admitted": census.get("admitted_at_armed")}},
            "F3": {"pass": c3_pass,
                   "n_ring_events": len(identity),
                   "n_armed_site": n_armed_site,
                   "identity_mismatches_outside_site":
                       n_identity_mism},
            "F4": {"pass": c4_pass, "rejections": n_rej,
                   "all_errs_finite": bool(all_finite)}},
        "verdict": verdict,
        "wall_s": round(time.time() - t0, 1)}

    os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(result, fh, indent=1, default=float)
    print(f"  deposited {out_path} | wall {result['wall_s']} s")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841
