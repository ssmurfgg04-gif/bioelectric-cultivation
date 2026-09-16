#!/usr/bin/env python3
"""exp152 — THE TEMPORAL FRONTIER (self-expansion on flip-clock media).

Workstream T. Foundation: exp151 L131 (4/4 — the cone expands 6/6 rings
under its own read, the emission rule = the read's own final V at the
frontier) and exp148 L129 (the flip-clock channel TC1-TC3 carries the
flip SCHEDULE with bit-exact static supersets, 12/12 separation,
+0.12 mV fidelity cost). L131's REGISTERED NEXT (c) names this
experiment verbatim: "temporal-channel expansion (time-varying frontier
medium where the cone's read must carry the flip clock)".

THIS EXPERIMENT: the cone protocol P1-P8 (exp151, reused VERBATIM where
possible) runs on a TIME-VARYING frontier medium — the read window is
no longer a static matrix but a flip-clock snapshot sequence whose
identity semantics live ONLY in the flip schedule. The cone's read is
exp148's temporal read (A_ext = A + F, TC1-TC3 verbatim); the emission
rule is UNCHANGED (P6: next ring's committed value per frontier node =
the read's own final V there). Zero knobs — every constant below is
inherited from the deposited line or fixed a priori.

THE TEMPORAL FRONTIER MEDIUM (P1'): exp148's adversarial-pair
construction VERBATIM (FlipPairMedium): static ring backbone (1.0) +
exp148's carrier chord set (chord_set, PROBE_SEED=7, K_CHORDS=6) where
the 6 chord edges flip: value -b when ON, 0.0 when OFF, over T=2400
frames, every chord edge ON in exactly c=1200 frames. Pair members
'per' (one contiguous ON-bout per edge, flip count 2) vs 'aper' (seeded
scattered 1200-of-2400 subset, flip count ~1200) have BIT-identical
time-averages (integer-valued partial sums, exact) — the latent class
is the SCHEDULE; the static read cannot see it (exp148 N1). The
substrate the cone lives on is the pair-identical time-average W_avg =
ring + chords at -b*(c/T). Dose b = 1792.0 = exp148's LADDER[0] — the
lowest ladder member, chosen A PRIORI (pre-registered here, before any
run; no post-hoc ladder selection). Family = F2_zone_head: the ONE
battery family whose chord set is C∪F-relevant within the 6-ring
horizon (its chords terminate in the canon head, so both endpoints sit
in the seed set C and the flip edges are inside EVERY ring window —
asserted per ring, deposited as the horizon map). F1/F3 chords lie
beyond the 6-ring horizon; they are run as the pre-registered
HORIZON CONTROLS (their windows must be flip-free: F = 0, windowed
frames bit-identical across the pair, the temporal read reduces to the
phase read — the out-of-horizon discipline, measured not assumed).

THE PROTOCOL (one instance, zero knobs — exp151 P1-P8 with P5's window
generalized to the temporal window, everything else verbatim):
  P1' SUBSTRATE: the FlipPairMedium pair above at b=1792; the cone's
     geometry/identity objects (canon, T_plan, seed set, frontier) are
     computed on the pair-identical time-average W_avg (bitwise
     asserted equal to both members' frame means).
  P2 MORPHOLOGY: T_plan = spec_target_n(MULTI, labeling_bfs_n(|W_avg|),
     n) — scorer-only, verbatim exp151.
  P3 SEED: the canon-head set of W_avg (exp151 seed_cone verbatim)
     carrying T_plan[seed].
  P4 FRONTIER: F(C) = {j not in C : exists i in C, |W_avg[i,j]| > 0}
     (exp151 frontier_of verbatim). The committed SET sequence is
     therefore pair-identical and seed-independent (support-driven) —
     only committed VALUES can differ across the pair.
  P5' THE TEMPORAL WINDOW: the read's visible anatomy over the read
     window = every frame of the member medium restricted to the
     induced subgraph on C u F (closed-world n x n node space,
     beyond-frontier edges zeroed; asserted per ring). The read =
     project_phase_native(window) -> A; flip_clock_matrix(window) -> F
     (TC1); A_ext = A + F (TC2); execute_signed(MULTI, A_ext, seed,
     STAR_OP) (TC3) — exp148's temporal read VERBATIM on the window.
  P6 THE EMISSION RULE (unchanged): next ring's committed value per
     frontier node = the read's own final V there. No rescaling,
     threshold, lookup. The scorer never touches committed values.
  P7 ITERATION: R = 6 rings, executor seeds = exp142's SEEDS=(1,2,3),
     same schedule on every arm (exp151 verbatim).
  P8 STATIC-READ CONTROL: the same windows, the same protocol, with the
     read = the static phase read (project_phase_native -> execute;
     exp145 verbatim, no flip-clock channel) — the pre-registered
     confirming negative.

PRE-REGISTERED GATES (fixed before any run):

  GATE-T1 (expansion on the temporal medium) on the F2 pair at
     b=1792: a (member, seed) cell passes iff it expands >= 3 of the 6
     rings with EVERY expanded ring err < 6.0 mV (the deposited bar;
     ring err = RMS(emitted[frontier] - T_plan[frontier]), exp151's
     convention). T1 passes iff >= 4 of the 6 cells pass (majority,
     exp151-S2's majority-of-instances form); the per-member breakdown
     is deposited. If expansion collapses, deposit WHERE (which ring,
     which member, which nodes, emitted vs plan).
  GATE-T2 (separation propagates into committed structure) on the
     adversarial pair: for >= 2 of 3 seeds, the two cones (per vs aper)
     commit DIFFERENT morphologies — the committed value vectors over
     the final committed node set differ with max-abs >= 0.05 mV
     (pre-registered magnitude bar: 3x exp151's minimum ring err
     0.015 mV — resolvable by the read's own precision; the static
     control's blindness is exactly 0, see T3, so any super-bar delta
     is schedule-borne). Deposit: per-seed max-abs and RMS committed
     deltas, per-ring emitted deltas, and the channel localization —
     the projection channel must be bitwise inert across the pair
     (asserted per ring: A bitwise-equal), so separation can enter
     ONLY through the flip-clock channel (TC1/TC2). If T2 fails,
     deposit WHERE it breaks: which ring, which channel (projection /
     flip-clock / commitment), which seed — that localizes the
     semantics-to-structure gap and registers the repair.
  GATE-T3 (static-read blindness — the confirming negative) the P8
     static-read control on the SAME windows: the two pair members'
     cones commit morphologies within the static read's blindness.
     Primary form (expected): the static projection A is bitwise
     pair-identical per ring (integer-exact frame means), so the two
     members' static cones are ONE deterministic run — committed
     structures array-equal with delta exactly 0.0 on ALL 3 seeds.
     Fallback form (only if the bitwise assert fails — instrument
     disclosure): static committed max-abs delta < 0.05 mV on >= 2 of
     3 seeds. T3 passes iff the primary form holds (or the fallback
     under disclosure) AND contrasts with T2 (temporal deltas > 0).
  GATE-T4 (bit-exact static superset at the protocol level) the
     temporal-frontier protocol run on STATIC media (exp151's P1
     carrier substrates, chords at +64, single-frame windows) must
     reproduce exp151's deposited committed structure EXACTLY: per
     (family, seed, ring) — window sha256_16, frontier ids, emitted
     (rounded), plan, ring_err_mV, read_ok, program_verified, and
     run-level rings_expanded / final_coverage all equal to
     results/exp151_self_expansion.json's S1 runs; AND the per-ring
     reduction chain holds on every static window: A bitwise == window
     matrix, F == 0, A_ext bitwise == window matrix (so the temporal
     read's execute_signed input is BITWISE exp151's read input).

REFUTATION BRANCHES (pre-registered): a T1 collapse is deposited with
ring/member/node detail (emitted vs plan); a T2 failure is deposited
with the ring x channel localization above; a T4 mismatch is deposited
per-field (first differing ring/field). A collapse deposited with its
channel is a WIN per the program's rules.

INSTRUMENT NOTE (disclosed, pre-commit): the registered run is the
single run of this instrument. Its FIRST gate evaluation
under-materialized T3's pre-registered primary form in one
evaluation-only way: with the static projections bitwise pair-
identical (asserted), the single deterministic control cone was run
once but not ATTRIBUTED to the second member, so the second member's
committed vector was empty and the gate read None deltas. Repaired to
match THIS pre-registered text before commit (the attribution
materializes; the physics is deterministic and the ring logs are
unchanged — no gate bar, constant or rule was touched).

DEPOSIT: results/exp152_temporal_frontier.json

RUN:
  python3 -m experiments.exp152_temporal_frontier            # registered
  python3 -m experiments.exp152_temporal_frontier --smoke    # instrument
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
    C_BATTERY, FlipPairMedium, FrameSeq, LADDER, T_BATTERY,
    chord_set, flip_clock_matrix, read_temporal,
)
from experiments.exp151_self_expansion import (
    ERR_BAR, FAMILIES, RINGS as RINGS_P7, carrier_substrate, frontier_of,
    plan_of, seed_cone, window_matrix,
)
from experiments.exp94_multizone_scale import MULTI, labeling_bfs_n, spec_target_n

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp152_temporal_frontier.json")
EXP151_DEPOSIT = os.path.join(ROOT, "results", "exp151_self_expansion.json")

# ---------------- protocol constants (zero knobs; logged once) --------
B_DOSE = LADDER[0]             # 1792.0 — LADDER[0], chosen a priori
TREAT_FAMILY = "F2_zone_head"  # the C∪F-relevant (in-horizon) family
HORIZON_FAMILIES = ("F1_zone_tail", "F3_canon_boundary")
RINGS = RINGS_P7               # P7: 6 rings (exp151 verbatim)
T2_BAR_MV = 0.05               # pre-registered committed-separation bar
T1_MIN_CELLS = 4               # of 6 (member, seed) cells
T2_MIN_SEEDS = 2               # of 3
P6_RULE = ("next ring's committed value per frontier node = the read's "
           "own final V at that node (temporal read on the C u F flip "
           "window, verbatim); no rescaling, threshold or lookup")
P4_RULE = ("F(C) = {j not in C : exists i in C, |W_avg[i,j]| > 0} — "
           "graph distance 1 through first-class edges (exp142 R1)")


# ------------------------------- P1': the temporal frontier medium ----
def averaged_substrate(family: str, b: float) -> tuple[np.ndarray, list]:
    """The pair-identical time-average: ring (1.0) + chords at
    -b*(c/T) (each chord edge ON in exactly c of T frames)."""
    A, chords = chord_set(100, family)
    W = A.copy()
    for (i, j) in chords:
        W[i, j] = W[j, i] = -b * (C_BATTERY / T_BATTERY)
    return W, chords


def pair_members(family: str, b: float) -> dict[str, FlipPairMedium]:
    """exp148's adversarial pair VERBATIM (shared sched seed base)."""
    return {"per": FlipPairMedium(b, family, "per"),
            "aper": FlipPairMedium(b, family, "aper")}


