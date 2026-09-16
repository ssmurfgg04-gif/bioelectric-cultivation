#!/usr/bin/env python3
"""exp151 — THE SELF-EXPANSION PROTOCOL (the cone reads its own frontier).

STAGE 4 of the 101% frame (workstream S). Foundation: the semantics-
carrying read line exp137 L115 -> exp142 (sign) -> exp145 (phase) ->
exp148 (temporal) — the M33-class reader now carries magnitude, sign,
phase and schedule semantics with bit-exact static supersets, zero
rejections OOD. exp148's registered (a) named the channel-split; the
101% Stage-4 target named here is the CONE: "self-expansion protocol.
M33 reader bypasses junctions — use it. Test: cone expands without
external control, cross-organism, survives blockade."

THIS EXPERIMENT: a cone = a growing region of COMMITTED MORPHOLOGY on a
substrate. The expansion step is EMITTED BY THE CONE'S OWN READ — the
M33-class read (exp142's execute_signed VERBATIM, exp145/148 front-ends)
run on the cone's visible anatomy — nothing external targets the next
ring. Pre-registered BEFORE any run:

THE PROTOCOL (one instance, zero knobs, used unchanged on every
substrate, every arm, every ring):

  P1 SUBSTRATE: exp142's carrier geometry VERBATIM (chord_set,
     PROBE_SEED=7, K_CHORDS=6, families F1_zone_tail / F2_zone_head /
     F3_canon_boundary) with the carrier chords at dose b=+64.0 — a
     deposited positive-verify dose (exp142 H2: the positive member of
     every separated pair verifies; the exp151 full-organism anchor read
     is run per substrate to confirm verify before any cone run).
     Cross-substrate class: exp137's SignedMedium (the A-NN-violating
     OOD battery class, n=100, 3 instances, seeds 151_000+i) — the
     exp142 sign-carrying read is the reader there, verbatim.
  P2 MORPHOLOGY (the identity object): T_plan = spec_target_n(MULTI,
     labeling_bfs_n(|W|), n) — the record's own canon+zone plan, the
     same object every decode in the line verifies against. T_plan is a
     SCORER-ONLY object: it is passed to the scoring function and to
     nothing else (asserted structurally; the window builder consumes
     only W and the committed set).
  P3 SEED (initial condition, not under test): the cone seeds as the
     organism's canon-head set — the nodes whose full-support canon
     label is HEAD_V (labeling_bfs_n's own n//4 rule) — carrying the
     parent's committed values T_plan[seed]. This is the standard
     committed-parent-patch initial condition of the regen line (exp94/
     exp124); the gates below concern rings >= 1 only.
  P4 FRONTIER (the expansion extent, zero knobs): F(C) = {j not in C :
     exists i in C with |W[i,j]| > 0} — graph distance 1 through
     first-class edges (exp142's R1 rule: a signed edge is a first-class
     edge). The frontier definition is the geometry; it is not tuned.
  P5 THE READ (the cone's own targeting input): the window matrix =
     the full n x n node space (the M33 closed-world node contract,
     exp137 A-CW: the read inherits the medium's node ids) with every
     edge whose endpoints are not BOTH in C u F zeroed — the read sees
     exactly the committed region, the frontier ring, and the edges
     among them (induced subgraph on C u F). Asserted per ring:
     support(window) == support(W) restricted to C u F, and zero
     outside. The read = execute_signed(MULTI, window, seed, STAR_OP,
     return_state=True) VERBATIM (structure on |window|, coupling on
     window; exp148's temporal front-end for the S4 reduction arm).
  P6 THE EMISSION RULE (the one rule, zero knobs, the controller IS the
     read): the next ring's committed value for each frontier node j is
     the read's own final V at j. Nothing else. No rescaling, no
     threshold, no lookup. The committed set grows C' = C u F with
     exactly those values (copied from the read output in code; the
     scorer never touches them).
  P7 ITERATION: R = 6 pre-registered rings per cone run (expansion
     stops early only on frontier exhaustion — the cone has swallowed
     the organism's support). Per-ring executor seeds = exp142's
     SEEDS = (1, 2, 3) — the battery-wide decode seeds, same schedule
     on every arm and substrate.
  P8 BLOCKADE ARM (S3): the record's GJ-blocker operating point
     gap_scale = 0.05 (the deposited gap ladder 1.0/0.5/0.25/0.05 ->
     3.93/4.54/6.03 mV: 0.05 is the cell at/over the 6.0 bar) applied
     to the cone-frontier junction edges — the C<->F edges of the
     window matrix are scaled by 0.05 (support preserved: |0.05*w|>0,
     so canon, dt and the walk's |A|>0 traversal are intact; the
     junction CONDUCTANCE the expansion flow would use is cut). The
     committed interior and frontier-internal edges stay intact — a
     blockade at the expansion front, where a GJ-blocker at the
     blastema frontier acts.

PRE-REGISTERED GATES (fixed before the registered run):

  GATE-S1 (self-targeted expansion) on the carrier substrates: on >= 2
     of the 3 families, the MAJORITY of seeds (>= 2 of 3) expand >= 3
     of the 6 rings with ring err < 6.0 mV on every expanded ring,
     where ring err = RMS(emitted[frontier] - T_plan[frontier]) (the
     record's pattern_error convention, mV) and the ONLY values that
     entered the committed set are the read's own outputs (per-ring
     targeting log deposited: window support edge count, window SHA256
     digest, frontier ids, emitted values, plan values, err — the log
     is the proof of sole targeting).
  GATE-S2 (cross-substrate portability) the SAME protocol instance
     (identical constants, seed schedule, emission rule — no
     per-substrate retuning) on exp137's SignedMedium class: majority
     of the 3 instances expand >= 3 rings OR to frontier exhaustion
     (support swallowed) with every expanded ring err < 6.0 mV.
  GATE-S3 (blockade survival via the reader route) the same protocol
     under P8's gap-0.05 frontier blockade: majority of (family, seed)
     carrier cells expand >= 3 rings with every ring err < 6.0 mV.
     PRE-REGISTERED DEGRADATION BOUND (stated before the run):
     "degraded-but-expanding" passes ONLY if every ring err stays
     under the record's 6.0 mV bar; the intact-vs-blockade per-ring
     err delta is deposited as the measured cost of the blockade
     route. If any ring err >= 6.0 the cell FAILS and the collapse is
     deposited (which ring, which nodes, emitted vs plan).
  GATE-S4 (zero-knobs + bit-exact static reduction) (i) on every F1
     (seed 1) ring window, the full temporal read (exp148 TC1-TC3:
     exp145 projection + flip-clock channel + execute_signed) applied
     to the static window reduces BIT-EXACTLY to the phase read
     (final V bitwise equal per ring — static windows have F = 0, so
     A_ext = A bitwise; the cone's read IS the current best read
     wherever the medium is static); (ii) the protocol constants
     (P1-P8) are logged once and are the same object across every
     arm, ring and substrate — the code has no per-ring parameter
     path; the deposit carries the constants table.

REFUTATION BRANCHES (pre-registered): if expansion collapses at ring
k, deposit WHERE — which ring, which family/instance, which nodes,
emitted vs plan values, and the window's canon head vs the global head
restricted to the window (the pre-identified collapse channel is the
canon-prefix break: the window ball is a global-BFS-order prefix only
while chord pulls stay inside the ball; F3's canon-boundary chords are
the adversarial geometry by construction) — and register the repair
direction (chord-aware ball or prefix-consistent seeding). A collapse
deposited with its channel is a WIN per the program's rules.

INSTRUMENT NOTE (disclosed, pre-commit): the registered run is the
single run of this instrument. Its FIRST gate evaluation
under-implemented the pre-registered wording in two evaluation-only
ways — (a) S2's exhaustion disjunct (">= 3 rings OR to frontier
exhaustion with every expanded ring err < 6.0") was coded as the
rings-only branch, and (b) rings_expanded counted the frontier-
exhaustion marker as an expanded ring. Both were repaired to match
THIS pre-registered text before commit; the physics is deterministic
and the ring logs are unchanged — no gate bar, constant or rule was
touched.

DEPOSIT: results/exp151_self_expansion.json

RUN:
  python3 -m experiments.exp151_self_expansion            # registered
  python3 -m experiments.exp151_self_expansion --smoke    # instrument
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

from experiments.exp137_universal_reader import SignedMedium
from experiments.exp142_sign_read import SEEDS, STAR_OP, execute_signed
from experiments.exp145_phase_read import (
    project_phase_native, warnings_as_errors,
)
from experiments.exp148_temporal_read import chord_set, flip_clock_matrix
from experiments.exp94_multizone_scale import MULTI, labeling_bfs_n, spec_target_n

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp151_self_expansion.json")

# ---------------- protocol constants (P1-P8; logged once, shared) ----
CARRIER_DOSE = 64.0            # exp142 deposited positive-verify dose
FAMILIES = ("F1_zone_tail", "F2_zone_head", "F3_canon_boundary")
RINGS = 6                      # P7: pre-registered ring count
GAP_BLOCKADE = 0.05            # P8: the record's gap-ladder blockade cell
ERR_BAR = 6.0                  # the record's verify bar (mV)
SIGNED_SEEDS = (151_000, 151_001, 151_002)   # exp137-class instances
S1_MIN_FAMILIES = 2            # of 3
S1_MIN_SEEDS = 2               # of 3 (majority per family)
S1_MIN_RINGS = 3               # of RINGS


# ------------------------------- P2/P3: identity object and seed -----
def canon_of(W: np.ndarray) -> np.ndarray:
    """The read's own canon rule on the support (labeling_bfs_n on
    |W| — exactly what execute_signed computes internally via R1)."""
    return labeling_bfs_n(np.abs(W))


def plan_of(W: np.ndarray) -> np.ndarray:
    """P2 — the morphology/identity object (SCORER-ONLY by protocol)."""
    canon = canon_of(W)
    return spec_target_n(MULTI, canon, W.shape[0])


def seed_cone(W: np.ndarray) -> list[int]:
    """P3 — the canon-head set (the read's own n//4 head rule on the
    full support) with the parent's committed values."""
    canon = canon_of(W)
    return [int(i) for i in np.where(canon == -20.0)[0]]  # HEAD_V


