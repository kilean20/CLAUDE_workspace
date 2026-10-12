# Actionable style map

Use this reference when drafting or substantially revising text in Kilean Hwang's current published voice. The evidence and recency weights are documented in [profile.md](profile.md). This map describes choices to make; it is not a template that every paragraph must fill.

## 1. Rhetorical architecture

The characteristic unit is a technical response to a concrete constraint. Organize the passage around this movement:

**operating context or model assumption → practical difficulty → chosen response → why it fits → observed result or boundary**

The difficulty is normally specific: limited beam time, few feasible evaluations, noisy measurements, machine drift, model discrepancy, insufficient diagnostics, computation time, or hardware ramping. Avoid replacing it with a broad opening about the general importance of the field.

For a method paragraph, answer these in reader order:

1. What makes the task difficult here?
2. What method or modification is used?
3. What part of the method addresses the difficulty?
4. What does it cost, assume, or leave unresolved?
5. What was observed under the stated conditions?

The paragraph may omit a step when the surrounding text already supplies it. Do not repeat the full chain mechanically.

## 2. Document-level movement

### Title and headings

Prefer a descriptive title that names the method and the system, task, or measurement. Do not use a slogan, question, or inflated novelty claim. Use functional section headings. A **why X is effective** heading is natural when the section genuinely develops the reasons; a short method label is natural in proceedings.

### Abstract

A typical abstract moves quickly through:

**operational need → method or customization → application/result → bounded scope**.

The newer papers tolerate one strong evaluative statement such as *well-suited*, *powerful*, or *critical* when the abstract also states the reason. Name the implemented work with direct verbs such as **implemented, developed, present, use,** or **demonstrate**. Do not pack the abstract with every secondary number or every caveat.

When the problem class is abstract, one concrete instance may follow it, mapping the abstract roles to hardware: *“A simple example is …: corrector magnets serve as controls, BPMs provide observables, …”*. The instance is followed by the constraint that makes the task hard. The 2026 msBO draft abstract shows this move (see the supplementary evidence in profile.md). Use it only when it shortens the reader's path to the problem.

### Introduction

Begin with the physical or operational setting, then narrow to the pressure it creates. Explain why the usual or obvious approach is insufficient before introducing the response. A short roadmap is natural in a journal article and acceptable in a longer invited proceeding.

### Methods and results

Introduce a technical choice through its purpose. Explain enough of the mechanism for the reader to see why it should help. When reporting a result, give the relevant comparison and condition before the interpretation. Keep implementation details that matter to reproducibility; move incidental detail out of the main argument.

### Conclusion

Synthesize the implemented elements and the practical outcome. Recent conclusions often end with a bounded statement of transferability to similar resource-constrained systems. Do not introduce a new method, metric, or unsupported universal claim.

## 3. Tone and stance

The tone is practical, technical, and explanatory. It can be openly positive about a method, particularly in recent invited proceedings and the 2026 journal article, but the positive assessment is usually earned by one of four things:

- a mechanism: probabilistic modeling balances exploration and exploitation;
- an operational quantity: fewer samples, seconds of computation, less ramping, or shorter beam time;
- a comparison under stated conditions;
- an observed machine or simulation result.

Be definite about completed actions and observations. Use qualification for extrapolation, causal interpretation, model fidelity, and untested generalization. The voice does not apologize for limitations; it states them and continues with the usable conclusion.

## 4. Lexical habits

### Productive word families

- **problem and boundary:** challenge, limitation, constraint, discrepancy, mismatch, error, noise, drift, inaccurate, nontrivial;
- **response:** address, mitigate, incorporate, employ, implement, adapt, constrain, regularize, suppress, leverage, exploit;
- **benefit:** efficient, sample-efficient, rapid, practical, robust, reliable, well-suited, informative;
- **explanation:** specifically, in particular, for example, because, due to, therefore, while, although;
- **evidence:** show, demonstrate, illustrate, indicate, observe, find, compare, suggest;
- **scope:** under these conditions, in this setting, for this task, outside the scope, requires further study.

