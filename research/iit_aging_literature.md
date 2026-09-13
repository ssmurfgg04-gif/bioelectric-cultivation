# Literature Dossier — Integrated Information Theory (Φ), Information-Theoretic Aging Theory, and Meditation/Neural Integration

**Compiled by:** Research Agent R-2 · **Date:** 2026-09-13
**Purpose:** Verified bibliography for a computational project that models aging as loss of information-integrity in a bioelectric control network and computes Φ approximations for coupled neural/bioelectric systems.

**Verification method.** Every entry below was verified against live API responses from **Crossref** (`api.crossref.org/works`, bibliographic queries + direct DOI lookups) and **PubMed eutils** (`esearch.fcgi` / `esummary.fcgi`). DOIs are copied verbatim from API responses (never from memory). Citation counts (`cited N×`) are Crossref `is-referenced-by-count` on the run date. Semantic Scholar, OpenAlex, and the arXiv export API were rate-limited (HTTP 429) during this run and were not needed. Notes on corrections vs. the commissioning brief are collected at the end of each theme and in the "Corrections" section.

**Entry count:** 47 verified entries (19 IIT / 19 aging / 5 meditation / 2 bioelectric / 2 supplementary IIT-computation). Leads that could not be verified are listed at the end.

---

## Theme (a) — Integrated Information Theory: core theory, computable approximations, critiques

### A.1 Core theory (what our approximations approximate)

1. **An information integration theory of consciousness** — Tononi G. (2004). *BMC Neuroscience* 5(1):42. DOI: `10.1186/1471-2202-5-42` — https://doi.org/10.1186/1471-2202-5-42 — cited 1310×.
   Relevance: Founding statement of IIT — consciousness is integrated information, with Φ defined via the minimum-information bipartition and effective information. This is the conceptual anchor for the project's premise that a bioelectric control network's "intrinsic information capacity" is what aging erodes.

2. **Measuring information integration** — Tononi G.; Sporns O. (2003). *BMC Neuroscience* 4(1):31. DOI: `10.1186/1471-2202-4-31` — https://doi.org/10.1186/1471-2202-4-31 — cited 211×.
   Relevance: Introduces effective information and bipartition-based integration measures computable on actual connectivity matrices — the first *practical* Φ-style metric and the direct ancestor of our network-degradation computations.

3. **Integrated Information in Discrete Dynamical Systems: Motivation and Theoretical Framework** — Balduzzi D.; Tononi G. (2008). *PLoS Computational Biology* 4(6):e1000091. DOI: `10.1371/journal.pcbi.1000091` — https://doi.org/10.1371/journal.pcbi.1000091 — cited 301×.
   Relevance: Extends Φ to discrete Markovian dynamical systems and defines the "main complex" — the machinery needed to treat coupled neural/bioelectric units as a *time-evolving* system rather than a static graph.

4. **From the Phenomenology to the Mechanisms of Consciousness: Integrated Information Theory 3.0** — Oizumi M.; Albantakis L.; Tononi G. (2014). *PLoS Computational Biology* 10(5):e1003588. DOI: `10.1371/journal.pcbi.1003588` — https://doi.org/10.1371/journal.pcbi.1003588 — cited 829×.
   Relevance: IIT 3.0 reformulates Φ as irreducibility of the cause-effect structure (cause-effect repertoires, QEMU/CORE). Defines the modern Φ our proxies stand in for, and explicitly motivates approximations because exact Φ is super-exponentially hard.

5. **Integrated information theory (IIT) 4.0: Formulating the properties of phenomenal existence in physical terms** — Albantakis L.; Barbosa L.; Findlay G.; Grasso M.; Haun A. M.; Marshall W.; Mayner W. G. P.; Zaeemzadeh A.; Boly M.; Juel B. E.; Sasai S.; Fujii K.; David I.; Hendren J.; Lang J. P.; Tononi G. (2023). *PLOS Computational Biology* 19(10):e1011465. DOI: `10.1371/journal.pcbi.1011465` — https://doi.org/10.1371/journal.pcbi.1011465 — cited 233×.
   Relevance: The current canonical formulation (intrinsic existence; Φ as intrinsic irreducibility over cause-effect power). Cite this as the formal reference when describing what our computable proxies approximate. **Note: first author is Albantakis (Tononi is last author), and it is a 2023 PLOS Comput Biol paper, not a preprint.**

