"""THE HUMAN BRIDGE — the human-scale extension of the bioelectric
cultivation model (batch HU-1; docs/HUMAN_EXTENSION.md is the charter).

THE HYPOTHESIS UNDER TEST (Section 2 of the handoff): the structural
findings of the planarian corpus — the two-channel law, the history
register, the composed carrier, the deadline law — are universal
properties of bioelectric systems, not planarian-specific. The test:
extend the model to real human connectome data and check which
findings transfer.

REAL DATA ONLY (Section 9: no new experiments, mine what exists):
  * data/human_fc_schaefer400.npy — the HCP group-average functional
    connectome at the Schaefer-400 parcellation (400 cortical parcels),
    the discovery cohort of Vos de Wael et al. 2018 (PNAS), as
    distributed with brainspace (load_group_fc('schaefer', 400)).
  * data/physionet/ — real human PSG (Sleep-EDF: the same subject two
    consecutive nights, 100 Hz) and 24 h ECG with beat annotations
    (NSRDB record 16420).

ZERO CORE CHANGES: this package ADDS an ingestion layer. Every file
under cultivation/ stays byte-identical (asserted by exp401's H3). The
human mapping enters through the REAL connectivity structure only —
the dynamical parameters keep the planarian defaults (no parameter was
fitted to make the human run resemble anything; the honest default).
"""
from .substrate import (
    FC_SHA256, load_human_fc, build_human_adjacency, human_target,
)
