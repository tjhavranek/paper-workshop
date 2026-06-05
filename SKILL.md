---
name: paper-workshop
description: |
  CRUCIBLE — a monumental, Claude-only dynamic-Workflow simulation of an
  elite workshop on a scientific paper, in two acts. ACT I (TRIBUNAL):
  from the paper PDF alone, a large topic-adapted fleet of expert referee
  subagents — every contested claim argued from at least two COMPETING
  intellectual traditions, plus generalist seats for relevance and
  understandability — stress-tests the paper exhaustively (every argument,
  every section, to the sentence), and every comment is checked by many
  independent verifiers from different angles before delivery. ACT II
  (ATELIER, opt-in): with the author's source + data + code, it implements
  the agreed changes as tracked edits, RE-RUNS the analysis, and produces an
  impeccable revised paper plus a full replication package — every change
  likewise multi-angle-verified, nothing fabricated, nothing applied without
  the author's sign-off on anything that touches the scientific record.

  Triggers:
   - "workshop this paper" / "workshop my paper <file>" / "run paper-workshop on <file>"
   - "convene the workshop on <file>" / "convene the tribunal on <file>"
   - "CRUCIBLE <file>" / "give me an elite referee workshop on <file>"
   - "brutally (but fairly) stress-test and workshop this manuscript"
   - "monumental review of <paper.pdf>"
   - Act II: "implement the workshop changes" / "rebuild my paper" /
     "build the replication package" / "do Act II / the atelier"

  Use mad-research instead for a fast, read-only, cross-model (Claude+Codex)
  audit memo with no implementation. Use paper-workshop when you want the
  largest possible Claude-only expert fleet AND the option to actually fix
  the paper and ship its replication package.
---

# paper-workshop (CRUCIBLE)

> *Every paper leaves changed.*

A two-act simulation of the workshop a paper would get if a world authority on
**every** sub-part were in the room, every contested choice were argued by **both**
rival schools, a generalist panel asked whether it **matters** and is
**intelligible**, every comment were **independently re-checked from many angles**,
and then the best of the room **rebuilt the paper and its replication package**.

Runtime is not a constraint — a monumental run takes hours by design. The whole
tool is Claude-only and orchestrated by Claude 4.8's **Workflow** engine; live
work (fetching cited sources, running the author's code) uses the **Agent/Bash**
tools inside that orchestration.

## The two acts and the gate between them

- **Act I — TRIBUNAL.** Input: **the paper PDF only.** Output: the best feedback
  achievable — a verified, prioritized finding ledger + a referee-report bundle +
  a debate transcript + an importance memo + a completeness certificate. Read-only;
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
  it (quote/locator, logical validity, factual/literature, severity calibration,
  decision-relevance, fix-safety, charitable steelman; Act II adds numeric
  provenance, consistency, integrity). See `helpers/verification_panel.md`.
- **Ground, don't recall; never fabricate.** Exact quote + locator on every
  finding, verified by the deterministic `helpers/quote_gate.py` (not an LLM).
  Unverifiable → `needs-author-confirmation`, never asserted.
- **No confidence scores. Severity is tone-invariant** (`rubric.md`).
- **Decorrelate by rival objective function**, commit-and-reveal independence,
  un-deletable verbatim dissent, preserved minority report.
- **Act II Execution-Provenance Wall:** no number enters the paper unless a real,
  logged re-run produced it; the author signs off on anything touching the record.

## Depth tiers

| Tier | Specialist seats | Use |
|---|---|---|
| `quick` | 6–8 (floor only) | a fast sanity pass |
| `thorough` (default) | 12–18 | a serious pre-submission review |
| `exhaustive` | 25–40 + per-section close-readers | top-venue preparation |
| `monumental` | 60–120+, loop-until-dry on findings AND coverage | "better than any conference" |

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

- No Python preprocessing of the PDF for Act I (Claude reads PDFs natively); the
  one piece of code in Act I is the deterministic quote-gate.
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
│                              stopping_rule, pdf_extraction, phase2_sandbox, safety_notes
├── workflow/                ← phase1_tribunal.js, phase2_atelier.js (the Workflow scripts)
└── examples/                ← self-audit/ (the tool run on itself)
```
