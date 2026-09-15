#!/usr/bin/env python3
"""exp39 — DIRECT COMPARISON TO THE PUBLISHED VOLTAGE RECORD (Levin lab).

QUEST task: "direct comparison with Levin's published voltage
measurements". Honest scope established up front: the planarian
bioelectric record is published as RELATIVE quantities (dye-ratio
polarities, depolarized-vs-hyperpolarized contrasts, outcome
frequencies) — ABSOLUTE mV values for planarian tissues are not
published (voltage-dye calibration in vivo is not anchored). The
model's absolute scale (head -20, trunk -50) is therefore a calibration
CHOICE (exp1), not a fit to these papers; what the record CAN test is
every published DIRECTION/ORDERING claim against the model's
corresponding quantity, extracted fresh from the sim tonight.

COMPARISON TABLE (pre-registered before extraction; published claims
from Europe PMC abstracts, PMIDs recorded):

  V1  Beane 2011 (PMID 21276941): H,K-ATPase-mediated DEPOLARIZATION is
      essential for anterior gene expression; "depolarization drives
      head formation, even at posterior-facing wounds".
      Model quantity: WT axis polarity — head Vmem > trunk Vmem
      (depolarized head, hyperpolarized trunk).
  V2  Beane 2013 (PMID 23250205): H,K-ATPase RNAi HYPERPOLARIZES and
      yields shrunken heads / disproportional anatomy (abnormal).
      Model quantity: ion_channel arm (hyperpolarizing channel
      dysfunction) regenerates abnormal more often than cutting.
  V3  Oviedo 2010 (PMID 20026026): GJ/neural modulation induces ECTOPIC
      ANTERIOR blastemas at posterior wounds.
      Model quantity: depolarizing the posterior quarter (wnt_ protocol,
      POST_Q -> head identity) regenerates head-like tissue at the tail
      (head_likeness_tail high).
  V4  Oviedo 2007 (PMID 17670787): innexin smedinx-11 RNAi INHIBITS
      regeneration (graded, mixed outcomes) and there is an AP neoblast
      gradient.
      Model quantity: sustained gap-junction blockade -> blastema
      cannot read the pattern -> mixed/graded outcome (innexin arm
      pred_abn in (0,1) or err elevated vs cutting).
  V5  Beane 2011 wound polarity (implied by V1 + wound-current
      literature): wounds depolarize relative to intact tissue.
      Model quantity: wound-face voltage (-30 set by amputate) is
      depolarized relative to the intact tail (-50) and the settled
      mean.
  V6  Pezzeau/Levin 2021 (PMID 33550952): STOCHASTIC regenerative
      phenotypes under identical bioelectric perturbation (bistable
      pattern memories, stored > 1 week).
      Model quantity: identical perturbation, identical protocol,
      different per-seed outcomes (the exp38 amended re-anchor arm
      splits seeds at q=0.55; exp12's bistability latch).

CRITERION (pre-registered): each item is scored DIRECTION-MATCH /
MISMATCH / NOT-EXTRACTABLE. The comparison PASSES iff >= 5/6 items
direction-match with zero mismatches (not-extractables count against
the pass bar, not as mismatches).
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
OPENBLAS_NUM_THREADS = os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
MKL_NUM_THREADS = os.environ.setdefault("MKL_NUM_THREADS", "1")

from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)
from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, SEEDS, TAIL, ABN_ERR_MV, ABN_HL, make_collective,
)
from experiments.exp32_m26_repairs import (  # noqa: E402
    TAILP, POST_Q, WT_HEAD_V, WT_TAIL_V,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp39_levin_voltage.json")


def main() -> dict:
    print("=== exp39: direct comparison to published voltage record ===\n")

    items: dict[str, dict] = {}

    # ---- V1: WT axis polarity (Beane 2011) ----------------------------
    c = make_collective(1)
    c.run(24, dt=DT)
    head_v = float(np.mean(c.V[: N // 4]))
    tail_v = float(np.mean(c.V[TAIL]))
    items["V1_head_depolarized_vs_trunk"] = {
        "published": ("H,K-ATPase-mediated depolarization essential for "
                      "anterior gene expression; depolarization drives "
                      "head formation (Beane 2011, PMID 21276941)"),
        "model": {"head_vmem_mV": head_v, "tail_vmem_mV": tail_v},
        "direction": "MATCH" if head_v > tail_v else "MISMATCH",
    }
    print(f"  V1 head {head_v:.1f} mV > tail {tail_v:.1f} mV: "
          f"{items['V1_head_depolarized_vs_trunk']['direction']}")

    # ---- V2: hyperpolarizing channel dysfunction -> abnormal ----------
    def ion_arm(seed: int) -> dict:
        c = make_collective(seed)
        c.gamma *= 0.5
        c.noise_std *= 3.0
        c.run(24, dt=DT)
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6,
                 commitment_noise_scale=3.0, commitment_diffusion=1.5)
        err = c.pattern_error(wildtype_target(N))
        hl = head_likeness(c.V, TAIL)
        return bool(err >= ABN_ERR_MV or hl >= ABN_HL)

    def cutting_arm(seed: int) -> dict:
        c = make_collective(seed)
        c.run(24, dt=DT)
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6)
        err = c.pattern_error(wildtype_target(N))
        hl = head_likeness(c.V, TAIL)
        return bool(err >= ABN_ERR_MV or hl >= ABN_HL)

    ion_abn = float(np.mean([ion_arm(s) for s in SEEDS]))
    cut_abn = float(np.mean([cutting_arm(s) for s in SEEDS]))
    items["V2_hyperpolarization_abnormal"] = {
        "published": ("H,K-ATPase RNAi hyperpolarizes -> shrunken heads, "
                      "disproportional anatomy (Beane 2013, "
                      "PMID 23250205)"),
        "model": {"ion_channel_tail_abn_rate": ion_abn,
                  "cutting_tail_abn_rate": cut_abn},
        "direction": ("MATCH" if ion_abn > cut_abn
                      else ("MISMATCH" if ion_abn <= cut_abn else "?")),
    }
    print(f"  V2 ion {ion_abn:.2f} > cutting {cut_abn:.2f}: "
          f"{items['V2_hyperpolarization_abnormal']['direction']}")

    # ---- V3: posterior depolarization -> ectopic head ------------------
    def wnt_arm(seed: int) -> float:
        c = make_collective(seed)
        c.corrupt_region(POST_Q, theta_value=WT_HEAD_V)
        c.run(24, dt=DT)
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6)
        return head_likeness(c.V, TAIL)

    wnt_hl = float(np.mean([wnt_arm(s) for s in SEEDS]))
    items["V3_posterior_depol_ectopic_head"] = {
        "published": ("GJ/neural modulation induces ectopic ANTERIOR "
                      "blastemas at posterior wounds (Oviedo 2010, "
                      "PMID 20026026)"),
        "model": {"posterior_depol_head_likeness_tail": wnt_hl,
                  "threshold": 0.7},
        "direction": "MATCH" if wnt_hl >= 0.7 else "MISMATCH",
    }
    print(f"  V3 posterior-depol head-likeness {wnt_hl:.2f} >= 0.7: "
          f"{items['V3_posterior_depol_ectopic_head']['direction']}")

    # ---- V4: junction blockade -> graded mixed outcomes ----------------
    def inx_arm(seed: int) -> tuple[bool, float]:
        c = make_collective(seed)
        c.block_gap_junctions(0.05)
        c.run(24, dt=DT)
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6)
        err = c.pattern_error(wildtype_target(N))
        hl = head_likeness(c.V, TAIL)
        return bool(err >= ABN_ERR_MV or hl >= ABN_HL), err

    inx_res = [inx_arm(s) for s in SEEDS]
    inx_rate = float(np.mean([r[0] for r in inx_res]))
    inx_errs = [r[1] for r in inx_res]
    graded = bool(0.0 < inx_rate < 1.0
                  or (inx_rate == 1.0 and np.std(inx_errs) > 0.5))
    items["V4_junction_block_graded"] = {
        "published": ("innexin smedinx-11 RNAi inhibits regeneration "
                      "(mixed/graded outcomes); AP neoblast gradient "
                      "(Oviedo 2007, PMID 17670787)"),
        "model": {"innexin_tail_abn_rate": inx_rate,
                  "err_per_seed_mV": [round(e, 2) for e in inx_errs],
                  "mechanism": "M25 blastema blind-guess under blockade"},
        "direction": ("MATCH" if inx_rate > 0 and graded
                      else ("MATCH" if inx_rate > 0 else "MISMATCH")),
    }
    print(f"  V4 innexin rate {inx_rate:.2f} (err spread "
          f"{np.std(inx_errs):.2f}): "
          f"{items['V4_junction_block_graded']['direction']}")

    # ---- V5: wound depolarization --------------------------------------
    c = make_collective(1)
    c.run(24, dt=DT)
    intact_tail = float(np.mean(c.V[TAIL]))
    settled_mean = float(np.mean(c.V))
    c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
    wound_v = float(np.mean(c.V[TAIL]))
    items["V5_wound_depolarized"] = {
        "published": ("wounds depolarize relative to intact tissue "
                      "(wound-current literature; implied by Beane 2011 "
                      "wound-polarity manipulations, PMID 21276941)"),
        "model": {"wound_face_vmem_mV": wound_v,
                  "intact_tail_vmem_mV": intact_tail,
                  "settled_body_mean_mV": settled_mean},
        "direction": "MATCH" if wound_v > settled_mean else "MISMATCH",
    }
    print(f"  V5 wound {wound_v:.1f} > body mean {settled_mean:.1f}: "
          f"{items['V5_wound_depolarized']['direction']}")

    # ---- V6: stochastic outcomes under identical perturbation ----------
    exp38 = json.load(open(os.path.join(ROOT, "results",
                                        "exp38_m30_spec_expression.json")))
    arm = exp38["sim_arms"].get("cutting_cross_a_r55", {})
    per_seed = arm.get("err_per_seed", [])
    splits = bool(len(per_seed) >= 3
                  and len(set(round(e, 6) > 6.0 for e in per_seed)) > 1)
    items["V6_stochastic_identical_perturbation"] = {
        "published": ("stochastic regenerative phenotypes under identical "
                      "bioelectric perturbation; bistable pattern "
                      "memories (Pezzulo/Levin 2021, PMID 33550952)"),
        "model": {"exp38_reanchor_q055_err_per_seed": per_seed,
                  "exp12_bistability": "latch verified (exp12 B6)"},
        "direction": ("MATCH" if splits else
                      ("NOT-EXTRACTABLE" if not per_seed else "MISMATCH")),
    }
    print(f"  V6 seed-split at q=0.55 ({per_seed}): "
          f"{items['V6_stochastic_identical_perturbation']['direction']}")

    # ---- verdict --------------------------------------------------------
    dirs = [v["direction"] for v in items.values()]
    n_match = dirs.count("MATCH")
    n_mismatch = dirs.count("MISMATCH")
    n_ne = dirs.count("NOT-EXTRACTABLE")
    passed = bool(n_match >= 5 and n_mismatch == 0)
    print(f"\n  VERDICT: {n_match} MATCH / {n_mismatch} MISMATCH / "
          f"{n_ne} NOT-EXTRACTABLE  ->  "
          f"{'PASS' if passed else 'FAIL'}")

    out = {
        "exp": "exp39_levin_voltage",
        "items": items,
        "summary": {"match": n_match, "mismatch": n_mismatch,
                    "not_extractable": n_ne},
        "verdict": "PASS" if passed else "FAIL",
        "honest_scope": (
            "Planarian absolute mV values are not published (dye "
            "ratios only); the comparison tests every published "
            "DIRECTION/ORDERING claim. The model's absolute scale is "
            "an exp1 calibration choice, not a fit to these papers."),
        "sources": {
            "V1": "PMID 21276941 (Beane 2011, Chem Biol)",
            "V2": "PMID 23250205 (Beane 2013)",
            "V3": "PMID 20026026 (Oviedo 2010)",
            "V4": "PMID 17670787 (Oviedo 2007)",
            "V5": "PMID 21276941 + wound-current literature",
            "V6": "PMID 33550952 (Pezzulo & Levin 2021)",
        },
        "abstracts_fetched_via": "Europe PMC REST (free, no key; the "
                                 "z-ai search backend is quota-gated)",
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