class WindowFlipMedium:
    """P5' — the temporal window: every frame of the member medium
    restricted to the induced subgraph on C u F (closed-world n x n
    node contract; beyond-frontier edges zeroed). Carries exp151's S4
    window contract (kind='window', snapshots() -> FrameSeq)."""

    kind = "window"

    def __init__(self, member, win_nodes: set[int]):
        n = member.A.shape[0]
        self.member, self.n, self.win_nodes = member, n, set(win_nodes)
        self.T = member.T
        mask = np.zeros((n, n))
        idx = np.array(sorted(self.win_nodes))
        mask[np.ix_(idx, idx)] = 1.0
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
        """Instrument validation: every frame zero outside C u F."""
        worst = 0.0
        for frame in self.snapshots():
            worst = max(worst, float(np.max(np.abs(frame[self._outside]))))
        return {"outside_zero_max": worst,
                "ok": bool(worst == 0.0)}


def c_sequence(W: np.ndarray, max_rings: int) -> tuple[list[set], list[list]]:
    """P4 — the deterministic committed-SET walk (support-driven, hence
    pair-identical and seed-independent): seq[0] = seed set, seq[k] =
    committed set after ring k; frontiers[k-1] = ring k's frontier."""
    C = set(seed_cone(W))
    seq, frontiers = [set(C)], []
    for _ in range(max_rings):
        F = frontier_of(C, W)
        if not F:
            break
        frontiers.append(F)
        C = C | set(F)
        seq.append(set(C))
    return seq, frontiers


