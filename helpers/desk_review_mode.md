# Desk Review mode — the minimal-setup path (no fleet, no Workflow)

Desk Review is the lightest mode: it needs neither dynamic workflows nor a large fleet,
so it runs on any setup (including the leanest plan/usage). The orchestrator drives it
directly with a handful of sequential subagent calls (Agent tool) — or, on the very
lightest setups, inline. It reuses the **same prompts, rubric, and grounding rules** as
the full workshop; it just skips the roster, the cross-critique, and the big verification
panel to keep cost at ~1–6 agents.

## The pass (in order)
1. **Cartography (simplified).** Read the PDF; extract `input/paper.txt` (verbatim) and a
   short list of the main load-bearing claims. Skip the full sentence-tiling map and the
   source manifest unless the user wants citation checks.
2. **1–3 specialist passes.** Call `prompts/01_specialist_seat.md` with a broad seat —
   `objective_function: neutral-audit`, jurisdiction "validity, identification/method, and
   overclaim across the whole paper" — and, if the budget allows two more, one
   `find-the-fatal-flaw` seat and one paper-type-bound specialist (e.g. publication-bias for
   a meta-analysis). Each returns findings in the standard `finding` schema.
3. **Generalist pass.** Call `prompts/02_generalist_seat.md` once for each of
   relevance / understandability / cross-field-significance (or fold into one call at the
   leanest budget).
4. **Quote-gate (deterministic, always).** Run `helpers/quote_gate.py batch` on the
   findings; force any unmatched quote to `needs-author-confirmation`. If any finding is
   absence-class (`absence-silence`, `contribution-undersell`), also run
   `helpers/absence_gate.py batch`; anything but a clean `absent` certificate forces
   `needs-author-confirmation`, and each result row is attached to its finding as
   `absence_gate` so the chair's inline checks can read it. This is the one step Desk Review never skips — it is
   the trust anchor.
5. **Synthesis.** Call `prompts/06_chair_synthesis.md` once to produce the report (verdict,
   prioritized must-fix capped ~5–7, venue read, minority report, rejected suggestions).
   Desk Review produces no integrators, no pre-mortem, and no completeness audit, so
   substitute explicitly: `VERIFIED_FINDINGS_JSON:` the gate-checked findings from step 4
   (the chair's primary input), `REGISTER:` the run's register, `RULES_PATH` /
   `RUBRIC_PATH:` the usual file paths,
   `INTEGRATION_JSON: []`, `PREMORTEM_JSON: []` (`kill_shots` may
   be empty), `REJECTED_JSON:` the findings the chair's inline checks dropped (below),
   and `COVERAGE_JSON: { claims_total: <count from step 1>, claims_covered: <claims
   touched by findings>, sentences_total: 0, sentences_covered: 0, dimension_coverage:
   [], reopen: [], not_covered: [] }` with the report labeled "coverage audit not run
   (Desk Review)" — `sentences_total: 0` means *not run*, never full coverage.
   There is no separate verification panel in Desk Review; instead the chair is instructed
   to apply the `logical-validity` and `steelman-charity` checks inline before it keeps a
   finding, and to fill each prioritized finding's `panel_summary` with
   "Desk Review: chair-inline logical-validity + steelman check (no panel)". Feed any
   `contribution-undersell` findings to the chair ONLY via `CONTRIBUTION_JSON` (empty
   array if none): they land in the non-blocking `contribution_memo` (cap 3), never in
   the prioritized list.

## Output
A prioritized, grounded findings list + a one-page report. If the user then wants Act II,
Desk Review hands its findings to the Atelier exactly like the full workshop does — the
ledger schema is identical — so a light review can still produce a redline.

## Labeling
Label the run "Desk Review" in the report header so the reader knows it is a single-pass
review, not the full adversarial workshop with the multi-angle panel. Severity is still
locked to `rubric.md`; nothing is fabricated; the quote-gate still runs.
