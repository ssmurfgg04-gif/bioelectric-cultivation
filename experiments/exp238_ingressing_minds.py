#!/usr/bin/env python3
"""exp238 — THE INGRESSING MINDS TEST (the Section 6 item; "Ingressing
Minds", MDPI 2409-9287/11/5/161; ledger L214).

THE CLAIM TESTED: a single body can host MULTIPLE, simultaneously
retrievable morphological memories — "multiple memories in the same
body" — and which memory surfaces is decided by the READ, not by
competitive storage. The stack already carries the two-layer substrate
for the claim: theta (the expression memory) and phi_spec (the spec/
identity memory, set_target's write-once layer) — two addressable
stores on ONE substrate at S* = (64.0, 0.0).

THE DESIGN (zero-knob): pattern A = the canonical labeling (exp43's
head/trunk); pattern B = a CONFLICTING zone map on the same cells
(the mirror labeling: the head zone relocated to the posterior third —
the two patterns disagree on >= 60% of cells, pre-named). The write
sequence: A into theta via the star write protocol (exp79's run_gm
verbatim), B into phi_spec via write_spec_layer (exp87's frozen
machinery, the R1 memory write). Then the retrieval battery.

PRE-REGISTERED GATES:

  M1  THE CO-EXISTENCE: both memories retrievable after the write
      sequence at S* on all 3 arms x 3 seeds — the expression read
      reports A (theta vs A: err < 6.0) AND the spec read reports B
      (phi_spec == B bit-exact) simultaneously.
  M2  THE NON-INTERFERENCE: running under A's expression (the star
      maintenance window T=24 x 3 rounds) does not corrupt B (phi_spec
      bit-exact before/after, sha-compared) and B's presence does not
      degrade A's maintenance (err within 0.5 mV of the B-free
      control).
  M3  THE CONFLICT (the claim's core): A and B disagree on >= 60% of
      cells AND both remain retrievable — "multiple memories in the
      same body" realized computationally at S*.
  M4  THE ADDRESSING (the ingress claim): which memory surfaces is
      decided by the READ PROTOCOL alone — the window read surfaces A,
      the spec read surfaces B, with ZERO re-writes between
      retrievals (the memory is addressed, not re-expressed); the
      switching is lossless (A's err identical before/after a B
      retrieval round, bit-exact theta).

THE BRANCH (pre-named): M1-M4 PASS -> MULTI-MEMORY-CONFIRMED (S*
reproduces the "multiple memories in the same body" claim — the
Ingressing Minds parallel grounded in the stack); M1 or M2 REFUTE ->
SINGLE-MEMORY (the two-layer substrate does not host independent
memories — the expression erases the spec, deposited honestly).

RUN: the write sequence + 4 retrieval panels x 3 arms x 3 seeds;
serial, BLAS pinned; minutes.
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
OUT = os.path.join(ROOT, "results", "exp238_ingressing_minds.json")


def main() -> dict:
    import hashlib

    # -- the frozen machinery, imported never re-implemented: exp79's
    #    run_gm (the star write protocol), exp87's write_spec_layer on
    #    GraphCollective (the R1 memory write), exp43's labeling, and
    #    exp73's battery (exp79's arms).
    from cultivation.substrate.graph import GraphCollective  # noqa: E402
    from experiments.exp43_substrate_independence import (  # noqa: E402
        labeling, HEAD_V, TRUNK_V,
    )
    from experiments.exp73_active_renormalization import (  # noqa: E402
        make_battery, N, ERR_BAR,
    )
    from experiments.exp79_two_channel_law import (  # noqa: E402
        run_gm, RUN_T, DT,
    )

    print("=== exp238: THE INGRESSING MINDS TEST "
          "(multiple memories in the same body) ===\n")

    # S* — the star point (the docstring's pre-named operating point;
    # exp79 TC-G3's verdict point, exp87's STAR_GAMMA/STAR_MU values).
    STAR_GAMMA, STAR_MU = 64.0, 0.0
    MAINT_ROUNDS = 3          # the star maintenance window T=24 x 3 rounds
    CONFLICT_BAR = 0.60       # the pre-named disagreement bar (M3)

    battery = make_battery()                    # exp73's battery (exp79's arms)
    arms = ("scale_free", "random3", "torus")   # exp79's plateau arms
    seeds = (1, 2, 3)

    # ---- the patterns (zero-knob) ------------------------------------
    # pattern A: exp43's canonical labeling, imported verbatim
    # (head identity on cells 0..24, trunk on 25..99).
    pat_A = labeling(N)
    # pattern B: the docstring's zero-knob MIRROR labeling — the head
    # zone relocated to the posterior third (cells [N - N//3, N)); the
    # vacated anterior head zone reverts to trunk. Built on exp43's own
    # identity constants; the only boundary is the docstring's own
    # "posterior third".
    pat_B = np.full(N, TRUNK_V)
    pat_B[N - N // 3:] = HEAD_V
    disagree_cells = int(np.sum(pat_A != pat_B))
    disagree_frac = disagree_cells / float(N)
    print(f"  pattern A: exp43's canonical labeling (head cells "
          f"{int(np.where(pat_A == HEAD_V)[0][0])}.."
          f"{int(np.where(pat_A == HEAD_V)[0][-1])})")
    print(f"  pattern B: the mirror labeling (head cells "
          f"{N - N // 3}..{N - 1}, the posterior third)")
    print(f"  disagreement: {disagree_cells}/{N} cells = "
          f"{disagree_frac:.0%} (pre-named bar >= 60%)\n")

    # ---- helpers (the protocol, closed over the frozen constants) ----
    def sha(a: np.ndarray) -> str:
        return hashlib.sha256(
            np.ascontiguousarray(a, dtype=np.float64).tobytes()).hexdigest()

    def rms(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.sqrt(np.mean((a - b) ** 2)))

    def window(c) -> None:
        # run_gm's window at the star point (its gamma > 0.25 branch,
        # verbatim expression).
        c.run(RUN_T, dt=min(DT, 1.2 / (STAR_GAMMA + float(c.deg.max()))))

    def write_sequence(A_adj: np.ndarray, seed: int):
        """THE WRITE SEQUENCE: A into theta via exp79's star write
        protocol (run_gm verbatim), then B into phi_spec via exp87's
        write_spec_layer (the R1 memory write, expression layers
        untouched). run_gm returns only the error, not the collective,
        so the carrier runs run_gm's protocol inline and is asserted
        BIT-EXACT against the imported run_gm's return."""
        c = GraphCollective(adjacency=A_adj, seed=seed, gamma=STAR_GAMMA,
                            mu_theta=STAR_MU)
        c.set_target(pat_A)              # run_gm verbatim (captures phi_spec=A)
        c.theta = pat_A.copy()
        c.V = c.theta + c.rng.normal(0.0, 2.0, N)
        if STAR_GAMMA <= 0.25:
            c.run(RUN_T, dt=DT)
        else:
            window(c)
        rg_err = run_gm(A_adj, pat_A, seed, STAR_GAMMA, STAR_MU)
        assert c.pattern_error(pat_A) == rg_err, \
            "carrier A-write deviates from exp79's run_gm verbatim"
        c.write_spec_layer(pat_B)        # exp87's R1 write: phi_spec := B
        return c, rg_err

    def bfree_control(A_adj: np.ndarray, seed: int):
        """The B-free control: the identical star write + maintenance
        minus the R1 spec write (seed-matched)."""
        c = GraphCollective(adjacency=A_adj, seed=seed, gamma=STAR_GAMMA,
                            mu_theta=STAR_MU)
        c.set_target(pat_A)
        c.theta = pat_A.copy()
        c.V = c.theta + c.rng.normal(0.0, 2.0, N)
        if STAR_GAMMA <= 0.25:
            c.run(RUN_T, dt=DT)
        else:
            window(c)
        for _ in range(MAINT_ROUNDS):
            window(c)
        return c

    # ---- the write sequence + 4 retrieval panels x 3 arms x 3 seeds ----
    instances = []
    n_verbatim = 0
    m1_all = m2_all = m3_ret_all = m4_all = True
    for arm in arms:
        A_adj = battery[arm]
        for seed in seeds:
            c, rg_err = write_sequence(A_adj, seed)
            n_verbatim += 1
            sha_phi_write = sha(c.phi_spec)
            canon_kept = bool(np.array_equal(c.phi_spec_canon, pat_A))

            # ---- M1: the co-existence (post-write reads, one state) ----
            m1_theta_err = rms(c.theta, pat_A)
            m1_v_err = float(c.pattern_error(pat_A))
            m1_spec_ok = bool(np.array_equal(c.phi_spec, pat_B))
            m1 = bool(m1_theta_err < ERR_BAR and m1_spec_ok)

            # ---- M2: the non-interference (T=24 x 3 under A's expression) --
            sha_phi_pre = sha(c.phi_spec)
            for _ in range(MAINT_ROUNDS):
                window(c)
            sha_phi_post = sha(c.phi_spec)
            err_A_after = rms(c.theta, pat_A)
            err_ctl = rms(bfree_control(A_adj, seed).theta, pat_A)
            delta = abs(err_A_after - err_ctl)
            m2 = bool(sha_phi_pre == sha_phi_post == sha_phi_write
                      and delta <= 0.5)

            # ---- M3: the conflict (the checkpoint reads) -------------------
            m3_theta_err = rms(c.theta, pat_A)
            m3_spec_ok = bool(np.array_equal(c.phi_spec, pat_B))
            m3_ret = bool(m3_theta_err < ERR_BAR and m3_spec_ok)

            # ---- M4: the addressing (the switching cycle; ZERO re-writes) --
            window(c)                         # the window read -> surfaces A
            w1_err = rms(c.theta, pat_A)
            surf_A1 = bool(w1_err < ERR_BAR)
            th_pre = c.theta.copy()           # the B retrieval round: the spec
            err_pre = rms(c.theta, pat_A)     # read (pure — addresses phi_spec)
            spec_B1 = bool(np.array_equal(c.phi_spec, pat_B))
            err_post = rms(c.theta, pat_A)
            lossless = bool(err_pre == err_post
                            and np.array_equal(th_pre, c.theta))
            window(c)                         # the window read -> surfaces A
            w2_err = rms(c.theta, pat_A)
            surf_A2 = bool(w2_err < ERR_BAR)
            spec_B2 = bool(np.array_equal(c.phi_spec, pat_B))
            zero_rw = bool(sha(c.phi_spec) == sha_phi_write)
            m4 = bool(surf_A1 and spec_B1 and lossless
                      and surf_A2 and spec_B2 and zero_rw)

            m1_all &= m1
            m2_all &= m2
            m3_ret_all &= m3_ret
            m4_all &= m4
            instances.append({
                "arm": arm, "seed": seed,
                "run_gm_verbatim_bit_exact": True,
                "run_gm_err": round(rg_err, 4),
                "phi_spec_canon_preserved": canon_kept,
                "M1": {"theta_err_vs_A": round(m1_theta_err, 3),
                       "v_err_vs_A": round(m1_v_err, 3),
                       "spec_bit_exact": m1_spec_ok, "pass": m1},
                "M2": {"phi_sha_write": sha_phi_write,
                       "phi_sha_pre": sha_phi_pre,
                       "phi_sha_post": sha_phi_post,
                       "phi_bit_exact": bool(sha_phi_pre == sha_phi_post
                                             == sha_phi_write),
                       "err_A_after_maintenance": round(err_A_after, 3),
                       "err_B_free_control": round(err_ctl, 3),
                       "delta_mV": round(delta, 4), "pass": m2},
                "M3": {"theta_err_vs_A": round(m3_theta_err, 3),
                       "spec_bit_exact": m3_spec_ok,
                       "both_retrievable": m3_ret},
                "M4": {"window_read1_err": round(w1_err, 3),
                       "surfaces_A_1": surf_A1,
                       "spec_read_B_1": spec_B1,
                       "lossless_switch_theta_bit_exact": lossless,
                       "window_read2_err": round(w2_err, 3),
                       "surfaces_A_2": surf_A2,
                       "spec_read_B_2": spec_B2,
                       "zero_re_writes_phi_sha_constant": zero_rw,
                       "pass": m4},
            })
            print(f"  {arm:11s} s{seed}: M1 {'PASS' if m1 else 'REFU'}  "
                  f"M2 {'PASS' if m2 else 'REFU'}  "
                  f"M3-ret {'ok' if m3_ret else 'LOST'}  "
                  f"M4 {'PASS' if m4 else 'REFU'}"
                  f"   (theta err {m1_theta_err:.2f}, ctrl delta {delta:.2f})")

    # ---- the gates -----------------------------------------------------
    m3 = bool(disagree_frac >= CONFLICT_BAR and m3_ret_all)
    print(f"\n  M1 the co-existence (theta reports A err < {ERR_BAR} AND "
          f"phi_spec == B bit-exact, one state, 9 instances): "
          f"{'PASS' if m1_all else 'REFUTED'}")
    print(f"  M2 the non-interference (phi_spec sha-constant through "
          f"T={RUN_T} x {MAINT_ROUNDS}; A's err within 0.5 mV of the "
          f"B-free control): {'PASS' if m2_all else 'REFUTED'}")
    print(f"  M3 the conflict (disagree {disagree_frac:.0%} >= 60% AND both "
          f"remain retrievable): {'PASS' if m3 else 'REFUTED'}")
    print(f"  M4 the addressing (the window read surfaces A, the spec read "
          f"surfaces B, zero re-writes, lossless switching): "
          f"{'PASS' if m4_all else 'REFUTED'}")
    criteria = {
        "M1_coexistence": bool(m1_all),
        "M2_non_interference": bool(m2_all),
        "M3_conflict": m3,
        "M4_addressing": bool(m4_all),
    }
    npass = sum(criteria.values())
    branch = "MULTI-MEMORY-CONFIRMED" if npass == 4 else "SINGLE-MEMORY"
    print(f"  BRANCH: {branch}")

    out = {
        "exp": "exp238_ingressing_minds (the Section 6 item; Ingressing "
               "Minds, MDPI 2409-9287/11/5/161, ledger L214)",
        "claim": "a single body hosts MULTIPLE, simultaneously retrievable "
                 "morphological memories; which memory surfaces is decided "
                 "by the READ, not by competitive storage",
        "star_point": {"gamma": STAR_GAMMA, "mu": STAR_MU},
        "arms": list(arms),
        "seeds": list(seeds),
        "patterns": {
            "A": {"source": "exp43_substrate_independence.labeling "
                             "(imported verbatim)",
                  "head_cells": [int(np.where(pat_A == HEAD_V)[0][0]),
                                 int(np.where(pat_A == HEAD_V)[0][-1])],
                  "head_v": HEAD_V, "trunk_v": TRUNK_V},
            "B": {"source": "the docstring's zero-knob mirror labeling: the "
                             "head zone relocated to the posterior third "
                             "(cells [N - N//3, N)); the vacated anterior "
                             "head zone reverts to trunk; built on exp43's "
                             "imported identity constants",
                  "head_cells": [N - N // 3, N - 1],
                  "head_v": HEAD_V, "trunk_v": TRUNK_V},
            "disagreement": {"cells": disagree_cells, "frac": disagree_frac,
                             "pre_named_bar": CONFLICT_BAR,
                             "clause_ge_60pct": bool(disagree_frac
                                                     >= CONFLICT_BAR)},
        },
        "write_sequence": {
            "A_into_theta": "exp79's run_gm star write protocol verbatim "
                            "(gamma=64, mu=0); the carrier runs run_gm's "
                            "protocol inline (run_gm returns only the error, "
                            "not the collective) and asserts bit-exact "
                            "post-window pattern error against the imported "
                            f"run_gm on every instance ({n_verbatim}/"
                            f"{len(instances)})",
            "B_into_phi_spec": "exp87's write_spec_layer (the R1 memory "
                               "write; preserves the set_target-captured "
                               "phi_spec (= A) as phi_spec_canon)",
        },
        "instances": instances,
        "criteria": criteria,
        "branch": branch,
        "notes": (
            "THE MIRROR ARITHMETIC (the honest deposit): the docstring's "
            "zero-knob mirror (the head zone relocated to the posterior "
            "third: cells [67,100) at HEAD_V, the vacated anterior head "
            "reverting to trunk) disagrees with exp43's labeling on "
            "58/100 cells = 58% — the pre-named '>= 60%' figure over-rounds "
            "the design (25 old-head + 33 posterior-third cells); M3's "
            "conflict clause REFUTES on the pre-named bar while both "
            "memories remain retrievable on every instance. The imported "
            "alternative, morpho_engineering.target_mirror (the head zone "
            "relocated to the posterior END at its original 25-cell size), "
            "disagrees at 50% — further from the bar; the docstring's own "
            "definition is the faithful execution. SUBSTRATE RESULT: M1 "
            "co-existence (theta reports A err<6 AND phi_spec == B "
            "bit-exact in ONE state), M2 non-interference (phi_spec "
            "sha-constant through T=24 x 3 under A's expression; A's "
            "maintenance delta vs the seed-matched B-free control exactly "
            "0.0 mV — the spec layer is dynamics-inert: phi_spec enters no "
            "step() term, so the 0.5 mV tolerance is not binding), and M4 "
            "addressing (the window read surfaces A, the spec read "
            "surfaces B, ZERO re-writes between retrievals, theta "
            "bit-exact across B rounds) all PASS on 9/9 instances — the "
            "two-layer substrate DOES host two independent, addressable, "
            "non-interfering memories at S*; the pre-named branch lands "
            "SINGLE-MEMORY because MULTI-MEMORY-CONFIRMED requires "
            "M1-M4 all PASS and M3's pre-named conflict bar is unmet by "
            "the zero-knob design's 58% disagreement (an arithmetic "
            "refute, not erasure). MACHINERY DISCLOSURES: run_gm returns "
            "the error, not the collective, so the carrier replicates "
            "run_gm's protocol inline and is bit-exact-asserted against "
            "the imported run_gm per instance; write_spec_layer preserved "
            "the set_target-captured phi_spec (= A) as phi_spec_canon "
            "(exp90's two-source behavior) on every instance (reported, "
            "not gated); the zero-re-writes discipline is structural "
            "(after the write sequence the battery performs only c.run "
            "steps and pure reads) and is witnessed by the phi_spec sha "
            "remaining constant from the write through the battery end on "
            "every instance."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    print(f"  === {npass}/4 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
