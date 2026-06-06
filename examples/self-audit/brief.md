# Self-audit brief (the tool, run on itself)

This is a SELF-AUDIT. The "manuscript" under review is the **design of the
`paper-workshop` / CRUCIBLE skill itself** (its SKILL.md, README, grounding rules,
verification panel, and design doc), concatenated into one document. The skill is
being run on itself before its first public release.

**Adapt (this is not an empirical paper):** treat the skill's *design claims* as the
claims to stress-test. Map the usual seats onto a software/methodology proposal:
- "identification / statistical" → *does the claimed mechanism actually deliver the
  property it claims* (e.g., does the Execution-Provenance Wall really make fabrication
  impossible; does multi-angle verification really stop consensus-laundering)?
- "robustness" → *failure modes*: where does this design break, mislead, or become
  theater at scale?
- "related-work / overclaim" → are the claims (e.g. "every word reviewed", "better than
  any conference", "impeccable") accurately sized?
- generalists → is the design *coherent and intelligible*, and does the whole thing
  *actually matter* vs. a single strong review?

**Register: brutal but fair.** Severity is tone-invariant; find the real weaknesses.
The point of this run is to surface what to fix before release — so prioritize genuine,
grounded design flaws over praise.
