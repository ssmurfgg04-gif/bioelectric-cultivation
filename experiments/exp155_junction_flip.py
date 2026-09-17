#!/usr/bin/env python3
"""exp155 — THE JUNCTION-FLIP FRONTIER DISCIPLINE (repair of the L134
horizon falsification).

Workstream T. Foundation: exp152 L134 (4/4 — the temporal cone self-
expands on flip-clock media; HORIZON FALSIFICATION deposited: the cone's
frontier walks THROUGH flip edges, and on junction-flip geometry (a
carrier flip edge crossing C<->F) the temporal cone breaks exactly at
the flip-entry ring — F1 ring-2 err 23.1 mV, F3 ring-1 errs 36.9-46.5 mV
per / 7.1-7.3 mV aper). L134's REGISTERED NEXT (a) names this experiment
verbatim: "junction-flip frontier discipline — the C<->F flip-coupled
frontier node is dragged by the -b/2 time-average coupling at the
flip-entry ring; repair = pre-registered window or frontier rule that
holds the junction node (which one is the open question)".

PREMISE (deposited at L134; re-asserted in-instrument BEFORE any run,
from the deposited horizon-control pass flags vs the recomputed walk
geometry): on exp152's horizon controls the break tracks the
C<->F-crossing flip edge EXACTLY — every deposited breaking ring has
>= 1 crossing chord in its window, every fully-passing ring has none
(F1: crossings at rings 2/4/5/6 = the breaking rings, none at the
passing rings 1/3; F3: one crossing at ring 1 = the breaking ring, none
at the passing rings 2-6; F2: no crossing ever = the all-passing
operating point). The drag is a JUNCTION property, not a flip property:
C-interior flip edges are in-window on every deposited passing F2/F3
ring.

THIS EXPERIMENT: the junction-flip frontier discipline (JD) — ONE rule,
zero knobs, pre-registered here before any run — and its causal test on
the junction battery {F1_zone_tail, F3_canon_boundary} x FlipPairMedium
at b=1792 (exp152's deposited break geometry, chord_seed=7).

THE JUNCTION-FLIP DISCIPLINE (JD; one rule — NO FLIP-ACTIVE EDGE MAY SIT
ON THE CONE'S C<->F JUNCTION — with two faces, both derived from the
single exclusion; every other protocol constant is exp152 verbatim):
  JD-a (membership face) the ring-k frontier is the FLIP-QUIET reach
      F_q(C) = {j not in C : exists i in C, |W_quiet[i,j]| > 0}, where
      W_quiet = the pair-identical time-average W_avg with every carrier
      chord edge zeroed — a node whose only committed-adjacency is a
      flip edge is not emitted to this ring (the chord-jump frontier is
      fenced; such nodes enter later through the backbone, with a quiet
      junction, or not at all within the horizon — the deposited
      coverage cost of the discipline).
  JD-b (window face) the read window = exp152's P5' temporal window
      (induced subgraph on C u F_q, closed-world n x n, beyond-frontier
      zeroed) with every carrier chord edge crossing C<->F zeroed in
      every frame — C-interior and F-interior flip edges stay in-window
      (F2's deposited operating point is untouched by construction).
  "Carrier chord" = the construction's own a-priori chord set (exp148
  chord_set; the medium's identity object). No threshold, no scale, no
  lookup exists in the rule. The committed SET walk stays support-driven
  (on W_quiet — pair-identical, seed-independent); P2 (plan scorer-only
  on W_avg), P3 (canon-head seed on W_avg), P5' (temporal read TC1-TC3
  VERBATIM on the window), P6 (emission = the read's own final V) and
  P7 (R=6, SEEDS=(1,2,3)) are exp152 VERBATIM. On a junction-flip-free
  family the discipline is VACUOUS by construction: F_q == P4's F and
  the JD-b zero set is empty at every ring (asserted on F2) — the
  disciplined protocol REDUCES to exp152's protocol there.

INSTRUMENT VALIDITY PRE-CHECKS (geometry only, run before the registered
run; no read/execute/gate physics): (i) the OOD chord placement
(chord_seed=11 — a priori, the first seed distinct from the deposited
PROBE_SEED=7) actually produces junction-flip geometry on both horizon
families: F1@11 has 5 crossing ring-events and F3@11 has 3 within the
6-ring P4 walk (verified pre-registration); (ii) pair time-averages
bitwise equal to the analytic W_avg per instance (exp152's instrument
asserts, mirrored).

PRE-REGISTERED GATES (fixed before any run):

  GATE-J1 (junction repair, primary) the disciplined protocol on the
     deposited junction battery {F1, F3} x {per, aper} x SEEDS=(1,2,3)
     at b=1792, chord_seed=7: a cell passes iff it expands >= 3 of the 6
     rings with EVERY expanded ring err < 6.0 mV (ERR_BAR, exp151/152's
     cell convention; ring err = RMS(emitted[frontier] -
     T_plan[frontier])). J1 passes iff ALL 12 cells pass — the geometry
     that broke at 23.1 (F1-per ring 2) and 36.9-46.5 mV (F3-per ring 1)
     must be repaired completely on the deposited battery. Per-ring
     disciplined errs are deposited side-by-side with the undisciplined
     arm's (J3) as the repair table.
  GATE-J2 (bit-exact non-junction superset) on the deposited
     non-junction battery F2_zone_head (all 6 flip edges C-interior from
     ring 1 — asserted), the disciplined protocol reproduces exp152's
     deposited temporal_frontier arm BIT-EXACTLY: per (member, seed,
     ring) — frontier, emitted (rounded), plan, ring_err_mV, read_ok,
     program_verified, pass; run-level rings_expanded / rings_passed /
     exhausted / cell_pass / attributed_from / committed (nodes+values);
     channel log — n_window_nodes, n_window_edges, window_sha256_16,
     proj_bitident_across_pair, fc_cross_delta_max, per-member fc stats,
     emitted_delta_max_by_seed — ZERO mismatches; AND the vacuity chain
     is structural (quiet walk == P4 walk and JD-b zero set empty at
     every ring, asserted). The discipline must cost nothing where
     there is no junction flip.
  GATE-J3 (causality — the confirming negative) removing the discipline
     (P4 membership + full induced window: exp152's run_flip_cone
     imported VERBATIM — the identical code path) on the same junction
     battery reproduces exp152's deposited horizon controls BIT-EXACTLY:
     every deposited (family, member, seed, ring) record's ring_err_mV
     and pass flag reproduced (deterministic re-run; 69 deposited ring
     records), and every deposited break ring still reads err >= 6.0 mV
     — the same geometry re-breaks at the same rings with the same errs
     when the discipline is lifted, so the J1 repair is attributable to
     the discipline alone.
  GATE-J4 (cross-substrate survival, one OOD class) the OOD class is
     the chord-placement axis at fixed dose/schedule construction:
     chord_seed=11 (a priori; b=1792, T=2400, c=1200, default schedule
     seeds; families F1/F3 — unseen junction geometries, verified
     junction-flip in the pre-check). The disciplined protocol runs
     UNCHANGED (zero knobs); J4 passes iff >= 8 of the 12 cells pass
     the J1 cell test (2/3 majority — the line's
     majority-of-instances convention).

REFUTATION BRANCHES (pre-registered): a J1 failure is deposited per
(family, member, seed, ring) with emitted vs plan, the disciplined
window content (which chords remained in-window) and the undisciplined
err at the same ring; a J2 mismatch per field; a J4 failure per cell.
A J1 failure WITH a clean J3 localizes the repair as insufficient — the
junction drag is then not the sole break channel (F3's ring-1 window
keeps its F-interior flip edge (11,14) and four C-interior chords under
JD, so a residual F3 ring-1 break would name the F-interior flip edges
as the next suspect).

DEPOSIT: results/exp155_junction_flip.json

INSTRUMENT NOTE (disclosed, pre-registered-run): the --smoke instrument
subset (F3@7, seed 1 — window machinery validation: outside-zero and
crossing-zero sweeps OK, quiet-walk asserts OK) ran before the
registered run and exposed two instrument-only bugs, both repaired
before registration (carrier_substrate tuple unpacking; walk-map loop
bounds) — no gate, bar, rule or constant was touched. The smoke
necessarily also showed F3 ring-1's disciplined errs (per 37.9 / aper
4.9 mV): the pre-registered refutation branch above names exactly this
residual (the F-interior flip edge), the gates below were NOT modified
after the observation, and one POST-HOC DIAGNOSTIC arm (JD zero set
widened by the F-interior chords; explicitly labeled not-gated in the
deposit) was added to test that named channel causally.

RUN:
  python3 -m experiments.exp155_junction_flip            # registered
  python3 -m experiments.exp155_junction_flip --smoke    # instrument subset
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp142_sign_read import SEEDS, STAR_OP, execute_signed
from experiments.exp145_phase_read import (
    project_phase_native, warnings_as_errors,
)
from experiments.exp148_temporal_read import (
    C_BATTERY, FlipPairMedium, FrameSeq, T_BATTERY, chord_set,
    flip_clock_matrix,
)
from experiments.exp151_self_expansion import (
    ERR_BAR, RINGS as RINGS_P7, carrier_substrate, frontier_of, plan_of,
    seed_cone,
)
from experiments.exp152_temporal_frontier import (
    B_DOSE, c_sequence, run_flip_cone,
)
from experiments.exp94_multizone_scale import MULTI

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp155_junction_flip.json")
EXP152_DEPOSIT = os.path.join(ROOT, "results", "exp152_temporal_frontier.json")

# ---------------- protocol constants (zero knobs; logged once) --------
FAMS_JUNCTION = ("F1_zone_tail", "F3_canon_boundary")
FAM_NONJUNCTION = "F2_zone_head"
CHORD_SEED_DEPOSITED = 7        # exp148 PROBE_SEED (the deposited geometry)
CHORD_SEED_OOD = 11             # a priori (pre-registered above)
RINGS = RINGS_P7                # P7: 6 rings (exp151/exp152 verbatim)
J4_MIN_CELLS = 8                # of 12 (2/3 majority)
J2_RUN_FIELDS = ("seed", "rings_expanded", "rings_passed", "exhausted",
                 "cell_pass", "attributed_from", "committed")
J2_RING_FIELDS = ("ring_expanded", "exhausted", "read_ok",
                  "program_verified", "ring_index", "frontier", "emitted",
                  "plan", "ring_err_mV", "pass")
J2_CHAN_FIELDS = ("ring_index", "frontier", "n_window_nodes",
                  "n_window_edges", "window_sha256_16",
                  "proj_bitident_across_pair", "fc_cross_delta_max",
                  "members", "emitted_delta_max_by_seed")
DISCIPLINE_RULE = (
    "JUNCTION-FLIP EXCLUSION (one rule, zero knobs): no flip-active edge "
    "may sit on the cone's C<->F junction. (JD-a membership) the ring-k "
    "frontier is F_q(C) = {j not in C : exists i in C, |W_quiet[i,j]| > 0} "
    "with W_quiet = W_avg and every carrier chord edge zeroed — a node "
    "whose only committed-adjacency is a flip edge is not emitted to this "
    "ring; (JD-b window) the read window = induced subgraph on C u F_q "
    "with every carrier chord edge crossing C<->F zeroed in every frame; "
    "C-interior and F-interior flip edges stay in-window. Carrier chords "
    "= the construction's a-priori chord set (exp148 chord_set); the "
    "committed SET walk stays support-driven (on W_quiet); P2/P3/P5'/P6/"
    "P7 exp152 verbatim.")


# ---------------- P1' media (chord_seed parameterized) ----------------
def averaged_substrate_cs(family: str, b: float,
                          chord_seed: int) -> tuple[np.ndarray, list]:
    """The pair-identical time-average: ring (1.0) + chords at
    -b*(c/T) (each chord edge ON in exactly c of T frames)."""
    A, chords = chord_set(100, family, chord_seed)
    W = A.copy()
    for (i, j) in chords:
        W[i, j] = W[j, i] = -b * (C_BATTERY / T_BATTERY)
    return W, chords


def pair_members_cs(family: str, b: float,
                    chord_seed: int) -> dict[str, FlipPairMedium]:
    """exp148's adversarial pair VERBATIM (shared schedule seed base)."""
    return {"per": FlipPairMedium(b, family, "per", chord_seed=chord_seed),
            "aper": FlipPairMedium(b, family, "aper",
                                   chord_seed=chord_seed)}


