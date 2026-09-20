# Research wave S-5 — Planarian bioelectric memory + BETSE updates (searched 2026-09-20)

Scope: two search targets — (1) new planarian regeneration-memory / bioelectric-memory results 2026 (D. japonica included), (2) BETSE updates relevant to the exp261 BETSE-grounded calcium-channel port (releases, Ca-ATPase / HH calcium constants, gap-junction gating, Na/K/Cl flux). Method: z-ai web_search (8 query variants), plus primary-source verification via PyPI JSON API and git (`git ls-remote`, shallow clones, tag diffs) — web snippets alone were not trusted for the BETSE verdict.

Stack context assumed (from task brief): graph-based Vmem walk with commit-noise writes; BETSE-grounded calcium channel ported in exp261, landed CA2-INERT with clean association 0.1738 < 0.5; gap-junction morphogenesis channel present.

Findings: 9 (F1–F9). Top-line BETSE verdict: **no 2026 upstream activity at all — and the channel physics our port depends on has not changed numerically since 2022**; the one thing that DID change is the repo URL.

---

## Target 1 — Planarian bioelectric memory

### F1. Hidden regenerative state in planarians: a geometric model of bioelectric memory using Tangential Action Spaces
- **Authors / date / venue**: Marcel Blattner (Applied AI Institute; solo preprint). Posted 2026-04-03 on bioRxiv. DOI: 10.64898/2026.04.01.715890.
- **URLs**: preprint full text at `https://www.biorxiv.org/content/10.64898/2026.04.01.715890v1`; code: `https://github.com/marcelbtec/tasmorpho`; arXiv precursor of the TAS framework: Blattner 2025, "Tangential Action Spaces: Geometry, Memory and Cost in..." (arXiv).
- **One-line summary**: Formulates regeneration-after-a-cut as an open path in a "Tangential Action Space", turning planarian regenerative memory into a *geometric, costed, experimentally testable* object — fragments regenerate normal gross anatomy after transient bioelectric perturbation yet carry altered re-cut outcomes (a hidden state not visible in current anatomy), with predictions about temporal profiles.
- **Relevance flags**:
  - (a) **TESTABLE against our stack — yes, directly.** The "hidden state not visible in current Vmem" claim is exactly what our commit-noise write machinery on the graph-based Vmem walk can implement (hidden register vs observable Vmem; re-cut = re-walk). Costed/geometric predictions give ready-made statistics (temporal-profile shape, not just endpoint).
  - (b) **Opens new experiment — yes** (highest-value item this wave).
  - (c) Changes current finding — no, but it *externalizes* our memory-model line: an independent 2026 theory group converged on hidden-state bioelectric memory.

