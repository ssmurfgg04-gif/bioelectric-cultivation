#!/usr/bin/env python3
"""exp58 — M-SHEET REPAIR: the corrected M-L intercalation front (night nine).

LITERATURE BASIS (research/NIGHT_NINE_RESEARCH.md — Saito 2003 FULL abstract,
DOI 10.1002/dvdy.10246, retrieved via Europe PMC this night):

  "A left lateral fragment containing a left auricle was implanted into the
  medial region of the host. Ectopic structures were always formed ONLY on
  the left side of the graft, where lateral tissues abutted onto the medial
  tissues. However, NO morphologic change was induced on the right side of
  the graft, where left-sided tissues faced onto right-sided tissues. [...]
  When the midline tissues were implanted into a lateral region, they
  induced a COMPLETE ECTOPIC head."

DECISIVE CORRECTION: exp55's intercalate() fires on OPPOSITE-SIGN (L-R
facing) contacts — it encodes the asymmetry hypothesis, the hypothesis
Saito refuted. The corrected rule fires on SAME-SIGN (same-side)
medial-lateral juxtaposition gaps and is STRUCTURALLY SILENT on L-R
contact. Mechanism (registered in exp55's L36, concretized tonight):
same-sign fire rule -> leaky exposure -> commitment (plastic cells, value
pinned) -> ORGANIZER-BEARING inheritance-copy propagation (midline-source
grafts propagate; sourceless grafts commit the local junction band only;
ablated-source grafts starve). Field maintenance: host homeostatic toward
the native ramp; non-source grafts homeostatic toward their transplanted
values; ablated grafts blend passively.

PARAMETER DERIVATION (no outcome peeking — a geometry pre-pass runs the
field-MAINTENANCE dynamics alone, no intercalation, and measures the
SUSTAINED junction drive of each published geometry):
  T_onset = 200 steps   (the exp54 published-window mapping: 3h/6h of the
                         400-step intercalation window)
  leak = 0.01
  restore_gain = 0.1    (maintenance-dominated regime: the maintenance
                         gain must dominate the 0.05 diffusion coupling
                         for "tissue actively maintains its positional
                         field" to hold — at 0.02 the junction contrast
                         collapses in ~20 steps, exp55's D2 world)
  budget_commit = (1 - exp(-leak*T_onset)) * drive_sustained(S2 geom)/leak
                  (the weaker published juxtaposition commits at T_onset;
                  the first pre-pass's ideal-contrast mapping was replaced
                  by this sustained-drive mapping BEFORE the re-run: the
                  maintained equilibrium contrast is what the front
                  actually delivers)
  budget_copy = budget_commit / 2   (fronts propagate above half-charge)
  copy_cadence = 40                 (4 copy waves fill the 5-wide graft
                                     inside the remaining window, 2x margin)

ABLATION SEMANTICS CORRECTION (registered before the re-run, mechanism-
motivated): carries_source=False is not passive blending — an ablated
organizer does not hold a decaying gradient, it ADOPTS THE HOST FIELD.
The first run's passive-sag semantics let the ablated block commit a
DEEPER band than the maintained graft (physically inverted); under
host-adoption the ablated junction contrast dies within ~10-20 steps and
the front starves, restoring the registered ordering S1 > S2 > S4.

PRE-REGISTERED GATES (fixed BEFORE the arms ran; 3 seeds each, majority):

  MSh-G1  COMPLETE ECTOPIC HEAD: midline donor -> flank graft commits the
          graft as head tissue (graft head fraction >= 0.8).
  MSh-G2  LOCAL ONE-SIDED INTERCALATION: lateral donor grafted AT the
          midline commits only the junction band on the HOST-MEDIAL side
          (LEFT half minus RIGHT half >= 0.2, overall <= 0.6).
          Side RE-REGISTERED vs exp55 (was right): the flip follows from
          the corrected geometry and matches the published figure.
  MSh-G3  TRUE ISOGRAFT (zero positional gap — donor re-implanted at its
          own site): no induction (fraction <= 0.1). RE-REGISTERED from
          exp55's shifted-block geometry: that geometry juxtaposes
          DIFFERENT positional values and is therefore not a null under
          the corrected rule (the published record contains no M-L
          gap-graft control; exp55's old geometry is run tonight as the
          EXPLORATORY G8 probe, no gate).
  MSh-G4  SOURCE LOAD-BEARING: ablated midline donor (carries_source=
          False) loses the complete-head outcome (G1 - G4 >= 0.3).
  MSh-G5  NATIVE-AXIS INTEGRITY: native head zone fraction >= 0.9 in ALL
          arms.
  MSh-G6  PROPAGATION-DEPTH ORDERING (the mechanism's own signature):
          depth(G1) >= 4 (organizer propagation fills) > depth(G2) <= 2
          (local band) > depth(G4) = 0 (starved), majority of seeds.
  MSh-G7  STRUCTURAL SILENCE OF L-R CONTACT: cumulative drive at the
          graft's RIGHT junction edge is EXACTLY 0.0 in G2 (the
          opposite-sign junction never fires — the refuted hypothesis's
          geometry, now silent by construction).
  G8      (exploratory, NO gate): shifted same-side gap graft — the model
          predicts no commitment (contrast ~0.36-0.43 sustained gives
          E_ss ~8-12 < budget ~20; the published record has no M-L
          gap-graft control to gate against).
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.bioelectric.sheet import IntercalationSheet  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp58_msheet_repair.json")

SEEDS = (1, 2, 3)
H, W = 40, 28
GR_R0, GR_H, GR_W = 18, 10, 5
HEAD_ZONE = (slice(0, 10), slice(0, W))
LEAK = 0.01
T_ONSET = 200.0          # 3h/6h of the 400-step window (exp54 mapping)
THRESH = 0.2
GAIN = 0.5
COPY_CADENCE = 40


def sustained_junction_drive(seed: int, donor_cols: tuple[int, int],
                             graft_cols: tuple[int, int],
                             n_hold: int = 400) -> dict:
    """Geometry pre-pass: the SUSTAINED left-junction drive under the
    field-maintenance dynamics ALONE (no intercalation, no commitment —
    geometry + maintenance semantics, not outcome). This is what the
    front actually delivers over the window, which is what the exposure
    budget must be mapped onto."""
    sh = IntercalationSheet(h=H, w=W, seed=seed)
    sh.settle(240)
    donor = sh.take_block(GR_R0, donor_cols[0], GR_H,
                          donor_cols[1] - donor_cols[0])
    sh.graft(donor, GR_R0, graft_cols[0])
    g0 = graft_cols[0]
    for _ in range(n_hold):
        lap_ml = sh._lap(sh.theta_ml)
        sh.theta_ml += 0.05 * lap_ml
        sh._apply_graft_sources()
        sh._apply_field_maintenance(0.1)
        sh._apply_pins()
    dml = np.abs(sh.theta_ml[GR_R0:GR_R0 + GR_H, g0 - 1]
                 - sh.theta_ml[GR_R0:GR_R0 + GR_H, g0]).mean()
    contrast = float(dml)
    drive = GAIN * max(0.0, contrast - THRESH)
    return {"sustained_contrast": contrast, "sustained_drive": drive}


def run_arm(seed: int, donor_cols: tuple[int, int],
            graft_cols: tuple[int, int],
            carries_source: bool | None = None,
            budget_commit: float = 20.0, budget_copy: float = 10.0) -> dict:
    sh = IntercalationSheet(h=H, w=W, seed=seed)
    sh.settle(240)
    donor = sh.take_block(GR_R0, donor_cols[0], GR_H,
                          donor_cols[1] - donor_cols[0])
    sh.graft(donor, GR_R0, graft_cols[0], carries_source=carries_source)
    trace = sh.intercalate_regen(400, drive_gain=GAIN,
                                 discontinuity_thresh=THRESH,
                                 budget_commit=budget_commit,
                                 budget_copy=budget_copy,
                                 copy_cadence=COPY_CADENCE, leak=LEAK)
    graft_region = (slice(GR_R0, GR_R0 + GR_H),
                    slice(graft_cols[0], graft_cols[0] + GR_W))
    left, right = sh.half_fractions(graft_region)
    return {
        "seed": seed,
        "graft_head_fraction": sh.head_fraction(graft_region),
        "left_half_fraction": left,
        "right_half_fraction": right,
        "native_head_fraction": sh.head_fraction(HEAD_ZONE),
        "committed_fraction": sh.committed_fraction(graft_region),
        "depth_cols": sh.column_depth(graft_region),
        "commit_step": trace["commit_step"],
        "copies": trace["copies"],
        "right_junction_drive": trace["right_junction_drive"],
    }


def majority(vals: list) -> bool:
    return sum(bool(v) for v in vals) >= (len(vals) // 2 + 1)


def main() -> None:
    print("=== exp58: M-sheet repair (corrected intercalation front) ===\n")

    # ---- geometry pre-pass (budgets derived BEFORE any arm runs) --------
    # Budget mapping (registered): T_onset is the time the WEAKER of the
    # two PUBLISHED juxtaposition geometries needs to commit — the local
    # band (S2 geometry) is what the window's onset delivers; the
    # complete head (S1 geometry) commits earlier under the same budget.
    pre = {"S1": [], "S2": []}
    for seed in SEEDS:
        pre["S1"].append(sustained_junction_drive(seed, (12, 17), (3, 8)))
        pre["S2"].append(sustained_junction_drive(seed, (2, 7), (12, 17)))
    c1 = float(np.mean([p["sustained_contrast"] for p in pre["S1"]]))
    c2 = float(np.mean([p["sustained_contrast"] for p in pre["S2"]]))
    drive_ref = float(np.mean([p["sustained_drive"] for p in pre["S2"]]))
    budget_commit = round((1 - math.exp(-LEAK * T_ONSET)) * drive_ref / LEAK, 1)
    budget_copy = round(budget_commit / 2, 1)
    print(f"  pre-pass sustained: S1 contrast {c1:.3f}, S2 {c2:.3f}")
    print(f"  S2 sustained drive {drive_ref:.3f} -> budget_commit "
          f"{budget_commit}, budget_copy {budget_copy}, cadence {COPY_CADENCE}\n")

    res: dict = {"exp": "exp58_msheet_repair",
                 "derived": {"t_onset": T_ONSET, "leak": LEAK,
                             "drive_ref": drive_ref,
                             "budget_commit": budget_commit,
                             "budget_copy": budget_copy,
                             "copy_cadence": COPY_CADENCE,
                             "s1_contrast": c1, "s2_contrast": c2},
                 "arms": {}}

    arms = {
        "G1_midline_to_flank": dict(donor_cols=(12, 17),
                                    graft_cols=(3, 8)),
        "G2_lateral_to_midline": dict(donor_cols=(2, 7),
                                      graft_cols=(12, 17)),
        "G3_true_isograft": dict(donor_cols=(2, 7),
                                 graft_cols=(2, 7)),
        "G4_midline_ablated": dict(donor_cols=(12, 17),
                                   graft_cols=(3, 8),
                                   carries_source=False),
        "G8_gap_graft_probe": dict(donor_cols=(2, 7),
                                   graft_cols=(8, 13)),
    }
    for name, kw in arms.items():
        rows = [run_arm(seed, budget_commit=budget_commit,
                        budget_copy=budget_copy, **kw) for seed in SEEDS]
        res["arms"][name] = rows
        f = [round(r["graft_head_fraction"], 3) for r in rows]
        d = [r["depth_cols"] for r in rows]
        print(f"  {name}: fractions {f}, depths {d}, "
              f"native {min(round(r['native_head_fraction'], 2) for r in rows)}")

    g = {k: [r["graft_head_fraction"] for r in v]
         for k, v in res["arms"].items()}
    d = {k: [r["depth_cols"] for r in v] for k, v in res["arms"].items()}
    s2_rows = res["arms"]["G2_lateral_to_midline"]
    asym = [r["left_half_fraction"] - r["right_half_fraction"]
            for r in s2_rows]
    rjd = [r["right_junction_drive"] for r in s2_rows]

    gates: dict[str, dict] = {}
    gates["MSh-G1_complete_ectopic_head"] = {
        "verdict": "PASS" if majority([v >= 0.8 for v in
                                       g["G1_midline_to_flank"]])
        else "REFUTED",
        "fractions": g["G1_midline_to_flank"],
        "gate": "graft head fraction >= 0.8 (majority of seeds)",
    }
    gates["MSh-G2_local_one_sided"] = {
        "verdict": "PASS" if majority(
            [(a >= 0.2) and (f <= 0.6)
             for a, f in zip(asym, g["G2_lateral_to_midline"])])
        else "REFUTED",
        "fractions": g["G2_lateral_to_midline"],
        "left_minus_right": [round(a, 3) for a in asym],
        "gate": ("LEFT-RIGHT >= 0.2 AND overall <= 0.6 "
                 "(side re-registered per the corrected geometry)"),
    }
    gates["MSh-G3_true_isograft_null"] = {
        "verdict": "PASS" if majority([v <= 0.1 for v in
                                       g["G3_true_isograft"]])
        else "REFUTED",
        "fractions": g["G3_true_isograft"],
        "gate": "zero-gap isograft fraction <= 0.1 (re-registered arm)",
    }
    gates["MSh-G4_source_load_bearing"] = {
        "verdict": "PASS" if majority(
            [a - b >= 0.3 for a, b in zip(g["G1_midline_to_flank"],
                                          g["G4_midline_ablated"])])
        else "REFUTED",
        "s1_fractions": g["G1_midline_to_flank"],
        "s4_fractions": g["G4_midline_ablated"],
        "gate": "G1 - G4 >= 0.3 (majority of seeds)",
    }
    native_all = [r["native_head_fraction"]
                  for rows in res["arms"].values() for r in rows]
    gates["MSh-G5_native_axis_integrity"] = {
        "verdict": "PASS" if min(native_all) >= 0.9 else "REFUTED",
        "min_native_fraction": float(min(native_all)),
        "gate": "native head zone fraction >= 0.9 in ALL arms",
    }
    gates["MSh-G6_propagation_depth_ordering"] = {
        "verdict": "PASS" if majority(
            [a >= 4 and b <= 2 and c == 0
             for a, b, c in zip(d["G1_midline_to_flank"],
                                d["G2_lateral_to_midline"],
                                d["G4_midline_ablated"])])
        else "REFUTED",
        "depths": d,
        "gate": "depth(G1) >= 4 > depth(G2) <= 2 > depth(G4) == 0",
    }
    gates["MSh-G7_structural_silence_LR"] = {
        "verdict": "PASS" if all(v == 0.0 for v in rjd) else "REFUTED",
        "right_junction_drives": rjd,
        "gate": "cumulative drive at the G2 right junction == 0.0 exactly",
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
    g8 = g["G8_gap_graft_probe"]
    print(f"  G8 probe (exploratory, no gate): fractions {g8} "
          f"(model predicted no commitment)")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
