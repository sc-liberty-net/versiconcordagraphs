# Smoke baseline record

Every line `smoke_concordagraph.py` prints is gated against `smoke-baseline.out`.
A line that moves fails the run until the cause is written here. Append only —
each entry is the evidence for why a number is what it is.

Move the baseline with `baseline_guard.py`, never by overwriting the file:

```
python <skills>/smoke-gate/scripts/baseline_guard.py \
    --baseline smoke-baseline.out --new new.out \
    --cause "<what changed, and why the new value is right>" \
    --record SMOKE-RECORD.md
```

---

## 2026-09-25 — first baseline, 32 lines

Recorded after the page shipped blank three times running.

**The defect this exists to catch.** The Bible Hub link change declared
`const HUB` for its slug overrides. That identifier was already taken further up
the same inline script for the hub *cluster*. A duplicate `const` is a **parse**
error, so the whole script died before its first line: no graph, no panel, no
filters, on a page whose HTML contained every string anyone thought to check.

Three separate verifications passed against that broken page — the biblehub URLs
were present, 25 of 25 book slugs resolved live, `META` held the right counts.
All three read the served HTML **as text**. None of them ran it. Ethan found the
blank page by opening it.

**Proved before it was trusted.** `prove_smoke.py` reintroduces the exact `HUB`
collision into a copy of the page and asserts the suite fails on it:

```
RED   exit 1, console errors: 1, drawn nodes: 0, drawn arcs: 0, fatal: 4
GREEN exit 0, console errors: 0, drawn nodes: 164, drawn arcs: 199, fatal: 0
```

The first version of the suite *crashed* on the red page rather than reporting —
`#net g` does not exist when the script has not run, so `getBBox()` threw and the
suite died halfway through its own output. A crashed suite gives the gate nothing
to diff. Fixed by routing every probe through `ev()` and every dict read through
`pick()`.

**The baseline at this commit:** 164 nodes, 199 edges, 25 books, 16 clusters,
3 warrants, 3 kinds. Matthew 23:23 shows 12 connections. Matthew 9:9 to
Mark 2:14 carries 2 edges of kinds `con,lex` on 2 distinct arc lanes — the
first use of the Q5 change. `NRSV payload present: False`, because the suite
runs against an isolated copy with no `verses.js`, which is what gets published.

**Guards confirmed working at record time:** `smoke_diff.py` passes on an
identical run and fails on a single hand-edited digit (`drawn nodes: 164` →
`163`). `dead_selector_lint.py` checks 22 call sites and 19 distinct tokens
against the page and finds no dead selector.

## 2026-09-25 - baseline refreshed: smoke-baseline.out
cause: treasure and metal material added: 2 clusters, 20 nodes, 24 edges. Haggai is a new book, hence one more tick and label; the two new clusters add two rail rows; bbox height grows with the extra arcs. Search still matches the same 8 verses (184-176 = 164-156 = 8).
moved: 13 changed, 0 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/new.out -> smoke-baseline.out

## 2026-09-25 - baseline refreshed: smoke-baseline.out
cause: motif filter added: a fourth rail group keyed on Strong's lemmas rather than on cluster. Seven new gated lines cover it. Ticking Treasure dims 170 and lights 14, which is exactly the node list corpus_motifs.csv records for that motif.
moved: 0 changed, 7 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/mo.out -> smoke-baseline.out

## 2026-09-25 - baseline refreshed: smoke-baseline.out
cause: UI pass: zoom clamped to the fitted view, title capitalised, dead arrangement control hidden, era label 10.5px to 34px, arcs thinned, group notes added for tooltips, reset moved over the canvas, motifs became pills in a bar. Twelve new gated lines. The tax motif lost Hebrews 7:3 because telos means end as well as toll.
moved: 2 changed, 12 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/ui.out -> smoke-baseline.out

## 2026-09-25 - baseline refreshed: smoke-baseline.out
cause: second UI pass: clicking a group name shows its passages in the panel, select-all and clear buttons above the group list, the opening view backed off by a 0.86 fit margin, and the header paragraph moved into an About dialog. Zoom floor moves 0.3271 to 0.2812 because the margin applies to the floor as well - the two are the same view by design.
moved: 5 changed, 14 new, 0 gone (0 allowed, not counted)
source: C:/Users/ethan/AppData/Local/Temp/ui2.out -> smoke-baseline.out
