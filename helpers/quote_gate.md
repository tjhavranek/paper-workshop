# quote_gate.py, usage

Deterministic quote verification (grounding rule 10). An LLM verifier shares the
hallucination it is checking, so this is a **script**, and it fails **closed**.

## When it runs
- At the barrier exiting Phase D (specialist findings), before anything enters
  cross-critique or synthesis.
- In Act II, on every quotation an edit relies on.

In Act I a relay subagent runs it via Bash at the Phase-D barrier and reports its JSON
output; no subagent judges quote presence by eye. The panel does **not** run it a second
time: the barrier result is authoritative and already enforced fail-closed there, so the
workflow transcribes it into each finding's `panel_verdicts` as the `quote-locator` row
(see `verification_panel.md`). In Act II the `quote-locator` angle is still an agent.

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
- `normalized`: matched after Unicode-NFKC + quote/dash/space canonicalization +
  zero-width/soft-hyphen removal + whitespace-collapse + casefold. The normal pass.
- `dehyphenated`: matched only after also joining `-`-at-line-break (PDF
  hyphenation). Still a pass; note it.
- `exempt-absence`: the finding is `absence-silence` with an empty quote; not gated
  HERE. Since v0.6.0 it rides the deterministic `helpers/absence_gate.py` instead
  (probe-term search, fail-closed). A `contribution-undersell` finding's foothold
  quote is NOT exempt and is gated normally.
- `empty-quote`: the quote normalized to nothing on a finding that is **not** `absence-silence`.
  Treated exactly like `none`: a fail, status forced to `needs-author-confirmation`.
- `none`: **no match. Fail closed.** The finding's `verification_status` is forced to
  `needs-author-confirmation`. The finding is **not** deleted, and its severity is
  **not** changed (rubric.md: status annotates, never vetoes).

## Exit codes
`0` if all non-exempt quotes matched, `2` otherwise. Use the exit code as a cheap
gate in scripts; use the JSON for per-finding handling.

## What it deliberately does NOT do
It does not paraphrase-match, fuzzy-match, or judge meaning. A near-miss is a miss. The author's text must contain the quote. This strictness is the point: it converts
"I'm fairly sure the paper says…" into a checkable fact.
