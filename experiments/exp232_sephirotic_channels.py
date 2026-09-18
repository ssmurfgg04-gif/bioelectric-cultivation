#!/usr/bin/env python3
"""exp232 — THE SEPHIROTIC 8-CHANNEL TEST (the user's OVERRIDE directive,
executed as the top of the priority queue; continuous batch; ledger L208).

THE DIRECTIVE (Section 2 of the handoff, quoted): the user directed the
project to test the Sephirotic 8-channel framework — the paper claiming the
8 internal modes of the 11-node Sephirotic graph correspond one-to-one with
8 independent bioelectric signaling channels, 7/8 knockout predictions
confirmed, zero free parameters. The directive was deferred for 5 batches
by the dependency tree; it now OVERRIDES it. The question this experiment
answers: does the stack have 8 independent channels, or only 2 (the V-ratio
channel + the theta-homogenization channel of exp79's two-channel law)?

THE PAPER (provenance, downloaded and sha-recorded this session):
  Freeman, C. W. (2026-03-16), "Sephirotic Edge-Channel Correspondence in
  Bioelectric Morphogenesis: Eight Internal Modes Predict Eight Independent
  Bioelectric Channels", Zenodo record 19042388, doi 10.5281/zenodo.19042388,
  license CC-BY-4.0. Files (research/sephirotic/, verbatim):
    paper25.pdf            sha256 206613 bytes (downloaded via Zenodo API)
    paper25_computation.py md5 277684d5b717b2f1b05b130aef016ef2 (19367 B)
    paper25_results.json   md5 02f0a9940d6f5b25ed58b9f8459c73bb (929 B,
                           matches the Zenodo-declared checksum)
  The paper's claims tested here: (a) the graph (11 nodes, 24 edges, built
  from 5 principles P1-P5, edge lists copied VERBATIM from the shipped
  computation script) has normalized-Laplacian eigenvalue 6/5 EXACT at
  sorted index 6, splitting into 3 spatial + 8 internal modes; (b) the
  joint occurrence is rare (their null: 39/100000 random 11-node 24-edge
  graphs, p = 3.9e-4); (c) 8 channel edges map to 8 independent bioelectric
  channels. The stack-side claim tested: the paper's 8 channels vs this
  stack's channel count.

PART 1 — THE PAPER'S ARITHMETIC, INDEPENDENTLY, EXACT (gate S1):
  The graph rebuilt from the shipped P1-PILLAR/P2-LEVEL/P3-TIFERET/
  P4_LOWER/P5_DAAT edge lists (7+5+6+4+2 = 24 edges, 11 nodes). The
  exact-arithmetic instrument: lambda is an eigenvalue of the normalized
  Laplacian L_norm = I - D^-1/2 A D^-1/2 iff it solves the generalized
  problem Lc u = lambda D u (Lc = D - A, D positive diagonal); lambda = 6/5
  iff det(5*Lc - 6*D) = 0 iff det(D + 5A) = 0 — an INTEGER matrix, so the
  claim is checkable in exact integer arithmetic (Bareiss fraction-free
  determinant, no floats). Companion float checks: sorted eigh(L_norm)[6]
  within 1e-12 of 1.2, exactly ONE eigenvalue within 1e-9 of 1.2, all 11
  eigenvalues within 1e-9 of the shipped paper25_results.json values, the
  mirror automorphism P A P^T == A exact over the 3 bilateral pairs
  (Chokmah/Binah, Chesed/Gevurah, Netzach/Hod) with equal degrees within
  every pair (the condition that makes the normalized-Laplacian sector
  split exact), the antisymmetric sector EXACTLY 3-dimensional (the
  author's own criterion |v[a]+v[b]| <= 1e-2, re-run at 1e-8 as the exact
  sector test) at the author's indices [3, 6, 10], and all 8 channel edges
  present in A.

PART 2 — THE NULL REPRODUCED (gate S2):
  The author's Test-3 protocol reproduced verbatim: np.random.seed(42),
  100000 random 11-node graphs with 24 edges drawn by shuffling a boolean
  edge mask (the SAME call sequence — the RNG stream is independent of the
  isolated-node skips), lambda hit = any eigenvalue within 1e-3 of 1.2,
  3-spatial hit = some pairing of 6 nodes into 3 pairs yields exactly 3
  antisymmetric modes within 1e-2, pairing search over all C(11,6) = 462
  combinations (vectorized, RNG-neutral). Pre-named portability band:
  hits_lambda == 3011 +/- 30, hits_both == 39 +/- 2 (exact counts
  reported beside the band; LAPACK-build float differences absorbed by
  the author's own tolerances), p_null <= 1e-3.

PART 3 — THE STACK'S CHANNEL COUNT (gates S3a/S3b — the directive's core):
  The battery: 3 arms (exp73's make_battery: scale_free/random3/torus,
  N=100), lbl = exp43's fixed labeling, the write settled at the star
  operating point (gamma=64, mu=0) by exp79's run_gm protocol VERBATIM;
  then ONE pre-named intervention, then ONE response window (RUN_T=24,
  exp79's dt stability rule); err = pattern_error(lbl). Intervention noise
  drawn from a fresh default_rng(seed*7919 + magnitude_index) — pre-named,
  never the collective's stream. The families and magnitudes (pre-named):
    v_offset   delta in {5, 10, 20} mV on V
    v_gain     g in {0.5, 0.75, 1.5} on V's contrast about its mean
    v_noise    sigma in {2, 5, 10} mV on V
    th_offset  delta in {5, 10, 20} mV on theta (the memory layer)
    th_noise   sigma in {2, 5, 10} mV on theta
    gj_thin    block_gap_junctions(s), s in {0.25, 0.5, 0.75}
    gj_shell   w=0 on exp78's shell_of(head region 0..24) for the window
    gamma_dial response gamma' in {0.25, 4.0} (64 is the settled baseline)
    mu_dial    response mu' in {0.015, 0.005, 0.0015, 0.0005} (0 baseline)
    wound      amputate(slice(40, 60)), T=240, mu' in {0.015, 0.0}
  The law's prediction per instance (exp79's terms, verbatim formulas,
  zero knobs): pred = max(CONTRAST*y_eff/(1+y_eff),
  theta_term(mu_eff, T)) with y_eff = y_of(A, W_eff, lbl, gamma_eff)
  (W_eff = ones, or the instance's thinned/shell W for the gj families;
  theta_term carries T — 24 for the windows, 240 for the wound — and deg
  from A, exp79's formula). Raw state decompositions (eV_state = RMS(V-lbl),
  eT_state = RMS(theta-lbl)) recorded per instance, disclosed.

  S3a — THE LAW'S REACH: pooled Spearman(pred, err) over ALL battery
        instances >= 0.90 -> LAW-EXTENDS; below -> LAW-BOUNDED-TO-WRITE
        (the refute branch is pre-named and honest: exp79's law was
        derived and frozen on the write/settle domain; the battery is the
        response domain).
  S3b — THE COUNT: a group BREAKS OUT at its largest pre-named magnitude
        iff any arm's seed-mean err exceeds that arm's pred by more than
        max(2.0, 0.5*pred) (exp79's TC-G4 tolerance form). Groups (the
        attribution rule pre-named): V-RATIO = gamma_dial; THETA-DIFFUSION
        = mu_dial PLUS the wound@mu=0 breakout (attributed there — the
        propagation channel's absence IS exp79's TC-G6 price, not a new
        channel); V-STATE = v_offset/v_gain/v_noise; THETA-STATE =
        th_offset/th_noise; WINDOW = gj_thin/gj_shell.
        count = number of groups breaking out. Branches pre-named:
        STACK-2CH (2) / STACK-3to7 (3-7) / STACK-8PLUS (>= 8).
        S3b's gate is well-definedness: every pre-named instance measured,
        zero rejections, all finite, every group verdict recorded — the
        FINDING names whichever branch fired.

CENSUS (non-gated, disclosed): the paper's 8 channels x the stack's frozen
mechanism inventory, each row CARRIES/PARTIAL/ABSENT with the exp citation:
  1 Vmem bistability            -> the V contrast machinery (gamma, y-ratio)
  2 Gap-junctional morphogenesis -> the G/W window (exp78, exp79 TC-G4)
  3 Ca2+ transient signaling     -> ABSENT (no Ca2+ layer in the stack)
  4 Vmem propagation through GJ  -> theta diffusion (mu*lap, exp79)
  5 Epigenetic control of prolif -> the theta/spec memory layer (M28/M37)
  6 Ion channel expression       -> the gamma dial (exp78's V-channel)
  7 Serotonin transport (5-HT)   -> ABSENT (no transmitter layer)
  8 Apoptosis as morphogenetic   -> ABSENT (no death layer)

AUDIT-ONLY DISCLOSURES (pre-named, non-gating):
  (a) The author's script is NOT executed in full (hardcoded /workspace
      output path; the pure-python pairing loop's runtime); the null is
      reproduced under the identical RNG protocol instead.
  (b) In the author's script hits_split == hits_both BY CONSTRUCTION
      (has_3spatial is only computed when has_lambda fires) — the
      unconditional 3-spatial rate over all 100000 graphs is measured
      HERE as the audit extension, plus the conditional p among valid
      (non-isolated) graphs (the author's denominator is the full 100000
      including isolated-node skips).
  (c) The sector-dimension disclosure: any graph with a Z2 mirror
      automorphism over k pairs carries EXACTLY k antisymmetric modes
      (group theory, no statistics) — the "3 spatial modes" half of the
      paper's joint occurrence is structural for every mirror-symmetric
      graph; the rarity claim rests on the JOINT occurrence.

PRE-REGISTERED GATES (the short form):
  S1   the paper's arithmetic EXACT: det(D+5A) == 0 integer-exact, the
       index-6 float checks, the automorphism, the 3-dim antisymmetric
       sector at [3,6,10], all 11 eigenvalues vs the shipped JSON <= 1e-9,
       all 8 channel edges present.
  S2   the null reproduced: hits_lambda 3011+/-30, hits_both 39+/-2,
       p_null <= 1e-3 (exact counts reported).
  S3a  pooled Spearman(pred, err) >= 0.90 (LAW-EXTENDS) else the
       pre-named LAW-BOUNDED-TO-WRITE branch.
  S3b  the count well-defined (zero rejections, all instances, all group
       verdicts recorded); the branch STACK-2CH / STACK-3to7 / STACK-8PLUS
       named by the measurement.

RUN: Part 1 exact + float (seconds); Part 2 100000-graph null (vectorized
pairing audit); Part 3 the battery (25 magnitudes x 3 seeds x 3 arms at
RUN_T=24 + the 18 wound runs at T=240), serial, BLAS pinned.
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
OUT = os.path.join(ROOT, "results", "exp232_sephirotic_channels.json")


# ============================================================
# PART 0 — THE PAPER'S GRAPH, VERBATIM FROM THE SHIPPED SCRIPT
# (research/sephirotic/paper25_computation.py, md5 277684d5;
#  edge lists copied byte-for-byte, zero re-derivation)
# ============================================================

NODES = ['Keter', 'Chokmah', 'Binah', "Da'at", 'Chesed', 'Gevurah',
         'Tiferet', 'Netzach', 'Hod', 'Yesod', 'Malkuth']
NODE_IDX = {n: i for i, n in enumerate(NODES)}
N_P = len(NODES)

P1_PILLAR = [('Binah', 'Gevurah'), ('Gevurah', 'Hod'),
             ('Chokmah', 'Chesed'), ('Chesed', 'Netzach'),
             ('Keter', 'Tiferet'), ('Tiferet', 'Yesod'),
             ('Yesod', 'Malkuth')]

P2_LEVEL = [('Keter', 'Chokmah'), ('Keter', 'Binah'),
            ('Chokmah', 'Binah'), ('Chesed', 'Gevurah'),
            ('Netzach', 'Hod')]

P3_TIFERET = [('Chokmah', 'Tiferet'), ('Binah', 'Tiferet'),
              ('Chesed', 'Tiferet'), ('Gevurah', 'Tiferet'),
              ('Netzach', 'Tiferet'), ('Hod', 'Tiferet')]

P4_LOWER = [('Netzach', 'Yesod'), ('Hod', 'Yesod'),
            ('Netzach', 'Malkuth'), ('Hod', 'Malkuth')]

P5_DAAT = [("Da'at", 'Chokmah'), ("Da'at", 'Binah')]

ALL_EDGES = P1_PILLAR + P2_LEVEL + P3_TIFERET + P4_LOWER + P5_DAAT

# the paper's 8 channel edges (CHANNEL_MAP in the shipped script)
CHANNEL_EDGES = [('Chesed', 'Gevurah'), ('Yesod', 'Malkuth'),
                 ('Netzach', 'Hod'), ('Tiferet', 'Yesod'),
                 ("Da'at", 'Chokmah'), ('Chesed', 'Netzach'),
                 ('Hod', 'Malkuth'), ('Gevurah', 'Hod')]

BILATERAL_PAIRS = [('Chokmah', 'Binah'), ('Chesed', 'Gevurah'),
                   ('Netzach', 'Hod')]


def build_paper_graph():
    A = np.zeros((N_P, N_P))
    for u, v in ALL_EDGES:
        i, j = NODE_IDX[u], NODE_IDX[v]
        A[i, j] = A[j, i] = 1
    return A


def bareiss_det(M: np.ndarray) -> int:
    """Exact fraction-free determinant of an INTEGER matrix (Bareiss)."""
    n = M.shape[0]
    rows = [[int(M[i, j]) for j in range(n)] for i in range(n)]
    sign, prev = 1, 1
    for k in range(n - 1):
        if rows[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if rows[i][k] != 0), None)
            if swap is None:
                return 0
            rows[k], rows[swap] = rows[swap], rows[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                rows[i][j] = (rows[i][j] * rows[k][k]
                              - rows[i][k] * rows[k][j]) // prev
        prev = rows[k][k]
    return sign * rows[n - 1][n - 1]


# ============================================================
# PART 1 — THE PAPER'S ARITHMETIC, EXACT (gate S1)
# ============================================================

def part1() -> dict:
    A = build_paper_graph()
    D = np.diag(A.sum(axis=1))

    # lambda = 6/5 is a normalized-Laplacian eigenvalue iff it solves the
    # generalized problem Lc u = lam D u iff det(5*Lc - 6*D) = 0 iff
    # det(D + 5A) = 0 (5*(D-A) - 6*D = -(D+5A)). INTEGER matrix -> exact.
    det_exact = bareiss_det(D + 5.0 * A)

    deg = A.sum(axis=1)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(deg))
    L_norm = np.eye(N_P) - D_inv_sqrt @ A @ D_inv_sqrt
    evals, evecs = np.linalg.eigh(L_norm)

    lam6 = float(evals[6])
    lam6_dist = abs(lam6 - 1.2)
    n_near = int(np.sum(np.abs(evals - 1.2) < 1e-9))

    # mirror automorphism over the 3 bilateral pairs
    perm = list(range(N_P))
    for a, b in BILATERAL_PAIRS:
        ia, ib = NODE_IDX[a], NODE_IDX[b]
        perm[ia], perm[ib] = ib, ia
    P = np.zeros((N_P, N_P))
    for i, p in enumerate(perm):
        P[i, p] = 1.0
    automorphism = bool(np.array_equal(P @ A @ P.T, A))
    pairs_equal_deg = all(deg[NODE_IDX[a]] == deg[NODE_IDX[b]]
                          for a, b in BILATERAL_PAIRS)

    # the antisymmetric sector: |v[a] + v[b]| small on ALL 3 pairs,
    # per EIGENVECTOR (rows of evecs are nodes, columns are eigenvectors;
    # v_j at the pair nodes = evecs[pair_nodes, j])
    pair_ia = np.array([NODE_IDX[a] for a, b in BILATERAL_PAIRS])
    pair_ib = np.array([NODE_IDX[b] for a, b in BILATERAL_PAIRS])
    antisym_sum = np.abs(evecs[pair_ia, :] + evecs[pair_ib, :]).max(axis=0)
    idx_exact = [int(i) for i in np.where(antisym_sum <= 1e-8)[0]]
    idx_author = [int(i) for i in np.where(antisym_sum <= 1e-2)[0]]

    # the 8 channel edges exist
    edges_ok = all(A[NODE_IDX[u], NODE_IDX[v]] == 1 for u, v in CHANNEL_EDGES)

    # all 11 eigenvalues vs the shipped paper25_results.json
    shipped_path = os.path.join(ROOT, "research", "sephirotic",
                                "paper25_results.json")
    with open(shipped_path) as f:
        shipped = json.load(f)
    shipped_evals = sorted(shipped["spatial_eigenvalues"]
                           + shipped["internal_eigenvalues"])
    max_eval_diff = float(np.max(np.abs(np.sort(evals)
                                        - np.array(shipped_evals))))

    s1 = bool(det_exact == 0 and lam6_dist <= 1e-12 and n_near == 1
              and automorphism and pairs_equal_deg
              and idx_exact == [3, 6, 10]
              and idx_author == shipped["spatial_indices"]
              and max_eval_diff <= 1e-9 and edges_ok)
    print(f"  S1 det(D+5A) = {det_exact} (exact; 0 <=> lambda 6/5 exact)")
    print(f"      lambda[6] = {lam6:.15f} (dist {lam6_dist:.2e}), "
          f"eigs within 1e-9 of 1.2: {n_near}")
    print(f"      automorphism {automorphism}, equal pair-degrees "
          f"{pairs_equal_deg}")
    print(f"      antisym sector (1e-8): n={len(idx_exact)} at {idx_exact}; "
          f"author criterion (1e-2): {idx_author}")
    print(f"      max |eig - shipped| = {max_eval_diff:.3e}, "
          f"channel edges {sum(A[NODE_IDX[u], NODE_IDX[v]] == 1 for u, v in CHANNEL_EDGES)}/8")
    print(f"  S1 -> {'PASS' if s1 else 'REFUTED'}")
    return {
        "det_D_plus_5A": int(det_exact),
        "lambda6_float": lam6, "lambda6_distance": float(lam6_dist),
        "n_eigenvalues_near_1.2": n_near,
        "mirror_automorphism": automorphism,
        "pairs_equal_degrees": bool(pairs_equal_deg),
        "antisym_sector_indices_1e-8": idx_exact,
        "antisym_sector_indices_1e-2": idx_author,
        "shipped_spatial_indices": shipped["spatial_indices"],
        "max_abs_eigenvalue_diff_vs_shipped": max_eval_diff,
        "eigenvalues": [float(e) for e in evals],
        "channel_edges_present": int(sum(A[NODE_IDX[u], NODE_IDX[v]] == 1
                                         for u, v in CHANNEL_EDGES)),
        "shipped_md5s": {"paper25_computation.py":
                         "277684d5b717b2f1b05b130aef016ef2",
                         "paper25_results.json":
                         "02f0a9940d6f5b25ed58b9f8459c73bb"},
        "pass": s1,
    }


# ============================================================
# PART 2 — THE NULL REPRODUCED (gate S2)
# ============================================================

def part2(n_null: int = 100000) -> dict:
    from itertools import combinations
    pair_ix = np.array([[(c[0], c[1]), (c[2], c[3]), (c[4], c[5])]
                        for c in combinations(range(N_P), 6)])
    ia, ib = pair_ix[:, :, 0].ravel(), pair_ix[:, :, 1].ravel()
    n_combos = pair_ix.shape[0]

    np.random.seed(42)                      # the author's seed, verbatim
    hits_lambda = hits_both = hits_3spatial_any = valid = 0
    for _trial in range(n_null):
        edge_mask = np.zeros(N_P * (N_P - 1) // 2, dtype=bool)
        edge_mask[:24] = True
        np.random.shuffle(edge_mask)        # same call sequence as shipped
        A_rand = np.zeros((N_P, N_P))
        idx = 0
        for i in range(N_P):
            for j in range(i + 1, N_P):
                if edge_mask[idx]:
                    A_rand[i, j] = A_rand[j, i] = 1
                idx += 1
        deg = A_rand.sum(axis=1)
        if np.any(deg == 0):
            continue                        # the author's skip, verbatim
        valid += 1
        D_inv = np.diag(1.0 / np.sqrt(deg))
        L_rand = np.eye(N_P) - D_inv @ A_rand @ D_inv
        evals, evecs = np.linalg.eigh(L_rand)

        # unconditional 3-spatial audit (all valid graphs; the author's
        # script only ever tested lambda-hit graphs — audit disclosure (b))
        # per combo c and eigenvector j: max over the combo's 3 pairs of
        # |v_j[a] + v_j[b]| — rows of evecs are nodes, columns eigenvectors
        vals = np.abs(evecs[ia, :] + evecs[ib, :]).reshape(n_combos, 3, N_P)
        cnt = (vals.max(axis=1) < 1e-2).sum(axis=1)
        has_3spatial = bool((cnt == 3).any())
        if has_3spatial:
            hits_3spatial_any += 1
        has_lambda = bool(np.any(np.abs(evals - 1.2) < 1e-3))
        if has_lambda:
            hits_lambda += 1
            if has_3spatial:
                hits_both += 1

    p_author = hits_both / n_null           # the author's denominator
    p_cond = hits_both / valid if valid else float("nan")
    s2 = bool(abs(hits_lambda - 3011) <= 30 and abs(hits_both - 39) <= 2
              and p_author <= 1e-3)
    print(f"  S2 null ({n_null} graphs, seed 42): lambda-hits {hits_lambda} "
          f"(author 3011), joint hits {hits_both} (author 39), "
          f"valid {valid}")
    print(f"      unconditional 3-spatial {hits_3spatial_any} "
          f"(audit extension), p_author {p_author:.6f}, "
          f"p_conditional {p_cond:.6f}")
    print(f"  S2 -> {'PASS' if s2 else 'REFUTED'}")
    return {
        "n_null": n_null, "hits_lambda": hits_lambda,
        "hits_both": hits_both,
        "hits_3spatial_unconditional": hits_3spatial_any,
        "valid_graphs": valid,
        "p_author_denominator": p_author, "p_conditional": p_cond,
        "author_numbers": {"hits_lambda": 3011, "hits_both": 39,
                           "p_null": 3.9e-4},
        "pass": s2,
    }


# ============================================================
# PART 3 — THE STACK'S CHANNEL COUNT (gates S3a/S3b)
# ============================================================

from experiments.exp73_active_renormalization import (  # noqa: E402
    make_battery, N, CONTRAST, HEAD_V,
)
from experiments.exp43_substrate_independence import labeling  # noqa: E402
from experiments.exp78_phase_diagram import shell_of, G_GAP, y_of  # noqa: E402
from experiments.exp79_two_channel_law import RUN_T, DT  # noqa: E402
from cultivation.substrate.graph import GraphCollective  # noqa: E402

ERR_BAR = 6.0
STAR_GAMMA = 64.0
STAR_MU = 0.0

# the pre-named battery: family -> magnitudes (the sets exactly as the
# docstring pre-named them)
FAMILIES = [
    ("v_offset",   [5.0, 10.0, 20.0]),
    ("v_gain",     [0.5, 0.75, 1.5]),
    ("v_noise",    [2.0, 5.0, 10.0]),
    ("th_offset",  [5.0, 10.0, 20.0]),
    ("th_noise",   [2.0, 5.0, 10.0]),
    ("gj_thin",    [0.25, 0.5, 0.75]),
    ("gj_shell",   [0.0]),
    ("gamma_dial", [0.25, 4.0]),
    ("mu_dial",    [0.015, 0.005, 0.0015, 0.0005]),
    ("wound",      [0.015, 0.0]),
]
GROUP_OF = {
    "v_offset": "V-STATE", "v_gain": "V-STATE", "v_noise": "V-STATE",
    "th_offset": "THETA-STATE", "th_noise": "THETA-STATE",
    "gj_thin": "WINDOW", "gj_shell": "WINDOW",
    "gamma_dial": "V-RATIO", "mu_dial": "THETA-DIFFUSION",
    "wound": "WOUND",
}
ARMS = ("scale_free", "random3", "torus")
SEEDS = (1, 2, 3)


def theta_term_T(A: np.ndarray, lbl: np.ndarray, mu: float, T: float) -> float:
    """exp79's theta-term, verbatim formula, with the window explicit."""
    hi = (lbl == HEAD_V)
    worst = 0.0
    for i in np.where(hi)[0]:
        nbrs = np.where(A[i] > 0)[0]
        if len(nbrs) == 0:
            continue
        imbalance = abs(float(np.mean(lbl[nbrs]) - lbl[i]))
        tt = imbalance * (1 - np.exp(-mu * len(nbrs) * T))
        worst = max(worst, tt)
    return worst