# ---------------- JD-a: the flip-quiet walk ---------------------------
def quiet_c_sequence(W_avg: np.ndarray, chords: list,
                     max_rings: int) -> tuple[list[set], list[list]]:
    """JD-a — the committed-SET walk through flip-quiet edges only:
    F_q(C) = {j not in C : exists i in C, |W_quiet[i,j]| > 0}. Seed =
    exp151/exp152's canon-head set on W_avg (P3 verbatim). Asserts the
    quiet reach is a subset of P4's reach at every ring."""
    Wq = W_avg.copy()
    for (i, j) in chords:
        Wq[i, j] = Wq[j, i] = 0.0
    C = set(seed_cone(W_avg))
    seq, frontiers = [set(C)], []
    for _ in range(max_rings):
        F = frontier_of(C, Wq)
        if not F:
            break
        assert set(F) <= set(frontier_of(C, W_avg)), \
            "quiet reach escaped P4 reach"
        frontiers.append(F)
        C = C | set(F)
        seq.append(set(C))
    return seq, frontiers


def crossing_chords(chords: list, C: set, F: list) -> list:
    """The flip-active junction edge set X(C): carrier chords with one
    endpoint in the committed set and one in the frontier."""
    return [(i, j) for (i, j) in chords
            if (i in C and j in F) or (j in C and i in F)]


