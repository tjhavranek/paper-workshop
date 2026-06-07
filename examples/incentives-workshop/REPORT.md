# CRUCIBLE workshop report — *Financial Incentives and Performance: A Meta-Analysis of Experiments in Economics*

*Cala, Havranek, Irsova, Luskova, Matousek & Novak — Journal of Political Economy Microeconomics, forthcoming.*
Workshop mode (tier `thorough`), supportive register. Act I (TRIBUNAL). Run 2026-06-07.

> **What this run is.** A demonstration run of the `paper-workshop` skill on an already-accepted
> paper, with the authors' consent. **Read "How this run was conducted" at the end first** — it ran
> under real constraints (no Python/R/Stata on the host; some phases on a smaller model; cited-source
> web-grounding skipped) and is labeled accordingly. Treat it as one thorough opinion, not a verdict.

---

## Verdict

A strong, unusually transparent meta-analysis whose descriptive headline — that after correcting for
publication bias and model uncertainty the mean incentive-performance partial correlation is near zero
in the experimental contexts economists study — is well supported by an above-field-standard correction
battery. Two issues dominate the workshop and were each raised independently by five seats:

1. **Scope vs. design-stage selection.** The abstract and title generalize into a policy-relevant claim
   a sample the paper itself describes as curated to avoid contexts where incentives are expected to
   have large effects. The scope qualifier that lives in Section 3 is missing exactly where readers form
   the takeaway (abstract, title, conclusion).
2. **The headline heterogeneity rests on a dependence-naive model.** The moderator inclusion ranking and
   the Table 5 implied effects come from a Bayesian model averaging exercise the authors concede *"treats
   all observations as independent,"* while the dependence-aware frequentist averaging — which already
   exists in the paper — is secondary.

Neither overturns the paper. Both are addressable by re-emphasis, explicit caveats, and promoting the
dependence-aware results. The single positive finding (lab + loss framing, PCC ≈ 0.07) is the most
fragile claim and should be re-derived and power-checked before it carries interpretive weight.

## Validity verdict (dominates the venue read)

The central descriptive claim is supported by the data and an unusually complete correction battery.
What is **not** fully licensed by the design is (a) the broader policy generalization — because the
pooled literature is, by the authors' own account, selected to avoid large-effect contexts — and (b) the
robustness of the single positive exception, which is a fitted, threshold-straddling, dependence-naive
quantity. **Publishable and strong, but the headline sentence and the one positive result should be
re-scoped and re-derived.**

## Venue read

**Bucket: competitive** (no acceptance-probability number, by design). Swing factor: whether the
abstract/conclusion carry the design-stage-selection scope qualifier and whether the dependence-aware
model-averaging results are promoted to anchor the heterogeneity claims (with the lab+loss exception
re-derived and power-checked). These are emphasis/transparency changes, not new science.

---

## Must-fix (prioritized, capped; sorted by magnitude, not seat seniority)

| # | Finding | Severity | Corroboration | Fix type |
|---|---|---|---|---|
| 1 | **Abstract/title overclaim vs. design-stage selection** (F-057, F-044, F-058, F-066, F-068, F-084, F-093, F-010) — the general "rarely produces large performance gains" claim omits that the sample is curated to avoid large-effect contexts; caveat appears only on p.70. | High | **5 seats** | Prose (safe) |
| 2 | **Headline heterogeneity / BMA treats observations as independent** (F-086, F-030, F-101, F-102, F-078, F-132) — 93% of estimates nest in 88 studies; promote the dependence-aware frequentist averaging to anchor Table 5 and the PIP ranking. | High | **5 seats** | Numeric re-run |
| 3 | **Lab + loss-framing exception is fragile** (F-078, F-082, F-080, F-090, F-048, F-101) — a fitted combination of marginal effects, not a directly estimated interaction; straddles the negligible/small threshold; no power analysis; framing-moderator inclusion reported unstable under alternative priors. | High | 4 seats | Numeric re-run |
| 4 | **MAIVE "preferred" status thin + defined inconsistently** (F-085, F-053, F-120, F-121) — body text says "inverse √ of degrees of freedom," table notes say "observations"; exclusion restriction asserted, not tested. | High | 3 seats | Text fix + author test |
| 5 | **PCC as common currency under-justified** (F-046, F-103, F-104, F-105) — comparability across heterogeneous primary models, and the sign-harmonization rule, are asserted rather than shown/surfaced. | High | 2 seats | Text + author analysis |
| 6 | **BMA rigor gaps** (F-026, F-027, F-028) — PIP>0.5 threshold unmotivated; no MCMC convergence diagnostics for a >30-billion-model space; a Table B12 robustness check that moves results is downplayed. | High | 2 seats | Text + author report |
| 7 | **Data-construction transparency** (F-038, F-092) — no inter-coder reliability for 48 hand-coded moderators (100,000+ data points); analysis protocol not stated as pre-registered. | Should | 2 seats | Author statistics |

Two should-fix prose items also carried: the **motivation-crowding mischaracterization** (F-067/F-069)
and the **Doucouliagos threshold interpretation** clarity gap (F-013).

## Kill shots (verbatim, un-deletable — from the desk-reject pre-mortem)

> This paper dies the way every meta-analysis dies that lets its abstract say more than its design can
> license: it tells readers "increasing financial rewards rarely produces large performance gains" while
> admitting in its own next breath that the literature it pooled was assembled by researchers who "rarely
> conduct experiments in contexts where incentives are expected to have large effects because such
> results are considered trivial" — so the paper precisely estimates the average size of an effect in a
> sample explicitly curated to exclude the cases where that effect would be large, and then states the
> resulting near-zero average as if it were evidence about effect size in general.

