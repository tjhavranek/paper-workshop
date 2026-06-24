# Changelog

## v0.8.2 — 2026-06-19

Archival release: the first release captured by the Zenodo GitHub integration, so the project now
has a citable DOI. No code, prompt, schema, or behavior change from v0.8.1.

## v0.8.1 — 2026-06-19

Post-release housekeeping for v0.8.0 Improvement Mode, from an independent multi-agent stress test
(6 review lanes, each finding adversarially refuted, then synthesis) that confirmed 0 blocking
issues and all five owner invariants holding in code. Four non-blocking follow-ups; a normal
(improvement-off) run is unchanged in behavior:

- **Chair ledger copy now carries `improvement_findings`.** The pre-chair resilience write already
  included it, but the chair's own overwrite template had dropped it, so a successful chair run lost
  it from the on-disk `findings_ledger.json` (the return blob, the documented source of truth,
  always carried it). The template now matches.
- **The low-budget cap checkpoint now tightens the improvement cap too**, so the budget throttle
  reaches the opt-in improvement wing (no-op when off; `IMPROVE_CAP` is already 0).
- **Wording precision.** Off-mode is now described as "rail- and decision-identical", not literally
  "byte-identical" (an off run emits a few additive empty placeholder keys); the `quote_gate.py`
  docstring now names `improvement-proposal` alongside `contribution-undersell` as dual-gated.
- **Considered and dropped:** a code-level sign-off floor on improvement edits. Improvement edits
  are meant to be applied as tracked changes the author accepts or rejects, so forcing more sign-off
  gates would run counter to the design; the proposal-only routing is already triage-instructed with
  the deterministic number and integrity floors binding.

All rituals green: 7 helper selftests + 5 schema checks + JS syntax on both engines + both
provenance proofs; SKILL.md at 0 em-dashes.

## v0.8.0 — 2026-06-19

Improvement Mode (opt-in): an optional generative wing that proposes substantive strengthenings
alongside the critique, plus two honesty-precision doc fixes. From owner field experience that the
suggested edits were too few and limited, and the wish for a bolder, more substantively helpful
tool whose proposals the author can accept or reject in track changes.

The whole wing is OPT-IN and default OFF. With `improvement` off, every run is rail- and
decision-identical to v0.7.6 (every off-path branch is a no-op; the only deltas are additive empty
placeholder keys): no seat is cast, no `improvement-proposal` finding can exist, the memo is empty,
and the Act-II triage directive is empty. So Improvement Mode moves no default-on rail (no detector,
severity value, locked rubric, default panel-angle set, or default per-run cost changes for a
normal run). It is governed exactly like the economy register and the contribution wing.

Shipped (opt-in feature):
- **A generative wing in Act I.** With `improvement: true`, the engine injects one or more
  `S-improvement-architect` seats (1 at Roundtable/Workshop, 2 at Symposium, 3 at Summit), each on
  a distinct lens (analyses worth running, sharper framing and bolder defensible claims,
  defensible extensions). They PROPOSE, never prosecute, and file a new non-blocking finding type
  `improvement-proposal`.
- **The same rails, a separate non-blocking home.** `improvement-proposal` is an absence-class
  finding: it rides the deterministic quote-gate (a foothold quote) AND the absence-gate (an
  `absence_probe` for the un-made improvement), and the full verification panel, exactly like
  `contribution-undersell`. It is code-routed out of the must-fix list, its status forced to
  `needs-author-confirmation`, into a separate `improvement_memo` capped by mode (3 at Roundtable
  up to 12 at Summit). It never raises a severity, never enters `prioritized_findings`, never moves
  the verdict, all enforced in `phase1_tribunal.js`, not by instruction.
- **Aggressive, author-rejectable Act-II drafting.** With `improvement: true` (and the Act-I
  `improvement_findings` forwarded in the ledger), the Triage agent ALSO drafts the improvement
  proposals as tracked-change edits, more of them at heavier tiers. Every improvement edit is
  PROPOSAL-ONLY with `author_signoff_required: true` (the author accepts or rejects each in track
  changes); a new analysis is lane C, a bolder claim is `claim-altering`, and any number still
  rides the Execution-Provenance Wall and every edit still carries `fix-safety` + `integrity`.
  Nothing auto-applies.
