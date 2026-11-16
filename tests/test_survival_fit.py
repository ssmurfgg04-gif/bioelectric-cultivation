"""Survival-fit correctness: the Gompertz MLE must recover a known slope
from a left-truncated adult sample (review fix H3)."""
from __future__ import annotations

import numpy as np

from cultivation.bioelectric.aging import hazard_and_fits


def _gompertz_sample(a, b, n, rng):
    u = rng.random(n)
    return np.log(1.0 - b * np.log(u) / a) / b


def test_truncated_gompertz_recovers_beta():
    rng = np.random.default_rng(0)
    for b in (0.05, 0.08, 0.12, 0.16):
        a = 1e-4 * np.exp(0.08 * 35) / np.exp(b * 35)
        t = _gompertz_sample(a, b, 6000, rng)
        ad = t[t >= 35].copy()
        ad[ad > 100] = np.inf
        fit = hazard_and_fits(ad, 100.0, entry=35.0)
        est = np.exp(fit["fits"]["gompertz"]["params"][1])
        assert abs(est - b) / b < 0.06, (b, est)
    print("  truncated Gompertz MLE recovers beta (4 slopes, <6% err): OK")


def test_entry_zero_is_legacy():
    rng = np.random.default_rng(1)
    t = _gompertz_sample(1e-3, 0.09, 800, rng)
    t[t > 100] = np.inf
    f0 = hazard_and_fits(t, 100.0)
    f1 = hazard_and_fits(t, 100.0, entry=0.0)
    assert f0["fits"]["gompertz"]["params"] == f1["fits"]["gompertz"]["params"]
    print("  entry=0 bit-exact with legacy fit: OK")


def main():
    print("survival-fit tests:")
    test_truncated_gompertz_recovers_beta()
    test_entry_zero_is_legacy()
    print("all survival-fit tests passed")


if __name__ == "__main__":
    main()
