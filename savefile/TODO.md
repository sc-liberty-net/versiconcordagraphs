# Todo — ranked by what it blocks

**Reconcile.** Close what ships, keep the numbers stable — they get referred to in
conversation — and add what is new.

**The ranking below is one agent's read of risk, not Ethan's priorities.** Ask him
which of these matters before working down it.

**The Mission Control Room is the authoritative queue**, not this file. Room tasks
49–66 are Biblography's and hold the full record of each — evidence, measurements,
sign-offs. This file says only *what each one blocks*, which the Room does not rank.
Where they disagree, the Room is right. Anything needing Ethan's authority rather than
an agent's work is in `QUESTIONS.md` instead.

---

## Blocking a second concordagraph

**1 · Quote the cluster key.**
`build_graph.py` emits cluster keys unquoted into a JS object literal; any key that is
not a bare identifier ships a blank page on a green build. Two lines — emit `{j(k)}`,
and widen `extract_corpus.py`'s cluster regex to accept a quoted key. Stops at Ethan's
go-ahead; it is live code.
*Blocks:* any concordagraph whose groups have two-word names, which is most of them.
Also blocks item 2, since a second module will want its own group names. Room 57,
`QUESTIONS.md` Q3.

**2 · Build the second module for real.**
"Wages" or similar, as its own branch of `versiconcordagraphs`. An agent built a
throwaway one during the design pass and it proved the three module decisions hold;
nothing of it was kept.
*Blocks:* the skill — everything that broke in the design pass broke on contact with a
second module. Also blocks 3 and `QUESTIONS.md` Q6.

**3 · Write the co-citation reporter.**
Eight lines over two `corpus_nodes.csv` files: which passages does more than one topic
claim, and what is each saying about them. An agent wrote and ran one during the
design pass; it found all six shared verses without any of the compile apparatus.
*Blocks:* the compare-or-compile decision (Q6). This is the cheap experiment that
answers it.

**4 · Then write the skill.**
Not before 2 and 3. The draft from 22 Sept is dead — see `DEAD-ENDS.md` — but its
diagnosis holds.
*Blocks:* a third and fourth concordagraph being built by hand, as the first three
were.

---

## Blocking a claim the project makes

**5 · Enforce "summaries are paraphrase, never NRSV wording."**
*Still open, and now overdue: the page is public.* Every node added on 25 Sept was
hand-checked against the five-word threshold before landing and two were rewritten for
it — so the discipline exists as a script in the scratchpad, not in the build.
`../CLAUDE.md` states the rule and nothing checks it; 22 of 151 already break it.
`build_graph.py` already holds the verse text in `raw` during its verify pass, so the
check costs almost nothing — flag any summary sharing a run of N+ consecutive words
with its verse, as a note rather than a refusal.
*Blocks:* the README's claim that the page is freely shareable because it carries only
references and summaries. Related to Q2, which is the editorial half.

**6 · Give the check-by-eye list a memory.**
It prints the same eleven ids on every build and blocks nothing, so it stops being
read. Record the cleared ids with the reason each was cleared, diff against it, and go
red only on a node that is new or whose summary has changed since.
*Blocks:* the list being trustworthy at 400 nodes across four topics. At 151 it is
still readable; that will not last.

---

## Worth doing, not urgent

**7 · Recover the 114 missing verses**, or decide they stay missing. Needs a different
splitting approach in `nrsv_index.py`, not a different extractor — that is settled.
No corpus node cites one today. Room 55.

**8 · ~~Delete the empty `files/` folder and the 22-byte `files.zip`.~~** Both are gone
from the working tree as of 25 Sept; the deletion of the tracked zip is still
uncommitted, and it belongs to whoever owns that change rather than to this session.
Room 50.

**9 · Make `build_graph.py` importable** so a second tool can reuse its rules instead
of re-implementing them. `argparse` is parsed at module scope, which is what stops it.
Nothing needs this until a second validator exists.

---

## Discussed, not started

**10 · A master compile.** Explicitly not built, and probably should not be until Q6
is answered. The apparatus a compile needs is larger than the payoff it delivers,
which the co-citation reporter demonstrates.

**11 · Reconcile the two meanings of "versicon".** `QUESTIONS.md` Q8. Whichever way it
goes, the losing document needs a dated correction rather than a silent edit.

---

## Closed 25 September 2026

**~~Two passages can carry only one connection.~~** Answered as Q5: one edge per pair
**per kind**. `build_graph.py`'s duplicate key is now the sorted pair plus the kind.
Proved red and green before it was trusted. First use un-flattened Matthew 9:9 to Mark
2:14, which had been carrying a `lex` claim and a `con` claim in one note. Room 59.

**~~Three passages carry no connection.~~** Answered as Q4: connect all three, plus a
fourth edge nobody had asked for. Every one chosen from a shared rare lemma rather than
by eye. Zero unconnected nodes remain. Room 58.

**~~Check Matthew 23:23 and Luke 11:42 by eye.~~** Answered as Q1 by Ethan: affirmed but
relativised, not rebuked. Cluster renamed, both gists rewritten. Room 54.

---

## New, 25 September 2026

**12 · Record the denominator on `lex` edges.**
The motif table carries a Bible-wide scope per motif and the page prints it. Individual
`lex` edges do not, so an edge resting on a 2-verse word and one resting on a 2,608-verse
word still render identically. Computable from `strongs_index.json`; a `scope` column on
`corpus_edges.csv`.
*Blocks:* motif work being weighable rather than assertable. This is the single
highest-leverage thing left.

**13 · Admit the backlog `crossexam.py` found.**
Roughly twenty edges and twenty nodes listed in the 25 Sept conversation and in
`motifs.pdf` — Micah 6:8, Hosea 6:6 with Matthew 9:13 and 12:7, Matthew 23:24, the
cup-and-tomb woes, Deuteronomy 14:22-23, Malachi 3:10, Luke 11:39-40.
*Blocks:* nothing mechanically. It is the research backlog.

**14 · Decide whether `motifs.pdf` should be published.**
It is caught by the `*.pdf` ignore rule, so it is local only, while `findings.pdf` has an
explicit exception and is public. Ethan's call.

**15 · A Septuagint layer.**
The lemma index is Hebrew OT plus Greek NT and Strong's numbers do not cross, so **no**
Old-to-New shared-wording claim is testable. github.com/nathans/lxx-swete is MIT-licensed and
Swete is a real critical edition; github.com/openscriptures/GreekResources carries the
LXX lemma data that Swete's plain text lacks.
*Blocks:* every cross-testament `lex` claim. The corpus currently makes zero, which is
the right discipline but is a limit rather than a choice.

**16 · Phone layout for the motif bar.**
The pills wrap and the rail stacks, but nothing has been driven at phone width since the
motif bar and About panel landed. Explicitly deferred by Ethan.

**17 · Fix `make_findings.py`'s output path.**
It writes to `/mnt/user-data/outputs/`, a Linux sandbox path, so `findings.pdf` cannot be
regenerated on this machine at all. One line. Held because the PDF it rebuilds is now
published and nobody has diffed a fresh build against the committed copy. Room 65.

**18 · The two index defects found while building the lemma layer.**
`Galatians`/`Galations` and `Psalm`/`Psalms` strand about thirty verses (Room 63); 161
duplicate Esther references make `attach_verses.py` silently return one of two texts
(Room 64). Both need a re-extraction and a deliberate `--record`, which is Ethan's call.
