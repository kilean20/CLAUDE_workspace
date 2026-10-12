"""Rebuild the evidence behind the kilean-write-style skill from Kilean Hwang's post-2021 lead-author papers.

  fetch     download each paper in MANIFEST (or copy <id>.pdf / <id>.txt from --pdf-dir), extract the prose with
            pdftotext, drop page furniture and the reference list, and cache the text outside the repository
  profile   measure every cached text with style_check.measure() and print a recency-weighted Markdown report per
            register: core and extended dimensions, opener types, modal and tense mix, recurring phrases (lexical
            bundles), the words that rose or fell between 2022-2023 and 2025-2026, and suggested checker ranges

Recency weight = 0.5 ** ((ref_year - year) / half_life), with ref_year the newest manifest year and a two-year
half-life by default (see references/profile.md). Paper text stays in the cache because the skill needs only the
measurements; review the extracted text once after a fresh fetch, since PDF layouts differ between venues.

Usage:
    python scripts/corpus.py fetch [--cache DIR] [--pdf-dir DIR] [--only ID ...]
    python scripts/corpus.py profile [--cache DIR] [--half-life YEARS] [--ref-year YEAR] [--json]
"""
from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import urllib.request
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from style_check import PROFILES, bundles, measure, sentences  # noqa: E402

DEFAULT_CACHE = Path.home() / ".cache" / "kilean-write-style"
# Kilean-led texts after 2021 (first author; corresponding author for the journal papers). URLs are tried in order.
MANIFEST = [
    {"id": "ipac2022", "year": 2022, "register": "proceedings",
     "title": "Beam Tuning at the FRIB Front End Using Machine Learning",
     "urls": ["https://proceedings.jacow.org/ipac2022/pdf/TUPOST053.pdf",
              "https://jacow.org/ipac2022/papers/tupost053.pdf"]},
    {"id": "pmbo2022", "year": 2022, "register": "proceedings",
     "title": "Prior-mean-assisted Bayesian optimization application on FRIB Front-End tunning (arXiv:2211.06400)",
     "urls": ["https://arxiv.org/pdf/2211.06400"]},
    {"id": "prab2023", "year": 2023, "register": "journal",
     "title": "Machine learning based phase space tomography using kicked beam turn-by-turn centroid data",
     "urls": ["https://journals.aps.org/prab/pdf/10.1103/PhysRevAccelBeams.26.104601",
              "https://link.aps.org/pdf/10.1103/PhysRevAccelBeams.26.104601"]},
    {"id": "linac2024", "year": 2024, "register": "proceedings",
     "title": "Machine-learning-assisted beam tuning at FRIB",
     "urls": ["https://proceedings.jacow.org/linac2024/pdf/THXA004.pdf"]},
    {"id": "hiat2025", "year": 2025, "register": "proceedings",
     "title": "Application of ML tools for extraction of BPM-Q and transverse beam matching",
     "urls": ["https://proceedings.jacow.org/hiat2025/pdf/TUP11.pdf"]},
    {"id": "icalepcs2025", "year": 2025, "register": "proceedings",
     "title": "Bayesian active learning for converging posteriors in latent variable inference for control systems",
     "urls": ["https://proceedings.jacow.org/icalepcs2025/pdf/WEPD075.pdf"]},
    {"id": "napac2025", "year": 2025, "register": "proceedings",
     "title": "Advanced ML methods for beam tuning at FRIB",
     "urls": ["https://proceedings.jacow.org/napac2025/pdf/THXN01.pdf"]},
    {"id": "prab2026", "year": 2026, "register": "journal",
     "title": "Customized Bayesian optimization for efficient beam tuning at the facility for rare isotope beams",
     "urls": ["https://journals.aps.org/prab/pdf/10.1103/5hyd-bhpx",
              "https://link.aps.org/pdf/10.1103/5hyd-bhpx",
              "https://www.osti.gov/pages/servlets/purl/3377202"]},
]
FURNITURE = re.compile(
    r"Content from this work may be used|Any distribution of this work|JACoW|ISBN|ISSN|doi: ?10\.18429|"
    r"Published by the American Physical Society|Creative Commons|PHYS\. REV\. ACCEL\. BEAMS|^\s*\d{6}-\d+\s*$|"
    r"^\s*[A-Z]{1,3}\d{1,2}(?:\.[A-Z]\d{1,2})?:\s|^\s*\*\s*Work supported|^\s*†|^\s*\S+@\S+\s*$|arXiv:\d{4}\.\d{4,5}",
    re.I,
)
FUNCTION_WORDS = {
    "the", "of", "to", "in", "a", "an", "is", "are", "be", "for", "on", "with", "as", "by", "that", "this", "which",
    "can", "it", "we", "our", "from", "at", "and", "or", "not", "than", "such", "these", "each", "its", "into",
}


