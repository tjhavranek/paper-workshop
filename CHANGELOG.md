# Changelog

## v0.3.3 — 2026-06-08
Showcase polish for the incentives example (reviewed by an adversarial fleet; presentation only, no
new claims).

- **Promoted the rarest result to the top** of `examples/incentives-workshop/README.md`: a short lede
  banner that the run re-ran the authors' own Stata + R end to end and regenerated the data
  byte-for-byte identical, with the deterministic provenance proof, so a visitor sees it in the first
  lines instead of half a page down.
- **Surfaced the flagship example in the main README** with a "See it on a real paper" pointer near
  the differentiator section (it had only appeared inside limitations asides).
- Reconciled the 2,193 vs 1,252 estimate figures (1,252 is the BMA subsample of the full 2,193) and
  trimmed a few em-dashes. The honest scope and every caveat are unchanged.

## v0.3.2 — 2026-06-08
Completed the Stata path of the incentives end-to-end example.

- **Ran the authors' `incentives.do` in Stata 15.1** on the raw `incentives.xlsx` (a copy; the
  original was untouched). Clean run (exit 0, no `r(N);` errors). It regenerates the R-feed
  intermediate `incentives_4R.csv` **byte-for-byte identical** to the shipped one (sha256
  `46df404…`, 1,252 rows), which is exactly the file the R/BMA pass recorded as its
  `input_data_hash`. So the chain raw data -> Stata -> R/BMA -> manuscript is now closed and
  deterministic, plus the full FAT-PET / publication-bias tables regenerate.
- **Added a lightweight, auditable proof set** under `examples/incentives-workshop/phase2_true/stata/`:
  `STATA_REPRODUCTION.md`, the regenerated FAT-PET tables, a focused log excerpt, and a provenance
  token + `helpers/provenance.py verify` output (`verified: true`) + a `hashes.json` recording the chain.
