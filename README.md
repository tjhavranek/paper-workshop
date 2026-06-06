# CRUCIBLE — the `paper-workshop` skill

> *Every paper leaves changed.*

**An adversarial expert workshop for your paper — that then helps you actually fix it.**

> **One skill, said two ways.** `paper-workshop` is the repo you install and the phrase you
> type to run it; **CRUCIBLE** is its name — you'll see it in the report headers. There is no
> separate tool.

CRUCIBLE convenes a panel of AI referees built specifically for *your* manuscript, makes
them **argue with each other** from rival schools of thought, grounds every criticism in
an exact quote (no invented objections, no confidence theater), and then — if you want —
**implements the agreed fixes**: a tracked-changes redline, a clean revised version, your
analysis code **re-run so the numbers are real**, and a reproducible replication package.

It is for researchers who want more than a list of complaints. You want the *sharpest*
objection a top referee would raise, argued from more than one angle — and the *actual
edits* that answer it, before you submit.

A [Claude Code](https://claude.com/claude-code) skill. Claude-only. Runs on any paid plan.

---

## What it does that a single AI review doesn't

- **The referees argue.** Every contested choice in your paper is taken up by at least two
  experts from *rival traditions* with *opposite jobs* — one tries to break it, one tries
  to defend it. You see the real disagreement and the crux, not a bland averaged verdict.
- **The panel is built from your paper.** A scout reads your manuscript and assembles the
  specific experts it needs — your identification strategy, your estimator, publication
  bias, your benchmark, your proof — plus generalists who ask "does this even matter?" and
  "would a smart outsider follow it?"
- **Nothing is made up.** Every criticism cites an exact quote, checked by a deterministic
  script rather than the model's memory; and the most load-bearing **cited works are
  fetched** so the paper's claims about them are checked against the originals. What can't
  be verified is flagged *needs author confirmation*, never asserted. No
  acceptance-probability numbers, ever.
- **Every comment is re-checked from many angles** by independent blind verifiers (does the
  quote exist, does the criticism actually follow, is the severity calibrated, does the
  proposed fix break something) before it ever reaches you.
- **It rebuilds the paper — it doesn't just review it.** Opt-in second act (the **ATELIER**):
  CRUCIBLE turns the agreed findings into a tracked-changes **redline** *and* a **clean accepted
  version**, **re-runs your own code** to regenerate the affected numbers, tables, and figures,
  and assembles a **replication package** — under one hard rule: *no number enters your paper
  unless a real, logged re-run produced it* (enforced by deterministic provenance and consistency
  checks). Every change is mapped to the reviewer concern it answers. (The rebuild engine is
  built and unit-tested but **not yet field-proven end-to-end on a real paper** — see Limits.)
- **You stay in control.** It works on copies, never your originals. Anything that touches a
  number, a sample, a claim, or a result waits for your sign-off. It never edits your only
  copy, never submits, never releases data.

## Where it fits

Good AI paper-reviewers already exist — multi-agent review, grounded critique, and
topic-adaptive reviewers are all prior art, and dedicated citation-checkers triangulate
more reference databases than CRUCIBLE's web-based check does. CRUCIBLE's bet is the
combination two of them rarely make together:

1. **Reviewers that genuinely debate** from opposed objective functions and rival
   traditions — adversarial *collaboration*, not N independent reviews averaged; and
2. **An integrated rebuild** that re-runs your analysis and hands back a corrected,
   reproducing manuscript — so you leave with a redline and a clean draft, not a to-do list.

If you only want a fast referee-style critique, lighter tools (and CRUCIBLE's own **Desk
Review** mode) do that. CRUCIBLE earns its keep when you want the argument *and* the rebuild.

**Honesty about limits.** See **[`LIMITATIONS.md`](LIMITATIONS.md)** for a straight account
of what is genuinely enforced, what is not proven yet (no measured recall / false-positive
numbers yet; same-model decorrelation is a design bet; coverage means *attention*, not
correctness; **Act II's rebuild is built and unit-tested but not yet field-proven end-to-end
on a real paper — re-derive any regenerated number yourself**), and the roadmap. We ran
CRUCIBLE on its own design before release — it caught real overclaims and a bug in its own
quote-gate, both fixed; that run is in [`examples/self-audit/`](examples/self-audit/), framed
as a development pass, not independent validation.

## Modes — pick your depth (every mode runs on any paid plan)

| Mode | What convenes | Experts | ≈ agents | Best for |
|---|---|---|---|---|
| **Desk Review** | one expert pass, no fleet | a few lenses | ~1–6 | a fast read; lightest setup |
| **Roundtable** | a small adversarial panel | 6–8 | ~20–30 | a quick but real workshop |
| **Workshop** *(default)* | the full adversarial workshop | 12–18 | ~45–65 | serious pre-submission review |
| **Symposium** | a large fleet + close-readers | 25–40 | ~90–250 | top-venue preparation |
| **Summit** | every subsystem, every sentence | 60–120+ | ~300–600 | the most exhaustive pass (opt-in) |

*(Symposium/Summit also scale with paper length and are best run with dynamic workflows enabled; without them they fall back to Workshop depth.)*

**Running it often is fine.** Desk Review and Roundtable are light (single-digit to ~30
agents) and the default Workshop is a few dozen — cheap enough to re-run as you revise a
paper. Reserve Symposium/Summit for a major pre-submission pass.

**Engine.** The workshop always runs via subagents (available on every plan). If dynamic
workflows are enabled — on by default on Max; on Pro, switch them on in `/config` — CRUCIBLE
uses them for faster orchestration; if they're off, Symposium/Summit quietly run at Workshop
depth and CRUCIBLE tells you, rather than downgrading silently. **Desk Review** needs neither,
so it works anywhere.

## Install

```bash
# 1. Claude Code installed; Python 3.8+ on PATH (for the deterministic quote/number checks).
#    Windows: if `python` isn't found, the `py -3` launcher or a conda Python works too.
# 2. Make the skills dir (it may not exist yet) and clone into it:
mkdir -p ~/.claude/skills
git clone https://github.com/tjhavranek/paper-workshop ~/.claude/skills/paper-workshop
#    Windows (PowerShell):
#      New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
#      git clone https://github.com/tjhavranek/paper-workshop "$env:USERPROFILE\.claude\skills\paper-workshop"
# 3. Restart Claude Code, then confirm it loaded with a quick pass on any PDF:
#      workshop my paper: some.pdf   desk review
```

For the rebuild (Act II) you also need the interpreters your analysis uses (R / Python /
Stata), `latexmk` (LaTeX) or the bundled `docx` skill (Word), and `git`.

## Use

```
workshop my paper: mypaper.pdf                 # default Workshop mode, supportive register
workshop my paper: mypaper.pdf  roundtable     # a quick adversarial pass
workshop my paper: mypaper.pdf  summit brutal  # the most exhaustive pass, brutal register
CRUCIBLE mypaper.pdf  symposium                 # the brand name works as a trigger too
```

CRUCIBLE runs the workshop and presents the report. Then it **stops and asks** whether to
implement the changes; if you say yes, it requests your source, data, and code and produces
the redline, the clean version, and the replication package. *Register* (`supportive` /
`brutal`) changes only the tone of the write-up — the severity of a finding never changes.

## Lineage

CRUCIBLE is the successor to the authors'
[`mad-research`](https://github.com/tjhavranek/mad-research) (a cross-model audit that
produces a memo) and
[`research-audit-duel-protocol`](https://github.com/tjhavranek/research-audit-duel-protocol)
(manual multi-model protocols). It inherits their discipline — a locked severity rubric,
quote-and-locate grounding, a preserved minority report, no confidence scores, read-only
treatment of your files — and adds the topic-adapted debating fleet and the rebuild.
(`mad-research`'s own small blinded comparison, n = 5 meta-analyses, found a Claude-only
configuration ranked above its cross-model setup by an independent judge — illustrative,
not proof; CRUCIBLE is Claude-only by design, and a single optional non-Claude "what did we
all miss?" pass is available for those who configure it.)

## What it deliberately will not do

No fabricated citations, numbers, quotes, data, or results. No confidence or
acceptance-odds numbers. No silent edits — changes arrive as tracked redlines on copies for
you to accept. No number in the revised paper that a logged re-run didn't produce. No
automatic merge, submission, or data release. The author remains the author.

## License & citation

CC-BY-4.0 ([`LICENSE`](LICENSE)). If it helps your work, please cite:

> Havranek, T. & Irsova, Z. (2026). *CRUCIBLE (`paper-workshop`): an adversarial multi-expert
> workshop that stress-tests and rebuilds a research paper.* GitHub.
