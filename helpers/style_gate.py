#!/usr/bin/env python3
"""
style_gate.py - deterministic AI-style detector for paper-workshop.

The author-voice standard (prompts/phase2/12_scribe_implementer.md) and the
`human-voice` verification angle catch AI-sounding prose, but until now they were
the ONE Act-II trust rail with no deterministic half: an LLM was asked to eyeball
em/en-dash, semicolon, antithesis and banned-lexicon counts. An LLM verifier shares
the tells it is meant to catch, so this script does the COUNTING the way quote_gate.py
does quote matching: deterministically, reproducibly, the same at batch size 1 or 30.

It is ADVISORY and AUTHOR-RELATIVE, the opposite polarity to quote_gate:
  - On a MANUSCRIPT edit, the target is the AUTHOR's own voice, not a fixed house style.
    The gate flags only a dash/semicolon RATE SPIKE above the author's baseline (never the
    mark itself, never an absolute count), and the banned-lexicon scan SUBTRACTS any term
    the author already uses (the deterministic form of "unless the author already uses it").
    A spike or a missing baseline is advisory -> route the edit to author sign-off; it NEVER
    auto-rejects, because a legitimate author may use dashes (grounding rule 14, the human
    decides). The LLM human-voice verifier still makes the semantic call on top.
  - Banned lexicon and the unambiguous staged antithesis ("it is not X, it is Y") are
    author-INDEPENDENT tells and exit non-zero, so they can drive a rewrite of the
    100%-AI deliverable prose (changes_map / README / MAP / disclosure) that has no author
    voice to protect.

Deliberately NOT flagged deterministically (left to the LLM's semantic judgment, to avoid
false positives on legitimate academic prose): bare "rather than X, Y" (a normal comparative
- "we use OLS rather than IV"), "not only X but also Y", and "highlight" as a verb (needs POS).

No third-party dependencies (stdlib only); reuses quote_gate.normalize so the gates never
drift. Dash COUNTING runs on RAW text (normalize collapses every dash to '-' for matching, so
it must NOT be used to count them); normalize() is used only for the word/phrase scans.

USAGE
  Single span (inserted text inline / file / stdin) vs an author baseline:
    python style_gate.py check --inserted "the new sentence" --baseline-file paper.txt
    python style_gate.py check --inserted-file new.txt --baseline-file paper.txt
    echo "text" | python style_gate.py check --inserted-stdin --baseline-file paper.txt

  Batch (many spans against one baseline):
    python style_gate.py batch --baseline-file paper.txt --spans spans.json
  spans.json: [{"id": "...", "text": "..."}, ...]
  -> prints a JSON array: [{"id","verdict","flags",...,"severity_hint","advisory"}...]
     verdict in: clean | signposting | spike | no-baseline | antithesis | banned
     exit 0 unless any span hit a banned token or the staged antithesis (then exit 2).
"""
import argparse
import json
import re
import sys

from quote_gate import normalize  # single source of truth for word-scan normalization

SPIKE_FACTOR = 1.5   # inserted rate must exceed author rate by this factor to count as a spike
SPIKE_FLOOR = 2      # ...AND have at least this many absolute, so one author-style dash never churns

# High-precision AI lexicon: the unambiguous tells from 12_scribe_implementer.md, with common
# inflections. Domain-common words ("crucial", "vital", "robust", "significant", "novel",
# "nuanced") are deliberately LEFT OFF the deterministic list and remain the LLM verifier's
# call, because an economist legitimately writes "crucial for identification" / "robust SEs".
# Every hit is still cancelled if the author's own baseline uses the word (the escape).
_BANNED_WORDS = {
    "delve", "delves", "delved", "delving",
    "leverage", "leverages", "leveraged", "leveraging",
    "underscore", "underscores", "underscored", "underscoring",
    "showcase", "showcases", "showcased", "showcasing",
    "foster", "fosters", "fostered", "fostering",
    "harness", "harnesses", "harnessed", "harnessing",
    "garner", "garners", "garnered", "garnering",
    "pivotal", "realm", "realms", "tapestry", "multifaceted", "intricate",
}
_BANNED_PHRASES = [
    "a testament to", "stands as a testament", "navigate the complexities",
    "navigating the complexities", "plays a key role", "plays a pivotal role",
    "plays a crucial role", "serves as a", "in today's", "ever-evolving",
]
# Over-signposting / filler. Advisory only (these sometimes appear in real prose), exit 0;
# author-escape applies. Trailing comma/space anchors the sentence-initial use.
_SIGNPOST = [
    "it is worth noting", "it's worth noting", "it is important to note",
    "importantly,", "notably,", "crucially,", "moreover,", "furthermore,",
    "in summary,", "to summarize,", "taken together,", "needless to say,",
]
# Staged negation-correction antithesis, NARROW on purpose: only the "it is not X, it is Y"
# family (and the "not about X, ... about Y" frame), which essentially never occurs in careful
# academic prose. Bare "rather than" / "not only ... but also" are NOT here by design.
_ANTITHESIS = [
    re.compile(r"\b(?:it'?s|it is|this is|that is|they are) not\b[^.?!;]{1,80}?,\s*"
               r"(?:it'?s|it is|but it'?s|rather it'?s|they are)\b", re.IGNORECASE),
    re.compile(r"\bnot about\b[^.?!;]{1,60}?,?\s*(?:but|it'?s|rather)\b[^.?!;]{0,20}?\babout\b",
               re.IGNORECASE),
]


