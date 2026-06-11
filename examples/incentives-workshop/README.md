# Example run — *Financial Incentives and Performance* (a real, accepted paper)

A demonstration of `paper-workshop` (CRUCIBLE) run **end-to-end on an external, already-accepted
paper**, with the authors' consent:

> Cala, Havranek, Irsova, Luskova, Matousek & Novak, *Financial Incentives and Performance: A
> Meta-Analysis of Experiments in Economics*, **Journal of Political Economy Microeconomics**,
> forthcoming. Source + data + code: <https://meta-analysis.cz/incentives/>.

This complements [`../self-audit/`](../self-audit/) (the tool run on its own design). Here the tool runs
on a real third-party meta-analysis: 2,193 estimates from 88 economics experiments, with publication-bias
correction and Bayesian model averaging.

> **Beyond the critique, the workshop re-ran the paper's analysis end to end.** It executed the
> authors' own Stata 15.1 and R/BMA on the raw data, and the regenerated R-feed intermediate came out
> **byte-for-byte identical** to the shipped one (sha256 `46df404...`). A deterministic provenance
> check ties the headline number `0.0724` to that run (`verified: true`), closing the chain raw data
> -> Stata -> R -> manuscript. Proof set in [`phase2_true/`](phase2_true/) (see
> [`stata/STATA_REPRODUCTION.md`](phase2_true/stata/STATA_REPRODUCTION.md)).

## Headline

A strong, transparent paper. The workshop's two dominant cruxes, each raised independently by at
least five seats, are:

