# style_gate.py — usage

Deterministic AI-style detector. It does the COUNTING the `human-voice` angle used to
eyeball, so voice stops being the one Act-II rail with no script under it. Unlike the quote
gate it is **advisory and author-relative**, and it fails **open**: a punctuation spike is a
flag for the human, never an auto-reject, because a legitimate author may use em-dashes.

## When it runs
- Inside the Act-II verification panel, as the deterministic aid to the `human-voice` angle:
  the verifier writes the edit's `new_text` and an adjacent author sentence to temp files,
  runs the gate, and quotes its JSON as the style diff instead of counting by eye.
- In the Package and Disclose phases, on every AI-authored deliverable (README,
  `changes_map.md`, `MAP.md`, `data_dictionary.md`, the disclosure): those files have no
  author voice to match, so a non-`clean` verdict means rewrite to plain prose.

## Modes
```
# one inserted span vs an author baseline (inline / file / stdin)
python helpers/style_gate.py check --inserted "new sentence" --baseline-file input/paper.txt
python helpers/style_gate.py check --inserted-file new.txt --baseline-file input/paper.txt
cat new.txt | python helpers/style_gate.py check --inserted-stdin --baseline-file input/paper.txt

# batch: many spans against one baseline ([{ "id", "text" }, ...])
python helpers/style_gate.py batch --baseline-file input/paper.txt --spans spans.json
```

## Verdicts (most severe first)
- `banned` — an AI-lexicon token (delve, leverage, underscore, showcase, foster, harness,
  pivotal, ...) or phrase the author does not also use. Author-independent. **Exit 2.**
- `antithesis` — the staged negation-correction flip ("it is not X, it is Y"). Narrow on
  purpose. Author-independent. **Exit 2.**
- `spike` — an em-dash, en-dash, or semicolon RATE above the author baseline by more than
  1.5x AND at least 2 absolute in the span. Author-relative; advisory. **Exit 0.**
- `signposting` — filler the author does not use (it is worth noting, importantly, moreover,
  furthermore, in summary). Advisory. **Exit 0.**
- `no-baseline` — no author baseline supplied; only banned/antithesis can still fire. **Exit 0.**
- `clean` — none of the above. **Exit 0.**

`severity_hint`: `rewrite-or-route-to-author-confirmation` for banned/antithesis;
`route-to-author-confirmation` for spike/signposting/no-baseline; `keep` for clean. Every row
carries `advisory: true` — the gate annotates, it never edits text and never returns a reject.

## What it deliberately does NOT flag deterministically
Left to the LLM's semantic judgment, to avoid false positives on legitimate academic prose:
bare `rather than X, Y` (a normal comparative — "we use OLS rather than IV"), `not only X but
also Y`, and `highlight` as a verb (needs part-of-speech). The author-voice standard in
`prompts/phase2/12_scribe_implementer.md` still bans these; the script just does not claim a
deterministic call it cannot make cleanly.

## Author-relative, by design
Dash counting runs on RAW text and counts both Unicode (—, –) and LaTeX-source (`---`, `--`)
encodings. The banned-lexicon scan subtracts any term that appears in the author baseline (the
deterministic form of "unless the author already uses it"). The gate runs ONLY on inserted
spans and AI-authored deliverables, NEVER on the author's untouched prose.

## The gate is only as clean as its baseline (multi-pass caveat)
Because the gate is author-relative, the `--baseline-file` must be the author's PRISTINE
original prose. On a multi-pass re-run whose input is itself an earlier paper-workshop
revision, the working copy already carries the tool's voice; baselining against it would read
the tool's own em-dashes as "the author's style" and the spike would never fire, so drift
launders and compounds across passes. Always pass the author's last hand-written version (the
`original_manuscript` recorded at intake) as the baseline, never a prior tool output.
