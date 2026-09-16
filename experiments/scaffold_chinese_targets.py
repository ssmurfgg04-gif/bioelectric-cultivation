#!/usr/bin/env python3
"""SCAFFOLD — gates per research/chinese_targets_gates.md; assign exp
number and finalize before running.

STATUS: SCAFFOLD. The data-loading and the ADOPTED exp92-mapping import
path are wired (and only those); every protocol body below is a
NotImplementedError stub. This file has NOT been run and must not be run
until (a) an exp number is assigned in the ledger, (b) the TO-PIN record
constants are transcribed from the PMCID full texts, and (c) the gate
bodies are finalized exactly as pre-registered in
research/chinese_targets_gates.md (the gates in that document are the
registration; this file is only their carriage).

THE THREE TARGETS (subagent 2-b's deposit,
/home/z/my-project/research/papers/chinese_planaria_mining.md):
  T1  metformin 10-point dose ladder, D. japonica, eyespot regeneration
      time in hours, biphasic — Genes 2025, PMID 40282325 (companion
      IJMS 2025, PMID 40806224).
  T2  Usp7 RNAi -> Islet/Wnt1 axis -> complete tail-regeneration failure
      (penetrance ~1.0) + R1d/R3d/R7d expression time-course — J Transl
      Med 2025, PMID 39885534.
  T3  opa1 RNAi impairment restored by drp1 co-RNAi (rescue epistasis) —
      Nat Commun 2024, PMID 39672898.

WHAT IS WIRED (imports only, no execution):
  - the ADOPTED corpus mapping path, verbatim from exp118:
      map_arm / build_rows / run_arms / attach_sim / mae and the pinned
      constants D_PAR=0.25, GEN_BIAS=0.321, the ledger pins, seeds (1,2,3)
  - the dose knob: exp91.run_arm_dose (the corruption-amplitude axis)
  - the exp92 class machinery: row_class / EFFECTOR_RE
  - the timing instrument: exp124.run_deadline (COMPILER SUBSTRATE —
    grid2d/torus via exp112.build_battery; NOT the 1D corpus sheet;
    scope-flagged in the gates document, T2-G2)
  - the anchor-gate reference: results/exp118_corpus_full.json numbers
    (decoded MAE 0.290 n=884 / raw 0.3705 n=905) — exp91/exp92's own
    result JSONs are lost (2-a rollback); exp118's full run is the
    deposited reference artifact.

WHAT IS STUBBED (NotImplementedError):
  anchor_gate()            A-G1  the L74/exp118 reference reproduces
  target1_dose_axis()      T1-G1 the recorded dose direction transfers
  target1_biphasic()       T1-G2 the biphasic stress-test (fine ladder)
  target2_penetrance()     T2-G1 the class rule transfers to the Usp7 row
  target2_timing_anchor()  T2-G2 the deadline instrument anchor + R-axis
                           deferral
  target3_impairment()     T3-G1 the impaired arm lands (family transfer)
  target3_rescue()         T3-G2 the kwargs channel as the drp1 rescue

main() runs the PURE-DB preflight only (no sim), prints the coverage and
the DJ-slice baseline the gates are judged against, then raises
NotImplementedError — the scaffold cannot silently half-run.
"""
from __future__ import annotations

import json
import os
import sys
from collections import Counter

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

# ---- the ADOPTED mapping path (wired; exp118's verbatim machinery) ------
from experiments.exp60_gene_layer import experiment_family  # noqa: E402,F401
from experiments.exp70_onset_corpus import classify_onset  # noqa: E402,F401
from experiments.exp88_corpus_rewire import run_arm_v5  # noqa: E402,F401
from experiments.exp91_dose_axis_wiring import (  # noqa: E402
    CNS_GRID,
    DIFF_GRID,
    run_arm_dose,
)
from experiments.exp92_fine_ladder_rowmap import (  # noqa: E402,F401
    EFFECTOR_RE,
    row_class,
)
from experiments.exp118_corpus_full_mine import (  # noqa: E402
    D_PAR,
    GEN_BIAS,
    PIN_C4_ROWS,
    PIN_L73_BLOCK,
    PIN_L74_MAE,
    PIN_L74_MODULATOR,
    PIN_CTRL_RATES,
    SEEDS,
    attach_sim,
    build_rows,
    map_arm,
    mae,
    run_arms,
)
from experiments.exp112_walk_speed_ladder import build_battery  # noqa: E402,F401
from experiments.exp124_deadline_curve import run_deadline  # noqa: E402,F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXP118_FULL = os.path.join(ROOT, "results", "exp118_corpus_full.json")

