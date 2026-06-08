# Act II (true) — Stata reproduction

Companion to [`../REPRODUCTION.md`](../REPRODUCTION.md) (the R/BMA pass). This documents the
Stata-side reproduction, which closes the data-provenance chain from the raw data all the way
to the manuscript.

## What was run
- **Stata:** StataMP-64 15.1, batch mode (`/e`), licensed to Tomas Havranek.
- **Date:** 2026-06-08, fully autonomously.
- **Working directory:** a copy of the published replication package. The authors' original was
  never modified. Source: https://meta-analysis.cz/incentives/
- **Input:** `incentives.xlsx`, sheet `data` (sha256 `570e8c09...`).
- **Script:** `incentives.do` v1.4, the authors' published replication script (1,214 lines).
- **Packages** (already installed in `c:\ado\plus`, so no network was needed): `winsor2`,
  `esttab`/`estout`, `ivreg2`, `boottest`, `ranktest`, `avar`.
- **Command:** `StataMP-64.exe /e do incentives.do`
- **Result:** exit code 0 in 9 min 38 s; the 8,324-line log has **zero Stata error sigils**
  (`r(N);`). The only "not found" lines are Stata's benign pre-save graph notes.

## What it regenerated
The full FAT-PET / publication-bias battery as 11 `.tex` tables (`tab_pcc_baseline`,
`tab_cd_baseline`, `tab_pcc_full`, `tab_wp_pcc`, the experiment tables, ...), about 20 `.gph`
graphs (funnel, histogram, caliper, patterns), and the R-feed intermediate
`auxiliaries/incentives_4R.csv` (1,252 estimates).

## The headline: the chain is closed and deterministic
- The regenerated `incentives_4R.csv` is **byte-for-byte identical** to the authors' shipped
  intermediate (sha256 `46df404...`, 1,252 rows).
- That same hash is the `input_data_hash` the R/BMA pass recorded in
  [`../provenance/token_lab.json`](../provenance/token_lab.json). So the file the R side treated
  as a given input is now shown to be a Stata output, regenerated from the raw `incentives.xlsx`.
- Full chain: `incentives.xlsx` -> Stata 15.1 (`incentives.do`) -> `incentives_4R.csv` (identical
  to shipped) -> R/BMA (Table 5 implied effects, e.g. Laboratory 0.0724) -> manuscript.

**What is reader-reproducible, and what is recorded from the run.** The two committed FAT-PET tables
hash to the values in [`provenance/hashes.json`](provenance/hashes.json), so anyone can reproduce
them with `python helpers/provenance.py hash`. The raw-data hash (`570e8c09...` for
`incentives.xlsx`) and the `incentives_4R.csv` byte-identity (`46df404...`) are recorded from this
run host: those two files are the authors' public web-package data and are not committed here, so a
reader confirms them by re-running the package (see "Reproduce it yourself" below), not by hashing a
committed file.

## Concrete Stata-side numbers (FAT-PET, PCC baseline; [`results/tab_pcc_baseline.tex`](results/tab_pcc_baseline.tex))

| | OLS | FE | BE | Study | Precision | IV |
|---|---|---|---|---|---|---|
| `se_pcc` (FAT publication-bias slope) | 0.854*** | 0.315 | 0.628** | 0.596** | . | 0.892*** |
| Constant (PET bias-corrected mean) | 0.0195** | 0.0393** | 0.0383** | 0.0400*** | 1.337*** | 0.0181* |
| Observations | 1252 | 1252 | 1252 | 1252 | 1252 | 1252 |

The bias-corrected mean beyond publication selection sits near 0.02 to 0.04 PCC, consistent with
the paper's corrected mean of about 0.03.

The `.tex` tables are the raw `esttab` output from the do-file (hence the nested `\sym{\sym{***}}`
and the escaped `\label` underscore), committed verbatim so the content hashes hold. They are
evidence through that content-hash provenance, not recompiled PDFs.

## Reproduce it yourself
1. Download the public replication package from https://meta-analysis.cz/incentives/ (it contains
   `incentives.xlsx` and `incentives.do`).
2. In that folder, run `StataMP-64 /e do incentives.do` (Stata 15+).
3. Confirm the data-side links: the sha256 of `incentives.xlsx` is `570e8c09...`, and
   `python helpers/provenance.py hash --file auxiliaries/incentives_4R.csv` returns `46df404...`
   (1,252 rows), the same hash as the regenerated and the shipped intermediates.
4. Confirm the committed tables:
   `python helpers/provenance.py hash --file results/tab_pcc_baseline.tex` returns `20e554cf...`,
   matching [`provenance/token_stata.json`](provenance/token_stata.json).

## Provenance proof (deterministic)
[`provenance/token_stata.json`](provenance/token_stata.json) ties the FAT slope `0.854` to the
content-hashed `tab_pcc_baseline.tex` and to the hashed raw input. The repo's own
`helpers/provenance.py verify` returns `verified: true`
([`provenance/verify_stata.txt`](provenance/verify_stata.txt)).
[`provenance/hashes.json`](provenance/hashes.json) records the closed chain.

## Honest scope
- One paper, from the authors' own group, a single deterministic run.
- Stata 15.1 was used; the authors' stated environment is Stata 15+. The full do-file ran without
  error on the raw data.
- This is a reproduction of the authors' own pipeline, which is the strongest form of "the numbers
  are real," not an independent re-analysis and not independent validation. Re-derive anything you
  rely on.
- The full 398 KB log, all graphs, and the compiled redline PDF stay in the local session. This
  folder carries the regenerated FAT-PET tables, a focused log excerpt, and the provenance proof.
