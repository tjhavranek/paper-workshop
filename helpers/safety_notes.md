# Safety notes, read before sending data anywhere or running code

## Data never leaves the machine without consent
- Act I and Act II run on Claude (the model already in your session) and locally.
  The **only** optional external call is the lower-weight dissent leg (below).
- **Model retention differs by model (as of June 2026).** Running the session on Claude
  Fable 5 means a Covered Model: inputs are retained for 30 days (used for safety defense
  only, not to train models), and zero-data-retention is **not** available for it. For
  manuscripts under strict confidentiality terms that require ZDR, run the session on a
  model that is not a Covered Model (the designation applies to the Mythos-class models;
  check Anthropic's current Covered Model list before promising ZDR).
- **Never send raw data externally**, under any circumstances. The dissent leg
  operates on abstracted findings/claims, never datasets.
- Before any web fetch (Phase C source-grounding) or any external-model call, warn the
  user what would be sent and to where, and get explicit, logged consent.
- Refuse embargoed / NDA / "no-AI-tools" material for anything that would transmit it.

## The optional external dissent leg
- Off by default. One lower-weight, **separate-provider** voice asking only "what
  assumption / citation / alternative explanation did **all** the Claude seats miss?", a tiebreaker, never a co-equal judge. The provider is the user's choice and is
  configured locally; the skill ships no provider wiring.
- Route only through a **no-train / retention-disabled** endpoint. If none is
  configured, **skip the leg and disclose it**, never fall back to a training-eligible
  free tier, and never imply cross-model coverage that did not happen.

## The scientific-integrity failure modes Act II must not commit
These are the reasons the Act-II rails exist. Where a rail is a deterministic, fail-closed
script it is named; the rest are LLM-judged on top, with author sign-off for anything that
touches the record.
- **Fabricated numbers** → the Execution-Provenance Wall. The Runner emits a provenance
  token for every value and the Scribe may only transcribe one; `helpers/provenance.py`
  re-hashes the named output artifact and confirms the value is present in it, and
  `helpers/consistency.py` confirms every transcribed value appears in the revised text and
  flags any changed number that has no token (an orphan). Both are deterministic, fail closed.
- **Result suppression** → removing/attenuating a result, narrowing a sample, dropping a
  control/observation, or weakening a caveat is a privileged edit behind per-item author
  sign-off. `helpers/integrity_diff.py` deterministically diffs {coefficients, N, samples,
  caveats} between the baseline and the revised manuscript and routes any net removal to that
  gate; the LLM `integrity` verification angle adds the semantic judgment a diff cannot make.
- **AI p-hacking / spec-search / HARKing** → "more likely to be accepted" is never a permitted
  justification for a substantive edit (triage and the Scribe allow `more-correct`/`clearer`
  only); a new specification is proposed only as a *labeled robustness check reported
  alongside the original* (lane C, proposal-only), never a silent swap; and the LLM
  `integrity` angle flags hypothesis-drift-toward-the-data. This one is **LLM-judged, not a
  deterministic ledger**, see `LIMITATIONS.md`.
- **Unreproducible numbers** → `helpers/reproduces.py` defines "reproduces" as code (per
  artifact class: float tolerance, fixed seeds), so the baseline gate and the package
  clean-room check are decided by a deterministic predicate, not an LLM's say-so.
- **Breaking a correct passage / introducing an error** → the fix-safety verifier, plus the
  rule that every changed span must trace to an approved finding (no collateral damage).
- **Overfitting to reviewers** → validity dominates venue; reviewer suggestions are themselves
  prosecuted (the Act-I panel) before they can drive an edit.

## Disclosure
The run auto-generates an **AI-involvement disclosure** from the audit trail
(everything the tool did: edits applied and queued, analyses re-run, proposals and
blocks), in a long form and a paste-able short form. Filing it per the venue's policy is part of
the deliverable. Substantive scientific judgments are **proposed** by the tool and
**ratified by the human**: the author remains the accountable author.

## Labeling
If inputs were missing, a source could not be fetched, the baseline did not reproduce,
or the external leg was skipped, the deliverable says so. A degraded run is labeled,
never disguised.
