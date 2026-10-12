---
name: kilean-write-style
description: Write or revise technical and scientific prose in Kilean Hwang's published voice (accelerator physicist at FRIB), including journal papers, conference proceedings, abstracts, reports, cover letters, and reviewer responses. Use whenever Kilean asks for text in his style, to sound natural or less machine-written, or before finalizing manuscript prose under his name. This skill controls voice and sentence habits; pair it with context-safe-document-writing for claims, evidence, terminology, and structure.
---

# Kilean Hwang's published writing style

Use this skill for voice, not scientific authority. Preserve the meaning, certainty, scope, numbers, and terminology established by the source material and the context-safe-document-writing skill.

The profile is based primarily on eight Kilean-led publications from 2022–2026, including the 2023 and 2026 *Physical Review Accelerators and Beams* papers. Evidence is recency weighted within each register: the 2026 journal paper and the 2025 proceedings have the greatest influence, while the 2022 texts retain only low-weight evidence for persistent habits.

Read [references/style-map.md](references/style-map.md) for any substantial draft or rewrite. It turns the evidence into decisions about abstracts, introductions, paragraph logic, comparisons, qualifications, figures, and conclusions. Read [references/profile.md](references/profile.md) when checking whether a choice is evidence-based or updating the skill; it records the corpus, weighting method, measurements, time evolution, and attribution limits.

Use this evidence order when sources differ:

1. the user's supplied wording and corrections;
2. the newest Kilean-led paper in the same register;
3. recurring patterns across older papers in that register;
4. the other register, used only for transferable habits.

Match the rhetorical behavior before matching vocabulary. Do not create a superficial imitation by sprinkling in favored words.

## What the voice consists of

Tone and word choice are only two of the dimensions this skill controls. In rough order of how strongly they identify the voice:

1. **Rhetorical architecture**: constraint → difficulty → response → reason → result or limit, at paragraph and document scale.
2. **Stance**: definite about completed work, qualified about interpretation and transfer, with evaluative words earned by a nearby mechanism or number.
3. **Comparison structure**: concede the alternative's proper domain, delimit the present problem class, then choose.
4. **Agency and tense**: *we* for decisions, the method or result as subject for behavior, passive for setup; past tense for what was done, present for what a method does or a figure shows.
5. **Cohesion**: explicit connectors and *This + specific noun* anaphora.
6. **Quantitative anchoring**: operational quantities such as evaluations, seconds, beam time, and dimensions justify each method choice.
7. **Diction**: established technical terms, defined acronyms repeated consistently, a practical evaluative vocabulary, and no ornamental words.
8. **Sentence and paragraph rhythm**: moderate declaratives with conditions kept attached; a few short consequence sentences.
9. **Figure, equation, and citation integration**: state the question a figure answers and the feature to inspect; explain the terms after an equation; cite at the specific claim.
10. **Punctuation and recurring phrases**: commas and parentheses carry most of the load; colons and dashes are occasional; recurring multi-word phrases are reported by the checker.

[references/profile.md](references/profile.md) gives the evidence and calibration status of each dimension. Tense, *This* anaphora, paragraph length, citation habits, and recurring phrases have measures added after the last corpus pass. The checker reports them, but they are not yet range-checked.

## Choose the register

Use the **journal register** by default for archival papers and formal technical documents. It is formal, explanatory, and occasionally advocative, but not ornate. Sentences are usually moderate in length, commonly around 19–22 words, with a longer sentence when a condition or mechanism must remain attached to the claim. Explain the reason for a technical choice and state its scope. Use first person for author decisions and actions, but let a method, measurement, or result be the subject when describing its properties.

Use the **proceedings register** for conference papers, technical reports, and talks. Keep the same reasoning style but compress background and move quickly to the operational problem, method, and result. Short subsection labels, compact enumerations, and direct statements such as “We present” or “We use” fit this register. Do not make it chatty merely because it is shorter.

For cover letters and reviewer responses, carry over the same direct, factual, and bounded tone. This is an extrapolation from the publication corpus, not a separately measured correspondence style.

## Core voice

Kilean writes as an accelerator physicist solving a concrete technical or operational problem. The prose normally moves through:

**context or constraint → technical difficulty → chosen response → why it fits → result or remaining limitation**.

The motivation is usually practical: beam time, sample efficiency, computation time, measurement noise, model discrepancy, reliability, or the number of feasible evaluations. Prefer this concrete motivation over a broad claim about importance.

The tone is confident about what was implemented or observed and cautious about interpretation. State a limitation where it changes the conclusion, then continue with what can still be concluded or done. Recent papers may call an approach **powerful, critical, practical, robust, principled,** or **well-suited**, but normally connect that evaluation to a mechanism, comparison, or operating constraint. Keep that support nearby.

## Agency and sentence subjects

- Use **“we”** for deliberate author actions and judgments: *we implemented, we used, we present, we found, we selected, we trained*.
- Use the **method, system, measurement, or result** as the subject when describing behavior: *BO uses all online data; measurement noise persists; the model predicts; Fig. 4 shows*.
- Passive voice is natural for definitions, established procedures, and experimental setup: *the parameters are reconstructed; the model was trained*.
- Do not force every paragraph into first person and do not replace a clear technical subject with “we” merely to meet a count.
- Use the **past tense** for what was done or observed in this work (*we implemented, the model was trained, the beam test showed*) and the **present tense** for what a method does, what a figure shows, and what the paper presents (*BO uses, Figure 4 shows, we present*). This follows the quoted corpus examples; the tense mix is measured by `--detail` but not yet calibrated.

