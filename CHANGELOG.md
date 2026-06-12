# Changelog

## v0.7.1 — 2026-06-12

Trust hardening from two further external reviews, triaged by a three-checker subagent pass
under an explicit high bar (the validation harness, both reviewers' top strategic ask, stays
deferred by owner decision; it remains Roadmap item 1).

- **CI: the rails now prove themselves on every push.** `.github/workflows/ci.yml` runs the
  six deterministic helper selftests, validates all five schemas, syntax-checks both workflow
  scripts, and re-verifies BOTH committed provenance proofs on a clean ubuntu checkout (the
  `.gitattributes -text` protection makes the byte-exact hashes reproduce cross-platform;
  every step verified locally before commit). README badge added; the "unit-tested" claims in
  README and LIMITATIONS now link to the workflow instead of standing bare.
- **The quote-locator gap is now disclosed, not papered over.** Both reviewers flagged that
  `quote_gate.py` verifies a quote exists somewhere in the manuscript, not that it sits at
  the finding's claimed locator. A deterministic locator check was scoped and REJECTED for
  now on measured grounds: in the two committed runs only 41% and 3% of findings carry a
  parseable sentence-range id (the field is voluntary and prompts never standardize it), and
  the fail-closed polarity would degrade legitimate findings far more often than it would
  catch the rare mislocated quote. Instead: the verification-panel doc's overclaiming
  quote-locator row is corrected, LIMITATIONS names the gap plainly, and the deterministic
  check is Roadmap item 6, gated on seats emitting parseable locators first.
- **Economy severity circularity closed.** Under economy, Low findings had skipped
  severity-calibration, the only channel that can flag an under-rated Low for the chair
  (the panel never raises a severity itself). Lows now get the quick gate set PLUS
  severity-calibration, at the cost of one extra angle on the minority Low batch.
- **The manuscript is now named as an injection vector.** Grounding rule 11 extends from
  inter-agent packets to the manuscript text and web-fetched sources: an imperative
  addressed to an AI reader inside them is evidence, never a directive. The cartography
  agent additionally writes a report-only `injection_scan.md` (never blocks, changes no
  finding) and the report header notes any hit; the subagent fallback carries the same
  instruction.
- **Every report now carries the coverage caveat.** The coverage certificate renders with
  "Coverage means reviewed, not proven correct: a flaw can hide in a covered span",
  previously stated only in LIMITATIONS.
- **Process metrics, labeled as process.** LIMITATIONS gains a small table of pipeline
  numbers from the committed example runs and the disclosed field run (raw vs delivered,
  panel rejections, gate results), explicitly distinguished from the outcome numbers
  (recall, false positives) that do not exist yet.
- **Small fixes.** ORCID iDs added to CITATION.cff (both verified against the ORCID public
  API); the README Modes heading dropped its redundant parenthetical.
- Also reviewed and rejected this pass, for the record: a tests/ wrapper (the selftests are
  the tests), moving `examples/parse_selfaudit.js` (three committed references point at its
  current path), a README four-way split (just streamlined in the prior pass), a shipped
  smoke-test PDF, LLM-behavior integration tests in CI (non-deterministic, would make the
  rails signal flaky), an environment lock-file format, a fallback enforcement-report
  artifact, and the "verified research-change pipeline" reframing.

## v0.7.0 — 2026-06-12

