# Task 10 sweep — the search-first directive in action

Standing order adopted this session (user directive): **before any new
computation or wet-lab stage, search the literature for the existing
answer.** This sweep grounded the three tasks: the PSCA ingest, the
century-hold CEM re-run, and the fidelity-clock experiment design.

## Queries (12 + 3 follow-ups)

| # | Query | What it found |
|---|---|---|
| q1 | PSCA download access | shiny.mdc-berlin.de/psca exposes the raw data files (dge.txt.gz, annotations, loom) on bimsbstatic.mdc-berlin.de — THE ingestion path |
| q2 | Fincher atlas download | bis.zju.edu.cn mirror of GSE111764 (50,456 cells) + digiworm browser |
| q3 | ion channel expression in atlases | the atlas landscape (PSCA/Fincher/PlanExp/PLANOSPHERE/STAPR/allometry 2025) |
| q4 | Vm from transcriptomics method | Tripathy 2017 (PNAS correlation maps), 2024 bioRxiv L1-regularized models, PREPS 2026 — the method class |
| q5 | GHK permeability inference | the mechanistic alternative used here |
| q6 | neoblast membrane potential | the stemness-hyperpolarization program (V1's ground truth) |
| q7 | CEM maintenance objectives | no direct precedent for century-hold fitness — genuinely open (exp19's contribution) |
| q8 | planarian innexin genes | Nogi 2005/2007, Oviedo 2009, Peiris 2013, the Frontiers 2018 innexin review (FC3 grounding) |
| q9 | voltage dyes planaria | the DiBAC4(3) live-imaging protocol, PMC10468776 / PMID 21356693 (FC1's measurement layer) |
| q10 | bystander effect dye transfer | Decrock 2009, Cusato 2003, Spray 2012 (FC3's coupling assay) |
| q11 | injury depolarization waves | Chifflet 2005 (leading-edge depolarization), Liu 2026 (depolarization gradient precedes Ca2+ wave) |
| q12 | bioelectric aging clock experiments | no existing fidelity-clock experiment — the FC1-FC5 gap is real |
| q13-q15 | planarian gene DBs | PlanMine (unreachable from sandbox), SmedGD retired → planosphere pub files: the Rosetta Stone + AHRD annotations that CLOSED the gene-ID gap |

## The two answers the search saved us from rediscovering

1. **The gene-ID mapping existed.** The dd_Smed_v6 -> SMED300 ->
functional-annotation chain (planosphere /pub/analysis/rosetta/ +
/pub/analysis/ahrd/) gave the full ion-transporter family inventory
(82 innexin AHRD entries, Na/K-ATPase, K2P/kv/k_ca K+ channels, TRPM/TRPA,
P2X, FaNaC, anoctamin/ClC) — mining this beat a from-scratch BLAST.
2. **The voltage-dye protocol existed.** DiBAC4(3) whole-mount planarian
Vmem imaging is a published, citable protocol — the fidelity clock's
measurement layer is a reproduction, not an invention.

## What was genuinely open (and this session's work)

- No existing test of V1-V4 against atlas data (exp18 ran it: V1 confirmed,
  V2/V4 refuted, V3 split)
- No century-hold CEM objective precedent (exp19: law rediscovered,
  plateau landscape)
- No fidelity-clock experiment design (FC1-FC5, pre-registered in
  docs/FIDELITY_CLOCK.md)
