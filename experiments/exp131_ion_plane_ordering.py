#!/usr/bin/env python3
"""exp131 — THE ION-ARM PLANE ORDERING (Task 5-g / T2 of the Levin-series
ranked targets, research/levin_voltage_series.md §4 T2).

THE RECORD (research/levin_voltage_series.json, Beane 2011 rows,
PMID 21276941, D. japonica, all SCH-28080 schedules (0.0, 3.0) =
sustained days 0-3):

  The headless-by-plane series (eids 391-395, n = 106-175):
    head crop          0.00  (n=120)
    pre-pharyngeal     0.00  (n=138)
    pharyngeal         0.67  (n=175)
    post-pharyngeal    0.16  (n=111)
    tail crop          0.40  (n=106)
  The opposing pair (the SAME "pharynx fragment with slanted anterior"
  protocol, eids 411/412, n = 11/13):
    ivermectin (depolarizer, sustained)  -> DH 0.92
    SCH-28080  (H,K-ATPase block)        -> headless 1.00
  (context rows, deposited not gated: chloride+ivermectin rescue WT 0.63,
  eid 413; SCH+K+ rescue WT 0.94, eid 297; nicardipine cyclop 0.34,
  eid 414.)

THE MAPPING (ledger L103-L104's record mapping completed in exp123; the
arm quantities are the stack-constants block's deposited model quantities
= the series' V2/V3 entries):
  SCH-28080 (hyperpolarizing H,K-ATPase block -> anterior failure) = the
    ION_CHANNEL arm family: gamma x0.5, noise x3.0,
    commitment_noise_scale 3.0, commitment_diffusion 1.5 — exp39's V2 arm
    (deposited ion_channel_tail_abn_rate 1.0 vs cutting 0.0) and the DB
    ion_channel group's arm in the corpus machinery (exp70.run_arm
    protocol "ion_channel"; exp118.map_arm maps the group's rows there).
  Ivermectin (depolarizer -> ectopic anterior at posterior-facing
    wounds) = its RECORDED arm: the posterior-depolarization arm,
    exp39's V3 arm (corrupt POST_Q to head identity; deposited
    head-likeness 0.9462 >= threshold 0.7).
  Planes: the corpus's PRE-REGISTERED plane taxonomy
  (experiments/planform_mining.py, "registered 2026-09-15, BEFORE any
  per-plane outcome"): head crop AND pre-pharyngeal crop -> head;
  pharyngeal crop -> trunk; post-pharyngeal crop AND tail crop -> tail
  (post-pharyngeal is the posterior family). No plane mapping is chosen
  for this test.

SCOPING NOTE (owned): experiments/exp86_regen_read.py's run_arm86
carries no ion_channel/wnt protocol (its protocols are
neoblast/generic/control), so the gates run on the ion_channel family's
actual arms VERBATIM (exp39's V2/V3 arms; exp70.run_arm's protocol
table). run_arm86 + M33_KW are used for a NOT-GATED harness-continuity
panel against exp86's deposited M33-read rates (the chain read
machinery the corpus now runs).

PRE-REGISTERED GATES (thresholds stated BEFORE running):

  IP-A1  (ANCHOR — exp39 continuity) the verbatim arms at seeds (1,2,3)
         reproduce all three deposited exp39 model quantities
         (results/exp39_levin_voltage.json): ion_channel_tail_abn_rate
         1.0, cutting_tail_abn_rate 0.0, posterior_depol_head_likeness_
         tail 0.9462 — each within 0.125.
  IP-G1  (ORDERING gate — two-sided) Spearman(published headless by
         plane [0.00, 0.00, 0.67, 0.16, 0.40] across
         head/pre-pharyngeal/pharyngeal/post-pharyngeal/tail, sim
         ion-arm abnormal rate mapped through the pre-registered plane
         taxonomy) >= 0.6 -> PASS (the md T2's registered bar);
         <= -0.3 -> REFUTED (anti-ordered: failure ordering runs
         anterior-ward); (-0.3, 0.6) -> PARTIAL (measured concordance,
         owned honestly); undefined (degenerate) -> PARTIAL.
  IP-G2  (THE 2x2 SIGN gate — strict, two-sided) on the tail-plane
         fragment protocol (the exp39-V2/V3 plane, the sim's
         posterior-facing-wound analog), per-seed flags:
           EA = head-likeness(c.V, TAIL) >= 0.7        (the DH sign)
           AF = pattern_error(WT) >= 6.0 AND NOT EA    (the headless sign)
         cells P_I(EA), P_I(AF) (ivermectin arm), P_S(EA), P_S(AF)
         (SCH-28080 arm):
           PASS   iff P_I(EA) >= 0.5 (pub DH 0.92) AND P_S(AF) >= 0.5
                  (pub headless 1.00) AND P_I(EA) > P_S(EA) AND
                  P_S(AF) > P_I(AF)  — both diagonal cells majority AND
                  the off-diagonal ordering strict;
           REFUTED iff either diagonal is INVERTED (P_S(EA) > P_I(EA)
                  or P_I(AF) > P_S(AF)) — the md's strict clause: one
                  wrong sign refutes the polarity mapping;
           else   PARTIAL.

RUN: anchors 3 arms x 3 seeds; ordering 3 planes x 3 seeds (+ the
exp70-variant robustness 3 x 3); 2x2 = the anchored arms' per-seed
flags; run_arm86 continuity 3 planes x 10 seeds. Seconds. Serial, BLAS
pinned.
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
from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, SEEDS, TAIL, ABN_ERR_MV, ABN_HL, make_collective,
)
from experiments.exp32_m26_repairs import (  # noqa: E402
    HEAD as HEAD_SL, TAILP, TRUNK, POST_Q, WT_HEAD_V,
)
from experiments.exp70_onset_corpus import run_arm  # noqa: E402
from experiments.exp86_regen_read import M33_KW, run_arm86  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp131_ion_plane_ordering.json")

# ---- the record (research/levin_voltage_series.json, Beane 2011 rows) ----
PUB_ORDER = ("head", "pre_pharyngeal", "pharyngeal",
             "post_pharyngeal", "tail")
PUB_HEADLESS = {"head": 0.00,        # eid 391, n=120
                "pre_pharyngeal": 0.00,   # eid 392, n=138
                "pharyngeal": 0.67,       # eid 393, n=175
                "post_pharyngeal": 0.16,  # eid 394, n=111
                "tail": 0.40}             # eid 395, n=106
PUB_EIDS = {"head": 391, "pre_pharyngeal": 392, "pharyngeal": 393,
            "post_pharyngeal": 394, "tail": 395}
# the corpus's pre-registered plane taxonomy (planform_mining.py)
TAXONOMY = {"head": "head", "pre_pharyngeal": "head",
            "pharyngeal": "trunk", "post_pharyngeal": "tail",
            "tail": "tail"}
IVERM_DH = 0.92          # eid 411, n=11 (Double head, one pharynx)
SCH_HEADLESS = 1.00      # eid 412, n=13 (Headless)

# ---- deposited anchors (results/exp39_levin_voltage.json V2/V3) -----------
DEP_ION_ABN = 1.0
DEP_CUT_ABN = 0.0
DEP_WNT_HL = 0.9462486413762442
ANCHOR_TOL = 0.125
G1_PASS, G1_REFUTE = 0.6, -0.3      # IP-G1 two-sided zones (pre-registered)
SIM_SIM_PLANES = ("head", "trunk", "tail")

WT = wildtype_target(N)


# ---- the exp39 arms, VERBATIM (experiments/exp39_levin_voltage.py
#      V2 ion_arm / cutting_arm; V3 wnt_arm — same kwargs, same readouts),
#      with the ion arm extended to the corpus's three planes via exp70's
#      amputate/regrow geometry (the anchor plane 'tail' is exp39's own).
def _flags(c) -> tuple[bool, bool, float, float]:
    err = float(c.pattern_error(WT))
    hl = float(head_likeness(c.V, TAIL))
    ea = bool(hl >= ABN_HL)
    af = bool(err >= ABN_ERR_MV and not ea)
    return ea, af, err, hl


def ion_arm(plane: str, seed: int) -> tuple[bool, bool, bool, float, float]:
    """exp39 V2 ion_arm verbatim (gamma x0.5, noise x3.0,
    commitment_noise_scale 3.0, commitment_diffusion 1.5); plane
    geometry from exp70.run_arm (tail = exp39's own plane)."""
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
    ea, af, err, hl = _flags(c)
    return ea, af, bool(err >= ABN_ERR_MV or hl >= ABN_HL), err, hl


def cutting_arm(seed: int) -> bool:
    """exp39 V2 cutting_arm verbatim (the anchor's control)."""
    c = make_collective(seed)
    c.run(24, dt=DT)
    c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
    c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6)
    err = c.pattern_error(WT)
    hl = head_likeness(c.V, TAIL)
    return bool(err >= ABN_ERR_MV or hl >= ABN_HL)


