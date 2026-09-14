# Fidelity Sweep Report — Level-3 gate robustness

- Shards aggregated: **24/24**
- Gate holds (codec/local >= 1.03): **24/24** (100%)
- Mean codec/local: **x1.548**  |  mean codec/none: x1.572  |  mean regen/none: x1.653

## Landscape cells (kappa x f_crit x jump_rate)

| kappa | f_crit | jump | none | local | codec | regen | chan | blind | codec/local | gate |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.020 | 0.55 | 0.003 | 111 | 112 | 135 | 143 | 135 | 135 | x1.204 | HOLDS |
| 0.020 | 0.55 | 0.005 | 89 | 92 | 131 | 140 | 131 | 131 | x1.422 | HOLDS |
| 0.030 | 0.55 | 0.005 | 85 | 86 | 105 | 107 | 107 | 107 | x1.222 | HOLDS |
| 0.030 | 0.55 | 0.008 | 71 | 70 | 103 | 105 | 103 | 103 | x1.472 | HOLDS |
| 0.030 | 0.62 | 0.003 | 88 | 87 | 103 | 107 | 106 | 106 | x1.185 | HOLDS |
| 0.030 | 0.62 | 0.005 | 72 | 74 | 103 | 105 | 104 | 104 | x1.388 | HOLDS |
| 0.030 | 0.62 | 0.008 | 60 | 60 | 99 | 103 | 100 | 100 | x1.643 | HOLDS |
| 0.030 | 0.7 | 0.003 | 75 | 76 | 98 | 102 | 102 | 102 | x1.290 | HOLDS |
| 0.030 | 0.7 | 0.005 | 60 | 61 | 98 | 97 | 98 | 98 | x1.593 | HOLDS |
| 0.030 | 0.7 | 0.008 | 50 | 52 | 92 | 92 | 93 | 93 | x1.793 | HOLDS |
| 0.020 | 0.55 | 0.008 | 72 | 71 | 127 | 136 | 122 | 122 | x1.802 | HOLDS |
| 0.020 | 0.62 | 0.003 | 96 | 97 | 131 | 140 | 129 | 129 | x1.344 | HOLDS |
| 0.020 | 0.62 | 0.005 | 77 | 80 | 126 | 140 | 124 | 124 | x1.575 | HOLDS |
| 0.020 | 0.62 | 0.008 | 61 | 60 | 121 | 129 | 117 | 117 | x2.014 | HOLDS |
| 0.020 | 0.7 | 0.003 | 78 | 79 | 124 | 133 | 121 | 121 | x1.564 | HOLDS |
| 0.020 | 0.7 | 0.005 | 61 | 62 | 119 | 125 | 114 | 114 | x1.915 | HOLDS |
| 0.020 | 0.7 | 0.008 | 49 | 53 | 109 | 107 | 104 | 104 | x2.044 | HOLDS |
| 0.030 | 0.55 | 0.003 | 93 | 93 | 105 | 108 | 109 | 109 | x1.133 | HOLDS |

## Probe cells

| probe | none | local | codec | regen | chan | blind | codec/local | gate |
|---|---|---|---|---|---|---|---|---|
| probe_degraded_channel | 77 | 80 | 108 | 140 | 96 | 96 | x1.350 | HOLDS |
| probe_cliff | 63 | 63 | 71 | 70 | 74 | 74 | x1.122 | HOLDS |
| probe_fast_propagation | 72 | 75 | 126 | 138 | 122 | 122 | x1.676 | HOLDS |
| probe_weak_inflammaging | 82 | 79 | 131 | 139 | 129 | 129 | x1.658 | HOLDS |
| probe_coarse_code | 79 | 85 | 129 | 133 | 130 | 130 | x1.525 | HOLDS |
| probe_heavy_corruption | 50 | 49 | 108 | 114 | 102 | 102 | x2.225 | HOLDS |

## Verdicts

- **gate_robustness**: the Level-3 gate (codec/local >= 1.03) holds in 24/24 cells (100%) across the physics landscape; mean codec/local x1.548
- **regen**: regeneration rejuvenates in 23/24 cells (mean x1.65)
- **gating_pays**: verification-gated channel therapy beats blind boosting in 0/24 cells (mean x1.000)
- **worst_cell**: probe_cliff
- **best_cell**: probe_heavy_corruption

Codec architecture note: this sweep runs the FIXED codec (consensus-read
detection + per-cell archive writes) — the batched rewrite that repaired
two latent bugs (boundary destruction by cluster-mean writes; BP-smear
false-positive detection). Gate gains are therefore directly comparable
across cells but slightly stronger than the original exp8 single-regime
run (documented in FALSIFICATION.md).
