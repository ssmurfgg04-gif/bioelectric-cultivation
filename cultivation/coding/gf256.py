"""GF(2^8) arithmetic — the field over which our Reed-Solomon code runs.

Clean-room implementation (mirrors the architecture of helix-codec's
src/lib/dna/gf256.ts, which we stress-tested; see helix-analysis/). Generator
polynomial 0x11d, generator element 2. Tables are built once at import.
"""

from __future__ import annotations

import numpy as np

PRIM = 0x11D  # primitive polynomial x^8 + x^4 + x^3 + x^2 + 1

_exp: list[int] = [0] * 512
_log: list[int] = [0] * 256


def _build_tables() -> None:
    x = 1
    for i in range(255):
        _exp[i] = x
        _log[x] = i
        x <<= 1
        if x & 0x100:
            x ^= PRIM
    for i in range(255, 512):
        _exp[i] = _exp[i - 255]


_build_tables()

EXP = np.array(_exp, dtype=np.int64)
LOG = np.array(_log, dtype=np.int64)


def gf_mul(a: int, b: int) -> int:
    if a == 0 or b == 0:
        return 0
    return int(_exp[_log[a] + _log[b]])


def gf_div(a: int, b: int) -> int:
    if b == 0:
        raise ZeroDivisionError("gf_div by zero")
    if a == 0:
        return 0
    return int(_exp[(_log[a] - _log[b]) % 255])


def gf_inv(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError("gf_inv of zero")
    return int(_exp[255 - _log[a]])


def gf_pow(a: int, n: int) -> int:
    if a == 0:
        return 0
    return int(_exp[(_log[a] * n) % 255])


def poly_mul(p1: list[int], p2: list[int]) -> list[int]:
    """Multiply two polynomials (coefficient lists, highest degree last)."""
    r = [0] * (len(p1) + len(p2) - 1)
    for i, a in enumerate(p1):
        if a == 0:
            continue
        for j, b in enumerate(p2):
            if b:
                r[i + j] ^= gf_mul(a, b)
    return r


def poly_eval(poly: list[int], x: int) -> int:
    """Evaluate polynomial at x (Horner). poly is highest-degree-last? -> use descending?"""
    y = poly[0]
    for c in poly[1:]:
        y = gf_mul(y, x) ^ c
    return y
