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
- **Agent tool (subagents) — required, available on every plan.** The workshop always
  runs via subagents. The **Workflow tool is OPTIONAL**: prefer it when available (default
  on Max; on Pro, enable it in `/config`) for efficient orchestration; otherwise use the
  subagent fallback (orchestration Step 4b). **Desk Review** needs neither. Detect the
  engine and tell the user which one you're using.
- **Orchestrator model and context (subagents inherit it).** Every seat and verifier is a
  subagent, and subagents run on the **same model and context window as the orchestrating
  session**; the skill cannot override this. Run that session on a model your plan can spawn at
  scale. In particular, a large-context model (a 1M-token window) may require usage credits
  enabled for that tier; without them, subagent spawns fail at the very start of a run, before
  any findings, with a context/credit error. That is an account setting, not a workshop bug.
  Fixes: (a) run the orchestrator on a standard-context model, so the subagents inherit standard
  context, or (b) enable usage credits for the large-context tier. Very large fan-outs can also
  hit transient rate limits that clear on their own; higher-tier plans (e.g. Max) have more
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

Record every check result in `meta.json`.
