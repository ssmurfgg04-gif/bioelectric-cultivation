# Roadmap (updated 2026-11-16, after phases 1–5)

## Done
- [x] **Review fixes:** truncated Gompertz MLE, exp447, claims audit, honest README (PR #1)
- [x] **Phase 1:** primaries P1–P3 frozen before running (`docs/PRIMARIES.md`, commit 6d64990)
- [x] **Phase 2:** 20-seed runs with CIs, ablation (ε = 0), GJ control, dose arm and Holm correction. P1 PASS, P2 PASS (`docs/PRIMARY_RESULTS.md`)
- [x] **Phase 3:** P3 Gompertz repair tested: FAIL, cause diagnosed (saturating hazard). Units table (`docs/UNITS.md`). Dormant-channel decision recorded
- [x] **Phase 4:** data audit (no absolute planarian mV exists); four falsifiable wet-lab predictions W1–W4 (`docs/DATA_CONTACT.md`)
- [x] **Phase 5:** draft preprint (`paper/preprint.md`), `CITATION.cff`, `.zenodo.json`, `experiments/INDEX.md`

## Needs Jack (cannot be done from code)
- [ ] **Post the preprint.** Read `paper/preprint.md`, add your full name and affiliation, and submit it to bioRxiv or arXiv (q-bio.TO).
- [ ] **Zenodo DOI.** Connect the GitHub repo at zenodo.org → GitHub, then publish a release `v0.3.0`. `.zenodo.json` is ready.
- [ ] **Wet-lab collaborator.** Send W1–W4 plus the protocol doc to a planarian lab. W4 is the novel test.
- [ ] **Shrink the repo.** Approve a history rewrite (`git filter-repo`) to move `results/` (54 MB) and `research/data` (18 MB) to a Zenodo record.

## Round 2 done (docs/PRIMARY_RESULTS_ROUND2.md)
- [x] P5 robustness: PASS (ε cliff found)
- [x] P4 information loss: PASS, narrowed
- [x] P3′ odds link: FAIL, root cause = stochastic single-onset

- [x] **P7** (round 4): escape in the model needs state + clock repair; synergy found
- [x] README cut to 65 lines; the night-by-night log moved to docs/HISTORY.md; censoring-aware median added

## Next science (each must be pre-registered first)
- [x] **P8/P9** (round 5): frontier = ≥75% every 10 yr; the noise clock carries the effect, junction loss is irrelevant
- **Next: P10.** In the current model, noise growth is purely time-driven (σ₀·e^{κt}) *by construction*, so state repair cannot touch it. P10 would add a feedback (noise grows with accumulated damage) and test whether state repair alone then slows the noise clock. That would decide whether a separate noise-reset therapy is needed.
- [x] **P6** (round 3): ε × exposure-time threshold. PASS, with collapse at ε·T ≈ 0.65
- **P3″:** a redundant-subsystem (reliability-theory) aging structure, as the only credible route to a rate-setting mechanism.
