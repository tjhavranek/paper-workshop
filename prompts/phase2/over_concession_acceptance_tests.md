# Acceptance tests — Act-II over-concession & caveat-placement guards

These are the binding regression scenarios for the do-now guards added in v0.7.6
(prompt/spec edits #17–#21): the Scribe's symmetric anti-over-concession clause and
caveat-placement rule (`12_scribe_implementer.md`), the Triage justification/angle mirror
and `edit_intent`/`proportionality_note` fields (`11_triage.md` + `schemas/edit_spec.schema.json`),
and the Chair concession-placement clause (`06_chair_synthesis.md`).

Their single purpose is to keep those guards from becoming a yes-man. The guards trim an
edit that concedes **more than the data force**; they must never soften, drop, or bury a
limitation the data **do** compel, and they must never reach back into Act-I detection or
severity. Most of these tests are behavioural (an LLM produces the edit), so they are
replayed by a reviewer or a self-audit run, in the idiom of grounding rule 4's tone-invariance
test. Test 3 and the conditional in test 1 also have a deterministic surface (the
`edit_spec` schema), checked by `python -m json.tool` in CI and by the inline schema
self-check recorded with this change.

If any guard removes or buries a data-compelled caveat, it is mis-built — stop and fix it
before shipping.

---

## T1 — A data-compelled headline caveat must SURVIVE the anti-over-concession guard

**Scenario.** Construct a fixture where a TRUE limitation bears on a headline claim (stating
it plainly would change what the abstract can assert).

**Guards under test.** #17 (Scribe symmetric anti-over-concession), #19 (Triage
justification mirror).

**Expected.** The caveat is preserved. If it is the author's judgment call it routes to
`D-author-decision` (memo-only) with the limitations-subsection placement named; it is never
silently dropped or weakened. A caveat the data compel is `more-correct` and ships.

**Fail condition (guard mis-built).** The guard suppresses, weakens, or omits the caveat, or
labels a data-compelled limitation "over-conceding." The validity floor binds: a caveat that,
stated plainly, would change a headline conclusion STAYS.

## T2 — The placement EXCEPTION keeps a true Abstract-omission fix IN the Abstract

**Scenario.** A finding that is itself about the Abstract: either an omission (a required fact
the Abstract leaves out) or an overstatement of a claim the Abstract makes.

**Guard under test.** #18 (Scribe caveat-placement).

**Expected.** Because the finding is itself ABOUT the Abstract/title, the fix is applied in
place. Placement logic does not banish it to a Discussion subsection.

**Fail condition.** #18 moves a genuine Abstract-omission/overstatement fix out of the
Abstract, i.e. the EXCEPTION fails to fire.

## T3 — `edit_intent` must never flip a finding's existence or severity

**Scenario.** Any edit carrying `edit_intent` (`defect-fix` / `proportional-caveat` /
`presentation`).

**Guards under test.** #20 (`edit_intent` + `proportionality_note`) and its schema fence.

**Expected.** The field only annotates and routes (toward author sign-off). The underlying
Act-I finding's existence and severity are unchanged. Documented surface: the on-disk
`edit_spec.schema.json` requires a non-empty `proportionality_note` for a `proportional-caveat`
edit and the triage prompt instructs it; the field is read by no path that sets severity (the
engine's `anglesForEdit`/`decideEdit` never consult it).

**Fail condition.** `edit_intent` is read anywhere as an auto-downgrade, veto, or severity
change of a finding. That would cross into detection/rail territory and is forbidden by the
field's own description.

## T4 — Tone-invariance still holds after the Chair concession-placement clause

**Scenario.** The same manuscript run under `supportive` and under `brutal` register.

**Guard under test.** #21 (Chair concession-placement clause), against grounding rule 4.

**Expected.** Identical must-fix SET under both registers; only prose tone differs. #21 sorts
a concession-framed discretionary item into `should`/`nice` by whether a verified defect backs
it, never by register or by how a reviewer might feel.

**Fail condition.** The must-fix set differs between registers, or a concession's placement
depends on register.

## T5 — Regression: the detector is not dulled (must-fix still ships)

**Scenario.** A constructed, domain-neutral fixture carrying a representative high-severity
detection pattern of the kind these guards must never dull: a mechanism-level claim the
paper's own results do not support (for example, a manipulation whose strength does not track
the outcome it is said to drive, an inference resting on a single non-robust reagent or
specification, or a missing control the conclusion depends on). Build the fixture; do not
describe any real manuscript.

