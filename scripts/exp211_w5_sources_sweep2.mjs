// exp211 — THE W5 SECOND PASS sweep (L182's registered next).
// Pre-registered protocol (module docstring, de1155d): (a) the 12
// pass-1-failed records re-swept at the protocol's pacing; (b) for
// records still failed, the pre-named widened query (drug + species +
// phenotype terms from the record's own fields); the acceptance
// predicate UNCHANGED (the Python module enforces it, not this file).
//
// DISCLOSURE (deposited verbatim in the sources file's meta): the
// pass-1 sweep script was lost (never committed); THIS script is the
// protocol's reimplementation from the deposited pass-1 protocol
// description (results/w5_pass_sources.json#protocol/#endpoint): one
// search per record per pass, num=8, verbatim-only regex extraction
// over the returned snippet text, unit conversion only into mM.
// Run from /home/z/my-project/zai-proxy (the SDK resolves there).
//
// Output: results/w5_pass_sources2.json — 119 records: the 107 ok
// pass-1 records carried VERBATIM (carried_from_pass1: true) + the
// 12 failed records re-swept (carried_from_pass1: false).
import { readFileSync, writeFileSync } from 'node:fs';
import ZAI from 'z-ai-web-dev-sdk';

const ROOT = '/home/z/my-project/bioelectric-cultivation';
const OUT = `${ROOT}/results/w5_pass_sources2.json`;
const PACING_MS = 12000;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const load = (p) => JSON.parse(readFileSync(p, 'utf8'));
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

const pass1 = load(`${ROOT}/results/w5_pass_sources.json`);
const series = load(`${ROOT}/research/levin_voltage_series.json`).series;
const bank = load(`${ROOT}/results/wetlab_companion_bank_w5.json`);
const byId = new Map(series.map((e) => [e.id, e]));

// ---- the blocker vocabulary: the bank's own blocker values --------
const BLOCKERS = new Set();
for (const r of [...(bank.entries || []), ...(bank.rejects || [])])
  if (r && typeof r.blocker === 'string' && r.blocker.trim())
    BLOCKERS.add(r.blocker.trim());
const blockerRe = BLOCKERS.size
  ? new RegExp([...BLOCKERS].map(esc).sort((a, b) => b.length - a.length)
      .join('|'), 'i')
  : null;

// ---- the extractor: verbatim-only, no inference --------------------
function extract(text, item) {
  const out = [];
  const quote = (m) => {
    const a = Math.max(0, m.index - 90);
    const b = Math.min(text.length, m.index + m[0].length + 90);
    return text.slice(a, b).replace(/\s+/g, ' ').trim();
  };
  const base = { url: item.url, host: item.host_name, name: item.name,
                 rank: item.rank };
  // concentration: value + unit -> value_mM (mM x1; µM /1e3; nM /1e6)
  const cre = /(\d+(?:[.,]\d+)?)\s*(mM|µM|uM|μM|nM)\b/gi;
  let m;
  while ((m = cre.exec(text)) !== null) {
    const v = parseFloat(m[1].replace(',', '.'));
    const u = m[2].toLowerCase();
    const mm = u === 'mm' ? v : u === 'nm' ? v / 1e6 : v / 1e3;
    if (mm > 0 && mm < 1e4)
      out.push({ kind: 'concentration', drug: null,
                 value_mM: Math.round(mm * 1e6) / 1e6,
                 quote: quote(m), ...base });
  }
  // blocker: a vocabulary drug verbatim
  if (blockerRe) {
    const bm = blockerRe.exec(text);
    if (bm) out.push({ kind: 'blocker', drug: bm[0],
                       quote: quote(bm), ...base });
  }
  // n: "n = 12" / "12 animals|worms|planarians|..."
  const nre = /\bn\s*=\s*(\d{1,4})\b/gi;
  while ((m = nre.exec(text)) !== null) {
    const v = parseInt(m[1], 10);
    if (v >= 1) out.push({ kind: 'n', value: v, quote: quote(m), ...base });
  }
  const nre2 = /\b(\d{1,4})\s+(animals|worms|planarians|specimens|samples|replicates|pieces|fragments)\b/gi;
  while ((m = nre2.exec(text)) !== null)
    out.push({ kind: 'n', value: parseInt(m[1], 10), quote: quote(m),
               ...base });
  // exposure_mode: sustained/pulse + exposure word, verbatim
  const ere = /\b(sustained|pulse)\s+(exposure|application|treatment|incubation)\b/gi;
  while ((m = ere.exec(text)) !== null)
    out.push({ kind: 'exposure_mode',
               value: m[1].toLowerCase(), quote: quote(m), ...base });
  // phenotype: explicit score/index 0..1
  const pre = /(?:regeneration\s+)?(?:score|index)\s*(?:of|=)\s*(\d(?:\.\d+)?)\b/gi;
  while ((m = pre.exec(text)) !== null) {
    const v = parseFloat(m[1]);
    if (v >= 0 && v <= 1)
      out.push({ kind: 'phenotype', value: v, quote: quote(m), ...base });
  }
  return out;
}