The economy register: the workshop now fits a usage-capped plan without trading away a single
rail. Motivated by a real failure (a default all-Fable Workshop exhausted a Max-20 window in
about two hours, mid-run) and two owner field patches that fixed it ad hoc; designed through a
three-position adversarial debate (token-economy engineer / quality guardian / maintainer,
brief-seeded, chair hunches withheld) with a fresh-context judge, whose minority report (the
engineer's case for flipping the default and for a Sonnet panel) is preserved in the project
records for re-adjudication once blind-validation data exists.

- **The `economy` register (opt-in, always disclosed; the default is unchanged session-model
  inheritance).** `economy: true` casts the fleet in two tiers: judgment layers (specialist
  seats, generalists, premortem, cross-critique integrators, the verification panel, and Act
  II's runner, triage, reconciler, package) at the Opus floor, never below; mechanical phases
  (cartography, grounding, gate relays, completeness, Act II intake/staging/disclosure) on
  Sonnet; the scout, the chair, and Act II's scribes ALWAYS at the session model (both field
  runs independently kept them there under explicit cost pressure). Every deterministic rail is
  identical in both modes. Field anchor (one run, disclosed as such): Act I at this cast = 39
  agents in total, its 37-agent tribunal workflow recorded at 3.70M subagent tokens in 55
  minutes, 60 delivered findings (11 High), full claim and
  sentence coverage.
- **Fail-safe casting, in code.** A spawn that returns nothing under a model override (a
  terminal API death, or a user skip — the engine cannot distinguish the two, so a skipped
  cast agent is re-run once at the session model and logged) retries once WITHOUT
  the override and logs the fallback (`casting.degraded_casting`) — a plan missing a mapped
  tier completes the run instead of crashing. A never-upgrade clamp guards the other
  direction: the orchestrator passes `session_model` in the args (the doctor mandates it
  whenever casting is on) and a mapped model ranked above the session tier inherits
  instead, logged to the casting record — so requesting economy on a Sonnet session cannot
  silently raise the run's cost; without the arg the map is applied as given and the
  doctor flags economy as not recommended on sub-Opus sessions. A raw
  `models` role→map remains as a power-user escape hatch; such runs are labeled `custom` and
  documented as unvalidated.
- **Casting disclosure is part of the record.** Both workflows return a machine-readable
  `casting` object (mode, role→model map, degraded fallbacks, caps, batch sizes) that the
  orchestrator persists to `meta.json`; whenever the mode is not `inherit`, the report header
  states the role-class cast in one sentence, and the brand sentence ("a Fable session runs
  every seat at that level") is now explicitly conditional on the default mode (SKILL.md,
  README, doctor.md, orchestration.md all updated). The doctor's end-of-run re-check now also
  covers the effective casting of inherited roles after a mid-run model migration.
- **The doctor now actively offers economy.** Pre-flight pairs the existing agent-count cost
  preview with a one-line economy offer before any Workshop-or-larger launch on a
  usage-capped Fable session — a locked-out run delivers zero findings, so the lockout becomes
  an informed choice rather than a surprise. Plus an availability note for mapped tiers and a
  notation-heavy-paper heuristic (keep cartography at the session model when extraction
  fidelity is load-bearing, since the quote gate matches against paper.txt).
- **Structural defaults tightened inside already-published claims (both modes).** The
  verification batch defaults to 25 (20 at exhaustive; `args.batch` clamped at 30) — the
  documented 15–25 range's upper end, field-validated; each seat now carries a standing
  findings-budget note making the long-published "at most ~8 findings" real (8 seats / 6
  generalists; 5/4 under economy; premortem and close-readers exempt); under economy the scout
  casts the lower Workshop band (8–12 specialists) with rival pairs and the engine-injected
  contribution floor never trimmed.
- **Act II restructured (every mode): Runners parallel, Scribes sequential, verification
  batched by angle across edits.** The original per-edit pipeline ran scribes concurrently
  against ONE working copy on ONE git branch — a real race on the file and the commit
  history, caught and fixed in the owner's field patch and now the engine default — and
  fanned verifiers out per edit (edits × angles agents). Verification now costs
  angles × ceil(edits/`verify_batch`) with identical fail-closed `decideEdit()` gating;
  scribes apply edits in ordered batches (`scribe_batch`, default 5), one commit per edit.
- **Span-diet (experimental, opt-in inside economy only).** `span_diet: true` lets the
  local-judgment panel angles read per-batch verbatim excerpts (quote + surrounding context,
  staged by a slicer agent) plus the precis instead of re-reading the full manuscript;
  quote-locator's deterministic gate still runs against the FULL paper.txt, steelman-charity
  keeps the full manuscript in every mode, a diet verifier that cannot adjudicate returns
  cant-tell (fail-closed), and a missing excerpt falls back to the full text. Unvalidated, so
  off by default and listed as a validation arm in LIMITATIONS.
- **Budget-target integration.** A harness token target (a "+500k"-style budget) auto-enables
  economy plus a small deterministic ladder — tighten the findings caps, raise the batch
  toward the clamp — with every action logged to `budget_actions`; the ladder never
  model-downgrades judgment layers below the economy floor. `economy: false` opts out.
- **Gate relays stop reading the manuscript.** Both relay prompts now state what was always
  the design: the Python gate reads the source file from disk; the agent passes paths and
  returns the script's JSON verbatim. Pure waste removal, no rail change.
- **The completed field run's own memo, folded in.** The Workshop-band field run finished
  (Act I + Act II end to end, ~6.1M subagent tokens including two baseline-gate retries)
  while this release was being built, and its orchestrating session left a grounded
  memo; its remaining recommendations landed here. (a) Severity-tiered panel under
  economy: Low findings get the quick three-angle set — safe because calibration only
  lowers, Lows never drive the verdict, and the hard logical-validity gate plus the
  steelman stay on every finding. (b) Findings word diet: seat prompts now cap
  issue/why/fix wording (~80/60/60 words), since findings bytes are re-read by every
  integrator and verifier downstream. (c) The chair persists `findings_ledger.json` and
  `synthesis_raw.json` to the session (best-effort, disclosed; the returned object stays
  the source of truth), and orchestration now tells the orchestrator to read files, not
  the blob — a large run's full return exceeds the notification channel. (d) Act II
  dependency pre-flight in the doctor: grep do-files for SSC commands and R sources for
  library() calls BEFORE any launch; a missing package becomes one consented question at
  kickoff instead of failed baseline attempts against a network-off sandbox. (e) Gate
  calibration defaults in the sandbox notes: precision-matched tolerances (half a unit of
  the anchor's last stated digit) and the consistent-horizon-mapping rule for LP/IRF
  papers, both of which a field attempt was lost to. (f) Consumed-token reconcile split:
  the deterministic run-match covers only tokens a scribed edit transcribed; unconsumed
  run byproducts are documented, never failures — orphan detection still sees every
  changed number. (g) Premortem dedup (the scout no longer casts a seat the engine
  already runs) and a completeness auditor keyed off delivered finding types and seat
  jurisdictions, not location strings (a field run produced false NOT-COVERED flags that
  would have triggered needless reopen rounds at the heavy tiers). (h) Resume
  (`resumeFromRunId` after fail-closed halts) documented as the primary cost containment:
  field-measured at 0.1-0.2M tokens per halted-baseline retry instead of a fresh run.
- **Supersedes the v0.4.0 deliberate non-change on per-agent model casting** (recorded below,
  kept intact). Its premise is stale: the per-agent `model` option is now documented public
  API on both the Agent tool and the Workflow engine's `agent()` call. The other half of that
  v0.4.0 caveat still stands and is restated in LIMITATIONS: no cross-tier quality or
  decorrelation benefit is measured yet, which is why economy is opt-in, the deeper cuts
  (Sonnet panel, Sonnet generalists, Haiku relays, span-diet, economy-as-default) are named
  validation arms rather than defaults, and the blind-validation harness remains the
  project's top queued item.

## v0.6.0 — 2026-06-11

The contribution wing: the workshop now argues FOR the paper as rigorously as it argues
against it, with the same fail-closed discipline. Designed through a three-layer adversarial
process (a rival-pair debate with judge; a full mad-research cross-model audit of the design
memo, whose six surviving criticisms reshaped the mechanics; and a Claude-only repair and
sequencing panel). The audited design decisions: undersell suggestions must ride deterministic
gates on BOTH halves, must be non-blocking in code rather than by instruction, and ship with
the honest caveat that their selection remains same-model judgment with no measured
undersell-recall yet.

- **New deterministic helper: `helpers/absence_gate.py` (+ `absence_gate.md`), closing a
  pre-existing gap.** Absence-class findings ("the paper never says X") were quote-EXEMPT and
  rode an unverified rail since v0.1. Every such finding now carries an `absence_probe` (at
  least 3 refuting terms including paraphrases, deduped on their normalized form so
  near-duplicates cannot pass the floor) searched deterministically against the manuscript
  with the quote-gate's own normalization (imported, so the two gates cannot drift) PLUS
  deliberately looser hyphen and spacing rungs: the two gates have opposite failure
  polarities, so where a missed match fails closed for the quote gate it would fail OPEN
  here, and the extra rungs only ever push a finding toward "present", which degrades it.
  Fail closed: a missing, thin, or hit-producing probe degrades the finding to
  needs-author-confirmation; hit snippets ride along as the steelman verifier's evidence
  trail. Certifies the SEARCH, not semantics; the semantic half stays LLM-judged and is
  labeled as such in LIMITATIONS. 23 selftest assertions, including the
  hyphenated-compound-split-at-a-line-break case that a quote-gate-strict ladder would
  have false-certified.
- **The contribution claim is now a permanently contested choice.** Every roster staffs the
  rival pair S-contribution-maximizer (find-the-strongest-defensible-version: the boldest
  claim the paper's OWN results support but never make) vs S-contribution-prosecutor
  (find-the-fatal-flaw on the framing). The scout's prompt mandates the pair and the engine
  injects it if omitted (close-reader pattern), so the floor survives a forgetful cast and a
  caller-supplied roster alike; the injection predicate matches seat names only (not
  jurisdictions, which mention the word "contribution" incidentally) and logs whenever it
  fires, so a transcript shows whether the floor was scout-cast or engine-injected.
- **New finding class `contribution-undersell`, gated twice.** Its `quote` is the
  under-leveraged result (the foothold, through the normal quote-gate); its `absence_probe`
  certifies the bolder claim really is absent (through the absence gate). Schema'd in
  `schemas/finding.schema.json` and the inline workflow mirror; seat, generalist
  (relevance + cross-field ask the undersell question), integrator (priority capped at
  `nice`), and panel prompts (inverted decision-relevance; steelman reads the gate hits)
  all updated.
- **The Contribution Memo: non-blocking by code, capped at 3.** Verified undersell findings
  reach the chair only through their own `CONTRIBUTION_JSON` channel; the canonical
  `schemas/synthesis.schema.json` and the inline workflow mirror both gain
  `contribution_memo` (bolder_claim / grounded_in / risk_of_overreach), and
  `schemas/finding.schema.json` gains the engine-attached annotations the ledger actually
  carries (`absence_gate`, `panel_verdicts`); after the chair returns, the engine strips
  any undersell id from `prioritized_findings`, caps the memo, and forces every undersell
  finding's verification_status to needs-author-confirmation, fail closed in code: the
  author ratifies any bolder claim (rule 14). Keeping the memo out of the chair's verdict
  prose is a prompt constraint (06), disclosed as such in LIMITATIONS. Report bundle
  (orchestration Step 5) renders it as its own clearly-labeled section.
- **Related-literature scout (Ground phase), fetch-or-drop.** A second grounding agent hunts
  works the paper does NOT cite under an anti-popularity mandate (adjacent fields, pre-2000,
  working-paper series, non-US journals); a work becomes a staged note only if its text was
  actually opened in-run, and unfetchable candidates are listed as leads (resolved DOI/URL
  only) in a file kept OUTSIDE the staged-sources tree, so seats and verifiers can never
  read them as evidence. Fetch-or-drop is a strict scout mandate, not a deterministic
  check (no script yet verifies a staged note against the fetched text); LIMITATIONS says
  so plainly. Tier-scaled (0 at quick, 5 thorough, 8 exhaustive,
  12 monumental), fail-safe like the cited-works grounding, positional result handling so a
  failed cited-works agent cannot be misread as the scout.
- **Docs aligned:** grounding rule 9 amended (first-class, quote-exempt, absence-gated) and
  rule 10 clarified (the undersell foothold is NOT exempt); the quote-gate's own docstring
  and quote_gate.md updated (absence findings now ride the sibling gate, not nothing);
  coverage rubric dimension 1 now reads "neither overclaimed nor undersold" and names the
  pair; SKILL.md gains "The contribution wing" section; README gains the "It also argues FOR
  your paper" bullet; LIMITATIONS gains the enforced-side entries (absence gate, memo
  cannot enter the must-fix list) and the not-proven entries (same-model selection, no
  undersell-recall; scout coverage not certified, fetch-or-drop is a mandate not a check);
  roadmap item 1 extended with the undersell-recall and
  consensus-deference validation arms; desk-review mode wires the gate and the memo;
  orchestration documents `paths.absence_gate` (omitted = absence findings fail closed);
  integrators give undersell findings their own clusters so a merged cluster can neither
  drag a real flaw down to `nice` nor smuggle undersell substance into the must-fix list.
- **Pre-push stress test, two blind auditors (engine/code lane + prompts/docs/claims lane),
  all findings folded in before release.** The code auditor confirmed a fail-open
  hyphenation case inside the new gate (fixed with the looser ladder + selftests), a
  floor-injection predicate suppressible by a substring coincidence (narrowed + logged),
  ledger annotations missing from the published finding schema (added), and a leads file
  readable by evidence-citing agents (moved out of the staged tree). The docs auditor
  caught the canonical synthesis schema lagging the inline mirror (updated) and a set of
  enforced-vs-instructed overclaims ("certifies the claim is absent", "guarantees",
  "every run"), each rewritten to the mechanism actually shipped.

## v0.5.0 — 2026-06-11

The tool run on itself, at scale: a Roundtable self-review on Claude Fable 5 (the fleet inherits
the session model), with 76 quote-gated findings from 11 blind seats (two rival pairs, a
premortem, a completeness critic, a records-consistency auditor), each finding cleared or
rejected by a blind three-angle verification panel, plus one-shot advisory reviews from two
external models (lower-weight by design; every adopted external point was independently probe-
or code-confirmed first). 72 findings delivered; the panel rejected 4 as re-litigating settled
design or already addressed. Everything below passed the full ritual set: 96 selftest assertions
across the five deterministic helpers, both workflow scripts, schema validity, and both
committed provenance proofs.

- **Deterministic gates hardened; probe-confirmed fail-opens fixed, each with new selftests.**
  `provenance.py` + `consistency.py`: the thousands-comma regex no longer merges a European
  decimal (a token "118" verified against text saying "1,18") or CSV fields; the dash family
  (en/em dash and friends) maps to ASCII minus before extraction so negatives keep their sign
  (a positive token reconciled against "–0.10"); exponent matching is case-insensitive;
  `provenance.py verify` requires the output file to resolve inside `--artifact-dir` (an
  absolute path or ".." escape fails closed); `consistency.py check` fails closed on a vacuous
  run (zero parsed tokens and no baseline, e.g. a typo'd top-level key); `reproduces.py` fails
  closed on an empty baseline, honors per-number tolerance classes from the baseline/CLI side
  only and rejects unknown class names (defense-in-depth hygiene: the same agent writes both
  comparison files, so this is not a security boundary); `quote_gate.py` batch mode, the
  production path, now has selftest coverage including the absence-exemption-abuse case.
- **Act-I engine (`phase1_tribunal.js`): fail-closed aggregation.** A finding the quote-gate
  relay drops is treated as unverified (was: silent keep of the seat's self-reported status);
  panel ties and cant-tell-only verdicts never pass a hard gate (a 1-1 reject tie at the
  redundant tiers used to deliver as clean); the chair now receives findings with their panel
  verdicts plus the panel-rejected list, so `panel_summary` and `rejected_suggestions` are
  data-backed, and the run output carries the verdicts for the session's `verification/`
  record; the roster floors (at least one seat, three generalists, nonempty justifying quote)
  are enforced in the inline schema; caller-staged sources survive when in-run grounding stages
  nothing; the premortem kill-shot routing label is set by the workflow, not the agent (an
  agent-phrased tradition string could silently empty the verbatim channel); severity revisions
  parse the explicit `High->Medium` arrow form first.
- **Act-II engine (`phase2_atelier.js`): three missing halts added.** A baseline run that
  crashes now halts exactly like a diverging baseline (previously only `baseline-failed`
  halted); a dirty reconcile (orphans, mismatches, run-mismatches, integrity flags) halts
  before packaging, which makes the documented terminal gate real and deterministically
  backstops any triage misclassification; Intake actually receives the finding ledger under
  the documented args (was: a literal `(inline)` placeholder); the Scribe receives all of the
  Runner's provenance tokens (multi-value numeric edits were unimplementable); the baseline
  Runner gets the manuscript source to anchor "current numbers"; the disclosure audit trail
  includes blocked edits and an honest pending-sign-off status.
- **Stale claims reconciled to the repo's own record** (the staleness was independently found
  by four sources): SKILL.md and the orchestration Step-6 gate text no longer say Act II is
  "not yet field-proven end to end", which had contradicted README/LIMITATIONS since v0.3.1;
  the never-produced "debate transcript" deliverable is renamed to what the pipeline actually
  produces (the cross-critique crux notes); the subagent-fallback phase order now matches the
  engine; the roster-approval pause is operational (`args.roster` documented); LIMITATIONS
  roadmap item 2 dropped its stale Stata clause; the SKILL files tree gained LIMITATIONS.md,
  desk_review_mode, and the flagship incentives example it had omitted.
- **The committed R-side provenance proof verifies again, now reader-reproducibly.** git's eol
  normalization had silently rewritten `rerun_keynumbers.json` (CRLF to LF), breaking the
  recorded sha256. The original bytes are restored (provable: only the authentic sequence
  reproduces the token's hash), the run-record dirs are `.gitattributes -text` protected, and
  REPRODUCTION.md discloses the incident. The token and the verify record were never edited.
- **Example READMEs aligned to their committed ledgers** (a records-consistency auditor caught
  the framing prose overstating its own records): the incentives README reports the ledger's
  23 needs-author-confirmation findings (not 3), attributes the numeric-claim quarantine to
  REPORT.md's reopen list rather than to the panel/ledger, labels the consistency result
  recorded-from-run, and the quote-gate bullet carries the one downgraded quote.
- **Docs and contracts tightened throughout:** SKILL.md fully de-dashed (24 em-dashes to 0,
  per the house human-voice standard), with a precise three-driver cost paragraph (anchored by
  the committed 42-agent self-audit run) and a new degraded-run contract section; the README
  positioning sentence de-garbled, the engine paragraph deduplicated and glossed for readers
  new to Claude Code, the install block split into bash and PowerShell; Desk Review's chair
  substitutions made explicit (`sentences_total: 0` means not run, never full coverage);
  prompts 03/04/05/06/07/12/13/14/16 aligned with the schemas and engines that execute them,
  including the locked rubric's `desk-reject-risk` hyphen (a deliberate maintainer alignment
  to the schema enum); the coverage rubric gained the missing cross-field-significance
  dimension (the third generalist seat had no dimension to certify); `stopping_rule.md` joined
  the reading order and orchestration now owns the deepening loop for the heavy tiers.
- **Process notes, disclosed:** the self-run was lighter than the design (a usage-limit
  restart; six of eleven seats salvaged from journals; integrator lenses folded into the
  chair). One external suggestion (hard-gating the advisory verification angles in Act II) was
  considered and declined per the panel's steelman: the docs deliberately mark those angles
  mixed, and auto-applied edits remain tracked changes awaiting the author. Roadmap item 1
  (the measured recall/false-positive validation run) remains the most important open work.

## v0.4.0 — 2026-06-10
Mythos-class (Claude Fable 5) support pass. Researched against primary sources and decided through
three adversarial subagent debates (fact verification, design, pre-push stress test). No workflow
code changed; the fleet's path to Fable is the session-model inheritance the skill already has.

- **README:** a "Running on Claude Fable 5 (mythos-class)" passage. Mechanism (the fleet inherits
  the session model, so `/model best` lifts every seat, verifier, and chair to the strongest model
  the plan has, mythos-class where Fable is available, with no configuration) plus the citable
  design endorsement: Anthropic's Fable 5 prompting guidance states
  that separate, fresh-context verifier subagents tend to outperform self-critique, which is the
  skill's verification-panel architecture. Cited as an endorsement, not a measured improvement. The
  same passage carries the honest constraints: classifier fallback, data retention, 2x pricing.
- **doctor.md:** session-model preflight (`/model best`), domain routing (biology- and
  security-flavored papers should start on Opus 4.8 deliberately, since Fable's classifiers reroute
  benign life-science content, sometimes from workspace context alone), and a model-disclosure rule:
  record the session model in `meta.json` at kickoff, re-check at the end, and carry both in the
  report header, because a flagged Fable session silently migrates to Opus 4.8 and stays there.
- **safety_notes.md:** Fable 5 is a Covered Model (30-day input retention, used for safety defense
  only, not training; zero-data-retention not available). Confidential manuscripts that require ZDR
  should run on a non-Covered model.
- **Runner prompt + sandbox notes:** added Anthropic's tested anti-fabrication instruction verbatim
  ("Before reporting progress, audit each claim against a tool result from this session...") as a
  complement to the deterministic provenance gate.
- **SKILL.md:** engine attribution fixed ("Claude Code's dynamic Workflow engine", not a
  model-named engine) and one sentence on mythos-class inheritance.
- **Deliberate non-changes, recorded for the record:** (1) per-agent model casting and cross-tier
  verification were considered and deferred: the principal Fable benefit already flows through
  session-level `/model` with zero code, the per-agent model override is observed in the harness but
  not documented public API, and a cross-tier decorrelation benefit is unmeasured. (2) Anthropic's
  guidance that prior-model skills can be "too prescriptive" for Fable 5 was reviewed against this
  skill: the prescriptions were retained because they are integrity rails and machine-parsed
  contracts (quote-gate inputs, finding/verdict schemas, provenance tokens), not style scaffolding.
  An audit confirmed the prompts contain no reasoning-echo phrasing (the `reasoning_extraction`
  refusal hazard).

## v0.3.4 — 2026-06-08
- **Stronger opening hook:** "Imagine a panel of the world's leading experts, assembled for your
  exact paper, arguing it out from rival schools and then rebuilding it themselves, re-running your
  own code so the numbers are real." (also the launch line). Dropped the "Every paper leaves changed."
  tagline and de-em-dashed the value sentence.

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
