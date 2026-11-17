"""Smoke tests for the reliability-theory aging model."""
import numpy as np
from cultivation.bioelectric.reliability import ReliabilityParams, simulate, late_hazard


def main():
    d = simulate(ReliabilityParams(lam=1000, k=0.04), 2000, 300, seed=0)
    assert np.isfinite(d).all(), "everyone should die by 300 yr without repair"
    d2 = simulate(ReliabilityParams(lam=1000, k=0.04), 2000, 300, seed=0,
                  repair_every=10, repair_c=1.0)
    assert np.median(d2) > np.median(d), "repair should extend lifespan"
    assert late_hazard(np.array([1.0, 2.0, np.inf]), 0, 10) > 0
    print("reliability tests: OK")


if __name__ == "__main__":
    main()
