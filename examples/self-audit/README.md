# Example: CRUCIBLE audits its own design (Act I)

Before its first release, we ran `paper-workshop` **on its own design** — a real, unedited
Act I run, in **brutal** register, at the cheapest fleet size (**Roundtable / `quick`**).
This folder is the result.

- **[`REPORT.md`](REPORT.md)** — the chair's verdict, validity & venue read, top strengths,
  prioritized must-fix list, the verbatim desk-reject "kill shots," the central tensions,
  a representative sample of findings, and the points the panel *rejected*.
- **[`findings.json`](findings.json)** — all 76 delivered findings, machine-readable.
- **[`run_meta.json`](run_meta.json)** — mode, register, counts, roster, coverage.
- **[`brief.md`](brief.md)** — the brief the run was given.

## What happened

| | |
|---|---|
| Mode / register | Roundtable (`quick`) / brutal |
| Roster (auto-generated) | 10 expert seats + 3 generalists, paired by rival objective function |
| Findings | 82 raised → **76 delivered, 6 rejected by the verification panel** |
| Total agents | **40** (batched verification keeps it bounded) |
| Verdict | `desk-reject-risk` — *as a research contribution*, because the design's headline claims were asserted but not yet measured |

## Why we're shipping our own bad review

Two reasons, and they matter more than a glowing example would.

**1. It found real bugs in itself, and we fixed them.** Run on the pre-release design, the
tool flagged — with grounded, code-checked findings — that the design overclaimed
("better than any conference," "impeccable," "fabrication structurally impossible," "every
word a checked invariant") and that its *own* deterministic quote-gate **failed open** on an
empty non-absence quote (finding **F-007**, verified against the actual Python). We acted on
its review: the superlatives are gone from the shipped skill, the quote-gate now fails
closed (and tolerates BOM files), the agent-count claims were corrected, and the
"every-word" coverage claim was relabeled as coverage of *attention*, not correctness. The
commit history reflects this. That is the tool doing its job — on us.

**2. We will not pretend a self-audit is independent validation.** The single sharpest
finding (**F-079**) is that a same-model system designing, claiming, auditing, and verifying
*itself* is a closed loop — a development pass, **not** evidence of trustworthiness. We
agree. This example demonstrates that the machine runs, stays bounded, grounds its findings,
and its panel rejects weak ones; it does **not** prove the tool catches flaws a human panel
would, or that its false-positive rate is low. That requires a measured run on third-party
papers with a known answer, which is future work, stated plainly rather than papered over.

This is **Act I (review) only** — the design document has no data or code, so it cannot
exercise Act II (the rebuild: redline + clean version + re-run code + replication package).

*(`parse_selfaudit.js` generated `REPORT.md` from the raw run for readability.)*
