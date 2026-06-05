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
- **Mode sanity.** Warn that **Summit** may run for an extended time and spawn ~180–300
  subagents; confirm before launching it. The default **Workshop** mode is ~40–55 agents.

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
- **git** for the per-finding-commit working copy of the manuscript.

## External dissent leg (optional, off by default)
- Only if the user asks for it. Confirm a **no-train / retention-disabled** endpoint
  is configured (provider is the user's choice; the skill ships no provider wiring). If not, **skip** the
  leg and disclose it — never downgrade silently to a training-eligible free tier,
  and never send raw data.

Record every check result in `meta.json`.
