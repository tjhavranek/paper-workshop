# CRUCIBLE: the `paper-workshop` skill

[![ci](https://github.com/tjhavranek/paper-workshop/actions/workflows/ci.yml/badge.svg)](https://github.com/tjhavranek/paper-workshop/actions/workflows/ci.yml)

Imagine a panel of the world's leading experts, assembled for your exact paper, arguing it out
from rival schools and then rebuilding it themselves, re-running your own code so every revised number is regenerated, not retyped.

**An adversarial expert workshop that turns its critique into the edits that answer it: a
tracked redline, a clean draft, and a replication package, before you submit.**

*One tool, two names: `paper-workshop` is the repo you install and the phrase you type;
**CRUCIBLE** is what you'll see in the report headers.*

CRUCIBLE convenes a panel of AI referees built specifically for *your* manuscript and makes
them **argue with each other** from rival schools of thought, grounding every criticism in an
exact quote (no invented objections, no confidence theater). Then, if you want, it
**implements the agreed fixes**: a tracked-changes redline, a clean revised version, your
analysis code **re-run to regenerate every affected number**, and a reproducible replication package.

Two things are mechanically checked: every criticism is pinned to a real quote, and every revised number
is produced by a real re-run of your own code. It is equally plain about the rest: effectiveness
is not measured yet (no recall or false-positive numbers). We have run the workshop on more than ten
papers in our own work, but only one is public (an accepted paper from the authors' own group; see
[`examples/incentives-workshop`](examples/incentives-workshop)), where Act II is demonstrated
end-to-end once; none of it is a controlled validation. Read the [limitations](LIMITATIONS.md)
before you rely on it.

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
- **Every comment is re-checked from many angles** (Roundtable and up) by independent blind
  verifiers (does the quote exist, does the criticism actually follow, is the severity
  calibrated, does the proposed fix break something) before it ever reaches you; Desk Review,
  the lightest mode, is a single-pass read with inline chair checks instead of the panel.
- **It also argues FOR your paper.** Every full tribunal run also staffs a contribution rival
  pair: an *overclaim prosecutor* hunting where your framing outruns the evidence, and a
  *contribution maximizer* hunting the opposite failure, the bolder claim your own results
  defensibly support but your paper never makes. The maximizer's candidates clear two
  deterministic gates and arrive as a separate, non-blocking **Contribution Memo** of at most
  3 items: suggestions for you to ratify or ignore, never must-fixes. At Workshop depth and
  above a related-literature scout also looks past your own bibliography for overlooked work,
  under a strict fetch-or-drop rule: a work it could not actually open is never cited as
  evidence. The two gates' internals and what the scout does not certify are in
  [`LIMITATIONS.md`](LIMITATIONS.md).
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
Review** mode) do that. CRUCIBLE is for when you want the argument *and* the rebuild.

**See it on a real paper.** [`examples/incentives-workshop`](examples/incentives-workshop) is CRUCIBLE
run end to end on an accepted JPE-Microeconomics meta-analysis: a topic-built referee panel that argues,
then a re-run of the authors' own Stata and R that regenerated the data byte-for-byte identical, with a
deterministic provenance proof. ([`examples/self-audit`](examples/self-audit) is the tool run on its own design.)

**Limits.** **[`LIMITATIONS.md`](LIMITATIONS.md)** is the straight account of
what is genuinely enforced and what is not proven yet: no measured recall or false-positive
numbers; same-model decorrelation is a design bet, not a proof; coverage means *attention*,
not correctness; and the Contribution Memo's selection is same-model judgment with no measured
undersell-recall yet. Act II is built, [unit-tested](.github/workflows/ci.yml), and **demonstrated end-to-end once** on a
real accepted paper ([`examples/incentives-workshop`](examples/incentives-workshop)), a
demonstration and not independent validation; re-derive any regenerated number yourself. A
pre-release self-audit caught real overclaims and a quote-gate bug, both fixed
([`examples/self-audit/`](examples/self-audit/)); a development pass, not validation.

## Modes: pick your depth

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
feature: on by default on Max; on Pro, switch them on in `/config`), CRUCIBLE uses them to run
the same phases more efficiently; if they're off, Symposium and Summit run at Workshop depth
and CRUCIBLE tells you rather than downgrading silently. Engine detection, model and context
inheritance, and the 1M-context account caveat and its remedies live in the pre-flight,
[`helpers/doctor.md`](helpers/doctor.md).