- **Reconciled the docs** (README, LIMITATIONS, the example README + REPRODUCTION) so the example is
  described as one end-to-end demonstration with **both the Stata and R paths re-run**, still honestly
  scoped (one paper, the authors' own group, a single run, not independent validation).

## v0.3.1 — 2026-06-07
Reconciliation pass (reviewed via a small adversarial debate): merge a pending fix and correct two
inaccuracies that had crept in.

- **Merged the leading-dot / identifier-boundary fix** to the deterministic numeric gates
  (`consistency.py` + `provenance.py`): `.05` now reads as `0.05`, and an identifier digit
  (`model_1`, `file2.txt`) no longer false-matches a bare number. Stdlib-only; all four helper
  selftests pass.
- **Corrected the engine guidance.** The docs implied dynamic workflows bypass the model/context
  inheritance; they do not (Workflow-spawned agents inherit the session model just as direct
  subagents do). The 1M-context credit caveat is now stated as engine-independent in
  `helpers/doctor.md`, `README.md`, `SKILL.md`, and `helpers/orchestration.md`: CRUCIBLE runs at
  full power on Max; on Pro, enable usage credits for the 1M tier or run the session on a
  standard-context model (`/model sonnet`). Neither remedy weakens the tool.
- **Reconciled the "field-proven" claims** with the shipped end-to-end demo: Act II has now been
  demonstrated end-to-end once on a real accepted paper (`examples/incentives-workshop/phase2_true/`
  — R/BMA path re-executed, provenance + consistency verified, headline reproduced). README and
  LIMITATIONS now say "demonstrated once, with caveats" (one paper, the authors' own group, R-path
  only) instead of "not yet field-proven," and roadmap item 2 is re-scoped to independent
  third-party and Stata-path runs.

## v0.3.0 — 2026-06-06
README / pitch overhaul, plus a Roundtable self-stress-test pass (the skill run on its own
package: 42 agents, 69 delivered findings, 11 panel-rejected).

- **Stronger, process-first pitch.** New opening hook that doubles as the launch line: "Imagine a
  panel of AI referees built for your exact paper, arguing it out from rival schools and then
  rebuilding it, re-running your own code so the numbers are real." It promises the *process*,
  never the outcome (no "perfection", no "world's leading experts").
- **README tightened and de-AI-styled.** Merged the two overlapping differentiator sections,
  converted negation-correction antitheses to positive statements, and cut em-dashes from 26 to 5.
  Moved the "Every paper leaves changed." epigraph to a closing flourish.
- **Honesty surfaced up front.** Added a lead-section line stating that effectiveness is not
  measured yet and the rebuild is not field-proven end to end, so the front matches LIMITATIONS
  instead of back-loading the caveats. (The tool's own Roundtable self-review capped the package
  at desk-reject-risk for exactly that front/back register gap.)
- **Fixed contradictions the self-review caught:** "every mode runs on any paid plan" now states
  that the deep modes (Symposium/Summit) need dynamic workflows to run at full depth; reconciled
  the README "always runs via subagents" vs SKILL "uses workflows instead" engine description; and
  relabeled `examples/self-audit/` as a development self-audit, not a "validation run."

## v0.2.0 — 2026-06-06
Act II finishing pass — deterministic rails + wiring fixes.

- **Deterministic Act-II checkers added** (stdlib-only, fail-closed, like the quote-gate;
  each ships a `selftest`): `helpers/provenance.py` (re-hash output artifacts + confirm the
  transcribed value is in them — the Execution-Provenance Wall), `helpers/consistency.py`
  (run-match every token value + flag orphans), `helpers/reproduces.py` (the reproduction
  predicate: per-artifact-class float tolerance + fixed seeds), and `helpers/integrity_diff.py`
  (deterministic net-removal diff of {coefficients, N, samples, caveats}).
- **Wiring fixes in `workflow/phase2_atelier.js`:** the Scribe now edits a real staged git
  working copy on branch `paper-workshop/phase2` (never the author's original); the reconciler
  and packager receive resolvable paths; the package return surfaces the redline / clean
  version / changes-map / MAP paths; `decideEdit()` is fail-closed (a missing or `cant-tell`
  hard-gate verdict no longer auto-applies — it routes to author sign-off); the provenance
  token requires all seven fields; the baseline gate runs whenever code+data exist and a run
  with no baseline anchor reports `reproduced: "n/a"`; blocking intake gaps always halt.
- **Docs reconciled to the artifacts:** `helpers/safety_notes.md` no longer claims an
  unimplemented "specification ledger / analysis-lock / HARKing detector" apparatus — it names
  the scripts that exist and labels the HARKing judgment as LLM-audited; `LIMITATIONS.md`,
  `helpers/verification_panel.md`, and `helpers/phase2_sandbox.md` updated to match.
- **README / brand + UX honesty pass:** restored CRUCIBLE as a consistent brand (brand-led
  title, the "Every paper leaves changed." tagline, the name as the subject of the value
  claims, named acts TRIBUNAL/ATELIER) instead of an orphaned nickname; surfaced Act II's
  "built + unit-tested, not yet field-proven end-to-end" status in the README limits section
  and at the Act-I→II gate; added a Windows `py` install note, an explicit engine-fallback
  announcement, and a per-mode agent-count cost preview.

## v0.1.0 — 2026-06-05
Initial release.

- **Act I (Tribunal):** topic-adaptive roster generation; competing-traditions
  staffing by opposed objective functions; generalist seats (relevance /
  understandability / cross-field significance); desk-reject pre-mortem; blind
  commit-and-reveal specialists; deterministic quote-gate; integrators under rival
  lenses; multi-angle verification panel; sentence-tiling completeness audit;
  fresh-chair synthesis with locked rubric, tone-invariant severity, verbatim
  un-deletable dissent, 3-bucket venue read (no acceptance odds), preserved minority
  report.
- **Act II (Atelier):** intake/scope; four-lane triage; baseline-reproduction gate;
  Runner/Scribe split under the Execution-Provenance Wall; multi-angle edit
  verification (fix-safety / numeric-provenance / consistency / integrity); consistency
  reconciler; clean-room-replicated package with provenance-generated MAP.md;
  AI-involvement disclosure; author sign-off gate on everything touching the record.
- **Verification panel** (the multi-angle independent re-check of every comment and
  every implementation) baked into both acts; **batched by angle** so cost stays bounded
  (default Workshop mode ≈ 45–65 agents).
- **Five modes** (Desk Review / Roundtable / Workshop / Symposium / Summit) and a
  **dual engine**: runs on any paid plan via subagents, using dynamic workflows as an
  accelerator when enabled. Desk Review needs neither.
- **Citation-grounding (Phase C):** fetches the most load-bearing cited works so the
  paper's claims about the literature are checked against originals (fail-safe; never
  blocks the run; never transmits the author's unpublished results).
- **Atelier redline:** tracked-changes / latexdiff **redline** + a **clean accepted
  version** + a `changes_map.md` tying every change to the reviewer concern it answers.
- **Dogfooded on itself** before release: a real brutal Act I run on its own design. It caught
  genuine overclaims in the design **and a fail-open bug in its own quote-gate** — both fixed in
  response (the quote-gate now fails closed and tolerates BOM files). A self-audit is a
  development pass, not independent validation. (`examples/self-audit/` now holds the later
  v0.3.0 self-audit run; see the v0.3.0 entry above for its counts.)
