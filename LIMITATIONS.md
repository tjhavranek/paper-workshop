# Limitations & roadmap (read this before you trust a run)

CRUCIBLE is built by people who care about research integrity, so this is the
account of what it does **not** yet guarantee. Several of these came from running the tool
on its own design (see [`examples/self-audit/`](examples/self-audit/)) and from
adversarial cross-review during development.

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
- **Absence claims now have their own deterministic gate** (`helpers/absence_gate.py`):
  every "the paper never says X" finding carries a probe of refuting terms that the script
  searches, fail-closed (a missing, thin, or hit-producing probe degrades the finding's
  status). What the certificate covers is the SEARCH, not semantics: a paraphrase outside
  the probe can still exist, and that semantic half stays LLM-judged (the steelman
  verifier, fed the gate's hit snippets) and is labeled as such here.
- **The Contribution Memo cannot enter the must-fix list**: on the Workflow path,
  `contribution-undersell` findings reach the chair through their own channel, land only
  in the capped (3) memo, are stripped from the must-fix list, and have their status
  forced to needs-author-confirmation, all in code (in Desk Review and the subagent
  fallback the orchestrator applies the same rules by instruction). Keeping the memo out
  of the chair's verdict prose is a prompt constraint, not code. Each item must carry a
  quote-gated foothold AND an absence certificate.

## What is *not* yet proven or fully enforced
- **No measured effectiveness numbers yet.** We have not yet published a run on third-party
  papers with known/planted flaws scoring **recall** (does it catch the real flaws?) and
  **false-positive rate** (does it manufacture confident wrong "must-fix" items?). Until
  that exists, treat the output as *one very thorough opinion*, not validated ground truth.
  This is the single most important piece of future work.
- **Same-model decorrelation is a design bet, not a proof.** Commit-and-reveal isolation
  removes inter-agent herding, and rival objective functions reduce sycophantic agreement,
  but every seat is the same model class and can share a blind spot. A fleet's agreement is
  *not* independent corroboration. The optional, off-by-default external (cross-provider)
  "what did we all miss?" leg is the intended mitigation; enable it for anything
  high-stakes.
- **The Act-II numeric rails now have deterministic backing, with an LLM layer on top.**
  `helpers/provenance.py` re-hashes each output artifact and confirms the transcribed value
  occurs in it as a standalone number (the Execution-Provenance Wall); binding that number to
  the cited cell or row stays LLM-judged, and the input-data hash is checked only when a data
  file is supplied. `helpers/consistency.py` run-matches every token
  value and flags orphans, `helpers/reproduces.py` defines the reproduction predicate, and
  `helpers/integrity_diff.py` flags net result-removals — all fail-closed, like the quote-gate.
  What stays LLM-judged (and is labeled as such): the *semantic* half — does a quantity match
  across the abstract/table/appendix by meaning, and is an edit HARKing or spin. The numeric
  extractors are best-effort (they read the source text), so a number written in unusual markup
  can still need the human eye.
- **Coverage means attention, not correctness.** The sentence-coverage ledger certifies every
  range was *examined*, not that each was *correctly* reviewed; a flaw can hide in a
  "covered" range.
- **Sentence coverage is only instrumented when close-reader sweeps actually return coverage.**
  In practice that means Symposium and Summit, the tiers that cast sweeps; below them nothing
  returns a per-range verdict. The code keys off the returned data rather than the tier, so a
  heavy run whose sweeps all died is also reported as uninstrumented instead of as full coverage.
  The certificate then reports `sentences_covered: 0`, set by code, meaning *not measured on this
  run* — not *not read*. Every seat reads the whole manuscript in every mode, and claim and dimension
  coverage are unaffected. Before v0.8.3 the auditor was handed the sentence map at every tier
  and supplied a count regardless: the committed Roundtable self-audit shows 648 of 795
  sentences "covered" on a run with zero close-reader seats and zero returned ranges. That
  number was an inference. Treat sentence counts in run records produced before v0.8.3 at
  Desk Review, Roundtable or Workshop as unmeasured.
- **Act II is now demonstrated end-to-end once, but not broadly field-proven.**
  `helpers/reproduces.py` decides "reproduces" per artifact class (float tolerance + fixed
  seeds; see its `classes` table), so the baseline gate and the package clean-room check are
  code-derived, not asserted. Act II has now been run end-to-end once on a real accepted paper
  (`examples/incentives-workshop/phase2_true/`). The record: both the Stata and R/BMA paths were
  re-executed (running the authors' `incentives.do` in Stata 15.1 regenerates the R-feed
  intermediate byte-identically to the shipped one, closing the chain raw data → Stata → R →
  manuscript); `helpers/provenance.py` tied the headline (0.0724) to a content-hashed run artifact
  and hashed input; `helpers/consistency.py` was clean on the run host (recorded from the run);
  and the manuscript was redlined against its real LaTeX source — the headline reproduced.
  Caveats, so this is a demonstration and not independent validation: one paper, from the
  authors' own group, in a single run; the numbers already reproduced, so the redline stayed
  prose-only and the path where a re-run value replaces a stale number was never exercised; and
  environment capture is not yet container-pinned. Treat Act II as *built, [unit-tested](.github/workflows/ci.yml), and
  demonstrated once* — and re-derive any number yourself before trusting it.
- **The Contribution Memo's selection is a same-model judgment with no measured
  undersell-recall yet.** The gates verify each memo item's anchors (the foothold quote is
  real; no probe term for the bolder claim occurs in the paper, which certifies the
  search, not the semantics; those stay with the steelman verifier). They cannot verify that the
  bolder claim is RIGHT, that the best undersell candidates were found, or that the
  ranking is not pulled toward the model's consensus priors, which is the very failure
  mode the contribution wing exists to counter. There is no measured undersell-recall or
  false-suggestion rate yet (see Roadmap). Treat the memo as a grounded option set the
  author ratifies, never as a verdict on what the contribution should be.
