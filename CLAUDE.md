# Working rules for this repository

This file loads automatically in every session opened here, which is why the
branch rule lives in it and not only in the README. A README is a pointer, and
pointers get skipped.

## One topic per branch

**Every branch holds a different concordagraph, on a different scriptural
topic.** A branch is a separate corpus — its own passages, connections, groups
and built page. It is not a version of another branch's work.

Consequences, all of which have caught somebody out before:

- **Do not merge branches into each other, and do not merge into `main`.**
  Nothing here is a feature branch. A merge would interleave two unrelated
  corpora and silently collide their node ids.
- **Do not assume `main` has the project.** It holds this note and the README.
  Checking out `main` and finding no CSVs is correct, not a broken clone.
- **Check which branch you are on before editing a corpus.** `git branch
  --show-current`. The files have the same names on every branch.
- **A new topic is a new branch off an empty root**, not off another topic.

## Never commit scripture text

`verses.json`, `nrsv.txt`, `chapters.json`, `verses.js` and any source PDF are
NRSV and under copyright. They are gitignored on every branch and have never
been committed. Do not override that, and do not add a file that embeds verse
text into the page.

What ships is references and paraphrase summaries. That is the whole reason a
branch can exist on GitHub at all.

## Every edge carries a type and a warrant

`lex` / `ref` / `con` for what kind of link it is; `states` / `supports` /
`spec` for how much weight the text actually puts behind it. Never promote a
speculation to a statement, and never let a representation of an edge drop its
warrant — a summary, an export or a screenshot that renders the tiers
identically is where speculation turns into settled reference.

## Each branch has its own rules

A topic branch carries its own `CLAUDE.md` with the rules for that corpus — the
run order, what its validator refuses, how its index is built. Read it. This
file governs the repository; that one governs the work.