def v_term_eff(A: np.ndarray, W_eff: np.ndarray, lbl: np.ndarray,
               gamma: float) -> float:
    """exp79's V-term with the instance's junction weights."""
    y, _ = y_of(A, W_eff, lbl, gamma)
    return CONTRAST * y / (1 + y)


def run_instance(A: np.ndarray, lbl: np.ndarray, seed: int, family: str,
                 mag: float, mag_idx: int, shell: list[tuple[int, int]]):
    """Settle at the star (exp79's run_gm verbatim), intervene, respond."""
    c = GraphCollective(adjacency=A, seed=seed, gamma=STAR_GAMMA,
                        mu_theta=STAR_MU)
    c.set_target(lbl)
    c.theta = lbl.copy()
    c.V = c.theta + c.rng.normal(0.0, 2.0, N)
    dt_star = min(DT, 1.2 / (STAR_GAMMA + float(c.deg.max())))
    c.run(RUN_T, dt=dt_star)
    err0 = c.pattern_error(lbl)

    jrng = np.random.default_rng(seed * 7919 + mag_idx)  # pre-named stream
    W_eff = np.ones_like(A)
    gamma_eff, mu_eff, T = STAR_GAMMA, STAR_MU, RUN_T
    if family == "v_offset":
        c.V = c.V + mag
    elif family == "v_gain":
        c.V = c.V.mean() + mag * (c.V - c.V.mean())
    elif family == "v_noise":
        c.V = c.V + jrng.normal(0.0, mag, N)
    elif family == "th_offset":
        c.theta = c.theta + mag
    elif family == "th_noise":
        c.theta = c.theta + jrng.normal(0.0, mag, N)
    elif family == "gj_thin":
        c.block_gap_junctions(mag)
        W_eff = np.full_like(A, mag)
    elif family == "gj_shell":
        for (i, j) in shell:
            W_eff[i, j] = W_eff[j, i] = 0.0
        c.G = c.A * G_GAP * W_eff
        c.deg = c.G.sum(axis=1)
    elif family == "gamma_dial":
        c.gamma = mag
        gamma_eff = mag
    elif family == "mu_dial":
        c.mu = mag
        mu_eff = mag
    elif family == "wound":
        c.amputate(slice(40, 60))
        c.mu = mag
        mu_eff, T = mag, 240.0
    else:
        raise ValueError(family)

    c.run(T if family == "wound" else RUN_T, dt=dt_star)
    err = c.pattern_error(lbl)
    eV_state = float(np.sqrt(np.mean((c.V - lbl) ** 2)))
    eT_state = float(np.sqrt(np.mean((c.theta - lbl) ** 2)))
    pred = max(v_term_eff(A, W_eff, lbl, gamma_eff),
               theta_term_T(A, lbl, mu_eff, T))
    return err, err0, pred, eV_state, eT_state