def fetch(args) -> None:
    pdf_dir, text_dir = args.cache / "pdf", args.cache / "text"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)
    for entry in MANIFEST:
        if args.only and entry["id"] not in args.only:
            continue
        pdf, txt = pdf_dir / f"{entry['id']}.pdf", text_dir / f"{entry['id']}.txt"
        local = args.pdf_dir / f"{entry['id']}" if args.pdf_dir else None
        if local and local.with_suffix(".txt").exists():
            raw = local.with_suffix(".txt").read_text(encoding="utf-8", errors="replace")
        else:
            if local and local.with_suffix(".pdf").exists():
                shutil.copyfile(local.with_suffix(".pdf"), pdf)
            elif not pdf.exists() and not download(entry, pdf):
                print(f"{entry['id']}: not fetched (put {entry['id']}.pdf in --pdf-dir to supply it)")
                continue
            raw = pdf_to_text(pdf)
        body = clean(raw)
        txt.write_text(body, encoding="utf-8")
        lines = [ln for ln in body.splitlines() if ln.strip()]
        m = measure(body)
        print(f"{entry['id']}: {m['words']} prose words, {m['sentences']} sentences -> {txt}")
        print(f"    starts: {lines[0][:100] if lines else ''}")
        print(f"    ends:   {lines[-1][:100] if lines else ''}")