Recent papers also use **powerful, critical, principled, substantial, successful,** and **landscape**. These words are not foreign to the voice. Use them only when the sentence or its neighbor supplies the technical basis.

Repeat the established technical noun or acronym when it is the clearest reference. Do not vary **Bayesian optimization**, **beam tuning**, or another defined term merely to avoid repetition.

Avoid ornamental or generic prose such as *delve, tapestry, realm, seamless,* or *paramount*. Avoid a chain of abstract nouns where a method, measurement, device, or result can be the subject.

## 5. Agency and grammatical subjects

Use **we** for a deliberate research action, decision, or interpretation:

- selecting or designing a method;
- implementing or training a model;
- performing a comparison or test;
- stating what the authors found or propose.

Use the **method, measurement, device, constraint, or result** as subject when its behavior is the point. This is increasingly common in the 2025–2026 papers and prevents repetitive *we* openings. Passive voice is natural for definitions, setup, and standard procedures.

Do not impose a first-person quota. In the recency-weighted corpus, first person is less frequent in the 2026 journal paper than in the 2023 paper, even though both are recognizably Kilean-led.

Tense follows the same division of roles. Use the past for what was done or observed in this work: *we implemented, the model was trained, the beam test showed*. Use the present for what a method does, what a figure or table shows, general facts, and what the paper itself presents: *BO uses all online data, Figure 4 shows, we present*. A results paragraph can therefore move from past (the measurement) to present (what the figure shows) without inconsistency. This rule is drawn from the quoted corpus examples; `style_check.py --detail` reports the mix, but it is not yet calibrated.

## 6. Sentence rhythm and syntax

The center is a moderate declarative sentence, roughly 19–21 words. Short sentences state a local fact or consequence. Longer sentences keep a condition, mechanism, or comparison attached to the claim it bounds. Split a sentence when its clauses make unrelated moves, not merely because it exceeds a target length.

Common syntactic moves include:

- purpose-first infinitives: **To reduce…, To address…, To improve…**;
- contrastive subordination: **While…, Although…, However,…**;
- causal attachment: **because, due to, so that**;
- specific technical anaphora: **This strategy…, This limitation…, This discrepancy…, Such a task…**;
- direct figure subjects: **Figure 4 shows/illustrates…**;
- a trailing consequence clause after a comma: **…, reducing the number of state switches needed**. This appears in the 2026 draft abstract and has not yet been measured in the published papers, so use it at most once or twice per paragraph.

Questions, imperatives, fragments, and slogan-like one-line paragraphs are uncommon outside headings and labels.

## 7. Cohesion and transitions

Make the relation between adjacent claims recoverable. Use an explicit connector when the relation is contrast, cause, consequence, addition, example, or purpose. The most characteristic transitions are ordinary rather than literary: **However, Therefore, In addition, Furthermore, Nevertheless, Instead, Specifically, For example, By contrast, In contrast, Conversely, Finally,** and **To address this**.

Do not begin every sentence with a connector. Another common pattern is to repeat the technical subject or use **This + specific noun**. Avoid a bare *This* when the referent is not immediately obvious.

## 8. Comparisons, trade-offs, and limitations

Compare methods on the axis that matters operationally: number of evaluations, computation time, available prior data, measurement time, dimensionality, noise handling, model discrepancy, hardware constraints, or adaptation to distribution shift.

Use a balanced sequence:

**acknowledge the alternative's proper domain → state why direct comparison is limited → identify the present problem class → justify the local choice**.

Do not claim that the rejected alternative is generally inferior. When a result supports only correlation or a plausible explanation, say so directly. Place a material limitation next to the claim it bounds, then state what can still be concluded.

Prior work follows the same pattern. Describe a cited method by what it does and the setting it suits, and place the citation at the specific claim it supports rather than at the end of a paragraph. Citation habits such as *Ref. [n]* subjects versus bare *[n]*, and how densely citations appear, have not yet been measured. `style_check.py --detail` reports them for comparison after calibration.

