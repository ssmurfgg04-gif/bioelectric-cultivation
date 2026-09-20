# 2026-09-20 — Search wave S-3: Sephirotic edge-channel follow-ups + anatomical compiler 2026

Research-only wave. Method: 10 web searches (2 target + 8 variants; one variant
"compiler morphogenetic fields implementation 2026" returned zero results and was
relaxed to "morphogenetic field compiler implementation"), plus direct REST fetches:
Zenodo record 19042388 + its deposited `paper25_results.json`, full Zenodo
`q=Sephirotic` author audit (36 records, 2 pages), OpenAlex citation graph
(cites:W7137259214), Semantic Scholar (rate-limited; target record not indexed),
arXiv API, targeted page fetches (HackMD ok; AJOSR Cloudflare-blocked; X via
snowflake-timestamp decode). Raw JSONs retained in /tmp/s3, /tmp/s3b.

Held findings under test (unchanged unless stated per finding):
premium lives in the spec layer's committed pattern (ρ=0.86); 8-channel schema
native, five channels inert; Sephirotic 8-channel spec = Zenodo 19042388 with 7/8
channels confirmed on the stack.

---

## TARGET 1 — Sephirotic edge-channel (Zenodo 19042388)

### F1 — Target record verified; deposited results JSON fetched
- **Title:** Sephirotic Edge-Channel Correspondence in Bioelectric Morphogenesis: Eight Internal Modes Predict Eight Independent Bioelectric Channels
- **Authors:** Freeman, Carlos W. (ORCID 0009-0005-7399-3204)
- **Date:** 2026-03-16 (revision 3; latest version, parent concept 19042387)
- **Venue/URL:** Zenodo, doi:10.5281/zenodo.19042388 — https://zenodo.org/records/19042388
- **Summary:** The Sephirotic graph (11 nodes, 24 edges, λ₆ = 6/5 exact) decomposes into 3 spatial + 8 internal eigenmodes; the 8 internal modes are mapped one-to-one onto Levin-program bioelectric channels, "forced by node descriptions, not fitted"; 7/8 knockout predictions confirmed, 1 partial; null p = 3.9e-4 (3011/100000 λ-hits), combined p = 1.6e-4 (3.6σ); zero free parameters.
- **Deposits:** paper25.pdf, paper25_computation.py (19,367 B), paper25_results.json (929 B, fetched). Results JSON: internal_indices [0,1,2,4,5,7,8,9] with 8 internal eigenvalues (0 → 1.5200…), channels_mapped 8, edges_verified 8, knockout_confirmed 7, knockout_partial 1, bio_mean_pathways 5.2 ± 2.15, p_count 0.193.
- **Uptake:** 46 downloads / 50 views at fetch time.
- **(a) Testable:** YES — decisively. The exact mode indices, eigenvalues, and null-model statistics are now obtainable by direct URL; this is precisely the "mode list" the batch-13 ledger flagged as prerequisite for the pre-registered Sephirotic 8-channel test (P1). The 8-mode → 8-channel *name* mapping table lives in paper25.pdf/computation.py (fetchable).
- **(b) Opens experiment:** YES — P1 unblocked: replay their 8 internal eigenmodes against our 8-channel state schema on the graph-based Vmem stack.
- **(c) Changes findings:** NO, but sharpens two. (i) The record's own 8th channel is "partial", not failed — our held phrase "7/8 channels confirmed" should be "7 confirmed + 1 partial" when citing. (ii) Confirms the record exists exactly as held (right ID, right claim, right stats).

### F2 — Citation audit: zero third-party uptake
- **Title:** (audit) OpenAlex citing works of W7137259214
- **Authors:** —
- **Date:** fetched 2026-09-20
- **Venue/URL:** https://api.openalex.org/works?filter=cites:W7137259214
- **Summary:** cited_by_count = 2, and both citing records are Freeman's own pre-registration (10.5281/zenodo.19562649 + its duplicate version 10.5281/zenodo.19562648, 2026-04-14). Semantic Scholar: record not indexed ("not found"). Web searches for "Sephirotic edge-channel bioelectric" / "Sephirotic edge channel Zenodo 19042388" / "Sephirotic bioelectric channels" / "Kabbalah bioelectric morphology framework 2026" returned only generic bioelectricity results — nothing citing, replicating, or extending the edge-channel spec.
- **(a) Testable:** n/a (audit).
- **(b) Opens experiment:** NO.
- **(c) Changes findings:** NO — the held position stands; no replication or response exists anywhere indexed as of 2026-09-20. Notably the author's own follow-up program left the bioelectric-morphology line entirely (went to EEG/consciousness, see F3): no author-side bioelectric extension either.

