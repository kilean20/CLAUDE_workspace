"""Measure a draft against Kilean Hwang's recency-weighted published style.

Reads plain text or LaTeX (comments, math and commands are stripped) and reports sentence rhythm, agency,
contrast and cause/purpose links, qualification, transition openings, punctuation, typical sentence openers,
evaluative wording, conversational phrases, and generic flourishes. With --compare, selected measures are shown
against broad ranges derived from the post-2021 corpus with a two-year recency half-life. The ranges are diagnostics,
not writing requirements; the checker cannot determine whether a claim is supported or scientifically correct.

With --detail it also reports extended dimensions: tense, passive voice, nominalization, modal mix, boosters,
citation and acronym habits, quantitative density, sentence-opener types, "This + noun" anaphora, enumeration,
paragraph length, and recurring multi-word phrases (lexical bundles). These are regex approximations without a
part-of-speech tagger. They are not range-checked until scripts/corpus.py has calibrated them against the corpus.

Registers (see references/profile.md):
  journal      journal articles (default). Calibrated from his 2023 and 2026 first/corresponding-author PRAB papers.
  proceedings  conference proceedings, preprints, and reports. Calibrated from six Kilean-led texts from 2022-2025.

Usage:
    python style_check.py DRAFT [--tex] [--from TEXT] [--to TEXT] [--register journal|proceedings] [--compare]
                          [--detail] [--json]
      --from/--to   keep only the part between two literal markers (e.g. --from "\\section{Introduction}"
                    --to "\\section{Methods}"); markers are matched before LaTeX is stripped
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

# Rates are per 1,000 prose words unless the name says otherwise. "target" is a recency-weighted center;
# "band" is a deliberately generous diagnostic range. Punctuation is reported but not compared because equations,
# notation, captions and venue typesetting contaminate those counts. See references/profile.md.
PROFILES = {
    "proceedings": {
        "median_sentence_words": {"target": 19, "band": (16, 23)},
        "p90_sentence_words": {"target": 35, "band": (28, 48)},
        "short_sentence_share_pct": {"target": 17, "band": (5, 30)},
        "first_person": {"target": 13.0, "band": (4, 24)},
        "we_sentence_openers_pct": {"target": 7.5, "band": (2, 16)},
        "contrast_markers": {"target": 4.8, "band": (1, 12)},
        "cause_purpose_markers": {"target": 5.8, "band": (2, 13)},
        "qualification_markers": {"target": 8.0, "band": (2, 20)},
        "explicit_transition_openers": {"target": 5.7, "band": (1, 14)},
        "conversational_markers": {"target": 0.5, "band": (0, 5.0)},
        "generic_flourishes": {"target": 0.0, "band": (0, 1.0)},
    },
    "journal": {
        "median_sentence_words": {"target": 21, "band": (17, 24)},
        "p90_sentence_words": {"target": 36, "band": (29, 46)},
        "short_sentence_share_pct": {"target": 16, "band": (8, 28)},
        "first_person": {"target": 9.0, "band": (3, 18)},
        "we_sentence_openers_pct": {"target": 5.0, "band": (1, 12)},
        "contrast_markers": {"target": 5.1, "band": (1, 11)},
        "cause_purpose_markers": {"target": 5.7, "band": (2, 12)},
        "qualification_markers": {"target": 5.3, "band": (1, 16)},
        "explicit_transition_openers": {"target": 6.9, "band": (2, 14)},
        "conversational_markers": {"target": 0.5, "band": (0, 3.0)},
        "generic_flourishes": {"target": 0.0, "band": (0, 1.0)},
    },
}
GENERIC_FLOURISHES = [
    r"pivotal", r"seamless(?:ly)?", r"delv\w*", r"underscor\w*", r"showcas\w*", r"tapestry", r"realm",
    r"paramount", r"holistic", r"taken together", r"each level of evidence", r"answers? a different question",
    r"what \w+ adds is",
]
# These phrases are present in some early proceedings, but repeated use can make a formal draft sound casual.
CONVERSATIONAL = [
    r"(?:^|(?<=[.!?] ))(?:And|So|Anyway|Plus)[ ,]", r"\ba\.k\.a\.", r"better than nothing", r"\ba lot\b",
    r"\bkind of\b", r"\bpretty\b",
    r"\bstuff\b", r"\bthings\b", r"\bin a shot\b", r"\bon the fly\b",
]
FIRST_PERSON = r"\b(?:we|our|us|ours)\b"
CONTRAST = (
    r"\b(?:however|nevertheless|nonetheless|by contrast|in contrast|whereas|while|although|rather than|instead|"
    r"conversely|unlike)\b"
)
CAUSE_PURPOSE = (
    r"\b(?:because|therefore|thus|hence|due to|owing to|so that|in order to|to address|to mitigate|to reduce|"
    r"to improve|to minimize|to avoid|to enable|to further)\b"
)
QUALIFICATION = (
    r"\b(?:may|might|can|could|potentially|approximately|suggests?|appears?|is expected to|are expected to|"
    r"requires? further stud(?:y|ies)|under (?:these|the tested) conditions|outside (?:the )?scope)\b"
)
EVALUATIVE = [
    r"powerful", r"critical", r"principled", r"practical(?:ity)?", r"robust(?:ness)?", r"reliable|reliability",
    r"successful(?:ly)?", r"substantial(?:ly)?", r"promising", r"well[- ]suited", r"sample[- ]efficient",
]
TRANSITION_OPENERS = [
    "however", "therefore", "thus", "in addition", "additionally", "furthermore", "moreover",
    "nevertheless", "instead", "specifically", "for example", "to address this", "to mitigate this",
    "by contrast", "in contrast", "conversely", "finally", "although", "because", "while", "note that",
]

# Extended dimensions (reported with --detail). Approximations; see the module docstring.
_PARTICIPLES = (
    r"\w+ed|shown|known|given|taken|chosen|made|done|seen|found|written|driven|drawn|set|put|built|held|kept|left|run|"
    r"split|spent|fit|met|sent|brought|thought|understood|begun|grown|frozen|hidden"
)
PASSIVE = r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?(?:" + _PARTICIPLES + r")\b"
IRREGULAR_PAST = {
    "found", "chose", "made", "took", "ran", "built", "saw", "wrote", "began", "got", "did", "kept", "held", "drew",
    "gave", "led", "left", "met", "sent", "brought", "thought", "understood", "spent", "set", "put", "fit", "split",
}
MODALS = ("can", "could", "may", "might", "will", "would", "should", "must")
NOMINAL = r"\b[a-z]{3,}(?:tion|sion|ment|ance|ence)s?\b"
# Concrete or technical nouns with nominal suffixes; counting them would make the nominalization rate track topic.
NOT_NOMINAL = {
    "function", "section", "equation", "position", "station", "emittance", "distance", "instance", "reference",
    "sequence", "mention", "question", "fraction", "dimension", "science", "conference", "experience", "element",
    "segment", "solenoid", "acceptance", "resonance", "inductance", "capacitance", "abundance", "evidence",
}
BOOSTERS = (
    r"\b(?:significantly|clearly|very|highly|greatly|strongly|obviously|extremely|remarkably|dramatically|"
    r"considerably|notably|indeed|drastically|tremendously|vastly|surprisingly)\b"
)
NUMERIC_CITATION = r"\[\d+(?:\s*[-–,]\s*\d+)*\]"
ACRONYM = r"\b[A-Z][A-Z0-9]*[A-Z]s?\b"
NOT_ACRONYM = {"II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII", "FIG", "FIGS", "TABLE", "OK"}
LATIN_AND_POINTERS = {
    "e.g.": r"\be\.g\.", "i.e.": r"\bi\.e\.", "etc.": r"\betc\.", "respectively": r"\brespectively\b",
    "via": r"\bvia\b", "et al.": r"\bet al\.", "Ref.": r"\bRefs?\.",
}
ENUMERATION = r"\((?:i{1,3}|iv|v|vi|[1-6]|[a-f])\)"
CONTRACTION = r"\b\w+(?:n't|'re|'ve|'ll|'m)\b|\b(?:it|that|there|let)'s\b"
FIRST_PERSON_SINGULAR = r"\b(?:I|my|me|mine)\b"
# A sentence-initial "This" followed by one of these is a bare demonstrative; otherwise it is usually "This + noun".
BARE_THIS_NEXT = {
    "is", "was", "allows", "enables", "makes", "means", "leads", "results", "can", "could", "may", "will", "would",
    "has", "had", "provides", "gives", "shows", "suggests", "indicates", "implies", "ensures", "requires", "reduces",
    "helps", "demonstrates", "motivates", "highlights", "also", "in", "approach's",
}
FRAMING_OPENERS = (
    r"(?:in|for|with|by|as|at|on|from|since|when|if|after|before|during|using|based|given|unlike|compared|due|under|"
    r"once|without|through|among|beyond|despite|here|there|upon|within|across|following|assuming|considering)\b"
)


def strip_latex(s: str) -> str:
    s = re.sub(r"(?<!\\)%.*", "", s)
    s = re.sub(r"\\begin\{(equation|align|figure|table|tabular)\*?\}.*?\\end\{\1\*?\}", " ", s, flags=re.S)
    s = re.sub(r"\$[^$]*\$", " X ", s)
    s = re.sub(r"\\cite[tp]?(?:\[[^\]]*\])?\{[^}]*\}", " [0]", s)  # keeps citation density measurable
    s = re.sub(r"\\(?:ref|eqref|label|input|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}", " ", s)
    s = re.sub(r"\\(?:emph|textbf|textit|section|subsection|subsubsection)\*?\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", s)
    s = re.sub(r"[{}~]", " ", s)
    return s


def prepare_plain_text(text: str) -> str:
    """Remove obvious PDF furniture while retaining ordinary short prose lines."""
    kept = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            kept.append("")
            continue
        if re.match(r"^(?:FIG\.?|Figure)\s*\d+\s*[:.]", line, flags=re.I):
            continue
        if re.match(r"^\(?Received\b|^\*?Contact author:|^\d{6,}-\d+$", line, flags=re.I):
            continue
        if len(line) < 90 and re.fullmatch(r"[A-Z0-9 .,:/&+\-–—()]+", line) and not re.search(r"[.!?]$", line):
            continue
        letters = sum(c.isalpha() for c in line)
        visible = sum(not c.isspace() for c in line)
        if visible and letters / visible < 0.35:
            continue
        kept.append(line)
    return "\n".join(kept)


def sentences(text: str) -> list[str]:
    flat = re.sub(r"\s+", " ", prepare_plain_text(text))
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(])", flat)
    return [p.strip() for p in parts if len(re.findall(r"[A-Za-z]{2,}", p)) >= 4]


def measure(text: str) -> dict:
    sents = sentences(text)
    prose = " ".join(sents)
    words = re.findall(r"[A-Za-z][A-Za-z'\-]*", prose)
    n = max(len(words), 1)
    lengths = sorted(len(re.findall(r"[A-Za-z][A-Za-z'\-]*", s)) for s in sents) or [0]
    per_k = lambda count: round(1000 * count / n, 1)
    flat = re.sub(r"\s+", " ", prose)
    openers = Counter(re.sub(r"[^A-Za-z]", "", s.split()[0]) for s in sents if s.split())
    flourish_hits, casual_hits, evaluative_hits = Counter(), Counter(), Counter()
    for pattern in GENERIC_FLOURISHES:
        for m in re.finditer(r"\b" + pattern + r"\b", flat, flags=re.I):
            flourish_hits[m.group(0).lower()] += 1
    for pattern in CONVERSATIONAL:
        for m in re.finditer(pattern, flat):
            casual_hits[m.group(0).strip().lower()] += 1
    for pattern in EVALUATIVE:
        for m in re.finditer(r"\b" + pattern + r"\b", flat, flags=re.I):
            evaluative_hits[m.group(0).lower()] += 1
    transition_hits = Counter()
    for sentence in sents:
        low = sentence.lower().lstrip("( ")
        opener = next((p for p in TRANSITION_OPENERS if low.startswith(p)), None)
        if opener:
            transition_hits[opener] += 1
    we_openers = sum(bool(re.match(r"^(?:In this (?:work|paper),? )?[Ww]e\b", s)) for s in sents)
    return {
        "words": n,
        "sentences": len(sents),
        "median_sentence_words": statistics.median(lengths),
        "p90_sentence_words": lengths[int(0.9 * (len(lengths) - 1))],
        "short_sentence_share_pct": round(100 * sum(1 for x in lengths if x < 12) / max(len(sents), 1)),
        "semicolons": per_k(prose.count(";")),
        "colons_in_prose": per_k(len(re.findall(r"[a-z\)]: [a-z]", prose))),
        "dashes_as_punctuation": per_k(len(re.findall(r"\s(?:--|—|–)\s|\w—\w", prose))),
        "parentheses": per_k(prose.count("(")),
        "first_person": per_k(len(re.findall(FIRST_PERSON, prose, flags=re.I))),
        "we_sentence_openers_pct": round(100 * we_openers / max(len(sents), 1), 1),
        "contrast_markers": per_k(len(re.findall(CONTRAST, prose, flags=re.I))),
        "cause_purpose_markers": per_k(len(re.findall(CAUSE_PURPOSE, prose, flags=re.I))),
        "qualification_markers": per_k(len(re.findall(QUALIFICATION, prose, flags=re.I))),
        "explicit_transition_openers": per_k(sum(transition_hits.values())),
        "conversational_markers": per_k(sum(casual_hits.values())),
        "rather_than": per_k(len(re.findall(r"\brather than\b", prose, flags=re.I))),
        "generic_flourishes": per_k(sum(flourish_hits.values())),
        "generic_flourish_hits": dict(flourish_hits.most_common()),
        "conversational_hits": dict(casual_hits.most_common()),
        "evaluative_terms": per_k(sum(evaluative_hits.values())),
        "evaluative_term_hits": dict(evaluative_hits.most_common()),
        "transition_opener_hits": dict(transition_hits.most_common()),
        "top_openers": dict(openers.most_common(8)),
        **measure_extended(text, sents, prose, lengths, per_k),
    }


def opener_category(sentence: str) -> str:
    low = sentence.lower().lstrip("( ")
    if re.match(r"(?:in this (?:work|paper|study),? )?(?:we|our)\b", low):
        return "we"
    if any(low.startswith(p) for p in TRANSITION_OPENERS):
        return "connector"
    if re.match(r"(?:fig\.|figs\.|figure|figures|table|eq\.|eqs\.|equation)\s", low):
        return "figure_table_equation"
    if re.match(r"(?:this|these|such|those)\b", low):
        return "this_these_such"
    if re.match(r"to [a-z]+\b", low):
        return "purpose_infinitive"
    if re.match(FRAMING_OPENERS, low):
        return "framing_phrase"
    if re.match(r"(?:the|a|an)\b", low):
        return "article_subject"
    return "other_subject"


def bundles(sents: list[str], n: int) -> Counter:
    """Count word n-grams within sentences (lexical bundles); numbers and symbols break a bundle."""
    counts: Counter = Counter()
    for sentence in sents:
        for chunk in re.split(r"[^A-Za-z'\- ]+", sentence):
            toks = chunk.lower().split()
            counts.update(" ".join(toks[i : i + n]) for i in range(len(toks) - n + 1))
    return counts


def measure_extended(text: str, sents: list[str], prose: str, lengths: list[int], per_k) -> dict:
    words_lower = re.findall(r"[a-z][a-z'\-]*", prose.lower())
    be_present = len(re.findall(r"\b(?:is|are)\b", prose, flags=re.I))
    be_past = len(re.findall(r"\b(?:was|were)\b", prose, flags=re.I))
    we_tense = Counter()
    for m in re.finditer(r"\bwe\s+(?:also\s+|then\s+|first\s+|further\s+|additionally\s+)?([a-z]+)\b", prose, flags=re.I):
        verb = m.group(1).lower()
        if verb in MODALS:
            we_tense["modal"] += 1
        elif verb in ("have", "has"):
            we_tense["perfect"] += 1
        elif verb.endswith("ed") or verb in IRREGULAR_PAST or verb == "had":
            we_tense["past"] += 1
        elif not verb.endswith("ly"):
            we_tense["present"] += 1
    modal_counts = Counter(w for w in words_lower if w in MODALS)
    nominal = [w for w in re.findall(NOMINAL, prose.lower()) if w.rstrip("s") not in NOT_NOMINAL]
    acronyms = [a for a in re.findall(ACRONYM, prose) if a not in NOT_ACRONYM and a.rstrip("s") not in NOT_ACRONYM]
    categories = Counter(opener_category(s) for s in sents)
    this_openers = [s.split() for s in sents if re.match(r"\(?(?:This|These)\b", s)]
    bare_this = sum(1 for toks in this_openers if len(toks) > 1 and toks[1].lower().strip(",") in BARE_THIS_NEXT)
    paragraphs = [p for p in re.split(r"\n\s*\n", prepare_plain_text(text)) if sentences(p)]
    para_sizes = sorted(len(sentences(p)) for p in paragraphs) or [0]
    four, three = bundles(sents, 4), bundles(sents, 3)
    mean = statistics.mean(lengths) if lengths else 0
    return {
        "mean_sentence_words": round(mean, 1),
        "sentence_length_cv": round(statistics.pstdev(lengths) / mean, 2) if mean else 0,
        "passive_constructions": per_k(len(re.findall(PASSIVE, prose, flags=re.I))),
        "comma_ing_clauses": per_k(len(re.findall(r",\s+(?:thereby\s+)?[a-z]{3,}ing\b", prose))),
        "be_past_share_pct": round(100 * be_past / max(be_present + be_past, 1)),
        "we_verb_tense": dict(we_tense.most_common()),
        "nominalizations": per_k(len(nominal)),
        "modal_verbs": per_k(sum(modal_counts.values())),
        "modal_share_pct": {k: round(100 * v / max(sum(modal_counts.values()), 1)) for k, v in modal_counts.most_common()},
        "boosters": per_k(len(re.findall(BOOSTERS, prose, flags=re.I))),
        "booster_hits": dict(Counter(m.lower() for m in re.findall(BOOSTERS, prose, flags=re.I)).most_common()),
        "first_person_singular": per_k(len(re.findall(FIRST_PERSON_SINGULAR, prose))),
        "contractions": per_k(len(re.findall(CONTRACTION, prose))),
        "questions": sum(1 for s in sents if s.rstrip().endswith("?")),
        "numeric_citations": per_k(len(re.findall(NUMERIC_CITATION, prose))),
        "pointer_hits": {k: c for k, p in LATIN_AND_POINTERS.items() if (c := len(re.findall(p, prose)))},
        "acronym_tokens": per_k(len(acronyms)),
        "distinct_acronyms": len(set(a.rstrip("s") for a in acronyms)),
        "acronym_definitions": len(re.findall(r"\([A-Z][A-Za-z0-9\-]*[A-Z]s?\)", prose)),
        "numbers": per_k(len(re.findall(r"(?<![A-Za-z\[])\d+(?:\.\d+)?(?![\]\d])", prose))),
        "enumeration_markers": per_k(len(re.findall(ENUMERATION, prose))),
        "opener_category_pct": {k: round(100 * v / max(len(sents), 1)) for k, v in categories.most_common()},
        "this_these_openers": len(this_openers),
        "bare_this_openers": bare_this,
        "paragraphs": len(paragraphs),
        "paragraph_median_sentences": statistics.median(para_sizes),
        "top_4gram_bundles": {k: v for k, v in four.most_common(12) if v >= 2},
        "top_3gram_bundles": {k: v for k, v in three.most_common(12) if v >= 2},
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("--tex", action="store_true", help="strip LaTeX first (default for .tex files)")
    ap.add_argument("--from", dest="start")
    ap.add_argument("--to", dest="end")
    ap.add_argument("--register", choices=sorted(PROFILES), default="journal")
    ap.add_argument("--compare", action="store_true")
    ap.add_argument("--detail", action="store_true", help="also report the extended (uncalibrated) dimensions")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    raw = Path(a.draft).read_text(encoding="utf-8", errors="replace")
    if a.start:
        raw = raw[raw.find(a.start):]
    if a.end and a.end in raw:
        raw = raw[: raw.find(a.end)]
    text = strip_latex(raw) if (a.tex or a.draft.endswith(".tex")) else raw
    m = measure(text)
    if a.json:
        print(json.dumps(m, indent=1))
        return
    profile = PROFILES[a.register]
    print(f"{m['words']} words, {m['sentences']} sentences (register: {a.register})")
    if a.compare and m["words"] < 400:
        print("  note: fewer than 400 prose words; rate comparisons are unstable")
    outside = 0
    for key, spec in profile.items():
        value = m[key]
        line = f"  {key:26s} {value:6}"
        if a.compare:
            lo, hi = spec["band"]
            ok = lo <= value <= hi
            outside += not ok
            line += f"   target {spec['target']:>5}   range {lo}-{hi}{'' if ok else '  <-- outside'}"
        print(line)
    print(
        "  punctuation diagnostics:"
        f" semicolons {m['semicolons']}/1k, colons {m['colons_in_prose']}/1k,"
        f" dashes {m['dashes_as_punctuation']}/1k, parentheses {m['parentheses']}/1k"
    )
    if m["generic_flourish_hits"]:
        print("  generic flourishes:", ", ".join(f"{k} x{v}" for k, v in m["generic_flourish_hits"].items()))
    if m["conversational_hits"]:
        print("  conversational markers:", ", ".join(f"{k} x{v}" for k, v in m["conversational_hits"].items()))
    if m["evaluative_term_hits"]:
        print("  evaluative terms (inspect support, do not remove automatically):", ", ".join(f"{k} x{v}" for k, v in m["evaluative_term_hits"].items()))
    if m["transition_opener_hits"]:
        print("  transition openers:", ", ".join(f"{k} x{v}" for k, v in m["transition_opener_hits"].items()))
    print("  top sentence openers:", ", ".join(f"{k} x{v}" for k, v in m["top_openers"].items()))
    if a.compare:
        print(f"  {outside} of {len(profile)} measures outside the {a.register} range")
    if a.detail:
        print_detail(m)


def print_detail(m: dict) -> None:
    fmt = lambda d: ", ".join(f"{k} {v}" for k, v in d.items()) or "none"
    print("  extended dimensions (regex approximations, not range-checked):")
    print(
        f"    sentences: mean {m['mean_sentence_words']} words, length CV {m['sentence_length_cv']};"
        f" paragraphs {m['paragraphs']}, median {m['paragraph_median_sentences']} sentences each"
    )
    print(f"    tense: was/were share of be-verbs {m['be_past_share_pct']}%; 'we + verb' {fmt(m['we_verb_tense'])}")
    print(
        f"    voice and density: passive {m['passive_constructions']}/1k, ', -ing' clauses {m['comma_ing_clauses']}/1k,"
        f" nominalizations {m['nominalizations']}/1k,"
        f" numbers {m['numbers']}/1k, enumeration markers {m['enumeration_markers']}/1k"
    )
    print(f"    modals {m['modal_verbs']}/1k ({fmt(m['modal_share_pct'])}); boosters {m['boosters']}/1k ({fmt(m['booster_hits'])})")
    print(
        f"    references: numeric citations {m['numeric_citations']}/1k; pointers {fmt(m['pointer_hits'])};"
        f" acronyms {m['acronym_tokens']}/1k, {m['distinct_acronyms']} distinct, {m['acronym_definitions']} defined in parentheses"
    )
    print(f"    opener types: {fmt(m['opener_category_pct'])} (% of sentences)")
    print(f"    This/These openers {m['this_these_openers']}, of which bare demonstrative {m['bare_this_openers']}")
    print(
        f"    register flags: I/my/me {m['first_person_singular']}/1k, contractions {m['contractions']}/1k,"
        f" questions {m['questions']}"
    )
    print(f"    recurring 4-word phrases: {fmt(m['top_4gram_bundles'])}")
    print(f"    recurring 3-word phrases: {fmt(m['top_3gram_bundles'])}")


if __name__ == "__main__":
    sys.exit(main())