### A.2 Computable Φ measures, Gaussian/linear approximations, toolboxes

6. **A measure for intrinsic information** — Barbosa L. S.; Marshall W.; Streipert S.; Albantakis L.; Tononi G. (2020). *Scientific Reports* 10(1):18803. DOI: `10.1038/s41598-020-75943-4` — https://doi.org/10.1038/s41598-020-75943-4 — cited 38×.
   Relevance: Introduces **Φ_R**, a principled yet tractable intrinsic-integration measure computed via "soft" perturbations (Lebesgue-measure interventions) — one of the best candidate Φ approximations to implement directly on coupled systems. **Note: exact title is "A measure for intrinsic information" (not "intrinsic integration") and the year is 2020 (not 2021).**

7. **Mechanism Integrated Information** — Barbosa L. S.; Marshall W.; Albantakis L.; Tononi G. (2021). *Entropy* 23(3):362. DOI: `10.3390/e23030362` — https://doi.org/10.3390/e23030362 — cited 46×.
   Relevance: Defines mechanism-level integrated information (MII) — irreducibility of small mechanisms rather than whole systems. Useful for node-level (as opposed to system-level) integration accounting in our aging network model.

8. **PyPhi: A toolbox for integrated information theory** — Mayner W. G. P.; Marshall W.; Albantakis L.; Findlay G.; Marchman R.; Tononi G. (2018). *PLOS Computational Biology* 14(7):e1006343. DOI: `10.1371/journal.pcbi.1006343` — https://doi.org/10.1371/journal.pcbi.1006343 — cited 93×.
   Relevance: The reference open-source implementation of IIT 3.0 Φ for discrete Markov systems — the natural benchmark/validation target for any custom Φ approximation code we write. **Note: venue is PLOS Computational Biology, not PLoS ONE.**

9. **Practical Measures of Integrated Information for Time-Series Data** — Barrett A. B.; Seth A. K. (2011). *PLoS Computational Biology* 7(1):e1001052. DOI: `10.1371/journal.pcbi.1001052` — https://doi.org/10.1371/journal.pcbi.1001052 — cited 178×.
   Relevance: **THE paper for a Gaussian-linear Φ implementation**: derives Φ_EI and Φ_ar for multivariate Gaussian/linear systems via Granger-causality-style effective-information perturbations, with careful caveats on empirical estimation bias. Our linear-system Φ code should follow its equations.

10. **Unified framework for information integration based on information geometry** — Oizumi M.; Tsuchiya N.; Amari S. (2016). *Proceedings of the National Academy of Sciences* 113(51):14817–14822. DOI: `10.1073/pnas.1603583113` — https://doi.org/10.1073/pnas.1603583113 — cited 131×.
    Relevance: Information-geometric integration measures (the Φ* family) with analytic treatment for Gaussian systems — a second, geometry-grounded route to linear-system Φ that pairs well with #9.

11. **A general spectral decomposition of causal influences applied to integrated information** — Cohen D.; Sasai S.; Tsuchiya N.; Oizumi M. (2020). *Journal of Neuroscience Methods* 330:108443. DOI: `10.1016/j.jneumeth.2019.108443` — https://doi.org/10.1016/j.jneumeth.2019.108443 — cited 13×.
    Relevance: From Oizumi's lab: spectral decomposition of causal influence for (linear) dynamical models — a practical route to frequency-resolved integration measures for time-series/network models of aging bioelectric systems.

12. **Measuring Integrated Information: Comparison of Candidate Measures in Theory and Simulation** — Mediano P.; Seth A.; Barrett A. B. (2018). *Entropy* 21(1):17. DOI: `10.3390/e21010017` — https://doi.org/10.3390/e21010017 — cited 99×.
    Relevance: Head-to-head comparison of candidate integrated-information measures (Φ_EI, Φ_G, Φ_R, etc.) in theory and simulation — use it to choose which proxy to adopt and to avoid known degeneracies (e.g., failures on feedforward chains).