### F3 — The author's broader MPFST program: honest external-test failures in the adjacent EEG domain
- **Title:** Pre-Registered Test of Sephirotic Topology Predictions for Sleep Stage EEG: One Pass, Two Fails, and Pathway-Dependent Boundary Crossing (+ 2 pre-registrations, + 6 theory/EEG series records)
- **Authors:** Freeman, Carlos W.
- **Date:** 2026-04-14 (test + pre-registrations); series 2026-03-07 → 2026-04-14
- **Venue/URL:** Zenodo 10.5281/zenodo.19563232 (test), 10.5281/zenodo.19562649 (pre-reg), 10.5281/zenodo.19564206 (pre-reg Test 2); series: 18897626 (well-posedness of the 11-field coupled fractional PDE), 19021725 (microtubule ion pumping / anesthesia, same λ=6/5), 19075942 + 19341982 (iEEG spectral exponents, near-duplicate titles), 19044607 (EEG cross-frequency coupling), 19390482 (dimensional reduction 11→2)
- **Summary:** Five zero-free-parameter MPFST predictions tested against 25,905 Sleep-EDF epochs: 1 pass (spectral-exponent ordering ρ=0.900, p=0.037), 1 partial (Mittag-Leffler dwell), 3 FAIL; failures attributed to pathway mechanism ("natural sleep uses top-down gamma collapse, not theta destabilization"). Propofol Test 2 pre-registered on Chennu 2016 (20 subjects, 4 levels, 91-channel).
- **(a) Testable:** NO on our Vmem stack directly (EEG substrate, different scale), but the *methodology* (zero-parameter spectral predictions, pre-registered pass/partial/fail, explicit null) is the same shape as ours.
- **(b) Opens experiment:** NO directly; calibration input only.
- **(c) Changes findings:** NO on the held edge-channel result, but it is the strongest credibility calibration available: the only external-data tests of MPFST predictions to date failed 3/5, run by the author himself, honestly reported. The 7/8 bioelectric knockout claim has never been touched by anyone other than the author.

### F4 — Full Zenodo "Sephirotic" corpus audit: 33/36 same author; the 3 others are esoterica
- **Title:** (audit) Zenodo q=Sephirotic, 36 records
- **Authors:** Freeman ×33; others: Ivezaj (20225605, Soyga MS 8 manuscript notes), Poernomo/Nāfidh/Nahla (20381203, "The Vessel and The Real"), Vakhtina (21966312, 2026-08-16, "The Metaphysics of the Cocoon…" — abstract art/philosophy, verified unrelated)
- **Date:** audit 2026-09-20; corpus 2026-03 → 2026-08
- **Venue/URL:** https://zenodo.org/api/records?q=Sephirotic
- **Summary:** No non-Freeman record is a bioelectric replication, response, or extension; the Sephirotic-graph idea is diffusing into grey-literature mysticism/art spaces but the edge-channel bioelectric mapping has zero scientific uptake.
- **(a) Testable:** NO. **(b) Opens experiment:** NO.
- **(c) Changes findings:** NO — reinforces F2; also flags that "Sephirotic" keyword searches will increasingly pollute with non-scientific hits (use author ORCID + record ID for future watches).

---

## TARGET 2 — Bioelectric anatomical compiler 2026

### F5 — Patni 2026: hidden-pattern inference from bioelectric changes in simulated regeneration
- **Title:** Predicting Hidden Anatomical Target Patterns from Bioelectric Changes during Simulated Tissue Regeneration
- **Authors:** Vivaan Patni (Deira International School; ORCID profile lists it alongside OpenOmicsBench / INR-Gate)
- **Date:** 2026-01 (per ResearchGate mirror; AJOSR page "by V Patni · 2026")
- **Venue/URL:** American Journal of Student Research — https://ajosr.org (full text Cloudflare-blocked; ResearchGate mirror exists; ORCID: https://orcid.org Vivaan Patni)
- **Summary:** In-silico tissue-regeneration model asking whether a hidden anatomical target pattern can be inferred from bioelectric signal changes, framed through planarian A-P polarity and anatomical homeostasis (Levin lineage; Patni also co-authored the earlier ML "cracking the bioelectric code" line).
- **(a) Testable:** YES — the closest external analogue to our spec layer: hidden-pattern inference from Vmem-domain dynamics in simulation. If methods are extractable, their protocol can be replayed on our graph stack.
- **(b) Opens experiment:** YES — replicate/benchmark their inference protocol on our 8-channel schema; compare hit rate against our committed-pattern ρ=0.86.
- **(c) Changes findings:** NO, but supplies the first external reference class for the spec-layer premium — the comparison itself is new leverage.

### F6 — HackMD explainer: expository only, possible ICML 2026 submission signal
- **Title:** The Anatomical Compiler
- **Authors:** dmarz (HackMD)
- **Date:** 2025-10-26, updated 2026-03-31
- **Venue/URL:** https://hackmd.io/@dmarz/HkoJpsSAee
- **Summary:** A long expository synthesis of Levin's anatomical-compiler vision (agential material, multiscale competency, Kriegman xenobot design-build pipeline as the de-facto "compiler" loop, "biological IDE" framing); no new implementation or math. Search index shows the page carries an "icml2026" tag — the author may be preparing a conference submission.
- **(a) Testable:** NO (no artifacts). **(b) Opens experiment:** NO.
- **(c) Changes findings:** NO. Weak lead: check the icml2026 track in ~6 months for a "compiler" paper.

