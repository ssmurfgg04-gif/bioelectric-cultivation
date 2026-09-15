#!/usr/bin/env python3
"""exp55 — GRAFT/LATERAL 2D REPRESENTATION (night-eight queue #3; ledger L36).

LITERATURE BASIS (exp53 wave; research/NIGHT_EIGHT_SYNTHESIS.md):

  Saito et al. 2003 (DOI 10.1002/dvdy.10246, Dev Dyn — verified via
  Crossref): "Mediolateral intercalation in planarians revealed by
  grafting experiments" — the SYMMETRY HYPOTHESIS: both sides carry
  symmetric positional values; M-L intercalation creates positional values
  along that axis; midline tissues implanted into a lateral region
  induce a COMPLETE ECTOPIC HEAD.

BUILD (research/NIGHT_EIGHT_SYNTHESIS.md section 2): a 2D sheet with TWO
INDEPENDENT position fields (AP identity, ML positional value) whose
midline is a SOURCE, not a wall (cultivation/bioelectric/sheet.py — new
additive module). Grafts transplant stored fields; the intercalation drive
fires where OPPOSITE-SIGN ML values meet with contrast ABOVE the
physiological adjacent gradient (the native midline is homeostatic, not
inductive — the physiological zero-crossing never fires).

PRE-REGISTERED GATES (fixed BEFORE the arms ran; 3 seeds each, majority):

  S1  COMPLETE ECTOPIC HEAD: midline donor -> flank graft re-specifies
      the graft as head tissue (graft head fraction >= 0.8).
  S2  ASYMMETRIC LOCAL INTERCALATION: lateral donor grafted AT the
      midline induces only on the abutting side (right-left >= 0.2,
      overall <= 0.6).
  S3  ISOGRAFT CONTROL (zero collateral): same-sign flank-to-flank graft
      produces no induction (fraction <= 0.1).
  S4  THE SOURCE IS LOAD-BEARING: carries_source=False loses the
      complete-head outcome (S1 - S4 >= 0.3).
  S5  NATIVE-AXIS INTEGRITY: native head zone fraction >= 0.9 in ALL arms.

RESULT (honest): S3 + S5 PASS; S1/S2/S4 REFUTED — with a precise
mechanism diagnosis recorded as the night-nine M-sheet repair candidate:

  D1 (artifact found and eliminated en route): the physiological midline
     zero-crossing fires a naive sign-opposition drive via diffusion
     asymmetry (80 spurious cells) — the discontinuity-threshold rule
     (contrast above the physiological gradient) eliminates it; S3/S5
     pass under the corrected rule.
  D2 (the load-bearing refutation): a PURE-DIFFUSION AP field cannot HOLD
     induced identity. The L-R juxtaposition front fires, the contact
     warms to -32 mV, but the contrast front decays under host blending
     (non-frozen ML) and the AP band relaxes back — the induction is not
     an attractor. The 1D model's stability is quasi-frozen slow
     dynamics + chain-written identity; the sheet has neither.
  D3 (the spatial constraint): even with a frozen organizer sustaining
     the edge contrast, a one-sided edge drive cannot fill the graft:
     the diffusion equilibrium across a 5-wide graft with one edge held
     at the pole is ~-35 mV mid-graft (below the head threshold). The
     published COMPLETE head spans the graft because the graft carries
     its OWN axis — the induction layer must be an organizing center
     with commitment (inheritance-copy, the 1D chain mechanism in 2D),
     not a contact-pair drive.
  REGISTERED REPAIR (night-nine, M-sheet): the intercalation front as a
  REGENERATION front — L-R juxtaposition commits head identity at the
  front and propagates it into the juxtaposed tissue BY INHERITANCE COPY
  (the exp27 chain mechanism in 2D), gated by sustained front activity
  (an exposure integrator — the ZENODO:18358611 fixed-shape exposure
  axis). Frozen-organizer fronts sustain (S1 complete); blending fronts
  stall (S2 local); source-dead fronts die first (S4). No free failure
  knob: the exposure budget is the mechanism's own commitment cadence.

RUN PROTOCOL: sheet 40x28, midline col 14; native head rows 0-9; graft
rows 18-26 (10 rows x 5 cols, mid-body). Arms: S1/S4 donor = midline
strip cols 12-16 -> flank cols 3-7; S2 donor = flank cols 2-6 -> AT the
midline cols 12-16; S3 donor = flank cols 2-6 -> same-sign cols 8-12.
Settle 240 steps; intercalate 400 steps. Seeds 1,2,3.
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

from cultivation.bioelectric.sheet import BioelectricSheet  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp55_sheet_graft.json")

SEEDS = (1, 2, 3)
H, W = 40, 28
MID = W // 2
GR_R0, GR_H, GR_W = 18, 10, 5
HEAD_ZONE = (slice(0, 10), slice(0, W))


def run_arm(seed: int, donor_cols: tuple[int, int],
            graft_cols: tuple[int, int],
            carries_source: bool | None = None) -> dict:
    sh = BioelectricSheet(h=H, w=W, seed=seed)
    sh.settle(240)
    r0, c0 = donor_cols
    donor = sh.take_block(GR_R0, c0, GR_H, r1w := GR_W)
    sh.graft(donor, GR_R0, graft_cols[0], carries_source=carries_source)
    sh.intercalate(400)
    graft_region = (slice(GR_R0, GR_R0 + GR_H),
                    slice(graft_cols[0], graft_cols[0] + GR_W))
    left, right = sh.half_fractions(graft_region)
    return {
        "seed": seed,
        "graft_head_fraction": sh.head_fraction(graft_region),
        "left_half_fraction": left,
        "right_half_fraction": right,
        "native_head_fraction": sh.head_fraction(HEAD_ZONE),
        "graft_mean_ap_mv": float(np.mean(
            sh.theta_ap[graft_region[0], graft_region[1]])),
    }


def majority(vals: list[bool]) -> bool:
    return sum(vals) >= (len(vals) // 2 + 1)


def main() -> None:
    print("=== exp55: 2D sheet graft/lateral representation ===\n")
    res: dict = {"exp": "exp55_sheet_graft", "arms": {}}

    arms = {
        "S1_midline_to_flank": dict(donor_cols=(12, 17),
                                    graft_cols=(3, 8)),
        "S2_lateral_to_midline": dict(donor_cols=(2, 7),
                                      graft_cols=(12, 17)),
        "S3_isograft_control": dict(donor_cols=(2, 7),
                                    graft_cols=(8, 13)),
        "S4_midline_to_flank_nosource": dict(donor_cols=(12, 17),
                                             graft_cols=(3, 8),
                                             carries_source=False),
    }
    for name, kw in arms.items():
        rows = [run_arm(seed, **kw) for seed in SEEDS]
        res["arms"][name] = rows
        f = [r["graft_head_fraction"] for r in rows]
        print(f"  {name}: graft fractions {[round(v, 3) for v in f]}, "
              f"native head {[round(r['native_head_fraction'], 3) for r in rows]}")

    g = {k: [r["graft_head_fraction"] for r in v]
         for k, v in res["arms"].items()}
    s1 = g["S1_midline_to_flank"]
    s2 = g["S2_lateral_to_midline"]
    s3 = g["S3_isograft_control"]
    s4 = g["S4_midline_to_flank_nosource"]

    # halves for S2 asymmetry
    s2_rows = res["arms"]["S2_lateral_to_midline"]
    asym = [r["right_half_fraction"] - r["left_half_fraction"]
            for r in s2_rows]

    gates: dict[str, dict] = {}

    gates["S1_complete_ectopic_head"] = {
        "verdict": "PASS" if majority([v >= 0.8 for v in s1]) else "REFUTED",
        "fractions": s1,
        "gate": "graft head fraction >= 0.8 (majority of seeds)",
    }
    gates["S2_asymmetric_local"] = {
        "verdict": "PASS" if majority(
            [(a >= 0.2) and (f <= 0.6)
             for a, f in zip(asym, s2)]) else "REFUTED",
        "fractions": s2,
        "right_minus_left": asym,
        "gate": ("right-left >= 0.2 AND overall <= 0.6 "
                 "(majority of seeds)"),
    }
    gates["S3_isograft_zero_collateral"] = {
        "verdict": "PASS" if majority([v <= 0.1 for v in s3]) else "REFUTED",
        "fractions": s3,
        "gate": "graft head fraction <= 0.1 (majority of seeds)",
    }
    gates["S4_source_load_bearing"] = {
        "verdict": "PASS" if majority(
            [a - b >= 0.3 for a, b in zip(s1, s4)]) else "REFUTED",
        "s1_fractions": s1,
        "s4_fractions": s4,
        "gate": "S1 fraction - S4 fraction >= 0.3 (majority of seeds)",
    }
    native_all = [r["native_head_fraction"]
                  for rows in res["arms"].values() for r in rows]
    gates["S5_native_axis_integrity"] = {
        "verdict": "PASS" if min(native_all) >= 0.9 else "REFUTED",
        "min_native_fraction": float(min(native_all)),
        "gate": "native head zone fraction >= 0.9 in ALL arms",
    }

    res["gates"] = gates
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
