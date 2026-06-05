#!/usr/bin/env python3
"""
quote_gate.py - deterministic quote verification for paper-workshop.

An LLM verifier shares the hallucination it is meant to catch, so quote
grounding (grounding rule 10) is enforced by THIS script, not by a model.
It normalizes a candidate quote and the source text and checks for a 1:1
substring match. It fails CLOSED: no match => the finding's quote is not
verified and must be downgraded to 'needs-author-confirmation'.

Findings of type 'absence-silence' carry an empty quote and are EXEMPT
(grounding rule 9): batch mode reports them as match_level='exempt-absence'.

No third-party dependencies (stdlib only) so it runs anywhere Python 3.8+ is.

USAGE
  Single check (quote inline or from a file/stdin), source from a file:
    python quote_gate.py check --source-file SRC.txt --quote "the exact text"
    python quote_gate.py check --source-file SRC.txt --quote-file Q.txt
    echo "the exact text" | python quote_gate.py check --source-file SRC.txt --quote-stdin

  Batch (verify every finding's quote against the source):
    python quote_gate.py batch --source-file SRC.txt --findings findings.json
  -> prints a JSON array: [{"id","matched","match_level","severity_hint"}...]
     match_level in: normalized | dehyphenated | exempt-absence | none
     exit code 0 if all non-exempt findings matched, 2 otherwise.

The same normalization is used everywhere so results are reproducible.
"""
import argparse
import json
import re
import sys
import unicodedata

# Characters PDF/Word extraction mangles, mapped to a canonical form.
_QUOTES = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"', "‟": '"',
    "«": '"', "»": '"', "‹": "'", "›": "'",
    "`": "'", "´": "'",
}
_DASHES = {
    "‐": "-", "‑": "-", "‒": "-", "–": "-",
    "—": "-", "―": "-", "−": "-",
}
_SPACES = {
    " ": " ", " ": " ", " ": " ", " ": " ",
    " ": " ", " ": " ", " ": " ", " ": " ",
    " ": " ", "\t": " ", "\r": " ", "\n": " ", "\f": " ",
}
_TRANS = {ord(k): v for k, v in {**_QUOTES, **_DASHES, **_SPACES}.items()}


def normalize(text, casefold=True):
    """Canonicalize text for matching. Deterministic and idempotent."""
    if text is None:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(_TRANS)
    if casefold:
        text = text.casefold()
    # collapse runs of whitespace to a single space
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def dehyphenate(text):
    """Join words split by a soft hyphen at a (former) line break: 'inter- national' -> 'international'."""
    return re.sub(r"-\s+", "", text)


def check(quote, source, casefold=True):
    """Return (matched: bool, match_level: str). Tries exact-normalized first,
    then a dehyphenated fallback for PDF line-break hyphenation."""
    nq = normalize(quote, casefold)
    if nq == "":
        return True, "exempt-absence"
    ns = normalize(source, casefold)
    if nq in ns:
        return True, "normalized"
    # PDF hyphenation fallback (applied to BOTH so a hyphenated source still matches)
    if dehyphenate(nq) in dehyphenate(ns):
        return True, "dehyphenated"
    return False, "none"


def _read_quote(args):
    if args.quote is not None:
        return args.quote
    if args.quote_file:
        with open(args.quote_file, encoding="utf-8") as fh:
            return fh.read()
    if args.quote_stdin:
        return sys.stdin.read()
    raise SystemExit("provide --quote, --quote-file, or --quote-stdin")


def cmd_check(args):
    with open(args.source_file, encoding="utf-8") as fh:
        source = fh.read()
    quote = _read_quote(args)
    matched, level = check(quote, source, casefold=not args.case_sensitive)
    print(json.dumps({"matched": matched, "match_level": level}))
    return 0 if matched else 2


def cmd_batch(args):
    with open(args.source_file, encoding="utf-8") as fh:
        source = fh.read()
    with open(args.findings, encoding="utf-8") as fh:
        data = json.load(fh)
    findings = data["findings"] if isinstance(data, dict) and "findings" in data else data
    out = []
    all_ok = True
    for f in findings:
        quote = f.get("quote", "")
        is_absence = f.get("finding_type") == "absence-silence"
        if is_absence and normalize(quote) == "":
            out.append({"id": f.get("id"), "matched": True, "match_level": "exempt-absence",
                        "severity_hint": "keep"})
            continue
        matched, level = check(quote, source, casefold=not args.case_sensitive)
        if not matched:
            all_ok = False
        out.append({
            "id": f.get("id"),
            "matched": matched,
            "match_level": level,
            # advisory only: the gate annotates; it never vetoes severity (rubric.md)
            "severity_hint": "keep" if matched else "downgrade-status-to-needs-author-confirmation",
        })
    print(json.dumps(out, indent=2))
    return 0 if all_ok else 2


def main(argv=None):
    p = argparse.ArgumentParser(description="Deterministic quote gate for paper-workshop.")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="check a single quote")
    c.add_argument("--source-file", required=True)
    c.add_argument("--quote")
    c.add_argument("--quote-file")
    c.add_argument("--quote-stdin", action="store_true")
    c.add_argument("--case-sensitive", action="store_true")
    c.set_defaults(func=cmd_check)

    b = sub.add_parser("batch", help="check every finding in a findings JSON")
    b.add_argument("--source-file", required=True)
    b.add_argument("--findings", required=True)
    b.add_argument("--case-sensitive", action="store_true")
    b.set_defaults(func=cmd_batch)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
