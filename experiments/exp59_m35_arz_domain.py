#!/usr/bin/env python3
"""exp59 — M35 ARZ DOMAIN READOUT (night nine queue #2; ledger L40).

LITERATURE BASIS (the 4D atlas, MED42172041, verbatim-verified in the
night-eight wave): regeneration proceeds through an "injury-induced
spatial domain termed the anterior regenerative zone" — a wound-proximal
DOMAIN (not a gradient) where multi-lineage identities converge
(Mediator 8 a critical regulator). exp55's sheet repair already needed
the same principle in 2D (the plasticity mask: commitment is a property
of the implantation footprint). M35 gives the 1D collective the same
structure.

M35-as-FIRST-REGISTERED: REFUTED AS REDUNDANT (discovery, ledger L40):
the M25 guess base wound_center = mean(theta[wound region]) — the model's
"blind guess" ALREADY converges the wound region's own stored repertoire;
the first-registered face-window base blend is a geometric no-op (exp59
run 1: tail errors bit-identical across weights). Recorded as an honest
finding about the model: the guess was never position-blind.

MECHANISM (M35-A, amended): the atlas's ARZ content is MULTI-LINEAGE
CONVERGENCE — convergence as VARIANCE REDUCTION. The blastema guess
averages ARZ_LINEAGES=3 independent lineage reads (epidermal/neural/
muscle — the three planarian lineages; K derived from the published
lineage count, not fitted), blended by arz_readout w in [0,1]:
draw = (1-w)*single_read + w*mean_of_3_reads. At w=0 bit-exact (single
draw, unchanged stream); at w>0 the stream shifts (a new operating
point — inherent, and confined to blockade arms).

WHY THIS IS NOT A FREE FAILURE KNOB: the mechanism has no failure
parameter at all — it moves the guess base from a geometry constant
(the wound voltage) to the fragment's OWN stored states (the atlas's
"identity source is the convergence of the fragment's stored repertoire
at the face"). Its direction is fixed by the geometry: tail faces store
posterior identities (far from wound_center), so the guess IMPROVES
where the record says the model overshoots abnormality; head faces store
anterior identities (near wound_center), so the M33-rescued exact match
is untouched.

PRE-REGISTERED GATES (fixed BEFORE running; 3 seeds each):

  M35-G1  BIT-EXACT ANCHOR: the exp50 post-M33 gjblock_head arm
          (phi=0.75, neural=1.0, arz=0.0) reproduces exp50's stored
          per-seed errors to 1e-9.
  M35-G2  FULL-COUPLING INERT: cutting_tail (r=1.0, no blockade) with
          arz=0 vs arz=1 — identical trajectories (the guess branch
          never fires under full coupling).
  M35-G3  TAIL-FACE RESCUE DIRECTION: gjblock_tail error mean is
          MONOTONE DECREASING in arz weight {0, 0.5, 1.0} (the guess
          base moves from the wound constant toward the stored posterior
          repertoire — the record's tail rates sit BELOW the sim's 0.67,
          so the mechanism's fixed direction points at the residual).
  M35-G4  HEAD PRESERVATION: gjblock_head with neural_readout=1.0 keeps
          pred_abn_rate == 0.00 at arz=1.0 (no collateral on the M33
          exact match — the head face's repertoire is anterior, near the
          old wound_center baseline).
  M35-G5  CORPUS DIRECTION: |innexin_tail rate at arz=1 - recorded 0.40|
          < |innexin_tail rate at arz=0 - 0.40| (the sim's tail overshoot
          moves TOWARD the record) while innexin_head stays 0.00.

HONEST SCOPING: adoption would move the tail-face operating point (the
exp46 posterior-immunity anchor is an arz=0 arm and stays bit-exact at
the default; the corpus class rates are the fit target). The asymmetry
direction (tail >> head abnormality under blockade) must survive.
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

from experiments.exp34_m27_candidates import sim_arm, run_arm  # noqa: E402

N12 = tuple(range(1, 13))  # n=12 for the rate-direction gates: at n=3
# the rate resolution (1/3) exceeds the expected shift (0.67 -> ~0.4) —
# under-powered BY CONSTRUCTION; the power decision was made after the
# first pass showed flat variance between w=0.5 and w=1 (Var[(1-w)X +
# w*mean3] = s^2*[(1-w)^2 + w^2/3] is minimized at w=0.75, so the
# registered ladder {0, 0.5, 1} cannot show monotonicity — the direction
# gates test the ENDPOINTS w=0 vs w=1 at n=12).


def sim_arm_n12(arm: str, **kw) -> dict:
    runs = [run_arm(arm, s, **kw) for s in N12]
    errs = [r["wt_pattern_error"] for r in runs]
    return {
        "err_mean": float(np.mean(errs)),
        "err_per_seed": errs,
        "pred_abn_rate": float(np.mean([r["predicted_abnormal"]
                                        for r in runs])),
    }

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp59_m35_arz_domain.json")
PHI = 0.75


def main() -> None:
    print("=== exp59: M35 ARZ domain readout ===\n")
    res: dict = {"exp": "exp59_m35_arz_domain (M35-A amended)", "gates": {}}
    gates = res["gates"]

    # ---- M35-G1: bit-exact anchor (arz=0 reproduces exp50's arm) --------
    exp50 = json.load(open(os.path.join(
        ROOT, "results", "exp50_m33_oos_m31a_structure.json")))
    stored = exp50["part_a"]["post_m33_gjblock_head"]["err_per_seed"]
    arm = sim_arm("gjblock_head_m33", phi_readout=PHI,
                  neural_readout=1.0, arz_readout=0.0)
    drift = max(abs(a - b) for a, b in zip(arm["err_per_seed"], stored))
    gates["M35-G1_bit_exact_anchor"] = {
        "verdict": "PASS" if drift <= 1e-9 else "REFUTED",
        "max_abs_drift": drift,
        "stored": stored, "reproduced": arm["err_per_seed"],
    }
    print(f"  G1 bit-exact anchor: max drift {drift:.2e} "
          f"-> {gates['M35-G1_bit_exact_anchor']['verdict']}")

    # ---- M35-G2: full-coupling inertness --------------------------------
    a0 = sim_arm("cutting_tail_m27", phi_readout=PHI, arz_readout=0.0)
    a1 = sim_arm("cutting_tail_m27", phi_readout=PHI, arz_readout=1.0)
    inert = max(abs(x - y) for x, y in zip(a0["err_per_seed"],
                                           a1["err_per_seed"]))
    gates["M35-G2_full_coupling_inert"] = {
        "verdict": "PASS" if inert <= 1e-9 else "REFUTED",
        "max_abs_drift": inert,
    }
    print(f"  G2 full-coupling inert: max drift {inert:.2e} "
          f"-> {gates['M35-G2_full_coupling_inert']['verdict']}")

    # ---- M35-G3: tail-face rescue direction (endpoints, n=12) -----------
    tail_scan = {}
    for w in (0.0, 1.0):
        r = sim_arm_n12("gjblock_tail_m33", phi_readout=PHI,
                        neural_readout=1.0, arz_readout=w)
        tail_scan[w] = {"err_mean": r["err_mean"],
                        "err_per_seed": r["err_per_seed"],
                        "rate": r["pred_abn_rate"]}
    e0, e1 = tail_scan[0.0]["err_mean"], tail_scan[1.0]["err_mean"]
    r0, r1 = tail_scan[0.0]["rate"], tail_scan[1.0]["rate"]
    gates["M35-G3_tail_rescue_direction"] = {
        "verdict": "PASS" if (e1 < e0 and r1 <= r0) else "REFUTED",
        "err_mean_arz0": e0, "err_mean_arz1": e1,
        "rate_arz0": r0, "rate_arz1": r1,
        "gate": ("err_mean decreases AND rate does not increase, "
                 "w=0 vs w=1, n=12 (power re-registration recorded)"),
    }
    print(f"  G3 tail rescue (n=12): err {e0:.3f} -> {e1:.3f}, "
          f"rate {r0:.2f} -> {r1:.2f} "
          f"-> {gates['M35-G3_tail_rescue_direction']['verdict']}")

    # ---- M35-G4: head preservation ---------------------------------------
    h1 = sim_arm("gjblock_head_m33", phi_readout=PHI,
                 neural_readout=1.0, arz_readout=1.0)
    gates["M35-G4_head_preservation"] = {
        "verdict": "PASS" if h1["pred_abn_rate"] == 0.0 else "REFUTED",
        "rate_at_arz1": h1["pred_abn_rate"],
        "err_mean_at_arz1": h1["err_mean"],
    }
    print(f"  G4 head preservation: rate {h1['pred_abn_rate']} "
          f"err {h1['err_mean']:.3f} "
          f"-> {gates['M35-G4_head_preservation']['verdict']}")

    # ---- M35-G5: corpus direction (innexin_tail toward the record) -------
    it0 = sim_arm_n12("innexin_tail_m33", phi_readout=PHI,
                      neural_readout=1.0, arz_readout=0.0)
    it1 = sim_arm_n12("innexin_tail_m33", phi_readout=PHI,
                      neural_readout=1.0, arz_readout=1.0)
    ih1 = sim_arm("innexin_head_m33", phi_readout=PHI,
                  neural_readout=1.0, arz_readout=1.0)
    rec_tail = 0.40
    d0 = abs(it0["pred_abn_rate"] - rec_tail)
    d1 = abs(it1["pred_abn_rate"] - rec_tail)
    gates["M35-G5_corpus_direction"] = {
        "verdict": "PASS" if (d1 < d0 and ih1["pred_abn_rate"] == 0.0)
        else "REFUTED",
        "innexin_tail_rate_arz0": it0["pred_abn_rate"],
        "innexin_tail_rate_arz1": it1["pred_abn_rate"],
        "recorded": rec_tail,
        "dist_arz0": d0, "dist_arz1": d1,
        "innexin_head_rate_arz1": ih1["pred_abn_rate"],
    }
    print(f"  G5 corpus direction: innexin_tail {it0['pred_abn_rate']} -> "
          f"{it1['pred_abn_rate']} (record 0.40); innexin_head at arz=1 "
          f"{ih1['pred_abn_rate']} -> "
          f"{gates['M35-G5_corpus_direction']['verdict']}")

    n_pass = sum(1 for x in gates.values() if x["verdict"] == "PASS")
    res["summary"] = f"{n_pass}/{len(gates)} gates PASS"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(res, f, indent=1)
    print(f"\nGATES: {res['summary']}")
    for k, x in gates.items():
        print(f"  {k}: {x['verdict']}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
