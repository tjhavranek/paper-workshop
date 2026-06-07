---
name: paper-workshop
description: |
  CRUCIBLE — a Claude-only adversarial expert workshop that stress-tests a
  scientific paper and then, opt-in, rebuilds it. ACT I (TRIBUNAL): from the
  paper PDF (plus a few public cited works it fetches), a topic-adapted fleet of expert
  referee subagents — every
  contested claim argued from at least two COMPETING intellectual traditions,
  plus generalist seats for relevance and understandability — reviews the paper
  to the sentence, every comment grounded in an exact quote (no fabrication, no
  confidence scores) and independently re-checked from many angles before
  delivery. ACT II (ATELIER, opt-in): with the author's source + data + code,
  it implements the agreed changes as a tracked-changes redline plus a clean
  accepted version, RE-RUNS the analysis under an execution-provenance wall
  (no number enters the paper unless a logged re-run produced it), and
  assembles a replication package — every change multi-angle-verified, nothing
  applied without the author's sign-off on anything that touches the record.

  Triggers:
   - "workshop this paper" / "workshop my paper <file>" / "run paper-workshop on <file>"
   - "convene the workshop on <file>" / "convene the tribunal on <file>"
   - "CRUCIBLE <file>" / "give me an elite referee workshop on <file>"
   - "workshop and stress-test this manuscript" / "brutally workshop this paper"
   - "red-team and rebuild my paper <file>"
   - Act II: "implement the workshop changes" / "rebuild my paper" /
     "build the replication package" / "do Act II / the atelier"

  Use mad-research instead for a fast, read-only, cross-model (Claude+Codex)
  audit memo with no implementation. Use paper-workshop when you want the
  largest possible Claude-only expert fleet AND the option to actually fix
  the paper and ship its replication package.
---

# paper-workshop (CRUCIBLE)

> *Every paper leaves changed.*

A two-act simulation of the workshop a paper would get if a specialist were
assigned to **every** contested choice, each one argued by **both** rival schools,
a generalist panel asked whether it **matters** and is **intelligible**, every
comment were **independently re-checked from many angles**, and then the best of
the room **rebuilt the paper and its replication package**.