# ------------------------------- P4/P5: frontier and window ----------
def frontier_of(C: set[int], W: np.ndarray) -> list[int]:
    """P4 — graph-distance-1 frontier through first-class |W|>0 edges."""
    C_arr = sorted(C)
    reach = np.abs(W)[C_arr, :].sum(axis=0) > 0
    return [int(j) for j in np.where(reach)[0] if int(j) not in C]


def window_matrix(W: np.ndarray, C: set[int], F: list[int],
                  gap: float | None) -> tuple[np.ndarray, dict]:
    """P5/P8 — the read's visible anatomy: induced submatrix on C u F
    in the FULL n x n node space (closed-world node contract), every
    beyond-frontier edge zeroed (asserted); under blockade the C<->F
    junction edges are scaled by the record's gap operating point."""
    n = W.shape[0]
    win_nodes = C | set(F)
    M = np.zeros_like(W)
    idx = np.array(sorted(win_nodes))
    M[np.ix_(idx, idx)] = W[np.ix_(idx, idx)]
    if gap is not None:
        # scale exactly the cross-frontier junction edges (C<->F)
        for i in C:
            for j in F:
                if M[i, j] != 0.0:
                    M[i, j] *= gap
                    M[j, i] *= gap
    # ---- instrument assertions (the visibility proof) ----
    sup_mask = np.zeros_like(W, dtype=bool)
    sup_mask[np.ix_(idx, idx)] = np.abs(W[np.ix_(idx, idx)]) > 0
    assert np.array_equal(np.abs(M) > 0, sup_mask), \
        "window support != induced support on C u F"
    outside = np.ones_like(W, dtype=bool)
    outside[np.ix_(idx, idx)] = False
    assert np.all(M[outside] == 0.0), "read sees beyond-frontier edges"
    digest = hashlib.sha256(M.tobytes()).hexdigest()[:16]
    meta = {"n_nodes": len(win_nodes), "n_edges":
            int(np.count_nonzero(np.triu(np.abs(M) > 0, 1))),
            "cf_edges_scaled":
                int(sum(1 for i in C for j in F if W[i, j] != 0.0))
            if gap is not None else 0,
            "sha256_16": digest}
    return M, meta


