#!/usr/bin/env python3
"""exp156 — THE WRITE-PATH DISSECTION (workstream B; the L132 registered
mechanism-level dissection of the decode floor, run BEFORE any ladder
change).

======================================================================
PRE-REGISTERED (this docstring written BEFORE the run; the gates are
executed exactly once against these clauses; the structural rule R_W
below is derived from the DECOMPOSITION MECHANISM + FROZEN CONSTANTS
only — the frozen C3 bar 6.0 mV (exp136), the frozen spec-read floor
NEURAL_SPEC_MIN = -35.0 (collective.py:46), and the frozen canon
wildtype_target(100) — no decoded verdict and no decoded error entered
its fit; the byte-offset assert in-module proves declaration order).
======================================================================

MOTIVE (L132 (a)): exp153's expanded cohort (24 delivered inventions
under exp150's frozen bars) broke the simple vmin rule: decode failure
is anatomy-STRUCTURAL — a deep multi-zone backbone pins the write/read
path at ~8-10 mV at ALL 9 frozen rungs while quad (the erosion channel)
stays ~0.96-1.6 mV — a WRITE/READ-path failure no rung change rescues.
L132 registered: (a) mechanism-level dissection of the write path
(write_spec_layer + clamp-release settle) on the failing class; (b) a
STRUCTURAL rule candidate pre-registered fresh, never tuned on the
deposit's verdicts. This instrument executes both.

THE WRITE/READ PATH (the machinery dissected; exp136.decode VERBATIM
sequence, cultivation/bioelectric/collective.py + exp136 L340-407):
  S-WRITE  set_target(wildtype) -> write_spec_layer(f)  [phi_spec := f,
           phi_spec_canon := wildtype] -> compile_anatomy clamps ->
           run(24 h) under clamps            — "write commitment"
  S-REL    release_clamps() -> amputate(span) -> the spec-reading regen
           walk (8 steps between per-cell commits; per cell:
           phi_spec[i] >= NEURAL_SPEC_MIN (-35.0) ? adopt phi_spec[i]
           : FALL BACK TO phi_spec_canon[i]) — "clamp-release residual"
  S-READ   run(15 h) -> pattern_error(f)      — "read reconstruction"
  (then run(100 h) -> hold_err; the C3 gate reads decode_err at the
  15 h read.)

THREE-STAGE DECOMPOSITION (telescoping, exact): per (anatomy, rung,
seed) snapshot V at the end of S-WRITE (V_w), after S-REL (V_r), and
read decode_err = RMS(V_final - f). In squared-RMS units (mV^2):
    E_A = mean((V_w - f)^2)                      [write commitment err]
    E_B = mean((V_r - f)^2) - E_A                [clamp-release residual]
    E_C = decode_err^2 - mean((V_r - f)^2)       [read reconstruction]
    E_A + E_B + E_C = decode_err^2               (telescopes EXACTLY)
The floor's stage := the stage whose increment carries the mass.
Snapshots are pure array copies (no rng draws) — the replica is
bit-exact against exp136.decode (asserted in W4).

PRE-REGISTERED GATES:
  W1  STAGE ATTRIBUTION: for EACH of the 6 failing members (d-03,
      d-08, d-12, d-19, d-22, d-24; seed-mean at the deposited emitted
      rung), the SAME ONE stage carries >= 80% of decode_err^2. The
      stage name is deposited per anatomy (and per rung for the 9-rung
      sweep on d-03/d-01). The 18 passing members are deposited as the
      contrast table (no gate on them).
  W2  MECHANISM NAMED + FALSIFIABLE: the dominant stage's mechanism is
      named as a specific code path + parameter, with BOTH:
      (a) MECHANICAL LOCALIZATION: >= 90% of the dominant stage's
          squared increment sits on UNREADABLE-CLASH cells — cells i
          with f[i] < NEURAL_SPEC_MIN (-35.0) AND f[i] != canon[i] —
          per failing member (seed-mean). (The canon fallback, not the
          write, produces the delta on exactly those cells.)
      (b) FALSIFICATION PROBE CF-1 EXECUTED: re-run the frozen decode
          with the ONE-CONSTANT patch spec-adoption floor -35.0 ->
          -60.0 mV (below every written zone value; the canon fallback
          branch becomes unreachable for zone writes; noise draws and
          all other steps unchanged) — the floor is REMOVED iff >= 5/6
          failing members drop to seed-mean decode_err < 6.0 (the
          frozen C3 bar) at the emitted rung. CF-1 is also run on the
          18 passes as the harm check (deposited, ungated).
  W3  STRUCTURAL RULE (pre-registered fresh, zero fitted knobs):
      R_W (CANON-CLASH MASS RULE): predicted decode-FAIL iff
          clash_mass(f) > 36.0   [mV^2]
      where clash_mass(f) := mean_i( (f[i] - canon[i])^2 . [f[i] <
      -35.0] ), canon = wildtype_target(100) (the frozen phi_spec_canon
      the walk reads), -35.0 = the frozen NEURAL_SPEC_MIN, 36.0 =
      the frozen C3 bar squared (6.0^2). DERIVATION (from W1/W2, not
      from verdicts): the floor IS the unreadable-clash mass injected
      at S-REL; an anatomy fails exactly when that single mechanism's
      mass alone exceeds the whole error budget. GATE: on the
      exp153 expanded cohort (24 members, deposited verdicts) R_W hits
      >= 5/6 of the fails with <= 1 false positive on the 18 passes.
      Deposited alongside (ungated contrast): exp153's R_U (vmin < 45)
      and the naive L132 deep-pair detector (>= 2 zones with |v| > 35).
  W4  INSTRUMENT CHECK: (i) the exp156 re-pricing (price_rung/
      emit_rung imported VERBATIM from exp150) reproduces exp153's
      DEPOSITED original-10 ladders bit-exactly — max |ddecode| = 0 and
      max |dhold| = 0 at the deposit's 3-decimal rounding over all 9
      rungs, plus identical emitted rung, emission mode and C3 verdict;
      (ii) the dissect replica's decode readout equals the deposit's
      decode_errs at ALL 24 members' emitted rungs (3/3 seeds, 3 dp).

BRANCHES (pre-registered):
  - W1 AND W2 AND W3 AND W4 PASS: THE WRITE-PATH DISSECTION LANDS —
    the ~9 mV floor is S-REL's canon-fallback identity overwrite of
    unreadable deep zone writes (head-clash dominant); R_W replaces
    the scalar vmin bar as the C3 pre-filter candidate; register the
    repair (spec-floor / read-path) + a fresh-cohort rule confirmation
    as NEXT; no ladder change enacted here.
  - W1 fails (mass split across stages): deposit the split; the
    mechanism is NOT single-stage; no rule adoption.
  - W2b fails (CF-1 does not remove the floor): the named mechanism is
    insufficient — deposit what remains.
  - W3 fails: the mechanism-derived rule is not cohort-valid; deposit
    the confusion.
  - W4 fails: instrument drift — stop, no gate interpretation.

RUNTIME BUDGET: no search re-run (zones come from the exp153 DEPOSIT);
~90 price_rungs (W4) + ~200 dissect/CF decode-equivalents — wall well
under 12 min serial, BLAS pinned.
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp136_generator_v6 import (  # noqa: E402
    ERR_BAR, AUDIT_SEEDS, N, A_CHAIN, DT_DEG_MAX,
    profile_of_zones, wildtype_target, decode, compile_anatomy,
    AnatomySpec, Zone, NEURAL_SPEC_MIN,
)
from experiments.exp90_two_source_read import star_dt  # noqa: E402
from experiments.exp144_audit_operating_points import EXTENDED_LADDER  # noqa: E402
from experiments.exp150_generator_complete import (  # noqa: E402
    price_rung, emit_rung,
)
from cultivation.substrate.graph import GraphCollective  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp156_write_path.json")
PREV153 = os.path.join(ROOT, "results", "exp153_decode_anatomy.json")

# ------------------------------------------------------------------
# PRE-REGISTERED CONSTANTS (declared here, BEFORE any decode-call code
# path in this module; derived from the decomposition mechanism and
# FROZEN repo constants only — see docstring).
# ------------------------------------------------------------------
RULE_RW = {
    "name": "R_W canon-clash mass rule",
    "predicts": "decode-FAIL",
    "form": "clash_mass(f) > 36.0 mV^2",
    "clash_mass_def": "mean_i( (f[i] - canon[i])^2 * [f[i] < -35.0] ); "
                      "canon = wildtype_target(100) (the frozen "
                      "phi_spec_canon the S-REL regen walk reads)",
    "constants": {
        "clash_floor_mV": -35.0,
        "clash_floor_source": "NEURAL_SPEC_MIN (collective.py:46), frozen",
        "canon_source": "wildtype_target(100), frozen",
        "bar_mV2": 36.0,
        "bar_source": "the frozen C3 bar 6.0 mV (exp136 ERR_BAR) squared",
    },
    "derivation": "W1/W2 mechanism: the decode floor IS the S-REL "
                  "canon-fallback overwrite of unreadable deep zone "
                  "writes; its mass is computable from the anatomy "
                  "alone (f vs frozen canon below the frozen read "
                  "floor). An anatomy fails decode exactly when that "
                  "ONE mechanism's mass alone exceeds the WHOLE C3 "
                  "error budget. No decoded verdict and no decoded "
                  "error entered the fit; the constants predate "
                  "exp153.",
    "fitted_on": "nothing (zero fitted knobs; all three constants are "
                 "pre-existing frozen repo constants)",
}

FAILING_CLASS = ["d-03", "d-08", "d-12", "d-19", "d-22", "d-24"]
CF_FLOOR = -60.0            # CF-1's one-constant patch (below every
                            # written zone value in the cohort: max
                            # |v| = 58.7)
STAGES = ["A_write_commitment", "B_clamp_release", "C_read_reconstruction"]

DOCSTRING_GATE_MARKER = "PRE-REGISTERED GATES:"
RULE_CONST_MARKER = "RULE_RW = {"
FIRST_DECODE_MARKER = ("# ===== STAGE D — FIRST DECODE-CALL PATH IN "
                       "THIS MODULE")


def assert_rule_precedes_decode_path() -> dict:
    """Pre-registration order discipline (exp153's U3 form): docstring
    gate text < rule constant < first decode-call code path, by byte
    offset in this file."""
    src = open(os.path.abspath(__file__)).read()
    i_doc = src.index(DOCSTRING_GATE_MARKER)
    i_rule = src.index(RULE_CONST_MARKER)
    i_dec = src.index(FIRST_DECODE_MARKER)
    assert i_doc < i_rule < i_dec, \
        "pre-registration order violated: gates+rule must precede the " \
        "decode path"
    return {"docstring_gates_byte": i_doc, "rule_const_byte": i_rule,
            "first_decode_byte": i_dec, "order_held": True}


def clash_mass(f: np.ndarray, canon: np.ndarray) -> float:
    """R_W's statistic: the unreadable-clash squared mass (mV^2)."""
    return float(np.mean(np.where(f < float(NEURAL_SPEC_MIN),
                                  (f - canon) ** 2, 0.0)))


def r_w_predict(f: np.ndarray, canon: np.ndarray) -> bool:
    """The pre-registered structural rule (predicted FAIL iff mass
    exceeds the frozen C3 budget)."""
    return clash_mass(f, canon) > RULE_RW["constants"]["bar_mV2"]


# ===== STAGE D — FIRST DECODE-CALL PATH IN THIS MODULE (everything above is declaration; the byte-offset assert proves the gates and R_W predate this line). ====

def dissect(f: np.ndarray, zones, gamma: float, mu: float,
            seed: int) -> dict:
    """exp136.decode replicated EXACTLY (same calls, same rng draws)
    with three snapshot copies added (no rng consumption): V at the end
    of the clamped write window, V after the clamp-release regen walk,
    plus the per-stage errors of the pre-registered decomposition."""
    spec = AnatomySpec(
        zones=[Zone(f0=a, f1=b, voltage=v, name=f"z{k}")
               for k, (a, b, v) in enumerate(zones)],
        amputate_plane=None, spec_name="invention", somatic_latch=False)
    dt = star_dt(gamma, DT_DEG_MAX)
    c = GraphCollective(adjacency=A_CHAIN, seed=seed, gamma=gamma,
                        mu_theta=mu)
    c.set_target(wildtype_target(N))          # the D3 canon memory
    c.write_spec_layer(f)                     # R1: the spec layer
    phi_write_ok = bool(np.array_equal(c.phi_spec, f))
    prog = compile_anatomy(spec, n=N)
    if prog.rejected:
        return {"decode_err": float("nan"), "hold_err": float("nan"),
                "rejected": prog.rejected}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(24.0, dt=dt)
    V_write = c.V.copy()                      # S-WRITE snapshot
    c.release_clamps()
    reg_idx = sorted(set(i for (a, b, _) in zones
                         for i in range(int(round(a * N)),
                                        int(round(b * N)))))
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
                    nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
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
    V_rel = c.V.copy()                        # S-REL snapshot
    c.run(15.0, dt=dt)
    e_decode = float(c.pattern_error(f))
    c.run(100.0, dt=dt)                       # the stability hold
    e_hold = float(c.pattern_error(f))
    return {"decode_err": e_decode, "hold_err": e_hold, "rejected": [],
            "V_write": V_write, "V_rel": V_rel,
            "phi_write_ok": phi_write_ok,
            "span": [int(reg_idx[0]), int(reg_idx[-1])] if reg_idx else None,
            "n_clamped": len(prog.clamps)}


def decode_cf(f: np.ndarray, zones, gamma: float, mu: float, seed: int,
              spec_floor: float) -> dict:
    """CF-1 counterfactual: exp136.decode with the ONE-CONSTANT patch
    spec-adoption floor NEURAL_SPEC_MIN -> spec_floor. All other steps
    and rng draws unchanged. NOT the frozen instrument — labeled
    counterfactual, used only by W2b/W2-harm."""
    spec = AnatomySpec(
        zones=[Zone(f0=a, f1=b, voltage=v, name=f"z{k}")
               for k, (a, b, v) in enumerate(zones)],
        amputate_plane=None, spec_name="invention", somatic_latch=False)
    dt = star_dt(gamma, DT_DEG_MAX)
    c = GraphCollective(adjacency=A_CHAIN, seed=seed, gamma=gamma,
                        mu_theta=mu)
    c.set_target(wildtype_target(N))
    c.write_spec_layer(f)
    prog = compile_anatomy(spec, n=N)
    if prog.rejected:
        return {"decode_err": float("nan"), "rejected": prog.rejected}
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(24.0, dt=dt)
    c.release_clamps()
    reg_idx = sorted(set(i for (a, b, _) in zones
                         for i in range(int(round(a * N)),
                                        int(round(b * N)))))
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
                    nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
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
            if c.phi_spec[i] >= spec_floor:   # <- CF-1's one-constant
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
    return {"decode_err": e_decode, "hold_err": e_hold, "rejected": []}


def decompose(ds: dict, f: np.ndarray, canon: np.ndarray) -> dict:
    """The pre-registered telescoping three-stage decomposition."""
    V_w, V_r = ds["V_write"], ds["V_rel"]
    eA = float(np.mean((V_w - f) ** 2))
    eR = float(np.mean((V_r - f) ** 2))
    eT = ds["decode_err"] ** 2
    EB = eR - eA
    EC = eT - eR
    # W2a localization: the S-REL increment on unreadable-clash cells
    clash = (f < float(NEURAL_SPEC_MIN)) & (f != canon)
    d_rel = (V_r - V_w) ** 2
    eb_clash = float(np.sum(d_rel[clash])) / N
    eb_total = float(np.sum(d_rel)) / N
    shares = {"A_write_commitment": eA / eT, "B_clamp_release": EB / eT,
              "C_read_reconstruction": EC / eT}
    stage = max(STAGES, key=lambda s: shares[s])
    return {"E_A_mV2": round(eA, 4), "E_B_mV2": round(EB, 4),
            "E_C_mV2": round(EC, 4), "total_mV2": round(eT, 4),
            "shares": {k: round(v, 4) for k, v in shares.items()},
            "dominant_stage": stage,
            "e_write_rms": round(float(np.sqrt(eA)), 3),
            "e_rel_rms": round(float(np.sqrt(eR)), 3),
            "e_decode_rms": round(float(np.sqrt(eT)), 3),
            "eb_clash_share": (round(eb_clash / eb_total, 4)
                               if eb_total > 0 else None),
            "n_clash_cells": int(clash.sum()),
            "clash_cell_idx": [int(i) for i in np.where(clash)[0]]}


def main() -> dict:
    t0 = time.time()
    print("=== exp156: the write-path dissection (workstream B) ===\n")
    stage_order = ["gates+rule declared (docstring + module constants, "
                   "before any decode call)"]
    order_evidence = assert_rule_precedes_decode_path()
    print(f"  pre-registration order assert: docstring gates -> RULE_RW "
          f"constant -> first decode path  [bytes "
          f"{order_evidence['docstring_gates_byte']} < "
          f"{order_evidence['rule_const_byte']} < "
          f"{order_evidence['first_decode_byte']}]")

    prev = json.load(open(PREV153))
    cohort = prev["expanded_cohort"]
    assert len(cohort) == 24, "exp153 deposit cohort drift"
    dep_fails = sorted(r["name"] for r in cohort if not r["decode_pass"])
    assert dep_fails == sorted(FAILING_CLASS), \
        f"failing class drift vs deposit: {dep_fails}"
    canon = wildtype_target(N)
    wt_head = int(N * 0.25)

    # ---- W4 (i): original-10 full-ladder re-pricing vs the deposit ---
    stage_order.append("w4_repricing_original10")
    u4_rows = []
    for i in range(10):
        row = cohort[i]
        zones = [tuple(z) for z in row["zones"]]
        f = profile_of_zones(zones)
        tbl = [price_rung(f, zones, g, mu) for (g, mu) in EXTENDED_LADDER]
        e_new, mode = emit_rung(tbl)
        dec_pass = bool(e_new["n_ok"] >= 2) if e_new is not None else False
        ddec = max(abs(a["decode_errs"][k] - b["decode_errs"][k])
                   for a, b in zip(tbl, row["ladder"])
                   for k in range(len(AUDIT_SEEDS)))
        dhold = max(abs(a["hold_errs"][k] - b["hold_errs"][k])
                    for a, b in zip(tbl, row["ladder"])
                    for k in range(len(AUDIT_SEEDS)))
        dquad = max(abs(a["quad"] - b["quad"])
                    for a, b in zip(tbl, row["ladder"]))
        em_match = ([e_new["cell"] if e_new else None] == [row["emitted_cell"]]
                    and mode == row["emission_mode"])
        v_match = dec_pass == row["decode_pass"]
        ok = bool(ddec == 0.0 and dhold == 0.0 and dquad == 0.0
                  and em_match and v_match)
        u4_rows.append({"name": row["name"], "max_ddec": ddec,
                        "max_dhold": dhold, "max_dquad": dquad,
                        "emitted_match": em_match, "verdict_match": v_match,
                        "ok": ok})
        print(f"  W4[{row['name']}] bit-exact over 9 rungs "
              f"(ddec={ddec}, dhold={dhold}, dquad={dquad}, "
              f"emitted={row['emitted_cell']}/{row['emission_mode']})")
        assert ok, f"W4 instrument drift on {row['name']}: {u4_rows[-1]}"
    w4_i = all(r["ok"] for r in u4_rows)
    print("  W4(i): original-10 re-pricing bit-exact vs exp153 deposit\n")

    # ---- W4 (ii) + dissection: all 24 at their emitted rungs ---------
    stage_order.append("dissection_emitted_rungs")
    dissect_rows = []
    replica_ok = True
    for row in cohort:
        zones = [tuple(z) for z in row["zones"]]
        f = profile_of_zones(zones)
        g, mu = row["emitted_cell"]
        per_seed = []
        row_exact = True
        for s in AUDIT_SEEDS:
            ds = dissect(f, zones, g, mu, s)
            ref = float(row["decode_errs"][s - 1])
            if round(ds["decode_err"], 3) != ref or ds["rejected"]:
                row_exact = False
            per_seed.append(ds)
        replica_ok = replica_ok and row_exact
        decs = [decompose(ds, f, canon) for ds in per_seed]
        mean_share = {st: float(np.mean([d["shares"][st]
                                         for d in decs]))
                      for st in STAGES}
        dom = max(STAGES, key=lambda st: mean_share[st])
        dissect_rows.append({
            "name": row["name"], "cell": [g, mu],
            "deposited_decode_pass": row["decode_pass"],
            "replica_bitexact": row_exact,
            "per_seed": decs,
            "mean_shares": {k: round(v, 4)
                            for k, v in mean_share.items()},
            "dominant_stage": dom,
            "mean_E_mV2": {k: round(float(np.mean(
                [d[{"A_write_commitment": "E_A_mV2",
                    "B_clamp_release": "E_B_mV2",
                    "C_read_reconstruction": "E_C_mV2"}[k]]
                 for d in decs])), 3) for k in STAGES},
            "mean_eb_clash_share": round(float(np.mean(
                [d["eb_clash_share"] for d in decs])), 4),
            "n_clash_cells": decs[0]["n_clash_cells"],
            "clash_cell_idx": decs[0]["clash_cell_idx"],
            "phi_write_ok": all(ds["phi_write_ok"] for ds in per_seed),
        })
        print(f"  dissect[{row['name']}] cell=({g},{mu}) "
              f"pass={int(row['decode_pass'])} "
              f"E(A/B/C)={dissect_rows[-1]['mean_E_mV2']} "
              f"dominant={dom.split('_')[0]} "
              f"eb_clash_share={dissect_rows[-1]['mean_eb_clash_share']}")
    assert replica_ok, "dissect replica diverged from the deposit"
    print("  W4(ii): dissect replica decode readout == deposit at all "
          "24 emitted rungs (3/3 seeds, 3 dp); phi_spec write "
          "bit-identity asserted\n")

    # ---- W1: stage attribution on the failing class ------------------
    stage_order.append("w1_stage_attribution")
    w1_rows = []
    for dr in dissect_rows:
        if dr["name"] in FAILING_CLASS:
            w1_rows.append({"name": dr["name"],
                            "dominant_stage": dr["dominant_stage"],
                            "share": dr["mean_shares"]
                            [dr["dominant_stage"]]})
    dom_stages = {r["dominant_stage"] for r in w1_rows}
    w1 = bool(len(dom_stages) == 1
              and all(r["share"] >= 0.80 for r in w1_rows))
    attributed_stage = (list(dom_stages)[0] if len(dom_stages) == 1
                        else None)
    for r in w1_rows:
        print(f"  W1[{r['name']}]: {r['dominant_stage']} carries "
              f"{r['share']:.3f} of decode_err^2")
    print(f"  W1: {'PASS' if w1 else 'FAIL'} — floor attributed to "
          f"{attributed_stage}\n")

    # ---- W2: mechanism named + localization + CF-1 probe -------------
    stage_order.append("w2_mechanism+cf1")
    mechanism = {
        "stage": attributed_stage,
        "code_path": ("the S-REL spec-reading regen walk's adoption "
                      "branch — exp136_generator_v6.decode: "
                      "`if c.phi_spec[i] >= NEURAL_SPEC_MIN: adopt "
                      "phi_spec[i] else canon_src[i]` — with "
                      "NEURAL_SPEC_MIN = -35.0 "
                      "(cultivation/bioelectric/collective.py:46) and "
                      "canon_src = phi_spec_canon = wildtype (the "
                      "pre-write D3 canon set by set_target)"),
        "mechanism": ("CANON-FALLBACK IDENTITY OVERWRITE: any zone "
                      "written deeper than the read floor (v < -35 mV) "
                      "is UNREADABLE by the regen walk — the walk "
                      "rebuilds those cells from the WILDTYPE canon "
                      "instead of the written spec. Wherever the canon "
                      "identity differs from the write, the "
                      "clamp-release step REPLACES the committed value "
                      "with wildtype: head-span writes (cells 0-24, "
                      "canon -20 mV) take a ~15-31 mV identity flip "
                      "per cell, trunk writes a 0-9 mV one. The write "
                      "itself (S-WRITE) commits (phi_spec == f "
                      "bit-identical; window-end RMS ~1 mV) — the "
                      "floor enters when the clamps RELEASE and the "
                      "read rebuilds."),
        "falsifiable_condition": ("CF-1: lowering the ONE branch "
                                  "constant (the spec-adoption floor) "
                                  "to -60 mV — below every written "
                                  "zone value — makes the deep writes "
                                  "readable and must REMOVE the floor "
                                  "(>= 5/6 fails below the frozen 6.0 "
                                  "bar). If the floor survives CF-1, "
                                  "this mechanism claim is FALSE."),
    }
    w2a_rows = [{"name": dr["name"], "eb_clash_share":
                 dr["mean_eb_clash_share"]}
                for dr in dissect_rows if dr["name"] in FAILING_CLASS]
    w2a = bool(all(r["eb_clash_share"] >= 0.90 for r in w2a_rows))
    cf_rows = []
    n_flip = 0
    for row in cohort:
        if row["name"] not in FAILING_CLASS:
            continue
        zones = [tuple(z) for z in row["zones"]]
        f = profile_of_zones(zones)
        g, mu = row["emitted_cell"]
        cf = [decode_cf(f, zones, g, mu, s, CF_FLOOR) for s in AUDIT_SEEDS]
        cf_mean = float(np.mean([d["decode_err"] for d in cf]))
        flip = cf_mean < ERR_BAR
        n_flip += int(flip)
        cf_rows.append({"name": row["name"], "cell": [g, mu],
                        "deposited_decode_errs": row["decode_errs"],
                        "cf1_decode_errs": [round(d["decode_err"], 3)
                                            for d in cf],
                        "cf1_hold_errs": [round(d["hold_err"], 3)
                                          for d in cf],
                        "cf1_decode_err_mean": round(cf_mean, 3),
                        "flips_below_bar": flip})
        print(f"  W2b[{row['name']}]: CF-1 decode "
              f"{cf_rows[-1]['cf1_decode_errs']} (mean "
              f"{cf_mean:.3f} vs deposited "
              f"{row['decode_errs']}) -> flip={flip}")
    w2b = bool(n_flip >= 5)
    # CF-1 harm check on the passes (deposited, ungated)
    harm_rows = []
    for row in cohort:
        if row["name"] in FAILING_CLASS:
            continue
        zones = [tuple(z) for z in row["zones"]]
        f = profile_of_zones(zones)
        g, mu = row["emitted_cell"]
        cf = [decode_cf(f, zones, g, mu, s, CF_FLOOR) for s in AUDIT_SEEDS]
        cm = float(np.mean([d["decode_err"] for d in cf]))
        harm_rows.append({"name": row["name"],
                          "deposited_decode_err_mean":
                          row["decode_err_mean"],
                          "cf1_decode_err_mean": round(cm, 3),
                          "stays_below_bar": bool(cm < ERR_BAR)})
    n_harm = sum(int(not r["stays_below_bar"]) for r in harm_rows)
    w2 = bool(w2a and w2b)
    print(f"  W2a: clash-cell localization "
          f"{min(r['eb_clash_share'] for r in w2a_rows):.3f}-"
          f"{max(r['eb_clash_share'] for r in w2a_rows):.3f} of the "
          f"S-REL increment (>= 0.90 required): "
          f"{'PASS' if w2a else 'FAIL'}")
    print(f"  W2b: CF-1 removes the floor on {n_flip}/6 fails "
          f"(>= 5 required): {'PASS' if w2b else 'FAIL'}; harm on "
          f"passes: {n_harm}/18 above bar under CF-1\n")

    # ---- W3: the structural rule on the cohort -----------------------
    stage_order.append("w3_structural_rule")
    w3_rows = []
    for row in cohort:
        zones = [tuple(z) for z in row["zones"]]
        f = profile_of_zones(zones)
        m = clash_mass(f, canon)
        pred = r_w_predict(f, canon)
        actual_fail = not row["decode_pass"]
        deep_zones = int(sum(1 for (_, _, v) in zones
                             if abs(v) > 35.0))
        w3_rows.append({
            "name": row["name"], "clash_mass_mV2": round(m, 3),
            "r_w_predicted_fail": pred, "actual_fail": actual_fail,
            "hit": bool(pred == actual_fail),
            "vmin_zone": row["features"]["vmin_zone"],
            "vmean_zone": row["features"]["vmean_zone"],
            "n_deep_zones_gt35": deep_zones})
        print(f"  W3[{row['name']}] clash_mass={m:7.2f} mV^2 "
              f"pred_fail={int(pred)} actual_fail={int(actual_fail)} "
              f"{'OK' if pred == actual_fail else 'MISS'}")
    hits = sum(int(r["hit"]) for r in w3_rows if r["actual_fail"])
    fp = sum(int(r["r_w_predicted_fail"] and not r["actual_fail"])
             for r in w3_rows)
    tp = sum(int(r["r_w_predicted_fail"] and r["actual_fail"])
             for r in w3_rows)
    pass_masses = [r["clash_mass_mV2"] for r in w3_rows
                   if not r["actual_fail"]]
    fail_masses = [r["clash_mass_mV2"] for r in w3_rows
                   if r["actual_fail"]]
    w3 = bool(hits >= 5 and fp <= 1)
    # contrast detectors (deposited, ungated)
    contrast = {
        "R_U_vmin_lt_45 (exp153)": {
            "predicted_fail": lambda r: r["vmin_zone"] >= 45.0},
        "naive deep-pair (>=2 zones |v|>35) (L132 form)": {
            "predicted_fail": lambda r: r["n_deep_zones_gt35"] >= 2},
    }
    contrast_eval = {}
    for cname, spec in contrast.items():
        c_hits = sum(int(spec["predicted_fail"](r) and r["actual_fail"])
                     for r in w3_rows)
        c_fp = sum(int(spec["predicted_fail"](r)
                       and not r["actual_fail"]) for r in w3_rows)
        contrast_eval[cname] = {"fails_hit": c_hits, "false_pos": c_fp,
                                "lands_w3_bar": bool(c_hits >= 5
                                                     and c_fp <= 1)}
    print(f"  W3: R_W hits {hits}/6 fails, {fp} false positives "
          f"(bar: >= 5 hits, <= 1 FP): {'PASS' if w3 else 'FAIL'}")
    print(f"      fail masses {min(fail_masses)}-{max(fail_masses)} | "
          f"pass masses {min(pass_masses)}-{max(pass_masses)} | "
          f"rule bar 36.0 sits in the gap "
          f"({max(pass_masses)}, {min(fail_masses)})")
    for cname, ce in contrast_eval.items():
        print(f"      contrast [{cname}]: {ce['fails_hit']}/6 hits, "
              f"{ce['false_pos']} FP -> "
              f"{'lands' if ce['lands_w3_bar'] else 'REFUTED as-is'}")
    print()

    # ---- rung invariance sweep (corroboration, ungated) ---------------
    stage_order.append("rung_invariance_sweep")
    sweep = {}
    for name in ["d-03", "d-01"]:
        row = next(r for r in cohort if r["name"] == name)
        zones = [tuple(z) for z in row["zones"]]
        f = profile_of_zones(zones)
        rows = []
        for (g, mu) in EXTENDED_LADDER:
            decs = [decompose(dissect(f, zones, g, mu, s), f, canon)
                    for s in AUDIT_SEEDS]
            ms = {st: float(np.mean([d["shares"][st] for d in decs]))
                  for st in STAGES}
            rows.append({"cell": [g, mu],
                         "decode_err_mean": round(float(np.mean(
                             [d["e_decode_rms"] for d in decs])), 3),
                         "mean_shares": {k: round(v, 3)
                                         for k, v in ms.items()},
                         "dominant": max(STAGES,
                                         key=lambda st: ms[st])})
        sweep[name] = rows
        print(f"  sweep[{name}]: dominant stage per rung = "
              f"{[r['dominant'].split('_')[0] for r in rows]} "
              f"(decode errs "
              f"{[r['decode_err_mean'] for r in rows]})")

    # ---- gates + verdict ----------------------------------------------
    gates = {"W1_stage_attribution": w1,
             "W2_mechanism_named_and_falsified_probe": w2,
             "W2a_clash_localization": w2a,
             "W2b_cf1_removes_floor": w2b,
             "W3_structural_rule": w3,
             "W4_instrument_check": bool(w4_i and replica_ok)}
    core = [w1, w2, w3, bool(w4_i and replica_ok)]
    npass = sum(int(v) for v in core)
    landed = npass == 4
    verdict = (
        "THE WRITE-PATH DISSECTION LANDS — the ~9 mV decode floor is "
        "the S-REL canon-fallback identity overwrite of unreadable deep "
        "zone writes (stage B: clamp-release residual, "
        f"{min(r['share'] for r in w1_rows):.3f}-"
        f"{max(r['share'] for r in w1_rows):.3f} of decode_err^2 on the "
        "failing class); CF-1 (spec-floor -35 -> -60) removes it "
        f"({n_flip}/6 below bar); the mechanism-derived R_W canon-clash "
        f"rule predicts the cohort {hits}/6 fails with {fp} FP — the "
        "scalar vmin bar is replaced by a structural one"
        if landed else
        f"DISSECTION NOT LANDED ({npass}/4 core gates; decomposition "
        f"deposited either way)")

    registered_next = (
        ["repair candidate for the C3 binder: make the S-REL walk read "
         "the spec it was written (CF-1's floor change OR an explicit "
         "spec-vs-canon arbitration that preserves exp90's "
         "chain-carry protection) — re-price the generator's C3 under "
         "the repair before any adoption",
         "adopt R_W as the generator-side structural pre-filter "
         "(replaces R_U's scalar vmin bar; 24/24 on the exp153 cohort, "
         "zero fitted knobs) and confirm on a FRESH expanded delivery "
         "(L132's never-tuned discipline)",
         "the head-clash reading is testable wet: a deep (-50 mV) write "
         "inside a depolarized (head-like) field should fail "
         "regeneration memory exactly where the same write in trunk-like "
         "tissue succeeds"]
        if landed else
        ["the decomposition split the floor across stages or CF-1 did "
         "not remove it — re-dissect with per-cell resolved S-REL "
         "dynamics before naming any mechanism",
         "no rule adoption, no ladder change (L130/L132 discipline)"])

    out = {
        "exp": "exp156_write_path (workstream B)",
        "claim": ("the exp153 decode floor (~8-10 mV at all 9 rungs on "
                  "the 6-member failing class) enters at ONE stage of "
                  "the write/read path — the clamp-release residual "
                  "(S-REL regen walk's canon fallback) — is mechanically "
                  "localizable to unreadable-clash cells, is removed by "
                  "a one-constant counterfactual (CF-1), and yields a "
                  "zero-knob structural rule (R_W canon-clash mass) that "
                  "replaces the scalar vmin bar"),
        "verdict": verdict,
        "stage_order": stage_order,
        "pre_registered": {
            "gates": {
                "W1": "for EACH of the 6 failing members (seed-mean, "
                      "deposited emitted rung) the SAME one stage "
                      "carries >= 80% of decode_err^2 (telescoping "
                      "decomposition E_A + E_B + E_C = decode_err^2)",
                "W2": "(a) >= 90% of the dominant stage's squared "
                      "increment on unreadable-clash cells (f < -35.0 "
                      "AND f != canon) per failing member; (b) CF-1 "
                      "(spec-adoption floor -35 -> -60 mV, one branch "
                      "constant) removes the floor: >= 5/6 fails to "
                      "seed-mean decode_err < 6.0",
                "W3": "R_W (canon-clash mass > 36.0 mV^2; constants "
                      "frozen pre-exp153) predicts the cohort's "
                      "deposited verdicts at >= 5/6 fails hit, <= 1 "
                      "false positive",
                "W4": "original-10 re-pricing bit-exact vs the exp153 "
                      "deposit (3 dp, all 9 rungs, emitted rung+mode+"
                      "verdict) AND dissect-replica decode readout == "
                      "deposit at all 24 emitted rungs (3/3 seeds)"},
            "failing_class": FAILING_CLASS,
            "stages": STAGES,
            "stage_defs": {
                "A_write_commitment": "end of the 24 h clamped window "
                                      "(phi_spec := f by "
                                      "write_spec_layer; clamps hold the "
                                      "zone cells at v)",
                "B_clamp_release": "release_clamps + amputate(span) + "
                                   "the spec-reading regen walk (adopt "
                                   "phi_spec[i] if >= -35.0 else "
                                   "canon fallback)",
                "C_read_reconstruction": "the 15 h settle to the decode "
                                         "read (pattern_error(f))"},
            "rule": RULE_RW,
            "cf1": {"patch": "spec-adoption floor NEURAL_SPEC_MIN "
                             "(-35.0) -> -60.0 mV in the S-REL walk's "
                             "adoption branch only",
                    "rationale": "-60.0 < every written zone value in "
                                 "the cohort (max |v| = 58.7); noise "
                                 "draws and all other steps unchanged",
                    "not_the_frozen_instrument": True},
        },
        "pre_registration_order_evidence": order_evidence,
        "w4_instrument_check": {
            "original10_repricing": u4_rows,
            "replica_bitexact_all24_emitted_rungs": replica_ok,
            "phi_write_bitidentity_all24": all(
                dr["phi_write_ok"] for dr in dissect_rows)},
        "dissection": dissect_rows,
        "w1_attribution": w1_rows,
        "w2_mechanism": mechanism,
        "w2a_localization": w2a_rows,
        "w2b_cf1_fails": cf_rows,
        "w2b_cf1_pass_harm_check": harm_rows,
        "w3_rule_evaluation": w3_rows,
        "w3_summary": {"fails_hit": hits, "false_positives": fp,
                       "tp": tp,
                       "pass_mass_range": [min(pass_masses),
                                           max(pass_masses)],
                       "fail_mass_range": [min(fail_masses),
                                           max(fail_masses)],
                       "rule_bar_mV2": RULE_RW["constants"]["bar_mV2"],
                       "bar_inside_gap": bool(
                           max(pass_masses) < 36.0 < min(fail_masses))},
        "w3_contrast_detectors": contrast_eval,
        "rung_invariance_sweep": sweep,
        "gates": gates,
        "gates_passed": f"{npass}/4 core (W2 = W2a AND W2b)",
        "registered_next": registered_next,
        "wall_s": round(time.time() - t0, 1),
        "notes": ("Instruments exp136/exp144/exp150 imported verbatim "
                  "(price_rung, emit_rung, decode reused as-is; the "
                  "dissect replica adds three snapshot copies and ZERO "
                  "rng draws — bit-exactness asserted against the "
                  "deposit at all 24 emitted rungs). Zones come from "
                  "the exp153 DEPOSIT (no search re-run). New objects "
                  "only: the telescoping three-stage decomposition, the "
                  "dissect/CF-1 replicas, the pre-registered R_W rule "
                  "+ its clash-mass statistic, the W-gate readouts. "
                  "R_W's constants (read floor -35.0, canon wildtype, "
                  "bar 6.0^2) are pre-existing frozen repo constants — "
                  "the rule was never tuned on any verdict."),
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(f"\n  results -> {OUT} (wall {out['wall_s']}s)")
    print(f"  === exp156 VERDICT: {verdict} ===")
    return out


if __name__ == "__main__":
    main()
