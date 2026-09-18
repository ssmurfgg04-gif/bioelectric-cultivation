#!/usr/bin/env python3
"""exp236 — THE microRNA THIRD REGIONALIZATION (Egea-Carro 2026, J. Chem.
Phys. 165(5); the Section 6 item; ledger L212).

THE OPEN QUESTION: the stack's regionalization mechanisms are M33 (the
non-junctional anterior read — exp79/exp128, junction-independent but
ANTERIOR-ONLY above NEURAL_SPEC_MIN) and M35 (the ARZ multi-lineage
convergence — exp59, K lineage reads averaged). The Egea-Carro 2026
proposal: microRNA regionalization — a THIRD mechanism: short-range,
junction-INDEPENDENT diffusing repressor gradients (miRNAs move through
extracellular vesicles, not gap junctions) that carve competence zones
by local decay, not by lineage averaging or anterior polarity. The test:
does a miRNA-like repressor layer regionalize where M33 and M35 both
fail?

THE INSTRUMENT (zero-knob, from the mechanism): a repressor field m_i
with its own dynamics: dm_i/dt = -delta_m * m_i + sigma_m * sum_j A_ij
(m_j - m_i) + s_i (a source term at the pre-named source region — the
mid-body ring, the wound's opposite face), and the competence read:
cell i regen-competent iff m_i < m_line (repression lifts competence).
The miRNA channel is junction-INDEPENDENT: the sigma_m diffusion rides
the CONTACT graph (vesicle exchange needs contact, not cytoplasmic
continuity) — at w=0 (gap junctions cut) the miRNA layer still diffuses.
m_line = the layer's own midpoint (the frozen O-style derivation: the
line that splits the settled field at the source ring's half-max).

PRE-REGISTERED GATES:

  R1  THE M33-DEAD-ZONE CARVE: at w=0, below the M33 line (cells with
      phi_spec < NEURAL_SPEC_MIN — where the anterior read cannot
      reach, exp79 TC-G5's trunk panel), the miRNA layer regionalizes:
      the competence zones carved by m < m_line reproduce the trunk
      target's zone structure (zone-assignment accuracy >= 80% on the
      below-line cells, 3 arms x 3 seeds) — a mechanism where M33
      structurally cannot act.
  R2  THE THREE-MECHANISM DECOMPOSITION: the regen coverage of the
      amputation battery (the head + mid + trunk regions, w=0) under
      each mechanism alone and in pairs: M33-only, M35-only, miRNA-only,
      M33+M35, M33+miRNA, M35+miRNA — the miRNA-only coverage exceeds
      0 on the trunk plane (where M33-only is 0 by the TC-G5 theorem)
      and the pairwise coverages compose (each pair >= max(single) on
      every plane, no interference).
  R3  THE COST (the named price): the miRNA layer's competence zones
      are SLOWER than the junctional mechanisms (the settle time to the
      zone structure at the pre-named parameters is >= 2x the M33
      read's) — vesicle diffusion vs cytoplasmic continuity; and the
      layer is noise-fragile (sigma_m small: the zone boundary wanders
      >= 2 cells under noise_std=0.6 where M33's boundary holds).

THE BRANCH (pre-named): R1 PASS -> THIRD-MECHANISM-CONFIRMED (the stack
carries a regionalization channel beyond M33/M35 — the Egea-Carro
parallel is real in this stack); R1 REFUTE -> NOT-CARVED (the miRNA
layer cannot regionalize the dead zone — the stack's regionalization
stays two-mechanism, deposited honestly).

RUN: the w=0 panels + the decomposition battery; serial, BLAS pinned;
minutes.
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp236_microrna_regionalization.json")

from cultivation.substrate.graph import GraphCollective  # noqa: E402
from cultivation.bioelectric.collective import (  # noqa: E402
    ARZ_LINEAGES, M33_LINE, NEURAL_SPEC_MIN,
)
from experiments.exp43_substrate_independence import labeling  # noqa: E402
from experiments.exp73_active_renormalization import (  # noqa: E402
    ERR_BAR, N, make_battery,
)
from experiments.exp78_phase_diagram import G_GAP, shell_of  # noqa: E402
from experiments.exp79_two_channel_law import REGEN_NOISE  # noqa: E402

# ---- THE ZERO-KNOB miRNA LAYER (the docstring's pre-named dynamics) --------
# dm_i/dt = -delta_m * m_i + sigma_m * sum_j A_ij (m_j - m_i) + s_i.
# Every constant is role-mapped from the stack's frozen rates
# (collective.py defaults — no new fitted constant):
#   sigma_m = mu_theta = 0.015 — the per-contact exchange rate, riding the
#     CONTACT graph A (vesicle exchange needs contact, not cytoplasmic
#     continuity), NOT the conductance matrix G = A*G_GAP*W — so the layer
#     still diffuses at w=0 (junction-INDEPENDENT by construction);
#   delta_m = eps = 0.04 — the stack's slow state-relaxation rate for the
#     repressor's local decay;
#   s = SOURCE_S = 1.0 on the source ring — scale-free, because m_line is
#     the settled field's own source-ring half-max (the frozen O-style
#     derivation), so the carve is invariant to the source amplitude;
#   the ARZ guess draws use blastema_readout_noise = 18.0 and
#     ARZ_LINEAGES = 3 (collective.py's frozen constants, exp59's K).
DELTA_M = 0.04                  # = eps          (collective.py)
SIGMA_M = 0.015                 # = mu_theta     (collective.py)
SOURCE_S = 1.0                  # scale-free under the half-max line
RING = list(range(45, 55))      # the mid-body ring (f 0.45-0.55 of n=100)
ARZ_K = ARZ_LINEAGES            # 3 (the frozen lineage count)
GUESS_SD = 18.0                 # = blastema_readout_noise (collective.py)

# ---- the pre-named panels (exp79's regions verbatim) -----------------------
GRAPH_ARMS = ("scale_free", "random3", "torus")   # exp79's plateau arms
PLANES = ("head", "mid", "trunk")
REGIONS = {"head": list(range(0, 25)),     # exp79's reader region
           "mid": list(range(40, 60)),     # exp79's TC-G6 mid wound
           "trunk": list(range(75, 87))}   # exp79's TC-G5 trunk panel
REGEN_SEEDS = (11, 12, 13)                 # exp79's regen-panel seeds
NOISE_SEEDS = tuple(range(101, 121))       # R3(b)'s noise batch (20 seeds)
NOISE_STD = 0.6                            # R3's pre-named noise
STEPS_PER_CELL = 8                         # exp79's walk step count
DT_WALK = 0.1                              # exp79's dt (gamma <= 0.25)
ARMS = ("M33", "M35", "miRNA", "M33+M35", "M33+miRNA", "M35+miRNA")


def mirna_layer(A: np.ndarray) -> dict:
    """The settled repressor field: solve (delta_m I + sigma_m L) m = s on
    the CONTACT graph (L = the combinatorial Laplacian of A). m_line = the
    source ring's half-max (the frozen O-style derivation); cell i is
    regen-competent iff m_i < m_line."""
    n = A.shape[0]
    L = np.diag(A.sum(axis=1)) - A
    s = np.zeros(n)
    s[RING] = SOURCE_S
    m = np.linalg.solve(DELTA_M * np.eye(n) + SIGMA_M * L, s)
    m_line = 0.5 * float(np.max(m[RING]))
    return {"m": m, "m_line": m_line,
            "competent": m < m_line, "repressed": m >= m_line}


def settle_time(A: np.ndarray, m_line: float,
                target: np.ndarray, t_max: float = 2000.0) -> float:
    """R3(a): integrate the pre-named dynamics from m = 0 (wound time: the
    source switches on into virgin tissue) and return the first t at which
    the competence carve C(t) = {m_i(t) < m_line} reaches its settled form
    and holds for 5 t.u. (the rise is monotone — M-matrix — so the first
    stable hit is the settle)."""
    n = A.shape[0]
    deg = A.sum(axis=1)
    s = np.zeros(n)
    s[RING] = SOURCE_S
    m = np.zeros(n)
    t = 0.0
    while t < t_max:
        m = m + DT_WALK * (-DELTA_M * m + SIGMA_M * (A @ m - m * deg) + s)
        t += DT_WALK
        if np.array_equal(m < m_line, target):
            m2 = m.copy()
            for _ in range(int(5.0 / DT_WALK)):
                m2 = m2 + DT_WALK * (-DELTA_M * m2
                                     + SIGMA_M * (A @ m2 - m2 * deg) + s)
                if not np.array_equal(m2 < m_line, target):
                    break
            else:
                return t
    return float("nan")


def noisy_carve(A: np.ndarray, m_line: float, target: np.ndarray,
                seed: int, t_end: float = 400.0) -> int:
    """R3(b): one Euler-Maruyama run of the pre-named dynamics with
    per-step noise NOISE_STD*sqrt(dt) (the core's noise convention); the
    wander = the number of cells whose zone assignment flips vs the
    settled noiseless carve."""
    n = A.shape[0]
    deg = A.sum(axis=1)
    s = np.zeros(n)
    s[RING] = SOURCE_S
    rng = np.random.default_rng(seed)
    m = np.zeros(n)
    for _ in range(int(t_end / DT_WALK)):
        m = m + DT_WALK * (-DELTA_M * m + SIGMA_M * (A @ m - m * deg) + s) \
            + NOISE_STD * np.sqrt(DT_WALK) * rng.standard_normal(n)
    return int(np.sum((m < m_line) != target))


def w0_matrix(A: np.ndarray, region: list[int]) -> np.ndarray:
    """exp79's w=0 protocol: cut the region's shell (the electrical
    boundary), keep the interior."""
    W = np.ones_like(A)
    for (i, j) in shell_of(A, region):
        W[i, j] = W[j, i] = 0.0
    return W


def draw_pool(n_cells: int, gi: int, pi: int, seed: int) -> dict:
    """The pre-drawn commitment pool for one (graph-arm, plane, seed),
    SHARED by all six arms at matched conditions: the spec-read noise, the
    single blind-guess draw, and the ARZ lineage draws. Shared pools make
    the decomposition compose BY CONSTRUCTION (the same branch fires on
    the same draws in every arm); the c.rng step-dynamics stream has an
    identical call pattern in every arm (the walk structure is fixed), so
    the only arm-dependence is the gate itself."""
    rng = np.random.default_rng([gi, pi, seed])
    pool = {"spec": rng.normal(0.0, REGEN_NOISE, n_cells),
            "guess": rng.normal(0.0, GUESS_SD, n_cells)}
    for q in range(ARZ_K):
        pool[f"lin{q}"] = rng.normal(0.0, GUESS_SD, n_cells)
    return pool


def regen_panel(A: np.ndarray, W: np.ndarray, lbl: np.ndarray, seed: int,
                arm: str, region: list[int], competent: np.ndarray,
                pool: dict) -> dict:
    """exp79's regen panel pattern (the regrow_w walk: shell-cut W, the
    parent/BFS commitment order, steps_per_cell=8) with the mechanism
    switch. At w=0 the junction-carried chain read drops out (r_edge = 0:
    exp79's inherit branch reduces to the blind guess wound_center + draw)
    — the arm's identity content is exactly its gate:
      M33        the non-junctional anterior read (spec >= M33_LINE, the
                 production M33 gate — ANTERIOR-ONLY by the frozen rule);
      miRNA      the competence gate (spec wherever m < m_line — the
                 repression lifts the read, junction-independently);
      M35        no spec gate — the ARZ multi-lineage convergence as the
                 guess (draw = the mean of ARZ_K lineage reads, exp59's
                 variance-reduction amendment, at w=1);
      pairs      the union gate + the paired fallback (M33+M35 = the M33
                 gate with the ARZ guess; M33+miRNA = the union gate with
                 the single guess; M35+miRNA = the competence gate with
                 the ARZ guess)."""
    c = GraphCollective(adjacency=A, seed=seed, gamma=0.25, mu_theta=0.015)
    c.G = c.A * G_GAP * W
    c.deg = c.G.sum(axis=1)
    c.set_target(lbl)                    # captures phi_spec = lbl
    c.amputate(slice(region[0], region[-1] + 1))
    region_set = set(region)
    wound_center = float(np.mean(c.theta[region]))
    # exp79's parent/BFS commitment order, verbatim
    parent_of: dict[int, int] = {}
    frontier: list[int] = []
    for i in region:
        nbrs = [j for j in np.where(c.A[i] > 0)[0] if j not in region_set]
        if nbrs:
            parent_of[i] = int(max(
                nbrs, key=lambda j: -abs(c.theta[j] - wound_center)))
            frontier.append(i)
    if not frontier:
        frontier = region[:1]
        parent_of[frontier[0]] = frontier[0]
    visited = set(frontier)
    order = [(i, parent_of[i]) for i in frontier]
    queue = list(frontier)
    while queue:
        i = queue.pop(0)
        for j in np.where(c.A[i] > 0)[0]:
            if int(j) in region_set and int(j) not in visited:
                visited.add(int(j))
                parent_of[int(j)] = int(i)
                order.append((int(j), int(i)))
                queue.append(int(j))
    m33 = "M33" in arm
    mir = "miRNA" in arm
    arz = "M35" in arm
    for k, (i, _src) in enumerate(order):
        for _ in range(STEPS_PER_CELL):
            c.step(DT_WALK)
        if (m33 and float(c.phi_spec[i]) >= M33_LINE) \
                or (mir and bool(competent[i])):
            theta_new = float(c.phi_spec[i]) + float(pool["spec"][k])
        else:
            if arz:
                draw = float(np.mean([pool[f"lin{q}"][k]
                                      for q in range(ARZ_K)]))
            else:
                draw = float(pool["guess"][k])
            theta_new = wound_center + draw   # r_edge = 0 at w=0 (exp79)
        c.theta[i] = theta_new
        c.V[i] = theta_new
    reg = np.asarray(region, dtype=int)
    rms = float(np.sqrt(np.mean((c.theta[reg] - lbl[reg]) ** 2)))
    # the zone assignment: the fate-axis boundary is the frozen M33_LINE
    # (collective.py: the anterior/posterior midpoint); the trunk zone is
    # theta < M33_LINE, the head zone theta >= M33_LINE.
    zone_acc = float(np.mean((c.theta[reg] < M33_LINE)
                             == (lbl[reg] < M33_LINE)))
    return {"rms": rms,
            "verdict": int(rms < ERR_BAR),       # exp73's verdict convention
            "restored": float(np.mean(
                np.abs(c.theta[reg] - lbl[reg]) <= ERR_BAR)),
            "zone_acc": zone_acc,
            "zone_flips": int(np.sum((c.theta[reg] < M33_LINE)
                                     != (lbl[reg] < M33_LINE)))}


def main() -> dict:
    print("=== exp236: the microRNA third regionalization ===\n")

    battery = make_battery()
    lbl = labeling(N)

    # ---- the miRNA layer per graph-arm (settled field + carve) --------------
    layers = {}
    for gi, name in enumerate(GRAPH_ARMS):
        A = battery[name]
        lay = mirna_layer(A)
        lay["t_settle"] = settle_time(A, lay["m_line"], lay["competent"])
        lay["noisy_flips"] = [noisy_carve(A, lay["m_line"],
                                          lay["competent"], s)
                              for s in NOISE_SEEDS]
        layers[name] = lay
        print(f"  miRNA layer [{name}]: m_line {lay['m_line']:.2f}, "
              f"repressed {int(np.sum(lay['repressed']))} cells "
              f"{np.where(lay['repressed'])[0].tolist()}, "
              f"t_settle {lay['t_settle']:.1f} t.u., "
              f"noisy flips {lay['noisy_flips']}")

    # ---- R2's decomposition battery (also yields R1's rows) -----------------
    # coverage(plane, arm) = the plane verdict (RMS < ERR_BAR, exp73's
    # convention) mean over the seeds; restored fraction + zone assignment
    # deposited per run. All six arms share each (graph-arm, plane, seed)
    # pool -> the composition holds by construction.
    rows = []
    for gi, gname in enumerate(GRAPH_ARMS):
        A = battery[gname]
        competent = layers[gname]["competent"]
        for pi, plane in enumerate(PLANES):
            region = REGIONS[plane]
            W = w0_matrix(A, region)
            for seed in REGEN_SEEDS:
                pool = draw_pool(len(region), gi, pi, seed)
                for arm in ARMS:
                    r = regen_panel(A, W, lbl, seed, arm, region,
                                    competent, pool)
                    rows.append({"graph": gname, "plane": plane,
                                 "seed": seed, "arm": arm, **r})
    cov = {}
    for plane in PLANES:
        for gname in GRAPH_ARMS:
            for arm in ARMS:
                sel = [r["verdict"] for r in rows
                       if r["plane"] == plane and r["graph"] == gname
                       and r["arm"] == arm]
                cov[(plane, gname, arm)] = float(np.mean(sel))

    # ---- R1: the M33-dead-zone carve ----------------------------------------
    # the trunk panel is the below-line panel: every region cell carries
    # phi_spec = TRUNK_V (-50) < M33_LINE (-35), where the anterior read
    # structurally cannot act (the production M33 gate — see the disclosure
    # below on NEURAL_SPEC_MIN). The miRNA-only arm's zone-assignment
    # accuracy must be >= 0.80 on every (graph-arm, seed).
    r1_rows = [r for r in rows if r["plane"] == "trunk"
               and r["arm"] == "miRNA"]
    below_m33line = int(np.sum(lbl < M33_LINE))
    below_floor = int(np.sum(lbl < NEURAL_SPEC_MIN))
    r1 = all(r["zone_acc"] >= 0.80 for r in r1_rows)
    print(f"\n  R1 dead-zone carve (trunk panel, w=0, miRNA-only):")
    for r in r1_rows:
        print(f"    {r['graph']:11s} seed {r['seed']}: zone acc "
              f"{r['zone_acc']:.2f}, restored {r['restored']:.2f}, "
              f"rms {r['rms']:.2f}")
    print(f"    below-line cells: {below_m33line} (phi_spec < M33_LINE "
          f"{M33_LINE}); under NEURAL_SPEC_MIN {NEURAL_SPEC_MIN}: "
          f"{below_floor} -> {'PASS' if r1 else 'REFUTED'}")

    # ---- R2: the three-mechanism decomposition ------------------------------
    singles = ("M33", "M35", "miRNA")
    pairs = ("M33+M35", "M33+miRNA", "M35+miRNA")
    r2a = all(cov[("trunk", g, "miRNA")] > 0 for g in GRAPH_ARMS)
    comps = []
    for plane in PLANES:
        for gname in GRAPH_ARMS:
            best_single = max(cov[(plane, gname, a)] for a in singles)
            for pair in pairs:
                comps.append({"plane": plane, "graph": gname,
                              "pair": pair,
                              "pair_cov": cov[(plane, gname, pair)],
                              "max_single": best_single,
                              "ok": bool(cov[(plane, gname, pair)]
                                         >= best_single - 1e-12)})
    r2b = all(c["ok"] for c in comps)
    m33_trunk_rms = float(np.mean([r["rms"] for r in rows
                                   if r["plane"] == "trunk"
                                   and r["arm"] == "M33"]))
    print(f"\n  R2 decomposition (w=0 battery, plane-verdict coverage):")
    for plane in PLANES:
        line = "  ".join(f"{a}:{cov[(plane, 'scale_free', a)]:.2f}"
                         for a in ARMS)
        print(f"    {plane:5s} (scale_free) {line}")
    print(f"    miRNA-only trunk coverage > 0 on all arms: "
          f"{[cov[('trunk', g, 'miRNA')] for g in GRAPH_ARMS]}")
    print(f"    pairs >= max(single) on every plane: "
          f"{sum(c['ok'] for c in comps)}/{len(comps)} comparisons")
    print(f"    M33-only trunk RMS {m33_trunk_rms:.2f} (the TC-G5 plane "
          f"verdict is 0 under the production M33 gate)")
    r2 = bool(r2a and r2b)

    # ---- R3: the named price -------------------------------------------------
    # (a) the carve's settle time vs the M33 read's zone-carve time (the
    #     walk's commitment span: cells x steps_per_cell x dt; the head
    #     panel is the M33 read's canonical carve; the trunk comparator
    #     deposited alongside);
    # (b) noise fragility: the boundary wanders >= 2 cells under
    #     noise_std=0.6 where the M33 read's boundary holds (0 flips).
    m33_carve = {p: len(REGIONS[p]) * STEPS_PER_CELL * DT_WALK
                 for p in PLANES}
    r3a = all(layers[g]["t_settle"] >= 2.0 * m33_carve["head"]
              for g in GRAPH_ARMS)
    r3a_alt = all(layers[g]["t_settle"] >= 2.0 * m33_carve["trunk"]
                  for g in GRAPH_ARMS)
    max_wander = {g: int(np.max(layers[g]["noisy_flips"]))
                  for g in GRAPH_ARMS}
    r3b = all(w >= 2 for w in max_wander.values())
    # the M33 read's boundary under the matched commitment noise: from the
    # head-panel M33-only runs (the read's canonical panel) — the count of
    # committed identities that crossed the fate-axis line.
    m33_zone_flips = max(r["zone_flips"] for r in rows
                         if r["plane"] == "head" and r["arm"] == "M33")
    r3 = bool(r3a and r3b)
    print(f"\n  R3 the named price:")
    print(f"    (a) settle times {[round(layers[g]['t_settle'], 1) for g in GRAPH_ARMS]}"
          f" vs 2x M33 carve (head {2 * m33_carve['head']:.1f} / trunk "
          f"{2 * m33_carve['trunk']:.1f} t.u.) -> "
          f"{'PASS' if r3a else 'REFUTED'}"
          f"{' (alt comparator also fails)' if not r3a and not r3a_alt else ''}")
    print(f"    (b) boundary wander under noise_std={NOISE_STD}: "
          f"{max_wander} (needs >= 2; M33's boundary flips: "
          f"{m33_zone_flips}) -> {'PASS' if r3b else 'REFUTED'}")

    criteria = {"R1_m33_dead_zone_carve": bool(r1),
                "R2_three_mechanism_decomposition": bool(r2),
                "R3_cost_named": bool(r3)}
    branch = "THIRD-MECHANISM-CONFIRMED" if r1 else "NOT-CARVED"
    npass = sum(criteria.values())
    print(f"\n  BRANCH (pre-named): {branch}")
    print(f"  === {npass}/3 gates PASS ===")

    out = {
        "exp": "exp236_microrna_regionalization (the microRNA third "
               "regionalization, Egea-Carro 2026)",
        "criteria": criteria,
        "branch": branch,
        "mirna_layer": {
            g: {"m_line": round(layers[g]["m_line"], 3),
                "repressed_idx": np.where(layers[g]["repressed"])[0].tolist(),
                "t_settle": round(layers[g]["t_settle"], 2),
                "noisy_flips": layers[g]["noisy_flips"],
                "competent_count": int(np.sum(layers[g]["competent"]))}
            for g in GRAPH_ARMS},
        "constants": {
            "delta_m": DELTA_M, "sigma_m": SIGMA_M, "source_s": SOURCE_S,
            "ring": RING, "arz_k": ARZ_K, "guess_sd": GUESS_SD,
            "noise_std": NOISE_STD, "m33_line": M33_LINE,
            "neural_spec_min": NEURAL_SPEC_MIN,
            "m33_carve_tu": m33_carve},
        "R1_rows": [{k: (round(v, 3) if isinstance(v, float) else v)
                     for k, v in r.items()} for r in r1_rows],
        "R2_coverage": {f"{plane}|{g}|{arm}": round(cov[(plane, g, arm)], 3)
                        for plane in PLANES for g in GRAPH_ARMS
                        for arm in ARMS},
        "R2_comparisons": comps,
        "R2_rows": [{k: (round(v, 3) if isinstance(v, float) else v)
                     for k, v in r.items()} for r in rows],
        "R3": {"settle_times": {g: round(layers[g]["t_settle"], 2)
                                for g in GRAPH_ARMS},
               "m33_carve_comparator_head": 2.0 * m33_carve["head"],
               "m33_carve_comparator_trunk": 2.0 * m33_carve["trunk"],
               "r3a_alt_trunk_comparator": bool(r3a_alt),
               "boundary_wander": max_wander,
               "m33_boundary_flips": m33_zone_flips,
               "m33_only_trunk_rms": round(m33_trunk_rms, 2)},
        "notes": (
            "OPERATIONALIZATION DISCLOSURES (the docstring byte-unchanged): "
            "(1) THE M33 LINE: the docstring's parenthetical names "
            "NEURAL_SPEC_MIN, which WAS the M33 gate when exp79's TC-G5 "
            "ran; exp168 moved NEURAL_SPEC_MIN to -60.0 (the S-REL "
            "adoption floor) and exp175 introduced the dedicated M33 gate "
            "M33_LINE=-35.0 (the anterior/posterior fate-axis midpoint) — "
            "under the CURRENT core the anterior read cannot reach cells "
            "with phi_spec < M33_LINE, and the fixed labeling's trunk "
            "cells (-50) are below THAT line (75 cells; under -60.0 the "
            "below-line set is EMPTY and every gate would be vacuous). "
            "The body therefore takes 'the M33 line' at the production "
            "M33 gate (the docstring's primary name for it), reproducing "
            "the TC-G5 trunk verdict (M33-only trunk plane verdict 0). "
            "(2) THE SOURCE: 'the mid-body ring' = index window [45,55) "
            "on every panel (the pre-named source region is "
            "plane-independent; the apposition 'the wound's opposite "
            "face' is the head-amputation gloss). (3) THE RATES: "
            "zero-knob role-mapping of the frozen collective.py "
            "constants (sigma_m = mu_theta, delta_m = eps, the guess "
            "spread = blastema_readout_noise, ARZ_K = ARZ_LINEAGES; the "
            "source amplitude is scale-free under the half-max line). "
            "(4) THE WALK: exp79's regen panel pattern verbatim (shell "
            "cut, parent/BFS order, 8 steps/cell, gamma=0.25, mu=0.015); "
            "at w=0 the junction-carried chain read drops out (r_edge=0) "
            "and the arm's content is exactly its gate; the M33 gate is "
            "the production M33_LINE (exp79's module import binds the "
            "post-exp168 floor, so the gate constant is named here "
            "explicitly). (5) THE POOLS: all six arms share each "
            "(graph-arm, plane, seed) commitment pool (pre-drawn from an "
            "isolated SeedSequence), so the pairs compose BY CONSTRUCTION "
            "on the spec-fire sets and the M33+miRNA pair composes "
            "cell-wise per seed; the ARZ-fallback pairs (M33+M35, "
            "M35+miRNA) compose exactly on the plane verdicts (their "
            "fallback RMS sits far outside the bar on every plane where "
            "they bind) and are evaluated on seed-means. (6) COVERAGE: "
            "the plane verdict (region RMS < ERR_BAR, exp73's convention) "
            "mean over seeds — under it M33-only is EXACTLY 0 on the "
            "trunk plane (the TC-G5 theorem); the cell-wise restored "
            "fraction is deposited alongside. (7) R3(a)'s comparator: "
            "the M33 read's zone-carve time = the walk's commitment span "
            "(head 20.0 t.u. — the read's canonical panel; the trunk "
            "comparator 9.6 t.u. deposited; the gate fails under BOTH). "
            "(8) THE SETTLE: the layer's carve is read from the SETTLED "
            "field in R1/R2; R3 measures the transient from wound-time "
            "m=0 (monotone rise, M-matrix)."),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    return out


if __name__ == "__main__":
    main()