# placeholder output name — ASSIGN THE EXP NUMBER FIRST
EXP_NUM = None            # e.g. 125, assigned in the ledger before any run
OUT = os.path.join(ROOT, "results", "expXXX_chinese_targets.json")

# ---- pre-registered grids (research/chinese_targets_gates.md §1c/§2c/§3c)
DOSE_GRID_COARSE = (0.0, 0.25, 0.5, 0.75, 1.0)   # T1-G1 (control->0, 40mM->1.0)
FINE_DOSES = (0.25, 0.30, 0.35, 0.40, 0.45, 0.50)  # T1-G2, exp92's instrument
FINE_SEEDS = (1, 2, 3, 4, 5, 6, 7)
ONSETS = (0.0, 6.0, 12.0, 18.0, 24.0, 36.0, 48.0, 72.0)  # exp124's grid
TIMING_GAMMA = 1.0                                # T2-G2, the exp123 anchor
TIMING_SEEDS = tuple(range(1, 9))

# ---- TO-PIN record constants (transcribe from the PMCIDs BEFORE any run;
#      the gates are unreadable until these are pinned) -------------------
PIN_T1_METFORMIN = None   # TODO: the 10-point per-dose mean/SD table (hours)
                          # from PMC12026922 Fig. 2 (+ the paper's own stats);
                          # 10 mM inhibit point from PMC12345652 (IJMS).
PIN_T2_USP7 = None        # TODO: the exact tail-failure penetrance (fraction)
                          # from PMC11783867 (the deposit says near-complete).
PIN_T3_OPA1 = None        # TODO: the exact impaired-arm and rescued-arm
                          # percentages from PMC11645412.

# the pre-registered concentration -> amplitude coarsening (T1-G1):
#   control -> 0.0; promote band (100 nM / 10 uM / 1 mM) -> D_PAR;
#   intermediate band -> 0.5; 10 mM (IJMS) -> 0.75; 40 mM -> 1.0.
T1_COARSENING = {
    "control": 0.0,
    "promote_band": D_PAR,
    "intermediate_band": 0.5,
    "inhibit_10mM": 0.75,
    "inhibit_40mM": 1.0,
}

# the pre-registered control-anchored readout transform (T1-G1; it
# deliberately DISCARDS the promote-band dip — that dip is T1-G2's
# business, in the paper's own units):
#   f(dose) = clamp((t_dose - t_control) / (t_max - t_control), 0, 1)
def t1_transform(t_dose: float, t_control: float, t_max: float) -> float:
    raise NotImplementedError("pin PMC12026922's table first; see gates §1b")


# ------------------------------------------------------------- data loading
def load_corpus() -> tuple[list[dict], dict]:
    """The full-corpus record side (pure DB, no sim) — exp118's build_rows
    verbatim: every Experiment row with its adopted-mapping arm, both
    recorded frames, the C4 flag, and the G1 pinned-block stats."""
    return build_rows()


