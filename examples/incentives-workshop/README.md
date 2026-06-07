# Example run — *Financial Incentives and Performance* (a real, accepted paper)

A demonstration of `paper-workshop` (CRUCIBLE) run **end-to-end on an external, already-accepted
paper**, with the authors' consent:

> Cala, Havranek, Irsova, Luskova, Matousek & Novak, *Financial Incentives and Performance: A
> Meta-Analysis of Experiments in Economics*, **Journal of Political Economy Microeconomics**,
> forthcoming. Source + data + code: <https://meta-analysis.cz/incentives/>.

This complements [`../self-audit/`](../self-audit/) (the tool run on its own design). Here the tool runs
on a real third-party meta-analysis: 2,193 estimates from 88 economics experiments, with publication-bias
correction and Bayesian model averaging.

## Headline

A strong, transparent paper. The workshop's two dominant cruxes — each raised independently by **five**
seats — are:

1. **Scope vs. design-stage selection.** The abstract/title state a general policy claim ("rarely
   produces large performance gains") while the sample is, by the authors' own account, curated to avoid
   contexts where incentives are expected to have large effects (the qualifier lives on p.70).
2. **The headline heterogeneity rests on a dependence-naive model.** The moderator ranking and Table 5
   come from a BMA that *"treats all observations as independent"*, while the dependence-aware
   frequentist averaging — already in the paper — is secondary.

Neither overturns the paper; both are fixable by re-emphasis and promoting the dependence-aware results.
Full reasoning in [`REPORT.md`](REPORT.md).

## What's here

| File | What it is |
|---|---|
| [`REPORT.md`](REPORT.md) | The Act I human-facing report (verdict, must-fix, kill-shots, minority report, venue read, coverage). |
| [`synthesis.json`](synthesis.json) | The structured chair synthesis (`schemas/synthesis.schema.json`). |
| [`findings.json`](findings.json) | All 137 findings (cleaned), with per-finding quote-gate result and verification-panel verdicts. |
| [`roster_contract.json`](roster_contract.json) | The adversarial panel the scout assembled (16 specialist seats + 3 generalists). |
| [`brief.md`](brief.md) | The on-disk brief every seat read. |
| [`run_meta.json`](run_meta.json) | Run metadata + the disclosed degradations. |
| [`phase2/`](phase2/) | Act II: the tracked-changes redline ([`redline.md`](phase2/redline.md), [`redline_passages.docx`](phase2/redline_passages.docx)), the [`changes_map.md`](phase2/changes_map.md) triage, [`edit_specs.json`](phase2/edit_specs.json), and the [`AI_DISCLOSURE.md`](phase2/AI_DISCLOSURE.md). |

## By the numbers

- 22 seats → **137 findings**; 131 delivered, 6 dropped by the verification panel, 3 needs-author-confirmation.
- Severity (post-calibration): **45 High / 58 Medium / 34 Low**.
- Every non-absence quote passed a deterministic quote-gate (108 quote-matched + 28 absence-exempt).
- Act II: **3 prose edits** applied as tracked changes; **0 numbers changed**.

## Honest run conditions (read this)

This is a **demonstration**, not a clean reference run or independent validation. It ran under real
constraints, all disclosed in [`run_meta.json`](run_meta.json) and at the foot of [`REPORT.md`](REPORT.md):

- **No Python on the host** → the deterministic quote-gate ran via a faithful **Node port** of
  `helpers/quote_gate.py` (same normalization).
- **No R/Stata** → Act II **could not re-run the analysis**, so — exactly as the Execution-Provenance
  Wall requires — **no number was changed**; numeric findings are routed to the authors' own re-run.
- **No `.tex`/`.docx` source** → the redline is reconstructed against the PDF-extracted text.
- **Model mix:** Sonnet for cartography/roster/12 seats; Haiku for the remaining 10 seats + the
  verification panel (a usage-limit workaround); the chair synthesis was composed by the orchestrator.
- **Phase C (web-grounding of cited works) was skipped**, so literature claims are not verified against
  originals.

Treat the output as one thorough opinion and re-derive any numeric sub-claim yourself.
