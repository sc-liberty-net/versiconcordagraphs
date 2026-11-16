# Concordagraph: Kings & The Kingdom

How man rules and how God rules, across the Bible, passage by passage. The pipeline is
the one from Taxes, Tithes, & Tribute (`..\Biblography\README.md` and `tooling.md`
explain it). This file lists what is particular to this topic.

## Run Order

```
python nrsv_index.py       # verse index; must report no drift
python build_graph.py      # validates the corpus, writes it into the page
python check_wording.py    # no summary or edge note copies five NRSV words
python attach_verses.py    # verses.js, local only, never committed
python overlaps.py         # OVERLAPS.md: where this topic meets the others
python make_icons.py       # favicon, home-screen icons, preview card (after corpus changes)
python check_page.py       # the gate: runs the page, diffs against smoke-baseline.out
```

Then open `concordagraph.html`.

## Files

| File | What it is |
|---|---|
| `corpus_nodes.csv` | The passages: id, reference, group, summary. **Edit this.** |
| `corpus_edges.csv` | The connections: source, target, kind, warrant, note. **Edit this.** Ids with another topic's prefix (`tithe:`, `sword:`) are cross-topic links, held back from this page. |
| `corpus_clusters.csv` | The 14 groups. Row order sets the ring; `hub` marks the centre. |
| `module.json` | Slug `king`, title. |
| `READING.md` | What the corpus shows, with warrant tiers. |
| `OVERLAPS.md` | Generated. Shared verses and cross-topic connections. |
| `check_wording.py` | Refuses five-word NRSV runs in summaries and edge notes. |
| `overlaps.py` | Writes `OVERLAPS.md` from all three topic folders. |
| `savefile/HANDOFF.md` | The agreed plan and what is not done. |
| `make_icons.py`, `icons/` | The crown emblem, favicons and the 1200 × 630 preview card, drawn from the built page. |
| `smoke_concordagraph.py`, `check_page.py` | The page test (desktop and phone, real touch, pinch) and its gate. |
| `smoke-baseline.out`, `SMOKE-RECORD.md` | The recorded test output, and why it last moved. |
| `REQUIREMENTS.md` | Ethan's decisions for this page, checked at every ship. |
