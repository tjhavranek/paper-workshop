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
session's model and context (the skill sets no per-agent model), so the 1M-context credit caveat
is engine-independent (see `helpers/doctor.md`). **Desk Review** uses neither a fleet nor
workflows (Step 4c).

**4a — Workflow engine.** Launch `workflow/phase1_tribunal.js` with `args` = `{ pdf_path,
tier, register, paths: { session, prompts_dir, helpers_dir, rules, rubric,
coverage_rubric, quote_gate, brief, staged_sources } }` — pass `tier` as the internal key
for the chosen mode. (The script parses `args` defensively whether it arrives as an object
or a JSON string.) It runs the nine phases (A ingest/cartography → B scout/roster → C
ground sources → D blind specialists → deterministic quote-gate → E cross-critique →
**F verification panel** (batched by angle) → G completeness audit → H fresh-chair
synthesis). The default run is a single pass
that **reports** coverage gaps; deepening (re-fanning the `reopen` list) is orchestrator-driven
per `helpers/stopping_rule.md`, not baked into the script. It writes every artifact to the
session and returns the `synthesis.schema.json` object.

**4b — Subagent fallback (no Workflow).** Drive the same phases yourself, in the same
order the Workflow runs them, with the Agent tool: cartography → Scout (`00`) → ground
the load-bearing cited sources → fan out the seats (`01`/`02`/`03`) as parallel Agent
calls in one message → run the deterministic quote-gate → integrate (`04`) → batch the
verification panel (`05`) by angle → completeness (`07`) → synthesize (`06`). Same
prompts, same schemas, same artifacts — slower, identical in substance.

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
  verifier via Bash at the barrier exiting Phase D and in the panel; absence-silence
  findings are exempt.
- **Deepening loop (Symposium and Summit).** After the workflow returns, apply
  `helpers/stopping_rule.md` before assembling the report: run at least the tier's
  minimum rounds (exhaustive 2, monumental 3) by re-fanning targeted seats at the
  returned `reopen` list and any unresolved High finding; pass the approved `roster`
  and the pre-staged cartography paths so re-entry runs skip recomputation; stop when
  both dry conditions hold or the budget cap is hit, and log the yield curve plus
  anything left open.

## Step 5 — Assemble and present the Act-I report
From the returned result object (the synthesis plus `findings` — each carrying its
`panel_verdicts` — `integration`, and `rejected_in_panel`), render the human-facing
**report bundle**: verdict; validity verdict (dominates venue); the prioritized
must-fix list (capped ~5–7, sorted by magnitude); the per-seat findings grouped by
seat; the cross-critique consolidation (clusters and crux notes — where rival seats
collided and what evidence would move each side); the generalists' relevance and
understandability findings; the verbatim kill-shots and minority report; the venue
read (3-bucket, no number); the **coverage certificate**; and the rejected-suggestions
list. Save the bundle as `report.md`, persist the per-finding panel verdicts under
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

## Step 7 — Run ACT II via the Workflow tool (only on opt-in)
1. **Intake** (`prompts/phase2/10_intake.md`): request source/data/code/.bib/figure
   sources/venue style/env, each with its reason; copy what's provided into
   `phase2/input/`; compute and show back the **achievable scope**.
2. **Baseline-reproduction gate** (`helpers/phase2_sandbox.md`): run the author's
   master script unchanged; diff current headline numbers. Mismatch ⇒ stop and report
   (a broken baseline is the first finding).
3. Launch `workflow/phase2_atelier.js` with `args` = `{ ledger, inputs, paths: { session,
   prompts_dir, helpers_dir, rules, rubric, quote_gate, sandbox_notes } }` — `helpers_dir`
   lets the Runner / reconciler / package agents call the deterministic checkers
   (`provenance.py`, `consistency.py`, `reproduces.py`, `integrity_diff.py`). It triages each
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
Produce: the revised manuscript (`revised_minimal` + `revised_optimal`, tracked), the
`changes.pdf`, the verification report, the replication package, and the
auto-generated **AI-involvement disclosure**. State plainly what was and was not done
(missing inputs, unreproduced baseline, skipped external leg). The terminal state is
"here is a reviewable branch + tracked changes + a reproducing package — accept what
you want." Never merge, submit, or release data.

## Degradation policy
If a phase's subagent fails, retry once, then record the gap in `meta.json` and the
report rather than fabricating a result. If Act II inputs are missing, narrow scope
and say so — never invent a number, a citation, or a reproduction that did not happen.
