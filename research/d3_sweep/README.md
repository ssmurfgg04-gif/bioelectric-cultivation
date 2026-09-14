# D3 research sweep — the write semantics of cell death (2026-09)

Sixteen web searches grounding `cultivation/bioelectric/senescence_semantics.py`
(exp16). Raw JSON results in this directory (`q*.json`). The sweep answered
one question — *what does the literature say is actually written when a cell
dies?* — and its answer is the module's design.

## The five facts that decided the design

1. **Death is an instant broadcast.** Injury produces immediate tissue-scale
   membrane-depolarization gradients and calcium waves (Zhao 2022 — wound
   electric fields arise instantaneously and persist until the barrier
   recovers; 2025 injury-induced electrochemical coupling). The dying cell
   does not die silently. → the `broadcast` semantics' decaying drive.

2. **The broadcast is written into neighbors through gap junctions.** The
   bystander effect: senescent cells induce senescence markers (DNA damage
   response) in junction-coupled neighbors ("A senescent cell bystander
   effect"; Decrock et al. 2009 — gap junctions propagate death AND survival
   signals; Cusato et al. 2003 — retinal bystander killing; Spray et al.
   2012); SASP paracrine spreading is cell-type-specific and directional
   (2026 characterization papers). Senescence is contagious through the
   state, not just the hazard. → `broadcast` is state-level, and the
   neighbors' consensus anchoring must survive it (the v2 latch's job).

3. **What propagates is the death signal, not the pattern.** Nothing in the
   bystander/SASP literature shows the dying cell's *pattern information*
   being copied into survivors; what propagates is depolarization + secreted
   damage signals. In planarians, dying cells trigger AiP (apoptosis-induced
   proliferation) and the new tissue takes its patterning cues from the
   surviving collective bioelectric state + genomic prepattern. → the
   transcription semantics is the *hypothesis under test* (the star's naive
   form), not the literature default.

4. **The pattern survives death distributedly.** Bistable somatic pattern
   memories persist in planarian tissue >1 week without reinforcement
   (Pezzulo & Levin 2021); the genomic archive encodes per-cell positional
   identity (the re-derivation source); the collective bioelectric state is
   the working copy. → the ledger's two carriers (V, anchor) + archive, and
   the "stasis/frozen anchor" recoverability semantics.

5. **The coupling is bidirectional.** Bioelectric state controls the death
   program: H+,K+-ATPase regulates apoptosis-mediated tissue remodeling
   during planarian regeneration (Beane et al. 2013, Development 140:313).
   Gap-junction decline is itself an integral indicator of aging (connexin
   43 loss across heart/liver/bone; planarian innexins — Oviedo 2009,
   Nogi 2007 smedinx-11, Peiris 2013 — are load-bearing for regeneration).
   → the junction-gated latch and the quarantine/broadcast trade-off.

## Field positioning found by the sweep

- **Aging as loss of morphostatic information** (Pio-Lopez, Levin et al.
  2024): the direct theoretical framing of this repo's fidelity clock.
- **Computational SOTA**: Manicka et al. 2025 (field-mediated bioelectric
  morphogenesis models); Hansali et al. 2025 (review: computational modeling
  of bioelectric propagation). None connect Vmem dynamics to
  information-theoretic mortality + AI-driven intervention discovery with
  falsification controls — that intersection is this repo's unique ground.
- **AI control of bioelectric signaling** exists as a 2025 preprint program
  (real-time control framing) — the tower's exp10-14 (CEM/GA inverse design
  + controls) is the quantitative version of that agenda.
- **Vm from transcriptomics is established method** (Tripathy et al. 2017;
  Bernaerts et al. 2025; Huang et al. 2025): L1-regularized expression ->
  resting potential. Applied here to planaria via
  `cultivation/validation/vmem_inference.py`.
- **Public datasets for the no-wetlab program**: Fincher et al. 2018
  (S. mediterranea cell-type atlas), the Rajewsky-lab PSCA, PLANOSPHERE
  (Stowers), Raz et al. 2021, the 2025 allometry atlas — the predicted-Vmem
  pipeline is ingest-ready for all of them.

## What the sweep changed in the model

| Sweep fact | Model change (exp16) |
|---|---|
| bystander effect is gap-junction-mediated | `broadcast` drive scales with junction conductance |
| wound fields persist until recovery | `broadcast_tau` decay (not a one-shot impulse) |
| pattern survives in bistable somatic memories | `stasis` semantics: senesced cells' anchors freeze (recoverable) |
| nothing shows pattern transcription | `transcription` kept as the tested-and-rejected star hypothesis |
| connexin decline is aging-integral | the junction-gated matched-channel latch (the D3 law) |
| H,K-ATPase controls the death program | vmem_inference's V2 falsifiable prediction |
