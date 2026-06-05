# Phase A — ingest & cartography

Phase A converts the PDF into the addressable substrate every later phase keys off.
Claude reads the PDF natively; the only artifacts to **write** are below.

## Artifacts to emit into the session

1. **`input/paper.txt`** — the full extracted plain text of the manuscript, as
   faithfully as possible (preserve the author's wording exactly; this is the file
   `quote_gate.py` matches against, so paraphrasing it would silently break grounding).
   Keep section headings inline so locators resolve.

2. **`cartography/claim_inventory.json`** — every load-bearing assertion, atomized:
   ```
   { "id": "C-014", "quote": "<verbatim>", "location": {page, section, paragraph},
     "type": "contribution|causal|identification|statistical|empirical-magnitude|
              theoretical|definitional|citation|scope|normative|presentational" }
   ```
   "Load-bearing" = the paper's argument depends on it. Be generous: a missed claim is
   a claim no seat is told to check.

3. **`cartography/sentence_map.json`** — the paper tiled into **disjoint, gapless**
   sentence ranges whose union is the whole body:
   ```
   { "ranges": [ { "id": "s1", "section": "1 Introduction", "text": "<sentence>",
                   "char_start": 0, "char_end": 142 }, ... ],
     "total_sentences": N }
   ```
   This is the spine of the sentence-coverage invariant (`coverage_rubric.md`): at the
   exhaustive/monumental tiers, close-reader sweeps must return a verdict for every
   range, so `covered_sentences == total_sentences` is checkable.

4. **`cartography/source_manifest.json`** — the handful of most decision-critical
   cited works worth fetching in Phase C, each with the in-text claim it supports.

5. **`cartography/precis.md`** — a neutral one-paragraph account of what the paper
   claims to do and why it says it matters. **No praise, no critique** — just the
   map. (The Scout reads this to build the roster; a slanted précis biases the whole
   fleet.)

## Notes
- Tables/figures: capture their captions and any numbers stated in the text. The tool
  does not OCR figure internals; a finding about a figure's content is
  `needs-author-confirmation` unless the number also appears in text.
- Equations: capture as the author wrote them; a proof-checker seat reads them in
  context.
- If the source is .tex rather than PDF, extract `paper.txt` from the compiled text
  (or de-macro'd source) and keep page locators approximate (note this in meta.json).
