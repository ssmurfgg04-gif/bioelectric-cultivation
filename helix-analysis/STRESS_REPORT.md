# helix-codec Stress Test Report

**Target:** `ssmurfgg04-gif/helix-codec` @ main (v3.7.0) — 434 TS files, ~60k LOC code, Rust + C++ native components.
**Environment:** local sandbox, 2 CPU (Xeon), 4.1GB RAM, Node 24, **pure-JS path** (no native addon — no local cargo), `npm ci --ignore-scripts`, vitest 4.
**Harness:** `stress_harness.ts` (in this directory) — encode → simulate(preset) → decode with per-case timeouts, incremental flush, deterministic seed 42. Raw results: `stress_local.json` (23 cases).

## Verdict

The clean-channel path is **fast and correct**. The noisy-channel path has a **systematic recovery ceiling (~57-68%) that is independent of sequencing coverage (2x-80x) and of soft-information decoding**, plus a **silent-corruption-shaped failure** on deletion-heavy channels, plus a **hard crash of the NANOPORE config on the pure-JS path**. Full end-to-end file recovery (SHA-256 match) did not occur in any noisy case at any tested setting, including the repo's own nominal presets.

## Findings

### F1 — Clean roundtrip: PASS, fast
- 1KB: encode 101ms, decode 114ms, 20 oligos, SHA match.
- 16KB: encode ~180ms, decode ~180-300ms, 305 oligos, SHA match (clean preset).
- vitest suite (codec + holographic): 7/7 pass in 1.3s without native addon.

### F2 — Noisy recovery ceiling ~2/3, coverage-invariant (CRITICAL)
At `PRESET_ILLUMINA` (sub 0.1%, ins 0.05%, del 0.1%):
| coverage | recovery | erased | failed inner RS |
|---|---|---|---|
| 80x | 66.6% | 115 | 102 |
| 40x | 65.6% | 117 | 105 |
| 20x | 67.9% | 116 | 98 |
| 5x  | 65.6% | 128 | 105 |
| 2x  | 57.7% | 159 | 129 |

~1/3 of oligos fail inner RS **regardless of read depth** → the per-oligo failure is systematic, not statistical. Consensus across 20-80 noisy reads should trivially fix sub-0.1% error rates; it does not. The repo's own CI test (`scripts/test-codec.ts`) shows the same ceiling at 256 bytes (57.1% recovery, asserts only >50%), so this is the codec's current steady state, not a harness artifact. `useSoftInfo` true vs false: 67.9% vs 66.9% — not the variable.

### F3 — Silent-corruption signature on deletion-heavy channels (CRITICAL)
`PRESET_REAL_2024` (del 8.2%): decode bails in ~5ms, reports **99.7% oligo recovery** but **SHA mismatch**. `PRESET_PACBIO` (ins 5%): 98.4% "recovery", SHA mismatch. Near-total recovery + failed hash means data was reconstructed into *wrong bytes* (or recovery is miscounted under the HMM-fusion path). The failure is detected (SHA) but not repaired. Worst-case failure mode for a storage codec.

### F4 — NANOPORE_CONFIG crashes on pure-JS path
`encodeFile` throws `offset is out of bounds` for both 1KB and 16KB. Their CI builds the Rust native addon (viterbi/conv path) *before* running tests, so the JS fallback for this config is never exercised in CI. Broken JS fallback = portability regression.

### F5 — Best-effort constraint violations at scale
16KB encode emits **44/305 (14.4%) oligos violating constraints** (max homopolymer up to **9** vs limit 3) after 51 failed screening retries. At clean channel the resulting losses (30) exactly exhaust outer-RS parity (~10%) — recovery succeeds with **zero margin**. Any noise on top pushes past parity capacity. At 256 bytes (their CI size) violations don't appear — a scale-dependent defect invisible to CI.

### F6 — Memory ceiling on JS path
64KB encode OOMs with a 2.2GB heap (16KB is safe). Native addon required for large payloads. Runner workflow raises heap and builds the addon.

### F7 — Error escalation (the graceful-degradation curve)
Illumina error multiplier 1x→4x: recovery 67% → 52% → 43% → 37% → 33%. Monotone, no cliff — the cascade degrades gracefully. This is the system's best behavior under stress.

## Performance profile (16KB, JS path)
- encode ~90 KB/s, decode 62-850ms scaling with coverage, single-threaded.
- Memory: dominant cost is JS LDPC encode (OOM at 64KB).

## Reproduce
```bash
cd helix-codec && npm ci --ignore-scripts
npx vitest run src/lib/dna/codec.test.ts                          # F1
NODE_OPTIONS=--max-old-space-size=1800 npx tsx scripts/diag-constraints.ts   # F2/F5
NODE_OPTIONS=--max-old-space-size=1800 npx tsx scripts/stress-escalating.ts --sizes=1000,16000  # full matrix
```
Full-scale runs (native addon, 128KB-1MB, wider matrix) execute on GitHub Actions runners via `.github/workflows/helix-stress.yml` in the bioelectric-cultivation repo.
