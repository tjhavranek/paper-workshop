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
- **Code where code is possible.** Several angles are backed by real deterministic,
  fail-closed scripts — not eyeballed judgments: `quote-locator` runs
  `helpers/quote_gate.py` and reports its result; for the quote-exempt absence classes
  (`absence-silence`, `contribution-undersell`) the verifier READS the certificate that
  `helpers/absence_gate.py` produced at the Phase-D barrier (attached to each finding as
  `absence_gate`; its hit snippets feed the steelman angle); and in Act II, `numeric-provenance` by
  `helpers/provenance.py` (re-hash the output artifact + confirm the value is in it),
  `consistency` by `helpers/consistency.py` (run-match every token value + flag orphans), the
  reproduction predicate by `helpers/reproduces.py` (per-class float tolerance), and the
  result-suppression half of `integrity` by `helpers/integrity_diff.py` (net-removal diff of
  {coefficients, N, samples, caveats}). The LLM verifier still runs on top for the semantic
  judgment a script cannot make — does the inference follow, is a quantity consistent across
  places by meaning, is an edit HARKing or spin — and that layer is LLM-audited and labeled as
  such in `LIMITATIONS.md`.
- **Aggregate in code, not by an LLM.** Verdicts are combined by the fixed rules
  below in the Workflow script — no model gets to "weigh" them.

## Act I — angles applied to every finding

| Angle | The question it asks | Hard gate? |
|---|---|---|
| `quote-locator` | Does the quote exist verbatim in the manuscript? (runs `quote_gate.py`, which checks 1:1 existence in paper.txt, not that the quote sits at the finding's stated locator, see `LIMITATIONS.md`; absence-class findings are instead certified by `absence_gate.py`, the probe-term search) | **Enforced by the standalone Quote-gate phase, not the panel aggregator** — fail (unmatched quote, or anything but a clean `absent` certificate) ⇒ status forced to `needs-author-confirmation`; the finding is **not** dropped |
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
list with the panel's reason. Delivered `contribution-undersell` findings take one
extra routing step: the engine feeds them to the chair through their own channel and
they can only land in the non-blocking `contribution_memo` (capped at 3), never in
the must-fix list — enforced in the Workflow script, not by instruction alone.

**Batched, not per-finding — this is what keeps the run feasible.** Each angle is run by
one blind agent (two redundant agents at the heavy tiers) that reviews the findings in
**batches** and returns a verdict *per finding*. So the panel costs
`angles × ceil(#findings / batch) × redundancy` agents — **never `#findings × angles`**,
which would explode with paper length. The batch size defaults to 25 (20 at `exhaustive`,
where the doubled redundancy already doubles each batch's reads; `args.batch` overrides,
clamped at 30 against attention dilution — field-validated at 25 on a real thorough run).
`quick` runs three angles (logical-validity,
fix-safety, steelman-charity); `thorough` runs six; `exhaustive`/`monumental` run all
seven with two redundant agents per angle (majority within an angle). The angle's
independence is preserved (one agent owns one angle, blind to the others); only the
wasteful one-agent-per-finding-per-angle fan-out is removed. The same shape applies in
Act II since v0.7.0: edit verification is batched by angle ACROSS edits
(`args.verify_batch`, default 12), never fanned out per edit.

**Severity-tiered angles (economy register only).** Under economy, Low-severity findings
are checked by the quick gate set (logical-validity, fix-safety, steelman-charity) plus
severity-calibration, while High/Medium findings get the tier's full set. This is safe
under the locked rubric, not a loosened rail: panel calibration can only LOWER a severity
(a Low has nowhere to go), Lows never drive the verdict or keep the deepening loop alive,
and every quote already rode the standalone deterministic gate. Severity-calibration rides
on Lows on purpose: it is the only angle that can flag a Low as under-rated for the chair
(the panel never raises a severity itself), so dropping it would remove the sole upgrade
channel; keeping it costs one extra angle on the minority Low batch. The hard
logical-validity gate and the steelman defense stay on every finding in every mode.

**The span-diet (experimental, opt-in inside the economy register only).** With
`span_diet: true`, the local-judgment angles (logical-validity, severity-calibration,
decision-relevance, fix-safety, factual-literature) read a per-batch EXCERPT file (each
finding's quote plus its surrounding context, copied verbatim by a slicer agent) and the
neutral precis instead of re-reading the full manuscript — the largest single input
saving on a long paper. The rails do not move: `quote-locator` still runs the
deterministic gate against the FULL paper.txt (the script reads the file, never the
agent), and `steelman-charity` ALWAYS receives the full manuscript in every mode, because
its question — does the paper already address this elsewhere? — is unanswerable from an
excerpt. A diet verifier that cannot adjudicate confidently from its excerpt is
instructed to return `cant-tell`, which the aggregator treats as fail-closed (never a
pass); a missing excerpt file falls back to the full text for that batch. Unvalidated so
far (no measured recall delta); that is why it is opt-in and labeled, not a default.

## Act II — angles applied to every edit (in addition to the Act-I angles on the originating finding)

| Angle | The question | Hard gate? |
|---|---|---|
| `numeric-provenance` | Does every number in this edit trace to a content-hashed output of a run executed **in this session**? (Execution-Provenance Wall) | **Yes** — fail ⇒ edit blocked |
| `consistency` | After this edit, does the value match **every** other place the same quantity appears (abstract/body/table/appendix)? | **Yes** — fail ⇒ edit blocked |
| `fix-safety` | Does the edit target the right span and avoid introducing a new error or breaking a correct passage? | **Yes** | 
| `integrity` | Does the edit suppress/attenuate a result, narrow a sample, drop a control/observation, weaken a caveat, swap the headline spec, or HARK? | **Yes** — fail ⇒ the edit is **blocked** and the finding routes back for a fresh proposal (independently, any `result-suppressing`/`claim-altering` **edit class** set at triage always waits for author sign-off, verdicts or no) |
| `human-voice` | Does the edit read as the author wrote it, not AI? (no negation-correction antithesis, no banned lexicon, no filler/over-signposting; punctuation matched to the author's baseline; verdict must quote an adjacent author sentence + a style diff) | **Yes** — fail ⇒ edit blocked |
| `logical-validity`, `factual-literature`, `steelman-charity` | (as in Act I, re-asked against the *edited* text) | mixed |

**Delivery rule (Act II).** An edit is auto-applied (as a tracked change on a copy)
**only** if its `edit_class` is `presentation` or `additive-verified` **and** every
hard-gate angle passes. Any `numeric`, `result-suppressing`, or `claim-altering`
edit — even when all verifiers pass — is **proposed**, not applied, and waits for the
author's per-item sign-off (grounding rule 14). A failing hard gate blocks the edit
and routes the underlying finding back for a fresh proposal. The deterministic
reconciler backstops a triage misclassification: an edit that changed a number without
a provenance token surfaces there as an orphan, and a dirty reconcile halts the run
before any "final" package is assembled.

## What the panel writes

Every verdict is a `verification.schema.json` object. The Act-I workflow returns each
delivered finding with its `panel_verdicts` attached plus the `rejected_in_panel` list,
and the orchestrator persists these to the session under `verification/` when it
assembles the report (orchestration.md Step 5); Act II returns each edit's verdicts the
same way (under `phase2/verification/`). The Workflow engine additionally retains every
verifier agent's full transcript. Together these are the auditable record: the author
can see exactly which angles cleared each comment and each change, and why anything
was rejected or revised.