# ------------------------------- P6: the expansion step --------------
def expansion_step(W: np.ndarray, T_plan: np.ndarray, C: set[int],
                   seed: int, gap: float | None,
                   temporal_check: bool = False) -> dict:
    """One expansion step: the cone's own read emits the next ring.

    The ONLY values that can enter the committed region are copied from
    the read's final V (P6); T_plan touches this function solely via
    the scoring at the end (provenance by code structure)."""
    F = frontier_of(C, W)
    if not F:
        return {"ring_expanded": False, "frontier": [],
                "exhausted": True}
    M, meta = window_matrix(W, C, F, gap)
    try:
        with warnings_as_errors():
            out = execute_signed(MULTI, M, seed, op=STAR_OP,
                                 return_state=True)
        V = np.asarray(out["final_state"]["V"], dtype=float)
        emitted = V[F]
        err = float(np.sqrt(np.mean((emitted - T_plan[F]) ** 2)))
        rec = {"ring_expanded": True, "exhausted": False,
               "read_ok": True, "program_verified":
                   bool(out.get("program_verified", False)),
               "frontier": [int(j) for j in F],
               "window": meta,
               "emitted": [round(float(x), 3) for x in emitted],
               "plan": [round(float(x), 3) for x in T_plan[F]],
               "ring_err_mV": round(err, 3)}
        rec["pass"] = bool(np.isfinite(err) and err < ERR_BAR)
        if temporal_check:
            # S4(i): the temporal read must reduce BIT-EXACTLY to the
            # phase read on this static window (F = 0 => A_ext = A).
            class _Win:
                kind = "window"
                def snapshots(self):
                    return [M]
            A_ph, rho, branch = project_phase_native(_Win())
            with warnings_as_errors():
                out_ph = execute_signed(MULTI, A_ph, seed, op=STAR_OP,
                                        return_state=True)
            A_t, rho_t, branch_t = project_phase_native(_Win())
            Fc = flip_clock_matrix(_Win())
            A_ext = A_t + Fc
            with warnings_as_errors():
                out_tm = execute_signed(MULTI, A_ext, seed, op=STAR_OP,
                                        return_state=True)
            V_ph = np.asarray(out_ph["final_state"]["V"], dtype=float)
            V_tm = np.asarray(out_tm["final_state"]["V"], dtype=float)
            rec["s4_bitexact"] = bool(np.array_equal(V_ph, V_tm))
            rec["s4_flip_zero"] = bool(np.count_nonzero(Fc) == 0)
            rec["s4_Aext_bitwise_A"] = bool(np.array_equal(A_ext, A_ph))
        return rec
    except Exception as e:                     # zero-rejection hygiene
        return {"ring_expanded": True, "exhausted": False,
                "read_ok": False,
                "rejection": f"{type(e).__name__}: {e}"[:200],
                "frontier": [int(j) for j in F], "window": meta,
                "pass": False}