# ------------------------------- the cone on flip media ----------------
def run_flip_cone(members: dict, W_avg: np.ndarray, T_plan: np.ndarray,
                  seeds: list[int], mode: str,
                  sweep_ring1: bool = False) -> dict:
    """P5'-P7 — the cone on the temporal frontier medium.

    mode='temporal': read = exp148's TC1-TC3 verbatim on the window.
    mode='static'  : read = exp145's phase read verbatim (P8 control).

    The window NODE sequence is precomputed from W_avg's support (P4)
    and shared across seeds and members; per ring the projection and
    flip clock are computed ONCE per member. A member's read is run
    whenever its input can differ (temporal: flip clocks differ;
    static: projections differ); otherwise ONE deterministic run is
    attributed to both members (inputs bitwise-asserted)."""
    seq, frontiers = c_sequence(W_avg, RINGS)
    names = list(members)
    runs = {m: {s: {"rings": [], "active": True, "committed": {},
                    "rings_expanded": 0}
                for s in seeds} for m in names}
    chan_log, sweep = [], None
    for k, F in enumerate(frontiers, 1):
        win = seq[k]
        wms = {m: WindowFlipMedium(members[m], win) for m in names}
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
        fc_delta = max(float(np.max(np.abs(Fcs[names[0]] - Fcs[m])))
                       for m in names)
        run_members = names
        if mode == "static" and proj_bitident:
            run_members = [names[0]]      # one deterministic cone
        elif mode == "temporal" and fc_delta == 0.0 and proj_bitident:
            run_members = [names[0]]      # horizon: inputs identical
        ring = {"ring_index": k,
                "frontier": [int(j) for j in F],
                "n_window_nodes": len(win),
                "n_window_edges": int(np.count_nonzero(
                    np.triu(np.abs(A0) > 0, 1))),
                "window_sha256_16": hashlib.sha256(
                    np.ascontiguousarray(A0).tobytes()).hexdigest()[:16],
                "proj_bitident_across_pair": bool(proj_bitident),
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
            A_ext = A + Fcs[m] if mode == "temporal" else A
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
                               bool(out.get("program_verified",
                                            False)),
                           "ring_index": k,
                           "frontier": [int(j) for j in F],
                           "emitted": [round(float(x), 3)
                                       for x in emitted],
                           "plan": [round(float(x), 3)
                                    for x in T_plan[F]],
                           "ring_err_mV": round(err, 3)}
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
                        "pass": False})
                    st["active"] = False
        if mode == "temporal" and len(run_members) == len(names):
            deltas = {}
            for s in seeds:
                if all(s in emitted_by.get(m, {}) for m in names):
                    d = np.abs(emitted_by[names[0]][s]
                               - emitted_by[names[1]][s])
                    deltas[str(s)] = round(float(np.max(d)), 6)
            ring["emitted_delta_max_by_seed"] = deltas
        chan_log.append(ring)
    # ---- single-run attribution (deterministic inputs) --------------
    # When only one member's read ran (bitwise-identical inputs), that
    # ONE deterministic cone IS both members' cone (T3 primary form);
    # materialize the attribution so the pair delta is exactly 0.0.
    ran = {m: any(st["rings"] for st in runs[m].values()) for m in names}
    if len(names) > 1 and ran.get(names[0]) and not all(ran.values()):
        for m in names:
            if not ran[m]:
                for s in seeds:
                    src = runs[names[0]][s]
                    runs[m][s] = {
                        "rings": [dict(r, attributed_from=names[0])
                                  for r in src["rings"]],
                        "active": src["active"],
                        "committed": dict(src["committed"]),
                        "rings_expanded": src["rings_expanded"]}
    # ---- finalize per (member, seed) cells (exp151 conventions) -----
    out_members = {}
    for m in names:
        rlist = []
        for s in seeds:
            st = runs[m][s]
            expanded = [x for x in st["rings"]
                        if x.get("read_ok")]
            n_pass = sum(1 for x in expanded if x.get("pass"))
            all_pass = n_pass == len(expanded)
            cell = bool(len(expanded) >= 3 and all_pass)
            committed_vec = None
            if st["committed"]:
                nodes = sorted(st["committed"])
                committed_vec = {"nodes": nodes,
                                 "values": [round(st["committed"][n], 3)
                                            for n in nodes]}
            rlist.append({"seed": s,
                          "rings_expanded": len(expanded),
                          "rings_passed": n_pass,
                          "exhausted": bool(
                              st["rings"] and
                              st["rings"][-1].get("exhausted"))
                          or len(frontiers) < RINGS,
                          "cell_pass": cell,
                          "attributed_from": (
                              names[0] if m != names[0] and
                              not ran.get(m, True) else None),
                          "committed": committed_vec,
                          "rings": st["rings"]})
        out_members[m] = {"runs": rlist}
    return {"members": out_members, "ring_channel_log": chan_log,
            "sweep_ring1": sweep,
            "n_frontier_walk": len(frontiers)}