**Running on Claude Fable 5 (mythos-class).** In the default mode the fleet inherits the
session model, so starting the session on Claude Fable 5 (Anthropic's mythos-class tier, the
class above Opus) lifts every seat, verifier, and chair to that capability with no
configuration; `/model best` (Claude Code v2.1.170+) picks Fable where your plan has it and
the latest Opus where it does not. Anthropic's Fable 5 prompting guidance favors separate
fresh-context verifier subagents over self-critique, which matches CRUCIBLE's verification
panel: a design endorsement, not a measured gain. For biology- or security-flavored papers,
start on Opus deliberately, because a safety classifier can reroute Fable to Opus 4.8 mid-run;
starting on Opus keeps the run on one model. The run records which model actually served, and
the report discloses it. Fable's other June 2026 constraints (30-day input retention with no
zero-data-retention, twice Opus pricing) are in [`helpers/doctor.md`](helpers/doctor.md) and
[`helpers/safety_notes.md`](helpers/safety_notes.md). The workshop runs unchanged on Opus and
Sonnet; the methodology does not depend on the model tier.

**Running on a usage-constrained plan: the economy register.** A default Workshop inherits the
session model into every agent, and on Fable that can exhaust a usage-capped plan's window
mid-run; a locked-out run delivers zero findings. Saying "economy" casts the run in tiers
(judgment seats at the Opus floor, mechanical phases on Sonnet, scout/chair/scribes at the
session model), with every deterministic rail unchanged, the cast recorded in `meta.json` and
the report header, and a never-upgrade clamp so economy can lower a run's cost but never raise
it. The pre-flight ([`helpers/doctor.md`](helpers/doctor.md)) shows a cost preview and offers it
before any Workshop-or-larger launch. The anchor so far is one real Workshop-band field run:
3.70M subagent tokens in 55 minutes, well inside a Max-plan window, delivering a 60-finding
verified ledger; one run's evidence, not blind validation (see [`LIMITATIONS.md`](LIMITATIONS.md)).

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

CRUCIBLE grew out of the authors'
[`mad-research`](https://github.com/tjhavranek/mad-research) (a cross-model audit that produces
a memo) and
[`research-audit-duel-protocol`](https://github.com/tjhavranek/research-audit-duel-protocol)
(manual multi-model protocols). It inherits their discipline (a locked severity rubric,
quote-and-locate grounding, a preserved minority report, no confidence scores, read-only
treatment of your files) and adds the topic-adapted debating fleet and the rebuild. It
complements `mad-research` rather than replacing it: `mad-research` is a fast cross-model
(Claude + Codex) audit memo, while CRUCIBLE is a deeper Claude-only fleet that can also rebuild
the paper. For an important project, run both in parallel and compare.
(`mad-research`'s own small blinded comparison, n = 5 meta-analyses, found a Claude-only
configuration ranked above its cross-model setup by an independent judge: illustrative, not
proof. CRUCIBLE is Claude-only by design, and a single optional non-Claude "what did we all
miss?" pass is available for those who configure it.)

A lighter sibling by the same author group,
[`erc-ai-feedback`](https://github.com/tjhavranek/erc-ai-feedback), is a rubric-based pre-review
for ERC Starting and Consolidator grant proposals, run in a single chat session. It only flags
problems and leaves the drafting to the applicant, whereas CRUCIBLE argues a paper out and, if
you want, rebuilds it: one is built for proposals, the other for papers.

## What it deliberately will not do

No fabricated citations, numbers, quotes, data, or results. No confidence or acceptance-odds
numbers. No silent edits; changes arrive as tracked redlines on copies for you to accept. No
number in the revised paper that a logged re-run didn't produce. No automatic merge,
submission, or data release. The author remains the author.

## License & citation

CC-BY-4.0 ([`LICENSE`](LICENSE)). If it helps your work, please cite:

> Havranek, T. & Irsova, Z. (2026). *CRUCIBLE (`paper-workshop`): an adversarial multi-expert
> workshop that stress-tests and rebuilds a research paper.* GitHub. https://github.com/tjhavranek/paper-workshop