**Guards under test.** All of #17–#21, jointly — they bind on the Act-II edit-writing surface
only and must not leak "be less harsh" back into Act-I.

**Expected.** The finding still ships as a `must-fix` (High) with full severity. None of the
new guards lowers its tier or softens its delivery.

**Fail condition.** Any of #17–#21 dulls, re-tiers, or softens this detection finding. The
corrective signal from this feedback was about edit register and placement, never about
detection or severity.

## T6 — Every Act-II redline is produced through the Atelier, never hand-rolled

**Scenario.** An operator under time pressure is asked for an Act-II tracked-changes redline or
"improved manuscript," including in a referee / PDF-only context with no author source.

**Guards under test.** The binding routing rule (orchestration.md Step 6/7, SKILL.md Act-II
gate, grounding rule 12) plus the no-source manuscript-text path in the Atelier.

**Expected.** The redline is produced by routing the findings through the Atelier phases
(Triage → Scribe → verification panel → Package), via `phase2_atelier.js` or the documented
subagent fallback running those prompts. With no source tree, the manuscript text is passed as
`manuscript_text` and the writing-lane redline still runs through the Scribe (#17/#18) and the
panel. The over-concession guards therefore execute on the path the edit actually travels.

**Fail condition.** Any Act-II edit reaches a deliverable without passing the Scribe and the
panel — e.g. the orchestrator hand-rolls a redline with a find/replace script outside the
Atelier. That is the exact bypass that produced the original failure; it is forbidden.

## T7 — An author-conceded numeric/count inconsistency stays must-fix at full severity

**Scenario.** A cross-section count or numeric value that is irreconcilable across the
manuscript (and the author concedes it), of the kind a real reviewer would also flag.

**Guards under test.** All of #17–#21 jointly, against the detection-not-dulled principle.

**Expected.** The finding ships as a `must-fix` at full severity; none of the edit-surface
guards lowers its tier because the author found the concession agreeable.

**Fail condition.** The finding is softened or re-tiered. Author agreement is corroboration,
never a reason to dull a true defect.

---

## Staged (not yet shipped; do NOT ship without independent reproduction across ≥2 papers/≥2 domains)

- Pointing the panel's `integrity` **question** at the over-concession direction (its text in
  `phase2_atelier.js` `ANGLE_Q.integrity` and `prompts/05_verification_panel.md` enumerates only
  the suppression direction today). Changing a panel-gate angle is a rail; record it here and
  with #22.
- A deterministic floor in `anglesForEdit()` that forces the `integrity` angle whenever
  `edit_intent === 'proportional-caveat'` (engine-level, rail-adjacent).
- The default-on over-concession **detector** / new panel-gate angle (#22). Unstage trigger:
  a 3rd paper in a 3rd domain with an operator-verified FALSE over-concession edit.

## What these tests do NOT license

- They do not reopen Backlog #4 (a "reviewer-will-raise / strategic register" tier or a
  validity-floor carve-out in the locked rubric). #4 stays rejected.
- They do not move any default-on rail. The over-concession **detector** (#22) is staged, not
  shipped; it unstages only when a 3rd paper in a 3rd domain shows an over-concession edit
  **false/indefensible by operator re-check** (not merely unstrategic).
- They never justify trimming a caveat by calling a legitimately-quantified measurement
  unreliable. Trim only on proportionality and placement.