# ---------------- JD-b: the quiet-junction window ---------------------
class WindowQuietMedium:
    """JD-b — exp152's P5' temporal window (induced subgraph on C u F_q,
    closed-world n x n) with the crossing chord entries zeroed in every
    frame. C-interior/F-interior flip edges stay in-window. Carries
    exp151's S4 window contract (kind='window', snapshots() -> FrameSeq).
    The mask IS the quiet-junction invariant (analytic); ring-1 frames
    are additionally swept (belt and braces, exp152's convention)."""

    kind = "window"

    def __init__(self, member, win_nodes: set[int], zero_pairs: list):
        n = member.A.shape[0]
        self.member, self.n, self.win_nodes = member, n, set(win_nodes)
        self.T = member.T
        self.zero_pairs = list(zero_pairs)
        mask = np.zeros((n, n))
        idx = np.array(sorted(self.win_nodes))
        mask[np.ix_(idx, idx)] = 1.0
        for (i, j) in self.zero_pairs:
            assert mask[i, j] == 1.0, "crossing edge outside C u F_q"
            mask[i, j] = mask[j, i] = 0.0
        self.mask = mask
        self._outside = np.ones((n, n), dtype=bool)
        self._outside[np.ix_(idx, idx)] = False

    def snapshots(self) -> FrameSeq:
        return FrameSeq(self._gen_frames, self.T)

    def _gen_frames(self):
        mask = self.mask
        for frame in self.member.snapshots():
            yield frame * mask

    def sweep_assert(self) -> dict:
        """Instrument validation: every frame zero outside C u F_q AND
        at every crossing entry."""
        worst_out, worst_x = 0.0, 0.0
        for frame in self.snapshots():
            worst_out = max(worst_out,
                            float(np.max(np.abs(frame[self._outside]))))
            if self.zero_pairs:
                zx = np.array([abs(frame[i, j]) for (i, j)
                               in self.zero_pairs] +
                              [abs(frame[j, i]) for (i, j)
                               in self.zero_pairs])
                worst_x = max(worst_x, float(np.max(zx)))
        return {"outside_zero_max": worst_out,
                "crossing_zero_max": worst_x,
                "ok": bool(worst_out == 0.0 and worst_x == 0.0)}


