"""Tests for the real-data validation layer (vmem_inference)."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cultivation.validation import vmem_inference as VI   # noqa: E402


def test_ghk_bounds():
    """Pure K permeability -> E_K; pure Na -> E_Na."""
    ion = VI.ION
    ek = VI.ghk(1.0, 0.0, 0.0, ion)
    ena = VI.ghk(0.0, 1.0, 0.0, ion)
    expected_ek = VI.RTF_MV * np.log(ion["K"]["out"] / ion["K"]["in"])
    expected_ena = VI.RTF_MV * np.log(ion["Na"]["out"] / ion["Na"]["in"])
    assert abs(ek - expected_ek) < 0.5
    assert abs(ena - expected_ena) < 0.5
    assert ek < ena   # K hyperpolarizes, Na depolarizes


def test_extended_gene_weights():
    """Atlas classes present; innexin deliberately absent."""
    for cls in ("k_channel_leak", "kv_channel", "k_ca_channel", "nak_atpase",
                "hk_atpase", "fana_nav", "nav_channel", "trp_cation",
                "p2x_purinergic", "cl_channel", "hvcn"):
        assert cls in VI.GENE_WEIGHTS, cls
        channel, _w = VI.GENE_WEIGHTS[cls]
        assert channel in ("PK", "PNa", "PCl")
    assert "innexin" not in VI.GENE_WEIGHTS   # V4: coupling, not own-Vm


def test_infer_vmem_matrix():
    """infer_vmem accepts an arbitrary {type: {class: level}} matrix."""
    mat = {
        "A": {"k_channel_leak": 0.9, "trp_cation": 0.1, "cl_channel": 0.1},
        "B": {"k_channel_leak": 0.1, "trp_cation": 0.9, "cl_channel": 0.1},
    }
    out = VI.infer_vmem(mat)
    assert out["A"]["Vm_mV"] < out["B"]["Vm_mV"]   # K-rich hyperpolarized
    # floors: with zero expression the model still yields a finite Vm
    out0 = VI.infer_vmem({"floor": {}})
    assert np.isfinite(out0["floor"]["Vm_mV"])


def test_fana_depolarizes():
    """FaNaC (flatworm Na channel) expression depolarizes the prediction."""
    base = {"k_channel_leak": 0.5, "trp_cation": 0.2}
    lo = VI.infer_vmem({"t": dict(base, fana_nav=0.1)})["t"]["Vm_mV"]
    hi = VI.infer_vmem({"t": dict(base, fana_nav=0.8)})["t"]["Vm_mV"]
    assert hi > lo


def test_predictions_registered():
    """V1-V4 pre-registered with ground-truth citations."""
    ids = [p["id"] for p in VI.PUBLISHED_PREDICTIONS]
    assert ids == ["V1", "V2", "V3", "V4"]
    for p in VI.PUBLISHED_PREDICTIONS:
        assert p["prediction"] and p["ground_truth"]


if __name__ == "__main__":
    for fn in [test_ghk_bounds, test_extended_gene_weights,
               test_infer_vmem_matrix, test_fana_depolarizes,
               test_predictions_registered]:
        fn()
        print(f"PASS {fn.__name__}")
    print("all vmem_inference tests pass")


def main() -> int:
    for fn in [test_ghk_bounds, test_extended_gene_weights,
               test_infer_vmem_matrix, test_fana_depolarizes,
               test_predictions_registered]:
        fn()
        print(f"PASS {fn.__name__}")
    print("all vmem_inference tests pass")
    return 0