- **Improvement Mode is an opt-in, unvalidated generative wing.** With `improvement: true`, one or
  more `S-improvement-architect` seats propose bolder defensible claims, analyses worth running, and
  reframings into a non-blocking, mode-scaled Improvement Memo, and Act II can draft them as
  author-rejectable tracked changes (more at heavier tiers). Every item rides the same deterministic
  gates (foothold quote + absence probe) and the same verification panel as a defect finding, and
  nothing auto-applies (proposal-only, author sign-off, the Execution-Provenance Wall on any
  number). But WHICH improvements surface, and whether a "bolder claim the results support" is
  actually right, are same-model judgments with no measured improvement-recall or false-suggestion
  rate yet, the same limitation as the Contribution Memo on a wider jurisdiction; a bolder
  generative claim is exactly where a same-model panel is least able to refute itself. Off by
  default, so a normal run is unaffected; treat the memo and its drafted edits as a grounded option
  set the author ratifies in track changes, never as a verdict on how the paper should change.
- **The related-literature scout widens the lens but cannot certify coverage or
  importance, and fetch-or-drop is a mandate, not a check.** The scout is instructed,
  strictly, to stage only works it actually opened in this run, and the leads list rests
  on the scout's own report that a DOI/URL resolved; no script yet verifies a staged
  note against the fetched text (that deterministic check is future work). Nor does
  anything guarantee the scout searched the right corners: which "overlooked" works
  surface is itself a model judgment. Leads are kept outside the staged-sources tree so
  seats and verifiers never read them as evidence.
- **The economy register is field-tested once, not blind-validated.** The economy casting map
  (judgment layers at the Opus floor, mechanical phases on Sonnet, scout/chair/scribes at the
  session model) matches one real Workshop-band run that delivered a strong verified ledger
  (60 findings, 11 High, full claim and sentence coverage); that run's record shows 3.70M
  subagent tokens and 55 minutes for its 37-agent tribunal workflow, 39 Act I agents in
  total. That is evidence of plan survival with output strength preserved on ONE paper — not
  measured recall/false-positive parity with the full-power default. Open validation arms, none
  of which becomes a default or is documented safe before its arm passes: a Sonnet verification
  panel (full and per-angle variants), Sonnet generalists, Haiku gate relays (a deterministic
  row-parity check), the panel span-diet (excerpts instead of the full manuscript for the
  local-judgment angles), and flipping economy to the default. Custom `models` maps beyond the
  shipped economy cast are entirely unvalidated and run labeled `custom`.
