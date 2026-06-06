# The verification panel — many angles, before delivery

> **Nothing reaches the author until several independent subagents, each from a
> different angle, have checked it.** This applies to every comment in Act I and
> every implemented change in Act II (grounding rule 8). It is the feature that
> lets the tool be monumental without being a confident-nonsense generator.

The panel is **not** the same as the Act-I red-team phase (which *produces*
adversarial findings). The panel *audits* candidate outputs — findings and edits
— and decides, by recorded verdicts, what is allowed out the door.

## Principles

- **Blind.** Each verifier sees the candidate finding/edit and the manuscript (and,
  for Act II, the run artifacts) — but **not** the proposer's private rationale and
  **not** the other verifiers' verdicts. Independence is the whole point; a verifier
  that can see another's verdict is contaminated.
- **One angle per verifier.** A verifier judges from exactly one angle and stays in
  its lane. Different angles catch different failure classes; mixing them lets a
  verifier rationalize.
- **Adversarial by construction.** At least one angle (`steelman-charity`) is tasked
  to *defend the paper* — to show the criticism is wrong because the paper already
  handles it. A finding that cannot survive a determined defense should not ship.
- **Code where code is possible.** The `quote-locator` angle is backed by a real
  deterministic script (`helpers/quote_gate.py`) — the verifier runs it and reports its
  output, not an eyeballed judgment. The Act-II `numeric-provenance` and `consistency`
  angles are **LLM-audited** (an agent inspects the run artifacts and the manuscript): they
  are far stronger than a single proposer's say-so, but they are not yet a standalone
  deterministic script, and we label them as such. (Hardening them into scripts —
  a re-hash of every transcribed value, a numeric cross-reference grep — is on the roadmap.)
- **Aggregate in code, not by an LLM.** Verdicts are combined by the fixed rules
  below in the Workflow script — no model gets to "weigh" them.

## Act I — angles applied to every finding

| Angle | The question it asks | Hard gate? |
|---|---|---|
| `quote-locator` | Does the quote exist verbatim at the stated location? (runs `quote_gate.py`) | **Enforced by the standalone Quote-gate phase, not the panel aggregator** — fail ⇒ status forced to `needs-author-confirmation`; the finding is **not** dropped; absence-silence findings are exempt |
| `logical-validity` | Does the criticism actually *follow* from the quoted text? (catches a real quote + an invalid inference) | **Yes** — fail ⇒ reject |
| `factual-literature` | Is the norm/method/citation the finding appeals to actually correct? (checked against fetched sources, never memory) | No — fail ⇒ revise or reject |
| `severity-calibration` | Is the severity calibrated under `rubric.md` — neither inflated nor deflated? | No — fail ⇒ revise severity (never silently; recorded) |
| `decision-relevance` | Would fixing this change a number, a conclusion, or only presentation? Is it non-trivial? (the finding-killer) | No — fail ⇒ demote to `nice` or reject as trivial |
| `steelman-charity` | Can the paper be defended — does it already address this elsewhere, or is the criticism mistaken? | No — strong defense ⇒ reject |
| `fix-safety` | Would the `proposed_fix` introduce a NEW error or break a correct passage? | **Yes (for the fix)** — fail ⇒ the fix is withheld/flagged even if the finding stands |

**Delivery rule (Act I).** A finding is delivered iff: the hard-gate logical-validity
holds; AND it is not killed by a strong steelman defense or judged trivial by
decision-relevance; AND severity is set to the **most conservative** value among the
upheld `upheld-with-revision` verdicts. A failed `quote-locator` does **not** delete
the finding — it forces `verification_status = needs-author-confirmation` (per
rubric.md, status annotates, never vetoes severity). Findings the panel rejects are
not discarded silently — they are written to the synthesis `rejected_suggestions`
list with the panel's reason.

**Batched, not per-finding — this is what keeps the run feasible.** Each angle is run by
one blind agent (two redundant agents at the heavy tiers) that reviews the findings in
**batches** and returns a verdict *per finding*. So the panel costs
`angles × ceil(#findings / batch) × redundancy` agents — **never `#findings × angles`**,
which would explode with paper length. `quick` runs three angles (logical-validity,
fix-safety, steelman-charity); `thorough` runs six; `exhaustive`/`monumental` run all
seven with two redundant agents per angle (majority within an angle). The angle's
independence is preserved (one agent owns one angle, blind to the others); only the
wasteful one-agent-per-finding-per-angle fan-out is removed.

## Act II — angles applied to every edit (in addition to the Act-I angles on the originating finding)

| Angle | The question | Hard gate? |
|---|---|---|
| `numeric-provenance` | Does every number in this edit trace to a content-hashed output of a run executed **in this session**? (Execution-Provenance Wall) | **Yes** — fail ⇒ edit blocked |
| `consistency` | After this edit, does the value match **every** other place the same quantity appears (abstract/body/table/appendix)? | **Yes** — fail ⇒ edit blocked |
| `fix-safety` | Does the edit target the right span and avoid introducing a new error or breaking a correct passage? | **Yes** | 
| `integrity` | Does the edit suppress/attenuate a result, narrow a sample, drop a control/observation, weaken a caveat, swap the headline spec, or HARK? | **Yes** — any ⇒ route to author sign-off, never auto-apply |
| `human-voice` | Does the edit read as the author wrote it, not AI? (no negation-correction antithesis, no banned lexicon, no filler/over-signposting; punctuation matched to the author's baseline; verdict must quote an adjacent author sentence + a style diff) | **Yes** — fail ⇒ edit blocked |
| `logical-validity`, `factual-literature`, `steelman-charity` | (as in Act I, re-asked against the *edited* text) | mixed |

**Delivery rule (Act II).** An edit is auto-applied (as a tracked change on a copy)
**only** if its `edit_class` is `presentation` or `additive-verified` **and** every
hard-gate angle passes. Any `numeric`, `result-suppressing`, or `claim-altering`
edit — even when all verifiers pass — is **proposed**, not applied, and waits for the
author's per-item sign-off (grounding rule 14). A failing hard gate blocks the edit
and routes the underlying finding back for a fresh proposal.

## What the panel writes

Every verdict is a `verification.schema.json` object, persisted to the session under
`verification/` (Act I) or `phase2/verification/` (Act II). These transcripts are
part of the auditable record: the author can see exactly which angles cleared each
comment and each change, and why anything was rejected or revised.
