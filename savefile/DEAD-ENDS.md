# Dead ends — tried, abandoned, and why

**Append only.** Correct an entry with a dated sequel beneath it.

An abandoned approach leaves no trace in the repository, and the reasons it was
abandoned are usually the same reasons it looks attractive from outside. Nothing here
repeats `HANDOFF.md`'s decisions — a *decision* chose between live options, a *dead
end* was built or half-built and put down.

---

**Blaming the PDF extractor for the missing verses.** — 20 Sept 2026

The rebuilt index had 77 fewer verses than an earlier build of the same PDF. The
machine had Xpdf's `pdftotext` rather than the more common Poppler one, and swapping
them looked certain to be the fix.

*Abandoned because:* it made things worse, measurably. Poppler installed and seven
extractor-and-flag combinations swept, each into its own scratch directory:

```
combination        markers  verses  vs 37542  holes  places  runs
xpdf (current)        1406   37465       -77    114     110    23
xpdf -layout          1403   37430      -112    122     118    17
xpdf -raw             1403   37428      -114    114     110    11
xpdf -simple          1403   37432      -110    121     117    16
poppler               1403   37269      -273    231     220     7
poppler -layout       1403   37425      -117    121     117     9
poppler -raw          1403   37420      -122    114     110     3
```

The configuration already in use is the best of the seven. Plain Xpdf is also the only
one finding 1,406 chapter markers; every other finds 1,403 — and `nrsv_index.py`'s
docstring describes reflowed output, which is Xpdf's default and not Poppler's. The
script was written against this extractor.

*Still true?* **Yes.** The holes are inherent to this PDF and this splitting logic.
Recovering them needs a different splitting approach in `nrsv_index.py`, not a
different extractor. The 37,542 figure is itself unverified — the Lexiconomicon
records it alongside an irreconcilable 31,102 and says so.

*Salvage:* the sweep table above; the count-and-reconcile machinery that came out of
the investigation (`index-baseline.json`, committed); Poppler, still installed and
occasionally useful.

---

**The tuned-stopword explanation for the check-by-eye count.** — 20 Sept 2026

`build_graph.py` printed 11 nodes to check by eye where a baseline expected 10. Six
hand-tuned stopwords at the tail of its `STOP` list (`form account version repeated
cited together`) looked like the obvious cause, since removing a shared word makes an
empty intersection more likely.

*Abandoned because:* tested and refuted. Removing all six changes nothing; adding each
one alone changes nothing. Identical eleven ids either way.

*Still true?* **Yes.** The cause was never found on the corpus side because there
isn't one — the corpus is intact (151/170, 0 duplicate ids, 0 dangling edges, 151
distinct refs, all resolving). The leading explanation is that the *index* differs
from the one the baseline was taken against, which the entry above makes likely and
nothing can now confirm.

*Salvage:* the elimination itself. Corpus integrity, extraction quality and the
stopword list are all ruled out and need not be re-examined.

---

**Re-appending a node to lift its label above its neighbours.** — 20 Sept 2026

SVG has no z-index. The obvious way to raise a magnified label over the labels beside
it is to pull its group out of the document and append it at the end.

*Abandoned because:* it happens under the cursor, and the browser then never
synthesises a click at all — `pointerdown`, `mousedown`, `pointerup` and `mouseup` all
land on the element and no `click` follows. It is why passages were unclickable.

*Still true?* **Yes**, for anything that must also be clickable.

*Salvage:* the replacement works and is better — `paint-order: stroke` with a
paper-coloured halo makes the magnified label readable over its neighbours without
moving anything. The readout below the spine carries the full reference regardless.

---

**`setPointerCapture` for panning.** — 20 Sept 2026

The conventional way to keep receiving pointer events during a drag.

*Abandoned because:* pointer capture retargets the following `click` to the capturing
element, so nothing underneath ever receives its own. Arcs and book labels were
unclickable for this reason.

*Still true?* **Yes**, wherever anything under the panning surface needs clicks.

*Salvage:* the replacement — record where the press started, begin panning only after
4px of movement, track on `window` so the drag survives leaving the element, and
swallow the trailing click of a real drag. A press that never moves stays a click.
Panning verified at 102×64 with nothing selected by the drag.

---

**The drafted `versicon` skill.** — 22 Sept 2026

A 14-agent design pass produced a complete draft skill — a skill definition, four
reference documents and three scripts — for building concordagraphs repeatably.

*Abandoned because:* not installable. An adversary built a real second module and
broke its modularity plan in four places: the compile gate was literally unsatisfiable
(the only existing module fails it, and adding a cross-module link fails it forever);
namespacing the cluster table kills the page and does not fix the hub it claims to
fix; it contradicted settled Decision 1 while claiming to build on it; and the payoff
it was built for was computed in eight lines without any of the apparatus. A second
critic found the draft not runnable at all — no step that creates a module, an
expansion tool emitting stems fed to a search tool matching whole words, wrong paths
throughout.

*Still true?* **Partly, and this one is an invitation rather than a fence.** The
draft is dead; the diagnosis is not. What is genuinely blocked is writing the skill
*before* a second concordagraph exists — everything that broke, broke on contact with
one.

*Salvage:* three verified findings about the live project, logged as Room tasks 57,
58 and 59. The proof that the three module decisions hold under a real second module.
And one finding about the form itself: **Leviticus 27:30 has degree 5 in the tithe
module and 2 in a wages module — union 7, an argument existing in neither reading.**
That is the modularity problem stated properly, and it is not a plumbing problem.

*Where:* the write-up was delivered to Ethan as a file on 22 Sept and is not in the
repository. The durable record is this entry plus Room tasks 57–59.
