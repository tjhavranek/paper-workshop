# Stopping rule, how a deepening run knows it is done

The completeness audit (Phase H) runs once per pass and **reports** any uncovered claim or
section (its `reopen` list ships with the result). The default single run does one coverage
pass and reports gaps. It does **not** silently auto-loop. When a run is *deepened* (the
orchestrator re-fans targeted reviewers at the `reopen` list, or the author re-invokes a
heavier mode), apply the **two-condition marginal-yield rule** below to decide when to stop,
rather than a naive "loop until no new findings" (which on a same-model fleet rewards
manufacturing marginal false positives to keep the loop alive).

## Stop only when BOTH hold

1. **Finding-yield dry.** The most recent round produced **zero new
   verification-panel-passed High or Medium findings.** Low-severity items and typos
   do **not** count. They can never keep the loop alive.
2. **Coverage dry.** The completeness audit (Phase H) reports **no `NOT COVERED`
   load-bearing dimension** (`coverage_rubric.md`) and **no untiled sentence range**
   (`covered_sentences == total_sentences`).

## Guardrails on the loop

- **Minimum-round floor.** Run at least the tier's minimum rounds before honoring a
  "dry" signal. A deep structural flaw often surfaces only after several rounds of a
  seat building context, so early quiet is **not** "clean."
- **Budget cap.** Honor an optional max-round / max-agent / token cap; if hit, stop
  and **log what remained** (open coverage gaps, leads not chased). Never present a
  capped run as exhaustive.
- **Targeted re-fan-out, not re-run-the-world.** When the logic verifier or the
  completeness auditor flags a hole, spawn a scoped mini-fan-out for exactly that
  uncovered claim / unresolved crux / sentence gap. Do not relaunch the whole fleet.
- **Log the yield curve.** Each round records new-High/Medium-findings-vs-round and an
  approximate agent/token count. The curve ships with the report so the run shows its
  own diminishing returns instead of asserting completeness.

## Per-tier loop shape

| Tier | Min rounds | Loop discover→verify? |
|---|---|---|
| `quick` | 1 | no |
| `thorough` | 1 (+1 targeted if a High is unresolved) | only on residue |
| `exhaustive` | 2 | yes, until both-dry or cap |
| `monumental` | 3 | yes, until both-dry or cap, on findings AND coverage |
