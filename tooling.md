# Tooling

What has been built for this project, what each piece does, and the terms
used to talk about them. Companion to `lexicon.md`, which covers the
conceptual vocabulary rather than the machinery.

---

## The pipeline, in order

```
NRSV PDF  ──pdftotext──▶  nrsv.txt  ──nrsv_index.py──▶  verses.json
                                                    └─▶  chapters.json
                                                             │
                                          curation + warrant-tagging
                                                             │
                                                             ▼
                                                   concordagraph.html
```

Each stage is a file on disk. Nothing depends on a conversation staying
open, which is the point — see **session-volatile** below.

---

## Scripts

### `nrsv_index.py`

Turns the extracted Bible text into an addressable index. Reads
`nrsv.txt`, writes `verses.json` (one record per verse: `ref`, `book`,
`ch`, `v`, `text`) and `chapters.json` (whole chapter bodies, for cases
where verse-level splitting is not trusted).

Two problems it solves, both of which produced wrong citations in the
first version:

**Inline chapter markers.** Chapter boundaries appear in the extracted
text as `[John 8]`. The extractor sometimes runs a marker into the end of
the previous verse rather than putting it on its own line. A
line-anchored regex silently dropped those chapters — 45 of them. The fix
scans for markers anywhere in the stream.

**Omitted verses.** The first splitter accepted a number only if it was
exactly one more than the last accepted verse. The NRSV omits certain
verses from its running text (Matt 17:21, Luke 23:17, John 5:4, Acts 24:7
and others), so the counter hit a number that never appeared and
truncated the rest of the chapter. The fix takes the **longest increasing
subsequence** of candidate numbers instead, which steps over gaps and
ignores stray numerals.

**Book-seam truncation.** The final chapter of each book ran into the next
book's introduction, whose numbering inflated the verse ceiling. Chapter
bodies are now cut at that seam.

Running it prints a self-check: chapters found, verses indexed, *thin*
chapters (ceiling under verse 8) and *gappy* chapters (under 90 percent
coverage). Both lists should be read, not just counted — most thin
chapters are genuinely short (Psalm 23 has six verses) and are not errors.

Result: 1,403 chapters, 37,269 verses, up from 1,358 and 34,285.

### `concordagraph.html`

The interactive graph. Self-contained: nodes, edges, layout, and styling
in one file, no external data. Filters by group, by edge kind, and by
warrant tier; full-text search across references and summaries; click a
node to see its connections with the reasoning for each.

Node summaries are **paraphrase written for this project**, never NRSV
text. This is a copyright constraint, not a style choice — the graph
holds references and gists, and the wording of a passage is checked
against the index when it matters.

---

## Terms of art for the machinery

**verse index** — `verses.json`. The lookup that makes a reference
resolvable. Its existence is what separates a citation from a
**ghost-citation** (see `lexicon.md`).

**thin chapter** — a chapter whose highest indexed verse is under 8.
Either a genuinely short chapter or a splitter failure; requires eyes.

**gappy chapter** — a chapter where the count of indexed verses is under
90 percent of its highest verse number. Usually means spurious high
numerals were admitted, not that verses were lost.

**drift** — the failure mode where verse-splitting loses sync partway
through a chapter and every subsequent reference in that chapter is
wrong. Dangerous because the returned text is real; only the label is
false.

**book seam** — the join where one book's last chapter runs into the next
book's front matter in the extracted text.

**raw-chapter fallback** — verifying a passage against `chapters.json`
rather than `verses.json` when the verse-level split is in doubt. This is
how the drifted Gospel passages were caught.

**session-volatile** — living only in a chat sandbox and lost when it
ends. The first verse index was session-volatile and had to be rebuilt
from scratch. Anything worth keeping belongs in the project folder.

**warrant tier** — `states` / `supports` / `spec`, attached to every edge.
Defined in `lexicon.md`; listed here because it is a field in the graph's
data model, not only a habit of reading.

**edge kind** — `lex` (shared wording), `ref` (one passage cites the
other), `con` (same idea). Also a data field.

---

## What is not built yet

- No script emits the graph data. Nodes and edges are authored by hand
  inside the HTML. A `build_graph.py` that reads a curated CSV and emits
  the data block would make the corpus editable without touching markup.
- No regression test. A fixture of thirty known references checked against
  the index after every change would catch drift automatically rather than
  by inspection.
- The Hebrew Bible corpus from the tithe and imperial-taxation work is not
  in the graph. It appears only as ten anchor nodes.
