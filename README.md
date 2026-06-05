# CRUCIBLE — the `paper-workshop` skill

> *Every paper leaves changed.*

A monumental, Claude-only [Claude Code](https://claude.com/claude-code) skill that
simulates the workshop a scientific paper would get if a world authority on **every**
sub-part were in the room, **every contested choice were argued by both rival
schools**, a generalist panel asked whether it **matters** and is **intelligible**,
**every comment were independently re-checked from many angles**, and then the best of
the room **rebuilt the paper and its replication package**.

It is built for power users who want the largest, most rigorous critique Claude can
produce — and then want the changes *implemented*, not just listed. Runtime is not a
constraint: a monumental run takes hours by design.

---

## Two acts

### Act I — TRIBUNAL  (input: the paper PDF only)
A topic-adapted fleet of expert referee subagents, generated **from the paper's own
content**, reviews it in parallel:

- **Competing traditions.** Every contested methodological choice is staffed by ≥2
  seats from **rival schools**, instantiated with *opposed objective functions* (one
  "find the fatal flaw," its rival "find the strongest defensible version"). Real
  disagreement, not disciplinary costume.
- **Generalist seats.** Distinguished outsiders test **relevance** ("does this
  matter?"), **understandability** ("is it intelligible to a brilliant outsider?"), and
  **cross-field significance** ("does it travel?") — so the panel never drowns in
  technical detail.
- **Exhaustive to the sentence.** The paper is tiled into disjoint sentence ranges and
  a completeness audit certifies `covered == total` — "every argument, every word" is a
  *checked invariant*, not a slogan.
- **Multi-angle verification before delivery.** Nothing reaches you until several
  blind subagents — each from a different angle (quote/locator, logical validity,
  factual/literature, severity calibration, decision-relevance, fix-safety, charitable
  steelman) — have cleared it.

Output: a verified, prioritized finding ledger; a per-seat referee-report bundle; a
debate transcript with the cruxes named; a generalists' importance memo; a verbatim
desk-reject pre-mortem; a 3-bucket venue read (no fake acceptance odds); a preserved
minority report; and a **completeness certificate**.

### Act II — ATELIER  (opt-in; asks for source + data + code)
The best of the room rebuilds the paper:

- Implements the agreed findings as **tracked changes** on copies (never your
  originals), one finding per commit.
- **Re-runs your actual code** against your data, regenerates figures and tables, and
  propagates every number under the **Execution-Provenance Wall**: *no number enters
  the paper unless a real, logged re-run produced it.*
- Assembles a genuinely runnable **replication package** (AEA/TOP-compatible) whose
  `MAP.md` ties every table, figure, and headline number to the exact script that
  produced it — and clean-room-replicates it to prove it reproduces.
- Auto-generates an **AI-involvement disclosure**.
- **Every edit is multi-angle-verified too** (adding numeric-provenance, consistency,
  and integrity angles), and anything touching a number, sample, claim, or result
  **waits for your sign-off** — the tool never alters the scientific record on its own.

---

## Why you can trust a 300-agent run

The fleet is the product; these rails (always on, ~free, never traded for scale) are
what keep it from laundering a fatal flaw into a confident green light. See
[`prompts/shared_grounding_rules.md`](prompts/shared_grounding_rules.md):

- **Ground, don't recall; never fabricate.** Exact quote + locator on every finding,
  verified by a deterministic script ([`helpers/quote_gate.py`](helpers/quote_gate.py)),
  not an LLM. Unverifiable → *needs author confirmation*, never asserted.
- **No confidence scores. Severity is tone-invariant** — the same paper reviewed
  "supportively" or "brutally" returns the same must-fix list.
- **Decorrelate by rival objective function; preserve dissent verbatim.**
- **The author is the author** — substantive scientific judgments are proposed, never
  imposed.

---

## Install

```bash
# 1. Claude Code (assumed installed)
# 2. Python 3.8+ on PATH (for the deterministic quote-gate)
# 3. Clone into your skills directory:
git clone https://github.com/tjhavranek/paper-workshop ~/.claude/skills/paper-workshop
#    (Windows: %USERPROFILE%\.claude\skills\paper-workshop)
# 4. Restart Claude Code.
```

For Act II you also need the interpreters your analysis uses (R / Python / Stata),
`latexmk` (LaTeX) or the bundled `docx` skill (Word), and `git`.

## Use

```
workshop this paper: mypaper.pdf                  # default 'thorough' tier
workshop this paper: mypaper.pdf  exhaustive      # bigger fleet
CRUCIBLE mypaper.pdf  monumental  brutal          # the full fleet, brutal register
```

Act I runs and presents the report. Then the skill **stops and asks** whether to
implement; on opt-in it requests your source/data/code and runs Act II. Tiers:
`quick` · `thorough` (default) · `exhaustive` · `monumental`. Register: `supportive`
(default) · `brutal` (delivery tone only — severity never changes).

## Relationship to `mad-research`

| | `mad-research` | `paper-workshop` (CRUCIBLE) |
|---|---|---|
| Shape | cross-model **audit** (3 fixed streams) | Claude-only **tribunal + atelier** (topic-adapted fleet) |
| Disagreement | cross-stream | **competing traditions** staffed as rival seats |
| Generalists | — | relevance + understandability + significance |
| Code | does **not** run it | **re-runs it** and ships the replication package |
| Output | an audit memo | memo **+ implemented paper + replication package** |
| Shared DNA | locked rubric · quote+locate · minority report · no confidence scores · read-only source | **ported here** |

Use `mad-research` for a fast cross-model second opinion; use `paper-workshop` for the
largest possible Claude fleet **and** to actually fix the paper.

## License & citation

CC-BY-4.0 (see [`LICENSE`](LICENSE)). If you use it, please cite:

> Havranek, T. & Irsova, Z. (2026). *paper-workshop (CRUCIBLE): a multi-agent
> simulated workshop that stress-tests and rebuilds a scientific paper.* GitHub.

Built on the lineage of
[`mad-research`](https://github.com/tjhavranek/mad-research) and
[`research-audit-duel-protocol`](https://github.com/tjhavranek/research-audit-duel-protocol).