// ---- the widened query (pre-named): drug + species + phenotype ----
function widenedQuery(e) {
  const drugs = (e.drug_start_end || []).map((d) => d[0])
    .filter((d) => typeof d === 'string' && d.trim());
  const parts = [...new Set(drugs), e.species,
                 'planarian regeneration', e.region_or_tissue,
                 'concentration dose exposure']
    .filter(Boolean).join(' ');
  return parts;
}

async function main() {
  const zai = await ZAI.create();
  const failed1 = pass1.records
    .filter((r) => r.search_error || r.n_results === 0)
    .map((r) => r.id);
  console.log(`pass-1 failed: ${failed1.length} -> ${failed1.join(', ')}`);

  const records = [];
  const doc = () => ({
    pass: 2,
    protocol: ('second pass of the exp206 protocol: (a) the '
      + `${failed1.length} pass-1-failed records re-swept at 12 s `
      + 'pacing with the SAME protocol query; (b) records still '
      + 'failed re-queried with the pre-named widened query (drug + '
      + 'species + phenotype terms from the record\'s own fields); '
      + 'extraction verbatim-only regex over the returned snippets, '
      + 'unit conversion only into mM; the 107 ok pass-1 records '
      + 'carried verbatim; the acceptance predicate lives in the '
      + 'Python module (exp203\'s census), not here'),
    endpoint: pass1.endpoint,
    script_disclosure: ('the pass-1 sweep script was never committed; '
      + 'this file is the protocol\'s reimplementation from the '
      + 'deposited pass-1 protocol description; the blocker '
      + `vocabulary (${BLOCKERS.size} names) is derived from the w5 `
      + 'bank\'s own rows, zero hand-tuning'),
    pass1_failed_ids: failed1,
    retrieved: new Date().toISOString().slice(0, 10),
    records,
  });
  // checkpoint after every record (timeout-tolerant)
  const flush = () => writeFileSync(OUT, JSON.stringify(doc(), null, 1));

  for (const r1 of pass1.records) {
    if (!(r1.search_error || r1.n_results === 0)) {
      records.push({ ...r1, carried_from_pass1: true });
      continue;
    }
    const e = byId.get(r1.id);
    // PASS A: the protocol query, re-swept at pacing
    await sleep(PACING_MS);
    let verdict = { index: r1.index, id: r1.id,
                    query: r1.query, query_pass: 'resweep',
                    retrieved: new Date().toISOString().slice(0, 10),
                    search_ok: false, search_error: null, n_results: 0,
                    sources_tried: [], extracts: [],
                    carried_from_pass1: false };
    try {
      const res = await zai.functions.invoke('web_search',
                                             { query: r1.query, num: 8 });
      const items = (res || []).map((it, rank) => ({
        rank, url: it.url, host_name: it.host_name, name: it.name,
        date: it.date_publish || '', snippet: it.snippet || '' }));
      verdict.search_ok = true;
      verdict.n_results = items.length;
      verdict.sources_tried = items;
      for (const it of items) verdict.extracts.push(...extract(it.snippet, it));
    } catch (err) {
      verdict.search_error = String(err).slice(0, 220);
    }
    // PASS B: the widened query, for records still failed
    if (!verdict.search_ok || verdict.n_results === 0) {
      await sleep(PACING_MS);
      const q2 = widenedQuery(e);
      const v2 = { ...verdict, query: q2, query_pass: 'widened',
                   extracts: [], sources_tried: [], n_results: 0,
                   search_ok: false, search_error: null };
      try {
        const res = await zai.functions.invoke('web_search',
                                               { query: q2, num: 8 });
        const items = (res || []).map((it, rank) => ({
          rank, url: it.url, host_name: it.host_name, name: it.name,
          date: it.date_publish || '', snippet: it.snippet || '' }));
        v2.search_ok = true;
        v2.n_results = items.length;
        v2.sources_tried = items;
        for (const it of items) v2.extracts.push(...extract(it.snippet, it));
      } catch (err) {
        v2.search_error = String(err).slice(0, 220);
      }
      records.push(v2);
    } else {
      records.push(verdict);
    }
    console.log(`  [${r1.id}] pass2 ok=${verdict.search_ok} `
      + `n=${verdict.n_results} extracts=${verdict.extracts.length}`);
    flush();
  }

  writeFileSync(OUT, JSON.stringify(doc(), null, 1));
  const ok = records.filter((r) => !r.carried_from_pass1
    && r.search_ok && r.n_results > 0).length;
  console.log(`deposited ${OUT}: ${records.length} records `
    + `(${records.length - failed1.length} carried, ${ok}/${failed1.length} `
    + `re-swept ok)`);
}

main().catch((e) => { console.error(String(e)); process.exit(3); });
