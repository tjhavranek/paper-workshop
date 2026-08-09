# Coverage rubric

The completeness audit (Act I) and the chair's `coverage_certificate` are scored against
**this list**. For every dimension below, the completeness auditor must
mark it `covered by seat <id>` or **`NOT COVERED`** (with a one-line reason); the chair
reports the result, it does not re-score it. On deepened runs, a `NOT COVERED`
load-bearing dimension re-opens a targeted mini-fan-out until it is green or is
explicitly logged "reviewed, nothing found" (the default single pass reports the gap
and stops; see `helpers/stopping_rule.md`). This is what lets the tool claim it
examined *everything*.

Dimensions not applicable to a given paper type are marked `N/A (<reason>)`, but
the Scout must have justified the N/A in the roster contract, not silently
skipped it.

## Substance dimensions
1. **Motivation & contribution.** Is the stated contribution real, novel, and
   correctly sized (neither overclaimed nor undersold)? The contribution rival
   pair (`S-contribution-maximizer` vs `S-contribution-prosecutor`) staffs this
   dimension on every fleet run (the engine injects the pair if the scout omits
   it; Desk Review folds the undersell question into its lighter passes).
2. **Positioning in the literature.** Correctly situated; no missing or
   misrepresented prior work.
3. **Identification / causal validity *(if any causal claim)*.** Does the design
   actually identify the effect; are the assumptions stated and defended?
4. **Data & measurement.** Provenance, sample construction, measurement
   validity, missingness, outliers.
5. **Estimation & statistical validity.** Estimator choice, inference,
   standard errors/clustering, multiple testing, power.
6. **Robustness & sensitivity.** Do the headline results survive obvious
   alternative specifications, samples, and assumptions?
7. **Mechanism & interpretation.** Is the proposed mechanism tested against
   rival explanations (analysis of competing hypotheses), not just asserted?
8. **Magnitude / real-world significance.** Is the effect size meaningful, and
   is its importance accurately characterized?
9. **External validity / generalizability.** How far do the conclusions travel?
10. **Reproducibility.** Are data and code available; is the analysis described
    well enough to reproduce; do declared materials match the claims?
11. **Limitations & threats.** Are they stated fully and completely?
12. **Ethics, integrity & disclosure.** Human-subjects/data ethics, conflicts,
    pre-registration status, AI-involvement disclosure where relevant.

## Presentation dimensions
13. **Abstract, figures, tables.** Accurate, self-contained, legible.
14. **Writing & clarity.** Structure, notation, readability.

## Generalist dimensions (always staffed)
15. **Relevance / so-what.** Does this matter; would the field care; what
    changes if it is true?
16. **Understandability / brilliant-outsider.** Is it intelligible to a strong
    scientist one field over; where does it lose them?
17. **Cross-field significance / does it travel.** Would a neighboring discipline
    care; is there a bigger claim the authors should make or defend? (Findings from
    this seat carry `finding_type: relevance`.)

## The sentence-coverage ledger
Independently of the dimensions above, the Section/Sentence Map (Phase A) tiles the paper
into disjoint sentence ranges whose union equals the whole paper. At the exhaustive and
monumental tiers, close-reader sweeps return a verdict for **every** range, so
`covered_sentences == total_sentences` is checkable. Be clear about what this proves: it
certifies that **every range was examined** (coverage of *attention*), **not** that each
was *correctly* reviewed. A flaw can still hide inside a "covered" range. It is an
auditable assignment ledger, not a correctness guarantee. Any gap re-spawns a sweep for
exactly that gap.

**When nothing returns per-range coverage, the counter is not instrumented, and the certificate
now says so.** In practice that means Desk Review, Roundtable and Workshop, which cast no
close-reader sweeps, but the rule the code applies is about the DATA, not the tier: if no seat
returned any covered range, there is nothing to count, and equally, a heavy-tier run whose sweeps
all died is honestly reported as uninstrumented rather than as full coverage. The workflow
reports `sentences_covered: 0` from code and does not hand the auditor a sentence map to read.
**A 0 there means "not measured on this run", never "not read"**. Every seat reads the
whole manuscript in every mode, and claim coverage and dimension coverage are unaffected.
This replaces earlier behavior in which the auditor was given the map and supplied a
sentence count anyway: the committed Roundtable self-audit reports 648 of 795 sentences
covered on a run with zero close-reader seats and zero returned ranges, which was an
inference, not a measurement.
