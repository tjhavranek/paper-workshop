# CRUCIBLE — the `paper-workshop` skill

Imagine a panel of the world's leading experts, assembled for your exact paper, arguing it out
from rival schools and then rebuilding it themselves, re-running your own code so the numbers are real.

**An adversarial expert workshop that doesn't stop at the critique. It hands back the edits
that answer each objection: a tracked redline, a clean draft, and a replication package,
before you submit.**

> **One skill, said two ways.** `paper-workshop` is the repo you install and the phrase you
> type to run it. **CRUCIBLE** is its name, the one you'll see in the report headers; there is
> no separate tool.

CRUCIBLE convenes a panel of AI referees built specifically for *your* manuscript and makes
them **argue with each other** from rival schools of thought, grounding every criticism in an
exact quote (no invented objections, no confidence theater). Then, if you want, it
**implements the agreed fixes**: a tracked-changes redline, a clean revised version, your
analysis code **re-run so the numbers are real**, and a reproducible replication package.

It is for researchers who want more than a list of complaints. You want the *sharpest*
objection a top referee would raise, argued from more than one angle, plus the *actual edits*
that answer it before you submit.

It earns trust at the seams: every criticism is pinned to a real quote, and every revised number
is produced by a real re-run of your own code. It is equally plain about the rest: effectiveness
is not measured yet, and Act II has been demonstrated end-to-end only once (one accepted paper,
the authors' own group; see [`examples/incentives-workshop`](examples/incentives-workshop)), not
broadly validated. Read the [honest limits](LIMITATIONS.md) before you rely on it.

A [Claude Code](https://claude.com/claude-code) skill. Claude-only. Runs on any paid plan.

---

## What makes it different

Good AI paper-reviewers already exist: multi-agent review, grounded critique, and
topic-adaptive reviewers are all prior art, and dedicated citation-checkers triangulate more
reference databases than CRUCIBLE's web-based check does. CRUCIBLE's bet is a pairing
existing tools rarely offer in one run: reviewers that genuinely **debate** from opposed
objective functions, and an integrated **rebuild** that re-runs your analysis and hands back
a corrected, reproducing manuscript.

- **The referees argue.** Every contested choice in your paper is taken up by at least two
  experts from *rival traditions* with *opposite jobs*: one tries to break it, one tries to
  defend it. You see the real disagreement and the crux instead of a bland averaged verdict.
- **The panel is built from your paper.** A scout reads your manuscript and assembles the
  specific experts it needs (your identification strategy, your estimator, publication bias,
  your benchmark, your proof), plus generalists who ask "does this even matter?" and "would a
  smart outsider follow it?"
- **Nothing is made up.** Every criticism cites an exact quote, checked by a deterministic
  script rather than the model's memory, and the most load-bearing **cited works are fetched**
  so the paper's claims about them are checked against the originals. What can't be verified is
  flagged *needs author confirmation* and never asserted. No acceptance-probability numbers, ever.
- **Every comment is re-checked from many angles** by independent blind verifiers (does the
  quote exist, does the criticism actually follow, is the severity calibrated, does the
  proposed fix break something) before it ever reaches you.
- **It also argues FOR your paper.** Every full tribunal run staffs a contribution rival
  pair: an *overclaim prosecutor* hunting where your framing outruns the evidence, and a
  *contribution maximizer* hunting the opposite failure, the bolder claim your own results
  defensibly support but your paper never makes. The maximizer's candidates ride two
  deterministic gates (the under-leveraged result must be quoted; a probe search confirms
  no refuting phrasing of the bolder claim occurs in your text, with the semantic call left
  to a steelman verifier) and arrive as a separate, non-blocking **Contribution
  Memo** of at most 3 items: suggestions for you to ratify or ignore, never must-fixes. At
  Workshop depth and above, a related-literature scout widens the lens past your own
  bibliography, deliberately hunting overlooked work (adjacent fields, older papers,
  working-paper series), under a strict fetch-or-drop rule: a work it could not actually
  open is never cited as evidence (a mandate the scout follows, not a script; see
  [`LIMITATIONS.md`](LIMITATIONS.md)).
- **It rebuilds the paper itself.** The opt-in second act (the **ATELIER**) turns the agreed
  findings into a tracked-changes **redline** *and* a **clean revised version**, **re-runs
  your own code** to regenerate the affected numbers, tables, and figures, and assembles a
  **replication package**, under one hard rule: *no number enters your paper unless a real,
  logged re-run produced it* (enforced by deterministic provenance and consistency checks).
  Every change is mapped to the reviewer concern it answers.
- **You stay in control.** It works on copies, never your originals. Anything that touches a
  number, a sample, a claim, or a result waits for your sign-off. It never edits your only
  copy, never submits, never releases data.

If you only want a fast referee-style critique, lighter tools (and CRUCIBLE's own **Desk
Review** mode) do that. CRUCIBLE earns its keep when you want the argument *and* the rebuild.

**See it on a real paper.** [`examples/incentives-workshop`](examples/incentives-workshop) is CRUCIBLE
run end to end on an accepted JPE-Microeconomics meta-analysis: a topic-built referee panel that argues,
then a re-run of the authors' own Stata and R that regenerated the data byte-for-byte identical, with a
deterministic provenance proof. ([`examples/self-audit`](examples/self-audit) is the tool run on its own design.)

**Honesty about limits.** See **[`LIMITATIONS.md`](LIMITATIONS.md)** for a straight account of
what is genuinely enforced and what is not proven yet: no measured recall or false-positive
numbers yet; same-model decorrelation is a design bet, not a proof; coverage means *attention*,
not correctness; and the Contribution Memo is a gate-anchored option set whose selection is
still same-model judgment, with no measured undersell-recall yet. Act II is built, unit-tested, and **demonstrated end-to-end once** on a real
accepted paper (see [`examples/incentives-workshop`](examples/incentives-workshop): both the
Stata and R paths re-executed, the headline reproduced), though on one paper from the authors'
own group, so it is a demonstration and not independent validation; re-derive any
regenerated number yourself. We ran CRUCIBLE on its own
design before release, and it caught real overclaims and a bug in its own quote-gate, both
fixed; a later self-audit of the shipped version is in
[`examples/self-audit/`](examples/self-audit/), framed as a development pass, not
independent validation.

## Modes: pick your depth (Desk Review through Workshop run at full depth on any paid plan)

| Mode | What convenes | Experts | ≈ agents | Best for |
|---|---|---|---|---|
| **Desk Review** | one expert pass, no fleet | a few lenses | ~1–6 | a fast read; lightest setup |
| **Roundtable** | a small adversarial panel | 6–8 | ~20–30 | a quick but real workshop |
| **Workshop** *(default)* | the full adversarial workshop | 12–18 | ~45–65 | serious pre-submission review |
| **Symposium** | a large fleet + close-readers | 25–40 | ~90–250 | top-venue preparation |
| **Summit** | every subsystem, every sentence | 60–120+ | ~300–600 | the most exhaustive pass (opt-in) |

*(Symposium/Summit also scale with paper length and are best run with dynamic workflows enabled; without them they fall back to Workshop depth.)*

**Running it often is fine.** Desk Review and Roundtable are light (single-digit to ~30 agents)
and the default Workshop is a few dozen — cheap enough to re-run as you revise a paper. Reserve
Symposium/Summit for a major pre-submission pass.

**Engine.** The workshop runs on subagents (helper Claude sessions your main session spawns),
which work on every plan. When dynamic workflows are available (a Claude Code orchestration
feature: on by default on Max; on Pro, switch them on in `/config`), CRUCIBLE uses them
to orchestrate those same subagent phases more efficiently; if they're off, Symposium and
Summit run at Workshop depth and CRUCIBLE tells you rather than downgrading silently. **Desk
Review** needs neither, so it works anywhere. CRUCIBLE
runs at full power on Max, with nothing capped. Either engine's agents inherit the orchestrating
session's model and context by default (the opt-in economy register below is the one
exception), so dynamic workflows do not bypass the one account caveat: a
large-context (1M) session may need usage credits enabled for that tier, or just run the session
on a standard-context model (`/model sonnet`), which keeps the methodology identical. Neither
weakens the tool (see [`helpers/doctor.md`](helpers/doctor.md)).

**Running on Claude Fable 5 (mythos-class).** In the default mode, that same inheritance means
starting the session on
Claude Fable 5 (Anthropic's mythos-class tier, the class above Opus) lifts every seat, verifier,
and chair to that capability with no configuration: select it with `/model best` in Claude Code
v2.1.170 or later, which picks Fable where your plan has it and the latest Opus where it does not.
Anthropic's prompting guidance for Fable 5 describes the pattern this skill is built on: it states
that separate, fresh-context verifier subagents tend to outperform self-critique, which matches
CRUCIBLE's verification panel. We cite that as a design endorsement, not as a measured improvement;
we have not measured one.

The honest constraints, as of June 2026. Fable 5 carries safety classifiers that can silently drop
a flagged session back to Opus 4.8, and the session then stays on Opus until you re-select Fable;
for substantive biology work expect nearly all requests to reroute, so for biology- or
security-flavored papers start on Opus 4.8 deliberately (see
[`helpers/doctor.md`](helpers/doctor.md); the run records which model actually served, and the
report discloses it). Fable 5 is a Covered Model: inputs are retained for 30 days (for safety
defense only, not training) and zero-data-retention is not available, which matters for
unpublished manuscripts (see [`helpers/safety_notes.md`](helpers/safety_notes.md)). It is priced at
twice Opus. The workshop runs unchanged on Opus and Sonnet; the methodology does not depend on the
model tier.

**Running on a usage-constrained plan: the economy register.** A default Workshop run inherits
the session model into every agent, and on Fable that can exhaust a usage-capped plan's window
before the run finishes — a locked-out run delivers zero findings. Saying "economy" casts the
fleet in two tiers instead: judgment layers (seats, generalists, premortem, integrators, the
verification panel, Act II's runner/triage/reconciler/package) at the Opus floor, mechanical
phases (cartography, grounding, gate relays, completeness, Act II intake/staging/disclosure)
on Sonnet, with the scout, the chair, and Act II's scribes always at the session model. Every
deterministic rail is unchanged, the cast is recorded in `meta.json` and stated in the report
header, and an unavailable model falls back to inheritance with the fallback logged. The
measured anchor so far: one real Workshop-band field run at this cast recorded its 37-agent
tribunal workflow at 3.70M subagent tokens in 55 minutes (Act I totaled 39 agents and
delivered a 60-finding verified ledger, 11 High) — well
inside a Max-plan window. That is one run's evidence, not blind validation; see
[`LIMITATIONS.md`](LIMITATIONS.md). The pre-flight (`helpers/doctor.md`) shows a cost preview
and offers economy before any Workshop-or-larger launch, so the choice is informed either way.

## Install

```bash
# 1. Claude Code installed; Python 3.8+ on PATH (for the deterministic quote/number checks).
# 2. Make the skills dir (it may not exist yet) and clone into it:
mkdir -p ~/.claude/skills
git clone https://github.com/tjhavranek/paper-workshop ~/.claude/skills/paper-workshop
# 3. Restart Claude Code, then confirm it loaded with a quick pass on any PDF:
#      workshop my paper: some.pdf   desk review
```

Windows (PowerShell; if `python` isn't found, the `py -3` launcher or a conda Python works too):

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
git clone https://github.com/tjhavranek/paper-workshop "$env:USERPROFILE\.claude\skills\paper-workshop"
# then restart Claude Code and confirm:  workshop my paper: some.pdf   desk review
```

For the rebuild (Act II) you also need the interpreters your analysis uses (R / Python /
Stata), `latexmk` (LaTeX) or the bundled `docx` skill (Word), and `git`.

## Use

Type these into a Claude Code session (run `claude` in a terminal to open one):

```
workshop my paper: mypaper.pdf  desk review     # the lightest pass, one expert (good first run)
workshop my paper: mypaper.pdf                 # default Workshop mode, supportive register
workshop my paper: mypaper.pdf  roundtable     # a quick adversarial pass
workshop my paper: mypaper.pdf  summit brutal  # the most exhaustive pass, brutal register
CRUCIBLE mypaper.pdf  symposium                 # the brand name works as a trigger too
```

CRUCIBLE runs the workshop and presents the report. Then it **stops and asks** whether to
implement the changes; if you say yes, it requests your source, data, and code and produces the
redline, the clean version, and the replication package. *Register* (`supportive` / `brutal`)
changes only the tone of the write-up; the severity of a finding never changes.

## Lineage

CRUCIBLE is the successor to the authors'
[`mad-research`](https://github.com/tjhavranek/mad-research) (a cross-model audit that produces
a memo) and
[`research-audit-duel-protocol`](https://github.com/tjhavranek/research-audit-duel-protocol)
(manual multi-model protocols). It inherits their discipline (a locked severity rubric,
quote-and-locate grounding, a preserved minority report, no confidence scores, read-only
treatment of your files) and adds the topic-adapted debating fleet and the rebuild.
(`mad-research`'s own small blinded comparison, n = 5 meta-analyses, found a Claude-only
configuration ranked above its cross-model setup by an independent judge: illustrative, not
proof. CRUCIBLE is Claude-only by design, and a single optional non-Claude "what did we all
miss?" pass is available for those who configure it.)

## What it deliberately will not do

No fabricated citations, numbers, quotes, data, or results. No confidence or acceptance-odds
numbers. No silent edits; changes arrive as tracked redlines on copies for you to accept. No
number in the revised paper that a logged re-run didn't produce. No automatic merge,
submission, or data release. The author remains the author.

## License & citation

CC-BY-4.0 ([`LICENSE`](LICENSE)). If it helps your work, please cite:

> Havranek, T. & Irsova, Z. (2026). *CRUCIBLE (`paper-workshop`): an adversarial multi-expert
> workshop that stress-tests and rebuilds a research paper.* GitHub. https://github.com/tjhavranek/paper-workshop