1. **Scope vs. design-stage selection.** The abstract/title state a general policy claim ("rarely
   produces large performance gains") while the sample is, by the authors' own account, curated to avoid
   contexts where incentives are expected to have large effects (the qualifier lives on p.70).
2. **The headline heterogeneity rests on a dependence-naive model.** The moderator ranking and Table 5
   come from a BMA that *"treats all observations as independent"*, while the dependence-aware
   frequentist averaging (already in the paper) is secondary.

Neither overturns the paper; both are fixable by re-emphasis and promoting the dependence-aware results.
Full reasoning in [`REPORT.md`](REPORT.md).

## What's here

| File | What it is |
|---|---|
| [`REPORT.md`](REPORT.md) | The Act I human-facing report (verdict, must-fix, kill-shots, minority report, venue read, coverage). |
| [`synthesis.json`](synthesis.json) | The structured chair synthesis (`schemas/synthesis.schema.json`). |
| [`findings.json`](findings.json) | All 137 findings (cleaned), with per-finding quote-gate result and verification-panel verdicts. |
| [`roster_contract.json`](roster_contract.json) | The adversarial panel the scout assembled (19 specialist seats + 3 generalists). |
| [`brief.md`](brief.md) | The on-disk brief every seat read. |
| [`run_meta.json`](run_meta.json) | Run metadata + the disclosed degradations. |
| [`phase2/`](phase2/) | Act II, **first pass (degraded)**: a tracked-changes redline + triage produced when no source/interpreters were available (numbers deferred). |
| [`phase2_true/`](phase2_true/) | Act II, **true pass**: the analysis was actually **re-run** (R + BMS), the **Stata publication-bias path re-run** (Stata 15.1, regenerating the R-feed data byte-identically), and the manuscript redlined against its real LaTeX source. See [`REPRODUCTION.md`](phase2_true/REPRODUCTION.md) and [`stata/STATA_REPRODUCTION.md`](phase2_true/stata/STATA_REPRODUCTION.md). |

## By the numbers

- 22 seats → **137 findings**; 131 delivered, 6 dropped by the verification panel; 23 of the
  delivered findings carry needs-author-confirmation status in `findings.json` (7 of those High).
- Severity (post-calibration): **45 High / 58 Medium / 34 Low**.
- The deterministic quote-gate checked every non-absence quote: 108 matched and the 1 it could
  not verify was downgraded to needs-author-confirmation, never asserted (28 absence findings
  are exempt by design).
- Act II: **3 prose edits** applied as tracked changes; **0 numbers changed**.

## True Act II — the analysis was actually re-run

A second pass (`phase2_true/`) did the *real* ATELIER: installed R + BMS, **re-ran the BMA heterogeneity
path** of the authors' `incentives.R` on the shipped data, and redlined the **real LaTeX source** with
`latexdiff`-style tracked changes (compiled, 45 pp; kept private since the source is not public).

- **The headline reproduces.** Corrected mean ≈ **0.030**, Laboratory implied effect **0.072** (paper:
  0.073), PIP(Laboratory) **0.9997** (paper: 1.000), on the same 1,252 estimates / 35 regressors (the
  BMA heterogeneity subsample of the full 2,193-estimate dataset).
- **The Execution-Provenance Wall verified for real:** `helpers/provenance.py` ties the value 0.0724 to
  a content-hashed run artifact + hashed input data → `verified: true`
  ([`verify_lab.txt`](phase2_true/provenance/verify_lab.txt)), a check anyone can re-run against this
  repo (the run artifact is committed byte-verbatim; see
  [`REPRODUCTION.md`](phase2_true/REPRODUCTION.md)); `helpers/consistency.py` confirms the
  regenerated 0.073 / 0.03 / 0.07 run-match the manuscript (recorded from the run; the consistency
  output is not committed, unlike the provenance verify files).
- **The Stata path is now re-run too (2026-06-08).** Running the authors' `incentives.do` in Stata 15.1
  on the raw `incentives.xlsx` regenerates `auxiliaries/incentives_4R.csv` **byte-for-byte identical** to
  the shipped intermediate this R pass consumed (sha256 `46df404...`), plus the full FAT-PET /
  publication-bias tables. The chain raw data -> Stata -> R/BMA -> manuscript is now closed end to end
  (the committed `.tex` hashes are reader-reproducible; the data-side byte-identity is recorded from
  the run and reproducible by re-running the public package). See
  [`stata/STATA_REPRODUCTION.md`](phase2_true/stata/STATA_REPRODUCTION.md).
- **The re-run resolved two of the workshop's own High findings, in the authors' favor.** A Haiku seat
  alleged the framing inclusion probability "drops below 0.5" under the BRIC prior (F-080); the re-run
  shows it is **0.957** (robust). And the "0.07 lab+loss" was clarified as lab and loss-framing each ~0.07
  (reproduced), not an unestimated combined cell (F-078). REPORT.md's reopen list had marked the
  garbled-table numeric claims (F-079, F-080, F-090) `needs-author-confirmation`; in the committed
  ledger the two findings stand as delivered High findings with verified quotes, and the re-run then
  tested their numeric sub-claims directly and decided both in the authors' favor.
- **No number was changed** (they reproduce); the redline carries only the three prose/scope edits.

## Honest run conditions (read this)

This is a **demonstration**, not a clean reference run or independent validation. It ran under real
constraints, all disclosed in [`run_meta.json`](run_meta.json) and at the foot of [`REPORT.md`](REPORT.md):

- **No Python on the host** → the deterministic quote-gate ran via a faithful **Node port** of
  `helpers/quote_gate.py` (same normalization).
- **R/Stata** → absent in this first (degraded) pass, so no number was changed here. Both have since
  been re-run in [`phase2_true/`](phase2_true/): R (the BMA path) and, on 2026-06-08, **Stata 15.1**
  (the full publication-bias path), which regenerates the R-feed data byte-identically. The redline
  still changes no number because the numbers reproduce.
- **No `.tex`/`.docx` source** → the redline is reconstructed against the PDF-extracted text.
- **Model mix:** Sonnet for cartography/roster/12 seats; Haiku for the remaining 10 seats + the
  verification panel (a usage-limit workaround); the chair synthesis was composed by the orchestrator.
- **Phase C (web-grounding of cited works) was skipped**, so literature claims are not verified against
  originals.

Treat the output as one thorough opinion and re-derive any numeric sub-claim yourself.
