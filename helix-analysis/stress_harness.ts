/**
 * Escalating stress harness for helix-codec core codec (pure-JS path, no native addon).
 *
 * Dimensions:
 *   1. Size ladder:        1KB / 16KB under DEFAULT (Illumina) and NANOPORE configs
 *   2. Error escalation:   error-rate multipliers 1x..4x until decode breaks
 *   3. Coverage starvation: 20x down to 2x reads per oligo
 *   4. Realistic worst-case presets: REAL_2024, PACBIO
 *
 * CLI: --out=path.json --sizes=1000,16000 --filter=substring   (filter skips execution)
 * Results are flushed to disk after EVERY case so timeouts/OOM never lose partial data.
 */
import { randomBytes } from 'crypto';
import { encodeFile } from '../src/lib/dna/codec';
import { decodeReads } from '../src/lib/dna/decode';
import {
  simulate,
  PRESET_ILLUMINA,
  PRESET_NANOPORE,
  PRESET_REAL_2024,
  PRESET_PACBIO,
  type MutationConfig,
} from '../src/lib/dna/simulate';
import {
  DEFAULT_CONFIG,
  NANOPORE_CONFIG,
  type CodecConfig,
} from '../src/lib/dna/types';

const OUT_PATH =
  process.argv.find((a) => a.startsWith('--out='))?.slice(6) ?? './stress_local.json';
const SIZE_ARG = process.argv.find((a) => a.startsWith('--sizes='))?.slice(8);
const SIZES = (SIZE_ARG ?? '1000,16000').split(',').map(Number);
const FILTER = process.argv.find((a) => a.startsWith('--filter='))?.slice(9) ?? '';
const want = (label: string) => !FILTER || label.includes(FILTER);

let warnCount = 0;
const origErr = console.error;
console.error = (...args: unknown[]) => {
  warnCount++;
  origErr(...args);
};

function withTimeout<T>(p: Promise<T>, ms: number, label: string): Promise<T | null> {
  return Promise.race([
    p,
    new Promise<null>((res) =>
      setTimeout(() => {
        origErr(`[stress] TIMEOUT ${label} after ${ms}ms`);
        res(null);
      }, ms),
    ),
  ]);
}

interface CaseResult {
  case: string;
  config: string;
  channel: string;
  bytes: number;
  oligos: number;
  reads: number;
  coverage: number;
  errMultiplier: number;
  encodeMs: number;
  simulateMs: number;
  decodeMs: number;
  success: boolean | 'timeout' | 'error';
  roundtripBytes: number;
  warnings: number;
  useSoftInfo?: boolean;
  recoveryRate?: number;
  oligosRecovered?: number;
  oligosErased?: number;
  failedInnerRS?: number;
  note?: string;
}

const results: CaseResult[] = [];
import { writeFileSync as _wfs } from 'fs';
const flush = () => _wfs(OUT_PATH, JSON.stringify({ results }, null, 2));

async function runCase(
  label: string,
  configName: string,
  channelName: string,
  data: Uint8Array,
  cfg: CodecConfig,
  mut: MutationConfig,
  errMultiplier = 1,
  useSoftInfo = true,
): Promise<void> {
  const warnBefore = warnCount;
  const result: CaseResult = {
    case: label,
    config: configName,
    channel: channelName,
    bytes: data.length,
    oligos: 0,
    reads: 0,
    coverage: mut.coverage,
    errMultiplier,
    encodeMs: -1,
    simulateMs: -1,
    decodeMs: -1,
    success: 'error',
    roundtripBytes: 0,
    warnings: 0,
    useSoftInfo,
  };
  try {
    const t0 = Date.now();
    const enc = await withTimeout(
      encodeFile(data, cfg, { fileName: label, contentType: 'application/octet-stream' }),
      120_000,
      `${label}:encode`,
    );
    if (!enc) {
      Object.assign(result, { success: 'timeout', note: 'encode timeout' });
    } else {
      result.encodeMs = Date.now() - t0;
      result.oligos = enc.encoded.oligos.length;

      const t1 = Date.now();
      const sim = simulate(enc.encoded.oligos, { ...mut, seed: 42 });
      result.simulateMs = Date.now() - t1;
      result.reads = sim.reads.length;

      const t2 = Date.now();
      const dec = await withTimeout(
        decodeReads(
          sim.reads,
          enc.encoded.metadata,
          cfg,
          enc.encoded.forwardPrimer,
          enc.encoded.reversePrimer,
          useSoftInfo,
        ),
        120_000,
        `${label}:decode`,
      );
      if (!dec) {
        Object.assign(result, { success: 'timeout', note: 'decode timeout' });
      } else {
        result.decodeMs = Date.now() - t2;
        result.success = dec.hashMatches === true;
        result.roundtripBytes = dec.data?.length ?? 0;
        const oc = enc.encoded.metadata.oligoCount || result.oligos || 1;
        result.oligosRecovered = dec.stats?.oligosRecovered ?? -1;
        result.oligosErased = dec.stats?.oligosErased ?? -1;
        result.failedInnerRS = dec.stats?.oligosFailedInnerRS ?? -1;
        result.recoveryRate = (dec.stats?.oligosRecovered ?? 0) / oc;
        if (!result.success) result.note = 'hash mismatch or null data';
      }
    }
  } catch (e) {
    result.note = `exception: ${(e as Error)?.message?.slice(0, 140)}`;
  }
  result.warnings = warnCount - warnBefore;
  results.push(result);
  flush();
  origErr(
    `[stress] ${label.padEnd(20)} ${String(result.success).padEnd(8)} enc=${result.encodeMs}ms dec=${result.decodeMs}ms oligos=${result.oligos}`,
  );
}