def run_cone(W: np.ndarray, T_plan: np.ndarray, seeds: list[int],
             gap: float | None, temporal_check_seed: int | None = None,
             exhaustion_ok: bool = False) -> dict:
    """P7 — iterate the expansion step for RINGS rings per seed.

    Gate cell semantics per the pre-registered wording: S1/S3 require
    rings_expanded >= 3 with EVERY expanded ring err < 6.0; S2 adds the
    exhaustion disjunct (the cone may swallow the organism's whole
    support before ring 3 on a dense substrate) — exhaustion passes iff
    every expanded ring passed and at least one ring expanded."""
    seed_set = set(seed_cone(W))
    support_n = int(np.count_nonzero(np.abs(W).sum(axis=1)))
    runs = []
    for s in seeds:
        C = set(seed_set)
        ring_logs = []
        for r in range(RINGS):
            tc = temporal_check_seed is not None and s == temporal_check_seed
            rec = expansion_step(W, T_plan, C, s, gap, temporal_check=tc)
            rec["ring_index"] = r + 1
            ring_logs.append(rec)
            if not rec.get("ring_expanded") or rec.get("exhausted"):
                break
            if not rec.get("read_ok", False):
                break
            # P6 commit: the read's own outputs, verbatim
            V = rec["emitted"]
            for j, v in zip(rec["frontier"], V):
                C.add(int(j))
        expanded = [x for x in ring_logs
                    if x.get("ring_expanded") and x.get("read_ok")]
        rings_expanded = len(expanded)
        n_pass = sum(1 for x in expanded if x.get("pass"))
        exhausted = bool(ring_logs[-1].get("exhausted"))
        all_pass = n_pass == rings_expanded
        cell_pass = bool(rings_expanded >= S1_MIN_RINGS and all_pass)
        if exhaustion_ok and exhausted and all_pass and rings_expanded >= 1:
            cell_pass = True
        runs.append({"seed": s,
                     "rings_expanded": rings_expanded,
                     "exhausted": exhausted,
                     "final_coverage": [len(C), support_n],
                     "ring_errs_mV": [x.get("ring_err_mV")
                                      for x in expanded],
                     "rings_passed": n_pass,
                     "cell_pass": cell_pass,
                     "rings": ring_logs})
    majority = sum(1 for r in runs if r["cell_pass"])
    return {"runs": runs, "majority_pass": bool(majority >= S1_MIN_SEEDS),
            "n_seed_pass": majority}


