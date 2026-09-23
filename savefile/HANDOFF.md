# Handoff — purpose, state, and what is already decided

Nothing here repeats `../CLAUDE.md` (how the machinery works and what not to touch),
`HAZARDS.md` (the incidents behind the decisions), or `TODO.md` (what is worth doing
next). Decisions below carry the claim and the reason only; the failure that produced
each one is in `HAZARDS.md`.

---

## What This Is For

This is Ethan's Bible-study research, not a software project that happens to contain
scripture. The artefact is an argument: **that tax and tithe are tangled in the
biblical corpus**, and that the tangle can be shown rather than asserted. The graph
exists to make each connection's standing visible — which ones the text states, which
are a reasonable reading, and which are Ethan's own construction.

What counts as good here is **not more connections**. It is connections whose warrant
is honest. A graph that renders speculation the same as statement is worse than no
graph, because it launders one into the other. Every piece of machinery in the project
exists to defend that single property, and a change that makes the corpus prettier at
the cost of that distinction is a regression however good it looks.

Two value judgements decide most close calls. **A refusal is better than a warning** —
`build_graph.py` exits non-zero rather than printing a caution, because a caution
printed on every build stops being read by the third one. And **a number the project
states about itself must be generated, not typed** — the page once claimed
eighty-nine passages in the New Testament while holding 151 across 25 books, 46 of
them Old Testament, and it was right on exactly the day somebody typed it.

Ethan is not a programmer. He does not run commands himself and does not want git
vocabulary. See `LESSONS.md` before writing anything addressed to him.

---

## State Of Play — 22 September 2026

Confidence levels used below, and the distinction is load-bearing:

| Level | Means |
|---|---|
| **Proven** | A check covers it and the check has been seen to fail on bad input |
| **Asserted** | A check covers it and has never gone red. A hypothesis with a green tick |
| **Spot-checked** | Somebody looked, once, at some of it |
| **Assumed** | Nobody has checked; it is here because it has not caused trouble |

### Done and verified

- **The pipeline runs end to end.** `nrsv_index.py` → `build_graph.py` →
  `attach_verses.py`. 151 nodes, 170 edges, 151 verses attached, 0 unresolved.
  **Proven** — twelve validation rules were each run against a build that must fail
  them, and each refused (see `LESSONS.md`, "prove it red").
- **The index reconciles against a recorded baseline.** `nrsv_index.py` exits non-zero
  on any drift in markers, verses, isolated holes, or per-book counts. **Proven** —
  tested against a forged baseline carrying the older 37,542 figure; it exited 1 and
  named `verses -77`, `Mark -5`, `Acts -4`.
- **The three module decisions are implemented.** Namespaced ids, clusters in a
  per-module CSV with a `role` column, reference-as-identity. **Proven** — an agent
  built a second module ("wages", 12 nodes, colliding bare ids, six shared verses) and
  it built green against the real `build_graph.py` with no script edit.
- **The page's counts and book order are generated, not typed.** **Proven** — 0 nodes
  with an unplaced book, all 25 books labelled, leftmost in Bible order is Genesis
  14:20.
- **No scripture text is in any commit or any published page.** **Proven** —
  `verses.json`, `nrsv.txt`, `chapters.json`, `verses.js` and the source PDF have 0
  commits each across all history; a scan of the built page against a 4,000-verse
  random sample of the index found 0 hits.

### Done, not witnessed

- **Passages, arcs and book labels are clickable.** **Asserted** — driven with real
  clicks at measured coordinates in one browser engine only. This shipped broken twice
  before anyone drove a real gesture; treat it as fragile.
- **Keyboard access to arcs and book labels.** **Assumed**. Tab reaches them and Enter
  activates, but the focus handlers that were meant to announce them never fire in the
  engine tested (`HAZARDS.md`). Nobody has used it with a screen reader.
- **The Bible Gateway chapter links.** **Spot-checked** — five URLs including
  multi-word book names were confirmed to encode correctly; one was opened.

### In progress

- **Codifying the concordagraph procedure as a reusable skill.** A 14-agent design
  pass ran on 22 Sept. The diagnosis is strong, the draft is not installable, and
  nothing was written to the skills folder. The working files went to a session
  scratch directory and are gone with the session; the durable record is
  `DEAD-ENDS.md` and Room tasks 57–59. Next step is not more design — it is building a
  second real concordagraph, because everything that broke in the pass broke on
  contact with one.

### Blocked on a person

- **Nine decisions are Ethan's**, listed in `QUESTIONS.md`. Three of them block the
  skill work outright.

---

## Decisions Already Made — Do Not Re-Litigate

**Ids are namespaced from `module.json` at build time; a bare id gets the module
prefix, an id already containing a colon passes through.** Settled 20 Sept. The
original plan prefixed everything unconditionally, which would have made a
cross-module edge inexpressible — and cross-module edges are the entire purpose of
compiling modules together. Revisiting means rewriting every corpus that exists.

**Clusters live in `corpus_clusters.csv`, and the hub is a `role`, not a cluster
named `bridge`.** Settled 20 Sept. Moving the colours alone would not have unblocked a
second module: the renderer hardcoded the key `bridge` in two load-bearing places
outside the generated block, pinning that cluster to the centre. The `role` column is
what makes the centre a property of the data.

**Reference is identity; everything else is module-scoped.** Settled 20 Sept. Not just
the summary — cluster and edge membership too. Within one module a verse may be cited
at most once, enforced by the build. Across modules the same verse may appear once per
module with its own reading. This is the corpus's actual finding expressed as a data
rule: a verse does different work in different arguments, and a merge that flattens
that throws the finding away.

**The extractor is not the cause of the missing verses, and 37,542 is not a target.**
Settled 20 Sept after testing seven extractor-and-flag combinations. The configuration
already in use is the best of them. See `DEAD-ENDS.md`.

**Verse text never travels.** References and paraphrase summaries ship; the NRSV
payload is generated locally and stays there. This is why the page can be published
at all.

**The page states its own size from generated counts.** Settled 22 Sept. Retyping the
two strings was the obvious fix and was rejected, because the failure was not the
numbers being wrong but a number being typed.

**`--record` is not for clearing a red.** Settled 20 Sept and written into
`../CLAUDE.md`. An index drift failure means this build is not the one the corpus was
checked against; re-recording the baseline to make it pass forges the evidence the
check exists to provide.
