# Orchestration — how to actually run a workshop

The orchestrating Claude does only four things: **scope, launch, gate, assemble.**
All heavy reasoning lives in fresh subagents that read the shared on-disk brief.
This file is the operational checklist.

## Step 0 — Pre-flight (`helpers/doctor.md`)
Confirm the input is readable. For Act II, also confirm interpreters (R/Python/Stata
as relevant), a sandbox, and `latexmk`/the `docx` skill are available. If anything is
missing, say so and offer the degraded scope rather than failing silently.

## Step 1 — Create the session
Make `<cwd>/paper_workshop_sessions/<YYYYMMDD-HHMM-slug>/` with `input/`,
`brief.md`, `round_artifacts/`, `verification/`, and (Act II) `phase2/`. **Copy**
the PDF (and later the source/data/code) into `input/` — never read or mutate the
author's originals in place. Write `meta.json` (session id, timestamp, session model, input
hashes, tier, register supportive|brutal, codex/external availability).

## Step 2 — Choose the mode and register
Modes (depth) and their internal tier keys: **Desk Review** (no fleet/workflow — Step
4c), **Roundtable** = `quick`, **Workshop** = `thorough` (default), **Symposium** =
`exhaustive`, **Summit** = `monumental`. The user may name a mode, give a tier key, or
just say "lighter"/"deeper". Register is `supportive` (default) or `brutal` — it changes
the chair's delivery only; severity is tone-invariant (grounding rule 4). Record the
mode→tier and register in `meta.json` and the brief.

## Step 3 — Write the brief
`brief.md` is read by every subagent and contains: the mission, the absolute path to
the copied PDF and any staged sources, the tier, the register, and a pointer to
`prompts/shared_grounding_rules.md`, `rubric.md`, and `coverage_rubric.md`. Keep the
heavy rules in those files; the brief just points to them and states the run's
specifics.

## Step 4 — Run ACT I (pick the engine first)
**Engine choice.** Strongly prefer the **Workflow** engine: it runs the same phases far more
efficiently, spawns its own agents, and is how the tool reaches full scale (default on Max; on
Pro, enable it in `/config`). If the Workflow tool is off, say so and **recommend enabling it**
(especially for Symposium/Summit) before falling back to the **same phases via the Agent tool**
(Step 4b); the fallback works on every plan. Both engines' agents inherit the orchestrating
session's model and context by default (no per-agent model is set unless the user opted into
the economy register or a custom `models` map; see `helpers/doctor.md`), so the 1M-context
credit caveat is engine-independent. **Desk Review** uses neither a fleet nor
workflows (Step 4c).