def dj_slice_baseline(rows: list[dict]) -> dict:
    """The D. japonica slice baseline the gates are judged against
    (gates document §0/§4 risk 6): decoded MAE and decode accuracy over
    the DJ scored rows, non-C4 for the MAE."""
    dj = [r for r in rows if r.get("species") == "Dugesia japonica"]
    scored = [r for r in dj if r.get("status") == "scored"]
    err = [abs(r["sim"] - r["recorded_corrected"]) for r in scored
           if r.get("sim") is not None and not r["excluded_C4"]]
    return {
        "n_dj_total": len(dj),
        "n_dj_scored": len(scored),
        "dj_decoded_mae": (round(float(np.mean(err)), 4) if err else None),
        "n_dj_decoded": len(err),
        "dj_decode_accuracy": (round(float(np.mean(
            [r["decode_match"] for r in scored])), 4) if scored else None),
        "dj_groups": dict(Counter(r["group"] for r in scored)),
    }


def preflight() -> dict:
    """Pure-DB preflight: the anchor's DB-side pins + coverage + the DJ
    baseline. No sim runs here. The sim-side anchor (A-G1) is a stub."""
    rows, stats = load_corpus()
    ref = json.load(open(EXP118_FULL))  # the deposited reference artifact
    out = {
        "scaffold": True,
        "exp_num": EXP_NUM,
        "n_db_total": stats["n_db_total"],
        "coverage_mapped_fraction": ref["coverage"]["mapped_fraction_of_outcome"],
        "db_pins": {
            "l73_block": stats["l73_block"],
            "l74_modulator": stats["l74_modulator"],
            "ctrl_rate": stats["ctrl_rate"],
            "n_c4": stats["n_c4"],
            "pinned_expectations": {
                "l73_block": PIN_L73_BLOCK,
                "l74_modulator": PIN_L74_MODULATOR,
                "ctrl_rate": PIN_CTRL_RATES,
                "n_c4": PIN_C4_ROWS,
            },
        },
        "dj_slice_baseline": dj_slice_baseline(rows),
        "anchor_reference": {
            "decoded_mae": ref["aggregates"]["mae_corrected_decoded"],
            "decoded_n": ref["aggregates"]["n_decoded"],
            "raw_mae": ref["aggregates"]["mae_raw"],
            "source": "results/exp118_corpus_full.json (L99; the L74 G5 "
                      "re-deposit — exp91/92's own JSONs are lost)",
        },
        "record_pins_pinned": all(
            v is not None for v in
            (PIN_T1_METFORMIN, PIN_T2_USP7, PIN_T3_OPA1)),
        "arm_anchors_to_verify": {
            "('wnt', 'tail', 0.5, 0.25)": 0.0,
            "('wnt', 'tail', 0.5, 1.0)": 1.0,
            "('wnt', 'trunk', 0.5, 0.25)": 0.0,
            "('wnt', 'trunk', 0.5, 1.0)": 1.0,
            "('generic', 'trunk', 0.5, None)": 0.667,
            "('cutting', 'trunk', 0.5, None)": 0.0,
        },
    }
    return out


# ---------------------------------------------------------------- the gates
def anchor_gate() -> dict:
    """A-G1 — the L74/exp118 reference reproduces bit-exactly (decoded
    0.290 n=884, raw 0.3705 n=905; the DB pins; the six arm anchors;
    one determinism re-run). REFUTE = harness/extraction drift: NO target
    gate may be read after a refuted anchor. Gates §ANCHOR."""
    raise NotImplementedError("finalize per gates §ANCHOR before running")


def target1_dose_axis() -> dict:
    """T1-G1 — the recorded dose DIRECTION transfers at the coarse grain:
    Spearman(sim rate, t1-transform vector) >= 0.6 over DOSE_GRID_COARSE on
    ('wnt','trunk',0.5) x SEEDS; inhibit end lands high (rate at d=1.0
    >= 0.5). Two-sided; third outcome = degenerate (saturated-flat)
    ladder -> span-recalibration lesson, not mapping failure. Gates §1d."""
    raise NotImplementedError("pin PIN_T1_METFORMIN; finalize per gates §1d")


def target1_biphasic() -> dict:
    """T1-G2 — the biphasic stress-test of exp29-S2R3's monotonicity:
    the 7-seed FINE_DOSES ladder on ('wnt','trunk',0.5); the recorded dip
    judged in the paper's own units (hours, n=30, the paper's own stats —
    NOT the transform). Two-sided + power third outcome. Gates §1d."""
    raise NotImplementedError("pin PIN_T1_METFORMIN; finalize per gates §1d")