# ---------------- the disciplined cone (P5'/P6/P7 verbatim) -----------
def run_quiet_cone(members: dict, W_avg: np.ndarray, chords: list,
                   T_plan: np.ndarray, seeds: list[int],
                   sweep_ring1: bool = False,
                   zero_ff: bool = False) -> dict:
    """JD — the disciplined temporal-frontier cone.

    Quiet walk (JD-a), quiet-junction windows (JD-b), temporal read
    TC1-TC3 verbatim, emission = the read's own final V (P6). When the
    window sequence is bitwise pair-identical (quiet AND flip-free),
    ONE deterministic cone is run and attributed to both members PER
    RING (inputs bitwise-asserted) — exp152's attribution, materialized
    at ring level.

    zero_ff=False (default) is the PRE-REGISTERED arm. zero_ff=True is
    the POST-HOC DIAGNOSTIC arm only (labeled as such in the deposit;
    not gated): the window's zero set additionally takes F-interior
    carrier chords (both endpoints in the frontier) — the residual
    channel the pre-registered refutation branch names."""
    seq, frontiers = quiet_c_sequence(W_avg, chords, RINGS)
    names = list(members)
    runs = {m: {s: {"rings": [], "active": True, "committed": {},
                    "rings_expanded": 0}
                for s in seeds} for m in names}
    chan_log, sweep = [], None
    for k, F in enumerate(frontiers, 1):
        win, C_prev = seq[k], seq[k - 1]
        crossing = crossing_chords(chords, C_prev, F)
        if zero_ff:
            ff = [(i, j) for (i, j) in chords
                  if i in F and j in F
                  and not (i in C_prev or j in C_prev)]
            crossing = crossing + [e for e in ff if e not in crossing]
        wms = {m: WindowQuietMedium(members[m], win, crossing)
               for m in names}
        if sweep_ring1 and k == 1:
            sweep = {m: wms[m].sweep_assert() for m in names}
        projs, Fcs = {}, {}
        for m in names:
            with warnings_as_errors():
                projs[m] = project_phase_native(wms[m])
            Fcs[m] = flip_clock_matrix(wms[m])
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
                    np.ascontiguousarray(A0).tobytes()).hexdigest()[:16],
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
            A_ext = A + Fcs[m]           # TC2 (temporal read, verbatim)
            for s in seeds:
                st = runs[m][s]
                if not st["active"]:
                    continue
                try:
                    with warnings_as_errors():
                        out = execute_signed(MULTI, A_ext, s,
                                             op=STAR_OP,
                                             return_state=True)
                    V = np.asarray(out["final_state"]["V"], dtype=float)
                    emitted = V[F]
                    err = float(np.sqrt(np.mean(
                        (emitted - T_plan[F]) ** 2)))
                    rec = {"ring_expanded": True, "exhausted": False,
                           "read_ok": True,
                           "program_verified":
                               bool(out.get("program_verified", False)),
                           "ring_index": k,
                           "frontier": [int(j) for j in F],
                           "emitted": [round(float(x), 3)
                                       for x in emitted],
                           "plan": [round(float(x), 3)
                                    for x in T_plan[F]],
                           "ring_err_mV": round(err, 3),
                           "attributed_from": None}
                    rec["pass"] = bool(np.isfinite(err)
                                       and err < ERR_BAR)
                    st["rings"].append(rec)
                    st["rings_expanded"] += 1
                    for j, v in zip(F, emitted):
                        st["committed"][int(j)] = float(v)
                    emitted_by.setdefault(m, {})[s] = emitted
                except Exception as e:            # zero-rejection hygiene
                    st["rings"].append({
                        "ring_expanded": True, "exhausted": False,
                        "read_ok": False, "ring_index": k,
                        "rejection":
                            f"{type(e).__name__}: {e}"[:200],
                        "attributed_from": None, "pass": False})
                    st["active"] = False
        if bitident and len(run_members) == 1:
            # per-ring attribution: the ONE deterministic cone IS both
            # members' cone (inputs bitwise-asserted above).
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
                        for j, v in zip(src["frontier"], src["emitted"]):
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
    # ---- finalize per (member, seed) cells (exp151/exp152 form) -----
    out_members = {}
    for m in names:
        rlist = []
        for s in seeds:
            st = runs[m][s]
            expanded = [x for x in st["rings"] if x.get("read_ok")]
            n_pass = sum(1 for x in expanded if x.get("pass"))
            cell = bool(len(expanded) >= 3 and n_pass == len(expanded))
            committed_vec = None
            if st["committed"]:
                nodes = sorted(st["committed"])
                committed_vec = {"nodes": nodes,
                                 "values": [round(st["committed"][n], 3)
                                            for n in nodes]}
            n_attr = sum(1 for x in st["rings"]
                         if x.get("attributed_from"))
            rlist.append({"seed": s,
                          "rings_expanded": len(expanded),
                          "rings_passed": n_pass,
                          "exhausted": bool(
                              st["rings"] and
                              st["rings"][-1].get("exhausted"))
                          or len(frontiers) < RINGS,
                          "cell_pass": cell,
                          "attributed_from": (names[0] if
                                              m != names[0] and
                                              n_attr > 0 else None),
                          "committed": committed_vec,
                          "rings": st["rings"]})
        out_members[m] = {"runs": rlist}
    return {"members": out_members, "ring_channel_log": chan_log,
            "sweep_ring1": sweep, "n_frontier_walk": len(frontiers)}


