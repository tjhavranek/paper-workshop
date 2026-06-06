# Example: paper-workshop audits its own design (Act I)

We ran `paper-workshop` on its **own design** — the tool eating its own dog food. This
folder holds the **validation run** on the cleaned-up shipped version, in **brutal**
register at the cheapest fleet (**Roundtable / `quick`**).

- **[`REPORT.md`](REPORT.md)** — the chair's verdict, validity & venue read, must-fix list,
  verbatim desk-reject "kill shots," central tensions, a sample of findings, and the
  points the panel *rejected*.
- **[`findings.json`](findings.json)** — all 69 delivered findings, machine-readable.
- **[`run_meta.json`](run_meta.json)** — mode, register, counts, roster, coverage.
- **[`brief.md`](brief.md)** — the brief the run was given.

## What happened (this run)

| | |
|---|---|
| Mode / register | Roundtable (`quick`) / brutal |
| Roster (auto-generated) | 11 expert seats + 3 generalists, incl. a decorrelation **skeptic vs. defender** rival pair |
| Findings | 80 raised → **69 delivered, 11 rejected by the verification panel** |
| Total agents | **42** — full pipeline incl. the new citation-grounding, bounded |
| Verdict | `desk-reject-risk` — *as a research contribution*, because the headline claims still lack measured numbers |

## Two runs — the tool kept finding things in itself

1. **A pre-release run** on the early design caught real **overclaims** ("better than any
   conference," "impeccable," "fabrication structurally impossible," "every word a checked
   invariant") **and a fail-open bug in the tool's own quote-gate** — all fixed before release.
2. **This validation run**, on the cleaned-up shipped code, ran **end-to-end at 42 bounded
   agents** and caught that the newly-added citation-grounding **contradicted a "PDF only"
   claim** in `SKILL.md` (finding F-001), plus a stale "one piece of code" line — both fixed
   in response.

Across the two runs the tool found, in itself, overclaims, a code bug, and a spec
contradiction — and we acted on each. That is the tool doing its job, on us.

## What this does *not* prove (please read [`../../LIMITATIONS.md`](../../LIMITATIONS.md))

The verdict is `desk-reject-risk` not because the machine failed — it ran cleanly and its
panel rejected 11 weak findings — but because **as a research contribution the headline
claims still lack measured recall / false-positive numbers**, and **a same-model system
auditing itself is a closed loop: a development pass, not independent validation.** We will
not pretend otherwise. The load-bearing next step is a measured run on third-party papers
with a known answer.

This is **Act I (review) only** — the design document has no data or code, so it cannot
exercise Act II (the rebuild).

*(`../parse_selfaudit.js` generated `REPORT.md` from the raw run for readability.)*
