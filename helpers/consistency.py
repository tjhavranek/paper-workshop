#!/usr/bin/env python3
"""
consistency.py - deterministic numeric cross-reference for paper-workshop (Act II reconciler).

This closes the DETERMINISTIC part of the reconciler's job (prompts/phase2/14): given the
revised manuscript text and the run provenance tokens, it checks that
  (1) run-match: every token's `value` appears as a STANDALONE numeric literal in the revised
      manuscript (0.08 does not match inside 0.083; 12 does not match inside 120);
  (2) orphans: when a BASELINE manuscript is supplied, every numeric VALUE of the revised
      text that appears nowhere in the baseline must trace to some token value (a new
      value with no run behind it is an orphan). This is per-VALUE, not per-occurrence:
      an edit that changes one occurrence to a value the baseline already contains
      elsewhere is invisible to this set-difference check. Bibliographic and structural
      numerals (citation years, page numbers) orphan by construction when newly added;
      the reconciler prompt routes them to author sign-off rather than re-running.
What it deliberately does NOT claim: semantic "same quantity in the abstract vs the table
vs the appendix" matching, and per-occurrence change tracking - both need meaning/position
and stay the LLM reconciler's job (the `mismatches` list is left for that stage; this
script reports `mismatches: []` with a note).

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

# A standalone numeric literal: optional sign, either digits with TRUE 3-digit thousands
# grouping ('46,118' but never '1,18') and decimal, plain digits and decimal, or a
# leading-dot decimal; optional exponent, optional percent. The comma branch is restricted
# to 3-digit grouping so a European decimal comma or adjacent CSV fields are read as
# separate literals, never merged into a fabricated one. Known residual, OPEN in both
# directions: a true 3-digit grouping that is also two CSV fields ('46,118') still reads
# as one literal (a merged value can wrongly match; the components read absent).
# KEEP IN SYNC with helpers/provenance.py: the wall and the reconciler must agree on what
# counts as a number (provenance.py's selftest cross-checks the two patterns).
_NUM_RE = re.compile(
    r"(?<![A-Za-z0-9_.+-])[-+]?(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?|\.\d+)(?:[eE][-+]?\d+)?%?"
    r"(?![A-Za-z0-9_]|\.[A-Za-z0-9_])"
)

# Dash variants substituted for a minus sign by PDF/Word/LaTeX, mapped to ASCII '-'
# BEFORE extraction so negatives keep their sign (see provenance.py for the rationale).
_DASH_TRANS = {0x2010: "-", 0x2011: "-", 0x2012: "-", 0x2013: "-",
               0x2014: "-", 0x2015: "-", 0x2212: "-"}


def norm_num(s):
    """Canonical form so '1,200' == '1200', '.05' == '0.05', '1.2E-05' == '1.2e-05'."""
    n = (s or "").replace(",", "").replace(" ", "").strip()
    n = n.replace("E", "e")
    if n.startswith("-."):
        return "-0" + n[1:]
    if n.startswith("+."):
        return "+0" + n[1:]
    if n.startswith("."):
        return "0" + n
    return n


def numbers_in(text):
    """The set of normalized numeric literals in a text.
    The dash family (en/em dash, Unicode minus, ...) is mapped to ASCII '-' first so
    PDF/LaTeX negatives keep their sign and match."""
    raw = _NUM_RE.findall((text or "").translate(_DASH_TRANS))
    norm = [norm_num(x) for x in raw if norm_num(x) not in ("", "+", "-")]
    return set(norm)


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
    return [norm_num(x) for x in _NUM_RE.findall((value or "").translate(_DASH_TRANS)) if norm_num(x) not in ("", "+", "-")]


def check(manuscript_text, tokens, baseline_text=None):
    rev_set = numbers_in(manuscript_text)

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
        base_set = numbers_in(baseline_text)
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
    # FAIL CLOSED on a vacuous run: zero parsed tokens and no baseline means zero checks
    # were performed (e.g. a typo'd top-level key in the tokens file), so a bare
    # "clean: true" would be meaningless. Refuse unless explicitly allowed.
    if not tokens and baseline is None and not args.allow_empty_tokens:
        print(json.dumps({"error": "no tokens parsed (accepted shapes: a list, or a dict keyed "
                                   "provenance_tokens / tokens / run_artifacts) and no --baseline: "
                                   "nothing was checked. Pass --allow-empty-tokens to permit this.",
                          "clean": False}, indent=2))
        return 2
    res = check(text, tokens, baseline)
    res["n_tokens_checked"] = len(tokens)
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
    expect("identifier digit does NOT match (model_1)",
           check("model_1 is enabled", [{"value": "1"}])["run_mismatches"] == ["1"])
    expect("identifier suffix does NOT match (file2.txt)",
           check("file2.txt was generated", [{"value": "2"}])["run_mismatches"] == ["2"])
    expect("standalone integer after label still matches",
           "1" in check("model = 1", [{"value": "1"}])["reconciled"])

    # Unicode minus (U+2212) in the manuscript matches an ASCII-minus token value
    expect("unicode-minus manuscript matches ascii-minus token",
           "-0.10" in check("the coefficient is −0.10", [{"value": "-0.10"}])["reconciled"])

    lead = check("p = .05; beta = -.05; se = +.05", [{"value": ".05"}, {"value": "-.05"}, {"value": "+.05"}])
    expect("leading-dot decimals reconcile", set(lead["reconciled"]) == {"0.05", "-0.05", "+0.05"})
    expect("leading-dot sign is preserved",
           check("p = .05", [{"value": "-.05"}])["run_mismatches"] == ["-0.05"])
    expect("leading-dot decimal does NOT match integer 05",
           check("p = .05", [{"value": "05"}])["run_mismatches"] == ["05"])

    expect("thousands-comma normalization (1,200 == 1200)",
           "1200" in check(rev, [{"value": "1200"}])["reconciled"])

    base = "The headline estimate is 0.300 (se 0.012) with N = 1,200 observations."
    # revised changed 0.300 -> 0.345 and added a stray 9.99 with no token
    rev3 = "The headline estimate is 0.345 (se 0.012) with N = 1,200; also 9.99."
    r3 = check(rev3, [{"value": "0.345"}], baseline_text=base)
    expect("changed number with token is not an orphan", "0.345" not in r3["orphans"])
    expect("new number without token is an orphan", "9.99" in r3["orphans"])
    expect("orphan -> not clean", r3["clean"] is False)

    # comma grouping: no fabricated merges (European decimal, CSV adjacency)
    expect("European decimal '1,18' does NOT reconcile a fabricated 118",
           check("estimate = 1,18", [{"value": "118"}])["run_mismatches"] == ["118"])
    expect("CSV field value reconciles next to a comma",
           "0.03" in check("46,118,0.03", [{"value": "0.03"}])["reconciled"])
    # dash family: sign integrity
    expect("en-dash negative reconciles '-0.10' token",
           "-0.10" in check("the effect is –0.10", [{"value": "-0.10"}])["reconciled"])
    expect("positive token does NOT reconcile en-dash negative",
           check("the effect is –0.10", [{"value": "0.10"}])["run_mismatches"] == ["0.10"])
    # exponent case-insensitivity
    expect("exponent case-insensitive (1.2E-05 == 1.2e-05)",
           "1.2e-05" in check("coef = 1.2E-05", [{"value": "1.2e-05"}])["reconciled"])
    expect("new citation year orphans by construction",
           "2021" in check("Smith (2021) and 0.345", [{"value": "0.345"}],
                           baseline_text="only 0.345")["orphans"])
    # vacuous-run guard: zero parsed tokens + no baseline exits 2 unless explicitly allowed
    import tempfile, os as _os
    with tempfile.TemporaryDirectory() as _d:
        mp = _os.path.join(_d, "m.txt"); tp = _os.path.join(_d, "t.json")
        with open(mp, "w", encoding="utf-8") as fh:
            fh.write("text with 9.99")
        with open(tp, "w", encoding="utf-8") as fh:
            json.dump({"provenance": [{"value": "0.345"}]}, fh)  # typo'd key -> zero tokens
        expect("typo'd tokens key + no baseline fails closed (exit 2)",
               main(["check", "--manuscript", mp, "--tokens", tp]) == 2)
        expect("--allow-empty-tokens permits the vacuous case (exit 0)",
               main(["check", "--manuscript", mp, "--tokens", tp, "--allow-empty-tokens"]) == 0)
    print("selftest: " + ("OK" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Deterministic Act-II numeric cross-reference.")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="cross-reference token values and detect orphans")
    c.add_argument("--manuscript", required=True)
    c.add_argument("--tokens", required=True)
    c.add_argument("--baseline", default=None, help="baseline manuscript text for orphan detection")
    c.add_argument("--allow-empty-tokens", action="store_true",
                   help="permit a run with zero parsed tokens and no baseline (otherwise fails closed)")
    c.set_defaults(func=cmd_check)

    s = sub.add_parser("selftest", help="run built-in tests")
    s.set_defaults(func=cmd_selftest)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
