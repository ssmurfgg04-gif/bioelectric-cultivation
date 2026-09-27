#!/usr/bin/env python3
"""exp432 — THE ENTANGLED REGISTER'S READ FACE (batch HU-13;
exp425's registered follow-up). exp425 landed DUALITY-ENTANGLED: the
dose correlations (rho_correct ~ -0.53, rho_stress ~ +0.58) are
INVARIANT across merged/split/stress_only/correct_only write
schedules — the register's channels are entangled at the READ, not
the write. THE OPEN QUESTION: WHICH CELLS' READS carry which
correlation? The blend reads at wound-facing boundary cells (exp425's
channel operationalization); the read face is the untested axis.

HYPOTHESIS: the read face, not the write schedule, is where the
entanglement lives — restricting the read to interior cells vs
boundary cells vs the union changes the correlations' magnitudes
(even if their signs survive, the exp425 lesson pre-named).

THE INSTRUMENT (exp425's landed form verbatim; the READ face as the
new axis): merged write schedule only (the calibration path), the
read restricted pre-named to three faces — BOUNDARY (exp425's own),
INTERIOR, UNION (every cell); the (pin x mult) crossing x hosts[:2]
x 3 seeds; R = the rescue read per face; rho per dose axis per face.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the anchors: floor -60.0 at entry/exit; constants asserted
      (COMMIT_NOISE 0.6, STEPS_PER_CELL 8, G_CTX 0.5); the merged
      arm at the BOUNDARY face replicates exp425's deposited merged
      rho within 1e-3 (fail=STOP).
  G2  the discipline: the read face is fixed per arm BEFORE the
      walks; no face-dependent rng path; the register-OFF twins
      cached per (host, seed, pin, mult).
  G3  THE DECOMPOSITION: the read face changes either correlation's
      magnitude by >= 0.1 on >= 1 face (READ-FACE-CARRIES) or it
      does not (READ-INVARIANT — the entanglement survives every
      read face too; the register's pluralism is total at n<=400).
  G4  the anatomy: the full (face x axis x host) rho table deposited
      + the per-face R tables.
  G5  deposit results/exp432_read_face_decomposition.json.

BRANCH LATTICE: READ-FACE-CARRIES / READ-INVARIANT /
INSTRUMENT-REFUTED (G1 fail).
"""