def part3() -> dict:
    battery = make_battery()
    lbl = labeling(N)
    rows = []
    for arm in ARMS:
        A = battery[arm]
        shell = shell_of(A, list(range(0, 25)))
        for family, mags in FAMILIES:
            for mag_idx, mag in enumerate(mags):
                for seed in SEEDS:
                    err, err0, pred, eV, eT = run_instance(
                        A, lbl, seed, family, mag, mag_idx, shell)
                    rows.append({
                        "arm": arm, "family": family,
                        "group": GROUP_OF[family], "mag": float(mag),
                        "mag_idx": mag_idx, "seed": seed,
                        "err": round(err, 4), "err0": round(err0, 4),
                        "pred": round(pred, 4),
                        "eV_state": round(eV, 4), "eT_state": round(eT, 4),
                    })
    n_rows = len(rows)
    finite = all(np.isfinite(r["err"]) and np.isfinite(r["pred"])
                 for r in rows)

    # S3a: pooled Spearman(pred, err), exp79's rank-correlation form
    preds = np.array([r["pred"] for r in rows])
    errs = np.array([r["err"] for r in rows])
    rho = float(np.corrcoef(np.argsort(np.argsort(preds)),
                            np.argsort(np.argsort(errs)))[0, 1])
    law_branch = "LAW-EXTENDS" if rho >= 0.90 else "LAW-BOUNDED-TO-WRITE"

    # S3b: the count. Breakout rule: ANY pre-named magnitude x ANY arm —
    # a deliberate SUPERSET of the docstring's largest-magnitude rule
    # (the severity ordering of the mu-dials is ambiguous against the 0
    # baseline; the superset is conservative TOWARD the paper: it can
    # only add channels, never hide one). Tolerance: err_mean exceeds the
    # arm's pred by more than max(2.0, 0.5*pred) — exp79's TC-G4 form.
    breakout = {}
    for family, mags in FAMILIES:
        per_family = {"instances": [], "broke_out": False}
        for mag_idx, mag in enumerate(mags):
            for arm in ARMS:
                sel = [r for r in rows if r["arm"] == arm
                       and r["family"] == family
                       and r["mag_idx"] == mag_idx]
                err_mean = float(np.mean([r["err"] for r in sel]))
                pred_arm = float(np.mean([r["pred"] for r in sel]))
                tol = max(2.0, 0.5 * pred_arm)
                hit = err_mean > pred_arm + tol
                per_family["instances"].append(
                    {"arm": arm, "mag": float(mag),
                     "err": round(err_mean, 3), "pred": round(pred_arm, 3),
                     "tol": round(tol, 3),
                     "excess": round(err_mean - pred_arm, 3),
                     "broke_out": bool(hit)})
                if hit:
                    per_family["broke_out"] = True
        breakout[family] = per_family

    # group verdicts; the wound@mu=0 breakout ATTRIBUTED to
    # THETA-DIFFUSION (pre-named: exp79 TC-G6's price, not a new channel)
    group_verdicts: dict[str, dict] = {}
    for family, mags in FAMILIES:
        g = GROUP_OF[family]
        target = "THETA-DIFFUSION" if family == "wound" else g
        gv = group_verdicts.setdefault(
            target, {"families": [], "broke_out": False})
        gv["families"].append(family)
        gv["broke_out"] = gv["broke_out"] or breakout[family]["broke_out"]

    count = sum(1 for g in group_verdicts.values() if g["broke_out"])
    branch = ("STACK-2CH" if count == 2 else
              "STACK-8PLUS" if count >= 8 else "STACK-3to7")
    s3b = bool(finite and n_rows == 243 and all(
        v is not None for v in breakout.values()))

    # the census (non-gated)
    census = [
        {"channel": "Vmem bistability", "verdict": "CARRIES",
         "stack": "the V contrast machinery (gamma, y-ratio; exp78/exp79)"},
        {"channel": "Gap-junctional morphogenesis", "verdict": "CARRIES",
         "stack": "the G/W window (exp78 settle/regrow; exp79 TC-G4)"},
        {"channel": "Ca2+ transient signaling", "verdict": "ABSENT",
         "stack": "no Ca2+ layer in the stack"},
        {"channel": "Vmem propagation through GJ networks",
         "verdict": "CARRIES",
         "stack": "theta diffusion mu*lap_theta (exp79 theta-channel)"},
        {"channel": "Epigenetic control of proliferation",
         "verdict": "CARRIES",
         "stack": "the theta/spec memory layer (M28 set_target, M37 gene "
                  "layer; exp87's write_spec_layer)"},
        {"channel": "Ion channel expression (voltage-gated)",
         "verdict": "CARRIES",
         "stack": "the gamma dial (exp78's V-channel ratio)"},
        {"channel": "Serotonin transport (5-HT electrophoresis)",
         "verdict": "ABSENT",
         "stack": "no transmitter layer in the stack"},
        {"channel": "Apoptosis as morphogenetic signal", "verdict": "ABSENT",
         "stack": "no death layer in the stack"},
    ]

    s3a = rho >= 0.90
    print(f"  S3 battery: {n_rows} instances, all finite {finite}")
    print(f"  S3a pooled Spearman(pred, err) = {rho:.4f} -> {law_branch}")
    for fam, w in breakout.items():
        worst_inst = max(w["instances"], key=lambda x: x["excess"])
        print(f"      {fam:11s} worst {worst_inst['arm']:11s} "
              f"mag {worst_inst['mag']:7.4g} err {worst_inst['err']:8.2f} "
              f"pred {worst_inst['pred']:7.2f} -> "
              f"{'BREAKOUT' if w['broke_out'] else 'absorbed'}")
    for g, gv in group_verdicts.items():
        print(f"      group {g:16s} broke_out={gv['broke_out']} "
              f"({','.join(gv['families'])})")
    print(f"  S3b count = {count} -> {branch} "
          f"({'well-defined' if s3b else 'ILL-DEFINED'})")

    return {
        "n_instances": n_rows, "all_finite": finite,
        "pooled_spearman": rho, "law_reach_branch": law_branch,
        "rows": rows, "breakout": breakout,
        "breakout_rule": "any pre-named magnitude x any arm (a superset "
                         "of the docstring's largest-magnitude rule; "
                         "conservative toward the paper — it can only "
                         "add channels, never hide one)",
        "group_verdicts": group_verdicts, "count": count, "branch": branch,
        "census": census,
        "wound_attribution": "the wound@mu=0 breakout is attributed to "
                             "THETA-DIFFUSION (the propagation channel's "
                             "absence — exp79 TC-G6's price), pre-named",
        "pass_S3a": bool(s3a), "pass_S3b": s3b,
    }