**4a — Workflow engine.** Launch `workflow/phase1_tribunal.js` with `args` = `{ pdf_path,
tier, register, paths: { session, prompts_dir, helpers_dir, rules, rubric,
coverage_rubric, quote_gate, absence_gate, brief, staged_sources } }` — pass `tier` as the
internal key for the chosen mode, and `absence_gate` as the path to
`helpers/absence_gate.py` (omit it and every absence-class finding fails closed to
`needs-author-confirmation`). (The script parses `args` defensively whether it arrives as
an object or a JSON string.) Optional knobs: `economy: true` (the disclosed economy
register; a harness token budget auto-enables it; `economy: false` opts out under a
budget), `session_model` (the session model recorded at kickoff — REQUIRED whenever
economy or `models` is on: it arms the engine's never-upgrade clamp), `span_diet: true`
(experimental, economy-only; see
`helpers/verification_panel.md`), `batch` (verification batch size, clamped to 30),
`max_seat_findings` / `max_generalist_findings` (cap-note overrides), `models` (a raw
role→model map; custom casts are unvalidated and the run is labeled `custom`), and
`improvement: true` (opt-in Improvement Mode: casts mode-scaled generative
`S-improvement-architect` seat(s) and a separate non-blocking, mode-scaled `improvement_memo` of
bolder substantive suggestions; default off and byte-identical when off, so it moves no default-on
rail; set it when the author says "improvement" / "be bolder" / "improve it aggressively"; see
SKILL.md). On a Fable
session, do not launch Workshop-or-larger until `meta.json` records the economy offer and
the user's answer (`economy_offered`; see `helpers/doctor.md`). The run
result includes `casting` and `budget_actions`: persist both into `meta.json`, and
whenever `casting.mode` is not `inherit`, state the role-class cast in one report-header
sentence (grounding rule 15). It runs the nine phases (A ingest/cartography → B
scout/roster, with the contribution rival pair enforced in the floor → C ground sources,
cited works plus the related-literature scout (fetch-or-drop, anti-popularity) → D blind
specialists → deterministic quote-gate + absence-gate → E cross-critique →
**F verification panel** (batched by angle) → G completeness audit → H fresh-chair
synthesis, with the non-blocking `contribution_memo` code-capped at 3). The default run is a single pass
that **reports** coverage gaps; deepening (re-fanning the `reopen` list) is orchestrator-driven
per `helpers/stopping_rule.md`, not baked into the script. It writes every artifact to the
session and returns the `synthesis.schema.json` object.

**4b — Subagent fallback (no Workflow).** Drive the same phases yourself, in the same
order the Workflow runs them, with the Agent tool: cartography (also write the report-only
`injection_scan.md` as the Workflow path does) → Scout (`00`, contribution
rival pair always in the floor) → ground the load-bearing cited sources + the
related-literature scout → fan out the seats (`01`/`02`/`03`) as parallel Agent
calls in one message → run the deterministic quote-gate AND absence-gate (attach each
absence-gate result row to its finding as `absence_gate` before the panel or chair sees
it — the panel's quote-locator and steelman angles read that field) → integrate
(`04`) → batch the verification panel (`05`) by angle → completeness (`07`) → synthesize
(`06`, feeding verified `contribution-undersell` findings ONLY through
`CONTRIBUTION_JSON`, and capping `contribution_memo` at 3 yourself — in the fallback YOU
are the enforcement layer). Same prompts, same schemas, same artifacts — slower,
identical in substance. The economy register carries over: the Agent tool documents the
same per-agent `model` option, so apply the identical role→model map when spawning
(judgment roles at the Opus floor, mechanical roles on Sonnet, scout/chair inherited),
record the identical `casting` object in `meta.json`, and where a role cannot be pinned
let it inherit and log it under `degraded_casting` — the disclosure contract is
engine-independent.

**4c — Desk Review (lightest).** Skip the fleet. The orchestrator (optionally with 2–3
sequential subagents) reads the paper, applies a handful of expert lenses + the three
generalist checks, runs the deterministic quote-gate, and produces a prioritized, grounded
findings list (and, if asked, an Act-II redline). No Workflow, minimal subagents. **See
`helpers/desk_review_mode.md` for the exact passes and which prompts to call** (it reuses
`01_specialist_seat.md`, `02_generalist_seat.md`, `06_chair_synthesis.md`, and the
quote-gate).

- On **Workshop and larger** runs, pause after Phase B and surface the `roster_contract`
  for the author to approve before the fleet runs. Operationally: run the cartography
  step first (as in 4b), call the Scout (`00`) on its outputs, show the returned
  contract to the author, then launch `phase1_tribunal.js` with the approved contract
  as `args.roster` (and the cartography paths in `args.paths`) — the script skips its
  own Roster phase when `roster` is supplied.
- The deterministic quote-gate (`helpers/quote_gate.py`) is run by the `quote-locator`
  verifier via Bash at the barrier exiting Phase D and in the panel; absence-class
  findings (`absence-silence`, `contribution-undersell`) are quote-exempt but ride the
  deterministic absence-gate (`helpers/absence_gate.py`) at the same barrier instead.
- **Deepening loop (Symposium and Summit).** After the workflow returns, apply
  `helpers/stopping_rule.md` before assembling the report: run at least the tier's
  minimum rounds (exhaustive 2, monumental 3) by re-fanning targeted seats at the
  returned `reopen` list and any unresolved High finding; pass the approved `roster`
  and the pre-staged cartography paths so re-entry runs skip recomputation; stop when
  both dry conditions hold or the budget cap is hit, and log the yield curve plus
  anything left open.

## Step 5 — Assemble and present the Act-I report
From the result (the synthesis plus `findings` — each carrying its
`panel_verdicts` — `integration`, and `rejected_in_panel`), render the human-facing
**report bundle**. On a large run the full return can exceed the notification channel:
prefer the chair-written artifact files named in the result's `artifact_paths`
(`round_artifacts/findings_ledger.json`, `round_artifacts/synthesis_raw.json` — verify
they exist and parse before relying on them; they are best-effort copies and the returned
object stays the source of truth), and fall back to the harness's task output file for
the complete return rather than pasting the blob into context. Then render: verdict; validity verdict (dominates venue); the prioritized
must-fix list (capped ~5–7, sorted by magnitude), marking any item whose finding is
`needs-author-confirmation` as not-yet-panel-cleared (the chair flags these in `panel_summary`, so
a comment whose checks did not fully resolve reads as "needs your confirmation", not as a settled
must-fix); the per-seat findings grouped by
seat; the cross-critique consolidation (clusters and crux notes — where rival seats
collided and what evidence would move each side); the generalists' relevance and
understandability findings; the **Contribution Memo** (its own clearly-labeled
section: at most 3 verified, non-blocking ways the paper undersells its own results,
each with the bolder claim, its quoted foothold, and the risk of overreach — labeled
"suggestions, author's call", never mixed into the must-fix list); the **Improvement Memo**
(opt-in improvement mode only: its own clearly-labeled section of non-blocking, mode-scaled bolder
substantive suggestions — additional analyses worth running, sharper framing, bolder defensible
claims — each grounded in a quoted foothold, labeled "suggestions, author's call", never mixed into
the must-fix list; empty/omitted when improvement mode is off); the verbatim
kill-shots and minority report; the venue read (3-bucket, no number); the **coverage
certificate**, rendered with the one-line caveat "Coverage means reviewed, not proven
correct: a flaw can hide in a covered span"; and the rejected-suggestions list. If
`cartography/injection_scan.md` flags any AI-addressed imperative in the manuscript, note
it in the report header as a report-only input-safety flag (grounding rule 11). Likewise, if
`cartography/missing_supplement_scan.md` lists any supplementary material this review was not
given, note it in the report header as a report-only scope-disclosure flag and set
`supplement_cited_not_provided` in `meta.json` (grounding rule 15). This flag is DISCLOSURE
ONLY: it records that the review did not see cited supplementary material so the author reads
the report with that scope in mind. It NEVER licenses deferring or downgrading a finding whose
evidence is in the main text — a real main-text finding is delivered in full regardless of any
un-provided supplement. The report header carries the run's mode,
the serving model (kickoff and end), and, whenever `casting.mode` is not `inherit`, one
sentence stating the role-class cast (for example: "seats and verifiers ran at the Opus
floor, mechanical phases on Sonnet, scout and chair at the session model — the disclosed
economy register"). Save the bundle as `report.md`, persist the per-finding panel verdicts under
`verification/` (the auditable record), and show the highlights.

## Step 6 — The GATE
Stop. Offer Act II explicitly:

> "I can now *implement* these findings — revise your manuscript with tracked
> changes, re-run the affected analyses against your data, regenerate figures/tables,
> and assemble a reproducing replication package. This needs your source files and
> is gated on your sign-off for anything that touches a number, sample, claim, or
> result. **Status, so you opt in with eyes open:** Act II's rails are deterministic and
> unit-tested; it has run end-to-end once on a real accepted paper (one paper, from the
> authors' own group — a demonstration, not independent validation; see
> `examples/incentives-workshop/phase2_true/`), and there are **no
> measured recall/false-positive numbers** yet — treat the output as one very thorough
> opinion and re-derive any regenerated number yourself. Proceed? (full / only the writing
> edits / let me pick which findings / not now)"

Never auto-start Act II.

**Route every Act-II edit through the Atelier; never hand-roll a redline.** Every Act-II edit,
redline, or tracked-changes "improved manuscript" (in every mode and every context, INCLUDING a
referee / PDF-only deliverable with no author source) is produced ONLY by routing the finding
ledger through the Atelier phases (Triage, Scribe, the Act-II verification panel, Package), via
`workflow/phase2_atelier.js` where dynamic workflows are available or the documented subagent
fallback running those same phase prompts otherwise. The orchestrator MUST NOT hand-roll tracked
changes or assemble a redline with its own Bash/Edit or scripting tools outside that pipeline
(e.g. a find/replace script): that bypasses the quote-grounding, the anti-over-concession +
caveat-placement guards, and the human-voice / fix-safety / integrity panel that make an edit
safe (grounding rules 7, 8, 12). A degraded run (no source, or no code/data) NARROWS scope; it
never drops the panel. With no editable source tree but the manuscript TEXT available, pass it as
`inputs.manuscript_text` so the Atelier still produces the writing-lane redline through the guards.

## Step 7 — Run ACT II via the Workflow tool (only on opt-in)
1. **Intake** (`prompts/phase2/10_intake.md`): request source/data/code/.bib/figure
   sources/venue style/env, each with its reason (or, in a referee / PDF-only context, the
   manuscript `manuscript_text` so the writing-lane redline still runs through the Atelier);
   copy what's provided into `phase2/input/`; compute and show back the **achievable scope**.
2. **Baseline-reproduction gate** (`helpers/phase2_sandbox.md`): run the author's
   master script unchanged; diff current headline numbers. Mismatch ⇒ stop and report
   (a broken baseline is the first finding).
3. Launch `workflow/phase2_atelier.js` with `args` = `{ ledger, inputs, paths: { session,
   prompts_dir, helpers_dir, rules, rubric, quote_gate, style_gate, sandbox_notes,
   staged_sources, ledger_path } }` — `helpers_dir`
   lets the Runner / reconciler / package agents call the deterministic checkers
   (`provenance.py`, `consistency.py`, `reproduces.py`, `integrity_diff.py`); `style_gate`
   (optional; falls back to `<helpers_dir>/style_gate.py`) is the deterministic author-voice
   counter the `human-voice` angle and the package/disclosure writers run;
   `staged_sources` feeds the Act-II panel's factual-literature/steelman angles the same
   staged cited-sources tree Act I used (omit it and those checks degrade to cant-tell);
   `ledger_path` is optional (falls back to the inlined `ledger`). The same
   optional knobs apply: `economy: true` (runner/triage/reconciler/package/panel at the
   Opus floor, intake/staging/disclosure on Sonnet, scribes ALWAYS at the session model),
   `session_model` (arms the never-upgrade clamp, as in Act I), `models`, `scribe_batch`
   (default 5), `verify_batch` (default 12, clamped to 30), and `improvement: true` with `tier`
   (opt-in Improvement Mode: the Triage agent ALSO drafts the ledger's `improvement-proposal`
   findings as bold author-rejectable tracked changes, more at heavier tiers — every one
   proposal-only + `author_signoff_required`, riding the same gates and the Execution-Provenance
   Wall; pass it whenever Act I ran in improvement mode AND include the Act-I `improvement_findings`
   in `ledger` so they are available to triage); the
   result's `casting` object is persisted and disclosed exactly as in Act I. It triages each
   finding into lanes A/B/C/D, drafts edits (`edit_spec.schema.json`), **stages a git working
   copy on branch `paper-workshop/phase2`** (the author's original is never touched), runs the
   Runner/Scribe split under the Execution-Provenance Wall, rebuilds, regenerates artifacts,
   runs the **Act-II verification panel**, reconciles every number deterministically, and
   assembles the replication package (its return surfaces the redline / clean-version /
   changes-map / MAP paths).
4. **Author sign-off:** the script returns the auto-applied tracked changes plus the
   queue of numeric/result-suppressing/claim-altering edits and lane-C/D proposals
   awaiting per-item approval. Walk the author through them.

## Step 8 — Final assembly and labeling
Produce (the names prompt 15 and the engine's return object actually use): the revised
manuscript `revised_clean.(tex|docx)` (+ compiled `revised_clean.pdf`), the auditable
redline (`revised_redline.pdf` via latexdiff, or `revised_tracked.docx` for Word), the
`changes_map.md` (every change → edit_id → finding_id → the reviewer concern it answers),
`MAP.md` (every headline number → script+line+run_id+output_hash), the verification
report, the replication package, and the
auto-generated **AI-involvement disclosure**. State plainly what was and was not done
(missing inputs, unreproduced baseline, skipped external leg). The terminal state is
"here is a reviewable branch + tracked changes + a reproducing package — accept what
you want." Never merge, submit, or release data.

## Degradation policy
If a phase's subagent fails, retry once, then record the gap in `meta.json` and the
report rather than fabricating a result. If Act II inputs are missing, narrow scope
and say so — never invent a number, a citation, or a reproduction that did not happen.

**Resume is the best cost containment in practice.** After any fail-closed halt (a
baseline gate failure, a blocking-gap return, a usage-limit interruption), relaunch the
SAME workflow script with `resumeFromRunId`: every completed agent call with unchanged
inputs replays from cache, so a halted Act II retry costs a fraction of a fresh run
(field-measured: 0.1–0.2M tokens per baseline retry instead of a full re-run). Pass the
pre-staged cartography paths and the approved roster on Act I re-entry for the same
reason. If no journal is available, the agent transcripts under the session's workflow
directory still hold every StructuredOutput payload for manual salvage.
