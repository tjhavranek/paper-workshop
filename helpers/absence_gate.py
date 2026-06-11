#!/usr/bin/env python3
"""
absence_gate.py - deterministic absence certificate for paper-workshop.

Absence-class findings ("the paper never says X") have no quote to gate, so
until now they rode an unverified rail (grounding rule 9 made them quote-EXEMPT).
This script is the deterministic half of the repair: the filing seat supplies an
`absence_probe` (the words and close paraphrases whose presence in the manuscript
would REFUTE the claimed absence), and this script runs a logged, reproducible
search for every term using the same normalization as the quote gate.

What it certifies, honestly:
  - "absent"  = none of the probe terms occurs in the source. This certifies the
    SEARCH, not the semantics: a paraphrase outside the probe can still exist.
    The verification panel's steelman angle adjudicates the semantic half, using
    the hit snippets this script logs as evidence.
  - "present" = at least one probe term occurs (snippets attached). The claimed
    absence is suspect; the finding degrades to needs-author-confirmation and
    the steelman verifier decides whether the paper already says it.
  - "thin-probe" / "no-probe" = fewer than MIN_TERMS probe terms supplied. Fails
    CLOSED: an unsearchable absence claim is never certified.

Applies to finding_type 'absence-silence' (probe = the allegedly missing thing)
and 'contribution-undersell' (probe = the bolder claim the paper allegedly never
makes; its `quote` foothold is checked by quote_gate.py as usual, so undersell
findings ride BOTH deterministic gates).

No third-party dependencies (stdlib only); reuses quote_gate.py normalization so
the two gates can never drift apart.

USAGE
  Single term:
    python absence_gate.py check --source-file SRC.txt --term "publication bias"

  Batch (certify every absence-class finding in a findings JSON):
    python absence_gate.py batch --source-file SRC.txt --findings findings.json
  -> prints a JSON array: [{"id","certified","terms_searched","hits"}...]
     certified in: absent | present | thin-probe | no-probe | not-absence-class
     hits: [{"term","count","snippets":[...]}] for terms that DID occur
     exit code 0 if every absence-class finding is certified "absent", 2 otherwise.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quote_gate import dehyphenate, normalize  # the canonical normalization

ABSENCE_CLASSES = ("absence-silence", "contribution-undersell")
MIN_TERMS = 3  # a probe this thin invites a narrow search; fail closed below it
SNIPPET_RADIUS = 60  # chars of context captured around each hit, per side
MAX_SNIPPETS = 3  # per term; enough for the steelman verifier, bounded for logs


def _find_all(needle, hay):
    """All start offsets of needle in hay (non-overlapping)."""
    out, start = [], 0
    while True:
        i = hay.find(needle, start)
        if i < 0:
            return out
        out.append(i)
        start = i + max(1, len(needle))


def _hyphens_to_space(text):
    """Map every hyphen to a space and re-collapse: 'small- study' and
    'small-study' both become 'small study'."""
    return re.sub(r"\s+", " ", text.replace("-", " ")).strip()


def _fuse_hyphens(text):
    """Fuse intra-word hyphens: 'small-study' -> 'smallstudy' (matches what
    quote_gate.dehyphenate produces from a hyphen at a line break)."""
    return re.sub(r"(\w)-(\w)", r"\1\2", text)


def search_term(term, source_norm, source_dehyph, source_hyphenless):
    """Deterministic occurrence search for one probe term against pre-normalized
    source text. Returns (count, snippets).

    The ladder is deliberately LOOSER than the quote gate's: it also tries
    hyphen-to-space and hyphen-fused variants on the needle. The two gates have
    opposite failure polarities. For the quote gate a missed match fails CLOSED
    (quote unverified). For an absence gate a missed match would fail OPEN (a
    false 'absent' certificate), so here extra match rungs only ever push a
    finding toward 'present', which degrades it - the conservative direction."""
    nt = normalize(term)
    if nt == "":
        return 0, []
    ladder = [
        (nt, source_norm),
        (dehyphenate(nt), source_dehyph),
        (_hyphens_to_space(nt), source_hyphenless),
        (_fuse_hyphens(nt), source_dehyph),
    ]
    for needle, hay in ladder:
        if needle == "":
            continue
        offsets = _find_all(needle, hay)
        if offsets:
            snippets = []
            for i in offsets[:MAX_SNIPPETS]:
                lo = max(0, i - SNIPPET_RADIUS)
                hi = min(len(hay), i + len(needle) + SNIPPET_RADIUS)
                snippets.append(("..." if lo > 0 else "") + hay[lo:hi] + ("..." if hi < len(hay) else ""))
            return len(offsets), snippets
    return 0, []


def certify(finding, source_norm, source_dehyph, source_hyphenless):
    """Certify one finding. Returns the result row (annotate, never veto:
    severity is untouched; the workflow maps a non-'absent' certificate to
    verification_status='needs-author-confirmation', per rubric.md)."""
    ftype = finding.get("finding_type")
    if ftype not in ABSENCE_CLASSES:
        return {"id": finding.get("id"), "certified": "not-absence-class",
                "terms_searched": 0, "hits": []}
    probe = finding.get("absence_probe") or {}
    # dedupe on the normalized form: near-duplicate list items are a common LLM
    # output mode, and duplicates must not pass the MIN_TERMS floor
    terms, seen = [], set()
    for t in (probe.get("terms") or []):
        nt = normalize(t)
        if nt != "" and nt not in seen:
            seen.add(nt)
            terms.append(t)
    if not terms:
        return {"id": finding.get("id"), "certified": "no-probe",
                "terms_searched": 0, "hits": []}
    hits = []
    for t in terms:
        count, snippets = search_term(t, source_norm, source_dehyph, source_hyphenless)
        if count:
            hits.append({"term": t, "count": count, "snippets": snippets})
    if hits:
        certified = "present"
    elif len(terms) < MIN_TERMS:
        certified = "thin-probe"
    else:
        certified = "absent"
    return {"id": finding.get("id"), "certified": certified,
            "terms_searched": len(terms), "hits": hits}


def _prepare(source):
    """The three pre-normalized source variants the search ladder runs against."""
    sn = normalize(source)
    return sn, dehyphenate(sn), _hyphens_to_space(sn)


def cmd_check(args):
    with open(args.source_file, encoding="utf-8-sig") as fh:
        source = fh.read()
    sn, sd, sh = _prepare(source)
    count, snippets = search_term(args.term, sn, sd, sh)
    print(json.dumps({"term": args.term, "count": count, "snippets": snippets}))
    return 0 if count == 0 else 2


def cmd_batch(args):
    with open(args.source_file, encoding="utf-8-sig") as fh:
        source = fh.read()
    with open(args.findings, encoding="utf-8-sig") as fh:
        data = json.load(fh)
    findings = data["findings"] if isinstance(data, dict) and "findings" in data else data
    sn, sd, sh = _prepare(source)
    out = []
    all_absent = True
    for f in findings:
        row = certify(f, sn, sd, sh)
        if row["certified"] == "not-absence-class":
            continue  # the quote gate owns those; keep this report absence-only
        out.append(row)
        if row["certified"] != "absent":
            all_absent = False
    print(json.dumps(out, indent=2))
    return 0 if all_absent else 2


def cmd_selftest(args):
    ok = True

    def expect(name, cond):
        nonlocal ok
        print(("  PASS " if cond else "  FAIL ") + name)
        ok = ok and cond

    src = ("We estimate the elasticity at 0.07. Publication bias is addressed with\n"
           "selection models, including the small-\nstudy effect channel. The inter-\n"
           "temporal margin is left to future work.")
    sn, sd, sh = _prepare(src)
    # present terms are found, with snippets; casefold + normalization apply
    c, snips = search_term("PUBLICATION BIAS", sn, sd, sh)
    expect("present term found (casefold)", c == 1 and len(snips) == 1)
    expect("snippet carries context", "selection models" in snips[0])
    # dehyphenation fallback finds a line-break-split word
    expect("dehyphenated term found", search_term("intertemporal", sn, sd, sh)[0] == 1)
    # the LOOSER-than-quote-gate rungs: a hyphenated compound split at a PDF line
    # break must be FOUND (in the quote gate this miss fails closed; here a miss
    # would fail OPEN as a false 'absent' certificate)
    expect("hyphenated probe found despite line-break split",
           search_term("small-study effect", sn, sd, sh)[0] >= 1)
    expect("space-variant probe found despite line-break split",
           search_term("small study effect", sn, sd, sh)[0] >= 1)
    expect("fused probe found despite line-break split",
           search_term("smallstudy effect", sn, sd, sh)[0] >= 1)
    # absent terms are not found
    expect("absent term not found", search_term("power analysis", sn, sd, sh)[0] == 0)
    expect("empty term never matches", search_term("", sn, sd, sh) == (0, []))
    # certify(): the full fail-closed ladder
    base = {"id": "A1", "finding_type": "absence-silence"}
    expect("no probe fails closed",
           certify(dict(base), sn, sd, sh)["certified"] == "no-probe")
    expect("empty-string terms fail closed",
           certify(dict(base, absence_probe={"terms": ["", "  "]}), sn, sd, sh)["certified"] == "no-probe")
    expect("thin probe (under minimum) fails closed",
           certify(dict(base, absence_probe={"terms": ["power analysis", "statistical power"]}),
                   sn, sd, sh)["certified"] == "thin-probe")
    expect("duplicate terms do not pass the floor (dedupe on normalized form)",
           certify(dict(base, absence_probe={"terms": ["power analysis", "power analysis",
                                                       "POWER  ANALYSIS"]}),
                   sn, sd, sh)["certified"] == "thin-probe")
    expect("genuinely absent certifies absent",
           certify(dict(base, absence_probe={"terms": ["power analysis", "statistical power",
                                                       "sample size calculation"]}),
                   sn, sd, sh)["certified"] == "absent")
    row = certify(dict(base, absence_probe={"terms": ["power analysis", "publication bias",
                                                      "sample size calculation"]}), sn, sd, sh)
    expect("any present term certifies present", row["certified"] == "present")
    expect("present hit names the term", row["hits"][0]["term"] == "publication bias")
    expect("undersell findings are in scope",
           certify({"id": "U1", "finding_type": "contribution-undersell",
                    "absence_probe": {"terms": ["one", "two", "three"]}},
                   sn, sd, sh)["certified"] == "absent")
    expect("non-absence types are out of scope",
           certify({"id": "Q1", "finding_type": "claim-support"}, sn, sd, sh)["certified"]
           == "not-absence-class")
    # batch mode: the production path (filtering, exit aggregation)
    import contextlib
    import io
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        sp = os.path.join(d, "src.txt")
        fp = os.path.join(d, "f.json")
        with open(sp, "w", encoding="utf-8") as fh:
            fh.write(src)
        cases = {"findings": [
            {"id": "B1", "finding_type": "absence-silence",
             "absence_probe": {"terms": ["power analysis", "statistical power", "sample size calculation"]}},
            {"id": "B2", "finding_type": "absence-silence",
             "absence_probe": {"terms": ["publication bias", "small-study effect", "funnel asymmetry"]}},
            {"id": "B3", "finding_type": "claim-support", "quote": "elasticity at 0.07"},
            {"id": "B4", "finding_type": "contribution-undersell"},
        ]}
        with open(fp, "w", encoding="utf-8") as fh:
            json.dump(cases, fh)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(["batch", "--source-file", sp, "--findings", fp])
        rows = {r["id"]: r for r in json.loads(buf.getvalue())}
        expect("batch: absent certifies", rows["B1"]["certified"] == "absent")
        expect("batch: present is caught", rows["B2"]["certified"] == "present")
        expect("batch: non-absence types are excluded from the report", "B3" not in rows)
        expect("batch: probe-less undersell fails closed", rows["B4"]["certified"] == "no-probe")
        expect("batch: any non-absent row -> exit 2", rc == 2)
        ok_only = {"findings": [{"id": "C1", "finding_type": "absence-silence",
                                 "absence_probe": {"terms": ["alpha beta", "gamma delta", "epsilon zeta"]}}]}
        with open(fp, "w", encoding="utf-8") as fh:
            json.dump(ok_only, fh)
        with contextlib.redirect_stdout(io.StringIO()):
            rc2 = main(["batch", "--source-file", sp, "--findings", fp])
        expect("batch: all absent -> exit 0", rc2 == 0)
    print("selftest: " + ("OK" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Deterministic absence certificate for paper-workshop.")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="search a single probe term")
    c.add_argument("--source-file", required=True)
    c.add_argument("--term", required=True)
    c.set_defaults(func=cmd_check)

    b = sub.add_parser("batch", help="certify every absence-class finding in a findings JSON")
    b.add_argument("--source-file", required=True)
    b.add_argument("--findings", required=True)
    b.set_defaults(func=cmd_batch)

    s = sub.add_parser("selftest", help="run built-in tests (no external files needed)")
    s.set_defaults(func=cmd_selftest)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
