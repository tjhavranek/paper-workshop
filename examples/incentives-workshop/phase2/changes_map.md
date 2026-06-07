# Act II changes map — every must-fix finding → disposition

Lanes: **A** = auto-applied prose edit (in `redline.md`); **B** = deferred, needs an author code re-run
(no number is changed by the tool); **C** = author scientific decision (tool proposes, author ratifies);
**D** = author-supplied statistic needed.

| Finding(s) | Concern | Lane | Disposition in this run |
|---|---|---|---|
| F-057, F-066, F-044, F-058, F-068, F-093, F-010 | Abstract/title generalize beyond a design-stage-selected sample | **A** | **Applied** (Edit 1): scope qualifier added to the abstract; mirror it in the title's framing and the conclusion (author to place). |
| F-086, F-030, F-101, F-102, F-132 | Headline heterogeneity from an independence-assuming BMA | **A + B** | **Applied** (Edit 2): prose foregrounds the dependence-aware averaging. **Deferred:** re-derive Table 5 / the PIP ranking from the frequentist model averaging (needs re-run). |
| F-053, F-121 | MAIVE exclusion restriction asserted, not tested | **A + C** | **Applied** (Edit 3): framed as an assumption. **Author:** run a falsification/over-identification test of the instrument. |
| F-085 | MAIVE defined inconsistently ("degrees of freedom" in body vs "observations" in table notes) | **C** | **Proposed (text consistency):** pick one definition (body text implies *degrees of freedom*) and make Table 2 + its B-appendix notes match verbatim. Not auto-applied because the table-note text was not recoverable from the PDF extraction; trivial in the source. |
| F-078, F-082, F-080, F-090, F-048 | Lab+loss exception is a fitted (not directly estimated) interaction; threshold-straddling; no power analysis; framing-inclusion reportedly unstable | **B** | **Deferred:** estimate the lab×loss interaction directly and report its PIP/CI; add a power/precision analysis for that cell; confirm stability under the alternative priors. All require a re-run. Numeric sub-claims marked *needs-author-confirmation*. |
| F-046, F-103, F-104, F-105 | PCC comparability across heterogeneous designs + sign-harmonization under-justified | **C + B** | **Author:** surface the sign-harmonization rule from the table footnote into the methods text (prose, author to place); optionally report PCC distributions by estimation technique (re-run). |
| F-026, F-027, F-028 | PIP>0.5 threshold unmotivated; no MCMC convergence diagnostics; a Table B12 robustness shift downplayed | **C + D** | **Author:** state the threshold convention + cite; report convergence diagnostics; give the B12 shift its due weight. |
| F-038, F-092 | No inter-coder reliability for 48 hand-coded moderators; protocol not stated as pre-registered | **D** | **Author-supplied:** report kappa/alpha/ICC for the coding; state registration status. |
| F-067, F-069 | Near-zero average framed as inconsistent with motivation-crowding theory | **C** | **Proposed (prose):** reword to note the theory predicts mechanism differences, not uniform magnitude differences; near-zero averages are compatible with offsetting crowding. Author to ratify the scientific framing. |
| F-013 | Doucouliagos thresholds cited but not used to interpret magnitudes for the reader | **A** | **Proposed (prose):** add one interpretive clause where the headline PCCs first appear (author to place). |

**Net result of this Act II run:** 3 prose edits applied as tracked changes; **0 numbers changed**; the
remaining must-fix items are routed to the author re-run or to author sign-off, exactly as the
Execution-Provenance Wall requires when the analysis cannot be re-executed.