The deeper modes can run for a while by design (you choose the depth). The whole
tool is Claude-only; it uses Claude 4.8's **Workflow** engine when available and
plain subagents otherwise, with live work (fetching cited sources, running the
author's code) via the **Agent/Bash** tools.

**Honest limits.** See [`LIMITATIONS.md`](LIMITATIONS.md): effectiveness is not measured yet
(no recall or false-positive numbers), same-model decorrelation is a design bet, and Act II's
rebuild is built and unit-tested but not yet field-proven end to end.

## The two acts and the gate between them

- **Act I — TRIBUNAL.** Input: **the paper PDF** — no data or code, and it touches none of
  your files (it does fetch a few *public* cited works to check the paper's claims). Output: a verified,
  prioritized finding ledger + a referee-report bundle + a debate transcript + an
  importance memo + a completeness certificate. Read-only;
  nothing of the author's is touched. (`workflow/phase1_tribunal.js`)
- **[HARD GATE].** The skill **stops** and offers to implement. It never
  auto-chains into Act II.
- **Act II — ATELIER.** Opt-in. Asks for the manuscript **source** (.tex/.docx),
  **data**, and **code**, then implements every safely-implementable finding as
  tracked changes, re-runs the analysis against the data, regenerates figures and
  tables, and assembles a reproducing **replication package** — all on copies, all
  author-approvable. (`workflow/phase2_atelier.js`)

The two acts share one spine: the **Verified Finding Ledger**
(`schemas/finding.schema.json`). Act I produces it; Act II consumes it.

## What makes it trustworthy at scale (read `prompts/shared_grounding_rules.md`)

The fleet is the product; the rails below are what keep a 300–600-agent run from
laundering a fatal flaw into a confident green light. They are always on and cost
almost nothing — never traded away for scale.

- **Multi-angle independent verification before delivery.** *Nothing* reaches the
  user until several blind subagents, **each from a different angle**, have checked
  it (quote/locator, logical validity, severity calibration, decision-relevance,
  fix-safety, charitable steelman — with factual/literature added at the deeper tiers; Act
  II adds numeric provenance, consistency, integrity). See `helpers/verification_panel.md`.
- **Ground, don't recall; never fabricate.** Exact quote + locator on every
  finding, verified by the deterministic `helpers/quote_gate.py` (not an LLM).
  Unverifiable → `needs-author-confirmation`, never asserted.
- **No confidence scores. Severity is tone-invariant** (`rubric.md`).
- **Decorrelate by rival objective function**, commit-and-reveal independence,
  un-deletable verbatim dissent, preserved minority report.
- **Act II Execution-Provenance Wall:** no number enters the paper unless a real, logged
  re-run produced it — re-hashed and value-checked by the deterministic `helpers/provenance.py`
  + `helpers/consistency.py` (fail-closed), with `helpers/reproduces.py` deciding "reproduces"
  and `helpers/integrity_diff.py` flagging any net result-removal to author sign-off.

## Modes (pick your depth — runs on any paid plan)

Run size scales with the number of **expert seats**; the verification panel is *batched by
angle* (cost ≈ `angles × ceil(#findings / batch) × redundancy`, not `#findings × angles`),
and each seat returns ≤ ~8 findings. The lighter modes' cost grows with the depth you
choose; the two heavy modes add a per-section sentence sweep, so their cost **also scales
with paper length**.

| Mode | What convenes | Expert seats | ≈ agents | Best for |
|---|---|---|---|---|
| **Desk Review** | one expert pass (no fleet) | a few inline lenses | ~1–6 | a fast read; lightest setup |
| **Roundtable** | a small adversarial panel | 6–8 | ~20–30 | a quick but real workshop |
| **Workshop** *(default)* | the full adversarial workshop | 12–18 | ~45–65 | serious pre-submission review |
| **Symposium** | a large fleet + close-readers | 25–40 | ~90–250 | top-venue preparation |
| **Summit** | every subsystem + every sentence | 60–120+ | ~300–600 | the most exhaustive pass (opt-in) |

Symposium/Summit counts grow with paper length (the sentence sweeps); a very long paper can
push Summit past 600. The seat count — the main cost driver — is cast by the scout within
the target bands, so these totals are typical, not hard limits (the script bounds only the
verification and sweep fan-out). Default is **Workshop**. **Symposium and Summit are
best run with the Workflow engine** — the subagent fallback is practical up to Workshop;
beyond that, without workflows the orchestrator should fall back to Workshop depth **and tell
the user**, rather than downgrading silently. (Internal
tier keys: Roundtable=`quick`, Workshop=`thorough`, Symposium=`exhaustive`,
Summit=`monumental`.)

**Engine & plans — the workshop runs for everyone.** Subagents (the Agent tool) work on
**every plan**, so the orchestrator can always run the phases by spawning subagents
directly. When **dynamic workflows** are enabled (default on Max; on Pro, turn them on in
`/config`), the skill uses `workflow/*.js` to orchestrate those same subagent phases more
efficiently (same phases, prompts, schemas); the subagents still do the work. **Desk Review**
needs neither a fleet nor workflows and is the safe choice on the lightest setups. See
`helpers/orchestration.md` for how the orchestrator picks the engine. Subagents inherit the
orchestrating session's model and context, so run on a model your plan can spawn at scale: a
1M-context session may need usage credits enabled for that tier, or run on a standard-context
model (`helpers/doctor.md` covers this pre-flight).

## Reading order for the orchestrating Claude

1. This file.
2. `prompts/shared_grounding_rules.md` — the fifteen non-negotiables (they bind every agent).
3. `helpers/doctor.md` — pre-flight checks (and, for Act II, sandbox/interpreter checks).
4. `helpers/orchestration.md` — the operational checklist (how to actually run both acts).
5. `helpers/verification_panel.md` — how the many-angle verification gate works.
6. `rubric.md` and `coverage_rubric.md` — the locked severity + coverage standards.
7. The `prompts/` for each phase, and `workflow/phase1_tribunal.js` / `phase2_atelier.js`, as the run proceeds.
8. `helpers/safety_notes.md` — warn the author about anything relevant before sending data anywhere or running code.

## Safety defaults

- Act I is **read-only**. Act II works only on **copies/branches**; the author's
  originals are never mutated, and anything touching a number, sample, claim, or
  result requires explicit author sign-off.
- Code re-runs (Act II) execute in a sandbox, **network-off by default**.
- The only optional non-Claude call is a single **lower-weight external dissent
  leg** ("what did all Claude seats miss?"), which operates on abstracted findings,
  **never raw data**, only with logged consent, and is skipped + disclosed if no
  no-train endpoint is configured.

## Session storage

Each run creates `<cwd>/paper_workshop_sessions/<YYYYMMDD-HHMM-slug>/` containing
the brief, copied inputs (`input/`), the per-phase artifacts and verifier
transcripts (the run's primary auditable record), and the final report. Never
modify the author's source documents — copy them into `input/` first.

## What this skill does NOT do

- No Python preprocessing of the PDF for Act I (Claude reads PDFs natively); the only
  Python in Act I is the deterministic quote-gate (the orchestration itself runs in the
  Workflow JS).
- No confidence scores, percentages, or venue acceptance-odds numbers anywhere.
- No fabricated citations, numbers, quotes, data, or results — ever.
- No silent edits: Act II emits tracked changes on copies for human acceptance.
- No number in the revised paper that a logged re-run did not produce.
- No automatic merge, submission, or data release.

## Files

```
paper-workshop/
├── SKILL.md                 ← you are here
├── README.md                ← brand, install, the mad-research relationship
├── rubric.md                ← LOCKED severity rubric (no numeric scores)
├── coverage_rubric.md       ← the dimensions the completeness audit certifies
├── schemas/                 ← finding, verification, roster_contract, synthesis, edit_spec
├── prompts/                 ← shared_grounding_rules + 00..07 (Act I) + phase2/10..16 (Act II)
├── helpers/                 ← orchestration, doctor, verification_panel, quote_gate.(py|md),
│                              provenance.py, consistency.py, reproduces.py, integrity_diff.py,
│                              stopping_rule, pdf_extraction, phase2_sandbox, safety_notes
├── workflow/                ← phase1_tribunal.js, phase2_atelier.js (the Workflow scripts)
└── examples/                ← self-audit/ (the tool run on itself)
```
