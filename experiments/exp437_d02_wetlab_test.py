#!/usr/bin/env python3
"""exp437 — THE MINIMAL FALSIFIABLE WET-LAB TEST FOR d-02 (batch HU-13;
exp416's registered follow-up). exp416 landed WETLAB-PATH-OPEN: 3/10
generator anatomies are realizable in the wet lab and the d-02 spec
was deposited. THE OPEN QUESTION: what is the MINIMAL falsifiable
test — the smallest intervention whose simulated signature, if
absent in the wet lab, kills the d-02 mechanism claim outright?

THE INSTRUMENT (a design experiment — the deliverable is the
protocol, the gates bind its structure): the d-02 anatomy's minimal
intervention selected by the pre-named criterion (fewest manipulated
variables with a pre-named simulated signature); the protocol
deposited as a structured spec (arm table, measurement, the
disconfirming observation, the confound list); every claim in the
spec traced to a landed experiment's deposit.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  THE TRACE: every mechanism claim in the spec cites a landed
      deposit (results/expNNN_*.json present in the repo); any
      uncited claim fails the gate (fail=STOP).
  G2  THE FALSIFIER: the spec names ONE disconfirming observation,
      stated as a measurement with a threshold, such that the
      mechanism claim is dead if it obtains; the observation is
      measurable with the equipment the d-02 anatomy's own paper
      used (no new instruments invented).
  G3  THE MINIMALITY: the intervention manipulates <= 2 variables
      and the arm table has <= 4 arms; a larger panel is a
      REFUTE of the minimality claim (deposited honestly).
  G4  THE SIGNATURE: the spec's simulated signature is computed
      from the repo's own machinery on the d-02 anatomy (the arm
      table's simulated outcomes deposited as numbers, not prose).
  G5  deposit results/exp437_d02_wetlab_test.json.

BRANCH LATTICE: SPEC-DEPOSITED (all gates pass) / SPEC-BLOATED (G3
REFUTE) / INSTRUMENT-REFUTED (G1 fail).
"""
