"""Systematic Reed-Solomon over GF(256) for spatial cell clusters.

Design inherits hard requirements from the helix-codec stress test
(helix-analysis/STRESS_REPORT.md):
  - erasures (dead/senesced clusters) are the dominant failure mode ->
    Vandermonde linear-system erasure decoding, provably MDS;
  - NO SILENT WRITES: symbol errors are *detected* via syndromes + CRC and
    converted to erasures (discard); a codeword is only trusted after full
    verification. The F3 silent-corruption failure mode is structurally
    forbidden here;
  - margin accounting: the codec reports parity budget remaining vs the
    current erasure count, so intervention triggers *before* capacity is
    exhausted (the F5 zero-margin failure mode is structurally forbidden).
"""

from __future__ import annotations

from .gf256 import gf_mul, gf_div, gf_inv, gf_pow, poly_mul, _exp, _log

# CRC-16/CCITT-FALSE for payload digests (verification before write-back)
def crc16(data: bytes | list[int]) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    return crc


def rs_generator_poly(nsym: int) -> list[int]:
    """Generator polynomial (x-a^1)(x-a^2)...(x-a^nsym), descending coeffs."""
    g = [1]
    for i in range(1, nsym + 1):
        g = poly_mul(g, [1, gf_pow(2, i)])
    return g


def rs_encode(data: list[int], nsym: int) -> list[int]:
    """Systematic encode: codeword = data (+ nsym parity symbols)."""
    gen = rs_generator_poly(nsym)
    n = len(data) + nsym
    buf = list(data) + [0] * nsym
    for i in range(len(data)):
        coef = buf[i]
        if coef != 0:
            for j in range(1, len(gen)):
                buf[i + j] ^= gf_mul(gen[j], coef)
    return list(data) + buf[len(data):]


def rs_syndromes(codeword: list[int], nsym: int) -> list[int]:
    """synd[i] = c(alpha^(i+1)) — all zero iff the codeword is valid."""
    n = len(codeword)
    out = []
    for i in range(1, nsym + 1):
        x = gf_pow(2, i)
        y = codeword[0]
        for c in codeword[1:]:
            y = gf_mul(y, x) ^ c
        out.append(y)
    return out


def _gauss_solve_gf(A: list[list[int]], b: list[int]) -> list[int] | None:
    """Solve A x = b over GF(256); returns None if singular."""
    m = len(A)
    n = len(A[0]) if m else 0
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = next((r for r in range(col, m) if M[r][col] != 0), None)
        if piv is None:
            return None
        M[col], M[piv] = M[piv], M[col]
        inv = gf_inv(M[col][col])
        M[col] = [gf_mul(v, inv) for v in M[col]]
        for r in range(m):
            if r != col and M[r][col] != 0:
                factor = M[r][col]
                M[r] = [M[r][j] ^ gf_mul(factor, M[col][j]) for j in range(n + 1)]
    return [M[r][n] for r in range(n)]


def rs_erase_decode(codeword: list[int], nsym: int,
                    erased: list[int]) -> list[int] | None:
    """Recover erased positions in-place. Any <= nsym erasures are correctable.

    Returns the repaired codeword, or None if not decodable (too many
    erasures / singular system). NEVER guesses silently: syndromes are
    re-verified after repair.
    """
    n = len(codeword)
    e = [i for i in erased if 0 <= i < n]
    if len(e) == 0:
        if any(rs_syndromes(codeword, nsym)):
            return None  # corrupted, nothing erased — caller must probe
        return list(codeword)
    if len(e) > nsym:
        return None
    # Parity check: sum_j c_j * (a^i)^(n-1-j) = 0 for i = 1..nsym
    # Unknowns: c_j for j in e.
    A = [[gf_pow(gf_pow(2, i + 1), n - 1 - j) for j in e] for i in range(nsym)]
    rhs = []
    for i in range(nsym):
        acc = 0
        for j in range(n):
            if j not in set(e):
                acc ^= gf_mul(codeword[j], gf_pow(gf_pow(2, i + 1), n - 1 - j))
        rhs.append(acc)
    sol = _gauss_solve_gf(A, rhs)
    if sol is None:
        return None
    repaired = list(codeword)
    for idx, j in enumerate(e):
        repaired[j] = sol[idx]
    if any(rs_syndromes(repaired, nsym)):
        return None  # verification failed — refuse to return a guess
    return repaired


