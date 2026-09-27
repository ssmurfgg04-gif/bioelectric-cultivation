#!/usr/bin/env python3
"""exp435 — WHAT THE COMMIT STREAM CARRIES: THE CONTENT DECOMPOSITION
(batch HU-13; exp414/421/425/426's shared exit). Three levers, three
nulls: coverage dilutes (exp421: union 0.598 < boundary 0.633), the
schedule is invariant (exp425), the chain buys +0.008 (exp426). The
shared exit: the boundary commits carry the fingerprint and the
interior commits do not. THE OPEN QUESTION: WHAT do the boundary
commits carry that the interior commits lack — dose magnitude, stress
context, wound adjacency, or timing?

THE INSTRUMENT (exp421's landed machinery verbatim; the content axis
as the new lever): the boundary stream scored as-is (the exp414 form,
the anchor); four ablations pre-named — (a) magnitude-shuffled
(each boundary commit's dose permuted within the stream), (b)
stress-context stripped (the stress pin lifted for boundary commits
only), (c) wound-adjacency stripped (the read face moved one hop off
the boundary), (d) timing-shuffled (the commit order permuted);
3 graphs x 3 seeds; AUC per ablation vs the anchor.

PRE-REGISTERED GATES (each evaluated exactly once):
  G1  the anchors: floor -60.0; constants asserted; the anchor arm
      reproduces exp421's deposited boundary per-graph bests within
      1e-3 (fail=STOP).
  G2  the discipline: the ablations fixed before the runs; each
      ablation touches ONE stream property; the permutions seeded
      and disclosed.
  G3  THE CONTENT: >= 1 ablation drops the AUC below the anchor by
      >= 0.05 (CONTENT-CARRIES — the ablation named) or no ablation
      moves it (CONTENT-NULL — the fingerprint is not in the
      boundary commits' content either; the program's read-side exit
      stands alone).
  G4  the anatomy: the (ablation x graph x seed) AUC table deposited.
  G5  deposit results/exp435_commit_stream_content.json.

BRANCH LATTICE: CONTENT-CARRIES / CONTENT-NULL / INSTRUMENT-REFUTED.
"""
