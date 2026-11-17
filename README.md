# bioelectric-cultivation

> ## Status (2026-11-16): exploratory simulation toolkit, claims under audit
>
> This repository is a **simulation toolkit plus a set of open
> hypotheses**. It is not a completed result. An external review
> ([docs/CLAIMS_AUDIT.md](docs/CLAIMS_AUDIT.md)) re-checked the headline
> claims:
>
> - **Stands:** the Level-1 qualitative reproductions (planarian
>   two-head memory, cancer normalisation), the Gompertz *form* of
>   emergent mortality, and the RS/GF(256) codec layer.
> - **Withdrawn:** "β ≈ 0.09/yr, the human range". With the
>   truncation-corrected fit, β = 0.054 and no model parameter controls
>   it (exp447). Also withdrawn: the cross-species ρ = 1.00 (the presets
>   are ordered by lifespan by construction) and the stage percentages.
> - **Narrowed:** the "human extension" runs on HCP *functional
>   connectivity*, not a connectome. It is a graph-robustness test, not
>   evidence of human transfer.
> - **Post-hoc:** exp443's calibrated falsifier is tautological. d-02
>   failed its original gate (exp437).
>
> **Pre-registered primaries** ([docs/PRIMARY_RESULTS.md](docs/PRIMARY_RESULTS.md)):
> P1 target memory **PASS** (20/20 seeds; θ plasticity necessary);
> P2 sustained > dose-matched one-shot maintenance **PASS**
> (×1.087 vs ×1.044); P3 Gompertz-rate repair **FAIL** (diagnosed).
> Round 2 ([docs/PRIMARY_RESULTS_ROUND2.md](docs/PRIMARY_RESULTS_ROUND2.md)):
> P5 memory robust to parameters **PASS** (only ε matters); P4 information
> loss beyond noise **PASS, small** (+0.08 bits; noise explains 92%);
> P3′ odds-link Gompertz repair **FAIL** (single-onset dynamics).
> Round 3: P6 memory threshold = plasticity × exposure time **PASS**
> (collapse at ε·T ≈ 0.65; [docs/PRIMARY_RESULTS_ROUND3.md](docs/PRIMARY_RESULTS_ROUND3.md)).
> Round 4: P7 negligible senescence in the model needs **both** state
> repair and clock repair. Either alone adds ~25–30 yr; both every 10 yr →
> 83% alive at 300 yr ([docs/PRIMARY_RESULTS_ROUND4.md](docs/PRIMARY_RESULTS_ROUND4.md)).
> Round 5: the synergy is state × **noise** (junction loss is irrelevant to
> lifespan); escape needs ≥75%-complete repair every 10 yr
> ([docs/PRIMARY_RESULTS_ROUND5.md](docs/PRIMARY_RESULTS_ROUND5.md)).
> Round 6: even if 90% of noise is damage-driven, damage repair alone
> reaches only 47% alive at 300 yr. P10 **FAIL** (near miss); a noise
> reset is still needed ([docs/PRIMARY_RESULTS_ROUND6.md](docs/PRIMARY_RESULTS_ROUND6.md)).
> Draft preprint: [paper/preprint.md](paper/preprint.md).
>
> Earlier status banners ("PROJECT COMPLETE", "101% PASSED") are retired.
> The roadmap is in [docs/ROADMAP.md](docs/ROADMAP.md).
> **Run:** `python3 -m tests.run_tests`.

**A computational research framework for bioelectric morphogenesis, aging-as-attractor-degradation, and inverse design of bioelectric interventions.**

## What's here
- `cultivation/`: the library. Coupled V/θ cell collectives, the aging cohort model, information measures, and the Reed–Solomon/GF(256) coding layer.
- `experiments/`: start from [experiments/INDEX.md](experiments/INDEX.md). The pre-registered primaries are exp448–exp457. Everything below exp447 is the exploratory record.
- `docs/`:
  - [PRIMARIES*.md](docs/PRIMARIES.md): frozen hypotheses and gates.
  - [PRIMARY_RESULTS*.md](docs/PRIMARY_RESULTS.md): the results against those gates.
  - [CLAIMS_AUDIT.md](docs/CLAIMS_AUDIT.md): what stands and what was withdrawn.
  - [UNITS.md](docs/UNITS.md): units and scales.
  - [DATA_CONTACT.md](docs/DATA_CONTACT.md): wet-lab predictions W1–W5.
  - [ROADMAP.md](docs/ROADMAP.md): what's next.
- `paper/preprint.md`: draft preprint.
- [docs/HISTORY.md](docs/HISTORY.md): the original night-by-night research log (historical, unaudited).

## Run
```bash
pip install -r requirements-lock.txt
python3 -m tests.run_tests
python3 -m experiments.exp448_p1_target_memory   # any primary
```

## Rules
Confirmatory claims are pre-registered: gates are committed before the run and never edited afterwards. Everything else is exploratory. See docs/PRIMARIES.md.
