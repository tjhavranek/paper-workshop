# Changelog

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
- **Dogfooded on itself** before release (`examples/self-audit/`): a real brutal Act I run
  (40 agents, 76/82 findings delivered, 6 panel-rejected). It caught genuine overclaims in
  the design **and a fail-open bug in its own quote-gate** — both fixed in response (the
  quote-gate now fails closed and tolerates BOM files). A self-audit is a
  development pass, not independent validation.
