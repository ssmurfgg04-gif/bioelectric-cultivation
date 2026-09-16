#!/usr/bin/env python3
"""exp139 — LEVIN T5: VOLTAGE-SERIES CROSS-VALIDATION (Workstream A; the
T5 target of the Levin-series ranked list, research/levin_voltage_series.md
§4 T5 — run LAST of the five targets by its own ranking because it is the
"cheapest, weakest refutation power" one: the absolute-value anchor).

THE RECORD: research/levin_voltage_series.json — 119 entries (99
PlanformDB 2.5.0 published-outcome rows + 20 curated entries). The record's
honest shape: ZERO absolute mV values for planarian tissues (relative DiBAC
polarities, outcome frequencies, timing kernels); absolute mV exists only
in adjacent models — Chernet 2013's Xenopus impalement delta (-19.4 mV,
entry C11) and the Levin lab's own BETSE simulator (entry C13: band
-10..-80 mV, bistable swing -57 -> -14 mV = 43 mV, GJ voltage-gating 15 mV).

THE STACK'S PREDICTORS (what "the stack predicts" concretely is here):
  P1  the absolute pattern-map calibration (exp1/exp39): the settled sheet
      reads head -24.86 / trunk-tail -50.26 / wound-face -38.03 mV. This is
      a CHOICE (exp39's honest scope), and T5 tests the choice against the
      only absolute numbers the record has.
  P2  the GHK inference layer (cultivation/validation/vmem_inference.py,
      entry C14): expression -> permeabilities -> absolute Vmem per cell
      type (7-type curated map).
  P3  the family-mapped perturbation arms (exp39-verbatim, re-run):
      A cutting control, B gap-junction blockade (block_gap_junctions 0.05,
      the exp39-V4/exp29-S2R3 recorded mapping), C the hyperpolarizing ion
      arm (gamma x0.5, noise x3.0, commitment_noise_scale 3.0,
      commitment_diffusion 1.5 — exp39-V2/exp131-verbatim), D the
      posterior-depolarization arm (exp39-V3 verbatim).
  P4  price map v2 / the corrected oracle (exp114/exp117) and the deadline
      map (exp124/exp125): DEPOSITED AS SCOPE, NOT GATED (see HONEST SCOPE).

THE PARTITION (pre-registered rule, applied to every entry exactly once;
per-ROW manipulation record only — drug_start_end / rnaic in the
manipulation string — never the shared direction_signature template):
  FAM-B GJ-BLOCKED: drug_start_end contains Octanol/Heptanol/Hexanol OR
        manipulation rnaic contains an innexin ('inx').
  FAM-C HYPERPOLARIZATION-AXIS: drug_start_end contains SCH-28080 /
        Potassium / Nicardipine, or a curated barium entry.
  FAM-D DEPOLARIZATION-AXIS: drug_start_end contains Ivermectin, or a
        curated nigericin/bistability entry.
  FAM-E ABSOLUTE-SCALE / ADJACENT-MODEL: the curated non-planarian,
        method, review and inference-layer entries (C07, C08, C11, C12,
        C13, C14).
  FAM-A GJ-INTACT POLARITY / REGENERATION BASELINE: everything else (naive
        cutting controls, canonical-axis RNAi, ectopic-persistence re-cuts,
        the field claim C10, the polarity pairs V1/V5). OWNED UP FRONT:
        FAM-A is the RESIDUE family and is heterogeneous (controls +
        octanol-lineage re-cuts + b-catenin/notch RNAi); its measured
        scalar carries that composition, deposited per-row.
  Expected counts (computed under this rule before running): A 30, B 57,
  C 21, D 5, E 6 (DB rows A 27 / B 53 / C 17 / D 2 + curated 3/4/4/3/6).

INSTRUMENT NOTE (owned): the stack cannot make quantitative ABSOLUTE Vmem
predictions for the planarian families — the record itself has none to
test against. The cross-family test is therefore on the families'
OUTCOME-DEVIATION ordering (the record's measured axis), the absolute test
is confined to FAM-E, and the sign battery carries the polarity skeleton.

PRE-REGISTERED GATES (thresholds frozen BEFORE running; two-sided where
the statistic is an ordering):

  LV-A1  (ANCHOR — partition + calibration continuity) every one of the
         119 entries lands in exactly one family (ids unique, total 119);
         the vmem_mv-bearing entries (C11, C13) land in FAM-E; the exp39
         deposited calibration quantities reproduce at seed 1 within
         0.125 mV (head -24.86, tail -50.26, wound -38.03 vs
         results/exp39_levin_voltage.json V1/V5).
  LV-G1  (CROSS-FAMILY ORDERING — the strict primary) across the four
         planarian families {A, B, C, D}:
           E_stack(f) = the family-mapped arm's deviation-from-WT rate
             (A cutting-arm abnormal, B GJ-block-arm abnormal,
              C ion-arm abnormal, D posterior-depol EA rate;
              seeds 1-3, exp39-verbatim arms).
           E_meas(f) = the mean over the family's DB rows of
             (1 - P(Wild type)) — the record's outcome-deviation from WT
             (curated entries carry no outcome frequencies; D has n=2 —
             owned).
         Spearman(E_stack, E_meas) >= 0.4 -> PASS; <= -0.6 -> REFUTED
         (anti-ordered); otherwise PARTIAL (measured concordance, owned
         honestly — exp131's IP-G1 zone convention).
  LV-G2  (ABSOLUTE ANCHOR — FAM-E, pre-registered CALIBRATION class: a
         failure is a recalibration target, NOT a falsification — the T5
         md's own clause) four sub-gates, PASS iff all four:
           (a) the calibration trio head/trunk/wound inside the BETSE band
               [-80, -10] mV;
           (b) head-trunk delta (25.4 mV) within +-50% of the BETSE
               bistable swing (43 mV);
           (c) wound-minus-intact-tail depolarization (12.2 mV) within
               +-50% of Chernet's measured knockout delta (19.4 mV);
           (d) ALL 7 GHK-inferred cell types inside the BETSE band.
  LV-G3  (THE SIGN BATTERY — the qualitative skeleton, strict 4/4; one
         wrong sign refutes the polarity mapping per exp131's IP-G2
         clause):
           S1 intact head V > intact trunk V (anterior depolarized);
           S2 wound-face V > settled body mean (wounds depolarized);
           S3 GJ-block abnormal rate > cutting abnormal rate;
           S4 ion-arm abnormal rate > cutting abnormal rate.
  LV-G4  (PER-PLANE ORDERING inside the manipulated families — two-sided)
         rho_B = Spearman(stack GJ-arm EA rate by plane mapped through the
         corpus's pre-registered plane taxonomy, published octanol DH by
         plane [head .05, pre-phar .28, pharyngeal .50, post-phar 1.00,
         tail .00], eids 415-419); rho_C = the same for the ion arm vs
         Beane 2011's headless series [0, 0, .67, .16, .40], eids 391-395
         (exp131's IP-G1 instrument, re-run as the family's own).
         PASS iff BOTH >= 0.4; REFUTED if either <= -0.3; else PARTIAL.

HONEST SCOPE (deposited, not gated):
  - P4 price map v2 / corrected oracle (exp114/exp117): the v2 oracle
    prices STACK SUBSTRATES (19-member class-level Spearman 0.63, exp114's
    corrected re-test). The family arms here run on the deployed DEFAULT0
    sheet cell (1, 0.015); no per-biological-family pricing column exists
    in the map — a family-level v2 test would be an instrument mismatch.
    Deposited as a scope boundary.
  - P4 deadline map (exp124/125): the record's timing kernels (3 h write
    window C04/Durant 2019; the 12-24 h octanol-kernel edge; the 48-72 h
    barium onset) were family-tested in exp130 (REFUTED as a rescue-vs-
    damage mismatch — the stack's deadline is a rescue curve, Oviedo's
    kernel a damage kernel) and exp131. exp139 registers NO new timing
    gate; the timing panel is deposited as context with exp130's
    refutation owned.

RUN: ~40 sim arms x <=1 s (exp39/exp131 machinery, seeds 1-3), GHK pure
arithmetic, partition pure JSON. Seconds. Serial, BLAS pinned.
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

from scipy.stats import spearmanr  # noqa: E402

from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)
from cultivation.validation.vmem_inference import (  # noqa: E402
    infer_vmem, MARKER_TABLE,
)
from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, SEEDS, TAIL, ABN_ERR_MV, ABN_HL, make_collective,
)
from experiments.exp32_m26_repairs import (  # noqa: E402
    HEAD as HEAD_SL, TAILP, TRUNK, POST_Q, WT_HEAD_V,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp139_levin_voltage.json")
SERIES = os.path.join(ROOT, "research", "levin_voltage_series.json")
EXP39 = os.path.join(ROOT, "results", "exp39_levin_voltage.json")

# ---- the record's absolute anchors (FAM-E) --------------------------------
BETSE_BAND = (-80.0, -10.0)     # C13: simulated Vmem range
BETSE_SWING = 43.0              # C13: bistable -57 -> -14 mV
CHERNET_DELTA = 19.4            # C11: Xenopus impalement delta (n=5)
REL_TOL = 0.5                   # the T5 md's +-50% windows

# ---- exp39 deposited calibration anchors ----------------------------------
DEP_HEAD = -24.859522940576216
DEP_TAIL = -50.25690149582484
DEP_WOUND = -38.02933652459853
ANCHOR_TOL = 0.125

# ---- published per-plane series (DB rows, Oviedo 2010 / Beane 2011) -------
PUB_ORDER = ("head", "pre_pharyngeal", "pharyngeal",
             "post_pharyngeal", "tail")
PUB_OCTANOL_DH = {"head": 0.05,         # eid 415, n=132
                  "pre_pharyngeal": 0.28,    # eid 416, n=118
                  "pharyngeal": 0.50,        # eid 417, n=115
                  "post_pharyngeal": 1.00,   # eid 418, n=145
                  "tail": 0.00}              # eid 419, n=178
PUB_HEADLESS = {"head": 0.00,           # eid 391, n=120
                "pre_pharyngeal": 0.00,      # eid 392, n=138
                "pharyngeal": 0.67,          # eid 393, n=175
                "post_pharyngeal": 0.16,     # eid 394, n=111
                "tail": 0.40}                # eid 395, n=106
# the corpus's pre-registered plane taxonomy (planform_mining.py)
TAXONOMY = {"head": "head", "pre_pharyngeal": "head",
            "pharyngeal": "trunk", "post_pharyngeal": "tail",
            "tail": "tail"}
SIM_PLANES = ("head", "trunk", "tail")

G1_PASS, G1_REFUTE = 0.4, -0.6      # LV-G1 two-sided zones (pre-registered)
G4_PASS, G4_REFUTE = 0.4, -0.3      # LV-G4 two-sided zones (pre-registered)

# ---- curated-entry family assignment (explicit table, pre-registered) -----
CURATED_FAM = {
    "V1_head_depolarized_vs_trunk": "A",
    "V5_wound_depolarized": "A",
    "C10-marsh-beams-1952": "A",
    "V3_posterior_depol_ectopic_head": "B",
    "V4_junction_block_graded": "B",
    "C03-durant2017-numbers": "B",
    "C05-eb2015-numbers": "B",
    "V2_hyperpolarization_abnormal": "C",
    "C01-beane2011-claim": "C",
    "C02-beane2013-claim": "C",
    "C06-eb2019-numbers": "C",
    "V6_stochastic_identical_perturbation": "D",
    "C04-durant2019-window": "D",
    "C09-pezzulo2021-claim": "D",
    "C07-oviedo2008-method": "E",
    "C08-durant2016-review": "E",
    "C11-chernet2013-xenopus": "E",
    "C12-chernet2014-xenopus": "E",
    "C13-betse-pietak-levin": "E",
    "C14-vmem-inference-layer": "E",
}
DB_D = ("Ivermectin", "Nigericin")
DB_C = ("SCH-28080", "Potassium", "Nicardipine")
DB_B = ("Octanol", "Heptanol", "Hexanol")

WT = wildtype_target(N)


# ---- the partition rule (frozen; see docstring) ---------------------------
def db_family(e: dict) -> str:
    drugs = [dr[0] for dr in (e.get("drug_start_end") or [])]
    man = str(e.get("manipulation", ""))
    if any(x in drugs for x in DB_D) or "nigericin" in man.lower():
        return "D"
    if any(x in drugs for x in DB_C):
        return "C"
    if (any(x in drugs for x in DB_B) or "inx" in man):
        return "B"
    return "A"


def build_families() -> tuple[dict, dict]:
    series = json.load(open(SERIES))
    fam: dict[str, str] = {}
    rows_by_fam: dict[str, list] = {k: [] for k in "ABCDE"}
    for e in series["series"]:
        eid = e["id"]
        if eid in CURATED_FAM:
            f = CURATED_FAM[eid]
        else:
            f = db_family(e)
        if eid in fam:
            raise ValueError(f"double assignment: {eid}")
        fam[eid] = f
        rows_by_fam[f].append(e)
    return fam, rows_by_fam


def db_rows(rows_by_fam: dict, f: str) -> list:
    """The family's PlanformDB outcome rows only (the curated entries
    carry no outcome frequencies — the E_meas instrument is DB-only)."""
    return [e for e in rows_by_fam[f]
            if e.get("kind", "").startswith("recorded-outcome")]


def mean_non_wt(rows: list) -> float:
    return float(np.mean(
        [1.0 - sum(of["frequency"] for of in e["outcome_frequencies"]
                   if of["outcome"] == "Wild type") for e in rows]))


# ---- the exp39-verbatim arms (exp131's verbatim extensions) ---------------
def _flags(c) -> tuple[bool, bool, float, float]:
    err = float(c.pattern_error(WT))
    hl = float(head_likeness(c.V, TAIL))
    ea = bool(hl >= ABN_HL)
    af = bool(err >= ABN_ERR_MV and not ea)
    return ea, af, err, hl


def cutting_arm(seed: int) -> tuple[bool, float, float]:
    """exp39 V2 cutting_arm verbatim (FAM-A's control)."""
    c = make_collective(seed)
    c.run(24, dt=DT)
    c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
    c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6)
    _, _, err, hl = _flags(c)
    return bool(err >= ABN_ERR_MV or hl >= ABN_HL), err, hl