function scaleErrors(base: MutationConfig, m: number): MutationConfig {
  return {
    ...base,
    substitutionRate: Math.min(0.4, base.substitutionRate * m),
    insertionRate: Math.min(0.4, base.insertionRate * m),
    deletionRate: Math.min(0.4, base.deletionRate * m),
    dropoutRate: Math.min(0.6, base.dropoutRate + (m - 1) * 0.02),
  };
}

async function main() {
  // 1. size ladder
  for (const [cfgName, cfg, mut] of [
    ['DEFAULT-illumina', DEFAULT_CONFIG, PRESET_ILLUMINA],
    ['NANOPORE', NANOPORE_CONFIG, PRESET_NANOPORE],
  ] as [string, CodecConfig, MutationConfig][]) {
    for (const size of SIZES) {
      if (!want(`size-${size}`)) continue;
      await runCase(`size-${size}`, cfgName, 'preset', randomBytes(size), cfg, {
        ...mut,
        seed: 42,
      });
    }
  }

  // 2. error escalation (16KB)
  for (const m of [1, 1.5, 2, 3, 4]) {
    if (!want(`illumina-err-${m}x`)) continue;
    await runCase(
      `illumina-err-${m}x`,
      'DEFAULT-illumina',
      'scaled',
      randomBytes(16_000),
      DEFAULT_CONFIG,
      scaleErrors(PRESET_ILLUMINA, m),
      m,
    );
  }
  for (const m of [1, 2]) {
    if (!want(`nanopore-err-${m}x`)) continue;
    await runCase(
      `nanopore-err-${m}x`,
      'NANOPORE',
      'scaled',
      randomBytes(16_000),
      NANOPORE_CONFIG,
      scaleErrors(PRESET_NANOPORE, m),
      m,
    );
  }

  // 3. coverage sweep: starvation AND full-recovery threshold (16KB, illumina)
  for (const cov of [80, 60, 40, 30, 20, 10, 5, 3, 2]) {
    if (!want(`coverage-${cov}x`)) continue;
    await runCase(
      `coverage-${cov}x`,
      'DEFAULT-illumina',
      'sweep',
      randomBytes(16_000),
      DEFAULT_CONFIG,
      { ...PRESET_ILLUMINA, coverage: cov, seed: 42 },
    );
  }
  if (want('coverage-20x-nosoft')) {
    await runCase(
      'coverage-20x-nosoft',
      'DEFAULT-illumina',
      'sweep',
      randomBytes(16_000),
      DEFAULT_CONFIG,
      { ...PRESET_ILLUMINA, coverage: 20, seed: 42 },
      1,
      false,
    );
  }

  // 4. realistic worst cases (16KB)
  if (want('real2024-16k')) {
    await runCase('real2024-16k', 'DEFAULT-illumina', 'real', randomBytes(16_000), DEFAULT_CONFIG, {
      ...PRESET_REAL_2024,
      seed: 42,
    });
  }
  if (want('pacbio-16k')) {
    await runCase('pacbio-16k', 'DEFAULT-illumina', 'real', randomBytes(16_000), DEFAULT_CONFIG, {
      ...PRESET_PACBIO,
      seed: 42,
    });
  }

  // final summary (overwrite flushed partial)
  const okCount = results.filter((r) => r.success === true).length;
  const summary = {
    repo: 'helix-codec @ local clone (pure JS path, no native addon)',
    nativeAddon: false,
    cases: results.length,
    passed: okCount,
    failed: results.length - okCount,
    totalEncodeMs: results.reduce((s, r) => s + Math.max(0, r.encodeMs), 0),
    totalDecodeMs: results.reduce((s, r) => s + Math.max(0, r.decodeMs), 0),
    totalWarnings: warnCount,
    timestamp: new Date().toISOString(),
  };
  _wfs(OUT_PATH, JSON.stringify({ summary, results }, null, 2));
  origErr('\n=== STRESS SUMMARY ===');
  origErr(JSON.stringify(summary, null, 2));
  origErr(`JSON written to ${OUT_PATH}`);
}

main().catch((e) => {
  origErr('[stress] FATAL', e);
  process.exit(1);
});
