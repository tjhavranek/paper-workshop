# Limitations & roadmap (read this before you trust a run)

CRUCIBLE is built by people who care about research integrity, so here is the honest
account of what it does **not** yet guarantee. Several of these came from running the tool
on its own design (see [`examples/self-audit/`](examples/self-audit/)) and from an
independent review panel.

## What is genuinely enforced
- **Quote grounding** is a real, deterministic, fail-closed script (`helpers/quote_gate.py`)
  — not an LLM checking itself. An unverifiable quote is flagged, never asserted.
- **No untraced number** can enter a revised paper: a value is either an author-reviewed
  text edit or the output of a logged re-run of the author's own code (the Runner/Scribe
  split). This is a strong control.
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
- **The "consistency" and "numeric-provenance" verifiers are LLM-audited, not deterministic
  scripts** (only the quote-gate is a real script today). Hardening them — a re-hash of every
  transcribed value and a numeric cross-reference checker — is on the roadmap.
- **Coverage means attention, not correctness.** The sentence-coverage ledger certifies every
  range was *examined*, not that each was *correctly* reviewed; a flaw can hide in a
  "covered" range.
- **Act II's reproduction check needs a precise predicate.** "Reproduces" must be defined per
  artifact class with float tolerance, fixed seeds, and environment capture; until that ships
  and is demonstrated end-to-end on a real paper, treat Act II as *designed, demonstrated in
  part* — and re-derive any number yourself before trusting it.
- **A self-audit is a development pass, not independent validation.** The example in this repo
  is the tool reviewing its own design; that is a closed loop and we label it as such.

## Roadmap
1. A measured validation run (recall + false-positive rate) on third-party papers; lead the
   README with the number.
2. Deterministic `consistency.py` + output re-hashing for the Act-II rails.
3. A precise Act-II reproduction predicate (tolerances, seeds, environment).
4. An optional **independent numerical re-derivation** pass (recompute a key result a second
   way to catch a real coding error; labeled, never auto-applied).
5. Make the cross-provider dissent leg a first-class, easy opt-in.

If any of these matter to your decision, weigh the output accordingly — and tell us what
breaks.
