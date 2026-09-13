# helix-codec Structure Map

Generated with `scc` 4.1.0 + repo inspection. Purpose: know exactly what exists before adapting its architecture to the bioelectric codec.

## Scale

| Language | Files | Lines | Code | Complexity |
|---|---|---|---|---|
| TypeScript | 434 | 88,391 | 59,763 | 10,342 |
| Rust | 18 | 5,712 | 4,106 | 1,146 |
| JavaScript | 23 | 5,420 | 4,066 | 721 |
| C++ | 10 | 1,138 | 792 | 177 |
| C | 2 | 686 | 459 | 97 |

It is a **Next.js 16 web app** (Radix UI, Prisma, TanStack) wrapped around a deep codec library in `src/lib/dna/` (~140 modules), with native acceleration in `rust/helix-dna-napi` (RS + Viterbi via napi-rs) and `rust/helix-dna-wasm`, plus C++ compressors compiled to WASM.

## Module map of `src/lib/dna/` (the part that matters to us)

**Error-correcting codes**
- `reedsolomon.ts` (299 LOC), `reedsolomon216.ts`, `fast-rs.ts`, `leopard-rs.ts` — RS variants (GF(256)/GF(2^16))
- `ldpc-codec.ts` (1,641 LOC), `neural-ldpc.ts`, `osd.ts`, `osd-full.ts` — LDPC + ordered-statistics decoding
- `convolutional.ts`, `convolutional-k9.ts`, `viterbi-preprocess.ts` — HEDGES-style conv inner code (Nanopore)
- `fountain.ts`, `raptor.ts` — rateless codes
- `gf256.ts`, `gf216.ts` — Galois field arithmetic

**Channel simulation** (→ direct analogue of our bioelectric channel)
- `simulate.ts` (668 LOC) — presets: CLEAN, ILLUMINA, REAL_2024, BANAL_2026, NANOPORE, PACBIO; sub/ins/del rates, coverage, dropout; `simulator: "basic" | "dt4dds"`
- `dt4dds-simulate.ts`, `wetlab-simulate.ts` — parametric wet-lab pipeline
- `presets.ts` (611 LOC) — full codec config presets per channel

**Consensus / soft decoding**
- `bayesian-consensus.ts`, `attention-consensus.ts`, `transformer-consensus.ts`, `msa-consensus.ts`, `soft-consensus.ts`, `soft-info-decode.ts`, `softinfo.ts`, `profileHmm.ts`, `profileHmm3.ts`, `progressive-msa.ts`

**Constraints & mapping** (→ bioelectric feasibility constraints)
- `constraints.ts`, `mapping.ts`, `constrained-mapping.ts`, `yinyang.ts`, `goldman.ts`, `gcplus.ts`, `mgc-plus.ts` — GC 40-60%, homopolymer ≤ 3, bijective derangement
- `thermodynamics.ts`, `bio-safety.ts`, `kmer.ts`

**Codec orchestration**
- `codec.ts` (1,959 LOC — encodeFile), `decode.ts`, `decode-strategies.ts`, `streaming-*.ts`, `encode-parallel.ts`, `worker-pool.ts`
- `archive.ts`, `bioarchive.ts`, `dna-aeon.ts`, `sovereign-archive.ts`, `addressing.ts`, `encryption.ts`, `signing.ts`, `post-quantum.ts`

**App layer (not reused):** UI panels, db, dashboards (`sota-dashboard.ts`), s3/hardware APIs.

## What we reuse vs reimplement

| helix-codec asset | Disposition in bioelectric-cultivation |
|---|---|
| Cascade architecture (outer RS across blocks + inner code per block + consensus + CRC/SHA verify) | **Reused as architecture** — clean-room reimplemented in Python (`cultivation/coding/`) |
| Channel preset concept (young/old noise profiles) | **Reused concept** → `bio_channel.py` presets |
| RS GF(256) systematic encoding | **Reimplemented** in `reed_solomon.py` (erasure + error decode) |
| Consensus from multiple noisy reads | **Reused concept** → neighbor belief propagation + repeated-measurement consensus |
| simulate.ts API shape (encode→simulate→decode, per-case stats) | **Reused as API design** for our stress harnesses |
| 23-case stress findings (coverage-invariant ceiling, silent corruption) | **Feeds design requirements**: strict verification before write-back, margin accounting |

Their TS/JS stack is not imported: the bioelectric framework is Python (scipy/numpy) for ODE dynamics; keeping the science layer dependency-light and runner-friendly.
