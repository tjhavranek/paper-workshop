# Act II (true) — re-run, reproduction, and provenance

This is the *true* Act II: the authors' analysis was **actually re-executed** and the manuscript was
redlined against its real LaTeX source. Run on 2026-06-07, fully autonomously.

## Environment (installed for this run)
- **R 4.3.2** (+ Rtools), package **BMS** (binary). Re-run of the heterogeneity/BMA path of
  `incentives.R` on the shipped Stata intermediate `auxiliaries/incentives_4R.csv`.
- **Python 3** — the real deterministic `helpers/provenance.py` and `helpers/consistency.py` (selftests pass).
- **MiKTeX** `latexmk` — compiled the original and the redline from the authors' `.tex`.
- **Stata (added 2026-06-08).** At the time of this R pass Stata was not available, so the Stata-side
  construction used the package's shipped intermediates. It has since been re-run in full: see
  [`stata/STATA_REPRODUCTION.md`](stata/STATA_REPRODUCTION.md). Running the authors' `incentives.do` in
  Stata 15.1 on the raw `incentives.xlsx` regenerates `auxiliaries/incentives_4R.csv` byte-identically
  to the shipped intermediate this R pass consumed, so the chain raw data -> Stata -> R is now closed.
  The R path here (BMA Table 4, Table 5 implied effects, the bias-correction battery) **was** re-run.

## Baseline-reproduction gate — published vs regenerated

| Quantity | Published | Regenerated (re-run) | Match |
|---|---|---|---|
| Estimates / regressors in BMA | 1,252 / 35 | **1,252 / 35** | ✓ |
| Mean best-practice corrected effect | ≈ 0.03 | **0.0301** | ✓ |
| Implied effect, Laboratory experiment | 0.073 | **0.0724** | ✓ |
| Implied effect, Field experiment | (small) | 0.0200 | ✓ (consistent) |
| Implied effect, Negative (loss) framing | ≈ 0.07 | **0.0653** | ✓ |
| PIP, Laboratory experiment | 1.000 | **0.9997** | ✓ |
| PIP, Positive framing (baseline UIP/dilut) | ≈ 0.96 | **0.9564** | ✓ |

**Verdict: the headline reproduces.** The corrected mean effect is ~0.03 and the lab / loss-framing
exceptions are ~0.07 each, as reported. (Tiny differences are MCMC sampling variation; the authors set
no seed, this re-run used `set.seed(2025)`.) Deterministic `consistency.py` confirms the regenerated
0.073 / 0.03 / 0.07 **run-match the manuscript text** (`clean: true`, no orphans).

## Execution-Provenance Wall — proof

`provenance/token_lab.json` ties the value **0.0724** to the hashed run artifact and the hashed input
data; `helpers/provenance.py verify` returns (`provenance/verify_lab.txt`):

```
"verified": true,
"checks": { fields_present, output_exists, output_hash_match, value_present, input_hash_match } → all true
```

So this number is the output of code actually executed in this run, identified by content hash — not a
recalled or transcribed figure.

## What the re-run resolved (two flagged findings, decided)

The Act-I verification panel had quarantined several Haiku-seat numeric claims as
`needs-author-confirmation` rather than asserting them. The re-run now decides them — **in the authors'
favor**:

- **F-080 (alleged): "framing PIP drops below 0.5 under the BRIC/random prior."** **Refuted.** The
  re-run gives PIP(Positive framing) = **0.957** under BRIC/random (and 0.956 under UIP/dilut) — robust,
  not collapsing. The robustness check the seat read as fragility actually corroborates the result.
- **F-078 (alleged): "the 0.07 lab+loss is a fitted combination never directly estimated."** **Clarified.**
  The manuscript's "0.07" refers to laboratory experiments **and** negative-framing experiments *each*
  yielding ~0.07 (reproduced: 0.072 and 0.065), not a single combined cell. For completeness the re-run
  also computes the explicit both-conditions cell (Laboratory + loss framing = **0.108**); this is a
  supplementary quantity the paper does not claim, offered for the authors to use or ignore.
- **F-086 (BMA treats observations as independent)** remains a fair *framing* point (addressed by redline
  Edit 2, foregrounding the dependence-aware frequentist averaging), but the re-run shows the
  conclusions are **robust** to it — the inclusion probabilities are stable across priors.

This is the provenance wall working as designed: unverified numeric criticisms were never asserted, and
the re-run resolved them against the originally-alleged flaws.

## Redline (real, against the authors' `.tex`)

`redline_marked/incentives.pdf` (45 pp) is the compiled manuscript with three tracked (blue) prose
insertions, each answering a corroborated finding; **no number was changed** (the numbers reproduce, so
none needed changing):
1. Abstract scope qualifier (design-stage selection) — F-057/F-066/F-044.
2. Heterogeneity: foreground the dependence-aware averaging — F-086.
3. Publication bias: MAIVE exclusion restriction stated as an assumption — F-053/F-121.

Files: `redline_marked/incentives.tex` (marked source), `redline_marked/incentives.pdf` (compiled),
`source_orig/` (pristine baseline), `source_revised/` (clean revised, no color markup).

## Privacy note
The authors' LaTeX source is **not public** (only the compiled PDF is). The full redline PDF and `.tex`
stay in this local session; the public demo PR carries only the reproduction report, the re-run script,
the provenance proof, and the text of the three redlined passages.