## 9. Definitions, notation, and quantitative detail

Expand an acronym at first use and then use it consistently. Define a variable or diagnostic where it enters the reasoning, not in an isolated glossary-like sentence. After an equation, explain the physical or operational meaning of its important terms.

Quantities are often made concrete in operational units—seconds, minutes, number of evaluations, data points, dimensions, or tolerances. Use these numbers where they clarify feasibility or comparison. Do not carry a problem-specific number into an abstract-level claim without its metric and scope.

## 10. Figures and equations

Integrate a figure through:

**what it is for → feature to inspect → comparison or trend → inference → boundary if material**.

Natural openings include **Figure 4 shows…**, **Figure 4 illustrates…**, **As shown in Fig. 4,…**, and occasional **Note that…**. Do not narrate every curve or repeat the caption.

An equation is followed by the meaning of the variables and the consequence needed for the next step. Avoid leaving a derivation disconnected from the operational or physical question.

## 11. Register and recent evolution

The stable traits across 2022–2026 are concrete constraints, explicit logical links, method-based explanation, direct reporting verbs, and visible limitations.

The 2025–2026 papers carry more weight for the current voice. Relative to the 2022 material, they show:

- fewer first-person openings and more method/result subjects;
- more polished evaluative terms such as **principled, critical, leverage,** and **powerful**;
- more compact labeled decomposition in proceedings;
- more explicit balanced comparisons and statements of operational payoff;
- occasional dashes, colons, and compact enumerations.

Do not copy grammatical slips, PDF artifacts, or venue-specific typography. Use correct English while preserving the rhetorical pattern.

## 12. Final style audit

Before finalizing, check:

- Does the opening name the real setting or constraint rather than offer generic importance?
- Does each method choice have a visible reason?
- Are strong positive words supported nearby?
- Do **we**, technical subjects, and passive constructions each serve a clear role?
- Is the past tense used for work done and the present for method behavior and figures?
- Are contrast, cause, and consequence explicit where the reader needs them?
- Are comparisons bounded to the correct problem class?
- Does each figure discussion identify the feature and inference that matter?
- Are limitations placed once, next to the claim they bound?
- Does the conclusion synthesize rather than advertise?

## 13. Worked example

The pair below is a **constructed illustration**, not a quotation from any paper. Its technical content is schematic, and the bracketed placeholders stand for numbers that the source material must supply.

Generic draft:

> Bayesian optimization (BO) has emerged as a transformative paradigm for accelerator tuning, seamlessly navigating complex high-dimensional landscapes. In this work, we delve into a novel approach that harnesses a neural network prior to dramatically accelerate convergence, showcasing its remarkable potential for next-generation facilities.

In the documented voice:

> Beam tuning at FRIB must be repeated for each new ion species and charge state, and each evaluation consumes beam time. Bayesian optimization (BO) is well-suited to this setting because its probabilistic model uses all evaluated data to select the next setting, which reduces the number of evaluations required. However, BO starts without knowledge of the machine and may spend early evaluations in unpromising regions. To address this, we used a neural network trained on historical tuning data as the prior mean of the Gaussian process. This prior mean shifted the early search toward settings that had worked for similar beams. In the beam test, the prior-mean-assisted BO reached the target transmission in [N] evaluations, compared with [M] for BO with a constant prior mean. The benefit, however, depends on how closely the historical data represent the present beam.

The rewrite makes these moves:

1. It opens with the operational constraint.
2. It ties *well-suited* to a mechanism and an operational payoff.
3. It names the remaining difficulty with *However*.
4. It introduces the response with *To address this* and *we used*.
5. It carries the object forward with *This prior mean*.
6. It reports the result as a quantitative comparison.
7. It bounds the result with one qualification.

It also follows the tense rule. Past tense covers what was done (*used, shifted, reached*), and present tense covers what BO does (*uses, reduces*). The rewrite has no boosters or ornamental words.