### F7 — Levin's own skeptical signal (Aug 2026) toward a claimed compiler implementation
- **Title:** X post, @drichaellevin status 2091994343225618664
- **Authors:** Michael Levin
- **Date:** 2026-08-24 (snowflake-timestamp decoded)
- **Venue/URL:** https://x.com/drmichaellevin/status/2091994343225618664
- **Summary:** "I haven't looked at it yet but I'd be surprised — we've been working on this for decades and it's very hard." The reply's target could not be identified from the search index (X content unfetchable), but as of Aug 2026 Levin himself treats some claimed anatomical-compiler implementation skeptically.
- **(a) Testable:** NO. **(b) Opens experiment:** NO.
- **(c) Changes findings:** NO — reinforces the held picture: no real-world anatomical compiler exists as of late 2026; our claim is a computational spec-layer result and is not contradicted.

### F8 — Venue signal: "Bioelectric Code of Life" seminar (SEMF)
- **Title:** Bioelectric Code of Life — frontier seminar
- **Authors:** SEMF (semf.org.es)
- **Date:** 2026-03-07 (online)
- **Venue/URL:** https://semf.org.es
- **Summary:** Program explicitly bridges bioelectric control, morphogenesis, two-headed-worm setpoint rewriting, and "Anatomical Compilers" — the concept is now an organizing theme in frontier-seminar circuits, still without a concrete implementation.
- **(a) Testable:** NO. **(b) Opens experiment:** NO. **(c) Changes findings:** NO.

### F9 — Negative results (audit, protects future waves from re-searching)
- **Title:** (audit) indexed-source search for compiler implementations
- **Date:** 2026-09-20
- **Venue/URL:** arXiv API (`all:"anatomical compiler" OR all:"bioelectric compiler"` → 0 entries), OpenAlex title searches (`anatomical compiler`, `bioelectric compiler` → 0), Semantic Scholar (rate-limited/empty), repo grep (no "Kammemaier" anywhere in repo or indexed sources)
- **Summary:** No indexed paper titled under either phrase exists; the verifiable lineage is Levin-concept (Cell 2021 doi:10.1016/j.cell.2021.02.034; Bioessays 2024 doi:10.1002/bies.202400196) + Patni ML line (2023 → F5). The "Kammemaier/Levin compiler" attribution could NOT be verified in any indexed source (arXiv/OpenAlex/PMC/web) — treat the name as unconfirmed until a primary source surfaces; to our knowledge our repo's Stage-3 compiler (exp41/exp47, `cultivation/compiler/anatomy.py`, committed-pattern writes) remains the only concrete committed-pattern compiler implementation located.
- **(a) Testable:** n/a. **(b) Opens experiment:** NO. **(c) Changes findings:** NO — but corrects task framing: do not cite "Kammemaier" externally until verified.

---

## ACTIONABLE FOR THE STACK

1. **Fetch + parse the record's deposits to unblock the pre-registered P1 Sephirotic 8-channel test** (the batch-13 registered next). Direct URLs verified live: `https://zenodo.org/api/records/19042388/files/paper25_computation.py/content` and `.../paper25.pdf/content`; `paper25_results.json` already fetched this wave (internal_indices [0,1,2,4,5,7,8,9], 8 eigenvalues, knockout 7+1 partial). Extract the 8-mode → 8-channel name mapping table from paper25.pdf, then replay their zero-parameter mapping against our 8-channel state schema on the graph Vmem stack. Highest leverage: converts an open frontier into a runnable experiment with no fitting.
2. **Benchmark F5 (Patni 2026) as the first external reference class for the spec-layer premium.** Obtain the full text (ResearchGate mirror / ORCID author contact / Cloudflare-bypassing fetch), extract the simulated-regeneration hidden-pattern inference protocol, run it on our stack, and compare its hit rate to our committed-pattern ρ=0.86. If it matches, the premium is generic; if we beat it, we have a quantified external delta for the ledger.
3. **Pre-register a "partial" outcome class for our P1 run, citing F3.** The record itself scores 7 confirmed + 1 partial, and the author's own external tests failed 3/5 — so a binary pass/fail gate on our Sephirotic test would mis-score exactly the kind of outcome the series actually produces. Mirror their confirmed/partial/fail trichotomy in the experiment's gate set.
4. **Localize the record's 8th ("partial") channel against our five inert channels.** Once the mode→channel table from item 1 is in hand, check whether the partial channel is one of our inert five: if yes, the 7/8-vs-8/8 question collapses into a single targeted test on that channel; if no, our five-inert finding and their partial are independent facts worth a ledger disclosure.
5. **Set the one-URL quarterly watch (all three checks were negative today):** OpenAlex `cites:W7137259214` count (today: 2, both self), Zenodo `q=Sephirotic` for any non-Freeman bioelectric record (today: 0 of 36), arXiv/OpenAlex for "anatomical/bioelectric compiler" titles (today: 0). First uptake on any of the three should trigger a full research wave.