def gj_arm(plane: str, seed: int) -> tuple[bool, bool, float, float]:
    """FAM-B's arm: sustained GJ blockade (block_gap_junctions 0.05, the
    exp39-V4 mapping) + exp70's plane geometry."""
    c = make_collective(seed)
    c.block_gap_junctions(0.05)
    c.run(24, dt=DT)
    kw = dict(cell_period=0.8, dt=DT, noise=0.6)
    if plane == "head":
        c.amputate(HEAD_SL, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(HEAD_SL, direction="backward", **kw)
    elif plane == "trunk":
        c.amputate(TRUNK, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TRUNK, direction="both", **kw)
    elif plane == "tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, **kw)
    else:
        raise ValueError(plane)
    return _flags(c)


def ion_arm(plane: str, seed: int) -> tuple[bool, bool, float, float]:
    """FAM-C's arm: exp39-V2/exp131-verbatim ion arm by plane."""
    c = make_collective(seed)
    c.gamma *= 0.5
    c.noise_std *= 3.0
    c.run(24, dt=DT)
    kw = dict(cell_period=0.8, dt=DT, noise=0.6,
              commitment_noise_scale=3.0, commitment_diffusion=1.5)
    if plane == "head":
        c.amputate(HEAD_SL, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(HEAD_SL, direction="backward", **kw)
    elif plane == "trunk":
        c.amputate(TRUNK, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TRUNK, direction="both", **kw)
    elif plane == "tail":
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, **kw)
    else:
        raise ValueError(plane)
    return _flags(c)


def wnt_arm(seed: int) -> tuple[bool, bool, float, float]:
    """FAM-D's arm: exp39-V3 verbatim (posterior quarter -> head
    identity)."""
    c = make_collective(seed)
    c.corrupt_region(POST_Q, theta_value=WT_HEAD_V)
    c.run(24, dt=DT)
    c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
    c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6)
    return _flags(c)


