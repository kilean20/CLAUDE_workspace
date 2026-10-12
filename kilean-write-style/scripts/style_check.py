"""Measure a draft against Kilean Hwang's recency-weighted published style.

Reads plain text or LaTeX (comments, math and commands are stripped) and reports sentence rhythm, agency,
contrast and cause/purpose links, qualification, transition openings, punctuation, typical sentence openers,
evaluative wording, conversational phrases, and generic flourishes. With --compare, selected measures are shown
against broad ranges derived from the post-2021 corpus with a two-year recency half-life. The ranges are diagnostics,
not writing requirements; the checker cannot determine whether a claim is supported or scientifically correct.

Registers (see references/profile.md):
  journal      journal articles (default). Calibrated from his 2023 and 2026 first/corresponding-author PRAB papers.
  proceedings  conference proceedings, preprints, and reports. Calibrated from six Kilean-led texts from 2022-2025.

Usage:
    python style_check.py DRAFT [--tex] [--from TEXT] [--to TEXT] [--register journal|proceedings] [--compare] [--json]
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


def strip_latex(s: str) -> str:
    s = re.sub(r"(?<!\\)%.*", "", s)
    s = re.sub(r"\\begin\{(equation|align|figure|table|tabular)\*?\}.*?\\end\{\1\*?\}", " ", s, flags=re.S)
    s = re.sub(r"\$[^$]*\$", " X ", s)
    s = re.sub(r"\\(?:cite[tp]?|ref|eqref|label|input|includegraphics)(?:\[[^\]]*\])?\{[^}]*\}", " ", s)
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
        "rather_than": per_k(len(re.findall(r"\brather than\b", text, flags=re.I))),
        "generic_flourishes": per_k(sum(flourish_hits.values())),
        "generic_flourish_hits": dict(flourish_hits.most_common()),
        "conversational_hits": dict(casual_hits.most_common()),
        "evaluative_terms": per_k(sum(evaluative_hits.values())),
        "evaluative_term_hits": dict(evaluative_hits.most_common()),
        "transition_opener_hits": dict(transition_hits.most_common()),
        "top_openers": dict(openers.most_common(8)),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft")
    ap.add_argument("--tex", action="store_true", help="strip LaTeX first (default for .tex files)")
    ap.add_argument("--from", dest="start")
    ap.add_argument("--to", dest="end")
    ap.add_argument("--register", choices=sorted(PROFILES), default="journal")
    ap.add_argument("--compare", action="store_true")
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


if __name__ == "__main__":
    sys.exit(main())
