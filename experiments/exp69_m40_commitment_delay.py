#!/usr/bin/env python3
"""exp69 — M40: COMMITMENT-RATE COUPLING (night nine continuous batch;
ledger L50).

Registered at exp66 (L47) after the washout-pulse refutation: the
chain RE-CARRIES blind-committed identity (the model's washout arm
rates 0.67 while e329 recorded 0.00), and pub20's whole series runs
cooler than blind-commitment predicts. THE CANDIDATE: blastema cells
under acute blockade DELAY commitment — they do not lock identities
they cannot read. The rate law: cell_period_eff = cell_period x
(1 + D x (1 - r)) — pure rate law on the inter-commit dynamics;
D=0 bit-exact (the calibrated sustained arms untouched BY
CONSTRUCTION at D=0; the gates below test the preservation at D>0).

PRE-REGISTERED GATES (fixed BEFORE running):

  M40-G1  BIT-EXACT AT D=0: the delayed and undelayed sustained
          arms agree to 1e-9.
  M40-G2  THE CONSTRAINT SWEEP (D in {1, 2, 4, 8}, pre-registered):
          the WASHOUT arm (e329 semantics: blockade 0 -> 2 h, then
          full coupling; inline rate-law walk) must reach rate <=
          0.34 (recorded 0.00, n=1) WHILE the SUSTAINED innexin-tail
          arm at the same D stays within +-0.34 of its D=0 rate (the
          exp27/31-calibrated signature must survive). The D
          satisfying both is the ADOPTED operating point.
  M40-G3  DOSE MONOTONICITY at the adopted D: abnormality across
          blockade windows {1, 2, 3, sustained} is non-decreasing
          (pub20's own direction: washout 0.00 < delayed-sustained
          0.19 < sustained ~0.67).
  M40-G4  THE M33 RESCUE SURVIVES: the sustained-blockade head arm
          (post-M33) stays 0.00 at the adopted D.

RUN: rate-law walk (inline for the washout arms; model regrow for
the sustained arms). Serial, BLAS pinned.
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

from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, make_collective,
)
from experiments.exp32_m26_repairs import HEAD, TAILP  # noqa: E402
from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp69_m40_commitment_delay.json")

WT = wildtype_target(N)
ABN_ERR_MV, ABN_HL = 6.0, 0.7
SEEDS = (1, 2, 3)


def washout_arm(seed: int, D: float, block_hours: float = 2.0) -> bool:
    """e329's semantics with the M40 rate law: the walk's per-commit
    duration scales with (1 + D(1-r)); r switches 0.05 -> 1.0 at
    block_hours of walk time."""
    c = make_collective(seed)
    c.gap_scale = 0.05
    c.G = c.G0 * c.gap_scale
    c.deg = c.G.sum(axis=1)
    c.run(24, dt=DT)
    c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
    idx = list(range(TAILP.start, N))
    wound_center = float(np.mean(c.theta[idx]))
    src = idx[0] - 1
    r = 0.05
    t = 0.0
    wash = block_hours
    for i in idx:
        dur = 0.8 * (1.0 + D * (1.0 - r))
        steps = max(1, int(round(dur / DT)))
        for _ in range(steps):
            c.step(dt=DT)
            t += DT
            if t >= wash and r != 1.0:
                r = 1.0
        chain_base = c.theta[src]
        theta_new = chain_base + c.rng.normal(0.0, 0.6)
        if r < 1.0:
            guess = wound_center + c.rng.normal(
                0.0, c.blastema_readout_noise)
            theta_new = r * theta_new + (1.0 - r) * guess
        c.theta[i] = theta_new
        c.V[i] = theta_new
        src = i
    c.run(15, dt=DT)
    rerr = float(np.mean(np.abs(c.V[TAILP] - WT[TAILP])))
    return bool(rerr >= ABN_ERR_MV
                or head_likeness(c.V, TAILP) >= ABN_HL)


def sustained_arm(seed: int, D: float, plane: str = "tail") -> bool:
    c = make_collective(seed)
    c.block_gap_junctions(0.05)
    c.run(24, dt=DT)
    kw = dict(cell_period=0.8, dt=DT, noise=0.6,
              phi_readout=0.75, neural_readout=1.0, arz_readout=1.0,
              commitment_delay=D)
    if plane == "tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, **kw)
        reg = TAILP
    else:
        c.amputate(HEAD, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(HEAD, direction="backward", **kw)
        reg = HEAD
    rerr = float(np.mean(np.abs(c.V[reg] - WT[reg])))
    return bool(rerr >= ABN_ERR_MV
                or head_likeness(c.V, TAILP) >= ABN_HL)


def main() -> dict:
    print("=== exp69: M40 commitment-rate coupling ===\n")

    # ---- M40-G1: bit-exact at D=0 -------------------------------------------
    c1 = make_collective(5)
    c1.gap_scale = 0.05; c1.G = c1.G0 * 0.05; c1.deg = c1.G.sum(axis=1)
    c1.run(24, dt=DT)
    c1.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
    c1.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6)
    c2 = make_collective(5)
    c2.gap_scale = 0.05; c2.G = c2.G0 * 0.05; c2.deg = c2.G.sum(axis=1)
    c2.run(24, dt=DT)
    c2.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
    c2.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6, commitment_delay=0.0)
    exact = float(np.max(np.abs(c1.V - c2.V))) == 0.0
    m40_g1 = bool(exact)
    print(f"  M40-G1 bit-exact at D=0: {exact} "
          f"-> {'PASS' if m40_g1 else 'REFUTED'}")

    # ---- M40-G2: the constraint sweep -----------------------------------------
    d0_sust = float(np.mean([sustained_arm(s, 0.0) for s in SEEDS]))
    print(f"  sustained tail at D=0: {d0_sust:.2f} (the calibrated "
          f"reference)")
    sweep = {}
    adopted_D = None
    for D in (1.0, 2.0, 4.0, 8.0):
        wr = float(np.mean([washout_arm(s, D) for s in SEEDS]))
        sr = float(np.mean([sustained_arm(s, D) for s in SEEDS]))
        ok = bool(wr <= 0.34 and abs(sr - d0_sust) <= 0.34)
        sweep[D] = {"washout_rate": wr, "sustained_rate": sr, "ok": ok}
        print(f"  D={D}: washout {wr:.2f} (bar 0.34), sustained "
              f"{sr:.2f} (delta {abs(sr - d0_sust):.2f}) "
              f"{'<- ADOPTED' if ok and adopted_D is None else ''}")
        if ok and adopted_D is None:
            adopted_D = D
    m40_g2 = adopted_D is not None
    print(f"  M40-G2 constraint sweep: adopted D = {adopted_D} "
          f"-> {'PASS' if m40_g2 else 'REFUTED'}")

    # ---- M40-G3: dose monotonicity --------------------------------------------
    if adopted_D is not None:
        doses = {}
        for bh in (1.0, 2.0, 3.0):
            doses[bh] = float(np.mean(
                [washout_arm(s, adopted_D, block_hours=bh)
                 for s in SEEDS]))
        doses["sustained"] = sweep[adopted_D]["sustained_rate"]
        vals = [doses[k] for k in (1.0, 2.0, 3.0, "sustained")]
        m40_g3 = all(vals[i] <= vals[i + 1] + 1e-9
                     for i in range(len(vals) - 1))
        print(f"  M40-G3 dose response at D={adopted_D}: "
              f"{ {k: round(v, 2) for k, v in doses.items()} } "
              f"-> {'PASS' if m40_g3 else 'REFUTED'}")
    else:
        m40_g3 = False
        print("  M40-G3 skipped (no adopted D)")

    # ---- M40-G4: the M33 rescue survives ---------------------------------------
    if adopted_D is not None:
        head_rate = float(np.mean([sustained_arm(s, adopted_D,
                                                 plane="head")
                                   for s in SEEDS]))
        m40_g4 = bool(head_rate == 0.0)
        print(f"  M40-G4 sustained head at adopted D: {head_rate:.2f} "
              f"-> {'PASS' if m40_g4 else 'REFUTED'}")
    else:
        m40_g4 = False
        print("  M40-G4 skipped (no adopted D)")

    out = {
        "exp": "exp69_m40_commitment_delay",
        "rate_law": "cell_period_eff = cell_period * (1 + D*(1-r)); "
                    "D=0 bit-exact",
        "constraint_sweep": {str(k): v for k, v in sweep.items()},
        "adopted_D": adopted_D,
        "criteria": {
            "M40_G1_bit_exact": bool(m40_g1),
            "M40_G2_constraint_sweep": bool(m40_g2),
            "M40_G3_dose_monotone": bool(m40_g3),
            "M40_G4_m33_rescue_survives": bool(m40_g4),
        },
        "notes": (
            "M40: commitment-rate coupling to coupling state — the "
            "exp66-registered candidate for the washout-pulse "
            "refutation. The constraint sweep is the honest adoption "
            "instrument: D must simultaneously satisfy the washout "
            "record (e329: 0.00 at n=1) AND preserve the calibrated "
            "sustained-blockade signature (exp27/31)."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/4 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