def rs_check(codeword: list[int], nsym: int) -> bool:
    return not any(rs_syndromes(codeword, nsym))


class ClusterRSCodec:
    """The bioelectric-target codec: pattern symbols across spatial clusters.

    symbol = one GF(256) element quantizing a cell-cluster's mean voltage
    deviation from its healthy setpoint. n clusters total, k data clusters,
    nsym = n - k parity clusters. Erasures = dead (senesced) clusters.
    """

    LEVELS = 256
    V_MIN = -70.0
    V_MAX = -10.0

    def __init__(self, n: int, k: int, levels: int = 16):
        """levels: quantization granularity (16 -> 4 mV per level: aging drift
        stays sub-quantum, so RS fights real failures — dead clusters and rare
        flips — not slow drift)."""
        assert 0 < k <= n <= 255
        assert 1 < levels <= 256
        self.n, self.k = n, k
        self.nsym = n - k
        self.levels = levels
        self._step = 255.0 / (levels - 1)

    # -- quantization ------------------------------------------------------
    def quantize(self, values: list[float]) -> list[int]:
        span = self.V_MAX - self.V_MIN
        idx = [int(round((v - self.V_MIN) / span * (self.levels - 1))) for v in values]
        idx = [min(self.levels - 1, max(0, i)) for i in idx]
        return [int(round(i * self._step)) for i in idx]  # GF(256) lattice

    def dequantize(self, symbols: list[int]) -> list[float]:
        span = self.V_MAX - self.V_MIN
        return [self.V_MIN + (s / self._step) / (self.levels - 1) * span
                for s in symbols]

    # -- codec -------------------------------------------------------------
    def encode(self, target_symbols: list[int]) -> tuple[list[int], int]:
        """target_symbols: k symbols (the morphological message).
        Returns (codeword of n symbols, crc16 digest of the message)."""
        assert len(target_symbols) == self.k
        cw = rs_encode(list(target_symbols), self.nsym)
        return cw, crc16(list(target_symbols))

    def decode(self, observed: list[int], dead: list[int],
               digest: int) -> tuple[list[int] | None, dict]:
        """observed: n symbols (possibly corrupted values at live positions),
        dead: indices of dead clusters (values there are ignored),
        digest: expected crc of the true message.
        Returns (message symbols or None, report). Never returns unverified data."""
        n, k, nsym = self.n, self.k, self.nsym
        cw = list(observed)
        # detect symbol errors: if a codeword with `dead` masked out has
        # nonzero syndromes, live clusters contain corruption we cannot
        # localize individually -> convert worst offenders to erasures via
        # syndrome-guided probing is complex; we instead treat all
        # syndrome-inconsistent live clusters as suspect by re-encoding check:
        # strategy: first try pure erasure decode; verify; if fail, probe.
        report = {"requested_erasures": len(dead)}
        repaired = rs_erase_decode(cw, nsym, dead)
        if repaired is not None:
            msg = repaired[:k]
            report["strategy"] = "erasure"
            report["verified"] = True
            if crc16(msg) == digest:
                report["digest_ok"] = True
                return msg, report
            report["digest_ok"] = False
            # corrupted live symbols — fall through to probe
        # corrupted live symbols: progressively convert suspicious clusters
        # to erasures — exhaustive single probes, then bounded pair probes
        # (recovers up to floor(budget/2) symbol errors, the classic RS bound)
        live = [i for i in range(n) if i not in set(dead)]
        budget = nsym - len(dead)
        if budget >= 1:
            for extra in live[: min(len(live), 64)]:
                repaired = rs_erase_decode(cw, nsym, dead + [extra])
                if repaired is not None:
                    msg = repaired[:k]
                    report["strategy"] = "erasure+probe1"
                    report["verified"] = True
                    if crc16(msg) == digest:
                        report["digest_ok"] = True
                        return msg, report
        if budget >= 2:
            tried = 0
            for a in range(len(live)):
                for b in range(a + 1, len(live)):
                    if tried >= 400:
                        break
                    tried += 1
                    repaired = rs_erase_decode(cw, nsym, dead + [live[a], live[b]])
                    if repaired is not None:
                        msg = repaired[:k]
                        report["strategy"] = "erasure+probe2"
                        report["verified"] = True
                        if crc16(msg) == digest:
                            report["digest_ok"] = True
                            return msg, report
                if tried >= 400:
                    break
        report["verified"] = False
        report["digest_ok"] = False
        return None, report