def committed_delta(run_a: dict, run_b: dict) -> dict:
    """T2/T3 measurement — committed-structure difference over the
    final committed node set (identical node sets by P4)."""
    ca, cb = run_a.get("committed"), run_b.get("committed")
    if ca is None or cb is None:
        return {"n_nodes": 0, "max_abs_mV": None, "rms_mV": None}
    assert ca["nodes"] == cb["nodes"], "committed node sets diverged"
    va = np.asarray(ca["values"], dtype=float)
    vb = np.asarray(cb["values"], dtype=float)
    d = va - vb
    return {"n_nodes": len(ca["nodes"]),
            "max_abs_mV": round(float(np.max(np.abs(d))), 6),
            "rms_mV": round(float(np.sqrt(np.mean(d * d))), 6)}


# ------------------------------- T4: static superset -------------------
def run_static_superset(family: str, seeds: list[int],
                        deposit151: dict) -> dict:
    """GATE-T4 — the temporal-frontier protocol on exp151's static
    carrier medium: single-frame windows (so F = 0, A_ext bitwise ==
    A bitwise == window matrix) must reproduce exp151's deposited S1
    committed structure EXACTLY, field by field."""
    W, chords = carrier_substrate(family)
    T_plan = plan_of(W)
    seq, frontiers = c_sequence(W, RINGS)
    ref_runs = {r["seed"]: r for r in
                deposit151["S1_intact"][family]["runs"]}
    class _Single:
        kind = "window"
        def __init__(self, M):
            self._M = M
        def snapshots(self):
            return FrameSeq(lambda: iter([self._M]), 1)
    rings_out, mismatches, n_reduction_ok = [], [], 0
    for k, F in enumerate(frontiers, 1):
        M, meta = window_matrix(W, set(seq[k - 1]), F, None)
        med = _Single(M)
        with warnings_as_errors():
            A, rho, branch = project_phase_native(med)
        Fc = flip_clock_matrix(med)
        A_ext = A + Fc
        red = {"proj_bitwise_window": bool(np.array_equal(A, M)),
               "flip_zero": bool(np.count_nonzero(Fc) == 0),
               "Aext_bitwise_window": bool(np.array_equal(A_ext, M))}
        if all(red.values()):
            n_reduction_ok += 1
        for s in seeds:
            with warnings_as_errors():
                out = execute_signed(MULTI, A_ext, s, op=STAR_OP,
                                     return_state=True)
            V = np.asarray(out["final_state"]["V"], dtype=float)
            emitted = V[F]
            err = float(np.sqrt(np.mean((emitted - T_plan[F]) ** 2)))
            rec = {"seed": s, "ring_index": k,
                   "frontier": [int(j) for j in F],
                   "window": meta,
                   "emitted": [round(float(x), 3) for x in emitted],
                   "plan": [round(float(x), 3) for x in T_plan[F]],
                   "ring_err_mV": round(err, 3),
                   "read_ok": True,
                   "program_verified":
                       bool(out.get("program_verified", False)),
                   "reduction": red}
            rings_out.append(rec)
            ref = ref_runs[s]
            rk = ref["rings"][k - 1]
            for field in ("frontier", "emitted", "plan",
                          "ring_err_mV", "read_ok",
                          "program_verified", "ring_index"):
                if rec[field] != rk.get(field):
                    mismatches.append(
                        {"family": family, "seed": s, "ring": k,
                         "field": field, "got": rec[field],
                         "want": rk.get(field)})
            if rec["window"] != rk.get("window"):
                mismatches.append({"family": family, "seed": s,
                                   "ring": k, "field": "window",
                                   "got": rec["window"],
                                   "want": rk.get("window")})
            if k == len(frontiers):
                if ref["rings_expanded"] != len(frontiers):
                    mismatches.append({"family": family, "seed": s,
                                       "field": "rings_expanded",
                                       "got": len(frontiers),
                                       "want": ref["rings_expanded"]})
                if ref["final_coverage"][0] != len(seq[-1]):
                    mismatches.append({"family": family, "seed": s,
                                       "field": "final_coverage",
                                       "got": len(seq[-1]),
                                       "want":
                                           ref["final_coverage"][0]})
    return {"family": family, "n_rings": len(frontiers),
            "n_reduction_ok": n_reduction_ok,
            "reduction_all_ok": n_reduction_ok == len(frontiers),
            "mismatches": mismatches,
            "match": bool(len(mismatches) == 0
                          and n_reduction_ok == len(frontiers)),
            "rings": rings_out}


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    out: dict = {
        "experiment": "exp152_temporal_frontier",
        "protocol_constants": {
            "b_dose": B_DOSE, "b_ladder": list(LADDER),
            "b_choice_rule": "LADDER[0], a priori (pre-registered)",
            "T": T_BATTERY, "c": C_BATTERY,
            "treat_family": TREAT_FAMILY,
            "horizon_families": list(HORIZON_FAMILIES),
            "rings": RINGS, "err_bar": ERR_BAR,
            "t2_bar_mV": T2_BAR_MV, "t1_min_cells": T1_MIN_CELLS,
            "t2_min_seeds": T2_MIN_SEEDS,
            "executor_seeds": list(SEEDS),
            "emission_rule": P6_RULE, "frontier_rule": P4_RULE},
        "smoke": bool(args.smoke)}
    seeds = [SEEDS[0]] if args.smoke else list(SEEDS)
    fams_treat = [TREAT_FAMILY]
    fams_horizon = [] if args.smoke else list(HORIZON_FAMILIES)

    # ---------- P1' instrument: pair construction + bit-identity -----
    instrument = {}
    members_all: dict[str, dict[str, FlipPairMedium]] = {}
    substrates: dict[str, tuple[np.ndarray, list]] = {}
    for fam in [TREAT_FAMILY, *fams_horizon]:
        members = pair_members(fam, B_DOSE)
        W_avg, chords = averaged_substrate(fam, B_DOSE)
        # the pair's time-averages are BIT-identical to W_avg
        means = {}
        for m in members:
            with warnings_as_errors():
                A_full, _, _ = project_phase_native(members[m])
            means[m] = A_full
        bit_ok = all(np.array_equal(means["per"], means[m])
                     for m in means)
        analytic_ok = np.array_equal(means["per"], W_avg)
        T_plan = plan_of(W_avg)
        # identity continuity with the deposited line (support-only)
        W_car, _ = carrier_substrate(fam)
        plan_continuity = bool(np.array_equal(T_plan, plan_of(W_car)))
        seq, frontiers = c_sequence(W_avg, RINGS)
        horizon_map = []
        for k in range(1, len(seq)):
            inside = [e for e, (i, j) in enumerate(chords)
                      if i in seq[k] and j in seq[k]]
            horizon_map.append({"ring": k, "chords_inside": inside})
        n_seed_chords = sum(1 for (i, j) in chords
                            if i in seq[0] and j in seq[0])
        instrument[fam] = {
            "pair_timeavg_bitidentical": bool(bit_ok),
            "timeavg_bitwise_analytic_W_avg": bool(analytic_ok),
            "plan_continuity_with_carrier": plan_continuity,
            "n_chords": len(chords),
            "n_chords_inside_seed_set": n_seed_chords,
            "horizon_map": horizon_map,
            "seed_set_size": len(seq[0]),
            "frontier_walk_rings": len(frontiers)}
        members_all[fam] = members
        substrates[fam] = (W_avg, chords)
    out["instrument"] = instrument

    # ---------- full-organism anchors (exp148 temporal read) ---------
    anchors = {}
    if not args.smoke:
        for fam in [TREAT_FAMILY, *fams_horizon]:
            for m in members_all[fam]:
                with warnings_as_errors():
                    a = read_temporal(members_all[fam][m], seeds[0])
                anchors[f"{fam}:{m}"] = {
                    "err_vs_target": round(float(a["err_vs_target"]), 3),
                    "verified": bool(a["program_verified"]),
                    "rho": round(float(a["rho"]), 6),
                    "branch": a["branch"]}
        out["anchors_full_organism_temporal"] = anchors

    # ---------- T1/T2: the temporal-frontier arm (F2 pair) -----------
    temporal = {}
    for fam in fams_treat:
        W_avg, chords = substrates[fam]
        T_plan = plan_of(W_avg)
        temporal[fam] = run_flip_cone(members_all[fam], W_avg, T_plan,
                                      seeds, mode="temporal",
                                      sweep_ring1=True)
    out["temporal_frontier"] = temporal

    # ---------- T3: the static-read control (same windows) -----------
    static_control = {}
    if not args.smoke:
        for fam in fams_treat:
            W_avg, chords = substrates[fam]
            T_plan = plan_of(W_avg)
            static_control[fam] = run_flip_cone(members_all[fam],
                                                W_avg, T_plan, seeds,
                                                mode="static")
        out["static_read_control"] = static_control

    # ---------- horizon controls (F1/F3: flips beyond the horizon) ---
    horizon = {}
    if not args.smoke:
        for fam in fams_horizon:
            W_avg, chords = substrates[fam]
            T_plan = plan_of(W_avg)
            horizon[fam] = run_flip_cone(members_all[fam], W_avg,
                                         T_plan, seeds,
                                         mode="temporal")
        out["horizon_controls"] = horizon

    # ---------- T4: static superset vs exp151's deposit --------------
    t4 = {}
    if not args.smoke:
        with open(EXP151_DEPOSIT) as f:
            deposit151 = json.load(f)
        for fam in FAMILIES:
            t4[fam] = run_static_superset(fam, seeds, deposit151)
        out["T4_static_superset"] = {
            fam: {k: v for k, v in t4[fam].items() if k != "rings"}
            for fam in t4}

    # ---------- gate evaluation --------------------------------------
    if not args.smoke:
        # T1: >= 4 of 6 (member, seed) cells on the temporal medium
        cells = [r for fam in fams_treat
                 for m in temporal[fam]["members"]
                 for r in temporal[fam]["members"][m]["runs"]]
        cells_pass = sum(1 for r in cells if r["cell_pass"])
        per_member = {m: sum(1 for r in
                             temporal[TREAT_FAMILY]["members"][m]["runs"]
                             if r["cell_pass"])
                      for m in temporal[TREAT_FAMILY]["members"]}
        g1 = bool(cells_pass >= T1_MIN_CELLS)
        # T2: committed separation on the adversarial pair
        t2_rows = []
        for m_a, m_b in (("per", "aper"),):
            for ra, rb in zip(temporal[TREAT_FAMILY]["members"][m_a]["runs"],
                              temporal[TREAT_FAMILY]["members"][m_b]["runs"]):
                d = committed_delta(ra, rb)
                d["seed"] = ra["seed"]
                d["rings_expanded"] = [ra["rings_expanded"],
                                       rb["rings_expanded"]]
                t2_rows.append(d)
        sep_seeds = sum(1 for d in t2_rows
                        if d["max_abs_mV"] is not None
                        and d["max_abs_mV"] >= T2_BAR_MV)
        g2 = bool(sep_seeds >= T2_MIN_SEEDS)
        # T3: static-read blindness (primary: bitwise inputs -> delta 0)
        t3_rows, bitwise_all = [], True
        for rl in static_control[TREAT_FAMILY]["ring_channel_log"]:
            bitwise_all &= bool(rl["proj_bitident_across_pair"])
        for ra, rb in zip(static_control[TREAT_FAMILY]["members"]["per"]["runs"],
                          static_control[TREAT_FAMILY]["members"]["aper"]["runs"]):
            d = committed_delta(ra, rb)
            d["seed"] = ra["seed"]
            t3_rows.append(d)
        if bitwise_all:
            g3 = bool(all(d["max_abs_mV"] == 0.0 for d in t3_rows)
                      and sep_seeds >= 1)
            g3_form = "primary_bitwise"
        else:
            g3 = bool(sum(1 for d in t3_rows
                          if d["max_abs_mV"] is not None
                          and d["max_abs_mV"] < T2_BAR_MV) >= T2_MIN_SEEDS)
            g3_form = "fallback_bar (disclosed: projections not bitwise)"
        # T4: bit-exact static superset
        g4 = bool(t4) and all(t4[fam]["match"] for fam in t4)
        out["gate_details"] = {
            "T1": {"cells_pass": cells_pass, "of": len(cells),
                   "per_member": per_member},
            "T2": {"separated_seeds": sep_seeds,
                   "of": len(t2_rows), "rows": t2_rows,
                   "channel_localization": {
                       "projection_bitwise_inert": bool(all(
                           rl["proj_bitident_across_pair"] for rl in
                           temporal[TREAT_FAMILY]["ring_channel_log"])),
                       "fc_cross_delta_max": max(
                           rl["fc_cross_delta_max"] for rl in
                           temporal[TREAT_FAMILY]["ring_channel_log"]),
                       "per_ring_emitted_delta":
                           [rl.get("emitted_delta_max_by_seed", {})
                            for rl in
                            temporal[TREAT_FAMILY]["ring_channel_log"]]}},
            "T3": {"form": g3_form, "rows": t3_rows,
                   "projections_bitwise_pair_identical":
                       bool(bitwise_all)},
            "T4": {"families_match": {fam: t4[fam]["match"]
                                      for fam in t4}}}
        out["gates"] = {
            "T1_expansion_on_temporal_medium": {"pass": g1},
            "T2_separation_into_structure": {"pass": g2},
            "T3_static_read_blindness": {"pass": g3},
            "T4_bitexact_static_superset": {"pass": g4}}
        out["verdict"] = "{} / 4 gates PASS".format(
            sum(1 for g in out["gates"].values() if g["pass"]))
    else:
        fam = TREAT_FAMILY
        runs = temporal[fam]["members"]
        out["smoke_checks"] = {
            "instrument": instrument[fam],
            "rings_expanded": {m: [r["rings_expanded"] for r in
                                   runs[m]["runs"]]
                               for m in runs},
            "ring_errs": {m: [r_["ring_err_mV"] for r_ in
                              runs[m]["runs"][0]["rings"]]
                          for m in runs},
            "emitted_deltas": [rl.get("emitted_delta_max_by_seed", {})
                               for rl in
                               temporal[fam]["ring_channel_log"]],
            "fc_max_per_member": [rl["members"] for rl in
                                  temporal[fam]["ring_channel_log"]]}
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
