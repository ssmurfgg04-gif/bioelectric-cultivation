// exp215 — THE W5 FIGURE-PASS sweep (L184's registered next).
// Pre-registered protocol (module docstring, 08b1cfc): STRUCTURE-DRIVEN,
// not query-driven — query by the record's FIGURE/PANEL identity
// (db_experiment_id + db_figure_panel name the exact experiment the
// literature describes). The figure queries pre-named: per record,
// "{source} {db_figure_panel} {species}" (variant A) and
// "{db_experiment_id} {db_figure_panel}" (variant B; B only when A
// returns nothing — the sweep2 pass-A/pass-B shape). Extraction
// verbatim-only regex over the returned snippets, unit conversion only
// into mM; the acceptance predicate lives in the Python module.
//
// DISCLOSURE: the 20 series records without db identity fields (the
// model-quantity leg) carry NO figure identity — they are deposited as
// figure_identity_absent verdicts (the figure pass is vacuous for
// them, disclosed), keeping the pass complete at 119/119.
// RESUME-TOLERANT: if OUT exists, records already swept in THIS pass
// are kept and skipped (checkpoint after every record).
//
// Run from /home/z/my-project/zai-proxy (the SDK resolves there).
// Output: results/w5_pass_sources3.json — 119 records.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import ZAI from 'z-ai-web-dev-sdk';

const ROOT = '/home/z/my-project/bioelectric-cultivation';
const OUT = `${ROOT}/results/w5_pass_sources3.json`;
const PACING_MS = 12000;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const load = (p) => JSON.parse(readFileSync(p, 'utf8'));
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

const pass2 = load(`${ROOT}/results/w5_pass_sources2.json`);
const series = load(`${ROOT}/research/levin_voltage_series.json`).series;
const bank = load(
  `${ROOT}/results/wetlab_companion_bank_w5b.json`);
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

// ---- the extractor: verbatim-only, no inference (sweep2 verbatim) --
function extract(text, item) {
  const out = [];
  const quote = (m) => {
    const a = Math.max(0, m.index - 90);
    const b = Math.min(text.length, m.index + m[0].length + 90);
    return text.slice(a, b).replace(/\s+/g, ' ').trim();
  };
  const base = { url: item.url, host: item.host_name, name: item.name,
                 rank: item.rank };
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
  if (blockerRe) {
    const bm = blockerRe.exec(text);
    if (bm) out.push({ kind: 'blocker', drug: bm[0],
                       quote: quote(bm), ...base });
  }
  const nre = /\bn\s*=\s*(\d{1,4})\b/gi;
  while ((m = nre.exec(text)) !== null) {
    const v = parseInt(m[1], 10);
    if (v >= 1) out.push({ kind: 'n', value: v, quote: quote(m), ...base });
  }
  const nre2 = /\b(\d{1,4})\s+(animals|worms|planarians|specimens|samples|replicates|pieces|fragments)\b/gi;
  while ((m = nre2.exec(text)) !== null)
    out.push({ kind: 'n', value: parseInt(m[1], 10), quote: quote(m),
               ...base });
  const ere = /\b(sustained|pulse)\s+(exposure|application|treatment|incubation)\b/gi;
  while ((m = ere.exec(text)) !== null)
    out.push({ kind: 'exposure_mode',
               value: m[1].toLowerCase(), quote: quote(m), ...base });
  const pre = /(?:regeneration\s+)?(?:score|index)\s*(?:of|=)\s*(\d(?:\.\d+)?)\b/gi;
  while ((m = pre.exec(text)) !== null) {
    const v = parseFloat(m[1]);
    if (v >= 0 && v <= 1)
      out.push({ kind: 'phenotype', value: v, quote: quote(m), ...base });
  }
  return out;
}

// ---- the pre-named figure queries (per record, two variants) ------
function figureQueries(e) {
  const fig = e.db_figure_panel;
  const a = [e.source, fig, e.species].filter(Boolean).join(' ');
  const b = [e.db_experiment_id, fig].filter(Boolean).join(' ');
  return { a, b };
}

async function search(zai, query) {
  const res = await zai.functions.invoke('web_search',
                                         { query, num: 8 });
  return (res || []).map((it, rank) => ({
    rank, url: it.url, host_name: it.host_name, name: it.name,
    date: it.date_publish || '', snippet: it.snippet || '' }));
}

