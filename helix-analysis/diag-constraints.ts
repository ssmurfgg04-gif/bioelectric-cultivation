// Diagnostic: does the 16KB encode emit constraint-violating (best-effort) oligos,
// and do they match the set that fails inner RS at decode time?
import { randomBytes } from 'crypto';
import { encodeFile } from '../src/lib/dna/codec';
import { simulate, PRESET_ILLUMINA } from '../src/lib/dna/simulate';
import { decodeReads } from '../src/lib/dna/decode';
import { DEFAULT_CONFIG } from '../src/lib/dna/types';
import { satisfiesConstraints, gcContent, maxHomopolymerRun } from '../src/lib/dna/mapping';

async function main() {
  const data = randomBytes(16000);
  const enc = await encodeFile(data, DEFAULT_CONFIG, {
    fileName: 'diag',
    contentType: 'application/octet-stream',
  });
  const cfg = DEFAULT_CONFIG;
  const violating = new Set<number>();
  let maxHpSeen = 0;
  for (const o of enc.encoded.oligos) {
    const inner = o.sequence.slice(cfg.primerLength, o.sequence.length - cfg.primerLength);
    if (!satisfiesConstraints(inner, cfg.constraints)) {
      violating.add(o.index);
      maxHpSeen = Math.max(maxHpSeen, maxHomopolymerRun(inner));
    }
  }
  console.log(`oligos=${enc.encoded.oligos.length} violating=${violating.size} maxHpSeen=${maxHpSeen}`);

  const sim = simulate(enc.encoded.oligos, { ...PRESET_ILLUMINA, seed: 42 });
  const dec = await decodeReads(
    sim.reads,
    enc.encoded.metadata,
    cfg,
    enc.encoded.forwardPrimer,
    enc.encoded.reversePrimer,
    true,
  );

  // Which oligos were erased / failed inner RS? decode stats don't expose per-oligo identity,
  // but oligosErased + oligosFailedInnerRS totals vs violating count is the correlation test.
  console.log(
    `recovered=${dec.stats.oligosRecovered} erased=${dec.stats.oligosErased} failedInnerRS=${dec.stats.oligosFailedInnerRS}`,
  );
  console.log(`violating(best-effort)=${violating.size}  lossTotal=${dec.stats.oligosErased + dec.stats.oligosFailedInnerRS}`);

  // Also: clean-channel decode of the SAME encoded set — do best-effort oligos fail even with ZERO noise?
  const simClean = simulate(enc.encoded.oligos, { ...PRESET_ILLUMINA, coverage: 0 + 1, substitutionRate: 0, insertionRate: 0, deletionRate: 0, dropoutRate: 0, seed: 42 });
  const decClean = await decodeReads(
    simClean.reads,
    enc.encoded.metadata,
    cfg,
    enc.encoded.forwardPrimer,
    enc.encoded.reversePrimer,
    true,
  );
  console.log(
    `CLEAN channel: recovered=${decClean.stats.oligosRecovered} erased=${decClean.stats.oligosErased} failedInnerRS=${decClean.stats.oligosFailedInnerRS} hashMatches=${decClean.hashMatches}`,
  );
}

main().catch((e) => {
  console.error('FATAL', e);
  process.exit(1);
});
