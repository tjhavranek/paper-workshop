# Doctor — pre-flight checks

Run these before a workshop. Report problems plainly; offer the degraded scope
rather than failing silently.

## Act I (always)
- **Input readable.** The paper exists and is a PDF (preferred) / .docx / .tex the
  orchestrator can read. PDF is preferred because page locators are stable.
- **Python 3.8+** on PATH (for `helpers/quote_gate.py`). Verify:
  `python --version` (or `python3`). If absent, the quote-gate cannot run and the
  whole grounding guarantee is void — do not proceed; tell the user.
- **Workflow + Agent tools available.** This skill is orchestrated by the Workflow
  engine and spawns Agent/Bash subagents. If the Workflow tool is unavailable, fall
  back to a sequential Agent-tool orchestration (slower, same phases) and say so.
- **Tier sanity.** Warn the user that `monumental` may run for hours and spawn
  hundreds of subagents; confirm before launching it.

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