> The paper's only positive, headline-worthy finding — the lab-plus-loss-framing effect — is not a
> directly estimated interaction but a fitted value combined from separate marginal effects, sitting on
> the negligible/small boundary, with no power analysis for that thin cell: it is the most-cited number
> most likely to fail to replicate.

## Minority report (preserved intact)

A substantial defender position (S-PUBBIAS-DEFENSE, S-BMA-DEFENSE, S-HETEROGENEITY-DEFENSE,
S-FRAMING-DEFENSE) holds that several "fatal" framings are better read as **emphasis and transparency
fixes than validity failures**: the bias-correction battery and dual model-averaging genuinely
triangulate; the design-stage-selection caveat and the BMA independence assumption *are* disclosed (just
not foregrounded); the lab/loss result is grounded in established loss-aversion theory rather than pure
data-dredging; and the PIP>0.5 cutoff is a standard convention (Eicher et al. 2011; Steel 2020). On this
reading the paper needs re-scoping, not re-doing.

## Top strengths (do not break these in revision)

- A publication-bias/p-hacking battery (linear meta-regression + WAAP/Top10/stem/Andrews-Kasy/kink,
  MAIVE, p-uniform*, caliper/p-curve) that triangulates across non-overlapping assumptions.
- Model uncertainty taken seriously with **both** Bayesian and frequentist model averaging — the
  dependence-aware version already exists and can be promoted.
- Unusual candor about its own load-bearing limitations, plus shipped data + code.
- A large hand-collected dataset (2,193 estimates / 88 experiments / 48 moderators) with a documented
  PRISMA search funnel.

## Generalists' importance / understandability memo

The contribution is real but **narrower than the abstract implies**: it cleanly corrects distortion in a
specific experimental literature, and the "so what" for practitioners should be stated as such rather
than as a broad policy claim. For a reader one field over, the load-bearing definitional choice (PCC as a
common currency across grades, donations, productivity, game payoffs) deserves an explicit
justification, and the magnitude thresholds should be used consistently to tell the reader what a PCC of
0.05–0.07 *means*.

## Rejected suggestions (considered, dropped by the verification panel)

Six seat findings were dropped on the **logical-validity** angle, e.g. "the paper offers no practitioner
guidance" and "the design-stage caveat makes the contribution pointless" (out of scope / misreads the
paper), and "PCC standardization is uninterpretable" (the defensible narrower point — comparability
across statistical models — was retained as F-105). Full list in `synthesis.json` → `rejected_suggestions`.

## Coverage certificate

- Claims inventoried: **65**; covered by ≥1 seat: **61**.
- All 12 mandatory coverage dimensions attended (see `synthesis.json` → `coverage_certificate`).
- **Coverage means *attention*, not correctness.** No per-sentence close-reader sweep was run (that is a
  Symposium/Summit-tier pass), so `sentences_covered` is reported as 0 rather than implying a full sweep.
- **Reopen:** (a) numeric claims read from garbled tables (F-079, F-080, F-090) are marked
  *needs-author-confirmation*; (b) related-work/citation-accuracy claims were **not web-grounded** this
  run; (c) Act II numeric findings require re-running the authors' code.

---

## Findings ledger

- **137 findings** from **22 seats** (19 specialist seats, which include the desk-reject pre-mortem
  and the neutral-audit seats, plus 3 generalists); **131 delivered**, 6 dropped by the panel, 3
  marked needs-author-confirmation.
- Severity (post-calibration): **45 High / 58 Medium / 34 Low**.
- Every non-absence quote passed the deterministic quote-gate (108 quote-matched + 28 absence-exempt; 1
  unverified quote was downgraded to needs-author-confirmation).
- Full machine-readable ledger: `round_artifacts/verified_ledger.json`; structured synthesis:
  `round_artifacts/synthesis.json`; per-seat raw findings: `round_artifacts/seats/`.

## How this run was conducted (accurate labeling — grounding rule 15)

This run was **degraded in disclosed ways** and is **not** a clean reference run:

- **No Python on the host** → the deterministic quote-gate was run via a faithful **Node port**
  (`quote_gate.mjs`, same normalization incl. zero-width strip + U+2212 handling) rather than
  `helpers/quote_gate.py`.
- **No R / Stata** → **Act II cannot re-run the analysis.** Per the Execution-Provenance Wall, **no
  number is changed**; every numeric finding is flagged for the authors' own re-run.
- **Model mix:** cartography, the roster, and the first 12 specialist seats ran on **Sonnet**; the
  remaining 10 seats and the verification panel ran on **Haiku** (a usage-limit workaround), so the
  back-half seats are lower-depth — numeric/table claims from those seats are treated skeptically and
  several were marked needs-author-confirmation or cant-tell by the panel.
- **Chair synthesis** was composed by the orchestrator (not a fresh blind subagent) due to the same
  limit — a deviation from the standard fresh-chair design.
- **Phase C (web-grounding of cited works) was skipped**, so the factual-literature angle returned
  cant-tell for claims about cited works; related-work findings need verification against originals.
- **Verification panel** covered the 45 High-severity findings on three angles (logical-validity,
  severity-calibration, fix-safety) plus the deterministic quote-locator; Medium/Low findings received
  the quote-gate but not the full multi-angle panel.

The substance above (the corroborated cruxes, the grounded quotes, the must-fix list) is robust to these
limits; the *exact numeric* sub-claims and the literature claims are the parts most affected.