# ---------------- comparisons -----------------------------------------
def compare_f2_arm(mine: dict, dep: dict) -> list:
    """J2 — field-by-field comparison against exp152's deposited F2
    temporal-frontier arm (bit-exact superset requirement)."""
    mismatches = []

    def mm(kind, **kw):
        mismatches.append(dict(kind=kind, **kw))

    for m in ("per", "aper"):
        ra_list = dep["members"][m]["runs"]
        rb_list = mine["members"][m]["runs"]
        if len(ra_list) != len(rb_list):
            mm("n_runs", member=m, got=len(rb_list),
               want=len(ra_list))
            continue
        for ra, rb in zip(ra_list, rb_list):
            for f in J2_RUN_FIELDS:
                if ra.get(f) != rb.get(f):
                    mm("run_field", member=m, seed=ra.get("seed"),
                       field=f, got=rb.get(f), want=ra.get(f))
            if len(ra["rings"]) != len(rb["rings"]):
                mm("n_rings", member=m, seed=ra.get("seed"),
                   got=len(rb["rings"]), want=len(ra["rings"]))
                continue
            for x, y in zip(ra["rings"], rb["rings"]):
                for f in J2_RING_FIELDS:
                    if x.get(f) != y.get(f):
                        mm("ring_field", member=m,
                           seed=ra.get("seed"), ring=x.get("ring_index"),
                           field=f, got=y.get(f), want=x.get(f))
    da = dep["ring_channel_log"]
    db = mine["ring_channel_log"]
    if len(da) != len(db):
        mm("n_chanlog", got=len(db), want=len(da))
    else:
        for x, y in zip(da, db):
            for f in J2_CHAN_FIELDS:
                if f == "members":
                    for mm_ in ("per", "aper"):
                        if x["members"][mm_] != y["members"][mm_]:
                            mm("chan_fc_stats", ring=x["ring_index"],
                               member=mm_, got=y["members"][mm_],
                               want=x["members"][mm_])
                elif x.get(f) != y.get(f):
                    mm("chan_field", ring=x.get("ring_index"), field=f,
                       got=y.get(f), want=x.get(f))
    return mismatches