def download(entry: dict, dest: Path) -> bool:
    for url in entry["urls"]:
        req = urllib.request.Request(url, headers={"User-Agent": "kilean-write-style corpus builder (research use)"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
        except Exception as exc:  # network policy, 404, bot protection
            print(f"{entry['id']}: {url} failed ({exc})")
            continue
        if data.startswith(b"%PDF"):
            dest.write_bytes(data)
            return True
        print(f"{entry['id']}: {url} did not return a PDF")
    return False


def pdf_to_text(pdf: Path) -> str:
    if shutil.which("pdftotext"):
        return subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"], capture_output=True, text=True).stdout
    from pypdf import PdfReader  # fallback when poppler is missing

    return "\n\n".join(page.extract_text() or "" for page in PdfReader(str(pdf)).pages)


def clean(raw: str) -> str:
    """Keep abstract-through-conclusion prose: drop furniture, rejoin hyphenated words, cut the reference list."""
    lines = [ln for ln in raw.replace("\f", "\n").splitlines() if not FURNITURE.search(ln)]
    text = re.sub(r"(\w)-\n(?=[a-z])", r"\1", "\n".join(lines))
    head = re.search(r"^\s*(?:Abstract|ABSTRACT)\b[.:]?", text, flags=re.M)
    received = re.search(r"^\s*\(Received[^\n]*\n", text, flags=re.M)
    if head and head.start() < 0.4 * len(text):
        text = text[head.end():]
    elif received and received.start() < 0.4 * len(text):
        text = text[received.end():]
    tail = [m.start() for m in re.finditer(r"^\s*(?:[IVX]+\.\s*)?(?:REFERENCES|References|ACKNOWLEDG\w*|Acknowledg\w*)\s*$",
                                           text, flags=re.M) if m.start() > 0.5 * len(text)]
    if tail:
        text = text[: min(tail)]
    return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def weight(year: int, ref_year: int, half_life: float) -> float:
    return 0.5 ** ((ref_year - year) / half_life)


def wmean(pairs: list[tuple[float, float]]) -> float:
    total = sum(w for _, w in pairs)
    return sum(v * w for v, w in pairs) / total if total else 0.0


def load(cache: Path, ref_year: int, half_life: float) -> list[dict]:
    texts = []
    for entry in MANIFEST:
        path = cache / "text" / f"{entry['id']}.txt"
        if path.exists():
            body = path.read_text(encoding="utf-8")
            texts.append({**entry, "text": body, "m": measure(body), "w": weight(entry["year"], ref_year, half_life)})
    return texts


def rates(texts: list[dict], counter) -> list[dict]:
    """Per-text rates per 1,000 words for every key a counter function returns."""
    return [{k: 1000 * v / max(t["m"]["words"], 1) for k, v in counter(t).items()} for t in texts]


def bundle_table(texts: list[dict], n: int, top: int) -> list[tuple[str, float, int]]:
    per_text = rates(texts, lambda t: bundles(sentences(t["text"]), n))
    keys = {k for r in per_text for k in r}
    need = max(2, math.ceil(len(texts) / 2))
    rows = []
    for k in keys:
        spread = sum(1 for r in per_text if k in r)
        if spread >= need and set(k.split()) & FUNCTION_WORDS:
            rows.append((k, wmean([(r.get(k, 0.0), t["w"]) for r, t in zip(per_text, texts)]), spread))
    return sorted(rows, key=lambda row: -row[1])[:top]


def evolution(texts: list[dict], ref_year: int, top: int) -> tuple[list, list]:
    recent = [t for t in texts if t["year"] >= ref_year - 1]
    early = [t for t in texts if t["year"] <= ref_year - 3]
    if not recent or not early:
        return [], []
    tokens = lambda t: Counter(re.findall(r"[a-z][a-z\-]+", " ".join(sentences(t["text"])).lower()))
    per_text = rates(texts, tokens)
    df = Counter(k for r in per_text for k in r)
    by_id = {t["id"]: r for t, r in zip(texts, per_text)}
    rows = []
    for k, d in df.items():
        if d < 3:
            continue
        a = wmean([(by_id[t["id"]].get(k, 0.0), t["w"]) for t in early])
        b = wmean([(by_id[t["id"]].get(k, 0.0), t["w"]) for t in recent])
        if a + b >= 0.6:
            rows.append((k, round(a, 2), round(b, 2), math.log((b + 0.1) / (a + 0.1))))
    rows.sort(key=lambda row: row[3])
    return rows[::-1][:top], rows[:top]


def profile(args) -> None:
    texts = load(args.cache, args.ref_year, args.half_life)
    if not texts:
        sys.exit(f"no cached texts in {args.cache / 'text'}; run `corpus.py fetch` first")
    report: dict = {"ref_year": args.ref_year, "half_life": args.half_life, "registers": {}}
    scalar_keys = [k for k, v in texts[0]["m"].items() if isinstance(v, (int, float))]
    dict_keys = ["opener_category_pct", "modal_share_pct", "we_verb_tense", "pointer_hits"]
    for register in ("journal", "proceedings"):
        group = [t for t in texts if t["register"] == register]
        if not group:
            continue
        reg: dict = {"texts": {t["id"]: round(t["w"], 2) for t in group}, "scalars": {}, "mixes": {}}
        for k in scalar_keys:
            vals = [(t["m"][k], t["w"]) for t in group]
            reg["scalars"][k] = {"center": round(wmean(vals), 1), "min": min(v for v, _ in vals),
                                 "max": max(v for v, _ in vals), "by_text": {t["id"]: t["m"][k] for t in group}}
        for k in dict_keys:
            shares = []
            for t in group:
                d = t["m"][k]
                if d:  # a text without any occurrence says nothing about the mix
                    shares.append(({kk: 100 * vv / sum(d.values()) for kk, vv in d.items()}, t["w"]))
            keys = {kk for d, _ in shares for kk in d}
            reg["mixes"][k] = dict(sorted(((kk, round(wmean([(d.get(kk, 0.0), w) for d, w in shares]), 1)) for kk in keys),
                                          key=lambda kv: -kv[1]))
        reg["bundles_4"] = bundle_table(group, 4, 25)
        reg["bundles_3"] = bundle_table(group, 3, 25)
        reg["suggested_bands"] = {
            k: {"target": reg["scalars"][k]["center"],
                "band": (math.floor(0.8 * reg["scalars"][k]["min"]), math.ceil(1.2 * reg["scalars"][k]["max"]))}
            for k in PROFILES[register]
        }
        report["registers"][register] = reg
    rising, falling = evolution(texts, args.ref_year, 30)
    report["evolution"] = {"rising": rising, "falling": falling}
    report["bundles_all_4"] = bundle_table(texts, 4, 30)
    report["bundles_all_3"] = bundle_table(texts, 3, 30)
    if args.json:
        print(json.dumps(report, indent=1))
    else:
        print_report(report)


def print_report(report: dict) -> None:
    print(f"# Corpus profile (reference year {report['ref_year']}, half-life {report['half_life']} years)\n")
    for register, reg in report["registers"].items():
        ids = list(reg["texts"])
        print(f"## {register} ({', '.join(f'{i} w={w}' for i, w in reg['texts'].items())})\n")
        print("| measure | weighted center | " + " | ".join(ids) + " |")
        print("|---|---:|" + "---:|" * len(ids))
        for k, s in reg["scalars"].items():
            print(f"| {k} | {s['center']} | " + " | ".join(str(s["by_text"][i]) for i in ids) + " |")
        for k, mix in reg["mixes"].items():
            print(f"\n{k} (weighted % of occurrences): " + ", ".join(f"{kk} {vv}" for kk, vv in mix.items()))
        for n in (4, 3):
            print(f"\n{n}-word bundles in at least half the {register} texts (weighted rate per 1k, texts): "
                  + "; ".join(f"{b} {r:.2f} ({c})" for b, r, c in reg[f"bundles_{n}"]))
        print("\nsuggested PROFILES entries (review before adopting):")
        print(json.dumps(reg["suggested_bands"], indent=1))
        print()
    for n in (4, 3):
        print(f"## {n}-word bundles across both registers\n")
        print("; ".join(f"{b} {r:.2f} ({c})" for b, r, c in report[f"bundles_all_{n}"]) + "\n")
    print("## Evolution: 2022-2023 versus the newest two years (weighted rate per 1k words)\n")
    for label in ("rising", "falling"):
        rows = report["evolution"][label]
        print(f"{label}: " + "; ".join(f"{w} {a}->{b}" for w, a, b, _ in rows) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    f.add_argument("--pdf-dir", type=Path, help="directory holding <id>.pdf or <id>.txt files to use instead of URLs")
    f.add_argument("--only", nargs="*", help="manifest ids to process")
    p = sub.add_parser("profile")
    p.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    p.add_argument("--half-life", type=float, default=2.0)
    p.add_argument("--ref-year", type=int, default=max(e["year"] for e in MANIFEST))
    p.add_argument("--json", action="store_true")
    args = ap.parse_args()
    fetch(args) if args.cmd == "fetch" else profile(args)


if __name__ == "__main__":
    main()
