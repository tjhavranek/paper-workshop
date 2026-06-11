# Locked severity rubric

**This file is locked.** No agent may modify, reinterpret, or "calibrate" it at
run time. The synthesizer and the verification panel apply it; they do not
change it. It contains **no numeric scores** by design (see grounding rule 3).

Severity measures a finding's effect on the paper's **validity and acceptance** —
*not* the reviewer's tone, confidence, or eloquence (grounding rule 4).

## The three levels

### High (must-fix)
A competent referee at the paper's target venue would **reject, or demand a
revision that blocks acceptance, on this point alone.** Any one of:
- a **correctness or integrity error** (a wrong derivation, a mis-computed
  statistic, a claim contradicted by the paper's own evidence, a
  mis-/un-attributed result);
- a threat that **changes a headline conclusion** if unaddressed (an
  identification failure, a confound the design cannot rule out, a result that
  does not survive an obvious robustness check);
- a **missing load-bearing analysis** without which the central claim is not
  established (no power analysis behind a null, no test of the key assumption);
- a **fatal framing/overclaim** in which the stated contribution is not what the
  evidence supports.

A single un-rebutted High of the correctness/integrity kind **caps the overall
headline verdict at the floor**, regardless of how strong the rest of the paper
is.

### Medium (should-fix)
Materially weakens the paper; a referee would flag it and require a fix, but it
is **not alone fatal.** Typically:
- changes a **secondary** number, table, or claim (not the headline);
- a robustness/sensitivity gap that probably-but-not-certainly holds up;
- an incomplete or mis-situated literature positioning;
- an interpretation that overreaches the evidence in a fixable way;
- a missing caveat that a careful reading requires.

### Low (nice-to-have)
Presentation, clarity, or polish that **does not change any claim's truth
value**: wording, structure, notation, figure/table legibility, a typo, a
dangling cross-reference. Low items are confined to an appendix in the report
and **never** keep the discovery loop alive (see `helpers/stopping_rule.md`).

## Severity is orthogonal to two other tags

- **`magnitude`** — does fixing it move *a number*, *a conclusion*, or *only
  presentation*? The chair sorts the must-fix list by magnitude, not by seat
  seniority or eloquence.
- **`verification_status`** — has the finding been quote-verified, logic-checked,
  grounded against a source, or is it `needs-author-confirmation` / `cant-tell`?
  **Verification status annotates a finding; it never vetoes its severity.** A
  structural/absence finding can be `High` *and* `needs-author-confirmation` at
  the same time — surface it loudly **and** flag it unconfirmed. Never demote a
  finding for being unquotable.

## The overall verdict

- The **validity verdict** ("is the central claim actually supported?")
  **dominates** the **venue verdict** ("would referees accept it?"). The tool
  never trades truth for acceptance odds.
- The venue read is a **coarse three-bucket** signal — `desk-reject-risk` /
  `major-revision` / `competitive` — accompanied by the two or three specific
  objections most likely to trigger rejection, each tied to a quote, and the
  decisive swing factor. **No acceptance probability, ever.**
