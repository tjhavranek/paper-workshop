---
name: paper-workshop
description: |
  CRUCIBLE: a Claude-only adversarial expert workshop that stress-tests a
  scientific paper and then, opt-in, rebuilds it. ACT I (TRIBUNAL): from the
  paper PDF (plus a few public cited works it fetches), a topic-adapted fleet of expert
  referee subagents (every
  contested claim argued from at least two COMPETING intellectual traditions,
  plus generalist seats for relevance, understandability, and cross-field
  significance) reviews the paper
  to the sentence, every comment grounded in an exact quote (no fabrication, no
  confidence scores) and independently re-checked from many angles before
  delivery. On every run it also flags where the paper UNDERSELLS its own
  results, in a separate non-blocking Contribution Memo (suggestions only). ACT II (ATELIER, opt-in): with the author's source + data + code,
  it implements the agreed changes as a tracked-changes redline plus a clean
  revised version, RE-RUNS the analysis under an execution-provenance wall
  (no number enters the paper unless a logged re-run produced it), and
  assembles a replication package, every change multi-angle-verified, nothing
  applied without the author's sign-off on anything that touches the record.

  Triggers:
   - "workshop this paper" / "workshop my paper <file>" / "run paper-workshop on <file>"
   - "convene the workshop on <file>" / "convene the tribunal on <file>"
   - "CRUCIBLE <file>" / "give me an elite referee workshop on <file>"
   - "workshop and stress-test this manuscript" / "brutally workshop this paper"
   - "red-team and rebuild my paper <file>"
   - Act II: "implement the workshop changes" / "rebuild my paper" /
     "build the replication package" / "do Act II / the atelier"
   - Improvement Mode (opt-in, any depth): "be bolder" / "improve it aggressively" /
     "suggest more improvements" / add the word "improvement" to the trigger

  mad-research and paper-workshop are complementary, not substitutes. Use
  mad-research for a fast, read-only, cross-model (Claude+Codex) audit memo with
  no implementation; use paper-workshop when you want the largest possible
  Claude-only expert fleet AND the option to actually fix the paper and ship its
  replication package. For an important paper you can run both in parallel and
  compare.
---

# paper-workshop (CRUCIBLE)

> *Every paper leaves changed.*

A two-act simulation of the workshop a paper would get if a specialist were
assigned to **every** contested choice, each one argued by **both** rival schools,
a generalist panel asked whether it **matters** and is **intelligible**, every
comment were **independently re-checked from many angles**, and then the best of
the room **rebuilt the paper and its replication package**.

