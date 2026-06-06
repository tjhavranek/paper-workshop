#!/usr/bin/env python3
"""
consistency.py - deterministic numeric cross-reference for paper-workshop (Act II reconciler).

This closes the DETERMINISTIC part of the reconciler's job (prompts/phase2/14): given the
revised manuscript text and the run provenance tokens, it checks that
  (1) run-match: every token's `value` appears as a STANDALONE numeric literal in the revised
      manuscript (0.08 does not match inside 0.083; 12 does not match inside 120);
  (2) orphans: when a BASELINE manuscript is supplied, every number that is NEW or CHANGED
      relative to the baseline traces to some token value (a changed number with no run
      behind it is an orphan).
What it deliberately does NOT claim: semantic "same quantity in the abstract vs the table
vs the appendix" matching, which needs meaning and stays the LLM reconciler's job (the
`mismatches` list is left for that stage; this script reports `mismatches: []` with a note).

Deterministic, stdlib-only (Python 3.8+), fails CLOSED: any run-mismatch or orphan exits 2.

USAGE
  python consistency.py check --manuscript revised.txt --tokens tokens.json
  python consistency.py check --manuscript revised.txt --tokens tokens.json --baseline baseline.txt
tokens.json may be a list of tokens, or {"provenance_tokens":[...]}, or {"tokens":[...]};
each token must carry a `value`. Output is an object with reconciled/orphans/run_mismatches/
mismatches (mirrors RECON in workflow/phase2_atelier.js). Exit 0 iff orphans and
run_mismatches are both empty.
"""
import argparse
import json
import re
import sys

# A numeric literal: optional sign, digits with optional thousands commas, optional decimal,
# optional scientific exponent, optional trailing percent.
_NUM_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?(?:[eE][-+]?\d+)?%?")


def norm_num(s):
    """Canonical form of a numeric literal so '1,200' == '1200' and ' 0.345 ' == '0.345'."""
    return (s or "").replace(",", "").replace(" ", "").strip()


def numbers_in(text):
    """The multiset (as a set + list) of normalized numeric literals in a text."""
    raw = _NUM_RE.findall(text or "")
    norm = [norm_num(x) for x in raw if norm_num(x) not in ("", "+", "-")]
    return set(norm), norm


def _token_list(data):
    if isinstance(data, dict):
        for key in ("provenance_tokens", "tokens", "run_artifacts"):
            if key in data and isinstance(data[key], list):
                return data[key]
        # a dict that is itself a single token
        if "value" in data:
            return [data]
        return []
    if isinstance(data, list):
        return data
    return []


def value_literals(value):
    """Normalized numeric literals inside a (possibly multi-part) token value string."""
    return [norm_num(x) for x in _NUM_RE.findall(value or "") if norm_num(x) not in ("", "+", "-")]


def check(manuscript_text, tokens, baseline_text=None):
    rev_set, _ = numbers_in(manuscript_text)

    reconciled, run_mismatches, tok_lits = [], [], set()
    for t in tokens:
        v = t.get("value") if isinstance(t, dict) else t
        if v is None:
            continue
        lits = value_literals(str(v))
        tok_lits.update(lits)
        # every numeric literal in the value must appear as a STANDALONE literal in the text —
        # NO substring fallback (so 0.08 does not "match" inside 0.083, nor 12 inside 120).
        present = bool(lits) and all(l in rev_set for l in lits)
        (reconciled if present else run_mismatches).append(norm_num(str(v)))

    orphans = []
    if baseline_text is not None:
        base_set, _ = numbers_in(baseline_text)
        changed_or_new = rev_set - base_set
        orphans = sorted(n for n in changed_or_new if n not in tok_lits)

    clean = (not orphans) and (not run_mismatches)
    return {
        "reconciled": sorted(set(reconciled)),
        "orphans": orphans,
        "run_mismatches": sorted(set(run_mismatches)),
        "mismatches": [],
        "note": "run-match and orphan detection are deterministic here; semantic same-quantity "
                "cross-place consistency (abstract vs table vs appendix) is left to the LLM reconciler.",
        "clean": clean,
    }


def _read(path):
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        return fh.read()


def cmd_check(args):
    text = _read(args.manuscript)
    with open(args.tokens, encoding="utf-8-sig") as fh:
        tokens = _token_list(json.load(fh))
    baseline = _read(args.baseline) if args.baseline else None
    res = check(text, tokens, baseline)
    print(json.dumps(res, indent=2))
    return 0 if res["clean"] else 2


def cmd_selftest(args):
    ok = True

    def expect(name, cond):
        nonlocal ok
        print(("  PASS " if cond else "  FAIL ") + name)
        ok = ok and cond

    rev = "The headline estimate is 0.345 (se 0.012) with N = 1,200 observations."
    toks = [{"value": "0.345"}, {"value": "0.012"}]
    r = check(rev, toks)
    expect("token values present -> reconciled", set(r["reconciled"]) == {"0.345", "0.012"})
    expect("all present -> clean", r["clean"] is True)

    r2 = check(rev, [{"value": "0.999"}])
    expect("absent token -> run_mismatch", r2["run_mismatches"] == ["0.999"])
    expect("run_mismatch -> not clean", r2["clean"] is False)

    # substring fail-open guard: a value that only appears INSIDE a longer number is NOT a match
    expect("0.08 does NOT match inside 0.083",
           check("the headline estimate is 0.083", [{"value": "0.08"}])["run_mismatches"] == ["0.08"])
    expect("12 does NOT match inside 120",
           check("N = 120 observations", [{"value": "12"}])["run_mismatches"] == ["12"])

    expect("thousands-comma normalization (1,200 == 1200)",
           "1200" in check(rev, [{"value": "1200"}])["reconciled"])

    base = "The headline estimate is 0.300 (se 0.012) with N = 1,200 observations."
    # revised changed 0.300 -> 0.345 and added a stray 9.99 with no token
    rev3 = "The headline estimate is 0.345 (se 0.012) with N = 1,200; also 9.99."
    r3 = check(rev3, [{"value": "0.345"}], baseline_text=base)
    expect("changed number with token is not an orphan", "0.345" not in r3["orphans"])
    expect("new number without token is an orphan", "9.99" in r3["orphans"])
    expect("orphan -> not clean", r3["clean"] is False)
    print("selftest: " + ("OK" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Deterministic Act-II numeric cross-reference.")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="cross-reference token values and detect orphans")
    c.add_argument("--manuscript", required=True)
    c.add_argument("--tokens", required=True)
    c.add_argument("--baseline", default=None, help="baseline manuscript text for orphan detection")
    c.set_defaults(func=cmd_check)

    s = sub.add_parser("selftest", help="run built-in tests")
    s.set_defaults(func=cmd_selftest)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