def _words(text):
    return re.findall(r"[^\W\d_]+", text)  # letter runs; excludes pure numbers/underscores


def _dash_counts(raw):
    """Count em/en dashes on RAW text in BOTH encodings. Unicode em U+2014 and en U+2013, plus
    LaTeX-source '---' (em) and '--' (en). Strip '---' before counting '--' so they never
    double-count. Returns (em_total, en_total, semicolons)."""
    em_uni = raw.count("—")
    en_uni = raw.count("–")
    em_tex = raw.count("---")
    en_tex = raw.replace("---", "").count("--")
    semis = raw.count(";")
    return em_uni + em_tex, en_uni + en_tex, semis


def _rate(n, words):
    return (n / words * 100.0) if words else 0.0


def _spike(ins_n, ins_words, base_n, base_words):
    """A mark spikes when the inserted RATE exceeds the author baseline rate by SPIKE_FACTOR
    AND the inserted absolute count is at least SPIKE_FLOOR. Author-relative, never absolute."""
    if ins_n < SPIKE_FLOOR:
        return False
    return _rate(ins_n, ins_words) > _rate(base_n, base_words) * SPIKE_FACTOR


def score_span(inserted, baseline):
    """Return a dict describing the inserted span's style relative to the author baseline.
    Deterministic and advisory. Never edits text; never returns 'reject'/'delete'."""
    inserted = inserted or ""
    baseline = baseline or ""
    has_base = normalize(baseline) != ""
    ni = normalize(inserted)                       # for word/phrase scans only
    nb = normalize(baseline)
    iwords = _words(inserted)
    bwords = _words(baseline)
    em_i, en_i, semi_i = _dash_counts(inserted)
    em_b, en_b, semi_b = _dash_counts(baseline)

    flags = []
    # dash / semicolon spikes (only meaningful with a baseline)
    if has_base:
        if _spike(em_i, len(iwords), em_b, len(bwords)):
            flags.append("em-dash-spike")
        if _spike(en_i, len(iwords), en_b, len(bwords)):
            flags.append("en-dash-spike")
        if _spike(semi_i, len(iwords), semi_b, len(bwords)):
            flags.append("semicolon-spike")

    # banned lexicon, minus any term the author's baseline already uses (the escape)
    iword_set = {w.casefold() for w in iwords}
    bword_set = {w.casefold() for w in _words(baseline)}
    banned_hits = sorted((iword_set & _BANNED_WORDS) - bword_set)
    for ph in _BANNED_PHRASES:
        if ph in ni and ph not in nb:
            banned_hits.append(ph)

    # staged antithesis (author-independent; the narrow family only)
    antithesis_hits = [m.group(0).strip() for pat in _ANTITHESIS for m in pat.finditer(inserted)]

    # over-signposting, minus author-used (advisory)
    signpost_hits = [ph for ph in _SIGNPOST if ph in ni and ph not in nb]

    if banned_hits:
        verdict = "banned"
    elif antithesis_hits:
        verdict = "antithesis"
    elif flags:
        verdict = "spike"
    elif signpost_hits:
        verdict = "signposting"
    elif not has_base:
        verdict = "no-baseline"
    else:
        verdict = "clean"

    if verdict in ("banned", "antithesis"):
        hint = "rewrite-or-route-to-author-confirmation"
    elif verdict in ("spike", "signposting", "no-baseline"):
        hint = "route-to-author-confirmation"
    else:
        hint = "keep"

    return {
        "verdict": verdict,
        "flags": flags,
        "banned_hits": banned_hits,
        "antithesis_hits": antithesis_hits,
        "signpost_hits": signpost_hits,
        "em_dash_inserted": em_i, "em_dash_baseline": em_b,
        "en_dash_inserted": en_i, "en_dash_baseline": en_b,
        "semicolon_inserted": semi_i, "semicolon_baseline": semi_b,
        "dash_rate_inserted": round(_rate(em_i + en_i, len(iwords)), 2),
        "dash_rate_author": round(_rate(em_b + en_b, len(bwords)), 2),
        "severity_hint": hint,
        "advisory": True,
    }


