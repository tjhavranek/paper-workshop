# quote_gate.py — usage

Deterministic quote verification (grounding rule 10). An LLM verifier shares the
hallucination it is checking, so this is a **script**, and it fails **closed**.

## When it runs
- At the barrier exiting Phase D (specialist findings), before anything enters
  cross-critique or synthesis.
- Inside the verification panel, as the `quote-locator` angle.
- In Act II, on every quotation an edit relies on.

The `quote-locator` verifier subagent runs it via Bash and reports its JSON output;
the subagent does not judge quote presence by eye.

## Modes
```
# single quote (inline, from a file, or stdin to dodge shell escaping)
python helpers/quote_gate.py check --source-file input/paper.txt --quote "exact text"
python helpers/quote_gate.py check --source-file input/paper.txt --quote-file q.txt
cat q.txt | python helpers/quote_gate.py check --source-file input/paper.txt --quote-stdin

# batch: verify every finding's quote at once
python helpers/quote_gate.py batch --source-file input/paper.txt --findings round1/findings.json
```

`batch` reads a findings JSON (an array, or `{ "findings": [...] }`) and prints
`[{ "id", "matched", "match_level", "severity_hint" }, ...]`.

## Match levels
- `normalized` — matched after Unicode-NFKC + quote/dash/space canonicalization +
  zero-width/soft-hyphen removal + whitespace-collapse + casefold. The normal pass.
- `dehyphenated` — matched only after also joining `-`-at-line-break (PDF
  hyphenation). Still a pass; note it.
- `exempt-absence` — the finding is `absence-silence` with an empty quote; not gated.
- `empty-quote` — the quote normalized to nothing on a finding that is **not** `absence-silence`.
  Treated exactly like `none`: a fail, status forced to `needs-author-confirmation`.
- `none` — **no match. Fail closed.** The finding's `verification_status` is forced to
  `needs-author-confirmation`. The finding is **not** deleted, and its severity is
  **not** changed (rubric.md: status annotates, never vetoes).

## Exit codes
`0` if all non-exempt quotes matched, `2` otherwise. Use the exit code as a cheap
gate in scripts; use the JSON for per-finding handling.

## What it deliberately does NOT do
It does not paraphrase-match, fuzzy-match, or judge meaning. A near-miss is a miss —
the author's text must contain the quote. This strictness is the point: it converts
"I'm fairly sure the paper says…" into a checkable fact.
