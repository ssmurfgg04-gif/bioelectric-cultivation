# 2026-09-20 — Search wave: field-mediated prepatterning (Manicka/Levin) + Cervera/Levin/Mafe Vmem→transcription

Task ID: S-4 (research-only). Methods: web-search CLI (multiple query variants per target), Crossref/PubMed
metadata confirmation, GitHub commits.atom fetch for repo activity. Stack context assumed: graph-based Vmem
pattern dynamics, 8-channel state incl. ion-channel-expression + Ca2+ channels; exp233 refuted
field-prepatterning as a 3rd channel; exp249 grounds Cervera (under repair); exp261 BETSE-grounded Ca2+
channel landed CA2-INERT.

Legend for classification: (a) = testable against our computational bioelectric stack; (b) = opens a new
experiment; (c) = changes any current finding. Yes/Maybe/No per finding.

---

## T1 — Manicka/Levin field-mediated prepatterning follow-ups

### F1. Field-mediated bioelectric basis of morphogenetic prepatterning (the anchor paper, now published)
- **Title:** Field-mediated bioelectric basis of morphogenetic prepatterning
- **Authors:** Santosh Manicka, Michael Levin
- **Date:** Oct 2025 (issue); OSF preprint first posted 2025-01-21 ("…a computational study", doi:10.31219/osf.io/kshpv; latest preprint version V17 "The bioelectric field basis of morphogenesis")
- **Venue/URL:** Cell Reports Physical Science 6, 102865, doi:10.1016/j.xcrp.2025.102865 — https://www.cell.com/cell-reports-physical-science (ScienceDirect listing); preprint: https://osf.io/kshpv
- **Summary:** Proposes that an intercellular electric field catalyzes NON-LOCAL causal interactions among cells constituting a Vmem pattern, adding a field-mediated coupling layer on top of localized non-neural bioelectric networks (gap-junction/ion-channel graph models); concludes "a bioelectric field basis of morphogenesis may indeed be viable."
- **Citations:** Crossref is-referenced-by 2; ScienceDirect shows "cited by 7" (includes preprint variants).
- **Classification:** (a) YES — this is exactly the model exp233 tested and refuted as a third channel in our graph stack. (b) No new experiment needed beyond the re-scope below. (c) NO change — the paper stands as published; exp233's refutation is a substrate-level falsification of the field-prepatternning mechanism as modeled by us, not of the paper's own code.

### F2. ElectricMorphogenesis repo active in 2026 (README model-overview update)
- **Title:** santamanicka/ElectricMorphogenesis (repo activity)
- **Authors/maintainer:** santamanicka (Manicka)
- **Date:** Last commits 2026-03-26 ("Updated README with model overview, structure, and usage guide"; "Corrected paper reference in README"); 371 commits total
- **Venue/URL:** https://github.com/santamanicka/ElectricMorphogenesis
- **Summary:** The reference implementation for field-mediated prepatterning received a maintenance/documentation pass in March 2026 — a README "model overview, structure, and usage guide" — but no new model version is evident from the commit titles.
- **Classification:** (a) YES — it is the reference implementation our graph stack approximates. (b) YES — cheap one-off: diff their documented model structure/parameters against our exp233 field-coupling implementation. (c) MAYBE — if their README discloses structure or parameters our exp233 did not cover, exp233's refutation scope needs a disclosure/rescoping note (or the refutation strengthens if we did cover it).

### F3. Lifetime imaging of Vmem patterns: three timescales + long-distance non-neural patterns (empirical)
- **Title:** Lifetime imaging reveals long-distance non-neural bioelectric patterns on timescales from seconds to hours
- **Authors:** Patrick McMillen, Michael Levin
- **Date:** 2026 (issue Nov 2026; online ~Aug 2026; PMID 42556770). Companion preprint: "The neural crest as a bioelectric Rosetta Stone" (OSF, 2025-03-20, doi:10.31219/osf.io/ncx84_v1)
- **Venue/URL:** Developmental Biology, doi:10.1016/j.ydbio.2026.08.001 — https://pubmed.ncbi.nlm.nih.gov/42556770/
- **Summary:** Fluorescence-lifetime (Vmem-oe) imaging of migrating neural crest for 17+ h shows bioelectric patterns with distinct seconds-, minutes-, and hours-scale components spanning long distances — the first dense empirical timescale decomposition of endogenous Vmem pattern dynamics in a non-neural collective.
- **Classification:** (a) YES — empirical targets for our graph-based Vmem pattern dynamics (temporal components, spatial span). (b) YES — a calibration/validation experiment: fit our stack's pattern dynamics to the published three-component decomposition. (c) MAYBE — if our stack's walk/smoothing timescales (exp112/135, exp226 smoothing bound) are inconsistent with the observed hours-scale slow component, the boundary-residual interpretation needs revisiting.

