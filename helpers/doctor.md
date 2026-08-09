# Doctor, pre-flight checks

Run these before a workshop. Report problems plainly; offer the degraded scope
rather than failing silently.

## Act I (always)
- **Input readable.** The paper exists and is a PDF (preferred) / .docx / .tex the
  orchestrator can read. PDF is preferred because page locators are stable.
- **Python 3.8+** on PATH (for `helpers/quote_gate.py`). Verify:
  `python --version` (or `python3`). If absent, the quote-gate cannot run and the
  whole grounding guarantee is void. Do not proceed; tell the user.
  **Windows:** Python must be callable as `python` or `python3` from the shell; if it
  was installed from the Microsoft Store or conda and the command fails, use the `py`
  launcher (`py -3 --version`) or add Python to PATH. If the gate ever can't run, a
  finding degrades to `needs-author-confirmation` (still valid, but unconfirmed), never
  a silent pass.
- **Engine: dynamic workflows are the intended path; subagents are the universal fallback.** The
  fleet can always run via the Agent tool (every plan), but the **Workflow engine** runs the same
  phases far more efficiently, spawns its own agents, and is how the tool reaches full scale. It is
  **default on Max**; on **Pro, enable it in `/config`** (recommended, especially for
  Symposium/Summit). Detect the active engine, tell the user, and if the subagent fallback is
  active, recommend enabling dynamic workflows. **Desk Review** needs neither.
- **Session model: run the strongest model available, and disclose which one served.** The fleet
  inherits the orchestrating session's model, so the session model **is** the workshop's capability.
  Recommend `/model best` (Claude Code v2.1.170+), which selects the strongest model the plan
  carries; the skill works unchanged on any model. As of August 2026 the current generation is the
  Claude 5 family (Opus 5, Sonnet 5, Fable 5) alongside Haiku 4.5, so read the live model list
  rather than assuming the names here are still current.
  `/model` on the session is the supported way to choose the fleet's model; by default the skill
  sets no per-agent model (the opt-in economy register below is the one exception). Cost note,
  checked June 2026 and not re-verified since: Fable 5's 1M context carried no long-context
  premium, but its base rate was twice that of the then-current Opus, so warn before the heavy
  tiers and re-check current pricing. **Record the
  session model in `meta.json` at kickoff, re-check it at the end of the run, and carry both in the
  report header.** On Fable 5, a safety-classifier hit silently moves the session to a different
  model and it stays there (observed dropping to Opus 4.8 in June 2026), so a run may not finish
  on the model it started on; the deliverable
  must say so (accurate labeling).
- **Domain routing (Fable 5 safety classifiers).** Fable 5's classifiers trigger on security
  content and on benign life-science content (lab methods, molecular mechanisms); the bio
  classifier can trip on workspace context alone, and the fleet's subagents see the same workspace.
  For life-science- or security-flavored papers, recommend starting the session deliberately on the
  current Opus rather than Fable: the run is then predictable and honestly labeled, instead of silently migrating
  mid-fleet.
- **Model/context inheritance (both engines): the 1M-context credit caveat.** Every seat and
  verifier inherits the orchestrating session's model and context; the skill sets no per-agent
  model, so this holds on BOTH paths. Dynamic workflows do **not** change it (Workflow-spawned
  agents inherit the session model just as direct subagents do). The remedies below are therefore
  engine-independent. If the orchestrator runs on a large-context (1M-token) model, that context tier may
  require usage credits enabled on the account; without them, subagent spawns fail at the very
  start of a run, before any findings, with a context/credit error. That is an account setting,
  not a workshop bug. Remedies: (a) enable usage credits for that tier, or (b) run the orchestrator
  on a standard-context model so the subagents inherit standard context. Very large fan-outs can
  also hit transient rate limits that clear on their own; higher-tier plans (e.g. Max) have more
  headroom. A spawn that fails at the start of a run is almost always one of these settings; a
  subagent that fails mid-run, after others succeeded, is worth reporting.