## Paragraph and sentence movement

1. Start with the concrete situation or claim. Add background only when the reader needs it.
2. Make the relation between sentences explicit with ordinary connectors: **However, Therefore, In addition, Furthermore, Nevertheless, Instead, Specifically, For example, To address this,** and **Although**.
3. Use **because, while, although, due to, which,** and **so that** to keep a reason or condition attached to the statement it qualifies. Avoid stacking unrelated clauses.
4. A paragraph often names a difficulty, explains why it matters in operation, gives the chosen response, and ends with a result, trade-off, or limit. Recent papers also use a short declarative claim followed by a **This + specific noun** sentence that carries the consequence forward: *This strategy…, This limitation…, This discrepancy…*.
5. Roadmaps and compact lists are acceptable when they reflect the actual technical decomposition. Avoid rhetorical lists whose only purpose is emphasis.

## Diction

Prefer established accelerator and machine-learning terms over ornamental synonyms. Define an abbreviation at first use, usually in parentheses, and then use it consistently.

Recurring choices in the recent corpus include **practical, efficient, sample-efficient, robust, well-suited, specifically, to address, enables, allows, incorporates, converges,** and **mitigates**. The recent papers also use **leverage, principled, critical, powerful, substantial, successful,** and **landscape**. These are authentic choices when they name a supported advantage, consequence, or technical object; remove them only when they are freestanding praise.

Avoid decorative language that does not occur naturally in the corpus, such as *delve, tapestry, realm, seamless, showcase,* or *paramount*. Also avoid slogans, aphorisms, and inflated declarations of novelty.

## Qualification and limitations

Use plain modal language: **may, can, could, is expected to, potentially, approximately, suggests,** and **requires further study**. Typical moves are:

- state what a method enables, then name the assumption or model error that limits it;
- distinguish a useful correlation from proof of the underlying explanation;
- say when a comparison applies only under the tested conditions;
- mark work outside the scope instead of implying that it was completed.

Do not add repeated defensive disclaimers. One well-placed qualification is better than the same caveat in several sections.

## Figures and technical explanation

Introduce a figure by the question or comparison it answers, identify the feature that matters, and state the inference. **“Figure 4 shows …,” “As shown in Fig. 4, …,”** and occasional **“Note that …”** are consistent with the corpus. Do not narrate every curve.

For methods, explain enough mechanism to justify the choice. Kilean's papers often compare alternatives in terms of sample efficiency, computational cost, available data, or operational constraints before stating why one was selected.

When comparing methods, first identify the problem class or condition under which each method is appropriate. Then make the local choice. The recent journal paper explicitly concedes the advantage of an alternative for dynamic control before preferring BO for static, expensive optimization. Preserve this balanced comparison pattern rather than presenting every alternative as deficient.

## Punctuation and rhythm

- Full stops and commas carry most of the prose.
- Parentheses are common for abbreviations, short conditions, definitions, and figure or equation pointers.
- Semicolons are uncommon in prose. Mathematical notation may contain them and should not influence the style judgment.
- Colons may introduce a real list, definition, or compact explanation.
- Dashes occur occasionally in recent papers to set off a short technical clarification. Use them sparingly; there is no blanket prohibition.
- Mix moderate sentences with some shorter ones. Do not lengthen a clear sentence merely to satisfy a numerical target.

## Apply and check

1. Settle the science, evidence, terminology, and claim strength first.
2. Choose the register and rewrite by paragraph, following the problem-to-response movement above.
3. Preserve quotations, recorded protocols, and wording the user has frozen.
4. Run `python scripts/style_check.py DRAFT --compare` for the journal register, or add `--register proceedings`. Treat the recency-weighted measurements as diagnostics, not requirements; inspect the prose before changing a scientifically necessary sentence. Add `--detail` to see tense, passive voice, opener types, bare versus specific *This*, citation and acronym habits, and recurring phrases; use these to spot a strong mismatch, since they have no calibrated range yet.
5. Read the result once for agency, practical motivation, explicit contrast or cause, supported evaluation, and bounded claims. If praise lacks nearby support, replace it with the mechanism, constraint, or observed result. Do not remove a strong evaluative word merely because it is strong.
6. For a large rewrite, show a representative paragraph first when the user has not already approved the direction.

The aim is current published voice with correct English. Do not reproduce non-native grammatical slips from the source papers.

## Refresh the evidence

When a new Kilean-led paper appears, or to calibrate the extended measures, add it to `MANIFEST` in `scripts/corpus.py` and run:

```
python scripts/corpus.py fetch      # downloads to ~/.cache/kilean-write-style, or use --pdf-dir with <id>.pdf files
python scripts/corpus.py profile    # recency-weighted report per register, with suggested checker ranges
```

Fetching needs network access to arxiv.org, proceedings.jacow.org, and journals.aps.org (or www.osti.gov). If they are blocked, place the PDFs in a directory and pass `--pdf-dir`. Review the extracted text once, then update `PROFILES` in `scripts/style_check.py` and the tables in `references/profile.md` from the report. Keep paper text out of the repository.