def rho_or_none(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.std(a) == 0.0 or np.std(b) == 0.0:
        return None
    return float(spearmanr(a, b)[0])


def zone(rho, lo_pass, lo_refute):
    if rho is None:
        return "PARTIAL"
    if rho >= lo_pass:
        return "PASS"
    if rho <= lo_refute:
        return "REFUTED"
    return "PARTIAL"


def main() -> dict:
    print("=== exp139: Levin T5 voltage-series cross-validation ===\n")

    # ---- LV-A1: the partition + calibration anchors -----------------------
    fam, rows_by_fam = build_families()
    counts = {f: len(rows_by_fam[f]) for f in "ABCDE"}
    total = sum(counts.values())
    ids_unique = len(fam) == 119 and total == 119
    mv_entries = [eid for e in json.load(open(SERIES))["series"]
                  if e.get("vmem_mv") is not None
                  for eid in [e["id"]]]
    mv_in_e = all(fam[eid] == "E" for eid in mv_entries)

    c = make_collective(1)
    c.run(24, dt=DT)
    head_v = float(np.mean(c.V[: N // 4]))
    tail_v = float(np.mean(c.V[TAIL]))
    settled = float(np.mean(c.V))
    c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
    wound_v = float(np.mean(c.V[TAIL]))
    dep39 = json.load(open(EXP39))
    d_head = abs(head_v - dep39["items"]["V1_head_depolarized_vs_trunk"]
                 ["model"]["head_vmem_mV"])
    d_tail = abs(tail_v - dep39["items"]["V1_head_depolarized_vs_trunk"]
                 ["model"]["tail_vmem_mV"])
    d_wound = abs(wound_v - dep39["items"]["V5_wound_depolarized"]
                  ["model"]["wound_face_vmem_mV"])
    anchor_ok = bool(max(d_head, d_tail, d_wound) <= ANCHOR_TOL)
    lv_a1 = bool(ids_unique and mv_in_e and anchor_ok)
    print(f"  partition counts {counts} (total {total}, ids unique "
          f"{ids_unique}); mv entries {mv_entries} in E: {mv_in_e}")
    print(f"  calibration seed-1: head {head_v:.2f} (d {d_head:.3f}), "
          f"tail {tail_v:.2f} (d {d_tail:.3f}), wound {wound_v:.2f} "
          f"(d {d_wound:.3f})")
    print(f"  LV-A1 anchor: {'PASS' if lv_a1 else 'REFUTED'}")

    # ---- FAM-A: the intact-polarity family (stack P1 + control arm) -------
    cut_res = [cutting_arm(s) for s in SEEDS]
    cut_abn = float(np.mean([r[0] for r in cut_res]))
    stack_a = {
        "head_vmem_mV": head_v, "trunk_vmem_mV": tail_v,
        "wound_face_vmem_mV": wound_v, "settled_mean_mV": settled,
        "cutting_arm_abn_rate": cut_abn,
        "head_minus_trunk_mV": head_v - tail_v,
        "wound_minus_intact_tail_mV": wound_v - tail_v,
        "wound_minus_settled_mean_mV": wound_v - settled,
    }
    fam_a_meas = mean_non_wt(db_rows(rows_by_fam, "A"))
    print(f"\n  FAM-A stack {json.dumps({k: round(v, 3) for k, v in stack_a.items()})}")
    print(f"  FAM-A measured mean(1-WT) {fam_a_meas:.4f} over "
          f"{counts['A']} rows")

    # ---- FAM-B: the GJ-blocked family --------------------------------------
    gj_tail = [gj_arm("tail", s) for s in SEEDS]
    gj_abn = float(np.mean([r[2] >= ABN_ERR_MV or r[3] >= ABN_HL
                            for r in gj_tail]))
    gj_by_plane = {}
    for plane in SIM_PLANES:
        rows = [gj_arm(plane, s) for s in SEEDS]
        gj_by_plane[plane] = {
            "ea_rate": float(np.mean([r[0] for r in rows])),
            "abn_rate": float(np.mean([r[2] >= ABN_ERR_MV
                                       or r[3] >= ABN_HL
                                       for r in rows])),
        }
    stack_b = {"gj_arm_abn_rate_tail": gj_abn, "by_plane": gj_by_plane}
    fam_b_meas = mean_non_wt(db_rows(rows_by_fam, "B"))
    print(f"\n  FAM-B stack: tail abn {gj_abn:.3f}, by-plane EA "
          f"{ {p: round(d['ea_rate'], 3) for p, d in gj_by_plane.items()} }")
    print(f"  FAM-B measured mean(1-WT) {fam_b_meas:.4f} over "
          f"{counts['B']} rows")

    # ---- FAM-C: the hyperpolarization family ------------------------------
    ion_tail = [ion_arm("tail", s) for s in SEEDS]
    ion_abn = float(np.mean([r[2] >= ABN_ERR_MV or r[3] >= ABN_HL
                             for r in ion_tail]))
    ion_by_plane = {}
    for plane in SIM_PLANES:
        rows = [ion_arm(plane, s) for s in SEEDS]
        ion_by_plane[plane] = {
            "af_rate": float(np.mean([r[1] for r in rows])),
            "abn_rate": float(np.mean([r[2] >= ABN_ERR_MV
                                       or r[3] >= ABN_HL
                                       for r in rows])),
        }
    stack_c = {"ion_arm_abn_rate_tail": ion_abn, "by_plane": ion_by_plane}
    fam_c_meas = mean_non_wt(db_rows(rows_by_fam, "C"))
    print(f"\n  FAM-C stack: tail abn {ion_abn:.3f}, by-plane AF "
          f"{ {p: round(d['af_rate'], 3) for p, d in ion_by_plane.items()} }")
    print(f"  FAM-C measured mean(1-WT) {fam_c_meas:.4f} over "
          f"{counts['C']} rows")

    # ---- FAM-D: the depolarization family ---------------------------------
    wnt_res = [wnt_arm(s) for s in SEEDS]
    wnt_ea = float(np.mean([r[0] for r in wnt_res]))
    stack_d = {"posterior_depol_ea_rate": wnt_ea,
               "hl_per_seed": [round(r[3], 4) for r in wnt_res]}
    fam_d_meas = mean_non_wt(db_rows(rows_by_fam, "D"))
    print(f"\n  FAM-D stack: EA rate {wnt_ea:.3f} "
          f"(hl {stack_d['hl_per_seed']})")
    print(f"  FAM-D measured mean(1-WT) {fam_d_meas:.4f} over "
          f"{counts['D']} rows (n=2, the slanted-pharynx protocol — owned)")

    # ---- LV-G1: the cross-family ordering ---------------------------------
    e_stack = [cut_abn, gj_abn, ion_abn, wnt_ea]
    e_meas = [fam_a_meas, fam_b_meas, fam_c_meas, fam_d_meas]
    rho_g1 = rho_or_none(e_stack, e_meas)
    g1 = zone(rho_g1, G1_PASS, G1_REFUTE)
    print(f"\n  LV-G1 cross-family (A,B,C,D): E_stack "
          f"{[round(x, 3) for x in e_stack]} vs E_meas "
          f"{[round(x, 4) for x in e_meas]} -> Spearman {rho_g1}: {g1}")

    # ---- LV-G2: the absolute anchor (FAM-E, calibration class) ------------
    ghk = infer_vmem(MARKER_TABLE)
    ghk_v = {k: float(v["Vm_mV"]) for k, v in ghk.items()}
    inside = {k: bool(BETSE_BAND[0] <= v <= BETSE_BAND[1])
              for k, v in ghk_v.items()}
    d_head_trunk = head_v - tail_v
    d_wound_dep = wound_v - tail_v
    g2a = bool(BETSE_BAND[0] <= head_v <= BETSE_BAND[1]
               and BETSE_BAND[0] <= tail_v <= BETSE_BAND[1]
               and BETSE_BAND[0] <= wound_v <= BETSE_BAND[1])
    g2b = bool(BETSE_SWING * (1 - REL_TOL) <= d_head_trunk
               <= BETSE_SWING * (1 + REL_TOL))
    g2c = bool(CHERNET_DELTA * (1 - REL_TOL) <= d_wound_dep
               <= CHERNET_DELTA * (1 + REL_TOL))
    n_inside = sum(inside.values())
    g2d = bool(n_inside == len(ghk_v))
    lv_g2 = bool(g2a and g2b and g2c and g2d)
    outside = [k for k, ok in inside.items() if not ok]
    print(f"\n  LV-G2 absolute anchor: (a) trio in band {g2a} "
          f"(head {head_v:.2f}, trunk {tail_v:.2f}, wound {wound_v:.2f})")
    print(f"    (b) head-trunk {d_head_trunk:.2f} mV vs swing "
          f"{BETSE_SWING} +-50%: {g2b}")
    print(f"    (c) wound depol {d_wound_dep:.2f} mV vs Chernet "
          f"{CHERNET_DELTA} +-50%: {g2c}")
    print(f"    (d) GHK map in band {n_inside}/{len(ghk_v)}: {g2d} "
          f"(outside: "
          f"{[(k, round(ghk_v[k], 2)) for k in outside]})")
    print(f"  LV-G2 verdict: "
          f"{'PASS' if lv_g2 else 'RECALIBRATION TARGET (calibration class, not falsification)'}")

    # ---- LV-G3: the sign battery (strict 4/4) ------------------------------
    signs = {
        "S1_head_gt_trunk": bool(head_v > tail_v),
        "S2_wound_gt_settled": bool(wound_v > settled),
        "S3_gj_gt_cutting": bool(gj_abn > cut_abn),
        "S4_ion_gt_cutting": bool(ion_abn > cut_abn),
    }
    lv_g3 = "PASS" if all(signs.values()) else "REFUTED"
    print(f"\n  LV-G3 sign battery: {signs} -> {lv_g3}")

    # ---- LV-G4: per-plane orderings (the matched instrument) --------------
    pub_b = [PUB_OCTANOL_DH[p] for p in PUB_ORDER]
    sim_b = [gj_by_plane[TAXONOMY[p]]["ea_rate"] for p in PUB_ORDER]
    rho_b = rho_or_none(sim_b, pub_b)
    pub_c = [PUB_HEADLESS[p] for p in PUB_ORDER]
    sim_c = [ion_by_plane[TAXONOMY[p]]["abn_rate"] for p in PUB_ORDER]
    rho_c = rho_or_none(sim_c, pub_c)
    zb, zc = zone(rho_b, G4_PASS, G4_REFUTE), zone(rho_c, G4_PASS,
                                                   G4_REFUTE)
    if "REFUTED" in (zb, zc):
        g4 = "REFUTED"
    elif zb == "PASS" and zc == "PASS":
        g4 = "PASS"
    else:
        g4 = "PARTIAL"
    print(f"\n  LV-G4 per-plane: B octanol-DH {pub_b} vs stack EA "
          f"{[round(x, 3) for x in sim_b]} -> rho {rho_b} ({zb})")
    print(f"           C headless {pub_c} vs stack abn "
          f"{[round(x, 3) for x in sim_c]} -> rho {rho_c} ({zc})")
    print(f"  LV-G4 verdict: {g4}")

    # ---- the not-gated scope panel (price map v2 + deadline map) ----------
    pm2 = json.load(open(os.path.join(ROOT, "results",
                                      "price_map_v2.json")))
    scope = {
        "price_map_v2": {
            "oracle_rho_deposited": pm2.get("oracle_rho"),
            "scope_note": (
                "the v2 oracle prices stack SUBSTRATES (19 members, "
                "class-level); the exp139 family arms run on the deployed "
                "DEFAULT0 sheet cell (1, 0.015) — no per-biological-family "
                "pricing column exists, so a family-level v2 test would be "
                "an instrument mismatch. Deposited as a scope boundary, "
                "not gated."),
        },
        "deadline_map": {
            "record_kernels": {
                "durant2019_write_window_h": 3.0,
                "octanol_kernel_edge_h": "12-24 (exp130 units resolution)",
                "barium_onset_h": "48-72 (C06)",
            },
            "stack_predictors": {
                "exp54_write_window_h": 3.0,
                "exp124_125_deadline_band_h": "36-72 (gamma-dependent)",
            },
            "scope_note": (
                "exp130 REFUTED the direct kernel fit (the stack's "
                "deadline is a rescue curve; Oviedo's kernel is a damage "
                "kernel — Spearman -0.660) and exp131 landed the ion-arm "
                "plane ordering (0.649). No new timing gate is registered "
                "here; exp130's refutation stands as the timing arc's "
                "verdict."),
        },
    }

    npass = sum([lv_a1, g1 == "PASS", lv_g2, lv_g3 == "PASS",
                 g4 == "PASS"])
    print(f"\n  === {npass}/5 gates PASS (A1 {lv_a1}, G1 {g1}, "
          f"G2 {'PASS' if lv_g2 else 'RECALIBRATION'}, G3 {lv_g3}, "
          f"G4 {g4}) ===")

    result = {
        "exp": "exp139_levin_voltage",
        "task": (
            "Levin T5: voltage-series cross-validation — partition the "
            "119-entry Levin voltage series into 5 regime families, run "
            "the stack's predictors per family, and test the stack's "
            "absolute-calibration and qualitative ordering predictions "
            "against the record (research/levin_voltage_series.md T5)."),
        "partition": {
            "rule": (
                "per-row manipulation record only (drug_start_end / rnaic "
                "in the manipulation string); curated entries by explicit "
                "pre-registered table; the shared direction_signature "
                "template is NOT a per-row regime tag (owned)"),
            "counts": counts,
            "curated_assignment": CURATED_FAM,
            "fam_a_composition_note": (
                "FAM-A is the residue family (naive controls + octanol-"
                "lineage re-cut persistence rows + b-catenin/notch RNAi + "
                "field claim) — heterogeneous by construction, owned"),
        },
        "stack_by_family": {
            "A_intact_polarity": stack_a,
            "B_gj_blocked": {"gj_arm_abn_rate_tail": gj_abn,
                             "ea_by_plane": {p: d["ea_rate"] for p, d
                                             in gj_by_plane.items()},
                             "abn_by_plane": {p: d["abn_rate"] for p, d
                                              in gj_by_plane.items()}},
            "C_hyperpolarization": {"ion_arm_abn_rate_tail": ion_abn,
                                    "af_by_plane": {p: d["af_rate"] for p, d
                                                    in ion_by_plane.items()},
                                    "abn_by_plane": {p: d["abn_rate"] for p, d
                                                     in ion_by_plane.items()}},
            "D_depolarization": stack_d,
            "E_absolute_scale": {
                "ghk_map_mV": {k: round(v, 3) for k, v in ghk_v.items()},
                "ghk_inside_betse_band": inside,
                "betse_band": list(BETSE_BAND),
                "betse_bistable_swing_mV": BETSE_SWING,
                "chernet_delta_mV": CHERNET_DELTA,
            },
        },
        "measured_by_family": {
            "metric": "mean over the family's DB rows of (1 - P(Wild type))",
            "A": fam_a_meas, "B": fam_b_meas, "C": fam_c_meas,
            "D": fam_d_meas,
            "row_counts_db_only": {f: len(db_rows(rows_by_fam, f))
                                   for f in "ABCDE"},
        },
        "gates": {
            "LV_A1": {
                "verdict": "PASS" if lv_a1 else "REFUTED",
                "partition_total": total, "ids_unique": ids_unique,
                "mv_entries_in_E": mv_in_e,
                "calibration_deltas": {"head": d_head, "tail": d_tail,
                                       "wound": d_wound},
                "tolerance": ANCHOR_TOL,
            },
            "LV_G1": {
                "verdict": g1,
                "e_stack": e_stack, "e_meas": e_meas,
                "spearman": rho_g1,
                "zones": {"pass": G1_PASS, "refute": G1_REFUTE},
            },
            "LV_G2": {
                "verdict": ("PASS" if lv_g2 else
                            "RECALIBRATION TARGET (calibration class, "
                            "not falsification — the T5 md's own clause)"),
                "sub_gates": {"a_trio_in_band": g2a,
                              "b_head_trunk_vs_swing": g2b,
                              "c_wound_depol_vs_chernet": g2c,
                              "d_ghk_all_in_band": g2d},
                "head_minus_trunk_mV": d_head_trunk,
                "wound_minus_intact_tail_mV": d_wound_dep,
                "ghk_outside_band": {k: round(ghk_v[k], 2)
                                     for k in outside},
            },
            "LV_G3": {"verdict": lv_g3, "signs": signs},
            "LV_G4": {
                "verdict": g4,
                "rho_B_octanol": rho_b, "rho_C_headless": rho_c,
                "sim_b_ea_by_pub_order": sim_b, "pub_b": pub_b,
                "sim_c_abn_by_pub_order": sim_c, "pub_c": pub_c,
                "zones": {"pass": G4_PASS, "refute": G4_REFUTE},
            },
        },
        "not_gated_scope": scope,
        "criteria": {
            "LV_A1_partition_anchor": lv_a1,
            "LV_G1_cross_family_ordering": g1,
            "LV_G2_absolute_anchor": ("PASS" if lv_g2 else
                                      "RECALIBRATION"),
            "LV_G3_sign_battery": lv_g3,
            "LV_G4_per_plane_ordering": g4,
        },
        "verdict": (
            f"{npass}/5 gates PASS (A1 {'PASS' if lv_a1 else 'REFUTED'}, "
            f"G1 {g1}, G2 {'PASS' if lv_g2 else 'RECALIBRATION'}, "
            f"G3 {lv_g3}, G4 {g4})"),
        "notes": (
            "The stack makes NO quantitative absolute-Vmem prediction for "
            "the planarian families (the record has none — 0 absolute mV "
            "in 70+ years); the cross-family test is therefore the "
            "families' outcome-deviation ordering and the sign battery, "
            "with the absolute test confined to FAM-E (BETSE band, "
            "bistable swing, Chernet delta). The GHK map's depolarized "
            "tail (phagocyte %.2f mV) overshoots the BETSE tissue band — "
            "the named recalibration target, pre-registered as "
            "calibration class by the T5 md itself. D-family n=2 "
            "(ivermectin + its chloride rescue, the slanted-pharynx "
            "protocol); A-family composition heterogeneous (residue "
            "family, owned)." % ghk_v.get("phagocyte / immune", float('nan'))),
        "sources": {
            "record": "research/levin_voltage_series.json (119 entries)",
            "arms": ("experiments/exp39_levin_voltage.py V1-V5 arms "
                     "(verbatim); experiments/exp131_ion_plane_ordering.py "
                     "(plane geometry + flags); exp29-S2R3 gap_scale "
                     "mapping (GJ blockade 0.05)"),
            "predictors": (
                "cultivation/validation/vmem_inference.py (GHK, P2); "
                "results/price_map_v2.json + exp114/exp117 (scope, not "
                "gated); exp124/125 deadline map (scope, not gated; "
                "exp130's refutation owned)"),
        },
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
