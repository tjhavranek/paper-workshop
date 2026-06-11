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
     match_level in: normalized | dehyphenated | exempt-absence | empty-quote | none
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
# Zero-width / invisible characters that survive NFKC and are neither whitespace nor in the
# maps above. PDF/Word extraction sprinkles these (soft hyphen, ZWSP, BOM, word-joiner,
# ZWNJ/ZWJ); left in, they make a real quote fail to match. Deleted on both sides (-> None).
_ZEROWIDTH = {0x00AD: None, 0x200B: None, 0xFEFF: None, 0x2060: None, 0x200C: None, 0x200D: None}
_TRANS = {ord(k): v for k, v in {**_QUOTES, **_DASHES, **_SPACES}.items()}
_TRANS.update(_ZEROWIDTH)


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
    """Join a word split by a hyphen at a (former) line break: 'inter- national' -> 'international',
    'covid- 19' -> 'covid19'. Does NOT join a numeric range such as '5- 10' (joining it would
    fabricate '510' and let a bogus quote match). Only a hyphen sitting between two word characters
    is joined, and never when both sides are digits."""
    return re.sub(
        r"(\w)-\s+(\w)",
        lambda m: m.group(0) if (m.group(1).isdigit() and m.group(2).isdigit())
        else m.group(1) + m.group(2),
        text,
    )


def check(quote, source, casefold=True):
    """Return (matched: bool, match_level: str). Tries exact-normalized first,
    then a dehyphenated fallback for PDF line-break hyphenation.

    An empty quote is NOT a match here (fail CLOSED). The absence/silence exemption
    needs the finding_type, so it is the CALLER's job (see cmd_batch); an empty quote
    on a non-absence finding must fail, never be waved through."""
    nq = normalize(quote, casefold)
    if nq == "":
        return False, "empty-quote"
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
        with open(args.quote_file, encoding="utf-8-sig") as fh:
            return fh.read()
    if args.quote_stdin:
        return sys.stdin.read()
    raise SystemExit("provide --quote, --quote-file, or --quote-stdin")


def cmd_check(args):
    with open(args.source_file, encoding="utf-8-sig") as fh:
        source = fh.read()
    quote = _read_quote(args)
    matched, level = check(quote, source, casefold=not args.case_sensitive)
    print(json.dumps({"matched": matched, "match_level": level}))
    return 0 if matched else 2


def cmd_batch(args):
    with open(args.source_file, encoding="utf-8-sig") as fh:
        source = fh.read()
    with open(args.findings, encoding="utf-8-sig") as fh:
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


def cmd_selftest(args):
    ok = True

    def expect(name, cond):
        nonlocal ok
        print(("  PASS " if cond else "  FAIL ") + name)
        ok = ok and cond

    src = ("The corrected mean effect is close to zero. We use inter- national\n"
           "evidence on covid- 19 and type- 2 tasks, with rates of 5- 10 percent.")
    # exact normalized substring + casefold
    expect("exact normalized match", check("corrected mean effect is close to zero", src)[0] is True)
    expect("casefold match", check("CORRECTED MEAN", src)[0] is True)
    # unicode dash/quote/space canonicalization
    expect("unicode-minus -> ascii", normalize("−0.10") == normalize("-0.10"))
    expect("en-dash -> ascii", normalize("0.10–0.20") == normalize("0.10-0.20"))
    expect("smart quotes -> ascii", normalize("“x”") == normalize('"x"'))
    # zero-width / soft hyphen stripped
    expect("soft hyphen stripped", check("international", "inter­national")[0] is True)
    expect("ZWSP stripped", check("abc", "a​b​c")[0] is True)
    # dehyphenation joins genuine line-break splits (letters, letter-digit)
    expect("dehyphenate joins letters", check("international", src) == (True, "dehyphenated"))
    expect("dehyphenate joins covid19 (letter-digit)", check("covid19", src)[0] is True)
    expect("dehyphenate joins type2 (letter-digit)", check("type2", src)[0] is True)
    # dehyphenation must NOT join a numeric range (no fabricated 510)
    expect("numeric range NOT joined", check("510", src)[0] is False)
    # fail-closed cases
    expect("empty quote -> empty-quote", check("", src) == (False, "empty-quote"))
    expect("absent quote -> none", check("phrase that is not present at all", src) == (False, "none"))
    # determinism
    expect("normalize idempotent", normalize(normalize(src)) == normalize(src))
    # batch mode: the production path (rule-9 absence exemption, fail-closed empty quote,
    # dict unwrap, severity_hint annotate-never-veto, exit aggregation)
    import contextlib
    import io
    import os
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        sp = os.path.join(d, "src.txt")
        fp = os.path.join(d, "f.json")
        with open(sp, "w", encoding="utf-8") as fh:
            fh.write(src)
        cases = {"findings": [
            {"id": "B1", "finding_type": "claim-support", "quote": "corrected mean effect"},
            {"id": "B2", "finding_type": "absence-silence", "quote": ""},
            {"id": "B3", "finding_type": "claim-support", "quote": ""},
            {"id": "B4", "finding_type": "absence-silence", "quote": "corrected mean effect"},
            {"id": "B5", "finding_type": "claim-support", "quote": "phrase that is not present"},
        ]}
        with open(fp, "w", encoding="utf-8") as fh:
            json.dump(cases, fh)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(["batch", "--source-file", sp, "--findings", fp])
        rows = {r["id"]: r for r in json.loads(buf.getvalue())}
        expect("batch: matched quote passes", rows["B1"]["matched"] is True)
        expect("batch: absence + empty quote is exempt", rows["B2"]["match_level"] == "exempt-absence")
        expect("batch: empty quote on non-absence fails closed",
               rows["B3"]["matched"] is False and rows["B3"]["match_level"] == "empty-quote")
        expect("batch: absence with a NON-empty quote is still gated (no exemption abuse)",
               rows["B4"]["match_level"] != "exempt-absence" and rows["B4"]["matched"] is True)
        expect("batch: unmatched quote hints downgrade, never delete",
               rows["B5"]["severity_hint"] == "downgrade-status-to-needs-author-confirmation")
        expect("batch: any non-exempt failure -> exit 2", rc == 2)
        ok_only = {"findings": [{"id": "C1", "finding_type": "claim-support", "quote": "corrected mean effect"}]}
        with open(fp, "w", encoding="utf-8") as fh:
            json.dump(ok_only, fh)
        with contextlib.redirect_stdout(io.StringIO()):
            rc2 = main(["batch", "--source-file", sp, "--findings", fp])
        expect("batch: all matched -> exit 0", rc2 == 0)
    print("selftest: " + ("OK" if ok else "FAILED"))
    return 0 if ok else 1


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

    s = sub.add_parser("selftest", help="run built-in tests (no external files needed)")
    s.set_defaults(func=cmd_selftest)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
