# Questions — what is not the agent's to decide

**Reconcile.** When one is answered, the answer moves to `HANDOFF.md`'s decisions
section and the question is struck here with a date.

Everything below needs authority, taste, or a reading nobody has done. Anything an
agent could settle by measuring is in `TODO.md` instead — that boundary is the whole
point of this file.

---

## Blocking the research finding

**Q1 · Do Matthew 23:23 and Luke 11:42 rebuke tithing, or affirm it while
relativising it?**
The summary of Matthew 23:23 accounts for 13 of the verse's 40 words and stops at the
woe; Luke 11:42's covers 16 of 36. Nobody has read what the remaining words say — this
was deliberately not guessed. The cluster is named "Tithing rebuked" and sits directly
on the path from the tithe statutes to the Hebrews 7 argument, so *rebuked* versus
*affirmed but relativised* changes the trajectory the whole corpus traces. Neither
node appears on the check-by-eye list, because that heuristic only fires when a
summary shares **no** content word with its verse.
*Needs:* Ethan, reading the two verses. This is his research, not a measurement.
Room task 54.

**Q2 · Should the 22 summaries that reuse NRSV wording be rewritten?**
22 of 151 contain a run of five or more consecutive words lifted from the verse; the
longest are nine ("Is it lawful to pay taxes to the emperor?", "the patriarch gave him
a tenth of the spoils"). `../CLAUDE.md` says summaries are paraphrase, never NRSV
wording. Nothing continuous is reconstructable, so the copyright exposure is small —
but these are the files that ship, and the README's claim that the page is shareable
*because* it carries only references and summaries is less clean than it reads.
*Needs:* Ethan. Rewriting a summary is an editorial act on his own argument. Room
task 51.

---

## Blocking a second concordagraph

**Q3 · Fix the unquoted cluster key now?**
Two lines: emit `{j(k)}` in `build_graph.py`, and widen `extract_corpus.py`'s cluster
regex to accept a quoted key. Left undone because it is live code and he was away.
Until it lands, any group name that is not a single lowercase word ships a blank page
on a green build.
*Needs:* Ethan's go-ahead. Room task 57, and it blocks Q6.

**Q4 · `i3`, `c4`, `c13` carry no connection at all — connect, remove, or keep?**
Luke 3:1, Matthew 10:3, Luke 15:1. Each has obvious neighbours. A concordagraph is a
claim about connections, and a node with none is either an unfinished thought or a
deliberate boundary marker; the corpus does not say which.
*Needs:* Ethan. Cheaper to settle at 151 nodes than at 400. Room task 58.

**Q5 · Can two passages carry more than one connection between them?**
The duplicate check keys on the node pair alone — undirected, kind-blind — so a
finding that two verses *both* share wording and make the same argument cannot be
recorded. Zero pairs collide today, so nothing has been lost yet. One line either way.
*Needs:* Ethan. It is a decision about what the corpus can say, and it should be
written into `DESIGN.md` whichever way it goes. Room task 59.

**Q6 · Compare, or compile?**
The settled module decisions hold under a real second module — that is proven. What is
not settled is whether many topics should be *compiled* onto one canvas at all. A
compiled graph asserts connections no module made: Leviticus 27:30 has degree 5 in
tithes and 2 in wages, union 7, an argument existing in neither reading. Two pages
side by side with a shared co-citation list may simply be better.
*Needs:* Ethan, after someone builds module two and the eight-line co-citation
reporter. The honest answer comes from looking, not arguing. Depends on Q3.

**Q7 · The first module can never have an honest discovery ledger — exempt it, or
accept that it never lints clean?**
It was built before any procedure existed. Backfilling a ledger would forge exactly
the evidence such a check exists to provide.
*Needs:* Ethan, and only once a skill with a ledger actually exists. Parked.

---

## Blocking nothing yet, but it will fester

**Q8 · "Versicon" means two incompatible things and nobody has reconciled them.**
The Lexiconomicon — where the word is filed — defines a versicon as *the addressable
index itself*: a fixed corpus converted once into a unit-addressable form so every
citation is retrieved rather than recalled. That is `verses.json`. This project's
`DESIGN.md` and `lexicon.md` use it for *a subject module*. The project's own entry
admits the word "arrived without a traceable point of coinage". Under the register's
definition this project has exactly one versicon and what `DESIGN.md` calls versicons
have no name.
*Needs:* Ethan, as register-keeper. Note the register's entry is `archived`, so the
word is not in force in conversation either way. Whichever wins, the loser's
documents need a dated correction rather than a silent edit.

**Q9 · How do the branches of `versiconcordagraphs` relate to `main`?**
Deferred deliberately on 22 Sept. `main` holds the branch rule and nothing else; each
topic is an independent branch with unrelated history. The live question is whether
they ever compile, which is Q6 in another costume.
*Needs:* Ethan, after Q6.

---

**The question worth asking him first:** *which of these actually matters to you this
month?* Q1 is the only one that changes what the research says. Q3 is the only one
that is currently costing anything. The rest can wait, and the ranking above is one
agent's read of risk, not his priorities.