13. **The strength of weak integrated information theory** — Mediano P. A.; Rosas F. E.; Bor D.; Seth A. K.; Barrett A. B. (2022). *Trends in Cognitive Sciences* 26(8):646–655. DOI: `10.1016/j.tics.2022.04.008` — https://doi.org/10.1016/j.tics.2022.04.008 — cited 63×.
    Relevance: "Weak IIT": use integrated-information measures as empirically useful descriptors of neural/biological data without committing to IIT's ontological claims — exactly the epistemic stance an aging-modeling project should adopt.

14. **Toward a unified taxonomy of information dynamics via Integrated Information Decomposition** — Mediano P. A. M.; Rosas F. E.; Luppi A. I.; Carhart-Harris R. L.; Bor D.; Seth A. K.; Barrett A. B. (2025). *Proceedings of the National Academy of Sciences* 122(39):e2423297122. DOI: `10.1073/pnas.2423297122` — https://doi.org/10.1073/pnas.2423297122 — cited 22×.
    Relevance: The published, citable form of **integrated information decomposition (PhiID)**: decomposes system-level integrated information into redundant/unique/synergistic components — ideal for quantifying *which kind* of integration aging destroys first. (The original 2021 PhiID preprint itself remained unpublished; see Leads.)

15. **Improved Measures of Integrated Information** — Tegmark M. (2016). *PLOS Computational Biology* 12(11):e1005123. DOI: `10.1371/journal.pcbi.1005123` — https://doi.org/10.1371/journal.pcbi.1005123 — cited 99×. *(supplementary)*
    Relevance: Proposes numerically optimized approximate Φ measures and scaling tricks — additional toolbox material for tractable Φ on larger networks.

16. **Computing Integrated Information (Φ) in Discrete Dynamical Systems with Multi-Valued Variables** — Gomez C.; Mayner W. G. P.; Beheler-Amass T.; Tononi G.; Albantakis L. (2020). *Entropy* 23(1):6. DOI: `10.3390/e23010006` — https://doi.org/10.3390/e23010006 — cited 15×. *(supplementary)*
    Relevance: Extends exact Φ computation to non-binary (multi-valued) node states — directly relevant if our bioelectric units carry graded states (e.g., discretized membrane-voltage levels).

### A.3 Critiques and adversarial tests (for honest framing)

