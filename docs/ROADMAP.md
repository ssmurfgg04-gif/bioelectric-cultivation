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

## Next science (each must be pre-registered first)
- **P3′:** an exponential burden-to-hazard link `k·(exp(c·burden) − 1)`; require elasticity(h_sys) ≥ 0.5.
- **P1 robustness beyond seeds:** a Sobol sweep over γ, g, ε, μ and σ. Report where memory is lost (the phase boundary in ε/γ).
- **P4 candidate:** "aging = information loss", tested against a noise-matched null with intact coupling.