- **Mode sanity & cost preview, with the economy offer.** Before launching, tell the user the
  chosen mode's ≈agent count so a weekly-limit-aware user can decide: Desk Review ~1–6,
  Roundtable ~20–30, Workshop ~45–65, Symposium ~90–250, Summit ~300–600 (the last two also grow
  with paper length). Warn that **Summit** may run for an extended time, and **confirm before
  launching Summit**. On a usage-capped plan with the session on Fable, ALWAYS pair the preview
  with the economy offer before any Workshop-or-larger launch. A default all-Fable Workshop has
  locked users out of a Max-plan window mid-run, and a locked-out run delivers zero findings.
  One line suffices: "Workshop at the session model is the full-power default and can spend a
  large share of your plan window; the economy register (judgment seats at the Opus floor,
  mechanical phases on Sonnet, scout/chair/scribes unchanged, every rail identical, fully
  disclosed) measured 3.70M subagent tokens / 55 minutes for its tribunal workflow on its one
  field run. Economy or full
  power?" **On a Fable session, present economy as the RECOMMENDED, pre-selected choice**
  (full power then requires the user's explicit "yes, spend it"). On Fable the lockout
  failure is documented and its cost is total (zero findings), so the default answer must
  be the safe one while the contract stays opt-in. On an Opus session present the choices
  neutrally (economy saves little there); on a Sonnet session do NOT recommend economy (it
  cannot help and, unclamped, would raise judgment seats to Opus). Never enable economy
  silently; never skip the offer where the lockout risk is real. **Structural gate:** write
  `economy_offered: true` (with the user's answer) into `meta.json` BEFORE launching any
  Workshop-or-larger run on a Fable session. A missing field is an auditable omission,
  not a silent skip.
- **Economy register pre-flight (only when economy or a custom `models` map is on).** Confirm
  which model tiers the plan actually serves (a quick probe: spawn one trivial subagent per
  mapped tier, or check plan documentation); a mapped-but-unavailable model falls back to
  inheritance at spawn time and is logged in the run's `casting.degraded_casting`. Expect and
  disclose that, do not treat it as a failure. ALWAYS pass `session_model` (the model
  recorded at kickoff) in the workflow args: it arms the engine's never-upgrade clamp, so a
  mapped model above the session tier inherits instead of silently raising the run's cost
  (the clamp is what makes economy safe to request on any session; without the arg the map
  is applied as given). For notation-, math-, or table-dense papers keep
  CARTOGRAPHY at the session model: paper.txt is what the deterministic quote gate matches
  against, so extraction fidelity is load-bearing. Mechanism (a `models` map REPLACES the
  economy map wholesale and labels the run `custom`, so there is no partial tweak): either
  run such papers at the default full power, or pass the full documented economy map with
  only the `carto` entry raised to the session tier and disclose the run as the
  `custom`-labeled cast it then is. Record the casting object (mode, role→model map, degraded fallbacks,
  caps, batch) in `meta.json` at kickoff; whenever the mode is not `inherit`, the report header
  must state the role-class cast in one sentence (grounding rule 15).

## Act II (only if the user opts in)
- **Manuscript source** present (.tex + `\input` children, or .docx). This is the
  near-blocking input; without it, offer "edit-spec only" mode.
- **Multi-pass provenance** (field-grounded: re-running on a prior revision compounded
  em-dash drift 10→18→20 across passes). Ask whether the source is the author's own writing
  or an earlier paper-workshop output being re-run. If the latter, also get the author's last
  hand-written version and record its path as `original_manuscript`: the style gate is
  author-relative, so a baseline that already carries the tool's voice lets the drift launder
  silently. The voice check must also run on the final polished text, not only the first
  revision's edits.
- **Interpreters** for the author's stack on PATH and runnable: `Rscript`,
  `python`, `stata`/`stata-mp`, as the code requires. Missing ⇒ the affected
  numeric/figure findings degrade to author-decision checklists.
- **Package dependencies, checked BEFORE any workflow launch** (field-grounded: a baseline
  gate failed twice on a missing SSC package a 30-second check would have caught, and the
  sandbox correctly refuses mid-run network installs). Stata: grep every do-file for
  community commands (`xtscc`, `reghdfe`, `ppmlhdfe`, `ivreg2`, `ivreghdfe`, `estout`,
  `esttab`, `outreg2`, `winsor2`, `coefplot`, `boottest`, `xtabond2`, …) and resolve each
  via Stata batch `which <cmd>`. R: parse `library()`/`require()`/`p_load()` calls against
  `installed.packages()`. Python: imports against the environment. Any missing dependency
  ⇒ ask the user UP FRONT: install now (network, with explicit consent) or run the
  documented degraded path. One question at kickoff replaces failed workflow launches and
  permission-denial round-trips mid-run.
- **Build tooling.** `latexmk` (+ `bibtex`/`biber`) for LaTeX; the bundled `docx`
  skill for Word. Missing `latexmk` ⇒ emit the tracked source but cannot prove a
  clean compile; say so.
- **Sandbox.** A way to run the author's code network-off, writing only inside the
  session. If unavailable, do **not** run untrusted code; offer to draft the edits
  for the author to run.
- **git** for the per-finding-commit working copy of the manuscript (the workflow stages a
  copy on branch `paper-workshop/phase2`; the author's original is never touched).
- **Act-II deterministic checkers** (`helpers/provenance.py`, `consistency.py`, `reproduces.py`,
  `integrity_diff.py`) are stdlib-only and use the same Python as the quote-gate, no extra
  install. `python helpers/<name>.py selftest` confirms each is runnable.

## External dissent leg (optional, off by default)
- Only if the user asks for it. Confirm a **no-train / retention-disabled** endpoint
  is configured (provider is the user's choice; the skill ships no provider wiring). If not, **skip** the
  leg and disclose it. Never downgrade silently to a training-eligible free tier,
  and never send raw data.

Record every check result in `meta.json`, including the session model at kickoff (and re-check
it at the end of the run; see the session-model bullet above). On a cast run, the end-of-run
re-check also covers the EFFECTIVE casting: a mid-run session-model migration (the Fable
classifier fallback) changes what the inherited roles (scout, chair, scribes) actually ran on,
and the record must say so.
