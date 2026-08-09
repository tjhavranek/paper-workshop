# absence_gate.py — usage

Deterministic absence certificate (grounding rule 9). Absence-class findings ("the
paper never says X") have no quote to gate, so this **script** searches the manuscript
for every term in the finding's `absence_probe` — the words and close paraphrases whose
presence would refute the claimed absence. Like the quote gate, it fails **closed**.

## When it runs
- At the barrier exiting Phase D, right after the quote-gate, on every finding of
  type `absence-silence` or `contribution-undersell`.
- Inside the verification panel: the certificate is transcribed into the finding's
  `quote-locator` row by the workflow (no agent re-runs the gate), and the
  `steelman-charity` verifier uses its hit snippets as the evidence trail.

## Modes
```
# single term
python helpers/absence_gate.py check --source-file input/paper.txt --term "power analysis"

# batch: certify every absence-class finding at once
python helpers/absence_gate.py batch --source-file input/paper.txt --findings round1/findings.json
```

`batch` reads a findings JSON (an array, or `{ "findings": [...] }`) and prints
`[{ "id", "certified", "terms_searched", "hits" }, ...]` for the absence-class findings
only (the quote gate owns everything else).

## Certificates
- `absent` — at least 3 distinct probe terms supplied (deduped on their normalized
  form), none found. The search ladder is the quote gate's canonicalization PLUS
  deliberately looser hyphen and spacing rungs: the two gates have opposite failure
  polarities, so a match the quote gate would conservatively miss must still count
  here (a miss would fail OPEN as a false certificate; over-matching only ever
  degrades a finding, never certifies one). The clean pass.
- `present` — at least one probe term occurs; `hits` carries the term, count, and up
  to 3 context snippets per term. The claimed absence is suspect: status forced to
  `needs-author-confirmation`; the steelman verifier judges whether the paper really
  already says it.
- `thin-probe` — fewer than 3 non-empty terms. A narrow probe invites a rigged
  search; **fail closed**, status forced to `needs-author-confirmation`.
- `no-probe` — no usable terms at all. Fail closed, same handling.

## Exit codes
`0` if every absence-class finding certified `absent`, `2` otherwise.

## What it deliberately does NOT do
It certifies the **search**, not the semantics: a paraphrase outside the probe can
still exist in the paper, which is why the panel's steelman angle stays on top of this
gate, and why a certificate annotates a finding's status but never raises its severity
or deletes it (rubric.md: status annotates, never vetoes).
