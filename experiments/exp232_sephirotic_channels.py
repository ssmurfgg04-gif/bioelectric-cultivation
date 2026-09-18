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


def main() -> dict:
    raise NotImplementedError(
        "exp232 body pending — pre-registration commit only")


if __name__ == "__main__":
    main()