### F4. Levin 2026 — "Ingressing Patterns of Life" (conceptual companion)
- **Title:** Ingressing Patterns of Life
- **Authors:** Michael Levin
- **Date:** 2026
- **Venue/URL:** Chapter in *Ingressing Minds* (see https://drmichaellevin.org, https://philarchive.org)
- **Summary:** Philosophical framing of anatomical pattern origin/persistence that places the 2025 field-prepatterning line inside a broader pattern-realist agenda; no new models or data.
- **Classification:** (a) NO. (b) NO. (c) NO. Record only for citation hygiene.

---

## T2 — Cervera/Levin/Mafe Vmem→transcription follow-ups

### F5. Top-down perspectives on cell membrane potential and protein transcription (the exp249 anchor, now published)
- **Title:** Top-down perspectives on cell membrane potential and protein transcription
- **Authors:** Javier Cervera, Michael Levin, Salvador Mafe
- **Date:** Online 2025-12-10; volume year 2026 (Sci Rep 16, 1996; PMID 41372487; Crossref cited-by 4, ~5 elsewhere)
- **Venue/URL:** Scientific Reports 16:1996, doi:10.1038/s41598-025-31696-6 — https://www.nature.com/articles/s41598-025-31696-6
- **Summary (from fetched abstract):** Top-down multicellular model (voltage-gated ion channels + junctions) making three explicit predictions: (i) shifts in membrane potential allow transitions between gene-expression states; (ii) with different potential-gated transcription programs, DEPOLARIZED cells control distinct gene expressions LESS effectively than polarized cells; (iii) community effects extend single-cell control to the multicellular level — a central cell "measures" neighbor number and learns neighbors' bioelectrical states via downward-induced Vmem changes.
- **Classification:** (a) YES — all three predictions map onto the 8-channel stack (Vmem reader, ion-channel-expression channel, degree/neighborhood structure). (b) YES — prediction (ii) is a one-arm test (controllability asymmetry vs Vmem sign); (iii) is a neighbor-count readout test (our degree ladder lineage). (c) NO change — confirms exp249's grounding is current; the published version's explicit predictions should be encoded in the repair.

### F6. Oscillatory Vmem ↔ ion-channel-protein transcription (new: Physica D 2026)
- **Title:** Oscillatory cell membrane potentials and ion channel protein transcription: a biophysical model
- **Authors:** Egea-Carro, Mafe, Cervera (NEW first author entering the Cervera/Mafe line)
- **Date:** Aug 2026
- **Venue/URL:** Physica D: Nonlinear Phenomena, doi:10.1016/j.physd.2026.135209 — https://doi.org/10.1016/j.physd.2026.135209
- **Summary:** Models the feedback loop where channel-protein expression drives membrane potential and Vmem in turn gates transcription of channel proteins, yielding oscillatory cell potentials — i.e., the transcription coupling lives (at least partly) in an oscillatory regime rather than a purely bistable one.
- **Classification:** (a) YES — this loop is literally our ion-channel-expression channel coupled to Vmem dynamics. (b) YES — a regime scan: bistable-vs-oscillatory phase boundary in the graph stack with expression feedback. (c) MAYBE — if the Cervera grounding only holds in the oscillatory regime, exp249's repair must use oscillation-capable dynamics (relevant to our equilibrium work exp26).

### F7. miRNA-driven bioelectrical regionalization (new: J. Chem. Phys. 2026)
- **Title:** Bioelectrical regionalization of multicellular aggregates by microRNAs
- **Authors:** Egea-Carro, Mafe, Levin, Cervera
- **Date:** 2026-08-06
- **Venue/URL:** The Journal of Chemical Physics, doi:10.1063/5.0345058 — https://pubs.aip.org
- **Summary:** miRNAs modulate ion-channel protein expression, converting uniform aggregates into polarized/depolarized regionalized bioelectrical patterns — a genetically-anchored WRITE mechanism for Vmem patterns (context-dependent effects of spatially regionalized signaling biomolecules).
- **Classification:** (a) YES — miRNA dose = a knob on our ion-channel-expression channel. (b) YES — expression-suppression sweep as a write-path intervention. (c) NO change; supplies a literature-grounded mechanism for the surviving write-path repair branch (exp221 lineage).

### F8. Device-side perspective incl. Vmem→Ca2+→transcription (Advanced Materials Interfaces 2026)
- **Title:** Bioelectrical Interfaces Beyond Excitable Cells: Cancer, Aging, and Gene Expression Modulation
- **Authors:** P. Cadinu, …, M. Levin, R. Moreddu (14 authors)
- **Date:** 2026-04-08 (arXiv:2504.00872, Apr 2025)
- **Venue/URL:** Advanced Materials Interfaces, doi:10.1002/admi.202500999 — https://advanced.onlinelibrary.wiley.com; preprint https://arxiv.org/abs/2504.00872
- **Summary:** Perspective on bioelectronic devices for non-excitable cells: membrane potential dynamics regulate gene expression via calcium flux and transcription-factor activation — a device-level statement of the same Ca2+-mediated Vmem→transcription route our stack encodes.
- **Classification:** (a) PARTIAL — review-level; motivates but does not test the Ca2+ arm. (b) MARGINAL — supports a future interface/delivery arm (our delivery line exp179) more than a core mechanism test. (c) NO — no contradiction with exp261's CA2-INERT result; the paper asserts Ca2+ flux importance in vivo, which only sharpens the need to explain why our BETSE-grounded Ca2+ channel was inert (disclosed caveat, not a change).

### F9. Baseline context: deterministic + stochastic adaptation models (Cervera et al. 2024)
- **Title:** Multicellular adaptation to electrophysiological perturbations analyzed by deterministic and stochastic bioelectrical models
- **Authors:** Javier Cervera, Michael Levin, Salvador Mafe
- **Date:** 2024 (received 2024-08-03)
- **Venue/URL:** Scientific Reports 14 (PMC: https://pmc.ncbi.nlm.nih.gov — cited by 13)
- **Summary:** Deterministic and stochastic treatments of multicellular electrophysiological adaptation — the methodological baseline on which the 2026 trio (F5–F7) builds; noise-aware modeling precedent.
- **Classification:** (a) YES as methodological precedent (stochastic vs deterministic agreement checks). (b) NO new. (c) NO.

---

## ACTIONABLE FOR THE STACK (≤5, ranked by leverage)

1. **Re-scope exp233 against the ElectricMorphogenesis README (2026-03-26 "model overview" update).** Diff their documented model structure/parameters vs our field-coupling implementation; either extend the exp233 refutation scope with a disclosure, or strengthen it (did-we-cover-their-model check). Cheapest action; protects/clarifies an existing ledger entry (F2).
2. **Upgrade exp249's grounding to the published Cervera et al. 2026 (Sci Rep 16:1996) and pre-name its three predictions as arms:** (i) Vmem-shift → gene-expression-state transition, (ii) polarized-vs-depolarized transcription-controllability asymmetry, (iii) community effects / neighbor-count readout. Prediction (ii) is a near one-day arm on the 8-channel state (F5).
3. **New experiment — expression→Vmem oscillation regime scan (Physica D 2026):** with ion-channel-expression feedback armed, map the bistable-vs-oscillatory phase boundary and compare to exp26 equilibrium points; determines whether the Cervera coupling requires oscillation-capable dynamics in the exp249 repair (F6).
4. **Temporal calibration to McMillen & Levin 2026 (Dev Biol):** fit the stack's Vmem pattern dynamics to the published seconds/minutes/hours three-component decomposition and long-distance spans; stress-tests exp226's smoothing bound and exp112/135 walk-speed regimes against real data (F3).
5. **Write-path arm — miRNA regionalization (JCP 2026):** channel-expression suppression as a literature-grounded write intervention on the surviving write-path repair branch (exp221 lineage), with dose → regionalization readout (F7).

*Non-actionable:* F1/F4/F8/F9 recorded for citation hygiene and context only.

— End of report. Sources checked: web-search (13 queries), Crossref API, PubMed E-utilities, Nature.com abstract fetch, GitHub commits.atom.
