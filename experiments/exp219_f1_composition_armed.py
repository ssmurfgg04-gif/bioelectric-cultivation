#!/usr/bin/env python3
"""exp219 — THE F1 COMPOSITION ARMED (L187's registered next).

exp212's census sweep named the site where the composed rule's
membership face can act for the first time: the JD-a fence bites at
F1_zone_tail rings 2-6 (11 excluded cell-ring pairs, 5 of them
canon-value boundary cells — the admission clause WOULD fire). This
run ARMS the exp210 composed rule (the fence's boundary-aware
exception + the plane-resolved read face) at F1: the boundary cells
in the fence's exclusions are ADMITTED with the plane-resolved read
face; everything else is exp155's disciplined protocol verbatim.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Instruments: exp210's composed machinery
VERBATIM (the JD-a' admission clause, the plane-resolved face, the
full-capture floor pin, the ring_table replay); the arm scope
PRE-NAMED from exp212's deposited census (zero re-derivation): the
F1_zone_tail family's exclusion sites (excl [74] at ring 2, [74] at
ring 3, [66, 74] at ring 4, [63, 66, 74] at ring 5, [61, 63, 66, 74]
at ring 6 — the canon-value boundary cells among them admitted, the
non-boundary exclusions KEEP the fence (the composition admits ONLY
boundary cells)); exp155's disciplined junction battery (the F1
family, members per/aper, seeds (1,2,3)) the replay baseline.

GATES (each evaluated exactly once):
  GATE-P1 (the replay) exp155's F1 rows reproduce bit-exactly
           outside the armed sites (the disciplined battery's ring
           errs at the deposit's rounding; the walk's committed SET
           identical).
  GATE-P2 (the composition) per-ring errs for the armed F1 events,
           all seeds; the branch named: REPAIR (every armed ring
           err < 6.0 mV), PARTIAL (>= 1 < 6.0 and none worse than
           the disciplined baseline at that ring), NONE.
  GATE-P3 (the identity clause) every NON-armed ring's err bit-exact
           vs the replay (the composition touches only the census-
           named boundary admissions; the aper member's rings
           included).
  GATE-P4 (hygiene) zero rejections; all finite; the -35.0 pin
           save/restore asserted; the admission sets asserted ==
           exp212's deposited census (the boundary cells only).
NO post-hoc tuning. --smoke permitted, discarded.
DEPOSIT: results/exp219_f1_composition_armed.json
RUN: python3 -m experiments.exp219_f1_composition_armed [--smoke] [--job ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "results", "exp219_f1_composition_armed.json")


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

    import cultivation.bioelectric.collective as CORE
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
        """exp210's full-capture pin VERBATIM (exp168's B2 mechanism,
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
    DEP212 = os.path.join(ROOT, "results",
                          "exp212_jda_census_sweep.json")
    ERR_BAR = E155.ERR_BAR
    FAM = "F1_zone_tail"
    VARS = ("per", "aper")
    ERR_MARGIN = 6.0                     # exp151/152's cell bar
    # THE ARM SCOPE, PRE-NAMED in the docstring from exp212's deposited
    # census (zero re-derivation): the F1_zone_tail family's exclusion
    # sites, rings 2-6; the canon-value boundary cells among the
    # exclusions are ADMITTED (the composition admits ONLY boundary
    # cells), the non-boundary exclusions KEEP the fence.
    ARMED_RINGS = (2, 3, 4, 5, 6)
    PRENAMED_EXCL = {2: [74], 3: [74], 4: [66, 74],
                     5: [63, 66, 74], 6: [61, 63, 66, 74]}
    PRENAMED_ADMIT = {2: [74], 3: [74], 4: [74], 5: [74], 6: [74]}

    dep155 = json.load(open(DEP155))
    dep212 = json.load(open(DEP212))

    # the arm scope read back from exp212's deposit and asserted
    # against the pre-named scope (the deposit must MATCH the
    # pre-registration, not the other way round)
    excl212 = {s["ring"]: sorted(s["excl"])
               for s in dep212["gates"]["C2"]["sites"]
               if s["family"] == FAM}
    cls212 = {c["ring"]: c
              for c in dep212["gates"]["C3"]["classified_sites"]
              if c["family"] == FAM}
    admit212 = {k: sorted(x["cell"] for x in cls212[k]["cells"]
                          if x["canon_boundary"])
                for k in cls212}
    assert excl212 == PRENAMED_EXCL, \
        "exp212's deposited excl sites drifted from the pre-named scope"
    assert admit212 == PRENAMED_ADMIT, \
        "exp212's deposited boundary classification drifted from the " \
        "pre-named admission scope"

    def ring_table(payload: dict, section: str,
                   fams=(FAM,)) -> list:
        # exp200's ring_table VERBATIM (exp210's instrument; the family
        # set parameterized, default the armed family)
        rows = []
        for fam in fams:
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
    # THE PLANE-RESOLVED FACE (exp158's machinery via exp210, zero
    # knobs).  The canon planes are the construction's OWN labeling
    # (exp148 chord_set's canon: labeling_bfs_n on the ring substrate,
    # head = canon >= the pinned NEURAL_SPEC_MIN).  The face reads the
    # window PLANE-RESOLVED: each canon plane's induced sub-window is
    # a WindowQuietMedium (E155's class verbatim, mask restricted to
    # the plane's nodes) decoded by the verbatim TC1/TC2/TC3 chain (PN
    # projection -> flip clock -> A_ext -> execute_signed), and the
    # frontier emission is stitched per plane (each frontier node
    # emitted by its OWN plane's read; the pooled RMS err convention
    # unchanged).  The boundary-plane cells — window cells whose
    # endpoints sit on different canon planes — have no plane home and
    # enter NO plane's decode: the read that sees the boundary.
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
        arm = {"member": m, "rings": {...}, ...} and the current
        (member, ring) matches, the pooled read of that ring-event is
        replaced by plane_resolved_read (the face above), and the
        ring's frontier is COMPOSED (the JD-a' admission clause: the
        flip-quiet reach plus the fence-excluded cells that sit on
        canon-value boundaries in the target plan — the fence yields
        for READING at the armed sites ONLY for boundary cells).
        Everything else — walk, windows, channel log, attribution,
        finalize — is the deposited JD protocol byte-for-byte.  Delta
        vs exp210's armed copy: the arm carries a SET of rings
        (exp212's census named five), the admission clause runs at
        every armed ring; the walk's committed set continues from the
        QUIET C (exp155 verbatim) at every ring."""
        seq, frontiers = E155.quiet_c_sequence(W_avg, chords, E155.RINGS)
        # THE COMPOSED RULE: at each armed ring the frontier is
        # COMPOSED — the flip-quiet reach plus the JD-excluded cells
        # that sit on canon-value boundaries in the target plan; the
        # walk's committed set continues from the QUIET C (exp155
        # verbatim), so every other ring is the replay's by
        # construction. The admitted set is computed once per ring,
        # here.
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
                    # ring (exp210's disclosure, now checked against
                    # exp212's deposited census at P4).
                    census_out["rings"].append({
                        "k": k, "n_raw": len(raw_F),
                        "n_quiet": len(quiet_F),
                        "excl": sorted(raw_F - quiet_F)})
                if k in arm["rings"]:
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
                        census_out.setdefault("armed_rings",
                                              []).append(k)
                        census_out.setdefault("n_excl_at_armed",
                                              {})[str(k)] = len(excl)
                        census_out.setdefault("admitted_at_armed",
                                              {})[str(k)] = sorted(adm)
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
            if arm is not None and k in arm["rings"] and sweep is None:
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
                                  and k in arm["rings"])
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
    # pre-registration; evaluates NO gate).  Builds the F1@cs7
    # instance, asserts the verbatim JD pooled read reproduces the
    # deposit's F1 ring-2 err (seed 1), asserts the ring-2 census ==
    # exp212's deposited site (excl [74], admitted [74]), runs the
    # composed face once at ring 2, deposits the smoke record, returns.
    # ==================================================================
    if args.smoke:
        saved = old_floor_pin()
        try:
            W, chords = E155.averaged_substrate_cs(FAM, E155.B_DOSE,
                                                   E155.CHORD_SEED_DEPOSITED)
            members = E155.pair_members_cs(FAM, E155.B_DOSE,
                                           E155.CHORD_SEED_DEPOSITED)
            T_plan = E155.plan_of(W)
            n = len(T_plan)
            seq, frontiers = E155.quiet_c_sequence(W, chords, E155.RINGS)
            # the census at the first armed ring (2), exp212's
            # machinery verbatim
            C = set(E155.seed_cone(W))
            excl2, quiet_F2 = [], set()
            for k in range(1, 2 + 1):
                raw_F = set(E155.frontier_of(C, W))
                quiet_F = set(frontiers[k - 1])
                if k == 2:
                    excl2 = sorted(raw_F - quiet_F)
                    quiet_F2 = quiet_F
                C = C | quiet_F
            adm2 = [j for j in excl2
                    if any(T_plan[i] != T_plan[j]
                           for i in ((j - 1) % n, (j + 1) % n))]
            # the pooled JD read at ring 2 (seed 1) on the QUIET
            # geometry vs the deposit
            F2q, win2, C_prev = (sorted(quiet_F2), seq[2], seq[1])
            crossing = E155.crossing_chords(chords, C_prev, F2q)
            wm = E155.WindowQuietMedium(members["per"], win2, crossing)
            with E155.warnings_as_errors():
                A_ext = (E155.project_phase_native(wm)[0]
                         + E155.flip_clock_matrix(wm))
            out = E155.execute_signed(E155.MULTI, A_ext, 1,
                                      op=E155.STAR_OP,
                                      return_state=True)
            V = np.asarray(out["final_state"]["V"], dtype=float)
            jd_err = round(float(np.sqrt(np.mean(
                (V[F2q] - T_plan[F2q]) ** 2))), 3)
            # the composed face once at ring 2 (seed 1)
            F2c = sorted(set(F2q) | set(adm2))
            win2c = set(win2) | set(adm2)
            crossing_c = E155.crossing_chords(chords, C_prev, F2c)
            plane_of = plane_of_map(W)
            Vs, meta = plane_resolved_read(members["per"], win2c,
                                           crossing_c, 1, plane_of,
                                           sweep=True)
            face_err = round(float(np.sqrt(np.mean(
                (Vs[F2c] - T_plan[F2c]) ** 2))), 3)
        finally:
            restore_floors(saved)
        dep_err = next(rr["ring_err_mV"]
                       for run in dep155["disciplined_junction"][FAM]
                       ["members"]["per"]["runs"] if run["seed"] == 1
                       for rr in run["rings"]
                       if rr["ring_index"] == 2)
        site2 = next(s for s in dep212["gates"]["C2"]["sites"]
                     if s["family"] == FAM and s["ring"] == 2)
        smoke = {
            "exp": "exp219_f1_composition_armed", "smoke": True,
            "instrument_check": {
                "jd_pooled_ring2_seed1_err_mV": jd_err,
                "deposit_err_mV": dep_err,
                "bit_exact_vs_deposit": bool(jd_err == dep_err),
                "ring2_census_excl": excl2,
                "exp212_site_excl": sorted(site2["excl"]),
                "census_matches_exp212": bool(
                    excl2 == sorted(site2["excl"])),
                "ring2_admitted_boundary": adm2},
            "face_probe": {
                "composed_frontier": F2c,
                "plane_resolved_ring2_seed1_err_mV": face_err,
                "planes": meta["planes"], "sweep_ok": meta["sweep_ok"],
                "frontier_planes": {int(j): plane_of[j]
                                    for j in sorted(F2c)}}}
        assert smoke["instrument_check"]["bit_exact_vs_deposit"], \
            "smoke: JD pooled read drifted from the deposit"
        assert smoke["instrument_check"]["census_matches_exp212"], \
            "smoke: ring-2 census drifted from exp212's deposit"
        os.makedirs(os.path.dirname(os.path.abspath(out_path)),
                    exist_ok=True)
        with open(out_path, "w") as fh:
            json.dump(smoke, fh, indent=1, default=float)
        print(f"  smoke deposited {out_path} (discarded; no gates) "
              f"| JD {jd_err} vs deposit {dep_err} | excl {excl2} "
              f"| face {face_err}")
        return smoke

    # ==================================================================
    # P1's REPLAY: exp155's battery re-run in-process under the FULL
    # floor pin (exp210's replay block verbatim; the scratch deposit
    # redirected).  The F1 disciplined rows are then diffed vs the
    # exp155 deposit (ring errs at the deposit's rounding; the walk's
    # committed SET identical) — the replay baseline for P2's branch
    # and P3's identity clause.
    # ==================================================================
    fresh155_path = os.path.join(ROOT, "results",
                                 "_exp219_replay_exp155.json")
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

    replay = {"rows_checked": 0, "mismatches": [],
              "committed_set_mismatches": []}
    old_f1 = [r for r in ring_table(dep155, "disciplined_junction")
              if r["family"] == FAM]
    new_f1 = [r for r in ring_table(fresh155, "disciplined_junction")
              if r["family"] == FAM]
    assert len(old_f1) == len(new_f1) == 36, \
        f"F1 ring-row count drift: {len(old_f1)} vs {len(new_f1)}"
    for a, b in zip(old_f1, new_f1):
        replay["rows_checked"] += 1
        key = {"variant": a["variant"], "seed": a["seed"],
               "ring": a["ring_index"]}
        if a["frontier"] != b["frontier"]:
            replay["mismatches"].append({**key, "field": "frontier"})
        if round(a["ring_err_mV"], 3) != round(b["ring_err_mV"], 3):
            replay["mismatches"].append({**key, "field": "ring_err_mV",
                                         "old": a["ring_err_mV"],
                                         "new": b["ring_err_mV"]})
        if a["pass"] != b["pass"]:
            replay["mismatches"].append({**key, "field": "pass"})
    # the walk's committed SET: per (member, seed), the committed node
    # set of the disciplined battery — replay vs deposit
    for var in VARS:
        for ro, rn in zip(dep155["disciplined_junction"][FAM]
                          ["members"][var]["runs"],
                          fresh155["disciplined_junction"][FAM]
                          ["members"][var]["runs"]):
            assert ro["seed"] == rn["seed"]
            so = set(ro["committed"]["nodes"]) if ro.get("committed") \
                else set()
            sn = set(rn["committed"]["nodes"]) if rn.get("committed") \
                else set()
            if so != sn:
                replay["committed_set_mismatches"].append(
                    {"variant": var, "seed": ro["seed"],
                     "deposit": sorted(so), "replay": sorted(sn)})
    fresh_verdict = str(fresh155.get("verdict", ""))
    c1_pass = bool(replay["rows_checked"] == 36
                   and len(replay["mismatches"]) == 0
                   and len(replay["committed_set_mismatches"]) == 0)
    print(f"  P1 replay: {replay['rows_checked']} F1 ring rows, "
          f"{len(replay['mismatches'])} mismatches, "
          f"{len(replay['committed_set_mismatches'])} committed-set "
          f"mismatches | fresh verdict {fresh_verdict}")

    # ==================================================================
    # THE ARMED PROTOCOL: the JD battery's F1 family re-run with the
    # composed rule armed at the census-named sites ONLY — (F1,
    # member per, rings 2-6): the admission clause admits the fence's
    # canon-boundary exclusions (cell 74 per ring; the non-boundary
    # exclusions 66/63/61 KEEP the fence) and the boundary cells' read
    # face is plane-resolved.  exp210's armed copy verbatim, the arm's
    # ring set the only generalization (five rings, pre-named).
    # ==================================================================
    armed = {}
    face_log = []
    census = {}
    plane_geom = {}
    saved_floors = old_floor_pin()
    try:
        W, chords = E155.averaged_substrate_cs(FAM, E155.B_DOSE,
                                               E155.CHORD_SEED_DEPOSITED)
        members = E155.pair_members_cs(FAM, E155.B_DOSE,
                                       E155.CHORD_SEED_DEPOSITED)
        T_plan = E155.plan_of(W)
        plane_of = plane_of_map(W)
        plane_geom[FAM] = {
            "planes_source": ("labeling_bfs_n on the averaged "
                              "substrate (the construction's own "
                              "canon), head = canon >= pinned "
                              f"NEURAL_SPEC_MIN ({OLD_FLOOR})"),
            "n_head": sum(1 for v in plane_of.values() if v == "head"),
            "n_tail": sum(1 for v in plane_of.values() if v == "tail")}
        armed[FAM] = armed_run_quiet_cone(
            members, W, chords, T_plan, list(E155.SEEDS),
            arm={"member": "per", "rings": frozenset(ARMED_RINGS),
                 "plane_of": plane_of, "T_plan": T_plan},
            face_log=face_log, census_out=census)
    finally:
        restore_floors(saved_floors)

    # ---- P4's admission-set check: the armed run's recomputed census
    #      vs exp212's deposited census (every ring; the admission
    #      sets == the deposited boundary cells ONLY) -----------------
    dep212_census_f1 = {r["ring"]: r
                        for r in dep212["sections"]["census"]
                        if r["family"] == FAM}
    run_census = {r["k"]: r for r in census.get("rings", [])}
    census_match = bool(
        set(run_census) == set(dep212_census_f1)
        == set(range(1, E155.RINGS + 1)))
    if census_match:
        for k in range(1, E155.RINGS + 1):
            a, b = run_census[k], dep212_census_f1[k]
            census_match = bool(
                census_match
                and a["n_raw"] == b["n_raw"]
                and a["n_quiet"] == b["n_quiet"]
                and a["excl"] == sorted(b["excl"]))
    census_match = bool(census_match
                        and census.get("armed_rings")
                        == list(ARMED_RINGS))
    for k in ARMED_RINGS:
        census_match = bool(
            census_match
            and sorted(census.get("admitted_at_armed", {})
                       .get(str(k), [])) == admit212[k])

    # ---- the composition-delta disclosure: armed vs replay channel
    #      geometry per ring — the arm must touch the frontier/window
    #      by EXACTLY the census-named admissions and nothing else ----
    replay_chan = {r["ring_index"]: r for r in
                   fresh155["disciplined_junction"][FAM]
                   ["ring_channel_log"]}
    armed_chan = {r["ring_index"]: r for r in
                  armed[FAM]["ring_channel_log"]}
    delta_rows = []
    for k in range(1, E155.RINGS + 1):
        ro, rn = replay_chan[k], armed_chan[k]
        added = sorted(set(rn["frontier"]) - set(ro["frontier"]))
        removed = sorted(set(ro["frontier"]) - set(rn["frontier"]))
        delta_rows.append({
            "ring": k,
            "replay_frontier": ro["frontier"],
            "armed_frontier": rn["frontier"],
            "frontier_added": added,
            "frontier_removed": removed,
            "n_window_nodes_replay": ro["n_window_nodes"],
            "n_window_nodes_armed": rn["n_window_nodes"],
            "window_nodes_added": rn["n_window_nodes"]
            - ro["n_window_nodes"],
            "n_crossing_zeroed_replay": ro["n_crossing_zeroed"],
            "n_crossing_zeroed_armed": rn["n_crossing_zeroed"],
            "delta_matches_census_admission":
                bool(added == admit212.get(k, [])
                     and removed == [] and rn["n_window_nodes"]
                     - ro["n_window_nodes"] == len(admit212.get(k, [])))
        })

    # ---- the boundary-plane cells of the armed windows (disclosure):
    #      the window cells the face removes from every plane's decode
    saved_floors = old_floor_pin()
    try:
        W_f1, chords_f1 = E155.averaged_substrate_cs(
            FAM, E155.B_DOSE, E155.CHORD_SEED_DEPOSITED)
        plane_of_f1 = plane_of_map(W_f1)
        seq_f1, front_f1 = E155.quiet_c_sequence(
            W_f1, chords_f1, E155.RINGS)
    finally:
        restore_floors(saved_floors)
    boundary_plane_cells = {}
    for k in ARMED_RINGS:
        win_k = set(seq_f1[k]) | set(admit212[k])
        F_k = sorted(set(front_f1[k - 1]) | set(admit212[k]))
        crossing_k = E155.crossing_chords(chords_f1, seq_f1[k - 1], F_k)
        bp = sorted((i, j) for i in win_k for j in win_k
                    if i < j and (W_f1[i, j] != 0.0
                                  or (i, j) in crossing_k)
                    and plane_of_f1[i] != plane_of_f1[j])
        boundary_plane_cells[str(k)] = {
            "n_window_nodes": len(win_k),
            "cells": [[int(i), int(j)] for (i, j) in bp]}

    # ==================================================================
    # GATE-P2 (the composition): per-ring errs for the armed F1
    # events, all seeds — every (member, seed, ring) record at the
    # armed rings (under F1's pair-attribution the aper records are
    # the cone's own; disclosed per record).  Branch: REPAIR (every
    # armed ring err < 6.0), PARTIAL (>= 1 < 6.0 and none worse than
    # the disciplined baseline at that ring), NONE.  The disciplined
    # baseline = the fresh replay's errs at the same (member, seed,
    # ring) (P1's rows).
    # ==================================================================
    baseline = {(r["variant"], r["seed"], r["ring_index"]):
                r["ring_err_mV"] for r in new_f1}
    armed_events = []
    for var in VARS:
        for run in armed[FAM]["members"][var]["runs"]:
            for rr in run["rings"]:
                if rr["ring_index"] not in ARMED_RINGS:
                    continue
                key = (var, run["seed"], rr["ring_index"])
                armed_events.append({
                    "variant": var, "seed": run["seed"],
                    "ring_index": rr["ring_index"],
                    "frontier": rr.get("frontier"),
                    "armed_err_mV": rr.get("ring_err_mV"),
                    "baseline_err_mV": baseline[key],
                    "emitted": rr.get("emitted"),
                    "plan": rr.get("plan"),
                    "pass": rr.get("pass"),
                    "attributed_from": rr.get("attributed_from"),
                    "face_read": bool(var == "per"
                                      and rr.get("attributed_from")
                                      is None
                                      and rr.get("read_ok")),
                    "planes_program_verified":
                        (rr.get("plane_face") or {})
                        .get("program_verified_all_planes")})
    armed_events.sort(key=lambda r: (r["variant"], r["seed"],
                                     r["ring_index"]))
    n_events = len(armed_events)
    n_below = sum(1 for e in armed_events
                  if e["armed_err_mV"] is not None
                  and e["armed_err_mV"] < ERR_MARGIN)
    n_worse = sum(1 for e in armed_events
                  if e["armed_err_mV"] is not None
                  and e["armed_err_mV"] > e["baseline_err_mV"])
    if n_events > 0 and n_below == n_events:
        branch = "REPAIR"
    elif n_below >= 1 and n_worse == 0:
        branch = "PARTIAL"
    else:
        branch = "NONE"
    c2_pass = True   # all three branches complete the gate (registered)
    print(f"  GATE-P2 repair: {n_events} armed events, errs below bar "
          f"{n_below}/{n_events}, worse than baseline {n_worse} -> "
          f"{branch}")

    # ==================================================================
    # GATE-P3 (the identity clause): every NON-armed ring's err
    # bit-exact vs the replay (ring_err_mV, emitted, frontier, pass) —
    # the composition touches only the census-named boundary
    # admissions; the aper member's rings included.  The armed sites
    # are the (member, ring) cells at rings 2-6 (the membership face
    # and window extension are pair-shared geometry); ring 1 — where
    # exp212's census has excl = [] — is the only non-armed ring.
    # ==================================================================
    identity = []
    n_identity_mism = 0
    n_nonarmed = 0
    for var in VARS:
        ra_list = fresh155["disciplined_junction"][FAM][
            "members"][var]["runs"]
        rb_list = armed[FAM]["members"][var]["runs"]
        assert len(ra_list) == len(rb_list)
        for ra, rb in zip(ra_list, rb_list):
            assert ra["seed"] == rb["seed"]
            for x, y in zip(ra["rings"], rb["rings"]):
                armed_site = bool(x["ring_index"] in ARMED_RINGS)
                fields_exact = bool(
                    x.get("ring_err_mV") == y.get("ring_err_mV")
                    and x.get("emitted") == y.get("emitted")
                    and x.get("frontier") == y.get("frontier")
                    and x.get("pass") == y.get("pass"))
                if not armed_site:
                    n_nonarmed += 1
                    n_identity_mism += int(not fields_exact)
                identity.append({
                    "variant": var, "seed": ra["seed"],
                    "ring": x["ring_index"],
                    "armed_site": armed_site,
                    "replay_err_mV": x.get("ring_err_mV"),
                    "armed_err_mV": y.get("ring_err_mV"),
                    "bit_exact": fields_exact})
    c3_pass = bool(n_identity_mism == 0 and n_nonarmed == 6)
    print(f"  GATE-P3 identity: {len(identity)} ring-events, "
          f"{n_nonarmed} outside the armed sites, "
          f"{n_identity_mism} identity mismatches")

    # ---- GATE-P4 (hygiene) ------------------------------------------
    def n_rej_cone(cone: dict) -> int:
        bad = 0
        for m in cone["members"]:
            for run in cone["members"][m]["runs"]:
                bad += sum(1 for x in run["rings"]
                           if not x.get("read_ok", True))
        return bad

    n_rej = (n_rej_cone(fresh155["disciplined_junction"][FAM])
             + n_rej_cone(armed[FAM]))

    def errs_of(cone: dict) -> list:
        return [x.get("ring_err_mV") for m in cone["members"]
                for run in cone["members"][m]["runs"]
                for x in run["rings"] if x.get("read_ok")]

    errs_all = (errs_of(fresh155["disciplined_junction"][FAM])
                + errs_of(armed[FAM]))
    all_finite = all(e is not None and np.isfinite(e) for e in errs_all)
    floors_restored = all(m.NEURAL_SPEC_MIN == v for m, v in
                          zip(PIN_MODS, FLOORS_ORIGINAL))
    c4_pass = bool(n_rej == 0 and all_finite and floors_restored
                   and census_match)
    print(f"  GATE-P4 hygiene: rejections {n_rej}, all errs finite "
          f"{all_finite}, floors restored to originals "
          f"{floors_restored}, admission sets == exp212's deposited "
          f"census {census_match}")

    verdict = (f"{sum(int(x) for x in (c1_pass, c2_pass, c3_pass,
                                       c4_pass))}/4 gates "
               f"(P1 P2 P3 P4) | repair {branch}")
    print(f"  === {verdict} ===")

    result = {
        "exp": "exp219_f1_composition_armed",
        "claim": (
            "THE F1 COMPOSITION ARMED (L187's registered next): "
            "exp212's census sweep named the site where the composed "
            "rule's membership face can act for the first time — the "
            "JD-a fence bites at F1_zone_tail rings 2-6 (11 excluded "
            "cell-ring pairs, 5 of them canon-value boundary cells). "
            "The exp210 composed rule (the fence's boundary-aware "
            "exception + the plane-resolved read face) ARMED at F1: "
            "the boundary cells in the fence's exclusions are ADMITTED "
            "with the plane-resolved read face; everything else is "
            "exp155's disciplined protocol verbatim."),
        "pre_registered": {
            "gates_source": (
                "module docstring, committed before any run "
                "(pre-registration d52addd, batch 11; gates P1-P4 "
                "fixed there, each evaluated exactly once)"),
            "gates": [
                "GATE-P1 (the replay) exp155's F1 rows reproduce "
                "bit-exactly outside the armed sites (the disciplined "
                "battery's ring errs at the deposit's rounding; the "
                "walk's committed SET identical)",
                "GATE-P2 (the composition) per-ring errs for the "
                "armed F1 events, all seeds; the branch named: "
                "REPAIR (every armed ring err < 6.0 mV), PARTIAL "
                "(>= 1 < 6.0 and none worse than the disciplined "
                "baseline at that ring), NONE",
                "GATE-P3 (the identity clause) every NON-armed ring's "
                "err bit-exact vs the replay (the composition touches "
                "only the census-named boundary admissions; the aper "
                "member's rings included)",
                "GATE-P4 (hygiene) zero rejections; all finite; the "
                "-35.0 pin save/restore asserted; the admission sets "
                "asserted == exp212's deposited census (the boundary "
                "cells only)"],
            "composed_rule": (
                "JD-a' = the flip-quiet reach F_q of exp155's JD-a, "
                "EXCEPT that at the armed sites a fence-excluded node "
                "which sits on a canon-value boundary in the target "
                "plan is ADMITTED to the frontier with the "
                "plane-resolved read face (exp158's machinery via "
                "exp210) instead of exclusion; the non-boundary "
                "exclusions KEEP the fence; everything else exp155's "
                "protocol verbatim. Zero knobs."),
            "arm_scope": (
                "PRE-NAMED from exp212's deposited census (zero "
                "re-derivation): F1_zone_tail rings 2-6, excl [74] at "
                "ring 2, [74] at ring 3, [66, 74] at ring 4, "
                "[63, 66, 74] at ring 5, [61, 63, 66, 74] at ring 6 — "
                "the canon-value boundary cells among them admitted "
                "(cell 74 per ring; the non-boundary exclusions "
                "66/63/61 keep the fence), member per (the face; the "
                "walk geometry is pair-shared), seeds (1, 2, 3). The "
                "walk's committed SET continues from the QUIET C at "
                "every ring (exp155 verbatim) — the admitted cells are "
                "read, never walk-committed"),
        },
        "sections": {
            "replay": {"rows_checked": replay["rows_checked"],
                       "mismatches": replay["mismatches"],
                       "committed_set_mismatches":
                           replay["committed_set_mismatches"],
                       "fresh155_verdict": fresh_verdict,
                       "scratch_deposit": fresh155_path},
            "exp212_scope": {
                "excl_deposited": {str(k): excl212[k]
                                   for k in sorted(excl212)},
                "admitted_boundary_deposited":
                    {str(k): admit212[k] for k in sorted(admit212)},
                "prenamed_asserts_pass": True},
            "plane_geometry": plane_geom,
            "armed_site": {"family": FAM, "member": "per",
                           "rings": list(ARMED_RINGS),
                           "seeds": list(E155.SEEDS)},
            "membership_census": {
                "disclosure": (
                    "per-ring census of the JD-a membership face on "
                    "this substrate, recomputed by the armed run "
                    "(excl = raw_F - quiet_F at every ring) and "
                    "checked against exp212's deposited census at "
                    "GATE-P4; the admission sets are the deposited "
                    "canon-boundary cells ONLY"),
                "census": census.get("rings", []),
                "armed_rings": census.get("armed_rings"),
                "n_excl_at_armed": census.get("n_excl_at_armed"),
                "admitted_at_armed": census.get("admitted_at_armed"),
                "matches_exp212_deposit": census_match},
            "composition_delta": {
                "disclosure": (
                    "armed vs replay channel geometry per ring: the "
                    "frontier/window deltas must be EXACTLY the "
                    "census-named admissions (disclosed, not gated; "
                    "the identity clause binds the errs)"),
                "rings": delta_rows},
            "boundary_plane_cells": {
                "description": (
                    "per armed ring: window cells (i<j) with a nonzero "
                    "averaged entry or a JD-zeroed crossing edge whose "
                    "endpoints sit on different canon planes — removed "
                    "from every plane's decode by the face"),
                "rings": boundary_plane_cells},
            "armed_events": armed_events,
            "face_log": face_log,
            "armed_protocol": armed,
            "identity_table": identity,
        },
        "gates": {
            "P1": {"pass": c1_pass,
                   "rows_checked": replay["rows_checked"],
                   "mismatches": len(replay["mismatches"]),
                   "committed_set_mismatches":
                       len(replay["committed_set_mismatches"])},
            "P2": {"pass": c2_pass, "branch": branch,
                   "n_armed_events": n_events,
                   "n_below_bar": n_below,
                   "n_worse_than_baseline": n_worse,
                   "armed_errs_mV": {
                       f"{e['variant']}|s{e['seed']}|r"
                       f"{e['ring_index']}": e["armed_err_mV"]
                       for e in armed_events},
                   "disciplined_baseline_mV": {
                       f"{e['variant']}|s{e['seed']}|r"
                       f"{e['ring_index']}": e["baseline_err_mV"]
                       for e in armed_events},
                   "membership_face_armed": {
                       "n_excl_at_armed":
                           census.get("n_excl_at_armed"),
                       "admitted_at_armed":
                           census.get("admitted_at_armed")}},
            "P3": {"pass": c3_pass,
                   "n_ring_events": len(identity),
                   "n_non_armed_events": n_nonarmed,
                   "identity_mismatches_outside_site":
                       n_identity_mism},
            "P4": {"pass": c4_pass, "rejections": n_rej,
                   "all_errs_finite": bool(all_finite),
                   "floors_restored": bool(floors_restored),
                   "admission_census_match": bool(census_match)}},
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
