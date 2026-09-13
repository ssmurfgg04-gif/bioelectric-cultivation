# helix-codec → Bioelectric Codec Adaptation Map

The user's thesis: **maintaining information integrity in a noisy biological channel is the same mathematical problem** whether the medium is DNA (synthesis/sequencing noise) or a cell collective (bioelectric noise, gap-junction dropout, target drift). helix-codec already implements the information-theoretic core for the DNA side. This document maps it onto the bioelectric side, which `cultivation/coding/` implements.

## The isomorphism, concretely grounded in their code

| helix-codec (verified in code) | Bioelectric framework (`cultivation/coding/`) |
|---|---|
| file → `encodeFile()` → oligos | morphological target θ* → quantize → symbols per spatial cluster |
| `PRESET_ILLUMINA` sub/ins/del rates | young organism: σ_η low, GJ dropout ~0 |
| `PRESET_NANOPORE` (indel-heavy, 9% raw) | old organism: σ_η grown e^κt, GJ dropout 5-30% |
| `coverage` (reads per oligo) | repeated measurement / redundant cells per cluster |
| `dropoutRate` (oligo lost) | cell death / senescence (cluster erasure) |
| outer RS across oligos (`outerParityRatio`) | RS(n,k) across spatial clusters — any n-k erasures recoverable |
| inner LDPC per oligo | gap-junction belief propagation within a neighborhood |
| `bayesian-consensus` / `msa-consensus` | neighbor consensus = iterative BP smoothing on the coupling graph |
| SHA-256 `hashMatches` gate | morphology check (pattern error threshold) before write-back |
| best-effort constraint emission (F5) | **forbidden in our codec** — write-back only after verified decode |
| clean-channel zero-margin recovery (F5) | margin accounting: parity budget ≥ expected erasures + noise margin |

## Design requirements imported from the stress test

1. **No silent writes.** F3 (99.7% "recovery" + hash mismatch) is the nightmare case for a biological write-back: applying a wrongly-decoded "corrected" pattern to a living collective is worse than no correction. The cultivation codec gates every `write()` on full verification of the decoded target against redundancy checks (RS parity + spatial coherence + CRC-style digest over the quantized pattern).
2. **Margin accounting, not bare capacity.** F5 showed outer RS succeeding at clean channel with exactly-zero margin. Our codec tracks "parity budget remaining vs expected erasure rate at current age" and triggers intervention *before* the budget is exhausted.
3. **Coverage is not a cure.** F2 showed consensus ceiling independent of coverage. Symptom for us: if the per-cell state is systematically corrupted (channel bias, not random noise), redundancy cannot fix it — the intervention must fix the bias (the aging model's drift term), which is precisely the bioelectric layer's job.
4. **Portability rule.** F4 (NANOPORE config crashes without native addon) — our Python reference implementation is pure-python+numpy with zero native deps, so the science layer runs anywhere (runners, laptops, containers).

## The cultivation codec (what we actually build)

```
maintain_loop(collective, codec, schedule):
    every Δt (a "checkup"):
        1. READ       noisy observation of cell voltages (measurement noise, dropouts)
        2. DECODE     BP smoothing on the coupling graph → denoised pattern
                      RS erasure-decode across clusters → recovered target
                      verify digest + parity budget
        3. DECIDE     if pattern error > threshold AND budget margin OK:
        4. WRITE      voltage clamp / conductance restore on the worst cells
                      (bounded intervention budget per cycle)
        5. LOG        margin ledger, error trajectory, interventions applied
```

This is the computational form of "cultivation as ongoing maintenance of the morphogenetic code" — the read/correct/write loop that keeps the error-correcting capability above the channel's noise level. Experiments: `experiments/exp6_error_correction.py` (lifespan extension with/without codec maintenance) and `experiments/exp7_stress.py` (sharded sweep over the degradation parameter space).

## Verification transfer

Their cascade ends in SHA-256. Ours ends in the falsification suite (`tests/test_falsification.py`): every claim about the codec's effect on pattern maintenance is an executable assertion with pre-registered thresholds.
