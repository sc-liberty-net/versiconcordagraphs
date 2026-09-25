# versiconcordagraphs

Scriptural concordagraphs. **One topic per branch.**

## Read them here

### → **[sc-liberty-net.github.io/versiconcordagraphs](https://sc-liberty-net.github.io/versiconcordagraphs/)**

The built pages, live. Deployed from the `gh-pages` branch, which holds one
directory per topic and nothing else. Each topic's page is generated from its
own branch by that branch's `build_graph.py`; `gh-pages` is the shelf, not the
workshop.

## The rule

**Each branch holds a different concordagraph, on a different scriptural
topic.** A branch is not a version of the same work and not a feature branch —
it is a separate corpus with its own passages, its own connections, its own
groups, and its own built page.

Do not merge one topic's branch into another's. Do not expect `main` to
contain them.

| Branch | Topic |
|---|---|
| `main` | This note. No corpus. |
| `taxes-and-tithes` | Tax, tithe and tribute — 158 passages across 25 books, 180 connections. **[Read it](https://sc-liberty-net.github.io/versiconcordagraphs/taxes-and-tithes/)** |
| `gh-pages` | The built pages. Generated output, not a topic. |

Ethan asked for the branch to be called *Taxes & Tithes*. Git will not accept a
space in a branch name, so it is `taxes-and-tithes` on disk. The topic's own
name, as the page shows it, lives in that branch's `module.json`.

## What a concordagraph is

From the Lexiconomicon, where the word is in force:

> A traversable network of source references in which nodes are locatable
> citations and edges carry both a **type** and a **warrant**.

- **Edge types** — `lex` (shared wording), `ref` (one passage cites the other),
  `con` (same idea).
- **Edge warrants** — `states` (the text says it), `supports` (a reasonable
  reading, inferred), `spec` (constructed by the reader; the text does not link
  these).
- **Rule of admissibility** — an edge counts only when it names its type,
  carries its warrant tier, **and both endpoints resolve to real, retrieved
  references**.

> Why it matters: a graph that renders all edge types identically launders
> speculation into settled reference. The visual distinction is not decoration
> — it is the verification surface.

## What is deliberately not here

**No scripture text, on any branch, ever.** The verse index a branch is built
and checked against (`verses.json`, `nrsv.txt`, `chapters.json`, `verses.js`)
and the source PDF are NRSV, under copyright. They are gitignored in every
branch and have never been committed. A branch carries references and
paraphrase summaries only, which is what makes it shareable at all.

Each branch rebuilds its own index locally from a source it holds itself. See
that branch's `README.md` for the run order.

## Open, and Ethan's to decide

**How the branches relate to `main`.** Deferred deliberately. The live
question is whether many topics compile into one master graph, and if so what
happens when two topics cite the same verse — that decision is settled in the
`taxes-and-tithes` branch's `DESIGN.md` as *reference is identity; everything
else is module-scoped*, but nothing has been built that does the compiling.

Until that is decided, branches stay independent and nothing merges.
