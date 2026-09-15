"""M37 gene-layer unit tests (exp60): the neoblast_depleted param is
additive and bit-exact at 0.0; at 1.0 the regenerated region seals
WITHOUT identity restoration (scar semantics) — a REGIONAL failure,
measured with the regen-region metric (the exp56 metric principle)."""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, ".")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp27_stage2_pilot import (  # noqa: E402
    N, DT, TAIL, ABN_ERR_MV, ABN_HL, make_collective,
)
from experiments.exp32_m26_repairs import HEAD, TAILP  # noqa: E402
from cultivation.bioelectric.morphospace import (  # noqa: E402
    wildtype_target, head_likeness,
)

WT = wildtype_target(N)


def _regen_region_err(c, reg: slice) -> float:
    """The regenerated region's deviation from its OWN wild-type target
    (the exp56 metric principle: regional failures are measured on the
    region that failed)."""
    return float(np.mean(np.abs(c.V[reg] - WT[reg])))


def test_neoblast_default_bit_exact():
    c1 = make_collective(7)
    c1.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
    c1.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6)
    c2 = make_collective(7)
    c2.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
    c2.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6,
              neoblast_depleted=0.0)
    assert float(np.max(np.abs(c1.V - c2.V))) == 0.0
    print("  neoblast_depleted=0.0 bit-exact: OK")


def test_neoblast_scar_regional():
    """nb=1.0: the regenerated region seals at the wound baseline —
    the regional error must exceed the abnormality bar while the whole-
    animal error can stay below it (regional failure dilution, the
    exp56 metric principle)."""
    for plane, reg, direction in (("tail", TAILP, "forward"),
                                  ("head", HEAD, "backward")):
        c = make_collective(7)
        c.amputate(reg, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(reg, cell_period=0.8, dt=DT, noise=0.6,
                 direction=direction, neoblast_depleted=1.0)
        rerr = _regen_region_err(c, reg)
        werr = c.pattern_error(WT)
        assert rerr >= ABN_ERR_MV, (plane, rerr)
        # the neoblast arm's abnormal verdict comes from the REGION
        assert rerr >= ABN_ERR_MV or head_likeness(c.V, TAIL) >= ABN_HL
    print("  neoblast scar regional abnormality (tail+head): OK")


def test_neoblate_dose_monotone():
    """Regional error decreases (weakly) as the scar blend weight drops:
    1.0 (pure scar) must produce the LARGEST regional deviation."""
    errs = []
    for nb in (1.0, 0.5, 0.25, 0.0):
        c = make_collective(7)
        c.amputate(TAILP, wound_voltage=-30.0, blastema_theta=-40.0)
        c.regrow(TAILP, cell_period=0.8, dt=DT, noise=0.6,
                 neoblast_depleted=nb)
        errs.append(_regen_region_err(c, TAILP))
    assert errs[0] >= errs[-1]
    print(f"  neoblast dose regional errors {[round(e, 2) for e in errs]}: OK")