def _hard_hit(row):
    """A row that justifies a non-zero exit: an author-INDEPENDENT tell (banned or staged
    antithesis). Spikes/signposting/no-baseline are advisory -> exit 0."""
    return row["verdict"] in ("banned", "antithesis")


def _read_inserted(args):
    if args.inserted is not None:
        return args.inserted
    if args.inserted_file:
        with open(args.inserted_file, encoding="utf-8-sig") as fh:
            return fh.read()
    if args.inserted_stdin:
        return sys.stdin.read()
    raise SystemExit("provide --inserted, --inserted-file, or --inserted-stdin")


def _read_baseline(args):
    if getattr(args, "baseline", None) is not None:
        return args.baseline
    if getattr(args, "baseline_file", None):
        with open(args.baseline_file, encoding="utf-8-sig") as fh:
            return fh.read()
    return ""


def cmd_check(args):
    row = score_span(_read_inserted(args), _read_baseline(args))
    print(json.dumps(row, indent=2))
    return 2 if _hard_hit(row) else 0


def cmd_batch(args):
    baseline = _read_baseline(args)
    with open(args.spans, encoding="utf-8-sig") as fh:
        data = json.load(fh)
    spans = data["spans"] if isinstance(data, dict) and "spans" in data else data
    out = []
    any_hard = False
    for s in spans:
        row = score_span(s.get("text", ""), baseline)
        row["id"] = s.get("id")
        any_hard = any_hard or _hard_hit(row)
        out.append(row)
    print(json.dumps(out, indent=2))
    return 2 if any_hard else 0


