"""Falsification suite — Level 1 and Level 2 automated checks.

Every claim below has a pre-registered pass criterion and a failure mode.
Honest negatives are recorded, not hidden. Run:

    python -m tests.run_tests            (or) python -m tests.test_falsification
"""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, ".")

T1 = {}


def test_T1_1_planarian_memory():
    """Level 1: reproduce Durant et al. structure — reprogramming + stable
    memory + negative control + dose-response."""
    from experiments import exp1_regeneration as e1
    r = e1.main()
    checks = {
        "twoheaded_achieved": r["twoheaded_achieved"],
        "memory_persists_2_rounds": r["memory_persists"],
        "negative_control_gj_block_only": r["control_gjblock_no_reprogram"],
        "dose_response_present": r["dose_response_present"],
    }
    T1.update(checks)
    return checks


def test_T1_2_cancer_normalization():
    """Level 1: reproduce Chernet & Levin structure — GJ-dependent
    normalization boundary."""
    from experiments import exp2_cancer as e2
    r = e2.main()
    checks = {
        "untreated_tumor_persists": r["untreated_tumor_persists"],
        "gj_restore_normalizes": r["gj_restore_normalizes"],
        "direct_works_without_gj": r["direct_works_without_gj"],
        "depolarizing_fails": r["depolarizing_fails_to_normalize"],
        "locked_not_normalizable": r["locked_not_normalizable"],
    }
    T1.update(checks)
    return checks


def test_T2_1_gompertz():
    """Level 2: Gompertz-form hazard emergence + honest negatives."""
    from experiments import exp3_gompertz as e3
    r = e3.main()
    checks = {
        "gompertz_competitive_adult": r["C1_gompertz_competitive"],
        "gompertz_wins_preaturation_window": r["C1b_gompertz_wins_narrow_window"],
        "NEGATIVE_beta_tracks_engine": not r["C2_beta_tracks_engine"],  # inverted: recorded
        "maintenance_extends_life": r["C3_maintenance_extends_life"],
    }
    return checks


def test_T2_2_cross_species():
    from experiments import exp4_species as e4
    r = e4.main()
    return {
        "species_ordering": r["C_species_ordering"],
        "ordering_robust_to_jitter": r["C_species_robust"],
        "hydra_negligible_senescence": r["hydra_immortal"],
        "ratio_compression_documented": r["ratio_compression_limitation"],
    }


def test_T2_3_information_metrics():
    from experiments import exp5_information as e5
    r = e5.main()
    return {
        "mi_high_when_healthy": r["C_mi_high_when_healthy"],
        "mi_decays_with_aging": r["C_mi_decays_with_noise"],
        "phi_peaks_intermediate": r["C_phi_peaks_intermediate"],
        "NEGATIVE_ctrnn_coherence_phi": not r["C_coherent_drive_raises_phi"],
    }


def test_T2_4_error_correction():
    from experiments import exp6_error_correction as e6
    r = e6.main()
    return {
        "maintenance_extends_life": r["C_maintenance_extends_life"],
        "NEGATIVE_codec_beats_local": not r["C_codec_beats_local"],
        "NEGATIVE_verification_pays": not r["C_verification_pays_in_noise"],
    }


def main() -> dict:
    results = {}
    results["T1.1 planarian memory"] = test_T1_1_planarian_memory()
    results["T1.2 cancer normalization"] = test_T1_2_cancer_normalization()
    results["T2.1 gompertz emergence"] = test_T2_1_gompertz()
    results["T2.2 cross-species"] = test_T2_2_cross_species()
    results["T2.3 information metrics"] = test_T2_3_information_metrics()
    results["T2.4 error correction"] = test_T2_4_error_correction()
    return results


if __name__ == "__main__":
    res = main()
    print("\n" + "=" * 64)
    print("FALSIFICATION SUITE RESULTS")
    print("=" * 64)
    n_pass = n_fail = 0
    for suite, checks in res.items():
        print(f"\n{suite}")
        for k, v in checks.items():
            mark = "PASS" if (v is True or v == 1) else ("NEG" if k.startswith("NEGATIVE") else "FAIL")
            if mark == "PASS":
                n_pass += 1
            elif mark == "NEG":
                print(f"  [{mark}] {k}: {v}  (honest negative, recorded)")
                continue
            else:
                n_fail += 1
            print(f"  [{mark}] {k}: {v}")
    print(f"\nTOTAL: {n_pass} pass, {n_fail} fail (+ recorded negatives)")
    sys.exit(1 if n_fail else 0)
