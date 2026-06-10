# Doctor — pre-flight checks

Run these before a workshop. Report problems plainly; offer the degraded scope
rather than failing silently.

## Act I (always)
- **Input readable.** The paper exists and is a PDF (preferred) / .docx / .tex the
  orchestrator can read. PDF is preferred because page locators are stable.
- **Python 3.8+** on PATH (for `helpers/quote_gate.py`). Verify:
  `python --version` (or `python3`). If absent, the quote-gate cannot run and the
  whole grounding guarantee is void — do not proceed; tell the user.
  **Windows:** Python must be callable as `python` or `python3` from the shell; if it
  was installed from the Microsoft Store or conda and the command fails, use the `py`
  launcher (`py -3 --version`) or add Python to PATH. If the gate ever can't run, a
  finding degrades to `needs-author-confirmation` (still valid, but unconfirmed) — never
  a silent pass.
- **Engine: dynamic workflows are the intended path; subagents are the universal fallback.** The
  fleet can always run via the Agent tool (every plan), but the **Workflow engine** runs the same
  phases far more efficiently, spawns its own agents, and is how the tool reaches full scale. It is
  **default on Max**; on **Pro, enable it in `/config`** (recommended, especially for
  Symposium/Summit). Detect the active engine, tell the user, and if the subagent fallback is
  active, recommend enabling dynamic workflows. **Desk Review** needs neither.
- **Session model: run the strongest model available, and disclose which one served.** The fleet
  inherits the orchestrating session's model, so the session model **is** the workshop's capability.
  Recommend `/model best` (Claude Code v2.1.170+), which selects Claude Fable 5 (mythos-class)
  where the plan has it and the latest Opus otherwise; the skill works unchanged on any model.
  `/model` on the session is the supported way to choose the fleet's model; the skill deliberately
  sets no per-agent model. Cost note (as of June 2026): Fable 5's 1M context carries no long-context
  premium, but its base rate is twice Opus 4.8's, so warn before the heavy tiers. **Record the
  session model in `meta.json` at kickoff, re-check it at the end of the run, and carry both in the
  report header.** On Fable 5, a safety-classifier hit silently drops the session back to Opus 4.8
  and it stays there, so a run that started mythos-class may not finish that way; the deliverable
  must say so (accurate labeling).
- **Domain routing (Fable 5 safety classifiers).** Fable 5's classifiers trigger on security
  content and on benign life-science content (lab methods, molecular mechanisms); the bio
  classifier can trip on workspace context alone, and the fleet's subagents see the same workspace.
  For life-science- or security-flavored papers, recommend starting the session on Claude Opus 4.8
  deliberately: the run is then predictable and honestly labeled, instead of silently migrating
  mid-fleet.
- **Model/context inheritance (both engines): the 1M-context credit caveat.** Every seat and
  verifier inherits the orchestrating session's model and context; the skill sets no per-agent
  model, so this holds on BOTH paths — dynamic workflows do **not** change it (Workflow-spawned
  agents inherit the session model just as direct subagents do). The remedies below are therefore
  engine-independent. If the orchestrator runs on a large-context (1M-token) model, that context tier may
  require usage credits enabled on the account; without them, subagent spawns fail at the very
  start of a run, before any findings, with a context/credit error. That is an account setting,
  not a workshop bug. Remedies: (a) enable usage credits for that tier, or (b) run the orchestrator
  on a standard-context model so the subagents inherit standard context. Very large fan-outs can
  also hit transient rate limits that clear on their own; higher-tier plans (e.g. Max) have more
  headroom. A spawn that fails at the start of a run is almost always one of these settings; a
  subagent that fails mid-run, after others succeeded, is worth reporting.
- **Mode sanity & cost preview.** Before launching, tell the user the chosen mode's ≈agent
  count so a weekly-limit-aware user can decide: Desk Review ~1–6, Roundtable ~20–30, Workshop
  ~45–65, Symposium ~90–250, Summit ~300–600 (the last two also grow with paper length). Warn
  that **Summit** may run for an extended time, and **confirm before launching Summit**.

## Act II (only if the user opts in)
- **Manuscript source** present (.tex + `\input` children, or .docx). This is the
  near-blocking input; without it, offer "edit-spec only" mode.
- **Interpreters** for the author's stack on PATH and runnable: `Rscript`,
  `python`, `stata`/`stata-mp`, as the code requires. Missing ⇒ the affected
  numeric/figure findings degrade to author-decision checklists.
- **Build tooling.** `latexmk` (+ `bibtex`/`biber`) for LaTeX; the bundled `docx`
  skill for Word. Missing `latexmk` ⇒ emit the tracked source but cannot prove a
  clean compile; say so.
- **Sandbox.** A way to run the author's code network-off, writing only inside the
  session. If unavailable, do **not** run untrusted code; offer to draft the edits
  for the author to run.
- **git** for the per-finding-commit working copy of the manuscript (the workflow stages a
  copy on branch `paper-workshop/phase2`; the author's original is never touched).
- **Act-II deterministic checkers** (`helpers/provenance.py`, `consistency.py`, `reproduces.py`,
  `integrity_diff.py`) are stdlib-only and use the same Python as the quote-gate — no extra
  install. `python helpers/<name>.py selftest` confirms each is runnable.

## External dissent leg (optional, off by default)
- Only if the user asks for it. Confirm a **no-train / retention-disabled** endpoint
  is configured (provider is the user's choice; the skill ships no provider wiring). If not, **skip** the
  leg and disclose it — never downgrade silently to a training-eligible free tier,
  and never send raw data.

Record every check result in `meta.json`, including the session model at kickoff (and re-check
it at the end of the run; see the session-model bullet above).