def compare_j3_reproduction(mine: dict, dep: dict) -> dict:
    """J3 — the undisciplined re-run must reproduce exp152's deposited
    horizon controls bit-exactly (ring_err_mV and pass per deposited
    record), and every deposited break ring must still break."""
    mismatches, n_records, n_break, break_ok = [], 0, 0, True
    for m in ("per", "aper"):
        ra_list = dep["members"][m]["runs"]
        rb_list = mine["members"][m]["runs"]
        if len(ra_list) != len(rb_list):
            mismatches.append({"member": m, "field": "n_runs",
                               "got": len(rb_list),
                               "want": len(ra_list)})
            continue
        for ra, rb in zip(ra_list, rb_list):
            if ra["seed"] != rb["seed"]:
                mismatches.append({"member": m, "field": "seed",
                                   "got": rb["seed"],
                                   "want": ra["seed"]})
                continue
            if ra["rings_expanded"] != rb["rings_expanded"]:
                mismatches.append({"member": m, "seed": ra["seed"],
                                   "field": "rings_expanded",
                                   "got": rb["rings_expanded"],
                                   "want": ra["rings_expanded"]})
            for x, y in zip(ra["rings"], rb["rings"]):
                n_records += 1
                if (x.get("ring_err_mV") != y.get("ring_err_mV")
                        or x.get("pass") != y.get("pass")):
                    mismatches.append({"member": m, "seed": ra["seed"],
                                       "ring": x.get("ring_index"),
                                       "field": "ring_err_mV/pass",
                                       "got": [y.get("ring_err_mV"),
                                               y.get("pass")],
                                       "want": [x.get("ring_err_mV"),
                                                x.get("pass")]})
                if x.get("pass") is False:
                    n_break += 1
                    got_err = y.get("ring_err_mV")
                    if got_err is None or got_err < ERR_BAR:
                        break_ok = False
    return {"n_records_compared": n_records, "n_break_rings": n_break,
            "break_rings_still_break": bool(break_ok),
            "mismatches": mismatches,
            "match": bool(len(mismatches) == 0 and break_ok
                          and n_records > 0)}


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    out: dict = {
        "experiment": "exp155_junction_flip",
        "protocol_constants": {
            "b_dose": B_DOSE, "T": T_BATTERY, "c": C_BATTERY,
            "junction_families": list(FAMS_JUNCTION),
            "nonjunction_family": FAM_NONJUNCTION,
            "chord_seed_deposited": CHORD_SEED_DEPOSITED,
            "chord_seed_ood": CHORD_SEED_OOD,
            "rings": RINGS, "err_bar": ERR_BAR,
            "executor_seeds": list(SEEDS),
            "j1_cell_rule": ("expands >= 3 of 6 rings with EVERY "
                             "expanded ring err < 6.0 mV; J1 = all 12 "
                             "junction cells"),
            "j4_rule": (">= 8 of 12 OOD cells pass the J1 cell test "
                        "(2/3 majority)"),
            "discipline_rule": DISCIPLINE_RULE},
        "smoke": bool(args.smoke)}
    seeds = [SEEDS[0]] if args.smoke else list(SEEDS)
    fams_j = [FAMS_JUNCTION[1]] if args.smoke else list(FAMS_JUNCTION)

    def build(fam: str, cs: int):
        W, chords = averaged_substrate_cs(fam, B_DOSE, cs)
        members = pair_members_cs(fam, B_DOSE, cs)
        T_plan = plan_of(W)
        return W, chords, members, T_plan

    # ---------- instrument: instances, walks, premise, vacuity -------
    instrument: dict = {}
    inst: dict = {}
    inst_keys = [(fam, CHORD_SEED_DEPOSITED) for fam in fams_j]
    if not args.smoke:
        inst_keys += [(FAM_NONJUNCTION, CHORD_SEED_DEPOSITED),
                      *[(fam, CHORD_SEED_OOD) for fam in FAMS_JUNCTION]]
    for fam, cs in inst_keys:
        W, chords, members, T_plan = build(fam, cs)
        means = {}
        for m in members:
            with warnings_as_errors():
                means[m] = project_phase_native(members[m])[0]
        bit_ok = all(np.array_equal(means["per"], means[m])
                     for m in means)
        analytic_ok = np.array_equal(means["per"], W)
        W_car, _ = carrier_substrate(fam)
        plan_cont = bool(np.array_equal(T_plan, plan_of(W_car)))
        seq_p4, front_p4 = c_sequence(W, RINGS)
        seq_q, front_q = quiet_c_sequence(W, chords, RINGS)
        p4_map, quiet_map, n_cross_events = [], [], 0
        f2_vacuous = True
        assert len(seq_q) == len(seq_p4), \
            "quiet walk exhausted before the P4 walk"
        for k in range(1, len(seq_p4)):
            C_prev, F_p4 = seq_p4[k - 1], front_p4[k - 1]
            inside = [e for e, (i, j) in enumerate(chords)
                      if i in seq_p4[k] and j in seq_p4[k]]
            cross = crossing_chords(chords, C_prev, F_p4)
            n_cross_events += len(cross)
            p4_map.append({"ring": k, "frontier": [int(j) for j in F_p4],
                           "chords_inside": inside,
                           "crossing": [[int(i), int(j)]
                                        for (i, j) in cross]})
            F_q = front_q[k - 1]
            X = crossing_chords(chords, seq_q[k - 1], F_q)
            # JD-a structural guarantee: every quiet-frontier node has
            # an in-window flip-quiet (backbone) coupling from C.
            Wq = W.copy()
            for (i, j) in chords:
                Wq[i, j] = Wq[j, i] = 0.0
            for j in F_q:
                assert any(Wq[i, j] != 0.0 for i in seq_q[k - 1]), \
                    "quiet frontier node without quiet coupling"
            quiet_map.append({"ring": k,
                              "frontier_q": [int(j) for j in F_q],
                              "crossing_zeroed": [[int(i), int(j)]
                                                  for (i, j) in X]})
            if fam == FAM_NONJUNCTION:
                f2_vacuous &= ([int(j) for j in F_q] ==
                               [int(j) for j in F_p4] and len(X) == 0)
        entry = {
            "pair_timeavg_bitidentical": bool(bit_ok),
            "timeavg_bitwise_analytic_W_avg": bool(analytic_ok),
            "plan_continuity_with_carrier": plan_cont,
            "n_chords": len(chords),
            "chords": [[int(i), int(j)] for (i, j) in chords],
            "seed_set_size": len(seq_q[0]),
            "frontier_walk_rings": len(front_q),
            "p4_walk_map": p4_map, "quiet_walk_map": quiet_map,
            "n_p4_crossing_events": n_cross_events,
            "quiet_subset_of_p4": True}
        if fam == FAM_NONJUNCTION:
            entry["f2_vacuity_q_eq_p4_and_no_crossing"] = bool(f2_vacuous)
        if cs != CHORD_SEED_DEPOSITED:
            entry["ood_junction_flips_present"] = bool(n_cross_events >= 1)
        inst_key = f"{fam}@cs{cs}"
        instrument[inst_key] = entry
        inst[inst_key] = (W, chords, members, T_plan)
    out["instrument"] = instrument

    # deposited-break premise (crossing presence <-> deposited break)
    premise = {}
    if not args.smoke:
        with open(EXP152_DEPOSIT) as f:
            dep152 = json.load(f)
        for fam in FAMS_JUNCTION:
            dep_hc = dep152["horizon_controls"][fam]
            fail_by_ring = {}
            for m in dep_hc["members"]:
                for r in dep_hc["members"][m]["runs"]:
                    for ring in r["rings"]:
                        kk = ring["ring_index"]
                        fail_by_ring[kk] = fail_by_ring.get(kk, False) \
                            or (ring.get("pass") is False)
            p4_map = instrument[f"{fam}@cs{CHORD_SEED_DEPOSITED}"][
                "p4_walk_map"]
            ok = True
            for row in p4_map:
                has_cross = len(row["crossing"]) > 0
                ok &= (has_cross == bool(fail_by_ring.get(row["ring"],
                                                          False)))
            premise[fam] = {
                "crossing_iff_deposited_break": bool(ok),
                "deposited_fail_rings": sorted(kk for kk, v in
                                               fail_by_ring.items()
                                               if v)}
        out["deposited_break_premise"] = premise

    # ---------- J1: the disciplined junction arm ----------------------
    disc_junction = {}
    for fam in fams_j:
        W, chords, members, T_plan = inst[f"{fam}@cs{CHORD_SEED_DEPOSITED}"]
        disc_junction[fam] = run_quiet_cone(members, W, chords, T_plan,
                                            seeds, sweep_ring1=True)
    out["disciplined_junction"] = disc_junction

    if args.smoke:
        fam = FAMS_JUNCTION[1]
        runs = disc_junction[fam]["members"]
        out["smoke_checks"] = {
            "instrument": instrument[f"{fam}@cs{CHORD_SEED_DEPOSITED}"],
            "rings_expanded": {m: [r["rings_expanded"]
                                   for r in runs[m]["runs"]]
                               for m in runs},
            "ring_errs": {m: [r_["ring_err_mV"]
                              for r_ in runs[m]["runs"][0]["rings"]]
                          for m in runs},
            "sweep_ring1": disc_junction[fam]["sweep_ring1"]}
        out["runtime_s"] = round(time.time() - t0, 1)
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with open(OUT, "w") as f:
            json.dump(out, f, indent=1)
        print(f"smoke deposited -> {OUT}")
        return out

    # ---------- J2: the disciplined non-junction arm ------------------
    W, chords, members, T_plan = inst[
        f"{FAM_NONJUNCTION}@cs{CHORD_SEED_DEPOSITED}"]
    disc_f2 = run_quiet_cone(members, W, chords, T_plan, seeds)
    out["disciplined_nonjunction"] = {FAM_NONJUNCTION: disc_f2}
    j2_mismatches = compare_f2_arm(
        disc_f2, dep152["temporal_frontier"][FAM_NONJUNCTION])
    f2_vacuity = instrument[
        f"{FAM_NONJUNCTION}@cs{CHORD_SEED_DEPOSITED}"][
            "f2_vacuity_q_eq_p4_and_no_crossing"]
    # bonus consistency: on F3 the quiet walk == P4 walk, so only the
    # crossing ring's window differs from exp152's — rings 2-6 must be
    # bit-identical to the deposited horizon control (P6 log-only
    # committed values never enter the read input).
    f3_r26_exact = None
    dep_f3 = dep152["horizon_controls"]["F3_canon_boundary"]
    mine_f3 = disc_junction["F3_canon_boundary"]
    f3_r26 = []
    for m in ("per", "aper"):
        for ra, rb in zip(dep_f3["members"][m]["runs"],
                          mine_f3["members"][m]["runs"]):
            for x, y in zip(ra["rings"], rb["rings"]):
                if x["ring_index"] >= 2:
                    f3_r26.append(
                        x["ring_err_mV"] == y["ring_err_mV"]
                        and x["emitted"] == y["emitted"])
    if f3_r26:
        f3_r26_exact = bool(all(f3_r26))

    # ---------- J3: the undisciplined arm (exp152 verbatim) -----------
    undisc_junction = {}
    j3 = {}
    for fam in FAMS_JUNCTION:
        W, chords, members, T_plan = inst[
            f"{fam}@cs{CHORD_SEED_DEPOSITED}"]
        undisc_junction[fam] = run_flip_cone(members, W, T_plan, seeds,
                                             mode="temporal")
        j3[fam] = compare_j3_reproduction(
            undisc_junction[fam], dep152["horizon_controls"][fam])
    out["undisciplined_junction"] = undisc_junction
    out["j3_reproduction"] = j3

    # ---------- J4: the OOD chord-placement arm -----------------------
    ood = {}
    for fam in FAMS_JUNCTION:
        W, chords, members, T_plan = inst[f"{fam}@cs{CHORD_SEED_OOD}"]
        ood[fam] = run_quiet_cone(members, W, chords, T_plan, seeds)
    out["ood_disciplined"] = ood

    # ---------- the repair table (errs, disciplined vs undisciplined)
    repair = {}
    for fam in FAMS_JUNCTION:
        rows = []
        for m in ("per", "aper"):
            for ra, rb in zip(
                    undisc_junction[fam]["members"][m]["runs"],
                    disc_junction[fam]["members"][m]["runs"]):
                assert ra["seed"] == rb["seed"]
                und = {r["ring_index"]: r.get("ring_err_mV")
                       for r in ra["rings"]}
                dis = {r["ring_index"]: r.get("ring_err_mV")
                       for r in rb["rings"]}
                rows.append({
                    "member": m, "seed": ra["seed"],
                    "undisc_rings_expanded": ra["rings_expanded"],
                    "disc_rings_expanded": rb["rings_expanded"],
                    "undisc_cell_pass": ra["cell_pass"],
                    "disc_cell_pass": rb["cell_pass"],
                    "per_ring": [
                        {"ring": k, "undisc_err_mV": und.get(k),
                         "disc_err_mV": dis.get(k),
                         "disc_frontier":
                             next((r["frontier"] for r in rb["rings"]
                                   if r["ring_index"] == k), None)}
                        for k in range(1, RINGS + 1)]})
        repair[fam] = rows
    out["repair_table"] = repair

    # ---------- POST-HOC DIAGNOSTIC (not gated; labeled) --------------
    # The pre-registered refutation branch names the F-interior flip
    # edges as the residual suspect when F3 ring 1 stays broken under
    # JD. This arm widens the window zero set by exactly those edges
    # (crossing + F-interior chords; C-interior untouched) — if the per
    # err collapses, the F-interior channel is confirmed as the sole
    # residual break channel. Deposited as a diagnostic, never a gate.
    diag = {}
    for fam in FAMS_JUNCTION:
        W, chords, members, T_plan = inst[
            f"{fam}@cs{CHORD_SEED_DEPOSITED}"]
        diag[fam] = run_quiet_cone(members, W, chords, T_plan, seeds,
                                   zero_ff=True)
    out["post_hoc_diagnostic_zero_ff"] = {
        "label": ("post-hoc diagnostic, NOT gated, NOT pre-registered: "
                  "JD window zero set widened by F-interior carrier "
                  "chords; tests the refutation branch's named "
                  "residual channel"),
        "arms": diag}

    # ---------- gate evaluation --------------------------------------
    j1_cells = [r for fam in FAMS_JUNCTION
                for m in disc_junction[fam]["members"]
                for r in disc_junction[fam]["members"][m]["runs"]]
    j1_pass_n = sum(1 for r in j1_cells if r["cell_pass"])
    g1 = bool(j1_pass_n == len(j1_cells) and len(j1_cells) == 12)
    g2 = bool(len(j2_mismatches) == 0 and f2_vacuity)
    g3 = bool(all(j3[fam]["match"] for fam in FAMS_JUNCTION))
    j4_cells = [r for fam in FAMS_JUNCTION
                for m in ood[fam]["members"]
                for r in ood[fam]["members"][m]["runs"]]
    j4_pass_n = sum(1 for r in j4_cells if r["cell_pass"])
    g4 = bool(j4_pass_n >= J4_MIN_CELLS and len(j4_cells) == 12)
    out["gate_details"] = {
        "J1": {"cells_pass": j1_pass_n, "of": len(j1_cells),
               "per_family": {fam: sum(
                   1 for m in disc_junction[fam]["members"]
                   for r in disc_junction[fam]["members"][m]["runs"]
                   if r["cell_pass"]) for fam in FAMS_JUNCTION}},
        "J2": {"n_mismatches": len(j2_mismatches),
               "mismatches": j2_mismatches[:50],
               "f2_vacuity_structural": bool(f2_vacuity),
               "f3_rings2to6_bitexact_vs_deposit": f3_r26_exact},
        "J3": {fam: {k: v for k, v in j3[fam].items()
                     if k != "mismatches"} for fam in FAMS_JUNCTION},
        "J4": {"cells_pass": j4_pass_n, "of": len(j4_cells),
               "per_family": {fam: sum(
                   1 for m in ood[fam]["members"]
                   for r in ood[fam]["members"][m]["runs"]
                   if r["cell_pass"]) for fam in FAMS_JUNCTION}},
        "deposited_break_premise_holds": bool(all(
            premise[fam]["crossing_iff_deposited_break"]
            for fam in FAMS_JUNCTION))}
    out["gates"] = {
        "J1_junction_repair": {"pass": g1},
        "J2_bitexact_nonjunction_superset": {"pass": g2},
        "J3_causality_confirming_negative": {"pass": g3},
        "J4_ood_chord_placement_survival": {"pass": g4}}
    out["verdict"] = "{} / 4 gates PASS".format(
        sum(1 for g in out["gates"].values() if g["pass"]))
    out["runtime_s"] = round(time.time() - t0, 1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: out[k] for k in
                      ("verdict", "gates", "runtime_s") if k in out},
                     indent=1))
    print(f"deposited -> {OUT}")
    return out


if __name__ == "__main__":
    main()
