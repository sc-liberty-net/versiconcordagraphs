# Concordagraph — tax, tithe and tribute

Everything needed to rebuild, verify and extend the graph.

## Run order

```
pdftotext New_Revised_Standard_Version_Bible.pdf nrsv.txt
python3 nrsv_index.py        # -> verses.json, chapters.json
python3 build_graph.py       # validates the corpus, writes it into the HTML
python3 attach_verses.py     # -> verses.js  (local only, see below)
```

Then open `concordagraph.html`.

## Files

| File | What it is |
|---|---|
| `concordagraph.html` | The graph. Self-contained; opens in any browser. |
| `corpus_nodes.csv` | 151 passages: id, reference, group, summary. **Edit this.** |
| `corpus_edges.csv` | 170 connections: source, target, kind, warrant, note. **Edit this.** |
| `build_graph.py` | Validates the corpus and writes it into the HTML. Refuses on any error. |
| `nrsv_index.py` | Builds the verse index from extracted text. |
| `attach_verses.py` | Generates `verses.js` so the page shows full verse text. |
| `extract_corpus.py` | Pulls the corpus back out of the HTML into CSVs. Recovery tool. |
| `make_findings.py` | Regenerates `findings.pdf`. |
| `findings.pdf` | The substantive results, warrant-tagged. |
| `lexicon.md` | Coined vocabulary. |
| `tooling.md` | How the pipeline works and why. |

## Two rules

**Do not hand-edit the block between `// <corpus>` and `// </corpus>` in the HTML.**
It is overwritten by `build_graph.py`. Edit the CSVs. Everything outside those
markers is safe — the warrant and edge-kind definitions live just past the
closing marker for exactly that reason.

**`verses.js` never leaves your machine.** It holds NRSV text, which is under
copyright. `concordagraph.html` is freely shareable because it carries only
references and summaries; the page reads the verse payload if it is present and
works without it. Do not publish, commit or forward `verses.js`.

## Before the first commit

`git init` before letting an agent edit anything here — edits land on real
disk, and version control is what makes them reversible.

Check `.gitignore` is in place first. It excludes `verses.js`, `nrsv.txt`,
`verses.json`, `chapters.json` and the source PDF. Without it, one `git add -A`
publishes the NRSV.

Keep edit approvals on until the loop is trustworthy. Auto-accept on a corpus
where a wrong reference is invisible is a bad trade.

## Editing the corpus

Add a row to `corpus_nodes.csv`, add its connections to `corpus_edges.csv`, run
`build_graph.py`. It will refuse to write if a reference does not resolve against
the index, an edge points at a missing node, an id is duplicated, or a warrant
tier is misspelled. An unresolved reference means the citation is wrong — fix it
before trusting the node.

The script also prints a "check by eye" list: nodes whose summary shares no
wording with the verse it cites. Most are meta-summaries ("Mark's form of the
ruling") and are fine. The list exists because resolving is not the same as
being right.

Warrant tiers are `states`, `supports`, `spec`. Edge kinds are `lex` (shared
wording), `ref` (one passage cites the other), `con` (same idea).

## Known gap

Matthew 6:12 cannot be addressed from this source — the Lord's Prayer is set
without inline verse numbers, so verses 10–13 do not exist in the extracted
text. That node points at 6:9, which carries the whole prayer.
