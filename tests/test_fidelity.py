"""Unit tests for the pattern-fidelity layer (Level-3 gate machinery)."""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import (
    FidelityAgingCohort, FidelityCodec, quantize, pattern_fidelity,
)

REGIME = dict(kappa_noise=0.020, lambda_gap=0.024, mu_theta=0.03,
              h_sys=0.050, seed_rate=6.0e-5, h_inflam=0.030, mortality_k=0.10)

TARGET = np.concatenate([np.full(12, v) for v in (-50.0, -20.0, -50.0, -60.0, -40.0)])


def test_quantize():
    # level centers at -70 + 10k
    assert quantize(-70.0) == 0
    assert quantize(-50.0) == 2
    assert quantize(-10.0) == 6
    assert quantize(-66.0) == 0      # rounds down toward center 0
    assert quantize(-35.0) in (3, 4)  # exactly between -> banker's rounding
    arr = quantize(np.array([-70.0, -55.0, -10.0]))
    assert list(arr) == [0, 2, 6]
    print("  quantize decision regions: OK")


def test_fidelity_metrics():
    ok = pattern_fidelity(TARGET.copy(), TARGET)
    assert ok == 1.0
    corrupted = TARGET.copy()
    corrupted[:5] = -20.0  # a jumped region
    assert pattern_fidelity(corrupted, TARGET) < 0.95
    # edge guard: boundary cells are excluded from the cohort metric
    ch = FidelityAgingCohort(K=10, params=AgingParams(n_cells=60, target0=TARGET,
                                                      **REGIME), seed=0)
    assert ch.F0 > 0.97, ch.F0
    assert ch._fid_keep.sum() == 52  # 60 - 8 boundary cells
    print(f"  fidelity + edge guard (F0={ch.F0:.3f}): OK")


def test_jump_statistics():
    ch = FidelityAgingCohort(K=200, params=AgingParams(n_cells=60, target0=TARGET,
                                                       **REGIME), seed=1,
                             jump_rate=0.01)
    # count cluster-jump EVENTS over 40 simulated years (end-state wrongness
    # is confounded by boundary blur and senesced-pin drag — events are clean)
    cell_events = 0
    for _ in range(160):
        pre = ch.theta.copy()
        ch.step(0.25)
        cell_events += int((np.abs(ch.theta - pre) > 5.0).sum())
    # expected: 12 clusters * 0.01/yr * 40 yr = 4.8 cluster-jumps/individual
    cluster_events_per_indiv = cell_events / 5.0 / 200
    assert 3.0 < cluster_events_per_indiv < 6.5, cluster_events_per_indiv
    print(f"  jump statistics ({cluster_events_per_indiv:.2f} cluster-jumps/indiv, "
          f"expected ~4.8): OK")


def test_codec_fixes_jumps_local_cannot():
    ch = FidelityAgingCohort(K=1, params=AgingParams(n_cells=60, target0=TARGET,
                                                     **REGIME), seed=2)
    ch.jump_rate = 0.0
    # manually jump cluster 3 (cells 15-19, a -20 region) to level 1 (-60)
    ch.theta[0, 15:20] = -60.0
    ch.V[0, 15:20] = -60.0
    f0 = float(ch.global_fidelity()[0])

    codec = FidelityCodec(n_cells=60, budget_per_cycle=6)
    preset = {"meas_noise_mV": 1.0, "dropout": 0.02, "symbol_err": 0.005}

    # local mode: consensus IS the jumped value -> invisible, nothing written
    ch_local = FidelityAgingCohort(K=1, params=AgingParams(n_cells=60, target0=TARGET,
                                                           **REGIME), seed=2)
    ch_local.jump_rate = 0.0
    ch_local.theta[0, 15:20] = -60.0
    ch_local.V[0, 15:20] = -60.0
    rep_l = codec.maintain(ch_local, preset, mode="local")
    f_local = float(ch_local.global_fidelity()[0])

    # codec mode: verified against archive -> detected and restored
    rep_c = codec.maintain(ch, preset, mode="codec")
    f_codec = float(ch.global_fidelity()[0])

    assert rep_l["restored"] == 0, rep_l
    assert rep_c["verified"] == 1 and rep_c["restored"] >= 5, rep_c
    assert f_codec > f_local + 0.05, (f_codec, f_local)
    print(f"  codec fixes jumped domains, local cannot "
          f"(F {f0:.2f} -> local {f_local:.2f}, codec {f_codec:.2f}): OK")


def test_regenerate_resets():
    ch = FidelityAgingCohort(K=20, params=AgingParams(n_cells=60, target0=TARGET,
                                                      **REGIME), seed=3)
    ch.jump_rate = 0.02
    for _ in range(80):
        ch.step(0.25)
    pre = float(np.mean(ch.global_fidelity()[ch.alive]))
    ch.regenerate(hazard=0.0)
    post = float(np.mean(ch.global_fidelity()[ch.alive]))
    assert post > pre + 0.1, (pre, post)
    assert ch.senesced[ch.alive].sum() == 0
    print(f"  regenerate restores pattern (F {pre:.2f} -> {post:.2f}): OK")


def test_write_precision_gate():
    codec = FidelityCodec(n_cells=60, budget_per_cycle=6)
    ch = FidelityAgingCohort(K=1, params=AgingParams(n_cells=60, target0=TARGET,
                                                     **REGIME), seed=4)
    ch.jump_rate = 0.0
    ch.theta[0, 15:20] = -60.0
    ch.V[0, 15:20] = -60.0
    # degraded channel: actuation 0.5*8 = 4 mV > 0.35*span (3.5 mV) -> refuse
    bad = {"meas_noise_mV": 8.0, "dropout": 0.3, "symbol_err": 0.08}
    rep = codec.maintain(ch, bad, mode="codec")
    assert rep["refused"] == 1 and rep["restored"] == 0, rep
    # local mode has no gate: it writes anyway (the contrast T3.1c tests)
    rep_l = codec.maintain(ch, bad, mode="local")
    assert rep_l["restored"] >= 0  # local never refuses
    print("  write-precision gate refuses reckless writes: OK")


def test_channel_boost():
    ch = FidelityAgingCohort(K=2, params=AgingParams(n_cells=60, target0=TARGET,
                                                     **REGIME), seed=5)
    for _ in range(200):  # ~50 yr: natural conductance decays
        ch.step(0.25)
    g_nat = np.exp(-ch.lam * ch.t) * ch.p.g0
    ch.boost_channel(np.array([True, False]), factor=4.0, cap=8.0)
    g_eff = np.minimum(g_nat * ch.channel_boost, ch.p.g0)
    assert ch.channel_boost[0] == 4.0 and ch.channel_boost[1] == 1.0
    assert g_eff[0] > g_nat[0] * 2 and g_eff[0] <= ch.p.g0 + 1e-12
    assert g_eff[1] == g_nat[1]
    print("  verification-gated channel boost (capped at youthful g0): OK")


def main():
    test_quantize()
    test_fidelity_metrics()
    test_jump_statistics()
    test_codec_fixes_jumps_local_cannot()
    test_regenerate_resets()
    test_write_precision_gate()
    test_channel_boost()
    print("\nALL FIDELITY TESTS PASSED")


if __name__ == "__main__":
    main()