def target2_penetrance() -> dict:
    """T2-G1 — the class rule transfers to the Chinese Usp7 row: the row
    enters as modulator -> d=D_PAR on ('wnt','tail',0.5) (deposited rate
    0.0; re-verify bit-exact + the d=1.0 arm at 1.0); compare the pinned
    penetrance at the dominant-class grain. The expected branch per the
    deposit (~1.0) is the REFUTE branch = a dose-CLASS assignment failure
    (a Chinese counterexample to L74's 'record property' closure). Gates §2d."""
    raise NotImplementedError("pin PIN_T2_USP7; finalize per gates §2d")


def target2_timing_anchor() -> dict:
    """T2-G2 — the timing instrument's anchor + the R-axis deferral:
    run_deadline on grid2d (build_battery), gamma=TIMING_GAMMA, ONSETS x
    TIMING_SEEDS; the edge must land in the deposited 36 h cell within one
    onset step (exp123's anchor, DC-G3). The R1d/R3d/R7d axis is an
    EXPRESSION time-course, not a timed-disruption ladder — registered as
    an honest DEFERRAL regardless of this gate. CROSS-SUBSTRATE instrument
    (compiler, not the 1D sheet). Gates §2d."""
    raise NotImplementedError("finalize per gates §2d before running")


def target3_impairment() -> dict:
    """T3-G1 — the impaired arm lands: pinned decoded impairment
    (raw - GEN_BIAS, clamped) within +/-0.25 of the deposited
    ('generic','trunk') rate 0.667 (re-verify bit-exact) and the raw
    impairment separates from the cutting control by >= 0.25. Two-sided +
    the readout-mismatch third outcome. GEN_BIAS is a PlanformDB decode
    constant (gates §4 risk 3). Gates §3d."""
    raise NotImplementedError("pin PIN_T3_OPA1; finalize per gates §3d")


def target3_rescue() -> dict:
    """T3-G2 — the kwargs channel as the drp1 rescue: the exp40 grid
    (CNS_GRID x DIFF_GRID = 30 cells) x SEEDS on ('generic','trunk').
    Confirm = some cell drops the rate >= 0.3 below 0.667 toward the 0.0
    control; Refute = the grid minimum stays >= 0.367 (L70's repair is
    slice-specific); Third outcome = every cell moves UP (channel polarity
    inverted on this arm class). Gates §3d."""
    raise NotImplementedError("finalize per gates §3d before running")


GATES = {
    "A_G1_anchor": anchor_gate,
    "T1_G1_dose_axis": target1_dose_axis,
    "T1_G2_biphasic": target1_biphasic,
    "T2_G1_penetrance": target2_penetrance,
    "T2_G2_timing_anchor": target2_timing_anchor,
    "T3_G1_impairment": target3_impairment,
    "T3_G2_rescue": target3_rescue,
}


def main() -> None:
    print("=== SCAFFOLD chinese targets — NOT an experiment yet ===")
    print("docstring: assign exp number and finalize before running "
          "(research/chinese_targets_gates.md is the registration)")
    pre = preflight()
    print(json.dumps(pre, indent=1, default=float))
    missing = [k for k, v in
               (("PIN_T1_METFORMIN", PIN_T1_METFORMIN),
                ("PIN_T2_USP7", PIN_T2_USP7),
                ("PIN_T3_OPA1", PIN_T3_OPA1)) if v is None]
    if missing:
        print(f"\n  TO-PIN record constants missing: {missing} — "
              "transcribe from the PMCIDs (gates document §6) before "
              "finalizing.")
    raise NotImplementedError(
        "SCAFFOLD: the protocol bodies are stubs. Assign an exp number "
        "(EXP_NUM), pin the record constants, finalize the gate bodies "
        "per research/chinese_targets_gates.md, and register in the "
        "ledger BEFORE running.")


if __name__ == "__main__":
    main()