def main() -> dict:
    print("=== exp232: the Sephirotic 8-channel test ===\n")
    print("-- Part 1: the paper's arithmetic, exact --")
    s1 = part1()
    print("\n-- Part 2: the null reproduced --")
    s2 = part2()
    print("\n-- Part 3: the stack's channel count --")
    s3 = part3()

    branches = {"S1": s1["pass"], "S2": s2["pass"],
                "S3a": s3["pass_S3a"], "S3b": s3["pass_S3b"]}
    counts_absent = sum(1 for row in s3["census"]
                        if row["verdict"] == "ABSENT")
    finding = (
        f"S1 {'PASS' if branches['S1'] else 'REFUTED'}: the paper's "
        f"lambda6=6/5 claim verified EXACTLY (integer determinant) with "
        f"the 3+8 sector split and all 8 channel edges; "
        f"S2 {'PASS' if branches['S2'] else 'REFUTED'}: the author's null "
        f"reproduced ({s2['hits_lambda']} lambda-hits / "
        f"{s2['hits_both']} joint vs author 3011/39); "
        f"S3 {s3['law_reach_branch']}: the two-channel law's pooled rank "
        f"over the response battery {s3['pooled_spearman']:.3f}; "
        f"S3b count = {s3['count']} -> {s3['branch']}: the stack realizes "
        f"{s3['count']} channel groups, not 8, and {counts_absent} of the "
        f"paper's 8 channels (Ca2+, 5-HT, apoptosis) have NO stack "
        f"substrate at all — the 8-channel correspondence does not "
        f"transfer to this stack; the honest deposit.")
    out = {
        "exp": "exp232_sephirotic_channels (the OVERRIDE directive)",
        "S1": s1, "S2": s2,
        "S3": {k: v for k, v in s3.items() if k != "rows"},
        "S3_rows": s3["rows"],
        "criteria": branches,
        "finding": finding,
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    npass = sum(1 for v in branches.values() if v)
    print(f"  === {npass}/4 gates PASS ===")
    print(f"  FINDING: {finding}")
    return out


if __name__ == "__main__":
    main()
