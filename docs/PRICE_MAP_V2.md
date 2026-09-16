# PRICE MAP V2 — the reader's honest current form

Re-issued by exp108-116 (ledger L90-L97): the walk-speed
arc. The deployed protocol's prices carried a WALK TAX
(the 0.8n-time-unit rebuild bathes the field in the wound
state — exp110) and a MU-SILENCE requirement on the middle
band that is binary in magnitude AND phase combination
(exp115-116). The oracle prices the ends; the dials pay
the middle; walk speed was hidden tax everywhere except
the geometry pair. (exp114: rho 0.63, references 0.73/0.81
on walk-taxed cells.)

| member | class v2 | deployed err | frozen cell | frozen err | speed buyback | mu requirement | v2 ratio |
|---|---|---|---|---|---|---|---|
| path | DEFAULT0 | 2.91 | (1, 0.015) | 2.04 | - | tolerant | - |
| path200 | DEFAULT0 | 2.38 | (1, 0.015) | 1.48 | - | tolerant | - |
| cycle | DEFAULT0 | 3.67 | (1, 0.015) | 2.66 | - | tolerant | - |
| small_world | DEFAULT0 | 4.23 | (1, 0.015) | 3.02 | - | tolerant | - |
| star | DEFAULT0 | 5.42 | (1, 0.015) | 5.71 | 2.0 | tolerant | 4.0202 |
| torus | MU0_SILENCE | 3.81 | (1, 0) | 5.54 | 4.0 | mandatory-silence | 4.8083 |
| torus_elong | MU0_SILENCE | 3.76 | (1, 0) | 5.47 | 4.0 | mandatory-silence | 5.7276 |
| random3 | MU0_SILENCE | 3.62 | (1, 0) | 5.16 | 4.0 | mandatory-silence | 7.5118 |
| random8 | MU0_SILENCE | 3.96 | (1, 0) | 5.28 | 4.0 | mandatory-silence | 2.8826 |
| scale_free | MU0_SILENCE | 3.59 | (1, 0) | 5.94 | 4.0 | mandatory-silence | 8.6209 |
| scale_free200 | MU0_SILENCE | 3.93 | (1, 0) | 5.91 | 4.0 | mandatory-silence | 13.1494 |
| tree | GAMMA0 | 5.35 | (16, 0.015) | 4.52 | 4.0 | tolerant | 6.2312 |
| grid2d | GAMMA0 | 4.99 | (16, 0.015) | 4.38 | 4.0 | tolerant | 4.174 |
| grid_elong | GAMMA0 | 5.58 | (16, 0.015) | 4.98 | 4.0 | tolerant | 5.1403 |
| ladder | GAMMA0 | 5.01 | (8, 0.015) | 3.98 | 4.0 | tolerant | 3.6168 |
| random6 | GAMMA0 | 5.54 | (8, 0.015) | 4.83 | 4.0 | tolerant | 2.0378 |
| barbell | GAMMA0 | 2.20 | (4, 0) | 3.77 | 4.0 | tolerant | 12.1007 |
| bipartite | GEOMETRY | 4.76 | (32, 0) | 4.47 | - | tolerant | 32.5 |
| complete | GEOMETRY | 5.42 | (32, 0) | 5.21 | - | tolerant | 25.0289 |

## The oracle's domain statement (exp114)

Spearman(v2, class-ordinal cost) = 0.63 on the honest
map (references 0.73 raw / 0.81 v2 on walk-taxed cells).
The boundary-to-volume ratio prices the ENDS — the cheap
band (v2 0.43-1.30) and the geometry pair (25.0-32.5,
domination without exception) — and does NOT price the
middle band (class-mean monotonicity REFUTED: MU0 7.12 >
GAMMA0 5.55).

## The calibration curve (exp111-112)

Walk speed (steps_per_cell 8 -> 0) buys back GAMMA,
never MU: 13/15 expensive members verify at a strictly
cheaper cell under the frozen walk (most at gamma/4; the
entire (4, 0) two-dial class at default gamma), the
torus trend INVERTS (+1.04 -> -1.03) and n=784 prices at
1.48 mV (3.3x cheaper, rate 1.0); grid2d is
protocol-robust to +/-0.02; bipartite/complete refuse
every descent rung (coupling geometry, not walk tax).

## The mu-silence law (exp115-116)

The middle band requires TOTAL mu silence — the 0.01
rung buys nothing (0/6), and either phase (window or
settle) carrying mu 0.015 fails identity 6/6. The cheap
band and the geometry pair are mu-tolerant.

## Bench prediction (deposited, testable)

REBUILD SPEED PREDICTS IDENTITY FIDELITY — faster
regeneration preserves pattern memory better (exp110's
intact-drift ladder 2.47 -> 5.32 with n; the frozen walk
collapses the trend). Candidate bench gate at the next
Stage-5 protocol revision.
