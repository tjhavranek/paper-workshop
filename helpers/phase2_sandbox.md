# Act II — running the author's code safely

This is where a paper tool becomes a research-integrity instrument or a catastrophe.
The rules here implement the Execution-Provenance Wall (grounding rule 13) and the
integrity rails.

## The sandbox
- Run all author code **network-off by default**, writing only inside the session
  (`phase2/runs/<run_id>/`). On Windows, prefer the Bash tool's sandbox; never run
  untrusted code with broad permissions.
- **Raw data is read-only.** Copy it into `phase2/input/data/`, hash it at start and
  end of the run, and confirm the hash is unchanged. All transformations are **new
  derived files produced by inspectable code**, never in-place edits.

## The baseline-reproduction gate (run FIRST, before any edit)
1. Stand up the environment; run the author's master script (or one you constructed
   and the author confirmed) **unchanged**.
2. Diff a handful of the paper's **current** headline numbers against the fresh outputs
   with the deterministic predicate (`python helpers/reproduces.py compare ...`), not by eye.
3. **Match** ⇒ record `baseline_reproduced: true` with the run log; this is the anchor
   for every later "the number still matches" check.
   **Mismatch / error** ⇒ **stop and report.** Show which numbers diverge and the log.
   A broken baseline is itself the most important finding; never "improve" numbers on
   top of a pipeline that never reproduced.

## Runner / Scribe separation
- The **Runner** subagent executes code and captures artifacts. It **cannot edit the
  manuscript.**
- The **Scribe** subagent edits prose/tables. It **cannot invent a number** — it may
  only transcribe a value that carries a **provenance token**.
- A **provenance token** = `{ value, script, line_or_chunk, run_id, input_data_hash,
  output_file, output_hash }` (every field required). Hashes are computed and re-verified by
  the deterministic `helpers/provenance.py` (fail-closed): the Act-II `numeric-provenance`
  verifier rejects any numeric change whose token is missing, whose output hash no longer
  matches, or whose value is not present in the named run artifact.
- **Evidence-grounded progress reports.** Before reporting progress, audit each claim
  against a tool result from this session. Only report work you can point to evidence
  for; if something is not yet verified, say so explicitly. (This complements the
  deterministic provenance gate above.)

## Re-running and propagating
- Re-run the **minimal closure** needed for an affected artifact (prefer `make
  <target>` granularity; fall back to whole-script). Write `phase2/runs/<run_id>/` with
  the exact command, stdout/stderr, env snapshot, and input/output hashes.
- **Tables/figures:** regenerate the script-produced artifact and swap the file;
  prefer the manuscript `\input{}` generated tables/figures so re-runs stay accurate.
  Apply presentation findings (labels, units, colorblind-safe palettes) **in the
  plotting code**, then regenerate. Never edit a rendered image or hand-type a table.
- **In-text numbers:** locate the producing computation, re-run, propagate the fresh
  value with its token. Offer to refactor headline numbers into an `\input`-able
  `numbers.tex` of `\newcommand`s so the text literally cannot drift from the code.
- **Determinism:** set and record explicit seeds for any stochastic step; if a re-run
  is non-deterministic and no seed exists, **add** a seed (a visible code change), do
  not report an unstable number.

## Environment capture (for the replication package)
Record the environment you actually ran in (`sessionInfo()`, `pip freeze`,
`conda list`, Stata version banner); pin via `renv`/`requirements`/`conda` where
possible; offer (do not impose) a `Dockerfile`. If the author's original environment
is unknown, say "reproduced under captured environment X" — never imply you matched an
environment you did not have.

## Clean-room replication (final gate)
A Replication-Verifier subagent re-executes the assembled package **from scratch** in a
fresh, seeded, network-off environment and confirms the manuscript's numbers reproduce. The
reproduce-or-fail decision is the deterministic `helpers/reproduces.py` predicate (per
artifact class: float tolerance, fixed seeds), not an LLM judgment. A package that cannot
reproduce its own outputs is **not** marked final — it is reported as failing.