### F2. "Bioelectricity, Marching on" — commentary explicitly discussing F1
- **Authors / date / venue**: Mustafa B.A. Djamgoz, Michael Levin. 2026-09-03. SAGE journal commentary (journals.sagepub.com).
- **URL**: via search result `https://journals.sagepub.com` (article "Bioelectricity, Marching on", Sep 3 2026; cites Blattner's biorxiv model by URL).
- **One-line summary**: A current field-level commentary that singles out Blattner's geometric planarian memory model as part of the state of bioelectricity — evidence the hidden-state/planarian-memory line is now field-visible, not fringe.
- **Relevance flags**: (a) not itself testable; (b) no; (c) no change, but raises the priority of F1 (Levin-lab-adjacent attention within 5 months of the preprint).

### F3. Salt exposure disrupts memory retrieval in habituation and conditioned place preference in planaria (Dugesia japonica)
- **Authors / date / venue**: T. Tazumi et al., 2026, APA journal (psycnet.apa.org record).
- **URL**: `https://psycnet.apa.org` (record "Salt exposure disrupts memory retrieval in habituation and conditioned place preference in planaria (Dugesia japonica)", Tazumi 2026).
- **One-line summary**: Ionic (salt) stress during/around training disrupts *retrieval* (not storage) of habituation and CPP memory in D. japonica — an ionic-environment manipulation that selectively damages memory read-out.
- **Relevance flags**:
  - (a) **Testable by analogy — yes.** The stack analog is an external ionic-gradient shift (Na/Cl bath change) applied at *read* time vs *write* time on the Vmem walk; our commit-noise writes make the write/read dissociation implementable.
  - (b) **Opens new experiment — yes**: a "write-time vs read-time ionic stress" arm with the retrieval-vs-storage dissociation as the registered prediction.
  - (c) no change.

### F4. Predicting hidden anatomical target patterns from bioelectric state (preregistered)
- **Authors / date / venue**: V. Patni, 2026, AJOSR (ajosr.org).
- **URL**: `https://ajosr.org` (article "Predicting Hidden Anatomical Target Patterns from...", Patni 2026).
- **One-line summary**: A preregistered junior-researcher study predicting hidden anatomical target patterns from bioelectric state, explicitly framing gap-junction / ion-pump perturbations as the levers that shift regenerative states (citing the classic planarian perturbation literature).
- **Relevance flags**: (a) testable — the stack's reader can be pointed at the same preregistered predictions as an external check; (b) marginal (low venue weight, but preregistered = cheap to compare); (c) no.

### F5. D. japonica behavioral/neurotoxicity screening wave (peripheral 2026 cluster)
- **Items**: (i) D. Ireland, 2026, Frontiers — "Rapid behavioral screening in the planarian Dugesia japonica"; (ii) R.T. Somach et al., 2026, Reproductive Toxicology — "Timing of exposure impacts how organophosphorus pesticides affect the developing brain in the planarian Dugesia japonica".
- **URLs**: `https://www.frontiersin.org` (Ireland 2026); `https://link.springer.com` (Somach 2026).
- **One-line summary**: D. japonica is being standardized as a rapid behavioral-screening organism in 2026 (pesticide neurotoxicity; exposure-timing effects) — useful strain/protocol sources, not memory-mechanism results.
- **Relevance flags**: (a) not testable against the stack; (b) marginal (protocol borrowing only: rapid screening as a template for wetlab validation of stack predictions); (c) no.

*(Secondary 2026 noise, not findings: theconsciousness.ai Sep 5 2026 retrospective "Levin's bioelectric memory line 2013→2026"; bioletric.com Aug 24 2026 blog. Both low-quality aggregator content — logged only so nobody mistakes them for primary literature. Also noted: Levin 2025 "Bioelectrical model of head-tail patterning based on cell ion channels and intercellular gap junctions" appears in the Tufts listing — recent-model context, not new this wave.)*

---

## Target 2 — BETSE

### F6. The BETSE canonical repo has MOVED: `betse/betse` → `betsee/betse`
- **Date verified**: 2026-09-20 (primary source).
- **URLs**: `https://github.com/betsee/betse` (canonical, branch `main`); old `https://github.com/betse/betse` now 404s (git ls-remote returns auth prompt = inaccessible).
- **Evidence**: PyPI `betse` metadata (`https://pypi.org/pypi/betse/json`) lists Homepage/Repository/Issues/Releases = github.com/**betsee**/betse; direct HTTP + git checks confirm old org dead.
- **One-line summary**: The task brief's cited URL `github.com/betse/betse` is stale; all BETSE URLs have moved to the `betsee` org (the GUI repo `betsee/betsee` was always there; the core simulator now lives at `betsee/betse`).
- **Relevance flags**: (a) no; (b) no; (c) **CHANGES a current finding** — any repo doc / provenance string / requirements pin still citing `betse/betse` is wrong and must be updated (cheap fix, do it before anything else).

### F7. BETSE release state: 1.5.0 (2025-04-15) is latest; NO 2026 releases or commits
- **Date verified**: 2026-09-20 (primary sources: PyPI JSON + git).
- **URLs**: `https://pypi.org/pypi/betse/json`; `https://github.com/betsee/betse` (HEAD `4bba062`, 2025-04-16 "PEP 561 x 2").
- **Evidence**: PyPI release history — 1.2.1 (2022-06-07), 1.3.0 (2022-09-15), 1.4.0/1.4.1 "The Resurrection of BETSE" (2024-09-24), **1.5.0 "It Begins with Bioelectricity" (2025-04-15)**; 1.5.1 opened (ca26640, 2025-04-15) but never released; `main` untouched since 2025-04-16.
- **One-line summary**: Upstream BETSE is dormant as of 2026-09: no 2026 release, no 2026 commit — the 1.4.x/1.5.0 waves were packaging/modernization (Hatch build, GitHub-Actions release workflow, matplotlib >= 3.10, PEP 561 py.typed), not physics.
- **Relevance flags**: (a) yes — means exp261's port is pinned against a *frozen* upstream (good for reproducibility); (b) no; (c) no change — confirms rather than undermines current findings.

### F8. BETSE channel physics verified numerically unchanged since 2022 — exp261 calcium port remains bit-valid
- **Date verified**: 2026-09-20 (primary source: tag diff in the cloned repo).
- **URL**: `https://github.com/betsee/betse` (diff `v1.2.2` → HEAD over `betse/science/channels/` + `betse/science/physics/` + `betse/science/organelles/`).
- **Evidence**: `git diff v1.2.2..HEAD` on the six channel modules (vg_ca, gap_junction, cation, vg_na, vg_k, vg_cl) and 8 physics files = **copyright-header year bumps only; zero changed numeric lines (0 lines containing `exp(...)` or any constant)**. Current constants confirmed in HEAD:
  - HH voltage-gated Ca: `Cav3p3` (T-type, Traboulsie et al. 2007: m_inf 1/(1+exp((V+45.454426)/5.073015)) etc.), `Cav2p1` (P/Q-type, Miyasho et al. 2001) — `betse/science/channels/vg_ca.py`.
  - Gap-junction gating: `alpha = lamb*exp(-A1*(V1 - gj_vthresh))`, `beta = lamb*exp(A2*(V1 - gj_vthresh))/(1 + 50*beta)`; alternative open-probability = two-Boltzmann `gj_min + (1/(1+exp((vgj+vthresh)/vgrad)) - 1/(1+exp((vgj-vthresh)/vgrad)))*gj_block` — `gap_junction.py`.
  - Ca-ATPase: thermodynamic (Gibbs/ΔG_ATP, cATP/cADP/cPi reaction-coupled) `pumpCaATP` (plasma membrane) and `pumpCaER` (SERCA, ER membrane) — `betse/science/sim_toolbox.py` + `organelles/endo_retic.py`.
- **One-line summary**: The HH calcium constants, gap-junction gating equations, and Na/K/Cl/Ca pump formulations that the exp261 BETSE-grounded calcium channel was ported from are **identical in BETSE 1.5.0 to what they were in 2022** — the CA2-INERT clean association (0.1738 < 0.5) is grounded against current upstream, and no re-port is needed.
- **Relevance flags**: (a) yes — validates the port; (b) no; (c) no change — affirmative confirmation.

### F9. External BETSE consumer: AI-driven control of bioelectric signalling
- **Authors / date / venue**: G.H. de Carvalho et al., 2025, arXiv (cited by 1).
- **URL**: `https://arxiv.org` (de Carvalho 2025, "AI-driven control of bioelectric signalling for real-time ...", uses BETSE from GitHub as the simulation substrate).
- **One-line summary**: An independent 2025 group wraps BETSE as the environment for real-time AI/RL control of bioelectric signalling — the same "simulator-as-environment for a policy" pattern as our CEM competition line (exp25).
- **Relevance flags**: (a) weakly (their control loop could be reproduced on our stack for comparison); (b) marginal; (c) no.

---

## ACTIONABLE FOR THE STACK

1. **Implement the Blattner-TAS hidden-state test on the Vmem walk** (F1). Model a cut as an open path on the cell graph; store a hidden register written by commit-noise writes that is NOT the observable Vmem; test Blattner's temporal-profile predictions on re-cut outcomes. Code exists (`marcelbtec/tasmorpho`) to port or diff against. Highest leverage: independent 2026 theory + runnable reference code + our write machinery already implements the needed dissociation.
2. **Fix all `github.com/betse/betse` references → `betsee/betse` and pin `betse==1.5.0`** (F6, F7). Stale provenance URLs are a provenance-integrity bug for every BETSE-grounded experiment (exp261 lineage). One-pass grep + docs + requirements; upstream is frozen so the pin is safe.
3. **Register the "write-time vs read-time ionic stress" experiment** (F3). Prediction: external Na/Cl gradient shift at read time degrades retrieval (association rises toward the noise floor) while the same shift at write time degrades storage — mirrors Tazumi 2026's retrieval-vs-storage dissociation; uses the commit-noise machinery as-is.
4. **Certify the gap-junction morphogenesis channel as BETSE-grounded** (F8). Run the parameter-equivalence test of our GJ channel against BETSE's two-Boltzmann open-probability (gj_min/gj_vthresh/gj_vgrad/gj_block) + alpha/beta kinetics, same as the calcium channel was certified — closes the only uncertified channel port.
5. **Add Patni 2026 preregistered hidden-target predictions as an external falsification target** (F4) — cheap: run the existing reader (n-invariant, ~0.6 mV) on the GJ/pump perturbation arms and check concordance with their preregistrations; also mine de Carvalho 2025's control-loop spec if the CEM line needs an external comparator.

*Search provenance: z-ai web_search JSON dumps for this wave kept in `/tmp/s5/` (p1–p6, b1–b5); BETSE primary verification via shallow clones in `/tmp/s5/betse_core` (tag diffs) and `/tmp/s5/pypi_betse.json`.*