- **Honesty.** Disclosed in `LIMITATIONS.md` as an opt-in, unvalidated generative wing (which
  improvements surface is a same-model judgment with no measured improvement-recall yet), with an
  improvement-recall / false-suggestion validation arm added to the roadmap. Documented in
  `SKILL.md`, `README.md`, `helpers/orchestration.md`, and `helpers/verification_panel.md`.

Also shipped (do-now honesty-precision, no rail):
- **Chair marks what is not fully panel-cleared.** A delivered finding carrying
  `needs-author-confirmation` (its quote or a panel angle did not fully resolve) is now flagged as
  such in its `panel_summary`, so the author can tell a panel-cleared must-fix from one that still
  needs their eye. Label only: it never moves a finding off the must-fix list and never changes a
  severity (`06_chair_synthesis.md`, `helpers/orchestration.md`, `README.md`).
- **Factual-literature tier carve-out surfaced.** `helpers/verification_panel.md` now states at the
  angle table that the dedicated `factual-literature` verifier runs at Symposium/Summit only; at
  the lighter tiers the cited works are still fetched and read by the seats, but that verifier angle
  is not applied to the findings.

All rituals green (7 helper selftests + 5 schema checks + JS syntax on both engines + both
provenance proofs; SKILL.md at 0 em-dashes). New schema fields (`improvement-proposal` finding
type, `improvement_memo` synthesis field) are additive and optional, so v0.7.6 outputs still
validate.

## v0.7.6 — 2026-06-18

Act-II over-concession and caveat-placement guards, from a second author's feedback in a
different domain (oncology / cancer cell biology). On that run the Scribe wrote a
self-defeating caveat the data did not force and foregrounded a limitation in the Abstract;
the author would not have written it that way. Detection itself was sound;
the problem was how the Scribe wrote and placed a caveat, so the corrective signal is about
the edit-writing surface, never about detection or severity. The
fix is the symmetric mirror of a gap the Scribe already guarded on one side: it barred
over-claiming but had no guard against over-conceding and no caveat-placement logic.

These changes are prompt/spec plus one additive Atelier-engine path (below). They touch no
rubric text, add no severity tier, change no must-fix SET, and move no default-on rail (no
detector, severity value, locked rubric, or panel-gate angle).

Shipped (do-now, prompt/spec only):
- **Symmetric anti-over-concession in the Scribe.** An inserted caveat, hedge, or admission
  must be forced by the data and must not concede more than the evidence requires; a
  self-defeating qualifier beyond what the finding establishes is a fix-introduced error
  (grounding rule 7), the mirror of over-claiming. A data-compelled caveat still ships, and a
  genuine missing caveat routes to author decision rather than being suppressed. The test is
  "exceeds what the data force," never "a referee will dislike it."
- **Caveat-placement logic in the Scribe.** A limitation goes in the lowest-prominence place
  that still discharges the finding (a Discussion limitations subsection, or beside the result
  it qualifies), not foregrounded in the Abstract/title/headline where it reads as the author
  disowning their own result. It harmonizes with any existing limitations passage. EXCEPTION:
  a finding that is itself about the Abstract/title is fixed in place; otherwise a placement
  conflict returns `blocked: needs-author-signoff` with the suggested location.
- **Triage mirror.** The banned "more likely to be accepted" justification now also bars
  "more-defensible-looking": an edit whose effect is to add or strengthen a caveat the data do
  not force is referee-management, not auto-applicable; a missing caveat that a careful reading
  requires (rubric Medium) routes to author decision. The `integrity` reverify angle now fires
  for caveat-ADDING edits too, not only caveat-weakening ones.