def cmd_selftest(args):
    ok = True

    def expect(name, cond):
        nonlocal ok
        print(("  PASS " if cond else "  FAIL ") + name)
        ok = ok and cond

    plain_author = ("We estimate the model by ordinary least squares. The sample covers "
                    "forty countries over twenty years. Standard errors are clustered by study. "
                    "We report the coefficient and its confidence interval in Table 2.")
    # constructed so the arithmetic is unambiguous: 4 em-dashes in 28 words => ~14 per 100 words
    dashy_author = ("word " * 20 + "x—y " * 4).strip()

    # em-dash spike fires against a dash-free author, not against an author at/below whose rate
    em_insert = "The effect is small—almost zero—and stable—across specifications."
    expect("em-dash spike vs plain author", score_span(em_insert, plain_author)["verdict"] == "spike")
    expect("em-dash spike flag present",
           "em-dash-spike" in score_span(em_insert, plain_author)["flags"])
    # an insert AT OR BELOW a dashy author's own rate must NOT spike (2 dashes / 24 words ~= 8 < 14*1.5)
    at_rate_insert = ("word " * 20 + "x—y " * 2).strip()
    expect("no spike at/below a dashy author's own rate",
           "em-dash-spike" not in score_span(at_rate_insert, dashy_author)["flags"])
    # but a genuine spike ABOVE even a dashy author still fires (50 per 100 >> 14*1.5)
    expect("spike fires above even a dashy author",
           "em-dash-spike" in score_span("a—b " * 4, dashy_author)["flags"])
    # LaTeX-source dashes are counted, not normalized away
    latex_insert = "The effect is small --- almost zero --- and stable --- everywhere."
    expect("LaTeX --- counted as em spike", "em-dash-spike" in score_span(latex_insert, plain_author)["flags"])
    expect("--- not double-counted as en",
           score_span("a --- b", "")["en_dash_inserted"] == 0 and score_span("a --- b", "")["em_dash_inserted"] == 1)
    expect("LaTeX -- counted as en", score_span("range 5 -- 10 and 20 -- 30", "")["en_dash_inserted"] == 2)
    # one dash never churns (absolute floor)
    expect("single em-dash does not spike",
           "em-dash-spike" not in score_span("A small effect—stable.", plain_author)["flags"])

    # banned lexicon, with the author-use escape
    expect("banned word flagged", score_span("We delve into the mechanism.", plain_author)["verdict"] == "banned")
    expect("banned word escaped when author uses it",
           score_span("We leverage the panel.", "Our identification strategy will leverage the panel structure.")["verdict"] != "banned")
    expect("banned phrase flagged",
           "a testament to" in score_span("This is a testament to the design.", plain_author)["banned_hits"])
    expect("banned exits non-zero", _hard_hit(score_span("We delve in.", plain_author)) is True)

    # staged antithesis caught; legitimate "rather than" comparative is NOT (the key non-damage)
    expect("staged antithesis caught",
           score_span("It is not a tested property, it is an assumption.", plain_author)["verdict"] == "antithesis")
    expect("'rather than' comparative NOT flagged as antithesis (legitimate prose)",
           score_span("We treat it as an assumption rather than a tested property, and as one "
                      "member of our battery rather than a decisive arbiter.", plain_author)["verdict"] != "antithesis")
    expect("'not only ... but also' NOT flagged (legitimate prose)",
           score_span("The effect is present not only in the pooled sample but also within firms.",
                      plain_author)["verdict"] != "antithesis")

    # signposting is advisory (exit 0), and escapes when the author uses it
    sp = score_span("Importantly, the effect persists. Moreover, it grows.", plain_author)
    expect("signposting detected", sp["verdict"] == "signposting")
    expect("signposting is advisory (exit 0)", _hard_hit(sp) is False)

    # clean inserted prose against a normal author is clean
    expect("clean inserted prose is clean",
           score_span("We add a caveat that the exclusion restriction is assumed, not tested.",
                      plain_author)["verdict"] == "clean")
    # no baseline -> advisory no-baseline (not a hard hit), but banned still fires
    expect("no baseline is advisory", score_span("A plain new sentence about the sample.", "")["verdict"] == "no-baseline")
    expect("banned still fires with no baseline", _hard_hit(score_span("We delve in.", "")) is True)
    # determinism
    r1 = score_span(em_insert, plain_author)
    r2 = score_span(em_insert, plain_author)
    expect("deterministic", r1 == r2)

    # batch mode + exit aggregation
    import contextlib
    import io
    import os
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        bp = os.path.join(d, "base.txt")
        spp = os.path.join(d, "spans.json")
        with open(bp, "w", encoding="utf-8") as fh:
            fh.write(plain_author)
        with open(spp, "w", encoding="utf-8") as fh:
            json.dump([{"id": "S1", "text": "A clean caveat sentence."},
                       {"id": "S2", "text": "We delve into it."}], fh)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = main(["batch", "--baseline-file", bp, "--spans", spp])
        rows = {r["id"]: r for r in json.loads(buf.getvalue())}
        expect("batch: clean span clean", rows["S1"]["verdict"] == "clean")
        expect("batch: banned span banned", rows["S2"]["verdict"] == "banned")
        expect("batch: any banned -> exit 2", rc == 2)
        with open(spp, "w", encoding="utf-8") as fh:
            json.dump([{"id": "S1", "text": "A clean caveat sentence about the sample."}], fh)
        with contextlib.redirect_stdout(io.StringIO()):
            rc2 = main(["batch", "--baseline-file", bp, "--spans", spp])
        expect("batch: all clean -> exit 0", rc2 == 0)

    print("selftest: " + ("OK" if ok else "FAILED"))
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Deterministic AI-style detector for paper-workshop (advisory, author-relative).")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("check", help="score one inserted span vs an author baseline")
    c.add_argument("--inserted")
    c.add_argument("--inserted-file")
    c.add_argument("--inserted-stdin", action="store_true")
    c.add_argument("--baseline")
    c.add_argument("--baseline-file")
    c.set_defaults(func=cmd_check)

    b = sub.add_parser("batch", help="score many spans against one baseline")
    b.add_argument("--spans", required=True)
    b.add_argument("--baseline")
    b.add_argument("--baseline-file")
    b.set_defaults(func=cmd_batch)

    s = sub.add_parser("selftest", help="run built-in tests (no external files needed)")
    s.set_defaults(func=cmd_selftest)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
