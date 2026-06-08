# Limitations & roadmap (read this before you trust a run)

CRUCIBLE is built by people who care about research integrity, so this is the
account of what it does **not** yet guarantee. Several of these came from running the tool
on its own design (see [`examples/self-audit/`](examples/self-audit/)) and from an
independent review panel.

## What is genuinely enforced
- **Quote grounding** is a real, deterministic, fail-closed script (`helpers/quote_gate.py`)
  — not an LLM checking itself. An unverifiable quote is flagged, never asserted.
- **No untraced number** can enter a revised paper: a value is either an author-reviewed
  text edit or the output of a logged re-run of the author's own code (the Runner/Scribe
  split), now re-checked deterministically — `helpers/provenance.py` re-hashes the output
  artifact and confirms the value is in it, and `helpers/consistency.py` flags any changed
  number with no run behind it. This is a strong control.
- **Severity is firewalled from tone**: the register (`supportive`/`brutal`) is passed only
  to the chair's delivery, never to the seats or verifiers that set severity.
- **Routing is code-enforced**: anything that changes a number, sample, claim, or result is
  queued for author sign-off; it cannot auto-apply.

## What is *not* yet proven or fully enforced
- **No measured effectiveness numbers yet.** We have not yet published a run on third-party
  papers with known/planted flaws scoring **recall** (does it catch the real flaws?) and
  **false-positive rate** (does it manufacture confident wrong "must-fix" items?). Until
  that exists, treat the output as *one very thorough opinion*, not validated ground truth.
  This is the single most important piece of future work.
- **Same-model decorrelation is a design bet, not a proof.** Commit-and-reveal isolation
  removes inter-agent herding, and rival objective functions reduce sycophantic agreement —
  but every seat is the same model class and can share a blind spot. A fleet's agreement is
  *not* independent corroboration. The optional, off-by-default external (cross-provider)
  "what did we all miss?" leg is the intended mitigation; enable it for anything
  high-stakes.
- **The Act-II numeric rails now have deterministic backing, with an LLM layer on top.**
  `helpers/provenance.py` re-hashes each output artifact and confirms the transcribed value is
  present (the Execution-Provenance Wall), `helpers/consistency.py` run-matches every token
  value and flags orphans, `helpers/reproduces.py` defines the reproduction predicate, and
  `helpers/integrity_diff.py` flags net result-removals — all fail-closed, like the quote-gate.
  What stays LLM-judged (and is labeled as such): the *semantic* half — does a quantity match
  across the abstract/table/appendix by meaning, and is an edit HARKing or spin. The numeric
  extractors are best-effort (they read the source text), so a number written in unusual markup
  can still need the human eye.
- **Coverage means attention, not correctness.** The sentence-coverage ledger certifies every
  range was *examined*, not that each was *correctly* reviewed; a flaw can hide in a
  "covered" range.
- **Act II is now demonstrated end-to-end once, but not broadly field-proven.**
  `helpers/reproduces.py` decides "reproduces" per artifact class (float tolerance + fixed
  seeds; see its `classes` table), so the baseline gate and the package clean-room check are
  code-derived, not asserted. Act II has now been run end-to-end once on a real accepted paper
  (`examples/incentives-workshop/phase2_true/`): the authors' own Stata and R/BMA paths were
  re-executed, `helpers/provenance.py` tied the headline (0.0724) to a content-hashed run artifact
  and hashed input, `helpers/consistency.py` was clean, and the manuscript was redlined against its
  real LaTeX source — the headline reproduced. Caveats, so this is a demonstration and not
  independent validation: one paper, from the authors' own group; both the Stata and R paths were
  re-executed (running the authors' `incentives.do` in Stata 15.1 regenerates the R-feed intermediate
  byte-identically to the shipped one, closing the chain), and the prose-only redline changed no
  number because the numbers already reproduced; a single run; and environment capture is not yet
  container-pinned. Treat Act II as *built, unit-tested, and demonstrated once* — and re-derive any
  number yourself before trusting it.
- **A self-audit is a development pass, not independent validation.** The example in this repo
  is the tool reviewing its own design; that is a closed loop and we label it as such.

## Roadmap
1. A measured validation run (recall + false-positive rate) on third-party papers; lead the
   README with the number.
2. End-to-end Act-II runs on **independent third-party** papers and across the **Stata** path
   (the interpreter path actually re-executed). The first end-to-end demonstration is done
   (`examples/incentives-workshop/phase2_true/`); broad, independent field-proofing is the next step.
3. Default environment pinning (a container/lockfile) for the reproduction predicate.
4. An optional **independent numerical re-derivation** pass (recompute a key result a second
   way to catch a real coding error; labeled, never auto-applied).
5. Make the cross-provider dissent leg a first-class, easy opt-in.

If any of these matter to your decision, weigh the output accordingly — and tell us what
breaks.
