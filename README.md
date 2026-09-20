# Concordagraph — tax, tithe and tribute

Everything needed to rebuild, verify and extend the graph.

## Run order

```
pdftotext "New Revised Standard Version Bible.pdf" nrsv.txt
python3 nrsv_index.py        # -> verses.json, chapters.json; reconciles the count
python3 build_graph.py       # validates the corpus, writes it into the HTML
python3 attach_verses.py     # -> verses.js  (local only, see below)
```

Then open `concordagraph.html`.

**`nrsv_index.py` exits non-zero if the extraction has changed.** It reconciles
its counts against `index-baseline.json` and prints what moved, per book. A
failure there is not a formatting complaint — it means this build of the index
is not the build the corpus was checked against, and references that used to
resolve may now return nothing. Decide which build is right before going on. If
the new one is correct, re-record it deliberately:

```
python3 nrsv_index.py --record
```

**Which `pdftotext` matters.** Two different programs ship under that name —
Poppler's and Xpdf's — and they extract differently. The current baseline was
produced with `pdftotext version 4.06 [www.xpdfreader.com]` (Xpdf, Glyph &
Cog). Swapping implementations will move the counts, and the reconciliation is
what will tell you.

## Files

| File | What it is |
|---|---|
| `concordagraph.html` | The graph. Self-contained; opens in any browser. |
| `corpus_nodes.csv` | 151 passages: id, reference, group, summary. **Edit this.** |
| `corpus_edges.csv` | 170 connections: source, target, kind, warrant, note. **Edit this.** |
| `corpus_clusters.csv` | The 16 groups: key, name, light colour, dark colour, role. **Edit this.** |
| `module.json` | Names this module — `slug` (the id namespace) and `title`. |
| `build_graph.py` | Validates the corpus and writes it into the HTML. Refuses on any error. |
| `nrsv_index.py` | Builds the verse index from extracted text, and reconciles its counts. |
| `index-baseline.json` | The counts the index is reconciled against. Counts only, no scripture — commit it. |
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
the index, an edge points at a missing node, an id is duplicated, a warrant
tier is misspelled, **the same verse is cited twice in this module**, or the
cluster table is malformed. An unresolved reference means the citation is wrong
— fix it before trusting the node.

Ids in the CSVs are bare (`g1`). The build prefixes them with this module's
slug from `module.json`, so they reach the page as `tithe:g1`. An id you write
with a colon already in it is left alone — that is how an edge points at
another module, and such edges are held back from this page until a master
compile has something to attach them to.

Groups are edited in `corpus_clusters.csv`. **Row order matters**: it sets both
the legend order and where each group sits around the ring. Exactly one group
may carry `hub` in the `role` column — that is the one drawn at the centre. The
renderer looks up the role, so the hub can be renamed or moved without touching
any code.

The script also prints a "check by eye" list: nodes whose summary shares no
wording with the verse it cites. Most are meta-summaries ("Mark's form of the
ruling") and are fine. The list exists because resolving is not the same as
being right.

Warrant tiers are `states`, `supports`, `spec`. Edge kinds are `lex` (shared
wording), `ref` (one passage cites the other), `con` (same idea).

## Known gaps

Matthew 6:12 cannot be addressed from this source — the Lord's Prayer is set
without inline verse numbers, so verses 10–13 do not exist in the extracted
text. That node points at 6:9, which carries the whole prayer.

The current index also drops **114 verses in 110 isolated places** — a verse
number glued onto the end of the previous verse, so the index skips it while
keeping everything around it. Hebrews 7:19, 1 Kings 9:16, 2 Samuel 1:18 and 1
Corinthians 7:11 are examples; `nrsv_index.py` prints the first twenty. None is
cited by the corpus today, so nothing is currently wrong — but a node that
cites one will be refused by `build_graph.py` with a message that reads like a
bad citation when the citation is fine and the index is not.

This is why the reconciliation exists. An earlier build of the same PDF
produced 37,542 verses against today's 37,465, and nothing failed: an index
that quietly loses verses answers every query inside the range it kept with
undiminished confidence. Careful reading cannot find what the extraction
dropped, because the dropped material is not there to be read. Only a count
checked against an independent expectation can.