The deeper modes can run for a while by design (you choose the depth). The whole
tool is Claude-only; it uses Claude Code's dynamic **Workflow** engine when available and
plain subagents otherwise, with live work (fetching cited sources, running the
author's code) via the **Agent/Bash** tools.

**Honest limits.** See [`LIMITATIONS.md`](LIMITATIONS.md): effectiveness is not measured yet
(no recall or false-positive numbers); same-model decorrelation is a design bet, not a proof;
and Act II is demonstrated end-to-end once on one accepted paper, not broadly validated.

## The two acts and the gate between them

- **Act I (TRIBUNAL).** Input: **the paper PDF**, no data or code, and it touches none of
  your files (it does fetch a few *public* cited works to check the paper's claims, plus a
  handful of related works the paper does NOT cite, hunted under an anti-popularity
  mandate and staged only if actually fetched). Output: a verified,
  prioritized finding ledger + a referee-report bundle + the cross-critique crux notes
  (where rival seats collided and what evidence would move each side) + the generalists'
  relevance, understandability, and cross-field-significance memo + a non-blocking **Contribution Memo** (at most 3
  verified ways the paper undersells its own results, each grounded in a quoted foothold;
  suggestions only, the author's call) + a completeness certificate. Read-only;
  nothing of the author's is touched. (`workflow/phase1_tribunal.js`)
- **[HARD GATE].** The skill **stops** and offers to implement. It never
  auto-chains into Act II.
- **Act II (ATELIER).** Opt-in. Asks for the manuscript **source** (.tex/.docx),
  **data**, and **code**, then implements every safely-implementable finding as
  tracked changes, re-runs the analysis against the data, regenerates figures and
  tables, and assembles a reproducing **replication package**, all on copies, all
  author-approvable. (`workflow/phase2_atelier.js`) Every Act-II redline is produced through
  this Atelier pipeline (Triage, Scribe, the verification panel, Package), never hand-rolled
  outside it; a referee or PDF-only context passes the manuscript text so the writing-lane
  redline still runs through the same guards.

The two acts share one spine: the **Verified Finding Ledger**
(`schemas/finding.schema.json`). Act I produces it; Act II consumes it.

## The contribution wing (sharper contribution, same rails)

Most review tools only subtract: they find flaws. CRUCIBLE also asks, on every fleet
run, whether the paper UNDERSELLS itself, and it does so without loosening a single
rail (Desk Review folds the same undersell question into its lighter passes):

- **The contribution claim is always a contested choice.** Every roster staffs the
  rival pair `S-contribution-maximizer` (the boldest claim the paper's OWN results
  defensibly support) vs `S-contribution-prosecutor` (where the stated contribution
  outruns the evidence), enforced by the Workflow engine, not just the prompt (the
  engine injects and logs any seat the scout omitted; in the subagent fallback the
  orchestrator applies the same floor by instruction).
- **Undersell findings ride BOTH deterministic gates.** A `contribution-undersell`
  finding must quote the under-leveraged result (its foothold, quote-gated) AND carry
  an absence probe whose terms the absence gate searches deterministically: a clean
  certificate means no refuting phrasing occurs in the text, and the semantic call
  stays with the steelman verifier. No foothold, no finding.
- **The Contribution Memo is non-blocking by construction.** At most 3 verified items,
  delivered in their own clearly-labeled report section; the engine strips any of them
  from the must-fix list and forces their status to needs-author-confirmation in code.
  They are suggestions; the author is the author.
- **The literature lens widens, fetch-or-drop (Workshop depth and above).** A
  related-literature scout hunts works the paper does NOT cite, deliberately preferring
  the idiosyncratic (adjacent fields, pre-2000, working papers, non-US journals), under
  a strict mandate (not a deterministic check; see `LIMITATIONS.md`): a work becomes
  citable evidence only if its text was actually fetched and read in this run.
  Unfetchable candidates are listed as leads for the author, in a file kept outside the
  staged-sources tree so seats and verifiers never see them as evidence.

Honest caveat: which undersell candidates surface, and which memo items rank highest,
remain same-model judgments with no measured undersell-recall yet (see
`LIMITATIONS.md`). The memo is a grounded option set, not a validated verdict on what
your contribution should be.

## Improvement Mode (opt-in: a generative wing that proposes substantive strengthenings)

By default the workshop is conservative and subtractive: it finds defects, with a small capped
Contribution Memo for where you undersell yourself. Say "improvement" (or "be bolder" / "improve it
aggressively"; the orchestrator passes `improvement: true` to the engine) and an opt-in generative
wing turns on:

- **Act I** casts one or more `S-improvement-architect` seats (more at heavier tiers) whose job is
  to PROPOSE, not prosecute: the boldest defensible claims your own results support, additional
  analyses worth running (robustness, placebo, alternative estimator, extension), and sharper
  framing. Their output rides the SAME deterministic gates as every finding (a quoted foothold plus
  an absence probe) and lands in a separate, non-blocking, mode-scaled **Improvement Memo** (cap 3
  at Roundtable up to 12 at Summit). It never enters the must-fix list, never raises a severity,
  never moves the verdict.
- **Act II** (if you opt in) drafts those improvement proposals as extra tracked changes, more of
  them in the heavier modes. Every improvement edit is PROPOSAL-ONLY and waits for your sign-off
  (you accept or reject each one in track changes); a new analysis is a proposal, any number it
  introduces still rides the Execution-Provenance Wall, and every edit still rides fix-safety and
  the integrity angle. Nothing auto-applies.

Off by default, a run is rail- and decision-identical to a normal run, so Improvement Mode moves
no default-on rail. It is a grounded option set, not a validated verdict: like the Contribution Memo, which
improvements surface is a same-model judgment with no measured improvement-recall yet (see
`LIMITATIONS.md`). The author is the author; these are suggestions you ratify or ignore.

## What makes it trustworthy at scale (read `prompts/shared_grounding_rules.md`)

The fleet is the product; the rails below are what keep a 300–600-agent run from
laundering a fatal flaw into a confident green light. They are always on, cost
almost nothing, and are never traded away for scale.

- **Multi-angle independent verification before delivery.** At Roundtable and above,
  *nothing* reaches the
  user until several blind subagents, **each from a different angle**, have checked
  it (logical validity, severity calibration, decision-relevance,
  fix-safety, charitable steelman; factual/literature added at the deeper tiers; Act
  II adds numeric provenance, consistency, integrity). The quote/locator check is not in
  that list because it is not a judgment: it is the deterministic gate that runs at the
  barrier before the panel, and its result is recorded into the panel record by the
  workflow rather than relayed by an agent. Desk Review, the lightest mode, runs
  no panel: its chair applies logical-validity and steelman inline and labels itself a
  single-pass read. See `helpers/verification_panel.md`.
- **Ground, don't recall; never fabricate.** Exact quote + locator on every
  finding, decided by the deterministic `helpers/quote_gate.py` script (a subagent runs it
  and relays the output; the script, not an LLM, makes the match call, and a dropped or
  mis-relayed row fails closed). Unverifiable → `needs-author-confirmation`, never asserted.
- **Even absence claims ride a deterministic gate.** "The paper never says X" findings
  (and their constructive twin, "the paper never CLAIMS what its own results support")
  carry a probe of refuting terms searched by `helpers/absence_gate.py`, fail-closed;
  the steelman verifier adjudicates the semantic half with the gate's hit snippets.
- **No confidence scores. Severity is tone-invariant** (`rubric.md`).
- **Decorrelate by rival objective function**, commit-and-reveal independence,
  un-deletable verbatim dissent, preserved minority report.
- **Act II Execution-Provenance Wall:** no number enters the paper unless a real, logged
  re-run produced it, re-hashed and value-checked by the deterministic `helpers/provenance.py`
  + `helpers/consistency.py` (fail-closed), with `helpers/reproduces.py` deciding "reproduces"
  and `helpers/integrity_diff.py` flagging any net result-removal to author sign-off.

## Modes (pick your depth; runs on any paid plan)

Three things set a run's cost. **Seats:** the mode fixes the expert-seat band (the scout
casts within it), and seats are the dominant driver. **Findings:** each seat returns at
most 8 findings (a standing budget note in the seat prompt; 5 under the economy register
below), and the verification panel is *batched by angle* (panel agents ≈
`angles × ceil(#findings / batch) × redundancy`): three
angles at Roundtable, five at Workshop, six with two agents per angle at
Symposium/Summit, over batches of 20–30 findings, default 25 (see
`helpers/verification_panel.md`). The quote/locator check adds no agent at any tier: the
deterministic gate has already run at the barrier, so the workflow records its result
directly instead of paying an agent to run the same script again.
**Paper length:** it enters only at Symposium and Summit, which add close-reader sweeps
over ~40-sentence blocks; the script bounds the sweep fan-out, and the lighter modes'
cost is set by the tier whatever the paper's length. As one measured anchor, the
committed Roundtable-mode self-audit ran 42 agents end to end
(`examples/self-audit/run_meta.json`, 2026-06-06).

| Mode | What convenes | Expert seats | ≈ agents | Best for |
|---|---|---|---|---|
| **Desk Review** | one expert pass (no fleet) | a few inline lenses | ~1–6 | a fast read; lightest setup |
| **Roundtable** | a small adversarial panel | 6–8 | ~20–30 | a quick but real workshop |
| **Workshop** *(default)* | the full adversarial workshop | 12–18 | ~45–65 | serious pre-submission review |
| **Symposium** | a large fleet + close-readers | 25–40 | ~90–250 | top-venue preparation |
| **Summit** | every subsystem + every sentence | 60–120+ | ~300–600 | the most exhaustive pass (opt-in) |

Symposium/Summit counts grow with paper length (the sentence sweeps); a very long paper can
push Summit past 600. The seat count, the main cost driver, is cast by the scout within
the target bands, so these totals are typical, not hard limits (the script bounds only the
verification and sweep fan-out). Default is **Workshop**. **Symposium and Summit are
best run with the Workflow engine**: the subagent fallback is practical up to Workshop;
beyond that, without workflows the orchestrator should fall back to Workshop depth **and tell
the user**, rather than downgrading silently. (Internal
tier keys: Roundtable=`quick`, Workshop=`thorough`, Symposium=`exhaustive`,
Summit=`monumental`.)

**Engine & plans: the workshop runs for everyone.** Subagents (the Agent tool) work on
**every plan**, so the orchestrator can always run the phases by spawning subagents
directly. When **dynamic workflows** are enabled (default on Max; on Pro, turn them on in
`/config`), the skill uses `workflow/*.js` to orchestrate those same subagent phases more
efficiently (same phases, prompts, schemas); the subagents still do the work. **Desk Review**
needs neither a fleet nor workflows and is the safe choice on the lightest setups. See
`helpers/orchestration.md` for how the orchestrator picks the engine.
Either way, the spawned agents inherit the orchestrating session's model and context by default
(no per-agent model is set unless you opt into the economy register below or supply a
custom role-to-model map), so dynamic
workflows do not bypass the 1M-context credit caveat: a 1M-context session may need usage
credits enabled for that tier, or run the orchestrator on a standard-context model. In the
default mode that inheritance means the session model sets the workshop's capability: a
session on Claude Fable 5 (Anthropic's mythos-class tier) runs every seat, verifier, and
chair at that level. `helpers/doctor.md` covers this pre-flight, the Fable safety-classifier
domain routing, and the model-disclosure rule.

**The economy register (opt-in, always disclosed).** A default all-Fable Workshop can
exhaust a usage-capped plan's window mid-run, and a locked-out run delivers nothing. Say
"economy" (the orchestrator passes `economy: true` to the engine) and the fleet is cast in
two tiers: the judgment layers (specialist seats, generalists, premortem, cross-critique
integrators, the verification panel, and Act II's runner, triage, reconciler, and package)
run at the Opus floor and never below it; the mechanical phases (cartography, source
grounding, gate relays, completeness, Act II intake/staging/disclosure) run on Sonnet; the
scout, the chair, and Act II's scribes always stay at the session model. Under economy,
Low-severity findings are panel-checked on the quick gate set plus severity-calibration
(the calibration angle is the one channel that can flag an under-rated Low for the chair;
the logical-validity
hard gate, fix-safety, and the steelman defense stay on every finding; the locked rubric
means a Low can neither rise nor drive the verdict). Every
deterministic rail (quote gate, absence gate, fail-closed panel aggregation, the
Execution-Provenance Wall) is identical in both modes. The cast is recorded in `meta.json`
and stated in the report header; a mapped model the plan does not serve falls back to
inheritance and is logged, never crashed on, and a never-upgrade clamp (armed by the
`session_model` argument the orchestrator passes) keeps economy from raising any role
above the session model, so asking for economy can lower a run's cost but never lift it.
On a Fable session the pre-flight presents economy as the recommended, pre-selected
choice (the documented lockout case); full power stays one explicit "yes" away. An
experimental span-diet for the verification panel is a separate economy-only opt-in
(`span_diet: true`; see `helpers/verification_panel.md`). Honest status: the economy cast matches one
real field run (Act I: 39 agents in total, its 37-agent tribunal workflow recorded at
3.70M subagent tokens in 55 minutes, delivering a 60-finding verified
ledger), which is evidence it preserves output strength, not blind validation; and unlike the
self-audit and incentives examples, this field run is author-disclosed only, with no committed
record in the repo (see `LIMITATIONS.md`). A user token target (a "+500k"-style budget) auto-enables economy plus
small logged structural adjustments; deeper cuts (a Sonnet panel, Sonnet generalists,
Haiku relays, the panel span-diet, economy as
the default) are named validation arms, not options.

## Reading order for the orchestrating Claude

1. This file.
2. `prompts/shared_grounding_rules.md`: the fifteen non-negotiables (they bind every agent).
3. `helpers/doctor.md`: pre-flight checks (and, for Act II, sandbox/interpreter checks).
4. `helpers/orchestration.md`: the operational checklist (how to actually run both acts).
5. `helpers/verification_panel.md`: how the many-angle verification gate works.
6. `rubric.md`, `coverage_rubric.md`, and `helpers/stopping_rule.md`: the locked severity +
   coverage standards, and when a deepened run is done.
7. The `prompts/` for each phase, and `workflow/phase1_tribunal.js` / `phase2_atelier.js`, as the run proceeds.
8. `helpers/safety_notes.md`: warn the author about anything relevant before sending data anywhere or running code.

## Safety defaults

- Act I is **read-only**. Act II works only on **copies/branches**; the author's
  originals are never mutated, and anything touching a number, sample, claim, or
  result requires explicit author sign-off.
- Code re-runs (Act II) execute in a sandbox, **network-off by default**.
- The only optional non-Claude call is a single **lower-weight external dissent
  leg** ("what did all Claude seats miss?"), which operates on abstracted findings,
  **never raw data**, only with logged consent, and is skipped + disclosed if no
  no-train endpoint is configured.

## The degraded-run contract

A degraded run is labeled, never disguised (grounding rule 15). Whatever breaks, the
deliverable states plainly what was and was not done. Specifically:

- **Missing or unreadable inputs.** The pre-flight doctor (`helpers/doctor.md`) reports
  the problem and offers the narrowed scope before anything runs. Without Python the
  quote-gate cannot run: the doctor stops the run and says so; if the gate fails
  mid-run, the affected findings degrade to `needs-author-confirmation`, never to a
  silent pass.
- **An agent dies mid-run.** On the subagent-fallback path the orchestrator retries once. On
  the Workflow path a dead seat is dropped fail-closed and the gap is recorded as the
  cast-vs-delivered seat count (`seats_cast` / `seats_delivered` in the run output and
  `meta.json`), so a missing seat is visible, never silent. A missing result stays missing;
  nothing is fabricated to fill it.
- **The chair dies.** Act I returns the complete verified record with `synthesis: null` and
  `degraded: chair-returned-null` instead of failing the run, so a single dead agent can no
  longer destroy every seat finding and panel verdict the fleet produced. The verified ledger
  was already written to disk before the chair was cast. The orchestrator re-runs the chair
  alone, and anything presented before that is labeled a verified-findings ledger with no chair
  report.
- **The completeness auditor dies.** The run continues with an empty coverage certificate whose
  `not_covered` says the audit did not run. Coverage is an audit of the workshop's own reading,
  not a finding, so it is reported as not done rather than silently assumed or fabricated, and
  the findings are unaffected.
- **The Workflow engine is off.** Symposium and Summit fall back to Workshop depth and
  the report says so. The fallback engine changes speed and scale only; every rule
  still applies.
- **Act II inputs are missing.** Scope narrows to what the inputs support (down to
  edit-spec only when there is no manuscript source), and the report lists each
  skipped item and why.
- **The baseline does not reproduce.** Act II stops before any edit; the diverging
  numbers and the run log are reported as the first finding.
- **Always.** `meta.json` records every check and degradation, and the report header
  carries the run's actual mode and the serving model, recorded at kickoff and
  re-checked at the end (a Fable session can silently migrate to Opus 4.8; see
  `helpers/doctor.md`).

## Session storage

Each run creates `<cwd>/paper_workshop_sessions/<YYYYMMDD-HHMM-slug>/` containing
the brief, copied inputs (`input/`), the per-phase artifacts and verifier
transcripts (the run's primary auditable record), and the final report. Never
modify the author's source documents; copy them into `input/` first.

## What this skill does NOT do

- No Python preprocessing of the PDF for Act I (Claude reads PDFs natively); the only
  Python in Act I is the deterministic quote-gate (the orchestration itself runs in the
  Workflow JS).
- No confidence scores, percentages, or venue acceptance-odds numbers anywhere.
- No fabricated citations, numbers, quotes, data, or results. Ever.
- No silent edits: Act II emits tracked changes on copies for human acceptance.
- No number in the revised paper that a logged re-run did not produce.
- No automatic merge, submission, or data release.

## Files

```
paper-workshop/
├── SKILL.md                 ← you are here
├── README.md                ← brand, install, the mad-research relationship
├── LIMITATIONS.md           ← what is enforced vs not yet proven
├── rubric.md                ← LOCKED severity rubric (no numeric scores)
├── coverage_rubric.md       ← the dimensions the completeness audit certifies
├── schemas/                 ← finding, verification, roster_contract, synthesis, edit_spec
├── prompts/                 ← shared_grounding_rules + 00..07 (Act I) + phase2/10..16 (Act II)
├── helpers/                 ← orchestration, doctor, verification_panel, quote_gate.(py|md),
│                              absence_gate.(py|md), style_gate.(py|md), provenance.py,
│                              consistency.py, reproduces.py, integrity_diff.py, stopping_rule,
│                              desk_review_mode, pdf_extraction, phase2_sandbox, safety_notes
├── workflow/                ← phase1_tribunal.js, phase2_atelier.js (the Workflow scripts)
└── examples/                ← incentives-workshop/ (end-to-end on a real accepted paper)
                               + self-audit/ (the tool run on its own design)
```