def wnt_arm(seed: int) -> tuple[float, bool, bool, float]:
    """exp39 V3 wnt_arm verbatim (ivermectin's recorded arm):
    posterior quarter corrupted to head identity -> DH sign at the
    posterior regenerate."""
    c = make_collective(seed)
    c.corrupt_region(POST_Q, theta_value=WT_HEAD_V)
    c.run(24, dt=DT)
    c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
    c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6)
    ea, af, err, hl = _flags(c)
    return hl, ea, af, err


def rho_or_none(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if np.std(a) == 0.0 or np.std(b) == 0.0:
        return None
    return float(spearmanr(a, b)[0])


def main() -> dict:
    print("=== exp131: the ion-arm plane ordering (Beane 2011) ===\n")

    # ---- IP-A1: the exp39 anchors (the arms verbatim) ---------------------
    ion_tail = [ion_arm("tail", s) for s in SEEDS]
    cut_tail = [cutting_arm(s) for s in SEEDS]
    wnt_res = [wnt_arm(s) for s in SEEDS]
    ion_abn = float(np.mean([r[2] for r in ion_tail]))
    cut_abn = float(np.mean(cut_tail))
    wnt_hls = [r[0] for r in wnt_res]
    wnt_hl = float(np.mean(wnt_hls))
    d_ion = abs(ion_abn - DEP_ION_ABN)
    d_cut = abs(cut_abn - DEP_CUT_ABN)
    d_wnt = abs(wnt_hl - DEP_WNT_HL)
    ip_a1 = bool(d_ion <= ANCHOR_TOL and d_cut <= ANCHOR_TOL
                 and d_wnt <= ANCHOR_TOL)
    print(f"  IP-A1 anchor: ion_tail_abn {ion_abn:.3f} (dep {DEP_ION_ABN}), "
          f"cut_tail_abn {cut_abn:.3f} (dep {DEP_CUT_ABN}), "
          f"wnt_hl {wnt_hl:.4f} (dep {DEP_WNT_HL:.4f}) "
          f"-> {'PASS' if ip_a1 else 'REFUTED'}")

    # ---- the ordering panel (ion arm by plane, seeds 1-3) -----------------
    sim_by_plane: dict = {}
    per_seed: dict = {}
    for plane in SIM_SIM_PLANES:
        rows = [ion_arm(plane, s) for s in SEEDS]
        sim_by_plane[plane] = float(np.mean([r[2] for r in rows]))
        per_seed[plane] = [{"seed": s, "abn": r[2], "ea": r[0],
                            "af": r[1], "err": round(r[3], 2),
                            "hl": round(r[4], 3)}
                           for s, r in zip(SEEDS, rows)]
    sim_vec = [sim_by_plane[TAXONOMY[p]] for p in PUB_ORDER]
    pub_vec = [PUB_HEADLESS[p] for p in PUB_ORDER]
    rho = rho_or_none(sim_vec, pub_vec)
    if rho is None:
        g1 = "PARTIAL"
    elif rho >= G1_PASS:
        g1 = "PASS"
    elif rho <= G1_REFUTE:
        g1 = "REFUTED"
    else:
        g1 = "PARTIAL"
    print(f"\n  ordering (published order {PUB_ORDER}):")
    print(f"    pub headless {pub_vec} (eids {[PUB_EIDS[p] for p in PUB_ORDER]})")
    print(f"    sim ion abn  {sim_vec} via taxonomy "
          f"{ {p: TAXONOMY[p] for p in PUB_ORDER} }")
    print(f"  IP-G1 ordering (Spearman {rho}): {g1}")

    # robustness: the corpus-mapped ion arm (exp70.run_arm, the
    # run_gj_onset file's protocol table — adds the readout kwargs
    # phi_readout/neural_readout/arz_readout/commitment_delay)
    rob = {}
    for plane in SIM_SIM_PLANES:
        rob[plane] = float(np.mean(
            [run_arm("ion_channel", plane, 0.5, s) for s in SEEDS]))
    rob_vec = [rob[TAXONOMY[p]] for p in PUB_ORDER]
    rho_rob = rho_or_none(rob_vec, pub_vec)
    rob_wnt = float(np.mean(
        [run_arm("wnt", "tail", 0.5, s) for s in SEEDS]))
    print(f"  [robustness] exp70-run_arm ion rates {rob} "
          f"(Spearman {rho_rob}); exp70-kwargs wnt abn {rob_wnt:.3f}")

    # ---- IP-G2: the 2x2 sign gate (the anchored arms, tail plane) ---------
    p_i_ea = float(np.mean([r[1] for r in wnt_res]))
    p_i_af = float(np.mean([r[2] for r in wnt_res]))
    p_s_ea = float(np.mean([r[0] for r in ion_tail]))
    p_s_af = float(np.mean([r[1] for r in ion_tail]))
    inverted = bool(p_s_ea > p_i_ea or p_i_af > p_s_af)
    diagonal = bool(p_i_ea >= 0.5 and p_s_af >= 0.5
                    and p_i_ea > p_s_ea and p_s_af > p_i_af)
    if inverted:
        g2 = "REFUTED"
    elif diagonal:
        g2 = "PASS"
    else:
        g2 = "PARTIAL"
    print(f"\n  IP-G2 the ivermectin/SCH 2x2 (tail-plane fragment):")
    print(f"    ivermectin arm: P(EA) {p_i_ea:.3f} (pub DH {IVERM_DH}), "
          f"P(AF) {p_i_af:.3f}")
    print(f"    SCH-28080 arm:  P(EA) {p_s_ea:.3f}, "
          f"P(AF) {p_s_af:.3f} (pub headless {SCH_HEADLESS})")
    print(f"  IP-G2 2x2 sign (strict): {g2}")

    # ---- continuity panel (run_arm86, NOT gated) --------------------------
    cont = {}
    for plane in SIM_SIM_PLANES:
        cont[plane] = float(np.mean(
            [run_arm86(plane, s, None, read_kw=M33_KW)
             for s in range(1, 11)]))
    exp86 = json.load(open(os.path.join(
        ROOT, "results", "exp86_regen_read.json")))
    dep86 = exp86["m33_read_coin_off"]
    cont_d = max(abs(cont[p] - dep86[p]) for p in SIM_SIM_PLANES)
    print(f"\n  [continuity] run_arm86+M33 read {cont} vs deposited "
          f"{dep86} (max|delta| {cont_d:.3f}, not gated)")

    npass = sum([ip_a1, g1 == "PASS", g2 == "PASS"])
    print(f"\n  === {npass}/3 gates PASS "
          f"(anchor {'PASS' if ip_a1 else 'REFUTED'}, "
          f"ordering {g1}, 2x2 {g2}) ===")

    result = {
        "exp": "exp131_ion_plane_ordering",
        "task": (
            "T2 of the Levin-series ranked targets "
            "(research/levin_voltage_series.md): the ion-arm headless "
            "ordering vs Beane 2011's plane series + the strict "
            "ivermectin/SCH 2x2 sign test, on the chain corpus "
            "machinery."),
        "record": {
            "pub_headless_by_plane": PUB_HEADLESS,
            "pub_eids": PUB_EIDS,
            "pub_order": list(PUB_ORDER),
            "ivermectin_dh": IVERM_DH,
            "sch_headless": SCH_HEADLESS,
            "source": ("research/levin_voltage_series.json DB-391..395, "
                       "DB-411/412 (Beane 2011, PMID 21276941); "
                       "0 of 3 web-search queries spent — every number "
                       "was already in the repo's series JSON"),
        },
        "mapping": {
            "sch_28080": ("ion_channel arm family (gamma x0.5, noise "
                          "x3.0, commitment_noise_scale 3.0, "
                          "commitment_diffusion 1.5): exp39 V2's arm; "
                          "exp70.run_arm protocol 'ion_channel'; "
                          "exp118.map_arm sends the DB ion_channel "
                          "group's rows there"),
            "ivermectin": ("its recorded arm = the posterior-"
                           "depolarization arm (exp39 V3: corrupt "
                           "POST_Q to head identity; deposited HL "
                           "0.9462 >= 0.7)"),
            "plane_taxonomy": TAXONOMY,
            "taxonomy_provenance": (
                "experiments/planform_mining.py 'PLANE TAXONOMY "
                "(pre-registered 2026-09-15, BEFORE any per-plane "
                "outcome)': pre-pharyngeal -> head, post-pharyngeal -> "
                "tail; no mapping chosen for this test"),
            "scoping_note": (
                "run_arm86 (exp86) carries no ion_channel/wnt protocol "
                "(neoblast/generic/control only); the gates run on the "
                "ion_channel family's arms verbatim (exp39 V2/V3; "
                "exp70.run_arm); run_arm86+M33_KW serve the not-gated "
                "continuity panel."),
        },
        "anchor": {
            "gate": "IP-A1 (exp39 V2/V3 quantities within 0.125)",
            "fresh": {"ion_tail_abn": ion_abn, "cut_tail_abn": cut_abn,
                      "wnt_hl_tail": wnt_hl},
            "deposited": {"ion_tail_abn": DEP_ION_ABN,
                          "cut_tail_abn": DEP_CUT_ABN,
                          "wnt_hl_tail": DEP_WNT_HL},
            "max_abs_delta": round(max(d_ion, d_cut, d_wnt), 4),
            "verdict": "PASS" if ip_a1 else "REFUTED",
        },
        "ordering": {
            "sim_by_plane": sim_by_plane,
            "per_seed": per_seed,
            "sim_vector_pub_order": sim_vec,
            "pub_vector": pub_vec,
            "spearman": rho,
            "verdict": g1,
            "robustness_exp70_run_arm": {
                "rates_by_plane": rob,
                "vector_pub_order": rob_vec,
                "spearman": rho_rob,
                "wnt_abn_exp70_kwargs": round(rob_wnt, 4),
                "note": ("the corpus-mapped kwargs variant adds "
                         "phi_readout/neural_readout/arz_readout/"
                         "commitment_delay; deposited, not gated"),
            },
        },
        "two_by_two": {
            "p_iverm_ectopic_anterior": p_i_ea,
            "p_iverm_anterior_failure": p_i_af,
            "p_sch_ectopic_anterior": p_s_ea,
            "p_sch_anterior_failure": p_s_af,
            "per_seed_iverm": [{"seed": s, "hl": round(r[0], 4),
                                "ea": r[1], "af": r[2],
                                "err": round(r[3], 2)}
                               for s, r in zip(SEEDS, wnt_res)],
            "per_seed_sch": [{"seed": s, "ea": r[0], "af": r[1],
                              "abn": r[2], "err": round(r[3], 2),
                              "hl": round(r[4], 3)}
                             for s, r in zip(SEEDS, ion_tail)],
            "inverted": inverted,
            "diagonal_majority_strict": diagonal,
            "verdict": g2,
        },
        "continuity_panel_not_gated": {
            "run_arm86_m33_read": cont,
            "deposited_exp86": dep86,
            "max_abs_delta": round(cont_d, 4),
        },
        "criteria": {
            "IP_A1_anchor_exp39": ip_a1,
            "IP_G1_plane_ordering": g1,
            "IP_G2_two_by_two_sign": g2,
        },
        "verdict": (
            f"{npass}/3 gates PASS (ordering {g1}, 2x2 {g2}; "
            f"anchor {'PASS' if ip_a1 else 'REFUTED'})"),
        "notes": (
            "Zero-free-parameter test at the recorded operating points: "
            "the ion_channel family's arm and the posterior-depol arm "
            "are the deposited exp39 V2/V3 objects run verbatim (anchored "
            "to their deposited quantities, seeds 1-3, the md T2's "
            "'5 planes x 3 seeds; exp39 machinery' runtime); the plane "
            "mapping is the corpus's pre-registered taxonomy. The 2x2's "
            "readouts: EA = head-likeness >= 0.7 (the DH sign, exp39 "
            "V3's deposited threshold = the corpus's ABN_HL), AF = "
            "pattern error >= 6.0 without EA (the headless sign). "
            "HONEST SCOPE OF IP-G1's PASS: it is specific to the "
            "anchored exp39-verbatim arm; the corpus-mapped exp70.run_arm "
            "kwargs variant (readout knobs + commitment_delay) "
            "ANTI-ORDERS (Spearman -0.725, trunk 0.0) — deposited under "
            "robustness, so the ordering claim's arm-dependence is on "
            "record, not hidden. The 2x2's ivermectin cell is robust "
            "(the exp70-kwargs wnt arm also reads abnormal 1.0). "
            "Context rows deposited not gated: chloride rescue WT 0.63 "
            "(eid 413), K+ rescue WT 0.94 (eid 297), nicardipine cyclop "
            "0.34 / headless 0.08 (eid 414)."),
        "sources": {
            "record": ("research/levin_voltage_series.json DB-391..395, "
                       "DB-411..414, DB-296/297 (Beane 2011, PMID "
                       "21276941)"),
            "arms": ("experiments/exp39_levin_voltage.py V2/V3 arms "
                     "(verbatim; results/exp39_levin_voltage.json "
                     "anchor); experiments/exp70_onset_corpus.py "
                     "run_arm/run_gj_onset protocol table (robustness); "
                     "experiments/exp86_regen_read.py run_arm86+M33_KW "
                     "(continuity, not gated)"),
            "harness_continuity": ("ledger L103-L104 (the record mapping "
                                   "completes: dual-channel pharmacology "
                                   "vs partial-channel); "
                                   "results/exp86_regen_read.json"),
        },
    }
    with open(OUT, "w") as f:
        json.dump(result, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return result


if __name__ == "__main__":
    main()
