# Coverage rubric

The completeness audit (Act I) and the chair's `coverage_certificate` are scored against
**this list**. For every dimension below, the completeness auditor must
mark it `covered by seat <id>` or **`NOT COVERED`** (with a one-line reason); the chair
reports the result, it does not re-score it. On deepened runs, a `NOT COVERED`
load-bearing dimension re-opens a targeted mini-fan-out until it is green or is
explicitly logged "reviewed, nothing found" (the default single pass reports the gap
and stops; see `helpers/stopping_rule.md`). This is what lets the tool claim it
examined *everything*.

Dimensions not applicable to a given paper type are marked `N/A (<reason>)` — but
the Scout must have justified the N/A in the roster contract, not silently
skipped it.

## Substance dimensions
1. **Motivation & contribution** — is the stated contribution real, novel, and
   correctly sized?
2. **Positioning in the literature** — correctly situated; no missing or
   misrepresented prior work.
3. **Identification / causal validity** *(if any causal claim)* — does the design
   actually identify the effect; are the assumptions stated and defended?
4. **Data & measurement** — provenance, sample construction, measurement
   validity, missingness, outliers.
5. **Estimation & statistical validity** — estimator choice, inference,
   standard errors/clustering, multiple testing, power.
6. **Robustness & sensitivity** — do the headline results survive obvious
   alternative specifications, samples, and assumptions?
7. **Mechanism & interpretation** — is the proposed mechanism tested against
   rival explanations (analysis of competing hypotheses), not just asserted?
8. **Magnitude / real-world significance** — is the effect size meaningful, and
   is its importance accurately characterized?
9. **External validity / generalizability** — how far do the conclusions travel?
10. **Reproducibility** — are data and code available; is the analysis described
    well enough to reproduce; do declared materials match the claims?
11. **Limitations & threats** — are they stated fully and completely?
12. **Ethics, integrity & disclosure** — human-subjects/data ethics, conflicts,
    pre-registration status, AI-involvement disclosure where relevant.

## Presentation dimensions
13. **Abstract, figures, tables** — accurate, self-contained, legible.
14. **Writing & clarity** — structure, notation, readability.

## Generalist dimensions (always staffed)
15. **Relevance / so-what** — does this matter; would the field care; what
    changes if it is true?
16. **Understandability / brilliant-outsider** — is it intelligible to a strong
    scientist one field over; where does it lose them?
17. **Cross-field significance / does it travel** — would a neighboring discipline
    care; is there a bigger claim the authors should make or defend? (Findings from
    this seat carry `finding_type: relevance`.)

## The sentence-coverage ledger
Independently of the dimensions above, the Section/Sentence Map (Phase A) tiles the paper
into disjoint sentence ranges whose union equals the whole paper. At the exhaustive and
monumental tiers, close-reader sweeps return a verdict for **every** range, so
`covered_sentences == total_sentences` is checkable. Be clear about what this proves: it
certifies that **every range was examined** (coverage of *attention*), **not** that each
was *correctly* reviewed — a flaw can still hide inside a "covered" range. It is an
auditable assignment ledger, not a correctness guarantee. Any gap re-spawns a sweep for
exactly that gap.