17. **The unfolding argument: Why IIT and other causal structure theories cannot explain consciousness** — Doerig A.; Schurger A.; Hess S.; Herzog M. H. (2019). *Consciousness and Cognition* 72:49–59. DOI: `10.1016/j.concog.2019.04.002` — https://doi.org/10.1016/j.concog.2019.04.002 — cited 99×.
    Relevance: The sharpest principled critique: any causal-structure theory (IIT included) is argued to be insensitive to isomorphic "unfoldings" of a network, undermining explanatory power. **Note: there is no paper literally titled "the unfalsifiability of IIT" — this (plus #18) is the critique the brief was remembering.**

18. **Hard criteria for empirical theories of consciousness** — Doerig A.; Schurger A.; Herzog M. H. (2020/2021). *Cognitive Neuroscience* 12(2):41–62. DOI: `10.1080/17588928.2020.1772214` — https://doi.org/10.1080/17588928.2020.1772214 — cited 120×. (PubMed PMID 32663056.)
    Relevance: Sets out falsifiability/empirical criteria that theories of consciousness should satisfy and evaluates IIT's shortfalls — cite alongside #17 for a balanced treatment of IIT's scientific status.

19. **The Integrated Information Theory of Consciousness as Pseudoscience** — Fleming S. M.; Frith C. D.; Goodale M.; Lau H.; LeDoux J. E.; Lee A. L. F.; Michel M.; Owen A. M.; Peters M. A. K.; Slagter H. A.; et al. (open letter, 100+ signatories) (2023). *PsyArXiv preprint* (OSF). DOI: `10.31234/osf.io/zsr78` — https://doi.org/10.31234/osf.io/zsr78 — cited 26×.
    Relevance: The strongest public criticism (arguing IIT's central claims have drifted into unfalsifiable territory). Any project that computes Φ must acknowledge this letter and position its work as "weak"/instrumental use of Φ measures (cf. #13).

20. **Adversarial testing of global neuronal workspace and integrated information theories of consciousness** — Cogitate Consortium; Ferrante O.; Gorska-Klimowska U.; Henin S.; Hirschhorn R.; et al. (incl. Tononi G., Pitts M., Mudrik L., Melloni L.) (2025). *Nature* 642(8066):133–142. DOI: `10.1038/s41586-025-08888-1` — https://doi.org/10.1038/s41586-025-08888-1 — cited 129×. (PubMed PMID 40307561.)
    Relevance: First preregistered adversarial head-to-head test of IIT vs GNW across humans, NHP, and mice; several IIT predictions (posterior-hot-zone signatures) were not supported. The empirical state of the art for IIT's contested status — cite for honesty and for the value of instrumentally-defined Φ. **Note: first author is Ferrante (Melloni is senior/consortium lead), Nature 2025.**

21. **Protocol for testing global neuronal workspace and integrated information theories of consciousness in non-human primates and mice** — Gibbons M.; McBride E. G.; et al. (2026). *PLOS ONE* 21(2):e0342770. DOI: `10.1371/journal.pone.0342770` — https://doi.org/10.1371/journal.pone.0342770 — cited 1×. (PubMed PMID 41739818.)
    Relevance: The preregistered animal-model protocol of the adversarial collaboration — a methodological template for any future empirical validation of Φ-style measures in coupled biological systems.

**Corrections to the brief (theme a):** IIT 4.0 is a 2023 PLOS Comput Biol paper led by Albantakis (entry 5); Barbosa's Φ_R paper is titled "A measure for intrinsic information," Sci Rep 2020 (entry 6); PyPhi is in PLOS Comput Biol, not PLoS ONE (entry 8); the PhiID framework's citable published form is the 2025 PNAS taxonomy paper (entry 14); "the unfalsifiability of IIT" does not exist as a title — the actual critiques are entries 17–19; the adversarial-collaboration results paper is Ferrante/Cogitate et al., Nature 2025 (entry 20).

---

## Theme (b) — Aging as loss of information integrity: mortality laws, reliability theory, dynamics

### B.1 Mortality laws: Gompertz, Makeham, Weibull (the target phenomena)

22. **XXIV. On the nature of the function expressive of the law of human mortality, and on a new mode of determining the value of life contingencies…** — Gompertz B. (1825). *Philosophical Transactions of the Royal Society of London* 115:513–583. DOI: `10.1098/rstl.1825.0026` — https://doi.org/10.1098/rstl.1825.0026 — cited 2898×.
    Relevance: The original statement of the exponential hazard law (μ(t) = a·e^{bt}) from actuarial data — the central empirical law our network-degradation model must derive. (An 1833 abstract version also exists: DOI `10.1098/rspl.1815.0271`.)

23. **On the Law of Mortality and the Construction of Annuity Tables** — Makeham W. M. (1860). *The Assurance Magazine and Journal of the Institute of Actuaries* 8(6):301–310. DOI: `10.1017/s204616580000126x` — https://doi.org/10.1017/s204616580000126x — cited 306×.
    Relevance: Adds the age-independent hazard term (μ = A + a·e^{bt}) — the Gompertz–Makeham model is the standard baseline our simulated hazard curves should be fitted against.

24. **A Statistical Distribution Function of Wide Applicability** — Weibull W. (1951). *Journal of Applied Mechanics* 18(3):293–297. DOI: `10.1115/1.4010337` — https://doi.org/10.1115/1.4010337 — cited 9533×.
    Relevance: The Weibull distribution is the canonical reliability-engineering hazard model (power-law hazard) — the competing null model to Gompertz when fitting hazard curves from degrading redundant networks.

25. **The analysis of survival (mortality) data: Fitting Gompertz, Weibull, and logistic functions** — Wilson D. L. (1994). *Mechanisms of Ageing and Development* 74(1–2):15–33. DOI: `10.1016/0047-6374(94)90095-7` — https://doi.org/10.1016/0047-6374(94)90095-7 — cited 150×.
    Relevance: Practical methodology for fitting and discriminating Gompertz vs Weibull vs logistic mortality models — the model-selection template for our simulated survival data.

26. **Biological Implications of the Weibull and Gompertz Models of Aging** — Ricklefs R. E.; Scheuerlein A. (2002). *The Journals of Gerontology Series A* 57(2):B69–B76. DOI: `10.1093/gerona/57.2.b69` — https://doi.org/10.1093/gerona/57.2.b69 — cited 118×.
    Relevance: Interprets the biological meaning of Weibull vs Gompertz parameterizations (initial vulnerability vs actuarial senescence) — supplies the interpretive logic for whichever law our redundancy-depletion model produces. **Note: venue is J Gerontol A, not Exp Gerontol.**

### B.2 Reliability theory — deriving Gompertz from redundancy depletion

27. **The Reliability Theory of Aging and Longevity** — Gavrilov L. A.; Gavrilova N. S. (2001). *Journal of Theoretical Biology* 213(4):527–545. DOI: `10.1006/jtbi.2001.2430` — https://doi.org/10.1006/jtbi.2001.2430 — cited 373×.
    Relevance: **CRITICAL for this project**: derives exponentially increasing (Gompertz-like) failure rates from systems built of *redundant, non-aging* elements whose redundancy is progressively exhausted; also derives Weibull regimes and late-life hazard plateaus. This is the mathematical template for deriving Gompertz from information-network redundancy depletion.

28. **Evolution of ageing** — Kirkwood T. B. L. (1977). *Nature* 270(5635):301–304. DOI: `10.1038/270301a0` — https://doi.org/10.1038/270301a0 — cited 1776×.
    Relevance: The disposable-soma theory: limited energy forces a trade-off between somatic maintenance (information-preserving repair) and reproduction — explains *why* bioelectric/genomic information integrity is permitted to decay in the first place.

29. **The temporal scaling of Caenorhabditis elegans ageing** — Stroustrup N.; Anthony W. E.; Nash Z. M.; Gowda V.; Gomez A.; López-Moyado I.; et al. (2016). *Nature* 530(7588):103–107. DOI: `10.1038/nature16550` — https://doi.org/10.1038/nature16550 — cited 193×.
    Relevance: Shows that lifespan interventions in worms act by uniform *temporal rescaling* of a single aging program — consistent with aging being a coordinated runaway dominated by one (or few) effective dimensions, e.g., a single integration-loss variable; our Φ-decline model should reproduce this scaling property.

30. **Biodemographic Trajectories of Longevity** — Vaupel J. W.; Carey J. R.; Christensen K.; Johnson T. E.; Yashin A. I.; et al. (1998). *Science* 280(5365):855–860. DOI: `10.1126/science.280.5365.855` — https://doi.org/10.1126/science.280.5365.855 — cited 799×.
    Relevance: The biodemographic synthesis documenting late-life mortality deceleration and plateaus across species — the high-age phenomenon our redundancy-exhaustion model must reproduce (plateau ≈ exhaustion of remaining integration/redundancy).

31. **Slowing of Mortality Rates at Older Ages in Large Medfly Cohorts** — Carey J. R.; Liedo P.; Orozco D.; Vaupel J. W. (1992). *Science* 258(5081):457–461. DOI: `10.1126/science.1411540` — https://doi.org/10.1126/science.1411540 — cited 458×.
    Relevance: Large-cohort evidence that hazard growth slows and even declines at extreme ages — key empirical constraint (mortality deceleration) that distinguishes redundancy-exhaustion models from pure Gompertz.

### B.3 Biological framing: hallmarks, epigenetic information loss

32. **The Hallmarks of Aging** — López-Otín C.; Blasco M. A.; Partridge L.; Serrano M.; Kroemer G. (2013). *Cell* 153(6):1194–1217. DOI: `10.1016/j.cell.2013.05.039` — https://doi.org/10.1016/j.cell.2013.05.039 — cited 14327×.
    Relevance: The canonical catalog of aging mechanisms — the bridge that maps our abstract "information-integrity loss" onto concrete biology (genomic instability, epigenetic alterations, loss of proteostasis, …).

33. **Hallmarks of aging: An expanding universe** — López-Otín C.; Blasco M. A.; Partridge L.; Serrano M.; Kroemer G. (2023). *Cell* 186(2):243–278. DOI: `10.1016/j.cell.2022.11.001` — https://doi.org/10.1016/j.cell.2022.11.001 — cited 6376×.
    Relevance: The updated hallmarks framework (12 hallmarks, incl. chronic inflammation, dysbiosis, disabled macroautophagy) with information-deregulation themes foregrounded — use for the biological-grounding section. **Note: DOI ends .001, not .002.**

34. **Loss of epigenetic information as a cause of mammalian aging** — Yang J.; Hayano M.; Griffin P. T.; Amorim J. A.; Bonkowski M. S.; et al.; Sinclair D. A. (2023). *Cell* 186(2):305–326.e27. DOI: `10.1016/j.cell.2022.12.027` — https://doi.org/10.1016/j.cell.2022.12.027 — cited 620×.
    Relevance: The flagship "information-theoretic" aging result: aging framed as *loss of epigenetic information* (measurable via information-theoretic aging clocks / DREAM), partially reversible by OSK reprogramming — the direct biological analog of our Φ-decline hypothesis, including its reversibility claim.

### B.4 Complexity loss, transcriptional noise, attractor drift, reversibility

35. **Loss of 'Complexity' and Aging** — Lipsitz L. A.; Goldberger A. L. (1992). *JAMA* 267(13):1806–1809. DOI: `10.1001/jama.1992.03480130122036` — https://doi.org/10.1001/jama.1992.03480130122036 — cited 1227×. (Authors confirmed via PubMed PMID 1482430; Crossref author list is incomplete for this record.)
    Relevance: The classic statement that aging is a *loss of physiological complexity* (fractal/dynamical metrics decline) — the dynamical-systems precursor to measuring information-integration decline with age.

36. **What is physiologic complexity and how does it change with aging and disease?** — Goldberger A. L.; Peng C.; Lipsitz L. A. (2002). *Neurobiology of Aging* 23(1):23–26. DOI: `10.1016/s0197-4580(01)00266-4` — https://doi.org/10.1016/s0197-4580(01)00266-4 — cited 714×.
    Relevance: Sharpens the physiologic-complexity thesis and its mechanisms — bridges #35 to concrete time-series complexity metrics that can be computed alongside Φ in our pipeline.

37. **Increased cell-to-cell variation in gene expression in ageing mouse heart** — Bahar R.; Hartmann C. H.; Rodriguez K. A.; Denny A. D.; Busuttil R. A.; Dollé M. E. T.; et al. (2006). *Nature* 441(7096):1011–1014. DOI: `10.1038/nature04844` — https://doi.org/10.1038/nature04844 — cited 548×.
    Relevance: Empirical demonstration that aging increases cell-to-cell gene-expression variance — direct evidence that aging destabilizes expression attractors (noise ↑ = cellular information integrity ↓). **Note: it is the ageing mouse *heart*, not haematopoietic stem cells.**

38. **Aging increases cell-to-cell transcriptional variability upon immune stimulation** — Martinez-Jimenez C. P.; Eling N.; Chen H.; Vallejos C. A.; et al. (2017). *Science* 355(6332):1433–1436. DOI: `10.1126/science.aah4115` — https://doi.org/10.1126/science.aah4115 — cited 348×.
    Relevance: Single-cell RNA-seq quantification of aging-driven transcriptional noise upon stimulation — modern attractor-destabilization evidence and a quantitative target for the noise-growth term in our model. **Note: Science 2017, not a 2023 Aging Cell paper.**

39. **Epigenetic gambling and epigenetic drift as an antagonistic pleiotropic mechanism of aging** — Martin G. M. (2009). *Aging Cell* 8(6):761–764. DOI: `10.1111/j.1474-9726.2009.00515.x` — https://doi.org/10.1111/j.1474-9726.2009.00515.x — cited 47×.
    Relevance: Frames stochastic epigenetic drift (random methylation divergence with age) as a mechanism of aging — the theoretical bridge between information-theoretic noise accumulation and phenotypic aging.

40. **In Vivo Amelioration of Age-Associated Hallmarks by Partial Reprogramming** — Ocampo A.; Reddy P.; Martinez-Redondo P.; Platero-Luengo A.; Hatanaka F.; et al.; Izpisua Belmonte J. C. (2016). *Cell* 167(7):1719–1733.e12. DOI: `10.1016/j.cell.2016.11.052` — https://doi.org/10.1016/j.cell.2016.11.052 — cited 921×.
    Relevance: Cyclic OSK partial reprogramming ameliorates multiple aging hallmarks in progeroid and wild-type mice — the demonstration that epigenetic/informational drift is *reversible*, motivating a "rejuvenation = restore Φ" intervention arm in our model. **Note: published in Cell (not Nature), 2016, with this exact title.**

---

## Theme (c) — Meditation and neural integration (the "upregulation" arm)

41. **Long-term meditators self-induce high-amplitude gamma synchrony during mental practice** — Lutz A.; Greischar L. L.; Rawlings N. B.; Ricard M.; Davidson R. J. (2004). *Proceedings of the National Academy of Sciences* 101(46):16369–16373. DOI: `10.1073/pnas.0407401101` — https://doi.org/10.1073/pnas.0407401101 — cited 869×.
    Relevance: The canonical evidence that sustained mental training can upregulate large-scale neural integration (high-amplitude long-distance gamma synchrony) — the empirical basis for treating meditation as an "increase Φ" intervention in the model.

42. **Alterations in Brain and Immune Function Produced by Mindfulness Meditation** — Davidson R. J.; Kabat-Zinn J.; Schumacher J.; Rosenkranz M.; et al. (2003). *Psychosomatic Medicine* 65(4):564–570. DOI: `10.1097/01.psy.0000077505.67574.e3` — https://doi.org/10.1097/01.psy.0000077505.67574.e3 — cited 1867×.
    Relevance: An 8-week mindfulness program shifted prefrontal EEG asymmetry *and* improved immune responses (influenza vaccine antibody titers) — the cleanest classic evidence for a trainable consciousness→body (bioelectric/physiological) interface.

43. **Well-being and affective style: neural substrates and biobehavioural correlates** — Davidson R. J. (2004). *Philosophical Transactions of the Royal Society B* 359(1449):1395–1411. DOI: `10.1098/rstb.2004.1510` — https://doi.org/10.1098/rstb.2004.1510 — cited 311×.
    Relevance: The formal framework linking affective style and well-being to prefrontal/limbic circuit function — the psychological-level correlate that an integration-based (Φ-style) biomarker would need to relate to. **Note: this is Phil Trans B 2004, not PNAS 2003.**

44. **The neuroscience of mindfulness meditation** — Tang Y.; Hölzel B. K.; Posner M. I. (2015). *Nature Reviews Neuroscience* 16(4):213–225. DOI: `10.1038/nrn3916` — https://doi.org/10.1038/nrn3916 — cited 2427×.
    Relevance: The authoritative mechanistic review (attention regulation, body awareness, emotion regulation, changed self-referential processing) — the framing document for meditation as trainable neural integration.

45. **Meditation states and traits: EEG, ERP, and neuroimaging studies** — Cahn B. R.; Polich J. (2006). *Psychological Bulletin* 132(2):180–211. DOI: `10.1037/0033-2909.132.2.180` — https://doi.org/10.1037/0033-2909.132.2.180 — cited 1247×.
    Relevance: The comprehensive EEG/ERP/neuroimaging review of meditation states vs traits — the methodological reference for electrophysiological coherence/integration measures against which our Φ estimates on neural data can be compared.

---

## Bonus — Bioelectric control networks (the project's substrate)

46. **Bioelectric signaling: Reprogrammable circuits underlying embryogenesis, regeneration, and cancer** — Levin M. (2021). *Cell* 184(8):1971–1989. DOI: `10.1016/j.cell.2021.02.034` — https://doi.org/10.1016/j.cell.2021.02.034 — cited 430×.
    Relevance: Defines bioelectric circuits (ion-channel/voltage networks storing and processing morphogenetic information, reprogrammable by drugs and light) as a genuine computational medium — the substrate-level reference for our "bioelectric control network."

47. **Information integration during bioelectric regulation of morphogenesis of the embryonic frog brain** — Manicka S.; Pai V. P.; Levin M. (2023). *iScience* 26(12):108398. DOI: `10.1016/j.isci.2023.108398` — https://doi.org/10.1016/j.isci.2023.108398 — cited 12×.
    Relevance: **The closest existing precedent to our project**: computes IIT-style integrated information over bioelectric state-transition models of embryonic morphogenesis — a direct template for coupling Φ computation to bioelectric network dynamics.

---

## Unverified / leads (not counted above)

- **Mediano, Rosas, Bor, Seth, Barrett — "Integrated information decomposition" (the original PhiID preprint, ~2021).** The framework's citable published forms are verified entries #13 (Trends Cogn Sci 2022) and #14 (PNAS 2025). The original preprint itself could not be verified via Crossref/PubMed (arXiv export API returned HTTP 429 during this session; retry with `sleep 25` suggested). If the arXiv ID is needed, verify it before citing.
- **"An adversarial collaboration protocol for testing theories of consciousness" (Melloni et al., ~2023 preprint).** Not found under this exact title in Crossref/PubMed. The published animal protocol is verified entry #21 (Gibbons et al. 2026, PLOS ONE); the human-results paper is verified entry #20 (Ferrante/Cogitate et al. 2025, Nature). Cite those instead.
- **"Raj?" (single-cell noise / Waddington-landscape aging drift).** No specific paper matching this recollection could be verified. The aging-noise/landscape-drift angle is instead covered by verified entries #37, #38, #39, #40.
- **"Attractor Landscape Analysis Distinguishes Aging Markers from Rejuvenation Targets" — Copes & Canfield (~2026), DOI `10.64898/2026.02.01.703159`** appeared in a Crossref response but is an unrefereed preprint (Research Square-style DOI, 0 citations) — treat as a lead only.
- **A specific "aging + Waddington landscape" review** could not be verified; nearest verified anchors are Martin 2009 (#39) and Ocampo 2016 (#40).
- Semantic Scholar, OpenAlex, and arXiv APIs were HTTP 429 (rate-limited) throughout; all DOIs above were verified via Crossref/PubMed only.

---

## Synthesis: what to use where

**(i) Gaussian-linear Φ implementation:** Barrett & Seth 2011 (#9, equations for Φ_EI/Φ_ar in linear-Gaussian systems) as the core; Oizumi/Tsuchiya/Amari 2016 (#10, information-geometric Φ* for Gaussians) and Cohen et al. 2020 (#11, spectral decomposition) as complementary routes; Mediano et al. 2018 (#12) to choose/validate the proxy; PyPhi (#8) and Gomez et al. 2020 (#16) for discrete-system benchmarks; Φ_R (Barbosa 2020, #6) for the intrinsic perturbational measure; Mediano et al. 2022 (#13) for the "weak IIT" framing that keeps the project scientifically defensible.

**(ii) Deriving Gompertz-style hazard from redundancy/network degradation:** Gavrilov & Gavrilova 2001 (#27) is the mathematical template (redundancy depletion → exponential hazard; also yields Weibull regimes and late-life plateaus). Fit/compare against Gompertz/Makeham/Weibull/logistic using Wilson 1994 (#25) and Ricklefs & Scheuerlein 2002 (#26), with the original laws Gompertz 1825 (#22), Makeham 1860 (#23), Weibull 1951 (#24). Validate deceleration/plateaus against Vaupel 1998 (#30) and Carey 1992 (#31); check the single-timescale scaling property against Stroustrup 2016 (#29). Biological grounding: Kirkwood 1977 (#28), López-Otín 2013/2023 (#32/#33), Yang/Sinclair 2023 (#34).

**(iii) Honest framing of IIT's criticisms:** Doerig et al. 2019 (#17, unfolding argument) and 2020 (#18, hard criteria); the 124-signatory "pseudoscience" letter (#19); and the adversarial empirical tests (#20, #21). Position the project as measuring integration *instrumentally* (weak IIT, #13), not as adjudicating consciousness claims.

**(iv) The consciousness-body interface (meditation arm):** Lutz 2004 (#41) and Davidson 2003 (#42) for trainable integration and brain→immune effects; Tang/Hölzel/Posner 2015 (#44) and Cahn & Polich 2006 (#45) for mechanistic/methodological framing; bioelectric substrate per Levin 2021 (#46) and the Φ-on-bioelectric precedent Manicka et al. 2023 (#47).
