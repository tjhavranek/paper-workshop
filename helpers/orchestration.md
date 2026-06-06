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
author's originals in place. Write `meta.json` (session id, timestamp, input hashes,
tier, register supportive|brutal, codex/external availability).

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
**Engine choice.** Prefer the **Workflow** engine if the Workflow tool is available
(default on Max; on Pro, enable it in `/config`). If it is not available, run the **same
phases via the Agent tool** (Step 4b) — subagents work on every plan, so the workshop
always runs. **Desk Review** uses neither a fleet nor workflows (Step 4c).

**4a — Workflow engine.** Launch `workflow/phase1_tribunal.js` with `args` = `{ pdf_path,
tier, register, paths: { session, prompts_dir, helpers_dir, rules, rubric,
coverage_rubric, quote_gate, brief, staged_sources } }` — pass `tier` as the internal key
for the chosen mode. (The script parses `args` defensively whether it arrives as an object
or a JSON string.) It runs the eight phases (A ingest/cartography → B scout/roster → C
ground sources → D blind specialists → E cross-critique → **F verification panel** (batched
by angle) → completeness audit → fresh-chair synthesis). The default run is a single pass
that **reports** coverage gaps; deepening (re-fanning the `reopen` list) is orchestrator-driven
per `helpers/stopping_rule.md`, not baked into the script. It writes every artifact to the
session and returns the `synthesis.schema.json` object.

**4b — Subagent fallback (no Workflow).** Drive the same phases yourself with the Agent
tool: cartography → Scout (`00`) → fan out the seats (`01`/`02`/`03`) as parallel Agent
calls in one message → batch the verification panel (`05`) by angle → integrate (`04`) →
synthesize (`06`) → completeness (`07`). Same prompts, same schemas, same artifacts —
slower, identical in substance.

**4c — Desk Review (lightest).** Skip the fleet. The orchestrator (optionally with 2–3
sequential subagents) reads the paper, applies a handful of expert lenses + the three
generalist checks, runs the deterministic quote-gate, and produces a prioritized, grounded
findings list (and, if asked, an Act-II redline). No Workflow, minimal subagents. **See
`helpers/desk_review_mode.md` for the exact passes and which prompts to call** (it reuses
`01_specialist_seat.md`, `02_generalist_seat.md`, `06_chair_synthesis.md`, and the
quote-gate).

- On **Workshop and larger** runs, pause after Phase B and surface the `roster_contract`
  for the author to approve before the fleet runs.
- The deterministic quote-gate (`helpers/quote_gate.py`) is run by the `quote-locator`
  verifier via Bash at the barrier exiting Phase D and in the panel; absence-silence
  findings are exempt.

## Step 5 — Assemble and present the Act-I report
From the returned synthesis, render the human-facing **report bundle**: verdict;
validity verdict (dominates venue); the prioritized must-fix list (capped ~5–7,
sorted by magnitude); the per-seat referee reports; the debate transcript; the
generalists' importance/understandability memo; the verbatim kill-shots and minority
report; the venue read (3-bucket, no number); the **coverage certificate**; and the
rejected-suggestions list. Save it as `report.md` and show the highlights.

## Step 6 — The GATE
Stop. Offer Act II explicitly:

> "I can now *implement* these findings — revise your manuscript with tracked
> changes, re-run the affected analyses against your data, regenerate figures/tables,
> and assemble a reproducing replication package. This needs your source files and
> is gated on your sign-off for anything that touches a number, sample, claim, or
> result. Proceed? (full / only the writing edits / let me pick which findings / not
> now)"

Never auto-start Act II.

## Step 7 — Run ACT II via the Workflow tool (only on opt-in)
1. **Intake** (`prompts/phase2/10_intake.md`): request source/data/code/.bib/figure
   sources/venue style/env, each with its reason; copy what's provided into
   `phase2/input/`; compute and show back the **achievable scope**.
2. **Baseline-reproduction gate** (`helpers/phase2_sandbox.md`): run the author's
   master script unchanged; diff current headline numbers. Mismatch ⇒ stop and report
   (a broken baseline is the first finding).
3. Launch `workflow/phase2_atelier.js` with `args` = `{ session_path, ledger,
   inputs, signoff_policy }`. It triages each finding into lanes A/B/C/D, drafts
   edits (`edit_spec.schema.json`), runs the Runner/Scribe split under the
   Execution-Provenance Wall, rebuilds, regenerates artifacts, runs the **Act-II
   verification panel**, and assembles the replication package.
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
