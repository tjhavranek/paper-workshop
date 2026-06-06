# Safety notes — read before sending data anywhere or running code

## Data never leaves the machine without consent
- Act I and Act II run on Claude (the model already in your session) and locally.
  The **only** optional external call is the lower-weight dissent leg (below).
- **Never send raw data externally**, under any circumstances. The dissent leg
  operates on abstracted findings/claims, never datasets.
- Before any web fetch (Phase C source-grounding) or any external-model call, warn the
  user what would be sent and to where, and get explicit, logged consent.
- Refuse embargoed / NDA / "no-AI-tools" material for anything that would transmit it.

## The optional external dissent leg
- Off by default. One lower-weight, **separate-provider** voice asking only "what
  assumption / citation / alternative explanation did **all** the Claude seats miss?" —
  a tiebreaker, never a co-equal judge. The provider is the user's choice and is
  configured locally; the skill ships no provider wiring.
- Route only through a **no-train / retention-disabled** endpoint. If none is
  configured, **skip the leg and disclose it** — never fall back to a training-eligible
  free tier, and never imply cross-model coverage that did not happen.

## The scientific-integrity failure modes Act II must not commit
These are the reasons the Act-II rails exist; keep them in view:
- **Fabricated numbers** → the Execution-Provenance Wall makes them impossible.
- **AI p-hacking / spec-search / HARKing** → the analysis-lock freezes the headline
  spec; new specs are added only as *labeled robustness checks reported alongside the
  original*; every spec run (including discarded) is logged to an immutable
  specification ledger; a HARKing detector flags hypothesis drift toward the data.
- **Result suppression** → removing/attenuating a result, narrowing a sample, dropping
  a control/observation, or weakening a caveat is a privileged, logged edit behind
  per-item author sign-off; a deterministic before/after diff of
  {coefficients, N, samples, caveats} routes any net removal to that gate.
- **Breaking a correct passage / introducing an error** → the fix-safety verifier and
  the no-collateral-damage diff (every changed span must trace to an approved finding).
- **Overfitting to reviewers** → "more likely to be accepted" is never a permitted
  justification for a substantive edit; validity dominates venue; reviewer suggestions
  are themselves prosecuted before they can drive an edit.

## Disclosure
The run auto-generates an **AI-involvement disclosure** from the audit trail
(everything the tool did: text edited, analyses re-run, citations added/verified), in
a long form and a paste-able short form. Filing it per the venue's policy is part of
the deliverable. Substantive scientific judgments are **proposed** by the tool and
**ratified by the human** — the author remains the accountable author.

## Labeling
If inputs were missing, a source could not be fetched, the baseline did not reproduce,
or the external leg was skipped, the deliverable says so. A degraded run is labeled,
never disguised.