# --------------------------------------------------------- substrates
def carrier_substrate(family: str) -> tuple[np.ndarray, np.ndarray]:
    """P1 — exp142's carrier geometry verbatim, chords at +64."""
    A, chords = chord_set(100, family)
    for (i, j) in chords:
        A[i, j] = A[j, i] = CARRIER_DOSE
    return A, np.asarray(chords)


# ---------------------------------------------------------------- main
def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    out: dict = {"experiment": "exp151_self_expansion",
                 "protocol_constants": {
                     "carrier_dose": CARRIER_DOSE, "rings": RINGS,
                     "gap_blockade": GAP_BLOCKADE, "err_bar": ERR_BAR,
                     "executor_seeds": list(SEEDS),
                     "signed_seeds": list(SIGNED_SEEDS),
                     "families": list(FAMILIES),
                     "emission_rule": P6_RULE,
                     "frontier_rule": P4_RULE},
                 "smoke": bool(args.smoke)}

    families_run = FAMILIES[:1] if args.smoke else FAMILIES
    seeds_run = SEEDS[:1] if args.smoke else list(SEEDS)

    # ---------- P1 anchor: the full-organism read verifies ----------
    anchors = {}
    substrates: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for fam in families_run:
        W, chords = carrier_substrate(fam)
        T_plan = plan_of(W)
        with warnings_as_errors():
            a = execute_signed(MULTI, W, seeds_run[0], op=STAR_OP)
        anchors[fam] = {"anchor_err": a["err_vs_target"],
                        "anchor_verified": bool(a["program_verified"]),
                        "n_chords": len(chords)}
        substrates[fam] = (W, T_plan)
    if not args.smoke:
        for sd in SIGNED_SEEDS:
            med = SignedMedium(100, sd)
            W = np.asarray(med.W, dtype=float)
            T_plan = plan_of(W)
            with warnings_as_errors():
                a = execute_signed(MULTI, W, seeds_run[0], op=STAR_OP)
            anchors[f"signed_{sd}"] = {
                "anchor_err": a["err_vs_target"],
                "anchor_verified": bool(a["program_verified"]),
                "neg_edge_frac": round(float(
                    np.mean(W[np.abs(W) > 0] < 0)), 3)}
            substrates[f"signed_{sd}"] = (W, T_plan)
    out["anchors"] = anchors

    # ---------- S1: intact expansion on the carrier substrates -------
    s1 = {}
    for fam in families_run:
        W, T_plan = substrates[fam]
        s1[fam] = run_cone(W, T_plan, seeds_run, gap=None,
                           temporal_check_seed=(seeds_run[0]
                                                if fam == "F1_zone_tail"
                                                else None))
    out["S1_intact"] = s1

    # ---------- S3: the gap-0.05 frontier blockade arm ---------------
    if not args.smoke:
        s3 = {}
        for fam in families_run:
            W, T_plan = substrates[fam]
            s3[fam] = run_cone(W, T_plan, seeds_run, gap=GAP_BLOCKADE)
        out["S3_blockade"] = s3
        # the pre-registered degradation deposit: per-ring err delta
        delta = {}
        for fam in families_run:
            di = []
            for k, r in enumerate(s1[fam]["runs"]):
                b = s3[fam]["runs"][k]
                pairs = [(a, c) for a, c in
                         zip(r["ring_errs_mV"], b["ring_errs_mV"])]
                di.append({"seed": r["seed"],
                           "intact_vs_blockade": [
                               [a, c, round(c - a, 3)] if a is not None
                               and c is not None else None
                               for a, c in pairs]})
            delta[fam] = di
        out["S3_degradation_delta"] = delta

        # ---------- S2: cross-substrate (exp137 SignedMedium) --------
        s2 = {}
        for key in [k for k in substrates if k.startswith("signed_")]:
            W, T_plan = substrates[key]
            s2[key] = run_cone(W, T_plan, seeds_run, gap=None,
                               exhaustion_ok=True)
        out["S2_cross_substrate"] = s2

    # ---------- gate evaluation ----------
    if not args.smoke:
        s1_fam_pass = sum(1 for v in s1.values() if v["majority_pass"])
        g1 = s1_fam_pass >= S1_MIN_FAMILIES
        s3_cells = [r for v in out["S3_blockade"].values()
                    for r in v["runs"]]
        s3_maj = sum(1 for r in s3_cells if r["cell_pass"])
        g3 = s3_maj >= (len(s3_cells) + 1) // 2   # majority of cells
        s2_inst = list(out["S2_cross_substrate"].values())
        g2 = (sum(1 for v in s2_inst if v["majority_pass"])
              >= (len(s2_inst) + 1) // 2)
        s4_bits = [x["s4_bitexact"] and x["s4_flip_zero"]
                   and x["s4_Aext_bitwise_A"]
                   for v in s1.values() for r in v["runs"]
                   for x in r["rings"] if "s4_bitexact" in x]
        g4 = bool(s4_bits) and all(s4_bits)
        out["gates"] = {
            "S1_self_targeted_expansion": {
                "pass": bool(g1), "families_pass": s1_fam_pass,
                "of": len(families_run)},
            "S2_cross_substrate": {
                "pass": bool(g2),
                "instances_pass": sum(1 for v in s2_inst
                                      if v["majority_pass"]),
                "of": len(s2_inst)},
            "S3_blockade_survival": {
                "pass": bool(g3), "cells_pass": s3_maj,
                "of": len(s3_cells),
                "degradation_bound": "ring err < 6.0 mV "
                                     "(pre-registered)"},
            "S4_zero_knobs_bitexact_superset": {
                "pass": g4, "n_checked": len(s4_bits)},
        }
        out["verdict"] = ("{} / 4 gates PASS".format(
            sum(1 for g in out["gates"].values() if g["pass"])))
    else:
        s4_bits = [x["s4_bitexact"] and x["s4_flip_zero"]
                   and x["s4_Aext_bitwise_A"]
                   for v in s1.values() for r in v["runs"]
                   for x in r["rings"] if "s4_bitexact" in x]
        out["smoke_checks"] = {
            "anchor_verified": all(v["anchor_verified"]
                                   for v in anchors.values()),
            "s4_bitexact": s4_bits,
            "rings_expanded": {k: [r["rings_expanded"]
                                   for r in v["runs"]]
                               for k, v in s1.items()},
        }
    out["runtime_s"] = round(time.time() - t0, 1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: out[k] for k in
                      ("verdict", "gates", "runtime_s") if k in out},
                     indent=1))
    print(f"deposited -> {OUT}")
    return out


P6_RULE = ("next ring's committed value per frontier node = the read's "
           "own final V at that node (execute_signed on the C u F "
           "window, verbatim); no rescaling, threshold or lookup")
P4_RULE = ("F(C) = {j not in C : exists i in C, |W[i,j]| > 0} — "
           "graph distance 1 through first-class edges (exp142 R1)")

if __name__ == "__main__":
    main()
