# Experiment index

## Confirmatory (pre-registered in docs/PRIMARIES.md)
| Script | Primary | Verdict |
|---|---|---|
| exp448_p1_target_memory.py | P1 target memory | PASS |
| exp449_p2_maintenance.py | P2 sustained > one-shot | PASS |
| exp450_p3_engine_variant.py | P3 Gompertz-rate repair | FAIL |
| exp452_p3prime_odds_link.py | P3′ odds hazard link | FAIL |
| exp453_p5_p1_robustness.py | P5 P1 parameter robustness | PASS |
| exp454_p4_information_loss.py | P4 information loss beyond noise | PASS (small) |
| exp456_p6_eps_time.py | P6 ε × exposure-time threshold | PASS |
| exp457_p7_escape.py | P7 what must be repaired for escape | PASS |
| exp458_p8_repair_frontier.py | P8 repair-budget frontier | PASS |
| exp459_p9_which_clock.py | P9 noise clock carries synergy | PASS |

## Review diagnostics
| Script | Purpose |
|---|---|
| exp447_beta_sensitivity.py | what sets Gompertz β (pre-registered audit check) |
| exp451_exploratory_h0_zero.py | post-hoc P3 follow-up (exploratory) |
| exp455_exploratory_odds_h0_zero.py | post-hoc P3′ follow-up (exploratory) |

## Foundational (reproduced by tests)
exp1_regeneration, exp2_cancer, exp3_gompertz, exp5_information, exp6_error_correction, exp8_fidelity.

## Everything else (exp4–exp446)
Exploratory record. These are not claims. The scripts stay in place because many import one another.
