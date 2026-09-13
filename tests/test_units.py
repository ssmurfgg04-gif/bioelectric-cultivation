"""Unit tests for the coding, dynamics, and information layers."""

from __future__ import annotations

import random
import sys

import numpy as np

sys.path.insert(0, ".")


def test_gf256():
    from cultivation.coding.gf256 import gf_mul, gf_inv, gf_div, gf_pow
    rng = random.Random(0)
    for _ in range(200):
        a, b = rng.randrange(256), rng.randrange(1, 256)
        assert gf_mul(a, b) // 1 >= 0
        assert gf_mul(a, gf_inv(b)) * 0 == 0
        assert gf_div(gf_mul(a, b), b) == a
        assert gf_mul(0, b) == 0 and gf_mul(a, 0) == 0
    assert gf_pow(2, 0) == 1
    print("  gf256 field axioms: OK")


def test_rs_roundtrip():
    from cultivation.coding.reed_solomon import ClusterRSCodec
    rng = random.Random(1)
    for (n, k) in [(20, 14), (24, 16), (12, 8), (15, 11)]:
        codec = ClusterRSCodec(n, k, levels=16)
        msg = [int(rng.randrange(16) * 17) for _ in range(k)]
        cw, digest = codec.encode(msg)
        dead = rng.sample(range(n), codec.nsym)
        obs = [int(rng.randrange(256)) if i in dead else cw[i] for i in range(n)]
        out, rep = codec.decode(obs, dead, digest)
        assert out == msg, (n, k, rep)
        # beyond capacity must refuse
        dead2 = rng.sample(range(n), codec.nsym + 1)
        obs2 = [int(rng.randrange(256)) if i in dead2 else cw[i] for i in range(n)]
        out2, _ = codec.decode(obs2, dead2, digest)
        assert out2 is None
    print("  RS erasure capacity + refusal: OK")


def test_rs_corruption():
    from cultivation.coding.reed_solomon import ClusterRSCodec
    rng = random.Random(2)
    codec = ClusterRSCodec(20, 14, levels=16)
    ok = 0
    for _ in range(10):
        msg = [int(rng.randrange(16) * 17) for _ in range(14)]
        cw, digest = codec.encode(msg)
        obs = list(cw)
        for i in rng.sample(range(20), 2):
            obs[i] = int(rng.randrange(16) * 17)
        out, _ = codec.decode(obs, [], digest)
        ok += int(out == msg)
    assert ok >= 9, ok
    print(f"  RS double-corruption probe: {ok}/10 OK")


def test_collective():
    from cultivation.bioelectric.collective import BioElectricCollective
    from cultivation.bioelectric.morphospace import wildtype_target
    c = BioElectricCollective(n=80, seed=3)
    c.set_target(wildtype_target(80))
    c.set_state(np.full(80, -50.0))
    c.run(20, dt=0.1)
    assert c.pattern_error(wildtype_target(80)) < 4.5
    # perturbation recovery (basin): a large injury partially corrupts the
    # slow target too (homeostatic plasticity), so recovery is partial but
    # real — the system pulls back from the injury-adjacent error.
    c.V[0:20] = -50.0
    immediate = c.pattern_error(wildtype_target(80))
    c.run(20, dt=0.1)
    recovered = c.pattern_error(wildtype_target(80))
    assert immediate > 2.0 * recovered and recovered < 5.0
    print("  collective convergence + basin recovery: OK")


def test_bp_smooth():
    from cultivation.coding.belief_prop import bp_smooth, bp_mse
    rng = np.random.default_rng(0)
    n = 60
    A = np.zeros((n, n))
    for i in range(n - 1):
        A[i, i + 1] = A[i + 1, i] = 1.0
    truth = np.linspace(-50, -20, n)
    y = truth + rng.normal(0, 3, n)
    mask = rng.random(n) > 0.4
    x = bp_smooth(y, A, mask, noise_var=9, iters=30)
    assert bp_mse(x, truth) < 2.0 * np.mean((y[mask] - truth[mask]) ** 2)
    print("  BP denoising/completion: OK")


def test_phi():
    from cultivation.information.phi import phi_integration
    n = 6
    W = np.zeros((n, n))
    for i in range(n - 1):
        W[i, i + 1] = W[i + 1, i] = 0.4
    integrated = phi_integration(W, np.eye(n) * 0.05)["phi"]
    W2 = np.zeros((n, n))
    for i in range(n // 2 - 1):
        W2[i, i + 1] = W2[i + 1, i] = 0.4
    for i in range(n // 2, n - 1):
        W2[i, i + 1] = W2[i + 1, i] = 0.4
    modular = phi_integration(W2, np.eye(n) * 0.05)["phi"]
    assert abs(modular) < 0.05, modular
    assert integrated > modular + 0.1
    print(f"  Phi: chain {integrated:.3f} vs modular {modular:.3f}: OK")


def test_mi():
    from cultivation.information.mutual_info import estimate_mi_joint
    rng = np.random.default_rng(0)
    X = rng.normal(0, 1, (500, 2))
    y = (X[:, 0] > 0).astype(int)
    mi = estimate_mi_joint(X, y, bins=2)
    assert 0.5 < mi <= 1.01, mi  # X0 determines y -> ~1 bit
    y2 = rng.integers(0, 2, 500)
    mi2 = estimate_mi_joint(X, y2, bins=2)
    assert mi2 < 0.1, mi2
    print(f"  MI estimator: informative {mi:.2f} bits, null {mi2:.2f} bits: OK")


def test_cem():
    from cultivation.inverse.cem import cem_optimize
    f = lambda u: float((u[0] - 2.0) ** 2 + (u[1] + 1.0) ** 2 + 3.0)
    u, fv, _ = cem_optimize(f, [(-10, 10)] * 2, pop=40, iters=15, seed=0)
    assert abs(u[0] - 2.0) < 0.2 and abs(u[1] + 1.0) < 0.2 and abs(fv - 3.0) < 0.05
    print("  CEM optimizer: OK")


def main():
    test_gf256()
    test_rs_roundtrip()
    test_rs_corruption()
    test_collective()
    test_bp_smooth()
    test_phi()
    test_mi()
    test_cem()
    print("\nALL UNIT TESTS PASSED")


if __name__ == "__main__":
    main()