- **The quote gate verifies a quote exists, not that it sits where the finding says.**
  `helpers/quote_gate.py` confirms each quote occurs verbatim somewhere in the manuscript; it
  does not yet map the match back through the sentence map to confirm the quote actually
  appears at the finding's claimed section or sentence range. A real quote pinned to the wrong
  locator (a misattributed section, a transposed line) passes the deterministic rail and is
  caught only by the LLM verification angles, not by code. Findings carry a locator
  (`location.sentence_range` / `section`), but seats fill it inconsistently and many findings
  give a free-text section only, so a deterministic locator check is not yet reliable across
  runs. Treat the locator on a finding as a pointer to check, not a code-verified fact.
- **A self-audit is a development pass, not independent validation.** The example in this repo
  is the tool reviewing its own design; that is a closed loop and we label it as such.

### Process metrics from the known runs (process, not outcome)

These are PROCESS numbers from the runs whose records are committed in this repo or already
disclosed above. They describe how the pipeline behaved (how many findings the panel dropped,
what the gates checked), NOT whether the findings were correct. They are not recall,
precision, or any measured-effectiveness number, none of which exists yet (see the first
bullet of this section and the Roadmap).

| Run | Mode / register | Agents | Raw -> delivered | Panel-rejected | Quote-gate | Severity |
|---|---|---|---|---|---|---|
| Self-audit (`examples/self-audit/`) | Roundtable (quick) / brutal | 42 | 80 -> 69 | 11 | not recorded | 31 High / 29 Med / 9 Low |
| Incentives meta-analysis (`examples/incentives-workshop/`) | Workshop (thorough) / supportive | 27 | 137 -> 131 | 6 | 108 matched, 1 downgraded, 28 absence-exempt | 45 High / 58 Med / 34 Low |
| Economy field run (disclosed above) | Workshop-band / economy | 39 (Act I) | -> 60 delivered | not recorded | not recorded | 11 High (rest not recorded) |

Notes: the self-audit is the tool reviewing its own design (a closed loop, not validation)
and ran Act I only; the incentives run is a demonstration on one already-accepted paper from
the authors' own group; the economy field run is the single Workshop-band economy pass
already described above (3.70M subagent tokens, 55 minutes, for its tribunal workflow), and
unlike the other two rows it is author-disclosed only, with no committed record in this repo.
The Severity column's basis is not uniform: the self-audit and economy counts are over the
delivered set, while the incentives row's 45 / 58 / 34 is the post-calibration set (137,
before the 6 panel rejections), so it sums to the raw count, not the 131 delivered. A
"not recorded" cell means the figure is not in a committed record, so it is left out rather
than estimated.

## Roadmap
1. A measured validation run (recall + false-positive rate) on third-party papers; lead the
   README with the number. Extend its design with two contribution-side arms before it
   runs: **undersell-recall** (papers with known under-claimed contributions seeded; does
   the memo recover them?) and **consensus-deference** (seeded flaws that contradict
   field-standard methods; do seats defer to convention?), plus an **improvement-recall /
   false-suggestion** arm for opt-in Improvement Mode (papers with known available strengthenings
   seeded; does the Improvement Memo recover them without manufacturing unsupported ones?). Add the
   casting arms listed above (economy vs full power, Sonnet panel, Sonnet generalists, Haiku relays,
   span-diet) to the same harness.
2. End-to-end Act-II runs on **independent third-party** papers. The first end-to-end
   demonstration is done (`examples/incentives-workshop/phase2_true/`, both the Stata and R
   paths re-executed); broad, independent field-proofing is the next step.
3. Default environment pinning (a container/lockfile) for the reproduction predicate.
4. An optional **independent numerical re-derivation** pass (recompute a key result a second
   way to catch a real coding error; labeled, never auto-applied).
5. Make the cross-provider dissent leg a first-class, easy opt-in.
6. A deterministic locator check: once seats emit a parseable sentence-map id on every
   finding, map the quote's match offset through the sentence map and confirm it falls in
   the claimed range, degrading a mismatch to needs-author-confirmation (annotate, never
   delete).

If any of these matter to your decision, weigh the output accordingly — and tell us what
breaks.