async function main() {
  const zai = await ZAI.create();
  const prev = existsSync(OUT) ? load(OUT) : null;
  const done = new Map();
  if (prev && Array.isArray(prev.records))
    for (const r of prev.records) done.set(r.id, r);
  console.log(`resume: ${done.size}/119 already swept in this pass`);

  const records = [];
  const noFig = series.filter((e) => !e.db_figure_panel
                                    && !e.db_experiment_id).length;
  const doc = () => ({
    pass: 3,
    protocol: ('third pass of the exp206 protocol, STRUCTURE-DRIVEN '
      + '(L184): the figure queries pre-named per record — variant A '
      + '"{source} {db_figure_panel} {species}", variant B '
      + '"{db_experiment_id} {db_figure_panel}" (B only when A '
      + 'returns nothing, the sweep2 shape); 12 s pacing, num=8; '
      + 'extraction verbatim-only regex over the returned snippets, '
      + 'unit conversion only into mM; the 20 records without db '
      + 'identity fields (the model-quantity leg) carry '
      + 'figure_identity_absent verdicts (disclosed); the acceptance '
      + 'predicate lives in the Python module (exp203\'s census), '
      + 'not here'),
    endpoint: pass2.endpoint,
    script_disclosure: ('this file is sweep2\'s reimplementation with '
      + 'the figure-identity queries (08b1cfc\'s pre-registration); '
      + `the blocker vocabulary (${BLOCKERS.size} names) is derived `
      + 'from the w5b bank\'s own rows, zero hand-tuning; resume '
      + 'keeps already-swept records verbatim'),
    pass2_ok_records: pass2.records.filter(
      (r) => !r.search_error && r.n_results > 0).length,
    figure_identity_absent_ids: series.filter(
      (e) => !e.db_figure_panel && !e.db_experiment_id).map(
      (e) => e.id),
    retrieved: new Date().toISOString().slice(0, 10),
    records,
  });
  const flush = () => writeFileSync(OUT, JSON.stringify(doc(), null, 1));

  let swept = 0;
  for (let i = 0; i < series.length; i++) {
    const e = series[i];
    if (done.has(e.id)) { records.push(done.get(e.id)); continue; }
    // figure-identity-absent records: the pass is vacuous for them
    if (!e.db_figure_panel && !e.db_experiment_id) {
      const r2 = pass2.records.find((r) => r.id === e.id);
      records.push({
        index: i, id: e.id,
        query: null, query_pass: 'figure_identity_absent',
        figure_identity_absent: true,
        carried_from_pass2: true,
        pass2_extracts: (r2 ? r2.extracts.length : 0),
        retrieved: new Date().toISOString().slice(0, 10),
        search_ok: false, search_error: null, n_results: 0,
        sources_tried: [], extracts: [] });
      flush();
      continue;
    }
    const { a, b } = figureQueries(e);
    await sleep(PACING_MS);
    const verdict = { index: i, id: e.id, query: a,
                      query_pass: 'figure_a',
                      retrieved: new Date().toISOString().slice(0, 10),
                      search_ok: false, search_error: null, n_results: 0,
                      sources_tried: [], extracts: [],
                      carried_from_pass2: false };
    try {
      const items = await search(zai, a);
      verdict.search_ok = true;
      verdict.n_results = items.length;
      verdict.sources_tried = items;
      for (const it of items)
        verdict.extracts.push(...extract(it.snippet, it));
    } catch (err) {
      verdict.search_error = String(err).slice(0, 220);
    }
    // variant B, only for records variant A returned nothing for
    if (!verdict.search_ok || verdict.n_results === 0) {
      await sleep(PACING_MS);
      const v2 = { ...verdict, query: b, query_pass: 'figure_b',
                   extracts: [], sources_tried: [], n_results: 0,
                   search_ok: false, search_error: null };
      try {
        const items = await search(zai, b);
        v2.search_ok = true;
        v2.n_results = items.length;
        v2.sources_tried = items;
        for (const it of items)
          v2.extracts.push(...extract(it.snippet, it));
      } catch (err) {
        v2.search_error = String(err).slice(0, 220);
      }
      records.push(v2);
    } else {
      records.push(verdict);
    }
    swept += 1;
    console.log(`  [${e.id}] fig ok=${verdict.search_ok || false} `
      + `n=${verdict.n_results} extracts=${verdict.extracts.length}`);
    flush();
  }

  writeFileSync(OUT, JSON.stringify(doc(), null, 1));
  const okN = records.filter((r) => !r.figure_identity_absent
    && r.search_ok && r.n_results > 0).length;
  console.log(`deposited ${OUT}: ${records.length} records `
    + `(${noFig} figure-identity-absent, ${okN} figure-swept ok, `
    + `${swept} swept this run)`);
}

main().catch((e) => { console.error(String(e)); process.exit(3); });