- **`edit_intent` + `proportionality_note` spec field** (`defect-fix` / `proportional-caveat`
  / `presentation`). Annotation and routing only: it tags an edit toward author sign-off and
  must never auto-downgrade, veto, or change a finding's severity or existence. The on-disk
  `edit_spec.schema.json` documents the contract that a `proportional-caveat` edit carries a
  non-empty `proportionality_note` citing the data, and the triage prompt requires it; the
  field is read by no path that sets severity (the engine's gating never consults it).
- **Chair concession-placement clause** (a one-clause extension of the v0.7.5 defect-vs-
  discretionary rule, not a new tier). A discretionary improvement framed as a concession is
  the author's strategic call: it goes to should/nice presented as the trade-off it is, never
  as the tool's recommended default. Placement only; changes no severity and no must-fix set,
  and tone-invariance (grounding rule 4) still holds.

Binding the guards to the path (a brutal multi-agent stress-test's central finding). The five
guards were correct but sat on a path the original failure never traveled: that redline had been
hand-rolled by the orchestrator OUTSIDE the Atelier, so none of the in-Atelier guards would have
run on it. Three fixes close that, none a rail:
- **Routing rule.** `orchestration.md`, `SKILL.md`, `desk_review_mode.md`, and grounding rule 12
  now bind every Act-II redline or tracked-changes "improved manuscript" (in every mode and
  context, including a referee / PDF-only deliverable with no author source) to the Atelier
  pipeline: Triage, Scribe, the verification panel, Package. The orchestrator may not hand-roll a
  redline with its own tools.
- **No-source manuscript-text path (engine).** `phase2_atelier.js` gains an additive Stage branch:
  with no editable source tree but a manuscript TEXT substrate (passed as `inputs.manuscript_text`),
  it stages a single-file working copy and runs the writing-lane redline THROUGH the Scribe + panel
  + Package, so the referee deliverable the routing rule now requires actually has a guarded route.
  The with-source path is unchanged; numeric findings still degrade to author-decision.
- **Runtime coherence + fail-safe.** The engine validates Triage output against an inline schema,
  so `edit_intent`/`proportionality_note` were added there too (not only to the on-disk schema),
  letting the field flow at runtime (the on-disk schema's `proportional-caveat`-requires-a-note
  conditional is the documented contract; the prompt instructs it). And Triage now attaches the
  `integrity` reverify angle BY DEFAULT to any caveat-adding edit, so a misclassified caveat-add
  cannot skip that angle; the Scribe's anti-over-concession and placement clauses plus `fix-safety`
  remain the primary over-concession guards (sharpening the integrity question itself is staged).
  The no-source manuscript-text path also fails closed if no working copy is staged (it will not
  edit the author's original in place), and the package step produces the referee redline over the
  text substrate rather than assuming a LaTeX/Word source.

Added: `prompts/phase2/over_concession_acceptance_tests.md` — binding regression scenarios so the
guards cannot become a yes-man (a data-compelled headline caveat must survive; a true
Abstract-omission fix stays in the Abstract; `edit_intent` never flips a finding; tone-invariance
holds; the protected detection pattern still ships as must-fix; every redline routes through the
Atelier, never hand-rolled; an author-conceded count inconsistency stays must-fix), plus a Staged
list recording the rail-class items held back (the integrity-question wording, a deterministic
force-integrity floor, and the #22 detector).

Not done, on purpose: a default-on over-concession DETECTOR / new panel-gate angle is a rail,
so it is STAGED, not shipped; it unstages only when a 3rd paper in a 3rd domain shows an
over-concession edit false or indefensible by operator re-check (not merely unstrategic). The
"reviewer-will-raise / strategic register" tier remains REJECTED (it would edit the locked
rubric on an author's negotiation strategy). Also bumped the CITATION.cff version, which had
been stale at 0.7.0 since the 0.7.0 release.

## v0.7.5 — 2026-06-17

Triaged response to one author's feedback on one biology run (Divin et al.; the tool's
detection was right on ~6 of 7 contested items, the author's two strongest rebuttals refuted
on his own tables). Two independent audits of the decision — a paper-workshop Roundtable on a
decision memo, and a mad-research pass (Claude streams + cross-critique + a Codex synthesis
judge on an abstracted packet) — converged, then a two-voice subpanel verified each edit is
safe. The discipline held: only cheap, generalizable fixes that touch no rail and no severity
shipped; the centerpiece ask was rejected; everything rail-touching stays staged under the
project's own >=2-papers-in->=2-domains rule (n=1 here).

Shipped (no rail or severity touched):
- **Resilience: persist the verified ledger before the chair runs.** The synthesis chair is a
  single point of failure; the engine now writes `findings_ledger.json` from the verified set
  before the chair is cast, so a chair death loses only the prose, never the fleet's findings.
- **No figure-render findings from a text substrate.** A "figure does not render/embed/display"
  claim is a binary/rendering property the extracted text cannot show; the seat prompt and
  `pdf_extraction.md` now forbid filing it from the text and downgrade any such observation to
  `needs-author-confirmation`. This closes the run's one genuine false positive.
- **Correction-propagation guard.** A mechanical fail-closed filter restricts the chair's
  `prioritized_findings` to ids actually delivered to the chair, so a rejected or downgraded
  finding cannot reappear in the must-fix list (the stale-claim leak), logged when it fires.
- **Defect-vs-discretionary placement in the chair.** A `must` entry must trace to a verified
  defect; a discretionary suggestion ("add a Limitations paragraph") goes under should/nice as
  the author's call. Placement only, keyed off whether a verified defect backs the item, never
  off how a reviewer might feel — it changes no severity and no must-fix set.
- **Supplement-disclosure banner.** Cartography scans for cited supplementary material not
  provided to the review and the report header discloses it; disclosure only, with an explicit
  rule that it never defers or softens a main-text finding.

Rejected: a "a reviewer will likely raise this; your strategic call" register tier with a
"validity floor." It would edit the locked severity rubric and the chair's severity on the
strength of one author's negotiation strategy, its only trigger was a true overclaim the
rubric already classes High, and the validity floor does not even bind on that overclaim. All
three audits flagged it as the owner's stated yes-man risk; the existing "register governs
delivery only" firewall plus the defect-vs-discretionary placement above cover the safe signal.

Staged (need a 2nd reproducing example in a 2nd domain): extending the deterministic
absence/credit-the-text gate to statistical finding types; a steelman-quote-the-hedge clause
(partly redundant with the existing steelman angle); hold-the-line tags; an unconditioned
supplement-deferral clause; an artifact-guard; an experiment->dataset ontology; a causal
classifier. Record: `workshop/_michal_revision_audit_20260616/`.

## v0.7.4 — 2026-06-16

Fixes from running CRUCIBLE on its own repo (Roundtable, Opus 4.8; 33 agents, 58 verified
findings, verdict major-revision). The audit's must-fix cluster sat on load-bearing trust
claims that were slightly stronger than the code or records support; these close the gap.
Two concrete bugs and five honesty-precision corrections, all verified against the code:

- **Bug (F-013):** the quote-gate log line dereferenced `gate.results` without guarding
  `gate` itself, so a fully-dead gate agent threw and aborted an otherwise cleanly
  fail-closed run after the findings were already correctly handled. Now guarded.
- **Bug / honesty (F-011):** a dead seat on the default Workflow path was dropped by
  `filter(Boolean)` with no record, while the degraded-run contract said "retries once,
  then records the gap." The engine now records `seats_cast` / `seats_delivered` (a dropped
  seat is visible in the log, the return, and meta.json), and SKILL.md's contract is
  corrected to describe the engine's actual behavior (retry is the subagent-fallback path).
- **F-020:** "verified by the deterministic quote_gate.py (not an LLM)" overstated the
  path: the engine does not run the gate, a subagent runs the script and relays its output.
  Restated to "the script, not an LLM, makes the match call, and a dropped or mis-relayed
  row fails closed."
- **F-044:** the "nothing reaches the user until several blind subagents have checked it"
  guarantee was unscoped, but Desk Review runs no panel. Scoped to "Roundtable and above"
  in SKILL.md and README.md, with the Desk Review single-pass carve-out stated where the
  guarantee is.
- **F-021:** the Execution-Provenance Wall confirms the value occurs as a standalone number
  in the hashed artifact; LIMITATIONS now states plainly that binding the number to a named
  cell or row stays LLM-judged, and the input-data hash is checked only when a data file is
  supplied.
- **F-004:** the economy field-run anchor has no committed record in the repo (unlike the
  self-audit and incentives examples); marked author-disclosed-only in SKILL.md and the
  LIMITATIONS process-metrics table.
- **F-001:** the process-metrics table's "Severity (delivered)" column was mislabeled for
  the incentives row (45/58/34 = 137 raw, not 131 delivered). The column basis is not
  uniform across rows; the header is now plain "Severity" and the Notes state each row's
  basis (the panel's fix-safety verdict ruled out recomputing a delivered split, since the
  committed records do not flag which rejected findings fell in which bucket).

Already-disclosed audit points (e.g. that the one end-to-end Act II demo reproduced
byte-identical, so the replace-a-stale-number path is unit-tested not yet exercised) were
confirmed already covered in LIMITATIONS and left as-is. Run record:
`paper_workshop_sessions/selfaudit-roundtable-20260616-1613/`.

## v0.7.3 — 2026-06-16

Multi-pass voice-baseline rule (doc/prompt only, no code), from a field post-mortem. On a
real paper whose author used zero em-dashes, a multi-pass Act II run let em-dashes compound
across passes (10 → 18 → 20) because pass 2's input was pass 1's own already-revised output,
so the author-relative voice check baselined against the tool's own prior prose and the
spike never fired. The deterministic style gate (v0.7.2) closes the single-pass detection
gap but not this one.

- Intake (`prompts/phase2/10_intake.md`) now asks whether the manuscript is the author's own
  writing or a prior paper-workshop revision being re-run, and records the author's last
  hand-written version as `original_manuscript`.
- The scribe standard (`prompts/phase2/12_scribe_implementer.md`) and the `human-voice` angle
  (`prompts/05_verification_panel.md`) state that the voice baseline is always the author's
  pristine original, never a prior tool revision.
- `helpers/style_gate.md` and `helpers/doctor.md` note that the gate is only as clean as its
  baseline, and that the voice check must run on the final polished text, not only the first
  revision's edits.
- Staged, not shipped (awaiting validation across ≥2 papers in ≥2 domains): threading the
  `original_manuscript` path into the engine so the gate baselines against it automatically
  on a detected re-run. The doc rule closes the realistic exposure now.

## v0.7.2 — 2026-06-12

Voice hardening, triaged by a brief subagent debate (3 grounded auditors + a fresh judge)
after the author observed AI-style artifacts surviving an Act II run. The author-voice
standard and the `human-voice` hard gate already covered manuscript edits well (the one
committed true-Act-II example inserted clean economics prose), but voice was the single
Act-II trust rail with no deterministic half, and the AI-authored deliverable and report
prose had no voice instruction at all.

- **New deterministic helper `helpers/style_gate.py` (+ `style_gate.md`).** It does the
  counting the `human-voice` angle used to eyeball: em/en-dash and semicolon rates (Unicode
  AND LaTeX `---`/`--`) measured against the author's baseline, the banned AI lexicon minus
  any word the author already uses, and the staged negation-correction antithesis. It is
  ADVISORY and author-relative, the opposite polarity to the quote gate: a rate spike maps to
  `cant-tell` (routes the edit to author sign-off, never an auto-reject, because a legitimate
  author may use dashes), and only an author-independent banned token or staged antithesis
  exits non-zero. Stdlib-only, reuses `quote_gate.normalize` so the gates cannot drift, with
  its own selftest now in CI.
- **Deliberately conservative, to avoid damaging legitimate prose.** Bare `rather than X, Y`
  (a normal comparative), `not only X but also Y`, and `highlight` as a verb are NOT flagged
  deterministically; they remain the LLM verifier's semantic call. (The committed Edit 3,
  "...an identifying assumption rather than a tested property...", scores `clean`.)
- **The `human-voice` angle now runs the gate** instead of eyeballing the counts (prompt 05
  + the engine's angle text), with the spike-to-`cant-tell` mapping wired through the existing
  sign-off path; `decideEdit()` and the hard-gate set are unchanged.
- **The unguarded AI-authored prose now has a voice rail.** The replication-package writer
  (README, `changes_map.md`, `MAP.md`, `data_dictionary.md`), the disclosure writer, and the
  Act I chair report get a plain-prose instruction pointing at the canonical standard, and the
  package/disclosure writers run the style gate over their own output and rewrite to `clean`
  (these files have no author voice to protect).
- **Additive-edit baseline defined.** When an inserted sentence has no adjacent author prose,
  the baseline is the document-wide author rate (sample paragraphs elsewhere in the file),
  named in the scribe standard and the `human-voice` angle so an additive edit never defaults
  to the model's own voice.

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
