# Evidence profile for Kilean Hwang's published style

Rebuilt 2026-10-11 after Kilean reported that the earlier skill did not yet sound like him, then refined with explicit recency weighting. This profile describes his **published output after 2021**. It does not try to separate every coauthor or editor contribution from the final prose.

## Corpus and attribution

The primary corpus contains eight papers or preprints in which Kilean is first author and, for the journal papers, corresponding author. These texts provide the strongest available evidence for wording and sentence-level choices.

1. K. Hwang et al., “Beam Tuning at the FRIB Front End Using Machine Learning,” IPAC 2022, TUPOST053, [doi:10.18429/JACoW-IPAC2022-TUPOST053](https://doi.org/10.18429/JACoW-IPAC2022-TUPOST053).
2. K. Hwang et al., “Prior-mean-assisted Bayesian optimization application on FRIB Front-End tunning,” arXiv:2211.06400 (2022), [arXiv](https://arxiv.org/abs/2211.06400).
3. K. Hwang, C. Mitchell, and R. Ryne, “Machine learning based phase space tomography using kicked beam turn-by-turn centroid data in a storage ring,” *Phys. Rev. Accel. Beams* 26, 104601 (2023), [doi:10.1103/PhysRevAccelBeams.26.104601](https://doi.org/10.1103/PhysRevAccelBeams.26.104601).
4. K. Hwang et al., “Machine-learning-assisted beam tuning at FRIB,” LINAC 2024, THXA004, [doi:10.18429/JACoW-LINAC2024-THXA004](https://doi.org/10.18429/JACoW-LINAC2024-THXA004).
5. K. Hwang et al., “Application of ML tools for extraction of BPM-Q and transverse beam matching,” HIAT 2025, TUP11, [doi:10.18429/JACoW-HIAT2025-TUP11](https://doi.org/10.18429/JACoW-HIAT2025-TUP11).
6. K. Hwang et al., “Bayesian active learning for converging posteriors in latent variable inference for control systems,” ICALEPCS 2025, WEPD075, [doi:10.18429/JACoW-ICALEPCS2025-WEPD075](https://doi.org/10.18429/JACoW-ICALEPCS2025-WEPD075).
7. K. Hwang et al., “Advanced ML methods for beam tuning at FRIB,” NAPAC 2025, THXN01, [doi:10.18429/JACoW-NAPAC2025-THXN01](https://doi.org/10.18429/JACoW-NAPAC2025-THXN01).
8. K. Hwang et al., “Customized Bayesian optimization for efficient beam tuning at the facility for rare isotope beams,” *Phys. Rev. Accel. Beams* 29, 024601 (2026), [doi:10.1103/5hyd-bhpx](https://doi.org/10.1103/5hyd-bhpx).

The extracted corpus contains about 23,600 prose words from the abstract through the conclusion, with references excluded. Equations and captions remain where they are integrated with the prose, so punctuation counts from PDF extraction are not reliable unless mathematical notation is removed.

### Recency weighting

Journal and proceedings registers are modeled separately. Within each register, evidence receives an exponential recency weight with a two-year half-life relative to 2026:

| Year | Weight |
|---:|---:|
| 2026 | 1.00 |
| 2025 | 0.71 |
| 2024 | 0.50 |
| 2023 | 0.35 |
| 2022 | 0.25 |

This makes the 2026 paper about 74% of the two-paper journal profile and the 2023 paper about 26%. In the proceedings profile, each 2025 paper contributes about 23%, the 2024 paper 16%, and each 2022 text 8%. The weighting applies to current style choices, not scientific authority. A trait that recurs across several years remains strong evidence even when it began in an older paper.

All eight primary texts list Kilean first. The two journal papers also identify him as contact author. No additional authorship multiplier is used. The 2022 arXiv preprint remains in the proceedings/preprint register because its less edited prose is useful voice evidence, but its age already gives it low influence.

Two additional post-2021 journal papers list Kilean as a non-leading author: “Using kernel-based statistical distance to study the dynamics of charged particle beams in particle-based simulation codes” (2022) and “Acceleration of uranium beam to record power of 10.4 kW and observation of new isotopes at Facility for Rare Isotope Beams” (2024). They establish publication context but are not used to assign individual sentence habits because the prose cannot be attributed to one coauthor.

## What changed from the earlier profile

The earlier skill relied on two 2022 texts and treated a single paragraph-level preference as a separate journal corpus. That produced several unsupported rules.

- The two measured journal papers have median sentence lengths of 19 and 20 words, not a target near 25–28 words.
- First-person use varies by paper. The 2023 journal paper uses it more often than the 2026 paper, and both also use the method, measurement, or result as a natural sentence subject.
- Recent papers repeatedly use *leverage, principled, critical,* and *landscape* in technical contexts. These words are therefore not evidence of a foreign voice by themselves.
- Recent journal and proceedings papers use occasional dashes, colons, roadmap sentences, and compact enumerations. None warrants a blanket prohibition.
- “Note that” and “Finally” occur in the journal papers. They should be used sparingly, not automatically removed.

The skill now targets the published voice itself. It does not label a recent published paper “not Kilean” because its register differs from the 2022 proceedings.

The second refinement also corrects a surface-only bias in the first revision. Tone and favored words are not enough to reproduce the voice. The more discriminating dimensions are rhetorical architecture, information order, grammatical agency, comparison structure, qualification, technical anaphora, figure integration, and the way operational quantities justify a method choice.

## Quantitative observations

Measurements below are approximate. PDF text was extracted in column-aware reading order; references were removed. Sentence statistics are useful for detecting a strong mismatch, not for prescribing every sentence.

| Text | Register | Weight | Median words/sentence | 90th percentile | Sentences under 12 words | First person per 1,000 words |
|---|---|---:|---:|---:|---:|---:|
| IPAC 2022 | proceedings | 0.25 | 22 | 60 | 13% | 21.3 |
| pmBO preprint 2022 | proceedings/preprint | 0.25 | 19 | 35 | 17% | 16.5 |
| PRAB tomography 2023 | journal | 0.35 | 19 | 38 | 16% | 14.8 |
| LINAC 2024 | proceedings | 0.50 | 20 | 34 | 8% | 14.7 |
| HIAT 2025 | proceedings | 0.71 | 20 | 36 | 12% | 7.7 |
| ICALEPCS 2025 | proceedings | 0.71 | 17 | 36 | 19% | 12.6 |
| NAPAC 2025 | proceedings | 0.71 | 19 | 32 | 24% | 12.5 |
| PRAB customized BO 2026 | journal | 1.00 | 20 | 36 | 20% | 7.2 |

The recency-weighted center is approximately 20–21 words for journal prose and 19 words for proceedings prose, with a 90th percentile near 35–36 words in both. The 60-word IPAC value is an outlier affected by compressed proceedings prose and footnote extraction. The journal register is not distinguished by uniformly longer sentences; it is distinguished more by fuller reasoning, more explicit scope, and less conversational compression.

First person declines in the newest material. The recency-weighted rate is about 9 per 1,000 words for journal prose and 13 per 1,000 for proceedings, but the within-register spread is large. This supports an agency rule, not a pronoun quota.

Contrast, cause, and purpose markers are more stable than punctuation counts. In the recency-weighted analysis, explicit contrast markers occur about 5 times per 1,000 words in both registers, and cause/purpose markers about 6 times per 1,000. These rates explain the visible connective texture without requiring a connector in every sentence.

## Tone

The dominant tone is practical, technical, and evidence-conscious. The papers explain a method through the constraint that motivated it: limited beam time, noisy measurements, machine drift, computational cost, model error, or the need to use few evaluations. The prose does not usually begin from an abstract claim about broad importance when a concrete operational reason is available.

The latest texts are somewhat more openly evaluative than the earlier papers. The 2025–2026 corpus uses *powerful, critical, principled, substantial,* and *successful* in addition to *efficient, robust,* and *practical*. These words are normally accompanied by a mechanism, operational comparison, or application. The current voice therefore should not be flattened into cautious minimalism or screened through a generic list of “AI words.”

Claims are direct when they concern completed work: *we implemented, we used, we found, we present*. Claims become qualified when they concern transfer, interpretation, or incomplete validation: *may, can, could, potentially, is expected to,* and *requires further study*.

The writer does not hide failure or limitation. A method may be too slow, a model may be inaccurate, a result may be only a correlation, or an extension may be outside scope. The next sentence normally explains what was done despite that limitation.

## Paragraph logic

A recurring paragraph pattern is:

1. name the operational or modeling problem;
2. explain why it matters or why the obvious approach is insufficient;
3. introduce the chosen response;
4. explain the mechanism or practical advantage;
5. report the result, trade-off, or remaining limit.

The 2022 preprint makes this pattern especially visible through repeated *However* and *Instead*. The later papers retain the logic but integrate it into a more formal journal or proceedings register.

The recent papers frequently use a short topic claim followed by a sentence beginning with a specific anaphoric noun phrase: *This strategy, This approach, This limitation, This discrepancy,* or *This localization*. This carries the exact object forward and avoids both abruptness and a vague bare *this*.

Common transitions across the corpus include **However, Therefore, In addition, Furthermore, Moreover, Nevertheless, Instead, Specifically, For example, To address this, By contrast, In contrast, Conversely,** and **Finally**. The connection is usually stated rather than left implicit.

## Agency and grammatical subjects

The corpus does not support a rule that “we” must narrate everything.

- **We** marks deliberate author action: choosing features, training a model, implementing a strategy, testing a method, or interpreting a result.
- **Methods and systems** are subjects when their properties matter: Bayesian optimization incorporates data, probabilistic modeling handles noise, a virtual diagnostic predicts a quantity, or a measurement limits accuracy.
- **Passive voice** is common for definitions and procedures: parameters are reconstructed, data are collected, a model is trained, and a setting is queried.

This alternation keeps agency clear without making every sentence personal.

## Choice of words

Frequently recurring or characteristic choices include:

- practical motivation: **beam time, time budget, computational cost, sample efficiency, machine drift, measurement noise, model error**;
- method evaluation: **efficient, sample-efficient, robust, well-suited, practical, reliable, promising**;
- response verbs: **address, mitigate, incorporate, exploit, leverage, enable, allow, improve, reduce, constrain, converge**;
- reporting verbs: **present, use, implement, train, demonstrate, find, show, discuss**;
- scope and uncertainty: **may, can, could, potentially, approximately, under these conditions, outside the scope, further study**.

The technical use of **principled** usually names a method with a defined rationale, such as balancing exploration and exploitation. **Leverage** usually means using information already available. **Landscape** refers to an objective-function landscape. **Critical** often marks an operational distinction or constraint. **Powerful** occurs in the recent overview-style prose, but is followed by the capability that earns the description. These uses are specific, not decorative.

Words absent or nearly absent from the corpus are more useful negative signals when they are used ornamentally: *delve, tapestry, realm, seamless, showcase,* and *paramount*. Their absence is not a ban on a scientifically necessary term; it is a warning against generic promotional prose.

## Figures and explanations

Figure discussion is explicit and selective. Typical moves are “Figure 4 shows…,” “As shown in Fig. 4…,” and “Note that…,” followed by the feature that supports the point. A caption or paragraph may compare a prediction with a reference, identify an error trend, or state where agreement breaks down. It does not normally describe every visual element.

Method sections often explain a technical choice by comparing it with an alternative. The comparison is framed in operational quantities such as number of samples, computation time, measurement time, dimensionality, or susceptibility to model error.

The 2026 journal paper makes the comparison structure especially clear: it first distinguishes static expensive optimization from long-horizon dynamic control, acknowledges the domain in which reinforcement learning is superior, and then argues for BO in the present problem class. This **concede → delimit → choose** movement is stronger evidence of the voice than any isolated adjective.

## Titles, headings, abstracts, and conclusions

Titles are descriptive and name the method plus the task or system. Headings are functional; proceedings often use short labels, while recent longer papers may use a heading that states the question a section answers.

Abstracts usually move from the operational problem to the method and then to an application or result. They can contain one broader evaluative claim, especially in the recent overview papers, but do not rely on a slogan. Conclusions synthesize the implemented components and practical benefit. The 2026 paper ends with a bounded transfer claim to other complex, resource-constrained scientific instruments, showing that modest generalization is part of the current journal voice when the common constraint is named.

## Information density and technical anchoring

The prose often justifies a claim with quantities that operators can interpret: seconds per evaluation, minutes of beam time, number of samples, dimensions, tolerances, or hardware delays. These details are not decorative precision; they explain why an algorithmic choice is practical. A definition or equation is followed by the physical meaning of its terms or the operational consequence needed for the next step.

## Register differences

### Journal

The 2023 and 2026 PRAB papers are formal but still direct. They use moderate sentences, clear section roadmaps, technical nouns as subjects, and enough detail to connect the method to its assumptions. First-person frequency varies substantially, so it is not a register-defining quota. The newer paper uses more polished terms such as *principled, leverage, critical,* and *powerful*, stronger local topic sentences, more balanced comparisons, and more occasional dash constructions than the 2023 paper.

### Proceedings and preprints

Proceedings compress context, use more short subsection labels, and often move quickly from an operational problem to an implementation. First person is sometimes more frequent, especially in 2022 and 2024, but the 2025 proceedings show that a concise paper can also use an impersonal technical subject. The register may use compact lists or labeled points when space is limited.

## Stable traits versus current traits

Treat the following as stable across the period: practical motivation, explicit logical relations, consistent technical terms, direct reporting verbs, concrete comparisons, visible model or measurement limitations, and selective figure interpretation.

Treat the following as current 2025–2026 preferences when no user example overrides them: lower dependence on first-person openings, stronger method/result subjects, compact labeled decomposition, supported evaluative language, balanced domain-specific comparison, and occasional colons or dashes. Do not resurrect a 2022 conversational phrase merely because it appears in the corpus.

## Limits of the evidence

- All publications are coauthored, so the profile describes recurring published output under Kilean's lead, not an experimentally isolated individual idiolect.
- Most of the post-2021 primary corpus concerns machine learning, beam tuning, diagnostics, or phase-space reconstruction. The reasoning habits are more transferable than the topic-specific vocabulary.
- Conference editing and journal copyediting can affect punctuation and word choice.
- The style checker should identify strong departures, not force a draft to match every corpus statistic.
- Correct English takes precedence over reproducing grammatical slips in the source papers.
